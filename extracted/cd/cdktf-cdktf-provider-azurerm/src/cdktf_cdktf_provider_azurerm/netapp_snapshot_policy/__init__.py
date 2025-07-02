r'''
# `azurerm_netapp_snapshot_policy`

Refer to the Terraform Registry for docs: [`azurerm_netapp_snapshot_policy`](https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_snapshot_policy).
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


class NetappSnapshotPolicy(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.netappSnapshotPolicy.NetappSnapshotPolicy",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_snapshot_policy azurerm_netapp_snapshot_policy}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        account_name: builtins.str,
        enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        location: builtins.str,
        name: builtins.str,
        resource_group_name: builtins.str,
        daily_schedule: typing.Optional[typing.Union["NetappSnapshotPolicyDailySchedule", typing.Dict[builtins.str, typing.Any]]] = None,
        hourly_schedule: typing.Optional[typing.Union["NetappSnapshotPolicyHourlySchedule", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        monthly_schedule: typing.Optional[typing.Union["NetappSnapshotPolicyMonthlySchedule", typing.Dict[builtins.str, typing.Any]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["NetappSnapshotPolicyTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        weekly_schedule: typing.Optional[typing.Union["NetappSnapshotPolicyWeeklySchedule", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_snapshot_policy azurerm_netapp_snapshot_policy} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param account_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_snapshot_policy#account_name NetappSnapshotPolicy#account_name}.
        :param enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_snapshot_policy#enabled NetappSnapshotPolicy#enabled}.
        :param location: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_snapshot_policy#location NetappSnapshotPolicy#location}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_snapshot_policy#name NetappSnapshotPolicy#name}.
        :param resource_group_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_snapshot_policy#resource_group_name NetappSnapshotPolicy#resource_group_name}.
        :param daily_schedule: daily_schedule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_snapshot_policy#daily_schedule NetappSnapshotPolicy#daily_schedule}
        :param hourly_schedule: hourly_schedule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_snapshot_policy#hourly_schedule NetappSnapshotPolicy#hourly_schedule}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_snapshot_policy#id NetappSnapshotPolicy#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param monthly_schedule: monthly_schedule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_snapshot_policy#monthly_schedule NetappSnapshotPolicy#monthly_schedule}
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_snapshot_policy#tags NetappSnapshotPolicy#tags}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_snapshot_policy#timeouts NetappSnapshotPolicy#timeouts}
        :param weekly_schedule: weekly_schedule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_snapshot_policy#weekly_schedule NetappSnapshotPolicy#weekly_schedule}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f00ad250f4197a6aced9f323cdabe7859b41b4d3de90ce3d26c0d3b42c253195)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = NetappSnapshotPolicyConfig(
            account_name=account_name,
            enabled=enabled,
            location=location,
            name=name,
            resource_group_name=resource_group_name,
            daily_schedule=daily_schedule,
            hourly_schedule=hourly_schedule,
            id=id,
            monthly_schedule=monthly_schedule,
            tags=tags,
            timeouts=timeouts,
            weekly_schedule=weekly_schedule,
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
        '''Generates CDKTF code for importing a NetappSnapshotPolicy resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the NetappSnapshotPolicy to import.
        :param import_from_id: The id of the existing NetappSnapshotPolicy that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_snapshot_policy#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the NetappSnapshotPolicy to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9c73309ced1abb33f63332a180ef6dc55364e6848288069f21656c60d4957b11)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putDailySchedule")
    def put_daily_schedule(
        self,
        *,
        hour: jsii.Number,
        minute: jsii.Number,
        snapshots_to_keep: jsii.Number,
    ) -> None:
        '''
        :param hour: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_snapshot_policy#hour NetappSnapshotPolicy#hour}.
        :param minute: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_snapshot_policy#minute NetappSnapshotPolicy#minute}.
        :param snapshots_to_keep: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_snapshot_policy#snapshots_to_keep NetappSnapshotPolicy#snapshots_to_keep}.
        '''
        value = NetappSnapshotPolicyDailySchedule(
            hour=hour, minute=minute, snapshots_to_keep=snapshots_to_keep
        )

        return typing.cast(None, jsii.invoke(self, "putDailySchedule", [value]))

    @jsii.member(jsii_name="putHourlySchedule")
    def put_hourly_schedule(
        self,
        *,
        minute: jsii.Number,
        snapshots_to_keep: jsii.Number,
    ) -> None:
        '''
        :param minute: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_snapshot_policy#minute NetappSnapshotPolicy#minute}.
        :param snapshots_to_keep: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_snapshot_policy#snapshots_to_keep NetappSnapshotPolicy#snapshots_to_keep}.
        '''
        value = NetappSnapshotPolicyHourlySchedule(
            minute=minute, snapshots_to_keep=snapshots_to_keep
        )

        return typing.cast(None, jsii.invoke(self, "putHourlySchedule", [value]))

    @jsii.member(jsii_name="putMonthlySchedule")
    def put_monthly_schedule(
        self,
        *,
        days_of_month: typing.Sequence[jsii.Number],
        hour: jsii.Number,
        minute: jsii.Number,
        snapshots_to_keep: jsii.Number,
    ) -> None:
        '''
        :param days_of_month: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_snapshot_policy#days_of_month NetappSnapshotPolicy#days_of_month}.
        :param hour: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_snapshot_policy#hour NetappSnapshotPolicy#hour}.
        :param minute: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_snapshot_policy#minute NetappSnapshotPolicy#minute}.
        :param snapshots_to_keep: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_snapshot_policy#snapshots_to_keep NetappSnapshotPolicy#snapshots_to_keep}.
        '''
        value = NetappSnapshotPolicyMonthlySchedule(
            days_of_month=days_of_month,
            hour=hour,
            minute=minute,
            snapshots_to_keep=snapshots_to_keep,
        )

        return typing.cast(None, jsii.invoke(self, "putMonthlySchedule", [value]))

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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_snapshot_policy#create NetappSnapshotPolicy#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_snapshot_policy#delete NetappSnapshotPolicy#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_snapshot_policy#read NetappSnapshotPolicy#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_snapshot_policy#update NetappSnapshotPolicy#update}.
        '''
        value = NetappSnapshotPolicyTimeouts(
            create=create, delete=delete, read=read, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="putWeeklySchedule")
    def put_weekly_schedule(
        self,
        *,
        days_of_week: typing.Sequence[builtins.str],
        hour: jsii.Number,
        minute: jsii.Number,
        snapshots_to_keep: jsii.Number,
    ) -> None:
        '''
        :param days_of_week: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_snapshot_policy#days_of_week NetappSnapshotPolicy#days_of_week}.
        :param hour: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_snapshot_policy#hour NetappSnapshotPolicy#hour}.
        :param minute: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_snapshot_policy#minute NetappSnapshotPolicy#minute}.
        :param snapshots_to_keep: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_snapshot_policy#snapshots_to_keep NetappSnapshotPolicy#snapshots_to_keep}.
        '''
        value = NetappSnapshotPolicyWeeklySchedule(
            days_of_week=days_of_week,
            hour=hour,
            minute=minute,
            snapshots_to_keep=snapshots_to_keep,
        )

        return typing.cast(None, jsii.invoke(self, "putWeeklySchedule", [value]))

    @jsii.member(jsii_name="resetDailySchedule")
    def reset_daily_schedule(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDailySchedule", []))

    @jsii.member(jsii_name="resetHourlySchedule")
    def reset_hourly_schedule(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHourlySchedule", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetMonthlySchedule")
    def reset_monthly_schedule(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMonthlySchedule", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

    @jsii.member(jsii_name="resetWeeklySchedule")
    def reset_weekly_schedule(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWeeklySchedule", []))

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
    @jsii.member(jsii_name="dailySchedule")
    def daily_schedule(self) -> "NetappSnapshotPolicyDailyScheduleOutputReference":
        return typing.cast("NetappSnapshotPolicyDailyScheduleOutputReference", jsii.get(self, "dailySchedule"))

    @builtins.property
    @jsii.member(jsii_name="hourlySchedule")
    def hourly_schedule(self) -> "NetappSnapshotPolicyHourlyScheduleOutputReference":
        return typing.cast("NetappSnapshotPolicyHourlyScheduleOutputReference", jsii.get(self, "hourlySchedule"))

    @builtins.property
    @jsii.member(jsii_name="monthlySchedule")
    def monthly_schedule(self) -> "NetappSnapshotPolicyMonthlyScheduleOutputReference":
        return typing.cast("NetappSnapshotPolicyMonthlyScheduleOutputReference", jsii.get(self, "monthlySchedule"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "NetappSnapshotPolicyTimeoutsOutputReference":
        return typing.cast("NetappSnapshotPolicyTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="weeklySchedule")
    def weekly_schedule(self) -> "NetappSnapshotPolicyWeeklyScheduleOutputReference":
        return typing.cast("NetappSnapshotPolicyWeeklyScheduleOutputReference", jsii.get(self, "weeklySchedule"))

    @builtins.property
    @jsii.member(jsii_name="accountNameInput")
    def account_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "accountNameInput"))

    @builtins.property
    @jsii.member(jsii_name="dailyScheduleInput")
    def daily_schedule_input(
        self,
    ) -> typing.Optional["NetappSnapshotPolicyDailySchedule"]:
        return typing.cast(typing.Optional["NetappSnapshotPolicyDailySchedule"], jsii.get(self, "dailyScheduleInput"))

    @builtins.property
    @jsii.member(jsii_name="enabledInput")
    def enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enabledInput"))

    @builtins.property
    @jsii.member(jsii_name="hourlyScheduleInput")
    def hourly_schedule_input(
        self,
    ) -> typing.Optional["NetappSnapshotPolicyHourlySchedule"]:
        return typing.cast(typing.Optional["NetappSnapshotPolicyHourlySchedule"], jsii.get(self, "hourlyScheduleInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="locationInput")
    def location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "locationInput"))

    @builtins.property
    @jsii.member(jsii_name="monthlyScheduleInput")
    def monthly_schedule_input(
        self,
    ) -> typing.Optional["NetappSnapshotPolicyMonthlySchedule"]:
        return typing.cast(typing.Optional["NetappSnapshotPolicyMonthlySchedule"], jsii.get(self, "monthlyScheduleInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceGroupNameInput")
    def resource_group_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "resourceGroupNameInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsInput")
    def tags_input(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "tagsInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "NetappSnapshotPolicyTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "NetappSnapshotPolicyTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="weeklyScheduleInput")
    def weekly_schedule_input(
        self,
    ) -> typing.Optional["NetappSnapshotPolicyWeeklySchedule"]:
        return typing.cast(typing.Optional["NetappSnapshotPolicyWeeklySchedule"], jsii.get(self, "weeklyScheduleInput"))

    @builtins.property
    @jsii.member(jsii_name="accountName")
    def account_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "accountName"))

    @account_name.setter
    def account_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a10af77e88c3df54a77ad287e1174dd59551430d22500b5a3e3f2b0755035d33)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accountName", value) # pyright: ignore[reportArgumentType]

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
            type_hints = typing.get_type_hints(_typecheckingstub__cf621192ec38fa24a53fe1b3147293d5e610d83e678c89b5b578d01f90ae995b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__18fd458356418752e2d2ebd1d54c6302c69a34f6beb3d6fce3f92ba2e6ff17e7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3eb7aa0d7333ac766636e4f03504a57bc6673a52028408ddeb5946de1c821b68)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__390563a5fc3e52d6b553221556106ed8a5f4d961ecb64af7c9dce9b01c15b9b2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resourceGroupName")
    def resource_group_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourceGroupName"))

    @resource_group_name.setter
    def resource_group_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eec06454c5cc8d8e032b060aa595565c0d38b498c49d3ebd1eaec67be9a390d4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceGroupName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fdf204326c6d585d222d55f6679c289b2f058036b9c68de41944368658df5df8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.netappSnapshotPolicy.NetappSnapshotPolicyConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "account_name": "accountName",
        "enabled": "enabled",
        "location": "location",
        "name": "name",
        "resource_group_name": "resourceGroupName",
        "daily_schedule": "dailySchedule",
        "hourly_schedule": "hourlySchedule",
        "id": "id",
        "monthly_schedule": "monthlySchedule",
        "tags": "tags",
        "timeouts": "timeouts",
        "weekly_schedule": "weeklySchedule",
    },
)
class NetappSnapshotPolicyConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        account_name: builtins.str,
        enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        location: builtins.str,
        name: builtins.str,
        resource_group_name: builtins.str,
        daily_schedule: typing.Optional[typing.Union["NetappSnapshotPolicyDailySchedule", typing.Dict[builtins.str, typing.Any]]] = None,
        hourly_schedule: typing.Optional[typing.Union["NetappSnapshotPolicyHourlySchedule", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        monthly_schedule: typing.Optional[typing.Union["NetappSnapshotPolicyMonthlySchedule", typing.Dict[builtins.str, typing.Any]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["NetappSnapshotPolicyTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        weekly_schedule: typing.Optional[typing.Union["NetappSnapshotPolicyWeeklySchedule", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param account_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_snapshot_policy#account_name NetappSnapshotPolicy#account_name}.
        :param enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_snapshot_policy#enabled NetappSnapshotPolicy#enabled}.
        :param location: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_snapshot_policy#location NetappSnapshotPolicy#location}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_snapshot_policy#name NetappSnapshotPolicy#name}.
        :param resource_group_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_snapshot_policy#resource_group_name NetappSnapshotPolicy#resource_group_name}.
        :param daily_schedule: daily_schedule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_snapshot_policy#daily_schedule NetappSnapshotPolicy#daily_schedule}
        :param hourly_schedule: hourly_schedule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_snapshot_policy#hourly_schedule NetappSnapshotPolicy#hourly_schedule}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_snapshot_policy#id NetappSnapshotPolicy#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param monthly_schedule: monthly_schedule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_snapshot_policy#monthly_schedule NetappSnapshotPolicy#monthly_schedule}
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_snapshot_policy#tags NetappSnapshotPolicy#tags}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_snapshot_policy#timeouts NetappSnapshotPolicy#timeouts}
        :param weekly_schedule: weekly_schedule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_snapshot_policy#weekly_schedule NetappSnapshotPolicy#weekly_schedule}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(daily_schedule, dict):
            daily_schedule = NetappSnapshotPolicyDailySchedule(**daily_schedule)
        if isinstance(hourly_schedule, dict):
            hourly_schedule = NetappSnapshotPolicyHourlySchedule(**hourly_schedule)
        if isinstance(monthly_schedule, dict):
            monthly_schedule = NetappSnapshotPolicyMonthlySchedule(**monthly_schedule)
        if isinstance(timeouts, dict):
            timeouts = NetappSnapshotPolicyTimeouts(**timeouts)
        if isinstance(weekly_schedule, dict):
            weekly_schedule = NetappSnapshotPolicyWeeklySchedule(**weekly_schedule)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__66a728b0d85d8666818fe218d35001a41f3eb0e1e1bdf5a199f38c56f099edbd)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument account_name", value=account_name, expected_type=type_hints["account_name"])
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument resource_group_name", value=resource_group_name, expected_type=type_hints["resource_group_name"])
            check_type(argname="argument daily_schedule", value=daily_schedule, expected_type=type_hints["daily_schedule"])
            check_type(argname="argument hourly_schedule", value=hourly_schedule, expected_type=type_hints["hourly_schedule"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument monthly_schedule", value=monthly_schedule, expected_type=type_hints["monthly_schedule"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
            check_type(argname="argument weekly_schedule", value=weekly_schedule, expected_type=type_hints["weekly_schedule"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "account_name": account_name,
            "enabled": enabled,
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
        if daily_schedule is not None:
            self._values["daily_schedule"] = daily_schedule
        if hourly_schedule is not None:
            self._values["hourly_schedule"] = hourly_schedule
        if id is not None:
            self._values["id"] = id
        if monthly_schedule is not None:
            self._values["monthly_schedule"] = monthly_schedule
        if tags is not None:
            self._values["tags"] = tags
        if timeouts is not None:
            self._values["timeouts"] = timeouts
        if weekly_schedule is not None:
            self._values["weekly_schedule"] = weekly_schedule

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
    def account_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_snapshot_policy#account_name NetappSnapshotPolicy#account_name}.'''
        result = self._values.get("account_name")
        assert result is not None, "Required property 'account_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_snapshot_policy#enabled NetappSnapshotPolicy#enabled}.'''
        result = self._values.get("enabled")
        assert result is not None, "Required property 'enabled' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    @builtins.property
    def location(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_snapshot_policy#location NetappSnapshotPolicy#location}.'''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_snapshot_policy#name NetappSnapshotPolicy#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def resource_group_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_snapshot_policy#resource_group_name NetappSnapshotPolicy#resource_group_name}.'''
        result = self._values.get("resource_group_name")
        assert result is not None, "Required property 'resource_group_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def daily_schedule(self) -> typing.Optional["NetappSnapshotPolicyDailySchedule"]:
        '''daily_schedule block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_snapshot_policy#daily_schedule NetappSnapshotPolicy#daily_schedule}
        '''
        result = self._values.get("daily_schedule")
        return typing.cast(typing.Optional["NetappSnapshotPolicyDailySchedule"], result)

    @builtins.property
    def hourly_schedule(self) -> typing.Optional["NetappSnapshotPolicyHourlySchedule"]:
        '''hourly_schedule block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_snapshot_policy#hourly_schedule NetappSnapshotPolicy#hourly_schedule}
        '''
        result = self._values.get("hourly_schedule")
        return typing.cast(typing.Optional["NetappSnapshotPolicyHourlySchedule"], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_snapshot_policy#id NetappSnapshotPolicy#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def monthly_schedule(
        self,
    ) -> typing.Optional["NetappSnapshotPolicyMonthlySchedule"]:
        '''monthly_schedule block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_snapshot_policy#monthly_schedule NetappSnapshotPolicy#monthly_schedule}
        '''
        result = self._values.get("monthly_schedule")
        return typing.cast(typing.Optional["NetappSnapshotPolicyMonthlySchedule"], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_snapshot_policy#tags NetappSnapshotPolicy#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["NetappSnapshotPolicyTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_snapshot_policy#timeouts NetappSnapshotPolicy#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["NetappSnapshotPolicyTimeouts"], result)

    @builtins.property
    def weekly_schedule(self) -> typing.Optional["NetappSnapshotPolicyWeeklySchedule"]:
        '''weekly_schedule block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_snapshot_policy#weekly_schedule NetappSnapshotPolicy#weekly_schedule}
        '''
        result = self._values.get("weekly_schedule")
        return typing.cast(typing.Optional["NetappSnapshotPolicyWeeklySchedule"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetappSnapshotPolicyConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.netappSnapshotPolicy.NetappSnapshotPolicyDailySchedule",
    jsii_struct_bases=[],
    name_mapping={
        "hour": "hour",
        "minute": "minute",
        "snapshots_to_keep": "snapshotsToKeep",
    },
)
class NetappSnapshotPolicyDailySchedule:
    def __init__(
        self,
        *,
        hour: jsii.Number,
        minute: jsii.Number,
        snapshots_to_keep: jsii.Number,
    ) -> None:
        '''
        :param hour: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_snapshot_policy#hour NetappSnapshotPolicy#hour}.
        :param minute: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_snapshot_policy#minute NetappSnapshotPolicy#minute}.
        :param snapshots_to_keep: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_snapshot_policy#snapshots_to_keep NetappSnapshotPolicy#snapshots_to_keep}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a69dd1c08d0ecfdc0a32ea567f1f9f51c19cdd2efb2373a180684d983b6fc2e8)
            check_type(argname="argument hour", value=hour, expected_type=type_hints["hour"])
            check_type(argname="argument minute", value=minute, expected_type=type_hints["minute"])
            check_type(argname="argument snapshots_to_keep", value=snapshots_to_keep, expected_type=type_hints["snapshots_to_keep"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "hour": hour,
            "minute": minute,
            "snapshots_to_keep": snapshots_to_keep,
        }

    @builtins.property
    def hour(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_snapshot_policy#hour NetappSnapshotPolicy#hour}.'''
        result = self._values.get("hour")
        assert result is not None, "Required property 'hour' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def minute(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_snapshot_policy#minute NetappSnapshotPolicy#minute}.'''
        result = self._values.get("minute")
        assert result is not None, "Required property 'minute' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def snapshots_to_keep(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_snapshot_policy#snapshots_to_keep NetappSnapshotPolicy#snapshots_to_keep}.'''
        result = self._values.get("snapshots_to_keep")
        assert result is not None, "Required property 'snapshots_to_keep' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetappSnapshotPolicyDailySchedule(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NetappSnapshotPolicyDailyScheduleOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.netappSnapshotPolicy.NetappSnapshotPolicyDailyScheduleOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6295798d3c2d30edd00c704297cd9c5e660264101ca19789719fd29c98994e92)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="hourInput")
    def hour_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "hourInput"))

    @builtins.property
    @jsii.member(jsii_name="minuteInput")
    def minute_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "minuteInput"))

    @builtins.property
    @jsii.member(jsii_name="snapshotsToKeepInput")
    def snapshots_to_keep_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "snapshotsToKeepInput"))

    @builtins.property
    @jsii.member(jsii_name="hour")
    def hour(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "hour"))

    @hour.setter
    def hour(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__44280b4fad611e74a3b583cc91df7cd2098c59a1b81bb102646d032a16528d56)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hour", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="minute")
    def minute(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "minute"))

    @minute.setter
    def minute(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f8cece723b5fcdc3377caf22100e5b5653574d9739e827a6aa00f9555016cfe3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minute", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="snapshotsToKeep")
    def snapshots_to_keep(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "snapshotsToKeep"))

    @snapshots_to_keep.setter
    def snapshots_to_keep(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__64973127dac5a139c385a6460b9e1addac00e23a4d5d257d34b88f6814351996)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "snapshotsToKeep", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[NetappSnapshotPolicyDailySchedule]:
        return typing.cast(typing.Optional[NetappSnapshotPolicyDailySchedule], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[NetappSnapshotPolicyDailySchedule],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eb874b3cc657bd70e687440e9f6f751b04c810cb0eb9d60c2bc2e158c70beefe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.netappSnapshotPolicy.NetappSnapshotPolicyHourlySchedule",
    jsii_struct_bases=[],
    name_mapping={"minute": "minute", "snapshots_to_keep": "snapshotsToKeep"},
)
class NetappSnapshotPolicyHourlySchedule:
    def __init__(self, *, minute: jsii.Number, snapshots_to_keep: jsii.Number) -> None:
        '''
        :param minute: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_snapshot_policy#minute NetappSnapshotPolicy#minute}.
        :param snapshots_to_keep: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_snapshot_policy#snapshots_to_keep NetappSnapshotPolicy#snapshots_to_keep}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f3511b55b4d934adf7cb8cbf9fc18601034f6e586754f0502dc8e6c2419f8a74)
            check_type(argname="argument minute", value=minute, expected_type=type_hints["minute"])
            check_type(argname="argument snapshots_to_keep", value=snapshots_to_keep, expected_type=type_hints["snapshots_to_keep"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "minute": minute,
            "snapshots_to_keep": snapshots_to_keep,
        }

    @builtins.property
    def minute(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_snapshot_policy#minute NetappSnapshotPolicy#minute}.'''
        result = self._values.get("minute")
        assert result is not None, "Required property 'minute' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def snapshots_to_keep(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_snapshot_policy#snapshots_to_keep NetappSnapshotPolicy#snapshots_to_keep}.'''
        result = self._values.get("snapshots_to_keep")
        assert result is not None, "Required property 'snapshots_to_keep' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetappSnapshotPolicyHourlySchedule(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NetappSnapshotPolicyHourlyScheduleOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.netappSnapshotPolicy.NetappSnapshotPolicyHourlyScheduleOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a8705aa9dfaec877fbb8e3908cda74fe3d0ec016f641e48a2ca57bbc637bfc61)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="minuteInput")
    def minute_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "minuteInput"))

    @builtins.property
    @jsii.member(jsii_name="snapshotsToKeepInput")
    def snapshots_to_keep_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "snapshotsToKeepInput"))

    @builtins.property
    @jsii.member(jsii_name="minute")
    def minute(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "minute"))

    @minute.setter
    def minute(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__61c982b7b2deff062c98365547b7fd670a3ef2adee57b0f479469174a3a59cc0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minute", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="snapshotsToKeep")
    def snapshots_to_keep(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "snapshotsToKeep"))

    @snapshots_to_keep.setter
    def snapshots_to_keep(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__74ef15df45604bc19155e6efa68eba23444cf1c82ee882bd50bc0952682a1d78)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "snapshotsToKeep", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[NetappSnapshotPolicyHourlySchedule]:
        return typing.cast(typing.Optional[NetappSnapshotPolicyHourlySchedule], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[NetappSnapshotPolicyHourlySchedule],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b2d34a10b8676242f3a0565aee53d61a182e23d5d89c43b6c147f8cc92a2f303)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.netappSnapshotPolicy.NetappSnapshotPolicyMonthlySchedule",
    jsii_struct_bases=[],
    name_mapping={
        "days_of_month": "daysOfMonth",
        "hour": "hour",
        "minute": "minute",
        "snapshots_to_keep": "snapshotsToKeep",
    },
)
class NetappSnapshotPolicyMonthlySchedule:
    def __init__(
        self,
        *,
        days_of_month: typing.Sequence[jsii.Number],
        hour: jsii.Number,
        minute: jsii.Number,
        snapshots_to_keep: jsii.Number,
    ) -> None:
        '''
        :param days_of_month: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_snapshot_policy#days_of_month NetappSnapshotPolicy#days_of_month}.
        :param hour: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_snapshot_policy#hour NetappSnapshotPolicy#hour}.
        :param minute: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_snapshot_policy#minute NetappSnapshotPolicy#minute}.
        :param snapshots_to_keep: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_snapshot_policy#snapshots_to_keep NetappSnapshotPolicy#snapshots_to_keep}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4d82c28f26e4c4a23019fb0039ff3558b79ef50ac28ffd55fe5e924410bc3cd7)
            check_type(argname="argument days_of_month", value=days_of_month, expected_type=type_hints["days_of_month"])
            check_type(argname="argument hour", value=hour, expected_type=type_hints["hour"])
            check_type(argname="argument minute", value=minute, expected_type=type_hints["minute"])
            check_type(argname="argument snapshots_to_keep", value=snapshots_to_keep, expected_type=type_hints["snapshots_to_keep"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "days_of_month": days_of_month,
            "hour": hour,
            "minute": minute,
            "snapshots_to_keep": snapshots_to_keep,
        }

    @builtins.property
    def days_of_month(self) -> typing.List[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_snapshot_policy#days_of_month NetappSnapshotPolicy#days_of_month}.'''
        result = self._values.get("days_of_month")
        assert result is not None, "Required property 'days_of_month' is missing"
        return typing.cast(typing.List[jsii.Number], result)

    @builtins.property
    def hour(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_snapshot_policy#hour NetappSnapshotPolicy#hour}.'''
        result = self._values.get("hour")
        assert result is not None, "Required property 'hour' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def minute(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_snapshot_policy#minute NetappSnapshotPolicy#minute}.'''
        result = self._values.get("minute")
        assert result is not None, "Required property 'minute' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def snapshots_to_keep(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_snapshot_policy#snapshots_to_keep NetappSnapshotPolicy#snapshots_to_keep}.'''
        result = self._values.get("snapshots_to_keep")
        assert result is not None, "Required property 'snapshots_to_keep' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetappSnapshotPolicyMonthlySchedule(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NetappSnapshotPolicyMonthlyScheduleOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.netappSnapshotPolicy.NetappSnapshotPolicyMonthlyScheduleOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__520005245147cf8c6f67a69086b440d6f9d8becda0b7eb1e14f60c8c1c0538e8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="daysOfMonthInput")
    def days_of_month_input(self) -> typing.Optional[typing.List[jsii.Number]]:
        return typing.cast(typing.Optional[typing.List[jsii.Number]], jsii.get(self, "daysOfMonthInput"))

    @builtins.property
    @jsii.member(jsii_name="hourInput")
    def hour_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "hourInput"))

    @builtins.property
    @jsii.member(jsii_name="minuteInput")
    def minute_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "minuteInput"))

    @builtins.property
    @jsii.member(jsii_name="snapshotsToKeepInput")
    def snapshots_to_keep_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "snapshotsToKeepInput"))

    @builtins.property
    @jsii.member(jsii_name="daysOfMonth")
    def days_of_month(self) -> typing.List[jsii.Number]:
        return typing.cast(typing.List[jsii.Number], jsii.get(self, "daysOfMonth"))

    @days_of_month.setter
    def days_of_month(self, value: typing.List[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5277390fe3f375ef68df8421260318cca1283f24b3f98d5ca98776d08ee8838a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "daysOfMonth", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="hour")
    def hour(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "hour"))

    @hour.setter
    def hour(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ebae2f42200608b30f32f97aa254a80a2edb3b3eb3c44acaaaf1090ea8ca6b3f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hour", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="minute")
    def minute(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "minute"))

    @minute.setter
    def minute(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__58e1075637184cfcacf4ce9d363b7d4b13aa3278adc9b58987479969def80d6e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minute", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="snapshotsToKeep")
    def snapshots_to_keep(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "snapshotsToKeep"))

    @snapshots_to_keep.setter
    def snapshots_to_keep(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d552b520bf2e20a5ff1c2a59fb4509cf483bccd4232810c8223077292b0208b1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "snapshotsToKeep", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[NetappSnapshotPolicyMonthlySchedule]:
        return typing.cast(typing.Optional[NetappSnapshotPolicyMonthlySchedule], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[NetappSnapshotPolicyMonthlySchedule],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__315ef4fbed372f972853af4c2f834aaf605eef83731734091f97d3507c04c45d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.netappSnapshotPolicy.NetappSnapshotPolicyTimeouts",
    jsii_struct_bases=[],
    name_mapping={
        "create": "create",
        "delete": "delete",
        "read": "read",
        "update": "update",
    },
)
class NetappSnapshotPolicyTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_snapshot_policy#create NetappSnapshotPolicy#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_snapshot_policy#delete NetappSnapshotPolicy#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_snapshot_policy#read NetappSnapshotPolicy#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_snapshot_policy#update NetappSnapshotPolicy#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f78fa1ee5ccd703ddb73d2df81081555e977784bb071069f2500bdacbbeb957a)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_snapshot_policy#create NetappSnapshotPolicy#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_snapshot_policy#delete NetappSnapshotPolicy#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def read(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_snapshot_policy#read NetappSnapshotPolicy#read}.'''
        result = self._values.get("read")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_snapshot_policy#update NetappSnapshotPolicy#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetappSnapshotPolicyTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NetappSnapshotPolicyTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.netappSnapshotPolicy.NetappSnapshotPolicyTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b2540acfc8a32681eb0830cf0f932af4d77b96dbe746b5ca33126181b5d9fa88)
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
            type_hints = typing.get_type_hints(_typecheckingstub__116956154ff74351ed8b8aa11352934651660899bf6c374e922f351b41e19b83)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f31a1ba599726d75b1eb0be6f4e7715aee6b7627ed1866a0a6a9adf8aba99d80)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="read")
    def read(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "read"))

    @read.setter
    def read(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8eb9e06f3607b01aaad8c818c00284a4a18681a80b4fbf7ca6b6c554a0e0909a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "read", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c88915b56edcfac8684b362509468e196d4de943cc2caf0aae941a421708326)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetappSnapshotPolicyTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetappSnapshotPolicyTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetappSnapshotPolicyTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__92065a99fcfe35aea30f9fe8c5ff37f4f0ead0219850da9bfaf2fb26afc06d04)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.netappSnapshotPolicy.NetappSnapshotPolicyWeeklySchedule",
    jsii_struct_bases=[],
    name_mapping={
        "days_of_week": "daysOfWeek",
        "hour": "hour",
        "minute": "minute",
        "snapshots_to_keep": "snapshotsToKeep",
    },
)
class NetappSnapshotPolicyWeeklySchedule:
    def __init__(
        self,
        *,
        days_of_week: typing.Sequence[builtins.str],
        hour: jsii.Number,
        minute: jsii.Number,
        snapshots_to_keep: jsii.Number,
    ) -> None:
        '''
        :param days_of_week: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_snapshot_policy#days_of_week NetappSnapshotPolicy#days_of_week}.
        :param hour: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_snapshot_policy#hour NetappSnapshotPolicy#hour}.
        :param minute: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_snapshot_policy#minute NetappSnapshotPolicy#minute}.
        :param snapshots_to_keep: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_snapshot_policy#snapshots_to_keep NetappSnapshotPolicy#snapshots_to_keep}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__86d566662f4a277aaf5dcfd96257c55bab92e4cb81531226f81b0a129de462e2)
            check_type(argname="argument days_of_week", value=days_of_week, expected_type=type_hints["days_of_week"])
            check_type(argname="argument hour", value=hour, expected_type=type_hints["hour"])
            check_type(argname="argument minute", value=minute, expected_type=type_hints["minute"])
            check_type(argname="argument snapshots_to_keep", value=snapshots_to_keep, expected_type=type_hints["snapshots_to_keep"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "days_of_week": days_of_week,
            "hour": hour,
            "minute": minute,
            "snapshots_to_keep": snapshots_to_keep,
        }

    @builtins.property
    def days_of_week(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_snapshot_policy#days_of_week NetappSnapshotPolicy#days_of_week}.'''
        result = self._values.get("days_of_week")
        assert result is not None, "Required property 'days_of_week' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def hour(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_snapshot_policy#hour NetappSnapshotPolicy#hour}.'''
        result = self._values.get("hour")
        assert result is not None, "Required property 'hour' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def minute(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_snapshot_policy#minute NetappSnapshotPolicy#minute}.'''
        result = self._values.get("minute")
        assert result is not None, "Required property 'minute' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def snapshots_to_keep(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_snapshot_policy#snapshots_to_keep NetappSnapshotPolicy#snapshots_to_keep}.'''
        result = self._values.get("snapshots_to_keep")
        assert result is not None, "Required property 'snapshots_to_keep' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetappSnapshotPolicyWeeklySchedule(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NetappSnapshotPolicyWeeklyScheduleOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.netappSnapshotPolicy.NetappSnapshotPolicyWeeklyScheduleOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3aff7399c77c7ab7361de54d8dc390338f7fc67a24d4f96e56abf5d899959aa8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="daysOfWeekInput")
    def days_of_week_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "daysOfWeekInput"))

    @builtins.property
    @jsii.member(jsii_name="hourInput")
    def hour_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "hourInput"))

    @builtins.property
    @jsii.member(jsii_name="minuteInput")
    def minute_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "minuteInput"))

    @builtins.property
    @jsii.member(jsii_name="snapshotsToKeepInput")
    def snapshots_to_keep_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "snapshotsToKeepInput"))

    @builtins.property
    @jsii.member(jsii_name="daysOfWeek")
    def days_of_week(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "daysOfWeek"))

    @days_of_week.setter
    def days_of_week(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__66069a7905d86579b02d4278ce05da516d3916eb75ce403524668515a68f3120)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "daysOfWeek", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="hour")
    def hour(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "hour"))

    @hour.setter
    def hour(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9841ac689a5639d1067d442c13e8937040c586e127676145b62ebe1ed4c31636)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hour", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="minute")
    def minute(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "minute"))

    @minute.setter
    def minute(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f984b49922e1edf06065e6c74fe0a25f30249a4edfd8c309d23a6890ae328ac0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minute", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="snapshotsToKeep")
    def snapshots_to_keep(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "snapshotsToKeep"))

    @snapshots_to_keep.setter
    def snapshots_to_keep(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b224b7c804d83bb7fd06bfdf7b90cc7e890bd6b7659c44daf6f73fe09064f26)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "snapshotsToKeep", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[NetappSnapshotPolicyWeeklySchedule]:
        return typing.cast(typing.Optional[NetappSnapshotPolicyWeeklySchedule], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[NetappSnapshotPolicyWeeklySchedule],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__37c6853e742a1431bb716e762910906b4cf476aff0500085075e89d52511d65b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "NetappSnapshotPolicy",
    "NetappSnapshotPolicyConfig",
    "NetappSnapshotPolicyDailySchedule",
    "NetappSnapshotPolicyDailyScheduleOutputReference",
    "NetappSnapshotPolicyHourlySchedule",
    "NetappSnapshotPolicyHourlyScheduleOutputReference",
    "NetappSnapshotPolicyMonthlySchedule",
    "NetappSnapshotPolicyMonthlyScheduleOutputReference",
    "NetappSnapshotPolicyTimeouts",
    "NetappSnapshotPolicyTimeoutsOutputReference",
    "NetappSnapshotPolicyWeeklySchedule",
    "NetappSnapshotPolicyWeeklyScheduleOutputReference",
]

