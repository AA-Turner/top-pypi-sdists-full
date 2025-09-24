r'''
# `newrelic_monitor_downtime`

Refer to the Terraform Registry for docs: [`newrelic_monitor_downtime`](https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/monitor_downtime).
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


class MonitorDowntime(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.monitorDowntime.MonitorDowntime",
):
    '''Represents a {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/monitor_downtime newrelic_monitor_downtime}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        end_time: builtins.str,
        mode: builtins.str,
        name: builtins.str,
        start_time: builtins.str,
        time_zone: builtins.str,
        account_id: typing.Optional[jsii.Number] = None,
        end_repeat: typing.Optional[typing.Union["MonitorDowntimeEndRepeat", typing.Dict[builtins.str, typing.Any]]] = None,
        frequency: typing.Optional[typing.Union["MonitorDowntimeFrequency", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        maintenance_days: typing.Optional[typing.Sequence[builtins.str]] = None,
        monitor_guids: typing.Optional[typing.Sequence[builtins.str]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/monitor_downtime newrelic_monitor_downtime} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param end_time: A datetime stamp signifying the end of the Monitor Downtime. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/monitor_downtime#end_time MonitorDowntime#end_time}
        :param mode: An identifier of the type of Monitor Downtime to be created. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/monitor_downtime#mode MonitorDowntime#mode}
        :param name: A name to identify the Monitor Downtime to be created. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/monitor_downtime#name MonitorDowntime#name}
        :param start_time: A datetime stamp signifying the start of the Monitor Downtime. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/monitor_downtime#start_time MonitorDowntime#start_time}
        :param time_zone: The timezone that applies to the Monitor Downtime schedule. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/monitor_downtime#time_zone MonitorDowntime#time_zone}
        :param account_id: The ID of the New Relic account in which the Monitor Downtime shall be created. Defaults to the ``account_id`` in the provider{} configuration if not specified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/monitor_downtime#account_id MonitorDowntime#account_id}
        :param end_repeat: end_repeat block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/monitor_downtime#end_repeat MonitorDowntime#end_repeat}
        :param frequency: frequency block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/monitor_downtime#frequency MonitorDowntime#frequency}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/monitor_downtime#id MonitorDowntime#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param maintenance_days: A list of maintenance days to be included with the created weekly Monitor Downtime. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/monitor_downtime#maintenance_days MonitorDowntime#maintenance_days}
        :param monitor_guids: A list of GUIDs of monitors, to which the created Monitor Downtime shall be applied. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/monitor_downtime#monitor_guids MonitorDowntime#monitor_guids}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__998dc455f7d424101eb83ce80ce6b46207c4f22f8e9e50dd3458074dd11cdc1c)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = MonitorDowntimeConfig(
            end_time=end_time,
            mode=mode,
            name=name,
            start_time=start_time,
            time_zone=time_zone,
            account_id=account_id,
            end_repeat=end_repeat,
            frequency=frequency,
            id=id,
            maintenance_days=maintenance_days,
            monitor_guids=monitor_guids,
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
        '''Generates CDKTF code for importing a MonitorDowntime resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the MonitorDowntime to import.
        :param import_from_id: The id of the existing MonitorDowntime that should be imported. Refer to the {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/monitor_downtime#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the MonitorDowntime to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e2dd140d8df2894170237aeb5304817911602a0bc9358bb80b9dd2c781cf8e7a)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putEndRepeat")
    def put_end_repeat(
        self,
        *,
        on_date: typing.Optional[builtins.str] = None,
        on_repeat: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param on_date: A date, on which the Monitor Downtime's repeat cycle is expected to end. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/monitor_downtime#on_date MonitorDowntime#on_date}
        :param on_repeat: Number of repetitions after which the Monitor Downtime's repeat cycle is expected to end. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/monitor_downtime#on_repeat MonitorDowntime#on_repeat}
        '''
        value = MonitorDowntimeEndRepeat(on_date=on_date, on_repeat=on_repeat)

        return typing.cast(None, jsii.invoke(self, "putEndRepeat", [value]))

    @jsii.member(jsii_name="putFrequency")
    def put_frequency(
        self,
        *,
        days_of_month: typing.Optional[typing.Sequence[jsii.Number]] = None,
        days_of_week: typing.Optional[typing.Union["MonitorDowntimeFrequencyDaysOfWeek", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param days_of_month: A numerical list of days of a month on which the Monitor Downtime is scheduled to run. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/monitor_downtime#days_of_month MonitorDowntime#days_of_month}
        :param days_of_week: days_of_week block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/monitor_downtime#days_of_week MonitorDowntime#days_of_week}
        '''
        value = MonitorDowntimeFrequency(
            days_of_month=days_of_month, days_of_week=days_of_week
        )

        return typing.cast(None, jsii.invoke(self, "putFrequency", [value]))

    @jsii.member(jsii_name="resetAccountId")
    def reset_account_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAccountId", []))

    @jsii.member(jsii_name="resetEndRepeat")
    def reset_end_repeat(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEndRepeat", []))

    @jsii.member(jsii_name="resetFrequency")
    def reset_frequency(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFrequency", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetMaintenanceDays")
    def reset_maintenance_days(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaintenanceDays", []))

    @jsii.member(jsii_name="resetMonitorGuids")
    def reset_monitor_guids(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMonitorGuids", []))

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
    @jsii.member(jsii_name="endRepeat")
    def end_repeat(self) -> "MonitorDowntimeEndRepeatOutputReference":
        return typing.cast("MonitorDowntimeEndRepeatOutputReference", jsii.get(self, "endRepeat"))

    @builtins.property
    @jsii.member(jsii_name="frequency")
    def frequency(self) -> "MonitorDowntimeFrequencyOutputReference":
        return typing.cast("MonitorDowntimeFrequencyOutputReference", jsii.get(self, "frequency"))

    @builtins.property
    @jsii.member(jsii_name="accountIdInput")
    def account_id_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "accountIdInput"))

    @builtins.property
    @jsii.member(jsii_name="endRepeatInput")
    def end_repeat_input(self) -> typing.Optional["MonitorDowntimeEndRepeat"]:
        return typing.cast(typing.Optional["MonitorDowntimeEndRepeat"], jsii.get(self, "endRepeatInput"))

    @builtins.property
    @jsii.member(jsii_name="endTimeInput")
    def end_time_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "endTimeInput"))

    @builtins.property
    @jsii.member(jsii_name="frequencyInput")
    def frequency_input(self) -> typing.Optional["MonitorDowntimeFrequency"]:
        return typing.cast(typing.Optional["MonitorDowntimeFrequency"], jsii.get(self, "frequencyInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="maintenanceDaysInput")
    def maintenance_days_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "maintenanceDaysInput"))

    @builtins.property
    @jsii.member(jsii_name="modeInput")
    def mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "modeInput"))

    @builtins.property
    @jsii.member(jsii_name="monitorGuidsInput")
    def monitor_guids_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "monitorGuidsInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="startTimeInput")
    def start_time_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "startTimeInput"))

    @builtins.property
    @jsii.member(jsii_name="timeZoneInput")
    def time_zone_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "timeZoneInput"))

    @builtins.property
    @jsii.member(jsii_name="accountId")
    def account_id(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "accountId"))

    @account_id.setter
    def account_id(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5805b89badb000114fa2ccc4f8fae4f1f948f49b8f0015f150ff5da04b299c08)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accountId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="endTime")
    def end_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "endTime"))

    @end_time.setter
    def end_time(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c2e2e7a769a690133a973d708c5d52e39b37af41cf560443b9f192401b05a061)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "endTime", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc75c5a671cfe8f282a76d7c4010054d614030d0c3d9ef893947c39d5121f315)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maintenanceDays")
    def maintenance_days(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "maintenanceDays"))

    @maintenance_days.setter
    def maintenance_days(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5718109134a5ecc43c611ad3460706da61db77ef508e96dfb9789e9f87df5c2d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maintenanceDays", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="mode")
    def mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mode"))

    @mode.setter
    def mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__99226c9a736012675e85b6a0fdddc595e38ae40d49fd0830ba11330c6cbe7e49)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="monitorGuids")
    def monitor_guids(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "monitorGuids"))

    @monitor_guids.setter
    def monitor_guids(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ccfba3e9fc8a75be5df21dc574abe68bd07aa65ae8b8ecc2dd2952eda44a7f58)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "monitorGuids", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__25f5aef9bab79b87809f16f2c6fa865e6fd371bc47ebff4ceedd3f25821f4a79)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="startTime")
    def start_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "startTime"))

    @start_time.setter
    def start_time(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__296fb51f2f56ea54c48680594ef66d70cbdf9ee23b9a6eae196f0b8b42af2117)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "startTime", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="timeZone")
    def time_zone(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "timeZone"))

    @time_zone.setter
    def time_zone(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__34e0b89deaa5c70aa09170da3c98ad74ed4d0642b934ad5d1344e80e8d96c340)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timeZone", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-newrelic.monitorDowntime.MonitorDowntimeConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "end_time": "endTime",
        "mode": "mode",
        "name": "name",
        "start_time": "startTime",
        "time_zone": "timeZone",
        "account_id": "accountId",
        "end_repeat": "endRepeat",
        "frequency": "frequency",
        "id": "id",
        "maintenance_days": "maintenanceDays",
        "monitor_guids": "monitorGuids",
    },
)
class MonitorDowntimeConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        end_time: builtins.str,
        mode: builtins.str,
        name: builtins.str,
        start_time: builtins.str,
        time_zone: builtins.str,
        account_id: typing.Optional[jsii.Number] = None,
        end_repeat: typing.Optional[typing.Union["MonitorDowntimeEndRepeat", typing.Dict[builtins.str, typing.Any]]] = None,
        frequency: typing.Optional[typing.Union["MonitorDowntimeFrequency", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        maintenance_days: typing.Optional[typing.Sequence[builtins.str]] = None,
        monitor_guids: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param end_time: A datetime stamp signifying the end of the Monitor Downtime. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/monitor_downtime#end_time MonitorDowntime#end_time}
        :param mode: An identifier of the type of Monitor Downtime to be created. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/monitor_downtime#mode MonitorDowntime#mode}
        :param name: A name to identify the Monitor Downtime to be created. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/monitor_downtime#name MonitorDowntime#name}
        :param start_time: A datetime stamp signifying the start of the Monitor Downtime. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/monitor_downtime#start_time MonitorDowntime#start_time}
        :param time_zone: The timezone that applies to the Monitor Downtime schedule. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/monitor_downtime#time_zone MonitorDowntime#time_zone}
        :param account_id: The ID of the New Relic account in which the Monitor Downtime shall be created. Defaults to the ``account_id`` in the provider{} configuration if not specified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/monitor_downtime#account_id MonitorDowntime#account_id}
        :param end_repeat: end_repeat block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/monitor_downtime#end_repeat MonitorDowntime#end_repeat}
        :param frequency: frequency block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/monitor_downtime#frequency MonitorDowntime#frequency}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/monitor_downtime#id MonitorDowntime#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param maintenance_days: A list of maintenance days to be included with the created weekly Monitor Downtime. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/monitor_downtime#maintenance_days MonitorDowntime#maintenance_days}
        :param monitor_guids: A list of GUIDs of monitors, to which the created Monitor Downtime shall be applied. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/monitor_downtime#monitor_guids MonitorDowntime#monitor_guids}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(end_repeat, dict):
            end_repeat = MonitorDowntimeEndRepeat(**end_repeat)
        if isinstance(frequency, dict):
            frequency = MonitorDowntimeFrequency(**frequency)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0299d69fbabb9404bf4adcac372fbea05addd3e16179e3454d3eacea15f20d00)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument end_time", value=end_time, expected_type=type_hints["end_time"])
            check_type(argname="argument mode", value=mode, expected_type=type_hints["mode"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument start_time", value=start_time, expected_type=type_hints["start_time"])
            check_type(argname="argument time_zone", value=time_zone, expected_type=type_hints["time_zone"])
            check_type(argname="argument account_id", value=account_id, expected_type=type_hints["account_id"])
            check_type(argname="argument end_repeat", value=end_repeat, expected_type=type_hints["end_repeat"])
            check_type(argname="argument frequency", value=frequency, expected_type=type_hints["frequency"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument maintenance_days", value=maintenance_days, expected_type=type_hints["maintenance_days"])
            check_type(argname="argument monitor_guids", value=monitor_guids, expected_type=type_hints["monitor_guids"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "end_time": end_time,
            "mode": mode,
            "name": name,
            "start_time": start_time,
            "time_zone": time_zone,
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
        if account_id is not None:
            self._values["account_id"] = account_id
        if end_repeat is not None:
            self._values["end_repeat"] = end_repeat
        if frequency is not None:
            self._values["frequency"] = frequency
        if id is not None:
            self._values["id"] = id
        if maintenance_days is not None:
            self._values["maintenance_days"] = maintenance_days
        if monitor_guids is not None:
            self._values["monitor_guids"] = monitor_guids

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
    def end_time(self) -> builtins.str:
        '''A datetime stamp signifying the end of the Monitor Downtime.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/monitor_downtime#end_time MonitorDowntime#end_time}
        '''
        result = self._values.get("end_time")
        assert result is not None, "Required property 'end_time' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def mode(self) -> builtins.str:
        '''An identifier of the type of Monitor Downtime to be created.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/monitor_downtime#mode MonitorDowntime#mode}
        '''
        result = self._values.get("mode")
        assert result is not None, "Required property 'mode' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''A name to identify the Monitor Downtime to be created.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/monitor_downtime#name MonitorDowntime#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def start_time(self) -> builtins.str:
        '''A datetime stamp signifying the start of the Monitor Downtime.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/monitor_downtime#start_time MonitorDowntime#start_time}
        '''
        result = self._values.get("start_time")
        assert result is not None, "Required property 'start_time' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def time_zone(self) -> builtins.str:
        '''The timezone that applies to the Monitor Downtime schedule.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/monitor_downtime#time_zone MonitorDowntime#time_zone}
        '''
        result = self._values.get("time_zone")
        assert result is not None, "Required property 'time_zone' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def account_id(self) -> typing.Optional[jsii.Number]:
        '''The ID of the New Relic account in which the Monitor Downtime shall be created.

        Defaults to the ``account_id`` in the provider{} configuration if not specified.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/monitor_downtime#account_id MonitorDowntime#account_id}
        '''
        result = self._values.get("account_id")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def end_repeat(self) -> typing.Optional["MonitorDowntimeEndRepeat"]:
        '''end_repeat block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/monitor_downtime#end_repeat MonitorDowntime#end_repeat}
        '''
        result = self._values.get("end_repeat")
        return typing.cast(typing.Optional["MonitorDowntimeEndRepeat"], result)

    @builtins.property
    def frequency(self) -> typing.Optional["MonitorDowntimeFrequency"]:
        '''frequency block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/monitor_downtime#frequency MonitorDowntime#frequency}
        '''
        result = self._values.get("frequency")
        return typing.cast(typing.Optional["MonitorDowntimeFrequency"], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/monitor_downtime#id MonitorDowntime#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def maintenance_days(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of maintenance days to be included with the created weekly Monitor Downtime.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/monitor_downtime#maintenance_days MonitorDowntime#maintenance_days}
        '''
        result = self._values.get("maintenance_days")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def monitor_guids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of GUIDs of monitors, to which the created Monitor Downtime shall be applied.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/monitor_downtime#monitor_guids MonitorDowntime#monitor_guids}
        '''
        result = self._values.get("monitor_guids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MonitorDowntimeConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-newrelic.monitorDowntime.MonitorDowntimeEndRepeat",
    jsii_struct_bases=[],
    name_mapping={"on_date": "onDate", "on_repeat": "onRepeat"},
)
class MonitorDowntimeEndRepeat:
    def __init__(
        self,
        *,
        on_date: typing.Optional[builtins.str] = None,
        on_repeat: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param on_date: A date, on which the Monitor Downtime's repeat cycle is expected to end. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/monitor_downtime#on_date MonitorDowntime#on_date}
        :param on_repeat: Number of repetitions after which the Monitor Downtime's repeat cycle is expected to end. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/monitor_downtime#on_repeat MonitorDowntime#on_repeat}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__74bd9c03b5fe81f9bf4e6fe656a65c61fbf8f676809b9547f32b91e376dd1d41)
            check_type(argname="argument on_date", value=on_date, expected_type=type_hints["on_date"])
            check_type(argname="argument on_repeat", value=on_repeat, expected_type=type_hints["on_repeat"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if on_date is not None:
            self._values["on_date"] = on_date
        if on_repeat is not None:
            self._values["on_repeat"] = on_repeat

    @builtins.property
    def on_date(self) -> typing.Optional[builtins.str]:
        '''A date, on which the Monitor Downtime's repeat cycle is expected to end.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/monitor_downtime#on_date MonitorDowntime#on_date}
        '''
        result = self._values.get("on_date")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def on_repeat(self) -> typing.Optional[jsii.Number]:
        '''Number of repetitions after which the Monitor Downtime's repeat cycle is expected to end.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/monitor_downtime#on_repeat MonitorDowntime#on_repeat}
        '''
        result = self._values.get("on_repeat")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MonitorDowntimeEndRepeat(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MonitorDowntimeEndRepeatOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.monitorDowntime.MonitorDowntimeEndRepeatOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__aed459309ae92c5820e512e7fbacea40f8c6a611a9031dc519bcc911c5251ce9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetOnDate")
    def reset_on_date(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOnDate", []))

    @jsii.member(jsii_name="resetOnRepeat")
    def reset_on_repeat(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOnRepeat", []))

    @builtins.property
    @jsii.member(jsii_name="onDateInput")
    def on_date_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "onDateInput"))

    @builtins.property
    @jsii.member(jsii_name="onRepeatInput")
    def on_repeat_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "onRepeatInput"))

    @builtins.property
    @jsii.member(jsii_name="onDate")
    def on_date(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "onDate"))

    @on_date.setter
    def on_date(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4685e2fb00957315de1b183dd5249f235edb13dea56c5c807d800ebe30e23545)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "onDate", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="onRepeat")
    def on_repeat(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "onRepeat"))

    @on_repeat.setter
    def on_repeat(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__48ace76ae31f84fb2c9adbf9c38a51ad55d26736f657bfb2998f6ca52621e1bf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "onRepeat", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[MonitorDowntimeEndRepeat]:
        return typing.cast(typing.Optional[MonitorDowntimeEndRepeat], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[MonitorDowntimeEndRepeat]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b5dfbf3d0c4392bd5a8c731d2aad5a04dcfe867a22ead7210af9a7e9478c8dac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-newrelic.monitorDowntime.MonitorDowntimeFrequency",
    jsii_struct_bases=[],
    name_mapping={"days_of_month": "daysOfMonth", "days_of_week": "daysOfWeek"},
)
class MonitorDowntimeFrequency:
    def __init__(
        self,
        *,
        days_of_month: typing.Optional[typing.Sequence[jsii.Number]] = None,
        days_of_week: typing.Optional[typing.Union["MonitorDowntimeFrequencyDaysOfWeek", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param days_of_month: A numerical list of days of a month on which the Monitor Downtime is scheduled to run. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/monitor_downtime#days_of_month MonitorDowntime#days_of_month}
        :param days_of_week: days_of_week block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/monitor_downtime#days_of_week MonitorDowntime#days_of_week}
        '''
        if isinstance(days_of_week, dict):
            days_of_week = MonitorDowntimeFrequencyDaysOfWeek(**days_of_week)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a0ee04e47e0e9d6dbbcf8dac376724d6a8ea24e5e8bd4c19f8ac3cc073da0f96)
            check_type(argname="argument days_of_month", value=days_of_month, expected_type=type_hints["days_of_month"])
            check_type(argname="argument days_of_week", value=days_of_week, expected_type=type_hints["days_of_week"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if days_of_month is not None:
            self._values["days_of_month"] = days_of_month
        if days_of_week is not None:
            self._values["days_of_week"] = days_of_week

    @builtins.property
    def days_of_month(self) -> typing.Optional[typing.List[jsii.Number]]:
        '''A numerical list of days of a month on which the Monitor Downtime is scheduled to run.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/monitor_downtime#days_of_month MonitorDowntime#days_of_month}
        '''
        result = self._values.get("days_of_month")
        return typing.cast(typing.Optional[typing.List[jsii.Number]], result)

    @builtins.property
    def days_of_week(self) -> typing.Optional["MonitorDowntimeFrequencyDaysOfWeek"]:
        '''days_of_week block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/monitor_downtime#days_of_week MonitorDowntime#days_of_week}
        '''
        result = self._values.get("days_of_week")
        return typing.cast(typing.Optional["MonitorDowntimeFrequencyDaysOfWeek"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MonitorDowntimeFrequency(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-newrelic.monitorDowntime.MonitorDowntimeFrequencyDaysOfWeek",
    jsii_struct_bases=[],
    name_mapping={"ordinal_day_of_month": "ordinalDayOfMonth", "week_day": "weekDay"},
)
class MonitorDowntimeFrequencyDaysOfWeek:
    def __init__(
        self,
        *,
        ordinal_day_of_month: builtins.str,
        week_day: builtins.str,
    ) -> None:
        '''
        :param ordinal_day_of_month: An occurrence of the day selected within the month. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/monitor_downtime#ordinal_day_of_month MonitorDowntime#ordinal_day_of_month}
        :param week_day: The day of the week on which the Monitor Downtime would run. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/monitor_downtime#week_day MonitorDowntime#week_day}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf7592de7ad276a459285f0b26de794971c22a6f5ca5575a08782186338e2963)
            check_type(argname="argument ordinal_day_of_month", value=ordinal_day_of_month, expected_type=type_hints["ordinal_day_of_month"])
            check_type(argname="argument week_day", value=week_day, expected_type=type_hints["week_day"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "ordinal_day_of_month": ordinal_day_of_month,
            "week_day": week_day,
        }

    @builtins.property
    def ordinal_day_of_month(self) -> builtins.str:
        '''An occurrence of the day selected within the month.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/monitor_downtime#ordinal_day_of_month MonitorDowntime#ordinal_day_of_month}
        '''
        result = self._values.get("ordinal_day_of_month")
        assert result is not None, "Required property 'ordinal_day_of_month' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def week_day(self) -> builtins.str:
        '''The day of the week on which the Monitor Downtime would run.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/monitor_downtime#week_day MonitorDowntime#week_day}
        '''
        result = self._values.get("week_day")
        assert result is not None, "Required property 'week_day' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MonitorDowntimeFrequencyDaysOfWeek(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MonitorDowntimeFrequencyDaysOfWeekOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.monitorDowntime.MonitorDowntimeFrequencyDaysOfWeekOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__306dfcde49621d07a30201a6639b683e97ec5ce794f46f2aee74729795d83b91)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="ordinalDayOfMonthInput")
    def ordinal_day_of_month_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ordinalDayOfMonthInput"))

    @builtins.property
    @jsii.member(jsii_name="weekDayInput")
    def week_day_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "weekDayInput"))

    @builtins.property
    @jsii.member(jsii_name="ordinalDayOfMonth")
    def ordinal_day_of_month(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ordinalDayOfMonth"))

    @ordinal_day_of_month.setter
    def ordinal_day_of_month(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6168003508b00a8257e82a16a52e5f6f4695a0355dec02e168c1c48e15a15333)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ordinalDayOfMonth", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="weekDay")
    def week_day(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "weekDay"))

    @week_day.setter
    def week_day(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f8c48381959e62519278f3c41d6b2acef93b0b1e04c46dbfec38af0ee376d3e1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "weekDay", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[MonitorDowntimeFrequencyDaysOfWeek]:
        return typing.cast(typing.Optional[MonitorDowntimeFrequencyDaysOfWeek], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MonitorDowntimeFrequencyDaysOfWeek],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b494679e3f4927f95b1c611a7c9908914de084832117d27a2e7b9a24836ab1d3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class MonitorDowntimeFrequencyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.monitorDowntime.MonitorDowntimeFrequencyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__184d9821fb1ae17a0056c540b7f382fa7d5fb5f343749be190e5cae9629b5886)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putDaysOfWeek")
    def put_days_of_week(
        self,
        *,
        ordinal_day_of_month: builtins.str,
        week_day: builtins.str,
    ) -> None:
        '''
        :param ordinal_day_of_month: An occurrence of the day selected within the month. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/monitor_downtime#ordinal_day_of_month MonitorDowntime#ordinal_day_of_month}
        :param week_day: The day of the week on which the Monitor Downtime would run. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/monitor_downtime#week_day MonitorDowntime#week_day}
        '''
        value = MonitorDowntimeFrequencyDaysOfWeek(
            ordinal_day_of_month=ordinal_day_of_month, week_day=week_day
        )

        return typing.cast(None, jsii.invoke(self, "putDaysOfWeek", [value]))

    @jsii.member(jsii_name="resetDaysOfMonth")
    def reset_days_of_month(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDaysOfMonth", []))

    @jsii.member(jsii_name="resetDaysOfWeek")
    def reset_days_of_week(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDaysOfWeek", []))

    @builtins.property
    @jsii.member(jsii_name="daysOfWeek")
    def days_of_week(self) -> MonitorDowntimeFrequencyDaysOfWeekOutputReference:
        return typing.cast(MonitorDowntimeFrequencyDaysOfWeekOutputReference, jsii.get(self, "daysOfWeek"))

    @builtins.property
    @jsii.member(jsii_name="daysOfMonthInput")
    def days_of_month_input(self) -> typing.Optional[typing.List[jsii.Number]]:
        return typing.cast(typing.Optional[typing.List[jsii.Number]], jsii.get(self, "daysOfMonthInput"))

    @builtins.property
    @jsii.member(jsii_name="daysOfWeekInput")
    def days_of_week_input(self) -> typing.Optional[MonitorDowntimeFrequencyDaysOfWeek]:
        return typing.cast(typing.Optional[MonitorDowntimeFrequencyDaysOfWeek], jsii.get(self, "daysOfWeekInput"))

    @builtins.property
    @jsii.member(jsii_name="daysOfMonth")
    def days_of_month(self) -> typing.List[jsii.Number]:
        return typing.cast(typing.List[jsii.Number], jsii.get(self, "daysOfMonth"))

    @days_of_month.setter
    def days_of_month(self, value: typing.List[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b3d5e7dfce5deb9520a578ff7307472e3c1b21f39989aa8360ff8ecd74448486)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "daysOfMonth", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[MonitorDowntimeFrequency]:
        return typing.cast(typing.Optional[MonitorDowntimeFrequency], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[MonitorDowntimeFrequency]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a89ffbe3bb24dc1b2be4966faaa5e6e8cc815ecca304c230e809c6fd9d32d8b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "MonitorDowntime",
    "MonitorDowntimeConfig",
    "MonitorDowntimeEndRepeat",
    "MonitorDowntimeEndRepeatOutputReference",
    "MonitorDowntimeFrequency",
    "MonitorDowntimeFrequencyDaysOfWeek",
    "MonitorDowntimeFrequencyDaysOfWeekOutputReference",
    "MonitorDowntimeFrequencyOutputReference",
]

publication.publish()

def _typecheckingstub__998dc455f7d424101eb83ce80ce6b46207c4f22f8e9e50dd3458074dd11cdc1c(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    end_time: builtins.str,
    mode: builtins.str,
    name: builtins.str,
    start_time: builtins.str,
    time_zone: builtins.str,
    account_id: typing.Optional[jsii.Number] = None,
    end_repeat: typing.Optional[typing.Union[MonitorDowntimeEndRepeat, typing.Dict[builtins.str, typing.Any]]] = None,
    frequency: typing.Optional[typing.Union[MonitorDowntimeFrequency, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    maintenance_days: typing.Optional[typing.Sequence[builtins.str]] = None,
    monitor_guids: typing.Optional[typing.Sequence[builtins.str]] = None,
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

def _typecheckingstub__e2dd140d8df2894170237aeb5304817911602a0bc9358bb80b9dd2c781cf8e7a(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5805b89badb000114fa2ccc4f8fae4f1f948f49b8f0015f150ff5da04b299c08(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2e2e7a769a690133a973d708c5d52e39b37af41cf560443b9f192401b05a061(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc75c5a671cfe8f282a76d7c4010054d614030d0c3d9ef893947c39d5121f315(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5718109134a5ecc43c611ad3460706da61db77ef508e96dfb9789e9f87df5c2d(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99226c9a736012675e85b6a0fdddc595e38ae40d49fd0830ba11330c6cbe7e49(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ccfba3e9fc8a75be5df21dc574abe68bd07aa65ae8b8ecc2dd2952eda44a7f58(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25f5aef9bab79b87809f16f2c6fa865e6fd371bc47ebff4ceedd3f25821f4a79(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__296fb51f2f56ea54c48680594ef66d70cbdf9ee23b9a6eae196f0b8b42af2117(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34e0b89deaa5c70aa09170da3c98ad74ed4d0642b934ad5d1344e80e8d96c340(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0299d69fbabb9404bf4adcac372fbea05addd3e16179e3454d3eacea15f20d00(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    end_time: builtins.str,
    mode: builtins.str,
    name: builtins.str,
    start_time: builtins.str,
    time_zone: builtins.str,
    account_id: typing.Optional[jsii.Number] = None,
    end_repeat: typing.Optional[typing.Union[MonitorDowntimeEndRepeat, typing.Dict[builtins.str, typing.Any]]] = None,
    frequency: typing.Optional[typing.Union[MonitorDowntimeFrequency, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    maintenance_days: typing.Optional[typing.Sequence[builtins.str]] = None,
    monitor_guids: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74bd9c03b5fe81f9bf4e6fe656a65c61fbf8f676809b9547f32b91e376dd1d41(
    *,
    on_date: typing.Optional[builtins.str] = None,
    on_repeat: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aed459309ae92c5820e512e7fbacea40f8c6a611a9031dc519bcc911c5251ce9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4685e2fb00957315de1b183dd5249f235edb13dea56c5c807d800ebe30e23545(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__48ace76ae31f84fb2c9adbf9c38a51ad55d26736f657bfb2998f6ca52621e1bf(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b5dfbf3d0c4392bd5a8c731d2aad5a04dcfe867a22ead7210af9a7e9478c8dac(
    value: typing.Optional[MonitorDowntimeEndRepeat],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0ee04e47e0e9d6dbbcf8dac376724d6a8ea24e5e8bd4c19f8ac3cc073da0f96(
    *,
    days_of_month: typing.Optional[typing.Sequence[jsii.Number]] = None,
    days_of_week: typing.Optional[typing.Union[MonitorDowntimeFrequencyDaysOfWeek, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf7592de7ad276a459285f0b26de794971c22a6f5ca5575a08782186338e2963(
    *,
    ordinal_day_of_month: builtins.str,
    week_day: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__306dfcde49621d07a30201a6639b683e97ec5ce794f46f2aee74729795d83b91(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6168003508b00a8257e82a16a52e5f6f4695a0355dec02e168c1c48e15a15333(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f8c48381959e62519278f3c41d6b2acef93b0b1e04c46dbfec38af0ee376d3e1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b494679e3f4927f95b1c611a7c9908914de084832117d27a2e7b9a24836ab1d3(
    value: typing.Optional[MonitorDowntimeFrequencyDaysOfWeek],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__184d9821fb1ae17a0056c540b7f382fa7d5fb5f343749be190e5cae9629b5886(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3d5e7dfce5deb9520a578ff7307472e3c1b21f39989aa8360ff8ecd74448486(
    value: typing.List[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a89ffbe3bb24dc1b2be4966faaa5e6e8cc815ecca304c230e809c6fd9d32d8b(
    value: typing.Optional[MonitorDowntimeFrequency],
) -> None:
    """Type checking stubs"""
    pass
