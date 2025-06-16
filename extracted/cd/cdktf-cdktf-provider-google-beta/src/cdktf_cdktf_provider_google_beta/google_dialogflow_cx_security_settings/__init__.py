r'''
# `google_dialogflow_cx_security_settings`

Refer to the Terraform Registry for docs: [`google_dialogflow_cx_security_settings`](https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_security_settings).
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


class GoogleDialogflowCxSecuritySettings(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDialogflowCxSecuritySettings.GoogleDialogflowCxSecuritySettings",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_security_settings google_dialogflow_cx_security_settings}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        display_name: builtins.str,
        location: builtins.str,
        audio_export_settings: typing.Optional[typing.Union["GoogleDialogflowCxSecuritySettingsAudioExportSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        deidentify_template: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        insights_export_settings: typing.Optional[typing.Union["GoogleDialogflowCxSecuritySettingsInsightsExportSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        inspect_template: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        purge_data_types: typing.Optional[typing.Sequence[builtins.str]] = None,
        redaction_scope: typing.Optional[builtins.str] = None,
        redaction_strategy: typing.Optional[builtins.str] = None,
        retention_strategy: typing.Optional[builtins.str] = None,
        retention_window_days: typing.Optional[jsii.Number] = None,
        timeouts: typing.Optional[typing.Union["GoogleDialogflowCxSecuritySettingsTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_security_settings google_dialogflow_cx_security_settings} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param display_name: The human-readable name of the security settings, unique within the location. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_security_settings#display_name GoogleDialogflowCxSecuritySettings#display_name}
        :param location: The location these settings are located in. Settings can only be applied to an agent in the same location. See `Available Regions <https://cloud.google.com/dialogflow/cx/docs/concept/region#avail>`_ for a list of supported locations. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_security_settings#location GoogleDialogflowCxSecuritySettings#location}
        :param audio_export_settings: audio_export_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_security_settings#audio_export_settings GoogleDialogflowCxSecuritySettings#audio_export_settings}
        :param deidentify_template: `DLP <https://cloud.google.com/dlp/docs>`_ deidentify template name. Use this template to define de-identification configuration for the content. If empty, Dialogflow replaces sensitive info with [redacted] text. Note: deidentifyTemplate must be located in the same region as the SecuritySettings. Format: projects//locations//deidentifyTemplates/ OR organizations//locations//deidentifyTemplates/. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_security_settings#deidentify_template GoogleDialogflowCxSecuritySettings#deidentify_template}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_security_settings#id GoogleDialogflowCxSecuritySettings#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param insights_export_settings: insights_export_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_security_settings#insights_export_settings GoogleDialogflowCxSecuritySettings#insights_export_settings}
        :param inspect_template: `DLP <https://cloud.google.com/dlp/docs>`_ inspect template name. Use this template to define inspect base settings. If empty, we use the default DLP inspect config. Note: inspectTemplate must be located in the same region as the SecuritySettings. Format: projects//locations//inspectTemplates/ OR organizations//locations//inspectTemplates/. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_security_settings#inspect_template GoogleDialogflowCxSecuritySettings#inspect_template}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_security_settings#project GoogleDialogflowCxSecuritySettings#project}.
        :param purge_data_types: List of types of data to remove when retention settings triggers purge. Possible values: ["DIALOGFLOW_HISTORY"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_security_settings#purge_data_types GoogleDialogflowCxSecuritySettings#purge_data_types}
        :param redaction_scope: Defines what types of data to redact. If not set, defaults to not redacting any kind of data. - REDACT_DISK_STORAGE: On data to be written to disk or similar devices that are capable of holding data even if power is disconnected. This includes data that are temporarily saved on disk. Possible values: ["REDACT_DISK_STORAGE"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_security_settings#redaction_scope GoogleDialogflowCxSecuritySettings#redaction_scope}
        :param redaction_strategy: Defines how we redact data. If not set, defaults to not redacting. - REDACT_WITH_SERVICE: Call redaction service to clean up the data to be persisted. Possible values: ["REDACT_WITH_SERVICE"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_security_settings#redaction_strategy GoogleDialogflowCxSecuritySettings#redaction_strategy}
        :param retention_strategy: Defines how long we retain persisted data that contains sensitive info. Only one of 'retention_window_days' and 'retention_strategy' may be set. - REMOVE_AFTER_CONVERSATION: Removes data when the conversation ends. If there is no conversation explicitly established, a default conversation ends when the corresponding Dialogflow session ends. Possible values: ["REMOVE_AFTER_CONVERSATION"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_security_settings#retention_strategy GoogleDialogflowCxSecuritySettings#retention_strategy}
        :param retention_window_days: Retains the data for the specified number of days. User must set a value lower than Dialogflow's default 365d TTL (30 days for Agent Assist traffic), higher value will be ignored and use default. Setting a value higher than that has no effect. A missing value or setting to 0 also means we use default TTL. Only one of 'retention_window_days' and 'retention_strategy' may be set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_security_settings#retention_window_days GoogleDialogflowCxSecuritySettings#retention_window_days}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_security_settings#timeouts GoogleDialogflowCxSecuritySettings#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c9a3c160f33d4e840cfb043da32cf70af4867c9f90352146cdabbf8df0d305b9)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = GoogleDialogflowCxSecuritySettingsConfig(
            display_name=display_name,
            location=location,
            audio_export_settings=audio_export_settings,
            deidentify_template=deidentify_template,
            id=id,
            insights_export_settings=insights_export_settings,
            inspect_template=inspect_template,
            project=project,
            purge_data_types=purge_data_types,
            redaction_scope=redaction_scope,
            redaction_strategy=redaction_strategy,
            retention_strategy=retention_strategy,
            retention_window_days=retention_window_days,
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
        '''Generates CDKTF code for importing a GoogleDialogflowCxSecuritySettings resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the GoogleDialogflowCxSecuritySettings to import.
        :param import_from_id: The id of the existing GoogleDialogflowCxSecuritySettings that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_security_settings#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the GoogleDialogflowCxSecuritySettings to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__18875c45ecf4ff891c39e35f46b45f338bfa1b2c59d70bc5d44ca069417a7b90)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putAudioExportSettings")
    def put_audio_export_settings(
        self,
        *,
        audio_export_pattern: typing.Optional[builtins.str] = None,
        audio_format: typing.Optional[builtins.str] = None,
        enable_audio_redaction: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        gcs_bucket: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param audio_export_pattern: Filename pattern for exported audio. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_security_settings#audio_export_pattern GoogleDialogflowCxSecuritySettings#audio_export_pattern}
        :param audio_format: File format for exported audio file. Currently only in telephony recordings. - MULAW: G.711 mu-law PCM with 8kHz sample rate. - MP3: MP3 file format. - OGG: OGG Vorbis. Possible values: ["MULAW", "MP3", "OGG"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_security_settings#audio_format GoogleDialogflowCxSecuritySettings#audio_format}
        :param enable_audio_redaction: Enable audio redaction if it is true. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_security_settings#enable_audio_redaction GoogleDialogflowCxSecuritySettings#enable_audio_redaction}
        :param gcs_bucket: Cloud Storage bucket to export audio record to. Setting this field would grant the Storage Object Creator role to the Dialogflow Service Agent. API caller that tries to modify this field should have the permission of storage.buckets.setIamPolicy. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_security_settings#gcs_bucket GoogleDialogflowCxSecuritySettings#gcs_bucket}
        '''
        value = GoogleDialogflowCxSecuritySettingsAudioExportSettings(
            audio_export_pattern=audio_export_pattern,
            audio_format=audio_format,
            enable_audio_redaction=enable_audio_redaction,
            gcs_bucket=gcs_bucket,
        )

        return typing.cast(None, jsii.invoke(self, "putAudioExportSettings", [value]))

    @jsii.member(jsii_name="putInsightsExportSettings")
    def put_insights_export_settings(
        self,
        *,
        enable_insights_export: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        '''
        :param enable_insights_export: If enabled, we will automatically exports conversations to Insights and Insights runs its analyzers. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_security_settings#enable_insights_export GoogleDialogflowCxSecuritySettings#enable_insights_export}
        '''
        value = GoogleDialogflowCxSecuritySettingsInsightsExportSettings(
            enable_insights_export=enable_insights_export
        )

        return typing.cast(None, jsii.invoke(self, "putInsightsExportSettings", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_security_settings#create GoogleDialogflowCxSecuritySettings#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_security_settings#delete GoogleDialogflowCxSecuritySettings#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_security_settings#update GoogleDialogflowCxSecuritySettings#update}.
        '''
        value = GoogleDialogflowCxSecuritySettingsTimeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetAudioExportSettings")
    def reset_audio_export_settings(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAudioExportSettings", []))

    @jsii.member(jsii_name="resetDeidentifyTemplate")
    def reset_deidentify_template(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDeidentifyTemplate", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetInsightsExportSettings")
    def reset_insights_export_settings(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInsightsExportSettings", []))

    @jsii.member(jsii_name="resetInspectTemplate")
    def reset_inspect_template(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInspectTemplate", []))

    @jsii.member(jsii_name="resetProject")
    def reset_project(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProject", []))

    @jsii.member(jsii_name="resetPurgeDataTypes")
    def reset_purge_data_types(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPurgeDataTypes", []))

    @jsii.member(jsii_name="resetRedactionScope")
    def reset_redaction_scope(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRedactionScope", []))

    @jsii.member(jsii_name="resetRedactionStrategy")
    def reset_redaction_strategy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRedactionStrategy", []))

    @jsii.member(jsii_name="resetRetentionStrategy")
    def reset_retention_strategy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRetentionStrategy", []))

    @jsii.member(jsii_name="resetRetentionWindowDays")
    def reset_retention_window_days(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRetentionWindowDays", []))

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
    @jsii.member(jsii_name="audioExportSettings")
    def audio_export_settings(
        self,
    ) -> "GoogleDialogflowCxSecuritySettingsAudioExportSettingsOutputReference":
        return typing.cast("GoogleDialogflowCxSecuritySettingsAudioExportSettingsOutputReference", jsii.get(self, "audioExportSettings"))

    @builtins.property
    @jsii.member(jsii_name="insightsExportSettings")
    def insights_export_settings(
        self,
    ) -> "GoogleDialogflowCxSecuritySettingsInsightsExportSettingsOutputReference":
        return typing.cast("GoogleDialogflowCxSecuritySettingsInsightsExportSettingsOutputReference", jsii.get(self, "insightsExportSettings"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "GoogleDialogflowCxSecuritySettingsTimeoutsOutputReference":
        return typing.cast("GoogleDialogflowCxSecuritySettingsTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="audioExportSettingsInput")
    def audio_export_settings_input(
        self,
    ) -> typing.Optional["GoogleDialogflowCxSecuritySettingsAudioExportSettings"]:
        return typing.cast(typing.Optional["GoogleDialogflowCxSecuritySettingsAudioExportSettings"], jsii.get(self, "audioExportSettingsInput"))

    @builtins.property
    @jsii.member(jsii_name="deidentifyTemplateInput")
    def deidentify_template_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "deidentifyTemplateInput"))

    @builtins.property
    @jsii.member(jsii_name="displayNameInput")
    def display_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "displayNameInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="insightsExportSettingsInput")
    def insights_export_settings_input(
        self,
    ) -> typing.Optional["GoogleDialogflowCxSecuritySettingsInsightsExportSettings"]:
        return typing.cast(typing.Optional["GoogleDialogflowCxSecuritySettingsInsightsExportSettings"], jsii.get(self, "insightsExportSettingsInput"))

    @builtins.property
    @jsii.member(jsii_name="inspectTemplateInput")
    def inspect_template_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "inspectTemplateInput"))

    @builtins.property
    @jsii.member(jsii_name="locationInput")
    def location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "locationInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="purgeDataTypesInput")
    def purge_data_types_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "purgeDataTypesInput"))

    @builtins.property
    @jsii.member(jsii_name="redactionScopeInput")
    def redaction_scope_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "redactionScopeInput"))

    @builtins.property
    @jsii.member(jsii_name="redactionStrategyInput")
    def redaction_strategy_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "redactionStrategyInput"))

    @builtins.property
    @jsii.member(jsii_name="retentionStrategyInput")
    def retention_strategy_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "retentionStrategyInput"))

    @builtins.property
    @jsii.member(jsii_name="retentionWindowDaysInput")
    def retention_window_days_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "retentionWindowDaysInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleDialogflowCxSecuritySettingsTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleDialogflowCxSecuritySettingsTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="deidentifyTemplate")
    def deidentify_template(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "deidentifyTemplate"))

    @deidentify_template.setter
    def deidentify_template(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__880fedb90de11ef9facd4bf8fe5667b70fbd0e2bafda9fb2657f1ae88eebf001)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deidentifyTemplate", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="displayName")
    def display_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "displayName"))

    @display_name.setter
    def display_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c89da646eb55252e99a6c5a9fe5e7a6a64b5712894fc70d9404a7734f9f89773)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "displayName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__de07d3a592d95cdd6481f21f93b52d19f889b8aac8a03a30eea9edd68b9caa0f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="inspectTemplate")
    def inspect_template(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "inspectTemplate"))

    @inspect_template.setter
    def inspect_template(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c3442192d146ad0efea8842dab81964af7901f6631bdd6ecab0aefcb431808d9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "inspectTemplate", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f6df94460d09ecff375c1127d648319e63db6e15107b810a558863ee29ddda6e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__138e33b8ba5c4a06e19f000a6100cedeaa5a2e1eb11a287d5f42a44e04a3d84d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="purgeDataTypes")
    def purge_data_types(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "purgeDataTypes"))

    @purge_data_types.setter
    def purge_data_types(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__074bdf668d67152c8d1545aed7d38c2b7ddd40f974f5470f3a635891e09e6515)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "purgeDataTypes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="redactionScope")
    def redaction_scope(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "redactionScope"))

    @redaction_scope.setter
    def redaction_scope(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f6d07c0eb104af4af46f1d850d1cfe973b2b2e1834c26d7dbb69dd474a8e33b9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "redactionScope", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="redactionStrategy")
    def redaction_strategy(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "redactionStrategy"))

    @redaction_strategy.setter
    def redaction_strategy(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__26324cd259ca0d3c9fc5f24259dca5291ae41fc5132d252eadeb60475dfd1b5c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "redactionStrategy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="retentionStrategy")
    def retention_strategy(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "retentionStrategy"))

    @retention_strategy.setter
    def retention_strategy(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__11be4e7c61a2bb45aa65368b987741d50a34c26f8dcec2fc0f50956fb009433f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "retentionStrategy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="retentionWindowDays")
    def retention_window_days(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "retentionWindowDays"))

    @retention_window_days.setter
    def retention_window_days(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d18ba1a355414c02707cd43d91b8e49f70eca58a7cc41a980867c109f07d6331)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "retentionWindowDays", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDialogflowCxSecuritySettings.GoogleDialogflowCxSecuritySettingsAudioExportSettings",
    jsii_struct_bases=[],
    name_mapping={
        "audio_export_pattern": "audioExportPattern",
        "audio_format": "audioFormat",
        "enable_audio_redaction": "enableAudioRedaction",
        "gcs_bucket": "gcsBucket",
    },
)
class GoogleDialogflowCxSecuritySettingsAudioExportSettings:
    def __init__(
        self,
        *,
        audio_export_pattern: typing.Optional[builtins.str] = None,
        audio_format: typing.Optional[builtins.str] = None,
        enable_audio_redaction: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        gcs_bucket: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param audio_export_pattern: Filename pattern for exported audio. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_security_settings#audio_export_pattern GoogleDialogflowCxSecuritySettings#audio_export_pattern}
        :param audio_format: File format for exported audio file. Currently only in telephony recordings. - MULAW: G.711 mu-law PCM with 8kHz sample rate. - MP3: MP3 file format. - OGG: OGG Vorbis. Possible values: ["MULAW", "MP3", "OGG"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_security_settings#audio_format GoogleDialogflowCxSecuritySettings#audio_format}
        :param enable_audio_redaction: Enable audio redaction if it is true. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_security_settings#enable_audio_redaction GoogleDialogflowCxSecuritySettings#enable_audio_redaction}
        :param gcs_bucket: Cloud Storage bucket to export audio record to. Setting this field would grant the Storage Object Creator role to the Dialogflow Service Agent. API caller that tries to modify this field should have the permission of storage.buckets.setIamPolicy. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_security_settings#gcs_bucket GoogleDialogflowCxSecuritySettings#gcs_bucket}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8c661e3eec872e49bc32dc402fcc223c27141e06f4437541ff705cf3413663c9)
            check_type(argname="argument audio_export_pattern", value=audio_export_pattern, expected_type=type_hints["audio_export_pattern"])
            check_type(argname="argument audio_format", value=audio_format, expected_type=type_hints["audio_format"])
            check_type(argname="argument enable_audio_redaction", value=enable_audio_redaction, expected_type=type_hints["enable_audio_redaction"])
            check_type(argname="argument gcs_bucket", value=gcs_bucket, expected_type=type_hints["gcs_bucket"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if audio_export_pattern is not None:
            self._values["audio_export_pattern"] = audio_export_pattern
        if audio_format is not None:
            self._values["audio_format"] = audio_format
        if enable_audio_redaction is not None:
            self._values["enable_audio_redaction"] = enable_audio_redaction
        if gcs_bucket is not None:
            self._values["gcs_bucket"] = gcs_bucket

    @builtins.property
    def audio_export_pattern(self) -> typing.Optional[builtins.str]:
        '''Filename pattern for exported audio.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_security_settings#audio_export_pattern GoogleDialogflowCxSecuritySettings#audio_export_pattern}
        '''
        result = self._values.get("audio_export_pattern")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def audio_format(self) -> typing.Optional[builtins.str]:
        '''File format for exported audio file.

        Currently only in telephony recordings.

        - MULAW: G.711 mu-law PCM with 8kHz sample rate.
        - MP3: MP3 file format.
        - OGG: OGG Vorbis. Possible values: ["MULAW", "MP3", "OGG"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_security_settings#audio_format GoogleDialogflowCxSecuritySettings#audio_format}
        '''
        result = self._values.get("audio_format")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enable_audio_redaction(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Enable audio redaction if it is true.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_security_settings#enable_audio_redaction GoogleDialogflowCxSecuritySettings#enable_audio_redaction}
        '''
        result = self._values.get("enable_audio_redaction")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def gcs_bucket(self) -> typing.Optional[builtins.str]:
        '''Cloud Storage bucket to export audio record to.

        Setting this field would grant the Storage Object Creator role to the Dialogflow Service Agent. API caller that tries to modify this field should have the permission of storage.buckets.setIamPolicy.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_security_settings#gcs_bucket GoogleDialogflowCxSecuritySettings#gcs_bucket}
        '''
        result = self._values.get("gcs_bucket")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDialogflowCxSecuritySettingsAudioExportSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDialogflowCxSecuritySettingsAudioExportSettingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDialogflowCxSecuritySettings.GoogleDialogflowCxSecuritySettingsAudioExportSettingsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c28781a9c75e52a2fd396536b648bc122f0176dce341925602ab9edcb969b7cb)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAudioExportPattern")
    def reset_audio_export_pattern(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAudioExportPattern", []))

    @jsii.member(jsii_name="resetAudioFormat")
    def reset_audio_format(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAudioFormat", []))

    @jsii.member(jsii_name="resetEnableAudioRedaction")
    def reset_enable_audio_redaction(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnableAudioRedaction", []))

    @jsii.member(jsii_name="resetGcsBucket")
    def reset_gcs_bucket(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGcsBucket", []))

    @builtins.property
    @jsii.member(jsii_name="audioExportPatternInput")
    def audio_export_pattern_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "audioExportPatternInput"))

    @builtins.property
    @jsii.member(jsii_name="audioFormatInput")
    def audio_format_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "audioFormatInput"))

    @builtins.property
    @jsii.member(jsii_name="enableAudioRedactionInput")
    def enable_audio_redaction_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enableAudioRedactionInput"))

    @builtins.property
    @jsii.member(jsii_name="gcsBucketInput")
    def gcs_bucket_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "gcsBucketInput"))

    @builtins.property
    @jsii.member(jsii_name="audioExportPattern")
    def audio_export_pattern(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "audioExportPattern"))

    @audio_export_pattern.setter
    def audio_export_pattern(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__029452f9f37fa85bacf2cdfcec2fde3b993b0f898ec10cba7a973a5c614041b6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "audioExportPattern", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="audioFormat")
    def audio_format(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "audioFormat"))

    @audio_format.setter
    def audio_format(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eacc5c331b2bf7616ea16383be408b4c067ed90438e54bcc8a8b5b461684323c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "audioFormat", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enableAudioRedaction")
    def enable_audio_redaction(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enableAudioRedaction"))

    @enable_audio_redaction.setter
    def enable_audio_redaction(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__34f1497fa50848363d323faa744ef6da19ba5a367442d827eeb58e8820af626a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableAudioRedaction", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="gcsBucket")
    def gcs_bucket(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "gcsBucket"))

    @gcs_bucket.setter
    def gcs_bucket(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7174fe92a4581ed5a75ad43127bede31d520d4f78010c1eb122813abc1597eab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "gcsBucket", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDialogflowCxSecuritySettingsAudioExportSettings]:
        return typing.cast(typing.Optional[GoogleDialogflowCxSecuritySettingsAudioExportSettings], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDialogflowCxSecuritySettingsAudioExportSettings],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__87ad5ff244edc3e2de69a9238143c53f869050e520740a89075837dc5edf255b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDialogflowCxSecuritySettings.GoogleDialogflowCxSecuritySettingsConfig",
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
        "audio_export_settings": "audioExportSettings",
        "deidentify_template": "deidentifyTemplate",
        "id": "id",
        "insights_export_settings": "insightsExportSettings",
        "inspect_template": "inspectTemplate",
        "project": "project",
        "purge_data_types": "purgeDataTypes",
        "redaction_scope": "redactionScope",
        "redaction_strategy": "redactionStrategy",
        "retention_strategy": "retentionStrategy",
        "retention_window_days": "retentionWindowDays",
        "timeouts": "timeouts",
    },
)
class GoogleDialogflowCxSecuritySettingsConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        audio_export_settings: typing.Optional[typing.Union[GoogleDialogflowCxSecuritySettingsAudioExportSettings, typing.Dict[builtins.str, typing.Any]]] = None,
        deidentify_template: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        insights_export_settings: typing.Optional[typing.Union["GoogleDialogflowCxSecuritySettingsInsightsExportSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        inspect_template: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        purge_data_types: typing.Optional[typing.Sequence[builtins.str]] = None,
        redaction_scope: typing.Optional[builtins.str] = None,
        redaction_strategy: typing.Optional[builtins.str] = None,
        retention_strategy: typing.Optional[builtins.str] = None,
        retention_window_days: typing.Optional[jsii.Number] = None,
        timeouts: typing.Optional[typing.Union["GoogleDialogflowCxSecuritySettingsTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param display_name: The human-readable name of the security settings, unique within the location. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_security_settings#display_name GoogleDialogflowCxSecuritySettings#display_name}
        :param location: The location these settings are located in. Settings can only be applied to an agent in the same location. See `Available Regions <https://cloud.google.com/dialogflow/cx/docs/concept/region#avail>`_ for a list of supported locations. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_security_settings#location GoogleDialogflowCxSecuritySettings#location}
        :param audio_export_settings: audio_export_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_security_settings#audio_export_settings GoogleDialogflowCxSecuritySettings#audio_export_settings}
        :param deidentify_template: `DLP <https://cloud.google.com/dlp/docs>`_ deidentify template name. Use this template to define de-identification configuration for the content. If empty, Dialogflow replaces sensitive info with [redacted] text. Note: deidentifyTemplate must be located in the same region as the SecuritySettings. Format: projects//locations//deidentifyTemplates/ OR organizations//locations//deidentifyTemplates/. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_security_settings#deidentify_template GoogleDialogflowCxSecuritySettings#deidentify_template}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_security_settings#id GoogleDialogflowCxSecuritySettings#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param insights_export_settings: insights_export_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_security_settings#insights_export_settings GoogleDialogflowCxSecuritySettings#insights_export_settings}
        :param inspect_template: `DLP <https://cloud.google.com/dlp/docs>`_ inspect template name. Use this template to define inspect base settings. If empty, we use the default DLP inspect config. Note: inspectTemplate must be located in the same region as the SecuritySettings. Format: projects//locations//inspectTemplates/ OR organizations//locations//inspectTemplates/. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_security_settings#inspect_template GoogleDialogflowCxSecuritySettings#inspect_template}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_security_settings#project GoogleDialogflowCxSecuritySettings#project}.
        :param purge_data_types: List of types of data to remove when retention settings triggers purge. Possible values: ["DIALOGFLOW_HISTORY"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_security_settings#purge_data_types GoogleDialogflowCxSecuritySettings#purge_data_types}
        :param redaction_scope: Defines what types of data to redact. If not set, defaults to not redacting any kind of data. - REDACT_DISK_STORAGE: On data to be written to disk or similar devices that are capable of holding data even if power is disconnected. This includes data that are temporarily saved on disk. Possible values: ["REDACT_DISK_STORAGE"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_security_settings#redaction_scope GoogleDialogflowCxSecuritySettings#redaction_scope}
        :param redaction_strategy: Defines how we redact data. If not set, defaults to not redacting. - REDACT_WITH_SERVICE: Call redaction service to clean up the data to be persisted. Possible values: ["REDACT_WITH_SERVICE"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_security_settings#redaction_strategy GoogleDialogflowCxSecuritySettings#redaction_strategy}
        :param retention_strategy: Defines how long we retain persisted data that contains sensitive info. Only one of 'retention_window_days' and 'retention_strategy' may be set. - REMOVE_AFTER_CONVERSATION: Removes data when the conversation ends. If there is no conversation explicitly established, a default conversation ends when the corresponding Dialogflow session ends. Possible values: ["REMOVE_AFTER_CONVERSATION"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_security_settings#retention_strategy GoogleDialogflowCxSecuritySettings#retention_strategy}
        :param retention_window_days: Retains the data for the specified number of days. User must set a value lower than Dialogflow's default 365d TTL (30 days for Agent Assist traffic), higher value will be ignored and use default. Setting a value higher than that has no effect. A missing value or setting to 0 also means we use default TTL. Only one of 'retention_window_days' and 'retention_strategy' may be set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_security_settings#retention_window_days GoogleDialogflowCxSecuritySettings#retention_window_days}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_security_settings#timeouts GoogleDialogflowCxSecuritySettings#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(audio_export_settings, dict):
            audio_export_settings = GoogleDialogflowCxSecuritySettingsAudioExportSettings(**audio_export_settings)
        if isinstance(insights_export_settings, dict):
            insights_export_settings = GoogleDialogflowCxSecuritySettingsInsightsExportSettings(**insights_export_settings)
        if isinstance(timeouts, dict):
            timeouts = GoogleDialogflowCxSecuritySettingsTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__324c262371473bb7117b5e46ce6a723f223c277e04fa9561ab9187bfb2c3ee9c)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument display_name", value=display_name, expected_type=type_hints["display_name"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument audio_export_settings", value=audio_export_settings, expected_type=type_hints["audio_export_settings"])
            check_type(argname="argument deidentify_template", value=deidentify_template, expected_type=type_hints["deidentify_template"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument insights_export_settings", value=insights_export_settings, expected_type=type_hints["insights_export_settings"])
            check_type(argname="argument inspect_template", value=inspect_template, expected_type=type_hints["inspect_template"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument purge_data_types", value=purge_data_types, expected_type=type_hints["purge_data_types"])
            check_type(argname="argument redaction_scope", value=redaction_scope, expected_type=type_hints["redaction_scope"])
            check_type(argname="argument redaction_strategy", value=redaction_strategy, expected_type=type_hints["redaction_strategy"])
            check_type(argname="argument retention_strategy", value=retention_strategy, expected_type=type_hints["retention_strategy"])
            check_type(argname="argument retention_window_days", value=retention_window_days, expected_type=type_hints["retention_window_days"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
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
        if audio_export_settings is not None:
            self._values["audio_export_settings"] = audio_export_settings
        if deidentify_template is not None:
            self._values["deidentify_template"] = deidentify_template
        if id is not None:
            self._values["id"] = id
        if insights_export_settings is not None:
            self._values["insights_export_settings"] = insights_export_settings
        if inspect_template is not None:
            self._values["inspect_template"] = inspect_template
        if project is not None:
            self._values["project"] = project
        if purge_data_types is not None:
            self._values["purge_data_types"] = purge_data_types
        if redaction_scope is not None:
            self._values["redaction_scope"] = redaction_scope
        if redaction_strategy is not None:
            self._values["redaction_strategy"] = redaction_strategy
        if retention_strategy is not None:
            self._values["retention_strategy"] = retention_strategy
        if retention_window_days is not None:
            self._values["retention_window_days"] = retention_window_days
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
    def display_name(self) -> builtins.str:
        '''The human-readable name of the security settings, unique within the location.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_security_settings#display_name GoogleDialogflowCxSecuritySettings#display_name}
        '''
        result = self._values.get("display_name")
        assert result is not None, "Required property 'display_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def location(self) -> builtins.str:
        '''The location these settings are located in.

        Settings can only be applied to an agent in the same location.
        See `Available Regions <https://cloud.google.com/dialogflow/cx/docs/concept/region#avail>`_ for a list of supported locations.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_security_settings#location GoogleDialogflowCxSecuritySettings#location}
        '''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def audio_export_settings(
        self,
    ) -> typing.Optional[GoogleDialogflowCxSecuritySettingsAudioExportSettings]:
        '''audio_export_settings block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_security_settings#audio_export_settings GoogleDialogflowCxSecuritySettings#audio_export_settings}
        '''
        result = self._values.get("audio_export_settings")
        return typing.cast(typing.Optional[GoogleDialogflowCxSecuritySettingsAudioExportSettings], result)

    @builtins.property
    def deidentify_template(self) -> typing.Optional[builtins.str]:
        '''`DLP <https://cloud.google.com/dlp/docs>`_ deidentify template name. Use this template to define de-identification configuration for the content. If empty, Dialogflow replaces sensitive info with [redacted] text. Note: deidentifyTemplate must be located in the same region as the SecuritySettings. Format: projects//locations//deidentifyTemplates/ OR organizations//locations//deidentifyTemplates/.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_security_settings#deidentify_template GoogleDialogflowCxSecuritySettings#deidentify_template}
        '''
        result = self._values.get("deidentify_template")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_security_settings#id GoogleDialogflowCxSecuritySettings#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def insights_export_settings(
        self,
    ) -> typing.Optional["GoogleDialogflowCxSecuritySettingsInsightsExportSettings"]:
        '''insights_export_settings block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_security_settings#insights_export_settings GoogleDialogflowCxSecuritySettings#insights_export_settings}
        '''
        result = self._values.get("insights_export_settings")
        return typing.cast(typing.Optional["GoogleDialogflowCxSecuritySettingsInsightsExportSettings"], result)

    @builtins.property
    def inspect_template(self) -> typing.Optional[builtins.str]:
        '''`DLP <https://cloud.google.com/dlp/docs>`_ inspect template name. Use this template to define inspect base settings. If empty, we use the default DLP inspect config. Note: inspectTemplate must be located in the same region as the SecuritySettings. Format: projects//locations//inspectTemplates/ OR organizations//locations//inspectTemplates/.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_security_settings#inspect_template GoogleDialogflowCxSecuritySettings#inspect_template}
        '''
        result = self._values.get("inspect_template")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_security_settings#project GoogleDialogflowCxSecuritySettings#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def purge_data_types(self) -> typing.Optional[typing.List[builtins.str]]:
        '''List of types of data to remove when retention settings triggers purge. Possible values: ["DIALOGFLOW_HISTORY"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_security_settings#purge_data_types GoogleDialogflowCxSecuritySettings#purge_data_types}
        '''
        result = self._values.get("purge_data_types")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def redaction_scope(self) -> typing.Optional[builtins.str]:
        '''Defines what types of data to redact.

        If not set, defaults to not redacting any kind of data.

        - REDACT_DISK_STORAGE: On data to be written to disk or similar devices that are capable of holding data even if power is disconnected. This includes data that are temporarily saved on disk. Possible values: ["REDACT_DISK_STORAGE"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_security_settings#redaction_scope GoogleDialogflowCxSecuritySettings#redaction_scope}
        '''
        result = self._values.get("redaction_scope")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def redaction_strategy(self) -> typing.Optional[builtins.str]:
        '''Defines how we redact data.

        If not set, defaults to not redacting.

        - REDACT_WITH_SERVICE: Call redaction service to clean up the data to be persisted. Possible values: ["REDACT_WITH_SERVICE"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_security_settings#redaction_strategy GoogleDialogflowCxSecuritySettings#redaction_strategy}
        '''
        result = self._values.get("redaction_strategy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def retention_strategy(self) -> typing.Optional[builtins.str]:
        '''Defines how long we retain persisted data that contains sensitive info.

        Only one of 'retention_window_days' and 'retention_strategy' may be set.

        - REMOVE_AFTER_CONVERSATION: Removes data when the conversation ends. If there is no conversation explicitly established, a default conversation ends when the corresponding Dialogflow session ends. Possible values: ["REMOVE_AFTER_CONVERSATION"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_security_settings#retention_strategy GoogleDialogflowCxSecuritySettings#retention_strategy}
        '''
        result = self._values.get("retention_strategy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def retention_window_days(self) -> typing.Optional[jsii.Number]:
        '''Retains the data for the specified number of days.

        User must set a value lower than Dialogflow's default 365d TTL (30 days for Agent Assist traffic), higher value will be ignored and use default. Setting a value higher than that has no effect. A missing value or setting to 0 also means we use default TTL.
        Only one of 'retention_window_days' and 'retention_strategy' may be set.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_security_settings#retention_window_days GoogleDialogflowCxSecuritySettings#retention_window_days}
        '''
        result = self._values.get("retention_window_days")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["GoogleDialogflowCxSecuritySettingsTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_security_settings#timeouts GoogleDialogflowCxSecuritySettings#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["GoogleDialogflowCxSecuritySettingsTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDialogflowCxSecuritySettingsConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDialogflowCxSecuritySettings.GoogleDialogflowCxSecuritySettingsInsightsExportSettings",
    jsii_struct_bases=[],
    name_mapping={"enable_insights_export": "enableInsightsExport"},
)
class GoogleDialogflowCxSecuritySettingsInsightsExportSettings:
    def __init__(
        self,
        *,
        enable_insights_export: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        '''
        :param enable_insights_export: If enabled, we will automatically exports conversations to Insights and Insights runs its analyzers. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_security_settings#enable_insights_export GoogleDialogflowCxSecuritySettings#enable_insights_export}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bc083fccea9322d8ec269ba6496a353654fad4c8929757e6f98ed58eb9dbd5d2)
            check_type(argname="argument enable_insights_export", value=enable_insights_export, expected_type=type_hints["enable_insights_export"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "enable_insights_export": enable_insights_export,
        }

    @builtins.property
    def enable_insights_export(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''If enabled, we will automatically exports conversations to Insights and Insights runs its analyzers.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_security_settings#enable_insights_export GoogleDialogflowCxSecuritySettings#enable_insights_export}
        '''
        result = self._values.get("enable_insights_export")
        assert result is not None, "Required property 'enable_insights_export' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDialogflowCxSecuritySettingsInsightsExportSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDialogflowCxSecuritySettingsInsightsExportSettingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDialogflowCxSecuritySettings.GoogleDialogflowCxSecuritySettingsInsightsExportSettingsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3e42c0c6fb143c55575c8e23c3028987f584ce763ee08d73c6209f14e89fb17b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="enableInsightsExportInput")
    def enable_insights_export_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enableInsightsExportInput"))

    @builtins.property
    @jsii.member(jsii_name="enableInsightsExport")
    def enable_insights_export(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enableInsightsExport"))

    @enable_insights_export.setter
    def enable_insights_export(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c7d334f065bef49610d81666a0bdcaba2757eac4731abe6628114c2f28d9845d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableInsightsExport", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDialogflowCxSecuritySettingsInsightsExportSettings]:
        return typing.cast(typing.Optional[GoogleDialogflowCxSecuritySettingsInsightsExportSettings], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDialogflowCxSecuritySettingsInsightsExportSettings],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fbaf1c14ace5a4e4f30423be76273012af44c1bdbab7995de0e87fe17f798797)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDialogflowCxSecuritySettings.GoogleDialogflowCxSecuritySettingsTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class GoogleDialogflowCxSecuritySettingsTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_security_settings#create GoogleDialogflowCxSecuritySettings#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_security_settings#delete GoogleDialogflowCxSecuritySettings#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_security_settings#update GoogleDialogflowCxSecuritySettings#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__107c3b4a6514538be09df44b5e757f6ece3d78ebe56d67798fd2a70292d44c93)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_security_settings#create GoogleDialogflowCxSecuritySettings#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_security_settings#delete GoogleDialogflowCxSecuritySettings#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_security_settings#update GoogleDialogflowCxSecuritySettings#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDialogflowCxSecuritySettingsTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDialogflowCxSecuritySettingsTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDialogflowCxSecuritySettings.GoogleDialogflowCxSecuritySettingsTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4b06b3b97947e0ab3f256fdf2488d83d40125724188732c3f6f80dca2a54da66)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d3c85a59abe700dd2161b7ce8e2c608a564515ffd62bf69449d85d1973eebe60)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c73e9befdfb2f3146a4bb2e9d258ec7169b4e97b351a448df099e5764bc3d3cb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0770c042f182f7ce931487b629afebf55cf1706e866c183891f52f955d35c98f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDialogflowCxSecuritySettingsTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDialogflowCxSecuritySettingsTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDialogflowCxSecuritySettingsTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__62475e80baa21b05608277b87142536cc18c935a276e419ab5f418872eaa4ce5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "GoogleDialogflowCxSecuritySettings",
    "GoogleDialogflowCxSecuritySettingsAudioExportSettings",
    "GoogleDialogflowCxSecuritySettingsAudioExportSettingsOutputReference",
    "GoogleDialogflowCxSecuritySettingsConfig",
    "GoogleDialogflowCxSecuritySettingsInsightsExportSettings",
    "GoogleDialogflowCxSecuritySettingsInsightsExportSettingsOutputReference",
    "GoogleDialogflowCxSecuritySettingsTimeouts",
    "GoogleDialogflowCxSecuritySettingsTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__c9a3c160f33d4e840cfb043da32cf70af4867c9f90352146cdabbf8df0d305b9(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    display_name: builtins.str,
    location: builtins.str,
    audio_export_settings: typing.Optional[typing.Union[GoogleDialogflowCxSecuritySettingsAudioExportSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    deidentify_template: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    insights_export_settings: typing.Optional[typing.Union[GoogleDialogflowCxSecuritySettingsInsightsExportSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    inspect_template: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    purge_data_types: typing.Optional[typing.Sequence[builtins.str]] = None,
    redaction_scope: typing.Optional[builtins.str] = None,
    redaction_strategy: typing.Optional[builtins.str] = None,
    retention_strategy: typing.Optional[builtins.str] = None,
    retention_window_days: typing.Optional[jsii.Number] = None,
    timeouts: typing.Optional[typing.Union[GoogleDialogflowCxSecuritySettingsTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__18875c45ecf4ff891c39e35f46b45f338bfa1b2c59d70bc5d44ca069417a7b90(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__880fedb90de11ef9facd4bf8fe5667b70fbd0e2bafda9fb2657f1ae88eebf001(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c89da646eb55252e99a6c5a9fe5e7a6a64b5712894fc70d9404a7734f9f89773(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de07d3a592d95cdd6481f21f93b52d19f889b8aac8a03a30eea9edd68b9caa0f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3442192d146ad0efea8842dab81964af7901f6631bdd6ecab0aefcb431808d9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6df94460d09ecff375c1127d648319e63db6e15107b810a558863ee29ddda6e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__138e33b8ba5c4a06e19f000a6100cedeaa5a2e1eb11a287d5f42a44e04a3d84d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__074bdf668d67152c8d1545aed7d38c2b7ddd40f974f5470f3a635891e09e6515(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6d07c0eb104af4af46f1d850d1cfe973b2b2e1834c26d7dbb69dd474a8e33b9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26324cd259ca0d3c9fc5f24259dca5291ae41fc5132d252eadeb60475dfd1b5c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11be4e7c61a2bb45aa65368b987741d50a34c26f8dcec2fc0f50956fb009433f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d18ba1a355414c02707cd43d91b8e49f70eca58a7cc41a980867c109f07d6331(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c661e3eec872e49bc32dc402fcc223c27141e06f4437541ff705cf3413663c9(
    *,
    audio_export_pattern: typing.Optional[builtins.str] = None,
    audio_format: typing.Optional[builtins.str] = None,
    enable_audio_redaction: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    gcs_bucket: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c28781a9c75e52a2fd396536b648bc122f0176dce341925602ab9edcb969b7cb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__029452f9f37fa85bacf2cdfcec2fde3b993b0f898ec10cba7a973a5c614041b6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eacc5c331b2bf7616ea16383be408b4c067ed90438e54bcc8a8b5b461684323c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34f1497fa50848363d323faa744ef6da19ba5a367442d827eeb58e8820af626a(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7174fe92a4581ed5a75ad43127bede31d520d4f78010c1eb122813abc1597eab(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87ad5ff244edc3e2de69a9238143c53f869050e520740a89075837dc5edf255b(
    value: typing.Optional[GoogleDialogflowCxSecuritySettingsAudioExportSettings],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__324c262371473bb7117b5e46ce6a723f223c277e04fa9561ab9187bfb2c3ee9c(
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
    audio_export_settings: typing.Optional[typing.Union[GoogleDialogflowCxSecuritySettingsAudioExportSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    deidentify_template: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    insights_export_settings: typing.Optional[typing.Union[GoogleDialogflowCxSecuritySettingsInsightsExportSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    inspect_template: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    purge_data_types: typing.Optional[typing.Sequence[builtins.str]] = None,
    redaction_scope: typing.Optional[builtins.str] = None,
    redaction_strategy: typing.Optional[builtins.str] = None,
    retention_strategy: typing.Optional[builtins.str] = None,
    retention_window_days: typing.Optional[jsii.Number] = None,
    timeouts: typing.Optional[typing.Union[GoogleDialogflowCxSecuritySettingsTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc083fccea9322d8ec269ba6496a353654fad4c8929757e6f98ed58eb9dbd5d2(
    *,
    enable_insights_export: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e42c0c6fb143c55575c8e23c3028987f584ce763ee08d73c6209f14e89fb17b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7d334f065bef49610d81666a0bdcaba2757eac4731abe6628114c2f28d9845d(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fbaf1c14ace5a4e4f30423be76273012af44c1bdbab7995de0e87fe17f798797(
    value: typing.Optional[GoogleDialogflowCxSecuritySettingsInsightsExportSettings],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__107c3b4a6514538be09df44b5e757f6ece3d78ebe56d67798fd2a70292d44c93(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b06b3b97947e0ab3f256fdf2488d83d40125724188732c3f6f80dca2a54da66(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3c85a59abe700dd2161b7ce8e2c608a564515ffd62bf69449d85d1973eebe60(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c73e9befdfb2f3146a4bb2e9d258ec7169b4e97b351a448df099e5764bc3d3cb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0770c042f182f7ce931487b629afebf55cf1706e866c183891f52f955d35c98f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62475e80baa21b05608277b87142536cc18c935a276e419ab5f418872eaa4ce5(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDialogflowCxSecuritySettingsTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
