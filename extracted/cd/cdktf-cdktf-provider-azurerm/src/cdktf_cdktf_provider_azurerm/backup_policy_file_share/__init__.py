r'''
# `azurerm_backup_policy_file_share`

Refer to the Terraform Registry for docs: [`azurerm_backup_policy_file_share`](https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_file_share).
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


class BackupPolicyFileShare(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.backupPolicyFileShare.BackupPolicyFileShare",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_file_share azurerm_backup_policy_file_share}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        backup: typing.Union["BackupPolicyFileShareBackup", typing.Dict[builtins.str, typing.Any]],
        name: builtins.str,
        recovery_vault_name: builtins.str,
        resource_group_name: builtins.str,
        retention_daily: typing.Union["BackupPolicyFileShareRetentionDaily", typing.Dict[builtins.str, typing.Any]],
        id: typing.Optional[builtins.str] = None,
        retention_monthly: typing.Optional[typing.Union["BackupPolicyFileShareRetentionMonthly", typing.Dict[builtins.str, typing.Any]]] = None,
        retention_weekly: typing.Optional[typing.Union["BackupPolicyFileShareRetentionWeekly", typing.Dict[builtins.str, typing.Any]]] = None,
        retention_yearly: typing.Optional[typing.Union["BackupPolicyFileShareRetentionYearly", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["BackupPolicyFileShareTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        timezone: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_file_share azurerm_backup_policy_file_share} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param backup: backup block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_file_share#backup BackupPolicyFileShare#backup}
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_file_share#name BackupPolicyFileShare#name}.
        :param recovery_vault_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_file_share#recovery_vault_name BackupPolicyFileShare#recovery_vault_name}.
        :param resource_group_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_file_share#resource_group_name BackupPolicyFileShare#resource_group_name}.
        :param retention_daily: retention_daily block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_file_share#retention_daily BackupPolicyFileShare#retention_daily}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_file_share#id BackupPolicyFileShare#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param retention_monthly: retention_monthly block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_file_share#retention_monthly BackupPolicyFileShare#retention_monthly}
        :param retention_weekly: retention_weekly block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_file_share#retention_weekly BackupPolicyFileShare#retention_weekly}
        :param retention_yearly: retention_yearly block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_file_share#retention_yearly BackupPolicyFileShare#retention_yearly}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_file_share#timeouts BackupPolicyFileShare#timeouts}
        :param timezone: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_file_share#timezone BackupPolicyFileShare#timezone}.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0d29b300a000a6a549995cec237dedd489648448601a41338bf544d7900bdea6)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = BackupPolicyFileShareConfig(
            backup=backup,
            name=name,
            recovery_vault_name=recovery_vault_name,
            resource_group_name=resource_group_name,
            retention_daily=retention_daily,
            id=id,
            retention_monthly=retention_monthly,
            retention_weekly=retention_weekly,
            retention_yearly=retention_yearly,
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
        '''Generates CDKTF code for importing a BackupPolicyFileShare resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the BackupPolicyFileShare to import.
        :param import_from_id: The id of the existing BackupPolicyFileShare that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_file_share#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the BackupPolicyFileShare to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__15678ae12bafe047fb5de19f9ec3aeba70800c01bc72cbaeeb1862347977c20b)
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
        hourly: typing.Optional[typing.Union["BackupPolicyFileShareBackupHourly", typing.Dict[builtins.str, typing.Any]]] = None,
        time: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param frequency: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_file_share#frequency BackupPolicyFileShare#frequency}.
        :param hourly: hourly block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_file_share#hourly BackupPolicyFileShare#hourly}
        :param time: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_file_share#time BackupPolicyFileShare#time}.
        '''
        value = BackupPolicyFileShareBackup(
            frequency=frequency, hourly=hourly, time=time
        )

        return typing.cast(None, jsii.invoke(self, "putBackup", [value]))

    @jsii.member(jsii_name="putRetentionDaily")
    def put_retention_daily(self, *, count: jsii.Number) -> None:
        '''
        :param count: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_file_share#count BackupPolicyFileShare#count}.
        '''
        value = BackupPolicyFileShareRetentionDaily(count=count)

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
        :param count: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_file_share#count BackupPolicyFileShare#count}.
        :param days: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_file_share#days BackupPolicyFileShare#days}.
        :param include_last_days: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_file_share#include_last_days BackupPolicyFileShare#include_last_days}.
        :param weekdays: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_file_share#weekdays BackupPolicyFileShare#weekdays}.
        :param weeks: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_file_share#weeks BackupPolicyFileShare#weeks}.
        '''
        value = BackupPolicyFileShareRetentionMonthly(
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
        :param count: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_file_share#count BackupPolicyFileShare#count}.
        :param weekdays: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_file_share#weekdays BackupPolicyFileShare#weekdays}.
        '''
        value = BackupPolicyFileShareRetentionWeekly(count=count, weekdays=weekdays)

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
        :param count: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_file_share#count BackupPolicyFileShare#count}.
        :param months: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_file_share#months BackupPolicyFileShare#months}.
        :param days: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_file_share#days BackupPolicyFileShare#days}.
        :param include_last_days: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_file_share#include_last_days BackupPolicyFileShare#include_last_days}.
        :param weekdays: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_file_share#weekdays BackupPolicyFileShare#weekdays}.
        :param weeks: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_file_share#weeks BackupPolicyFileShare#weeks}.
        '''
        value = BackupPolicyFileShareRetentionYearly(
            count=count,
            months=months,
            days=days,
            include_last_days=include_last_days,
            weekdays=weekdays,
            weeks=weeks,
        )

        return typing.cast(None, jsii.invoke(self, "putRetentionYearly", [value]))

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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_file_share#create BackupPolicyFileShare#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_file_share#delete BackupPolicyFileShare#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_file_share#read BackupPolicyFileShare#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_file_share#update BackupPolicyFileShare#update}.
        '''
        value = BackupPolicyFileShareTimeouts(
            create=create, delete=delete, read=read, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetRetentionMonthly")
    def reset_retention_monthly(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRetentionMonthly", []))

    @jsii.member(jsii_name="resetRetentionWeekly")
    def reset_retention_weekly(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRetentionWeekly", []))

    @jsii.member(jsii_name="resetRetentionYearly")
    def reset_retention_yearly(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRetentionYearly", []))

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
    def backup(self) -> "BackupPolicyFileShareBackupOutputReference":
        return typing.cast("BackupPolicyFileShareBackupOutputReference", jsii.get(self, "backup"))

    @builtins.property
    @jsii.member(jsii_name="retentionDaily")
    def retention_daily(self) -> "BackupPolicyFileShareRetentionDailyOutputReference":
        return typing.cast("BackupPolicyFileShareRetentionDailyOutputReference", jsii.get(self, "retentionDaily"))

    @builtins.property
    @jsii.member(jsii_name="retentionMonthly")
    def retention_monthly(
        self,
    ) -> "BackupPolicyFileShareRetentionMonthlyOutputReference":
        return typing.cast("BackupPolicyFileShareRetentionMonthlyOutputReference", jsii.get(self, "retentionMonthly"))

    @builtins.property
    @jsii.member(jsii_name="retentionWeekly")
    def retention_weekly(self) -> "BackupPolicyFileShareRetentionWeeklyOutputReference":
        return typing.cast("BackupPolicyFileShareRetentionWeeklyOutputReference", jsii.get(self, "retentionWeekly"))

    @builtins.property
    @jsii.member(jsii_name="retentionYearly")
    def retention_yearly(self) -> "BackupPolicyFileShareRetentionYearlyOutputReference":
        return typing.cast("BackupPolicyFileShareRetentionYearlyOutputReference", jsii.get(self, "retentionYearly"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "BackupPolicyFileShareTimeoutsOutputReference":
        return typing.cast("BackupPolicyFileShareTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="backupInput")
    def backup_input(self) -> typing.Optional["BackupPolicyFileShareBackup"]:
        return typing.cast(typing.Optional["BackupPolicyFileShareBackup"], jsii.get(self, "backupInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

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
    def retention_daily_input(
        self,
    ) -> typing.Optional["BackupPolicyFileShareRetentionDaily"]:
        return typing.cast(typing.Optional["BackupPolicyFileShareRetentionDaily"], jsii.get(self, "retentionDailyInput"))

    @builtins.property
    @jsii.member(jsii_name="retentionMonthlyInput")
    def retention_monthly_input(
        self,
    ) -> typing.Optional["BackupPolicyFileShareRetentionMonthly"]:
        return typing.cast(typing.Optional["BackupPolicyFileShareRetentionMonthly"], jsii.get(self, "retentionMonthlyInput"))

    @builtins.property
    @jsii.member(jsii_name="retentionWeeklyInput")
    def retention_weekly_input(
        self,
    ) -> typing.Optional["BackupPolicyFileShareRetentionWeekly"]:
        return typing.cast(typing.Optional["BackupPolicyFileShareRetentionWeekly"], jsii.get(self, "retentionWeeklyInput"))

    @builtins.property
    @jsii.member(jsii_name="retentionYearlyInput")
    def retention_yearly_input(
        self,
    ) -> typing.Optional["BackupPolicyFileShareRetentionYearly"]:
        return typing.cast(typing.Optional["BackupPolicyFileShareRetentionYearly"], jsii.get(self, "retentionYearlyInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "BackupPolicyFileShareTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "BackupPolicyFileShareTimeouts"]], jsii.get(self, "timeoutsInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__22a896c62af1fe99926a7831fa4057f7ecedef36710d7af01f57bd5e7fffca03)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aeaf1245c06adf32492cc376075976e963a902f2e3edc998e7c5afc612bc4c69)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="recoveryVaultName")
    def recovery_vault_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "recoveryVaultName"))

    @recovery_vault_name.setter
    def recovery_vault_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__28e79b2a42581d244b4ef64983a0bf2dd3cd94d6dfd859e08252f22acd48dab8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "recoveryVaultName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resourceGroupName")
    def resource_group_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourceGroupName"))

    @resource_group_name.setter
    def resource_group_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d92a97f4466fb17f7fce891bb7376b265b5c1aacec29bded58a5d3567cf30ada)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceGroupName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="timezone")
    def timezone(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "timezone"))

    @timezone.setter
    def timezone(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5cae1ccbd7972519bdef7751396b1b59276a688f30f6bfa94f89397ee919a166)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timezone", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.backupPolicyFileShare.BackupPolicyFileShareBackup",
    jsii_struct_bases=[],
    name_mapping={"frequency": "frequency", "hourly": "hourly", "time": "time"},
)
class BackupPolicyFileShareBackup:
    def __init__(
        self,
        *,
        frequency: builtins.str,
        hourly: typing.Optional[typing.Union["BackupPolicyFileShareBackupHourly", typing.Dict[builtins.str, typing.Any]]] = None,
        time: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param frequency: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_file_share#frequency BackupPolicyFileShare#frequency}.
        :param hourly: hourly block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_file_share#hourly BackupPolicyFileShare#hourly}
        :param time: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_file_share#time BackupPolicyFileShare#time}.
        '''
        if isinstance(hourly, dict):
            hourly = BackupPolicyFileShareBackupHourly(**hourly)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__02d6775803e1ef502c2522cac9e3cd3a64a178063a3f53a4fccc0e2013d067d5)
            check_type(argname="argument frequency", value=frequency, expected_type=type_hints["frequency"])
            check_type(argname="argument hourly", value=hourly, expected_type=type_hints["hourly"])
            check_type(argname="argument time", value=time, expected_type=type_hints["time"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "frequency": frequency,
        }
        if hourly is not None:
            self._values["hourly"] = hourly
        if time is not None:
            self._values["time"] = time

    @builtins.property
    def frequency(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_file_share#frequency BackupPolicyFileShare#frequency}.'''
        result = self._values.get("frequency")
        assert result is not None, "Required property 'frequency' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def hourly(self) -> typing.Optional["BackupPolicyFileShareBackupHourly"]:
        '''hourly block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_file_share#hourly BackupPolicyFileShare#hourly}
        '''
        result = self._values.get("hourly")
        return typing.cast(typing.Optional["BackupPolicyFileShareBackupHourly"], result)

    @builtins.property
    def time(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_file_share#time BackupPolicyFileShare#time}.'''
        result = self._values.get("time")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BackupPolicyFileShareBackup(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.backupPolicyFileShare.BackupPolicyFileShareBackupHourly",
    jsii_struct_bases=[],
    name_mapping={
        "interval": "interval",
        "start_time": "startTime",
        "window_duration": "windowDuration",
    },
)
class BackupPolicyFileShareBackupHourly:
    def __init__(
        self,
        *,
        interval: jsii.Number,
        start_time: builtins.str,
        window_duration: jsii.Number,
    ) -> None:
        '''
        :param interval: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_file_share#interval BackupPolicyFileShare#interval}.
        :param start_time: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_file_share#start_time BackupPolicyFileShare#start_time}.
        :param window_duration: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_file_share#window_duration BackupPolicyFileShare#window_duration}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6953f72f034ff798daaf117215cb41a39ae5dde1d439d51ba20a94c3dba5bcce)
            check_type(argname="argument interval", value=interval, expected_type=type_hints["interval"])
            check_type(argname="argument start_time", value=start_time, expected_type=type_hints["start_time"])
            check_type(argname="argument window_duration", value=window_duration, expected_type=type_hints["window_duration"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "interval": interval,
            "start_time": start_time,
            "window_duration": window_duration,
        }

    @builtins.property
    def interval(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_file_share#interval BackupPolicyFileShare#interval}.'''
        result = self._values.get("interval")
        assert result is not None, "Required property 'interval' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def start_time(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_file_share#start_time BackupPolicyFileShare#start_time}.'''
        result = self._values.get("start_time")
        assert result is not None, "Required property 'start_time' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def window_duration(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_file_share#window_duration BackupPolicyFileShare#window_duration}.'''
        result = self._values.get("window_duration")
        assert result is not None, "Required property 'window_duration' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BackupPolicyFileShareBackupHourly(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BackupPolicyFileShareBackupHourlyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.backupPolicyFileShare.BackupPolicyFileShareBackupHourlyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bc892ddf49499fee3df7310802cd55eefdc9d5addcb4d96d302c0db30952d552)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="intervalInput")
    def interval_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "intervalInput"))

    @builtins.property
    @jsii.member(jsii_name="startTimeInput")
    def start_time_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "startTimeInput"))

    @builtins.property
    @jsii.member(jsii_name="windowDurationInput")
    def window_duration_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "windowDurationInput"))

    @builtins.property
    @jsii.member(jsii_name="interval")
    def interval(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "interval"))

    @interval.setter
    def interval(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d7d486810919c43464bd1ea0eef97283b0507d5cfcebfeb5131fa8c928b46317)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "interval", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="startTime")
    def start_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "startTime"))

    @start_time.setter
    def start_time(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__37ffe95d88b1734a609409f42c492ef8ff993d7fd3c4041c30ed19deb799ef8e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "startTime", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="windowDuration")
    def window_duration(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "windowDuration"))

    @window_duration.setter
    def window_duration(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c96c3853203c418957af626070e863563c0e03ac88be9faa7121ce5661cc17a9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "windowDuration", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[BackupPolicyFileShareBackupHourly]:
        return typing.cast(typing.Optional[BackupPolicyFileShareBackupHourly], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[BackupPolicyFileShareBackupHourly],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__475cb4eb311e339c5649ce6440d7c777a8511cd7fecc05342c7804ee1c4f4773)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class BackupPolicyFileShareBackupOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.backupPolicyFileShare.BackupPolicyFileShareBackupOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2fb8427c201a19292b1e7a3bd13b0f2f82d98312fa7f8f930500d3aff5b01571)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putHourly")
    def put_hourly(
        self,
        *,
        interval: jsii.Number,
        start_time: builtins.str,
        window_duration: jsii.Number,
    ) -> None:
        '''
        :param interval: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_file_share#interval BackupPolicyFileShare#interval}.
        :param start_time: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_file_share#start_time BackupPolicyFileShare#start_time}.
        :param window_duration: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_file_share#window_duration BackupPolicyFileShare#window_duration}.
        '''
        value = BackupPolicyFileShareBackupHourly(
            interval=interval, start_time=start_time, window_duration=window_duration
        )

        return typing.cast(None, jsii.invoke(self, "putHourly", [value]))

    @jsii.member(jsii_name="resetHourly")
    def reset_hourly(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHourly", []))

    @jsii.member(jsii_name="resetTime")
    def reset_time(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTime", []))

    @builtins.property
    @jsii.member(jsii_name="hourly")
    def hourly(self) -> BackupPolicyFileShareBackupHourlyOutputReference:
        return typing.cast(BackupPolicyFileShareBackupHourlyOutputReference, jsii.get(self, "hourly"))

    @builtins.property
    @jsii.member(jsii_name="frequencyInput")
    def frequency_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "frequencyInput"))

    @builtins.property
    @jsii.member(jsii_name="hourlyInput")
    def hourly_input(self) -> typing.Optional[BackupPolicyFileShareBackupHourly]:
        return typing.cast(typing.Optional[BackupPolicyFileShareBackupHourly], jsii.get(self, "hourlyInput"))

    @builtins.property
    @jsii.member(jsii_name="timeInput")
    def time_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "timeInput"))

    @builtins.property
    @jsii.member(jsii_name="frequency")
    def frequency(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "frequency"))

    @frequency.setter
    def frequency(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__17a30dac303d16ab8017451a6c13b7fc7d205d07ac7e2b9ebbbe79ed72ba73cc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "frequency", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="time")
    def time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "time"))

    @time.setter
    def time(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2a866f24f6740cb351311e4f0e1961249a0f7eb496b84147f84f22043b87af2b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "time", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[BackupPolicyFileShareBackup]:
        return typing.cast(typing.Optional[BackupPolicyFileShareBackup], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[BackupPolicyFileShareBackup],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__50b0b0bdfca03d6fa64981c8243774b6bc1159aac639592c60d691fd2f0979c2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.backupPolicyFileShare.BackupPolicyFileShareConfig",
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
        "retention_daily": "retentionDaily",
        "id": "id",
        "retention_monthly": "retentionMonthly",
        "retention_weekly": "retentionWeekly",
        "retention_yearly": "retentionYearly",
        "timeouts": "timeouts",
        "timezone": "timezone",
    },
)
class BackupPolicyFileShareConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        backup: typing.Union[BackupPolicyFileShareBackup, typing.Dict[builtins.str, typing.Any]],
        name: builtins.str,
        recovery_vault_name: builtins.str,
        resource_group_name: builtins.str,
        retention_daily: typing.Union["BackupPolicyFileShareRetentionDaily", typing.Dict[builtins.str, typing.Any]],
        id: typing.Optional[builtins.str] = None,
        retention_monthly: typing.Optional[typing.Union["BackupPolicyFileShareRetentionMonthly", typing.Dict[builtins.str, typing.Any]]] = None,
        retention_weekly: typing.Optional[typing.Union["BackupPolicyFileShareRetentionWeekly", typing.Dict[builtins.str, typing.Any]]] = None,
        retention_yearly: typing.Optional[typing.Union["BackupPolicyFileShareRetentionYearly", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["BackupPolicyFileShareTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
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
        :param backup: backup block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_file_share#backup BackupPolicyFileShare#backup}
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_file_share#name BackupPolicyFileShare#name}.
        :param recovery_vault_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_file_share#recovery_vault_name BackupPolicyFileShare#recovery_vault_name}.
        :param resource_group_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_file_share#resource_group_name BackupPolicyFileShare#resource_group_name}.
        :param retention_daily: retention_daily block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_file_share#retention_daily BackupPolicyFileShare#retention_daily}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_file_share#id BackupPolicyFileShare#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param retention_monthly: retention_monthly block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_file_share#retention_monthly BackupPolicyFileShare#retention_monthly}
        :param retention_weekly: retention_weekly block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_file_share#retention_weekly BackupPolicyFileShare#retention_weekly}
        :param retention_yearly: retention_yearly block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_file_share#retention_yearly BackupPolicyFileShare#retention_yearly}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_file_share#timeouts BackupPolicyFileShare#timeouts}
        :param timezone: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_file_share#timezone BackupPolicyFileShare#timezone}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(backup, dict):
            backup = BackupPolicyFileShareBackup(**backup)
        if isinstance(retention_daily, dict):
            retention_daily = BackupPolicyFileShareRetentionDaily(**retention_daily)
        if isinstance(retention_monthly, dict):
            retention_monthly = BackupPolicyFileShareRetentionMonthly(**retention_monthly)
        if isinstance(retention_weekly, dict):
            retention_weekly = BackupPolicyFileShareRetentionWeekly(**retention_weekly)
        if isinstance(retention_yearly, dict):
            retention_yearly = BackupPolicyFileShareRetentionYearly(**retention_yearly)
        if isinstance(timeouts, dict):
            timeouts = BackupPolicyFileShareTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__057b1c9018b681ca8b281825536c2156dddcaa175bee1287cb1eeeabd7b849be)
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
            check_type(argname="argument retention_daily", value=retention_daily, expected_type=type_hints["retention_daily"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument retention_monthly", value=retention_monthly, expected_type=type_hints["retention_monthly"])
            check_type(argname="argument retention_weekly", value=retention_weekly, expected_type=type_hints["retention_weekly"])
            check_type(argname="argument retention_yearly", value=retention_yearly, expected_type=type_hints["retention_yearly"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
            check_type(argname="argument timezone", value=timezone, expected_type=type_hints["timezone"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "backup": backup,
            "name": name,
            "recovery_vault_name": recovery_vault_name,
            "resource_group_name": resource_group_name,
            "retention_daily": retention_daily,
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
        if retention_monthly is not None:
            self._values["retention_monthly"] = retention_monthly
        if retention_weekly is not None:
            self._values["retention_weekly"] = retention_weekly
        if retention_yearly is not None:
            self._values["retention_yearly"] = retention_yearly
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
    def backup(self) -> BackupPolicyFileShareBackup:
        '''backup block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_file_share#backup BackupPolicyFileShare#backup}
        '''
        result = self._values.get("backup")
        assert result is not None, "Required property 'backup' is missing"
        return typing.cast(BackupPolicyFileShareBackup, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_file_share#name BackupPolicyFileShare#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def recovery_vault_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_file_share#recovery_vault_name BackupPolicyFileShare#recovery_vault_name}.'''
        result = self._values.get("recovery_vault_name")
        assert result is not None, "Required property 'recovery_vault_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def resource_group_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_file_share#resource_group_name BackupPolicyFileShare#resource_group_name}.'''
        result = self._values.get("resource_group_name")
        assert result is not None, "Required property 'resource_group_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def retention_daily(self) -> "BackupPolicyFileShareRetentionDaily":
        '''retention_daily block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_file_share#retention_daily BackupPolicyFileShare#retention_daily}
        '''
        result = self._values.get("retention_daily")
        assert result is not None, "Required property 'retention_daily' is missing"
        return typing.cast("BackupPolicyFileShareRetentionDaily", result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_file_share#id BackupPolicyFileShare#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def retention_monthly(
        self,
    ) -> typing.Optional["BackupPolicyFileShareRetentionMonthly"]:
        '''retention_monthly block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_file_share#retention_monthly BackupPolicyFileShare#retention_monthly}
        '''
        result = self._values.get("retention_monthly")
        return typing.cast(typing.Optional["BackupPolicyFileShareRetentionMonthly"], result)

    @builtins.property
    def retention_weekly(
        self,
    ) -> typing.Optional["BackupPolicyFileShareRetentionWeekly"]:
        '''retention_weekly block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_file_share#retention_weekly BackupPolicyFileShare#retention_weekly}
        '''
        result = self._values.get("retention_weekly")
        return typing.cast(typing.Optional["BackupPolicyFileShareRetentionWeekly"], result)

    @builtins.property
    def retention_yearly(
        self,
    ) -> typing.Optional["BackupPolicyFileShareRetentionYearly"]:
        '''retention_yearly block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_file_share#retention_yearly BackupPolicyFileShare#retention_yearly}
        '''
        result = self._values.get("retention_yearly")
        return typing.cast(typing.Optional["BackupPolicyFileShareRetentionYearly"], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["BackupPolicyFileShareTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_file_share#timeouts BackupPolicyFileShare#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["BackupPolicyFileShareTimeouts"], result)

    @builtins.property
    def timezone(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_file_share#timezone BackupPolicyFileShare#timezone}.'''
        result = self._values.get("timezone")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BackupPolicyFileShareConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.backupPolicyFileShare.BackupPolicyFileShareRetentionDaily",
    jsii_struct_bases=[],
    name_mapping={"count": "count"},
)
class BackupPolicyFileShareRetentionDaily:
    def __init__(self, *, count: jsii.Number) -> None:
        '''
        :param count: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_file_share#count BackupPolicyFileShare#count}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8dff3ac8d0d7d409bd61a6a4007165acc48b40798d551941a8186c199e445e6d)
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "count": count,
        }

    @builtins.property
    def count(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_file_share#count BackupPolicyFileShare#count}.'''
        result = self._values.get("count")
        assert result is not None, "Required property 'count' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BackupPolicyFileShareRetentionDaily(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BackupPolicyFileShareRetentionDailyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.backupPolicyFileShare.BackupPolicyFileShareRetentionDailyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__92ceec0ef8359824a4bb9e3afdbf119c29f02aa675ff7c154b01eda16d192d14)
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
            type_hints = typing.get_type_hints(_typecheckingstub__23ab7e056439da04f0b3fcf94076bfb8fe4730e0ae2552e9ff56f71b14c7e1bd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "count", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[BackupPolicyFileShareRetentionDaily]:
        return typing.cast(typing.Optional[BackupPolicyFileShareRetentionDaily], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[BackupPolicyFileShareRetentionDaily],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0504dd5699beeb402141e31c3e7eb7c4e3c9edb70b3b1ba35f60068bf0646ad7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.backupPolicyFileShare.BackupPolicyFileShareRetentionMonthly",
    jsii_struct_bases=[],
    name_mapping={
        "count": "count",
        "days": "days",
        "include_last_days": "includeLastDays",
        "weekdays": "weekdays",
        "weeks": "weeks",
    },
)
class BackupPolicyFileShareRetentionMonthly:
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
        :param count: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_file_share#count BackupPolicyFileShare#count}.
        :param days: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_file_share#days BackupPolicyFileShare#days}.
        :param include_last_days: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_file_share#include_last_days BackupPolicyFileShare#include_last_days}.
        :param weekdays: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_file_share#weekdays BackupPolicyFileShare#weekdays}.
        :param weeks: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_file_share#weeks BackupPolicyFileShare#weeks}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8fdb181078a50430be1991221b4ee1d19fe7dd9dad19281810a79c5939d34769)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_file_share#count BackupPolicyFileShare#count}.'''
        result = self._values.get("count")
        assert result is not None, "Required property 'count' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def days(self) -> typing.Optional[typing.List[jsii.Number]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_file_share#days BackupPolicyFileShare#days}.'''
        result = self._values.get("days")
        return typing.cast(typing.Optional[typing.List[jsii.Number]], result)

    @builtins.property
    def include_last_days(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_file_share#include_last_days BackupPolicyFileShare#include_last_days}.'''
        result = self._values.get("include_last_days")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def weekdays(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_file_share#weekdays BackupPolicyFileShare#weekdays}.'''
        result = self._values.get("weekdays")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def weeks(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_file_share#weeks BackupPolicyFileShare#weeks}.'''
        result = self._values.get("weeks")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BackupPolicyFileShareRetentionMonthly(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BackupPolicyFileShareRetentionMonthlyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.backupPolicyFileShare.BackupPolicyFileShareRetentionMonthlyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__39a53eb556224069cd3de4d0beca3458f2f749d857be7af6f2fa695afd763cb6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__135203db9b8e503125de4a8e927adcdad0d0866bc35e8f47c9a2a0b3cff10a7e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "count", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="days")
    def days(self) -> typing.List[jsii.Number]:
        return typing.cast(typing.List[jsii.Number], jsii.get(self, "days"))

    @days.setter
    def days(self, value: typing.List[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f85cc409e5439b15de9b2a3298a0afec79f5be9cd5c0b64fa98f65d5acdcfed)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f1e84918555cbb9a158a27aae5a5d48ec1118d269847951e85ef642db314b27b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "includeLastDays", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="weekdays")
    def weekdays(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "weekdays"))

    @weekdays.setter
    def weekdays(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aab2ceca1f5d5001aaf28a62617c62f612b028c37a6fd6026e462607d8f5927d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "weekdays", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="weeks")
    def weeks(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "weeks"))

    @weeks.setter
    def weeks(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f0276931d6697eb696ed659acd8e12f18e2d5a1d6e277021771e06b923c0ce0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "weeks", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[BackupPolicyFileShareRetentionMonthly]:
        return typing.cast(typing.Optional[BackupPolicyFileShareRetentionMonthly], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[BackupPolicyFileShareRetentionMonthly],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b2c025ae2dac94cd0640ab4c2c52ce789e46a094b5ce8b587cae8cc1e8cfb75)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.backupPolicyFileShare.BackupPolicyFileShareRetentionWeekly",
    jsii_struct_bases=[],
    name_mapping={"count": "count", "weekdays": "weekdays"},
)
class BackupPolicyFileShareRetentionWeekly:
    def __init__(
        self,
        *,
        count: jsii.Number,
        weekdays: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param count: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_file_share#count BackupPolicyFileShare#count}.
        :param weekdays: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_file_share#weekdays BackupPolicyFileShare#weekdays}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e5805539c2b799dbb49353021bd7fa782f553a403be791939d56ee18ccaa9b1c)
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument weekdays", value=weekdays, expected_type=type_hints["weekdays"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "count": count,
            "weekdays": weekdays,
        }

    @builtins.property
    def count(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_file_share#count BackupPolicyFileShare#count}.'''
        result = self._values.get("count")
        assert result is not None, "Required property 'count' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def weekdays(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_file_share#weekdays BackupPolicyFileShare#weekdays}.'''
        result = self._values.get("weekdays")
        assert result is not None, "Required property 'weekdays' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BackupPolicyFileShareRetentionWeekly(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BackupPolicyFileShareRetentionWeeklyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.backupPolicyFileShare.BackupPolicyFileShareRetentionWeeklyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__86244f0877eb231c161ea5c20247dc36e004cde1d13ba5b5b4d68fe032cfedd0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6f6736722e6a370e5b725cb1cfb67ed357c536f02e4bc73a773c605ca8fe0751)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "count", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="weekdays")
    def weekdays(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "weekdays"))

    @weekdays.setter
    def weekdays(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__75b3e128270086ba1703cfa5393322b36ce47b11b155ea673785ba38a612710d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "weekdays", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[BackupPolicyFileShareRetentionWeekly]:
        return typing.cast(typing.Optional[BackupPolicyFileShareRetentionWeekly], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[BackupPolicyFileShareRetentionWeekly],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e1456fa8bb40866949d8dab757e1a4e5defc4a93e405055fef1641bfca8af03a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.backupPolicyFileShare.BackupPolicyFileShareRetentionYearly",
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
class BackupPolicyFileShareRetentionYearly:
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
        :param count: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_file_share#count BackupPolicyFileShare#count}.
        :param months: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_file_share#months BackupPolicyFileShare#months}.
        :param days: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_file_share#days BackupPolicyFileShare#days}.
        :param include_last_days: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_file_share#include_last_days BackupPolicyFileShare#include_last_days}.
        :param weekdays: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_file_share#weekdays BackupPolicyFileShare#weekdays}.
        :param weeks: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_file_share#weeks BackupPolicyFileShare#weeks}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a9bc1f6449d56f130cde5cece0f8a351445738f212e20c06b92fab36b12a88b3)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_file_share#count BackupPolicyFileShare#count}.'''
        result = self._values.get("count")
        assert result is not None, "Required property 'count' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def months(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_file_share#months BackupPolicyFileShare#months}.'''
        result = self._values.get("months")
        assert result is not None, "Required property 'months' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def days(self) -> typing.Optional[typing.List[jsii.Number]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_file_share#days BackupPolicyFileShare#days}.'''
        result = self._values.get("days")
        return typing.cast(typing.Optional[typing.List[jsii.Number]], result)

    @builtins.property
    def include_last_days(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_file_share#include_last_days BackupPolicyFileShare#include_last_days}.'''
        result = self._values.get("include_last_days")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def weekdays(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_file_share#weekdays BackupPolicyFileShare#weekdays}.'''
        result = self._values.get("weekdays")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def weeks(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_file_share#weeks BackupPolicyFileShare#weeks}.'''
        result = self._values.get("weeks")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BackupPolicyFileShareRetentionYearly(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BackupPolicyFileShareRetentionYearlyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.backupPolicyFileShare.BackupPolicyFileShareRetentionYearlyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__45bce1586d439a6ba1d057f76921c3b5f45de66765950226d40b3f9a30cb430a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5f243f1d3ff3606e48321bf2595e41b9c4eb26760b7c4a3b453e6b112a2d32c7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "count", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="days")
    def days(self) -> typing.List[jsii.Number]:
        return typing.cast(typing.List[jsii.Number], jsii.get(self, "days"))

    @days.setter
    def days(self, value: typing.List[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e839c284b6d952a96312ec6899559a32c98794ad13923fe36eaadff20e1f9c6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__874cc38f89de1dcb62e935c738bbb7eee05c2fa8e803451eac55e2133b244f9f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "includeLastDays", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="months")
    def months(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "months"))

    @months.setter
    def months(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cb9ab6ff59358a5927d980a2a9ee1197693c8e7e572523449c012f72312d2b44)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "months", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="weekdays")
    def weekdays(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "weekdays"))

    @weekdays.setter
    def weekdays(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__acbc91ad05ac9554726d60bbeeadab74aaee01c9374680bf2cbc4ee890ea6e6d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "weekdays", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="weeks")
    def weeks(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "weeks"))

    @weeks.setter
    def weeks(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5c316f077ef7a8f8bc353bfeaf6b54a05b789b22daf327ac22f13dafa45051c1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "weeks", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[BackupPolicyFileShareRetentionYearly]:
        return typing.cast(typing.Optional[BackupPolicyFileShareRetentionYearly], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[BackupPolicyFileShareRetentionYearly],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8b69d6b0877c564c16c170e6410d27916bf7547858da3194abd44c3f3d8dfadc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.backupPolicyFileShare.BackupPolicyFileShareTimeouts",
    jsii_struct_bases=[],
    name_mapping={
        "create": "create",
        "delete": "delete",
        "read": "read",
        "update": "update",
    },
)
class BackupPolicyFileShareTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_file_share#create BackupPolicyFileShare#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_file_share#delete BackupPolicyFileShare#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_file_share#read BackupPolicyFileShare#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_file_share#update BackupPolicyFileShare#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__83893bce256371919e9472f0f12fa5523f13b518b70d86dd4f4a377dbbe70df7)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_file_share#create BackupPolicyFileShare#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_file_share#delete BackupPolicyFileShare#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def read(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_file_share#read BackupPolicyFileShare#read}.'''
        result = self._values.get("read")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_file_share#update BackupPolicyFileShare#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BackupPolicyFileShareTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BackupPolicyFileShareTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.backupPolicyFileShare.BackupPolicyFileShareTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f9a7ae14b128ebf2f78a6b5ec6620a4130c60550e28bed6e2933602c913596c1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8fe676ab396b359f79f3f9172cb199df1761c84430031ad49184c7bc3e39aa39)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d578b1bb741cfa45b4b1c361dc4be3bd703ef0a4263bc62d9257f3dad53186f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="read")
    def read(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "read"))

    @read.setter
    def read(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4d1175ec3f7aefaed28ea1b93c3c96739805a5bf22cb44a8fb77cfc6bdccddb1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "read", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9671bd7ca4f3d74ffec739ac56935892c0de1bf750f0beed54223445a97a8f6a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BackupPolicyFileShareTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BackupPolicyFileShareTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BackupPolicyFileShareTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__44cc38a881f69cf30ef0d60f13e4862b6ae78d9cc580f0384cc0e4cf51f6c4fe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "BackupPolicyFileShare",
    "BackupPolicyFileShareBackup",
    "BackupPolicyFileShareBackupHourly",
    "BackupPolicyFileShareBackupHourlyOutputReference",
    "BackupPolicyFileShareBackupOutputReference",
    "BackupPolicyFileShareConfig",
    "BackupPolicyFileShareRetentionDaily",
    "BackupPolicyFileShareRetentionDailyOutputReference",
    "BackupPolicyFileShareRetentionMonthly",
    "BackupPolicyFileShareRetentionMonthlyOutputReference",
    "BackupPolicyFileShareRetentionWeekly",
    "BackupPolicyFileShareRetentionWeeklyOutputReference",
    "BackupPolicyFileShareRetentionYearly",
    "BackupPolicyFileShareRetentionYearlyOutputReference",
    "BackupPolicyFileShareTimeouts",
    "BackupPolicyFileShareTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__0d29b300a000a6a549995cec237dedd489648448601a41338bf544d7900bdea6(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    backup: typing.Union[BackupPolicyFileShareBackup, typing.Dict[builtins.str, typing.Any]],
    name: builtins.str,
    recovery_vault_name: builtins.str,
    resource_group_name: builtins.str,
    retention_daily: typing.Union[BackupPolicyFileShareRetentionDaily, typing.Dict[builtins.str, typing.Any]],
    id: typing.Optional[builtins.str] = None,
    retention_monthly: typing.Optional[typing.Union[BackupPolicyFileShareRetentionMonthly, typing.Dict[builtins.str, typing.Any]]] = None,
    retention_weekly: typing.Optional[typing.Union[BackupPolicyFileShareRetentionWeekly, typing.Dict[builtins.str, typing.Any]]] = None,
    retention_yearly: typing.Optional[typing.Union[BackupPolicyFileShareRetentionYearly, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[BackupPolicyFileShareTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__15678ae12bafe047fb5de19f9ec3aeba70800c01bc72cbaeeb1862347977c20b(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22a896c62af1fe99926a7831fa4057f7ecedef36710d7af01f57bd5e7fffca03(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aeaf1245c06adf32492cc376075976e963a902f2e3edc998e7c5afc612bc4c69(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28e79b2a42581d244b4ef64983a0bf2dd3cd94d6dfd859e08252f22acd48dab8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d92a97f4466fb17f7fce891bb7376b265b5c1aacec29bded58a5d3567cf30ada(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5cae1ccbd7972519bdef7751396b1b59276a688f30f6bfa94f89397ee919a166(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02d6775803e1ef502c2522cac9e3cd3a64a178063a3f53a4fccc0e2013d067d5(
    *,
    frequency: builtins.str,
    hourly: typing.Optional[typing.Union[BackupPolicyFileShareBackupHourly, typing.Dict[builtins.str, typing.Any]]] = None,
    time: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6953f72f034ff798daaf117215cb41a39ae5dde1d439d51ba20a94c3dba5bcce(
    *,
    interval: jsii.Number,
    start_time: builtins.str,
    window_duration: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc892ddf49499fee3df7310802cd55eefdc9d5addcb4d96d302c0db30952d552(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d7d486810919c43464bd1ea0eef97283b0507d5cfcebfeb5131fa8c928b46317(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37ffe95d88b1734a609409f42c492ef8ff993d7fd3c4041c30ed19deb799ef8e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c96c3853203c418957af626070e863563c0e03ac88be9faa7121ce5661cc17a9(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__475cb4eb311e339c5649ce6440d7c777a8511cd7fecc05342c7804ee1c4f4773(
    value: typing.Optional[BackupPolicyFileShareBackupHourly],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2fb8427c201a19292b1e7a3bd13b0f2f82d98312fa7f8f930500d3aff5b01571(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__17a30dac303d16ab8017451a6c13b7fc7d205d07ac7e2b9ebbbe79ed72ba73cc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a866f24f6740cb351311e4f0e1961249a0f7eb496b84147f84f22043b87af2b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50b0b0bdfca03d6fa64981c8243774b6bc1159aac639592c60d691fd2f0979c2(
    value: typing.Optional[BackupPolicyFileShareBackup],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__057b1c9018b681ca8b281825536c2156dddcaa175bee1287cb1eeeabd7b849be(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    backup: typing.Union[BackupPolicyFileShareBackup, typing.Dict[builtins.str, typing.Any]],
    name: builtins.str,
    recovery_vault_name: builtins.str,
    resource_group_name: builtins.str,
    retention_daily: typing.Union[BackupPolicyFileShareRetentionDaily, typing.Dict[builtins.str, typing.Any]],
    id: typing.Optional[builtins.str] = None,
    retention_monthly: typing.Optional[typing.Union[BackupPolicyFileShareRetentionMonthly, typing.Dict[builtins.str, typing.Any]]] = None,
    retention_weekly: typing.Optional[typing.Union[BackupPolicyFileShareRetentionWeekly, typing.Dict[builtins.str, typing.Any]]] = None,
    retention_yearly: typing.Optional[typing.Union[BackupPolicyFileShareRetentionYearly, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[BackupPolicyFileShareTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    timezone: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8dff3ac8d0d7d409bd61a6a4007165acc48b40798d551941a8186c199e445e6d(
    *,
    count: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92ceec0ef8359824a4bb9e3afdbf119c29f02aa675ff7c154b01eda16d192d14(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__23ab7e056439da04f0b3fcf94076bfb8fe4730e0ae2552e9ff56f71b14c7e1bd(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0504dd5699beeb402141e31c3e7eb7c4e3c9edb70b3b1ba35f60068bf0646ad7(
    value: typing.Optional[BackupPolicyFileShareRetentionDaily],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8fdb181078a50430be1991221b4ee1d19fe7dd9dad19281810a79c5939d34769(
    *,
    count: jsii.Number,
    days: typing.Optional[typing.Sequence[jsii.Number]] = None,
    include_last_days: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    weekdays: typing.Optional[typing.Sequence[builtins.str]] = None,
    weeks: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39a53eb556224069cd3de4d0beca3458f2f749d857be7af6f2fa695afd763cb6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__135203db9b8e503125de4a8e927adcdad0d0866bc35e8f47c9a2a0b3cff10a7e(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f85cc409e5439b15de9b2a3298a0afec79f5be9cd5c0b64fa98f65d5acdcfed(
    value: typing.List[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1e84918555cbb9a158a27aae5a5d48ec1118d269847951e85ef642db314b27b(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aab2ceca1f5d5001aaf28a62617c62f612b028c37a6fd6026e462607d8f5927d(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f0276931d6697eb696ed659acd8e12f18e2d5a1d6e277021771e06b923c0ce0(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b2c025ae2dac94cd0640ab4c2c52ce789e46a094b5ce8b587cae8cc1e8cfb75(
    value: typing.Optional[BackupPolicyFileShareRetentionMonthly],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5805539c2b799dbb49353021bd7fa782f553a403be791939d56ee18ccaa9b1c(
    *,
    count: jsii.Number,
    weekdays: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86244f0877eb231c161ea5c20247dc36e004cde1d13ba5b5b4d68fe032cfedd0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f6736722e6a370e5b725cb1cfb67ed357c536f02e4bc73a773c605ca8fe0751(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75b3e128270086ba1703cfa5393322b36ce47b11b155ea673785ba38a612710d(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1456fa8bb40866949d8dab757e1a4e5defc4a93e405055fef1641bfca8af03a(
    value: typing.Optional[BackupPolicyFileShareRetentionWeekly],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9bc1f6449d56f130cde5cece0f8a351445738f212e20c06b92fab36b12a88b3(
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

def _typecheckingstub__45bce1586d439a6ba1d057f76921c3b5f45de66765950226d40b3f9a30cb430a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f243f1d3ff3606e48321bf2595e41b9c4eb26760b7c4a3b453e6b112a2d32c7(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e839c284b6d952a96312ec6899559a32c98794ad13923fe36eaadff20e1f9c6(
    value: typing.List[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__874cc38f89de1dcb62e935c738bbb7eee05c2fa8e803451eac55e2133b244f9f(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb9ab6ff59358a5927d980a2a9ee1197693c8e7e572523449c012f72312d2b44(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__acbc91ad05ac9554726d60bbeeadab74aaee01c9374680bf2cbc4ee890ea6e6d(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c316f077ef7a8f8bc353bfeaf6b54a05b789b22daf327ac22f13dafa45051c1(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b69d6b0877c564c16c170e6410d27916bf7547858da3194abd44c3f3d8dfadc(
    value: typing.Optional[BackupPolicyFileShareRetentionYearly],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83893bce256371919e9472f0f12fa5523f13b518b70d86dd4f4a377dbbe70df7(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    read: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9a7ae14b128ebf2f78a6b5ec6620a4130c60550e28bed6e2933602c913596c1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8fe676ab396b359f79f3f9172cb199df1761c84430031ad49184c7bc3e39aa39(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d578b1bb741cfa45b4b1c361dc4be3bd703ef0a4263bc62d9257f3dad53186f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d1175ec3f7aefaed28ea1b93c3c96739805a5bf22cb44a8fb77cfc6bdccddb1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9671bd7ca4f3d74ffec739ac56935892c0de1bf750f0beed54223445a97a8f6a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44cc38a881f69cf30ef0d60f13e4862b6ae78d9cc580f0384cc0e4cf51f6c4fe(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BackupPolicyFileShareTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
