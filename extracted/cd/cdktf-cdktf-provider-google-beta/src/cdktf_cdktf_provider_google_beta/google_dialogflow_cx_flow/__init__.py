r'''
# `google_dialogflow_cx_flow`

Refer to the Terraform Registry for docs: [`google_dialogflow_cx_flow`](https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow).
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


class GoogleDialogflowCxFlow(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDialogflowCxFlow.GoogleDialogflowCxFlow",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow google_dialogflow_cx_flow}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        display_name: builtins.str,
        advanced_settings: typing.Optional[typing.Union["GoogleDialogflowCxFlowAdvancedSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        description: typing.Optional[builtins.str] = None,
        event_handlers: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleDialogflowCxFlowEventHandlers", typing.Dict[builtins.str, typing.Any]]]]] = None,
        id: typing.Optional[builtins.str] = None,
        is_default_start_flow: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        knowledge_connector_settings: typing.Optional[typing.Union["GoogleDialogflowCxFlowKnowledgeConnectorSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        language_code: typing.Optional[builtins.str] = None,
        nlu_settings: typing.Optional[typing.Union["GoogleDialogflowCxFlowNluSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        parent: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["GoogleDialogflowCxFlowTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        transition_route_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
        transition_routes: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleDialogflowCxFlowTransitionRoutes", typing.Dict[builtins.str, typing.Any]]]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow google_dialogflow_cx_flow} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param display_name: The human-readable name of the flow. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#display_name GoogleDialogflowCxFlow#display_name}
        :param advanced_settings: advanced_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#advanced_settings GoogleDialogflowCxFlow#advanced_settings}
        :param description: The description of the flow. The maximum length is 500 characters. If exceeded, the request is rejected. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#description GoogleDialogflowCxFlow#description}
        :param event_handlers: event_handlers block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#event_handlers GoogleDialogflowCxFlow#event_handlers}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#id GoogleDialogflowCxFlow#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param is_default_start_flow: Marks this as the `Default Start Flow <https://cloud.google.com/dialogflow/cx/docs/concept/flow#start>`_ for an agent. When you create an agent, the Default Start Flow is created automatically. The Default Start Flow cannot be deleted; deleting the 'google_dialogflow_cx_flow' resource does nothing to the underlying GCP resources. ~> Avoid having multiple 'google_dialogflow_cx_flow' resources linked to the same agent with 'is_default_start_flow = true' because they will compete to control a single Default Start Flow resource in GCP. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#is_default_start_flow GoogleDialogflowCxFlow#is_default_start_flow}
        :param knowledge_connector_settings: knowledge_connector_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#knowledge_connector_settings GoogleDialogflowCxFlow#knowledge_connector_settings}
        :param language_code: The language of the following fields in flow: Flow.event_handlers.trigger_fulfillment.messages Flow.event_handlers.trigger_fulfillment.conditional_cases Flow.transition_routes.trigger_fulfillment.messages Flow.transition_routes.trigger_fulfillment.conditional_cases If not specified, the agent's default language is used. Many languages are supported. Note: languages must be enabled in the agent before they can be used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#language_code GoogleDialogflowCxFlow#language_code}
        :param nlu_settings: nlu_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#nlu_settings GoogleDialogflowCxFlow#nlu_settings}
        :param parent: The agent to create a flow for. Format: projects//locations//agents/. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#parent GoogleDialogflowCxFlow#parent}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#timeouts GoogleDialogflowCxFlow#timeouts}
        :param transition_route_groups: A flow's transition route group serve two purposes: They are responsible for matching the user's first utterances in the flow. They are inherited by every page's [transition route groups][Page.transition_route_groups]. Transition route groups defined in the page have higher priority than those defined in the flow. Format:projects//locations//agents//flows//transitionRouteGroups/. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#transition_route_groups GoogleDialogflowCxFlow#transition_route_groups}
        :param transition_routes: transition_routes block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#transition_routes GoogleDialogflowCxFlow#transition_routes}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ddc1c9bd1aaab871a2b80768c2bc499e93a36227c2ec26b6797aac6fac61ceb)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = GoogleDialogflowCxFlowConfig(
            display_name=display_name,
            advanced_settings=advanced_settings,
            description=description,
            event_handlers=event_handlers,
            id=id,
            is_default_start_flow=is_default_start_flow,
            knowledge_connector_settings=knowledge_connector_settings,
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
        '''Generates CDKTF code for importing a GoogleDialogflowCxFlow resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the GoogleDialogflowCxFlow to import.
        :param import_from_id: The id of the existing GoogleDialogflowCxFlow that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the GoogleDialogflowCxFlow to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ad3b054a471de21d0a367ca38d61ec2a1c86d28c7c7e15d0fa29c34cef2e8ffa)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putAdvancedSettings")
    def put_advanced_settings(
        self,
        *,
        audio_export_gcs_destination: typing.Optional[typing.Union["GoogleDialogflowCxFlowAdvancedSettingsAudioExportGcsDestination", typing.Dict[builtins.str, typing.Any]]] = None,
        dtmf_settings: typing.Optional[typing.Union["GoogleDialogflowCxFlowAdvancedSettingsDtmfSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        logging_settings: typing.Optional[typing.Union["GoogleDialogflowCxFlowAdvancedSettingsLoggingSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        speech_settings: typing.Optional[typing.Union["GoogleDialogflowCxFlowAdvancedSettingsSpeechSettings", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param audio_export_gcs_destination: audio_export_gcs_destination block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#audio_export_gcs_destination GoogleDialogflowCxFlow#audio_export_gcs_destination}
        :param dtmf_settings: dtmf_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#dtmf_settings GoogleDialogflowCxFlow#dtmf_settings}
        :param logging_settings: logging_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#logging_settings GoogleDialogflowCxFlow#logging_settings}
        :param speech_settings: speech_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#speech_settings GoogleDialogflowCxFlow#speech_settings}
        '''
        value = GoogleDialogflowCxFlowAdvancedSettings(
            audio_export_gcs_destination=audio_export_gcs_destination,
            dtmf_settings=dtmf_settings,
            logging_settings=logging_settings,
            speech_settings=speech_settings,
        )

        return typing.cast(None, jsii.invoke(self, "putAdvancedSettings", [value]))

    @jsii.member(jsii_name="putEventHandlers")
    def put_event_handlers(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleDialogflowCxFlowEventHandlers", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7d5763a95f2a19a20a2cee1cd63b8e22e995b6ccdda0bc67f0a8ba7c9afea462)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putEventHandlers", [value]))

    @jsii.member(jsii_name="putKnowledgeConnectorSettings")
    def put_knowledge_connector_settings(
        self,
        *,
        data_store_connections: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleDialogflowCxFlowKnowledgeConnectorSettingsDataStoreConnections", typing.Dict[builtins.str, typing.Any]]]]] = None,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        target_flow: typing.Optional[builtins.str] = None,
        target_page: typing.Optional[builtins.str] = None,
        trigger_fulfillment: typing.Optional[typing.Union["GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillment", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param data_store_connections: data_store_connections block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#data_store_connections GoogleDialogflowCxFlow#data_store_connections}
        :param enabled: Whether Knowledge Connector is enabled or not. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#enabled GoogleDialogflowCxFlow#enabled}
        :param target_flow: The target flow to transition to. Format: projects//locations//agents//flows/. This field is part of a union field 'target': Only one of 'targetPage' or 'targetFlow' may be set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#target_flow GoogleDialogflowCxFlow#target_flow}
        :param target_page: The target page to transition to. Format: projects//locations//agents//flows//pages/. The page must be in the same host flow (the flow that owns this 'KnowledgeConnectorSettings'). This field is part of a union field 'target': Only one of 'targetPage' or 'targetFlow' may be set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#target_page GoogleDialogflowCxFlow#target_page}
        :param trigger_fulfillment: trigger_fulfillment block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#trigger_fulfillment GoogleDialogflowCxFlow#trigger_fulfillment}
        '''
        value = GoogleDialogflowCxFlowKnowledgeConnectorSettings(
            data_store_connections=data_store_connections,
            enabled=enabled,
            target_flow=target_flow,
            target_page=target_page,
            trigger_fulfillment=trigger_fulfillment,
        )

        return typing.cast(None, jsii.invoke(self, "putKnowledgeConnectorSettings", [value]))

    @jsii.member(jsii_name="putNluSettings")
    def put_nlu_settings(
        self,
        *,
        classification_threshold: typing.Optional[jsii.Number] = None,
        model_training_mode: typing.Optional[builtins.str] = None,
        model_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param classification_threshold: To filter out false positive results and still get variety in matched natural language inputs for your agent, you can tune the machine learning classification threshold. If the returned score value is less than the threshold value, then a no-match event will be triggered. The score values range from 0.0 (completely uncertain) to 1.0 (completely certain). If set to 0.0, the default of 0.3 is used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#classification_threshold GoogleDialogflowCxFlow#classification_threshold}
        :param model_training_mode: Indicates NLU model training mode. - MODEL_TRAINING_MODE_AUTOMATIC: NLU model training is automatically triggered when a flow gets modified. User can also manually trigger model training in this mode. - MODEL_TRAINING_MODE_MANUAL: User needs to manually trigger NLU model training. Best for large flows whose models take long time to train. Possible values: ["MODEL_TRAINING_MODE_AUTOMATIC", "MODEL_TRAINING_MODE_MANUAL"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#model_training_mode GoogleDialogflowCxFlow#model_training_mode}
        :param model_type: Indicates the type of NLU model. - MODEL_TYPE_STANDARD: Use standard NLU model. - MODEL_TYPE_ADVANCED: Use advanced NLU model. Possible values: ["MODEL_TYPE_STANDARD", "MODEL_TYPE_ADVANCED"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#model_type GoogleDialogflowCxFlow#model_type}
        '''
        value = GoogleDialogflowCxFlowNluSettings(
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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#create GoogleDialogflowCxFlow#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#delete GoogleDialogflowCxFlow#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#update GoogleDialogflowCxFlow#update}.
        '''
        value = GoogleDialogflowCxFlowTimeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="putTransitionRoutes")
    def put_transition_routes(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleDialogflowCxFlowTransitionRoutes", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3f67d14e084641d1578e154aed126fcf46d108e0c8f21351b034db072abbe3b8)
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

    @jsii.member(jsii_name="resetKnowledgeConnectorSettings")
    def reset_knowledge_connector_settings(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKnowledgeConnectorSettings", []))

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
    def advanced_settings(
        self,
    ) -> "GoogleDialogflowCxFlowAdvancedSettingsOutputReference":
        return typing.cast("GoogleDialogflowCxFlowAdvancedSettingsOutputReference", jsii.get(self, "advancedSettings"))

    @builtins.property
    @jsii.member(jsii_name="eventHandlers")
    def event_handlers(self) -> "GoogleDialogflowCxFlowEventHandlersList":
        return typing.cast("GoogleDialogflowCxFlowEventHandlersList", jsii.get(self, "eventHandlers"))

    @builtins.property
    @jsii.member(jsii_name="knowledgeConnectorSettings")
    def knowledge_connector_settings(
        self,
    ) -> "GoogleDialogflowCxFlowKnowledgeConnectorSettingsOutputReference":
        return typing.cast("GoogleDialogflowCxFlowKnowledgeConnectorSettingsOutputReference", jsii.get(self, "knowledgeConnectorSettings"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="nluSettings")
    def nlu_settings(self) -> "GoogleDialogflowCxFlowNluSettingsOutputReference":
        return typing.cast("GoogleDialogflowCxFlowNluSettingsOutputReference", jsii.get(self, "nluSettings"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "GoogleDialogflowCxFlowTimeoutsOutputReference":
        return typing.cast("GoogleDialogflowCxFlowTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="transitionRoutes")
    def transition_routes(self) -> "GoogleDialogflowCxFlowTransitionRoutesList":
        return typing.cast("GoogleDialogflowCxFlowTransitionRoutesList", jsii.get(self, "transitionRoutes"))

    @builtins.property
    @jsii.member(jsii_name="advancedSettingsInput")
    def advanced_settings_input(
        self,
    ) -> typing.Optional["GoogleDialogflowCxFlowAdvancedSettings"]:
        return typing.cast(typing.Optional["GoogleDialogflowCxFlowAdvancedSettings"], jsii.get(self, "advancedSettingsInput"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleDialogflowCxFlowEventHandlers"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleDialogflowCxFlowEventHandlers"]]], jsii.get(self, "eventHandlersInput"))

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
    @jsii.member(jsii_name="knowledgeConnectorSettingsInput")
    def knowledge_connector_settings_input(
        self,
    ) -> typing.Optional["GoogleDialogflowCxFlowKnowledgeConnectorSettings"]:
        return typing.cast(typing.Optional["GoogleDialogflowCxFlowKnowledgeConnectorSettings"], jsii.get(self, "knowledgeConnectorSettingsInput"))

    @builtins.property
    @jsii.member(jsii_name="languageCodeInput")
    def language_code_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "languageCodeInput"))

    @builtins.property
    @jsii.member(jsii_name="nluSettingsInput")
    def nlu_settings_input(
        self,
    ) -> typing.Optional["GoogleDialogflowCxFlowNluSettings"]:
        return typing.cast(typing.Optional["GoogleDialogflowCxFlowNluSettings"], jsii.get(self, "nluSettingsInput"))

    @builtins.property
    @jsii.member(jsii_name="parentInput")
    def parent_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "parentInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleDialogflowCxFlowTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleDialogflowCxFlowTimeouts"]], jsii.get(self, "timeoutsInput"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleDialogflowCxFlowTransitionRoutes"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleDialogflowCxFlowTransitionRoutes"]]], jsii.get(self, "transitionRoutesInput"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7564a7905ff3d080ec73fd5b3674d80316185888f34b793426007f2891348fc4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="displayName")
    def display_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "displayName"))

    @display_name.setter
    def display_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3d57e353ea4e0c1dbefde806a99b8c916a02fa1ed2fdd994823bfcf5422e9934)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "displayName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eab5ec690ece1ff9fa75d59b2a15d2b7ececfba9a83206cd737e9f2f7198cb5b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bc61fcc21cb3d353f84d5d4e88bdffe57d189d4c895ab85b7d3f152168394a73)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "isDefaultStartFlow", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="languageCode")
    def language_code(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "languageCode"))

    @language_code.setter
    def language_code(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fb70b48e85ea80ce1f103a0c05a4b3466c57a382c528c7a81ce07b3b8df410ec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "languageCode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="parent")
    def parent(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "parent"))

    @parent.setter
    def parent(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a48c675e5612a9b38a6595f66082b141506e7336639e253e7d20e4b003a2e87d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "parent", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="transitionRouteGroups")
    def transition_route_groups(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "transitionRouteGroups"))

    @transition_route_groups.setter
    def transition_route_groups(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c8b9d2da6f549846ac8b8c3ea7bb8b102639d483550c7cb5ff7fa1924d572b11)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "transitionRouteGroups", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDialogflowCxFlow.GoogleDialogflowCxFlowAdvancedSettings",
    jsii_struct_bases=[],
    name_mapping={
        "audio_export_gcs_destination": "audioExportGcsDestination",
        "dtmf_settings": "dtmfSettings",
        "logging_settings": "loggingSettings",
        "speech_settings": "speechSettings",
    },
)
class GoogleDialogflowCxFlowAdvancedSettings:
    def __init__(
        self,
        *,
        audio_export_gcs_destination: typing.Optional[typing.Union["GoogleDialogflowCxFlowAdvancedSettingsAudioExportGcsDestination", typing.Dict[builtins.str, typing.Any]]] = None,
        dtmf_settings: typing.Optional[typing.Union["GoogleDialogflowCxFlowAdvancedSettingsDtmfSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        logging_settings: typing.Optional[typing.Union["GoogleDialogflowCxFlowAdvancedSettingsLoggingSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        speech_settings: typing.Optional[typing.Union["GoogleDialogflowCxFlowAdvancedSettingsSpeechSettings", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param audio_export_gcs_destination: audio_export_gcs_destination block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#audio_export_gcs_destination GoogleDialogflowCxFlow#audio_export_gcs_destination}
        :param dtmf_settings: dtmf_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#dtmf_settings GoogleDialogflowCxFlow#dtmf_settings}
        :param logging_settings: logging_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#logging_settings GoogleDialogflowCxFlow#logging_settings}
        :param speech_settings: speech_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#speech_settings GoogleDialogflowCxFlow#speech_settings}
        '''
        if isinstance(audio_export_gcs_destination, dict):
            audio_export_gcs_destination = GoogleDialogflowCxFlowAdvancedSettingsAudioExportGcsDestination(**audio_export_gcs_destination)
        if isinstance(dtmf_settings, dict):
            dtmf_settings = GoogleDialogflowCxFlowAdvancedSettingsDtmfSettings(**dtmf_settings)
        if isinstance(logging_settings, dict):
            logging_settings = GoogleDialogflowCxFlowAdvancedSettingsLoggingSettings(**logging_settings)
        if isinstance(speech_settings, dict):
            speech_settings = GoogleDialogflowCxFlowAdvancedSettingsSpeechSettings(**speech_settings)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__74522f9b5137db65e0921cf1c5e8aa67898022072b01667d01626b26b51a97d4)
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
    ) -> typing.Optional["GoogleDialogflowCxFlowAdvancedSettingsAudioExportGcsDestination"]:
        '''audio_export_gcs_destination block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#audio_export_gcs_destination GoogleDialogflowCxFlow#audio_export_gcs_destination}
        '''
        result = self._values.get("audio_export_gcs_destination")
        return typing.cast(typing.Optional["GoogleDialogflowCxFlowAdvancedSettingsAudioExportGcsDestination"], result)

    @builtins.property
    def dtmf_settings(
        self,
    ) -> typing.Optional["GoogleDialogflowCxFlowAdvancedSettingsDtmfSettings"]:
        '''dtmf_settings block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#dtmf_settings GoogleDialogflowCxFlow#dtmf_settings}
        '''
        result = self._values.get("dtmf_settings")
        return typing.cast(typing.Optional["GoogleDialogflowCxFlowAdvancedSettingsDtmfSettings"], result)

    @builtins.property
    def logging_settings(
        self,
    ) -> typing.Optional["GoogleDialogflowCxFlowAdvancedSettingsLoggingSettings"]:
        '''logging_settings block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#logging_settings GoogleDialogflowCxFlow#logging_settings}
        '''
        result = self._values.get("logging_settings")
        return typing.cast(typing.Optional["GoogleDialogflowCxFlowAdvancedSettingsLoggingSettings"], result)

    @builtins.property
    def speech_settings(
        self,
    ) -> typing.Optional["GoogleDialogflowCxFlowAdvancedSettingsSpeechSettings"]:
        '''speech_settings block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#speech_settings GoogleDialogflowCxFlow#speech_settings}
        '''
        result = self._values.get("speech_settings")
        return typing.cast(typing.Optional["GoogleDialogflowCxFlowAdvancedSettingsSpeechSettings"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDialogflowCxFlowAdvancedSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDialogflowCxFlow.GoogleDialogflowCxFlowAdvancedSettingsAudioExportGcsDestination",
    jsii_struct_bases=[],
    name_mapping={"uri": "uri"},
)
class GoogleDialogflowCxFlowAdvancedSettingsAudioExportGcsDestination:
    def __init__(self, *, uri: typing.Optional[builtins.str] = None) -> None:
        '''
        :param uri: The Google Cloud Storage URI for the exported objects. Whether a full object name, or just a prefix, its usage depends on the Dialogflow operation. Format: gs://bucket/object-name-or-prefix Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#uri GoogleDialogflowCxFlow#uri}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f14a90e7cb3882840e4ec911e01e5451e2d8b19a9979b602f4294dbcd64ba59c)
            check_type(argname="argument uri", value=uri, expected_type=type_hints["uri"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if uri is not None:
            self._values["uri"] = uri

    @builtins.property
    def uri(self) -> typing.Optional[builtins.str]:
        '''The Google Cloud Storage URI for the exported objects.

        Whether a full object name, or just a prefix, its usage depends on the Dialogflow operation.
        Format: gs://bucket/object-name-or-prefix

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#uri GoogleDialogflowCxFlow#uri}
        '''
        result = self._values.get("uri")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDialogflowCxFlowAdvancedSettingsAudioExportGcsDestination(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDialogflowCxFlowAdvancedSettingsAudioExportGcsDestinationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDialogflowCxFlow.GoogleDialogflowCxFlowAdvancedSettingsAudioExportGcsDestinationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__126bfaf474003387ad65638cfd0a1d944237446dd9255e7e0c74b0ed088028dc)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bcf8efda4b84a8fbcd37d884c901b0367ea99053549c30a600b982d7b6ae0208)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "uri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDialogflowCxFlowAdvancedSettingsAudioExportGcsDestination]:
        return typing.cast(typing.Optional[GoogleDialogflowCxFlowAdvancedSettingsAudioExportGcsDestination], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDialogflowCxFlowAdvancedSettingsAudioExportGcsDestination],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6753a3d1e6d9677e891ba03b4be61d55b680366939ab6a465ec78726af5affdc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDialogflowCxFlow.GoogleDialogflowCxFlowAdvancedSettingsDtmfSettings",
    jsii_struct_bases=[],
    name_mapping={
        "enabled": "enabled",
        "finish_digit": "finishDigit",
        "max_digits": "maxDigits",
    },
)
class GoogleDialogflowCxFlowAdvancedSettingsDtmfSettings:
    def __init__(
        self,
        *,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        finish_digit: typing.Optional[builtins.str] = None,
        max_digits: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param enabled: If true, incoming audio is processed for DTMF (dual tone multi frequency) events. For example, if the caller presses a button on their telephone keypad and DTMF processing is enabled, Dialogflow will detect the event (e.g. a "3" was pressed) in the incoming audio and pass the event to the bot to drive business logic (e.g. when 3 is pressed, return the account balance). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#enabled GoogleDialogflowCxFlow#enabled}
        :param finish_digit: The digit that terminates a DTMF digit sequence. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#finish_digit GoogleDialogflowCxFlow#finish_digit}
        :param max_digits: Max length of DTMF digits. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#max_digits GoogleDialogflowCxFlow#max_digits}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dbbd4cad34ff6aa630667af905d7c23565c8b573fc94b53aeedc8657f064a053)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#enabled GoogleDialogflowCxFlow#enabled}
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def finish_digit(self) -> typing.Optional[builtins.str]:
        '''The digit that terminates a DTMF digit sequence.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#finish_digit GoogleDialogflowCxFlow#finish_digit}
        '''
        result = self._values.get("finish_digit")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def max_digits(self) -> typing.Optional[jsii.Number]:
        '''Max length of DTMF digits.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#max_digits GoogleDialogflowCxFlow#max_digits}
        '''
        result = self._values.get("max_digits")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDialogflowCxFlowAdvancedSettingsDtmfSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDialogflowCxFlowAdvancedSettingsDtmfSettingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDialogflowCxFlow.GoogleDialogflowCxFlowAdvancedSettingsDtmfSettingsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__94e13c969a0969e8c13bac2c5a7a19f17db5928989f957c7eff5e02b1285b21c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__444113a02773315b4f4224c440ff697f2d51c4eb404fb307174f2a56c5ff5bfb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="finishDigit")
    def finish_digit(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "finishDigit"))

    @finish_digit.setter
    def finish_digit(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__080fea3290e7f671c0b7921f05c14cfde7ad37d6a3ae820c5301a730c89c0ba4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "finishDigit", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxDigits")
    def max_digits(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxDigits"))

    @max_digits.setter
    def max_digits(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__79d79812fc802c105c6e8454b68dff149578f978375c174f256286489e456019)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxDigits", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDialogflowCxFlowAdvancedSettingsDtmfSettings]:
        return typing.cast(typing.Optional[GoogleDialogflowCxFlowAdvancedSettingsDtmfSettings], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDialogflowCxFlowAdvancedSettingsDtmfSettings],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5d36606aa4eb8bd597c3494f9c89fb89e5f555047331abb521468e0e51933e94)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDialogflowCxFlow.GoogleDialogflowCxFlowAdvancedSettingsLoggingSettings",
    jsii_struct_bases=[],
    name_mapping={
        "enable_consent_based_redaction": "enableConsentBasedRedaction",
        "enable_interaction_logging": "enableInteractionLogging",
        "enable_stackdriver_logging": "enableStackdriverLogging",
    },
)
class GoogleDialogflowCxFlowAdvancedSettingsLoggingSettings:
    def __init__(
        self,
        *,
        enable_consent_based_redaction: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_interaction_logging: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_stackdriver_logging: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param enable_consent_based_redaction: Enables consent-based end-user input redaction, if true, a pre-defined session parameter **$session.params.conversation-redaction** will be used to determine if the utterance should be redacted. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#enable_consent_based_redaction GoogleDialogflowCxFlow#enable_consent_based_redaction}
        :param enable_interaction_logging: Enables DF Interaction logging. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#enable_interaction_logging GoogleDialogflowCxFlow#enable_interaction_logging}
        :param enable_stackdriver_logging: Enables Google Cloud Logging. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#enable_stackdriver_logging GoogleDialogflowCxFlow#enable_stackdriver_logging}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3492a20de1578c5c1d3da93c3c3beb7951c686d51823edd9730603c329cfac98)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#enable_consent_based_redaction GoogleDialogflowCxFlow#enable_consent_based_redaction}
        '''
        result = self._values.get("enable_consent_based_redaction")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def enable_interaction_logging(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Enables DF Interaction logging.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#enable_interaction_logging GoogleDialogflowCxFlow#enable_interaction_logging}
        '''
        result = self._values.get("enable_interaction_logging")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def enable_stackdriver_logging(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Enables Google Cloud Logging.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#enable_stackdriver_logging GoogleDialogflowCxFlow#enable_stackdriver_logging}
        '''
        result = self._values.get("enable_stackdriver_logging")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDialogflowCxFlowAdvancedSettingsLoggingSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDialogflowCxFlowAdvancedSettingsLoggingSettingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDialogflowCxFlow.GoogleDialogflowCxFlowAdvancedSettingsLoggingSettingsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__eda197ee35e2807c014125376afc7f94d02f5134ff62b3175995252f225a43e3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__38398b43bc6f1b41b7d99174462ef2aac48d94bae30ee43ea74ec23337c2b288)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d5115bf01330153cb029216351ce854be302723316e25d50b61af4e3a6437642)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bfa2016117ffbd080867f9afc0a524229692dbd88ca49e57d688d600135d97a9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableStackdriverLogging", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDialogflowCxFlowAdvancedSettingsLoggingSettings]:
        return typing.cast(typing.Optional[GoogleDialogflowCxFlowAdvancedSettingsLoggingSettings], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDialogflowCxFlowAdvancedSettingsLoggingSettings],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__42733c4b44cc0960d1e468fdab957bed90caa698a8ccd72a0e2f48e116fe1756)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleDialogflowCxFlowAdvancedSettingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDialogflowCxFlow.GoogleDialogflowCxFlowAdvancedSettingsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0a4cfef87b8c76c85a3fbfc1b57d3fdf6b29e64131a20d9a3f54dc95a49cf56d)
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
        :param uri: The Google Cloud Storage URI for the exported objects. Whether a full object name, or just a prefix, its usage depends on the Dialogflow operation. Format: gs://bucket/object-name-or-prefix Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#uri GoogleDialogflowCxFlow#uri}
        '''
        value = GoogleDialogflowCxFlowAdvancedSettingsAudioExportGcsDestination(
            uri=uri
        )

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
        :param enabled: If true, incoming audio is processed for DTMF (dual tone multi frequency) events. For example, if the caller presses a button on their telephone keypad and DTMF processing is enabled, Dialogflow will detect the event (e.g. a "3" was pressed) in the incoming audio and pass the event to the bot to drive business logic (e.g. when 3 is pressed, return the account balance). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#enabled GoogleDialogflowCxFlow#enabled}
        :param finish_digit: The digit that terminates a DTMF digit sequence. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#finish_digit GoogleDialogflowCxFlow#finish_digit}
        :param max_digits: Max length of DTMF digits. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#max_digits GoogleDialogflowCxFlow#max_digits}
        '''
        value = GoogleDialogflowCxFlowAdvancedSettingsDtmfSettings(
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
        :param enable_consent_based_redaction: Enables consent-based end-user input redaction, if true, a pre-defined session parameter **$session.params.conversation-redaction** will be used to determine if the utterance should be redacted. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#enable_consent_based_redaction GoogleDialogflowCxFlow#enable_consent_based_redaction}
        :param enable_interaction_logging: Enables DF Interaction logging. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#enable_interaction_logging GoogleDialogflowCxFlow#enable_interaction_logging}
        :param enable_stackdriver_logging: Enables Google Cloud Logging. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#enable_stackdriver_logging GoogleDialogflowCxFlow#enable_stackdriver_logging}
        '''
        value = GoogleDialogflowCxFlowAdvancedSettingsLoggingSettings(
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
        :param endpointer_sensitivity: Sensitivity of the speech model that detects the end of speech. Scale from 0 to 100. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#endpointer_sensitivity GoogleDialogflowCxFlow#endpointer_sensitivity}
        :param models: Mapping from language to Speech-to-Text model. The mapped Speech-to-Text model will be selected for requests from its corresponding language. For more information, see `Speech models <https://cloud.google.com/dialogflow/cx/docs/concept/speech-models>`_. An object containing a list of **"key": value** pairs. Example: **{ "name": "wrench", "mass": "1.3kg", "count": "3" }**. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#models GoogleDialogflowCxFlow#models}
        :param no_speech_timeout: Timeout before detecting no speech. A duration in seconds with up to nine fractional digits, ending with 's'. Example: "3.5s". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#no_speech_timeout GoogleDialogflowCxFlow#no_speech_timeout}
        :param use_timeout_based_endpointing: Use timeout based endpointing, interpreting endpointer sensitivity as seconds of timeout value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#use_timeout_based_endpointing GoogleDialogflowCxFlow#use_timeout_based_endpointing}
        '''
        value = GoogleDialogflowCxFlowAdvancedSettingsSpeechSettings(
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
    ) -> GoogleDialogflowCxFlowAdvancedSettingsAudioExportGcsDestinationOutputReference:
        return typing.cast(GoogleDialogflowCxFlowAdvancedSettingsAudioExportGcsDestinationOutputReference, jsii.get(self, "audioExportGcsDestination"))

    @builtins.property
    @jsii.member(jsii_name="dtmfSettings")
    def dtmf_settings(
        self,
    ) -> GoogleDialogflowCxFlowAdvancedSettingsDtmfSettingsOutputReference:
        return typing.cast(GoogleDialogflowCxFlowAdvancedSettingsDtmfSettingsOutputReference, jsii.get(self, "dtmfSettings"))

    @builtins.property
    @jsii.member(jsii_name="loggingSettings")
    def logging_settings(
        self,
    ) -> GoogleDialogflowCxFlowAdvancedSettingsLoggingSettingsOutputReference:
        return typing.cast(GoogleDialogflowCxFlowAdvancedSettingsLoggingSettingsOutputReference, jsii.get(self, "loggingSettings"))

    @builtins.property
    @jsii.member(jsii_name="speechSettings")
    def speech_settings(
        self,
    ) -> "GoogleDialogflowCxFlowAdvancedSettingsSpeechSettingsOutputReference":
        return typing.cast("GoogleDialogflowCxFlowAdvancedSettingsSpeechSettingsOutputReference", jsii.get(self, "speechSettings"))

    @builtins.property
    @jsii.member(jsii_name="audioExportGcsDestinationInput")
    def audio_export_gcs_destination_input(
        self,
    ) -> typing.Optional[GoogleDialogflowCxFlowAdvancedSettingsAudioExportGcsDestination]:
        return typing.cast(typing.Optional[GoogleDialogflowCxFlowAdvancedSettingsAudioExportGcsDestination], jsii.get(self, "audioExportGcsDestinationInput"))

    @builtins.property
    @jsii.member(jsii_name="dtmfSettingsInput")
    def dtmf_settings_input(
        self,
    ) -> typing.Optional[GoogleDialogflowCxFlowAdvancedSettingsDtmfSettings]:
        return typing.cast(typing.Optional[GoogleDialogflowCxFlowAdvancedSettingsDtmfSettings], jsii.get(self, "dtmfSettingsInput"))

    @builtins.property
    @jsii.member(jsii_name="loggingSettingsInput")
    def logging_settings_input(
        self,
    ) -> typing.Optional[GoogleDialogflowCxFlowAdvancedSettingsLoggingSettings]:
        return typing.cast(typing.Optional[GoogleDialogflowCxFlowAdvancedSettingsLoggingSettings], jsii.get(self, "loggingSettingsInput"))

    @builtins.property
    @jsii.member(jsii_name="speechSettingsInput")
    def speech_settings_input(
        self,
    ) -> typing.Optional["GoogleDialogflowCxFlowAdvancedSettingsSpeechSettings"]:
        return typing.cast(typing.Optional["GoogleDialogflowCxFlowAdvancedSettingsSpeechSettings"], jsii.get(self, "speechSettingsInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GoogleDialogflowCxFlowAdvancedSettings]:
        return typing.cast(typing.Optional[GoogleDialogflowCxFlowAdvancedSettings], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDialogflowCxFlowAdvancedSettings],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf2a7517d1b6799be5bbd2bca26336584a9c1d7021407f29c7456dedcdffaa7c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDialogflowCxFlow.GoogleDialogflowCxFlowAdvancedSettingsSpeechSettings",
    jsii_struct_bases=[],
    name_mapping={
        "endpointer_sensitivity": "endpointerSensitivity",
        "models": "models",
        "no_speech_timeout": "noSpeechTimeout",
        "use_timeout_based_endpointing": "useTimeoutBasedEndpointing",
    },
)
class GoogleDialogflowCxFlowAdvancedSettingsSpeechSettings:
    def __init__(
        self,
        *,
        endpointer_sensitivity: typing.Optional[jsii.Number] = None,
        models: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        no_speech_timeout: typing.Optional[builtins.str] = None,
        use_timeout_based_endpointing: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param endpointer_sensitivity: Sensitivity of the speech model that detects the end of speech. Scale from 0 to 100. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#endpointer_sensitivity GoogleDialogflowCxFlow#endpointer_sensitivity}
        :param models: Mapping from language to Speech-to-Text model. The mapped Speech-to-Text model will be selected for requests from its corresponding language. For more information, see `Speech models <https://cloud.google.com/dialogflow/cx/docs/concept/speech-models>`_. An object containing a list of **"key": value** pairs. Example: **{ "name": "wrench", "mass": "1.3kg", "count": "3" }**. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#models GoogleDialogflowCxFlow#models}
        :param no_speech_timeout: Timeout before detecting no speech. A duration in seconds with up to nine fractional digits, ending with 's'. Example: "3.5s". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#no_speech_timeout GoogleDialogflowCxFlow#no_speech_timeout}
        :param use_timeout_based_endpointing: Use timeout based endpointing, interpreting endpointer sensitivity as seconds of timeout value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#use_timeout_based_endpointing GoogleDialogflowCxFlow#use_timeout_based_endpointing}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b64a57b0c34c8d30441358acced2700a3b48fec9630d061356c581d519ce94e7)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#endpointer_sensitivity GoogleDialogflowCxFlow#endpointer_sensitivity}
        '''
        result = self._values.get("endpointer_sensitivity")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def models(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Mapping from language to Speech-to-Text model.

        The mapped Speech-to-Text model will be selected for requests from its corresponding language. For more information, see `Speech models <https://cloud.google.com/dialogflow/cx/docs/concept/speech-models>`_.
        An object containing a list of **"key": value** pairs. Example: **{ "name": "wrench", "mass": "1.3kg", "count": "3" }**.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#models GoogleDialogflowCxFlow#models}
        '''
        result = self._values.get("models")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def no_speech_timeout(self) -> typing.Optional[builtins.str]:
        '''Timeout before detecting no speech. A duration in seconds with up to nine fractional digits, ending with 's'. Example: "3.5s".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#no_speech_timeout GoogleDialogflowCxFlow#no_speech_timeout}
        '''
        result = self._values.get("no_speech_timeout")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def use_timeout_based_endpointing(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Use timeout based endpointing, interpreting endpointer sensitivity as seconds of timeout value.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#use_timeout_based_endpointing GoogleDialogflowCxFlow#use_timeout_based_endpointing}
        '''
        result = self._values.get("use_timeout_based_endpointing")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDialogflowCxFlowAdvancedSettingsSpeechSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDialogflowCxFlowAdvancedSettingsSpeechSettingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDialogflowCxFlow.GoogleDialogflowCxFlowAdvancedSettingsSpeechSettingsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__373c7d629578331f1a8b8da6aba231d69c324dd2eea9b4c3e1e8f3af0c55a085)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1e8af063947de8ed1d7a7875ca13ab6e3c88628ff99ad2764e7037bf76d30276)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "endpointerSensitivity", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="models")
    def models(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "models"))

    @models.setter
    def models(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3860718a3f419c431bb5ce68d767688868f3d6436ac512fe59a00177a3b585ff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "models", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="noSpeechTimeout")
    def no_speech_timeout(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "noSpeechTimeout"))

    @no_speech_timeout.setter
    def no_speech_timeout(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__68ee48cb429657778e991d921e8f985675b5abe21a5553c7a25f8c3e9893da20)
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
            type_hints = typing.get_type_hints(_typecheckingstub__54ace7069c2f5634036911d0430435b34c9f393ba0b8d46e17d82cd60a22979b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "useTimeoutBasedEndpointing", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDialogflowCxFlowAdvancedSettingsSpeechSettings]:
        return typing.cast(typing.Optional[GoogleDialogflowCxFlowAdvancedSettingsSpeechSettings], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDialogflowCxFlowAdvancedSettingsSpeechSettings],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__990fa67d3660106df9524adc4b6476553f3e3912f5f307ea5d196b451508519e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDialogflowCxFlow.GoogleDialogflowCxFlowConfig",
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
        "knowledge_connector_settings": "knowledgeConnectorSettings",
        "language_code": "languageCode",
        "nlu_settings": "nluSettings",
        "parent": "parent",
        "timeouts": "timeouts",
        "transition_route_groups": "transitionRouteGroups",
        "transition_routes": "transitionRoutes",
    },
)
class GoogleDialogflowCxFlowConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        advanced_settings: typing.Optional[typing.Union[GoogleDialogflowCxFlowAdvancedSettings, typing.Dict[builtins.str, typing.Any]]] = None,
        description: typing.Optional[builtins.str] = None,
        event_handlers: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleDialogflowCxFlowEventHandlers", typing.Dict[builtins.str, typing.Any]]]]] = None,
        id: typing.Optional[builtins.str] = None,
        is_default_start_flow: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        knowledge_connector_settings: typing.Optional[typing.Union["GoogleDialogflowCxFlowKnowledgeConnectorSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        language_code: typing.Optional[builtins.str] = None,
        nlu_settings: typing.Optional[typing.Union["GoogleDialogflowCxFlowNluSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        parent: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["GoogleDialogflowCxFlowTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        transition_route_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
        transition_routes: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleDialogflowCxFlowTransitionRoutes", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param display_name: The human-readable name of the flow. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#display_name GoogleDialogflowCxFlow#display_name}
        :param advanced_settings: advanced_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#advanced_settings GoogleDialogflowCxFlow#advanced_settings}
        :param description: The description of the flow. The maximum length is 500 characters. If exceeded, the request is rejected. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#description GoogleDialogflowCxFlow#description}
        :param event_handlers: event_handlers block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#event_handlers GoogleDialogflowCxFlow#event_handlers}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#id GoogleDialogflowCxFlow#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param is_default_start_flow: Marks this as the `Default Start Flow <https://cloud.google.com/dialogflow/cx/docs/concept/flow#start>`_ for an agent. When you create an agent, the Default Start Flow is created automatically. The Default Start Flow cannot be deleted; deleting the 'google_dialogflow_cx_flow' resource does nothing to the underlying GCP resources. ~> Avoid having multiple 'google_dialogflow_cx_flow' resources linked to the same agent with 'is_default_start_flow = true' because they will compete to control a single Default Start Flow resource in GCP. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#is_default_start_flow GoogleDialogflowCxFlow#is_default_start_flow}
        :param knowledge_connector_settings: knowledge_connector_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#knowledge_connector_settings GoogleDialogflowCxFlow#knowledge_connector_settings}
        :param language_code: The language of the following fields in flow: Flow.event_handlers.trigger_fulfillment.messages Flow.event_handlers.trigger_fulfillment.conditional_cases Flow.transition_routes.trigger_fulfillment.messages Flow.transition_routes.trigger_fulfillment.conditional_cases If not specified, the agent's default language is used. Many languages are supported. Note: languages must be enabled in the agent before they can be used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#language_code GoogleDialogflowCxFlow#language_code}
        :param nlu_settings: nlu_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#nlu_settings GoogleDialogflowCxFlow#nlu_settings}
        :param parent: The agent to create a flow for. Format: projects//locations//agents/. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#parent GoogleDialogflowCxFlow#parent}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#timeouts GoogleDialogflowCxFlow#timeouts}
        :param transition_route_groups: A flow's transition route group serve two purposes: They are responsible for matching the user's first utterances in the flow. They are inherited by every page's [transition route groups][Page.transition_route_groups]. Transition route groups defined in the page have higher priority than those defined in the flow. Format:projects//locations//agents//flows//transitionRouteGroups/. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#transition_route_groups GoogleDialogflowCxFlow#transition_route_groups}
        :param transition_routes: transition_routes block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#transition_routes GoogleDialogflowCxFlow#transition_routes}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(advanced_settings, dict):
            advanced_settings = GoogleDialogflowCxFlowAdvancedSettings(**advanced_settings)
        if isinstance(knowledge_connector_settings, dict):
            knowledge_connector_settings = GoogleDialogflowCxFlowKnowledgeConnectorSettings(**knowledge_connector_settings)
        if isinstance(nlu_settings, dict):
            nlu_settings = GoogleDialogflowCxFlowNluSettings(**nlu_settings)
        if isinstance(timeouts, dict):
            timeouts = GoogleDialogflowCxFlowTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c5b6d22821ccb6c1261edc07f6bc6656e98299156ae0eaee2da8542a3e22cb90)
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
            check_type(argname="argument knowledge_connector_settings", value=knowledge_connector_settings, expected_type=type_hints["knowledge_connector_settings"])
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
        if knowledge_connector_settings is not None:
            self._values["knowledge_connector_settings"] = knowledge_connector_settings
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#display_name GoogleDialogflowCxFlow#display_name}
        '''
        result = self._values.get("display_name")
        assert result is not None, "Required property 'display_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def advanced_settings(
        self,
    ) -> typing.Optional[GoogleDialogflowCxFlowAdvancedSettings]:
        '''advanced_settings block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#advanced_settings GoogleDialogflowCxFlow#advanced_settings}
        '''
        result = self._values.get("advanced_settings")
        return typing.cast(typing.Optional[GoogleDialogflowCxFlowAdvancedSettings], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the flow. The maximum length is 500 characters. If exceeded, the request is rejected.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#description GoogleDialogflowCxFlow#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def event_handlers(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleDialogflowCxFlowEventHandlers"]]]:
        '''event_handlers block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#event_handlers GoogleDialogflowCxFlow#event_handlers}
        '''
        result = self._values.get("event_handlers")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleDialogflowCxFlowEventHandlers"]]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#id GoogleDialogflowCxFlow#id}.

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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#is_default_start_flow GoogleDialogflowCxFlow#is_default_start_flow}
        '''
        result = self._values.get("is_default_start_flow")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def knowledge_connector_settings(
        self,
    ) -> typing.Optional["GoogleDialogflowCxFlowKnowledgeConnectorSettings"]:
        '''knowledge_connector_settings block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#knowledge_connector_settings GoogleDialogflowCxFlow#knowledge_connector_settings}
        '''
        result = self._values.get("knowledge_connector_settings")
        return typing.cast(typing.Optional["GoogleDialogflowCxFlowKnowledgeConnectorSettings"], result)

    @builtins.property
    def language_code(self) -> typing.Optional[builtins.str]:
        '''The language of the following fields in flow: Flow.event_handlers.trigger_fulfillment.messages Flow.event_handlers.trigger_fulfillment.conditional_cases Flow.transition_routes.trigger_fulfillment.messages Flow.transition_routes.trigger_fulfillment.conditional_cases If not specified, the agent's default language is used. Many languages are supported. Note: languages must be enabled in the agent before they can be used.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#language_code GoogleDialogflowCxFlow#language_code}
        '''
        result = self._values.get("language_code")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def nlu_settings(self) -> typing.Optional["GoogleDialogflowCxFlowNluSettings"]:
        '''nlu_settings block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#nlu_settings GoogleDialogflowCxFlow#nlu_settings}
        '''
        result = self._values.get("nlu_settings")
        return typing.cast(typing.Optional["GoogleDialogflowCxFlowNluSettings"], result)

    @builtins.property
    def parent(self) -> typing.Optional[builtins.str]:
        '''The agent to create a flow for. Format: projects//locations//agents/.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#parent GoogleDialogflowCxFlow#parent}
        '''
        result = self._values.get("parent")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["GoogleDialogflowCxFlowTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#timeouts GoogleDialogflowCxFlow#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["GoogleDialogflowCxFlowTimeouts"], result)

    @builtins.property
    def transition_route_groups(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A flow's transition route group serve two purposes: They are responsible for matching the user's first utterances in the flow.

        They are inherited by every page's [transition route groups][Page.transition_route_groups]. Transition route groups defined in the page have higher priority than those defined in the flow.
        Format:projects//locations//agents//flows//transitionRouteGroups/.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#transition_route_groups GoogleDialogflowCxFlow#transition_route_groups}
        '''
        result = self._values.get("transition_route_groups")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def transition_routes(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleDialogflowCxFlowTransitionRoutes"]]]:
        '''transition_routes block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#transition_routes GoogleDialogflowCxFlow#transition_routes}
        '''
        result = self._values.get("transition_routes")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleDialogflowCxFlowTransitionRoutes"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDialogflowCxFlowConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDialogflowCxFlow.GoogleDialogflowCxFlowEventHandlers",
    jsii_struct_bases=[],
    name_mapping={
        "event": "event",
        "target_flow": "targetFlow",
        "target_page": "targetPage",
        "trigger_fulfillment": "triggerFulfillment",
    },
)
class GoogleDialogflowCxFlowEventHandlers:
    def __init__(
        self,
        *,
        event: typing.Optional[builtins.str] = None,
        target_flow: typing.Optional[builtins.str] = None,
        target_page: typing.Optional[builtins.str] = None,
        trigger_fulfillment: typing.Optional[typing.Union["GoogleDialogflowCxFlowEventHandlersTriggerFulfillment", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param event: The name of the event to handle. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#event GoogleDialogflowCxFlow#event}
        :param target_flow: The target flow to transition to. Format: projects//locations//agents//flows/. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#target_flow GoogleDialogflowCxFlow#target_flow}
        :param target_page: The target page to transition to. Format: projects//locations//agents//flows//pages/. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#target_page GoogleDialogflowCxFlow#target_page}
        :param trigger_fulfillment: trigger_fulfillment block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#trigger_fulfillment GoogleDialogflowCxFlow#trigger_fulfillment}
        '''
        if isinstance(trigger_fulfillment, dict):
            trigger_fulfillment = GoogleDialogflowCxFlowEventHandlersTriggerFulfillment(**trigger_fulfillment)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__98d6b437f59c96e369e9a65e8cba23f38e57df796929bbd75224bcedc388b721)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#event GoogleDialogflowCxFlow#event}
        '''
        result = self._values.get("event")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def target_flow(self) -> typing.Optional[builtins.str]:
        '''The target flow to transition to. Format: projects//locations//agents//flows/.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#target_flow GoogleDialogflowCxFlow#target_flow}
        '''
        result = self._values.get("target_flow")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def target_page(self) -> typing.Optional[builtins.str]:
        '''The target page to transition to. Format: projects//locations//agents//flows//pages/.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#target_page GoogleDialogflowCxFlow#target_page}
        '''
        result = self._values.get("target_page")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def trigger_fulfillment(
        self,
    ) -> typing.Optional["GoogleDialogflowCxFlowEventHandlersTriggerFulfillment"]:
        '''trigger_fulfillment block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#trigger_fulfillment GoogleDialogflowCxFlow#trigger_fulfillment}
        '''
        result = self._values.get("trigger_fulfillment")
        return typing.cast(typing.Optional["GoogleDialogflowCxFlowEventHandlersTriggerFulfillment"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDialogflowCxFlowEventHandlers(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDialogflowCxFlowEventHandlersList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDialogflowCxFlow.GoogleDialogflowCxFlowEventHandlersList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2ea6d2385130136ba9ba2449229da1e1d3e391e41dfafc4c8ca3bb1631d4ce14)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleDialogflowCxFlowEventHandlersOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b72692e2f83b58047d9ef491b2c6b8d6d65b1d0576f01c8e029ece54d7ca94a)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleDialogflowCxFlowEventHandlersOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__10e47925b00e47f983de73bfa202626a1e3135e199f22fe97d586dabb330c1f3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a87ff1ba2605882bab6a41459482a8d5ce15d04140c213017f7aa60d0f1f8cd4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__797650aaec31e7ca6bb8bc45d5cb90e35913ad807f256a34b97189d1d969d736)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDialogflowCxFlowEventHandlers]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDialogflowCxFlowEventHandlers]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDialogflowCxFlowEventHandlers]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__550686a1780bbee4f9f8564add05760636a98a28cf7e02f3c02b086103f5e3dc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleDialogflowCxFlowEventHandlersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDialogflowCxFlow.GoogleDialogflowCxFlowEventHandlersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c0b49a2bf192f63cb5a72c1bd7cdffb07f5cdb45767d0977c9c0af70fe72a68a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putTriggerFulfillment")
    def put_trigger_fulfillment(
        self,
        *,
        conditional_cases: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleDialogflowCxFlowEventHandlersTriggerFulfillmentConditionalCases", typing.Dict[builtins.str, typing.Any]]]]] = None,
        enable_generative_fallback: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        messages: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleDialogflowCxFlowEventHandlersTriggerFulfillmentMessages", typing.Dict[builtins.str, typing.Any]]]]] = None,
        return_partial_responses: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        set_parameter_actions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleDialogflowCxFlowEventHandlersTriggerFulfillmentSetParameterActions", typing.Dict[builtins.str, typing.Any]]]]] = None,
        tag: typing.Optional[builtins.str] = None,
        webhook: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param conditional_cases: conditional_cases block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#conditional_cases GoogleDialogflowCxFlow#conditional_cases}
        :param enable_generative_fallback: If the flag is true, the agent will utilize LLM to generate a text response. If LLM generation fails, the defined responses in the fulfillment will be respected. This flag is only useful for fulfillments associated with no-match event handlers. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#enable_generative_fallback GoogleDialogflowCxFlow#enable_generative_fallback}
        :param messages: messages block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#messages GoogleDialogflowCxFlow#messages}
        :param return_partial_responses: Whether Dialogflow should return currently queued fulfillment response messages in streaming APIs. If a webhook is specified, it happens before Dialogflow invokes webhook. Warning: 1) This flag only affects streaming API. Responses are still queued and returned once in non-streaming API. 2) The flag can be enabled in any fulfillment but only the first 3 partial responses will be returned. You may only want to apply it to fulfillments that have slow webhooks. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#return_partial_responses GoogleDialogflowCxFlow#return_partial_responses}
        :param set_parameter_actions: set_parameter_actions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#set_parameter_actions GoogleDialogflowCxFlow#set_parameter_actions}
        :param tag: The tag used by the webhook to identify which fulfillment is being called. This field is required if webhook is specified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#tag GoogleDialogflowCxFlow#tag}
        :param webhook: The webhook to call. Format: projects//locations//agents//webhooks/. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#webhook GoogleDialogflowCxFlow#webhook}
        '''
        value = GoogleDialogflowCxFlowEventHandlersTriggerFulfillment(
            conditional_cases=conditional_cases,
            enable_generative_fallback=enable_generative_fallback,
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
    ) -> "GoogleDialogflowCxFlowEventHandlersTriggerFulfillmentOutputReference":
        return typing.cast("GoogleDialogflowCxFlowEventHandlersTriggerFulfillmentOutputReference", jsii.get(self, "triggerFulfillment"))

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
    ) -> typing.Optional["GoogleDialogflowCxFlowEventHandlersTriggerFulfillment"]:
        return typing.cast(typing.Optional["GoogleDialogflowCxFlowEventHandlersTriggerFulfillment"], jsii.get(self, "triggerFulfillmentInput"))

    @builtins.property
    @jsii.member(jsii_name="event")
    def event(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "event"))

    @event.setter
    def event(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__65b6f23d473fdfa3616c5c573a6311ed0c64ca67237e5fc371844d19be8d4b06)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "event", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="targetFlow")
    def target_flow(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "targetFlow"))

    @target_flow.setter
    def target_flow(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e8232a76d7dd21a85014f51ee2b25961374daa0e33aba5d27aed553abf55ee0b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "targetFlow", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="targetPage")
    def target_page(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "targetPage"))

    @target_page.setter
    def target_page(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf6d60b11ea63adf1c7be2210f0b5cecc0c0346fad1ab06f7f78bd60d2f16a37)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "targetPage", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDialogflowCxFlowEventHandlers]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDialogflowCxFlowEventHandlers]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDialogflowCxFlowEventHandlers]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__22b10706871c1d1f665ef2d90bd0d58a208650af42514f7be1dca25fb9f02432)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDialogflowCxFlow.GoogleDialogflowCxFlowEventHandlersTriggerFulfillment",
    jsii_struct_bases=[],
    name_mapping={
        "conditional_cases": "conditionalCases",
        "enable_generative_fallback": "enableGenerativeFallback",
        "messages": "messages",
        "return_partial_responses": "returnPartialResponses",
        "set_parameter_actions": "setParameterActions",
        "tag": "tag",
        "webhook": "webhook",
    },
)
class GoogleDialogflowCxFlowEventHandlersTriggerFulfillment:
    def __init__(
        self,
        *,
        conditional_cases: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleDialogflowCxFlowEventHandlersTriggerFulfillmentConditionalCases", typing.Dict[builtins.str, typing.Any]]]]] = None,
        enable_generative_fallback: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        messages: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleDialogflowCxFlowEventHandlersTriggerFulfillmentMessages", typing.Dict[builtins.str, typing.Any]]]]] = None,
        return_partial_responses: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        set_parameter_actions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleDialogflowCxFlowEventHandlersTriggerFulfillmentSetParameterActions", typing.Dict[builtins.str, typing.Any]]]]] = None,
        tag: typing.Optional[builtins.str] = None,
        webhook: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param conditional_cases: conditional_cases block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#conditional_cases GoogleDialogflowCxFlow#conditional_cases}
        :param enable_generative_fallback: If the flag is true, the agent will utilize LLM to generate a text response. If LLM generation fails, the defined responses in the fulfillment will be respected. This flag is only useful for fulfillments associated with no-match event handlers. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#enable_generative_fallback GoogleDialogflowCxFlow#enable_generative_fallback}
        :param messages: messages block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#messages GoogleDialogflowCxFlow#messages}
        :param return_partial_responses: Whether Dialogflow should return currently queued fulfillment response messages in streaming APIs. If a webhook is specified, it happens before Dialogflow invokes webhook. Warning: 1) This flag only affects streaming API. Responses are still queued and returned once in non-streaming API. 2) The flag can be enabled in any fulfillment but only the first 3 partial responses will be returned. You may only want to apply it to fulfillments that have slow webhooks. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#return_partial_responses GoogleDialogflowCxFlow#return_partial_responses}
        :param set_parameter_actions: set_parameter_actions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#set_parameter_actions GoogleDialogflowCxFlow#set_parameter_actions}
        :param tag: The tag used by the webhook to identify which fulfillment is being called. This field is required if webhook is specified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#tag GoogleDialogflowCxFlow#tag}
        :param webhook: The webhook to call. Format: projects//locations//agents//webhooks/. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#webhook GoogleDialogflowCxFlow#webhook}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e2b0b5e0e8e08564eff12bc1e01fd9807cb7a628d58f0aa0ac775e881f69e3fe)
            check_type(argname="argument conditional_cases", value=conditional_cases, expected_type=type_hints["conditional_cases"])
            check_type(argname="argument enable_generative_fallback", value=enable_generative_fallback, expected_type=type_hints["enable_generative_fallback"])
            check_type(argname="argument messages", value=messages, expected_type=type_hints["messages"])
            check_type(argname="argument return_partial_responses", value=return_partial_responses, expected_type=type_hints["return_partial_responses"])
            check_type(argname="argument set_parameter_actions", value=set_parameter_actions, expected_type=type_hints["set_parameter_actions"])
            check_type(argname="argument tag", value=tag, expected_type=type_hints["tag"])
            check_type(argname="argument webhook", value=webhook, expected_type=type_hints["webhook"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if conditional_cases is not None:
            self._values["conditional_cases"] = conditional_cases
        if enable_generative_fallback is not None:
            self._values["enable_generative_fallback"] = enable_generative_fallback
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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleDialogflowCxFlowEventHandlersTriggerFulfillmentConditionalCases"]]]:
        '''conditional_cases block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#conditional_cases GoogleDialogflowCxFlow#conditional_cases}
        '''
        result = self._values.get("conditional_cases")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleDialogflowCxFlowEventHandlersTriggerFulfillmentConditionalCases"]]], result)

    @builtins.property
    def enable_generative_fallback(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If the flag is true, the agent will utilize LLM to generate a text response.

        If LLM generation fails, the defined responses in the fulfillment will be respected.
        This flag is only useful for fulfillments associated with no-match event handlers.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#enable_generative_fallback GoogleDialogflowCxFlow#enable_generative_fallback}
        '''
        result = self._values.get("enable_generative_fallback")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def messages(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleDialogflowCxFlowEventHandlersTriggerFulfillmentMessages"]]]:
        '''messages block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#messages GoogleDialogflowCxFlow#messages}
        '''
        result = self._values.get("messages")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleDialogflowCxFlowEventHandlersTriggerFulfillmentMessages"]]], result)

    @builtins.property
    def return_partial_responses(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether Dialogflow should return currently queued fulfillment response messages in streaming APIs.

        If a webhook is specified, it happens before Dialogflow invokes webhook. Warning: 1) This flag only affects streaming API. Responses are still queued and returned once in non-streaming API. 2) The flag can be enabled in any fulfillment but only the first 3 partial responses will be returned. You may only want to apply it to fulfillments that have slow webhooks.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#return_partial_responses GoogleDialogflowCxFlow#return_partial_responses}
        '''
        result = self._values.get("return_partial_responses")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def set_parameter_actions(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleDialogflowCxFlowEventHandlersTriggerFulfillmentSetParameterActions"]]]:
        '''set_parameter_actions block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#set_parameter_actions GoogleDialogflowCxFlow#set_parameter_actions}
        '''
        result = self._values.get("set_parameter_actions")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleDialogflowCxFlowEventHandlersTriggerFulfillmentSetParameterActions"]]], result)

    @builtins.property
    def tag(self) -> typing.Optional[builtins.str]:
        '''The tag used by the webhook to identify which fulfillment is being called.

        This field is required if webhook is specified.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#tag GoogleDialogflowCxFlow#tag}
        '''
        result = self._values.get("tag")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def webhook(self) -> typing.Optional[builtins.str]:
        '''The webhook to call. Format: projects//locations//agents//webhooks/.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#webhook GoogleDialogflowCxFlow#webhook}
        '''
        result = self._values.get("webhook")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDialogflowCxFlowEventHandlersTriggerFulfillment(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDialogflowCxFlow.GoogleDialogflowCxFlowEventHandlersTriggerFulfillmentConditionalCases",
    jsii_struct_bases=[],
    name_mapping={"cases": "cases"},
)
class GoogleDialogflowCxFlowEventHandlersTriggerFulfillmentConditionalCases:
    def __init__(self, *, cases: typing.Optional[builtins.str] = None) -> None:
        '''
        :param cases: A JSON encoded list of cascading if-else conditions. Cases are mutually exclusive. The first one with a matching condition is selected, all the rest ignored. See `Case <https://cloud.google.com/dialogflow/cx/docs/reference/rest/v3/Fulfillment#case>`_ for the schema. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#cases GoogleDialogflowCxFlow#cases}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8c91d12edab2a2dbd0bf7747bb2162e7c5824f681ff0be9abf60fd5a33549bd1)
            check_type(argname="argument cases", value=cases, expected_type=type_hints["cases"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if cases is not None:
            self._values["cases"] = cases

    @builtins.property
    def cases(self) -> typing.Optional[builtins.str]:
        '''A JSON encoded list of cascading if-else conditions.

        Cases are mutually exclusive. The first one with a matching condition is selected, all the rest ignored.
        See `Case <https://cloud.google.com/dialogflow/cx/docs/reference/rest/v3/Fulfillment#case>`_ for the schema.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#cases GoogleDialogflowCxFlow#cases}
        '''
        result = self._values.get("cases")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDialogflowCxFlowEventHandlersTriggerFulfillmentConditionalCases(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDialogflowCxFlowEventHandlersTriggerFulfillmentConditionalCasesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDialogflowCxFlow.GoogleDialogflowCxFlowEventHandlersTriggerFulfillmentConditionalCasesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8dc297fa3b4deca51bde040af9d3d85d51244a4f502dc3dc2edfd6b442cd6cf3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleDialogflowCxFlowEventHandlersTriggerFulfillmentConditionalCasesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c5085cb33cee60f0351f3707232a96f794e06e88c9214ab90efd906fee9c0034)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleDialogflowCxFlowEventHandlersTriggerFulfillmentConditionalCasesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ba859ff220cb9d944e616471ac511e557a5570ae65fcc73358ef0b6aee8b570)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e5d1ff8d188984b06b917cc566fa0b77d1abdc648bc70011da6ca2c1425ef353)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0c046a332b2e188696b71b7ebb514bc26bebd1e040aebcd934005665a2890fc2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDialogflowCxFlowEventHandlersTriggerFulfillmentConditionalCases]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDialogflowCxFlowEventHandlersTriggerFulfillmentConditionalCases]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDialogflowCxFlowEventHandlersTriggerFulfillmentConditionalCases]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aaf545456d221be7117ea8e6a65ac1c3cc6ce3dc384d83d3d6f8aec0539adb64)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleDialogflowCxFlowEventHandlersTriggerFulfillmentConditionalCasesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDialogflowCxFlow.GoogleDialogflowCxFlowEventHandlersTriggerFulfillmentConditionalCasesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4d18f9237ed20e32840fe9794f3f02ec81890ca29521cd3ea20bff5398ba6515)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f6059d8a6d6d9cc3d499120d5011eeb5726168e3b30d8845649011bb6ea07f40)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cases", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDialogflowCxFlowEventHandlersTriggerFulfillmentConditionalCases]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDialogflowCxFlowEventHandlersTriggerFulfillmentConditionalCases]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDialogflowCxFlowEventHandlersTriggerFulfillmentConditionalCases]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8c97cb0f6e6865d8ec850b8cbeedc765de0021d6a630119f6ace7b60ba3f5d0f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDialogflowCxFlow.GoogleDialogflowCxFlowEventHandlersTriggerFulfillmentMessages",
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
class GoogleDialogflowCxFlowEventHandlersTriggerFulfillmentMessages:
    def __init__(
        self,
        *,
        channel: typing.Optional[builtins.str] = None,
        conversation_success: typing.Optional[typing.Union["GoogleDialogflowCxFlowEventHandlersTriggerFulfillmentMessagesConversationSuccess", typing.Dict[builtins.str, typing.Any]]] = None,
        live_agent_handoff: typing.Optional[typing.Union["GoogleDialogflowCxFlowEventHandlersTriggerFulfillmentMessagesLiveAgentHandoff", typing.Dict[builtins.str, typing.Any]]] = None,
        output_audio_text: typing.Optional[typing.Union["GoogleDialogflowCxFlowEventHandlersTriggerFulfillmentMessagesOutputAudioText", typing.Dict[builtins.str, typing.Any]]] = None,
        payload: typing.Optional[builtins.str] = None,
        play_audio: typing.Optional[typing.Union["GoogleDialogflowCxFlowEventHandlersTriggerFulfillmentMessagesPlayAudio", typing.Dict[builtins.str, typing.Any]]] = None,
        telephony_transfer_call: typing.Optional[typing.Union["GoogleDialogflowCxFlowEventHandlersTriggerFulfillmentMessagesTelephonyTransferCall", typing.Dict[builtins.str, typing.Any]]] = None,
        text: typing.Optional[typing.Union["GoogleDialogflowCxFlowEventHandlersTriggerFulfillmentMessagesText", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param channel: The channel which the response is associated with. Clients can specify the channel via QueryParameters.channel, and only associated channel response will be returned. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#channel GoogleDialogflowCxFlow#channel}
        :param conversation_success: conversation_success block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#conversation_success GoogleDialogflowCxFlow#conversation_success}
        :param live_agent_handoff: live_agent_handoff block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#live_agent_handoff GoogleDialogflowCxFlow#live_agent_handoff}
        :param output_audio_text: output_audio_text block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#output_audio_text GoogleDialogflowCxFlow#output_audio_text}
        :param payload: A custom, platform-specific payload. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#payload GoogleDialogflowCxFlow#payload}
        :param play_audio: play_audio block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#play_audio GoogleDialogflowCxFlow#play_audio}
        :param telephony_transfer_call: telephony_transfer_call block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#telephony_transfer_call GoogleDialogflowCxFlow#telephony_transfer_call}
        :param text: text block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#text GoogleDialogflowCxFlow#text}
        '''
        if isinstance(conversation_success, dict):
            conversation_success = GoogleDialogflowCxFlowEventHandlersTriggerFulfillmentMessagesConversationSuccess(**conversation_success)
        if isinstance(live_agent_handoff, dict):
            live_agent_handoff = GoogleDialogflowCxFlowEventHandlersTriggerFulfillmentMessagesLiveAgentHandoff(**live_agent_handoff)
        if isinstance(output_audio_text, dict):
            output_audio_text = GoogleDialogflowCxFlowEventHandlersTriggerFulfillmentMessagesOutputAudioText(**output_audio_text)
        if isinstance(play_audio, dict):
            play_audio = GoogleDialogflowCxFlowEventHandlersTriggerFulfillmentMessagesPlayAudio(**play_audio)
        if isinstance(telephony_transfer_call, dict):
            telephony_transfer_call = GoogleDialogflowCxFlowEventHandlersTriggerFulfillmentMessagesTelephonyTransferCall(**telephony_transfer_call)
        if isinstance(text, dict):
            text = GoogleDialogflowCxFlowEventHandlersTriggerFulfillmentMessagesText(**text)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__47cf1b77ff3ec061bdddb90036c33368f3e5b8f584b5d70cb6c8d6c442148a4f)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#channel GoogleDialogflowCxFlow#channel}
        '''
        result = self._values.get("channel")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def conversation_success(
        self,
    ) -> typing.Optional["GoogleDialogflowCxFlowEventHandlersTriggerFulfillmentMessagesConversationSuccess"]:
        '''conversation_success block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#conversation_success GoogleDialogflowCxFlow#conversation_success}
        '''
        result = self._values.get("conversation_success")
        return typing.cast(typing.Optional["GoogleDialogflowCxFlowEventHandlersTriggerFulfillmentMessagesConversationSuccess"], result)

    @builtins.property
    def live_agent_handoff(
        self,
    ) -> typing.Optional["GoogleDialogflowCxFlowEventHandlersTriggerFulfillmentMessagesLiveAgentHandoff"]:
        '''live_agent_handoff block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#live_agent_handoff GoogleDialogflowCxFlow#live_agent_handoff}
        '''
        result = self._values.get("live_agent_handoff")
        return typing.cast(typing.Optional["GoogleDialogflowCxFlowEventHandlersTriggerFulfillmentMessagesLiveAgentHandoff"], result)

    @builtins.property
    def output_audio_text(
        self,
    ) -> typing.Optional["GoogleDialogflowCxFlowEventHandlersTriggerFulfillmentMessagesOutputAudioText"]:
        '''output_audio_text block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#output_audio_text GoogleDialogflowCxFlow#output_audio_text}
        '''
        result = self._values.get("output_audio_text")
        return typing.cast(typing.Optional["GoogleDialogflowCxFlowEventHandlersTriggerFulfillmentMessagesOutputAudioText"], result)

    @builtins.property
    def payload(self) -> typing.Optional[builtins.str]:
        '''A custom, platform-specific payload.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#payload GoogleDialogflowCxFlow#payload}
        '''
        result = self._values.get("payload")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def play_audio(
        self,
    ) -> typing.Optional["GoogleDialogflowCxFlowEventHandlersTriggerFulfillmentMessagesPlayAudio"]:
        '''play_audio block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#play_audio GoogleDialogflowCxFlow#play_audio}
        '''
        result = self._values.get("play_audio")
        return typing.cast(typing.Optional["GoogleDialogflowCxFlowEventHandlersTriggerFulfillmentMessagesPlayAudio"], result)

    @builtins.property
    def telephony_transfer_call(
        self,
    ) -> typing.Optional["GoogleDialogflowCxFlowEventHandlersTriggerFulfillmentMessagesTelephonyTransferCall"]:
        '''telephony_transfer_call block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#telephony_transfer_call GoogleDialogflowCxFlow#telephony_transfer_call}
        '''
        result = self._values.get("telephony_transfer_call")
        return typing.cast(typing.Optional["GoogleDialogflowCxFlowEventHandlersTriggerFulfillmentMessagesTelephonyTransferCall"], result)

    @builtins.property
    def text(
        self,
    ) -> typing.Optional["GoogleDialogflowCxFlowEventHandlersTriggerFulfillmentMessagesText"]:
        '''text block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#text GoogleDialogflowCxFlow#text}
        '''
        result = self._values.get("text")
        return typing.cast(typing.Optional["GoogleDialogflowCxFlowEventHandlersTriggerFulfillmentMessagesText"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDialogflowCxFlowEventHandlersTriggerFulfillmentMessages(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDialogflowCxFlow.GoogleDialogflowCxFlowEventHandlersTriggerFulfillmentMessagesConversationSuccess",
    jsii_struct_bases=[],
    name_mapping={"metadata": "metadata"},
)
class GoogleDialogflowCxFlowEventHandlersTriggerFulfillmentMessagesConversationSuccess:
    def __init__(self, *, metadata: typing.Optional[builtins.str] = None) -> None:
        '''
        :param metadata: Custom metadata. Dialogflow doesn't impose any structure on this. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#metadata GoogleDialogflowCxFlow#metadata}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__71ba2f39b3e982d1ed7e0151541fccd54bbba72eb06788d47077001ea900f65b)
            check_type(argname="argument metadata", value=metadata, expected_type=type_hints["metadata"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if metadata is not None:
            self._values["metadata"] = metadata

    @builtins.property
    def metadata(self) -> typing.Optional[builtins.str]:
        '''Custom metadata. Dialogflow doesn't impose any structure on this.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#metadata GoogleDialogflowCxFlow#metadata}
        '''
        result = self._values.get("metadata")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDialogflowCxFlowEventHandlersTriggerFulfillmentMessagesConversationSuccess(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDialogflowCxFlowEventHandlersTriggerFulfillmentMessagesConversationSuccessOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDialogflowCxFlow.GoogleDialogflowCxFlowEventHandlersTriggerFulfillmentMessagesConversationSuccessOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__999db007c9c1915b58c71b617ffb2b51d98449f40e550093ac8de4804f4b8bab)
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
            type_hints = typing.get_type_hints(_typecheckingstub__80c92f6879994241f8be0374257b2000fb20537e65d4e70e623aacebb56b8da9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metadata", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDialogflowCxFlowEventHandlersTriggerFulfillmentMessagesConversationSuccess]:
        return typing.cast(typing.Optional[GoogleDialogflowCxFlowEventHandlersTriggerFulfillmentMessagesConversationSuccess], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDialogflowCxFlowEventHandlersTriggerFulfillmentMessagesConversationSuccess],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ad2092c5876164f320659d6b4e0c9ee2959f15bfc8ab9c6240bed7c672aca6db)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleDialogflowCxFlowEventHandlersTriggerFulfillmentMessagesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDialogflowCxFlow.GoogleDialogflowCxFlowEventHandlersTriggerFulfillmentMessagesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__91a30f242e5ea4183f4a388675dae2a39a85ebb559121c69b38971a70ae0259b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleDialogflowCxFlowEventHandlersTriggerFulfillmentMessagesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ef209c5de032bddd5d5f68a59e2625324e8d419c75f45bb6c212f1afcdcf5337)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleDialogflowCxFlowEventHandlersTriggerFulfillmentMessagesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3fb9eaee16e8332e5d899c05745620e138957c5e96c41b0be100922470cea560)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8df20db12f6bf4a2136b74d845969b82f6c72d29f3160edf5aaf3e9607405c84)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fc59802a7434cb11ca69be912e59b031a4a61b4c64c7c3877cf2b86eedfb6dc5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDialogflowCxFlowEventHandlersTriggerFulfillmentMessages]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDialogflowCxFlowEventHandlersTriggerFulfillmentMessages]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDialogflowCxFlowEventHandlersTriggerFulfillmentMessages]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__66fc6f716cf1db773623fff9494d38d2fd97eaa1964cbad881bf5cb7c48ed834)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDialogflowCxFlow.GoogleDialogflowCxFlowEventHandlersTriggerFulfillmentMessagesLiveAgentHandoff",
    jsii_struct_bases=[],
    name_mapping={"metadata": "metadata"},
)
class GoogleDialogflowCxFlowEventHandlersTriggerFulfillmentMessagesLiveAgentHandoff:
    def __init__(self, *, metadata: typing.Optional[builtins.str] = None) -> None:
        '''
        :param metadata: Custom metadata. Dialogflow doesn't impose any structure on this. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#metadata GoogleDialogflowCxFlow#metadata}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__de157fcd6751d9db70e1e58531c48002ac6b8c5e271e1629c9cfe53f64074595)
            check_type(argname="argument metadata", value=metadata, expected_type=type_hints["metadata"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if metadata is not None:
            self._values["metadata"] = metadata

    @builtins.property
    def metadata(self) -> typing.Optional[builtins.str]:
        '''Custom metadata. Dialogflow doesn't impose any structure on this.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#metadata GoogleDialogflowCxFlow#metadata}
        '''
        result = self._values.get("metadata")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDialogflowCxFlowEventHandlersTriggerFulfillmentMessagesLiveAgentHandoff(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDialogflowCxFlowEventHandlersTriggerFulfillmentMessagesLiveAgentHandoffOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDialogflowCxFlow.GoogleDialogflowCxFlowEventHandlersTriggerFulfillmentMessagesLiveAgentHandoffOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c2d9347e9d2f662db1ce7f21c8a413ffd0a12b9032e84ad52c72b13bb5a38b4c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6de09dd2cb920aec8c6fa2d52287a5fe3f6517d58922ee571408de959977b10e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metadata", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDialogflowCxFlowEventHandlersTriggerFulfillmentMessagesLiveAgentHandoff]:
        return typing.cast(typing.Optional[GoogleDialogflowCxFlowEventHandlersTriggerFulfillmentMessagesLiveAgentHandoff], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDialogflowCxFlowEventHandlersTriggerFulfillmentMessagesLiveAgentHandoff],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__17248d3513fcfd5a6bdcb22aa7baa4cc0a70cd192852dbe9123ed496586b7418)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDialogflowCxFlow.GoogleDialogflowCxFlowEventHandlersTriggerFulfillmentMessagesOutputAudioText",
    jsii_struct_bases=[],
    name_mapping={"ssml": "ssml", "text": "text"},
)
class GoogleDialogflowCxFlowEventHandlersTriggerFulfillmentMessagesOutputAudioText:
    def __init__(
        self,
        *,
        ssml: typing.Optional[builtins.str] = None,
        text: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param ssml: The SSML text to be synthesized. For more information, see SSML. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#ssml GoogleDialogflowCxFlow#ssml}
        :param text: The raw text to be synthesized. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#text GoogleDialogflowCxFlow#text}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2cd4b98e2ab2e75f2d752a959a0b0e1ef2932096b760b53b77c60a04151f4085)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#ssml GoogleDialogflowCxFlow#ssml}
        '''
        result = self._values.get("ssml")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def text(self) -> typing.Optional[builtins.str]:
        '''The raw text to be synthesized.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#text GoogleDialogflowCxFlow#text}
        '''
        result = self._values.get("text")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDialogflowCxFlowEventHandlersTriggerFulfillmentMessagesOutputAudioText(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDialogflowCxFlowEventHandlersTriggerFulfillmentMessagesOutputAudioTextOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDialogflowCxFlow.GoogleDialogflowCxFlowEventHandlersTriggerFulfillmentMessagesOutputAudioTextOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__54f4bdf6f12fb261e41faa5a2b0f3246d66e76f40c88d4a533e2192eb312f928)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1d4b85156c1116cd26e4873b89c1a4966f7a568ab35aebf2d9be598cd25c2003)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ssml", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="text")
    def text(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "text"))

    @text.setter
    def text(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aed58b632dd33e478da2b95a0c954d89c8684469ad93a8c05bf1fefb92334ef6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "text", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDialogflowCxFlowEventHandlersTriggerFulfillmentMessagesOutputAudioText]:
        return typing.cast(typing.Optional[GoogleDialogflowCxFlowEventHandlersTriggerFulfillmentMessagesOutputAudioText], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDialogflowCxFlowEventHandlersTriggerFulfillmentMessagesOutputAudioText],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__407c042b8ffe7beb5fd352f1cc631efea66dd2870ba4c36b89578b5c469a4725)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleDialogflowCxFlowEventHandlersTriggerFulfillmentMessagesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDialogflowCxFlow.GoogleDialogflowCxFlowEventHandlersTriggerFulfillmentMessagesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0a5d7394da129220d20cf2d3e9de1e4a8bc97cf36ff80f93157bd345d447f814)
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
        :param metadata: Custom metadata. Dialogflow doesn't impose any structure on this. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#metadata GoogleDialogflowCxFlow#metadata}
        '''
        value = GoogleDialogflowCxFlowEventHandlersTriggerFulfillmentMessagesConversationSuccess(
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
        :param metadata: Custom metadata. Dialogflow doesn't impose any structure on this. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#metadata GoogleDialogflowCxFlow#metadata}
        '''
        value = GoogleDialogflowCxFlowEventHandlersTriggerFulfillmentMessagesLiveAgentHandoff(
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
        :param ssml: The SSML text to be synthesized. For more information, see SSML. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#ssml GoogleDialogflowCxFlow#ssml}
        :param text: The raw text to be synthesized. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#text GoogleDialogflowCxFlow#text}
        '''
        value = GoogleDialogflowCxFlowEventHandlersTriggerFulfillmentMessagesOutputAudioText(
            ssml=ssml, text=text
        )

        return typing.cast(None, jsii.invoke(self, "putOutputAudioText", [value]))

    @jsii.member(jsii_name="putPlayAudio")
    def put_play_audio(self, *, audio_uri: builtins.str) -> None:
        '''
        :param audio_uri: URI of the audio clip. Dialogflow does not impose any validation on this value. It is specific to the client that reads it. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#audio_uri GoogleDialogflowCxFlow#audio_uri}
        '''
        value = GoogleDialogflowCxFlowEventHandlersTriggerFulfillmentMessagesPlayAudio(
            audio_uri=audio_uri
        )

        return typing.cast(None, jsii.invoke(self, "putPlayAudio", [value]))

    @jsii.member(jsii_name="putTelephonyTransferCall")
    def put_telephony_transfer_call(self, *, phone_number: builtins.str) -> None:
        '''
        :param phone_number: Transfer the call to a phone number in E.164 format. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#phone_number GoogleDialogflowCxFlow#phone_number}
        '''
        value = GoogleDialogflowCxFlowEventHandlersTriggerFulfillmentMessagesTelephonyTransferCall(
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
        :param text: A collection of text responses. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#text GoogleDialogflowCxFlow#text}
        '''
        value = GoogleDialogflowCxFlowEventHandlersTriggerFulfillmentMessagesText(
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
    ) -> GoogleDialogflowCxFlowEventHandlersTriggerFulfillmentMessagesConversationSuccessOutputReference:
        return typing.cast(GoogleDialogflowCxFlowEventHandlersTriggerFulfillmentMessagesConversationSuccessOutputReference, jsii.get(self, "conversationSuccess"))

    @builtins.property
    @jsii.member(jsii_name="liveAgentHandoff")
    def live_agent_handoff(
        self,
    ) -> GoogleDialogflowCxFlowEventHandlersTriggerFulfillmentMessagesLiveAgentHandoffOutputReference:
        return typing.cast(GoogleDialogflowCxFlowEventHandlersTriggerFulfillmentMessagesLiveAgentHandoffOutputReference, jsii.get(self, "liveAgentHandoff"))

    @builtins.property
    @jsii.member(jsii_name="outputAudioText")
    def output_audio_text(
        self,
    ) -> GoogleDialogflowCxFlowEventHandlersTriggerFulfillmentMessagesOutputAudioTextOutputReference:
        return typing.cast(GoogleDialogflowCxFlowEventHandlersTriggerFulfillmentMessagesOutputAudioTextOutputReference, jsii.get(self, "outputAudioText"))

    @builtins.property
    @jsii.member(jsii_name="playAudio")
    def play_audio(
        self,
    ) -> "GoogleDialogflowCxFlowEventHandlersTriggerFulfillmentMessagesPlayAudioOutputReference":
        return typing.cast("GoogleDialogflowCxFlowEventHandlersTriggerFulfillmentMessagesPlayAudioOutputReference", jsii.get(self, "playAudio"))

    @builtins.property
    @jsii.member(jsii_name="telephonyTransferCall")
    def telephony_transfer_call(
        self,
    ) -> "GoogleDialogflowCxFlowEventHandlersTriggerFulfillmentMessagesTelephonyTransferCallOutputReference":
        return typing.cast("GoogleDialogflowCxFlowEventHandlersTriggerFulfillmentMessagesTelephonyTransferCallOutputReference", jsii.get(self, "telephonyTransferCall"))

    @builtins.property
    @jsii.member(jsii_name="text")
    def text(
        self,
    ) -> "GoogleDialogflowCxFlowEventHandlersTriggerFulfillmentMessagesTextOutputReference":
        return typing.cast("GoogleDialogflowCxFlowEventHandlersTriggerFulfillmentMessagesTextOutputReference", jsii.get(self, "text"))

    @builtins.property
    @jsii.member(jsii_name="channelInput")
    def channel_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "channelInput"))

    @builtins.property
    @jsii.member(jsii_name="conversationSuccessInput")
    def conversation_success_input(
        self,
    ) -> typing.Optional[GoogleDialogflowCxFlowEventHandlersTriggerFulfillmentMessagesConversationSuccess]:
        return typing.cast(typing.Optional[GoogleDialogflowCxFlowEventHandlersTriggerFulfillmentMessagesConversationSuccess], jsii.get(self, "conversationSuccessInput"))

    @builtins.property
    @jsii.member(jsii_name="liveAgentHandoffInput")
    def live_agent_handoff_input(
        self,
    ) -> typing.Optional[GoogleDialogflowCxFlowEventHandlersTriggerFulfillmentMessagesLiveAgentHandoff]:
        return typing.cast(typing.Optional[GoogleDialogflowCxFlowEventHandlersTriggerFulfillmentMessagesLiveAgentHandoff], jsii.get(self, "liveAgentHandoffInput"))

    @builtins.property
    @jsii.member(jsii_name="outputAudioTextInput")
    def output_audio_text_input(
        self,
    ) -> typing.Optional[GoogleDialogflowCxFlowEventHandlersTriggerFulfillmentMessagesOutputAudioText]:
        return typing.cast(typing.Optional[GoogleDialogflowCxFlowEventHandlersTriggerFulfillmentMessagesOutputAudioText], jsii.get(self, "outputAudioTextInput"))

    @builtins.property
    @jsii.member(jsii_name="payloadInput")
    def payload_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "payloadInput"))

    @builtins.property
    @jsii.member(jsii_name="playAudioInput")
    def play_audio_input(
        self,
    ) -> typing.Optional["GoogleDialogflowCxFlowEventHandlersTriggerFulfillmentMessagesPlayAudio"]:
        return typing.cast(typing.Optional["GoogleDialogflowCxFlowEventHandlersTriggerFulfillmentMessagesPlayAudio"], jsii.get(self, "playAudioInput"))

    @builtins.property
    @jsii.member(jsii_name="telephonyTransferCallInput")
    def telephony_transfer_call_input(
        self,
    ) -> typing.Optional["GoogleDialogflowCxFlowEventHandlersTriggerFulfillmentMessagesTelephonyTransferCall"]:
        return typing.cast(typing.Optional["GoogleDialogflowCxFlowEventHandlersTriggerFulfillmentMessagesTelephonyTransferCall"], jsii.get(self, "telephonyTransferCallInput"))

    @builtins.property
    @jsii.member(jsii_name="textInput")
    def text_input(
        self,
    ) -> typing.Optional["GoogleDialogflowCxFlowEventHandlersTriggerFulfillmentMessagesText"]:
        return typing.cast(typing.Optional["GoogleDialogflowCxFlowEventHandlersTriggerFulfillmentMessagesText"], jsii.get(self, "textInput"))

    @builtins.property
    @jsii.member(jsii_name="channel")
    def channel(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "channel"))

    @channel.setter
    def channel(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ee365bd5e7ad02443edec08b36d422ebd6ba0925fb54f56b43c0d0b5b6e08f5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "channel", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="payload")
    def payload(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "payload"))

    @payload.setter
    def payload(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e2cd3500edffc79de60595b43ccb8b511bac26f94034afd27658ce0f1dbb34d3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "payload", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDialogflowCxFlowEventHandlersTriggerFulfillmentMessages]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDialogflowCxFlowEventHandlersTriggerFulfillmentMessages]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDialogflowCxFlowEventHandlersTriggerFulfillmentMessages]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b33fd52d5aee1abc2af7510c2d810adabcf29a9323ff8a75fac9e0e5a9b3d8e2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDialogflowCxFlow.GoogleDialogflowCxFlowEventHandlersTriggerFulfillmentMessagesPlayAudio",
    jsii_struct_bases=[],
    name_mapping={"audio_uri": "audioUri"},
)
class GoogleDialogflowCxFlowEventHandlersTriggerFulfillmentMessagesPlayAudio:
    def __init__(self, *, audio_uri: builtins.str) -> None:
        '''
        :param audio_uri: URI of the audio clip. Dialogflow does not impose any validation on this value. It is specific to the client that reads it. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#audio_uri GoogleDialogflowCxFlow#audio_uri}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__efa71b0a2ce84c87ecd1d7c824a1b3d735c9cf5482efb3d60fc9b5a4a0486262)
            check_type(argname="argument audio_uri", value=audio_uri, expected_type=type_hints["audio_uri"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "audio_uri": audio_uri,
        }

    @builtins.property
    def audio_uri(self) -> builtins.str:
        '''URI of the audio clip.

        Dialogflow does not impose any validation on this value. It is specific to the client that reads it.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#audio_uri GoogleDialogflowCxFlow#audio_uri}
        '''
        result = self._values.get("audio_uri")
        assert result is not None, "Required property 'audio_uri' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDialogflowCxFlowEventHandlersTriggerFulfillmentMessagesPlayAudio(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDialogflowCxFlowEventHandlersTriggerFulfillmentMessagesPlayAudioOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDialogflowCxFlow.GoogleDialogflowCxFlowEventHandlersTriggerFulfillmentMessagesPlayAudioOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ecc3fe6bb8b710da9ac63e4d0055e56679e0eebb090c310213eff1a90119e934)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9e7dc243844b4f75b91211ae2d27b9887c7baa9733bc9bdbed88745218e44d94)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "audioUri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDialogflowCxFlowEventHandlersTriggerFulfillmentMessagesPlayAudio]:
        return typing.cast(typing.Optional[GoogleDialogflowCxFlowEventHandlersTriggerFulfillmentMessagesPlayAudio], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDialogflowCxFlowEventHandlersTriggerFulfillmentMessagesPlayAudio],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__11fdc1ebecce9edee0dd805324d6cf8aee3e2b30bd7204e4a9f3d3dbbe9424e4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDialogflowCxFlow.GoogleDialogflowCxFlowEventHandlersTriggerFulfillmentMessagesTelephonyTransferCall",
    jsii_struct_bases=[],
    name_mapping={"phone_number": "phoneNumber"},
)
class GoogleDialogflowCxFlowEventHandlersTriggerFulfillmentMessagesTelephonyTransferCall:
    def __init__(self, *, phone_number: builtins.str) -> None:
        '''
        :param phone_number: Transfer the call to a phone number in E.164 format. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#phone_number GoogleDialogflowCxFlow#phone_number}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e89b70a63040a97046353aa145e0c5def89f523a28e0e3192d56cb96c46a58d1)
            check_type(argname="argument phone_number", value=phone_number, expected_type=type_hints["phone_number"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "phone_number": phone_number,
        }

    @builtins.property
    def phone_number(self) -> builtins.str:
        '''Transfer the call to a phone number in E.164 format.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#phone_number GoogleDialogflowCxFlow#phone_number}
        '''
        result = self._values.get("phone_number")
        assert result is not None, "Required property 'phone_number' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDialogflowCxFlowEventHandlersTriggerFulfillmentMessagesTelephonyTransferCall(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDialogflowCxFlowEventHandlersTriggerFulfillmentMessagesTelephonyTransferCallOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDialogflowCxFlow.GoogleDialogflowCxFlowEventHandlersTriggerFulfillmentMessagesTelephonyTransferCallOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8d1e51f50aa052e9299e27e0ff1c13913459e9ec3fb03cdd73bb574e8248a106)
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
            type_hints = typing.get_type_hints(_typecheckingstub__54701318c05c962d1797c39a43227a0a786172c08ece78e448a8f61fcc24f506)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "phoneNumber", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDialogflowCxFlowEventHandlersTriggerFulfillmentMessagesTelephonyTransferCall]:
        return typing.cast(typing.Optional[GoogleDialogflowCxFlowEventHandlersTriggerFulfillmentMessagesTelephonyTransferCall], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDialogflowCxFlowEventHandlersTriggerFulfillmentMessagesTelephonyTransferCall],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bc6365e33a446197ecc983cc3b6027917a4bd3902601a9e02ecc1c5923b39d43)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDialogflowCxFlow.GoogleDialogflowCxFlowEventHandlersTriggerFulfillmentMessagesText",
    jsii_struct_bases=[],
    name_mapping={"text": "text"},
)
class GoogleDialogflowCxFlowEventHandlersTriggerFulfillmentMessagesText:
    def __init__(
        self,
        *,
        text: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param text: A collection of text responses. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#text GoogleDialogflowCxFlow#text}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__caf968656644d2b99fc0f819ca3a16b23f096995475b7b3a6e08e5c1c1358318)
            check_type(argname="argument text", value=text, expected_type=type_hints["text"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if text is not None:
            self._values["text"] = text

    @builtins.property
    def text(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A collection of text responses.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#text GoogleDialogflowCxFlow#text}
        '''
        result = self._values.get("text")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDialogflowCxFlowEventHandlersTriggerFulfillmentMessagesText(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDialogflowCxFlowEventHandlersTriggerFulfillmentMessagesTextOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDialogflowCxFlow.GoogleDialogflowCxFlowEventHandlersTriggerFulfillmentMessagesTextOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c4ec1e46f38dd2a469bcfc5e0b204a6b11595e08e119b7981575105910d8c78d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__037aec295bb472f589ea596cbfebb45456ce81962af528f351d6b6e616e3b242)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "text", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDialogflowCxFlowEventHandlersTriggerFulfillmentMessagesText]:
        return typing.cast(typing.Optional[GoogleDialogflowCxFlowEventHandlersTriggerFulfillmentMessagesText], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDialogflowCxFlowEventHandlersTriggerFulfillmentMessagesText],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__479b59249a9dfb3608d4dc0fed24b0337e07fe844e83827b6f943b301566db71)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleDialogflowCxFlowEventHandlersTriggerFulfillmentOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDialogflowCxFlow.GoogleDialogflowCxFlowEventHandlersTriggerFulfillmentOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3bad15ed6b01e2d0546b46b152ea04c1371cb3c7d4324e188ef4e47b66fade90)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putConditionalCases")
    def put_conditional_cases(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleDialogflowCxFlowEventHandlersTriggerFulfillmentConditionalCases, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__819a5d95220721c41d98998c537993544cc544bb52e5607faed5c09e1193c8a8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putConditionalCases", [value]))

    @jsii.member(jsii_name="putMessages")
    def put_messages(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleDialogflowCxFlowEventHandlersTriggerFulfillmentMessages, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__42f5acfd4c64d5ac63b8f15f48c10d2fd9d8bc9b56ae86ee6bab6d18e6328278)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putMessages", [value]))

    @jsii.member(jsii_name="putSetParameterActions")
    def put_set_parameter_actions(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleDialogflowCxFlowEventHandlersTriggerFulfillmentSetParameterActions", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__760234eadd3578b5586974b36f2ac0369361d386d0d7c7e1288fef584b33164c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putSetParameterActions", [value]))

    @jsii.member(jsii_name="resetConditionalCases")
    def reset_conditional_cases(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConditionalCases", []))

    @jsii.member(jsii_name="resetEnableGenerativeFallback")
    def reset_enable_generative_fallback(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnableGenerativeFallback", []))

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
    ) -> GoogleDialogflowCxFlowEventHandlersTriggerFulfillmentConditionalCasesList:
        return typing.cast(GoogleDialogflowCxFlowEventHandlersTriggerFulfillmentConditionalCasesList, jsii.get(self, "conditionalCases"))

    @builtins.property
    @jsii.member(jsii_name="messages")
    def messages(
        self,
    ) -> GoogleDialogflowCxFlowEventHandlersTriggerFulfillmentMessagesList:
        return typing.cast(GoogleDialogflowCxFlowEventHandlersTriggerFulfillmentMessagesList, jsii.get(self, "messages"))

    @builtins.property
    @jsii.member(jsii_name="setParameterActions")
    def set_parameter_actions(
        self,
    ) -> "GoogleDialogflowCxFlowEventHandlersTriggerFulfillmentSetParameterActionsList":
        return typing.cast("GoogleDialogflowCxFlowEventHandlersTriggerFulfillmentSetParameterActionsList", jsii.get(self, "setParameterActions"))

    @builtins.property
    @jsii.member(jsii_name="conditionalCasesInput")
    def conditional_cases_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDialogflowCxFlowEventHandlersTriggerFulfillmentConditionalCases]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDialogflowCxFlowEventHandlersTriggerFulfillmentConditionalCases]]], jsii.get(self, "conditionalCasesInput"))

    @builtins.property
    @jsii.member(jsii_name="enableGenerativeFallbackInput")
    def enable_generative_fallback_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enableGenerativeFallbackInput"))

    @builtins.property
    @jsii.member(jsii_name="messagesInput")
    def messages_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDialogflowCxFlowEventHandlersTriggerFulfillmentMessages]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDialogflowCxFlowEventHandlersTriggerFulfillmentMessages]]], jsii.get(self, "messagesInput"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleDialogflowCxFlowEventHandlersTriggerFulfillmentSetParameterActions"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleDialogflowCxFlowEventHandlersTriggerFulfillmentSetParameterActions"]]], jsii.get(self, "setParameterActionsInput"))

    @builtins.property
    @jsii.member(jsii_name="tagInput")
    def tag_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tagInput"))

    @builtins.property
    @jsii.member(jsii_name="webhookInput")
    def webhook_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "webhookInput"))

    @builtins.property
    @jsii.member(jsii_name="enableGenerativeFallback")
    def enable_generative_fallback(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enableGenerativeFallback"))

    @enable_generative_fallback.setter
    def enable_generative_fallback(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__547e1494f898245896601649f3fdef7524af98269263987cc20749f812479ebb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableGenerativeFallback", value) # pyright: ignore[reportArgumentType]

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
            type_hints = typing.get_type_hints(_typecheckingstub__b357e6f9c60440207ddaad42c083f61899fd2ca2bcace2737949eb6ea6851467)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "returnPartialResponses", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tag")
    def tag(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tag"))

    @tag.setter
    def tag(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__05e50fe901dbf61aa635a56e265013a777da162a618815e4ec01998dc21f697c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tag", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="webhook")
    def webhook(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "webhook"))

    @webhook.setter
    def webhook(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__91bf4cce913b48aa52137ae8d78dc55d18dccf652b6d505fed4dc622a5a91a55)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "webhook", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDialogflowCxFlowEventHandlersTriggerFulfillment]:
        return typing.cast(typing.Optional[GoogleDialogflowCxFlowEventHandlersTriggerFulfillment], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDialogflowCxFlowEventHandlersTriggerFulfillment],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d3744515a4e7ffc4c34a960ba8fd725e26afa66704674a5e14177efa17342c58)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDialogflowCxFlow.GoogleDialogflowCxFlowEventHandlersTriggerFulfillmentSetParameterActions",
    jsii_struct_bases=[],
    name_mapping={"parameter": "parameter", "value": "value"},
)
class GoogleDialogflowCxFlowEventHandlersTriggerFulfillmentSetParameterActions:
    def __init__(
        self,
        *,
        parameter: typing.Optional[builtins.str] = None,
        value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param parameter: Display name of the parameter. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#parameter GoogleDialogflowCxFlow#parameter}
        :param value: The new JSON-encoded value of the parameter. A null value clears the parameter. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#value GoogleDialogflowCxFlow#value}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__93c78aaa9dc78e546841f3429b21f134fd3cdfc47dbb4d8f2861327ff41bba56)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#parameter GoogleDialogflowCxFlow#parameter}
        '''
        result = self._values.get("parameter")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def value(self) -> typing.Optional[builtins.str]:
        '''The new JSON-encoded value of the parameter. A null value clears the parameter.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#value GoogleDialogflowCxFlow#value}
        '''
        result = self._values.get("value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDialogflowCxFlowEventHandlersTriggerFulfillmentSetParameterActions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDialogflowCxFlowEventHandlersTriggerFulfillmentSetParameterActionsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDialogflowCxFlow.GoogleDialogflowCxFlowEventHandlersTriggerFulfillmentSetParameterActionsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9baca73387f09f5353e93c5f8700bc045106f221b0359c2d131fbe7055705769)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleDialogflowCxFlowEventHandlersTriggerFulfillmentSetParameterActionsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5c9ad8bc904ef45fbdb508b5a50c2dfc3a1b4e647fee04655b5392a8520e079e)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleDialogflowCxFlowEventHandlersTriggerFulfillmentSetParameterActionsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c541f89743bc296f16f4c020a2a70c5dc373b7354aa36161ab1482de47aeb6fe)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b3a0503fe09a702f31a139eb8a7dfb556ff06b6c53476a4294840f14b231b11c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d6cf7ea8214c4ca0a99eee21e0cf65fee0b65d6581d592e2d3d31b0952b82d5e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDialogflowCxFlowEventHandlersTriggerFulfillmentSetParameterActions]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDialogflowCxFlowEventHandlersTriggerFulfillmentSetParameterActions]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDialogflowCxFlowEventHandlersTriggerFulfillmentSetParameterActions]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c918962fb69ac22fe5c492c71097cef5730be8d3a6fdd704d0a953706262f01)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleDialogflowCxFlowEventHandlersTriggerFulfillmentSetParameterActionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDialogflowCxFlow.GoogleDialogflowCxFlowEventHandlersTriggerFulfillmentSetParameterActionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9e849e95ac9146804ad1cc766b09fdac80cb113b5fc45e4da4325aecd79c3bb9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ee39d77d0d3a755ced9500b7843b711e233e1f5458838cf3e5f254227d056d77)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "parameter", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__645180431c81e6015f9b747ca228f3de8abb61a09f9c6aaca262bc6f8bdfe421)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDialogflowCxFlowEventHandlersTriggerFulfillmentSetParameterActions]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDialogflowCxFlowEventHandlersTriggerFulfillmentSetParameterActions]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDialogflowCxFlowEventHandlersTriggerFulfillmentSetParameterActions]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__404abb45a68419b24509e89c3c666e1384d97c4fb58a267936d63a46cd84b790)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDialogflowCxFlow.GoogleDialogflowCxFlowKnowledgeConnectorSettings",
    jsii_struct_bases=[],
    name_mapping={
        "data_store_connections": "dataStoreConnections",
        "enabled": "enabled",
        "target_flow": "targetFlow",
        "target_page": "targetPage",
        "trigger_fulfillment": "triggerFulfillment",
    },
)
class GoogleDialogflowCxFlowKnowledgeConnectorSettings:
    def __init__(
        self,
        *,
        data_store_connections: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleDialogflowCxFlowKnowledgeConnectorSettingsDataStoreConnections", typing.Dict[builtins.str, typing.Any]]]]] = None,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        target_flow: typing.Optional[builtins.str] = None,
        target_page: typing.Optional[builtins.str] = None,
        trigger_fulfillment: typing.Optional[typing.Union["GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillment", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param data_store_connections: data_store_connections block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#data_store_connections GoogleDialogflowCxFlow#data_store_connections}
        :param enabled: Whether Knowledge Connector is enabled or not. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#enabled GoogleDialogflowCxFlow#enabled}
        :param target_flow: The target flow to transition to. Format: projects//locations//agents//flows/. This field is part of a union field 'target': Only one of 'targetPage' or 'targetFlow' may be set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#target_flow GoogleDialogflowCxFlow#target_flow}
        :param target_page: The target page to transition to. Format: projects//locations//agents//flows//pages/. The page must be in the same host flow (the flow that owns this 'KnowledgeConnectorSettings'). This field is part of a union field 'target': Only one of 'targetPage' or 'targetFlow' may be set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#target_page GoogleDialogflowCxFlow#target_page}
        :param trigger_fulfillment: trigger_fulfillment block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#trigger_fulfillment GoogleDialogflowCxFlow#trigger_fulfillment}
        '''
        if isinstance(trigger_fulfillment, dict):
            trigger_fulfillment = GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillment(**trigger_fulfillment)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4895735831ff36aef22d4802ce53b60d5076c6af9ff3cd15c5d596ec4a1b6b1f)
            check_type(argname="argument data_store_connections", value=data_store_connections, expected_type=type_hints["data_store_connections"])
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument target_flow", value=target_flow, expected_type=type_hints["target_flow"])
            check_type(argname="argument target_page", value=target_page, expected_type=type_hints["target_page"])
            check_type(argname="argument trigger_fulfillment", value=trigger_fulfillment, expected_type=type_hints["trigger_fulfillment"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if data_store_connections is not None:
            self._values["data_store_connections"] = data_store_connections
        if enabled is not None:
            self._values["enabled"] = enabled
        if target_flow is not None:
            self._values["target_flow"] = target_flow
        if target_page is not None:
            self._values["target_page"] = target_page
        if trigger_fulfillment is not None:
            self._values["trigger_fulfillment"] = trigger_fulfillment

    @builtins.property
    def data_store_connections(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleDialogflowCxFlowKnowledgeConnectorSettingsDataStoreConnections"]]]:
        '''data_store_connections block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#data_store_connections GoogleDialogflowCxFlow#data_store_connections}
        '''
        result = self._values.get("data_store_connections")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleDialogflowCxFlowKnowledgeConnectorSettingsDataStoreConnections"]]], result)

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether Knowledge Connector is enabled or not.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#enabled GoogleDialogflowCxFlow#enabled}
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def target_flow(self) -> typing.Optional[builtins.str]:
        '''The target flow to transition to.

        Format: projects//locations//agents//flows/.
        This field is part of a union field 'target': Only one of 'targetPage' or 'targetFlow' may be set.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#target_flow GoogleDialogflowCxFlow#target_flow}
        '''
        result = self._values.get("target_flow")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def target_page(self) -> typing.Optional[builtins.str]:
        '''The target page to transition to.

        Format: projects//locations//agents//flows//pages/.
        The page must be in the same host flow (the flow that owns this 'KnowledgeConnectorSettings').
        This field is part of a union field 'target': Only one of 'targetPage' or 'targetFlow' may be set.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#target_page GoogleDialogflowCxFlow#target_page}
        '''
        result = self._values.get("target_page")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def trigger_fulfillment(
        self,
    ) -> typing.Optional["GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillment"]:
        '''trigger_fulfillment block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#trigger_fulfillment GoogleDialogflowCxFlow#trigger_fulfillment}
        '''
        result = self._values.get("trigger_fulfillment")
        return typing.cast(typing.Optional["GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillment"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDialogflowCxFlowKnowledgeConnectorSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDialogflowCxFlow.GoogleDialogflowCxFlowKnowledgeConnectorSettingsDataStoreConnections",
    jsii_struct_bases=[],
    name_mapping={
        "data_store": "dataStore",
        "data_store_type": "dataStoreType",
        "document_processing_mode": "documentProcessingMode",
    },
)
class GoogleDialogflowCxFlowKnowledgeConnectorSettingsDataStoreConnections:
    def __init__(
        self,
        *,
        data_store: typing.Optional[builtins.str] = None,
        data_store_type: typing.Optional[builtins.str] = None,
        document_processing_mode: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param data_store: The full name of the referenced data store. Formats: projects/{project}/locations/{location}/collections/{collection}/dataStores/{dataStore} projects/{project}/locations/{location}/dataStores/{dataStore}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#data_store GoogleDialogflowCxFlow#data_store}
        :param data_store_type: The type of the connected data store. - PUBLIC_WEB: A data store that contains public web content. - UNSTRUCTURED: A data store that contains unstructured private data. - STRUCTURED: A data store that contains structured data (for example FAQ). Possible values: ["PUBLIC_WEB", "UNSTRUCTURED", "STRUCTURED"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#data_store_type GoogleDialogflowCxFlow#data_store_type}
        :param document_processing_mode: The document processing mode for the data store connection. Should only be set for PUBLIC_WEB and UNSTRUCTURED data stores. If not set it is considered as DOCUMENTS, as this is the legacy mode. - DOCUMENTS: Documents are processed as documents. - CHUNKS: Documents are converted to chunks. Possible values: ["DOCUMENTS", "CHUNKS"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#document_processing_mode GoogleDialogflowCxFlow#document_processing_mode}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c2db33e6c1852358223a4a1919e6bd2721a030a06c0bce5c4ff43e2cb603f9f0)
            check_type(argname="argument data_store", value=data_store, expected_type=type_hints["data_store"])
            check_type(argname="argument data_store_type", value=data_store_type, expected_type=type_hints["data_store_type"])
            check_type(argname="argument document_processing_mode", value=document_processing_mode, expected_type=type_hints["document_processing_mode"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if data_store is not None:
            self._values["data_store"] = data_store
        if data_store_type is not None:
            self._values["data_store_type"] = data_store_type
        if document_processing_mode is not None:
            self._values["document_processing_mode"] = document_processing_mode

    @builtins.property
    def data_store(self) -> typing.Optional[builtins.str]:
        '''The full name of the referenced data store. Formats: projects/{project}/locations/{location}/collections/{collection}/dataStores/{dataStore} projects/{project}/locations/{location}/dataStores/{dataStore}.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#data_store GoogleDialogflowCxFlow#data_store}
        '''
        result = self._values.get("data_store")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def data_store_type(self) -> typing.Optional[builtins.str]:
        '''The type of the connected data store.

        - PUBLIC_WEB: A data store that contains public web content.
        - UNSTRUCTURED: A data store that contains unstructured private data.
        - STRUCTURED: A data store that contains structured data (for example FAQ). Possible values: ["PUBLIC_WEB", "UNSTRUCTURED", "STRUCTURED"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#data_store_type GoogleDialogflowCxFlow#data_store_type}
        '''
        result = self._values.get("data_store_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def document_processing_mode(self) -> typing.Optional[builtins.str]:
        '''The document processing mode for the data store connection.

        Should only be set for PUBLIC_WEB and UNSTRUCTURED data stores. If not set it is considered as DOCUMENTS, as this is the legacy mode.

        - DOCUMENTS: Documents are processed as documents.
        - CHUNKS: Documents are converted to chunks. Possible values: ["DOCUMENTS", "CHUNKS"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#document_processing_mode GoogleDialogflowCxFlow#document_processing_mode}
        '''
        result = self._values.get("document_processing_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDialogflowCxFlowKnowledgeConnectorSettingsDataStoreConnections(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDialogflowCxFlowKnowledgeConnectorSettingsDataStoreConnectionsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDialogflowCxFlow.GoogleDialogflowCxFlowKnowledgeConnectorSettingsDataStoreConnectionsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__96860768c90bb930356f1e3ac037a4cfe9a0b188952139a39d40bebed5e4126f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleDialogflowCxFlowKnowledgeConnectorSettingsDataStoreConnectionsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e5c02b6c4007dc4b93f138859d7e19ff65ffd93570a7b363a6ce748ba442aa5c)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleDialogflowCxFlowKnowledgeConnectorSettingsDataStoreConnectionsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d1585289b2b7da555eee8f15913541598350247153dcf605adc800dccb76bd3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__017aeb8599ae55a6ffd0d5d067e50419ab3fb8b5c13ceda047fb0954af3bde61)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d827aefacd7c573682da51af165f664a36cf2ed0de0de1a73acb5b7bb83e188e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDialogflowCxFlowKnowledgeConnectorSettingsDataStoreConnections]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDialogflowCxFlowKnowledgeConnectorSettingsDataStoreConnections]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDialogflowCxFlowKnowledgeConnectorSettingsDataStoreConnections]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1909f8394c8d6380dec9fe6dcb10eaee50db66f51835a6bf2b9d855d945c9402)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleDialogflowCxFlowKnowledgeConnectorSettingsDataStoreConnectionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDialogflowCxFlow.GoogleDialogflowCxFlowKnowledgeConnectorSettingsDataStoreConnectionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0141c759169d740cc0cda2e699028e89811eb3f60fe520fe4ef7e2915546ecd6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetDataStore")
    def reset_data_store(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDataStore", []))

    @jsii.member(jsii_name="resetDataStoreType")
    def reset_data_store_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDataStoreType", []))

    @jsii.member(jsii_name="resetDocumentProcessingMode")
    def reset_document_processing_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDocumentProcessingMode", []))

    @builtins.property
    @jsii.member(jsii_name="dataStoreInput")
    def data_store_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dataStoreInput"))

    @builtins.property
    @jsii.member(jsii_name="dataStoreTypeInput")
    def data_store_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dataStoreTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="documentProcessingModeInput")
    def document_processing_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "documentProcessingModeInput"))

    @builtins.property
    @jsii.member(jsii_name="dataStore")
    def data_store(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dataStore"))

    @data_store.setter
    def data_store(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f4b80698f774ac7ee463f23a41e437324c7467aaa610d9d3140c3dbbf54f80d5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dataStore", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dataStoreType")
    def data_store_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dataStoreType"))

    @data_store_type.setter
    def data_store_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e4e40cd3095a5d845e4691eb085178b7ed8753bc5a26590bd144c4fad4e60299)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dataStoreType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="documentProcessingMode")
    def document_processing_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "documentProcessingMode"))

    @document_processing_mode.setter
    def document_processing_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3279b5d7c01ccf2b5a11cb5170756ca125fc208f151d2add4c9233a0eeb66279)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "documentProcessingMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDialogflowCxFlowKnowledgeConnectorSettingsDataStoreConnections]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDialogflowCxFlowKnowledgeConnectorSettingsDataStoreConnections]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDialogflowCxFlowKnowledgeConnectorSettingsDataStoreConnections]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c2f71b0de45fc46f13177a0438c5648b2c1e71b06c25e5d9cd8ee81109082932)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleDialogflowCxFlowKnowledgeConnectorSettingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDialogflowCxFlow.GoogleDialogflowCxFlowKnowledgeConnectorSettingsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__553468fdfe39b122adbb174d9142692897748ece50a051bdbb684f55ed0528e5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putDataStoreConnections")
    def put_data_store_connections(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleDialogflowCxFlowKnowledgeConnectorSettingsDataStoreConnections, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__966823029217fd19a3729262f168c7cb08f49e6c3daf610c405f207064e7c97b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putDataStoreConnections", [value]))

    @jsii.member(jsii_name="putTriggerFulfillment")
    def put_trigger_fulfillment(
        self,
        *,
        advanced_settings: typing.Optional[typing.Union["GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentAdvancedSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        conditional_cases: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentConditionalCases", typing.Dict[builtins.str, typing.Any]]]]] = None,
        enable_generative_fallback: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        messages: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentMessages", typing.Dict[builtins.str, typing.Any]]]]] = None,
        return_partial_responses: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        set_parameter_actions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentSetParameterActions", typing.Dict[builtins.str, typing.Any]]]]] = None,
        tag: typing.Optional[builtins.str] = None,
        webhook: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param advanced_settings: advanced_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#advanced_settings GoogleDialogflowCxFlow#advanced_settings}
        :param conditional_cases: conditional_cases block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#conditional_cases GoogleDialogflowCxFlow#conditional_cases}
        :param enable_generative_fallback: If the flag is true, the agent will utilize LLM to generate a text response. If LLM generation fails, the defined responses in the fulfillment will be respected. This flag is only useful for fulfillments associated with no-match event handlers. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#enable_generative_fallback GoogleDialogflowCxFlow#enable_generative_fallback}
        :param messages: messages block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#messages GoogleDialogflowCxFlow#messages}
        :param return_partial_responses: Whether Dialogflow should return currently queued fulfillment response messages in streaming APIs. If a webhook is specified, it happens before Dialogflow invokes webhook. Warning: 1) This flag only affects streaming API. Responses are still queued and returned once in non-streaming API. 2) The flag can be enabled in any fulfillment but only the first 3 partial responses will be returned. You may only want to apply it to fulfillments that have slow webhooks. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#return_partial_responses GoogleDialogflowCxFlow#return_partial_responses}
        :param set_parameter_actions: set_parameter_actions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#set_parameter_actions GoogleDialogflowCxFlow#set_parameter_actions}
        :param tag: The tag used by the webhook to identify which fulfillment is being called. This field is required if webhook is specified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#tag GoogleDialogflowCxFlow#tag}
        :param webhook: The webhook to call. Format: projects//locations//agents//webhooks/. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#webhook GoogleDialogflowCxFlow#webhook}
        '''
        value = GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillment(
            advanced_settings=advanced_settings,
            conditional_cases=conditional_cases,
            enable_generative_fallback=enable_generative_fallback,
            messages=messages,
            return_partial_responses=return_partial_responses,
            set_parameter_actions=set_parameter_actions,
            tag=tag,
            webhook=webhook,
        )

        return typing.cast(None, jsii.invoke(self, "putTriggerFulfillment", [value]))

    @jsii.member(jsii_name="resetDataStoreConnections")
    def reset_data_store_connections(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDataStoreConnections", []))

    @jsii.member(jsii_name="resetEnabled")
    def reset_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnabled", []))

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
    @jsii.member(jsii_name="dataStoreConnections")
    def data_store_connections(
        self,
    ) -> GoogleDialogflowCxFlowKnowledgeConnectorSettingsDataStoreConnectionsList:
        return typing.cast(GoogleDialogflowCxFlowKnowledgeConnectorSettingsDataStoreConnectionsList, jsii.get(self, "dataStoreConnections"))

    @builtins.property
    @jsii.member(jsii_name="triggerFulfillment")
    def trigger_fulfillment(
        self,
    ) -> "GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentOutputReference":
        return typing.cast("GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentOutputReference", jsii.get(self, "triggerFulfillment"))

    @builtins.property
    @jsii.member(jsii_name="dataStoreConnectionsInput")
    def data_store_connections_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDialogflowCxFlowKnowledgeConnectorSettingsDataStoreConnections]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDialogflowCxFlowKnowledgeConnectorSettingsDataStoreConnections]]], jsii.get(self, "dataStoreConnectionsInput"))

    @builtins.property
    @jsii.member(jsii_name="enabledInput")
    def enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enabledInput"))

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
    ) -> typing.Optional["GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillment"]:
        return typing.cast(typing.Optional["GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillment"], jsii.get(self, "triggerFulfillmentInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__a11aca10931e6041e92881ba007f12227988048fdd33eee10b52a9737bce58cb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="targetFlow")
    def target_flow(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "targetFlow"))

    @target_flow.setter
    def target_flow(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9c01d25c9744df665875024fd57a3aeb50c191eafabe1393fad3e72534683714)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "targetFlow", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="targetPage")
    def target_page(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "targetPage"))

    @target_page.setter
    def target_page(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__88e4207fa49dec1138d1cb31b07baa445a32fc34d1d51a016a5070b681aaa216)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "targetPage", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDialogflowCxFlowKnowledgeConnectorSettings]:
        return typing.cast(typing.Optional[GoogleDialogflowCxFlowKnowledgeConnectorSettings], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDialogflowCxFlowKnowledgeConnectorSettings],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0b8beb22dc061ba0fa9a28b27578276ba3bddb409e94df89b99276dbe16cdc52)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDialogflowCxFlow.GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillment",
    jsii_struct_bases=[],
    name_mapping={
        "advanced_settings": "advancedSettings",
        "conditional_cases": "conditionalCases",
        "enable_generative_fallback": "enableGenerativeFallback",
        "messages": "messages",
        "return_partial_responses": "returnPartialResponses",
        "set_parameter_actions": "setParameterActions",
        "tag": "tag",
        "webhook": "webhook",
    },
)
class GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillment:
    def __init__(
        self,
        *,
        advanced_settings: typing.Optional[typing.Union["GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentAdvancedSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        conditional_cases: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentConditionalCases", typing.Dict[builtins.str, typing.Any]]]]] = None,
        enable_generative_fallback: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        messages: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentMessages", typing.Dict[builtins.str, typing.Any]]]]] = None,
        return_partial_responses: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        set_parameter_actions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentSetParameterActions", typing.Dict[builtins.str, typing.Any]]]]] = None,
        tag: typing.Optional[builtins.str] = None,
        webhook: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param advanced_settings: advanced_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#advanced_settings GoogleDialogflowCxFlow#advanced_settings}
        :param conditional_cases: conditional_cases block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#conditional_cases GoogleDialogflowCxFlow#conditional_cases}
        :param enable_generative_fallback: If the flag is true, the agent will utilize LLM to generate a text response. If LLM generation fails, the defined responses in the fulfillment will be respected. This flag is only useful for fulfillments associated with no-match event handlers. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#enable_generative_fallback GoogleDialogflowCxFlow#enable_generative_fallback}
        :param messages: messages block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#messages GoogleDialogflowCxFlow#messages}
        :param return_partial_responses: Whether Dialogflow should return currently queued fulfillment response messages in streaming APIs. If a webhook is specified, it happens before Dialogflow invokes webhook. Warning: 1) This flag only affects streaming API. Responses are still queued and returned once in non-streaming API. 2) The flag can be enabled in any fulfillment but only the first 3 partial responses will be returned. You may only want to apply it to fulfillments that have slow webhooks. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#return_partial_responses GoogleDialogflowCxFlow#return_partial_responses}
        :param set_parameter_actions: set_parameter_actions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#set_parameter_actions GoogleDialogflowCxFlow#set_parameter_actions}
        :param tag: The tag used by the webhook to identify which fulfillment is being called. This field is required if webhook is specified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#tag GoogleDialogflowCxFlow#tag}
        :param webhook: The webhook to call. Format: projects//locations//agents//webhooks/. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#webhook GoogleDialogflowCxFlow#webhook}
        '''
        if isinstance(advanced_settings, dict):
            advanced_settings = GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentAdvancedSettings(**advanced_settings)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__61c09bd1713fba814cee6c32162a4065faaee6366df7a2dd9c3f7e007b839861)
            check_type(argname="argument advanced_settings", value=advanced_settings, expected_type=type_hints["advanced_settings"])
            check_type(argname="argument conditional_cases", value=conditional_cases, expected_type=type_hints["conditional_cases"])
            check_type(argname="argument enable_generative_fallback", value=enable_generative_fallback, expected_type=type_hints["enable_generative_fallback"])
            check_type(argname="argument messages", value=messages, expected_type=type_hints["messages"])
            check_type(argname="argument return_partial_responses", value=return_partial_responses, expected_type=type_hints["return_partial_responses"])
            check_type(argname="argument set_parameter_actions", value=set_parameter_actions, expected_type=type_hints["set_parameter_actions"])
            check_type(argname="argument tag", value=tag, expected_type=type_hints["tag"])
            check_type(argname="argument webhook", value=webhook, expected_type=type_hints["webhook"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if advanced_settings is not None:
            self._values["advanced_settings"] = advanced_settings
        if conditional_cases is not None:
            self._values["conditional_cases"] = conditional_cases
        if enable_generative_fallback is not None:
            self._values["enable_generative_fallback"] = enable_generative_fallback
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
    def advanced_settings(
        self,
    ) -> typing.Optional["GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentAdvancedSettings"]:
        '''advanced_settings block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#advanced_settings GoogleDialogflowCxFlow#advanced_settings}
        '''
        result = self._values.get("advanced_settings")
        return typing.cast(typing.Optional["GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentAdvancedSettings"], result)

    @builtins.property
    def conditional_cases(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentConditionalCases"]]]:
        '''conditional_cases block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#conditional_cases GoogleDialogflowCxFlow#conditional_cases}
        '''
        result = self._values.get("conditional_cases")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentConditionalCases"]]], result)

    @builtins.property
    def enable_generative_fallback(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If the flag is true, the agent will utilize LLM to generate a text response.

        If LLM generation fails, the defined responses in the fulfillment will be respected. This flag is only useful for fulfillments associated with no-match event handlers.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#enable_generative_fallback GoogleDialogflowCxFlow#enable_generative_fallback}
        '''
        result = self._values.get("enable_generative_fallback")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def messages(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentMessages"]]]:
        '''messages block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#messages GoogleDialogflowCxFlow#messages}
        '''
        result = self._values.get("messages")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentMessages"]]], result)

    @builtins.property
    def return_partial_responses(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether Dialogflow should return currently queued fulfillment response messages in streaming APIs.

        If a webhook is specified, it happens before Dialogflow invokes webhook. Warning: 1) This flag only affects streaming API. Responses are still queued and returned once in non-streaming API. 2) The flag can be enabled in any fulfillment but only the first 3 partial responses will be returned. You may only want to apply it to fulfillments that have slow webhooks.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#return_partial_responses GoogleDialogflowCxFlow#return_partial_responses}
        '''
        result = self._values.get("return_partial_responses")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def set_parameter_actions(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentSetParameterActions"]]]:
        '''set_parameter_actions block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#set_parameter_actions GoogleDialogflowCxFlow#set_parameter_actions}
        '''
        result = self._values.get("set_parameter_actions")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentSetParameterActions"]]], result)

    @builtins.property
    def tag(self) -> typing.Optional[builtins.str]:
        '''The tag used by the webhook to identify which fulfillment is being called.

        This field is required if webhook is specified.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#tag GoogleDialogflowCxFlow#tag}
        '''
        result = self._values.get("tag")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def webhook(self) -> typing.Optional[builtins.str]:
        '''The webhook to call. Format: projects//locations//agents//webhooks/.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#webhook GoogleDialogflowCxFlow#webhook}
        '''
        result = self._values.get("webhook")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillment(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDialogflowCxFlow.GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentAdvancedSettings",
    jsii_struct_bases=[],
    name_mapping={
        "dtmf_settings": "dtmfSettings",
        "logging_settings": "loggingSettings",
        "speech_settings": "speechSettings",
    },
)
class GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentAdvancedSettings:
    def __init__(
        self,
        *,
        dtmf_settings: typing.Optional[typing.Union["GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentAdvancedSettingsDtmfSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        logging_settings: typing.Optional[typing.Union["GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentAdvancedSettingsLoggingSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        speech_settings: typing.Optional[typing.Union["GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentAdvancedSettingsSpeechSettings", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param dtmf_settings: dtmf_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#dtmf_settings GoogleDialogflowCxFlow#dtmf_settings}
        :param logging_settings: logging_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#logging_settings GoogleDialogflowCxFlow#logging_settings}
        :param speech_settings: speech_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#speech_settings GoogleDialogflowCxFlow#speech_settings}
        '''
        if isinstance(dtmf_settings, dict):
            dtmf_settings = GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentAdvancedSettingsDtmfSettings(**dtmf_settings)
        if isinstance(logging_settings, dict):
            logging_settings = GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentAdvancedSettingsLoggingSettings(**logging_settings)
        if isinstance(speech_settings, dict):
            speech_settings = GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentAdvancedSettingsSpeechSettings(**speech_settings)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d27c1e3315ac786ad057f159b214ed632d9d24c28842b05e867e7c741784e9b0)
            check_type(argname="argument dtmf_settings", value=dtmf_settings, expected_type=type_hints["dtmf_settings"])
            check_type(argname="argument logging_settings", value=logging_settings, expected_type=type_hints["logging_settings"])
            check_type(argname="argument speech_settings", value=speech_settings, expected_type=type_hints["speech_settings"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if dtmf_settings is not None:
            self._values["dtmf_settings"] = dtmf_settings
        if logging_settings is not None:
            self._values["logging_settings"] = logging_settings
        if speech_settings is not None:
            self._values["speech_settings"] = speech_settings

    @builtins.property
    def dtmf_settings(
        self,
    ) -> typing.Optional["GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentAdvancedSettingsDtmfSettings"]:
        '''dtmf_settings block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#dtmf_settings GoogleDialogflowCxFlow#dtmf_settings}
        '''
        result = self._values.get("dtmf_settings")
        return typing.cast(typing.Optional["GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentAdvancedSettingsDtmfSettings"], result)

    @builtins.property
    def logging_settings(
        self,
    ) -> typing.Optional["GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentAdvancedSettingsLoggingSettings"]:
        '''logging_settings block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#logging_settings GoogleDialogflowCxFlow#logging_settings}
        '''
        result = self._values.get("logging_settings")
        return typing.cast(typing.Optional["GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentAdvancedSettingsLoggingSettings"], result)

    @builtins.property
    def speech_settings(
        self,
    ) -> typing.Optional["GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentAdvancedSettingsSpeechSettings"]:
        '''speech_settings block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#speech_settings GoogleDialogflowCxFlow#speech_settings}
        '''
        result = self._values.get("speech_settings")
        return typing.cast(typing.Optional["GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentAdvancedSettingsSpeechSettings"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentAdvancedSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDialogflowCxFlow.GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentAdvancedSettingsDtmfSettings",
    jsii_struct_bases=[],
    name_mapping={
        "enabled": "enabled",
        "endpointing_timeout_duration": "endpointingTimeoutDuration",
        "finish_digit": "finishDigit",
        "interdigit_timeout_duration": "interdigitTimeoutDuration",
        "max_digits": "maxDigits",
    },
)
class GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentAdvancedSettingsDtmfSettings:
    def __init__(
        self,
        *,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        endpointing_timeout_duration: typing.Optional[builtins.str] = None,
        finish_digit: typing.Optional[builtins.str] = None,
        interdigit_timeout_duration: typing.Optional[builtins.str] = None,
        max_digits: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param enabled: If true, incoming audio is processed for DTMF (dual tone multi frequtectency) events. For example, if the caller presses a button on their telephone keypad and DTMF processing is enabled, Dialogflow will de the event (e.g. a "3" was pressed) in the incoming audio and pass the event to the bot to drive business logic (e.g. when 3 is pressed, return the account balance). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#enabled GoogleDialogflowCxFlow#enabled}
        :param endpointing_timeout_duration: Endpoint timeout setting for matching dtmf input to regex. A duration in seconds with up to nine fractional digits, ending with 's'. Example: "3.500s". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#endpointing_timeout_duration GoogleDialogflowCxFlow#endpointing_timeout_duration}
        :param finish_digit: The digit that terminates a DTMF digit sequence. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#finish_digit GoogleDialogflowCxFlow#finish_digit}
        :param interdigit_timeout_duration: Interdigit timeout setting for matching dtmf input to regex. A duration in seconds with up to nine fractional digits, ending with 's'. Example: "3.500s". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#interdigit_timeout_duration GoogleDialogflowCxFlow#interdigit_timeout_duration}
        :param max_digits: Max length of DTMF digits. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#max_digits GoogleDialogflowCxFlow#max_digits}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ecf201bf5ef3ff8d12af6463226798015d1b6d371419d1fbe7799e0d41661e3)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument endpointing_timeout_duration", value=endpointing_timeout_duration, expected_type=type_hints["endpointing_timeout_duration"])
            check_type(argname="argument finish_digit", value=finish_digit, expected_type=type_hints["finish_digit"])
            check_type(argname="argument interdigit_timeout_duration", value=interdigit_timeout_duration, expected_type=type_hints["interdigit_timeout_duration"])
            check_type(argname="argument max_digits", value=max_digits, expected_type=type_hints["max_digits"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if enabled is not None:
            self._values["enabled"] = enabled
        if endpointing_timeout_duration is not None:
            self._values["endpointing_timeout_duration"] = endpointing_timeout_duration
        if finish_digit is not None:
            self._values["finish_digit"] = finish_digit
        if interdigit_timeout_duration is not None:
            self._values["interdigit_timeout_duration"] = interdigit_timeout_duration
        if max_digits is not None:
            self._values["max_digits"] = max_digits

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If true, incoming audio is processed for DTMF (dual tone multi frequtectency) events.

        For example, if the caller presses a button on their telephone keypad and DTMF processing is enabled, Dialogflow will de the event (e.g. a "3" was pressed) in the incoming audio and pass the event to the bot to drive business logic (e.g. when 3 is pressed, return the account balance).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#enabled GoogleDialogflowCxFlow#enabled}
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def endpointing_timeout_duration(self) -> typing.Optional[builtins.str]:
        '''Endpoint timeout setting for matching dtmf input to regex.

        A duration in seconds with up to nine fractional digits, ending with 's'. Example: "3.500s".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#endpointing_timeout_duration GoogleDialogflowCxFlow#endpointing_timeout_duration}
        '''
        result = self._values.get("endpointing_timeout_duration")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def finish_digit(self) -> typing.Optional[builtins.str]:
        '''The digit that terminates a DTMF digit sequence.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#finish_digit GoogleDialogflowCxFlow#finish_digit}
        '''
        result = self._values.get("finish_digit")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def interdigit_timeout_duration(self) -> typing.Optional[builtins.str]:
        '''Interdigit timeout setting for matching dtmf input to regex.

        A duration in seconds with up to nine fractional digits, ending with 's'. Example: "3.500s".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#interdigit_timeout_duration GoogleDialogflowCxFlow#interdigit_timeout_duration}
        '''
        result = self._values.get("interdigit_timeout_duration")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def max_digits(self) -> typing.Optional[jsii.Number]:
        '''Max length of DTMF digits.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#max_digits GoogleDialogflowCxFlow#max_digits}
        '''
        result = self._values.get("max_digits")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentAdvancedSettingsDtmfSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentAdvancedSettingsDtmfSettingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDialogflowCxFlow.GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentAdvancedSettingsDtmfSettingsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__26fc93952bc0e8c19e688df7fa2f0220a11004d373ed44323512682ddded55a3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetEnabled")
    def reset_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnabled", []))

    @jsii.member(jsii_name="resetEndpointingTimeoutDuration")
    def reset_endpointing_timeout_duration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEndpointingTimeoutDuration", []))

    @jsii.member(jsii_name="resetFinishDigit")
    def reset_finish_digit(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFinishDigit", []))

    @jsii.member(jsii_name="resetInterdigitTimeoutDuration")
    def reset_interdigit_timeout_duration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInterdigitTimeoutDuration", []))

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
    @jsii.member(jsii_name="endpointingTimeoutDurationInput")
    def endpointing_timeout_duration_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "endpointingTimeoutDurationInput"))

    @builtins.property
    @jsii.member(jsii_name="finishDigitInput")
    def finish_digit_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "finishDigitInput"))

    @builtins.property
    @jsii.member(jsii_name="interdigitTimeoutDurationInput")
    def interdigit_timeout_duration_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "interdigitTimeoutDurationInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__d5141eec5c11f7ecc2ccfb926d7c613b68343f213218bcd90ce3740b768bc75f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="endpointingTimeoutDuration")
    def endpointing_timeout_duration(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "endpointingTimeoutDuration"))

    @endpointing_timeout_duration.setter
    def endpointing_timeout_duration(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fe1c696022530a728c2ba038a0184b2677ba8b5af9b5cc0b0ccb995e9c6f0dd1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "endpointingTimeoutDuration", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="finishDigit")
    def finish_digit(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "finishDigit"))

    @finish_digit.setter
    def finish_digit(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7ed8f48fcba0836be1f96495b016b188887020b6317ed9550b19257ad1d6bde5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "finishDigit", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="interdigitTimeoutDuration")
    def interdigit_timeout_duration(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "interdigitTimeoutDuration"))

    @interdigit_timeout_duration.setter
    def interdigit_timeout_duration(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d839e915331d8bf2bc6ec768f3c4eb33b0bbcd2dbc05d4d7f7f88a9338081d1c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "interdigitTimeoutDuration", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxDigits")
    def max_digits(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxDigits"))

    @max_digits.setter
    def max_digits(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a02d66f3bcd3895d6a7c12848a776ad08585789fa85f9a613e3036669db9ac97)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxDigits", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentAdvancedSettingsDtmfSettings]:
        return typing.cast(typing.Optional[GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentAdvancedSettingsDtmfSettings], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentAdvancedSettingsDtmfSettings],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__453e822885b4998da7eb548d6d248ddfee6912ae1922e064ca42ba8d64fff390)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDialogflowCxFlow.GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentAdvancedSettingsLoggingSettings",
    jsii_struct_bases=[],
    name_mapping={
        "enable_consent_based_redaction": "enableConsentBasedRedaction",
        "enable_interaction_logging": "enableInteractionLogging",
        "enable_stackdriver_logging": "enableStackdriverLogging",
    },
)
class GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentAdvancedSettingsLoggingSettings:
    def __init__(
        self,
        *,
        enable_consent_based_redaction: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_interaction_logging: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_stackdriver_logging: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param enable_consent_based_redaction: Enables consent-based end-user input redaction, if true, a pre-defined session parameter **$session.params.conversation-redaction** will be used to determine if the utterance should be redacted. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#enable_consent_based_redaction GoogleDialogflowCxFlow#enable_consent_based_redaction}
        :param enable_interaction_logging: Enables DF Interaction logging. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#enable_interaction_logging GoogleDialogflowCxFlow#enable_interaction_logging}
        :param enable_stackdriver_logging: Enables Google Cloud Logging. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#enable_stackdriver_logging GoogleDialogflowCxFlow#enable_stackdriver_logging}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9133c5c6eeee3c5e77e353fd96664574f8ba70f9bd6ec63190094796b4b23a66)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#enable_consent_based_redaction GoogleDialogflowCxFlow#enable_consent_based_redaction}
        '''
        result = self._values.get("enable_consent_based_redaction")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def enable_interaction_logging(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Enables DF Interaction logging.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#enable_interaction_logging GoogleDialogflowCxFlow#enable_interaction_logging}
        '''
        result = self._values.get("enable_interaction_logging")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def enable_stackdriver_logging(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Enables Google Cloud Logging.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#enable_stackdriver_logging GoogleDialogflowCxFlow#enable_stackdriver_logging}
        '''
        result = self._values.get("enable_stackdriver_logging")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentAdvancedSettingsLoggingSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentAdvancedSettingsLoggingSettingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDialogflowCxFlow.GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentAdvancedSettingsLoggingSettingsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b8256ffb535ab55f7080dd956c218b6ef7eac42b5c399a2a7433490e93cc835d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3abaf43708f51e71d6a9eb8781a9de7e6c882b9fb0189055d22e20851de3861b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a51cdb22632e0ff830126024216f8b6dcdac1f3f77e1a5702a13405e727780f2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3b45a896cbfdc93041bb124f325b1399c13b5bc9e3484c76bd4d5901ee090e37)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableStackdriverLogging", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentAdvancedSettingsLoggingSettings]:
        return typing.cast(typing.Optional[GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentAdvancedSettingsLoggingSettings], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentAdvancedSettingsLoggingSettings],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c0d73456de78cf99f30f036cf5c477369c6d21d44b698f503c3753355500a7c9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentAdvancedSettingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDialogflowCxFlow.GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentAdvancedSettingsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6f7cc235c8ff5a76245800c191ddb02a6d4778cb17e9e418aed8854aebb31eeb)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putDtmfSettings")
    def put_dtmf_settings(
        self,
        *,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        endpointing_timeout_duration: typing.Optional[builtins.str] = None,
        finish_digit: typing.Optional[builtins.str] = None,
        interdigit_timeout_duration: typing.Optional[builtins.str] = None,
        max_digits: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param enabled: If true, incoming audio is processed for DTMF (dual tone multi frequtectency) events. For example, if the caller presses a button on their telephone keypad and DTMF processing is enabled, Dialogflow will de the event (e.g. a "3" was pressed) in the incoming audio and pass the event to the bot to drive business logic (e.g. when 3 is pressed, return the account balance). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#enabled GoogleDialogflowCxFlow#enabled}
        :param endpointing_timeout_duration: Endpoint timeout setting for matching dtmf input to regex. A duration in seconds with up to nine fractional digits, ending with 's'. Example: "3.500s". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#endpointing_timeout_duration GoogleDialogflowCxFlow#endpointing_timeout_duration}
        :param finish_digit: The digit that terminates a DTMF digit sequence. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#finish_digit GoogleDialogflowCxFlow#finish_digit}
        :param interdigit_timeout_duration: Interdigit timeout setting for matching dtmf input to regex. A duration in seconds with up to nine fractional digits, ending with 's'. Example: "3.500s". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#interdigit_timeout_duration GoogleDialogflowCxFlow#interdigit_timeout_duration}
        :param max_digits: Max length of DTMF digits. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#max_digits GoogleDialogflowCxFlow#max_digits}
        '''
        value = GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentAdvancedSettingsDtmfSettings(
            enabled=enabled,
            endpointing_timeout_duration=endpointing_timeout_duration,
            finish_digit=finish_digit,
            interdigit_timeout_duration=interdigit_timeout_duration,
            max_digits=max_digits,
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
        :param enable_consent_based_redaction: Enables consent-based end-user input redaction, if true, a pre-defined session parameter **$session.params.conversation-redaction** will be used to determine if the utterance should be redacted. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#enable_consent_based_redaction GoogleDialogflowCxFlow#enable_consent_based_redaction}
        :param enable_interaction_logging: Enables DF Interaction logging. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#enable_interaction_logging GoogleDialogflowCxFlow#enable_interaction_logging}
        :param enable_stackdriver_logging: Enables Google Cloud Logging. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#enable_stackdriver_logging GoogleDialogflowCxFlow#enable_stackdriver_logging}
        '''
        value = GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentAdvancedSettingsLoggingSettings(
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
        :param endpointer_sensitivity: Sensitivity of the speech model that detects the end of speech. Scale from 0 to 100. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#endpointer_sensitivity GoogleDialogflowCxFlow#endpointer_sensitivity}
        :param models: Mapping from language to Speech-to-Text model. The mapped Speech-to-Text model will be selected for requests from its corresponding language. For more information, see `Speech models <https://cloud.google.com/dialogflow/cx/docs/concept/speech-models>`_. An object containing a list of **"key": value** pairs. Example: **{ "name": "wrench", "mass": "1.3kg", "count": "3" }**. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#models GoogleDialogflowCxFlow#models}
        :param no_speech_timeout: Timeout before detecting no speech. A duration in seconds with up to nine fractional digits, ending with 's'. Example: "3.500s". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#no_speech_timeout GoogleDialogflowCxFlow#no_speech_timeout}
        :param use_timeout_based_endpointing: Use timeout based endpointing, interpreting endpointer sensitivity as seconds of timeout value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#use_timeout_based_endpointing GoogleDialogflowCxFlow#use_timeout_based_endpointing}
        '''
        value = GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentAdvancedSettingsSpeechSettings(
            endpointer_sensitivity=endpointer_sensitivity,
            models=models,
            no_speech_timeout=no_speech_timeout,
            use_timeout_based_endpointing=use_timeout_based_endpointing,
        )

        return typing.cast(None, jsii.invoke(self, "putSpeechSettings", [value]))

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
    @jsii.member(jsii_name="dtmfSettings")
    def dtmf_settings(
        self,
    ) -> GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentAdvancedSettingsDtmfSettingsOutputReference:
        return typing.cast(GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentAdvancedSettingsDtmfSettingsOutputReference, jsii.get(self, "dtmfSettings"))

    @builtins.property
    @jsii.member(jsii_name="loggingSettings")
    def logging_settings(
        self,
    ) -> GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentAdvancedSettingsLoggingSettingsOutputReference:
        return typing.cast(GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentAdvancedSettingsLoggingSettingsOutputReference, jsii.get(self, "loggingSettings"))

    @builtins.property
    @jsii.member(jsii_name="speechSettings")
    def speech_settings(
        self,
    ) -> "GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentAdvancedSettingsSpeechSettingsOutputReference":
        return typing.cast("GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentAdvancedSettingsSpeechSettingsOutputReference", jsii.get(self, "speechSettings"))

    @builtins.property
    @jsii.member(jsii_name="dtmfSettingsInput")
    def dtmf_settings_input(
        self,
    ) -> typing.Optional[GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentAdvancedSettingsDtmfSettings]:
        return typing.cast(typing.Optional[GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentAdvancedSettingsDtmfSettings], jsii.get(self, "dtmfSettingsInput"))

    @builtins.property
    @jsii.member(jsii_name="loggingSettingsInput")
    def logging_settings_input(
        self,
    ) -> typing.Optional[GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentAdvancedSettingsLoggingSettings]:
        return typing.cast(typing.Optional[GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentAdvancedSettingsLoggingSettings], jsii.get(self, "loggingSettingsInput"))

    @builtins.property
    @jsii.member(jsii_name="speechSettingsInput")
    def speech_settings_input(
        self,
    ) -> typing.Optional["GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentAdvancedSettingsSpeechSettings"]:
        return typing.cast(typing.Optional["GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentAdvancedSettingsSpeechSettings"], jsii.get(self, "speechSettingsInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentAdvancedSettings]:
        return typing.cast(typing.Optional[GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentAdvancedSettings], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentAdvancedSettings],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bc0cad544b71343b72faf63639a34bfa5124ffb71583606c737b491742da5ed5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDialogflowCxFlow.GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentAdvancedSettingsSpeechSettings",
    jsii_struct_bases=[],
    name_mapping={
        "endpointer_sensitivity": "endpointerSensitivity",
        "models": "models",
        "no_speech_timeout": "noSpeechTimeout",
        "use_timeout_based_endpointing": "useTimeoutBasedEndpointing",
    },
)
class GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentAdvancedSettingsSpeechSettings:
    def __init__(
        self,
        *,
        endpointer_sensitivity: typing.Optional[jsii.Number] = None,
        models: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        no_speech_timeout: typing.Optional[builtins.str] = None,
        use_timeout_based_endpointing: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param endpointer_sensitivity: Sensitivity of the speech model that detects the end of speech. Scale from 0 to 100. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#endpointer_sensitivity GoogleDialogflowCxFlow#endpointer_sensitivity}
        :param models: Mapping from language to Speech-to-Text model. The mapped Speech-to-Text model will be selected for requests from its corresponding language. For more information, see `Speech models <https://cloud.google.com/dialogflow/cx/docs/concept/speech-models>`_. An object containing a list of **"key": value** pairs. Example: **{ "name": "wrench", "mass": "1.3kg", "count": "3" }**. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#models GoogleDialogflowCxFlow#models}
        :param no_speech_timeout: Timeout before detecting no speech. A duration in seconds with up to nine fractional digits, ending with 's'. Example: "3.500s". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#no_speech_timeout GoogleDialogflowCxFlow#no_speech_timeout}
        :param use_timeout_based_endpointing: Use timeout based endpointing, interpreting endpointer sensitivity as seconds of timeout value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#use_timeout_based_endpointing GoogleDialogflowCxFlow#use_timeout_based_endpointing}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c880a72ba2e942a2e6f762c4b4ac83519f868dc0ea444055b19a16990d79936)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#endpointer_sensitivity GoogleDialogflowCxFlow#endpointer_sensitivity}
        '''
        result = self._values.get("endpointer_sensitivity")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def models(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Mapping from language to Speech-to-Text model.

        The mapped Speech-to-Text model will be selected for requests from its corresponding language. For more information, see `Speech models <https://cloud.google.com/dialogflow/cx/docs/concept/speech-models>`_.
        An object containing a list of **"key": value** pairs. Example: **{ "name": "wrench", "mass": "1.3kg", "count": "3" }**.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#models GoogleDialogflowCxFlow#models}
        '''
        result = self._values.get("models")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def no_speech_timeout(self) -> typing.Optional[builtins.str]:
        '''Timeout before detecting no speech. A duration in seconds with up to nine fractional digits, ending with 's'. Example: "3.500s".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#no_speech_timeout GoogleDialogflowCxFlow#no_speech_timeout}
        '''
        result = self._values.get("no_speech_timeout")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def use_timeout_based_endpointing(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Use timeout based endpointing, interpreting endpointer sensitivity as seconds of timeout value.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#use_timeout_based_endpointing GoogleDialogflowCxFlow#use_timeout_based_endpointing}
        '''
        result = self._values.get("use_timeout_based_endpointing")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentAdvancedSettingsSpeechSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentAdvancedSettingsSpeechSettingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDialogflowCxFlow.GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentAdvancedSettingsSpeechSettingsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4128d2cc3ee905397ebcd8438fe38a7bb27730de3af5446a4245cdf3e1a3d4e0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__202f5caafe97df860ef041e9b31f617d610b3ddb037962fd9f47281c8c975d13)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "endpointerSensitivity", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="models")
    def models(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "models"))

    @models.setter
    def models(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a2ffa7919ea24f10179497728bef4521001bcc2cbddf357c1a0b0b278bd5612)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "models", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="noSpeechTimeout")
    def no_speech_timeout(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "noSpeechTimeout"))

    @no_speech_timeout.setter
    def no_speech_timeout(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9303fc7d7f14b4b9c3db917f357a4556f8d79dc588e267a82a46aa59c7a378cd)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ea01611390474913569e29eeeacc75f8b169fbbd645c249d53f842848d917fc9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "useTimeoutBasedEndpointing", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentAdvancedSettingsSpeechSettings]:
        return typing.cast(typing.Optional[GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentAdvancedSettingsSpeechSettings], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentAdvancedSettingsSpeechSettings],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4eff1b1d631b021134faa90955fc43116541ce38cf35629fede416632b81737d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDialogflowCxFlow.GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentConditionalCases",
    jsii_struct_bases=[],
    name_mapping={"cases": "cases"},
)
class GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentConditionalCases:
    def __init__(self, *, cases: typing.Optional[builtins.str] = None) -> None:
        '''
        :param cases: A JSON encoded list of cascading if-else conditions. Cases are mutually exclusive. The first one with a matching condition is selected, all the rest ignored. See `Case <https://cloud.google.com/dialogflow/cx/docs/reference/rest/v3/Fulfillment#case>`_ for the schema. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#cases GoogleDialogflowCxFlow#cases}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c415dab972eed9d090cf49c4b658347c00a3bf803b4ce2bb055174aaa57866b8)
            check_type(argname="argument cases", value=cases, expected_type=type_hints["cases"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if cases is not None:
            self._values["cases"] = cases

    @builtins.property
    def cases(self) -> typing.Optional[builtins.str]:
        '''A JSON encoded list of cascading if-else conditions.

        Cases are mutually exclusive. The first one with a matching condition is selected, all the rest ignored.
        See `Case <https://cloud.google.com/dialogflow/cx/docs/reference/rest/v3/Fulfillment#case>`_ for the schema.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#cases GoogleDialogflowCxFlow#cases}
        '''
        result = self._values.get("cases")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentConditionalCases(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentConditionalCasesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDialogflowCxFlow.GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentConditionalCasesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a1ec138620154f9a9e9aa2a079e65e4a4025f1091cd1e38e0e01258d3315cf1a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentConditionalCasesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c1d181a1fa30e4e6ce6a7acc5992646fb2a0b59059e4aef8ce5f7bd9dd2df639)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentConditionalCasesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__82b3091048f4d51d8532425b23a17c88d4eb7b3e01967462ff1de319fb88f29c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__15affd6185dbf94a3d761ca4bd59630d14584464234188ce06f6ca76d19dc8fe)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ecb4b60be1d0cad6c2027056951fa2207ba232b99f024aa7df84216a138efffc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentConditionalCases]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentConditionalCases]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentConditionalCases]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e5bb0f62ff94a3249a3fcea65930f405c467e08f247019a4873b69a1bbdbc084)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentConditionalCasesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDialogflowCxFlow.GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentConditionalCasesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1ca55a1bf56741348bfd6bff257da60aec962c96259a6f3f30d6d755e8dba2a2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3f8a0e0cf9697d472539bcc0c2173e6e5a59f0584a52d74c18e0f221b9a19f0b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cases", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentConditionalCases]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentConditionalCases]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentConditionalCases]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ae31b66b4721fd4d36b0acff39f3d9efd5212c86bea2e5f01de94f6be394d104)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDialogflowCxFlow.GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentMessages",
    jsii_struct_bases=[],
    name_mapping={
        "channel": "channel",
        "conversation_success": "conversationSuccess",
        "knowledge_info_card": "knowledgeInfoCard",
        "live_agent_handoff": "liveAgentHandoff",
        "output_audio_text": "outputAudioText",
        "payload": "payload",
        "play_audio": "playAudio",
        "telephony_transfer_call": "telephonyTransferCall",
        "text": "text",
    },
)
class GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentMessages:
    def __init__(
        self,
        *,
        channel: typing.Optional[builtins.str] = None,
        conversation_success: typing.Optional[typing.Union["GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentMessagesConversationSuccess", typing.Dict[builtins.str, typing.Any]]] = None,
        knowledge_info_card: typing.Optional[typing.Union["GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentMessagesKnowledgeInfoCard", typing.Dict[builtins.str, typing.Any]]] = None,
        live_agent_handoff: typing.Optional[typing.Union["GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentMessagesLiveAgentHandoff", typing.Dict[builtins.str, typing.Any]]] = None,
        output_audio_text: typing.Optional[typing.Union["GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentMessagesOutputAudioText", typing.Dict[builtins.str, typing.Any]]] = None,
        payload: typing.Optional[builtins.str] = None,
        play_audio: typing.Optional[typing.Union["GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentMessagesPlayAudio", typing.Dict[builtins.str, typing.Any]]] = None,
        telephony_transfer_call: typing.Optional[typing.Union["GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentMessagesTelephonyTransferCall", typing.Dict[builtins.str, typing.Any]]] = None,
        text: typing.Optional[typing.Union["GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentMessagesText", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param channel: The channel which the response is associated with. Clients can specify the channel via QueryParameters.channel, and only associated channel response will be returned. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#channel GoogleDialogflowCxFlow#channel}
        :param conversation_success: conversation_success block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#conversation_success GoogleDialogflowCxFlow#conversation_success}
        :param knowledge_info_card: knowledge_info_card block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#knowledge_info_card GoogleDialogflowCxFlow#knowledge_info_card}
        :param live_agent_handoff: live_agent_handoff block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#live_agent_handoff GoogleDialogflowCxFlow#live_agent_handoff}
        :param output_audio_text: output_audio_text block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#output_audio_text GoogleDialogflowCxFlow#output_audio_text}
        :param payload: Returns a response containing a custom, platform-specific payload. This field is part of a union field 'message': Only one of 'text', 'payload', 'conversationSuccess', 'outputAudioText', 'liveAgentHandoff', 'endInteraction', 'playAudio', 'mixedAudio', 'telephonyTransferCall', or 'knowledgeInfoCard' may be set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#payload GoogleDialogflowCxFlow#payload}
        :param play_audio: play_audio block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#play_audio GoogleDialogflowCxFlow#play_audio}
        :param telephony_transfer_call: telephony_transfer_call block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#telephony_transfer_call GoogleDialogflowCxFlow#telephony_transfer_call}
        :param text: text block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#text GoogleDialogflowCxFlow#text}
        '''
        if isinstance(conversation_success, dict):
            conversation_success = GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentMessagesConversationSuccess(**conversation_success)
        if isinstance(knowledge_info_card, dict):
            knowledge_info_card = GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentMessagesKnowledgeInfoCard(**knowledge_info_card)
        if isinstance(live_agent_handoff, dict):
            live_agent_handoff = GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentMessagesLiveAgentHandoff(**live_agent_handoff)
        if isinstance(output_audio_text, dict):
            output_audio_text = GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentMessagesOutputAudioText(**output_audio_text)
        if isinstance(play_audio, dict):
            play_audio = GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentMessagesPlayAudio(**play_audio)
        if isinstance(telephony_transfer_call, dict):
            telephony_transfer_call = GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentMessagesTelephonyTransferCall(**telephony_transfer_call)
        if isinstance(text, dict):
            text = GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentMessagesText(**text)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8f6a6bc532e6403fc912fbe2a036388695609a011a5b3f836de836afc6a284f5)
            check_type(argname="argument channel", value=channel, expected_type=type_hints["channel"])
            check_type(argname="argument conversation_success", value=conversation_success, expected_type=type_hints["conversation_success"])
            check_type(argname="argument knowledge_info_card", value=knowledge_info_card, expected_type=type_hints["knowledge_info_card"])
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
        if knowledge_info_card is not None:
            self._values["knowledge_info_card"] = knowledge_info_card
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#channel GoogleDialogflowCxFlow#channel}
        '''
        result = self._values.get("channel")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def conversation_success(
        self,
    ) -> typing.Optional["GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentMessagesConversationSuccess"]:
        '''conversation_success block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#conversation_success GoogleDialogflowCxFlow#conversation_success}
        '''
        result = self._values.get("conversation_success")
        return typing.cast(typing.Optional["GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentMessagesConversationSuccess"], result)

    @builtins.property
    def knowledge_info_card(
        self,
    ) -> typing.Optional["GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentMessagesKnowledgeInfoCard"]:
        '''knowledge_info_card block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#knowledge_info_card GoogleDialogflowCxFlow#knowledge_info_card}
        '''
        result = self._values.get("knowledge_info_card")
        return typing.cast(typing.Optional["GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentMessagesKnowledgeInfoCard"], result)

    @builtins.property
    def live_agent_handoff(
        self,
    ) -> typing.Optional["GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentMessagesLiveAgentHandoff"]:
        '''live_agent_handoff block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#live_agent_handoff GoogleDialogflowCxFlow#live_agent_handoff}
        '''
        result = self._values.get("live_agent_handoff")
        return typing.cast(typing.Optional["GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentMessagesLiveAgentHandoff"], result)

    @builtins.property
    def output_audio_text(
        self,
    ) -> typing.Optional["GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentMessagesOutputAudioText"]:
        '''output_audio_text block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#output_audio_text GoogleDialogflowCxFlow#output_audio_text}
        '''
        result = self._values.get("output_audio_text")
        return typing.cast(typing.Optional["GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentMessagesOutputAudioText"], result)

    @builtins.property
    def payload(self) -> typing.Optional[builtins.str]:
        '''Returns a response containing a custom, platform-specific payload.

        This field is part of a union field 'message': Only one of 'text', 'payload', 'conversationSuccess', 'outputAudioText', 'liveAgentHandoff', 'endInteraction', 'playAudio', 'mixedAudio', 'telephonyTransferCall', or 'knowledgeInfoCard' may be set.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#payload GoogleDialogflowCxFlow#payload}
        '''
        result = self._values.get("payload")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def play_audio(
        self,
    ) -> typing.Optional["GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentMessagesPlayAudio"]:
        '''play_audio block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#play_audio GoogleDialogflowCxFlow#play_audio}
        '''
        result = self._values.get("play_audio")
        return typing.cast(typing.Optional["GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentMessagesPlayAudio"], result)

    @builtins.property
    def telephony_transfer_call(
        self,
    ) -> typing.Optional["GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentMessagesTelephonyTransferCall"]:
        '''telephony_transfer_call block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#telephony_transfer_call GoogleDialogflowCxFlow#telephony_transfer_call}
        '''
        result = self._values.get("telephony_transfer_call")
        return typing.cast(typing.Optional["GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentMessagesTelephonyTransferCall"], result)

    @builtins.property
    def text(
        self,
    ) -> typing.Optional["GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentMessagesText"]:
        '''text block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#text GoogleDialogflowCxFlow#text}
        '''
        result = self._values.get("text")
        return typing.cast(typing.Optional["GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentMessagesText"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentMessages(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDialogflowCxFlow.GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentMessagesConversationSuccess",
    jsii_struct_bases=[],
    name_mapping={"metadata": "metadata"},
)
class GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentMessagesConversationSuccess:
    def __init__(self, *, metadata: typing.Optional[builtins.str] = None) -> None:
        '''
        :param metadata: Custom metadata. Dialogflow doesn't impose any structure on this. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#metadata GoogleDialogflowCxFlow#metadata}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__14cd7102922e60646f31f1d75d74115844d03f54a06e7fe2441d19c8920faf8e)
            check_type(argname="argument metadata", value=metadata, expected_type=type_hints["metadata"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if metadata is not None:
            self._values["metadata"] = metadata

    @builtins.property
    def metadata(self) -> typing.Optional[builtins.str]:
        '''Custom metadata. Dialogflow doesn't impose any structure on this.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#metadata GoogleDialogflowCxFlow#metadata}
        '''
        result = self._values.get("metadata")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentMessagesConversationSuccess(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentMessagesConversationSuccessOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDialogflowCxFlow.GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentMessagesConversationSuccessOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d4033ef7c0d319e14b3cdcd8afed07b3af344f0846815d11e96346ae0bdc03ee)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f44a196e5b84a41361554375fad0fa5a1832ae74ee114530a8cf7763e69b4030)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metadata", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentMessagesConversationSuccess]:
        return typing.cast(typing.Optional[GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentMessagesConversationSuccess], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentMessagesConversationSuccess],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__61625681278978bb556af655883541c87ba90741e383d68da2af1a841c02afdc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDialogflowCxFlow.GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentMessagesEndInteraction",
    jsii_struct_bases=[],
    name_mapping={},
)
class GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentMessagesEndInteraction:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentMessagesEndInteraction(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentMessagesEndInteractionList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDialogflowCxFlow.GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentMessagesEndInteractionList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d8f2878fd3481953339f1c9a83bd7cb38551289e7a56c8ab0af196a38e232c3a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentMessagesEndInteractionOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__165b64b80feda19c61604bd45681edff95b51b8db1b78cb3a4cb093cfe21ca59)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentMessagesEndInteractionOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b6a1043b02fabd859f0a577f961594d2d18b99b28b153a7e0939dae853196512)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c477cd966ca6f90275836dcca77bf135649148ee5fa9dac9fde5ec57a658e8bf)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8da5df974d7dc4a2d60d0db32a04c15fb43db614aa0d903ffe2e2e997b429c75)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentMessagesEndInteractionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDialogflowCxFlow.GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentMessagesEndInteractionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d3fbce1b1b4330e103528320ecb7ef6cd0e17befd49b5b6a6abbd70a27723a27)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentMessagesEndInteraction]:
        return typing.cast(typing.Optional[GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentMessagesEndInteraction], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentMessagesEndInteraction],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f9e6d0d84bd1b3f11917e913f9a3790cc4bba68780a39c595324dc5208fb5d3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDialogflowCxFlow.GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentMessagesKnowledgeInfoCard",
    jsii_struct_bases=[],
    name_mapping={},
)
class GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentMessagesKnowledgeInfoCard:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentMessagesKnowledgeInfoCard(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentMessagesKnowledgeInfoCardOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDialogflowCxFlow.GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentMessagesKnowledgeInfoCardOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0bdd2e61f92789e8c1ae634e6fc22cea87a7a5e76d5409b46aa020805e658c26)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentMessagesKnowledgeInfoCard]:
        return typing.cast(typing.Optional[GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentMessagesKnowledgeInfoCard], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentMessagesKnowledgeInfoCard],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e58ef0648e803de0f6ad54fcdb3b29a5dd2ad5cb6a54813f4f01289fac87c8cb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentMessagesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDialogflowCxFlow.GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentMessagesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d6af67eb4efe099eca0491c5399e2b57eba1312cdfffdf37752af6c1c57dc947)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentMessagesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1cc99ab72aab37db27822fe17462f86b124276db04859f554d0836452d88d5e2)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentMessagesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__28f5d9f7f6ca35d3a6348f6ccc46452837f4eb71d8fc7925ea7640899c4c3a64)
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
            type_hints = typing.get_type_hints(_typecheckingstub__414cbdf1466ae5d28187e4d1566c53e33efd9f070460f660e6ecfa200979c5cf)
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
            type_hints = typing.get_type_hints(_typecheckingstub__07bf1fbbe372506ef5942f52399a98760f21953854536830fa3e6eb0e305f38b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentMessages]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentMessages]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentMessages]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2a787d65125828ac0c89c33a09b1e5bfe479b1fb6d13924e665aef243cc539e1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDialogflowCxFlow.GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentMessagesLiveAgentHandoff",
    jsii_struct_bases=[],
    name_mapping={"metadata": "metadata"},
)
class GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentMessagesLiveAgentHandoff:
    def __init__(self, *, metadata: typing.Optional[builtins.str] = None) -> None:
        '''
        :param metadata: Custom metadata. Dialogflow doesn't impose any structure on this. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#metadata GoogleDialogflowCxFlow#metadata}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b9d2187a3f51d016e83ef0586a8c75528af56d26a0173717d7d00ada2e31435c)
            check_type(argname="argument metadata", value=metadata, expected_type=type_hints["metadata"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if metadata is not None:
            self._values["metadata"] = metadata

    @builtins.property
    def metadata(self) -> typing.Optional[builtins.str]:
        '''Custom metadata. Dialogflow doesn't impose any structure on this.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#metadata GoogleDialogflowCxFlow#metadata}
        '''
        result = self._values.get("metadata")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentMessagesLiveAgentHandoff(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentMessagesLiveAgentHandoffOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDialogflowCxFlow.GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentMessagesLiveAgentHandoffOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__62de3b71663e780c7e1fe09707923bb8e2ace0b4c3b4565b6b4208cd6007a919)
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
            type_hints = typing.get_type_hints(_typecheckingstub__07263cc98fb9f102f38f0d4ab8b589f7fefbdbe0c9c7f383fd5bdc955e108682)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metadata", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentMessagesLiveAgentHandoff]:
        return typing.cast(typing.Optional[GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentMessagesLiveAgentHandoff], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentMessagesLiveAgentHandoff],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e503f332afabf467ee66c1469aec82784e02cf3084d93852e034645c8344081)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDialogflowCxFlow.GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentMessagesMixedAudio",
    jsii_struct_bases=[],
    name_mapping={},
)
class GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentMessagesMixedAudio:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentMessagesMixedAudio(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentMessagesMixedAudioList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDialogflowCxFlow.GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentMessagesMixedAudioList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__604a16fa6c641a22ff234206ba936b2beaf7f37e75c0398794ff9fe70cf690e5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentMessagesMixedAudioOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f6628aa239e76f57366d6bfdc8438aa7760680c590e8f9768d497ad3577de6ec)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentMessagesMixedAudioOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c6d38cc5de9e4a89d020c5f79d31e4a92e73824f7db312ab2c019e616a9f7df2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__745ec9fee7229bc241f4e1df64e9f038492ff195b07c2caac30c7e12e4e871fa)
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
            type_hints = typing.get_type_hints(_typecheckingstub__db10fb5ec1fd173d4398a0cc30f361ff59df39beb47f4c0f7998e6f2de694aea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentMessagesMixedAudioOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDialogflowCxFlow.GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentMessagesMixedAudioOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8674ecea09a0e152c48b1e085d163eb3934247d34f7e55a9bb00cc2388277e7c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="segments")
    def segments(
        self,
    ) -> "GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentMessagesMixedAudioSegmentsList":
        return typing.cast("GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentMessagesMixedAudioSegmentsList", jsii.get(self, "segments"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentMessagesMixedAudio]:
        return typing.cast(typing.Optional[GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentMessagesMixedAudio], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentMessagesMixedAudio],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__997addcbfe45927c3dfb348d690e739e6297ae0c4237dc06bd08470f1ee228bb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDialogflowCxFlow.GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentMessagesMixedAudioSegments",
    jsii_struct_bases=[],
    name_mapping={},
)
class GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentMessagesMixedAudioSegments:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentMessagesMixedAudioSegments(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentMessagesMixedAudioSegmentsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDialogflowCxFlow.GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentMessagesMixedAudioSegmentsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9cee157f77d7f52bc96acf7ecf83e75f7ef114fb4f1ca136c7996278788e67c1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentMessagesMixedAudioSegmentsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f92a49f44d1c9054235e38b7e44e3636265e89ac4af3bdaadc070b0a6f4f1b32)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentMessagesMixedAudioSegmentsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b7284b7f8e93160927df17c6c55238304d8e00a942a5e31dcf2ec4c1f18cf5b4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__410ad1ee2f7b3329209fc5c5f5597a2120ba7078841b426bfaec4e1637df9a56)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9be1ffb9358f746fb89debd6e559f6d680f1e2dfc02270806f4c50c071772426)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentMessagesMixedAudioSegmentsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDialogflowCxFlow.GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentMessagesMixedAudioSegmentsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d0ba0b8c826f24181408e4da7c605851fc985f24247c2691fbe499dcbcb0867d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="allowPlaybackInterruption")
    def allow_playback_interruption(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "allowPlaybackInterruption"))

    @builtins.property
    @jsii.member(jsii_name="audio")
    def audio(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "audio"))

    @builtins.property
    @jsii.member(jsii_name="uri")
    def uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "uri"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentMessagesMixedAudioSegments]:
        return typing.cast(typing.Optional[GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentMessagesMixedAudioSegments], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentMessagesMixedAudioSegments],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__85b6a48b37b6716d9dadde9fbe09d8901b6ca1e5f625bad15089e0a4eda26119)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDialogflowCxFlow.GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentMessagesOutputAudioText",
    jsii_struct_bases=[],
    name_mapping={"ssml": "ssml", "text": "text"},
)
class GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentMessagesOutputAudioText:
    def __init__(
        self,
        *,
        ssml: typing.Optional[builtins.str] = None,
        text: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param ssml: The SSML text to be synthesized. For more information, see SSML. This field is part of a union field 'source': Only one of 'text' or 'ssml' may be set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#ssml GoogleDialogflowCxFlow#ssml}
        :param text: The raw text to be synthesized. This field is part of a union field 'source': Only one of 'text' or 'ssml' may be set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#text GoogleDialogflowCxFlow#text}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f580abc06de8355d78901540b820e50beeec9d07bad1cad42948a27ab75cf26)
            check_type(argname="argument ssml", value=ssml, expected_type=type_hints["ssml"])
            check_type(argname="argument text", value=text, expected_type=type_hints["text"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if ssml is not None:
            self._values["ssml"] = ssml
        if text is not None:
            self._values["text"] = text

    @builtins.property
    def ssml(self) -> typing.Optional[builtins.str]:
        '''The SSML text to be synthesized.

        For more information, see SSML.
        This field is part of a union field 'source': Only one of 'text' or 'ssml' may be set.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#ssml GoogleDialogflowCxFlow#ssml}
        '''
        result = self._values.get("ssml")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def text(self) -> typing.Optional[builtins.str]:
        '''The raw text to be synthesized.

        This field is part of a union field 'source': Only one of 'text' or 'ssml' may be set.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#text GoogleDialogflowCxFlow#text}
        '''
        result = self._values.get("text")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentMessagesOutputAudioText(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentMessagesOutputAudioTextOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDialogflowCxFlow.GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentMessagesOutputAudioTextOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__798e33e06758f3a4e7f51d02745e83391c1fc302c133d5eed3085ee2e223a5a2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__056f7f27d3e3e5d39ef984c18ae65c95eb1f160f687985a2c3123501b1fac513)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ssml", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="text")
    def text(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "text"))

    @text.setter
    def text(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3795b9c9c09e4d847122c978a2c55f808591197cc922ae88c5bb9859b41b17ed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "text", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentMessagesOutputAudioText]:
        return typing.cast(typing.Optional[GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentMessagesOutputAudioText], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentMessagesOutputAudioText],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a96f2d3ba9a5ea8ecde280f2710a9584b93002dd1808abf407954958be5f0642)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentMessagesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDialogflowCxFlow.GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentMessagesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__030dc961255b053398c28345e67cca09d4ea8739108a20598544679129757531)
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
        :param metadata: Custom metadata. Dialogflow doesn't impose any structure on this. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#metadata GoogleDialogflowCxFlow#metadata}
        '''
        value = GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentMessagesConversationSuccess(
            metadata=metadata
        )

        return typing.cast(None, jsii.invoke(self, "putConversationSuccess", [value]))

    @jsii.member(jsii_name="putKnowledgeInfoCard")
    def put_knowledge_info_card(self) -> None:
        value = GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentMessagesKnowledgeInfoCard()

        return typing.cast(None, jsii.invoke(self, "putKnowledgeInfoCard", [value]))

    @jsii.member(jsii_name="putLiveAgentHandoff")
    def put_live_agent_handoff(
        self,
        *,
        metadata: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param metadata: Custom metadata. Dialogflow doesn't impose any structure on this. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#metadata GoogleDialogflowCxFlow#metadata}
        '''
        value = GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentMessagesLiveAgentHandoff(
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
        :param ssml: The SSML text to be synthesized. For more information, see SSML. This field is part of a union field 'source': Only one of 'text' or 'ssml' may be set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#ssml GoogleDialogflowCxFlow#ssml}
        :param text: The raw text to be synthesized. This field is part of a union field 'source': Only one of 'text' or 'ssml' may be set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#text GoogleDialogflowCxFlow#text}
        '''
        value = GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentMessagesOutputAudioText(
            ssml=ssml, text=text
        )

        return typing.cast(None, jsii.invoke(self, "putOutputAudioText", [value]))

    @jsii.member(jsii_name="putPlayAudio")
    def put_play_audio(self, *, audio_uri: builtins.str) -> None:
        '''
        :param audio_uri: URI of the audio clip. Dialogflow does not impose any validation on this value. It is specific to the client that reads it. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#audio_uri GoogleDialogflowCxFlow#audio_uri}
        '''
        value = GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentMessagesPlayAudio(
            audio_uri=audio_uri
        )

        return typing.cast(None, jsii.invoke(self, "putPlayAudio", [value]))

    @jsii.member(jsii_name="putTelephonyTransferCall")
    def put_telephony_transfer_call(self, *, phone_number: builtins.str) -> None:
        '''
        :param phone_number: Transfer the call to a phone number in E.164 format. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#phone_number GoogleDialogflowCxFlow#phone_number}
        '''
        value = GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentMessagesTelephonyTransferCall(
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
        :param text: A collection of text response variants. If multiple variants are defined, only one text response variant is returned at runtime. required: true Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#text GoogleDialogflowCxFlow#text}
        '''
        value = GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentMessagesText(
            text=text
        )

        return typing.cast(None, jsii.invoke(self, "putText", [value]))

    @jsii.member(jsii_name="resetChannel")
    def reset_channel(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetChannel", []))

    @jsii.member(jsii_name="resetConversationSuccess")
    def reset_conversation_success(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConversationSuccess", []))

    @jsii.member(jsii_name="resetKnowledgeInfoCard")
    def reset_knowledge_info_card(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKnowledgeInfoCard", []))

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
    ) -> GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentMessagesConversationSuccessOutputReference:
        return typing.cast(GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentMessagesConversationSuccessOutputReference, jsii.get(self, "conversationSuccess"))

    @builtins.property
    @jsii.member(jsii_name="endInteraction")
    def end_interaction(
        self,
    ) -> GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentMessagesEndInteractionList:
        return typing.cast(GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentMessagesEndInteractionList, jsii.get(self, "endInteraction"))

    @builtins.property
    @jsii.member(jsii_name="knowledgeInfoCard")
    def knowledge_info_card(
        self,
    ) -> GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentMessagesKnowledgeInfoCardOutputReference:
        return typing.cast(GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentMessagesKnowledgeInfoCardOutputReference, jsii.get(self, "knowledgeInfoCard"))

    @builtins.property
    @jsii.member(jsii_name="liveAgentHandoff")
    def live_agent_handoff(
        self,
    ) -> GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentMessagesLiveAgentHandoffOutputReference:
        return typing.cast(GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentMessagesLiveAgentHandoffOutputReference, jsii.get(self, "liveAgentHandoff"))

    @builtins.property
    @jsii.member(jsii_name="mixedAudio")
    def mixed_audio(
        self,
    ) -> GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentMessagesMixedAudioList:
        return typing.cast(GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentMessagesMixedAudioList, jsii.get(self, "mixedAudio"))

    @builtins.property
    @jsii.member(jsii_name="outputAudioText")
    def output_audio_text(
        self,
    ) -> GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentMessagesOutputAudioTextOutputReference:
        return typing.cast(GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentMessagesOutputAudioTextOutputReference, jsii.get(self, "outputAudioText"))

    @builtins.property
    @jsii.member(jsii_name="playAudio")
    def play_audio(
        self,
    ) -> "GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentMessagesPlayAudioOutputReference":
        return typing.cast("GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentMessagesPlayAudioOutputReference", jsii.get(self, "playAudio"))

    @builtins.property
    @jsii.member(jsii_name="telephonyTransferCall")
    def telephony_transfer_call(
        self,
    ) -> "GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentMessagesTelephonyTransferCallOutputReference":
        return typing.cast("GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentMessagesTelephonyTransferCallOutputReference", jsii.get(self, "telephonyTransferCall"))

    @builtins.property
    @jsii.member(jsii_name="text")
    def text(
        self,
    ) -> "GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentMessagesTextOutputReference":
        return typing.cast("GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentMessagesTextOutputReference", jsii.get(self, "text"))

    @builtins.property
    @jsii.member(jsii_name="channelInput")
    def channel_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "channelInput"))

    @builtins.property
    @jsii.member(jsii_name="conversationSuccessInput")
    def conversation_success_input(
        self,
    ) -> typing.Optional[GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentMessagesConversationSuccess]:
        return typing.cast(typing.Optional[GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentMessagesConversationSuccess], jsii.get(self, "conversationSuccessInput"))

    @builtins.property
    @jsii.member(jsii_name="knowledgeInfoCardInput")
    def knowledge_info_card_input(
        self,
    ) -> typing.Optional[GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentMessagesKnowledgeInfoCard]:
        return typing.cast(typing.Optional[GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentMessagesKnowledgeInfoCard], jsii.get(self, "knowledgeInfoCardInput"))

    @builtins.property
    @jsii.member(jsii_name="liveAgentHandoffInput")
    def live_agent_handoff_input(
        self,
    ) -> typing.Optional[GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentMessagesLiveAgentHandoff]:
        return typing.cast(typing.Optional[GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentMessagesLiveAgentHandoff], jsii.get(self, "liveAgentHandoffInput"))

    @builtins.property
    @jsii.member(jsii_name="outputAudioTextInput")
    def output_audio_text_input(
        self,
    ) -> typing.Optional[GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentMessagesOutputAudioText]:
        return typing.cast(typing.Optional[GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentMessagesOutputAudioText], jsii.get(self, "outputAudioTextInput"))

    @builtins.property
    @jsii.member(jsii_name="payloadInput")
    def payload_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "payloadInput"))

    @builtins.property
    @jsii.member(jsii_name="playAudioInput")
    def play_audio_input(
        self,
    ) -> typing.Optional["GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentMessagesPlayAudio"]:
        return typing.cast(typing.Optional["GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentMessagesPlayAudio"], jsii.get(self, "playAudioInput"))

    @builtins.property
    @jsii.member(jsii_name="telephonyTransferCallInput")
    def telephony_transfer_call_input(
        self,
    ) -> typing.Optional["GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentMessagesTelephonyTransferCall"]:
        return typing.cast(typing.Optional["GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentMessagesTelephonyTransferCall"], jsii.get(self, "telephonyTransferCallInput"))

    @builtins.property
    @jsii.member(jsii_name="textInput")
    def text_input(
        self,
    ) -> typing.Optional["GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentMessagesText"]:
        return typing.cast(typing.Optional["GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentMessagesText"], jsii.get(self, "textInput"))

    @builtins.property
    @jsii.member(jsii_name="channel")
    def channel(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "channel"))

    @channel.setter
    def channel(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__be495b72980c5399b0036df5ba3b68f9b220106106640b4cc7a47283ab4f4de7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "channel", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="payload")
    def payload(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "payload"))

    @payload.setter
    def payload(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1bf3940821ceea1106c96f20732ccfce25feeda3d6d3787ab56bd96d95753616)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "payload", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentMessages]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentMessages]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentMessages]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__83435ede2c4242be3414d53f8e58664b6e4cc491ebcea1bcb07b57240d12a8a0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDialogflowCxFlow.GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentMessagesPlayAudio",
    jsii_struct_bases=[],
    name_mapping={"audio_uri": "audioUri"},
)
class GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentMessagesPlayAudio:
    def __init__(self, *, audio_uri: builtins.str) -> None:
        '''
        :param audio_uri: URI of the audio clip. Dialogflow does not impose any validation on this value. It is specific to the client that reads it. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#audio_uri GoogleDialogflowCxFlow#audio_uri}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cb7af42ca688f446ceaec9e314df249af25abc90bd24289883e99fb610fa70d3)
            check_type(argname="argument audio_uri", value=audio_uri, expected_type=type_hints["audio_uri"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "audio_uri": audio_uri,
        }

    @builtins.property
    def audio_uri(self) -> builtins.str:
        '''URI of the audio clip.

        Dialogflow does not impose any validation on this value. It is specific to the client that reads it.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#audio_uri GoogleDialogflowCxFlow#audio_uri}
        '''
        result = self._values.get("audio_uri")
        assert result is not None, "Required property 'audio_uri' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentMessagesPlayAudio(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentMessagesPlayAudioOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDialogflowCxFlow.GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentMessagesPlayAudioOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3a483a732de5575059a233ab4f6920fe0f386645f8bec5f6bc63fbe4acb1d906)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fa0927078debc3b96967bfa03c5c7539be570a83dbfb750c7da6236443e463e9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "audioUri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentMessagesPlayAudio]:
        return typing.cast(typing.Optional[GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentMessagesPlayAudio], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentMessagesPlayAudio],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d6289eb7105b81d8760d5dd0d26886fd62337e54ba45ecb6093ad88f4a06f3b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDialogflowCxFlow.GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentMessagesTelephonyTransferCall",
    jsii_struct_bases=[],
    name_mapping={"phone_number": "phoneNumber"},
)
class GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentMessagesTelephonyTransferCall:
    def __init__(self, *, phone_number: builtins.str) -> None:
        '''
        :param phone_number: Transfer the call to a phone number in E.164 format. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#phone_number GoogleDialogflowCxFlow#phone_number}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8bbc41d76fcf87daa6a09e2c97c12703d1ee20353a5e7ca16f1665fd3e5c416c)
            check_type(argname="argument phone_number", value=phone_number, expected_type=type_hints["phone_number"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "phone_number": phone_number,
        }

    @builtins.property
    def phone_number(self) -> builtins.str:
        '''Transfer the call to a phone number in E.164 format.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#phone_number GoogleDialogflowCxFlow#phone_number}
        '''
        result = self._values.get("phone_number")
        assert result is not None, "Required property 'phone_number' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentMessagesTelephonyTransferCall(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentMessagesTelephonyTransferCallOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDialogflowCxFlow.GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentMessagesTelephonyTransferCallOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5078bbe09e8c82bd96e6308fd6a47231e5d855263bfb324cdad9fb20e20300ca)
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
            type_hints = typing.get_type_hints(_typecheckingstub__807cf14d47bc48d30fd9671aeeaad39f218913168ae132cd540f3d7f7109f872)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "phoneNumber", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentMessagesTelephonyTransferCall]:
        return typing.cast(typing.Optional[GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentMessagesTelephonyTransferCall], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentMessagesTelephonyTransferCall],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__445e3519bede696544170ecc1ce808775dd347f18951d34a26c97f0983c1fce7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDialogflowCxFlow.GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentMessagesText",
    jsii_struct_bases=[],
    name_mapping={"text": "text"},
)
class GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentMessagesText:
    def __init__(
        self,
        *,
        text: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param text: A collection of text response variants. If multiple variants are defined, only one text response variant is returned at runtime. required: true Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#text GoogleDialogflowCxFlow#text}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__67da1257b0a85f5de0c2bcbc322d969004509dafa920ffa3f7189182c6d1a041)
            check_type(argname="argument text", value=text, expected_type=type_hints["text"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if text is not None:
            self._values["text"] = text

    @builtins.property
    def text(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A collection of text response variants.

        If multiple variants are defined, only one text response variant is returned at runtime.
        required: true

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#text GoogleDialogflowCxFlow#text}
        '''
        result = self._values.get("text")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentMessagesText(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentMessagesTextOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDialogflowCxFlow.GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentMessagesTextOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6d754b09cc0511620e725d816fe27749924ba15bb59be2dcdcf33a199c53bd93)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e6fa5bf7fe80813977789f63a9ad51649be683435fff88f0a124377b002c70e6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "text", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentMessagesText]:
        return typing.cast(typing.Optional[GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentMessagesText], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentMessagesText],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a8a643ad1f283713a3ff9a4079c97fd14fd01f06c0e041adef9be9f82973c99a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDialogflowCxFlow.GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4757f40b0c6e0bc6864e9145ca411844af18da5ec61b4fa61eb55df9b992a5b3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAdvancedSettings")
    def put_advanced_settings(
        self,
        *,
        dtmf_settings: typing.Optional[typing.Union[GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentAdvancedSettingsDtmfSettings, typing.Dict[builtins.str, typing.Any]]] = None,
        logging_settings: typing.Optional[typing.Union[GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentAdvancedSettingsLoggingSettings, typing.Dict[builtins.str, typing.Any]]] = None,
        speech_settings: typing.Optional[typing.Union[GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentAdvancedSettingsSpeechSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param dtmf_settings: dtmf_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#dtmf_settings GoogleDialogflowCxFlow#dtmf_settings}
        :param logging_settings: logging_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#logging_settings GoogleDialogflowCxFlow#logging_settings}
        :param speech_settings: speech_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#speech_settings GoogleDialogflowCxFlow#speech_settings}
        '''
        value = GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentAdvancedSettings(
            dtmf_settings=dtmf_settings,
            logging_settings=logging_settings,
            speech_settings=speech_settings,
        )

        return typing.cast(None, jsii.invoke(self, "putAdvancedSettings", [value]))

    @jsii.member(jsii_name="putConditionalCases")
    def put_conditional_cases(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentConditionalCases, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8897a02c9d16749273ff1874fd575c50f639196949fd2c11da2862aab0a15527)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putConditionalCases", [value]))

    @jsii.member(jsii_name="putMessages")
    def put_messages(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentMessages, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5551c7c953a8f481f1ed6b54571d3fa8e7b750942674ace2b1f5207b6544810d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putMessages", [value]))

    @jsii.member(jsii_name="putSetParameterActions")
    def put_set_parameter_actions(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentSetParameterActions", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__61dab2c4af5f47879214e7134bfa2b3f086975b78078b9cc187ccda41efbc97c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putSetParameterActions", [value]))

    @jsii.member(jsii_name="resetAdvancedSettings")
    def reset_advanced_settings(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAdvancedSettings", []))

    @jsii.member(jsii_name="resetConditionalCases")
    def reset_conditional_cases(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConditionalCases", []))

    @jsii.member(jsii_name="resetEnableGenerativeFallback")
    def reset_enable_generative_fallback(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnableGenerativeFallback", []))

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
    @jsii.member(jsii_name="advancedSettings")
    def advanced_settings(
        self,
    ) -> GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentAdvancedSettingsOutputReference:
        return typing.cast(GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentAdvancedSettingsOutputReference, jsii.get(self, "advancedSettings"))

    @builtins.property
    @jsii.member(jsii_name="conditionalCases")
    def conditional_cases(
        self,
    ) -> GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentConditionalCasesList:
        return typing.cast(GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentConditionalCasesList, jsii.get(self, "conditionalCases"))

    @builtins.property
    @jsii.member(jsii_name="messages")
    def messages(
        self,
    ) -> GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentMessagesList:
        return typing.cast(GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentMessagesList, jsii.get(self, "messages"))

    @builtins.property
    @jsii.member(jsii_name="setParameterActions")
    def set_parameter_actions(
        self,
    ) -> "GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentSetParameterActionsList":
        return typing.cast("GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentSetParameterActionsList", jsii.get(self, "setParameterActions"))

    @builtins.property
    @jsii.member(jsii_name="advancedSettingsInput")
    def advanced_settings_input(
        self,
    ) -> typing.Optional[GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentAdvancedSettings]:
        return typing.cast(typing.Optional[GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentAdvancedSettings], jsii.get(self, "advancedSettingsInput"))

    @builtins.property
    @jsii.member(jsii_name="conditionalCasesInput")
    def conditional_cases_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentConditionalCases]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentConditionalCases]]], jsii.get(self, "conditionalCasesInput"))

    @builtins.property
    @jsii.member(jsii_name="enableGenerativeFallbackInput")
    def enable_generative_fallback_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enableGenerativeFallbackInput"))

    @builtins.property
    @jsii.member(jsii_name="messagesInput")
    def messages_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentMessages]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentMessages]]], jsii.get(self, "messagesInput"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentSetParameterActions"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentSetParameterActions"]]], jsii.get(self, "setParameterActionsInput"))

    @builtins.property
    @jsii.member(jsii_name="tagInput")
    def tag_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tagInput"))

    @builtins.property
    @jsii.member(jsii_name="webhookInput")
    def webhook_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "webhookInput"))

    @builtins.property
    @jsii.member(jsii_name="enableGenerativeFallback")
    def enable_generative_fallback(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enableGenerativeFallback"))

    @enable_generative_fallback.setter
    def enable_generative_fallback(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf575002abb7156167529652420b91e7e8e3c0ebc2cfbc43e5aa33adc02649e8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableGenerativeFallback", value) # pyright: ignore[reportArgumentType]

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
            type_hints = typing.get_type_hints(_typecheckingstub__54e070c194a5b9109dc7f906ad50aaa526881a46336dc04c65388679748faee3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "returnPartialResponses", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tag")
    def tag(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tag"))

    @tag.setter
    def tag(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d875b0bd1a3b574cf2c6458f527ea3a1b1f1509a0c020c29acde249a4978dce)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tag", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="webhook")
    def webhook(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "webhook"))

    @webhook.setter
    def webhook(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__31f8105c09537721a3d4acaf735e24ded8278b724bce1692282c3b6ab5b19837)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "webhook", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillment]:
        return typing.cast(typing.Optional[GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillment], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillment],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f6d583767b4acd854c392ffcddbfb23215ebb70520283915d7715a4f129cbb6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDialogflowCxFlow.GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentSetParameterActions",
    jsii_struct_bases=[],
    name_mapping={"parameter": "parameter", "value": "value"},
)
class GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentSetParameterActions:
    def __init__(
        self,
        *,
        parameter: typing.Optional[builtins.str] = None,
        value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param parameter: Display name of the parameter. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#parameter GoogleDialogflowCxFlow#parameter}
        :param value: The new JSON-encoded value of the parameter. A null value clears the parameter. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#value GoogleDialogflowCxFlow#value}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__859c00631fe9a87037b70ec7d706d9d78447ca0fac0a2f207e9eff1f2bed5e25)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#parameter GoogleDialogflowCxFlow#parameter}
        '''
        result = self._values.get("parameter")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def value(self) -> typing.Optional[builtins.str]:
        '''The new JSON-encoded value of the parameter. A null value clears the parameter.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#value GoogleDialogflowCxFlow#value}
        '''
        result = self._values.get("value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentSetParameterActions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentSetParameterActionsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDialogflowCxFlow.GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentSetParameterActionsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4f59a07715588bb2e498c8aa0643276f7eb1d92666189d689d08d4f1afefc71a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentSetParameterActionsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f0c6a402d87f40831c9f8a9542818c46c70997c7ffc861043504ad7b48acef1)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentSetParameterActionsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__19b92920d6e285342c2b6f78e4b89d3d58e87c7277ac61fd5a893a377c3192b4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ed018cdab6df3b0898ae8140bacdb07eaf5a4bcfea9db7f4603867f79ea2892f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d1e7241fafd91d0e7640411347a40d725b4dcdbe78c36526de13493eb69d2227)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentSetParameterActions]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentSetParameterActions]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentSetParameterActions]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9079a67fbba5727e636d66a246e9de3cb13047e8c15ab6254175a9177d7ec52f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentSetParameterActionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDialogflowCxFlow.GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentSetParameterActionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__52328e0613721df57d04da8c8713cd55194da0bae846e83dc193b4ca5ee53d93)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7dfa57edfa310ee4134e55445d3b44ea0a718df196f2fa01ef45e1877f3c0df8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "parameter", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a01a79cd86a4df215ea1730c7ff0ced8bbeb6131b1ce0e7b74c92d7a0e1659f8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentSetParameterActions]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentSetParameterActions]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentSetParameterActions]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8cb486d001ee2b1c1c6fcb871e9deac8226eb6892e7e68d7b8e8dad01f6ab66b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDialogflowCxFlow.GoogleDialogflowCxFlowNluSettings",
    jsii_struct_bases=[],
    name_mapping={
        "classification_threshold": "classificationThreshold",
        "model_training_mode": "modelTrainingMode",
        "model_type": "modelType",
    },
)
class GoogleDialogflowCxFlowNluSettings:
    def __init__(
        self,
        *,
        classification_threshold: typing.Optional[jsii.Number] = None,
        model_training_mode: typing.Optional[builtins.str] = None,
        model_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param classification_threshold: To filter out false positive results and still get variety in matched natural language inputs for your agent, you can tune the machine learning classification threshold. If the returned score value is less than the threshold value, then a no-match event will be triggered. The score values range from 0.0 (completely uncertain) to 1.0 (completely certain). If set to 0.0, the default of 0.3 is used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#classification_threshold GoogleDialogflowCxFlow#classification_threshold}
        :param model_training_mode: Indicates NLU model training mode. - MODEL_TRAINING_MODE_AUTOMATIC: NLU model training is automatically triggered when a flow gets modified. User can also manually trigger model training in this mode. - MODEL_TRAINING_MODE_MANUAL: User needs to manually trigger NLU model training. Best for large flows whose models take long time to train. Possible values: ["MODEL_TRAINING_MODE_AUTOMATIC", "MODEL_TRAINING_MODE_MANUAL"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#model_training_mode GoogleDialogflowCxFlow#model_training_mode}
        :param model_type: Indicates the type of NLU model. - MODEL_TYPE_STANDARD: Use standard NLU model. - MODEL_TYPE_ADVANCED: Use advanced NLU model. Possible values: ["MODEL_TYPE_STANDARD", "MODEL_TYPE_ADVANCED"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#model_type GoogleDialogflowCxFlow#model_type}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e11d2415d17184287951f07c3c59b5989b582c6777731b857475cbefa2994ab9)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#classification_threshold GoogleDialogflowCxFlow#classification_threshold}
        '''
        result = self._values.get("classification_threshold")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def model_training_mode(self) -> typing.Optional[builtins.str]:
        '''Indicates NLU model training mode.

        - MODEL_TRAINING_MODE_AUTOMATIC: NLU model training is automatically triggered when a flow gets modified. User can also manually trigger model training in this mode.
        - MODEL_TRAINING_MODE_MANUAL: User needs to manually trigger NLU model training. Best for large flows whose models take long time to train. Possible values: ["MODEL_TRAINING_MODE_AUTOMATIC", "MODEL_TRAINING_MODE_MANUAL"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#model_training_mode GoogleDialogflowCxFlow#model_training_mode}
        '''
        result = self._values.get("model_training_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def model_type(self) -> typing.Optional[builtins.str]:
        '''Indicates the type of NLU model.

        - MODEL_TYPE_STANDARD: Use standard NLU model.
        - MODEL_TYPE_ADVANCED: Use advanced NLU model. Possible values: ["MODEL_TYPE_STANDARD", "MODEL_TYPE_ADVANCED"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#model_type GoogleDialogflowCxFlow#model_type}
        '''
        result = self._values.get("model_type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDialogflowCxFlowNluSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDialogflowCxFlowNluSettingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDialogflowCxFlow.GoogleDialogflowCxFlowNluSettingsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__98d9f3909bba7513ded942dd49ab4eff31602cdb034f4a4e1475a92d9195e3cd)
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
            type_hints = typing.get_type_hints(_typecheckingstub__45305366a1d242576564cf317b03d1a334294e16921345b493918e93aecceff7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "classificationThreshold", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="modelTrainingMode")
    def model_training_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "modelTrainingMode"))

    @model_training_mode.setter
    def model_training_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__536cbd1264bd06bfdfe3cee75d9622418afef8311158512d4f56b6ab9158e3f8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "modelTrainingMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="modelType")
    def model_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "modelType"))

    @model_type.setter
    def model_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dbe96da0683e88b188041d7de4c92fed18d30c2e19f30792d01ac81a7e8fc06f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "modelType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GoogleDialogflowCxFlowNluSettings]:
        return typing.cast(typing.Optional[GoogleDialogflowCxFlowNluSettings], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDialogflowCxFlowNluSettings],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__524f25a80f58940c6773cd38d1d4a7c6ddb98c11023b57dd08686d71d4bec644)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDialogflowCxFlow.GoogleDialogflowCxFlowTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class GoogleDialogflowCxFlowTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#create GoogleDialogflowCxFlow#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#delete GoogleDialogflowCxFlow#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#update GoogleDialogflowCxFlow#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0210a03cea17a8ef6bb6c8d12573cd1b0d7140688721c228c725071420680dd6)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#create GoogleDialogflowCxFlow#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#delete GoogleDialogflowCxFlow#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#update GoogleDialogflowCxFlow#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDialogflowCxFlowTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDialogflowCxFlowTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDialogflowCxFlow.GoogleDialogflowCxFlowTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a0e68db04b76164173d2591ddd75bb1b9b052a340e3f358976041e891232cfc2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6c8fa4d3bd2d4d417cd91617f1a451745bf4aaf04d58d7966be4fba2c6597fe3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d5975630e9faa60ef9b199ec40a0b2873f5df8a921e7f852dabdc8a78073309)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e778f648906def1b0b98d5164ec361e201a715e15a0d72467b7788a670fc5c4d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDialogflowCxFlowTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDialogflowCxFlowTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDialogflowCxFlowTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__86c6d5b814a990c8b13a0674f1e520f123196a9fc67d10ff966cfed6d664ab5a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDialogflowCxFlow.GoogleDialogflowCxFlowTransitionRoutes",
    jsii_struct_bases=[],
    name_mapping={
        "condition": "condition",
        "intent": "intent",
        "target_flow": "targetFlow",
        "target_page": "targetPage",
        "trigger_fulfillment": "triggerFulfillment",
    },
)
class GoogleDialogflowCxFlowTransitionRoutes:
    def __init__(
        self,
        *,
        condition: typing.Optional[builtins.str] = None,
        intent: typing.Optional[builtins.str] = None,
        target_flow: typing.Optional[builtins.str] = None,
        target_page: typing.Optional[builtins.str] = None,
        trigger_fulfillment: typing.Optional[typing.Union["GoogleDialogflowCxFlowTransitionRoutesTriggerFulfillment", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param condition: The condition to evaluate against form parameters or session parameters. At least one of intent or condition must be specified. When both intent and condition are specified, the transition can only happen when both are fulfilled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#condition GoogleDialogflowCxFlow#condition}
        :param intent: The unique identifier of an Intent. Format: projects//locations//agents//intents/. Indicates that the transition can only happen when the given intent is matched. At least one of intent or condition must be specified. When both intent and condition are specified, the transition can only happen when both are fulfilled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#intent GoogleDialogflowCxFlow#intent}
        :param target_flow: The target flow to transition to. Format: projects//locations//agents//flows/. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#target_flow GoogleDialogflowCxFlow#target_flow}
        :param target_page: The target page to transition to. Format: projects//locations//agents//flows//pages/. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#target_page GoogleDialogflowCxFlow#target_page}
        :param trigger_fulfillment: trigger_fulfillment block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#trigger_fulfillment GoogleDialogflowCxFlow#trigger_fulfillment}
        '''
        if isinstance(trigger_fulfillment, dict):
            trigger_fulfillment = GoogleDialogflowCxFlowTransitionRoutesTriggerFulfillment(**trigger_fulfillment)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7d1a18960d79eb590c9d5bf3e090bd2e010515560266b7c63ff53264e0f013b1)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#condition GoogleDialogflowCxFlow#condition}
        '''
        result = self._values.get("condition")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def intent(self) -> typing.Optional[builtins.str]:
        '''The unique identifier of an Intent.

        Format: projects//locations//agents//intents/. Indicates that the transition can only happen when the given intent is matched. At least one of intent or condition must be specified. When both intent and condition are specified, the transition can only happen when both are fulfilled.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#intent GoogleDialogflowCxFlow#intent}
        '''
        result = self._values.get("intent")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def target_flow(self) -> typing.Optional[builtins.str]:
        '''The target flow to transition to. Format: projects//locations//agents//flows/.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#target_flow GoogleDialogflowCxFlow#target_flow}
        '''
        result = self._values.get("target_flow")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def target_page(self) -> typing.Optional[builtins.str]:
        '''The target page to transition to. Format: projects//locations//agents//flows//pages/.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#target_page GoogleDialogflowCxFlow#target_page}
        '''
        result = self._values.get("target_page")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def trigger_fulfillment(
        self,
    ) -> typing.Optional["GoogleDialogflowCxFlowTransitionRoutesTriggerFulfillment"]:
        '''trigger_fulfillment block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#trigger_fulfillment GoogleDialogflowCxFlow#trigger_fulfillment}
        '''
        result = self._values.get("trigger_fulfillment")
        return typing.cast(typing.Optional["GoogleDialogflowCxFlowTransitionRoutesTriggerFulfillment"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDialogflowCxFlowTransitionRoutes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDialogflowCxFlowTransitionRoutesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDialogflowCxFlow.GoogleDialogflowCxFlowTransitionRoutesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c658a26b791ed47c005526f0d203bf77af0ce5f404c11ebc43fd87ecac58b40b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleDialogflowCxFlowTransitionRoutesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c3785a2a26b46925c4961926dbf735621325bd370269361e64e4cae714adf64c)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleDialogflowCxFlowTransitionRoutesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__72390c857e2ae72ecbbe1a54bb412b4ff281d146112ca0926eef1c03e9ab9c40)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bef78f412e276f63bb4c9db73a3c134a65b4d12146688888d6a4695ad3ac274b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__be10637d5d8fa7172423bd8f96a2561a939265c1e9b1d560cbb735def4faa7a2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDialogflowCxFlowTransitionRoutes]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDialogflowCxFlowTransitionRoutes]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDialogflowCxFlowTransitionRoutes]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e4831c1a17de10c1ab5840826b85ccb8471666de0b3bafe39b6002b027cc2f31)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleDialogflowCxFlowTransitionRoutesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDialogflowCxFlow.GoogleDialogflowCxFlowTransitionRoutesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__48ac555298c8903d2371e18de384242e6abe071a26c75bfecc87cdb684fc1f5b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putTriggerFulfillment")
    def put_trigger_fulfillment(
        self,
        *,
        conditional_cases: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleDialogflowCxFlowTransitionRoutesTriggerFulfillmentConditionalCases", typing.Dict[builtins.str, typing.Any]]]]] = None,
        messages: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleDialogflowCxFlowTransitionRoutesTriggerFulfillmentMessages", typing.Dict[builtins.str, typing.Any]]]]] = None,
        return_partial_responses: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        set_parameter_actions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleDialogflowCxFlowTransitionRoutesTriggerFulfillmentSetParameterActions", typing.Dict[builtins.str, typing.Any]]]]] = None,
        tag: typing.Optional[builtins.str] = None,
        webhook: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param conditional_cases: conditional_cases block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#conditional_cases GoogleDialogflowCxFlow#conditional_cases}
        :param messages: messages block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#messages GoogleDialogflowCxFlow#messages}
        :param return_partial_responses: Whether Dialogflow should return currently queued fulfillment response messages in streaming APIs. If a webhook is specified, it happens before Dialogflow invokes webhook. Warning: 1) This flag only affects streaming API. Responses are still queued and returned once in non-streaming API. 2) The flag can be enabled in any fulfillment but only the first 3 partial responses will be returned. You may only want to apply it to fulfillments that have slow webhooks. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#return_partial_responses GoogleDialogflowCxFlow#return_partial_responses}
        :param set_parameter_actions: set_parameter_actions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#set_parameter_actions GoogleDialogflowCxFlow#set_parameter_actions}
        :param tag: The tag used by the webhook to identify which fulfillment is being called. This field is required if webhook is specified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#tag GoogleDialogflowCxFlow#tag}
        :param webhook: The webhook to call. Format: projects//locations//agents//webhooks/. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#webhook GoogleDialogflowCxFlow#webhook}
        '''
        value = GoogleDialogflowCxFlowTransitionRoutesTriggerFulfillment(
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
    ) -> "GoogleDialogflowCxFlowTransitionRoutesTriggerFulfillmentOutputReference":
        return typing.cast("GoogleDialogflowCxFlowTransitionRoutesTriggerFulfillmentOutputReference", jsii.get(self, "triggerFulfillment"))

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
    ) -> typing.Optional["GoogleDialogflowCxFlowTransitionRoutesTriggerFulfillment"]:
        return typing.cast(typing.Optional["GoogleDialogflowCxFlowTransitionRoutesTriggerFulfillment"], jsii.get(self, "triggerFulfillmentInput"))

    @builtins.property
    @jsii.member(jsii_name="condition")
    def condition(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "condition"))

    @condition.setter
    def condition(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__76e46873b24a3efeb8ec6f6a61f81217f1e21900852c2da220810827b27be97d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "condition", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="intent")
    def intent(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "intent"))

    @intent.setter
    def intent(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a7bbd5463bb362fe073852100eb5bc655db95f2128105531a3af0073f278523b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "intent", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="targetFlow")
    def target_flow(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "targetFlow"))

    @target_flow.setter
    def target_flow(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__76d249e51248c27f926d6d592e9b4877379d8f9d5c09d9cc691e3dc24dab1974)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "targetFlow", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="targetPage")
    def target_page(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "targetPage"))

    @target_page.setter
    def target_page(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1ec782606f320f8dceb8e53942677095abfe92dc2acf5f176bf57abeb0a5f8ad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "targetPage", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDialogflowCxFlowTransitionRoutes]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDialogflowCxFlowTransitionRoutes]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDialogflowCxFlowTransitionRoutes]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c71428de0494ae2981349f4c2a95e9ba77bf5b1e6a1b3ec8c23594a99918944a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDialogflowCxFlow.GoogleDialogflowCxFlowTransitionRoutesTriggerFulfillment",
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
class GoogleDialogflowCxFlowTransitionRoutesTriggerFulfillment:
    def __init__(
        self,
        *,
        conditional_cases: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleDialogflowCxFlowTransitionRoutesTriggerFulfillmentConditionalCases", typing.Dict[builtins.str, typing.Any]]]]] = None,
        messages: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleDialogflowCxFlowTransitionRoutesTriggerFulfillmentMessages", typing.Dict[builtins.str, typing.Any]]]]] = None,
        return_partial_responses: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        set_parameter_actions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleDialogflowCxFlowTransitionRoutesTriggerFulfillmentSetParameterActions", typing.Dict[builtins.str, typing.Any]]]]] = None,
        tag: typing.Optional[builtins.str] = None,
        webhook: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param conditional_cases: conditional_cases block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#conditional_cases GoogleDialogflowCxFlow#conditional_cases}
        :param messages: messages block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#messages GoogleDialogflowCxFlow#messages}
        :param return_partial_responses: Whether Dialogflow should return currently queued fulfillment response messages in streaming APIs. If a webhook is specified, it happens before Dialogflow invokes webhook. Warning: 1) This flag only affects streaming API. Responses are still queued and returned once in non-streaming API. 2) The flag can be enabled in any fulfillment but only the first 3 partial responses will be returned. You may only want to apply it to fulfillments that have slow webhooks. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#return_partial_responses GoogleDialogflowCxFlow#return_partial_responses}
        :param set_parameter_actions: set_parameter_actions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#set_parameter_actions GoogleDialogflowCxFlow#set_parameter_actions}
        :param tag: The tag used by the webhook to identify which fulfillment is being called. This field is required if webhook is specified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#tag GoogleDialogflowCxFlow#tag}
        :param webhook: The webhook to call. Format: projects//locations//agents//webhooks/. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#webhook GoogleDialogflowCxFlow#webhook}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__944315f63373bd1968029dfa9b00946a674228d84fcc82289742d14c69a9a569)
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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleDialogflowCxFlowTransitionRoutesTriggerFulfillmentConditionalCases"]]]:
        '''conditional_cases block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#conditional_cases GoogleDialogflowCxFlow#conditional_cases}
        '''
        result = self._values.get("conditional_cases")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleDialogflowCxFlowTransitionRoutesTriggerFulfillmentConditionalCases"]]], result)

    @builtins.property
    def messages(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleDialogflowCxFlowTransitionRoutesTriggerFulfillmentMessages"]]]:
        '''messages block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#messages GoogleDialogflowCxFlow#messages}
        '''
        result = self._values.get("messages")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleDialogflowCxFlowTransitionRoutesTriggerFulfillmentMessages"]]], result)

    @builtins.property
    def return_partial_responses(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether Dialogflow should return currently queued fulfillment response messages in streaming APIs.

        If a webhook is specified, it happens before Dialogflow invokes webhook. Warning: 1) This flag only affects streaming API. Responses are still queued and returned once in non-streaming API. 2) The flag can be enabled in any fulfillment but only the first 3 partial responses will be returned. You may only want to apply it to fulfillments that have slow webhooks.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#return_partial_responses GoogleDialogflowCxFlow#return_partial_responses}
        '''
        result = self._values.get("return_partial_responses")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def set_parameter_actions(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleDialogflowCxFlowTransitionRoutesTriggerFulfillmentSetParameterActions"]]]:
        '''set_parameter_actions block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#set_parameter_actions GoogleDialogflowCxFlow#set_parameter_actions}
        '''
        result = self._values.get("set_parameter_actions")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleDialogflowCxFlowTransitionRoutesTriggerFulfillmentSetParameterActions"]]], result)

    @builtins.property
    def tag(self) -> typing.Optional[builtins.str]:
        '''The tag used by the webhook to identify which fulfillment is being called.

        This field is required if webhook is specified.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#tag GoogleDialogflowCxFlow#tag}
        '''
        result = self._values.get("tag")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def webhook(self) -> typing.Optional[builtins.str]:
        '''The webhook to call. Format: projects//locations//agents//webhooks/.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#webhook GoogleDialogflowCxFlow#webhook}
        '''
        result = self._values.get("webhook")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDialogflowCxFlowTransitionRoutesTriggerFulfillment(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDialogflowCxFlow.GoogleDialogflowCxFlowTransitionRoutesTriggerFulfillmentConditionalCases",
    jsii_struct_bases=[],
    name_mapping={"cases": "cases"},
)
class GoogleDialogflowCxFlowTransitionRoutesTriggerFulfillmentConditionalCases:
    def __init__(self, *, cases: typing.Optional[builtins.str] = None) -> None:
        '''
        :param cases: A JSON encoded list of cascading if-else conditions. Cases are mutually exclusive. The first one with a matching condition is selected, all the rest ignored. See `Case <https://cloud.google.com/dialogflow/cx/docs/reference/rest/v3/Fulfillment#case>`_ for the schema. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#cases GoogleDialogflowCxFlow#cases}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__073564628f5e4b1c595d0ca2ef50b8c8b21b6fcd3d9829ed222747ee2033d788)
            check_type(argname="argument cases", value=cases, expected_type=type_hints["cases"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if cases is not None:
            self._values["cases"] = cases

    @builtins.property
    def cases(self) -> typing.Optional[builtins.str]:
        '''A JSON encoded list of cascading if-else conditions.

        Cases are mutually exclusive. The first one with a matching condition is selected, all the rest ignored.
        See `Case <https://cloud.google.com/dialogflow/cx/docs/reference/rest/v3/Fulfillment#case>`_ for the schema.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#cases GoogleDialogflowCxFlow#cases}
        '''
        result = self._values.get("cases")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDialogflowCxFlowTransitionRoutesTriggerFulfillmentConditionalCases(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDialogflowCxFlowTransitionRoutesTriggerFulfillmentConditionalCasesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDialogflowCxFlow.GoogleDialogflowCxFlowTransitionRoutesTriggerFulfillmentConditionalCasesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__dccd900a9d9cd7c15f9a0c287a2f99de34596f9a2f5812f158211134371b883f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleDialogflowCxFlowTransitionRoutesTriggerFulfillmentConditionalCasesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d64b4fa477655ece9114be172123489468135e33629d889949ef5b326669db33)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleDialogflowCxFlowTransitionRoutesTriggerFulfillmentConditionalCasesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__11e9aac43e2eaf7698d6c27ae81848e22e314ec08d9dc72e608142031ca45f04)
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
            type_hints = typing.get_type_hints(_typecheckingstub__dc763207d105bcd2b733520647fced1e0d09ea742305106dcf6f6d380450b38a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ce5f923d4c327212d62c992838d955b10993908e731036936ae74e3e27b5d7ca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDialogflowCxFlowTransitionRoutesTriggerFulfillmentConditionalCases]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDialogflowCxFlowTransitionRoutesTriggerFulfillmentConditionalCases]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDialogflowCxFlowTransitionRoutesTriggerFulfillmentConditionalCases]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b94ce98d4da9e0fb393f8633e49995caf36570b625f581b6bc2c1c719a1e6000)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleDialogflowCxFlowTransitionRoutesTriggerFulfillmentConditionalCasesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDialogflowCxFlow.GoogleDialogflowCxFlowTransitionRoutesTriggerFulfillmentConditionalCasesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__84305fb27b217397ad3c42dba23ed2b0f210bab4cbe3d6933666a8a28542afa3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f43465b9e291c5c5b7730cac16168be734ee87b24422e2c0956f46ae12735ef6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cases", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDialogflowCxFlowTransitionRoutesTriggerFulfillmentConditionalCases]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDialogflowCxFlowTransitionRoutesTriggerFulfillmentConditionalCases]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDialogflowCxFlowTransitionRoutesTriggerFulfillmentConditionalCases]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__69319f6b9393fa10bdaed0904605aae7b5596401b7f85dbab7ab898f27bedee3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDialogflowCxFlow.GoogleDialogflowCxFlowTransitionRoutesTriggerFulfillmentMessages",
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
class GoogleDialogflowCxFlowTransitionRoutesTriggerFulfillmentMessages:
    def __init__(
        self,
        *,
        channel: typing.Optional[builtins.str] = None,
        conversation_success: typing.Optional[typing.Union["GoogleDialogflowCxFlowTransitionRoutesTriggerFulfillmentMessagesConversationSuccess", typing.Dict[builtins.str, typing.Any]]] = None,
        live_agent_handoff: typing.Optional[typing.Union["GoogleDialogflowCxFlowTransitionRoutesTriggerFulfillmentMessagesLiveAgentHandoff", typing.Dict[builtins.str, typing.Any]]] = None,
        output_audio_text: typing.Optional[typing.Union["GoogleDialogflowCxFlowTransitionRoutesTriggerFulfillmentMessagesOutputAudioText", typing.Dict[builtins.str, typing.Any]]] = None,
        payload: typing.Optional[builtins.str] = None,
        play_audio: typing.Optional[typing.Union["GoogleDialogflowCxFlowTransitionRoutesTriggerFulfillmentMessagesPlayAudio", typing.Dict[builtins.str, typing.Any]]] = None,
        telephony_transfer_call: typing.Optional[typing.Union["GoogleDialogflowCxFlowTransitionRoutesTriggerFulfillmentMessagesTelephonyTransferCall", typing.Dict[builtins.str, typing.Any]]] = None,
        text: typing.Optional[typing.Union["GoogleDialogflowCxFlowTransitionRoutesTriggerFulfillmentMessagesText", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param channel: The channel which the response is associated with. Clients can specify the channel via QueryParameters.channel, and only associated channel response will be returned. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#channel GoogleDialogflowCxFlow#channel}
        :param conversation_success: conversation_success block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#conversation_success GoogleDialogflowCxFlow#conversation_success}
        :param live_agent_handoff: live_agent_handoff block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#live_agent_handoff GoogleDialogflowCxFlow#live_agent_handoff}
        :param output_audio_text: output_audio_text block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#output_audio_text GoogleDialogflowCxFlow#output_audio_text}
        :param payload: A custom, platform-specific payload. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#payload GoogleDialogflowCxFlow#payload}
        :param play_audio: play_audio block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#play_audio GoogleDialogflowCxFlow#play_audio}
        :param telephony_transfer_call: telephony_transfer_call block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#telephony_transfer_call GoogleDialogflowCxFlow#telephony_transfer_call}
        :param text: text block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#text GoogleDialogflowCxFlow#text}
        '''
        if isinstance(conversation_success, dict):
            conversation_success = GoogleDialogflowCxFlowTransitionRoutesTriggerFulfillmentMessagesConversationSuccess(**conversation_success)
        if isinstance(live_agent_handoff, dict):
            live_agent_handoff = GoogleDialogflowCxFlowTransitionRoutesTriggerFulfillmentMessagesLiveAgentHandoff(**live_agent_handoff)
        if isinstance(output_audio_text, dict):
            output_audio_text = GoogleDialogflowCxFlowTransitionRoutesTriggerFulfillmentMessagesOutputAudioText(**output_audio_text)
        if isinstance(play_audio, dict):
            play_audio = GoogleDialogflowCxFlowTransitionRoutesTriggerFulfillmentMessagesPlayAudio(**play_audio)
        if isinstance(telephony_transfer_call, dict):
            telephony_transfer_call = GoogleDialogflowCxFlowTransitionRoutesTriggerFulfillmentMessagesTelephonyTransferCall(**telephony_transfer_call)
        if isinstance(text, dict):
            text = GoogleDialogflowCxFlowTransitionRoutesTriggerFulfillmentMessagesText(**text)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__65436ee4b59d66753768513811493c2a9d9e47b34fd247b3f479f85953b0e120)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#channel GoogleDialogflowCxFlow#channel}
        '''
        result = self._values.get("channel")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def conversation_success(
        self,
    ) -> typing.Optional["GoogleDialogflowCxFlowTransitionRoutesTriggerFulfillmentMessagesConversationSuccess"]:
        '''conversation_success block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#conversation_success GoogleDialogflowCxFlow#conversation_success}
        '''
        result = self._values.get("conversation_success")
        return typing.cast(typing.Optional["GoogleDialogflowCxFlowTransitionRoutesTriggerFulfillmentMessagesConversationSuccess"], result)

    @builtins.property
    def live_agent_handoff(
        self,
    ) -> typing.Optional["GoogleDialogflowCxFlowTransitionRoutesTriggerFulfillmentMessagesLiveAgentHandoff"]:
        '''live_agent_handoff block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#live_agent_handoff GoogleDialogflowCxFlow#live_agent_handoff}
        '''
        result = self._values.get("live_agent_handoff")
        return typing.cast(typing.Optional["GoogleDialogflowCxFlowTransitionRoutesTriggerFulfillmentMessagesLiveAgentHandoff"], result)

    @builtins.property
    def output_audio_text(
        self,
    ) -> typing.Optional["GoogleDialogflowCxFlowTransitionRoutesTriggerFulfillmentMessagesOutputAudioText"]:
        '''output_audio_text block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#output_audio_text GoogleDialogflowCxFlow#output_audio_text}
        '''
        result = self._values.get("output_audio_text")
        return typing.cast(typing.Optional["GoogleDialogflowCxFlowTransitionRoutesTriggerFulfillmentMessagesOutputAudioText"], result)

    @builtins.property
    def payload(self) -> typing.Optional[builtins.str]:
        '''A custom, platform-specific payload.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#payload GoogleDialogflowCxFlow#payload}
        '''
        result = self._values.get("payload")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def play_audio(
        self,
    ) -> typing.Optional["GoogleDialogflowCxFlowTransitionRoutesTriggerFulfillmentMessagesPlayAudio"]:
        '''play_audio block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#play_audio GoogleDialogflowCxFlow#play_audio}
        '''
        result = self._values.get("play_audio")
        return typing.cast(typing.Optional["GoogleDialogflowCxFlowTransitionRoutesTriggerFulfillmentMessagesPlayAudio"], result)

    @builtins.property
    def telephony_transfer_call(
        self,
    ) -> typing.Optional["GoogleDialogflowCxFlowTransitionRoutesTriggerFulfillmentMessagesTelephonyTransferCall"]:
        '''telephony_transfer_call block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#telephony_transfer_call GoogleDialogflowCxFlow#telephony_transfer_call}
        '''
        result = self._values.get("telephony_transfer_call")
        return typing.cast(typing.Optional["GoogleDialogflowCxFlowTransitionRoutesTriggerFulfillmentMessagesTelephonyTransferCall"], result)

    @builtins.property
    def text(
        self,
    ) -> typing.Optional["GoogleDialogflowCxFlowTransitionRoutesTriggerFulfillmentMessagesText"]:
        '''text block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#text GoogleDialogflowCxFlow#text}
        '''
        result = self._values.get("text")
        return typing.cast(typing.Optional["GoogleDialogflowCxFlowTransitionRoutesTriggerFulfillmentMessagesText"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDialogflowCxFlowTransitionRoutesTriggerFulfillmentMessages(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDialogflowCxFlow.GoogleDialogflowCxFlowTransitionRoutesTriggerFulfillmentMessagesConversationSuccess",
    jsii_struct_bases=[],
    name_mapping={"metadata": "metadata"},
)
class GoogleDialogflowCxFlowTransitionRoutesTriggerFulfillmentMessagesConversationSuccess:
    def __init__(self, *, metadata: typing.Optional[builtins.str] = None) -> None:
        '''
        :param metadata: Custom metadata. Dialogflow doesn't impose any structure on this. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#metadata GoogleDialogflowCxFlow#metadata}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__443cb296068677570ca31681b7a23fce70b15134c83624ecdfa4d4d7d48c4e54)
            check_type(argname="argument metadata", value=metadata, expected_type=type_hints["metadata"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if metadata is not None:
            self._values["metadata"] = metadata

    @builtins.property
    def metadata(self) -> typing.Optional[builtins.str]:
        '''Custom metadata. Dialogflow doesn't impose any structure on this.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#metadata GoogleDialogflowCxFlow#metadata}
        '''
        result = self._values.get("metadata")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDialogflowCxFlowTransitionRoutesTriggerFulfillmentMessagesConversationSuccess(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDialogflowCxFlowTransitionRoutesTriggerFulfillmentMessagesConversationSuccessOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDialogflowCxFlow.GoogleDialogflowCxFlowTransitionRoutesTriggerFulfillmentMessagesConversationSuccessOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a62fef97b7856041a1713b9b5ae779fb408afd1be81ba4f16c1ba424089cb264)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8ada7298689527b5c065cde8e48c22db97db2e508e922c6fd36a87403bf090ce)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metadata", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDialogflowCxFlowTransitionRoutesTriggerFulfillmentMessagesConversationSuccess]:
        return typing.cast(typing.Optional[GoogleDialogflowCxFlowTransitionRoutesTriggerFulfillmentMessagesConversationSuccess], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDialogflowCxFlowTransitionRoutesTriggerFulfillmentMessagesConversationSuccess],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5103b2b839d9b966e63faeba0e1d3965459265a261e7c5f637daa589b15b432f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleDialogflowCxFlowTransitionRoutesTriggerFulfillmentMessagesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDialogflowCxFlow.GoogleDialogflowCxFlowTransitionRoutesTriggerFulfillmentMessagesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7435871870af685282002420434c13db7b6579027b6925f2e68d8de4a5c3fc9e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleDialogflowCxFlowTransitionRoutesTriggerFulfillmentMessagesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6be189241fff7bf38c1fca21ad4f28dc6cccdf2f4f554aaea715de229737a76e)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleDialogflowCxFlowTransitionRoutesTriggerFulfillmentMessagesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ae7d59f0511c56d7eb840244429c79966ee48fc81349d5f84f2319907031903)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c9a46f9994035fdfbc69bb83a7a8c239a963e6e9eecfe39d1df33a45f82ec229)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3eda6061a4d7d2bdf6484af0aac95aaeab9ba650ee6cb0480fade59673b8fade)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDialogflowCxFlowTransitionRoutesTriggerFulfillmentMessages]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDialogflowCxFlowTransitionRoutesTriggerFulfillmentMessages]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDialogflowCxFlowTransitionRoutesTriggerFulfillmentMessages]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__25a4af56b921e555a8e66e8345e3e8709927bd080ce8209d365603fa341a6b54)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDialogflowCxFlow.GoogleDialogflowCxFlowTransitionRoutesTriggerFulfillmentMessagesLiveAgentHandoff",
    jsii_struct_bases=[],
    name_mapping={"metadata": "metadata"},
)
class GoogleDialogflowCxFlowTransitionRoutesTriggerFulfillmentMessagesLiveAgentHandoff:
    def __init__(self, *, metadata: typing.Optional[builtins.str] = None) -> None:
        '''
        :param metadata: Custom metadata. Dialogflow doesn't impose any structure on this. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#metadata GoogleDialogflowCxFlow#metadata}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__037577492ee768c84baa425a81e9da4bed7eca07320eb112467dd187e32ab818)
            check_type(argname="argument metadata", value=metadata, expected_type=type_hints["metadata"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if metadata is not None:
            self._values["metadata"] = metadata

    @builtins.property
    def metadata(self) -> typing.Optional[builtins.str]:
        '''Custom metadata. Dialogflow doesn't impose any structure on this.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#metadata GoogleDialogflowCxFlow#metadata}
        '''
        result = self._values.get("metadata")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDialogflowCxFlowTransitionRoutesTriggerFulfillmentMessagesLiveAgentHandoff(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDialogflowCxFlowTransitionRoutesTriggerFulfillmentMessagesLiveAgentHandoffOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDialogflowCxFlow.GoogleDialogflowCxFlowTransitionRoutesTriggerFulfillmentMessagesLiveAgentHandoffOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__29c23b527aedf7f56b05ebd207e8bf44b96dead12716c5f2ad05f70660f45f63)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b3ec186ffc12bc91a22be609e0440c45a7148cd2adf3d8455c03443084b991c9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metadata", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDialogflowCxFlowTransitionRoutesTriggerFulfillmentMessagesLiveAgentHandoff]:
        return typing.cast(typing.Optional[GoogleDialogflowCxFlowTransitionRoutesTriggerFulfillmentMessagesLiveAgentHandoff], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDialogflowCxFlowTransitionRoutesTriggerFulfillmentMessagesLiveAgentHandoff],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0b99adafea9b3ca2b24c5226c7aed674a5a7acb0b2cf866a9968359adc9b2328)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDialogflowCxFlow.GoogleDialogflowCxFlowTransitionRoutesTriggerFulfillmentMessagesOutputAudioText",
    jsii_struct_bases=[],
    name_mapping={"ssml": "ssml", "text": "text"},
)
class GoogleDialogflowCxFlowTransitionRoutesTriggerFulfillmentMessagesOutputAudioText:
    def __init__(
        self,
        *,
        ssml: typing.Optional[builtins.str] = None,
        text: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param ssml: The SSML text to be synthesized. For more information, see SSML. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#ssml GoogleDialogflowCxFlow#ssml}
        :param text: The raw text to be synthesized. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#text GoogleDialogflowCxFlow#text}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__754cf0eb58c8b5554cec150e39db7d963e7b5a5ccab6c9ea5619b02e0953ac39)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#ssml GoogleDialogflowCxFlow#ssml}
        '''
        result = self._values.get("ssml")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def text(self) -> typing.Optional[builtins.str]:
        '''The raw text to be synthesized.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#text GoogleDialogflowCxFlow#text}
        '''
        result = self._values.get("text")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDialogflowCxFlowTransitionRoutesTriggerFulfillmentMessagesOutputAudioText(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDialogflowCxFlowTransitionRoutesTriggerFulfillmentMessagesOutputAudioTextOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDialogflowCxFlow.GoogleDialogflowCxFlowTransitionRoutesTriggerFulfillmentMessagesOutputAudioTextOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4f98db449db3742aa31405a7fb2f355780ca03773173b8e1e5094869b9a3e7fb)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3de77f51bd45be075e048dd6cd7856fca94294384103b6e481857cee90bce522)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ssml", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="text")
    def text(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "text"))

    @text.setter
    def text(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b51f673294b2e4d47f56a817c0f960b1ecaef6d00f7708f6309d8e6488be465)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "text", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDialogflowCxFlowTransitionRoutesTriggerFulfillmentMessagesOutputAudioText]:
        return typing.cast(typing.Optional[GoogleDialogflowCxFlowTransitionRoutesTriggerFulfillmentMessagesOutputAudioText], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDialogflowCxFlowTransitionRoutesTriggerFulfillmentMessagesOutputAudioText],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b36fe60a0dd9d4a7f3180cdb0e06de888cd52e708d8c6a2b52160de645883ee6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleDialogflowCxFlowTransitionRoutesTriggerFulfillmentMessagesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDialogflowCxFlow.GoogleDialogflowCxFlowTransitionRoutesTriggerFulfillmentMessagesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3e09d82d13a056100809df1747e9032e7cff75fcd0fd2e85fd7cac7fe514183f)
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
        :param metadata: Custom metadata. Dialogflow doesn't impose any structure on this. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#metadata GoogleDialogflowCxFlow#metadata}
        '''
        value = GoogleDialogflowCxFlowTransitionRoutesTriggerFulfillmentMessagesConversationSuccess(
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
        :param metadata: Custom metadata. Dialogflow doesn't impose any structure on this. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#metadata GoogleDialogflowCxFlow#metadata}
        '''
        value = GoogleDialogflowCxFlowTransitionRoutesTriggerFulfillmentMessagesLiveAgentHandoff(
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
        :param ssml: The SSML text to be synthesized. For more information, see SSML. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#ssml GoogleDialogflowCxFlow#ssml}
        :param text: The raw text to be synthesized. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#text GoogleDialogflowCxFlow#text}
        '''
        value = GoogleDialogflowCxFlowTransitionRoutesTriggerFulfillmentMessagesOutputAudioText(
            ssml=ssml, text=text
        )

        return typing.cast(None, jsii.invoke(self, "putOutputAudioText", [value]))

    @jsii.member(jsii_name="putPlayAudio")
    def put_play_audio(self, *, audio_uri: builtins.str) -> None:
        '''
        :param audio_uri: URI of the audio clip. Dialogflow does not impose any validation on this value. It is specific to the client that reads it. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#audio_uri GoogleDialogflowCxFlow#audio_uri}
        '''
        value = GoogleDialogflowCxFlowTransitionRoutesTriggerFulfillmentMessagesPlayAudio(
            audio_uri=audio_uri
        )

        return typing.cast(None, jsii.invoke(self, "putPlayAudio", [value]))

    @jsii.member(jsii_name="putTelephonyTransferCall")
    def put_telephony_transfer_call(self, *, phone_number: builtins.str) -> None:
        '''
        :param phone_number: Transfer the call to a phone number in E.164 format. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#phone_number GoogleDialogflowCxFlow#phone_number}
        '''
        value = GoogleDialogflowCxFlowTransitionRoutesTriggerFulfillmentMessagesTelephonyTransferCall(
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
        :param text: A collection of text responses. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#text GoogleDialogflowCxFlow#text}
        '''
        value = GoogleDialogflowCxFlowTransitionRoutesTriggerFulfillmentMessagesText(
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
    ) -> GoogleDialogflowCxFlowTransitionRoutesTriggerFulfillmentMessagesConversationSuccessOutputReference:
        return typing.cast(GoogleDialogflowCxFlowTransitionRoutesTriggerFulfillmentMessagesConversationSuccessOutputReference, jsii.get(self, "conversationSuccess"))

    @builtins.property
    @jsii.member(jsii_name="liveAgentHandoff")
    def live_agent_handoff(
        self,
    ) -> GoogleDialogflowCxFlowTransitionRoutesTriggerFulfillmentMessagesLiveAgentHandoffOutputReference:
        return typing.cast(GoogleDialogflowCxFlowTransitionRoutesTriggerFulfillmentMessagesLiveAgentHandoffOutputReference, jsii.get(self, "liveAgentHandoff"))

    @builtins.property
    @jsii.member(jsii_name="outputAudioText")
    def output_audio_text(
        self,
    ) -> GoogleDialogflowCxFlowTransitionRoutesTriggerFulfillmentMessagesOutputAudioTextOutputReference:
        return typing.cast(GoogleDialogflowCxFlowTransitionRoutesTriggerFulfillmentMessagesOutputAudioTextOutputReference, jsii.get(self, "outputAudioText"))

    @builtins.property
    @jsii.member(jsii_name="playAudio")
    def play_audio(
        self,
    ) -> "GoogleDialogflowCxFlowTransitionRoutesTriggerFulfillmentMessagesPlayAudioOutputReference":
        return typing.cast("GoogleDialogflowCxFlowTransitionRoutesTriggerFulfillmentMessagesPlayAudioOutputReference", jsii.get(self, "playAudio"))

    @builtins.property
    @jsii.member(jsii_name="telephonyTransferCall")
    def telephony_transfer_call(
        self,
    ) -> "GoogleDialogflowCxFlowTransitionRoutesTriggerFulfillmentMessagesTelephonyTransferCallOutputReference":
        return typing.cast("GoogleDialogflowCxFlowTransitionRoutesTriggerFulfillmentMessagesTelephonyTransferCallOutputReference", jsii.get(self, "telephonyTransferCall"))

    @builtins.property
    @jsii.member(jsii_name="text")
    def text(
        self,
    ) -> "GoogleDialogflowCxFlowTransitionRoutesTriggerFulfillmentMessagesTextOutputReference":
        return typing.cast("GoogleDialogflowCxFlowTransitionRoutesTriggerFulfillmentMessagesTextOutputReference", jsii.get(self, "text"))

    @builtins.property
    @jsii.member(jsii_name="channelInput")
    def channel_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "channelInput"))

    @builtins.property
    @jsii.member(jsii_name="conversationSuccessInput")
    def conversation_success_input(
        self,
    ) -> typing.Optional[GoogleDialogflowCxFlowTransitionRoutesTriggerFulfillmentMessagesConversationSuccess]:
        return typing.cast(typing.Optional[GoogleDialogflowCxFlowTransitionRoutesTriggerFulfillmentMessagesConversationSuccess], jsii.get(self, "conversationSuccessInput"))

    @builtins.property
    @jsii.member(jsii_name="liveAgentHandoffInput")
    def live_agent_handoff_input(
        self,
    ) -> typing.Optional[GoogleDialogflowCxFlowTransitionRoutesTriggerFulfillmentMessagesLiveAgentHandoff]:
        return typing.cast(typing.Optional[GoogleDialogflowCxFlowTransitionRoutesTriggerFulfillmentMessagesLiveAgentHandoff], jsii.get(self, "liveAgentHandoffInput"))

    @builtins.property
    @jsii.member(jsii_name="outputAudioTextInput")
    def output_audio_text_input(
        self,
    ) -> typing.Optional[GoogleDialogflowCxFlowTransitionRoutesTriggerFulfillmentMessagesOutputAudioText]:
        return typing.cast(typing.Optional[GoogleDialogflowCxFlowTransitionRoutesTriggerFulfillmentMessagesOutputAudioText], jsii.get(self, "outputAudioTextInput"))

    @builtins.property
    @jsii.member(jsii_name="payloadInput")
    def payload_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "payloadInput"))

    @builtins.property
    @jsii.member(jsii_name="playAudioInput")
    def play_audio_input(
        self,
    ) -> typing.Optional["GoogleDialogflowCxFlowTransitionRoutesTriggerFulfillmentMessagesPlayAudio"]:
        return typing.cast(typing.Optional["GoogleDialogflowCxFlowTransitionRoutesTriggerFulfillmentMessagesPlayAudio"], jsii.get(self, "playAudioInput"))

    @builtins.property
    @jsii.member(jsii_name="telephonyTransferCallInput")
    def telephony_transfer_call_input(
        self,
    ) -> typing.Optional["GoogleDialogflowCxFlowTransitionRoutesTriggerFulfillmentMessagesTelephonyTransferCall"]:
        return typing.cast(typing.Optional["GoogleDialogflowCxFlowTransitionRoutesTriggerFulfillmentMessagesTelephonyTransferCall"], jsii.get(self, "telephonyTransferCallInput"))

    @builtins.property
    @jsii.member(jsii_name="textInput")
    def text_input(
        self,
    ) -> typing.Optional["GoogleDialogflowCxFlowTransitionRoutesTriggerFulfillmentMessagesText"]:
        return typing.cast(typing.Optional["GoogleDialogflowCxFlowTransitionRoutesTriggerFulfillmentMessagesText"], jsii.get(self, "textInput"))

    @builtins.property
    @jsii.member(jsii_name="channel")
    def channel(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "channel"))

    @channel.setter
    def channel(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8690d15b9137257d6f9ee9213315231c41ec83f5b4527dd525e724ffc5c480ee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "channel", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="payload")
    def payload(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "payload"))

    @payload.setter
    def payload(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fccc74f5e06ef36a07f83277c279bc200de603b16835ff1e70a68b0d957c5334)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "payload", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDialogflowCxFlowTransitionRoutesTriggerFulfillmentMessages]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDialogflowCxFlowTransitionRoutesTriggerFulfillmentMessages]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDialogflowCxFlowTransitionRoutesTriggerFulfillmentMessages]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__453d82510f9adc9db614143cd517ba4f565b2a6db300b9f8a6faedcdb1372282)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDialogflowCxFlow.GoogleDialogflowCxFlowTransitionRoutesTriggerFulfillmentMessagesPlayAudio",
    jsii_struct_bases=[],
    name_mapping={"audio_uri": "audioUri"},
)
class GoogleDialogflowCxFlowTransitionRoutesTriggerFulfillmentMessagesPlayAudio:
    def __init__(self, *, audio_uri: builtins.str) -> None:
        '''
        :param audio_uri: URI of the audio clip. Dialogflow does not impose any validation on this value. It is specific to the client that reads it. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#audio_uri GoogleDialogflowCxFlow#audio_uri}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aeaa482bfaa5dfaad614fee2fef6fef4103da1f019699ea086f8687451a0debb)
            check_type(argname="argument audio_uri", value=audio_uri, expected_type=type_hints["audio_uri"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "audio_uri": audio_uri,
        }

    @builtins.property
    def audio_uri(self) -> builtins.str:
        '''URI of the audio clip.

        Dialogflow does not impose any validation on this value. It is specific to the client that reads it.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#audio_uri GoogleDialogflowCxFlow#audio_uri}
        '''
        result = self._values.get("audio_uri")
        assert result is not None, "Required property 'audio_uri' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDialogflowCxFlowTransitionRoutesTriggerFulfillmentMessagesPlayAudio(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDialogflowCxFlowTransitionRoutesTriggerFulfillmentMessagesPlayAudioOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDialogflowCxFlow.GoogleDialogflowCxFlowTransitionRoutesTriggerFulfillmentMessagesPlayAudioOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2b742708f1595104a689aa6369edb59ed9c8fcbb51ce27e58cc79fc6a27527fb)
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
            type_hints = typing.get_type_hints(_typecheckingstub__53fdde3b49c83d9a3cbd9f2f9efbefcf3b82f2fa111960ae5924e9c818cdd315)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "audioUri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDialogflowCxFlowTransitionRoutesTriggerFulfillmentMessagesPlayAudio]:
        return typing.cast(typing.Optional[GoogleDialogflowCxFlowTransitionRoutesTriggerFulfillmentMessagesPlayAudio], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDialogflowCxFlowTransitionRoutesTriggerFulfillmentMessagesPlayAudio],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf03831b63f25ea1a0403eaadd1fbd9036d0e7001aba80950ccb6658ab717806)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDialogflowCxFlow.GoogleDialogflowCxFlowTransitionRoutesTriggerFulfillmentMessagesTelephonyTransferCall",
    jsii_struct_bases=[],
    name_mapping={"phone_number": "phoneNumber"},
)
class GoogleDialogflowCxFlowTransitionRoutesTriggerFulfillmentMessagesTelephonyTransferCall:
    def __init__(self, *, phone_number: builtins.str) -> None:
        '''
        :param phone_number: Transfer the call to a phone number in E.164 format. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#phone_number GoogleDialogflowCxFlow#phone_number}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e186a2b1ef179a0437ddfd4ae0f6eca9225a010c0d1c190a0b679f3c0e8e3e4)
            check_type(argname="argument phone_number", value=phone_number, expected_type=type_hints["phone_number"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "phone_number": phone_number,
        }

    @builtins.property
    def phone_number(self) -> builtins.str:
        '''Transfer the call to a phone number in E.164 format.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#phone_number GoogleDialogflowCxFlow#phone_number}
        '''
        result = self._values.get("phone_number")
        assert result is not None, "Required property 'phone_number' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDialogflowCxFlowTransitionRoutesTriggerFulfillmentMessagesTelephonyTransferCall(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDialogflowCxFlowTransitionRoutesTriggerFulfillmentMessagesTelephonyTransferCallOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDialogflowCxFlow.GoogleDialogflowCxFlowTransitionRoutesTriggerFulfillmentMessagesTelephonyTransferCallOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__57331cb9c6069d413867ce93e466e0c1ab9e4abab3d9a67e5aa4a394dff4fca7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5ab54ecaf8c1ed91aa519e07af5b72d0e7cfed9b66a102d9e11c0b00beed5e7f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "phoneNumber", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDialogflowCxFlowTransitionRoutesTriggerFulfillmentMessagesTelephonyTransferCall]:
        return typing.cast(typing.Optional[GoogleDialogflowCxFlowTransitionRoutesTriggerFulfillmentMessagesTelephonyTransferCall], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDialogflowCxFlowTransitionRoutesTriggerFulfillmentMessagesTelephonyTransferCall],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3cf35e97d6bbfc5664a8f38870f4d775a25938b2e2fa5e4b158d016e49b7b04c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDialogflowCxFlow.GoogleDialogflowCxFlowTransitionRoutesTriggerFulfillmentMessagesText",
    jsii_struct_bases=[],
    name_mapping={"text": "text"},
)
class GoogleDialogflowCxFlowTransitionRoutesTriggerFulfillmentMessagesText:
    def __init__(
        self,
        *,
        text: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param text: A collection of text responses. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#text GoogleDialogflowCxFlow#text}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0153409442fb161b628945747122cdf8ddc6e15a3d6d3a0948bc10c7a26885f6)
            check_type(argname="argument text", value=text, expected_type=type_hints["text"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if text is not None:
            self._values["text"] = text

    @builtins.property
    def text(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A collection of text responses.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#text GoogleDialogflowCxFlow#text}
        '''
        result = self._values.get("text")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDialogflowCxFlowTransitionRoutesTriggerFulfillmentMessagesText(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDialogflowCxFlowTransitionRoutesTriggerFulfillmentMessagesTextOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDialogflowCxFlow.GoogleDialogflowCxFlowTransitionRoutesTriggerFulfillmentMessagesTextOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a06dd4513f065ad9309d0a96051645e8a1e25667073f4ca1e04b988bc1877e2e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4129b5304583b960d5f0beec820380ae650c062c078679046d54b3e60db3a84c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "text", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDialogflowCxFlowTransitionRoutesTriggerFulfillmentMessagesText]:
        return typing.cast(typing.Optional[GoogleDialogflowCxFlowTransitionRoutesTriggerFulfillmentMessagesText], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDialogflowCxFlowTransitionRoutesTriggerFulfillmentMessagesText],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__50f2da856a359f6e13479ee354302498446f8687051668ea56ea87c957f0b2cb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleDialogflowCxFlowTransitionRoutesTriggerFulfillmentOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDialogflowCxFlow.GoogleDialogflowCxFlowTransitionRoutesTriggerFulfillmentOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7dbb19ced0b6c9b1d22198ba4a7f0983290defd105af87f66c03662cda69e461)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putConditionalCases")
    def put_conditional_cases(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleDialogflowCxFlowTransitionRoutesTriggerFulfillmentConditionalCases, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0582dbdbcdfcc015af334e2c55df9c543eb7cc8aab2c8f879e6ac28e82843b26)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putConditionalCases", [value]))

    @jsii.member(jsii_name="putMessages")
    def put_messages(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleDialogflowCxFlowTransitionRoutesTriggerFulfillmentMessages, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b0b934ff43ca7625a4f7b3d2b74223683bab64ed983cdb10e1e244620b05270)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putMessages", [value]))

    @jsii.member(jsii_name="putSetParameterActions")
    def put_set_parameter_actions(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleDialogflowCxFlowTransitionRoutesTriggerFulfillmentSetParameterActions", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__189b19022a0a37d65f611da92ce86132c15753dff6e3d735ffc2a5bb2f5f7d9e)
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
    ) -> GoogleDialogflowCxFlowTransitionRoutesTriggerFulfillmentConditionalCasesList:
        return typing.cast(GoogleDialogflowCxFlowTransitionRoutesTriggerFulfillmentConditionalCasesList, jsii.get(self, "conditionalCases"))

    @builtins.property
    @jsii.member(jsii_name="messages")
    def messages(
        self,
    ) -> GoogleDialogflowCxFlowTransitionRoutesTriggerFulfillmentMessagesList:
        return typing.cast(GoogleDialogflowCxFlowTransitionRoutesTriggerFulfillmentMessagesList, jsii.get(self, "messages"))

    @builtins.property
    @jsii.member(jsii_name="setParameterActions")
    def set_parameter_actions(
        self,
    ) -> "GoogleDialogflowCxFlowTransitionRoutesTriggerFulfillmentSetParameterActionsList":
        return typing.cast("GoogleDialogflowCxFlowTransitionRoutesTriggerFulfillmentSetParameterActionsList", jsii.get(self, "setParameterActions"))

    @builtins.property
    @jsii.member(jsii_name="conditionalCasesInput")
    def conditional_cases_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDialogflowCxFlowTransitionRoutesTriggerFulfillmentConditionalCases]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDialogflowCxFlowTransitionRoutesTriggerFulfillmentConditionalCases]]], jsii.get(self, "conditionalCasesInput"))

    @builtins.property
    @jsii.member(jsii_name="messagesInput")
    def messages_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDialogflowCxFlowTransitionRoutesTriggerFulfillmentMessages]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDialogflowCxFlowTransitionRoutesTriggerFulfillmentMessages]]], jsii.get(self, "messagesInput"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleDialogflowCxFlowTransitionRoutesTriggerFulfillmentSetParameterActions"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleDialogflowCxFlowTransitionRoutesTriggerFulfillmentSetParameterActions"]]], jsii.get(self, "setParameterActionsInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__3bc3ed29a6fe1a6c56df7a77a6dafca943bcfc091afa8b6d48041ad775e8b814)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "returnPartialResponses", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tag")
    def tag(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tag"))

    @tag.setter
    def tag(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c9f70849da3e966fdf6b96ed7433d72b3121157e46ef03cb37bcc66ac4dd2b01)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tag", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="webhook")
    def webhook(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "webhook"))

    @webhook.setter
    def webhook(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aeee2472db9caa2d47a89521789e8b35f36e94f69faeb5e8e3a183a96628c091)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "webhook", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDialogflowCxFlowTransitionRoutesTriggerFulfillment]:
        return typing.cast(typing.Optional[GoogleDialogflowCxFlowTransitionRoutesTriggerFulfillment], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDialogflowCxFlowTransitionRoutesTriggerFulfillment],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__220977d5a118b7da09035631babbb52080bd1f81cc737ffa8743eebdfbed6d4b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDialogflowCxFlow.GoogleDialogflowCxFlowTransitionRoutesTriggerFulfillmentSetParameterActions",
    jsii_struct_bases=[],
    name_mapping={"parameter": "parameter", "value": "value"},
)
class GoogleDialogflowCxFlowTransitionRoutesTriggerFulfillmentSetParameterActions:
    def __init__(
        self,
        *,
        parameter: typing.Optional[builtins.str] = None,
        value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param parameter: Display name of the parameter. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#parameter GoogleDialogflowCxFlow#parameter}
        :param value: The new JSON-encoded value of the parameter. A null value clears the parameter. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#value GoogleDialogflowCxFlow#value}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__64ce5b4c1ad6bc6fd3c99bb3cb134de4b9fbc58d10cb9c822cba3d1ab87681a4)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#parameter GoogleDialogflowCxFlow#parameter}
        '''
        result = self._values.get("parameter")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def value(self) -> typing.Optional[builtins.str]:
        '''The new JSON-encoded value of the parameter. A null value clears the parameter.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_flow#value GoogleDialogflowCxFlow#value}
        '''
        result = self._values.get("value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDialogflowCxFlowTransitionRoutesTriggerFulfillmentSetParameterActions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDialogflowCxFlowTransitionRoutesTriggerFulfillmentSetParameterActionsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDialogflowCxFlow.GoogleDialogflowCxFlowTransitionRoutesTriggerFulfillmentSetParameterActionsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1009379d86a81f455f149be928b5167054ab533b589dbe561f7f79d4c5d25510)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleDialogflowCxFlowTransitionRoutesTriggerFulfillmentSetParameterActionsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d630eb93806d039a7a3be4015b25441367e050cb2051227e0697b8350fa2b188)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleDialogflowCxFlowTransitionRoutesTriggerFulfillmentSetParameterActionsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3678a2a493a46d2caed937bb0e6d6d7d7ab5f74e63263abbd8de24e174040145)
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
            type_hints = typing.get_type_hints(_typecheckingstub__db8186aeed4322c4b8712a7e1d8ae779695931b38a479f99a2fee24571c061cf)
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
            type_hints = typing.get_type_hints(_typecheckingstub__65ccf02e547b9c9c1c79f52b2913957dae39dd5af3cf05dc2598d8c185979bfd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDialogflowCxFlowTransitionRoutesTriggerFulfillmentSetParameterActions]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDialogflowCxFlowTransitionRoutesTriggerFulfillmentSetParameterActions]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDialogflowCxFlowTransitionRoutesTriggerFulfillmentSetParameterActions]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__23361771f23ebe9a1ed4c64c22b1f9725c28b96f39af11c1428dd0a53a053b33)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleDialogflowCxFlowTransitionRoutesTriggerFulfillmentSetParameterActionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDialogflowCxFlow.GoogleDialogflowCxFlowTransitionRoutesTriggerFulfillmentSetParameterActionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__918e7e9ba3fde7d211de3237538cae953afc374dedfa658ae13f2ece422f5bb8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b67d67b07417c3d48974e8f75da3e2985e69a745d9600461aba776c5232c103d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "parameter", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b65d59229d975c4b30135574d2a00ab712add1d09ac284b6f5f22b4fc3ed795)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDialogflowCxFlowTransitionRoutesTriggerFulfillmentSetParameterActions]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDialogflowCxFlowTransitionRoutesTriggerFulfillmentSetParameterActions]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDialogflowCxFlowTransitionRoutesTriggerFulfillmentSetParameterActions]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bbf8ba72500a2f738831af42f750ba19782166ea872ad100c0378e20368d07e3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "GoogleDialogflowCxFlow",
    "GoogleDialogflowCxFlowAdvancedSettings",
    "GoogleDialogflowCxFlowAdvancedSettingsAudioExportGcsDestination",
    "GoogleDialogflowCxFlowAdvancedSettingsAudioExportGcsDestinationOutputReference",
    "GoogleDialogflowCxFlowAdvancedSettingsDtmfSettings",
    "GoogleDialogflowCxFlowAdvancedSettingsDtmfSettingsOutputReference",
    "GoogleDialogflowCxFlowAdvancedSettingsLoggingSettings",
    "GoogleDialogflowCxFlowAdvancedSettingsLoggingSettingsOutputReference",
    "GoogleDialogflowCxFlowAdvancedSettingsOutputReference",
    "GoogleDialogflowCxFlowAdvancedSettingsSpeechSettings",
    "GoogleDialogflowCxFlowAdvancedSettingsSpeechSettingsOutputReference",
    "GoogleDialogflowCxFlowConfig",
    "GoogleDialogflowCxFlowEventHandlers",
    "GoogleDialogflowCxFlowEventHandlersList",
    "GoogleDialogflowCxFlowEventHandlersOutputReference",
    "GoogleDialogflowCxFlowEventHandlersTriggerFulfillment",
    "GoogleDialogflowCxFlowEventHandlersTriggerFulfillmentConditionalCases",
    "GoogleDialogflowCxFlowEventHandlersTriggerFulfillmentConditionalCasesList",
    "GoogleDialogflowCxFlowEventHandlersTriggerFulfillmentConditionalCasesOutputReference",
    "GoogleDialogflowCxFlowEventHandlersTriggerFulfillmentMessages",
    "GoogleDialogflowCxFlowEventHandlersTriggerFulfillmentMessagesConversationSuccess",
    "GoogleDialogflowCxFlowEventHandlersTriggerFulfillmentMessagesConversationSuccessOutputReference",
    "GoogleDialogflowCxFlowEventHandlersTriggerFulfillmentMessagesList",
    "GoogleDialogflowCxFlowEventHandlersTriggerFulfillmentMessagesLiveAgentHandoff",
    "GoogleDialogflowCxFlowEventHandlersTriggerFulfillmentMessagesLiveAgentHandoffOutputReference",
    "GoogleDialogflowCxFlowEventHandlersTriggerFulfillmentMessagesOutputAudioText",
    "GoogleDialogflowCxFlowEventHandlersTriggerFulfillmentMessagesOutputAudioTextOutputReference",
    "GoogleDialogflowCxFlowEventHandlersTriggerFulfillmentMessagesOutputReference",
    "GoogleDialogflowCxFlowEventHandlersTriggerFulfillmentMessagesPlayAudio",
    "GoogleDialogflowCxFlowEventHandlersTriggerFulfillmentMessagesPlayAudioOutputReference",
    "GoogleDialogflowCxFlowEventHandlersTriggerFulfillmentMessagesTelephonyTransferCall",
    "GoogleDialogflowCxFlowEventHandlersTriggerFulfillmentMessagesTelephonyTransferCallOutputReference",
    "GoogleDialogflowCxFlowEventHandlersTriggerFulfillmentMessagesText",
    "GoogleDialogflowCxFlowEventHandlersTriggerFulfillmentMessagesTextOutputReference",
    "GoogleDialogflowCxFlowEventHandlersTriggerFulfillmentOutputReference",
    "GoogleDialogflowCxFlowEventHandlersTriggerFulfillmentSetParameterActions",
    "GoogleDialogflowCxFlowEventHandlersTriggerFulfillmentSetParameterActionsList",
    "GoogleDialogflowCxFlowEventHandlersTriggerFulfillmentSetParameterActionsOutputReference",
    "GoogleDialogflowCxFlowKnowledgeConnectorSettings",
    "GoogleDialogflowCxFlowKnowledgeConnectorSettingsDataStoreConnections",
    "GoogleDialogflowCxFlowKnowledgeConnectorSettingsDataStoreConnectionsList",
    "GoogleDialogflowCxFlowKnowledgeConnectorSettingsDataStoreConnectionsOutputReference",
    "GoogleDialogflowCxFlowKnowledgeConnectorSettingsOutputReference",
    "GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillment",
    "GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentAdvancedSettings",
    "GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentAdvancedSettingsDtmfSettings",
    "GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentAdvancedSettingsDtmfSettingsOutputReference",
    "GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentAdvancedSettingsLoggingSettings",
    "GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentAdvancedSettingsLoggingSettingsOutputReference",
    "GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentAdvancedSettingsOutputReference",
    "GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentAdvancedSettingsSpeechSettings",
    "GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentAdvancedSettingsSpeechSettingsOutputReference",
    "GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentConditionalCases",
    "GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentConditionalCasesList",
    "GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentConditionalCasesOutputReference",
    "GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentMessages",
    "GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentMessagesConversationSuccess",
    "GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentMessagesConversationSuccessOutputReference",
    "GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentMessagesEndInteraction",
    "GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentMessagesEndInteractionList",
    "GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentMessagesEndInteractionOutputReference",
    "GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentMessagesKnowledgeInfoCard",
    "GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentMessagesKnowledgeInfoCardOutputReference",
    "GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentMessagesList",
    "GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentMessagesLiveAgentHandoff",
    "GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentMessagesLiveAgentHandoffOutputReference",
    "GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentMessagesMixedAudio",
    "GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentMessagesMixedAudioList",
    "GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentMessagesMixedAudioOutputReference",
    "GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentMessagesMixedAudioSegments",
    "GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentMessagesMixedAudioSegmentsList",
    "GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentMessagesMixedAudioSegmentsOutputReference",
    "GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentMessagesOutputAudioText",
    "GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentMessagesOutputAudioTextOutputReference",
    "GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentMessagesOutputReference",
    "GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentMessagesPlayAudio",
    "GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentMessagesPlayAudioOutputReference",
    "GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentMessagesTelephonyTransferCall",
    "GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentMessagesTelephonyTransferCallOutputReference",
    "GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentMessagesText",
    "GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentMessagesTextOutputReference",
    "GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentOutputReference",
    "GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentSetParameterActions",
    "GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentSetParameterActionsList",
    "GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentSetParameterActionsOutputReference",
    "GoogleDialogflowCxFlowNluSettings",
    "GoogleDialogflowCxFlowNluSettingsOutputReference",
    "GoogleDialogflowCxFlowTimeouts",
    "GoogleDialogflowCxFlowTimeoutsOutputReference",
    "GoogleDialogflowCxFlowTransitionRoutes",
    "GoogleDialogflowCxFlowTransitionRoutesList",
    "GoogleDialogflowCxFlowTransitionRoutesOutputReference",
    "GoogleDialogflowCxFlowTransitionRoutesTriggerFulfillment",
    "GoogleDialogflowCxFlowTransitionRoutesTriggerFulfillmentConditionalCases",
    "GoogleDialogflowCxFlowTransitionRoutesTriggerFulfillmentConditionalCasesList",
    "GoogleDialogflowCxFlowTransitionRoutesTriggerFulfillmentConditionalCasesOutputReference",
    "GoogleDialogflowCxFlowTransitionRoutesTriggerFulfillmentMessages",
    "GoogleDialogflowCxFlowTransitionRoutesTriggerFulfillmentMessagesConversationSuccess",
    "GoogleDialogflowCxFlowTransitionRoutesTriggerFulfillmentMessagesConversationSuccessOutputReference",
    "GoogleDialogflowCxFlowTransitionRoutesTriggerFulfillmentMessagesList",
    "GoogleDialogflowCxFlowTransitionRoutesTriggerFulfillmentMessagesLiveAgentHandoff",
    "GoogleDialogflowCxFlowTransitionRoutesTriggerFulfillmentMessagesLiveAgentHandoffOutputReference",
    "GoogleDialogflowCxFlowTransitionRoutesTriggerFulfillmentMessagesOutputAudioText",
    "GoogleDialogflowCxFlowTransitionRoutesTriggerFulfillmentMessagesOutputAudioTextOutputReference",
    "GoogleDialogflowCxFlowTransitionRoutesTriggerFulfillmentMessagesOutputReference",
    "GoogleDialogflowCxFlowTransitionRoutesTriggerFulfillmentMessagesPlayAudio",
    "GoogleDialogflowCxFlowTransitionRoutesTriggerFulfillmentMessagesPlayAudioOutputReference",
    "GoogleDialogflowCxFlowTransitionRoutesTriggerFulfillmentMessagesTelephonyTransferCall",
    "GoogleDialogflowCxFlowTransitionRoutesTriggerFulfillmentMessagesTelephonyTransferCallOutputReference",
    "GoogleDialogflowCxFlowTransitionRoutesTriggerFulfillmentMessagesText",
    "GoogleDialogflowCxFlowTransitionRoutesTriggerFulfillmentMessagesTextOutputReference",
    "GoogleDialogflowCxFlowTransitionRoutesTriggerFulfillmentOutputReference",
    "GoogleDialogflowCxFlowTransitionRoutesTriggerFulfillmentSetParameterActions",
    "GoogleDialogflowCxFlowTransitionRoutesTriggerFulfillmentSetParameterActionsList",
    "GoogleDialogflowCxFlowTransitionRoutesTriggerFulfillmentSetParameterActionsOutputReference",
]

