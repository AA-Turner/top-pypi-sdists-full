r'''
# `newrelic_nrql_alert_condition`

Refer to the Terraform Registry for docs: [`newrelic_nrql_alert_condition`](https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/nrql_alert_condition).
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


class NrqlAlertCondition(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.nrqlAlertCondition.NrqlAlertCondition",
):
    '''Represents a {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/nrql_alert_condition newrelic_nrql_alert_condition}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        name: builtins.str,
        nrql: typing.Union["NrqlAlertConditionNrql", typing.Dict[builtins.str, typing.Any]],
        policy_id: jsii.Number,
        account_id: typing.Optional[jsii.Number] = None,
        aggregation_delay: typing.Optional[builtins.str] = None,
        aggregation_method: typing.Optional[builtins.str] = None,
        aggregation_timer: typing.Optional[builtins.str] = None,
        aggregation_window: typing.Optional[jsii.Number] = None,
        baseline_direction: typing.Optional[builtins.str] = None,
        close_violations_on_expiration: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        critical: typing.Optional[typing.Union["NrqlAlertConditionCritical", typing.Dict[builtins.str, typing.Any]]] = None,
        description: typing.Optional[builtins.str] = None,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        evaluation_delay: typing.Optional[jsii.Number] = None,
        expiration_duration: typing.Optional[jsii.Number] = None,
        fill_option: typing.Optional[builtins.str] = None,
        fill_value: typing.Optional[jsii.Number] = None,
        id: typing.Optional[builtins.str] = None,
        ignore_on_expected_termination: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        open_violation_on_expiration: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        runbook_url: typing.Optional[builtins.str] = None,
        signal_seasonality: typing.Optional[builtins.str] = None,
        slide_by: typing.Optional[jsii.Number] = None,
        term: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["NrqlAlertConditionTerm", typing.Dict[builtins.str, typing.Any]]]]] = None,
        timeouts: typing.Optional[typing.Union["NrqlAlertConditionTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        title_template: typing.Optional[builtins.str] = None,
        type: typing.Optional[builtins.str] = None,
        violation_time_limit: typing.Optional[builtins.str] = None,
        violation_time_limit_seconds: typing.Optional[jsii.Number] = None,
        warning: typing.Optional[typing.Union["NrqlAlertConditionWarning", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/nrql_alert_condition newrelic_nrql_alert_condition} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: The title of the condition. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/nrql_alert_condition#name NrqlAlertCondition#name}
        :param nrql: nrql block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/nrql_alert_condition#nrql NrqlAlertCondition#nrql}
        :param policy_id: The ID of the policy where this condition should be used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/nrql_alert_condition#policy_id NrqlAlertCondition#policy_id}
        :param account_id: The New Relic account ID for managing your NRQL alert conditions. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/nrql_alert_condition#account_id NrqlAlertCondition#account_id}
        :param aggregation_delay: How long we wait for data that belongs in each aggregation window. Depending on your data, a longer delay may increase accuracy but delay notifications. Use aggregationDelay with the EVENT_FLOW and CADENCE aggregation methods. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/nrql_alert_condition#aggregation_delay NrqlAlertCondition#aggregation_delay}
        :param aggregation_method: The method that determines when we consider an aggregation window to be complete so that we can evaluate the signal for incidents. Default is EVENT_FLOW. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/nrql_alert_condition#aggregation_method NrqlAlertCondition#aggregation_method}
        :param aggregation_timer: How long we wait after each data point arrives to make sure we've processed the whole batch. Use aggregationTimer with the EVENT_TIMER aggregation method. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/nrql_alert_condition#aggregation_timer NrqlAlertCondition#aggregation_timer}
        :param aggregation_window: The duration of the time window used to evaluate the NRQL query, in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/nrql_alert_condition#aggregation_window NrqlAlertCondition#aggregation_window}
        :param baseline_direction: The baseline direction of a baseline NRQL alert condition. Valid values are: 'LOWER_ONLY', 'UPPER_AND_LOWER', 'UPPER_ONLY' (case insensitive). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/nrql_alert_condition#baseline_direction NrqlAlertCondition#baseline_direction}
        :param close_violations_on_expiration: Whether to close all open incidents when the signal expires. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/nrql_alert_condition#close_violations_on_expiration NrqlAlertCondition#close_violations_on_expiration}
        :param critical: critical block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/nrql_alert_condition#critical NrqlAlertCondition#critical}
        :param description: The description of the NRQL alert condition. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/nrql_alert_condition#description NrqlAlertCondition#description}
        :param enabled: Whether or not to enable the alert condition. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/nrql_alert_condition#enabled NrqlAlertCondition#enabled}
        :param evaluation_delay: How long we wait until the signal starts evaluating. The maximum delay is 7200 seconds (120 minutes). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/nrql_alert_condition#evaluation_delay NrqlAlertCondition#evaluation_delay}
        :param expiration_duration: The amount of time (in seconds) to wait before considering the signal expired. Must be in the range of 30 to 172800 (inclusive) Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/nrql_alert_condition#expiration_duration NrqlAlertCondition#expiration_duration}
        :param fill_option: Which strategy to use when filling gaps in the signal. If static, the 'fill value' will be used for filling gaps in the signal. Valid values are: 'NONE', 'LAST_VALUE', or 'STATIC' (case insensitive). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/nrql_alert_condition#fill_option NrqlAlertCondition#fill_option}
        :param fill_value: If using the 'static' fill option, this value will be used for filling gaps in the signal. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/nrql_alert_condition#fill_value NrqlAlertCondition#fill_value}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/nrql_alert_condition#id NrqlAlertCondition#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param ignore_on_expected_termination: Whether to ignore expected termination of a signal when considering whether to create a loss of signal incident. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/nrql_alert_condition#ignore_on_expected_termination NrqlAlertCondition#ignore_on_expected_termination}
        :param open_violation_on_expiration: Whether to create a new incident to capture that the signal expired. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/nrql_alert_condition#open_violation_on_expiration NrqlAlertCondition#open_violation_on_expiration}
        :param runbook_url: Runbook URL to display in notifications. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/nrql_alert_condition#runbook_url NrqlAlertCondition#runbook_url}
        :param signal_seasonality: Seasonality under which a condition's signal(s) are evaluated. Valid values are: 'NEW_RELIC_CALCULATION', 'HOURLY', 'DAILY', 'WEEKLY', or 'NONE'. To have New Relic calculate seasonality automatically, set to 'NEW_RELIC_CALCULATION' (default). To turn off seasonality completely, set to 'NONE'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/nrql_alert_condition#signal_seasonality NrqlAlertCondition#signal_seasonality}
        :param slide_by: The duration of overlapping time windows used to smooth the chart line, in seconds. Must be a factor of ``aggregation_window`` and less than the aggregation window. If ``aggregation_window`` is less than or equal to 3600 seconds, it should be greater or equal to 30 seconds. If ``aggregation_window`` is greater than 3600 seconds but less than 7200 seconds, it should be greater or equal to ``aggregation_window / 120``. If ``aggregation_window`` is greater than 7200 seconds, it should be greater or equal to `aggregation_window / 24 Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/nrql_alert_condition#slide_by NrqlAlertCondition#slide_by}
        :param term: term block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/nrql_alert_condition#term NrqlAlertCondition#term}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/nrql_alert_condition#timeouts NrqlAlertCondition#timeouts}
        :param title_template: This field allows you to create a custom title to be used when incidents are opened by the condition. Setting this field will override the default title. Must be Handlebars format. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/nrql_alert_condition#title_template NrqlAlertCondition#title_template}
        :param type: The type of NRQL alert condition to create. Valid values are: 'static', 'baseline'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/nrql_alert_condition#type NrqlAlertCondition#type}
        :param violation_time_limit: Sets a time limit, in hours, that will automatically force-close a long-lasting incident after the time limit you select. Possible values are 'ONE_HOUR', 'TWO_HOURS', 'FOUR_HOURS', 'EIGHT_HOURS', 'TWELVE_HOURS', 'TWENTY_FOUR_HOURS', 'THIRTY_DAYS' (case insensitive). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/nrql_alert_condition#violation_time_limit NrqlAlertCondition#violation_time_limit}
        :param violation_time_limit_seconds: Sets a time limit, in seconds, that will automatically force-close a long-lasting incident after the time limit you select. Must be in the range of 300 to 2592000 (inclusive) Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/nrql_alert_condition#violation_time_limit_seconds NrqlAlertCondition#violation_time_limit_seconds}
        :param warning: warning block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/nrql_alert_condition#warning NrqlAlertCondition#warning}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e52eb0f2929f737ba1776df9d79a771b2f00a332e1b163d9ab3fa64a7d8e284b)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = NrqlAlertConditionConfig(
            name=name,
            nrql=nrql,
            policy_id=policy_id,
            account_id=account_id,
            aggregation_delay=aggregation_delay,
            aggregation_method=aggregation_method,
            aggregation_timer=aggregation_timer,
            aggregation_window=aggregation_window,
            baseline_direction=baseline_direction,
            close_violations_on_expiration=close_violations_on_expiration,
            critical=critical,
            description=description,
            enabled=enabled,
            evaluation_delay=evaluation_delay,
            expiration_duration=expiration_duration,
            fill_option=fill_option,
            fill_value=fill_value,
            id=id,
            ignore_on_expected_termination=ignore_on_expected_termination,
            open_violation_on_expiration=open_violation_on_expiration,
            runbook_url=runbook_url,
            signal_seasonality=signal_seasonality,
            slide_by=slide_by,
            term=term,
            timeouts=timeouts,
            title_template=title_template,
            type=type,
            violation_time_limit=violation_time_limit,
            violation_time_limit_seconds=violation_time_limit_seconds,
            warning=warning,
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
        '''Generates CDKTF code for importing a NrqlAlertCondition resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the NrqlAlertCondition to import.
        :param import_from_id: The id of the existing NrqlAlertCondition that should be imported. Refer to the {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/nrql_alert_condition#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the NrqlAlertCondition to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e79d1dec7621d60689a8187f4a099221235baf35b489f1d84c73121c677f404)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putCritical")
    def put_critical(
        self,
        *,
        threshold: jsii.Number,
        disable_health_status_reporting: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        duration: typing.Optional[jsii.Number] = None,
        operator: typing.Optional[builtins.str] = None,
        prediction: typing.Optional[typing.Union["NrqlAlertConditionCriticalPrediction", typing.Dict[builtins.str, typing.Any]]] = None,
        threshold_duration: typing.Optional[jsii.Number] = None,
        threshold_occurrences: typing.Optional[builtins.str] = None,
        time_function: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param threshold: For baseline conditions must be in range [1, 1000]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/nrql_alert_condition#threshold NrqlAlertCondition#threshold}
        :param disable_health_status_reporting: Violations will not change system health status for this term. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/nrql_alert_condition#disable_health_status_reporting NrqlAlertCondition#disable_health_status_reporting}
        :param duration: In minutes, must be in the range of 1 to 120 (inclusive). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/nrql_alert_condition#duration NrqlAlertCondition#duration}
        :param operator: One of (above, above_or_equals, below, below_or_equals, equals, not_equals). Defaults to 'equals'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/nrql_alert_condition#operator NrqlAlertCondition#operator}
        :param prediction: prediction block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/nrql_alert_condition#prediction NrqlAlertCondition#prediction}
        :param threshold_duration: The duration, in seconds, that the threshold must violate in order to create an incident. Value must be a multiple of the 'aggregation_window' (which has a default of 60 seconds). Value must be within 120-86400 seconds for baseline conditions, and within 60-86400 seconds for static conditions Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/nrql_alert_condition#threshold_duration NrqlAlertCondition#threshold_duration}
        :param threshold_occurrences: The criteria for how many data points must be in violation for the specified threshold duration. Valid values are: 'ALL' or 'AT_LEAST_ONCE' (case insensitive). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/nrql_alert_condition#threshold_occurrences NrqlAlertCondition#threshold_occurrences}
        :param time_function: Valid values are: 'all' or 'any'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/nrql_alert_condition#time_function NrqlAlertCondition#time_function}
        '''
        value = NrqlAlertConditionCritical(
            threshold=threshold,
            disable_health_status_reporting=disable_health_status_reporting,
            duration=duration,
            operator=operator,
            prediction=prediction,
            threshold_duration=threshold_duration,
            threshold_occurrences=threshold_occurrences,
            time_function=time_function,
        )

        return typing.cast(None, jsii.invoke(self, "putCritical", [value]))

    @jsii.member(jsii_name="putNrql")
    def put_nrql(
        self,
        *,
        query: builtins.str,
        data_account_id: typing.Optional[jsii.Number] = None,
        evaluation_offset: typing.Optional[jsii.Number] = None,
        since_value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param query: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/nrql_alert_condition#query NrqlAlertCondition#query}.
        :param data_account_id: The New Relic account ID to use as the basis for the NRQL alert condition's ``query``; will default to ``account_id`` if unspecified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/nrql_alert_condition#data_account_id NrqlAlertCondition#data_account_id}
        :param evaluation_offset: NRQL queries are evaluated in one-minute time windows. The start time depends on the value you provide in the NRQL condition's ``evaluation_offset``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/nrql_alert_condition#evaluation_offset NrqlAlertCondition#evaluation_offset}
        :param since_value: NRQL queries are evaluated in one-minute time windows. The start time depends on the value you provide in the NRQL condition's ``since_value``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/nrql_alert_condition#since_value NrqlAlertCondition#since_value}
        '''
        value = NrqlAlertConditionNrql(
            query=query,
            data_account_id=data_account_id,
            evaluation_offset=evaluation_offset,
            since_value=since_value,
        )

        return typing.cast(None, jsii.invoke(self, "putNrql", [value]))

    @jsii.member(jsii_name="putTerm")
    def put_term(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["NrqlAlertConditionTerm", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__851d50fac13c83b56520f6d4f20e709f2cfa7ed90e48fa776d7fdbf7744e538b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putTerm", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(self, *, create: typing.Optional[builtins.str] = None) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/nrql_alert_condition#create NrqlAlertCondition#create}.
        '''
        value = NrqlAlertConditionTimeouts(create=create)

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="putWarning")
    def put_warning(
        self,
        *,
        threshold: jsii.Number,
        disable_health_status_reporting: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        duration: typing.Optional[jsii.Number] = None,
        operator: typing.Optional[builtins.str] = None,
        prediction: typing.Optional[typing.Union["NrqlAlertConditionWarningPrediction", typing.Dict[builtins.str, typing.Any]]] = None,
        threshold_duration: typing.Optional[jsii.Number] = None,
        threshold_occurrences: typing.Optional[builtins.str] = None,
        time_function: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param threshold: For baseline conditions must be in range [1, 1000]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/nrql_alert_condition#threshold NrqlAlertCondition#threshold}
        :param disable_health_status_reporting: Violations will not change system health status for this term. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/nrql_alert_condition#disable_health_status_reporting NrqlAlertCondition#disable_health_status_reporting}
        :param duration: In minutes, must be in the range of 1 to 120 (inclusive). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/nrql_alert_condition#duration NrqlAlertCondition#duration}
        :param operator: One of (above, above_or_equals, below, below_or_equals, equals, not_equals). Defaults to 'equals'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/nrql_alert_condition#operator NrqlAlertCondition#operator}
        :param prediction: prediction block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/nrql_alert_condition#prediction NrqlAlertCondition#prediction}
        :param threshold_duration: The duration, in seconds, that the threshold must violate in order to create an incident. Value must be a multiple of the 'aggregation_window' (which has a default of 60 seconds). Value must be within 120-86400 seconds for baseline conditions, and within 60-86400 seconds for static conditions Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/nrql_alert_condition#threshold_duration NrqlAlertCondition#threshold_duration}
        :param threshold_occurrences: The criteria for how many data points must be in violation for the specified threshold duration. Valid values are: 'ALL' or 'AT_LEAST_ONCE' (case insensitive). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/nrql_alert_condition#threshold_occurrences NrqlAlertCondition#threshold_occurrences}
        :param time_function: Valid values are: 'all' or 'any'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/nrql_alert_condition#time_function NrqlAlertCondition#time_function}
        '''
        value = NrqlAlertConditionWarning(
            threshold=threshold,
            disable_health_status_reporting=disable_health_status_reporting,
            duration=duration,
            operator=operator,
            prediction=prediction,
            threshold_duration=threshold_duration,
            threshold_occurrences=threshold_occurrences,
            time_function=time_function,
        )

        return typing.cast(None, jsii.invoke(self, "putWarning", [value]))

    @jsii.member(jsii_name="resetAccountId")
    def reset_account_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAccountId", []))

    @jsii.member(jsii_name="resetAggregationDelay")
    def reset_aggregation_delay(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAggregationDelay", []))

    @jsii.member(jsii_name="resetAggregationMethod")
    def reset_aggregation_method(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAggregationMethod", []))

    @jsii.member(jsii_name="resetAggregationTimer")
    def reset_aggregation_timer(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAggregationTimer", []))

    @jsii.member(jsii_name="resetAggregationWindow")
    def reset_aggregation_window(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAggregationWindow", []))

    @jsii.member(jsii_name="resetBaselineDirection")
    def reset_baseline_direction(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBaselineDirection", []))

    @jsii.member(jsii_name="resetCloseViolationsOnExpiration")
    def reset_close_violations_on_expiration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCloseViolationsOnExpiration", []))

    @jsii.member(jsii_name="resetCritical")
    def reset_critical(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCritical", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetEnabled")
    def reset_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnabled", []))

    @jsii.member(jsii_name="resetEvaluationDelay")
    def reset_evaluation_delay(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEvaluationDelay", []))

    @jsii.member(jsii_name="resetExpirationDuration")
    def reset_expiration_duration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExpirationDuration", []))

    @jsii.member(jsii_name="resetFillOption")
    def reset_fill_option(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFillOption", []))

    @jsii.member(jsii_name="resetFillValue")
    def reset_fill_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFillValue", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetIgnoreOnExpectedTermination")
    def reset_ignore_on_expected_termination(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIgnoreOnExpectedTermination", []))

    @jsii.member(jsii_name="resetOpenViolationOnExpiration")
    def reset_open_violation_on_expiration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOpenViolationOnExpiration", []))

    @jsii.member(jsii_name="resetRunbookUrl")
    def reset_runbook_url(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRunbookUrl", []))

    @jsii.member(jsii_name="resetSignalSeasonality")
    def reset_signal_seasonality(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSignalSeasonality", []))

    @jsii.member(jsii_name="resetSlideBy")
    def reset_slide_by(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSlideBy", []))

    @jsii.member(jsii_name="resetTerm")
    def reset_term(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTerm", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

    @jsii.member(jsii_name="resetTitleTemplate")
    def reset_title_template(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTitleTemplate", []))

    @jsii.member(jsii_name="resetType")
    def reset_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetType", []))

    @jsii.member(jsii_name="resetViolationTimeLimit")
    def reset_violation_time_limit(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetViolationTimeLimit", []))

    @jsii.member(jsii_name="resetViolationTimeLimitSeconds")
    def reset_violation_time_limit_seconds(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetViolationTimeLimitSeconds", []))

    @jsii.member(jsii_name="resetWarning")
    def reset_warning(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWarning", []))

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
    @jsii.member(jsii_name="critical")
    def critical(self) -> "NrqlAlertConditionCriticalOutputReference":
        return typing.cast("NrqlAlertConditionCriticalOutputReference", jsii.get(self, "critical"))

    @builtins.property
    @jsii.member(jsii_name="entityGuid")
    def entity_guid(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "entityGuid"))

    @builtins.property
    @jsii.member(jsii_name="nrql")
    def nrql(self) -> "NrqlAlertConditionNrqlOutputReference":
        return typing.cast("NrqlAlertConditionNrqlOutputReference", jsii.get(self, "nrql"))

    @builtins.property
    @jsii.member(jsii_name="term")
    def term(self) -> "NrqlAlertConditionTermList":
        return typing.cast("NrqlAlertConditionTermList", jsii.get(self, "term"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "NrqlAlertConditionTimeoutsOutputReference":
        return typing.cast("NrqlAlertConditionTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="warning")
    def warning(self) -> "NrqlAlertConditionWarningOutputReference":
        return typing.cast("NrqlAlertConditionWarningOutputReference", jsii.get(self, "warning"))

    @builtins.property
    @jsii.member(jsii_name="accountIdInput")
    def account_id_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "accountIdInput"))

    @builtins.property
    @jsii.member(jsii_name="aggregationDelayInput")
    def aggregation_delay_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "aggregationDelayInput"))

    @builtins.property
    @jsii.member(jsii_name="aggregationMethodInput")
    def aggregation_method_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "aggregationMethodInput"))

    @builtins.property
    @jsii.member(jsii_name="aggregationTimerInput")
    def aggregation_timer_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "aggregationTimerInput"))

    @builtins.property
    @jsii.member(jsii_name="aggregationWindowInput")
    def aggregation_window_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "aggregationWindowInput"))

    @builtins.property
    @jsii.member(jsii_name="baselineDirectionInput")
    def baseline_direction_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "baselineDirectionInput"))

    @builtins.property
    @jsii.member(jsii_name="closeViolationsOnExpirationInput")
    def close_violations_on_expiration_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "closeViolationsOnExpirationInput"))

    @builtins.property
    @jsii.member(jsii_name="criticalInput")
    def critical_input(self) -> typing.Optional["NrqlAlertConditionCritical"]:
        return typing.cast(typing.Optional["NrqlAlertConditionCritical"], jsii.get(self, "criticalInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="enabledInput")
    def enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enabledInput"))

    @builtins.property
    @jsii.member(jsii_name="evaluationDelayInput")
    def evaluation_delay_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "evaluationDelayInput"))

    @builtins.property
    @jsii.member(jsii_name="expirationDurationInput")
    def expiration_duration_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "expirationDurationInput"))

    @builtins.property
    @jsii.member(jsii_name="fillOptionInput")
    def fill_option_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "fillOptionInput"))

    @builtins.property
    @jsii.member(jsii_name="fillValueInput")
    def fill_value_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "fillValueInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="ignoreOnExpectedTerminationInput")
    def ignore_on_expected_termination_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "ignoreOnExpectedTerminationInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="nrqlInput")
    def nrql_input(self) -> typing.Optional["NrqlAlertConditionNrql"]:
        return typing.cast(typing.Optional["NrqlAlertConditionNrql"], jsii.get(self, "nrqlInput"))

    @builtins.property
    @jsii.member(jsii_name="openViolationOnExpirationInput")
    def open_violation_on_expiration_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "openViolationOnExpirationInput"))

    @builtins.property
    @jsii.member(jsii_name="policyIdInput")
    def policy_id_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "policyIdInput"))

    @builtins.property
    @jsii.member(jsii_name="runbookUrlInput")
    def runbook_url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "runbookUrlInput"))

    @builtins.property
    @jsii.member(jsii_name="signalSeasonalityInput")
    def signal_seasonality_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "signalSeasonalityInput"))

    @builtins.property
    @jsii.member(jsii_name="slideByInput")
    def slide_by_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "slideByInput"))

    @builtins.property
    @jsii.member(jsii_name="termInput")
    def term_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NrqlAlertConditionTerm"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NrqlAlertConditionTerm"]]], jsii.get(self, "termInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "NrqlAlertConditionTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "NrqlAlertConditionTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="titleTemplateInput")
    def title_template_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "titleTemplateInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="violationTimeLimitInput")
    def violation_time_limit_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "violationTimeLimitInput"))

    @builtins.property
    @jsii.member(jsii_name="violationTimeLimitSecondsInput")
    def violation_time_limit_seconds_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "violationTimeLimitSecondsInput"))

    @builtins.property
    @jsii.member(jsii_name="warningInput")
    def warning_input(self) -> typing.Optional["NrqlAlertConditionWarning"]:
        return typing.cast(typing.Optional["NrqlAlertConditionWarning"], jsii.get(self, "warningInput"))

    @builtins.property
    @jsii.member(jsii_name="accountId")
    def account_id(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "accountId"))

    @account_id.setter
    def account_id(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__649a181d2072f4986a6d916e0fb1b523d523ac324e9d34cb668c3b071ab95216)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accountId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="aggregationDelay")
    def aggregation_delay(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "aggregationDelay"))

    @aggregation_delay.setter
    def aggregation_delay(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2cf83ef31936d18108d0d7869272a1c8b68ee44b30362ccc0e4a553f78a6fd36)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "aggregationDelay", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="aggregationMethod")
    def aggregation_method(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "aggregationMethod"))

    @aggregation_method.setter
    def aggregation_method(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c53efff34b60671f0633dda09ad8cd277ced39b706772506e9bf8c0ba9d68f7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "aggregationMethod", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="aggregationTimer")
    def aggregation_timer(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "aggregationTimer"))

    @aggregation_timer.setter
    def aggregation_timer(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5d11a04b2424e03b4f56fd2218a413d1ffc119863799049f6d2fe107edce2206)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "aggregationTimer", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="aggregationWindow")
    def aggregation_window(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "aggregationWindow"))

    @aggregation_window.setter
    def aggregation_window(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c83a096d66a01205222103170d31ff422455bf5f8b1a2176d12b0b1eec7ef77)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "aggregationWindow", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="baselineDirection")
    def baseline_direction(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "baselineDirection"))

    @baseline_direction.setter
    def baseline_direction(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1178104c45a96e85c754764950b49690215ad1d7e5c6970c1fcd56ddc4a1967a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "baselineDirection", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="closeViolationsOnExpiration")
    def close_violations_on_expiration(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "closeViolationsOnExpiration"))

    @close_violations_on_expiration.setter
    def close_violations_on_expiration(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ad799bf9921ce6ec8d6b2f55c260e5b238c4bfcd33ca1861a5c3639a16036d4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "closeViolationsOnExpiration", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__844560a7037a9b8f022aae9243361dc8c7883e5effb553677f4997ae891de136)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

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
            type_hints = typing.get_type_hints(_typecheckingstub__df6416b87f6aa0ae47d2d61248337887867763e9beaaa54c78a5f0701110aec7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="evaluationDelay")
    def evaluation_delay(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "evaluationDelay"))

    @evaluation_delay.setter
    def evaluation_delay(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3026a32318e81a7cb6cbcd36463c84b2348ac09f647b8d2a6ef4a4b4ee2c5aaf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "evaluationDelay", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="expirationDuration")
    def expiration_duration(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "expirationDuration"))

    @expiration_duration.setter
    def expiration_duration(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4b10ee5ebf73800fff06eeaeaa5a0297eb5a1a9941adf9030affa878abbf8b6a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "expirationDuration", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="fillOption")
    def fill_option(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "fillOption"))

    @fill_option.setter
    def fill_option(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5a277ffdb5cc4519b811e78635819ea848d780f0d307eb9d228d10372b53856f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fillOption", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="fillValue")
    def fill_value(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "fillValue"))

    @fill_value.setter
    def fill_value(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e2ba585e1de77b18cdee092bc6924807ee2afbeec0753a019d66bdf53fabf74f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fillValue", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1ca73208e17ed2b1c79afdb18903405f0fab6a4ef181e7b60c7a2ee763b494e6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ignoreOnExpectedTermination")
    def ignore_on_expected_termination(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "ignoreOnExpectedTermination"))

    @ignore_on_expected_termination.setter
    def ignore_on_expected_termination(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__112ae38312274f8905f9db29f0d82f726039e66ded6af4fe7b3b1ea69e6ffe22)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ignoreOnExpectedTermination", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__50e9efa16666dc60ee2056f36051e419522e2b838d489e75a0de5eed91b719f5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="openViolationOnExpiration")
    def open_violation_on_expiration(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "openViolationOnExpiration"))

    @open_violation_on_expiration.setter
    def open_violation_on_expiration(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2dd7027f0f0cb75a1e2b9066b8521b9353ae41003dca5710d0a1e16f1148c57a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "openViolationOnExpiration", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="policyId")
    def policy_id(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "policyId"))

    @policy_id.setter
    def policy_id(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c65358198af17285a6ee7e5b0d3a07394f4aa1e3c23e1d077d6d8cc5055678c6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "policyId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="runbookUrl")
    def runbook_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "runbookUrl"))

    @runbook_url.setter
    def runbook_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d42d637ba8127466722b67c70c65ac1193c2e5ca86759ccac911e7e986e6ed0b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "runbookUrl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="signalSeasonality")
    def signal_seasonality(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "signalSeasonality"))

    @signal_seasonality.setter
    def signal_seasonality(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f2b8a9a0344c79490b627e46c7e036dd74bd6dca74a718cf9209f0a850ad42af)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "signalSeasonality", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="slideBy")
    def slide_by(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "slideBy"))

    @slide_by.setter
    def slide_by(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aba9e1adf13481848ce3c898ab366ef7f1aa053bf6ed22d0b16375dd1b4266fa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "slideBy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="titleTemplate")
    def title_template(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "titleTemplate"))

    @title_template.setter
    def title_template(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f38e9255c94019f151736a491f525b6a239494adc4f8e48e64e6d6206890392a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "titleTemplate", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4bedef0fb1419f165f98d8ebe6ab344c3681eb4f79e2da4a0fcf1e53f1142b65)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="violationTimeLimit")
    def violation_time_limit(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "violationTimeLimit"))

    @violation_time_limit.setter
    def violation_time_limit(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f2ffbebd1a9672d2f85bd1c49a1d48f04dfba18d558133d676040784ef29c7d9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "violationTimeLimit", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="violationTimeLimitSeconds")
    def violation_time_limit_seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "violationTimeLimitSeconds"))

    @violation_time_limit_seconds.setter
    def violation_time_limit_seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b889225e14227f9771c2c9ef955d88fe029675182009ddcb2021ce90e815343)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "violationTimeLimitSeconds", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-newrelic.nrqlAlertCondition.NrqlAlertConditionConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "name": "name",
        "nrql": "nrql",
        "policy_id": "policyId",
        "account_id": "accountId",
        "aggregation_delay": "aggregationDelay",
        "aggregation_method": "aggregationMethod",
        "aggregation_timer": "aggregationTimer",
        "aggregation_window": "aggregationWindow",
        "baseline_direction": "baselineDirection",
        "close_violations_on_expiration": "closeViolationsOnExpiration",
        "critical": "critical",
        "description": "description",
        "enabled": "enabled",
        "evaluation_delay": "evaluationDelay",
        "expiration_duration": "expirationDuration",
        "fill_option": "fillOption",
        "fill_value": "fillValue",
        "id": "id",
        "ignore_on_expected_termination": "ignoreOnExpectedTermination",
        "open_violation_on_expiration": "openViolationOnExpiration",
        "runbook_url": "runbookUrl",
        "signal_seasonality": "signalSeasonality",
        "slide_by": "slideBy",
        "term": "term",
        "timeouts": "timeouts",
        "title_template": "titleTemplate",
        "type": "type",
        "violation_time_limit": "violationTimeLimit",
        "violation_time_limit_seconds": "violationTimeLimitSeconds",
        "warning": "warning",
    },
)
class NrqlAlertConditionConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        name: builtins.str,
        nrql: typing.Union["NrqlAlertConditionNrql", typing.Dict[builtins.str, typing.Any]],
        policy_id: jsii.Number,
        account_id: typing.Optional[jsii.Number] = None,
        aggregation_delay: typing.Optional[builtins.str] = None,
        aggregation_method: typing.Optional[builtins.str] = None,
        aggregation_timer: typing.Optional[builtins.str] = None,
        aggregation_window: typing.Optional[jsii.Number] = None,
        baseline_direction: typing.Optional[builtins.str] = None,
        close_violations_on_expiration: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        critical: typing.Optional[typing.Union["NrqlAlertConditionCritical", typing.Dict[builtins.str, typing.Any]]] = None,
        description: typing.Optional[builtins.str] = None,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        evaluation_delay: typing.Optional[jsii.Number] = None,
        expiration_duration: typing.Optional[jsii.Number] = None,
        fill_option: typing.Optional[builtins.str] = None,
        fill_value: typing.Optional[jsii.Number] = None,
        id: typing.Optional[builtins.str] = None,
        ignore_on_expected_termination: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        open_violation_on_expiration: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        runbook_url: typing.Optional[builtins.str] = None,
        signal_seasonality: typing.Optional[builtins.str] = None,
        slide_by: typing.Optional[jsii.Number] = None,
        term: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["NrqlAlertConditionTerm", typing.Dict[builtins.str, typing.Any]]]]] = None,
        timeouts: typing.Optional[typing.Union["NrqlAlertConditionTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        title_template: typing.Optional[builtins.str] = None,
        type: typing.Optional[builtins.str] = None,
        violation_time_limit: typing.Optional[builtins.str] = None,
        violation_time_limit_seconds: typing.Optional[jsii.Number] = None,
        warning: typing.Optional[typing.Union["NrqlAlertConditionWarning", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param name: The title of the condition. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/nrql_alert_condition#name NrqlAlertCondition#name}
        :param nrql: nrql block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/nrql_alert_condition#nrql NrqlAlertCondition#nrql}
        :param policy_id: The ID of the policy where this condition should be used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/nrql_alert_condition#policy_id NrqlAlertCondition#policy_id}
        :param account_id: The New Relic account ID for managing your NRQL alert conditions. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/nrql_alert_condition#account_id NrqlAlertCondition#account_id}
        :param aggregation_delay: How long we wait for data that belongs in each aggregation window. Depending on your data, a longer delay may increase accuracy but delay notifications. Use aggregationDelay with the EVENT_FLOW and CADENCE aggregation methods. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/nrql_alert_condition#aggregation_delay NrqlAlertCondition#aggregation_delay}
        :param aggregation_method: The method that determines when we consider an aggregation window to be complete so that we can evaluate the signal for incidents. Default is EVENT_FLOW. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/nrql_alert_condition#aggregation_method NrqlAlertCondition#aggregation_method}
        :param aggregation_timer: How long we wait after each data point arrives to make sure we've processed the whole batch. Use aggregationTimer with the EVENT_TIMER aggregation method. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/nrql_alert_condition#aggregation_timer NrqlAlertCondition#aggregation_timer}
        :param aggregation_window: The duration of the time window used to evaluate the NRQL query, in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/nrql_alert_condition#aggregation_window NrqlAlertCondition#aggregation_window}
        :param baseline_direction: The baseline direction of a baseline NRQL alert condition. Valid values are: 'LOWER_ONLY', 'UPPER_AND_LOWER', 'UPPER_ONLY' (case insensitive). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/nrql_alert_condition#baseline_direction NrqlAlertCondition#baseline_direction}
        :param close_violations_on_expiration: Whether to close all open incidents when the signal expires. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/nrql_alert_condition#close_violations_on_expiration NrqlAlertCondition#close_violations_on_expiration}
        :param critical: critical block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/nrql_alert_condition#critical NrqlAlertCondition#critical}
        :param description: The description of the NRQL alert condition. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/nrql_alert_condition#description NrqlAlertCondition#description}
        :param enabled: Whether or not to enable the alert condition. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/nrql_alert_condition#enabled NrqlAlertCondition#enabled}
        :param evaluation_delay: How long we wait until the signal starts evaluating. The maximum delay is 7200 seconds (120 minutes). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/nrql_alert_condition#evaluation_delay NrqlAlertCondition#evaluation_delay}
        :param expiration_duration: The amount of time (in seconds) to wait before considering the signal expired. Must be in the range of 30 to 172800 (inclusive) Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/nrql_alert_condition#expiration_duration NrqlAlertCondition#expiration_duration}
        :param fill_option: Which strategy to use when filling gaps in the signal. If static, the 'fill value' will be used for filling gaps in the signal. Valid values are: 'NONE', 'LAST_VALUE', or 'STATIC' (case insensitive). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/nrql_alert_condition#fill_option NrqlAlertCondition#fill_option}
        :param fill_value: If using the 'static' fill option, this value will be used for filling gaps in the signal. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/nrql_alert_condition#fill_value NrqlAlertCondition#fill_value}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/nrql_alert_condition#id NrqlAlertCondition#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param ignore_on_expected_termination: Whether to ignore expected termination of a signal when considering whether to create a loss of signal incident. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/nrql_alert_condition#ignore_on_expected_termination NrqlAlertCondition#ignore_on_expected_termination}
        :param open_violation_on_expiration: Whether to create a new incident to capture that the signal expired. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/nrql_alert_condition#open_violation_on_expiration NrqlAlertCondition#open_violation_on_expiration}
        :param runbook_url: Runbook URL to display in notifications. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/nrql_alert_condition#runbook_url NrqlAlertCondition#runbook_url}
        :param signal_seasonality: Seasonality under which a condition's signal(s) are evaluated. Valid values are: 'NEW_RELIC_CALCULATION', 'HOURLY', 'DAILY', 'WEEKLY', or 'NONE'. To have New Relic calculate seasonality automatically, set to 'NEW_RELIC_CALCULATION' (default). To turn off seasonality completely, set to 'NONE'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/nrql_alert_condition#signal_seasonality NrqlAlertCondition#signal_seasonality}
        :param slide_by: The duration of overlapping time windows used to smooth the chart line, in seconds. Must be a factor of ``aggregation_window`` and less than the aggregation window. If ``aggregation_window`` is less than or equal to 3600 seconds, it should be greater or equal to 30 seconds. If ``aggregation_window`` is greater than 3600 seconds but less than 7200 seconds, it should be greater or equal to ``aggregation_window / 120``. If ``aggregation_window`` is greater than 7200 seconds, it should be greater or equal to `aggregation_window / 24 Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/nrql_alert_condition#slide_by NrqlAlertCondition#slide_by}
        :param term: term block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/nrql_alert_condition#term NrqlAlertCondition#term}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/nrql_alert_condition#timeouts NrqlAlertCondition#timeouts}
        :param title_template: This field allows you to create a custom title to be used when incidents are opened by the condition. Setting this field will override the default title. Must be Handlebars format. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/nrql_alert_condition#title_template NrqlAlertCondition#title_template}
        :param type: The type of NRQL alert condition to create. Valid values are: 'static', 'baseline'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/nrql_alert_condition#type NrqlAlertCondition#type}
        :param violation_time_limit: Sets a time limit, in hours, that will automatically force-close a long-lasting incident after the time limit you select. Possible values are 'ONE_HOUR', 'TWO_HOURS', 'FOUR_HOURS', 'EIGHT_HOURS', 'TWELVE_HOURS', 'TWENTY_FOUR_HOURS', 'THIRTY_DAYS' (case insensitive). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/nrql_alert_condition#violation_time_limit NrqlAlertCondition#violation_time_limit}
        :param violation_time_limit_seconds: Sets a time limit, in seconds, that will automatically force-close a long-lasting incident after the time limit you select. Must be in the range of 300 to 2592000 (inclusive) Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/nrql_alert_condition#violation_time_limit_seconds NrqlAlertCondition#violation_time_limit_seconds}
        :param warning: warning block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/nrql_alert_condition#warning NrqlAlertCondition#warning}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(nrql, dict):
            nrql = NrqlAlertConditionNrql(**nrql)
        if isinstance(critical, dict):
            critical = NrqlAlertConditionCritical(**critical)
        if isinstance(timeouts, dict):
            timeouts = NrqlAlertConditionTimeouts(**timeouts)
        if isinstance(warning, dict):
            warning = NrqlAlertConditionWarning(**warning)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc0430dc9a3ee76d1557f1c8c9c13137528d867e7657bd1048c6d0fab99060f5)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument nrql", value=nrql, expected_type=type_hints["nrql"])
            check_type(argname="argument policy_id", value=policy_id, expected_type=type_hints["policy_id"])
            check_type(argname="argument account_id", value=account_id, expected_type=type_hints["account_id"])
            check_type(argname="argument aggregation_delay", value=aggregation_delay, expected_type=type_hints["aggregation_delay"])
            check_type(argname="argument aggregation_method", value=aggregation_method, expected_type=type_hints["aggregation_method"])
            check_type(argname="argument aggregation_timer", value=aggregation_timer, expected_type=type_hints["aggregation_timer"])
            check_type(argname="argument aggregation_window", value=aggregation_window, expected_type=type_hints["aggregation_window"])
            check_type(argname="argument baseline_direction", value=baseline_direction, expected_type=type_hints["baseline_direction"])
            check_type(argname="argument close_violations_on_expiration", value=close_violations_on_expiration, expected_type=type_hints["close_violations_on_expiration"])
            check_type(argname="argument critical", value=critical, expected_type=type_hints["critical"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument evaluation_delay", value=evaluation_delay, expected_type=type_hints["evaluation_delay"])
            check_type(argname="argument expiration_duration", value=expiration_duration, expected_type=type_hints["expiration_duration"])
            check_type(argname="argument fill_option", value=fill_option, expected_type=type_hints["fill_option"])
            check_type(argname="argument fill_value", value=fill_value, expected_type=type_hints["fill_value"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument ignore_on_expected_termination", value=ignore_on_expected_termination, expected_type=type_hints["ignore_on_expected_termination"])
            check_type(argname="argument open_violation_on_expiration", value=open_violation_on_expiration, expected_type=type_hints["open_violation_on_expiration"])
            check_type(argname="argument runbook_url", value=runbook_url, expected_type=type_hints["runbook_url"])
            check_type(argname="argument signal_seasonality", value=signal_seasonality, expected_type=type_hints["signal_seasonality"])
            check_type(argname="argument slide_by", value=slide_by, expected_type=type_hints["slide_by"])
            check_type(argname="argument term", value=term, expected_type=type_hints["term"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
            check_type(argname="argument title_template", value=title_template, expected_type=type_hints["title_template"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument violation_time_limit", value=violation_time_limit, expected_type=type_hints["violation_time_limit"])
            check_type(argname="argument violation_time_limit_seconds", value=violation_time_limit_seconds, expected_type=type_hints["violation_time_limit_seconds"])
            check_type(argname="argument warning", value=warning, expected_type=type_hints["warning"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "nrql": nrql,
            "policy_id": policy_id,
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
        if aggregation_delay is not None:
            self._values["aggregation_delay"] = aggregation_delay
        if aggregation_method is not None:
            self._values["aggregation_method"] = aggregation_method
        if aggregation_timer is not None:
            self._values["aggregation_timer"] = aggregation_timer
        if aggregation_window is not None:
            self._values["aggregation_window"] = aggregation_window
        if baseline_direction is not None:
            self._values["baseline_direction"] = baseline_direction
        if close_violations_on_expiration is not None:
            self._values["close_violations_on_expiration"] = close_violations_on_expiration
        if critical is not None:
            self._values["critical"] = critical
        if description is not None:
            self._values["description"] = description
        if enabled is not None:
            self._values["enabled"] = enabled
        if evaluation_delay is not None:
            self._values["evaluation_delay"] = evaluation_delay
        if expiration_duration is not None:
            self._values["expiration_duration"] = expiration_duration
        if fill_option is not None:
            self._values["fill_option"] = fill_option
        if fill_value is not None:
            self._values["fill_value"] = fill_value
        if id is not None:
            self._values["id"] = id
        if ignore_on_expected_termination is not None:
            self._values["ignore_on_expected_termination"] = ignore_on_expected_termination
        if open_violation_on_expiration is not None:
            self._values["open_violation_on_expiration"] = open_violation_on_expiration
        if runbook_url is not None:
            self._values["runbook_url"] = runbook_url
        if signal_seasonality is not None:
            self._values["signal_seasonality"] = signal_seasonality
        if slide_by is not None:
            self._values["slide_by"] = slide_by
        if term is not None:
            self._values["term"] = term
        if timeouts is not None:
            self._values["timeouts"] = timeouts
        if title_template is not None:
            self._values["title_template"] = title_template
        if type is not None:
            self._values["type"] = type
        if violation_time_limit is not None:
            self._values["violation_time_limit"] = violation_time_limit
        if violation_time_limit_seconds is not None:
            self._values["violation_time_limit_seconds"] = violation_time_limit_seconds
        if warning is not None:
            self._values["warning"] = warning

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
    def name(self) -> builtins.str:
        '''The title of the condition.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/nrql_alert_condition#name NrqlAlertCondition#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def nrql(self) -> "NrqlAlertConditionNrql":
        '''nrql block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/nrql_alert_condition#nrql NrqlAlertCondition#nrql}
        '''
        result = self._values.get("nrql")
        assert result is not None, "Required property 'nrql' is missing"
        return typing.cast("NrqlAlertConditionNrql", result)

    @builtins.property
    def policy_id(self) -> jsii.Number:
        '''The ID of the policy where this condition should be used.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/nrql_alert_condition#policy_id NrqlAlertCondition#policy_id}
        '''
        result = self._values.get("policy_id")
        assert result is not None, "Required property 'policy_id' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def account_id(self) -> typing.Optional[jsii.Number]:
        '''The New Relic account ID for managing your NRQL alert conditions.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/nrql_alert_condition#account_id NrqlAlertCondition#account_id}
        '''
        result = self._values.get("account_id")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def aggregation_delay(self) -> typing.Optional[builtins.str]:
        '''How long we wait for data that belongs in each aggregation window.

        Depending on your data, a longer delay may increase accuracy but delay notifications. Use aggregationDelay with the EVENT_FLOW and CADENCE aggregation methods.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/nrql_alert_condition#aggregation_delay NrqlAlertCondition#aggregation_delay}
        '''
        result = self._values.get("aggregation_delay")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def aggregation_method(self) -> typing.Optional[builtins.str]:
        '''The method that determines when we consider an aggregation window to be complete so that we can evaluate the signal for incidents.

        Default is EVENT_FLOW.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/nrql_alert_condition#aggregation_method NrqlAlertCondition#aggregation_method}
        '''
        result = self._values.get("aggregation_method")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def aggregation_timer(self) -> typing.Optional[builtins.str]:
        '''How long we wait after each data point arrives to make sure we've processed the whole batch.

        Use aggregationTimer with the EVENT_TIMER aggregation method.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/nrql_alert_condition#aggregation_timer NrqlAlertCondition#aggregation_timer}
        '''
        result = self._values.get("aggregation_timer")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def aggregation_window(self) -> typing.Optional[jsii.Number]:
        '''The duration of the time window used to evaluate the NRQL query, in seconds.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/nrql_alert_condition#aggregation_window NrqlAlertCondition#aggregation_window}
        '''
        result = self._values.get("aggregation_window")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def baseline_direction(self) -> typing.Optional[builtins.str]:
        '''The baseline direction of a baseline NRQL alert condition. Valid values are: 'LOWER_ONLY', 'UPPER_AND_LOWER', 'UPPER_ONLY' (case insensitive).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/nrql_alert_condition#baseline_direction NrqlAlertCondition#baseline_direction}
        '''
        result = self._values.get("baseline_direction")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def close_violations_on_expiration(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether to close all open incidents when the signal expires.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/nrql_alert_condition#close_violations_on_expiration NrqlAlertCondition#close_violations_on_expiration}
        '''
        result = self._values.get("close_violations_on_expiration")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def critical(self) -> typing.Optional["NrqlAlertConditionCritical"]:
        '''critical block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/nrql_alert_condition#critical NrqlAlertCondition#critical}
        '''
        result = self._values.get("critical")
        return typing.cast(typing.Optional["NrqlAlertConditionCritical"], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the NRQL alert condition.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/nrql_alert_condition#description NrqlAlertCondition#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether or not to enable the alert condition.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/nrql_alert_condition#enabled NrqlAlertCondition#enabled}
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def evaluation_delay(self) -> typing.Optional[jsii.Number]:
        '''How long we wait until the signal starts evaluating. The maximum delay is 7200 seconds (120 minutes).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/nrql_alert_condition#evaluation_delay NrqlAlertCondition#evaluation_delay}
        '''
        result = self._values.get("evaluation_delay")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def expiration_duration(self) -> typing.Optional[jsii.Number]:
        '''The amount of time (in seconds) to wait before considering the signal expired.

        Must be in the range of 30 to 172800 (inclusive)

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/nrql_alert_condition#expiration_duration NrqlAlertCondition#expiration_duration}
        '''
        result = self._values.get("expiration_duration")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def fill_option(self) -> typing.Optional[builtins.str]:
        '''Which strategy to use when filling gaps in the signal.

        If static, the 'fill value' will be used for filling gaps in the signal. Valid values are: 'NONE', 'LAST_VALUE', or 'STATIC' (case insensitive).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/nrql_alert_condition#fill_option NrqlAlertCondition#fill_option}
        '''
        result = self._values.get("fill_option")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def fill_value(self) -> typing.Optional[jsii.Number]:
        '''If using the 'static' fill option, this value will be used for filling gaps in the signal.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/nrql_alert_condition#fill_value NrqlAlertCondition#fill_value}
        '''
        result = self._values.get("fill_value")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/nrql_alert_condition#id NrqlAlertCondition#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ignore_on_expected_termination(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether to ignore expected termination of a signal when considering whether to create a loss of signal incident.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/nrql_alert_condition#ignore_on_expected_termination NrqlAlertCondition#ignore_on_expected_termination}
        '''
        result = self._values.get("ignore_on_expected_termination")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def open_violation_on_expiration(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether to create a new incident to capture that the signal expired.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/nrql_alert_condition#open_violation_on_expiration NrqlAlertCondition#open_violation_on_expiration}
        '''
        result = self._values.get("open_violation_on_expiration")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def runbook_url(self) -> typing.Optional[builtins.str]:
        '''Runbook URL to display in notifications.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/nrql_alert_condition#runbook_url NrqlAlertCondition#runbook_url}
        '''
        result = self._values.get("runbook_url")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def signal_seasonality(self) -> typing.Optional[builtins.str]:
        '''Seasonality under which a condition's signal(s) are evaluated.

        Valid values are: 'NEW_RELIC_CALCULATION', 'HOURLY', 'DAILY', 'WEEKLY', or 'NONE'. To have New Relic calculate seasonality automatically, set to 'NEW_RELIC_CALCULATION' (default). To turn off seasonality completely, set to 'NONE'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/nrql_alert_condition#signal_seasonality NrqlAlertCondition#signal_seasonality}
        '''
        result = self._values.get("signal_seasonality")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def slide_by(self) -> typing.Optional[jsii.Number]:
        '''The duration of overlapping time windows used to smooth the chart line, in seconds.

        Must be a factor of ``aggregation_window`` and less than the aggregation window. If ``aggregation_window`` is less than or equal to 3600 seconds, it should be greater or equal to 30 seconds. If ``aggregation_window`` is greater than 3600 seconds but less than 7200 seconds, it should be greater or equal to ``aggregation_window / 120``.  If ``aggregation_window`` is greater than 7200 seconds, it should be greater or equal to `aggregation_window / 24

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/nrql_alert_condition#slide_by NrqlAlertCondition#slide_by}
        '''
        result = self._values.get("slide_by")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def term(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NrqlAlertConditionTerm"]]]:
        '''term block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/nrql_alert_condition#term NrqlAlertCondition#term}
        '''
        result = self._values.get("term")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NrqlAlertConditionTerm"]]], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["NrqlAlertConditionTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/nrql_alert_condition#timeouts NrqlAlertCondition#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["NrqlAlertConditionTimeouts"], result)

    @builtins.property
    def title_template(self) -> typing.Optional[builtins.str]:
        '''This field allows you to create a custom title to be used when incidents are opened by the condition.

        Setting this field will override the default title. Must be Handlebars format.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/nrql_alert_condition#title_template NrqlAlertCondition#title_template}
        '''
        result = self._values.get("title_template")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''The type of NRQL alert condition to create. Valid values are: 'static', 'baseline'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/nrql_alert_condition#type NrqlAlertCondition#type}
        '''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def violation_time_limit(self) -> typing.Optional[builtins.str]:
        '''Sets a time limit, in hours, that will automatically force-close a long-lasting incident after the time limit you select.

        Possible values are 'ONE_HOUR', 'TWO_HOURS', 'FOUR_HOURS', 'EIGHT_HOURS', 'TWELVE_HOURS', 'TWENTY_FOUR_HOURS', 'THIRTY_DAYS' (case insensitive).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/nrql_alert_condition#violation_time_limit NrqlAlertCondition#violation_time_limit}
        '''
        result = self._values.get("violation_time_limit")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def violation_time_limit_seconds(self) -> typing.Optional[jsii.Number]:
        '''Sets a time limit, in seconds, that will automatically force-close a long-lasting incident after the time limit you select.

        Must be in the range of 300 to 2592000 (inclusive)

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/nrql_alert_condition#violation_time_limit_seconds NrqlAlertCondition#violation_time_limit_seconds}
        '''
        result = self._values.get("violation_time_limit_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def warning(self) -> typing.Optional["NrqlAlertConditionWarning"]:
        '''warning block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/nrql_alert_condition#warning NrqlAlertCondition#warning}
        '''
        result = self._values.get("warning")
        return typing.cast(typing.Optional["NrqlAlertConditionWarning"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NrqlAlertConditionConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-newrelic.nrqlAlertCondition.NrqlAlertConditionCritical",
    jsii_struct_bases=[],
    name_mapping={
        "threshold": "threshold",
        "disable_health_status_reporting": "disableHealthStatusReporting",
        "duration": "duration",
        "operator": "operator",
        "prediction": "prediction",
        "threshold_duration": "thresholdDuration",
        "threshold_occurrences": "thresholdOccurrences",
        "time_function": "timeFunction",
    },
)
class NrqlAlertConditionCritical:
    def __init__(
        self,
        *,
        threshold: jsii.Number,
        disable_health_status_reporting: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        duration: typing.Optional[jsii.Number] = None,
        operator: typing.Optional[builtins.str] = None,
        prediction: typing.Optional[typing.Union["NrqlAlertConditionCriticalPrediction", typing.Dict[builtins.str, typing.Any]]] = None,
        threshold_duration: typing.Optional[jsii.Number] = None,
        threshold_occurrences: typing.Optional[builtins.str] = None,
        time_function: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param threshold: For baseline conditions must be in range [1, 1000]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/nrql_alert_condition#threshold NrqlAlertCondition#threshold}
        :param disable_health_status_reporting: Violations will not change system health status for this term. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/nrql_alert_condition#disable_health_status_reporting NrqlAlertCondition#disable_health_status_reporting}
        :param duration: In minutes, must be in the range of 1 to 120 (inclusive). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/nrql_alert_condition#duration NrqlAlertCondition#duration}
        :param operator: One of (above, above_or_equals, below, below_or_equals, equals, not_equals). Defaults to 'equals'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/nrql_alert_condition#operator NrqlAlertCondition#operator}
        :param prediction: prediction block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/nrql_alert_condition#prediction NrqlAlertCondition#prediction}
        :param threshold_duration: The duration, in seconds, that the threshold must violate in order to create an incident. Value must be a multiple of the 'aggregation_window' (which has a default of 60 seconds). Value must be within 120-86400 seconds for baseline conditions, and within 60-86400 seconds for static conditions Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/nrql_alert_condition#threshold_duration NrqlAlertCondition#threshold_duration}
        :param threshold_occurrences: The criteria for how many data points must be in violation for the specified threshold duration. Valid values are: 'ALL' or 'AT_LEAST_ONCE' (case insensitive). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/nrql_alert_condition#threshold_occurrences NrqlAlertCondition#threshold_occurrences}
        :param time_function: Valid values are: 'all' or 'any'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/nrql_alert_condition#time_function NrqlAlertCondition#time_function}
        '''
        if isinstance(prediction, dict):
            prediction = NrqlAlertConditionCriticalPrediction(**prediction)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9cc7d6cd689719ee6613918d93752c1b1df2a84ebf4cb678d6c69aad3c55e36d)
            check_type(argname="argument threshold", value=threshold, expected_type=type_hints["threshold"])
            check_type(argname="argument disable_health_status_reporting", value=disable_health_status_reporting, expected_type=type_hints["disable_health_status_reporting"])
            check_type(argname="argument duration", value=duration, expected_type=type_hints["duration"])
            check_type(argname="argument operator", value=operator, expected_type=type_hints["operator"])
            check_type(argname="argument prediction", value=prediction, expected_type=type_hints["prediction"])
            check_type(argname="argument threshold_duration", value=threshold_duration, expected_type=type_hints["threshold_duration"])
            check_type(argname="argument threshold_occurrences", value=threshold_occurrences, expected_type=type_hints["threshold_occurrences"])
            check_type(argname="argument time_function", value=time_function, expected_type=type_hints["time_function"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "threshold": threshold,
        }
        if disable_health_status_reporting is not None:
            self._values["disable_health_status_reporting"] = disable_health_status_reporting
        if duration is not None:
            self._values["duration"] = duration
        if operator is not None:
            self._values["operator"] = operator
        if prediction is not None:
            self._values["prediction"] = prediction
        if threshold_duration is not None:
            self._values["threshold_duration"] = threshold_duration
        if threshold_occurrences is not None:
            self._values["threshold_occurrences"] = threshold_occurrences
        if time_function is not None:
            self._values["time_function"] = time_function

    @builtins.property
    def threshold(self) -> jsii.Number:
        '''For baseline conditions must be in range [1, 1000].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/nrql_alert_condition#threshold NrqlAlertCondition#threshold}
        '''
        result = self._values.get("threshold")
        assert result is not None, "Required property 'threshold' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def disable_health_status_reporting(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Violations will not change system health status for this term.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/nrql_alert_condition#disable_health_status_reporting NrqlAlertCondition#disable_health_status_reporting}
        '''
        result = self._values.get("disable_health_status_reporting")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def duration(self) -> typing.Optional[jsii.Number]:
        '''In minutes, must be in the range of 1 to 120 (inclusive).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/nrql_alert_condition#duration NrqlAlertCondition#duration}
        '''
        result = self._values.get("duration")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def operator(self) -> typing.Optional[builtins.str]:
        '''One of (above, above_or_equals, below, below_or_equals, equals, not_equals). Defaults to 'equals'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/nrql_alert_condition#operator NrqlAlertCondition#operator}
        '''
        result = self._values.get("operator")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def prediction(self) -> typing.Optional["NrqlAlertConditionCriticalPrediction"]:
        '''prediction block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/nrql_alert_condition#prediction NrqlAlertCondition#prediction}
        '''
        result = self._values.get("prediction")
        return typing.cast(typing.Optional["NrqlAlertConditionCriticalPrediction"], result)

    @builtins.property
    def threshold_duration(self) -> typing.Optional[jsii.Number]:
        '''The duration, in seconds, that the threshold must violate in order to create an incident.

        Value must be a multiple of the 'aggregation_window' (which has a default of 60 seconds). Value must be within 120-86400 seconds for baseline conditions, and within 60-86400 seconds for static conditions

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/nrql_alert_condition#threshold_duration NrqlAlertCondition#threshold_duration}
        '''
        result = self._values.get("threshold_duration")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def threshold_occurrences(self) -> typing.Optional[builtins.str]:
        '''The criteria for how many data points must be in violation for the specified threshold duration.

        Valid values are: 'ALL' or 'AT_LEAST_ONCE' (case insensitive).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/nrql_alert_condition#threshold_occurrences NrqlAlertCondition#threshold_occurrences}
        '''
        result = self._values.get("threshold_occurrences")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def time_function(self) -> typing.Optional[builtins.str]:
        '''Valid values are: 'all' or 'any'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/nrql_alert_condition#time_function NrqlAlertCondition#time_function}
        '''
        result = self._values.get("time_function")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NrqlAlertConditionCritical(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NrqlAlertConditionCriticalOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.nrqlAlertCondition.NrqlAlertConditionCriticalOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fe7a5abac695cf60326226f1d06d767876623700784e01dd6fcc777627da5745)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putPrediction")
    def put_prediction(
        self,
        *,
        predict_by: typing.Optional[jsii.Number] = None,
        prefer_prediction_violation: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param predict_by: BETA PREVIEW: the ``predict_by`` field is in limited release and only enabled for preview on a per-account basis. - The duration, in seconds, that the prediction should look into the future. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/nrql_alert_condition#predict_by NrqlAlertCondition#predict_by}
        :param prefer_prediction_violation: BETA PREVIEW: the ``prefer_prediction_violation`` field is in limited release and only enabled for preview on a per-account basis. - If a prediction incident is open when a term's static threshold is breached by the actual signal, default behavior is to close the prediction incident and open a static incident. Setting ``prefer_prediction_violation`` to ``true`` overrides this behavior leaving the prediction incident open and preventing a static incident from opening. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/nrql_alert_condition#prefer_prediction_violation NrqlAlertCondition#prefer_prediction_violation}
        '''
        value = NrqlAlertConditionCriticalPrediction(
            predict_by=predict_by,
            prefer_prediction_violation=prefer_prediction_violation,
        )

        return typing.cast(None, jsii.invoke(self, "putPrediction", [value]))

    @jsii.member(jsii_name="resetDisableHealthStatusReporting")
    def reset_disable_health_status_reporting(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDisableHealthStatusReporting", []))

    @jsii.member(jsii_name="resetDuration")
    def reset_duration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDuration", []))

    @jsii.member(jsii_name="resetOperator")
    def reset_operator(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOperator", []))

    @jsii.member(jsii_name="resetPrediction")
    def reset_prediction(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPrediction", []))

    @jsii.member(jsii_name="resetThresholdDuration")
    def reset_threshold_duration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetThresholdDuration", []))

    @jsii.member(jsii_name="resetThresholdOccurrences")
    def reset_threshold_occurrences(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetThresholdOccurrences", []))

    @jsii.member(jsii_name="resetTimeFunction")
    def reset_time_function(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeFunction", []))

    @builtins.property
    @jsii.member(jsii_name="prediction")
    def prediction(self) -> "NrqlAlertConditionCriticalPredictionOutputReference":
        return typing.cast("NrqlAlertConditionCriticalPredictionOutputReference", jsii.get(self, "prediction"))

    @builtins.property
    @jsii.member(jsii_name="disableHealthStatusReportingInput")
    def disable_health_status_reporting_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "disableHealthStatusReportingInput"))

    @builtins.property
    @jsii.member(jsii_name="durationInput")
    def duration_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "durationInput"))

    @builtins.property
    @jsii.member(jsii_name="operatorInput")
    def operator_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "operatorInput"))

    @builtins.property
    @jsii.member(jsii_name="predictionInput")
    def prediction_input(
        self,
    ) -> typing.Optional["NrqlAlertConditionCriticalPrediction"]:
        return typing.cast(typing.Optional["NrqlAlertConditionCriticalPrediction"], jsii.get(self, "predictionInput"))

    @builtins.property
    @jsii.member(jsii_name="thresholdDurationInput")
    def threshold_duration_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "thresholdDurationInput"))

    @builtins.property
    @jsii.member(jsii_name="thresholdInput")
    def threshold_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "thresholdInput"))

    @builtins.property
    @jsii.member(jsii_name="thresholdOccurrencesInput")
    def threshold_occurrences_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "thresholdOccurrencesInput"))

    @builtins.property
    @jsii.member(jsii_name="timeFunctionInput")
    def time_function_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "timeFunctionInput"))

    @builtins.property
    @jsii.member(jsii_name="disableHealthStatusReporting")
    def disable_health_status_reporting(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "disableHealthStatusReporting"))

    @disable_health_status_reporting.setter
    def disable_health_status_reporting(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ab98be15f1b90d6daf004e1ebc5c7e27cfdad1e66262f18943e3624eb58f896a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "disableHealthStatusReporting", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="duration")
    def duration(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "duration"))

    @duration.setter
    def duration(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__544bb90e3fb8f478ac9b4a18241c77a415497b7c485bc8731cb2448641ff5461)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "duration", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="operator")
    def operator(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "operator"))

    @operator.setter
    def operator(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__499aaafc5ad66d0316461ee703bbe2c6ef67e7423684b4334a3a8a015a1918c6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "operator", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="threshold")
    def threshold(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "threshold"))

    @threshold.setter
    def threshold(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa2471d7eff28412af98e903bd026131c7d026baf9e867c15074cc3fcc54e242)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "threshold", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="thresholdDuration")
    def threshold_duration(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "thresholdDuration"))

    @threshold_duration.setter
    def threshold_duration(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e7401fb6d9b681b5ae68cdae9f5927a2d3a40df0df5bbb0a04929e93feaf7957)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "thresholdDuration", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="thresholdOccurrences")
    def threshold_occurrences(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "thresholdOccurrences"))

    @threshold_occurrences.setter
    def threshold_occurrences(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__56cbb1a7cec39889560b92cdbd37369e3dd059ce135fe15d38185e14e46d67ce)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "thresholdOccurrences", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="timeFunction")
    def time_function(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "timeFunction"))

    @time_function.setter
    def time_function(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e8de95945dbccb17cd1e5a21f92b99f5645dea3130215d51515b5fa449ae6f03)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timeFunction", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[NrqlAlertConditionCritical]:
        return typing.cast(typing.Optional[NrqlAlertConditionCritical], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[NrqlAlertConditionCritical],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__523d0bbe6deb8a0a6bafbe28b69cf691774de8a93d6700a9ccbaf055e0846311)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-newrelic.nrqlAlertCondition.NrqlAlertConditionCriticalPrediction",
    jsii_struct_bases=[],
    name_mapping={
        "predict_by": "predictBy",
        "prefer_prediction_violation": "preferPredictionViolation",
    },
)
class NrqlAlertConditionCriticalPrediction:
    def __init__(
        self,
        *,
        predict_by: typing.Optional[jsii.Number] = None,
        prefer_prediction_violation: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param predict_by: BETA PREVIEW: the ``predict_by`` field is in limited release and only enabled for preview on a per-account basis. - The duration, in seconds, that the prediction should look into the future. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/nrql_alert_condition#predict_by NrqlAlertCondition#predict_by}
        :param prefer_prediction_violation: BETA PREVIEW: the ``prefer_prediction_violation`` field is in limited release and only enabled for preview on a per-account basis. - If a prediction incident is open when a term's static threshold is breached by the actual signal, default behavior is to close the prediction incident and open a static incident. Setting ``prefer_prediction_violation`` to ``true`` overrides this behavior leaving the prediction incident open and preventing a static incident from opening. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/nrql_alert_condition#prefer_prediction_violation NrqlAlertCondition#prefer_prediction_violation}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f016c68996fe74893413497c1cd7939a04ea54e41746ce3a67c2d7859eaa893d)
            check_type(argname="argument predict_by", value=predict_by, expected_type=type_hints["predict_by"])
            check_type(argname="argument prefer_prediction_violation", value=prefer_prediction_violation, expected_type=type_hints["prefer_prediction_violation"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if predict_by is not None:
            self._values["predict_by"] = predict_by
        if prefer_prediction_violation is not None:
            self._values["prefer_prediction_violation"] = prefer_prediction_violation

    @builtins.property
    def predict_by(self) -> typing.Optional[jsii.Number]:
        '''BETA PREVIEW: the ``predict_by`` field is in limited release and only enabled for preview on a per-account basis.

        - The duration, in seconds, that the prediction should look into the future.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/nrql_alert_condition#predict_by NrqlAlertCondition#predict_by}
        '''
        result = self._values.get("predict_by")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def prefer_prediction_violation(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''BETA PREVIEW: the ``prefer_prediction_violation`` field is in limited release and only enabled for preview on a per-account basis.

        - If a prediction incident is open when a term's static threshold is breached by the actual signal, default behavior is to close the prediction incident and open a static incident. Setting ``prefer_prediction_violation`` to ``true`` overrides this behavior leaving the prediction incident open and preventing a static incident from opening.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/nrql_alert_condition#prefer_prediction_violation NrqlAlertCondition#prefer_prediction_violation}
        '''
        result = self._values.get("prefer_prediction_violation")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NrqlAlertConditionCriticalPrediction(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NrqlAlertConditionCriticalPredictionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.nrqlAlertCondition.NrqlAlertConditionCriticalPredictionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bdf68c1b87aefa5f4395870c494cd64aebdf5c6ed9a1d153b81d66ddd42feb47)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetPredictBy")
    def reset_predict_by(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPredictBy", []))

    @jsii.member(jsii_name="resetPreferPredictionViolation")
    def reset_prefer_prediction_violation(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPreferPredictionViolation", []))

    @builtins.property
    @jsii.member(jsii_name="predictByInput")
    def predict_by_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "predictByInput"))

    @builtins.property
    @jsii.member(jsii_name="preferPredictionViolationInput")
    def prefer_prediction_violation_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "preferPredictionViolationInput"))

    @builtins.property
    @jsii.member(jsii_name="predictBy")
    def predict_by(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "predictBy"))

    @predict_by.setter
    def predict_by(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f53c5995050e2f1ecf1aa6a532c4b2884e7cc5aef394de8c6703021a1c7cc04e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "predictBy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="preferPredictionViolation")
    def prefer_prediction_violation(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "preferPredictionViolation"))

    @prefer_prediction_violation.setter
    def prefer_prediction_violation(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b85df81d38451feb236c8cfb426a1837d48430d331e527143c5ef43adb54747)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "preferPredictionViolation", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[NrqlAlertConditionCriticalPrediction]:
        return typing.cast(typing.Optional[NrqlAlertConditionCriticalPrediction], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[NrqlAlertConditionCriticalPrediction],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c50c3f66dd42b50785626177b42e53847249be00cf79cfd3ee4ff82300828187)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-newrelic.nrqlAlertCondition.NrqlAlertConditionNrql",
    jsii_struct_bases=[],
    name_mapping={
        "query": "query",
        "data_account_id": "dataAccountId",
        "evaluation_offset": "evaluationOffset",
        "since_value": "sinceValue",
    },
)
class NrqlAlertConditionNrql:
    def __init__(
        self,
        *,
        query: builtins.str,
        data_account_id: typing.Optional[jsii.Number] = None,
        evaluation_offset: typing.Optional[jsii.Number] = None,
        since_value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param query: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/nrql_alert_condition#query NrqlAlertCondition#query}.
        :param data_account_id: The New Relic account ID to use as the basis for the NRQL alert condition's ``query``; will default to ``account_id`` if unspecified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/nrql_alert_condition#data_account_id NrqlAlertCondition#data_account_id}
        :param evaluation_offset: NRQL queries are evaluated in one-minute time windows. The start time depends on the value you provide in the NRQL condition's ``evaluation_offset``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/nrql_alert_condition#evaluation_offset NrqlAlertCondition#evaluation_offset}
        :param since_value: NRQL queries are evaluated in one-minute time windows. The start time depends on the value you provide in the NRQL condition's ``since_value``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/nrql_alert_condition#since_value NrqlAlertCondition#since_value}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9c62249076f8a1e95787e0bdf5c0c59b2f6e89562e4dfc241b121925caa3708d)
            check_type(argname="argument query", value=query, expected_type=type_hints["query"])
            check_type(argname="argument data_account_id", value=data_account_id, expected_type=type_hints["data_account_id"])
            check_type(argname="argument evaluation_offset", value=evaluation_offset, expected_type=type_hints["evaluation_offset"])
            check_type(argname="argument since_value", value=since_value, expected_type=type_hints["since_value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "query": query,
        }
        if data_account_id is not None:
            self._values["data_account_id"] = data_account_id
        if evaluation_offset is not None:
            self._values["evaluation_offset"] = evaluation_offset
        if since_value is not None:
            self._values["since_value"] = since_value

    @builtins.property
    def query(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/nrql_alert_condition#query NrqlAlertCondition#query}.'''
        result = self._values.get("query")
        assert result is not None, "Required property 'query' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def data_account_id(self) -> typing.Optional[jsii.Number]:
        '''The New Relic account ID to use as the basis for the NRQL alert condition's ``query``;

        will default to ``account_id`` if unspecified.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/nrql_alert_condition#data_account_id NrqlAlertCondition#data_account_id}
        '''
        result = self._values.get("data_account_id")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def evaluation_offset(self) -> typing.Optional[jsii.Number]:
        '''NRQL queries are evaluated in one-minute time windows.

        The start time depends on the value you provide in the NRQL condition's ``evaluation_offset``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/nrql_alert_condition#evaluation_offset NrqlAlertCondition#evaluation_offset}
        '''
        result = self._values.get("evaluation_offset")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def since_value(self) -> typing.Optional[builtins.str]:
        '''NRQL queries are evaluated in one-minute time windows.

        The start time depends on the value you provide in the NRQL condition's ``since_value``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/nrql_alert_condition#since_value NrqlAlertCondition#since_value}
        '''
        result = self._values.get("since_value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NrqlAlertConditionNrql(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NrqlAlertConditionNrqlOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.nrqlAlertCondition.NrqlAlertConditionNrqlOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__61b56ec5c882142ee82c70c1be58ba6ed1a3b7ea49b7f86799ab01357e328cb2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetDataAccountId")
    def reset_data_account_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDataAccountId", []))

    @jsii.member(jsii_name="resetEvaluationOffset")
    def reset_evaluation_offset(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEvaluationOffset", []))

    @jsii.member(jsii_name="resetSinceValue")
    def reset_since_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSinceValue", []))

    @builtins.property
    @jsii.member(jsii_name="dataAccountIdInput")
    def data_account_id_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "dataAccountIdInput"))

    @builtins.property
    @jsii.member(jsii_name="evaluationOffsetInput")
    def evaluation_offset_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "evaluationOffsetInput"))

    @builtins.property
    @jsii.member(jsii_name="queryInput")
    def query_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "queryInput"))

    @builtins.property
    @jsii.member(jsii_name="sinceValueInput")
    def since_value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sinceValueInput"))

    @builtins.property
    @jsii.member(jsii_name="dataAccountId")
    def data_account_id(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "dataAccountId"))

    @data_account_id.setter
    def data_account_id(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa732f6321cb5b98380e37224e8433ac5b46cf972b92646c99383de78f08e67c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dataAccountId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="evaluationOffset")
    def evaluation_offset(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "evaluationOffset"))

    @evaluation_offset.setter
    def evaluation_offset(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd8c7c3b76ac2f43e775b8e8d83482ad19b5cf4fe169e54a1189696dfc4792e2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "evaluationOffset", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="query")
    def query(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "query"))

    @query.setter
    def query(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__58a623927db6ec8c356f7cf0ac9ae87a5c0456f1aea2b27b539a25b314c88eaf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "query", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sinceValue")
    def since_value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sinceValue"))

    @since_value.setter
    def since_value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5fe27c9b02aab9609180ef17c7f8079f66daba17886da427b7367ab94132747d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sinceValue", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[NrqlAlertConditionNrql]:
        return typing.cast(typing.Optional[NrqlAlertConditionNrql], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[NrqlAlertConditionNrql]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__78b60e0cbb22b6a787c5884dd47d99c013a34c17031205979d4ba8146ac0b951)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-newrelic.nrqlAlertCondition.NrqlAlertConditionTerm",
    jsii_struct_bases=[],
    name_mapping={
        "threshold": "threshold",
        "disable_health_status_reporting": "disableHealthStatusReporting",
        "duration": "duration",
        "operator": "operator",
        "prediction": "prediction",
        "priority": "priority",
        "threshold_duration": "thresholdDuration",
        "threshold_occurrences": "thresholdOccurrences",
        "time_function": "timeFunction",
    },
)
class NrqlAlertConditionTerm:
    def __init__(
        self,
        *,
        threshold: jsii.Number,
        disable_health_status_reporting: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        duration: typing.Optional[jsii.Number] = None,
        operator: typing.Optional[builtins.str] = None,
        prediction: typing.Optional[typing.Union["NrqlAlertConditionTermPrediction", typing.Dict[builtins.str, typing.Any]]] = None,
        priority: typing.Optional[builtins.str] = None,
        threshold_duration: typing.Optional[jsii.Number] = None,
        threshold_occurrences: typing.Optional[builtins.str] = None,
        time_function: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param threshold: For baseline conditions must be in range [1, 1000]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/nrql_alert_condition#threshold NrqlAlertCondition#threshold}
        :param disable_health_status_reporting: Violations will not change system health status for this term. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/nrql_alert_condition#disable_health_status_reporting NrqlAlertCondition#disable_health_status_reporting}
        :param duration: In minutes, must be in the range of 1 to 120 (inclusive). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/nrql_alert_condition#duration NrqlAlertCondition#duration}
        :param operator: One of (above, above_or_equals, below, below_or_equals, equals, not_equals). Defaults to 'equals'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/nrql_alert_condition#operator NrqlAlertCondition#operator}
        :param prediction: prediction block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/nrql_alert_condition#prediction NrqlAlertCondition#prediction}
        :param priority: One of (critical, warning). Defaults to 'critical'. At least one condition term must have priority set to 'critical'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/nrql_alert_condition#priority NrqlAlertCondition#priority}
        :param threshold_duration: The duration, in seconds, that the threshold must violate in order to create an incident. Value must be a multiple of the 'aggregation_window' (which has a default of 60 seconds). Value must be within 120-86400 seconds for baseline conditions, and within 60-86400 seconds for static conditions Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/nrql_alert_condition#threshold_duration NrqlAlertCondition#threshold_duration}
        :param threshold_occurrences: The criteria for how many data points must be in violation for the specified threshold duration. Valid values are: 'ALL' or 'AT_LEAST_ONCE' (case insensitive). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/nrql_alert_condition#threshold_occurrences NrqlAlertCondition#threshold_occurrences}
        :param time_function: Valid values are: 'all' or 'any'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/nrql_alert_condition#time_function NrqlAlertCondition#time_function}
        '''
        if isinstance(prediction, dict):
            prediction = NrqlAlertConditionTermPrediction(**prediction)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__472601cc201d7341e0bb9b95ae234ecf5726c2f0aaf9c8341255ddcd44f88883)
            check_type(argname="argument threshold", value=threshold, expected_type=type_hints["threshold"])
            check_type(argname="argument disable_health_status_reporting", value=disable_health_status_reporting, expected_type=type_hints["disable_health_status_reporting"])
            check_type(argname="argument duration", value=duration, expected_type=type_hints["duration"])
            check_type(argname="argument operator", value=operator, expected_type=type_hints["operator"])
            check_type(argname="argument prediction", value=prediction, expected_type=type_hints["prediction"])
            check_type(argname="argument priority", value=priority, expected_type=type_hints["priority"])
            check_type(argname="argument threshold_duration", value=threshold_duration, expected_type=type_hints["threshold_duration"])
            check_type(argname="argument threshold_occurrences", value=threshold_occurrences, expected_type=type_hints["threshold_occurrences"])
            check_type(argname="argument time_function", value=time_function, expected_type=type_hints["time_function"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "threshold": threshold,
        }
        if disable_health_status_reporting is not None:
            self._values["disable_health_status_reporting"] = disable_health_status_reporting
        if duration is not None:
            self._values["duration"] = duration
        if operator is not None:
            self._values["operator"] = operator
        if prediction is not None:
            self._values["prediction"] = prediction
        if priority is not None:
            self._values["priority"] = priority
        if threshold_duration is not None:
            self._values["threshold_duration"] = threshold_duration
        if threshold_occurrences is not None:
            self._values["threshold_occurrences"] = threshold_occurrences
        if time_function is not None:
            self._values["time_function"] = time_function

    @builtins.property
    def threshold(self) -> jsii.Number:
        '''For baseline conditions must be in range [1, 1000].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/nrql_alert_condition#threshold NrqlAlertCondition#threshold}
        '''
        result = self._values.get("threshold")
        assert result is not None, "Required property 'threshold' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def disable_health_status_reporting(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Violations will not change system health status for this term.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/nrql_alert_condition#disable_health_status_reporting NrqlAlertCondition#disable_health_status_reporting}
        '''
        result = self._values.get("disable_health_status_reporting")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def duration(self) -> typing.Optional[jsii.Number]:
        '''In minutes, must be in the range of 1 to 120 (inclusive).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/nrql_alert_condition#duration NrqlAlertCondition#duration}
        '''
        result = self._values.get("duration")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def operator(self) -> typing.Optional[builtins.str]:
        '''One of (above, above_or_equals, below, below_or_equals, equals, not_equals). Defaults to 'equals'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/nrql_alert_condition#operator NrqlAlertCondition#operator}
        '''
        result = self._values.get("operator")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def prediction(self) -> typing.Optional["NrqlAlertConditionTermPrediction"]:
        '''prediction block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/nrql_alert_condition#prediction NrqlAlertCondition#prediction}
        '''
        result = self._values.get("prediction")
        return typing.cast(typing.Optional["NrqlAlertConditionTermPrediction"], result)

    @builtins.property
    def priority(self) -> typing.Optional[builtins.str]:
        '''One of (critical, warning). Defaults to 'critical'. At least one condition term must have priority set to 'critical'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/nrql_alert_condition#priority NrqlAlertCondition#priority}
        '''
        result = self._values.get("priority")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def threshold_duration(self) -> typing.Optional[jsii.Number]:
        '''The duration, in seconds, that the threshold must violate in order to create an incident.

        Value must be a multiple of the 'aggregation_window' (which has a default of 60 seconds). Value must be within 120-86400 seconds for baseline conditions, and within 60-86400 seconds for static conditions

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/nrql_alert_condition#threshold_duration NrqlAlertCondition#threshold_duration}
        '''
        result = self._values.get("threshold_duration")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def threshold_occurrences(self) -> typing.Optional[builtins.str]:
        '''The criteria for how many data points must be in violation for the specified threshold duration.

        Valid values are: 'ALL' or 'AT_LEAST_ONCE' (case insensitive).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/nrql_alert_condition#threshold_occurrences NrqlAlertCondition#threshold_occurrences}
        '''
        result = self._values.get("threshold_occurrences")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def time_function(self) -> typing.Optional[builtins.str]:
        '''Valid values are: 'all' or 'any'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/nrql_alert_condition#time_function NrqlAlertCondition#time_function}
        '''
        result = self._values.get("time_function")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NrqlAlertConditionTerm(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NrqlAlertConditionTermList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.nrqlAlertCondition.NrqlAlertConditionTermList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8ffa6a169fca23d503484a3774099df44d57d60b274b987ed15d11a170b2ef21)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "NrqlAlertConditionTermOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aee25de4ca2d5290185bc0a21a5b7058c8fbf62ce184b381b4ebb1b7f0b6b7d0)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("NrqlAlertConditionTermOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b9cf557d8a2c56fb843582b1b64048dad71b2d966d35a3727b7aca4cbd9d04b3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ed02c780a39b21ab214c13d7e9256fb6c7fe55521aef43f3021b6e56c812204b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7c0eef006611b4d7bfb3b951a2a022704f1a47169f6034b2c6da6782958aef06)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NrqlAlertConditionTerm]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NrqlAlertConditionTerm]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NrqlAlertConditionTerm]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9005ee3460458e7b62441df3c099e5647f27b333784846bd32ce2399ffcd82e2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class NrqlAlertConditionTermOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.nrqlAlertCondition.NrqlAlertConditionTermOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d048ac133ef35f3687c54fcb3c76ce9dc76768eb5814f3d9ed7a2ae47be35dfc)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putPrediction")
    def put_prediction(
        self,
        *,
        predict_by: typing.Optional[jsii.Number] = None,
        prefer_prediction_violation: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param predict_by: BETA PREVIEW: the ``predict_by`` field is in limited release and only enabled for preview on a per-account basis. - The duration, in seconds, that the prediction should look into the future. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/nrql_alert_condition#predict_by NrqlAlertCondition#predict_by}
        :param prefer_prediction_violation: BETA PREVIEW: the ``prefer_prediction_violation`` field is in limited release and only enabled for preview on a per-account basis. - If a prediction incident is open when a term's static threshold is breached by the actual signal, default behavior is to close the prediction incident and open a static incident. Setting ``prefer_prediction_violation`` to ``true`` overrides this behavior leaving the prediction incident open and preventing a static incident from opening. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/nrql_alert_condition#prefer_prediction_violation NrqlAlertCondition#prefer_prediction_violation}
        '''
        value = NrqlAlertConditionTermPrediction(
            predict_by=predict_by,
            prefer_prediction_violation=prefer_prediction_violation,
        )

        return typing.cast(None, jsii.invoke(self, "putPrediction", [value]))

    @jsii.member(jsii_name="resetDisableHealthStatusReporting")
    def reset_disable_health_status_reporting(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDisableHealthStatusReporting", []))

    @jsii.member(jsii_name="resetDuration")
    def reset_duration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDuration", []))

    @jsii.member(jsii_name="resetOperator")
    def reset_operator(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOperator", []))

    @jsii.member(jsii_name="resetPrediction")
    def reset_prediction(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPrediction", []))

    @jsii.member(jsii_name="resetPriority")
    def reset_priority(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPriority", []))

    @jsii.member(jsii_name="resetThresholdDuration")
    def reset_threshold_duration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetThresholdDuration", []))

    @jsii.member(jsii_name="resetThresholdOccurrences")
    def reset_threshold_occurrences(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetThresholdOccurrences", []))

    @jsii.member(jsii_name="resetTimeFunction")
    def reset_time_function(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeFunction", []))

    @builtins.property
    @jsii.member(jsii_name="prediction")
    def prediction(self) -> "NrqlAlertConditionTermPredictionOutputReference":
        return typing.cast("NrqlAlertConditionTermPredictionOutputReference", jsii.get(self, "prediction"))

    @builtins.property
    @jsii.member(jsii_name="disableHealthStatusReportingInput")
    def disable_health_status_reporting_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "disableHealthStatusReportingInput"))

    @builtins.property
    @jsii.member(jsii_name="durationInput")
    def duration_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "durationInput"))

    @builtins.property
    @jsii.member(jsii_name="operatorInput")
    def operator_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "operatorInput"))

    @builtins.property
    @jsii.member(jsii_name="predictionInput")
    def prediction_input(self) -> typing.Optional["NrqlAlertConditionTermPrediction"]:
        return typing.cast(typing.Optional["NrqlAlertConditionTermPrediction"], jsii.get(self, "predictionInput"))

    @builtins.property
    @jsii.member(jsii_name="priorityInput")
    def priority_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "priorityInput"))

    @builtins.property
    @jsii.member(jsii_name="thresholdDurationInput")
    def threshold_duration_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "thresholdDurationInput"))

    @builtins.property
    @jsii.member(jsii_name="thresholdInput")
    def threshold_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "thresholdInput"))

    @builtins.property
    @jsii.member(jsii_name="thresholdOccurrencesInput")
    def threshold_occurrences_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "thresholdOccurrencesInput"))

    @builtins.property
    @jsii.member(jsii_name="timeFunctionInput")
    def time_function_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "timeFunctionInput"))

    @builtins.property
    @jsii.member(jsii_name="disableHealthStatusReporting")
    def disable_health_status_reporting(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "disableHealthStatusReporting"))

    @disable_health_status_reporting.setter
    def disable_health_status_reporting(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aac9b9bc3f78ad9469fa7d29c1dc60f40fc12fa372a4bb64b6505a290b183967)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "disableHealthStatusReporting", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="duration")
    def duration(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "duration"))

    @duration.setter
    def duration(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6de5a2e381d0196e105eb3c5866b69774eb16a3412dd485cb17b70485b47d044)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "duration", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="operator")
    def operator(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "operator"))

    @operator.setter
    def operator(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d8bce72ed4fd9971633c0113db359bbf9a4247667d07317b2de3a4a2f8b77cb4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "operator", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="priority")
    def priority(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "priority"))

    @priority.setter
    def priority(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__921e62834048f8c6fa8808fec40fa01287dad469484c83052e90b13b5a577bfd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "priority", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="threshold")
    def threshold(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "threshold"))

    @threshold.setter
    def threshold(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cae0a5ed6476407dfdc3660cb0a743833764217f428c036f5346646f6e085d6a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "threshold", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="thresholdDuration")
    def threshold_duration(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "thresholdDuration"))

    @threshold_duration.setter
    def threshold_duration(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__08715be7a59b0a2b582ac5bd89c3fce130ab5f5e3118e24efc2a871e36ec081f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "thresholdDuration", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="thresholdOccurrences")
    def threshold_occurrences(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "thresholdOccurrences"))

    @threshold_occurrences.setter
    def threshold_occurrences(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__835e90259465623ac1be32cc9adfbcbfe793bfd82fc79bf493007dae8967b041)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "thresholdOccurrences", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="timeFunction")
    def time_function(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "timeFunction"))

    @time_function.setter
    def time_function(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c8f452ea66baacf4145872daa895d6b74f6413dfb3a6dad071608b0cd055248)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timeFunction", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NrqlAlertConditionTerm]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NrqlAlertConditionTerm]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NrqlAlertConditionTerm]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d5867fb1b30d0f09ef72a03955634050a9a709670306032c34b09db4f284485b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-newrelic.nrqlAlertCondition.NrqlAlertConditionTermPrediction",
    jsii_struct_bases=[],
    name_mapping={
        "predict_by": "predictBy",
        "prefer_prediction_violation": "preferPredictionViolation",
    },
)
class NrqlAlertConditionTermPrediction:
    def __init__(
        self,
        *,
        predict_by: typing.Optional[jsii.Number] = None,
        prefer_prediction_violation: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param predict_by: BETA PREVIEW: the ``predict_by`` field is in limited release and only enabled for preview on a per-account basis. - The duration, in seconds, that the prediction should look into the future. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/nrql_alert_condition#predict_by NrqlAlertCondition#predict_by}
        :param prefer_prediction_violation: BETA PREVIEW: the ``prefer_prediction_violation`` field is in limited release and only enabled for preview on a per-account basis. - If a prediction incident is open when a term's static threshold is breached by the actual signal, default behavior is to close the prediction incident and open a static incident. Setting ``prefer_prediction_violation`` to ``true`` overrides this behavior leaving the prediction incident open and preventing a static incident from opening. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/nrql_alert_condition#prefer_prediction_violation NrqlAlertCondition#prefer_prediction_violation}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a9d8d626bf7989bbb243f3b8cc5d92cc286b2c5de6e1de6512d57aa529402bc4)
            check_type(argname="argument predict_by", value=predict_by, expected_type=type_hints["predict_by"])
            check_type(argname="argument prefer_prediction_violation", value=prefer_prediction_violation, expected_type=type_hints["prefer_prediction_violation"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if predict_by is not None:
            self._values["predict_by"] = predict_by
        if prefer_prediction_violation is not None:
            self._values["prefer_prediction_violation"] = prefer_prediction_violation

    @builtins.property
    def predict_by(self) -> typing.Optional[jsii.Number]:
        '''BETA PREVIEW: the ``predict_by`` field is in limited release and only enabled for preview on a per-account basis.

        - The duration, in seconds, that the prediction should look into the future.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/nrql_alert_condition#predict_by NrqlAlertCondition#predict_by}
        '''
        result = self._values.get("predict_by")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def prefer_prediction_violation(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''BETA PREVIEW: the ``prefer_prediction_violation`` field is in limited release and only enabled for preview on a per-account basis.

        - If a prediction incident is open when a term's static threshold is breached by the actual signal, default behavior is to close the prediction incident and open a static incident. Setting ``prefer_prediction_violation`` to ``true`` overrides this behavior leaving the prediction incident open and preventing a static incident from opening.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/nrql_alert_condition#prefer_prediction_violation NrqlAlertCondition#prefer_prediction_violation}
        '''
        result = self._values.get("prefer_prediction_violation")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NrqlAlertConditionTermPrediction(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NrqlAlertConditionTermPredictionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.nrqlAlertCondition.NrqlAlertConditionTermPredictionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a4aecf9fa2c13608fbd2a4374a100044fb35d462c10b525905a7c2b9f6d2021f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetPredictBy")
    def reset_predict_by(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPredictBy", []))

    @jsii.member(jsii_name="resetPreferPredictionViolation")
    def reset_prefer_prediction_violation(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPreferPredictionViolation", []))

    @builtins.property
    @jsii.member(jsii_name="predictByInput")
    def predict_by_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "predictByInput"))

    @builtins.property
    @jsii.member(jsii_name="preferPredictionViolationInput")
    def prefer_prediction_violation_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "preferPredictionViolationInput"))

    @builtins.property
    @jsii.member(jsii_name="predictBy")
    def predict_by(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "predictBy"))

    @predict_by.setter
    def predict_by(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4eb907af12c53e90886585f9243296afe3505bfc1288689f6b23119ea22bf22b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "predictBy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="preferPredictionViolation")
    def prefer_prediction_violation(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "preferPredictionViolation"))

    @prefer_prediction_violation.setter
    def prefer_prediction_violation(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d9198e72a63068c080815551b77f4c563fda08b65cc28c59c7e0dfb45102ce56)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "preferPredictionViolation", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[NrqlAlertConditionTermPrediction]:
        return typing.cast(typing.Optional[NrqlAlertConditionTermPrediction], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[NrqlAlertConditionTermPrediction],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8be29f22a84e7eccb6d1597e942fce2160730a25c6b0f41fd9f7402970a6df7b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-newrelic.nrqlAlertCondition.NrqlAlertConditionTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create"},
)
class NrqlAlertConditionTimeouts:
    def __init__(self, *, create: typing.Optional[builtins.str] = None) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/nrql_alert_condition#create NrqlAlertCondition#create}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ad557cdb849fcdabb8eb24917c404848f2760660e0b62e55ca1dad407aec562)
            check_type(argname="argument create", value=create, expected_type=type_hints["create"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if create is not None:
            self._values["create"] = create

    @builtins.property
    def create(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/nrql_alert_condition#create NrqlAlertCondition#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NrqlAlertConditionTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NrqlAlertConditionTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.nrqlAlertCondition.NrqlAlertConditionTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f4088db823487b55fc997dab356525bc556b555d5c3d64ec839ce414e3ce6bf2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCreate")
    def reset_create(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCreate", []))

    @builtins.property
    @jsii.member(jsii_name="createInput")
    def create_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "createInput"))

    @builtins.property
    @jsii.member(jsii_name="create")
    def create(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "create"))

    @create.setter
    def create(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__060dec044642fc1004ed3a66c6c032e5d0084366fcd17c8c383f7d561316c0ed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NrqlAlertConditionTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NrqlAlertConditionTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NrqlAlertConditionTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b9e3ca0effb140cc7bd5e446c4bb34697a236c010d087a8bc3a92f36da2b496e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-newrelic.nrqlAlertCondition.NrqlAlertConditionWarning",
    jsii_struct_bases=[],
    name_mapping={
        "threshold": "threshold",
        "disable_health_status_reporting": "disableHealthStatusReporting",
        "duration": "duration",
        "operator": "operator",
        "prediction": "prediction",
        "threshold_duration": "thresholdDuration",
        "threshold_occurrences": "thresholdOccurrences",
        "time_function": "timeFunction",
    },
)
class NrqlAlertConditionWarning:
    def __init__(
        self,
        *,
        threshold: jsii.Number,
        disable_health_status_reporting: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        duration: typing.Optional[jsii.Number] = None,
        operator: typing.Optional[builtins.str] = None,
        prediction: typing.Optional[typing.Union["NrqlAlertConditionWarningPrediction", typing.Dict[builtins.str, typing.Any]]] = None,
        threshold_duration: typing.Optional[jsii.Number] = None,
        threshold_occurrences: typing.Optional[builtins.str] = None,
        time_function: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param threshold: For baseline conditions must be in range [1, 1000]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/nrql_alert_condition#threshold NrqlAlertCondition#threshold}
        :param disable_health_status_reporting: Violations will not change system health status for this term. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/nrql_alert_condition#disable_health_status_reporting NrqlAlertCondition#disable_health_status_reporting}
        :param duration: In minutes, must be in the range of 1 to 120 (inclusive). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/nrql_alert_condition#duration NrqlAlertCondition#duration}
        :param operator: One of (above, above_or_equals, below, below_or_equals, equals, not_equals). Defaults to 'equals'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/nrql_alert_condition#operator NrqlAlertCondition#operator}
        :param prediction: prediction block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/nrql_alert_condition#prediction NrqlAlertCondition#prediction}
        :param threshold_duration: The duration, in seconds, that the threshold must violate in order to create an incident. Value must be a multiple of the 'aggregation_window' (which has a default of 60 seconds). Value must be within 120-86400 seconds for baseline conditions, and within 60-86400 seconds for static conditions Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/nrql_alert_condition#threshold_duration NrqlAlertCondition#threshold_duration}
        :param threshold_occurrences: The criteria for how many data points must be in violation for the specified threshold duration. Valid values are: 'ALL' or 'AT_LEAST_ONCE' (case insensitive). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/nrql_alert_condition#threshold_occurrences NrqlAlertCondition#threshold_occurrences}
        :param time_function: Valid values are: 'all' or 'any'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/nrql_alert_condition#time_function NrqlAlertCondition#time_function}
        '''
        if isinstance(prediction, dict):
            prediction = NrqlAlertConditionWarningPrediction(**prediction)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a906eb9e700e83c5bfb17aac849a1f4fe122be55f472074e1087e4f759c52bf6)
            check_type(argname="argument threshold", value=threshold, expected_type=type_hints["threshold"])
            check_type(argname="argument disable_health_status_reporting", value=disable_health_status_reporting, expected_type=type_hints["disable_health_status_reporting"])
            check_type(argname="argument duration", value=duration, expected_type=type_hints["duration"])
            check_type(argname="argument operator", value=operator, expected_type=type_hints["operator"])
            check_type(argname="argument prediction", value=prediction, expected_type=type_hints["prediction"])
            check_type(argname="argument threshold_duration", value=threshold_duration, expected_type=type_hints["threshold_duration"])
            check_type(argname="argument threshold_occurrences", value=threshold_occurrences, expected_type=type_hints["threshold_occurrences"])
            check_type(argname="argument time_function", value=time_function, expected_type=type_hints["time_function"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "threshold": threshold,
        }
        if disable_health_status_reporting is not None:
            self._values["disable_health_status_reporting"] = disable_health_status_reporting
        if duration is not None:
            self._values["duration"] = duration
        if operator is not None:
            self._values["operator"] = operator
        if prediction is not None:
            self._values["prediction"] = prediction
        if threshold_duration is not None:
            self._values["threshold_duration"] = threshold_duration
        if threshold_occurrences is not None:
            self._values["threshold_occurrences"] = threshold_occurrences
        if time_function is not None:
            self._values["time_function"] = time_function

    @builtins.property
    def threshold(self) -> jsii.Number:
        '''For baseline conditions must be in range [1, 1000].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/nrql_alert_condition#threshold NrqlAlertCondition#threshold}
        '''
        result = self._values.get("threshold")
        assert result is not None, "Required property 'threshold' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def disable_health_status_reporting(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Violations will not change system health status for this term.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/nrql_alert_condition#disable_health_status_reporting NrqlAlertCondition#disable_health_status_reporting}
        '''
        result = self._values.get("disable_health_status_reporting")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def duration(self) -> typing.Optional[jsii.Number]:
        '''In minutes, must be in the range of 1 to 120 (inclusive).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/nrql_alert_condition#duration NrqlAlertCondition#duration}
        '''
        result = self._values.get("duration")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def operator(self) -> typing.Optional[builtins.str]:
        '''One of (above, above_or_equals, below, below_or_equals, equals, not_equals). Defaults to 'equals'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/nrql_alert_condition#operator NrqlAlertCondition#operator}
        '''
        result = self._values.get("operator")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def prediction(self) -> typing.Optional["NrqlAlertConditionWarningPrediction"]:
        '''prediction block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/nrql_alert_condition#prediction NrqlAlertCondition#prediction}
        '''
        result = self._values.get("prediction")
        return typing.cast(typing.Optional["NrqlAlertConditionWarningPrediction"], result)

    @builtins.property
    def threshold_duration(self) -> typing.Optional[jsii.Number]:
        '''The duration, in seconds, that the threshold must violate in order to create an incident.

        Value must be a multiple of the 'aggregation_window' (which has a default of 60 seconds). Value must be within 120-86400 seconds for baseline conditions, and within 60-86400 seconds for static conditions

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/nrql_alert_condition#threshold_duration NrqlAlertCondition#threshold_duration}
        '''
        result = self._values.get("threshold_duration")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def threshold_occurrences(self) -> typing.Optional[builtins.str]:
        '''The criteria for how many data points must be in violation for the specified threshold duration.

        Valid values are: 'ALL' or 'AT_LEAST_ONCE' (case insensitive).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/nrql_alert_condition#threshold_occurrences NrqlAlertCondition#threshold_occurrences}
        '''
        result = self._values.get("threshold_occurrences")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def time_function(self) -> typing.Optional[builtins.str]:
        '''Valid values are: 'all' or 'any'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/nrql_alert_condition#time_function NrqlAlertCondition#time_function}
        '''
        result = self._values.get("time_function")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NrqlAlertConditionWarning(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NrqlAlertConditionWarningOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.nrqlAlertCondition.NrqlAlertConditionWarningOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__396902798d995dbd5cfef87e84cdffaa06f918e064d3c594ff61a1fbdf69fedf)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putPrediction")
    def put_prediction(
        self,
        *,
        predict_by: typing.Optional[jsii.Number] = None,
        prefer_prediction_violation: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param predict_by: BETA PREVIEW: the ``predict_by`` field is in limited release and only enabled for preview on a per-account basis. - The duration, in seconds, that the prediction should look into the future. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/nrql_alert_condition#predict_by NrqlAlertCondition#predict_by}
        :param prefer_prediction_violation: BETA PREVIEW: the ``prefer_prediction_violation`` field is in limited release and only enabled for preview on a per-account basis. - If a prediction incident is open when a term's static threshold is breached by the actual signal, default behavior is to close the prediction incident and open a static incident. Setting ``prefer_prediction_violation`` to ``true`` overrides this behavior leaving the prediction incident open and preventing a static incident from opening. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/nrql_alert_condition#prefer_prediction_violation NrqlAlertCondition#prefer_prediction_violation}
        '''
        value = NrqlAlertConditionWarningPrediction(
            predict_by=predict_by,
            prefer_prediction_violation=prefer_prediction_violation,
        )

        return typing.cast(None, jsii.invoke(self, "putPrediction", [value]))

    @jsii.member(jsii_name="resetDisableHealthStatusReporting")
    def reset_disable_health_status_reporting(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDisableHealthStatusReporting", []))

    @jsii.member(jsii_name="resetDuration")
    def reset_duration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDuration", []))

    @jsii.member(jsii_name="resetOperator")
    def reset_operator(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOperator", []))

    @jsii.member(jsii_name="resetPrediction")
    def reset_prediction(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPrediction", []))

    @jsii.member(jsii_name="resetThresholdDuration")
    def reset_threshold_duration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetThresholdDuration", []))

    @jsii.member(jsii_name="resetThresholdOccurrences")
    def reset_threshold_occurrences(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetThresholdOccurrences", []))

    @jsii.member(jsii_name="resetTimeFunction")
    def reset_time_function(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeFunction", []))

    @builtins.property
    @jsii.member(jsii_name="prediction")
    def prediction(self) -> "NrqlAlertConditionWarningPredictionOutputReference":
        return typing.cast("NrqlAlertConditionWarningPredictionOutputReference", jsii.get(self, "prediction"))

    @builtins.property
    @jsii.member(jsii_name="disableHealthStatusReportingInput")
    def disable_health_status_reporting_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "disableHealthStatusReportingInput"))

    @builtins.property
    @jsii.member(jsii_name="durationInput")
    def duration_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "durationInput"))

    @builtins.property
    @jsii.member(jsii_name="operatorInput")
    def operator_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "operatorInput"))

    @builtins.property
    @jsii.member(jsii_name="predictionInput")
    def prediction_input(
        self,
    ) -> typing.Optional["NrqlAlertConditionWarningPrediction"]:
        return typing.cast(typing.Optional["NrqlAlertConditionWarningPrediction"], jsii.get(self, "predictionInput"))

    @builtins.property
    @jsii.member(jsii_name="thresholdDurationInput")
    def threshold_duration_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "thresholdDurationInput"))

    @builtins.property
    @jsii.member(jsii_name="thresholdInput")
    def threshold_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "thresholdInput"))

    @builtins.property
    @jsii.member(jsii_name="thresholdOccurrencesInput")
    def threshold_occurrences_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "thresholdOccurrencesInput"))

    @builtins.property
    @jsii.member(jsii_name="timeFunctionInput")
    def time_function_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "timeFunctionInput"))

    @builtins.property
    @jsii.member(jsii_name="disableHealthStatusReporting")
    def disable_health_status_reporting(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "disableHealthStatusReporting"))

    @disable_health_status_reporting.setter
    def disable_health_status_reporting(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__847f92e3eb72d25916d7a9d0d7934e58c5112e74910e8c9c1da40a3f0bcc7a64)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "disableHealthStatusReporting", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="duration")
    def duration(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "duration"))

    @duration.setter
    def duration(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__572c495f386f17c5d5ee7e11ae17e07737033e1592ef250b189f45222eb74511)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "duration", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="operator")
    def operator(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "operator"))

    @operator.setter
    def operator(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__07fb469beb269ad6f6f63616c18dcb40a6eea255977dc5ae80decfd7cfdd91d9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "operator", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="threshold")
    def threshold(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "threshold"))

    @threshold.setter
    def threshold(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1128af0e89adec1a343888413f7f0b9d38d2fca8da5d4581868a762f279b6c9e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "threshold", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="thresholdDuration")
    def threshold_duration(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "thresholdDuration"))

    @threshold_duration.setter
    def threshold_duration(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7626af1439d533086d2b10f8c5ac9e71020e0be84ad36641a29f0b2a6b454bdd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "thresholdDuration", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="thresholdOccurrences")
    def threshold_occurrences(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "thresholdOccurrences"))

    @threshold_occurrences.setter
    def threshold_occurrences(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bd4aaf330585267dbfa62de3081897da4d20914c08950768a2f8c4c485c7c680)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "thresholdOccurrences", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="timeFunction")
    def time_function(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "timeFunction"))

    @time_function.setter
    def time_function(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0d936f54e74b913147af6cc5837dd4e6ebfeaf0b5c60659ccddc22d1fea26516)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timeFunction", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[NrqlAlertConditionWarning]:
        return typing.cast(typing.Optional[NrqlAlertConditionWarning], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[NrqlAlertConditionWarning]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__310aaefe7b3617c786c11b8d4bd3e393be8fa18c36bab4107df69461bf86c0ab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-newrelic.nrqlAlertCondition.NrqlAlertConditionWarningPrediction",
    jsii_struct_bases=[],
    name_mapping={
        "predict_by": "predictBy",
        "prefer_prediction_violation": "preferPredictionViolation",
    },
)
class NrqlAlertConditionWarningPrediction:
    def __init__(
        self,
        *,
        predict_by: typing.Optional[jsii.Number] = None,
        prefer_prediction_violation: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param predict_by: BETA PREVIEW: the ``predict_by`` field is in limited release and only enabled for preview on a per-account basis. - The duration, in seconds, that the prediction should look into the future. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/nrql_alert_condition#predict_by NrqlAlertCondition#predict_by}
        :param prefer_prediction_violation: BETA PREVIEW: the ``prefer_prediction_violation`` field is in limited release and only enabled for preview on a per-account basis. - If a prediction incident is open when a term's static threshold is breached by the actual signal, default behavior is to close the prediction incident and open a static incident. Setting ``prefer_prediction_violation`` to ``true`` overrides this behavior leaving the prediction incident open and preventing a static incident from opening. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/nrql_alert_condition#prefer_prediction_violation NrqlAlertCondition#prefer_prediction_violation}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__16cd67c82e668e9d0589af97fac34021db2897c7dde623d83be37e583afc80a8)
            check_type(argname="argument predict_by", value=predict_by, expected_type=type_hints["predict_by"])
            check_type(argname="argument prefer_prediction_violation", value=prefer_prediction_violation, expected_type=type_hints["prefer_prediction_violation"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if predict_by is not None:
            self._values["predict_by"] = predict_by
        if prefer_prediction_violation is not None:
            self._values["prefer_prediction_violation"] = prefer_prediction_violation

    @builtins.property
    def predict_by(self) -> typing.Optional[jsii.Number]:
        '''BETA PREVIEW: the ``predict_by`` field is in limited release and only enabled for preview on a per-account basis.

        - The duration, in seconds, that the prediction should look into the future.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/nrql_alert_condition#predict_by NrqlAlertCondition#predict_by}
        '''
        result = self._values.get("predict_by")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def prefer_prediction_violation(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''BETA PREVIEW: the ``prefer_prediction_violation`` field is in limited release and only enabled for preview on a per-account basis.

        - If a prediction incident is open when a term's static threshold is breached by the actual signal, default behavior is to close the prediction incident and open a static incident. Setting ``prefer_prediction_violation`` to ``true`` overrides this behavior leaving the prediction incident open and preventing a static incident from opening.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/nrql_alert_condition#prefer_prediction_violation NrqlAlertCondition#prefer_prediction_violation}
        '''
        result = self._values.get("prefer_prediction_violation")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NrqlAlertConditionWarningPrediction(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NrqlAlertConditionWarningPredictionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.nrqlAlertCondition.NrqlAlertConditionWarningPredictionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__abc9f8bdb919fb8f3a409758ba44c85305a52869dd96e83bacabb730fcef4233)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetPredictBy")
    def reset_predict_by(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPredictBy", []))

    @jsii.member(jsii_name="resetPreferPredictionViolation")
    def reset_prefer_prediction_violation(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPreferPredictionViolation", []))

    @builtins.property
    @jsii.member(jsii_name="predictByInput")
    def predict_by_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "predictByInput"))

    @builtins.property
    @jsii.member(jsii_name="preferPredictionViolationInput")
    def prefer_prediction_violation_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "preferPredictionViolationInput"))

    @builtins.property
    @jsii.member(jsii_name="predictBy")
    def predict_by(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "predictBy"))

    @predict_by.setter
    def predict_by(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a43c1399dea6f8df1f7c49941d0168fc69e3be796e4a3953a94f2f1d5834d20d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "predictBy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="preferPredictionViolation")
    def prefer_prediction_violation(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "preferPredictionViolation"))

    @prefer_prediction_violation.setter
    def prefer_prediction_violation(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__002906d00c4eb2efc9007b55a00c07bd6927572e79878c4ac4f409c9d568b610)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "preferPredictionViolation", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[NrqlAlertConditionWarningPrediction]:
        return typing.cast(typing.Optional[NrqlAlertConditionWarningPrediction], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[NrqlAlertConditionWarningPrediction],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__10d30bf40e663eb40225336c9b900f3ace8069d2aee67f8e776dbd538cb123bc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "NrqlAlertCondition",
    "NrqlAlertConditionConfig",
    "NrqlAlertConditionCritical",
    "NrqlAlertConditionCriticalOutputReference",
    "NrqlAlertConditionCriticalPrediction",
    "NrqlAlertConditionCriticalPredictionOutputReference",
    "NrqlAlertConditionNrql",
    "NrqlAlertConditionNrqlOutputReference",
    "NrqlAlertConditionTerm",
    "NrqlAlertConditionTermList",
    "NrqlAlertConditionTermOutputReference",
    "NrqlAlertConditionTermPrediction",
    "NrqlAlertConditionTermPredictionOutputReference",
    "NrqlAlertConditionTimeouts",
    "NrqlAlertConditionTimeoutsOutputReference",
    "NrqlAlertConditionWarning",
    "NrqlAlertConditionWarningOutputReference",
    "NrqlAlertConditionWarningPrediction",
    "NrqlAlertConditionWarningPredictionOutputReference",
]

