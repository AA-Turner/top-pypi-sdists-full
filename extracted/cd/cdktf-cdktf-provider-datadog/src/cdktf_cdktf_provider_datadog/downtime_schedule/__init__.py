r'''
# `datadog_downtime_schedule`

Refer to the Terraform Registry for docs: [`datadog_downtime_schedule`](https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/downtime_schedule).
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


class DowntimeSchedule(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.downtimeSchedule.DowntimeSchedule",
):
    '''Represents a {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/downtime_schedule datadog_downtime_schedule}.'''

    def __init__(
        self,
        scope_: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        scope: builtins.str,
        display_timezone: typing.Optional[builtins.str] = None,
        message: typing.Optional[builtins.str] = None,
        monitor_identifier: typing.Optional[typing.Union["DowntimeScheduleMonitorIdentifier", typing.Dict[builtins.str, typing.Any]]] = None,
        mute_first_recovery_notification: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        notify_end_states: typing.Optional[typing.Sequence[builtins.str]] = None,
        notify_end_types: typing.Optional[typing.Sequence[builtins.str]] = None,
        one_time_schedule: typing.Optional[typing.Union["DowntimeScheduleOneTimeSchedule", typing.Dict[builtins.str, typing.Any]]] = None,
        recurring_schedule: typing.Optional[typing.Union["DowntimeScheduleRecurringSchedule", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/downtime_schedule datadog_downtime_schedule} Resource.

        :param scope_: The scope in which to define this construct.
        :param id: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param scope: The scope to which the downtime applies. Must follow the `common search syntax <https://docs.datadoghq.com/logs/explorer/search_syntax/>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/downtime_schedule#scope DowntimeSchedule#scope}
        :param display_timezone: The timezone in which to display the downtime's start and end times in Datadog applications. This is not used as an offset for scheduling. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/downtime_schedule#display_timezone DowntimeSchedule#display_timezone}
        :param message: A message to include with notifications for this downtime. Email notifications can be sent to specific users by using the same ``@username`` notation as events. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/downtime_schedule#message DowntimeSchedule#message}
        :param monitor_identifier: monitor_identifier block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/downtime_schedule#monitor_identifier DowntimeSchedule#monitor_identifier}
        :param mute_first_recovery_notification: If the first recovery notification during a downtime should be muted. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/downtime_schedule#mute_first_recovery_notification DowntimeSchedule#mute_first_recovery_notification}
        :param notify_end_states: States that will trigger a monitor notification when the ``notify_end_types`` action occurs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/downtime_schedule#notify_end_states DowntimeSchedule#notify_end_states}
        :param notify_end_types: Actions that will trigger a monitor notification if the downtime is in the ``notify_end_types`` state. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/downtime_schedule#notify_end_types DowntimeSchedule#notify_end_types}
        :param one_time_schedule: one_time_schedule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/downtime_schedule#one_time_schedule DowntimeSchedule#one_time_schedule}
        :param recurring_schedule: recurring_schedule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/downtime_schedule#recurring_schedule DowntimeSchedule#recurring_schedule}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b1e223b7f836a1025ca3ed2b8a6af63f5471e59bfad2d879943995dc339d5f06)
            check_type(argname="argument scope_", value=scope_, expected_type=type_hints["scope_"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        config = DowntimeScheduleConfig(
            scope=scope,
            display_timezone=display_timezone,
            message=message,
            monitor_identifier=monitor_identifier,
            mute_first_recovery_notification=mute_first_recovery_notification,
            notify_end_states=notify_end_states,
            notify_end_types=notify_end_types,
            one_time_schedule=one_time_schedule,
            recurring_schedule=recurring_schedule,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope_, id, config])

    @jsii.member(jsii_name="generateConfigForImport")
    @builtins.classmethod
    def generate_config_for_import(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        import_to_id: builtins.str,
        import_from_id: builtins.str,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    ) -> _cdktf_9a9027ec.ImportableResource:
        '''Generates CDKTF code for importing a DowntimeSchedule resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the DowntimeSchedule to import.
        :param import_from_id: The id of the existing DowntimeSchedule that should be imported. Refer to the {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/downtime_schedule#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the DowntimeSchedule to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e4adb358eccdf3554f7c40d543384c64c7e749abd809cb9db2bf377866d3a1b9)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putMonitorIdentifier")
    def put_monitor_identifier(
        self,
        *,
        monitor_id: typing.Optional[jsii.Number] = None,
        monitor_tags: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param monitor_id: ID of the monitor to prevent notifications. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/downtime_schedule#monitor_id DowntimeSchedule#monitor_id}
        :param monitor_tags: A list of monitor tags. For example, tags that are applied directly to monitors, not tags that are used in monitor queries (which are filtered by the scope parameter), to which the downtime applies. The resulting downtime applies to monitors that match **all** provided monitor tags. Setting ``monitor_tags`` to ``[*]`` configures the downtime to mute all monitors for the given scope. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/downtime_schedule#monitor_tags DowntimeSchedule#monitor_tags}
        '''
        value = DowntimeScheduleMonitorIdentifier(
            monitor_id=monitor_id, monitor_tags=monitor_tags
        )

        return typing.cast(None, jsii.invoke(self, "putMonitorIdentifier", [value]))

    @jsii.member(jsii_name="putOneTimeSchedule")
    def put_one_time_schedule(
        self,
        *,
        end: typing.Optional[builtins.str] = None,
        start: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param end: ISO-8601 Datetime to end the downtime. Must include a UTC offset of zero. If not provided, the downtime never ends. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/downtime_schedule#end DowntimeSchedule#end}
        :param start: ISO-8601 Datetime to start the downtime. Must include a UTC offset of zero. If not provided, the downtime starts the moment it is created. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/downtime_schedule#start DowntimeSchedule#start}
        '''
        value = DowntimeScheduleOneTimeSchedule(end=end, start=start)

        return typing.cast(None, jsii.invoke(self, "putOneTimeSchedule", [value]))

    @jsii.member(jsii_name="putRecurringSchedule")
    def put_recurring_schedule(
        self,
        *,
        recurrence: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DowntimeScheduleRecurringScheduleRecurrence", typing.Dict[builtins.str, typing.Any]]]]] = None,
        timezone: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param recurrence: recurrence block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/downtime_schedule#recurrence DowntimeSchedule#recurrence}
        :param timezone: The timezone in which to schedule the downtime. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/downtime_schedule#timezone DowntimeSchedule#timezone}
        '''
        value = DowntimeScheduleRecurringSchedule(
            recurrence=recurrence, timezone=timezone
        )

        return typing.cast(None, jsii.invoke(self, "putRecurringSchedule", [value]))

    @jsii.member(jsii_name="resetDisplayTimezone")
    def reset_display_timezone(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDisplayTimezone", []))

    @jsii.member(jsii_name="resetMessage")
    def reset_message(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMessage", []))

    @jsii.member(jsii_name="resetMonitorIdentifier")
    def reset_monitor_identifier(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMonitorIdentifier", []))

    @jsii.member(jsii_name="resetMuteFirstRecoveryNotification")
    def reset_mute_first_recovery_notification(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMuteFirstRecoveryNotification", []))

    @jsii.member(jsii_name="resetNotifyEndStates")
    def reset_notify_end_states(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNotifyEndStates", []))

    @jsii.member(jsii_name="resetNotifyEndTypes")
    def reset_notify_end_types(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNotifyEndTypes", []))

    @jsii.member(jsii_name="resetOneTimeSchedule")
    def reset_one_time_schedule(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOneTimeSchedule", []))

    @jsii.member(jsii_name="resetRecurringSchedule")
    def reset_recurring_schedule(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRecurringSchedule", []))

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
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property
    @jsii.member(jsii_name="monitorIdentifier")
    def monitor_identifier(self) -> "DowntimeScheduleMonitorIdentifierOutputReference":
        return typing.cast("DowntimeScheduleMonitorIdentifierOutputReference", jsii.get(self, "monitorIdentifier"))

    @builtins.property
    @jsii.member(jsii_name="oneTimeSchedule")
    def one_time_schedule(self) -> "DowntimeScheduleOneTimeScheduleOutputReference":
        return typing.cast("DowntimeScheduleOneTimeScheduleOutputReference", jsii.get(self, "oneTimeSchedule"))

    @builtins.property
    @jsii.member(jsii_name="recurringSchedule")
    def recurring_schedule(self) -> "DowntimeScheduleRecurringScheduleOutputReference":
        return typing.cast("DowntimeScheduleRecurringScheduleOutputReference", jsii.get(self, "recurringSchedule"))

    @builtins.property
    @jsii.member(jsii_name="displayTimezoneInput")
    def display_timezone_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "displayTimezoneInput"))

    @builtins.property
    @jsii.member(jsii_name="messageInput")
    def message_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "messageInput"))

    @builtins.property
    @jsii.member(jsii_name="monitorIdentifierInput")
    def monitor_identifier_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "DowntimeScheduleMonitorIdentifier"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "DowntimeScheduleMonitorIdentifier"]], jsii.get(self, "monitorIdentifierInput"))

    @builtins.property
    @jsii.member(jsii_name="muteFirstRecoveryNotificationInput")
    def mute_first_recovery_notification_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "muteFirstRecoveryNotificationInput"))

    @builtins.property
    @jsii.member(jsii_name="notifyEndStatesInput")
    def notify_end_states_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "notifyEndStatesInput"))

    @builtins.property
    @jsii.member(jsii_name="notifyEndTypesInput")
    def notify_end_types_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "notifyEndTypesInput"))

    @builtins.property
    @jsii.member(jsii_name="oneTimeScheduleInput")
    def one_time_schedule_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "DowntimeScheduleOneTimeSchedule"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "DowntimeScheduleOneTimeSchedule"]], jsii.get(self, "oneTimeScheduleInput"))

    @builtins.property
    @jsii.member(jsii_name="recurringScheduleInput")
    def recurring_schedule_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "DowntimeScheduleRecurringSchedule"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "DowntimeScheduleRecurringSchedule"]], jsii.get(self, "recurringScheduleInput"))

    @builtins.property
    @jsii.member(jsii_name="scopeInput")
    def scope_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "scopeInput"))

    @builtins.property
    @jsii.member(jsii_name="displayTimezone")
    def display_timezone(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "displayTimezone"))

    @display_timezone.setter
    def display_timezone(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cdb564afb1f323db76e8e46840b85a150d43beeac31756cd2c2db9b11d253f70)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "displayTimezone", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="message")
    def message(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "message"))

    @message.setter
    def message(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__310dbd787e59f7bc0f0454c43804e81dc28bdc4c8be205f6e30f6c926f2ad9b8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "message", value) # pyright: ignore[reportArgumentType]

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
            type_hints = typing.get_type_hints(_typecheckingstub__abe7b14734c552f1345c524ef7bda59f2fce266e7c006373dd0d8be474b6bc60)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "muteFirstRecoveryNotification", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="notifyEndStates")
    def notify_end_states(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "notifyEndStates"))

    @notify_end_states.setter
    def notify_end_states(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1a6fa67bf8ef5ea4ba616af4da5d7144634983855aef68927b377f65e8a66f0e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "notifyEndStates", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="notifyEndTypes")
    def notify_end_types(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "notifyEndTypes"))

    @notify_end_types.setter
    def notify_end_types(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d2a1e72a169641cf13c6b016e417393349468700ee7d888800301056ee618030)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "notifyEndTypes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="scope")
    def scope(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "scope"))

    @scope.setter
    def scope(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa6413f2ab552c5a353ec1ebc71e290018ca4bad1619620b798b6da41ae6e018)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scope", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.downtimeSchedule.DowntimeScheduleConfig",
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
        "display_timezone": "displayTimezone",
        "message": "message",
        "monitor_identifier": "monitorIdentifier",
        "mute_first_recovery_notification": "muteFirstRecoveryNotification",
        "notify_end_states": "notifyEndStates",
        "notify_end_types": "notifyEndTypes",
        "one_time_schedule": "oneTimeSchedule",
        "recurring_schedule": "recurringSchedule",
    },
)
class DowntimeScheduleConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        scope: builtins.str,
        display_timezone: typing.Optional[builtins.str] = None,
        message: typing.Optional[builtins.str] = None,
        monitor_identifier: typing.Optional[typing.Union["DowntimeScheduleMonitorIdentifier", typing.Dict[builtins.str, typing.Any]]] = None,
        mute_first_recovery_notification: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        notify_end_states: typing.Optional[typing.Sequence[builtins.str]] = None,
        notify_end_types: typing.Optional[typing.Sequence[builtins.str]] = None,
        one_time_schedule: typing.Optional[typing.Union["DowntimeScheduleOneTimeSchedule", typing.Dict[builtins.str, typing.Any]]] = None,
        recurring_schedule: typing.Optional[typing.Union["DowntimeScheduleRecurringSchedule", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param scope: The scope to which the downtime applies. Must follow the `common search syntax <https://docs.datadoghq.com/logs/explorer/search_syntax/>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/downtime_schedule#scope DowntimeSchedule#scope}
        :param display_timezone: The timezone in which to display the downtime's start and end times in Datadog applications. This is not used as an offset for scheduling. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/downtime_schedule#display_timezone DowntimeSchedule#display_timezone}
        :param message: A message to include with notifications for this downtime. Email notifications can be sent to specific users by using the same ``@username`` notation as events. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/downtime_schedule#message DowntimeSchedule#message}
        :param monitor_identifier: monitor_identifier block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/downtime_schedule#monitor_identifier DowntimeSchedule#monitor_identifier}
        :param mute_first_recovery_notification: If the first recovery notification during a downtime should be muted. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/downtime_schedule#mute_first_recovery_notification DowntimeSchedule#mute_first_recovery_notification}
        :param notify_end_states: States that will trigger a monitor notification when the ``notify_end_types`` action occurs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/downtime_schedule#notify_end_states DowntimeSchedule#notify_end_states}
        :param notify_end_types: Actions that will trigger a monitor notification if the downtime is in the ``notify_end_types`` state. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/downtime_schedule#notify_end_types DowntimeSchedule#notify_end_types}
        :param one_time_schedule: one_time_schedule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/downtime_schedule#one_time_schedule DowntimeSchedule#one_time_schedule}
        :param recurring_schedule: recurring_schedule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/downtime_schedule#recurring_schedule DowntimeSchedule#recurring_schedule}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(monitor_identifier, dict):
            monitor_identifier = DowntimeScheduleMonitorIdentifier(**monitor_identifier)
        if isinstance(one_time_schedule, dict):
            one_time_schedule = DowntimeScheduleOneTimeSchedule(**one_time_schedule)
        if isinstance(recurring_schedule, dict):
            recurring_schedule = DowntimeScheduleRecurringSchedule(**recurring_schedule)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__be8f37b7e144b3b157d68716ade513f5f4e102bb555d119705598fe0e47f26ed)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument display_timezone", value=display_timezone, expected_type=type_hints["display_timezone"])
            check_type(argname="argument message", value=message, expected_type=type_hints["message"])
            check_type(argname="argument monitor_identifier", value=monitor_identifier, expected_type=type_hints["monitor_identifier"])
            check_type(argname="argument mute_first_recovery_notification", value=mute_first_recovery_notification, expected_type=type_hints["mute_first_recovery_notification"])
            check_type(argname="argument notify_end_states", value=notify_end_states, expected_type=type_hints["notify_end_states"])
            check_type(argname="argument notify_end_types", value=notify_end_types, expected_type=type_hints["notify_end_types"])
            check_type(argname="argument one_time_schedule", value=one_time_schedule, expected_type=type_hints["one_time_schedule"])
            check_type(argname="argument recurring_schedule", value=recurring_schedule, expected_type=type_hints["recurring_schedule"])
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
        if display_timezone is not None:
            self._values["display_timezone"] = display_timezone
        if message is not None:
            self._values["message"] = message
        if monitor_identifier is not None:
            self._values["monitor_identifier"] = monitor_identifier
        if mute_first_recovery_notification is not None:
            self._values["mute_first_recovery_notification"] = mute_first_recovery_notification
        if notify_end_states is not None:
            self._values["notify_end_states"] = notify_end_states
        if notify_end_types is not None:
            self._values["notify_end_types"] = notify_end_types
        if one_time_schedule is not None:
            self._values["one_time_schedule"] = one_time_schedule
        if recurring_schedule is not None:
            self._values["recurring_schedule"] = recurring_schedule

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
    def scope(self) -> builtins.str:
        '''The scope to which the downtime applies. Must follow the `common search syntax <https://docs.datadoghq.com/logs/explorer/search_syntax/>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/downtime_schedule#scope DowntimeSchedule#scope}
        '''
        result = self._values.get("scope")
        assert result is not None, "Required property 'scope' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def display_timezone(self) -> typing.Optional[builtins.str]:
        '''The timezone in which to display the downtime's start and end times in Datadog applications.

        This is not used as an offset for scheduling.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/downtime_schedule#display_timezone DowntimeSchedule#display_timezone}
        '''
        result = self._values.get("display_timezone")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def message(self) -> typing.Optional[builtins.str]:
        '''A message to include with notifications for this downtime.

        Email notifications can be sent to specific users by using the same ``@username`` notation as events.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/downtime_schedule#message DowntimeSchedule#message}
        '''
        result = self._values.get("message")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def monitor_identifier(
        self,
    ) -> typing.Optional["DowntimeScheduleMonitorIdentifier"]:
        '''monitor_identifier block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/downtime_schedule#monitor_identifier DowntimeSchedule#monitor_identifier}
        '''
        result = self._values.get("monitor_identifier")
        return typing.cast(typing.Optional["DowntimeScheduleMonitorIdentifier"], result)

    @builtins.property
    def mute_first_recovery_notification(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If the first recovery notification during a downtime should be muted.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/downtime_schedule#mute_first_recovery_notification DowntimeSchedule#mute_first_recovery_notification}
        '''
        result = self._values.get("mute_first_recovery_notification")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def notify_end_states(self) -> typing.Optional[typing.List[builtins.str]]:
        '''States that will trigger a monitor notification when the ``notify_end_types`` action occurs.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/downtime_schedule#notify_end_states DowntimeSchedule#notify_end_states}
        '''
        result = self._values.get("notify_end_states")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def notify_end_types(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Actions that will trigger a monitor notification if the downtime is in the ``notify_end_types`` state.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/downtime_schedule#notify_end_types DowntimeSchedule#notify_end_types}
        '''
        result = self._values.get("notify_end_types")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def one_time_schedule(self) -> typing.Optional["DowntimeScheduleOneTimeSchedule"]:
        '''one_time_schedule block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/downtime_schedule#one_time_schedule DowntimeSchedule#one_time_schedule}
        '''
        result = self._values.get("one_time_schedule")
        return typing.cast(typing.Optional["DowntimeScheduleOneTimeSchedule"], result)

    @builtins.property
    def recurring_schedule(
        self,
    ) -> typing.Optional["DowntimeScheduleRecurringSchedule"]:
        '''recurring_schedule block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/downtime_schedule#recurring_schedule DowntimeSchedule#recurring_schedule}
        '''
        result = self._values.get("recurring_schedule")
        return typing.cast(typing.Optional["DowntimeScheduleRecurringSchedule"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DowntimeScheduleConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.downtimeSchedule.DowntimeScheduleMonitorIdentifier",
    jsii_struct_bases=[],
    name_mapping={"monitor_id": "monitorId", "monitor_tags": "monitorTags"},
)
class DowntimeScheduleMonitorIdentifier:
    def __init__(
        self,
        *,
        monitor_id: typing.Optional[jsii.Number] = None,
        monitor_tags: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param monitor_id: ID of the monitor to prevent notifications. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/downtime_schedule#monitor_id DowntimeSchedule#monitor_id}
        :param monitor_tags: A list of monitor tags. For example, tags that are applied directly to monitors, not tags that are used in monitor queries (which are filtered by the scope parameter), to which the downtime applies. The resulting downtime applies to monitors that match **all** provided monitor tags. Setting ``monitor_tags`` to ``[*]`` configures the downtime to mute all monitors for the given scope. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/downtime_schedule#monitor_tags DowntimeSchedule#monitor_tags}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b3dfa52cde1ae41461718af62317420cfd67c1d0ac0686a76c10926fd403f41e)
            check_type(argname="argument monitor_id", value=monitor_id, expected_type=type_hints["monitor_id"])
            check_type(argname="argument monitor_tags", value=monitor_tags, expected_type=type_hints["monitor_tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if monitor_id is not None:
            self._values["monitor_id"] = monitor_id
        if monitor_tags is not None:
            self._values["monitor_tags"] = monitor_tags

    @builtins.property
    def monitor_id(self) -> typing.Optional[jsii.Number]:
        '''ID of the monitor to prevent notifications.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/downtime_schedule#monitor_id DowntimeSchedule#monitor_id}
        '''
        result = self._values.get("monitor_id")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def monitor_tags(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of monitor tags.

        For example, tags that are applied directly to monitors, not tags that are used in monitor queries (which are filtered by the scope parameter), to which the downtime applies. The resulting downtime applies to monitors that match **all** provided monitor tags. Setting ``monitor_tags`` to ``[*]`` configures the downtime to mute all monitors for the given scope.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/downtime_schedule#monitor_tags DowntimeSchedule#monitor_tags}
        '''
        result = self._values.get("monitor_tags")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DowntimeScheduleMonitorIdentifier(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DowntimeScheduleMonitorIdentifierOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.downtimeSchedule.DowntimeScheduleMonitorIdentifierOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__009625c84c9df8d2ceb339ab76b194a9f5bdba69b2f30ce35bce1c76d68ff755)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetMonitorId")
    def reset_monitor_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMonitorId", []))

    @jsii.member(jsii_name="resetMonitorTags")
    def reset_monitor_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMonitorTags", []))

    @builtins.property
    @jsii.member(jsii_name="monitorIdInput")
    def monitor_id_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "monitorIdInput"))

    @builtins.property
    @jsii.member(jsii_name="monitorTagsInput")
    def monitor_tags_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "monitorTagsInput"))

    @builtins.property
    @jsii.member(jsii_name="monitorId")
    def monitor_id(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "monitorId"))

    @monitor_id.setter
    def monitor_id(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cfaa047aa152e323ecd7c6a726a7daa2c55de4206d901a67667fed9234ae8f82)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "monitorId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="monitorTags")
    def monitor_tags(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "monitorTags"))

    @monitor_tags.setter
    def monitor_tags(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cad44e5a459baf8bcb87c1a6d07c9425d886ecba27edbcf4be02c8e862c7be98)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "monitorTags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DowntimeScheduleMonitorIdentifier]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DowntimeScheduleMonitorIdentifier]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DowntimeScheduleMonitorIdentifier]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cefdc0b1da0bae0179435261302c2100bd712e9838ea92e4ea03e7e87b70f24d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.downtimeSchedule.DowntimeScheduleOneTimeSchedule",
    jsii_struct_bases=[],
    name_mapping={"end": "end", "start": "start"},
)
class DowntimeScheduleOneTimeSchedule:
    def __init__(
        self,
        *,
        end: typing.Optional[builtins.str] = None,
        start: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param end: ISO-8601 Datetime to end the downtime. Must include a UTC offset of zero. If not provided, the downtime never ends. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/downtime_schedule#end DowntimeSchedule#end}
        :param start: ISO-8601 Datetime to start the downtime. Must include a UTC offset of zero. If not provided, the downtime starts the moment it is created. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/downtime_schedule#start DowntimeSchedule#start}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__25a01102831bf752fdca0af8c31db42c1cf36a0c78b5e3ee0b2ffd62546cbc4c)
            check_type(argname="argument end", value=end, expected_type=type_hints["end"])
            check_type(argname="argument start", value=start, expected_type=type_hints["start"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if end is not None:
            self._values["end"] = end
        if start is not None:
            self._values["start"] = start

    @builtins.property
    def end(self) -> typing.Optional[builtins.str]:
        '''ISO-8601 Datetime to end the downtime.

        Must include a UTC offset of zero. If not provided, the downtime never ends.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/downtime_schedule#end DowntimeSchedule#end}
        '''
        result = self._values.get("end")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def start(self) -> typing.Optional[builtins.str]:
        '''ISO-8601 Datetime to start the downtime.

        Must include a UTC offset of zero. If not provided, the downtime starts the moment it is created.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/downtime_schedule#start DowntimeSchedule#start}
        '''
        result = self._values.get("start")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DowntimeScheduleOneTimeSchedule(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DowntimeScheduleOneTimeScheduleOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.downtimeSchedule.DowntimeScheduleOneTimeScheduleOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f1e6b7b3b7de266ab7cac1e2a196902d610fe2ce6c787fe77f521c177b1cffbf)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetEnd")
    def reset_end(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnd", []))

    @jsii.member(jsii_name="resetStart")
    def reset_start(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStart", []))

    @builtins.property
    @jsii.member(jsii_name="endInput")
    def end_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "endInput"))

    @builtins.property
    @jsii.member(jsii_name="startInput")
    def start_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "startInput"))

    @builtins.property
    @jsii.member(jsii_name="end")
    def end(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "end"))

    @end.setter
    def end(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2fc451d56073c9a9aee9eea87396955fcf6c5c79bc2166f5b7ab64e9afb7bc76)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "end", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="start")
    def start(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "start"))

    @start.setter
    def start(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__94228bebf7382cf576a7d54de433d09c63a5904bf3457c2de62b77a2473f86c1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "start", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DowntimeScheduleOneTimeSchedule]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DowntimeScheduleOneTimeSchedule]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DowntimeScheduleOneTimeSchedule]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__de973058929cb4a383a5e7f06e85c7a48b7dda5d6462aa698df95a0d5442f37e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.downtimeSchedule.DowntimeScheduleRecurringSchedule",
    jsii_struct_bases=[],
    name_mapping={"recurrence": "recurrence", "timezone": "timezone"},
)
class DowntimeScheduleRecurringSchedule:
    def __init__(
        self,
        *,
        recurrence: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DowntimeScheduleRecurringScheduleRecurrence", typing.Dict[builtins.str, typing.Any]]]]] = None,
        timezone: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param recurrence: recurrence block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/downtime_schedule#recurrence DowntimeSchedule#recurrence}
        :param timezone: The timezone in which to schedule the downtime. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/downtime_schedule#timezone DowntimeSchedule#timezone}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d4b671b1fa7ddcc524f32faa41f3665f18dcb2fa5aa363a646fcaac94cd83a52)
            check_type(argname="argument recurrence", value=recurrence, expected_type=type_hints["recurrence"])
            check_type(argname="argument timezone", value=timezone, expected_type=type_hints["timezone"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if recurrence is not None:
            self._values["recurrence"] = recurrence
        if timezone is not None:
            self._values["timezone"] = timezone

    @builtins.property
    def recurrence(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DowntimeScheduleRecurringScheduleRecurrence"]]]:
        '''recurrence block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/downtime_schedule#recurrence DowntimeSchedule#recurrence}
        '''
        result = self._values.get("recurrence")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DowntimeScheduleRecurringScheduleRecurrence"]]], result)

    @builtins.property
    def timezone(self) -> typing.Optional[builtins.str]:
        '''The timezone in which to schedule the downtime.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/downtime_schedule#timezone DowntimeSchedule#timezone}
        '''
        result = self._values.get("timezone")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DowntimeScheduleRecurringSchedule(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DowntimeScheduleRecurringScheduleOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.downtimeSchedule.DowntimeScheduleRecurringScheduleOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__28b8810cf7dfb650e3019277a4d87abb842bbf23064c92bdcc019290ca259416)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putRecurrence")
    def put_recurrence(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DowntimeScheduleRecurringScheduleRecurrence", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a11564e493a8d4a64242e67e70cc6608ba3d6063bda2ecb4b464013f93044dda)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putRecurrence", [value]))

    @jsii.member(jsii_name="resetRecurrence")
    def reset_recurrence(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRecurrence", []))

    @jsii.member(jsii_name="resetTimezone")
    def reset_timezone(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimezone", []))

    @builtins.property
    @jsii.member(jsii_name="recurrence")
    def recurrence(self) -> "DowntimeScheduleRecurringScheduleRecurrenceList":
        return typing.cast("DowntimeScheduleRecurringScheduleRecurrenceList", jsii.get(self, "recurrence"))

    @builtins.property
    @jsii.member(jsii_name="recurrenceInput")
    def recurrence_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DowntimeScheduleRecurringScheduleRecurrence"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DowntimeScheduleRecurringScheduleRecurrence"]]], jsii.get(self, "recurrenceInput"))

    @builtins.property
    @jsii.member(jsii_name="timezoneInput")
    def timezone_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "timezoneInput"))

    @builtins.property
    @jsii.member(jsii_name="timezone")
    def timezone(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "timezone"))

    @timezone.setter
    def timezone(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ff63429bce5f2e07e1aadc601432955dbdbfeeb9cbb1cf011195d60754925dd3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timezone", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DowntimeScheduleRecurringSchedule]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DowntimeScheduleRecurringSchedule]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DowntimeScheduleRecurringSchedule]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0fb6907382d73d22860aba48f23632a1ad72b66dea57ca190b949a60312f3142)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.downtimeSchedule.DowntimeScheduleRecurringScheduleRecurrence",
    jsii_struct_bases=[],
    name_mapping={"duration": "duration", "rrule": "rrule", "start": "start"},
)
class DowntimeScheduleRecurringScheduleRecurrence:
    def __init__(
        self,
        *,
        duration: builtins.str,
        rrule: builtins.str,
        start: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param duration: The length of the downtime. Must begin with an integer and end with one of 'm', 'h', d', or 'w'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/downtime_schedule#duration DowntimeSchedule#duration}
        :param rrule: The ``RRULE`` standard for defining recurring events. For example, to have a recurring event on the first day of each month, set the type to ``rrule`` and set the ``FREQ`` to ``MONTHLY`` and ``BYMONTHDAY`` to ``1``. Most common ``rrule`` options from the `iCalendar Spec <https://tools.ietf.org/html/rfc5545>`_ are supported. **Note**: Attributes specifying the duration in ``RRULE`` are not supported (for example, ``DTSTART``, ``DTEND``, ``DURATION``). More examples available in this `downtime guide <https://docs.datadoghq.com/monitors/guide/suppress-alert-with-downtimes/?tab=api>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/downtime_schedule#rrule DowntimeSchedule#rrule}
        :param start: ISO-8601 Datetime to start the downtime. Must not include a UTC offset. If not provided, the downtime starts the moment it is created. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/downtime_schedule#start DowntimeSchedule#start}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__13a3bc5af5cf602547d0bf2e72c7699aba53b9259e240adef401ec28fb684dd7)
            check_type(argname="argument duration", value=duration, expected_type=type_hints["duration"])
            check_type(argname="argument rrule", value=rrule, expected_type=type_hints["rrule"])
            check_type(argname="argument start", value=start, expected_type=type_hints["start"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "duration": duration,
            "rrule": rrule,
        }
        if start is not None:
            self._values["start"] = start

    @builtins.property
    def duration(self) -> builtins.str:
        '''The length of the downtime.

        Must begin with an integer and end with one of 'm', 'h', d', or 'w'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/downtime_schedule#duration DowntimeSchedule#duration}
        '''
        result = self._values.get("duration")
        assert result is not None, "Required property 'duration' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def rrule(self) -> builtins.str:
        '''The ``RRULE`` standard for defining recurring events.

        For example, to have a recurring event on the first day of each month, set the type to ``rrule`` and set the ``FREQ`` to ``MONTHLY`` and ``BYMONTHDAY`` to ``1``. Most common ``rrule`` options from the `iCalendar Spec <https://tools.ietf.org/html/rfc5545>`_ are supported.  **Note**: Attributes specifying the duration in ``RRULE`` are not supported (for example, ``DTSTART``, ``DTEND``, ``DURATION``). More examples available in this `downtime guide <https://docs.datadoghq.com/monitors/guide/suppress-alert-with-downtimes/?tab=api>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/downtime_schedule#rrule DowntimeSchedule#rrule}
        '''
        result = self._values.get("rrule")
        assert result is not None, "Required property 'rrule' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def start(self) -> typing.Optional[builtins.str]:
        '''ISO-8601 Datetime to start the downtime.

        Must not include a UTC offset. If not provided, the downtime starts the moment it is created.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/downtime_schedule#start DowntimeSchedule#start}
        '''
        result = self._values.get("start")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DowntimeScheduleRecurringScheduleRecurrence(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DowntimeScheduleRecurringScheduleRecurrenceList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.downtimeSchedule.DowntimeScheduleRecurringScheduleRecurrenceList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5809a6830551dd5e6bc0b290fbc98de2ade91a8c3c30618b4a7c6d7332f434c1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DowntimeScheduleRecurringScheduleRecurrenceOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf01bb2a40c0d26692535059e4ac964746b397cd217cd4eead6e28f98620ec85)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DowntimeScheduleRecurringScheduleRecurrenceOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b9210291974746e9c79628b73303622b574308869bf34e69896b1d3c958b867)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9cc288dfcbbc4d25c49448aacb8131d23a87424ca09c2704aaffbb1e78763be8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__71460db3fcdfe8c7b2a9250a5ba8e779afc9b31b41d8064087f789eea0b142a5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DowntimeScheduleRecurringScheduleRecurrence]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DowntimeScheduleRecurringScheduleRecurrence]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DowntimeScheduleRecurringScheduleRecurrence]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a5b1655d2449eed599a95f3eee1656ab5d80e7cf2346081fa52872575548f8f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DowntimeScheduleRecurringScheduleRecurrenceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.downtimeSchedule.DowntimeScheduleRecurringScheduleRecurrenceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__36556b77a94d04cbcefaffa919603339b9b54a036b7f5c9a32fcfd9409620e1b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetStart")
    def reset_start(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStart", []))

    @builtins.property
    @jsii.member(jsii_name="durationInput")
    def duration_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "durationInput"))

    @builtins.property
    @jsii.member(jsii_name="rruleInput")
    def rrule_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "rruleInput"))

    @builtins.property
    @jsii.member(jsii_name="startInput")
    def start_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "startInput"))

    @builtins.property
    @jsii.member(jsii_name="duration")
    def duration(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "duration"))

    @duration.setter
    def duration(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__90c1001e01ef15a67ee129b9595266fa16b3de151c1e027063d9a875a8abaffa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "duration", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="rrule")
    def rrule(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "rrule"))

    @rrule.setter
    def rrule(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ffb7d972a97392c76641301341cca14a3e51264ffbe8e586d81640f6e6cd0e1a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rrule", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="start")
    def start(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "start"))

    @start.setter
    def start(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__19773170419ffb0413a576d4e1c3d3d4d1e94ecd38224c568d38d75b12860449)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "start", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DowntimeScheduleRecurringScheduleRecurrence]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DowntimeScheduleRecurringScheduleRecurrence]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DowntimeScheduleRecurringScheduleRecurrence]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1110d4c3059be99b776867608680af1be0b662a317c62a02559ba8f49a89c244)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "DowntimeSchedule",
    "DowntimeScheduleConfig",
    "DowntimeScheduleMonitorIdentifier",
    "DowntimeScheduleMonitorIdentifierOutputReference",
    "DowntimeScheduleOneTimeSchedule",
    "DowntimeScheduleOneTimeScheduleOutputReference",
    "DowntimeScheduleRecurringSchedule",
    "DowntimeScheduleRecurringScheduleOutputReference",
    "DowntimeScheduleRecurringScheduleRecurrence",
    "DowntimeScheduleRecurringScheduleRecurrenceList",
    "DowntimeScheduleRecurringScheduleRecurrenceOutputReference",
]

