r'''
# `azurerm_automanage_configuration`

Refer to the Terraform Registry for docs: [`azurerm_automanage_configuration`](https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automanage_configuration).
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


class AutomanageConfiguration(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.automanageConfiguration.AutomanageConfiguration",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automanage_configuration azurerm_automanage_configuration}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        location: builtins.str,
        name: builtins.str,
        resource_group_name: builtins.str,
        antimalware: typing.Optional[typing.Union["AutomanageConfigurationAntimalware", typing.Dict[builtins.str, typing.Any]]] = None,
        automation_account_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        azure_security_baseline: typing.Optional[typing.Union["AutomanageConfigurationAzureSecurityBaseline", typing.Dict[builtins.str, typing.Any]]] = None,
        backup: typing.Optional[typing.Union["AutomanageConfigurationBackup", typing.Dict[builtins.str, typing.Any]]] = None,
        boot_diagnostics_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        defender_for_cloud_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        guest_configuration_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        log_analytics_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        status_change_alert_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["AutomanageConfigurationTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automanage_configuration azurerm_automanage_configuration} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param location: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automanage_configuration#location AutomanageConfiguration#location}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automanage_configuration#name AutomanageConfiguration#name}.
        :param resource_group_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automanage_configuration#resource_group_name AutomanageConfiguration#resource_group_name}.
        :param antimalware: antimalware block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automanage_configuration#antimalware AutomanageConfiguration#antimalware}
        :param automation_account_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automanage_configuration#automation_account_enabled AutomanageConfiguration#automation_account_enabled}.
        :param azure_security_baseline: azure_security_baseline block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automanage_configuration#azure_security_baseline AutomanageConfiguration#azure_security_baseline}
        :param backup: backup block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automanage_configuration#backup AutomanageConfiguration#backup}
        :param boot_diagnostics_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automanage_configuration#boot_diagnostics_enabled AutomanageConfiguration#boot_diagnostics_enabled}.
        :param defender_for_cloud_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automanage_configuration#defender_for_cloud_enabled AutomanageConfiguration#defender_for_cloud_enabled}.
        :param guest_configuration_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automanage_configuration#guest_configuration_enabled AutomanageConfiguration#guest_configuration_enabled}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automanage_configuration#id AutomanageConfiguration#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param log_analytics_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automanage_configuration#log_analytics_enabled AutomanageConfiguration#log_analytics_enabled}.
        :param status_change_alert_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automanage_configuration#status_change_alert_enabled AutomanageConfiguration#status_change_alert_enabled}.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automanage_configuration#tags AutomanageConfiguration#tags}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automanage_configuration#timeouts AutomanageConfiguration#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4bf8edfd8d5df3948bdc6feab0461de4a1bd8f6ea2c1ee19bffcfc32193a394c)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = AutomanageConfigurationConfig(
            location=location,
            name=name,
            resource_group_name=resource_group_name,
            antimalware=antimalware,
            automation_account_enabled=automation_account_enabled,
            azure_security_baseline=azure_security_baseline,
            backup=backup,
            boot_diagnostics_enabled=boot_diagnostics_enabled,
            defender_for_cloud_enabled=defender_for_cloud_enabled,
            guest_configuration_enabled=guest_configuration_enabled,
            id=id,
            log_analytics_enabled=log_analytics_enabled,
            status_change_alert_enabled=status_change_alert_enabled,
            tags=tags,
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
        '''Generates CDKTF code for importing a AutomanageConfiguration resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the AutomanageConfiguration to import.
        :param import_from_id: The id of the existing AutomanageConfiguration that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automanage_configuration#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the AutomanageConfiguration to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__78272d94e9e27f1f5eda9d3f218bf3800fb0861ba6bdb95a63ea8a24865a886a)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putAntimalware")
    def put_antimalware(
        self,
        *,
        exclusions: typing.Optional[typing.Union["AutomanageConfigurationAntimalwareExclusions", typing.Dict[builtins.str, typing.Any]]] = None,
        real_time_protection_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        scheduled_scan_day: typing.Optional[jsii.Number] = None,
        scheduled_scan_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        scheduled_scan_time_in_minutes: typing.Optional[jsii.Number] = None,
        scheduled_scan_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param exclusions: exclusions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automanage_configuration#exclusions AutomanageConfiguration#exclusions}
        :param real_time_protection_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automanage_configuration#real_time_protection_enabled AutomanageConfiguration#real_time_protection_enabled}.
        :param scheduled_scan_day: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automanage_configuration#scheduled_scan_day AutomanageConfiguration#scheduled_scan_day}.
        :param scheduled_scan_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automanage_configuration#scheduled_scan_enabled AutomanageConfiguration#scheduled_scan_enabled}.
        :param scheduled_scan_time_in_minutes: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automanage_configuration#scheduled_scan_time_in_minutes AutomanageConfiguration#scheduled_scan_time_in_minutes}.
        :param scheduled_scan_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automanage_configuration#scheduled_scan_type AutomanageConfiguration#scheduled_scan_type}.
        '''
        value = AutomanageConfigurationAntimalware(
            exclusions=exclusions,
            real_time_protection_enabled=real_time_protection_enabled,
            scheduled_scan_day=scheduled_scan_day,
            scheduled_scan_enabled=scheduled_scan_enabled,
            scheduled_scan_time_in_minutes=scheduled_scan_time_in_minutes,
            scheduled_scan_type=scheduled_scan_type,
        )

        return typing.cast(None, jsii.invoke(self, "putAntimalware", [value]))

    @jsii.member(jsii_name="putAzureSecurityBaseline")
    def put_azure_security_baseline(
        self,
        *,
        assignment_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param assignment_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automanage_configuration#assignment_type AutomanageConfiguration#assignment_type}.
        '''
        value = AutomanageConfigurationAzureSecurityBaseline(
            assignment_type=assignment_type
        )

        return typing.cast(None, jsii.invoke(self, "putAzureSecurityBaseline", [value]))

    @jsii.member(jsii_name="putBackup")
    def put_backup(
        self,
        *,
        instant_rp_retention_range_in_days: typing.Optional[jsii.Number] = None,
        policy_name: typing.Optional[builtins.str] = None,
        retention_policy: typing.Optional[typing.Union["AutomanageConfigurationBackupRetentionPolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        schedule_policy: typing.Optional[typing.Union["AutomanageConfigurationBackupSchedulePolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        time_zone: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param instant_rp_retention_range_in_days: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automanage_configuration#instant_rp_retention_range_in_days AutomanageConfiguration#instant_rp_retention_range_in_days}.
        :param policy_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automanage_configuration#policy_name AutomanageConfiguration#policy_name}.
        :param retention_policy: retention_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automanage_configuration#retention_policy AutomanageConfiguration#retention_policy}
        :param schedule_policy: schedule_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automanage_configuration#schedule_policy AutomanageConfiguration#schedule_policy}
        :param time_zone: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automanage_configuration#time_zone AutomanageConfiguration#time_zone}.
        '''
        value = AutomanageConfigurationBackup(
            instant_rp_retention_range_in_days=instant_rp_retention_range_in_days,
            policy_name=policy_name,
            retention_policy=retention_policy,
            schedule_policy=schedule_policy,
            time_zone=time_zone,
        )

        return typing.cast(None, jsii.invoke(self, "putBackup", [value]))

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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automanage_configuration#create AutomanageConfiguration#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automanage_configuration#delete AutomanageConfiguration#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automanage_configuration#read AutomanageConfiguration#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automanage_configuration#update AutomanageConfiguration#update}.
        '''
        value = AutomanageConfigurationTimeouts(
            create=create, delete=delete, read=read, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetAntimalware")
    def reset_antimalware(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAntimalware", []))

    @jsii.member(jsii_name="resetAutomationAccountEnabled")
    def reset_automation_account_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAutomationAccountEnabled", []))

    @jsii.member(jsii_name="resetAzureSecurityBaseline")
    def reset_azure_security_baseline(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAzureSecurityBaseline", []))

    @jsii.member(jsii_name="resetBackup")
    def reset_backup(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBackup", []))

    @jsii.member(jsii_name="resetBootDiagnosticsEnabled")
    def reset_boot_diagnostics_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBootDiagnosticsEnabled", []))

    @jsii.member(jsii_name="resetDefenderForCloudEnabled")
    def reset_defender_for_cloud_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDefenderForCloudEnabled", []))

    @jsii.member(jsii_name="resetGuestConfigurationEnabled")
    def reset_guest_configuration_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGuestConfigurationEnabled", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetLogAnalyticsEnabled")
    def reset_log_analytics_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLogAnalyticsEnabled", []))

    @jsii.member(jsii_name="resetStatusChangeAlertEnabled")
    def reset_status_change_alert_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStatusChangeAlertEnabled", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

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
    @jsii.member(jsii_name="antimalware")
    def antimalware(self) -> "AutomanageConfigurationAntimalwareOutputReference":
        return typing.cast("AutomanageConfigurationAntimalwareOutputReference", jsii.get(self, "antimalware"))

    @builtins.property
    @jsii.member(jsii_name="azureSecurityBaseline")
    def azure_security_baseline(
        self,
    ) -> "AutomanageConfigurationAzureSecurityBaselineOutputReference":
        return typing.cast("AutomanageConfigurationAzureSecurityBaselineOutputReference", jsii.get(self, "azureSecurityBaseline"))

    @builtins.property
    @jsii.member(jsii_name="backup")
    def backup(self) -> "AutomanageConfigurationBackupOutputReference":
        return typing.cast("AutomanageConfigurationBackupOutputReference", jsii.get(self, "backup"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "AutomanageConfigurationTimeoutsOutputReference":
        return typing.cast("AutomanageConfigurationTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="antimalwareInput")
    def antimalware_input(
        self,
    ) -> typing.Optional["AutomanageConfigurationAntimalware"]:
        return typing.cast(typing.Optional["AutomanageConfigurationAntimalware"], jsii.get(self, "antimalwareInput"))

    @builtins.property
    @jsii.member(jsii_name="automationAccountEnabledInput")
    def automation_account_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "automationAccountEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="azureSecurityBaselineInput")
    def azure_security_baseline_input(
        self,
    ) -> typing.Optional["AutomanageConfigurationAzureSecurityBaseline"]:
        return typing.cast(typing.Optional["AutomanageConfigurationAzureSecurityBaseline"], jsii.get(self, "azureSecurityBaselineInput"))

    @builtins.property
    @jsii.member(jsii_name="backupInput")
    def backup_input(self) -> typing.Optional["AutomanageConfigurationBackup"]:
        return typing.cast(typing.Optional["AutomanageConfigurationBackup"], jsii.get(self, "backupInput"))

    @builtins.property
    @jsii.member(jsii_name="bootDiagnosticsEnabledInput")
    def boot_diagnostics_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "bootDiagnosticsEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="defenderForCloudEnabledInput")
    def defender_for_cloud_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "defenderForCloudEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="guestConfigurationEnabledInput")
    def guest_configuration_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "guestConfigurationEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="locationInput")
    def location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "locationInput"))

    @builtins.property
    @jsii.member(jsii_name="logAnalyticsEnabledInput")
    def log_analytics_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "logAnalyticsEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceGroupNameInput")
    def resource_group_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "resourceGroupNameInput"))

    @builtins.property
    @jsii.member(jsii_name="statusChangeAlertEnabledInput")
    def status_change_alert_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "statusChangeAlertEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsInput")
    def tags_input(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "tagsInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "AutomanageConfigurationTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "AutomanageConfigurationTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="automationAccountEnabled")
    def automation_account_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "automationAccountEnabled"))

    @automation_account_enabled.setter
    def automation_account_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c8e20969043a0e60d3ccc464a21873965996c39c80608d35b840d93ffe9b4ec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "automationAccountEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="bootDiagnosticsEnabled")
    def boot_diagnostics_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "bootDiagnosticsEnabled"))

    @boot_diagnostics_enabled.setter
    def boot_diagnostics_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__28a5e48f30907ff12f558baf02ffe66d1b4eee98e4c8b363a3d727f35384667a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bootDiagnosticsEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="defenderForCloudEnabled")
    def defender_for_cloud_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "defenderForCloudEnabled"))

    @defender_for_cloud_enabled.setter
    def defender_for_cloud_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__539952120a9753fb9abce9d76eb0e06176d812619a39c46f8395ecdac789bcd6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defenderForCloudEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="guestConfigurationEnabled")
    def guest_configuration_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "guestConfigurationEnabled"))

    @guest_configuration_enabled.setter
    def guest_configuration_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d5d55ad1f6f39e165e59607b985c7e6235b1b0391970453c30919b8509bca127)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "guestConfigurationEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7143ccf4957085d3d1274fcfe37de5f2e40bdd842611b357a8610a1326478da3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c5a252d8d6a7d5f7aa02f7733fa15993edac7c881c59852225b551f95226ca23)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="logAnalyticsEnabled")
    def log_analytics_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "logAnalyticsEnabled"))

    @log_analytics_enabled.setter
    def log_analytics_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7ca4994a592b2673727d39ac4067c850be05e40d37d62f46105c9812ffdab1ef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "logAnalyticsEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d06d6f87f6613a3515992b9be7c873c7d506d023566e5d09797c30bd276578c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resourceGroupName")
    def resource_group_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourceGroupName"))

    @resource_group_name.setter
    def resource_group_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b809809582785dc8e0647c79d9eefd37fe692297f03a733d2cd380b684bf0aa7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceGroupName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="statusChangeAlertEnabled")
    def status_change_alert_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "statusChangeAlertEnabled"))

    @status_change_alert_enabled.setter
    def status_change_alert_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__de37291325d364e90dd1ba8bf2e3b4cfe4df16fced03ecb1c35b6029baf33e0e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "statusChangeAlertEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__92acc0f21178f169b82acfa843253647f1d0a6dc801cb8a39280c00f6c3baa9a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.automanageConfiguration.AutomanageConfigurationAntimalware",
    jsii_struct_bases=[],
    name_mapping={
        "exclusions": "exclusions",
        "real_time_protection_enabled": "realTimeProtectionEnabled",
        "scheduled_scan_day": "scheduledScanDay",
        "scheduled_scan_enabled": "scheduledScanEnabled",
        "scheduled_scan_time_in_minutes": "scheduledScanTimeInMinutes",
        "scheduled_scan_type": "scheduledScanType",
    },
)
class AutomanageConfigurationAntimalware:
    def __init__(
        self,
        *,
        exclusions: typing.Optional[typing.Union["AutomanageConfigurationAntimalwareExclusions", typing.Dict[builtins.str, typing.Any]]] = None,
        real_time_protection_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        scheduled_scan_day: typing.Optional[jsii.Number] = None,
        scheduled_scan_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        scheduled_scan_time_in_minutes: typing.Optional[jsii.Number] = None,
        scheduled_scan_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param exclusions: exclusions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automanage_configuration#exclusions AutomanageConfiguration#exclusions}
        :param real_time_protection_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automanage_configuration#real_time_protection_enabled AutomanageConfiguration#real_time_protection_enabled}.
        :param scheduled_scan_day: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automanage_configuration#scheduled_scan_day AutomanageConfiguration#scheduled_scan_day}.
        :param scheduled_scan_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automanage_configuration#scheduled_scan_enabled AutomanageConfiguration#scheduled_scan_enabled}.
        :param scheduled_scan_time_in_minutes: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automanage_configuration#scheduled_scan_time_in_minutes AutomanageConfiguration#scheduled_scan_time_in_minutes}.
        :param scheduled_scan_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automanage_configuration#scheduled_scan_type AutomanageConfiguration#scheduled_scan_type}.
        '''
        if isinstance(exclusions, dict):
            exclusions = AutomanageConfigurationAntimalwareExclusions(**exclusions)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f87650b0b7cd438005b39a2199a9b3cc2a8446a58dbe9058a7331309f6a8164)
            check_type(argname="argument exclusions", value=exclusions, expected_type=type_hints["exclusions"])
            check_type(argname="argument real_time_protection_enabled", value=real_time_protection_enabled, expected_type=type_hints["real_time_protection_enabled"])
            check_type(argname="argument scheduled_scan_day", value=scheduled_scan_day, expected_type=type_hints["scheduled_scan_day"])
            check_type(argname="argument scheduled_scan_enabled", value=scheduled_scan_enabled, expected_type=type_hints["scheduled_scan_enabled"])
            check_type(argname="argument scheduled_scan_time_in_minutes", value=scheduled_scan_time_in_minutes, expected_type=type_hints["scheduled_scan_time_in_minutes"])
            check_type(argname="argument scheduled_scan_type", value=scheduled_scan_type, expected_type=type_hints["scheduled_scan_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if exclusions is not None:
            self._values["exclusions"] = exclusions
        if real_time_protection_enabled is not None:
            self._values["real_time_protection_enabled"] = real_time_protection_enabled
        if scheduled_scan_day is not None:
            self._values["scheduled_scan_day"] = scheduled_scan_day
        if scheduled_scan_enabled is not None:
            self._values["scheduled_scan_enabled"] = scheduled_scan_enabled
        if scheduled_scan_time_in_minutes is not None:
            self._values["scheduled_scan_time_in_minutes"] = scheduled_scan_time_in_minutes
        if scheduled_scan_type is not None:
            self._values["scheduled_scan_type"] = scheduled_scan_type

    @builtins.property
    def exclusions(
        self,
    ) -> typing.Optional["AutomanageConfigurationAntimalwareExclusions"]:
        '''exclusions block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automanage_configuration#exclusions AutomanageConfiguration#exclusions}
        '''
        result = self._values.get("exclusions")
        return typing.cast(typing.Optional["AutomanageConfigurationAntimalwareExclusions"], result)

    @builtins.property
    def real_time_protection_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automanage_configuration#real_time_protection_enabled AutomanageConfiguration#real_time_protection_enabled}.'''
        result = self._values.get("real_time_protection_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def scheduled_scan_day(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automanage_configuration#scheduled_scan_day AutomanageConfiguration#scheduled_scan_day}.'''
        result = self._values.get("scheduled_scan_day")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def scheduled_scan_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automanage_configuration#scheduled_scan_enabled AutomanageConfiguration#scheduled_scan_enabled}.'''
        result = self._values.get("scheduled_scan_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def scheduled_scan_time_in_minutes(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automanage_configuration#scheduled_scan_time_in_minutes AutomanageConfiguration#scheduled_scan_time_in_minutes}.'''
        result = self._values.get("scheduled_scan_time_in_minutes")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def scheduled_scan_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automanage_configuration#scheduled_scan_type AutomanageConfiguration#scheduled_scan_type}.'''
        result = self._values.get("scheduled_scan_type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AutomanageConfigurationAntimalware(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.automanageConfiguration.AutomanageConfigurationAntimalwareExclusions",
    jsii_struct_bases=[],
    name_mapping={
        "extensions": "extensions",
        "paths": "paths",
        "processes": "processes",
    },
)
class AutomanageConfigurationAntimalwareExclusions:
    def __init__(
        self,
        *,
        extensions: typing.Optional[builtins.str] = None,
        paths: typing.Optional[builtins.str] = None,
        processes: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param extensions: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automanage_configuration#extensions AutomanageConfiguration#extensions}.
        :param paths: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automanage_configuration#paths AutomanageConfiguration#paths}.
        :param processes: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automanage_configuration#processes AutomanageConfiguration#processes}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__548b30bc103376491ebe1d5621ebe2a2cd65d44589abc7ea451955e0d9db7ede)
            check_type(argname="argument extensions", value=extensions, expected_type=type_hints["extensions"])
            check_type(argname="argument paths", value=paths, expected_type=type_hints["paths"])
            check_type(argname="argument processes", value=processes, expected_type=type_hints["processes"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if extensions is not None:
            self._values["extensions"] = extensions
        if paths is not None:
            self._values["paths"] = paths
        if processes is not None:
            self._values["processes"] = processes

    @builtins.property
    def extensions(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automanage_configuration#extensions AutomanageConfiguration#extensions}.'''
        result = self._values.get("extensions")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def paths(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automanage_configuration#paths AutomanageConfiguration#paths}.'''
        result = self._values.get("paths")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def processes(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automanage_configuration#processes AutomanageConfiguration#processes}.'''
        result = self._values.get("processes")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AutomanageConfigurationAntimalwareExclusions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AutomanageConfigurationAntimalwareExclusionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.automanageConfiguration.AutomanageConfigurationAntimalwareExclusionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__37f2a8eee239781dc740883e864858036728afbc6f88561a57d08566fe3cbc1c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetExtensions")
    def reset_extensions(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExtensions", []))

    @jsii.member(jsii_name="resetPaths")
    def reset_paths(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPaths", []))

    @jsii.member(jsii_name="resetProcesses")
    def reset_processes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProcesses", []))

    @builtins.property
    @jsii.member(jsii_name="extensionsInput")
    def extensions_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "extensionsInput"))

    @builtins.property
    @jsii.member(jsii_name="pathsInput")
    def paths_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pathsInput"))

    @builtins.property
    @jsii.member(jsii_name="processesInput")
    def processes_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "processesInput"))

    @builtins.property
    @jsii.member(jsii_name="extensions")
    def extensions(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "extensions"))

    @extensions.setter
    def extensions(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__74afd5b456a468304e847674b29015574c5a2ba0bcab7aa1a984f02a3adb0d3d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "extensions", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="paths")
    def paths(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "paths"))

    @paths.setter
    def paths(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d3f81eb06a153b60023d8f64921b33cc2dbe789921c57d5e3ee6488c2737b51a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "paths", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="processes")
    def processes(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "processes"))

    @processes.setter
    def processes(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4d6d933464a2f167d0aea40fcd78ab26f71ef33e1efaf6ceabb2776d9ce7c238)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "processes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AutomanageConfigurationAntimalwareExclusions]:
        return typing.cast(typing.Optional[AutomanageConfigurationAntimalwareExclusions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AutomanageConfigurationAntimalwareExclusions],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f29209505ad37f052fa2245e0958ee1d1a1de3fb80a84d7b8fa51f8684edc142)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AutomanageConfigurationAntimalwareOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.automanageConfiguration.AutomanageConfigurationAntimalwareOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8ff28e678c67a018be51c29e876ed89b27b9884faa2891931382b60d26911191)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putExclusions")
    def put_exclusions(
        self,
        *,
        extensions: typing.Optional[builtins.str] = None,
        paths: typing.Optional[builtins.str] = None,
        processes: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param extensions: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automanage_configuration#extensions AutomanageConfiguration#extensions}.
        :param paths: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automanage_configuration#paths AutomanageConfiguration#paths}.
        :param processes: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automanage_configuration#processes AutomanageConfiguration#processes}.
        '''
        value = AutomanageConfigurationAntimalwareExclusions(
            extensions=extensions, paths=paths, processes=processes
        )

        return typing.cast(None, jsii.invoke(self, "putExclusions", [value]))

    @jsii.member(jsii_name="resetExclusions")
    def reset_exclusions(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExclusions", []))

    @jsii.member(jsii_name="resetRealTimeProtectionEnabled")
    def reset_real_time_protection_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRealTimeProtectionEnabled", []))

    @jsii.member(jsii_name="resetScheduledScanDay")
    def reset_scheduled_scan_day(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetScheduledScanDay", []))

    @jsii.member(jsii_name="resetScheduledScanEnabled")
    def reset_scheduled_scan_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetScheduledScanEnabled", []))

    @jsii.member(jsii_name="resetScheduledScanTimeInMinutes")
    def reset_scheduled_scan_time_in_minutes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetScheduledScanTimeInMinutes", []))

    @jsii.member(jsii_name="resetScheduledScanType")
    def reset_scheduled_scan_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetScheduledScanType", []))

    @builtins.property
    @jsii.member(jsii_name="exclusions")
    def exclusions(self) -> AutomanageConfigurationAntimalwareExclusionsOutputReference:
        return typing.cast(AutomanageConfigurationAntimalwareExclusionsOutputReference, jsii.get(self, "exclusions"))

    @builtins.property
    @jsii.member(jsii_name="exclusionsInput")
    def exclusions_input(
        self,
    ) -> typing.Optional[AutomanageConfigurationAntimalwareExclusions]:
        return typing.cast(typing.Optional[AutomanageConfigurationAntimalwareExclusions], jsii.get(self, "exclusionsInput"))

    @builtins.property
    @jsii.member(jsii_name="realTimeProtectionEnabledInput")
    def real_time_protection_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "realTimeProtectionEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="scheduledScanDayInput")
    def scheduled_scan_day_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "scheduledScanDayInput"))

    @builtins.property
    @jsii.member(jsii_name="scheduledScanEnabledInput")
    def scheduled_scan_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "scheduledScanEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="scheduledScanTimeInMinutesInput")
    def scheduled_scan_time_in_minutes_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "scheduledScanTimeInMinutesInput"))

    @builtins.property
    @jsii.member(jsii_name="scheduledScanTypeInput")
    def scheduled_scan_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "scheduledScanTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="realTimeProtectionEnabled")
    def real_time_protection_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "realTimeProtectionEnabled"))

    @real_time_protection_enabled.setter
    def real_time_protection_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8a580c94df6a4a325c6297f52d71615d6e5ee9b7dd0f02d53b4b67d2bc1c42f1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "realTimeProtectionEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="scheduledScanDay")
    def scheduled_scan_day(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "scheduledScanDay"))

    @scheduled_scan_day.setter
    def scheduled_scan_day(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__235901e6c5781a00ff51c171b9384df6a44f982e2d336c0cd3eb426d2ddae504)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scheduledScanDay", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="scheduledScanEnabled")
    def scheduled_scan_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "scheduledScanEnabled"))

    @scheduled_scan_enabled.setter
    def scheduled_scan_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0d8a35190bf675e129f4acd6b928c861ab10fb8929a77c1bfe27589b0fc252ea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scheduledScanEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="scheduledScanTimeInMinutes")
    def scheduled_scan_time_in_minutes(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "scheduledScanTimeInMinutes"))

    @scheduled_scan_time_in_minutes.setter
    def scheduled_scan_time_in_minutes(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c344c28b3f0e5f0bd8900d9445cfc2b7041aeca83c6f32c57eae953e989deca4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scheduledScanTimeInMinutes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="scheduledScanType")
    def scheduled_scan_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "scheduledScanType"))

    @scheduled_scan_type.setter
    def scheduled_scan_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3b3212a6b4974dc178509fb3aa5ac6c58a844619ba5071c653ed08c5049f76d1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scheduledScanType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[AutomanageConfigurationAntimalware]:
        return typing.cast(typing.Optional[AutomanageConfigurationAntimalware], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AutomanageConfigurationAntimalware],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd480d3c1618d8a3f02e735df223f0ca3e67f1a038463bb38bf05572d34f6f2b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.automanageConfiguration.AutomanageConfigurationAzureSecurityBaseline",
    jsii_struct_bases=[],
    name_mapping={"assignment_type": "assignmentType"},
)
class AutomanageConfigurationAzureSecurityBaseline:
    def __init__(
        self,
        *,
        assignment_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param assignment_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automanage_configuration#assignment_type AutomanageConfiguration#assignment_type}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__75ac1994442bc83c581b22ffcdb1ec4d9c50c4b63ef5b12576d9ec38da1ae047)
            check_type(argname="argument assignment_type", value=assignment_type, expected_type=type_hints["assignment_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if assignment_type is not None:
            self._values["assignment_type"] = assignment_type

    @builtins.property
    def assignment_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automanage_configuration#assignment_type AutomanageConfiguration#assignment_type}.'''
        result = self._values.get("assignment_type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AutomanageConfigurationAzureSecurityBaseline(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AutomanageConfigurationAzureSecurityBaselineOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.automanageConfiguration.AutomanageConfigurationAzureSecurityBaselineOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__02b46199b026cd300be2295207713faccfff30fd8a4e0993bc6653b0ea68c526)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAssignmentType")
    def reset_assignment_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAssignmentType", []))

    @builtins.property
    @jsii.member(jsii_name="assignmentTypeInput")
    def assignment_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "assignmentTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="assignmentType")
    def assignment_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "assignmentType"))

    @assignment_type.setter
    def assignment_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3eed58231ae5576abfa77f155e48b7633ce9811425eabf126c514302ad260a71)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "assignmentType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AutomanageConfigurationAzureSecurityBaseline]:
        return typing.cast(typing.Optional[AutomanageConfigurationAzureSecurityBaseline], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AutomanageConfigurationAzureSecurityBaseline],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0fd6310d530cdc47de3a1a0b8ad39f0984deab6235711424f428bc9bb64debf9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.automanageConfiguration.AutomanageConfigurationBackup",
    jsii_struct_bases=[],
    name_mapping={
        "instant_rp_retention_range_in_days": "instantRpRetentionRangeInDays",
        "policy_name": "policyName",
        "retention_policy": "retentionPolicy",
        "schedule_policy": "schedulePolicy",
        "time_zone": "timeZone",
    },
)
class AutomanageConfigurationBackup:
    def __init__(
        self,
        *,
        instant_rp_retention_range_in_days: typing.Optional[jsii.Number] = None,
        policy_name: typing.Optional[builtins.str] = None,
        retention_policy: typing.Optional[typing.Union["AutomanageConfigurationBackupRetentionPolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        schedule_policy: typing.Optional[typing.Union["AutomanageConfigurationBackupSchedulePolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        time_zone: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param instant_rp_retention_range_in_days: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automanage_configuration#instant_rp_retention_range_in_days AutomanageConfiguration#instant_rp_retention_range_in_days}.
        :param policy_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automanage_configuration#policy_name AutomanageConfiguration#policy_name}.
        :param retention_policy: retention_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automanage_configuration#retention_policy AutomanageConfiguration#retention_policy}
        :param schedule_policy: schedule_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automanage_configuration#schedule_policy AutomanageConfiguration#schedule_policy}
        :param time_zone: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automanage_configuration#time_zone AutomanageConfiguration#time_zone}.
        '''
        if isinstance(retention_policy, dict):
            retention_policy = AutomanageConfigurationBackupRetentionPolicy(**retention_policy)
        if isinstance(schedule_policy, dict):
            schedule_policy = AutomanageConfigurationBackupSchedulePolicy(**schedule_policy)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__59bc6c705f4bd04241d6e73b2618d0b369fbff0971e262aac68cd57a1e760798)
            check_type(argname="argument instant_rp_retention_range_in_days", value=instant_rp_retention_range_in_days, expected_type=type_hints["instant_rp_retention_range_in_days"])
            check_type(argname="argument policy_name", value=policy_name, expected_type=type_hints["policy_name"])
            check_type(argname="argument retention_policy", value=retention_policy, expected_type=type_hints["retention_policy"])
            check_type(argname="argument schedule_policy", value=schedule_policy, expected_type=type_hints["schedule_policy"])
            check_type(argname="argument time_zone", value=time_zone, expected_type=type_hints["time_zone"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if instant_rp_retention_range_in_days is not None:
            self._values["instant_rp_retention_range_in_days"] = instant_rp_retention_range_in_days
        if policy_name is not None:
            self._values["policy_name"] = policy_name
        if retention_policy is not None:
            self._values["retention_policy"] = retention_policy
        if schedule_policy is not None:
            self._values["schedule_policy"] = schedule_policy
        if time_zone is not None:
            self._values["time_zone"] = time_zone

    @builtins.property
    def instant_rp_retention_range_in_days(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automanage_configuration#instant_rp_retention_range_in_days AutomanageConfiguration#instant_rp_retention_range_in_days}.'''
        result = self._values.get("instant_rp_retention_range_in_days")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def policy_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automanage_configuration#policy_name AutomanageConfiguration#policy_name}.'''
        result = self._values.get("policy_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def retention_policy(
        self,
    ) -> typing.Optional["AutomanageConfigurationBackupRetentionPolicy"]:
        '''retention_policy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automanage_configuration#retention_policy AutomanageConfiguration#retention_policy}
        '''
        result = self._values.get("retention_policy")
        return typing.cast(typing.Optional["AutomanageConfigurationBackupRetentionPolicy"], result)

    @builtins.property
    def schedule_policy(
        self,
    ) -> typing.Optional["AutomanageConfigurationBackupSchedulePolicy"]:
        '''schedule_policy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automanage_configuration#schedule_policy AutomanageConfiguration#schedule_policy}
        '''
        result = self._values.get("schedule_policy")
        return typing.cast(typing.Optional["AutomanageConfigurationBackupSchedulePolicy"], result)

    @builtins.property
    def time_zone(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automanage_configuration#time_zone AutomanageConfiguration#time_zone}.'''
        result = self._values.get("time_zone")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AutomanageConfigurationBackup(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AutomanageConfigurationBackupOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.automanageConfiguration.AutomanageConfigurationBackupOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__655a42eff7549dc6fb3080ad76ff3064c1ee71d7d4d420b6d73fdc36d2a3099c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putRetentionPolicy")
    def put_retention_policy(
        self,
        *,
        daily_schedule: typing.Optional[typing.Union["AutomanageConfigurationBackupRetentionPolicyDailySchedule", typing.Dict[builtins.str, typing.Any]]] = None,
        retention_policy_type: typing.Optional[builtins.str] = None,
        weekly_schedule: typing.Optional[typing.Union["AutomanageConfigurationBackupRetentionPolicyWeeklySchedule", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param daily_schedule: daily_schedule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automanage_configuration#daily_schedule AutomanageConfiguration#daily_schedule}
        :param retention_policy_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automanage_configuration#retention_policy_type AutomanageConfiguration#retention_policy_type}.
        :param weekly_schedule: weekly_schedule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automanage_configuration#weekly_schedule AutomanageConfiguration#weekly_schedule}
        '''
        value = AutomanageConfigurationBackupRetentionPolicy(
            daily_schedule=daily_schedule,
            retention_policy_type=retention_policy_type,
            weekly_schedule=weekly_schedule,
        )

        return typing.cast(None, jsii.invoke(self, "putRetentionPolicy", [value]))

    @jsii.member(jsii_name="putSchedulePolicy")
    def put_schedule_policy(
        self,
        *,
        schedule_policy_type: typing.Optional[builtins.str] = None,
        schedule_run_days: typing.Optional[typing.Sequence[builtins.str]] = None,
        schedule_run_frequency: typing.Optional[builtins.str] = None,
        schedule_run_times: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param schedule_policy_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automanage_configuration#schedule_policy_type AutomanageConfiguration#schedule_policy_type}.
        :param schedule_run_days: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automanage_configuration#schedule_run_days AutomanageConfiguration#schedule_run_days}.
        :param schedule_run_frequency: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automanage_configuration#schedule_run_frequency AutomanageConfiguration#schedule_run_frequency}.
        :param schedule_run_times: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automanage_configuration#schedule_run_times AutomanageConfiguration#schedule_run_times}.
        '''
        value = AutomanageConfigurationBackupSchedulePolicy(
            schedule_policy_type=schedule_policy_type,
            schedule_run_days=schedule_run_days,
            schedule_run_frequency=schedule_run_frequency,
            schedule_run_times=schedule_run_times,
        )

        return typing.cast(None, jsii.invoke(self, "putSchedulePolicy", [value]))

    @jsii.member(jsii_name="resetInstantRpRetentionRangeInDays")
    def reset_instant_rp_retention_range_in_days(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInstantRpRetentionRangeInDays", []))

    @jsii.member(jsii_name="resetPolicyName")
    def reset_policy_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPolicyName", []))

    @jsii.member(jsii_name="resetRetentionPolicy")
    def reset_retention_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRetentionPolicy", []))

    @jsii.member(jsii_name="resetSchedulePolicy")
    def reset_schedule_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSchedulePolicy", []))

    @jsii.member(jsii_name="resetTimeZone")
    def reset_time_zone(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeZone", []))

    @builtins.property
    @jsii.member(jsii_name="retentionPolicy")
    def retention_policy(
        self,
    ) -> "AutomanageConfigurationBackupRetentionPolicyOutputReference":
        return typing.cast("AutomanageConfigurationBackupRetentionPolicyOutputReference", jsii.get(self, "retentionPolicy"))

    @builtins.property
    @jsii.member(jsii_name="schedulePolicy")
    def schedule_policy(
        self,
    ) -> "AutomanageConfigurationBackupSchedulePolicyOutputReference":
        return typing.cast("AutomanageConfigurationBackupSchedulePolicyOutputReference", jsii.get(self, "schedulePolicy"))

    @builtins.property
    @jsii.member(jsii_name="instantRpRetentionRangeInDaysInput")
    def instant_rp_retention_range_in_days_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "instantRpRetentionRangeInDaysInput"))

    @builtins.property
    @jsii.member(jsii_name="policyNameInput")
    def policy_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "policyNameInput"))

    @builtins.property
    @jsii.member(jsii_name="retentionPolicyInput")
    def retention_policy_input(
        self,
    ) -> typing.Optional["AutomanageConfigurationBackupRetentionPolicy"]:
        return typing.cast(typing.Optional["AutomanageConfigurationBackupRetentionPolicy"], jsii.get(self, "retentionPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="schedulePolicyInput")
    def schedule_policy_input(
        self,
    ) -> typing.Optional["AutomanageConfigurationBackupSchedulePolicy"]:
        return typing.cast(typing.Optional["AutomanageConfigurationBackupSchedulePolicy"], jsii.get(self, "schedulePolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="timeZoneInput")
    def time_zone_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "timeZoneInput"))

    @builtins.property
    @jsii.member(jsii_name="instantRpRetentionRangeInDays")
    def instant_rp_retention_range_in_days(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "instantRpRetentionRangeInDays"))

    @instant_rp_retention_range_in_days.setter
    def instant_rp_retention_range_in_days(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bbf1d440b55d782cb10a84cbab9f31aeacd19643989f5f6547bc24c6b76bd064)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "instantRpRetentionRangeInDays", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="policyName")
    def policy_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "policyName"))

    @policy_name.setter
    def policy_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bdf4e355e95d46f390181426ee1db175ff282ef3a569c5527c75cab8297eb046)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "policyName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="timeZone")
    def time_zone(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "timeZone"))

    @time_zone.setter
    def time_zone(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8fa8f701ae832e4864557b2d754d91347700c628e84ba49bdbd9a0437c4e5dc9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timeZone", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[AutomanageConfigurationBackup]:
        return typing.cast(typing.Optional[AutomanageConfigurationBackup], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AutomanageConfigurationBackup],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__42f21f0f02521badfbbc9720574fbeab5897d6e7e766476135fdaddf0322fe1a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.automanageConfiguration.AutomanageConfigurationBackupRetentionPolicy",
    jsii_struct_bases=[],
    name_mapping={
        "daily_schedule": "dailySchedule",
        "retention_policy_type": "retentionPolicyType",
        "weekly_schedule": "weeklySchedule",
    },
)
class AutomanageConfigurationBackupRetentionPolicy:
    def __init__(
        self,
        *,
        daily_schedule: typing.Optional[typing.Union["AutomanageConfigurationBackupRetentionPolicyDailySchedule", typing.Dict[builtins.str, typing.Any]]] = None,
        retention_policy_type: typing.Optional[builtins.str] = None,
        weekly_schedule: typing.Optional[typing.Union["AutomanageConfigurationBackupRetentionPolicyWeeklySchedule", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param daily_schedule: daily_schedule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automanage_configuration#daily_schedule AutomanageConfiguration#daily_schedule}
        :param retention_policy_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automanage_configuration#retention_policy_type AutomanageConfiguration#retention_policy_type}.
        :param weekly_schedule: weekly_schedule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automanage_configuration#weekly_schedule AutomanageConfiguration#weekly_schedule}
        '''
        if isinstance(daily_schedule, dict):
            daily_schedule = AutomanageConfigurationBackupRetentionPolicyDailySchedule(**daily_schedule)
        if isinstance(weekly_schedule, dict):
            weekly_schedule = AutomanageConfigurationBackupRetentionPolicyWeeklySchedule(**weekly_schedule)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fd152e61d885ce4a0d581ec026abb0a63219b1ef4dc6f6e392231c417b295d04)
            check_type(argname="argument daily_schedule", value=daily_schedule, expected_type=type_hints["daily_schedule"])
            check_type(argname="argument retention_policy_type", value=retention_policy_type, expected_type=type_hints["retention_policy_type"])
            check_type(argname="argument weekly_schedule", value=weekly_schedule, expected_type=type_hints["weekly_schedule"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if daily_schedule is not None:
            self._values["daily_schedule"] = daily_schedule
        if retention_policy_type is not None:
            self._values["retention_policy_type"] = retention_policy_type
        if weekly_schedule is not None:
            self._values["weekly_schedule"] = weekly_schedule

    @builtins.property
    def daily_schedule(
        self,
    ) -> typing.Optional["AutomanageConfigurationBackupRetentionPolicyDailySchedule"]:
        '''daily_schedule block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automanage_configuration#daily_schedule AutomanageConfiguration#daily_schedule}
        '''
        result = self._values.get("daily_schedule")
        return typing.cast(typing.Optional["AutomanageConfigurationBackupRetentionPolicyDailySchedule"], result)

    @builtins.property
    def retention_policy_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automanage_configuration#retention_policy_type AutomanageConfiguration#retention_policy_type}.'''
        result = self._values.get("retention_policy_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def weekly_schedule(
        self,
    ) -> typing.Optional["AutomanageConfigurationBackupRetentionPolicyWeeklySchedule"]:
        '''weekly_schedule block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automanage_configuration#weekly_schedule AutomanageConfiguration#weekly_schedule}
        '''
        result = self._values.get("weekly_schedule")
        return typing.cast(typing.Optional["AutomanageConfigurationBackupRetentionPolicyWeeklySchedule"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AutomanageConfigurationBackupRetentionPolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.automanageConfiguration.AutomanageConfigurationBackupRetentionPolicyDailySchedule",
    jsii_struct_bases=[],
    name_mapping={
        "retention_duration": "retentionDuration",
        "retention_times": "retentionTimes",
    },
)
class AutomanageConfigurationBackupRetentionPolicyDailySchedule:
    def __init__(
        self,
        *,
        retention_duration: typing.Optional[typing.Union["AutomanageConfigurationBackupRetentionPolicyDailyScheduleRetentionDuration", typing.Dict[builtins.str, typing.Any]]] = None,
        retention_times: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param retention_duration: retention_duration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automanage_configuration#retention_duration AutomanageConfiguration#retention_duration}
        :param retention_times: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automanage_configuration#retention_times AutomanageConfiguration#retention_times}.
        '''
        if isinstance(retention_duration, dict):
            retention_duration = AutomanageConfigurationBackupRetentionPolicyDailyScheduleRetentionDuration(**retention_duration)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__40a69ee39a1ef64c4cdf1169b8f97c00f65593e08c1e784fe3a5bdaf693fc008)
            check_type(argname="argument retention_duration", value=retention_duration, expected_type=type_hints["retention_duration"])
            check_type(argname="argument retention_times", value=retention_times, expected_type=type_hints["retention_times"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if retention_duration is not None:
            self._values["retention_duration"] = retention_duration
        if retention_times is not None:
            self._values["retention_times"] = retention_times

    @builtins.property
    def retention_duration(
        self,
    ) -> typing.Optional["AutomanageConfigurationBackupRetentionPolicyDailyScheduleRetentionDuration"]:
        '''retention_duration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automanage_configuration#retention_duration AutomanageConfiguration#retention_duration}
        '''
        result = self._values.get("retention_duration")
        return typing.cast(typing.Optional["AutomanageConfigurationBackupRetentionPolicyDailyScheduleRetentionDuration"], result)

    @builtins.property
    def retention_times(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automanage_configuration#retention_times AutomanageConfiguration#retention_times}.'''
        result = self._values.get("retention_times")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AutomanageConfigurationBackupRetentionPolicyDailySchedule(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AutomanageConfigurationBackupRetentionPolicyDailyScheduleOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.automanageConfiguration.AutomanageConfigurationBackupRetentionPolicyDailyScheduleOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c77d297d9cef499adaeae924ae04f8b5e35e72f7afdb045b035f17081a50eb9b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putRetentionDuration")
    def put_retention_duration(
        self,
        *,
        count: typing.Optional[jsii.Number] = None,
        duration_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param count: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automanage_configuration#count AutomanageConfiguration#count}.
        :param duration_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automanage_configuration#duration_type AutomanageConfiguration#duration_type}.
        '''
        value = AutomanageConfigurationBackupRetentionPolicyDailyScheduleRetentionDuration(
            count=count, duration_type=duration_type
        )

        return typing.cast(None, jsii.invoke(self, "putRetentionDuration", [value]))

    @jsii.member(jsii_name="resetRetentionDuration")
    def reset_retention_duration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRetentionDuration", []))

    @jsii.member(jsii_name="resetRetentionTimes")
    def reset_retention_times(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRetentionTimes", []))

    @builtins.property
    @jsii.member(jsii_name="retentionDuration")
    def retention_duration(
        self,
    ) -> "AutomanageConfigurationBackupRetentionPolicyDailyScheduleRetentionDurationOutputReference":
        return typing.cast("AutomanageConfigurationBackupRetentionPolicyDailyScheduleRetentionDurationOutputReference", jsii.get(self, "retentionDuration"))

    @builtins.property
    @jsii.member(jsii_name="retentionDurationInput")
    def retention_duration_input(
        self,
    ) -> typing.Optional["AutomanageConfigurationBackupRetentionPolicyDailyScheduleRetentionDuration"]:
        return typing.cast(typing.Optional["AutomanageConfigurationBackupRetentionPolicyDailyScheduleRetentionDuration"], jsii.get(self, "retentionDurationInput"))

    @builtins.property
    @jsii.member(jsii_name="retentionTimesInput")
    def retention_times_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "retentionTimesInput"))

    @builtins.property
    @jsii.member(jsii_name="retentionTimes")
    def retention_times(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "retentionTimes"))

    @retention_times.setter
    def retention_times(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__86d3865f90fd56515389f8017890b9098e65969526845a92945f65e42673245b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "retentionTimes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AutomanageConfigurationBackupRetentionPolicyDailySchedule]:
        return typing.cast(typing.Optional[AutomanageConfigurationBackupRetentionPolicyDailySchedule], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AutomanageConfigurationBackupRetentionPolicyDailySchedule],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e08499ca77e2301c845e6748cffa24dc701902cae817629616c2e6d55c8b7188)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.automanageConfiguration.AutomanageConfigurationBackupRetentionPolicyDailyScheduleRetentionDuration",
    jsii_struct_bases=[],
    name_mapping={"count": "count", "duration_type": "durationType"},
)
class AutomanageConfigurationBackupRetentionPolicyDailyScheduleRetentionDuration:
    def __init__(
        self,
        *,
        count: typing.Optional[jsii.Number] = None,
        duration_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param count: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automanage_configuration#count AutomanageConfiguration#count}.
        :param duration_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automanage_configuration#duration_type AutomanageConfiguration#duration_type}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c1f70c65f224b72f8ea594bfbf06792aa4af0dadf04f109238c2587b579ac90a)
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument duration_type", value=duration_type, expected_type=type_hints["duration_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if count is not None:
            self._values["count"] = count
        if duration_type is not None:
            self._values["duration_type"] = duration_type

    @builtins.property
    def count(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automanage_configuration#count AutomanageConfiguration#count}.'''
        result = self._values.get("count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def duration_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automanage_configuration#duration_type AutomanageConfiguration#duration_type}.'''
        result = self._values.get("duration_type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AutomanageConfigurationBackupRetentionPolicyDailyScheduleRetentionDuration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AutomanageConfigurationBackupRetentionPolicyDailyScheduleRetentionDurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.automanageConfiguration.AutomanageConfigurationBackupRetentionPolicyDailyScheduleRetentionDurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c1ccba957ec81120b859a5d40b8e64a4580b5a7ab4f6757de920f9b9b0521e68)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCount")
    def reset_count(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCount", []))

    @jsii.member(jsii_name="resetDurationType")
    def reset_duration_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDurationType", []))

    @builtins.property
    @jsii.member(jsii_name="countInput")
    def count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "countInput"))

    @builtins.property
    @jsii.member(jsii_name="durationTypeInput")
    def duration_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "durationTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="count")
    def count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "count"))

    @count.setter
    def count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e2a637cba3c99ebf6c85d8f8549602d4494a7013fccd86d477423d86402bc46e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "count", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="durationType")
    def duration_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "durationType"))

    @duration_type.setter
    def duration_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__db7317561b60b102263d480580c23df63a710d54931f578d1e8fc77a8a00c88c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "durationType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AutomanageConfigurationBackupRetentionPolicyDailyScheduleRetentionDuration]:
        return typing.cast(typing.Optional[AutomanageConfigurationBackupRetentionPolicyDailyScheduleRetentionDuration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AutomanageConfigurationBackupRetentionPolicyDailyScheduleRetentionDuration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e7b46a9327954b41d4e8337349d193b5165859f8ef655d44d31ae21f3285560d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AutomanageConfigurationBackupRetentionPolicyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.automanageConfiguration.AutomanageConfigurationBackupRetentionPolicyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__19fd44ae16426baa1acbf991de5f8b832e8920feff601fda01bfed1d85b1ac77)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putDailySchedule")
    def put_daily_schedule(
        self,
        *,
        retention_duration: typing.Optional[typing.Union[AutomanageConfigurationBackupRetentionPolicyDailyScheduleRetentionDuration, typing.Dict[builtins.str, typing.Any]]] = None,
        retention_times: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param retention_duration: retention_duration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automanage_configuration#retention_duration AutomanageConfiguration#retention_duration}
        :param retention_times: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automanage_configuration#retention_times AutomanageConfiguration#retention_times}.
        '''
        value = AutomanageConfigurationBackupRetentionPolicyDailySchedule(
            retention_duration=retention_duration, retention_times=retention_times
        )

        return typing.cast(None, jsii.invoke(self, "putDailySchedule", [value]))

    @jsii.member(jsii_name="putWeeklySchedule")
    def put_weekly_schedule(
        self,
        *,
        retention_duration: typing.Optional[typing.Union["AutomanageConfigurationBackupRetentionPolicyWeeklyScheduleRetentionDuration", typing.Dict[builtins.str, typing.Any]]] = None,
        retention_times: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param retention_duration: retention_duration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automanage_configuration#retention_duration AutomanageConfiguration#retention_duration}
        :param retention_times: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automanage_configuration#retention_times AutomanageConfiguration#retention_times}.
        '''
        value = AutomanageConfigurationBackupRetentionPolicyWeeklySchedule(
            retention_duration=retention_duration, retention_times=retention_times
        )

        return typing.cast(None, jsii.invoke(self, "putWeeklySchedule", [value]))

    @jsii.member(jsii_name="resetDailySchedule")
    def reset_daily_schedule(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDailySchedule", []))

    @jsii.member(jsii_name="resetRetentionPolicyType")
    def reset_retention_policy_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRetentionPolicyType", []))

    @jsii.member(jsii_name="resetWeeklySchedule")
    def reset_weekly_schedule(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWeeklySchedule", []))

    @builtins.property
    @jsii.member(jsii_name="dailySchedule")
    def daily_schedule(
        self,
    ) -> AutomanageConfigurationBackupRetentionPolicyDailyScheduleOutputReference:
        return typing.cast(AutomanageConfigurationBackupRetentionPolicyDailyScheduleOutputReference, jsii.get(self, "dailySchedule"))

    @builtins.property
    @jsii.member(jsii_name="weeklySchedule")
    def weekly_schedule(
        self,
    ) -> "AutomanageConfigurationBackupRetentionPolicyWeeklyScheduleOutputReference":
        return typing.cast("AutomanageConfigurationBackupRetentionPolicyWeeklyScheduleOutputReference", jsii.get(self, "weeklySchedule"))

    @builtins.property
    @jsii.member(jsii_name="dailyScheduleInput")
    def daily_schedule_input(
        self,
    ) -> typing.Optional[AutomanageConfigurationBackupRetentionPolicyDailySchedule]:
        return typing.cast(typing.Optional[AutomanageConfigurationBackupRetentionPolicyDailySchedule], jsii.get(self, "dailyScheduleInput"))

    @builtins.property
    @jsii.member(jsii_name="retentionPolicyTypeInput")
    def retention_policy_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "retentionPolicyTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="weeklyScheduleInput")
    def weekly_schedule_input(
        self,
    ) -> typing.Optional["AutomanageConfigurationBackupRetentionPolicyWeeklySchedule"]:
        return typing.cast(typing.Optional["AutomanageConfigurationBackupRetentionPolicyWeeklySchedule"], jsii.get(self, "weeklyScheduleInput"))

    @builtins.property
    @jsii.member(jsii_name="retentionPolicyType")
    def retention_policy_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "retentionPolicyType"))

    @retention_policy_type.setter
    def retention_policy_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__56a0812d2c24aedd292f6da365feac0d506911daacfcf06480428b39580fe34e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "retentionPolicyType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AutomanageConfigurationBackupRetentionPolicy]:
        return typing.cast(typing.Optional[AutomanageConfigurationBackupRetentionPolicy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AutomanageConfigurationBackupRetentionPolicy],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2b7961a720b4a84d26a76d6c97fb3148d26af0f68189d8a8f0faf0cb692e34f7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.automanageConfiguration.AutomanageConfigurationBackupRetentionPolicyWeeklySchedule",
    jsii_struct_bases=[],
    name_mapping={
        "retention_duration": "retentionDuration",
        "retention_times": "retentionTimes",
    },
)
class AutomanageConfigurationBackupRetentionPolicyWeeklySchedule:
    def __init__(
        self,
        *,
        retention_duration: typing.Optional[typing.Union["AutomanageConfigurationBackupRetentionPolicyWeeklyScheduleRetentionDuration", typing.Dict[builtins.str, typing.Any]]] = None,
        retention_times: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param retention_duration: retention_duration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automanage_configuration#retention_duration AutomanageConfiguration#retention_duration}
        :param retention_times: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automanage_configuration#retention_times AutomanageConfiguration#retention_times}.
        '''
        if isinstance(retention_duration, dict):
            retention_duration = AutomanageConfigurationBackupRetentionPolicyWeeklyScheduleRetentionDuration(**retention_duration)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__15120c102b8d7317a70a98a1e0311ccb5b8e78ad8ce3e15ae8529d9cf5031a8c)
            check_type(argname="argument retention_duration", value=retention_duration, expected_type=type_hints["retention_duration"])
            check_type(argname="argument retention_times", value=retention_times, expected_type=type_hints["retention_times"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if retention_duration is not None:
            self._values["retention_duration"] = retention_duration
        if retention_times is not None:
            self._values["retention_times"] = retention_times

    @builtins.property
    def retention_duration(
        self,
    ) -> typing.Optional["AutomanageConfigurationBackupRetentionPolicyWeeklyScheduleRetentionDuration"]:
        '''retention_duration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automanage_configuration#retention_duration AutomanageConfiguration#retention_duration}
        '''
        result = self._values.get("retention_duration")
        return typing.cast(typing.Optional["AutomanageConfigurationBackupRetentionPolicyWeeklyScheduleRetentionDuration"], result)

    @builtins.property
    def retention_times(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automanage_configuration#retention_times AutomanageConfiguration#retention_times}.'''
        result = self._values.get("retention_times")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AutomanageConfigurationBackupRetentionPolicyWeeklySchedule(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AutomanageConfigurationBackupRetentionPolicyWeeklyScheduleOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.automanageConfiguration.AutomanageConfigurationBackupRetentionPolicyWeeklyScheduleOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0f403434eaccd2add943be2970d35115c54a3dced2d9ccbd132965f932a5cc8e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putRetentionDuration")
    def put_retention_duration(
        self,
        *,
        count: typing.Optional[jsii.Number] = None,
        duration_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param count: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automanage_configuration#count AutomanageConfiguration#count}.
        :param duration_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automanage_configuration#duration_type AutomanageConfiguration#duration_type}.
        '''
        value = AutomanageConfigurationBackupRetentionPolicyWeeklyScheduleRetentionDuration(
            count=count, duration_type=duration_type
        )

        return typing.cast(None, jsii.invoke(self, "putRetentionDuration", [value]))

    @jsii.member(jsii_name="resetRetentionDuration")
    def reset_retention_duration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRetentionDuration", []))

    @jsii.member(jsii_name="resetRetentionTimes")
    def reset_retention_times(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRetentionTimes", []))

    @builtins.property
    @jsii.member(jsii_name="retentionDuration")
    def retention_duration(
        self,
    ) -> "AutomanageConfigurationBackupRetentionPolicyWeeklyScheduleRetentionDurationOutputReference":
        return typing.cast("AutomanageConfigurationBackupRetentionPolicyWeeklyScheduleRetentionDurationOutputReference", jsii.get(self, "retentionDuration"))

    @builtins.property
    @jsii.member(jsii_name="retentionDurationInput")
    def retention_duration_input(
        self,
    ) -> typing.Optional["AutomanageConfigurationBackupRetentionPolicyWeeklyScheduleRetentionDuration"]:
        return typing.cast(typing.Optional["AutomanageConfigurationBackupRetentionPolicyWeeklyScheduleRetentionDuration"], jsii.get(self, "retentionDurationInput"))

    @builtins.property
    @jsii.member(jsii_name="retentionTimesInput")
    def retention_times_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "retentionTimesInput"))

    @builtins.property
    @jsii.member(jsii_name="retentionTimes")
    def retention_times(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "retentionTimes"))

    @retention_times.setter
    def retention_times(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8353560bbb315c4afc281748111cc1050c0dbde707d213c0d76377dc4248f914)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "retentionTimes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AutomanageConfigurationBackupRetentionPolicyWeeklySchedule]:
        return typing.cast(typing.Optional[AutomanageConfigurationBackupRetentionPolicyWeeklySchedule], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AutomanageConfigurationBackupRetentionPolicyWeeklySchedule],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__07b3b00c4e7cad80a46d68218ad37e2c04c5c025046aa9c88d239628ecb0e4d4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.automanageConfiguration.AutomanageConfigurationBackupRetentionPolicyWeeklyScheduleRetentionDuration",
    jsii_struct_bases=[],
    name_mapping={"count": "count", "duration_type": "durationType"},
)
class AutomanageConfigurationBackupRetentionPolicyWeeklyScheduleRetentionDuration:
    def __init__(
        self,
        *,
        count: typing.Optional[jsii.Number] = None,
        duration_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param count: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automanage_configuration#count AutomanageConfiguration#count}.
        :param duration_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automanage_configuration#duration_type AutomanageConfiguration#duration_type}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4cc2636b42f253415563f6ea2bf83b631910676dadb238989dee85e44bc029f0)
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument duration_type", value=duration_type, expected_type=type_hints["duration_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if count is not None:
            self._values["count"] = count
        if duration_type is not None:
            self._values["duration_type"] = duration_type

    @builtins.property
    def count(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automanage_configuration#count AutomanageConfiguration#count}.'''
        result = self._values.get("count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def duration_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automanage_configuration#duration_type AutomanageConfiguration#duration_type}.'''
        result = self._values.get("duration_type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AutomanageConfigurationBackupRetentionPolicyWeeklyScheduleRetentionDuration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AutomanageConfigurationBackupRetentionPolicyWeeklyScheduleRetentionDurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.automanageConfiguration.AutomanageConfigurationBackupRetentionPolicyWeeklyScheduleRetentionDurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fdfb70fc588d3db47680ad35b8c86ca23b856fc010cd62988a68698ae2dfc75b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCount")
    def reset_count(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCount", []))

    @jsii.member(jsii_name="resetDurationType")
    def reset_duration_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDurationType", []))

    @builtins.property
    @jsii.member(jsii_name="countInput")
    def count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "countInput"))

    @builtins.property
    @jsii.member(jsii_name="durationTypeInput")
    def duration_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "durationTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="count")
    def count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "count"))

    @count.setter
    def count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__47d92d9ca662dff7160ab52db363e42f295ff31dbc2f48a7904a542a8076a1ab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "count", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="durationType")
    def duration_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "durationType"))

    @duration_type.setter
    def duration_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e72d7997650ffab2ff29359122935fb3809d27faf64a2f3bafdb37f360ff06d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "durationType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AutomanageConfigurationBackupRetentionPolicyWeeklyScheduleRetentionDuration]:
        return typing.cast(typing.Optional[AutomanageConfigurationBackupRetentionPolicyWeeklyScheduleRetentionDuration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AutomanageConfigurationBackupRetentionPolicyWeeklyScheduleRetentionDuration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__870800dfc2d1943f22e9c05d70df199927df64609a5037dfd368a5403c192441)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.automanageConfiguration.AutomanageConfigurationBackupSchedulePolicy",
    jsii_struct_bases=[],
    name_mapping={
        "schedule_policy_type": "schedulePolicyType",
        "schedule_run_days": "scheduleRunDays",
        "schedule_run_frequency": "scheduleRunFrequency",
        "schedule_run_times": "scheduleRunTimes",
    },
)
class AutomanageConfigurationBackupSchedulePolicy:
    def __init__(
        self,
        *,
        schedule_policy_type: typing.Optional[builtins.str] = None,
        schedule_run_days: typing.Optional[typing.Sequence[builtins.str]] = None,
        schedule_run_frequency: typing.Optional[builtins.str] = None,
        schedule_run_times: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param schedule_policy_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automanage_configuration#schedule_policy_type AutomanageConfiguration#schedule_policy_type}.
        :param schedule_run_days: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automanage_configuration#schedule_run_days AutomanageConfiguration#schedule_run_days}.
        :param schedule_run_frequency: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automanage_configuration#schedule_run_frequency AutomanageConfiguration#schedule_run_frequency}.
        :param schedule_run_times: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automanage_configuration#schedule_run_times AutomanageConfiguration#schedule_run_times}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__91323e5462197be72339cf521a28ea5b7888fb4dfce19adbcb19b0c19475905b)
            check_type(argname="argument schedule_policy_type", value=schedule_policy_type, expected_type=type_hints["schedule_policy_type"])
            check_type(argname="argument schedule_run_days", value=schedule_run_days, expected_type=type_hints["schedule_run_days"])
            check_type(argname="argument schedule_run_frequency", value=schedule_run_frequency, expected_type=type_hints["schedule_run_frequency"])
            check_type(argname="argument schedule_run_times", value=schedule_run_times, expected_type=type_hints["schedule_run_times"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if schedule_policy_type is not None:
            self._values["schedule_policy_type"] = schedule_policy_type
        if schedule_run_days is not None:
            self._values["schedule_run_days"] = schedule_run_days
        if schedule_run_frequency is not None:
            self._values["schedule_run_frequency"] = schedule_run_frequency
        if schedule_run_times is not None:
            self._values["schedule_run_times"] = schedule_run_times

    @builtins.property
    def schedule_policy_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automanage_configuration#schedule_policy_type AutomanageConfiguration#schedule_policy_type}.'''
        result = self._values.get("schedule_policy_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def schedule_run_days(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automanage_configuration#schedule_run_days AutomanageConfiguration#schedule_run_days}.'''
        result = self._values.get("schedule_run_days")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def schedule_run_frequency(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automanage_configuration#schedule_run_frequency AutomanageConfiguration#schedule_run_frequency}.'''
        result = self._values.get("schedule_run_frequency")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def schedule_run_times(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automanage_configuration#schedule_run_times AutomanageConfiguration#schedule_run_times}.'''
        result = self._values.get("schedule_run_times")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AutomanageConfigurationBackupSchedulePolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AutomanageConfigurationBackupSchedulePolicyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.automanageConfiguration.AutomanageConfigurationBackupSchedulePolicyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c359b344a8068a870dda9b0b51f64f4427b716e9a069b83e1a221d13c41bfdc7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetSchedulePolicyType")
    def reset_schedule_policy_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSchedulePolicyType", []))

    @jsii.member(jsii_name="resetScheduleRunDays")
    def reset_schedule_run_days(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetScheduleRunDays", []))

    @jsii.member(jsii_name="resetScheduleRunFrequency")
    def reset_schedule_run_frequency(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetScheduleRunFrequency", []))

    @jsii.member(jsii_name="resetScheduleRunTimes")
    def reset_schedule_run_times(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetScheduleRunTimes", []))

    @builtins.property
    @jsii.member(jsii_name="schedulePolicyTypeInput")
    def schedule_policy_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "schedulePolicyTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="scheduleRunDaysInput")
    def schedule_run_days_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "scheduleRunDaysInput"))

    @builtins.property
    @jsii.member(jsii_name="scheduleRunFrequencyInput")
    def schedule_run_frequency_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "scheduleRunFrequencyInput"))

    @builtins.property
    @jsii.member(jsii_name="scheduleRunTimesInput")
    def schedule_run_times_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "scheduleRunTimesInput"))

    @builtins.property
    @jsii.member(jsii_name="schedulePolicyType")
    def schedule_policy_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "schedulePolicyType"))

    @schedule_policy_type.setter
    def schedule_policy_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4bb481188ec89a2b6266d3867d4f9a1ff4a9ece87bc1fe39138ba7bce9ae81e1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "schedulePolicyType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="scheduleRunDays")
    def schedule_run_days(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "scheduleRunDays"))

    @schedule_run_days.setter
    def schedule_run_days(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac762e92e6178793504d9741d0555f06f40cabcc2de8272d7e82dbdccc75b65f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scheduleRunDays", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="scheduleRunFrequency")
    def schedule_run_frequency(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "scheduleRunFrequency"))

    @schedule_run_frequency.setter
    def schedule_run_frequency(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__655fc258ddc67e42e6c790f0cec6d62d5a124533865f8a094ae0b21f98fd7839)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scheduleRunFrequency", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="scheduleRunTimes")
    def schedule_run_times(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "scheduleRunTimes"))

    @schedule_run_times.setter
    def schedule_run_times(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a5d546570336da17ac6171245fae82407779006aee379f913cbee828cb3e89b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scheduleRunTimes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AutomanageConfigurationBackupSchedulePolicy]:
        return typing.cast(typing.Optional[AutomanageConfigurationBackupSchedulePolicy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AutomanageConfigurationBackupSchedulePolicy],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ffeecf5767f809ad1b1557bfb79e011b45912d04cc5ef24c9d06887210a70e9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.automanageConfiguration.AutomanageConfigurationConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "location": "location",
        "name": "name",
        "resource_group_name": "resourceGroupName",
        "antimalware": "antimalware",
        "automation_account_enabled": "automationAccountEnabled",
        "azure_security_baseline": "azureSecurityBaseline",
        "backup": "backup",
        "boot_diagnostics_enabled": "bootDiagnosticsEnabled",
        "defender_for_cloud_enabled": "defenderForCloudEnabled",
        "guest_configuration_enabled": "guestConfigurationEnabled",
        "id": "id",
        "log_analytics_enabled": "logAnalyticsEnabled",
        "status_change_alert_enabled": "statusChangeAlertEnabled",
        "tags": "tags",
        "timeouts": "timeouts",
    },
)
class AutomanageConfigurationConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        location: builtins.str,
        name: builtins.str,
        resource_group_name: builtins.str,
        antimalware: typing.Optional[typing.Union[AutomanageConfigurationAntimalware, typing.Dict[builtins.str, typing.Any]]] = None,
        automation_account_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        azure_security_baseline: typing.Optional[typing.Union[AutomanageConfigurationAzureSecurityBaseline, typing.Dict[builtins.str, typing.Any]]] = None,
        backup: typing.Optional[typing.Union[AutomanageConfigurationBackup, typing.Dict[builtins.str, typing.Any]]] = None,
        boot_diagnostics_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        defender_for_cloud_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        guest_configuration_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        log_analytics_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        status_change_alert_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["AutomanageConfigurationTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param location: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automanage_configuration#location AutomanageConfiguration#location}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automanage_configuration#name AutomanageConfiguration#name}.
        :param resource_group_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automanage_configuration#resource_group_name AutomanageConfiguration#resource_group_name}.
        :param antimalware: antimalware block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automanage_configuration#antimalware AutomanageConfiguration#antimalware}
        :param automation_account_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automanage_configuration#automation_account_enabled AutomanageConfiguration#automation_account_enabled}.
        :param azure_security_baseline: azure_security_baseline block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automanage_configuration#azure_security_baseline AutomanageConfiguration#azure_security_baseline}
        :param backup: backup block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automanage_configuration#backup AutomanageConfiguration#backup}
        :param boot_diagnostics_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automanage_configuration#boot_diagnostics_enabled AutomanageConfiguration#boot_diagnostics_enabled}.
        :param defender_for_cloud_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automanage_configuration#defender_for_cloud_enabled AutomanageConfiguration#defender_for_cloud_enabled}.
        :param guest_configuration_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automanage_configuration#guest_configuration_enabled AutomanageConfiguration#guest_configuration_enabled}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automanage_configuration#id AutomanageConfiguration#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param log_analytics_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automanage_configuration#log_analytics_enabled AutomanageConfiguration#log_analytics_enabled}.
        :param status_change_alert_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automanage_configuration#status_change_alert_enabled AutomanageConfiguration#status_change_alert_enabled}.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automanage_configuration#tags AutomanageConfiguration#tags}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automanage_configuration#timeouts AutomanageConfiguration#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(antimalware, dict):
            antimalware = AutomanageConfigurationAntimalware(**antimalware)
        if isinstance(azure_security_baseline, dict):
            azure_security_baseline = AutomanageConfigurationAzureSecurityBaseline(**azure_security_baseline)
        if isinstance(backup, dict):
            backup = AutomanageConfigurationBackup(**backup)
        if isinstance(timeouts, dict):
            timeouts = AutomanageConfigurationTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__33a19bcb6f00592868a7bc71124a422ccf40122cf2f8e42ed0beac80bfafcd73)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument resource_group_name", value=resource_group_name, expected_type=type_hints["resource_group_name"])
            check_type(argname="argument antimalware", value=antimalware, expected_type=type_hints["antimalware"])
            check_type(argname="argument automation_account_enabled", value=automation_account_enabled, expected_type=type_hints["automation_account_enabled"])
            check_type(argname="argument azure_security_baseline", value=azure_security_baseline, expected_type=type_hints["azure_security_baseline"])
            check_type(argname="argument backup", value=backup, expected_type=type_hints["backup"])
            check_type(argname="argument boot_diagnostics_enabled", value=boot_diagnostics_enabled, expected_type=type_hints["boot_diagnostics_enabled"])
            check_type(argname="argument defender_for_cloud_enabled", value=defender_for_cloud_enabled, expected_type=type_hints["defender_for_cloud_enabled"])
            check_type(argname="argument guest_configuration_enabled", value=guest_configuration_enabled, expected_type=type_hints["guest_configuration_enabled"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument log_analytics_enabled", value=log_analytics_enabled, expected_type=type_hints["log_analytics_enabled"])
            check_type(argname="argument status_change_alert_enabled", value=status_change_alert_enabled, expected_type=type_hints["status_change_alert_enabled"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "location": location,
            "name": name,
            "resource_group_name": resource_group_name,
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
        if antimalware is not None:
            self._values["antimalware"] = antimalware
        if automation_account_enabled is not None:
            self._values["automation_account_enabled"] = automation_account_enabled
        if azure_security_baseline is not None:
            self._values["azure_security_baseline"] = azure_security_baseline
        if backup is not None:
            self._values["backup"] = backup
        if boot_diagnostics_enabled is not None:
            self._values["boot_diagnostics_enabled"] = boot_diagnostics_enabled
        if defender_for_cloud_enabled is not None:
            self._values["defender_for_cloud_enabled"] = defender_for_cloud_enabled
        if guest_configuration_enabled is not None:
            self._values["guest_configuration_enabled"] = guest_configuration_enabled
        if id is not None:
            self._values["id"] = id
        if log_analytics_enabled is not None:
            self._values["log_analytics_enabled"] = log_analytics_enabled
        if status_change_alert_enabled is not None:
            self._values["status_change_alert_enabled"] = status_change_alert_enabled
        if tags is not None:
            self._values["tags"] = tags
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
    def location(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automanage_configuration#location AutomanageConfiguration#location}.'''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automanage_configuration#name AutomanageConfiguration#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def resource_group_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automanage_configuration#resource_group_name AutomanageConfiguration#resource_group_name}.'''
        result = self._values.get("resource_group_name")
        assert result is not None, "Required property 'resource_group_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def antimalware(self) -> typing.Optional[AutomanageConfigurationAntimalware]:
        '''antimalware block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automanage_configuration#antimalware AutomanageConfiguration#antimalware}
        '''
        result = self._values.get("antimalware")
        return typing.cast(typing.Optional[AutomanageConfigurationAntimalware], result)

    @builtins.property
    def automation_account_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automanage_configuration#automation_account_enabled AutomanageConfiguration#automation_account_enabled}.'''
        result = self._values.get("automation_account_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def azure_security_baseline(
        self,
    ) -> typing.Optional[AutomanageConfigurationAzureSecurityBaseline]:
        '''azure_security_baseline block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automanage_configuration#azure_security_baseline AutomanageConfiguration#azure_security_baseline}
        '''
        result = self._values.get("azure_security_baseline")
        return typing.cast(typing.Optional[AutomanageConfigurationAzureSecurityBaseline], result)

    @builtins.property
    def backup(self) -> typing.Optional[AutomanageConfigurationBackup]:
        '''backup block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automanage_configuration#backup AutomanageConfiguration#backup}
        '''
        result = self._values.get("backup")
        return typing.cast(typing.Optional[AutomanageConfigurationBackup], result)

    @builtins.property
    def boot_diagnostics_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automanage_configuration#boot_diagnostics_enabled AutomanageConfiguration#boot_diagnostics_enabled}.'''
        result = self._values.get("boot_diagnostics_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def defender_for_cloud_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automanage_configuration#defender_for_cloud_enabled AutomanageConfiguration#defender_for_cloud_enabled}.'''
        result = self._values.get("defender_for_cloud_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def guest_configuration_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automanage_configuration#guest_configuration_enabled AutomanageConfiguration#guest_configuration_enabled}.'''
        result = self._values.get("guest_configuration_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automanage_configuration#id AutomanageConfiguration#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def log_analytics_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automanage_configuration#log_analytics_enabled AutomanageConfiguration#log_analytics_enabled}.'''
        result = self._values.get("log_analytics_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def status_change_alert_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automanage_configuration#status_change_alert_enabled AutomanageConfiguration#status_change_alert_enabled}.'''
        result = self._values.get("status_change_alert_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automanage_configuration#tags AutomanageConfiguration#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["AutomanageConfigurationTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automanage_configuration#timeouts AutomanageConfiguration#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["AutomanageConfigurationTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AutomanageConfigurationConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.automanageConfiguration.AutomanageConfigurationTimeouts",
    jsii_struct_bases=[],
    name_mapping={
        "create": "create",
        "delete": "delete",
        "read": "read",
        "update": "update",
    },
)
class AutomanageConfigurationTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automanage_configuration#create AutomanageConfiguration#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automanage_configuration#delete AutomanageConfiguration#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automanage_configuration#read AutomanageConfiguration#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automanage_configuration#update AutomanageConfiguration#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e77a667f22aa911ab67e937b8d6577f12dcf272418a3bb5e2c9bc6d8cc73f577)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automanage_configuration#create AutomanageConfiguration#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automanage_configuration#delete AutomanageConfiguration#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def read(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automanage_configuration#read AutomanageConfiguration#read}.'''
        result = self._values.get("read")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automanage_configuration#update AutomanageConfiguration#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AutomanageConfigurationTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AutomanageConfigurationTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.automanageConfiguration.AutomanageConfigurationTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__478071835ab24f48a5a1c44588e9040119e816fb5d77aaf7ab4e843e2fe0016f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__741bbbafd56fdb002bc83c4441b894ca7282dcfa2843b2dadc9c9d60df3528dd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__17abae9724c09fbc30f47a079ea12c202f5246fa90ecddff450fbf486ef2759b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="read")
    def read(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "read"))

    @read.setter
    def read(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a8349888958a6eed2ddc74d1f45adbb034842208e3204cb5451af9c2d0165b95)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "read", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bfd02e14bac71d1da866bd777ca68140d5b705e89cd067cb38e0031121bbb687)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AutomanageConfigurationTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AutomanageConfigurationTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AutomanageConfigurationTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7304250ae4256a2c8fe5968f2b18d26df89b5192dd0cd6ecf146dca43e04fadc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "AutomanageConfiguration",
    "AutomanageConfigurationAntimalware",
    "AutomanageConfigurationAntimalwareExclusions",
    "AutomanageConfigurationAntimalwareExclusionsOutputReference",
    "AutomanageConfigurationAntimalwareOutputReference",
    "AutomanageConfigurationAzureSecurityBaseline",
    "AutomanageConfigurationAzureSecurityBaselineOutputReference",
    "AutomanageConfigurationBackup",
    "AutomanageConfigurationBackupOutputReference",
    "AutomanageConfigurationBackupRetentionPolicy",
    "AutomanageConfigurationBackupRetentionPolicyDailySchedule",
    "AutomanageConfigurationBackupRetentionPolicyDailyScheduleOutputReference",
    "AutomanageConfigurationBackupRetentionPolicyDailyScheduleRetentionDuration",
    "AutomanageConfigurationBackupRetentionPolicyDailyScheduleRetentionDurationOutputReference",
    "AutomanageConfigurationBackupRetentionPolicyOutputReference",
    "AutomanageConfigurationBackupRetentionPolicyWeeklySchedule",
    "AutomanageConfigurationBackupRetentionPolicyWeeklyScheduleOutputReference",
    "AutomanageConfigurationBackupRetentionPolicyWeeklyScheduleRetentionDuration",
    "AutomanageConfigurationBackupRetentionPolicyWeeklyScheduleRetentionDurationOutputReference",
    "AutomanageConfigurationBackupSchedulePolicy",
    "AutomanageConfigurationBackupSchedulePolicyOutputReference",
    "AutomanageConfigurationConfig",
    "AutomanageConfigurationTimeouts",
    "AutomanageConfigurationTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__4bf8edfd8d5df3948bdc6feab0461de4a1bd8f6ea2c1ee19bffcfc32193a394c(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    location: builtins.str,
    name: builtins.str,
    resource_group_name: builtins.str,
    antimalware: typing.Optional[typing.Union[AutomanageConfigurationAntimalware, typing.Dict[builtins.str, typing.Any]]] = None,
    automation_account_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    azure_security_baseline: typing.Optional[typing.Union[AutomanageConfigurationAzureSecurityBaseline, typing.Dict[builtins.str, typing.Any]]] = None,
    backup: typing.Optional[typing.Union[AutomanageConfigurationBackup, typing.Dict[builtins.str, typing.Any]]] = None,
    boot_diagnostics_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    defender_for_cloud_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    guest_configuration_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    log_analytics_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    status_change_alert_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[AutomanageConfigurationTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__78272d94e9e27f1f5eda9d3f218bf3800fb0861ba6bdb95a63ea8a24865a886a(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c8e20969043a0e60d3ccc464a21873965996c39c80608d35b840d93ffe9b4ec(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28a5e48f30907ff12f558baf02ffe66d1b4eee98e4c8b363a3d727f35384667a(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__539952120a9753fb9abce9d76eb0e06176d812619a39c46f8395ecdac789bcd6(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5d55ad1f6f39e165e59607b985c7e6235b1b0391970453c30919b8509bca127(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7143ccf4957085d3d1274fcfe37de5f2e40bdd842611b357a8610a1326478da3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5a252d8d6a7d5f7aa02f7733fa15993edac7c881c59852225b551f95226ca23(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ca4994a592b2673727d39ac4067c850be05e40d37d62f46105c9812ffdab1ef(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d06d6f87f6613a3515992b9be7c873c7d506d023566e5d09797c30bd276578c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b809809582785dc8e0647c79d9eefd37fe692297f03a733d2cd380b684bf0aa7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de37291325d364e90dd1ba8bf2e3b4cfe4df16fced03ecb1c35b6029baf33e0e(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92acc0f21178f169b82acfa843253647f1d0a6dc801cb8a39280c00f6c3baa9a(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f87650b0b7cd438005b39a2199a9b3cc2a8446a58dbe9058a7331309f6a8164(
    *,
    exclusions: typing.Optional[typing.Union[AutomanageConfigurationAntimalwareExclusions, typing.Dict[builtins.str, typing.Any]]] = None,
    real_time_protection_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    scheduled_scan_day: typing.Optional[jsii.Number] = None,
    scheduled_scan_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    scheduled_scan_time_in_minutes: typing.Optional[jsii.Number] = None,
    scheduled_scan_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__548b30bc103376491ebe1d5621ebe2a2cd65d44589abc7ea451955e0d9db7ede(
    *,
    extensions: typing.Optional[builtins.str] = None,
    paths: typing.Optional[builtins.str] = None,
    processes: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37f2a8eee239781dc740883e864858036728afbc6f88561a57d08566fe3cbc1c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74afd5b456a468304e847674b29015574c5a2ba0bcab7aa1a984f02a3adb0d3d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3f81eb06a153b60023d8f64921b33cc2dbe789921c57d5e3ee6488c2737b51a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d6d933464a2f167d0aea40fcd78ab26f71ef33e1efaf6ceabb2776d9ce7c238(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f29209505ad37f052fa2245e0958ee1d1a1de3fb80a84d7b8fa51f8684edc142(
    value: typing.Optional[AutomanageConfigurationAntimalwareExclusions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ff28e678c67a018be51c29e876ed89b27b9884faa2891931382b60d26911191(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a580c94df6a4a325c6297f52d71615d6e5ee9b7dd0f02d53b4b67d2bc1c42f1(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__235901e6c5781a00ff51c171b9384df6a44f982e2d336c0cd3eb426d2ddae504(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d8a35190bf675e129f4acd6b928c861ab10fb8929a77c1bfe27589b0fc252ea(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c344c28b3f0e5f0bd8900d9445cfc2b7041aeca83c6f32c57eae953e989deca4(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b3212a6b4974dc178509fb3aa5ac6c58a844619ba5071c653ed08c5049f76d1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd480d3c1618d8a3f02e735df223f0ca3e67f1a038463bb38bf05572d34f6f2b(
    value: typing.Optional[AutomanageConfigurationAntimalware],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75ac1994442bc83c581b22ffcdb1ec4d9c50c4b63ef5b12576d9ec38da1ae047(
    *,
    assignment_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02b46199b026cd300be2295207713faccfff30fd8a4e0993bc6653b0ea68c526(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3eed58231ae5576abfa77f155e48b7633ce9811425eabf126c514302ad260a71(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0fd6310d530cdc47de3a1a0b8ad39f0984deab6235711424f428bc9bb64debf9(
    value: typing.Optional[AutomanageConfigurationAzureSecurityBaseline],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59bc6c705f4bd04241d6e73b2618d0b369fbff0971e262aac68cd57a1e760798(
    *,
    instant_rp_retention_range_in_days: typing.Optional[jsii.Number] = None,
    policy_name: typing.Optional[builtins.str] = None,
    retention_policy: typing.Optional[typing.Union[AutomanageConfigurationBackupRetentionPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    schedule_policy: typing.Optional[typing.Union[AutomanageConfigurationBackupSchedulePolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    time_zone: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__655a42eff7549dc6fb3080ad76ff3064c1ee71d7d4d420b6d73fdc36d2a3099c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bbf1d440b55d782cb10a84cbab9f31aeacd19643989f5f6547bc24c6b76bd064(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bdf4e355e95d46f390181426ee1db175ff282ef3a569c5527c75cab8297eb046(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8fa8f701ae832e4864557b2d754d91347700c628e84ba49bdbd9a0437c4e5dc9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42f21f0f02521badfbbc9720574fbeab5897d6e7e766476135fdaddf0322fe1a(
    value: typing.Optional[AutomanageConfigurationBackup],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd152e61d885ce4a0d581ec026abb0a63219b1ef4dc6f6e392231c417b295d04(
    *,
    daily_schedule: typing.Optional[typing.Union[AutomanageConfigurationBackupRetentionPolicyDailySchedule, typing.Dict[builtins.str, typing.Any]]] = None,
    retention_policy_type: typing.Optional[builtins.str] = None,
    weekly_schedule: typing.Optional[typing.Union[AutomanageConfigurationBackupRetentionPolicyWeeklySchedule, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40a69ee39a1ef64c4cdf1169b8f97c00f65593e08c1e784fe3a5bdaf693fc008(
    *,
    retention_duration: typing.Optional[typing.Union[AutomanageConfigurationBackupRetentionPolicyDailyScheduleRetentionDuration, typing.Dict[builtins.str, typing.Any]]] = None,
    retention_times: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c77d297d9cef499adaeae924ae04f8b5e35e72f7afdb045b035f17081a50eb9b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86d3865f90fd56515389f8017890b9098e65969526845a92945f65e42673245b(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e08499ca77e2301c845e6748cffa24dc701902cae817629616c2e6d55c8b7188(
    value: typing.Optional[AutomanageConfigurationBackupRetentionPolicyDailySchedule],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1f70c65f224b72f8ea594bfbf06792aa4af0dadf04f109238c2587b579ac90a(
    *,
    count: typing.Optional[jsii.Number] = None,
    duration_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1ccba957ec81120b859a5d40b8e64a4580b5a7ab4f6757de920f9b9b0521e68(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2a637cba3c99ebf6c85d8f8549602d4494a7013fccd86d477423d86402bc46e(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db7317561b60b102263d480580c23df63a710d54931f578d1e8fc77a8a00c88c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7b46a9327954b41d4e8337349d193b5165859f8ef655d44d31ae21f3285560d(
    value: typing.Optional[AutomanageConfigurationBackupRetentionPolicyDailyScheduleRetentionDuration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19fd44ae16426baa1acbf991de5f8b832e8920feff601fda01bfed1d85b1ac77(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__56a0812d2c24aedd292f6da365feac0d506911daacfcf06480428b39580fe34e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b7961a720b4a84d26a76d6c97fb3148d26af0f68189d8a8f0faf0cb692e34f7(
    value: typing.Optional[AutomanageConfigurationBackupRetentionPolicy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15120c102b8d7317a70a98a1e0311ccb5b8e78ad8ce3e15ae8529d9cf5031a8c(
    *,
    retention_duration: typing.Optional[typing.Union[AutomanageConfigurationBackupRetentionPolicyWeeklyScheduleRetentionDuration, typing.Dict[builtins.str, typing.Any]]] = None,
    retention_times: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f403434eaccd2add943be2970d35115c54a3dced2d9ccbd132965f932a5cc8e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8353560bbb315c4afc281748111cc1050c0dbde707d213c0d76377dc4248f914(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__07b3b00c4e7cad80a46d68218ad37e2c04c5c025046aa9c88d239628ecb0e4d4(
    value: typing.Optional[AutomanageConfigurationBackupRetentionPolicyWeeklySchedule],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4cc2636b42f253415563f6ea2bf83b631910676dadb238989dee85e44bc029f0(
    *,
    count: typing.Optional[jsii.Number] = None,
    duration_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fdfb70fc588d3db47680ad35b8c86ca23b856fc010cd62988a68698ae2dfc75b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__47d92d9ca662dff7160ab52db363e42f295ff31dbc2f48a7904a542a8076a1ab(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e72d7997650ffab2ff29359122935fb3809d27faf64a2f3bafdb37f360ff06d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__870800dfc2d1943f22e9c05d70df199927df64609a5037dfd368a5403c192441(
    value: typing.Optional[AutomanageConfigurationBackupRetentionPolicyWeeklyScheduleRetentionDuration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91323e5462197be72339cf521a28ea5b7888fb4dfce19adbcb19b0c19475905b(
    *,
    schedule_policy_type: typing.Optional[builtins.str] = None,
    schedule_run_days: typing.Optional[typing.Sequence[builtins.str]] = None,
    schedule_run_frequency: typing.Optional[builtins.str] = None,
    schedule_run_times: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c359b344a8068a870dda9b0b51f64f4427b716e9a069b83e1a221d13c41bfdc7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4bb481188ec89a2b6266d3867d4f9a1ff4a9ece87bc1fe39138ba7bce9ae81e1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac762e92e6178793504d9741d0555f06f40cabcc2de8272d7e82dbdccc75b65f(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__655fc258ddc67e42e6c790f0cec6d62d5a124533865f8a094ae0b21f98fd7839(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a5d546570336da17ac6171245fae82407779006aee379f913cbee828cb3e89b(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ffeecf5767f809ad1b1557bfb79e011b45912d04cc5ef24c9d06887210a70e9(
    value: typing.Optional[AutomanageConfigurationBackupSchedulePolicy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33a19bcb6f00592868a7bc71124a422ccf40122cf2f8e42ed0beac80bfafcd73(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    location: builtins.str,
    name: builtins.str,
    resource_group_name: builtins.str,
    antimalware: typing.Optional[typing.Union[AutomanageConfigurationAntimalware, typing.Dict[builtins.str, typing.Any]]] = None,
    automation_account_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    azure_security_baseline: typing.Optional[typing.Union[AutomanageConfigurationAzureSecurityBaseline, typing.Dict[builtins.str, typing.Any]]] = None,
    backup: typing.Optional[typing.Union[AutomanageConfigurationBackup, typing.Dict[builtins.str, typing.Any]]] = None,
    boot_diagnostics_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    defender_for_cloud_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    guest_configuration_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    log_analytics_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    status_change_alert_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[AutomanageConfigurationTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e77a667f22aa911ab67e937b8d6577f12dcf272418a3bb5e2c9bc6d8cc73f577(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    read: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__478071835ab24f48a5a1c44588e9040119e816fb5d77aaf7ab4e843e2fe0016f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__741bbbafd56fdb002bc83c4441b894ca7282dcfa2843b2dadc9c9d60df3528dd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__17abae9724c09fbc30f47a079ea12c202f5246fa90ecddff450fbf486ef2759b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8349888958a6eed2ddc74d1f45adbb034842208e3204cb5451af9c2d0165b95(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bfd02e14bac71d1da866bd777ca68140d5b705e89cd067cb38e0031121bbb687(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7304250ae4256a2c8fe5968f2b18d26df89b5192dd0cd6ecf146dca43e04fadc(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AutomanageConfigurationTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
