r'''
# `azurerm_dev_test_schedule`

Refer to the Terraform Registry for docs: [`azurerm_dev_test_schedule`](https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/dev_test_schedule).
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


class DevTestSchedule(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.devTestSchedule.DevTestSchedule",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/dev_test_schedule azurerm_dev_test_schedule}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        lab_name: builtins.str,
        location: builtins.str,
        name: builtins.str,
        notification_settings: typing.Union["DevTestScheduleNotificationSettings", typing.Dict[builtins.str, typing.Any]],
        resource_group_name: builtins.str,
        task_type: builtins.str,
        time_zone_id: builtins.str,
        daily_recurrence: typing.Optional[typing.Union["DevTestScheduleDailyRecurrence", typing.Dict[builtins.str, typing.Any]]] = None,
        hourly_recurrence: typing.Optional[typing.Union["DevTestScheduleHourlyRecurrence", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        status: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["DevTestScheduleTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        weekly_recurrence: typing.Optional[typing.Union["DevTestScheduleWeeklyRecurrence", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/dev_test_schedule azurerm_dev_test_schedule} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param lab_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/dev_test_schedule#lab_name DevTestSchedule#lab_name}.
        :param location: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/dev_test_schedule#location DevTestSchedule#location}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/dev_test_schedule#name DevTestSchedule#name}.
        :param notification_settings: notification_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/dev_test_schedule#notification_settings DevTestSchedule#notification_settings}
        :param resource_group_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/dev_test_schedule#resource_group_name DevTestSchedule#resource_group_name}.
        :param task_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/dev_test_schedule#task_type DevTestSchedule#task_type}.
        :param time_zone_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/dev_test_schedule#time_zone_id DevTestSchedule#time_zone_id}.
        :param daily_recurrence: daily_recurrence block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/dev_test_schedule#daily_recurrence DevTestSchedule#daily_recurrence}
        :param hourly_recurrence: hourly_recurrence block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/dev_test_schedule#hourly_recurrence DevTestSchedule#hourly_recurrence}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/dev_test_schedule#id DevTestSchedule#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param status: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/dev_test_schedule#status DevTestSchedule#status}.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/dev_test_schedule#tags DevTestSchedule#tags}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/dev_test_schedule#timeouts DevTestSchedule#timeouts}
        :param weekly_recurrence: weekly_recurrence block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/dev_test_schedule#weekly_recurrence DevTestSchedule#weekly_recurrence}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__28dc7d0f76bb17ab4d8ce059397707c24a0c905f64e05ea71ebcab07a6ee18c4)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = DevTestScheduleConfig(
            lab_name=lab_name,
            location=location,
            name=name,
            notification_settings=notification_settings,
            resource_group_name=resource_group_name,
            task_type=task_type,
            time_zone_id=time_zone_id,
            daily_recurrence=daily_recurrence,
            hourly_recurrence=hourly_recurrence,
            id=id,
            status=status,
            tags=tags,
            timeouts=timeouts,
            weekly_recurrence=weekly_recurrence,
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
        '''Generates CDKTF code for importing a DevTestSchedule resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the DevTestSchedule to import.
        :param import_from_id: The id of the existing DevTestSchedule that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/dev_test_schedule#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the DevTestSchedule to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__105fe7dab070ea94e0588b64aaf60e1a96947c43ff9dfa08381ab2cfaad30def)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putDailyRecurrence")
    def put_daily_recurrence(self, *, time: builtins.str) -> None:
        '''
        :param time: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/dev_test_schedule#time DevTestSchedule#time}.
        '''
        value = DevTestScheduleDailyRecurrence(time=time)

        return typing.cast(None, jsii.invoke(self, "putDailyRecurrence", [value]))

    @jsii.member(jsii_name="putHourlyRecurrence")
    def put_hourly_recurrence(self, *, minute: jsii.Number) -> None:
        '''
        :param minute: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/dev_test_schedule#minute DevTestSchedule#minute}.
        '''
        value = DevTestScheduleHourlyRecurrence(minute=minute)

        return typing.cast(None, jsii.invoke(self, "putHourlyRecurrence", [value]))

    @jsii.member(jsii_name="putNotificationSettings")
    def put_notification_settings(
        self,
        *,
        status: typing.Optional[builtins.str] = None,
        time_in_minutes: typing.Optional[jsii.Number] = None,
        webhook_url: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param status: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/dev_test_schedule#status DevTestSchedule#status}.
        :param time_in_minutes: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/dev_test_schedule#time_in_minutes DevTestSchedule#time_in_minutes}.
        :param webhook_url: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/dev_test_schedule#webhook_url DevTestSchedule#webhook_url}.
        '''
        value = DevTestScheduleNotificationSettings(
            status=status, time_in_minutes=time_in_minutes, webhook_url=webhook_url
        )

        return typing.cast(None, jsii.invoke(self, "putNotificationSettings", [value]))

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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/dev_test_schedule#create DevTestSchedule#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/dev_test_schedule#delete DevTestSchedule#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/dev_test_schedule#read DevTestSchedule#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/dev_test_schedule#update DevTestSchedule#update}.
        '''
        value = DevTestScheduleTimeouts(
            create=create, delete=delete, read=read, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="putWeeklyRecurrence")
    def put_weekly_recurrence(
        self,
        *,
        time: builtins.str,
        week_days: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param time: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/dev_test_schedule#time DevTestSchedule#time}.
        :param week_days: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/dev_test_schedule#week_days DevTestSchedule#week_days}.
        '''
        value = DevTestScheduleWeeklyRecurrence(time=time, week_days=week_days)

        return typing.cast(None, jsii.invoke(self, "putWeeklyRecurrence", [value]))

    @jsii.member(jsii_name="resetDailyRecurrence")
    def reset_daily_recurrence(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDailyRecurrence", []))

    @jsii.member(jsii_name="resetHourlyRecurrence")
    def reset_hourly_recurrence(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHourlyRecurrence", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetStatus")
    def reset_status(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStatus", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

    @jsii.member(jsii_name="resetWeeklyRecurrence")
    def reset_weekly_recurrence(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWeeklyRecurrence", []))

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
    @jsii.member(jsii_name="dailyRecurrence")
    def daily_recurrence(self) -> "DevTestScheduleDailyRecurrenceOutputReference":
        return typing.cast("DevTestScheduleDailyRecurrenceOutputReference", jsii.get(self, "dailyRecurrence"))

    @builtins.property
    @jsii.member(jsii_name="hourlyRecurrence")
    def hourly_recurrence(self) -> "DevTestScheduleHourlyRecurrenceOutputReference":
        return typing.cast("DevTestScheduleHourlyRecurrenceOutputReference", jsii.get(self, "hourlyRecurrence"))

    @builtins.property
    @jsii.member(jsii_name="notificationSettings")
    def notification_settings(
        self,
    ) -> "DevTestScheduleNotificationSettingsOutputReference":
        return typing.cast("DevTestScheduleNotificationSettingsOutputReference", jsii.get(self, "notificationSettings"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "DevTestScheduleTimeoutsOutputReference":
        return typing.cast("DevTestScheduleTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="weeklyRecurrence")
    def weekly_recurrence(self) -> "DevTestScheduleWeeklyRecurrenceOutputReference":
        return typing.cast("DevTestScheduleWeeklyRecurrenceOutputReference", jsii.get(self, "weeklyRecurrence"))

    @builtins.property
    @jsii.member(jsii_name="dailyRecurrenceInput")
    def daily_recurrence_input(
        self,
    ) -> typing.Optional["DevTestScheduleDailyRecurrence"]:
        return typing.cast(typing.Optional["DevTestScheduleDailyRecurrence"], jsii.get(self, "dailyRecurrenceInput"))

    @builtins.property
    @jsii.member(jsii_name="hourlyRecurrenceInput")
    def hourly_recurrence_input(
        self,
    ) -> typing.Optional["DevTestScheduleHourlyRecurrence"]:
        return typing.cast(typing.Optional["DevTestScheduleHourlyRecurrence"], jsii.get(self, "hourlyRecurrenceInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="labNameInput")
    def lab_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "labNameInput"))

    @builtins.property
    @jsii.member(jsii_name="locationInput")
    def location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "locationInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="notificationSettingsInput")
    def notification_settings_input(
        self,
    ) -> typing.Optional["DevTestScheduleNotificationSettings"]:
        return typing.cast(typing.Optional["DevTestScheduleNotificationSettings"], jsii.get(self, "notificationSettingsInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceGroupNameInput")
    def resource_group_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "resourceGroupNameInput"))

    @builtins.property
    @jsii.member(jsii_name="statusInput")
    def status_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "statusInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsInput")
    def tags_input(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "tagsInput"))

    @builtins.property
    @jsii.member(jsii_name="taskTypeInput")
    def task_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "taskTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "DevTestScheduleTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "DevTestScheduleTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="timeZoneIdInput")
    def time_zone_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "timeZoneIdInput"))

    @builtins.property
    @jsii.member(jsii_name="weeklyRecurrenceInput")
    def weekly_recurrence_input(
        self,
    ) -> typing.Optional["DevTestScheduleWeeklyRecurrence"]:
        return typing.cast(typing.Optional["DevTestScheduleWeeklyRecurrence"], jsii.get(self, "weeklyRecurrenceInput"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7d2e6be2612e77fff5bc36d5b59b33ac2e7bac0cfd7d2e86161ddb4b0c5054ba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="labName")
    def lab_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "labName"))

    @lab_name.setter
    def lab_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a060a61e1e1eff104ca7c2fe62621c5479bc3489ff8a615b3e5e22cdad456af)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd5f2734a9b23fc4d65d2773c5778b682d388adf1334382f3d1be0cf9f4c961a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4cbb1c96f43a9b939883977bed89dc692bbd5bcf0f58862509fdac7bc2b08ab5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resourceGroupName")
    def resource_group_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourceGroupName"))

    @resource_group_name.setter
    def resource_group_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5223a7eb31e92409b15e15273d08304eed08f510b39be98af0ec626d30531faa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceGroupName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "status"))

    @status.setter
    def status(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__13433504108dd18008b7056cb117d53465d750e9f124df91a8d234edfe40a12e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "status", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__058b12f6c9ba61c1c861a43fee6ac737477bee45a6c5e9f4c30a7d34f25b9794)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="taskType")
    def task_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "taskType"))

    @task_type.setter
    def task_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0994be7d8431e37e376c2cd334076ccf9117fd0e92d4376aa465ba804578fb78)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "taskType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="timeZoneId")
    def time_zone_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "timeZoneId"))

    @time_zone_id.setter
    def time_zone_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e79ed60865ff64008fa5e2e2832ff265ae7455847f381ffc76a0c9a7265dca9a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timeZoneId", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.devTestSchedule.DevTestScheduleConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "lab_name": "labName",
        "location": "location",
        "name": "name",
        "notification_settings": "notificationSettings",
        "resource_group_name": "resourceGroupName",
        "task_type": "taskType",
        "time_zone_id": "timeZoneId",
        "daily_recurrence": "dailyRecurrence",
        "hourly_recurrence": "hourlyRecurrence",
        "id": "id",
        "status": "status",
        "tags": "tags",
        "timeouts": "timeouts",
        "weekly_recurrence": "weeklyRecurrence",
    },
)
class DevTestScheduleConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        lab_name: builtins.str,
        location: builtins.str,
        name: builtins.str,
        notification_settings: typing.Union["DevTestScheduleNotificationSettings", typing.Dict[builtins.str, typing.Any]],
        resource_group_name: builtins.str,
        task_type: builtins.str,
        time_zone_id: builtins.str,
        daily_recurrence: typing.Optional[typing.Union["DevTestScheduleDailyRecurrence", typing.Dict[builtins.str, typing.Any]]] = None,
        hourly_recurrence: typing.Optional[typing.Union["DevTestScheduleHourlyRecurrence", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        status: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["DevTestScheduleTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        weekly_recurrence: typing.Optional[typing.Union["DevTestScheduleWeeklyRecurrence", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param lab_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/dev_test_schedule#lab_name DevTestSchedule#lab_name}.
        :param location: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/dev_test_schedule#location DevTestSchedule#location}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/dev_test_schedule#name DevTestSchedule#name}.
        :param notification_settings: notification_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/dev_test_schedule#notification_settings DevTestSchedule#notification_settings}
        :param resource_group_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/dev_test_schedule#resource_group_name DevTestSchedule#resource_group_name}.
        :param task_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/dev_test_schedule#task_type DevTestSchedule#task_type}.
        :param time_zone_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/dev_test_schedule#time_zone_id DevTestSchedule#time_zone_id}.
        :param daily_recurrence: daily_recurrence block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/dev_test_schedule#daily_recurrence DevTestSchedule#daily_recurrence}
        :param hourly_recurrence: hourly_recurrence block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/dev_test_schedule#hourly_recurrence DevTestSchedule#hourly_recurrence}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/dev_test_schedule#id DevTestSchedule#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param status: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/dev_test_schedule#status DevTestSchedule#status}.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/dev_test_schedule#tags DevTestSchedule#tags}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/dev_test_schedule#timeouts DevTestSchedule#timeouts}
        :param weekly_recurrence: weekly_recurrence block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/dev_test_schedule#weekly_recurrence DevTestSchedule#weekly_recurrence}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(notification_settings, dict):
            notification_settings = DevTestScheduleNotificationSettings(**notification_settings)
        if isinstance(daily_recurrence, dict):
            daily_recurrence = DevTestScheduleDailyRecurrence(**daily_recurrence)
        if isinstance(hourly_recurrence, dict):
            hourly_recurrence = DevTestScheduleHourlyRecurrence(**hourly_recurrence)
        if isinstance(timeouts, dict):
            timeouts = DevTestScheduleTimeouts(**timeouts)
        if isinstance(weekly_recurrence, dict):
            weekly_recurrence = DevTestScheduleWeeklyRecurrence(**weekly_recurrence)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9604002ad2a4d4b0b1203dbf11b493ad3edbb736cb1db88837a84248c435ce70)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument lab_name", value=lab_name, expected_type=type_hints["lab_name"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument notification_settings", value=notification_settings, expected_type=type_hints["notification_settings"])
            check_type(argname="argument resource_group_name", value=resource_group_name, expected_type=type_hints["resource_group_name"])
            check_type(argname="argument task_type", value=task_type, expected_type=type_hints["task_type"])
            check_type(argname="argument time_zone_id", value=time_zone_id, expected_type=type_hints["time_zone_id"])
            check_type(argname="argument daily_recurrence", value=daily_recurrence, expected_type=type_hints["daily_recurrence"])
            check_type(argname="argument hourly_recurrence", value=hourly_recurrence, expected_type=type_hints["hourly_recurrence"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument status", value=status, expected_type=type_hints["status"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
            check_type(argname="argument weekly_recurrence", value=weekly_recurrence, expected_type=type_hints["weekly_recurrence"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "lab_name": lab_name,
            "location": location,
            "name": name,
            "notification_settings": notification_settings,
            "resource_group_name": resource_group_name,
            "task_type": task_type,
            "time_zone_id": time_zone_id,
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
        if daily_recurrence is not None:
            self._values["daily_recurrence"] = daily_recurrence
        if hourly_recurrence is not None:
            self._values["hourly_recurrence"] = hourly_recurrence
        if id is not None:
            self._values["id"] = id
        if status is not None:
            self._values["status"] = status
        if tags is not None:
            self._values["tags"] = tags
        if timeouts is not None:
            self._values["timeouts"] = timeouts
        if weekly_recurrence is not None:
            self._values["weekly_recurrence"] = weekly_recurrence

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
    def lab_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/dev_test_schedule#lab_name DevTestSchedule#lab_name}.'''
        result = self._values.get("lab_name")
        assert result is not None, "Required property 'lab_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def location(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/dev_test_schedule#location DevTestSchedule#location}.'''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/dev_test_schedule#name DevTestSchedule#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def notification_settings(self) -> "DevTestScheduleNotificationSettings":
        '''notification_settings block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/dev_test_schedule#notification_settings DevTestSchedule#notification_settings}
        '''
        result = self._values.get("notification_settings")
        assert result is not None, "Required property 'notification_settings' is missing"
        return typing.cast("DevTestScheduleNotificationSettings", result)

    @builtins.property
    def resource_group_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/dev_test_schedule#resource_group_name DevTestSchedule#resource_group_name}.'''
        result = self._values.get("resource_group_name")
        assert result is not None, "Required property 'resource_group_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def task_type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/dev_test_schedule#task_type DevTestSchedule#task_type}.'''
        result = self._values.get("task_type")
        assert result is not None, "Required property 'task_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def time_zone_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/dev_test_schedule#time_zone_id DevTestSchedule#time_zone_id}.'''
        result = self._values.get("time_zone_id")
        assert result is not None, "Required property 'time_zone_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def daily_recurrence(self) -> typing.Optional["DevTestScheduleDailyRecurrence"]:
        '''daily_recurrence block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/dev_test_schedule#daily_recurrence DevTestSchedule#daily_recurrence}
        '''
        result = self._values.get("daily_recurrence")
        return typing.cast(typing.Optional["DevTestScheduleDailyRecurrence"], result)

    @builtins.property
    def hourly_recurrence(self) -> typing.Optional["DevTestScheduleHourlyRecurrence"]:
        '''hourly_recurrence block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/dev_test_schedule#hourly_recurrence DevTestSchedule#hourly_recurrence}
        '''
        result = self._values.get("hourly_recurrence")
        return typing.cast(typing.Optional["DevTestScheduleHourlyRecurrence"], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/dev_test_schedule#id DevTestSchedule#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def status(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/dev_test_schedule#status DevTestSchedule#status}.'''
        result = self._values.get("status")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/dev_test_schedule#tags DevTestSchedule#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["DevTestScheduleTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/dev_test_schedule#timeouts DevTestSchedule#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["DevTestScheduleTimeouts"], result)

    @builtins.property
    def weekly_recurrence(self) -> typing.Optional["DevTestScheduleWeeklyRecurrence"]:
        '''weekly_recurrence block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/dev_test_schedule#weekly_recurrence DevTestSchedule#weekly_recurrence}
        '''
        result = self._values.get("weekly_recurrence")
        return typing.cast(typing.Optional["DevTestScheduleWeeklyRecurrence"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DevTestScheduleConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.devTestSchedule.DevTestScheduleDailyRecurrence",
    jsii_struct_bases=[],
    name_mapping={"time": "time"},
)
class DevTestScheduleDailyRecurrence:
    def __init__(self, *, time: builtins.str) -> None:
        '''
        :param time: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/dev_test_schedule#time DevTestSchedule#time}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b6cc8c0424bd7a950bc4857403e1f2281d8cb9e63e0a89f3a39bbe2563b1ed49)
            check_type(argname="argument time", value=time, expected_type=type_hints["time"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "time": time,
        }

    @builtins.property
    def time(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/dev_test_schedule#time DevTestSchedule#time}.'''
        result = self._values.get("time")
        assert result is not None, "Required property 'time' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DevTestScheduleDailyRecurrence(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DevTestScheduleDailyRecurrenceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.devTestSchedule.DevTestScheduleDailyRecurrenceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__001928fa3959131480be9d9d88af7cf0ba5a89279f6290c340d8c2b1813ebc19)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="timeInput")
    def time_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "timeInput"))

    @builtins.property
    @jsii.member(jsii_name="time")
    def time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "time"))

    @time.setter
    def time(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__663b36bf8cf59a9b10e110c454844c42384594cd49c0f6e806217d28f72a4a6b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "time", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[DevTestScheduleDailyRecurrence]:
        return typing.cast(typing.Optional[DevTestScheduleDailyRecurrence], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DevTestScheduleDailyRecurrence],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a2c4f9cf98c2dc45ff01c3143d690d4c35a42ca1a7aec14bcdd3ebdf3d4e64c5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.devTestSchedule.DevTestScheduleHourlyRecurrence",
    jsii_struct_bases=[],
    name_mapping={"minute": "minute"},
)
class DevTestScheduleHourlyRecurrence:
    def __init__(self, *, minute: jsii.Number) -> None:
        '''
        :param minute: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/dev_test_schedule#minute DevTestSchedule#minute}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a2a6f75bca231b69416ad6662d902b05f8d55f019febdd709935312d223e50a4)
            check_type(argname="argument minute", value=minute, expected_type=type_hints["minute"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "minute": minute,
        }

    @builtins.property
    def minute(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/dev_test_schedule#minute DevTestSchedule#minute}.'''
        result = self._values.get("minute")
        assert result is not None, "Required property 'minute' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DevTestScheduleHourlyRecurrence(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DevTestScheduleHourlyRecurrenceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.devTestSchedule.DevTestScheduleHourlyRecurrenceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fb6d558a0c5b6d89f0d369e40084e6bfb0685f39ddcd2869c2119fd1dc8bddfa)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="minuteInput")
    def minute_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "minuteInput"))

    @builtins.property
    @jsii.member(jsii_name="minute")
    def minute(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "minute"))

    @minute.setter
    def minute(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__78693656949a7c666501c94c03078c4a83ac1441c99357256384415a4c0ac679)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minute", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[DevTestScheduleHourlyRecurrence]:
        return typing.cast(typing.Optional[DevTestScheduleHourlyRecurrence], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DevTestScheduleHourlyRecurrence],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__49077ae5618e45831c4f653dad62773f1d29dc3f1c33147e6dd0aac4e3fb8435)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.devTestSchedule.DevTestScheduleNotificationSettings",
    jsii_struct_bases=[],
    name_mapping={
        "status": "status",
        "time_in_minutes": "timeInMinutes",
        "webhook_url": "webhookUrl",
    },
)
class DevTestScheduleNotificationSettings:
    def __init__(
        self,
        *,
        status: typing.Optional[builtins.str] = None,
        time_in_minutes: typing.Optional[jsii.Number] = None,
        webhook_url: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param status: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/dev_test_schedule#status DevTestSchedule#status}.
        :param time_in_minutes: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/dev_test_schedule#time_in_minutes DevTestSchedule#time_in_minutes}.
        :param webhook_url: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/dev_test_schedule#webhook_url DevTestSchedule#webhook_url}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c245ca5694a1b0c74f9a27e0ad28ec269eaaad444f12b18062562e9a0fcb1f99)
            check_type(argname="argument status", value=status, expected_type=type_hints["status"])
            check_type(argname="argument time_in_minutes", value=time_in_minutes, expected_type=type_hints["time_in_minutes"])
            check_type(argname="argument webhook_url", value=webhook_url, expected_type=type_hints["webhook_url"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if status is not None:
            self._values["status"] = status
        if time_in_minutes is not None:
            self._values["time_in_minutes"] = time_in_minutes
        if webhook_url is not None:
            self._values["webhook_url"] = webhook_url

    @builtins.property
    def status(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/dev_test_schedule#status DevTestSchedule#status}.'''
        result = self._values.get("status")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def time_in_minutes(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/dev_test_schedule#time_in_minutes DevTestSchedule#time_in_minutes}.'''
        result = self._values.get("time_in_minutes")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def webhook_url(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/dev_test_schedule#webhook_url DevTestSchedule#webhook_url}.'''
        result = self._values.get("webhook_url")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DevTestScheduleNotificationSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DevTestScheduleNotificationSettingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.devTestSchedule.DevTestScheduleNotificationSettingsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b7b6721e65dba94aa171b04cd66031e1d939437efcf43987c94afd824872097a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetStatus")
    def reset_status(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStatus", []))

    @jsii.member(jsii_name="resetTimeInMinutes")
    def reset_time_in_minutes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeInMinutes", []))

    @jsii.member(jsii_name="resetWebhookUrl")
    def reset_webhook_url(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWebhookUrl", []))

    @builtins.property
    @jsii.member(jsii_name="statusInput")
    def status_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "statusInput"))

    @builtins.property
    @jsii.member(jsii_name="timeInMinutesInput")
    def time_in_minutes_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "timeInMinutesInput"))

    @builtins.property
    @jsii.member(jsii_name="webhookUrlInput")
    def webhook_url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "webhookUrlInput"))

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "status"))

    @status.setter
    def status(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__043fc82ef9275663e679d913d99efc19f1c8dd42b1ebffc1b2f9db9561d4e2a1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "status", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="timeInMinutes")
    def time_in_minutes(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "timeInMinutes"))

    @time_in_minutes.setter
    def time_in_minutes(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ae2d15e7dba009e187a81bbd3c736566608dabf16c7392522fdc900e38ed3392)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timeInMinutes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="webhookUrl")
    def webhook_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "webhookUrl"))

    @webhook_url.setter
    def webhook_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bc5d86232d6d1b101f139d594f8b691d8c34c9dc7ba7aafc4fb3da4ba47180e0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "webhookUrl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[DevTestScheduleNotificationSettings]:
        return typing.cast(typing.Optional[DevTestScheduleNotificationSettings], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DevTestScheduleNotificationSettings],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e4662d85bc23cd845543f99c1491df67a70b20d653b5ee9460a9129215626c0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.devTestSchedule.DevTestScheduleTimeouts",
    jsii_struct_bases=[],
    name_mapping={
        "create": "create",
        "delete": "delete",
        "read": "read",
        "update": "update",
    },
)
class DevTestScheduleTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/dev_test_schedule#create DevTestSchedule#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/dev_test_schedule#delete DevTestSchedule#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/dev_test_schedule#read DevTestSchedule#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/dev_test_schedule#update DevTestSchedule#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__55890127b64b8c4f8a6dd33a1c83e6df9621e8cd665b3df92abb234328e3514a)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/dev_test_schedule#create DevTestSchedule#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/dev_test_schedule#delete DevTestSchedule#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def read(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/dev_test_schedule#read DevTestSchedule#read}.'''
        result = self._values.get("read")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/dev_test_schedule#update DevTestSchedule#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DevTestScheduleTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DevTestScheduleTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.devTestSchedule.DevTestScheduleTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2f8bd30c2a88252d15449f40ba2188f8b3f91c4517128dbbbb7adb9efeed11e1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__30e41f3a33bfecec5299f1d701382c83838cf8115659d3d7e90e7f799254a772)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e0caa1bcb2a72e0bde22ca58eb15ce084cb01ca6127caf8fea627abcfdd8e650)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="read")
    def read(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "read"))

    @read.setter
    def read(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4193edeef3fb6adc358f1d3c10b428c7f753c3d21c4783274d605d60af554b0d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "read", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__be9456ef1cde6f13d4ce85882d606d896bebb2ec5267dc171712f007fbb056a2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DevTestScheduleTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DevTestScheduleTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DevTestScheduleTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f4d8f5b44327374183ff03176e00bbd6eadf7941e5a0fcd91e92d4164a9f6abc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.devTestSchedule.DevTestScheduleWeeklyRecurrence",
    jsii_struct_bases=[],
    name_mapping={"time": "time", "week_days": "weekDays"},
)
class DevTestScheduleWeeklyRecurrence:
    def __init__(
        self,
        *,
        time: builtins.str,
        week_days: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param time: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/dev_test_schedule#time DevTestSchedule#time}.
        :param week_days: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/dev_test_schedule#week_days DevTestSchedule#week_days}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9477c2e0193d2967bd62e8d5adb14952ba7585a8014370b2c178f138658e3fe3)
            check_type(argname="argument time", value=time, expected_type=type_hints["time"])
            check_type(argname="argument week_days", value=week_days, expected_type=type_hints["week_days"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "time": time,
        }
        if week_days is not None:
            self._values["week_days"] = week_days

    @builtins.property
    def time(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/dev_test_schedule#time DevTestSchedule#time}.'''
        result = self._values.get("time")
        assert result is not None, "Required property 'time' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def week_days(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/dev_test_schedule#week_days DevTestSchedule#week_days}.'''
        result = self._values.get("week_days")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DevTestScheduleWeeklyRecurrence(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DevTestScheduleWeeklyRecurrenceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.devTestSchedule.DevTestScheduleWeeklyRecurrenceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__66761efeb0e40eb54be0f94e84386b01510f774c1eb298640460dab50872aa2d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetWeekDays")
    def reset_week_days(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWeekDays", []))

    @builtins.property
    @jsii.member(jsii_name="timeInput")
    def time_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "timeInput"))

    @builtins.property
    @jsii.member(jsii_name="weekDaysInput")
    def week_days_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "weekDaysInput"))

    @builtins.property
    @jsii.member(jsii_name="time")
    def time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "time"))

    @time.setter
    def time(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d5bce78b66139847cb3ee63eabd134ca4c27969814d52008bdc48643bde29cb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "time", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="weekDays")
    def week_days(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "weekDays"))

    @week_days.setter
    def week_days(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__52bb1675213987a5234f7bc9952f93e70e466817875570796d2e326455ff08e9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "weekDays", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[DevTestScheduleWeeklyRecurrence]:
        return typing.cast(typing.Optional[DevTestScheduleWeeklyRecurrence], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DevTestScheduleWeeklyRecurrence],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__524eb35c71fcffa0ce9aa7a15cb0c4dc9d91b95adf709585f9eb6936bc9baae6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "DevTestSchedule",
    "DevTestScheduleConfig",
    "DevTestScheduleDailyRecurrence",
    "DevTestScheduleDailyRecurrenceOutputReference",
    "DevTestScheduleHourlyRecurrence",
    "DevTestScheduleHourlyRecurrenceOutputReference",
    "DevTestScheduleNotificationSettings",
    "DevTestScheduleNotificationSettingsOutputReference",
    "DevTestScheduleTimeouts",
    "DevTestScheduleTimeoutsOutputReference",
    "DevTestScheduleWeeklyRecurrence",
    "DevTestScheduleWeeklyRecurrenceOutputReference",
]