publication.publish()

def _typecheckingstub__b1e223b7f836a1025ca3ed2b8a6af63f5471e59bfad2d879943995dc339d5f06(
    scope_: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    scope: builtins.str,
    display_timezone: typing.Optional[builtins.str] = None,
    message: typing.Optional[builtins.str] = None,
    monitor_identifier: typing.Optional[typing.Union[DowntimeScheduleMonitorIdentifier, typing.Dict[builtins.str, typing.Any]]] = None,
    mute_first_recovery_notification: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    notify_end_states: typing.Optional[typing.Sequence[builtins.str]] = None,
    notify_end_types: typing.Optional[typing.Sequence[builtins.str]] = None,
    one_time_schedule: typing.Optional[typing.Union[DowntimeScheduleOneTimeSchedule, typing.Dict[builtins.str, typing.Any]]] = None,
    recurring_schedule: typing.Optional[typing.Union[DowntimeScheduleRecurringSchedule, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__e4adb358eccdf3554f7c40d543384c64c7e749abd809cb9db2bf377866d3a1b9(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cdb564afb1f323db76e8e46840b85a150d43beeac31756cd2c2db9b11d253f70(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__310dbd787e59f7bc0f0454c43804e81dc28bdc4c8be205f6e30f6c926f2ad9b8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__abe7b14734c552f1345c524ef7bda59f2fce266e7c006373dd0d8be474b6bc60(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a6fa67bf8ef5ea4ba616af4da5d7144634983855aef68927b377f65e8a66f0e(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2a1e72a169641cf13c6b016e417393349468700ee7d888800301056ee618030(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa6413f2ab552c5a353ec1ebc71e290018ca4bad1619620b798b6da41ae6e018(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be8f37b7e144b3b157d68716ade513f5f4e102bb555d119705598fe0e47f26ed(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    scope: builtins.str,
    display_timezone: typing.Optional[builtins.str] = None,
    message: typing.Optional[builtins.str] = None,
    monitor_identifier: typing.Optional[typing.Union[DowntimeScheduleMonitorIdentifier, typing.Dict[builtins.str, typing.Any]]] = None,
    mute_first_recovery_notification: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    notify_end_states: typing.Optional[typing.Sequence[builtins.str]] = None,
    notify_end_types: typing.Optional[typing.Sequence[builtins.str]] = None,
    one_time_schedule: typing.Optional[typing.Union[DowntimeScheduleOneTimeSchedule, typing.Dict[builtins.str, typing.Any]]] = None,
    recurring_schedule: typing.Optional[typing.Union[DowntimeScheduleRecurringSchedule, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3dfa52cde1ae41461718af62317420cfd67c1d0ac0686a76c10926fd403f41e(
    *,
    monitor_id: typing.Optional[jsii.Number] = None,
    monitor_tags: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__009625c84c9df8d2ceb339ab76b194a9f5bdba69b2f30ce35bce1c76d68ff755(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cfaa047aa152e323ecd7c6a726a7daa2c55de4206d901a67667fed9234ae8f82(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cad44e5a459baf8bcb87c1a6d07c9425d886ecba27edbcf4be02c8e862c7be98(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cefdc0b1da0bae0179435261302c2100bd712e9838ea92e4ea03e7e87b70f24d(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DowntimeScheduleMonitorIdentifier]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25a01102831bf752fdca0af8c31db42c1cf36a0c78b5e3ee0b2ffd62546cbc4c(
    *,
    end: typing.Optional[builtins.str] = None,
    start: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1e6b7b3b7de266ab7cac1e2a196902d610fe2ce6c787fe77f521c177b1cffbf(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2fc451d56073c9a9aee9eea87396955fcf6c5c79bc2166f5b7ab64e9afb7bc76(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94228bebf7382cf576a7d54de433d09c63a5904bf3457c2de62b77a2473f86c1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de973058929cb4a383a5e7f06e85c7a48b7dda5d6462aa698df95a0d5442f37e(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DowntimeScheduleOneTimeSchedule]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4b671b1fa7ddcc524f32faa41f3665f18dcb2fa5aa363a646fcaac94cd83a52(
    *,
    recurrence: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DowntimeScheduleRecurringScheduleRecurrence, typing.Dict[builtins.str, typing.Any]]]]] = None,
    timezone: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28b8810cf7dfb650e3019277a4d87abb842bbf23064c92bdcc019290ca259416(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a11564e493a8d4a64242e67e70cc6608ba3d6063bda2ecb4b464013f93044dda(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DowntimeScheduleRecurringScheduleRecurrence, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff63429bce5f2e07e1aadc601432955dbdbfeeb9cbb1cf011195d60754925dd3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0fb6907382d73d22860aba48f23632a1ad72b66dea57ca190b949a60312f3142(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DowntimeScheduleRecurringSchedule]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13a3bc5af5cf602547d0bf2e72c7699aba53b9259e240adef401ec28fb684dd7(
    *,
    duration: builtins.str,
    rrule: builtins.str,
    start: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5809a6830551dd5e6bc0b290fbc98de2ade91a8c3c30618b4a7c6d7332f434c1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf01bb2a40c0d26692535059e4ac964746b397cd217cd4eead6e28f98620ec85(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b9210291974746e9c79628b73303622b574308869bf34e69896b1d3c958b867(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9cc288dfcbbc4d25c49448aacb8131d23a87424ca09c2704aaffbb1e78763be8(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71460db3fcdfe8c7b2a9250a5ba8e779afc9b31b41d8064087f789eea0b142a5(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a5b1655d2449eed599a95f3eee1656ab5d80e7cf2346081fa52872575548f8f(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DowntimeScheduleRecurringScheduleRecurrence]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36556b77a94d04cbcefaffa919603339b9b54a036b7f5c9a32fcfd9409620e1b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__90c1001e01ef15a67ee129b9595266fa16b3de151c1e027063d9a875a8abaffa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ffb7d972a97392c76641301341cca14a3e51264ffbe8e586d81640f6e6cd0e1a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19773170419ffb0413a576d4e1c3d3d4d1e94ecd38224c568d38d75b12860449(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1110d4c3059be99b776867608680af1be0b662a317c62a02559ba8f49a89c244(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DowntimeScheduleRecurringScheduleRecurrence]],
) -> None:
    """Type checking stubs"""
    pass
