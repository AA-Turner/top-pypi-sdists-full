r'''
# `datadog_downtime`

Refer to the Terraform Registry for docs: [`datadog_downtime`](https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/downtime).
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


class Downtime(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.downtime.Downtime",
):
    '''Represents a {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/downtime datadog_downtime}.'''

    def __init__(
        self,
        scope_: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        scope: typing.Sequence[builtins.str],
        end: typing.Optional[jsii.Number] = None,
        end_date: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        message: typing.Optional[builtins.str] = None,
        monitor_id: typing.Optional[jsii.Number] = None,
        monitor_tags: typing.Optional[typing.Sequence[builtins.str]] = None,
        mute_first_recovery_notification: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        recurrence: typing.Optional[typing.Union["DowntimeRecurrence", typing.Dict[builtins.str, typing.Any]]] = None,
        start: typing.Optional[jsii.Number] = None,
        start_date: typing.Optional[builtins.str] = None,
        timezone: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/downtime datadog_downtime} Resource.

        :param scope_: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param scope: specify the group scope to which this downtime applies. For everything use '*'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/downtime#scope Downtime#scope}
        :param end: Optionally specify an end date when this downtime should expire. Accepts a Unix timestamp in UTC. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/downtime#end Downtime#end}
        :param end_date: String representing date and time to end the downtime in RFC3339 format. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/downtime#end_date Downtime#end_date}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/downtime#id Downtime#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param message: An optional message to provide when creating the downtime, can include notification handles. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/downtime#message Downtime#message}
        :param monitor_id: When specified, this downtime will only apply to this monitor. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/downtime#monitor_id Downtime#monitor_id}
        :param monitor_tags: A list of monitor tags (up to 32) to base the scheduled downtime on. Only monitors that have all selected tags are silenced Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/downtime#monitor_tags Downtime#monitor_tags}
        :param mute_first_recovery_notification: When true the first recovery notification during the downtime will be muted Defaults to ``false``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/downtime#mute_first_recovery_notification Downtime#mute_first_recovery_notification}
        :param recurrence: recurrence block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/downtime#recurrence Downtime#recurrence}
        :param start: Specify when this downtime should start. Accepts a Unix timestamp in UTC. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/downtime#start Downtime#start}
        :param start_date: String representing date and time to start the downtime in RFC3339 format. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/downtime#start_date Downtime#start_date}
        :param timezone: The timezone for the downtime. Follows IANA timezone database identifiers. Defaults to ``"UTC"``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/downtime#timezone Downtime#timezone}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__748fb363a8565dd2824b0bfacd7b133c8f4b298e87589202438b2c43f062db25)
            check_type(argname="argument scope_", value=scope_, expected_type=type_hints["scope_"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = DowntimeConfig(
            scope=scope,
            end=end,
            end_date=end_date,
            id=id,
            message=message,
            monitor_id=monitor_id,
            monitor_tags=monitor_tags,
            mute_first_recovery_notification=mute_first_recovery_notification,
            recurrence=recurrence,
            start=start,
            start_date=start_date,
            timezone=timezone,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope_, id_, config])

    @jsii.member(jsii_name="generateConfigForImport")
    @builtins.classmethod
    def generate_config_for_import(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        import_to_id: builtins.str,
        import_from_id: builtins.str,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    ) -> _cdktf_9a9027ec.ImportableResource:
        '''Generates CDKTF code for importing a Downtime resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the Downtime to import.
        :param import_from_id: The id of the existing Downtime that should be imported. Refer to the {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/downtime#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the Downtime to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6dde5aa15fb8273e214cab0565eb7f57f7a2ccaa3e65b95360ff097eb5b7988d)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putRecurrence")
    def put_recurrence(
        self,
        *,
        type: builtins.str,
        period: typing.Optional[jsii.Number] = None,
        rrule: typing.Optional[builtins.str] = None,
        until_date: typing.Optional[jsii.Number] = None,
        until_occurrences: typing.Optional[jsii.Number] = None,
        week_days: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param type: One of ``days``, ``weeks``, ``months``, ``years``, or ``rrule``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/downtime#type Downtime#type}
        :param period: How often to repeat as an integer. For example to repeat every 3 days, select a ``type`` of ``days`` and a ``period`` of ``3``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/downtime#period Downtime#period}
        :param rrule: The RRULE standard for defining recurring events. For example, to have a recurring event on the first day of each month, use ``FREQ=MONTHLY;INTERVAL=1``. Most common rrule options from the iCalendar Spec are supported. Attributes specifying the duration in RRULE are not supported (for example, ``DTSTART``, ``DTEND``, ``DURATION``). Only applicable when ``type`` is ``rrule``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/downtime#rrule Downtime#rrule}
        :param until_date: The date at which the recurrence should end as a POSIX timestamp. ``until_occurrences`` and ``until_date`` are mutually exclusive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/downtime#until_date Downtime#until_date}
        :param until_occurrences: How many times the downtime will be rescheduled. ``until_occurrences`` and ``until_date`` are mutually exclusive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/downtime#until_occurrences Downtime#until_occurrences}
        :param week_days: A list of week days to repeat on. Choose from: ``Mon``, ``Tue``, ``Wed``, ``Thu``, ``Fri``, ``Sat`` or ``Sun``. Only applicable when ``type`` is ``weeks``. First letter must be capitalized. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/downtime#week_days Downtime#week_days}
        '''
        value = DowntimeRecurrence(
            type=type,
            period=period,
            rrule=rrule,
            until_date=until_date,
            until_occurrences=until_occurrences,
            week_days=week_days,
        )

        return typing.cast(None, jsii.invoke(self, "putRecurrence", [value]))

    @jsii.member(jsii_name="resetEnd")
    def reset_end(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnd", []))

    @jsii.member(jsii_name="resetEndDate")
    def reset_end_date(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEndDate", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetMessage")
    def reset_message(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMessage", []))

    @jsii.member(jsii_name="resetMonitorId")
    def reset_monitor_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMonitorId", []))

    @jsii.member(jsii_name="resetMonitorTags")
    def reset_monitor_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMonitorTags", []))

    @jsii.member(jsii_name="resetMuteFirstRecoveryNotification")
    def reset_mute_first_recovery_notification(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMuteFirstRecoveryNotification", []))

    @jsii.member(jsii_name="resetRecurrence")
    def reset_recurrence(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRecurrence", []))

    @jsii.member(jsii_name="resetStart")
    def reset_start(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStart", []))

    @jsii.member(jsii_name="resetStartDate")
    def reset_start_date(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStartDate", []))

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
    @jsii.member(jsii_name="active")
    def active(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "active"))

    @builtins.property
    @jsii.member(jsii_name="activeChildId")
    def active_child_id(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "activeChildId"))

    @builtins.property
    @jsii.member(jsii_name="disabled")
    def disabled(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "disabled"))

    @builtins.property
    @jsii.member(jsii_name="recurrence")
    def recurrence(self) -> "DowntimeRecurrenceOutputReference":
        return typing.cast("DowntimeRecurrenceOutputReference", jsii.get(self, "recurrence"))

    @builtins.property
    @jsii.member(jsii_name="endDateInput")
    def end_date_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "endDateInput"))

    @builtins.property
    @jsii.member(jsii_name="endInput")
    def end_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "endInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="messageInput")
    def message_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "messageInput"))

    @builtins.property
    @jsii.member(jsii_name="monitorIdInput")
    def monitor_id_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "monitorIdInput"))

    @builtins.property
    @jsii.member(jsii_name="monitorTagsInput")
    def monitor_tags_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "monitorTagsInput"))

    @builtins.property
    @jsii.member(jsii_name="muteFirstRecoveryNotificationInput")
    def mute_first_recovery_notification_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "muteFirstRecoveryNotificationInput"))

    @builtins.property
    @jsii.member(jsii_name="recurrenceInput")
    def recurrence_input(self) -> typing.Optional["DowntimeRecurrence"]:
        return typing.cast(typing.Optional["DowntimeRecurrence"], jsii.get(self, "recurrenceInput"))

    @builtins.property
    @jsii.member(jsii_name="scopeInput")
    def scope_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "scopeInput"))

    @builtins.property
    @jsii.member(jsii_name="startDateInput")
    def start_date_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "startDateInput"))

    @builtins.property
    @jsii.member(jsii_name="startInput")
    def start_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "startInput"))

    @builtins.property
    @jsii.member(jsii_name="timezoneInput")
    def timezone_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "timezoneInput"))

    @builtins.property
    @jsii.member(jsii_name="end")
    def end(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "end"))

    @end.setter
    def end(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__88e7d5be460a99299e203d0c57ca32a70a0fc344edc325800216231c5a79f796)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "end", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="endDate")
    def end_date(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "endDate"))

    @end_date.setter
    def end_date(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f00a96f510bd53c84ea1ac95f990bc95bd1bb6efb52c4f6d08b038abd2214c41)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "endDate", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b87e0f72ad1c27b05c97beb4101b498e7fed7bd7996f54a5653f956756b41c96)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="message")
    def message(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "message"))

    @message.setter
    def message(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ae1c19e788cea146085858a4a19787dab7bd544091844dd471863d3c732cc561)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "message", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="monitorId")
    def monitor_id(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "monitorId"))

    @monitor_id.setter
    def monitor_id(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a01983b9869e01632328fab91c9ecf0e6f3adc371a9d933b31aac2fa72156af)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "monitorId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="monitorTags")
    def monitor_tags(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "monitorTags"))

    @monitor_tags.setter
    def monitor_tags(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__187fa959d70a8ac327705836ad6d3e46529373d752e8581813d0409b9668efd3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "monitorTags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="muteFirstRecoveryNotification")
    def mute_first_recovery_notification(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "muteFirstRecoveryNotification"))

    @mute_first_recovery_notification.setter
    def mute_first_recovery_notification(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a2d12427b52fd2b9b30f295e80bf0ed918cf613111cd11c19aa3d3ec8375e659)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "muteFirstRecoveryNotification", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="scope")
    def scope(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "scope"))

    @scope.setter
    def scope(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4d0aae3eec8db3b9201a2b09a3b2427c90eb4805affbceff8f633c2884f8c10a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scope", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="start")
    def start(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "start"))

    @start.setter
    def start(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c5448314c9ded1fd339e621f944ff283cf5a35d3d88592c56ddf588badcc5a6e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "start", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="startDate")
    def start_date(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "startDate"))

    @start_date.setter
    def start_date(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a90172101b81fd97d2c830e7c167c2f40761ca6991986d1d604ea96cf685427)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "startDate", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="timezone")
    def timezone(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "timezone"))

    @timezone.setter
    def timezone(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d39434039f9b5c12ef08d9b7c4b9903e1310573f0283f24eeb7a2a60ee89b51)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timezone", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.downtime.DowntimeConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "scope": "scope",
        "end": "end",
        "end_date": "endDate",
        "id": "id",
        "message": "message",
        "monitor_id": "monitorId",
        "monitor_tags": "monitorTags",
        "mute_first_recovery_notification": "muteFirstRecoveryNotification",
        "recurrence": "recurrence",
        "start": "start",
        "start_date": "startDate",
        "timezone": "timezone",
    },
)
class DowntimeConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        scope: typing.Sequence[builtins.str],
        end: typing.Optional[jsii.Number] = None,
        end_date: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        message: typing.Optional[builtins.str] = None,
        monitor_id: typing.Optional[jsii.Number] = None,
        monitor_tags: typing.Optional[typing.Sequence[builtins.str]] = None,
        mute_first_recovery_notification: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        recurrence: typing.Optional[typing.Union["DowntimeRecurrence", typing.Dict[builtins.str, typing.Any]]] = None,
        start: typing.Optional[jsii.Number] = None,
        start_date: typing.Optional[builtins.str] = None,
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
        :param scope: specify the group scope to which this downtime applies. For everything use '*'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/downtime#scope Downtime#scope}
        :param end: Optionally specify an end date when this downtime should expire. Accepts a Unix timestamp in UTC. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/downtime#end Downtime#end}
        :param end_date: String representing date and time to end the downtime in RFC3339 format. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/downtime#end_date Downtime#end_date}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/downtime#id Downtime#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param message: An optional message to provide when creating the downtime, can include notification handles. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/downtime#message Downtime#message}
        :param monitor_id: When specified, this downtime will only apply to this monitor. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/downtime#monitor_id Downtime#monitor_id}
        :param monitor_tags: A list of monitor tags (up to 32) to base the scheduled downtime on. Only monitors that have all selected tags are silenced Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/downtime#monitor_tags Downtime#monitor_tags}
        :param mute_first_recovery_notification: When true the first recovery notification during the downtime will be muted Defaults to ``false``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/downtime#mute_first_recovery_notification Downtime#mute_first_recovery_notification}
        :param recurrence: recurrence block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/downtime#recurrence Downtime#recurrence}
        :param start: Specify when this downtime should start. Accepts a Unix timestamp in UTC. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/downtime#start Downtime#start}
        :param start_date: String representing date and time to start the downtime in RFC3339 format. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/downtime#start_date Downtime#start_date}
        :param timezone: The timezone for the downtime. Follows IANA timezone database identifiers. Defaults to ``"UTC"``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/downtime#timezone Downtime#timezone}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(recurrence, dict):
            recurrence = DowntimeRecurrence(**recurrence)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__53ddfe0ed99170dd5239f75d697327f90d1e50370ef23d06f1d09124f5138ff4)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument end", value=end, expected_type=type_hints["end"])
            check_type(argname="argument end_date", value=end_date, expected_type=type_hints["end_date"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument message", value=message, expected_type=type_hints["message"])
            check_type(argname="argument monitor_id", value=monitor_id, expected_type=type_hints["monitor_id"])
            check_type(argname="argument monitor_tags", value=monitor_tags, expected_type=type_hints["monitor_tags"])
            check_type(argname="argument mute_first_recovery_notification", value=mute_first_recovery_notification, expected_type=type_hints["mute_first_recovery_notification"])
            check_type(argname="argument recurrence", value=recurrence, expected_type=type_hints["recurrence"])
            check_type(argname="argument start", value=start, expected_type=type_hints["start"])
            check_type(argname="argument start_date", value=start_date, expected_type=type_hints["start_date"])
            check_type(argname="argument timezone", value=timezone, expected_type=type_hints["timezone"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "scope": scope,
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
        if end is not None:
            self._values["end"] = end
        if end_date is not None:
            self._values["end_date"] = end_date
        if id is not None:
            self._values["id"] = id
        if message is not None:
            self._values["message"] = message
        if monitor_id is not None:
            self._values["monitor_id"] = monitor_id
        if monitor_tags is not None:
            self._values["monitor_tags"] = monitor_tags
        if mute_first_recovery_notification is not None:
            self._values["mute_first_recovery_notification"] = mute_first_recovery_notification
        if recurrence is not None:
            self._values["recurrence"] = recurrence
        if start is not None:
            self._values["start"] = start
        if start_date is not None:
            self._values["start_date"] = start_date
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
    def scope(self) -> typing.List[builtins.str]:
        '''specify the group scope to which this downtime applies. For everything use '*'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/downtime#scope Downtime#scope}
        '''
        result = self._values.get("scope")
        assert result is not None, "Required property 'scope' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def end(self) -> typing.Optional[jsii.Number]:
        '''Optionally specify an end date when this downtime should expire. Accepts a Unix timestamp in UTC.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/downtime#end Downtime#end}
        '''
        result = self._values.get("end")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def end_date(self) -> typing.Optional[builtins.str]:
        '''String representing date and time to end the downtime in RFC3339 format.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/downtime#end_date Downtime#end_date}
        '''
        result = self._values.get("end_date")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/downtime#id Downtime#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def message(self) -> typing.Optional[builtins.str]:
        '''An optional message to provide when creating the downtime, can include notification handles.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/downtime#message Downtime#message}
        '''
        result = self._values.get("message")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def monitor_id(self) -> typing.Optional[jsii.Number]:
        '''When specified, this downtime will only apply to this monitor.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/downtime#monitor_id Downtime#monitor_id}
        '''
        result = self._values.get("monitor_id")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def monitor_tags(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of monitor tags (up to 32) to base the scheduled downtime on.

        Only monitors that have all selected tags are silenced

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/downtime#monitor_tags Downtime#monitor_tags}
        '''
        result = self._values.get("monitor_tags")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def mute_first_recovery_notification(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''When true the first recovery notification during the downtime will be muted Defaults to ``false``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/downtime#mute_first_recovery_notification Downtime#mute_first_recovery_notification}
        '''
        result = self._values.get("mute_first_recovery_notification")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def recurrence(self) -> typing.Optional["DowntimeRecurrence"]:
        '''recurrence block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/downtime#recurrence Downtime#recurrence}
        '''
        result = self._values.get("recurrence")
        return typing.cast(typing.Optional["DowntimeRecurrence"], result)

    @builtins.property
    def start(self) -> typing.Optional[jsii.Number]:
        '''Specify when this downtime should start. Accepts a Unix timestamp in UTC.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/downtime#start Downtime#start}
        '''
        result = self._values.get("start")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def start_date(self) -> typing.Optional[builtins.str]:
        '''String representing date and time to start the downtime in RFC3339 format.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/downtime#start_date Downtime#start_date}
        '''
        result = self._values.get("start_date")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timezone(self) -> typing.Optional[builtins.str]:
        '''The timezone for the downtime. Follows IANA timezone database identifiers. Defaults to ``"UTC"``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/downtime#timezone Downtime#timezone}
        '''
        result = self._values.get("timezone")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DowntimeConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.downtime.DowntimeRecurrence",
    jsii_struct_bases=[],
    name_mapping={
        "type": "type",
        "period": "period",
        "rrule": "rrule",
        "until_date": "untilDate",
        "until_occurrences": "untilOccurrences",
        "week_days": "weekDays",
    },
)
class DowntimeRecurrence:
    def __init__(
        self,
        *,
        type: builtins.str,
        period: typing.Optional[jsii.Number] = None,
        rrule: typing.Optional[builtins.str] = None,
        until_date: typing.Optional[jsii.Number] = None,
        until_occurrences: typing.Optional[jsii.Number] = None,
        week_days: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param type: One of ``days``, ``weeks``, ``months``, ``years``, or ``rrule``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/downtime#type Downtime#type}
        :param period: How often to repeat as an integer. For example to repeat every 3 days, select a ``type`` of ``days`` and a ``period`` of ``3``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/downtime#period Downtime#period}
        :param rrule: The RRULE standard for defining recurring events. For example, to have a recurring event on the first day of each month, use ``FREQ=MONTHLY;INTERVAL=1``. Most common rrule options from the iCalendar Spec are supported. Attributes specifying the duration in RRULE are not supported (for example, ``DTSTART``, ``DTEND``, ``DURATION``). Only applicable when ``type`` is ``rrule``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/downtime#rrule Downtime#rrule}
        :param until_date: The date at which the recurrence should end as a POSIX timestamp. ``until_occurrences`` and ``until_date`` are mutually exclusive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/downtime#until_date Downtime#until_date}
        :param until_occurrences: How many times the downtime will be rescheduled. ``until_occurrences`` and ``until_date`` are mutually exclusive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/downtime#until_occurrences Downtime#until_occurrences}
        :param week_days: A list of week days to repeat on. Choose from: ``Mon``, ``Tue``, ``Wed``, ``Thu``, ``Fri``, ``Sat`` or ``Sun``. Only applicable when ``type`` is ``weeks``. First letter must be capitalized. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/downtime#week_days Downtime#week_days}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7422e9de5415d77eebe132bf4f1e5225ed40c4a1b01cd88ff4ea1152f01ef13e)
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument period", value=period, expected_type=type_hints["period"])
            check_type(argname="argument rrule", value=rrule, expected_type=type_hints["rrule"])
            check_type(argname="argument until_date", value=until_date, expected_type=type_hints["until_date"])
            check_type(argname="argument until_occurrences", value=until_occurrences, expected_type=type_hints["until_occurrences"])
            check_type(argname="argument week_days", value=week_days, expected_type=type_hints["week_days"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "type": type,
        }
        if period is not None:
            self._values["period"] = period
        if rrule is not None:
            self._values["rrule"] = rrule
        if until_date is not None:
            self._values["until_date"] = until_date
        if until_occurrences is not None:
            self._values["until_occurrences"] = until_occurrences
        if week_days is not None:
            self._values["week_days"] = week_days

    @builtins.property
    def type(self) -> builtins.str:
        '''One of ``days``, ``weeks``, ``months``, ``years``, or ``rrule``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/downtime#type Downtime#type}
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def period(self) -> typing.Optional[jsii.Number]:
        '''How often to repeat as an integer.

        For example to repeat every 3 days, select a ``type`` of ``days`` and a ``period`` of ``3``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/downtime#period Downtime#period}
        '''
        result = self._values.get("period")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def rrule(self) -> typing.Optional[builtins.str]:
        '''The RRULE standard for defining recurring events.

        For example, to have a recurring event on the first day of each month, use ``FREQ=MONTHLY;INTERVAL=1``. Most common rrule options from the iCalendar Spec are supported. Attributes specifying the duration in RRULE are not supported (for example, ``DTSTART``, ``DTEND``, ``DURATION``). Only applicable when ``type`` is ``rrule``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/downtime#rrule Downtime#rrule}
        '''
        result = self._values.get("rrule")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def until_date(self) -> typing.Optional[jsii.Number]:
        '''The date at which the recurrence should end as a POSIX timestamp. ``until_occurrences`` and ``until_date`` are mutually exclusive.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/downtime#until_date Downtime#until_date}
        '''
        result = self._values.get("until_date")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def until_occurrences(self) -> typing.Optional[jsii.Number]:
        '''How many times the downtime will be rescheduled. ``until_occurrences`` and ``until_date`` are mutually exclusive.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/downtime#until_occurrences Downtime#until_occurrences}
        '''
        result = self._values.get("until_occurrences")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def week_days(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of week days to repeat on.

        Choose from: ``Mon``, ``Tue``, ``Wed``, ``Thu``, ``Fri``, ``Sat`` or ``Sun``. Only applicable when ``type`` is ``weeks``. First letter must be capitalized.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/downtime#week_days Downtime#week_days}
        '''
        result = self._values.get("week_days")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DowntimeRecurrence(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DowntimeRecurrenceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.downtime.DowntimeRecurrenceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1e0b55c996099ce2e7a0e5b269cc634780eb62b310902a29d25450e7524d4ad5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetPeriod")
    def reset_period(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPeriod", []))

    @jsii.member(jsii_name="resetRrule")
    def reset_rrule(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRrule", []))

    @jsii.member(jsii_name="resetUntilDate")
    def reset_until_date(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUntilDate", []))

    @jsii.member(jsii_name="resetUntilOccurrences")
    def reset_until_occurrences(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUntilOccurrences", []))

    @jsii.member(jsii_name="resetWeekDays")
    def reset_week_days(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWeekDays", []))

    @builtins.property
    @jsii.member(jsii_name="periodInput")
    def period_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "periodInput"))

    @builtins.property
    @jsii.member(jsii_name="rruleInput")
    def rrule_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "rruleInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="untilDateInput")
    def until_date_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "untilDateInput"))

    @builtins.property
    @jsii.member(jsii_name="untilOccurrencesInput")
    def until_occurrences_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "untilOccurrencesInput"))

    @builtins.property
    @jsii.member(jsii_name="weekDaysInput")
    def week_days_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "weekDaysInput"))

    @builtins.property
    @jsii.member(jsii_name="period")
    def period(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "period"))

    @period.setter
    def period(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__579b2c18024cb470b403bfb6d5ec1c1a3b420a9e5a3f89d1573706ed524eb7ee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "period", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="rrule")
    def rrule(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "rrule"))

    @rrule.setter
    def rrule(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__79d591385f5861f0b03786ed149dde069313c4f38ab9a43338ae94209c20f93a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rrule", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__744ec5458ace6e9b732b8b94f8fb6fc74a6199a40fa67adb688ff18582929741)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="untilDate")
    def until_date(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "untilDate"))

    @until_date.setter
    def until_date(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dadd434fe3eaf13878d7d7946f86bf9bb4b0a57bfe5d478791288bd7436158db)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "untilDate", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="untilOccurrences")
    def until_occurrences(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "untilOccurrences"))

    @until_occurrences.setter
    def until_occurrences(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__252f4a8fbcb49d7cc925b94a838547836a4ab954ce2bf4937757a007aa6744bd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "untilOccurrences", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="weekDays")
    def week_days(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "weekDays"))

    @week_days.setter
    def week_days(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__386bce39028bf7ec5d2fa41b94f8e7bb076a519d5d4d6f0e184ac6787ba23f01)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "weekDays", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[DowntimeRecurrence]:
        return typing.cast(typing.Optional[DowntimeRecurrence], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[DowntimeRecurrence]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__76a995701f58f4523f9bfc53a22ce6fde42f503aee4d8117fdefb2449072648e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "Downtime",
    "DowntimeConfig",
    "DowntimeRecurrence",
    "DowntimeRecurrenceOutputReference",
]

publication.publish()

def _typecheckingstub__748fb363a8565dd2824b0bfacd7b133c8f4b298e87589202438b2c43f062db25(
    scope_: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    scope: typing.Sequence[builtins.str],
    end: typing.Optional[jsii.Number] = None,
    end_date: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    message: typing.Optional[builtins.str] = None,
    monitor_id: typing.Optional[jsii.Number] = None,
    monitor_tags: typing.Optional[typing.Sequence[builtins.str]] = None,
    mute_first_recovery_notification: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    recurrence: typing.Optional[typing.Union[DowntimeRecurrence, typing.Dict[builtins.str, typing.Any]]] = None,
    start: typing.Optional[jsii.Number] = None,
    start_date: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__6dde5aa15fb8273e214cab0565eb7f57f7a2ccaa3e65b95360ff097eb5b7988d(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88e7d5be460a99299e203d0c57ca32a70a0fc344edc325800216231c5a79f796(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f00a96f510bd53c84ea1ac95f990bc95bd1bb6efb52c4f6d08b038abd2214c41(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b87e0f72ad1c27b05c97beb4101b498e7fed7bd7996f54a5653f956756b41c96(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae1c19e788cea146085858a4a19787dab7bd544091844dd471863d3c732cc561(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a01983b9869e01632328fab91c9ecf0e6f3adc371a9d933b31aac2fa72156af(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__187fa959d70a8ac327705836ad6d3e46529373d752e8581813d0409b9668efd3(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2d12427b52fd2b9b30f295e80bf0ed918cf613111cd11c19aa3d3ec8375e659(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d0aae3eec8db3b9201a2b09a3b2427c90eb4805affbceff8f633c2884f8c10a(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5448314c9ded1fd339e621f944ff283cf5a35d3d88592c56ddf588badcc5a6e(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a90172101b81fd97d2c830e7c167c2f40761ca6991986d1d604ea96cf685427(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d39434039f9b5c12ef08d9b7c4b9903e1310573f0283f24eeb7a2a60ee89b51(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53ddfe0ed99170dd5239f75d697327f90d1e50370ef23d06f1d09124f5138ff4(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    scope: typing.Sequence[builtins.str],
    end: typing.Optional[jsii.Number] = None,
    end_date: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    message: typing.Optional[builtins.str] = None,
    monitor_id: typing.Optional[jsii.Number] = None,
    monitor_tags: typing.Optional[typing.Sequence[builtins.str]] = None,
    mute_first_recovery_notification: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    recurrence: typing.Optional[typing.Union[DowntimeRecurrence, typing.Dict[builtins.str, typing.Any]]] = None,
    start: typing.Optional[jsii.Number] = None,
    start_date: typing.Optional[builtins.str] = None,
    timezone: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7422e9de5415d77eebe132bf4f1e5225ed40c4a1b01cd88ff4ea1152f01ef13e(
    *,
    type: builtins.str,
    period: typing.Optional[jsii.Number] = None,
    rrule: typing.Optional[builtins.str] = None,
    until_date: typing.Optional[jsii.Number] = None,
    until_occurrences: typing.Optional[jsii.Number] = None,
    week_days: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e0b55c996099ce2e7a0e5b269cc634780eb62b310902a29d25450e7524d4ad5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__579b2c18024cb470b403bfb6d5ec1c1a3b420a9e5a3f89d1573706ed524eb7ee(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79d591385f5861f0b03786ed149dde069313c4f38ab9a43338ae94209c20f93a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__744ec5458ace6e9b732b8b94f8fb6fc74a6199a40fa67adb688ff18582929741(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dadd434fe3eaf13878d7d7946f86bf9bb4b0a57bfe5d478791288bd7436158db(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__252f4a8fbcb49d7cc925b94a838547836a4ab954ce2bf4937757a007aa6744bd(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__386bce39028bf7ec5d2fa41b94f8e7bb076a519d5d4d6f0e184ac6787ba23f01(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76a995701f58f4523f9bfc53a22ce6fde42f503aee4d8117fdefb2449072648e(
    value: typing.Optional[DowntimeRecurrence],
) -> None:
    """Type checking stubs"""
    pass
