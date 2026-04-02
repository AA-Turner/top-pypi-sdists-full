r'''
# `google_dialogflow_conversation_profile`

Refer to the Terraform Registry for docs: [`google_dialogflow_conversation_profile`](https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile).
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


class GoogleDialogflowConversationProfile(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDialogflowConversationProfile.GoogleDialogflowConversationProfile",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile google_dialogflow_conversation_profile}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        display_name: builtins.str,
        location: builtins.str,
        automated_agent_config: typing.Optional[typing.Union["GoogleDialogflowConversationProfileAutomatedAgentConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        human_agent_assistant_config: typing.Optional[typing.Union["GoogleDialogflowConversationProfileHumanAgentAssistantConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        human_agent_handoff_config: typing.Optional[typing.Union["GoogleDialogflowConversationProfileHumanAgentHandoffConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        language_code: typing.Optional[builtins.str] = None,
        logging_config: typing.Optional[typing.Union["GoogleDialogflowConversationProfileLoggingConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        new_message_event_notification_config: typing.Optional[typing.Union["GoogleDialogflowConversationProfileNewMessageEventNotificationConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        notification_config: typing.Optional[typing.Union["GoogleDialogflowConversationProfileNotificationConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        project: typing.Optional[builtins.str] = None,
        security_settings: typing.Optional[builtins.str] = None,
        stt_config: typing.Optional[typing.Union["GoogleDialogflowConversationProfileSttConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["GoogleDialogflowConversationProfileTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        time_zone: typing.Optional[builtins.str] = None,
        tts_config: typing.Optional[typing.Union["GoogleDialogflowConversationProfileTtsConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile google_dialogflow_conversation_profile} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param display_name: Required. Human readable name for this profile. Max length 1024 bytes. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#display_name GoogleDialogflowConversationProfile#display_name}
        :param location: desc. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#location GoogleDialogflowConversationProfile#location}
        :param automated_agent_config: automated_agent_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#automated_agent_config GoogleDialogflowConversationProfile#automated_agent_config}
        :param human_agent_assistant_config: human_agent_assistant_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#human_agent_assistant_config GoogleDialogflowConversationProfile#human_agent_assistant_config}
        :param human_agent_handoff_config: human_agent_handoff_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#human_agent_handoff_config GoogleDialogflowConversationProfile#human_agent_handoff_config}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#id GoogleDialogflowConversationProfile#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param language_code: Language code for the conversation profile. This should be a BCP-47 language tag. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#language_code GoogleDialogflowConversationProfile#language_code}
        :param logging_config: logging_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#logging_config GoogleDialogflowConversationProfile#logging_config}
        :param new_message_event_notification_config: new_message_event_notification_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#new_message_event_notification_config GoogleDialogflowConversationProfile#new_message_event_notification_config}
        :param notification_config: notification_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#notification_config GoogleDialogflowConversationProfile#notification_config}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#project GoogleDialogflowConversationProfile#project}.
        :param security_settings: Name of the CX SecuritySettings reference for the agent. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#security_settings GoogleDialogflowConversationProfile#security_settings}
        :param stt_config: stt_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#stt_config GoogleDialogflowConversationProfile#stt_config}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#timeouts GoogleDialogflowConversationProfile#timeouts}
        :param time_zone: The time zone of this conversational profile. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#time_zone GoogleDialogflowConversationProfile#time_zone}
        :param tts_config: tts_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#tts_config GoogleDialogflowConversationProfile#tts_config}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a17f873d89d667612aaa984f37ab0b0bf78386a3f82af16cc699b733adfaf7b)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = GoogleDialogflowConversationProfileConfig(
            display_name=display_name,
            location=location,
            automated_agent_config=automated_agent_config,
            human_agent_assistant_config=human_agent_assistant_config,
            human_agent_handoff_config=human_agent_handoff_config,
            id=id,
            language_code=language_code,
            logging_config=logging_config,
            new_message_event_notification_config=new_message_event_notification_config,
            notification_config=notification_config,
            project=project,
            security_settings=security_settings,
            stt_config=stt_config,
            timeouts=timeouts,
            time_zone=time_zone,
            tts_config=tts_config,
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
        '''Generates CDKTF code for importing a GoogleDialogflowConversationProfile resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the GoogleDialogflowConversationProfile to import.
        :param import_from_id: The id of the existing GoogleDialogflowConversationProfile that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the GoogleDialogflowConversationProfile to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c515b686347fa542215cc131657c8047591e51db862439506ba75a3d36982ed9)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putAutomatedAgentConfig")
    def put_automated_agent_config(
        self,
        *,
        agent: builtins.str,
        session_ttl: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param agent: ID of the Dialogflow agent environment to use. Expects the format "projects//locations//agent/environments/". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#agent GoogleDialogflowConversationProfile#agent}
        :param session_ttl: Configure lifetime of the Dialogflow session. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#session_ttl GoogleDialogflowConversationProfile#session_ttl}
        '''
        value = GoogleDialogflowConversationProfileAutomatedAgentConfig(
            agent=agent, session_ttl=session_ttl
        )

        return typing.cast(None, jsii.invoke(self, "putAutomatedAgentConfig", [value]))

    @jsii.member(jsii_name="putHumanAgentAssistantConfig")
    def put_human_agent_assistant_config(
        self,
        *,
        end_user_suggestion_config: typing.Optional[typing.Union["GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        human_agent_suggestion_config: typing.Optional[typing.Union["GoogleDialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        message_analysis_config: typing.Optional[typing.Union["GoogleDialogflowConversationProfileHumanAgentAssistantConfigMessageAnalysisConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        notification_config: typing.Optional[typing.Union["GoogleDialogflowConversationProfileHumanAgentAssistantConfigNotificationConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param end_user_suggestion_config: end_user_suggestion_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#end_user_suggestion_config GoogleDialogflowConversationProfile#end_user_suggestion_config}
        :param human_agent_suggestion_config: human_agent_suggestion_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#human_agent_suggestion_config GoogleDialogflowConversationProfile#human_agent_suggestion_config}
        :param message_analysis_config: message_analysis_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#message_analysis_config GoogleDialogflowConversationProfile#message_analysis_config}
        :param notification_config: notification_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#notification_config GoogleDialogflowConversationProfile#notification_config}
        '''
        value = GoogleDialogflowConversationProfileHumanAgentAssistantConfig(
            end_user_suggestion_config=end_user_suggestion_config,
            human_agent_suggestion_config=human_agent_suggestion_config,
            message_analysis_config=message_analysis_config,
            notification_config=notification_config,
        )

        return typing.cast(None, jsii.invoke(self, "putHumanAgentAssistantConfig", [value]))

    @jsii.member(jsii_name="putHumanAgentHandoffConfig")
    def put_human_agent_handoff_config(
        self,
        *,
        live_person_config: typing.Optional[typing.Union["GoogleDialogflowConversationProfileHumanAgentHandoffConfigLivePersonConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param live_person_config: live_person_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#live_person_config GoogleDialogflowConversationProfile#live_person_config}
        '''
        value = GoogleDialogflowConversationProfileHumanAgentHandoffConfig(
            live_person_config=live_person_config
        )

        return typing.cast(None, jsii.invoke(self, "putHumanAgentHandoffConfig", [value]))

    @jsii.member(jsii_name="putLoggingConfig")
    def put_logging_config(
        self,
        *,
        enable_stackdriver_logging: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param enable_stackdriver_logging: Whether to log conversation events. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#enable_stackdriver_logging GoogleDialogflowConversationProfile#enable_stackdriver_logging}
        '''
        value = GoogleDialogflowConversationProfileLoggingConfig(
            enable_stackdriver_logging=enable_stackdriver_logging
        )

        return typing.cast(None, jsii.invoke(self, "putLoggingConfig", [value]))

    @jsii.member(jsii_name="putNewMessageEventNotificationConfig")
    def put_new_message_event_notification_config(
        self,
        *,
        message_format: typing.Optional[builtins.str] = None,
        topic: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param message_format: Format of the message Possible values: ["MESSAGE_FORMAT_UNSPECIFIED", "PROTO", "JSON"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#message_format GoogleDialogflowConversationProfile#message_format}
        :param topic: Name of the Pub/Sub topic to publish conversation events. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#topic GoogleDialogflowConversationProfile#topic}
        '''
        value = GoogleDialogflowConversationProfileNewMessageEventNotificationConfig(
            message_format=message_format, topic=topic
        )

        return typing.cast(None, jsii.invoke(self, "putNewMessageEventNotificationConfig", [value]))

    @jsii.member(jsii_name="putNotificationConfig")
    def put_notification_config(
        self,
        *,
        message_format: typing.Optional[builtins.str] = None,
        topic: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param message_format: Format of the message Possible values: ["MESSAGE_FORMAT_UNSPECIFIED", "PROTO", "JSON"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#message_format GoogleDialogflowConversationProfile#message_format}
        :param topic: Name of the Pub/Sub topic to publish conversation events. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#topic GoogleDialogflowConversationProfile#topic}
        '''
        value = GoogleDialogflowConversationProfileNotificationConfig(
            message_format=message_format, topic=topic
        )

        return typing.cast(None, jsii.invoke(self, "putNotificationConfig", [value]))

    @jsii.member(jsii_name="putSttConfig")
    def put_stt_config(
        self,
        *,
        audio_encoding: typing.Optional[builtins.str] = None,
        enable_word_info: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        language_code: typing.Optional[builtins.str] = None,
        model: typing.Optional[builtins.str] = None,
        sample_rate_hertz: typing.Optional[jsii.Number] = None,
        speech_model_variant: typing.Optional[builtins.str] = None,
        use_timeout_based_endpointing: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param audio_encoding: Audio encoding of the audio content to process. Possible values: ["AUDIO_ENCODING_UNSPECIFIED", "AUDIO_ENCODING_LINEAR_16", "AUDIO_ENCODING_FLAC", "AUDIO_ENCODING_MULAW", "AUDIO_ENCODING_AMR", "AUDIO_ENCODING_AMR_WB", "AUDIO_ENCODING_OGG_OPUS", "AUDIOENCODING_SPEEX_WITH_HEADER_BYTE"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#audio_encoding GoogleDialogflowConversationProfile#audio_encoding}
        :param enable_word_info: If true, Dialogflow returns SpeechWordInfo in StreamingRecognitionResult with information about the recognized speech words. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#enable_word_info GoogleDialogflowConversationProfile#enable_word_info}
        :param language_code: The language of the supplied audio. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#language_code GoogleDialogflowConversationProfile#language_code}
        :param model: Which Speech model to select. Leave this field unspecified to use Agent Speech settings for model selection. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#model GoogleDialogflowConversationProfile#model}
        :param sample_rate_hertz: Sample rate (in Hertz) of the audio content sent in the query. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#sample_rate_hertz GoogleDialogflowConversationProfile#sample_rate_hertz}
        :param speech_model_variant: The speech model used in speech to text. Possible values: ["SPEECH_MODEL_VARIANT_UNSPECIFIED", "USE_BEST_AVAILABLE", "USE_STANDARD", "USE_ENHANCED"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#speech_model_variant GoogleDialogflowConversationProfile#speech_model_variant}
        :param use_timeout_based_endpointing: Use timeout based endpointing, interpreting endpointer sensitivy as seconds of timeout value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#use_timeout_based_endpointing GoogleDialogflowConversationProfile#use_timeout_based_endpointing}
        '''
        value = GoogleDialogflowConversationProfileSttConfig(
            audio_encoding=audio_encoding,
            enable_word_info=enable_word_info,
            language_code=language_code,
            model=model,
            sample_rate_hertz=sample_rate_hertz,
            speech_model_variant=speech_model_variant,
            use_timeout_based_endpointing=use_timeout_based_endpointing,
        )

        return typing.cast(None, jsii.invoke(self, "putSttConfig", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#create GoogleDialogflowConversationProfile#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#delete GoogleDialogflowConversationProfile#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#update GoogleDialogflowConversationProfile#update}.
        '''
        value = GoogleDialogflowConversationProfileTimeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="putTtsConfig")
    def put_tts_config(
        self,
        *,
        effects_profile_id: typing.Optional[typing.Sequence[builtins.str]] = None,
        pitch: typing.Optional[jsii.Number] = None,
        speaking_rate: typing.Optional[jsii.Number] = None,
        voice: typing.Optional[typing.Union["GoogleDialogflowConversationProfileTtsConfigVoice", typing.Dict[builtins.str, typing.Any]]] = None,
        volume_gain_db: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param effects_profile_id: An identifier which selects 'audio effects' profiles that are applied on (post synthesized) text to speech. Effects are applied on top of each other in the order they are given. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#effects_profile_id GoogleDialogflowConversationProfile#effects_profile_id}
        :param pitch: Speaking pitch, in the range [-20.0, 20.0]. 20 means increase 20 semitones from the original pitch. -20 means decrease 20 semitones from the original pitch. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#pitch GoogleDialogflowConversationProfile#pitch}
        :param speaking_rate: Speaking rate/speed, in the range [0.25, 4.0]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#speaking_rate GoogleDialogflowConversationProfile#speaking_rate}
        :param voice: voice block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#voice GoogleDialogflowConversationProfile#voice}
        :param volume_gain_db: Volume gain (in dB) of the normal native volume supported by the specific voice. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#volume_gain_db GoogleDialogflowConversationProfile#volume_gain_db}
        '''
        value = GoogleDialogflowConversationProfileTtsConfig(
            effects_profile_id=effects_profile_id,
            pitch=pitch,
            speaking_rate=speaking_rate,
            voice=voice,
            volume_gain_db=volume_gain_db,
        )

        return typing.cast(None, jsii.invoke(self, "putTtsConfig", [value]))

    @jsii.member(jsii_name="resetAutomatedAgentConfig")
    def reset_automated_agent_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAutomatedAgentConfig", []))

    @jsii.member(jsii_name="resetHumanAgentAssistantConfig")
    def reset_human_agent_assistant_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHumanAgentAssistantConfig", []))

    @jsii.member(jsii_name="resetHumanAgentHandoffConfig")
    def reset_human_agent_handoff_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHumanAgentHandoffConfig", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetLanguageCode")
    def reset_language_code(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLanguageCode", []))

    @jsii.member(jsii_name="resetLoggingConfig")
    def reset_logging_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLoggingConfig", []))

    @jsii.member(jsii_name="resetNewMessageEventNotificationConfig")
    def reset_new_message_event_notification_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNewMessageEventNotificationConfig", []))

    @jsii.member(jsii_name="resetNotificationConfig")
    def reset_notification_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNotificationConfig", []))

    @jsii.member(jsii_name="resetProject")
    def reset_project(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProject", []))

    @jsii.member(jsii_name="resetSecuritySettings")
    def reset_security_settings(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSecuritySettings", []))

    @jsii.member(jsii_name="resetSttConfig")
    def reset_stt_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSttConfig", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

    @jsii.member(jsii_name="resetTimeZone")
    def reset_time_zone(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeZone", []))

    @jsii.member(jsii_name="resetTtsConfig")
    def reset_tts_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTtsConfig", []))

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
    @jsii.member(jsii_name="automatedAgentConfig")
    def automated_agent_config(
        self,
    ) -> "GoogleDialogflowConversationProfileAutomatedAgentConfigOutputReference":
        return typing.cast("GoogleDialogflowConversationProfileAutomatedAgentConfigOutputReference", jsii.get(self, "automatedAgentConfig"))

    @builtins.property
    @jsii.member(jsii_name="humanAgentAssistantConfig")
    def human_agent_assistant_config(
        self,
    ) -> "GoogleDialogflowConversationProfileHumanAgentAssistantConfigOutputReference":
        return typing.cast("GoogleDialogflowConversationProfileHumanAgentAssistantConfigOutputReference", jsii.get(self, "humanAgentAssistantConfig"))

    @builtins.property
    @jsii.member(jsii_name="humanAgentHandoffConfig")
    def human_agent_handoff_config(
        self,
    ) -> "GoogleDialogflowConversationProfileHumanAgentHandoffConfigOutputReference":
        return typing.cast("GoogleDialogflowConversationProfileHumanAgentHandoffConfigOutputReference", jsii.get(self, "humanAgentHandoffConfig"))

    @builtins.property
    @jsii.member(jsii_name="loggingConfig")
    def logging_config(
        self,
    ) -> "GoogleDialogflowConversationProfileLoggingConfigOutputReference":
        return typing.cast("GoogleDialogflowConversationProfileLoggingConfigOutputReference", jsii.get(self, "loggingConfig"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="newMessageEventNotificationConfig")
    def new_message_event_notification_config(
        self,
    ) -> "GoogleDialogflowConversationProfileNewMessageEventNotificationConfigOutputReference":
        return typing.cast("GoogleDialogflowConversationProfileNewMessageEventNotificationConfigOutputReference", jsii.get(self, "newMessageEventNotificationConfig"))

    @builtins.property
    @jsii.member(jsii_name="notificationConfig")
    def notification_config(
        self,
    ) -> "GoogleDialogflowConversationProfileNotificationConfigOutputReference":
        return typing.cast("GoogleDialogflowConversationProfileNotificationConfigOutputReference", jsii.get(self, "notificationConfig"))

    @builtins.property
    @jsii.member(jsii_name="sttConfig")
    def stt_config(
        self,
    ) -> "GoogleDialogflowConversationProfileSttConfigOutputReference":
        return typing.cast("GoogleDialogflowConversationProfileSttConfigOutputReference", jsii.get(self, "sttConfig"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "GoogleDialogflowConversationProfileTimeoutsOutputReference":
        return typing.cast("GoogleDialogflowConversationProfileTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="ttsConfig")
    def tts_config(
        self,
    ) -> "GoogleDialogflowConversationProfileTtsConfigOutputReference":
        return typing.cast("GoogleDialogflowConversationProfileTtsConfigOutputReference", jsii.get(self, "ttsConfig"))

    @builtins.property
    @jsii.member(jsii_name="automatedAgentConfigInput")
    def automated_agent_config_input(
        self,
    ) -> typing.Optional["GoogleDialogflowConversationProfileAutomatedAgentConfig"]:
        return typing.cast(typing.Optional["GoogleDialogflowConversationProfileAutomatedAgentConfig"], jsii.get(self, "automatedAgentConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="displayNameInput")
    def display_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "displayNameInput"))

    @builtins.property
    @jsii.member(jsii_name="humanAgentAssistantConfigInput")
    def human_agent_assistant_config_input(
        self,
    ) -> typing.Optional["GoogleDialogflowConversationProfileHumanAgentAssistantConfig"]:
        return typing.cast(typing.Optional["GoogleDialogflowConversationProfileHumanAgentAssistantConfig"], jsii.get(self, "humanAgentAssistantConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="humanAgentHandoffConfigInput")
    def human_agent_handoff_config_input(
        self,
    ) -> typing.Optional["GoogleDialogflowConversationProfileHumanAgentHandoffConfig"]:
        return typing.cast(typing.Optional["GoogleDialogflowConversationProfileHumanAgentHandoffConfig"], jsii.get(self, "humanAgentHandoffConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="languageCodeInput")
    def language_code_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "languageCodeInput"))

    @builtins.property
    @jsii.member(jsii_name="locationInput")
    def location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "locationInput"))

    @builtins.property
    @jsii.member(jsii_name="loggingConfigInput")
    def logging_config_input(
        self,
    ) -> typing.Optional["GoogleDialogflowConversationProfileLoggingConfig"]:
        return typing.cast(typing.Optional["GoogleDialogflowConversationProfileLoggingConfig"], jsii.get(self, "loggingConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="newMessageEventNotificationConfigInput")
    def new_message_event_notification_config_input(
        self,
    ) -> typing.Optional["GoogleDialogflowConversationProfileNewMessageEventNotificationConfig"]:
        return typing.cast(typing.Optional["GoogleDialogflowConversationProfileNewMessageEventNotificationConfig"], jsii.get(self, "newMessageEventNotificationConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="notificationConfigInput")
    def notification_config_input(
        self,
    ) -> typing.Optional["GoogleDialogflowConversationProfileNotificationConfig"]:
        return typing.cast(typing.Optional["GoogleDialogflowConversationProfileNotificationConfig"], jsii.get(self, "notificationConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="securitySettingsInput")
    def security_settings_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "securitySettingsInput"))

    @builtins.property
    @jsii.member(jsii_name="sttConfigInput")
    def stt_config_input(
        self,
    ) -> typing.Optional["GoogleDialogflowConversationProfileSttConfig"]:
        return typing.cast(typing.Optional["GoogleDialogflowConversationProfileSttConfig"], jsii.get(self, "sttConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleDialogflowConversationProfileTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleDialogflowConversationProfileTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="timeZoneInput")
    def time_zone_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "timeZoneInput"))

    @builtins.property
    @jsii.member(jsii_name="ttsConfigInput")
    def tts_config_input(
        self,
    ) -> typing.Optional["GoogleDialogflowConversationProfileTtsConfig"]:
        return typing.cast(typing.Optional["GoogleDialogflowConversationProfileTtsConfig"], jsii.get(self, "ttsConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="displayName")
    def display_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "displayName"))

    @display_name.setter
    def display_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ddebf923837b0e490ea540d92bb066e5195e63e731aa90b2047234060e052b74)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "displayName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d4c8fdabeb69813b7b26a73c167554b1e191662a1411b2ae645b28b2f5b18cb9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="languageCode")
    def language_code(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "languageCode"))

    @language_code.setter
    def language_code(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3d75ac04a82c32095bdd157de9ed5f06e3d0fe2d724eb5a985ea76b75f8337f3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "languageCode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8a2e40b785ea1b96e68c585d6a46d8d78e60deffa24521598fabf9265fffbaa3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__16942d46f1a057e986d373037536aad3fae5eac6a236b86dea12449a534f8768)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="securitySettings")
    def security_settings(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "securitySettings"))

    @security_settings.setter
    def security_settings(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ad6382496a7fc58c784e9b8a890bfdeb0cfd1bceef2b3b183c4600df2f027f7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "securitySettings", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="timeZone")
    def time_zone(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "timeZone"))

    @time_zone.setter
    def time_zone(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eb6b034d845d01d0c285703b82042cfccd09686c502f40031b083e21b529cead)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timeZone", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDialogflowConversationProfile.GoogleDialogflowConversationProfileAutomatedAgentConfig",
    jsii_struct_bases=[],
    name_mapping={"agent": "agent", "session_ttl": "sessionTtl"},
)
class GoogleDialogflowConversationProfileAutomatedAgentConfig:
    def __init__(
        self,
        *,
        agent: builtins.str,
        session_ttl: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param agent: ID of the Dialogflow agent environment to use. Expects the format "projects//locations//agent/environments/". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#agent GoogleDialogflowConversationProfile#agent}
        :param session_ttl: Configure lifetime of the Dialogflow session. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#session_ttl GoogleDialogflowConversationProfile#session_ttl}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f2596641cb81649cfa0a972372316cc459dcd76cdfbab38a4885069d7ef1b146)
            check_type(argname="argument agent", value=agent, expected_type=type_hints["agent"])
            check_type(argname="argument session_ttl", value=session_ttl, expected_type=type_hints["session_ttl"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "agent": agent,
        }
        if session_ttl is not None:
            self._values["session_ttl"] = session_ttl

    @builtins.property
    def agent(self) -> builtins.str:
        '''ID of the Dialogflow agent environment to use. Expects the format "projects//locations//agent/environments/".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#agent GoogleDialogflowConversationProfile#agent}
        '''
        result = self._values.get("agent")
        assert result is not None, "Required property 'agent' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def session_ttl(self) -> typing.Optional[builtins.str]:
        '''Configure lifetime of the Dialogflow session.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#session_ttl GoogleDialogflowConversationProfile#session_ttl}
        '''
        result = self._values.get("session_ttl")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDialogflowConversationProfileAutomatedAgentConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDialogflowConversationProfileAutomatedAgentConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDialogflowConversationProfile.GoogleDialogflowConversationProfileAutomatedAgentConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b1d39ebeb6243f19fa3125d24b62d47106888168130b75212ea286e8e4f6a29f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetSessionTtl")
    def reset_session_ttl(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSessionTtl", []))

    @builtins.property
    @jsii.member(jsii_name="agentInput")
    def agent_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "agentInput"))

    @builtins.property
    @jsii.member(jsii_name="sessionTtlInput")
    def session_ttl_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sessionTtlInput"))

    @builtins.property
    @jsii.member(jsii_name="agent")
    def agent(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "agent"))

    @agent.setter
    def agent(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__59edade15f95ab8710f88b99e9173fd8ab8392fa360d22a1281eb13708a19a4a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "agent", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sessionTtl")
    def session_ttl(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sessionTtl"))

    @session_ttl.setter
    def session_ttl(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ae3f7afa45b0ee71f2d5385ad9d92b7208978d05b8336653ba347dc4b9d65c50)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sessionTtl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDialogflowConversationProfileAutomatedAgentConfig]:
        return typing.cast(typing.Optional[GoogleDialogflowConversationProfileAutomatedAgentConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDialogflowConversationProfileAutomatedAgentConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ccf543c02a38cdc22baa242f6120fa6d10e750c5a8195bfcacaa44cc93aebad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDialogflowConversationProfile.GoogleDialogflowConversationProfileConfig",
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
        "location": "location",
        "automated_agent_config": "automatedAgentConfig",
        "human_agent_assistant_config": "humanAgentAssistantConfig",
        "human_agent_handoff_config": "humanAgentHandoffConfig",
        "id": "id",
        "language_code": "languageCode",
        "logging_config": "loggingConfig",
        "new_message_event_notification_config": "newMessageEventNotificationConfig",
        "notification_config": "notificationConfig",
        "project": "project",
        "security_settings": "securitySettings",
        "stt_config": "sttConfig",
        "timeouts": "timeouts",
        "time_zone": "timeZone",
        "tts_config": "ttsConfig",
    },
)
class GoogleDialogflowConversationProfileConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        location: builtins.str,
        automated_agent_config: typing.Optional[typing.Union[GoogleDialogflowConversationProfileAutomatedAgentConfig, typing.Dict[builtins.str, typing.Any]]] = None,
        human_agent_assistant_config: typing.Optional[typing.Union["GoogleDialogflowConversationProfileHumanAgentAssistantConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        human_agent_handoff_config: typing.Optional[typing.Union["GoogleDialogflowConversationProfileHumanAgentHandoffConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        language_code: typing.Optional[builtins.str] = None,
        logging_config: typing.Optional[typing.Union["GoogleDialogflowConversationProfileLoggingConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        new_message_event_notification_config: typing.Optional[typing.Union["GoogleDialogflowConversationProfileNewMessageEventNotificationConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        notification_config: typing.Optional[typing.Union["GoogleDialogflowConversationProfileNotificationConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        project: typing.Optional[builtins.str] = None,
        security_settings: typing.Optional[builtins.str] = None,
        stt_config: typing.Optional[typing.Union["GoogleDialogflowConversationProfileSttConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["GoogleDialogflowConversationProfileTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        time_zone: typing.Optional[builtins.str] = None,
        tts_config: typing.Optional[typing.Union["GoogleDialogflowConversationProfileTtsConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param display_name: Required. Human readable name for this profile. Max length 1024 bytes. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#display_name GoogleDialogflowConversationProfile#display_name}
        :param location: desc. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#location GoogleDialogflowConversationProfile#location}
        :param automated_agent_config: automated_agent_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#automated_agent_config GoogleDialogflowConversationProfile#automated_agent_config}
        :param human_agent_assistant_config: human_agent_assistant_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#human_agent_assistant_config GoogleDialogflowConversationProfile#human_agent_assistant_config}
        :param human_agent_handoff_config: human_agent_handoff_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#human_agent_handoff_config GoogleDialogflowConversationProfile#human_agent_handoff_config}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#id GoogleDialogflowConversationProfile#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param language_code: Language code for the conversation profile. This should be a BCP-47 language tag. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#language_code GoogleDialogflowConversationProfile#language_code}
        :param logging_config: logging_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#logging_config GoogleDialogflowConversationProfile#logging_config}
        :param new_message_event_notification_config: new_message_event_notification_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#new_message_event_notification_config GoogleDialogflowConversationProfile#new_message_event_notification_config}
        :param notification_config: notification_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#notification_config GoogleDialogflowConversationProfile#notification_config}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#project GoogleDialogflowConversationProfile#project}.
        :param security_settings: Name of the CX SecuritySettings reference for the agent. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#security_settings GoogleDialogflowConversationProfile#security_settings}
        :param stt_config: stt_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#stt_config GoogleDialogflowConversationProfile#stt_config}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#timeouts GoogleDialogflowConversationProfile#timeouts}
        :param time_zone: The time zone of this conversational profile. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#time_zone GoogleDialogflowConversationProfile#time_zone}
        :param tts_config: tts_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#tts_config GoogleDialogflowConversationProfile#tts_config}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(automated_agent_config, dict):
            automated_agent_config = GoogleDialogflowConversationProfileAutomatedAgentConfig(**automated_agent_config)
        if isinstance(human_agent_assistant_config, dict):
            human_agent_assistant_config = GoogleDialogflowConversationProfileHumanAgentAssistantConfig(**human_agent_assistant_config)
        if isinstance(human_agent_handoff_config, dict):
            human_agent_handoff_config = GoogleDialogflowConversationProfileHumanAgentHandoffConfig(**human_agent_handoff_config)
        if isinstance(logging_config, dict):
            logging_config = GoogleDialogflowConversationProfileLoggingConfig(**logging_config)
        if isinstance(new_message_event_notification_config, dict):
            new_message_event_notification_config = GoogleDialogflowConversationProfileNewMessageEventNotificationConfig(**new_message_event_notification_config)
        if isinstance(notification_config, dict):
            notification_config = GoogleDialogflowConversationProfileNotificationConfig(**notification_config)
        if isinstance(stt_config, dict):
            stt_config = GoogleDialogflowConversationProfileSttConfig(**stt_config)
        if isinstance(timeouts, dict):
            timeouts = GoogleDialogflowConversationProfileTimeouts(**timeouts)
        if isinstance(tts_config, dict):
            tts_config = GoogleDialogflowConversationProfileTtsConfig(**tts_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__38639dfe4ce7699b19a401169762b4db3ba7d183ac657111f2898e8aee01a723)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument display_name", value=display_name, expected_type=type_hints["display_name"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument automated_agent_config", value=automated_agent_config, expected_type=type_hints["automated_agent_config"])
            check_type(argname="argument human_agent_assistant_config", value=human_agent_assistant_config, expected_type=type_hints["human_agent_assistant_config"])
            check_type(argname="argument human_agent_handoff_config", value=human_agent_handoff_config, expected_type=type_hints["human_agent_handoff_config"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument language_code", value=language_code, expected_type=type_hints["language_code"])
            check_type(argname="argument logging_config", value=logging_config, expected_type=type_hints["logging_config"])
            check_type(argname="argument new_message_event_notification_config", value=new_message_event_notification_config, expected_type=type_hints["new_message_event_notification_config"])
            check_type(argname="argument notification_config", value=notification_config, expected_type=type_hints["notification_config"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument security_settings", value=security_settings, expected_type=type_hints["security_settings"])
            check_type(argname="argument stt_config", value=stt_config, expected_type=type_hints["stt_config"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
            check_type(argname="argument time_zone", value=time_zone, expected_type=type_hints["time_zone"])
            check_type(argname="argument tts_config", value=tts_config, expected_type=type_hints["tts_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "display_name": display_name,
            "location": location,
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
        if automated_agent_config is not None:
            self._values["automated_agent_config"] = automated_agent_config
        if human_agent_assistant_config is not None:
            self._values["human_agent_assistant_config"] = human_agent_assistant_config
        if human_agent_handoff_config is not None:
            self._values["human_agent_handoff_config"] = human_agent_handoff_config
        if id is not None:
            self._values["id"] = id
        if language_code is not None:
            self._values["language_code"] = language_code
        if logging_config is not None:
            self._values["logging_config"] = logging_config
        if new_message_event_notification_config is not None:
            self._values["new_message_event_notification_config"] = new_message_event_notification_config
        if notification_config is not None:
            self._values["notification_config"] = notification_config
        if project is not None:
            self._values["project"] = project
        if security_settings is not None:
            self._values["security_settings"] = security_settings
        if stt_config is not None:
            self._values["stt_config"] = stt_config
        if timeouts is not None:
            self._values["timeouts"] = timeouts
        if time_zone is not None:
            self._values["time_zone"] = time_zone
        if tts_config is not None:
            self._values["tts_config"] = tts_config

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
        '''Required. Human readable name for this profile. Max length 1024 bytes.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#display_name GoogleDialogflowConversationProfile#display_name}
        '''
        result = self._values.get("display_name")
        assert result is not None, "Required property 'display_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def location(self) -> builtins.str:
        '''desc.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#location GoogleDialogflowConversationProfile#location}
        '''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def automated_agent_config(
        self,
    ) -> typing.Optional[GoogleDialogflowConversationProfileAutomatedAgentConfig]:
        '''automated_agent_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#automated_agent_config GoogleDialogflowConversationProfile#automated_agent_config}
        '''
        result = self._values.get("automated_agent_config")
        return typing.cast(typing.Optional[GoogleDialogflowConversationProfileAutomatedAgentConfig], result)

    @builtins.property
    def human_agent_assistant_config(
        self,
    ) -> typing.Optional["GoogleDialogflowConversationProfileHumanAgentAssistantConfig"]:
        '''human_agent_assistant_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#human_agent_assistant_config GoogleDialogflowConversationProfile#human_agent_assistant_config}
        '''
        result = self._values.get("human_agent_assistant_config")
        return typing.cast(typing.Optional["GoogleDialogflowConversationProfileHumanAgentAssistantConfig"], result)

    @builtins.property
    def human_agent_handoff_config(
        self,
    ) -> typing.Optional["GoogleDialogflowConversationProfileHumanAgentHandoffConfig"]:
        '''human_agent_handoff_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#human_agent_handoff_config GoogleDialogflowConversationProfile#human_agent_handoff_config}
        '''
        result = self._values.get("human_agent_handoff_config")
        return typing.cast(typing.Optional["GoogleDialogflowConversationProfileHumanAgentHandoffConfig"], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#id GoogleDialogflowConversationProfile#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def language_code(self) -> typing.Optional[builtins.str]:
        '''Language code for the conversation profile. This should be a BCP-47 language tag.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#language_code GoogleDialogflowConversationProfile#language_code}
        '''
        result = self._values.get("language_code")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def logging_config(
        self,
    ) -> typing.Optional["GoogleDialogflowConversationProfileLoggingConfig"]:
        '''logging_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#logging_config GoogleDialogflowConversationProfile#logging_config}
        '''
        result = self._values.get("logging_config")
        return typing.cast(typing.Optional["GoogleDialogflowConversationProfileLoggingConfig"], result)

    @builtins.property
    def new_message_event_notification_config(
        self,
    ) -> typing.Optional["GoogleDialogflowConversationProfileNewMessageEventNotificationConfig"]:
        '''new_message_event_notification_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#new_message_event_notification_config GoogleDialogflowConversationProfile#new_message_event_notification_config}
        '''
        result = self._values.get("new_message_event_notification_config")
        return typing.cast(typing.Optional["GoogleDialogflowConversationProfileNewMessageEventNotificationConfig"], result)

    @builtins.property
    def notification_config(
        self,
    ) -> typing.Optional["GoogleDialogflowConversationProfileNotificationConfig"]:
        '''notification_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#notification_config GoogleDialogflowConversationProfile#notification_config}
        '''
        result = self._values.get("notification_config")
        return typing.cast(typing.Optional["GoogleDialogflowConversationProfileNotificationConfig"], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#project GoogleDialogflowConversationProfile#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def security_settings(self) -> typing.Optional[builtins.str]:
        '''Name of the CX SecuritySettings reference for the agent.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#security_settings GoogleDialogflowConversationProfile#security_settings}
        '''
        result = self._values.get("security_settings")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def stt_config(
        self,
    ) -> typing.Optional["GoogleDialogflowConversationProfileSttConfig"]:
        '''stt_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#stt_config GoogleDialogflowConversationProfile#stt_config}
        '''
        result = self._values.get("stt_config")
        return typing.cast(typing.Optional["GoogleDialogflowConversationProfileSttConfig"], result)

    @builtins.property
    def timeouts(
        self,
    ) -> typing.Optional["GoogleDialogflowConversationProfileTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#timeouts GoogleDialogflowConversationProfile#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["GoogleDialogflowConversationProfileTimeouts"], result)

    @builtins.property
    def time_zone(self) -> typing.Optional[builtins.str]:
        '''The time zone of this conversational profile.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#time_zone GoogleDialogflowConversationProfile#time_zone}
        '''
        result = self._values.get("time_zone")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tts_config(
        self,
    ) -> typing.Optional["GoogleDialogflowConversationProfileTtsConfig"]:
        '''tts_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#tts_config GoogleDialogflowConversationProfile#tts_config}
        '''
        result = self._values.get("tts_config")
        return typing.cast(typing.Optional["GoogleDialogflowConversationProfileTtsConfig"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDialogflowConversationProfileConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDialogflowConversationProfile.GoogleDialogflowConversationProfileHumanAgentAssistantConfig",
    jsii_struct_bases=[],
    name_mapping={
        "end_user_suggestion_config": "endUserSuggestionConfig",
        "human_agent_suggestion_config": "humanAgentSuggestionConfig",
        "message_analysis_config": "messageAnalysisConfig",
        "notification_config": "notificationConfig",
    },
)
class GoogleDialogflowConversationProfileHumanAgentAssistantConfig:
    def __init__(
        self,
        *,
        end_user_suggestion_config: typing.Optional[typing.Union["GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        human_agent_suggestion_config: typing.Optional[typing.Union["GoogleDialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        message_analysis_config: typing.Optional[typing.Union["GoogleDialogflowConversationProfileHumanAgentAssistantConfigMessageAnalysisConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        notification_config: typing.Optional[typing.Union["GoogleDialogflowConversationProfileHumanAgentAssistantConfigNotificationConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param end_user_suggestion_config: end_user_suggestion_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#end_user_suggestion_config GoogleDialogflowConversationProfile#end_user_suggestion_config}
        :param human_agent_suggestion_config: human_agent_suggestion_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#human_agent_suggestion_config GoogleDialogflowConversationProfile#human_agent_suggestion_config}
        :param message_analysis_config: message_analysis_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#message_analysis_config GoogleDialogflowConversationProfile#message_analysis_config}
        :param notification_config: notification_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#notification_config GoogleDialogflowConversationProfile#notification_config}
        '''
        if isinstance(end_user_suggestion_config, dict):
            end_user_suggestion_config = GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfig(**end_user_suggestion_config)
        if isinstance(human_agent_suggestion_config, dict):
            human_agent_suggestion_config = GoogleDialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfig(**human_agent_suggestion_config)
        if isinstance(message_analysis_config, dict):
            message_analysis_config = GoogleDialogflowConversationProfileHumanAgentAssistantConfigMessageAnalysisConfig(**message_analysis_config)
        if isinstance(notification_config, dict):
            notification_config = GoogleDialogflowConversationProfileHumanAgentAssistantConfigNotificationConfig(**notification_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1bca06c71dcdcd764a7f9d52121ae563c50d7089edc5cfa4dc43f3963cb71643)
            check_type(argname="argument end_user_suggestion_config", value=end_user_suggestion_config, expected_type=type_hints["end_user_suggestion_config"])
            check_type(argname="argument human_agent_suggestion_config", value=human_agent_suggestion_config, expected_type=type_hints["human_agent_suggestion_config"])
            check_type(argname="argument message_analysis_config", value=message_analysis_config, expected_type=type_hints["message_analysis_config"])
            check_type(argname="argument notification_config", value=notification_config, expected_type=type_hints["notification_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if end_user_suggestion_config is not None:
            self._values["end_user_suggestion_config"] = end_user_suggestion_config
        if human_agent_suggestion_config is not None:
            self._values["human_agent_suggestion_config"] = human_agent_suggestion_config
        if message_analysis_config is not None:
            self._values["message_analysis_config"] = message_analysis_config
        if notification_config is not None:
            self._values["notification_config"] = notification_config

    @builtins.property
    def end_user_suggestion_config(
        self,
    ) -> typing.Optional["GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfig"]:
        '''end_user_suggestion_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#end_user_suggestion_config GoogleDialogflowConversationProfile#end_user_suggestion_config}
        '''
        result = self._values.get("end_user_suggestion_config")
        return typing.cast(typing.Optional["GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfig"], result)

    @builtins.property
    def human_agent_suggestion_config(
        self,
    ) -> typing.Optional["GoogleDialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfig"]:
        '''human_agent_suggestion_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#human_agent_suggestion_config GoogleDialogflowConversationProfile#human_agent_suggestion_config}
        '''
        result = self._values.get("human_agent_suggestion_config")
        return typing.cast(typing.Optional["GoogleDialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfig"], result)

    @builtins.property
    def message_analysis_config(
        self,
    ) -> typing.Optional["GoogleDialogflowConversationProfileHumanAgentAssistantConfigMessageAnalysisConfig"]:
        '''message_analysis_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#message_analysis_config GoogleDialogflowConversationProfile#message_analysis_config}
        '''
        result = self._values.get("message_analysis_config")
        return typing.cast(typing.Optional["GoogleDialogflowConversationProfileHumanAgentAssistantConfigMessageAnalysisConfig"], result)

    @builtins.property
    def notification_config(
        self,
    ) -> typing.Optional["GoogleDialogflowConversationProfileHumanAgentAssistantConfigNotificationConfig"]:
        '''notification_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#notification_config GoogleDialogflowConversationProfile#notification_config}
        '''
        result = self._values.get("notification_config")
        return typing.cast(typing.Optional["GoogleDialogflowConversationProfileHumanAgentAssistantConfigNotificationConfig"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDialogflowConversationProfileHumanAgentAssistantConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDialogflowConversationProfile.GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfig",
    jsii_struct_bases=[],
    name_mapping={
        "disable_high_latency_features_sync_delivery": "disableHighLatencyFeaturesSyncDelivery",
        "feature_configs": "featureConfigs",
        "generators": "generators",
        "group_suggestion_responses": "groupSuggestionResponses",
    },
)
class GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfig:
    def __init__(
        self,
        *,
        disable_high_latency_features_sync_delivery: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        feature_configs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigs", typing.Dict[builtins.str, typing.Any]]]]] = None,
        generators: typing.Optional[typing.Sequence[builtins.str]] = None,
        group_suggestion_responses: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param disable_high_latency_features_sync_delivery: When disableHighLatencyFeaturesSyncDelivery is true and using the AnalyzeContent API, we will not deliver the responses from high latency features in the API response. The humanAgentAssistantConfig.notification_config must be configured and enableEventBasedSuggestion must be set to true to receive the responses from high latency features in Pub/Sub. High latency feature(s): KNOWLEDGE_ASSIST Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#disable_high_latency_features_sync_delivery GoogleDialogflowConversationProfile#disable_high_latency_features_sync_delivery}
        :param feature_configs: feature_configs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#feature_configs GoogleDialogflowConversationProfile#feature_configs}
        :param generators: List of various generator resource names used in the conversation profile. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#generators GoogleDialogflowConversationProfile#generators}
        :param group_suggestion_responses: If groupSuggestionResponses is false, and there are multiple featureConfigs in event based suggestion or StreamingAnalyzeContent, we will try to deliver suggestions to customers as soon as we get new suggestion. Different type of suggestions based on the same context will be in separate Pub/Sub event or StreamingAnalyzeContentResponse. If groupSuggestionResponses set to true. All the suggestions to the same participant based on the same context will be grouped into a single Pub/Sub event or StreamingAnalyzeContentResponse. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#group_suggestion_responses GoogleDialogflowConversationProfile#group_suggestion_responses}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__33edd33cd630f347ed3c005058ffab527aedf1a341319aa437427ee8538a7a86)
            check_type(argname="argument disable_high_latency_features_sync_delivery", value=disable_high_latency_features_sync_delivery, expected_type=type_hints["disable_high_latency_features_sync_delivery"])
            check_type(argname="argument feature_configs", value=feature_configs, expected_type=type_hints["feature_configs"])
            check_type(argname="argument generators", value=generators, expected_type=type_hints["generators"])
            check_type(argname="argument group_suggestion_responses", value=group_suggestion_responses, expected_type=type_hints["group_suggestion_responses"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if disable_high_latency_features_sync_delivery is not None:
            self._values["disable_high_latency_features_sync_delivery"] = disable_high_latency_features_sync_delivery
        if feature_configs is not None:
            self._values["feature_configs"] = feature_configs
        if generators is not None:
            self._values["generators"] = generators
        if group_suggestion_responses is not None:
            self._values["group_suggestion_responses"] = group_suggestion_responses

    @builtins.property
    def disable_high_latency_features_sync_delivery(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''When disableHighLatencyFeaturesSyncDelivery is true and using the AnalyzeContent API, we will not deliver the responses from high latency features in the API response.

        The humanAgentAssistantConfig.notification_config must be configured and enableEventBasedSuggestion must be set to true to receive the responses from high latency features in Pub/Sub. High latency feature(s): KNOWLEDGE_ASSIST

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#disable_high_latency_features_sync_delivery GoogleDialogflowConversationProfile#disable_high_latency_features_sync_delivery}
        '''
        result = self._values.get("disable_high_latency_features_sync_delivery")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def feature_configs(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigs"]]]:
        '''feature_configs block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#feature_configs GoogleDialogflowConversationProfile#feature_configs}
        '''
        result = self._values.get("feature_configs")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigs"]]], result)

    @builtins.property
    def generators(self) -> typing.Optional[typing.List[builtins.str]]:
        '''List of various generator resource names used in the conversation profile.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#generators GoogleDialogflowConversationProfile#generators}
        '''
        result = self._values.get("generators")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def group_suggestion_responses(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If groupSuggestionResponses is false, and there are multiple featureConfigs in event based suggestion or StreamingAnalyzeContent, we will try to deliver suggestions to customers as soon as we get new suggestion.

        Different type of suggestions based on the same context will be in separate Pub/Sub event or StreamingAnalyzeContentResponse.

        If groupSuggestionResponses set to true. All the suggestions to the same participant based on the same context will be grouped into a single Pub/Sub event or StreamingAnalyzeContentResponse.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#group_suggestion_responses GoogleDialogflowConversationProfile#group_suggestion_responses}
        '''
        result = self._values.get("group_suggestion_responses")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDialogflowConversationProfile.GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigs",
    jsii_struct_bases=[],
    name_mapping={
        "conversation_model_config": "conversationModelConfig",
        "conversation_process_config": "conversationProcessConfig",
        "disable_agent_query_logging": "disableAgentQueryLogging",
        "enable_conversation_augmented_query": "enableConversationAugmentedQuery",
        "enable_event_based_suggestion": "enableEventBasedSuggestion",
        "enable_query_suggestion_only": "enableQuerySuggestionOnly",
        "enable_query_suggestion_when_no_answer": "enableQuerySuggestionWhenNoAnswer",
        "query_config": "queryConfig",
        "suggestion_feature": "suggestionFeature",
        "suggestion_trigger_settings": "suggestionTriggerSettings",
    },
)
class GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigs:
    def __init__(
        self,
        *,
        conversation_model_config: typing.Optional[typing.Union["GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsConversationModelConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        conversation_process_config: typing.Optional[typing.Union["GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsConversationProcessConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        disable_agent_query_logging: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_conversation_augmented_query: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_event_based_suggestion: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_query_suggestion_only: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_query_suggestion_when_no_answer: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        query_config: typing.Optional[typing.Union["GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        suggestion_feature: typing.Optional[typing.Union["GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsSuggestionFeature", typing.Dict[builtins.str, typing.Any]]] = None,
        suggestion_trigger_settings: typing.Optional[typing.Union["GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsSuggestionTriggerSettings", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param conversation_model_config: conversation_model_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#conversation_model_config GoogleDialogflowConversationProfile#conversation_model_config}
        :param conversation_process_config: conversation_process_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#conversation_process_config GoogleDialogflowConversationProfile#conversation_process_config}
        :param disable_agent_query_logging: Disable the logging of search queries sent by human agents. It can prevent those queries from being stored at answer records. This feature is only supported for types: KNOWLEDGE_SEARCH. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#disable_agent_query_logging GoogleDialogflowConversationProfile#disable_agent_query_logging}
        :param enable_conversation_augmented_query: Enable including conversation context during query answer generation. This feature is only supported for types: KNOWLEDGE_SEARCH. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#enable_conversation_augmented_query GoogleDialogflowConversationProfile#enable_conversation_augmented_query}
        :param enable_event_based_suggestion: Automatically iterates all participants and tries to compile suggestions. This feature is only supported for types: ARTICLE_SUGGESTION, FAQ, DIALOGFLOW_ASSIST, KNOWLEDGE_ASSIST. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#enable_event_based_suggestion GoogleDialogflowConversationProfile#enable_event_based_suggestion}
        :param enable_query_suggestion_only: Enable query suggestion only. This feature is only supported for types: KNOWLEDGE_ASSIST. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#enable_query_suggestion_only GoogleDialogflowConversationProfile#enable_query_suggestion_only}
        :param enable_query_suggestion_when_no_answer: Enable query suggestion even if we can't find its answer. By default, queries are suggested only if we find its answer. This feature is only supported for types: KNOWLEDGE_ASSIST. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#enable_query_suggestion_when_no_answer GoogleDialogflowConversationProfile#enable_query_suggestion_when_no_answer}
        :param query_config: query_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#query_config GoogleDialogflowConversationProfile#query_config}
        :param suggestion_feature: suggestion_feature block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#suggestion_feature GoogleDialogflowConversationProfile#suggestion_feature}
        :param suggestion_trigger_settings: suggestion_trigger_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#suggestion_trigger_settings GoogleDialogflowConversationProfile#suggestion_trigger_settings}
        '''
        if isinstance(conversation_model_config, dict):
            conversation_model_config = GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsConversationModelConfig(**conversation_model_config)
        if isinstance(conversation_process_config, dict):
            conversation_process_config = GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsConversationProcessConfig(**conversation_process_config)
        if isinstance(query_config, dict):
            query_config = GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfig(**query_config)
        if isinstance(suggestion_feature, dict):
            suggestion_feature = GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsSuggestionFeature(**suggestion_feature)
        if isinstance(suggestion_trigger_settings, dict):
            suggestion_trigger_settings = GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsSuggestionTriggerSettings(**suggestion_trigger_settings)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__297cb20731a08760e08b03bd05d2ca40e0bad911c2b2f20fc469deacbd45ba14)
            check_type(argname="argument conversation_model_config", value=conversation_model_config, expected_type=type_hints["conversation_model_config"])
            check_type(argname="argument conversation_process_config", value=conversation_process_config, expected_type=type_hints["conversation_process_config"])
            check_type(argname="argument disable_agent_query_logging", value=disable_agent_query_logging, expected_type=type_hints["disable_agent_query_logging"])
            check_type(argname="argument enable_conversation_augmented_query", value=enable_conversation_augmented_query, expected_type=type_hints["enable_conversation_augmented_query"])
            check_type(argname="argument enable_event_based_suggestion", value=enable_event_based_suggestion, expected_type=type_hints["enable_event_based_suggestion"])
            check_type(argname="argument enable_query_suggestion_only", value=enable_query_suggestion_only, expected_type=type_hints["enable_query_suggestion_only"])
            check_type(argname="argument enable_query_suggestion_when_no_answer", value=enable_query_suggestion_when_no_answer, expected_type=type_hints["enable_query_suggestion_when_no_answer"])
            check_type(argname="argument query_config", value=query_config, expected_type=type_hints["query_config"])
            check_type(argname="argument suggestion_feature", value=suggestion_feature, expected_type=type_hints["suggestion_feature"])
            check_type(argname="argument suggestion_trigger_settings", value=suggestion_trigger_settings, expected_type=type_hints["suggestion_trigger_settings"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if conversation_model_config is not None:
            self._values["conversation_model_config"] = conversation_model_config
        if conversation_process_config is not None:
            self._values["conversation_process_config"] = conversation_process_config
        if disable_agent_query_logging is not None:
            self._values["disable_agent_query_logging"] = disable_agent_query_logging
        if enable_conversation_augmented_query is not None:
            self._values["enable_conversation_augmented_query"] = enable_conversation_augmented_query
        if enable_event_based_suggestion is not None:
            self._values["enable_event_based_suggestion"] = enable_event_based_suggestion
        if enable_query_suggestion_only is not None:
            self._values["enable_query_suggestion_only"] = enable_query_suggestion_only
        if enable_query_suggestion_when_no_answer is not None:
            self._values["enable_query_suggestion_when_no_answer"] = enable_query_suggestion_when_no_answer
        if query_config is not None:
            self._values["query_config"] = query_config
        if suggestion_feature is not None:
            self._values["suggestion_feature"] = suggestion_feature
        if suggestion_trigger_settings is not None:
            self._values["suggestion_trigger_settings"] = suggestion_trigger_settings

    @builtins.property
    def conversation_model_config(
        self,
    ) -> typing.Optional["GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsConversationModelConfig"]:
        '''conversation_model_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#conversation_model_config GoogleDialogflowConversationProfile#conversation_model_config}
        '''
        result = self._values.get("conversation_model_config")
        return typing.cast(typing.Optional["GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsConversationModelConfig"], result)

    @builtins.property
    def conversation_process_config(
        self,
    ) -> typing.Optional["GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsConversationProcessConfig"]:
        '''conversation_process_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#conversation_process_config GoogleDialogflowConversationProfile#conversation_process_config}
        '''
        result = self._values.get("conversation_process_config")
        return typing.cast(typing.Optional["GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsConversationProcessConfig"], result)

    @builtins.property
    def disable_agent_query_logging(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Disable the logging of search queries sent by human agents.

        It can prevent those queries from being stored at answer records.
        This feature is only supported for types: KNOWLEDGE_SEARCH.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#disable_agent_query_logging GoogleDialogflowConversationProfile#disable_agent_query_logging}
        '''
        result = self._values.get("disable_agent_query_logging")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def enable_conversation_augmented_query(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Enable including conversation context during query answer generation. This feature is only supported for types: KNOWLEDGE_SEARCH.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#enable_conversation_augmented_query GoogleDialogflowConversationProfile#enable_conversation_augmented_query}
        '''
        result = self._values.get("enable_conversation_augmented_query")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def enable_event_based_suggestion(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Automatically iterates all participants and tries to compile suggestions. This feature is only supported for types: ARTICLE_SUGGESTION, FAQ, DIALOGFLOW_ASSIST, KNOWLEDGE_ASSIST.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#enable_event_based_suggestion GoogleDialogflowConversationProfile#enable_event_based_suggestion}
        '''
        result = self._values.get("enable_event_based_suggestion")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def enable_query_suggestion_only(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Enable query suggestion only. This feature is only supported for types: KNOWLEDGE_ASSIST.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#enable_query_suggestion_only GoogleDialogflowConversationProfile#enable_query_suggestion_only}
        '''
        result = self._values.get("enable_query_suggestion_only")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def enable_query_suggestion_when_no_answer(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Enable query suggestion even if we can't find its answer.

        By default, queries are suggested only if we find its answer.
        This feature is only supported for types: KNOWLEDGE_ASSIST.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#enable_query_suggestion_when_no_answer GoogleDialogflowConversationProfile#enable_query_suggestion_when_no_answer}
        '''
        result = self._values.get("enable_query_suggestion_when_no_answer")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def query_config(
        self,
    ) -> typing.Optional["GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfig"]:
        '''query_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#query_config GoogleDialogflowConversationProfile#query_config}
        '''
        result = self._values.get("query_config")
        return typing.cast(typing.Optional["GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfig"], result)

    @builtins.property
    def suggestion_feature(
        self,
    ) -> typing.Optional["GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsSuggestionFeature"]:
        '''suggestion_feature block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#suggestion_feature GoogleDialogflowConversationProfile#suggestion_feature}
        '''
        result = self._values.get("suggestion_feature")
        return typing.cast(typing.Optional["GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsSuggestionFeature"], result)

    @builtins.property
    def suggestion_trigger_settings(
        self,
    ) -> typing.Optional["GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsSuggestionTriggerSettings"]:
        '''suggestion_trigger_settings block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#suggestion_trigger_settings GoogleDialogflowConversationProfile#suggestion_trigger_settings}
        '''
        result = self._values.get("suggestion_trigger_settings")
        return typing.cast(typing.Optional["GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsSuggestionTriggerSettings"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigs(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDialogflowConversationProfile.GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsConversationModelConfig",
    jsii_struct_bases=[],
    name_mapping={"baseline_model_version": "baselineModelVersion", "model": "model"},
)
class GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsConversationModelConfig:
    def __init__(
        self,
        *,
        baseline_model_version: typing.Optional[builtins.str] = None,
        model: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param baseline_model_version: Version of current baseline model. It will be ignored if model is set. Valid versions are: Article Suggestion baseline model: - 0.9 - 1.0 (default) Summarization baseline model: - 1.0 Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#baseline_model_version GoogleDialogflowConversationProfile#baseline_model_version}
        :param model: Conversation model resource name. Format: projects//conversationModels/. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#model GoogleDialogflowConversationProfile#model}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d88c1aa4efd22f2f6f7fc7493aa4ab9b28e9b0fe3afd1308a7e3b63b848d38d9)
            check_type(argname="argument baseline_model_version", value=baseline_model_version, expected_type=type_hints["baseline_model_version"])
            check_type(argname="argument model", value=model, expected_type=type_hints["model"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if baseline_model_version is not None:
            self._values["baseline_model_version"] = baseline_model_version
        if model is not None:
            self._values["model"] = model

    @builtins.property
    def baseline_model_version(self) -> typing.Optional[builtins.str]:
        '''Version of current baseline model.

        It will be ignored if model is set. Valid versions are: Article Suggestion baseline model: - 0.9 - 1.0 (default) Summarization baseline model: - 1.0

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#baseline_model_version GoogleDialogflowConversationProfile#baseline_model_version}
        '''
        result = self._values.get("baseline_model_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def model(self) -> typing.Optional[builtins.str]:
        '''Conversation model resource name. Format: projects//conversationModels/.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#model GoogleDialogflowConversationProfile#model}
        '''
        result = self._values.get("model")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsConversationModelConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsConversationModelConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDialogflowConversationProfile.GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsConversationModelConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__49298e6b0f00f2b7d95e9f666f9135d7dc60074ce252b096d6524b78e44b8908)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetBaselineModelVersion")
    def reset_baseline_model_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBaselineModelVersion", []))

    @jsii.member(jsii_name="resetModel")
    def reset_model(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetModel", []))

    @builtins.property
    @jsii.member(jsii_name="baselineModelVersionInput")
    def baseline_model_version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "baselineModelVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="modelInput")
    def model_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "modelInput"))

    @builtins.property
    @jsii.member(jsii_name="baselineModelVersion")
    def baseline_model_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "baselineModelVersion"))

    @baseline_model_version.setter
    def baseline_model_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__df8abec4af95d66b2203cb85dec56933d6e0bf9e9769eeed5a2f56e9fef72182)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "baselineModelVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="model")
    def model(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "model"))

    @model.setter
    def model(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c6bc69ed048f0bfc9934059c715b34cded833295fa9fcca63fab63961fc597b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "model", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsConversationModelConfig]:
        return typing.cast(typing.Optional[GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsConversationModelConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsConversationModelConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce69286f4243dd19687c56634be1ceaa7ba318e45f05fdd191569558b1eaef4b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDialogflowConversationProfile.GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsConversationProcessConfig",
    jsii_struct_bases=[],
    name_mapping={"recent_sentences_count": "recentSentencesCount"},
)
class GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsConversationProcessConfig:
    def __init__(
        self,
        *,
        recent_sentences_count: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param recent_sentences_count: Number of recent non-small-talk sentences to use as context for article and FAQ suggestion. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#recent_sentences_count GoogleDialogflowConversationProfile#recent_sentences_count}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__49f50e5c804fec73164409c0fc234ab7e07f8e2a2671f9641616fdc7f34757b4)
            check_type(argname="argument recent_sentences_count", value=recent_sentences_count, expected_type=type_hints["recent_sentences_count"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if recent_sentences_count is not None:
            self._values["recent_sentences_count"] = recent_sentences_count

    @builtins.property
    def recent_sentences_count(self) -> typing.Optional[jsii.Number]:
        '''Number of recent non-small-talk sentences to use as context for article and FAQ suggestion.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#recent_sentences_count GoogleDialogflowConversationProfile#recent_sentences_count}
        '''
        result = self._values.get("recent_sentences_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsConversationProcessConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsConversationProcessConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDialogflowConversationProfile.GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsConversationProcessConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__211634fd9a9b938c302002f9188d9acbf73205889d358ceccfb169505bb67422)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetRecentSentencesCount")
    def reset_recent_sentences_count(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRecentSentencesCount", []))

    @builtins.property
    @jsii.member(jsii_name="recentSentencesCountInput")
    def recent_sentences_count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "recentSentencesCountInput"))

    @builtins.property
    @jsii.member(jsii_name="recentSentencesCount")
    def recent_sentences_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "recentSentencesCount"))

    @recent_sentences_count.setter
    def recent_sentences_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f2e27c72c6098ae35ddded5341da736014caacbf56c10415adde0079c09f77b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "recentSentencesCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsConversationProcessConfig]:
        return typing.cast(typing.Optional[GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsConversationProcessConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsConversationProcessConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d57323306ab0292c6f4a0a747f472faf60b7f5136df680f043056ae93c9824c5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDialogflowConversationProfile.GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ade049557c95e9f0e8c289bc63f00a7b2bb55128f80d942383d7d6938ce2814d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__553e262c025e3897bd95ed3335767920f41e0a97860ddc1b88c90c348170559d)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d4f22545fe83eab937f778818faba8c50dcbeb9dca392bcce58d82942df97783)
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
            type_hints = typing.get_type_hints(_typecheckingstub__75d7c5eaa5b319709a1cd990ad3fd7a01e3bb276122fd53e12d6472ba9798abc)
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
            type_hints = typing.get_type_hints(_typecheckingstub__75118c0cbb4bf3e97657359d3aa3f28f1aec25f0952b889624bb003e130a6217)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigs]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigs]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigs]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__98e82d347df584c27e9714720b6f778bcc783d1863f7e72b2d8b4d8360b6f250)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDialogflowConversationProfile.GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3980ae579196aa45dd9dfe4970a65c789b24416e7c25c9555577107ed15bad8a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putConversationModelConfig")
    def put_conversation_model_config(
        self,
        *,
        baseline_model_version: typing.Optional[builtins.str] = None,
        model: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param baseline_model_version: Version of current baseline model. It will be ignored if model is set. Valid versions are: Article Suggestion baseline model: - 0.9 - 1.0 (default) Summarization baseline model: - 1.0 Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#baseline_model_version GoogleDialogflowConversationProfile#baseline_model_version}
        :param model: Conversation model resource name. Format: projects//conversationModels/. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#model GoogleDialogflowConversationProfile#model}
        '''
        value = GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsConversationModelConfig(
            baseline_model_version=baseline_model_version, model=model
        )

        return typing.cast(None, jsii.invoke(self, "putConversationModelConfig", [value]))

    @jsii.member(jsii_name="putConversationProcessConfig")
    def put_conversation_process_config(
        self,
        *,
        recent_sentences_count: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param recent_sentences_count: Number of recent non-small-talk sentences to use as context for article and FAQ suggestion. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#recent_sentences_count GoogleDialogflowConversationProfile#recent_sentences_count}
        '''
        value = GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsConversationProcessConfig(
            recent_sentences_count=recent_sentences_count
        )

        return typing.cast(None, jsii.invoke(self, "putConversationProcessConfig", [value]))

    @jsii.member(jsii_name="putQueryConfig")
    def put_query_config(
        self,
        *,
        confidence_threshold: typing.Optional[jsii.Number] = None,
        context_filter_settings: typing.Optional[typing.Union["GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfigContextFilterSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        dialogflow_query_source: typing.Optional[typing.Union["GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfigDialogflowQuerySource", typing.Dict[builtins.str, typing.Any]]] = None,
        document_query_source: typing.Optional[typing.Union["GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfigDocumentQuerySource", typing.Dict[builtins.str, typing.Any]]] = None,
        knowledge_base_query_source: typing.Optional[typing.Union["GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfigKnowledgeBaseQuerySource", typing.Dict[builtins.str, typing.Any]]] = None,
        max_results: typing.Optional[jsii.Number] = None,
        sections: typing.Optional[typing.Union["GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfigSections", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param confidence_threshold: Confidence threshold of query result. This feature is only supported for types: ARTICLE_SUGGESTION, FAQ, SMART_REPLY, SMART_COMPOSE, KNOWLEDGE_SEARCH, KNOWLEDGE_ASSIST, ENTITY_EXTRACTION. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#confidence_threshold GoogleDialogflowConversationProfile#confidence_threshold}
        :param context_filter_settings: context_filter_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#context_filter_settings GoogleDialogflowConversationProfile#context_filter_settings}
        :param dialogflow_query_source: dialogflow_query_source block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#dialogflow_query_source GoogleDialogflowConversationProfile#dialogflow_query_source}
        :param document_query_source: document_query_source block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#document_query_source GoogleDialogflowConversationProfile#document_query_source}
        :param knowledge_base_query_source: knowledge_base_query_source block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#knowledge_base_query_source GoogleDialogflowConversationProfile#knowledge_base_query_source}
        :param max_results: Maximum number of results to return. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#max_results GoogleDialogflowConversationProfile#max_results}
        :param sections: sections block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#sections GoogleDialogflowConversationProfile#sections}
        '''
        value = GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfig(
            confidence_threshold=confidence_threshold,
            context_filter_settings=context_filter_settings,
            dialogflow_query_source=dialogflow_query_source,
            document_query_source=document_query_source,
            knowledge_base_query_source=knowledge_base_query_source,
            max_results=max_results,
            sections=sections,
        )

        return typing.cast(None, jsii.invoke(self, "putQueryConfig", [value]))

    @jsii.member(jsii_name="putSuggestionFeature")
    def put_suggestion_feature(
        self,
        *,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param type: Type of Human Agent Assistant API feature to request. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#type GoogleDialogflowConversationProfile#type}
        '''
        value = GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsSuggestionFeature(
            type=type
        )

        return typing.cast(None, jsii.invoke(self, "putSuggestionFeature", [value]))

    @jsii.member(jsii_name="putSuggestionTriggerSettings")
    def put_suggestion_trigger_settings(
        self,
        *,
        no_small_talk: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        only_end_user: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param no_small_talk: Do not trigger if last utterance is small talk. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#no_small_talk GoogleDialogflowConversationProfile#no_small_talk}
        :param only_end_user: Only trigger suggestion if participant role of last utterance is END_USER. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#only_end_user GoogleDialogflowConversationProfile#only_end_user}
        '''
        value = GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsSuggestionTriggerSettings(
            no_small_talk=no_small_talk, only_end_user=only_end_user
        )

        return typing.cast(None, jsii.invoke(self, "putSuggestionTriggerSettings", [value]))

    @jsii.member(jsii_name="resetConversationModelConfig")
    def reset_conversation_model_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConversationModelConfig", []))

    @jsii.member(jsii_name="resetConversationProcessConfig")
    def reset_conversation_process_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConversationProcessConfig", []))

    @jsii.member(jsii_name="resetDisableAgentQueryLogging")
    def reset_disable_agent_query_logging(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDisableAgentQueryLogging", []))

    @jsii.member(jsii_name="resetEnableConversationAugmentedQuery")
    def reset_enable_conversation_augmented_query(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnableConversationAugmentedQuery", []))

    @jsii.member(jsii_name="resetEnableEventBasedSuggestion")
    def reset_enable_event_based_suggestion(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnableEventBasedSuggestion", []))

    @jsii.member(jsii_name="resetEnableQuerySuggestionOnly")
    def reset_enable_query_suggestion_only(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnableQuerySuggestionOnly", []))

    @jsii.member(jsii_name="resetEnableQuerySuggestionWhenNoAnswer")
    def reset_enable_query_suggestion_when_no_answer(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnableQuerySuggestionWhenNoAnswer", []))

    @jsii.member(jsii_name="resetQueryConfig")
    def reset_query_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetQueryConfig", []))

    @jsii.member(jsii_name="resetSuggestionFeature")
    def reset_suggestion_feature(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSuggestionFeature", []))

    @jsii.member(jsii_name="resetSuggestionTriggerSettings")
    def reset_suggestion_trigger_settings(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSuggestionTriggerSettings", []))

    @builtins.property
    @jsii.member(jsii_name="conversationModelConfig")
    def conversation_model_config(
        self,
    ) -> GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsConversationModelConfigOutputReference:
        return typing.cast(GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsConversationModelConfigOutputReference, jsii.get(self, "conversationModelConfig"))

    @builtins.property
    @jsii.member(jsii_name="conversationProcessConfig")
    def conversation_process_config(
        self,
    ) -> GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsConversationProcessConfigOutputReference:
        return typing.cast(GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsConversationProcessConfigOutputReference, jsii.get(self, "conversationProcessConfig"))

    @builtins.property
    @jsii.member(jsii_name="queryConfig")
    def query_config(
        self,
    ) -> "GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfigOutputReference":
        return typing.cast("GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfigOutputReference", jsii.get(self, "queryConfig"))

    @builtins.property
    @jsii.member(jsii_name="suggestionFeature")
    def suggestion_feature(
        self,
    ) -> "GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsSuggestionFeatureOutputReference":
        return typing.cast("GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsSuggestionFeatureOutputReference", jsii.get(self, "suggestionFeature"))

    @builtins.property
    @jsii.member(jsii_name="suggestionTriggerSettings")
    def suggestion_trigger_settings(
        self,
    ) -> "GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsSuggestionTriggerSettingsOutputReference":
        return typing.cast("GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsSuggestionTriggerSettingsOutputReference", jsii.get(self, "suggestionTriggerSettings"))

    @builtins.property
    @jsii.member(jsii_name="conversationModelConfigInput")
    def conversation_model_config_input(
        self,
    ) -> typing.Optional[GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsConversationModelConfig]:
        return typing.cast(typing.Optional[GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsConversationModelConfig], jsii.get(self, "conversationModelConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="conversationProcessConfigInput")
    def conversation_process_config_input(
        self,
    ) -> typing.Optional[GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsConversationProcessConfig]:
        return typing.cast(typing.Optional[GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsConversationProcessConfig], jsii.get(self, "conversationProcessConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="disableAgentQueryLoggingInput")
    def disable_agent_query_logging_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "disableAgentQueryLoggingInput"))

    @builtins.property
    @jsii.member(jsii_name="enableConversationAugmentedQueryInput")
    def enable_conversation_augmented_query_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enableConversationAugmentedQueryInput"))

    @builtins.property
    @jsii.member(jsii_name="enableEventBasedSuggestionInput")
    def enable_event_based_suggestion_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enableEventBasedSuggestionInput"))

    @builtins.property
    @jsii.member(jsii_name="enableQuerySuggestionOnlyInput")
    def enable_query_suggestion_only_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enableQuerySuggestionOnlyInput"))

    @builtins.property
    @jsii.member(jsii_name="enableQuerySuggestionWhenNoAnswerInput")
    def enable_query_suggestion_when_no_answer_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enableQuerySuggestionWhenNoAnswerInput"))

    @builtins.property
    @jsii.member(jsii_name="queryConfigInput")
    def query_config_input(
        self,
    ) -> typing.Optional["GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfig"]:
        return typing.cast(typing.Optional["GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfig"], jsii.get(self, "queryConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="suggestionFeatureInput")
    def suggestion_feature_input(
        self,
    ) -> typing.Optional["GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsSuggestionFeature"]:
        return typing.cast(typing.Optional["GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsSuggestionFeature"], jsii.get(self, "suggestionFeatureInput"))

    @builtins.property
    @jsii.member(jsii_name="suggestionTriggerSettingsInput")
    def suggestion_trigger_settings_input(
        self,
    ) -> typing.Optional["GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsSuggestionTriggerSettings"]:
        return typing.cast(typing.Optional["GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsSuggestionTriggerSettings"], jsii.get(self, "suggestionTriggerSettingsInput"))

    @builtins.property
    @jsii.member(jsii_name="disableAgentQueryLogging")
    def disable_agent_query_logging(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "disableAgentQueryLogging"))

    @disable_agent_query_logging.setter
    def disable_agent_query_logging(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__90517bfc871a5c332ec9926c8f94861b060b798a0d8cfef1d1d6c381e0f5a063)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "disableAgentQueryLogging", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enableConversationAugmentedQuery")
    def enable_conversation_augmented_query(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enableConversationAugmentedQuery"))

    @enable_conversation_augmented_query.setter
    def enable_conversation_augmented_query(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ec569fbee6e9c93927fec811f0116c83483b1a78f1f4d7e7980ba0ee12886cf3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableConversationAugmentedQuery", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enableEventBasedSuggestion")
    def enable_event_based_suggestion(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enableEventBasedSuggestion"))

    @enable_event_based_suggestion.setter
    def enable_event_based_suggestion(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b7ac4c891bef78f8a316a4db77848e0f5ef9d8dfaff2e2eff00be2372ac7f774)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableEventBasedSuggestion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enableQuerySuggestionOnly")
    def enable_query_suggestion_only(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enableQuerySuggestionOnly"))

    @enable_query_suggestion_only.setter
    def enable_query_suggestion_only(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c5b5ed1746e670d653e728d5f563b2dbfbdfbb2e511c10e7a39dd67d18b74c88)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableQuerySuggestionOnly", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enableQuerySuggestionWhenNoAnswer")
    def enable_query_suggestion_when_no_answer(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enableQuerySuggestionWhenNoAnswer"))

    @enable_query_suggestion_when_no_answer.setter
    def enable_query_suggestion_when_no_answer(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__401a5797def297e9e352552599a155fece67def4eb579828e2fc57551d2284c3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableQuerySuggestionWhenNoAnswer", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigs]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigs]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigs]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__31fa0d19a601908a479927c514a8f9d4b11cffa39631cfc0356c78b4c78585db)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDialogflowConversationProfile.GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfig",
    jsii_struct_bases=[],
    name_mapping={
        "confidence_threshold": "confidenceThreshold",
        "context_filter_settings": "contextFilterSettings",
        "dialogflow_query_source": "dialogflowQuerySource",
        "document_query_source": "documentQuerySource",
        "knowledge_base_query_source": "knowledgeBaseQuerySource",
        "max_results": "maxResults",
        "sections": "sections",
    },
)
class GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfig:
    def __init__(
        self,
        *,
        confidence_threshold: typing.Optional[jsii.Number] = None,
        context_filter_settings: typing.Optional[typing.Union["GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfigContextFilterSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        dialogflow_query_source: typing.Optional[typing.Union["GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfigDialogflowQuerySource", typing.Dict[builtins.str, typing.Any]]] = None,
        document_query_source: typing.Optional[typing.Union["GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfigDocumentQuerySource", typing.Dict[builtins.str, typing.Any]]] = None,
        knowledge_base_query_source: typing.Optional[typing.Union["GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfigKnowledgeBaseQuerySource", typing.Dict[builtins.str, typing.Any]]] = None,
        max_results: typing.Optional[jsii.Number] = None,
        sections: typing.Optional[typing.Union["GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfigSections", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param confidence_threshold: Confidence threshold of query result. This feature is only supported for types: ARTICLE_SUGGESTION, FAQ, SMART_REPLY, SMART_COMPOSE, KNOWLEDGE_SEARCH, KNOWLEDGE_ASSIST, ENTITY_EXTRACTION. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#confidence_threshold GoogleDialogflowConversationProfile#confidence_threshold}
        :param context_filter_settings: context_filter_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#context_filter_settings GoogleDialogflowConversationProfile#context_filter_settings}
        :param dialogflow_query_source: dialogflow_query_source block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#dialogflow_query_source GoogleDialogflowConversationProfile#dialogflow_query_source}
        :param document_query_source: document_query_source block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#document_query_source GoogleDialogflowConversationProfile#document_query_source}
        :param knowledge_base_query_source: knowledge_base_query_source block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#knowledge_base_query_source GoogleDialogflowConversationProfile#knowledge_base_query_source}
        :param max_results: Maximum number of results to return. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#max_results GoogleDialogflowConversationProfile#max_results}
        :param sections: sections block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#sections GoogleDialogflowConversationProfile#sections}
        '''
        if isinstance(context_filter_settings, dict):
            context_filter_settings = GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfigContextFilterSettings(**context_filter_settings)
        if isinstance(dialogflow_query_source, dict):
            dialogflow_query_source = GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfigDialogflowQuerySource(**dialogflow_query_source)
        if isinstance(document_query_source, dict):
            document_query_source = GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfigDocumentQuerySource(**document_query_source)
        if isinstance(knowledge_base_query_source, dict):
            knowledge_base_query_source = GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfigKnowledgeBaseQuerySource(**knowledge_base_query_source)
        if isinstance(sections, dict):
            sections = GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfigSections(**sections)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__086c304372aa8e27a5954359077394abf565d98493cabb440861ca69c9ca15bf)
            check_type(argname="argument confidence_threshold", value=confidence_threshold, expected_type=type_hints["confidence_threshold"])
            check_type(argname="argument context_filter_settings", value=context_filter_settings, expected_type=type_hints["context_filter_settings"])
            check_type(argname="argument dialogflow_query_source", value=dialogflow_query_source, expected_type=type_hints["dialogflow_query_source"])
            check_type(argname="argument document_query_source", value=document_query_source, expected_type=type_hints["document_query_source"])
            check_type(argname="argument knowledge_base_query_source", value=knowledge_base_query_source, expected_type=type_hints["knowledge_base_query_source"])
            check_type(argname="argument max_results", value=max_results, expected_type=type_hints["max_results"])
            check_type(argname="argument sections", value=sections, expected_type=type_hints["sections"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if confidence_threshold is not None:
            self._values["confidence_threshold"] = confidence_threshold
        if context_filter_settings is not None:
            self._values["context_filter_settings"] = context_filter_settings
        if dialogflow_query_source is not None:
            self._values["dialogflow_query_source"] = dialogflow_query_source
        if document_query_source is not None:
            self._values["document_query_source"] = document_query_source
        if knowledge_base_query_source is not None:
            self._values["knowledge_base_query_source"] = knowledge_base_query_source
        if max_results is not None:
            self._values["max_results"] = max_results
        if sections is not None:
            self._values["sections"] = sections

    @builtins.property
    def confidence_threshold(self) -> typing.Optional[jsii.Number]:
        '''Confidence threshold of query result. This feature is only supported for types: ARTICLE_SUGGESTION, FAQ, SMART_REPLY, SMART_COMPOSE, KNOWLEDGE_SEARCH, KNOWLEDGE_ASSIST, ENTITY_EXTRACTION.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#confidence_threshold GoogleDialogflowConversationProfile#confidence_threshold}
        '''
        result = self._values.get("confidence_threshold")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def context_filter_settings(
        self,
    ) -> typing.Optional["GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfigContextFilterSettings"]:
        '''context_filter_settings block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#context_filter_settings GoogleDialogflowConversationProfile#context_filter_settings}
        '''
        result = self._values.get("context_filter_settings")
        return typing.cast(typing.Optional["GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfigContextFilterSettings"], result)

    @builtins.property
    def dialogflow_query_source(
        self,
    ) -> typing.Optional["GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfigDialogflowQuerySource"]:
        '''dialogflow_query_source block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#dialogflow_query_source GoogleDialogflowConversationProfile#dialogflow_query_source}
        '''
        result = self._values.get("dialogflow_query_source")
        return typing.cast(typing.Optional["GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfigDialogflowQuerySource"], result)

    @builtins.property
    def document_query_source(
        self,
    ) -> typing.Optional["GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfigDocumentQuerySource"]:
        '''document_query_source block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#document_query_source GoogleDialogflowConversationProfile#document_query_source}
        '''
        result = self._values.get("document_query_source")
        return typing.cast(typing.Optional["GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfigDocumentQuerySource"], result)

    @builtins.property
    def knowledge_base_query_source(
        self,
    ) -> typing.Optional["GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfigKnowledgeBaseQuerySource"]:
        '''knowledge_base_query_source block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#knowledge_base_query_source GoogleDialogflowConversationProfile#knowledge_base_query_source}
        '''
        result = self._values.get("knowledge_base_query_source")
        return typing.cast(typing.Optional["GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfigKnowledgeBaseQuerySource"], result)

    @builtins.property
    def max_results(self) -> typing.Optional[jsii.Number]:
        '''Maximum number of results to return.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#max_results GoogleDialogflowConversationProfile#max_results}
        '''
        result = self._values.get("max_results")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def sections(
        self,
    ) -> typing.Optional["GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfigSections"]:
        '''sections block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#sections GoogleDialogflowConversationProfile#sections}
        '''
        result = self._values.get("sections")
        return typing.cast(typing.Optional["GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfigSections"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDialogflowConversationProfile.GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfigContextFilterSettings",
    jsii_struct_bases=[],
    name_mapping={
        "drop_handoff_messages": "dropHandoffMessages",
        "drop_ivr_messages": "dropIvrMessages",
        "drop_virtual_agent_messages": "dropVirtualAgentMessages",
    },
)
class GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfigContextFilterSettings:
    def __init__(
        self,
        *,
        drop_handoff_messages: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        drop_ivr_messages: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        drop_virtual_agent_messages: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param drop_handoff_messages: If set to true, the last message from virtual agent (hand off message) and the message before it (trigger message of hand off) are dropped. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#drop_handoff_messages GoogleDialogflowConversationProfile#drop_handoff_messages}
        :param drop_ivr_messages: If set to true, all messages from ivr stage are dropped. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#drop_ivr_messages GoogleDialogflowConversationProfile#drop_ivr_messages}
        :param drop_virtual_agent_messages: If set to true, all messages from virtual agent are dropped. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#drop_virtual_agent_messages GoogleDialogflowConversationProfile#drop_virtual_agent_messages}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c6458c1297e771b91da0733c933fdec144e05b1c3afb6bfc783bb33dfe8a5821)
            check_type(argname="argument drop_handoff_messages", value=drop_handoff_messages, expected_type=type_hints["drop_handoff_messages"])
            check_type(argname="argument drop_ivr_messages", value=drop_ivr_messages, expected_type=type_hints["drop_ivr_messages"])
            check_type(argname="argument drop_virtual_agent_messages", value=drop_virtual_agent_messages, expected_type=type_hints["drop_virtual_agent_messages"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if drop_handoff_messages is not None:
            self._values["drop_handoff_messages"] = drop_handoff_messages
        if drop_ivr_messages is not None:
            self._values["drop_ivr_messages"] = drop_ivr_messages
        if drop_virtual_agent_messages is not None:
            self._values["drop_virtual_agent_messages"] = drop_virtual_agent_messages

    @builtins.property
    def drop_handoff_messages(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If set to true, the last message from virtual agent (hand off message) and the message before it (trigger message of hand off) are dropped.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#drop_handoff_messages GoogleDialogflowConversationProfile#drop_handoff_messages}
        '''
        result = self._values.get("drop_handoff_messages")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def drop_ivr_messages(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If set to true, all messages from ivr stage are dropped.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#drop_ivr_messages GoogleDialogflowConversationProfile#drop_ivr_messages}
        '''
        result = self._values.get("drop_ivr_messages")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def drop_virtual_agent_messages(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If set to true, all messages from virtual agent are dropped.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#drop_virtual_agent_messages GoogleDialogflowConversationProfile#drop_virtual_agent_messages}
        '''
        result = self._values.get("drop_virtual_agent_messages")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfigContextFilterSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfigContextFilterSettingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDialogflowConversationProfile.GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfigContextFilterSettingsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__995a13129d2ae0d9f12df33f30ffe8f9c89fe9fd390e94b4088dd3d1b23bc36a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetDropHandoffMessages")
    def reset_drop_handoff_messages(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDropHandoffMessages", []))

    @jsii.member(jsii_name="resetDropIvrMessages")
    def reset_drop_ivr_messages(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDropIvrMessages", []))

    @jsii.member(jsii_name="resetDropVirtualAgentMessages")
    def reset_drop_virtual_agent_messages(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDropVirtualAgentMessages", []))

    @builtins.property
    @jsii.member(jsii_name="dropHandoffMessagesInput")
    def drop_handoff_messages_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "dropHandoffMessagesInput"))

    @builtins.property
    @jsii.member(jsii_name="dropIvrMessagesInput")
    def drop_ivr_messages_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "dropIvrMessagesInput"))

    @builtins.property
    @jsii.member(jsii_name="dropVirtualAgentMessagesInput")
    def drop_virtual_agent_messages_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "dropVirtualAgentMessagesInput"))

    @builtins.property
    @jsii.member(jsii_name="dropHandoffMessages")
    def drop_handoff_messages(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "dropHandoffMessages"))

    @drop_handoff_messages.setter
    def drop_handoff_messages(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8f303b3b564a3625529067a3107526e3c7faee27b7d22733cdf00f1c15c02f71)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dropHandoffMessages", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dropIvrMessages")
    def drop_ivr_messages(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "dropIvrMessages"))

    @drop_ivr_messages.setter
    def drop_ivr_messages(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__47f492f40496956328fa46cf0f6e573bdc31780dff539e00a0f13f75099bca50)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dropIvrMessages", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dropVirtualAgentMessages")
    def drop_virtual_agent_messages(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "dropVirtualAgentMessages"))

    @drop_virtual_agent_messages.setter
    def drop_virtual_agent_messages(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__17fa2f996bb470bd6b6a67f27870f58a1fdf3623f523a113aefd5a23532e759a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dropVirtualAgentMessages", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfigContextFilterSettings]:
        return typing.cast(typing.Optional[GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfigContextFilterSettings], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfigContextFilterSettings],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5771200000db2a8a3b094623ae3814225cceb0821f22347185146d5d1cc33351)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDialogflowConversationProfile.GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfigDialogflowQuerySource",
    jsii_struct_bases=[],
    name_mapping={"agent": "agent", "human_agent_side_config": "humanAgentSideConfig"},
)
class GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfigDialogflowQuerySource:
    def __init__(
        self,
        *,
        agent: builtins.str,
        human_agent_side_config: typing.Optional[typing.Union["GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfigDialogflowQuerySourceHumanAgentSideConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param agent: he name of a Dialogflow virtual agent used for end user side intent detection and suggestion. Format: projects//locations//agent. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#agent GoogleDialogflowConversationProfile#agent}
        :param human_agent_side_config: human_agent_side_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#human_agent_side_config GoogleDialogflowConversationProfile#human_agent_side_config}
        '''
        if isinstance(human_agent_side_config, dict):
            human_agent_side_config = GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfigDialogflowQuerySourceHumanAgentSideConfig(**human_agent_side_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0abef54c34982a8445fbb530c479d536f0730de48568f61b2c84b13be0740e62)
            check_type(argname="argument agent", value=agent, expected_type=type_hints["agent"])
            check_type(argname="argument human_agent_side_config", value=human_agent_side_config, expected_type=type_hints["human_agent_side_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "agent": agent,
        }
        if human_agent_side_config is not None:
            self._values["human_agent_side_config"] = human_agent_side_config

    @builtins.property
    def agent(self) -> builtins.str:
        '''he name of a Dialogflow virtual agent used for end user side intent detection and suggestion.

        Format: projects//locations//agent.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#agent GoogleDialogflowConversationProfile#agent}
        '''
        result = self._values.get("agent")
        assert result is not None, "Required property 'agent' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def human_agent_side_config(
        self,
    ) -> typing.Optional["GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfigDialogflowQuerySourceHumanAgentSideConfig"]:
        '''human_agent_side_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#human_agent_side_config GoogleDialogflowConversationProfile#human_agent_side_config}
        '''
        result = self._values.get("human_agent_side_config")
        return typing.cast(typing.Optional["GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfigDialogflowQuerySourceHumanAgentSideConfig"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfigDialogflowQuerySource(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDialogflowConversationProfile.GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfigDialogflowQuerySourceHumanAgentSideConfig",
    jsii_struct_bases=[],
    name_mapping={"agent": "agent"},
)
class GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfigDialogflowQuerySourceHumanAgentSideConfig:
    def __init__(self, *, agent: typing.Optional[builtins.str] = None) -> None:
        '''
        :param agent: The name of a dialogflow virtual agent used for intent detection and suggestion triggered by human agent. Format: projects//locations//agent. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#agent GoogleDialogflowConversationProfile#agent}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__50ded44e1b188f6b56ab2e6d5fa91273828d94de099d1bf3b70e6179c583d28f)
            check_type(argname="argument agent", value=agent, expected_type=type_hints["agent"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if agent is not None:
            self._values["agent"] = agent

    @builtins.property
    def agent(self) -> typing.Optional[builtins.str]:
        '''The name of a dialogflow virtual agent used for intent detection and suggestion triggered by human agent.

        Format: projects//locations//agent.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#agent GoogleDialogflowConversationProfile#agent}
        '''
        result = self._values.get("agent")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfigDialogflowQuerySourceHumanAgentSideConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfigDialogflowQuerySourceHumanAgentSideConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDialogflowConversationProfile.GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfigDialogflowQuerySourceHumanAgentSideConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7a0d1abbae4726112987612da4c60532a5c59c2dee2b6f19539e0a3fc39222fb)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAgent")
    def reset_agent(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAgent", []))

    @builtins.property
    @jsii.member(jsii_name="agentInput")
    def agent_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "agentInput"))

    @builtins.property
    @jsii.member(jsii_name="agent")
    def agent(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "agent"))

    @agent.setter
    def agent(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__11e0e820c58447988345c0daf9ffc8c4cf50b448970eb2f4fc7eb5268092eee5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "agent", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfigDialogflowQuerySourceHumanAgentSideConfig]:
        return typing.cast(typing.Optional[GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfigDialogflowQuerySourceHumanAgentSideConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfigDialogflowQuerySourceHumanAgentSideConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4729788b6358e1a1b99901bec976a6e4520970838e0287f4182db73c5a3261ec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfigDialogflowQuerySourceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDialogflowConversationProfile.GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfigDialogflowQuerySourceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f62789ddc6e30febb411d153668ef9cbac1ae15126d477729d499b1e21b7df57)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putHumanAgentSideConfig")
    def put_human_agent_side_config(
        self,
        *,
        agent: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param agent: The name of a dialogflow virtual agent used for intent detection and suggestion triggered by human agent. Format: projects//locations//agent. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#agent GoogleDialogflowConversationProfile#agent}
        '''
        value = GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfigDialogflowQuerySourceHumanAgentSideConfig(
            agent=agent
        )

        return typing.cast(None, jsii.invoke(self, "putHumanAgentSideConfig", [value]))

    @jsii.member(jsii_name="resetHumanAgentSideConfig")
    def reset_human_agent_side_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHumanAgentSideConfig", []))

    @builtins.property
    @jsii.member(jsii_name="humanAgentSideConfig")
    def human_agent_side_config(
        self,
    ) -> GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfigDialogflowQuerySourceHumanAgentSideConfigOutputReference:
        return typing.cast(GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfigDialogflowQuerySourceHumanAgentSideConfigOutputReference, jsii.get(self, "humanAgentSideConfig"))

    @builtins.property
    @jsii.member(jsii_name="agentInput")
    def agent_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "agentInput"))

    @builtins.property
    @jsii.member(jsii_name="humanAgentSideConfigInput")
    def human_agent_side_config_input(
        self,
    ) -> typing.Optional[GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfigDialogflowQuerySourceHumanAgentSideConfig]:
        return typing.cast(typing.Optional[GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfigDialogflowQuerySourceHumanAgentSideConfig], jsii.get(self, "humanAgentSideConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="agent")
    def agent(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "agent"))

    @agent.setter
    def agent(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f390316257049d29f8def2da344dcef53c7da8a55d72d9d4f5b0694c7f986f0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "agent", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfigDialogflowQuerySource]:
        return typing.cast(typing.Optional[GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfigDialogflowQuerySource], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfigDialogflowQuerySource],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c2fd2dca90c48f7c26d38c362a83e491ec03f977b3b107079fa0c317e7a5ac0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDialogflowConversationProfile.GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfigDocumentQuerySource",
    jsii_struct_bases=[],
    name_mapping={"documents": "documents"},
)
class GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfigDocumentQuerySource:
    def __init__(self, *, documents: typing.Sequence[builtins.str]) -> None:
        '''
        :param documents: Knowledge documents to query from. Format: projects//locations//knowledgeBases//documents/. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#documents GoogleDialogflowConversationProfile#documents}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e00dd1ee4be88ac923a01fdb3db047be4a4fab3b79450221e2fc240155705d92)
            check_type(argname="argument documents", value=documents, expected_type=type_hints["documents"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "documents": documents,
        }

    @builtins.property
    def documents(self) -> typing.List[builtins.str]:
        '''Knowledge documents to query from. Format: projects//locations//knowledgeBases//documents/.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#documents GoogleDialogflowConversationProfile#documents}
        '''
        result = self._values.get("documents")
        assert result is not None, "Required property 'documents' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfigDocumentQuerySource(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfigDocumentQuerySourceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDialogflowConversationProfile.GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfigDocumentQuerySourceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d1cbf19b265fdd026252b6106c9fba7b2005b41a91f860310950f4e6d035789f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="documentsInput")
    def documents_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "documentsInput"))

    @builtins.property
    @jsii.member(jsii_name="documents")
    def documents(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "documents"))

    @documents.setter
    def documents(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__66a48c0d08d10fd48db4120fbce805a325cfad22360350ffabbc5410efdb8cb6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "documents", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfigDocumentQuerySource]:
        return typing.cast(typing.Optional[GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfigDocumentQuerySource], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfigDocumentQuerySource],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8f2a674fbdab335e8c8226fd0b1670564aca60383471269d49c265c02256441a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDialogflowConversationProfile.GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfigKnowledgeBaseQuerySource",
    jsii_struct_bases=[],
    name_mapping={"knowledge_bases": "knowledgeBases"},
)
class GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfigKnowledgeBaseQuerySource:
    def __init__(self, *, knowledge_bases: typing.Sequence[builtins.str]) -> None:
        '''
        :param knowledge_bases: Knowledge bases to query. Format: projects//locations//knowledgeBases/. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#knowledge_bases GoogleDialogflowConversationProfile#knowledge_bases}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8cc6012357dfd3132af13ad6ae40e9c803cf66fe80ba45df7c849f5bc5c05a95)
            check_type(argname="argument knowledge_bases", value=knowledge_bases, expected_type=type_hints["knowledge_bases"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "knowledge_bases": knowledge_bases,
        }

    @builtins.property
    def knowledge_bases(self) -> typing.List[builtins.str]:
        '''Knowledge bases to query. Format: projects//locations//knowledgeBases/.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#knowledge_bases GoogleDialogflowConversationProfile#knowledge_bases}
        '''
        result = self._values.get("knowledge_bases")
        assert result is not None, "Required property 'knowledge_bases' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfigKnowledgeBaseQuerySource(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfigKnowledgeBaseQuerySourceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDialogflowConversationProfile.GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfigKnowledgeBaseQuerySourceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7e5437347804d9daaa24b3cffa55159a1f8b3f32772922ddf5434b258ccef13f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="knowledgeBasesInput")
    def knowledge_bases_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "knowledgeBasesInput"))

    @builtins.property
    @jsii.member(jsii_name="knowledgeBases")
    def knowledge_bases(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "knowledgeBases"))

    @knowledge_bases.setter
    def knowledge_bases(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4aeb1e667a3c7d42ae731cc463bab66cd47e293a078ccbe0d99a83908b03b4ff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "knowledgeBases", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfigKnowledgeBaseQuerySource]:
        return typing.cast(typing.Optional[GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfigKnowledgeBaseQuerySource], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfigKnowledgeBaseQuerySource],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4ff750a7028f0788ab1cf5c66555ca9c3d036871a6dee3c296413a80641ac5a5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDialogflowConversationProfile.GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__61800be705f3f58af0640115cd800ab55802123cfe4cf9906bf27b2e3821e5f6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putContextFilterSettings")
    def put_context_filter_settings(
        self,
        *,
        drop_handoff_messages: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        drop_ivr_messages: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        drop_virtual_agent_messages: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param drop_handoff_messages: If set to true, the last message from virtual agent (hand off message) and the message before it (trigger message of hand off) are dropped. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#drop_handoff_messages GoogleDialogflowConversationProfile#drop_handoff_messages}
        :param drop_ivr_messages: If set to true, all messages from ivr stage are dropped. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#drop_ivr_messages GoogleDialogflowConversationProfile#drop_ivr_messages}
        :param drop_virtual_agent_messages: If set to true, all messages from virtual agent are dropped. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#drop_virtual_agent_messages GoogleDialogflowConversationProfile#drop_virtual_agent_messages}
        '''
        value = GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfigContextFilterSettings(
            drop_handoff_messages=drop_handoff_messages,
            drop_ivr_messages=drop_ivr_messages,
            drop_virtual_agent_messages=drop_virtual_agent_messages,
        )

        return typing.cast(None, jsii.invoke(self, "putContextFilterSettings", [value]))

    @jsii.member(jsii_name="putDialogflowQuerySource")
    def put_dialogflow_query_source(
        self,
        *,
        agent: builtins.str,
        human_agent_side_config: typing.Optional[typing.Union[GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfigDialogflowQuerySourceHumanAgentSideConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param agent: he name of a Dialogflow virtual agent used for end user side intent detection and suggestion. Format: projects//locations//agent. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#agent GoogleDialogflowConversationProfile#agent}
        :param human_agent_side_config: human_agent_side_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#human_agent_side_config GoogleDialogflowConversationProfile#human_agent_side_config}
        '''
        value = GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfigDialogflowQuerySource(
            agent=agent, human_agent_side_config=human_agent_side_config
        )

        return typing.cast(None, jsii.invoke(self, "putDialogflowQuerySource", [value]))

    @jsii.member(jsii_name="putDocumentQuerySource")
    def put_document_query_source(
        self,
        *,
        documents: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param documents: Knowledge documents to query from. Format: projects//locations//knowledgeBases//documents/. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#documents GoogleDialogflowConversationProfile#documents}
        '''
        value = GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfigDocumentQuerySource(
            documents=documents
        )

        return typing.cast(None, jsii.invoke(self, "putDocumentQuerySource", [value]))

    @jsii.member(jsii_name="putKnowledgeBaseQuerySource")
    def put_knowledge_base_query_source(
        self,
        *,
        knowledge_bases: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param knowledge_bases: Knowledge bases to query. Format: projects//locations//knowledgeBases/. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#knowledge_bases GoogleDialogflowConversationProfile#knowledge_bases}
        '''
        value = GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfigKnowledgeBaseQuerySource(
            knowledge_bases=knowledge_bases
        )

        return typing.cast(None, jsii.invoke(self, "putKnowledgeBaseQuerySource", [value]))

    @jsii.member(jsii_name="putSections")
    def put_sections(
        self,
        *,
        section_types: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param section_types: The selected sections chosen to return when requesting a summary of a conversation If not provided the default selection will be "{SITUATION, ACTION, RESULT}". Possible values: ["SECTION_TYPE_UNSPECIFIED", "SITUATION", "ACTION", "RESOLUTION", "REASON_FOR_CANCELLATION", "CUSTOMER_SATISFACTION", "ENTITIES"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#section_types GoogleDialogflowConversationProfile#section_types}
        '''
        value = GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfigSections(
            section_types=section_types
        )

        return typing.cast(None, jsii.invoke(self, "putSections", [value]))

    @jsii.member(jsii_name="resetConfidenceThreshold")
    def reset_confidence_threshold(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConfidenceThreshold", []))

    @jsii.member(jsii_name="resetContextFilterSettings")
    def reset_context_filter_settings(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetContextFilterSettings", []))

    @jsii.member(jsii_name="resetDialogflowQuerySource")
    def reset_dialogflow_query_source(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDialogflowQuerySource", []))

    @jsii.member(jsii_name="resetDocumentQuerySource")
    def reset_document_query_source(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDocumentQuerySource", []))

    @jsii.member(jsii_name="resetKnowledgeBaseQuerySource")
    def reset_knowledge_base_query_source(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKnowledgeBaseQuerySource", []))

    @jsii.member(jsii_name="resetMaxResults")
    def reset_max_results(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxResults", []))

    @jsii.member(jsii_name="resetSections")
    def reset_sections(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSections", []))

    @builtins.property
    @jsii.member(jsii_name="contextFilterSettings")
    def context_filter_settings(
        self,
    ) -> GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfigContextFilterSettingsOutputReference:
        return typing.cast(GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfigContextFilterSettingsOutputReference, jsii.get(self, "contextFilterSettings"))

    @builtins.property
    @jsii.member(jsii_name="dialogflowQuerySource")
    def dialogflow_query_source(
        self,
    ) -> GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfigDialogflowQuerySourceOutputReference:
        return typing.cast(GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfigDialogflowQuerySourceOutputReference, jsii.get(self, "dialogflowQuerySource"))

    @builtins.property
    @jsii.member(jsii_name="documentQuerySource")
    def document_query_source(
        self,
    ) -> GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfigDocumentQuerySourceOutputReference:
        return typing.cast(GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfigDocumentQuerySourceOutputReference, jsii.get(self, "documentQuerySource"))

    @builtins.property
    @jsii.member(jsii_name="knowledgeBaseQuerySource")
    def knowledge_base_query_source(
        self,
    ) -> GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfigKnowledgeBaseQuerySourceOutputReference:
        return typing.cast(GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfigKnowledgeBaseQuerySourceOutputReference, jsii.get(self, "knowledgeBaseQuerySource"))

    @builtins.property
    @jsii.member(jsii_name="sections")
    def sections(
        self,
    ) -> "GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfigSectionsOutputReference":
        return typing.cast("GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfigSectionsOutputReference", jsii.get(self, "sections"))

    @builtins.property
    @jsii.member(jsii_name="confidenceThresholdInput")
    def confidence_threshold_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "confidenceThresholdInput"))

    @builtins.property
    @jsii.member(jsii_name="contextFilterSettingsInput")
    def context_filter_settings_input(
        self,
    ) -> typing.Optional[GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfigContextFilterSettings]:
        return typing.cast(typing.Optional[GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfigContextFilterSettings], jsii.get(self, "contextFilterSettingsInput"))

    @builtins.property
    @jsii.member(jsii_name="dialogflowQuerySourceInput")
    def dialogflow_query_source_input(
        self,
    ) -> typing.Optional[GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfigDialogflowQuerySource]:
        return typing.cast(typing.Optional[GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfigDialogflowQuerySource], jsii.get(self, "dialogflowQuerySourceInput"))

    @builtins.property
    @jsii.member(jsii_name="documentQuerySourceInput")
    def document_query_source_input(
        self,
    ) -> typing.Optional[GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfigDocumentQuerySource]:
        return typing.cast(typing.Optional[GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfigDocumentQuerySource], jsii.get(self, "documentQuerySourceInput"))

    @builtins.property
    @jsii.member(jsii_name="knowledgeBaseQuerySourceInput")
    def knowledge_base_query_source_input(
        self,
    ) -> typing.Optional[GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfigKnowledgeBaseQuerySource]:
        return typing.cast(typing.Optional[GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfigKnowledgeBaseQuerySource], jsii.get(self, "knowledgeBaseQuerySourceInput"))

    @builtins.property
    @jsii.member(jsii_name="maxResultsInput")
    def max_results_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxResultsInput"))

    @builtins.property
    @jsii.member(jsii_name="sectionsInput")
    def sections_input(
        self,
    ) -> typing.Optional["GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfigSections"]:
        return typing.cast(typing.Optional["GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfigSections"], jsii.get(self, "sectionsInput"))

    @builtins.property
    @jsii.member(jsii_name="confidenceThreshold")
    def confidence_threshold(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "confidenceThreshold"))

    @confidence_threshold.setter
    def confidence_threshold(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e8947530bfd0f85fd2bf5332cfb20d3656bc54b9edc4389ce0d350f49ac47b95)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "confidenceThreshold", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxResults")
    def max_results(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxResults"))

    @max_results.setter
    def max_results(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d1af5c91de2985ccdf9bd75ddde47f4bcae5146659bb04384d9e35ee145c60e0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxResults", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfig]:
        return typing.cast(typing.Optional[GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5bd6eeafc453a33f6bd1bd6dfed8870b09a72cd4b94330bc45fb7329b8ddab3a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDialogflowConversationProfile.GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfigSections",
    jsii_struct_bases=[],
    name_mapping={"section_types": "sectionTypes"},
)
class GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfigSections:
    def __init__(
        self,
        *,
        section_types: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param section_types: The selected sections chosen to return when requesting a summary of a conversation If not provided the default selection will be "{SITUATION, ACTION, RESULT}". Possible values: ["SECTION_TYPE_UNSPECIFIED", "SITUATION", "ACTION", "RESOLUTION", "REASON_FOR_CANCELLATION", "CUSTOMER_SATISFACTION", "ENTITIES"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#section_types GoogleDialogflowConversationProfile#section_types}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d553d2c1d236bb3fc2595320bc3fc213c01d7dd4fcd472734c6c552d075b2c0e)
            check_type(argname="argument section_types", value=section_types, expected_type=type_hints["section_types"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if section_types is not None:
            self._values["section_types"] = section_types

    @builtins.property
    def section_types(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The selected sections chosen to return when requesting a summary of a conversation If not provided the default selection will be "{SITUATION, ACTION, RESULT}".

        Possible values: ["SECTION_TYPE_UNSPECIFIED", "SITUATION", "ACTION", "RESOLUTION", "REASON_FOR_CANCELLATION", "CUSTOMER_SATISFACTION", "ENTITIES"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#section_types GoogleDialogflowConversationProfile#section_types}
        '''
        result = self._values.get("section_types")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfigSections(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfigSectionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDialogflowConversationProfile.GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfigSectionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f2576565488cae4a3313344724ea25480d1618fc65abbacf27d87c5086cd88d1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetSectionTypes")
    def reset_section_types(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSectionTypes", []))

    @builtins.property
    @jsii.member(jsii_name="sectionTypesInput")
    def section_types_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "sectionTypesInput"))

    @builtins.property
    @jsii.member(jsii_name="sectionTypes")
    def section_types(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "sectionTypes"))

    @section_types.setter
    def section_types(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4cdcc62bc7e4aeab04be6f812faa4f7d4a83f1f1ebd9eb076e42126e7bec14d9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sectionTypes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfigSections]:
        return typing.cast(typing.Optional[GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfigSections], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfigSections],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c1127eca952e7e4895891d09c3e9f8c2c4734abc361f52facd7cddaa4e5890b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDialogflowConversationProfile.GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsSuggestionFeature",
    jsii_struct_bases=[],
    name_mapping={"type": "type"},
)
class GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsSuggestionFeature:
    def __init__(self, *, type: typing.Optional[builtins.str] = None) -> None:
        '''
        :param type: Type of Human Agent Assistant API feature to request. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#type GoogleDialogflowConversationProfile#type}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a57996091da5d0b5e55c8507f70a9d450970612ef085c6b9b5281006623249d)
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if type is not None:
            self._values["type"] = type

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''Type of Human Agent Assistant API feature to request.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#type GoogleDialogflowConversationProfile#type}
        '''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsSuggestionFeature(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsSuggestionFeatureOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDialogflowConversationProfile.GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsSuggestionFeatureOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b041f7f59210c2259eb893933c1eefa9986336aa4d178030e88952d8a1e83504)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetType")
    def reset_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetType", []))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a4dab3df91fdd5429624bdc2cec92111722eaadff930690aa769ee793527770)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsSuggestionFeature]:
        return typing.cast(typing.Optional[GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsSuggestionFeature], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsSuggestionFeature],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6ac7965b16cd2e873fbb29702ebf024025c3f4cba045c06cdb4c98fcf015826b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDialogflowConversationProfile.GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsSuggestionTriggerSettings",
    jsii_struct_bases=[],
    name_mapping={"no_small_talk": "noSmallTalk", "only_end_user": "onlyEndUser"},
)
class GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsSuggestionTriggerSettings:
    def __init__(
        self,
        *,
        no_small_talk: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        only_end_user: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param no_small_talk: Do not trigger if last utterance is small talk. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#no_small_talk GoogleDialogflowConversationProfile#no_small_talk}
        :param only_end_user: Only trigger suggestion if participant role of last utterance is END_USER. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#only_end_user GoogleDialogflowConversationProfile#only_end_user}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cfd7296600756b6d79e7d11d26c6699eb3c5e54efe063e0d15776ec3fd2554f6)
            check_type(argname="argument no_small_talk", value=no_small_talk, expected_type=type_hints["no_small_talk"])
            check_type(argname="argument only_end_user", value=only_end_user, expected_type=type_hints["only_end_user"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if no_small_talk is not None:
            self._values["no_small_talk"] = no_small_talk
        if only_end_user is not None:
            self._values["only_end_user"] = only_end_user

    @builtins.property
    def no_small_talk(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Do not trigger if last utterance is small talk.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#no_small_talk GoogleDialogflowConversationProfile#no_small_talk}
        '''
        result = self._values.get("no_small_talk")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def only_end_user(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Only trigger suggestion if participant role of last utterance is END_USER.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#only_end_user GoogleDialogflowConversationProfile#only_end_user}
        '''
        result = self._values.get("only_end_user")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsSuggestionTriggerSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsSuggestionTriggerSettingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDialogflowConversationProfile.GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsSuggestionTriggerSettingsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2b76608cc1fe7e9496dd958db8e6e4af64a4b37b4de78142399f6ef5f52325eb)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetNoSmallTalk")
    def reset_no_small_talk(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNoSmallTalk", []))

    @jsii.member(jsii_name="resetOnlyEndUser")
    def reset_only_end_user(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOnlyEndUser", []))

    @builtins.property
    @jsii.member(jsii_name="noSmallTalkInput")
    def no_small_talk_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "noSmallTalkInput"))

    @builtins.property
    @jsii.member(jsii_name="onlyEndUserInput")
    def only_end_user_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "onlyEndUserInput"))

    @builtins.property
    @jsii.member(jsii_name="noSmallTalk")
    def no_small_talk(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "noSmallTalk"))

    @no_small_talk.setter
    def no_small_talk(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cb484c809bde4076fec7f1c6764a8cbc01d79ac0b2496b10ac113a26ce1aeddc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "noSmallTalk", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="onlyEndUser")
    def only_end_user(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "onlyEndUser"))

    @only_end_user.setter
    def only_end_user(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__740b55cbeeab97cc2a7b66b143f8d324f0126296ffb14524811f97b9825afe57)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "onlyEndUser", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsSuggestionTriggerSettings]:
        return typing.cast(typing.Optional[GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsSuggestionTriggerSettings], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsSuggestionTriggerSettings],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c5b79d1a7c36a8507360ac159b0090eaf1cd6d44317b4ec3a1ee1a639673c8e5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDialogflowConversationProfile.GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ad6edda364698814cd15efbd2372f270f2777b6d16152724e66b9f3346926b92)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putFeatureConfigs")
    def put_feature_configs(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigs, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aaac5d869cfbbaa01a5bdb15ffb589b2c1ab959a967d4a60fd39e5974e0ab8d3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putFeatureConfigs", [value]))

    @jsii.member(jsii_name="resetDisableHighLatencyFeaturesSyncDelivery")
    def reset_disable_high_latency_features_sync_delivery(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDisableHighLatencyFeaturesSyncDelivery", []))

    @jsii.member(jsii_name="resetFeatureConfigs")
    def reset_feature_configs(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFeatureConfigs", []))

    @jsii.member(jsii_name="resetGenerators")
    def reset_generators(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGenerators", []))

    @jsii.member(jsii_name="resetGroupSuggestionResponses")
    def reset_group_suggestion_responses(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGroupSuggestionResponses", []))

    @builtins.property
    @jsii.member(jsii_name="featureConfigs")
    def feature_configs(
        self,
    ) -> GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsList:
        return typing.cast(GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsList, jsii.get(self, "featureConfigs"))

    @builtins.property
    @jsii.member(jsii_name="disableHighLatencyFeaturesSyncDeliveryInput")
    def disable_high_latency_features_sync_delivery_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "disableHighLatencyFeaturesSyncDeliveryInput"))

    @builtins.property
    @jsii.member(jsii_name="featureConfigsInput")
    def feature_configs_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigs]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigs]]], jsii.get(self, "featureConfigsInput"))

    @builtins.property
    @jsii.member(jsii_name="generatorsInput")
    def generators_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "generatorsInput"))

    @builtins.property
    @jsii.member(jsii_name="groupSuggestionResponsesInput")
    def group_suggestion_responses_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "groupSuggestionResponsesInput"))

    @builtins.property
    @jsii.member(jsii_name="disableHighLatencyFeaturesSyncDelivery")
    def disable_high_latency_features_sync_delivery(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "disableHighLatencyFeaturesSyncDelivery"))

    @disable_high_latency_features_sync_delivery.setter
    def disable_high_latency_features_sync_delivery(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__54708dd6c43fb2e0f4ad8ffd8e054938cd1b687c4388f9cced2600674416a847)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "disableHighLatencyFeaturesSyncDelivery", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="generators")
    def generators(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "generators"))

    @generators.setter
    def generators(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__56ec680add0e949d4a99f52ff63a50f69eb6c0d4d77f7ff801a3519463c3b6bc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "generators", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="groupSuggestionResponses")
    def group_suggestion_responses(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "groupSuggestionResponses"))

    @group_suggestion_responses.setter
    def group_suggestion_responses(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e79db7c9fcfcd6de8ab20a3a6d08438610a39152e68df860c528d04974e7a78)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "groupSuggestionResponses", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfig]:
        return typing.cast(typing.Optional[GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4b06ff4921c9573a3ff7e2db6420fa96104ca3569d573182020a8faabd26a543)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDialogflowConversationProfile.GoogleDialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfig",
    jsii_struct_bases=[],
    name_mapping={
        "disable_high_latency_features_sync_delivery": "disableHighLatencyFeaturesSyncDelivery",
        "feature_configs": "featureConfigs",
        "generators": "generators",
        "group_suggestion_responses": "groupSuggestionResponses",
    },
)
class GoogleDialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfig:
    def __init__(
        self,
        *,
        disable_high_latency_features_sync_delivery: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        feature_configs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleDialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigs", typing.Dict[builtins.str, typing.Any]]]]] = None,
        generators: typing.Optional[typing.Sequence[builtins.str]] = None,
        group_suggestion_responses: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param disable_high_latency_features_sync_delivery: When disableHighLatencyFeaturesSyncDelivery is true and using the AnalyzeContent API, we will not deliver the responses from high latency features in the API response. The humanAgentAssistantConfig.notification_config must be configured and enableEventBasedSuggestion must be set to true to receive the responses from high latency features in Pub/Sub. High latency feature(s): KNOWLEDGE_ASSIST Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#disable_high_latency_features_sync_delivery GoogleDialogflowConversationProfile#disable_high_latency_features_sync_delivery}
        :param feature_configs: feature_configs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#feature_configs GoogleDialogflowConversationProfile#feature_configs}
        :param generators: List of various generator resource names used in the conversation profile. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#generators GoogleDialogflowConversationProfile#generators}
        :param group_suggestion_responses: If groupSuggestionResponses is false, and there are multiple featureConfigs in event based suggestion or StreamingAnalyzeContent, we will try to deliver suggestions to customers as soon as we get new suggestion. Different type of suggestions based on the same context will be in separate Pub/Sub event or StreamingAnalyzeContentResponse. If groupSuggestionResponses set to true. All the suggestions to the same participant based on the same context will be grouped into a single Pub/Sub event or StreamingAnalyzeContentResponse. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#group_suggestion_responses GoogleDialogflowConversationProfile#group_suggestion_responses}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3f9f2892b20edff1dca277f92722d47590deb0e297c12101121d8a25d6c3fc11)
            check_type(argname="argument disable_high_latency_features_sync_delivery", value=disable_high_latency_features_sync_delivery, expected_type=type_hints["disable_high_latency_features_sync_delivery"])
            check_type(argname="argument feature_configs", value=feature_configs, expected_type=type_hints["feature_configs"])
            check_type(argname="argument generators", value=generators, expected_type=type_hints["generators"])
            check_type(argname="argument group_suggestion_responses", value=group_suggestion_responses, expected_type=type_hints["group_suggestion_responses"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if disable_high_latency_features_sync_delivery is not None:
            self._values["disable_high_latency_features_sync_delivery"] = disable_high_latency_features_sync_delivery
        if feature_configs is not None:
            self._values["feature_configs"] = feature_configs
        if generators is not None:
            self._values["generators"] = generators
        if group_suggestion_responses is not None:
            self._values["group_suggestion_responses"] = group_suggestion_responses

    @builtins.property
    def disable_high_latency_features_sync_delivery(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''When disableHighLatencyFeaturesSyncDelivery is true and using the AnalyzeContent API, we will not deliver the responses from high latency features in the API response.

        The humanAgentAssistantConfig.notification_config must be configured and enableEventBasedSuggestion must be set to true to receive the responses from high latency features in Pub/Sub. High latency feature(s): KNOWLEDGE_ASSIST

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#disable_high_latency_features_sync_delivery GoogleDialogflowConversationProfile#disable_high_latency_features_sync_delivery}
        '''
        result = self._values.get("disable_high_latency_features_sync_delivery")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def feature_configs(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleDialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigs"]]]:
        '''feature_configs block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#feature_configs GoogleDialogflowConversationProfile#feature_configs}
        '''
        result = self._values.get("feature_configs")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleDialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigs"]]], result)

    @builtins.property
    def generators(self) -> typing.Optional[typing.List[builtins.str]]:
        '''List of various generator resource names used in the conversation profile.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#generators GoogleDialogflowConversationProfile#generators}
        '''
        result = self._values.get("generators")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def group_suggestion_responses(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If groupSuggestionResponses is false, and there are multiple featureConfigs in event based suggestion or StreamingAnalyzeContent, we will try to deliver suggestions to customers as soon as we get new suggestion.

        Different type of suggestions based on the same context will be in separate Pub/Sub event or StreamingAnalyzeContentResponse.

        If groupSuggestionResponses set to true. All the suggestions to the same participant based on the same context will be grouped into a single Pub/Sub event or StreamingAnalyzeContentResponse.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#group_suggestion_responses GoogleDialogflowConversationProfile#group_suggestion_responses}
        '''
        result = self._values.get("group_suggestion_responses")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDialogflowConversationProfile.GoogleDialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigs",
    jsii_struct_bases=[],
    name_mapping={
        "conversation_model_config": "conversationModelConfig",
        "conversation_process_config": "conversationProcessConfig",
        "disable_agent_query_logging": "disableAgentQueryLogging",
        "enable_conversation_augmented_query": "enableConversationAugmentedQuery",
        "enable_event_based_suggestion": "enableEventBasedSuggestion",
        "enable_query_suggestion_only": "enableQuerySuggestionOnly",
        "enable_query_suggestion_when_no_answer": "enableQuerySuggestionWhenNoAnswer",
        "query_config": "queryConfig",
        "suggestion_feature": "suggestionFeature",
        "suggestion_trigger_settings": "suggestionTriggerSettings",
    },
)
class GoogleDialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigs:
    def __init__(
        self,
        *,
        conversation_model_config: typing.Optional[typing.Union["GoogleDialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsConversationModelConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        conversation_process_config: typing.Optional[typing.Union["GoogleDialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsConversationProcessConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        disable_agent_query_logging: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_conversation_augmented_query: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_event_based_suggestion: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_query_suggestion_only: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_query_suggestion_when_no_answer: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        query_config: typing.Optional[typing.Union["GoogleDialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsQueryConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        suggestion_feature: typing.Optional[typing.Union["GoogleDialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsSuggestionFeature", typing.Dict[builtins.str, typing.Any]]] = None,
        suggestion_trigger_settings: typing.Optional[typing.Union["GoogleDialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsSuggestionTriggerSettings", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param conversation_model_config: conversation_model_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#conversation_model_config GoogleDialogflowConversationProfile#conversation_model_config}
        :param conversation_process_config: conversation_process_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#conversation_process_config GoogleDialogflowConversationProfile#conversation_process_config}
        :param disable_agent_query_logging: Disable the logging of search queries sent by human agents. It can prevent those queries from being stored at answer records. This feature is only supported for types: KNOWLEDGE_SEARCH. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#disable_agent_query_logging GoogleDialogflowConversationProfile#disable_agent_query_logging}
        :param enable_conversation_augmented_query: Enable including conversation context during query answer generation. This feature is only supported for types: KNOWLEDGE_SEARCH. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#enable_conversation_augmented_query GoogleDialogflowConversationProfile#enable_conversation_augmented_query}
        :param enable_event_based_suggestion: Automatically iterates all participants and tries to compile suggestions. This feature is only supported for types: ARTICLE_SUGGESTION, FAQ, DIALOGFLOW_ASSIST, KNOWLEDGE_ASSIST. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#enable_event_based_suggestion GoogleDialogflowConversationProfile#enable_event_based_suggestion}
        :param enable_query_suggestion_only: Enable query suggestion only. This feature is only supported for types: KNOWLEDGE_ASSIST. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#enable_query_suggestion_only GoogleDialogflowConversationProfile#enable_query_suggestion_only}
        :param enable_query_suggestion_when_no_answer: Enable query suggestion even if we can't find its answer. By default, queries are suggested only if we find its answer. This feature is only supported for types: KNOWLEDGE_ASSIST. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#enable_query_suggestion_when_no_answer GoogleDialogflowConversationProfile#enable_query_suggestion_when_no_answer}
        :param query_config: query_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#query_config GoogleDialogflowConversationProfile#query_config}
        :param suggestion_feature: suggestion_feature block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#suggestion_feature GoogleDialogflowConversationProfile#suggestion_feature}
        :param suggestion_trigger_settings: suggestion_trigger_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#suggestion_trigger_settings GoogleDialogflowConversationProfile#suggestion_trigger_settings}
        '''
        if isinstance(conversation_model_config, dict):
            conversation_model_config = GoogleDialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsConversationModelConfig(**conversation_model_config)
        if isinstance(conversation_process_config, dict):
            conversation_process_config = GoogleDialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsConversationProcessConfig(**conversation_process_config)
        if isinstance(query_config, dict):
            query_config = GoogleDialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsQueryConfig(**query_config)
        if isinstance(suggestion_feature, dict):
            suggestion_feature = GoogleDialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsSuggestionFeature(**suggestion_feature)
        if isinstance(suggestion_trigger_settings, dict):
            suggestion_trigger_settings = GoogleDialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsSuggestionTriggerSettings(**suggestion_trigger_settings)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__76b189e81965539bfd1a9158b08ff82cf1c836159474da7c472880b046c44d0b)
            check_type(argname="argument conversation_model_config", value=conversation_model_config, expected_type=type_hints["conversation_model_config"])
            check_type(argname="argument conversation_process_config", value=conversation_process_config, expected_type=type_hints["conversation_process_config"])
            check_type(argname="argument disable_agent_query_logging", value=disable_agent_query_logging, expected_type=type_hints["disable_agent_query_logging"])
            check_type(argname="argument enable_conversation_augmented_query", value=enable_conversation_augmented_query, expected_type=type_hints["enable_conversation_augmented_query"])
            check_type(argname="argument enable_event_based_suggestion", value=enable_event_based_suggestion, expected_type=type_hints["enable_event_based_suggestion"])
            check_type(argname="argument enable_query_suggestion_only", value=enable_query_suggestion_only, expected_type=type_hints["enable_query_suggestion_only"])
            check_type(argname="argument enable_query_suggestion_when_no_answer", value=enable_query_suggestion_when_no_answer, expected_type=type_hints["enable_query_suggestion_when_no_answer"])
            check_type(argname="argument query_config", value=query_config, expected_type=type_hints["query_config"])
            check_type(argname="argument suggestion_feature", value=suggestion_feature, expected_type=type_hints["suggestion_feature"])
            check_type(argname="argument suggestion_trigger_settings", value=suggestion_trigger_settings, expected_type=type_hints["suggestion_trigger_settings"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if conversation_model_config is not None:
            self._values["conversation_model_config"] = conversation_model_config
        if conversation_process_config is not None:
            self._values["conversation_process_config"] = conversation_process_config
        if disable_agent_query_logging is not None:
            self._values["disable_agent_query_logging"] = disable_agent_query_logging
        if enable_conversation_augmented_query is not None:
            self._values["enable_conversation_augmented_query"] = enable_conversation_augmented_query
        if enable_event_based_suggestion is not None:
            self._values["enable_event_based_suggestion"] = enable_event_based_suggestion
        if enable_query_suggestion_only is not None:
            self._values["enable_query_suggestion_only"] = enable_query_suggestion_only
        if enable_query_suggestion_when_no_answer is not None:
            self._values["enable_query_suggestion_when_no_answer"] = enable_query_suggestion_when_no_answer
        if query_config is not None:
            self._values["query_config"] = query_config
        if suggestion_feature is not None:
            self._values["suggestion_feature"] = suggestion_feature
        if suggestion_trigger_settings is not None:
            self._values["suggestion_trigger_settings"] = suggestion_trigger_settings

    @builtins.property
    def conversation_model_config(
        self,
    ) -> typing.Optional["GoogleDialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsConversationModelConfig"]:
        '''conversation_model_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#conversation_model_config GoogleDialogflowConversationProfile#conversation_model_config}
        '''
        result = self._values.get("conversation_model_config")
        return typing.cast(typing.Optional["GoogleDialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsConversationModelConfig"], result)

    @builtins.property
    def conversation_process_config(
        self,
    ) -> typing.Optional["GoogleDialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsConversationProcessConfig"]:
        '''conversation_process_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#conversation_process_config GoogleDialogflowConversationProfile#conversation_process_config}
        '''
        result = self._values.get("conversation_process_config")
        return typing.cast(typing.Optional["GoogleDialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsConversationProcessConfig"], result)

    @builtins.property
    def disable_agent_query_logging(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Disable the logging of search queries sent by human agents.

        It can prevent those queries from being stored at answer records.
        This feature is only supported for types: KNOWLEDGE_SEARCH.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#disable_agent_query_logging GoogleDialogflowConversationProfile#disable_agent_query_logging}
        '''
        result = self._values.get("disable_agent_query_logging")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def enable_conversation_augmented_query(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Enable including conversation context during query answer generation. This feature is only supported for types: KNOWLEDGE_SEARCH.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#enable_conversation_augmented_query GoogleDialogflowConversationProfile#enable_conversation_augmented_query}
        '''
        result = self._values.get("enable_conversation_augmented_query")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def enable_event_based_suggestion(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Automatically iterates all participants and tries to compile suggestions. This feature is only supported for types: ARTICLE_SUGGESTION, FAQ, DIALOGFLOW_ASSIST, KNOWLEDGE_ASSIST.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#enable_event_based_suggestion GoogleDialogflowConversationProfile#enable_event_based_suggestion}
        '''
        result = self._values.get("enable_event_based_suggestion")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def enable_query_suggestion_only(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Enable query suggestion only. This feature is only supported for types: KNOWLEDGE_ASSIST.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#enable_query_suggestion_only GoogleDialogflowConversationProfile#enable_query_suggestion_only}
        '''
        result = self._values.get("enable_query_suggestion_only")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def enable_query_suggestion_when_no_answer(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Enable query suggestion even if we can't find its answer.

        By default, queries are suggested only if we find its answer.
        This feature is only supported for types: KNOWLEDGE_ASSIST.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#enable_query_suggestion_when_no_answer GoogleDialogflowConversationProfile#enable_query_suggestion_when_no_answer}
        '''
        result = self._values.get("enable_query_suggestion_when_no_answer")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def query_config(
        self,
    ) -> typing.Optional["GoogleDialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsQueryConfig"]:
        '''query_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#query_config GoogleDialogflowConversationProfile#query_config}
        '''
        result = self._values.get("query_config")
        return typing.cast(typing.Optional["GoogleDialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsQueryConfig"], result)

    @builtins.property
    def suggestion_feature(
        self,
    ) -> typing.Optional["GoogleDialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsSuggestionFeature"]:
        '''suggestion_feature block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#suggestion_feature GoogleDialogflowConversationProfile#suggestion_feature}
        '''
        result = self._values.get("suggestion_feature")
        return typing.cast(typing.Optional["GoogleDialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsSuggestionFeature"], result)

    @builtins.property
    def suggestion_trigger_settings(
        self,
    ) -> typing.Optional["GoogleDialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsSuggestionTriggerSettings"]:
        '''suggestion_trigger_settings block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#suggestion_trigger_settings GoogleDialogflowConversationProfile#suggestion_trigger_settings}
        '''
        result = self._values.get("suggestion_trigger_settings")
        return typing.cast(typing.Optional["GoogleDialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsSuggestionTriggerSettings"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigs(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDialogflowConversationProfile.GoogleDialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsConversationModelConfig",
    jsii_struct_bases=[],
    name_mapping={"baseline_model_version": "baselineModelVersion", "model": "model"},
)
class GoogleDialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsConversationModelConfig:
    def __init__(
        self,
        *,
        baseline_model_version: typing.Optional[builtins.str] = None,
        model: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param baseline_model_version: Version of current baseline model. It will be ignored if model is set. Valid versions are: Article Suggestion baseline model: - 0.9 - 1.0 (default) Summarization baseline model: - 1.0 Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#baseline_model_version GoogleDialogflowConversationProfile#baseline_model_version}
        :param model: Conversation model resource name. Format: projects//conversationModels/. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#model GoogleDialogflowConversationProfile#model}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a70cd8cce14df41c2ae67797fa8c3bada18f6a61a49b9c72c50cc008e5eab020)
            check_type(argname="argument baseline_model_version", value=baseline_model_version, expected_type=type_hints["baseline_model_version"])
            check_type(argname="argument model", value=model, expected_type=type_hints["model"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if baseline_model_version is not None:
            self._values["baseline_model_version"] = baseline_model_version
        if model is not None:
            self._values["model"] = model

    @builtins.property
    def baseline_model_version(self) -> typing.Optional[builtins.str]:
        '''Version of current baseline model.

        It will be ignored if model is set. Valid versions are: Article Suggestion baseline model: - 0.9 - 1.0 (default) Summarization baseline model: - 1.0

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#baseline_model_version GoogleDialogflowConversationProfile#baseline_model_version}
        '''
        result = self._values.get("baseline_model_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def model(self) -> typing.Optional[builtins.str]:
        '''Conversation model resource name. Format: projects//conversationModels/.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#model GoogleDialogflowConversationProfile#model}
        '''
        result = self._values.get("model")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsConversationModelConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsConversationModelConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDialogflowConversationProfile.GoogleDialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsConversationModelConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bb1f188a63a7c4556e0c832d561bf70b31b6ec54ec2dc700d5de4ebc47aea67d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetBaselineModelVersion")
    def reset_baseline_model_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBaselineModelVersion", []))

    @jsii.member(jsii_name="resetModel")
    def reset_model(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetModel", []))

    @builtins.property
    @jsii.member(jsii_name="baselineModelVersionInput")
    def baseline_model_version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "baselineModelVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="modelInput")
    def model_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "modelInput"))

    @builtins.property
    @jsii.member(jsii_name="baselineModelVersion")
    def baseline_model_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "baselineModelVersion"))

    @baseline_model_version.setter
    def baseline_model_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f5aa5f5db153636ecdb6ae6710f2427062dd11c16400d900e85af13677a343bc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "baselineModelVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="model")
    def model(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "model"))

    @model.setter
    def model(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a518d4269e88d5e9d162938d2ba8a3cc2aaae5bc641fdd7592d8502d51e766fc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "model", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsConversationModelConfig]:
        return typing.cast(typing.Optional[GoogleDialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsConversationModelConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsConversationModelConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7fec2f80d3deefb2f438dd71d462cb39fd1a941578e7357553a3b0acf8d257e9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDialogflowConversationProfile.GoogleDialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsConversationProcessConfig",
    jsii_struct_bases=[],
    name_mapping={"recent_sentences_count": "recentSentencesCount"},
)
class GoogleDialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsConversationProcessConfig:
    def __init__(
        self,
        *,
        recent_sentences_count: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param recent_sentences_count: Number of recent non-small-talk sentences to use as context for article and FAQ suggestion. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#recent_sentences_count GoogleDialogflowConversationProfile#recent_sentences_count}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc2b5980aff72f1fccc5d348c6a1aec3215d3c0bc8b0420990c0136b99d5d9b8)
            check_type(argname="argument recent_sentences_count", value=recent_sentences_count, expected_type=type_hints["recent_sentences_count"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if recent_sentences_count is not None:
            self._values["recent_sentences_count"] = recent_sentences_count

    @builtins.property
    def recent_sentences_count(self) -> typing.Optional[jsii.Number]:
        '''Number of recent non-small-talk sentences to use as context for article and FAQ suggestion.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#recent_sentences_count GoogleDialogflowConversationProfile#recent_sentences_count}
        '''
        result = self._values.get("recent_sentences_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsConversationProcessConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsConversationProcessConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDialogflowConversationProfile.GoogleDialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsConversationProcessConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5978806849214e383ed99b1b2578e163e18a6fae53e75ee844ce3de748971699)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetRecentSentencesCount")
    def reset_recent_sentences_count(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRecentSentencesCount", []))

    @builtins.property
    @jsii.member(jsii_name="recentSentencesCountInput")
    def recent_sentences_count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "recentSentencesCountInput"))

    @builtins.property
    @jsii.member(jsii_name="recentSentencesCount")
    def recent_sentences_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "recentSentencesCount"))

    @recent_sentences_count.setter
    def recent_sentences_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d26bb6eefe3a16bff5f7c501800a3000302eee870355d0d5dbfee94827d0729a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "recentSentencesCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsConversationProcessConfig]:
        return typing.cast(typing.Optional[GoogleDialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsConversationProcessConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsConversationProcessConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__42d7a4ec1755f8642207977d625e554d5d08a3217127f934b54fa84f3e633cfd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleDialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDialogflowConversationProfile.GoogleDialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0b76dc7b506fab2dd16624351da5e90e8b077fbbac48eca431bffdceffdec139)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleDialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__70ca49a653eb3cd153080884a0869efcdffddb4a94dad8c19590401ce5ae9e9f)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleDialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a50299aaab94fcccd50253a658c477dee689a88201f9ee5fb0e617e90d08ddc)
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
            type_hints = typing.get_type_hints(_typecheckingstub__828f27d398832d254aa073e3989faba09ff1d3cca8127b3ebfb1a8c4f5e00243)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3f5056a8b495a42c6d38d828bc2c90e33b5b8f59c74542348281cc07b24e3fbb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigs]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigs]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigs]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__68e76c26159ac2786f98b73d3ef67e7472f77bf065ff259d125127bfa21e7ac7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleDialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDialogflowConversationProfile.GoogleDialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ff88b0a299435cd9d45969ec1647dfe6d81ffff7f442911c2048af0ea69751d7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putConversationModelConfig")
    def put_conversation_model_config(
        self,
        *,
        baseline_model_version: typing.Optional[builtins.str] = None,
        model: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param baseline_model_version: Version of current baseline model. It will be ignored if model is set. Valid versions are: Article Suggestion baseline model: - 0.9 - 1.0 (default) Summarization baseline model: - 1.0 Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#baseline_model_version GoogleDialogflowConversationProfile#baseline_model_version}
        :param model: Conversation model resource name. Format: projects//conversationModels/. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#model GoogleDialogflowConversationProfile#model}
        '''
        value = GoogleDialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsConversationModelConfig(
            baseline_model_version=baseline_model_version, model=model
        )

        return typing.cast(None, jsii.invoke(self, "putConversationModelConfig", [value]))

    @jsii.member(jsii_name="putConversationProcessConfig")
    def put_conversation_process_config(
        self,
        *,
        recent_sentences_count: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param recent_sentences_count: Number of recent non-small-talk sentences to use as context for article and FAQ suggestion. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#recent_sentences_count GoogleDialogflowConversationProfile#recent_sentences_count}
        '''
        value = GoogleDialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsConversationProcessConfig(
            recent_sentences_count=recent_sentences_count
        )

        return typing.cast(None, jsii.invoke(self, "putConversationProcessConfig", [value]))

    @jsii.member(jsii_name="putQueryConfig")
    def put_query_config(
        self,
        *,
        confidence_threshold: typing.Optional[jsii.Number] = None,
        context_filter_settings: typing.Optional[typing.Union["GoogleDialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsQueryConfigContextFilterSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        dialogflow_query_source: typing.Optional[typing.Union["GoogleDialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsQueryConfigDialogflowQuerySource", typing.Dict[builtins.str, typing.Any]]] = None,
        max_results: typing.Optional[jsii.Number] = None,
        sections: typing.Optional[typing.Union["GoogleDialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsQueryConfigSections", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param confidence_threshold: Confidence threshold of query result. This feature is only supported for types: ARTICLE_SUGGESTION, FAQ, SMART_REPLY, SMART_COMPOSE, KNOWLEDGE_SEARCH, KNOWLEDGE_ASSIST, ENTITY_EXTRACTION. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#confidence_threshold GoogleDialogflowConversationProfile#confidence_threshold}
        :param context_filter_settings: context_filter_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#context_filter_settings GoogleDialogflowConversationProfile#context_filter_settings}
        :param dialogflow_query_source: dialogflow_query_source block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#dialogflow_query_source GoogleDialogflowConversationProfile#dialogflow_query_source}
        :param max_results: Maximum number of results to return. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#max_results GoogleDialogflowConversationProfile#max_results}
        :param sections: sections block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#sections GoogleDialogflowConversationProfile#sections}
        '''
        value = GoogleDialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsQueryConfig(
            confidence_threshold=confidence_threshold,
            context_filter_settings=context_filter_settings,
            dialogflow_query_source=dialogflow_query_source,
            max_results=max_results,
            sections=sections,
        )

        return typing.cast(None, jsii.invoke(self, "putQueryConfig", [value]))

    @jsii.member(jsii_name="putSuggestionFeature")
    def put_suggestion_feature(
        self,
        *,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param type: Type of Human Agent Assistant API feature to request. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#type GoogleDialogflowConversationProfile#type}
        '''
        value = GoogleDialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsSuggestionFeature(
            type=type
        )

        return typing.cast(None, jsii.invoke(self, "putSuggestionFeature", [value]))

    @jsii.member(jsii_name="putSuggestionTriggerSettings")
    def put_suggestion_trigger_settings(
        self,
        *,
        no_small_talk: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        only_end_user: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param no_small_talk: Do not trigger if last utterance is small talk. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#no_small_talk GoogleDialogflowConversationProfile#no_small_talk}
        :param only_end_user: Only trigger suggestion if participant role of last utterance is END_USER. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#only_end_user GoogleDialogflowConversationProfile#only_end_user}
        '''
        value = GoogleDialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsSuggestionTriggerSettings(
            no_small_talk=no_small_talk, only_end_user=only_end_user
        )

        return typing.cast(None, jsii.invoke(self, "putSuggestionTriggerSettings", [value]))

    @jsii.member(jsii_name="resetConversationModelConfig")
    def reset_conversation_model_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConversationModelConfig", []))

    @jsii.member(jsii_name="resetConversationProcessConfig")
    def reset_conversation_process_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConversationProcessConfig", []))

    @jsii.member(jsii_name="resetDisableAgentQueryLogging")
    def reset_disable_agent_query_logging(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDisableAgentQueryLogging", []))

    @jsii.member(jsii_name="resetEnableConversationAugmentedQuery")
    def reset_enable_conversation_augmented_query(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnableConversationAugmentedQuery", []))

    @jsii.member(jsii_name="resetEnableEventBasedSuggestion")
    def reset_enable_event_based_suggestion(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnableEventBasedSuggestion", []))

    @jsii.member(jsii_name="resetEnableQuerySuggestionOnly")
    def reset_enable_query_suggestion_only(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnableQuerySuggestionOnly", []))

    @jsii.member(jsii_name="resetEnableQuerySuggestionWhenNoAnswer")
    def reset_enable_query_suggestion_when_no_answer(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnableQuerySuggestionWhenNoAnswer", []))

    @jsii.member(jsii_name="resetQueryConfig")
    def reset_query_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetQueryConfig", []))

    @jsii.member(jsii_name="resetSuggestionFeature")
    def reset_suggestion_feature(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSuggestionFeature", []))

    @jsii.member(jsii_name="resetSuggestionTriggerSettings")
    def reset_suggestion_trigger_settings(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSuggestionTriggerSettings", []))

    @builtins.property
    @jsii.member(jsii_name="conversationModelConfig")
    def conversation_model_config(
        self,
    ) -> GoogleDialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsConversationModelConfigOutputReference:
        return typing.cast(GoogleDialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsConversationModelConfigOutputReference, jsii.get(self, "conversationModelConfig"))

    @builtins.property
    @jsii.member(jsii_name="conversationProcessConfig")
    def conversation_process_config(
        self,
    ) -> GoogleDialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsConversationProcessConfigOutputReference:
        return typing.cast(GoogleDialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsConversationProcessConfigOutputReference, jsii.get(self, "conversationProcessConfig"))

    @builtins.property
    @jsii.member(jsii_name="queryConfig")
    def query_config(
        self,
    ) -> "GoogleDialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsQueryConfigOutputReference":
        return typing.cast("GoogleDialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsQueryConfigOutputReference", jsii.get(self, "queryConfig"))

    @builtins.property
    @jsii.member(jsii_name="suggestionFeature")
    def suggestion_feature(
        self,
    ) -> "GoogleDialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsSuggestionFeatureOutputReference":
        return typing.cast("GoogleDialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsSuggestionFeatureOutputReference", jsii.get(self, "suggestionFeature"))

    @builtins.property
    @jsii.member(jsii_name="suggestionTriggerSettings")
    def suggestion_trigger_settings(
        self,
    ) -> "GoogleDialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsSuggestionTriggerSettingsOutputReference":
        return typing.cast("GoogleDialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsSuggestionTriggerSettingsOutputReference", jsii.get(self, "suggestionTriggerSettings"))

    @builtins.property
    @jsii.member(jsii_name="conversationModelConfigInput")
    def conversation_model_config_input(
        self,
    ) -> typing.Optional[GoogleDialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsConversationModelConfig]:
        return typing.cast(typing.Optional[GoogleDialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsConversationModelConfig], jsii.get(self, "conversationModelConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="conversationProcessConfigInput")
    def conversation_process_config_input(
        self,
    ) -> typing.Optional[GoogleDialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsConversationProcessConfig]:
        return typing.cast(typing.Optional[GoogleDialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsConversationProcessConfig], jsii.get(self, "conversationProcessConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="disableAgentQueryLoggingInput")
    def disable_agent_query_logging_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "disableAgentQueryLoggingInput"))

    @builtins.property
    @jsii.member(jsii_name="enableConversationAugmentedQueryInput")
    def enable_conversation_augmented_query_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enableConversationAugmentedQueryInput"))

    @builtins.property
    @jsii.member(jsii_name="enableEventBasedSuggestionInput")
    def enable_event_based_suggestion_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enableEventBasedSuggestionInput"))

    @builtins.property
    @jsii.member(jsii_name="enableQuerySuggestionOnlyInput")
    def enable_query_suggestion_only_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enableQuerySuggestionOnlyInput"))

    @builtins.property
    @jsii.member(jsii_name="enableQuerySuggestionWhenNoAnswerInput")
    def enable_query_suggestion_when_no_answer_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enableQuerySuggestionWhenNoAnswerInput"))

    @builtins.property
    @jsii.member(jsii_name="queryConfigInput")
    def query_config_input(
        self,
    ) -> typing.Optional["GoogleDialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsQueryConfig"]:
        return typing.cast(typing.Optional["GoogleDialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsQueryConfig"], jsii.get(self, "queryConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="suggestionFeatureInput")
    def suggestion_feature_input(
        self,
    ) -> typing.Optional["GoogleDialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsSuggestionFeature"]:
        return typing.cast(typing.Optional["GoogleDialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsSuggestionFeature"], jsii.get(self, "suggestionFeatureInput"))

    @builtins.property
    @jsii.member(jsii_name="suggestionTriggerSettingsInput")
    def suggestion_trigger_settings_input(
        self,
    ) -> typing.Optional["GoogleDialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsSuggestionTriggerSettings"]:
        return typing.cast(typing.Optional["GoogleDialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsSuggestionTriggerSettings"], jsii.get(self, "suggestionTriggerSettingsInput"))

    @builtins.property
    @jsii.member(jsii_name="disableAgentQueryLogging")
    def disable_agent_query_logging(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "disableAgentQueryLogging"))

    @disable_agent_query_logging.setter
    def disable_agent_query_logging(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ec7e627eba3d1052094535335c48a1630e92ffabd6ae22b2e41eaed0e5099fb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "disableAgentQueryLogging", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enableConversationAugmentedQuery")
    def enable_conversation_augmented_query(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enableConversationAugmentedQuery"))

    @enable_conversation_augmented_query.setter
    def enable_conversation_augmented_query(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b37cdb55d51ed589500269ce5dfb684739f05b766df34abd765ac1e1588998e8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableConversationAugmentedQuery", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enableEventBasedSuggestion")
    def enable_event_based_suggestion(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enableEventBasedSuggestion"))

    @enable_event_based_suggestion.setter
    def enable_event_based_suggestion(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__755bdc5df6669e539e4c5a47b0eef9296d501ad069f5c7d1530293199174620c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableEventBasedSuggestion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enableQuerySuggestionOnly")
    def enable_query_suggestion_only(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enableQuerySuggestionOnly"))

    @enable_query_suggestion_only.setter
    def enable_query_suggestion_only(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__de51c0f1a1f0b69d4016520405d3852fd6cc466c01f025a68a5f85dad2467793)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableQuerySuggestionOnly", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enableQuerySuggestionWhenNoAnswer")
    def enable_query_suggestion_when_no_answer(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enableQuerySuggestionWhenNoAnswer"))

    @enable_query_suggestion_when_no_answer.setter
    def enable_query_suggestion_when_no_answer(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9bfd9f8102a6c865bd5a2ff5c9b8baee54249cb9502472e3b83cf9bf78f0d26c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableQuerySuggestionWhenNoAnswer", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigs]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigs]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigs]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc69088fdde5b2f04ce6235803537b01117e12b6eba5fd49770b6af04910c437)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDialogflowConversationProfile.GoogleDialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsQueryConfig",
    jsii_struct_bases=[],
    name_mapping={
        "confidence_threshold": "confidenceThreshold",
        "context_filter_settings": "contextFilterSettings",
        "dialogflow_query_source": "dialogflowQuerySource",
        "max_results": "maxResults",
        "sections": "sections",
    },
)
class GoogleDialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsQueryConfig:
    def __init__(
        self,
        *,
        confidence_threshold: typing.Optional[jsii.Number] = None,
        context_filter_settings: typing.Optional[typing.Union["GoogleDialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsQueryConfigContextFilterSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        dialogflow_query_source: typing.Optional[typing.Union["GoogleDialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsQueryConfigDialogflowQuerySource", typing.Dict[builtins.str, typing.Any]]] = None,
        max_results: typing.Optional[jsii.Number] = None,
        sections: typing.Optional[typing.Union["GoogleDialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsQueryConfigSections", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param confidence_threshold: Confidence threshold of query result. This feature is only supported for types: ARTICLE_SUGGESTION, FAQ, SMART_REPLY, SMART_COMPOSE, KNOWLEDGE_SEARCH, KNOWLEDGE_ASSIST, ENTITY_EXTRACTION. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#confidence_threshold GoogleDialogflowConversationProfile#confidence_threshold}
        :param context_filter_settings: context_filter_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#context_filter_settings GoogleDialogflowConversationProfile#context_filter_settings}
        :param dialogflow_query_source: dialogflow_query_source block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#dialogflow_query_source GoogleDialogflowConversationProfile#dialogflow_query_source}
        :param max_results: Maximum number of results to return. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#max_results GoogleDialogflowConversationProfile#max_results}
        :param sections: sections block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#sections GoogleDialogflowConversationProfile#sections}
        '''
        if isinstance(context_filter_settings, dict):
            context_filter_settings = GoogleDialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsQueryConfigContextFilterSettings(**context_filter_settings)
        if isinstance(dialogflow_query_source, dict):
            dialogflow_query_source = GoogleDialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsQueryConfigDialogflowQuerySource(**dialogflow_query_source)
        if isinstance(sections, dict):
            sections = GoogleDialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsQueryConfigSections(**sections)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fe53b16ce30ebc3ab27946159713ac396d8291a09f4d2c069fdfce4434819bc7)
            check_type(argname="argument confidence_threshold", value=confidence_threshold, expected_type=type_hints["confidence_threshold"])
            check_type(argname="argument context_filter_settings", value=context_filter_settings, expected_type=type_hints["context_filter_settings"])
            check_type(argname="argument dialogflow_query_source", value=dialogflow_query_source, expected_type=type_hints["dialogflow_query_source"])
            check_type(argname="argument max_results", value=max_results, expected_type=type_hints["max_results"])
            check_type(argname="argument sections", value=sections, expected_type=type_hints["sections"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if confidence_threshold is not None:
            self._values["confidence_threshold"] = confidence_threshold
        if context_filter_settings is not None:
            self._values["context_filter_settings"] = context_filter_settings
        if dialogflow_query_source is not None:
            self._values["dialogflow_query_source"] = dialogflow_query_source
        if max_results is not None:
            self._values["max_results"] = max_results
        if sections is not None:
            self._values["sections"] = sections

    @builtins.property
    def confidence_threshold(self) -> typing.Optional[jsii.Number]:
        '''Confidence threshold of query result. This feature is only supported for types: ARTICLE_SUGGESTION, FAQ, SMART_REPLY, SMART_COMPOSE, KNOWLEDGE_SEARCH, KNOWLEDGE_ASSIST, ENTITY_EXTRACTION.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#confidence_threshold GoogleDialogflowConversationProfile#confidence_threshold}
        '''
        result = self._values.get("confidence_threshold")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def context_filter_settings(
        self,
    ) -> typing.Optional["GoogleDialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsQueryConfigContextFilterSettings"]:
        '''context_filter_settings block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#context_filter_settings GoogleDialogflowConversationProfile#context_filter_settings}
        '''
        result = self._values.get("context_filter_settings")
        return typing.cast(typing.Optional["GoogleDialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsQueryConfigContextFilterSettings"], result)

    @builtins.property
    def dialogflow_query_source(
        self,
    ) -> typing.Optional["GoogleDialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsQueryConfigDialogflowQuerySource"]:
        '''dialogflow_query_source block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#dialogflow_query_source GoogleDialogflowConversationProfile#dialogflow_query_source}
        '''
        result = self._values.get("dialogflow_query_source")
        return typing.cast(typing.Optional["GoogleDialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsQueryConfigDialogflowQuerySource"], result)

    @builtins.property
    def max_results(self) -> typing.Optional[jsii.Number]:
        '''Maximum number of results to return.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#max_results GoogleDialogflowConversationProfile#max_results}
        '''
        result = self._values.get("max_results")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def sections(
        self,
    ) -> typing.Optional["GoogleDialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsQueryConfigSections"]:
        '''sections block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#sections GoogleDialogflowConversationProfile#sections}
        '''
        result = self._values.get("sections")
        return typing.cast(typing.Optional["GoogleDialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsQueryConfigSections"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsQueryConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDialogflowConversationProfile.GoogleDialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsQueryConfigContextFilterSettings",
    jsii_struct_bases=[],
    name_mapping={
        "drop_handoff_messages": "dropHandoffMessages",
        "drop_ivr_messages": "dropIvrMessages",
        "drop_virtual_agent_messages": "dropVirtualAgentMessages",
    },
)
class GoogleDialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsQueryConfigContextFilterSettings:
    def __init__(
        self,
        *,
        drop_handoff_messages: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        drop_ivr_messages: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        drop_virtual_agent_messages: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param drop_handoff_messages: If set to true, the last message from virtual agent (hand off message) and the message before it (trigger message of hand off) are dropped. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#drop_handoff_messages GoogleDialogflowConversationProfile#drop_handoff_messages}
        :param drop_ivr_messages: If set to true, all messages from ivr stage are dropped. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#drop_ivr_messages GoogleDialogflowConversationProfile#drop_ivr_messages}
        :param drop_virtual_agent_messages: If set to true, all messages from virtual agent are dropped. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#drop_virtual_agent_messages GoogleDialogflowConversationProfile#drop_virtual_agent_messages}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__797948b84737b42b251f7431dd152ef2468a93331154eb76d99b7fe34ffe5c36)
            check_type(argname="argument drop_handoff_messages", value=drop_handoff_messages, expected_type=type_hints["drop_handoff_messages"])
            check_type(argname="argument drop_ivr_messages", value=drop_ivr_messages, expected_type=type_hints["drop_ivr_messages"])
            check_type(argname="argument drop_virtual_agent_messages", value=drop_virtual_agent_messages, expected_type=type_hints["drop_virtual_agent_messages"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if drop_handoff_messages is not None:
            self._values["drop_handoff_messages"] = drop_handoff_messages
        if drop_ivr_messages is not None:
            self._values["drop_ivr_messages"] = drop_ivr_messages
        if drop_virtual_agent_messages is not None:
            self._values["drop_virtual_agent_messages"] = drop_virtual_agent_messages

    @builtins.property
    def drop_handoff_messages(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If set to true, the last message from virtual agent (hand off message) and the message before it (trigger message of hand off) are dropped.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#drop_handoff_messages GoogleDialogflowConversationProfile#drop_handoff_messages}
        '''
        result = self._values.get("drop_handoff_messages")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def drop_ivr_messages(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If set to true, all messages from ivr stage are dropped.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#drop_ivr_messages GoogleDialogflowConversationProfile#drop_ivr_messages}
        '''
        result = self._values.get("drop_ivr_messages")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def drop_virtual_agent_messages(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If set to true, all messages from virtual agent are dropped.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#drop_virtual_agent_messages GoogleDialogflowConversationProfile#drop_virtual_agent_messages}
        '''
        result = self._values.get("drop_virtual_agent_messages")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsQueryConfigContextFilterSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsQueryConfigContextFilterSettingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDialogflowConversationProfile.GoogleDialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsQueryConfigContextFilterSettingsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ab57542f46c2398b7bea812e9a1a7417ad2c144d677f20bcf939aca417c25386)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetDropHandoffMessages")
    def reset_drop_handoff_messages(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDropHandoffMessages", []))

    @jsii.member(jsii_name="resetDropIvrMessages")
    def reset_drop_ivr_messages(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDropIvrMessages", []))

    @jsii.member(jsii_name="resetDropVirtualAgentMessages")
    def reset_drop_virtual_agent_messages(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDropVirtualAgentMessages", []))

    @builtins.property
    @jsii.member(jsii_name="dropHandoffMessagesInput")
    def drop_handoff_messages_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "dropHandoffMessagesInput"))

    @builtins.property
    @jsii.member(jsii_name="dropIvrMessagesInput")
    def drop_ivr_messages_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "dropIvrMessagesInput"))

    @builtins.property
    @jsii.member(jsii_name="dropVirtualAgentMessagesInput")
    def drop_virtual_agent_messages_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "dropVirtualAgentMessagesInput"))

    @builtins.property
    @jsii.member(jsii_name="dropHandoffMessages")
    def drop_handoff_messages(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "dropHandoffMessages"))

    @drop_handoff_messages.setter
    def drop_handoff_messages(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bb426f39e91a5c49285093fc73efe8947c5f907ea13463df549fa14134af9390)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dropHandoffMessages", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dropIvrMessages")
    def drop_ivr_messages(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "dropIvrMessages"))

    @drop_ivr_messages.setter
    def drop_ivr_messages(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__211330c9a11aec966a441c0fd4786ce97011485e5b7dc1ee53d15353797c1a84)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dropIvrMessages", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dropVirtualAgentMessages")
    def drop_virtual_agent_messages(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "dropVirtualAgentMessages"))

    @drop_virtual_agent_messages.setter
    def drop_virtual_agent_messages(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__50215eb91f6285fe2c7b1e8fd56e899d3564b6222f73e8383409bc2d12b3f973)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dropVirtualAgentMessages", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsQueryConfigContextFilterSettings]:
        return typing.cast(typing.Optional[GoogleDialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsQueryConfigContextFilterSettings], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsQueryConfigContextFilterSettings],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__337597f3dbfee6fe3144f7997f091448c4792cbdaf934c0cf96436ae9eda2e1e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDialogflowConversationProfile.GoogleDialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsQueryConfigDialogflowQuerySource",
    jsii_struct_bases=[],
    name_mapping={"agent": "agent", "human_agent_side_config": "humanAgentSideConfig"},
)
class GoogleDialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsQueryConfigDialogflowQuerySource:
    def __init__(
        self,
        *,
        agent: builtins.str,
        human_agent_side_config: typing.Optional[typing.Union["GoogleDialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsQueryConfigDialogflowQuerySourceHumanAgentSideConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param agent: he name of a Dialogflow virtual agent used for end user side intent detection and suggestion. Format: projects//locations//agent. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#agent GoogleDialogflowConversationProfile#agent}
        :param human_agent_side_config: human_agent_side_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#human_agent_side_config GoogleDialogflowConversationProfile#human_agent_side_config}
        '''
        if isinstance(human_agent_side_config, dict):
            human_agent_side_config = GoogleDialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsQueryConfigDialogflowQuerySourceHumanAgentSideConfig(**human_agent_side_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f66807c71a3b86e7ed5ceb24bae791ce6c6fe44d30ee7cf6881e929e67198774)
            check_type(argname="argument agent", value=agent, expected_type=type_hints["agent"])
            check_type(argname="argument human_agent_side_config", value=human_agent_side_config, expected_type=type_hints["human_agent_side_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "agent": agent,
        }
        if human_agent_side_config is not None:
            self._values["human_agent_side_config"] = human_agent_side_config

    @builtins.property
    def agent(self) -> builtins.str:
        '''he name of a Dialogflow virtual agent used for end user side intent detection and suggestion.

        Format: projects//locations//agent.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#agent GoogleDialogflowConversationProfile#agent}
        '''
        result = self._values.get("agent")
        assert result is not None, "Required property 'agent' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def human_agent_side_config(
        self,
    ) -> typing.Optional["GoogleDialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsQueryConfigDialogflowQuerySourceHumanAgentSideConfig"]:
        '''human_agent_side_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#human_agent_side_config GoogleDialogflowConversationProfile#human_agent_side_config}
        '''
        result = self._values.get("human_agent_side_config")
        return typing.cast(typing.Optional["GoogleDialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsQueryConfigDialogflowQuerySourceHumanAgentSideConfig"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsQueryConfigDialogflowQuerySource(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDialogflowConversationProfile.GoogleDialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsQueryConfigDialogflowQuerySourceHumanAgentSideConfig",
    jsii_struct_bases=[],
    name_mapping={"agent": "agent"},
)
class GoogleDialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsQueryConfigDialogflowQuerySourceHumanAgentSideConfig:
    def __init__(self, *, agent: typing.Optional[builtins.str] = None) -> None:
        '''
        :param agent: The name of a dialogflow virtual agent used for intent detection and suggestion triggered by human agent. Format: projects//locations//agent. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#agent GoogleDialogflowConversationProfile#agent}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__be3d78b18360b64326c0f72d7137a4b9848d471f33b5bd9fe75311f41cc0a798)
            check_type(argname="argument agent", value=agent, expected_type=type_hints["agent"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if agent is not None:
            self._values["agent"] = agent

    @builtins.property
    def agent(self) -> typing.Optional[builtins.str]:
        '''The name of a dialogflow virtual agent used for intent detection and suggestion triggered by human agent.

        Format: projects//locations//agent.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#agent GoogleDialogflowConversationProfile#agent}
        '''
        result = self._values.get("agent")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsQueryConfigDialogflowQuerySourceHumanAgentSideConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsQueryConfigDialogflowQuerySourceHumanAgentSideConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDialogflowConversationProfile.GoogleDialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsQueryConfigDialogflowQuerySourceHumanAgentSideConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b8a9e5969320ba5e69a858d6b2809cffefabcc0a1a89fc604f46ef1d5c61e005)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAgent")
    def reset_agent(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAgent", []))

    @builtins.property
    @jsii.member(jsii_name="agentInput")
    def agent_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "agentInput"))

    @builtins.property
    @jsii.member(jsii_name="agent")
    def agent(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "agent"))

    @agent.setter
    def agent(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d3a4a85b17f1034462ce0cdc2161ffb6e58e5134ac60c8a933b1ad4de6bad85)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "agent", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsQueryConfigDialogflowQuerySourceHumanAgentSideConfig]:
        return typing.cast(typing.Optional[GoogleDialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsQueryConfigDialogflowQuerySourceHumanAgentSideConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsQueryConfigDialogflowQuerySourceHumanAgentSideConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1858c7a070064383b871cd3681a847547c112652a1f2bd0e1a36dafe21844c3f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleDialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsQueryConfigDialogflowQuerySourceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDialogflowConversationProfile.GoogleDialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsQueryConfigDialogflowQuerySourceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__dca5c1819853ce3f62ab01c07c38803232e36f9f71666c244920d730cb318051)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putHumanAgentSideConfig")
    def put_human_agent_side_config(
        self,
        *,
        agent: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param agent: The name of a dialogflow virtual agent used for intent detection and suggestion triggered by human agent. Format: projects//locations//agent. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#agent GoogleDialogflowConversationProfile#agent}
        '''
        value = GoogleDialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsQueryConfigDialogflowQuerySourceHumanAgentSideConfig(
            agent=agent
        )

        return typing.cast(None, jsii.invoke(self, "putHumanAgentSideConfig", [value]))

    @jsii.member(jsii_name="resetHumanAgentSideConfig")
    def reset_human_agent_side_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHumanAgentSideConfig", []))

    @builtins.property
    @jsii.member(jsii_name="humanAgentSideConfig")
    def human_agent_side_config(
        self,
    ) -> GoogleDialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsQueryConfigDialogflowQuerySourceHumanAgentSideConfigOutputReference:
        return typing.cast(GoogleDialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsQueryConfigDialogflowQuerySourceHumanAgentSideConfigOutputReference, jsii.get(self, "humanAgentSideConfig"))

    @builtins.property
    @jsii.member(jsii_name="agentInput")
    def agent_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "agentInput"))

    @builtins.property
    @jsii.member(jsii_name="humanAgentSideConfigInput")
    def human_agent_side_config_input(
        self,
    ) -> typing.Optional[GoogleDialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsQueryConfigDialogflowQuerySourceHumanAgentSideConfig]:
        return typing.cast(typing.Optional[GoogleDialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsQueryConfigDialogflowQuerySourceHumanAgentSideConfig], jsii.get(self, "humanAgentSideConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="agent")
    def agent(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "agent"))

    @agent.setter
    def agent(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bc4402da4c3be8a16b41a222e562dc2ffcc6510d9126790a335687f5f1c0d3db)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "agent", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsQueryConfigDialogflowQuerySource]:
        return typing.cast(typing.Optional[GoogleDialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsQueryConfigDialogflowQuerySource], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsQueryConfigDialogflowQuerySource],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1429c5e236e9b8cae6ef50008e1b06206a0043cdf5c926b33f52cdbf5232b106)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleDialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsQueryConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDialogflowConversationProfile.GoogleDialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsQueryConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ba843e1258e2f3bfc040c5618dbb77f6e7be87b0c1ae288d3dafddc1b737d039)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putContextFilterSettings")
    def put_context_filter_settings(
        self,
        *,
        drop_handoff_messages: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        drop_ivr_messages: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        drop_virtual_agent_messages: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param drop_handoff_messages: If set to true, the last message from virtual agent (hand off message) and the message before it (trigger message of hand off) are dropped. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#drop_handoff_messages GoogleDialogflowConversationProfile#drop_handoff_messages}
        :param drop_ivr_messages: If set to true, all messages from ivr stage are dropped. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#drop_ivr_messages GoogleDialogflowConversationProfile#drop_ivr_messages}
        :param drop_virtual_agent_messages: If set to true, all messages from virtual agent are dropped. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#drop_virtual_agent_messages GoogleDialogflowConversationProfile#drop_virtual_agent_messages}
        '''
        value = GoogleDialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsQueryConfigContextFilterSettings(
            drop_handoff_messages=drop_handoff_messages,
            drop_ivr_messages=drop_ivr_messages,
            drop_virtual_agent_messages=drop_virtual_agent_messages,
        )

        return typing.cast(None, jsii.invoke(self, "putContextFilterSettings", [value]))

    @jsii.member(jsii_name="putDialogflowQuerySource")
    def put_dialogflow_query_source(
        self,
        *,
        agent: builtins.str,
        human_agent_side_config: typing.Optional[typing.Union[GoogleDialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsQueryConfigDialogflowQuerySourceHumanAgentSideConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param agent: he name of a Dialogflow virtual agent used for end user side intent detection and suggestion. Format: projects//locations//agent. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#agent GoogleDialogflowConversationProfile#agent}
        :param human_agent_side_config: human_agent_side_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#human_agent_side_config GoogleDialogflowConversationProfile#human_agent_side_config}
        '''
        value = GoogleDialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsQueryConfigDialogflowQuerySource(
            agent=agent, human_agent_side_config=human_agent_side_config
        )

        return typing.cast(None, jsii.invoke(self, "putDialogflowQuerySource", [value]))

    @jsii.member(jsii_name="putSections")
    def put_sections(
        self,
        *,
        section_types: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param section_types: The selected sections chosen to return when requesting a summary of a conversation If not provided the default selection will be "{SITUATION, ACTION, RESULT}". Possible values: ["SECTION_TYPE_UNSPECIFIED", "SITUATION", "ACTION", "RESOLUTION", "REASON_FOR_CANCELLATION", "CUSTOMER_SATISFACTION", "ENTITIES"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#section_types GoogleDialogflowConversationProfile#section_types}
        '''
        value = GoogleDialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsQueryConfigSections(
            section_types=section_types
        )

        return typing.cast(None, jsii.invoke(self, "putSections", [value]))

    @jsii.member(jsii_name="resetConfidenceThreshold")
    def reset_confidence_threshold(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConfidenceThreshold", []))

    @jsii.member(jsii_name="resetContextFilterSettings")
    def reset_context_filter_settings(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetContextFilterSettings", []))

    @jsii.member(jsii_name="resetDialogflowQuerySource")
    def reset_dialogflow_query_source(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDialogflowQuerySource", []))

    @jsii.member(jsii_name="resetMaxResults")
    def reset_max_results(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxResults", []))

    @jsii.member(jsii_name="resetSections")
    def reset_sections(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSections", []))

    @builtins.property
    @jsii.member(jsii_name="contextFilterSettings")
    def context_filter_settings(
        self,
    ) -> GoogleDialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsQueryConfigContextFilterSettingsOutputReference:
        return typing.cast(GoogleDialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsQueryConfigContextFilterSettingsOutputReference, jsii.get(self, "contextFilterSettings"))

    @builtins.property
    @jsii.member(jsii_name="dialogflowQuerySource")
    def dialogflow_query_source(
        self,
    ) -> GoogleDialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsQueryConfigDialogflowQuerySourceOutputReference:
        return typing.cast(GoogleDialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsQueryConfigDialogflowQuerySourceOutputReference, jsii.get(self, "dialogflowQuerySource"))

    @builtins.property
    @jsii.member(jsii_name="sections")
    def sections(
        self,
    ) -> "GoogleDialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsQueryConfigSectionsOutputReference":
        return typing.cast("GoogleDialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsQueryConfigSectionsOutputReference", jsii.get(self, "sections"))

    @builtins.property
    @jsii.member(jsii_name="confidenceThresholdInput")
    def confidence_threshold_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "confidenceThresholdInput"))

    @builtins.property
    @jsii.member(jsii_name="contextFilterSettingsInput")
    def context_filter_settings_input(
        self,
    ) -> typing.Optional[GoogleDialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsQueryConfigContextFilterSettings]:
        return typing.cast(typing.Optional[GoogleDialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsQueryConfigContextFilterSettings], jsii.get(self, "contextFilterSettingsInput"))

    @builtins.property
    @jsii.member(jsii_name="dialogflowQuerySourceInput")
    def dialogflow_query_source_input(
        self,
    ) -> typing.Optional[GoogleDialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsQueryConfigDialogflowQuerySource]:
        return typing.cast(typing.Optional[GoogleDialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsQueryConfigDialogflowQuerySource], jsii.get(self, "dialogflowQuerySourceInput"))

    @builtins.property
    @jsii.member(jsii_name="maxResultsInput")
    def max_results_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxResultsInput"))

    @builtins.property
    @jsii.member(jsii_name="sectionsInput")
    def sections_input(
        self,
    ) -> typing.Optional["GoogleDialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsQueryConfigSections"]:
        return typing.cast(typing.Optional["GoogleDialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsQueryConfigSections"], jsii.get(self, "sectionsInput"))

    @builtins.property
    @jsii.member(jsii_name="confidenceThreshold")
    def confidence_threshold(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "confidenceThreshold"))

    @confidence_threshold.setter
    def confidence_threshold(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f03438e43c554acb38440bd8794fbaaadc760e8a11d3facad9468eec4811e34)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "confidenceThreshold", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxResults")
    def max_results(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxResults"))

    @max_results.setter
    def max_results(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aef125518cb38c8c14d56b7966b56e517492e97ba06897a059db71abcbcfcb38)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxResults", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsQueryConfig]:
        return typing.cast(typing.Optional[GoogleDialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsQueryConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsQueryConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__749d696c1f8073fca97a1ce2a73e3d4671a0730de54fedd43509a496e8e6c009)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDialogflowConversationProfile.GoogleDialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsQueryConfigSections",
    jsii_struct_bases=[],
    name_mapping={"section_types": "sectionTypes"},
)
class GoogleDialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsQueryConfigSections:
    def __init__(
        self,
        *,
        section_types: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param section_types: The selected sections chosen to return when requesting a summary of a conversation If not provided the default selection will be "{SITUATION, ACTION, RESULT}". Possible values: ["SECTION_TYPE_UNSPECIFIED", "SITUATION", "ACTION", "RESOLUTION", "REASON_FOR_CANCELLATION", "CUSTOMER_SATISFACTION", "ENTITIES"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#section_types GoogleDialogflowConversationProfile#section_types}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f61fce52b68bddf4ee43fc15002df216d11049f56fb3c13c2ee5c365a9c086b)
            check_type(argname="argument section_types", value=section_types, expected_type=type_hints["section_types"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if section_types is not None:
            self._values["section_types"] = section_types

    @builtins.property
    def section_types(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The selected sections chosen to return when requesting a summary of a conversation If not provided the default selection will be "{SITUATION, ACTION, RESULT}".

        Possible values: ["SECTION_TYPE_UNSPECIFIED", "SITUATION", "ACTION", "RESOLUTION", "REASON_FOR_CANCELLATION", "CUSTOMER_SATISFACTION", "ENTITIES"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#section_types GoogleDialogflowConversationProfile#section_types}
        '''
        result = self._values.get("section_types")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsQueryConfigSections(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsQueryConfigSectionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDialogflowConversationProfile.GoogleDialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsQueryConfigSectionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1bd91e129887f90d1b9215cf1fc88e312957949997012ab27a2d764e78485146)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetSectionTypes")
    def reset_section_types(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSectionTypes", []))

    @builtins.property
    @jsii.member(jsii_name="sectionTypesInput")
    def section_types_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "sectionTypesInput"))

    @builtins.property
    @jsii.member(jsii_name="sectionTypes")
    def section_types(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "sectionTypes"))

    @section_types.setter
    def section_types(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__21450ed341999b8594fecac04f08c70c6473d4299ccabdc09f5123af48b0aaad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sectionTypes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsQueryConfigSections]:
        return typing.cast(typing.Optional[GoogleDialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsQueryConfigSections], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsQueryConfigSections],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cec7b2e9c7dcf17dbd65aea4f86f0fb5eb3fd43b106e6994197a48794b1eb4ae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDialogflowConversationProfile.GoogleDialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsSuggestionFeature",
    jsii_struct_bases=[],
    name_mapping={"type": "type"},
)
class GoogleDialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsSuggestionFeature:
    def __init__(self, *, type: typing.Optional[builtins.str] = None) -> None:
        '''
        :param type: Type of Human Agent Assistant API feature to request. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#type GoogleDialogflowConversationProfile#type}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f23e6efdbfbecd662958c722624645cd17e70dc4092a1f4f4addac4964f9dd59)
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if type is not None:
            self._values["type"] = type

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''Type of Human Agent Assistant API feature to request.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#type GoogleDialogflowConversationProfile#type}
        '''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsSuggestionFeature(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsSuggestionFeatureOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDialogflowConversationProfile.GoogleDialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsSuggestionFeatureOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a5e82b25ae7f7f2947d877a82a05e670ea6787880d28a8786552e91dcd567138)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetType")
    def reset_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetType", []))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e5e7924154ba28f5458d9539ac3513537c6620cbdf9b7907545cd8651b7097a8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsSuggestionFeature]:
        return typing.cast(typing.Optional[GoogleDialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsSuggestionFeature], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsSuggestionFeature],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e97fc7bcd83c449a1b48f8839e6cf39eb6caeaca415706ce6f1b9764cc588353)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDialogflowConversationProfile.GoogleDialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsSuggestionTriggerSettings",
    jsii_struct_bases=[],
    name_mapping={"no_small_talk": "noSmallTalk", "only_end_user": "onlyEndUser"},
)
class GoogleDialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsSuggestionTriggerSettings:
    def __init__(
        self,
        *,
        no_small_talk: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        only_end_user: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param no_small_talk: Do not trigger if last utterance is small talk. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#no_small_talk GoogleDialogflowConversationProfile#no_small_talk}
        :param only_end_user: Only trigger suggestion if participant role of last utterance is END_USER. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#only_end_user GoogleDialogflowConversationProfile#only_end_user}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__acb225b0ecde5c8c65d23cac4a5555f5e9353d83db9ead66a477bf4b7a00f30d)
            check_type(argname="argument no_small_talk", value=no_small_talk, expected_type=type_hints["no_small_talk"])
            check_type(argname="argument only_end_user", value=only_end_user, expected_type=type_hints["only_end_user"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if no_small_talk is not None:
            self._values["no_small_talk"] = no_small_talk
        if only_end_user is not None:
            self._values["only_end_user"] = only_end_user

    @builtins.property
    def no_small_talk(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Do not trigger if last utterance is small talk.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#no_small_talk GoogleDialogflowConversationProfile#no_small_talk}
        '''
        result = self._values.get("no_small_talk")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def only_end_user(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Only trigger suggestion if participant role of last utterance is END_USER.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#only_end_user GoogleDialogflowConversationProfile#only_end_user}
        '''
        result = self._values.get("only_end_user")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsSuggestionTriggerSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsSuggestionTriggerSettingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDialogflowConversationProfile.GoogleDialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsSuggestionTriggerSettingsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f570ddde9981974e77936bd5deff84aff50b07506989c7969739952fd2f10ede)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetNoSmallTalk")
    def reset_no_small_talk(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNoSmallTalk", []))

    @jsii.member(jsii_name="resetOnlyEndUser")
    def reset_only_end_user(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOnlyEndUser", []))

    @builtins.property
    @jsii.member(jsii_name="noSmallTalkInput")
    def no_small_talk_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "noSmallTalkInput"))

    @builtins.property
    @jsii.member(jsii_name="onlyEndUserInput")
    def only_end_user_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "onlyEndUserInput"))

    @builtins.property
    @jsii.member(jsii_name="noSmallTalk")
    def no_small_talk(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "noSmallTalk"))

    @no_small_talk.setter
    def no_small_talk(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7ff8bbf4a26e7c13371d21bc149750648366939a79841b8258500b6d06eafcf4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "noSmallTalk", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="onlyEndUser")
    def only_end_user(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "onlyEndUser"))

    @only_end_user.setter
    def only_end_user(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b59509c0f4230630d5e3064f6797874aa8a92c1c8eb21eb556ed241164bcfbf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "onlyEndUser", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsSuggestionTriggerSettings]:
        return typing.cast(typing.Optional[GoogleDialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsSuggestionTriggerSettings], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsSuggestionTriggerSettings],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cef008eb8ccd11cb9942a64b316590285094ef18cdb8cc111dd2d7d3264352ef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleDialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDialogflowConversationProfile.GoogleDialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b049715ea10bf69d77c85fa668cbe15850c86f6d1b44787f6522cc875aab200d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putFeatureConfigs")
    def put_feature_configs(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleDialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigs, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e61d4e58b31f58ec721ed705ebf2d18e70d2647e7b532fb36f4e0ad5a24b3c94)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putFeatureConfigs", [value]))

    @jsii.member(jsii_name="resetDisableHighLatencyFeaturesSyncDelivery")
    def reset_disable_high_latency_features_sync_delivery(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDisableHighLatencyFeaturesSyncDelivery", []))

    @jsii.member(jsii_name="resetFeatureConfigs")
    def reset_feature_configs(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFeatureConfigs", []))

    @jsii.member(jsii_name="resetGenerators")
    def reset_generators(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGenerators", []))

    @jsii.member(jsii_name="resetGroupSuggestionResponses")
    def reset_group_suggestion_responses(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGroupSuggestionResponses", []))

    @builtins.property
    @jsii.member(jsii_name="featureConfigs")
    def feature_configs(
        self,
    ) -> GoogleDialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsList:
        return typing.cast(GoogleDialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsList, jsii.get(self, "featureConfigs"))

    @builtins.property
    @jsii.member(jsii_name="disableHighLatencyFeaturesSyncDeliveryInput")
    def disable_high_latency_features_sync_delivery_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "disableHighLatencyFeaturesSyncDeliveryInput"))

    @builtins.property
    @jsii.member(jsii_name="featureConfigsInput")
    def feature_configs_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigs]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigs]]], jsii.get(self, "featureConfigsInput"))

    @builtins.property
    @jsii.member(jsii_name="generatorsInput")
    def generators_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "generatorsInput"))

    @builtins.property
    @jsii.member(jsii_name="groupSuggestionResponsesInput")
    def group_suggestion_responses_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "groupSuggestionResponsesInput"))

    @builtins.property
    @jsii.member(jsii_name="disableHighLatencyFeaturesSyncDelivery")
    def disable_high_latency_features_sync_delivery(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "disableHighLatencyFeaturesSyncDelivery"))

    @disable_high_latency_features_sync_delivery.setter
    def disable_high_latency_features_sync_delivery(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0b644c2935eac32ac5058ec8e71adf3dce199cb923acb9cf7b69f935ad3a8561)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "disableHighLatencyFeaturesSyncDelivery", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="generators")
    def generators(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "generators"))

    @generators.setter
    def generators(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__45144aa37fe43c8adbb09ce668902b86ce661de11d6d42a8687bf8cb27a7582d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "generators", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="groupSuggestionResponses")
    def group_suggestion_responses(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "groupSuggestionResponses"))

    @group_suggestion_responses.setter
    def group_suggestion_responses(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__01c659c03f6651f62cb14f8c825d09d20376332e8a3200e76e9cd049bb29dab2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "groupSuggestionResponses", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfig]:
        return typing.cast(typing.Optional[GoogleDialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ff8c26fab87265bfef5e659367a9c85527eac17a52891302e45201a6401935e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDialogflowConversationProfile.GoogleDialogflowConversationProfileHumanAgentAssistantConfigMessageAnalysisConfig",
    jsii_struct_bases=[],
    name_mapping={
        "enable_entity_extraction": "enableEntityExtraction",
        "enable_sentiment_analysis": "enableSentimentAnalysis",
    },
)
class GoogleDialogflowConversationProfileHumanAgentAssistantConfigMessageAnalysisConfig:
    def __init__(
        self,
        *,
        enable_entity_extraction: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_sentiment_analysis: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param enable_entity_extraction: Enable entity extraction in conversation messages on agent assist stage. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#enable_entity_extraction GoogleDialogflowConversationProfile#enable_entity_extraction}
        :param enable_sentiment_analysis: Enable sentiment analysis in conversation messages on agent assist stage. Sentiment analysis inspects user input and identifies the prevailing subjective opinion, especially to determine a user's attitude as positive, negative, or neutral. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#enable_sentiment_analysis GoogleDialogflowConversationProfile#enable_sentiment_analysis}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd78da24e57371d334902f592a6a6f0a06304a41e1ad8844e58c546fc8b0c459)
            check_type(argname="argument enable_entity_extraction", value=enable_entity_extraction, expected_type=type_hints["enable_entity_extraction"])
            check_type(argname="argument enable_sentiment_analysis", value=enable_sentiment_analysis, expected_type=type_hints["enable_sentiment_analysis"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if enable_entity_extraction is not None:
            self._values["enable_entity_extraction"] = enable_entity_extraction
        if enable_sentiment_analysis is not None:
            self._values["enable_sentiment_analysis"] = enable_sentiment_analysis

    @builtins.property
    def enable_entity_extraction(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Enable entity extraction in conversation messages on agent assist stage.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#enable_entity_extraction GoogleDialogflowConversationProfile#enable_entity_extraction}
        '''
        result = self._values.get("enable_entity_extraction")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def enable_sentiment_analysis(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Enable sentiment analysis in conversation messages on agent assist stage.

        Sentiment analysis inspects user input and identifies the prevailing subjective opinion, especially to determine a user's attitude as positive, negative, or neutral.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#enable_sentiment_analysis GoogleDialogflowConversationProfile#enable_sentiment_analysis}
        '''
        result = self._values.get("enable_sentiment_analysis")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDialogflowConversationProfileHumanAgentAssistantConfigMessageAnalysisConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDialogflowConversationProfileHumanAgentAssistantConfigMessageAnalysisConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDialogflowConversationProfile.GoogleDialogflowConversationProfileHumanAgentAssistantConfigMessageAnalysisConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2a90ddd1e65bdeb981fa1d4f2e12327d344452549eddfcba566649b59911fd8b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetEnableEntityExtraction")
    def reset_enable_entity_extraction(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnableEntityExtraction", []))

    @jsii.member(jsii_name="resetEnableSentimentAnalysis")
    def reset_enable_sentiment_analysis(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnableSentimentAnalysis", []))

    @builtins.property
    @jsii.member(jsii_name="enableEntityExtractionInput")
    def enable_entity_extraction_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enableEntityExtractionInput"))

    @builtins.property
    @jsii.member(jsii_name="enableSentimentAnalysisInput")
    def enable_sentiment_analysis_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enableSentimentAnalysisInput"))

    @builtins.property
    @jsii.member(jsii_name="enableEntityExtraction")
    def enable_entity_extraction(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enableEntityExtraction"))

    @enable_entity_extraction.setter
    def enable_entity_extraction(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0680663466b45830af6dfaabd3d5c04e8da9455bf0284086b297f9a0ea8a2bd7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableEntityExtraction", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enableSentimentAnalysis")
    def enable_sentiment_analysis(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enableSentimentAnalysis"))

    @enable_sentiment_analysis.setter
    def enable_sentiment_analysis(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3eb08dced778aebeb7401b79ae9ec0701bf3138e1f4cfabbafc31fbd7a0c84cd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableSentimentAnalysis", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDialogflowConversationProfileHumanAgentAssistantConfigMessageAnalysisConfig]:
        return typing.cast(typing.Optional[GoogleDialogflowConversationProfileHumanAgentAssistantConfigMessageAnalysisConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDialogflowConversationProfileHumanAgentAssistantConfigMessageAnalysisConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ed2ab3143ae8668b9babf4d3142e390f39f4e958d305d3499d6ee6e81b0c2c0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDialogflowConversationProfile.GoogleDialogflowConversationProfileHumanAgentAssistantConfigNotificationConfig",
    jsii_struct_bases=[],
    name_mapping={"message_format": "messageFormat", "topic": "topic"},
)
class GoogleDialogflowConversationProfileHumanAgentAssistantConfigNotificationConfig:
    def __init__(
        self,
        *,
        message_format: typing.Optional[builtins.str] = None,
        topic: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param message_format: Format of the message Possible values: ["MESSAGE_FORMAT_UNSPECIFIED", "PROTO", "JSON"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#message_format GoogleDialogflowConversationProfile#message_format}
        :param topic: Name of the Pub/Sub topic to publish conversation events. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#topic GoogleDialogflowConversationProfile#topic}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e15ef4ad139058a3f4478c58b2af9f64f35baa6d48cb570ceebe8f22748d52aa)
            check_type(argname="argument message_format", value=message_format, expected_type=type_hints["message_format"])
            check_type(argname="argument topic", value=topic, expected_type=type_hints["topic"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if message_format is not None:
            self._values["message_format"] = message_format
        if topic is not None:
            self._values["topic"] = topic

    @builtins.property
    def message_format(self) -> typing.Optional[builtins.str]:
        '''Format of the message Possible values: ["MESSAGE_FORMAT_UNSPECIFIED", "PROTO", "JSON"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#message_format GoogleDialogflowConversationProfile#message_format}
        '''
        result = self._values.get("message_format")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def topic(self) -> typing.Optional[builtins.str]:
        '''Name of the Pub/Sub topic to publish conversation events.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#topic GoogleDialogflowConversationProfile#topic}
        '''
        result = self._values.get("topic")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDialogflowConversationProfileHumanAgentAssistantConfigNotificationConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDialogflowConversationProfileHumanAgentAssistantConfigNotificationConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDialogflowConversationProfile.GoogleDialogflowConversationProfileHumanAgentAssistantConfigNotificationConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__076b4fca6c3548f8ea40bef95e67e33e4f648dc92a959fb454ae4c2b05cf8e58)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetMessageFormat")
    def reset_message_format(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMessageFormat", []))

    @jsii.member(jsii_name="resetTopic")
    def reset_topic(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTopic", []))

    @builtins.property
    @jsii.member(jsii_name="messageFormatInput")
    def message_format_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "messageFormatInput"))

    @builtins.property
    @jsii.member(jsii_name="topicInput")
    def topic_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "topicInput"))

    @builtins.property
    @jsii.member(jsii_name="messageFormat")
    def message_format(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "messageFormat"))

    @message_format.setter
    def message_format(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0e360033a53be3a1eb81cef8a33af893ac4cbb02bd779c3d0cb4cb3ecf120bc1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "messageFormat", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="topic")
    def topic(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "topic"))

    @topic.setter
    def topic(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__874f0d17b5f1d9428cf4eb7eab849f1fe6b9d84583b051b519c40a8c7b648b0e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "topic", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDialogflowConversationProfileHumanAgentAssistantConfigNotificationConfig]:
        return typing.cast(typing.Optional[GoogleDialogflowConversationProfileHumanAgentAssistantConfigNotificationConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDialogflowConversationProfileHumanAgentAssistantConfigNotificationConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__31e689c80702f7b994028f7c9801935b9f0f6d974ad163a03e0b52b71dd835ef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleDialogflowConversationProfileHumanAgentAssistantConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDialogflowConversationProfile.GoogleDialogflowConversationProfileHumanAgentAssistantConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__729c31f4016fad11f4ae15257f3aa815fbf71407c5d9c53d60ef854362ecad2d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putEndUserSuggestionConfig")
    def put_end_user_suggestion_config(
        self,
        *,
        disable_high_latency_features_sync_delivery: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        feature_configs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigs, typing.Dict[builtins.str, typing.Any]]]]] = None,
        generators: typing.Optional[typing.Sequence[builtins.str]] = None,
        group_suggestion_responses: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param disable_high_latency_features_sync_delivery: When disableHighLatencyFeaturesSyncDelivery is true and using the AnalyzeContent API, we will not deliver the responses from high latency features in the API response. The humanAgentAssistantConfig.notification_config must be configured and enableEventBasedSuggestion must be set to true to receive the responses from high latency features in Pub/Sub. High latency feature(s): KNOWLEDGE_ASSIST Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#disable_high_latency_features_sync_delivery GoogleDialogflowConversationProfile#disable_high_latency_features_sync_delivery}
        :param feature_configs: feature_configs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#feature_configs GoogleDialogflowConversationProfile#feature_configs}
        :param generators: List of various generator resource names used in the conversation profile. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#generators GoogleDialogflowConversationProfile#generators}
        :param group_suggestion_responses: If groupSuggestionResponses is false, and there are multiple featureConfigs in event based suggestion or StreamingAnalyzeContent, we will try to deliver suggestions to customers as soon as we get new suggestion. Different type of suggestions based on the same context will be in separate Pub/Sub event or StreamingAnalyzeContentResponse. If groupSuggestionResponses set to true. All the suggestions to the same participant based on the same context will be grouped into a single Pub/Sub event or StreamingAnalyzeContentResponse. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#group_suggestion_responses GoogleDialogflowConversationProfile#group_suggestion_responses}
        '''
        value = GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfig(
            disable_high_latency_features_sync_delivery=disable_high_latency_features_sync_delivery,
            feature_configs=feature_configs,
            generators=generators,
            group_suggestion_responses=group_suggestion_responses,
        )

        return typing.cast(None, jsii.invoke(self, "putEndUserSuggestionConfig", [value]))

    @jsii.member(jsii_name="putHumanAgentSuggestionConfig")
    def put_human_agent_suggestion_config(
        self,
        *,
        disable_high_latency_features_sync_delivery: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        feature_configs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleDialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigs, typing.Dict[builtins.str, typing.Any]]]]] = None,
        generators: typing.Optional[typing.Sequence[builtins.str]] = None,
        group_suggestion_responses: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param disable_high_latency_features_sync_delivery: When disableHighLatencyFeaturesSyncDelivery is true and using the AnalyzeContent API, we will not deliver the responses from high latency features in the API response. The humanAgentAssistantConfig.notification_config must be configured and enableEventBasedSuggestion must be set to true to receive the responses from high latency features in Pub/Sub. High latency feature(s): KNOWLEDGE_ASSIST Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#disable_high_latency_features_sync_delivery GoogleDialogflowConversationProfile#disable_high_latency_features_sync_delivery}
        :param feature_configs: feature_configs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#feature_configs GoogleDialogflowConversationProfile#feature_configs}
        :param generators: List of various generator resource names used in the conversation profile. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#generators GoogleDialogflowConversationProfile#generators}
        :param group_suggestion_responses: If groupSuggestionResponses is false, and there are multiple featureConfigs in event based suggestion or StreamingAnalyzeContent, we will try to deliver suggestions to customers as soon as we get new suggestion. Different type of suggestions based on the same context will be in separate Pub/Sub event or StreamingAnalyzeContentResponse. If groupSuggestionResponses set to true. All the suggestions to the same participant based on the same context will be grouped into a single Pub/Sub event or StreamingAnalyzeContentResponse. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#group_suggestion_responses GoogleDialogflowConversationProfile#group_suggestion_responses}
        '''
        value = GoogleDialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfig(
            disable_high_latency_features_sync_delivery=disable_high_latency_features_sync_delivery,
            feature_configs=feature_configs,
            generators=generators,
            group_suggestion_responses=group_suggestion_responses,
        )

        return typing.cast(None, jsii.invoke(self, "putHumanAgentSuggestionConfig", [value]))

    @jsii.member(jsii_name="putMessageAnalysisConfig")
    def put_message_analysis_config(
        self,
        *,
        enable_entity_extraction: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_sentiment_analysis: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param enable_entity_extraction: Enable entity extraction in conversation messages on agent assist stage. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#enable_entity_extraction GoogleDialogflowConversationProfile#enable_entity_extraction}
        :param enable_sentiment_analysis: Enable sentiment analysis in conversation messages on agent assist stage. Sentiment analysis inspects user input and identifies the prevailing subjective opinion, especially to determine a user's attitude as positive, negative, or neutral. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#enable_sentiment_analysis GoogleDialogflowConversationProfile#enable_sentiment_analysis}
        '''
        value = GoogleDialogflowConversationProfileHumanAgentAssistantConfigMessageAnalysisConfig(
            enable_entity_extraction=enable_entity_extraction,
            enable_sentiment_analysis=enable_sentiment_analysis,
        )

        return typing.cast(None, jsii.invoke(self, "putMessageAnalysisConfig", [value]))

    @jsii.member(jsii_name="putNotificationConfig")
    def put_notification_config(
        self,
        *,
        message_format: typing.Optional[builtins.str] = None,
        topic: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param message_format: Format of the message Possible values: ["MESSAGE_FORMAT_UNSPECIFIED", "PROTO", "JSON"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#message_format GoogleDialogflowConversationProfile#message_format}
        :param topic: Name of the Pub/Sub topic to publish conversation events. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#topic GoogleDialogflowConversationProfile#topic}
        '''
        value = GoogleDialogflowConversationProfileHumanAgentAssistantConfigNotificationConfig(
            message_format=message_format, topic=topic
        )

        return typing.cast(None, jsii.invoke(self, "putNotificationConfig", [value]))

    @jsii.member(jsii_name="resetEndUserSuggestionConfig")
    def reset_end_user_suggestion_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEndUserSuggestionConfig", []))

    @jsii.member(jsii_name="resetHumanAgentSuggestionConfig")
    def reset_human_agent_suggestion_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHumanAgentSuggestionConfig", []))

    @jsii.member(jsii_name="resetMessageAnalysisConfig")
    def reset_message_analysis_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMessageAnalysisConfig", []))

    @jsii.member(jsii_name="resetNotificationConfig")
    def reset_notification_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNotificationConfig", []))

    @builtins.property
    @jsii.member(jsii_name="endUserSuggestionConfig")
    def end_user_suggestion_config(
        self,
    ) -> GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigOutputReference:
        return typing.cast(GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigOutputReference, jsii.get(self, "endUserSuggestionConfig"))

    @builtins.property
    @jsii.member(jsii_name="humanAgentSuggestionConfig")
    def human_agent_suggestion_config(
        self,
    ) -> GoogleDialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigOutputReference:
        return typing.cast(GoogleDialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigOutputReference, jsii.get(self, "humanAgentSuggestionConfig"))

    @builtins.property
    @jsii.member(jsii_name="messageAnalysisConfig")
    def message_analysis_config(
        self,
    ) -> GoogleDialogflowConversationProfileHumanAgentAssistantConfigMessageAnalysisConfigOutputReference:
        return typing.cast(GoogleDialogflowConversationProfileHumanAgentAssistantConfigMessageAnalysisConfigOutputReference, jsii.get(self, "messageAnalysisConfig"))

    @builtins.property
    @jsii.member(jsii_name="notificationConfig")
    def notification_config(
        self,
    ) -> GoogleDialogflowConversationProfileHumanAgentAssistantConfigNotificationConfigOutputReference:
        return typing.cast(GoogleDialogflowConversationProfileHumanAgentAssistantConfigNotificationConfigOutputReference, jsii.get(self, "notificationConfig"))

    @builtins.property
    @jsii.member(jsii_name="endUserSuggestionConfigInput")
    def end_user_suggestion_config_input(
        self,
    ) -> typing.Optional[GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfig]:
        return typing.cast(typing.Optional[GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfig], jsii.get(self, "endUserSuggestionConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="humanAgentSuggestionConfigInput")
    def human_agent_suggestion_config_input(
        self,
    ) -> typing.Optional[GoogleDialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfig]:
        return typing.cast(typing.Optional[GoogleDialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfig], jsii.get(self, "humanAgentSuggestionConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="messageAnalysisConfigInput")
    def message_analysis_config_input(
        self,
    ) -> typing.Optional[GoogleDialogflowConversationProfileHumanAgentAssistantConfigMessageAnalysisConfig]:
        return typing.cast(typing.Optional[GoogleDialogflowConversationProfileHumanAgentAssistantConfigMessageAnalysisConfig], jsii.get(self, "messageAnalysisConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="notificationConfigInput")
    def notification_config_input(
        self,
    ) -> typing.Optional[GoogleDialogflowConversationProfileHumanAgentAssistantConfigNotificationConfig]:
        return typing.cast(typing.Optional[GoogleDialogflowConversationProfileHumanAgentAssistantConfigNotificationConfig], jsii.get(self, "notificationConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDialogflowConversationProfileHumanAgentAssistantConfig]:
        return typing.cast(typing.Optional[GoogleDialogflowConversationProfileHumanAgentAssistantConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDialogflowConversationProfileHumanAgentAssistantConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f1d552013363bcc41d4303ed6bd46defe6d901d615d17100dbe28c6681dcc202)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDialogflowConversationProfile.GoogleDialogflowConversationProfileHumanAgentHandoffConfig",
    jsii_struct_bases=[],
    name_mapping={"live_person_config": "livePersonConfig"},
)
class GoogleDialogflowConversationProfileHumanAgentHandoffConfig:
    def __init__(
        self,
        *,
        live_person_config: typing.Optional[typing.Union["GoogleDialogflowConversationProfileHumanAgentHandoffConfigLivePersonConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param live_person_config: live_person_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#live_person_config GoogleDialogflowConversationProfile#live_person_config}
        '''
        if isinstance(live_person_config, dict):
            live_person_config = GoogleDialogflowConversationProfileHumanAgentHandoffConfigLivePersonConfig(**live_person_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf5f8e4da1d49ef730b303772a9d01e4c07e9da970df73deb90f4ae7f0baf73b)
            check_type(argname="argument live_person_config", value=live_person_config, expected_type=type_hints["live_person_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if live_person_config is not None:
            self._values["live_person_config"] = live_person_config

    @builtins.property
    def live_person_config(
        self,
    ) -> typing.Optional["GoogleDialogflowConversationProfileHumanAgentHandoffConfigLivePersonConfig"]:
        '''live_person_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#live_person_config GoogleDialogflowConversationProfile#live_person_config}
        '''
        result = self._values.get("live_person_config")
        return typing.cast(typing.Optional["GoogleDialogflowConversationProfileHumanAgentHandoffConfigLivePersonConfig"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDialogflowConversationProfileHumanAgentHandoffConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDialogflowConversationProfile.GoogleDialogflowConversationProfileHumanAgentHandoffConfigLivePersonConfig",
    jsii_struct_bases=[],
    name_mapping={"account_number": "accountNumber"},
)
class GoogleDialogflowConversationProfileHumanAgentHandoffConfigLivePersonConfig:
    def __init__(self, *, account_number: builtins.str) -> None:
        '''
        :param account_number: Account number of the LivePerson account to connect. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#account_number GoogleDialogflowConversationProfile#account_number}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4585ed9a37855bb406defc1c088ecf1aed482ee912c1ac631db64163e546351a)
            check_type(argname="argument account_number", value=account_number, expected_type=type_hints["account_number"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "account_number": account_number,
        }

    @builtins.property
    def account_number(self) -> builtins.str:
        '''Account number of the LivePerson account to connect.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#account_number GoogleDialogflowConversationProfile#account_number}
        '''
        result = self._values.get("account_number")
        assert result is not None, "Required property 'account_number' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDialogflowConversationProfileHumanAgentHandoffConfigLivePersonConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDialogflowConversationProfileHumanAgentHandoffConfigLivePersonConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDialogflowConversationProfile.GoogleDialogflowConversationProfileHumanAgentHandoffConfigLivePersonConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f5599690d842ffc6a714c71b5c0a56ed01dbe4859316678f9c7256e664aa8859)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="accountNumberInput")
    def account_number_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "accountNumberInput"))

    @builtins.property
    @jsii.member(jsii_name="accountNumber")
    def account_number(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "accountNumber"))

    @account_number.setter
    def account_number(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f73419a9dd7044a795d93356cddd27e6a97e012b989d1797e1d88861863c0ef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accountNumber", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDialogflowConversationProfileHumanAgentHandoffConfigLivePersonConfig]:
        return typing.cast(typing.Optional[GoogleDialogflowConversationProfileHumanAgentHandoffConfigLivePersonConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDialogflowConversationProfileHumanAgentHandoffConfigLivePersonConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e1112fde6594c17e454468c48fa08706eddabb87d8e8cb58ccea9f41f58933b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleDialogflowConversationProfileHumanAgentHandoffConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDialogflowConversationProfile.GoogleDialogflowConversationProfileHumanAgentHandoffConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__191a5ba23c0a0f72335d6a4541cc1c089f13a32d9a259406fa640fb55eb8918a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putLivePersonConfig")
    def put_live_person_config(self, *, account_number: builtins.str) -> None:
        '''
        :param account_number: Account number of the LivePerson account to connect. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#account_number GoogleDialogflowConversationProfile#account_number}
        '''
        value = GoogleDialogflowConversationProfileHumanAgentHandoffConfigLivePersonConfig(
            account_number=account_number
        )

        return typing.cast(None, jsii.invoke(self, "putLivePersonConfig", [value]))

    @jsii.member(jsii_name="resetLivePersonConfig")
    def reset_live_person_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLivePersonConfig", []))

    @builtins.property
    @jsii.member(jsii_name="livePersonConfig")
    def live_person_config(
        self,
    ) -> GoogleDialogflowConversationProfileHumanAgentHandoffConfigLivePersonConfigOutputReference:
        return typing.cast(GoogleDialogflowConversationProfileHumanAgentHandoffConfigLivePersonConfigOutputReference, jsii.get(self, "livePersonConfig"))

    @builtins.property
    @jsii.member(jsii_name="livePersonConfigInput")
    def live_person_config_input(
        self,
    ) -> typing.Optional[GoogleDialogflowConversationProfileHumanAgentHandoffConfigLivePersonConfig]:
        return typing.cast(typing.Optional[GoogleDialogflowConversationProfileHumanAgentHandoffConfigLivePersonConfig], jsii.get(self, "livePersonConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDialogflowConversationProfileHumanAgentHandoffConfig]:
        return typing.cast(typing.Optional[GoogleDialogflowConversationProfileHumanAgentHandoffConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDialogflowConversationProfileHumanAgentHandoffConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fb7a306c0a3bf5dd70c1b9704b20ef592fa9bc2b98b024bcbff13b300d4c81d5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDialogflowConversationProfile.GoogleDialogflowConversationProfileLoggingConfig",
    jsii_struct_bases=[],
    name_mapping={"enable_stackdriver_logging": "enableStackdriverLogging"},
)
class GoogleDialogflowConversationProfileLoggingConfig:
    def __init__(
        self,
        *,
        enable_stackdriver_logging: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param enable_stackdriver_logging: Whether to log conversation events. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#enable_stackdriver_logging GoogleDialogflowConversationProfile#enable_stackdriver_logging}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5c850200bcbfc0070efbedfd78dd68d40bf7089ef9300b87c7e84273e1967e96)
            check_type(argname="argument enable_stackdriver_logging", value=enable_stackdriver_logging, expected_type=type_hints["enable_stackdriver_logging"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if enable_stackdriver_logging is not None:
            self._values["enable_stackdriver_logging"] = enable_stackdriver_logging

    @builtins.property
    def enable_stackdriver_logging(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether to log conversation events.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#enable_stackdriver_logging GoogleDialogflowConversationProfile#enable_stackdriver_logging}
        '''
        result = self._values.get("enable_stackdriver_logging")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDialogflowConversationProfileLoggingConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDialogflowConversationProfileLoggingConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDialogflowConversationProfile.GoogleDialogflowConversationProfileLoggingConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9f77650b17b7d0244a4c35f027cc61a601a7581cb457e2d18163bdbefcb55bc4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetEnableStackdriverLogging")
    def reset_enable_stackdriver_logging(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnableStackdriverLogging", []))

    @builtins.property
    @jsii.member(jsii_name="enableStackdriverLoggingInput")
    def enable_stackdriver_logging_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enableStackdriverLoggingInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__b26456a21b813c85a95784880dd99a8d13b5a39ee69906eb369bf6d83ee9b8fb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableStackdriverLogging", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDialogflowConversationProfileLoggingConfig]:
        return typing.cast(typing.Optional[GoogleDialogflowConversationProfileLoggingConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDialogflowConversationProfileLoggingConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8c3e594ec2142327134a7bb5b7fe2930348981293774cb2802dc8f24460e67dc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDialogflowConversationProfile.GoogleDialogflowConversationProfileNewMessageEventNotificationConfig",
    jsii_struct_bases=[],
    name_mapping={"message_format": "messageFormat", "topic": "topic"},
)
class GoogleDialogflowConversationProfileNewMessageEventNotificationConfig:
    def __init__(
        self,
        *,
        message_format: typing.Optional[builtins.str] = None,
        topic: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param message_format: Format of the message Possible values: ["MESSAGE_FORMAT_UNSPECIFIED", "PROTO", "JSON"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#message_format GoogleDialogflowConversationProfile#message_format}
        :param topic: Name of the Pub/Sub topic to publish conversation events. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#topic GoogleDialogflowConversationProfile#topic}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eeb83ca68c0da9ef8ba18a61b9f292ae9d09c1845191777f28b6dff25d1ed3cc)
            check_type(argname="argument message_format", value=message_format, expected_type=type_hints["message_format"])
            check_type(argname="argument topic", value=topic, expected_type=type_hints["topic"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if message_format is not None:
            self._values["message_format"] = message_format
        if topic is not None:
            self._values["topic"] = topic

    @builtins.property
    def message_format(self) -> typing.Optional[builtins.str]:
        '''Format of the message Possible values: ["MESSAGE_FORMAT_UNSPECIFIED", "PROTO", "JSON"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#message_format GoogleDialogflowConversationProfile#message_format}
        '''
        result = self._values.get("message_format")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def topic(self) -> typing.Optional[builtins.str]:
        '''Name of the Pub/Sub topic to publish conversation events.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#topic GoogleDialogflowConversationProfile#topic}
        '''
        result = self._values.get("topic")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDialogflowConversationProfileNewMessageEventNotificationConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDialogflowConversationProfileNewMessageEventNotificationConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDialogflowConversationProfile.GoogleDialogflowConversationProfileNewMessageEventNotificationConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f16905f489f48bf03b317843ee322fbf4b3df4ded6a15d73fbe628f8b3c3eb1b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetMessageFormat")
    def reset_message_format(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMessageFormat", []))

    @jsii.member(jsii_name="resetTopic")
    def reset_topic(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTopic", []))

    @builtins.property
    @jsii.member(jsii_name="messageFormatInput")
    def message_format_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "messageFormatInput"))

    @builtins.property
    @jsii.member(jsii_name="topicInput")
    def topic_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "topicInput"))

    @builtins.property
    @jsii.member(jsii_name="messageFormat")
    def message_format(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "messageFormat"))

    @message_format.setter
    def message_format(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__538be31f790819ae360e6fa2a90b9d9bd1afc550f8badd827d98fce0c7fde97b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "messageFormat", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="topic")
    def topic(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "topic"))

    @topic.setter
    def topic(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b225d3acebf81a4293390b2bc2f6aa5b89415ef6ec8c914c74c4d1785b69d0d7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "topic", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDialogflowConversationProfileNewMessageEventNotificationConfig]:
        return typing.cast(typing.Optional[GoogleDialogflowConversationProfileNewMessageEventNotificationConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDialogflowConversationProfileNewMessageEventNotificationConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7eeacef626afd43433cc5fac0e5ba1ec80885ca5d3cf8faf22a7f6408a19d650)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDialogflowConversationProfile.GoogleDialogflowConversationProfileNotificationConfig",
    jsii_struct_bases=[],
    name_mapping={"message_format": "messageFormat", "topic": "topic"},
)
class GoogleDialogflowConversationProfileNotificationConfig:
    def __init__(
        self,
        *,
        message_format: typing.Optional[builtins.str] = None,
        topic: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param message_format: Format of the message Possible values: ["MESSAGE_FORMAT_UNSPECIFIED", "PROTO", "JSON"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#message_format GoogleDialogflowConversationProfile#message_format}
        :param topic: Name of the Pub/Sub topic to publish conversation events. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#topic GoogleDialogflowConversationProfile#topic}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__984055048436815db863e6b168ccbd31005bbc05efc78d7b2b714636b50c7b11)
            check_type(argname="argument message_format", value=message_format, expected_type=type_hints["message_format"])
            check_type(argname="argument topic", value=topic, expected_type=type_hints["topic"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if message_format is not None:
            self._values["message_format"] = message_format
        if topic is not None:
            self._values["topic"] = topic

    @builtins.property
    def message_format(self) -> typing.Optional[builtins.str]:
        '''Format of the message Possible values: ["MESSAGE_FORMAT_UNSPECIFIED", "PROTO", "JSON"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#message_format GoogleDialogflowConversationProfile#message_format}
        '''
        result = self._values.get("message_format")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def topic(self) -> typing.Optional[builtins.str]:
        '''Name of the Pub/Sub topic to publish conversation events.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#topic GoogleDialogflowConversationProfile#topic}
        '''
        result = self._values.get("topic")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDialogflowConversationProfileNotificationConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDialogflowConversationProfileNotificationConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDialogflowConversationProfile.GoogleDialogflowConversationProfileNotificationConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ad7164d2531051e8dcb1ec21b9d3e6d9a5be3a0aceccd3a14bd65154dce033ca)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetMessageFormat")
    def reset_message_format(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMessageFormat", []))

    @jsii.member(jsii_name="resetTopic")
    def reset_topic(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTopic", []))

    @builtins.property
    @jsii.member(jsii_name="messageFormatInput")
    def message_format_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "messageFormatInput"))

    @builtins.property
    @jsii.member(jsii_name="topicInput")
    def topic_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "topicInput"))

    @builtins.property
    @jsii.member(jsii_name="messageFormat")
    def message_format(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "messageFormat"))

    @message_format.setter
    def message_format(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ad61f606c7b5575e61ea02c58be47b22241c3b5d33bb653f4688b04ed1abe697)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "messageFormat", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="topic")
    def topic(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "topic"))

    @topic.setter
    def topic(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2b83dec2dcb26d76f118884e38dba30eb35fab3ade7de20832542de9d4868a34)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "topic", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDialogflowConversationProfileNotificationConfig]:
        return typing.cast(typing.Optional[GoogleDialogflowConversationProfileNotificationConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDialogflowConversationProfileNotificationConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ebe4400c259b7e110c2aadb35bd9ef8785289162ce9d4ebc04f75bf44692903)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDialogflowConversationProfile.GoogleDialogflowConversationProfileSttConfig",
    jsii_struct_bases=[],
    name_mapping={
        "audio_encoding": "audioEncoding",
        "enable_word_info": "enableWordInfo",
        "language_code": "languageCode",
        "model": "model",
        "sample_rate_hertz": "sampleRateHertz",
        "speech_model_variant": "speechModelVariant",
        "use_timeout_based_endpointing": "useTimeoutBasedEndpointing",
    },
)
class GoogleDialogflowConversationProfileSttConfig:
    def __init__(
        self,
        *,
        audio_encoding: typing.Optional[builtins.str] = None,
        enable_word_info: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        language_code: typing.Optional[builtins.str] = None,
        model: typing.Optional[builtins.str] = None,
        sample_rate_hertz: typing.Optional[jsii.Number] = None,
        speech_model_variant: typing.Optional[builtins.str] = None,
        use_timeout_based_endpointing: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param audio_encoding: Audio encoding of the audio content to process. Possible values: ["AUDIO_ENCODING_UNSPECIFIED", "AUDIO_ENCODING_LINEAR_16", "AUDIO_ENCODING_FLAC", "AUDIO_ENCODING_MULAW", "AUDIO_ENCODING_AMR", "AUDIO_ENCODING_AMR_WB", "AUDIO_ENCODING_OGG_OPUS", "AUDIOENCODING_SPEEX_WITH_HEADER_BYTE"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#audio_encoding GoogleDialogflowConversationProfile#audio_encoding}
        :param enable_word_info: If true, Dialogflow returns SpeechWordInfo in StreamingRecognitionResult with information about the recognized speech words. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#enable_word_info GoogleDialogflowConversationProfile#enable_word_info}
        :param language_code: The language of the supplied audio. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#language_code GoogleDialogflowConversationProfile#language_code}
        :param model: Which Speech model to select. Leave this field unspecified to use Agent Speech settings for model selection. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#model GoogleDialogflowConversationProfile#model}
        :param sample_rate_hertz: Sample rate (in Hertz) of the audio content sent in the query. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#sample_rate_hertz GoogleDialogflowConversationProfile#sample_rate_hertz}
        :param speech_model_variant: The speech model used in speech to text. Possible values: ["SPEECH_MODEL_VARIANT_UNSPECIFIED", "USE_BEST_AVAILABLE", "USE_STANDARD", "USE_ENHANCED"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#speech_model_variant GoogleDialogflowConversationProfile#speech_model_variant}
        :param use_timeout_based_endpointing: Use timeout based endpointing, interpreting endpointer sensitivy as seconds of timeout value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#use_timeout_based_endpointing GoogleDialogflowConversationProfile#use_timeout_based_endpointing}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e18660b13cdbd17fe84b031f9afd91474ec3b3788d8d500b899ce1e4fdfae41e)
            check_type(argname="argument audio_encoding", value=audio_encoding, expected_type=type_hints["audio_encoding"])
            check_type(argname="argument enable_word_info", value=enable_word_info, expected_type=type_hints["enable_word_info"])
            check_type(argname="argument language_code", value=language_code, expected_type=type_hints["language_code"])
            check_type(argname="argument model", value=model, expected_type=type_hints["model"])
            check_type(argname="argument sample_rate_hertz", value=sample_rate_hertz, expected_type=type_hints["sample_rate_hertz"])
            check_type(argname="argument speech_model_variant", value=speech_model_variant, expected_type=type_hints["speech_model_variant"])
            check_type(argname="argument use_timeout_based_endpointing", value=use_timeout_based_endpointing, expected_type=type_hints["use_timeout_based_endpointing"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if audio_encoding is not None:
            self._values["audio_encoding"] = audio_encoding
        if enable_word_info is not None:
            self._values["enable_word_info"] = enable_word_info
        if language_code is not None:
            self._values["language_code"] = language_code
        if model is not None:
            self._values["model"] = model
        if sample_rate_hertz is not None:
            self._values["sample_rate_hertz"] = sample_rate_hertz
        if speech_model_variant is not None:
            self._values["speech_model_variant"] = speech_model_variant
        if use_timeout_based_endpointing is not None:
            self._values["use_timeout_based_endpointing"] = use_timeout_based_endpointing

    @builtins.property
    def audio_encoding(self) -> typing.Optional[builtins.str]:
        '''Audio encoding of the audio content to process. Possible values: ["AUDIO_ENCODING_UNSPECIFIED", "AUDIO_ENCODING_LINEAR_16", "AUDIO_ENCODING_FLAC", "AUDIO_ENCODING_MULAW", "AUDIO_ENCODING_AMR", "AUDIO_ENCODING_AMR_WB", "AUDIO_ENCODING_OGG_OPUS", "AUDIOENCODING_SPEEX_WITH_HEADER_BYTE"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#audio_encoding GoogleDialogflowConversationProfile#audio_encoding}
        '''
        result = self._values.get("audio_encoding")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enable_word_info(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If true, Dialogflow returns SpeechWordInfo in StreamingRecognitionResult with information about the recognized speech words.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#enable_word_info GoogleDialogflowConversationProfile#enable_word_info}
        '''
        result = self._values.get("enable_word_info")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def language_code(self) -> typing.Optional[builtins.str]:
        '''The language of the supplied audio.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#language_code GoogleDialogflowConversationProfile#language_code}
        '''
        result = self._values.get("language_code")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def model(self) -> typing.Optional[builtins.str]:
        '''Which Speech model to select. Leave this field unspecified to use Agent Speech settings for model selection.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#model GoogleDialogflowConversationProfile#model}
        '''
        result = self._values.get("model")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sample_rate_hertz(self) -> typing.Optional[jsii.Number]:
        '''Sample rate (in Hertz) of the audio content sent in the query.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#sample_rate_hertz GoogleDialogflowConversationProfile#sample_rate_hertz}
        '''
        result = self._values.get("sample_rate_hertz")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def speech_model_variant(self) -> typing.Optional[builtins.str]:
        '''The speech model used in speech to text. Possible values: ["SPEECH_MODEL_VARIANT_UNSPECIFIED", "USE_BEST_AVAILABLE", "USE_STANDARD", "USE_ENHANCED"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#speech_model_variant GoogleDialogflowConversationProfile#speech_model_variant}
        '''
        result = self._values.get("speech_model_variant")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def use_timeout_based_endpointing(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Use timeout based endpointing, interpreting endpointer sensitivy as seconds of timeout value.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#use_timeout_based_endpointing GoogleDialogflowConversationProfile#use_timeout_based_endpointing}
        '''
        result = self._values.get("use_timeout_based_endpointing")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDialogflowConversationProfileSttConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDialogflowConversationProfileSttConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDialogflowConversationProfile.GoogleDialogflowConversationProfileSttConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__74232fefc7ed8298dce4e8836872cbbf1f3e44f33379e0f631c3d4f7da759884)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAudioEncoding")
    def reset_audio_encoding(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAudioEncoding", []))

    @jsii.member(jsii_name="resetEnableWordInfo")
    def reset_enable_word_info(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnableWordInfo", []))

    @jsii.member(jsii_name="resetLanguageCode")
    def reset_language_code(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLanguageCode", []))

    @jsii.member(jsii_name="resetModel")
    def reset_model(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetModel", []))

    @jsii.member(jsii_name="resetSampleRateHertz")
    def reset_sample_rate_hertz(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSampleRateHertz", []))

    @jsii.member(jsii_name="resetSpeechModelVariant")
    def reset_speech_model_variant(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSpeechModelVariant", []))

    @jsii.member(jsii_name="resetUseTimeoutBasedEndpointing")
    def reset_use_timeout_based_endpointing(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUseTimeoutBasedEndpointing", []))

    @builtins.property
    @jsii.member(jsii_name="audioEncodingInput")
    def audio_encoding_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "audioEncodingInput"))

    @builtins.property
    @jsii.member(jsii_name="enableWordInfoInput")
    def enable_word_info_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enableWordInfoInput"))

    @builtins.property
    @jsii.member(jsii_name="languageCodeInput")
    def language_code_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "languageCodeInput"))

    @builtins.property
    @jsii.member(jsii_name="modelInput")
    def model_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "modelInput"))

    @builtins.property
    @jsii.member(jsii_name="sampleRateHertzInput")
    def sample_rate_hertz_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "sampleRateHertzInput"))

    @builtins.property
    @jsii.member(jsii_name="speechModelVariantInput")
    def speech_model_variant_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "speechModelVariantInput"))

    @builtins.property
    @jsii.member(jsii_name="useTimeoutBasedEndpointingInput")
    def use_timeout_based_endpointing_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "useTimeoutBasedEndpointingInput"))

    @builtins.property
    @jsii.member(jsii_name="audioEncoding")
    def audio_encoding(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "audioEncoding"))

    @audio_encoding.setter
    def audio_encoding(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b67bd6c3bac05324e9544c93a0bc021db611750016a8c75509a2b3df5e2f2c0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "audioEncoding", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enableWordInfo")
    def enable_word_info(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enableWordInfo"))

    @enable_word_info.setter
    def enable_word_info(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7598b07a18b163b9bbc275d1357bbc7d52d5f0ba69d26fc63720a7a72d03ea0b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableWordInfo", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="languageCode")
    def language_code(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "languageCode"))

    @language_code.setter
    def language_code(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5406de7f1b2b27a30e1226b53bb69a3320c4f45ed9cb1c980740fd4e51a9bd26)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "languageCode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="model")
    def model(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "model"))

    @model.setter
    def model(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc76d2d7eeacdf97a25dfdffb1a4277fb4f6337d30a2b1e12c10a35e0ab2b9de)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "model", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sampleRateHertz")
    def sample_rate_hertz(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "sampleRateHertz"))

    @sample_rate_hertz.setter
    def sample_rate_hertz(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__936fe14c326b6a049ed3f7eaedf34cbe8e7dcf4ae4d8e6064a4598d3ce412c2f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sampleRateHertz", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="speechModelVariant")
    def speech_model_variant(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "speechModelVariant"))

    @speech_model_variant.setter
    def speech_model_variant(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c383c89e3ffd61c435428ff87aafbab55ae799886a5038f1c4c142df46ca1003)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "speechModelVariant", value) # pyright: ignore[reportArgumentType]

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
            type_hints = typing.get_type_hints(_typecheckingstub__1a51a76b19f4fde469429ae61ce45efd6c2f943f7f6ee3f6e9cda698ab8b262a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "useTimeoutBasedEndpointing", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDialogflowConversationProfileSttConfig]:
        return typing.cast(typing.Optional[GoogleDialogflowConversationProfileSttConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDialogflowConversationProfileSttConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f39f0246d910577b2e0c5e758f7ebf7308a69be0284de0bb8207480cc8f5b905)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDialogflowConversationProfile.GoogleDialogflowConversationProfileTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class GoogleDialogflowConversationProfileTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#create GoogleDialogflowConversationProfile#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#delete GoogleDialogflowConversationProfile#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#update GoogleDialogflowConversationProfile#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a1be1e9797a56e5feb96ed9f7022be70fc0fbafce72fff81696f5faa5e361ae3)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#create GoogleDialogflowConversationProfile#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#delete GoogleDialogflowConversationProfile#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#update GoogleDialogflowConversationProfile#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDialogflowConversationProfileTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDialogflowConversationProfileTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDialogflowConversationProfile.GoogleDialogflowConversationProfileTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__30f9eb94fc82edaec88e2c88b7a72c3c75286a952fcd1fb85cad2c295e83b624)
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
            type_hints = typing.get_type_hints(_typecheckingstub__cb32e1116cd912923545072defb39c488c23dc1c10cb0cfa8b6cf01f51160bea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__812c318e18897e55b5ad251ab4dca348af4c2e92e5baebb031220e94f4562e94)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7568b0615df7b65c85dcfea6b5a50798b304b38d86fc111f91bc2583d6fc2278)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDialogflowConversationProfileTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDialogflowConversationProfileTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDialogflowConversationProfileTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc3aafd558b746d25624edc77add2ba9cfe3d2ebe631c8b17cf5a4294149032f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDialogflowConversationProfile.GoogleDialogflowConversationProfileTtsConfig",
    jsii_struct_bases=[],
    name_mapping={
        "effects_profile_id": "effectsProfileId",
        "pitch": "pitch",
        "speaking_rate": "speakingRate",
        "voice": "voice",
        "volume_gain_db": "volumeGainDb",
    },
)
class GoogleDialogflowConversationProfileTtsConfig:
    def __init__(
        self,
        *,
        effects_profile_id: typing.Optional[typing.Sequence[builtins.str]] = None,
        pitch: typing.Optional[jsii.Number] = None,
        speaking_rate: typing.Optional[jsii.Number] = None,
        voice: typing.Optional[typing.Union["GoogleDialogflowConversationProfileTtsConfigVoice", typing.Dict[builtins.str, typing.Any]]] = None,
        volume_gain_db: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param effects_profile_id: An identifier which selects 'audio effects' profiles that are applied on (post synthesized) text to speech. Effects are applied on top of each other in the order they are given. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#effects_profile_id GoogleDialogflowConversationProfile#effects_profile_id}
        :param pitch: Speaking pitch, in the range [-20.0, 20.0]. 20 means increase 20 semitones from the original pitch. -20 means decrease 20 semitones from the original pitch. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#pitch GoogleDialogflowConversationProfile#pitch}
        :param speaking_rate: Speaking rate/speed, in the range [0.25, 4.0]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#speaking_rate GoogleDialogflowConversationProfile#speaking_rate}
        :param voice: voice block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#voice GoogleDialogflowConversationProfile#voice}
        :param volume_gain_db: Volume gain (in dB) of the normal native volume supported by the specific voice. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#volume_gain_db GoogleDialogflowConversationProfile#volume_gain_db}
        '''
        if isinstance(voice, dict):
            voice = GoogleDialogflowConversationProfileTtsConfigVoice(**voice)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__850f57bcc02107ebebd9de87acd86c81cc55fc0b8686f7b7220f9c25d73d59d7)
            check_type(argname="argument effects_profile_id", value=effects_profile_id, expected_type=type_hints["effects_profile_id"])
            check_type(argname="argument pitch", value=pitch, expected_type=type_hints["pitch"])
            check_type(argname="argument speaking_rate", value=speaking_rate, expected_type=type_hints["speaking_rate"])
            check_type(argname="argument voice", value=voice, expected_type=type_hints["voice"])
            check_type(argname="argument volume_gain_db", value=volume_gain_db, expected_type=type_hints["volume_gain_db"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if effects_profile_id is not None:
            self._values["effects_profile_id"] = effects_profile_id
        if pitch is not None:
            self._values["pitch"] = pitch
        if speaking_rate is not None:
            self._values["speaking_rate"] = speaking_rate
        if voice is not None:
            self._values["voice"] = voice
        if volume_gain_db is not None:
            self._values["volume_gain_db"] = volume_gain_db

    @builtins.property
    def effects_profile_id(self) -> typing.Optional[typing.List[builtins.str]]:
        '''An identifier which selects 'audio effects' profiles that are applied on (post synthesized) text to speech.

        Effects are applied on top of each other in the order they are given.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#effects_profile_id GoogleDialogflowConversationProfile#effects_profile_id}
        '''
        result = self._values.get("effects_profile_id")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def pitch(self) -> typing.Optional[jsii.Number]:
        '''Speaking pitch, in the range [-20.0, 20.0]. 20 means increase 20 semitones from the original pitch. -20 means decrease 20 semitones from the original pitch.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#pitch GoogleDialogflowConversationProfile#pitch}
        '''
        result = self._values.get("pitch")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def speaking_rate(self) -> typing.Optional[jsii.Number]:
        '''Speaking rate/speed, in the range [0.25, 4.0].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#speaking_rate GoogleDialogflowConversationProfile#speaking_rate}
        '''
        result = self._values.get("speaking_rate")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def voice(
        self,
    ) -> typing.Optional["GoogleDialogflowConversationProfileTtsConfigVoice"]:
        '''voice block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#voice GoogleDialogflowConversationProfile#voice}
        '''
        result = self._values.get("voice")
        return typing.cast(typing.Optional["GoogleDialogflowConversationProfileTtsConfigVoice"], result)

    @builtins.property
    def volume_gain_db(self) -> typing.Optional[jsii.Number]:
        '''Volume gain (in dB) of the normal native volume supported by the specific voice.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#volume_gain_db GoogleDialogflowConversationProfile#volume_gain_db}
        '''
        result = self._values.get("volume_gain_db")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDialogflowConversationProfileTtsConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDialogflowConversationProfileTtsConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDialogflowConversationProfile.GoogleDialogflowConversationProfileTtsConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__99ad314ddbe107dcf424aae46d8f49c665ebf2ed1cfbdb921d69397f6fb80ee1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putVoice")
    def put_voice(
        self,
        *,
        name: typing.Optional[builtins.str] = None,
        ssml_gender: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: The name of the voice. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#name GoogleDialogflowConversationProfile#name}
        :param ssml_gender: The preferred gender of the voice. Possible values: ["SSML_VOICE_GENDER_UNSPECIFIED", "SSML_VOICE_GENDER_MALE", "SSML_VOICE_GENDER_FEMALE", "SSML_VOICE_GENDER_NEUTRAL"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#ssml_gender GoogleDialogflowConversationProfile#ssml_gender}
        '''
        value = GoogleDialogflowConversationProfileTtsConfigVoice(
            name=name, ssml_gender=ssml_gender
        )

        return typing.cast(None, jsii.invoke(self, "putVoice", [value]))

    @jsii.member(jsii_name="resetEffectsProfileId")
    def reset_effects_profile_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEffectsProfileId", []))

    @jsii.member(jsii_name="resetPitch")
    def reset_pitch(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPitch", []))

    @jsii.member(jsii_name="resetSpeakingRate")
    def reset_speaking_rate(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSpeakingRate", []))

    @jsii.member(jsii_name="resetVoice")
    def reset_voice(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVoice", []))

    @jsii.member(jsii_name="resetVolumeGainDb")
    def reset_volume_gain_db(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVolumeGainDb", []))

    @builtins.property
    @jsii.member(jsii_name="voice")
    def voice(
        self,
    ) -> "GoogleDialogflowConversationProfileTtsConfigVoiceOutputReference":
        return typing.cast("GoogleDialogflowConversationProfileTtsConfigVoiceOutputReference", jsii.get(self, "voice"))

    @builtins.property
    @jsii.member(jsii_name="effectsProfileIdInput")
    def effects_profile_id_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "effectsProfileIdInput"))

    @builtins.property
    @jsii.member(jsii_name="pitchInput")
    def pitch_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "pitchInput"))

    @builtins.property
    @jsii.member(jsii_name="speakingRateInput")
    def speaking_rate_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "speakingRateInput"))

    @builtins.property
    @jsii.member(jsii_name="voiceInput")
    def voice_input(
        self,
    ) -> typing.Optional["GoogleDialogflowConversationProfileTtsConfigVoice"]:
        return typing.cast(typing.Optional["GoogleDialogflowConversationProfileTtsConfigVoice"], jsii.get(self, "voiceInput"))

    @builtins.property
    @jsii.member(jsii_name="volumeGainDbInput")
    def volume_gain_db_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "volumeGainDbInput"))

    @builtins.property
    @jsii.member(jsii_name="effectsProfileId")
    def effects_profile_id(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "effectsProfileId"))

    @effects_profile_id.setter
    def effects_profile_id(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf9a16cdd2be634ec51e004933395bb65a84e31199a06b6bd13b4d4f6b683003)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "effectsProfileId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="pitch")
    def pitch(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "pitch"))

    @pitch.setter
    def pitch(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__df6200f0cd320ee3e557fb7d95a43192f88c6b335917c1c63c7059d81248345c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pitch", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="speakingRate")
    def speaking_rate(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "speakingRate"))

    @speaking_rate.setter
    def speaking_rate(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf5df74004cffb71c1831fcd7d732d1df42bbeb22fd50352e6ccfa7b83a12f27)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "speakingRate", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="volumeGainDb")
    def volume_gain_db(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "volumeGainDb"))

    @volume_gain_db.setter
    def volume_gain_db(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b467315dcf115ed5dcc23c44b49f03c9a75b092d5a060b8104769895f9918f8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "volumeGainDb", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDialogflowConversationProfileTtsConfig]:
        return typing.cast(typing.Optional[GoogleDialogflowConversationProfileTtsConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDialogflowConversationProfileTtsConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e46e1ee254c4a2f8ee120a61f70bd27b83b5a3361dd851304feee22dcbd5d806)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDialogflowConversationProfile.GoogleDialogflowConversationProfileTtsConfigVoice",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "ssml_gender": "ssmlGender"},
)
class GoogleDialogflowConversationProfileTtsConfigVoice:
    def __init__(
        self,
        *,
        name: typing.Optional[builtins.str] = None,
        ssml_gender: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: The name of the voice. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#name GoogleDialogflowConversationProfile#name}
        :param ssml_gender: The preferred gender of the voice. Possible values: ["SSML_VOICE_GENDER_UNSPECIFIED", "SSML_VOICE_GENDER_MALE", "SSML_VOICE_GENDER_FEMALE", "SSML_VOICE_GENDER_NEUTRAL"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#ssml_gender GoogleDialogflowConversationProfile#ssml_gender}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b6e69c14a10eb6a5d43c711faf722da843e9595213d6341e24699e1f3605aeb7)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument ssml_gender", value=ssml_gender, expected_type=type_hints["ssml_gender"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if name is not None:
            self._values["name"] = name
        if ssml_gender is not None:
            self._values["ssml_gender"] = ssml_gender

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the voice.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#name GoogleDialogflowConversationProfile#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ssml_gender(self) -> typing.Optional[builtins.str]:
        '''The preferred gender of the voice. Possible values: ["SSML_VOICE_GENDER_UNSPECIFIED", "SSML_VOICE_GENDER_MALE", "SSML_VOICE_GENDER_FEMALE", "SSML_VOICE_GENDER_NEUTRAL"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_dialogflow_conversation_profile#ssml_gender GoogleDialogflowConversationProfile#ssml_gender}
        '''
        result = self._values.get("ssml_gender")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDialogflowConversationProfileTtsConfigVoice(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDialogflowConversationProfileTtsConfigVoiceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDialogflowConversationProfile.GoogleDialogflowConversationProfileTtsConfigVoiceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2b8d805b69d745f6366b73fd63dfc4e40a0be74a49fe7972398c469bd18d4a6b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @jsii.member(jsii_name="resetSsmlGender")
    def reset_ssml_gender(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSsmlGender", []))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="ssmlGenderInput")
    def ssml_gender_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ssmlGenderInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__937963a22ecbaa10e77d508cf0df6273fc090d44d3b59c219ce13f53aaeff826)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ssmlGender")
    def ssml_gender(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ssmlGender"))

    @ssml_gender.setter
    def ssml_gender(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b1f9f646d0b27c8317ae834617cf6c53668f2370b8deebde3a481c049fc166a7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ssmlGender", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDialogflowConversationProfileTtsConfigVoice]:
        return typing.cast(typing.Optional[GoogleDialogflowConversationProfileTtsConfigVoice], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDialogflowConversationProfileTtsConfigVoice],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ba6a4eb82278005072013ecaf02addd80a5dda208e8262b26adde5712799e76)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "GoogleDialogflowConversationProfile",
    "GoogleDialogflowConversationProfileAutomatedAgentConfig",
    "GoogleDialogflowConversationProfileAutomatedAgentConfigOutputReference",
    "GoogleDialogflowConversationProfileConfig",
    "GoogleDialogflowConversationProfileHumanAgentAssistantConfig",
    "GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfig",
    "GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigs",
    "GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsConversationModelConfig",
    "GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsConversationModelConfigOutputReference",
    "GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsConversationProcessConfig",
    "GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsConversationProcessConfigOutputReference",
    "GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsList",
    "GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsOutputReference",
    "GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfig",
    "GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfigContextFilterSettings",
    "GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfigContextFilterSettingsOutputReference",
    "GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfigDialogflowQuerySource",
    "GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfigDialogflowQuerySourceHumanAgentSideConfig",
    "GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfigDialogflowQuerySourceHumanAgentSideConfigOutputReference",
    "GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfigDialogflowQuerySourceOutputReference",
    "GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfigDocumentQuerySource",
    "GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfigDocumentQuerySourceOutputReference",
    "GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfigKnowledgeBaseQuerySource",
    "GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfigKnowledgeBaseQuerySourceOutputReference",
    "GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfigOutputReference",
    "GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfigSections",
    "GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfigSectionsOutputReference",
    "GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsSuggestionFeature",
    "GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsSuggestionFeatureOutputReference",
    "GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsSuggestionTriggerSettings",
    "GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsSuggestionTriggerSettingsOutputReference",
    "GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigOutputReference",
    "GoogleDialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfig",
    "GoogleDialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigs",
    "GoogleDialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsConversationModelConfig",
    "GoogleDialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsConversationModelConfigOutputReference",
    "GoogleDialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsConversationProcessConfig",
    "GoogleDialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsConversationProcessConfigOutputReference",
    "GoogleDialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsList",
    "GoogleDialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsOutputReference",
    "GoogleDialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsQueryConfig",
    "GoogleDialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsQueryConfigContextFilterSettings",
    "GoogleDialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsQueryConfigContextFilterSettingsOutputReference",
    "GoogleDialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsQueryConfigDialogflowQuerySource",
    "GoogleDialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsQueryConfigDialogflowQuerySourceHumanAgentSideConfig",
    "GoogleDialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsQueryConfigDialogflowQuerySourceHumanAgentSideConfigOutputReference",
    "GoogleDialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsQueryConfigDialogflowQuerySourceOutputReference",
    "GoogleDialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsQueryConfigOutputReference",
    "GoogleDialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsQueryConfigSections",
    "GoogleDialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsQueryConfigSectionsOutputReference",
    "GoogleDialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsSuggestionFeature",
    "GoogleDialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsSuggestionFeatureOutputReference",
    "GoogleDialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsSuggestionTriggerSettings",
    "GoogleDialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsSuggestionTriggerSettingsOutputReference",
    "GoogleDialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigOutputReference",
    "GoogleDialogflowConversationProfileHumanAgentAssistantConfigMessageAnalysisConfig",
    "GoogleDialogflowConversationProfileHumanAgentAssistantConfigMessageAnalysisConfigOutputReference",
    "GoogleDialogflowConversationProfileHumanAgentAssistantConfigNotificationConfig",
    "GoogleDialogflowConversationProfileHumanAgentAssistantConfigNotificationConfigOutputReference",
    "GoogleDialogflowConversationProfileHumanAgentAssistantConfigOutputReference",
    "GoogleDialogflowConversationProfileHumanAgentHandoffConfig",
    "GoogleDialogflowConversationProfileHumanAgentHandoffConfigLivePersonConfig",
    "GoogleDialogflowConversationProfileHumanAgentHandoffConfigLivePersonConfigOutputReference",
    "GoogleDialogflowConversationProfileHumanAgentHandoffConfigOutputReference",
    "GoogleDialogflowConversationProfileLoggingConfig",
    "GoogleDialogflowConversationProfileLoggingConfigOutputReference",
    "GoogleDialogflowConversationProfileNewMessageEventNotificationConfig",
    "GoogleDialogflowConversationProfileNewMessageEventNotificationConfigOutputReference",
    "GoogleDialogflowConversationProfileNotificationConfig",
    "GoogleDialogflowConversationProfileNotificationConfigOutputReference",
    "GoogleDialogflowConversationProfileSttConfig",
    "GoogleDialogflowConversationProfileSttConfigOutputReference",
    "GoogleDialogflowConversationProfileTimeouts",
    "GoogleDialogflowConversationProfileTimeoutsOutputReference",
    "GoogleDialogflowConversationProfileTtsConfig",
    "GoogleDialogflowConversationProfileTtsConfigOutputReference",
    "GoogleDialogflowConversationProfileTtsConfigVoice",
    "GoogleDialogflowConversationProfileTtsConfigVoiceOutputReference",
]

publication.publish()

def _typecheckingstub__0a17f873d89d667612aaa984f37ab0b0bf78386a3f82af16cc699b733adfaf7b(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    display_name: builtins.str,
    location: builtins.str,
    automated_agent_config: typing.Optional[typing.Union[GoogleDialogflowConversationProfileAutomatedAgentConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    human_agent_assistant_config: typing.Optional[typing.Union[GoogleDialogflowConversationProfileHumanAgentAssistantConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    human_agent_handoff_config: typing.Optional[typing.Union[GoogleDialogflowConversationProfileHumanAgentHandoffConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    language_code: typing.Optional[builtins.str] = None,
    logging_config: typing.Optional[typing.Union[GoogleDialogflowConversationProfileLoggingConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    new_message_event_notification_config: typing.Optional[typing.Union[GoogleDialogflowConversationProfileNewMessageEventNotificationConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    notification_config: typing.Optional[typing.Union[GoogleDialogflowConversationProfileNotificationConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    project: typing.Optional[builtins.str] = None,
    security_settings: typing.Optional[builtins.str] = None,
    stt_config: typing.Optional[typing.Union[GoogleDialogflowConversationProfileSttConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[GoogleDialogflowConversationProfileTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    time_zone: typing.Optional[builtins.str] = None,
    tts_config: typing.Optional[typing.Union[GoogleDialogflowConversationProfileTtsConfig, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__c515b686347fa542215cc131657c8047591e51db862439506ba75a3d36982ed9(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ddebf923837b0e490ea540d92bb066e5195e63e731aa90b2047234060e052b74(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4c8fdabeb69813b7b26a73c167554b1e191662a1411b2ae645b28b2f5b18cb9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d75ac04a82c32095bdd157de9ed5f06e3d0fe2d724eb5a985ea76b75f8337f3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a2e40b785ea1b96e68c585d6a46d8d78e60deffa24521598fabf9265fffbaa3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16942d46f1a057e986d373037536aad3fae5eac6a236b86dea12449a534f8768(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ad6382496a7fc58c784e9b8a890bfdeb0cfd1bceef2b3b183c4600df2f027f7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb6b034d845d01d0c285703b82042cfccd09686c502f40031b083e21b529cead(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2596641cb81649cfa0a972372316cc459dcd76cdfbab38a4885069d7ef1b146(
    *,
    agent: builtins.str,
    session_ttl: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1d39ebeb6243f19fa3125d24b62d47106888168130b75212ea286e8e4f6a29f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59edade15f95ab8710f88b99e9173fd8ab8392fa360d22a1281eb13708a19a4a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae3f7afa45b0ee71f2d5385ad9d92b7208978d05b8336653ba347dc4b9d65c50(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ccf543c02a38cdc22baa242f6120fa6d10e750c5a8195bfcacaa44cc93aebad(
    value: typing.Optional[GoogleDialogflowConversationProfileAutomatedAgentConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38639dfe4ce7699b19a401169762b4db3ba7d183ac657111f2898e8aee01a723(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    display_name: builtins.str,
    location: builtins.str,
    automated_agent_config: typing.Optional[typing.Union[GoogleDialogflowConversationProfileAutomatedAgentConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    human_agent_assistant_config: typing.Optional[typing.Union[GoogleDialogflowConversationProfileHumanAgentAssistantConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    human_agent_handoff_config: typing.Optional[typing.Union[GoogleDialogflowConversationProfileHumanAgentHandoffConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    language_code: typing.Optional[builtins.str] = None,
    logging_config: typing.Optional[typing.Union[GoogleDialogflowConversationProfileLoggingConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    new_message_event_notification_config: typing.Optional[typing.Union[GoogleDialogflowConversationProfileNewMessageEventNotificationConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    notification_config: typing.Optional[typing.Union[GoogleDialogflowConversationProfileNotificationConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    project: typing.Optional[builtins.str] = None,
    security_settings: typing.Optional[builtins.str] = None,
    stt_config: typing.Optional[typing.Union[GoogleDialogflowConversationProfileSttConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[GoogleDialogflowConversationProfileTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    time_zone: typing.Optional[builtins.str] = None,
    tts_config: typing.Optional[typing.Union[GoogleDialogflowConversationProfileTtsConfig, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1bca06c71dcdcd764a7f9d52121ae563c50d7089edc5cfa4dc43f3963cb71643(
    *,
    end_user_suggestion_config: typing.Optional[typing.Union[GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    human_agent_suggestion_config: typing.Optional[typing.Union[GoogleDialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    message_analysis_config: typing.Optional[typing.Union[GoogleDialogflowConversationProfileHumanAgentAssistantConfigMessageAnalysisConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    notification_config: typing.Optional[typing.Union[GoogleDialogflowConversationProfileHumanAgentAssistantConfigNotificationConfig, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33edd33cd630f347ed3c005058ffab527aedf1a341319aa437427ee8538a7a86(
    *,
    disable_high_latency_features_sync_delivery: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    feature_configs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigs, typing.Dict[builtins.str, typing.Any]]]]] = None,
    generators: typing.Optional[typing.Sequence[builtins.str]] = None,
    group_suggestion_responses: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__297cb20731a08760e08b03bd05d2ca40e0bad911c2b2f20fc469deacbd45ba14(
    *,
    conversation_model_config: typing.Optional[typing.Union[GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsConversationModelConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    conversation_process_config: typing.Optional[typing.Union[GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsConversationProcessConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    disable_agent_query_logging: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enable_conversation_augmented_query: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enable_event_based_suggestion: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enable_query_suggestion_only: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enable_query_suggestion_when_no_answer: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    query_config: typing.Optional[typing.Union[GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    suggestion_feature: typing.Optional[typing.Union[GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsSuggestionFeature, typing.Dict[builtins.str, typing.Any]]] = None,
    suggestion_trigger_settings: typing.Optional[typing.Union[GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsSuggestionTriggerSettings, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d88c1aa4efd22f2f6f7fc7493aa4ab9b28e9b0fe3afd1308a7e3b63b848d38d9(
    *,
    baseline_model_version: typing.Optional[builtins.str] = None,
    model: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__49298e6b0f00f2b7d95e9f666f9135d7dc60074ce252b096d6524b78e44b8908(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df8abec4af95d66b2203cb85dec56933d6e0bf9e9769eeed5a2f56e9fef72182(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c6bc69ed048f0bfc9934059c715b34cded833295fa9fcca63fab63961fc597b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce69286f4243dd19687c56634be1ceaa7ba318e45f05fdd191569558b1eaef4b(
    value: typing.Optional[GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsConversationModelConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__49f50e5c804fec73164409c0fc234ab7e07f8e2a2671f9641616fdc7f34757b4(
    *,
    recent_sentences_count: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__211634fd9a9b938c302002f9188d9acbf73205889d358ceccfb169505bb67422(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f2e27c72c6098ae35ddded5341da736014caacbf56c10415adde0079c09f77b(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d57323306ab0292c6f4a0a747f472faf60b7f5136df680f043056ae93c9824c5(
    value: typing.Optional[GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsConversationProcessConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ade049557c95e9f0e8c289bc63f00a7b2bb55128f80d942383d7d6938ce2814d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__553e262c025e3897bd95ed3335767920f41e0a97860ddc1b88c90c348170559d(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4f22545fe83eab937f778818faba8c50dcbeb9dca392bcce58d82942df97783(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75d7c5eaa5b319709a1cd990ad3fd7a01e3bb276122fd53e12d6472ba9798abc(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75118c0cbb4bf3e97657359d3aa3f28f1aec25f0952b889624bb003e130a6217(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98e82d347df584c27e9714720b6f778bcc783d1863f7e72b2d8b4d8360b6f250(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigs]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3980ae579196aa45dd9dfe4970a65c789b24416e7c25c9555577107ed15bad8a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__90517bfc871a5c332ec9926c8f94861b060b798a0d8cfef1d1d6c381e0f5a063(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec569fbee6e9c93927fec811f0116c83483b1a78f1f4d7e7980ba0ee12886cf3(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b7ac4c891bef78f8a316a4db77848e0f5ef9d8dfaff2e2eff00be2372ac7f774(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5b5ed1746e670d653e728d5f563b2dbfbdfbb2e511c10e7a39dd67d18b74c88(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__401a5797def297e9e352552599a155fece67def4eb579828e2fc57551d2284c3(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31fa0d19a601908a479927c514a8f9d4b11cffa39631cfc0356c78b4c78585db(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigs]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__086c304372aa8e27a5954359077394abf565d98493cabb440861ca69c9ca15bf(
    *,
    confidence_threshold: typing.Optional[jsii.Number] = None,
    context_filter_settings: typing.Optional[typing.Union[GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfigContextFilterSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    dialogflow_query_source: typing.Optional[typing.Union[GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfigDialogflowQuerySource, typing.Dict[builtins.str, typing.Any]]] = None,
    document_query_source: typing.Optional[typing.Union[GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfigDocumentQuerySource, typing.Dict[builtins.str, typing.Any]]] = None,
    knowledge_base_query_source: typing.Optional[typing.Union[GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfigKnowledgeBaseQuerySource, typing.Dict[builtins.str, typing.Any]]] = None,
    max_results: typing.Optional[jsii.Number] = None,
    sections: typing.Optional[typing.Union[GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfigSections, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6458c1297e771b91da0733c933fdec144e05b1c3afb6bfc783bb33dfe8a5821(
    *,
    drop_handoff_messages: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    drop_ivr_messages: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    drop_virtual_agent_messages: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__995a13129d2ae0d9f12df33f30ffe8f9c89fe9fd390e94b4088dd3d1b23bc36a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f303b3b564a3625529067a3107526e3c7faee27b7d22733cdf00f1c15c02f71(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__47f492f40496956328fa46cf0f6e573bdc31780dff539e00a0f13f75099bca50(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__17fa2f996bb470bd6b6a67f27870f58a1fdf3623f523a113aefd5a23532e759a(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5771200000db2a8a3b094623ae3814225cceb0821f22347185146d5d1cc33351(
    value: typing.Optional[GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfigContextFilterSettings],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0abef54c34982a8445fbb530c479d536f0730de48568f61b2c84b13be0740e62(
    *,
    agent: builtins.str,
    human_agent_side_config: typing.Optional[typing.Union[GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfigDialogflowQuerySourceHumanAgentSideConfig, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50ded44e1b188f6b56ab2e6d5fa91273828d94de099d1bf3b70e6179c583d28f(
    *,
    agent: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a0d1abbae4726112987612da4c60532a5c59c2dee2b6f19539e0a3fc39222fb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11e0e820c58447988345c0daf9ffc8c4cf50b448970eb2f4fc7eb5268092eee5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4729788b6358e1a1b99901bec976a6e4520970838e0287f4182db73c5a3261ec(
    value: typing.Optional[GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfigDialogflowQuerySourceHumanAgentSideConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f62789ddc6e30febb411d153668ef9cbac1ae15126d477729d499b1e21b7df57(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f390316257049d29f8def2da344dcef53c7da8a55d72d9d4f5b0694c7f986f0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c2fd2dca90c48f7c26d38c362a83e491ec03f977b3b107079fa0c317e7a5ac0(
    value: typing.Optional[GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfigDialogflowQuerySource],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e00dd1ee4be88ac923a01fdb3db047be4a4fab3b79450221e2fc240155705d92(
    *,
    documents: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1cbf19b265fdd026252b6106c9fba7b2005b41a91f860310950f4e6d035789f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66a48c0d08d10fd48db4120fbce805a325cfad22360350ffabbc5410efdb8cb6(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f2a674fbdab335e8c8226fd0b1670564aca60383471269d49c265c02256441a(
    value: typing.Optional[GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfigDocumentQuerySource],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8cc6012357dfd3132af13ad6ae40e9c803cf66fe80ba45df7c849f5bc5c05a95(
    *,
    knowledge_bases: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e5437347804d9daaa24b3cffa55159a1f8b3f32772922ddf5434b258ccef13f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4aeb1e667a3c7d42ae731cc463bab66cd47e293a078ccbe0d99a83908b03b4ff(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ff750a7028f0788ab1cf5c66555ca9c3d036871a6dee3c296413a80641ac5a5(
    value: typing.Optional[GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfigKnowledgeBaseQuerySource],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61800be705f3f58af0640115cd800ab55802123cfe4cf9906bf27b2e3821e5f6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8947530bfd0f85fd2bf5332cfb20d3656bc54b9edc4389ce0d350f49ac47b95(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1af5c91de2985ccdf9bd75ddde47f4bcae5146659bb04384d9e35ee145c60e0(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5bd6eeafc453a33f6bd1bd6dfed8870b09a72cd4b94330bc45fb7329b8ddab3a(
    value: typing.Optional[GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d553d2c1d236bb3fc2595320bc3fc213c01d7dd4fcd472734c6c552d075b2c0e(
    *,
    section_types: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2576565488cae4a3313344724ea25480d1618fc65abbacf27d87c5086cd88d1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4cdcc62bc7e4aeab04be6f812faa4f7d4a83f1f1ebd9eb076e42126e7bec14d9(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c1127eca952e7e4895891d09c3e9f8c2c4734abc361f52facd7cddaa4e5890b(
    value: typing.Optional[GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfigSections],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a57996091da5d0b5e55c8507f70a9d450970612ef085c6b9b5281006623249d(
    *,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b041f7f59210c2259eb893933c1eefa9986336aa4d178030e88952d8a1e83504(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a4dab3df91fdd5429624bdc2cec92111722eaadff930690aa769ee793527770(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ac7965b16cd2e873fbb29702ebf024025c3f4cba045c06cdb4c98fcf015826b(
    value: typing.Optional[GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsSuggestionFeature],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cfd7296600756b6d79e7d11d26c6699eb3c5e54efe063e0d15776ec3fd2554f6(
    *,
    no_small_talk: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    only_end_user: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b76608cc1fe7e9496dd958db8e6e4af64a4b37b4de78142399f6ef5f52325eb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb484c809bde4076fec7f1c6764a8cbc01d79ac0b2496b10ac113a26ce1aeddc(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__740b55cbeeab97cc2a7b66b143f8d324f0126296ffb14524811f97b9825afe57(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5b79d1a7c36a8507360ac159b0090eaf1cd6d44317b4ec3a1ee1a639673c8e5(
    value: typing.Optional[GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsSuggestionTriggerSettings],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad6edda364698814cd15efbd2372f270f2777b6d16152724e66b9f3346926b92(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aaac5d869cfbbaa01a5bdb15ffb589b2c1ab959a967d4a60fd39e5974e0ab8d3(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigs, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54708dd6c43fb2e0f4ad8ffd8e054938cd1b687c4388f9cced2600674416a847(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__56ec680add0e949d4a99f52ff63a50f69eb6c0d4d77f7ff801a3519463c3b6bc(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e79db7c9fcfcd6de8ab20a3a6d08438610a39152e68df860c528d04974e7a78(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b06ff4921c9573a3ff7e2db6420fa96104ca3569d573182020a8faabd26a543(
    value: typing.Optional[GoogleDialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f9f2892b20edff1dca277f92722d47590deb0e297c12101121d8a25d6c3fc11(
    *,
    disable_high_latency_features_sync_delivery: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    feature_configs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleDialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigs, typing.Dict[builtins.str, typing.Any]]]]] = None,
    generators: typing.Optional[typing.Sequence[builtins.str]] = None,
    group_suggestion_responses: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76b189e81965539bfd1a9158b08ff82cf1c836159474da7c472880b046c44d0b(
    *,
    conversation_model_config: typing.Optional[typing.Union[GoogleDialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsConversationModelConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    conversation_process_config: typing.Optional[typing.Union[GoogleDialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsConversationProcessConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    disable_agent_query_logging: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enable_conversation_augmented_query: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enable_event_based_suggestion: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enable_query_suggestion_only: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enable_query_suggestion_when_no_answer: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    query_config: typing.Optional[typing.Union[GoogleDialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsQueryConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    suggestion_feature: typing.Optional[typing.Union[GoogleDialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsSuggestionFeature, typing.Dict[builtins.str, typing.Any]]] = None,
    suggestion_trigger_settings: typing.Optional[typing.Union[GoogleDialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsSuggestionTriggerSettings, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a70cd8cce14df41c2ae67797fa8c3bada18f6a61a49b9c72c50cc008e5eab020(
    *,
    baseline_model_version: typing.Optional[builtins.str] = None,
    model: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb1f188a63a7c4556e0c832d561bf70b31b6ec54ec2dc700d5de4ebc47aea67d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5aa5f5db153636ecdb6ae6710f2427062dd11c16400d900e85af13677a343bc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a518d4269e88d5e9d162938d2ba8a3cc2aaae5bc641fdd7592d8502d51e766fc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7fec2f80d3deefb2f438dd71d462cb39fd1a941578e7357553a3b0acf8d257e9(
    value: typing.Optional[GoogleDialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsConversationModelConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc2b5980aff72f1fccc5d348c6a1aec3215d3c0bc8b0420990c0136b99d5d9b8(
    *,
    recent_sentences_count: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5978806849214e383ed99b1b2578e163e18a6fae53e75ee844ce3de748971699(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d26bb6eefe3a16bff5f7c501800a3000302eee870355d0d5dbfee94827d0729a(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42d7a4ec1755f8642207977d625e554d5d08a3217127f934b54fa84f3e633cfd(
    value: typing.Optional[GoogleDialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsConversationProcessConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b76dc7b506fab2dd16624351da5e90e8b077fbbac48eca431bffdceffdec139(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__70ca49a653eb3cd153080884a0869efcdffddb4a94dad8c19590401ce5ae9e9f(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a50299aaab94fcccd50253a658c477dee689a88201f9ee5fb0e617e90d08ddc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__828f27d398832d254aa073e3989faba09ff1d3cca8127b3ebfb1a8c4f5e00243(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f5056a8b495a42c6d38d828bc2c90e33b5b8f59c74542348281cc07b24e3fbb(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68e76c26159ac2786f98b73d3ef67e7472f77bf065ff259d125127bfa21e7ac7(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigs]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff88b0a299435cd9d45969ec1647dfe6d81ffff7f442911c2048af0ea69751d7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ec7e627eba3d1052094535335c48a1630e92ffabd6ae22b2e41eaed0e5099fb(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b37cdb55d51ed589500269ce5dfb684739f05b766df34abd765ac1e1588998e8(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__755bdc5df6669e539e4c5a47b0eef9296d501ad069f5c7d1530293199174620c(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de51c0f1a1f0b69d4016520405d3852fd6cc466c01f025a68a5f85dad2467793(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9bfd9f8102a6c865bd5a2ff5c9b8baee54249cb9502472e3b83cf9bf78f0d26c(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc69088fdde5b2f04ce6235803537b01117e12b6eba5fd49770b6af04910c437(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigs]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe53b16ce30ebc3ab27946159713ac396d8291a09f4d2c069fdfce4434819bc7(
    *,
    confidence_threshold: typing.Optional[jsii.Number] = None,
    context_filter_settings: typing.Optional[typing.Union[GoogleDialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsQueryConfigContextFilterSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    dialogflow_query_source: typing.Optional[typing.Union[GoogleDialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsQueryConfigDialogflowQuerySource, typing.Dict[builtins.str, typing.Any]]] = None,
    max_results: typing.Optional[jsii.Number] = None,
    sections: typing.Optional[typing.Union[GoogleDialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsQueryConfigSections, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__797948b84737b42b251f7431dd152ef2468a93331154eb76d99b7fe34ffe5c36(
    *,
    drop_handoff_messages: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    drop_ivr_messages: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    drop_virtual_agent_messages: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab57542f46c2398b7bea812e9a1a7417ad2c144d677f20bcf939aca417c25386(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb426f39e91a5c49285093fc73efe8947c5f907ea13463df549fa14134af9390(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__211330c9a11aec966a441c0fd4786ce97011485e5b7dc1ee53d15353797c1a84(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50215eb91f6285fe2c7b1e8fd56e899d3564b6222f73e8383409bc2d12b3f973(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__337597f3dbfee6fe3144f7997f091448c4792cbdaf934c0cf96436ae9eda2e1e(
    value: typing.Optional[GoogleDialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsQueryConfigContextFilterSettings],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f66807c71a3b86e7ed5ceb24bae791ce6c6fe44d30ee7cf6881e929e67198774(
    *,
    agent: builtins.str,
    human_agent_side_config: typing.Optional[typing.Union[GoogleDialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsQueryConfigDialogflowQuerySourceHumanAgentSideConfig, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be3d78b18360b64326c0f72d7137a4b9848d471f33b5bd9fe75311f41cc0a798(
    *,
    agent: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8a9e5969320ba5e69a858d6b2809cffefabcc0a1a89fc604f46ef1d5c61e005(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d3a4a85b17f1034462ce0cdc2161ffb6e58e5134ac60c8a933b1ad4de6bad85(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1858c7a070064383b871cd3681a847547c112652a1f2bd0e1a36dafe21844c3f(
    value: typing.Optional[GoogleDialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsQueryConfigDialogflowQuerySourceHumanAgentSideConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dca5c1819853ce3f62ab01c07c38803232e36f9f71666c244920d730cb318051(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc4402da4c3be8a16b41a222e562dc2ffcc6510d9126790a335687f5f1c0d3db(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1429c5e236e9b8cae6ef50008e1b06206a0043cdf5c926b33f52cdbf5232b106(
    value: typing.Optional[GoogleDialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsQueryConfigDialogflowQuerySource],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba843e1258e2f3bfc040c5618dbb77f6e7be87b0c1ae288d3dafddc1b737d039(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f03438e43c554acb38440bd8794fbaaadc760e8a11d3facad9468eec4811e34(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aef125518cb38c8c14d56b7966b56e517492e97ba06897a059db71abcbcfcb38(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__749d696c1f8073fca97a1ce2a73e3d4671a0730de54fedd43509a496e8e6c009(
    value: typing.Optional[GoogleDialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsQueryConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f61fce52b68bddf4ee43fc15002df216d11049f56fb3c13c2ee5c365a9c086b(
    *,
    section_types: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1bd91e129887f90d1b9215cf1fc88e312957949997012ab27a2d764e78485146(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__21450ed341999b8594fecac04f08c70c6473d4299ccabdc09f5123af48b0aaad(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cec7b2e9c7dcf17dbd65aea4f86f0fb5eb3fd43b106e6994197a48794b1eb4ae(
    value: typing.Optional[GoogleDialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsQueryConfigSections],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f23e6efdbfbecd662958c722624645cd17e70dc4092a1f4f4addac4964f9dd59(
    *,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5e82b25ae7f7f2947d877a82a05e670ea6787880d28a8786552e91dcd567138(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5e7924154ba28f5458d9539ac3513537c6620cbdf9b7907545cd8651b7097a8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e97fc7bcd83c449a1b48f8839e6cf39eb6caeaca415706ce6f1b9764cc588353(
    value: typing.Optional[GoogleDialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsSuggestionFeature],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__acb225b0ecde5c8c65d23cac4a5555f5e9353d83db9ead66a477bf4b7a00f30d(
    *,
    no_small_talk: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    only_end_user: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f570ddde9981974e77936bd5deff84aff50b07506989c7969739952fd2f10ede(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ff8bbf4a26e7c13371d21bc149750648366939a79841b8258500b6d06eafcf4(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b59509c0f4230630d5e3064f6797874aa8a92c1c8eb21eb556ed241164bcfbf(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cef008eb8ccd11cb9942a64b316590285094ef18cdb8cc111dd2d7d3264352ef(
    value: typing.Optional[GoogleDialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsSuggestionTriggerSettings],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b049715ea10bf69d77c85fa668cbe15850c86f6d1b44787f6522cc875aab200d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e61d4e58b31f58ec721ed705ebf2d18e70d2647e7b532fb36f4e0ad5a24b3c94(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleDialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigs, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b644c2935eac32ac5058ec8e71adf3dce199cb923acb9cf7b69f935ad3a8561(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45144aa37fe43c8adbb09ce668902b86ce661de11d6d42a8687bf8cb27a7582d(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__01c659c03f6651f62cb14f8c825d09d20376332e8a3200e76e9cd049bb29dab2(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ff8c26fab87265bfef5e659367a9c85527eac17a52891302e45201a6401935e(
    value: typing.Optional[GoogleDialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd78da24e57371d334902f592a6a6f0a06304a41e1ad8844e58c546fc8b0c459(
    *,
    enable_entity_extraction: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enable_sentiment_analysis: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a90ddd1e65bdeb981fa1d4f2e12327d344452549eddfcba566649b59911fd8b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0680663466b45830af6dfaabd3d5c04e8da9455bf0284086b297f9a0ea8a2bd7(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3eb08dced778aebeb7401b79ae9ec0701bf3138e1f4cfabbafc31fbd7a0c84cd(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ed2ab3143ae8668b9babf4d3142e390f39f4e958d305d3499d6ee6e81b0c2c0(
    value: typing.Optional[GoogleDialogflowConversationProfileHumanAgentAssistantConfigMessageAnalysisConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e15ef4ad139058a3f4478c58b2af9f64f35baa6d48cb570ceebe8f22748d52aa(
    *,
    message_format: typing.Optional[builtins.str] = None,
    topic: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__076b4fca6c3548f8ea40bef95e67e33e4f648dc92a959fb454ae4c2b05cf8e58(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e360033a53be3a1eb81cef8a33af893ac4cbb02bd779c3d0cb4cb3ecf120bc1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__874f0d17b5f1d9428cf4eb7eab849f1fe6b9d84583b051b519c40a8c7b648b0e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31e689c80702f7b994028f7c9801935b9f0f6d974ad163a03e0b52b71dd835ef(
    value: typing.Optional[GoogleDialogflowConversationProfileHumanAgentAssistantConfigNotificationConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__729c31f4016fad11f4ae15257f3aa815fbf71407c5d9c53d60ef854362ecad2d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1d552013363bcc41d4303ed6bd46defe6d901d615d17100dbe28c6681dcc202(
    value: typing.Optional[GoogleDialogflowConversationProfileHumanAgentAssistantConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf5f8e4da1d49ef730b303772a9d01e4c07e9da970df73deb90f4ae7f0baf73b(
    *,
    live_person_config: typing.Optional[typing.Union[GoogleDialogflowConversationProfileHumanAgentHandoffConfigLivePersonConfig, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4585ed9a37855bb406defc1c088ecf1aed482ee912c1ac631db64163e546351a(
    *,
    account_number: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5599690d842ffc6a714c71b5c0a56ed01dbe4859316678f9c7256e664aa8859(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f73419a9dd7044a795d93356cddd27e6a97e012b989d1797e1d88861863c0ef(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e1112fde6594c17e454468c48fa08706eddabb87d8e8cb58ccea9f41f58933b(
    value: typing.Optional[GoogleDialogflowConversationProfileHumanAgentHandoffConfigLivePersonConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__191a5ba23c0a0f72335d6a4541cc1c089f13a32d9a259406fa640fb55eb8918a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb7a306c0a3bf5dd70c1b9704b20ef592fa9bc2b98b024bcbff13b300d4c81d5(
    value: typing.Optional[GoogleDialogflowConversationProfileHumanAgentHandoffConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c850200bcbfc0070efbedfd78dd68d40bf7089ef9300b87c7e84273e1967e96(
    *,
    enable_stackdriver_logging: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f77650b17b7d0244a4c35f027cc61a601a7581cb457e2d18163bdbefcb55bc4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b26456a21b813c85a95784880dd99a8d13b5a39ee69906eb369bf6d83ee9b8fb(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c3e594ec2142327134a7bb5b7fe2930348981293774cb2802dc8f24460e67dc(
    value: typing.Optional[GoogleDialogflowConversationProfileLoggingConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eeb83ca68c0da9ef8ba18a61b9f292ae9d09c1845191777f28b6dff25d1ed3cc(
    *,
    message_format: typing.Optional[builtins.str] = None,
    topic: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f16905f489f48bf03b317843ee322fbf4b3df4ded6a15d73fbe628f8b3c3eb1b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__538be31f790819ae360e6fa2a90b9d9bd1afc550f8badd827d98fce0c7fde97b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b225d3acebf81a4293390b2bc2f6aa5b89415ef6ec8c914c74c4d1785b69d0d7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7eeacef626afd43433cc5fac0e5ba1ec80885ca5d3cf8faf22a7f6408a19d650(
    value: typing.Optional[GoogleDialogflowConversationProfileNewMessageEventNotificationConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__984055048436815db863e6b168ccbd31005bbc05efc78d7b2b714636b50c7b11(
    *,
    message_format: typing.Optional[builtins.str] = None,
    topic: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad7164d2531051e8dcb1ec21b9d3e6d9a5be3a0aceccd3a14bd65154dce033ca(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad61f606c7b5575e61ea02c58be47b22241c3b5d33bb653f4688b04ed1abe697(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b83dec2dcb26d76f118884e38dba30eb35fab3ade7de20832542de9d4868a34(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ebe4400c259b7e110c2aadb35bd9ef8785289162ce9d4ebc04f75bf44692903(
    value: typing.Optional[GoogleDialogflowConversationProfileNotificationConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e18660b13cdbd17fe84b031f9afd91474ec3b3788d8d500b899ce1e4fdfae41e(
    *,
    audio_encoding: typing.Optional[builtins.str] = None,
    enable_word_info: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    language_code: typing.Optional[builtins.str] = None,
    model: typing.Optional[builtins.str] = None,
    sample_rate_hertz: typing.Optional[jsii.Number] = None,
    speech_model_variant: typing.Optional[builtins.str] = None,
    use_timeout_based_endpointing: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74232fefc7ed8298dce4e8836872cbbf1f3e44f33379e0f631c3d4f7da759884(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b67bd6c3bac05324e9544c93a0bc021db611750016a8c75509a2b3df5e2f2c0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7598b07a18b163b9bbc275d1357bbc7d52d5f0ba69d26fc63720a7a72d03ea0b(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5406de7f1b2b27a30e1226b53bb69a3320c4f45ed9cb1c980740fd4e51a9bd26(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc76d2d7eeacdf97a25dfdffb1a4277fb4f6337d30a2b1e12c10a35e0ab2b9de(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__936fe14c326b6a049ed3f7eaedf34cbe8e7dcf4ae4d8e6064a4598d3ce412c2f(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c383c89e3ffd61c435428ff87aafbab55ae799886a5038f1c4c142df46ca1003(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a51a76b19f4fde469429ae61ce45efd6c2f943f7f6ee3f6e9cda698ab8b262a(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f39f0246d910577b2e0c5e758f7ebf7308a69be0284de0bb8207480cc8f5b905(
    value: typing.Optional[GoogleDialogflowConversationProfileSttConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1be1e9797a56e5feb96ed9f7022be70fc0fbafce72fff81696f5faa5e361ae3(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30f9eb94fc82edaec88e2c88b7a72c3c75286a952fcd1fb85cad2c295e83b624(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb32e1116cd912923545072defb39c488c23dc1c10cb0cfa8b6cf01f51160bea(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__812c318e18897e55b5ad251ab4dca348af4c2e92e5baebb031220e94f4562e94(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7568b0615df7b65c85dcfea6b5a50798b304b38d86fc111f91bc2583d6fc2278(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc3aafd558b746d25624edc77add2ba9cfe3d2ebe631c8b17cf5a4294149032f(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDialogflowConversationProfileTimeouts]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__850f57bcc02107ebebd9de87acd86c81cc55fc0b8686f7b7220f9c25d73d59d7(
    *,
    effects_profile_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    pitch: typing.Optional[jsii.Number] = None,
    speaking_rate: typing.Optional[jsii.Number] = None,
    voice: typing.Optional[typing.Union[GoogleDialogflowConversationProfileTtsConfigVoice, typing.Dict[builtins.str, typing.Any]]] = None,
    volume_gain_db: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99ad314ddbe107dcf424aae46d8f49c665ebf2ed1cfbdb921d69397f6fb80ee1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf9a16cdd2be634ec51e004933395bb65a84e31199a06b6bd13b4d4f6b683003(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df6200f0cd320ee3e557fb7d95a43192f88c6b335917c1c63c7059d81248345c(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf5df74004cffb71c1831fcd7d732d1df42bbeb22fd50352e6ccfa7b83a12f27(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b467315dcf115ed5dcc23c44b49f03c9a75b092d5a060b8104769895f9918f8(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e46e1ee254c4a2f8ee120a61f70bd27b83b5a3361dd851304feee22dcbd5d806(
    value: typing.Optional[GoogleDialogflowConversationProfileTtsConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6e69c14a10eb6a5d43c711faf722da843e9595213d6341e24699e1f3605aeb7(
    *,
    name: typing.Optional[builtins.str] = None,
    ssml_gender: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b8d805b69d745f6366b73fd63dfc4e40a0be74a49fe7972398c469bd18d4a6b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__937963a22ecbaa10e77d508cf0df6273fc090d44d3b59c219ce13f53aaeff826(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1f9f646d0b27c8317ae834617cf6c53668f2370b8deebde3a481c049fc166a7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ba6a4eb82278005072013ecaf02addd80a5dda208e8262b26adde5712799e76(
    value: typing.Optional[GoogleDialogflowConversationProfileTtsConfigVoice],
) -> None:
    """Type checking stubs"""
    pass
