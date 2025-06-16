r'''
# `google_dialogflow_cx_agent`

Refer to the Terraform Registry for docs: [`google_dialogflow_cx_agent`](https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_agent).
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


class GoogleDialogflowCxAgent(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDialogflowCxAgent.GoogleDialogflowCxAgent",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_agent google_dialogflow_cx_agent}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        default_language_code: builtins.str,
        display_name: builtins.str,
        location: builtins.str,
        time_zone: builtins.str,
        advanced_settings: typing.Optional[typing.Union["GoogleDialogflowCxAgentAdvancedSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        avatar_uri: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        enable_spell_correction: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_stackdriver_logging: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        gen_app_builder_settings: typing.Optional[typing.Union["GoogleDialogflowCxAgentGenAppBuilderSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        git_integration_settings: typing.Optional[typing.Union["GoogleDialogflowCxAgentGitIntegrationSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        security_settings: typing.Optional[builtins.str] = None,
        speech_to_text_settings: typing.Optional[typing.Union["GoogleDialogflowCxAgentSpeechToTextSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        supported_language_codes: typing.Optional[typing.Sequence[builtins.str]] = None,
        text_to_speech_settings: typing.Optional[typing.Union["GoogleDialogflowCxAgentTextToSpeechSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["GoogleDialogflowCxAgentTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_agent google_dialogflow_cx_agent} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param default_language_code: The default language of the agent as a language tag. `See Language Support <https://cloud.google.com/dialogflow/cx/docs/reference/language>`_ for a list of the currently supported language codes. This field cannot be updated after creation. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_agent#default_language_code GoogleDialogflowCxAgent#default_language_code}
        :param display_name: The human-readable name of the agent, unique within the location. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_agent#display_name GoogleDialogflowCxAgent#display_name}
        :param location: The name of the location this agent is located in. ~> **Note:** The first time you are deploying an Agent in your project you must configure location settings. This is a one time step but at the moment you can only `configure location settings <https://cloud.google.com/dialogflow/cx/docs/concept/region#location-settings>`_ via the Dialogflow CX console. Another options is to use global location so you don't need to manually configure location settings. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_agent#location GoogleDialogflowCxAgent#location}
        :param time_zone: The time zone of this agent from the `time zone database <https://www.iana.org/time-zones>`_, e.g., America/New_York, Europe/Paris. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_agent#time_zone GoogleDialogflowCxAgent#time_zone}
        :param advanced_settings: advanced_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_agent#advanced_settings GoogleDialogflowCxAgent#advanced_settings}
        :param avatar_uri: The URI of the agent's avatar. Avatars are used throughout the Dialogflow console and in the self-hosted Web Demo integration. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_agent#avatar_uri GoogleDialogflowCxAgent#avatar_uri}
        :param description: The description of this agent. The maximum length is 500 characters. If exceeded, the request is rejected. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_agent#description GoogleDialogflowCxAgent#description}
        :param enable_spell_correction: Indicates if automatic spell correction is enabled in detect intent requests. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_agent#enable_spell_correction GoogleDialogflowCxAgent#enable_spell_correction}
        :param enable_stackdriver_logging: Determines whether this agent should log conversation queries. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_agent#enable_stackdriver_logging GoogleDialogflowCxAgent#enable_stackdriver_logging}
        :param gen_app_builder_settings: gen_app_builder_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_agent#gen_app_builder_settings GoogleDialogflowCxAgent#gen_app_builder_settings}
        :param git_integration_settings: git_integration_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_agent#git_integration_settings GoogleDialogflowCxAgent#git_integration_settings}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_agent#id GoogleDialogflowCxAgent#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_agent#project GoogleDialogflowCxAgent#project}.
        :param security_settings: Name of the SecuritySettings reference for the agent. Format: projects//locations//securitySettings/. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_agent#security_settings GoogleDialogflowCxAgent#security_settings}
        :param speech_to_text_settings: speech_to_text_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_agent#speech_to_text_settings GoogleDialogflowCxAgent#speech_to_text_settings}
        :param supported_language_codes: The list of all languages supported by this agent (except for the default_language_code). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_agent#supported_language_codes GoogleDialogflowCxAgent#supported_language_codes}
        :param text_to_speech_settings: text_to_speech_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_agent#text_to_speech_settings GoogleDialogflowCxAgent#text_to_speech_settings}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_agent#timeouts GoogleDialogflowCxAgent#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ca1f328a2790e853c9443590e831be92cb702fcba64a3f201ffd86cf20e0b5d)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = GoogleDialogflowCxAgentConfig(
            default_language_code=default_language_code,
            display_name=display_name,
            location=location,
            time_zone=time_zone,
            advanced_settings=advanced_settings,
            avatar_uri=avatar_uri,
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
        '''Generates CDKTF code for importing a GoogleDialogflowCxAgent resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the GoogleDialogflowCxAgent to import.
        :param import_from_id: The id of the existing GoogleDialogflowCxAgent that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_agent#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the GoogleDialogflowCxAgent to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1ddedd6bbdfd57c65d351ceb583ac0612e79a3ba8a1d85b8e1058bfbf549ce5b)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putAdvancedSettings")
    def put_advanced_settings(
        self,
        *,
        audio_export_gcs_destination: typing.Optional[typing.Union["GoogleDialogflowCxAgentAdvancedSettingsAudioExportGcsDestination", typing.Dict[builtins.str, typing.Any]]] = None,
        dtmf_settings: typing.Optional[typing.Union["GoogleDialogflowCxAgentAdvancedSettingsDtmfSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        logging_settings: typing.Optional[typing.Union["GoogleDialogflowCxAgentAdvancedSettingsLoggingSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        speech_settings: typing.Optional[typing.Union["GoogleDialogflowCxAgentAdvancedSettingsSpeechSettings", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param audio_export_gcs_destination: audio_export_gcs_destination block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_agent#audio_export_gcs_destination GoogleDialogflowCxAgent#audio_export_gcs_destination}
        :param dtmf_settings: dtmf_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_agent#dtmf_settings GoogleDialogflowCxAgent#dtmf_settings}
        :param logging_settings: logging_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_agent#logging_settings GoogleDialogflowCxAgent#logging_settings}
        :param speech_settings: speech_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_agent#speech_settings GoogleDialogflowCxAgent#speech_settings}
        '''
        value = GoogleDialogflowCxAgentAdvancedSettings(
            audio_export_gcs_destination=audio_export_gcs_destination,
            dtmf_settings=dtmf_settings,
            logging_settings=logging_settings,
            speech_settings=speech_settings,
        )

        return typing.cast(None, jsii.invoke(self, "putAdvancedSettings", [value]))

    @jsii.member(jsii_name="putGenAppBuilderSettings")
    def put_gen_app_builder_settings(self, *, engine: builtins.str) -> None:
        '''
        :param engine: The full name of the Gen App Builder engine related to this agent if there is one. Format: projects/{Project ID}/locations/{Location ID}/collections/{Collection ID}/engines/{Engine ID} Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_agent#engine GoogleDialogflowCxAgent#engine}
        '''
        value = GoogleDialogflowCxAgentGenAppBuilderSettings(engine=engine)

        return typing.cast(None, jsii.invoke(self, "putGenAppBuilderSettings", [value]))

    @jsii.member(jsii_name="putGitIntegrationSettings")
    def put_git_integration_settings(
        self,
        *,
        github_settings: typing.Optional[typing.Union["GoogleDialogflowCxAgentGitIntegrationSettingsGithubSettings", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param github_settings: github_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_agent#github_settings GoogleDialogflowCxAgent#github_settings}
        '''
        value = GoogleDialogflowCxAgentGitIntegrationSettings(
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
        :param enable_speech_adaptation: Whether to use speech adaptation for speech recognition. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_agent#enable_speech_adaptation GoogleDialogflowCxAgent#enable_speech_adaptation}
        '''
        value = GoogleDialogflowCxAgentSpeechToTextSettings(
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
        :param synthesize_speech_configs: Configuration of how speech should be synthesized, mapping from `language <https://cloud.google.com/dialogflow/cx/docs/reference/language>`_ to `SynthesizeSpeechConfig <https://cloud.google.com/dialogflow/cx/docs/reference/rest/v3/projects.locations.agents#synthesizespeechconfig>`_. These settings affect: * The phone gateway synthesize configuration set via Agent.text_to_speech_settings. * How speech is synthesized when invoking session APIs. 'Agent.text_to_speech_settings' only applies if 'OutputAudioConfig.synthesize_speech_config' is not specified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_agent#synthesize_speech_configs GoogleDialogflowCxAgent#synthesize_speech_configs}
        '''
        value = GoogleDialogflowCxAgentTextToSpeechSettings(
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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_agent#create GoogleDialogflowCxAgent#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_agent#delete GoogleDialogflowCxAgent#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_agent#update GoogleDialogflowCxAgent#update}.
        '''
        value = GoogleDialogflowCxAgentTimeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetAdvancedSettings")
    def reset_advanced_settings(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAdvancedSettings", []))

    @jsii.member(jsii_name="resetAvatarUri")
    def reset_avatar_uri(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAvatarUri", []))

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
    def advanced_settings(
        self,
    ) -> "GoogleDialogflowCxAgentAdvancedSettingsOutputReference":
        return typing.cast("GoogleDialogflowCxAgentAdvancedSettingsOutputReference", jsii.get(self, "advancedSettings"))

    @builtins.property
    @jsii.member(jsii_name="genAppBuilderSettings")
    def gen_app_builder_settings(
        self,
    ) -> "GoogleDialogflowCxAgentGenAppBuilderSettingsOutputReference":
        return typing.cast("GoogleDialogflowCxAgentGenAppBuilderSettingsOutputReference", jsii.get(self, "genAppBuilderSettings"))

    @builtins.property
    @jsii.member(jsii_name="gitIntegrationSettings")
    def git_integration_settings(
        self,
    ) -> "GoogleDialogflowCxAgentGitIntegrationSettingsOutputReference":
        return typing.cast("GoogleDialogflowCxAgentGitIntegrationSettingsOutputReference", jsii.get(self, "gitIntegrationSettings"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="speechToTextSettings")
    def speech_to_text_settings(
        self,
    ) -> "GoogleDialogflowCxAgentSpeechToTextSettingsOutputReference":
        return typing.cast("GoogleDialogflowCxAgentSpeechToTextSettingsOutputReference", jsii.get(self, "speechToTextSettings"))

    @builtins.property
    @jsii.member(jsii_name="startFlow")
    def start_flow(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "startFlow"))

    @builtins.property
    @jsii.member(jsii_name="textToSpeechSettings")
    def text_to_speech_settings(
        self,
    ) -> "GoogleDialogflowCxAgentTextToSpeechSettingsOutputReference":
        return typing.cast("GoogleDialogflowCxAgentTextToSpeechSettingsOutputReference", jsii.get(self, "textToSpeechSettings"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "GoogleDialogflowCxAgentTimeoutsOutputReference":
        return typing.cast("GoogleDialogflowCxAgentTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="advancedSettingsInput")
    def advanced_settings_input(
        self,
    ) -> typing.Optional["GoogleDialogflowCxAgentAdvancedSettings"]:
        return typing.cast(typing.Optional["GoogleDialogflowCxAgentAdvancedSettings"], jsii.get(self, "advancedSettingsInput"))

    @builtins.property
    @jsii.member(jsii_name="avatarUriInput")
    def avatar_uri_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "avatarUriInput"))

    @builtins.property
    @jsii.member(jsii_name="defaultLanguageCodeInput")
    def default_language_code_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "defaultLanguageCodeInput"))

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
    ) -> typing.Optional["GoogleDialogflowCxAgentGenAppBuilderSettings"]:
        return typing.cast(typing.Optional["GoogleDialogflowCxAgentGenAppBuilderSettings"], jsii.get(self, "genAppBuilderSettingsInput"))

    @builtins.property
    @jsii.member(jsii_name="gitIntegrationSettingsInput")
    def git_integration_settings_input(
        self,
    ) -> typing.Optional["GoogleDialogflowCxAgentGitIntegrationSettings"]:
        return typing.cast(typing.Optional["GoogleDialogflowCxAgentGitIntegrationSettings"], jsii.get(self, "gitIntegrationSettingsInput"))

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
    ) -> typing.Optional["GoogleDialogflowCxAgentSpeechToTextSettings"]:
        return typing.cast(typing.Optional["GoogleDialogflowCxAgentSpeechToTextSettings"], jsii.get(self, "speechToTextSettingsInput"))

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
    ) -> typing.Optional["GoogleDialogflowCxAgentTextToSpeechSettings"]:
        return typing.cast(typing.Optional["GoogleDialogflowCxAgentTextToSpeechSettings"], jsii.get(self, "textToSpeechSettingsInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleDialogflowCxAgentTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleDialogflowCxAgentTimeouts"]], jsii.get(self, "timeoutsInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__8e875f2b69646bbd2e26827da76e07f873b2aa5aa4cedd1cee494a8608ad21c6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "avatarUri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="defaultLanguageCode")
    def default_language_code(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "defaultLanguageCode"))

    @default_language_code.setter
    def default_language_code(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bc3d0d597790982613780fcbbad91e72961e2309f7a3677377475f74a044188e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultLanguageCode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d5f781deb9d9f3716387e56cda9991aa50000a7223476aaa3f532f101679803)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="displayName")
    def display_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "displayName"))

    @display_name.setter
    def display_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__036812a32d1821e736f8dbbd23ba2b83f1cdfac0599475b20ea8f5851e63be27)
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
            type_hints = typing.get_type_hints(_typecheckingstub__93bfffc5c247efbd81c6505c465ef314f485da80ae689ab1354d4bd989dd2ca3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__066946d07bb61956a0ceac83b3d7d73e8bfbb76ad109eb4bd29d31344fb4d211)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableStackdriverLogging", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0143a9bb7afda9b3f7c18ba505443153171c8fb75405d4e7bd77753abc5f5d1b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f446f2070d165ff6f6aeebda042b3ee1c13c03a64dd82cf49ff579eedb9d2b21)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__34bd07c2c345a8d8a28f8062bbeecb62ae8ad9dd031c0250035caaccc096d489)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="securitySettings")
    def security_settings(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "securitySettings"))

    @security_settings.setter
    def security_settings(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2b89d837837a7874acfaf82eb79f525f77df8075f2bb7888bf9d9c03c7adc82c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "securitySettings", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="supportedLanguageCodes")
    def supported_language_codes(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "supportedLanguageCodes"))

    @supported_language_codes.setter
    def supported_language_codes(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__64b69152ca10303499ff6dceebca860f4861413aeb57172e7da2bc3debe865de)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "supportedLanguageCodes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="timeZone")
    def time_zone(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "timeZone"))

    @time_zone.setter
    def time_zone(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__780a8b69fbb0691c03bc36f83a658d1022a58fe00b047d2472911024908000bb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timeZone", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDialogflowCxAgent.GoogleDialogflowCxAgentAdvancedSettings",
    jsii_struct_bases=[],
    name_mapping={
        "audio_export_gcs_destination": "audioExportGcsDestination",
        "dtmf_settings": "dtmfSettings",
        "logging_settings": "loggingSettings",
        "speech_settings": "speechSettings",
    },
)
class GoogleDialogflowCxAgentAdvancedSettings:
    def __init__(
        self,
        *,
        audio_export_gcs_destination: typing.Optional[typing.Union["GoogleDialogflowCxAgentAdvancedSettingsAudioExportGcsDestination", typing.Dict[builtins.str, typing.Any]]] = None,
        dtmf_settings: typing.Optional[typing.Union["GoogleDialogflowCxAgentAdvancedSettingsDtmfSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        logging_settings: typing.Optional[typing.Union["GoogleDialogflowCxAgentAdvancedSettingsLoggingSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        speech_settings: typing.Optional[typing.Union["GoogleDialogflowCxAgentAdvancedSettingsSpeechSettings", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param audio_export_gcs_destination: audio_export_gcs_destination block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_agent#audio_export_gcs_destination GoogleDialogflowCxAgent#audio_export_gcs_destination}
        :param dtmf_settings: dtmf_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_agent#dtmf_settings GoogleDialogflowCxAgent#dtmf_settings}
        :param logging_settings: logging_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_agent#logging_settings GoogleDialogflowCxAgent#logging_settings}
        :param speech_settings: speech_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_agent#speech_settings GoogleDialogflowCxAgent#speech_settings}
        '''
        if isinstance(audio_export_gcs_destination, dict):
            audio_export_gcs_destination = GoogleDialogflowCxAgentAdvancedSettingsAudioExportGcsDestination(**audio_export_gcs_destination)
        if isinstance(dtmf_settings, dict):
            dtmf_settings = GoogleDialogflowCxAgentAdvancedSettingsDtmfSettings(**dtmf_settings)
        if isinstance(logging_settings, dict):
            logging_settings = GoogleDialogflowCxAgentAdvancedSettingsLoggingSettings(**logging_settings)
        if isinstance(speech_settings, dict):
            speech_settings = GoogleDialogflowCxAgentAdvancedSettingsSpeechSettings(**speech_settings)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6f7ae78c31a0b7f6305c04fe906e38ba4453aa6c5aa4f7fcc4331449fd4b4589)
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
    ) -> typing.Optional["GoogleDialogflowCxAgentAdvancedSettingsAudioExportGcsDestination"]:
        '''audio_export_gcs_destination block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_agent#audio_export_gcs_destination GoogleDialogflowCxAgent#audio_export_gcs_destination}
        '''
        result = self._values.get("audio_export_gcs_destination")
        return typing.cast(typing.Optional["GoogleDialogflowCxAgentAdvancedSettingsAudioExportGcsDestination"], result)

    @builtins.property
    def dtmf_settings(
        self,
    ) -> typing.Optional["GoogleDialogflowCxAgentAdvancedSettingsDtmfSettings"]:
        '''dtmf_settings block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_agent#dtmf_settings GoogleDialogflowCxAgent#dtmf_settings}
        '''
        result = self._values.get("dtmf_settings")
        return typing.cast(typing.Optional["GoogleDialogflowCxAgentAdvancedSettingsDtmfSettings"], result)

    @builtins.property
    def logging_settings(
        self,
    ) -> typing.Optional["GoogleDialogflowCxAgentAdvancedSettingsLoggingSettings"]:
        '''logging_settings block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_agent#logging_settings GoogleDialogflowCxAgent#logging_settings}
        '''
        result = self._values.get("logging_settings")
        return typing.cast(typing.Optional["GoogleDialogflowCxAgentAdvancedSettingsLoggingSettings"], result)

    @builtins.property
    def speech_settings(
        self,
    ) -> typing.Optional["GoogleDialogflowCxAgentAdvancedSettingsSpeechSettings"]:
        '''speech_settings block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_agent#speech_settings GoogleDialogflowCxAgent#speech_settings}
        '''
        result = self._values.get("speech_settings")
        return typing.cast(typing.Optional["GoogleDialogflowCxAgentAdvancedSettingsSpeechSettings"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDialogflowCxAgentAdvancedSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDialogflowCxAgent.GoogleDialogflowCxAgentAdvancedSettingsAudioExportGcsDestination",
    jsii_struct_bases=[],
    name_mapping={"uri": "uri"},
)
class GoogleDialogflowCxAgentAdvancedSettingsAudioExportGcsDestination:
    def __init__(self, *, uri: typing.Optional[builtins.str] = None) -> None:
        '''
        :param uri: The Google Cloud Storage URI for the exported objects. Whether a full object name, or just a prefix, its usage depends on the Dialogflow operation. Format: gs://bucket/object-name-or-prefix Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_agent#uri GoogleDialogflowCxAgent#uri}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7826a4e2aca9208785a39a6c63ce592612a8638eb14fcde6193de840f633d8f4)
            check_type(argname="argument uri", value=uri, expected_type=type_hints["uri"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if uri is not None:
            self._values["uri"] = uri

    @builtins.property
    def uri(self) -> typing.Optional[builtins.str]:
        '''The Google Cloud Storage URI for the exported objects.

        Whether a full object name, or just a prefix, its usage depends on the Dialogflow operation.
        Format: gs://bucket/object-name-or-prefix

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_agent#uri GoogleDialogflowCxAgent#uri}
        '''
        result = self._values.get("uri")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDialogflowCxAgentAdvancedSettingsAudioExportGcsDestination(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDialogflowCxAgentAdvancedSettingsAudioExportGcsDestinationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDialogflowCxAgent.GoogleDialogflowCxAgentAdvancedSettingsAudioExportGcsDestinationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9ddfc65278f04fec083af5d77e372a5a49a8d4f122f614b9c3c4a591f686a09e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f0d4792faea773ffd46526c0ae03bdc340ed6740975ed38c2b520f9177716e3e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "uri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDialogflowCxAgentAdvancedSettingsAudioExportGcsDestination]:
        return typing.cast(typing.Optional[GoogleDialogflowCxAgentAdvancedSettingsAudioExportGcsDestination], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDialogflowCxAgentAdvancedSettingsAudioExportGcsDestination],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__749759f10e85cc42ca38e1f3f02a453c7c008b31d19c23e80f231d59e947a2b9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDialogflowCxAgent.GoogleDialogflowCxAgentAdvancedSettingsDtmfSettings",
    jsii_struct_bases=[],
    name_mapping={
        "enabled": "enabled",
        "finish_digit": "finishDigit",
        "max_digits": "maxDigits",
    },
)
class GoogleDialogflowCxAgentAdvancedSettingsDtmfSettings:
    def __init__(
        self,
        *,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        finish_digit: typing.Optional[builtins.str] = None,
        max_digits: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param enabled: If true, incoming audio is processed for DTMF (dual tone multi frequency) events. For example, if the caller presses a button on their telephone keypad and DTMF processing is enabled, Dialogflow will detect the event (e.g. a "3" was pressed) in the incoming audio and pass the event to the bot to drive business logic (e.g. when 3 is pressed, return the account balance). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_agent#enabled GoogleDialogflowCxAgent#enabled}
        :param finish_digit: The digit that terminates a DTMF digit sequence. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_agent#finish_digit GoogleDialogflowCxAgent#finish_digit}
        :param max_digits: Max length of DTMF digits. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_agent#max_digits GoogleDialogflowCxAgent#max_digits}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a08fd56302072e718fdc252a948f0811b78e345dae49861a85062a0c16859e5)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_agent#enabled GoogleDialogflowCxAgent#enabled}
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def finish_digit(self) -> typing.Optional[builtins.str]:
        '''The digit that terminates a DTMF digit sequence.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_agent#finish_digit GoogleDialogflowCxAgent#finish_digit}
        '''
        result = self._values.get("finish_digit")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def max_digits(self) -> typing.Optional[jsii.Number]:
        '''Max length of DTMF digits.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_agent#max_digits GoogleDialogflowCxAgent#max_digits}
        '''
        result = self._values.get("max_digits")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDialogflowCxAgentAdvancedSettingsDtmfSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDialogflowCxAgentAdvancedSettingsDtmfSettingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDialogflowCxAgent.GoogleDialogflowCxAgentAdvancedSettingsDtmfSettingsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a9f34e00edca4e7417e94b26d4afae2cc6bc7b224811c6119e7c1f5e4543dca7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c1d2dd2efaadffde5ed5fcd493a1fde8dd90a0c3240545e9f5f0195223cea0af)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="finishDigit")
    def finish_digit(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "finishDigit"))

    @finish_digit.setter
    def finish_digit(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a9d460a49500ea13094f34d3d974d1c5583e53c5aeedaa641f7565256a171756)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "finishDigit", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxDigits")
    def max_digits(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxDigits"))

    @max_digits.setter
    def max_digits(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__39926dd6b184ba9696fa92ad0be0c62ced0bd8b4e28c85ffaa9b0c344054c84e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxDigits", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDialogflowCxAgentAdvancedSettingsDtmfSettings]:
        return typing.cast(typing.Optional[GoogleDialogflowCxAgentAdvancedSettingsDtmfSettings], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDialogflowCxAgentAdvancedSettingsDtmfSettings],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f0bf0acaa00b74483e34e0b1214ebfa4d0515ff7e0ce90d498ab80bc1432cc7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDialogflowCxAgent.GoogleDialogflowCxAgentAdvancedSettingsLoggingSettings",
    jsii_struct_bases=[],
    name_mapping={
        "enable_consent_based_redaction": "enableConsentBasedRedaction",
        "enable_interaction_logging": "enableInteractionLogging",
        "enable_stackdriver_logging": "enableStackdriverLogging",
    },
)
class GoogleDialogflowCxAgentAdvancedSettingsLoggingSettings:
    def __init__(
        self,
        *,
        enable_consent_based_redaction: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_interaction_logging: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_stackdriver_logging: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param enable_consent_based_redaction: Enables consent-based end-user input redaction, if true, a pre-defined session parameter **$session.params.conversation-redaction** will be used to determine if the utterance should be redacted. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_agent#enable_consent_based_redaction GoogleDialogflowCxAgent#enable_consent_based_redaction}
        :param enable_interaction_logging: Enables DF Interaction logging. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_agent#enable_interaction_logging GoogleDialogflowCxAgent#enable_interaction_logging}
        :param enable_stackdriver_logging: Enables Google Cloud Logging. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_agent#enable_stackdriver_logging GoogleDialogflowCxAgent#enable_stackdriver_logging}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f045dfeab82eb329977019edf3b6b2df073b6a5aae3766a0f152534109c65f05)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_agent#enable_consent_based_redaction GoogleDialogflowCxAgent#enable_consent_based_redaction}
        '''
        result = self._values.get("enable_consent_based_redaction")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def enable_interaction_logging(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Enables DF Interaction logging.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_agent#enable_interaction_logging GoogleDialogflowCxAgent#enable_interaction_logging}
        '''
        result = self._values.get("enable_interaction_logging")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def enable_stackdriver_logging(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Enables Google Cloud Logging.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_agent#enable_stackdriver_logging GoogleDialogflowCxAgent#enable_stackdriver_logging}
        '''
        result = self._values.get("enable_stackdriver_logging")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDialogflowCxAgentAdvancedSettingsLoggingSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDialogflowCxAgentAdvancedSettingsLoggingSettingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDialogflowCxAgent.GoogleDialogflowCxAgentAdvancedSettingsLoggingSettingsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__909a114a1ec11e8800e27b9e2c97628ab975dd071b0890d27c00cd35f58ba3fa)
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
            type_hints = typing.get_type_hints(_typecheckingstub__05039968d7fd799916eb89f5cdf18e08dd768caece8f022e8cadd5569b1199fb)
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
            type_hints = typing.get_type_hints(_typecheckingstub__08ab899897de524d21e02f2774d8074a12e4d4ff044af3ddf9753bb3a6cef863)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3c41bf213d0439a60cc12c4971278a07d81fc9e2c3de07dfa6ded78194e3188c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableStackdriverLogging", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDialogflowCxAgentAdvancedSettingsLoggingSettings]:
        return typing.cast(typing.Optional[GoogleDialogflowCxAgentAdvancedSettingsLoggingSettings], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDialogflowCxAgentAdvancedSettingsLoggingSettings],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b78bc78ca7dcd8c1698e75c821277d72dfaded1679362ed8dfde1fde6de84ed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleDialogflowCxAgentAdvancedSettingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDialogflowCxAgent.GoogleDialogflowCxAgentAdvancedSettingsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ce3511b0a511669313a4db9aaa653a4da99e2f69f6c8098cc69bf5fefa667bf7)
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
        :param uri: The Google Cloud Storage URI for the exported objects. Whether a full object name, or just a prefix, its usage depends on the Dialogflow operation. Format: gs://bucket/object-name-or-prefix Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_agent#uri GoogleDialogflowCxAgent#uri}
        '''
        value = GoogleDialogflowCxAgentAdvancedSettingsAudioExportGcsDestination(
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
        :param enabled: If true, incoming audio is processed for DTMF (dual tone multi frequency) events. For example, if the caller presses a button on their telephone keypad and DTMF processing is enabled, Dialogflow will detect the event (e.g. a "3" was pressed) in the incoming audio and pass the event to the bot to drive business logic (e.g. when 3 is pressed, return the account balance). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_agent#enabled GoogleDialogflowCxAgent#enabled}
        :param finish_digit: The digit that terminates a DTMF digit sequence. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_agent#finish_digit GoogleDialogflowCxAgent#finish_digit}
        :param max_digits: Max length of DTMF digits. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_agent#max_digits GoogleDialogflowCxAgent#max_digits}
        '''
        value = GoogleDialogflowCxAgentAdvancedSettingsDtmfSettings(
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
        :param enable_consent_based_redaction: Enables consent-based end-user input redaction, if true, a pre-defined session parameter **$session.params.conversation-redaction** will be used to determine if the utterance should be redacted. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_agent#enable_consent_based_redaction GoogleDialogflowCxAgent#enable_consent_based_redaction}
        :param enable_interaction_logging: Enables DF Interaction logging. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_agent#enable_interaction_logging GoogleDialogflowCxAgent#enable_interaction_logging}
        :param enable_stackdriver_logging: Enables Google Cloud Logging. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_agent#enable_stackdriver_logging GoogleDialogflowCxAgent#enable_stackdriver_logging}
        '''
        value = GoogleDialogflowCxAgentAdvancedSettingsLoggingSettings(
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
        :param endpointer_sensitivity: Sensitivity of the speech model that detects the end of speech. Scale from 0 to 100. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_agent#endpointer_sensitivity GoogleDialogflowCxAgent#endpointer_sensitivity}
        :param models: Mapping from language to Speech-to-Text model. The mapped Speech-to-Text model will be selected for requests from its corresponding language. For more information, see `Speech models <https://cloud.google.com/dialogflow/cx/docs/concept/speech-models>`_. An object containing a list of **"key": value** pairs. Example: **{ "name": "wrench", "mass": "1.3kg", "count": "3" }**. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_agent#models GoogleDialogflowCxAgent#models}
        :param no_speech_timeout: Timeout before detecting no speech. A duration in seconds with up to nine fractional digits, ending with 's'. Example: "3.5s". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_agent#no_speech_timeout GoogleDialogflowCxAgent#no_speech_timeout}
        :param use_timeout_based_endpointing: Use timeout based endpointing, interpreting endpointer sensitivity as seconds of timeout value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_agent#use_timeout_based_endpointing GoogleDialogflowCxAgent#use_timeout_based_endpointing}
        '''
        value = GoogleDialogflowCxAgentAdvancedSettingsSpeechSettings(
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
    ) -> GoogleDialogflowCxAgentAdvancedSettingsAudioExportGcsDestinationOutputReference:
        return typing.cast(GoogleDialogflowCxAgentAdvancedSettingsAudioExportGcsDestinationOutputReference, jsii.get(self, "audioExportGcsDestination"))

    @builtins.property
    @jsii.member(jsii_name="dtmfSettings")
    def dtmf_settings(
        self,
    ) -> GoogleDialogflowCxAgentAdvancedSettingsDtmfSettingsOutputReference:
        return typing.cast(GoogleDialogflowCxAgentAdvancedSettingsDtmfSettingsOutputReference, jsii.get(self, "dtmfSettings"))

    @builtins.property
    @jsii.member(jsii_name="loggingSettings")
    def logging_settings(
        self,
    ) -> GoogleDialogflowCxAgentAdvancedSettingsLoggingSettingsOutputReference:
        return typing.cast(GoogleDialogflowCxAgentAdvancedSettingsLoggingSettingsOutputReference, jsii.get(self, "loggingSettings"))

    @builtins.property
    @jsii.member(jsii_name="speechSettings")
    def speech_settings(
        self,
    ) -> "GoogleDialogflowCxAgentAdvancedSettingsSpeechSettingsOutputReference":
        return typing.cast("GoogleDialogflowCxAgentAdvancedSettingsSpeechSettingsOutputReference", jsii.get(self, "speechSettings"))

    @builtins.property
    @jsii.member(jsii_name="audioExportGcsDestinationInput")
    def audio_export_gcs_destination_input(
        self,
    ) -> typing.Optional[GoogleDialogflowCxAgentAdvancedSettingsAudioExportGcsDestination]:
        return typing.cast(typing.Optional[GoogleDialogflowCxAgentAdvancedSettingsAudioExportGcsDestination], jsii.get(self, "audioExportGcsDestinationInput"))

    @builtins.property
    @jsii.member(jsii_name="dtmfSettingsInput")
    def dtmf_settings_input(
        self,
    ) -> typing.Optional[GoogleDialogflowCxAgentAdvancedSettingsDtmfSettings]:
        return typing.cast(typing.Optional[GoogleDialogflowCxAgentAdvancedSettingsDtmfSettings], jsii.get(self, "dtmfSettingsInput"))

    @builtins.property
    @jsii.member(jsii_name="loggingSettingsInput")
    def logging_settings_input(
        self,
    ) -> typing.Optional[GoogleDialogflowCxAgentAdvancedSettingsLoggingSettings]:
        return typing.cast(typing.Optional[GoogleDialogflowCxAgentAdvancedSettingsLoggingSettings], jsii.get(self, "loggingSettingsInput"))

    @builtins.property
    @jsii.member(jsii_name="speechSettingsInput")
    def speech_settings_input(
        self,
    ) -> typing.Optional["GoogleDialogflowCxAgentAdvancedSettingsSpeechSettings"]:
        return typing.cast(typing.Optional["GoogleDialogflowCxAgentAdvancedSettingsSpeechSettings"], jsii.get(self, "speechSettingsInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDialogflowCxAgentAdvancedSettings]:
        return typing.cast(typing.Optional[GoogleDialogflowCxAgentAdvancedSettings], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDialogflowCxAgentAdvancedSettings],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__de640232010ecafe349b807907f77ad04f56cf29382edb40226488ad6ad55df1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDialogflowCxAgent.GoogleDialogflowCxAgentAdvancedSettingsSpeechSettings",
    jsii_struct_bases=[],
    name_mapping={
        "endpointer_sensitivity": "endpointerSensitivity",
        "models": "models",
        "no_speech_timeout": "noSpeechTimeout",
        "use_timeout_based_endpointing": "useTimeoutBasedEndpointing",
    },
)
class GoogleDialogflowCxAgentAdvancedSettingsSpeechSettings:
    def __init__(
        self,
        *,
        endpointer_sensitivity: typing.Optional[jsii.Number] = None,
        models: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        no_speech_timeout: typing.Optional[builtins.str] = None,
        use_timeout_based_endpointing: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param endpointer_sensitivity: Sensitivity of the speech model that detects the end of speech. Scale from 0 to 100. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_agent#endpointer_sensitivity GoogleDialogflowCxAgent#endpointer_sensitivity}
        :param models: Mapping from language to Speech-to-Text model. The mapped Speech-to-Text model will be selected for requests from its corresponding language. For more information, see `Speech models <https://cloud.google.com/dialogflow/cx/docs/concept/speech-models>`_. An object containing a list of **"key": value** pairs. Example: **{ "name": "wrench", "mass": "1.3kg", "count": "3" }**. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_agent#models GoogleDialogflowCxAgent#models}
        :param no_speech_timeout: Timeout before detecting no speech. A duration in seconds with up to nine fractional digits, ending with 's'. Example: "3.5s". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_agent#no_speech_timeout GoogleDialogflowCxAgent#no_speech_timeout}
        :param use_timeout_based_endpointing: Use timeout based endpointing, interpreting endpointer sensitivity as seconds of timeout value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_agent#use_timeout_based_endpointing GoogleDialogflowCxAgent#use_timeout_based_endpointing}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__94113e8eaaf132e2549619115c7d535090cda218d538b1d2d273da23a805094e)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_agent#endpointer_sensitivity GoogleDialogflowCxAgent#endpointer_sensitivity}
        '''
        result = self._values.get("endpointer_sensitivity")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def models(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Mapping from language to Speech-to-Text model.

        The mapped Speech-to-Text model will be selected for requests from its corresponding language. For more information, see `Speech models <https://cloud.google.com/dialogflow/cx/docs/concept/speech-models>`_.
        An object containing a list of **"key": value** pairs. Example: **{ "name": "wrench", "mass": "1.3kg", "count": "3" }**.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_agent#models GoogleDialogflowCxAgent#models}
        '''
        result = self._values.get("models")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def no_speech_timeout(self) -> typing.Optional[builtins.str]:
        '''Timeout before detecting no speech. A duration in seconds with up to nine fractional digits, ending with 's'. Example: "3.5s".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_agent#no_speech_timeout GoogleDialogflowCxAgent#no_speech_timeout}
        '''
        result = self._values.get("no_speech_timeout")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def use_timeout_based_endpointing(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Use timeout based endpointing, interpreting endpointer sensitivity as seconds of timeout value.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_agent#use_timeout_based_endpointing GoogleDialogflowCxAgent#use_timeout_based_endpointing}
        '''
        result = self._values.get("use_timeout_based_endpointing")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDialogflowCxAgentAdvancedSettingsSpeechSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDialogflowCxAgentAdvancedSettingsSpeechSettingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDialogflowCxAgent.GoogleDialogflowCxAgentAdvancedSettingsSpeechSettingsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9fe35c5103e03946ca92a605d802ae75cc0d30d5731ac9df77d6836abe5015fe)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1ec6cf8b07d89b5acebd34a3ef3c07676b9fd1b77a5dfdc531810d2f7f149895)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "endpointerSensitivity", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="models")
    def models(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "models"))

    @models.setter
    def models(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__29ea591c8b5575a1607015a69f3661fbe61a86c7eecf8d97f067f3bd199a1cb6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "models", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="noSpeechTimeout")
    def no_speech_timeout(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "noSpeechTimeout"))

    @no_speech_timeout.setter
    def no_speech_timeout(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__df82d6fdff662519757af753b00eea2a653260137b4978b40621e16d4d4ae057)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0bb93aff7a81e971b30a3f250a89b0392eea8c0afc853f6a57d621c50528417a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "useTimeoutBasedEndpointing", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDialogflowCxAgentAdvancedSettingsSpeechSettings]:
        return typing.cast(typing.Optional[GoogleDialogflowCxAgentAdvancedSettingsSpeechSettings], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDialogflowCxAgentAdvancedSettingsSpeechSettings],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b0d351c14fa73535ae4072379e5907a0572ae0cdc10db73e0baefa9cc4b3bb1f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDialogflowCxAgent.GoogleDialogflowCxAgentConfig",
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
class GoogleDialogflowCxAgentConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        advanced_settings: typing.Optional[typing.Union[GoogleDialogflowCxAgentAdvancedSettings, typing.Dict[builtins.str, typing.Any]]] = None,
        avatar_uri: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        enable_spell_correction: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_stackdriver_logging: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        gen_app_builder_settings: typing.Optional[typing.Union["GoogleDialogflowCxAgentGenAppBuilderSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        git_integration_settings: typing.Optional[typing.Union["GoogleDialogflowCxAgentGitIntegrationSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        security_settings: typing.Optional[builtins.str] = None,
        speech_to_text_settings: typing.Optional[typing.Union["GoogleDialogflowCxAgentSpeechToTextSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        supported_language_codes: typing.Optional[typing.Sequence[builtins.str]] = None,
        text_to_speech_settings: typing.Optional[typing.Union["GoogleDialogflowCxAgentTextToSpeechSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["GoogleDialogflowCxAgentTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param default_language_code: The default language of the agent as a language tag. `See Language Support <https://cloud.google.com/dialogflow/cx/docs/reference/language>`_ for a list of the currently supported language codes. This field cannot be updated after creation. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_agent#default_language_code GoogleDialogflowCxAgent#default_language_code}
        :param display_name: The human-readable name of the agent, unique within the location. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_agent#display_name GoogleDialogflowCxAgent#display_name}
        :param location: The name of the location this agent is located in. ~> **Note:** The first time you are deploying an Agent in your project you must configure location settings. This is a one time step but at the moment you can only `configure location settings <https://cloud.google.com/dialogflow/cx/docs/concept/region#location-settings>`_ via the Dialogflow CX console. Another options is to use global location so you don't need to manually configure location settings. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_agent#location GoogleDialogflowCxAgent#location}
        :param time_zone: The time zone of this agent from the `time zone database <https://www.iana.org/time-zones>`_, e.g., America/New_York, Europe/Paris. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_agent#time_zone GoogleDialogflowCxAgent#time_zone}
        :param advanced_settings: advanced_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_agent#advanced_settings GoogleDialogflowCxAgent#advanced_settings}
        :param avatar_uri: The URI of the agent's avatar. Avatars are used throughout the Dialogflow console and in the self-hosted Web Demo integration. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_agent#avatar_uri GoogleDialogflowCxAgent#avatar_uri}
        :param description: The description of this agent. The maximum length is 500 characters. If exceeded, the request is rejected. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_agent#description GoogleDialogflowCxAgent#description}
        :param enable_spell_correction: Indicates if automatic spell correction is enabled in detect intent requests. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_agent#enable_spell_correction GoogleDialogflowCxAgent#enable_spell_correction}
        :param enable_stackdriver_logging: Determines whether this agent should log conversation queries. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_agent#enable_stackdriver_logging GoogleDialogflowCxAgent#enable_stackdriver_logging}
        :param gen_app_builder_settings: gen_app_builder_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_agent#gen_app_builder_settings GoogleDialogflowCxAgent#gen_app_builder_settings}
        :param git_integration_settings: git_integration_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_agent#git_integration_settings GoogleDialogflowCxAgent#git_integration_settings}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_agent#id GoogleDialogflowCxAgent#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_agent#project GoogleDialogflowCxAgent#project}.
        :param security_settings: Name of the SecuritySettings reference for the agent. Format: projects//locations//securitySettings/. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_agent#security_settings GoogleDialogflowCxAgent#security_settings}
        :param speech_to_text_settings: speech_to_text_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_agent#speech_to_text_settings GoogleDialogflowCxAgent#speech_to_text_settings}
        :param supported_language_codes: The list of all languages supported by this agent (except for the default_language_code). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_agent#supported_language_codes GoogleDialogflowCxAgent#supported_language_codes}
        :param text_to_speech_settings: text_to_speech_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_agent#text_to_speech_settings GoogleDialogflowCxAgent#text_to_speech_settings}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_agent#timeouts GoogleDialogflowCxAgent#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(advanced_settings, dict):
            advanced_settings = GoogleDialogflowCxAgentAdvancedSettings(**advanced_settings)
        if isinstance(gen_app_builder_settings, dict):
            gen_app_builder_settings = GoogleDialogflowCxAgentGenAppBuilderSettings(**gen_app_builder_settings)
        if isinstance(git_integration_settings, dict):
            git_integration_settings = GoogleDialogflowCxAgentGitIntegrationSettings(**git_integration_settings)
        if isinstance(speech_to_text_settings, dict):
            speech_to_text_settings = GoogleDialogflowCxAgentSpeechToTextSettings(**speech_to_text_settings)
        if isinstance(text_to_speech_settings, dict):
            text_to_speech_settings = GoogleDialogflowCxAgentTextToSpeechSettings(**text_to_speech_settings)
        if isinstance(timeouts, dict):
            timeouts = GoogleDialogflowCxAgentTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cdd776bb719b34a1cc2e63a7eea8701e0e9ddf0d838184fa109a83eea4766b4e)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_agent#default_language_code GoogleDialogflowCxAgent#default_language_code}
        '''
        result = self._values.get("default_language_code")
        assert result is not None, "Required property 'default_language_code' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def display_name(self) -> builtins.str:
        '''The human-readable name of the agent, unique within the location.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_agent#display_name GoogleDialogflowCxAgent#display_name}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_agent#location GoogleDialogflowCxAgent#location}
        '''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def time_zone(self) -> builtins.str:
        '''The time zone of this agent from the `time zone database <https://www.iana.org/time-zones>`_, e.g., America/New_York, Europe/Paris.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_agent#time_zone GoogleDialogflowCxAgent#time_zone}
        '''
        result = self._values.get("time_zone")
        assert result is not None, "Required property 'time_zone' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def advanced_settings(
        self,
    ) -> typing.Optional[GoogleDialogflowCxAgentAdvancedSettings]:
        '''advanced_settings block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_agent#advanced_settings GoogleDialogflowCxAgent#advanced_settings}
        '''
        result = self._values.get("advanced_settings")
        return typing.cast(typing.Optional[GoogleDialogflowCxAgentAdvancedSettings], result)

    @builtins.property
    def avatar_uri(self) -> typing.Optional[builtins.str]:
        '''The URI of the agent's avatar.

        Avatars are used throughout the Dialogflow console and in the self-hosted Web Demo integration.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_agent#avatar_uri GoogleDialogflowCxAgent#avatar_uri}
        '''
        result = self._values.get("avatar_uri")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of this agent. The maximum length is 500 characters. If exceeded, the request is rejected.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_agent#description GoogleDialogflowCxAgent#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enable_spell_correction(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Indicates if automatic spell correction is enabled in detect intent requests.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_agent#enable_spell_correction GoogleDialogflowCxAgent#enable_spell_correction}
        '''
        result = self._values.get("enable_spell_correction")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def enable_stackdriver_logging(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Determines whether this agent should log conversation queries.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_agent#enable_stackdriver_logging GoogleDialogflowCxAgent#enable_stackdriver_logging}
        '''
        result = self._values.get("enable_stackdriver_logging")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def gen_app_builder_settings(
        self,
    ) -> typing.Optional["GoogleDialogflowCxAgentGenAppBuilderSettings"]:
        '''gen_app_builder_settings block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_agent#gen_app_builder_settings GoogleDialogflowCxAgent#gen_app_builder_settings}
        '''
        result = self._values.get("gen_app_builder_settings")
        return typing.cast(typing.Optional["GoogleDialogflowCxAgentGenAppBuilderSettings"], result)

    @builtins.property
    def git_integration_settings(
        self,
    ) -> typing.Optional["GoogleDialogflowCxAgentGitIntegrationSettings"]:
        '''git_integration_settings block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_agent#git_integration_settings GoogleDialogflowCxAgent#git_integration_settings}
        '''
        result = self._values.get("git_integration_settings")
        return typing.cast(typing.Optional["GoogleDialogflowCxAgentGitIntegrationSettings"], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_agent#id GoogleDialogflowCxAgent#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_agent#project GoogleDialogflowCxAgent#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def security_settings(self) -> typing.Optional[builtins.str]:
        '''Name of the SecuritySettings reference for the agent. Format: projects//locations//securitySettings/.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_agent#security_settings GoogleDialogflowCxAgent#security_settings}
        '''
        result = self._values.get("security_settings")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def speech_to_text_settings(
        self,
    ) -> typing.Optional["GoogleDialogflowCxAgentSpeechToTextSettings"]:
        '''speech_to_text_settings block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_agent#speech_to_text_settings GoogleDialogflowCxAgent#speech_to_text_settings}
        '''
        result = self._values.get("speech_to_text_settings")
        return typing.cast(typing.Optional["GoogleDialogflowCxAgentSpeechToTextSettings"], result)

    @builtins.property
    def supported_language_codes(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The list of all languages supported by this agent (except for the default_language_code).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_agent#supported_language_codes GoogleDialogflowCxAgent#supported_language_codes}
        '''
        result = self._values.get("supported_language_codes")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def text_to_speech_settings(
        self,
    ) -> typing.Optional["GoogleDialogflowCxAgentTextToSpeechSettings"]:
        '''text_to_speech_settings block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_agent#text_to_speech_settings GoogleDialogflowCxAgent#text_to_speech_settings}
        '''
        result = self._values.get("text_to_speech_settings")
        return typing.cast(typing.Optional["GoogleDialogflowCxAgentTextToSpeechSettings"], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["GoogleDialogflowCxAgentTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_agent#timeouts GoogleDialogflowCxAgent#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["GoogleDialogflowCxAgentTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDialogflowCxAgentConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDialogflowCxAgent.GoogleDialogflowCxAgentGenAppBuilderSettings",
    jsii_struct_bases=[],
    name_mapping={"engine": "engine"},
)
class GoogleDialogflowCxAgentGenAppBuilderSettings:
    def __init__(self, *, engine: builtins.str) -> None:
        '''
        :param engine: The full name of the Gen App Builder engine related to this agent if there is one. Format: projects/{Project ID}/locations/{Location ID}/collections/{Collection ID}/engines/{Engine ID} Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_agent#engine GoogleDialogflowCxAgent#engine}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d004519c9e5a977164c456e41594c189437f7db562db2020fb91f0abb31975c)
            check_type(argname="argument engine", value=engine, expected_type=type_hints["engine"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "engine": engine,
        }

    @builtins.property
    def engine(self) -> builtins.str:
        '''The full name of the Gen App Builder engine related to this agent if there is one.

        Format: projects/{Project ID}/locations/{Location ID}/collections/{Collection ID}/engines/{Engine ID}

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_agent#engine GoogleDialogflowCxAgent#engine}
        '''
        result = self._values.get("engine")
        assert result is not None, "Required property 'engine' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDialogflowCxAgentGenAppBuilderSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDialogflowCxAgentGenAppBuilderSettingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDialogflowCxAgent.GoogleDialogflowCxAgentGenAppBuilderSettingsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3961da80c7ea39425bb78f7093d4e1555d09edd05a51973e6646f08aee6d4a0d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b2a5c03c8aff705021610bd3b83d646b93d9430442534ba397703649f7f01334)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "engine", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDialogflowCxAgentGenAppBuilderSettings]:
        return typing.cast(typing.Optional[GoogleDialogflowCxAgentGenAppBuilderSettings], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDialogflowCxAgentGenAppBuilderSettings],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d3c17dea32ee1074af44b1d421df6a3c5b74c669fe7b2d3f77943b93894f633e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDialogflowCxAgent.GoogleDialogflowCxAgentGitIntegrationSettings",
    jsii_struct_bases=[],
    name_mapping={"github_settings": "githubSettings"},
)
class GoogleDialogflowCxAgentGitIntegrationSettings:
    def __init__(
        self,
        *,
        github_settings: typing.Optional[typing.Union["GoogleDialogflowCxAgentGitIntegrationSettingsGithubSettings", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param github_settings: github_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_agent#github_settings GoogleDialogflowCxAgent#github_settings}
        '''
        if isinstance(github_settings, dict):
            github_settings = GoogleDialogflowCxAgentGitIntegrationSettingsGithubSettings(**github_settings)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7413302e2938512ac0f133a0938272a96c9d030bbf9ec486b098efd6aa918428)
            check_type(argname="argument github_settings", value=github_settings, expected_type=type_hints["github_settings"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if github_settings is not None:
            self._values["github_settings"] = github_settings

    @builtins.property
    def github_settings(
        self,
    ) -> typing.Optional["GoogleDialogflowCxAgentGitIntegrationSettingsGithubSettings"]:
        '''github_settings block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_agent#github_settings GoogleDialogflowCxAgent#github_settings}
        '''
        result = self._values.get("github_settings")
        return typing.cast(typing.Optional["GoogleDialogflowCxAgentGitIntegrationSettingsGithubSettings"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDialogflowCxAgentGitIntegrationSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDialogflowCxAgent.GoogleDialogflowCxAgentGitIntegrationSettingsGithubSettings",
    jsii_struct_bases=[],
    name_mapping={
        "access_token": "accessToken",
        "branches": "branches",
        "display_name": "displayName",
        "repository_uri": "repositoryUri",
        "tracking_branch": "trackingBranch",
    },
)
class GoogleDialogflowCxAgentGitIntegrationSettingsGithubSettings:
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
        :param access_token: The access token used to authenticate the access to the GitHub repository. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_agent#access_token GoogleDialogflowCxAgent#access_token}
        :param branches: A list of branches configured to be used from Dialogflow. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_agent#branches GoogleDialogflowCxAgent#branches}
        :param display_name: The unique repository display name for the GitHub repository. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_agent#display_name GoogleDialogflowCxAgent#display_name}
        :param repository_uri: The GitHub repository URI related to the agent. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_agent#repository_uri GoogleDialogflowCxAgent#repository_uri}
        :param tracking_branch: The branch of the GitHub repository tracked for this agent. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_agent#tracking_branch GoogleDialogflowCxAgent#tracking_branch}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__77ad9f7e06bf786ce2347f94eeca73dcfe2bfa2d7425258473436d469bbad8c8)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_agent#access_token GoogleDialogflowCxAgent#access_token}
        '''
        result = self._values.get("access_token")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def branches(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of branches configured to be used from Dialogflow.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_agent#branches GoogleDialogflowCxAgent#branches}
        '''
        result = self._values.get("branches")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def display_name(self) -> typing.Optional[builtins.str]:
        '''The unique repository display name for the GitHub repository.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_agent#display_name GoogleDialogflowCxAgent#display_name}
        '''
        result = self._values.get("display_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def repository_uri(self) -> typing.Optional[builtins.str]:
        '''The GitHub repository URI related to the agent.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_agent#repository_uri GoogleDialogflowCxAgent#repository_uri}
        '''
        result = self._values.get("repository_uri")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tracking_branch(self) -> typing.Optional[builtins.str]:
        '''The branch of the GitHub repository tracked for this agent.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_agent#tracking_branch GoogleDialogflowCxAgent#tracking_branch}
        '''
        result = self._values.get("tracking_branch")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDialogflowCxAgentGitIntegrationSettingsGithubSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDialogflowCxAgentGitIntegrationSettingsGithubSettingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDialogflowCxAgent.GoogleDialogflowCxAgentGitIntegrationSettingsGithubSettingsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c573c34196f2e9dc3c39817a1f94639888461ea75e8092e07b7c9887adff0c2a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__49919b53a85ec1a4fb04db0efd5e0c6aa19b38ab828e9e49670e6e60a2e8f29f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accessToken", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="branches")
    def branches(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "branches"))

    @branches.setter
    def branches(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0dbbca1347971c9025875ebf7682962f0cd26c1bd1953e545faa4a455db73319)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "branches", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="displayName")
    def display_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "displayName"))

    @display_name.setter
    def display_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b4c9ad391d128ab6efa7b0599348ab410e4b0175cd2b3d6d2859eae89ed9f8bd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "displayName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="repositoryUri")
    def repository_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "repositoryUri"))

    @repository_uri.setter
    def repository_uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__558fe2dece9b371340a203c7b55563387b0e2fb12c599cbda19d6e9e4cfea9e1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "repositoryUri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="trackingBranch")
    def tracking_branch(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "trackingBranch"))

    @tracking_branch.setter
    def tracking_branch(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__85d0268575e7e08d8c9e3de2d09872e5e9bb75c81f2eb922742683f687c05643)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "trackingBranch", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDialogflowCxAgentGitIntegrationSettingsGithubSettings]:
        return typing.cast(typing.Optional[GoogleDialogflowCxAgentGitIntegrationSettingsGithubSettings], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDialogflowCxAgentGitIntegrationSettingsGithubSettings],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__af055d9de43927e96f1748248603b615624bbcc1abcfd1d678921555d6cfa1df)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleDialogflowCxAgentGitIntegrationSettingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDialogflowCxAgent.GoogleDialogflowCxAgentGitIntegrationSettingsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__941ae479a22b23c118a5c06438f63e43a2651c9247888c0544a65fcc2477cc61)
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
        :param access_token: The access token used to authenticate the access to the GitHub repository. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_agent#access_token GoogleDialogflowCxAgent#access_token}
        :param branches: A list of branches configured to be used from Dialogflow. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_agent#branches GoogleDialogflowCxAgent#branches}
        :param display_name: The unique repository display name for the GitHub repository. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_agent#display_name GoogleDialogflowCxAgent#display_name}
        :param repository_uri: The GitHub repository URI related to the agent. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_agent#repository_uri GoogleDialogflowCxAgent#repository_uri}
        :param tracking_branch: The branch of the GitHub repository tracked for this agent. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_agent#tracking_branch GoogleDialogflowCxAgent#tracking_branch}
        '''
        value = GoogleDialogflowCxAgentGitIntegrationSettingsGithubSettings(
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
    ) -> GoogleDialogflowCxAgentGitIntegrationSettingsGithubSettingsOutputReference:
        return typing.cast(GoogleDialogflowCxAgentGitIntegrationSettingsGithubSettingsOutputReference, jsii.get(self, "githubSettings"))

    @builtins.property
    @jsii.member(jsii_name="githubSettingsInput")
    def github_settings_input(
        self,
    ) -> typing.Optional[GoogleDialogflowCxAgentGitIntegrationSettingsGithubSettings]:
        return typing.cast(typing.Optional[GoogleDialogflowCxAgentGitIntegrationSettingsGithubSettings], jsii.get(self, "githubSettingsInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDialogflowCxAgentGitIntegrationSettings]:
        return typing.cast(typing.Optional[GoogleDialogflowCxAgentGitIntegrationSettings], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDialogflowCxAgentGitIntegrationSettings],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ffdb62ab00cf31c4e6a67ea59e57497b29480c99cd17a485a56bfc0785192d3a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDialogflowCxAgent.GoogleDialogflowCxAgentSpeechToTextSettings",
    jsii_struct_bases=[],
    name_mapping={"enable_speech_adaptation": "enableSpeechAdaptation"},
)
class GoogleDialogflowCxAgentSpeechToTextSettings:
    def __init__(
        self,
        *,
        enable_speech_adaptation: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param enable_speech_adaptation: Whether to use speech adaptation for speech recognition. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_agent#enable_speech_adaptation GoogleDialogflowCxAgent#enable_speech_adaptation}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__68033230e2091c9acb17b67150483bee4636f2e3748901138d2eda2079a1a59d)
            check_type(argname="argument enable_speech_adaptation", value=enable_speech_adaptation, expected_type=type_hints["enable_speech_adaptation"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if enable_speech_adaptation is not None:
            self._values["enable_speech_adaptation"] = enable_speech_adaptation

    @builtins.property
    def enable_speech_adaptation(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether to use speech adaptation for speech recognition.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_agent#enable_speech_adaptation GoogleDialogflowCxAgent#enable_speech_adaptation}
        '''
        result = self._values.get("enable_speech_adaptation")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDialogflowCxAgentSpeechToTextSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDialogflowCxAgentSpeechToTextSettingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDialogflowCxAgent.GoogleDialogflowCxAgentSpeechToTextSettingsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a58a30cd12b164f49dca868b1979fa3ab311ad444ccc2151d39096e8b9ef6c5c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__41b6d8d7f5f685139ab7bb4f0eed8df54061f4d1c1dddebf21b530350dbc96f9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableSpeechAdaptation", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDialogflowCxAgentSpeechToTextSettings]:
        return typing.cast(typing.Optional[GoogleDialogflowCxAgentSpeechToTextSettings], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDialogflowCxAgentSpeechToTextSettings],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a0e52067b7370711ef264d41dd9b8b1535d7d744868269aedf5a948b9aa42205)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDialogflowCxAgent.GoogleDialogflowCxAgentTextToSpeechSettings",
    jsii_struct_bases=[],
    name_mapping={"synthesize_speech_configs": "synthesizeSpeechConfigs"},
)
class GoogleDialogflowCxAgentTextToSpeechSettings:
    def __init__(
        self,
        *,
        synthesize_speech_configs: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param synthesize_speech_configs: Configuration of how speech should be synthesized, mapping from `language <https://cloud.google.com/dialogflow/cx/docs/reference/language>`_ to `SynthesizeSpeechConfig <https://cloud.google.com/dialogflow/cx/docs/reference/rest/v3/projects.locations.agents#synthesizespeechconfig>`_. These settings affect: * The phone gateway synthesize configuration set via Agent.text_to_speech_settings. * How speech is synthesized when invoking session APIs. 'Agent.text_to_speech_settings' only applies if 'OutputAudioConfig.synthesize_speech_config' is not specified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_agent#synthesize_speech_configs GoogleDialogflowCxAgent#synthesize_speech_configs}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3f9943b379dd5b967d5adb9337a32e4651a21c5ff3b9287c98fa85985dd9f851)
            check_type(argname="argument synthesize_speech_configs", value=synthesize_speech_configs, expected_type=type_hints["synthesize_speech_configs"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if synthesize_speech_configs is not None:
            self._values["synthesize_speech_configs"] = synthesize_speech_configs

    @builtins.property
    def synthesize_speech_configs(self) -> typing.Optional[builtins.str]:
        '''Configuration of how speech should be synthesized, mapping from `language <https://cloud.google.com/dialogflow/cx/docs/reference/language>`_ to `SynthesizeSpeechConfig <https://cloud.google.com/dialogflow/cx/docs/reference/rest/v3/projects.locations.agents#synthesizespeechconfig>`_. These settings affect: * The phone gateway synthesize configuration set via Agent.text_to_speech_settings. * How speech is synthesized when invoking session APIs. 'Agent.text_to_speech_settings' only applies if 'OutputAudioConfig.synthesize_speech_config' is not specified.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_agent#synthesize_speech_configs GoogleDialogflowCxAgent#synthesize_speech_configs}
        '''
        result = self._values.get("synthesize_speech_configs")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDialogflowCxAgentTextToSpeechSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDialogflowCxAgentTextToSpeechSettingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDialogflowCxAgent.GoogleDialogflowCxAgentTextToSpeechSettingsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__80f40d26e103d4f5cbda9d1356fc657dfacc74af4274e8569d5ebc0f665330e9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__df65298841b473427cceca0e015f04fd344971f243daf72ca47f803629314fb8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "synthesizeSpeechConfigs", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDialogflowCxAgentTextToSpeechSettings]:
        return typing.cast(typing.Optional[GoogleDialogflowCxAgentTextToSpeechSettings], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDialogflowCxAgentTextToSpeechSettings],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ec9038d41263ebfe30d9f3fe36353ddc115eb4668e6a746b5b01328694e8c818)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDialogflowCxAgent.GoogleDialogflowCxAgentTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class GoogleDialogflowCxAgentTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_agent#create GoogleDialogflowCxAgent#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_agent#delete GoogleDialogflowCxAgent#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_agent#update GoogleDialogflowCxAgent#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__225720a17f5b4a5f36f61e5ddad0a7f28badc0a007952351a0fea2d42feb801b)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_agent#create GoogleDialogflowCxAgent#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_agent#delete GoogleDialogflowCxAgent#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_agent#update GoogleDialogflowCxAgent#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDialogflowCxAgentTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDialogflowCxAgentTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDialogflowCxAgent.GoogleDialogflowCxAgentTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__260c906e2420892ae299388924c7c96519351103cbc2af04f76cde081134cfea)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2db32879b4ff8a436635ef01afb0c0a9afc7ea0929646bbd959a8ad5e16029b8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__017633a77912086d09a0163e2b1968394ec46428b313e5ebefc6b5889cfd8577)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__05c957ebc0759447ca1f28c4992a97cae2011ede36992929a042cf6570992935)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDialogflowCxAgentTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDialogflowCxAgentTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDialogflowCxAgentTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d6f0fa6684d217aadc86171473ba1a44904cf3e8652d47b77253d297956be95d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "GoogleDialogflowCxAgent",
    "GoogleDialogflowCxAgentAdvancedSettings",
    "GoogleDialogflowCxAgentAdvancedSettingsAudioExportGcsDestination",
    "GoogleDialogflowCxAgentAdvancedSettingsAudioExportGcsDestinationOutputReference",
    "GoogleDialogflowCxAgentAdvancedSettingsDtmfSettings",
    "GoogleDialogflowCxAgentAdvancedSettingsDtmfSettingsOutputReference",
    "GoogleDialogflowCxAgentAdvancedSettingsLoggingSettings",
    "GoogleDialogflowCxAgentAdvancedSettingsLoggingSettingsOutputReference",
    "GoogleDialogflowCxAgentAdvancedSettingsOutputReference",
    "GoogleDialogflowCxAgentAdvancedSettingsSpeechSettings",
    "GoogleDialogflowCxAgentAdvancedSettingsSpeechSettingsOutputReference",
    "GoogleDialogflowCxAgentConfig",
    "GoogleDialogflowCxAgentGenAppBuilderSettings",
    "GoogleDialogflowCxAgentGenAppBuilderSettingsOutputReference",
    "GoogleDialogflowCxAgentGitIntegrationSettings",
    "GoogleDialogflowCxAgentGitIntegrationSettingsGithubSettings",
    "GoogleDialogflowCxAgentGitIntegrationSettingsGithubSettingsOutputReference",
    "GoogleDialogflowCxAgentGitIntegrationSettingsOutputReference",
    "GoogleDialogflowCxAgentSpeechToTextSettings",
    "GoogleDialogflowCxAgentSpeechToTextSettingsOutputReference",
    "GoogleDialogflowCxAgentTextToSpeechSettings",
    "GoogleDialogflowCxAgentTextToSpeechSettingsOutputReference",
    "GoogleDialogflowCxAgentTimeouts",
    "GoogleDialogflowCxAgentTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__0ca1f328a2790e853c9443590e831be92cb702fcba64a3f201ffd86cf20e0b5d(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    default_language_code: builtins.str,
    display_name: builtins.str,
    location: builtins.str,
    time_zone: builtins.str,
    advanced_settings: typing.Optional[typing.Union[GoogleDialogflowCxAgentAdvancedSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    avatar_uri: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    enable_spell_correction: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enable_stackdriver_logging: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    gen_app_builder_settings: typing.Optional[typing.Union[GoogleDialogflowCxAgentGenAppBuilderSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    git_integration_settings: typing.Optional[typing.Union[GoogleDialogflowCxAgentGitIntegrationSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    security_settings: typing.Optional[builtins.str] = None,
    speech_to_text_settings: typing.Optional[typing.Union[GoogleDialogflowCxAgentSpeechToTextSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    supported_language_codes: typing.Optional[typing.Sequence[builtins.str]] = None,
    text_to_speech_settings: typing.Optional[typing.Union[GoogleDialogflowCxAgentTextToSpeechSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[GoogleDialogflowCxAgentTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__1ddedd6bbdfd57c65d351ceb583ac0612e79a3ba8a1d85b8e1058bfbf549ce5b(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e875f2b69646bbd2e26827da76e07f873b2aa5aa4cedd1cee494a8608ad21c6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc3d0d597790982613780fcbbad91e72961e2309f7a3677377475f74a044188e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d5f781deb9d9f3716387e56cda9991aa50000a7223476aaa3f532f101679803(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__036812a32d1821e736f8dbbd23ba2b83f1cdfac0599475b20ea8f5851e63be27(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93bfffc5c247efbd81c6505c465ef314f485da80ae689ab1354d4bd989dd2ca3(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__066946d07bb61956a0ceac83b3d7d73e8bfbb76ad109eb4bd29d31344fb4d211(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0143a9bb7afda9b3f7c18ba505443153171c8fb75405d4e7bd77753abc5f5d1b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f446f2070d165ff6f6aeebda042b3ee1c13c03a64dd82cf49ff579eedb9d2b21(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34bd07c2c345a8d8a28f8062bbeecb62ae8ad9dd031c0250035caaccc096d489(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b89d837837a7874acfaf82eb79f525f77df8075f2bb7888bf9d9c03c7adc82c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64b69152ca10303499ff6dceebca860f4861413aeb57172e7da2bc3debe865de(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__780a8b69fbb0691c03bc36f83a658d1022a58fe00b047d2472911024908000bb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f7ae78c31a0b7f6305c04fe906e38ba4453aa6c5aa4f7fcc4331449fd4b4589(
    *,
    audio_export_gcs_destination: typing.Optional[typing.Union[GoogleDialogflowCxAgentAdvancedSettingsAudioExportGcsDestination, typing.Dict[builtins.str, typing.Any]]] = None,
    dtmf_settings: typing.Optional[typing.Union[GoogleDialogflowCxAgentAdvancedSettingsDtmfSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    logging_settings: typing.Optional[typing.Union[GoogleDialogflowCxAgentAdvancedSettingsLoggingSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    speech_settings: typing.Optional[typing.Union[GoogleDialogflowCxAgentAdvancedSettingsSpeechSettings, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7826a4e2aca9208785a39a6c63ce592612a8638eb14fcde6193de840f633d8f4(
    *,
    uri: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ddfc65278f04fec083af5d77e372a5a49a8d4f122f614b9c3c4a591f686a09e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0d4792faea773ffd46526c0ae03bdc340ed6740975ed38c2b520f9177716e3e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__749759f10e85cc42ca38e1f3f02a453c7c008b31d19c23e80f231d59e947a2b9(
    value: typing.Optional[GoogleDialogflowCxAgentAdvancedSettingsAudioExportGcsDestination],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a08fd56302072e718fdc252a948f0811b78e345dae49861a85062a0c16859e5(
    *,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    finish_digit: typing.Optional[builtins.str] = None,
    max_digits: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9f34e00edca4e7417e94b26d4afae2cc6bc7b224811c6119e7c1f5e4543dca7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1d2dd2efaadffde5ed5fcd493a1fde8dd90a0c3240545e9f5f0195223cea0af(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9d460a49500ea13094f34d3d974d1c5583e53c5aeedaa641f7565256a171756(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39926dd6b184ba9696fa92ad0be0c62ced0bd8b4e28c85ffaa9b0c344054c84e(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f0bf0acaa00b74483e34e0b1214ebfa4d0515ff7e0ce90d498ab80bc1432cc7(
    value: typing.Optional[GoogleDialogflowCxAgentAdvancedSettingsDtmfSettings],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f045dfeab82eb329977019edf3b6b2df073b6a5aae3766a0f152534109c65f05(
    *,
    enable_consent_based_redaction: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enable_interaction_logging: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enable_stackdriver_logging: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__909a114a1ec11e8800e27b9e2c97628ab975dd071b0890d27c00cd35f58ba3fa(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05039968d7fd799916eb89f5cdf18e08dd768caece8f022e8cadd5569b1199fb(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__08ab899897de524d21e02f2774d8074a12e4d4ff044af3ddf9753bb3a6cef863(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c41bf213d0439a60cc12c4971278a07d81fc9e2c3de07dfa6ded78194e3188c(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b78bc78ca7dcd8c1698e75c821277d72dfaded1679362ed8dfde1fde6de84ed(
    value: typing.Optional[GoogleDialogflowCxAgentAdvancedSettingsLoggingSettings],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce3511b0a511669313a4db9aaa653a4da99e2f69f6c8098cc69bf5fefa667bf7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de640232010ecafe349b807907f77ad04f56cf29382edb40226488ad6ad55df1(
    value: typing.Optional[GoogleDialogflowCxAgentAdvancedSettings],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94113e8eaaf132e2549619115c7d535090cda218d538b1d2d273da23a805094e(
    *,
    endpointer_sensitivity: typing.Optional[jsii.Number] = None,
    models: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    no_speech_timeout: typing.Optional[builtins.str] = None,
    use_timeout_based_endpointing: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9fe35c5103e03946ca92a605d802ae75cc0d30d5731ac9df77d6836abe5015fe(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ec6cf8b07d89b5acebd34a3ef3c07676b9fd1b77a5dfdc531810d2f7f149895(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29ea591c8b5575a1607015a69f3661fbe61a86c7eecf8d97f067f3bd199a1cb6(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df82d6fdff662519757af753b00eea2a653260137b4978b40621e16d4d4ae057(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0bb93aff7a81e971b30a3f250a89b0392eea8c0afc853f6a57d621c50528417a(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0d351c14fa73535ae4072379e5907a0572ae0cdc10db73e0baefa9cc4b3bb1f(
    value: typing.Optional[GoogleDialogflowCxAgentAdvancedSettingsSpeechSettings],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cdd776bb719b34a1cc2e63a7eea8701e0e9ddf0d838184fa109a83eea4766b4e(
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
    advanced_settings: typing.Optional[typing.Union[GoogleDialogflowCxAgentAdvancedSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    avatar_uri: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    enable_spell_correction: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enable_stackdriver_logging: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    gen_app_builder_settings: typing.Optional[typing.Union[GoogleDialogflowCxAgentGenAppBuilderSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    git_integration_settings: typing.Optional[typing.Union[GoogleDialogflowCxAgentGitIntegrationSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    security_settings: typing.Optional[builtins.str] = None,
    speech_to_text_settings: typing.Optional[typing.Union[GoogleDialogflowCxAgentSpeechToTextSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    supported_language_codes: typing.Optional[typing.Sequence[builtins.str]] = None,
    text_to_speech_settings: typing.Optional[typing.Union[GoogleDialogflowCxAgentTextToSpeechSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[GoogleDialogflowCxAgentTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d004519c9e5a977164c456e41594c189437f7db562db2020fb91f0abb31975c(
    *,
    engine: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3961da80c7ea39425bb78f7093d4e1555d09edd05a51973e6646f08aee6d4a0d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b2a5c03c8aff705021610bd3b83d646b93d9430442534ba397703649f7f01334(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3c17dea32ee1074af44b1d421df6a3c5b74c669fe7b2d3f77943b93894f633e(
    value: typing.Optional[GoogleDialogflowCxAgentGenAppBuilderSettings],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7413302e2938512ac0f133a0938272a96c9d030bbf9ec486b098efd6aa918428(
    *,
    github_settings: typing.Optional[typing.Union[GoogleDialogflowCxAgentGitIntegrationSettingsGithubSettings, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77ad9f7e06bf786ce2347f94eeca73dcfe2bfa2d7425258473436d469bbad8c8(
    *,
    access_token: typing.Optional[builtins.str] = None,
    branches: typing.Optional[typing.Sequence[builtins.str]] = None,
    display_name: typing.Optional[builtins.str] = None,
    repository_uri: typing.Optional[builtins.str] = None,
    tracking_branch: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c573c34196f2e9dc3c39817a1f94639888461ea75e8092e07b7c9887adff0c2a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__49919b53a85ec1a4fb04db0efd5e0c6aa19b38ab828e9e49670e6e60a2e8f29f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0dbbca1347971c9025875ebf7682962f0cd26c1bd1953e545faa4a455db73319(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4c9ad391d128ab6efa7b0599348ab410e4b0175cd2b3d6d2859eae89ed9f8bd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__558fe2dece9b371340a203c7b55563387b0e2fb12c599cbda19d6e9e4cfea9e1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85d0268575e7e08d8c9e3de2d09872e5e9bb75c81f2eb922742683f687c05643(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af055d9de43927e96f1748248603b615624bbcc1abcfd1d678921555d6cfa1df(
    value: typing.Optional[GoogleDialogflowCxAgentGitIntegrationSettingsGithubSettings],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__941ae479a22b23c118a5c06438f63e43a2651c9247888c0544a65fcc2477cc61(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ffdb62ab00cf31c4e6a67ea59e57497b29480c99cd17a485a56bfc0785192d3a(
    value: typing.Optional[GoogleDialogflowCxAgentGitIntegrationSettings],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68033230e2091c9acb17b67150483bee4636f2e3748901138d2eda2079a1a59d(
    *,
    enable_speech_adaptation: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a58a30cd12b164f49dca868b1979fa3ab311ad444ccc2151d39096e8b9ef6c5c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41b6d8d7f5f685139ab7bb4f0eed8df54061f4d1c1dddebf21b530350dbc96f9(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0e52067b7370711ef264d41dd9b8b1535d7d744868269aedf5a948b9aa42205(
    value: typing.Optional[GoogleDialogflowCxAgentSpeechToTextSettings],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f9943b379dd5b967d5adb9337a32e4651a21c5ff3b9287c98fa85985dd9f851(
    *,
    synthesize_speech_configs: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80f40d26e103d4f5cbda9d1356fc657dfacc74af4274e8569d5ebc0f665330e9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df65298841b473427cceca0e015f04fd344971f243daf72ca47f803629314fb8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec9038d41263ebfe30d9f3fe36353ddc115eb4668e6a746b5b01328694e8c818(
    value: typing.Optional[GoogleDialogflowCxAgentTextToSpeechSettings],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__225720a17f5b4a5f36f61e5ddad0a7f28badc0a007952351a0fea2d42feb801b(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__260c906e2420892ae299388924c7c96519351103cbc2af04f76cde081134cfea(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2db32879b4ff8a436635ef01afb0c0a9afc7ea0929646bbd959a8ad5e16029b8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__017633a77912086d09a0163e2b1968394ec46428b313e5ebefc6b5889cfd8577(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05c957ebc0759447ca1f28c4992a97cae2011ede36992929a042cf6570992935(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d6f0fa6684d217aadc86171473ba1a44904cf3e8652d47b77253d297956be95d(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDialogflowCxAgentTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
