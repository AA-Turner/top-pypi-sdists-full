r'''
# `google_dialogflow_cx_security_settings`

Refer to the Terraform Registry for docs: [`google_dialogflow_cx_security_settings`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_security_settings).
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


class DialogflowCxSecuritySettings(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dialogflowCxSecuritySettings.DialogflowCxSecuritySettings",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_security_settings google_dialogflow_cx_security_settings}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        display_name: builtins.str,
        location: builtins.str,
        audio_export_settings: typing.Optional[typing.Union["DialogflowCxSecuritySettingsAudioExportSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        deidentify_template: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        insights_export_settings: typing.Optional[typing.Union["DialogflowCxSecuritySettingsInsightsExportSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        inspect_template: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        purge_data_types: typing.Optional[typing.Sequence[builtins.str]] = None,
        redaction_scope: typing.Optional[builtins.str] = None,
        redaction_strategy: typing.Optional[builtins.str] = None,
        retention_strategy: typing.Optional[builtins.str] = None,
        retention_window_days: typing.Optional[jsii.Number] = None,
        timeouts: typing.Optional[typing.Union["DialogflowCxSecuritySettingsTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_security_settings google_dialogflow_cx_security_settings} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param display_name: The human-readable name of the security settings, unique within the location. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_security_settings#display_name DialogflowCxSecuritySettings#display_name}
        :param location: The location these settings are located in. Settings can only be applied to an agent in the same location. See `Available Regions <https://cloud.google.com/dialogflow/cx/docs/concept/region#avail>`_ for a list of supported locations. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_security_settings#location DialogflowCxSecuritySettings#location}
        :param audio_export_settings: audio_export_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_security_settings#audio_export_settings DialogflowCxSecuritySettings#audio_export_settings}
        :param deidentify_template: `DLP <https://cloud.google.com/dlp/docs>`_ deidentify template name. Use this template to define de-identification configuration for the content. If empty, Dialogflow replaces sensitive info with [redacted] text. Note: deidentifyTemplate must be located in the same region as the SecuritySettings. Format: projects//locations//deidentifyTemplates/ OR organizations//locations//deidentifyTemplates/. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_security_settings#deidentify_template DialogflowCxSecuritySettings#deidentify_template}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_security_settings#id DialogflowCxSecuritySettings#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param insights_export_settings: insights_export_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_security_settings#insights_export_settings DialogflowCxSecuritySettings#insights_export_settings}
        :param inspect_template: `DLP <https://cloud.google.com/dlp/docs>`_ inspect template name. Use this template to define inspect base settings. If empty, we use the default DLP inspect config. Note: inspectTemplate must be located in the same region as the SecuritySettings. Format: projects//locations//inspectTemplates/ OR organizations//locations//inspectTemplates/. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_security_settings#inspect_template DialogflowCxSecuritySettings#inspect_template}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_security_settings#project DialogflowCxSecuritySettings#project}.
        :param purge_data_types: List of types of data to remove when retention settings triggers purge. Possible values: ["DIALOGFLOW_HISTORY"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_security_settings#purge_data_types DialogflowCxSecuritySettings#purge_data_types}
        :param redaction_scope: Defines what types of data to redact. If not set, defaults to not redacting any kind of data. - REDACT_DISK_STORAGE: On data to be written to disk or similar devices that are capable of holding data even if power is disconnected. This includes data that are temporarily saved on disk. Possible values: ["REDACT_DISK_STORAGE"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_security_settings#redaction_scope DialogflowCxSecuritySettings#redaction_scope}
        :param redaction_strategy: Defines how we redact data. If not set, defaults to not redacting. - REDACT_WITH_SERVICE: Call redaction service to clean up the data to be persisted. Possible values: ["REDACT_WITH_SERVICE"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_security_settings#redaction_strategy DialogflowCxSecuritySettings#redaction_strategy}
        :param retention_strategy: Defines how long we retain persisted data that contains sensitive info. Only one of 'retention_window_days' and 'retention_strategy' may be set. - REMOVE_AFTER_CONVERSATION: Removes data when the conversation ends. If there is no conversation explicitly established, a default conversation ends when the corresponding Dialogflow session ends. Possible values: ["REMOVE_AFTER_CONVERSATION"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_security_settings#retention_strategy DialogflowCxSecuritySettings#retention_strategy}
        :param retention_window_days: Retains the data for the specified number of days. User must set a value lower than Dialogflow's default 365d TTL (30 days for Agent Assist traffic), higher value will be ignored and use default. Setting a value higher than that has no effect. A missing value or setting to 0 also means we use default TTL. Only one of 'retention_window_days' and 'retention_strategy' may be set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_security_settings#retention_window_days DialogflowCxSecuritySettings#retention_window_days}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_security_settings#timeouts DialogflowCxSecuritySettings#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0169e2458c31bcbace4db550b2bd16abfd1296fdf5be1af92fbf0eadc04f9336)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = DialogflowCxSecuritySettingsConfig(
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
        '''Generates CDKTF code for importing a DialogflowCxSecuritySettings resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the DialogflowCxSecuritySettings to import.
        :param import_from_id: The id of the existing DialogflowCxSecuritySettings that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_security_settings#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the DialogflowCxSecuritySettings to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__948d4c7047640a56087832c02d12a60734a890e2374faa5f21f6511c31a33033)
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
        :param audio_export_pattern: Filename pattern for exported audio. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_security_settings#audio_export_pattern DialogflowCxSecuritySettings#audio_export_pattern}
        :param audio_format: File format for exported audio file. Currently only in telephony recordings. - MULAW: G.711 mu-law PCM with 8kHz sample rate. - MP3: MP3 file format. - OGG: OGG Vorbis. Possible values: ["MULAW", "MP3", "OGG"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_security_settings#audio_format DialogflowCxSecuritySettings#audio_format}
        :param enable_audio_redaction: Enable audio redaction if it is true. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_security_settings#enable_audio_redaction DialogflowCxSecuritySettings#enable_audio_redaction}
        :param gcs_bucket: Cloud Storage bucket to export audio record to. Setting this field would grant the Storage Object Creator role to the Dialogflow Service Agent. API caller that tries to modify this field should have the permission of storage.buckets.setIamPolicy. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_security_settings#gcs_bucket DialogflowCxSecuritySettings#gcs_bucket}
        '''
        value = DialogflowCxSecuritySettingsAudioExportSettings(
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
        :param enable_insights_export: If enabled, we will automatically exports conversations to Insights and Insights runs its analyzers. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_security_settings#enable_insights_export DialogflowCxSecuritySettings#enable_insights_export}
        '''
        value = DialogflowCxSecuritySettingsInsightsExportSettings(
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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_security_settings#create DialogflowCxSecuritySettings#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_security_settings#delete DialogflowCxSecuritySettings#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_security_settings#update DialogflowCxSecuritySettings#update}.
        '''
        value = DialogflowCxSecuritySettingsTimeouts(
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
    ) -> "DialogflowCxSecuritySettingsAudioExportSettingsOutputReference":
        return typing.cast("DialogflowCxSecuritySettingsAudioExportSettingsOutputReference", jsii.get(self, "audioExportSettings"))

    @builtins.property
    @jsii.member(jsii_name="insightsExportSettings")
    def insights_export_settings(
        self,
    ) -> "DialogflowCxSecuritySettingsInsightsExportSettingsOutputReference":
        return typing.cast("DialogflowCxSecuritySettingsInsightsExportSettingsOutputReference", jsii.get(self, "insightsExportSettings"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "DialogflowCxSecuritySettingsTimeoutsOutputReference":
        return typing.cast("DialogflowCxSecuritySettingsTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="audioExportSettingsInput")
    def audio_export_settings_input(
        self,
    ) -> typing.Optional["DialogflowCxSecuritySettingsAudioExportSettings"]:
        return typing.cast(typing.Optional["DialogflowCxSecuritySettingsAudioExportSettings"], jsii.get(self, "audioExportSettingsInput"))

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
    ) -> typing.Optional["DialogflowCxSecuritySettingsInsightsExportSettings"]:
        return typing.cast(typing.Optional["DialogflowCxSecuritySettingsInsightsExportSettings"], jsii.get(self, "insightsExportSettingsInput"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "DialogflowCxSecuritySettingsTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "DialogflowCxSecuritySettingsTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="deidentifyTemplate")
    def deidentify_template(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "deidentifyTemplate"))

    @deidentify_template.setter
    def deidentify_template(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bad64b194da5aa8f0387b10933b441cbd2491c38c0fcbd1bc8cdb93c2eda59a6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deidentifyTemplate", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="displayName")
    def display_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "displayName"))

    @display_name.setter
    def display_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ef698632e978591dbe52a1e7a52589c3329ad6e61efbb2abf72ee5fac80931b4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "displayName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c9244a18a2854630851b6577ab2caecec2d61f1ab167f4cb1d8dc2f1eaf0965)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="inspectTemplate")
    def inspect_template(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "inspectTemplate"))

    @inspect_template.setter
    def inspect_template(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d805bf8d8ff8ff70d29d5117e84908309436ce25b4a2325caa5fd3eae89944a3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "inspectTemplate", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1ebb4de8aa25e318d0b3a28ba3bf7125b579780823fff13afd6a6495e7db848a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__486ee88b93ecf3d3d17618671a89b815664da3a27dc5b6a9d4cb8097b64a6337)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="purgeDataTypes")
    def purge_data_types(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "purgeDataTypes"))

    @purge_data_types.setter
    def purge_data_types(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cbbfc9934dc581f5c4b50b61ece6dffa4dc3f5845dc1c52373ed4985c8f55d6c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "purgeDataTypes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="redactionScope")
    def redaction_scope(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "redactionScope"))

    @redaction_scope.setter
    def redaction_scope(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6355bbd935c7dc0eee50715fec206086e9e8dca2a6319dfe03d7fcefcfd2cb63)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "redactionScope", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="redactionStrategy")
    def redaction_strategy(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "redactionStrategy"))

    @redaction_strategy.setter
    def redaction_strategy(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__506d28e948384e35848fc626e581e6b4893a037713044d0a85010b36d22b1792)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "redactionStrategy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="retentionStrategy")
    def retention_strategy(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "retentionStrategy"))

    @retention_strategy.setter
    def retention_strategy(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5a783ec41614185c9ccd46fdbfd6d031104b9aa90a7a074f1dcecc62e1e98466)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "retentionStrategy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="retentionWindowDays")
    def retention_window_days(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "retentionWindowDays"))

    @retention_window_days.setter
    def retention_window_days(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__405e6faddeb2276ce3eac6e4c72c48da37f8cd4fceff1aee3999ec6e1f920241)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "retentionWindowDays", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dialogflowCxSecuritySettings.DialogflowCxSecuritySettingsAudioExportSettings",
    jsii_struct_bases=[],
    name_mapping={
        "audio_export_pattern": "audioExportPattern",
        "audio_format": "audioFormat",
        "enable_audio_redaction": "enableAudioRedaction",
        "gcs_bucket": "gcsBucket",
    },
)
class DialogflowCxSecuritySettingsAudioExportSettings:
    def __init__(
        self,
        *,
        audio_export_pattern: typing.Optional[builtins.str] = None,
        audio_format: typing.Optional[builtins.str] = None,
        enable_audio_redaction: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        gcs_bucket: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param audio_export_pattern: Filename pattern for exported audio. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_security_settings#audio_export_pattern DialogflowCxSecuritySettings#audio_export_pattern}
        :param audio_format: File format for exported audio file. Currently only in telephony recordings. - MULAW: G.711 mu-law PCM with 8kHz sample rate. - MP3: MP3 file format. - OGG: OGG Vorbis. Possible values: ["MULAW", "MP3", "OGG"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_security_settings#audio_format DialogflowCxSecuritySettings#audio_format}
        :param enable_audio_redaction: Enable audio redaction if it is true. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_security_settings#enable_audio_redaction DialogflowCxSecuritySettings#enable_audio_redaction}
        :param gcs_bucket: Cloud Storage bucket to export audio record to. Setting this field would grant the Storage Object Creator role to the Dialogflow Service Agent. API caller that tries to modify this field should have the permission of storage.buckets.setIamPolicy. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_security_settings#gcs_bucket DialogflowCxSecuritySettings#gcs_bucket}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8b93cefe58167b8043fe6ac34e94646a81dcef88535eb1e7bc0b553a9592dac7)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_security_settings#audio_export_pattern DialogflowCxSecuritySettings#audio_export_pattern}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_security_settings#audio_format DialogflowCxSecuritySettings#audio_format}
        '''
        result = self._values.get("audio_format")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enable_audio_redaction(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Enable audio redaction if it is true.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_security_settings#enable_audio_redaction DialogflowCxSecuritySettings#enable_audio_redaction}
        '''
        result = self._values.get("enable_audio_redaction")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def gcs_bucket(self) -> typing.Optional[builtins.str]:
        '''Cloud Storage bucket to export audio record to.

        Setting this field would grant the Storage Object Creator role to the Dialogflow Service Agent. API caller that tries to modify this field should have the permission of storage.buckets.setIamPolicy.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_security_settings#gcs_bucket DialogflowCxSecuritySettings#gcs_bucket}
        '''
        result = self._values.get("gcs_bucket")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DialogflowCxSecuritySettingsAudioExportSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DialogflowCxSecuritySettingsAudioExportSettingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dialogflowCxSecuritySettings.DialogflowCxSecuritySettingsAudioExportSettingsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__45aa4e617d0cd894a524f2e67e5b47df59dad4309a16907b2dc13dd9f524cca9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4cd0c325a708c707b8926a74d40ac02f47b5e9842777652afad38415c2ff1ace)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "audioExportPattern", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="audioFormat")
    def audio_format(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "audioFormat"))

    @audio_format.setter
    def audio_format(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__75cfa1cccaf31bfafb74d581712f252944128a17afbb49da3eac004d7c29d5cb)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ddfec97239932104e5d52fa2570e636daa9fe5899115d9f21d9fdb76ba2f9b55)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableAudioRedaction", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="gcsBucket")
    def gcs_bucket(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "gcsBucket"))

    @gcs_bucket.setter
    def gcs_bucket(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f08ea088bd1cbedf67a2d1d75e207f8b95e3d0103d5d4ec1591ffac33952a60)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "gcsBucket", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DialogflowCxSecuritySettingsAudioExportSettings]:
        return typing.cast(typing.Optional[DialogflowCxSecuritySettingsAudioExportSettings], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DialogflowCxSecuritySettingsAudioExportSettings],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f274dc8d5b88187b3f6000995f507ee8019e9b242424a51b5e02220bd8f29b35)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dialogflowCxSecuritySettings.DialogflowCxSecuritySettingsConfig",
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
class DialogflowCxSecuritySettingsConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        audio_export_settings: typing.Optional[typing.Union[DialogflowCxSecuritySettingsAudioExportSettings, typing.Dict[builtins.str, typing.Any]]] = None,
        deidentify_template: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        insights_export_settings: typing.Optional[typing.Union["DialogflowCxSecuritySettingsInsightsExportSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        inspect_template: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        purge_data_types: typing.Optional[typing.Sequence[builtins.str]] = None,
        redaction_scope: typing.Optional[builtins.str] = None,
        redaction_strategy: typing.Optional[builtins.str] = None,
        retention_strategy: typing.Optional[builtins.str] = None,
        retention_window_days: typing.Optional[jsii.Number] = None,
        timeouts: typing.Optional[typing.Union["DialogflowCxSecuritySettingsTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param display_name: The human-readable name of the security settings, unique within the location. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_security_settings#display_name DialogflowCxSecuritySettings#display_name}
        :param location: The location these settings are located in. Settings can only be applied to an agent in the same location. See `Available Regions <https://cloud.google.com/dialogflow/cx/docs/concept/region#avail>`_ for a list of supported locations. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_security_settings#location DialogflowCxSecuritySettings#location}
        :param audio_export_settings: audio_export_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_security_settings#audio_export_settings DialogflowCxSecuritySettings#audio_export_settings}
        :param deidentify_template: `DLP <https://cloud.google.com/dlp/docs>`_ deidentify template name. Use this template to define de-identification configuration for the content. If empty, Dialogflow replaces sensitive info with [redacted] text. Note: deidentifyTemplate must be located in the same region as the SecuritySettings. Format: projects//locations//deidentifyTemplates/ OR organizations//locations//deidentifyTemplates/. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_security_settings#deidentify_template DialogflowCxSecuritySettings#deidentify_template}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_security_settings#id DialogflowCxSecuritySettings#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param insights_export_settings: insights_export_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_security_settings#insights_export_settings DialogflowCxSecuritySettings#insights_export_settings}
        :param inspect_template: `DLP <https://cloud.google.com/dlp/docs>`_ inspect template name. Use this template to define inspect base settings. If empty, we use the default DLP inspect config. Note: inspectTemplate must be located in the same region as the SecuritySettings. Format: projects//locations//inspectTemplates/ OR organizations//locations//inspectTemplates/. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_security_settings#inspect_template DialogflowCxSecuritySettings#inspect_template}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_security_settings#project DialogflowCxSecuritySettings#project}.
        :param purge_data_types: List of types of data to remove when retention settings triggers purge. Possible values: ["DIALOGFLOW_HISTORY"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_security_settings#purge_data_types DialogflowCxSecuritySettings#purge_data_types}
        :param redaction_scope: Defines what types of data to redact. If not set, defaults to not redacting any kind of data. - REDACT_DISK_STORAGE: On data to be written to disk or similar devices that are capable of holding data even if power is disconnected. This includes data that are temporarily saved on disk. Possible values: ["REDACT_DISK_STORAGE"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_security_settings#redaction_scope DialogflowCxSecuritySettings#redaction_scope}
        :param redaction_strategy: Defines how we redact data. If not set, defaults to not redacting. - REDACT_WITH_SERVICE: Call redaction service to clean up the data to be persisted. Possible values: ["REDACT_WITH_SERVICE"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_security_settings#redaction_strategy DialogflowCxSecuritySettings#redaction_strategy}
        :param retention_strategy: Defines how long we retain persisted data that contains sensitive info. Only one of 'retention_window_days' and 'retention_strategy' may be set. - REMOVE_AFTER_CONVERSATION: Removes data when the conversation ends. If there is no conversation explicitly established, a default conversation ends when the corresponding Dialogflow session ends. Possible values: ["REMOVE_AFTER_CONVERSATION"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_security_settings#retention_strategy DialogflowCxSecuritySettings#retention_strategy}
        :param retention_window_days: Retains the data for the specified number of days. User must set a value lower than Dialogflow's default 365d TTL (30 days for Agent Assist traffic), higher value will be ignored and use default. Setting a value higher than that has no effect. A missing value or setting to 0 also means we use default TTL. Only one of 'retention_window_days' and 'retention_strategy' may be set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_security_settings#retention_window_days DialogflowCxSecuritySettings#retention_window_days}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_security_settings#timeouts DialogflowCxSecuritySettings#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(audio_export_settings, dict):
            audio_export_settings = DialogflowCxSecuritySettingsAudioExportSettings(**audio_export_settings)
        if isinstance(insights_export_settings, dict):
            insights_export_settings = DialogflowCxSecuritySettingsInsightsExportSettings(**insights_export_settings)
        if isinstance(timeouts, dict):
            timeouts = DialogflowCxSecuritySettingsTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__49c4d4b266656edfd642508fa2b8f7be7d47495a191977f1199a5c13062a1670)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_security_settings#display_name DialogflowCxSecuritySettings#display_name}
        '''
        result = self._values.get("display_name")
        assert result is not None, "Required property 'display_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def location(self) -> builtins.str:
        '''The location these settings are located in.

        Settings can only be applied to an agent in the same location.
        See `Available Regions <https://cloud.google.com/dialogflow/cx/docs/concept/region#avail>`_ for a list of supported locations.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_security_settings#location DialogflowCxSecuritySettings#location}
        '''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def audio_export_settings(
        self,
    ) -> typing.Optional[DialogflowCxSecuritySettingsAudioExportSettings]:
        '''audio_export_settings block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_security_settings#audio_export_settings DialogflowCxSecuritySettings#audio_export_settings}
        '''
        result = self._values.get("audio_export_settings")
        return typing.cast(typing.Optional[DialogflowCxSecuritySettingsAudioExportSettings], result)

    @builtins.property
    def deidentify_template(self) -> typing.Optional[builtins.str]:
        '''`DLP <https://cloud.google.com/dlp/docs>`_ deidentify template name. Use this template to define de-identification configuration for the content. If empty, Dialogflow replaces sensitive info with [redacted] text. Note: deidentifyTemplate must be located in the same region as the SecuritySettings. Format: projects//locations//deidentifyTemplates/ OR organizations//locations//deidentifyTemplates/.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_security_settings#deidentify_template DialogflowCxSecuritySettings#deidentify_template}
        '''
        result = self._values.get("deidentify_template")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_security_settings#id DialogflowCxSecuritySettings#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def insights_export_settings(
        self,
    ) -> typing.Optional["DialogflowCxSecuritySettingsInsightsExportSettings"]:
        '''insights_export_settings block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_security_settings#insights_export_settings DialogflowCxSecuritySettings#insights_export_settings}
        '''
        result = self._values.get("insights_export_settings")
        return typing.cast(typing.Optional["DialogflowCxSecuritySettingsInsightsExportSettings"], result)

    @builtins.property
    def inspect_template(self) -> typing.Optional[builtins.str]:
        '''`DLP <https://cloud.google.com/dlp/docs>`_ inspect template name. Use this template to define inspect base settings. If empty, we use the default DLP inspect config. Note: inspectTemplate must be located in the same region as the SecuritySettings. Format: projects//locations//inspectTemplates/ OR organizations//locations//inspectTemplates/.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_security_settings#inspect_template DialogflowCxSecuritySettings#inspect_template}
        '''
        result = self._values.get("inspect_template")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_security_settings#project DialogflowCxSecuritySettings#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def purge_data_types(self) -> typing.Optional[typing.List[builtins.str]]:
        '''List of types of data to remove when retention settings triggers purge. Possible values: ["DIALOGFLOW_HISTORY"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_security_settings#purge_data_types DialogflowCxSecuritySettings#purge_data_types}
        '''
        result = self._values.get("purge_data_types")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def redaction_scope(self) -> typing.Optional[builtins.str]:
        '''Defines what types of data to redact.

        If not set, defaults to not redacting any kind of data.

        - REDACT_DISK_STORAGE: On data to be written to disk or similar devices that are capable of holding data even if power is disconnected. This includes data that are temporarily saved on disk. Possible values: ["REDACT_DISK_STORAGE"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_security_settings#redaction_scope DialogflowCxSecuritySettings#redaction_scope}
        '''
        result = self._values.get("redaction_scope")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def redaction_strategy(self) -> typing.Optional[builtins.str]:
        '''Defines how we redact data.

        If not set, defaults to not redacting.

        - REDACT_WITH_SERVICE: Call redaction service to clean up the data to be persisted. Possible values: ["REDACT_WITH_SERVICE"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_security_settings#redaction_strategy DialogflowCxSecuritySettings#redaction_strategy}
        '''
        result = self._values.get("redaction_strategy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def retention_strategy(self) -> typing.Optional[builtins.str]:
        '''Defines how long we retain persisted data that contains sensitive info.

        Only one of 'retention_window_days' and 'retention_strategy' may be set.

        - REMOVE_AFTER_CONVERSATION: Removes data when the conversation ends. If there is no conversation explicitly established, a default conversation ends when the corresponding Dialogflow session ends. Possible values: ["REMOVE_AFTER_CONVERSATION"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_security_settings#retention_strategy DialogflowCxSecuritySettings#retention_strategy}
        '''
        result = self._values.get("retention_strategy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def retention_window_days(self) -> typing.Optional[jsii.Number]:
        '''Retains the data for the specified number of days.

        User must set a value lower than Dialogflow's default 365d TTL (30 days for Agent Assist traffic), higher value will be ignored and use default. Setting a value higher than that has no effect. A missing value or setting to 0 also means we use default TTL.
        Only one of 'retention_window_days' and 'retention_strategy' may be set.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_security_settings#retention_window_days DialogflowCxSecuritySettings#retention_window_days}
        '''
        result = self._values.get("retention_window_days")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["DialogflowCxSecuritySettingsTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_security_settings#timeouts DialogflowCxSecuritySettings#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["DialogflowCxSecuritySettingsTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DialogflowCxSecuritySettingsConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dialogflowCxSecuritySettings.DialogflowCxSecuritySettingsInsightsExportSettings",
    jsii_struct_bases=[],
    name_mapping={"enable_insights_export": "enableInsightsExport"},
)
class DialogflowCxSecuritySettingsInsightsExportSettings:
    def __init__(
        self,
        *,
        enable_insights_export: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        '''
        :param enable_insights_export: If enabled, we will automatically exports conversations to Insights and Insights runs its analyzers. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_security_settings#enable_insights_export DialogflowCxSecuritySettings#enable_insights_export}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__af4fdbd0504d7c29875f5c36682a4411c81b7d06b939a615da4b5f3dab94ce88)
            check_type(argname="argument enable_insights_export", value=enable_insights_export, expected_type=type_hints["enable_insights_export"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "enable_insights_export": enable_insights_export,
        }

    @builtins.property
    def enable_insights_export(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''If enabled, we will automatically exports conversations to Insights and Insights runs its analyzers.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_security_settings#enable_insights_export DialogflowCxSecuritySettings#enable_insights_export}
        '''
        result = self._values.get("enable_insights_export")
        assert result is not None, "Required property 'enable_insights_export' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DialogflowCxSecuritySettingsInsightsExportSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DialogflowCxSecuritySettingsInsightsExportSettingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dialogflowCxSecuritySettings.DialogflowCxSecuritySettingsInsightsExportSettingsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e6a11c4eb41c3e6e3d381a87e483743713b12f03af8424afcfa4892779815b57)
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
            type_hints = typing.get_type_hints(_typecheckingstub__83b4a7dc31950c780c558462efae187b78a224ee3fd8475594098c1ccac61eb6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableInsightsExport", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DialogflowCxSecuritySettingsInsightsExportSettings]:
        return typing.cast(typing.Optional[DialogflowCxSecuritySettingsInsightsExportSettings], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DialogflowCxSecuritySettingsInsightsExportSettings],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__26f3cf3c0d491644e8c900fedf17d97b33ba97cb9936c9e235ec425f36ae51a3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dialogflowCxSecuritySettings.DialogflowCxSecuritySettingsTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class DialogflowCxSecuritySettingsTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_security_settings#create DialogflowCxSecuritySettings#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_security_settings#delete DialogflowCxSecuritySettings#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_security_settings#update DialogflowCxSecuritySettings#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a2f0621d2b02e9b99780bb2a67aa6fb36abaf945aedba1fc2199c0e775521bf8)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_security_settings#create DialogflowCxSecuritySettings#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_security_settings#delete DialogflowCxSecuritySettings#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_security_settings#update DialogflowCxSecuritySettings#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DialogflowCxSecuritySettingsTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DialogflowCxSecuritySettingsTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dialogflowCxSecuritySettings.DialogflowCxSecuritySettingsTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__415110c05794daa06d064104111f20238494407c7fd2005a3bb3d463b384d8a8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__dc1a7b58c1945ace5fd84be0f54809193644713d66a60f08c5aacea0046bbe0e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__33c80e6d69da2a2b2e3c3724c645ad9686a7517dd447f11a2970b2c21a3ce54b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9498495af49972b30215fac2bf884f821b024b03521f0eb401c3ca363f3b5361)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DialogflowCxSecuritySettingsTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DialogflowCxSecuritySettingsTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DialogflowCxSecuritySettingsTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__600a0d87af9192574a97b56a1d05bc4835207f6666be4edbb3893a69a32daad5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "DialogflowCxSecuritySettings",
    "DialogflowCxSecuritySettingsAudioExportSettings",
    "DialogflowCxSecuritySettingsAudioExportSettingsOutputReference",
    "DialogflowCxSecuritySettingsConfig",
    "DialogflowCxSecuritySettingsInsightsExportSettings",
    "DialogflowCxSecuritySettingsInsightsExportSettingsOutputReference",
    "DialogflowCxSecuritySettingsTimeouts",
    "DialogflowCxSecuritySettingsTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__0169e2458c31bcbace4db550b2bd16abfd1296fdf5be1af92fbf0eadc04f9336(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    display_name: builtins.str,
    location: builtins.str,
    audio_export_settings: typing.Optional[typing.Union[DialogflowCxSecuritySettingsAudioExportSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    deidentify_template: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    insights_export_settings: typing.Optional[typing.Union[DialogflowCxSecuritySettingsInsightsExportSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    inspect_template: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    purge_data_types: typing.Optional[typing.Sequence[builtins.str]] = None,
    redaction_scope: typing.Optional[builtins.str] = None,
    redaction_strategy: typing.Optional[builtins.str] = None,
    retention_strategy: typing.Optional[builtins.str] = None,
    retention_window_days: typing.Optional[jsii.Number] = None,
    timeouts: typing.Optional[typing.Union[DialogflowCxSecuritySettingsTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__948d4c7047640a56087832c02d12a60734a890e2374faa5f21f6511c31a33033(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bad64b194da5aa8f0387b10933b441cbd2491c38c0fcbd1bc8cdb93c2eda59a6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef698632e978591dbe52a1e7a52589c3329ad6e61efbb2abf72ee5fac80931b4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c9244a18a2854630851b6577ab2caecec2d61f1ab167f4cb1d8dc2f1eaf0965(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d805bf8d8ff8ff70d29d5117e84908309436ce25b4a2325caa5fd3eae89944a3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ebb4de8aa25e318d0b3a28ba3bf7125b579780823fff13afd6a6495e7db848a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__486ee88b93ecf3d3d17618671a89b815664da3a27dc5b6a9d4cb8097b64a6337(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cbbfc9934dc581f5c4b50b61ece6dffa4dc3f5845dc1c52373ed4985c8f55d6c(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6355bbd935c7dc0eee50715fec206086e9e8dca2a6319dfe03d7fcefcfd2cb63(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__506d28e948384e35848fc626e581e6b4893a037713044d0a85010b36d22b1792(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a783ec41614185c9ccd46fdbfd6d031104b9aa90a7a074f1dcecc62e1e98466(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__405e6faddeb2276ce3eac6e4c72c48da37f8cd4fceff1aee3999ec6e1f920241(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b93cefe58167b8043fe6ac34e94646a81dcef88535eb1e7bc0b553a9592dac7(
    *,
    audio_export_pattern: typing.Optional[builtins.str] = None,
    audio_format: typing.Optional[builtins.str] = None,
    enable_audio_redaction: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    gcs_bucket: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45aa4e617d0cd894a524f2e67e5b47df59dad4309a16907b2dc13dd9f524cca9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4cd0c325a708c707b8926a74d40ac02f47b5e9842777652afad38415c2ff1ace(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75cfa1cccaf31bfafb74d581712f252944128a17afbb49da3eac004d7c29d5cb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ddfec97239932104e5d52fa2570e636daa9fe5899115d9f21d9fdb76ba2f9b55(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f08ea088bd1cbedf67a2d1d75e207f8b95e3d0103d5d4ec1591ffac33952a60(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f274dc8d5b88187b3f6000995f507ee8019e9b242424a51b5e02220bd8f29b35(
    value: typing.Optional[DialogflowCxSecuritySettingsAudioExportSettings],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__49c4d4b266656edfd642508fa2b8f7be7d47495a191977f1199a5c13062a1670(
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
    audio_export_settings: typing.Optional[typing.Union[DialogflowCxSecuritySettingsAudioExportSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    deidentify_template: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    insights_export_settings: typing.Optional[typing.Union[DialogflowCxSecuritySettingsInsightsExportSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    inspect_template: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    purge_data_types: typing.Optional[typing.Sequence[builtins.str]] = None,
    redaction_scope: typing.Optional[builtins.str] = None,
    redaction_strategy: typing.Optional[builtins.str] = None,
    retention_strategy: typing.Optional[builtins.str] = None,
    retention_window_days: typing.Optional[jsii.Number] = None,
    timeouts: typing.Optional[typing.Union[DialogflowCxSecuritySettingsTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af4fdbd0504d7c29875f5c36682a4411c81b7d06b939a615da4b5f3dab94ce88(
    *,
    enable_insights_export: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6a11c4eb41c3e6e3d381a87e483743713b12f03af8424afcfa4892779815b57(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83b4a7dc31950c780c558462efae187b78a224ee3fd8475594098c1ccac61eb6(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26f3cf3c0d491644e8c900fedf17d97b33ba97cb9936c9e235ec425f36ae51a3(
    value: typing.Optional[DialogflowCxSecuritySettingsInsightsExportSettings],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2f0621d2b02e9b99780bb2a67aa6fb36abaf945aedba1fc2199c0e775521bf8(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__415110c05794daa06d064104111f20238494407c7fd2005a3bb3d463b384d8a8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc1a7b58c1945ace5fd84be0f54809193644713d66a60f08c5aacea0046bbe0e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33c80e6d69da2a2b2e3c3724c645ad9686a7517dd447f11a2970b2c21a3ce54b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9498495af49972b30215fac2bf884f821b024b03521f0eb401c3ca363f3b5361(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__600a0d87af9192574a97b56a1d05bc4835207f6666be4edbb3893a69a32daad5(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DialogflowCxSecuritySettingsTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
