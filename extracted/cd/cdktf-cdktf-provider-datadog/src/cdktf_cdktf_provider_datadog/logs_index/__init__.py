r'''
# `datadog_logs_index`

Refer to the Terraform Registry for docs: [`datadog_logs_index`](https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_index).
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


class LogsIndex(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.logsIndex.LogsIndex",
):
    '''Represents a {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_index datadog_logs_index}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        filter: typing.Union["LogsIndexFilter", typing.Dict[builtins.str, typing.Any]],
        name: builtins.str,
        daily_limit: typing.Optional[jsii.Number] = None,
        daily_limit_reset: typing.Optional[typing.Union["LogsIndexDailyLimitReset", typing.Dict[builtins.str, typing.Any]]] = None,
        daily_limit_warning_threshold_percentage: typing.Optional[jsii.Number] = None,
        disable_daily_limit: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        exclusion_filter: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["LogsIndexExclusionFilter", typing.Dict[builtins.str, typing.Any]]]]] = None,
        flex_retention_days: typing.Optional[jsii.Number] = None,
        id: typing.Optional[builtins.str] = None,
        retention_days: typing.Optional[jsii.Number] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_index datadog_logs_index} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param filter: filter block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_index#filter LogsIndex#filter}
        :param name: The name of the index. Index names cannot be modified after creation. If this value is changed, a new index will be created. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_index#name LogsIndex#name}
        :param daily_limit: The number of log events you can send in this index per day before you are rate-limited. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_index#daily_limit LogsIndex#daily_limit}
        :param daily_limit_reset: daily_limit_reset block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_index#daily_limit_reset LogsIndex#daily_limit_reset}
        :param daily_limit_warning_threshold_percentage: A percentage threshold of the daily quota at which a Datadog warning event is generated. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_index#daily_limit_warning_threshold_percentage LogsIndex#daily_limit_warning_threshold_percentage}
        :param disable_daily_limit: If true, sets the daily_limit value to null and the index is not limited on a daily basis (any specified daily_limit value in the request is ignored). If false or omitted, the index's current daily_limit is maintained. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_index#disable_daily_limit LogsIndex#disable_daily_limit}
        :param exclusion_filter: exclusion_filter block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_index#exclusion_filter LogsIndex#exclusion_filter}
        :param flex_retention_days: The total number of days logs are stored in Standard and Flex Tier before being deleted from the index. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_index#flex_retention_days LogsIndex#flex_retention_days}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_index#id LogsIndex#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param retention_days: The number of days logs are stored in Standard Tier before aging into the Flex Tier or being deleted from the index. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_index#retention_days LogsIndex#retention_days}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__71f852daee8491727704e10b0e4871b055d008960915e26261bfb9423e0a35c6)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = LogsIndexConfig(
            filter=filter,
            name=name,
            daily_limit=daily_limit,
            daily_limit_reset=daily_limit_reset,
            daily_limit_warning_threshold_percentage=daily_limit_warning_threshold_percentage,
            disable_daily_limit=disable_daily_limit,
            exclusion_filter=exclusion_filter,
            flex_retention_days=flex_retention_days,
            id=id,
            retention_days=retention_days,
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
        '''Generates CDKTF code for importing a LogsIndex resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the LogsIndex to import.
        :param import_from_id: The id of the existing LogsIndex that should be imported. Refer to the {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_index#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the LogsIndex to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d9e0a9066cdaa1c81fc56f11b8a2a5eac4da6574c16bbbb247b7eaf546fd986)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putDailyLimitReset")
    def put_daily_limit_reset(
        self,
        *,
        reset_time: builtins.str,
        reset_utc_offset: builtins.str,
    ) -> None:
        '''
        :param reset_time: String in ``HH:00`` format representing the time of day the daily limit should be reset. The hours must be between 00 and 23 (inclusive). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_index#reset_time LogsIndex#reset_time}
        :param reset_utc_offset: String in ``(-|+)HH:00`` format representing the UTC offset to apply to the given reset time. The hours must be between -12 and +14 (inclusive). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_index#reset_utc_offset LogsIndex#reset_utc_offset}
        '''
        value = LogsIndexDailyLimitReset(
            reset_time=reset_time, reset_utc_offset=reset_utc_offset
        )

        return typing.cast(None, jsii.invoke(self, "putDailyLimitReset", [value]))

    @jsii.member(jsii_name="putExclusionFilter")
    def put_exclusion_filter(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["LogsIndexExclusionFilter", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__21bdc520645a99859bc64d692da76244958adc905cbfb6274070c55248330685)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putExclusionFilter", [value]))

    @jsii.member(jsii_name="putFilter")
    def put_filter(self, *, query: builtins.str) -> None:
        '''
        :param query: Logs filter criteria. Only logs matching this filter criteria are considered for this index. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_index#query LogsIndex#query}
        '''
        value = LogsIndexFilter(query=query)

        return typing.cast(None, jsii.invoke(self, "putFilter", [value]))

    @jsii.member(jsii_name="resetDailyLimit")
    def reset_daily_limit(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDailyLimit", []))

    @jsii.member(jsii_name="resetDailyLimitReset")
    def reset_daily_limit_reset(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDailyLimitReset", []))

    @jsii.member(jsii_name="resetDailyLimitWarningThresholdPercentage")
    def reset_daily_limit_warning_threshold_percentage(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDailyLimitWarningThresholdPercentage", []))

    @jsii.member(jsii_name="resetDisableDailyLimit")
    def reset_disable_daily_limit(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDisableDailyLimit", []))

    @jsii.member(jsii_name="resetExclusionFilter")
    def reset_exclusion_filter(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExclusionFilter", []))

    @jsii.member(jsii_name="resetFlexRetentionDays")
    def reset_flex_retention_days(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFlexRetentionDays", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetRetentionDays")
    def reset_retention_days(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRetentionDays", []))

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
    @jsii.member(jsii_name="dailyLimitReset")
    def daily_limit_reset(self) -> "LogsIndexDailyLimitResetOutputReference":
        return typing.cast("LogsIndexDailyLimitResetOutputReference", jsii.get(self, "dailyLimitReset"))

    @builtins.property
    @jsii.member(jsii_name="exclusionFilter")
    def exclusion_filter(self) -> "LogsIndexExclusionFilterList":
        return typing.cast("LogsIndexExclusionFilterList", jsii.get(self, "exclusionFilter"))

    @builtins.property
    @jsii.member(jsii_name="filter")
    def filter(self) -> "LogsIndexFilterOutputReference":
        return typing.cast("LogsIndexFilterOutputReference", jsii.get(self, "filter"))

    @builtins.property
    @jsii.member(jsii_name="dailyLimitInput")
    def daily_limit_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "dailyLimitInput"))

    @builtins.property
    @jsii.member(jsii_name="dailyLimitResetInput")
    def daily_limit_reset_input(self) -> typing.Optional["LogsIndexDailyLimitReset"]:
        return typing.cast(typing.Optional["LogsIndexDailyLimitReset"], jsii.get(self, "dailyLimitResetInput"))

    @builtins.property
    @jsii.member(jsii_name="dailyLimitWarningThresholdPercentageInput")
    def daily_limit_warning_threshold_percentage_input(
        self,
    ) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "dailyLimitWarningThresholdPercentageInput"))

    @builtins.property
    @jsii.member(jsii_name="disableDailyLimitInput")
    def disable_daily_limit_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "disableDailyLimitInput"))

    @builtins.property
    @jsii.member(jsii_name="exclusionFilterInput")
    def exclusion_filter_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["LogsIndexExclusionFilter"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["LogsIndexExclusionFilter"]]], jsii.get(self, "exclusionFilterInput"))

    @builtins.property
    @jsii.member(jsii_name="filterInput")
    def filter_input(self) -> typing.Optional["LogsIndexFilter"]:
        return typing.cast(typing.Optional["LogsIndexFilter"], jsii.get(self, "filterInput"))

    @builtins.property
    @jsii.member(jsii_name="flexRetentionDaysInput")
    def flex_retention_days_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "flexRetentionDaysInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="retentionDaysInput")
    def retention_days_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "retentionDaysInput"))

    @builtins.property
    @jsii.member(jsii_name="dailyLimit")
    def daily_limit(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "dailyLimit"))

    @daily_limit.setter
    def daily_limit(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__accad69d28a25a268f7ce6ef06ac37819407953a60e7608c3addd74f4e0c3e94)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dailyLimit", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dailyLimitWarningThresholdPercentage")
    def daily_limit_warning_threshold_percentage(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "dailyLimitWarningThresholdPercentage"))

    @daily_limit_warning_threshold_percentage.setter
    def daily_limit_warning_threshold_percentage(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a6fd62e68747cecf533a256f3812b81b06ce7a148adf4fb84acd5137251beaad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dailyLimitWarningThresholdPercentage", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="disableDailyLimit")
    def disable_daily_limit(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "disableDailyLimit"))

    @disable_daily_limit.setter
    def disable_daily_limit(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6291776b47ec5c150af340c8ac5bedeb2d33d0ec533b8238ed52f022cf7cf9b2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "disableDailyLimit", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="flexRetentionDays")
    def flex_retention_days(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "flexRetentionDays"))

    @flex_retention_days.setter
    def flex_retention_days(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d9ead1fc6f249e876b4efc15cf40d930334bd465f3493852eef70b65f2d39c5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "flexRetentionDays", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c00d4df189661fcb8521b494c5a40536dd3945e1aa16a2d83eeab7224ff12c85)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a808a3ffbf4a8f95f879a8e3cb8d8bb97cb8413d623ff79cb10b0bac90773675)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="retentionDays")
    def retention_days(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "retentionDays"))

    @retention_days.setter
    def retention_days(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d006febdb62fbe6f5e50d54ae55b0a53bb5328f4a7c45bfb0349bd46573400fd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "retentionDays", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.logsIndex.LogsIndexConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "filter": "filter",
        "name": "name",
        "daily_limit": "dailyLimit",
        "daily_limit_reset": "dailyLimitReset",
        "daily_limit_warning_threshold_percentage": "dailyLimitWarningThresholdPercentage",
        "disable_daily_limit": "disableDailyLimit",
        "exclusion_filter": "exclusionFilter",
        "flex_retention_days": "flexRetentionDays",
        "id": "id",
        "retention_days": "retentionDays",
    },
)
class LogsIndexConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        filter: typing.Union["LogsIndexFilter", typing.Dict[builtins.str, typing.Any]],
        name: builtins.str,
        daily_limit: typing.Optional[jsii.Number] = None,
        daily_limit_reset: typing.Optional[typing.Union["LogsIndexDailyLimitReset", typing.Dict[builtins.str, typing.Any]]] = None,
        daily_limit_warning_threshold_percentage: typing.Optional[jsii.Number] = None,
        disable_daily_limit: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        exclusion_filter: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["LogsIndexExclusionFilter", typing.Dict[builtins.str, typing.Any]]]]] = None,
        flex_retention_days: typing.Optional[jsii.Number] = None,
        id: typing.Optional[builtins.str] = None,
        retention_days: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param filter: filter block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_index#filter LogsIndex#filter}
        :param name: The name of the index. Index names cannot be modified after creation. If this value is changed, a new index will be created. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_index#name LogsIndex#name}
        :param daily_limit: The number of log events you can send in this index per day before you are rate-limited. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_index#daily_limit LogsIndex#daily_limit}
        :param daily_limit_reset: daily_limit_reset block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_index#daily_limit_reset LogsIndex#daily_limit_reset}
        :param daily_limit_warning_threshold_percentage: A percentage threshold of the daily quota at which a Datadog warning event is generated. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_index#daily_limit_warning_threshold_percentage LogsIndex#daily_limit_warning_threshold_percentage}
        :param disable_daily_limit: If true, sets the daily_limit value to null and the index is not limited on a daily basis (any specified daily_limit value in the request is ignored). If false or omitted, the index's current daily_limit is maintained. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_index#disable_daily_limit LogsIndex#disable_daily_limit}
        :param exclusion_filter: exclusion_filter block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_index#exclusion_filter LogsIndex#exclusion_filter}
        :param flex_retention_days: The total number of days logs are stored in Standard and Flex Tier before being deleted from the index. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_index#flex_retention_days LogsIndex#flex_retention_days}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_index#id LogsIndex#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param retention_days: The number of days logs are stored in Standard Tier before aging into the Flex Tier or being deleted from the index. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_index#retention_days LogsIndex#retention_days}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(filter, dict):
            filter = LogsIndexFilter(**filter)
        if isinstance(daily_limit_reset, dict):
            daily_limit_reset = LogsIndexDailyLimitReset(**daily_limit_reset)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__946a0ac0e909c20d1423e2dc1c2fda7695d9907b4761f9e04a808c53d98c47ed)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument filter", value=filter, expected_type=type_hints["filter"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument daily_limit", value=daily_limit, expected_type=type_hints["daily_limit"])
            check_type(argname="argument daily_limit_reset", value=daily_limit_reset, expected_type=type_hints["daily_limit_reset"])
            check_type(argname="argument daily_limit_warning_threshold_percentage", value=daily_limit_warning_threshold_percentage, expected_type=type_hints["daily_limit_warning_threshold_percentage"])
            check_type(argname="argument disable_daily_limit", value=disable_daily_limit, expected_type=type_hints["disable_daily_limit"])
            check_type(argname="argument exclusion_filter", value=exclusion_filter, expected_type=type_hints["exclusion_filter"])
            check_type(argname="argument flex_retention_days", value=flex_retention_days, expected_type=type_hints["flex_retention_days"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument retention_days", value=retention_days, expected_type=type_hints["retention_days"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "filter": filter,
            "name": name,
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
        if daily_limit is not None:
            self._values["daily_limit"] = daily_limit
        if daily_limit_reset is not None:
            self._values["daily_limit_reset"] = daily_limit_reset
        if daily_limit_warning_threshold_percentage is not None:
            self._values["daily_limit_warning_threshold_percentage"] = daily_limit_warning_threshold_percentage
        if disable_daily_limit is not None:
            self._values["disable_daily_limit"] = disable_daily_limit
        if exclusion_filter is not None:
            self._values["exclusion_filter"] = exclusion_filter
        if flex_retention_days is not None:
            self._values["flex_retention_days"] = flex_retention_days
        if id is not None:
            self._values["id"] = id
        if retention_days is not None:
            self._values["retention_days"] = retention_days

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
    def filter(self) -> "LogsIndexFilter":
        '''filter block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_index#filter LogsIndex#filter}
        '''
        result = self._values.get("filter")
        assert result is not None, "Required property 'filter' is missing"
        return typing.cast("LogsIndexFilter", result)

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of the index.

        Index names cannot be modified after creation. If this value is changed, a new index will be created.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_index#name LogsIndex#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def daily_limit(self) -> typing.Optional[jsii.Number]:
        '''The number of log events you can send in this index per day before you are rate-limited.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_index#daily_limit LogsIndex#daily_limit}
        '''
        result = self._values.get("daily_limit")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def daily_limit_reset(self) -> typing.Optional["LogsIndexDailyLimitReset"]:
        '''daily_limit_reset block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_index#daily_limit_reset LogsIndex#daily_limit_reset}
        '''
        result = self._values.get("daily_limit_reset")
        return typing.cast(typing.Optional["LogsIndexDailyLimitReset"], result)

    @builtins.property
    def daily_limit_warning_threshold_percentage(self) -> typing.Optional[jsii.Number]:
        '''A percentage threshold of the daily quota at which a Datadog warning event is generated.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_index#daily_limit_warning_threshold_percentage LogsIndex#daily_limit_warning_threshold_percentage}
        '''
        result = self._values.get("daily_limit_warning_threshold_percentage")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def disable_daily_limit(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If true, sets the daily_limit value to null and the index is not limited on a daily basis (any specified daily_limit value in the request is ignored).

        If false or omitted, the index's current daily_limit is maintained.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_index#disable_daily_limit LogsIndex#disable_daily_limit}
        '''
        result = self._values.get("disable_daily_limit")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def exclusion_filter(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["LogsIndexExclusionFilter"]]]:
        '''exclusion_filter block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_index#exclusion_filter LogsIndex#exclusion_filter}
        '''
        result = self._values.get("exclusion_filter")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["LogsIndexExclusionFilter"]]], result)

    @builtins.property
    def flex_retention_days(self) -> typing.Optional[jsii.Number]:
        '''The total number of days logs are stored in Standard and Flex Tier before being deleted from the index.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_index#flex_retention_days LogsIndex#flex_retention_days}
        '''
        result = self._values.get("flex_retention_days")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_index#id LogsIndex#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def retention_days(self) -> typing.Optional[jsii.Number]:
        '''The number of days logs are stored in Standard Tier before aging into the Flex Tier or being deleted from the index.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_index#retention_days LogsIndex#retention_days}
        '''
        result = self._values.get("retention_days")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LogsIndexConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.logsIndex.LogsIndexDailyLimitReset",
    jsii_struct_bases=[],
    name_mapping={"reset_time": "resetTime", "reset_utc_offset": "resetUtcOffset"},
)
class LogsIndexDailyLimitReset:
    def __init__(
        self,
        *,
        reset_time: builtins.str,
        reset_utc_offset: builtins.str,
    ) -> None:
        '''
        :param reset_time: String in ``HH:00`` format representing the time of day the daily limit should be reset. The hours must be between 00 and 23 (inclusive). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_index#reset_time LogsIndex#reset_time}
        :param reset_utc_offset: String in ``(-|+)HH:00`` format representing the UTC offset to apply to the given reset time. The hours must be between -12 and +14 (inclusive). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_index#reset_utc_offset LogsIndex#reset_utc_offset}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e2d7b2e4df0041fe0d8f1ddbfd490bcc69de4d2294f5979c89c436e2b601a78d)
            check_type(argname="argument reset_time", value=reset_time, expected_type=type_hints["reset_time"])
            check_type(argname="argument reset_utc_offset", value=reset_utc_offset, expected_type=type_hints["reset_utc_offset"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "reset_time": reset_time,
            "reset_utc_offset": reset_utc_offset,
        }

    @builtins.property
    def reset_time(self) -> builtins.str:
        '''String in ``HH:00`` format representing the time of day the daily limit should be reset.

        The hours must be between 00 and 23 (inclusive).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_index#reset_time LogsIndex#reset_time}
        '''
        result = self._values.get("reset_time")
        assert result is not None, "Required property 'reset_time' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def reset_utc_offset(self) -> builtins.str:
        '''String in ``(-|+)HH:00`` format representing the UTC offset to apply to the given reset time.

        The hours must be between -12 and +14 (inclusive).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_index#reset_utc_offset LogsIndex#reset_utc_offset}
        '''
        result = self._values.get("reset_utc_offset")
        assert result is not None, "Required property 'reset_utc_offset' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LogsIndexDailyLimitReset(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LogsIndexDailyLimitResetOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.logsIndex.LogsIndexDailyLimitResetOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__837db8a1a841a6f532114328ed6bfeb9573ff0e1e7f7c4cfdb17c78a6eb960e9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="resetTimeInput")
    def reset_time_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "resetTimeInput"))

    @builtins.property
    @jsii.member(jsii_name="resetUtcOffsetInput")
    def reset_utc_offset_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "resetUtcOffsetInput"))

    @builtins.property
    @jsii.member(jsii_name="resetTime")
    def reset_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resetTime"))

    @reset_time.setter
    def reset_time(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__78b832986249fff1841a9a72bb4c10e27d3075a2a8f8b1ee07a6d534fe076085)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resetTime", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resetUtcOffset")
    def reset_utc_offset(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resetUtcOffset"))

    @reset_utc_offset.setter
    def reset_utc_offset(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__321df926afa51cfdcc30d715e8f43d5db9a109c4c38f5aa53cfda31c2cc43e08)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resetUtcOffset", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[LogsIndexDailyLimitReset]:
        return typing.cast(typing.Optional[LogsIndexDailyLimitReset], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[LogsIndexDailyLimitReset]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__851be5ea85451197a0150b54a92c351909a202a83c92d2538205c7fb89db6286)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.logsIndex.LogsIndexExclusionFilter",
    jsii_struct_bases=[],
    name_mapping={"filter": "filter", "is_enabled": "isEnabled", "name": "name"},
)
class LogsIndexExclusionFilter:
    def __init__(
        self,
        *,
        filter: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["LogsIndexExclusionFilterFilter", typing.Dict[builtins.str, typing.Any]]]]] = None,
        is_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param filter: filter block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_index#filter LogsIndex#filter}
        :param is_enabled: A boolean stating if the exclusion is active or not. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_index#is_enabled LogsIndex#is_enabled}
        :param name: The name of the exclusion filter. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_index#name LogsIndex#name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9030c94ba3ee97c1ced66e7da3c53e6ae4fa8ba7086b25a93bd7340b62daea61)
            check_type(argname="argument filter", value=filter, expected_type=type_hints["filter"])
            check_type(argname="argument is_enabled", value=is_enabled, expected_type=type_hints["is_enabled"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if filter is not None:
            self._values["filter"] = filter
        if is_enabled is not None:
            self._values["is_enabled"] = is_enabled
        if name is not None:
            self._values["name"] = name

    @builtins.property
    def filter(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["LogsIndexExclusionFilterFilter"]]]:
        '''filter block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_index#filter LogsIndex#filter}
        '''
        result = self._values.get("filter")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["LogsIndexExclusionFilterFilter"]]], result)

    @builtins.property
    def is_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''A boolean stating if the exclusion is active or not.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_index#is_enabled LogsIndex#is_enabled}
        '''
        result = self._values.get("is_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the exclusion filter.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_index#name LogsIndex#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LogsIndexExclusionFilter(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.logsIndex.LogsIndexExclusionFilterFilter",
    jsii_struct_bases=[],
    name_mapping={"query": "query", "sample_rate": "sampleRate"},
)
class LogsIndexExclusionFilterFilter:
    def __init__(
        self,
        *,
        query: typing.Optional[builtins.str] = None,
        sample_rate: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param query: Only logs matching the filter criteria and the query of the parent index will be considered for this exclusion filter. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_index#query LogsIndex#query}
        :param sample_rate: The fraction of logs excluded by the exclusion filter, when active. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_index#sample_rate LogsIndex#sample_rate}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc2c38b49a445abd9e6676ee5afd97577d38d7ea035d3e1da48dc72ffa22742e)
            check_type(argname="argument query", value=query, expected_type=type_hints["query"])
            check_type(argname="argument sample_rate", value=sample_rate, expected_type=type_hints["sample_rate"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if query is not None:
            self._values["query"] = query
        if sample_rate is not None:
            self._values["sample_rate"] = sample_rate

    @builtins.property
    def query(self) -> typing.Optional[builtins.str]:
        '''Only logs matching the filter criteria and the query of the parent index will be considered for this exclusion filter.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_index#query LogsIndex#query}
        '''
        result = self._values.get("query")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sample_rate(self) -> typing.Optional[jsii.Number]:
        '''The fraction of logs excluded by the exclusion filter, when active.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_index#sample_rate LogsIndex#sample_rate}
        '''
        result = self._values.get("sample_rate")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LogsIndexExclusionFilterFilter(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LogsIndexExclusionFilterFilterList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.logsIndex.LogsIndexExclusionFilterFilterList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d01c4bffa323b8dcdd472abcbb95a1eaeeb45e689878b30d1cf4dc423dfdb8fb)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "LogsIndexExclusionFilterFilterOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b6080527d06d54c344cf2127788d1b95eb66fcc186b133be18992ee1e8362d91)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("LogsIndexExclusionFilterFilterOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__055c04eb74440b1747a57b00eb24ed322258224da228b385200af96860aaec12)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a722f7f9e9cac346e810749fc452f192ef91c9a5bd1fbe37d425d4a952ab6ebc)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1810abd395637940c58627f4f92cfe805f0c99f92bacacd1a87102a85d4b0e08)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LogsIndexExclusionFilterFilter]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LogsIndexExclusionFilterFilter]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LogsIndexExclusionFilterFilter]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a13b638028be997e1046a7d9ca51b3fa1c05f3483abbb278c54b8bb53ded2e9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class LogsIndexExclusionFilterFilterOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.logsIndex.LogsIndexExclusionFilterFilterOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a803379cb25e8f0fa60a2a234db67fa3bb20f6b4d55fef2708e541def3a6ff9e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetQuery")
    def reset_query(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetQuery", []))

    @jsii.member(jsii_name="resetSampleRate")
    def reset_sample_rate(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSampleRate", []))

    @builtins.property
    @jsii.member(jsii_name="queryInput")
    def query_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "queryInput"))

    @builtins.property
    @jsii.member(jsii_name="sampleRateInput")
    def sample_rate_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "sampleRateInput"))

    @builtins.property
    @jsii.member(jsii_name="query")
    def query(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "query"))

    @query.setter
    def query(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__33524b52e2acc065618e8d3f88869cef3d5eeb55bd7870163da735d9ab27f311)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "query", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sampleRate")
    def sample_rate(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "sampleRate"))

    @sample_rate.setter
    def sample_rate(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f192de4c6291989c63126856a2299d443032653716654db4eabb3620c810b126)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sampleRate", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LogsIndexExclusionFilterFilter]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LogsIndexExclusionFilterFilter]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LogsIndexExclusionFilterFilter]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__557fb882550c9fdef0ff190f10dad8e159b5280da17c315b6187e5a0faf9bfe3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class LogsIndexExclusionFilterList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.logsIndex.LogsIndexExclusionFilterList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__533ad228fec881999382e5eae8ab1a8d13b89a66386b269e683a8f323aff11e5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "LogsIndexExclusionFilterOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f5598705427641f3cddfa8c7927db41a783be7215fa0447a0b49f4600ba31717)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("LogsIndexExclusionFilterOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ed102344f292f7f930d8655d9f1dacba43cc8074f1b1dd79399e2f961d2e2924)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6c600db63266e4fb4995cfd1083fa5b2d46400ef33909b90d0b037adba2e31be)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a4312cba2bcf9bdc37cd89daed27ccec80b80daa0d82b415a5c03ebc6b9e95de)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LogsIndexExclusionFilter]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LogsIndexExclusionFilter]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LogsIndexExclusionFilter]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c18d89c6ed9bf18f76129d576d38c39aaf53d8646b61fa8d6286cd47d3c03057)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class LogsIndexExclusionFilterOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.logsIndex.LogsIndexExclusionFilterOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c2ee3d4dcb8b7e84a36697e8eab8cceb521ba6089b0ddc4843ea4238c57e3f29)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putFilter")
    def put_filter(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[LogsIndexExclusionFilterFilter, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bd1ce3d556314c2e3a015ad555d2fee45a3ad230376b3c132ea8c1ac11256c01)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putFilter", [value]))

    @jsii.member(jsii_name="resetFilter")
    def reset_filter(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFilter", []))

    @jsii.member(jsii_name="resetIsEnabled")
    def reset_is_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIsEnabled", []))

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @builtins.property
    @jsii.member(jsii_name="filter")
    def filter(self) -> LogsIndexExclusionFilterFilterList:
        return typing.cast(LogsIndexExclusionFilterFilterList, jsii.get(self, "filter"))

    @builtins.property
    @jsii.member(jsii_name="filterInput")
    def filter_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LogsIndexExclusionFilterFilter]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LogsIndexExclusionFilterFilter]]], jsii.get(self, "filterInput"))

    @builtins.property
    @jsii.member(jsii_name="isEnabledInput")
    def is_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "isEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="isEnabled")
    def is_enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "isEnabled"))

    @is_enabled.setter
    def is_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e28cc4a09691b919e744a3fe0804f53b158b4a4050233fb0998afaeeaf2c17dd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "isEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a7b82766604097dbb4abae78ca6ffc5830343f62201f31abd03c332d2355a365)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LogsIndexExclusionFilter]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LogsIndexExclusionFilter]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LogsIndexExclusionFilter]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a04334291cb70ff013dd08788b4bf6eca114911fa3d4e0e0980c81bb0515daf5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.logsIndex.LogsIndexFilter",
    jsii_struct_bases=[],
    name_mapping={"query": "query"},
)
class LogsIndexFilter:
    def __init__(self, *, query: builtins.str) -> None:
        '''
        :param query: Logs filter criteria. Only logs matching this filter criteria are considered for this index. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_index#query LogsIndex#query}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__46d074c569565f3244a456793ad24d0d4983d5f03fa958b9ba1232f8797da245)
            check_type(argname="argument query", value=query, expected_type=type_hints["query"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "query": query,
        }

    @builtins.property
    def query(self) -> builtins.str:
        '''Logs filter criteria. Only logs matching this filter criteria are considered for this index.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_index#query LogsIndex#query}
        '''
        result = self._values.get("query")
        assert result is not None, "Required property 'query' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LogsIndexFilter(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LogsIndexFilterOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.logsIndex.LogsIndexFilterOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1fc5e3568b4754e6b00d0861c480039a46c0093f379d57030d7773aebf9f781f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="queryInput")
    def query_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "queryInput"))

    @builtins.property
    @jsii.member(jsii_name="query")
    def query(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "query"))

    @query.setter
    def query(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e14218e79ee9a928d2413a19acc297fc5e2f95006876c6bda11b3a7e5258913c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "query", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[LogsIndexFilter]:
        return typing.cast(typing.Optional[LogsIndexFilter], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[LogsIndexFilter]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f9cad348f492f70ad712d8a24330bb7767e5a5665752f19c8cb80754cf88e7ec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "LogsIndex",
    "LogsIndexConfig",
    "LogsIndexDailyLimitReset",
    "LogsIndexDailyLimitResetOutputReference",
    "LogsIndexExclusionFilter",
    "LogsIndexExclusionFilterFilter",
    "LogsIndexExclusionFilterFilterList",
    "LogsIndexExclusionFilterFilterOutputReference",
    "LogsIndexExclusionFilterList",
    "LogsIndexExclusionFilterOutputReference",
    "LogsIndexFilter",
    "LogsIndexFilterOutputReference",
]

publication.publish()

def _typecheckingstub__71f852daee8491727704e10b0e4871b055d008960915e26261bfb9423e0a35c6(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    filter: typing.Union[LogsIndexFilter, typing.Dict[builtins.str, typing.Any]],
    name: builtins.str,
    daily_limit: typing.Optional[jsii.Number] = None,
    daily_limit_reset: typing.Optional[typing.Union[LogsIndexDailyLimitReset, typing.Dict[builtins.str, typing.Any]]] = None,
    daily_limit_warning_threshold_percentage: typing.Optional[jsii.Number] = None,
    disable_daily_limit: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    exclusion_filter: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[LogsIndexExclusionFilter, typing.Dict[builtins.str, typing.Any]]]]] = None,
    flex_retention_days: typing.Optional[jsii.Number] = None,
    id: typing.Optional[builtins.str] = None,
    retention_days: typing.Optional[jsii.Number] = None,
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

def _typecheckingstub__6d9e0a9066cdaa1c81fc56f11b8a2a5eac4da6574c16bbbb247b7eaf546fd986(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__21bdc520645a99859bc64d692da76244958adc905cbfb6274070c55248330685(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[LogsIndexExclusionFilter, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__accad69d28a25a268f7ce6ef06ac37819407953a60e7608c3addd74f4e0c3e94(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a6fd62e68747cecf533a256f3812b81b06ce7a148adf4fb84acd5137251beaad(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6291776b47ec5c150af340c8ac5bedeb2d33d0ec533b8238ed52f022cf7cf9b2(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d9ead1fc6f249e876b4efc15cf40d930334bd465f3493852eef70b65f2d39c5(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c00d4df189661fcb8521b494c5a40536dd3945e1aa16a2d83eeab7224ff12c85(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a808a3ffbf4a8f95f879a8e3cb8d8bb97cb8413d623ff79cb10b0bac90773675(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d006febdb62fbe6f5e50d54ae55b0a53bb5328f4a7c45bfb0349bd46573400fd(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__946a0ac0e909c20d1423e2dc1c2fda7695d9907b4761f9e04a808c53d98c47ed(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    filter: typing.Union[LogsIndexFilter, typing.Dict[builtins.str, typing.Any]],
    name: builtins.str,
    daily_limit: typing.Optional[jsii.Number] = None,
    daily_limit_reset: typing.Optional[typing.Union[LogsIndexDailyLimitReset, typing.Dict[builtins.str, typing.Any]]] = None,
    daily_limit_warning_threshold_percentage: typing.Optional[jsii.Number] = None,
    disable_daily_limit: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    exclusion_filter: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[LogsIndexExclusionFilter, typing.Dict[builtins.str, typing.Any]]]]] = None,
    flex_retention_days: typing.Optional[jsii.Number] = None,
    id: typing.Optional[builtins.str] = None,
    retention_days: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2d7b2e4df0041fe0d8f1ddbfd490bcc69de4d2294f5979c89c436e2b601a78d(
    *,
    reset_time: builtins.str,
    reset_utc_offset: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__837db8a1a841a6f532114328ed6bfeb9573ff0e1e7f7c4cfdb17c78a6eb960e9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78b832986249fff1841a9a72bb4c10e27d3075a2a8f8b1ee07a6d534fe076085(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__321df926afa51cfdcc30d715e8f43d5db9a109c4c38f5aa53cfda31c2cc43e08(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__851be5ea85451197a0150b54a92c351909a202a83c92d2538205c7fb89db6286(
    value: typing.Optional[LogsIndexDailyLimitReset],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9030c94ba3ee97c1ced66e7da3c53e6ae4fa8ba7086b25a93bd7340b62daea61(
    *,
    filter: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[LogsIndexExclusionFilterFilter, typing.Dict[builtins.str, typing.Any]]]]] = None,
    is_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc2c38b49a445abd9e6676ee5afd97577d38d7ea035d3e1da48dc72ffa22742e(
    *,
    query: typing.Optional[builtins.str] = None,
    sample_rate: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d01c4bffa323b8dcdd472abcbb95a1eaeeb45e689878b30d1cf4dc423dfdb8fb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6080527d06d54c344cf2127788d1b95eb66fcc186b133be18992ee1e8362d91(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__055c04eb74440b1747a57b00eb24ed322258224da228b385200af96860aaec12(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a722f7f9e9cac346e810749fc452f192ef91c9a5bd1fbe37d425d4a952ab6ebc(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1810abd395637940c58627f4f92cfe805f0c99f92bacacd1a87102a85d4b0e08(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a13b638028be997e1046a7d9ca51b3fa1c05f3483abbb278c54b8bb53ded2e9(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LogsIndexExclusionFilterFilter]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a803379cb25e8f0fa60a2a234db67fa3bb20f6b4d55fef2708e541def3a6ff9e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33524b52e2acc065618e8d3f88869cef3d5eeb55bd7870163da735d9ab27f311(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f192de4c6291989c63126856a2299d443032653716654db4eabb3620c810b126(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__557fb882550c9fdef0ff190f10dad8e159b5280da17c315b6187e5a0faf9bfe3(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LogsIndexExclusionFilterFilter]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__533ad228fec881999382e5eae8ab1a8d13b89a66386b269e683a8f323aff11e5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5598705427641f3cddfa8c7927db41a783be7215fa0447a0b49f4600ba31717(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed102344f292f7f930d8655d9f1dacba43cc8074f1b1dd79399e2f961d2e2924(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c600db63266e4fb4995cfd1083fa5b2d46400ef33909b90d0b037adba2e31be(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4312cba2bcf9bdc37cd89daed27ccec80b80daa0d82b415a5c03ebc6b9e95de(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c18d89c6ed9bf18f76129d576d38c39aaf53d8646b61fa8d6286cd47d3c03057(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LogsIndexExclusionFilter]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2ee3d4dcb8b7e84a36697e8eab8cceb521ba6089b0ddc4843ea4238c57e3f29(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd1ce3d556314c2e3a015ad555d2fee45a3ad230376b3c132ea8c1ac11256c01(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[LogsIndexExclusionFilterFilter, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e28cc4a09691b919e744a3fe0804f53b158b4a4050233fb0998afaeeaf2c17dd(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a7b82766604097dbb4abae78ca6ffc5830343f62201f31abd03c332d2355a365(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a04334291cb70ff013dd08788b4bf6eca114911fa3d4e0e0980c81bb0515daf5(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LogsIndexExclusionFilter]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46d074c569565f3244a456793ad24d0d4983d5f03fa958b9ba1232f8797da245(
    *,
    query: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1fc5e3568b4754e6b00d0861c480039a46c0093f379d57030d7773aebf9f781f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e14218e79ee9a928d2413a19acc297fc5e2f95006876c6bda11b3a7e5258913c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9cad348f492f70ad712d8a24330bb7767e5a5665752f19c8cb80754cf88e7ec(
    value: typing.Optional[LogsIndexFilter],
) -> None:
    """Type checking stubs"""
    pass
