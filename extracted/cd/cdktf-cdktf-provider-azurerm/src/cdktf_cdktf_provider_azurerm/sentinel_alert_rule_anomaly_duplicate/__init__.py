r'''
# `azurerm_sentinel_alert_rule_anomaly_duplicate`

Refer to the Terraform Registry for docs: [`azurerm_sentinel_alert_rule_anomaly_duplicate`](https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_alert_rule_anomaly_duplicate).
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


class SentinelAlertRuleAnomalyDuplicate(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.sentinelAlertRuleAnomalyDuplicate.SentinelAlertRuleAnomalyDuplicate",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_alert_rule_anomaly_duplicate azurerm_sentinel_alert_rule_anomaly_duplicate}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        built_in_rule_id: builtins.str,
        display_name: builtins.str,
        enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        log_analytics_workspace_id: builtins.str,
        mode: builtins.str,
        id: typing.Optional[builtins.str] = None,
        multi_select_observation: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SentinelAlertRuleAnomalyDuplicateMultiSelectObservation", typing.Dict[builtins.str, typing.Any]]]]] = None,
        prioritized_exclude_observation: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SentinelAlertRuleAnomalyDuplicatePrioritizedExcludeObservation", typing.Dict[builtins.str, typing.Any]]]]] = None,
        single_select_observation: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SentinelAlertRuleAnomalyDuplicateSingleSelectObservation", typing.Dict[builtins.str, typing.Any]]]]] = None,
        threshold_observation: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SentinelAlertRuleAnomalyDuplicateThresholdObservation", typing.Dict[builtins.str, typing.Any]]]]] = None,
        timeouts: typing.Optional[typing.Union["SentinelAlertRuleAnomalyDuplicateTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_alert_rule_anomaly_duplicate azurerm_sentinel_alert_rule_anomaly_duplicate} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param built_in_rule_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_alert_rule_anomaly_duplicate#built_in_rule_id SentinelAlertRuleAnomalyDuplicate#built_in_rule_id}.
        :param display_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_alert_rule_anomaly_duplicate#display_name SentinelAlertRuleAnomalyDuplicate#display_name}.
        :param enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_alert_rule_anomaly_duplicate#enabled SentinelAlertRuleAnomalyDuplicate#enabled}.
        :param log_analytics_workspace_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_alert_rule_anomaly_duplicate#log_analytics_workspace_id SentinelAlertRuleAnomalyDuplicate#log_analytics_workspace_id}.
        :param mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_alert_rule_anomaly_duplicate#mode SentinelAlertRuleAnomalyDuplicate#mode}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_alert_rule_anomaly_duplicate#id SentinelAlertRuleAnomalyDuplicate#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param multi_select_observation: multi_select_observation block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_alert_rule_anomaly_duplicate#multi_select_observation SentinelAlertRuleAnomalyDuplicate#multi_select_observation}
        :param prioritized_exclude_observation: prioritized_exclude_observation block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_alert_rule_anomaly_duplicate#prioritized_exclude_observation SentinelAlertRuleAnomalyDuplicate#prioritized_exclude_observation}
        :param single_select_observation: single_select_observation block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_alert_rule_anomaly_duplicate#single_select_observation SentinelAlertRuleAnomalyDuplicate#single_select_observation}
        :param threshold_observation: threshold_observation block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_alert_rule_anomaly_duplicate#threshold_observation SentinelAlertRuleAnomalyDuplicate#threshold_observation}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_alert_rule_anomaly_duplicate#timeouts SentinelAlertRuleAnomalyDuplicate#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__207ad69a2e2ab917c73e43484b2dcf0104d40c5c5fcccfcfc03d6684d729b67f)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = SentinelAlertRuleAnomalyDuplicateConfig(
            built_in_rule_id=built_in_rule_id,
            display_name=display_name,
            enabled=enabled,
            log_analytics_workspace_id=log_analytics_workspace_id,
            mode=mode,
            id=id,
            multi_select_observation=multi_select_observation,
            prioritized_exclude_observation=prioritized_exclude_observation,
            single_select_observation=single_select_observation,
            threshold_observation=threshold_observation,
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
        '''Generates CDKTF code for importing a SentinelAlertRuleAnomalyDuplicate resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the SentinelAlertRuleAnomalyDuplicate to import.
        :param import_from_id: The id of the existing SentinelAlertRuleAnomalyDuplicate that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_alert_rule_anomaly_duplicate#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the SentinelAlertRuleAnomalyDuplicate to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e9a082a4c7165edd2814ea486485ea851abdc4d548b8ca41cbafdd468385a83b)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putMultiSelectObservation")
    def put_multi_select_observation(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SentinelAlertRuleAnomalyDuplicateMultiSelectObservation", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c85917dfb488b371a68a770f96fdfac69cb916315c0aec77a58fb63b81ff6a6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putMultiSelectObservation", [value]))

    @jsii.member(jsii_name="putPrioritizedExcludeObservation")
    def put_prioritized_exclude_observation(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SentinelAlertRuleAnomalyDuplicatePrioritizedExcludeObservation", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9eab9c551963dde88e44f0347d12ca8d9af58146012f00d740bdd7e6e4f68c70)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putPrioritizedExcludeObservation", [value]))

    @jsii.member(jsii_name="putSingleSelectObservation")
    def put_single_select_observation(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SentinelAlertRuleAnomalyDuplicateSingleSelectObservation", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd8ca01a5ca37d951ee1ab70e517712709691a57efc6a5e9601ab22c65399575)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putSingleSelectObservation", [value]))

    @jsii.member(jsii_name="putThresholdObservation")
    def put_threshold_observation(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SentinelAlertRuleAnomalyDuplicateThresholdObservation", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__735dcebbe32ecbba1b71fccbb97f2f46d037be0fdb60b7291ee14e858d8c798d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putThresholdObservation", [value]))

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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_alert_rule_anomaly_duplicate#create SentinelAlertRuleAnomalyDuplicate#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_alert_rule_anomaly_duplicate#delete SentinelAlertRuleAnomalyDuplicate#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_alert_rule_anomaly_duplicate#read SentinelAlertRuleAnomalyDuplicate#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_alert_rule_anomaly_duplicate#update SentinelAlertRuleAnomalyDuplicate#update}.
        '''
        value = SentinelAlertRuleAnomalyDuplicateTimeouts(
            create=create, delete=delete, read=read, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetMultiSelectObservation")
    def reset_multi_select_observation(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMultiSelectObservation", []))

    @jsii.member(jsii_name="resetPrioritizedExcludeObservation")
    def reset_prioritized_exclude_observation(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPrioritizedExcludeObservation", []))

    @jsii.member(jsii_name="resetSingleSelectObservation")
    def reset_single_select_observation(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSingleSelectObservation", []))

    @jsii.member(jsii_name="resetThresholdObservation")
    def reset_threshold_observation(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetThresholdObservation", []))

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
    @jsii.member(jsii_name="anomalySettingsVersion")
    def anomaly_settings_version(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "anomalySettingsVersion"))

    @builtins.property
    @jsii.member(jsii_name="anomalyVersion")
    def anomaly_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "anomalyVersion"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @builtins.property
    @jsii.member(jsii_name="frequency")
    def frequency(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "frequency"))

    @builtins.property
    @jsii.member(jsii_name="isDefaultSettings")
    def is_default_settings(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "isDefaultSettings"))

    @builtins.property
    @jsii.member(jsii_name="multiSelectObservation")
    def multi_select_observation(
        self,
    ) -> "SentinelAlertRuleAnomalyDuplicateMultiSelectObservationList":
        return typing.cast("SentinelAlertRuleAnomalyDuplicateMultiSelectObservationList", jsii.get(self, "multiSelectObservation"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="prioritizedExcludeObservation")
    def prioritized_exclude_observation(
        self,
    ) -> "SentinelAlertRuleAnomalyDuplicatePrioritizedExcludeObservationList":
        return typing.cast("SentinelAlertRuleAnomalyDuplicatePrioritizedExcludeObservationList", jsii.get(self, "prioritizedExcludeObservation"))

    @builtins.property
    @jsii.member(jsii_name="requiredDataConnector")
    def required_data_connector(
        self,
    ) -> "SentinelAlertRuleAnomalyDuplicateRequiredDataConnectorList":
        return typing.cast("SentinelAlertRuleAnomalyDuplicateRequiredDataConnectorList", jsii.get(self, "requiredDataConnector"))

    @builtins.property
    @jsii.member(jsii_name="settingsDefinitionId")
    def settings_definition_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "settingsDefinitionId"))

    @builtins.property
    @jsii.member(jsii_name="singleSelectObservation")
    def single_select_observation(
        self,
    ) -> "SentinelAlertRuleAnomalyDuplicateSingleSelectObservationList":
        return typing.cast("SentinelAlertRuleAnomalyDuplicateSingleSelectObservationList", jsii.get(self, "singleSelectObservation"))

    @builtins.property
    @jsii.member(jsii_name="tactics")
    def tactics(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "tactics"))

    @builtins.property
    @jsii.member(jsii_name="techniques")
    def techniques(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "techniques"))

    @builtins.property
    @jsii.member(jsii_name="thresholdObservation")
    def threshold_observation(
        self,
    ) -> "SentinelAlertRuleAnomalyDuplicateThresholdObservationList":
        return typing.cast("SentinelAlertRuleAnomalyDuplicateThresholdObservationList", jsii.get(self, "thresholdObservation"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "SentinelAlertRuleAnomalyDuplicateTimeoutsOutputReference":
        return typing.cast("SentinelAlertRuleAnomalyDuplicateTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="builtInRuleIdInput")
    def built_in_rule_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "builtInRuleIdInput"))

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
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="logAnalyticsWorkspaceIdInput")
    def log_analytics_workspace_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "logAnalyticsWorkspaceIdInput"))

    @builtins.property
    @jsii.member(jsii_name="modeInput")
    def mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "modeInput"))

    @builtins.property
    @jsii.member(jsii_name="multiSelectObservationInput")
    def multi_select_observation_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SentinelAlertRuleAnomalyDuplicateMultiSelectObservation"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SentinelAlertRuleAnomalyDuplicateMultiSelectObservation"]]], jsii.get(self, "multiSelectObservationInput"))

    @builtins.property
    @jsii.member(jsii_name="prioritizedExcludeObservationInput")
    def prioritized_exclude_observation_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SentinelAlertRuleAnomalyDuplicatePrioritizedExcludeObservation"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SentinelAlertRuleAnomalyDuplicatePrioritizedExcludeObservation"]]], jsii.get(self, "prioritizedExcludeObservationInput"))

    @builtins.property
    @jsii.member(jsii_name="singleSelectObservationInput")
    def single_select_observation_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SentinelAlertRuleAnomalyDuplicateSingleSelectObservation"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SentinelAlertRuleAnomalyDuplicateSingleSelectObservation"]]], jsii.get(self, "singleSelectObservationInput"))

    @builtins.property
    @jsii.member(jsii_name="thresholdObservationInput")
    def threshold_observation_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SentinelAlertRuleAnomalyDuplicateThresholdObservation"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SentinelAlertRuleAnomalyDuplicateThresholdObservation"]]], jsii.get(self, "thresholdObservationInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "SentinelAlertRuleAnomalyDuplicateTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "SentinelAlertRuleAnomalyDuplicateTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="builtInRuleId")
    def built_in_rule_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "builtInRuleId"))

    @built_in_rule_id.setter
    def built_in_rule_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c25cf08d63e61a88dea44e980828bf71b5c7c70c1626591e1895f39b7f1e33ab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "builtInRuleId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="displayName")
    def display_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "displayName"))

    @display_name.setter
    def display_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f85c46c9af6cf2d77868a81b8e562e79b350016b34c94573e0c7694bcde2b8e7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9f7b355458ab9905e257e082a350770f914d81eaf77c6cbbe54da1d0421d1df9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7da461eaf0c4612b7bea8f7642af8459fcaebe76afb5098ff90ac455bf15271d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="logAnalyticsWorkspaceId")
    def log_analytics_workspace_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "logAnalyticsWorkspaceId"))

    @log_analytics_workspace_id.setter
    def log_analytics_workspace_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9cb94920b41d807d69de151f2e6a290c80888854ad296c1d7b6b5f66b5714ce7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "logAnalyticsWorkspaceId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="mode")
    def mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mode"))

    @mode.setter
    def mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4cb1a2f29eff56a15117d11c3d1d308ec6575817489f6ad4f229ec24c94c8ae4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mode", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.sentinelAlertRuleAnomalyDuplicate.SentinelAlertRuleAnomalyDuplicateConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "built_in_rule_id": "builtInRuleId",
        "display_name": "displayName",
        "enabled": "enabled",
        "log_analytics_workspace_id": "logAnalyticsWorkspaceId",
        "mode": "mode",
        "id": "id",
        "multi_select_observation": "multiSelectObservation",
        "prioritized_exclude_observation": "prioritizedExcludeObservation",
        "single_select_observation": "singleSelectObservation",
        "threshold_observation": "thresholdObservation",
        "timeouts": "timeouts",
    },
)
class SentinelAlertRuleAnomalyDuplicateConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        built_in_rule_id: builtins.str,
        display_name: builtins.str,
        enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        log_analytics_workspace_id: builtins.str,
        mode: builtins.str,
        id: typing.Optional[builtins.str] = None,
        multi_select_observation: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SentinelAlertRuleAnomalyDuplicateMultiSelectObservation", typing.Dict[builtins.str, typing.Any]]]]] = None,
        prioritized_exclude_observation: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SentinelAlertRuleAnomalyDuplicatePrioritizedExcludeObservation", typing.Dict[builtins.str, typing.Any]]]]] = None,
        single_select_observation: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SentinelAlertRuleAnomalyDuplicateSingleSelectObservation", typing.Dict[builtins.str, typing.Any]]]]] = None,
        threshold_observation: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SentinelAlertRuleAnomalyDuplicateThresholdObservation", typing.Dict[builtins.str, typing.Any]]]]] = None,
        timeouts: typing.Optional[typing.Union["SentinelAlertRuleAnomalyDuplicateTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param built_in_rule_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_alert_rule_anomaly_duplicate#built_in_rule_id SentinelAlertRuleAnomalyDuplicate#built_in_rule_id}.
        :param display_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_alert_rule_anomaly_duplicate#display_name SentinelAlertRuleAnomalyDuplicate#display_name}.
        :param enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_alert_rule_anomaly_duplicate#enabled SentinelAlertRuleAnomalyDuplicate#enabled}.
        :param log_analytics_workspace_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_alert_rule_anomaly_duplicate#log_analytics_workspace_id SentinelAlertRuleAnomalyDuplicate#log_analytics_workspace_id}.
        :param mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_alert_rule_anomaly_duplicate#mode SentinelAlertRuleAnomalyDuplicate#mode}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_alert_rule_anomaly_duplicate#id SentinelAlertRuleAnomalyDuplicate#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param multi_select_observation: multi_select_observation block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_alert_rule_anomaly_duplicate#multi_select_observation SentinelAlertRuleAnomalyDuplicate#multi_select_observation}
        :param prioritized_exclude_observation: prioritized_exclude_observation block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_alert_rule_anomaly_duplicate#prioritized_exclude_observation SentinelAlertRuleAnomalyDuplicate#prioritized_exclude_observation}
        :param single_select_observation: single_select_observation block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_alert_rule_anomaly_duplicate#single_select_observation SentinelAlertRuleAnomalyDuplicate#single_select_observation}
        :param threshold_observation: threshold_observation block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_alert_rule_anomaly_duplicate#threshold_observation SentinelAlertRuleAnomalyDuplicate#threshold_observation}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_alert_rule_anomaly_duplicate#timeouts SentinelAlertRuleAnomalyDuplicate#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(timeouts, dict):
            timeouts = SentinelAlertRuleAnomalyDuplicateTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3bf1b33a1717fa55485ff40868f18c23bc9e83cce3a600406a6e4e8d357f438b)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument built_in_rule_id", value=built_in_rule_id, expected_type=type_hints["built_in_rule_id"])
            check_type(argname="argument display_name", value=display_name, expected_type=type_hints["display_name"])
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument log_analytics_workspace_id", value=log_analytics_workspace_id, expected_type=type_hints["log_analytics_workspace_id"])
            check_type(argname="argument mode", value=mode, expected_type=type_hints["mode"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument multi_select_observation", value=multi_select_observation, expected_type=type_hints["multi_select_observation"])
            check_type(argname="argument prioritized_exclude_observation", value=prioritized_exclude_observation, expected_type=type_hints["prioritized_exclude_observation"])
            check_type(argname="argument single_select_observation", value=single_select_observation, expected_type=type_hints["single_select_observation"])
            check_type(argname="argument threshold_observation", value=threshold_observation, expected_type=type_hints["threshold_observation"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "built_in_rule_id": built_in_rule_id,
            "display_name": display_name,
            "enabled": enabled,
            "log_analytics_workspace_id": log_analytics_workspace_id,
            "mode": mode,
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
        if id is not None:
            self._values["id"] = id
        if multi_select_observation is not None:
            self._values["multi_select_observation"] = multi_select_observation
        if prioritized_exclude_observation is not None:
            self._values["prioritized_exclude_observation"] = prioritized_exclude_observation
        if single_select_observation is not None:
            self._values["single_select_observation"] = single_select_observation
        if threshold_observation is not None:
            self._values["threshold_observation"] = threshold_observation
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
    def built_in_rule_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_alert_rule_anomaly_duplicate#built_in_rule_id SentinelAlertRuleAnomalyDuplicate#built_in_rule_id}.'''
        result = self._values.get("built_in_rule_id")
        assert result is not None, "Required property 'built_in_rule_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def display_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_alert_rule_anomaly_duplicate#display_name SentinelAlertRuleAnomalyDuplicate#display_name}.'''
        result = self._values.get("display_name")
        assert result is not None, "Required property 'display_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_alert_rule_anomaly_duplicate#enabled SentinelAlertRuleAnomalyDuplicate#enabled}.'''
        result = self._values.get("enabled")
        assert result is not None, "Required property 'enabled' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    @builtins.property
    def log_analytics_workspace_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_alert_rule_anomaly_duplicate#log_analytics_workspace_id SentinelAlertRuleAnomalyDuplicate#log_analytics_workspace_id}.'''
        result = self._values.get("log_analytics_workspace_id")
        assert result is not None, "Required property 'log_analytics_workspace_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def mode(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_alert_rule_anomaly_duplicate#mode SentinelAlertRuleAnomalyDuplicate#mode}.'''
        result = self._values.get("mode")
        assert result is not None, "Required property 'mode' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_alert_rule_anomaly_duplicate#id SentinelAlertRuleAnomalyDuplicate#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def multi_select_observation(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SentinelAlertRuleAnomalyDuplicateMultiSelectObservation"]]]:
        '''multi_select_observation block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_alert_rule_anomaly_duplicate#multi_select_observation SentinelAlertRuleAnomalyDuplicate#multi_select_observation}
        '''
        result = self._values.get("multi_select_observation")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SentinelAlertRuleAnomalyDuplicateMultiSelectObservation"]]], result)

    @builtins.property
    def prioritized_exclude_observation(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SentinelAlertRuleAnomalyDuplicatePrioritizedExcludeObservation"]]]:
        '''prioritized_exclude_observation block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_alert_rule_anomaly_duplicate#prioritized_exclude_observation SentinelAlertRuleAnomalyDuplicate#prioritized_exclude_observation}
        '''
        result = self._values.get("prioritized_exclude_observation")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SentinelAlertRuleAnomalyDuplicatePrioritizedExcludeObservation"]]], result)

    @builtins.property
    def single_select_observation(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SentinelAlertRuleAnomalyDuplicateSingleSelectObservation"]]]:
        '''single_select_observation block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_alert_rule_anomaly_duplicate#single_select_observation SentinelAlertRuleAnomalyDuplicate#single_select_observation}
        '''
        result = self._values.get("single_select_observation")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SentinelAlertRuleAnomalyDuplicateSingleSelectObservation"]]], result)

    @builtins.property
    def threshold_observation(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SentinelAlertRuleAnomalyDuplicateThresholdObservation"]]]:
        '''threshold_observation block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_alert_rule_anomaly_duplicate#threshold_observation SentinelAlertRuleAnomalyDuplicate#threshold_observation}
        '''
        result = self._values.get("threshold_observation")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SentinelAlertRuleAnomalyDuplicateThresholdObservation"]]], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["SentinelAlertRuleAnomalyDuplicateTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_alert_rule_anomaly_duplicate#timeouts SentinelAlertRuleAnomalyDuplicate#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["SentinelAlertRuleAnomalyDuplicateTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SentinelAlertRuleAnomalyDuplicateConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.sentinelAlertRuleAnomalyDuplicate.SentinelAlertRuleAnomalyDuplicateMultiSelectObservation",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "values": "values"},
)
class SentinelAlertRuleAnomalyDuplicateMultiSelectObservation:
    def __init__(
        self,
        *,
        name: builtins.str,
        values: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_alert_rule_anomaly_duplicate#name SentinelAlertRuleAnomalyDuplicate#name}.
        :param values: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_alert_rule_anomaly_duplicate#values SentinelAlertRuleAnomalyDuplicate#values}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6a83572d9d94f5055bba775d3439d24cf318eb6b29a92f10972e3a6a23f93bc4)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument values", value=values, expected_type=type_hints["values"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "values": values,
        }

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_alert_rule_anomaly_duplicate#name SentinelAlertRuleAnomalyDuplicate#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def values(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_alert_rule_anomaly_duplicate#values SentinelAlertRuleAnomalyDuplicate#values}.'''
        result = self._values.get("values")
        assert result is not None, "Required property 'values' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SentinelAlertRuleAnomalyDuplicateMultiSelectObservation(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SentinelAlertRuleAnomalyDuplicateMultiSelectObservationList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.sentinelAlertRuleAnomalyDuplicate.SentinelAlertRuleAnomalyDuplicateMultiSelectObservationList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__838802738b581205a0c5d5d08fb22d360c92f43232c0c89412c31b04b0026a35)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "SentinelAlertRuleAnomalyDuplicateMultiSelectObservationOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c1b347fa0ce968134c74c5b4b0479600842bdd6fbd028a8ceb59ee34d17b8a1d)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("SentinelAlertRuleAnomalyDuplicateMultiSelectObservationOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__94da8bdfd0b9c3fead2ecde0d50375c3d548f63fa2395d2c11c4586f36a5122d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3968c21482707efea22a8865cb405f56757e7212da116de110a63e5c8f799d98)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0f1618f86b0b960721b8f25a88500a8eeafe236b747489346e8276cf80f57278)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SentinelAlertRuleAnomalyDuplicateMultiSelectObservation]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SentinelAlertRuleAnomalyDuplicateMultiSelectObservation]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SentinelAlertRuleAnomalyDuplicateMultiSelectObservation]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__30124d0f5b3b65df8f33c0ac7b5d06edcf7fb06e926d4554e1d92541801bcf89)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class SentinelAlertRuleAnomalyDuplicateMultiSelectObservationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.sentinelAlertRuleAnomalyDuplicate.SentinelAlertRuleAnomalyDuplicateMultiSelectObservationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__08f9e078d85a1c1db3cccdb2cbad43433bdc5ab1e075d9e8e4ac95f5abfa79f7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @builtins.property
    @jsii.member(jsii_name="supportedValues")
    def supported_values(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "supportedValues"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="valuesInput")
    def values_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "valuesInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f4a0bc3ee9af03a94c24dae4099cd991fdf801a03eb89ee58949da5cc77a828c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="values")
    def values(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "values"))

    @values.setter
    def values(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__038cb24a951aa9c1d6e88014a49ba29dcbea4ce28d06c40d065464d2ee15495b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "values", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SentinelAlertRuleAnomalyDuplicateMultiSelectObservation]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SentinelAlertRuleAnomalyDuplicateMultiSelectObservation]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SentinelAlertRuleAnomalyDuplicateMultiSelectObservation]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3830566f0ab46c670f6ca2db19002389f15d70af4446e05365bef2a93193d299)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.sentinelAlertRuleAnomalyDuplicate.SentinelAlertRuleAnomalyDuplicatePrioritizedExcludeObservation",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "exclude": "exclude", "prioritize": "prioritize"},
)
class SentinelAlertRuleAnomalyDuplicatePrioritizedExcludeObservation:
    def __init__(
        self,
        *,
        name: builtins.str,
        exclude: typing.Optional[builtins.str] = None,
        prioritize: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_alert_rule_anomaly_duplicate#name SentinelAlertRuleAnomalyDuplicate#name}.
        :param exclude: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_alert_rule_anomaly_duplicate#exclude SentinelAlertRuleAnomalyDuplicate#exclude}.
        :param prioritize: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_alert_rule_anomaly_duplicate#prioritize SentinelAlertRuleAnomalyDuplicate#prioritize}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__15b3e8bf677d3f1a6e169ae2286d81c6e30d7cc1d03ed13e7882b3fda93ce8a7)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument exclude", value=exclude, expected_type=type_hints["exclude"])
            check_type(argname="argument prioritize", value=prioritize, expected_type=type_hints["prioritize"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }
        if exclude is not None:
            self._values["exclude"] = exclude
        if prioritize is not None:
            self._values["prioritize"] = prioritize

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_alert_rule_anomaly_duplicate#name SentinelAlertRuleAnomalyDuplicate#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def exclude(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_alert_rule_anomaly_duplicate#exclude SentinelAlertRuleAnomalyDuplicate#exclude}.'''
        result = self._values.get("exclude")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def prioritize(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_alert_rule_anomaly_duplicate#prioritize SentinelAlertRuleAnomalyDuplicate#prioritize}.'''
        result = self._values.get("prioritize")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SentinelAlertRuleAnomalyDuplicatePrioritizedExcludeObservation(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SentinelAlertRuleAnomalyDuplicatePrioritizedExcludeObservationList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.sentinelAlertRuleAnomalyDuplicate.SentinelAlertRuleAnomalyDuplicatePrioritizedExcludeObservationList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__665b95b3fef73d4c9abc135c55376819d2f4afed55dc9ce51d971e11f234c7c1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "SentinelAlertRuleAnomalyDuplicatePrioritizedExcludeObservationOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eee76f0e2007a39dc7c267c05954aa8b162f73596a98e7ca96401d7229081663)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("SentinelAlertRuleAnomalyDuplicatePrioritizedExcludeObservationOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__43d47c9568221bfa464178e288ce9c79e83bb57ce158fc30917c680907b25aad)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fe5414b6645d2b8a532cbc21b09f48fb1d4ab4c343dfdf938dede6f49704f4e3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bf3955983556f3a0ec94bd97a19c96c0bb78dc0bf9d8f582f250fbdaec11b481)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SentinelAlertRuleAnomalyDuplicatePrioritizedExcludeObservation]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SentinelAlertRuleAnomalyDuplicatePrioritizedExcludeObservation]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SentinelAlertRuleAnomalyDuplicatePrioritizedExcludeObservation]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dab1c4c18cc77142f41e9590ca4b22c5d504031eeafd285d489e66e05a2fe948)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class SentinelAlertRuleAnomalyDuplicatePrioritizedExcludeObservationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.sentinelAlertRuleAnomalyDuplicate.SentinelAlertRuleAnomalyDuplicatePrioritizedExcludeObservationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ad93d830675edcc5e0a3c5333ee5ca5573672c7441b83831aad53ad1d01aec6a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetExclude")
    def reset_exclude(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExclude", []))

    @jsii.member(jsii_name="resetPrioritize")
    def reset_prioritize(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPrioritize", []))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @builtins.property
    @jsii.member(jsii_name="excludeInput")
    def exclude_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "excludeInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="prioritizeInput")
    def prioritize_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "prioritizeInput"))

    @builtins.property
    @jsii.member(jsii_name="exclude")
    def exclude(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "exclude"))

    @exclude.setter
    def exclude(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__adf05109684b3cf010f8294565aca68424f72a05ea6de4c5cc0d3778548f77e8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "exclude", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dde8cf94625ad2b202427337da00162fa13879eb0cdb47e112fb7e1e827e503e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="prioritize")
    def prioritize(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "prioritize"))

    @prioritize.setter
    def prioritize(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__301f4006aed40cc6e01879883cd69d20b4502fa732dea7c47427f4f8a9c05b30)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "prioritize", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SentinelAlertRuleAnomalyDuplicatePrioritizedExcludeObservation]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SentinelAlertRuleAnomalyDuplicatePrioritizedExcludeObservation]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SentinelAlertRuleAnomalyDuplicatePrioritizedExcludeObservation]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8686e5ff219bf92a429cb1026b88bf6a8fc9eb0916204ddb03e4a5f44b4afb12)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.sentinelAlertRuleAnomalyDuplicate.SentinelAlertRuleAnomalyDuplicateRequiredDataConnector",
    jsii_struct_bases=[],
    name_mapping={},
)
class SentinelAlertRuleAnomalyDuplicateRequiredDataConnector:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SentinelAlertRuleAnomalyDuplicateRequiredDataConnector(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SentinelAlertRuleAnomalyDuplicateRequiredDataConnectorList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.sentinelAlertRuleAnomalyDuplicate.SentinelAlertRuleAnomalyDuplicateRequiredDataConnectorList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4ab2986e6c3fc00e9c4a59dbcd74030db1386939561c1bb85e91265b53f666ee)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "SentinelAlertRuleAnomalyDuplicateRequiredDataConnectorOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd666b02bad050e8f514dd68c6363a85f2735ff5a158e23688c0ed90b36bb79c)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("SentinelAlertRuleAnomalyDuplicateRequiredDataConnectorOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa9286a92b12154ac446e9a2e02437dc92811524f7ebc53d822bc92d7d23828a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2a31d4876d3c345a5f871d185774886c7d5661005cd0f533e5288f21b9face8f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ac9880260b40f98f7cfa9626f7e8e459911807a3c9664595f4b92495c7d26b7f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class SentinelAlertRuleAnomalyDuplicateRequiredDataConnectorOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.sentinelAlertRuleAnomalyDuplicate.SentinelAlertRuleAnomalyDuplicateRequiredDataConnectorOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5b590666d0ce0875651237fe74c9d1e79bc92f9a333faa7793693e7129d7b2c7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="connectorId")
    def connector_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "connectorId"))

    @builtins.property
    @jsii.member(jsii_name="dataTypes")
    def data_types(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "dataTypes"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[SentinelAlertRuleAnomalyDuplicateRequiredDataConnector]:
        return typing.cast(typing.Optional[SentinelAlertRuleAnomalyDuplicateRequiredDataConnector], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SentinelAlertRuleAnomalyDuplicateRequiredDataConnector],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e55c0c29714b90ea8fd8f6bac69d625e2b1092abb951e5d5ee904fee21da8447)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.sentinelAlertRuleAnomalyDuplicate.SentinelAlertRuleAnomalyDuplicateSingleSelectObservation",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "value": "value"},
)
class SentinelAlertRuleAnomalyDuplicateSingleSelectObservation:
    def __init__(self, *, name: builtins.str, value: builtins.str) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_alert_rule_anomaly_duplicate#name SentinelAlertRuleAnomalyDuplicate#name}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_alert_rule_anomaly_duplicate#value SentinelAlertRuleAnomalyDuplicate#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1ced964b297207c37d2f064c564d1d7b71cdeac42a8847573358a3abcfd33127)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "value": value,
        }

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_alert_rule_anomaly_duplicate#name SentinelAlertRuleAnomalyDuplicate#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_alert_rule_anomaly_duplicate#value SentinelAlertRuleAnomalyDuplicate#value}.'''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SentinelAlertRuleAnomalyDuplicateSingleSelectObservation(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SentinelAlertRuleAnomalyDuplicateSingleSelectObservationList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.sentinelAlertRuleAnomalyDuplicate.SentinelAlertRuleAnomalyDuplicateSingleSelectObservationList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a3ae363fff3175ac4acd7ee1f47ed7d947a9abff14509c20f11cf4980c983e97)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "SentinelAlertRuleAnomalyDuplicateSingleSelectObservationOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee98cd0de630694394776b55d119e6dc62d41ba43e4b23cd333e5311a354413c)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("SentinelAlertRuleAnomalyDuplicateSingleSelectObservationOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__90c161113de4d68c677e8d6d72d984f33a6adf6c64c6f3d92c1a0a509640acdd)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3a5101ca7c8fbed0a588a8061441d3de8f85ec0e8e1dddb21449606f01becad5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0f6457d0fbe9335f4affb51e6294bb4376e48ee5c96c1d7951ce0e8223f827c3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SentinelAlertRuleAnomalyDuplicateSingleSelectObservation]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SentinelAlertRuleAnomalyDuplicateSingleSelectObservation]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SentinelAlertRuleAnomalyDuplicateSingleSelectObservation]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f32e301388d1efd13447397013511ae7f3a4ac2fb66d6025f11b2e6071de5ce6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class SentinelAlertRuleAnomalyDuplicateSingleSelectObservationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.sentinelAlertRuleAnomalyDuplicate.SentinelAlertRuleAnomalyDuplicateSingleSelectObservationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__25af4ec007543e9e4e5c13d07257cdef96137744639a4355400a6aac45e902b4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @builtins.property
    @jsii.member(jsii_name="supportedValues")
    def supported_values(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "supportedValues"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__02eb840376dff19d4ad7bf0819d69c994163f4b0f50b84d58ef138d280ac7f97)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__774fdaf4024e12f4dac53b2342edf77c0bc61868ab088939fedf0351d160f97f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SentinelAlertRuleAnomalyDuplicateSingleSelectObservation]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SentinelAlertRuleAnomalyDuplicateSingleSelectObservation]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SentinelAlertRuleAnomalyDuplicateSingleSelectObservation]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b2d2b299de4ab3ae751829303546befc282ef1ea84eed7484cc3d8e253dac997)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.sentinelAlertRuleAnomalyDuplicate.SentinelAlertRuleAnomalyDuplicateThresholdObservation",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "value": "value"},
)
class SentinelAlertRuleAnomalyDuplicateThresholdObservation:
    def __init__(self, *, name: builtins.str, value: builtins.str) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_alert_rule_anomaly_duplicate#name SentinelAlertRuleAnomalyDuplicate#name}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_alert_rule_anomaly_duplicate#value SentinelAlertRuleAnomalyDuplicate#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__108d049ca2818f2de5ebba88951231caadebb651fa0706bb3ee5e7af507bf12e)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "value": value,
        }

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_alert_rule_anomaly_duplicate#name SentinelAlertRuleAnomalyDuplicate#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_alert_rule_anomaly_duplicate#value SentinelAlertRuleAnomalyDuplicate#value}.'''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SentinelAlertRuleAnomalyDuplicateThresholdObservation(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SentinelAlertRuleAnomalyDuplicateThresholdObservationList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.sentinelAlertRuleAnomalyDuplicate.SentinelAlertRuleAnomalyDuplicateThresholdObservationList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__25291cd18d4a5dee4f740c52aaac6adc2dda376ace65ce6ecb35f0d6be867299)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "SentinelAlertRuleAnomalyDuplicateThresholdObservationOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__771b48deaab352bf55fb1d721e2aba2681d6a23439dd551f7fe9359724041f79)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("SentinelAlertRuleAnomalyDuplicateThresholdObservationOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7fa7309eebca212c7149e90d737ff9a72a029ab057cfb6905ce48e2affec2d91)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3ed4d6a728ee5ff54d9f0710640981c2e650c7e16b2f9e158bd7302e1cdc84ec)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1e076887a4961d6143175688fe1962b0918724f1531df69663ed4067e8538dda)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SentinelAlertRuleAnomalyDuplicateThresholdObservation]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SentinelAlertRuleAnomalyDuplicateThresholdObservation]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SentinelAlertRuleAnomalyDuplicateThresholdObservation]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b20b95711d55ad8176d5e1106b7ddc7ddf0717cbecb7a84dd98b844e98100f15)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class SentinelAlertRuleAnomalyDuplicateThresholdObservationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.sentinelAlertRuleAnomalyDuplicate.SentinelAlertRuleAnomalyDuplicateThresholdObservationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__82cf4b2168a5be39def97003443b79ed8ac482ace312a0a697f3cc40222ea9de)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @builtins.property
    @jsii.member(jsii_name="max")
    def max(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "max"))

    @builtins.property
    @jsii.member(jsii_name="min")
    def min(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "min"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__4cd796703836f4037fdcc3467dbcf2e49975eb7c823592c7c7ec0e2759dce27f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b4ceaba0106b4d97c07057c149ad43d97fded996739f196e031019e1af7147d3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SentinelAlertRuleAnomalyDuplicateThresholdObservation]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SentinelAlertRuleAnomalyDuplicateThresholdObservation]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SentinelAlertRuleAnomalyDuplicateThresholdObservation]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__99f9e5af351b5a105ee89f5ba6cd7c8a84efd33e01182f3b1c5d1481c5e28cd1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.sentinelAlertRuleAnomalyDuplicate.SentinelAlertRuleAnomalyDuplicateTimeouts",
    jsii_struct_bases=[],
    name_mapping={
        "create": "create",
        "delete": "delete",
        "read": "read",
        "update": "update",
    },
)
class SentinelAlertRuleAnomalyDuplicateTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_alert_rule_anomaly_duplicate#create SentinelAlertRuleAnomalyDuplicate#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_alert_rule_anomaly_duplicate#delete SentinelAlertRuleAnomalyDuplicate#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_alert_rule_anomaly_duplicate#read SentinelAlertRuleAnomalyDuplicate#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_alert_rule_anomaly_duplicate#update SentinelAlertRuleAnomalyDuplicate#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__925542c36bb6c82bd85e2a921964f41d910c607df407e2c485cc96f51326d019)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_alert_rule_anomaly_duplicate#create SentinelAlertRuleAnomalyDuplicate#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_alert_rule_anomaly_duplicate#delete SentinelAlertRuleAnomalyDuplicate#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def read(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_alert_rule_anomaly_duplicate#read SentinelAlertRuleAnomalyDuplicate#read}.'''
        result = self._values.get("read")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_alert_rule_anomaly_duplicate#update SentinelAlertRuleAnomalyDuplicate#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SentinelAlertRuleAnomalyDuplicateTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SentinelAlertRuleAnomalyDuplicateTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.sentinelAlertRuleAnomalyDuplicate.SentinelAlertRuleAnomalyDuplicateTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__07c50d375f3cebc2a0b2125c7c810532ac97596b2884c2bdcf9176461e1fd7f1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3c7d8ca9e4d904588c49bc72f770f0429eaa7251cb6338ed95fae5ace3e551f4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ca4e470bef03c8851601888ca97971243b3889fe2b3602cee34c654d0e7e90dd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="read")
    def read(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "read"))

    @read.setter
    def read(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e5deafd463c25f9150aa5a8e661ebf703c0c7d9ddfed6a4f17be3a41d7d599e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "read", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4216d0328d141984806b4b2b57421a0f46121217f1e7e49f83fa81ff2db26b00)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SentinelAlertRuleAnomalyDuplicateTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SentinelAlertRuleAnomalyDuplicateTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SentinelAlertRuleAnomalyDuplicateTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__919224961610dfdb6395102173892560b82a644ea8d756059bd8d6957fb3e84d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "SentinelAlertRuleAnomalyDuplicate",
    "SentinelAlertRuleAnomalyDuplicateConfig",
    "SentinelAlertRuleAnomalyDuplicateMultiSelectObservation",
    "SentinelAlertRuleAnomalyDuplicateMultiSelectObservationList",
    "SentinelAlertRuleAnomalyDuplicateMultiSelectObservationOutputReference",
    "SentinelAlertRuleAnomalyDuplicatePrioritizedExcludeObservation",
    "SentinelAlertRuleAnomalyDuplicatePrioritizedExcludeObservationList",
    "SentinelAlertRuleAnomalyDuplicatePrioritizedExcludeObservationOutputReference",
    "SentinelAlertRuleAnomalyDuplicateRequiredDataConnector",
    "SentinelAlertRuleAnomalyDuplicateRequiredDataConnectorList",
    "SentinelAlertRuleAnomalyDuplicateRequiredDataConnectorOutputReference",
    "SentinelAlertRuleAnomalyDuplicateSingleSelectObservation",
    "SentinelAlertRuleAnomalyDuplicateSingleSelectObservationList",
    "SentinelAlertRuleAnomalyDuplicateSingleSelectObservationOutputReference",
    "SentinelAlertRuleAnomalyDuplicateThresholdObservation",
    "SentinelAlertRuleAnomalyDuplicateThresholdObservationList",
    "SentinelAlertRuleAnomalyDuplicateThresholdObservationOutputReference",
    "SentinelAlertRuleAnomalyDuplicateTimeouts",
    "SentinelAlertRuleAnomalyDuplicateTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__207ad69a2e2ab917c73e43484b2dcf0104d40c5c5fcccfcfc03d6684d729b67f(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    built_in_rule_id: builtins.str,
    display_name: builtins.str,
    enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    log_analytics_workspace_id: builtins.str,
    mode: builtins.str,
    id: typing.Optional[builtins.str] = None,
    multi_select_observation: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SentinelAlertRuleAnomalyDuplicateMultiSelectObservation, typing.Dict[builtins.str, typing.Any]]]]] = None,
    prioritized_exclude_observation: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SentinelAlertRuleAnomalyDuplicatePrioritizedExcludeObservation, typing.Dict[builtins.str, typing.Any]]]]] = None,
    single_select_observation: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SentinelAlertRuleAnomalyDuplicateSingleSelectObservation, typing.Dict[builtins.str, typing.Any]]]]] = None,
    threshold_observation: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SentinelAlertRuleAnomalyDuplicateThresholdObservation, typing.Dict[builtins.str, typing.Any]]]]] = None,
    timeouts: typing.Optional[typing.Union[SentinelAlertRuleAnomalyDuplicateTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__e9a082a4c7165edd2814ea486485ea851abdc4d548b8ca41cbafdd468385a83b(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c85917dfb488b371a68a770f96fdfac69cb916315c0aec77a58fb63b81ff6a6(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SentinelAlertRuleAnomalyDuplicateMultiSelectObservation, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9eab9c551963dde88e44f0347d12ca8d9af58146012f00d740bdd7e6e4f68c70(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SentinelAlertRuleAnomalyDuplicatePrioritizedExcludeObservation, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd8ca01a5ca37d951ee1ab70e517712709691a57efc6a5e9601ab22c65399575(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SentinelAlertRuleAnomalyDuplicateSingleSelectObservation, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__735dcebbe32ecbba1b71fccbb97f2f46d037be0fdb60b7291ee14e858d8c798d(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SentinelAlertRuleAnomalyDuplicateThresholdObservation, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c25cf08d63e61a88dea44e980828bf71b5c7c70c1626591e1895f39b7f1e33ab(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f85c46c9af6cf2d77868a81b8e562e79b350016b34c94573e0c7694bcde2b8e7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f7b355458ab9905e257e082a350770f914d81eaf77c6cbbe54da1d0421d1df9(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7da461eaf0c4612b7bea8f7642af8459fcaebe76afb5098ff90ac455bf15271d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9cb94920b41d807d69de151f2e6a290c80888854ad296c1d7b6b5f66b5714ce7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4cb1a2f29eff56a15117d11c3d1d308ec6575817489f6ad4f229ec24c94c8ae4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3bf1b33a1717fa55485ff40868f18c23bc9e83cce3a600406a6e4e8d357f438b(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    built_in_rule_id: builtins.str,
    display_name: builtins.str,
    enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    log_analytics_workspace_id: builtins.str,
    mode: builtins.str,
    id: typing.Optional[builtins.str] = None,
    multi_select_observation: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SentinelAlertRuleAnomalyDuplicateMultiSelectObservation, typing.Dict[builtins.str, typing.Any]]]]] = None,
    prioritized_exclude_observation: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SentinelAlertRuleAnomalyDuplicatePrioritizedExcludeObservation, typing.Dict[builtins.str, typing.Any]]]]] = None,
    single_select_observation: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SentinelAlertRuleAnomalyDuplicateSingleSelectObservation, typing.Dict[builtins.str, typing.Any]]]]] = None,
    threshold_observation: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SentinelAlertRuleAnomalyDuplicateThresholdObservation, typing.Dict[builtins.str, typing.Any]]]]] = None,
    timeouts: typing.Optional[typing.Union[SentinelAlertRuleAnomalyDuplicateTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a83572d9d94f5055bba775d3439d24cf318eb6b29a92f10972e3a6a23f93bc4(
    *,
    name: builtins.str,
    values: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__838802738b581205a0c5d5d08fb22d360c92f43232c0c89412c31b04b0026a35(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1b347fa0ce968134c74c5b4b0479600842bdd6fbd028a8ceb59ee34d17b8a1d(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94da8bdfd0b9c3fead2ecde0d50375c3d548f63fa2395d2c11c4586f36a5122d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3968c21482707efea22a8865cb405f56757e7212da116de110a63e5c8f799d98(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f1618f86b0b960721b8f25a88500a8eeafe236b747489346e8276cf80f57278(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30124d0f5b3b65df8f33c0ac7b5d06edcf7fb06e926d4554e1d92541801bcf89(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SentinelAlertRuleAnomalyDuplicateMultiSelectObservation]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__08f9e078d85a1c1db3cccdb2cbad43433bdc5ab1e075d9e8e4ac95f5abfa79f7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4a0bc3ee9af03a94c24dae4099cd991fdf801a03eb89ee58949da5cc77a828c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__038cb24a951aa9c1d6e88014a49ba29dcbea4ce28d06c40d065464d2ee15495b(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3830566f0ab46c670f6ca2db19002389f15d70af4446e05365bef2a93193d299(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SentinelAlertRuleAnomalyDuplicateMultiSelectObservation]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15b3e8bf677d3f1a6e169ae2286d81c6e30d7cc1d03ed13e7882b3fda93ce8a7(
    *,
    name: builtins.str,
    exclude: typing.Optional[builtins.str] = None,
    prioritize: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__665b95b3fef73d4c9abc135c55376819d2f4afed55dc9ce51d971e11f234c7c1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eee76f0e2007a39dc7c267c05954aa8b162f73596a98e7ca96401d7229081663(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43d47c9568221bfa464178e288ce9c79e83bb57ce158fc30917c680907b25aad(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe5414b6645d2b8a532cbc21b09f48fb1d4ab4c343dfdf938dede6f49704f4e3(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf3955983556f3a0ec94bd97a19c96c0bb78dc0bf9d8f582f250fbdaec11b481(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dab1c4c18cc77142f41e9590ca4b22c5d504031eeafd285d489e66e05a2fe948(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SentinelAlertRuleAnomalyDuplicatePrioritizedExcludeObservation]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad93d830675edcc5e0a3c5333ee5ca5573672c7441b83831aad53ad1d01aec6a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__adf05109684b3cf010f8294565aca68424f72a05ea6de4c5cc0d3778548f77e8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dde8cf94625ad2b202427337da00162fa13879eb0cdb47e112fb7e1e827e503e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__301f4006aed40cc6e01879883cd69d20b4502fa732dea7c47427f4f8a9c05b30(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8686e5ff219bf92a429cb1026b88bf6a8fc9eb0916204ddb03e4a5f44b4afb12(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SentinelAlertRuleAnomalyDuplicatePrioritizedExcludeObservation]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ab2986e6c3fc00e9c4a59dbcd74030db1386939561c1bb85e91265b53f666ee(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd666b02bad050e8f514dd68c6363a85f2735ff5a158e23688c0ed90b36bb79c(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa9286a92b12154ac446e9a2e02437dc92811524f7ebc53d822bc92d7d23828a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a31d4876d3c345a5f871d185774886c7d5661005cd0f533e5288f21b9face8f(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac9880260b40f98f7cfa9626f7e8e459911807a3c9664595f4b92495c7d26b7f(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b590666d0ce0875651237fe74c9d1e79bc92f9a333faa7793693e7129d7b2c7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e55c0c29714b90ea8fd8f6bac69d625e2b1092abb951e5d5ee904fee21da8447(
    value: typing.Optional[SentinelAlertRuleAnomalyDuplicateRequiredDataConnector],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ced964b297207c37d2f064c564d1d7b71cdeac42a8847573358a3abcfd33127(
    *,
    name: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3ae363fff3175ac4acd7ee1f47ed7d947a9abff14509c20f11cf4980c983e97(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee98cd0de630694394776b55d119e6dc62d41ba43e4b23cd333e5311a354413c(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__90c161113de4d68c677e8d6d72d984f33a6adf6c64c6f3d92c1a0a509640acdd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a5101ca7c8fbed0a588a8061441d3de8f85ec0e8e1dddb21449606f01becad5(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f6457d0fbe9335f4affb51e6294bb4376e48ee5c96c1d7951ce0e8223f827c3(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f32e301388d1efd13447397013511ae7f3a4ac2fb66d6025f11b2e6071de5ce6(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SentinelAlertRuleAnomalyDuplicateSingleSelectObservation]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25af4ec007543e9e4e5c13d07257cdef96137744639a4355400a6aac45e902b4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02eb840376dff19d4ad7bf0819d69c994163f4b0f50b84d58ef138d280ac7f97(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__774fdaf4024e12f4dac53b2342edf77c0bc61868ab088939fedf0351d160f97f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b2d2b299de4ab3ae751829303546befc282ef1ea84eed7484cc3d8e253dac997(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SentinelAlertRuleAnomalyDuplicateSingleSelectObservation]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__108d049ca2818f2de5ebba88951231caadebb651fa0706bb3ee5e7af507bf12e(
    *,
    name: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25291cd18d4a5dee4f740c52aaac6adc2dda376ace65ce6ecb35f0d6be867299(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__771b48deaab352bf55fb1d721e2aba2681d6a23439dd551f7fe9359724041f79(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7fa7309eebca212c7149e90d737ff9a72a029ab057cfb6905ce48e2affec2d91(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ed4d6a728ee5ff54d9f0710640981c2e650c7e16b2f9e158bd7302e1cdc84ec(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e076887a4961d6143175688fe1962b0918724f1531df69663ed4067e8538dda(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b20b95711d55ad8176d5e1106b7ddc7ddf0717cbecb7a84dd98b844e98100f15(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SentinelAlertRuleAnomalyDuplicateThresholdObservation]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__82cf4b2168a5be39def97003443b79ed8ac482ace312a0a697f3cc40222ea9de(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4cd796703836f4037fdcc3467dbcf2e49975eb7c823592c7c7ec0e2759dce27f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4ceaba0106b4d97c07057c149ad43d97fded996739f196e031019e1af7147d3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99f9e5af351b5a105ee89f5ba6cd7c8a84efd33e01182f3b1c5d1481c5e28cd1(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SentinelAlertRuleAnomalyDuplicateThresholdObservation]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__925542c36bb6c82bd85e2a921964f41d910c607df407e2c485cc96f51326d019(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    read: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__07c50d375f3cebc2a0b2125c7c810532ac97596b2884c2bdcf9176461e1fd7f1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c7d8ca9e4d904588c49bc72f770f0429eaa7251cb6338ed95fae5ace3e551f4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca4e470bef03c8851601888ca97971243b3889fe2b3602cee34c654d0e7e90dd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e5deafd463c25f9150aa5a8e661ebf703c0c7d9ddfed6a4f17be3a41d7d599e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4216d0328d141984806b4b2b57421a0f46121217f1e7e49f83fa81ff2db26b00(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__919224961610dfdb6395102173892560b82a644ea8d756059bd8d6957fb3e84d(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SentinelAlertRuleAnomalyDuplicateTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
