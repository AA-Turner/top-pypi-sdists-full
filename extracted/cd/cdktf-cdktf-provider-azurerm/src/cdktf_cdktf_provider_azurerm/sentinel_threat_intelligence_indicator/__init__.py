r'''
# `azurerm_sentinel_threat_intelligence_indicator`

Refer to the Terraform Registry for docs: [`azurerm_sentinel_threat_intelligence_indicator`](https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_threat_intelligence_indicator).
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


class SentinelThreatIntelligenceIndicator(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.sentinelThreatIntelligenceIndicator.SentinelThreatIntelligenceIndicator",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_threat_intelligence_indicator azurerm_sentinel_threat_intelligence_indicator}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        display_name: builtins.str,
        pattern: builtins.str,
        pattern_type: builtins.str,
        source: builtins.str,
        validate_from_utc: builtins.str,
        workspace_id: builtins.str,
        confidence: typing.Optional[jsii.Number] = None,
        created_by: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        extension: typing.Optional[builtins.str] = None,
        external_reference: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SentinelThreatIntelligenceIndicatorExternalReference", typing.Dict[builtins.str, typing.Any]]]]] = None,
        granular_marking: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SentinelThreatIntelligenceIndicatorGranularMarking", typing.Dict[builtins.str, typing.Any]]]]] = None,
        id: typing.Optional[builtins.str] = None,
        kill_chain_phase: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SentinelThreatIntelligenceIndicatorKillChainPhase", typing.Dict[builtins.str, typing.Any]]]]] = None,
        language: typing.Optional[builtins.str] = None,
        object_marking_refs: typing.Optional[typing.Sequence[builtins.str]] = None,
        pattern_version: typing.Optional[builtins.str] = None,
        revoked: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        tags: typing.Optional[typing.Sequence[builtins.str]] = None,
        threat_types: typing.Optional[typing.Sequence[builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["SentinelThreatIntelligenceIndicatorTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        validate_until_utc: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_threat_intelligence_indicator azurerm_sentinel_threat_intelligence_indicator} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param display_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_threat_intelligence_indicator#display_name SentinelThreatIntelligenceIndicator#display_name}.
        :param pattern: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_threat_intelligence_indicator#pattern SentinelThreatIntelligenceIndicator#pattern}.
        :param pattern_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_threat_intelligence_indicator#pattern_type SentinelThreatIntelligenceIndicator#pattern_type}.
        :param source: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_threat_intelligence_indicator#source SentinelThreatIntelligenceIndicator#source}.
        :param validate_from_utc: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_threat_intelligence_indicator#validate_from_utc SentinelThreatIntelligenceIndicator#validate_from_utc}.
        :param workspace_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_threat_intelligence_indicator#workspace_id SentinelThreatIntelligenceIndicator#workspace_id}.
        :param confidence: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_threat_intelligence_indicator#confidence SentinelThreatIntelligenceIndicator#confidence}.
        :param created_by: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_threat_intelligence_indicator#created_by SentinelThreatIntelligenceIndicator#created_by}.
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_threat_intelligence_indicator#description SentinelThreatIntelligenceIndicator#description}.
        :param extension: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_threat_intelligence_indicator#extension SentinelThreatIntelligenceIndicator#extension}.
        :param external_reference: external_reference block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_threat_intelligence_indicator#external_reference SentinelThreatIntelligenceIndicator#external_reference}
        :param granular_marking: granular_marking block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_threat_intelligence_indicator#granular_marking SentinelThreatIntelligenceIndicator#granular_marking}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_threat_intelligence_indicator#id SentinelThreatIntelligenceIndicator#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param kill_chain_phase: kill_chain_phase block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_threat_intelligence_indicator#kill_chain_phase SentinelThreatIntelligenceIndicator#kill_chain_phase}
        :param language: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_threat_intelligence_indicator#language SentinelThreatIntelligenceIndicator#language}.
        :param object_marking_refs: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_threat_intelligence_indicator#object_marking_refs SentinelThreatIntelligenceIndicator#object_marking_refs}.
        :param pattern_version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_threat_intelligence_indicator#pattern_version SentinelThreatIntelligenceIndicator#pattern_version}.
        :param revoked: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_threat_intelligence_indicator#revoked SentinelThreatIntelligenceIndicator#revoked}.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_threat_intelligence_indicator#tags SentinelThreatIntelligenceIndicator#tags}.
        :param threat_types: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_threat_intelligence_indicator#threat_types SentinelThreatIntelligenceIndicator#threat_types}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_threat_intelligence_indicator#timeouts SentinelThreatIntelligenceIndicator#timeouts}
        :param validate_until_utc: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_threat_intelligence_indicator#validate_until_utc SentinelThreatIntelligenceIndicator#validate_until_utc}.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7817adcd75aa1da35fca88b14e5cc128f08b8ec6a6884a9213dd35d93873dac0)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = SentinelThreatIntelligenceIndicatorConfig(
            display_name=display_name,
            pattern=pattern,
            pattern_type=pattern_type,
            source=source,
            validate_from_utc=validate_from_utc,
            workspace_id=workspace_id,
            confidence=confidence,
            created_by=created_by,
            description=description,
            extension=extension,
            external_reference=external_reference,
            granular_marking=granular_marking,
            id=id,
            kill_chain_phase=kill_chain_phase,
            language=language,
            object_marking_refs=object_marking_refs,
            pattern_version=pattern_version,
            revoked=revoked,
            tags=tags,
            threat_types=threat_types,
            timeouts=timeouts,
            validate_until_utc=validate_until_utc,
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
        '''Generates CDKTF code for importing a SentinelThreatIntelligenceIndicator resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the SentinelThreatIntelligenceIndicator to import.
        :param import_from_id: The id of the existing SentinelThreatIntelligenceIndicator that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_threat_intelligence_indicator#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the SentinelThreatIntelligenceIndicator to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b9a204a8ac1ba71bc9467e51e723164b55c48f478fc0264b7c08a7d8a8cedb0)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putExternalReference")
    def put_external_reference(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SentinelThreatIntelligenceIndicatorExternalReference", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ce7fd512c5f04391b387875b49cdbb62b7857f8a16109d3fecea737c7cdda57)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putExternalReference", [value]))

    @jsii.member(jsii_name="putGranularMarking")
    def put_granular_marking(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SentinelThreatIntelligenceIndicatorGranularMarking", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f50d041b16922ac2df8092307f3708ecfa72b143b999a2c1a886f9dd5a0b2c0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putGranularMarking", [value]))

    @jsii.member(jsii_name="putKillChainPhase")
    def put_kill_chain_phase(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SentinelThreatIntelligenceIndicatorKillChainPhase", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1a4572d52b0dcb29657225f12e9a6c14bee20e3f3bf02c962d292dd579427701)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putKillChainPhase", [value]))

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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_threat_intelligence_indicator#create SentinelThreatIntelligenceIndicator#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_threat_intelligence_indicator#delete SentinelThreatIntelligenceIndicator#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_threat_intelligence_indicator#read SentinelThreatIntelligenceIndicator#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_threat_intelligence_indicator#update SentinelThreatIntelligenceIndicator#update}.
        '''
        value = SentinelThreatIntelligenceIndicatorTimeouts(
            create=create, delete=delete, read=read, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetConfidence")
    def reset_confidence(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConfidence", []))

    @jsii.member(jsii_name="resetCreatedBy")
    def reset_created_by(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCreatedBy", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetExtension")
    def reset_extension(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExtension", []))

    @jsii.member(jsii_name="resetExternalReference")
    def reset_external_reference(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExternalReference", []))

    @jsii.member(jsii_name="resetGranularMarking")
    def reset_granular_marking(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGranularMarking", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetKillChainPhase")
    def reset_kill_chain_phase(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKillChainPhase", []))

    @jsii.member(jsii_name="resetLanguage")
    def reset_language(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLanguage", []))

    @jsii.member(jsii_name="resetObjectMarkingRefs")
    def reset_object_marking_refs(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetObjectMarkingRefs", []))

    @jsii.member(jsii_name="resetPatternVersion")
    def reset_pattern_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPatternVersion", []))

    @jsii.member(jsii_name="resetRevoked")
    def reset_revoked(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRevoked", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

    @jsii.member(jsii_name="resetThreatTypes")
    def reset_threat_types(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetThreatTypes", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

    @jsii.member(jsii_name="resetValidateUntilUtc")
    def reset_validate_until_utc(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetValidateUntilUtc", []))

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
    @jsii.member(jsii_name="createdOn")
    def created_on(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createdOn"))

    @builtins.property
    @jsii.member(jsii_name="defanged")
    def defanged(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "defanged"))

    @builtins.property
    @jsii.member(jsii_name="externalId")
    def external_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "externalId"))

    @builtins.property
    @jsii.member(jsii_name="externalLastUpdatedTimeUtc")
    def external_last_updated_time_utc(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "externalLastUpdatedTimeUtc"))

    @builtins.property
    @jsii.member(jsii_name="externalReference")
    def external_reference(
        self,
    ) -> "SentinelThreatIntelligenceIndicatorExternalReferenceList":
        return typing.cast("SentinelThreatIntelligenceIndicatorExternalReferenceList", jsii.get(self, "externalReference"))

    @builtins.property
    @jsii.member(jsii_name="granularMarking")
    def granular_marking(
        self,
    ) -> "SentinelThreatIntelligenceIndicatorGranularMarkingList":
        return typing.cast("SentinelThreatIntelligenceIndicatorGranularMarkingList", jsii.get(self, "granularMarking"))

    @builtins.property
    @jsii.member(jsii_name="guid")
    def guid(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "guid"))

    @builtins.property
    @jsii.member(jsii_name="indicatorType")
    def indicator_type(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "indicatorType"))

    @builtins.property
    @jsii.member(jsii_name="killChainPhase")
    def kill_chain_phase(
        self,
    ) -> "SentinelThreatIntelligenceIndicatorKillChainPhaseList":
        return typing.cast("SentinelThreatIntelligenceIndicatorKillChainPhaseList", jsii.get(self, "killChainPhase"))

    @builtins.property
    @jsii.member(jsii_name="lastUpdatedTimeUtc")
    def last_updated_time_utc(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "lastUpdatedTimeUtc"))

    @builtins.property
    @jsii.member(jsii_name="parsedPattern")
    def parsed_pattern(self) -> "SentinelThreatIntelligenceIndicatorParsedPatternList":
        return typing.cast("SentinelThreatIntelligenceIndicatorParsedPatternList", jsii.get(self, "parsedPattern"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "SentinelThreatIntelligenceIndicatorTimeoutsOutputReference":
        return typing.cast("SentinelThreatIntelligenceIndicatorTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="confidenceInput")
    def confidence_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "confidenceInput"))

    @builtins.property
    @jsii.member(jsii_name="createdByInput")
    def created_by_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "createdByInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="displayNameInput")
    def display_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "displayNameInput"))

    @builtins.property
    @jsii.member(jsii_name="extensionInput")
    def extension_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "extensionInput"))

    @builtins.property
    @jsii.member(jsii_name="externalReferenceInput")
    def external_reference_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SentinelThreatIntelligenceIndicatorExternalReference"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SentinelThreatIntelligenceIndicatorExternalReference"]]], jsii.get(self, "externalReferenceInput"))

    @builtins.property
    @jsii.member(jsii_name="granularMarkingInput")
    def granular_marking_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SentinelThreatIntelligenceIndicatorGranularMarking"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SentinelThreatIntelligenceIndicatorGranularMarking"]]], jsii.get(self, "granularMarkingInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="killChainPhaseInput")
    def kill_chain_phase_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SentinelThreatIntelligenceIndicatorKillChainPhase"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SentinelThreatIntelligenceIndicatorKillChainPhase"]]], jsii.get(self, "killChainPhaseInput"))

    @builtins.property
    @jsii.member(jsii_name="languageInput")
    def language_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "languageInput"))

    @builtins.property
    @jsii.member(jsii_name="objectMarkingRefsInput")
    def object_marking_refs_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "objectMarkingRefsInput"))

    @builtins.property
    @jsii.member(jsii_name="patternInput")
    def pattern_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "patternInput"))

    @builtins.property
    @jsii.member(jsii_name="patternTypeInput")
    def pattern_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "patternTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="patternVersionInput")
    def pattern_version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "patternVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="revokedInput")
    def revoked_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "revokedInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceInput")
    def source_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sourceInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsInput")
    def tags_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "tagsInput"))

    @builtins.property
    @jsii.member(jsii_name="threatTypesInput")
    def threat_types_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "threatTypesInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "SentinelThreatIntelligenceIndicatorTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "SentinelThreatIntelligenceIndicatorTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="validateFromUtcInput")
    def validate_from_utc_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "validateFromUtcInput"))

    @builtins.property
    @jsii.member(jsii_name="validateUntilUtcInput")
    def validate_until_utc_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "validateUntilUtcInput"))

    @builtins.property
    @jsii.member(jsii_name="workspaceIdInput")
    def workspace_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "workspaceIdInput"))

    @builtins.property
    @jsii.member(jsii_name="confidence")
    def confidence(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "confidence"))

    @confidence.setter
    def confidence(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4701bc4f5395745912e47dd255d6257c21b245832e9caf0d5e8b1ef9c3e90880)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "confidence", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="createdBy")
    def created_by(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createdBy"))

    @created_by.setter
    def created_by(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c861121a0a20a0e6d265819461f3cf5b437e4907e2ab90a70a7eac8e33d5a376)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "createdBy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a0495fb26d2f294b364d75d010f811d35757ea62ee8456a882fd32c6e4035fbb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="displayName")
    def display_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "displayName"))

    @display_name.setter
    def display_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d8179d4562ae5797593b0844e7623d23c0ff3945d9d1a28d6cac105f22ea4901)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "displayName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="extension")
    def extension(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "extension"))

    @extension.setter
    def extension(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fae71b6a877566a7f736cedbe27ebae7497267f5d77ee9bcf08b267aa432c993)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "extension", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3293f95fef3c5368cca7473d0928dd03d4df2ac1dd45d2a886238e7f5a01a9c2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="language")
    def language(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "language"))

    @language.setter
    def language(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__25bc8052d350c09bdc864c2a245a3f88e210bff81f652946e5e30685966e46c6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "language", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="objectMarkingRefs")
    def object_marking_refs(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "objectMarkingRefs"))

    @object_marking_refs.setter
    def object_marking_refs(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5454463a333578130daf5abb2396ec8a6b83373f115d5e18155abd2a0921b19b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "objectMarkingRefs", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="pattern")
    def pattern(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "pattern"))

    @pattern.setter
    def pattern(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__28df4d33fa9e1ef1bbdd4426e0ab860cc1a7991bc3b1b52fcd4f98c74bd12ce5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pattern", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="patternType")
    def pattern_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "patternType"))

    @pattern_type.setter
    def pattern_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__85fc16400becb0b56fdce7d830311424c2461a494674a06279794e560d8e4b26)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "patternType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="patternVersion")
    def pattern_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "patternVersion"))

    @pattern_version.setter
    def pattern_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f9fdfc788645df74708bf8f154f7978cd6dc434e6f368a122c0385dd8e025a98)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "patternVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="revoked")
    def revoked(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "revoked"))

    @revoked.setter
    def revoked(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aacc8150f719efa6bb96583a32e76b0f8faf9b0480290d44bd0a7a763e158f42)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "revoked", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="source")
    def source(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "source"))

    @source.setter
    def source(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__51231cbdf606635a46927c64ece72fdf5c5eae0d433e4ee4df81cb18a9a8b962)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "source", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4486dc58fef018723831cadf6772ee808f20b3e8f9a2f7e6c655e8c85d94bdf6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="threatTypes")
    def threat_types(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "threatTypes"))

    @threat_types.setter
    def threat_types(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1a255f63f93b557b53d7eb5b8c763df70634777d7ce493041d4c0c157256a923)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "threatTypes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="validateFromUtc")
    def validate_from_utc(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "validateFromUtc"))

    @validate_from_utc.setter
    def validate_from_utc(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__57521af187b93a44f5f01acf941705e1cbca038a2431f7c872e821050cc04d0b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "validateFromUtc", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="validateUntilUtc")
    def validate_until_utc(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "validateUntilUtc"))

    @validate_until_utc.setter
    def validate_until_utc(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__24328b419ccebf3f9e2f00f68cc9d7958cbd67ea7cbcb3b90b4e259b916dc2d2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "validateUntilUtc", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="workspaceId")
    def workspace_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "workspaceId"))

    @workspace_id.setter
    def workspace_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__14c3ab419c45eeacde73b071e017f9363ac61e1d4c92c0709e23026cabccc1f5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "workspaceId", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.sentinelThreatIntelligenceIndicator.SentinelThreatIntelligenceIndicatorConfig",
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
        "pattern": "pattern",
        "pattern_type": "patternType",
        "source": "source",
        "validate_from_utc": "validateFromUtc",
        "workspace_id": "workspaceId",
        "confidence": "confidence",
        "created_by": "createdBy",
        "description": "description",
        "extension": "extension",
        "external_reference": "externalReference",
        "granular_marking": "granularMarking",
        "id": "id",
        "kill_chain_phase": "killChainPhase",
        "language": "language",
        "object_marking_refs": "objectMarkingRefs",
        "pattern_version": "patternVersion",
        "revoked": "revoked",
        "tags": "tags",
        "threat_types": "threatTypes",
        "timeouts": "timeouts",
        "validate_until_utc": "validateUntilUtc",
    },
)
class SentinelThreatIntelligenceIndicatorConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        pattern: builtins.str,
        pattern_type: builtins.str,
        source: builtins.str,
        validate_from_utc: builtins.str,
        workspace_id: builtins.str,
        confidence: typing.Optional[jsii.Number] = None,
        created_by: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        extension: typing.Optional[builtins.str] = None,
        external_reference: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SentinelThreatIntelligenceIndicatorExternalReference", typing.Dict[builtins.str, typing.Any]]]]] = None,
        granular_marking: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SentinelThreatIntelligenceIndicatorGranularMarking", typing.Dict[builtins.str, typing.Any]]]]] = None,
        id: typing.Optional[builtins.str] = None,
        kill_chain_phase: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SentinelThreatIntelligenceIndicatorKillChainPhase", typing.Dict[builtins.str, typing.Any]]]]] = None,
        language: typing.Optional[builtins.str] = None,
        object_marking_refs: typing.Optional[typing.Sequence[builtins.str]] = None,
        pattern_version: typing.Optional[builtins.str] = None,
        revoked: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        tags: typing.Optional[typing.Sequence[builtins.str]] = None,
        threat_types: typing.Optional[typing.Sequence[builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["SentinelThreatIntelligenceIndicatorTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        validate_until_utc: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param display_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_threat_intelligence_indicator#display_name SentinelThreatIntelligenceIndicator#display_name}.
        :param pattern: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_threat_intelligence_indicator#pattern SentinelThreatIntelligenceIndicator#pattern}.
        :param pattern_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_threat_intelligence_indicator#pattern_type SentinelThreatIntelligenceIndicator#pattern_type}.
        :param source: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_threat_intelligence_indicator#source SentinelThreatIntelligenceIndicator#source}.
        :param validate_from_utc: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_threat_intelligence_indicator#validate_from_utc SentinelThreatIntelligenceIndicator#validate_from_utc}.
        :param workspace_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_threat_intelligence_indicator#workspace_id SentinelThreatIntelligenceIndicator#workspace_id}.
        :param confidence: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_threat_intelligence_indicator#confidence SentinelThreatIntelligenceIndicator#confidence}.
        :param created_by: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_threat_intelligence_indicator#created_by SentinelThreatIntelligenceIndicator#created_by}.
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_threat_intelligence_indicator#description SentinelThreatIntelligenceIndicator#description}.
        :param extension: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_threat_intelligence_indicator#extension SentinelThreatIntelligenceIndicator#extension}.
        :param external_reference: external_reference block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_threat_intelligence_indicator#external_reference SentinelThreatIntelligenceIndicator#external_reference}
        :param granular_marking: granular_marking block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_threat_intelligence_indicator#granular_marking SentinelThreatIntelligenceIndicator#granular_marking}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_threat_intelligence_indicator#id SentinelThreatIntelligenceIndicator#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param kill_chain_phase: kill_chain_phase block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_threat_intelligence_indicator#kill_chain_phase SentinelThreatIntelligenceIndicator#kill_chain_phase}
        :param language: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_threat_intelligence_indicator#language SentinelThreatIntelligenceIndicator#language}.
        :param object_marking_refs: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_threat_intelligence_indicator#object_marking_refs SentinelThreatIntelligenceIndicator#object_marking_refs}.
        :param pattern_version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_threat_intelligence_indicator#pattern_version SentinelThreatIntelligenceIndicator#pattern_version}.
        :param revoked: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_threat_intelligence_indicator#revoked SentinelThreatIntelligenceIndicator#revoked}.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_threat_intelligence_indicator#tags SentinelThreatIntelligenceIndicator#tags}.
        :param threat_types: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_threat_intelligence_indicator#threat_types SentinelThreatIntelligenceIndicator#threat_types}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_threat_intelligence_indicator#timeouts SentinelThreatIntelligenceIndicator#timeouts}
        :param validate_until_utc: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_threat_intelligence_indicator#validate_until_utc SentinelThreatIntelligenceIndicator#validate_until_utc}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(timeouts, dict):
            timeouts = SentinelThreatIntelligenceIndicatorTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__845ca128ec8aad545d3fddb209929a1c49a2f435c44c66882c0a749bf838bffb)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument display_name", value=display_name, expected_type=type_hints["display_name"])
            check_type(argname="argument pattern", value=pattern, expected_type=type_hints["pattern"])
            check_type(argname="argument pattern_type", value=pattern_type, expected_type=type_hints["pattern_type"])
            check_type(argname="argument source", value=source, expected_type=type_hints["source"])
            check_type(argname="argument validate_from_utc", value=validate_from_utc, expected_type=type_hints["validate_from_utc"])
            check_type(argname="argument workspace_id", value=workspace_id, expected_type=type_hints["workspace_id"])
            check_type(argname="argument confidence", value=confidence, expected_type=type_hints["confidence"])
            check_type(argname="argument created_by", value=created_by, expected_type=type_hints["created_by"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument extension", value=extension, expected_type=type_hints["extension"])
            check_type(argname="argument external_reference", value=external_reference, expected_type=type_hints["external_reference"])
            check_type(argname="argument granular_marking", value=granular_marking, expected_type=type_hints["granular_marking"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument kill_chain_phase", value=kill_chain_phase, expected_type=type_hints["kill_chain_phase"])
            check_type(argname="argument language", value=language, expected_type=type_hints["language"])
            check_type(argname="argument object_marking_refs", value=object_marking_refs, expected_type=type_hints["object_marking_refs"])
            check_type(argname="argument pattern_version", value=pattern_version, expected_type=type_hints["pattern_version"])
            check_type(argname="argument revoked", value=revoked, expected_type=type_hints["revoked"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument threat_types", value=threat_types, expected_type=type_hints["threat_types"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
            check_type(argname="argument validate_until_utc", value=validate_until_utc, expected_type=type_hints["validate_until_utc"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "display_name": display_name,
            "pattern": pattern,
            "pattern_type": pattern_type,
            "source": source,
            "validate_from_utc": validate_from_utc,
            "workspace_id": workspace_id,
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
        if confidence is not None:
            self._values["confidence"] = confidence
        if created_by is not None:
            self._values["created_by"] = created_by
        if description is not None:
            self._values["description"] = description
        if extension is not None:
            self._values["extension"] = extension
        if external_reference is not None:
            self._values["external_reference"] = external_reference
        if granular_marking is not None:
            self._values["granular_marking"] = granular_marking
        if id is not None:
            self._values["id"] = id
        if kill_chain_phase is not None:
            self._values["kill_chain_phase"] = kill_chain_phase
        if language is not None:
            self._values["language"] = language
        if object_marking_refs is not None:
            self._values["object_marking_refs"] = object_marking_refs
        if pattern_version is not None:
            self._values["pattern_version"] = pattern_version
        if revoked is not None:
            self._values["revoked"] = revoked
        if tags is not None:
            self._values["tags"] = tags
        if threat_types is not None:
            self._values["threat_types"] = threat_types
        if timeouts is not None:
            self._values["timeouts"] = timeouts
        if validate_until_utc is not None:
            self._values["validate_until_utc"] = validate_until_utc

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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_threat_intelligence_indicator#display_name SentinelThreatIntelligenceIndicator#display_name}.'''
        result = self._values.get("display_name")
        assert result is not None, "Required property 'display_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def pattern(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_threat_intelligence_indicator#pattern SentinelThreatIntelligenceIndicator#pattern}.'''
        result = self._values.get("pattern")
        assert result is not None, "Required property 'pattern' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def pattern_type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_threat_intelligence_indicator#pattern_type SentinelThreatIntelligenceIndicator#pattern_type}.'''
        result = self._values.get("pattern_type")
        assert result is not None, "Required property 'pattern_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def source(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_threat_intelligence_indicator#source SentinelThreatIntelligenceIndicator#source}.'''
        result = self._values.get("source")
        assert result is not None, "Required property 'source' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def validate_from_utc(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_threat_intelligence_indicator#validate_from_utc SentinelThreatIntelligenceIndicator#validate_from_utc}.'''
        result = self._values.get("validate_from_utc")
        assert result is not None, "Required property 'validate_from_utc' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def workspace_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_threat_intelligence_indicator#workspace_id SentinelThreatIntelligenceIndicator#workspace_id}.'''
        result = self._values.get("workspace_id")
        assert result is not None, "Required property 'workspace_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def confidence(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_threat_intelligence_indicator#confidence SentinelThreatIntelligenceIndicator#confidence}.'''
        result = self._values.get("confidence")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def created_by(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_threat_intelligence_indicator#created_by SentinelThreatIntelligenceIndicator#created_by}.'''
        result = self._values.get("created_by")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_threat_intelligence_indicator#description SentinelThreatIntelligenceIndicator#description}.'''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def extension(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_threat_intelligence_indicator#extension SentinelThreatIntelligenceIndicator#extension}.'''
        result = self._values.get("extension")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def external_reference(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SentinelThreatIntelligenceIndicatorExternalReference"]]]:
        '''external_reference block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_threat_intelligence_indicator#external_reference SentinelThreatIntelligenceIndicator#external_reference}
        '''
        result = self._values.get("external_reference")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SentinelThreatIntelligenceIndicatorExternalReference"]]], result)

    @builtins.property
    def granular_marking(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SentinelThreatIntelligenceIndicatorGranularMarking"]]]:
        '''granular_marking block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_threat_intelligence_indicator#granular_marking SentinelThreatIntelligenceIndicator#granular_marking}
        '''
        result = self._values.get("granular_marking")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SentinelThreatIntelligenceIndicatorGranularMarking"]]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_threat_intelligence_indicator#id SentinelThreatIntelligenceIndicator#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kill_chain_phase(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SentinelThreatIntelligenceIndicatorKillChainPhase"]]]:
        '''kill_chain_phase block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_threat_intelligence_indicator#kill_chain_phase SentinelThreatIntelligenceIndicator#kill_chain_phase}
        '''
        result = self._values.get("kill_chain_phase")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SentinelThreatIntelligenceIndicatorKillChainPhase"]]], result)

    @builtins.property
    def language(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_threat_intelligence_indicator#language SentinelThreatIntelligenceIndicator#language}.'''
        result = self._values.get("language")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def object_marking_refs(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_threat_intelligence_indicator#object_marking_refs SentinelThreatIntelligenceIndicator#object_marking_refs}.'''
        result = self._values.get("object_marking_refs")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def pattern_version(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_threat_intelligence_indicator#pattern_version SentinelThreatIntelligenceIndicator#pattern_version}.'''
        result = self._values.get("pattern_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def revoked(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_threat_intelligence_indicator#revoked SentinelThreatIntelligenceIndicator#revoked}.'''
        result = self._values.get("revoked")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_threat_intelligence_indicator#tags SentinelThreatIntelligenceIndicator#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def threat_types(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_threat_intelligence_indicator#threat_types SentinelThreatIntelligenceIndicator#threat_types}.'''
        result = self._values.get("threat_types")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def timeouts(
        self,
    ) -> typing.Optional["SentinelThreatIntelligenceIndicatorTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_threat_intelligence_indicator#timeouts SentinelThreatIntelligenceIndicator#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["SentinelThreatIntelligenceIndicatorTimeouts"], result)

    @builtins.property
    def validate_until_utc(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_threat_intelligence_indicator#validate_until_utc SentinelThreatIntelligenceIndicator#validate_until_utc}.'''
        result = self._values.get("validate_until_utc")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SentinelThreatIntelligenceIndicatorConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.sentinelThreatIntelligenceIndicator.SentinelThreatIntelligenceIndicatorExternalReference",
    jsii_struct_bases=[],
    name_mapping={
        "description": "description",
        "hashes": "hashes",
        "source_name": "sourceName",
        "url": "url",
    },
)
class SentinelThreatIntelligenceIndicatorExternalReference:
    def __init__(
        self,
        *,
        description: typing.Optional[builtins.str] = None,
        hashes: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        source_name: typing.Optional[builtins.str] = None,
        url: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_threat_intelligence_indicator#description SentinelThreatIntelligenceIndicator#description}.
        :param hashes: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_threat_intelligence_indicator#hashes SentinelThreatIntelligenceIndicator#hashes}.
        :param source_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_threat_intelligence_indicator#source_name SentinelThreatIntelligenceIndicator#source_name}.
        :param url: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_threat_intelligence_indicator#url SentinelThreatIntelligenceIndicator#url}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__24ecb05e05f5cf9d0d0503e6c583bf811c955e6cbab66534fb5fd023a8cda499)
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument hashes", value=hashes, expected_type=type_hints["hashes"])
            check_type(argname="argument source_name", value=source_name, expected_type=type_hints["source_name"])
            check_type(argname="argument url", value=url, expected_type=type_hints["url"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if description is not None:
            self._values["description"] = description
        if hashes is not None:
            self._values["hashes"] = hashes
        if source_name is not None:
            self._values["source_name"] = source_name
        if url is not None:
            self._values["url"] = url

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_threat_intelligence_indicator#description SentinelThreatIntelligenceIndicator#description}.'''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def hashes(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_threat_intelligence_indicator#hashes SentinelThreatIntelligenceIndicator#hashes}.'''
        result = self._values.get("hashes")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def source_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_threat_intelligence_indicator#source_name SentinelThreatIntelligenceIndicator#source_name}.'''
        result = self._values.get("source_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def url(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_threat_intelligence_indicator#url SentinelThreatIntelligenceIndicator#url}.'''
        result = self._values.get("url")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SentinelThreatIntelligenceIndicatorExternalReference(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SentinelThreatIntelligenceIndicatorExternalReferenceList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.sentinelThreatIntelligenceIndicator.SentinelThreatIntelligenceIndicatorExternalReferenceList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__193c2db83a5440460e7919c800579e087fd69b2286f8aacd5274848b73a5374e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "SentinelThreatIntelligenceIndicatorExternalReferenceOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6af0470ce63fdffc3176e9fe7883a5a4e203d5aba7ac8cbea91572a972f5a170)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("SentinelThreatIntelligenceIndicatorExternalReferenceOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__44358fd054671ec74f5c7ae104c227dc011df976762e19a209f70c49317bb309)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8166b9794d26e137ec703929ee170430a9a6d1419e63a75ac8e53bdf5170a424)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6fa16e1901277a9f5b541f32088b42790a14f890b8d119f522096bbabed61d50)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SentinelThreatIntelligenceIndicatorExternalReference]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SentinelThreatIntelligenceIndicatorExternalReference]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SentinelThreatIntelligenceIndicatorExternalReference]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7fa7e305dc6183026592940d12610942eb31847039335418220cf89e8ed03d95)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class SentinelThreatIntelligenceIndicatorExternalReferenceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.sentinelThreatIntelligenceIndicator.SentinelThreatIntelligenceIndicatorExternalReferenceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__962d58d40d1e8f2c9fe9fbf28a37bd76e63388a0d1a417b676f4f08ec8dd2d30)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetHashes")
    def reset_hashes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHashes", []))

    @jsii.member(jsii_name="resetSourceName")
    def reset_source_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSourceName", []))

    @jsii.member(jsii_name="resetUrl")
    def reset_url(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUrl", []))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="hashesInput")
    def hashes_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "hashesInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceNameInput")
    def source_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sourceNameInput"))

    @builtins.property
    @jsii.member(jsii_name="urlInput")
    def url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "urlInput"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a6a32232bdf700bd598794619b5ad5971fcf88063d1e730d58781789b3b6ce3d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="hashes")
    def hashes(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "hashes"))

    @hashes.setter
    def hashes(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__55abe5c5a04127ee33a77fcd9063071e17564be923e99067b1c626b8dc2fcb4d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hashes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sourceName")
    def source_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sourceName"))

    @source_name.setter
    def source_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e36d9c31e04abce089fa7f214765e192badf375ad53c518816bcbe0e312e7d4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sourceName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="url")
    def url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "url"))

    @url.setter
    def url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__31e29f5679d19ba5d08cf201662a7fc823e57939b1ea1f4d9da5072f2fc36b6e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "url", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SentinelThreatIntelligenceIndicatorExternalReference]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SentinelThreatIntelligenceIndicatorExternalReference]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SentinelThreatIntelligenceIndicatorExternalReference]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__25670fc4740facd5b36689302dd21659b0033b439418bc0b7eca307c155ab93d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.sentinelThreatIntelligenceIndicator.SentinelThreatIntelligenceIndicatorGranularMarking",
    jsii_struct_bases=[],
    name_mapping={
        "language": "language",
        "marking_ref": "markingRef",
        "selectors": "selectors",
    },
)
class SentinelThreatIntelligenceIndicatorGranularMarking:
    def __init__(
        self,
        *,
        language: typing.Optional[builtins.str] = None,
        marking_ref: typing.Optional[builtins.str] = None,
        selectors: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param language: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_threat_intelligence_indicator#language SentinelThreatIntelligenceIndicator#language}.
        :param marking_ref: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_threat_intelligence_indicator#marking_ref SentinelThreatIntelligenceIndicator#marking_ref}.
        :param selectors: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_threat_intelligence_indicator#selectors SentinelThreatIntelligenceIndicator#selectors}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9719f58939752f61ccf7fbdbafbb1ac5c0665406ec70f73715ec9f171c0c6858)
            check_type(argname="argument language", value=language, expected_type=type_hints["language"])
            check_type(argname="argument marking_ref", value=marking_ref, expected_type=type_hints["marking_ref"])
            check_type(argname="argument selectors", value=selectors, expected_type=type_hints["selectors"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if language is not None:
            self._values["language"] = language
        if marking_ref is not None:
            self._values["marking_ref"] = marking_ref
        if selectors is not None:
            self._values["selectors"] = selectors

    @builtins.property
    def language(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_threat_intelligence_indicator#language SentinelThreatIntelligenceIndicator#language}.'''
        result = self._values.get("language")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def marking_ref(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_threat_intelligence_indicator#marking_ref SentinelThreatIntelligenceIndicator#marking_ref}.'''
        result = self._values.get("marking_ref")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def selectors(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_threat_intelligence_indicator#selectors SentinelThreatIntelligenceIndicator#selectors}.'''
        result = self._values.get("selectors")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SentinelThreatIntelligenceIndicatorGranularMarking(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SentinelThreatIntelligenceIndicatorGranularMarkingList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.sentinelThreatIntelligenceIndicator.SentinelThreatIntelligenceIndicatorGranularMarkingList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1cda6e961189928ffb61f6d521659fa4a67a5f70b4e4c88bdfd1f4c9a129f58b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "SentinelThreatIntelligenceIndicatorGranularMarkingOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f8bcca1db1b96208a51855d86bb20075368ec6f697664eb082c08d8dce98935)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("SentinelThreatIntelligenceIndicatorGranularMarkingOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1296feb9b19ec64d382ca36a99a60d38d2e30b6a87b13f877ad90a4c2d52730c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e355035fb7224591c50a7f0f0d5963da82d3a1fa13f8f1f164f5e16e58619946)
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
            type_hints = typing.get_type_hints(_typecheckingstub__45b5a75196a80fee8f680b46c96135308af3ccfc8553e325b5c390f6829978fe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SentinelThreatIntelligenceIndicatorGranularMarking]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SentinelThreatIntelligenceIndicatorGranularMarking]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SentinelThreatIntelligenceIndicatorGranularMarking]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d3f533379a07c1cc823a5f83d7c136c75bf12b20afa64386408f240aa26a7e65)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class SentinelThreatIntelligenceIndicatorGranularMarkingOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.sentinelThreatIntelligenceIndicator.SentinelThreatIntelligenceIndicatorGranularMarkingOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d73b75359d6cb173d068dbb1fabca240b46b52131f1ee544b2088093e9742f1d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetLanguage")
    def reset_language(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLanguage", []))

    @jsii.member(jsii_name="resetMarkingRef")
    def reset_marking_ref(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMarkingRef", []))

    @jsii.member(jsii_name="resetSelectors")
    def reset_selectors(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSelectors", []))

    @builtins.property
    @jsii.member(jsii_name="languageInput")
    def language_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "languageInput"))

    @builtins.property
    @jsii.member(jsii_name="markingRefInput")
    def marking_ref_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "markingRefInput"))

    @builtins.property
    @jsii.member(jsii_name="selectorsInput")
    def selectors_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "selectorsInput"))

    @builtins.property
    @jsii.member(jsii_name="language")
    def language(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "language"))

    @language.setter
    def language(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e84bd61d3cf401ffb0506370f8b29d40b16ae77a61b478725b2579108a82a21)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "language", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="markingRef")
    def marking_ref(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "markingRef"))

    @marking_ref.setter
    def marking_ref(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8842692ae0e6119ca2f1bf8dd667c05657546253c869493cd18dc60e63a3b1fc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "markingRef", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="selectors")
    def selectors(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "selectors"))

    @selectors.setter
    def selectors(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7cad1d9324083666fdeb48bec08d75b23f82e161ca2c5839c86d5fe4d397e08e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "selectors", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SentinelThreatIntelligenceIndicatorGranularMarking]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SentinelThreatIntelligenceIndicatorGranularMarking]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SentinelThreatIntelligenceIndicatorGranularMarking]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f73b72e4f290bec1eb18068917387b9c160d9230d6ff71c360204696318518bf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.sentinelThreatIntelligenceIndicator.SentinelThreatIntelligenceIndicatorKillChainPhase",
    jsii_struct_bases=[],
    name_mapping={"name": "name"},
)
class SentinelThreatIntelligenceIndicatorKillChainPhase:
    def __init__(self, *, name: typing.Optional[builtins.str] = None) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_threat_intelligence_indicator#name SentinelThreatIntelligenceIndicator#name}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0e9f5492d25458ea2af1e5d5b7a05ba17532ef8139f19461f2f078b68f0609b8)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if name is not None:
            self._values["name"] = name

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_threat_intelligence_indicator#name SentinelThreatIntelligenceIndicator#name}.'''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SentinelThreatIntelligenceIndicatorKillChainPhase(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SentinelThreatIntelligenceIndicatorKillChainPhaseList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.sentinelThreatIntelligenceIndicator.SentinelThreatIntelligenceIndicatorKillChainPhaseList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__52db5bb53c2864e4b496adabe43ed1380f923987a69b15a1cdc80c991c97bce6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "SentinelThreatIntelligenceIndicatorKillChainPhaseOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f16460df7edc1446e04ad806ca59991cecb72286ff8e6cbf99b2aa4450660a4c)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("SentinelThreatIntelligenceIndicatorKillChainPhaseOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9029ba47a07f743e3267bdff3f1da7a7a7b750faab0da19b0dadb43deb0f3f33)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9d3265ae50e6a60a69ad123a10be9f4c29e610ac885acf085a5ec20d9be007a9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__792d1c0023d0b1363d90ff37e4a17795b4b36a3d418e6b6968ec35d384c6e791)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SentinelThreatIntelligenceIndicatorKillChainPhase]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SentinelThreatIntelligenceIndicatorKillChainPhase]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SentinelThreatIntelligenceIndicatorKillChainPhase]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d31357c803a1b2ea861704330ff1ebde1d75c381f93a64782b0261cf7be74392)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class SentinelThreatIntelligenceIndicatorKillChainPhaseOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.sentinelThreatIntelligenceIndicator.SentinelThreatIntelligenceIndicatorKillChainPhaseOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f1109fb2ade460f72b88406830f0b3d746cb32b83bb8e8e49cfe0dc3443fafc6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__32b1f4e1d7243bf6a9b63c2f3fe93e6b6883153e7b4bed9fdb58a793808c7237)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SentinelThreatIntelligenceIndicatorKillChainPhase]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SentinelThreatIntelligenceIndicatorKillChainPhase]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SentinelThreatIntelligenceIndicatorKillChainPhase]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d48cd621d8e5f8cc434a24a764c0c25629797e360b777831c94e7f26b57be53)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.sentinelThreatIntelligenceIndicator.SentinelThreatIntelligenceIndicatorParsedPattern",
    jsii_struct_bases=[],
    name_mapping={},
)
class SentinelThreatIntelligenceIndicatorParsedPattern:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SentinelThreatIntelligenceIndicatorParsedPattern(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SentinelThreatIntelligenceIndicatorParsedPatternList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.sentinelThreatIntelligenceIndicator.SentinelThreatIntelligenceIndicatorParsedPatternList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bed8e28de4c3f9c6bfc3a81bcb969ed38ffd8abe0b60a19f8069316ae5836454)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "SentinelThreatIntelligenceIndicatorParsedPatternOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f50bf621fa2090791bff6b922222762dcc6e183f180f06180dc9cc8ab7440599)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("SentinelThreatIntelligenceIndicatorParsedPatternOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d882a123bb13392074c6e390f6efcdb7622aa0744d8243c4551c798435dc300)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9a8e1f34894f9e05e410438bed3f8c64c1e4686aad9ce77215dfd48cea64e7bc)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f2352b9418550de134a0478eca8f2116c7ea9b0eb5b1f2df40e4c4a52ee335ee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class SentinelThreatIntelligenceIndicatorParsedPatternOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.sentinelThreatIntelligenceIndicator.SentinelThreatIntelligenceIndicatorParsedPatternOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4e6f56de7fa33363507610f29b461c56467c80b1c64eca108b13a94198d75992)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="patternTypeKey")
    def pattern_type_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "patternTypeKey"))

    @builtins.property
    @jsii.member(jsii_name="patternTypeValues")
    def pattern_type_values(
        self,
    ) -> "SentinelThreatIntelligenceIndicatorParsedPatternPatternTypeValuesList":
        return typing.cast("SentinelThreatIntelligenceIndicatorParsedPatternPatternTypeValuesList", jsii.get(self, "patternTypeValues"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[SentinelThreatIntelligenceIndicatorParsedPattern]:
        return typing.cast(typing.Optional[SentinelThreatIntelligenceIndicatorParsedPattern], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SentinelThreatIntelligenceIndicatorParsedPattern],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__66a3f1b7bf44e0210fc80493374786ddd06596988d7e048f4ea76006a300e62f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.sentinelThreatIntelligenceIndicator.SentinelThreatIntelligenceIndicatorParsedPatternPatternTypeValues",
    jsii_struct_bases=[],
    name_mapping={},
)
class SentinelThreatIntelligenceIndicatorParsedPatternPatternTypeValues:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SentinelThreatIntelligenceIndicatorParsedPatternPatternTypeValues(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SentinelThreatIntelligenceIndicatorParsedPatternPatternTypeValuesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.sentinelThreatIntelligenceIndicator.SentinelThreatIntelligenceIndicatorParsedPatternPatternTypeValuesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a16d44bf7b814fbd0ce244f279ff3e7d2a9cf8f5996f8cccf1563d35793b7c6c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "SentinelThreatIntelligenceIndicatorParsedPatternPatternTypeValuesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__30f477e4cdcf5ae6ade730f19e291cc38ad56c1b575027be18a2b461eeac618f)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("SentinelThreatIntelligenceIndicatorParsedPatternPatternTypeValuesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__94992d3c477bafe9ce81d2bfb07d873d86758519f30e95b45198c49931fa8a1c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8f959d0adfd380a57f95bb2c62ef4dd79eccdcec45415984a655a4aab2d1c26d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a46e82696a22e9959d065d553e243366cfc2c7f5fd5be2bfbb9bb3afcc4e0a77)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class SentinelThreatIntelligenceIndicatorParsedPatternPatternTypeValuesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.sentinelThreatIntelligenceIndicator.SentinelThreatIntelligenceIndicatorParsedPatternPatternTypeValuesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9cd8014e2c4831390aaee3f72cd8091a46ab4fa727a18d807cb69ef0f7906eb3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @builtins.property
    @jsii.member(jsii_name="valueType")
    def value_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "valueType"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[SentinelThreatIntelligenceIndicatorParsedPatternPatternTypeValues]:
        return typing.cast(typing.Optional[SentinelThreatIntelligenceIndicatorParsedPatternPatternTypeValues], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SentinelThreatIntelligenceIndicatorParsedPatternPatternTypeValues],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__694607ce7173eda9012102469c6cfb1627fd606bdd6be3402affe1bc740ecb7c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.sentinelThreatIntelligenceIndicator.SentinelThreatIntelligenceIndicatorTimeouts",
    jsii_struct_bases=[],
    name_mapping={
        "create": "create",
        "delete": "delete",
        "read": "read",
        "update": "update",
    },
)
class SentinelThreatIntelligenceIndicatorTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_threat_intelligence_indicator#create SentinelThreatIntelligenceIndicator#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_threat_intelligence_indicator#delete SentinelThreatIntelligenceIndicator#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_threat_intelligence_indicator#read SentinelThreatIntelligenceIndicator#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_threat_intelligence_indicator#update SentinelThreatIntelligenceIndicator#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__80e24bfef6dd8ce529b2a9624b45f4b6bac1564edf318842503e3cd8f660e98e)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_threat_intelligence_indicator#create SentinelThreatIntelligenceIndicator#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_threat_intelligence_indicator#delete SentinelThreatIntelligenceIndicator#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def read(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_threat_intelligence_indicator#read SentinelThreatIntelligenceIndicator#read}.'''
        result = self._values.get("read")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_threat_intelligence_indicator#update SentinelThreatIntelligenceIndicator#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SentinelThreatIntelligenceIndicatorTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SentinelThreatIntelligenceIndicatorTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.sentinelThreatIntelligenceIndicator.SentinelThreatIntelligenceIndicatorTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bdc6e6ef52ccb6ed8a7a50db9797123db60a73dfe93bf83bba741053f891a85d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__057e3c75ba9634c09834bca331a6d48ad5ad03162a696cb9178157b8304a9016)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2dc38561aac4efcb1daccd318c8d9c6797c4299d44f8d7d6bab2baa4be312d00)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="read")
    def read(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "read"))

    @read.setter
    def read(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7fffdf265b7ce1d6270bd12429440e20a322135e83e573cc50a948e28fa879cc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "read", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__484475bb4fca7e3dd7ce5afc4172d07dbf3d7cbe42ac3f8b7560f0897fd30ee2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SentinelThreatIntelligenceIndicatorTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SentinelThreatIntelligenceIndicatorTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SentinelThreatIntelligenceIndicatorTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__abf488907b61b64ef902eab3d3968d8a9bc89469e9949511e9d82161777eca9e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "SentinelThreatIntelligenceIndicator",
    "SentinelThreatIntelligenceIndicatorConfig",
    "SentinelThreatIntelligenceIndicatorExternalReference",
    "SentinelThreatIntelligenceIndicatorExternalReferenceList",
    "SentinelThreatIntelligenceIndicatorExternalReferenceOutputReference",
    "SentinelThreatIntelligenceIndicatorGranularMarking",
    "SentinelThreatIntelligenceIndicatorGranularMarkingList",
    "SentinelThreatIntelligenceIndicatorGranularMarkingOutputReference",
    "SentinelThreatIntelligenceIndicatorKillChainPhase",
    "SentinelThreatIntelligenceIndicatorKillChainPhaseList",
    "SentinelThreatIntelligenceIndicatorKillChainPhaseOutputReference",
    "SentinelThreatIntelligenceIndicatorParsedPattern",
    "SentinelThreatIntelligenceIndicatorParsedPatternList",
    "SentinelThreatIntelligenceIndicatorParsedPatternOutputReference",
    "SentinelThreatIntelligenceIndicatorParsedPatternPatternTypeValues",
    "SentinelThreatIntelligenceIndicatorParsedPatternPatternTypeValuesList",
    "SentinelThreatIntelligenceIndicatorParsedPatternPatternTypeValuesOutputReference",
    "SentinelThreatIntelligenceIndicatorTimeouts",
    "SentinelThreatIntelligenceIndicatorTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__7817adcd75aa1da35fca88b14e5cc128f08b8ec6a6884a9213dd35d93873dac0(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    display_name: builtins.str,
    pattern: builtins.str,
    pattern_type: builtins.str,
    source: builtins.str,
    validate_from_utc: builtins.str,
    workspace_id: builtins.str,
    confidence: typing.Optional[jsii.Number] = None,
    created_by: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    extension: typing.Optional[builtins.str] = None,
    external_reference: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SentinelThreatIntelligenceIndicatorExternalReference, typing.Dict[builtins.str, typing.Any]]]]] = None,
    granular_marking: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SentinelThreatIntelligenceIndicatorGranularMarking, typing.Dict[builtins.str, typing.Any]]]]] = None,
    id: typing.Optional[builtins.str] = None,
    kill_chain_phase: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SentinelThreatIntelligenceIndicatorKillChainPhase, typing.Dict[builtins.str, typing.Any]]]]] = None,
    language: typing.Optional[builtins.str] = None,
    object_marking_refs: typing.Optional[typing.Sequence[builtins.str]] = None,
    pattern_version: typing.Optional[builtins.str] = None,
    revoked: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    tags: typing.Optional[typing.Sequence[builtins.str]] = None,
    threat_types: typing.Optional[typing.Sequence[builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[SentinelThreatIntelligenceIndicatorTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    validate_until_utc: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__7b9a204a8ac1ba71bc9467e51e723164b55c48f478fc0264b7c08a7d8a8cedb0(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ce7fd512c5f04391b387875b49cdbb62b7857f8a16109d3fecea737c7cdda57(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SentinelThreatIntelligenceIndicatorExternalReference, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f50d041b16922ac2df8092307f3708ecfa72b143b999a2c1a886f9dd5a0b2c0(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SentinelThreatIntelligenceIndicatorGranularMarking, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a4572d52b0dcb29657225f12e9a6c14bee20e3f3bf02c962d292dd579427701(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SentinelThreatIntelligenceIndicatorKillChainPhase, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4701bc4f5395745912e47dd255d6257c21b245832e9caf0d5e8b1ef9c3e90880(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c861121a0a20a0e6d265819461f3cf5b437e4907e2ab90a70a7eac8e33d5a376(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0495fb26d2f294b364d75d010f811d35757ea62ee8456a882fd32c6e4035fbb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8179d4562ae5797593b0844e7623d23c0ff3945d9d1a28d6cac105f22ea4901(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fae71b6a877566a7f736cedbe27ebae7497267f5d77ee9bcf08b267aa432c993(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3293f95fef3c5368cca7473d0928dd03d4df2ac1dd45d2a886238e7f5a01a9c2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25bc8052d350c09bdc864c2a245a3f88e210bff81f652946e5e30685966e46c6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5454463a333578130daf5abb2396ec8a6b83373f115d5e18155abd2a0921b19b(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28df4d33fa9e1ef1bbdd4426e0ab860cc1a7991bc3b1b52fcd4f98c74bd12ce5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85fc16400becb0b56fdce7d830311424c2461a494674a06279794e560d8e4b26(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9fdfc788645df74708bf8f154f7978cd6dc434e6f368a122c0385dd8e025a98(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aacc8150f719efa6bb96583a32e76b0f8faf9b0480290d44bd0a7a763e158f42(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__51231cbdf606635a46927c64ece72fdf5c5eae0d433e4ee4df81cb18a9a8b962(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4486dc58fef018723831cadf6772ee808f20b3e8f9a2f7e6c655e8c85d94bdf6(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a255f63f93b557b53d7eb5b8c763df70634777d7ce493041d4c0c157256a923(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57521af187b93a44f5f01acf941705e1cbca038a2431f7c872e821050cc04d0b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24328b419ccebf3f9e2f00f68cc9d7958cbd67ea7cbcb3b90b4e259b916dc2d2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14c3ab419c45eeacde73b071e017f9363ac61e1d4c92c0709e23026cabccc1f5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__845ca128ec8aad545d3fddb209929a1c49a2f435c44c66882c0a749bf838bffb(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    display_name: builtins.str,
    pattern: builtins.str,
    pattern_type: builtins.str,
    source: builtins.str,
    validate_from_utc: builtins.str,
    workspace_id: builtins.str,
    confidence: typing.Optional[jsii.Number] = None,
    created_by: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    extension: typing.Optional[builtins.str] = None,
    external_reference: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SentinelThreatIntelligenceIndicatorExternalReference, typing.Dict[builtins.str, typing.Any]]]]] = None,
    granular_marking: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SentinelThreatIntelligenceIndicatorGranularMarking, typing.Dict[builtins.str, typing.Any]]]]] = None,
    id: typing.Optional[builtins.str] = None,
    kill_chain_phase: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SentinelThreatIntelligenceIndicatorKillChainPhase, typing.Dict[builtins.str, typing.Any]]]]] = None,
    language: typing.Optional[builtins.str] = None,
    object_marking_refs: typing.Optional[typing.Sequence[builtins.str]] = None,
    pattern_version: typing.Optional[builtins.str] = None,
    revoked: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    tags: typing.Optional[typing.Sequence[builtins.str]] = None,
    threat_types: typing.Optional[typing.Sequence[builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[SentinelThreatIntelligenceIndicatorTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    validate_until_utc: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24ecb05e05f5cf9d0d0503e6c583bf811c955e6cbab66534fb5fd023a8cda499(
    *,
    description: typing.Optional[builtins.str] = None,
    hashes: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    source_name: typing.Optional[builtins.str] = None,
    url: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__193c2db83a5440460e7919c800579e087fd69b2286f8aacd5274848b73a5374e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6af0470ce63fdffc3176e9fe7883a5a4e203d5aba7ac8cbea91572a972f5a170(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44358fd054671ec74f5c7ae104c227dc011df976762e19a209f70c49317bb309(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8166b9794d26e137ec703929ee170430a9a6d1419e63a75ac8e53bdf5170a424(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6fa16e1901277a9f5b541f32088b42790a14f890b8d119f522096bbabed61d50(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7fa7e305dc6183026592940d12610942eb31847039335418220cf89e8ed03d95(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SentinelThreatIntelligenceIndicatorExternalReference]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__962d58d40d1e8f2c9fe9fbf28a37bd76e63388a0d1a417b676f4f08ec8dd2d30(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a6a32232bdf700bd598794619b5ad5971fcf88063d1e730d58781789b3b6ce3d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__55abe5c5a04127ee33a77fcd9063071e17564be923e99067b1c626b8dc2fcb4d(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e36d9c31e04abce089fa7f214765e192badf375ad53c518816bcbe0e312e7d4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31e29f5679d19ba5d08cf201662a7fc823e57939b1ea1f4d9da5072f2fc36b6e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25670fc4740facd5b36689302dd21659b0033b439418bc0b7eca307c155ab93d(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SentinelThreatIntelligenceIndicatorExternalReference]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9719f58939752f61ccf7fbdbafbb1ac5c0665406ec70f73715ec9f171c0c6858(
    *,
    language: typing.Optional[builtins.str] = None,
    marking_ref: typing.Optional[builtins.str] = None,
    selectors: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1cda6e961189928ffb61f6d521659fa4a67a5f70b4e4c88bdfd1f4c9a129f58b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f8bcca1db1b96208a51855d86bb20075368ec6f697664eb082c08d8dce98935(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1296feb9b19ec64d382ca36a99a60d38d2e30b6a87b13f877ad90a4c2d52730c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e355035fb7224591c50a7f0f0d5963da82d3a1fa13f8f1f164f5e16e58619946(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45b5a75196a80fee8f680b46c96135308af3ccfc8553e325b5c390f6829978fe(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3f533379a07c1cc823a5f83d7c136c75bf12b20afa64386408f240aa26a7e65(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SentinelThreatIntelligenceIndicatorGranularMarking]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d73b75359d6cb173d068dbb1fabca240b46b52131f1ee544b2088093e9742f1d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e84bd61d3cf401ffb0506370f8b29d40b16ae77a61b478725b2579108a82a21(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8842692ae0e6119ca2f1bf8dd667c05657546253c869493cd18dc60e63a3b1fc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7cad1d9324083666fdeb48bec08d75b23f82e161ca2c5839c86d5fe4d397e08e(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f73b72e4f290bec1eb18068917387b9c160d9230d6ff71c360204696318518bf(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SentinelThreatIntelligenceIndicatorGranularMarking]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e9f5492d25458ea2af1e5d5b7a05ba17532ef8139f19461f2f078b68f0609b8(
    *,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52db5bb53c2864e4b496adabe43ed1380f923987a69b15a1cdc80c991c97bce6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f16460df7edc1446e04ad806ca59991cecb72286ff8e6cbf99b2aa4450660a4c(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9029ba47a07f743e3267bdff3f1da7a7a7b750faab0da19b0dadb43deb0f3f33(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d3265ae50e6a60a69ad123a10be9f4c29e610ac885acf085a5ec20d9be007a9(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__792d1c0023d0b1363d90ff37e4a17795b4b36a3d418e6b6968ec35d384c6e791(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d31357c803a1b2ea861704330ff1ebde1d75c381f93a64782b0261cf7be74392(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SentinelThreatIntelligenceIndicatorKillChainPhase]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1109fb2ade460f72b88406830f0b3d746cb32b83bb8e8e49cfe0dc3443fafc6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__32b1f4e1d7243bf6a9b63c2f3fe93e6b6883153e7b4bed9fdb58a793808c7237(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d48cd621d8e5f8cc434a24a764c0c25629797e360b777831c94e7f26b57be53(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SentinelThreatIntelligenceIndicatorKillChainPhase]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bed8e28de4c3f9c6bfc3a81bcb969ed38ffd8abe0b60a19f8069316ae5836454(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f50bf621fa2090791bff6b922222762dcc6e183f180f06180dc9cc8ab7440599(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d882a123bb13392074c6e390f6efcdb7622aa0744d8243c4551c798435dc300(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a8e1f34894f9e05e410438bed3f8c64c1e4686aad9ce77215dfd48cea64e7bc(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2352b9418550de134a0478eca8f2116c7ea9b0eb5b1f2df40e4c4a52ee335ee(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e6f56de7fa33363507610f29b461c56467c80b1c64eca108b13a94198d75992(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66a3f1b7bf44e0210fc80493374786ddd06596988d7e048f4ea76006a300e62f(
    value: typing.Optional[SentinelThreatIntelligenceIndicatorParsedPattern],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a16d44bf7b814fbd0ce244f279ff3e7d2a9cf8f5996f8cccf1563d35793b7c6c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30f477e4cdcf5ae6ade730f19e291cc38ad56c1b575027be18a2b461eeac618f(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94992d3c477bafe9ce81d2bfb07d873d86758519f30e95b45198c49931fa8a1c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f959d0adfd380a57f95bb2c62ef4dd79eccdcec45415984a655a4aab2d1c26d(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a46e82696a22e9959d065d553e243366cfc2c7f5fd5be2bfbb9bb3afcc4e0a77(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9cd8014e2c4831390aaee3f72cd8091a46ab4fa727a18d807cb69ef0f7906eb3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__694607ce7173eda9012102469c6cfb1627fd606bdd6be3402affe1bc740ecb7c(
    value: typing.Optional[SentinelThreatIntelligenceIndicatorParsedPatternPatternTypeValues],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80e24bfef6dd8ce529b2a9624b45f4b6bac1564edf318842503e3cd8f660e98e(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    read: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bdc6e6ef52ccb6ed8a7a50db9797123db60a73dfe93bf83bba741053f891a85d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__057e3c75ba9634c09834bca331a6d48ad5ad03162a696cb9178157b8304a9016(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2dc38561aac4efcb1daccd318c8d9c6797c4299d44f8d7d6bab2baa4be312d00(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7fffdf265b7ce1d6270bd12429440e20a322135e83e573cc50a948e28fa879cc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__484475bb4fca7e3dd7ce5afc4172d07dbf3d7cbe42ac3f8b7560f0897fd30ee2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__abf488907b61b64ef902eab3d3968d8a9bc89469e9949511e9d82161777eca9e(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SentinelThreatIntelligenceIndicatorTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
