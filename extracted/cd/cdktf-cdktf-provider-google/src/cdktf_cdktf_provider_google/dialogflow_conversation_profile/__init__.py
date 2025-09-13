r'''
# `google_dialogflow_conversation_profile`

Refer to the Terraform Registry for docs: [`google_dialogflow_conversation_profile`](https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile).
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


class DialogflowConversationProfile(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dialogflowConversationProfile.DialogflowConversationProfile",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile google_dialogflow_conversation_profile}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        display_name: builtins.str,
        location: builtins.str,
        automated_agent_config: typing.Optional[typing.Union["DialogflowConversationProfileAutomatedAgentConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        human_agent_assistant_config: typing.Optional[typing.Union["DialogflowConversationProfileHumanAgentAssistantConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        human_agent_handoff_config: typing.Optional[typing.Union["DialogflowConversationProfileHumanAgentHandoffConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        language_code: typing.Optional[builtins.str] = None,
        logging_config: typing.Optional[typing.Union["DialogflowConversationProfileLoggingConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        new_message_event_notification_config: typing.Optional[typing.Union["DialogflowConversationProfileNewMessageEventNotificationConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        notification_config: typing.Optional[typing.Union["DialogflowConversationProfileNotificationConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        project: typing.Optional[builtins.str] = None,
        security_settings: typing.Optional[builtins.str] = None,
        stt_config: typing.Optional[typing.Union["DialogflowConversationProfileSttConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["DialogflowConversationProfileTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        time_zone: typing.Optional[builtins.str] = None,
        tts_config: typing.Optional[typing.Union["DialogflowConversationProfileTtsConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile google_dialogflow_conversation_profile} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param display_name: Required. Human readable name for this profile. Max length 1024 bytes. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#display_name DialogflowConversationProfile#display_name}
        :param location: desc. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#location DialogflowConversationProfile#location}
        :param automated_agent_config: automated_agent_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#automated_agent_config DialogflowConversationProfile#automated_agent_config}
        :param human_agent_assistant_config: human_agent_assistant_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#human_agent_assistant_config DialogflowConversationProfile#human_agent_assistant_config}
        :param human_agent_handoff_config: human_agent_handoff_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#human_agent_handoff_config DialogflowConversationProfile#human_agent_handoff_config}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#id DialogflowConversationProfile#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param language_code: Language code for the conversation profile. This should be a BCP-47 language tag. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#language_code DialogflowConversationProfile#language_code}
        :param logging_config: logging_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#logging_config DialogflowConversationProfile#logging_config}
        :param new_message_event_notification_config: new_message_event_notification_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#new_message_event_notification_config DialogflowConversationProfile#new_message_event_notification_config}
        :param notification_config: notification_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#notification_config DialogflowConversationProfile#notification_config}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#project DialogflowConversationProfile#project}.
        :param security_settings: Name of the CX SecuritySettings reference for the agent. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#security_settings DialogflowConversationProfile#security_settings}
        :param stt_config: stt_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#stt_config DialogflowConversationProfile#stt_config}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#timeouts DialogflowConversationProfile#timeouts}
        :param time_zone: The time zone of this conversational profile. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#time_zone DialogflowConversationProfile#time_zone}
        :param tts_config: tts_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#tts_config DialogflowConversationProfile#tts_config}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__223237aa40860e4bc01bf819eeeb6119b731d6acb9f4922363b40a491915fb2f)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = DialogflowConversationProfileConfig(
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
        '''Generates CDKTF code for importing a DialogflowConversationProfile resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the DialogflowConversationProfile to import.
        :param import_from_id: The id of the existing DialogflowConversationProfile that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the DialogflowConversationProfile to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__829826b451be440daf6dbdfddcc8414517a9c40a13a0fe6bb966cab15d6d5878)
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
        :param agent: ID of the Dialogflow agent environment to use. Expects the format "projects//locations//agent/environments/". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#agent DialogflowConversationProfile#agent}
        :param session_ttl: Configure lifetime of the Dialogflow session. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#session_ttl DialogflowConversationProfile#session_ttl}
        '''
        value = DialogflowConversationProfileAutomatedAgentConfig(
            agent=agent, session_ttl=session_ttl
        )

        return typing.cast(None, jsii.invoke(self, "putAutomatedAgentConfig", [value]))

    @jsii.member(jsii_name="putHumanAgentAssistantConfig")
    def put_human_agent_assistant_config(
        self,
        *,
        end_user_suggestion_config: typing.Optional[typing.Union["DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        human_agent_suggestion_config: typing.Optional[typing.Union["DialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        message_analysis_config: typing.Optional[typing.Union["DialogflowConversationProfileHumanAgentAssistantConfigMessageAnalysisConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        notification_config: typing.Optional[typing.Union["DialogflowConversationProfileHumanAgentAssistantConfigNotificationConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param end_user_suggestion_config: end_user_suggestion_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#end_user_suggestion_config DialogflowConversationProfile#end_user_suggestion_config}
        :param human_agent_suggestion_config: human_agent_suggestion_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#human_agent_suggestion_config DialogflowConversationProfile#human_agent_suggestion_config}
        :param message_analysis_config: message_analysis_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#message_analysis_config DialogflowConversationProfile#message_analysis_config}
        :param notification_config: notification_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#notification_config DialogflowConversationProfile#notification_config}
        '''
        value = DialogflowConversationProfileHumanAgentAssistantConfig(
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
        live_person_config: typing.Optional[typing.Union["DialogflowConversationProfileHumanAgentHandoffConfigLivePersonConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param live_person_config: live_person_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#live_person_config DialogflowConversationProfile#live_person_config}
        '''
        value = DialogflowConversationProfileHumanAgentHandoffConfig(
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
        :param enable_stackdriver_logging: Whether to log conversation events. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#enable_stackdriver_logging DialogflowConversationProfile#enable_stackdriver_logging}
        '''
        value = DialogflowConversationProfileLoggingConfig(
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
        :param message_format: Format of the message Possible values: ["MESSAGE_FORMAT_UNSPECIFIED", "PROTO", "JSON"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#message_format DialogflowConversationProfile#message_format}
        :param topic: Name of the Pub/Sub topic to publish conversation events. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#topic DialogflowConversationProfile#topic}
        '''
        value = DialogflowConversationProfileNewMessageEventNotificationConfig(
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
        :param message_format: Format of the message Possible values: ["MESSAGE_FORMAT_UNSPECIFIED", "PROTO", "JSON"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#message_format DialogflowConversationProfile#message_format}
        :param topic: Name of the Pub/Sub topic to publish conversation events. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#topic DialogflowConversationProfile#topic}
        '''
        value = DialogflowConversationProfileNotificationConfig(
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
        :param audio_encoding: Audio encoding of the audio content to process. Possible values: ["AUDIO_ENCODING_UNSPECIFIED", "AUDIO_ENCODING_LINEAR_16", "AUDIO_ENCODING_FLAC", "AUDIO_ENCODING_MULAW", "AUDIO_ENCODING_AMR", "AUDIO_ENCODING_AMR_WB", "AUDIO_ENCODING_OGG_OPUS", "AUDIOENCODING_SPEEX_WITH_HEADER_BYTE"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#audio_encoding DialogflowConversationProfile#audio_encoding}
        :param enable_word_info: If true, Dialogflow returns SpeechWordInfo in StreamingRecognitionResult with information about the recognized speech words. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#enable_word_info DialogflowConversationProfile#enable_word_info}
        :param language_code: The language of the supplied audio. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#language_code DialogflowConversationProfile#language_code}
        :param model: Which Speech model to select. Leave this field unspecified to use Agent Speech settings for model selection. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#model DialogflowConversationProfile#model}
        :param sample_rate_hertz: Sample rate (in Hertz) of the audio content sent in the query. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#sample_rate_hertz DialogflowConversationProfile#sample_rate_hertz}
        :param speech_model_variant: The speech model used in speech to text. Possible values: ["SPEECH_MODEL_VARIANT_UNSPECIFIED", "USE_BEST_AVAILABLE", "USE_STANDARD", "USE_ENHANCED"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#speech_model_variant DialogflowConversationProfile#speech_model_variant}
        :param use_timeout_based_endpointing: Use timeout based endpointing, interpreting endpointer sensitivy as seconds of timeout value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#use_timeout_based_endpointing DialogflowConversationProfile#use_timeout_based_endpointing}
        '''
        value = DialogflowConversationProfileSttConfig(
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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#create DialogflowConversationProfile#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#delete DialogflowConversationProfile#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#update DialogflowConversationProfile#update}.
        '''
        value = DialogflowConversationProfileTimeouts(
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
        voice: typing.Optional[typing.Union["DialogflowConversationProfileTtsConfigVoice", typing.Dict[builtins.str, typing.Any]]] = None,
        volume_gain_db: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param effects_profile_id: An identifier which selects 'audio effects' profiles that are applied on (post synthesized) text to speech. Effects are applied on top of each other in the order they are given. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#effects_profile_id DialogflowConversationProfile#effects_profile_id}
        :param pitch: Speaking pitch, in the range [-20.0, 20.0]. 20 means increase 20 semitones from the original pitch. -20 means decrease 20 semitones from the original pitch. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#pitch DialogflowConversationProfile#pitch}
        :param speaking_rate: Speaking rate/speed, in the range [0.25, 4.0]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#speaking_rate DialogflowConversationProfile#speaking_rate}
        :param voice: voice block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#voice DialogflowConversationProfile#voice}
        :param volume_gain_db: Volume gain (in dB) of the normal native volume supported by the specific voice. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#volume_gain_db DialogflowConversationProfile#volume_gain_db}
        '''
        value = DialogflowConversationProfileTtsConfig(
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
    ) -> "DialogflowConversationProfileAutomatedAgentConfigOutputReference":
        return typing.cast("DialogflowConversationProfileAutomatedAgentConfigOutputReference", jsii.get(self, "automatedAgentConfig"))

    @builtins.property
    @jsii.member(jsii_name="humanAgentAssistantConfig")
    def human_agent_assistant_config(
        self,
    ) -> "DialogflowConversationProfileHumanAgentAssistantConfigOutputReference":
        return typing.cast("DialogflowConversationProfileHumanAgentAssistantConfigOutputReference", jsii.get(self, "humanAgentAssistantConfig"))

    @builtins.property
    @jsii.member(jsii_name="humanAgentHandoffConfig")
    def human_agent_handoff_config(
        self,
    ) -> "DialogflowConversationProfileHumanAgentHandoffConfigOutputReference":
        return typing.cast("DialogflowConversationProfileHumanAgentHandoffConfigOutputReference", jsii.get(self, "humanAgentHandoffConfig"))

    @builtins.property
    @jsii.member(jsii_name="loggingConfig")
    def logging_config(
        self,
    ) -> "DialogflowConversationProfileLoggingConfigOutputReference":
        return typing.cast("DialogflowConversationProfileLoggingConfigOutputReference", jsii.get(self, "loggingConfig"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="newMessageEventNotificationConfig")
    def new_message_event_notification_config(
        self,
    ) -> "DialogflowConversationProfileNewMessageEventNotificationConfigOutputReference":
        return typing.cast("DialogflowConversationProfileNewMessageEventNotificationConfigOutputReference", jsii.get(self, "newMessageEventNotificationConfig"))

    @builtins.property
    @jsii.member(jsii_name="notificationConfig")
    def notification_config(
        self,
    ) -> "DialogflowConversationProfileNotificationConfigOutputReference":
        return typing.cast("DialogflowConversationProfileNotificationConfigOutputReference", jsii.get(self, "notificationConfig"))

    @builtins.property
    @jsii.member(jsii_name="sttConfig")
    def stt_config(self) -> "DialogflowConversationProfileSttConfigOutputReference":
        return typing.cast("DialogflowConversationProfileSttConfigOutputReference", jsii.get(self, "sttConfig"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "DialogflowConversationProfileTimeoutsOutputReference":
        return typing.cast("DialogflowConversationProfileTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="ttsConfig")
    def tts_config(self) -> "DialogflowConversationProfileTtsConfigOutputReference":
        return typing.cast("DialogflowConversationProfileTtsConfigOutputReference", jsii.get(self, "ttsConfig"))

    @builtins.property
    @jsii.member(jsii_name="automatedAgentConfigInput")
    def automated_agent_config_input(
        self,
    ) -> typing.Optional["DialogflowConversationProfileAutomatedAgentConfig"]:
        return typing.cast(typing.Optional["DialogflowConversationProfileAutomatedAgentConfig"], jsii.get(self, "automatedAgentConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="displayNameInput")
    def display_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "displayNameInput"))

    @builtins.property
    @jsii.member(jsii_name="humanAgentAssistantConfigInput")
    def human_agent_assistant_config_input(
        self,
    ) -> typing.Optional["DialogflowConversationProfileHumanAgentAssistantConfig"]:
        return typing.cast(typing.Optional["DialogflowConversationProfileHumanAgentAssistantConfig"], jsii.get(self, "humanAgentAssistantConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="humanAgentHandoffConfigInput")
    def human_agent_handoff_config_input(
        self,
    ) -> typing.Optional["DialogflowConversationProfileHumanAgentHandoffConfig"]:
        return typing.cast(typing.Optional["DialogflowConversationProfileHumanAgentHandoffConfig"], jsii.get(self, "humanAgentHandoffConfigInput"))

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
    ) -> typing.Optional["DialogflowConversationProfileLoggingConfig"]:
        return typing.cast(typing.Optional["DialogflowConversationProfileLoggingConfig"], jsii.get(self, "loggingConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="newMessageEventNotificationConfigInput")
    def new_message_event_notification_config_input(
        self,
    ) -> typing.Optional["DialogflowConversationProfileNewMessageEventNotificationConfig"]:
        return typing.cast(typing.Optional["DialogflowConversationProfileNewMessageEventNotificationConfig"], jsii.get(self, "newMessageEventNotificationConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="notificationConfigInput")
    def notification_config_input(
        self,
    ) -> typing.Optional["DialogflowConversationProfileNotificationConfig"]:
        return typing.cast(typing.Optional["DialogflowConversationProfileNotificationConfig"], jsii.get(self, "notificationConfigInput"))

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
    ) -> typing.Optional["DialogflowConversationProfileSttConfig"]:
        return typing.cast(typing.Optional["DialogflowConversationProfileSttConfig"], jsii.get(self, "sttConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "DialogflowConversationProfileTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "DialogflowConversationProfileTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="timeZoneInput")
    def time_zone_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "timeZoneInput"))

    @builtins.property
    @jsii.member(jsii_name="ttsConfigInput")
    def tts_config_input(
        self,
    ) -> typing.Optional["DialogflowConversationProfileTtsConfig"]:
        return typing.cast(typing.Optional["DialogflowConversationProfileTtsConfig"], jsii.get(self, "ttsConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="displayName")
    def display_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "displayName"))

    @display_name.setter
    def display_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__231c8c2581c6656aeaf27596a7c073becf40790f261465dea6ae2d8887c61193)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "displayName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf950dd7a6ebfaaed9ef1b51eb97bbc4851e14f5a1577adadb9cb65a92e49bd5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="languageCode")
    def language_code(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "languageCode"))

    @language_code.setter
    def language_code(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ecc85f8a166a5730e3f737000bae80af676478719e308497d9d523c5f33df173)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "languageCode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ce4ef4befcc5b46c3d9c97f025388f82bcf694f54a4bd1317ab404623149773)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dfd8c6e7045c51a7465ea24c44481e56920e340962b7714a387146da6447eff4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="securitySettings")
    def security_settings(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "securitySettings"))

    @security_settings.setter
    def security_settings(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2dc80c8c8fbfff24f94eab02aee8572b179f93049328a50233275ecb6bd45dc7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "securitySettings", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="timeZone")
    def time_zone(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "timeZone"))

    @time_zone.setter
    def time_zone(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a92ce0f9506d2410bf7fb4dfb6bc93ea18b3966582580609ce748ec0b9bc771a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timeZone", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dialogflowConversationProfile.DialogflowConversationProfileAutomatedAgentConfig",
    jsii_struct_bases=[],
    name_mapping={"agent": "agent", "session_ttl": "sessionTtl"},
)
class DialogflowConversationProfileAutomatedAgentConfig:
    def __init__(
        self,
        *,
        agent: builtins.str,
        session_ttl: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param agent: ID of the Dialogflow agent environment to use. Expects the format "projects//locations//agent/environments/". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#agent DialogflowConversationProfile#agent}
        :param session_ttl: Configure lifetime of the Dialogflow session. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#session_ttl DialogflowConversationProfile#session_ttl}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b401d5d43fb62253f6cf2a61b8e8af9c09d816a07383ac16dd592746897e11c5)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#agent DialogflowConversationProfile#agent}
        '''
        result = self._values.get("agent")
        assert result is not None, "Required property 'agent' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def session_ttl(self) -> typing.Optional[builtins.str]:
        '''Configure lifetime of the Dialogflow session.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#session_ttl DialogflowConversationProfile#session_ttl}
        '''
        result = self._values.get("session_ttl")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DialogflowConversationProfileAutomatedAgentConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DialogflowConversationProfileAutomatedAgentConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dialogflowConversationProfile.DialogflowConversationProfileAutomatedAgentConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a4b9c114ea0ae8c06078992f2401361071bf4ed28b8e2d69d735f8af313cd004)
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
            type_hints = typing.get_type_hints(_typecheckingstub__98c1f000e3d5cf837c00974b3e548feb7b899475ace8db143f685e7bdafe2510)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "agent", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sessionTtl")
    def session_ttl(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sessionTtl"))

    @session_ttl.setter
    def session_ttl(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e48f52dd1272472d6bffd088480f0f4a7db5466782e89602607445bada470767)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sessionTtl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DialogflowConversationProfileAutomatedAgentConfig]:
        return typing.cast(typing.Optional[DialogflowConversationProfileAutomatedAgentConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DialogflowConversationProfileAutomatedAgentConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e868f5cce1dbb6e1c603e11df42a0b7c07402fa5d8bde08a650aeadb7b00fd1e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dialogflowConversationProfile.DialogflowConversationProfileConfig",
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
class DialogflowConversationProfileConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        automated_agent_config: typing.Optional[typing.Union[DialogflowConversationProfileAutomatedAgentConfig, typing.Dict[builtins.str, typing.Any]]] = None,
        human_agent_assistant_config: typing.Optional[typing.Union["DialogflowConversationProfileHumanAgentAssistantConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        human_agent_handoff_config: typing.Optional[typing.Union["DialogflowConversationProfileHumanAgentHandoffConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        language_code: typing.Optional[builtins.str] = None,
        logging_config: typing.Optional[typing.Union["DialogflowConversationProfileLoggingConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        new_message_event_notification_config: typing.Optional[typing.Union["DialogflowConversationProfileNewMessageEventNotificationConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        notification_config: typing.Optional[typing.Union["DialogflowConversationProfileNotificationConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        project: typing.Optional[builtins.str] = None,
        security_settings: typing.Optional[builtins.str] = None,
        stt_config: typing.Optional[typing.Union["DialogflowConversationProfileSttConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["DialogflowConversationProfileTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        time_zone: typing.Optional[builtins.str] = None,
        tts_config: typing.Optional[typing.Union["DialogflowConversationProfileTtsConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param display_name: Required. Human readable name for this profile. Max length 1024 bytes. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#display_name DialogflowConversationProfile#display_name}
        :param location: desc. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#location DialogflowConversationProfile#location}
        :param automated_agent_config: automated_agent_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#automated_agent_config DialogflowConversationProfile#automated_agent_config}
        :param human_agent_assistant_config: human_agent_assistant_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#human_agent_assistant_config DialogflowConversationProfile#human_agent_assistant_config}
        :param human_agent_handoff_config: human_agent_handoff_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#human_agent_handoff_config DialogflowConversationProfile#human_agent_handoff_config}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#id DialogflowConversationProfile#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param language_code: Language code for the conversation profile. This should be a BCP-47 language tag. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#language_code DialogflowConversationProfile#language_code}
        :param logging_config: logging_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#logging_config DialogflowConversationProfile#logging_config}
        :param new_message_event_notification_config: new_message_event_notification_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#new_message_event_notification_config DialogflowConversationProfile#new_message_event_notification_config}
        :param notification_config: notification_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#notification_config DialogflowConversationProfile#notification_config}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#project DialogflowConversationProfile#project}.
        :param security_settings: Name of the CX SecuritySettings reference for the agent. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#security_settings DialogflowConversationProfile#security_settings}
        :param stt_config: stt_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#stt_config DialogflowConversationProfile#stt_config}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#timeouts DialogflowConversationProfile#timeouts}
        :param time_zone: The time zone of this conversational profile. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#time_zone DialogflowConversationProfile#time_zone}
        :param tts_config: tts_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#tts_config DialogflowConversationProfile#tts_config}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(automated_agent_config, dict):
            automated_agent_config = DialogflowConversationProfileAutomatedAgentConfig(**automated_agent_config)
        if isinstance(human_agent_assistant_config, dict):
            human_agent_assistant_config = DialogflowConversationProfileHumanAgentAssistantConfig(**human_agent_assistant_config)
        if isinstance(human_agent_handoff_config, dict):
            human_agent_handoff_config = DialogflowConversationProfileHumanAgentHandoffConfig(**human_agent_handoff_config)
        if isinstance(logging_config, dict):
            logging_config = DialogflowConversationProfileLoggingConfig(**logging_config)
        if isinstance(new_message_event_notification_config, dict):
            new_message_event_notification_config = DialogflowConversationProfileNewMessageEventNotificationConfig(**new_message_event_notification_config)
        if isinstance(notification_config, dict):
            notification_config = DialogflowConversationProfileNotificationConfig(**notification_config)
        if isinstance(stt_config, dict):
            stt_config = DialogflowConversationProfileSttConfig(**stt_config)
        if isinstance(timeouts, dict):
            timeouts = DialogflowConversationProfileTimeouts(**timeouts)
        if isinstance(tts_config, dict):
            tts_config = DialogflowConversationProfileTtsConfig(**tts_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__641e7434d0d7fac6924947f95509745270d2f8bfb3d0ac86dffed129065b552b)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#display_name DialogflowConversationProfile#display_name}
        '''
        result = self._values.get("display_name")
        assert result is not None, "Required property 'display_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def location(self) -> builtins.str:
        '''desc.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#location DialogflowConversationProfile#location}
        '''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def automated_agent_config(
        self,
    ) -> typing.Optional[DialogflowConversationProfileAutomatedAgentConfig]:
        '''automated_agent_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#automated_agent_config DialogflowConversationProfile#automated_agent_config}
        '''
        result = self._values.get("automated_agent_config")
        return typing.cast(typing.Optional[DialogflowConversationProfileAutomatedAgentConfig], result)

    @builtins.property
    def human_agent_assistant_config(
        self,
    ) -> typing.Optional["DialogflowConversationProfileHumanAgentAssistantConfig"]:
        '''human_agent_assistant_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#human_agent_assistant_config DialogflowConversationProfile#human_agent_assistant_config}
        '''
        result = self._values.get("human_agent_assistant_config")
        return typing.cast(typing.Optional["DialogflowConversationProfileHumanAgentAssistantConfig"], result)

    @builtins.property
    def human_agent_handoff_config(
        self,
    ) -> typing.Optional["DialogflowConversationProfileHumanAgentHandoffConfig"]:
        '''human_agent_handoff_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#human_agent_handoff_config DialogflowConversationProfile#human_agent_handoff_config}
        '''
        result = self._values.get("human_agent_handoff_config")
        return typing.cast(typing.Optional["DialogflowConversationProfileHumanAgentHandoffConfig"], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#id DialogflowConversationProfile#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def language_code(self) -> typing.Optional[builtins.str]:
        '''Language code for the conversation profile. This should be a BCP-47 language tag.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#language_code DialogflowConversationProfile#language_code}
        '''
        result = self._values.get("language_code")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def logging_config(
        self,
    ) -> typing.Optional["DialogflowConversationProfileLoggingConfig"]:
        '''logging_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#logging_config DialogflowConversationProfile#logging_config}
        '''
        result = self._values.get("logging_config")
        return typing.cast(typing.Optional["DialogflowConversationProfileLoggingConfig"], result)

    @builtins.property
    def new_message_event_notification_config(
        self,
    ) -> typing.Optional["DialogflowConversationProfileNewMessageEventNotificationConfig"]:
        '''new_message_event_notification_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#new_message_event_notification_config DialogflowConversationProfile#new_message_event_notification_config}
        '''
        result = self._values.get("new_message_event_notification_config")
        return typing.cast(typing.Optional["DialogflowConversationProfileNewMessageEventNotificationConfig"], result)

    @builtins.property
    def notification_config(
        self,
    ) -> typing.Optional["DialogflowConversationProfileNotificationConfig"]:
        '''notification_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#notification_config DialogflowConversationProfile#notification_config}
        '''
        result = self._values.get("notification_config")
        return typing.cast(typing.Optional["DialogflowConversationProfileNotificationConfig"], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#project DialogflowConversationProfile#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def security_settings(self) -> typing.Optional[builtins.str]:
        '''Name of the CX SecuritySettings reference for the agent.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#security_settings DialogflowConversationProfile#security_settings}
        '''
        result = self._values.get("security_settings")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def stt_config(self) -> typing.Optional["DialogflowConversationProfileSttConfig"]:
        '''stt_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#stt_config DialogflowConversationProfile#stt_config}
        '''
        result = self._values.get("stt_config")
        return typing.cast(typing.Optional["DialogflowConversationProfileSttConfig"], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["DialogflowConversationProfileTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#timeouts DialogflowConversationProfile#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["DialogflowConversationProfileTimeouts"], result)

    @builtins.property
    def time_zone(self) -> typing.Optional[builtins.str]:
        '''The time zone of this conversational profile.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#time_zone DialogflowConversationProfile#time_zone}
        '''
        result = self._values.get("time_zone")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tts_config(self) -> typing.Optional["DialogflowConversationProfileTtsConfig"]:
        '''tts_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#tts_config DialogflowConversationProfile#tts_config}
        '''
        result = self._values.get("tts_config")
        return typing.cast(typing.Optional["DialogflowConversationProfileTtsConfig"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DialogflowConversationProfileConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dialogflowConversationProfile.DialogflowConversationProfileHumanAgentAssistantConfig",
    jsii_struct_bases=[],
    name_mapping={
        "end_user_suggestion_config": "endUserSuggestionConfig",
        "human_agent_suggestion_config": "humanAgentSuggestionConfig",
        "message_analysis_config": "messageAnalysisConfig",
        "notification_config": "notificationConfig",
    },
)
class DialogflowConversationProfileHumanAgentAssistantConfig:
    def __init__(
        self,
        *,
        end_user_suggestion_config: typing.Optional[typing.Union["DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        human_agent_suggestion_config: typing.Optional[typing.Union["DialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        message_analysis_config: typing.Optional[typing.Union["DialogflowConversationProfileHumanAgentAssistantConfigMessageAnalysisConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        notification_config: typing.Optional[typing.Union["DialogflowConversationProfileHumanAgentAssistantConfigNotificationConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param end_user_suggestion_config: end_user_suggestion_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#end_user_suggestion_config DialogflowConversationProfile#end_user_suggestion_config}
        :param human_agent_suggestion_config: human_agent_suggestion_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#human_agent_suggestion_config DialogflowConversationProfile#human_agent_suggestion_config}
        :param message_analysis_config: message_analysis_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#message_analysis_config DialogflowConversationProfile#message_analysis_config}
        :param notification_config: notification_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#notification_config DialogflowConversationProfile#notification_config}
        '''
        if isinstance(end_user_suggestion_config, dict):
            end_user_suggestion_config = DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfig(**end_user_suggestion_config)
        if isinstance(human_agent_suggestion_config, dict):
            human_agent_suggestion_config = DialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfig(**human_agent_suggestion_config)
        if isinstance(message_analysis_config, dict):
            message_analysis_config = DialogflowConversationProfileHumanAgentAssistantConfigMessageAnalysisConfig(**message_analysis_config)
        if isinstance(notification_config, dict):
            notification_config = DialogflowConversationProfileHumanAgentAssistantConfigNotificationConfig(**notification_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a56695d36a1f96dc3ed7a6446e6ddd0262124129f39daabf0ccf62c318af94b4)
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
    ) -> typing.Optional["DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfig"]:
        '''end_user_suggestion_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#end_user_suggestion_config DialogflowConversationProfile#end_user_suggestion_config}
        '''
        result = self._values.get("end_user_suggestion_config")
        return typing.cast(typing.Optional["DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfig"], result)

    @builtins.property
    def human_agent_suggestion_config(
        self,
    ) -> typing.Optional["DialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfig"]:
        '''human_agent_suggestion_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#human_agent_suggestion_config DialogflowConversationProfile#human_agent_suggestion_config}
        '''
        result = self._values.get("human_agent_suggestion_config")
        return typing.cast(typing.Optional["DialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfig"], result)

    @builtins.property
    def message_analysis_config(
        self,
    ) -> typing.Optional["DialogflowConversationProfileHumanAgentAssistantConfigMessageAnalysisConfig"]:
        '''message_analysis_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#message_analysis_config DialogflowConversationProfile#message_analysis_config}
        '''
        result = self._values.get("message_analysis_config")
        return typing.cast(typing.Optional["DialogflowConversationProfileHumanAgentAssistantConfigMessageAnalysisConfig"], result)

    @builtins.property
    def notification_config(
        self,
    ) -> typing.Optional["DialogflowConversationProfileHumanAgentAssistantConfigNotificationConfig"]:
        '''notification_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#notification_config DialogflowConversationProfile#notification_config}
        '''
        result = self._values.get("notification_config")
        return typing.cast(typing.Optional["DialogflowConversationProfileHumanAgentAssistantConfigNotificationConfig"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DialogflowConversationProfileHumanAgentAssistantConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dialogflowConversationProfile.DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfig",
    jsii_struct_bases=[],
    name_mapping={
        "disable_high_latency_features_sync_delivery": "disableHighLatencyFeaturesSyncDelivery",
        "feature_configs": "featureConfigs",
        "generators": "generators",
        "group_suggestion_responses": "groupSuggestionResponses",
    },
)
class DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfig:
    def __init__(
        self,
        *,
        disable_high_latency_features_sync_delivery: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        feature_configs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigs", typing.Dict[builtins.str, typing.Any]]]]] = None,
        generators: typing.Optional[typing.Sequence[builtins.str]] = None,
        group_suggestion_responses: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param disable_high_latency_features_sync_delivery: When disableHighLatencyFeaturesSyncDelivery is true and using the AnalyzeContent API, we will not deliver the responses from high latency features in the API response. The humanAgentAssistantConfig.notification_config must be configured and enableEventBasedSuggestion must be set to true to receive the responses from high latency features in Pub/Sub. High latency feature(s): KNOWLEDGE_ASSIST Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#disable_high_latency_features_sync_delivery DialogflowConversationProfile#disable_high_latency_features_sync_delivery}
        :param feature_configs: feature_configs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#feature_configs DialogflowConversationProfile#feature_configs}
        :param generators: List of various generator resource names used in the conversation profile. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#generators DialogflowConversationProfile#generators}
        :param group_suggestion_responses: If groupSuggestionResponses is false, and there are multiple featureConfigs in event based suggestion or StreamingAnalyzeContent, we will try to deliver suggestions to customers as soon as we get new suggestion. Different type of suggestions based on the same context will be in separate Pub/Sub event or StreamingAnalyzeContentResponse. If groupSuggestionResponses set to true. All the suggestions to the same participant based on the same context will be grouped into a single Pub/Sub event or StreamingAnalyzeContentResponse. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#group_suggestion_responses DialogflowConversationProfile#group_suggestion_responses}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b1bed750542ab379233e26e631ee8a85400019330c95b4de92f47ceefe9a3cde)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#disable_high_latency_features_sync_delivery DialogflowConversationProfile#disable_high_latency_features_sync_delivery}
        '''
        result = self._values.get("disable_high_latency_features_sync_delivery")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def feature_configs(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigs"]]]:
        '''feature_configs block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#feature_configs DialogflowConversationProfile#feature_configs}
        '''
        result = self._values.get("feature_configs")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigs"]]], result)

    @builtins.property
    def generators(self) -> typing.Optional[typing.List[builtins.str]]:
        '''List of various generator resource names used in the conversation profile.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#generators DialogflowConversationProfile#generators}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#group_suggestion_responses DialogflowConversationProfile#group_suggestion_responses}
        '''
        result = self._values.get("group_suggestion_responses")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dialogflowConversationProfile.DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigs",
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
class DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigs:
    def __init__(
        self,
        *,
        conversation_model_config: typing.Optional[typing.Union["DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsConversationModelConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        conversation_process_config: typing.Optional[typing.Union["DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsConversationProcessConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        disable_agent_query_logging: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_conversation_augmented_query: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_event_based_suggestion: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_query_suggestion_only: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_query_suggestion_when_no_answer: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        query_config: typing.Optional[typing.Union["DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        suggestion_feature: typing.Optional[typing.Union["DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsSuggestionFeature", typing.Dict[builtins.str, typing.Any]]] = None,
        suggestion_trigger_settings: typing.Optional[typing.Union["DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsSuggestionTriggerSettings", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param conversation_model_config: conversation_model_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#conversation_model_config DialogflowConversationProfile#conversation_model_config}
        :param conversation_process_config: conversation_process_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#conversation_process_config DialogflowConversationProfile#conversation_process_config}
        :param disable_agent_query_logging: Disable the logging of search queries sent by human agents. It can prevent those queries from being stored at answer records. This feature is only supported for types: KNOWLEDGE_SEARCH. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#disable_agent_query_logging DialogflowConversationProfile#disable_agent_query_logging}
        :param enable_conversation_augmented_query: Enable including conversation context during query answer generation. This feature is only supported for types: KNOWLEDGE_SEARCH. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#enable_conversation_augmented_query DialogflowConversationProfile#enable_conversation_augmented_query}
        :param enable_event_based_suggestion: Automatically iterates all participants and tries to compile suggestions. This feature is only supported for types: ARTICLE_SUGGESTION, FAQ, DIALOGFLOW_ASSIST, KNOWLEDGE_ASSIST. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#enable_event_based_suggestion DialogflowConversationProfile#enable_event_based_suggestion}
        :param enable_query_suggestion_only: Enable query suggestion only. This feature is only supported for types: KNOWLEDGE_ASSIST. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#enable_query_suggestion_only DialogflowConversationProfile#enable_query_suggestion_only}
        :param enable_query_suggestion_when_no_answer: Enable query suggestion even if we can't find its answer. By default, queries are suggested only if we find its answer. This feature is only supported for types: KNOWLEDGE_ASSIST. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#enable_query_suggestion_when_no_answer DialogflowConversationProfile#enable_query_suggestion_when_no_answer}
        :param query_config: query_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#query_config DialogflowConversationProfile#query_config}
        :param suggestion_feature: suggestion_feature block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#suggestion_feature DialogflowConversationProfile#suggestion_feature}
        :param suggestion_trigger_settings: suggestion_trigger_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#suggestion_trigger_settings DialogflowConversationProfile#suggestion_trigger_settings}
        '''
        if isinstance(conversation_model_config, dict):
            conversation_model_config = DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsConversationModelConfig(**conversation_model_config)
        if isinstance(conversation_process_config, dict):
            conversation_process_config = DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsConversationProcessConfig(**conversation_process_config)
        if isinstance(query_config, dict):
            query_config = DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfig(**query_config)
        if isinstance(suggestion_feature, dict):
            suggestion_feature = DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsSuggestionFeature(**suggestion_feature)
        if isinstance(suggestion_trigger_settings, dict):
            suggestion_trigger_settings = DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsSuggestionTriggerSettings(**suggestion_trigger_settings)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__981a92704043d3d69d9c7d3d1d86f6ebd44c533facfaedb9b60a308b94131018)
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
    ) -> typing.Optional["DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsConversationModelConfig"]:
        '''conversation_model_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#conversation_model_config DialogflowConversationProfile#conversation_model_config}
        '''
        result = self._values.get("conversation_model_config")
        return typing.cast(typing.Optional["DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsConversationModelConfig"], result)

    @builtins.property
    def conversation_process_config(
        self,
    ) -> typing.Optional["DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsConversationProcessConfig"]:
        '''conversation_process_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#conversation_process_config DialogflowConversationProfile#conversation_process_config}
        '''
        result = self._values.get("conversation_process_config")
        return typing.cast(typing.Optional["DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsConversationProcessConfig"], result)

    @builtins.property
    def disable_agent_query_logging(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Disable the logging of search queries sent by human agents.

        It can prevent those queries from being stored at answer records.
        This feature is only supported for types: KNOWLEDGE_SEARCH.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#disable_agent_query_logging DialogflowConversationProfile#disable_agent_query_logging}
        '''
        result = self._values.get("disable_agent_query_logging")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def enable_conversation_augmented_query(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Enable including conversation context during query answer generation. This feature is only supported for types: KNOWLEDGE_SEARCH.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#enable_conversation_augmented_query DialogflowConversationProfile#enable_conversation_augmented_query}
        '''
        result = self._values.get("enable_conversation_augmented_query")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def enable_event_based_suggestion(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Automatically iterates all participants and tries to compile suggestions. This feature is only supported for types: ARTICLE_SUGGESTION, FAQ, DIALOGFLOW_ASSIST, KNOWLEDGE_ASSIST.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#enable_event_based_suggestion DialogflowConversationProfile#enable_event_based_suggestion}
        '''
        result = self._values.get("enable_event_based_suggestion")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def enable_query_suggestion_only(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Enable query suggestion only. This feature is only supported for types: KNOWLEDGE_ASSIST.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#enable_query_suggestion_only DialogflowConversationProfile#enable_query_suggestion_only}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#enable_query_suggestion_when_no_answer DialogflowConversationProfile#enable_query_suggestion_when_no_answer}
        '''
        result = self._values.get("enable_query_suggestion_when_no_answer")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def query_config(
        self,
    ) -> typing.Optional["DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfig"]:
        '''query_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#query_config DialogflowConversationProfile#query_config}
        '''
        result = self._values.get("query_config")
        return typing.cast(typing.Optional["DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfig"], result)

    @builtins.property
    def suggestion_feature(
        self,
    ) -> typing.Optional["DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsSuggestionFeature"]:
        '''suggestion_feature block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#suggestion_feature DialogflowConversationProfile#suggestion_feature}
        '''
        result = self._values.get("suggestion_feature")
        return typing.cast(typing.Optional["DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsSuggestionFeature"], result)

    @builtins.property
    def suggestion_trigger_settings(
        self,
    ) -> typing.Optional["DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsSuggestionTriggerSettings"]:
        '''suggestion_trigger_settings block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#suggestion_trigger_settings DialogflowConversationProfile#suggestion_trigger_settings}
        '''
        result = self._values.get("suggestion_trigger_settings")
        return typing.cast(typing.Optional["DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsSuggestionTriggerSettings"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigs(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dialogflowConversationProfile.DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsConversationModelConfig",
    jsii_struct_bases=[],
    name_mapping={"baseline_model_version": "baselineModelVersion", "model": "model"},
)
class DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsConversationModelConfig:
    def __init__(
        self,
        *,
        baseline_model_version: typing.Optional[builtins.str] = None,
        model: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param baseline_model_version: Version of current baseline model. It will be ignored if model is set. Valid versions are: Article Suggestion baseline model: - 0.9 - 1.0 (default) Summarization baseline model: - 1.0 Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#baseline_model_version DialogflowConversationProfile#baseline_model_version}
        :param model: Conversation model resource name. Format: projects//conversationModels/. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#model DialogflowConversationProfile#model}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a6c77ce9c3e63c24097c9b3991b029d4e6e98573c505cdada7b67a276f6f48ed)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#baseline_model_version DialogflowConversationProfile#baseline_model_version}
        '''
        result = self._values.get("baseline_model_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def model(self) -> typing.Optional[builtins.str]:
        '''Conversation model resource name. Format: projects//conversationModels/.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#model DialogflowConversationProfile#model}
        '''
        result = self._values.get("model")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsConversationModelConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsConversationModelConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dialogflowConversationProfile.DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsConversationModelConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e0339ac1afe4aedd03fb933356e48183cb79c8d5989c1115f3e8b265a0605b1a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bb0087abea8719603870187ffdf26b812736f33273950f82c0927616dd8c6910)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "baselineModelVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="model")
    def model(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "model"))

    @model.setter
    def model(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__973bdd5ff0fdf45fdc2eec00cd7e1512518ea2646fcd136ab53a2f9bb6bc03d5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "model", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsConversationModelConfig]:
        return typing.cast(typing.Optional[DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsConversationModelConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsConversationModelConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__78b47f588128b392a652a7d6d54d52eceb32afe27cdb64c775a3bc45ffac2889)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dialogflowConversationProfile.DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsConversationProcessConfig",
    jsii_struct_bases=[],
    name_mapping={"recent_sentences_count": "recentSentencesCount"},
)
class DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsConversationProcessConfig:
    def __init__(
        self,
        *,
        recent_sentences_count: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param recent_sentences_count: Number of recent non-small-talk sentences to use as context for article and FAQ suggestion. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#recent_sentences_count DialogflowConversationProfile#recent_sentences_count}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__56665caf4ef4b602d60be5b4093727fd4bf00a2e39e89ec03fde803a02ad2b33)
            check_type(argname="argument recent_sentences_count", value=recent_sentences_count, expected_type=type_hints["recent_sentences_count"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if recent_sentences_count is not None:
            self._values["recent_sentences_count"] = recent_sentences_count

    @builtins.property
    def recent_sentences_count(self) -> typing.Optional[jsii.Number]:
        '''Number of recent non-small-talk sentences to use as context for article and FAQ suggestion.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#recent_sentences_count DialogflowConversationProfile#recent_sentences_count}
        '''
        result = self._values.get("recent_sentences_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsConversationProcessConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsConversationProcessConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dialogflowConversationProfile.DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsConversationProcessConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__71905e4a1cfe682137b3ea03c9ac3c42c8fc0e30490a7bbc84b95c06cf83c6c7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e9175510abc9413fccab61f584ae34b1fe5ed5ab65654882cb847764788f9f96)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "recentSentencesCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsConversationProcessConfig]:
        return typing.cast(typing.Optional[DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsConversationProcessConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsConversationProcessConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf976d6d9183540a378509aedefd6b896c73dca22378931afa7a8f1ec4b55645)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dialogflowConversationProfile.DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0eede5fbb11346e83cd0a114f8708ba2a9aa2b83cb9db5af3a0239ad5d6f79ea)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__368e328631977cc44968b30dc9f5e4e14fbb1985c05dc939bcaffbbadb3f94b9)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e245e2b6bbc7b77cadf7b26a43162e7a6abb3904732ee86eff84b49bd0102c4a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__af3f224bf409080cfcf32237585def9f9493e7acb5c9feff60075eeb23a3f700)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7af7303ef1f08beebc954cf45f1109da29fff543e3c8a24dba696ce221557e53)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigs]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigs]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigs]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5487152b5f6701aab1f3c69ec58c6aa128f543431ad46601bac72df7aaebea89)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dialogflowConversationProfile.DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9edcef4c8babaff590ebe7caf8a925d2d6c25db551ed999c22e8c48a905afef9)
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
        :param baseline_model_version: Version of current baseline model. It will be ignored if model is set. Valid versions are: Article Suggestion baseline model: - 0.9 - 1.0 (default) Summarization baseline model: - 1.0 Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#baseline_model_version DialogflowConversationProfile#baseline_model_version}
        :param model: Conversation model resource name. Format: projects//conversationModels/. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#model DialogflowConversationProfile#model}
        '''
        value = DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsConversationModelConfig(
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
        :param recent_sentences_count: Number of recent non-small-talk sentences to use as context for article and FAQ suggestion. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#recent_sentences_count DialogflowConversationProfile#recent_sentences_count}
        '''
        value = DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsConversationProcessConfig(
            recent_sentences_count=recent_sentences_count
        )

        return typing.cast(None, jsii.invoke(self, "putConversationProcessConfig", [value]))

    @jsii.member(jsii_name="putQueryConfig")
    def put_query_config(
        self,
        *,
        confidence_threshold: typing.Optional[jsii.Number] = None,
        context_filter_settings: typing.Optional[typing.Union["DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfigContextFilterSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        dialogflow_query_source: typing.Optional[typing.Union["DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfigDialogflowQuerySource", typing.Dict[builtins.str, typing.Any]]] = None,
        document_query_source: typing.Optional[typing.Union["DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfigDocumentQuerySource", typing.Dict[builtins.str, typing.Any]]] = None,
        knowledge_base_query_source: typing.Optional[typing.Union["DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfigKnowledgeBaseQuerySource", typing.Dict[builtins.str, typing.Any]]] = None,
        max_results: typing.Optional[jsii.Number] = None,
        sections: typing.Optional[typing.Union["DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfigSections", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param confidence_threshold: Confidence threshold of query result. This feature is only supported for types: ARTICLE_SUGGESTION, FAQ, SMART_REPLY, SMART_COMPOSE, KNOWLEDGE_SEARCH, KNOWLEDGE_ASSIST, ENTITY_EXTRACTION. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#confidence_threshold DialogflowConversationProfile#confidence_threshold}
        :param context_filter_settings: context_filter_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#context_filter_settings DialogflowConversationProfile#context_filter_settings}
        :param dialogflow_query_source: dialogflow_query_source block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#dialogflow_query_source DialogflowConversationProfile#dialogflow_query_source}
        :param document_query_source: document_query_source block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#document_query_source DialogflowConversationProfile#document_query_source}
        :param knowledge_base_query_source: knowledge_base_query_source block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#knowledge_base_query_source DialogflowConversationProfile#knowledge_base_query_source}
        :param max_results: Maximum number of results to return. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#max_results DialogflowConversationProfile#max_results}
        :param sections: sections block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#sections DialogflowConversationProfile#sections}
        '''
        value = DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfig(
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
        :param type: Type of Human Agent Assistant API feature to request. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#type DialogflowConversationProfile#type}
        '''
        value = DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsSuggestionFeature(
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
        :param no_small_talk: Do not trigger if last utterance is small talk. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#no_small_talk DialogflowConversationProfile#no_small_talk}
        :param only_end_user: Only trigger suggestion if participant role of last utterance is END_USER. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#only_end_user DialogflowConversationProfile#only_end_user}
        '''
        value = DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsSuggestionTriggerSettings(
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
    ) -> DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsConversationModelConfigOutputReference:
        return typing.cast(DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsConversationModelConfigOutputReference, jsii.get(self, "conversationModelConfig"))

    @builtins.property
    @jsii.member(jsii_name="conversationProcessConfig")
    def conversation_process_config(
        self,
    ) -> DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsConversationProcessConfigOutputReference:
        return typing.cast(DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsConversationProcessConfigOutputReference, jsii.get(self, "conversationProcessConfig"))

    @builtins.property
    @jsii.member(jsii_name="queryConfig")
    def query_config(
        self,
    ) -> "DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfigOutputReference":
        return typing.cast("DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfigOutputReference", jsii.get(self, "queryConfig"))

    @builtins.property
    @jsii.member(jsii_name="suggestionFeature")
    def suggestion_feature(
        self,
    ) -> "DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsSuggestionFeatureOutputReference":
        return typing.cast("DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsSuggestionFeatureOutputReference", jsii.get(self, "suggestionFeature"))

    @builtins.property
    @jsii.member(jsii_name="suggestionTriggerSettings")
    def suggestion_trigger_settings(
        self,
    ) -> "DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsSuggestionTriggerSettingsOutputReference":
        return typing.cast("DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsSuggestionTriggerSettingsOutputReference", jsii.get(self, "suggestionTriggerSettings"))

    @builtins.property
    @jsii.member(jsii_name="conversationModelConfigInput")
    def conversation_model_config_input(
        self,
    ) -> typing.Optional[DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsConversationModelConfig]:
        return typing.cast(typing.Optional[DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsConversationModelConfig], jsii.get(self, "conversationModelConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="conversationProcessConfigInput")
    def conversation_process_config_input(
        self,
    ) -> typing.Optional[DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsConversationProcessConfig]:
        return typing.cast(typing.Optional[DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsConversationProcessConfig], jsii.get(self, "conversationProcessConfigInput"))

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
    ) -> typing.Optional["DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfig"]:
        return typing.cast(typing.Optional["DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfig"], jsii.get(self, "queryConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="suggestionFeatureInput")
    def suggestion_feature_input(
        self,
    ) -> typing.Optional["DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsSuggestionFeature"]:
        return typing.cast(typing.Optional["DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsSuggestionFeature"], jsii.get(self, "suggestionFeatureInput"))

    @builtins.property
    @jsii.member(jsii_name="suggestionTriggerSettingsInput")
    def suggestion_trigger_settings_input(
        self,
    ) -> typing.Optional["DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsSuggestionTriggerSettings"]:
        return typing.cast(typing.Optional["DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsSuggestionTriggerSettings"], jsii.get(self, "suggestionTriggerSettingsInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__72373f8071fa9ab595af19bddc490002f8da63dad67c2d2d8b69656600977b73)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9ecc55a6a371757ab2067bacc28016c11bc85808ada4343d5f78a02c196c5533)
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
            type_hints = typing.get_type_hints(_typecheckingstub__11693605454146fd7b058134518d3f8f6c8694403dd11faf8eca0921ea243a2e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__26a8049f1db311ace3f9ed48bd8af329d1917d8b1833db64ea92fbb77069a516)
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
            type_hints = typing.get_type_hints(_typecheckingstub__03b5d6488de75ab381a23ed95e34128aa5ff1d770f6c13f891bade673a4e8d29)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableQuerySuggestionWhenNoAnswer", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigs]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigs]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigs]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__58f0af7c850bd1701f3fc8fd8c465213e3d8ac5dbc713f8d2c099997fb134ee4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dialogflowConversationProfile.DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfig",
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
class DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfig:
    def __init__(
        self,
        *,
        confidence_threshold: typing.Optional[jsii.Number] = None,
        context_filter_settings: typing.Optional[typing.Union["DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfigContextFilterSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        dialogflow_query_source: typing.Optional[typing.Union["DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfigDialogflowQuerySource", typing.Dict[builtins.str, typing.Any]]] = None,
        document_query_source: typing.Optional[typing.Union["DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfigDocumentQuerySource", typing.Dict[builtins.str, typing.Any]]] = None,
        knowledge_base_query_source: typing.Optional[typing.Union["DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfigKnowledgeBaseQuerySource", typing.Dict[builtins.str, typing.Any]]] = None,
        max_results: typing.Optional[jsii.Number] = None,
        sections: typing.Optional[typing.Union["DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfigSections", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param confidence_threshold: Confidence threshold of query result. This feature is only supported for types: ARTICLE_SUGGESTION, FAQ, SMART_REPLY, SMART_COMPOSE, KNOWLEDGE_SEARCH, KNOWLEDGE_ASSIST, ENTITY_EXTRACTION. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#confidence_threshold DialogflowConversationProfile#confidence_threshold}
        :param context_filter_settings: context_filter_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#context_filter_settings DialogflowConversationProfile#context_filter_settings}
        :param dialogflow_query_source: dialogflow_query_source block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#dialogflow_query_source DialogflowConversationProfile#dialogflow_query_source}
        :param document_query_source: document_query_source block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#document_query_source DialogflowConversationProfile#document_query_source}
        :param knowledge_base_query_source: knowledge_base_query_source block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#knowledge_base_query_source DialogflowConversationProfile#knowledge_base_query_source}
        :param max_results: Maximum number of results to return. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#max_results DialogflowConversationProfile#max_results}
        :param sections: sections block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#sections DialogflowConversationProfile#sections}
        '''
        if isinstance(context_filter_settings, dict):
            context_filter_settings = DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfigContextFilterSettings(**context_filter_settings)
        if isinstance(dialogflow_query_source, dict):
            dialogflow_query_source = DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfigDialogflowQuerySource(**dialogflow_query_source)
        if isinstance(document_query_source, dict):
            document_query_source = DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfigDocumentQuerySource(**document_query_source)
        if isinstance(knowledge_base_query_source, dict):
            knowledge_base_query_source = DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfigKnowledgeBaseQuerySource(**knowledge_base_query_source)
        if isinstance(sections, dict):
            sections = DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfigSections(**sections)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1ee9fcf1cb89f491ac849058d5859a5f17df1c2659aba86703d5feb20400de0c)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#confidence_threshold DialogflowConversationProfile#confidence_threshold}
        '''
        result = self._values.get("confidence_threshold")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def context_filter_settings(
        self,
    ) -> typing.Optional["DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfigContextFilterSettings"]:
        '''context_filter_settings block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#context_filter_settings DialogflowConversationProfile#context_filter_settings}
        '''
        result = self._values.get("context_filter_settings")
        return typing.cast(typing.Optional["DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfigContextFilterSettings"], result)

    @builtins.property
    def dialogflow_query_source(
        self,
    ) -> typing.Optional["DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfigDialogflowQuerySource"]:
        '''dialogflow_query_source block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#dialogflow_query_source DialogflowConversationProfile#dialogflow_query_source}
        '''
        result = self._values.get("dialogflow_query_source")
        return typing.cast(typing.Optional["DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfigDialogflowQuerySource"], result)

    @builtins.property
    def document_query_source(
        self,
    ) -> typing.Optional["DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfigDocumentQuerySource"]:
        '''document_query_source block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#document_query_source DialogflowConversationProfile#document_query_source}
        '''
        result = self._values.get("document_query_source")
        return typing.cast(typing.Optional["DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfigDocumentQuerySource"], result)

    @builtins.property
    def knowledge_base_query_source(
        self,
    ) -> typing.Optional["DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfigKnowledgeBaseQuerySource"]:
        '''knowledge_base_query_source block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#knowledge_base_query_source DialogflowConversationProfile#knowledge_base_query_source}
        '''
        result = self._values.get("knowledge_base_query_source")
        return typing.cast(typing.Optional["DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfigKnowledgeBaseQuerySource"], result)

    @builtins.property
    def max_results(self) -> typing.Optional[jsii.Number]:
        '''Maximum number of results to return.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#max_results DialogflowConversationProfile#max_results}
        '''
        result = self._values.get("max_results")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def sections(
        self,
    ) -> typing.Optional["DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfigSections"]:
        '''sections block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#sections DialogflowConversationProfile#sections}
        '''
        result = self._values.get("sections")
        return typing.cast(typing.Optional["DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfigSections"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dialogflowConversationProfile.DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfigContextFilterSettings",
    jsii_struct_bases=[],
    name_mapping={
        "drop_handoff_messages": "dropHandoffMessages",
        "drop_ivr_messages": "dropIvrMessages",
        "drop_virtual_agent_messages": "dropVirtualAgentMessages",
    },
)
class DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfigContextFilterSettings:
    def __init__(
        self,
        *,
        drop_handoff_messages: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        drop_ivr_messages: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        drop_virtual_agent_messages: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param drop_handoff_messages: If set to true, the last message from virtual agent (hand off message) and the message before it (trigger message of hand off) are dropped. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#drop_handoff_messages DialogflowConversationProfile#drop_handoff_messages}
        :param drop_ivr_messages: If set to true, all messages from ivr stage are dropped. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#drop_ivr_messages DialogflowConversationProfile#drop_ivr_messages}
        :param drop_virtual_agent_messages: If set to true, all messages from virtual agent are dropped. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#drop_virtual_agent_messages DialogflowConversationProfile#drop_virtual_agent_messages}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__35a4461efb86cf6729738f3bc71e36a8128e87f6ff3dd50c48a17f7caf379774)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#drop_handoff_messages DialogflowConversationProfile#drop_handoff_messages}
        '''
        result = self._values.get("drop_handoff_messages")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def drop_ivr_messages(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If set to true, all messages from ivr stage are dropped.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#drop_ivr_messages DialogflowConversationProfile#drop_ivr_messages}
        '''
        result = self._values.get("drop_ivr_messages")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def drop_virtual_agent_messages(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If set to true, all messages from virtual agent are dropped.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#drop_virtual_agent_messages DialogflowConversationProfile#drop_virtual_agent_messages}
        '''
        result = self._values.get("drop_virtual_agent_messages")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfigContextFilterSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfigContextFilterSettingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dialogflowConversationProfile.DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfigContextFilterSettingsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__77572a4370dbdaf104df2798a4fa8d9f5c1e0b08f61ff0c4c97a1acdf8101fd8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__015c1213c1d2ba982b02a0342a7f2bb16387c38839cbb9bfbf18c8f279001091)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f2aecdb0e60ea79d29e817b845da091971adb2eb0ae491efc0b87bd8d1123e01)
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
            type_hints = typing.get_type_hints(_typecheckingstub__853b2fc2d0773225873390cbce61a1aea4232a1d46cfa15507ebdf29b992443d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dropVirtualAgentMessages", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfigContextFilterSettings]:
        return typing.cast(typing.Optional[DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfigContextFilterSettings], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfigContextFilterSettings],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d81addcacfd82d140f90396615200d6882eafc48b9970e6370e45c7ec8734856)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dialogflowConversationProfile.DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfigDialogflowQuerySource",
    jsii_struct_bases=[],
    name_mapping={"agent": "agent", "human_agent_side_config": "humanAgentSideConfig"},
)
class DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfigDialogflowQuerySource:
    def __init__(
        self,
        *,
        agent: builtins.str,
        human_agent_side_config: typing.Optional[typing.Union["DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfigDialogflowQuerySourceHumanAgentSideConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param agent: he name of a Dialogflow virtual agent used for end user side intent detection and suggestion. Format: projects//locations//agent. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#agent DialogflowConversationProfile#agent}
        :param human_agent_side_config: human_agent_side_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#human_agent_side_config DialogflowConversationProfile#human_agent_side_config}
        '''
        if isinstance(human_agent_side_config, dict):
            human_agent_side_config = DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfigDialogflowQuerySourceHumanAgentSideConfig(**human_agent_side_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__44916a521be93e016d51addc204793eb8ef3a3e59c7d579463a606f97edf90be)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#agent DialogflowConversationProfile#agent}
        '''
        result = self._values.get("agent")
        assert result is not None, "Required property 'agent' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def human_agent_side_config(
        self,
    ) -> typing.Optional["DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfigDialogflowQuerySourceHumanAgentSideConfig"]:
        '''human_agent_side_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#human_agent_side_config DialogflowConversationProfile#human_agent_side_config}
        '''
        result = self._values.get("human_agent_side_config")
        return typing.cast(typing.Optional["DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfigDialogflowQuerySourceHumanAgentSideConfig"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfigDialogflowQuerySource(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dialogflowConversationProfile.DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfigDialogflowQuerySourceHumanAgentSideConfig",
    jsii_struct_bases=[],
    name_mapping={"agent": "agent"},
)
class DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfigDialogflowQuerySourceHumanAgentSideConfig:
    def __init__(self, *, agent: typing.Optional[builtins.str] = None) -> None:
        '''
        :param agent: The name of a dialogflow virtual agent used for intent detection and suggestion triggered by human agent. Format: projects//locations//agent. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#agent DialogflowConversationProfile#agent}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a03215840345ec042c0da820858e14178cf34ce4a5b2ebef1996d6ce36010966)
            check_type(argname="argument agent", value=agent, expected_type=type_hints["agent"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if agent is not None:
            self._values["agent"] = agent

    @builtins.property
    def agent(self) -> typing.Optional[builtins.str]:
        '''The name of a dialogflow virtual agent used for intent detection and suggestion triggered by human agent.

        Format: projects//locations//agent.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#agent DialogflowConversationProfile#agent}
        '''
        result = self._values.get("agent")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfigDialogflowQuerySourceHumanAgentSideConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfigDialogflowQuerySourceHumanAgentSideConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dialogflowConversationProfile.DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfigDialogflowQuerySourceHumanAgentSideConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fea1ff5b519dd76d4bfa610481e331ba4500810399e0b3af33e21be227798544)
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
            type_hints = typing.get_type_hints(_typecheckingstub__eb18323c673835b6c764be8b43f8b56c3de295ad8b735db6a605da4df32c57ec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "agent", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfigDialogflowQuerySourceHumanAgentSideConfig]:
        return typing.cast(typing.Optional[DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfigDialogflowQuerySourceHumanAgentSideConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfigDialogflowQuerySourceHumanAgentSideConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__840a2606e34f5789cdf61f8d085faf0986b697160e15170533ce430d9f346556)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfigDialogflowQuerySourceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dialogflowConversationProfile.DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfigDialogflowQuerySourceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3f58bb77bfc79b452a3a5b1b6f5e288b64d65dde73857687e3aa23da3c110395)
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
        :param agent: The name of a dialogflow virtual agent used for intent detection and suggestion triggered by human agent. Format: projects//locations//agent. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#agent DialogflowConversationProfile#agent}
        '''
        value = DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfigDialogflowQuerySourceHumanAgentSideConfig(
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
    ) -> DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfigDialogflowQuerySourceHumanAgentSideConfigOutputReference:
        return typing.cast(DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfigDialogflowQuerySourceHumanAgentSideConfigOutputReference, jsii.get(self, "humanAgentSideConfig"))

    @builtins.property
    @jsii.member(jsii_name="agentInput")
    def agent_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "agentInput"))

    @builtins.property
    @jsii.member(jsii_name="humanAgentSideConfigInput")
    def human_agent_side_config_input(
        self,
    ) -> typing.Optional[DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfigDialogflowQuerySourceHumanAgentSideConfig]:
        return typing.cast(typing.Optional[DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfigDialogflowQuerySourceHumanAgentSideConfig], jsii.get(self, "humanAgentSideConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="agent")
    def agent(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "agent"))

    @agent.setter
    def agent(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__56c83c807da2350745bdf6151adddca2483185f3a8bf4cb3b4b5696a77f27f40)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "agent", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfigDialogflowQuerySource]:
        return typing.cast(typing.Optional[DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfigDialogflowQuerySource], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfigDialogflowQuerySource],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0cb7ad203b17b71b225b03816ba0ab41463680c0c146a4ce9a28abdbe0b5ced3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dialogflowConversationProfile.DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfigDocumentQuerySource",
    jsii_struct_bases=[],
    name_mapping={"documents": "documents"},
)
class DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfigDocumentQuerySource:
    def __init__(self, *, documents: typing.Sequence[builtins.str]) -> None:
        '''
        :param documents: Knowledge documents to query from. Format: projects//locations//knowledgeBases//documents/. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#documents DialogflowConversationProfile#documents}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5916f2d67777551e985d3f61aa7566505f8da261e9bef6a166a25f20d8c46806)
            check_type(argname="argument documents", value=documents, expected_type=type_hints["documents"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "documents": documents,
        }

    @builtins.property
    def documents(self) -> typing.List[builtins.str]:
        '''Knowledge documents to query from. Format: projects//locations//knowledgeBases//documents/.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#documents DialogflowConversationProfile#documents}
        '''
        result = self._values.get("documents")
        assert result is not None, "Required property 'documents' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfigDocumentQuerySource(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfigDocumentQuerySourceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dialogflowConversationProfile.DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfigDocumentQuerySourceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ed8e4c6145dff9830ebdc66d326ea11f7d0b7d1a7c4b97305a754fdaebb839e3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fb4344dd9f54343204002f329fbd2268ed2fd7d83d10cc2ed56899fe855985f1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "documents", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfigDocumentQuerySource]:
        return typing.cast(typing.Optional[DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfigDocumentQuerySource], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfigDocumentQuerySource],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e9432c71790f69ccbb3280221ff7b0d6853572d88d4efe02c977da64827d841a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dialogflowConversationProfile.DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfigKnowledgeBaseQuerySource",
    jsii_struct_bases=[],
    name_mapping={"knowledge_bases": "knowledgeBases"},
)
class DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfigKnowledgeBaseQuerySource:
    def __init__(self, *, knowledge_bases: typing.Sequence[builtins.str]) -> None:
        '''
        :param knowledge_bases: Knowledge bases to query. Format: projects//locations//knowledgeBases/. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#knowledge_bases DialogflowConversationProfile#knowledge_bases}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ecda5c89511d1cf6e9bbd291a615db98d915e130ebb1afa29d1acbfd71a9f41e)
            check_type(argname="argument knowledge_bases", value=knowledge_bases, expected_type=type_hints["knowledge_bases"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "knowledge_bases": knowledge_bases,
        }

    @builtins.property
    def knowledge_bases(self) -> typing.List[builtins.str]:
        '''Knowledge bases to query. Format: projects//locations//knowledgeBases/.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#knowledge_bases DialogflowConversationProfile#knowledge_bases}
        '''
        result = self._values.get("knowledge_bases")
        assert result is not None, "Required property 'knowledge_bases' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfigKnowledgeBaseQuerySource(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfigKnowledgeBaseQuerySourceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dialogflowConversationProfile.DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfigKnowledgeBaseQuerySourceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__70f554988cd6d133be6af0d8c65e53907e6be343936322d31d635bb4d4407c7f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9fcaf743980da5e652f3ba51982cebbc0c116deea4daf0b287a3fa7822e17dbd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "knowledgeBases", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfigKnowledgeBaseQuerySource]:
        return typing.cast(typing.Optional[DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfigKnowledgeBaseQuerySource], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfigKnowledgeBaseQuerySource],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__178c31edaaa7238f72fcf4af5a5e6caa9b2a72e1b2b36bb8a85101f6c2bb83b5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dialogflowConversationProfile.DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ffd7ffb384f5d67058af3aef38f55ea3076c08a4c0e3a6d92f5967baf8ae8f79)
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
        :param drop_handoff_messages: If set to true, the last message from virtual agent (hand off message) and the message before it (trigger message of hand off) are dropped. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#drop_handoff_messages DialogflowConversationProfile#drop_handoff_messages}
        :param drop_ivr_messages: If set to true, all messages from ivr stage are dropped. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#drop_ivr_messages DialogflowConversationProfile#drop_ivr_messages}
        :param drop_virtual_agent_messages: If set to true, all messages from virtual agent are dropped. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#drop_virtual_agent_messages DialogflowConversationProfile#drop_virtual_agent_messages}
        '''
        value = DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfigContextFilterSettings(
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
        human_agent_side_config: typing.Optional[typing.Union[DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfigDialogflowQuerySourceHumanAgentSideConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param agent: he name of a Dialogflow virtual agent used for end user side intent detection and suggestion. Format: projects//locations//agent. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#agent DialogflowConversationProfile#agent}
        :param human_agent_side_config: human_agent_side_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#human_agent_side_config DialogflowConversationProfile#human_agent_side_config}
        '''
        value = DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfigDialogflowQuerySource(
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
        :param documents: Knowledge documents to query from. Format: projects//locations//knowledgeBases//documents/. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#documents DialogflowConversationProfile#documents}
        '''
        value = DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfigDocumentQuerySource(
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
        :param knowledge_bases: Knowledge bases to query. Format: projects//locations//knowledgeBases/. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#knowledge_bases DialogflowConversationProfile#knowledge_bases}
        '''
        value = DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfigKnowledgeBaseQuerySource(
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
        :param section_types: The selected sections chosen to return when requesting a summary of a conversation If not provided the default selection will be "{SITUATION, ACTION, RESULT}". Possible values: ["SECTION_TYPE_UNSPECIFIED", "SITUATION", "ACTION", "RESOLUTION", "REASON_FOR_CANCELLATION", "CUSTOMER_SATISFACTION", "ENTITIES"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#section_types DialogflowConversationProfile#section_types}
        '''
        value = DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfigSections(
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
    ) -> DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfigContextFilterSettingsOutputReference:
        return typing.cast(DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfigContextFilterSettingsOutputReference, jsii.get(self, "contextFilterSettings"))

    @builtins.property
    @jsii.member(jsii_name="dialogflowQuerySource")
    def dialogflow_query_source(
        self,
    ) -> DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfigDialogflowQuerySourceOutputReference:
        return typing.cast(DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfigDialogflowQuerySourceOutputReference, jsii.get(self, "dialogflowQuerySource"))

    @builtins.property
    @jsii.member(jsii_name="documentQuerySource")
    def document_query_source(
        self,
    ) -> DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfigDocumentQuerySourceOutputReference:
        return typing.cast(DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfigDocumentQuerySourceOutputReference, jsii.get(self, "documentQuerySource"))

    @builtins.property
    @jsii.member(jsii_name="knowledgeBaseQuerySource")
    def knowledge_base_query_source(
        self,
    ) -> DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfigKnowledgeBaseQuerySourceOutputReference:
        return typing.cast(DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfigKnowledgeBaseQuerySourceOutputReference, jsii.get(self, "knowledgeBaseQuerySource"))

    @builtins.property
    @jsii.member(jsii_name="sections")
    def sections(
        self,
    ) -> "DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfigSectionsOutputReference":
        return typing.cast("DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfigSectionsOutputReference", jsii.get(self, "sections"))

    @builtins.property
    @jsii.member(jsii_name="confidenceThresholdInput")
    def confidence_threshold_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "confidenceThresholdInput"))

    @builtins.property
    @jsii.member(jsii_name="contextFilterSettingsInput")
    def context_filter_settings_input(
        self,
    ) -> typing.Optional[DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfigContextFilterSettings]:
        return typing.cast(typing.Optional[DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfigContextFilterSettings], jsii.get(self, "contextFilterSettingsInput"))

    @builtins.property
    @jsii.member(jsii_name="dialogflowQuerySourceInput")
    def dialogflow_query_source_input(
        self,
    ) -> typing.Optional[DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfigDialogflowQuerySource]:
        return typing.cast(typing.Optional[DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfigDialogflowQuerySource], jsii.get(self, "dialogflowQuerySourceInput"))

    @builtins.property
    @jsii.member(jsii_name="documentQuerySourceInput")
    def document_query_source_input(
        self,
    ) -> typing.Optional[DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfigDocumentQuerySource]:
        return typing.cast(typing.Optional[DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfigDocumentQuerySource], jsii.get(self, "documentQuerySourceInput"))

    @builtins.property
    @jsii.member(jsii_name="knowledgeBaseQuerySourceInput")
    def knowledge_base_query_source_input(
        self,
    ) -> typing.Optional[DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfigKnowledgeBaseQuerySource]:
        return typing.cast(typing.Optional[DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfigKnowledgeBaseQuerySource], jsii.get(self, "knowledgeBaseQuerySourceInput"))

    @builtins.property
    @jsii.member(jsii_name="maxResultsInput")
    def max_results_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxResultsInput"))

    @builtins.property
    @jsii.member(jsii_name="sectionsInput")
    def sections_input(
        self,
    ) -> typing.Optional["DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfigSections"]:
        return typing.cast(typing.Optional["DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfigSections"], jsii.get(self, "sectionsInput"))

    @builtins.property
    @jsii.member(jsii_name="confidenceThreshold")
    def confidence_threshold(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "confidenceThreshold"))

    @confidence_threshold.setter
    def confidence_threshold(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__20664f9bfa1a8e67472af75d8e042ba0af579aab559a71254505ee6c0a15990f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "confidenceThreshold", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxResults")
    def max_results(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxResults"))

    @max_results.setter
    def max_results(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__37c5ac15e3b2407aeafca3db3af3949e96fe22180897618832fcaaa3d101b6ec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxResults", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfig]:
        return typing.cast(typing.Optional[DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__41a9129c752df3e9f1cbbf105139c5efb9e372fcdbd07a53520b68ef69cad04d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dialogflowConversationProfile.DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfigSections",
    jsii_struct_bases=[],
    name_mapping={"section_types": "sectionTypes"},
)
class DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfigSections:
    def __init__(
        self,
        *,
        section_types: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param section_types: The selected sections chosen to return when requesting a summary of a conversation If not provided the default selection will be "{SITUATION, ACTION, RESULT}". Possible values: ["SECTION_TYPE_UNSPECIFIED", "SITUATION", "ACTION", "RESOLUTION", "REASON_FOR_CANCELLATION", "CUSTOMER_SATISFACTION", "ENTITIES"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#section_types DialogflowConversationProfile#section_types}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d9cca18a6634a88fd1a514a3d862b2c69736a1bd17b24c81e2c9ebfdf6a85b52)
            check_type(argname="argument section_types", value=section_types, expected_type=type_hints["section_types"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if section_types is not None:
            self._values["section_types"] = section_types

    @builtins.property
    def section_types(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The selected sections chosen to return when requesting a summary of a conversation If not provided the default selection will be "{SITUATION, ACTION, RESULT}".

        Possible values: ["SECTION_TYPE_UNSPECIFIED", "SITUATION", "ACTION", "RESOLUTION", "REASON_FOR_CANCELLATION", "CUSTOMER_SATISFACTION", "ENTITIES"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#section_types DialogflowConversationProfile#section_types}
        '''
        result = self._values.get("section_types")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfigSections(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfigSectionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dialogflowConversationProfile.DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfigSectionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e6616de12e10eb61217476a9ea5cf2958739a474acd2c197ce9c2857adabf95a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__57164eea9a39a4167f0ee03d8ac77e1b2cfc888e8f7e70588f037572c3479633)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sectionTypes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfigSections]:
        return typing.cast(typing.Optional[DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfigSections], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfigSections],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__908819a0cca627d04e1ea05176f1b1783458858bb654e2f1b80ac16364701d6b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dialogflowConversationProfile.DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsSuggestionFeature",
    jsii_struct_bases=[],
    name_mapping={"type": "type"},
)
class DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsSuggestionFeature:
    def __init__(self, *, type: typing.Optional[builtins.str] = None) -> None:
        '''
        :param type: Type of Human Agent Assistant API feature to request. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#type DialogflowConversationProfile#type}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__29128bf19a5da111e2e6fd4388ed0cd616f8aa2936b6ba37f3bccc952a6e8525)
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if type is not None:
            self._values["type"] = type

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''Type of Human Agent Assistant API feature to request.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#type DialogflowConversationProfile#type}
        '''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsSuggestionFeature(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsSuggestionFeatureOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dialogflowConversationProfile.DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsSuggestionFeatureOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4778d9cbcc9813c5ecf271dea806e4ad141a89aa747d2aed6533f4af4b550497)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5c780cb6f90bb3c0e717283c944547058b34ff09da37f454b41dcbf7283a6ed2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsSuggestionFeature]:
        return typing.cast(typing.Optional[DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsSuggestionFeature], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsSuggestionFeature],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f2896ea410d8b3dd7d1fab1cf2a06e496c9aee94da707b8a2dfa65cd2c1f42c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dialogflowConversationProfile.DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsSuggestionTriggerSettings",
    jsii_struct_bases=[],
    name_mapping={"no_small_talk": "noSmallTalk", "only_end_user": "onlyEndUser"},
)
class DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsSuggestionTriggerSettings:
    def __init__(
        self,
        *,
        no_small_talk: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        only_end_user: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param no_small_talk: Do not trigger if last utterance is small talk. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#no_small_talk DialogflowConversationProfile#no_small_talk}
        :param only_end_user: Only trigger suggestion if participant role of last utterance is END_USER. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#only_end_user DialogflowConversationProfile#only_end_user}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fd5d9ab02b1449755adff26b4085efc8477bf20dfed413a31b0f18556b43e0bb)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#no_small_talk DialogflowConversationProfile#no_small_talk}
        '''
        result = self._values.get("no_small_talk")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def only_end_user(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Only trigger suggestion if participant role of last utterance is END_USER.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#only_end_user DialogflowConversationProfile#only_end_user}
        '''
        result = self._values.get("only_end_user")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsSuggestionTriggerSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsSuggestionTriggerSettingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dialogflowConversationProfile.DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsSuggestionTriggerSettingsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bee633b09e2214f769830f27a067549bd47d0934e81d570f93b360e26609e8a2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8116e5553912c477d08d6ff92b0117b153bae272b7b8a5397aed62cc31b0eb5a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__92728370e2a56388a148a74f26144f6db370d5b80a5e5c5462b7578f0a58576d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "onlyEndUser", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsSuggestionTriggerSettings]:
        return typing.cast(typing.Optional[DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsSuggestionTriggerSettings], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsSuggestionTriggerSettings],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__147db57be1128aff564405a06ea7800d2e36b0fcbfff6d060dbcb0cc6f333211)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dialogflowConversationProfile.DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3d0202ae02993657d66824c22321186d26bde614884285a81b8408a2867250f7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putFeatureConfigs")
    def put_feature_configs(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigs, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e7dbb0658db88657f3bf1ef37692d7d5d76062c5dedaef69f7b59e98e0d31899)
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
    ) -> DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsList:
        return typing.cast(DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsList, jsii.get(self, "featureConfigs"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigs]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigs]]], jsii.get(self, "featureConfigsInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__0e4d85bef9852bb5d954306f9f3cbf8031105a43d0360f99b7726a903caa2f9e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "disableHighLatencyFeaturesSyncDelivery", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="generators")
    def generators(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "generators"))

    @generators.setter
    def generators(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d7c369ab3ab0176c3e7e44efe6521057b6fb8823b44fbadada2110a55b0ea4b9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ce2927d1b006d4776330611002db92ae38794f4bd3185e81390e9a8627203760)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "groupSuggestionResponses", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfig]:
        return typing.cast(typing.Optional[DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__450a5e06c0fa3be9f741d5a7d7b062f0e519876f38966ca7fb9a08a247d02ba5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dialogflowConversationProfile.DialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfig",
    jsii_struct_bases=[],
    name_mapping={
        "disable_high_latency_features_sync_delivery": "disableHighLatencyFeaturesSyncDelivery",
        "feature_configs": "featureConfigs",
        "generators": "generators",
        "group_suggestion_responses": "groupSuggestionResponses",
    },
)
class DialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfig:
    def __init__(
        self,
        *,
        disable_high_latency_features_sync_delivery: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        feature_configs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigs", typing.Dict[builtins.str, typing.Any]]]]] = None,
        generators: typing.Optional[typing.Sequence[builtins.str]] = None,
        group_suggestion_responses: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param disable_high_latency_features_sync_delivery: When disableHighLatencyFeaturesSyncDelivery is true and using the AnalyzeContent API, we will not deliver the responses from high latency features in the API response. The humanAgentAssistantConfig.notification_config must be configured and enableEventBasedSuggestion must be set to true to receive the responses from high latency features in Pub/Sub. High latency feature(s): KNOWLEDGE_ASSIST Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#disable_high_latency_features_sync_delivery DialogflowConversationProfile#disable_high_latency_features_sync_delivery}
        :param feature_configs: feature_configs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#feature_configs DialogflowConversationProfile#feature_configs}
        :param generators: List of various generator resource names used in the conversation profile. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#generators DialogflowConversationProfile#generators}
        :param group_suggestion_responses: If groupSuggestionResponses is false, and there are multiple featureConfigs in event based suggestion or StreamingAnalyzeContent, we will try to deliver suggestions to customers as soon as we get new suggestion. Different type of suggestions based on the same context will be in separate Pub/Sub event or StreamingAnalyzeContentResponse. If groupSuggestionResponses set to true. All the suggestions to the same participant based on the same context will be grouped into a single Pub/Sub event or StreamingAnalyzeContentResponse. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#group_suggestion_responses DialogflowConversationProfile#group_suggestion_responses}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a3c71bb3f79a2f2dfb7c8982d5626c62cd838a7f2248a3e82a35bd0a3714127)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#disable_high_latency_features_sync_delivery DialogflowConversationProfile#disable_high_latency_features_sync_delivery}
        '''
        result = self._values.get("disable_high_latency_features_sync_delivery")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def feature_configs(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigs"]]]:
        '''feature_configs block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#feature_configs DialogflowConversationProfile#feature_configs}
        '''
        result = self._values.get("feature_configs")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigs"]]], result)

    @builtins.property
    def generators(self) -> typing.Optional[typing.List[builtins.str]]:
        '''List of various generator resource names used in the conversation profile.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#generators DialogflowConversationProfile#generators}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#group_suggestion_responses DialogflowConversationProfile#group_suggestion_responses}
        '''
        result = self._values.get("group_suggestion_responses")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dialogflowConversationProfile.DialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigs",
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
class DialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigs:
    def __init__(
        self,
        *,
        conversation_model_config: typing.Optional[typing.Union["DialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsConversationModelConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        conversation_process_config: typing.Optional[typing.Union["DialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsConversationProcessConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        disable_agent_query_logging: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_conversation_augmented_query: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_event_based_suggestion: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_query_suggestion_only: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_query_suggestion_when_no_answer: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        query_config: typing.Optional[typing.Union["DialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsQueryConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        suggestion_feature: typing.Optional[typing.Union["DialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsSuggestionFeature", typing.Dict[builtins.str, typing.Any]]] = None,
        suggestion_trigger_settings: typing.Optional[typing.Union["DialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsSuggestionTriggerSettings", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param conversation_model_config: conversation_model_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#conversation_model_config DialogflowConversationProfile#conversation_model_config}
        :param conversation_process_config: conversation_process_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#conversation_process_config DialogflowConversationProfile#conversation_process_config}
        :param disable_agent_query_logging: Disable the logging of search queries sent by human agents. It can prevent those queries from being stored at answer records. This feature is only supported for types: KNOWLEDGE_SEARCH. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#disable_agent_query_logging DialogflowConversationProfile#disable_agent_query_logging}
        :param enable_conversation_augmented_query: Enable including conversation context during query answer generation. This feature is only supported for types: KNOWLEDGE_SEARCH. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#enable_conversation_augmented_query DialogflowConversationProfile#enable_conversation_augmented_query}
        :param enable_event_based_suggestion: Automatically iterates all participants and tries to compile suggestions. This feature is only supported for types: ARTICLE_SUGGESTION, FAQ, DIALOGFLOW_ASSIST, KNOWLEDGE_ASSIST. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#enable_event_based_suggestion DialogflowConversationProfile#enable_event_based_suggestion}
        :param enable_query_suggestion_only: Enable query suggestion only. This feature is only supported for types: KNOWLEDGE_ASSIST. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#enable_query_suggestion_only DialogflowConversationProfile#enable_query_suggestion_only}
        :param enable_query_suggestion_when_no_answer: Enable query suggestion even if we can't find its answer. By default, queries are suggested only if we find its answer. This feature is only supported for types: KNOWLEDGE_ASSIST. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#enable_query_suggestion_when_no_answer DialogflowConversationProfile#enable_query_suggestion_when_no_answer}
        :param query_config: query_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#query_config DialogflowConversationProfile#query_config}
        :param suggestion_feature: suggestion_feature block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#suggestion_feature DialogflowConversationProfile#suggestion_feature}
        :param suggestion_trigger_settings: suggestion_trigger_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#suggestion_trigger_settings DialogflowConversationProfile#suggestion_trigger_settings}
        '''
        if isinstance(conversation_model_config, dict):
            conversation_model_config = DialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsConversationModelConfig(**conversation_model_config)
        if isinstance(conversation_process_config, dict):
            conversation_process_config = DialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsConversationProcessConfig(**conversation_process_config)
        if isinstance(query_config, dict):
            query_config = DialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsQueryConfig(**query_config)
        if isinstance(suggestion_feature, dict):
            suggestion_feature = DialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsSuggestionFeature(**suggestion_feature)
        if isinstance(suggestion_trigger_settings, dict):
            suggestion_trigger_settings = DialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsSuggestionTriggerSettings(**suggestion_trigger_settings)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ddc475dd3ad52ec6d0c6032c7a162412a5fa2d9d5f9c9b36d68910c59f2bd9c)
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
    ) -> typing.Optional["DialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsConversationModelConfig"]:
        '''conversation_model_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#conversation_model_config DialogflowConversationProfile#conversation_model_config}
        '''
        result = self._values.get("conversation_model_config")
        return typing.cast(typing.Optional["DialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsConversationModelConfig"], result)

    @builtins.property
    def conversation_process_config(
        self,
    ) -> typing.Optional["DialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsConversationProcessConfig"]:
        '''conversation_process_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#conversation_process_config DialogflowConversationProfile#conversation_process_config}
        '''
        result = self._values.get("conversation_process_config")
        return typing.cast(typing.Optional["DialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsConversationProcessConfig"], result)

    @builtins.property
    def disable_agent_query_logging(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Disable the logging of search queries sent by human agents.

        It can prevent those queries from being stored at answer records.
        This feature is only supported for types: KNOWLEDGE_SEARCH.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#disable_agent_query_logging DialogflowConversationProfile#disable_agent_query_logging}
        '''
        result = self._values.get("disable_agent_query_logging")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def enable_conversation_augmented_query(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Enable including conversation context during query answer generation. This feature is only supported for types: KNOWLEDGE_SEARCH.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#enable_conversation_augmented_query DialogflowConversationProfile#enable_conversation_augmented_query}
        '''
        result = self._values.get("enable_conversation_augmented_query")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def enable_event_based_suggestion(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Automatically iterates all participants and tries to compile suggestions. This feature is only supported for types: ARTICLE_SUGGESTION, FAQ, DIALOGFLOW_ASSIST, KNOWLEDGE_ASSIST.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#enable_event_based_suggestion DialogflowConversationProfile#enable_event_based_suggestion}
        '''
        result = self._values.get("enable_event_based_suggestion")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def enable_query_suggestion_only(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Enable query suggestion only. This feature is only supported for types: KNOWLEDGE_ASSIST.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#enable_query_suggestion_only DialogflowConversationProfile#enable_query_suggestion_only}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#enable_query_suggestion_when_no_answer DialogflowConversationProfile#enable_query_suggestion_when_no_answer}
        '''
        result = self._values.get("enable_query_suggestion_when_no_answer")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def query_config(
        self,
    ) -> typing.Optional["DialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsQueryConfig"]:
        '''query_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#query_config DialogflowConversationProfile#query_config}
        '''
        result = self._values.get("query_config")
        return typing.cast(typing.Optional["DialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsQueryConfig"], result)

    @builtins.property
    def suggestion_feature(
        self,
    ) -> typing.Optional["DialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsSuggestionFeature"]:
        '''suggestion_feature block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#suggestion_feature DialogflowConversationProfile#suggestion_feature}
        '''
        result = self._values.get("suggestion_feature")
        return typing.cast(typing.Optional["DialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsSuggestionFeature"], result)

    @builtins.property
    def suggestion_trigger_settings(
        self,
    ) -> typing.Optional["DialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsSuggestionTriggerSettings"]:
        '''suggestion_trigger_settings block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#suggestion_trigger_settings DialogflowConversationProfile#suggestion_trigger_settings}
        '''
        result = self._values.get("suggestion_trigger_settings")
        return typing.cast(typing.Optional["DialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsSuggestionTriggerSettings"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigs(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dialogflowConversationProfile.DialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsConversationModelConfig",
    jsii_struct_bases=[],
    name_mapping={"baseline_model_version": "baselineModelVersion", "model": "model"},
)
class DialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsConversationModelConfig:
    def __init__(
        self,
        *,
        baseline_model_version: typing.Optional[builtins.str] = None,
        model: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param baseline_model_version: Version of current baseline model. It will be ignored if model is set. Valid versions are: Article Suggestion baseline model: - 0.9 - 1.0 (default) Summarization baseline model: - 1.0 Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#baseline_model_version DialogflowConversationProfile#baseline_model_version}
        :param model: Conversation model resource name. Format: projects//conversationModels/. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#model DialogflowConversationProfile#model}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__04808a52e4bb73404fbdd5fba2dc38161f9403f27859c1eb6036c669527f1a28)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#baseline_model_version DialogflowConversationProfile#baseline_model_version}
        '''
        result = self._values.get("baseline_model_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def model(self) -> typing.Optional[builtins.str]:
        '''Conversation model resource name. Format: projects//conversationModels/.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#model DialogflowConversationProfile#model}
        '''
        result = self._values.get("model")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsConversationModelConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsConversationModelConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dialogflowConversationProfile.DialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsConversationModelConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bebc6ffe849c608fc59123c67c55b0d9db53f0b21338e0384bb1fa4d7e66d3f7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5c730906d3aca59500c7556564d8903eb171a245bb52130317c6efb01a019ed1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "baselineModelVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="model")
    def model(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "model"))

    @model.setter
    def model(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d461731db19c3233a887f3551735afe658ca79dbe8d9cb95126890e1f0561a6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "model", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsConversationModelConfig]:
        return typing.cast(typing.Optional[DialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsConversationModelConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsConversationModelConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__01a90ef6a90baf4dabd7834cbf978af25248cea0cd662c365df819c6638309f3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dialogflowConversationProfile.DialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsConversationProcessConfig",
    jsii_struct_bases=[],
    name_mapping={"recent_sentences_count": "recentSentencesCount"},
)
class DialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsConversationProcessConfig:
    def __init__(
        self,
        *,
        recent_sentences_count: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param recent_sentences_count: Number of recent non-small-talk sentences to use as context for article and FAQ suggestion. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#recent_sentences_count DialogflowConversationProfile#recent_sentences_count}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__575323893bb94b554e377420102aa75e9eab5c5595163fe2cf9da95053e1b1a1)
            check_type(argname="argument recent_sentences_count", value=recent_sentences_count, expected_type=type_hints["recent_sentences_count"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if recent_sentences_count is not None:
            self._values["recent_sentences_count"] = recent_sentences_count

    @builtins.property
    def recent_sentences_count(self) -> typing.Optional[jsii.Number]:
        '''Number of recent non-small-talk sentences to use as context for article and FAQ suggestion.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#recent_sentences_count DialogflowConversationProfile#recent_sentences_count}
        '''
        result = self._values.get("recent_sentences_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsConversationProcessConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsConversationProcessConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dialogflowConversationProfile.DialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsConversationProcessConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__57269fd26979ab08e4253dc4e67d4150d6e991d2f0aa34c3a7944163e82bf87a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8fbee899d477baac9594cf08e8c0516a1030af7a6f60c9a53f1696f871694c7d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "recentSentencesCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsConversationProcessConfig]:
        return typing.cast(typing.Optional[DialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsConversationProcessConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsConversationProcessConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd5eed4fa5b3578a583c61e3069c07777bccb74aabb93af392a968701eee7cac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dialogflowConversationProfile.DialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__754d0f1e4224f63e9b60943945c1f802104503ccf44a708a5848c48baff5fe92)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ce3396c026183c9dc6f49c39fe00816122680d84fe5a9f7435ed54529b1c49b)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__57e09be60b3732b37a2890dd0c2cef51bedc29b66fa3565abee94e2722a5b6b7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__38e8ead1389a03ecc9fe078d4fbfc4183e9e33436ce21a038cbcc8726257c331)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2f9ffe6895daa5b901a9692dac0cff03df0357c249aee0980298959861eb02cf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigs]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigs]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigs]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__477476bd0d10d6bb36ffa552f08246f2d7b40ce97da4f55d0141ba8efc40b643)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dialogflowConversationProfile.DialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a7a94c63328d767a443e125d3edd16db84b5247f23ac4afa73a3da5032cadd56)
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
        :param baseline_model_version: Version of current baseline model. It will be ignored if model is set. Valid versions are: Article Suggestion baseline model: - 0.9 - 1.0 (default) Summarization baseline model: - 1.0 Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#baseline_model_version DialogflowConversationProfile#baseline_model_version}
        :param model: Conversation model resource name. Format: projects//conversationModels/. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#model DialogflowConversationProfile#model}
        '''
        value = DialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsConversationModelConfig(
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
        :param recent_sentences_count: Number of recent non-small-talk sentences to use as context for article and FAQ suggestion. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#recent_sentences_count DialogflowConversationProfile#recent_sentences_count}
        '''
        value = DialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsConversationProcessConfig(
            recent_sentences_count=recent_sentences_count
        )

        return typing.cast(None, jsii.invoke(self, "putConversationProcessConfig", [value]))

    @jsii.member(jsii_name="putQueryConfig")
    def put_query_config(
        self,
        *,
        confidence_threshold: typing.Optional[jsii.Number] = None,
        context_filter_settings: typing.Optional[typing.Union["DialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsQueryConfigContextFilterSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        dialogflow_query_source: typing.Optional[typing.Union["DialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsQueryConfigDialogflowQuerySource", typing.Dict[builtins.str, typing.Any]]] = None,
        max_results: typing.Optional[jsii.Number] = None,
        sections: typing.Optional[typing.Union["DialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsQueryConfigSections", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param confidence_threshold: Confidence threshold of query result. This feature is only supported for types: ARTICLE_SUGGESTION, FAQ, SMART_REPLY, SMART_COMPOSE, KNOWLEDGE_SEARCH, KNOWLEDGE_ASSIST, ENTITY_EXTRACTION. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#confidence_threshold DialogflowConversationProfile#confidence_threshold}
        :param context_filter_settings: context_filter_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#context_filter_settings DialogflowConversationProfile#context_filter_settings}
        :param dialogflow_query_source: dialogflow_query_source block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#dialogflow_query_source DialogflowConversationProfile#dialogflow_query_source}
        :param max_results: Maximum number of results to return. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#max_results DialogflowConversationProfile#max_results}
        :param sections: sections block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#sections DialogflowConversationProfile#sections}
        '''
        value = DialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsQueryConfig(
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
        :param type: Type of Human Agent Assistant API feature to request. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#type DialogflowConversationProfile#type}
        '''
        value = DialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsSuggestionFeature(
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
        :param no_small_talk: Do not trigger if last utterance is small talk. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#no_small_talk DialogflowConversationProfile#no_small_talk}
        :param only_end_user: Only trigger suggestion if participant role of last utterance is END_USER. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#only_end_user DialogflowConversationProfile#only_end_user}
        '''
        value = DialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsSuggestionTriggerSettings(
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
    ) -> DialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsConversationModelConfigOutputReference:
        return typing.cast(DialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsConversationModelConfigOutputReference, jsii.get(self, "conversationModelConfig"))

    @builtins.property
    @jsii.member(jsii_name="conversationProcessConfig")
    def conversation_process_config(
        self,
    ) -> DialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsConversationProcessConfigOutputReference:
        return typing.cast(DialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsConversationProcessConfigOutputReference, jsii.get(self, "conversationProcessConfig"))

    @builtins.property
    @jsii.member(jsii_name="queryConfig")
    def query_config(
        self,
    ) -> "DialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsQueryConfigOutputReference":
        return typing.cast("DialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsQueryConfigOutputReference", jsii.get(self, "queryConfig"))

    @builtins.property
    @jsii.member(jsii_name="suggestionFeature")
    def suggestion_feature(
        self,
    ) -> "DialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsSuggestionFeatureOutputReference":
        return typing.cast("DialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsSuggestionFeatureOutputReference", jsii.get(self, "suggestionFeature"))

    @builtins.property
    @jsii.member(jsii_name="suggestionTriggerSettings")
    def suggestion_trigger_settings(
        self,
    ) -> "DialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsSuggestionTriggerSettingsOutputReference":
        return typing.cast("DialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsSuggestionTriggerSettingsOutputReference", jsii.get(self, "suggestionTriggerSettings"))

    @builtins.property
    @jsii.member(jsii_name="conversationModelConfigInput")
    def conversation_model_config_input(
        self,
    ) -> typing.Optional[DialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsConversationModelConfig]:
        return typing.cast(typing.Optional[DialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsConversationModelConfig], jsii.get(self, "conversationModelConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="conversationProcessConfigInput")
    def conversation_process_config_input(
        self,
    ) -> typing.Optional[DialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsConversationProcessConfig]:
        return typing.cast(typing.Optional[DialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsConversationProcessConfig], jsii.get(self, "conversationProcessConfigInput"))

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
    ) -> typing.Optional["DialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsQueryConfig"]:
        return typing.cast(typing.Optional["DialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsQueryConfig"], jsii.get(self, "queryConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="suggestionFeatureInput")
    def suggestion_feature_input(
        self,
    ) -> typing.Optional["DialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsSuggestionFeature"]:
        return typing.cast(typing.Optional["DialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsSuggestionFeature"], jsii.get(self, "suggestionFeatureInput"))

    @builtins.property
    @jsii.member(jsii_name="suggestionTriggerSettingsInput")
    def suggestion_trigger_settings_input(
        self,
    ) -> typing.Optional["DialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsSuggestionTriggerSettings"]:
        return typing.cast(typing.Optional["DialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsSuggestionTriggerSettings"], jsii.get(self, "suggestionTriggerSettingsInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__836dc9b8f25a682002e0c50b8174390558d3138f3e669aff5928e2f6cfe8ae38)
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
            type_hints = typing.get_type_hints(_typecheckingstub__065cb28d7713161b6a2149adcb6d0488f25cc2f50b2545102553d10e53ab56f6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__eb0bce5d5c067d823f50e573d2538887808dc778918b235b7ea2787321816324)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fc3716fa1d84ea9024929ae072877aa5446159fc0c1f910bc78921e5be00eec7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__03368f6d19e0bfa3cd1f29edade4d72a7d1ca4ca12a5de45ef024e47989ee007)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableQuerySuggestionWhenNoAnswer", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigs]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigs]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigs]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6697d3fea97ac17d953c70c15675bcdc9700a4c038ddd96b2040c9d0be73cdd5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dialogflowConversationProfile.DialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsQueryConfig",
    jsii_struct_bases=[],
    name_mapping={
        "confidence_threshold": "confidenceThreshold",
        "context_filter_settings": "contextFilterSettings",
        "dialogflow_query_source": "dialogflowQuerySource",
        "max_results": "maxResults",
        "sections": "sections",
    },
)
class DialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsQueryConfig:
    def __init__(
        self,
        *,
        confidence_threshold: typing.Optional[jsii.Number] = None,
        context_filter_settings: typing.Optional[typing.Union["DialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsQueryConfigContextFilterSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        dialogflow_query_source: typing.Optional[typing.Union["DialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsQueryConfigDialogflowQuerySource", typing.Dict[builtins.str, typing.Any]]] = None,
        max_results: typing.Optional[jsii.Number] = None,
        sections: typing.Optional[typing.Union["DialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsQueryConfigSections", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param confidence_threshold: Confidence threshold of query result. This feature is only supported for types: ARTICLE_SUGGESTION, FAQ, SMART_REPLY, SMART_COMPOSE, KNOWLEDGE_SEARCH, KNOWLEDGE_ASSIST, ENTITY_EXTRACTION. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#confidence_threshold DialogflowConversationProfile#confidence_threshold}
        :param context_filter_settings: context_filter_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#context_filter_settings DialogflowConversationProfile#context_filter_settings}
        :param dialogflow_query_source: dialogflow_query_source block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#dialogflow_query_source DialogflowConversationProfile#dialogflow_query_source}
        :param max_results: Maximum number of results to return. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#max_results DialogflowConversationProfile#max_results}
        :param sections: sections block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#sections DialogflowConversationProfile#sections}
        '''
        if isinstance(context_filter_settings, dict):
            context_filter_settings = DialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsQueryConfigContextFilterSettings(**context_filter_settings)
        if isinstance(dialogflow_query_source, dict):
            dialogflow_query_source = DialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsQueryConfigDialogflowQuerySource(**dialogflow_query_source)
        if isinstance(sections, dict):
            sections = DialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsQueryConfigSections(**sections)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__24aae5556c35e71f8fc0bc42976e06decff0cd528f170e2c74199a5b91433b7a)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#confidence_threshold DialogflowConversationProfile#confidence_threshold}
        '''
        result = self._values.get("confidence_threshold")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def context_filter_settings(
        self,
    ) -> typing.Optional["DialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsQueryConfigContextFilterSettings"]:
        '''context_filter_settings block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#context_filter_settings DialogflowConversationProfile#context_filter_settings}
        '''
        result = self._values.get("context_filter_settings")
        return typing.cast(typing.Optional["DialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsQueryConfigContextFilterSettings"], result)

    @builtins.property
    def dialogflow_query_source(
        self,
    ) -> typing.Optional["DialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsQueryConfigDialogflowQuerySource"]:
        '''dialogflow_query_source block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#dialogflow_query_source DialogflowConversationProfile#dialogflow_query_source}
        '''
        result = self._values.get("dialogflow_query_source")
        return typing.cast(typing.Optional["DialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsQueryConfigDialogflowQuerySource"], result)

    @builtins.property
    def max_results(self) -> typing.Optional[jsii.Number]:
        '''Maximum number of results to return.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#max_results DialogflowConversationProfile#max_results}
        '''
        result = self._values.get("max_results")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def sections(
        self,
    ) -> typing.Optional["DialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsQueryConfigSections"]:
        '''sections block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#sections DialogflowConversationProfile#sections}
        '''
        result = self._values.get("sections")
        return typing.cast(typing.Optional["DialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsQueryConfigSections"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsQueryConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dialogflowConversationProfile.DialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsQueryConfigContextFilterSettings",
    jsii_struct_bases=[],
    name_mapping={
        "drop_handoff_messages": "dropHandoffMessages",
        "drop_ivr_messages": "dropIvrMessages",
        "drop_virtual_agent_messages": "dropVirtualAgentMessages",
    },
)
class DialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsQueryConfigContextFilterSettings:
    def __init__(
        self,
        *,
        drop_handoff_messages: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        drop_ivr_messages: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        drop_virtual_agent_messages: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param drop_handoff_messages: If set to true, the last message from virtual agent (hand off message) and the message before it (trigger message of hand off) are dropped. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#drop_handoff_messages DialogflowConversationProfile#drop_handoff_messages}
        :param drop_ivr_messages: If set to true, all messages from ivr stage are dropped. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#drop_ivr_messages DialogflowConversationProfile#drop_ivr_messages}
        :param drop_virtual_agent_messages: If set to true, all messages from virtual agent are dropped. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#drop_virtual_agent_messages DialogflowConversationProfile#drop_virtual_agent_messages}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__685fa8c94180db89bff05f6d0baba2e8ae67c96b903638289d0c4d6b3d97ea3e)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#drop_handoff_messages DialogflowConversationProfile#drop_handoff_messages}
        '''
        result = self._values.get("drop_handoff_messages")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def drop_ivr_messages(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If set to true, all messages from ivr stage are dropped.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#drop_ivr_messages DialogflowConversationProfile#drop_ivr_messages}
        '''
        result = self._values.get("drop_ivr_messages")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def drop_virtual_agent_messages(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If set to true, all messages from virtual agent are dropped.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#drop_virtual_agent_messages DialogflowConversationProfile#drop_virtual_agent_messages}
        '''
        result = self._values.get("drop_virtual_agent_messages")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsQueryConfigContextFilterSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsQueryConfigContextFilterSettingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dialogflowConversationProfile.DialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsQueryConfigContextFilterSettingsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2e0e13f40014c3fc78337e4740be4651becafcda6af647c28218e245ea61336e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3209ad6ca6a5394f198ddef47d691b6e2c0da9fc790ae144cd4df18d494e9fe3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2941d36be524ce099e10f09988722fc3e33562cb3e4b389b597035ebfc4b7d4d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__390695a6b1ef743e9e639ffa9b80832b4ce6ba6dc4d4a2debe7e1a5d5e216ddb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dropVirtualAgentMessages", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsQueryConfigContextFilterSettings]:
        return typing.cast(typing.Optional[DialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsQueryConfigContextFilterSettings], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsQueryConfigContextFilterSettings],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c9a047e3b40e15cf96c71d848ed5f1af6d19b114ee621d68805a0a88d2b47abc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dialogflowConversationProfile.DialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsQueryConfigDialogflowQuerySource",
    jsii_struct_bases=[],
    name_mapping={"agent": "agent", "human_agent_side_config": "humanAgentSideConfig"},
)
class DialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsQueryConfigDialogflowQuerySource:
    def __init__(
        self,
        *,
        agent: builtins.str,
        human_agent_side_config: typing.Optional[typing.Union["DialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsQueryConfigDialogflowQuerySourceHumanAgentSideConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param agent: he name of a Dialogflow virtual agent used for end user side intent detection and suggestion. Format: projects//locations//agent. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#agent DialogflowConversationProfile#agent}
        :param human_agent_side_config: human_agent_side_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#human_agent_side_config DialogflowConversationProfile#human_agent_side_config}
        '''
        if isinstance(human_agent_side_config, dict):
            human_agent_side_config = DialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsQueryConfigDialogflowQuerySourceHumanAgentSideConfig(**human_agent_side_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d6404b902a74e5917de8e17855c42c90b4ac73ffe932544640b94e78aef2cebd)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#agent DialogflowConversationProfile#agent}
        '''
        result = self._values.get("agent")
        assert result is not None, "Required property 'agent' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def human_agent_side_config(
        self,
    ) -> typing.Optional["DialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsQueryConfigDialogflowQuerySourceHumanAgentSideConfig"]:
        '''human_agent_side_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#human_agent_side_config DialogflowConversationProfile#human_agent_side_config}
        '''
        result = self._values.get("human_agent_side_config")
        return typing.cast(typing.Optional["DialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsQueryConfigDialogflowQuerySourceHumanAgentSideConfig"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsQueryConfigDialogflowQuerySource(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dialogflowConversationProfile.DialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsQueryConfigDialogflowQuerySourceHumanAgentSideConfig",
    jsii_struct_bases=[],
    name_mapping={"agent": "agent"},
)
class DialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsQueryConfigDialogflowQuerySourceHumanAgentSideConfig:
    def __init__(self, *, agent: typing.Optional[builtins.str] = None) -> None:
        '''
        :param agent: The name of a dialogflow virtual agent used for intent detection and suggestion triggered by human agent. Format: projects//locations//agent. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#agent DialogflowConversationProfile#agent}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__448cb69feb94d1a7ff8211e1790bf2b8338a5a4bd6a8b7db6a3f263a68038bbd)
            check_type(argname="argument agent", value=agent, expected_type=type_hints["agent"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if agent is not None:
            self._values["agent"] = agent

    @builtins.property
    def agent(self) -> typing.Optional[builtins.str]:
        '''The name of a dialogflow virtual agent used for intent detection and suggestion triggered by human agent.

        Format: projects//locations//agent.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#agent DialogflowConversationProfile#agent}
        '''
        result = self._values.get("agent")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsQueryConfigDialogflowQuerySourceHumanAgentSideConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsQueryConfigDialogflowQuerySourceHumanAgentSideConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dialogflowConversationProfile.DialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsQueryConfigDialogflowQuerySourceHumanAgentSideConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b8270c2c3b05942dde0ac2accb9c5b9eb00a9b4703be002783323d6ec31556a7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a2a6f720966d2a48a4f9682fcf1f825781b8c8213dc0dce0caa7acf131b5a5da)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "agent", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsQueryConfigDialogflowQuerySourceHumanAgentSideConfig]:
        return typing.cast(typing.Optional[DialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsQueryConfigDialogflowQuerySourceHumanAgentSideConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsQueryConfigDialogflowQuerySourceHumanAgentSideConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e4dcc291b89b6987f3817049ea1e3ede39dcf044b4439d0729ce8668921dd2d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsQueryConfigDialogflowQuerySourceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dialogflowConversationProfile.DialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsQueryConfigDialogflowQuerySourceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0e8c19ae04a8e3139a27d3f0632aaf0e3c0c96c593913ff81f3b9426726f10ba)
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
        :param agent: The name of a dialogflow virtual agent used for intent detection and suggestion triggered by human agent. Format: projects//locations//agent. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#agent DialogflowConversationProfile#agent}
        '''
        value = DialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsQueryConfigDialogflowQuerySourceHumanAgentSideConfig(
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
    ) -> DialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsQueryConfigDialogflowQuerySourceHumanAgentSideConfigOutputReference:
        return typing.cast(DialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsQueryConfigDialogflowQuerySourceHumanAgentSideConfigOutputReference, jsii.get(self, "humanAgentSideConfig"))

    @builtins.property
    @jsii.member(jsii_name="agentInput")
    def agent_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "agentInput"))

    @builtins.property
    @jsii.member(jsii_name="humanAgentSideConfigInput")
    def human_agent_side_config_input(
        self,
    ) -> typing.Optional[DialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsQueryConfigDialogflowQuerySourceHumanAgentSideConfig]:
        return typing.cast(typing.Optional[DialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsQueryConfigDialogflowQuerySourceHumanAgentSideConfig], jsii.get(self, "humanAgentSideConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="agent")
    def agent(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "agent"))

    @agent.setter
    def agent(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d61a68514a1c9220d6bbddbacd0430566d1a2079be133ae01bd811c404586a8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "agent", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsQueryConfigDialogflowQuerySource]:
        return typing.cast(typing.Optional[DialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsQueryConfigDialogflowQuerySource], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsQueryConfigDialogflowQuerySource],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa1d1d23bc8080dae26e3d663c7f93a901f2a110a63f47c8c0d68fb9fc4e845c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsQueryConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dialogflowConversationProfile.DialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsQueryConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__492df00b618bd2c01c221aa74d3e1c027919575d2d428117ae6bd617809b3d6f)
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
        :param drop_handoff_messages: If set to true, the last message from virtual agent (hand off message) and the message before it (trigger message of hand off) are dropped. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#drop_handoff_messages DialogflowConversationProfile#drop_handoff_messages}
        :param drop_ivr_messages: If set to true, all messages from ivr stage are dropped. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#drop_ivr_messages DialogflowConversationProfile#drop_ivr_messages}
        :param drop_virtual_agent_messages: If set to true, all messages from virtual agent are dropped. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#drop_virtual_agent_messages DialogflowConversationProfile#drop_virtual_agent_messages}
        '''
        value = DialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsQueryConfigContextFilterSettings(
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
        human_agent_side_config: typing.Optional[typing.Union[DialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsQueryConfigDialogflowQuerySourceHumanAgentSideConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param agent: he name of a Dialogflow virtual agent used for end user side intent detection and suggestion. Format: projects//locations//agent. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#agent DialogflowConversationProfile#agent}
        :param human_agent_side_config: human_agent_side_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#human_agent_side_config DialogflowConversationProfile#human_agent_side_config}
        '''
        value = DialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsQueryConfigDialogflowQuerySource(
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
        :param section_types: The selected sections chosen to return when requesting a summary of a conversation If not provided the default selection will be "{SITUATION, ACTION, RESULT}". Possible values: ["SECTION_TYPE_UNSPECIFIED", "SITUATION", "ACTION", "RESOLUTION", "REASON_FOR_CANCELLATION", "CUSTOMER_SATISFACTION", "ENTITIES"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#section_types DialogflowConversationProfile#section_types}
        '''
        value = DialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsQueryConfigSections(
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
    ) -> DialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsQueryConfigContextFilterSettingsOutputReference:
        return typing.cast(DialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsQueryConfigContextFilterSettingsOutputReference, jsii.get(self, "contextFilterSettings"))

    @builtins.property
    @jsii.member(jsii_name="dialogflowQuerySource")
    def dialogflow_query_source(
        self,
    ) -> DialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsQueryConfigDialogflowQuerySourceOutputReference:
        return typing.cast(DialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsQueryConfigDialogflowQuerySourceOutputReference, jsii.get(self, "dialogflowQuerySource"))

    @builtins.property
    @jsii.member(jsii_name="sections")
    def sections(
        self,
    ) -> "DialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsQueryConfigSectionsOutputReference":
        return typing.cast("DialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsQueryConfigSectionsOutputReference", jsii.get(self, "sections"))

    @builtins.property
    @jsii.member(jsii_name="confidenceThresholdInput")
    def confidence_threshold_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "confidenceThresholdInput"))

    @builtins.property
    @jsii.member(jsii_name="contextFilterSettingsInput")
    def context_filter_settings_input(
        self,
    ) -> typing.Optional[DialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsQueryConfigContextFilterSettings]:
        return typing.cast(typing.Optional[DialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsQueryConfigContextFilterSettings], jsii.get(self, "contextFilterSettingsInput"))

    @builtins.property
    @jsii.member(jsii_name="dialogflowQuerySourceInput")
    def dialogflow_query_source_input(
        self,
    ) -> typing.Optional[DialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsQueryConfigDialogflowQuerySource]:
        return typing.cast(typing.Optional[DialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsQueryConfigDialogflowQuerySource], jsii.get(self, "dialogflowQuerySourceInput"))

    @builtins.property
    @jsii.member(jsii_name="maxResultsInput")
    def max_results_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxResultsInput"))

    @builtins.property
    @jsii.member(jsii_name="sectionsInput")
    def sections_input(
        self,
    ) -> typing.Optional["DialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsQueryConfigSections"]:
        return typing.cast(typing.Optional["DialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsQueryConfigSections"], jsii.get(self, "sectionsInput"))

    @builtins.property
    @jsii.member(jsii_name="confidenceThreshold")
    def confidence_threshold(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "confidenceThreshold"))

    @confidence_threshold.setter
    def confidence_threshold(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4510f4a1187fbba7e3f4657d7a62d8bdc63a0df2ac1d19e762c2b305e3bca092)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "confidenceThreshold", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxResults")
    def max_results(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxResults"))

    @max_results.setter
    def max_results(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e2d2206a6143ea9b7ad6b40dae0fa39dd2358640d64ec169daceee9da2c0d81b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxResults", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsQueryConfig]:
        return typing.cast(typing.Optional[DialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsQueryConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsQueryConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__84085d37a00aeb1fa8321339c02e0cf08630b695d74d089535e6775f85910527)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dialogflowConversationProfile.DialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsQueryConfigSections",
    jsii_struct_bases=[],
    name_mapping={"section_types": "sectionTypes"},
)
class DialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsQueryConfigSections:
    def __init__(
        self,
        *,
        section_types: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param section_types: The selected sections chosen to return when requesting a summary of a conversation If not provided the default selection will be "{SITUATION, ACTION, RESULT}". Possible values: ["SECTION_TYPE_UNSPECIFIED", "SITUATION", "ACTION", "RESOLUTION", "REASON_FOR_CANCELLATION", "CUSTOMER_SATISFACTION", "ENTITIES"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#section_types DialogflowConversationProfile#section_types}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__69a657bb6dbe582fe73d8146ff800cb3cca2262847118288660e8e4e467df401)
            check_type(argname="argument section_types", value=section_types, expected_type=type_hints["section_types"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if section_types is not None:
            self._values["section_types"] = section_types

    @builtins.property
    def section_types(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The selected sections chosen to return when requesting a summary of a conversation If not provided the default selection will be "{SITUATION, ACTION, RESULT}".

        Possible values: ["SECTION_TYPE_UNSPECIFIED", "SITUATION", "ACTION", "RESOLUTION", "REASON_FOR_CANCELLATION", "CUSTOMER_SATISFACTION", "ENTITIES"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#section_types DialogflowConversationProfile#section_types}
        '''
        result = self._values.get("section_types")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsQueryConfigSections(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsQueryConfigSectionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dialogflowConversationProfile.DialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsQueryConfigSectionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__160b7d308cc07dc0f66d39bd844a62c6973d82d91dcdee500fed83d4cfed0f83)
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
            type_hints = typing.get_type_hints(_typecheckingstub__96a7cf3a6bf19b9e9f9cd77f5eaeadb269473fc738147bf7bcdc18c33b2309fe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sectionTypes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsQueryConfigSections]:
        return typing.cast(typing.Optional[DialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsQueryConfigSections], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsQueryConfigSections],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f6414d72c645b585d6eca83240a48d5373674d0c09ced7e7fa0ea9caa7502c16)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dialogflowConversationProfile.DialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsSuggestionFeature",
    jsii_struct_bases=[],
    name_mapping={"type": "type"},
)
class DialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsSuggestionFeature:
    def __init__(self, *, type: typing.Optional[builtins.str] = None) -> None:
        '''
        :param type: Type of Human Agent Assistant API feature to request. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#type DialogflowConversationProfile#type}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__672d5129f4cfc70fe1c7a8fd9f03d80ceb5cac7b2ede6180acec017bb45f419e)
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if type is not None:
            self._values["type"] = type

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''Type of Human Agent Assistant API feature to request.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#type DialogflowConversationProfile#type}
        '''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsSuggestionFeature(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsSuggestionFeatureOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dialogflowConversationProfile.DialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsSuggestionFeatureOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__13d4f882daeb49cff11615f81a59d2f219b32aec31965fa3ab92caec7ecf133b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c902835767d33fe09eae98c12378cd3c83d830eb32e8610b5ddf5a9303bf57ed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsSuggestionFeature]:
        return typing.cast(typing.Optional[DialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsSuggestionFeature], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsSuggestionFeature],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8eef322461609cb342a114316922cc6916cb47d88d5f9f33643844e72d985156)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dialogflowConversationProfile.DialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsSuggestionTriggerSettings",
    jsii_struct_bases=[],
    name_mapping={"no_small_talk": "noSmallTalk", "only_end_user": "onlyEndUser"},
)
class DialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsSuggestionTriggerSettings:
    def __init__(
        self,
        *,
        no_small_talk: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        only_end_user: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param no_small_talk: Do not trigger if last utterance is small talk. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#no_small_talk DialogflowConversationProfile#no_small_talk}
        :param only_end_user: Only trigger suggestion if participant role of last utterance is END_USER. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#only_end_user DialogflowConversationProfile#only_end_user}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c2df082c67c60f29f6f0dc741633d93d6148412e1e261df65dde8205fd7e0e3)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#no_small_talk DialogflowConversationProfile#no_small_talk}
        '''
        result = self._values.get("no_small_talk")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def only_end_user(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Only trigger suggestion if participant role of last utterance is END_USER.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#only_end_user DialogflowConversationProfile#only_end_user}
        '''
        result = self._values.get("only_end_user")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsSuggestionTriggerSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsSuggestionTriggerSettingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dialogflowConversationProfile.DialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsSuggestionTriggerSettingsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6ca4e0a801df1c57ad264d0a79c5cea12e872b5fa4f5dc7704ab7fa4e3065106)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c4fd019f908e5f78360052882645ba8f48aab891a22eb5f6eb4857663a138b69)
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
            type_hints = typing.get_type_hints(_typecheckingstub__aadb359ac692b09bcc8d5318868503eec7e596a2f7e91d139cfdc5b62be6c8cd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "onlyEndUser", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsSuggestionTriggerSettings]:
        return typing.cast(typing.Optional[DialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsSuggestionTriggerSettings], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsSuggestionTriggerSettings],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4516a58088bec16db7b93679a1d84e8e6a7f591b4590f3afaf9e4357834afbf6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dialogflowConversationProfile.DialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f73d45cee9563d132676528fd325bf4bff803188d495e08e3517be6d7021c073)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putFeatureConfigs")
    def put_feature_configs(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigs, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1dc6fdc3b840a2bf31b7fdab282ba8361b5a4c02ffab5506e74b67793efb0c0a)
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
    ) -> DialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsList:
        return typing.cast(DialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsList, jsii.get(self, "featureConfigs"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigs]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigs]]], jsii.get(self, "featureConfigsInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__703ac7fb83c5dec1956e80c580d9a4420232e2b6a709d9ead925dba32f0386ba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "disableHighLatencyFeaturesSyncDelivery", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="generators")
    def generators(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "generators"))

    @generators.setter
    def generators(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d572236e82eb73fcf8712951ab7b5a5bd26cfd415ef32f9d1a8163899ed7a11)
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
            type_hints = typing.get_type_hints(_typecheckingstub__06b8cb90fc1742d859a958b9ec81ed15e89ac3c27e8ed941196daa80f6e1937e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "groupSuggestionResponses", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfig]:
        return typing.cast(typing.Optional[DialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c895ee95a39cead6b27218d1614855c5b6a480e107de62426fec3ec715cdf293)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dialogflowConversationProfile.DialogflowConversationProfileHumanAgentAssistantConfigMessageAnalysisConfig",
    jsii_struct_bases=[],
    name_mapping={
        "enable_entity_extraction": "enableEntityExtraction",
        "enable_sentiment_analysis": "enableSentimentAnalysis",
    },
)
class DialogflowConversationProfileHumanAgentAssistantConfigMessageAnalysisConfig:
    def __init__(
        self,
        *,
        enable_entity_extraction: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_sentiment_analysis: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param enable_entity_extraction: Enable entity extraction in conversation messages on agent assist stage. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#enable_entity_extraction DialogflowConversationProfile#enable_entity_extraction}
        :param enable_sentiment_analysis: Enable sentiment analysis in conversation messages on agent assist stage. Sentiment analysis inspects user input and identifies the prevailing subjective opinion, especially to determine a user's attitude as positive, negative, or neutral. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#enable_sentiment_analysis DialogflowConversationProfile#enable_sentiment_analysis}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6fe83ce3d3c33b6c87595f27a2515f0c44ab6c927adc78c4d486a53e13f9bd72)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#enable_entity_extraction DialogflowConversationProfile#enable_entity_extraction}
        '''
        result = self._values.get("enable_entity_extraction")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def enable_sentiment_analysis(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Enable sentiment analysis in conversation messages on agent assist stage.

        Sentiment analysis inspects user input and identifies the prevailing subjective opinion, especially to determine a user's attitude as positive, negative, or neutral.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#enable_sentiment_analysis DialogflowConversationProfile#enable_sentiment_analysis}
        '''
        result = self._values.get("enable_sentiment_analysis")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DialogflowConversationProfileHumanAgentAssistantConfigMessageAnalysisConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DialogflowConversationProfileHumanAgentAssistantConfigMessageAnalysisConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dialogflowConversationProfile.DialogflowConversationProfileHumanAgentAssistantConfigMessageAnalysisConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__cdd3b76fedd86dac4161af2858930ad8dfa2a43f64d15a2ffb423b51237c5356)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bb13b1cbf201e5e385731cd87e0a21012e3b3f37000d2f898a0c87cda39236b7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2b32e654fff239f381127d6abdc87bed55663c4df97639a5d0375f8c111d957c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableSentimentAnalysis", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DialogflowConversationProfileHumanAgentAssistantConfigMessageAnalysisConfig]:
        return typing.cast(typing.Optional[DialogflowConversationProfileHumanAgentAssistantConfigMessageAnalysisConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DialogflowConversationProfileHumanAgentAssistantConfigMessageAnalysisConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__227c733dec493262fe6ad96d3c67bb6ee911cea84c26627de3c93da91f8a3c86)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dialogflowConversationProfile.DialogflowConversationProfileHumanAgentAssistantConfigNotificationConfig",
    jsii_struct_bases=[],
    name_mapping={"message_format": "messageFormat", "topic": "topic"},
)
class DialogflowConversationProfileHumanAgentAssistantConfigNotificationConfig:
    def __init__(
        self,
        *,
        message_format: typing.Optional[builtins.str] = None,
        topic: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param message_format: Format of the message Possible values: ["MESSAGE_FORMAT_UNSPECIFIED", "PROTO", "JSON"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#message_format DialogflowConversationProfile#message_format}
        :param topic: Name of the Pub/Sub topic to publish conversation events. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#topic DialogflowConversationProfile#topic}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__763cf6b26cc1f09d4c3adbf3824bc8cf5416899079db93159d51ea3b3e31493c)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#message_format DialogflowConversationProfile#message_format}
        '''
        result = self._values.get("message_format")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def topic(self) -> typing.Optional[builtins.str]:
        '''Name of the Pub/Sub topic to publish conversation events.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#topic DialogflowConversationProfile#topic}
        '''
        result = self._values.get("topic")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DialogflowConversationProfileHumanAgentAssistantConfigNotificationConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DialogflowConversationProfileHumanAgentAssistantConfigNotificationConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dialogflowConversationProfile.DialogflowConversationProfileHumanAgentAssistantConfigNotificationConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f23e1a1f97f8ea9a0e6dc7c38051b9b73e55b386b986b0708b665509ffbcf7e1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__215a256f5b7413024624bc17665dbf734ebf896227c2f79f76e8f248b4736d96)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "messageFormat", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="topic")
    def topic(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "topic"))

    @topic.setter
    def topic(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9564dfe5c1ae005f0b6d9297226acf0c016a53cf128b49b02febce5c842d6f0c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "topic", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DialogflowConversationProfileHumanAgentAssistantConfigNotificationConfig]:
        return typing.cast(typing.Optional[DialogflowConversationProfileHumanAgentAssistantConfigNotificationConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DialogflowConversationProfileHumanAgentAssistantConfigNotificationConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f8b0464aa544d4f2840b686d7ac32716679102d91f5e51c71db6cb2084765228)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DialogflowConversationProfileHumanAgentAssistantConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dialogflowConversationProfile.DialogflowConversationProfileHumanAgentAssistantConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2621fb08aa44a2a5c55bc652317d6a11b5ea10dc44672ab90260b8a7112d76e6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putEndUserSuggestionConfig")
    def put_end_user_suggestion_config(
        self,
        *,
        disable_high_latency_features_sync_delivery: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        feature_configs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigs, typing.Dict[builtins.str, typing.Any]]]]] = None,
        generators: typing.Optional[typing.Sequence[builtins.str]] = None,
        group_suggestion_responses: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param disable_high_latency_features_sync_delivery: When disableHighLatencyFeaturesSyncDelivery is true and using the AnalyzeContent API, we will not deliver the responses from high latency features in the API response. The humanAgentAssistantConfig.notification_config must be configured and enableEventBasedSuggestion must be set to true to receive the responses from high latency features in Pub/Sub. High latency feature(s): KNOWLEDGE_ASSIST Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#disable_high_latency_features_sync_delivery DialogflowConversationProfile#disable_high_latency_features_sync_delivery}
        :param feature_configs: feature_configs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#feature_configs DialogflowConversationProfile#feature_configs}
        :param generators: List of various generator resource names used in the conversation profile. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#generators DialogflowConversationProfile#generators}
        :param group_suggestion_responses: If groupSuggestionResponses is false, and there are multiple featureConfigs in event based suggestion or StreamingAnalyzeContent, we will try to deliver suggestions to customers as soon as we get new suggestion. Different type of suggestions based on the same context will be in separate Pub/Sub event or StreamingAnalyzeContentResponse. If groupSuggestionResponses set to true. All the suggestions to the same participant based on the same context will be grouped into a single Pub/Sub event or StreamingAnalyzeContentResponse. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#group_suggestion_responses DialogflowConversationProfile#group_suggestion_responses}
        '''
        value = DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfig(
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
        feature_configs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigs, typing.Dict[builtins.str, typing.Any]]]]] = None,
        generators: typing.Optional[typing.Sequence[builtins.str]] = None,
        group_suggestion_responses: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param disable_high_latency_features_sync_delivery: When disableHighLatencyFeaturesSyncDelivery is true and using the AnalyzeContent API, we will not deliver the responses from high latency features in the API response. The humanAgentAssistantConfig.notification_config must be configured and enableEventBasedSuggestion must be set to true to receive the responses from high latency features in Pub/Sub. High latency feature(s): KNOWLEDGE_ASSIST Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#disable_high_latency_features_sync_delivery DialogflowConversationProfile#disable_high_latency_features_sync_delivery}
        :param feature_configs: feature_configs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#feature_configs DialogflowConversationProfile#feature_configs}
        :param generators: List of various generator resource names used in the conversation profile. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#generators DialogflowConversationProfile#generators}
        :param group_suggestion_responses: If groupSuggestionResponses is false, and there are multiple featureConfigs in event based suggestion or StreamingAnalyzeContent, we will try to deliver suggestions to customers as soon as we get new suggestion. Different type of suggestions based on the same context will be in separate Pub/Sub event or StreamingAnalyzeContentResponse. If groupSuggestionResponses set to true. All the suggestions to the same participant based on the same context will be grouped into a single Pub/Sub event or StreamingAnalyzeContentResponse. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#group_suggestion_responses DialogflowConversationProfile#group_suggestion_responses}
        '''
        value = DialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfig(
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
        :param enable_entity_extraction: Enable entity extraction in conversation messages on agent assist stage. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#enable_entity_extraction DialogflowConversationProfile#enable_entity_extraction}
        :param enable_sentiment_analysis: Enable sentiment analysis in conversation messages on agent assist stage. Sentiment analysis inspects user input and identifies the prevailing subjective opinion, especially to determine a user's attitude as positive, negative, or neutral. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#enable_sentiment_analysis DialogflowConversationProfile#enable_sentiment_analysis}
        '''
        value = DialogflowConversationProfileHumanAgentAssistantConfigMessageAnalysisConfig(
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
        :param message_format: Format of the message Possible values: ["MESSAGE_FORMAT_UNSPECIFIED", "PROTO", "JSON"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#message_format DialogflowConversationProfile#message_format}
        :param topic: Name of the Pub/Sub topic to publish conversation events. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#topic DialogflowConversationProfile#topic}
        '''
        value = DialogflowConversationProfileHumanAgentAssistantConfigNotificationConfig(
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
    ) -> DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigOutputReference:
        return typing.cast(DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigOutputReference, jsii.get(self, "endUserSuggestionConfig"))

    @builtins.property
    @jsii.member(jsii_name="humanAgentSuggestionConfig")
    def human_agent_suggestion_config(
        self,
    ) -> DialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigOutputReference:
        return typing.cast(DialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigOutputReference, jsii.get(self, "humanAgentSuggestionConfig"))

    @builtins.property
    @jsii.member(jsii_name="messageAnalysisConfig")
    def message_analysis_config(
        self,
    ) -> DialogflowConversationProfileHumanAgentAssistantConfigMessageAnalysisConfigOutputReference:
        return typing.cast(DialogflowConversationProfileHumanAgentAssistantConfigMessageAnalysisConfigOutputReference, jsii.get(self, "messageAnalysisConfig"))

    @builtins.property
    @jsii.member(jsii_name="notificationConfig")
    def notification_config(
        self,
    ) -> DialogflowConversationProfileHumanAgentAssistantConfigNotificationConfigOutputReference:
        return typing.cast(DialogflowConversationProfileHumanAgentAssistantConfigNotificationConfigOutputReference, jsii.get(self, "notificationConfig"))

    @builtins.property
    @jsii.member(jsii_name="endUserSuggestionConfigInput")
    def end_user_suggestion_config_input(
        self,
    ) -> typing.Optional[DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfig]:
        return typing.cast(typing.Optional[DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfig], jsii.get(self, "endUserSuggestionConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="humanAgentSuggestionConfigInput")
    def human_agent_suggestion_config_input(
        self,
    ) -> typing.Optional[DialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfig]:
        return typing.cast(typing.Optional[DialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfig], jsii.get(self, "humanAgentSuggestionConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="messageAnalysisConfigInput")
    def message_analysis_config_input(
        self,
    ) -> typing.Optional[DialogflowConversationProfileHumanAgentAssistantConfigMessageAnalysisConfig]:
        return typing.cast(typing.Optional[DialogflowConversationProfileHumanAgentAssistantConfigMessageAnalysisConfig], jsii.get(self, "messageAnalysisConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="notificationConfigInput")
    def notification_config_input(
        self,
    ) -> typing.Optional[DialogflowConversationProfileHumanAgentAssistantConfigNotificationConfig]:
        return typing.cast(typing.Optional[DialogflowConversationProfileHumanAgentAssistantConfigNotificationConfig], jsii.get(self, "notificationConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DialogflowConversationProfileHumanAgentAssistantConfig]:
        return typing.cast(typing.Optional[DialogflowConversationProfileHumanAgentAssistantConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DialogflowConversationProfileHumanAgentAssistantConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d935258d610bf5be37e172e138f2355dff634fb24f608b0d68ecd0a042a01c0c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dialogflowConversationProfile.DialogflowConversationProfileHumanAgentHandoffConfig",
    jsii_struct_bases=[],
    name_mapping={"live_person_config": "livePersonConfig"},
)
class DialogflowConversationProfileHumanAgentHandoffConfig:
    def __init__(
        self,
        *,
        live_person_config: typing.Optional[typing.Union["DialogflowConversationProfileHumanAgentHandoffConfigLivePersonConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param live_person_config: live_person_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#live_person_config DialogflowConversationProfile#live_person_config}
        '''
        if isinstance(live_person_config, dict):
            live_person_config = DialogflowConversationProfileHumanAgentHandoffConfigLivePersonConfig(**live_person_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1718f9257fd95311000a2765c65ee0aeeff2863e4dc9dc75a8d8a2b340f6de04)
            check_type(argname="argument live_person_config", value=live_person_config, expected_type=type_hints["live_person_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if live_person_config is not None:
            self._values["live_person_config"] = live_person_config

    @builtins.property
    def live_person_config(
        self,
    ) -> typing.Optional["DialogflowConversationProfileHumanAgentHandoffConfigLivePersonConfig"]:
        '''live_person_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#live_person_config DialogflowConversationProfile#live_person_config}
        '''
        result = self._values.get("live_person_config")
        return typing.cast(typing.Optional["DialogflowConversationProfileHumanAgentHandoffConfigLivePersonConfig"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DialogflowConversationProfileHumanAgentHandoffConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dialogflowConversationProfile.DialogflowConversationProfileHumanAgentHandoffConfigLivePersonConfig",
    jsii_struct_bases=[],
    name_mapping={"account_number": "accountNumber"},
)
class DialogflowConversationProfileHumanAgentHandoffConfigLivePersonConfig:
    def __init__(self, *, account_number: builtins.str) -> None:
        '''
        :param account_number: Account number of the LivePerson account to connect. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#account_number DialogflowConversationProfile#account_number}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__599ab865f51960f1a47595f149cde9e8ca29b1f67e45c2c1169fa67f25d4c528)
            check_type(argname="argument account_number", value=account_number, expected_type=type_hints["account_number"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "account_number": account_number,
        }

    @builtins.property
    def account_number(self) -> builtins.str:
        '''Account number of the LivePerson account to connect.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#account_number DialogflowConversationProfile#account_number}
        '''
        result = self._values.get("account_number")
        assert result is not None, "Required property 'account_number' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DialogflowConversationProfileHumanAgentHandoffConfigLivePersonConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DialogflowConversationProfileHumanAgentHandoffConfigLivePersonConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dialogflowConversationProfile.DialogflowConversationProfileHumanAgentHandoffConfigLivePersonConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5d5b8af5274fd64f970a256a050eccaa6e69aa362588535fb93c19577f132b32)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2c0ac30f66fd213776951683b936b7eb3737ba21dcde88ae312874f8e3c81121)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accountNumber", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DialogflowConversationProfileHumanAgentHandoffConfigLivePersonConfig]:
        return typing.cast(typing.Optional[DialogflowConversationProfileHumanAgentHandoffConfigLivePersonConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DialogflowConversationProfileHumanAgentHandoffConfigLivePersonConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e9f2813797a8000a7db55caca0b7366f8c7ea8c674e96d31850f144dc7efee3e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DialogflowConversationProfileHumanAgentHandoffConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dialogflowConversationProfile.DialogflowConversationProfileHumanAgentHandoffConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__77f8cc7fa00f202bb5de276ee6f80801e44521a1a7a290d4d1aea0f16ae49655)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putLivePersonConfig")
    def put_live_person_config(self, *, account_number: builtins.str) -> None:
        '''
        :param account_number: Account number of the LivePerson account to connect. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#account_number DialogflowConversationProfile#account_number}
        '''
        value = DialogflowConversationProfileHumanAgentHandoffConfigLivePersonConfig(
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
    ) -> DialogflowConversationProfileHumanAgentHandoffConfigLivePersonConfigOutputReference:
        return typing.cast(DialogflowConversationProfileHumanAgentHandoffConfigLivePersonConfigOutputReference, jsii.get(self, "livePersonConfig"))

    @builtins.property
    @jsii.member(jsii_name="livePersonConfigInput")
    def live_person_config_input(
        self,
    ) -> typing.Optional[DialogflowConversationProfileHumanAgentHandoffConfigLivePersonConfig]:
        return typing.cast(typing.Optional[DialogflowConversationProfileHumanAgentHandoffConfigLivePersonConfig], jsii.get(self, "livePersonConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DialogflowConversationProfileHumanAgentHandoffConfig]:
        return typing.cast(typing.Optional[DialogflowConversationProfileHumanAgentHandoffConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DialogflowConversationProfileHumanAgentHandoffConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4d103d403f202002960b562e12e00009b7e04d1d8b711bdabf65bf5115e96812)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dialogflowConversationProfile.DialogflowConversationProfileLoggingConfig",
    jsii_struct_bases=[],
    name_mapping={"enable_stackdriver_logging": "enableStackdriverLogging"},
)
class DialogflowConversationProfileLoggingConfig:
    def __init__(
        self,
        *,
        enable_stackdriver_logging: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param enable_stackdriver_logging: Whether to log conversation events. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#enable_stackdriver_logging DialogflowConversationProfile#enable_stackdriver_logging}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a582142a5689c0d07833ac9313df508e76bdf5ace685b3cf4f1bbb5ed66f19fb)
            check_type(argname="argument enable_stackdriver_logging", value=enable_stackdriver_logging, expected_type=type_hints["enable_stackdriver_logging"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if enable_stackdriver_logging is not None:
            self._values["enable_stackdriver_logging"] = enable_stackdriver_logging

    @builtins.property
    def enable_stackdriver_logging(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether to log conversation events.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#enable_stackdriver_logging DialogflowConversationProfile#enable_stackdriver_logging}
        '''
        result = self._values.get("enable_stackdriver_logging")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DialogflowConversationProfileLoggingConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DialogflowConversationProfileLoggingConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dialogflowConversationProfile.DialogflowConversationProfileLoggingConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3983d54419a9ab79f51c84a92bd13a170c6aedd8f2d0eb96ba397262cd8e45a5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__499ad5552c3c602d4b93b1a425ed7ce19b21abe20d6f2bfce198ea5b88d0b12f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableStackdriverLogging", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DialogflowConversationProfileLoggingConfig]:
        return typing.cast(typing.Optional[DialogflowConversationProfileLoggingConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DialogflowConversationProfileLoggingConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d2142a034903fb450d77769f0bb392e23137315ee429c8294eed7b5b85679d6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dialogflowConversationProfile.DialogflowConversationProfileNewMessageEventNotificationConfig",
    jsii_struct_bases=[],
    name_mapping={"message_format": "messageFormat", "topic": "topic"},
)
class DialogflowConversationProfileNewMessageEventNotificationConfig:
    def __init__(
        self,
        *,
        message_format: typing.Optional[builtins.str] = None,
        topic: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param message_format: Format of the message Possible values: ["MESSAGE_FORMAT_UNSPECIFIED", "PROTO", "JSON"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#message_format DialogflowConversationProfile#message_format}
        :param topic: Name of the Pub/Sub topic to publish conversation events. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#topic DialogflowConversationProfile#topic}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__64ed90dd7ffd8a247c438b40f61040c92e56f130f44469a967082a36d946ee98)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#message_format DialogflowConversationProfile#message_format}
        '''
        result = self._values.get("message_format")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def topic(self) -> typing.Optional[builtins.str]:
        '''Name of the Pub/Sub topic to publish conversation events.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#topic DialogflowConversationProfile#topic}
        '''
        result = self._values.get("topic")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DialogflowConversationProfileNewMessageEventNotificationConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DialogflowConversationProfileNewMessageEventNotificationConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dialogflowConversationProfile.DialogflowConversationProfileNewMessageEventNotificationConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f3ee71bdec52f86a59d3744a5fe46148fc429e02e33597b8da5e82df775d0d1c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__724d7497ed764c66e2477940ffaae97e2008c023e75067d0ae79ff8e36f2e58d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "messageFormat", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="topic")
    def topic(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "topic"))

    @topic.setter
    def topic(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__107961b46feb26c8aa167ef5a8179fe49885f9335fd3cd56a73a80ff9ad64a26)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "topic", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DialogflowConversationProfileNewMessageEventNotificationConfig]:
        return typing.cast(typing.Optional[DialogflowConversationProfileNewMessageEventNotificationConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DialogflowConversationProfileNewMessageEventNotificationConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac8168c02680146ea3dabee544892b1439168e79efb8492d655883064755f7e3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dialogflowConversationProfile.DialogflowConversationProfileNotificationConfig",
    jsii_struct_bases=[],
    name_mapping={"message_format": "messageFormat", "topic": "topic"},
)
class DialogflowConversationProfileNotificationConfig:
    def __init__(
        self,
        *,
        message_format: typing.Optional[builtins.str] = None,
        topic: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param message_format: Format of the message Possible values: ["MESSAGE_FORMAT_UNSPECIFIED", "PROTO", "JSON"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#message_format DialogflowConversationProfile#message_format}
        :param topic: Name of the Pub/Sub topic to publish conversation events. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#topic DialogflowConversationProfile#topic}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__000f258ac2daa600b135933b614262c19f4e525864b43f5dbabb915a8cfa8c3c)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#message_format DialogflowConversationProfile#message_format}
        '''
        result = self._values.get("message_format")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def topic(self) -> typing.Optional[builtins.str]:
        '''Name of the Pub/Sub topic to publish conversation events.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#topic DialogflowConversationProfile#topic}
        '''
        result = self._values.get("topic")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DialogflowConversationProfileNotificationConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DialogflowConversationProfileNotificationConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dialogflowConversationProfile.DialogflowConversationProfileNotificationConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c7fb62f520fc8c276d9737ebef0402df85579b92aa6f8b798997ed3418d6e36b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f69de11bfd5528b40438d9588e5f20bc84972bb25c49f3ff4c39a507ca05f656)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "messageFormat", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="topic")
    def topic(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "topic"))

    @topic.setter
    def topic(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3aacbcf79a349e9b07d40eeeff3b4bf2b013456a8389ee66693c8d51ecd843d7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "topic", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DialogflowConversationProfileNotificationConfig]:
        return typing.cast(typing.Optional[DialogflowConversationProfileNotificationConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DialogflowConversationProfileNotificationConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7fecd7178ff795cacdca15963bfde5abace3969b53f308456cbe0562e46ee737)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dialogflowConversationProfile.DialogflowConversationProfileSttConfig",
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
class DialogflowConversationProfileSttConfig:
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
        :param audio_encoding: Audio encoding of the audio content to process. Possible values: ["AUDIO_ENCODING_UNSPECIFIED", "AUDIO_ENCODING_LINEAR_16", "AUDIO_ENCODING_FLAC", "AUDIO_ENCODING_MULAW", "AUDIO_ENCODING_AMR", "AUDIO_ENCODING_AMR_WB", "AUDIO_ENCODING_OGG_OPUS", "AUDIOENCODING_SPEEX_WITH_HEADER_BYTE"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#audio_encoding DialogflowConversationProfile#audio_encoding}
        :param enable_word_info: If true, Dialogflow returns SpeechWordInfo in StreamingRecognitionResult with information about the recognized speech words. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#enable_word_info DialogflowConversationProfile#enable_word_info}
        :param language_code: The language of the supplied audio. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#language_code DialogflowConversationProfile#language_code}
        :param model: Which Speech model to select. Leave this field unspecified to use Agent Speech settings for model selection. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#model DialogflowConversationProfile#model}
        :param sample_rate_hertz: Sample rate (in Hertz) of the audio content sent in the query. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#sample_rate_hertz DialogflowConversationProfile#sample_rate_hertz}
        :param speech_model_variant: The speech model used in speech to text. Possible values: ["SPEECH_MODEL_VARIANT_UNSPECIFIED", "USE_BEST_AVAILABLE", "USE_STANDARD", "USE_ENHANCED"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#speech_model_variant DialogflowConversationProfile#speech_model_variant}
        :param use_timeout_based_endpointing: Use timeout based endpointing, interpreting endpointer sensitivy as seconds of timeout value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#use_timeout_based_endpointing DialogflowConversationProfile#use_timeout_based_endpointing}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d92564e6830d40dc3576e0b4d04825ac6f699a457e4cce727d2918feeec2571)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#audio_encoding DialogflowConversationProfile#audio_encoding}
        '''
        result = self._values.get("audio_encoding")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enable_word_info(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If true, Dialogflow returns SpeechWordInfo in StreamingRecognitionResult with information about the recognized speech words.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#enable_word_info DialogflowConversationProfile#enable_word_info}
        '''
        result = self._values.get("enable_word_info")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def language_code(self) -> typing.Optional[builtins.str]:
        '''The language of the supplied audio.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#language_code DialogflowConversationProfile#language_code}
        '''
        result = self._values.get("language_code")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def model(self) -> typing.Optional[builtins.str]:
        '''Which Speech model to select. Leave this field unspecified to use Agent Speech settings for model selection.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#model DialogflowConversationProfile#model}
        '''
        result = self._values.get("model")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sample_rate_hertz(self) -> typing.Optional[jsii.Number]:
        '''Sample rate (in Hertz) of the audio content sent in the query.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#sample_rate_hertz DialogflowConversationProfile#sample_rate_hertz}
        '''
        result = self._values.get("sample_rate_hertz")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def speech_model_variant(self) -> typing.Optional[builtins.str]:
        '''The speech model used in speech to text. Possible values: ["SPEECH_MODEL_VARIANT_UNSPECIFIED", "USE_BEST_AVAILABLE", "USE_STANDARD", "USE_ENHANCED"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#speech_model_variant DialogflowConversationProfile#speech_model_variant}
        '''
        result = self._values.get("speech_model_variant")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def use_timeout_based_endpointing(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Use timeout based endpointing, interpreting endpointer sensitivy as seconds of timeout value.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#use_timeout_based_endpointing DialogflowConversationProfile#use_timeout_based_endpointing}
        '''
        result = self._values.get("use_timeout_based_endpointing")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DialogflowConversationProfileSttConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DialogflowConversationProfileSttConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dialogflowConversationProfile.DialogflowConversationProfileSttConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f0d0a6337c82e0840076c3d59938f03594bc535bd1def4e19ba44299bddce855)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7e6db8a30efc08fe2b642be81e96db736bd297e5c785cb7a61acb41b009361aa)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bd99125bef9dd5fc957bf022f13bbe4f9eca345d170434df41bf61cf04983c45)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableWordInfo", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="languageCode")
    def language_code(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "languageCode"))

    @language_code.setter
    def language_code(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e5d9b61d8fe7874e32d2104af3f321bbf15ed9edf0f9e85b6ae78da5c921c2a3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "languageCode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="model")
    def model(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "model"))

    @model.setter
    def model(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__af144a0ed41b7551168f5ceb7ae2005e1fec42d2066b0b7c47974ff0296d57b0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "model", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sampleRateHertz")
    def sample_rate_hertz(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "sampleRateHertz"))

    @sample_rate_hertz.setter
    def sample_rate_hertz(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c9705a507934e0e08fec57f62d09f50f71f2d4d2e2f825cd75bc977a13110e10)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sampleRateHertz", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="speechModelVariant")
    def speech_model_variant(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "speechModelVariant"))

    @speech_model_variant.setter
    def speech_model_variant(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c12314bf80a937ebd3f773d0200dcd67984a731adff0e7d05ee4fe808163ba26)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8d192e62a08017dfc9fb8091f4e081bb62f135fda2eebed274e2cdcf9e1a6a2a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "useTimeoutBasedEndpointing", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[DialogflowConversationProfileSttConfig]:
        return typing.cast(typing.Optional[DialogflowConversationProfileSttConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DialogflowConversationProfileSttConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c6d609fc0c6672b4e67807eea3c7757249be52dc21d6cb3d105160d091ec71c7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dialogflowConversationProfile.DialogflowConversationProfileTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class DialogflowConversationProfileTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#create DialogflowConversationProfile#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#delete DialogflowConversationProfile#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#update DialogflowConversationProfile#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8270acb762b737898d7a33aea14870824c7bd52b19690dc06fef52f5e373c177)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#create DialogflowConversationProfile#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#delete DialogflowConversationProfile#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#update DialogflowConversationProfile#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DialogflowConversationProfileTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DialogflowConversationProfileTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dialogflowConversationProfile.DialogflowConversationProfileTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__65c2a04b21f0288c053bb390d0321097a561f1b4fa9521a6861eb6b1bcdeb25d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__49ecda2ce3d646e1fec96002b99d0b02871b630a7593bf73a0cccd855115e080)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c429f2f24201467d7a0589e3317bf37871a30565b0cecd4e14bb443f534da9fb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__042e7a8bb8844e76d081d198480e4160866458d47a7205cebc18b00afca2c940)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DialogflowConversationProfileTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DialogflowConversationProfileTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DialogflowConversationProfileTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__355e31925b2f5cd6a615d7a74f94d4a3bfb3c579e11fa79429487db99b3dd9db)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dialogflowConversationProfile.DialogflowConversationProfileTtsConfig",
    jsii_struct_bases=[],
    name_mapping={
        "effects_profile_id": "effectsProfileId",
        "pitch": "pitch",
        "speaking_rate": "speakingRate",
        "voice": "voice",
        "volume_gain_db": "volumeGainDb",
    },
)
class DialogflowConversationProfileTtsConfig:
    def __init__(
        self,
        *,
        effects_profile_id: typing.Optional[typing.Sequence[builtins.str]] = None,
        pitch: typing.Optional[jsii.Number] = None,
        speaking_rate: typing.Optional[jsii.Number] = None,
        voice: typing.Optional[typing.Union["DialogflowConversationProfileTtsConfigVoice", typing.Dict[builtins.str, typing.Any]]] = None,
        volume_gain_db: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param effects_profile_id: An identifier which selects 'audio effects' profiles that are applied on (post synthesized) text to speech. Effects are applied on top of each other in the order they are given. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#effects_profile_id DialogflowConversationProfile#effects_profile_id}
        :param pitch: Speaking pitch, in the range [-20.0, 20.0]. 20 means increase 20 semitones from the original pitch. -20 means decrease 20 semitones from the original pitch. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#pitch DialogflowConversationProfile#pitch}
        :param speaking_rate: Speaking rate/speed, in the range [0.25, 4.0]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#speaking_rate DialogflowConversationProfile#speaking_rate}
        :param voice: voice block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#voice DialogflowConversationProfile#voice}
        :param volume_gain_db: Volume gain (in dB) of the normal native volume supported by the specific voice. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#volume_gain_db DialogflowConversationProfile#volume_gain_db}
        '''
        if isinstance(voice, dict):
            voice = DialogflowConversationProfileTtsConfigVoice(**voice)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4b3d060a699590c975a6c718ad2655fa3251ae6d2024b2cc992c23a8fb8e63aa)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#effects_profile_id DialogflowConversationProfile#effects_profile_id}
        '''
        result = self._values.get("effects_profile_id")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def pitch(self) -> typing.Optional[jsii.Number]:
        '''Speaking pitch, in the range [-20.0, 20.0]. 20 means increase 20 semitones from the original pitch. -20 means decrease 20 semitones from the original pitch.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#pitch DialogflowConversationProfile#pitch}
        '''
        result = self._values.get("pitch")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def speaking_rate(self) -> typing.Optional[jsii.Number]:
        '''Speaking rate/speed, in the range [0.25, 4.0].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#speaking_rate DialogflowConversationProfile#speaking_rate}
        '''
        result = self._values.get("speaking_rate")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def voice(self) -> typing.Optional["DialogflowConversationProfileTtsConfigVoice"]:
        '''voice block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#voice DialogflowConversationProfile#voice}
        '''
        result = self._values.get("voice")
        return typing.cast(typing.Optional["DialogflowConversationProfileTtsConfigVoice"], result)

    @builtins.property
    def volume_gain_db(self) -> typing.Optional[jsii.Number]:
        '''Volume gain (in dB) of the normal native volume supported by the specific voice.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#volume_gain_db DialogflowConversationProfile#volume_gain_db}
        '''
        result = self._values.get("volume_gain_db")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DialogflowConversationProfileTtsConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DialogflowConversationProfileTtsConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dialogflowConversationProfile.DialogflowConversationProfileTtsConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2ea08500dc69cd73ecc0b8a0d5840cd1f6684e1eb6bcd7c7cb9b66697279003f)
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
        :param name: The name of the voice. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#name DialogflowConversationProfile#name}
        :param ssml_gender: The preferred gender of the voice. Possible values: ["SSML_VOICE_GENDER_UNSPECIFIED", "SSML_VOICE_GENDER_MALE", "SSML_VOICE_GENDER_FEMALE", "SSML_VOICE_GENDER_NEUTRAL"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#ssml_gender DialogflowConversationProfile#ssml_gender}
        '''
        value = DialogflowConversationProfileTtsConfigVoice(
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
    def voice(self) -> "DialogflowConversationProfileTtsConfigVoiceOutputReference":
        return typing.cast("DialogflowConversationProfileTtsConfigVoiceOutputReference", jsii.get(self, "voice"))

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
    ) -> typing.Optional["DialogflowConversationProfileTtsConfigVoice"]:
        return typing.cast(typing.Optional["DialogflowConversationProfileTtsConfigVoice"], jsii.get(self, "voiceInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__b9b315d196343c7e6ec0e197a79c9d3430e8b10617ac82b45cc73c2501f340cc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "effectsProfileId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="pitch")
    def pitch(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "pitch"))

    @pitch.setter
    def pitch(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5841c88e35d1187cb87d4db806cb4fc8c6ad99086ddc43ef0c5e25eef0e08338)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pitch", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="speakingRate")
    def speaking_rate(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "speakingRate"))

    @speaking_rate.setter
    def speaking_rate(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c73d479a1e3dc1d1f2e16d9f10ea8d3995171ebe4c0923992611bc2cb7f3379f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "speakingRate", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="volumeGainDb")
    def volume_gain_db(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "volumeGainDb"))

    @volume_gain_db.setter
    def volume_gain_db(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9c2094d36014b762922649add892037047643ac2bb1fd568939ba9788f42f85a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "volumeGainDb", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[DialogflowConversationProfileTtsConfig]:
        return typing.cast(typing.Optional[DialogflowConversationProfileTtsConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DialogflowConversationProfileTtsConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__40e0b1c9f6f242bc68dc701413fe02ad68b4e5dd847f7940b1262bc7ba09169b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dialogflowConversationProfile.DialogflowConversationProfileTtsConfigVoice",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "ssml_gender": "ssmlGender"},
)
class DialogflowConversationProfileTtsConfigVoice:
    def __init__(
        self,
        *,
        name: typing.Optional[builtins.str] = None,
        ssml_gender: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: The name of the voice. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#name DialogflowConversationProfile#name}
        :param ssml_gender: The preferred gender of the voice. Possible values: ["SSML_VOICE_GENDER_UNSPECIFIED", "SSML_VOICE_GENDER_MALE", "SSML_VOICE_GENDER_FEMALE", "SSML_VOICE_GENDER_NEUTRAL"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#ssml_gender DialogflowConversationProfile#ssml_gender}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__18ae1ded32ab41cb5e11802cbfa39ea8095cd2f9704462efa266e561ba79120f)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#name DialogflowConversationProfile#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ssml_gender(self) -> typing.Optional[builtins.str]:
        '''The preferred gender of the voice. Possible values: ["SSML_VOICE_GENDER_UNSPECIFIED", "SSML_VOICE_GENDER_MALE", "SSML_VOICE_GENDER_FEMALE", "SSML_VOICE_GENDER_NEUTRAL"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/dialogflow_conversation_profile#ssml_gender DialogflowConversationProfile#ssml_gender}
        '''
        result = self._values.get("ssml_gender")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DialogflowConversationProfileTtsConfigVoice(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DialogflowConversationProfileTtsConfigVoiceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dialogflowConversationProfile.DialogflowConversationProfileTtsConfigVoiceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__86ab2ee5a8724e87225e8b24390b3b6bca7cc4e4fb71f2be60aa95ade00ba480)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0322549b5e1f14787c70c47614e6b39f4cda1d761c9748c81d252e0ef41ce11c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ssmlGender")
    def ssml_gender(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ssmlGender"))

    @ssml_gender.setter
    def ssml_gender(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__372008a42d254dafd64bfe8f4bc012da2c198c20d57af7cff1cd830b49211a9b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ssmlGender", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DialogflowConversationProfileTtsConfigVoice]:
        return typing.cast(typing.Optional[DialogflowConversationProfileTtsConfigVoice], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DialogflowConversationProfileTtsConfigVoice],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__01824733e58a9e401d025b6ea182c1d00cf4f9204f5326e4a0336f9add04e237)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "DialogflowConversationProfile",
    "DialogflowConversationProfileAutomatedAgentConfig",
    "DialogflowConversationProfileAutomatedAgentConfigOutputReference",
    "DialogflowConversationProfileConfig",
    "DialogflowConversationProfileHumanAgentAssistantConfig",
    "DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfig",
    "DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigs",
    "DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsConversationModelConfig",
    "DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsConversationModelConfigOutputReference",
    "DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsConversationProcessConfig",
    "DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsConversationProcessConfigOutputReference",
    "DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsList",
    "DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsOutputReference",
    "DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfig",
    "DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfigContextFilterSettings",
    "DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfigContextFilterSettingsOutputReference",
    "DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfigDialogflowQuerySource",
    "DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfigDialogflowQuerySourceHumanAgentSideConfig",
    "DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfigDialogflowQuerySourceHumanAgentSideConfigOutputReference",
    "DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfigDialogflowQuerySourceOutputReference",
    "DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfigDocumentQuerySource",
    "DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfigDocumentQuerySourceOutputReference",
    "DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfigKnowledgeBaseQuerySource",
    "DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfigKnowledgeBaseQuerySourceOutputReference",
    "DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfigOutputReference",
    "DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfigSections",
    "DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfigSectionsOutputReference",
    "DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsSuggestionFeature",
    "DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsSuggestionFeatureOutputReference",
    "DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsSuggestionTriggerSettings",
    "DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsSuggestionTriggerSettingsOutputReference",
    "DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigOutputReference",
    "DialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfig",
    "DialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigs",
    "DialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsConversationModelConfig",
    "DialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsConversationModelConfigOutputReference",
    "DialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsConversationProcessConfig",
    "DialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsConversationProcessConfigOutputReference",
    "DialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsList",
    "DialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsOutputReference",
    "DialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsQueryConfig",
    "DialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsQueryConfigContextFilterSettings",
    "DialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsQueryConfigContextFilterSettingsOutputReference",
    "DialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsQueryConfigDialogflowQuerySource",
    "DialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsQueryConfigDialogflowQuerySourceHumanAgentSideConfig",
    "DialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsQueryConfigDialogflowQuerySourceHumanAgentSideConfigOutputReference",
    "DialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsQueryConfigDialogflowQuerySourceOutputReference",
    "DialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsQueryConfigOutputReference",
    "DialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsQueryConfigSections",
    "DialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsQueryConfigSectionsOutputReference",
    "DialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsSuggestionFeature",
    "DialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsSuggestionFeatureOutputReference",
    "DialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsSuggestionTriggerSettings",
    "DialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsSuggestionTriggerSettingsOutputReference",
    "DialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigOutputReference",
    "DialogflowConversationProfileHumanAgentAssistantConfigMessageAnalysisConfig",
    "DialogflowConversationProfileHumanAgentAssistantConfigMessageAnalysisConfigOutputReference",
    "DialogflowConversationProfileHumanAgentAssistantConfigNotificationConfig",
    "DialogflowConversationProfileHumanAgentAssistantConfigNotificationConfigOutputReference",
    "DialogflowConversationProfileHumanAgentAssistantConfigOutputReference",
    "DialogflowConversationProfileHumanAgentHandoffConfig",
    "DialogflowConversationProfileHumanAgentHandoffConfigLivePersonConfig",
    "DialogflowConversationProfileHumanAgentHandoffConfigLivePersonConfigOutputReference",
    "DialogflowConversationProfileHumanAgentHandoffConfigOutputReference",
    "DialogflowConversationProfileLoggingConfig",
    "DialogflowConversationProfileLoggingConfigOutputReference",
    "DialogflowConversationProfileNewMessageEventNotificationConfig",
    "DialogflowConversationProfileNewMessageEventNotificationConfigOutputReference",
    "DialogflowConversationProfileNotificationConfig",
    "DialogflowConversationProfileNotificationConfigOutputReference",
    "DialogflowConversationProfileSttConfig",
    "DialogflowConversationProfileSttConfigOutputReference",
    "DialogflowConversationProfileTimeouts",
    "DialogflowConversationProfileTimeoutsOutputReference",
    "DialogflowConversationProfileTtsConfig",
    "DialogflowConversationProfileTtsConfigOutputReference",
    "DialogflowConversationProfileTtsConfigVoice",
    "DialogflowConversationProfileTtsConfigVoiceOutputReference",
]

publication.publish()

def _typecheckingstub__223237aa40860e4bc01bf819eeeb6119b731d6acb9f4922363b40a491915fb2f(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    display_name: builtins.str,
    location: builtins.str,
    automated_agent_config: typing.Optional[typing.Union[DialogflowConversationProfileAutomatedAgentConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    human_agent_assistant_config: typing.Optional[typing.Union[DialogflowConversationProfileHumanAgentAssistantConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    human_agent_handoff_config: typing.Optional[typing.Union[DialogflowConversationProfileHumanAgentHandoffConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    language_code: typing.Optional[builtins.str] = None,
    logging_config: typing.Optional[typing.Union[DialogflowConversationProfileLoggingConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    new_message_event_notification_config: typing.Optional[typing.Union[DialogflowConversationProfileNewMessageEventNotificationConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    notification_config: typing.Optional[typing.Union[DialogflowConversationProfileNotificationConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    project: typing.Optional[builtins.str] = None,
    security_settings: typing.Optional[builtins.str] = None,
    stt_config: typing.Optional[typing.Union[DialogflowConversationProfileSttConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[DialogflowConversationProfileTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    time_zone: typing.Optional[builtins.str] = None,
    tts_config: typing.Optional[typing.Union[DialogflowConversationProfileTtsConfig, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__829826b451be440daf6dbdfddcc8414517a9c40a13a0fe6bb966cab15d6d5878(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__231c8c2581c6656aeaf27596a7c073becf40790f261465dea6ae2d8887c61193(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf950dd7a6ebfaaed9ef1b51eb97bbc4851e14f5a1577adadb9cb65a92e49bd5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ecc85f8a166a5730e3f737000bae80af676478719e308497d9d523c5f33df173(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ce4ef4befcc5b46c3d9c97f025388f82bcf694f54a4bd1317ab404623149773(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dfd8c6e7045c51a7465ea24c44481e56920e340962b7714a387146da6447eff4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2dc80c8c8fbfff24f94eab02aee8572b179f93049328a50233275ecb6bd45dc7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a92ce0f9506d2410bf7fb4dfb6bc93ea18b3966582580609ce748ec0b9bc771a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b401d5d43fb62253f6cf2a61b8e8af9c09d816a07383ac16dd592746897e11c5(
    *,
    agent: builtins.str,
    session_ttl: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4b9c114ea0ae8c06078992f2401361071bf4ed28b8e2d69d735f8af313cd004(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98c1f000e3d5cf837c00974b3e548feb7b899475ace8db143f685e7bdafe2510(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e48f52dd1272472d6bffd088480f0f4a7db5466782e89602607445bada470767(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e868f5cce1dbb6e1c603e11df42a0b7c07402fa5d8bde08a650aeadb7b00fd1e(
    value: typing.Optional[DialogflowConversationProfileAutomatedAgentConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__641e7434d0d7fac6924947f95509745270d2f8bfb3d0ac86dffed129065b552b(
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
    automated_agent_config: typing.Optional[typing.Union[DialogflowConversationProfileAutomatedAgentConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    human_agent_assistant_config: typing.Optional[typing.Union[DialogflowConversationProfileHumanAgentAssistantConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    human_agent_handoff_config: typing.Optional[typing.Union[DialogflowConversationProfileHumanAgentHandoffConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    language_code: typing.Optional[builtins.str] = None,
    logging_config: typing.Optional[typing.Union[DialogflowConversationProfileLoggingConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    new_message_event_notification_config: typing.Optional[typing.Union[DialogflowConversationProfileNewMessageEventNotificationConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    notification_config: typing.Optional[typing.Union[DialogflowConversationProfileNotificationConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    project: typing.Optional[builtins.str] = None,
    security_settings: typing.Optional[builtins.str] = None,
    stt_config: typing.Optional[typing.Union[DialogflowConversationProfileSttConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[DialogflowConversationProfileTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    time_zone: typing.Optional[builtins.str] = None,
    tts_config: typing.Optional[typing.Union[DialogflowConversationProfileTtsConfig, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a56695d36a1f96dc3ed7a6446e6ddd0262124129f39daabf0ccf62c318af94b4(
    *,
    end_user_suggestion_config: typing.Optional[typing.Union[DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    human_agent_suggestion_config: typing.Optional[typing.Union[DialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    message_analysis_config: typing.Optional[typing.Union[DialogflowConversationProfileHumanAgentAssistantConfigMessageAnalysisConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    notification_config: typing.Optional[typing.Union[DialogflowConversationProfileHumanAgentAssistantConfigNotificationConfig, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1bed750542ab379233e26e631ee8a85400019330c95b4de92f47ceefe9a3cde(
    *,
    disable_high_latency_features_sync_delivery: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    feature_configs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigs, typing.Dict[builtins.str, typing.Any]]]]] = None,
    generators: typing.Optional[typing.Sequence[builtins.str]] = None,
    group_suggestion_responses: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__981a92704043d3d69d9c7d3d1d86f6ebd44c533facfaedb9b60a308b94131018(
    *,
    conversation_model_config: typing.Optional[typing.Union[DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsConversationModelConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    conversation_process_config: typing.Optional[typing.Union[DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsConversationProcessConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    disable_agent_query_logging: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enable_conversation_augmented_query: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enable_event_based_suggestion: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enable_query_suggestion_only: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enable_query_suggestion_when_no_answer: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    query_config: typing.Optional[typing.Union[DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    suggestion_feature: typing.Optional[typing.Union[DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsSuggestionFeature, typing.Dict[builtins.str, typing.Any]]] = None,
    suggestion_trigger_settings: typing.Optional[typing.Union[DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsSuggestionTriggerSettings, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a6c77ce9c3e63c24097c9b3991b029d4e6e98573c505cdada7b67a276f6f48ed(
    *,
    baseline_model_version: typing.Optional[builtins.str] = None,
    model: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e0339ac1afe4aedd03fb933356e48183cb79c8d5989c1115f3e8b265a0605b1a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb0087abea8719603870187ffdf26b812736f33273950f82c0927616dd8c6910(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__973bdd5ff0fdf45fdc2eec00cd7e1512518ea2646fcd136ab53a2f9bb6bc03d5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78b47f588128b392a652a7d6d54d52eceb32afe27cdb64c775a3bc45ffac2889(
    value: typing.Optional[DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsConversationModelConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__56665caf4ef4b602d60be5b4093727fd4bf00a2e39e89ec03fde803a02ad2b33(
    *,
    recent_sentences_count: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71905e4a1cfe682137b3ea03c9ac3c42c8fc0e30490a7bbc84b95c06cf83c6c7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9175510abc9413fccab61f584ae34b1fe5ed5ab65654882cb847764788f9f96(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf976d6d9183540a378509aedefd6b896c73dca22378931afa7a8f1ec4b55645(
    value: typing.Optional[DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsConversationProcessConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0eede5fbb11346e83cd0a114f8708ba2a9aa2b83cb9db5af3a0239ad5d6f79ea(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__368e328631977cc44968b30dc9f5e4e14fbb1985c05dc939bcaffbbadb3f94b9(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e245e2b6bbc7b77cadf7b26a43162e7a6abb3904732ee86eff84b49bd0102c4a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af3f224bf409080cfcf32237585def9f9493e7acb5c9feff60075eeb23a3f700(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7af7303ef1f08beebc954cf45f1109da29fff543e3c8a24dba696ce221557e53(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5487152b5f6701aab1f3c69ec58c6aa128f543431ad46601bac72df7aaebea89(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigs]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9edcef4c8babaff590ebe7caf8a925d2d6c25db551ed999c22e8c48a905afef9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72373f8071fa9ab595af19bddc490002f8da63dad67c2d2d8b69656600977b73(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ecc55a6a371757ab2067bacc28016c11bc85808ada4343d5f78a02c196c5533(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11693605454146fd7b058134518d3f8f6c8694403dd11faf8eca0921ea243a2e(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26a8049f1db311ace3f9ed48bd8af329d1917d8b1833db64ea92fbb77069a516(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03b5d6488de75ab381a23ed95e34128aa5ff1d770f6c13f891bade673a4e8d29(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__58f0af7c850bd1701f3fc8fd8c465213e3d8ac5dbc713f8d2c099997fb134ee4(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigs]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ee9fcf1cb89f491ac849058d5859a5f17df1c2659aba86703d5feb20400de0c(
    *,
    confidence_threshold: typing.Optional[jsii.Number] = None,
    context_filter_settings: typing.Optional[typing.Union[DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfigContextFilterSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    dialogflow_query_source: typing.Optional[typing.Union[DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfigDialogflowQuerySource, typing.Dict[builtins.str, typing.Any]]] = None,
    document_query_source: typing.Optional[typing.Union[DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfigDocumentQuerySource, typing.Dict[builtins.str, typing.Any]]] = None,
    knowledge_base_query_source: typing.Optional[typing.Union[DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfigKnowledgeBaseQuerySource, typing.Dict[builtins.str, typing.Any]]] = None,
    max_results: typing.Optional[jsii.Number] = None,
    sections: typing.Optional[typing.Union[DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfigSections, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__35a4461efb86cf6729738f3bc71e36a8128e87f6ff3dd50c48a17f7caf379774(
    *,
    drop_handoff_messages: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    drop_ivr_messages: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    drop_virtual_agent_messages: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77572a4370dbdaf104df2798a4fa8d9f5c1e0b08f61ff0c4c97a1acdf8101fd8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__015c1213c1d2ba982b02a0342a7f2bb16387c38839cbb9bfbf18c8f279001091(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2aecdb0e60ea79d29e817b845da091971adb2eb0ae491efc0b87bd8d1123e01(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__853b2fc2d0773225873390cbce61a1aea4232a1d46cfa15507ebdf29b992443d(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d81addcacfd82d140f90396615200d6882eafc48b9970e6370e45c7ec8734856(
    value: typing.Optional[DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfigContextFilterSettings],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44916a521be93e016d51addc204793eb8ef3a3e59c7d579463a606f97edf90be(
    *,
    agent: builtins.str,
    human_agent_side_config: typing.Optional[typing.Union[DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfigDialogflowQuerySourceHumanAgentSideConfig, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a03215840345ec042c0da820858e14178cf34ce4a5b2ebef1996d6ce36010966(
    *,
    agent: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fea1ff5b519dd76d4bfa610481e331ba4500810399e0b3af33e21be227798544(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb18323c673835b6c764be8b43f8b56c3de295ad8b735db6a605da4df32c57ec(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__840a2606e34f5789cdf61f8d085faf0986b697160e15170533ce430d9f346556(
    value: typing.Optional[DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfigDialogflowQuerySourceHumanAgentSideConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f58bb77bfc79b452a3a5b1b6f5e288b64d65dde73857687e3aa23da3c110395(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__56c83c807da2350745bdf6151adddca2483185f3a8bf4cb3b4b5696a77f27f40(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0cb7ad203b17b71b225b03816ba0ab41463680c0c146a4ce9a28abdbe0b5ced3(
    value: typing.Optional[DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfigDialogflowQuerySource],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5916f2d67777551e985d3f61aa7566505f8da261e9bef6a166a25f20d8c46806(
    *,
    documents: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed8e4c6145dff9830ebdc66d326ea11f7d0b7d1a7c4b97305a754fdaebb839e3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb4344dd9f54343204002f329fbd2268ed2fd7d83d10cc2ed56899fe855985f1(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9432c71790f69ccbb3280221ff7b0d6853572d88d4efe02c977da64827d841a(
    value: typing.Optional[DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfigDocumentQuerySource],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ecda5c89511d1cf6e9bbd291a615db98d915e130ebb1afa29d1acbfd71a9f41e(
    *,
    knowledge_bases: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__70f554988cd6d133be6af0d8c65e53907e6be343936322d31d635bb4d4407c7f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9fcaf743980da5e652f3ba51982cebbc0c116deea4daf0b287a3fa7822e17dbd(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__178c31edaaa7238f72fcf4af5a5e6caa9b2a72e1b2b36bb8a85101f6c2bb83b5(
    value: typing.Optional[DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfigKnowledgeBaseQuerySource],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ffd7ffb384f5d67058af3aef38f55ea3076c08a4c0e3a6d92f5967baf8ae8f79(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20664f9bfa1a8e67472af75d8e042ba0af579aab559a71254505ee6c0a15990f(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37c5ac15e3b2407aeafca3db3af3949e96fe22180897618832fcaaa3d101b6ec(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41a9129c752df3e9f1cbbf105139c5efb9e372fcdbd07a53520b68ef69cad04d(
    value: typing.Optional[DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d9cca18a6634a88fd1a514a3d862b2c69736a1bd17b24c81e2c9ebfdf6a85b52(
    *,
    section_types: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6616de12e10eb61217476a9ea5cf2958739a474acd2c197ce9c2857adabf95a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57164eea9a39a4167f0ee03d8ac77e1b2cfc888e8f7e70588f037572c3479633(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__908819a0cca627d04e1ea05176f1b1783458858bb654e2f1b80ac16364701d6b(
    value: typing.Optional[DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsQueryConfigSections],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29128bf19a5da111e2e6fd4388ed0cd616f8aa2936b6ba37f3bccc952a6e8525(
    *,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4778d9cbcc9813c5ecf271dea806e4ad141a89aa747d2aed6533f4af4b550497(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c780cb6f90bb3c0e717283c944547058b34ff09da37f454b41dcbf7283a6ed2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f2896ea410d8b3dd7d1fab1cf2a06e496c9aee94da707b8a2dfa65cd2c1f42c(
    value: typing.Optional[DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsSuggestionFeature],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd5d9ab02b1449755adff26b4085efc8477bf20dfed413a31b0f18556b43e0bb(
    *,
    no_small_talk: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    only_end_user: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bee633b09e2214f769830f27a067549bd47d0934e81d570f93b360e26609e8a2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8116e5553912c477d08d6ff92b0117b153bae272b7b8a5397aed62cc31b0eb5a(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92728370e2a56388a148a74f26144f6db370d5b80a5e5c5462b7578f0a58576d(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__147db57be1128aff564405a06ea7800d2e36b0fcbfff6d060dbcb0cc6f333211(
    value: typing.Optional[DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigsSuggestionTriggerSettings],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d0202ae02993657d66824c22321186d26bde614884285a81b8408a2867250f7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7dbb0658db88657f3bf1ef37692d7d5d76062c5dedaef69f7b59e98e0d31899(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfigFeatureConfigs, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e4d85bef9852bb5d954306f9f3cbf8031105a43d0360f99b7726a903caa2f9e(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d7c369ab3ab0176c3e7e44efe6521057b6fb8823b44fbadada2110a55b0ea4b9(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce2927d1b006d4776330611002db92ae38794f4bd3185e81390e9a8627203760(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__450a5e06c0fa3be9f741d5a7d7b062f0e519876f38966ca7fb9a08a247d02ba5(
    value: typing.Optional[DialogflowConversationProfileHumanAgentAssistantConfigEndUserSuggestionConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a3c71bb3f79a2f2dfb7c8982d5626c62cd838a7f2248a3e82a35bd0a3714127(
    *,
    disable_high_latency_features_sync_delivery: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    feature_configs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigs, typing.Dict[builtins.str, typing.Any]]]]] = None,
    generators: typing.Optional[typing.Sequence[builtins.str]] = None,
    group_suggestion_responses: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ddc475dd3ad52ec6d0c6032c7a162412a5fa2d9d5f9c9b36d68910c59f2bd9c(
    *,
    conversation_model_config: typing.Optional[typing.Union[DialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsConversationModelConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    conversation_process_config: typing.Optional[typing.Union[DialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsConversationProcessConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    disable_agent_query_logging: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enable_conversation_augmented_query: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enable_event_based_suggestion: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enable_query_suggestion_only: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enable_query_suggestion_when_no_answer: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    query_config: typing.Optional[typing.Union[DialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsQueryConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    suggestion_feature: typing.Optional[typing.Union[DialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsSuggestionFeature, typing.Dict[builtins.str, typing.Any]]] = None,
    suggestion_trigger_settings: typing.Optional[typing.Union[DialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsSuggestionTriggerSettings, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04808a52e4bb73404fbdd5fba2dc38161f9403f27859c1eb6036c669527f1a28(
    *,
    baseline_model_version: typing.Optional[builtins.str] = None,
    model: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bebc6ffe849c608fc59123c67c55b0d9db53f0b21338e0384bb1fa4d7e66d3f7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c730906d3aca59500c7556564d8903eb171a245bb52130317c6efb01a019ed1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d461731db19c3233a887f3551735afe658ca79dbe8d9cb95126890e1f0561a6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__01a90ef6a90baf4dabd7834cbf978af25248cea0cd662c365df819c6638309f3(
    value: typing.Optional[DialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsConversationModelConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__575323893bb94b554e377420102aa75e9eab5c5595163fe2cf9da95053e1b1a1(
    *,
    recent_sentences_count: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57269fd26979ab08e4253dc4e67d4150d6e991d2f0aa34c3a7944163e82bf87a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8fbee899d477baac9594cf08e8c0516a1030af7a6f60c9a53f1696f871694c7d(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd5eed4fa5b3578a583c61e3069c07777bccb74aabb93af392a968701eee7cac(
    value: typing.Optional[DialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsConversationProcessConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__754d0f1e4224f63e9b60943945c1f802104503ccf44a708a5848c48baff5fe92(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ce3396c026183c9dc6f49c39fe00816122680d84fe5a9f7435ed54529b1c49b(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57e09be60b3732b37a2890dd0c2cef51bedc29b66fa3565abee94e2722a5b6b7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38e8ead1389a03ecc9fe078d4fbfc4183e9e33436ce21a038cbcc8726257c331(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f9ffe6895daa5b901a9692dac0cff03df0357c249aee0980298959861eb02cf(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__477476bd0d10d6bb36ffa552f08246f2d7b40ce97da4f55d0141ba8efc40b643(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigs]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a7a94c63328d767a443e125d3edd16db84b5247f23ac4afa73a3da5032cadd56(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__836dc9b8f25a682002e0c50b8174390558d3138f3e669aff5928e2f6cfe8ae38(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__065cb28d7713161b6a2149adcb6d0488f25cc2f50b2545102553d10e53ab56f6(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb0bce5d5c067d823f50e573d2538887808dc778918b235b7ea2787321816324(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc3716fa1d84ea9024929ae072877aa5446159fc0c1f910bc78921e5be00eec7(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03368f6d19e0bfa3cd1f29edade4d72a7d1ca4ca12a5de45ef024e47989ee007(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6697d3fea97ac17d953c70c15675bcdc9700a4c038ddd96b2040c9d0be73cdd5(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigs]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24aae5556c35e71f8fc0bc42976e06decff0cd528f170e2c74199a5b91433b7a(
    *,
    confidence_threshold: typing.Optional[jsii.Number] = None,
    context_filter_settings: typing.Optional[typing.Union[DialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsQueryConfigContextFilterSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    dialogflow_query_source: typing.Optional[typing.Union[DialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsQueryConfigDialogflowQuerySource, typing.Dict[builtins.str, typing.Any]]] = None,
    max_results: typing.Optional[jsii.Number] = None,
    sections: typing.Optional[typing.Union[DialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsQueryConfigSections, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__685fa8c94180db89bff05f6d0baba2e8ae67c96b903638289d0c4d6b3d97ea3e(
    *,
    drop_handoff_messages: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    drop_ivr_messages: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    drop_virtual_agent_messages: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e0e13f40014c3fc78337e4740be4651becafcda6af647c28218e245ea61336e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3209ad6ca6a5394f198ddef47d691b6e2c0da9fc790ae144cd4df18d494e9fe3(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2941d36be524ce099e10f09988722fc3e33562cb3e4b389b597035ebfc4b7d4d(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__390695a6b1ef743e9e639ffa9b80832b4ce6ba6dc4d4a2debe7e1a5d5e216ddb(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9a047e3b40e15cf96c71d848ed5f1af6d19b114ee621d68805a0a88d2b47abc(
    value: typing.Optional[DialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsQueryConfigContextFilterSettings],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d6404b902a74e5917de8e17855c42c90b4ac73ffe932544640b94e78aef2cebd(
    *,
    agent: builtins.str,
    human_agent_side_config: typing.Optional[typing.Union[DialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsQueryConfigDialogflowQuerySourceHumanAgentSideConfig, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__448cb69feb94d1a7ff8211e1790bf2b8338a5a4bd6a8b7db6a3f263a68038bbd(
    *,
    agent: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8270c2c3b05942dde0ac2accb9c5b9eb00a9b4703be002783323d6ec31556a7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2a6f720966d2a48a4f9682fcf1f825781b8c8213dc0dce0caa7acf131b5a5da(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e4dcc291b89b6987f3817049ea1e3ede39dcf044b4439d0729ce8668921dd2d(
    value: typing.Optional[DialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsQueryConfigDialogflowQuerySourceHumanAgentSideConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e8c19ae04a8e3139a27d3f0632aaf0e3c0c96c593913ff81f3b9426726f10ba(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d61a68514a1c9220d6bbddbacd0430566d1a2079be133ae01bd811c404586a8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa1d1d23bc8080dae26e3d663c7f93a901f2a110a63f47c8c0d68fb9fc4e845c(
    value: typing.Optional[DialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsQueryConfigDialogflowQuerySource],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__492df00b618bd2c01c221aa74d3e1c027919575d2d428117ae6bd617809b3d6f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4510f4a1187fbba7e3f4657d7a62d8bdc63a0df2ac1d19e762c2b305e3bca092(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2d2206a6143ea9b7ad6b40dae0fa39dd2358640d64ec169daceee9da2c0d81b(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__84085d37a00aeb1fa8321339c02e0cf08630b695d74d089535e6775f85910527(
    value: typing.Optional[DialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsQueryConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69a657bb6dbe582fe73d8146ff800cb3cca2262847118288660e8e4e467df401(
    *,
    section_types: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__160b7d308cc07dc0f66d39bd844a62c6973d82d91dcdee500fed83d4cfed0f83(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96a7cf3a6bf19b9e9f9cd77f5eaeadb269473fc738147bf7bcdc18c33b2309fe(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6414d72c645b585d6eca83240a48d5373674d0c09ced7e7fa0ea9caa7502c16(
    value: typing.Optional[DialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsQueryConfigSections],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__672d5129f4cfc70fe1c7a8fd9f03d80ceb5cac7b2ede6180acec017bb45f419e(
    *,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13d4f882daeb49cff11615f81a59d2f219b32aec31965fa3ab92caec7ecf133b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c902835767d33fe09eae98c12378cd3c83d830eb32e8610b5ddf5a9303bf57ed(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8eef322461609cb342a114316922cc6916cb47d88d5f9f33643844e72d985156(
    value: typing.Optional[DialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsSuggestionFeature],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c2df082c67c60f29f6f0dc741633d93d6148412e1e261df65dde8205fd7e0e3(
    *,
    no_small_talk: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    only_end_user: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ca4e0a801df1c57ad264d0a79c5cea12e872b5fa4f5dc7704ab7fa4e3065106(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4fd019f908e5f78360052882645ba8f48aab891a22eb5f6eb4857663a138b69(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aadb359ac692b09bcc8d5318868503eec7e596a2f7e91d139cfdc5b62be6c8cd(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4516a58088bec16db7b93679a1d84e8e6a7f591b4590f3afaf9e4357834afbf6(
    value: typing.Optional[DialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigsSuggestionTriggerSettings],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f73d45cee9563d132676528fd325bf4bff803188d495e08e3517be6d7021c073(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1dc6fdc3b840a2bf31b7fdab282ba8361b5a4c02ffab5506e74b67793efb0c0a(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfigFeatureConfigs, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__703ac7fb83c5dec1956e80c580d9a4420232e2b6a709d9ead925dba32f0386ba(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d572236e82eb73fcf8712951ab7b5a5bd26cfd415ef32f9d1a8163899ed7a11(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__06b8cb90fc1742d859a958b9ec81ed15e89ac3c27e8ed941196daa80f6e1937e(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c895ee95a39cead6b27218d1614855c5b6a480e107de62426fec3ec715cdf293(
    value: typing.Optional[DialogflowConversationProfileHumanAgentAssistantConfigHumanAgentSuggestionConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6fe83ce3d3c33b6c87595f27a2515f0c44ab6c927adc78c4d486a53e13f9bd72(
    *,
    enable_entity_extraction: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enable_sentiment_analysis: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cdd3b76fedd86dac4161af2858930ad8dfa2a43f64d15a2ffb423b51237c5356(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb13b1cbf201e5e385731cd87e0a21012e3b3f37000d2f898a0c87cda39236b7(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b32e654fff239f381127d6abdc87bed55663c4df97639a5d0375f8c111d957c(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__227c733dec493262fe6ad96d3c67bb6ee911cea84c26627de3c93da91f8a3c86(
    value: typing.Optional[DialogflowConversationProfileHumanAgentAssistantConfigMessageAnalysisConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__763cf6b26cc1f09d4c3adbf3824bc8cf5416899079db93159d51ea3b3e31493c(
    *,
    message_format: typing.Optional[builtins.str] = None,
    topic: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f23e1a1f97f8ea9a0e6dc7c38051b9b73e55b386b986b0708b665509ffbcf7e1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__215a256f5b7413024624bc17665dbf734ebf896227c2f79f76e8f248b4736d96(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9564dfe5c1ae005f0b6d9297226acf0c016a53cf128b49b02febce5c842d6f0c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f8b0464aa544d4f2840b686d7ac32716679102d91f5e51c71db6cb2084765228(
    value: typing.Optional[DialogflowConversationProfileHumanAgentAssistantConfigNotificationConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2621fb08aa44a2a5c55bc652317d6a11b5ea10dc44672ab90260b8a7112d76e6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d935258d610bf5be37e172e138f2355dff634fb24f608b0d68ecd0a042a01c0c(
    value: typing.Optional[DialogflowConversationProfileHumanAgentAssistantConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1718f9257fd95311000a2765c65ee0aeeff2863e4dc9dc75a8d8a2b340f6de04(
    *,
    live_person_config: typing.Optional[typing.Union[DialogflowConversationProfileHumanAgentHandoffConfigLivePersonConfig, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__599ab865f51960f1a47595f149cde9e8ca29b1f67e45c2c1169fa67f25d4c528(
    *,
    account_number: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d5b8af5274fd64f970a256a050eccaa6e69aa362588535fb93c19577f132b32(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c0ac30f66fd213776951683b936b7eb3737ba21dcde88ae312874f8e3c81121(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9f2813797a8000a7db55caca0b7366f8c7ea8c674e96d31850f144dc7efee3e(
    value: typing.Optional[DialogflowConversationProfileHumanAgentHandoffConfigLivePersonConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77f8cc7fa00f202bb5de276ee6f80801e44521a1a7a290d4d1aea0f16ae49655(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d103d403f202002960b562e12e00009b7e04d1d8b711bdabf65bf5115e96812(
    value: typing.Optional[DialogflowConversationProfileHumanAgentHandoffConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a582142a5689c0d07833ac9313df508e76bdf5ace685b3cf4f1bbb5ed66f19fb(
    *,
    enable_stackdriver_logging: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3983d54419a9ab79f51c84a92bd13a170c6aedd8f2d0eb96ba397262cd8e45a5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__499ad5552c3c602d4b93b1a425ed7ce19b21abe20d6f2bfce198ea5b88d0b12f(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d2142a034903fb450d77769f0bb392e23137315ee429c8294eed7b5b85679d6(
    value: typing.Optional[DialogflowConversationProfileLoggingConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64ed90dd7ffd8a247c438b40f61040c92e56f130f44469a967082a36d946ee98(
    *,
    message_format: typing.Optional[builtins.str] = None,
    topic: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3ee71bdec52f86a59d3744a5fe46148fc429e02e33597b8da5e82df775d0d1c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__724d7497ed764c66e2477940ffaae97e2008c023e75067d0ae79ff8e36f2e58d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__107961b46feb26c8aa167ef5a8179fe49885f9335fd3cd56a73a80ff9ad64a26(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac8168c02680146ea3dabee544892b1439168e79efb8492d655883064755f7e3(
    value: typing.Optional[DialogflowConversationProfileNewMessageEventNotificationConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__000f258ac2daa600b135933b614262c19f4e525864b43f5dbabb915a8cfa8c3c(
    *,
    message_format: typing.Optional[builtins.str] = None,
    topic: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7fb62f520fc8c276d9737ebef0402df85579b92aa6f8b798997ed3418d6e36b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f69de11bfd5528b40438d9588e5f20bc84972bb25c49f3ff4c39a507ca05f656(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3aacbcf79a349e9b07d40eeeff3b4bf2b013456a8389ee66693c8d51ecd843d7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7fecd7178ff795cacdca15963bfde5abace3969b53f308456cbe0562e46ee737(
    value: typing.Optional[DialogflowConversationProfileNotificationConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d92564e6830d40dc3576e0b4d04825ac6f699a457e4cce727d2918feeec2571(
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

def _typecheckingstub__f0d0a6337c82e0840076c3d59938f03594bc535bd1def4e19ba44299bddce855(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e6db8a30efc08fe2b642be81e96db736bd297e5c785cb7a61acb41b009361aa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd99125bef9dd5fc957bf022f13bbe4f9eca345d170434df41bf61cf04983c45(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5d9b61d8fe7874e32d2104af3f321bbf15ed9edf0f9e85b6ae78da5c921c2a3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af144a0ed41b7551168f5ceb7ae2005e1fec42d2066b0b7c47974ff0296d57b0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9705a507934e0e08fec57f62d09f50f71f2d4d2e2f825cd75bc977a13110e10(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c12314bf80a937ebd3f773d0200dcd67984a731adff0e7d05ee4fe808163ba26(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d192e62a08017dfc9fb8091f4e081bb62f135fda2eebed274e2cdcf9e1a6a2a(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6d609fc0c6672b4e67807eea3c7757249be52dc21d6cb3d105160d091ec71c7(
    value: typing.Optional[DialogflowConversationProfileSttConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8270acb762b737898d7a33aea14870824c7bd52b19690dc06fef52f5e373c177(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65c2a04b21f0288c053bb390d0321097a561f1b4fa9521a6861eb6b1bcdeb25d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__49ecda2ce3d646e1fec96002b99d0b02871b630a7593bf73a0cccd855115e080(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c429f2f24201467d7a0589e3317bf37871a30565b0cecd4e14bb443f534da9fb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__042e7a8bb8844e76d081d198480e4160866458d47a7205cebc18b00afca2c940(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__355e31925b2f5cd6a615d7a74f94d4a3bfb3c579e11fa79429487db99b3dd9db(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DialogflowConversationProfileTimeouts]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b3d060a699590c975a6c718ad2655fa3251ae6d2024b2cc992c23a8fb8e63aa(
    *,
    effects_profile_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    pitch: typing.Optional[jsii.Number] = None,
    speaking_rate: typing.Optional[jsii.Number] = None,
    voice: typing.Optional[typing.Union[DialogflowConversationProfileTtsConfigVoice, typing.Dict[builtins.str, typing.Any]]] = None,
    volume_gain_db: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ea08500dc69cd73ecc0b8a0d5840cd1f6684e1eb6bcd7c7cb9b66697279003f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9b315d196343c7e6ec0e197a79c9d3430e8b10617ac82b45cc73c2501f340cc(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5841c88e35d1187cb87d4db806cb4fc8c6ad99086ddc43ef0c5e25eef0e08338(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c73d479a1e3dc1d1f2e16d9f10ea8d3995171ebe4c0923992611bc2cb7f3379f(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c2094d36014b762922649add892037047643ac2bb1fd568939ba9788f42f85a(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40e0b1c9f6f242bc68dc701413fe02ad68b4e5dd847f7940b1262bc7ba09169b(
    value: typing.Optional[DialogflowConversationProfileTtsConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18ae1ded32ab41cb5e11802cbfa39ea8095cd2f9704462efa266e561ba79120f(
    *,
    name: typing.Optional[builtins.str] = None,
    ssml_gender: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86ab2ee5a8724e87225e8b24390b3b6bca7cc4e4fb71f2be60aa95ade00ba480(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0322549b5e1f14787c70c47614e6b39f4cda1d761c9748c81d252e0ef41ce11c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__372008a42d254dafd64bfe8f4bc012da2c198c20d57af7cff1cd830b49211a9b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__01824733e58a9e401d025b6ea182c1d00cf4f9204f5326e4a0336f9add04e237(
    value: typing.Optional[DialogflowConversationProfileTtsConfigVoice],
) -> None:
    """Type checking stubs"""
    pass
