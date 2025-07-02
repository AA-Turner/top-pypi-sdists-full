r'''
# `azurerm_sentinel_alert_rule_nrt`

Refer to the Terraform Registry for docs: [`azurerm_sentinel_alert_rule_nrt`](https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_alert_rule_nrt).
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


class SentinelAlertRuleNrt(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.sentinelAlertRuleNrt.SentinelAlertRuleNrt",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_alert_rule_nrt azurerm_sentinel_alert_rule_nrt}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        display_name: builtins.str,
        event_grouping: typing.Union["SentinelAlertRuleNrtEventGrouping", typing.Dict[builtins.str, typing.Any]],
        log_analytics_workspace_id: builtins.str,
        name: builtins.str,
        query: builtins.str,
        severity: builtins.str,
        alert_details_override: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SentinelAlertRuleNrtAlertDetailsOverride", typing.Dict[builtins.str, typing.Any]]]]] = None,
        alert_rule_template_guid: typing.Optional[builtins.str] = None,
        alert_rule_template_version: typing.Optional[builtins.str] = None,
        custom_details: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        description: typing.Optional[builtins.str] = None,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        entity_mapping: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SentinelAlertRuleNrtEntityMapping", typing.Dict[builtins.str, typing.Any]]]]] = None,
        id: typing.Optional[builtins.str] = None,
        incident: typing.Optional[typing.Union["SentinelAlertRuleNrtIncident", typing.Dict[builtins.str, typing.Any]]] = None,
        sentinel_entity_mapping: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SentinelAlertRuleNrtSentinelEntityMapping", typing.Dict[builtins.str, typing.Any]]]]] = None,
        suppression_duration: typing.Optional[builtins.str] = None,
        suppression_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        tactics: typing.Optional[typing.Sequence[builtins.str]] = None,
        techniques: typing.Optional[typing.Sequence[builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["SentinelAlertRuleNrtTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_alert_rule_nrt azurerm_sentinel_alert_rule_nrt} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param display_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_alert_rule_nrt#display_name SentinelAlertRuleNrt#display_name}.
        :param event_grouping: event_grouping block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_alert_rule_nrt#event_grouping SentinelAlertRuleNrt#event_grouping}
        :param log_analytics_workspace_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_alert_rule_nrt#log_analytics_workspace_id SentinelAlertRuleNrt#log_analytics_workspace_id}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_alert_rule_nrt#name SentinelAlertRuleNrt#name}.
        :param query: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_alert_rule_nrt#query SentinelAlertRuleNrt#query}.
        :param severity: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_alert_rule_nrt#severity SentinelAlertRuleNrt#severity}.
        :param alert_details_override: alert_details_override block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_alert_rule_nrt#alert_details_override SentinelAlertRuleNrt#alert_details_override}
        :param alert_rule_template_guid: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_alert_rule_nrt#alert_rule_template_guid SentinelAlertRuleNrt#alert_rule_template_guid}.
        :param alert_rule_template_version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_alert_rule_nrt#alert_rule_template_version SentinelAlertRuleNrt#alert_rule_template_version}.
        :param custom_details: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_alert_rule_nrt#custom_details SentinelAlertRuleNrt#custom_details}.
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_alert_rule_nrt#description SentinelAlertRuleNrt#description}.
        :param enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_alert_rule_nrt#enabled SentinelAlertRuleNrt#enabled}.
        :param entity_mapping: entity_mapping block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_alert_rule_nrt#entity_mapping SentinelAlertRuleNrt#entity_mapping}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_alert_rule_nrt#id SentinelAlertRuleNrt#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param incident: incident block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_alert_rule_nrt#incident SentinelAlertRuleNrt#incident}
        :param sentinel_entity_mapping: sentinel_entity_mapping block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_alert_rule_nrt#sentinel_entity_mapping SentinelAlertRuleNrt#sentinel_entity_mapping}
        :param suppression_duration: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_alert_rule_nrt#suppression_duration SentinelAlertRuleNrt#suppression_duration}.
        :param suppression_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_alert_rule_nrt#suppression_enabled SentinelAlertRuleNrt#suppression_enabled}.
        :param tactics: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_alert_rule_nrt#tactics SentinelAlertRuleNrt#tactics}.
        :param techniques: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_alert_rule_nrt#techniques SentinelAlertRuleNrt#techniques}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_alert_rule_nrt#timeouts SentinelAlertRuleNrt#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bfbaa88fe7e2a9dc64067329ed8c574fd89e3cb4a5f2ed4f136a36964efd974e)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = SentinelAlertRuleNrtConfig(
            display_name=display_name,
            event_grouping=event_grouping,
            log_analytics_workspace_id=log_analytics_workspace_id,
            name=name,
            query=query,
            severity=severity,
            alert_details_override=alert_details_override,
            alert_rule_template_guid=alert_rule_template_guid,
            alert_rule_template_version=alert_rule_template_version,
            custom_details=custom_details,
            description=description,
            enabled=enabled,
            entity_mapping=entity_mapping,
            id=id,
            incident=incident,
            sentinel_entity_mapping=sentinel_entity_mapping,
            suppression_duration=suppression_duration,
            suppression_enabled=suppression_enabled,
            tactics=tactics,
            techniques=techniques,
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
        '''Generates CDKTF code for importing a SentinelAlertRuleNrt resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the SentinelAlertRuleNrt to import.
        :param import_from_id: The id of the existing SentinelAlertRuleNrt that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_alert_rule_nrt#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the SentinelAlertRuleNrt to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5df39870b373f86babd0c09ab76ca498d33896fc56d449ff10f0738f8ad8971f)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putAlertDetailsOverride")
    def put_alert_details_override(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SentinelAlertRuleNrtAlertDetailsOverride", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7d52e84e64a22d075c64dbc38327d763e95ac60106e42d5d8b4a8420c35e7e11)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putAlertDetailsOverride", [value]))

    @jsii.member(jsii_name="putEntityMapping")
    def put_entity_mapping(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SentinelAlertRuleNrtEntityMapping", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa4a3534b020c49f1421955bbc402f224db7a244535f28c293da4ea8ed202d4f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putEntityMapping", [value]))

    @jsii.member(jsii_name="putEventGrouping")
    def put_event_grouping(self, *, aggregation_method: builtins.str) -> None:
        '''
        :param aggregation_method: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_alert_rule_nrt#aggregation_method SentinelAlertRuleNrt#aggregation_method}.
        '''
        value = SentinelAlertRuleNrtEventGrouping(
            aggregation_method=aggregation_method
        )

        return typing.cast(None, jsii.invoke(self, "putEventGrouping", [value]))

    @jsii.member(jsii_name="putIncident")
    def put_incident(
        self,
        *,
        create_incident_enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        grouping: typing.Union["SentinelAlertRuleNrtIncidentGrouping", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param create_incident_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_alert_rule_nrt#create_incident_enabled SentinelAlertRuleNrt#create_incident_enabled}.
        :param grouping: grouping block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_alert_rule_nrt#grouping SentinelAlertRuleNrt#grouping}
        '''
        value = SentinelAlertRuleNrtIncident(
            create_incident_enabled=create_incident_enabled, grouping=grouping
        )

        return typing.cast(None, jsii.invoke(self, "putIncident", [value]))

    @jsii.member(jsii_name="putSentinelEntityMapping")
    def put_sentinel_entity_mapping(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SentinelAlertRuleNrtSentinelEntityMapping", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8aaca0f95fae7566b6a576b284f803a5b66f55e55720fbf90bc325bf9c42690e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putSentinelEntityMapping", [value]))

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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_alert_rule_nrt#create SentinelAlertRuleNrt#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_alert_rule_nrt#delete SentinelAlertRuleNrt#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_alert_rule_nrt#read SentinelAlertRuleNrt#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_alert_rule_nrt#update SentinelAlertRuleNrt#update}.
        '''
        value = SentinelAlertRuleNrtTimeouts(
            create=create, delete=delete, read=read, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetAlertDetailsOverride")
    def reset_alert_details_override(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAlertDetailsOverride", []))

    @jsii.member(jsii_name="resetAlertRuleTemplateGuid")
    def reset_alert_rule_template_guid(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAlertRuleTemplateGuid", []))

    @jsii.member(jsii_name="resetAlertRuleTemplateVersion")
    def reset_alert_rule_template_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAlertRuleTemplateVersion", []))

    @jsii.member(jsii_name="resetCustomDetails")
    def reset_custom_details(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCustomDetails", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetEnabled")
    def reset_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnabled", []))

    @jsii.member(jsii_name="resetEntityMapping")
    def reset_entity_mapping(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEntityMapping", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetIncident")
    def reset_incident(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIncident", []))

    @jsii.member(jsii_name="resetSentinelEntityMapping")
    def reset_sentinel_entity_mapping(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSentinelEntityMapping", []))

    @jsii.member(jsii_name="resetSuppressionDuration")
    def reset_suppression_duration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSuppressionDuration", []))

    @jsii.member(jsii_name="resetSuppressionEnabled")
    def reset_suppression_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSuppressionEnabled", []))

    @jsii.member(jsii_name="resetTactics")
    def reset_tactics(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTactics", []))

    @jsii.member(jsii_name="resetTechniques")
    def reset_techniques(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTechniques", []))

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
    @jsii.member(jsii_name="alertDetailsOverride")
    def alert_details_override(self) -> "SentinelAlertRuleNrtAlertDetailsOverrideList":
        return typing.cast("SentinelAlertRuleNrtAlertDetailsOverrideList", jsii.get(self, "alertDetailsOverride"))

    @builtins.property
    @jsii.member(jsii_name="entityMapping")
    def entity_mapping(self) -> "SentinelAlertRuleNrtEntityMappingList":
        return typing.cast("SentinelAlertRuleNrtEntityMappingList", jsii.get(self, "entityMapping"))

    @builtins.property
    @jsii.member(jsii_name="eventGrouping")
    def event_grouping(self) -> "SentinelAlertRuleNrtEventGroupingOutputReference":
        return typing.cast("SentinelAlertRuleNrtEventGroupingOutputReference", jsii.get(self, "eventGrouping"))

    @builtins.property
    @jsii.member(jsii_name="incident")
    def incident(self) -> "SentinelAlertRuleNrtIncidentOutputReference":
        return typing.cast("SentinelAlertRuleNrtIncidentOutputReference", jsii.get(self, "incident"))

    @builtins.property
    @jsii.member(jsii_name="sentinelEntityMapping")
    def sentinel_entity_mapping(
        self,
    ) -> "SentinelAlertRuleNrtSentinelEntityMappingList":
        return typing.cast("SentinelAlertRuleNrtSentinelEntityMappingList", jsii.get(self, "sentinelEntityMapping"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "SentinelAlertRuleNrtTimeoutsOutputReference":
        return typing.cast("SentinelAlertRuleNrtTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="alertDetailsOverrideInput")
    def alert_details_override_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SentinelAlertRuleNrtAlertDetailsOverride"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SentinelAlertRuleNrtAlertDetailsOverride"]]], jsii.get(self, "alertDetailsOverrideInput"))

    @builtins.property
    @jsii.member(jsii_name="alertRuleTemplateGuidInput")
    def alert_rule_template_guid_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "alertRuleTemplateGuidInput"))

    @builtins.property
    @jsii.member(jsii_name="alertRuleTemplateVersionInput")
    def alert_rule_template_version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "alertRuleTemplateVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="customDetailsInput")
    def custom_details_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "customDetailsInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="displayNameInput")
    def display_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "displayNameInput"))

    @builtins.property
    @jsii.member(jsii_name="enabledInput")
    def enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enabledInput"))

    @builtins.property
    @jsii.member(jsii_name="entityMappingInput")
    def entity_mapping_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SentinelAlertRuleNrtEntityMapping"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SentinelAlertRuleNrtEntityMapping"]]], jsii.get(self, "entityMappingInput"))

    @builtins.property
    @jsii.member(jsii_name="eventGroupingInput")
    def event_grouping_input(
        self,
    ) -> typing.Optional["SentinelAlertRuleNrtEventGrouping"]:
        return typing.cast(typing.Optional["SentinelAlertRuleNrtEventGrouping"], jsii.get(self, "eventGroupingInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="incidentInput")
    def incident_input(self) -> typing.Optional["SentinelAlertRuleNrtIncident"]:
        return typing.cast(typing.Optional["SentinelAlertRuleNrtIncident"], jsii.get(self, "incidentInput"))

    @builtins.property
    @jsii.member(jsii_name="logAnalyticsWorkspaceIdInput")
    def log_analytics_workspace_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "logAnalyticsWorkspaceIdInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="queryInput")
    def query_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "queryInput"))

    @builtins.property
    @jsii.member(jsii_name="sentinelEntityMappingInput")
    def sentinel_entity_mapping_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SentinelAlertRuleNrtSentinelEntityMapping"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SentinelAlertRuleNrtSentinelEntityMapping"]]], jsii.get(self, "sentinelEntityMappingInput"))

    @builtins.property
    @jsii.member(jsii_name="severityInput")
    def severity_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "severityInput"))

    @builtins.property
    @jsii.member(jsii_name="suppressionDurationInput")
    def suppression_duration_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "suppressionDurationInput"))

    @builtins.property
    @jsii.member(jsii_name="suppressionEnabledInput")
    def suppression_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "suppressionEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="tacticsInput")
    def tactics_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "tacticsInput"))

    @builtins.property
    @jsii.member(jsii_name="techniquesInput")
    def techniques_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "techniquesInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "SentinelAlertRuleNrtTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "SentinelAlertRuleNrtTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="alertRuleTemplateGuid")
    def alert_rule_template_guid(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "alertRuleTemplateGuid"))

    @alert_rule_template_guid.setter
    def alert_rule_template_guid(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8f80c7c8dd3c129bb0eec89322aa268786835d1c2c9d1ba1ddb7bf881954804a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "alertRuleTemplateGuid", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="alertRuleTemplateVersion")
    def alert_rule_template_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "alertRuleTemplateVersion"))

    @alert_rule_template_version.setter
    def alert_rule_template_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b0889127053c3f81e80eef5f658e9d4e86ca92295dd87553b218ad5d358ade96)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "alertRuleTemplateVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="customDetails")
    def custom_details(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "customDetails"))

    @custom_details.setter
    def custom_details(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e816787399352b8a3e7db4891417f4fa0010df96d064f6bd3b88ea584a454f5f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "customDetails", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2fd708d4a9222d9de71abd958b289a1e24184f61e313c56b81b2510ef5f874c4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="displayName")
    def display_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "displayName"))

    @display_name.setter
    def display_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf2c3c73192e69d08e681fca07b43ea787ae9743d2a6d9fafb265174ce27a07f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "displayName", value) # pyright: ignore[reportArgumentType]

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
            type_hints = typing.get_type_hints(_typecheckingstub__00b564a80c7c23f8f73e3546f2e4133d0041a94a0f40ca3f06ae71747ee023ca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e8eff7f1b152fd39e7df93cbfff933b04fc4390c77edcb8975edf803bef223d4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="logAnalyticsWorkspaceId")
    def log_analytics_workspace_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "logAnalyticsWorkspaceId"))

    @log_analytics_workspace_id.setter
    def log_analytics_workspace_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f78d2dceeb9c203f4987f9c3b547725248445ab9b99a6fbdf392da852b2326a1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "logAnalyticsWorkspaceId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cbb452ccbfcd5a354eeb5ff24a2a2fa9f07ae91638198c56fe4de2a1b96e3daa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="query")
    def query(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "query"))

    @query.setter
    def query(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ca089963f0dc95d6702cb27928ffae60dd9a4cb84a999cf4ed84943afb826ca6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "query", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="severity")
    def severity(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "severity"))

    @severity.setter
    def severity(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c02688e6e5602e4a97e96a8240914e245d74144ea295686bbf04a37a8093cfc4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "severity", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="suppressionDuration")
    def suppression_duration(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "suppressionDuration"))

    @suppression_duration.setter
    def suppression_duration(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a0f0175597a97240ebcd6645b2a7f72cb88f617c0b862a931bd3011866c2fdae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "suppressionDuration", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="suppressionEnabled")
    def suppression_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "suppressionEnabled"))

    @suppression_enabled.setter
    def suppression_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__24d167e32f4aa42c10150eaab63119cdcce81e95fe9937032ecc94d8b91b54d0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "suppressionEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tactics")
    def tactics(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "tactics"))

    @tactics.setter
    def tactics(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__73e9e5f346102d8d836409b3542644c002402d767c546ce17c541bacf2e6f84f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tactics", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="techniques")
    def techniques(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "techniques"))

    @techniques.setter
    def techniques(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4b783bfdd21834181cf70a0a298541652dd16c9ab301344d7fc6c8698eba694c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "techniques", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.sentinelAlertRuleNrt.SentinelAlertRuleNrtAlertDetailsOverride",
    jsii_struct_bases=[],
    name_mapping={
        "description_format": "descriptionFormat",
        "display_name_format": "displayNameFormat",
        "dynamic_property": "dynamicProperty",
        "severity_column_name": "severityColumnName",
        "tactics_column_name": "tacticsColumnName",
    },
)
class SentinelAlertRuleNrtAlertDetailsOverride:
    def __init__(
        self,
        *,
        description_format: typing.Optional[builtins.str] = None,
        display_name_format: typing.Optional[builtins.str] = None,
        dynamic_property: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SentinelAlertRuleNrtAlertDetailsOverrideDynamicProperty", typing.Dict[builtins.str, typing.Any]]]]] = None,
        severity_column_name: typing.Optional[builtins.str] = None,
        tactics_column_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param description_format: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_alert_rule_nrt#description_format SentinelAlertRuleNrt#description_format}.
        :param display_name_format: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_alert_rule_nrt#display_name_format SentinelAlertRuleNrt#display_name_format}.
        :param dynamic_property: dynamic_property block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_alert_rule_nrt#dynamic_property SentinelAlertRuleNrt#dynamic_property}
        :param severity_column_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_alert_rule_nrt#severity_column_name SentinelAlertRuleNrt#severity_column_name}.
        :param tactics_column_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_alert_rule_nrt#tactics_column_name SentinelAlertRuleNrt#tactics_column_name}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f4c1c0f00bcb6b905d0b3b13374bee1b8252b45b2dd3b100814631bad7aeccf)
            check_type(argname="argument description_format", value=description_format, expected_type=type_hints["description_format"])
            check_type(argname="argument display_name_format", value=display_name_format, expected_type=type_hints["display_name_format"])
            check_type(argname="argument dynamic_property", value=dynamic_property, expected_type=type_hints["dynamic_property"])
            check_type(argname="argument severity_column_name", value=severity_column_name, expected_type=type_hints["severity_column_name"])
            check_type(argname="argument tactics_column_name", value=tactics_column_name, expected_type=type_hints["tactics_column_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if description_format is not None:
            self._values["description_format"] = description_format
        if display_name_format is not None:
            self._values["display_name_format"] = display_name_format
        if dynamic_property is not None:
            self._values["dynamic_property"] = dynamic_property
        if severity_column_name is not None:
            self._values["severity_column_name"] = severity_column_name
        if tactics_column_name is not None:
            self._values["tactics_column_name"] = tactics_column_name

    @builtins.property
    def description_format(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_alert_rule_nrt#description_format SentinelAlertRuleNrt#description_format}.'''
        result = self._values.get("description_format")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def display_name_format(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_alert_rule_nrt#display_name_format SentinelAlertRuleNrt#display_name_format}.'''
        result = self._values.get("display_name_format")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def dynamic_property(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SentinelAlertRuleNrtAlertDetailsOverrideDynamicProperty"]]]:
        '''dynamic_property block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_alert_rule_nrt#dynamic_property SentinelAlertRuleNrt#dynamic_property}
        '''
        result = self._values.get("dynamic_property")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SentinelAlertRuleNrtAlertDetailsOverrideDynamicProperty"]]], result)

    @builtins.property
    def severity_column_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_alert_rule_nrt#severity_column_name SentinelAlertRuleNrt#severity_column_name}.'''
        result = self._values.get("severity_column_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tactics_column_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_alert_rule_nrt#tactics_column_name SentinelAlertRuleNrt#tactics_column_name}.'''
        result = self._values.get("tactics_column_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SentinelAlertRuleNrtAlertDetailsOverride(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.sentinelAlertRuleNrt.SentinelAlertRuleNrtAlertDetailsOverrideDynamicProperty",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "value": "value"},
)
class SentinelAlertRuleNrtAlertDetailsOverrideDynamicProperty:
    def __init__(self, *, name: builtins.str, value: builtins.str) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_alert_rule_nrt#name SentinelAlertRuleNrt#name}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_alert_rule_nrt#value SentinelAlertRuleNrt#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f3c0bec216e206ad5adbb4073b89cd5e00e4d11dec2c474e256021994ad662ca)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "value": value,
        }

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_alert_rule_nrt#name SentinelAlertRuleNrt#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_alert_rule_nrt#value SentinelAlertRuleNrt#value}.'''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SentinelAlertRuleNrtAlertDetailsOverrideDynamicProperty(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SentinelAlertRuleNrtAlertDetailsOverrideDynamicPropertyList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.sentinelAlertRuleNrt.SentinelAlertRuleNrtAlertDetailsOverrideDynamicPropertyList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__67536f98ed031f6975d3bf155cde7718d8d89d3e49a210290232e7531d79dc7b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "SentinelAlertRuleNrtAlertDetailsOverrideDynamicPropertyOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9cfd43c97f2b4ffc4b24e935505d5fb8de066714091eb0c9d9d796b2172a62b6)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("SentinelAlertRuleNrtAlertDetailsOverrideDynamicPropertyOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b709c51164d5fe1091f915aea7de95dee880c57ab6de77320fcca98fc552edad)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1ae2acdf59073dce1a516713b3dbada1b055c05f6722d61ff35d789e979ce2c8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1171cdcd664e2111ac46005cbc9cd9d28a88a0c30af1a9944655a7e62458f9ff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SentinelAlertRuleNrtAlertDetailsOverrideDynamicProperty]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SentinelAlertRuleNrtAlertDetailsOverrideDynamicProperty]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SentinelAlertRuleNrtAlertDetailsOverrideDynamicProperty]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__635c177988f56af3027f7754126857781a21baaebb2eda5766d202cd001701fb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class SentinelAlertRuleNrtAlertDetailsOverrideDynamicPropertyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.sentinelAlertRuleNrt.SentinelAlertRuleNrtAlertDetailsOverrideDynamicPropertyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__237107f072dd42cca0d9c86be4c8f70851f9c92ce82c9dcc171807d47a1a1e6b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dba29a3d5aed094e4c8526b74117ec6c7bdf8420e434e4a38f6bdd5103926e57)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__443b794809d808ca9cbccd4af894d643d76ca0da5d98090b2e7b60f0fa4e17b3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SentinelAlertRuleNrtAlertDetailsOverrideDynamicProperty]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SentinelAlertRuleNrtAlertDetailsOverrideDynamicProperty]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SentinelAlertRuleNrtAlertDetailsOverrideDynamicProperty]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ec5073694e7cb11a13cd586eac18995fb3fa481ae3b62bdf8a467c9fad3693bd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class SentinelAlertRuleNrtAlertDetailsOverrideList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.sentinelAlertRuleNrt.SentinelAlertRuleNrtAlertDetailsOverrideList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__26359d17b8676b060ab33f9521e2a53918b378991ae3986eb27c4512cba18886)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "SentinelAlertRuleNrtAlertDetailsOverrideOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e22019b16fd99e9bcf4267e1ee5c7c75eaf848d47f7c8a5ac11bb96c01af0025)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("SentinelAlertRuleNrtAlertDetailsOverrideOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a69ed4b2e3e6e6a904a0197035667241a5f5f8a63dc7db68d05def1691f1448)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2b001f62cce0518accb2dde800a20c83fc32b8a232a2781d5eb26334d46cd61a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__84b52cbbcfcf95b711963e8a3c08b48d7774890b8d5c6c592f2286a91eb6879c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SentinelAlertRuleNrtAlertDetailsOverride]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SentinelAlertRuleNrtAlertDetailsOverride]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SentinelAlertRuleNrtAlertDetailsOverride]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f7527afa00a19618274a13173e54a91f3cb756a4257994cceb001e823071ceca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class SentinelAlertRuleNrtAlertDetailsOverrideOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.sentinelAlertRuleNrt.SentinelAlertRuleNrtAlertDetailsOverrideOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__05ce7389f6959015342b599a1df9b4729ff139782fd0aa91f45e27a967a09f5f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putDynamicProperty")
    def put_dynamic_property(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SentinelAlertRuleNrtAlertDetailsOverrideDynamicProperty, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__74c88ec4dc7948689f6e346dab230746a6ad09b75807b640a7d584bda2ba5d04)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putDynamicProperty", [value]))

    @jsii.member(jsii_name="resetDescriptionFormat")
    def reset_description_format(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescriptionFormat", []))

    @jsii.member(jsii_name="resetDisplayNameFormat")
    def reset_display_name_format(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDisplayNameFormat", []))

    @jsii.member(jsii_name="resetDynamicProperty")
    def reset_dynamic_property(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDynamicProperty", []))

    @jsii.member(jsii_name="resetSeverityColumnName")
    def reset_severity_column_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSeverityColumnName", []))

    @jsii.member(jsii_name="resetTacticsColumnName")
    def reset_tactics_column_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTacticsColumnName", []))

    @builtins.property
    @jsii.member(jsii_name="dynamicProperty")
    def dynamic_property(
        self,
    ) -> SentinelAlertRuleNrtAlertDetailsOverrideDynamicPropertyList:
        return typing.cast(SentinelAlertRuleNrtAlertDetailsOverrideDynamicPropertyList, jsii.get(self, "dynamicProperty"))

    @builtins.property
    @jsii.member(jsii_name="descriptionFormatInput")
    def description_format_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionFormatInput"))

    @builtins.property
    @jsii.member(jsii_name="displayNameFormatInput")
    def display_name_format_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "displayNameFormatInput"))

    @builtins.property
    @jsii.member(jsii_name="dynamicPropertyInput")
    def dynamic_property_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SentinelAlertRuleNrtAlertDetailsOverrideDynamicProperty]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SentinelAlertRuleNrtAlertDetailsOverrideDynamicProperty]]], jsii.get(self, "dynamicPropertyInput"))

    @builtins.property
    @jsii.member(jsii_name="severityColumnNameInput")
    def severity_column_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "severityColumnNameInput"))

    @builtins.property
    @jsii.member(jsii_name="tacticsColumnNameInput")
    def tactics_column_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tacticsColumnNameInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionFormat")
    def description_format(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "descriptionFormat"))

    @description_format.setter
    def description_format(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__24e8fabdfc879fc5a6cb2c64ce822925212eb39af870a6da3c8a0ed9137aecf3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "descriptionFormat", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="displayNameFormat")
    def display_name_format(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "displayNameFormat"))

    @display_name_format.setter
    def display_name_format(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee7760b8a210d9aaca649c96529a387aa122782e36a3a214070822893213522e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "displayNameFormat", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="severityColumnName")
    def severity_column_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "severityColumnName"))

    @severity_column_name.setter
    def severity_column_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a801893b02bcdf698e623615bb4b135431a61a60b6fa8acb0074ee05575a3d46)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "severityColumnName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tacticsColumnName")
    def tactics_column_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tacticsColumnName"))

    @tactics_column_name.setter
    def tactics_column_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a31447b0cad07616b156dfa75a9e06436ddb2989371314faca072b33822efbe7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tacticsColumnName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SentinelAlertRuleNrtAlertDetailsOverride]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SentinelAlertRuleNrtAlertDetailsOverride]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SentinelAlertRuleNrtAlertDetailsOverride]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0584a63145811b0340bfbee289284cb449a9cbadc5c52b1a22f70b4d7cdfda7d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.sentinelAlertRuleNrt.SentinelAlertRuleNrtConfig",
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
        "event_grouping": "eventGrouping",
        "log_analytics_workspace_id": "logAnalyticsWorkspaceId",
        "name": "name",
        "query": "query",
        "severity": "severity",
        "alert_details_override": "alertDetailsOverride",
        "alert_rule_template_guid": "alertRuleTemplateGuid",
        "alert_rule_template_version": "alertRuleTemplateVersion",
        "custom_details": "customDetails",
        "description": "description",
        "enabled": "enabled",
        "entity_mapping": "entityMapping",
        "id": "id",
        "incident": "incident",
        "sentinel_entity_mapping": "sentinelEntityMapping",
        "suppression_duration": "suppressionDuration",
        "suppression_enabled": "suppressionEnabled",
        "tactics": "tactics",
        "techniques": "techniques",
        "timeouts": "timeouts",
    },
)
class SentinelAlertRuleNrtConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        event_grouping: typing.Union["SentinelAlertRuleNrtEventGrouping", typing.Dict[builtins.str, typing.Any]],
        log_analytics_workspace_id: builtins.str,
        name: builtins.str,
        query: builtins.str,
        severity: builtins.str,
        alert_details_override: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SentinelAlertRuleNrtAlertDetailsOverride, typing.Dict[builtins.str, typing.Any]]]]] = None,
        alert_rule_template_guid: typing.Optional[builtins.str] = None,
        alert_rule_template_version: typing.Optional[builtins.str] = None,
        custom_details: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        description: typing.Optional[builtins.str] = None,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        entity_mapping: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SentinelAlertRuleNrtEntityMapping", typing.Dict[builtins.str, typing.Any]]]]] = None,
        id: typing.Optional[builtins.str] = None,
        incident: typing.Optional[typing.Union["SentinelAlertRuleNrtIncident", typing.Dict[builtins.str, typing.Any]]] = None,
        sentinel_entity_mapping: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SentinelAlertRuleNrtSentinelEntityMapping", typing.Dict[builtins.str, typing.Any]]]]] = None,
        suppression_duration: typing.Optional[builtins.str] = None,
        suppression_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        tactics: typing.Optional[typing.Sequence[builtins.str]] = None,
        techniques: typing.Optional[typing.Sequence[builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["SentinelAlertRuleNrtTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param display_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_alert_rule_nrt#display_name SentinelAlertRuleNrt#display_name}.
        :param event_grouping: event_grouping block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_alert_rule_nrt#event_grouping SentinelAlertRuleNrt#event_grouping}
        :param log_analytics_workspace_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_alert_rule_nrt#log_analytics_workspace_id SentinelAlertRuleNrt#log_analytics_workspace_id}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_alert_rule_nrt#name SentinelAlertRuleNrt#name}.
        :param query: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_alert_rule_nrt#query SentinelAlertRuleNrt#query}.
        :param severity: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_alert_rule_nrt#severity SentinelAlertRuleNrt#severity}.
        :param alert_details_override: alert_details_override block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_alert_rule_nrt#alert_details_override SentinelAlertRuleNrt#alert_details_override}
        :param alert_rule_template_guid: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_alert_rule_nrt#alert_rule_template_guid SentinelAlertRuleNrt#alert_rule_template_guid}.
        :param alert_rule_template_version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_alert_rule_nrt#alert_rule_template_version SentinelAlertRuleNrt#alert_rule_template_version}.
        :param custom_details: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_alert_rule_nrt#custom_details SentinelAlertRuleNrt#custom_details}.
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_alert_rule_nrt#description SentinelAlertRuleNrt#description}.
        :param enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_alert_rule_nrt#enabled SentinelAlertRuleNrt#enabled}.
        :param entity_mapping: entity_mapping block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_alert_rule_nrt#entity_mapping SentinelAlertRuleNrt#entity_mapping}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_alert_rule_nrt#id SentinelAlertRuleNrt#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param incident: incident block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_alert_rule_nrt#incident SentinelAlertRuleNrt#incident}
        :param sentinel_entity_mapping: sentinel_entity_mapping block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_alert_rule_nrt#sentinel_entity_mapping SentinelAlertRuleNrt#sentinel_entity_mapping}
        :param suppression_duration: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_alert_rule_nrt#suppression_duration SentinelAlertRuleNrt#suppression_duration}.
        :param suppression_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_alert_rule_nrt#suppression_enabled SentinelAlertRuleNrt#suppression_enabled}.
        :param tactics: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_alert_rule_nrt#tactics SentinelAlertRuleNrt#tactics}.
        :param techniques: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_alert_rule_nrt#techniques SentinelAlertRuleNrt#techniques}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_alert_rule_nrt#timeouts SentinelAlertRuleNrt#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(event_grouping, dict):
            event_grouping = SentinelAlertRuleNrtEventGrouping(**event_grouping)
        if isinstance(incident, dict):
            incident = SentinelAlertRuleNrtIncident(**incident)
        if isinstance(timeouts, dict):
            timeouts = SentinelAlertRuleNrtTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__293a8328b2dc4ac66a254aa74c8b8c20f0bffe7981e9b2d6ec0a571989d825c3)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument display_name", value=display_name, expected_type=type_hints["display_name"])
            check_type(argname="argument event_grouping", value=event_grouping, expected_type=type_hints["event_grouping"])
            check_type(argname="argument log_analytics_workspace_id", value=log_analytics_workspace_id, expected_type=type_hints["log_analytics_workspace_id"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument query", value=query, expected_type=type_hints["query"])
            check_type(argname="argument severity", value=severity, expected_type=type_hints["severity"])
            check_type(argname="argument alert_details_override", value=alert_details_override, expected_type=type_hints["alert_details_override"])
            check_type(argname="argument alert_rule_template_guid", value=alert_rule_template_guid, expected_type=type_hints["alert_rule_template_guid"])
            check_type(argname="argument alert_rule_template_version", value=alert_rule_template_version, expected_type=type_hints["alert_rule_template_version"])
            check_type(argname="argument custom_details", value=custom_details, expected_type=type_hints["custom_details"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument entity_mapping", value=entity_mapping, expected_type=type_hints["entity_mapping"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument incident", value=incident, expected_type=type_hints["incident"])
            check_type(argname="argument sentinel_entity_mapping", value=sentinel_entity_mapping, expected_type=type_hints["sentinel_entity_mapping"])
            check_type(argname="argument suppression_duration", value=suppression_duration, expected_type=type_hints["suppression_duration"])
            check_type(argname="argument suppression_enabled", value=suppression_enabled, expected_type=type_hints["suppression_enabled"])
            check_type(argname="argument tactics", value=tactics, expected_type=type_hints["tactics"])
            check_type(argname="argument techniques", value=techniques, expected_type=type_hints["techniques"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "display_name": display_name,
            "event_grouping": event_grouping,
            "log_analytics_workspace_id": log_analytics_workspace_id,
            "name": name,
            "query": query,
            "severity": severity,
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
        if alert_details_override is not None:
            self._values["alert_details_override"] = alert_details_override
        if alert_rule_template_guid is not None:
            self._values["alert_rule_template_guid"] = alert_rule_template_guid
        if alert_rule_template_version is not None:
            self._values["alert_rule_template_version"] = alert_rule_template_version
        if custom_details is not None:
            self._values["custom_details"] = custom_details
        if description is not None:
            self._values["description"] = description
        if enabled is not None:
            self._values["enabled"] = enabled
        if entity_mapping is not None:
            self._values["entity_mapping"] = entity_mapping
        if id is not None:
            self._values["id"] = id
        if incident is not None:
            self._values["incident"] = incident
        if sentinel_entity_mapping is not None:
            self._values["sentinel_entity_mapping"] = sentinel_entity_mapping
        if suppression_duration is not None:
            self._values["suppression_duration"] = suppression_duration
        if suppression_enabled is not None:
            self._values["suppression_enabled"] = suppression_enabled
        if tactics is not None:
            self._values["tactics"] = tactics
        if techniques is not None:
            self._values["techniques"] = techniques
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_alert_rule_nrt#display_name SentinelAlertRuleNrt#display_name}.'''
        result = self._values.get("display_name")
        assert result is not None, "Required property 'display_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def event_grouping(self) -> "SentinelAlertRuleNrtEventGrouping":
        '''event_grouping block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_alert_rule_nrt#event_grouping SentinelAlertRuleNrt#event_grouping}
        '''
        result = self._values.get("event_grouping")
        assert result is not None, "Required property 'event_grouping' is missing"
        return typing.cast("SentinelAlertRuleNrtEventGrouping", result)

    @builtins.property
    def log_analytics_workspace_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_alert_rule_nrt#log_analytics_workspace_id SentinelAlertRuleNrt#log_analytics_workspace_id}.'''
        result = self._values.get("log_analytics_workspace_id")
        assert result is not None, "Required property 'log_analytics_workspace_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_alert_rule_nrt#name SentinelAlertRuleNrt#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def query(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_alert_rule_nrt#query SentinelAlertRuleNrt#query}.'''
        result = self._values.get("query")
        assert result is not None, "Required property 'query' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def severity(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_alert_rule_nrt#severity SentinelAlertRuleNrt#severity}.'''
        result = self._values.get("severity")
        assert result is not None, "Required property 'severity' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def alert_details_override(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SentinelAlertRuleNrtAlertDetailsOverride]]]:
        '''alert_details_override block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_alert_rule_nrt#alert_details_override SentinelAlertRuleNrt#alert_details_override}
        '''
        result = self._values.get("alert_details_override")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SentinelAlertRuleNrtAlertDetailsOverride]]], result)

    @builtins.property
    def alert_rule_template_guid(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_alert_rule_nrt#alert_rule_template_guid SentinelAlertRuleNrt#alert_rule_template_guid}.'''
        result = self._values.get("alert_rule_template_guid")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def alert_rule_template_version(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_alert_rule_nrt#alert_rule_template_version SentinelAlertRuleNrt#alert_rule_template_version}.'''
        result = self._values.get("alert_rule_template_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def custom_details(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_alert_rule_nrt#custom_details SentinelAlertRuleNrt#custom_details}.'''
        result = self._values.get("custom_details")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_alert_rule_nrt#description SentinelAlertRuleNrt#description}.'''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_alert_rule_nrt#enabled SentinelAlertRuleNrt#enabled}.'''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def entity_mapping(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SentinelAlertRuleNrtEntityMapping"]]]:
        '''entity_mapping block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_alert_rule_nrt#entity_mapping SentinelAlertRuleNrt#entity_mapping}
        '''
        result = self._values.get("entity_mapping")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SentinelAlertRuleNrtEntityMapping"]]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_alert_rule_nrt#id SentinelAlertRuleNrt#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def incident(self) -> typing.Optional["SentinelAlertRuleNrtIncident"]:
        '''incident block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_alert_rule_nrt#incident SentinelAlertRuleNrt#incident}
        '''
        result = self._values.get("incident")
        return typing.cast(typing.Optional["SentinelAlertRuleNrtIncident"], result)

    @builtins.property
    def sentinel_entity_mapping(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SentinelAlertRuleNrtSentinelEntityMapping"]]]:
        '''sentinel_entity_mapping block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_alert_rule_nrt#sentinel_entity_mapping SentinelAlertRuleNrt#sentinel_entity_mapping}
        '''
        result = self._values.get("sentinel_entity_mapping")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SentinelAlertRuleNrtSentinelEntityMapping"]]], result)

    @builtins.property
    def suppression_duration(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_alert_rule_nrt#suppression_duration SentinelAlertRuleNrt#suppression_duration}.'''
        result = self._values.get("suppression_duration")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def suppression_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_alert_rule_nrt#suppression_enabled SentinelAlertRuleNrt#suppression_enabled}.'''
        result = self._values.get("suppression_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def tactics(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_alert_rule_nrt#tactics SentinelAlertRuleNrt#tactics}.'''
        result = self._values.get("tactics")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def techniques(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_alert_rule_nrt#techniques SentinelAlertRuleNrt#techniques}.'''
        result = self._values.get("techniques")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["SentinelAlertRuleNrtTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_alert_rule_nrt#timeouts SentinelAlertRuleNrt#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["SentinelAlertRuleNrtTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SentinelAlertRuleNrtConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.sentinelAlertRuleNrt.SentinelAlertRuleNrtEntityMapping",
    jsii_struct_bases=[],
    name_mapping={"entity_type": "entityType", "field_mapping": "fieldMapping"},
)
class SentinelAlertRuleNrtEntityMapping:
    def __init__(
        self,
        *,
        entity_type: builtins.str,
        field_mapping: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SentinelAlertRuleNrtEntityMappingFieldMapping", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param entity_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_alert_rule_nrt#entity_type SentinelAlertRuleNrt#entity_type}.
        :param field_mapping: field_mapping block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_alert_rule_nrt#field_mapping SentinelAlertRuleNrt#field_mapping}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__87b0f288f1aa364d86e5ccfe68a6e6a4cc2663f79b13f29e44434a4c8c4b2465)
            check_type(argname="argument entity_type", value=entity_type, expected_type=type_hints["entity_type"])
            check_type(argname="argument field_mapping", value=field_mapping, expected_type=type_hints["field_mapping"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "entity_type": entity_type,
            "field_mapping": field_mapping,
        }

    @builtins.property
    def entity_type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_alert_rule_nrt#entity_type SentinelAlertRuleNrt#entity_type}.'''
        result = self._values.get("entity_type")
        assert result is not None, "Required property 'entity_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def field_mapping(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SentinelAlertRuleNrtEntityMappingFieldMapping"]]:
        '''field_mapping block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_alert_rule_nrt#field_mapping SentinelAlertRuleNrt#field_mapping}
        '''
        result = self._values.get("field_mapping")
        assert result is not None, "Required property 'field_mapping' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SentinelAlertRuleNrtEntityMappingFieldMapping"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SentinelAlertRuleNrtEntityMapping(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.sentinelAlertRuleNrt.SentinelAlertRuleNrtEntityMappingFieldMapping",
    jsii_struct_bases=[],
    name_mapping={"column_name": "columnName", "identifier": "identifier"},
)
class SentinelAlertRuleNrtEntityMappingFieldMapping:
    def __init__(self, *, column_name: builtins.str, identifier: builtins.str) -> None:
        '''
        :param column_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_alert_rule_nrt#column_name SentinelAlertRuleNrt#column_name}.
        :param identifier: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_alert_rule_nrt#identifier SentinelAlertRuleNrt#identifier}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3d14f19d3b4fa1eb4d0c364496fbb9d9242c2dddb9b50e63bd05ed2196abaf00)
            check_type(argname="argument column_name", value=column_name, expected_type=type_hints["column_name"])
            check_type(argname="argument identifier", value=identifier, expected_type=type_hints["identifier"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "column_name": column_name,
            "identifier": identifier,
        }

    @builtins.property
    def column_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_alert_rule_nrt#column_name SentinelAlertRuleNrt#column_name}.'''
        result = self._values.get("column_name")
        assert result is not None, "Required property 'column_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def identifier(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_alert_rule_nrt#identifier SentinelAlertRuleNrt#identifier}.'''
        result = self._values.get("identifier")
        assert result is not None, "Required property 'identifier' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SentinelAlertRuleNrtEntityMappingFieldMapping(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SentinelAlertRuleNrtEntityMappingFieldMappingList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.sentinelAlertRuleNrt.SentinelAlertRuleNrtEntityMappingFieldMappingList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ca7a8b6016b7435d83c7725c8d4c2d6c89f6fde8c6372e24ef3b8465daa40cf5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "SentinelAlertRuleNrtEntityMappingFieldMappingOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__96d03d6850298c7a8b4033b12eca3b4b3c5b3cf140c13384dfc8cc36932b5a3d)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("SentinelAlertRuleNrtEntityMappingFieldMappingOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__791b6d3ae51ea28f7c10dbe701ad10046fbe39e338ab2245222dd0313a965417)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6bd02e2a81cc84eaafeeff1a1ed6cc114a1d6d5e5028bcadf0319fe03649c7c8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__213eb1fa921a4ac7584345aae052f82a62b287dbba97579bf478fbca69bae9c4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SentinelAlertRuleNrtEntityMappingFieldMapping]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SentinelAlertRuleNrtEntityMappingFieldMapping]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SentinelAlertRuleNrtEntityMappingFieldMapping]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cdc4d73f5432aa06cd40d70b0faf8297c376a960d09329f9129a0dae44260d30)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class SentinelAlertRuleNrtEntityMappingFieldMappingOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.sentinelAlertRuleNrt.SentinelAlertRuleNrtEntityMappingFieldMappingOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9c119db0e51d982ca62f11438ee8cf103109bb3653681a8f88e2e2ac34c38f82)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="columnNameInput")
    def column_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "columnNameInput"))

    @builtins.property
    @jsii.member(jsii_name="identifierInput")
    def identifier_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "identifierInput"))

    @builtins.property
    @jsii.member(jsii_name="columnName")
    def column_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "columnName"))

    @column_name.setter
    def column_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d152a435a31f886fa63c55df6e3f2ff9ca5f3c49b80341e6076b6c73aec73fc2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "columnName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="identifier")
    def identifier(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "identifier"))

    @identifier.setter
    def identifier(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fb6dc385a2375a866e99fc8874e1cff1b3619a0904e6ff22e531d930c881f4ac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "identifier", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SentinelAlertRuleNrtEntityMappingFieldMapping]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SentinelAlertRuleNrtEntityMappingFieldMapping]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SentinelAlertRuleNrtEntityMappingFieldMapping]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cb0936ab2095ce00147398962f443aecf42cc5e8be885543a87759bfc3dd1642)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class SentinelAlertRuleNrtEntityMappingList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.sentinelAlertRuleNrt.SentinelAlertRuleNrtEntityMappingList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a00d2c0a678075bfcc9e5b4ee1ab07ae60030da31071fbc052a7c76413958d08)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "SentinelAlertRuleNrtEntityMappingOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3d91bc38f44207cde23a7394cada382db91b9ec598ab5854f2516811e2b656a1)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("SentinelAlertRuleNrtEntityMappingOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__66e19e25ba65acb3d83b7d519cc4c60740ae421bff88674fd167971aa28f6354)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e585fb96fdca5a9c501d5b2085ee6d3218a5ba98dc7e0aea54feabde71212088)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ae27abab29e47e4756def0b702a1e8408c6e743789f9b57dba6eb033076ea3ab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SentinelAlertRuleNrtEntityMapping]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SentinelAlertRuleNrtEntityMapping]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SentinelAlertRuleNrtEntityMapping]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__538f6fda356549c531d220cce9d59f549c19dbda93394e4a787a0e1e81019afe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class SentinelAlertRuleNrtEntityMappingOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.sentinelAlertRuleNrt.SentinelAlertRuleNrtEntityMappingOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0b06596c44b0c57d798b07e44a266d31ebeed135a6ce801802190c822222694a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putFieldMapping")
    def put_field_mapping(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SentinelAlertRuleNrtEntityMappingFieldMapping, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__de277832eb613411d63bda4b85bf8b7aa4f4fe6e7e6baf76dac571e61e662c76)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putFieldMapping", [value]))

    @builtins.property
    @jsii.member(jsii_name="fieldMapping")
    def field_mapping(self) -> SentinelAlertRuleNrtEntityMappingFieldMappingList:
        return typing.cast(SentinelAlertRuleNrtEntityMappingFieldMappingList, jsii.get(self, "fieldMapping"))

    @builtins.property
    @jsii.member(jsii_name="entityTypeInput")
    def entity_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "entityTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="fieldMappingInput")
    def field_mapping_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SentinelAlertRuleNrtEntityMappingFieldMapping]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SentinelAlertRuleNrtEntityMappingFieldMapping]]], jsii.get(self, "fieldMappingInput"))

    @builtins.property
    @jsii.member(jsii_name="entityType")
    def entity_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "entityType"))

    @entity_type.setter
    def entity_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ddf8640633bd5bf3a303dc5f30771788474e2a3a79353e28cb1a1013bf71d178)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "entityType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SentinelAlertRuleNrtEntityMapping]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SentinelAlertRuleNrtEntityMapping]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SentinelAlertRuleNrtEntityMapping]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd80c2da03483c235c5731adfc7dfd89b22935988268964ceda37f4184abc072)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.sentinelAlertRuleNrt.SentinelAlertRuleNrtEventGrouping",
    jsii_struct_bases=[],
    name_mapping={"aggregation_method": "aggregationMethod"},
)
class SentinelAlertRuleNrtEventGrouping:
    def __init__(self, *, aggregation_method: builtins.str) -> None:
        '''
        :param aggregation_method: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_alert_rule_nrt#aggregation_method SentinelAlertRuleNrt#aggregation_method}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7ba1a9e8d2ad2414e3042750f659cfc348edfaa57aeaf492dde4b998eedc52ca)
            check_type(argname="argument aggregation_method", value=aggregation_method, expected_type=type_hints["aggregation_method"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "aggregation_method": aggregation_method,
        }

    @builtins.property
    def aggregation_method(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_alert_rule_nrt#aggregation_method SentinelAlertRuleNrt#aggregation_method}.'''
        result = self._values.get("aggregation_method")
        assert result is not None, "Required property 'aggregation_method' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SentinelAlertRuleNrtEventGrouping(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SentinelAlertRuleNrtEventGroupingOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.sentinelAlertRuleNrt.SentinelAlertRuleNrtEventGroupingOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0e8eac6cc60839267bd65c6a1b344c927e0b541ba213b10282b4c86efeb06d8a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="aggregationMethodInput")
    def aggregation_method_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "aggregationMethodInput"))

    @builtins.property
    @jsii.member(jsii_name="aggregationMethod")
    def aggregation_method(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "aggregationMethod"))

    @aggregation_method.setter
    def aggregation_method(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8a30cc8c9a64c98e7274b6f7c09c872c64c94991c0258fc39fd621db0b48c01d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "aggregationMethod", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[SentinelAlertRuleNrtEventGrouping]:
        return typing.cast(typing.Optional[SentinelAlertRuleNrtEventGrouping], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SentinelAlertRuleNrtEventGrouping],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5af4b0148da7a16ba1a9ff86e758d4c5bb5ee6f365db83215bec727e3da36670)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.sentinelAlertRuleNrt.SentinelAlertRuleNrtIncident",
    jsii_struct_bases=[],
    name_mapping={
        "create_incident_enabled": "createIncidentEnabled",
        "grouping": "grouping",
    },
)
class SentinelAlertRuleNrtIncident:
    def __init__(
        self,
        *,
        create_incident_enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        grouping: typing.Union["SentinelAlertRuleNrtIncidentGrouping", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param create_incident_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_alert_rule_nrt#create_incident_enabled SentinelAlertRuleNrt#create_incident_enabled}.
        :param grouping: grouping block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_alert_rule_nrt#grouping SentinelAlertRuleNrt#grouping}
        '''
        if isinstance(grouping, dict):
            grouping = SentinelAlertRuleNrtIncidentGrouping(**grouping)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c6429b74873fdd357733100598eb1330eba19ad265e3a5453e9c7a6d5997a29)
            check_type(argname="argument create_incident_enabled", value=create_incident_enabled, expected_type=type_hints["create_incident_enabled"])
            check_type(argname="argument grouping", value=grouping, expected_type=type_hints["grouping"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "create_incident_enabled": create_incident_enabled,
            "grouping": grouping,
        }

    @builtins.property
    def create_incident_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_alert_rule_nrt#create_incident_enabled SentinelAlertRuleNrt#create_incident_enabled}.'''
        result = self._values.get("create_incident_enabled")
        assert result is not None, "Required property 'create_incident_enabled' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    @builtins.property
    def grouping(self) -> "SentinelAlertRuleNrtIncidentGrouping":
        '''grouping block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_alert_rule_nrt#grouping SentinelAlertRuleNrt#grouping}
        '''
        result = self._values.get("grouping")
        assert result is not None, "Required property 'grouping' is missing"
        return typing.cast("SentinelAlertRuleNrtIncidentGrouping", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SentinelAlertRuleNrtIncident(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.sentinelAlertRuleNrt.SentinelAlertRuleNrtIncidentGrouping",
    jsii_struct_bases=[],
    name_mapping={
        "by_alert_details": "byAlertDetails",
        "by_custom_details": "byCustomDetails",
        "by_entities": "byEntities",
        "enabled": "enabled",
        "entity_matching_method": "entityMatchingMethod",
        "lookback_duration": "lookbackDuration",
        "reopen_closed_incidents": "reopenClosedIncidents",
    },
)
class SentinelAlertRuleNrtIncidentGrouping:
    def __init__(
        self,
        *,
        by_alert_details: typing.Optional[typing.Sequence[builtins.str]] = None,
        by_custom_details: typing.Optional[typing.Sequence[builtins.str]] = None,
        by_entities: typing.Optional[typing.Sequence[builtins.str]] = None,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        entity_matching_method: typing.Optional[builtins.str] = None,
        lookback_duration: typing.Optional[builtins.str] = None,
        reopen_closed_incidents: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param by_alert_details: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_alert_rule_nrt#by_alert_details SentinelAlertRuleNrt#by_alert_details}.
        :param by_custom_details: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_alert_rule_nrt#by_custom_details SentinelAlertRuleNrt#by_custom_details}.
        :param by_entities: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_alert_rule_nrt#by_entities SentinelAlertRuleNrt#by_entities}.
        :param enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_alert_rule_nrt#enabled SentinelAlertRuleNrt#enabled}.
        :param entity_matching_method: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_alert_rule_nrt#entity_matching_method SentinelAlertRuleNrt#entity_matching_method}.
        :param lookback_duration: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_alert_rule_nrt#lookback_duration SentinelAlertRuleNrt#lookback_duration}.
        :param reopen_closed_incidents: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_alert_rule_nrt#reopen_closed_incidents SentinelAlertRuleNrt#reopen_closed_incidents}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fd39019482a6b64f0dd855e7bafd73c9f09361f10f267af2233c2da75ba8c442)
            check_type(argname="argument by_alert_details", value=by_alert_details, expected_type=type_hints["by_alert_details"])
            check_type(argname="argument by_custom_details", value=by_custom_details, expected_type=type_hints["by_custom_details"])
            check_type(argname="argument by_entities", value=by_entities, expected_type=type_hints["by_entities"])
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument entity_matching_method", value=entity_matching_method, expected_type=type_hints["entity_matching_method"])
            check_type(argname="argument lookback_duration", value=lookback_duration, expected_type=type_hints["lookback_duration"])
            check_type(argname="argument reopen_closed_incidents", value=reopen_closed_incidents, expected_type=type_hints["reopen_closed_incidents"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if by_alert_details is not None:
            self._values["by_alert_details"] = by_alert_details
        if by_custom_details is not None:
            self._values["by_custom_details"] = by_custom_details
        if by_entities is not None:
            self._values["by_entities"] = by_entities
        if enabled is not None:
            self._values["enabled"] = enabled
        if entity_matching_method is not None:
            self._values["entity_matching_method"] = entity_matching_method
        if lookback_duration is not None:
            self._values["lookback_duration"] = lookback_duration
        if reopen_closed_incidents is not None:
            self._values["reopen_closed_incidents"] = reopen_closed_incidents

    @builtins.property
    def by_alert_details(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_alert_rule_nrt#by_alert_details SentinelAlertRuleNrt#by_alert_details}.'''
        result = self._values.get("by_alert_details")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def by_custom_details(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_alert_rule_nrt#by_custom_details SentinelAlertRuleNrt#by_custom_details}.'''
        result = self._values.get("by_custom_details")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def by_entities(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_alert_rule_nrt#by_entities SentinelAlertRuleNrt#by_entities}.'''
        result = self._values.get("by_entities")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_alert_rule_nrt#enabled SentinelAlertRuleNrt#enabled}.'''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def entity_matching_method(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_alert_rule_nrt#entity_matching_method SentinelAlertRuleNrt#entity_matching_method}.'''
        result = self._values.get("entity_matching_method")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def lookback_duration(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_alert_rule_nrt#lookback_duration SentinelAlertRuleNrt#lookback_duration}.'''
        result = self._values.get("lookback_duration")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def reopen_closed_incidents(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_alert_rule_nrt#reopen_closed_incidents SentinelAlertRuleNrt#reopen_closed_incidents}.'''
        result = self._values.get("reopen_closed_incidents")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SentinelAlertRuleNrtIncidentGrouping(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SentinelAlertRuleNrtIncidentGroupingOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.sentinelAlertRuleNrt.SentinelAlertRuleNrtIncidentGroupingOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bc497597443ae8166cfe6ec3284f8c8aef528196bd0d5d7a6326254f0cd23643)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetByAlertDetails")
    def reset_by_alert_details(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetByAlertDetails", []))

    @jsii.member(jsii_name="resetByCustomDetails")
    def reset_by_custom_details(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetByCustomDetails", []))

    @jsii.member(jsii_name="resetByEntities")
    def reset_by_entities(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetByEntities", []))

    @jsii.member(jsii_name="resetEnabled")
    def reset_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnabled", []))

    @jsii.member(jsii_name="resetEntityMatchingMethod")
    def reset_entity_matching_method(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEntityMatchingMethod", []))

    @jsii.member(jsii_name="resetLookbackDuration")
    def reset_lookback_duration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLookbackDuration", []))

    @jsii.member(jsii_name="resetReopenClosedIncidents")
    def reset_reopen_closed_incidents(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetReopenClosedIncidents", []))

    @builtins.property
    @jsii.member(jsii_name="byAlertDetailsInput")
    def by_alert_details_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "byAlertDetailsInput"))

    @builtins.property
    @jsii.member(jsii_name="byCustomDetailsInput")
    def by_custom_details_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "byCustomDetailsInput"))

    @builtins.property
    @jsii.member(jsii_name="byEntitiesInput")
    def by_entities_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "byEntitiesInput"))

    @builtins.property
    @jsii.member(jsii_name="enabledInput")
    def enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enabledInput"))

    @builtins.property
    @jsii.member(jsii_name="entityMatchingMethodInput")
    def entity_matching_method_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "entityMatchingMethodInput"))

    @builtins.property
    @jsii.member(jsii_name="lookbackDurationInput")
    def lookback_duration_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "lookbackDurationInput"))

    @builtins.property
    @jsii.member(jsii_name="reopenClosedIncidentsInput")
    def reopen_closed_incidents_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "reopenClosedIncidentsInput"))

    @builtins.property
    @jsii.member(jsii_name="byAlertDetails")
    def by_alert_details(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "byAlertDetails"))

    @by_alert_details.setter
    def by_alert_details(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8687a6c4cb29109d3a2e0f11c9e0f1334f45949123c9a9d5ef9c0b40bd9cd54e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "byAlertDetails", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="byCustomDetails")
    def by_custom_details(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "byCustomDetails"))

    @by_custom_details.setter
    def by_custom_details(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__75b927b91a64fa35c44d73a90d20e7e88f8b60e43f57dc03111a548147bc708a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "byCustomDetails", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="byEntities")
    def by_entities(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "byEntities"))

    @by_entities.setter
    def by_entities(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__433792dcc1258aee8cf8b8ebca91c510085209b6d0bb1ac18285edf8e1930e68)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "byEntities", value) # pyright: ignore[reportArgumentType]

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
            type_hints = typing.get_type_hints(_typecheckingstub__043a6354d8f16cb5fbf8d4f0e8496bf65a15bd9563a16a8729fb4c71fc2b8b79)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="entityMatchingMethod")
    def entity_matching_method(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "entityMatchingMethod"))

    @entity_matching_method.setter
    def entity_matching_method(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3214588d819abe8b4bf30894995f30344d826991ed786a55d429f34a3e0518c7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "entityMatchingMethod", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="lookbackDuration")
    def lookback_duration(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "lookbackDuration"))

    @lookback_duration.setter
    def lookback_duration(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1073fe36ae3a9cb761b34924ef19b76a38f20fc5a567379f4551e940ec08aae6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "lookbackDuration", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="reopenClosedIncidents")
    def reopen_closed_incidents(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "reopenClosedIncidents"))

    @reopen_closed_incidents.setter
    def reopen_closed_incidents(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dde6df3fc8fbd871491388a327f5f7e6af9ba8a89ce0006a5b4a9288d6a4e2f2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "reopenClosedIncidents", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[SentinelAlertRuleNrtIncidentGrouping]:
        return typing.cast(typing.Optional[SentinelAlertRuleNrtIncidentGrouping], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SentinelAlertRuleNrtIncidentGrouping],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8321be78e884b5e767cda271ce0c00e6dafe78b836e2618e3b5269eaffe1c88d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class SentinelAlertRuleNrtIncidentOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.sentinelAlertRuleNrt.SentinelAlertRuleNrtIncidentOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e7bf1c489697b1255749df56441a27e81fe7d5b8ae5f407ec8c0facffb3dc4bc)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putGrouping")
    def put_grouping(
        self,
        *,
        by_alert_details: typing.Optional[typing.Sequence[builtins.str]] = None,
        by_custom_details: typing.Optional[typing.Sequence[builtins.str]] = None,
        by_entities: typing.Optional[typing.Sequence[builtins.str]] = None,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        entity_matching_method: typing.Optional[builtins.str] = None,
        lookback_duration: typing.Optional[builtins.str] = None,
        reopen_closed_incidents: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param by_alert_details: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_alert_rule_nrt#by_alert_details SentinelAlertRuleNrt#by_alert_details}.
        :param by_custom_details: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_alert_rule_nrt#by_custom_details SentinelAlertRuleNrt#by_custom_details}.
        :param by_entities: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_alert_rule_nrt#by_entities SentinelAlertRuleNrt#by_entities}.
        :param enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_alert_rule_nrt#enabled SentinelAlertRuleNrt#enabled}.
        :param entity_matching_method: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_alert_rule_nrt#entity_matching_method SentinelAlertRuleNrt#entity_matching_method}.
        :param lookback_duration: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_alert_rule_nrt#lookback_duration SentinelAlertRuleNrt#lookback_duration}.
        :param reopen_closed_incidents: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_alert_rule_nrt#reopen_closed_incidents SentinelAlertRuleNrt#reopen_closed_incidents}.
        '''
        value = SentinelAlertRuleNrtIncidentGrouping(
            by_alert_details=by_alert_details,
            by_custom_details=by_custom_details,
            by_entities=by_entities,
            enabled=enabled,
            entity_matching_method=entity_matching_method,
            lookback_duration=lookback_duration,
            reopen_closed_incidents=reopen_closed_incidents,
        )

        return typing.cast(None, jsii.invoke(self, "putGrouping", [value]))

    @builtins.property
    @jsii.member(jsii_name="grouping")
    def grouping(self) -> SentinelAlertRuleNrtIncidentGroupingOutputReference:
        return typing.cast(SentinelAlertRuleNrtIncidentGroupingOutputReference, jsii.get(self, "grouping"))

    @builtins.property
    @jsii.member(jsii_name="createIncidentEnabledInput")
    def create_incident_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "createIncidentEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="groupingInput")
    def grouping_input(self) -> typing.Optional[SentinelAlertRuleNrtIncidentGrouping]:
        return typing.cast(typing.Optional[SentinelAlertRuleNrtIncidentGrouping], jsii.get(self, "groupingInput"))

    @builtins.property
    @jsii.member(jsii_name="createIncidentEnabled")
    def create_incident_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "createIncidentEnabled"))

    @create_incident_enabled.setter
    def create_incident_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c26e8e48ba77fc58ddaa71fdb138f1b93de1e09e2ba3cd72ccbc5af295f1598c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "createIncidentEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[SentinelAlertRuleNrtIncident]:
        return typing.cast(typing.Optional[SentinelAlertRuleNrtIncident], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SentinelAlertRuleNrtIncident],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c86e480106f851c5e49b14b1de153e20cffc05c9dfa7ccfb22e7307c98643271)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.sentinelAlertRuleNrt.SentinelAlertRuleNrtSentinelEntityMapping",
    jsii_struct_bases=[],
    name_mapping={"column_name": "columnName"},
)
class SentinelAlertRuleNrtSentinelEntityMapping:
    def __init__(self, *, column_name: builtins.str) -> None:
        '''
        :param column_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_alert_rule_nrt#column_name SentinelAlertRuleNrt#column_name}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b6f31e3939e3f84d6752ec66d83be06ca7a057ff7db6ba5444675aeb72baf18a)
            check_type(argname="argument column_name", value=column_name, expected_type=type_hints["column_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "column_name": column_name,
        }

    @builtins.property
    def column_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_alert_rule_nrt#column_name SentinelAlertRuleNrt#column_name}.'''
        result = self._values.get("column_name")
        assert result is not None, "Required property 'column_name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SentinelAlertRuleNrtSentinelEntityMapping(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SentinelAlertRuleNrtSentinelEntityMappingList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.sentinelAlertRuleNrt.SentinelAlertRuleNrtSentinelEntityMappingList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c60caa37bb9e457349486003e8f83bec54246985d8d72d15c86cbb7c4e98f691)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "SentinelAlertRuleNrtSentinelEntityMappingOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c9fba8ced5a28517987ea964d2446f80527948d347571a7d6b5ddbfd39450b1a)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("SentinelAlertRuleNrtSentinelEntityMappingOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__33c1b9a8fabfa125baba50d71a15a03b0bcf5837a829d89421012e3c2fb32aa0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__db23e2070f0d527bb41aa723f1aab41fbf4f0881b4967bbc009d5c31349ac58d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7a700be192dc0306c659e1dbcf50c7c18a1d4dc13c633a04602e8309577c6200)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SentinelAlertRuleNrtSentinelEntityMapping]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SentinelAlertRuleNrtSentinelEntityMapping]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SentinelAlertRuleNrtSentinelEntityMapping]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fce7730dedfc625cc7dc7afb59219914ff1cfbbfe0fc9c64778cc0af144cd744)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class SentinelAlertRuleNrtSentinelEntityMappingOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.sentinelAlertRuleNrt.SentinelAlertRuleNrtSentinelEntityMappingOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a286c9750382a80baaf3829b83ad78e4e12ef464eaec85ec59a3bbd4b2b90602)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="columnNameInput")
    def column_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "columnNameInput"))

    @builtins.property
    @jsii.member(jsii_name="columnName")
    def column_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "columnName"))

    @column_name.setter
    def column_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5d6a6d24d434198e0b324ee5c9ee88ed24442de1e93f7da1932c37b2e6314bf7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "columnName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SentinelAlertRuleNrtSentinelEntityMapping]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SentinelAlertRuleNrtSentinelEntityMapping]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SentinelAlertRuleNrtSentinelEntityMapping]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f173bd9c1e526e674a9fa1a0b6b5c609a5f46055154d53d8b2992056cae7ded1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.sentinelAlertRuleNrt.SentinelAlertRuleNrtTimeouts",
    jsii_struct_bases=[],
    name_mapping={
        "create": "create",
        "delete": "delete",
        "read": "read",
        "update": "update",
    },
)
class SentinelAlertRuleNrtTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_alert_rule_nrt#create SentinelAlertRuleNrt#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_alert_rule_nrt#delete SentinelAlertRuleNrt#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_alert_rule_nrt#read SentinelAlertRuleNrt#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_alert_rule_nrt#update SentinelAlertRuleNrt#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__00b2a5f446a2f081f728524d4690f51e090c70eb0bd694c54429e2cbd61a9cad)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_alert_rule_nrt#create SentinelAlertRuleNrt#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_alert_rule_nrt#delete SentinelAlertRuleNrt#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def read(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_alert_rule_nrt#read SentinelAlertRuleNrt#read}.'''
        result = self._values.get("read")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_alert_rule_nrt#update SentinelAlertRuleNrt#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SentinelAlertRuleNrtTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SentinelAlertRuleNrtTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.sentinelAlertRuleNrt.SentinelAlertRuleNrtTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__dc229f167a0b3b34b6b971ecee6adc903e5d70e9073fbb1b2b585312fd3b0998)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f836006ba4a6de04b856b857da0522f6a62a56b0287272ec12f7929e39b395b6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0bd3ffd16edd41a00eabe75fd27f38f54d19ed7d08ba1e7198ae37d7c4bfcc11)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="read")
    def read(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "read"))

    @read.setter
    def read(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__42a2672153d54cb976cab9c76e0c280e12aa7612e297dae57eef99ab20b9b78e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "read", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__480ef2fdc6a820b05715fea569079fbdcf465bd7db389d10cf0f89841055e7d2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SentinelAlertRuleNrtTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SentinelAlertRuleNrtTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SentinelAlertRuleNrtTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a06d815f4b0f487ae3ba262585940832bda85d432405b31fada33ffe3e8bb8b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "SentinelAlertRuleNrt",
    "SentinelAlertRuleNrtAlertDetailsOverride",
    "SentinelAlertRuleNrtAlertDetailsOverrideDynamicProperty",
    "SentinelAlertRuleNrtAlertDetailsOverrideDynamicPropertyList",
    "SentinelAlertRuleNrtAlertDetailsOverrideDynamicPropertyOutputReference",
    "SentinelAlertRuleNrtAlertDetailsOverrideList",
    "SentinelAlertRuleNrtAlertDetailsOverrideOutputReference",
    "SentinelAlertRuleNrtConfig",
    "SentinelAlertRuleNrtEntityMapping",
    "SentinelAlertRuleNrtEntityMappingFieldMapping",
    "SentinelAlertRuleNrtEntityMappingFieldMappingList",
    "SentinelAlertRuleNrtEntityMappingFieldMappingOutputReference",
    "SentinelAlertRuleNrtEntityMappingList",
    "SentinelAlertRuleNrtEntityMappingOutputReference",
    "SentinelAlertRuleNrtEventGrouping",
    "SentinelAlertRuleNrtEventGroupingOutputReference",
    "SentinelAlertRuleNrtIncident",
    "SentinelAlertRuleNrtIncidentGrouping",
    "SentinelAlertRuleNrtIncidentGroupingOutputReference",
    "SentinelAlertRuleNrtIncidentOutputReference",
    "SentinelAlertRuleNrtSentinelEntityMapping",
    "SentinelAlertRuleNrtSentinelEntityMappingList",
    "SentinelAlertRuleNrtSentinelEntityMappingOutputReference",
    "SentinelAlertRuleNrtTimeouts",
    "SentinelAlertRuleNrtTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__bfbaa88fe7e2a9dc64067329ed8c574fd89e3cb4a5f2ed4f136a36964efd974e(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    display_name: builtins.str,
    event_grouping: typing.Union[SentinelAlertRuleNrtEventGrouping, typing.Dict[builtins.str, typing.Any]],
    log_analytics_workspace_id: builtins.str,
    name: builtins.str,
    query: builtins.str,
    severity: builtins.str,
    alert_details_override: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SentinelAlertRuleNrtAlertDetailsOverride, typing.Dict[builtins.str, typing.Any]]]]] = None,
    alert_rule_template_guid: typing.Optional[builtins.str] = None,
    alert_rule_template_version: typing.Optional[builtins.str] = None,
    custom_details: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    description: typing.Optional[builtins.str] = None,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    entity_mapping: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SentinelAlertRuleNrtEntityMapping, typing.Dict[builtins.str, typing.Any]]]]] = None,
    id: typing.Optional[builtins.str] = None,
    incident: typing.Optional[typing.Union[SentinelAlertRuleNrtIncident, typing.Dict[builtins.str, typing.Any]]] = None,
    sentinel_entity_mapping: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SentinelAlertRuleNrtSentinelEntityMapping, typing.Dict[builtins.str, typing.Any]]]]] = None,
    suppression_duration: typing.Optional[builtins.str] = None,
    suppression_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    tactics: typing.Optional[typing.Sequence[builtins.str]] = None,
    techniques: typing.Optional[typing.Sequence[builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[SentinelAlertRuleNrtTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__5df39870b373f86babd0c09ab76ca498d33896fc56d449ff10f0738f8ad8971f(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d52e84e64a22d075c64dbc38327d763e95ac60106e42d5d8b4a8420c35e7e11(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SentinelAlertRuleNrtAlertDetailsOverride, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa4a3534b020c49f1421955bbc402f224db7a244535f28c293da4ea8ed202d4f(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SentinelAlertRuleNrtEntityMapping, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8aaca0f95fae7566b6a576b284f803a5b66f55e55720fbf90bc325bf9c42690e(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SentinelAlertRuleNrtSentinelEntityMapping, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f80c7c8dd3c129bb0eec89322aa268786835d1c2c9d1ba1ddb7bf881954804a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0889127053c3f81e80eef5f658e9d4e86ca92295dd87553b218ad5d358ade96(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e816787399352b8a3e7db4891417f4fa0010df96d064f6bd3b88ea584a454f5f(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2fd708d4a9222d9de71abd958b289a1e24184f61e313c56b81b2510ef5f874c4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf2c3c73192e69d08e681fca07b43ea787ae9743d2a6d9fafb265174ce27a07f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00b564a80c7c23f8f73e3546f2e4133d0041a94a0f40ca3f06ae71747ee023ca(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8eff7f1b152fd39e7df93cbfff933b04fc4390c77edcb8975edf803bef223d4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f78d2dceeb9c203f4987f9c3b547725248445ab9b99a6fbdf392da852b2326a1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cbb452ccbfcd5a354eeb5ff24a2a2fa9f07ae91638198c56fe4de2a1b96e3daa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca089963f0dc95d6702cb27928ffae60dd9a4cb84a999cf4ed84943afb826ca6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c02688e6e5602e4a97e96a8240914e245d74144ea295686bbf04a37a8093cfc4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0f0175597a97240ebcd6645b2a7f72cb88f617c0b862a931bd3011866c2fdae(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24d167e32f4aa42c10150eaab63119cdcce81e95fe9937032ecc94d8b91b54d0(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73e9e5f346102d8d836409b3542644c002402d767c546ce17c541bacf2e6f84f(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b783bfdd21834181cf70a0a298541652dd16c9ab301344d7fc6c8698eba694c(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f4c1c0f00bcb6b905d0b3b13374bee1b8252b45b2dd3b100814631bad7aeccf(
    *,
    description_format: typing.Optional[builtins.str] = None,
    display_name_format: typing.Optional[builtins.str] = None,
    dynamic_property: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SentinelAlertRuleNrtAlertDetailsOverrideDynamicProperty, typing.Dict[builtins.str, typing.Any]]]]] = None,
    severity_column_name: typing.Optional[builtins.str] = None,
    tactics_column_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3c0bec216e206ad5adbb4073b89cd5e00e4d11dec2c474e256021994ad662ca(
    *,
    name: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67536f98ed031f6975d3bf155cde7718d8d89d3e49a210290232e7531d79dc7b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9cfd43c97f2b4ffc4b24e935505d5fb8de066714091eb0c9d9d796b2172a62b6(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b709c51164d5fe1091f915aea7de95dee880c57ab6de77320fcca98fc552edad(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ae2acdf59073dce1a516713b3dbada1b055c05f6722d61ff35d789e979ce2c8(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1171cdcd664e2111ac46005cbc9cd9d28a88a0c30af1a9944655a7e62458f9ff(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__635c177988f56af3027f7754126857781a21baaebb2eda5766d202cd001701fb(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SentinelAlertRuleNrtAlertDetailsOverrideDynamicProperty]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__237107f072dd42cca0d9c86be4c8f70851f9c92ce82c9dcc171807d47a1a1e6b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dba29a3d5aed094e4c8526b74117ec6c7bdf8420e434e4a38f6bdd5103926e57(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__443b794809d808ca9cbccd4af894d643d76ca0da5d98090b2e7b60f0fa4e17b3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec5073694e7cb11a13cd586eac18995fb3fa481ae3b62bdf8a467c9fad3693bd(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SentinelAlertRuleNrtAlertDetailsOverrideDynamicProperty]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26359d17b8676b060ab33f9521e2a53918b378991ae3986eb27c4512cba18886(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e22019b16fd99e9bcf4267e1ee5c7c75eaf848d47f7c8a5ac11bb96c01af0025(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a69ed4b2e3e6e6a904a0197035667241a5f5f8a63dc7db68d05def1691f1448(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b001f62cce0518accb2dde800a20c83fc32b8a232a2781d5eb26334d46cd61a(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__84b52cbbcfcf95b711963e8a3c08b48d7774890b8d5c6c592f2286a91eb6879c(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7527afa00a19618274a13173e54a91f3cb756a4257994cceb001e823071ceca(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SentinelAlertRuleNrtAlertDetailsOverride]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05ce7389f6959015342b599a1df9b4729ff139782fd0aa91f45e27a967a09f5f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74c88ec4dc7948689f6e346dab230746a6ad09b75807b640a7d584bda2ba5d04(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SentinelAlertRuleNrtAlertDetailsOverrideDynamicProperty, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24e8fabdfc879fc5a6cb2c64ce822925212eb39af870a6da3c8a0ed9137aecf3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee7760b8a210d9aaca649c96529a387aa122782e36a3a214070822893213522e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a801893b02bcdf698e623615bb4b135431a61a60b6fa8acb0074ee05575a3d46(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a31447b0cad07616b156dfa75a9e06436ddb2989371314faca072b33822efbe7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0584a63145811b0340bfbee289284cb449a9cbadc5c52b1a22f70b4d7cdfda7d(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SentinelAlertRuleNrtAlertDetailsOverride]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__293a8328b2dc4ac66a254aa74c8b8c20f0bffe7981e9b2d6ec0a571989d825c3(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    display_name: builtins.str,
    event_grouping: typing.Union[SentinelAlertRuleNrtEventGrouping, typing.Dict[builtins.str, typing.Any]],
    log_analytics_workspace_id: builtins.str,
    name: builtins.str,
    query: builtins.str,
    severity: builtins.str,
    alert_details_override: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SentinelAlertRuleNrtAlertDetailsOverride, typing.Dict[builtins.str, typing.Any]]]]] = None,
    alert_rule_template_guid: typing.Optional[builtins.str] = None,
    alert_rule_template_version: typing.Optional[builtins.str] = None,
    custom_details: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    description: typing.Optional[builtins.str] = None,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    entity_mapping: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SentinelAlertRuleNrtEntityMapping, typing.Dict[builtins.str, typing.Any]]]]] = None,
    id: typing.Optional[builtins.str] = None,
    incident: typing.Optional[typing.Union[SentinelAlertRuleNrtIncident, typing.Dict[builtins.str, typing.Any]]] = None,
    sentinel_entity_mapping: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SentinelAlertRuleNrtSentinelEntityMapping, typing.Dict[builtins.str, typing.Any]]]]] = None,
    suppression_duration: typing.Optional[builtins.str] = None,
    suppression_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    tactics: typing.Optional[typing.Sequence[builtins.str]] = None,
    techniques: typing.Optional[typing.Sequence[builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[SentinelAlertRuleNrtTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87b0f288f1aa364d86e5ccfe68a6e6a4cc2663f79b13f29e44434a4c8c4b2465(
    *,
    entity_type: builtins.str,
    field_mapping: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SentinelAlertRuleNrtEntityMappingFieldMapping, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d14f19d3b4fa1eb4d0c364496fbb9d9242c2dddb9b50e63bd05ed2196abaf00(
    *,
    column_name: builtins.str,
    identifier: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca7a8b6016b7435d83c7725c8d4c2d6c89f6fde8c6372e24ef3b8465daa40cf5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96d03d6850298c7a8b4033b12eca3b4b3c5b3cf140c13384dfc8cc36932b5a3d(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__791b6d3ae51ea28f7c10dbe701ad10046fbe39e338ab2245222dd0313a965417(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6bd02e2a81cc84eaafeeff1a1ed6cc114a1d6d5e5028bcadf0319fe03649c7c8(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__213eb1fa921a4ac7584345aae052f82a62b287dbba97579bf478fbca69bae9c4(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cdc4d73f5432aa06cd40d70b0faf8297c376a960d09329f9129a0dae44260d30(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SentinelAlertRuleNrtEntityMappingFieldMapping]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c119db0e51d982ca62f11438ee8cf103109bb3653681a8f88e2e2ac34c38f82(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d152a435a31f886fa63c55df6e3f2ff9ca5f3c49b80341e6076b6c73aec73fc2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb6dc385a2375a866e99fc8874e1cff1b3619a0904e6ff22e531d930c881f4ac(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb0936ab2095ce00147398962f443aecf42cc5e8be885543a87759bfc3dd1642(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SentinelAlertRuleNrtEntityMappingFieldMapping]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a00d2c0a678075bfcc9e5b4ee1ab07ae60030da31071fbc052a7c76413958d08(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d91bc38f44207cde23a7394cada382db91b9ec598ab5854f2516811e2b656a1(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66e19e25ba65acb3d83b7d519cc4c60740ae421bff88674fd167971aa28f6354(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e585fb96fdca5a9c501d5b2085ee6d3218a5ba98dc7e0aea54feabde71212088(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae27abab29e47e4756def0b702a1e8408c6e743789f9b57dba6eb033076ea3ab(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__538f6fda356549c531d220cce9d59f549c19dbda93394e4a787a0e1e81019afe(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SentinelAlertRuleNrtEntityMapping]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b06596c44b0c57d798b07e44a266d31ebeed135a6ce801802190c822222694a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de277832eb613411d63bda4b85bf8b7aa4f4fe6e7e6baf76dac571e61e662c76(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SentinelAlertRuleNrtEntityMappingFieldMapping, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ddf8640633bd5bf3a303dc5f30771788474e2a3a79353e28cb1a1013bf71d178(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd80c2da03483c235c5731adfc7dfd89b22935988268964ceda37f4184abc072(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SentinelAlertRuleNrtEntityMapping]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ba1a9e8d2ad2414e3042750f659cfc348edfaa57aeaf492dde4b998eedc52ca(
    *,
    aggregation_method: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e8eac6cc60839267bd65c6a1b344c927e0b541ba213b10282b4c86efeb06d8a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a30cc8c9a64c98e7274b6f7c09c872c64c94991c0258fc39fd621db0b48c01d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5af4b0148da7a16ba1a9ff86e758d4c5bb5ee6f365db83215bec727e3da36670(
    value: typing.Optional[SentinelAlertRuleNrtEventGrouping],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c6429b74873fdd357733100598eb1330eba19ad265e3a5453e9c7a6d5997a29(
    *,
    create_incident_enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    grouping: typing.Union[SentinelAlertRuleNrtIncidentGrouping, typing.Dict[builtins.str, typing.Any]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd39019482a6b64f0dd855e7bafd73c9f09361f10f267af2233c2da75ba8c442(
    *,
    by_alert_details: typing.Optional[typing.Sequence[builtins.str]] = None,
    by_custom_details: typing.Optional[typing.Sequence[builtins.str]] = None,
    by_entities: typing.Optional[typing.Sequence[builtins.str]] = None,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    entity_matching_method: typing.Optional[builtins.str] = None,
    lookback_duration: typing.Optional[builtins.str] = None,
    reopen_closed_incidents: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc497597443ae8166cfe6ec3284f8c8aef528196bd0d5d7a6326254f0cd23643(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8687a6c4cb29109d3a2e0f11c9e0f1334f45949123c9a9d5ef9c0b40bd9cd54e(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75b927b91a64fa35c44d73a90d20e7e88f8b60e43f57dc03111a548147bc708a(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__433792dcc1258aee8cf8b8ebca91c510085209b6d0bb1ac18285edf8e1930e68(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__043a6354d8f16cb5fbf8d4f0e8496bf65a15bd9563a16a8729fb4c71fc2b8b79(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3214588d819abe8b4bf30894995f30344d826991ed786a55d429f34a3e0518c7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1073fe36ae3a9cb761b34924ef19b76a38f20fc5a567379f4551e940ec08aae6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dde6df3fc8fbd871491388a327f5f7e6af9ba8a89ce0006a5b4a9288d6a4e2f2(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8321be78e884b5e767cda271ce0c00e6dafe78b836e2618e3b5269eaffe1c88d(
    value: typing.Optional[SentinelAlertRuleNrtIncidentGrouping],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7bf1c489697b1255749df56441a27e81fe7d5b8ae5f407ec8c0facffb3dc4bc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c26e8e48ba77fc58ddaa71fdb138f1b93de1e09e2ba3cd72ccbc5af295f1598c(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c86e480106f851c5e49b14b1de153e20cffc05c9dfa7ccfb22e7307c98643271(
    value: typing.Optional[SentinelAlertRuleNrtIncident],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6f31e3939e3f84d6752ec66d83be06ca7a057ff7db6ba5444675aeb72baf18a(
    *,
    column_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c60caa37bb9e457349486003e8f83bec54246985d8d72d15c86cbb7c4e98f691(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9fba8ced5a28517987ea964d2446f80527948d347571a7d6b5ddbfd39450b1a(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33c1b9a8fabfa125baba50d71a15a03b0bcf5837a829d89421012e3c2fb32aa0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db23e2070f0d527bb41aa723f1aab41fbf4f0881b4967bbc009d5c31349ac58d(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a700be192dc0306c659e1dbcf50c7c18a1d4dc13c633a04602e8309577c6200(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fce7730dedfc625cc7dc7afb59219914ff1cfbbfe0fc9c64778cc0af144cd744(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SentinelAlertRuleNrtSentinelEntityMapping]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a286c9750382a80baaf3829b83ad78e4e12ef464eaec85ec59a3bbd4b2b90602(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d6a6d24d434198e0b324ee5c9ee88ed24442de1e93f7da1932c37b2e6314bf7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f173bd9c1e526e674a9fa1a0b6b5c609a5f46055154d53d8b2992056cae7ded1(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SentinelAlertRuleNrtSentinelEntityMapping]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00b2a5f446a2f081f728524d4690f51e090c70eb0bd694c54429e2cbd61a9cad(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    read: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc229f167a0b3b34b6b971ecee6adc903e5d70e9073fbb1b2b585312fd3b0998(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f836006ba4a6de04b856b857da0522f6a62a56b0287272ec12f7929e39b395b6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0bd3ffd16edd41a00eabe75fd27f38f54d19ed7d08ba1e7198ae37d7c4bfcc11(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42a2672153d54cb976cab9c76e0c280e12aa7612e297dae57eef99ab20b9b78e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__480ef2fdc6a820b05715fea569079fbdcf465bd7db389d10cf0f89841055e7d2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a06d815f4b0f487ae3ba262585940832bda85d432405b31fada33ffe3e8bb8b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SentinelAlertRuleNrtTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