publication.publish()

def _typecheckingstub__f00ad250f4197a6aced9f323cdabe7859b41b4d3de90ce3d26c0d3b42c253195(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    account_name: builtins.str,
    enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    location: builtins.str,
    name: builtins.str,
    resource_group_name: builtins.str,
    daily_schedule: typing.Optional[typing.Union[NetappSnapshotPolicyDailySchedule, typing.Dict[builtins.str, typing.Any]]] = None,
    hourly_schedule: typing.Optional[typing.Union[NetappSnapshotPolicyHourlySchedule, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    monthly_schedule: typing.Optional[typing.Union[NetappSnapshotPolicyMonthlySchedule, typing.Dict[builtins.str, typing.Any]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[NetappSnapshotPolicyTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    weekly_schedule: typing.Optional[typing.Union[NetappSnapshotPolicyWeeklySchedule, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__9c73309ced1abb33f63332a180ef6dc55364e6848288069f21656c60d4957b11(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a10af77e88c3df54a77ad287e1174dd59551430d22500b5a3e3f2b0755035d33(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf621192ec38fa24a53fe1b3147293d5e610d83e678c89b5b578d01f90ae995b(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18fd458356418752e2d2ebd1d54c6302c69a34f6beb3d6fce3f92ba2e6ff17e7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3eb7aa0d7333ac766636e4f03504a57bc6673a52028408ddeb5946de1c821b68(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__390563a5fc3e52d6b553221556106ed8a5f4d961ecb64af7c9dce9b01c15b9b2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eec06454c5cc8d8e032b060aa595565c0d38b498c49d3ebd1eaec67be9a390d4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fdf204326c6d585d222d55f6679c289b2f058036b9c68de41944368658df5df8(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66a728b0d85d8666818fe218d35001a41f3eb0e1e1bdf5a199f38c56f099edbd(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    account_name: builtins.str,
    enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    location: builtins.str,
    name: builtins.str,
    resource_group_name: builtins.str,
    daily_schedule: typing.Optional[typing.Union[NetappSnapshotPolicyDailySchedule, typing.Dict[builtins.str, typing.Any]]] = None,
    hourly_schedule: typing.Optional[typing.Union[NetappSnapshotPolicyHourlySchedule, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    monthly_schedule: typing.Optional[typing.Union[NetappSnapshotPolicyMonthlySchedule, typing.Dict[builtins.str, typing.Any]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[NetappSnapshotPolicyTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    weekly_schedule: typing.Optional[typing.Union[NetappSnapshotPolicyWeeklySchedule, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a69dd1c08d0ecfdc0a32ea567f1f9f51c19cdd2efb2373a180684d983b6fc2e8(
    *,
    hour: jsii.Number,
    minute: jsii.Number,
    snapshots_to_keep: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6295798d3c2d30edd00c704297cd9c5e660264101ca19789719fd29c98994e92(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44280b4fad611e74a3b583cc91df7cd2098c59a1b81bb102646d032a16528d56(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f8cece723b5fcdc3377caf22100e5b5653574d9739e827a6aa00f9555016cfe3(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64973127dac5a139c385a6460b9e1addac00e23a4d5d257d34b88f6814351996(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb874b3cc657bd70e687440e9f6f751b04c810cb0eb9d60c2bc2e158c70beefe(
    value: typing.Optional[NetappSnapshotPolicyDailySchedule],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3511b55b4d934adf7cb8cbf9fc18601034f6e586754f0502dc8e6c2419f8a74(
    *,
    minute: jsii.Number,
    snapshots_to_keep: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8705aa9dfaec877fbb8e3908cda74fe3d0ec016f641e48a2ca57bbc637bfc61(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61c982b7b2deff062c98365547b7fd670a3ef2adee57b0f479469174a3a59cc0(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74ef15df45604bc19155e6efa68eba23444cf1c82ee882bd50bc0952682a1d78(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b2d34a10b8676242f3a0565aee53d61a182e23d5d89c43b6c147f8cc92a2f303(
    value: typing.Optional[NetappSnapshotPolicyHourlySchedule],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d82c28f26e4c4a23019fb0039ff3558b79ef50ac28ffd55fe5e924410bc3cd7(
    *,
    days_of_month: typing.Sequence[jsii.Number],
    hour: jsii.Number,
    minute: jsii.Number,
    snapshots_to_keep: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__520005245147cf8c6f67a69086b440d6f9d8becda0b7eb1e14f60c8c1c0538e8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5277390fe3f375ef68df8421260318cca1283f24b3f98d5ca98776d08ee8838a(
    value: typing.List[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ebae2f42200608b30f32f97aa254a80a2edb3b3eb3c44acaaaf1090ea8ca6b3f(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__58e1075637184cfcacf4ce9d363b7d4b13aa3278adc9b58987479969def80d6e(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d552b520bf2e20a5ff1c2a59fb4509cf483bccd4232810c8223077292b0208b1(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__315ef4fbed372f972853af4c2f834aaf605eef83731734091f97d3507c04c45d(
    value: typing.Optional[NetappSnapshotPolicyMonthlySchedule],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f78fa1ee5ccd703ddb73d2df81081555e977784bb071069f2500bdacbbeb957a(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    read: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b2540acfc8a32681eb0830cf0f932af4d77b96dbe746b5ca33126181b5d9fa88(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__116956154ff74351ed8b8aa11352934651660899bf6c374e922f351b41e19b83(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f31a1ba599726d75b1eb0be6f4e7715aee6b7627ed1866a0a6a9adf8aba99d80(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8eb9e06f3607b01aaad8c818c00284a4a18681a80b4fbf7ca6b6c554a0e0909a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c88915b56edcfac8684b362509468e196d4de943cc2caf0aae941a421708326(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92065a99fcfe35aea30f9fe8c5ff37f4f0ead0219850da9bfaf2fb26afc06d04(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetappSnapshotPolicyTimeouts]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86d566662f4a277aaf5dcfd96257c55bab92e4cb81531226f81b0a129de462e2(
    *,
    days_of_week: typing.Sequence[builtins.str],
    hour: jsii.Number,
    minute: jsii.Number,
    snapshots_to_keep: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3aff7399c77c7ab7361de54d8dc390338f7fc67a24d4f96e56abf5d899959aa8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66069a7905d86579b02d4278ce05da516d3916eb75ce403524668515a68f3120(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9841ac689a5639d1067d442c13e8937040c586e127676145b62ebe1ed4c31636(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f984b49922e1edf06065e6c74fe0a25f30249a4edfd8c309d23a6890ae328ac0(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b224b7c804d83bb7fd06bfdf7b90cc7e890bd6b7659c44daf6f73fe09064f26(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37c6853e742a1431bb716e762910906b4cf476aff0500085075e89d52511d65b(
    value: typing.Optional[NetappSnapshotPolicyWeeklySchedule],
) -> None:
    """Type checking stubs"""
    pass
