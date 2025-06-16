r'''
# `google_monitoring_slo`

Refer to the Terraform Registry for docs: [`google_monitoring_slo`](https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_monitoring_slo).
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


class GoogleMonitoringSlo(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleMonitoringSlo.GoogleMonitoringSlo",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_monitoring_slo google_monitoring_slo}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        goal: jsii.Number,
        service: builtins.str,
        basic_sli: typing.Optional[typing.Union["GoogleMonitoringSloBasicSli", typing.Dict[builtins.str, typing.Any]]] = None,
        calendar_period: typing.Optional[builtins.str] = None,
        display_name: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        request_based_sli: typing.Optional[typing.Union["GoogleMonitoringSloRequestBasedSli", typing.Dict[builtins.str, typing.Any]]] = None,
        rolling_period_days: typing.Optional[jsii.Number] = None,
        slo_id: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["GoogleMonitoringSloTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        user_labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        windows_based_sli: typing.Optional[typing.Union["GoogleMonitoringSloWindowsBasedSli", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_monitoring_slo google_monitoring_slo} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param goal: The fraction of service that must be good in order for this objective to be met. 0 < goal <= 0.999 Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_monitoring_slo#goal GoogleMonitoringSlo#goal}
        :param service: ID of the service to which this SLO belongs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_monitoring_slo#service GoogleMonitoringSlo#service}
        :param basic_sli: basic_sli block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_monitoring_slo#basic_sli GoogleMonitoringSlo#basic_sli}
        :param calendar_period: A calendar period, semantically "since the start of the current ". Possible values: ["DAY", "WEEK", "FORTNIGHT", "MONTH"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_monitoring_slo#calendar_period GoogleMonitoringSlo#calendar_period}
        :param display_name: Name used for UI elements listing this SLO. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_monitoring_slo#display_name GoogleMonitoringSlo#display_name}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_monitoring_slo#id GoogleMonitoringSlo#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_monitoring_slo#project GoogleMonitoringSlo#project}.
        :param request_based_sli: request_based_sli block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_monitoring_slo#request_based_sli GoogleMonitoringSlo#request_based_sli}
        :param rolling_period_days: A rolling time period, semantically "in the past X days". Must be between 1 to 30 days, inclusive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_monitoring_slo#rolling_period_days GoogleMonitoringSlo#rolling_period_days}
        :param slo_id: The id to use for this ServiceLevelObjective. If omitted, an id will be generated instead. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_monitoring_slo#slo_id GoogleMonitoringSlo#slo_id}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_monitoring_slo#timeouts GoogleMonitoringSlo#timeouts}
        :param user_labels: This field is intended to be used for organizing and identifying the AlertPolicy objects.The field can contain up to 64 entries. Each key and value is limited to 63 Unicode characters or 128 bytes, whichever is smaller. Labels and values can contain only lowercase letters, numerals, underscores, and dashes. Keys must begin with a letter. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_monitoring_slo#user_labels GoogleMonitoringSlo#user_labels}
        :param windows_based_sli: windows_based_sli block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_monitoring_slo#windows_based_sli GoogleMonitoringSlo#windows_based_sli}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6f8e48c39632cd11ed5c735a8e97888def468302d75498f6ca6dfd8c54bb9844)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = GoogleMonitoringSloConfig(
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
        '''Generates CDKTF code for importing a GoogleMonitoringSlo resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the GoogleMonitoringSlo to import.
        :param import_from_id: The id of the existing GoogleMonitoringSlo that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_monitoring_slo#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the GoogleMonitoringSlo to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f6e0c11c3bf4a330cdf40e099525f3f23f2c4a0461aa4a0c835f983c612b7920)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putBasicSli")
    def put_basic_sli(
        self,
        *,
        availability: typing.Optional[typing.Union["GoogleMonitoringSloBasicSliAvailability", typing.Dict[builtins.str, typing.Any]]] = None,
        latency: typing.Optional[typing.Union["GoogleMonitoringSloBasicSliLatency", typing.Dict[builtins.str, typing.Any]]] = None,
        location: typing.Optional[typing.Sequence[builtins.str]] = None,
        method: typing.Optional[typing.Sequence[builtins.str]] = None,
        version: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param availability: availability block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_monitoring_slo#availability GoogleMonitoringSlo#availability}
        :param latency: latency block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_monitoring_slo#latency GoogleMonitoringSlo#latency}
        :param location: An optional set of locations to which this SLI is relevant. Telemetry from other locations will not be used to calculate performance for this SLI. If omitted, this SLI applies to all locations in which the Service has activity. For service types that don't support breaking down by location, setting this field will result in an error. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_monitoring_slo#location GoogleMonitoringSlo#location}
        :param method: An optional set of RPCs to which this SLI is relevant. Telemetry from other methods will not be used to calculate performance for this SLI. If omitted, this SLI applies to all the Service's methods. For service types that don't support breaking down by method, setting this field will result in an error. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_monitoring_slo#method GoogleMonitoringSlo#method}
        :param version: The set of API versions to which this SLI is relevant. Telemetry from other API versions will not be used to calculate performance for this SLI. If omitted, this SLI applies to all API versions. For service types that don't support breaking down by version, setting this field will result in an error. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_monitoring_slo#version GoogleMonitoringSlo#version}
        '''
        value = GoogleMonitoringSloBasicSli(
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
        distribution_cut: typing.Optional[typing.Union["GoogleMonitoringSloRequestBasedSliDistributionCut", typing.Dict[builtins.str, typing.Any]]] = None,
        good_total_ratio: typing.Optional[typing.Union["GoogleMonitoringSloRequestBasedSliGoodTotalRatio", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param distribution_cut: distribution_cut block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_monitoring_slo#distribution_cut GoogleMonitoringSlo#distribution_cut}
        :param good_total_ratio: good_total_ratio block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_monitoring_slo#good_total_ratio GoogleMonitoringSlo#good_total_ratio}
        '''
        value = GoogleMonitoringSloRequestBasedSli(
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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_monitoring_slo#create GoogleMonitoringSlo#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_monitoring_slo#delete GoogleMonitoringSlo#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_monitoring_slo#update GoogleMonitoringSlo#update}.
        '''
        value = GoogleMonitoringSloTimeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="putWindowsBasedSli")
    def put_windows_based_sli(
        self,
        *,
        good_bad_metric_filter: typing.Optional[builtins.str] = None,
        good_total_ratio_threshold: typing.Optional[typing.Union["GoogleMonitoringSloWindowsBasedSliGoodTotalRatioThreshold", typing.Dict[builtins.str, typing.Any]]] = None,
        metric_mean_in_range: typing.Optional[typing.Union["GoogleMonitoringSloWindowsBasedSliMetricMeanInRange", typing.Dict[builtins.str, typing.Any]]] = None,
        metric_sum_in_range: typing.Optional[typing.Union["GoogleMonitoringSloWindowsBasedSliMetricSumInRange", typing.Dict[builtins.str, typing.Any]]] = None,
        window_period: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param good_bad_metric_filter: A TimeSeries `monitoring filter <https://cloud.google.com/monitoring/api/v3/filters>`_ with ValueType = BOOL. The window is good if any true values appear in the window. One of 'good_bad_metric_filter', 'good_total_ratio_threshold', 'metric_mean_in_range', 'metric_sum_in_range' must be set for 'windows_based_sli'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_monitoring_slo#good_bad_metric_filter GoogleMonitoringSlo#good_bad_metric_filter}
        :param good_total_ratio_threshold: good_total_ratio_threshold block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_monitoring_slo#good_total_ratio_threshold GoogleMonitoringSlo#good_total_ratio_threshold}
        :param metric_mean_in_range: metric_mean_in_range block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_monitoring_slo#metric_mean_in_range GoogleMonitoringSlo#metric_mean_in_range}
        :param metric_sum_in_range: metric_sum_in_range block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_monitoring_slo#metric_sum_in_range GoogleMonitoringSlo#metric_sum_in_range}
        :param window_period: Duration over which window quality is evaluated, given as a duration string "{X}s" representing X seconds. Must be an integer fraction of a day and at least 60s. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_monitoring_slo#window_period GoogleMonitoringSlo#window_period}
        '''
        value = GoogleMonitoringSloWindowsBasedSli(
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
    def basic_sli(self) -> "GoogleMonitoringSloBasicSliOutputReference":
        return typing.cast("GoogleMonitoringSloBasicSliOutputReference", jsii.get(self, "basicSli"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="requestBasedSli")
    def request_based_sli(self) -> "GoogleMonitoringSloRequestBasedSliOutputReference":
        return typing.cast("GoogleMonitoringSloRequestBasedSliOutputReference", jsii.get(self, "requestBasedSli"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "GoogleMonitoringSloTimeoutsOutputReference":
        return typing.cast("GoogleMonitoringSloTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="windowsBasedSli")
    def windows_based_sli(self) -> "GoogleMonitoringSloWindowsBasedSliOutputReference":
        return typing.cast("GoogleMonitoringSloWindowsBasedSliOutputReference", jsii.get(self, "windowsBasedSli"))

    @builtins.property
    @jsii.member(jsii_name="basicSliInput")
    def basic_sli_input(self) -> typing.Optional["GoogleMonitoringSloBasicSli"]:
        return typing.cast(typing.Optional["GoogleMonitoringSloBasicSli"], jsii.get(self, "basicSliInput"))

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
    ) -> typing.Optional["GoogleMonitoringSloRequestBasedSli"]:
        return typing.cast(typing.Optional["GoogleMonitoringSloRequestBasedSli"], jsii.get(self, "requestBasedSliInput"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleMonitoringSloTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleMonitoringSloTimeouts"]], jsii.get(self, "timeoutsInput"))

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
    ) -> typing.Optional["GoogleMonitoringSloWindowsBasedSli"]:
        return typing.cast(typing.Optional["GoogleMonitoringSloWindowsBasedSli"], jsii.get(self, "windowsBasedSliInput"))

    @builtins.property
    @jsii.member(jsii_name="calendarPeriod")
    def calendar_period(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "calendarPeriod"))

    @calendar_period.setter
    def calendar_period(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ebf5d267625730c1e1ba533eae10dfcaeeb3fc25292a2be5133b83a118179f5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "calendarPeriod", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="displayName")
    def display_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "displayName"))

    @display_name.setter
    def display_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9606d9c0c9411927a0eff528703da27f8bb182e048df1fff2c28fd5c2685af2b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "displayName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="goal")
    def goal(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "goal"))

    @goal.setter
    def goal(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8c171ad308da7188439adcb7f9351802422a696341abfbd76b6d76126b57730b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "goal", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e500661d821e8d8289ffa45f8a9286fea606dee830fdece77a20266af196028f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9434368644b308fbb513695227d65d1e501aa90c83640b5e2828be738f7b522d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="rollingPeriodDays")
    def rolling_period_days(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "rollingPeriodDays"))

    @rolling_period_days.setter
    def rolling_period_days(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f1d7cf8ffb64e92d302872ffa3bb602019a38d4d3173b7eb995bf09c380d396)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rollingPeriodDays", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="service")
    def service(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "service"))

    @service.setter
    def service(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5eb64d97cee71c4d6baf9c5b05368e8d96e75d182d54187d7fadfe0ac3e45f3f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "service", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sloId")
    def slo_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sloId"))

    @slo_id.setter
    def slo_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8c2ba42faaa394ac9d81d59708f0c8ea406f236086dde50609b6f0783312f895)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sloId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="userLabels")
    def user_labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "userLabels"))

    @user_labels.setter
    def user_labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__36a1dfd2cbae6879b2049244c364f659516075737c129fd36b2a69945a27650d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "userLabels", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleMonitoringSlo.GoogleMonitoringSloBasicSli",
    jsii_struct_bases=[],
    name_mapping={
        "availability": "availability",
        "latency": "latency",
        "location": "location",
        "method": "method",
        "version": "version",
    },
)
class GoogleMonitoringSloBasicSli:
    def __init__(
        self,
        *,
        availability: typing.Optional[typing.Union["GoogleMonitoringSloBasicSliAvailability", typing.Dict[builtins.str, typing.Any]]] = None,
        latency: typing.Optional[typing.Union["GoogleMonitoringSloBasicSliLatency", typing.Dict[builtins.str, typing.Any]]] = None,
        location: typing.Optional[typing.Sequence[builtins.str]] = None,
        method: typing.Optional[typing.Sequence[builtins.str]] = None,
        version: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param availability: availability block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_monitoring_slo#availability GoogleMonitoringSlo#availability}
        :param latency: latency block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_monitoring_slo#latency GoogleMonitoringSlo#latency}
        :param location: An optional set of locations to which this SLI is relevant. Telemetry from other locations will not be used to calculate performance for this SLI. If omitted, this SLI applies to all locations in which the Service has activity. For service types that don't support breaking down by location, setting this field will result in an error. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_monitoring_slo#location GoogleMonitoringSlo#location}
        :param method: An optional set of RPCs to which this SLI is relevant. Telemetry from other methods will not be used to calculate performance for this SLI. If omitted, this SLI applies to all the Service's methods. For service types that don't support breaking down by method, setting this field will result in an error. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_monitoring_slo#method GoogleMonitoringSlo#method}
        :param version: The set of API versions to which this SLI is relevant. Telemetry from other API versions will not be used to calculate performance for this SLI. If omitted, this SLI applies to all API versions. For service types that don't support breaking down by version, setting this field will result in an error. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_monitoring_slo#version GoogleMonitoringSlo#version}
        '''
        if isinstance(availability, dict):
            availability = GoogleMonitoringSloBasicSliAvailability(**availability)
        if isinstance(latency, dict):
            latency = GoogleMonitoringSloBasicSliLatency(**latency)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b7f87f35c192bbcff73736b26786efddfdc94e7a14ba8b42ac313b7f75a82fb7)
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
    ) -> typing.Optional["GoogleMonitoringSloBasicSliAvailability"]:
        '''availability block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_monitoring_slo#availability GoogleMonitoringSlo#availability}
        '''
        result = self._values.get("availability")
        return typing.cast(typing.Optional["GoogleMonitoringSloBasicSliAvailability"], result)

    @builtins.property
    def latency(self) -> typing.Optional["GoogleMonitoringSloBasicSliLatency"]:
        '''latency block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_monitoring_slo#latency GoogleMonitoringSlo#latency}
        '''
        result = self._values.get("latency")
        return typing.cast(typing.Optional["GoogleMonitoringSloBasicSliLatency"], result)

    @builtins.property
    def location(self) -> typing.Optional[typing.List[builtins.str]]:
        '''An optional set of locations to which this SLI is relevant.

        Telemetry from other locations will not be used to calculate
        performance for this SLI. If omitted, this SLI applies to all
        locations in which the Service has activity. For service types
        that don't support breaking down by location, setting this
        field will result in an error.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_monitoring_slo#location GoogleMonitoringSlo#location}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_monitoring_slo#method GoogleMonitoringSlo#method}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_monitoring_slo#version GoogleMonitoringSlo#version}
        '''
        result = self._values.get("version")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleMonitoringSloBasicSli(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleMonitoringSlo.GoogleMonitoringSloBasicSliAvailability",
    jsii_struct_bases=[],
    name_mapping={"enabled": "enabled"},
)
class GoogleMonitoringSloBasicSliAvailability:
    def __init__(
        self,
        *,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param enabled: Whether an availability SLI is enabled or not. Must be set to true. Defaults to 'true'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_monitoring_slo#enabled GoogleMonitoringSlo#enabled}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__37343d1f027f9e5db974458ee9662d71fd3271d314912933f0276baf6dfa67bb)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if enabled is not None:
            self._values["enabled"] = enabled

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether an availability SLI is enabled or not. Must be set to true. Defaults to 'true'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_monitoring_slo#enabled GoogleMonitoringSlo#enabled}
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleMonitoringSloBasicSliAvailability(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleMonitoringSloBasicSliAvailabilityOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleMonitoringSlo.GoogleMonitoringSloBasicSliAvailabilityOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1b939f21fbf27015b286bcc52088b3257f134e5f1ee1049ee9b643ac61544fa5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3eb5f21a3bc398a32bbc4125e452e71da72d82d5c7ae1b3eb041aa250ef2b580)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleMonitoringSloBasicSliAvailability]:
        return typing.cast(typing.Optional[GoogleMonitoringSloBasicSliAvailability], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleMonitoringSloBasicSliAvailability],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c1c087dcb869f474f2ace6a4e6b7a25174b0e7e84382e15f3c37251c6329f1bb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleMonitoringSlo.GoogleMonitoringSloBasicSliLatency",
    jsii_struct_bases=[],
    name_mapping={"threshold": "threshold"},
)
class GoogleMonitoringSloBasicSliLatency:
    def __init__(self, *, threshold: builtins.str) -> None:
        '''
        :param threshold: A duration string, e.g. 10s. Good service is defined to be the count of requests made to this service that return in no more than threshold. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_monitoring_slo#threshold GoogleMonitoringSlo#threshold}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d3f7d913872443492a00af5b3abb2328adbd6540200757eb4503696002a0fa6f)
            check_type(argname="argument threshold", value=threshold, expected_type=type_hints["threshold"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "threshold": threshold,
        }

    @builtins.property
    def threshold(self) -> builtins.str:
        '''A duration string, e.g. 10s. Good service is defined to be the count of requests made to this service that return in no more than threshold.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_monitoring_slo#threshold GoogleMonitoringSlo#threshold}
        '''
        result = self._values.get("threshold")
        assert result is not None, "Required property 'threshold' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleMonitoringSloBasicSliLatency(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleMonitoringSloBasicSliLatencyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleMonitoringSlo.GoogleMonitoringSloBasicSliLatencyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3158d7b71a7a1312103f9844bb86957be9a43812e037c7094fae13d1c57baaed)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3571727927f3f1f9ffa66e7903d1b4fc968509f2741314bedf9729bbcc984ceb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "threshold", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GoogleMonitoringSloBasicSliLatency]:
        return typing.cast(typing.Optional[GoogleMonitoringSloBasicSliLatency], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleMonitoringSloBasicSliLatency],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6ce808649ced7d76d465afdbc9720dca0ef369ffc15c957ab6799679d93ab78a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleMonitoringSloBasicSliOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleMonitoringSlo.GoogleMonitoringSloBasicSliOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__652014590e70dc400e38430996b8b023c387ee44d51a43c51f70f6d85cf2d794)
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
        :param enabled: Whether an availability SLI is enabled or not. Must be set to true. Defaults to 'true'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_monitoring_slo#enabled GoogleMonitoringSlo#enabled}
        '''
        value = GoogleMonitoringSloBasicSliAvailability(enabled=enabled)

        return typing.cast(None, jsii.invoke(self, "putAvailability", [value]))

    @jsii.member(jsii_name="putLatency")
    def put_latency(self, *, threshold: builtins.str) -> None:
        '''
        :param threshold: A duration string, e.g. 10s. Good service is defined to be the count of requests made to this service that return in no more than threshold. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_monitoring_slo#threshold GoogleMonitoringSlo#threshold}
        '''
        value = GoogleMonitoringSloBasicSliLatency(threshold=threshold)

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
    def availability(self) -> GoogleMonitoringSloBasicSliAvailabilityOutputReference:
        return typing.cast(GoogleMonitoringSloBasicSliAvailabilityOutputReference, jsii.get(self, "availability"))

    @builtins.property
    @jsii.member(jsii_name="latency")
    def latency(self) -> GoogleMonitoringSloBasicSliLatencyOutputReference:
        return typing.cast(GoogleMonitoringSloBasicSliLatencyOutputReference, jsii.get(self, "latency"))

    @builtins.property
    @jsii.member(jsii_name="availabilityInput")
    def availability_input(
        self,
    ) -> typing.Optional[GoogleMonitoringSloBasicSliAvailability]:
        return typing.cast(typing.Optional[GoogleMonitoringSloBasicSliAvailability], jsii.get(self, "availabilityInput"))

    @builtins.property
    @jsii.member(jsii_name="latencyInput")
    def latency_input(self) -> typing.Optional[GoogleMonitoringSloBasicSliLatency]:
        return typing.cast(typing.Optional[GoogleMonitoringSloBasicSliLatency], jsii.get(self, "latencyInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__db8cab8859ab8e444c4ff4c9035012da501e25d5ea88b0b411c4297a278e1f05)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="method")
    def method(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "method"))

    @method.setter
    def method(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__44f2373c69265e6117053439a694edf30c0460b840169e29cb7a8e1deee7cade)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "method", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="version")
    def version(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "version"))

    @version.setter
    def version(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f78b6a2987c1d15b441aefdbf882f04e7d604c3591e02a75f4cb5e0af1c2841)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "version", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GoogleMonitoringSloBasicSli]:
        return typing.cast(typing.Optional[GoogleMonitoringSloBasicSli], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleMonitoringSloBasicSli],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3472e7a22322a9e8c746eef2667b55675b4a8282868d6f1b40075dc2e8da8b59)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleMonitoringSlo.GoogleMonitoringSloConfig",
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
class GoogleMonitoringSloConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        basic_sli: typing.Optional[typing.Union[GoogleMonitoringSloBasicSli, typing.Dict[builtins.str, typing.Any]]] = None,
        calendar_period: typing.Optional[builtins.str] = None,
        display_name: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        request_based_sli: typing.Optional[typing.Union["GoogleMonitoringSloRequestBasedSli", typing.Dict[builtins.str, typing.Any]]] = None,
        rolling_period_days: typing.Optional[jsii.Number] = None,
        slo_id: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["GoogleMonitoringSloTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        user_labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        windows_based_sli: typing.Optional[typing.Union["GoogleMonitoringSloWindowsBasedSli", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param goal: The fraction of service that must be good in order for this objective to be met. 0 < goal <= 0.999 Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_monitoring_slo#goal GoogleMonitoringSlo#goal}
        :param service: ID of the service to which this SLO belongs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_monitoring_slo#service GoogleMonitoringSlo#service}
        :param basic_sli: basic_sli block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_monitoring_slo#basic_sli GoogleMonitoringSlo#basic_sli}
        :param calendar_period: A calendar period, semantically "since the start of the current ". Possible values: ["DAY", "WEEK", "FORTNIGHT", "MONTH"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_monitoring_slo#calendar_period GoogleMonitoringSlo#calendar_period}
        :param display_name: Name used for UI elements listing this SLO. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_monitoring_slo#display_name GoogleMonitoringSlo#display_name}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_monitoring_slo#id GoogleMonitoringSlo#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_monitoring_slo#project GoogleMonitoringSlo#project}.
        :param request_based_sli: request_based_sli block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_monitoring_slo#request_based_sli GoogleMonitoringSlo#request_based_sli}
        :param rolling_period_days: A rolling time period, semantically "in the past X days". Must be between 1 to 30 days, inclusive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_monitoring_slo#rolling_period_days GoogleMonitoringSlo#rolling_period_days}
        :param slo_id: The id to use for this ServiceLevelObjective. If omitted, an id will be generated instead. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_monitoring_slo#slo_id GoogleMonitoringSlo#slo_id}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_monitoring_slo#timeouts GoogleMonitoringSlo#timeouts}
        :param user_labels: This field is intended to be used for organizing and identifying the AlertPolicy objects.The field can contain up to 64 entries. Each key and value is limited to 63 Unicode characters or 128 bytes, whichever is smaller. Labels and values can contain only lowercase letters, numerals, underscores, and dashes. Keys must begin with a letter. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_monitoring_slo#user_labels GoogleMonitoringSlo#user_labels}
        :param windows_based_sli: windows_based_sli block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_monitoring_slo#windows_based_sli GoogleMonitoringSlo#windows_based_sli}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(basic_sli, dict):
            basic_sli = GoogleMonitoringSloBasicSli(**basic_sli)
        if isinstance(request_based_sli, dict):
            request_based_sli = GoogleMonitoringSloRequestBasedSli(**request_based_sli)
        if isinstance(timeouts, dict):
            timeouts = GoogleMonitoringSloTimeouts(**timeouts)
        if isinstance(windows_based_sli, dict):
            windows_based_sli = GoogleMonitoringSloWindowsBasedSli(**windows_based_sli)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__58e97d5b6aae7a8e928f7dc3f5c636840f0911c00e050396ef71d5cba8d79d01)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_monitoring_slo#goal GoogleMonitoringSlo#goal}
        '''
        result = self._values.get("goal")
        assert result is not None, "Required property 'goal' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def service(self) -> builtins.str:
        '''ID of the service to which this SLO belongs.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_monitoring_slo#service GoogleMonitoringSlo#service}
        '''
        result = self._values.get("service")
        assert result is not None, "Required property 'service' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def basic_sli(self) -> typing.Optional[GoogleMonitoringSloBasicSli]:
        '''basic_sli block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_monitoring_slo#basic_sli GoogleMonitoringSlo#basic_sli}
        '''
        result = self._values.get("basic_sli")
        return typing.cast(typing.Optional[GoogleMonitoringSloBasicSli], result)

    @builtins.property
    def calendar_period(self) -> typing.Optional[builtins.str]:
        '''A calendar period, semantically "since the start of the current ". Possible values: ["DAY", "WEEK", "FORTNIGHT", "MONTH"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_monitoring_slo#calendar_period GoogleMonitoringSlo#calendar_period}
        '''
        result = self._values.get("calendar_period")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def display_name(self) -> typing.Optional[builtins.str]:
        '''Name used for UI elements listing this SLO.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_monitoring_slo#display_name GoogleMonitoringSlo#display_name}
        '''
        result = self._values.get("display_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_monitoring_slo#id GoogleMonitoringSlo#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_monitoring_slo#project GoogleMonitoringSlo#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def request_based_sli(
        self,
    ) -> typing.Optional["GoogleMonitoringSloRequestBasedSli"]:
        '''request_based_sli block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_monitoring_slo#request_based_sli GoogleMonitoringSlo#request_based_sli}
        '''
        result = self._values.get("request_based_sli")
        return typing.cast(typing.Optional["GoogleMonitoringSloRequestBasedSli"], result)

    @builtins.property
    def rolling_period_days(self) -> typing.Optional[jsii.Number]:
        '''A rolling time period, semantically "in the past X days". Must be between 1 to 30 days, inclusive.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_monitoring_slo#rolling_period_days GoogleMonitoringSlo#rolling_period_days}
        '''
        result = self._values.get("rolling_period_days")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def slo_id(self) -> typing.Optional[builtins.str]:
        '''The id to use for this ServiceLevelObjective. If omitted, an id will be generated instead.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_monitoring_slo#slo_id GoogleMonitoringSlo#slo_id}
        '''
        result = self._values.get("slo_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["GoogleMonitoringSloTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_monitoring_slo#timeouts GoogleMonitoringSlo#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["GoogleMonitoringSloTimeouts"], result)

    @builtins.property
    def user_labels(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''This field is intended to be used for organizing and identifying the AlertPolicy objects.The field can contain up to 64 entries. Each key and value is limited to 63 Unicode characters or 128 bytes, whichever is smaller. Labels and values can contain only lowercase letters, numerals, underscores, and dashes. Keys must begin with a letter.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_monitoring_slo#user_labels GoogleMonitoringSlo#user_labels}
        '''
        result = self._values.get("user_labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def windows_based_sli(
        self,
    ) -> typing.Optional["GoogleMonitoringSloWindowsBasedSli"]:
        '''windows_based_sli block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_monitoring_slo#windows_based_sli GoogleMonitoringSlo#windows_based_sli}
        '''
        result = self._values.get("windows_based_sli")
        return typing.cast(typing.Optional["GoogleMonitoringSloWindowsBasedSli"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleMonitoringSloConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleMonitoringSlo.GoogleMonitoringSloRequestBasedSli",
    jsii_struct_bases=[],
    name_mapping={
        "distribution_cut": "distributionCut",
        "good_total_ratio": "goodTotalRatio",
    },
)
class GoogleMonitoringSloRequestBasedSli:
    def __init__(
        self,
        *,
        distribution_cut: typing.Optional[typing.Union["GoogleMonitoringSloRequestBasedSliDistributionCut", typing.Dict[builtins.str, typing.Any]]] = None,
        good_total_ratio: typing.Optional[typing.Union["GoogleMonitoringSloRequestBasedSliGoodTotalRatio", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param distribution_cut: distribution_cut block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_monitoring_slo#distribution_cut GoogleMonitoringSlo#distribution_cut}
        :param good_total_ratio: good_total_ratio block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_monitoring_slo#good_total_ratio GoogleMonitoringSlo#good_total_ratio}
        '''
        if isinstance(distribution_cut, dict):
            distribution_cut = GoogleMonitoringSloRequestBasedSliDistributionCut(**distribution_cut)
        if isinstance(good_total_ratio, dict):
            good_total_ratio = GoogleMonitoringSloRequestBasedSliGoodTotalRatio(**good_total_ratio)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__11eea7e51138021445634361287ad771a0740cf387bc71301fa76f1b88708a3f)
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
    ) -> typing.Optional["GoogleMonitoringSloRequestBasedSliDistributionCut"]:
        '''distribution_cut block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_monitoring_slo#distribution_cut GoogleMonitoringSlo#distribution_cut}
        '''
        result = self._values.get("distribution_cut")
        return typing.cast(typing.Optional["GoogleMonitoringSloRequestBasedSliDistributionCut"], result)

    @builtins.property
    def good_total_ratio(
        self,
    ) -> typing.Optional["GoogleMonitoringSloRequestBasedSliGoodTotalRatio"]:
        '''good_total_ratio block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_monitoring_slo#good_total_ratio GoogleMonitoringSlo#good_total_ratio}
        '''
        result = self._values.get("good_total_ratio")
        return typing.cast(typing.Optional["GoogleMonitoringSloRequestBasedSliGoodTotalRatio"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleMonitoringSloRequestBasedSli(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleMonitoringSlo.GoogleMonitoringSloRequestBasedSliDistributionCut",
    jsii_struct_bases=[],
    name_mapping={"distribution_filter": "distributionFilter", "range": "range"},
)
class GoogleMonitoringSloRequestBasedSliDistributionCut:
    def __init__(
        self,
        *,
        distribution_filter: builtins.str,
        range: typing.Union["GoogleMonitoringSloRequestBasedSliDistributionCutRange", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param distribution_filter: A TimeSeries `monitoring filter <https://cloud.google.com/monitoring/api/v3/filters>`_ aggregating values to quantify the good service provided. Must have ValueType = DISTRIBUTION and MetricKind = DELTA or MetricKind = CUMULATIVE. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_monitoring_slo#distribution_filter GoogleMonitoringSlo#distribution_filter}
        :param range: range block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_monitoring_slo#range GoogleMonitoringSlo#range}
        '''
        if isinstance(range, dict):
            range = GoogleMonitoringSloRequestBasedSliDistributionCutRange(**range)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f5909ed8e39704d9c67c45c531f3c1c2ee3a35e42aefc1855574418416b0294d)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_monitoring_slo#distribution_filter GoogleMonitoringSlo#distribution_filter}
        '''
        result = self._values.get("distribution_filter")
        assert result is not None, "Required property 'distribution_filter' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def range(self) -> "GoogleMonitoringSloRequestBasedSliDistributionCutRange":
        '''range block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_monitoring_slo#range GoogleMonitoringSlo#range}
        '''
        result = self._values.get("range")
        assert result is not None, "Required property 'range' is missing"
        return typing.cast("GoogleMonitoringSloRequestBasedSliDistributionCutRange", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleMonitoringSloRequestBasedSliDistributionCut(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleMonitoringSloRequestBasedSliDistributionCutOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleMonitoringSlo.GoogleMonitoringSloRequestBasedSliDistributionCutOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7e2bf80c88541cd9b4c7096413d43b2b0bc173df255649e1f45c32a5cf082172)
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
        :param max: max value for the range (inclusive). If not given, will be set to 0. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_monitoring_slo#max GoogleMonitoringSlo#max}
        :param min: Min value for the range (inclusive). If not given, will be set to 0. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_monitoring_slo#min GoogleMonitoringSlo#min}
        '''
        value = GoogleMonitoringSloRequestBasedSliDistributionCutRange(
            max=max, min=min
        )

        return typing.cast(None, jsii.invoke(self, "putRange", [value]))

    @builtins.property
    @jsii.member(jsii_name="range")
    def range(
        self,
    ) -> "GoogleMonitoringSloRequestBasedSliDistributionCutRangeOutputReference":
        return typing.cast("GoogleMonitoringSloRequestBasedSliDistributionCutRangeOutputReference", jsii.get(self, "range"))

    @builtins.property
    @jsii.member(jsii_name="distributionFilterInput")
    def distribution_filter_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "distributionFilterInput"))

    @builtins.property
    @jsii.member(jsii_name="rangeInput")
    def range_input(
        self,
    ) -> typing.Optional["GoogleMonitoringSloRequestBasedSliDistributionCutRange"]:
        return typing.cast(typing.Optional["GoogleMonitoringSloRequestBasedSliDistributionCutRange"], jsii.get(self, "rangeInput"))

    @builtins.property
    @jsii.member(jsii_name="distributionFilter")
    def distribution_filter(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "distributionFilter"))

    @distribution_filter.setter
    def distribution_filter(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7817c010648dbc9f5a879be067b065b6a7c8668885aee18c354dd7e613740ae4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "distributionFilter", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleMonitoringSloRequestBasedSliDistributionCut]:
        return typing.cast(typing.Optional[GoogleMonitoringSloRequestBasedSliDistributionCut], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleMonitoringSloRequestBasedSliDistributionCut],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f05f575b9c0c758cebcb10b293e038c93c9169cbcfa5329b9ebab9793a071f9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleMonitoringSlo.GoogleMonitoringSloRequestBasedSliDistributionCutRange",
    jsii_struct_bases=[],
    name_mapping={"max": "max", "min": "min"},
)
class GoogleMonitoringSloRequestBasedSliDistributionCutRange:
    def __init__(
        self,
        *,
        max: typing.Optional[jsii.Number] = None,
        min: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param max: max value for the range (inclusive). If not given, will be set to 0. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_monitoring_slo#max GoogleMonitoringSlo#max}
        :param min: Min value for the range (inclusive). If not given, will be set to 0. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_monitoring_slo#min GoogleMonitoringSlo#min}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9367acf6f7038cf112d1acd07484491bc8206d76861a56ec4ed0c534a6ae574a)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_monitoring_slo#max GoogleMonitoringSlo#max}
        '''
        result = self._values.get("max")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def min(self) -> typing.Optional[jsii.Number]:
        '''Min value for the range (inclusive). If not given, will be set to 0.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_monitoring_slo#min GoogleMonitoringSlo#min}
        '''
        result = self._values.get("min")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleMonitoringSloRequestBasedSliDistributionCutRange(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleMonitoringSloRequestBasedSliDistributionCutRangeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleMonitoringSlo.GoogleMonitoringSloRequestBasedSliDistributionCutRangeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__15be52a92f96347ce53ab6aea442eaf3c6e163233361204454cd01c8afc831d2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8095a0b4f8b2791e9ada06483799c24e026ae49bc8ab3a3f9e5075d3d352f9ed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "max", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="min")
    def min(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "min"))

    @min.setter
    def min(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e3a65e515dbaf3ee3f71f5ad40be3385d8cc0ecb06af7bc0b185981405503db)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "min", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleMonitoringSloRequestBasedSliDistributionCutRange]:
        return typing.cast(typing.Optional[GoogleMonitoringSloRequestBasedSliDistributionCutRange], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleMonitoringSloRequestBasedSliDistributionCutRange],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b83667fd5d291c628efbc35a00aea30486c757528c1df630431c9064f0cca201)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleMonitoringSlo.GoogleMonitoringSloRequestBasedSliGoodTotalRatio",
    jsii_struct_bases=[],
    name_mapping={
        "bad_service_filter": "badServiceFilter",
        "good_service_filter": "goodServiceFilter",
        "total_service_filter": "totalServiceFilter",
    },
)
class GoogleMonitoringSloRequestBasedSliGoodTotalRatio:
    def __init__(
        self,
        *,
        bad_service_filter: typing.Optional[builtins.str] = None,
        good_service_filter: typing.Optional[builtins.str] = None,
        total_service_filter: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param bad_service_filter: A TimeSeries `monitoring filter <https://cloud.google.com/monitoring/api/v3/filters>`_ quantifying bad service provided, either demanded service that was not provided or demanded service that was of inadequate quality. Must have ValueType = DOUBLE or ValueType = INT64 and must have MetricKind = DELTA or MetricKind = CUMULATIVE. Exactly two of 'good_service_filter','bad_service_filter','total_service_filter' must be set (good + bad = total is assumed). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_monitoring_slo#bad_service_filter GoogleMonitoringSlo#bad_service_filter}
        :param good_service_filter: A TimeSeries `monitoring filter <https://cloud.google.com/monitoring/api/v3/filters>`_ quantifying good service provided. Must have ValueType = DOUBLE or ValueType = INT64 and must have MetricKind = DELTA or MetricKind = CUMULATIVE. Exactly two of 'good_service_filter','bad_service_filter','total_service_filter' must be set (good + bad = total is assumed). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_monitoring_slo#good_service_filter GoogleMonitoringSlo#good_service_filter}
        :param total_service_filter: A TimeSeries `monitoring filter <https://cloud.google.com/monitoring/api/v3/filters>`_ quantifying total demanded service. Must have ValueType = DOUBLE or ValueType = INT64 and must have MetricKind = DELTA or MetricKind = CUMULATIVE. Exactly two of 'good_service_filter','bad_service_filter','total_service_filter' must be set (good + bad = total is assumed). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_monitoring_slo#total_service_filter GoogleMonitoringSlo#total_service_filter}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__39912629b823184bf4c218b33c1a38fb01cd844f8315f20ba15d61a5712eb262)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_monitoring_slo#bad_service_filter GoogleMonitoringSlo#bad_service_filter}
        '''
        result = self._values.get("bad_service_filter")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def good_service_filter(self) -> typing.Optional[builtins.str]:
        '''A TimeSeries `monitoring filter <https://cloud.google.com/monitoring/api/v3/filters>`_ quantifying good service provided. Must have ValueType = DOUBLE or ValueType = INT64 and must have MetricKind = DELTA or MetricKind = CUMULATIVE.

        Exactly two of 'good_service_filter','bad_service_filter','total_service_filter'
        must be set (good + bad = total is assumed).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_monitoring_slo#good_service_filter GoogleMonitoringSlo#good_service_filter}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_monitoring_slo#total_service_filter GoogleMonitoringSlo#total_service_filter}
        '''
        result = self._values.get("total_service_filter")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleMonitoringSloRequestBasedSliGoodTotalRatio(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleMonitoringSloRequestBasedSliGoodTotalRatioOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleMonitoringSlo.GoogleMonitoringSloRequestBasedSliGoodTotalRatioOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e14888b16f6e88204a1a6b845ec06d6b77f55d6845e5207de779218f7ffe40ac)
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
            type_hints = typing.get_type_hints(_typecheckingstub__946fe0035824ed2fa4a58f1666ace594bd9fd2a1f63e0f14d5159162754c3d78)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "badServiceFilter", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="goodServiceFilter")
    def good_service_filter(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "goodServiceFilter"))

    @good_service_filter.setter
    def good_service_filter(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__80818c61dc266c9e8972e349c2ebf19cc5a3b60595b11be9a7663d42601f3de9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "goodServiceFilter", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="totalServiceFilter")
    def total_service_filter(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "totalServiceFilter"))

    @total_service_filter.setter
    def total_service_filter(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9006993b55ec49485a7c664008c54565fd7f82a98ec131d74dc7a7827adb7458)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "totalServiceFilter", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleMonitoringSloRequestBasedSliGoodTotalRatio]:
        return typing.cast(typing.Optional[GoogleMonitoringSloRequestBasedSliGoodTotalRatio], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleMonitoringSloRequestBasedSliGoodTotalRatio],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__00c6cfc0ce722970406d1b647d0f6fe42d8759447bbf95147ce50c3e1110944a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleMonitoringSloRequestBasedSliOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleMonitoringSlo.GoogleMonitoringSloRequestBasedSliOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__41caa54ae0b7ba802a40a7e9d5293e5ba945e5b3ce5214cf875af80a96deacba)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putDistributionCut")
    def put_distribution_cut(
        self,
        *,
        distribution_filter: builtins.str,
        range: typing.Union[GoogleMonitoringSloRequestBasedSliDistributionCutRange, typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param distribution_filter: A TimeSeries `monitoring filter <https://cloud.google.com/monitoring/api/v3/filters>`_ aggregating values to quantify the good service provided. Must have ValueType = DISTRIBUTION and MetricKind = DELTA or MetricKind = CUMULATIVE. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_monitoring_slo#distribution_filter GoogleMonitoringSlo#distribution_filter}
        :param range: range block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_monitoring_slo#range GoogleMonitoringSlo#range}
        '''
        value = GoogleMonitoringSloRequestBasedSliDistributionCut(
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
        :param bad_service_filter: A TimeSeries `monitoring filter <https://cloud.google.com/monitoring/api/v3/filters>`_ quantifying bad service provided, either demanded service that was not provided or demanded service that was of inadequate quality. Must have ValueType = DOUBLE or ValueType = INT64 and must have MetricKind = DELTA or MetricKind = CUMULATIVE. Exactly two of 'good_service_filter','bad_service_filter','total_service_filter' must be set (good + bad = total is assumed). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_monitoring_slo#bad_service_filter GoogleMonitoringSlo#bad_service_filter}
        :param good_service_filter: A TimeSeries `monitoring filter <https://cloud.google.com/monitoring/api/v3/filters>`_ quantifying good service provided. Must have ValueType = DOUBLE or ValueType = INT64 and must have MetricKind = DELTA or MetricKind = CUMULATIVE. Exactly two of 'good_service_filter','bad_service_filter','total_service_filter' must be set (good + bad = total is assumed). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_monitoring_slo#good_service_filter GoogleMonitoringSlo#good_service_filter}
        :param total_service_filter: A TimeSeries `monitoring filter <https://cloud.google.com/monitoring/api/v3/filters>`_ quantifying total demanded service. Must have ValueType = DOUBLE or ValueType = INT64 and must have MetricKind = DELTA or MetricKind = CUMULATIVE. Exactly two of 'good_service_filter','bad_service_filter','total_service_filter' must be set (good + bad = total is assumed). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_monitoring_slo#total_service_filter GoogleMonitoringSlo#total_service_filter}
        '''
        value = GoogleMonitoringSloRequestBasedSliGoodTotalRatio(
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
    ) -> GoogleMonitoringSloRequestBasedSliDistributionCutOutputReference:
        return typing.cast(GoogleMonitoringSloRequestBasedSliDistributionCutOutputReference, jsii.get(self, "distributionCut"))

    @builtins.property
    @jsii.member(jsii_name="goodTotalRatio")
    def good_total_ratio(
        self,
    ) -> GoogleMonitoringSloRequestBasedSliGoodTotalRatioOutputReference:
        return typing.cast(GoogleMonitoringSloRequestBasedSliGoodTotalRatioOutputReference, jsii.get(self, "goodTotalRatio"))

    @builtins.property
    @jsii.member(jsii_name="distributionCutInput")
    def distribution_cut_input(
        self,
    ) -> typing.Optional[GoogleMonitoringSloRequestBasedSliDistributionCut]:
        return typing.cast(typing.Optional[GoogleMonitoringSloRequestBasedSliDistributionCut], jsii.get(self, "distributionCutInput"))

    @builtins.property
    @jsii.member(jsii_name="goodTotalRatioInput")
    def good_total_ratio_input(
        self,
    ) -> typing.Optional[GoogleMonitoringSloRequestBasedSliGoodTotalRatio]:
        return typing.cast(typing.Optional[GoogleMonitoringSloRequestBasedSliGoodTotalRatio], jsii.get(self, "goodTotalRatioInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GoogleMonitoringSloRequestBasedSli]:
        return typing.cast(typing.Optional[GoogleMonitoringSloRequestBasedSli], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleMonitoringSloRequestBasedSli],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3593bdcc9034993c2c16b3e35ceffdc326eb79220576e2f04d23bb6c3fec326e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleMonitoringSlo.GoogleMonitoringSloTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class GoogleMonitoringSloTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_monitoring_slo#create GoogleMonitoringSlo#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_monitoring_slo#delete GoogleMonitoringSlo#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_monitoring_slo#update GoogleMonitoringSlo#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7510f436e42e9568d51c2dd209fb91ced383bd5a8a2413a37fea383ad2952354)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_monitoring_slo#create GoogleMonitoringSlo#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_monitoring_slo#delete GoogleMonitoringSlo#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_monitoring_slo#update GoogleMonitoringSlo#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleMonitoringSloTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleMonitoringSloTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleMonitoringSlo.GoogleMonitoringSloTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__622784d9038cc6a428ce0ec3f7cd1c184068da1aa5d27e704f95abc6765bf3af)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e00ed7a61b6f8940967c360c8642f8b64f1e8ca4a04580dea6bd8185b4241ac9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__38f74684f2832d927f636ac356455d27eb4044a3f5e5a436ddfbe0380ee956ea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f9f638327371d288f3f1868973486f837f3498e52196a70e3e01f48280d58875)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleMonitoringSloTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleMonitoringSloTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleMonitoringSloTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d1ca28a80b90ab16b89a9368459b87a3b63bfb970f42985fcaa92866358d274e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleMonitoringSlo.GoogleMonitoringSloWindowsBasedSli",
    jsii_struct_bases=[],
    name_mapping={
        "good_bad_metric_filter": "goodBadMetricFilter",
        "good_total_ratio_threshold": "goodTotalRatioThreshold",
        "metric_mean_in_range": "metricMeanInRange",
        "metric_sum_in_range": "metricSumInRange",
        "window_period": "windowPeriod",
    },
)
class GoogleMonitoringSloWindowsBasedSli:
    def __init__(
        self,
        *,
        good_bad_metric_filter: typing.Optional[builtins.str] = None,
        good_total_ratio_threshold: typing.Optional[typing.Union["GoogleMonitoringSloWindowsBasedSliGoodTotalRatioThreshold", typing.Dict[builtins.str, typing.Any]]] = None,
        metric_mean_in_range: typing.Optional[typing.Union["GoogleMonitoringSloWindowsBasedSliMetricMeanInRange", typing.Dict[builtins.str, typing.Any]]] = None,
        metric_sum_in_range: typing.Optional[typing.Union["GoogleMonitoringSloWindowsBasedSliMetricSumInRange", typing.Dict[builtins.str, typing.Any]]] = None,
        window_period: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param good_bad_metric_filter: A TimeSeries `monitoring filter <https://cloud.google.com/monitoring/api/v3/filters>`_ with ValueType = BOOL. The window is good if any true values appear in the window. One of 'good_bad_metric_filter', 'good_total_ratio_threshold', 'metric_mean_in_range', 'metric_sum_in_range' must be set for 'windows_based_sli'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_monitoring_slo#good_bad_metric_filter GoogleMonitoringSlo#good_bad_metric_filter}
        :param good_total_ratio_threshold: good_total_ratio_threshold block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_monitoring_slo#good_total_ratio_threshold GoogleMonitoringSlo#good_total_ratio_threshold}
        :param metric_mean_in_range: metric_mean_in_range block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_monitoring_slo#metric_mean_in_range GoogleMonitoringSlo#metric_mean_in_range}
        :param metric_sum_in_range: metric_sum_in_range block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_monitoring_slo#metric_sum_in_range GoogleMonitoringSlo#metric_sum_in_range}
        :param window_period: Duration over which window quality is evaluated, given as a duration string "{X}s" representing X seconds. Must be an integer fraction of a day and at least 60s. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_monitoring_slo#window_period GoogleMonitoringSlo#window_period}
        '''
        if isinstance(good_total_ratio_threshold, dict):
            good_total_ratio_threshold = GoogleMonitoringSloWindowsBasedSliGoodTotalRatioThreshold(**good_total_ratio_threshold)
        if isinstance(metric_mean_in_range, dict):
            metric_mean_in_range = GoogleMonitoringSloWindowsBasedSliMetricMeanInRange(**metric_mean_in_range)
        if isinstance(metric_sum_in_range, dict):
            metric_sum_in_range = GoogleMonitoringSloWindowsBasedSliMetricSumInRange(**metric_sum_in_range)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c83fb1f2e3c959039975e48591d358ce70f6970f985548e2d244ea51153cb0e7)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_monitoring_slo#good_bad_metric_filter GoogleMonitoringSlo#good_bad_metric_filter}
        '''
        result = self._values.get("good_bad_metric_filter")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def good_total_ratio_threshold(
        self,
    ) -> typing.Optional["GoogleMonitoringSloWindowsBasedSliGoodTotalRatioThreshold"]:
        '''good_total_ratio_threshold block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_monitoring_slo#good_total_ratio_threshold GoogleMonitoringSlo#good_total_ratio_threshold}
        '''
        result = self._values.get("good_total_ratio_threshold")
        return typing.cast(typing.Optional["GoogleMonitoringSloWindowsBasedSliGoodTotalRatioThreshold"], result)

    @builtins.property
    def metric_mean_in_range(
        self,
    ) -> typing.Optional["GoogleMonitoringSloWindowsBasedSliMetricMeanInRange"]:
        '''metric_mean_in_range block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_monitoring_slo#metric_mean_in_range GoogleMonitoringSlo#metric_mean_in_range}
        '''
        result = self._values.get("metric_mean_in_range")
        return typing.cast(typing.Optional["GoogleMonitoringSloWindowsBasedSliMetricMeanInRange"], result)

    @builtins.property
    def metric_sum_in_range(
        self,
    ) -> typing.Optional["GoogleMonitoringSloWindowsBasedSliMetricSumInRange"]:
        '''metric_sum_in_range block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_monitoring_slo#metric_sum_in_range GoogleMonitoringSlo#metric_sum_in_range}
        '''
        result = self._values.get("metric_sum_in_range")
        return typing.cast(typing.Optional["GoogleMonitoringSloWindowsBasedSliMetricSumInRange"], result)

    @builtins.property
    def window_period(self) -> typing.Optional[builtins.str]:
        '''Duration over which window quality is evaluated, given as a duration string "{X}s" representing X seconds.

        Must be an
        integer fraction of a day and at least 60s.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_monitoring_slo#window_period GoogleMonitoringSlo#window_period}
        '''
        result = self._values.get("window_period")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleMonitoringSloWindowsBasedSli(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleMonitoringSlo.GoogleMonitoringSloWindowsBasedSliGoodTotalRatioThreshold",
    jsii_struct_bases=[],
    name_mapping={
        "basic_sli_performance": "basicSliPerformance",
        "performance": "performance",
        "threshold": "threshold",
    },
)
class GoogleMonitoringSloWindowsBasedSliGoodTotalRatioThreshold:
    def __init__(
        self,
        *,
        basic_sli_performance: typing.Optional[typing.Union["GoogleMonitoringSloWindowsBasedSliGoodTotalRatioThresholdBasicSliPerformance", typing.Dict[builtins.str, typing.Any]]] = None,
        performance: typing.Optional[typing.Union["GoogleMonitoringSloWindowsBasedSliGoodTotalRatioThresholdPerformance", typing.Dict[builtins.str, typing.Any]]] = None,
        threshold: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param basic_sli_performance: basic_sli_performance block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_monitoring_slo#basic_sli_performance GoogleMonitoringSlo#basic_sli_performance}
        :param performance: performance block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_monitoring_slo#performance GoogleMonitoringSlo#performance}
        :param threshold: If window performance >= threshold, the window is counted as good. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_monitoring_slo#threshold GoogleMonitoringSlo#threshold}
        '''
        if isinstance(basic_sli_performance, dict):
            basic_sli_performance = GoogleMonitoringSloWindowsBasedSliGoodTotalRatioThresholdBasicSliPerformance(**basic_sli_performance)
        if isinstance(performance, dict):
            performance = GoogleMonitoringSloWindowsBasedSliGoodTotalRatioThresholdPerformance(**performance)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ec8bc6b6ddae4d6f759772a758d7d316eedf3cb2986f3fe700e3ae9a6f1db35c)
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
    ) -> typing.Optional["GoogleMonitoringSloWindowsBasedSliGoodTotalRatioThresholdBasicSliPerformance"]:
        '''basic_sli_performance block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_monitoring_slo#basic_sli_performance GoogleMonitoringSlo#basic_sli_performance}
        '''
        result = self._values.get("basic_sli_performance")
        return typing.cast(typing.Optional["GoogleMonitoringSloWindowsBasedSliGoodTotalRatioThresholdBasicSliPerformance"], result)

    @builtins.property
    def performance(
        self,
    ) -> typing.Optional["GoogleMonitoringSloWindowsBasedSliGoodTotalRatioThresholdPerformance"]:
        '''performance block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_monitoring_slo#performance GoogleMonitoringSlo#performance}
        '''
        result = self._values.get("performance")
        return typing.cast(typing.Optional["GoogleMonitoringSloWindowsBasedSliGoodTotalRatioThresholdPerformance"], result)

    @builtins.property
    def threshold(self) -> typing.Optional[jsii.Number]:
        '''If window performance >= threshold, the window is counted as good.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_monitoring_slo#threshold GoogleMonitoringSlo#threshold}
        '''
        result = self._values.get("threshold")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleMonitoringSloWindowsBasedSliGoodTotalRatioThreshold(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleMonitoringSlo.GoogleMonitoringSloWindowsBasedSliGoodTotalRatioThresholdBasicSliPerformance",
    jsii_struct_bases=[],
    name_mapping={
        "availability": "availability",
        "latency": "latency",
        "location": "location",
        "method": "method",
        "version": "version",
    },
)
class GoogleMonitoringSloWindowsBasedSliGoodTotalRatioThresholdBasicSliPerformance:
    def __init__(
        self,
        *,
        availability: typing.Optional[typing.Union["GoogleMonitoringSloWindowsBasedSliGoodTotalRatioThresholdBasicSliPerformanceAvailability", typing.Dict[builtins.str, typing.Any]]] = None,
        latency: typing.Optional[typing.Union["GoogleMonitoringSloWindowsBasedSliGoodTotalRatioThresholdBasicSliPerformanceLatency", typing.Dict[builtins.str, typing.Any]]] = None,
        location: typing.Optional[typing.Sequence[builtins.str]] = None,
        method: typing.Optional[typing.Sequence[builtins.str]] = None,
        version: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param availability: availability block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_monitoring_slo#availability GoogleMonitoringSlo#availability}
        :param latency: latency block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_monitoring_slo#latency GoogleMonitoringSlo#latency}
        :param location: An optional set of locations to which this SLI is relevant. Telemetry from other locations will not be used to calculate performance for this SLI. If omitted, this SLI applies to all locations in which the Service has activity. For service types that don't support breaking down by location, setting this field will result in an error. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_monitoring_slo#location GoogleMonitoringSlo#location}
        :param method: An optional set of RPCs to which this SLI is relevant. Telemetry from other methods will not be used to calculate performance for this SLI. If omitted, this SLI applies to all the Service's methods. For service types that don't support breaking down by method, setting this field will result in an error. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_monitoring_slo#method GoogleMonitoringSlo#method}
        :param version: The set of API versions to which this SLI is relevant. Telemetry from other API versions will not be used to calculate performance for this SLI. If omitted, this SLI applies to all API versions. For service types that don't support breaking down by version, setting this field will result in an error. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_monitoring_slo#version GoogleMonitoringSlo#version}
        '''
        if isinstance(availability, dict):
            availability = GoogleMonitoringSloWindowsBasedSliGoodTotalRatioThresholdBasicSliPerformanceAvailability(**availability)
        if isinstance(latency, dict):
            latency = GoogleMonitoringSloWindowsBasedSliGoodTotalRatioThresholdBasicSliPerformanceLatency(**latency)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2185c34869967e5df51026f56d2b1393a72978ccaf8bff03ff1ce0a5c99c9678)
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
    ) -> typing.Optional["GoogleMonitoringSloWindowsBasedSliGoodTotalRatioThresholdBasicSliPerformanceAvailability"]:
        '''availability block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_monitoring_slo#availability GoogleMonitoringSlo#availability}
        '''
        result = self._values.get("availability")
        return typing.cast(typing.Optional["GoogleMonitoringSloWindowsBasedSliGoodTotalRatioThresholdBasicSliPerformanceAvailability"], result)

    @builtins.property
    def latency(
        self,
    ) -> typing.Optional["GoogleMonitoringSloWindowsBasedSliGoodTotalRatioThresholdBasicSliPerformanceLatency"]:
        '''latency block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_monitoring_slo#latency GoogleMonitoringSlo#latency}
        '''
        result = self._values.get("latency")
        return typing.cast(typing.Optional["GoogleMonitoringSloWindowsBasedSliGoodTotalRatioThresholdBasicSliPerformanceLatency"], result)

    @builtins.property
    def location(self) -> typing.Optional[typing.List[builtins.str]]:
        '''An optional set of locations to which this SLI is relevant.

        Telemetry from other locations will not be used to calculate
        performance for this SLI. If omitted, this SLI applies to all
        locations in which the Service has activity. For service types
        that don't support breaking down by location, setting this
        field will result in an error.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_monitoring_slo#location GoogleMonitoringSlo#location}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_monitoring_slo#method GoogleMonitoringSlo#method}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_monitoring_slo#version GoogleMonitoringSlo#version}
        '''
        result = self._values.get("version")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleMonitoringSloWindowsBasedSliGoodTotalRatioThresholdBasicSliPerformance(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleMonitoringSlo.GoogleMonitoringSloWindowsBasedSliGoodTotalRatioThresholdBasicSliPerformanceAvailability",
    jsii_struct_bases=[],
    name_mapping={"enabled": "enabled"},
)
class GoogleMonitoringSloWindowsBasedSliGoodTotalRatioThresholdBasicSliPerformanceAvailability:
    def __init__(
        self,
        *,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param enabled: Whether an availability SLI is enabled or not. Must be set to 'true. Defaults to 'true'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_monitoring_slo#enabled GoogleMonitoringSlo#enabled}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__527653955244846709f7a104b6201ca150b260b62fb18bdd7b1263f1382dec34)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if enabled is not None:
            self._values["enabled"] = enabled

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether an availability SLI is enabled or not. Must be set to 'true. Defaults to 'true'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_monitoring_slo#enabled GoogleMonitoringSlo#enabled}
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleMonitoringSloWindowsBasedSliGoodTotalRatioThresholdBasicSliPerformanceAvailability(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleMonitoringSloWindowsBasedSliGoodTotalRatioThresholdBasicSliPerformanceAvailabilityOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleMonitoringSlo.GoogleMonitoringSloWindowsBasedSliGoodTotalRatioThresholdBasicSliPerformanceAvailabilityOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fedf9d44ff1387479089c7adff079b7ee03fec4bb2a24f1c7a637e0631fb1227)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f661c9773f3a19a25ad516708103966ab72f9b850644c296e676f4e18f4e10be)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleMonitoringSloWindowsBasedSliGoodTotalRatioThresholdBasicSliPerformanceAvailability]:
        return typing.cast(typing.Optional[GoogleMonitoringSloWindowsBasedSliGoodTotalRatioThresholdBasicSliPerformanceAvailability], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleMonitoringSloWindowsBasedSliGoodTotalRatioThresholdBasicSliPerformanceAvailability],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0d2b4572f0f71dcae3d2e4e455d8d8d353c18fec7b127b0cdec0897452a7aac1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleMonitoringSlo.GoogleMonitoringSloWindowsBasedSliGoodTotalRatioThresholdBasicSliPerformanceLatency",
    jsii_struct_bases=[],
    name_mapping={"threshold": "threshold"},
)
class GoogleMonitoringSloWindowsBasedSliGoodTotalRatioThresholdBasicSliPerformanceLatency:
    def __init__(self, *, threshold: builtins.str) -> None:
        '''
        :param threshold: A duration string, e.g. 10s. Good service is defined to be the count of requests made to this service that return in no more than threshold. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_monitoring_slo#threshold GoogleMonitoringSlo#threshold}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__96c59b57a749da14f11f45e32264e97936a4ea338266aff7e7d990ed9fe6585c)
            check_type(argname="argument threshold", value=threshold, expected_type=type_hints["threshold"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "threshold": threshold,
        }

    @builtins.property
    def threshold(self) -> builtins.str:
        '''A duration string, e.g. 10s. Good service is defined to be the count of requests made to this service that return in no more than threshold.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_monitoring_slo#threshold GoogleMonitoringSlo#threshold}
        '''
        result = self._values.get("threshold")
        assert result is not None, "Required property 'threshold' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleMonitoringSloWindowsBasedSliGoodTotalRatioThresholdBasicSliPerformanceLatency(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleMonitoringSloWindowsBasedSliGoodTotalRatioThresholdBasicSliPerformanceLatencyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleMonitoringSlo.GoogleMonitoringSloWindowsBasedSliGoodTotalRatioThresholdBasicSliPerformanceLatencyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1a026a2cb63f4a5688ecbfc575808348a2ac719727dc521e34c79e9c3137dffd)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5f2d2bf1fbeeab0c09f606be87e09195e8a6c02d3a1ff156feb1b9c65311bbbe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "threshold", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleMonitoringSloWindowsBasedSliGoodTotalRatioThresholdBasicSliPerformanceLatency]:
        return typing.cast(typing.Optional[GoogleMonitoringSloWindowsBasedSliGoodTotalRatioThresholdBasicSliPerformanceLatency], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleMonitoringSloWindowsBasedSliGoodTotalRatioThresholdBasicSliPerformanceLatency],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e69ca2a202fc7cad9d0a9c2b48ac0fc66fa4f87bb65d30704be197723f9307b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleMonitoringSloWindowsBasedSliGoodTotalRatioThresholdBasicSliPerformanceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleMonitoringSlo.GoogleMonitoringSloWindowsBasedSliGoodTotalRatioThresholdBasicSliPerformanceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__217fe7d91ac9e0dde7228b6b5ce492bc1e1fb0b03460761119ec06de2f93dfd5)
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
        :param enabled: Whether an availability SLI is enabled or not. Must be set to 'true. Defaults to 'true'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_monitoring_slo#enabled GoogleMonitoringSlo#enabled}
        '''
        value = GoogleMonitoringSloWindowsBasedSliGoodTotalRatioThresholdBasicSliPerformanceAvailability(
            enabled=enabled
        )

        return typing.cast(None, jsii.invoke(self, "putAvailability", [value]))

    @jsii.member(jsii_name="putLatency")
    def put_latency(self, *, threshold: builtins.str) -> None:
        '''
        :param threshold: A duration string, e.g. 10s. Good service is defined to be the count of requests made to this service that return in no more than threshold. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_monitoring_slo#threshold GoogleMonitoringSlo#threshold}
        '''
        value = GoogleMonitoringSloWindowsBasedSliGoodTotalRatioThresholdBasicSliPerformanceLatency(
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
    ) -> GoogleMonitoringSloWindowsBasedSliGoodTotalRatioThresholdBasicSliPerformanceAvailabilityOutputReference:
        return typing.cast(GoogleMonitoringSloWindowsBasedSliGoodTotalRatioThresholdBasicSliPerformanceAvailabilityOutputReference, jsii.get(self, "availability"))

    @builtins.property
    @jsii.member(jsii_name="latency")
    def latency(
        self,
    ) -> GoogleMonitoringSloWindowsBasedSliGoodTotalRatioThresholdBasicSliPerformanceLatencyOutputReference:
        return typing.cast(GoogleMonitoringSloWindowsBasedSliGoodTotalRatioThresholdBasicSliPerformanceLatencyOutputReference, jsii.get(self, "latency"))

    @builtins.property
    @jsii.member(jsii_name="availabilityInput")
    def availability_input(
        self,
    ) -> typing.Optional[GoogleMonitoringSloWindowsBasedSliGoodTotalRatioThresholdBasicSliPerformanceAvailability]:
        return typing.cast(typing.Optional[GoogleMonitoringSloWindowsBasedSliGoodTotalRatioThresholdBasicSliPerformanceAvailability], jsii.get(self, "availabilityInput"))

    @builtins.property
    @jsii.member(jsii_name="latencyInput")
    def latency_input(
        self,
    ) -> typing.Optional[GoogleMonitoringSloWindowsBasedSliGoodTotalRatioThresholdBasicSliPerformanceLatency]:
        return typing.cast(typing.Optional[GoogleMonitoringSloWindowsBasedSliGoodTotalRatioThresholdBasicSliPerformanceLatency], jsii.get(self, "latencyInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__0f4f3d26afb3a44ecb930b361a4c9a49a004e6deae76a75b1beabe9652dd74e5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="method")
    def method(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "method"))

    @method.setter
    def method(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cbab6cd36f01dd3d09b64d552408d9544464330dfc0d1a11e68de1b762c189df)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "method", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="version")
    def version(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "version"))

    @version.setter
    def version(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c86f089856c1247e0a53dd48303fb7942711d2d9b8d165f4d1ce6cc864797569)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "version", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleMonitoringSloWindowsBasedSliGoodTotalRatioThresholdBasicSliPerformance]:
        return typing.cast(typing.Optional[GoogleMonitoringSloWindowsBasedSliGoodTotalRatioThresholdBasicSliPerformance], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleMonitoringSloWindowsBasedSliGoodTotalRatioThresholdBasicSliPerformance],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7ca9051cb9a04ead7d19a0b2d0305f85316130a43ab932ded469bce91a5242ce)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleMonitoringSloWindowsBasedSliGoodTotalRatioThresholdOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleMonitoringSlo.GoogleMonitoringSloWindowsBasedSliGoodTotalRatioThresholdOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0df884151f9185d8f015e6fcab58b4601f8663b9c2dc66640083a26060680420)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putBasicSliPerformance")
    def put_basic_sli_performance(
        self,
        *,
        availability: typing.Optional[typing.Union[GoogleMonitoringSloWindowsBasedSliGoodTotalRatioThresholdBasicSliPerformanceAvailability, typing.Dict[builtins.str, typing.Any]]] = None,
        latency: typing.Optional[typing.Union[GoogleMonitoringSloWindowsBasedSliGoodTotalRatioThresholdBasicSliPerformanceLatency, typing.Dict[builtins.str, typing.Any]]] = None,
        location: typing.Optional[typing.Sequence[builtins.str]] = None,
        method: typing.Optional[typing.Sequence[builtins.str]] = None,
        version: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param availability: availability block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_monitoring_slo#availability GoogleMonitoringSlo#availability}
        :param latency: latency block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_monitoring_slo#latency GoogleMonitoringSlo#latency}
        :param location: An optional set of locations to which this SLI is relevant. Telemetry from other locations will not be used to calculate performance for this SLI. If omitted, this SLI applies to all locations in which the Service has activity. For service types that don't support breaking down by location, setting this field will result in an error. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_monitoring_slo#location GoogleMonitoringSlo#location}
        :param method: An optional set of RPCs to which this SLI is relevant. Telemetry from other methods will not be used to calculate performance for this SLI. If omitted, this SLI applies to all the Service's methods. For service types that don't support breaking down by method, setting this field will result in an error. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_monitoring_slo#method GoogleMonitoringSlo#method}
        :param version: The set of API versions to which this SLI is relevant. Telemetry from other API versions will not be used to calculate performance for this SLI. If omitted, this SLI applies to all API versions. For service types that don't support breaking down by version, setting this field will result in an error. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_monitoring_slo#version GoogleMonitoringSlo#version}
        '''
        value = GoogleMonitoringSloWindowsBasedSliGoodTotalRatioThresholdBasicSliPerformance(
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
        distribution_cut: typing.Optional[typing.Union["GoogleMonitoringSloWindowsBasedSliGoodTotalRatioThresholdPerformanceDistributionCut", typing.Dict[builtins.str, typing.Any]]] = None,
        good_total_ratio: typing.Optional[typing.Union["GoogleMonitoringSloWindowsBasedSliGoodTotalRatioThresholdPerformanceGoodTotalRatio", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param distribution_cut: distribution_cut block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_monitoring_slo#distribution_cut GoogleMonitoringSlo#distribution_cut}
        :param good_total_ratio: good_total_ratio block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_monitoring_slo#good_total_ratio GoogleMonitoringSlo#good_total_ratio}
        '''
        value = GoogleMonitoringSloWindowsBasedSliGoodTotalRatioThresholdPerformance(
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
    ) -> GoogleMonitoringSloWindowsBasedSliGoodTotalRatioThresholdBasicSliPerformanceOutputReference:
        return typing.cast(GoogleMonitoringSloWindowsBasedSliGoodTotalRatioThresholdBasicSliPerformanceOutputReference, jsii.get(self, "basicSliPerformance"))

    @builtins.property
    @jsii.member(jsii_name="performance")
    def performance(
        self,
    ) -> "GoogleMonitoringSloWindowsBasedSliGoodTotalRatioThresholdPerformanceOutputReference":
        return typing.cast("GoogleMonitoringSloWindowsBasedSliGoodTotalRatioThresholdPerformanceOutputReference", jsii.get(self, "performance"))

    @builtins.property
    @jsii.member(jsii_name="basicSliPerformanceInput")
    def basic_sli_performance_input(
        self,
    ) -> typing.Optional[GoogleMonitoringSloWindowsBasedSliGoodTotalRatioThresholdBasicSliPerformance]:
        return typing.cast(typing.Optional[GoogleMonitoringSloWindowsBasedSliGoodTotalRatioThresholdBasicSliPerformance], jsii.get(self, "basicSliPerformanceInput"))

    @builtins.property
    @jsii.member(jsii_name="performanceInput")
    def performance_input(
        self,
    ) -> typing.Optional["GoogleMonitoringSloWindowsBasedSliGoodTotalRatioThresholdPerformance"]:
        return typing.cast(typing.Optional["GoogleMonitoringSloWindowsBasedSliGoodTotalRatioThresholdPerformance"], jsii.get(self, "performanceInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__5209182b7906a4cfa75010fc3c644e2cbf2f972a4ae48e8d47ecd84507c34a8f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "threshold", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleMonitoringSloWindowsBasedSliGoodTotalRatioThreshold]:
        return typing.cast(typing.Optional[GoogleMonitoringSloWindowsBasedSliGoodTotalRatioThreshold], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleMonitoringSloWindowsBasedSliGoodTotalRatioThreshold],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e00ce614bc08dd26d688491ee18d26c089dc55152ac63a5ce4208b3872139e25)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleMonitoringSlo.GoogleMonitoringSloWindowsBasedSliGoodTotalRatioThresholdPerformance",
    jsii_struct_bases=[],
    name_mapping={
        "distribution_cut": "distributionCut",
        "good_total_ratio": "goodTotalRatio",
    },
)
class GoogleMonitoringSloWindowsBasedSliGoodTotalRatioThresholdPerformance:
    def __init__(
        self,
        *,
        distribution_cut: typing.Optional[typing.Union["GoogleMonitoringSloWindowsBasedSliGoodTotalRatioThresholdPerformanceDistributionCut", typing.Dict[builtins.str, typing.Any]]] = None,
        good_total_ratio: typing.Optional[typing.Union["GoogleMonitoringSloWindowsBasedSliGoodTotalRatioThresholdPerformanceGoodTotalRatio", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param distribution_cut: distribution_cut block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_monitoring_slo#distribution_cut GoogleMonitoringSlo#distribution_cut}
        :param good_total_ratio: good_total_ratio block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_monitoring_slo#good_total_ratio GoogleMonitoringSlo#good_total_ratio}
        '''
        if isinstance(distribution_cut, dict):
            distribution_cut = GoogleMonitoringSloWindowsBasedSliGoodTotalRatioThresholdPerformanceDistributionCut(**distribution_cut)
        if isinstance(good_total_ratio, dict):
            good_total_ratio = GoogleMonitoringSloWindowsBasedSliGoodTotalRatioThresholdPerformanceGoodTotalRatio(**good_total_ratio)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a131d08b4c9cb3ca45b1e7239544f6557bae753e7e474f09fdb41c3520ea891f)
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
    ) -> typing.Optional["GoogleMonitoringSloWindowsBasedSliGoodTotalRatioThresholdPerformanceDistributionCut"]:
        '''distribution_cut block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_monitoring_slo#distribution_cut GoogleMonitoringSlo#distribution_cut}
        '''
        result = self._values.get("distribution_cut")
        return typing.cast(typing.Optional["GoogleMonitoringSloWindowsBasedSliGoodTotalRatioThresholdPerformanceDistributionCut"], result)

    @builtins.property
    def good_total_ratio(
        self,
    ) -> typing.Optional["GoogleMonitoringSloWindowsBasedSliGoodTotalRatioThresholdPerformanceGoodTotalRatio"]:
        '''good_total_ratio block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_monitoring_slo#good_total_ratio GoogleMonitoringSlo#good_total_ratio}
        '''
        result = self._values.get("good_total_ratio")
        return typing.cast(typing.Optional["GoogleMonitoringSloWindowsBasedSliGoodTotalRatioThresholdPerformanceGoodTotalRatio"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleMonitoringSloWindowsBasedSliGoodTotalRatioThresholdPerformance(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleMonitoringSlo.GoogleMonitoringSloWindowsBasedSliGoodTotalRatioThresholdPerformanceDistributionCut",
    jsii_struct_bases=[],
    name_mapping={"distribution_filter": "distributionFilter", "range": "range"},
)
class GoogleMonitoringSloWindowsBasedSliGoodTotalRatioThresholdPerformanceDistributionCut:
    def __init__(
        self,
        *,
        distribution_filter: builtins.str,
        range: typing.Union["GoogleMonitoringSloWindowsBasedSliGoodTotalRatioThresholdPerformanceDistributionCutRange", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param distribution_filter: A TimeSeries `monitoring filter <https://cloud.google.com/monitoring/api/v3/filters>`_ aggregating values to quantify the good service provided. Must have ValueType = DISTRIBUTION and MetricKind = DELTA or MetricKind = CUMULATIVE. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_monitoring_slo#distribution_filter GoogleMonitoringSlo#distribution_filter}
        :param range: range block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_monitoring_slo#range GoogleMonitoringSlo#range}
        '''
        if isinstance(range, dict):
            range = GoogleMonitoringSloWindowsBasedSliGoodTotalRatioThresholdPerformanceDistributionCutRange(**range)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0e28bb87ffbc643dcbcc2d77a8b4306adeee591d12e290b7ab97539eadf43d41)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_monitoring_slo#distribution_filter GoogleMonitoringSlo#distribution_filter}
        '''
        result = self._values.get("distribution_filter")
        assert result is not None, "Required property 'distribution_filter' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def range(
        self,
    ) -> "GoogleMonitoringSloWindowsBasedSliGoodTotalRatioThresholdPerformanceDistributionCutRange":
        '''range block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_monitoring_slo#range GoogleMonitoringSlo#range}
        '''
        result = self._values.get("range")
        assert result is not None, "Required property 'range' is missing"
        return typing.cast("GoogleMonitoringSloWindowsBasedSliGoodTotalRatioThresholdPerformanceDistributionCutRange", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleMonitoringSloWindowsBasedSliGoodTotalRatioThresholdPerformanceDistributionCut(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleMonitoringSloWindowsBasedSliGoodTotalRatioThresholdPerformanceDistributionCutOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleMonitoringSlo.GoogleMonitoringSloWindowsBasedSliGoodTotalRatioThresholdPerformanceDistributionCutOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__efb491fc4e31d3c4fb6758f9c015d015d8f2528908fedd75f85f1ab129883aef)
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
        :param max: max value for the range (inclusive). If not given, will be set to 0. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_monitoring_slo#max GoogleMonitoringSlo#max}
        :param min: Min value for the range (inclusive). If not given, will be set to 0. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_monitoring_slo#min GoogleMonitoringSlo#min}
        '''
        value = GoogleMonitoringSloWindowsBasedSliGoodTotalRatioThresholdPerformanceDistributionCutRange(
            max=max, min=min
        )

        return typing.cast(None, jsii.invoke(self, "putRange", [value]))

    @builtins.property
    @jsii.member(jsii_name="range")
    def range(
        self,
    ) -> "GoogleMonitoringSloWindowsBasedSliGoodTotalRatioThresholdPerformanceDistributionCutRangeOutputReference":
        return typing.cast("GoogleMonitoringSloWindowsBasedSliGoodTotalRatioThresholdPerformanceDistributionCutRangeOutputReference", jsii.get(self, "range"))

    @builtins.property
    @jsii.member(jsii_name="distributionFilterInput")
    def distribution_filter_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "distributionFilterInput"))

    @builtins.property
    @jsii.member(jsii_name="rangeInput")
    def range_input(
        self,
    ) -> typing.Optional["GoogleMonitoringSloWindowsBasedSliGoodTotalRatioThresholdPerformanceDistributionCutRange"]:
        return typing.cast(typing.Optional["GoogleMonitoringSloWindowsBasedSliGoodTotalRatioThresholdPerformanceDistributionCutRange"], jsii.get(self, "rangeInput"))

    @builtins.property
    @jsii.member(jsii_name="distributionFilter")
    def distribution_filter(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "distributionFilter"))

    @distribution_filter.setter
    def distribution_filter(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d158cc26db0a3d39e2f25a2a163aeef9c4a2955cbbc84423cd27197bc702814f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "distributionFilter", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleMonitoringSloWindowsBasedSliGoodTotalRatioThresholdPerformanceDistributionCut]:
        return typing.cast(typing.Optional[GoogleMonitoringSloWindowsBasedSliGoodTotalRatioThresholdPerformanceDistributionCut], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleMonitoringSloWindowsBasedSliGoodTotalRatioThresholdPerformanceDistributionCut],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1004262ff59486dd66e7a6dc0fe72886403d1376a8c2d69561890b0b4c6364db)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleMonitoringSlo.GoogleMonitoringSloWindowsBasedSliGoodTotalRatioThresholdPerformanceDistributionCutRange",
    jsii_struct_bases=[],
    name_mapping={"max": "max", "min": "min"},
)
class GoogleMonitoringSloWindowsBasedSliGoodTotalRatioThresholdPerformanceDistributionCutRange:
    def __init__(
        self,
        *,
        max: typing.Optional[jsii.Number] = None,
        min: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param max: max value for the range (inclusive). If not given, will be set to 0. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_monitoring_slo#max GoogleMonitoringSlo#max}
        :param min: Min value for the range (inclusive). If not given, will be set to 0. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_monitoring_slo#min GoogleMonitoringSlo#min}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d463367d08b1f71e02ba6dfcd6ae5b419ddc1debc5c7ea9d7c87b3d94fa82971)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_monitoring_slo#max GoogleMonitoringSlo#max}
        '''
        result = self._values.get("max")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def min(self) -> typing.Optional[jsii.Number]:
        '''Min value for the range (inclusive). If not given, will be set to 0.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_monitoring_slo#min GoogleMonitoringSlo#min}
        '''
        result = self._values.get("min")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleMonitoringSloWindowsBasedSliGoodTotalRatioThresholdPerformanceDistributionCutRange(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleMonitoringSloWindowsBasedSliGoodTotalRatioThresholdPerformanceDistributionCutRangeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleMonitoringSlo.GoogleMonitoringSloWindowsBasedSliGoodTotalRatioThresholdPerformanceDistributionCutRangeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__62971dae28b49e26dc91b69204876d2ee613d566e39c2523bcb46de74c0c8d42)
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
            type_hints = typing.get_type_hints(_typecheckingstub__70b3a973a99b7261e4de7da061b62246d04b9821c584a084d89a737870e0a5c1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "max", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="min")
    def min(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "min"))

    @min.setter
    def min(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ec9ca4cf6b4e635b5db1d66b6f1fe17c4b8be5d7bd649ec77ac0571379f6a1e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "min", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleMonitoringSloWindowsBasedSliGoodTotalRatioThresholdPerformanceDistributionCutRange]:
        return typing.cast(typing.Optional[GoogleMonitoringSloWindowsBasedSliGoodTotalRatioThresholdPerformanceDistributionCutRange], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleMonitoringSloWindowsBasedSliGoodTotalRatioThresholdPerformanceDistributionCutRange],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__42dda9fad0d9f5096936a10e4f5b395922e489a5c283997c38537155f1481d99)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleMonitoringSlo.GoogleMonitoringSloWindowsBasedSliGoodTotalRatioThresholdPerformanceGoodTotalRatio",
    jsii_struct_bases=[],
    name_mapping={
        "bad_service_filter": "badServiceFilter",
        "good_service_filter": "goodServiceFilter",
        "total_service_filter": "totalServiceFilter",
    },
)
class GoogleMonitoringSloWindowsBasedSliGoodTotalRatioThresholdPerformanceGoodTotalRatio:
    def __init__(
        self,
        *,
        bad_service_filter: typing.Optional[builtins.str] = None,
        good_service_filter: typing.Optional[builtins.str] = None,
        total_service_filter: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param bad_service_filter: A TimeSeries `monitoring filter <https://cloud.google.com/monitoring/api/v3/filters>`_ quantifying bad service provided, either demanded service that was not provided or demanded service that was of inadequate quality. Exactly two of good, bad, or total service filter must be defined (where good + bad = total is assumed). Must have ValueType = DOUBLE or ValueType = INT64 and must have MetricKind = DELTA or MetricKind = CUMULATIVE. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_monitoring_slo#bad_service_filter GoogleMonitoringSlo#bad_service_filter}
        :param good_service_filter: A TimeSeries `monitoring filter <https://cloud.google.com/monitoring/api/v3/filters>`_ quantifying good service provided. Exactly two of good, bad, or total service filter must be defined (where good + bad = total is assumed). Must have ValueType = DOUBLE or ValueType = INT64 and must have MetricKind = DELTA or MetricKind = CUMULATIVE. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_monitoring_slo#good_service_filter GoogleMonitoringSlo#good_service_filter}
        :param total_service_filter: A TimeSeries `monitoring filter <https://cloud.google.com/monitoring/api/v3/filters>`_ quantifying total demanded service. Exactly two of good, bad, or total service filter must be defined (where good + bad = total is assumed). Must have ValueType = DOUBLE or ValueType = INT64 and must have MetricKind = DELTA or MetricKind = CUMULATIVE. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_monitoring_slo#total_service_filter GoogleMonitoringSlo#total_service_filter}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c406bae56ea5de3ba3a5f3bf882e34cbeb7c404f82a08ea1c35317571a0054df)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_monitoring_slo#bad_service_filter GoogleMonitoringSlo#bad_service_filter}
        '''
        result = self._values.get("bad_service_filter")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def good_service_filter(self) -> typing.Optional[builtins.str]:
        '''A TimeSeries `monitoring filter <https://cloud.google.com/monitoring/api/v3/filters>`_ quantifying good service provided. Exactly two of good, bad, or total service filter must be defined (where good + bad = total is assumed).

        Must have ValueType = DOUBLE or ValueType = INT64 and
        must have MetricKind = DELTA or MetricKind = CUMULATIVE.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_monitoring_slo#good_service_filter GoogleMonitoringSlo#good_service_filter}
        '''
        result = self._values.get("good_service_filter")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def total_service_filter(self) -> typing.Optional[builtins.str]:
        '''A TimeSeries `monitoring filter <https://cloud.google.com/monitoring/api/v3/filters>`_ quantifying total demanded service. Exactly two of good, bad, or total service filter must be defined (where good + bad = total is assumed).

        Must have ValueType = DOUBLE or ValueType = INT64 and
        must have MetricKind = DELTA or MetricKind = CUMULATIVE.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_monitoring_slo#total_service_filter GoogleMonitoringSlo#total_service_filter}
        '''
        result = self._values.get("total_service_filter")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleMonitoringSloWindowsBasedSliGoodTotalRatioThresholdPerformanceGoodTotalRatio(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleMonitoringSloWindowsBasedSliGoodTotalRatioThresholdPerformanceGoodTotalRatioOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleMonitoringSlo.GoogleMonitoringSloWindowsBasedSliGoodTotalRatioThresholdPerformanceGoodTotalRatioOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3f4db84814ad1ee17189df427cd33c7dabc1d2d826ecaca35b45af9e6f619ac2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0481ae3ed66a95a2fe860d93aa9dd129fafee0fb55d8ac6e2bc20d516bb42331)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "badServiceFilter", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="goodServiceFilter")
    def good_service_filter(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "goodServiceFilter"))

    @good_service_filter.setter
    def good_service_filter(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4d1a3662205ac4b919d016c731966ddf1c6ec7f976832bc4b8890a0ff3849bf9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "goodServiceFilter", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="totalServiceFilter")
    def total_service_filter(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "totalServiceFilter"))

    @total_service_filter.setter
    def total_service_filter(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__de13f1ade0e887807e0f2c7348cd3c52118516203706700afd7c13de68319684)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "totalServiceFilter", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleMonitoringSloWindowsBasedSliGoodTotalRatioThresholdPerformanceGoodTotalRatio]:
        return typing.cast(typing.Optional[GoogleMonitoringSloWindowsBasedSliGoodTotalRatioThresholdPerformanceGoodTotalRatio], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleMonitoringSloWindowsBasedSliGoodTotalRatioThresholdPerformanceGoodTotalRatio],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf67f4af99d0960d86ae2223d3ac7a420dbb0d17ba61f02ce024e35f08766ab5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleMonitoringSloWindowsBasedSliGoodTotalRatioThresholdPerformanceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleMonitoringSlo.GoogleMonitoringSloWindowsBasedSliGoodTotalRatioThresholdPerformanceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a4911d829d341da3f42aef6593eb704aac326a1870262ce07e7a090305f51bdf)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putDistributionCut")
    def put_distribution_cut(
        self,
        *,
        distribution_filter: builtins.str,
        range: typing.Union[GoogleMonitoringSloWindowsBasedSliGoodTotalRatioThresholdPerformanceDistributionCutRange, typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param distribution_filter: A TimeSeries `monitoring filter <https://cloud.google.com/monitoring/api/v3/filters>`_ aggregating values to quantify the good service provided. Must have ValueType = DISTRIBUTION and MetricKind = DELTA or MetricKind = CUMULATIVE. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_monitoring_slo#distribution_filter GoogleMonitoringSlo#distribution_filter}
        :param range: range block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_monitoring_slo#range GoogleMonitoringSlo#range}
        '''
        value = GoogleMonitoringSloWindowsBasedSliGoodTotalRatioThresholdPerformanceDistributionCut(
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
        :param bad_service_filter: A TimeSeries `monitoring filter <https://cloud.google.com/monitoring/api/v3/filters>`_ quantifying bad service provided, either demanded service that was not provided or demanded service that was of inadequate quality. Exactly two of good, bad, or total service filter must be defined (where good + bad = total is assumed). Must have ValueType = DOUBLE or ValueType = INT64 and must have MetricKind = DELTA or MetricKind = CUMULATIVE. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_monitoring_slo#bad_service_filter GoogleMonitoringSlo#bad_service_filter}
        :param good_service_filter: A TimeSeries `monitoring filter <https://cloud.google.com/monitoring/api/v3/filters>`_ quantifying good service provided. Exactly two of good, bad, or total service filter must be defined (where good + bad = total is assumed). Must have ValueType = DOUBLE or ValueType = INT64 and must have MetricKind = DELTA or MetricKind = CUMULATIVE. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_monitoring_slo#good_service_filter GoogleMonitoringSlo#good_service_filter}
        :param total_service_filter: A TimeSeries `monitoring filter <https://cloud.google.com/monitoring/api/v3/filters>`_ quantifying total demanded service. Exactly two of good, bad, or total service filter must be defined (where good + bad = total is assumed). Must have ValueType = DOUBLE or ValueType = INT64 and must have MetricKind = DELTA or MetricKind = CUMULATIVE. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_monitoring_slo#total_service_filter GoogleMonitoringSlo#total_service_filter}
        '''
        value = GoogleMonitoringSloWindowsBasedSliGoodTotalRatioThresholdPerformanceGoodTotalRatio(
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
    ) -> GoogleMonitoringSloWindowsBasedSliGoodTotalRatioThresholdPerformanceDistributionCutOutputReference:
        return typing.cast(GoogleMonitoringSloWindowsBasedSliGoodTotalRatioThresholdPerformanceDistributionCutOutputReference, jsii.get(self, "distributionCut"))

    @builtins.property
    @jsii.member(jsii_name="goodTotalRatio")
    def good_total_ratio(
        self,
    ) -> GoogleMonitoringSloWindowsBasedSliGoodTotalRatioThresholdPerformanceGoodTotalRatioOutputReference:
        return typing.cast(GoogleMonitoringSloWindowsBasedSliGoodTotalRatioThresholdPerformanceGoodTotalRatioOutputReference, jsii.get(self, "goodTotalRatio"))

    @builtins.property
    @jsii.member(jsii_name="distributionCutInput")
    def distribution_cut_input(
        self,
    ) -> typing.Optional[GoogleMonitoringSloWindowsBasedSliGoodTotalRatioThresholdPerformanceDistributionCut]:
        return typing.cast(typing.Optional[GoogleMonitoringSloWindowsBasedSliGoodTotalRatioThresholdPerformanceDistributionCut], jsii.get(self, "distributionCutInput"))

    @builtins.property
    @jsii.member(jsii_name="goodTotalRatioInput")
    def good_total_ratio_input(
        self,
    ) -> typing.Optional[GoogleMonitoringSloWindowsBasedSliGoodTotalRatioThresholdPerformanceGoodTotalRatio]:
        return typing.cast(typing.Optional[GoogleMonitoringSloWindowsBasedSliGoodTotalRatioThresholdPerformanceGoodTotalRatio], jsii.get(self, "goodTotalRatioInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleMonitoringSloWindowsBasedSliGoodTotalRatioThresholdPerformance]:
        return typing.cast(typing.Optional[GoogleMonitoringSloWindowsBasedSliGoodTotalRatioThresholdPerformance], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleMonitoringSloWindowsBasedSliGoodTotalRatioThresholdPerformance],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f653ea9686f74cf4f120f527859d69578b7e62063865b564ce5fbb375ccca6a9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleMonitoringSlo.GoogleMonitoringSloWindowsBasedSliMetricMeanInRange",
    jsii_struct_bases=[],
    name_mapping={"range": "range", "time_series": "timeSeries"},
)
class GoogleMonitoringSloWindowsBasedSliMetricMeanInRange:
    def __init__(
        self,
        *,
        range: typing.Union["GoogleMonitoringSloWindowsBasedSliMetricMeanInRangeRange", typing.Dict[builtins.str, typing.Any]],
        time_series: builtins.str,
    ) -> None:
        '''
        :param range: range block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_monitoring_slo#range GoogleMonitoringSlo#range}
        :param time_series: A `monitoring filter <https://cloud.google.com/monitoring/api/v3/filters>`_ specifying the TimeSeries to use for evaluating window The provided TimeSeries must have ValueType = INT64 or ValueType = DOUBLE and MetricKind = GAUGE. Mean value 'X' should satisfy 'range.min <= X <= range.max' under good service. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_monitoring_slo#time_series GoogleMonitoringSlo#time_series}
        '''
        if isinstance(range, dict):
            range = GoogleMonitoringSloWindowsBasedSliMetricMeanInRangeRange(**range)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ae8e64b9def803407892e4244faaa60a808dce63e915134c5d199c62407ed6f7)
            check_type(argname="argument range", value=range, expected_type=type_hints["range"])
            check_type(argname="argument time_series", value=time_series, expected_type=type_hints["time_series"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "range": range,
            "time_series": time_series,
        }

    @builtins.property
    def range(self) -> "GoogleMonitoringSloWindowsBasedSliMetricMeanInRangeRange":
        '''range block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_monitoring_slo#range GoogleMonitoringSlo#range}
        '''
        result = self._values.get("range")
        assert result is not None, "Required property 'range' is missing"
        return typing.cast("GoogleMonitoringSloWindowsBasedSliMetricMeanInRangeRange", result)

    @builtins.property
    def time_series(self) -> builtins.str:
        '''A `monitoring filter <https://cloud.google.com/monitoring/api/v3/filters>`_ specifying the TimeSeries to use for evaluating window The provided TimeSeries must have ValueType = INT64 or ValueType = DOUBLE and MetricKind = GAUGE. Mean value 'X' should satisfy 'range.min <= X <= range.max' under good service.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_monitoring_slo#time_series GoogleMonitoringSlo#time_series}
        '''
        result = self._values.get("time_series")
        assert result is not None, "Required property 'time_series' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleMonitoringSloWindowsBasedSliMetricMeanInRange(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleMonitoringSloWindowsBasedSliMetricMeanInRangeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleMonitoringSlo.GoogleMonitoringSloWindowsBasedSliMetricMeanInRangeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__03f9f2aa278b02b383b0741b9974438d48a3fac131ebce548b9b32a26079e9ab)
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
        :param max: max value for the range (inclusive). If not given, will be set to "infinity", defining an open range ">= range.min". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_monitoring_slo#max GoogleMonitoringSlo#max}
        :param min: Min value for the range (inclusive). If not given, will be set to "-infinity", defining an open range "< range.max". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_monitoring_slo#min GoogleMonitoringSlo#min}
        '''
        value = GoogleMonitoringSloWindowsBasedSliMetricMeanInRangeRange(
            max=max, min=min
        )

        return typing.cast(None, jsii.invoke(self, "putRange", [value]))

    @builtins.property
    @jsii.member(jsii_name="range")
    def range(
        self,
    ) -> "GoogleMonitoringSloWindowsBasedSliMetricMeanInRangeRangeOutputReference":
        return typing.cast("GoogleMonitoringSloWindowsBasedSliMetricMeanInRangeRangeOutputReference", jsii.get(self, "range"))

    @builtins.property
    @jsii.member(jsii_name="rangeInput")
    def range_input(
        self,
    ) -> typing.Optional["GoogleMonitoringSloWindowsBasedSliMetricMeanInRangeRange"]:
        return typing.cast(typing.Optional["GoogleMonitoringSloWindowsBasedSliMetricMeanInRangeRange"], jsii.get(self, "rangeInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__14d55db43dc5e2f18627d4a714d116036be14be7c2ebeb080117e6da7706d0a0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timeSeries", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleMonitoringSloWindowsBasedSliMetricMeanInRange]:
        return typing.cast(typing.Optional[GoogleMonitoringSloWindowsBasedSliMetricMeanInRange], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleMonitoringSloWindowsBasedSliMetricMeanInRange],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__64f9e52103ff563dad322f509f91ad14e1b67361b0420ffd2cc21ebc07464f6b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleMonitoringSlo.GoogleMonitoringSloWindowsBasedSliMetricMeanInRangeRange",
    jsii_struct_bases=[],
    name_mapping={"max": "max", "min": "min"},
)
class GoogleMonitoringSloWindowsBasedSliMetricMeanInRangeRange:
    def __init__(
        self,
        *,
        max: typing.Optional[jsii.Number] = None,
        min: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param max: max value for the range (inclusive). If not given, will be set to "infinity", defining an open range ">= range.min". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_monitoring_slo#max GoogleMonitoringSlo#max}
        :param min: Min value for the range (inclusive). If not given, will be set to "-infinity", defining an open range "< range.max". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_monitoring_slo#min GoogleMonitoringSlo#min}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b1fac05055ef61f7daacf12d524de10cb41179b26a65c122f792f870447a81a)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_monitoring_slo#max GoogleMonitoringSlo#max}
        '''
        result = self._values.get("max")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def min(self) -> typing.Optional[jsii.Number]:
        '''Min value for the range (inclusive). If not given, will be set to "-infinity", defining an open range "< range.max".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_monitoring_slo#min GoogleMonitoringSlo#min}
        '''
        result = self._values.get("min")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleMonitoringSloWindowsBasedSliMetricMeanInRangeRange(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleMonitoringSloWindowsBasedSliMetricMeanInRangeRangeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleMonitoringSlo.GoogleMonitoringSloWindowsBasedSliMetricMeanInRangeRangeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fa2c6eb1367197c5f4f8973fcc8a49e910a9f18fb3e0536b30cd7b0bf4b04147)
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
            type_hints = typing.get_type_hints(_typecheckingstub__cba0fdbf0e39c35156fdc6859907939f6e94fad42204e82a468284599bb0522d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "max", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="min")
    def min(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "min"))

    @min.setter
    def min(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d880ee8652b50076ba116d02a3b8034bb8be065d6180df7e8fd475703e72045d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "min", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleMonitoringSloWindowsBasedSliMetricMeanInRangeRange]:
        return typing.cast(typing.Optional[GoogleMonitoringSloWindowsBasedSliMetricMeanInRangeRange], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleMonitoringSloWindowsBasedSliMetricMeanInRangeRange],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ae52d43fb42c37b6907ec8b53d86d2bd52e6236254c579024d1850ff50e20c79)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleMonitoringSlo.GoogleMonitoringSloWindowsBasedSliMetricSumInRange",
    jsii_struct_bases=[],
    name_mapping={"range": "range", "time_series": "timeSeries"},
)
class GoogleMonitoringSloWindowsBasedSliMetricSumInRange:
    def __init__(
        self,
        *,
        range: typing.Union["GoogleMonitoringSloWindowsBasedSliMetricSumInRangeRange", typing.Dict[builtins.str, typing.Any]],
        time_series: builtins.str,
    ) -> None:
        '''
        :param range: range block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_monitoring_slo#range GoogleMonitoringSlo#range}
        :param time_series: A `monitoring filter <https://cloud.google.com/monitoring/api/v3/filters>`_ specifying the TimeSeries to use for evaluating window quality. The provided TimeSeries must have ValueType = INT64 or ValueType = DOUBLE and MetricKind = GAUGE. Summed value 'X' should satisfy 'range.min <= X <= range.max' for a good window. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_monitoring_slo#time_series GoogleMonitoringSlo#time_series}
        '''
        if isinstance(range, dict):
            range = GoogleMonitoringSloWindowsBasedSliMetricSumInRangeRange(**range)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e7ecadadbe333ecf896ad956315ee1ce68ded53f3514ff5e5ec029813027d7e)
            check_type(argname="argument range", value=range, expected_type=type_hints["range"])
            check_type(argname="argument time_series", value=time_series, expected_type=type_hints["time_series"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "range": range,
            "time_series": time_series,
        }

    @builtins.property
    def range(self) -> "GoogleMonitoringSloWindowsBasedSliMetricSumInRangeRange":
        '''range block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_monitoring_slo#range GoogleMonitoringSlo#range}
        '''
        result = self._values.get("range")
        assert result is not None, "Required property 'range' is missing"
        return typing.cast("GoogleMonitoringSloWindowsBasedSliMetricSumInRangeRange", result)

    @builtins.property
    def time_series(self) -> builtins.str:
        '''A `monitoring filter <https://cloud.google.com/monitoring/api/v3/filters>`_ specifying the TimeSeries to use for evaluating window quality. The provided TimeSeries must have ValueType = INT64 or ValueType = DOUBLE and MetricKind = GAUGE.

        Summed value 'X' should satisfy
        'range.min <= X <= range.max' for a good window.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_monitoring_slo#time_series GoogleMonitoringSlo#time_series}
        '''
        result = self._values.get("time_series")
        assert result is not None, "Required property 'time_series' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleMonitoringSloWindowsBasedSliMetricSumInRange(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleMonitoringSloWindowsBasedSliMetricSumInRangeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleMonitoringSlo.GoogleMonitoringSloWindowsBasedSliMetricSumInRangeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c914894775721c16635f94fe37cd4520e6f31e092a1a3a5723ebee693e5e532b)
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
        :param max: max value for the range (inclusive). If not given, will be set to "infinity", defining an open range ">= range.min". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_monitoring_slo#max GoogleMonitoringSlo#max}
        :param min: Min value for the range (inclusive). If not given, will be set to "-infinity", defining an open range "< range.max". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_monitoring_slo#min GoogleMonitoringSlo#min}
        '''
        value = GoogleMonitoringSloWindowsBasedSliMetricSumInRangeRange(
            max=max, min=min
        )

        return typing.cast(None, jsii.invoke(self, "putRange", [value]))

    @builtins.property
    @jsii.member(jsii_name="range")
    def range(
        self,
    ) -> "GoogleMonitoringSloWindowsBasedSliMetricSumInRangeRangeOutputReference":
        return typing.cast("GoogleMonitoringSloWindowsBasedSliMetricSumInRangeRangeOutputReference", jsii.get(self, "range"))

    @builtins.property
    @jsii.member(jsii_name="rangeInput")
    def range_input(
        self,
    ) -> typing.Optional["GoogleMonitoringSloWindowsBasedSliMetricSumInRangeRange"]:
        return typing.cast(typing.Optional["GoogleMonitoringSloWindowsBasedSliMetricSumInRangeRange"], jsii.get(self, "rangeInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__b18e8efd4419b11a3745826c2e3828e3447522958136bd16eb0057d275d262fa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timeSeries", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleMonitoringSloWindowsBasedSliMetricSumInRange]:
        return typing.cast(typing.Optional[GoogleMonitoringSloWindowsBasedSliMetricSumInRange], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleMonitoringSloWindowsBasedSliMetricSumInRange],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ea245dddd961c8076d1bf76bd76ef1848fd2cbd17d96e31442ce151f58da6583)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleMonitoringSlo.GoogleMonitoringSloWindowsBasedSliMetricSumInRangeRange",
    jsii_struct_bases=[],
    name_mapping={"max": "max", "min": "min"},
)
class GoogleMonitoringSloWindowsBasedSliMetricSumInRangeRange:
    def __init__(
        self,
        *,
        max: typing.Optional[jsii.Number] = None,
        min: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param max: max value for the range (inclusive). If not given, will be set to "infinity", defining an open range ">= range.min". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_monitoring_slo#max GoogleMonitoringSlo#max}
        :param min: Min value for the range (inclusive). If not given, will be set to "-infinity", defining an open range "< range.max". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_monitoring_slo#min GoogleMonitoringSlo#min}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__91b00091ff969bee08d7427a6be32276f168d038a45d2c39a13e18016cf4d009)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_monitoring_slo#max GoogleMonitoringSlo#max}
        '''
        result = self._values.get("max")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def min(self) -> typing.Optional[jsii.Number]:
        '''Min value for the range (inclusive). If not given, will be set to "-infinity", defining an open range "< range.max".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_monitoring_slo#min GoogleMonitoringSlo#min}
        '''
        result = self._values.get("min")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleMonitoringSloWindowsBasedSliMetricSumInRangeRange(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleMonitoringSloWindowsBasedSliMetricSumInRangeRangeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleMonitoringSlo.GoogleMonitoringSloWindowsBasedSliMetricSumInRangeRangeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__55fd835ffc4d2c3d94e849452c754852c2e26a63ee125359277311dc81d9a094)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e31899706362ce1be993fd6cf5c9f14492d51d0a562faa0eacba060b083b7f2e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "max", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="min")
    def min(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "min"))

    @min.setter
    def min(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ccb0c9ac3acdc5f3cfd5a8da00a936f0f6ca16d2891db9c6226e728c8c6a8411)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "min", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleMonitoringSloWindowsBasedSliMetricSumInRangeRange]:
        return typing.cast(typing.Optional[GoogleMonitoringSloWindowsBasedSliMetricSumInRangeRange], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleMonitoringSloWindowsBasedSliMetricSumInRangeRange],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__88fff5eb9f7e751c894392a2767c2656d1d38bb2195ed36894f37481da263f6b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleMonitoringSloWindowsBasedSliOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleMonitoringSlo.GoogleMonitoringSloWindowsBasedSliOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a1300f4a56ee225e74655c3f0315f607790bac1017b65a56e4dab6a64c4ac633)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putGoodTotalRatioThreshold")
    def put_good_total_ratio_threshold(
        self,
        *,
        basic_sli_performance: typing.Optional[typing.Union[GoogleMonitoringSloWindowsBasedSliGoodTotalRatioThresholdBasicSliPerformance, typing.Dict[builtins.str, typing.Any]]] = None,
        performance: typing.Optional[typing.Union[GoogleMonitoringSloWindowsBasedSliGoodTotalRatioThresholdPerformance, typing.Dict[builtins.str, typing.Any]]] = None,
        threshold: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param basic_sli_performance: basic_sli_performance block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_monitoring_slo#basic_sli_performance GoogleMonitoringSlo#basic_sli_performance}
        :param performance: performance block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_monitoring_slo#performance GoogleMonitoringSlo#performance}
        :param threshold: If window performance >= threshold, the window is counted as good. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_monitoring_slo#threshold GoogleMonitoringSlo#threshold}
        '''
        value = GoogleMonitoringSloWindowsBasedSliGoodTotalRatioThreshold(
            basic_sli_performance=basic_sli_performance,
            performance=performance,
            threshold=threshold,
        )

        return typing.cast(None, jsii.invoke(self, "putGoodTotalRatioThreshold", [value]))

    @jsii.member(jsii_name="putMetricMeanInRange")
    def put_metric_mean_in_range(
        self,
        *,
        range: typing.Union[GoogleMonitoringSloWindowsBasedSliMetricMeanInRangeRange, typing.Dict[builtins.str, typing.Any]],
        time_series: builtins.str,
    ) -> None:
        '''
        :param range: range block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_monitoring_slo#range GoogleMonitoringSlo#range}
        :param time_series: A `monitoring filter <https://cloud.google.com/monitoring/api/v3/filters>`_ specifying the TimeSeries to use for evaluating window The provided TimeSeries must have ValueType = INT64 or ValueType = DOUBLE and MetricKind = GAUGE. Mean value 'X' should satisfy 'range.min <= X <= range.max' under good service. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_monitoring_slo#time_series GoogleMonitoringSlo#time_series}
        '''
        value = GoogleMonitoringSloWindowsBasedSliMetricMeanInRange(
            range=range, time_series=time_series
        )

        return typing.cast(None, jsii.invoke(self, "putMetricMeanInRange", [value]))

    @jsii.member(jsii_name="putMetricSumInRange")
    def put_metric_sum_in_range(
        self,
        *,
        range: typing.Union[GoogleMonitoringSloWindowsBasedSliMetricSumInRangeRange, typing.Dict[builtins.str, typing.Any]],
        time_series: builtins.str,
    ) -> None:
        '''
        :param range: range block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_monitoring_slo#range GoogleMonitoringSlo#range}
        :param time_series: A `monitoring filter <https://cloud.google.com/monitoring/api/v3/filters>`_ specifying the TimeSeries to use for evaluating window quality. The provided TimeSeries must have ValueType = INT64 or ValueType = DOUBLE and MetricKind = GAUGE. Summed value 'X' should satisfy 'range.min <= X <= range.max' for a good window. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_monitoring_slo#time_series GoogleMonitoringSlo#time_series}
        '''
        value = GoogleMonitoringSloWindowsBasedSliMetricSumInRange(
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
    ) -> GoogleMonitoringSloWindowsBasedSliGoodTotalRatioThresholdOutputReference:
        return typing.cast(GoogleMonitoringSloWindowsBasedSliGoodTotalRatioThresholdOutputReference, jsii.get(self, "goodTotalRatioThreshold"))

    @builtins.property
    @jsii.member(jsii_name="metricMeanInRange")
    def metric_mean_in_range(
        self,
    ) -> GoogleMonitoringSloWindowsBasedSliMetricMeanInRangeOutputReference:
        return typing.cast(GoogleMonitoringSloWindowsBasedSliMetricMeanInRangeOutputReference, jsii.get(self, "metricMeanInRange"))

    @builtins.property
    @jsii.member(jsii_name="metricSumInRange")
    def metric_sum_in_range(
        self,
    ) -> GoogleMonitoringSloWindowsBasedSliMetricSumInRangeOutputReference:
        return typing.cast(GoogleMonitoringSloWindowsBasedSliMetricSumInRangeOutputReference, jsii.get(self, "metricSumInRange"))

    @builtins.property
    @jsii.member(jsii_name="goodBadMetricFilterInput")
    def good_bad_metric_filter_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "goodBadMetricFilterInput"))

    @builtins.property
    @jsii.member(jsii_name="goodTotalRatioThresholdInput")
    def good_total_ratio_threshold_input(
        self,
    ) -> typing.Optional[GoogleMonitoringSloWindowsBasedSliGoodTotalRatioThreshold]:
        return typing.cast(typing.Optional[GoogleMonitoringSloWindowsBasedSliGoodTotalRatioThreshold], jsii.get(self, "goodTotalRatioThresholdInput"))

    @builtins.property
    @jsii.member(jsii_name="metricMeanInRangeInput")
    def metric_mean_in_range_input(
        self,
    ) -> typing.Optional[GoogleMonitoringSloWindowsBasedSliMetricMeanInRange]:
        return typing.cast(typing.Optional[GoogleMonitoringSloWindowsBasedSliMetricMeanInRange], jsii.get(self, "metricMeanInRangeInput"))

    @builtins.property
    @jsii.member(jsii_name="metricSumInRangeInput")
    def metric_sum_in_range_input(
        self,
    ) -> typing.Optional[GoogleMonitoringSloWindowsBasedSliMetricSumInRange]:
        return typing.cast(typing.Optional[GoogleMonitoringSloWindowsBasedSliMetricSumInRange], jsii.get(self, "metricSumInRangeInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__f52af4d01172f03d269d49b9ddf9b0351711b6eac3f7de68933afe83de6e61d3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "goodBadMetricFilter", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="windowPeriod")
    def window_period(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "windowPeriod"))

    @window_period.setter
    def window_period(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c0c5d9759c124d7393b4416b677068b1cf7b2ba76cbe259c3ec4b356dd19d384)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "windowPeriod", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GoogleMonitoringSloWindowsBasedSli]:
        return typing.cast(typing.Optional[GoogleMonitoringSloWindowsBasedSli], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleMonitoringSloWindowsBasedSli],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d8564f59f273aecb50af9c0d70ec833a3bd42e4130e374cbcc2b07df03a240d5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "GoogleMonitoringSlo",
    "GoogleMonitoringSloBasicSli",
    "GoogleMonitoringSloBasicSliAvailability",
    "GoogleMonitoringSloBasicSliAvailabilityOutputReference",
    "GoogleMonitoringSloBasicSliLatency",
    "GoogleMonitoringSloBasicSliLatencyOutputReference",
    "GoogleMonitoringSloBasicSliOutputReference",
    "GoogleMonitoringSloConfig",
    "GoogleMonitoringSloRequestBasedSli",
    "GoogleMonitoringSloRequestBasedSliDistributionCut",
    "GoogleMonitoringSloRequestBasedSliDistributionCutOutputReference",
    "GoogleMonitoringSloRequestBasedSliDistributionCutRange",
    "GoogleMonitoringSloRequestBasedSliDistributionCutRangeOutputReference",
    "GoogleMonitoringSloRequestBasedSliGoodTotalRatio",
    "GoogleMonitoringSloRequestBasedSliGoodTotalRatioOutputReference",
    "GoogleMonitoringSloRequestBasedSliOutputReference",
    "GoogleMonitoringSloTimeouts",
    "GoogleMonitoringSloTimeoutsOutputReference",
    "GoogleMonitoringSloWindowsBasedSli",
    "GoogleMonitoringSloWindowsBasedSliGoodTotalRatioThreshold",
    "GoogleMonitoringSloWindowsBasedSliGoodTotalRatioThresholdBasicSliPerformance",
    "GoogleMonitoringSloWindowsBasedSliGoodTotalRatioThresholdBasicSliPerformanceAvailability",
    "GoogleMonitoringSloWindowsBasedSliGoodTotalRatioThresholdBasicSliPerformanceAvailabilityOutputReference",
    "GoogleMonitoringSloWindowsBasedSliGoodTotalRatioThresholdBasicSliPerformanceLatency",
    "GoogleMonitoringSloWindowsBasedSliGoodTotalRatioThresholdBasicSliPerformanceLatencyOutputReference",
    "GoogleMonitoringSloWindowsBasedSliGoodTotalRatioThresholdBasicSliPerformanceOutputReference",
    "GoogleMonitoringSloWindowsBasedSliGoodTotalRatioThresholdOutputReference",
    "GoogleMonitoringSloWindowsBasedSliGoodTotalRatioThresholdPerformance",
    "GoogleMonitoringSloWindowsBasedSliGoodTotalRatioThresholdPerformanceDistributionCut",
    "GoogleMonitoringSloWindowsBasedSliGoodTotalRatioThresholdPerformanceDistributionCutOutputReference",
    "GoogleMonitoringSloWindowsBasedSliGoodTotalRatioThresholdPerformanceDistributionCutRange",
    "GoogleMonitoringSloWindowsBasedSliGoodTotalRatioThresholdPerformanceDistributionCutRangeOutputReference",
    "GoogleMonitoringSloWindowsBasedSliGoodTotalRatioThresholdPerformanceGoodTotalRatio",
    "GoogleMonitoringSloWindowsBasedSliGoodTotalRatioThresholdPerformanceGoodTotalRatioOutputReference",
    "GoogleMonitoringSloWindowsBasedSliGoodTotalRatioThresholdPerformanceOutputReference",
    "GoogleMonitoringSloWindowsBasedSliMetricMeanInRange",
    "GoogleMonitoringSloWindowsBasedSliMetricMeanInRangeOutputReference",
    "GoogleMonitoringSloWindowsBasedSliMetricMeanInRangeRange",
    "GoogleMonitoringSloWindowsBasedSliMetricMeanInRangeRangeOutputReference",
    "GoogleMonitoringSloWindowsBasedSliMetricSumInRange",
    "GoogleMonitoringSloWindowsBasedSliMetricSumInRangeOutputReference",
    "GoogleMonitoringSloWindowsBasedSliMetricSumInRangeRange",
    "GoogleMonitoringSloWindowsBasedSliMetricSumInRangeRangeOutputReference",
    "GoogleMonitoringSloWindowsBasedSliOutputReference",
]

publication.publish()

def _typecheckingstub__6f8e48c39632cd11ed5c735a8e97888def468302d75498f6ca6dfd8c54bb9844(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    goal: jsii.Number,
    service: builtins.str,
    basic_sli: typing.Optional[typing.Union[GoogleMonitoringSloBasicSli, typing.Dict[builtins.str, typing.Any]]] = None,
    calendar_period: typing.Optional[builtins.str] = None,
    display_name: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    request_based_sli: typing.Optional[typing.Union[GoogleMonitoringSloRequestBasedSli, typing.Dict[builtins.str, typing.Any]]] = None,
    rolling_period_days: typing.Optional[jsii.Number] = None,
    slo_id: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[GoogleMonitoringSloTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    user_labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    windows_based_sli: typing.Optional[typing.Union[GoogleMonitoringSloWindowsBasedSli, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__f6e0c11c3bf4a330cdf40e099525f3f23f2c4a0461aa4a0c835f983c612b7920(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ebf5d267625730c1e1ba533eae10dfcaeeb3fc25292a2be5133b83a118179f5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9606d9c0c9411927a0eff528703da27f8bb182e048df1fff2c28fd5c2685af2b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c171ad308da7188439adcb7f9351802422a696341abfbd76b6d76126b57730b(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e500661d821e8d8289ffa45f8a9286fea606dee830fdece77a20266af196028f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9434368644b308fbb513695227d65d1e501aa90c83640b5e2828be738f7b522d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f1d7cf8ffb64e92d302872ffa3bb602019a38d4d3173b7eb995bf09c380d396(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5eb64d97cee71c4d6baf9c5b05368e8d96e75d182d54187d7fadfe0ac3e45f3f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c2ba42faaa394ac9d81d59708f0c8ea406f236086dde50609b6f0783312f895(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36a1dfd2cbae6879b2049244c364f659516075737c129fd36b2a69945a27650d(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b7f87f35c192bbcff73736b26786efddfdc94e7a14ba8b42ac313b7f75a82fb7(
    *,
    availability: typing.Optional[typing.Union[GoogleMonitoringSloBasicSliAvailability, typing.Dict[builtins.str, typing.Any]]] = None,
    latency: typing.Optional[typing.Union[GoogleMonitoringSloBasicSliLatency, typing.Dict[builtins.str, typing.Any]]] = None,
    location: typing.Optional[typing.Sequence[builtins.str]] = None,
    method: typing.Optional[typing.Sequence[builtins.str]] = None,
    version: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37343d1f027f9e5db974458ee9662d71fd3271d314912933f0276baf6dfa67bb(
    *,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b939f21fbf27015b286bcc52088b3257f134e5f1ee1049ee9b643ac61544fa5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3eb5f21a3bc398a32bbc4125e452e71da72d82d5c7ae1b3eb041aa250ef2b580(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1c087dcb869f474f2ace6a4e6b7a25174b0e7e84382e15f3c37251c6329f1bb(
    value: typing.Optional[GoogleMonitoringSloBasicSliAvailability],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3f7d913872443492a00af5b3abb2328adbd6540200757eb4503696002a0fa6f(
    *,
    threshold: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3158d7b71a7a1312103f9844bb86957be9a43812e037c7094fae13d1c57baaed(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3571727927f3f1f9ffa66e7903d1b4fc968509f2741314bedf9729bbcc984ceb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ce808649ced7d76d465afdbc9720dca0ef369ffc15c957ab6799679d93ab78a(
    value: typing.Optional[GoogleMonitoringSloBasicSliLatency],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__652014590e70dc400e38430996b8b023c387ee44d51a43c51f70f6d85cf2d794(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db8cab8859ab8e444c4ff4c9035012da501e25d5ea88b0b411c4297a278e1f05(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44f2373c69265e6117053439a694edf30c0460b840169e29cb7a8e1deee7cade(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f78b6a2987c1d15b441aefdbf882f04e7d604c3591e02a75f4cb5e0af1c2841(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3472e7a22322a9e8c746eef2667b55675b4a8282868d6f1b40075dc2e8da8b59(
    value: typing.Optional[GoogleMonitoringSloBasicSli],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__58e97d5b6aae7a8e928f7dc3f5c636840f0911c00e050396ef71d5cba8d79d01(
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
    basic_sli: typing.Optional[typing.Union[GoogleMonitoringSloBasicSli, typing.Dict[builtins.str, typing.Any]]] = None,
    calendar_period: typing.Optional[builtins.str] = None,
    display_name: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    request_based_sli: typing.Optional[typing.Union[GoogleMonitoringSloRequestBasedSli, typing.Dict[builtins.str, typing.Any]]] = None,
    rolling_period_days: typing.Optional[jsii.Number] = None,
    slo_id: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[GoogleMonitoringSloTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    user_labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    windows_based_sli: typing.Optional[typing.Union[GoogleMonitoringSloWindowsBasedSli, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11eea7e51138021445634361287ad771a0740cf387bc71301fa76f1b88708a3f(
    *,
    distribution_cut: typing.Optional[typing.Union[GoogleMonitoringSloRequestBasedSliDistributionCut, typing.Dict[builtins.str, typing.Any]]] = None,
    good_total_ratio: typing.Optional[typing.Union[GoogleMonitoringSloRequestBasedSliGoodTotalRatio, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5909ed8e39704d9c67c45c531f3c1c2ee3a35e42aefc1855574418416b0294d(
    *,
    distribution_filter: builtins.str,
    range: typing.Union[GoogleMonitoringSloRequestBasedSliDistributionCutRange, typing.Dict[builtins.str, typing.Any]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e2bf80c88541cd9b4c7096413d43b2b0bc173df255649e1f45c32a5cf082172(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7817c010648dbc9f5a879be067b065b6a7c8668885aee18c354dd7e613740ae4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f05f575b9c0c758cebcb10b293e038c93c9169cbcfa5329b9ebab9793a071f9(
    value: typing.Optional[GoogleMonitoringSloRequestBasedSliDistributionCut],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9367acf6f7038cf112d1acd07484491bc8206d76861a56ec4ed0c534a6ae574a(
    *,
    max: typing.Optional[jsii.Number] = None,
    min: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15be52a92f96347ce53ab6aea442eaf3c6e163233361204454cd01c8afc831d2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8095a0b4f8b2791e9ada06483799c24e026ae49bc8ab3a3f9e5075d3d352f9ed(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e3a65e515dbaf3ee3f71f5ad40be3385d8cc0ecb06af7bc0b185981405503db(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b83667fd5d291c628efbc35a00aea30486c757528c1df630431c9064f0cca201(
    value: typing.Optional[GoogleMonitoringSloRequestBasedSliDistributionCutRange],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39912629b823184bf4c218b33c1a38fb01cd844f8315f20ba15d61a5712eb262(
    *,
    bad_service_filter: typing.Optional[builtins.str] = None,
    good_service_filter: typing.Optional[builtins.str] = None,
    total_service_filter: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e14888b16f6e88204a1a6b845ec06d6b77f55d6845e5207de779218f7ffe40ac(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__946fe0035824ed2fa4a58f1666ace594bd9fd2a1f63e0f14d5159162754c3d78(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80818c61dc266c9e8972e349c2ebf19cc5a3b60595b11be9a7663d42601f3de9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9006993b55ec49485a7c664008c54565fd7f82a98ec131d74dc7a7827adb7458(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00c6cfc0ce722970406d1b647d0f6fe42d8759447bbf95147ce50c3e1110944a(
    value: typing.Optional[GoogleMonitoringSloRequestBasedSliGoodTotalRatio],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41caa54ae0b7ba802a40a7e9d5293e5ba945e5b3ce5214cf875af80a96deacba(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3593bdcc9034993c2c16b3e35ceffdc326eb79220576e2f04d23bb6c3fec326e(
    value: typing.Optional[GoogleMonitoringSloRequestBasedSli],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7510f436e42e9568d51c2dd209fb91ced383bd5a8a2413a37fea383ad2952354(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__622784d9038cc6a428ce0ec3f7cd1c184068da1aa5d27e704f95abc6765bf3af(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e00ed7a61b6f8940967c360c8642f8b64f1e8ca4a04580dea6bd8185b4241ac9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38f74684f2832d927f636ac356455d27eb4044a3f5e5a436ddfbe0380ee956ea(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9f638327371d288f3f1868973486f837f3498e52196a70e3e01f48280d58875(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1ca28a80b90ab16b89a9368459b87a3b63bfb970f42985fcaa92866358d274e(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleMonitoringSloTimeouts]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c83fb1f2e3c959039975e48591d358ce70f6970f985548e2d244ea51153cb0e7(
    *,
    good_bad_metric_filter: typing.Optional[builtins.str] = None,
    good_total_ratio_threshold: typing.Optional[typing.Union[GoogleMonitoringSloWindowsBasedSliGoodTotalRatioThreshold, typing.Dict[builtins.str, typing.Any]]] = None,
    metric_mean_in_range: typing.Optional[typing.Union[GoogleMonitoringSloWindowsBasedSliMetricMeanInRange, typing.Dict[builtins.str, typing.Any]]] = None,
    metric_sum_in_range: typing.Optional[typing.Union[GoogleMonitoringSloWindowsBasedSliMetricSumInRange, typing.Dict[builtins.str, typing.Any]]] = None,
    window_period: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec8bc6b6ddae4d6f759772a758d7d316eedf3cb2986f3fe700e3ae9a6f1db35c(
    *,
    basic_sli_performance: typing.Optional[typing.Union[GoogleMonitoringSloWindowsBasedSliGoodTotalRatioThresholdBasicSliPerformance, typing.Dict[builtins.str, typing.Any]]] = None,
    performance: typing.Optional[typing.Union[GoogleMonitoringSloWindowsBasedSliGoodTotalRatioThresholdPerformance, typing.Dict[builtins.str, typing.Any]]] = None,
    threshold: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2185c34869967e5df51026f56d2b1393a72978ccaf8bff03ff1ce0a5c99c9678(
    *,
    availability: typing.Optional[typing.Union[GoogleMonitoringSloWindowsBasedSliGoodTotalRatioThresholdBasicSliPerformanceAvailability, typing.Dict[builtins.str, typing.Any]]] = None,
    latency: typing.Optional[typing.Union[GoogleMonitoringSloWindowsBasedSliGoodTotalRatioThresholdBasicSliPerformanceLatency, typing.Dict[builtins.str, typing.Any]]] = None,
    location: typing.Optional[typing.Sequence[builtins.str]] = None,
    method: typing.Optional[typing.Sequence[builtins.str]] = None,
    version: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__527653955244846709f7a104b6201ca150b260b62fb18bdd7b1263f1382dec34(
    *,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fedf9d44ff1387479089c7adff079b7ee03fec4bb2a24f1c7a637e0631fb1227(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f661c9773f3a19a25ad516708103966ab72f9b850644c296e676f4e18f4e10be(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d2b4572f0f71dcae3d2e4e455d8d8d353c18fec7b127b0cdec0897452a7aac1(
    value: typing.Optional[GoogleMonitoringSloWindowsBasedSliGoodTotalRatioThresholdBasicSliPerformanceAvailability],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96c59b57a749da14f11f45e32264e97936a4ea338266aff7e7d990ed9fe6585c(
    *,
    threshold: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a026a2cb63f4a5688ecbfc575808348a2ac719727dc521e34c79e9c3137dffd(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f2d2bf1fbeeab0c09f606be87e09195e8a6c02d3a1ff156feb1b9c65311bbbe(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e69ca2a202fc7cad9d0a9c2b48ac0fc66fa4f87bb65d30704be197723f9307b(
    value: typing.Optional[GoogleMonitoringSloWindowsBasedSliGoodTotalRatioThresholdBasicSliPerformanceLatency],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__217fe7d91ac9e0dde7228b6b5ce492bc1e1fb0b03460761119ec06de2f93dfd5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f4f3d26afb3a44ecb930b361a4c9a49a004e6deae76a75b1beabe9652dd74e5(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cbab6cd36f01dd3d09b64d552408d9544464330dfc0d1a11e68de1b762c189df(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c86f089856c1247e0a53dd48303fb7942711d2d9b8d165f4d1ce6cc864797569(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ca9051cb9a04ead7d19a0b2d0305f85316130a43ab932ded469bce91a5242ce(
    value: typing.Optional[GoogleMonitoringSloWindowsBasedSliGoodTotalRatioThresholdBasicSliPerformance],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0df884151f9185d8f015e6fcab58b4601f8663b9c2dc66640083a26060680420(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5209182b7906a4cfa75010fc3c644e2cbf2f972a4ae48e8d47ecd84507c34a8f(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e00ce614bc08dd26d688491ee18d26c089dc55152ac63a5ce4208b3872139e25(
    value: typing.Optional[GoogleMonitoringSloWindowsBasedSliGoodTotalRatioThreshold],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a131d08b4c9cb3ca45b1e7239544f6557bae753e7e474f09fdb41c3520ea891f(
    *,
    distribution_cut: typing.Optional[typing.Union[GoogleMonitoringSloWindowsBasedSliGoodTotalRatioThresholdPerformanceDistributionCut, typing.Dict[builtins.str, typing.Any]]] = None,
    good_total_ratio: typing.Optional[typing.Union[GoogleMonitoringSloWindowsBasedSliGoodTotalRatioThresholdPerformanceGoodTotalRatio, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e28bb87ffbc643dcbcc2d77a8b4306adeee591d12e290b7ab97539eadf43d41(
    *,
    distribution_filter: builtins.str,
    range: typing.Union[GoogleMonitoringSloWindowsBasedSliGoodTotalRatioThresholdPerformanceDistributionCutRange, typing.Dict[builtins.str, typing.Any]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__efb491fc4e31d3c4fb6758f9c015d015d8f2528908fedd75f85f1ab129883aef(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d158cc26db0a3d39e2f25a2a163aeef9c4a2955cbbc84423cd27197bc702814f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1004262ff59486dd66e7a6dc0fe72886403d1376a8c2d69561890b0b4c6364db(
    value: typing.Optional[GoogleMonitoringSloWindowsBasedSliGoodTotalRatioThresholdPerformanceDistributionCut],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d463367d08b1f71e02ba6dfcd6ae5b419ddc1debc5c7ea9d7c87b3d94fa82971(
    *,
    max: typing.Optional[jsii.Number] = None,
    min: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62971dae28b49e26dc91b69204876d2ee613d566e39c2523bcb46de74c0c8d42(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__70b3a973a99b7261e4de7da061b62246d04b9821c584a084d89a737870e0a5c1(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ec9ca4cf6b4e635b5db1d66b6f1fe17c4b8be5d7bd649ec77ac0571379f6a1e(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42dda9fad0d9f5096936a10e4f5b395922e489a5c283997c38537155f1481d99(
    value: typing.Optional[GoogleMonitoringSloWindowsBasedSliGoodTotalRatioThresholdPerformanceDistributionCutRange],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c406bae56ea5de3ba3a5f3bf882e34cbeb7c404f82a08ea1c35317571a0054df(
    *,
    bad_service_filter: typing.Optional[builtins.str] = None,
    good_service_filter: typing.Optional[builtins.str] = None,
    total_service_filter: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f4db84814ad1ee17189df427cd33c7dabc1d2d826ecaca35b45af9e6f619ac2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0481ae3ed66a95a2fe860d93aa9dd129fafee0fb55d8ac6e2bc20d516bb42331(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d1a3662205ac4b919d016c731966ddf1c6ec7f976832bc4b8890a0ff3849bf9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de13f1ade0e887807e0f2c7348cd3c52118516203706700afd7c13de68319684(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf67f4af99d0960d86ae2223d3ac7a420dbb0d17ba61f02ce024e35f08766ab5(
    value: typing.Optional[GoogleMonitoringSloWindowsBasedSliGoodTotalRatioThresholdPerformanceGoodTotalRatio],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4911d829d341da3f42aef6593eb704aac326a1870262ce07e7a090305f51bdf(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f653ea9686f74cf4f120f527859d69578b7e62063865b564ce5fbb375ccca6a9(
    value: typing.Optional[GoogleMonitoringSloWindowsBasedSliGoodTotalRatioThresholdPerformance],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae8e64b9def803407892e4244faaa60a808dce63e915134c5d199c62407ed6f7(
    *,
    range: typing.Union[GoogleMonitoringSloWindowsBasedSliMetricMeanInRangeRange, typing.Dict[builtins.str, typing.Any]],
    time_series: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03f9f2aa278b02b383b0741b9974438d48a3fac131ebce548b9b32a26079e9ab(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14d55db43dc5e2f18627d4a714d116036be14be7c2ebeb080117e6da7706d0a0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64f9e52103ff563dad322f509f91ad14e1b67361b0420ffd2cc21ebc07464f6b(
    value: typing.Optional[GoogleMonitoringSloWindowsBasedSliMetricMeanInRange],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b1fac05055ef61f7daacf12d524de10cb41179b26a65c122f792f870447a81a(
    *,
    max: typing.Optional[jsii.Number] = None,
    min: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa2c6eb1367197c5f4f8973fcc8a49e910a9f18fb3e0536b30cd7b0bf4b04147(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cba0fdbf0e39c35156fdc6859907939f6e94fad42204e82a468284599bb0522d(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d880ee8652b50076ba116d02a3b8034bb8be065d6180df7e8fd475703e72045d(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae52d43fb42c37b6907ec8b53d86d2bd52e6236254c579024d1850ff50e20c79(
    value: typing.Optional[GoogleMonitoringSloWindowsBasedSliMetricMeanInRangeRange],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e7ecadadbe333ecf896ad956315ee1ce68ded53f3514ff5e5ec029813027d7e(
    *,
    range: typing.Union[GoogleMonitoringSloWindowsBasedSliMetricSumInRangeRange, typing.Dict[builtins.str, typing.Any]],
    time_series: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c914894775721c16635f94fe37cd4520e6f31e092a1a3a5723ebee693e5e532b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b18e8efd4419b11a3745826c2e3828e3447522958136bd16eb0057d275d262fa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea245dddd961c8076d1bf76bd76ef1848fd2cbd17d96e31442ce151f58da6583(
    value: typing.Optional[GoogleMonitoringSloWindowsBasedSliMetricSumInRange],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91b00091ff969bee08d7427a6be32276f168d038a45d2c39a13e18016cf4d009(
    *,
    max: typing.Optional[jsii.Number] = None,
    min: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__55fd835ffc4d2c3d94e849452c754852c2e26a63ee125359277311dc81d9a094(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e31899706362ce1be993fd6cf5c9f14492d51d0a562faa0eacba060b083b7f2e(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ccb0c9ac3acdc5f3cfd5a8da00a936f0f6ca16d2891db9c6226e728c8c6a8411(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88fff5eb9f7e751c894392a2767c2656d1d38bb2195ed36894f37481da263f6b(
    value: typing.Optional[GoogleMonitoringSloWindowsBasedSliMetricSumInRangeRange],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1300f4a56ee225e74655c3f0315f607790bac1017b65a56e4dab6a64c4ac633(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f52af4d01172f03d269d49b9ddf9b0351711b6eac3f7de68933afe83de6e61d3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0c5d9759c124d7393b4416b677068b1cf7b2ba76cbe259c3ec4b356dd19d384(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8564f59f273aecb50af9c0d70ec833a3bd42e4130e374cbcc2b07df03a240d5(
    value: typing.Optional[GoogleMonitoringSloWindowsBasedSli],
) -> None:
    """Type checking stubs"""
    pass
