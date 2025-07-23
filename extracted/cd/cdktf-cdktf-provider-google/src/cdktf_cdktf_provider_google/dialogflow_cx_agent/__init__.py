r'''
# `google_dialogflow_cx_agent`

Refer to the Terraform Registry for docs: [`google_dialogflow_cx_agent`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_agent).
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


class DialogflowCxAgent(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dialogflowCxAgent.DialogflowCxAgent",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_agent google_dialogflow_cx_agent}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        default_language_code: builtins.str,
        display_name: builtins.str,
        location: builtins.str,
        time_zone: builtins.str,
        advanced_settings: typing.Optional[typing.Union["DialogflowCxAgentAdvancedSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        avatar_uri: typing.Optional[builtins.str] = None,
        delete_chat_engine_on_destroy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        description: typing.Optional[builtins.str] = None,
        enable_spell_correction: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_stackdriver_logging: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        gen_app_builder_settings: typing.Optional[typing.Union["DialogflowCxAgentGenAppBuilderSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        git_integration_settings: typing.Optional[typing.Union["DialogflowCxAgentGitIntegrationSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        security_settings: typing.Optional[builtins.str] = None,
        speech_to_text_settings: typing.Optional[typing.Union["DialogflowCxAgentSpeechToTextSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        supported_language_codes: typing.Optional[typing.Sequence[builtins.str]] = None,
        text_to_speech_settings: typing.Optional[typing.Union["DialogflowCxAgentTextToSpeechSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["DialogflowCxAgentTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_agent google_dialogflow_cx_agent} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param default_language_code: The default language of the agent as a language tag. `See Language Support <https://cloud.google.com/dialogflow/cx/docs/reference/language>`_ for a list of the currently supported language codes. This field cannot be updated after creation. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_agent#default_language_code DialogflowCxAgent#default_language_code}
        :param display_name: The human-readable name of the agent, unique within the location. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_agent#display_name DialogflowCxAgent#display_name}
        :param location: The name of the location this agent is located in. ~> **Note:** The first time you are deploying an Agent in your project you must configure location settings. This is a one time step but at the moment you can only `configure location settings <https://cloud.google.com/dialogflow/cx/docs/concept/region#location-settings>`_ via the Dialogflow CX console. Another options is to use global location so you don't need to manually configure location settings. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_agent#location DialogflowCxAgent#location}
        :param time_zone: The time zone of this agent from the `time zone database <https://www.iana.org/time-zones>`_, e.g., America/New_York, Europe/Paris. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_agent#time_zone DialogflowCxAgent#time_zone}
        :param advanced_settings: advanced_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_agent#advanced_settings DialogflowCxAgent#advanced_settings}
        :param avatar_uri: The URI of the agent's avatar. Avatars are used throughout the Dialogflow console and in the self-hosted Web Demo integration. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_agent#avatar_uri DialogflowCxAgent#avatar_uri}
        :param delete_chat_engine_on_destroy: If set to 'true', Terraform will delete the chat engine associated with the agent when the agent is destroyed. Otherwise, the chat engine will persist. This virtual field addresses a critical dependency chain: 'agent' -> 'engine' -> 'data store'. The chat engine is automatically provisioned when a data store is linked to the agent, meaning Terraform doesn't have direct control over its lifecycle as a managed resource. This creates a problem when both the agent and data store are managed by Terraform and need to be destroyed. Without delete_chat_engine_on_destroy set to true, the data store's deletion would fail because the unmanaged chat engine would still be using it. This setting ensures that the entire dependency chain can be properly torn down. See 'mmv1/templates/terraform/examples/dialogflowcx_tool_data_store.tf.tmpl' as an example. Data store can be linked to an agent through the 'knowledgeConnectorSettings' field of a `flow <https://cloud.google.com/dialogflow/cx/docs/reference/rest/v3/projects.locations.agents.flows#resource:-flow>`_ or a `page <https://cloud.google.com/dialogflow/cx/docs/reference/rest/v3/projects.locations.agents.flows.pages#resource:-page>`_ or the 'dataStoreSpec' field of a `tool <https://cloud.google.com/dialogflow/cx/docs/reference/rest/v3/projects.locations.agents.tools#resource:-tool>`_. The ID of the implicitly created engine is stored in the 'genAppBuilderSettings' field of the `agent <https://cloud.google.com/dialogflow/cx/docs/reference/rest/v3/projects.locations.agents#resource:-agent>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_agent#delete_chat_engine_on_destroy DialogflowCxAgent#delete_chat_engine_on_destroy}
        :param description: The description of this agent. The maximum length is 500 characters. If exceeded, the request is rejected. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_agent#description DialogflowCxAgent#description}
        :param enable_spell_correction: Indicates if automatic spell correction is enabled in detect intent requests. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_agent#enable_spell_correction DialogflowCxAgent#enable_spell_correction}
        :param enable_stackdriver_logging: Determines whether this agent should log conversation queries. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_agent#enable_stackdriver_logging DialogflowCxAgent#enable_stackdriver_logging}
        :param gen_app_builder_settings: gen_app_builder_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_agent#gen_app_builder_settings DialogflowCxAgent#gen_app_builder_settings}
        :param git_integration_settings: git_integration_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_agent#git_integration_settings DialogflowCxAgent#git_integration_settings}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_agent#id DialogflowCxAgent#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_agent#project DialogflowCxAgent#project}.
        :param security_settings: Name of the SecuritySettings reference for the agent. Format: projects//locations//securitySettings/. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_agent#security_settings DialogflowCxAgent#security_settings}
        :param speech_to_text_settings: speech_to_text_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_agent#speech_to_text_settings DialogflowCxAgent#speech_to_text_settings}
        :param supported_language_codes: The list of all languages supported by this agent (except for the default_language_code). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_agent#supported_language_codes DialogflowCxAgent#supported_language_codes}
        :param text_to_speech_settings: text_to_speech_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_agent#text_to_speech_settings DialogflowCxAgent#text_to_speech_settings}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_agent#timeouts DialogflowCxAgent#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__61bc8ebf23753dd057cb6e8d4f9cd853d22b0db49b9c2922bb276b018421e905)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = DialogflowCxAgentConfig(
            default_language_code=default_language_code,
            display_name=display_name,
            location=location,
            time_zone=time_zone,
            advanced_settings=advanced_settings,
            avatar_uri=avatar_uri,
            delete_chat_engine_on_destroy=delete_chat_engine_on_destroy,
            description=description,
            enable_spell_correction=enable_spell_correction,
            enable_stackdriver_logging=enable_stackdriver_logging,
            gen_app_builder_settings=gen_app_builder_settings,
            git_integration_settings=git_integration_settings,
            id=id,
            project=project,
            security_settings=security_settings,
            speech_to_text_settings=speech_to_text_settings,
            supported_language_codes=supported_language_codes,
            text_to_speech_settings=text_to_speech_settings,
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
        '''Generates CDKTF code for importing a DialogflowCxAgent resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the DialogflowCxAgent to import.
        :param import_from_id: The id of the existing DialogflowCxAgent that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_agent#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the DialogflowCxAgent to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__59d8e46fd3a432635720c1f804dc3fadb282ea1f32a85de798e8ef30042eccf0)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putAdvancedSettings")
    def put_advanced_settings(
        self,
        *,
        audio_export_gcs_destination: typing.Optional[typing.Union["DialogflowCxAgentAdvancedSettingsAudioExportGcsDestination", typing.Dict[builtins.str, typing.Any]]] = None,
        dtmf_settings: typing.Optional[typing.Union["DialogflowCxAgentAdvancedSettingsDtmfSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        logging_settings: typing.Optional[typing.Union["DialogflowCxAgentAdvancedSettingsLoggingSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        speech_settings: typing.Optional[typing.Union["DialogflowCxAgentAdvancedSettingsSpeechSettings", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param audio_export_gcs_destination: audio_export_gcs_destination block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_agent#audio_export_gcs_destination DialogflowCxAgent#audio_export_gcs_destination}
        :param dtmf_settings: dtmf_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_agent#dtmf_settings DialogflowCxAgent#dtmf_settings}
        :param logging_settings: logging_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_agent#logging_settings DialogflowCxAgent#logging_settings}
        :param speech_settings: speech_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_agent#speech_settings DialogflowCxAgent#speech_settings}
        '''
        value = DialogflowCxAgentAdvancedSettings(
            audio_export_gcs_destination=audio_export_gcs_destination,
            dtmf_settings=dtmf_settings,
            logging_settings=logging_settings,
            speech_settings=speech_settings,
        )

        return typing.cast(None, jsii.invoke(self, "putAdvancedSettings", [value]))

    @jsii.member(jsii_name="putGenAppBuilderSettings")
    def put_gen_app_builder_settings(self, *, engine: builtins.str) -> None:
        '''
        :param engine: The full name of the Gen App Builder engine related to this agent if there is one. Format: projects/{Project ID}/locations/{Location ID}/collections/{Collection ID}/engines/{Engine ID} Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_agent#engine DialogflowCxAgent#engine}
        '''
        value = DialogflowCxAgentGenAppBuilderSettings(engine=engine)

        return typing.cast(None, jsii.invoke(self, "putGenAppBuilderSettings", [value]))

    @jsii.member(jsii_name="putGitIntegrationSettings")
    def put_git_integration_settings(
        self,
        *,
        github_settings: typing.Optional[typing.Union["DialogflowCxAgentGitIntegrationSettingsGithubSettings", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param github_settings: github_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_agent#github_settings DialogflowCxAgent#github_settings}
        '''
        value = DialogflowCxAgentGitIntegrationSettings(
            github_settings=github_settings
        )

        return typing.cast(None, jsii.invoke(self, "putGitIntegrationSettings", [value]))

    @jsii.member(jsii_name="putSpeechToTextSettings")
    def put_speech_to_text_settings(
        self,
        *,
        enable_speech_adaptation: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param enable_speech_adaptation: Whether to use speech adaptation for speech recognition. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_agent#enable_speech_adaptation DialogflowCxAgent#enable_speech_adaptation}
        '''
        value = DialogflowCxAgentSpeechToTextSettings(
            enable_speech_adaptation=enable_speech_adaptation
        )

        return typing.cast(None, jsii.invoke(self, "putSpeechToTextSettings", [value]))

    @jsii.member(jsii_name="putTextToSpeechSettings")
    def put_text_to_speech_settings(
        self,
        *,
        synthesize_speech_configs: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param synthesize_speech_configs: Configuration of how speech should be synthesized, mapping from `language <https://cloud.google.com/dialogflow/cx/docs/reference/language>`_ to `SynthesizeSpeechConfig <https://cloud.google.com/dialogflow/cx/docs/reference/rest/v3/projects.locations.agents#synthesizespeechconfig>`_. These settings affect: * The phone gateway synthesize configuration set via Agent.text_to_speech_settings. * How speech is synthesized when invoking session APIs. 'Agent.text_to_speech_settings' only applies if 'OutputAudioConfig.synthesize_speech_config' is not specified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_agent#synthesize_speech_configs DialogflowCxAgent#synthesize_speech_configs}
        '''
        value = DialogflowCxAgentTextToSpeechSettings(
            synthesize_speech_configs=synthesize_speech_configs
        )

        return typing.cast(None, jsii.invoke(self, "putTextToSpeechSettings", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_agent#create DialogflowCxAgent#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_agent#delete DialogflowCxAgent#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_agent#update DialogflowCxAgent#update}.
        '''
        value = DialogflowCxAgentTimeouts(create=create, delete=delete, update=update)

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetAdvancedSettings")
    def reset_advanced_settings(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAdvancedSettings", []))

    @jsii.member(jsii_name="resetAvatarUri")
    def reset_avatar_uri(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAvatarUri", []))

    @jsii.member(jsii_name="resetDeleteChatEngineOnDestroy")
    def reset_delete_chat_engine_on_destroy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDeleteChatEngineOnDestroy", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetEnableSpellCorrection")
    def reset_enable_spell_correction(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnableSpellCorrection", []))

    @jsii.member(jsii_name="resetEnableStackdriverLogging")
    def reset_enable_stackdriver_logging(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnableStackdriverLogging", []))

    @jsii.member(jsii_name="resetGenAppBuilderSettings")
    def reset_gen_app_builder_settings(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGenAppBuilderSettings", []))

    @jsii.member(jsii_name="resetGitIntegrationSettings")
    def reset_git_integration_settings(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGitIntegrationSettings", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetProject")
    def reset_project(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProject", []))

    @jsii.member(jsii_name="resetSecuritySettings")
    def reset_security_settings(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSecuritySettings", []))

    @jsii.member(jsii_name="resetSpeechToTextSettings")
    def reset_speech_to_text_settings(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSpeechToTextSettings", []))

    @jsii.member(jsii_name="resetSupportedLanguageCodes")
    def reset_supported_language_codes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSupportedLanguageCodes", []))

    @jsii.member(jsii_name="resetTextToSpeechSettings")
    def reset_text_to_speech_settings(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTextToSpeechSettings", []))

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
    @jsii.member(jsii_name="advancedSettings")
    def advanced_settings(self) -> "DialogflowCxAgentAdvancedSettingsOutputReference":
        return typing.cast("DialogflowCxAgentAdvancedSettingsOutputReference", jsii.get(self, "advancedSettings"))

    @builtins.property
    @jsii.member(jsii_name="genAppBuilderSettings")
    def gen_app_builder_settings(
        self,
    ) -> "DialogflowCxAgentGenAppBuilderSettingsOutputReference":
        return typing.cast("DialogflowCxAgentGenAppBuilderSettingsOutputReference", jsii.get(self, "genAppBuilderSettings"))

    @builtins.property
    @jsii.member(jsii_name="gitIntegrationSettings")
    def git_integration_settings(
        self,
    ) -> "DialogflowCxAgentGitIntegrationSettingsOutputReference":
        return typing.cast("DialogflowCxAgentGitIntegrationSettingsOutputReference", jsii.get(self, "gitIntegrationSettings"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="speechToTextSettings")
    def speech_to_text_settings(
        self,
    ) -> "DialogflowCxAgentSpeechToTextSettingsOutputReference":
        return typing.cast("DialogflowCxAgentSpeechToTextSettingsOutputReference", jsii.get(self, "speechToTextSettings"))

    @builtins.property
    @jsii.member(jsii_name="startFlow")
    def start_flow(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "startFlow"))

    @builtins.property
    @jsii.member(jsii_name="textToSpeechSettings")
    def text_to_speech_settings(
        self,
    ) -> "DialogflowCxAgentTextToSpeechSettingsOutputReference":
        return typing.cast("DialogflowCxAgentTextToSpeechSettingsOutputReference", jsii.get(self, "textToSpeechSettings"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "DialogflowCxAgentTimeoutsOutputReference":
        return typing.cast("DialogflowCxAgentTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="advancedSettingsInput")
    def advanced_settings_input(
        self,
    ) -> typing.Optional["DialogflowCxAgentAdvancedSettings"]:
        return typing.cast(typing.Optional["DialogflowCxAgentAdvancedSettings"], jsii.get(self, "advancedSettingsInput"))

    @builtins.property
    @jsii.member(jsii_name="avatarUriInput")
    def avatar_uri_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "avatarUriInput"))

    @builtins.property
    @jsii.member(jsii_name="defaultLanguageCodeInput")
    def default_language_code_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "defaultLanguageCodeInput"))

    @builtins.property
    @jsii.member(jsii_name="deleteChatEngineOnDestroyInput")
    def delete_chat_engine_on_destroy_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "deleteChatEngineOnDestroyInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="displayNameInput")
    def display_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "displayNameInput"))

    @builtins.property
    @jsii.member(jsii_name="enableSpellCorrectionInput")
    def enable_spell_correction_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enableSpellCorrectionInput"))

    @builtins.property
    @jsii.member(jsii_name="enableStackdriverLoggingInput")
    def enable_stackdriver_logging_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enableStackdriverLoggingInput"))

    @builtins.property
    @jsii.member(jsii_name="genAppBuilderSettingsInput")
    def gen_app_builder_settings_input(
        self,
    ) -> typing.Optional["DialogflowCxAgentGenAppBuilderSettings"]:
        return typing.cast(typing.Optional["DialogflowCxAgentGenAppBuilderSettings"], jsii.get(self, "genAppBuilderSettingsInput"))

    @builtins.property
    @jsii.member(jsii_name="gitIntegrationSettingsInput")
    def git_integration_settings_input(
        self,
    ) -> typing.Optional["DialogflowCxAgentGitIntegrationSettings"]:
        return typing.cast(typing.Optional["DialogflowCxAgentGitIntegrationSettings"], jsii.get(self, "gitIntegrationSettingsInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="locationInput")
    def location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "locationInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="securitySettingsInput")
    def security_settings_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "securitySettingsInput"))

    @builtins.property
    @jsii.member(jsii_name="speechToTextSettingsInput")
    def speech_to_text_settings_input(
        self,
    ) -> typing.Optional["DialogflowCxAgentSpeechToTextSettings"]:
        return typing.cast(typing.Optional["DialogflowCxAgentSpeechToTextSettings"], jsii.get(self, "speechToTextSettingsInput"))

    @builtins.property
    @jsii.member(jsii_name="supportedLanguageCodesInput")
    def supported_language_codes_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "supportedLanguageCodesInput"))

    @builtins.property
    @jsii.member(jsii_name="textToSpeechSettingsInput")
    def text_to_speech_settings_input(
        self,
    ) -> typing.Optional["DialogflowCxAgentTextToSpeechSettings"]:
        return typing.cast(typing.Optional["DialogflowCxAgentTextToSpeechSettings"], jsii.get(self, "textToSpeechSettingsInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "DialogflowCxAgentTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "DialogflowCxAgentTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="timeZoneInput")
    def time_zone_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "timeZoneInput"))

    @builtins.property
    @jsii.member(jsii_name="avatarUri")
    def avatar_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "avatarUri"))

    @avatar_uri.setter
    def avatar_uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3f8342ecdcceb1cabba42fe56e31dbc4a14507bfaef9856c10796f591d512b1d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "avatarUri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="defaultLanguageCode")
    def default_language_code(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "defaultLanguageCode"))

    @default_language_code.setter
    def default_language_code(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9bc0b4ccf9181d2f9f6f678eeef3eeb36a64dc0fcc331c10be266fd624efb683)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultLanguageCode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="deleteChatEngineOnDestroy")
    def delete_chat_engine_on_destroy(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "deleteChatEngineOnDestroy"))

    @delete_chat_engine_on_destroy.setter
    def delete_chat_engine_on_destroy(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3005024be4224cf213f91866c88d53a8a85d887af243aa71d2e83dc8dce76fb8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deleteChatEngineOnDestroy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a40be0b053fa106e7cd28a68719bed0f75eb5e745376e20a1cce3dbf10d3d3ea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="displayName")
    def display_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "displayName"))

    @display_name.setter
    def display_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__76cde625c357c697363055d9778903f7556f2ff4429366505dec0397319438e0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "displayName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enableSpellCorrection")
    def enable_spell_correction(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enableSpellCorrection"))

    @enable_spell_correction.setter
    def enable_spell_correction(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__852f9a4bbdb359fce82d94e4ec9e1c19a2a3ce9055173ebf9741fb32ad338082)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableSpellCorrection", value) # pyright: ignore[reportArgumentType]

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
            type_hints = typing.get_type_hints(_typecheckingstub__9076bdd2a578519759a083b967238a1fe8a7f22236ea2c5546cb7be1b4f5ab77)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableStackdriverLogging", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__af559d9afdf65e776615de7bfe4984ce199773f4928c7767ebaa0b61d6755470)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f6144bab910f257b0b948dc47375128bd670cae3fe3c17b8ecd25584c51b849e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c1cc79a9c1491ecf859c84adc5762c52f705c16b40203907edf7ffb4320f9bb3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="securitySettings")
    def security_settings(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "securitySettings"))

    @security_settings.setter
    def security_settings(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__65c7b967aea01cb6fb2707be603fb0bbf07ed6b9f53a43f099002cd5e7c81ff8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "securitySettings", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="supportedLanguageCodes")
    def supported_language_codes(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "supportedLanguageCodes"))

    @supported_language_codes.setter
    def supported_language_codes(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa74fce4e5b331de1ab843d0f0fae51e53e2a011f0120f4c26638e8b9736b9ca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "supportedLanguageCodes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="timeZone")
    def time_zone(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "timeZone"))

    @time_zone.setter
    def time_zone(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2a60a74ebc2d61e20780b51fd6e21558a214487625a399fb079862df69f84431)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timeZone", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dialogflowCxAgent.DialogflowCxAgentAdvancedSettings",
    jsii_struct_bases=[],
    name_mapping={
        "audio_export_gcs_destination": "audioExportGcsDestination",
        "dtmf_settings": "dtmfSettings",
        "logging_settings": "loggingSettings",
        "speech_settings": "speechSettings",
    },
)
class DialogflowCxAgentAdvancedSettings:
    def __init__(
        self,
        *,
        audio_export_gcs_destination: typing.Optional[typing.Union["DialogflowCxAgentAdvancedSettingsAudioExportGcsDestination", typing.Dict[builtins.str, typing.Any]]] = None,
        dtmf_settings: typing.Optional[typing.Union["DialogflowCxAgentAdvancedSettingsDtmfSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        logging_settings: typing.Optional[typing.Union["DialogflowCxAgentAdvancedSettingsLoggingSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        speech_settings: typing.Optional[typing.Union["DialogflowCxAgentAdvancedSettingsSpeechSettings", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param audio_export_gcs_destination: audio_export_gcs_destination block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_agent#audio_export_gcs_destination DialogflowCxAgent#audio_export_gcs_destination}
        :param dtmf_settings: dtmf_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_agent#dtmf_settings DialogflowCxAgent#dtmf_settings}
        :param logging_settings: logging_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_agent#logging_settings DialogflowCxAgent#logging_settings}
        :param speech_settings: speech_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_agent#speech_settings DialogflowCxAgent#speech_settings}
        '''
        if isinstance(audio_export_gcs_destination, dict):
            audio_export_gcs_destination = DialogflowCxAgentAdvancedSettingsAudioExportGcsDestination(**audio_export_gcs_destination)
        if isinstance(dtmf_settings, dict):
            dtmf_settings = DialogflowCxAgentAdvancedSettingsDtmfSettings(**dtmf_settings)
        if isinstance(logging_settings, dict):
            logging_settings = DialogflowCxAgentAdvancedSettingsLoggingSettings(**logging_settings)
        if isinstance(speech_settings, dict):
            speech_settings = DialogflowCxAgentAdvancedSettingsSpeechSettings(**speech_settings)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a4ef011254bdedd274a441a86dadaddeda8b5a4ab84050e8a77259cd9f78c6da)
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
    ) -> typing.Optional["DialogflowCxAgentAdvancedSettingsAudioExportGcsDestination"]:
        '''audio_export_gcs_destination block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_agent#audio_export_gcs_destination DialogflowCxAgent#audio_export_gcs_destination}
        '''
        result = self._values.get("audio_export_gcs_destination")
        return typing.cast(typing.Optional["DialogflowCxAgentAdvancedSettingsAudioExportGcsDestination"], result)

    @builtins.property
    def dtmf_settings(
        self,
    ) -> typing.Optional["DialogflowCxAgentAdvancedSettingsDtmfSettings"]:
        '''dtmf_settings block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_agent#dtmf_settings DialogflowCxAgent#dtmf_settings}
        '''
        result = self._values.get("dtmf_settings")
        return typing.cast(typing.Optional["DialogflowCxAgentAdvancedSettingsDtmfSettings"], result)

    @builtins.property
    def logging_settings(
        self,
    ) -> typing.Optional["DialogflowCxAgentAdvancedSettingsLoggingSettings"]:
        '''logging_settings block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_agent#logging_settings DialogflowCxAgent#logging_settings}
        '''
        result = self._values.get("logging_settings")
        return typing.cast(typing.Optional["DialogflowCxAgentAdvancedSettingsLoggingSettings"], result)

    @builtins.property
    def speech_settings(
        self,
    ) -> typing.Optional["DialogflowCxAgentAdvancedSettingsSpeechSettings"]:
        '''speech_settings block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_agent#speech_settings DialogflowCxAgent#speech_settings}
        '''
        result = self._values.get("speech_settings")
        return typing.cast(typing.Optional["DialogflowCxAgentAdvancedSettingsSpeechSettings"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DialogflowCxAgentAdvancedSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dialogflowCxAgent.DialogflowCxAgentAdvancedSettingsAudioExportGcsDestination",
    jsii_struct_bases=[],
    name_mapping={"uri": "uri"},
)
class DialogflowCxAgentAdvancedSettingsAudioExportGcsDestination:
    def __init__(self, *, uri: typing.Optional[builtins.str] = None) -> None:
        '''
        :param uri: The Google Cloud Storage URI for the exported objects. Whether a full object name, or just a prefix, its usage depends on the Dialogflow operation. Format: gs://bucket/object-name-or-prefix Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_agent#uri DialogflowCxAgent#uri}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a13b1796fd04c2551b0272643e49874e1def2d40d0e3e3c9ffc1f5c0da58a578)
            check_type(argname="argument uri", value=uri, expected_type=type_hints["uri"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if uri is not None:
            self._values["uri"] = uri

    @builtins.property
    def uri(self) -> typing.Optional[builtins.str]:
        '''The Google Cloud Storage URI for the exported objects.

        Whether a full object name, or just a prefix, its usage depends on the Dialogflow operation.
        Format: gs://bucket/object-name-or-prefix

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_agent#uri DialogflowCxAgent#uri}
        '''
        result = self._values.get("uri")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DialogflowCxAgentAdvancedSettingsAudioExportGcsDestination(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DialogflowCxAgentAdvancedSettingsAudioExportGcsDestinationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dialogflowCxAgent.DialogflowCxAgentAdvancedSettingsAudioExportGcsDestinationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3b6724d7b658e6314e47041d7bd3b85812c01ccd229a82d6de4c677d784c230d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__327afc88dde179d5c29ec64396fdac7f110670ae71058285caf832aab00e4769)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "uri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DialogflowCxAgentAdvancedSettingsAudioExportGcsDestination]:
        return typing.cast(typing.Optional[DialogflowCxAgentAdvancedSettingsAudioExportGcsDestination], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DialogflowCxAgentAdvancedSettingsAudioExportGcsDestination],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__77331375ea49ea9fad6e0cf4912145311a01881c0de1bf42fbe4d981df1f63a3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dialogflowCxAgent.DialogflowCxAgentAdvancedSettingsDtmfSettings",
    jsii_struct_bases=[],
    name_mapping={
        "enabled": "enabled",
        "finish_digit": "finishDigit",
        "max_digits": "maxDigits",
    },
)
class DialogflowCxAgentAdvancedSettingsDtmfSettings:
    def __init__(
        self,
        *,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        finish_digit: typing.Optional[builtins.str] = None,
        max_digits: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param enabled: If true, incoming audio is processed for DTMF (dual tone multi frequency) events. For example, if the caller presses a button on their telephone keypad and DTMF processing is enabled, Dialogflow will detect the event (e.g. a "3" was pressed) in the incoming audio and pass the event to the bot to drive business logic (e.g. when 3 is pressed, return the account balance). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_agent#enabled DialogflowCxAgent#enabled}
        :param finish_digit: The digit that terminates a DTMF digit sequence. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_agent#finish_digit DialogflowCxAgent#finish_digit}
        :param max_digits: Max length of DTMF digits. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_agent#max_digits DialogflowCxAgent#max_digits}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__309bfd4ca87ed9f97ca14df367b79510ddd859af4b1c1c9b5f5b6400468f84a4)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_agent#enabled DialogflowCxAgent#enabled}
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def finish_digit(self) -> typing.Optional[builtins.str]:
        '''The digit that terminates a DTMF digit sequence.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_agent#finish_digit DialogflowCxAgent#finish_digit}
        '''
        result = self._values.get("finish_digit")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def max_digits(self) -> typing.Optional[jsii.Number]:
        '''Max length of DTMF digits.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_agent#max_digits DialogflowCxAgent#max_digits}
        '''
        result = self._values.get("max_digits")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DialogflowCxAgentAdvancedSettingsDtmfSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DialogflowCxAgentAdvancedSettingsDtmfSettingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dialogflowCxAgent.DialogflowCxAgentAdvancedSettingsDtmfSettingsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__db5d2f1647d0849572f5c0c8191eb167d8cfd008e8cdf259a8ae6f768d48e07f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0e137fff10c85299bd1dcb3b9feebe1f6aed8f3dba9b9325689f83e8209897cb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="finishDigit")
    def finish_digit(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "finishDigit"))

    @finish_digit.setter
    def finish_digit(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__90e990c37bdad50c2f2b01fb2b6d6b3424db487892f11844a7689f64dd751e83)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "finishDigit", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxDigits")
    def max_digits(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxDigits"))

    @max_digits.setter
    def max_digits(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__007472309a021a1d72a228d4e30e5c5acfa6715b46b3f64c5da3e196ab512ad3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxDigits", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DialogflowCxAgentAdvancedSettingsDtmfSettings]:
        return typing.cast(typing.Optional[DialogflowCxAgentAdvancedSettingsDtmfSettings], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DialogflowCxAgentAdvancedSettingsDtmfSettings],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2fc2f5da8dc098b31d66c0d388eb1f851d1749df38320e4df6f4cec37252d100)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dialogflowCxAgent.DialogflowCxAgentAdvancedSettingsLoggingSettings",
    jsii_struct_bases=[],
    name_mapping={
        "enable_consent_based_redaction": "enableConsentBasedRedaction",
        "enable_interaction_logging": "enableInteractionLogging",
        "enable_stackdriver_logging": "enableStackdriverLogging",
    },
)
class DialogflowCxAgentAdvancedSettingsLoggingSettings:
    def __init__(
        self,
        *,
        enable_consent_based_redaction: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_interaction_logging: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_stackdriver_logging: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param enable_consent_based_redaction: Enables consent-based end-user input redaction, if true, a pre-defined session parameter **$session.params.conversation-redaction** will be used to determine if the utterance should be redacted. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_agent#enable_consent_based_redaction DialogflowCxAgent#enable_consent_based_redaction}
        :param enable_interaction_logging: Enables DF Interaction logging. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_agent#enable_interaction_logging DialogflowCxAgent#enable_interaction_logging}
        :param enable_stackdriver_logging: Enables Google Cloud Logging. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_agent#enable_stackdriver_logging DialogflowCxAgent#enable_stackdriver_logging}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0b9e2b38e5255381aa68b8971e2b5820c094afad00f5b4d255cc2c73f6957fb5)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_agent#enable_consent_based_redaction DialogflowCxAgent#enable_consent_based_redaction}
        '''
        result = self._values.get("enable_consent_based_redaction")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def enable_interaction_logging(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Enables DF Interaction logging.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_agent#enable_interaction_logging DialogflowCxAgent#enable_interaction_logging}
        '''
        result = self._values.get("enable_interaction_logging")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def enable_stackdriver_logging(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Enables Google Cloud Logging.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_agent#enable_stackdriver_logging DialogflowCxAgent#enable_stackdriver_logging}
        '''
        result = self._values.get("enable_stackdriver_logging")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DialogflowCxAgentAdvancedSettingsLoggingSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DialogflowCxAgentAdvancedSettingsLoggingSettingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dialogflowCxAgent.DialogflowCxAgentAdvancedSettingsLoggingSettingsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__80d7ef0e77591b64bd5f860af136b35096676263837e83f149851abe6afe89eb)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5cce831812eedcd9bec976503a52248ccfffea3ba06f733adbfcc38861075a8c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bb895a5bcb5457e2b064c625a9d79cfa0a18022187da8e75bbe0f446d62ebc92)
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
            type_hints = typing.get_type_hints(_typecheckingstub__62b66a4a4eba029e06afa7f031417d527d146fce9637e6e8064495f104b29c5a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableStackdriverLogging", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DialogflowCxAgentAdvancedSettingsLoggingSettings]:
        return typing.cast(typing.Optional[DialogflowCxAgentAdvancedSettingsLoggingSettings], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DialogflowCxAgentAdvancedSettingsLoggingSettings],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6242327b451c39df52b8f8588c62cb3f6fadc560b8f1f42067c46dd8cecaeca3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DialogflowCxAgentAdvancedSettingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dialogflowCxAgent.DialogflowCxAgentAdvancedSettingsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__baa11be897f83b4c88612729658d69a9abbf4b014d7b4c779e7872710de01453)
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
        :param uri: The Google Cloud Storage URI for the exported objects. Whether a full object name, or just a prefix, its usage depends on the Dialogflow operation. Format: gs://bucket/object-name-or-prefix Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_agent#uri DialogflowCxAgent#uri}
        '''
        value = DialogflowCxAgentAdvancedSettingsAudioExportGcsDestination(uri=uri)

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
        :param enabled: If true, incoming audio is processed for DTMF (dual tone multi frequency) events. For example, if the caller presses a button on their telephone keypad and DTMF processing is enabled, Dialogflow will detect the event (e.g. a "3" was pressed) in the incoming audio and pass the event to the bot to drive business logic (e.g. when 3 is pressed, return the account balance). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_agent#enabled DialogflowCxAgent#enabled}
        :param finish_digit: The digit that terminates a DTMF digit sequence. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_agent#finish_digit DialogflowCxAgent#finish_digit}
        :param max_digits: Max length of DTMF digits. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_agent#max_digits DialogflowCxAgent#max_digits}
        '''
        value = DialogflowCxAgentAdvancedSettingsDtmfSettings(
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
        :param enable_consent_based_redaction: Enables consent-based end-user input redaction, if true, a pre-defined session parameter **$session.params.conversation-redaction** will be used to determine if the utterance should be redacted. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_agent#enable_consent_based_redaction DialogflowCxAgent#enable_consent_based_redaction}
        :param enable_interaction_logging: Enables DF Interaction logging. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_agent#enable_interaction_logging DialogflowCxAgent#enable_interaction_logging}
        :param enable_stackdriver_logging: Enables Google Cloud Logging. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_agent#enable_stackdriver_logging DialogflowCxAgent#enable_stackdriver_logging}
        '''
        value = DialogflowCxAgentAdvancedSettingsLoggingSettings(
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
        :param endpointer_sensitivity: Sensitivity of the speech model that detects the end of speech. Scale from 0 to 100. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_agent#endpointer_sensitivity DialogflowCxAgent#endpointer_sensitivity}
        :param models: Mapping from language to Speech-to-Text model. The mapped Speech-to-Text model will be selected for requests from its corresponding language. For more information, see `Speech models <https://cloud.google.com/dialogflow/cx/docs/concept/speech-models>`_. An object containing a list of **"key": value** pairs. Example: **{ "name": "wrench", "mass": "1.3kg", "count": "3" }**. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_agent#models DialogflowCxAgent#models}
        :param no_speech_timeout: Timeout before detecting no speech. A duration in seconds with up to nine fractional digits, ending with 's'. Example: "3.5s". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_agent#no_speech_timeout DialogflowCxAgent#no_speech_timeout}
        :param use_timeout_based_endpointing: Use timeout based endpointing, interpreting endpointer sensitivity as seconds of timeout value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_agent#use_timeout_based_endpointing DialogflowCxAgent#use_timeout_based_endpointing}
        '''
        value = DialogflowCxAgentAdvancedSettingsSpeechSettings(
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
    ) -> DialogflowCxAgentAdvancedSettingsAudioExportGcsDestinationOutputReference:
        return typing.cast(DialogflowCxAgentAdvancedSettingsAudioExportGcsDestinationOutputReference, jsii.get(self, "audioExportGcsDestination"))

    @builtins.property
    @jsii.member(jsii_name="dtmfSettings")
    def dtmf_settings(
        self,
    ) -> DialogflowCxAgentAdvancedSettingsDtmfSettingsOutputReference:
        return typing.cast(DialogflowCxAgentAdvancedSettingsDtmfSettingsOutputReference, jsii.get(self, "dtmfSettings"))

    @builtins.property
    @jsii.member(jsii_name="loggingSettings")
    def logging_settings(
        self,
    ) -> DialogflowCxAgentAdvancedSettingsLoggingSettingsOutputReference:
        return typing.cast(DialogflowCxAgentAdvancedSettingsLoggingSettingsOutputReference, jsii.get(self, "loggingSettings"))

    @builtins.property
    @jsii.member(jsii_name="speechSettings")
    def speech_settings(
        self,
    ) -> "DialogflowCxAgentAdvancedSettingsSpeechSettingsOutputReference":
        return typing.cast("DialogflowCxAgentAdvancedSettingsSpeechSettingsOutputReference", jsii.get(self, "speechSettings"))

    @builtins.property
    @jsii.member(jsii_name="audioExportGcsDestinationInput")
    def audio_export_gcs_destination_input(
        self,
    ) -> typing.Optional[DialogflowCxAgentAdvancedSettingsAudioExportGcsDestination]:
        return typing.cast(typing.Optional[DialogflowCxAgentAdvancedSettingsAudioExportGcsDestination], jsii.get(self, "audioExportGcsDestinationInput"))

    @builtins.property
    @jsii.member(jsii_name="dtmfSettingsInput")
    def dtmf_settings_input(
        self,
    ) -> typing.Optional[DialogflowCxAgentAdvancedSettingsDtmfSettings]:
        return typing.cast(typing.Optional[DialogflowCxAgentAdvancedSettingsDtmfSettings], jsii.get(self, "dtmfSettingsInput"))

    @builtins.property
    @jsii.member(jsii_name="loggingSettingsInput")
    def logging_settings_input(
        self,
    ) -> typing.Optional[DialogflowCxAgentAdvancedSettingsLoggingSettings]:
        return typing.cast(typing.Optional[DialogflowCxAgentAdvancedSettingsLoggingSettings], jsii.get(self, "loggingSettingsInput"))

    @builtins.property
    @jsii.member(jsii_name="speechSettingsInput")
    def speech_settings_input(
        self,
    ) -> typing.Optional["DialogflowCxAgentAdvancedSettingsSpeechSettings"]:
        return typing.cast(typing.Optional["DialogflowCxAgentAdvancedSettingsSpeechSettings"], jsii.get(self, "speechSettingsInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[DialogflowCxAgentAdvancedSettings]:
        return typing.cast(typing.Optional[DialogflowCxAgentAdvancedSettings], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DialogflowCxAgentAdvancedSettings],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c1a0c12e169f59fa751cddfceab869b005bd6fe8278cec8bd08a2e6ce5cb9cbb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dialogflowCxAgent.DialogflowCxAgentAdvancedSettingsSpeechSettings",
    jsii_struct_bases=[],
    name_mapping={
        "endpointer_sensitivity": "endpointerSensitivity",
        "models": "models",
        "no_speech_timeout": "noSpeechTimeout",
        "use_timeout_based_endpointing": "useTimeoutBasedEndpointing",
    },
)
class DialogflowCxAgentAdvancedSettingsSpeechSettings:
    def __init__(
        self,
        *,
        endpointer_sensitivity: typing.Optional[jsii.Number] = None,
        models: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        no_speech_timeout: typing.Optional[builtins.str] = None,
        use_timeout_based_endpointing: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param endpointer_sensitivity: Sensitivity of the speech model that detects the end of speech. Scale from 0 to 100. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_agent#endpointer_sensitivity DialogflowCxAgent#endpointer_sensitivity}
        :param models: Mapping from language to Speech-to-Text model. The mapped Speech-to-Text model will be selected for requests from its corresponding language. For more information, see `Speech models <https://cloud.google.com/dialogflow/cx/docs/concept/speech-models>`_. An object containing a list of **"key": value** pairs. Example: **{ "name": "wrench", "mass": "1.3kg", "count": "3" }**. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_agent#models DialogflowCxAgent#models}
        :param no_speech_timeout: Timeout before detecting no speech. A duration in seconds with up to nine fractional digits, ending with 's'. Example: "3.5s". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_agent#no_speech_timeout DialogflowCxAgent#no_speech_timeout}
        :param use_timeout_based_endpointing: Use timeout based endpointing, interpreting endpointer sensitivity as seconds of timeout value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_agent#use_timeout_based_endpointing DialogflowCxAgent#use_timeout_based_endpointing}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__01f57f97f6af01b3217d3c01d6623e5550df4c8221b6548bb9fb7680af6d032e)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_agent#endpointer_sensitivity DialogflowCxAgent#endpointer_sensitivity}
        '''
        result = self._values.get("endpointer_sensitivity")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def models(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Mapping from language to Speech-to-Text model.

        The mapped Speech-to-Text model will be selected for requests from its corresponding language. For more information, see `Speech models <https://cloud.google.com/dialogflow/cx/docs/concept/speech-models>`_.
        An object containing a list of **"key": value** pairs. Example: **{ "name": "wrench", "mass": "1.3kg", "count": "3" }**.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_agent#models DialogflowCxAgent#models}
        '''
        result = self._values.get("models")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def no_speech_timeout(self) -> typing.Optional[builtins.str]:
        '''Timeout before detecting no speech. A duration in seconds with up to nine fractional digits, ending with 's'. Example: "3.5s".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_agent#no_speech_timeout DialogflowCxAgent#no_speech_timeout}
        '''
        result = self._values.get("no_speech_timeout")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def use_timeout_based_endpointing(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Use timeout based endpointing, interpreting endpointer sensitivity as seconds of timeout value.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_agent#use_timeout_based_endpointing DialogflowCxAgent#use_timeout_based_endpointing}
        '''
        result = self._values.get("use_timeout_based_endpointing")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DialogflowCxAgentAdvancedSettingsSpeechSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DialogflowCxAgentAdvancedSettingsSpeechSettingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dialogflowCxAgent.DialogflowCxAgentAdvancedSettingsSpeechSettingsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f2b1c1ab6c1a086820eae5a63505a67e5ccd9314449632cbe727b0dbef5dc228)
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
            type_hints = typing.get_type_hints(_typecheckingstub__45e570f0fba1ae5d5c628a90e62541d159d917f6aef134d5addda1e25b7c6ce7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "endpointerSensitivity", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="models")
    def models(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "models"))

    @models.setter
    def models(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e8f2c5bf00796a68328d0ce83e592669834115b259b6b333549990381b96193)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "models", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="noSpeechTimeout")
    def no_speech_timeout(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "noSpeechTimeout"))

    @no_speech_timeout.setter
    def no_speech_timeout(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0571a67b67d2a997eec8e4bc123ca36afe4cf65d1bafcb7282f6d22c165b54b7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bb2a098d41c1e4f441cecc8a39066fc7910edbc189bc82552ce0e5b4e068856c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "useTimeoutBasedEndpointing", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DialogflowCxAgentAdvancedSettingsSpeechSettings]:
        return typing.cast(typing.Optional[DialogflowCxAgentAdvancedSettingsSpeechSettings], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DialogflowCxAgentAdvancedSettingsSpeechSettings],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6a2379f9a03e0abb947bb0b09f3d52c2970bf436a73ae5849971e99f4209e077)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dialogflowCxAgent.DialogflowCxAgentConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "default_language_code": "defaultLanguageCode",
        "display_name": "displayName",
        "location": "location",
        "time_zone": "timeZone",
        "advanced_settings": "advancedSettings",
        "avatar_uri": "avatarUri",
        "delete_chat_engine_on_destroy": "deleteChatEngineOnDestroy",
        "description": "description",
        "enable_spell_correction": "enableSpellCorrection",
        "enable_stackdriver_logging": "enableStackdriverLogging",
        "gen_app_builder_settings": "genAppBuilderSettings",
        "git_integration_settings": "gitIntegrationSettings",
        "id": "id",
        "project": "project",
        "security_settings": "securitySettings",
        "speech_to_text_settings": "speechToTextSettings",
        "supported_language_codes": "supportedLanguageCodes",
        "text_to_speech_settings": "textToSpeechSettings",
        "timeouts": "timeouts",
    },
)
class DialogflowCxAgentConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        default_language_code: builtins.str,
        display_name: builtins.str,
        location: builtins.str,
        time_zone: builtins.str,
        advanced_settings: typing.Optional[typing.Union[DialogflowCxAgentAdvancedSettings, typing.Dict[builtins.str, typing.Any]]] = None,
        avatar_uri: typing.Optional[builtins.str] = None,
        delete_chat_engine_on_destroy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        description: typing.Optional[builtins.str] = None,
        enable_spell_correction: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_stackdriver_logging: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        gen_app_builder_settings: typing.Optional[typing.Union["DialogflowCxAgentGenAppBuilderSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        git_integration_settings: typing.Optional[typing.Union["DialogflowCxAgentGitIntegrationSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        security_settings: typing.Optional[builtins.str] = None,
        speech_to_text_settings: typing.Optional[typing.Union["DialogflowCxAgentSpeechToTextSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        supported_language_codes: typing.Optional[typing.Sequence[builtins.str]] = None,
        text_to_speech_settings: typing.Optional[typing.Union["DialogflowCxAgentTextToSpeechSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["DialogflowCxAgentTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param default_language_code: The default language of the agent as a language tag. `See Language Support <https://cloud.google.com/dialogflow/cx/docs/reference/language>`_ for a list of the currently supported language codes. This field cannot be updated after creation. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_agent#default_language_code DialogflowCxAgent#default_language_code}
        :param display_name: The human-readable name of the agent, unique within the location. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_agent#display_name DialogflowCxAgent#display_name}
        :param location: The name of the location this agent is located in. ~> **Note:** The first time you are deploying an Agent in your project you must configure location settings. This is a one time step but at the moment you can only `configure location settings <https://cloud.google.com/dialogflow/cx/docs/concept/region#location-settings>`_ via the Dialogflow CX console. Another options is to use global location so you don't need to manually configure location settings. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_agent#location DialogflowCxAgent#location}
        :param time_zone: The time zone of this agent from the `time zone database <https://www.iana.org/time-zones>`_, e.g., America/New_York, Europe/Paris. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_agent#time_zone DialogflowCxAgent#time_zone}
        :param advanced_settings: advanced_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_agent#advanced_settings DialogflowCxAgent#advanced_settings}
        :param avatar_uri: The URI of the agent's avatar. Avatars are used throughout the Dialogflow console and in the self-hosted Web Demo integration. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_agent#avatar_uri DialogflowCxAgent#avatar_uri}
        :param delete_chat_engine_on_destroy: If set to 'true', Terraform will delete the chat engine associated with the agent when the agent is destroyed. Otherwise, the chat engine will persist. This virtual field addresses a critical dependency chain: 'agent' -> 'engine' -> 'data store'. The chat engine is automatically provisioned when a data store is linked to the agent, meaning Terraform doesn't have direct control over its lifecycle as a managed resource. This creates a problem when both the agent and data store are managed by Terraform and need to be destroyed. Without delete_chat_engine_on_destroy set to true, the data store's deletion would fail because the unmanaged chat engine would still be using it. This setting ensures that the entire dependency chain can be properly torn down. See 'mmv1/templates/terraform/examples/dialogflowcx_tool_data_store.tf.tmpl' as an example. Data store can be linked to an agent through the 'knowledgeConnectorSettings' field of a `flow <https://cloud.google.com/dialogflow/cx/docs/reference/rest/v3/projects.locations.agents.flows#resource:-flow>`_ or a `page <https://cloud.google.com/dialogflow/cx/docs/reference/rest/v3/projects.locations.agents.flows.pages#resource:-page>`_ or the 'dataStoreSpec' field of a `tool <https://cloud.google.com/dialogflow/cx/docs/reference/rest/v3/projects.locations.agents.tools#resource:-tool>`_. The ID of the implicitly created engine is stored in the 'genAppBuilderSettings' field of the `agent <https://cloud.google.com/dialogflow/cx/docs/reference/rest/v3/projects.locations.agents#resource:-agent>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_agent#delete_chat_engine_on_destroy DialogflowCxAgent#delete_chat_engine_on_destroy}
        :param description: The description of this agent. The maximum length is 500 characters. If exceeded, the request is rejected. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_agent#description DialogflowCxAgent#description}
        :param enable_spell_correction: Indicates if automatic spell correction is enabled in detect intent requests. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_agent#enable_spell_correction DialogflowCxAgent#enable_spell_correction}
        :param enable_stackdriver_logging: Determines whether this agent should log conversation queries. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_agent#enable_stackdriver_logging DialogflowCxAgent#enable_stackdriver_logging}
        :param gen_app_builder_settings: gen_app_builder_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_agent#gen_app_builder_settings DialogflowCxAgent#gen_app_builder_settings}
        :param git_integration_settings: git_integration_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_agent#git_integration_settings DialogflowCxAgent#git_integration_settings}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_agent#id DialogflowCxAgent#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_agent#project DialogflowCxAgent#project}.
        :param security_settings: Name of the SecuritySettings reference for the agent. Format: projects//locations//securitySettings/. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_agent#security_settings DialogflowCxAgent#security_settings}
        :param speech_to_text_settings: speech_to_text_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_agent#speech_to_text_settings DialogflowCxAgent#speech_to_text_settings}
        :param supported_language_codes: The list of all languages supported by this agent (except for the default_language_code). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_agent#supported_language_codes DialogflowCxAgent#supported_language_codes}
        :param text_to_speech_settings: text_to_speech_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_agent#text_to_speech_settings DialogflowCxAgent#text_to_speech_settings}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_agent#timeouts DialogflowCxAgent#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(advanced_settings, dict):
            advanced_settings = DialogflowCxAgentAdvancedSettings(**advanced_settings)
        if isinstance(gen_app_builder_settings, dict):
            gen_app_builder_settings = DialogflowCxAgentGenAppBuilderSettings(**gen_app_builder_settings)
        if isinstance(git_integration_settings, dict):
            git_integration_settings = DialogflowCxAgentGitIntegrationSettings(**git_integration_settings)
        if isinstance(speech_to_text_settings, dict):
            speech_to_text_settings = DialogflowCxAgentSpeechToTextSettings(**speech_to_text_settings)
        if isinstance(text_to_speech_settings, dict):
            text_to_speech_settings = DialogflowCxAgentTextToSpeechSettings(**text_to_speech_settings)
        if isinstance(timeouts, dict):
            timeouts = DialogflowCxAgentTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f1cdc3ec5885cae236dbed1fab750af37905b761eb071a01995f6899822650c1)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument default_language_code", value=default_language_code, expected_type=type_hints["default_language_code"])
            check_type(argname="argument display_name", value=display_name, expected_type=type_hints["display_name"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument time_zone", value=time_zone, expected_type=type_hints["time_zone"])
            check_type(argname="argument advanced_settings", value=advanced_settings, expected_type=type_hints["advanced_settings"])
            check_type(argname="argument avatar_uri", value=avatar_uri, expected_type=type_hints["avatar_uri"])
            check_type(argname="argument delete_chat_engine_on_destroy", value=delete_chat_engine_on_destroy, expected_type=type_hints["delete_chat_engine_on_destroy"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument enable_spell_correction", value=enable_spell_correction, expected_type=type_hints["enable_spell_correction"])
            check_type(argname="argument enable_stackdriver_logging", value=enable_stackdriver_logging, expected_type=type_hints["enable_stackdriver_logging"])
            check_type(argname="argument gen_app_builder_settings", value=gen_app_builder_settings, expected_type=type_hints["gen_app_builder_settings"])
            check_type(argname="argument git_integration_settings", value=git_integration_settings, expected_type=type_hints["git_integration_settings"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument security_settings", value=security_settings, expected_type=type_hints["security_settings"])
            check_type(argname="argument speech_to_text_settings", value=speech_to_text_settings, expected_type=type_hints["speech_to_text_settings"])
            check_type(argname="argument supported_language_codes", value=supported_language_codes, expected_type=type_hints["supported_language_codes"])
            check_type(argname="argument text_to_speech_settings", value=text_to_speech_settings, expected_type=type_hints["text_to_speech_settings"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "default_language_code": default_language_code,
            "display_name": display_name,
            "location": location,
            "time_zone": time_zone,
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
        if avatar_uri is not None:
            self._values["avatar_uri"] = avatar_uri
        if delete_chat_engine_on_destroy is not None:
            self._values["delete_chat_engine_on_destroy"] = delete_chat_engine_on_destroy
        if description is not None:
            self._values["description"] = description
        if enable_spell_correction is not None:
            self._values["enable_spell_correction"] = enable_spell_correction
        if enable_stackdriver_logging is not None:
            self._values["enable_stackdriver_logging"] = enable_stackdriver_logging
        if gen_app_builder_settings is not None:
            self._values["gen_app_builder_settings"] = gen_app_builder_settings
        if git_integration_settings is not None:
            self._values["git_integration_settings"] = git_integration_settings
        if id is not None:
            self._values["id"] = id
        if project is not None:
            self._values["project"] = project
        if security_settings is not None:
            self._values["security_settings"] = security_settings
        if speech_to_text_settings is not None:
            self._values["speech_to_text_settings"] = speech_to_text_settings
        if supported_language_codes is not None:
            self._values["supported_language_codes"] = supported_language_codes
        if text_to_speech_settings is not None:
            self._values["text_to_speech_settings"] = text_to_speech_settings
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
    def default_language_code(self) -> builtins.str:
        '''The default language of the agent as a language tag.

        `See Language Support <https://cloud.google.com/dialogflow/cx/docs/reference/language>`_
        for a list of the currently supported language codes. This field cannot be updated after creation.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_agent#default_language_code DialogflowCxAgent#default_language_code}
        '''
        result = self._values.get("default_language_code")
        assert result is not None, "Required property 'default_language_code' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def display_name(self) -> builtins.str:
        '''The human-readable name of the agent, unique within the location.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_agent#display_name DialogflowCxAgent#display_name}
        '''
        result = self._values.get("display_name")
        assert result is not None, "Required property 'display_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def location(self) -> builtins.str:
        '''The name of the location this agent is located in.

        ~> **Note:** The first time you are deploying an Agent in your project you must configure location settings.
        This is a one time step but at the moment you can only `configure location settings <https://cloud.google.com/dialogflow/cx/docs/concept/region#location-settings>`_ via the Dialogflow CX console.
        Another options is to use global location so you don't need to manually configure location settings.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_agent#location DialogflowCxAgent#location}
        '''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def time_zone(self) -> builtins.str:
        '''The time zone of this agent from the `time zone database <https://www.iana.org/time-zones>`_, e.g., America/New_York, Europe/Paris.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_agent#time_zone DialogflowCxAgent#time_zone}
        '''
        result = self._values.get("time_zone")
        assert result is not None, "Required property 'time_zone' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def advanced_settings(self) -> typing.Optional[DialogflowCxAgentAdvancedSettings]:
        '''advanced_settings block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_agent#advanced_settings DialogflowCxAgent#advanced_settings}
        '''
        result = self._values.get("advanced_settings")
        return typing.cast(typing.Optional[DialogflowCxAgentAdvancedSettings], result)

    @builtins.property
    def avatar_uri(self) -> typing.Optional[builtins.str]:
        '''The URI of the agent's avatar.

        Avatars are used throughout the Dialogflow console and in the self-hosted Web Demo integration.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_agent#avatar_uri DialogflowCxAgent#avatar_uri}
        '''
        result = self._values.get("avatar_uri")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete_chat_engine_on_destroy(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If set to 'true', Terraform will delete the chat engine associated with the agent when the agent is destroyed.

        Otherwise, the chat engine will persist.

        This virtual field addresses a critical dependency chain: 'agent' -> 'engine' -> 'data store'. The chat engine is automatically
        provisioned when a data store is linked to the agent, meaning Terraform doesn't have direct control over its lifecycle as a managed
        resource. This creates a problem when both the agent and data store are managed by Terraform and need to be destroyed. Without
        delete_chat_engine_on_destroy set to true, the data store's deletion would fail because the unmanaged chat engine would still be
        using it. This setting ensures that the entire dependency chain can be properly torn down.
        See 'mmv1/templates/terraform/examples/dialogflowcx_tool_data_store.tf.tmpl' as an example.

        Data store can be linked to an agent through the 'knowledgeConnectorSettings' field of a `flow <https://cloud.google.com/dialogflow/cx/docs/reference/rest/v3/projects.locations.agents.flows#resource:-flow>`_
        or a `page <https://cloud.google.com/dialogflow/cx/docs/reference/rest/v3/projects.locations.agents.flows.pages#resource:-page>`_
        or the 'dataStoreSpec' field of a `tool <https://cloud.google.com/dialogflow/cx/docs/reference/rest/v3/projects.locations.agents.tools#resource:-tool>`_.
        The ID of the implicitly created engine is stored in the 'genAppBuilderSettings' field of the `agent <https://cloud.google.com/dialogflow/cx/docs/reference/rest/v3/projects.locations.agents#resource:-agent>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_agent#delete_chat_engine_on_destroy DialogflowCxAgent#delete_chat_engine_on_destroy}
        '''
        result = self._values.get("delete_chat_engine_on_destroy")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of this agent. The maximum length is 500 characters. If exceeded, the request is rejected.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_agent#description DialogflowCxAgent#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enable_spell_correction(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Indicates if automatic spell correction is enabled in detect intent requests.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_agent#enable_spell_correction DialogflowCxAgent#enable_spell_correction}
        '''
        result = self._values.get("enable_spell_correction")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def enable_stackdriver_logging(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Determines whether this agent should log conversation queries.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_agent#enable_stackdriver_logging DialogflowCxAgent#enable_stackdriver_logging}
        '''
        result = self._values.get("enable_stackdriver_logging")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def gen_app_builder_settings(
        self,
    ) -> typing.Optional["DialogflowCxAgentGenAppBuilderSettings"]:
        '''gen_app_builder_settings block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_agent#gen_app_builder_settings DialogflowCxAgent#gen_app_builder_settings}
        '''
        result = self._values.get("gen_app_builder_settings")
        return typing.cast(typing.Optional["DialogflowCxAgentGenAppBuilderSettings"], result)

    @builtins.property
    def git_integration_settings(
        self,
    ) -> typing.Optional["DialogflowCxAgentGitIntegrationSettings"]:
        '''git_integration_settings block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_agent#git_integration_settings DialogflowCxAgent#git_integration_settings}
        '''
        result = self._values.get("git_integration_settings")
        return typing.cast(typing.Optional["DialogflowCxAgentGitIntegrationSettings"], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_agent#id DialogflowCxAgent#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_agent#project DialogflowCxAgent#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def security_settings(self) -> typing.Optional[builtins.str]:
        '''Name of the SecuritySettings reference for the agent. Format: projects//locations//securitySettings/.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_agent#security_settings DialogflowCxAgent#security_settings}
        '''
        result = self._values.get("security_settings")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def speech_to_text_settings(
        self,
    ) -> typing.Optional["DialogflowCxAgentSpeechToTextSettings"]:
        '''speech_to_text_settings block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_agent#speech_to_text_settings DialogflowCxAgent#speech_to_text_settings}
        '''
        result = self._values.get("speech_to_text_settings")
        return typing.cast(typing.Optional["DialogflowCxAgentSpeechToTextSettings"], result)

    @builtins.property
    def supported_language_codes(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The list of all languages supported by this agent (except for the default_language_code).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_agent#supported_language_codes DialogflowCxAgent#supported_language_codes}
        '''
        result = self._values.get("supported_language_codes")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def text_to_speech_settings(
        self,
    ) -> typing.Optional["DialogflowCxAgentTextToSpeechSettings"]:
        '''text_to_speech_settings block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_agent#text_to_speech_settings DialogflowCxAgent#text_to_speech_settings}
        '''
        result = self._values.get("text_to_speech_settings")
        return typing.cast(typing.Optional["DialogflowCxAgentTextToSpeechSettings"], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["DialogflowCxAgentTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_agent#timeouts DialogflowCxAgent#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["DialogflowCxAgentTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DialogflowCxAgentConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dialogflowCxAgent.DialogflowCxAgentGenAppBuilderSettings",
    jsii_struct_bases=[],
    name_mapping={"engine": "engine"},
)
class DialogflowCxAgentGenAppBuilderSettings:
    def __init__(self, *, engine: builtins.str) -> None:
        '''
        :param engine: The full name of the Gen App Builder engine related to this agent if there is one. Format: projects/{Project ID}/locations/{Location ID}/collections/{Collection ID}/engines/{Engine ID} Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_agent#engine DialogflowCxAgent#engine}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__471887f4da87e30edaf305b8914ee440c3b479aee813785e5c9a3a913270e98f)
            check_type(argname="argument engine", value=engine, expected_type=type_hints["engine"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "engine": engine,
        }

    @builtins.property
    def engine(self) -> builtins.str:
        '''The full name of the Gen App Builder engine related to this agent if there is one.

        Format: projects/{Project ID}/locations/{Location ID}/collections/{Collection ID}/engines/{Engine ID}

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_agent#engine DialogflowCxAgent#engine}
        '''
        result = self._values.get("engine")
        assert result is not None, "Required property 'engine' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DialogflowCxAgentGenAppBuilderSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DialogflowCxAgentGenAppBuilderSettingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dialogflowCxAgent.DialogflowCxAgentGenAppBuilderSettingsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__537849b133f80b84a42b8e9e85b8b02fc1c8bbae8bdbd5a0920bc5fd5d167231)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="engineInput")
    def engine_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "engineInput"))

    @builtins.property
    @jsii.member(jsii_name="engine")
    def engine(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "engine"))

    @engine.setter
    def engine(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f5ee16c4177b307814bf37f218c398101d4307d268506b0d8427a14c1c0a058)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "engine", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[DialogflowCxAgentGenAppBuilderSettings]:
        return typing.cast(typing.Optional[DialogflowCxAgentGenAppBuilderSettings], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DialogflowCxAgentGenAppBuilderSettings],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b760b217a582df2b7bd79909b42bfaff0762a49b297e5ca731de1bc7ccdb7149)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dialogflowCxAgent.DialogflowCxAgentGitIntegrationSettings",
    jsii_struct_bases=[],
    name_mapping={"github_settings": "githubSettings"},
)
class DialogflowCxAgentGitIntegrationSettings:
    def __init__(
        self,
        *,
        github_settings: typing.Optional[typing.Union["DialogflowCxAgentGitIntegrationSettingsGithubSettings", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param github_settings: github_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_agent#github_settings DialogflowCxAgent#github_settings}
        '''
        if isinstance(github_settings, dict):
            github_settings = DialogflowCxAgentGitIntegrationSettingsGithubSettings(**github_settings)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b170084649e428d18414a88f125d21c64d81b4b6ae1a7c140e04697450a9b7aa)
            check_type(argname="argument github_settings", value=github_settings, expected_type=type_hints["github_settings"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if github_settings is not None:
            self._values["github_settings"] = github_settings

    @builtins.property
    def github_settings(
        self,
    ) -> typing.Optional["DialogflowCxAgentGitIntegrationSettingsGithubSettings"]:
        '''github_settings block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_agent#github_settings DialogflowCxAgent#github_settings}
        '''
        result = self._values.get("github_settings")
        return typing.cast(typing.Optional["DialogflowCxAgentGitIntegrationSettingsGithubSettings"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DialogflowCxAgentGitIntegrationSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dialogflowCxAgent.DialogflowCxAgentGitIntegrationSettingsGithubSettings",
    jsii_struct_bases=[],
    name_mapping={
        "access_token": "accessToken",
        "branches": "branches",
        "display_name": "displayName",
        "repository_uri": "repositoryUri",
        "tracking_branch": "trackingBranch",
    },
)
class DialogflowCxAgentGitIntegrationSettingsGithubSettings:
    def __init__(
        self,
        *,
        access_token: typing.Optional[builtins.str] = None,
        branches: typing.Optional[typing.Sequence[builtins.str]] = None,
        display_name: typing.Optional[builtins.str] = None,
        repository_uri: typing.Optional[builtins.str] = None,
        tracking_branch: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param access_token: The access token used to authenticate the access to the GitHub repository. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_agent#access_token DialogflowCxAgent#access_token}
        :param branches: A list of branches configured to be used from Dialogflow. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_agent#branches DialogflowCxAgent#branches}
        :param display_name: The unique repository display name for the GitHub repository. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_agent#display_name DialogflowCxAgent#display_name}
        :param repository_uri: The GitHub repository URI related to the agent. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_agent#repository_uri DialogflowCxAgent#repository_uri}
        :param tracking_branch: The branch of the GitHub repository tracked for this agent. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_agent#tracking_branch DialogflowCxAgent#tracking_branch}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cdbf7722d2eb10c1c97a4674f34774f267f5b7d44d9c8fc25fb58ffc99ad6576)
            check_type(argname="argument access_token", value=access_token, expected_type=type_hints["access_token"])
            check_type(argname="argument branches", value=branches, expected_type=type_hints["branches"])
            check_type(argname="argument display_name", value=display_name, expected_type=type_hints["display_name"])
            check_type(argname="argument repository_uri", value=repository_uri, expected_type=type_hints["repository_uri"])
            check_type(argname="argument tracking_branch", value=tracking_branch, expected_type=type_hints["tracking_branch"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if access_token is not None:
            self._values["access_token"] = access_token
        if branches is not None:
            self._values["branches"] = branches
        if display_name is not None:
            self._values["display_name"] = display_name
        if repository_uri is not None:
            self._values["repository_uri"] = repository_uri
        if tracking_branch is not None:
            self._values["tracking_branch"] = tracking_branch

    @builtins.property
    def access_token(self) -> typing.Optional[builtins.str]:
        '''The access token used to authenticate the access to the GitHub repository.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_agent#access_token DialogflowCxAgent#access_token}
        '''
        result = self._values.get("access_token")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def branches(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of branches configured to be used from Dialogflow.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_agent#branches DialogflowCxAgent#branches}
        '''
        result = self._values.get("branches")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def display_name(self) -> typing.Optional[builtins.str]:
        '''The unique repository display name for the GitHub repository.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_agent#display_name DialogflowCxAgent#display_name}
        '''
        result = self._values.get("display_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def repository_uri(self) -> typing.Optional[builtins.str]:
        '''The GitHub repository URI related to the agent.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_agent#repository_uri DialogflowCxAgent#repository_uri}
        '''
        result = self._values.get("repository_uri")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tracking_branch(self) -> typing.Optional[builtins.str]:
        '''The branch of the GitHub repository tracked for this agent.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_agent#tracking_branch DialogflowCxAgent#tracking_branch}
        '''
        result = self._values.get("tracking_branch")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DialogflowCxAgentGitIntegrationSettingsGithubSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DialogflowCxAgentGitIntegrationSettingsGithubSettingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dialogflowCxAgent.DialogflowCxAgentGitIntegrationSettingsGithubSettingsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4e2701bd94e040cf1d1cfbd301e92a302555d49fba925c7dd0d44723f5384171)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAccessToken")
    def reset_access_token(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAccessToken", []))

    @jsii.member(jsii_name="resetBranches")
    def reset_branches(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBranches", []))

    @jsii.member(jsii_name="resetDisplayName")
    def reset_display_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDisplayName", []))

    @jsii.member(jsii_name="resetRepositoryUri")
    def reset_repository_uri(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRepositoryUri", []))

    @jsii.member(jsii_name="resetTrackingBranch")
    def reset_tracking_branch(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTrackingBranch", []))

    @builtins.property
    @jsii.member(jsii_name="accessTokenInput")
    def access_token_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "accessTokenInput"))

    @builtins.property
    @jsii.member(jsii_name="branchesInput")
    def branches_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "branchesInput"))

    @builtins.property
    @jsii.member(jsii_name="displayNameInput")
    def display_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "displayNameInput"))

    @builtins.property
    @jsii.member(jsii_name="repositoryUriInput")
    def repository_uri_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "repositoryUriInput"))

    @builtins.property
    @jsii.member(jsii_name="trackingBranchInput")
    def tracking_branch_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "trackingBranchInput"))

    @builtins.property
    @jsii.member(jsii_name="accessToken")
    def access_token(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "accessToken"))

    @access_token.setter
    def access_token(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__49fb8249130ef897a2808f305d11ab15de849437a3ed417a2833b070b0893ab1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accessToken", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="branches")
    def branches(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "branches"))

    @branches.setter
    def branches(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__86633f1bce6c7ed0830f12e59360aeafa3701ad523347d71d8db87b5261fc3d2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "branches", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="displayName")
    def display_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "displayName"))

    @display_name.setter
    def display_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__afdd7919e9fb6cc6391717d498e23965a3dde9e29031a54e177fa4d9252d0af6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "displayName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="repositoryUri")
    def repository_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "repositoryUri"))

    @repository_uri.setter
    def repository_uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d8a3084ffaf6c704f98dc32ba10957af771bae5cdc3aa6a6d528091fed3ccd1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "repositoryUri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="trackingBranch")
    def tracking_branch(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "trackingBranch"))

    @tracking_branch.setter
    def tracking_branch(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2303bdf02c630ab1e2c6b4e97c1e406a8c88003e75268a3a7213784b8683969f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "trackingBranch", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DialogflowCxAgentGitIntegrationSettingsGithubSettings]:
        return typing.cast(typing.Optional[DialogflowCxAgentGitIntegrationSettingsGithubSettings], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DialogflowCxAgentGitIntegrationSettingsGithubSettings],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b8414b768b84eaba2992ef6f73705af2d389dd0ce9dc15e9633a46ad6660a210)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DialogflowCxAgentGitIntegrationSettingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dialogflowCxAgent.DialogflowCxAgentGitIntegrationSettingsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bc0abab0c019d2806785246efce515fbb3181de277b72ce89f4aa6b8ea7acee9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putGithubSettings")
    def put_github_settings(
        self,
        *,
        access_token: typing.Optional[builtins.str] = None,
        branches: typing.Optional[typing.Sequence[builtins.str]] = None,
        display_name: typing.Optional[builtins.str] = None,
        repository_uri: typing.Optional[builtins.str] = None,
        tracking_branch: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param access_token: The access token used to authenticate the access to the GitHub repository. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_agent#access_token DialogflowCxAgent#access_token}
        :param branches: A list of branches configured to be used from Dialogflow. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_agent#branches DialogflowCxAgent#branches}
        :param display_name: The unique repository display name for the GitHub repository. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_agent#display_name DialogflowCxAgent#display_name}
        :param repository_uri: The GitHub repository URI related to the agent. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_agent#repository_uri DialogflowCxAgent#repository_uri}
        :param tracking_branch: The branch of the GitHub repository tracked for this agent. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_agent#tracking_branch DialogflowCxAgent#tracking_branch}
        '''
        value = DialogflowCxAgentGitIntegrationSettingsGithubSettings(
            access_token=access_token,
            branches=branches,
            display_name=display_name,
            repository_uri=repository_uri,
            tracking_branch=tracking_branch,
        )

        return typing.cast(None, jsii.invoke(self, "putGithubSettings", [value]))

    @jsii.member(jsii_name="resetGithubSettings")
    def reset_github_settings(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGithubSettings", []))

    @builtins.property
    @jsii.member(jsii_name="githubSettings")
    def github_settings(
        self,
    ) -> DialogflowCxAgentGitIntegrationSettingsGithubSettingsOutputReference:
        return typing.cast(DialogflowCxAgentGitIntegrationSettingsGithubSettingsOutputReference, jsii.get(self, "githubSettings"))

    @builtins.property
    @jsii.member(jsii_name="githubSettingsInput")
    def github_settings_input(
        self,
    ) -> typing.Optional[DialogflowCxAgentGitIntegrationSettingsGithubSettings]:
        return typing.cast(typing.Optional[DialogflowCxAgentGitIntegrationSettingsGithubSettings], jsii.get(self, "githubSettingsInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DialogflowCxAgentGitIntegrationSettings]:
        return typing.cast(typing.Optional[DialogflowCxAgentGitIntegrationSettings], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DialogflowCxAgentGitIntegrationSettings],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7cfff895eeefeabc684feb5ee3a6921d24a46a0d1c3b9648e0722947f4d854da)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dialogflowCxAgent.DialogflowCxAgentSpeechToTextSettings",
    jsii_struct_bases=[],
    name_mapping={"enable_speech_adaptation": "enableSpeechAdaptation"},
)
class DialogflowCxAgentSpeechToTextSettings:
    def __init__(
        self,
        *,
        enable_speech_adaptation: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param enable_speech_adaptation: Whether to use speech adaptation for speech recognition. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_agent#enable_speech_adaptation DialogflowCxAgent#enable_speech_adaptation}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__926b122006c1e9e79ed70f35af2ca75f677a1b35d30fb4abc783d008593f0235)
            check_type(argname="argument enable_speech_adaptation", value=enable_speech_adaptation, expected_type=type_hints["enable_speech_adaptation"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if enable_speech_adaptation is not None:
            self._values["enable_speech_adaptation"] = enable_speech_adaptation

    @builtins.property
    def enable_speech_adaptation(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether to use speech adaptation for speech recognition.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_agent#enable_speech_adaptation DialogflowCxAgent#enable_speech_adaptation}
        '''
        result = self._values.get("enable_speech_adaptation")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DialogflowCxAgentSpeechToTextSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DialogflowCxAgentSpeechToTextSettingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dialogflowCxAgent.DialogflowCxAgentSpeechToTextSettingsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fb2ecd0f6bbafc8dc303cdd31134cfec04fabc59ecaa036749a0d95d691e902a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetEnableSpeechAdaptation")
    def reset_enable_speech_adaptation(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnableSpeechAdaptation", []))

    @builtins.property
    @jsii.member(jsii_name="enableSpeechAdaptationInput")
    def enable_speech_adaptation_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enableSpeechAdaptationInput"))

    @builtins.property
    @jsii.member(jsii_name="enableSpeechAdaptation")
    def enable_speech_adaptation(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enableSpeechAdaptation"))

    @enable_speech_adaptation.setter
    def enable_speech_adaptation(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__816e3fee077b167014c315711d9aff35c88055a32c3086a5d283e895271388d7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableSpeechAdaptation", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[DialogflowCxAgentSpeechToTextSettings]:
        return typing.cast(typing.Optional[DialogflowCxAgentSpeechToTextSettings], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DialogflowCxAgentSpeechToTextSettings],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b19c56ebbd32d78350855cfefdcdbdc1251faf121f20d99f72c2c69480b359a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dialogflowCxAgent.DialogflowCxAgentTextToSpeechSettings",
    jsii_struct_bases=[],
    name_mapping={"synthesize_speech_configs": "synthesizeSpeechConfigs"},
)
class DialogflowCxAgentTextToSpeechSettings:
    def __init__(
        self,
        *,
        synthesize_speech_configs: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param synthesize_speech_configs: Configuration of how speech should be synthesized, mapping from `language <https://cloud.google.com/dialogflow/cx/docs/reference/language>`_ to `SynthesizeSpeechConfig <https://cloud.google.com/dialogflow/cx/docs/reference/rest/v3/projects.locations.agents#synthesizespeechconfig>`_. These settings affect: * The phone gateway synthesize configuration set via Agent.text_to_speech_settings. * How speech is synthesized when invoking session APIs. 'Agent.text_to_speech_settings' only applies if 'OutputAudioConfig.synthesize_speech_config' is not specified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_agent#synthesize_speech_configs DialogflowCxAgent#synthesize_speech_configs}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ac766594717231baafeae826f3c33978e75321e771143f867f022bc0aac2e96)
            check_type(argname="argument synthesize_speech_configs", value=synthesize_speech_configs, expected_type=type_hints["synthesize_speech_configs"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if synthesize_speech_configs is not None:
            self._values["synthesize_speech_configs"] = synthesize_speech_configs

    @builtins.property
    def synthesize_speech_configs(self) -> typing.Optional[builtins.str]:
        '''Configuration of how speech should be synthesized, mapping from `language <https://cloud.google.com/dialogflow/cx/docs/reference/language>`_ to `SynthesizeSpeechConfig <https://cloud.google.com/dialogflow/cx/docs/reference/rest/v3/projects.locations.agents#synthesizespeechconfig>`_. These settings affect: * The phone gateway synthesize configuration set via Agent.text_to_speech_settings. * How speech is synthesized when invoking session APIs. 'Agent.text_to_speech_settings' only applies if 'OutputAudioConfig.synthesize_speech_config' is not specified.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_agent#synthesize_speech_configs DialogflowCxAgent#synthesize_speech_configs}
        '''
        result = self._values.get("synthesize_speech_configs")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DialogflowCxAgentTextToSpeechSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DialogflowCxAgentTextToSpeechSettingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dialogflowCxAgent.DialogflowCxAgentTextToSpeechSettingsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__267ee8c8b799793840f205cebaefbff1f725bc37430dda29b9f732eeb1c3bd19)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetSynthesizeSpeechConfigs")
    def reset_synthesize_speech_configs(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSynthesizeSpeechConfigs", []))

    @builtins.property
    @jsii.member(jsii_name="synthesizeSpeechConfigsInput")
    def synthesize_speech_configs_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "synthesizeSpeechConfigsInput"))

    @builtins.property
    @jsii.member(jsii_name="synthesizeSpeechConfigs")
    def synthesize_speech_configs(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "synthesizeSpeechConfigs"))

    @synthesize_speech_configs.setter
    def synthesize_speech_configs(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__03bf313064150d65871d66e4a4d6275406a0bd0efeed8a3c0035fa775e4f1362)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "synthesizeSpeechConfigs", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[DialogflowCxAgentTextToSpeechSettings]:
        return typing.cast(typing.Optional[DialogflowCxAgentTextToSpeechSettings], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DialogflowCxAgentTextToSpeechSettings],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__93fce85f176fe85dcb9f3c2246bc5865a7308d9e5e106130fe5175f392678ee5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dialogflowCxAgent.DialogflowCxAgentTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class DialogflowCxAgentTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_agent#create DialogflowCxAgent#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_agent#delete DialogflowCxAgent#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_agent#update DialogflowCxAgent#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__834b92cd0c3b54b3a5968d7f7e2f1ac5dbe76dd39697e902d2da8a83550223ce)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_agent#create DialogflowCxAgent#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_agent#delete DialogflowCxAgent#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_agent#update DialogflowCxAgent#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DialogflowCxAgentTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DialogflowCxAgentTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dialogflowCxAgent.DialogflowCxAgentTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2dbd1125069a82588014a0569e709f5ee3fe4249fd3d64197c306052f14b2c7a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__eb40cfb7e89d43f5409927bfe09b5942fa74f192bf8388d8f962ef92f85f1d21)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ce7d6e4255f0c54e113ce3664351548279d771836fffee79c1f849e5b803c6b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__56fea1942b835f8ccb7fd81cb2425d18583bb4c543407a018555292414c58194)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DialogflowCxAgentTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DialogflowCxAgentTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DialogflowCxAgentTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3b363813d9730e14a97601d4d9dec551302278221e30803ee54b291d9d6c86e1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "DialogflowCxAgent",
    "DialogflowCxAgentAdvancedSettings",
    "DialogflowCxAgentAdvancedSettingsAudioExportGcsDestination",
    "DialogflowCxAgentAdvancedSettingsAudioExportGcsDestinationOutputReference",
    "DialogflowCxAgentAdvancedSettingsDtmfSettings",
    "DialogflowCxAgentAdvancedSettingsDtmfSettingsOutputReference",
    "DialogflowCxAgentAdvancedSettingsLoggingSettings",
    "DialogflowCxAgentAdvancedSettingsLoggingSettingsOutputReference",
    "DialogflowCxAgentAdvancedSettingsOutputReference",
    "DialogflowCxAgentAdvancedSettingsSpeechSettings",
    "DialogflowCxAgentAdvancedSettingsSpeechSettingsOutputReference",
    "DialogflowCxAgentConfig",
    "DialogflowCxAgentGenAppBuilderSettings",
    "DialogflowCxAgentGenAppBuilderSettingsOutputReference",
    "DialogflowCxAgentGitIntegrationSettings",
    "DialogflowCxAgentGitIntegrationSettingsGithubSettings",
    "DialogflowCxAgentGitIntegrationSettingsGithubSettingsOutputReference",
    "DialogflowCxAgentGitIntegrationSettingsOutputReference",
    "DialogflowCxAgentSpeechToTextSettings",
    "DialogflowCxAgentSpeechToTextSettingsOutputReference",
    "DialogflowCxAgentTextToSpeechSettings",
    "DialogflowCxAgentTextToSpeechSettingsOutputReference",
    "DialogflowCxAgentTimeouts",
    "DialogflowCxAgentTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__61bc8ebf23753dd057cb6e8d4f9cd853d22b0db49b9c2922bb276b018421e905(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    default_language_code: builtins.str,
    display_name: builtins.str,
    location: builtins.str,
    time_zone: builtins.str,
    advanced_settings: typing.Optional[typing.Union[DialogflowCxAgentAdvancedSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    avatar_uri: typing.Optional[builtins.str] = None,
    delete_chat_engine_on_destroy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    description: typing.Optional[builtins.str] = None,
    enable_spell_correction: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enable_stackdriver_logging: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    gen_app_builder_settings: typing.Optional[typing.Union[DialogflowCxAgentGenAppBuilderSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    git_integration_settings: typing.Optional[typing.Union[DialogflowCxAgentGitIntegrationSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    security_settings: typing.Optional[builtins.str] = None,
    speech_to_text_settings: typing.Optional[typing.Union[DialogflowCxAgentSpeechToTextSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    supported_language_codes: typing.Optional[typing.Sequence[builtins.str]] = None,
    text_to_speech_settings: typing.Optional[typing.Union[DialogflowCxAgentTextToSpeechSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[DialogflowCxAgentTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__59d8e46fd3a432635720c1f804dc3fadb282ea1f32a85de798e8ef30042eccf0(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f8342ecdcceb1cabba42fe56e31dbc4a14507bfaef9856c10796f591d512b1d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9bc0b4ccf9181d2f9f6f678eeef3eeb36a64dc0fcc331c10be266fd624efb683(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3005024be4224cf213f91866c88d53a8a85d887af243aa71d2e83dc8dce76fb8(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a40be0b053fa106e7cd28a68719bed0f75eb5e745376e20a1cce3dbf10d3d3ea(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76cde625c357c697363055d9778903f7556f2ff4429366505dec0397319438e0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__852f9a4bbdb359fce82d94e4ec9e1c19a2a3ce9055173ebf9741fb32ad338082(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9076bdd2a578519759a083b967238a1fe8a7f22236ea2c5546cb7be1b4f5ab77(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af559d9afdf65e776615de7bfe4984ce199773f4928c7767ebaa0b61d6755470(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6144bab910f257b0b948dc47375128bd670cae3fe3c17b8ecd25584c51b849e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1cc79a9c1491ecf859c84adc5762c52f705c16b40203907edf7ffb4320f9bb3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65c7b967aea01cb6fb2707be603fb0bbf07ed6b9f53a43f099002cd5e7c81ff8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa74fce4e5b331de1ab843d0f0fae51e53e2a011f0120f4c26638e8b9736b9ca(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a60a74ebc2d61e20780b51fd6e21558a214487625a399fb079862df69f84431(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4ef011254bdedd274a441a86dadaddeda8b5a4ab84050e8a77259cd9f78c6da(
    *,
    audio_export_gcs_destination: typing.Optional[typing.Union[DialogflowCxAgentAdvancedSettingsAudioExportGcsDestination, typing.Dict[builtins.str, typing.Any]]] = None,
    dtmf_settings: typing.Optional[typing.Union[DialogflowCxAgentAdvancedSettingsDtmfSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    logging_settings: typing.Optional[typing.Union[DialogflowCxAgentAdvancedSettingsLoggingSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    speech_settings: typing.Optional[typing.Union[DialogflowCxAgentAdvancedSettingsSpeechSettings, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a13b1796fd04c2551b0272643e49874e1def2d40d0e3e3c9ffc1f5c0da58a578(
    *,
    uri: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b6724d7b658e6314e47041d7bd3b85812c01ccd229a82d6de4c677d784c230d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__327afc88dde179d5c29ec64396fdac7f110670ae71058285caf832aab00e4769(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77331375ea49ea9fad6e0cf4912145311a01881c0de1bf42fbe4d981df1f63a3(
    value: typing.Optional[DialogflowCxAgentAdvancedSettingsAudioExportGcsDestination],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__309bfd4ca87ed9f97ca14df367b79510ddd859af4b1c1c9b5f5b6400468f84a4(
    *,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    finish_digit: typing.Optional[builtins.str] = None,
    max_digits: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db5d2f1647d0849572f5c0c8191eb167d8cfd008e8cdf259a8ae6f768d48e07f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e137fff10c85299bd1dcb3b9feebe1f6aed8f3dba9b9325689f83e8209897cb(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__90e990c37bdad50c2f2b01fb2b6d6b3424db487892f11844a7689f64dd751e83(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__007472309a021a1d72a228d4e30e5c5acfa6715b46b3f64c5da3e196ab512ad3(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2fc2f5da8dc098b31d66c0d388eb1f851d1749df38320e4df6f4cec37252d100(
    value: typing.Optional[DialogflowCxAgentAdvancedSettingsDtmfSettings],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b9e2b38e5255381aa68b8971e2b5820c094afad00f5b4d255cc2c73f6957fb5(
    *,
    enable_consent_based_redaction: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enable_interaction_logging: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enable_stackdriver_logging: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80d7ef0e77591b64bd5f860af136b35096676263837e83f149851abe6afe89eb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5cce831812eedcd9bec976503a52248ccfffea3ba06f733adbfcc38861075a8c(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb895a5bcb5457e2b064c625a9d79cfa0a18022187da8e75bbe0f446d62ebc92(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62b66a4a4eba029e06afa7f031417d527d146fce9637e6e8064495f104b29c5a(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6242327b451c39df52b8f8588c62cb3f6fadc560b8f1f42067c46dd8cecaeca3(
    value: typing.Optional[DialogflowCxAgentAdvancedSettingsLoggingSettings],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__baa11be897f83b4c88612729658d69a9abbf4b014d7b4c779e7872710de01453(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1a0c12e169f59fa751cddfceab869b005bd6fe8278cec8bd08a2e6ce5cb9cbb(
    value: typing.Optional[DialogflowCxAgentAdvancedSettings],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__01f57f97f6af01b3217d3c01d6623e5550df4c8221b6548bb9fb7680af6d032e(
    *,
    endpointer_sensitivity: typing.Optional[jsii.Number] = None,
    models: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    no_speech_timeout: typing.Optional[builtins.str] = None,
    use_timeout_based_endpointing: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2b1c1ab6c1a086820eae5a63505a67e5ccd9314449632cbe727b0dbef5dc228(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45e570f0fba1ae5d5c628a90e62541d159d917f6aef134d5addda1e25b7c6ce7(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e8f2c5bf00796a68328d0ce83e592669834115b259b6b333549990381b96193(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0571a67b67d2a997eec8e4bc123ca36afe4cf65d1bafcb7282f6d22c165b54b7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb2a098d41c1e4f441cecc8a39066fc7910edbc189bc82552ce0e5b4e068856c(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a2379f9a03e0abb947bb0b09f3d52c2970bf436a73ae5849971e99f4209e077(
    value: typing.Optional[DialogflowCxAgentAdvancedSettingsSpeechSettings],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1cdc3ec5885cae236dbed1fab750af37905b761eb071a01995f6899822650c1(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    default_language_code: builtins.str,
    display_name: builtins.str,
    location: builtins.str,
    time_zone: builtins.str,
    advanced_settings: typing.Optional[typing.Union[DialogflowCxAgentAdvancedSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    avatar_uri: typing.Optional[builtins.str] = None,
    delete_chat_engine_on_destroy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    description: typing.Optional[builtins.str] = None,
    enable_spell_correction: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enable_stackdriver_logging: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    gen_app_builder_settings: typing.Optional[typing.Union[DialogflowCxAgentGenAppBuilderSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    git_integration_settings: typing.Optional[typing.Union[DialogflowCxAgentGitIntegrationSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    security_settings: typing.Optional[builtins.str] = None,
    speech_to_text_settings: typing.Optional[typing.Union[DialogflowCxAgentSpeechToTextSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    supported_language_codes: typing.Optional[typing.Sequence[builtins.str]] = None,
    text_to_speech_settings: typing.Optional[typing.Union[DialogflowCxAgentTextToSpeechSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[DialogflowCxAgentTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__471887f4da87e30edaf305b8914ee440c3b479aee813785e5c9a3a913270e98f(
    *,
    engine: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__537849b133f80b84a42b8e9e85b8b02fc1c8bbae8bdbd5a0920bc5fd5d167231(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f5ee16c4177b307814bf37f218c398101d4307d268506b0d8427a14c1c0a058(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b760b217a582df2b7bd79909b42bfaff0762a49b297e5ca731de1bc7ccdb7149(
    value: typing.Optional[DialogflowCxAgentGenAppBuilderSettings],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b170084649e428d18414a88f125d21c64d81b4b6ae1a7c140e04697450a9b7aa(
    *,
    github_settings: typing.Optional[typing.Union[DialogflowCxAgentGitIntegrationSettingsGithubSettings, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cdbf7722d2eb10c1c97a4674f34774f267f5b7d44d9c8fc25fb58ffc99ad6576(
    *,
    access_token: typing.Optional[builtins.str] = None,
    branches: typing.Optional[typing.Sequence[builtins.str]] = None,
    display_name: typing.Optional[builtins.str] = None,
    repository_uri: typing.Optional[builtins.str] = None,
    tracking_branch: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e2701bd94e040cf1d1cfbd301e92a302555d49fba925c7dd0d44723f5384171(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__49fb8249130ef897a2808f305d11ab15de849437a3ed417a2833b070b0893ab1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86633f1bce6c7ed0830f12e59360aeafa3701ad523347d71d8db87b5261fc3d2(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__afdd7919e9fb6cc6391717d498e23965a3dde9e29031a54e177fa4d9252d0af6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d8a3084ffaf6c704f98dc32ba10957af771bae5cdc3aa6a6d528091fed3ccd1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2303bdf02c630ab1e2c6b4e97c1e406a8c88003e75268a3a7213784b8683969f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8414b768b84eaba2992ef6f73705af2d389dd0ce9dc15e9633a46ad6660a210(
    value: typing.Optional[DialogflowCxAgentGitIntegrationSettingsGithubSettings],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc0abab0c019d2806785246efce515fbb3181de277b72ce89f4aa6b8ea7acee9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7cfff895eeefeabc684feb5ee3a6921d24a46a0d1c3b9648e0722947f4d854da(
    value: typing.Optional[DialogflowCxAgentGitIntegrationSettings],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__926b122006c1e9e79ed70f35af2ca75f677a1b35d30fb4abc783d008593f0235(
    *,
    enable_speech_adaptation: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb2ecd0f6bbafc8dc303cdd31134cfec04fabc59ecaa036749a0d95d691e902a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__816e3fee077b167014c315711d9aff35c88055a32c3086a5d283e895271388d7(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b19c56ebbd32d78350855cfefdcdbdc1251faf121f20d99f72c2c69480b359a(
    value: typing.Optional[DialogflowCxAgentSpeechToTextSettings],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ac766594717231baafeae826f3c33978e75321e771143f867f022bc0aac2e96(
    *,
    synthesize_speech_configs: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__267ee8c8b799793840f205cebaefbff1f725bc37430dda29b9f732eeb1c3bd19(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03bf313064150d65871d66e4a4d6275406a0bd0efeed8a3c0035fa775e4f1362(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93fce85f176fe85dcb9f3c2246bc5865a7308d9e5e106130fe5175f392678ee5(
    value: typing.Optional[DialogflowCxAgentTextToSpeechSettings],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__834b92cd0c3b54b3a5968d7f7e2f1ac5dbe76dd39697e902d2da8a83550223ce(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2dbd1125069a82588014a0569e709f5ee3fe4249fd3d64197c306052f14b2c7a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb40cfb7e89d43f5409927bfe09b5942fa74f192bf8388d8f962ef92f85f1d21(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ce7d6e4255f0c54e113ce3664351548279d771836fffee79c1f849e5b803c6b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__56fea1942b835f8ccb7fd81cb2425d18583bb4c543407a018555292414c58194(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b363813d9730e14a97601d4d9dec551302278221e30803ee54b291d9d6c86e1(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DialogflowCxAgentTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