publication.publish()

def _typecheckingstub__28dc7d0f76bb17ab4d8ce059397707c24a0c905f64e05ea71ebcab07a6ee18c4(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    lab_name: builtins.str,
    location: builtins.str,
    name: builtins.str,
    notification_settings: typing.Union[DevTestScheduleNotificationSettings, typing.Dict[builtins.str, typing.Any]],
    resource_group_name: builtins.str,
    task_type: builtins.str,
    time_zone_id: builtins.str,
    daily_recurrence: typing.Optional[typing.Union[DevTestScheduleDailyRecurrence, typing.Dict[builtins.str, typing.Any]]] = None,
    hourly_recurrence: typing.Optional[typing.Union[DevTestScheduleHourlyRecurrence, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    status: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[DevTestScheduleTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    weekly_recurrence: typing.Optional[typing.Union[DevTestScheduleWeeklyRecurrence, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__105fe7dab070ea94e0588b64aaf60e1a96947c43ff9dfa08381ab2cfaad30def(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d2e6be2612e77fff5bc36d5b59b33ac2e7bac0cfd7d2e86161ddb4b0c5054ba(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a060a61e1e1eff104ca7c2fe62621c5479bc3489ff8a615b3e5e22cdad456af(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd5f2734a9b23fc4d65d2773c5778b682d388adf1334382f3d1be0cf9f4c961a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4cbb1c96f43a9b939883977bed89dc692bbd5bcf0f58862509fdac7bc2b08ab5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5223a7eb31e92409b15e15273d08304eed08f510b39be98af0ec626d30531faa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13433504108dd18008b7056cb117d53465d750e9f124df91a8d234edfe40a12e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__058b12f6c9ba61c1c861a43fee6ac737477bee45a6c5e9f4c30a7d34f25b9794(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0994be7d8431e37e376c2cd334076ccf9117fd0e92d4376aa465ba804578fb78(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e79ed60865ff64008fa5e2e2832ff265ae7455847f381ffc76a0c9a7265dca9a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9604002ad2a4d4b0b1203dbf11b493ad3edbb736cb1db88837a84248c435ce70(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    lab_name: builtins.str,
    location: builtins.str,
    name: builtins.str,
    notification_settings: typing.Union[DevTestScheduleNotificationSettings, typing.Dict[builtins.str, typing.Any]],
    resource_group_name: builtins.str,
    task_type: builtins.str,
    time_zone_id: builtins.str,
    daily_recurrence: typing.Optional[typing.Union[DevTestScheduleDailyRecurrence, typing.Dict[builtins.str, typing.Any]]] = None,
    hourly_recurrence: typing.Optional[typing.Union[DevTestScheduleHourlyRecurrence, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    status: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[DevTestScheduleTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    weekly_recurrence: typing.Optional[typing.Union[DevTestScheduleWeeklyRecurrence, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6cc8c0424bd7a950bc4857403e1f2281d8cb9e63e0a89f3a39bbe2563b1ed49(
    *,
    time: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__001928fa3959131480be9d9d88af7cf0ba5a89279f6290c340d8c2b1813ebc19(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__663b36bf8cf59a9b10e110c454844c42384594cd49c0f6e806217d28f72a4a6b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2c4f9cf98c2dc45ff01c3143d690d4c35a42ca1a7aec14bcdd3ebdf3d4e64c5(
    value: typing.Optional[DevTestScheduleDailyRecurrence],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2a6f75bca231b69416ad6662d902b05f8d55f019febdd709935312d223e50a4(
    *,
    minute: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb6d558a0c5b6d89f0d369e40084e6bfb0685f39ddcd2869c2119fd1dc8bddfa(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78693656949a7c666501c94c03078c4a83ac1441c99357256384415a4c0ac679(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__49077ae5618e45831c4f653dad62773f1d29dc3f1c33147e6dd0aac4e3fb8435(
    value: typing.Optional[DevTestScheduleHourlyRecurrence],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c245ca5694a1b0c74f9a27e0ad28ec269eaaad444f12b18062562e9a0fcb1f99(
    *,
    status: typing.Optional[builtins.str] = None,
    time_in_minutes: typing.Optional[jsii.Number] = None,
    webhook_url: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b7b6721e65dba94aa171b04cd66031e1d939437efcf43987c94afd824872097a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__043fc82ef9275663e679d913d99efc19f1c8dd42b1ebffc1b2f9db9561d4e2a1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae2d15e7dba009e187a81bbd3c736566608dabf16c7392522fdc900e38ed3392(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc5d86232d6d1b101f139d594f8b691d8c34c9dc7ba7aafc4fb3da4ba47180e0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e4662d85bc23cd845543f99c1491df67a70b20d653b5ee9460a9129215626c0(
    value: typing.Optional[DevTestScheduleNotificationSettings],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__55890127b64b8c4f8a6dd33a1c83e6df9621e8cd665b3df92abb234328e3514a(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    read: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f8bd30c2a88252d15449f40ba2188f8b3f91c4517128dbbbb7adb9efeed11e1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30e41f3a33bfecec5299f1d701382c83838cf8115659d3d7e90e7f799254a772(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e0caa1bcb2a72e0bde22ca58eb15ce084cb01ca6127caf8fea627abcfdd8e650(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4193edeef3fb6adc358f1d3c10b428c7f753c3d21c4783274d605d60af554b0d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be9456ef1cde6f13d4ce85882d606d896bebb2ec5267dc171712f007fbb056a2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4d8f5b44327374183ff03176e00bbd6eadf7941e5a0fcd91e92d4164a9f6abc(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DevTestScheduleTimeouts]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9477c2e0193d2967bd62e8d5adb14952ba7585a8014370b2c178f138658e3fe3(
    *,
    time: builtins.str,
    week_days: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66761efeb0e40eb54be0f94e84386b01510f774c1eb298640460dab50872aa2d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d5bce78b66139847cb3ee63eabd134ca4c27969814d52008bdc48643bde29cb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52bb1675213987a5234f7bc9952f93e70e466817875570796d2e326455ff08e9(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__524eb35c71fcffa0ce9aa7a15cb0c4dc9d91b95adf709585f9eb6936bc9baae6(
    value: typing.Optional[DevTestScheduleWeeklyRecurrence],
) -> None:
    """Type checking stubs"""
    pass