publication.publish()

def _typecheckingstub__e52eb0f2929f737ba1776df9d79a771b2f00a332e1b163d9ab3fa64a7d8e284b(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    name: builtins.str,
    nrql: typing.Union[NrqlAlertConditionNrql, typing.Dict[builtins.str, typing.Any]],
    policy_id: jsii.Number,
    account_id: typing.Optional[jsii.Number] = None,
    aggregation_delay: typing.Optional[builtins.str] = None,
    aggregation_method: typing.Optional[builtins.str] = None,
    aggregation_timer: typing.Optional[builtins.str] = None,
    aggregation_window: typing.Optional[jsii.Number] = None,
    baseline_direction: typing.Optional[builtins.str] = None,
    close_violations_on_expiration: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    critical: typing.Optional[typing.Union[NrqlAlertConditionCritical, typing.Dict[builtins.str, typing.Any]]] = None,
    description: typing.Optional[builtins.str] = None,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    evaluation_delay: typing.Optional[jsii.Number] = None,
    expiration_duration: typing.Optional[jsii.Number] = None,
    fill_option: typing.Optional[builtins.str] = None,
    fill_value: typing.Optional[jsii.Number] = None,
    id: typing.Optional[builtins.str] = None,
    ignore_on_expected_termination: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    open_violation_on_expiration: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    runbook_url: typing.Optional[builtins.str] = None,
    signal_seasonality: typing.Optional[builtins.str] = None,
    slide_by: typing.Optional[jsii.Number] = None,
    term: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NrqlAlertConditionTerm, typing.Dict[builtins.str, typing.Any]]]]] = None,
    timeouts: typing.Optional[typing.Union[NrqlAlertConditionTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    title_template: typing.Optional[builtins.str] = None,
    type: typing.Optional[builtins.str] = None,
    violation_time_limit: typing.Optional[builtins.str] = None,
    violation_time_limit_seconds: typing.Optional[jsii.Number] = None,
    warning: typing.Optional[typing.Union[NrqlAlertConditionWarning, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__3e79d1dec7621d60689a8187f4a099221235baf35b489f1d84c73121c677f404(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__851d50fac13c83b56520f6d4f20e709f2cfa7ed90e48fa776d7fdbf7744e538b(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NrqlAlertConditionTerm, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__649a181d2072f4986a6d916e0fb1b523d523ac324e9d34cb668c3b071ab95216(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2cf83ef31936d18108d0d7869272a1c8b68ee44b30362ccc0e4a553f78a6fd36(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c53efff34b60671f0633dda09ad8cd277ced39b706772506e9bf8c0ba9d68f7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d11a04b2424e03b4f56fd2218a413d1ffc119863799049f6d2fe107edce2206(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c83a096d66a01205222103170d31ff422455bf5f8b1a2176d12b0b1eec7ef77(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1178104c45a96e85c754764950b49690215ad1d7e5c6970c1fcd56ddc4a1967a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ad799bf9921ce6ec8d6b2f55c260e5b238c4bfcd33ca1861a5c3639a16036d4(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__844560a7037a9b8f022aae9243361dc8c7883e5effb553677f4997ae891de136(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df6416b87f6aa0ae47d2d61248337887867763e9beaaa54c78a5f0701110aec7(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3026a32318e81a7cb6cbcd36463c84b2348ac09f647b8d2a6ef4a4b4ee2c5aaf(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b10ee5ebf73800fff06eeaeaa5a0297eb5a1a9941adf9030affa878abbf8b6a(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a277ffdb5cc4519b811e78635819ea848d780f0d307eb9d228d10372b53856f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2ba585e1de77b18cdee092bc6924807ee2afbeec0753a019d66bdf53fabf74f(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ca73208e17ed2b1c79afdb18903405f0fab6a4ef181e7b60c7a2ee763b494e6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__112ae38312274f8905f9db29f0d82f726039e66ded6af4fe7b3b1ea69e6ffe22(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50e9efa16666dc60ee2056f36051e419522e2b838d489e75a0de5eed91b719f5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2dd7027f0f0cb75a1e2b9066b8521b9353ae41003dca5710d0a1e16f1148c57a(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c65358198af17285a6ee7e5b0d3a07394f4aa1e3c23e1d077d6d8cc5055678c6(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d42d637ba8127466722b67c70c65ac1193c2e5ca86759ccac911e7e986e6ed0b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2b8a9a0344c79490b627e46c7e036dd74bd6dca74a718cf9209f0a850ad42af(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aba9e1adf13481848ce3c898ab366ef7f1aa053bf6ed22d0b16375dd1b4266fa(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f38e9255c94019f151736a491f525b6a239494adc4f8e48e64e6d6206890392a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4bedef0fb1419f165f98d8ebe6ab344c3681eb4f79e2da4a0fcf1e53f1142b65(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2ffbebd1a9672d2f85bd1c49a1d48f04dfba18d558133d676040784ef29c7d9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b889225e14227f9771c2c9ef955d88fe029675182009ddcb2021ce90e815343(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc0430dc9a3ee76d1557f1c8c9c13137528d867e7657bd1048c6d0fab99060f5(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    name: builtins.str,
    nrql: typing.Union[NrqlAlertConditionNrql, typing.Dict[builtins.str, typing.Any]],
    policy_id: jsii.Number,
    account_id: typing.Optional[jsii.Number] = None,
    aggregation_delay: typing.Optional[builtins.str] = None,
    aggregation_method: typing.Optional[builtins.str] = None,
    aggregation_timer: typing.Optional[builtins.str] = None,
    aggregation_window: typing.Optional[jsii.Number] = None,
    baseline_direction: typing.Optional[builtins.str] = None,
    close_violations_on_expiration: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    critical: typing.Optional[typing.Union[NrqlAlertConditionCritical, typing.Dict[builtins.str, typing.Any]]] = None,
    description: typing.Optional[builtins.str] = None,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    evaluation_delay: typing.Optional[jsii.Number] = None,
    expiration_duration: typing.Optional[jsii.Number] = None,
    fill_option: typing.Optional[builtins.str] = None,
    fill_value: typing.Optional[jsii.Number] = None,
    id: typing.Optional[builtins.str] = None,
    ignore_on_expected_termination: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    open_violation_on_expiration: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    runbook_url: typing.Optional[builtins.str] = None,
    signal_seasonality: typing.Optional[builtins.str] = None,
    slide_by: typing.Optional[jsii.Number] = None,
    term: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NrqlAlertConditionTerm, typing.Dict[builtins.str, typing.Any]]]]] = None,
    timeouts: typing.Optional[typing.Union[NrqlAlertConditionTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    title_template: typing.Optional[builtins.str] = None,
    type: typing.Optional[builtins.str] = None,
    violation_time_limit: typing.Optional[builtins.str] = None,
    violation_time_limit_seconds: typing.Optional[jsii.Number] = None,
    warning: typing.Optional[typing.Union[NrqlAlertConditionWarning, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9cc7d6cd689719ee6613918d93752c1b1df2a84ebf4cb678d6c69aad3c55e36d(
    *,
    threshold: jsii.Number,
    disable_health_status_reporting: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    duration: typing.Optional[jsii.Number] = None,
    operator: typing.Optional[builtins.str] = None,
    prediction: typing.Optional[typing.Union[NrqlAlertConditionCriticalPrediction, typing.Dict[builtins.str, typing.Any]]] = None,
    threshold_duration: typing.Optional[jsii.Number] = None,
    threshold_occurrences: typing.Optional[builtins.str] = None,
    time_function: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe7a5abac695cf60326226f1d06d767876623700784e01dd6fcc777627da5745(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab98be15f1b90d6daf004e1ebc5c7e27cfdad1e66262f18943e3624eb58f896a(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__544bb90e3fb8f478ac9b4a18241c77a415497b7c485bc8731cb2448641ff5461(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__499aaafc5ad66d0316461ee703bbe2c6ef67e7423684b4334a3a8a015a1918c6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa2471d7eff28412af98e903bd026131c7d026baf9e867c15074cc3fcc54e242(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7401fb6d9b681b5ae68cdae9f5927a2d3a40df0df5bbb0a04929e93feaf7957(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__56cbb1a7cec39889560b92cdbd37369e3dd059ce135fe15d38185e14e46d67ce(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8de95945dbccb17cd1e5a21f92b99f5645dea3130215d51515b5fa449ae6f03(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__523d0bbe6deb8a0a6bafbe28b69cf691774de8a93d6700a9ccbaf055e0846311(
    value: typing.Optional[NrqlAlertConditionCritical],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f016c68996fe74893413497c1cd7939a04ea54e41746ce3a67c2d7859eaa893d(
    *,
    predict_by: typing.Optional[jsii.Number] = None,
    prefer_prediction_violation: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bdf68c1b87aefa5f4395870c494cd64aebdf5c6ed9a1d153b81d66ddd42feb47(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f53c5995050e2f1ecf1aa6a532c4b2884e7cc5aef394de8c6703021a1c7cc04e(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b85df81d38451feb236c8cfb426a1837d48430d331e527143c5ef43adb54747(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c50c3f66dd42b50785626177b42e53847249be00cf79cfd3ee4ff82300828187(
    value: typing.Optional[NrqlAlertConditionCriticalPrediction],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c62249076f8a1e95787e0bdf5c0c59b2f6e89562e4dfc241b121925caa3708d(
    *,
    query: builtins.str,
    data_account_id: typing.Optional[jsii.Number] = None,
    evaluation_offset: typing.Optional[jsii.Number] = None,
    since_value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61b56ec5c882142ee82c70c1be58ba6ed1a3b7ea49b7f86799ab01357e328cb2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa732f6321cb5b98380e37224e8433ac5b46cf972b92646c99383de78f08e67c(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd8c7c3b76ac2f43e775b8e8d83482ad19b5cf4fe169e54a1189696dfc4792e2(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__58a623927db6ec8c356f7cf0ac9ae87a5c0456f1aea2b27b539a25b314c88eaf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5fe27c9b02aab9609180ef17c7f8079f66daba17886da427b7367ab94132747d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78b60e0cbb22b6a787c5884dd47d99c013a34c17031205979d4ba8146ac0b951(
    value: typing.Optional[NrqlAlertConditionNrql],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__472601cc201d7341e0bb9b95ae234ecf5726c2f0aaf9c8341255ddcd44f88883(
    *,
    threshold: jsii.Number,
    disable_health_status_reporting: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    duration: typing.Optional[jsii.Number] = None,
    operator: typing.Optional[builtins.str] = None,
    prediction: typing.Optional[typing.Union[NrqlAlertConditionTermPrediction, typing.Dict[builtins.str, typing.Any]]] = None,
    priority: typing.Optional[builtins.str] = None,
    threshold_duration: typing.Optional[jsii.Number] = None,
    threshold_occurrences: typing.Optional[builtins.str] = None,
    time_function: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ffa6a169fca23d503484a3774099df44d57d60b274b987ed15d11a170b2ef21(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aee25de4ca2d5290185bc0a21a5b7058c8fbf62ce184b381b4ebb1b7f0b6b7d0(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9cf557d8a2c56fb843582b1b64048dad71b2d966d35a3727b7aca4cbd9d04b3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed02c780a39b21ab214c13d7e9256fb6c7fe55521aef43f3021b6e56c812204b(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c0eef006611b4d7bfb3b951a2a022704f1a47169f6034b2c6da6782958aef06(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9005ee3460458e7b62441df3c099e5647f27b333784846bd32ce2399ffcd82e2(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NrqlAlertConditionTerm]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d048ac133ef35f3687c54fcb3c76ce9dc76768eb5814f3d9ed7a2ae47be35dfc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aac9b9bc3f78ad9469fa7d29c1dc60f40fc12fa372a4bb64b6505a290b183967(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6de5a2e381d0196e105eb3c5866b69774eb16a3412dd485cb17b70485b47d044(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8bce72ed4fd9971633c0113db359bbf9a4247667d07317b2de3a4a2f8b77cb4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__921e62834048f8c6fa8808fec40fa01287dad469484c83052e90b13b5a577bfd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cae0a5ed6476407dfdc3660cb0a743833764217f428c036f5346646f6e085d6a(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__08715be7a59b0a2b582ac5bd89c3fce130ab5f5e3118e24efc2a871e36ec081f(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__835e90259465623ac1be32cc9adfbcbfe793bfd82fc79bf493007dae8967b041(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c8f452ea66baacf4145872daa895d6b74f6413dfb3a6dad071608b0cd055248(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5867fb1b30d0f09ef72a03955634050a9a709670306032c34b09db4f284485b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NrqlAlertConditionTerm]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9d8d626bf7989bbb243f3b8cc5d92cc286b2c5de6e1de6512d57aa529402bc4(
    *,
    predict_by: typing.Optional[jsii.Number] = None,
    prefer_prediction_violation: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4aecf9fa2c13608fbd2a4374a100044fb35d462c10b525905a7c2b9f6d2021f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4eb907af12c53e90886585f9243296afe3505bfc1288689f6b23119ea22bf22b(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d9198e72a63068c080815551b77f4c563fda08b65cc28c59c7e0dfb45102ce56(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8be29f22a84e7eccb6d1597e942fce2160730a25c6b0f41fd9f7402970a6df7b(
    value: typing.Optional[NrqlAlertConditionTermPrediction],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ad557cdb849fcdabb8eb24917c404848f2760660e0b62e55ca1dad407aec562(
    *,
    create: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4088db823487b55fc997dab356525bc556b555d5c3d64ec839ce414e3ce6bf2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__060dec044642fc1004ed3a66c6c032e5d0084366fcd17c8c383f7d561316c0ed(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9e3ca0effb140cc7bd5e446c4bb34697a236c010d087a8bc3a92f36da2b496e(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NrqlAlertConditionTimeouts]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a906eb9e700e83c5bfb17aac849a1f4fe122be55f472074e1087e4f759c52bf6(
    *,
    threshold: jsii.Number,
    disable_health_status_reporting: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    duration: typing.Optional[jsii.Number] = None,
    operator: typing.Optional[builtins.str] = None,
    prediction: typing.Optional[typing.Union[NrqlAlertConditionWarningPrediction, typing.Dict[builtins.str, typing.Any]]] = None,
    threshold_duration: typing.Optional[jsii.Number] = None,
    threshold_occurrences: typing.Optional[builtins.str] = None,
    time_function: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__396902798d995dbd5cfef87e84cdffaa06f918e064d3c594ff61a1fbdf69fedf(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__847f92e3eb72d25916d7a9d0d7934e58c5112e74910e8c9c1da40a3f0bcc7a64(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__572c495f386f17c5d5ee7e11ae17e07737033e1592ef250b189f45222eb74511(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__07fb469beb269ad6f6f63616c18dcb40a6eea255977dc5ae80decfd7cfdd91d9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1128af0e89adec1a343888413f7f0b9d38d2fca8da5d4581868a762f279b6c9e(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7626af1439d533086d2b10f8c5ac9e71020e0be84ad36641a29f0b2a6b454bdd(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd4aaf330585267dbfa62de3081897da4d20914c08950768a2f8c4c485c7c680(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d936f54e74b913147af6cc5837dd4e6ebfeaf0b5c60659ccddc22d1fea26516(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__310aaefe7b3617c786c11b8d4bd3e393be8fa18c36bab4107df69461bf86c0ab(
    value: typing.Optional[NrqlAlertConditionWarning],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16cd67c82e668e9d0589af97fac34021db2897c7dde623d83be37e583afc80a8(
    *,
    predict_by: typing.Optional[jsii.Number] = None,
    prefer_prediction_violation: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__abc9f8bdb919fb8f3a409758ba44c85305a52869dd96e83bacabb730fcef4233(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a43c1399dea6f8df1f7c49941d0168fc69e3be796e4a3953a94f2f1d5834d20d(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__002906d00c4eb2efc9007b55a00c07bd6927572e79878c4ac4f409c9d568b610(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10d30bf40e663eb40225336c9b900f3ace8069d2aee67f8e776dbd538cb123bc(
    value: typing.Optional[NrqlAlertConditionWarningPrediction],
) -> None:
    """Type checking stubs"""
    pass