publication.publish()

def _typecheckingstub__8ddc1c9bd1aaab871a2b80768c2bc499e93a36227c2ec26b6797aac6fac61ceb(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    display_name: builtins.str,
    advanced_settings: typing.Optional[typing.Union[GoogleDialogflowCxFlowAdvancedSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    description: typing.Optional[builtins.str] = None,
    event_handlers: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleDialogflowCxFlowEventHandlers, typing.Dict[builtins.str, typing.Any]]]]] = None,
    id: typing.Optional[builtins.str] = None,
    is_default_start_flow: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    knowledge_connector_settings: typing.Optional[typing.Union[GoogleDialogflowCxFlowKnowledgeConnectorSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    language_code: typing.Optional[builtins.str] = None,
    nlu_settings: typing.Optional[typing.Union[GoogleDialogflowCxFlowNluSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    parent: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[GoogleDialogflowCxFlowTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    transition_route_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
    transition_routes: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleDialogflowCxFlowTransitionRoutes, typing.Dict[builtins.str, typing.Any]]]]] = None,
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

def _typecheckingstub__ad3b054a471de21d0a367ca38d61ec2a1c86d28c7c7e15d0fa29c34cef2e8ffa(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d5763a95f2a19a20a2cee1cd63b8e22e995b6ccdda0bc67f0a8ba7c9afea462(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleDialogflowCxFlowEventHandlers, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f67d14e084641d1578e154aed126fcf46d108e0c8f21351b034db072abbe3b8(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleDialogflowCxFlowTransitionRoutes, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7564a7905ff3d080ec73fd5b3674d80316185888f34b793426007f2891348fc4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d57e353ea4e0c1dbefde806a99b8c916a02fa1ed2fdd994823bfcf5422e9934(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eab5ec690ece1ff9fa75d59b2a15d2b7ececfba9a83206cd737e9f2f7198cb5b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc61fcc21cb3d353f84d5d4e88bdffe57d189d4c895ab85b7d3f152168394a73(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb70b48e85ea80ce1f103a0c05a4b3466c57a382c528c7a81ce07b3b8df410ec(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a48c675e5612a9b38a6595f66082b141506e7336639e253e7d20e4b003a2e87d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8b9d2da6f549846ac8b8c3ea7bb8b102639d483550c7cb5ff7fa1924d572b11(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74522f9b5137db65e0921cf1c5e8aa67898022072b01667d01626b26b51a97d4(
    *,
    audio_export_gcs_destination: typing.Optional[typing.Union[GoogleDialogflowCxFlowAdvancedSettingsAudioExportGcsDestination, typing.Dict[builtins.str, typing.Any]]] = None,
    dtmf_settings: typing.Optional[typing.Union[GoogleDialogflowCxFlowAdvancedSettingsDtmfSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    logging_settings: typing.Optional[typing.Union[GoogleDialogflowCxFlowAdvancedSettingsLoggingSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    speech_settings: typing.Optional[typing.Union[GoogleDialogflowCxFlowAdvancedSettingsSpeechSettings, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f14a90e7cb3882840e4ec911e01e5451e2d8b19a9979b602f4294dbcd64ba59c(
    *,
    uri: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__126bfaf474003387ad65638cfd0a1d944237446dd9255e7e0c74b0ed088028dc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bcf8efda4b84a8fbcd37d884c901b0367ea99053549c30a600b982d7b6ae0208(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6753a3d1e6d9677e891ba03b4be61d55b680366939ab6a465ec78726af5affdc(
    value: typing.Optional[GoogleDialogflowCxFlowAdvancedSettingsAudioExportGcsDestination],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dbbd4cad34ff6aa630667af905d7c23565c8b573fc94b53aeedc8657f064a053(
    *,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    finish_digit: typing.Optional[builtins.str] = None,
    max_digits: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94e13c969a0969e8c13bac2c5a7a19f17db5928989f957c7eff5e02b1285b21c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__444113a02773315b4f4224c440ff697f2d51c4eb404fb307174f2a56c5ff5bfb(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__080fea3290e7f671c0b7921f05c14cfde7ad37d6a3ae820c5301a730c89c0ba4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79d79812fc802c105c6e8454b68dff149578f978375c174f256286489e456019(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d36606aa4eb8bd597c3494f9c89fb89e5f555047331abb521468e0e51933e94(
    value: typing.Optional[GoogleDialogflowCxFlowAdvancedSettingsDtmfSettings],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3492a20de1578c5c1d3da93c3c3beb7951c686d51823edd9730603c329cfac98(
    *,
    enable_consent_based_redaction: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enable_interaction_logging: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enable_stackdriver_logging: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eda197ee35e2807c014125376afc7f94d02f5134ff62b3175995252f225a43e3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38398b43bc6f1b41b7d99174462ef2aac48d94bae30ee43ea74ec23337c2b288(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5115bf01330153cb029216351ce854be302723316e25d50b61af4e3a6437642(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bfa2016117ffbd080867f9afc0a524229692dbd88ca49e57d688d600135d97a9(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42733c4b44cc0960d1e468fdab957bed90caa698a8ccd72a0e2f48e116fe1756(
    value: typing.Optional[GoogleDialogflowCxFlowAdvancedSettingsLoggingSettings],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a4cfef87b8c76c85a3fbfc1b57d3fdf6b29e64131a20d9a3f54dc95a49cf56d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf2a7517d1b6799be5bbd2bca26336584a9c1d7021407f29c7456dedcdffaa7c(
    value: typing.Optional[GoogleDialogflowCxFlowAdvancedSettings],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b64a57b0c34c8d30441358acced2700a3b48fec9630d061356c581d519ce94e7(
    *,
    endpointer_sensitivity: typing.Optional[jsii.Number] = None,
    models: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    no_speech_timeout: typing.Optional[builtins.str] = None,
    use_timeout_based_endpointing: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__373c7d629578331f1a8b8da6aba231d69c324dd2eea9b4c3e1e8f3af0c55a085(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e8af063947de8ed1d7a7875ca13ab6e3c88628ff99ad2764e7037bf76d30276(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3860718a3f419c431bb5ce68d767688868f3d6436ac512fe59a00177a3b585ff(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68ee48cb429657778e991d921e8f985675b5abe21a5553c7a25f8c3e9893da20(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54ace7069c2f5634036911d0430435b34c9f393ba0b8d46e17d82cd60a22979b(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__990fa67d3660106df9524adc4b6476553f3e3912f5f307ea5d196b451508519e(
    value: typing.Optional[GoogleDialogflowCxFlowAdvancedSettingsSpeechSettings],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5b6d22821ccb6c1261edc07f6bc6656e98299156ae0eaee2da8542a3e22cb90(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    display_name: builtins.str,
    advanced_settings: typing.Optional[typing.Union[GoogleDialogflowCxFlowAdvancedSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    description: typing.Optional[builtins.str] = None,
    event_handlers: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleDialogflowCxFlowEventHandlers, typing.Dict[builtins.str, typing.Any]]]]] = None,
    id: typing.Optional[builtins.str] = None,
    is_default_start_flow: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    knowledge_connector_settings: typing.Optional[typing.Union[GoogleDialogflowCxFlowKnowledgeConnectorSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    language_code: typing.Optional[builtins.str] = None,
    nlu_settings: typing.Optional[typing.Union[GoogleDialogflowCxFlowNluSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    parent: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[GoogleDialogflowCxFlowTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    transition_route_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
    transition_routes: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleDialogflowCxFlowTransitionRoutes, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98d6b437f59c96e369e9a65e8cba23f38e57df796929bbd75224bcedc388b721(
    *,
    event: typing.Optional[builtins.str] = None,
    target_flow: typing.Optional[builtins.str] = None,
    target_page: typing.Optional[builtins.str] = None,
    trigger_fulfillment: typing.Optional[typing.Union[GoogleDialogflowCxFlowEventHandlersTriggerFulfillment, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ea6d2385130136ba9ba2449229da1e1d3e391e41dfafc4c8ca3bb1631d4ce14(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b72692e2f83b58047d9ef491b2c6b8d6d65b1d0576f01c8e029ece54d7ca94a(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10e47925b00e47f983de73bfa202626a1e3135e199f22fe97d586dabb330c1f3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a87ff1ba2605882bab6a41459482a8d5ce15d04140c213017f7aa60d0f1f8cd4(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__797650aaec31e7ca6bb8bc45d5cb90e35913ad807f256a34b97189d1d969d736(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__550686a1780bbee4f9f8564add05760636a98a28cf7e02f3c02b086103f5e3dc(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDialogflowCxFlowEventHandlers]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0b49a2bf192f63cb5a72c1bd7cdffb07f5cdb45767d0977c9c0af70fe72a68a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65b6f23d473fdfa3616c5c573a6311ed0c64ca67237e5fc371844d19be8d4b06(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8232a76d7dd21a85014f51ee2b25961374daa0e33aba5d27aed553abf55ee0b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf6d60b11ea63adf1c7be2210f0b5cecc0c0346fad1ab06f7f78bd60d2f16a37(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22b10706871c1d1f665ef2d90bd0d58a208650af42514f7be1dca25fb9f02432(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDialogflowCxFlowEventHandlers]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2b0b5e0e8e08564eff12bc1e01fd9807cb7a628d58f0aa0ac775e881f69e3fe(
    *,
    conditional_cases: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleDialogflowCxFlowEventHandlersTriggerFulfillmentConditionalCases, typing.Dict[builtins.str, typing.Any]]]]] = None,
    enable_generative_fallback: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    messages: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleDialogflowCxFlowEventHandlersTriggerFulfillmentMessages, typing.Dict[builtins.str, typing.Any]]]]] = None,
    return_partial_responses: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    set_parameter_actions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleDialogflowCxFlowEventHandlersTriggerFulfillmentSetParameterActions, typing.Dict[builtins.str, typing.Any]]]]] = None,
    tag: typing.Optional[builtins.str] = None,
    webhook: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c91d12edab2a2dbd0bf7747bb2162e7c5824f681ff0be9abf60fd5a33549bd1(
    *,
    cases: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8dc297fa3b4deca51bde040af9d3d85d51244a4f502dc3dc2edfd6b442cd6cf3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5085cb33cee60f0351f3707232a96f794e06e88c9214ab90efd906fee9c0034(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ba859ff220cb9d944e616471ac511e557a5570ae65fcc73358ef0b6aee8b570(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5d1ff8d188984b06b917cc566fa0b77d1abdc648bc70011da6ca2c1425ef353(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c046a332b2e188696b71b7ebb514bc26bebd1e040aebcd934005665a2890fc2(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aaf545456d221be7117ea8e6a65ac1c3cc6ce3dc384d83d3d6f8aec0539adb64(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDialogflowCxFlowEventHandlersTriggerFulfillmentConditionalCases]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d18f9237ed20e32840fe9794f3f02ec81890ca29521cd3ea20bff5398ba6515(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6059d8a6d6d9cc3d499120d5011eeb5726168e3b30d8845649011bb6ea07f40(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c97cb0f6e6865d8ec850b8cbeedc765de0021d6a630119f6ace7b60ba3f5d0f(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDialogflowCxFlowEventHandlersTriggerFulfillmentConditionalCases]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__47cf1b77ff3ec061bdddb90036c33368f3e5b8f584b5d70cb6c8d6c442148a4f(
    *,
    channel: typing.Optional[builtins.str] = None,
    conversation_success: typing.Optional[typing.Union[GoogleDialogflowCxFlowEventHandlersTriggerFulfillmentMessagesConversationSuccess, typing.Dict[builtins.str, typing.Any]]] = None,
    live_agent_handoff: typing.Optional[typing.Union[GoogleDialogflowCxFlowEventHandlersTriggerFulfillmentMessagesLiveAgentHandoff, typing.Dict[builtins.str, typing.Any]]] = None,
    output_audio_text: typing.Optional[typing.Union[GoogleDialogflowCxFlowEventHandlersTriggerFulfillmentMessagesOutputAudioText, typing.Dict[builtins.str, typing.Any]]] = None,
    payload: typing.Optional[builtins.str] = None,
    play_audio: typing.Optional[typing.Union[GoogleDialogflowCxFlowEventHandlersTriggerFulfillmentMessagesPlayAudio, typing.Dict[builtins.str, typing.Any]]] = None,
    telephony_transfer_call: typing.Optional[typing.Union[GoogleDialogflowCxFlowEventHandlersTriggerFulfillmentMessagesTelephonyTransferCall, typing.Dict[builtins.str, typing.Any]]] = None,
    text: typing.Optional[typing.Union[GoogleDialogflowCxFlowEventHandlersTriggerFulfillmentMessagesText, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71ba2f39b3e982d1ed7e0151541fccd54bbba72eb06788d47077001ea900f65b(
    *,
    metadata: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__999db007c9c1915b58c71b617ffb2b51d98449f40e550093ac8de4804f4b8bab(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80c92f6879994241f8be0374257b2000fb20537e65d4e70e623aacebb56b8da9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad2092c5876164f320659d6b4e0c9ee2959f15bfc8ab9c6240bed7c672aca6db(
    value: typing.Optional[GoogleDialogflowCxFlowEventHandlersTriggerFulfillmentMessagesConversationSuccess],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91a30f242e5ea4183f4a388675dae2a39a85ebb559121c69b38971a70ae0259b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef209c5de032bddd5d5f68a59e2625324e8d419c75f45bb6c212f1afcdcf5337(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3fb9eaee16e8332e5d899c05745620e138957c5e96c41b0be100922470cea560(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8df20db12f6bf4a2136b74d845969b82f6c72d29f3160edf5aaf3e9607405c84(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc59802a7434cb11ca69be912e59b031a4a61b4c64c7c3877cf2b86eedfb6dc5(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66fc6f716cf1db773623fff9494d38d2fd97eaa1964cbad881bf5cb7c48ed834(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDialogflowCxFlowEventHandlersTriggerFulfillmentMessages]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de157fcd6751d9db70e1e58531c48002ac6b8c5e271e1629c9cfe53f64074595(
    *,
    metadata: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2d9347e9d2f662db1ce7f21c8a413ffd0a12b9032e84ad52c72b13bb5a38b4c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6de09dd2cb920aec8c6fa2d52287a5fe3f6517d58922ee571408de959977b10e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__17248d3513fcfd5a6bdcb22aa7baa4cc0a70cd192852dbe9123ed496586b7418(
    value: typing.Optional[GoogleDialogflowCxFlowEventHandlersTriggerFulfillmentMessagesLiveAgentHandoff],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2cd4b98e2ab2e75f2d752a959a0b0e1ef2932096b760b53b77c60a04151f4085(
    *,
    ssml: typing.Optional[builtins.str] = None,
    text: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54f4bdf6f12fb261e41faa5a2b0f3246d66e76f40c88d4a533e2192eb312f928(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d4b85156c1116cd26e4873b89c1a4966f7a568ab35aebf2d9be598cd25c2003(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aed58b632dd33e478da2b95a0c954d89c8684469ad93a8c05bf1fefb92334ef6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__407c042b8ffe7beb5fd352f1cc631efea66dd2870ba4c36b89578b5c469a4725(
    value: typing.Optional[GoogleDialogflowCxFlowEventHandlersTriggerFulfillmentMessagesOutputAudioText],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a5d7394da129220d20cf2d3e9de1e4a8bc97cf36ff80f93157bd345d447f814(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ee365bd5e7ad02443edec08b36d422ebd6ba0925fb54f56b43c0d0b5b6e08f5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2cd3500edffc79de60595b43ccb8b511bac26f94034afd27658ce0f1dbb34d3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b33fd52d5aee1abc2af7510c2d810adabcf29a9323ff8a75fac9e0e5a9b3d8e2(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDialogflowCxFlowEventHandlersTriggerFulfillmentMessages]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__efa71b0a2ce84c87ecd1d7c824a1b3d735c9cf5482efb3d60fc9b5a4a0486262(
    *,
    audio_uri: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ecc3fe6bb8b710da9ac63e4d0055e56679e0eebb090c310213eff1a90119e934(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e7dc243844b4f75b91211ae2d27b9887c7baa9733bc9bdbed88745218e44d94(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11fdc1ebecce9edee0dd805324d6cf8aee3e2b30bd7204e4a9f3d3dbbe9424e4(
    value: typing.Optional[GoogleDialogflowCxFlowEventHandlersTriggerFulfillmentMessagesPlayAudio],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e89b70a63040a97046353aa145e0c5def89f523a28e0e3192d56cb96c46a58d1(
    *,
    phone_number: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d1e51f50aa052e9299e27e0ff1c13913459e9ec3fb03cdd73bb574e8248a106(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54701318c05c962d1797c39a43227a0a786172c08ece78e448a8f61fcc24f506(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc6365e33a446197ecc983cc3b6027917a4bd3902601a9e02ecc1c5923b39d43(
    value: typing.Optional[GoogleDialogflowCxFlowEventHandlersTriggerFulfillmentMessagesTelephonyTransferCall],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__caf968656644d2b99fc0f819ca3a16b23f096995475b7b3a6e08e5c1c1358318(
    *,
    text: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4ec1e46f38dd2a469bcfc5e0b204a6b11595e08e119b7981575105910d8c78d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__037aec295bb472f589ea596cbfebb45456ce81962af528f351d6b6e616e3b242(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__479b59249a9dfb3608d4dc0fed24b0337e07fe844e83827b6f943b301566db71(
    value: typing.Optional[GoogleDialogflowCxFlowEventHandlersTriggerFulfillmentMessagesText],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3bad15ed6b01e2d0546b46b152ea04c1371cb3c7d4324e188ef4e47b66fade90(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__819a5d95220721c41d98998c537993544cc544bb52e5607faed5c09e1193c8a8(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleDialogflowCxFlowEventHandlersTriggerFulfillmentConditionalCases, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42f5acfd4c64d5ac63b8f15f48c10d2fd9d8bc9b56ae86ee6bab6d18e6328278(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleDialogflowCxFlowEventHandlersTriggerFulfillmentMessages, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__760234eadd3578b5586974b36f2ac0369361d386d0d7c7e1288fef584b33164c(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleDialogflowCxFlowEventHandlersTriggerFulfillmentSetParameterActions, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__547e1494f898245896601649f3fdef7524af98269263987cc20749f812479ebb(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b357e6f9c60440207ddaad42c083f61899fd2ca2bcace2737949eb6ea6851467(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05e50fe901dbf61aa635a56e265013a777da162a618815e4ec01998dc21f697c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91bf4cce913b48aa52137ae8d78dc55d18dccf652b6d505fed4dc622a5a91a55(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3744515a4e7ffc4c34a960ba8fd725e26afa66704674a5e14177efa17342c58(
    value: typing.Optional[GoogleDialogflowCxFlowEventHandlersTriggerFulfillment],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93c78aaa9dc78e546841f3429b21f134fd3cdfc47dbb4d8f2861327ff41bba56(
    *,
    parameter: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9baca73387f09f5353e93c5f8700bc045106f221b0359c2d131fbe7055705769(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c9ad8bc904ef45fbdb508b5a50c2dfc3a1b4e647fee04655b5392a8520e079e(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c541f89743bc296f16f4c020a2a70c5dc373b7354aa36161ab1482de47aeb6fe(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3a0503fe09a702f31a139eb8a7dfb556ff06b6c53476a4294840f14b231b11c(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d6cf7ea8214c4ca0a99eee21e0cf65fee0b65d6581d592e2d3d31b0952b82d5e(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c918962fb69ac22fe5c492c71097cef5730be8d3a6fdd704d0a953706262f01(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDialogflowCxFlowEventHandlersTriggerFulfillmentSetParameterActions]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e849e95ac9146804ad1cc766b09fdac80cb113b5fc45e4da4325aecd79c3bb9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee39d77d0d3a755ced9500b7843b711e233e1f5458838cf3e5f254227d056d77(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__645180431c81e6015f9b747ca228f3de8abb61a09f9c6aaca262bc6f8bdfe421(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__404abb45a68419b24509e89c3c666e1384d97c4fb58a267936d63a46cd84b790(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDialogflowCxFlowEventHandlersTriggerFulfillmentSetParameterActions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4895735831ff36aef22d4802ce53b60d5076c6af9ff3cd15c5d596ec4a1b6b1f(
    *,
    data_store_connections: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleDialogflowCxFlowKnowledgeConnectorSettingsDataStoreConnections, typing.Dict[builtins.str, typing.Any]]]]] = None,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    target_flow: typing.Optional[builtins.str] = None,
    target_page: typing.Optional[builtins.str] = None,
    trigger_fulfillment: typing.Optional[typing.Union[GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillment, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2db33e6c1852358223a4a1919e6bd2721a030a06c0bce5c4ff43e2cb603f9f0(
    *,
    data_store: typing.Optional[builtins.str] = None,
    data_store_type: typing.Optional[builtins.str] = None,
    document_processing_mode: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96860768c90bb930356f1e3ac037a4cfe9a0b188952139a39d40bebed5e4126f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5c02b6c4007dc4b93f138859d7e19ff65ffd93570a7b363a6ce748ba442aa5c(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d1585289b2b7da555eee8f15913541598350247153dcf605adc800dccb76bd3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__017aeb8599ae55a6ffd0d5d067e50419ab3fb8b5c13ceda047fb0954af3bde61(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d827aefacd7c573682da51af165f664a36cf2ed0de0de1a73acb5b7bb83e188e(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1909f8394c8d6380dec9fe6dcb10eaee50db66f51835a6bf2b9d855d945c9402(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDialogflowCxFlowKnowledgeConnectorSettingsDataStoreConnections]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0141c759169d740cc0cda2e699028e89811eb3f60fe520fe4ef7e2915546ecd6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4b80698f774ac7ee463f23a41e437324c7467aaa610d9d3140c3dbbf54f80d5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4e40cd3095a5d845e4691eb085178b7ed8753bc5a26590bd144c4fad4e60299(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3279b5d7c01ccf2b5a11cb5170756ca125fc208f151d2add4c9233a0eeb66279(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2f71b0de45fc46f13177a0438c5648b2c1e71b06c25e5d9cd8ee81109082932(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDialogflowCxFlowKnowledgeConnectorSettingsDataStoreConnections]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__553468fdfe39b122adbb174d9142692897748ece50a051bdbb684f55ed0528e5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__966823029217fd19a3729262f168c7cb08f49e6c3daf610c405f207064e7c97b(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleDialogflowCxFlowKnowledgeConnectorSettingsDataStoreConnections, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a11aca10931e6041e92881ba007f12227988048fdd33eee10b52a9737bce58cb(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c01d25c9744df665875024fd57a3aeb50c191eafabe1393fad3e72534683714(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88e4207fa49dec1138d1cb31b07baa445a32fc34d1d51a016a5070b681aaa216(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b8beb22dc061ba0fa9a28b27578276ba3bddb409e94df89b99276dbe16cdc52(
    value: typing.Optional[GoogleDialogflowCxFlowKnowledgeConnectorSettings],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61c09bd1713fba814cee6c32162a4065faaee6366df7a2dd9c3f7e007b839861(
    *,
    advanced_settings: typing.Optional[typing.Union[GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentAdvancedSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    conditional_cases: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentConditionalCases, typing.Dict[builtins.str, typing.Any]]]]] = None,
    enable_generative_fallback: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    messages: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentMessages, typing.Dict[builtins.str, typing.Any]]]]] = None,
    return_partial_responses: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    set_parameter_actions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentSetParameterActions, typing.Dict[builtins.str, typing.Any]]]]] = None,
    tag: typing.Optional[builtins.str] = None,
    webhook: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d27c1e3315ac786ad057f159b214ed632d9d24c28842b05e867e7c741784e9b0(
    *,
    dtmf_settings: typing.Optional[typing.Union[GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentAdvancedSettingsDtmfSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    logging_settings: typing.Optional[typing.Union[GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentAdvancedSettingsLoggingSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    speech_settings: typing.Optional[typing.Union[GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentAdvancedSettingsSpeechSettings, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ecf201bf5ef3ff8d12af6463226798015d1b6d371419d1fbe7799e0d41661e3(
    *,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    endpointing_timeout_duration: typing.Optional[builtins.str] = None,
    finish_digit: typing.Optional[builtins.str] = None,
    interdigit_timeout_duration: typing.Optional[builtins.str] = None,
    max_digits: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26fc93952bc0e8c19e688df7fa2f0220a11004d373ed44323512682ddded55a3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5141eec5c11f7ecc2ccfb926d7c613b68343f213218bcd90ce3740b768bc75f(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe1c696022530a728c2ba038a0184b2677ba8b5af9b5cc0b0ccb995e9c6f0dd1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ed8f48fcba0836be1f96495b016b188887020b6317ed9550b19257ad1d6bde5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d839e915331d8bf2bc6ec768f3c4eb33b0bbcd2dbc05d4d7f7f88a9338081d1c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a02d66f3bcd3895d6a7c12848a776ad08585789fa85f9a613e3036669db9ac97(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__453e822885b4998da7eb548d6d248ddfee6912ae1922e064ca42ba8d64fff390(
    value: typing.Optional[GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentAdvancedSettingsDtmfSettings],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9133c5c6eeee3c5e77e353fd96664574f8ba70f9bd6ec63190094796b4b23a66(
    *,
    enable_consent_based_redaction: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enable_interaction_logging: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enable_stackdriver_logging: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8256ffb535ab55f7080dd956c218b6ef7eac42b5c399a2a7433490e93cc835d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3abaf43708f51e71d6a9eb8781a9de7e6c882b9fb0189055d22e20851de3861b(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a51cdb22632e0ff830126024216f8b6dcdac1f3f77e1a5702a13405e727780f2(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b45a896cbfdc93041bb124f325b1399c13b5bc9e3484c76bd4d5901ee090e37(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0d73456de78cf99f30f036cf5c477369c6d21d44b698f503c3753355500a7c9(
    value: typing.Optional[GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentAdvancedSettingsLoggingSettings],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f7cc235c8ff5a76245800c191ddb02a6d4778cb17e9e418aed8854aebb31eeb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc0cad544b71343b72faf63639a34bfa5124ffb71583606c737b491742da5ed5(
    value: typing.Optional[GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentAdvancedSettings],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c880a72ba2e942a2e6f762c4b4ac83519f868dc0ea444055b19a16990d79936(
    *,
    endpointer_sensitivity: typing.Optional[jsii.Number] = None,
    models: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    no_speech_timeout: typing.Optional[builtins.str] = None,
    use_timeout_based_endpointing: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4128d2cc3ee905397ebcd8438fe38a7bb27730de3af5446a4245cdf3e1a3d4e0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__202f5caafe97df860ef041e9b31f617d610b3ddb037962fd9f47281c8c975d13(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a2ffa7919ea24f10179497728bef4521001bcc2cbddf357c1a0b0b278bd5612(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9303fc7d7f14b4b9c3db917f357a4556f8d79dc588e267a82a46aa59c7a378cd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea01611390474913569e29eeeacc75f8b169fbbd645c249d53f842848d917fc9(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4eff1b1d631b021134faa90955fc43116541ce38cf35629fede416632b81737d(
    value: typing.Optional[GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentAdvancedSettingsSpeechSettings],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c415dab972eed9d090cf49c4b658347c00a3bf803b4ce2bb055174aaa57866b8(
    *,
    cases: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1ec138620154f9a9e9aa2a079e65e4a4025f1091cd1e38e0e01258d3315cf1a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1d181a1fa30e4e6ce6a7acc5992646fb2a0b59059e4aef8ce5f7bd9dd2df639(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__82b3091048f4d51d8532425b23a17c88d4eb7b3e01967462ff1de319fb88f29c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15affd6185dbf94a3d761ca4bd59630d14584464234188ce06f6ca76d19dc8fe(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ecb4b60be1d0cad6c2027056951fa2207ba232b99f024aa7df84216a138efffc(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5bb0f62ff94a3249a3fcea65930f405c467e08f247019a4873b69a1bbdbc084(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentConditionalCases]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ca55a1bf56741348bfd6bff257da60aec962c96259a6f3f30d6d755e8dba2a2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f8a0e0cf9697d472539bcc0c2173e6e5a59f0584a52d74c18e0f221b9a19f0b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae31b66b4721fd4d36b0acff39f3d9efd5212c86bea2e5f01de94f6be394d104(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentConditionalCases]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f6a6bc532e6403fc912fbe2a036388695609a011a5b3f836de836afc6a284f5(
    *,
    channel: typing.Optional[builtins.str] = None,
    conversation_success: typing.Optional[typing.Union[GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentMessagesConversationSuccess, typing.Dict[builtins.str, typing.Any]]] = None,
    knowledge_info_card: typing.Optional[typing.Union[GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentMessagesKnowledgeInfoCard, typing.Dict[builtins.str, typing.Any]]] = None,
    live_agent_handoff: typing.Optional[typing.Union[GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentMessagesLiveAgentHandoff, typing.Dict[builtins.str, typing.Any]]] = None,
    output_audio_text: typing.Optional[typing.Union[GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentMessagesOutputAudioText, typing.Dict[builtins.str, typing.Any]]] = None,
    payload: typing.Optional[builtins.str] = None,
    play_audio: typing.Optional[typing.Union[GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentMessagesPlayAudio, typing.Dict[builtins.str, typing.Any]]] = None,
    telephony_transfer_call: typing.Optional[typing.Union[GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentMessagesTelephonyTransferCall, typing.Dict[builtins.str, typing.Any]]] = None,
    text: typing.Optional[typing.Union[GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentMessagesText, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14cd7102922e60646f31f1d75d74115844d03f54a06e7fe2441d19c8920faf8e(
    *,
    metadata: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4033ef7c0d319e14b3cdcd8afed07b3af344f0846815d11e96346ae0bdc03ee(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f44a196e5b84a41361554375fad0fa5a1832ae74ee114530a8cf7763e69b4030(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61625681278978bb556af655883541c87ba90741e383d68da2af1a841c02afdc(
    value: typing.Optional[GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentMessagesConversationSuccess],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8f2878fd3481953339f1c9a83bd7cb38551289e7a56c8ab0af196a38e232c3a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__165b64b80feda19c61604bd45681edff95b51b8db1b78cb3a4cb093cfe21ca59(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6a1043b02fabd859f0a577f961594d2d18b99b28b153a7e0939dae853196512(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c477cd966ca6f90275836dcca77bf135649148ee5fa9dac9fde5ec57a658e8bf(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8da5df974d7dc4a2d60d0db32a04c15fb43db614aa0d903ffe2e2e997b429c75(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3fbce1b1b4330e103528320ecb7ef6cd0e17befd49b5b6a6abbd70a27723a27(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f9e6d0d84bd1b3f11917e913f9a3790cc4bba68780a39c595324dc5208fb5d3(
    value: typing.Optional[GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentMessagesEndInteraction],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0bdd2e61f92789e8c1ae634e6fc22cea87a7a5e76d5409b46aa020805e658c26(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e58ef0648e803de0f6ad54fcdb3b29a5dd2ad5cb6a54813f4f01289fac87c8cb(
    value: typing.Optional[GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentMessagesKnowledgeInfoCard],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d6af67eb4efe099eca0491c5399e2b57eba1312cdfffdf37752af6c1c57dc947(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1cc99ab72aab37db27822fe17462f86b124276db04859f554d0836452d88d5e2(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28f5d9f7f6ca35d3a6348f6ccc46452837f4eb71d8fc7925ea7640899c4c3a64(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__414cbdf1466ae5d28187e4d1566c53e33efd9f070460f660e6ecfa200979c5cf(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__07bf1fbbe372506ef5942f52399a98760f21953854536830fa3e6eb0e305f38b(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a787d65125828ac0c89c33a09b1e5bfe479b1fb6d13924e665aef243cc539e1(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentMessages]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9d2187a3f51d016e83ef0586a8c75528af56d26a0173717d7d00ada2e31435c(
    *,
    metadata: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62de3b71663e780c7e1fe09707923bb8e2ace0b4c3b4565b6b4208cd6007a919(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__07263cc98fb9f102f38f0d4ab8b589f7fefbdbe0c9c7f383fd5bdc955e108682(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e503f332afabf467ee66c1469aec82784e02cf3084d93852e034645c8344081(
    value: typing.Optional[GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentMessagesLiveAgentHandoff],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__604a16fa6c641a22ff234206ba936b2beaf7f37e75c0398794ff9fe70cf690e5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6628aa239e76f57366d6bfdc8438aa7760680c590e8f9768d497ad3577de6ec(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6d38cc5de9e4a89d020c5f79d31e4a92e73824f7db312ab2c019e616a9f7df2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__745ec9fee7229bc241f4e1df64e9f038492ff195b07c2caac30c7e12e4e871fa(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db10fb5ec1fd173d4398a0cc30f361ff59df39beb47f4c0f7998e6f2de694aea(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8674ecea09a0e152c48b1e085d163eb3934247d34f7e55a9bb00cc2388277e7c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__997addcbfe45927c3dfb348d690e739e6297ae0c4237dc06bd08470f1ee228bb(
    value: typing.Optional[GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentMessagesMixedAudio],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9cee157f77d7f52bc96acf7ecf83e75f7ef114fb4f1ca136c7996278788e67c1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f92a49f44d1c9054235e38b7e44e3636265e89ac4af3bdaadc070b0a6f4f1b32(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b7284b7f8e93160927df17c6c55238304d8e00a942a5e31dcf2ec4c1f18cf5b4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__410ad1ee2f7b3329209fc5c5f5597a2120ba7078841b426bfaec4e1637df9a56(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9be1ffb9358f746fb89debd6e559f6d680f1e2dfc02270806f4c50c071772426(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0ba0b8c826f24181408e4da7c605851fc985f24247c2691fbe499dcbcb0867d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85b6a48b37b6716d9dadde9fbe09d8901b6ca1e5f625bad15089e0a4eda26119(
    value: typing.Optional[GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentMessagesMixedAudioSegments],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f580abc06de8355d78901540b820e50beeec9d07bad1cad42948a27ab75cf26(
    *,
    ssml: typing.Optional[builtins.str] = None,
    text: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__798e33e06758f3a4e7f51d02745e83391c1fc302c133d5eed3085ee2e223a5a2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__056f7f27d3e3e5d39ef984c18ae65c95eb1f160f687985a2c3123501b1fac513(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3795b9c9c09e4d847122c978a2c55f808591197cc922ae88c5bb9859b41b17ed(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a96f2d3ba9a5ea8ecde280f2710a9584b93002dd1808abf407954958be5f0642(
    value: typing.Optional[GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentMessagesOutputAudioText],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__030dc961255b053398c28345e67cca09d4ea8739108a20598544679129757531(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be495b72980c5399b0036df5ba3b68f9b220106106640b4cc7a47283ab4f4de7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1bf3940821ceea1106c96f20732ccfce25feeda3d6d3787ab56bd96d95753616(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83435ede2c4242be3414d53f8e58664b6e4cc491ebcea1bcb07b57240d12a8a0(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentMessages]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb7af42ca688f446ceaec9e314df249af25abc90bd24289883e99fb610fa70d3(
    *,
    audio_uri: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a483a732de5575059a233ab4f6920fe0f386645f8bec5f6bc63fbe4acb1d906(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa0927078debc3b96967bfa03c5c7539be570a83dbfb750c7da6236443e463e9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d6289eb7105b81d8760d5dd0d26886fd62337e54ba45ecb6093ad88f4a06f3b(
    value: typing.Optional[GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentMessagesPlayAudio],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8bbc41d76fcf87daa6a09e2c97c12703d1ee20353a5e7ca16f1665fd3e5c416c(
    *,
    phone_number: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5078bbe09e8c82bd96e6308fd6a47231e5d855263bfb324cdad9fb20e20300ca(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__807cf14d47bc48d30fd9671aeeaad39f218913168ae132cd540f3d7f7109f872(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__445e3519bede696544170ecc1ce808775dd347f18951d34a26c97f0983c1fce7(
    value: typing.Optional[GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentMessagesTelephonyTransferCall],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67da1257b0a85f5de0c2bcbc322d969004509dafa920ffa3f7189182c6d1a041(
    *,
    text: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d754b09cc0511620e725d816fe27749924ba15bb59be2dcdcf33a199c53bd93(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6fa5bf7fe80813977789f63a9ad51649be683435fff88f0a124377b002c70e6(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8a643ad1f283713a3ff9a4079c97fd14fd01f06c0e041adef9be9f82973c99a(
    value: typing.Optional[GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentMessagesText],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4757f40b0c6e0bc6864e9145ca411844af18da5ec61b4fa61eb55df9b992a5b3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8897a02c9d16749273ff1874fd575c50f639196949fd2c11da2862aab0a15527(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentConditionalCases, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5551c7c953a8f481f1ed6b54571d3fa8e7b750942674ace2b1f5207b6544810d(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentMessages, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61dab2c4af5f47879214e7134bfa2b3f086975b78078b9cc187ccda41efbc97c(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentSetParameterActions, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf575002abb7156167529652420b91e7e8e3c0ebc2cfbc43e5aa33adc02649e8(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54e070c194a5b9109dc7f906ad50aaa526881a46336dc04c65388679748faee3(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d875b0bd1a3b574cf2c6458f527ea3a1b1f1509a0c020c29acde249a4978dce(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31f8105c09537721a3d4acaf735e24ded8278b724bce1692282c3b6ab5b19837(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f6d583767b4acd854c392ffcddbfb23215ebb70520283915d7715a4f129cbb6(
    value: typing.Optional[GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillment],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__859c00631fe9a87037b70ec7d706d9d78447ca0fac0a2f207e9eff1f2bed5e25(
    *,
    parameter: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f59a07715588bb2e498c8aa0643276f7eb1d92666189d689d08d4f1afefc71a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f0c6a402d87f40831c9f8a9542818c46c70997c7ffc861043504ad7b48acef1(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19b92920d6e285342c2b6f78e4b89d3d58e87c7277ac61fd5a893a377c3192b4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed018cdab6df3b0898ae8140bacdb07eaf5a4bcfea9db7f4603867f79ea2892f(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1e7241fafd91d0e7640411347a40d725b4dcdbe78c36526de13493eb69d2227(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9079a67fbba5727e636d66a246e9de3cb13047e8c15ab6254175a9177d7ec52f(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentSetParameterActions]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52328e0613721df57d04da8c8713cd55194da0bae846e83dc193b4ca5ee53d93(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7dfa57edfa310ee4134e55445d3b44ea0a718df196f2fa01ef45e1877f3c0df8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a01a79cd86a4df215ea1730c7ff0ced8bbeb6131b1ce0e7b74c92d7a0e1659f8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8cb486d001ee2b1c1c6fcb871e9deac8226eb6892e7e68d7b8e8dad01f6ab66b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDialogflowCxFlowKnowledgeConnectorSettingsTriggerFulfillmentSetParameterActions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e11d2415d17184287951f07c3c59b5989b582c6777731b857475cbefa2994ab9(
    *,
    classification_threshold: typing.Optional[jsii.Number] = None,
    model_training_mode: typing.Optional[builtins.str] = None,
    model_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98d9f3909bba7513ded942dd49ab4eff31602cdb034f4a4e1475a92d9195e3cd(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45305366a1d242576564cf317b03d1a334294e16921345b493918e93aecceff7(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__536cbd1264bd06bfdfe3cee75d9622418afef8311158512d4f56b6ab9158e3f8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dbe96da0683e88b188041d7de4c92fed18d30c2e19f30792d01ac81a7e8fc06f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__524f25a80f58940c6773cd38d1d4a7c6ddb98c11023b57dd08686d71d4bec644(
    value: typing.Optional[GoogleDialogflowCxFlowNluSettings],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0210a03cea17a8ef6bb6c8d12573cd1b0d7140688721c228c725071420680dd6(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0e68db04b76164173d2591ddd75bb1b9b052a340e3f358976041e891232cfc2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c8fa4d3bd2d4d417cd91617f1a451745bf4aaf04d58d7966be4fba2c6597fe3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d5975630e9faa60ef9b199ec40a0b2873f5df8a921e7f852dabdc8a78073309(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e778f648906def1b0b98d5164ec361e201a715e15a0d72467b7788a670fc5c4d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86c6d5b814a990c8b13a0674f1e520f123196a9fc67d10ff966cfed6d664ab5a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDialogflowCxFlowTimeouts]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d1a18960d79eb590c9d5bf3e090bd2e010515560266b7c63ff53264e0f013b1(
    *,
    condition: typing.Optional[builtins.str] = None,
    intent: typing.Optional[builtins.str] = None,
    target_flow: typing.Optional[builtins.str] = None,
    target_page: typing.Optional[builtins.str] = None,
    trigger_fulfillment: typing.Optional[typing.Union[GoogleDialogflowCxFlowTransitionRoutesTriggerFulfillment, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c658a26b791ed47c005526f0d203bf77af0ce5f404c11ebc43fd87ecac58b40b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3785a2a26b46925c4961926dbf735621325bd370269361e64e4cae714adf64c(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72390c857e2ae72ecbbe1a54bb412b4ff281d146112ca0926eef1c03e9ab9c40(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bef78f412e276f63bb4c9db73a3c134a65b4d12146688888d6a4695ad3ac274b(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be10637d5d8fa7172423bd8f96a2561a939265c1e9b1d560cbb735def4faa7a2(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4831c1a17de10c1ab5840826b85ccb8471666de0b3bafe39b6002b027cc2f31(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDialogflowCxFlowTransitionRoutes]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__48ac555298c8903d2371e18de384242e6abe071a26c75bfecc87cdb684fc1f5b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76e46873b24a3efeb8ec6f6a61f81217f1e21900852c2da220810827b27be97d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a7bbd5463bb362fe073852100eb5bc655db95f2128105531a3af0073f278523b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76d249e51248c27f926d6d592e9b4877379d8f9d5c09d9cc691e3dc24dab1974(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ec782606f320f8dceb8e53942677095abfe92dc2acf5f176bf57abeb0a5f8ad(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c71428de0494ae2981349f4c2a95e9ba77bf5b1e6a1b3ec8c23594a99918944a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDialogflowCxFlowTransitionRoutes]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__944315f63373bd1968029dfa9b00946a674228d84fcc82289742d14c69a9a569(
    *,
    conditional_cases: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleDialogflowCxFlowTransitionRoutesTriggerFulfillmentConditionalCases, typing.Dict[builtins.str, typing.Any]]]]] = None,
    messages: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleDialogflowCxFlowTransitionRoutesTriggerFulfillmentMessages, typing.Dict[builtins.str, typing.Any]]]]] = None,
    return_partial_responses: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    set_parameter_actions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleDialogflowCxFlowTransitionRoutesTriggerFulfillmentSetParameterActions, typing.Dict[builtins.str, typing.Any]]]]] = None,
    tag: typing.Optional[builtins.str] = None,
    webhook: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__073564628f5e4b1c595d0ca2ef50b8c8b21b6fcd3d9829ed222747ee2033d788(
    *,
    cases: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dccd900a9d9cd7c15f9a0c287a2f99de34596f9a2f5812f158211134371b883f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d64b4fa477655ece9114be172123489468135e33629d889949ef5b326669db33(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11e9aac43e2eaf7698d6c27ae81848e22e314ec08d9dc72e608142031ca45f04(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc763207d105bcd2b733520647fced1e0d09ea742305106dcf6f6d380450b38a(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce5f923d4c327212d62c992838d955b10993908e731036936ae74e3e27b5d7ca(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b94ce98d4da9e0fb393f8633e49995caf36570b625f581b6bc2c1c719a1e6000(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDialogflowCxFlowTransitionRoutesTriggerFulfillmentConditionalCases]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__84305fb27b217397ad3c42dba23ed2b0f210bab4cbe3d6933666a8a28542afa3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f43465b9e291c5c5b7730cac16168be734ee87b24422e2c0956f46ae12735ef6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69319f6b9393fa10bdaed0904605aae7b5596401b7f85dbab7ab898f27bedee3(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDialogflowCxFlowTransitionRoutesTriggerFulfillmentConditionalCases]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65436ee4b59d66753768513811493c2a9d9e47b34fd247b3f479f85953b0e120(
    *,
    channel: typing.Optional[builtins.str] = None,
    conversation_success: typing.Optional[typing.Union[GoogleDialogflowCxFlowTransitionRoutesTriggerFulfillmentMessagesConversationSuccess, typing.Dict[builtins.str, typing.Any]]] = None,
    live_agent_handoff: typing.Optional[typing.Union[GoogleDialogflowCxFlowTransitionRoutesTriggerFulfillmentMessagesLiveAgentHandoff, typing.Dict[builtins.str, typing.Any]]] = None,
    output_audio_text: typing.Optional[typing.Union[GoogleDialogflowCxFlowTransitionRoutesTriggerFulfillmentMessagesOutputAudioText, typing.Dict[builtins.str, typing.Any]]] = None,
    payload: typing.Optional[builtins.str] = None,
    play_audio: typing.Optional[typing.Union[GoogleDialogflowCxFlowTransitionRoutesTriggerFulfillmentMessagesPlayAudio, typing.Dict[builtins.str, typing.Any]]] = None,
    telephony_transfer_call: typing.Optional[typing.Union[GoogleDialogflowCxFlowTransitionRoutesTriggerFulfillmentMessagesTelephonyTransferCall, typing.Dict[builtins.str, typing.Any]]] = None,
    text: typing.Optional[typing.Union[GoogleDialogflowCxFlowTransitionRoutesTriggerFulfillmentMessagesText, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__443cb296068677570ca31681b7a23fce70b15134c83624ecdfa4d4d7d48c4e54(
    *,
    metadata: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a62fef97b7856041a1713b9b5ae779fb408afd1be81ba4f16c1ba424089cb264(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ada7298689527b5c065cde8e48c22db97db2e508e922c6fd36a87403bf090ce(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5103b2b839d9b966e63faeba0e1d3965459265a261e7c5f637daa589b15b432f(
    value: typing.Optional[GoogleDialogflowCxFlowTransitionRoutesTriggerFulfillmentMessagesConversationSuccess],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7435871870af685282002420434c13db7b6579027b6925f2e68d8de4a5c3fc9e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6be189241fff7bf38c1fca21ad4f28dc6cccdf2f4f554aaea715de229737a76e(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ae7d59f0511c56d7eb840244429c79966ee48fc81349d5f84f2319907031903(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9a46f9994035fdfbc69bb83a7a8c239a963e6e9eecfe39d1df33a45f82ec229(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3eda6061a4d7d2bdf6484af0aac95aaeab9ba650ee6cb0480fade59673b8fade(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25a4af56b921e555a8e66e8345e3e8709927bd080ce8209d365603fa341a6b54(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDialogflowCxFlowTransitionRoutesTriggerFulfillmentMessages]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__037577492ee768c84baa425a81e9da4bed7eca07320eb112467dd187e32ab818(
    *,
    metadata: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29c23b527aedf7f56b05ebd207e8bf44b96dead12716c5f2ad05f70660f45f63(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3ec186ffc12bc91a22be609e0440c45a7148cd2adf3d8455c03443084b991c9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b99adafea9b3ca2b24c5226c7aed674a5a7acb0b2cf866a9968359adc9b2328(
    value: typing.Optional[GoogleDialogflowCxFlowTransitionRoutesTriggerFulfillmentMessagesLiveAgentHandoff],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__754cf0eb58c8b5554cec150e39db7d963e7b5a5ccab6c9ea5619b02e0953ac39(
    *,
    ssml: typing.Optional[builtins.str] = None,
    text: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f98db449db3742aa31405a7fb2f355780ca03773173b8e1e5094869b9a3e7fb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3de77f51bd45be075e048dd6cd7856fca94294384103b6e481857cee90bce522(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b51f673294b2e4d47f56a817c0f960b1ecaef6d00f7708f6309d8e6488be465(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b36fe60a0dd9d4a7f3180cdb0e06de888cd52e708d8c6a2b52160de645883ee6(
    value: typing.Optional[GoogleDialogflowCxFlowTransitionRoutesTriggerFulfillmentMessagesOutputAudioText],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e09d82d13a056100809df1747e9032e7cff75fcd0fd2e85fd7cac7fe514183f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8690d15b9137257d6f9ee9213315231c41ec83f5b4527dd525e724ffc5c480ee(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fccc74f5e06ef36a07f83277c279bc200de603b16835ff1e70a68b0d957c5334(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__453d82510f9adc9db614143cd517ba4f565b2a6db300b9f8a6faedcdb1372282(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDialogflowCxFlowTransitionRoutesTriggerFulfillmentMessages]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aeaa482bfaa5dfaad614fee2fef6fef4103da1f019699ea086f8687451a0debb(
    *,
    audio_uri: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b742708f1595104a689aa6369edb59ed9c8fcbb51ce27e58cc79fc6a27527fb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53fdde3b49c83d9a3cbd9f2f9efbefcf3b82f2fa111960ae5924e9c818cdd315(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf03831b63f25ea1a0403eaadd1fbd9036d0e7001aba80950ccb6658ab717806(
    value: typing.Optional[GoogleDialogflowCxFlowTransitionRoutesTriggerFulfillmentMessagesPlayAudio],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e186a2b1ef179a0437ddfd4ae0f6eca9225a010c0d1c190a0b679f3c0e8e3e4(
    *,
    phone_number: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57331cb9c6069d413867ce93e466e0c1ab9e4abab3d9a67e5aa4a394dff4fca7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ab54ecaf8c1ed91aa519e07af5b72d0e7cfed9b66a102d9e11c0b00beed5e7f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3cf35e97d6bbfc5664a8f38870f4d775a25938b2e2fa5e4b158d016e49b7b04c(
    value: typing.Optional[GoogleDialogflowCxFlowTransitionRoutesTriggerFulfillmentMessagesTelephonyTransferCall],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0153409442fb161b628945747122cdf8ddc6e15a3d6d3a0948bc10c7a26885f6(
    *,
    text: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a06dd4513f065ad9309d0a96051645e8a1e25667073f4ca1e04b988bc1877e2e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4129b5304583b960d5f0beec820380ae650c062c078679046d54b3e60db3a84c(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50f2da856a359f6e13479ee354302498446f8687051668ea56ea87c957f0b2cb(
    value: typing.Optional[GoogleDialogflowCxFlowTransitionRoutesTriggerFulfillmentMessagesText],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7dbb19ced0b6c9b1d22198ba4a7f0983290defd105af87f66c03662cda69e461(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0582dbdbcdfcc015af334e2c55df9c543eb7cc8aab2c8f879e6ac28e82843b26(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleDialogflowCxFlowTransitionRoutesTriggerFulfillmentConditionalCases, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b0b934ff43ca7625a4f7b3d2b74223683bab64ed983cdb10e1e244620b05270(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleDialogflowCxFlowTransitionRoutesTriggerFulfillmentMessages, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__189b19022a0a37d65f611da92ce86132c15753dff6e3d735ffc2a5bb2f5f7d9e(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleDialogflowCxFlowTransitionRoutesTriggerFulfillmentSetParameterActions, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3bc3ed29a6fe1a6c56df7a77a6dafca943bcfc091afa8b6d48041ad775e8b814(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9f70849da3e966fdf6b96ed7433d72b3121157e46ef03cb37bcc66ac4dd2b01(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aeee2472db9caa2d47a89521789e8b35f36e94f69faeb5e8e3a183a96628c091(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__220977d5a118b7da09035631babbb52080bd1f81cc737ffa8743eebdfbed6d4b(
    value: typing.Optional[GoogleDialogflowCxFlowTransitionRoutesTriggerFulfillment],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64ce5b4c1ad6bc6fd3c99bb3cb134de4b9fbc58d10cb9c822cba3d1ab87681a4(
    *,
    parameter: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1009379d86a81f455f149be928b5167054ab533b589dbe561f7f79d4c5d25510(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d630eb93806d039a7a3be4015b25441367e050cb2051227e0697b8350fa2b188(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3678a2a493a46d2caed937bb0e6d6d7d7ab5f74e63263abbd8de24e174040145(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db8186aeed4322c4b8712a7e1d8ae779695931b38a479f99a2fee24571c061cf(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65ccf02e547b9c9c1c79f52b2913957dae39dd5af3cf05dc2598d8c185979bfd(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__23361771f23ebe9a1ed4c64c22b1f9725c28b96f39af11c1428dd0a53a053b33(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDialogflowCxFlowTransitionRoutesTriggerFulfillmentSetParameterActions]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__918e7e9ba3fde7d211de3237538cae953afc374dedfa658ae13f2ece422f5bb8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b67d67b07417c3d48974e8f75da3e2985e69a745d9600461aba776c5232c103d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b65d59229d975c4b30135574d2a00ab712add1d09ac284b6f5f22b4fc3ed795(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bbf8ba72500a2f738831af42f750ba19782166ea872ad100c0378e20368d07e3(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDialogflowCxFlowTransitionRoutesTriggerFulfillmentSetParameterActions]],
) -> None:
    """Type checking stubs"""
    pass
