r'''
# `azurerm_backup_policy_vm`

Refer to the Terraform Registry for docs: [`azurerm_backup_policy_vm`](https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_vm).
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


class BackupPolicyVm(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.backupPolicyVm.BackupPolicyVm",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_vm azurerm_backup_policy_vm}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        backup: typing.Union["BackupPolicyVmBackup", typing.Dict[builtins.str, typing.Any]],
        name: builtins.str,
        recovery_vault_name: builtins.str,
        resource_group_name: builtins.str,
        id: typing.Optional[builtins.str] = None,
        instant_restore_resource_group: typing.Optional[typing.Union["BackupPolicyVmInstantRestoreResourceGroup", typing.Dict[builtins.str, typing.Any]]] = None,
        instant_restore_retention_days: typing.Optional[jsii.Number] = None,
        policy_type: typing.Optional[builtins.str] = None,
        retention_daily: typing.Optional[typing.Union["BackupPolicyVmRetentionDaily", typing.Dict[builtins.str, typing.Any]]] = None,
        retention_monthly: typing.Optional[typing.Union["BackupPolicyVmRetentionMonthly", typing.Dict[builtins.str, typing.Any]]] = None,
        retention_weekly: typing.Optional[typing.Union["BackupPolicyVmRetentionWeekly", typing.Dict[builtins.str, typing.Any]]] = None,
        retention_yearly: typing.Optional[typing.Union["BackupPolicyVmRetentionYearly", typing.Dict[builtins.str, typing.Any]]] = None,
        tiering_policy: typing.Optional[typing.Union["BackupPolicyVmTieringPolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["BackupPolicyVmTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        timezone: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_vm azurerm_backup_policy_vm} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param backup: backup block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_vm#backup BackupPolicyVm#backup}
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_vm#name BackupPolicyVm#name}.
        :param recovery_vault_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_vm#recovery_vault_name BackupPolicyVm#recovery_vault_name}.
        :param resource_group_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_vm#resource_group_name BackupPolicyVm#resource_group_name}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_vm#id BackupPolicyVm#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param instant_restore_resource_group: instant_restore_resource_group block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_vm#instant_restore_resource_group BackupPolicyVm#instant_restore_resource_group}
        :param instant_restore_retention_days: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_vm#instant_restore_retention_days BackupPolicyVm#instant_restore_retention_days}.
        :param policy_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_vm#policy_type BackupPolicyVm#policy_type}.
        :param retention_daily: retention_daily block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_vm#retention_daily BackupPolicyVm#retention_daily}
        :param retention_monthly: retention_monthly block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_vm#retention_monthly BackupPolicyVm#retention_monthly}
        :param retention_weekly: retention_weekly block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_vm#retention_weekly BackupPolicyVm#retention_weekly}
        :param retention_yearly: retention_yearly block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_vm#retention_yearly BackupPolicyVm#retention_yearly}
        :param tiering_policy: tiering_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_vm#tiering_policy BackupPolicyVm#tiering_policy}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_vm#timeouts BackupPolicyVm#timeouts}
        :param timezone: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_vm#timezone BackupPolicyVm#timezone}.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a1698716c878c41aa7c0471a1715d1b9a9276e9c79996c6b1438c378e1049d0)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = BackupPolicyVmConfig(
            backup=backup,
            name=name,
            recovery_vault_name=recovery_vault_name,
            resource_group_name=resource_group_name,
            id=id,
            instant_restore_resource_group=instant_restore_resource_group,
            instant_restore_retention_days=instant_restore_retention_days,
            policy_type=policy_type,
            retention_daily=retention_daily,
            retention_monthly=retention_monthly,
            retention_weekly=retention_weekly,
            retention_yearly=retention_yearly,
            tiering_policy=tiering_policy,
            timeouts=timeouts,
            timezone=timezone,
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
        '''Generates CDKTF code for importing a BackupPolicyVm resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the BackupPolicyVm to import.
        :param import_from_id: The id of the existing BackupPolicyVm that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_vm#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the BackupPolicyVm to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8182027f3d77e2fd30fae4a24f10fac3a5ecb4076c81f8d205c63e356c77464b)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putBackup")
    def put_backup(
        self,
        *,
        frequency: builtins.str,
        time: builtins.str,
        hour_duration: typing.Optional[jsii.Number] = None,
        hour_interval: typing.Optional[jsii.Number] = None,
        weekdays: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param frequency: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_vm#frequency BackupPolicyVm#frequency}.
        :param time: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_vm#time BackupPolicyVm#time}.
        :param hour_duration: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_vm#hour_duration BackupPolicyVm#hour_duration}.
        :param hour_interval: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_vm#hour_interval BackupPolicyVm#hour_interval}.
        :param weekdays: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_vm#weekdays BackupPolicyVm#weekdays}.
        '''
        value = BackupPolicyVmBackup(
            frequency=frequency,
            time=time,
            hour_duration=hour_duration,
            hour_interval=hour_interval,
            weekdays=weekdays,
        )

        return typing.cast(None, jsii.invoke(self, "putBackup", [value]))

    @jsii.member(jsii_name="putInstantRestoreResourceGroup")
    def put_instant_restore_resource_group(
        self,
        *,
        prefix: builtins.str,
        suffix: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param prefix: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_vm#prefix BackupPolicyVm#prefix}.
        :param suffix: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_vm#suffix BackupPolicyVm#suffix}.
        '''
        value = BackupPolicyVmInstantRestoreResourceGroup(prefix=prefix, suffix=suffix)

        return typing.cast(None, jsii.invoke(self, "putInstantRestoreResourceGroup", [value]))

    @jsii.member(jsii_name="putRetentionDaily")
    def put_retention_daily(self, *, count: jsii.Number) -> None:
        '''
        :param count: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_vm#count BackupPolicyVm#count}.
        '''
        value = BackupPolicyVmRetentionDaily(count=count)

        return typing.cast(None, jsii.invoke(self, "putRetentionDaily", [value]))

    @jsii.member(jsii_name="putRetentionMonthly")
    def put_retention_monthly(
        self,
        *,
        count: jsii.Number,
        days: typing.Optional[typing.Sequence[jsii.Number]] = None,
        include_last_days: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        weekdays: typing.Optional[typing.Sequence[builtins.str]] = None,
        weeks: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param count: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_vm#count BackupPolicyVm#count}.
        :param days: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_vm#days BackupPolicyVm#days}.
        :param include_last_days: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_vm#include_last_days BackupPolicyVm#include_last_days}.
        :param weekdays: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_vm#weekdays BackupPolicyVm#weekdays}.
        :param weeks: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_vm#weeks BackupPolicyVm#weeks}.
        '''
        value = BackupPolicyVmRetentionMonthly(
            count=count,
            days=days,
            include_last_days=include_last_days,
            weekdays=weekdays,
            weeks=weeks,
        )

        return typing.cast(None, jsii.invoke(self, "putRetentionMonthly", [value]))

    @jsii.member(jsii_name="putRetentionWeekly")
    def put_retention_weekly(
        self,
        *,
        count: jsii.Number,
        weekdays: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param count: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_vm#count BackupPolicyVm#count}.
        :param weekdays: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_vm#weekdays BackupPolicyVm#weekdays}.
        '''
        value = BackupPolicyVmRetentionWeekly(count=count, weekdays=weekdays)

        return typing.cast(None, jsii.invoke(self, "putRetentionWeekly", [value]))

    @jsii.member(jsii_name="putRetentionYearly")
    def put_retention_yearly(
        self,
        *,
        count: jsii.Number,
        months: typing.Sequence[builtins.str],
        days: typing.Optional[typing.Sequence[jsii.Number]] = None,
        include_last_days: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        weekdays: typing.Optional[typing.Sequence[builtins.str]] = None,
        weeks: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param count: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_vm#count BackupPolicyVm#count}.
        :param months: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_vm#months BackupPolicyVm#months}.
        :param days: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_vm#days BackupPolicyVm#days}.
        :param include_last_days: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_vm#include_last_days BackupPolicyVm#include_last_days}.
        :param weekdays: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_vm#weekdays BackupPolicyVm#weekdays}.
        :param weeks: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_vm#weeks BackupPolicyVm#weeks}.
        '''
        value = BackupPolicyVmRetentionYearly(
            count=count,
            months=months,
            days=days,
            include_last_days=include_last_days,
            weekdays=weekdays,
            weeks=weeks,
        )

        return typing.cast(None, jsii.invoke(self, "putRetentionYearly", [value]))

    @jsii.member(jsii_name="putTieringPolicy")
    def put_tiering_policy(
        self,
        *,
        archived_restore_point: typing.Union["BackupPolicyVmTieringPolicyArchivedRestorePoint", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param archived_restore_point: archived_restore_point block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_vm#archived_restore_point BackupPolicyVm#archived_restore_point}
        '''
        value = BackupPolicyVmTieringPolicy(
            archived_restore_point=archived_restore_point
        )

        return typing.cast(None, jsii.invoke(self, "putTieringPolicy", [value]))

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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_vm#create BackupPolicyVm#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_vm#delete BackupPolicyVm#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_vm#read BackupPolicyVm#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_vm#update BackupPolicyVm#update}.
        '''
        value = BackupPolicyVmTimeouts(
            create=create, delete=delete, read=read, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetInstantRestoreResourceGroup")
    def reset_instant_restore_resource_group(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInstantRestoreResourceGroup", []))

    @jsii.member(jsii_name="resetInstantRestoreRetentionDays")
    def reset_instant_restore_retention_days(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInstantRestoreRetentionDays", []))

    @jsii.member(jsii_name="resetPolicyType")
    def reset_policy_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPolicyType", []))

    @jsii.member(jsii_name="resetRetentionDaily")
    def reset_retention_daily(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRetentionDaily", []))

    @jsii.member(jsii_name="resetRetentionMonthly")
    def reset_retention_monthly(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRetentionMonthly", []))

    @jsii.member(jsii_name="resetRetentionWeekly")
    def reset_retention_weekly(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRetentionWeekly", []))

    @jsii.member(jsii_name="resetRetentionYearly")
    def reset_retention_yearly(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRetentionYearly", []))

    @jsii.member(jsii_name="resetTieringPolicy")
    def reset_tiering_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTieringPolicy", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

    @jsii.member(jsii_name="resetTimezone")
    def reset_timezone(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimezone", []))

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
    @jsii.member(jsii_name="backup")
    def backup(self) -> "BackupPolicyVmBackupOutputReference":
        return typing.cast("BackupPolicyVmBackupOutputReference", jsii.get(self, "backup"))

    @builtins.property
    @jsii.member(jsii_name="instantRestoreResourceGroup")
    def instant_restore_resource_group(
        self,
    ) -> "BackupPolicyVmInstantRestoreResourceGroupOutputReference":
        return typing.cast("BackupPolicyVmInstantRestoreResourceGroupOutputReference", jsii.get(self, "instantRestoreResourceGroup"))

    @builtins.property
    @jsii.member(jsii_name="retentionDaily")
    def retention_daily(self) -> "BackupPolicyVmRetentionDailyOutputReference":
        return typing.cast("BackupPolicyVmRetentionDailyOutputReference", jsii.get(self, "retentionDaily"))

    @builtins.property
    @jsii.member(jsii_name="retentionMonthly")
    def retention_monthly(self) -> "BackupPolicyVmRetentionMonthlyOutputReference":
        return typing.cast("BackupPolicyVmRetentionMonthlyOutputReference", jsii.get(self, "retentionMonthly"))

    @builtins.property
    @jsii.member(jsii_name="retentionWeekly")
    def retention_weekly(self) -> "BackupPolicyVmRetentionWeeklyOutputReference":
        return typing.cast("BackupPolicyVmRetentionWeeklyOutputReference", jsii.get(self, "retentionWeekly"))

    @builtins.property
    @jsii.member(jsii_name="retentionYearly")
    def retention_yearly(self) -> "BackupPolicyVmRetentionYearlyOutputReference":
        return typing.cast("BackupPolicyVmRetentionYearlyOutputReference", jsii.get(self, "retentionYearly"))

    @builtins.property
    @jsii.member(jsii_name="tieringPolicy")
    def tiering_policy(self) -> "BackupPolicyVmTieringPolicyOutputReference":
        return typing.cast("BackupPolicyVmTieringPolicyOutputReference", jsii.get(self, "tieringPolicy"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "BackupPolicyVmTimeoutsOutputReference":
        return typing.cast("BackupPolicyVmTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="backupInput")
    def backup_input(self) -> typing.Optional["BackupPolicyVmBackup"]:
        return typing.cast(typing.Optional["BackupPolicyVmBackup"], jsii.get(self, "backupInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="instantRestoreResourceGroupInput")
    def instant_restore_resource_group_input(
        self,
    ) -> typing.Optional["BackupPolicyVmInstantRestoreResourceGroup"]:
        return typing.cast(typing.Optional["BackupPolicyVmInstantRestoreResourceGroup"], jsii.get(self, "instantRestoreResourceGroupInput"))

    @builtins.property
    @jsii.member(jsii_name="instantRestoreRetentionDaysInput")
    def instant_restore_retention_days_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "instantRestoreRetentionDaysInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="policyTypeInput")
    def policy_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "policyTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="recoveryVaultNameInput")
    def recovery_vault_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "recoveryVaultNameInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceGroupNameInput")
    def resource_group_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "resourceGroupNameInput"))

    @builtins.property
    @jsii.member(jsii_name="retentionDailyInput")
    def retention_daily_input(self) -> typing.Optional["BackupPolicyVmRetentionDaily"]:
        return typing.cast(typing.Optional["BackupPolicyVmRetentionDaily"], jsii.get(self, "retentionDailyInput"))

    @builtins.property
    @jsii.member(jsii_name="retentionMonthlyInput")
    def retention_monthly_input(
        self,
    ) -> typing.Optional["BackupPolicyVmRetentionMonthly"]:
        return typing.cast(typing.Optional["BackupPolicyVmRetentionMonthly"], jsii.get(self, "retentionMonthlyInput"))

    @builtins.property
    @jsii.member(jsii_name="retentionWeeklyInput")
    def retention_weekly_input(
        self,
    ) -> typing.Optional["BackupPolicyVmRetentionWeekly"]:
        return typing.cast(typing.Optional["BackupPolicyVmRetentionWeekly"], jsii.get(self, "retentionWeeklyInput"))

    @builtins.property
    @jsii.member(jsii_name="retentionYearlyInput")
    def retention_yearly_input(
        self,
    ) -> typing.Optional["BackupPolicyVmRetentionYearly"]:
        return typing.cast(typing.Optional["BackupPolicyVmRetentionYearly"], jsii.get(self, "retentionYearlyInput"))

    @builtins.property
    @jsii.member(jsii_name="tieringPolicyInput")
    def tiering_policy_input(self) -> typing.Optional["BackupPolicyVmTieringPolicy"]:
        return typing.cast(typing.Optional["BackupPolicyVmTieringPolicy"], jsii.get(self, "tieringPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "BackupPolicyVmTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "BackupPolicyVmTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="timezoneInput")
    def timezone_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "timezoneInput"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0d1a2ec30ce6ac88e58b851d95daf93f5cfc47552703ec4f8a67513ce6c1a589)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="instantRestoreRetentionDays")
    def instant_restore_retention_days(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "instantRestoreRetentionDays"))

    @instant_restore_retention_days.setter
    def instant_restore_retention_days(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__60737d8cc9e51cdfe8b8992443b56049aed3275ffffbf58e799e95e1e6aa684b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "instantRestoreRetentionDays", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ccf4668e3354c49cc8cae42c1eb4bd7282af97f77b525143d0810f57a461313e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="policyType")
    def policy_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "policyType"))

    @policy_type.setter
    def policy_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__31c1acd4abc8bd91685ba0233f3f37f20935e2044460b604e41ee723aaac029a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "policyType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="recoveryVaultName")
    def recovery_vault_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "recoveryVaultName"))

    @recovery_vault_name.setter
    def recovery_vault_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__899bd26c4c0bde1a4cafd09ae9fee2239d1523ce0b126c0973af78fae8f5de5d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "recoveryVaultName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resourceGroupName")
    def resource_group_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourceGroupName"))

    @resource_group_name.setter
    def resource_group_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3199e3cb11247b322931e3a37dab39f1a31cc30b82e10a9c19c04d023fb9fc47)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceGroupName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="timezone")
    def timezone(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "timezone"))

    @timezone.setter
    def timezone(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cad2aa916c149592cd095b6edc44e378bbedfc8b7049c4ce46ea80778b5dda51)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timezone", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.backupPolicyVm.BackupPolicyVmBackup",
    jsii_struct_bases=[],
    name_mapping={
        "frequency": "frequency",
        "time": "time",
        "hour_duration": "hourDuration",
        "hour_interval": "hourInterval",
        "weekdays": "weekdays",
    },
)
class BackupPolicyVmBackup:
    def __init__(
        self,
        *,
        frequency: builtins.str,
        time: builtins.str,
        hour_duration: typing.Optional[jsii.Number] = None,
        hour_interval: typing.Optional[jsii.Number] = None,
        weekdays: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param frequency: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_vm#frequency BackupPolicyVm#frequency}.
        :param time: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_vm#time BackupPolicyVm#time}.
        :param hour_duration: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_vm#hour_duration BackupPolicyVm#hour_duration}.
        :param hour_interval: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_vm#hour_interval BackupPolicyVm#hour_interval}.
        :param weekdays: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_vm#weekdays BackupPolicyVm#weekdays}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d7bc6be143d6238b15698c70fa197499d046914287b2257c375803dd53c73b03)
            check_type(argname="argument frequency", value=frequency, expected_type=type_hints["frequency"])
            check_type(argname="argument time", value=time, expected_type=type_hints["time"])
            check_type(argname="argument hour_duration", value=hour_duration, expected_type=type_hints["hour_duration"])
            check_type(argname="argument hour_interval", value=hour_interval, expected_type=type_hints["hour_interval"])
            check_type(argname="argument weekdays", value=weekdays, expected_type=type_hints["weekdays"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "frequency": frequency,
            "time": time,
        }
        if hour_duration is not None:
            self._values["hour_duration"] = hour_duration
        if hour_interval is not None:
            self._values["hour_interval"] = hour_interval
        if weekdays is not None:
            self._values["weekdays"] = weekdays

    @builtins.property
    def frequency(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_vm#frequency BackupPolicyVm#frequency}.'''
        result = self._values.get("frequency")
        assert result is not None, "Required property 'frequency' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def time(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_vm#time BackupPolicyVm#time}.'''
        result = self._values.get("time")
        assert result is not None, "Required property 'time' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def hour_duration(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_vm#hour_duration BackupPolicyVm#hour_duration}.'''
        result = self._values.get("hour_duration")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def hour_interval(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_vm#hour_interval BackupPolicyVm#hour_interval}.'''
        result = self._values.get("hour_interval")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def weekdays(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_vm#weekdays BackupPolicyVm#weekdays}.'''
        result = self._values.get("weekdays")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BackupPolicyVmBackup(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BackupPolicyVmBackupOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.backupPolicyVm.BackupPolicyVmBackupOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__449f443595ff35e90eaa3ea27d036ac6124c67638117751ad0d73bf72612610d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetHourDuration")
    def reset_hour_duration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHourDuration", []))

    @jsii.member(jsii_name="resetHourInterval")
    def reset_hour_interval(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHourInterval", []))

    @jsii.member(jsii_name="resetWeekdays")
    def reset_weekdays(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWeekdays", []))

    @builtins.property
    @jsii.member(jsii_name="frequencyInput")
    def frequency_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "frequencyInput"))

    @builtins.property
    @jsii.member(jsii_name="hourDurationInput")
    def hour_duration_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "hourDurationInput"))

    @builtins.property
    @jsii.member(jsii_name="hourIntervalInput")
    def hour_interval_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "hourIntervalInput"))

    @builtins.property
    @jsii.member(jsii_name="timeInput")
    def time_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "timeInput"))

    @builtins.property
    @jsii.member(jsii_name="weekdaysInput")
    def weekdays_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "weekdaysInput"))

    @builtins.property
    @jsii.member(jsii_name="frequency")
    def frequency(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "frequency"))

    @frequency.setter
    def frequency(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5040dced6321898042d3ca8e11d4d5a4b475d9b4ed49fac4324c869d2f324b02)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "frequency", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="hourDuration")
    def hour_duration(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "hourDuration"))

    @hour_duration.setter
    def hour_duration(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__66c93fe9abb182263693540a8e5982b6323c24dc0d066f76174d1a18ba14cf94)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hourDuration", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="hourInterval")
    def hour_interval(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "hourInterval"))

    @hour_interval.setter
    def hour_interval(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__76ca270f27280a55a0e7c59cca575874e457fe31985e18e14e965eb6b3ee7313)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hourInterval", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="time")
    def time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "time"))

    @time.setter
    def time(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f759a5c524bf4c3ecfb62d7407f68ddda52d34b3990ae04dc154bb9a070f62ba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "time", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="weekdays")
    def weekdays(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "weekdays"))

    @weekdays.setter
    def weekdays(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9697a4d514d107e6a63dc73d853f343bed0d5d4e5f0bcf240b176e80577fceaf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "weekdays", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[BackupPolicyVmBackup]:
        return typing.cast(typing.Optional[BackupPolicyVmBackup], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[BackupPolicyVmBackup]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f6b869f4697d73bcadcf464e1c7475de2ff87a76dcf61026e31a6a6ed6e2406d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.backupPolicyVm.BackupPolicyVmConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "backup": "backup",
        "name": "name",
        "recovery_vault_name": "recoveryVaultName",
        "resource_group_name": "resourceGroupName",
        "id": "id",
        "instant_restore_resource_group": "instantRestoreResourceGroup",
        "instant_restore_retention_days": "instantRestoreRetentionDays",
        "policy_type": "policyType",
        "retention_daily": "retentionDaily",
        "retention_monthly": "retentionMonthly",
        "retention_weekly": "retentionWeekly",
        "retention_yearly": "retentionYearly",
        "tiering_policy": "tieringPolicy",
        "timeouts": "timeouts",
        "timezone": "timezone",
    },
)
class BackupPolicyVmConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        backup: typing.Union[BackupPolicyVmBackup, typing.Dict[builtins.str, typing.Any]],
        name: builtins.str,
        recovery_vault_name: builtins.str,
        resource_group_name: builtins.str,
        id: typing.Optional[builtins.str] = None,
        instant_restore_resource_group: typing.Optional[typing.Union["BackupPolicyVmInstantRestoreResourceGroup", typing.Dict[builtins.str, typing.Any]]] = None,
        instant_restore_retention_days: typing.Optional[jsii.Number] = None,
        policy_type: typing.Optional[builtins.str] = None,
        retention_daily: typing.Optional[typing.Union["BackupPolicyVmRetentionDaily", typing.Dict[builtins.str, typing.Any]]] = None,
        retention_monthly: typing.Optional[typing.Union["BackupPolicyVmRetentionMonthly", typing.Dict[builtins.str, typing.Any]]] = None,
        retention_weekly: typing.Optional[typing.Union["BackupPolicyVmRetentionWeekly", typing.Dict[builtins.str, typing.Any]]] = None,
        retention_yearly: typing.Optional[typing.Union["BackupPolicyVmRetentionYearly", typing.Dict[builtins.str, typing.Any]]] = None,
        tiering_policy: typing.Optional[typing.Union["BackupPolicyVmTieringPolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["BackupPolicyVmTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        timezone: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param backup: backup block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_vm#backup BackupPolicyVm#backup}
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_vm#name BackupPolicyVm#name}.
        :param recovery_vault_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_vm#recovery_vault_name BackupPolicyVm#recovery_vault_name}.
        :param resource_group_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_vm#resource_group_name BackupPolicyVm#resource_group_name}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_vm#id BackupPolicyVm#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param instant_restore_resource_group: instant_restore_resource_group block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_vm#instant_restore_resource_group BackupPolicyVm#instant_restore_resource_group}
        :param instant_restore_retention_days: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_vm#instant_restore_retention_days BackupPolicyVm#instant_restore_retention_days}.
        :param policy_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_vm#policy_type BackupPolicyVm#policy_type}.
        :param retention_daily: retention_daily block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_vm#retention_daily BackupPolicyVm#retention_daily}
        :param retention_monthly: retention_monthly block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_vm#retention_monthly BackupPolicyVm#retention_monthly}
        :param retention_weekly: retention_weekly block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_vm#retention_weekly BackupPolicyVm#retention_weekly}
        :param retention_yearly: retention_yearly block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_vm#retention_yearly BackupPolicyVm#retention_yearly}
        :param tiering_policy: tiering_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_vm#tiering_policy BackupPolicyVm#tiering_policy}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_vm#timeouts BackupPolicyVm#timeouts}
        :param timezone: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_vm#timezone BackupPolicyVm#timezone}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(backup, dict):
            backup = BackupPolicyVmBackup(**backup)
        if isinstance(instant_restore_resource_group, dict):
            instant_restore_resource_group = BackupPolicyVmInstantRestoreResourceGroup(**instant_restore_resource_group)
        if isinstance(retention_daily, dict):
            retention_daily = BackupPolicyVmRetentionDaily(**retention_daily)
        if isinstance(retention_monthly, dict):
            retention_monthly = BackupPolicyVmRetentionMonthly(**retention_monthly)
        if isinstance(retention_weekly, dict):
            retention_weekly = BackupPolicyVmRetentionWeekly(**retention_weekly)
        if isinstance(retention_yearly, dict):
            retention_yearly = BackupPolicyVmRetentionYearly(**retention_yearly)
        if isinstance(tiering_policy, dict):
            tiering_policy = BackupPolicyVmTieringPolicy(**tiering_policy)
        if isinstance(timeouts, dict):
            timeouts = BackupPolicyVmTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7ecd90ffd534383f4d3013c04cee9059d9cae17a6e1fe118b26a80cd63f11f66)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument backup", value=backup, expected_type=type_hints["backup"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument recovery_vault_name", value=recovery_vault_name, expected_type=type_hints["recovery_vault_name"])
            check_type(argname="argument resource_group_name", value=resource_group_name, expected_type=type_hints["resource_group_name"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument instant_restore_resource_group", value=instant_restore_resource_group, expected_type=type_hints["instant_restore_resource_group"])
            check_type(argname="argument instant_restore_retention_days", value=instant_restore_retention_days, expected_type=type_hints["instant_restore_retention_days"])
            check_type(argname="argument policy_type", value=policy_type, expected_type=type_hints["policy_type"])
            check_type(argname="argument retention_daily", value=retention_daily, expected_type=type_hints["retention_daily"])
            check_type(argname="argument retention_monthly", value=retention_monthly, expected_type=type_hints["retention_monthly"])
            check_type(argname="argument retention_weekly", value=retention_weekly, expected_type=type_hints["retention_weekly"])
            check_type(argname="argument retention_yearly", value=retention_yearly, expected_type=type_hints["retention_yearly"])
            check_type(argname="argument tiering_policy", value=tiering_policy, expected_type=type_hints["tiering_policy"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
            check_type(argname="argument timezone", value=timezone, expected_type=type_hints["timezone"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "backup": backup,
            "name": name,
            "recovery_vault_name": recovery_vault_name,
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
        if id is not None:
            self._values["id"] = id
        if instant_restore_resource_group is not None:
            self._values["instant_restore_resource_group"] = instant_restore_resource_group
        if instant_restore_retention_days is not None:
            self._values["instant_restore_retention_days"] = instant_restore_retention_days
        if policy_type is not None:
            self._values["policy_type"] = policy_type
        if retention_daily is not None:
            self._values["retention_daily"] = retention_daily
        if retention_monthly is not None:
            self._values["retention_monthly"] = retention_monthly
        if retention_weekly is not None:
            self._values["retention_weekly"] = retention_weekly
        if retention_yearly is not None:
            self._values["retention_yearly"] = retention_yearly
        if tiering_policy is not None:
            self._values["tiering_policy"] = tiering_policy
        if timeouts is not None:
            self._values["timeouts"] = timeouts
        if timezone is not None:
            self._values["timezone"] = timezone

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
    def backup(self) -> BackupPolicyVmBackup:
        '''backup block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_vm#backup BackupPolicyVm#backup}
        '''
        result = self._values.get("backup")
        assert result is not None, "Required property 'backup' is missing"
        return typing.cast(BackupPolicyVmBackup, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_vm#name BackupPolicyVm#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def recovery_vault_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_vm#recovery_vault_name BackupPolicyVm#recovery_vault_name}.'''
        result = self._values.get("recovery_vault_name")
        assert result is not None, "Required property 'recovery_vault_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def resource_group_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_vm#resource_group_name BackupPolicyVm#resource_group_name}.'''
        result = self._values.get("resource_group_name")
        assert result is not None, "Required property 'resource_group_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_vm#id BackupPolicyVm#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def instant_restore_resource_group(
        self,
    ) -> typing.Optional["BackupPolicyVmInstantRestoreResourceGroup"]:
        '''instant_restore_resource_group block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_vm#instant_restore_resource_group BackupPolicyVm#instant_restore_resource_group}
        '''
        result = self._values.get("instant_restore_resource_group")
        return typing.cast(typing.Optional["BackupPolicyVmInstantRestoreResourceGroup"], result)

    @builtins.property
    def instant_restore_retention_days(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_vm#instant_restore_retention_days BackupPolicyVm#instant_restore_retention_days}.'''
        result = self._values.get("instant_restore_retention_days")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def policy_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_vm#policy_type BackupPolicyVm#policy_type}.'''
        result = self._values.get("policy_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def retention_daily(self) -> typing.Optional["BackupPolicyVmRetentionDaily"]:
        '''retention_daily block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_vm#retention_daily BackupPolicyVm#retention_daily}
        '''
        result = self._values.get("retention_daily")
        return typing.cast(typing.Optional["BackupPolicyVmRetentionDaily"], result)

    @builtins.property
    def retention_monthly(self) -> typing.Optional["BackupPolicyVmRetentionMonthly"]:
        '''retention_monthly block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_vm#retention_monthly BackupPolicyVm#retention_monthly}
        '''
        result = self._values.get("retention_monthly")
        return typing.cast(typing.Optional["BackupPolicyVmRetentionMonthly"], result)

    @builtins.property
    def retention_weekly(self) -> typing.Optional["BackupPolicyVmRetentionWeekly"]:
        '''retention_weekly block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_vm#retention_weekly BackupPolicyVm#retention_weekly}
        '''
        result = self._values.get("retention_weekly")
        return typing.cast(typing.Optional["BackupPolicyVmRetentionWeekly"], result)

    @builtins.property
    def retention_yearly(self) -> typing.Optional["BackupPolicyVmRetentionYearly"]:
        '''retention_yearly block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_vm#retention_yearly BackupPolicyVm#retention_yearly}
        '''
        result = self._values.get("retention_yearly")
        return typing.cast(typing.Optional["BackupPolicyVmRetentionYearly"], result)

    @builtins.property
    def tiering_policy(self) -> typing.Optional["BackupPolicyVmTieringPolicy"]:
        '''tiering_policy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_vm#tiering_policy BackupPolicyVm#tiering_policy}
        '''
        result = self._values.get("tiering_policy")
        return typing.cast(typing.Optional["BackupPolicyVmTieringPolicy"], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["BackupPolicyVmTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_vm#timeouts BackupPolicyVm#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["BackupPolicyVmTimeouts"], result)

    @builtins.property
    def timezone(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_vm#timezone BackupPolicyVm#timezone}.'''
        result = self._values.get("timezone")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BackupPolicyVmConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.backupPolicyVm.BackupPolicyVmInstantRestoreResourceGroup",
    jsii_struct_bases=[],
    name_mapping={"prefix": "prefix", "suffix": "suffix"},
)
class BackupPolicyVmInstantRestoreResourceGroup:
    def __init__(
        self,
        *,
        prefix: builtins.str,
        suffix: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param prefix: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_vm#prefix BackupPolicyVm#prefix}.
        :param suffix: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_vm#suffix BackupPolicyVm#suffix}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bacf93ee67b874066f2d3cb7b542ce0c409193070e75f64ba802771e0c4568b8)
            check_type(argname="argument prefix", value=prefix, expected_type=type_hints["prefix"])
            check_type(argname="argument suffix", value=suffix, expected_type=type_hints["suffix"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "prefix": prefix,
        }
        if suffix is not None:
            self._values["suffix"] = suffix

    @builtins.property
    def prefix(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_vm#prefix BackupPolicyVm#prefix}.'''
        result = self._values.get("prefix")
        assert result is not None, "Required property 'prefix' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def suffix(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_vm#suffix BackupPolicyVm#suffix}.'''
        result = self._values.get("suffix")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BackupPolicyVmInstantRestoreResourceGroup(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BackupPolicyVmInstantRestoreResourceGroupOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.backupPolicyVm.BackupPolicyVmInstantRestoreResourceGroupOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7e347bc67914f962538ab2427e5f409e8b3f268f276ff3e1cbdab1f6ef0ea820)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetSuffix")
    def reset_suffix(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSuffix", []))

    @builtins.property
    @jsii.member(jsii_name="prefixInput")
    def prefix_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "prefixInput"))

    @builtins.property
    @jsii.member(jsii_name="suffixInput")
    def suffix_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "suffixInput"))

    @builtins.property
    @jsii.member(jsii_name="prefix")
    def prefix(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "prefix"))

    @prefix.setter
    def prefix(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__54641dfa43f6744bee6d12bde4decb4b4ed5783e1abc61315087faf9a48f7944)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "prefix", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="suffix")
    def suffix(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "suffix"))

    @suffix.setter
    def suffix(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__10bbeaff148cd4fd7378d85ee12bedd87215eec5c41624ec9ecd23cc749df391)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "suffix", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[BackupPolicyVmInstantRestoreResourceGroup]:
        return typing.cast(typing.Optional[BackupPolicyVmInstantRestoreResourceGroup], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[BackupPolicyVmInstantRestoreResourceGroup],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5576d1f9d2227764b0bbf5aa0629f452529010ffc7b4420ec3c3e8af93285b36)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.backupPolicyVm.BackupPolicyVmRetentionDaily",
    jsii_struct_bases=[],
    name_mapping={"count": "count"},
)
class BackupPolicyVmRetentionDaily:
    def __init__(self, *, count: jsii.Number) -> None:
        '''
        :param count: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_vm#count BackupPolicyVm#count}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a05279dc383d40cde12754d0824541bae4f1bf3de801f16543f90863d70e295e)
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "count": count,
        }

    @builtins.property
    def count(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_vm#count BackupPolicyVm#count}.'''
        result = self._values.get("count")
        assert result is not None, "Required property 'count' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BackupPolicyVmRetentionDaily(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BackupPolicyVmRetentionDailyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.backupPolicyVm.BackupPolicyVmRetentionDailyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c9a03f979ae14bc6419257d3f9229fe4a9fc0326def3aacd637045e2f812af33)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="countInput")
    def count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "countInput"))

    @builtins.property
    @jsii.member(jsii_name="count")
    def count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "count"))

    @count.setter
    def count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f593896179e4f7f81863630e932527ab5352dbfe446b9af0df2cb9d684d01e63)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "count", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[BackupPolicyVmRetentionDaily]:
        return typing.cast(typing.Optional[BackupPolicyVmRetentionDaily], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[BackupPolicyVmRetentionDaily],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__22944531f27d0c7be5b2604f57029cb72d40854d8a6fec11fdb11ee24d72d4d6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.backupPolicyVm.BackupPolicyVmRetentionMonthly",
    jsii_struct_bases=[],
    name_mapping={
        "count": "count",
        "days": "days",
        "include_last_days": "includeLastDays",
        "weekdays": "weekdays",
        "weeks": "weeks",
    },
)
class BackupPolicyVmRetentionMonthly:
    def __init__(
        self,
        *,
        count: jsii.Number,
        days: typing.Optional[typing.Sequence[jsii.Number]] = None,
        include_last_days: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        weekdays: typing.Optional[typing.Sequence[builtins.str]] = None,
        weeks: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param count: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_vm#count BackupPolicyVm#count}.
        :param days: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_vm#days BackupPolicyVm#days}.
        :param include_last_days: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_vm#include_last_days BackupPolicyVm#include_last_days}.
        :param weekdays: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_vm#weekdays BackupPolicyVm#weekdays}.
        :param weeks: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_vm#weeks BackupPolicyVm#weeks}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__139bc79354c6ba2aba51656be37db8b610098be5d065354f50933936adbd03d7)
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument days", value=days, expected_type=type_hints["days"])
            check_type(argname="argument include_last_days", value=include_last_days, expected_type=type_hints["include_last_days"])
            check_type(argname="argument weekdays", value=weekdays, expected_type=type_hints["weekdays"])
            check_type(argname="argument weeks", value=weeks, expected_type=type_hints["weeks"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "count": count,
        }
        if days is not None:
            self._values["days"] = days
        if include_last_days is not None:
            self._values["include_last_days"] = include_last_days
        if weekdays is not None:
            self._values["weekdays"] = weekdays
        if weeks is not None:
            self._values["weeks"] = weeks

    @builtins.property
    def count(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_vm#count BackupPolicyVm#count}.'''
        result = self._values.get("count")
        assert result is not None, "Required property 'count' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def days(self) -> typing.Optional[typing.List[jsii.Number]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_vm#days BackupPolicyVm#days}.'''
        result = self._values.get("days")
        return typing.cast(typing.Optional[typing.List[jsii.Number]], result)

    @builtins.property
    def include_last_days(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_vm#include_last_days BackupPolicyVm#include_last_days}.'''
        result = self._values.get("include_last_days")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def weekdays(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_vm#weekdays BackupPolicyVm#weekdays}.'''
        result = self._values.get("weekdays")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def weeks(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_vm#weeks BackupPolicyVm#weeks}.'''
        result = self._values.get("weeks")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BackupPolicyVmRetentionMonthly(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BackupPolicyVmRetentionMonthlyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.backupPolicyVm.BackupPolicyVmRetentionMonthlyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__59ec4e4cce803d72cde48b6f631b7f0437e2479104f083246f070ba0e8a7617f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetDays")
    def reset_days(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDays", []))

    @jsii.member(jsii_name="resetIncludeLastDays")
    def reset_include_last_days(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIncludeLastDays", []))

    @jsii.member(jsii_name="resetWeekdays")
    def reset_weekdays(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWeekdays", []))

    @jsii.member(jsii_name="resetWeeks")
    def reset_weeks(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWeeks", []))

    @builtins.property
    @jsii.member(jsii_name="countInput")
    def count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "countInput"))

    @builtins.property
    @jsii.member(jsii_name="daysInput")
    def days_input(self) -> typing.Optional[typing.List[jsii.Number]]:
        return typing.cast(typing.Optional[typing.List[jsii.Number]], jsii.get(self, "daysInput"))

    @builtins.property
    @jsii.member(jsii_name="includeLastDaysInput")
    def include_last_days_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "includeLastDaysInput"))

    @builtins.property
    @jsii.member(jsii_name="weekdaysInput")
    def weekdays_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "weekdaysInput"))

    @builtins.property
    @jsii.member(jsii_name="weeksInput")
    def weeks_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "weeksInput"))

    @builtins.property
    @jsii.member(jsii_name="count")
    def count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "count"))

    @count.setter
    def count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eb178e1dcacee59f3367f3703e6b63461d8dd28f0b029832a03ba4d6c06a8c55)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "count", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="days")
    def days(self) -> typing.List[jsii.Number]:
        return typing.cast(typing.List[jsii.Number], jsii.get(self, "days"))

    @days.setter
    def days(self, value: typing.List[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2cfc087e909dd9b1f24efc0db0e26c913719104d236aca14c6518dda6d0b2dcf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "days", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="includeLastDays")
    def include_last_days(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "includeLastDays"))

    @include_last_days.setter
    def include_last_days(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3af798fc726cccacd683044b8e47edfcc488a69bc74976bd7c776a2720ca0f3e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "includeLastDays", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="weekdays")
    def weekdays(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "weekdays"))

    @weekdays.setter
    def weekdays(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4b8a6c419951a25bbe61f3dd318577954b507c153b4891a0c7feaf9f28443b93)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "weekdays", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="weeks")
    def weeks(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "weeks"))

    @weeks.setter
    def weeks(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3fb6e19eef05126ecbd73454b057607dc0a2d07f99e90e71a0d367e275202771)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "weeks", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[BackupPolicyVmRetentionMonthly]:
        return typing.cast(typing.Optional[BackupPolicyVmRetentionMonthly], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[BackupPolicyVmRetentionMonthly],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0745e3ea3ff4978ae52728b5188baa15b71eca5beb12ebc4f83451c6308d2b5c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.backupPolicyVm.BackupPolicyVmRetentionWeekly",
    jsii_struct_bases=[],
    name_mapping={"count": "count", "weekdays": "weekdays"},
)
class BackupPolicyVmRetentionWeekly:
    def __init__(
        self,
        *,
        count: jsii.Number,
        weekdays: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param count: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_vm#count BackupPolicyVm#count}.
        :param weekdays: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_vm#weekdays BackupPolicyVm#weekdays}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__95c434888f45992c184ae3bc9da24fac935fd608a6b81ec94f7649808979143c)
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument weekdays", value=weekdays, expected_type=type_hints["weekdays"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "count": count,
            "weekdays": weekdays,
        }

    @builtins.property
    def count(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_vm#count BackupPolicyVm#count}.'''
        result = self._values.get("count")
        assert result is not None, "Required property 'count' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def weekdays(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_vm#weekdays BackupPolicyVm#weekdays}.'''
        result = self._values.get("weekdays")
        assert result is not None, "Required property 'weekdays' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BackupPolicyVmRetentionWeekly(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BackupPolicyVmRetentionWeeklyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.backupPolicyVm.BackupPolicyVmRetentionWeeklyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ad40afc0bbd8687fdd11a0b92824ed26b895093405459364b60db30872149075)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="countInput")
    def count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "countInput"))

    @builtins.property
    @jsii.member(jsii_name="weekdaysInput")
    def weekdays_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "weekdaysInput"))

    @builtins.property
    @jsii.member(jsii_name="count")
    def count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "count"))

    @count.setter
    def count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b8913ae15d3bfefff6168c8247e814d1e104d91f2f1f5b9d9c32c39d5c02b7d5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "count", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="weekdays")
    def weekdays(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "weekdays"))

    @weekdays.setter
    def weekdays(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__50c31d28ddd94a8792c3dfec8b988c121110ab4b5ff4cbfeec672ebd8fdb6230)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "weekdays", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[BackupPolicyVmRetentionWeekly]:
        return typing.cast(typing.Optional[BackupPolicyVmRetentionWeekly], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[BackupPolicyVmRetentionWeekly],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__155e268544a721f38197955cf2e8812cf9988a4529075f76f162056b6cda5561)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.backupPolicyVm.BackupPolicyVmRetentionYearly",
    jsii_struct_bases=[],
    name_mapping={
        "count": "count",
        "months": "months",
        "days": "days",
        "include_last_days": "includeLastDays",
        "weekdays": "weekdays",
        "weeks": "weeks",
    },
)
class BackupPolicyVmRetentionYearly:
    def __init__(
        self,
        *,
        count: jsii.Number,
        months: typing.Sequence[builtins.str],
        days: typing.Optional[typing.Sequence[jsii.Number]] = None,
        include_last_days: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        weekdays: typing.Optional[typing.Sequence[builtins.str]] = None,
        weeks: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param count: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_vm#count BackupPolicyVm#count}.
        :param months: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_vm#months BackupPolicyVm#months}.
        :param days: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_vm#days BackupPolicyVm#days}.
        :param include_last_days: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_vm#include_last_days BackupPolicyVm#include_last_days}.
        :param weekdays: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_vm#weekdays BackupPolicyVm#weekdays}.
        :param weeks: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_vm#weeks BackupPolicyVm#weeks}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__64bdb9835a13234d8a8afe70ab5325d87428be84ba3d9608c93789dc1fec650e)
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument months", value=months, expected_type=type_hints["months"])
            check_type(argname="argument days", value=days, expected_type=type_hints["days"])
            check_type(argname="argument include_last_days", value=include_last_days, expected_type=type_hints["include_last_days"])
            check_type(argname="argument weekdays", value=weekdays, expected_type=type_hints["weekdays"])
            check_type(argname="argument weeks", value=weeks, expected_type=type_hints["weeks"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "count": count,
            "months": months,
        }
        if days is not None:
            self._values["days"] = days
        if include_last_days is not None:
            self._values["include_last_days"] = include_last_days
        if weekdays is not None:
            self._values["weekdays"] = weekdays
        if weeks is not None:
            self._values["weeks"] = weeks

    @builtins.property
    def count(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_vm#count BackupPolicyVm#count}.'''
        result = self._values.get("count")
        assert result is not None, "Required property 'count' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def months(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_vm#months BackupPolicyVm#months}.'''
        result = self._values.get("months")
        assert result is not None, "Required property 'months' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def days(self) -> typing.Optional[typing.List[jsii.Number]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_vm#days BackupPolicyVm#days}.'''
        result = self._values.get("days")
        return typing.cast(typing.Optional[typing.List[jsii.Number]], result)

    @builtins.property
    def include_last_days(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_vm#include_last_days BackupPolicyVm#include_last_days}.'''
        result = self._values.get("include_last_days")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def weekdays(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_vm#weekdays BackupPolicyVm#weekdays}.'''
        result = self._values.get("weekdays")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def weeks(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_vm#weeks BackupPolicyVm#weeks}.'''
        result = self._values.get("weeks")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BackupPolicyVmRetentionYearly(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BackupPolicyVmRetentionYearlyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.backupPolicyVm.BackupPolicyVmRetentionYearlyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__36ad0d6958746f759ddb3fcc8189855057abd01f9ac8be08db2abe7c94ac1cb8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetDays")
    def reset_days(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDays", []))

    @jsii.member(jsii_name="resetIncludeLastDays")
    def reset_include_last_days(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIncludeLastDays", []))

    @jsii.member(jsii_name="resetWeekdays")
    def reset_weekdays(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWeekdays", []))

    @jsii.member(jsii_name="resetWeeks")
    def reset_weeks(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWeeks", []))

    @builtins.property
    @jsii.member(jsii_name="countInput")
    def count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "countInput"))

    @builtins.property
    @jsii.member(jsii_name="daysInput")
    def days_input(self) -> typing.Optional[typing.List[jsii.Number]]:
        return typing.cast(typing.Optional[typing.List[jsii.Number]], jsii.get(self, "daysInput"))

    @builtins.property
    @jsii.member(jsii_name="includeLastDaysInput")
    def include_last_days_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "includeLastDaysInput"))

    @builtins.property
    @jsii.member(jsii_name="monthsInput")
    def months_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "monthsInput"))

    @builtins.property
    @jsii.member(jsii_name="weekdaysInput")
    def weekdays_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "weekdaysInput"))

    @builtins.property
    @jsii.member(jsii_name="weeksInput")
    def weeks_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "weeksInput"))

    @builtins.property
    @jsii.member(jsii_name="count")
    def count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "count"))

    @count.setter
    def count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b68deff57ded27aed9c52ca83a19d15e2e01a6b03b8a9275343cd95976de745a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "count", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="days")
    def days(self) -> typing.List[jsii.Number]:
        return typing.cast(typing.List[jsii.Number], jsii.get(self, "days"))

    @days.setter
    def days(self, value: typing.List[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__16e5e4570f74e04c8afdf94ac3eabdb9853f39a4c746ebe27a6bc82bb8d063a9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "days", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="includeLastDays")
    def include_last_days(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "includeLastDays"))

    @include_last_days.setter
    def include_last_days(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8cad001fcf935e44feab4b4fe9c6da4099e8bb0ab6ba91085ef3ecd1ac3c4c1d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "includeLastDays", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="months")
    def months(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "months"))

    @months.setter
    def months(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8f837075a89037f2b3fdf72779b1be49f6f89cfee20498dd7252ed10c5ef6da5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "months", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="weekdays")
    def weekdays(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "weekdays"))

    @weekdays.setter
    def weekdays(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5d2b66ad0de09632347d8d0fd1dcfd554e0e9d97a8f1d6066abb33137cfad638)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "weekdays", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="weeks")
    def weeks(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "weeks"))

    @weeks.setter
    def weeks(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f29d1c0978b5e1155ade4db7429c3b4a65ff326d3ade75c40f4c04bbab199be)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "weeks", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[BackupPolicyVmRetentionYearly]:
        return typing.cast(typing.Optional[BackupPolicyVmRetentionYearly], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[BackupPolicyVmRetentionYearly],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5611f82abe0379c69dd96c3e9e20c40db25df6dfec18f9dbc2c84c115d2f2f2b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.backupPolicyVm.BackupPolicyVmTieringPolicy",
    jsii_struct_bases=[],
    name_mapping={"archived_restore_point": "archivedRestorePoint"},
)
class BackupPolicyVmTieringPolicy:
    def __init__(
        self,
        *,
        archived_restore_point: typing.Union["BackupPolicyVmTieringPolicyArchivedRestorePoint", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param archived_restore_point: archived_restore_point block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_vm#archived_restore_point BackupPolicyVm#archived_restore_point}
        '''
        if isinstance(archived_restore_point, dict):
            archived_restore_point = BackupPolicyVmTieringPolicyArchivedRestorePoint(**archived_restore_point)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c4e7b40135044471f73ed33ffaeef0388000c6ad73c55f3dd6888d26b3841578)
            check_type(argname="argument archived_restore_point", value=archived_restore_point, expected_type=type_hints["archived_restore_point"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "archived_restore_point": archived_restore_point,
        }

    @builtins.property
    def archived_restore_point(
        self,
    ) -> "BackupPolicyVmTieringPolicyArchivedRestorePoint":
        '''archived_restore_point block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_vm#archived_restore_point BackupPolicyVm#archived_restore_point}
        '''
        result = self._values.get("archived_restore_point")
        assert result is not None, "Required property 'archived_restore_point' is missing"
        return typing.cast("BackupPolicyVmTieringPolicyArchivedRestorePoint", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BackupPolicyVmTieringPolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.backupPolicyVm.BackupPolicyVmTieringPolicyArchivedRestorePoint",
    jsii_struct_bases=[],
    name_mapping={
        "mode": "mode",
        "duration": "duration",
        "duration_type": "durationType",
    },
)
class BackupPolicyVmTieringPolicyArchivedRestorePoint:
    def __init__(
        self,
        *,
        mode: builtins.str,
        duration: typing.Optional[jsii.Number] = None,
        duration_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_vm#mode BackupPolicyVm#mode}.
        :param duration: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_vm#duration BackupPolicyVm#duration}.
        :param duration_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_vm#duration_type BackupPolicyVm#duration_type}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1970fc8e5acce908b98faddfe7bb43f257f700641d562d32bdb45c7a04911453)
            check_type(argname="argument mode", value=mode, expected_type=type_hints["mode"])
            check_type(argname="argument duration", value=duration, expected_type=type_hints["duration"])
            check_type(argname="argument duration_type", value=duration_type, expected_type=type_hints["duration_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "mode": mode,
        }
        if duration is not None:
            self._values["duration"] = duration
        if duration_type is not None:
            self._values["duration_type"] = duration_type

    @builtins.property
    def mode(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_vm#mode BackupPolicyVm#mode}.'''
        result = self._values.get("mode")
        assert result is not None, "Required property 'mode' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def duration(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_vm#duration BackupPolicyVm#duration}.'''
        result = self._values.get("duration")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def duration_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_vm#duration_type BackupPolicyVm#duration_type}.'''
        result = self._values.get("duration_type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BackupPolicyVmTieringPolicyArchivedRestorePoint(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BackupPolicyVmTieringPolicyArchivedRestorePointOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.backupPolicyVm.BackupPolicyVmTieringPolicyArchivedRestorePointOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__aa235b75d7763a994fc334a10d1f0077949d317510d2a25cec5ed610458e6a07)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetDuration")
    def reset_duration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDuration", []))

    @jsii.member(jsii_name="resetDurationType")
    def reset_duration_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDurationType", []))

    @builtins.property
    @jsii.member(jsii_name="durationInput")
    def duration_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "durationInput"))

    @builtins.property
    @jsii.member(jsii_name="durationTypeInput")
    def duration_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "durationTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="modeInput")
    def mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "modeInput"))

    @builtins.property
    @jsii.member(jsii_name="duration")
    def duration(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "duration"))

    @duration.setter
    def duration(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f1cf6d1a30daf3d801fc4ca49a65d4164b3ff6344373724009bff3698a733ee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "duration", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="durationType")
    def duration_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "durationType"))

    @duration_type.setter
    def duration_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e61fcc6736f6460574481674ac62960867e958425cf291a945cbc14fee7bc9fa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "durationType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="mode")
    def mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mode"))

    @mode.setter
    def mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__957d1385ad14bb4b3ba184e7387a36e3a5d6985e5c29611b2f7c00e556c829b8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[BackupPolicyVmTieringPolicyArchivedRestorePoint]:
        return typing.cast(typing.Optional[BackupPolicyVmTieringPolicyArchivedRestorePoint], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[BackupPolicyVmTieringPolicyArchivedRestorePoint],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e6416d732f0521dd1bb4f6ccdc92f418ece52478caf8991a2b3194dc65a654f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class BackupPolicyVmTieringPolicyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.backupPolicyVm.BackupPolicyVmTieringPolicyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0149b73fda0ce90d6672d653656ad72cd1002aed2dfd22ed3a83fd1d93b5f49e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putArchivedRestorePoint")
    def put_archived_restore_point(
        self,
        *,
        mode: builtins.str,
        duration: typing.Optional[jsii.Number] = None,
        duration_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_vm#mode BackupPolicyVm#mode}.
        :param duration: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_vm#duration BackupPolicyVm#duration}.
        :param duration_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_vm#duration_type BackupPolicyVm#duration_type}.
        '''
        value = BackupPolicyVmTieringPolicyArchivedRestorePoint(
            mode=mode, duration=duration, duration_type=duration_type
        )

        return typing.cast(None, jsii.invoke(self, "putArchivedRestorePoint", [value]))

    @builtins.property
    @jsii.member(jsii_name="archivedRestorePoint")
    def archived_restore_point(
        self,
    ) -> BackupPolicyVmTieringPolicyArchivedRestorePointOutputReference:
        return typing.cast(BackupPolicyVmTieringPolicyArchivedRestorePointOutputReference, jsii.get(self, "archivedRestorePoint"))

    @builtins.property
    @jsii.member(jsii_name="archivedRestorePointInput")
    def archived_restore_point_input(
        self,
    ) -> typing.Optional[BackupPolicyVmTieringPolicyArchivedRestorePoint]:
        return typing.cast(typing.Optional[BackupPolicyVmTieringPolicyArchivedRestorePoint], jsii.get(self, "archivedRestorePointInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[BackupPolicyVmTieringPolicy]:
        return typing.cast(typing.Optional[BackupPolicyVmTieringPolicy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[BackupPolicyVmTieringPolicy],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f397d764c00a4f6d269ce778d896b97fcad28ffcc3b1eb5b1721793ac850efeb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.backupPolicyVm.BackupPolicyVmTimeouts",
    jsii_struct_bases=[],
    name_mapping={
        "create": "create",
        "delete": "delete",
        "read": "read",
        "update": "update",
    },
)
class BackupPolicyVmTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_vm#create BackupPolicyVm#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_vm#delete BackupPolicyVm#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_vm#read BackupPolicyVm#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_vm#update BackupPolicyVm#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__43811beab3461fa03928c3c6953ad12c4691b64f2a60a5ab64cab57cae3a9c2f)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_vm#create BackupPolicyVm#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_vm#delete BackupPolicyVm#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def read(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_vm#read BackupPolicyVm#read}.'''
        result = self._values.get("read")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_vm#update BackupPolicyVm#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BackupPolicyVmTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BackupPolicyVmTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.backupPolicyVm.BackupPolicyVmTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6119538de094812505c101fb41fb9ceb2fb940f9563e0ba86686f958d99c54dc)
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
            type_hints = typing.get_type_hints(_typecheckingstub__deaec4f874ff6d1a046be83029e29d6f2467a65a587e67beb5409fc4deb7a11a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a65533f8e68eeb485620dcbff835c626752dc0e081eb9bf905642cc36c59fd19)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="read")
    def read(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "read"))

    @read.setter
    def read(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2000776e8f6bbf0e28f96808649dbc525f86cc9a8c75c060dc98562787d6f6f4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "read", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac5ba67620542a3e435458749357f7cbd2dc10075291a6ab7ff2851aa9b9680e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BackupPolicyVmTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BackupPolicyVmTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BackupPolicyVmTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5de94b331acb0f60d060ab8ab0eed06fe3d8ea612238b1eb526f4b1b84df7cbc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "BackupPolicyVm",
    "BackupPolicyVmBackup",
    "BackupPolicyVmBackupOutputReference",
    "BackupPolicyVmConfig",
    "BackupPolicyVmInstantRestoreResourceGroup",
    "BackupPolicyVmInstantRestoreResourceGroupOutputReference",
    "BackupPolicyVmRetentionDaily",
    "BackupPolicyVmRetentionDailyOutputReference",
    "BackupPolicyVmRetentionMonthly",
    "BackupPolicyVmRetentionMonthlyOutputReference",
    "BackupPolicyVmRetentionWeekly",
    "BackupPolicyVmRetentionWeeklyOutputReference",
    "BackupPolicyVmRetentionYearly",
    "BackupPolicyVmRetentionYearlyOutputReference",
    "BackupPolicyVmTieringPolicy",
    "BackupPolicyVmTieringPolicyArchivedRestorePoint",
    "BackupPolicyVmTieringPolicyArchivedRestorePointOutputReference",
    "BackupPolicyVmTieringPolicyOutputReference",
    "BackupPolicyVmTimeouts",
    "BackupPolicyVmTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__0a1698716c878c41aa7c0471a1715d1b9a9276e9c79996c6b1438c378e1049d0(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    backup: typing.Union[BackupPolicyVmBackup, typing.Dict[builtins.str, typing.Any]],
    name: builtins.str,
    recovery_vault_name: builtins.str,
    resource_group_name: builtins.str,
    id: typing.Optional[builtins.str] = None,
    instant_restore_resource_group: typing.Optional[typing.Union[BackupPolicyVmInstantRestoreResourceGroup, typing.Dict[builtins.str, typing.Any]]] = None,
    instant_restore_retention_days: typing.Optional[jsii.Number] = None,
    policy_type: typing.Optional[builtins.str] = None,
    retention_daily: typing.Optional[typing.Union[BackupPolicyVmRetentionDaily, typing.Dict[builtins.str, typing.Any]]] = None,
    retention_monthly: typing.Optional[typing.Union[BackupPolicyVmRetentionMonthly, typing.Dict[builtins.str, typing.Any]]] = None,
    retention_weekly: typing.Optional[typing.Union[BackupPolicyVmRetentionWeekly, typing.Dict[builtins.str, typing.Any]]] = None,
    retention_yearly: typing.Optional[typing.Union[BackupPolicyVmRetentionYearly, typing.Dict[builtins.str, typing.Any]]] = None,
    tiering_policy: typing.Optional[typing.Union[BackupPolicyVmTieringPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[BackupPolicyVmTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    timezone: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__8182027f3d77e2fd30fae4a24f10fac3a5ecb4076c81f8d205c63e356c77464b(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d1a2ec30ce6ac88e58b851d95daf93f5cfc47552703ec4f8a67513ce6c1a589(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60737d8cc9e51cdfe8b8992443b56049aed3275ffffbf58e799e95e1e6aa684b(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ccf4668e3354c49cc8cae42c1eb4bd7282af97f77b525143d0810f57a461313e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31c1acd4abc8bd91685ba0233f3f37f20935e2044460b604e41ee723aaac029a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__899bd26c4c0bde1a4cafd09ae9fee2239d1523ce0b126c0973af78fae8f5de5d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3199e3cb11247b322931e3a37dab39f1a31cc30b82e10a9c19c04d023fb9fc47(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cad2aa916c149592cd095b6edc44e378bbedfc8b7049c4ce46ea80778b5dda51(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d7bc6be143d6238b15698c70fa197499d046914287b2257c375803dd53c73b03(
    *,
    frequency: builtins.str,
    time: builtins.str,
    hour_duration: typing.Optional[jsii.Number] = None,
    hour_interval: typing.Optional[jsii.Number] = None,
    weekdays: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__449f443595ff35e90eaa3ea27d036ac6124c67638117751ad0d73bf72612610d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5040dced6321898042d3ca8e11d4d5a4b475d9b4ed49fac4324c869d2f324b02(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66c93fe9abb182263693540a8e5982b6323c24dc0d066f76174d1a18ba14cf94(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76ca270f27280a55a0e7c59cca575874e457fe31985e18e14e965eb6b3ee7313(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f759a5c524bf4c3ecfb62d7407f68ddda52d34b3990ae04dc154bb9a070f62ba(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9697a4d514d107e6a63dc73d853f343bed0d5d4e5f0bcf240b176e80577fceaf(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6b869f4697d73bcadcf464e1c7475de2ff87a76dcf61026e31a6a6ed6e2406d(
    value: typing.Optional[BackupPolicyVmBackup],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ecd90ffd534383f4d3013c04cee9059d9cae17a6e1fe118b26a80cd63f11f66(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    backup: typing.Union[BackupPolicyVmBackup, typing.Dict[builtins.str, typing.Any]],
    name: builtins.str,
    recovery_vault_name: builtins.str,
    resource_group_name: builtins.str,
    id: typing.Optional[builtins.str] = None,
    instant_restore_resource_group: typing.Optional[typing.Union[BackupPolicyVmInstantRestoreResourceGroup, typing.Dict[builtins.str, typing.Any]]] = None,
    instant_restore_retention_days: typing.Optional[jsii.Number] = None,
    policy_type: typing.Optional[builtins.str] = None,
    retention_daily: typing.Optional[typing.Union[BackupPolicyVmRetentionDaily, typing.Dict[builtins.str, typing.Any]]] = None,
    retention_monthly: typing.Optional[typing.Union[BackupPolicyVmRetentionMonthly, typing.Dict[builtins.str, typing.Any]]] = None,
    retention_weekly: typing.Optional[typing.Union[BackupPolicyVmRetentionWeekly, typing.Dict[builtins.str, typing.Any]]] = None,
    retention_yearly: typing.Optional[typing.Union[BackupPolicyVmRetentionYearly, typing.Dict[builtins.str, typing.Any]]] = None,
    tiering_policy: typing.Optional[typing.Union[BackupPolicyVmTieringPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[BackupPolicyVmTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    timezone: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bacf93ee67b874066f2d3cb7b542ce0c409193070e75f64ba802771e0c4568b8(
    *,
    prefix: builtins.str,
    suffix: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e347bc67914f962538ab2427e5f409e8b3f268f276ff3e1cbdab1f6ef0ea820(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54641dfa43f6744bee6d12bde4decb4b4ed5783e1abc61315087faf9a48f7944(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10bbeaff148cd4fd7378d85ee12bedd87215eec5c41624ec9ecd23cc749df391(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5576d1f9d2227764b0bbf5aa0629f452529010ffc7b4420ec3c3e8af93285b36(
    value: typing.Optional[BackupPolicyVmInstantRestoreResourceGroup],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a05279dc383d40cde12754d0824541bae4f1bf3de801f16543f90863d70e295e(
    *,
    count: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9a03f979ae14bc6419257d3f9229fe4a9fc0326def3aacd637045e2f812af33(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f593896179e4f7f81863630e932527ab5352dbfe446b9af0df2cb9d684d01e63(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22944531f27d0c7be5b2604f57029cb72d40854d8a6fec11fdb11ee24d72d4d6(
    value: typing.Optional[BackupPolicyVmRetentionDaily],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__139bc79354c6ba2aba51656be37db8b610098be5d065354f50933936adbd03d7(
    *,
    count: jsii.Number,
    days: typing.Optional[typing.Sequence[jsii.Number]] = None,
    include_last_days: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    weekdays: typing.Optional[typing.Sequence[builtins.str]] = None,
    weeks: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59ec4e4cce803d72cde48b6f631b7f0437e2479104f083246f070ba0e8a7617f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb178e1dcacee59f3367f3703e6b63461d8dd28f0b029832a03ba4d6c06a8c55(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2cfc087e909dd9b1f24efc0db0e26c913719104d236aca14c6518dda6d0b2dcf(
    value: typing.List[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3af798fc726cccacd683044b8e47edfcc488a69bc74976bd7c776a2720ca0f3e(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b8a6c419951a25bbe61f3dd318577954b507c153b4891a0c7feaf9f28443b93(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3fb6e19eef05126ecbd73454b057607dc0a2d07f99e90e71a0d367e275202771(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0745e3ea3ff4978ae52728b5188baa15b71eca5beb12ebc4f83451c6308d2b5c(
    value: typing.Optional[BackupPolicyVmRetentionMonthly],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__95c434888f45992c184ae3bc9da24fac935fd608a6b81ec94f7649808979143c(
    *,
    count: jsii.Number,
    weekdays: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad40afc0bbd8687fdd11a0b92824ed26b895093405459364b60db30872149075(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8913ae15d3bfefff6168c8247e814d1e104d91f2f1f5b9d9c32c39d5c02b7d5(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50c31d28ddd94a8792c3dfec8b988c121110ab4b5ff4cbfeec672ebd8fdb6230(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__155e268544a721f38197955cf2e8812cf9988a4529075f76f162056b6cda5561(
    value: typing.Optional[BackupPolicyVmRetentionWeekly],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64bdb9835a13234d8a8afe70ab5325d87428be84ba3d9608c93789dc1fec650e(
    *,
    count: jsii.Number,
    months: typing.Sequence[builtins.str],
    days: typing.Optional[typing.Sequence[jsii.Number]] = None,
    include_last_days: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    weekdays: typing.Optional[typing.Sequence[builtins.str]] = None,
    weeks: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36ad0d6958746f759ddb3fcc8189855057abd01f9ac8be08db2abe7c94ac1cb8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b68deff57ded27aed9c52ca83a19d15e2e01a6b03b8a9275343cd95976de745a(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16e5e4570f74e04c8afdf94ac3eabdb9853f39a4c746ebe27a6bc82bb8d063a9(
    value: typing.List[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8cad001fcf935e44feab4b4fe9c6da4099e8bb0ab6ba91085ef3ecd1ac3c4c1d(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f837075a89037f2b3fdf72779b1be49f6f89cfee20498dd7252ed10c5ef6da5(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d2b66ad0de09632347d8d0fd1dcfd554e0e9d97a8f1d6066abb33137cfad638(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f29d1c0978b5e1155ade4db7429c3b4a65ff326d3ade75c40f4c04bbab199be(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5611f82abe0379c69dd96c3e9e20c40db25df6dfec18f9dbc2c84c115d2f2f2b(
    value: typing.Optional[BackupPolicyVmRetentionYearly],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4e7b40135044471f73ed33ffaeef0388000c6ad73c55f3dd6888d26b3841578(
    *,
    archived_restore_point: typing.Union[BackupPolicyVmTieringPolicyArchivedRestorePoint, typing.Dict[builtins.str, typing.Any]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1970fc8e5acce908b98faddfe7bb43f257f700641d562d32bdb45c7a04911453(
    *,
    mode: builtins.str,
    duration: typing.Optional[jsii.Number] = None,
    duration_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa235b75d7763a994fc334a10d1f0077949d317510d2a25cec5ed610458e6a07(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f1cf6d1a30daf3d801fc4ca49a65d4164b3ff6344373724009bff3698a733ee(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e61fcc6736f6460574481674ac62960867e958425cf291a945cbc14fee7bc9fa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__957d1385ad14bb4b3ba184e7387a36e3a5d6985e5c29611b2f7c00e556c829b8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e6416d732f0521dd1bb4f6ccdc92f418ece52478caf8991a2b3194dc65a654f(
    value: typing.Optional[BackupPolicyVmTieringPolicyArchivedRestorePoint],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0149b73fda0ce90d6672d653656ad72cd1002aed2dfd22ed3a83fd1d93b5f49e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f397d764c00a4f6d269ce778d896b97fcad28ffcc3b1eb5b1721793ac850efeb(
    value: typing.Optional[BackupPolicyVmTieringPolicy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43811beab3461fa03928c3c6953ad12c4691b64f2a60a5ab64cab57cae3a9c2f(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    read: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6119538de094812505c101fb41fb9ceb2fb940f9563e0ba86686f958d99c54dc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__deaec4f874ff6d1a046be83029e29d6f2467a65a587e67beb5409fc4deb7a11a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a65533f8e68eeb485620dcbff835c626752dc0e081eb9bf905642cc36c59fd19(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2000776e8f6bbf0e28f96808649dbc525f86cc9a8c75c060dc98562787d6f6f4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac5ba67620542a3e435458749357f7cbd2dc10075291a6ab7ff2851aa9b9680e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5de94b331acb0f60d060ab8ab0eed06fe3d8ea612238b1eb526f4b1b84df7cbc(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BackupPolicyVmTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
