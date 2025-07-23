r'''
# `google_monitoring_slo`

Refer to the Terraform Registry for docs: [`google_monitoring_slo`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_slo).
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


class MonitoringSlo(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.monitoringSlo.MonitoringSlo",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_slo google_monitoring_slo}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        goal: jsii.Number,
        service: builtins.str,
        basic_sli: typing.Optional[typing.Union["MonitoringSloBasicSli", typing.Dict[builtins.str, typing.Any]]] = None,
        calendar_period: typing.Optional[builtins.str] = None,
        display_name: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        request_based_sli: typing.Optional[typing.Union["MonitoringSloRequestBasedSli", typing.Dict[builtins.str, typing.Any]]] = None,
        rolling_period_days: typing.Optional[jsii.Number] = None,
        slo_id: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["MonitoringSloTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        user_labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        windows_based_sli: typing.Optional[typing.Union["MonitoringSloWindowsBasedSli", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_slo google_monitoring_slo} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param goal: The fraction of service that must be good in order for this objective to be met. 0 < goal <= 0.999 Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_slo#goal MonitoringSlo#goal}
        :param service: ID of the service to which this SLO belongs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_slo#service MonitoringSlo#service}
        :param basic_sli: basic_sli block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_slo#basic_sli MonitoringSlo#basic_sli}
        :param calendar_period: A calendar period, semantically "since the start of the current ". Possible values: ["DAY", "WEEK", "FORTNIGHT", "MONTH"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_slo#calendar_period MonitoringSlo#calendar_period}
        :param display_name: Name used for UI elements listing this SLO. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_slo#display_name MonitoringSlo#display_name}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_slo#id MonitoringSlo#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_slo#project MonitoringSlo#project}.
        :param request_based_sli: request_based_sli block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_slo#request_based_sli MonitoringSlo#request_based_sli}
        :param rolling_period_days: A rolling time period, semantically "in the past X days". Must be between 1 to 30 days, inclusive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_slo#rolling_period_days MonitoringSlo#rolling_period_days}
        :param slo_id: The id to use for this ServiceLevelObjective. If omitted, an id will be generated instead. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_slo#slo_id MonitoringSlo#slo_id}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_slo#timeouts MonitoringSlo#timeouts}
        :param user_labels: This field is intended to be used for organizing and identifying the AlertPolicy objects.The field can contain up to 64 entries. Each key and value is limited to 63 Unicode characters or 128 bytes, whichever is smaller. Labels and values can contain only lowercase letters, numerals, underscores, and dashes. Keys must begin with a letter. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_slo#user_labels MonitoringSlo#user_labels}
        :param windows_based_sli: windows_based_sli block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_slo#windows_based_sli MonitoringSlo#windows_based_sli}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__207b652ab8f29be86224b293d4519cbf5091a04790795a5ca6ca6da683d2f304)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = MonitoringSloConfig(
            goal=goal,
            service=service,
            basic_sli=basic_sli,
            calendar_period=calendar_period,
            display_name=display_name,
            id=id,
            project=project,
            request_based_sli=request_based_sli,
            rolling_period_days=rolling_period_days,
            slo_id=slo_id,
            timeouts=timeouts,
            user_labels=user_labels,
            windows_based_sli=windows_based_sli,
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
        '''Generates CDKTF code for importing a MonitoringSlo resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the MonitoringSlo to import.
        :param import_from_id: The id of the existing MonitoringSlo that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_slo#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the MonitoringSlo to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e43d18645fca18bdf331ec929bcd97d329d39ba2684bea5469cdc8f274b2cc51)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putBasicSli")
    def put_basic_sli(
        self,
        *,
        availability: typing.Optional[typing.Union["MonitoringSloBasicSliAvailability", typing.Dict[builtins.str, typing.Any]]] = None,
        latency: typing.Optional[typing.Union["MonitoringSloBasicSliLatency", typing.Dict[builtins.str, typing.Any]]] = None,
        location: typing.Optional[typing.Sequence[builtins.str]] = None,
        method: typing.Optional[typing.Sequence[builtins.str]] = None,
        version: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param availability: availability block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_slo#availability MonitoringSlo#availability}
        :param latency: latency block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_slo#latency MonitoringSlo#latency}
        :param location: An optional set of locations to which this SLI is relevant. Telemetry from other locations will not be used to calculate performance for this SLI. If omitted, this SLI applies to all locations in which the Service has activity. For service types that don't support breaking down by location, setting this field will result in an error. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_slo#location MonitoringSlo#location}
        :param method: An optional set of RPCs to which this SLI is relevant. Telemetry from other methods will not be used to calculate performance for this SLI. If omitted, this SLI applies to all the Service's methods. For service types that don't support breaking down by method, setting this field will result in an error. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_slo#method MonitoringSlo#method}
        :param version: The set of API versions to which this SLI is relevant. Telemetry from other API versions will not be used to calculate performance for this SLI. If omitted, this SLI applies to all API versions. For service types that don't support breaking down by version, setting this field will result in an error. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_slo#version MonitoringSlo#version}
        '''
        value = MonitoringSloBasicSli(
            availability=availability,
            latency=latency,
            location=location,
            method=method,
            version=version,
        )

        return typing.cast(None, jsii.invoke(self, "putBasicSli", [value]))

    @jsii.member(jsii_name="putRequestBasedSli")
    def put_request_based_sli(
        self,
        *,
        distribution_cut: typing.Optional[typing.Union["MonitoringSloRequestBasedSliDistributionCut", typing.Dict[builtins.str, typing.Any]]] = None,
        good_total_ratio: typing.Optional[typing.Union["MonitoringSloRequestBasedSliGoodTotalRatio", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param distribution_cut: distribution_cut block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_slo#distribution_cut MonitoringSlo#distribution_cut}
        :param good_total_ratio: good_total_ratio block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_slo#good_total_ratio MonitoringSlo#good_total_ratio}
        '''
        value = MonitoringSloRequestBasedSli(
            distribution_cut=distribution_cut, good_total_ratio=good_total_ratio
        )

        return typing.cast(None, jsii.invoke(self, "putRequestBasedSli", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_slo#create MonitoringSlo#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_slo#delete MonitoringSlo#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_slo#update MonitoringSlo#update}.
        '''
        value = MonitoringSloTimeouts(create=create, delete=delete, update=update)

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="putWindowsBasedSli")
    def put_windows_based_sli(
        self,
        *,
        good_bad_metric_filter: typing.Optional[builtins.str] = None,
        good_total_ratio_threshold: typing.Optional[typing.Union["MonitoringSloWindowsBasedSliGoodTotalRatioThreshold", typing.Dict[builtins.str, typing.Any]]] = None,
        metric_mean_in_range: typing.Optional[typing.Union["MonitoringSloWindowsBasedSliMetricMeanInRange", typing.Dict[builtins.str, typing.Any]]] = None,
        metric_sum_in_range: typing.Optional[typing.Union["MonitoringSloWindowsBasedSliMetricSumInRange", typing.Dict[builtins.str, typing.Any]]] = None,
        window_period: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param good_bad_metric_filter: A TimeSeries `monitoring filter <https://cloud.google.com/monitoring/api/v3/filters>`_ with ValueType = BOOL. The window is good if any true values appear in the window. One of 'good_bad_metric_filter', 'good_total_ratio_threshold', 'metric_mean_in_range', 'metric_sum_in_range' must be set for 'windows_based_sli'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_slo#good_bad_metric_filter MonitoringSlo#good_bad_metric_filter}
        :param good_total_ratio_threshold: good_total_ratio_threshold block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_slo#good_total_ratio_threshold MonitoringSlo#good_total_ratio_threshold}
        :param metric_mean_in_range: metric_mean_in_range block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_slo#metric_mean_in_range MonitoringSlo#metric_mean_in_range}
        :param metric_sum_in_range: metric_sum_in_range block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_slo#metric_sum_in_range MonitoringSlo#metric_sum_in_range}
        :param window_period: Duration over which window quality is evaluated, given as a duration string "{X}s" representing X seconds. Must be an integer fraction of a day and at least 60s. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_slo#window_period MonitoringSlo#window_period}
        '''
        value = MonitoringSloWindowsBasedSli(
            good_bad_metric_filter=good_bad_metric_filter,
            good_total_ratio_threshold=good_total_ratio_threshold,
            metric_mean_in_range=metric_mean_in_range,
            metric_sum_in_range=metric_sum_in_range,
            window_period=window_period,
        )

        return typing.cast(None, jsii.invoke(self, "putWindowsBasedSli", [value]))

    @jsii.member(jsii_name="resetBasicSli")
    def reset_basic_sli(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBasicSli", []))

    @jsii.member(jsii_name="resetCalendarPeriod")
    def reset_calendar_period(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCalendarPeriod", []))

    @jsii.member(jsii_name="resetDisplayName")
    def reset_display_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDisplayName", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetProject")
    def reset_project(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProject", []))

    @jsii.member(jsii_name="resetRequestBasedSli")
    def reset_request_based_sli(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRequestBasedSli", []))

    @jsii.member(jsii_name="resetRollingPeriodDays")
    def reset_rolling_period_days(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRollingPeriodDays", []))

    @jsii.member(jsii_name="resetSloId")
    def reset_slo_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSloId", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

    @jsii.member(jsii_name="resetUserLabels")
    def reset_user_labels(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUserLabels", []))

    @jsii.member(jsii_name="resetWindowsBasedSli")
    def reset_windows_based_sli(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWindowsBasedSli", []))

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
    @jsii.member(jsii_name="basicSli")
    def basic_sli(self) -> "MonitoringSloBasicSliOutputReference":
        return typing.cast("MonitoringSloBasicSliOutputReference", jsii.get(self, "basicSli"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="requestBasedSli")
    def request_based_sli(self) -> "MonitoringSloRequestBasedSliOutputReference":
        return typing.cast("MonitoringSloRequestBasedSliOutputReference", jsii.get(self, "requestBasedSli"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "MonitoringSloTimeoutsOutputReference":
        return typing.cast("MonitoringSloTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="windowsBasedSli")
    def windows_based_sli(self) -> "MonitoringSloWindowsBasedSliOutputReference":
        return typing.cast("MonitoringSloWindowsBasedSliOutputReference", jsii.get(self, "windowsBasedSli"))

    @builtins.property
    @jsii.member(jsii_name="basicSliInput")
    def basic_sli_input(self) -> typing.Optional["MonitoringSloBasicSli"]:
        return typing.cast(typing.Optional["MonitoringSloBasicSli"], jsii.get(self, "basicSliInput"))

    @builtins.property
    @jsii.member(jsii_name="calendarPeriodInput")
    def calendar_period_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "calendarPeriodInput"))

    @builtins.property
    @jsii.member(jsii_name="displayNameInput")
    def display_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "displayNameInput"))

    @builtins.property
    @jsii.member(jsii_name="goalInput")
    def goal_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "goalInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="requestBasedSliInput")
    def request_based_sli_input(
        self,
    ) -> typing.Optional["MonitoringSloRequestBasedSli"]:
        return typing.cast(typing.Optional["MonitoringSloRequestBasedSli"], jsii.get(self, "requestBasedSliInput"))

    @builtins.property
    @jsii.member(jsii_name="rollingPeriodDaysInput")
    def rolling_period_days_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "rollingPeriodDaysInput"))

    @builtins.property
    @jsii.member(jsii_name="serviceInput")
    def service_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serviceInput"))

    @builtins.property
    @jsii.member(jsii_name="sloIdInput")
    def slo_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sloIdInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "MonitoringSloTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "MonitoringSloTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="userLabelsInput")
    def user_labels_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "userLabelsInput"))

    @builtins.property
    @jsii.member(jsii_name="windowsBasedSliInput")
    def windows_based_sli_input(
        self,
    ) -> typing.Optional["MonitoringSloWindowsBasedSli"]:
        return typing.cast(typing.Optional["MonitoringSloWindowsBasedSli"], jsii.get(self, "windowsBasedSliInput"))

    @builtins.property
    @jsii.member(jsii_name="calendarPeriod")
    def calendar_period(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "calendarPeriod"))

    @calendar_period.setter
    def calendar_period(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9066f60553036899e5b299db59154ae346e49161f31b2934b639589661534484)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "calendarPeriod", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="displayName")
    def display_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "displayName"))

    @display_name.setter
    def display_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__57bab5a3af3e1d284e54421c3889dd951031b6d6ffecab839a10141a864ab57e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "displayName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="goal")
    def goal(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "goal"))

    @goal.setter
    def goal(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ff95a8b0fcb6782f315b5b7692460344c144b9bee0392c513152e5c1e0fd544e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "goal", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c2125d892d7024c202fd1897da5b0c9e987ba1c95fe8ed5b2329bb8d4e0f21a0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c80f39fe062ef3f1ef28c27bb0910f641c293eb653898d2be2e1ed4009273fbd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="rollingPeriodDays")
    def rolling_period_days(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "rollingPeriodDays"))

    @rolling_period_days.setter
    def rolling_period_days(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__db0c86dfbefd61900a859460450810eab96d5f044a0b44ad8468fbac07b48339)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rollingPeriodDays", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="service")
    def service(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "service"))

    @service.setter
    def service(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9c01709cd6776bbb195c1bfc8243b774ef1a970d5d3a7eec2a56efe933c9eb47)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "service", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sloId")
    def slo_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sloId"))

    @slo_id.setter
    def slo_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6cbfc76eee1c044ab03df264d8b67f2aa5ff856cf7c053541400e846ab3596ee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sloId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="userLabels")
    def user_labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "userLabels"))

    @user_labels.setter
    def user_labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1a000caab5276cd9471152b25140a03e972abc5f4448962316100f3dec116326)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "userLabels", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.monitoringSlo.MonitoringSloBasicSli",
    jsii_struct_bases=[],
    name_mapping={
        "availability": "availability",
        "latency": "latency",
        "location": "location",
        "method": "method",
        "version": "version",
    },
)
class MonitoringSloBasicSli:
    def __init__(
        self,
        *,
        availability: typing.Optional[typing.Union["MonitoringSloBasicSliAvailability", typing.Dict[builtins.str, typing.Any]]] = None,
        latency: typing.Optional[typing.Union["MonitoringSloBasicSliLatency", typing.Dict[builtins.str, typing.Any]]] = None,
        location: typing.Optional[typing.Sequence[builtins.str]] = None,
        method: typing.Optional[typing.Sequence[builtins.str]] = None,
        version: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param availability: availability block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_slo#availability MonitoringSlo#availability}
        :param latency: latency block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_slo#latency MonitoringSlo#latency}
        :param location: An optional set of locations to which this SLI is relevant. Telemetry from other locations will not be used to calculate performance for this SLI. If omitted, this SLI applies to all locations in which the Service has activity. For service types that don't support breaking down by location, setting this field will result in an error. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_slo#location MonitoringSlo#location}
        :param method: An optional set of RPCs to which this SLI is relevant. Telemetry from other methods will not be used to calculate performance for this SLI. If omitted, this SLI applies to all the Service's methods. For service types that don't support breaking down by method, setting this field will result in an error. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_slo#method MonitoringSlo#method}
        :param version: The set of API versions to which this SLI is relevant. Telemetry from other API versions will not be used to calculate performance for this SLI. If omitted, this SLI applies to all API versions. For service types that don't support breaking down by version, setting this field will result in an error. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_slo#version MonitoringSlo#version}
        '''
        if isinstance(availability, dict):
            availability = MonitoringSloBasicSliAvailability(**availability)
        if isinstance(latency, dict):
            latency = MonitoringSloBasicSliLatency(**latency)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__772cc51c21ae02acf20f08f028fab38ef4663d5374642cca1ce08e4b252024ae)
            check_type(argname="argument availability", value=availability, expected_type=type_hints["availability"])
            check_type(argname="argument latency", value=latency, expected_type=type_hints["latency"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument method", value=method, expected_type=type_hints["method"])
            check_type(argname="argument version", value=version, expected_type=type_hints["version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if availability is not None:
            self._values["availability"] = availability
        if latency is not None:
            self._values["latency"] = latency
        if location is not None:
            self._values["location"] = location
        if method is not None:
            self._values["method"] = method
        if version is not None:
            self._values["version"] = version

    @builtins.property
    def availability(self) -> typing.Optional["MonitoringSloBasicSliAvailability"]:
        '''availability block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_slo#availability MonitoringSlo#availability}
        '''
        result = self._values.get("availability")
        return typing.cast(typing.Optional["MonitoringSloBasicSliAvailability"], result)

    @builtins.property
    def latency(self) -> typing.Optional["MonitoringSloBasicSliLatency"]:
        '''latency block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_slo#latency MonitoringSlo#latency}
        '''
        result = self._values.get("latency")
        return typing.cast(typing.Optional["MonitoringSloBasicSliLatency"], result)

    @builtins.property
    def location(self) -> typing.Optional[typing.List[builtins.str]]:
        '''An optional set of locations to which this SLI is relevant.

        Telemetry from other locations will not be used to calculate
        performance for this SLI. If omitted, this SLI applies to all
        locations in which the Service has activity. For service types
        that don't support breaking down by location, setting this
        field will result in an error.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_slo#location MonitoringSlo#location}
        '''
        result = self._values.get("location")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def method(self) -> typing.Optional[typing.List[builtins.str]]:
        '''An optional set of RPCs to which this SLI is relevant.

        Telemetry from other methods will not be used to calculate
        performance for this SLI. If omitted, this SLI applies to all
        the Service's methods. For service types that don't support
        breaking down by method, setting this field will result in an
        error.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_slo#method MonitoringSlo#method}
        '''
        result = self._values.get("method")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def version(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The set of API versions to which this SLI is relevant.

        Telemetry from other API versions will not be used to
        calculate performance for this SLI. If omitted,
        this SLI applies to all API versions. For service types
        that don't support breaking down by version, setting this
        field will result in an error.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_slo#version MonitoringSlo#version}
        '''
        result = self._values.get("version")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MonitoringSloBasicSli(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.monitoringSlo.MonitoringSloBasicSliAvailability",
    jsii_struct_bases=[],
    name_mapping={"enabled": "enabled"},
)
class MonitoringSloBasicSliAvailability:
    def __init__(
        self,
        *,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param enabled: Whether an availability SLI is enabled or not. Must be set to true. Defaults to 'true'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_slo#enabled MonitoringSlo#enabled}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__47e95fd062f3c2da8ce7524a2c46ce75ef6789f9afa30bcba0495061a9c77802)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if enabled is not None:
            self._values["enabled"] = enabled

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether an availability SLI is enabled or not. Must be set to true. Defaults to 'true'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_slo#enabled MonitoringSlo#enabled}
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MonitoringSloBasicSliAvailability(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MonitoringSloBasicSliAvailabilityOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.monitoringSlo.MonitoringSloBasicSliAvailabilityOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__807b8e97e94af37ae7b74b18fa5766bafcd3e16c6686065ac16fe28c32f0749f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetEnabled")
    def reset_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnabled", []))

    @builtins.property
    @jsii.member(jsii_name="enabledInput")
    def enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enabledInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__5bc8a298c0763d0a18bbb9a648c6c73d46a7c2551279af0f1c4ae68e6c6c66af)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[MonitoringSloBasicSliAvailability]:
        return typing.cast(typing.Optional[MonitoringSloBasicSliAvailability], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MonitoringSloBasicSliAvailability],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a162a1dcff0d464afde8d8a46c85c7de31ba22dc430343af32d5e7b1d2455b73)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.monitoringSlo.MonitoringSloBasicSliLatency",
    jsii_struct_bases=[],
    name_mapping={"threshold": "threshold"},
)
class MonitoringSloBasicSliLatency:
    def __init__(self, *, threshold: builtins.str) -> None:
        '''
        :param threshold: A duration string, e.g. 10s. Good service is defined to be the count of requests made to this service that return in no more than threshold. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_slo#threshold MonitoringSlo#threshold}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__61da1433c687348106428e6099b255da5a7a9a7587af61765d79190fdb7a19d9)
            check_type(argname="argument threshold", value=threshold, expected_type=type_hints["threshold"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "threshold": threshold,
        }

    @builtins.property
    def threshold(self) -> builtins.str:
        '''A duration string, e.g. 10s. Good service is defined to be the count of requests made to this service that return in no more than threshold.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_slo#threshold MonitoringSlo#threshold}
        '''
        result = self._values.get("threshold")
        assert result is not None, "Required property 'threshold' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MonitoringSloBasicSliLatency(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MonitoringSloBasicSliLatencyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.monitoringSlo.MonitoringSloBasicSliLatencyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ba4a0ec4a9469e32f8e91faee562efdcfecc2502dd8b00e918ed69a275799423)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="thresholdInput")
    def threshold_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "thresholdInput"))

    @builtins.property
    @jsii.member(jsii_name="threshold")
    def threshold(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "threshold"))

    @threshold.setter
    def threshold(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__af33329d6f69546c5439382d004212cbbed5340ead6897b2aed06084d1bdf56d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "threshold", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[MonitoringSloBasicSliLatency]:
        return typing.cast(typing.Optional[MonitoringSloBasicSliLatency], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MonitoringSloBasicSliLatency],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e47211385bf6b15ed1864a549dbeb16da2cf216b6b321743c2f1ec36139cd4a5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class MonitoringSloBasicSliOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.monitoringSlo.MonitoringSloBasicSliOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7781601bc68352b81045d6c2d12859ab6c8028201fa947a03febf9ecaae5a6cc)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAvailability")
    def put_availability(
        self,
        *,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param enabled: Whether an availability SLI is enabled or not. Must be set to true. Defaults to 'true'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_slo#enabled MonitoringSlo#enabled}
        '''
        value = MonitoringSloBasicSliAvailability(enabled=enabled)

        return typing.cast(None, jsii.invoke(self, "putAvailability", [value]))

    @jsii.member(jsii_name="putLatency")
    def put_latency(self, *, threshold: builtins.str) -> None:
        '''
        :param threshold: A duration string, e.g. 10s. Good service is defined to be the count of requests made to this service that return in no more than threshold. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_slo#threshold MonitoringSlo#threshold}
        '''
        value = MonitoringSloBasicSliLatency(threshold=threshold)

        return typing.cast(None, jsii.invoke(self, "putLatency", [value]))

    @jsii.member(jsii_name="resetAvailability")
    def reset_availability(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAvailability", []))

    @jsii.member(jsii_name="resetLatency")
    def reset_latency(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLatency", []))

    @jsii.member(jsii_name="resetLocation")
    def reset_location(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLocation", []))

    @jsii.member(jsii_name="resetMethod")
    def reset_method(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMethod", []))

    @jsii.member(jsii_name="resetVersion")
    def reset_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVersion", []))

    @builtins.property
    @jsii.member(jsii_name="availability")
    def availability(self) -> MonitoringSloBasicSliAvailabilityOutputReference:
        return typing.cast(MonitoringSloBasicSliAvailabilityOutputReference, jsii.get(self, "availability"))

    @builtins.property
    @jsii.member(jsii_name="latency")
    def latency(self) -> MonitoringSloBasicSliLatencyOutputReference:
        return typing.cast(MonitoringSloBasicSliLatencyOutputReference, jsii.get(self, "latency"))

    @builtins.property
    @jsii.member(jsii_name="availabilityInput")
    def availability_input(self) -> typing.Optional[MonitoringSloBasicSliAvailability]:
        return typing.cast(typing.Optional[MonitoringSloBasicSliAvailability], jsii.get(self, "availabilityInput"))

    @builtins.property
    @jsii.member(jsii_name="latencyInput")
    def latency_input(self) -> typing.Optional[MonitoringSloBasicSliLatency]:
        return typing.cast(typing.Optional[MonitoringSloBasicSliLatency], jsii.get(self, "latencyInput"))

    @builtins.property
    @jsii.member(jsii_name="locationInput")
    def location_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "locationInput"))

    @builtins.property
    @jsii.member(jsii_name="methodInput")
    def method_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "methodInput"))

    @builtins.property
    @jsii.member(jsii_name="versionInput")
    def version_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "versionInput"))

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "location"))

    @location.setter
    def location(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c6be21f928c84cc328aae597a9c57738e0c3d91c64541ffbcda3316a9b7bfaf4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="method")
    def method(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "method"))

    @method.setter
    def method(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2aca4c31372e9847e3911397548f478a90dc2e08b2e9144e2772c253ed918ac0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "method", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="version")
    def version(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "version"))

    @version.setter
    def version(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__abeecac0bbe5ef164b09ff78f4b0cc6b5ade23d01d2003aed1d1a00d7f002b3b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "version", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[MonitoringSloBasicSli]:
        return typing.cast(typing.Optional[MonitoringSloBasicSli], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[MonitoringSloBasicSli]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__80521bbee05e66a47440c1f5d43646bc5fc616a765e0025960580b8f67f9e3fd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.monitoringSlo.MonitoringSloConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "goal": "goal",
        "service": "service",
        "basic_sli": "basicSli",
        "calendar_period": "calendarPeriod",
        "display_name": "displayName",
        "id": "id",
        "project": "project",
        "request_based_sli": "requestBasedSli",
        "rolling_period_days": "rollingPeriodDays",
        "slo_id": "sloId",
        "timeouts": "timeouts",
        "user_labels": "userLabels",
        "windows_based_sli": "windowsBasedSli",
    },
)
class MonitoringSloConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        goal: jsii.Number,
        service: builtins.str,
        basic_sli: typing.Optional[typing.Union[MonitoringSloBasicSli, typing.Dict[builtins.str, typing.Any]]] = None,
        calendar_period: typing.Optional[builtins.str] = None,
        display_name: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        request_based_sli: typing.Optional[typing.Union["MonitoringSloRequestBasedSli", typing.Dict[builtins.str, typing.Any]]] = None,
        rolling_period_days: typing.Optional[jsii.Number] = None,
        slo_id: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["MonitoringSloTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        user_labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        windows_based_sli: typing.Optional[typing.Union["MonitoringSloWindowsBasedSli", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param goal: The fraction of service that must be good in order for this objective to be met. 0 < goal <= 0.999 Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_slo#goal MonitoringSlo#goal}
        :param service: ID of the service to which this SLO belongs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_slo#service MonitoringSlo#service}
        :param basic_sli: basic_sli block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_slo#basic_sli MonitoringSlo#basic_sli}
        :param calendar_period: A calendar period, semantically "since the start of the current ". Possible values: ["DAY", "WEEK", "FORTNIGHT", "MONTH"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_slo#calendar_period MonitoringSlo#calendar_period}
        :param display_name: Name used for UI elements listing this SLO. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_slo#display_name MonitoringSlo#display_name}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_slo#id MonitoringSlo#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_slo#project MonitoringSlo#project}.
        :param request_based_sli: request_based_sli block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_slo#request_based_sli MonitoringSlo#request_based_sli}
        :param rolling_period_days: A rolling time period, semantically "in the past X days". Must be between 1 to 30 days, inclusive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_slo#rolling_period_days MonitoringSlo#rolling_period_days}
        :param slo_id: The id to use for this ServiceLevelObjective. If omitted, an id will be generated instead. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_slo#slo_id MonitoringSlo#slo_id}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_slo#timeouts MonitoringSlo#timeouts}
        :param user_labels: This field is intended to be used for organizing and identifying the AlertPolicy objects.The field can contain up to 64 entries. Each key and value is limited to 63 Unicode characters or 128 bytes, whichever is smaller. Labels and values can contain only lowercase letters, numerals, underscores, and dashes. Keys must begin with a letter. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_slo#user_labels MonitoringSlo#user_labels}
        :param windows_based_sli: windows_based_sli block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_slo#windows_based_sli MonitoringSlo#windows_based_sli}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(basic_sli, dict):
            basic_sli = MonitoringSloBasicSli(**basic_sli)
        if isinstance(request_based_sli, dict):
            request_based_sli = MonitoringSloRequestBasedSli(**request_based_sli)
        if isinstance(timeouts, dict):
            timeouts = MonitoringSloTimeouts(**timeouts)
        if isinstance(windows_based_sli, dict):
            windows_based_sli = MonitoringSloWindowsBasedSli(**windows_based_sli)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d1778f877d5d053c2d3a19988d224711bdc293b12708b21698f06e3ecec3edda)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument goal", value=goal, expected_type=type_hints["goal"])
            check_type(argname="argument service", value=service, expected_type=type_hints["service"])
            check_type(argname="argument basic_sli", value=basic_sli, expected_type=type_hints["basic_sli"])
            check_type(argname="argument calendar_period", value=calendar_period, expected_type=type_hints["calendar_period"])
            check_type(argname="argument display_name", value=display_name, expected_type=type_hints["display_name"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument request_based_sli", value=request_based_sli, expected_type=type_hints["request_based_sli"])
            check_type(argname="argument rolling_period_days", value=rolling_period_days, expected_type=type_hints["rolling_period_days"])
            check_type(argname="argument slo_id", value=slo_id, expected_type=type_hints["slo_id"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
            check_type(argname="argument user_labels", value=user_labels, expected_type=type_hints["user_labels"])
            check_type(argname="argument windows_based_sli", value=windows_based_sli, expected_type=type_hints["windows_based_sli"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "goal": goal,
            "service": service,
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
        if basic_sli is not None:
            self._values["basic_sli"] = basic_sli
        if calendar_period is not None:
            self._values["calendar_period"] = calendar_period
        if display_name is not None:
            self._values["display_name"] = display_name
        if id is not None:
            self._values["id"] = id
        if project is not None:
            self._values["project"] = project
        if request_based_sli is not None:
            self._values["request_based_sli"] = request_based_sli
        if rolling_period_days is not None:
            self._values["rolling_period_days"] = rolling_period_days
        if slo_id is not None:
            self._values["slo_id"] = slo_id
        if timeouts is not None:
            self._values["timeouts"] = timeouts
        if user_labels is not None:
            self._values["user_labels"] = user_labels
        if windows_based_sli is not None:
            self._values["windows_based_sli"] = windows_based_sli

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
    def goal(self) -> jsii.Number:
        '''The fraction of service that must be good in order for this objective to be met.

        0 < goal <= 0.999

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_slo#goal MonitoringSlo#goal}
        '''
        result = self._values.get("goal")
        assert result is not None, "Required property 'goal' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def service(self) -> builtins.str:
        '''ID of the service to which this SLO belongs.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_slo#service MonitoringSlo#service}
        '''
        result = self._values.get("service")
        assert result is not None, "Required property 'service' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def basic_sli(self) -> typing.Optional[MonitoringSloBasicSli]:
        '''basic_sli block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_slo#basic_sli MonitoringSlo#basic_sli}
        '''
        result = self._values.get("basic_sli")
        return typing.cast(typing.Optional[MonitoringSloBasicSli], result)

    @builtins.property
    def calendar_period(self) -> typing.Optional[builtins.str]:
        '''A calendar period, semantically "since the start of the current ". Possible values: ["DAY", "WEEK", "FORTNIGHT", "MONTH"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_slo#calendar_period MonitoringSlo#calendar_period}
        '''
        result = self._values.get("calendar_period")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def display_name(self) -> typing.Optional[builtins.str]:
        '''Name used for UI elements listing this SLO.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_slo#display_name MonitoringSlo#display_name}
        '''
        result = self._values.get("display_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_slo#id MonitoringSlo#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_slo#project MonitoringSlo#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def request_based_sli(self) -> typing.Optional["MonitoringSloRequestBasedSli"]:
        '''request_based_sli block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_slo#request_based_sli MonitoringSlo#request_based_sli}
        '''
        result = self._values.get("request_based_sli")
        return typing.cast(typing.Optional["MonitoringSloRequestBasedSli"], result)

    @builtins.property
    def rolling_period_days(self) -> typing.Optional[jsii.Number]:
        '''A rolling time period, semantically "in the past X days". Must be between 1 to 30 days, inclusive.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_slo#rolling_period_days MonitoringSlo#rolling_period_days}
        '''
        result = self._values.get("rolling_period_days")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def slo_id(self) -> typing.Optional[builtins.str]:
        '''The id to use for this ServiceLevelObjective. If omitted, an id will be generated instead.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_slo#slo_id MonitoringSlo#slo_id}
        '''
        result = self._values.get("slo_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["MonitoringSloTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_slo#timeouts MonitoringSlo#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["MonitoringSloTimeouts"], result)

    @builtins.property
    def user_labels(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''This field is intended to be used for organizing and identifying the AlertPolicy objects.The field can contain up to 64 entries. Each key and value is limited to 63 Unicode characters or 128 bytes, whichever is smaller. Labels and values can contain only lowercase letters, numerals, underscores, and dashes. Keys must begin with a letter.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_slo#user_labels MonitoringSlo#user_labels}
        '''
        result = self._values.get("user_labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def windows_based_sli(self) -> typing.Optional["MonitoringSloWindowsBasedSli"]:
        '''windows_based_sli block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_slo#windows_based_sli MonitoringSlo#windows_based_sli}
        '''
        result = self._values.get("windows_based_sli")
        return typing.cast(typing.Optional["MonitoringSloWindowsBasedSli"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MonitoringSloConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.monitoringSlo.MonitoringSloRequestBasedSli",
    jsii_struct_bases=[],
    name_mapping={
        "distribution_cut": "distributionCut",
        "good_total_ratio": "goodTotalRatio",
    },
)
class MonitoringSloRequestBasedSli:
    def __init__(
        self,
        *,
        distribution_cut: typing.Optional[typing.Union["MonitoringSloRequestBasedSliDistributionCut", typing.Dict[builtins.str, typing.Any]]] = None,
        good_total_ratio: typing.Optional[typing.Union["MonitoringSloRequestBasedSliGoodTotalRatio", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param distribution_cut: distribution_cut block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_slo#distribution_cut MonitoringSlo#distribution_cut}
        :param good_total_ratio: good_total_ratio block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_slo#good_total_ratio MonitoringSlo#good_total_ratio}
        '''
        if isinstance(distribution_cut, dict):
            distribution_cut = MonitoringSloRequestBasedSliDistributionCut(**distribution_cut)
        if isinstance(good_total_ratio, dict):
            good_total_ratio = MonitoringSloRequestBasedSliGoodTotalRatio(**good_total_ratio)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c1f0a300fc6b2b4e90c116bcd28b0a2bcd187ca369b466d5c53f0ddc10e98583)
            check_type(argname="argument distribution_cut", value=distribution_cut, expected_type=type_hints["distribution_cut"])
            check_type(argname="argument good_total_ratio", value=good_total_ratio, expected_type=type_hints["good_total_ratio"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if distribution_cut is not None:
            self._values["distribution_cut"] = distribution_cut
        if good_total_ratio is not None:
            self._values["good_total_ratio"] = good_total_ratio

    @builtins.property
    def distribution_cut(
        self,
    ) -> typing.Optional["MonitoringSloRequestBasedSliDistributionCut"]:
        '''distribution_cut block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_slo#distribution_cut MonitoringSlo#distribution_cut}
        '''
        result = self._values.get("distribution_cut")
        return typing.cast(typing.Optional["MonitoringSloRequestBasedSliDistributionCut"], result)

    @builtins.property
    def good_total_ratio(
        self,
    ) -> typing.Optional["MonitoringSloRequestBasedSliGoodTotalRatio"]:
        '''good_total_ratio block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_slo#good_total_ratio MonitoringSlo#good_total_ratio}
        '''
        result = self._values.get("good_total_ratio")
        return typing.cast(typing.Optional["MonitoringSloRequestBasedSliGoodTotalRatio"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MonitoringSloRequestBasedSli(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.monitoringSlo.MonitoringSloRequestBasedSliDistributionCut",
    jsii_struct_bases=[],
    name_mapping={"distribution_filter": "distributionFilter", "range": "range"},
)
class MonitoringSloRequestBasedSliDistributionCut:
    def __init__(
        self,
        *,
        distribution_filter: builtins.str,
        range: typing.Union["MonitoringSloRequestBasedSliDistributionCutRange", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param distribution_filter: A TimeSeries `monitoring filter <https://cloud.google.com/monitoring/api/v3/filters>`_ aggregating values to quantify the good service provided. Must have ValueType = DISTRIBUTION and MetricKind = DELTA or MetricKind = CUMULATIVE. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_slo#distribution_filter MonitoringSlo#distribution_filter}
        :param range: range block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_slo#range MonitoringSlo#range}
        '''
        if isinstance(range, dict):
            range = MonitoringSloRequestBasedSliDistributionCutRange(**range)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fced9f8643c35bebf070f5919492c2f10d30f77e5edd120c0a6980227402073a)
            check_type(argname="argument distribution_filter", value=distribution_filter, expected_type=type_hints["distribution_filter"])
            check_type(argname="argument range", value=range, expected_type=type_hints["range"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "distribution_filter": distribution_filter,
            "range": range,
        }

    @builtins.property
    def distribution_filter(self) -> builtins.str:
        '''A TimeSeries `monitoring filter <https://cloud.google.com/monitoring/api/v3/filters>`_ aggregating values to quantify the good service provided.

        Must have ValueType = DISTRIBUTION and
        MetricKind = DELTA or MetricKind = CUMULATIVE.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_slo#distribution_filter MonitoringSlo#distribution_filter}
        '''
        result = self._values.get("distribution_filter")
        assert result is not None, "Required property 'distribution_filter' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def range(self) -> "MonitoringSloRequestBasedSliDistributionCutRange":
        '''range block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_slo#range MonitoringSlo#range}
        '''
        result = self._values.get("range")
        assert result is not None, "Required property 'range' is missing"
        return typing.cast("MonitoringSloRequestBasedSliDistributionCutRange", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MonitoringSloRequestBasedSliDistributionCut(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MonitoringSloRequestBasedSliDistributionCutOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.monitoringSlo.MonitoringSloRequestBasedSliDistributionCutOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9e8ef88d7e237e9a30a7d3511d29fb5d039a284d72f3289594b50fbc3090d7d1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putRange")
    def put_range(
        self,
        *,
        max: typing.Optional[jsii.Number] = None,
        min: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param max: max value for the range (inclusive). If not given, will be set to 0. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_slo#max MonitoringSlo#max}
        :param min: Min value for the range (inclusive). If not given, will be set to 0. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_slo#min MonitoringSlo#min}
        '''
        value = MonitoringSloRequestBasedSliDistributionCutRange(max=max, min=min)

        return typing.cast(None, jsii.invoke(self, "putRange", [value]))

    @builtins.property
    @jsii.member(jsii_name="range")
    def range(
        self,
    ) -> "MonitoringSloRequestBasedSliDistributionCutRangeOutputReference":
        return typing.cast("MonitoringSloRequestBasedSliDistributionCutRangeOutputReference", jsii.get(self, "range"))

    @builtins.property
    @jsii.member(jsii_name="distributionFilterInput")
    def distribution_filter_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "distributionFilterInput"))

    @builtins.property
    @jsii.member(jsii_name="rangeInput")
    def range_input(
        self,
    ) -> typing.Optional["MonitoringSloRequestBasedSliDistributionCutRange"]:
        return typing.cast(typing.Optional["MonitoringSloRequestBasedSliDistributionCutRange"], jsii.get(self, "rangeInput"))

    @builtins.property
    @jsii.member(jsii_name="distributionFilter")
    def distribution_filter(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "distributionFilter"))

    @distribution_filter.setter
    def distribution_filter(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ef411de09906fd84c2e654c3f606691e4cbdb6799c859415b56b99b5ef55f4df)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "distributionFilter", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[MonitoringSloRequestBasedSliDistributionCut]:
        return typing.cast(typing.Optional[MonitoringSloRequestBasedSliDistributionCut], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MonitoringSloRequestBasedSliDistributionCut],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__216afbd19fbeb75120dd4ea774c6e6974e8bfe011360d762474e13378e3ca06e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.monitoringSlo.MonitoringSloRequestBasedSliDistributionCutRange",
    jsii_struct_bases=[],
    name_mapping={"max": "max", "min": "min"},
)
class MonitoringSloRequestBasedSliDistributionCutRange:
    def __init__(
        self,
        *,
        max: typing.Optional[jsii.Number] = None,
        min: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param max: max value for the range (inclusive). If not given, will be set to 0. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_slo#max MonitoringSlo#max}
        :param min: Min value for the range (inclusive). If not given, will be set to 0. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_slo#min MonitoringSlo#min}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__28e9d5029a81bf6dc0c01362c78d0b0620d6d6683773bfedc8d0129eaae26568)
            check_type(argname="argument max", value=max, expected_type=type_hints["max"])
            check_type(argname="argument min", value=min, expected_type=type_hints["min"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if max is not None:
            self._values["max"] = max
        if min is not None:
            self._values["min"] = min

    @builtins.property
    def max(self) -> typing.Optional[jsii.Number]:
        '''max value for the range (inclusive). If not given, will be set to 0.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_slo#max MonitoringSlo#max}
        '''
        result = self._values.get("max")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def min(self) -> typing.Optional[jsii.Number]:
        '''Min value for the range (inclusive). If not given, will be set to 0.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_slo#min MonitoringSlo#min}
        '''
        result = self._values.get("min")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MonitoringSloRequestBasedSliDistributionCutRange(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MonitoringSloRequestBasedSliDistributionCutRangeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.monitoringSlo.MonitoringSloRequestBasedSliDistributionCutRangeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__57a8f07586b0d71eb49ba27e66a8522ae7def26c215f75f2498247da7b63994d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetMax")
    def reset_max(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMax", []))

    @jsii.member(jsii_name="resetMin")
    def reset_min(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMin", []))

    @builtins.property
    @jsii.member(jsii_name="maxInput")
    def max_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxInput"))

    @builtins.property
    @jsii.member(jsii_name="minInput")
    def min_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "minInput"))

    @builtins.property
    @jsii.member(jsii_name="max")
    def max(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "max"))

    @max.setter
    def max(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2668efc3e93fa1a8d14b33413379544e2f26c702b7804cbb864ad39e0a748ed3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "max", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="min")
    def min(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "min"))

    @min.setter
    def min(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4537b5781a714853d26a9c5d8d67eedb6d3866da925e4fb251ce5e7db87a57ad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "min", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[MonitoringSloRequestBasedSliDistributionCutRange]:
        return typing.cast(typing.Optional[MonitoringSloRequestBasedSliDistributionCutRange], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MonitoringSloRequestBasedSliDistributionCutRange],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e4d5cade2ebe0c44fcc0e27fa3956eaaaf5359ed77009693b3aeb87fd1f77ba9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.monitoringSlo.MonitoringSloRequestBasedSliGoodTotalRatio",
    jsii_struct_bases=[],
    name_mapping={
        "bad_service_filter": "badServiceFilter",
        "good_service_filter": "goodServiceFilter",
        "total_service_filter": "totalServiceFilter",
    },
)
class MonitoringSloRequestBasedSliGoodTotalRatio:
    def __init__(
        self,
        *,
        bad_service_filter: typing.Optional[builtins.str] = None,
        good_service_filter: typing.Optional[builtins.str] = None,
        total_service_filter: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param bad_service_filter: A TimeSeries `monitoring filter <https://cloud.google.com/monitoring/api/v3/filters>`_ quantifying bad service provided, either demanded service that was not provided or demanded service that was of inadequate quality. Must have ValueType = DOUBLE or ValueType = INT64 and must have MetricKind = DELTA or MetricKind = CUMULATIVE. Exactly two of 'good_service_filter','bad_service_filter','total_service_filter' must be set (good + bad = total is assumed). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_slo#bad_service_filter MonitoringSlo#bad_service_filter}
        :param good_service_filter: A TimeSeries `monitoring filter <https://cloud.google.com/monitoring/api/v3/filters>`_ quantifying good service provided. Must have ValueType = DOUBLE or ValueType = INT64 and must have MetricKind = DELTA or MetricKind = CUMULATIVE. Exactly two of 'good_service_filter','bad_service_filter','total_service_filter' must be set (good + bad = total is assumed). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_slo#good_service_filter MonitoringSlo#good_service_filter}
        :param total_service_filter: A TimeSeries `monitoring filter <https://cloud.google.com/monitoring/api/v3/filters>`_ quantifying total demanded service. Must have ValueType = DOUBLE or ValueType = INT64 and must have MetricKind = DELTA or MetricKind = CUMULATIVE. Exactly two of 'good_service_filter','bad_service_filter','total_service_filter' must be set (good + bad = total is assumed). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_slo#total_service_filter MonitoringSlo#total_service_filter}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4ed687ed0fbf28eb538bf4c02d97ee323ba0dc75e3ebe20c5544ff793dc3cff2)
            check_type(argname="argument bad_service_filter", value=bad_service_filter, expected_type=type_hints["bad_service_filter"])
            check_type(argname="argument good_service_filter", value=good_service_filter, expected_type=type_hints["good_service_filter"])
            check_type(argname="argument total_service_filter", value=total_service_filter, expected_type=type_hints["total_service_filter"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if bad_service_filter is not None:
            self._values["bad_service_filter"] = bad_service_filter
        if good_service_filter is not None:
            self._values["good_service_filter"] = good_service_filter
        if total_service_filter is not None:
            self._values["total_service_filter"] = total_service_filter

    @builtins.property
    def bad_service_filter(self) -> typing.Optional[builtins.str]:
        '''A TimeSeries `monitoring filter <https://cloud.google.com/monitoring/api/v3/filters>`_ quantifying bad service provided, either demanded service that was not provided or demanded service that was of inadequate quality.

        Must have ValueType = DOUBLE or ValueType = INT64 and
        must have MetricKind = DELTA or MetricKind = CUMULATIVE.

        Exactly two of 'good_service_filter','bad_service_filter','total_service_filter'
        must be set (good + bad = total is assumed).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_slo#bad_service_filter MonitoringSlo#bad_service_filter}
        '''
        result = self._values.get("bad_service_filter")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def good_service_filter(self) -> typing.Optional[builtins.str]:
        '''A TimeSeries `monitoring filter <https://cloud.google.com/monitoring/api/v3/filters>`_ quantifying good service provided. Must have ValueType = DOUBLE or ValueType = INT64 and must have MetricKind = DELTA or MetricKind = CUMULATIVE.

        Exactly two of 'good_service_filter','bad_service_filter','total_service_filter'
        must be set (good + bad = total is assumed).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_slo#good_service_filter MonitoringSlo#good_service_filter}
        '''
        result = self._values.get("good_service_filter")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def total_service_filter(self) -> typing.Optional[builtins.str]:
        '''A TimeSeries `monitoring filter <https://cloud.google.com/monitoring/api/v3/filters>`_ quantifying total demanded service.

        Must have ValueType = DOUBLE or ValueType = INT64 and
        must have MetricKind = DELTA or MetricKind = CUMULATIVE.

        Exactly two of 'good_service_filter','bad_service_filter','total_service_filter'
        must be set (good + bad = total is assumed).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_slo#total_service_filter MonitoringSlo#total_service_filter}
        '''
        result = self._values.get("total_service_filter")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MonitoringSloRequestBasedSliGoodTotalRatio(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MonitoringSloRequestBasedSliGoodTotalRatioOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.monitoringSlo.MonitoringSloRequestBasedSliGoodTotalRatioOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__891b6d25f5f34243c36d0c0c3d0e39a67b9ddfa42ea3817d2600a410395c49bc)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetBadServiceFilter")
    def reset_bad_service_filter(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBadServiceFilter", []))

    @jsii.member(jsii_name="resetGoodServiceFilter")
    def reset_good_service_filter(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGoodServiceFilter", []))

    @jsii.member(jsii_name="resetTotalServiceFilter")
    def reset_total_service_filter(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTotalServiceFilter", []))

    @builtins.property
    @jsii.member(jsii_name="badServiceFilterInput")
    def bad_service_filter_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "badServiceFilterInput"))

    @builtins.property
    @jsii.member(jsii_name="goodServiceFilterInput")
    def good_service_filter_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "goodServiceFilterInput"))

    @builtins.property
    @jsii.member(jsii_name="totalServiceFilterInput")
    def total_service_filter_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "totalServiceFilterInput"))

    @builtins.property
    @jsii.member(jsii_name="badServiceFilter")
    def bad_service_filter(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "badServiceFilter"))

    @bad_service_filter.setter
    def bad_service_filter(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__964586f5cc1c36e7d2a0260b4b09db9955d65c7aa0ae5c041d61f67d90e2c5f7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "badServiceFilter", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="goodServiceFilter")
    def good_service_filter(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "goodServiceFilter"))

    @good_service_filter.setter
    def good_service_filter(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ffaaaa1cedb4e3c315e6cc26da3f991db8ccad83195c778af340c4e84bbdced9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "goodServiceFilter", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="totalServiceFilter")
    def total_service_filter(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "totalServiceFilter"))

    @total_service_filter.setter
    def total_service_filter(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7be69f76f64014b370acfdbed6df8b2f66151e50e63d21a1443347b7e42d594e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "totalServiceFilter", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[MonitoringSloRequestBasedSliGoodTotalRatio]:
        return typing.cast(typing.Optional[MonitoringSloRequestBasedSliGoodTotalRatio], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MonitoringSloRequestBasedSliGoodTotalRatio],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ff3ca33c63c18221e0d4c5677e0a6d90071c1e15682778a5de75c9251e4ef1e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class MonitoringSloRequestBasedSliOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.monitoringSlo.MonitoringSloRequestBasedSliOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__dd08559d56778789a60789a5781768897fcddeec96b52ede485eb1ff0d892deb)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putDistributionCut")
    def put_distribution_cut(
        self,
        *,
        distribution_filter: builtins.str,
        range: typing.Union[MonitoringSloRequestBasedSliDistributionCutRange, typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param distribution_filter: A TimeSeries `monitoring filter <https://cloud.google.com/monitoring/api/v3/filters>`_ aggregating values to quantify the good service provided. Must have ValueType = DISTRIBUTION and MetricKind = DELTA or MetricKind = CUMULATIVE. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_slo#distribution_filter MonitoringSlo#distribution_filter}
        :param range: range block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_slo#range MonitoringSlo#range}
        '''
        value = MonitoringSloRequestBasedSliDistributionCut(
            distribution_filter=distribution_filter, range=range
        )

        return typing.cast(None, jsii.invoke(self, "putDistributionCut", [value]))

    @jsii.member(jsii_name="putGoodTotalRatio")
    def put_good_total_ratio(
        self,
        *,
        bad_service_filter: typing.Optional[builtins.str] = None,
        good_service_filter: typing.Optional[builtins.str] = None,
        total_service_filter: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param bad_service_filter: A TimeSeries `monitoring filter <https://cloud.google.com/monitoring/api/v3/filters>`_ quantifying bad service provided, either demanded service that was not provided or demanded service that was of inadequate quality. Must have ValueType = DOUBLE or ValueType = INT64 and must have MetricKind = DELTA or MetricKind = CUMULATIVE. Exactly two of 'good_service_filter','bad_service_filter','total_service_filter' must be set (good + bad = total is assumed). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_slo#bad_service_filter MonitoringSlo#bad_service_filter}
        :param good_service_filter: A TimeSeries `monitoring filter <https://cloud.google.com/monitoring/api/v3/filters>`_ quantifying good service provided. Must have ValueType = DOUBLE or ValueType = INT64 and must have MetricKind = DELTA or MetricKind = CUMULATIVE. Exactly two of 'good_service_filter','bad_service_filter','total_service_filter' must be set (good + bad = total is assumed). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_slo#good_service_filter MonitoringSlo#good_service_filter}
        :param total_service_filter: A TimeSeries `monitoring filter <https://cloud.google.com/monitoring/api/v3/filters>`_ quantifying total demanded service. Must have ValueType = DOUBLE or ValueType = INT64 and must have MetricKind = DELTA or MetricKind = CUMULATIVE. Exactly two of 'good_service_filter','bad_service_filter','total_service_filter' must be set (good + bad = total is assumed). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_slo#total_service_filter MonitoringSlo#total_service_filter}
        '''
        value = MonitoringSloRequestBasedSliGoodTotalRatio(
            bad_service_filter=bad_service_filter,
            good_service_filter=good_service_filter,
            total_service_filter=total_service_filter,
        )

        return typing.cast(None, jsii.invoke(self, "putGoodTotalRatio", [value]))

    @jsii.member(jsii_name="resetDistributionCut")
    def reset_distribution_cut(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDistributionCut", []))

    @jsii.member(jsii_name="resetGoodTotalRatio")
    def reset_good_total_ratio(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGoodTotalRatio", []))

    @builtins.property
    @jsii.member(jsii_name="distributionCut")
    def distribution_cut(
        self,
    ) -> MonitoringSloRequestBasedSliDistributionCutOutputReference:
        return typing.cast(MonitoringSloRequestBasedSliDistributionCutOutputReference, jsii.get(self, "distributionCut"))

    @builtins.property
    @jsii.member(jsii_name="goodTotalRatio")
    def good_total_ratio(
        self,
    ) -> MonitoringSloRequestBasedSliGoodTotalRatioOutputReference:
        return typing.cast(MonitoringSloRequestBasedSliGoodTotalRatioOutputReference, jsii.get(self, "goodTotalRatio"))

    @builtins.property
    @jsii.member(jsii_name="distributionCutInput")
    def distribution_cut_input(
        self,
    ) -> typing.Optional[MonitoringSloRequestBasedSliDistributionCut]:
        return typing.cast(typing.Optional[MonitoringSloRequestBasedSliDistributionCut], jsii.get(self, "distributionCutInput"))

    @builtins.property
    @jsii.member(jsii_name="goodTotalRatioInput")
    def good_total_ratio_input(
        self,
    ) -> typing.Optional[MonitoringSloRequestBasedSliGoodTotalRatio]:
        return typing.cast(typing.Optional[MonitoringSloRequestBasedSliGoodTotalRatio], jsii.get(self, "goodTotalRatioInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[MonitoringSloRequestBasedSli]:
        return typing.cast(typing.Optional[MonitoringSloRequestBasedSli], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MonitoringSloRequestBasedSli],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b3c035af86257ca2d2797ae5ba7fc711d3ff3e7adb5f351d6e2dec48099c4488)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.monitoringSlo.MonitoringSloTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class MonitoringSloTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_slo#create MonitoringSlo#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_slo#delete MonitoringSlo#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_slo#update MonitoringSlo#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__120f2bd4e2ffae44bd7ce2216e8935f923951ab5fdd23d05885ac6481a831cb2)
            check_type(argname="argument create", value=create, expected_type=type_hints["create"])
            check_type(argname="argument delete", value=delete, expected_type=type_hints["delete"])
            check_type(argname="argument update", value=update, expected_type=type_hints["update"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if create is not None:
            self._values["create"] = create
        if delete is not None:
            self._values["delete"] = delete
        if update is not None:
            self._values["update"] = update

    @builtins.property
    def create(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_slo#create MonitoringSlo#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_slo#delete MonitoringSlo#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_slo#update MonitoringSlo#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MonitoringSloTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MonitoringSloTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.monitoringSlo.MonitoringSloTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__13d536094c4de2069c68ff0d620c26224eb0d848ef4b15bc440c388362d6dc23)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCreate")
    def reset_create(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCreate", []))

    @jsii.member(jsii_name="resetDelete")
    def reset_delete(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDelete", []))

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
            type_hints = typing.get_type_hints(_typecheckingstub__fc785ed8e0af3bee5f8343591135fb41a4edbead1f88d483bede64160a258b4b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2eaaa9f70ed1a1c8cb70268267646e8a3c03a7681e9c0ea9c4426ec1f3f4b0c5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f7d637d05a96948397413aa468f18ef905379d298f89631c22f037e2ce1e45d0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MonitoringSloTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MonitoringSloTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MonitoringSloTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bc49ededaea616782b974b2c6d0789568a34b91fa66ac4e366654a1259ff1a11)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.monitoringSlo.MonitoringSloWindowsBasedSli",
    jsii_struct_bases=[],
    name_mapping={
        "good_bad_metric_filter": "goodBadMetricFilter",
        "good_total_ratio_threshold": "goodTotalRatioThreshold",
        "metric_mean_in_range": "metricMeanInRange",
        "metric_sum_in_range": "metricSumInRange",
        "window_period": "windowPeriod",
    },
)
class MonitoringSloWindowsBasedSli:
    def __init__(
        self,
        *,
        good_bad_metric_filter: typing.Optional[builtins.str] = None,
        good_total_ratio_threshold: typing.Optional[typing.Union["MonitoringSloWindowsBasedSliGoodTotalRatioThreshold", typing.Dict[builtins.str, typing.Any]]] = None,
        metric_mean_in_range: typing.Optional[typing.Union["MonitoringSloWindowsBasedSliMetricMeanInRange", typing.Dict[builtins.str, typing.Any]]] = None,
        metric_sum_in_range: typing.Optional[typing.Union["MonitoringSloWindowsBasedSliMetricSumInRange", typing.Dict[builtins.str, typing.Any]]] = None,
        window_period: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param good_bad_metric_filter: A TimeSeries `monitoring filter <https://cloud.google.com/monitoring/api/v3/filters>`_ with ValueType = BOOL. The window is good if any true values appear in the window. One of 'good_bad_metric_filter', 'good_total_ratio_threshold', 'metric_mean_in_range', 'metric_sum_in_range' must be set for 'windows_based_sli'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_slo#good_bad_metric_filter MonitoringSlo#good_bad_metric_filter}
        :param good_total_ratio_threshold: good_total_ratio_threshold block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_slo#good_total_ratio_threshold MonitoringSlo#good_total_ratio_threshold}
        :param metric_mean_in_range: metric_mean_in_range block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_slo#metric_mean_in_range MonitoringSlo#metric_mean_in_range}
        :param metric_sum_in_range: metric_sum_in_range block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_slo#metric_sum_in_range MonitoringSlo#metric_sum_in_range}
        :param window_period: Duration over which window quality is evaluated, given as a duration string "{X}s" representing X seconds. Must be an integer fraction of a day and at least 60s. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_slo#window_period MonitoringSlo#window_period}
        '''
        if isinstance(good_total_ratio_threshold, dict):
            good_total_ratio_threshold = MonitoringSloWindowsBasedSliGoodTotalRatioThreshold(**good_total_ratio_threshold)
        if isinstance(metric_mean_in_range, dict):
            metric_mean_in_range = MonitoringSloWindowsBasedSliMetricMeanInRange(**metric_mean_in_range)
        if isinstance(metric_sum_in_range, dict):
            metric_sum_in_range = MonitoringSloWindowsBasedSliMetricSumInRange(**metric_sum_in_range)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__60645092bab8621d94a4a2c559ae520dec5295a7217536df141e41d394604f6a)
            check_type(argname="argument good_bad_metric_filter", value=good_bad_metric_filter, expected_type=type_hints["good_bad_metric_filter"])
            check_type(argname="argument good_total_ratio_threshold", value=good_total_ratio_threshold, expected_type=type_hints["good_total_ratio_threshold"])
            check_type(argname="argument metric_mean_in_range", value=metric_mean_in_range, expected_type=type_hints["metric_mean_in_range"])
            check_type(argname="argument metric_sum_in_range", value=metric_sum_in_range, expected_type=type_hints["metric_sum_in_range"])
            check_type(argname="argument window_period", value=window_period, expected_type=type_hints["window_period"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if good_bad_metric_filter is not None:
            self._values["good_bad_metric_filter"] = good_bad_metric_filter
        if good_total_ratio_threshold is not None:
            self._values["good_total_ratio_threshold"] = good_total_ratio_threshold
        if metric_mean_in_range is not None:
            self._values["metric_mean_in_range"] = metric_mean_in_range
        if metric_sum_in_range is not None:
            self._values["metric_sum_in_range"] = metric_sum_in_range
        if window_period is not None:
            self._values["window_period"] = window_period

    @builtins.property
    def good_bad_metric_filter(self) -> typing.Optional[builtins.str]:
        '''A TimeSeries `monitoring filter <https://cloud.google.com/monitoring/api/v3/filters>`_ with ValueType = BOOL. The window is good if any true values appear in the window. One of 'good_bad_metric_filter', 'good_total_ratio_threshold', 'metric_mean_in_range', 'metric_sum_in_range' must be set for 'windows_based_sli'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_slo#good_bad_metric_filter MonitoringSlo#good_bad_metric_filter}
        '''
        result = self._values.get("good_bad_metric_filter")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def good_total_ratio_threshold(
        self,
    ) -> typing.Optional["MonitoringSloWindowsBasedSliGoodTotalRatioThreshold"]:
        '''good_total_ratio_threshold block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_slo#good_total_ratio_threshold MonitoringSlo#good_total_ratio_threshold}
        '''
        result = self._values.get("good_total_ratio_threshold")
        return typing.cast(typing.Optional["MonitoringSloWindowsBasedSliGoodTotalRatioThreshold"], result)

    @builtins.property
    def metric_mean_in_range(
        self,
    ) -> typing.Optional["MonitoringSloWindowsBasedSliMetricMeanInRange"]:
        '''metric_mean_in_range block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_slo#metric_mean_in_range MonitoringSlo#metric_mean_in_range}
        '''
        result = self._values.get("metric_mean_in_range")
        return typing.cast(typing.Optional["MonitoringSloWindowsBasedSliMetricMeanInRange"], result)

    @builtins.property
    def metric_sum_in_range(
        self,
    ) -> typing.Optional["MonitoringSloWindowsBasedSliMetricSumInRange"]:
        '''metric_sum_in_range block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_slo#metric_sum_in_range MonitoringSlo#metric_sum_in_range}
        '''
        result = self._values.get("metric_sum_in_range")
        return typing.cast(typing.Optional["MonitoringSloWindowsBasedSliMetricSumInRange"], result)

    @builtins.property
    def window_period(self) -> typing.Optional[builtins.str]:
        '''Duration over which window quality is evaluated, given as a duration string "{X}s" representing X seconds.

        Must be an
        integer fraction of a day and at least 60s.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_slo#window_period MonitoringSlo#window_period}
        '''
        result = self._values.get("window_period")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MonitoringSloWindowsBasedSli(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.monitoringSlo.MonitoringSloWindowsBasedSliGoodTotalRatioThreshold",
    jsii_struct_bases=[],
    name_mapping={
        "basic_sli_performance": "basicSliPerformance",
        "performance": "performance",
        "threshold": "threshold",
    },
)
class MonitoringSloWindowsBasedSliGoodTotalRatioThreshold:
    def __init__(
        self,
        *,
        basic_sli_performance: typing.Optional[typing.Union["MonitoringSloWindowsBasedSliGoodTotalRatioThresholdBasicSliPerformance", typing.Dict[builtins.str, typing.Any]]] = None,
        performance: typing.Optional[typing.Union["MonitoringSloWindowsBasedSliGoodTotalRatioThresholdPerformance", typing.Dict[builtins.str, typing.Any]]] = None,
        threshold: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param basic_sli_performance: basic_sli_performance block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_slo#basic_sli_performance MonitoringSlo#basic_sli_performance}
        :param performance: performance block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_slo#performance MonitoringSlo#performance}
        :param threshold: If window performance >= threshold, the window is counted as good. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_slo#threshold MonitoringSlo#threshold}
        '''
        if isinstance(basic_sli_performance, dict):
            basic_sli_performance = MonitoringSloWindowsBasedSliGoodTotalRatioThresholdBasicSliPerformance(**basic_sli_performance)
        if isinstance(performance, dict):
            performance = MonitoringSloWindowsBasedSliGoodTotalRatioThresholdPerformance(**performance)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__efe1aa2237c56694972671501cdba5fcd2130274120796c81aa8f81f19d70a2a)
            check_type(argname="argument basic_sli_performance", value=basic_sli_performance, expected_type=type_hints["basic_sli_performance"])
            check_type(argname="argument performance", value=performance, expected_type=type_hints["performance"])
            check_type(argname="argument threshold", value=threshold, expected_type=type_hints["threshold"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if basic_sli_performance is not None:
            self._values["basic_sli_performance"] = basic_sli_performance
        if performance is not None:
            self._values["performance"] = performance
        if threshold is not None:
            self._values["threshold"] = threshold

    @builtins.property
    def basic_sli_performance(
        self,
    ) -> typing.Optional["MonitoringSloWindowsBasedSliGoodTotalRatioThresholdBasicSliPerformance"]:
        '''basic_sli_performance block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_slo#basic_sli_performance MonitoringSlo#basic_sli_performance}
        '''
        result = self._values.get("basic_sli_performance")
        return typing.cast(typing.Optional["MonitoringSloWindowsBasedSliGoodTotalRatioThresholdBasicSliPerformance"], result)

    @builtins.property
    def performance(
        self,
    ) -> typing.Optional["MonitoringSloWindowsBasedSliGoodTotalRatioThresholdPerformance"]:
        '''performance block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_slo#performance MonitoringSlo#performance}
        '''
        result = self._values.get("performance")
        return typing.cast(typing.Optional["MonitoringSloWindowsBasedSliGoodTotalRatioThresholdPerformance"], result)

    @builtins.property
    def threshold(self) -> typing.Optional[jsii.Number]:
        '''If window performance >= threshold, the window is counted as good.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_slo#threshold MonitoringSlo#threshold}
        '''
        result = self._values.get("threshold")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MonitoringSloWindowsBasedSliGoodTotalRatioThreshold(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.monitoringSlo.MonitoringSloWindowsBasedSliGoodTotalRatioThresholdBasicSliPerformance",
    jsii_struct_bases=[],
    name_mapping={
        "availability": "availability",
        "latency": "latency",
        "location": "location",
        "method": "method",
        "version": "version",
    },
)
class MonitoringSloWindowsBasedSliGoodTotalRatioThresholdBasicSliPerformance:
    def __init__(
        self,
        *,
        availability: typing.Optional[typing.Union["MonitoringSloWindowsBasedSliGoodTotalRatioThresholdBasicSliPerformanceAvailability", typing.Dict[builtins.str, typing.Any]]] = None,
        latency: typing.Optional[typing.Union["MonitoringSloWindowsBasedSliGoodTotalRatioThresholdBasicSliPerformanceLatency", typing.Dict[builtins.str, typing.Any]]] = None,
        location: typing.Optional[typing.Sequence[builtins.str]] = None,
        method: typing.Optional[typing.Sequence[builtins.str]] = None,
        version: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param availability: availability block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_slo#availability MonitoringSlo#availability}
        :param latency: latency block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_slo#latency MonitoringSlo#latency}
        :param location: An optional set of locations to which this SLI is relevant. Telemetry from other locations will not be used to calculate performance for this SLI. If omitted, this SLI applies to all locations in which the Service has activity. For service types that don't support breaking down by location, setting this field will result in an error. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_slo#location MonitoringSlo#location}
        :param method: An optional set of RPCs to which this SLI is relevant. Telemetry from other methods will not be used to calculate performance for this SLI. If omitted, this SLI applies to all the Service's methods. For service types that don't support breaking down by method, setting this field will result in an error. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_slo#method MonitoringSlo#method}
        :param version: The set of API versions to which this SLI is relevant. Telemetry from other API versions will not be used to calculate performance for this SLI. If omitted, this SLI applies to all API versions. For service types that don't support breaking down by version, setting this field will result in an error. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_slo#version MonitoringSlo#version}
        '''
        if isinstance(availability, dict):
            availability = MonitoringSloWindowsBasedSliGoodTotalRatioThresholdBasicSliPerformanceAvailability(**availability)
        if isinstance(latency, dict):
            latency = MonitoringSloWindowsBasedSliGoodTotalRatioThresholdBasicSliPerformanceLatency(**latency)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f52fe944f229d4446f0a8e53fb27a6ef67ebb7e40e1b65f870ee965768d22081)
            check_type(argname="argument availability", value=availability, expected_type=type_hints["availability"])
            check_type(argname="argument latency", value=latency, expected_type=type_hints["latency"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument method", value=method, expected_type=type_hints["method"])
            check_type(argname="argument version", value=version, expected_type=type_hints["version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if availability is not None:
            self._values["availability"] = availability
        if latency is not None:
            self._values["latency"] = latency
        if location is not None:
            self._values["location"] = location
        if method is not None:
            self._values["method"] = method
        if version is not None:
            self._values["version"] = version

    @builtins.property
    def availability(
        self,
    ) -> typing.Optional["MonitoringSloWindowsBasedSliGoodTotalRatioThresholdBasicSliPerformanceAvailability"]:
        '''availability block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_slo#availability MonitoringSlo#availability}
        '''
        result = self._values.get("availability")
        return typing.cast(typing.Optional["MonitoringSloWindowsBasedSliGoodTotalRatioThresholdBasicSliPerformanceAvailability"], result)

    @builtins.property
    def latency(
        self,
    ) -> typing.Optional["MonitoringSloWindowsBasedSliGoodTotalRatioThresholdBasicSliPerformanceLatency"]:
        '''latency block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_slo#latency MonitoringSlo#latency}
        '''
        result = self._values.get("latency")
        return typing.cast(typing.Optional["MonitoringSloWindowsBasedSliGoodTotalRatioThresholdBasicSliPerformanceLatency"], result)

    @builtins.property
    def location(self) -> typing.Optional[typing.List[builtins.str]]:
        '''An optional set of locations to which this SLI is relevant.

        Telemetry from other locations will not be used to calculate
        performance for this SLI. If omitted, this SLI applies to all
        locations in which the Service has activity. For service types
        that don't support breaking down by location, setting this
        field will result in an error.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_slo#location MonitoringSlo#location}
        '''
        result = self._values.get("location")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def method(self) -> typing.Optional[typing.List[builtins.str]]:
        '''An optional set of RPCs to which this SLI is relevant.

        Telemetry from other methods will not be used to calculate
        performance for this SLI. If omitted, this SLI applies to all
        the Service's methods. For service types that don't support
        breaking down by method, setting this field will result in an
        error.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_slo#method MonitoringSlo#method}
        '''
        result = self._values.get("method")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def version(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The set of API versions to which this SLI is relevant.

        Telemetry from other API versions will not be used to
        calculate performance for this SLI. If omitted,
        this SLI applies to all API versions. For service types
        that don't support breaking down by version, setting this
        field will result in an error.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_slo#version MonitoringSlo#version}
        '''
        result = self._values.get("version")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MonitoringSloWindowsBasedSliGoodTotalRatioThresholdBasicSliPerformance(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.monitoringSlo.MonitoringSloWindowsBasedSliGoodTotalRatioThresholdBasicSliPerformanceAvailability",
    jsii_struct_bases=[],
    name_mapping={"enabled": "enabled"},
)
class MonitoringSloWindowsBasedSliGoodTotalRatioThresholdBasicSliPerformanceAvailability:
    def __init__(
        self,
        *,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param enabled: Whether an availability SLI is enabled or not. Must be set to 'true. Defaults to 'true'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_slo#enabled MonitoringSlo#enabled}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e79c2af469e4d210fcb5e77624e4c6a980e881f4bd2c1cec32b9a69a26edc71)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if enabled is not None:
            self._values["enabled"] = enabled

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether an availability SLI is enabled or not. Must be set to 'true. Defaults to 'true'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_slo#enabled MonitoringSlo#enabled}
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MonitoringSloWindowsBasedSliGoodTotalRatioThresholdBasicSliPerformanceAvailability(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MonitoringSloWindowsBasedSliGoodTotalRatioThresholdBasicSliPerformanceAvailabilityOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.monitoringSlo.MonitoringSloWindowsBasedSliGoodTotalRatioThresholdBasicSliPerformanceAvailabilityOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bbd93368815745a68acc29db8470d3f9a3d75977b4da44f38c58a514d0da6748)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetEnabled")
    def reset_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnabled", []))

    @builtins.property
    @jsii.member(jsii_name="enabledInput")
    def enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enabledInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__c279453c5eb9b4d1a3ca6663fc6b1bb5e34df92ae1aa255bd1039f98a7baaefd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[MonitoringSloWindowsBasedSliGoodTotalRatioThresholdBasicSliPerformanceAvailability]:
        return typing.cast(typing.Optional[MonitoringSloWindowsBasedSliGoodTotalRatioThresholdBasicSliPerformanceAvailability], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MonitoringSloWindowsBasedSliGoodTotalRatioThresholdBasicSliPerformanceAvailability],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ca27d90c1a0e255a064e3df60804bfcfcff86e2aa340b978f10ae9d027af0f7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.monitoringSlo.MonitoringSloWindowsBasedSliGoodTotalRatioThresholdBasicSliPerformanceLatency",
    jsii_struct_bases=[],
    name_mapping={"threshold": "threshold"},
)
class MonitoringSloWindowsBasedSliGoodTotalRatioThresholdBasicSliPerformanceLatency:
    def __init__(self, *, threshold: builtins.str) -> None:
        '''
        :param threshold: A duration string, e.g. 10s. Good service is defined to be the count of requests made to this service that return in no more than threshold. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_slo#threshold MonitoringSlo#threshold}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__139a2cdc410a78f46967381e9607401f3b35a36f0724fae463021a29e77f986e)
            check_type(argname="argument threshold", value=threshold, expected_type=type_hints["threshold"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "threshold": threshold,
        }

    @builtins.property
    def threshold(self) -> builtins.str:
        '''A duration string, e.g. 10s. Good service is defined to be the count of requests made to this service that return in no more than threshold.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_slo#threshold MonitoringSlo#threshold}
        '''
        result = self._values.get("threshold")
        assert result is not None, "Required property 'threshold' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MonitoringSloWindowsBasedSliGoodTotalRatioThresholdBasicSliPerformanceLatency(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MonitoringSloWindowsBasedSliGoodTotalRatioThresholdBasicSliPerformanceLatencyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.monitoringSlo.MonitoringSloWindowsBasedSliGoodTotalRatioThresholdBasicSliPerformanceLatencyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__56f4600c244bf85746af169db966e9b4d90101131dc1e703b67b94f00dbbb3ee)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="thresholdInput")
    def threshold_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "thresholdInput"))

    @builtins.property
    @jsii.member(jsii_name="threshold")
    def threshold(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "threshold"))

    @threshold.setter
    def threshold(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7d40ce047f8c4191bd1842dd53a3d3ef89087f8d8b844e30431d93132ceb7a8e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "threshold", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[MonitoringSloWindowsBasedSliGoodTotalRatioThresholdBasicSliPerformanceLatency]:
        return typing.cast(typing.Optional[MonitoringSloWindowsBasedSliGoodTotalRatioThresholdBasicSliPerformanceLatency], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MonitoringSloWindowsBasedSliGoodTotalRatioThresholdBasicSliPerformanceLatency],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9c86279a98fab1e83f1bafd468883b16a471e65456bfbd439a78983d433fec70)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class MonitoringSloWindowsBasedSliGoodTotalRatioThresholdBasicSliPerformanceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.monitoringSlo.MonitoringSloWindowsBasedSliGoodTotalRatioThresholdBasicSliPerformanceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b57d11014e9ad6617025f7b7b9392f7e8469f3e3903e02d99b4ecd80ca6b183c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAvailability")
    def put_availability(
        self,
        *,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param enabled: Whether an availability SLI is enabled or not. Must be set to 'true. Defaults to 'true'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_slo#enabled MonitoringSlo#enabled}
        '''
        value = MonitoringSloWindowsBasedSliGoodTotalRatioThresholdBasicSliPerformanceAvailability(
            enabled=enabled
        )

        return typing.cast(None, jsii.invoke(self, "putAvailability", [value]))

    @jsii.member(jsii_name="putLatency")
    def put_latency(self, *, threshold: builtins.str) -> None:
        '''
        :param threshold: A duration string, e.g. 10s. Good service is defined to be the count of requests made to this service that return in no more than threshold. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_slo#threshold MonitoringSlo#threshold}
        '''
        value = MonitoringSloWindowsBasedSliGoodTotalRatioThresholdBasicSliPerformanceLatency(
            threshold=threshold
        )

        return typing.cast(None, jsii.invoke(self, "putLatency", [value]))

    @jsii.member(jsii_name="resetAvailability")
    def reset_availability(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAvailability", []))

    @jsii.member(jsii_name="resetLatency")
    def reset_latency(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLatency", []))

    @jsii.member(jsii_name="resetLocation")
    def reset_location(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLocation", []))

    @jsii.member(jsii_name="resetMethod")
    def reset_method(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMethod", []))

    @jsii.member(jsii_name="resetVersion")
    def reset_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVersion", []))

    @builtins.property
    @jsii.member(jsii_name="availability")
    def availability(
        self,
    ) -> MonitoringSloWindowsBasedSliGoodTotalRatioThresholdBasicSliPerformanceAvailabilityOutputReference:
        return typing.cast(MonitoringSloWindowsBasedSliGoodTotalRatioThresholdBasicSliPerformanceAvailabilityOutputReference, jsii.get(self, "availability"))

    @builtins.property
    @jsii.member(jsii_name="latency")
    def latency(
        self,
    ) -> MonitoringSloWindowsBasedSliGoodTotalRatioThresholdBasicSliPerformanceLatencyOutputReference:
        return typing.cast(MonitoringSloWindowsBasedSliGoodTotalRatioThresholdBasicSliPerformanceLatencyOutputReference, jsii.get(self, "latency"))

    @builtins.property
    @jsii.member(jsii_name="availabilityInput")
    def availability_input(
        self,
    ) -> typing.Optional[MonitoringSloWindowsBasedSliGoodTotalRatioThresholdBasicSliPerformanceAvailability]:
        return typing.cast(typing.Optional[MonitoringSloWindowsBasedSliGoodTotalRatioThresholdBasicSliPerformanceAvailability], jsii.get(self, "availabilityInput"))

    @builtins.property
    @jsii.member(jsii_name="latencyInput")
    def latency_input(
        self,
    ) -> typing.Optional[MonitoringSloWindowsBasedSliGoodTotalRatioThresholdBasicSliPerformanceLatency]:
        return typing.cast(typing.Optional[MonitoringSloWindowsBasedSliGoodTotalRatioThresholdBasicSliPerformanceLatency], jsii.get(self, "latencyInput"))

    @builtins.property
    @jsii.member(jsii_name="locationInput")
    def location_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "locationInput"))

    @builtins.property
    @jsii.member(jsii_name="methodInput")
    def method_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "methodInput"))

    @builtins.property
    @jsii.member(jsii_name="versionInput")
    def version_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "versionInput"))

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "location"))

    @location.setter
    def location(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c421a37196d5e60e42116ac782444c55ff72f2a2768a6da909b9e67506996908)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="method")
    def method(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "method"))

    @method.setter
    def method(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1ee89bf83ff6f544bd5d41d51e46fa4982c23c1b6eb578434a5f573824f75da7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "method", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="version")
    def version(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "version"))

    @version.setter
    def version(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2aa8064083564254dc05825fbb18123d434d4db363250a7c603df4634fb404a5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "version", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[MonitoringSloWindowsBasedSliGoodTotalRatioThresholdBasicSliPerformance]:
        return typing.cast(typing.Optional[MonitoringSloWindowsBasedSliGoodTotalRatioThresholdBasicSliPerformance], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MonitoringSloWindowsBasedSliGoodTotalRatioThresholdBasicSliPerformance],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__52c0d8b0c48fcc2170c359921a44c4928f469f7d7386a2940f44c61e9c77dd4c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class MonitoringSloWindowsBasedSliGoodTotalRatioThresholdOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.monitoringSlo.MonitoringSloWindowsBasedSliGoodTotalRatioThresholdOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7ec89540a70bc796c123741e79587ba62772b4bb3547436ad6d068b700cd7917)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putBasicSliPerformance")
    def put_basic_sli_performance(
        self,
        *,
        availability: typing.Optional[typing.Union[MonitoringSloWindowsBasedSliGoodTotalRatioThresholdBasicSliPerformanceAvailability, typing.Dict[builtins.str, typing.Any]]] = None,
        latency: typing.Optional[typing.Union[MonitoringSloWindowsBasedSliGoodTotalRatioThresholdBasicSliPerformanceLatency, typing.Dict[builtins.str, typing.Any]]] = None,
        location: typing.Optional[typing.Sequence[builtins.str]] = None,
        method: typing.Optional[typing.Sequence[builtins.str]] = None,
        version: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param availability: availability block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_slo#availability MonitoringSlo#availability}
        :param latency: latency block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_slo#latency MonitoringSlo#latency}
        :param location: An optional set of locations to which this SLI is relevant. Telemetry from other locations will not be used to calculate performance for this SLI. If omitted, this SLI applies to all locations in which the Service has activity. For service types that don't support breaking down by location, setting this field will result in an error. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_slo#location MonitoringSlo#location}
        :param method: An optional set of RPCs to which this SLI is relevant. Telemetry from other methods will not be used to calculate performance for this SLI. If omitted, this SLI applies to all the Service's methods. For service types that don't support breaking down by method, setting this field will result in an error. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_slo#method MonitoringSlo#method}
        :param version: The set of API versions to which this SLI is relevant. Telemetry from other API versions will not be used to calculate performance for this SLI. If omitted, this SLI applies to all API versions. For service types that don't support breaking down by version, setting this field will result in an error. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_slo#version MonitoringSlo#version}
        '''
        value = MonitoringSloWindowsBasedSliGoodTotalRatioThresholdBasicSliPerformance(
            availability=availability,
            latency=latency,
            location=location,
            method=method,
            version=version,
        )

        return typing.cast(None, jsii.invoke(self, "putBasicSliPerformance", [value]))

    @jsii.member(jsii_name="putPerformance")
    def put_performance(
        self,
        *,
        distribution_cut: typing.Optional[typing.Union["MonitoringSloWindowsBasedSliGoodTotalRatioThresholdPerformanceDistributionCut", typing.Dict[builtins.str, typing.Any]]] = None,
        good_total_ratio: typing.Optional[typing.Union["MonitoringSloWindowsBasedSliGoodTotalRatioThresholdPerformanceGoodTotalRatio", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param distribution_cut: distribution_cut block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_slo#distribution_cut MonitoringSlo#distribution_cut}
        :param good_total_ratio: good_total_ratio block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_slo#good_total_ratio MonitoringSlo#good_total_ratio}
        '''
        value = MonitoringSloWindowsBasedSliGoodTotalRatioThresholdPerformance(
            distribution_cut=distribution_cut, good_total_ratio=good_total_ratio
        )

        return typing.cast(None, jsii.invoke(self, "putPerformance", [value]))

    @jsii.member(jsii_name="resetBasicSliPerformance")
    def reset_basic_sli_performance(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBasicSliPerformance", []))

    @jsii.member(jsii_name="resetPerformance")
    def reset_performance(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPerformance", []))

    @jsii.member(jsii_name="resetThreshold")
    def reset_threshold(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetThreshold", []))

    @builtins.property
    @jsii.member(jsii_name="basicSliPerformance")
    def basic_sli_performance(
        self,
    ) -> MonitoringSloWindowsBasedSliGoodTotalRatioThresholdBasicSliPerformanceOutputReference:
        return typing.cast(MonitoringSloWindowsBasedSliGoodTotalRatioThresholdBasicSliPerformanceOutputReference, jsii.get(self, "basicSliPerformance"))

    @builtins.property
    @jsii.member(jsii_name="performance")
    def performance(
        self,
    ) -> "MonitoringSloWindowsBasedSliGoodTotalRatioThresholdPerformanceOutputReference":
        return typing.cast("MonitoringSloWindowsBasedSliGoodTotalRatioThresholdPerformanceOutputReference", jsii.get(self, "performance"))

    @builtins.property
    @jsii.member(jsii_name="basicSliPerformanceInput")
    def basic_sli_performance_input(
        self,
    ) -> typing.Optional[MonitoringSloWindowsBasedSliGoodTotalRatioThresholdBasicSliPerformance]:
        return typing.cast(typing.Optional[MonitoringSloWindowsBasedSliGoodTotalRatioThresholdBasicSliPerformance], jsii.get(self, "basicSliPerformanceInput"))

    @builtins.property
    @jsii.member(jsii_name="performanceInput")
    def performance_input(
        self,
    ) -> typing.Optional["MonitoringSloWindowsBasedSliGoodTotalRatioThresholdPerformance"]:
        return typing.cast(typing.Optional["MonitoringSloWindowsBasedSliGoodTotalRatioThresholdPerformance"], jsii.get(self, "performanceInput"))

    @builtins.property
    @jsii.member(jsii_name="thresholdInput")
    def threshold_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "thresholdInput"))

    @builtins.property
    @jsii.member(jsii_name="threshold")
    def threshold(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "threshold"))

    @threshold.setter
    def threshold(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__182b6f98799ebca30d7ebdc7e6a5029e83f59365ab74f4a2e7580bb1c6e05190)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "threshold", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[MonitoringSloWindowsBasedSliGoodTotalRatioThreshold]:
        return typing.cast(typing.Optional[MonitoringSloWindowsBasedSliGoodTotalRatioThreshold], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MonitoringSloWindowsBasedSliGoodTotalRatioThreshold],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__200a7c5430ed167fdbac5c0e3e6b9d4a3524f3ea75545f4575ac74d082eeba3a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.monitoringSlo.MonitoringSloWindowsBasedSliGoodTotalRatioThresholdPerformance",
    jsii_struct_bases=[],
    name_mapping={
        "distribution_cut": "distributionCut",
        "good_total_ratio": "goodTotalRatio",
    },
)
class MonitoringSloWindowsBasedSliGoodTotalRatioThresholdPerformance:
    def __init__(
        self,
        *,
        distribution_cut: typing.Optional[typing.Union["MonitoringSloWindowsBasedSliGoodTotalRatioThresholdPerformanceDistributionCut", typing.Dict[builtins.str, typing.Any]]] = None,
        good_total_ratio: typing.Optional[typing.Union["MonitoringSloWindowsBasedSliGoodTotalRatioThresholdPerformanceGoodTotalRatio", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param distribution_cut: distribution_cut block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_slo#distribution_cut MonitoringSlo#distribution_cut}
        :param good_total_ratio: good_total_ratio block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_slo#good_total_ratio MonitoringSlo#good_total_ratio}
        '''
        if isinstance(distribution_cut, dict):
            distribution_cut = MonitoringSloWindowsBasedSliGoodTotalRatioThresholdPerformanceDistributionCut(**distribution_cut)
        if isinstance(good_total_ratio, dict):
            good_total_ratio = MonitoringSloWindowsBasedSliGoodTotalRatioThresholdPerformanceGoodTotalRatio(**good_total_ratio)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aeca6a1579c7b112ef92f401a2f695f9ced8457520ff08697c92b49529f9615b)
            check_type(argname="argument distribution_cut", value=distribution_cut, expected_type=type_hints["distribution_cut"])
            check_type(argname="argument good_total_ratio", value=good_total_ratio, expected_type=type_hints["good_total_ratio"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if distribution_cut is not None:
            self._values["distribution_cut"] = distribution_cut
        if good_total_ratio is not None:
            self._values["good_total_ratio"] = good_total_ratio

    @builtins.property
    def distribution_cut(
        self,
    ) -> typing.Optional["MonitoringSloWindowsBasedSliGoodTotalRatioThresholdPerformanceDistributionCut"]:
        '''distribution_cut block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_slo#distribution_cut MonitoringSlo#distribution_cut}
        '''
        result = self._values.get("distribution_cut")
        return typing.cast(typing.Optional["MonitoringSloWindowsBasedSliGoodTotalRatioThresholdPerformanceDistributionCut"], result)

    @builtins.property
    def good_total_ratio(
        self,
    ) -> typing.Optional["MonitoringSloWindowsBasedSliGoodTotalRatioThresholdPerformanceGoodTotalRatio"]:
        '''good_total_ratio block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_slo#good_total_ratio MonitoringSlo#good_total_ratio}
        '''
        result = self._values.get("good_total_ratio")
        return typing.cast(typing.Optional["MonitoringSloWindowsBasedSliGoodTotalRatioThresholdPerformanceGoodTotalRatio"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MonitoringSloWindowsBasedSliGoodTotalRatioThresholdPerformance(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.monitoringSlo.MonitoringSloWindowsBasedSliGoodTotalRatioThresholdPerformanceDistributionCut",
    jsii_struct_bases=[],
    name_mapping={"distribution_filter": "distributionFilter", "range": "range"},
)
class MonitoringSloWindowsBasedSliGoodTotalRatioThresholdPerformanceDistributionCut:
    def __init__(
        self,
        *,
        distribution_filter: builtins.str,
        range: typing.Union["MonitoringSloWindowsBasedSliGoodTotalRatioThresholdPerformanceDistributionCutRange", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param distribution_filter: A TimeSeries `monitoring filter <https://cloud.google.com/monitoring/api/v3/filters>`_ aggregating values to quantify the good service provided. Must have ValueType = DISTRIBUTION and MetricKind = DELTA or MetricKind = CUMULATIVE. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_slo#distribution_filter MonitoringSlo#distribution_filter}
        :param range: range block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_slo#range MonitoringSlo#range}
        '''
        if isinstance(range, dict):
            range = MonitoringSloWindowsBasedSliGoodTotalRatioThresholdPerformanceDistributionCutRange(**range)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__21f253cfbb05e2d148de7eadfdeea95a4502590acd46908bca54d36a15d99469)
            check_type(argname="argument distribution_filter", value=distribution_filter, expected_type=type_hints["distribution_filter"])
            check_type(argname="argument range", value=range, expected_type=type_hints["range"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "distribution_filter": distribution_filter,
            "range": range,
        }

    @builtins.property
    def distribution_filter(self) -> builtins.str:
        '''A TimeSeries `monitoring filter <https://cloud.google.com/monitoring/api/v3/filters>`_ aggregating values to quantify the good service provided.

        Must have ValueType = DISTRIBUTION and
        MetricKind = DELTA or MetricKind = CUMULATIVE.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_slo#distribution_filter MonitoringSlo#distribution_filter}
        '''
        result = self._values.get("distribution_filter")
        assert result is not None, "Required property 'distribution_filter' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def range(
        self,
    ) -> "MonitoringSloWindowsBasedSliGoodTotalRatioThresholdPerformanceDistributionCutRange":
        '''range block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_slo#range MonitoringSlo#range}
        '''
        result = self._values.get("range")
        assert result is not None, "Required property 'range' is missing"
        return typing.cast("MonitoringSloWindowsBasedSliGoodTotalRatioThresholdPerformanceDistributionCutRange", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MonitoringSloWindowsBasedSliGoodTotalRatioThresholdPerformanceDistributionCut(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MonitoringSloWindowsBasedSliGoodTotalRatioThresholdPerformanceDistributionCutOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.monitoringSlo.MonitoringSloWindowsBasedSliGoodTotalRatioThresholdPerformanceDistributionCutOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1791f62b95bc4ff9e8cfc0c1fadd46e5b69c08ae847da8287ddc3d33db9e69ee)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putRange")
    def put_range(
        self,
        *,
        max: typing.Optional[jsii.Number] = None,
        min: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param max: max value for the range (inclusive). If not given, will be set to 0. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_slo#max MonitoringSlo#max}
        :param min: Min value for the range (inclusive). If not given, will be set to 0. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_slo#min MonitoringSlo#min}
        '''
        value = MonitoringSloWindowsBasedSliGoodTotalRatioThresholdPerformanceDistributionCutRange(
            max=max, min=min
        )

        return typing.cast(None, jsii.invoke(self, "putRange", [value]))

    @builtins.property
    @jsii.member(jsii_name="range")
    def range(
        self,
    ) -> "MonitoringSloWindowsBasedSliGoodTotalRatioThresholdPerformanceDistributionCutRangeOutputReference":
        return typing.cast("MonitoringSloWindowsBasedSliGoodTotalRatioThresholdPerformanceDistributionCutRangeOutputReference", jsii.get(self, "range"))

    @builtins.property
    @jsii.member(jsii_name="distributionFilterInput")
    def distribution_filter_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "distributionFilterInput"))

    @builtins.property
    @jsii.member(jsii_name="rangeInput")
    def range_input(
        self,
    ) -> typing.Optional["MonitoringSloWindowsBasedSliGoodTotalRatioThresholdPerformanceDistributionCutRange"]:
        return typing.cast(typing.Optional["MonitoringSloWindowsBasedSliGoodTotalRatioThresholdPerformanceDistributionCutRange"], jsii.get(self, "rangeInput"))

    @builtins.property
    @jsii.member(jsii_name="distributionFilter")
    def distribution_filter(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "distributionFilter"))

    @distribution_filter.setter
    def distribution_filter(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__47ac6b29e79701a79b7b5aa6e9d616618999442351e16b5d589760b73be2f353)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "distributionFilter", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[MonitoringSloWindowsBasedSliGoodTotalRatioThresholdPerformanceDistributionCut]:
        return typing.cast(typing.Optional[MonitoringSloWindowsBasedSliGoodTotalRatioThresholdPerformanceDistributionCut], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MonitoringSloWindowsBasedSliGoodTotalRatioThresholdPerformanceDistributionCut],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a570ffc81926463339fd203b39bd4ef6bf5b66f4f3fac0c9ff7e3dbcb82f3a0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.monitoringSlo.MonitoringSloWindowsBasedSliGoodTotalRatioThresholdPerformanceDistributionCutRange",
    jsii_struct_bases=[],
    name_mapping={"max": "max", "min": "min"},
)
class MonitoringSloWindowsBasedSliGoodTotalRatioThresholdPerformanceDistributionCutRange:
    def __init__(
        self,
        *,
        max: typing.Optional[jsii.Number] = None,
        min: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param max: max value for the range (inclusive). If not given, will be set to 0. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_slo#max MonitoringSlo#max}
        :param min: Min value for the range (inclusive). If not given, will be set to 0. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_slo#min MonitoringSlo#min}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc0a368a251dd14da75e784b3ab825511c9cc9aedf0ebc4315b6990bcd51fa6d)
            check_type(argname="argument max", value=max, expected_type=type_hints["max"])
            check_type(argname="argument min", value=min, expected_type=type_hints["min"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if max is not None:
            self._values["max"] = max
        if min is not None:
            self._values["min"] = min

    @builtins.property
    def max(self) -> typing.Optional[jsii.Number]:
        '''max value for the range (inclusive). If not given, will be set to 0.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_slo#max MonitoringSlo#max}
        '''
        result = self._values.get("max")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def min(self) -> typing.Optional[jsii.Number]:
        '''Min value for the range (inclusive). If not given, will be set to 0.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_slo#min MonitoringSlo#min}
        '''
        result = self._values.get("min")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MonitoringSloWindowsBasedSliGoodTotalRatioThresholdPerformanceDistributionCutRange(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MonitoringSloWindowsBasedSliGoodTotalRatioThresholdPerformanceDistributionCutRangeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.monitoringSlo.MonitoringSloWindowsBasedSliGoodTotalRatioThresholdPerformanceDistributionCutRangeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b4e7950d4c51ad16476a07ce5a313f7126e4f7e8ee37218df19826251d6e3751)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetMax")
    def reset_max(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMax", []))

    @jsii.member(jsii_name="resetMin")
    def reset_min(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMin", []))

    @builtins.property
    @jsii.member(jsii_name="maxInput")
    def max_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxInput"))

    @builtins.property
    @jsii.member(jsii_name="minInput")
    def min_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "minInput"))

    @builtins.property
    @jsii.member(jsii_name="max")
    def max(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "max"))

    @max.setter
    def max(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__71315b5e0f2c313d930fe012ca3c5299d5af146e51015210f5140929dd3f507d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "max", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="min")
    def min(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "min"))

    @min.setter
    def min(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__da49bd6bfcb40dc4e48f7b8f31d1356f04775d013d7291f58d6c455f62df69fd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "min", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[MonitoringSloWindowsBasedSliGoodTotalRatioThresholdPerformanceDistributionCutRange]:
        return typing.cast(typing.Optional[MonitoringSloWindowsBasedSliGoodTotalRatioThresholdPerformanceDistributionCutRange], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MonitoringSloWindowsBasedSliGoodTotalRatioThresholdPerformanceDistributionCutRange],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__593309e6c2688b9445b5b2a2d518e1b60c99ed8b32d8b12c4c3d340b82695dd9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.monitoringSlo.MonitoringSloWindowsBasedSliGoodTotalRatioThresholdPerformanceGoodTotalRatio",
    jsii_struct_bases=[],
    name_mapping={
        "bad_service_filter": "badServiceFilter",
        "good_service_filter": "goodServiceFilter",
        "total_service_filter": "totalServiceFilter",
    },
)
class MonitoringSloWindowsBasedSliGoodTotalRatioThresholdPerformanceGoodTotalRatio:
    def __init__(
        self,
        *,
        bad_service_filter: typing.Optional[builtins.str] = None,
        good_service_filter: typing.Optional[builtins.str] = None,
        total_service_filter: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param bad_service_filter: A TimeSeries `monitoring filter <https://cloud.google.com/monitoring/api/v3/filters>`_ quantifying bad service provided, either demanded service that was not provided or demanded service that was of inadequate quality. Exactly two of good, bad, or total service filter must be defined (where good + bad = total is assumed). Must have ValueType = DOUBLE or ValueType = INT64 and must have MetricKind = DELTA or MetricKind = CUMULATIVE. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_slo#bad_service_filter MonitoringSlo#bad_service_filter}
        :param good_service_filter: A TimeSeries `monitoring filter <https://cloud.google.com/monitoring/api/v3/filters>`_ quantifying good service provided. Exactly two of good, bad, or total service filter must be defined (where good + bad = total is assumed). Must have ValueType = DOUBLE or ValueType = INT64 and must have MetricKind = DELTA or MetricKind = CUMULATIVE. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_slo#good_service_filter MonitoringSlo#good_service_filter}
        :param total_service_filter: A TimeSeries `monitoring filter <https://cloud.google.com/monitoring/api/v3/filters>`_ quantifying total demanded service. Exactly two of good, bad, or total service filter must be defined (where good + bad = total is assumed). Must have ValueType = DOUBLE or ValueType = INT64 and must have MetricKind = DELTA or MetricKind = CUMULATIVE. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_slo#total_service_filter MonitoringSlo#total_service_filter}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ac504d247839ed1b679b672f7beada8943ec6a5248733036b8dd9f71a275cc0)
            check_type(argname="argument bad_service_filter", value=bad_service_filter, expected_type=type_hints["bad_service_filter"])
            check_type(argname="argument good_service_filter", value=good_service_filter, expected_type=type_hints["good_service_filter"])
            check_type(argname="argument total_service_filter", value=total_service_filter, expected_type=type_hints["total_service_filter"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if bad_service_filter is not None:
            self._values["bad_service_filter"] = bad_service_filter
        if good_service_filter is not None:
            self._values["good_service_filter"] = good_service_filter
        if total_service_filter is not None:
            self._values["total_service_filter"] = total_service_filter

    @builtins.property
    def bad_service_filter(self) -> typing.Optional[builtins.str]:
        '''A TimeSeries `monitoring filter <https://cloud.google.com/monitoring/api/v3/filters>`_ quantifying bad service provided, either demanded service that was not provided or demanded service that was of inadequate quality. Exactly two of good, bad, or total service filter must be defined (where good + bad = total is assumed).

        Must have ValueType = DOUBLE or ValueType = INT64 and
        must have MetricKind = DELTA or MetricKind = CUMULATIVE.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_slo#bad_service_filter MonitoringSlo#bad_service_filter}
        '''
        result = self._values.get("bad_service_filter")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def good_service_filter(self) -> typing.Optional[builtins.str]:
        '''A TimeSeries `monitoring filter <https://cloud.google.com/monitoring/api/v3/filters>`_ quantifying good service provided. Exactly two of good, bad, or total service filter must be defined (where good + bad = total is assumed).

        Must have ValueType = DOUBLE or ValueType = INT64 and
        must have MetricKind = DELTA or MetricKind = CUMULATIVE.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_slo#good_service_filter MonitoringSlo#good_service_filter}
        '''
        result = self._values.get("good_service_filter")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def total_service_filter(self) -> typing.Optional[builtins.str]:
        '''A TimeSeries `monitoring filter <https://cloud.google.com/monitoring/api/v3/filters>`_ quantifying total demanded service. Exactly two of good, bad, or total service filter must be defined (where good + bad = total is assumed).

        Must have ValueType = DOUBLE or ValueType = INT64 and
        must have MetricKind = DELTA or MetricKind = CUMULATIVE.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_slo#total_service_filter MonitoringSlo#total_service_filter}
        '''
        result = self._values.get("total_service_filter")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MonitoringSloWindowsBasedSliGoodTotalRatioThresholdPerformanceGoodTotalRatio(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MonitoringSloWindowsBasedSliGoodTotalRatioThresholdPerformanceGoodTotalRatioOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.monitoringSlo.MonitoringSloWindowsBasedSliGoodTotalRatioThresholdPerformanceGoodTotalRatioOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__00b9266df88644b25819798840a208983e84e39bcb2be1de6dcfa069626311cb)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetBadServiceFilter")
    def reset_bad_service_filter(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBadServiceFilter", []))

    @jsii.member(jsii_name="resetGoodServiceFilter")
    def reset_good_service_filter(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGoodServiceFilter", []))

    @jsii.member(jsii_name="resetTotalServiceFilter")
    def reset_total_service_filter(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTotalServiceFilter", []))

    @builtins.property
    @jsii.member(jsii_name="badServiceFilterInput")
    def bad_service_filter_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "badServiceFilterInput"))

    @builtins.property
    @jsii.member(jsii_name="goodServiceFilterInput")
    def good_service_filter_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "goodServiceFilterInput"))

    @builtins.property
    @jsii.member(jsii_name="totalServiceFilterInput")
    def total_service_filter_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "totalServiceFilterInput"))

    @builtins.property
    @jsii.member(jsii_name="badServiceFilter")
    def bad_service_filter(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "badServiceFilter"))

    @bad_service_filter.setter
    def bad_service_filter(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__325c616e8785d92ddc21907eb9caa22c8ca35fab9be822093f37072406a69faf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "badServiceFilter", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="goodServiceFilter")
    def good_service_filter(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "goodServiceFilter"))

    @good_service_filter.setter
    def good_service_filter(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2b144b1067236abe1ba9a075d850536d23dab34e78341406633f6601166ea0a1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "goodServiceFilter", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="totalServiceFilter")
    def total_service_filter(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "totalServiceFilter"))

    @total_service_filter.setter
    def total_service_filter(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b701a3010fae1833f70697893af0b3d1eca072b583703418afa0fb1a278b5fec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "totalServiceFilter", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[MonitoringSloWindowsBasedSliGoodTotalRatioThresholdPerformanceGoodTotalRatio]:
        return typing.cast(typing.Optional[MonitoringSloWindowsBasedSliGoodTotalRatioThresholdPerformanceGoodTotalRatio], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MonitoringSloWindowsBasedSliGoodTotalRatioThresholdPerformanceGoodTotalRatio],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__202b339889ba08d1cbddb0104d56412b14d48ade992a7ccdc23a2fa8edca06ae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class MonitoringSloWindowsBasedSliGoodTotalRatioThresholdPerformanceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.monitoringSlo.MonitoringSloWindowsBasedSliGoodTotalRatioThresholdPerformanceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7a00b1e247752f304e2d77592c68ce8ae950916e3aa351f072c5898876f47567)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putDistributionCut")
    def put_distribution_cut(
        self,
        *,
        distribution_filter: builtins.str,
        range: typing.Union[MonitoringSloWindowsBasedSliGoodTotalRatioThresholdPerformanceDistributionCutRange, typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param distribution_filter: A TimeSeries `monitoring filter <https://cloud.google.com/monitoring/api/v3/filters>`_ aggregating values to quantify the good service provided. Must have ValueType = DISTRIBUTION and MetricKind = DELTA or MetricKind = CUMULATIVE. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_slo#distribution_filter MonitoringSlo#distribution_filter}
        :param range: range block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_slo#range MonitoringSlo#range}
        '''
        value = MonitoringSloWindowsBasedSliGoodTotalRatioThresholdPerformanceDistributionCut(
            distribution_filter=distribution_filter, range=range
        )

        return typing.cast(None, jsii.invoke(self, "putDistributionCut", [value]))

    @jsii.member(jsii_name="putGoodTotalRatio")
    def put_good_total_ratio(
        self,
        *,
        bad_service_filter: typing.Optional[builtins.str] = None,
        good_service_filter: typing.Optional[builtins.str] = None,
        total_service_filter: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param bad_service_filter: A TimeSeries `monitoring filter <https://cloud.google.com/monitoring/api/v3/filters>`_ quantifying bad service provided, either demanded service that was not provided or demanded service that was of inadequate quality. Exactly two of good, bad, or total service filter must be defined (where good + bad = total is assumed). Must have ValueType = DOUBLE or ValueType = INT64 and must have MetricKind = DELTA or MetricKind = CUMULATIVE. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_slo#bad_service_filter MonitoringSlo#bad_service_filter}
        :param good_service_filter: A TimeSeries `monitoring filter <https://cloud.google.com/monitoring/api/v3/filters>`_ quantifying good service provided. Exactly two of good, bad, or total service filter must be defined (where good + bad = total is assumed). Must have ValueType = DOUBLE or ValueType = INT64 and must have MetricKind = DELTA or MetricKind = CUMULATIVE. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_slo#good_service_filter MonitoringSlo#good_service_filter}
        :param total_service_filter: A TimeSeries `monitoring filter <https://cloud.google.com/monitoring/api/v3/filters>`_ quantifying total demanded service. Exactly two of good, bad, or total service filter must be defined (where good + bad = total is assumed). Must have ValueType = DOUBLE or ValueType = INT64 and must have MetricKind = DELTA or MetricKind = CUMULATIVE. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_slo#total_service_filter MonitoringSlo#total_service_filter}
        '''
        value = MonitoringSloWindowsBasedSliGoodTotalRatioThresholdPerformanceGoodTotalRatio(
            bad_service_filter=bad_service_filter,
            good_service_filter=good_service_filter,
            total_service_filter=total_service_filter,
        )

        return typing.cast(None, jsii.invoke(self, "putGoodTotalRatio", [value]))

    @jsii.member(jsii_name="resetDistributionCut")
    def reset_distribution_cut(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDistributionCut", []))

    @jsii.member(jsii_name="resetGoodTotalRatio")
    def reset_good_total_ratio(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGoodTotalRatio", []))

    @builtins.property
    @jsii.member(jsii_name="distributionCut")
    def distribution_cut(
        self,
    ) -> MonitoringSloWindowsBasedSliGoodTotalRatioThresholdPerformanceDistributionCutOutputReference:
        return typing.cast(MonitoringSloWindowsBasedSliGoodTotalRatioThresholdPerformanceDistributionCutOutputReference, jsii.get(self, "distributionCut"))

    @builtins.property
    @jsii.member(jsii_name="goodTotalRatio")
    def good_total_ratio(
        self,
    ) -> MonitoringSloWindowsBasedSliGoodTotalRatioThresholdPerformanceGoodTotalRatioOutputReference:
        return typing.cast(MonitoringSloWindowsBasedSliGoodTotalRatioThresholdPerformanceGoodTotalRatioOutputReference, jsii.get(self, "goodTotalRatio"))

    @builtins.property
    @jsii.member(jsii_name="distributionCutInput")
    def distribution_cut_input(
        self,
    ) -> typing.Optional[MonitoringSloWindowsBasedSliGoodTotalRatioThresholdPerformanceDistributionCut]:
        return typing.cast(typing.Optional[MonitoringSloWindowsBasedSliGoodTotalRatioThresholdPerformanceDistributionCut], jsii.get(self, "distributionCutInput"))

    @builtins.property
    @jsii.member(jsii_name="goodTotalRatioInput")
    def good_total_ratio_input(
        self,
    ) -> typing.Optional[MonitoringSloWindowsBasedSliGoodTotalRatioThresholdPerformanceGoodTotalRatio]:
        return typing.cast(typing.Optional[MonitoringSloWindowsBasedSliGoodTotalRatioThresholdPerformanceGoodTotalRatio], jsii.get(self, "goodTotalRatioInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[MonitoringSloWindowsBasedSliGoodTotalRatioThresholdPerformance]:
        return typing.cast(typing.Optional[MonitoringSloWindowsBasedSliGoodTotalRatioThresholdPerformance], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MonitoringSloWindowsBasedSliGoodTotalRatioThresholdPerformance],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e7cb13cacc4ca7994b69c77ef5282d2e04e34da8c9f4de20a9c9afa8eadd0527)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.monitoringSlo.MonitoringSloWindowsBasedSliMetricMeanInRange",
    jsii_struct_bases=[],
    name_mapping={"range": "range", "time_series": "timeSeries"},
)
class MonitoringSloWindowsBasedSliMetricMeanInRange:
    def __init__(
        self,
        *,
        range: typing.Union["MonitoringSloWindowsBasedSliMetricMeanInRangeRange", typing.Dict[builtins.str, typing.Any]],
        time_series: builtins.str,
    ) -> None:
        '''
        :param range: range block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_slo#range MonitoringSlo#range}
        :param time_series: A `monitoring filter <https://cloud.google.com/monitoring/api/v3/filters>`_ specifying the TimeSeries to use for evaluating window The provided TimeSeries must have ValueType = INT64 or ValueType = DOUBLE and MetricKind = GAUGE. Mean value 'X' should satisfy 'range.min <= X <= range.max' under good service. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_slo#time_series MonitoringSlo#time_series}
        '''
        if isinstance(range, dict):
            range = MonitoringSloWindowsBasedSliMetricMeanInRangeRange(**range)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__361f396b9fb1d98450e1a871f476c737dcaa2f6c003156e6a8452f70973fb021)
            check_type(argname="argument range", value=range, expected_type=type_hints["range"])
            check_type(argname="argument time_series", value=time_series, expected_type=type_hints["time_series"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "range": range,
            "time_series": time_series,
        }

    @builtins.property
    def range(self) -> "MonitoringSloWindowsBasedSliMetricMeanInRangeRange":
        '''range block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_slo#range MonitoringSlo#range}
        '''
        result = self._values.get("range")
        assert result is not None, "Required property 'range' is missing"
        return typing.cast("MonitoringSloWindowsBasedSliMetricMeanInRangeRange", result)

    @builtins.property
    def time_series(self) -> builtins.str:
        '''A `monitoring filter <https://cloud.google.com/monitoring/api/v3/filters>`_ specifying the TimeSeries to use for evaluating window The provided TimeSeries must have ValueType = INT64 or ValueType = DOUBLE and MetricKind = GAUGE. Mean value 'X' should satisfy 'range.min <= X <= range.max' under good service.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_slo#time_series MonitoringSlo#time_series}
        '''
        result = self._values.get("time_series")
        assert result is not None, "Required property 'time_series' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MonitoringSloWindowsBasedSliMetricMeanInRange(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MonitoringSloWindowsBasedSliMetricMeanInRangeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.monitoringSlo.MonitoringSloWindowsBasedSliMetricMeanInRangeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8f8b3149ff855e5a54e6b29b68d9e4204930329477f01d5864d0f4c2fbc9e85d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putRange")
    def put_range(
        self,
        *,
        max: typing.Optional[jsii.Number] = None,
        min: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param max: max value for the range (inclusive). If not given, will be set to "infinity", defining an open range ">= range.min". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_slo#max MonitoringSlo#max}
        :param min: Min value for the range (inclusive). If not given, will be set to "-infinity", defining an open range "< range.max". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_slo#min MonitoringSlo#min}
        '''
        value = MonitoringSloWindowsBasedSliMetricMeanInRangeRange(max=max, min=min)

        return typing.cast(None, jsii.invoke(self, "putRange", [value]))

    @builtins.property
    @jsii.member(jsii_name="range")
    def range(
        self,
    ) -> "MonitoringSloWindowsBasedSliMetricMeanInRangeRangeOutputReference":
        return typing.cast("MonitoringSloWindowsBasedSliMetricMeanInRangeRangeOutputReference", jsii.get(self, "range"))

    @builtins.property
    @jsii.member(jsii_name="rangeInput")
    def range_input(
        self,
    ) -> typing.Optional["MonitoringSloWindowsBasedSliMetricMeanInRangeRange"]:
        return typing.cast(typing.Optional["MonitoringSloWindowsBasedSliMetricMeanInRangeRange"], jsii.get(self, "rangeInput"))

    @builtins.property
    @jsii.member(jsii_name="timeSeriesInput")
    def time_series_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "timeSeriesInput"))

    @builtins.property
    @jsii.member(jsii_name="timeSeries")
    def time_series(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "timeSeries"))

    @time_series.setter
    def time_series(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fb9fc4a404fcdcf2896057c1b77eb6329bf1305590307afce5ed2d517eead9d1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timeSeries", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[MonitoringSloWindowsBasedSliMetricMeanInRange]:
        return typing.cast(typing.Optional[MonitoringSloWindowsBasedSliMetricMeanInRange], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MonitoringSloWindowsBasedSliMetricMeanInRange],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c732dcc41873634191206ed1521e35f1dcb2eceecf5b16da8caa77732b820d97)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.monitoringSlo.MonitoringSloWindowsBasedSliMetricMeanInRangeRange",
    jsii_struct_bases=[],
    name_mapping={"max": "max", "min": "min"},
)
class MonitoringSloWindowsBasedSliMetricMeanInRangeRange:
    def __init__(
        self,
        *,
        max: typing.Optional[jsii.Number] = None,
        min: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param max: max value for the range (inclusive). If not given, will be set to "infinity", defining an open range ">= range.min". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_slo#max MonitoringSlo#max}
        :param min: Min value for the range (inclusive). If not given, will be set to "-infinity", defining an open range "< range.max". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_slo#min MonitoringSlo#min}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d694adda4d216d07795d270681c6275f3cfecc449c1fd0340761bb10cbb6368f)
            check_type(argname="argument max", value=max, expected_type=type_hints["max"])
            check_type(argname="argument min", value=min, expected_type=type_hints["min"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if max is not None:
            self._values["max"] = max
        if min is not None:
            self._values["min"] = min

    @builtins.property
    def max(self) -> typing.Optional[jsii.Number]:
        '''max value for the range (inclusive). If not given, will be set to "infinity", defining an open range ">= range.min".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_slo#max MonitoringSlo#max}
        '''
        result = self._values.get("max")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def min(self) -> typing.Optional[jsii.Number]:
        '''Min value for the range (inclusive). If not given, will be set to "-infinity", defining an open range "< range.max".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_slo#min MonitoringSlo#min}
        '''
        result = self._values.get("min")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MonitoringSloWindowsBasedSliMetricMeanInRangeRange(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MonitoringSloWindowsBasedSliMetricMeanInRangeRangeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.monitoringSlo.MonitoringSloWindowsBasedSliMetricMeanInRangeRangeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ed0f815e20b9d1519c0f8ee0885a98fcc9f319c54668047c91bc7ee67f580020)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetMax")
    def reset_max(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMax", []))

    @jsii.member(jsii_name="resetMin")
    def reset_min(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMin", []))

    @builtins.property
    @jsii.member(jsii_name="maxInput")
    def max_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxInput"))

    @builtins.property
    @jsii.member(jsii_name="minInput")
    def min_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "minInput"))

    @builtins.property
    @jsii.member(jsii_name="max")
    def max(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "max"))

    @max.setter
    def max(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d857e94d3d84748b6b8b007ec488211949ae47f550f680de45e6cf0b090b8a92)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "max", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="min")
    def min(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "min"))

    @min.setter
    def min(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__74d94ff2654e31fc5aa0bcbef16721f36aa8aedec207338ab80c75b86231a356)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "min", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[MonitoringSloWindowsBasedSliMetricMeanInRangeRange]:
        return typing.cast(typing.Optional[MonitoringSloWindowsBasedSliMetricMeanInRangeRange], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MonitoringSloWindowsBasedSliMetricMeanInRangeRange],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__097147ee2b264888712c04c1a0b660f83f08183de657ef63ca75f85830494111)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.monitoringSlo.MonitoringSloWindowsBasedSliMetricSumInRange",
    jsii_struct_bases=[],
    name_mapping={"range": "range", "time_series": "timeSeries"},
)
class MonitoringSloWindowsBasedSliMetricSumInRange:
    def __init__(
        self,
        *,
        range: typing.Union["MonitoringSloWindowsBasedSliMetricSumInRangeRange", typing.Dict[builtins.str, typing.Any]],
        time_series: builtins.str,
    ) -> None:
        '''
        :param range: range block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_slo#range MonitoringSlo#range}
        :param time_series: A `monitoring filter <https://cloud.google.com/monitoring/api/v3/filters>`_ specifying the TimeSeries to use for evaluating window quality. The provided TimeSeries must have ValueType = INT64 or ValueType = DOUBLE and MetricKind = GAUGE. Summed value 'X' should satisfy 'range.min <= X <= range.max' for a good window. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_slo#time_series MonitoringSlo#time_series}
        '''
        if isinstance(range, dict):
            range = MonitoringSloWindowsBasedSliMetricSumInRangeRange(**range)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4ef82b945a09b2b3f89d0ba7b8b250f448f4b8d609a6ba0692d62de100b9dffa)
            check_type(argname="argument range", value=range, expected_type=type_hints["range"])
            check_type(argname="argument time_series", value=time_series, expected_type=type_hints["time_series"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "range": range,
            "time_series": time_series,
        }

    @builtins.property
    def range(self) -> "MonitoringSloWindowsBasedSliMetricSumInRangeRange":
        '''range block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_slo#range MonitoringSlo#range}
        '''
        result = self._values.get("range")
        assert result is not None, "Required property 'range' is missing"
        return typing.cast("MonitoringSloWindowsBasedSliMetricSumInRangeRange", result)

    @builtins.property
    def time_series(self) -> builtins.str:
        '''A `monitoring filter <https://cloud.google.com/monitoring/api/v3/filters>`_ specifying the TimeSeries to use for evaluating window quality. The provided TimeSeries must have ValueType = INT64 or ValueType = DOUBLE and MetricKind = GAUGE.

        Summed value 'X' should satisfy
        'range.min <= X <= range.max' for a good window.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_slo#time_series MonitoringSlo#time_series}
        '''
        result = self._values.get("time_series")
        assert result is not None, "Required property 'time_series' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MonitoringSloWindowsBasedSliMetricSumInRange(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MonitoringSloWindowsBasedSliMetricSumInRangeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.monitoringSlo.MonitoringSloWindowsBasedSliMetricSumInRangeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3f47131a106fcf9cd6e099d94591dd5936a5a9d8face6f79546dc92403740266)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putRange")
    def put_range(
        self,
        *,
        max: typing.Optional[jsii.Number] = None,
        min: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param max: max value for the range (inclusive). If not given, will be set to "infinity", defining an open range ">= range.min". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_slo#max MonitoringSlo#max}
        :param min: Min value for the range (inclusive). If not given, will be set to "-infinity", defining an open range "< range.max". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_slo#min MonitoringSlo#min}
        '''
        value = MonitoringSloWindowsBasedSliMetricSumInRangeRange(max=max, min=min)

        return typing.cast(None, jsii.invoke(self, "putRange", [value]))

    @builtins.property
    @jsii.member(jsii_name="range")
    def range(
        self,
    ) -> "MonitoringSloWindowsBasedSliMetricSumInRangeRangeOutputReference":
        return typing.cast("MonitoringSloWindowsBasedSliMetricSumInRangeRangeOutputReference", jsii.get(self, "range"))

    @builtins.property
    @jsii.member(jsii_name="rangeInput")
    def range_input(
        self,
    ) -> typing.Optional["MonitoringSloWindowsBasedSliMetricSumInRangeRange"]:
        return typing.cast(typing.Optional["MonitoringSloWindowsBasedSliMetricSumInRangeRange"], jsii.get(self, "rangeInput"))

    @builtins.property
    @jsii.member(jsii_name="timeSeriesInput")
    def time_series_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "timeSeriesInput"))

    @builtins.property
    @jsii.member(jsii_name="timeSeries")
    def time_series(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "timeSeries"))

    @time_series.setter
    def time_series(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0013e6e34b538f22a264dc28954635858bc2a9f6f4ec410f98f6a9f33a75d64c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timeSeries", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[MonitoringSloWindowsBasedSliMetricSumInRange]:
        return typing.cast(typing.Optional[MonitoringSloWindowsBasedSliMetricSumInRange], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MonitoringSloWindowsBasedSliMetricSumInRange],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c318a7f6a6bee5cd43928b7e1f2d126113830b9276c1b7ad6296fd1bbb1f04d4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.monitoringSlo.MonitoringSloWindowsBasedSliMetricSumInRangeRange",
    jsii_struct_bases=[],
    name_mapping={"max": "max", "min": "min"},
)
class MonitoringSloWindowsBasedSliMetricSumInRangeRange:
    def __init__(
        self,
        *,
        max: typing.Optional[jsii.Number] = None,
        min: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param max: max value for the range (inclusive). If not given, will be set to "infinity", defining an open range ">= range.min". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_slo#max MonitoringSlo#max}
        :param min: Min value for the range (inclusive). If not given, will be set to "-infinity", defining an open range "< range.max". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_slo#min MonitoringSlo#min}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__518ee179b99666a150fa812d29c26332cae4b69ce1df8627b9bd351874dc67f4)
            check_type(argname="argument max", value=max, expected_type=type_hints["max"])
            check_type(argname="argument min", value=min, expected_type=type_hints["min"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if max is not None:
            self._values["max"] = max
        if min is not None:
            self._values["min"] = min

    @builtins.property
    def max(self) -> typing.Optional[jsii.Number]:
        '''max value for the range (inclusive). If not given, will be set to "infinity", defining an open range ">= range.min".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_slo#max MonitoringSlo#max}
        '''
        result = self._values.get("max")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def min(self) -> typing.Optional[jsii.Number]:
        '''Min value for the range (inclusive). If not given, will be set to "-infinity", defining an open range "< range.max".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_slo#min MonitoringSlo#min}
        '''
        result = self._values.get("min")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MonitoringSloWindowsBasedSliMetricSumInRangeRange(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MonitoringSloWindowsBasedSliMetricSumInRangeRangeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.monitoringSlo.MonitoringSloWindowsBasedSliMetricSumInRangeRangeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6185bf0602456b514255cdce23c5884ab841ab0d6f734af7a6a8795263211513)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetMax")
    def reset_max(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMax", []))

    @jsii.member(jsii_name="resetMin")
    def reset_min(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMin", []))

    @builtins.property
    @jsii.member(jsii_name="maxInput")
    def max_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxInput"))

    @builtins.property
    @jsii.member(jsii_name="minInput")
    def min_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "minInput"))

    @builtins.property
    @jsii.member(jsii_name="max")
    def max(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "max"))

    @max.setter
    def max(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__931f03d7fd5b691cbb8c92b9bc1b448acbf0eaa79cd9b82d77db3e44aff7ab7c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "max", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="min")
    def min(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "min"))

    @min.setter
    def min(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ad46789d1c5cab7f34188fc9653603373dbf9a5af25dfe1635cf38f9d3ab9a25)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "min", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[MonitoringSloWindowsBasedSliMetricSumInRangeRange]:
        return typing.cast(typing.Optional[MonitoringSloWindowsBasedSliMetricSumInRangeRange], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MonitoringSloWindowsBasedSliMetricSumInRangeRange],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__438a43939b0a738382e18e78970a4528c2bc299d6e43071dc8b2b9e53ca93e33)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class MonitoringSloWindowsBasedSliOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.monitoringSlo.MonitoringSloWindowsBasedSliOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7fe05b23378a8e9c86f0197acf5fab87cabc0d899d73195a68028b44e589ee5b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putGoodTotalRatioThreshold")
    def put_good_total_ratio_threshold(
        self,
        *,
        basic_sli_performance: typing.Optional[typing.Union[MonitoringSloWindowsBasedSliGoodTotalRatioThresholdBasicSliPerformance, typing.Dict[builtins.str, typing.Any]]] = None,
        performance: typing.Optional[typing.Union[MonitoringSloWindowsBasedSliGoodTotalRatioThresholdPerformance, typing.Dict[builtins.str, typing.Any]]] = None,
        threshold: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param basic_sli_performance: basic_sli_performance block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_slo#basic_sli_performance MonitoringSlo#basic_sli_performance}
        :param performance: performance block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_slo#performance MonitoringSlo#performance}
        :param threshold: If window performance >= threshold, the window is counted as good. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_slo#threshold MonitoringSlo#threshold}
        '''
        value = MonitoringSloWindowsBasedSliGoodTotalRatioThreshold(
            basic_sli_performance=basic_sli_performance,
            performance=performance,
            threshold=threshold,
        )

        return typing.cast(None, jsii.invoke(self, "putGoodTotalRatioThreshold", [value]))

    @jsii.member(jsii_name="putMetricMeanInRange")
    def put_metric_mean_in_range(
        self,
        *,
        range: typing.Union[MonitoringSloWindowsBasedSliMetricMeanInRangeRange, typing.Dict[builtins.str, typing.Any]],
        time_series: builtins.str,
    ) -> None:
        '''
        :param range: range block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_slo#range MonitoringSlo#range}
        :param time_series: A `monitoring filter <https://cloud.google.com/monitoring/api/v3/filters>`_ specifying the TimeSeries to use for evaluating window The provided TimeSeries must have ValueType = INT64 or ValueType = DOUBLE and MetricKind = GAUGE. Mean value 'X' should satisfy 'range.min <= X <= range.max' under good service. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_slo#time_series MonitoringSlo#time_series}
        '''
        value = MonitoringSloWindowsBasedSliMetricMeanInRange(
            range=range, time_series=time_series
        )

        return typing.cast(None, jsii.invoke(self, "putMetricMeanInRange", [value]))

    @jsii.member(jsii_name="putMetricSumInRange")
    def put_metric_sum_in_range(
        self,
        *,
        range: typing.Union[MonitoringSloWindowsBasedSliMetricSumInRangeRange, typing.Dict[builtins.str, typing.Any]],
        time_series: builtins.str,
    ) -> None:
        '''
        :param range: range block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_slo#range MonitoringSlo#range}
        :param time_series: A `monitoring filter <https://cloud.google.com/monitoring/api/v3/filters>`_ specifying the TimeSeries to use for evaluating window quality. The provided TimeSeries must have ValueType = INT64 or ValueType = DOUBLE and MetricKind = GAUGE. Summed value 'X' should satisfy 'range.min <= X <= range.max' for a good window. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_slo#time_series MonitoringSlo#time_series}
        '''
        value = MonitoringSloWindowsBasedSliMetricSumInRange(
            range=range, time_series=time_series
        )

        return typing.cast(None, jsii.invoke(self, "putMetricSumInRange", [value]))

    @jsii.member(jsii_name="resetGoodBadMetricFilter")
    def reset_good_bad_metric_filter(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGoodBadMetricFilter", []))

    @jsii.member(jsii_name="resetGoodTotalRatioThreshold")
    def reset_good_total_ratio_threshold(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGoodTotalRatioThreshold", []))

    @jsii.member(jsii_name="resetMetricMeanInRange")
    def reset_metric_mean_in_range(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMetricMeanInRange", []))

    @jsii.member(jsii_name="resetMetricSumInRange")
    def reset_metric_sum_in_range(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMetricSumInRange", []))

    @jsii.member(jsii_name="resetWindowPeriod")
    def reset_window_period(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWindowPeriod", []))

    @builtins.property
    @jsii.member(jsii_name="goodTotalRatioThreshold")
    def good_total_ratio_threshold(
        self,
    ) -> MonitoringSloWindowsBasedSliGoodTotalRatioThresholdOutputReference:
        return typing.cast(MonitoringSloWindowsBasedSliGoodTotalRatioThresholdOutputReference, jsii.get(self, "goodTotalRatioThreshold"))

    @builtins.property
    @jsii.member(jsii_name="metricMeanInRange")
    def metric_mean_in_range(
        self,
    ) -> MonitoringSloWindowsBasedSliMetricMeanInRangeOutputReference:
        return typing.cast(MonitoringSloWindowsBasedSliMetricMeanInRangeOutputReference, jsii.get(self, "metricMeanInRange"))

    @builtins.property
    @jsii.member(jsii_name="metricSumInRange")
    def metric_sum_in_range(
        self,
    ) -> MonitoringSloWindowsBasedSliMetricSumInRangeOutputReference:
        return typing.cast(MonitoringSloWindowsBasedSliMetricSumInRangeOutputReference, jsii.get(self, "metricSumInRange"))

    @builtins.property
    @jsii.member(jsii_name="goodBadMetricFilterInput")
    def good_bad_metric_filter_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "goodBadMetricFilterInput"))

    @builtins.property
    @jsii.member(jsii_name="goodTotalRatioThresholdInput")
    def good_total_ratio_threshold_input(
        self,
    ) -> typing.Optional[MonitoringSloWindowsBasedSliGoodTotalRatioThreshold]:
        return typing.cast(typing.Optional[MonitoringSloWindowsBasedSliGoodTotalRatioThreshold], jsii.get(self, "goodTotalRatioThresholdInput"))

    @builtins.property
    @jsii.member(jsii_name="metricMeanInRangeInput")
    def metric_mean_in_range_input(
        self,
    ) -> typing.Optional[MonitoringSloWindowsBasedSliMetricMeanInRange]:
        return typing.cast(typing.Optional[MonitoringSloWindowsBasedSliMetricMeanInRange], jsii.get(self, "metricMeanInRangeInput"))

    @builtins.property
    @jsii.member(jsii_name="metricSumInRangeInput")
    def metric_sum_in_range_input(
        self,
    ) -> typing.Optional[MonitoringSloWindowsBasedSliMetricSumInRange]:
        return typing.cast(typing.Optional[MonitoringSloWindowsBasedSliMetricSumInRange], jsii.get(self, "metricSumInRangeInput"))

    @builtins.property
    @jsii.member(jsii_name="windowPeriodInput")
    def window_period_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "windowPeriodInput"))

    @builtins.property
    @jsii.member(jsii_name="goodBadMetricFilter")
    def good_bad_metric_filter(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "goodBadMetricFilter"))

    @good_bad_metric_filter.setter
    def good_bad_metric_filter(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__487a0a89ba38a23348d34e15188be5b15adf5ef8b68e428f228002b747c0d9f4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "goodBadMetricFilter", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="windowPeriod")
    def window_period(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "windowPeriod"))

    @window_period.setter
    def window_period(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__760a0d010271810636e755021bf5efd13d19a471fcf1b02f0bdfd3601513eb94)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "windowPeriod", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[MonitoringSloWindowsBasedSli]:
        return typing.cast(typing.Optional[MonitoringSloWindowsBasedSli], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MonitoringSloWindowsBasedSli],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__70a9ab47dd724ac1d2096893f24ab5617528832f5dfeeed678b2ab9e32f37110)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "MonitoringSlo",
    "MonitoringSloBasicSli",
    "MonitoringSloBasicSliAvailability",
    "MonitoringSloBasicSliAvailabilityOutputReference",
    "MonitoringSloBasicSliLatency",
    "MonitoringSloBasicSliLatencyOutputReference",
    "MonitoringSloBasicSliOutputReference",
    "MonitoringSloConfig",
    "MonitoringSloRequestBasedSli",
    "MonitoringSloRequestBasedSliDistributionCut",
    "MonitoringSloRequestBasedSliDistributionCutOutputReference",
    "MonitoringSloRequestBasedSliDistributionCutRange",
    "MonitoringSloRequestBasedSliDistributionCutRangeOutputReference",
    "MonitoringSloRequestBasedSliGoodTotalRatio",
    "MonitoringSloRequestBasedSliGoodTotalRatioOutputReference",
    "MonitoringSloRequestBasedSliOutputReference",
    "MonitoringSloTimeouts",
    "MonitoringSloTimeoutsOutputReference",
    "MonitoringSloWindowsBasedSli",
    "MonitoringSloWindowsBasedSliGoodTotalRatioThreshold",
    "MonitoringSloWindowsBasedSliGoodTotalRatioThresholdBasicSliPerformance",
    "MonitoringSloWindowsBasedSliGoodTotalRatioThresholdBasicSliPerformanceAvailability",
    "MonitoringSloWindowsBasedSliGoodTotalRatioThresholdBasicSliPerformanceAvailabilityOutputReference",
    "MonitoringSloWindowsBasedSliGoodTotalRatioThresholdBasicSliPerformanceLatency",
    "MonitoringSloWindowsBasedSliGoodTotalRatioThresholdBasicSliPerformanceLatencyOutputReference",
    "MonitoringSloWindowsBasedSliGoodTotalRatioThresholdBasicSliPerformanceOutputReference",
    "MonitoringSloWindowsBasedSliGoodTotalRatioThresholdOutputReference",
    "MonitoringSloWindowsBasedSliGoodTotalRatioThresholdPerformance",
    "MonitoringSloWindowsBasedSliGoodTotalRatioThresholdPerformanceDistributionCut",
    "MonitoringSloWindowsBasedSliGoodTotalRatioThresholdPerformanceDistributionCutOutputReference",
    "MonitoringSloWindowsBasedSliGoodTotalRatioThresholdPerformanceDistributionCutRange",
    "MonitoringSloWindowsBasedSliGoodTotalRatioThresholdPerformanceDistributionCutRangeOutputReference",
    "MonitoringSloWindowsBasedSliGoodTotalRatioThresholdPerformanceGoodTotalRatio",
    "MonitoringSloWindowsBasedSliGoodTotalRatioThresholdPerformanceGoodTotalRatioOutputReference",
    "MonitoringSloWindowsBasedSliGoodTotalRatioThresholdPerformanceOutputReference",
    "MonitoringSloWindowsBasedSliMetricMeanInRange",
    "MonitoringSloWindowsBasedSliMetricMeanInRangeOutputReference",
    "MonitoringSloWindowsBasedSliMetricMeanInRangeRange",
    "MonitoringSloWindowsBasedSliMetricMeanInRangeRangeOutputReference",
    "MonitoringSloWindowsBasedSliMetricSumInRange",
    "MonitoringSloWindowsBasedSliMetricSumInRangeOutputReference",
    "MonitoringSloWindowsBasedSliMetricSumInRangeRange",
    "MonitoringSloWindowsBasedSliMetricSumInRangeRangeOutputReference",
    "MonitoringSloWindowsBasedSliOutputReference",
]

publication.publish()

def _typecheckingstub__207b652ab8f29be86224b293d4519cbf5091a04790795a5ca6ca6da683d2f304(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    goal: jsii.Number,
    service: builtins.str,
    basic_sli: typing.Optional[typing.Union[MonitoringSloBasicSli, typing.Dict[builtins.str, typing.Any]]] = None,
    calendar_period: typing.Optional[builtins.str] = None,
    display_name: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    request_based_sli: typing.Optional[typing.Union[MonitoringSloRequestBasedSli, typing.Dict[builtins.str, typing.Any]]] = None,
    rolling_period_days: typing.Optional[jsii.Number] = None,
    slo_id: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[MonitoringSloTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    user_labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    windows_based_sli: typing.Optional[typing.Union[MonitoringSloWindowsBasedSli, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__e43d18645fca18bdf331ec929bcd97d329d39ba2684bea5469cdc8f274b2cc51(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9066f60553036899e5b299db59154ae346e49161f31b2934b639589661534484(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57bab5a3af3e1d284e54421c3889dd951031b6d6ffecab839a10141a864ab57e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff95a8b0fcb6782f315b5b7692460344c144b9bee0392c513152e5c1e0fd544e(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2125d892d7024c202fd1897da5b0c9e987ba1c95fe8ed5b2329bb8d4e0f21a0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c80f39fe062ef3f1ef28c27bb0910f641c293eb653898d2be2e1ed4009273fbd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db0c86dfbefd61900a859460450810eab96d5f044a0b44ad8468fbac07b48339(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c01709cd6776bbb195c1bfc8243b774ef1a970d5d3a7eec2a56efe933c9eb47(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6cbfc76eee1c044ab03df264d8b67f2aa5ff856cf7c053541400e846ab3596ee(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a000caab5276cd9471152b25140a03e972abc5f4448962316100f3dec116326(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__772cc51c21ae02acf20f08f028fab38ef4663d5374642cca1ce08e4b252024ae(
    *,
    availability: typing.Optional[typing.Union[MonitoringSloBasicSliAvailability, typing.Dict[builtins.str, typing.Any]]] = None,
    latency: typing.Optional[typing.Union[MonitoringSloBasicSliLatency, typing.Dict[builtins.str, typing.Any]]] = None,
    location: typing.Optional[typing.Sequence[builtins.str]] = None,
    method: typing.Optional[typing.Sequence[builtins.str]] = None,
    version: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__47e95fd062f3c2da8ce7524a2c46ce75ef6789f9afa30bcba0495061a9c77802(
    *,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__807b8e97e94af37ae7b74b18fa5766bafcd3e16c6686065ac16fe28c32f0749f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5bc8a298c0763d0a18bbb9a648c6c73d46a7c2551279af0f1c4ae68e6c6c66af(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a162a1dcff0d464afde8d8a46c85c7de31ba22dc430343af32d5e7b1d2455b73(
    value: typing.Optional[MonitoringSloBasicSliAvailability],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61da1433c687348106428e6099b255da5a7a9a7587af61765d79190fdb7a19d9(
    *,
    threshold: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba4a0ec4a9469e32f8e91faee562efdcfecc2502dd8b00e918ed69a275799423(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af33329d6f69546c5439382d004212cbbed5340ead6897b2aed06084d1bdf56d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e47211385bf6b15ed1864a549dbeb16da2cf216b6b321743c2f1ec36139cd4a5(
    value: typing.Optional[MonitoringSloBasicSliLatency],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7781601bc68352b81045d6c2d12859ab6c8028201fa947a03febf9ecaae5a6cc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6be21f928c84cc328aae597a9c57738e0c3d91c64541ffbcda3316a9b7bfaf4(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2aca4c31372e9847e3911397548f478a90dc2e08b2e9144e2772c253ed918ac0(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__abeecac0bbe5ef164b09ff78f4b0cc6b5ade23d01d2003aed1d1a00d7f002b3b(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80521bbee05e66a47440c1f5d43646bc5fc616a765e0025960580b8f67f9e3fd(
    value: typing.Optional[MonitoringSloBasicSli],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1778f877d5d053c2d3a19988d224711bdc293b12708b21698f06e3ecec3edda(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    goal: jsii.Number,
    service: builtins.str,
    basic_sli: typing.Optional[typing.Union[MonitoringSloBasicSli, typing.Dict[builtins.str, typing.Any]]] = None,
    calendar_period: typing.Optional[builtins.str] = None,
    display_name: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    request_based_sli: typing.Optional[typing.Union[MonitoringSloRequestBasedSli, typing.Dict[builtins.str, typing.Any]]] = None,
    rolling_period_days: typing.Optional[jsii.Number] = None,
    slo_id: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[MonitoringSloTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    user_labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    windows_based_sli: typing.Optional[typing.Union[MonitoringSloWindowsBasedSli, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1f0a300fc6b2b4e90c116bcd28b0a2bcd187ca369b466d5c53f0ddc10e98583(
    *,
    distribution_cut: typing.Optional[typing.Union[MonitoringSloRequestBasedSliDistributionCut, typing.Dict[builtins.str, typing.Any]]] = None,
    good_total_ratio: typing.Optional[typing.Union[MonitoringSloRequestBasedSliGoodTotalRatio, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fced9f8643c35bebf070f5919492c2f10d30f77e5edd120c0a6980227402073a(
    *,
    distribution_filter: builtins.str,
    range: typing.Union[MonitoringSloRequestBasedSliDistributionCutRange, typing.Dict[builtins.str, typing.Any]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e8ef88d7e237e9a30a7d3511d29fb5d039a284d72f3289594b50fbc3090d7d1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef411de09906fd84c2e654c3f606691e4cbdb6799c859415b56b99b5ef55f4df(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__216afbd19fbeb75120dd4ea774c6e6974e8bfe011360d762474e13378e3ca06e(
    value: typing.Optional[MonitoringSloRequestBasedSliDistributionCut],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28e9d5029a81bf6dc0c01362c78d0b0620d6d6683773bfedc8d0129eaae26568(
    *,
    max: typing.Optional[jsii.Number] = None,
    min: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57a8f07586b0d71eb49ba27e66a8522ae7def26c215f75f2498247da7b63994d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2668efc3e93fa1a8d14b33413379544e2f26c702b7804cbb864ad39e0a748ed3(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4537b5781a714853d26a9c5d8d67eedb6d3866da925e4fb251ce5e7db87a57ad(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4d5cade2ebe0c44fcc0e27fa3956eaaaf5359ed77009693b3aeb87fd1f77ba9(
    value: typing.Optional[MonitoringSloRequestBasedSliDistributionCutRange],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ed687ed0fbf28eb538bf4c02d97ee323ba0dc75e3ebe20c5544ff793dc3cff2(
    *,
    bad_service_filter: typing.Optional[builtins.str] = None,
    good_service_filter: typing.Optional[builtins.str] = None,
    total_service_filter: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__891b6d25f5f34243c36d0c0c3d0e39a67b9ddfa42ea3817d2600a410395c49bc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__964586f5cc1c36e7d2a0260b4b09db9955d65c7aa0ae5c041d61f67d90e2c5f7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ffaaaa1cedb4e3c315e6cc26da3f991db8ccad83195c778af340c4e84bbdced9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7be69f76f64014b370acfdbed6df8b2f66151e50e63d21a1443347b7e42d594e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ff3ca33c63c18221e0d4c5677e0a6d90071c1e15682778a5de75c9251e4ef1e(
    value: typing.Optional[MonitoringSloRequestBasedSliGoodTotalRatio],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd08559d56778789a60789a5781768897fcddeec96b52ede485eb1ff0d892deb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3c035af86257ca2d2797ae5ba7fc711d3ff3e7adb5f351d6e2dec48099c4488(
    value: typing.Optional[MonitoringSloRequestBasedSli],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__120f2bd4e2ffae44bd7ce2216e8935f923951ab5fdd23d05885ac6481a831cb2(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13d536094c4de2069c68ff0d620c26224eb0d848ef4b15bc440c388362d6dc23(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc785ed8e0af3bee5f8343591135fb41a4edbead1f88d483bede64160a258b4b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2eaaa9f70ed1a1c8cb70268267646e8a3c03a7681e9c0ea9c4426ec1f3f4b0c5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7d637d05a96948397413aa468f18ef905379d298f89631c22f037e2ce1e45d0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc49ededaea616782b974b2c6d0789568a34b91fa66ac4e366654a1259ff1a11(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MonitoringSloTimeouts]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60645092bab8621d94a4a2c559ae520dec5295a7217536df141e41d394604f6a(
    *,
    good_bad_metric_filter: typing.Optional[builtins.str] = None,
    good_total_ratio_threshold: typing.Optional[typing.Union[MonitoringSloWindowsBasedSliGoodTotalRatioThreshold, typing.Dict[builtins.str, typing.Any]]] = None,
    metric_mean_in_range: typing.Optional[typing.Union[MonitoringSloWindowsBasedSliMetricMeanInRange, typing.Dict[builtins.str, typing.Any]]] = None,
    metric_sum_in_range: typing.Optional[typing.Union[MonitoringSloWindowsBasedSliMetricSumInRange, typing.Dict[builtins.str, typing.Any]]] = None,
    window_period: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__efe1aa2237c56694972671501cdba5fcd2130274120796c81aa8f81f19d70a2a(
    *,
    basic_sli_performance: typing.Optional[typing.Union[MonitoringSloWindowsBasedSliGoodTotalRatioThresholdBasicSliPerformance, typing.Dict[builtins.str, typing.Any]]] = None,
    performance: typing.Optional[typing.Union[MonitoringSloWindowsBasedSliGoodTotalRatioThresholdPerformance, typing.Dict[builtins.str, typing.Any]]] = None,
    threshold: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f52fe944f229d4446f0a8e53fb27a6ef67ebb7e40e1b65f870ee965768d22081(
    *,
    availability: typing.Optional[typing.Union[MonitoringSloWindowsBasedSliGoodTotalRatioThresholdBasicSliPerformanceAvailability, typing.Dict[builtins.str, typing.Any]]] = None,
    latency: typing.Optional[typing.Union[MonitoringSloWindowsBasedSliGoodTotalRatioThresholdBasicSliPerformanceLatency, typing.Dict[builtins.str, typing.Any]]] = None,
    location: typing.Optional[typing.Sequence[builtins.str]] = None,
    method: typing.Optional[typing.Sequence[builtins.str]] = None,
    version: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e79c2af469e4d210fcb5e77624e4c6a980e881f4bd2c1cec32b9a69a26edc71(
    *,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bbd93368815745a68acc29db8470d3f9a3d75977b4da44f38c58a514d0da6748(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c279453c5eb9b4d1a3ca6663fc6b1bb5e34df92ae1aa255bd1039f98a7baaefd(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ca27d90c1a0e255a064e3df60804bfcfcff86e2aa340b978f10ae9d027af0f7(
    value: typing.Optional[MonitoringSloWindowsBasedSliGoodTotalRatioThresholdBasicSliPerformanceAvailability],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__139a2cdc410a78f46967381e9607401f3b35a36f0724fae463021a29e77f986e(
    *,
    threshold: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__56f4600c244bf85746af169db966e9b4d90101131dc1e703b67b94f00dbbb3ee(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d40ce047f8c4191bd1842dd53a3d3ef89087f8d8b844e30431d93132ceb7a8e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c86279a98fab1e83f1bafd468883b16a471e65456bfbd439a78983d433fec70(
    value: typing.Optional[MonitoringSloWindowsBasedSliGoodTotalRatioThresholdBasicSliPerformanceLatency],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b57d11014e9ad6617025f7b7b9392f7e8469f3e3903e02d99b4ecd80ca6b183c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c421a37196d5e60e42116ac782444c55ff72f2a2768a6da909b9e67506996908(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ee89bf83ff6f544bd5d41d51e46fa4982c23c1b6eb578434a5f573824f75da7(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2aa8064083564254dc05825fbb18123d434d4db363250a7c603df4634fb404a5(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52c0d8b0c48fcc2170c359921a44c4928f469f7d7386a2940f44c61e9c77dd4c(
    value: typing.Optional[MonitoringSloWindowsBasedSliGoodTotalRatioThresholdBasicSliPerformance],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ec89540a70bc796c123741e79587ba62772b4bb3547436ad6d068b700cd7917(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__182b6f98799ebca30d7ebdc7e6a5029e83f59365ab74f4a2e7580bb1c6e05190(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__200a7c5430ed167fdbac5c0e3e6b9d4a3524f3ea75545f4575ac74d082eeba3a(
    value: typing.Optional[MonitoringSloWindowsBasedSliGoodTotalRatioThreshold],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aeca6a1579c7b112ef92f401a2f695f9ced8457520ff08697c92b49529f9615b(
    *,
    distribution_cut: typing.Optional[typing.Union[MonitoringSloWindowsBasedSliGoodTotalRatioThresholdPerformanceDistributionCut, typing.Dict[builtins.str, typing.Any]]] = None,
    good_total_ratio: typing.Optional[typing.Union[MonitoringSloWindowsBasedSliGoodTotalRatioThresholdPerformanceGoodTotalRatio, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__21f253cfbb05e2d148de7eadfdeea95a4502590acd46908bca54d36a15d99469(
    *,
    distribution_filter: builtins.str,
    range: typing.Union[MonitoringSloWindowsBasedSliGoodTotalRatioThresholdPerformanceDistributionCutRange, typing.Dict[builtins.str, typing.Any]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1791f62b95bc4ff9e8cfc0c1fadd46e5b69c08ae847da8287ddc3d33db9e69ee(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__47ac6b29e79701a79b7b5aa6e9d616618999442351e16b5d589760b73be2f353(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a570ffc81926463339fd203b39bd4ef6bf5b66f4f3fac0c9ff7e3dbcb82f3a0(
    value: typing.Optional[MonitoringSloWindowsBasedSliGoodTotalRatioThresholdPerformanceDistributionCut],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc0a368a251dd14da75e784b3ab825511c9cc9aedf0ebc4315b6990bcd51fa6d(
    *,
    max: typing.Optional[jsii.Number] = None,
    min: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4e7950d4c51ad16476a07ce5a313f7126e4f7e8ee37218df19826251d6e3751(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71315b5e0f2c313d930fe012ca3c5299d5af146e51015210f5140929dd3f507d(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da49bd6bfcb40dc4e48f7b8f31d1356f04775d013d7291f58d6c455f62df69fd(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__593309e6c2688b9445b5b2a2d518e1b60c99ed8b32d8b12c4c3d340b82695dd9(
    value: typing.Optional[MonitoringSloWindowsBasedSliGoodTotalRatioThresholdPerformanceDistributionCutRange],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ac504d247839ed1b679b672f7beada8943ec6a5248733036b8dd9f71a275cc0(
    *,
    bad_service_filter: typing.Optional[builtins.str] = None,
    good_service_filter: typing.Optional[builtins.str] = None,
    total_service_filter: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00b9266df88644b25819798840a208983e84e39bcb2be1de6dcfa069626311cb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__325c616e8785d92ddc21907eb9caa22c8ca35fab9be822093f37072406a69faf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b144b1067236abe1ba9a075d850536d23dab34e78341406633f6601166ea0a1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b701a3010fae1833f70697893af0b3d1eca072b583703418afa0fb1a278b5fec(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__202b339889ba08d1cbddb0104d56412b14d48ade992a7ccdc23a2fa8edca06ae(
    value: typing.Optional[MonitoringSloWindowsBasedSliGoodTotalRatioThresholdPerformanceGoodTotalRatio],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a00b1e247752f304e2d77592c68ce8ae950916e3aa351f072c5898876f47567(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7cb13cacc4ca7994b69c77ef5282d2e04e34da8c9f4de20a9c9afa8eadd0527(
    value: typing.Optional[MonitoringSloWindowsBasedSliGoodTotalRatioThresholdPerformance],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__361f396b9fb1d98450e1a871f476c737dcaa2f6c003156e6a8452f70973fb021(
    *,
    range: typing.Union[MonitoringSloWindowsBasedSliMetricMeanInRangeRange, typing.Dict[builtins.str, typing.Any]],
    time_series: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f8b3149ff855e5a54e6b29b68d9e4204930329477f01d5864d0f4c2fbc9e85d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb9fc4a404fcdcf2896057c1b77eb6329bf1305590307afce5ed2d517eead9d1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c732dcc41873634191206ed1521e35f1dcb2eceecf5b16da8caa77732b820d97(
    value: typing.Optional[MonitoringSloWindowsBasedSliMetricMeanInRange],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d694adda4d216d07795d270681c6275f3cfecc449c1fd0340761bb10cbb6368f(
    *,
    max: typing.Optional[jsii.Number] = None,
    min: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed0f815e20b9d1519c0f8ee0885a98fcc9f319c54668047c91bc7ee67f580020(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d857e94d3d84748b6b8b007ec488211949ae47f550f680de45e6cf0b090b8a92(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74d94ff2654e31fc5aa0bcbef16721f36aa8aedec207338ab80c75b86231a356(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__097147ee2b264888712c04c1a0b660f83f08183de657ef63ca75f85830494111(
    value: typing.Optional[MonitoringSloWindowsBasedSliMetricMeanInRangeRange],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ef82b945a09b2b3f89d0ba7b8b250f448f4b8d609a6ba0692d62de100b9dffa(
    *,
    range: typing.Union[MonitoringSloWindowsBasedSliMetricSumInRangeRange, typing.Dict[builtins.str, typing.Any]],
    time_series: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f47131a106fcf9cd6e099d94591dd5936a5a9d8face6f79546dc92403740266(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0013e6e34b538f22a264dc28954635858bc2a9f6f4ec410f98f6a9f33a75d64c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c318a7f6a6bee5cd43928b7e1f2d126113830b9276c1b7ad6296fd1bbb1f04d4(
    value: typing.Optional[MonitoringSloWindowsBasedSliMetricSumInRange],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__518ee179b99666a150fa812d29c26332cae4b69ce1df8627b9bd351874dc67f4(
    *,
    max: typing.Optional[jsii.Number] = None,
    min: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6185bf0602456b514255cdce23c5884ab841ab0d6f734af7a6a8795263211513(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__931f03d7fd5b691cbb8c92b9bc1b448acbf0eaa79cd9b82d77db3e44aff7ab7c(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad46789d1c5cab7f34188fc9653603373dbf9a5af25dfe1635cf38f9d3ab9a25(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__438a43939b0a738382e18e78970a4528c2bc299d6e43071dc8b2b9e53ca93e33(
    value: typing.Optional[MonitoringSloWindowsBasedSliMetricSumInRangeRange],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7fe05b23378a8e9c86f0197acf5fab87cabc0d899d73195a68028b44e589ee5b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__487a0a89ba38a23348d34e15188be5b15adf5ef8b68e428f228002b747c0d9f4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__760a0d010271810636e755021bf5efd13d19a471fcf1b02f0bdfd3601513eb94(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__70a9ab47dd724ac1d2096893f24ab5617528832f5dfeeed678b2ab9e32f37110(
    value: typing.Optional[MonitoringSloWindowsBasedSli],
) -> None:
    """Type checking stubs"""
    pass
