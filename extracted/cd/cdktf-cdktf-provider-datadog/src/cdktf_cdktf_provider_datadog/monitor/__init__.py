r'''
# `datadog_monitor`

Refer to the Terraform Registry for docs: [`datadog_monitor`](https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/monitor).
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


class Monitor(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.monitor.Monitor",
):
    '''Represents a {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/monitor datadog_monitor}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        message: builtins.str,
        name: builtins.str,
        query: builtins.str,
        type: builtins.str,
        enable_logs_sample: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_samples: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        escalation_message: typing.Optional[builtins.str] = None,
        evaluation_delay: typing.Optional[jsii.Number] = None,
        force_delete: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        groupby_simple_monitor: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        group_retention_duration: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        include_tags: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        locked: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        monitor_thresholds: typing.Optional[typing.Union["MonitorMonitorThresholds", typing.Dict[builtins.str, typing.Any]]] = None,
        monitor_threshold_windows: typing.Optional[typing.Union["MonitorMonitorThresholdWindows", typing.Dict[builtins.str, typing.Any]]] = None,
        new_group_delay: typing.Optional[jsii.Number] = None,
        new_host_delay: typing.Optional[jsii.Number] = None,
        no_data_timeframe: typing.Optional[jsii.Number] = None,
        notification_preset_name: typing.Optional[builtins.str] = None,
        notify_audit: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        notify_by: typing.Optional[typing.Sequence[builtins.str]] = None,
        notify_no_data: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        on_missing_data: typing.Optional[builtins.str] = None,
        priority: typing.Optional[builtins.str] = None,
        renotify_interval: typing.Optional[jsii.Number] = None,
        renotify_occurrences: typing.Optional[jsii.Number] = None,
        renotify_statuses: typing.Optional[typing.Sequence[builtins.str]] = None,
        require_full_window: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        restricted_roles: typing.Optional[typing.Sequence[builtins.str]] = None,
        scheduling_options: typing.Optional[typing.Union["MonitorSchedulingOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        tags: typing.Optional[typing.Sequence[builtins.str]] = None,
        timeout_h: typing.Optional[jsii.Number] = None,
        validate: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        variables: typing.Optional[typing.Union["MonitorVariables", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/monitor datadog_monitor} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param message: A message to include with notifications for this monitor. Email notifications can be sent to specific users by using the same ``@username`` notation as events. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/monitor#message Monitor#message}
        :param name: Name of Datadog monitor. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/monitor#name Monitor#name}
        :param query: The monitor query to notify on. Note this is not the same query you see in the UI and the syntax is different depending on the monitor type, please see the `API Reference <https://docs.datadoghq.com/api/v1/monitors/#create-a-monitor>`_ for details. ``terraform plan`` will validate query contents unless ``validate`` is set to ``false``. **Note:** APM latency data is now available as Distribution Metrics. Existing monitors have been migrated automatically but all terraformed monitors can still use the existing metrics. We strongly recommend updating monitor definitions to query the new metrics. To learn more, or to see examples of how to update your terraform definitions to utilize the new distribution metrics, see the `detailed doc <https://docs.datadoghq.com/tracing/guide/ddsketch_trace_metrics/>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/monitor#query Monitor#query}
        :param type: The type of the monitor. The mapping from these types to the types found in the Datadog Web UI can be found in the Datadog API `documentation page <https://docs.datadoghq.com/api/v1/monitors/#create-a-monitor>`_. Note: The monitor type cannot be changed after a monitor is created. Valid values are ``composite``, ``event alert``, ``log alert``, ``metric alert``, ``process alert``, ``query alert``, ``rum alert``, ``service check``, ``synthetics alert``, ``trace-analytics alert``, ``slo alert``, ``event-v2 alert``, ``audit alert``, ``ci-pipelines alert``, ``ci-tests alert``, ``error-tracking alert``, ``database-monitoring alert``, ``network-performance alert``, ``cost alert``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/monitor#type Monitor#type}
        :param enable_logs_sample: A boolean indicating whether or not to include a list of log values which triggered the alert. This is only used by log monitors. Defaults to ``false``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/monitor#enable_logs_sample Monitor#enable_logs_sample}
        :param enable_samples: Whether or not a list of samples which triggered the alert is included. This is only used by CI Test and Pipeline monitors. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/monitor#enable_samples Monitor#enable_samples}
        :param escalation_message: A message to include with a re-notification. Supports the ``@username`` notification allowed elsewhere. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/monitor#escalation_message Monitor#escalation_message}
        :param evaluation_delay: (Only applies to metric alert) Time (in seconds) to delay evaluation, as a non-negative integer. For example, if the value is set to ``300`` (5min), the ``timeframe`` is set to ``last_5m`` and the time is 7:00, the monitor will evaluate data from 6:50 to 6:55. This is useful for AWS CloudWatch and other backfilled metrics to ensure the monitor will always have data during evaluation. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/monitor#evaluation_delay Monitor#evaluation_delay}
        :param force_delete: A boolean indicating whether this monitor can be deleted even if it’s referenced by other resources (e.g. SLO, composite monitor). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/monitor#force_delete Monitor#force_delete}
        :param groupby_simple_monitor: Whether or not to trigger one alert if any source breaches a threshold. This is only used by log monitors. Defaults to ``false``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/monitor#groupby_simple_monitor Monitor#groupby_simple_monitor}
        :param group_retention_duration: The time span after which groups with missing data are dropped from the monitor state. The minimum value is one hour, and the maximum value is 72 hours. Example values are: 60m, 1h, and 2d. This option is only available for APM Trace Analytics, Audit Trail, CI, Error Tracking, Event, Logs, and RUM monitors. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/monitor#group_retention_duration Monitor#group_retention_duration}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/monitor#id Monitor#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param include_tags: A boolean indicating whether notifications from this monitor automatically insert its triggering tags into the title. Defaults to ``true``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/monitor#include_tags Monitor#include_tags}
        :param locked: A boolean indicating whether changes to this monitor should be restricted to the creator or admins. Defaults to ``false``. **Deprecated.** Use ``restricted_roles``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/monitor#locked Monitor#locked}
        :param monitor_thresholds: monitor_thresholds block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/monitor#monitor_thresholds Monitor#monitor_thresholds}
        :param monitor_threshold_windows: monitor_threshold_windows block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/monitor#monitor_threshold_windows Monitor#monitor_threshold_windows}
        :param new_group_delay: The time (in seconds) to skip evaluations for new groups. ``new_group_delay`` overrides ``new_host_delay`` if it is set to a nonzero value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/monitor#new_group_delay Monitor#new_group_delay}
        :param new_host_delay: **Deprecated**. See ``new_group_delay``. Time (in seconds) to allow a host to boot and applications to fully start before starting the evaluation of monitor results. Should be a non-negative integer. This value is ignored for simple monitors and monitors not grouped by host. The only case when this should be used is to override the default and set ``new_host_delay`` to zero for monitors grouped by host. **Deprecated.** Use ``new_group_delay`` except when setting ``new_host_delay`` to zero. Defaults to ``300``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/monitor#new_host_delay Monitor#new_host_delay}
        :param no_data_timeframe: The number of minutes before a monitor will notify when data stops reporting. We recommend at least 2x the monitor timeframe for metric alerts or 2 minutes for service checks. Defaults to ``10``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/monitor#no_data_timeframe Monitor#no_data_timeframe}
        :param notification_preset_name: Toggles the display of additional content sent in the monitor notification. Valid values are ``show_all``, ``hide_query``, ``hide_handles``, ``hide_all``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/monitor#notification_preset_name Monitor#notification_preset_name}
        :param notify_audit: A boolean indicating whether tagged users will be notified on changes to this monitor. Defaults to ``false``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/monitor#notify_audit Monitor#notify_audit}
        :param notify_by: Controls what granularity a monitor alerts on. Only available for monitors with groupings. For instance, a monitor grouped by ``cluster``, ``namespace``, and ``pod`` can be configured to only notify on each new ``cluster`` violating the alert conditions by setting ``notify_by`` to ``['cluster']``. Tags mentioned in ``notify_by`` must be a subset of the grouping tags in the query. For example, a query grouped by ``cluster`` and ``namespace`` cannot notify on ``region``. Setting ``notify_by`` to ``[*]`` configures the monitor to notify as a simple-alert. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/monitor#notify_by Monitor#notify_by}
        :param notify_no_data: A boolean indicating whether this monitor will notify when data stops reporting. Defaults to ``false``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/monitor#notify_no_data Monitor#notify_no_data}
        :param on_missing_data: Controls how groups or monitors are treated if an evaluation does not return any data points. The default option results in different behavior depending on the monitor query type. For monitors using ``Count`` queries, an empty monitor evaluation is treated as 0 and is compared to the threshold conditions. For monitors using any query type other than ``Count``, for example ``Gauge``, ``Measure``, or ``Rate``, the monitor shows the last known status. This option is not available for Service Check, Composite, or SLO monitors. Valid values are: ``show_no_data``, ``show_and_notify_no_data``, ``resolve``, and ``default``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/monitor#on_missing_data Monitor#on_missing_data}
        :param priority: Integer from 1 (high) to 5 (low) indicating alert severity. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/monitor#priority Monitor#priority}
        :param renotify_interval: The number of minutes after the last notification before a monitor will re-notify on the current status. It will only re-notify if it's not resolved. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/monitor#renotify_interval Monitor#renotify_interval}
        :param renotify_occurrences: The number of re-notification messages that should be sent on the current status. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/monitor#renotify_occurrences Monitor#renotify_occurrences}
        :param renotify_statuses: The types of statuses for which re-notification messages should be sent. Valid values are ``alert``, ``warn``, ``no data``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/monitor#renotify_statuses Monitor#renotify_statuses}
        :param require_full_window: A boolean indicating whether this monitor needs a full window of data before it's evaluated. Datadog strongly recommends you set this to ``false`` for sparse metrics, otherwise some evaluations may be skipped. If there's a custom_schedule set, ``require_full_window`` must be false and will be ignored. Defaults to ``true``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/monitor#require_full_window Monitor#require_full_window}
        :param restricted_roles: A list of unique role identifiers to define which roles are allowed to edit the monitor. Editing a monitor includes any updates to the monitor configuration, monitor deletion, and muting of the monitor for any amount of time. Roles unique identifiers can be pulled from the `Roles API <https://docs.datadoghq.com/api/latest/roles/#list-roles>`_ in the ``data.id`` field. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/monitor#restricted_roles Monitor#restricted_roles}
        :param scheduling_options: scheduling_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/monitor#scheduling_options Monitor#scheduling_options}
        :param tags: A list of tags to associate with your monitor. This can help you categorize and filter monitors in the manage monitors page of the UI. Note: it's not currently possible to filter by these tags when querying via the API Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/monitor#tags Monitor#tags}
        :param timeout_h: The number of hours of the monitor not reporting data before it automatically resolves from a triggered state. The minimum allowed value is 0 hours. The maximum allowed value is 24 hours. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/monitor#timeout_h Monitor#timeout_h}
        :param validate: If set to ``false``, skip the validation call done during plan. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/monitor#validate Monitor#validate}
        :param variables: variables block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/monitor#variables Monitor#variables}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__03d752530da5a500b776a36d7bb2dfc57404c491f23b5196cf52d9deec0a993d)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = MonitorConfig(
            message=message,
            name=name,
            query=query,
            type=type,
            enable_logs_sample=enable_logs_sample,
            enable_samples=enable_samples,
            escalation_message=escalation_message,
            evaluation_delay=evaluation_delay,
            force_delete=force_delete,
            groupby_simple_monitor=groupby_simple_monitor,
            group_retention_duration=group_retention_duration,
            id=id,
            include_tags=include_tags,
            locked=locked,
            monitor_thresholds=monitor_thresholds,
            monitor_threshold_windows=monitor_threshold_windows,
            new_group_delay=new_group_delay,
            new_host_delay=new_host_delay,
            no_data_timeframe=no_data_timeframe,
            notification_preset_name=notification_preset_name,
            notify_audit=notify_audit,
            notify_by=notify_by,
            notify_no_data=notify_no_data,
            on_missing_data=on_missing_data,
            priority=priority,
            renotify_interval=renotify_interval,
            renotify_occurrences=renotify_occurrences,
            renotify_statuses=renotify_statuses,
            require_full_window=require_full_window,
            restricted_roles=restricted_roles,
            scheduling_options=scheduling_options,
            tags=tags,
            timeout_h=timeout_h,
            validate=validate,
            variables=variables,
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
        '''Generates CDKTF code for importing a Monitor resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the Monitor to import.
        :param import_from_id: The id of the existing Monitor that should be imported. Refer to the {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/monitor#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the Monitor to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b15249212d54849270fa62a88a2fc2945d9c971610728df9f77f1dd018583e86)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putMonitorThresholds")
    def put_monitor_thresholds(
        self,
        *,
        critical: typing.Optional[builtins.str] = None,
        critical_recovery: typing.Optional[builtins.str] = None,
        ok: typing.Optional[builtins.str] = None,
        unknown: typing.Optional[builtins.str] = None,
        warning: typing.Optional[builtins.str] = None,
        warning_recovery: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param critical: The monitor ``CRITICAL`` threshold. Must be a number. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/monitor#critical Monitor#critical}
        :param critical_recovery: The monitor ``CRITICAL`` recovery threshold. Must be a number. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/monitor#critical_recovery Monitor#critical_recovery}
        :param ok: The monitor ``OK`` threshold. Only supported in monitor type ``service check``. Must be a number. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/monitor#ok Monitor#ok}
        :param unknown: The monitor ``UNKNOWN`` threshold. Only supported in monitor type ``service check``. Must be a number. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/monitor#unknown Monitor#unknown}
        :param warning: The monitor ``WARNING`` threshold. Must be a number. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/monitor#warning Monitor#warning}
        :param warning_recovery: The monitor ``WARNING`` recovery threshold. Must be a number. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/monitor#warning_recovery Monitor#warning_recovery}
        '''
        value = MonitorMonitorThresholds(
            critical=critical,
            critical_recovery=critical_recovery,
            ok=ok,
            unknown=unknown,
            warning=warning,
            warning_recovery=warning_recovery,
        )

        return typing.cast(None, jsii.invoke(self, "putMonitorThresholds", [value]))

    @jsii.member(jsii_name="putMonitorThresholdWindows")
    def put_monitor_threshold_windows(
        self,
        *,
        recovery_window: typing.Optional[builtins.str] = None,
        trigger_window: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param recovery_window: Describes how long an anomalous metric must be normal before the alert recovers. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/monitor#recovery_window Monitor#recovery_window}
        :param trigger_window: Describes how long a metric must be anomalous before an alert triggers. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/monitor#trigger_window Monitor#trigger_window}
        '''
        value = MonitorMonitorThresholdWindows(
            recovery_window=recovery_window, trigger_window=trigger_window
        )

        return typing.cast(None, jsii.invoke(self, "putMonitorThresholdWindows", [value]))

    @jsii.member(jsii_name="putSchedulingOptions")
    def put_scheduling_options(
        self,
        *,
        custom_schedule: typing.Optional[typing.Union["MonitorSchedulingOptionsCustomSchedule", typing.Dict[builtins.str, typing.Any]]] = None,
        evaluation_window: typing.Optional[typing.Union["MonitorSchedulingOptionsEvaluationWindow", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param custom_schedule: custom_schedule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/monitor#custom_schedule Monitor#custom_schedule}
        :param evaluation_window: evaluation_window block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/monitor#evaluation_window Monitor#evaluation_window}
        '''
        value = MonitorSchedulingOptions(
            custom_schedule=custom_schedule, evaluation_window=evaluation_window
        )

        return typing.cast(None, jsii.invoke(self, "putSchedulingOptions", [value]))

    @jsii.member(jsii_name="putVariables")
    def put_variables(
        self,
        *,
        cloud_cost_query: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["MonitorVariablesCloudCostQuery", typing.Dict[builtins.str, typing.Any]]]]] = None,
        event_query: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["MonitorVariablesEventQuery", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param cloud_cost_query: cloud_cost_query block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/monitor#cloud_cost_query Monitor#cloud_cost_query}
        :param event_query: event_query block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/monitor#event_query Monitor#event_query}
        '''
        value = MonitorVariables(
            cloud_cost_query=cloud_cost_query, event_query=event_query
        )

        return typing.cast(None, jsii.invoke(self, "putVariables", [value]))

    @jsii.member(jsii_name="resetEnableLogsSample")
    def reset_enable_logs_sample(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnableLogsSample", []))

    @jsii.member(jsii_name="resetEnableSamples")
    def reset_enable_samples(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnableSamples", []))

    @jsii.member(jsii_name="resetEscalationMessage")
    def reset_escalation_message(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEscalationMessage", []))

    @jsii.member(jsii_name="resetEvaluationDelay")
    def reset_evaluation_delay(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEvaluationDelay", []))

    @jsii.member(jsii_name="resetForceDelete")
    def reset_force_delete(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetForceDelete", []))

    @jsii.member(jsii_name="resetGroupbySimpleMonitor")
    def reset_groupby_simple_monitor(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGroupbySimpleMonitor", []))

    @jsii.member(jsii_name="resetGroupRetentionDuration")
    def reset_group_retention_duration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGroupRetentionDuration", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetIncludeTags")
    def reset_include_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIncludeTags", []))

    @jsii.member(jsii_name="resetLocked")
    def reset_locked(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLocked", []))

    @jsii.member(jsii_name="resetMonitorThresholds")
    def reset_monitor_thresholds(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMonitorThresholds", []))

    @jsii.member(jsii_name="resetMonitorThresholdWindows")
    def reset_monitor_threshold_windows(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMonitorThresholdWindows", []))

    @jsii.member(jsii_name="resetNewGroupDelay")
    def reset_new_group_delay(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNewGroupDelay", []))

    @jsii.member(jsii_name="resetNewHostDelay")
    def reset_new_host_delay(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNewHostDelay", []))

    @jsii.member(jsii_name="resetNoDataTimeframe")
    def reset_no_data_timeframe(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNoDataTimeframe", []))

    @jsii.member(jsii_name="resetNotificationPresetName")
    def reset_notification_preset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNotificationPresetName", []))

    @jsii.member(jsii_name="resetNotifyAudit")
    def reset_notify_audit(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNotifyAudit", []))

    @jsii.member(jsii_name="resetNotifyBy")
    def reset_notify_by(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNotifyBy", []))

    @jsii.member(jsii_name="resetNotifyNoData")
    def reset_notify_no_data(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNotifyNoData", []))

    @jsii.member(jsii_name="resetOnMissingData")
    def reset_on_missing_data(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOnMissingData", []))

    @jsii.member(jsii_name="resetPriority")
    def reset_priority(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPriority", []))

    @jsii.member(jsii_name="resetRenotifyInterval")
    def reset_renotify_interval(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRenotifyInterval", []))

    @jsii.member(jsii_name="resetRenotifyOccurrences")
    def reset_renotify_occurrences(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRenotifyOccurrences", []))

    @jsii.member(jsii_name="resetRenotifyStatuses")
    def reset_renotify_statuses(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRenotifyStatuses", []))

    @jsii.member(jsii_name="resetRequireFullWindow")
    def reset_require_full_window(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRequireFullWindow", []))

    @jsii.member(jsii_name="resetRestrictedRoles")
    def reset_restricted_roles(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRestrictedRoles", []))

    @jsii.member(jsii_name="resetSchedulingOptions")
    def reset_scheduling_options(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSchedulingOptions", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

    @jsii.member(jsii_name="resetTimeoutH")
    def reset_timeout_h(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeoutH", []))

    @jsii.member(jsii_name="resetValidate")
    def reset_validate(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetValidate", []))

    @jsii.member(jsii_name="resetVariables")
    def reset_variables(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVariables", []))

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
    @jsii.member(jsii_name="monitorThresholds")
    def monitor_thresholds(self) -> "MonitorMonitorThresholdsOutputReference":
        return typing.cast("MonitorMonitorThresholdsOutputReference", jsii.get(self, "monitorThresholds"))

    @builtins.property
    @jsii.member(jsii_name="monitorThresholdWindows")
    def monitor_threshold_windows(
        self,
    ) -> "MonitorMonitorThresholdWindowsOutputReference":
        return typing.cast("MonitorMonitorThresholdWindowsOutputReference", jsii.get(self, "monitorThresholdWindows"))

    @builtins.property
    @jsii.member(jsii_name="schedulingOptions")
    def scheduling_options(self) -> "MonitorSchedulingOptionsOutputReference":
        return typing.cast("MonitorSchedulingOptionsOutputReference", jsii.get(self, "schedulingOptions"))

    @builtins.property
    @jsii.member(jsii_name="variables")
    def variables(self) -> "MonitorVariablesOutputReference":
        return typing.cast("MonitorVariablesOutputReference", jsii.get(self, "variables"))

    @builtins.property
    @jsii.member(jsii_name="enableLogsSampleInput")
    def enable_logs_sample_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enableLogsSampleInput"))

    @builtins.property
    @jsii.member(jsii_name="enableSamplesInput")
    def enable_samples_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enableSamplesInput"))

    @builtins.property
    @jsii.member(jsii_name="escalationMessageInput")
    def escalation_message_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "escalationMessageInput"))

    @builtins.property
    @jsii.member(jsii_name="evaluationDelayInput")
    def evaluation_delay_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "evaluationDelayInput"))

    @builtins.property
    @jsii.member(jsii_name="forceDeleteInput")
    def force_delete_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "forceDeleteInput"))

    @builtins.property
    @jsii.member(jsii_name="groupbySimpleMonitorInput")
    def groupby_simple_monitor_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "groupbySimpleMonitorInput"))

    @builtins.property
    @jsii.member(jsii_name="groupRetentionDurationInput")
    def group_retention_duration_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "groupRetentionDurationInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="includeTagsInput")
    def include_tags_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "includeTagsInput"))

    @builtins.property
    @jsii.member(jsii_name="lockedInput")
    def locked_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "lockedInput"))

    @builtins.property
    @jsii.member(jsii_name="messageInput")
    def message_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "messageInput"))

    @builtins.property
    @jsii.member(jsii_name="monitorThresholdsInput")
    def monitor_thresholds_input(self) -> typing.Optional["MonitorMonitorThresholds"]:
        return typing.cast(typing.Optional["MonitorMonitorThresholds"], jsii.get(self, "monitorThresholdsInput"))

    @builtins.property
    @jsii.member(jsii_name="monitorThresholdWindowsInput")
    def monitor_threshold_windows_input(
        self,
    ) -> typing.Optional["MonitorMonitorThresholdWindows"]:
        return typing.cast(typing.Optional["MonitorMonitorThresholdWindows"], jsii.get(self, "monitorThresholdWindowsInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="newGroupDelayInput")
    def new_group_delay_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "newGroupDelayInput"))

    @builtins.property
    @jsii.member(jsii_name="newHostDelayInput")
    def new_host_delay_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "newHostDelayInput"))

    @builtins.property
    @jsii.member(jsii_name="noDataTimeframeInput")
    def no_data_timeframe_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "noDataTimeframeInput"))

    @builtins.property
    @jsii.member(jsii_name="notificationPresetNameInput")
    def notification_preset_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "notificationPresetNameInput"))

    @builtins.property
    @jsii.member(jsii_name="notifyAuditInput")
    def notify_audit_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "notifyAuditInput"))

    @builtins.property
    @jsii.member(jsii_name="notifyByInput")
    def notify_by_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "notifyByInput"))

    @builtins.property
    @jsii.member(jsii_name="notifyNoDataInput")
    def notify_no_data_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "notifyNoDataInput"))

    @builtins.property
    @jsii.member(jsii_name="onMissingDataInput")
    def on_missing_data_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "onMissingDataInput"))

    @builtins.property
    @jsii.member(jsii_name="priorityInput")
    def priority_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "priorityInput"))

    @builtins.property
    @jsii.member(jsii_name="queryInput")
    def query_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "queryInput"))

    @builtins.property
    @jsii.member(jsii_name="renotifyIntervalInput")
    def renotify_interval_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "renotifyIntervalInput"))

    @builtins.property
    @jsii.member(jsii_name="renotifyOccurrencesInput")
    def renotify_occurrences_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "renotifyOccurrencesInput"))

    @builtins.property
    @jsii.member(jsii_name="renotifyStatusesInput")
    def renotify_statuses_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "renotifyStatusesInput"))

    @builtins.property
    @jsii.member(jsii_name="requireFullWindowInput")
    def require_full_window_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "requireFullWindowInput"))

    @builtins.property
    @jsii.member(jsii_name="restrictedRolesInput")
    def restricted_roles_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "restrictedRolesInput"))

    @builtins.property
    @jsii.member(jsii_name="schedulingOptionsInput")
    def scheduling_options_input(self) -> typing.Optional["MonitorSchedulingOptions"]:
        return typing.cast(typing.Optional["MonitorSchedulingOptions"], jsii.get(self, "schedulingOptionsInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsInput")
    def tags_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "tagsInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutHInput")
    def timeout_h_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "timeoutHInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="validateInput")
    def validate_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "validateInput"))

    @builtins.property
    @jsii.member(jsii_name="variablesInput")
    def variables_input(self) -> typing.Optional["MonitorVariables"]:
        return typing.cast(typing.Optional["MonitorVariables"], jsii.get(self, "variablesInput"))

    @builtins.property
    @jsii.member(jsii_name="enableLogsSample")
    def enable_logs_sample(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enableLogsSample"))

    @enable_logs_sample.setter
    def enable_logs_sample(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__81f8bf9e49030b5d383d179324967617c80b47d66c25bf8ffca99f3b8d912d39)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableLogsSample", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enableSamples")
    def enable_samples(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enableSamples"))

    @enable_samples.setter
    def enable_samples(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8340d3da1a091fa7c96cb62d406689deab438ff63063c1cc368ccc4bc22bcbad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableSamples", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="escalationMessage")
    def escalation_message(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "escalationMessage"))

    @escalation_message.setter
    def escalation_message(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cdddae296bdc4ca4e7901bae00211aaf3e372b924063de1da6352146817ad3a2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "escalationMessage", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="evaluationDelay")
    def evaluation_delay(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "evaluationDelay"))

    @evaluation_delay.setter
    def evaluation_delay(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e947460955ee77f41adba167010c6831a68353458127bc53ef62895214186920)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "evaluationDelay", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="forceDelete")
    def force_delete(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "forceDelete"))

    @force_delete.setter
    def force_delete(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e1f22ee04be8d02f3e5f17e4a1fbb7fd5d725cb4424e80c2961159409a189ddc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "forceDelete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="groupbySimpleMonitor")
    def groupby_simple_monitor(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "groupbySimpleMonitor"))

    @groupby_simple_monitor.setter
    def groupby_simple_monitor(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__325235c7b12b9fd92cfd8af5e0ef60b3c94a2bc7146b53a6ef88a2241ede1567)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "groupbySimpleMonitor", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="groupRetentionDuration")
    def group_retention_duration(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "groupRetentionDuration"))

    @group_retention_duration.setter
    def group_retention_duration(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6ae82f283395599aa52863ffd23cb17b690d32d223702cb3ccbc707b840abed8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "groupRetentionDuration", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__33386788a4cf80d4118761b9dc6165be89c25285d457904aa5d10a271e32afc5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="includeTags")
    def include_tags(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "includeTags"))

    @include_tags.setter
    def include_tags(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__78b1ccab005bd762704465fa121c3e6e6b2841f65caed6a6722614a365f5703a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "includeTags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="locked")
    def locked(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "locked"))

    @locked.setter
    def locked(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__29387954e743005838e858cc8ade6f246aca8b7159fea378ad779862ffffb8ca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "locked", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="message")
    def message(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "message"))

    @message.setter
    def message(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c2ca38574b162a31cc2e94a0eec2172022985a90478110641c9339851c1f22c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "message", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ed18a1d689eacf09c858f1c31d18eb7684ef017871eff9f80d696b164436723a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="newGroupDelay")
    def new_group_delay(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "newGroupDelay"))

    @new_group_delay.setter
    def new_group_delay(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c5518c7add5bc89adf6c937b23dea14e182ff53a5ae77bb797d875ded363cd90)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "newGroupDelay", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="newHostDelay")
    def new_host_delay(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "newHostDelay"))

    @new_host_delay.setter
    def new_host_delay(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0fc8c77298456e6070b6ff2abc888af064be80906b002bb5c9ba2fb338556aed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "newHostDelay", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="noDataTimeframe")
    def no_data_timeframe(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "noDataTimeframe"))

    @no_data_timeframe.setter
    def no_data_timeframe(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__357287683238a9286f71794dc0de94d1a95adde6b954d1adf8e4756fccc0d849)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "noDataTimeframe", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="notificationPresetName")
    def notification_preset_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "notificationPresetName"))

    @notification_preset_name.setter
    def notification_preset_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f67009a561d6fe51e8d77d9c4cdd957c5651ecc089b0410d450d1b090e806ba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "notificationPresetName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="notifyAudit")
    def notify_audit(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "notifyAudit"))

    @notify_audit.setter
    def notify_audit(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ffaf673280b156d724376e2518e7be13c8a49d5820fd148e1835d145921ef8e0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "notifyAudit", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="notifyBy")
    def notify_by(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "notifyBy"))

    @notify_by.setter
    def notify_by(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__245ec3db4d968566c54423a52f811cccb975e906f67bb6bda1a649ecddc492f0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "notifyBy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="notifyNoData")
    def notify_no_data(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "notifyNoData"))

    @notify_no_data.setter
    def notify_no_data(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fd4037766595c563bf35d0f7459bd782b91b2c8006fa7f4186fd29cef79790f9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "notifyNoData", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="onMissingData")
    def on_missing_data(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "onMissingData"))

    @on_missing_data.setter
    def on_missing_data(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a3a23bf86e1137584d2547b5a79e5d1f5449786664ec8b2a242c40a9ba359200)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "onMissingData", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="priority")
    def priority(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "priority"))

    @priority.setter
    def priority(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dce69cc7a405ce2fc0186e161a1e680cb8c4cd19eb0dc7e668177978ed9cd985)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "priority", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="query")
    def query(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "query"))

    @query.setter
    def query(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa3b1655ea5f7a07bf8bdee4922c34100172507557e6491c5f50acf96260408f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "query", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="renotifyInterval")
    def renotify_interval(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "renotifyInterval"))

    @renotify_interval.setter
    def renotify_interval(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1081324b3abca8958c5f0ed25494a029d150e5e28be5fcd79c1e38282647f939)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "renotifyInterval", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="renotifyOccurrences")
    def renotify_occurrences(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "renotifyOccurrences"))

    @renotify_occurrences.setter
    def renotify_occurrences(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f364f7da306f36883ebac18f373870fdcdce1d7668cf34291ec05d755305d69)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "renotifyOccurrences", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="renotifyStatuses")
    def renotify_statuses(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "renotifyStatuses"))

    @renotify_statuses.setter
    def renotify_statuses(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d9ad5a4d8a5aacc6a36cf757f614acb83c05a6c2280edf39d5f096b2802411f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "renotifyStatuses", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="requireFullWindow")
    def require_full_window(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "requireFullWindow"))

    @require_full_window.setter
    def require_full_window(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b84b707bdaa6bd1a058f696c923aab3bfce769fd39faba082efe25ea6ceea36a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "requireFullWindow", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="restrictedRoles")
    def restricted_roles(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "restrictedRoles"))

    @restricted_roles.setter
    def restricted_roles(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__75d9388eaa7398274281eba434f3342dc23d536cfe6ed6f53cc0dde7739fc21a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "restrictedRoles", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf3f00b724397b82df625731c524cc348b18a9c83d6ea529516a0bbf1b27d12f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="timeoutH")
    def timeout_h(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "timeoutH"))

    @timeout_h.setter
    def timeout_h(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__29fb2f8478c7ee4e69c6d1319593ba7656e802d5278a62cb4be71d5b9e09f936)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timeoutH", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__df5d7430a7b3b60245bc0662ca8db68de84fe87f9d835dfa543f4a924c9a6e96)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="validate")
    def validate(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "validate"))

    @validate.setter
    def validate(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a2c3244bee93836af124e02d0fa395c5165449b116b119a7d5db59a6ea731f5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "validate", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.monitor.MonitorConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "message": "message",
        "name": "name",
        "query": "query",
        "type": "type",
        "enable_logs_sample": "enableLogsSample",
        "enable_samples": "enableSamples",
        "escalation_message": "escalationMessage",
        "evaluation_delay": "evaluationDelay",
        "force_delete": "forceDelete",
        "groupby_simple_monitor": "groupbySimpleMonitor",
        "group_retention_duration": "groupRetentionDuration",
        "id": "id",
        "include_tags": "includeTags",
        "locked": "locked",
        "monitor_thresholds": "monitorThresholds",
        "monitor_threshold_windows": "monitorThresholdWindows",
        "new_group_delay": "newGroupDelay",
        "new_host_delay": "newHostDelay",
        "no_data_timeframe": "noDataTimeframe",
        "notification_preset_name": "notificationPresetName",
        "notify_audit": "notifyAudit",
        "notify_by": "notifyBy",
        "notify_no_data": "notifyNoData",
        "on_missing_data": "onMissingData",
        "priority": "priority",
        "renotify_interval": "renotifyInterval",
        "renotify_occurrences": "renotifyOccurrences",
        "renotify_statuses": "renotifyStatuses",
        "require_full_window": "requireFullWindow",
        "restricted_roles": "restrictedRoles",
        "scheduling_options": "schedulingOptions",
        "tags": "tags",
        "timeout_h": "timeoutH",
        "validate": "validate",
        "variables": "variables",
    },
)
class MonitorConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        message: builtins.str,
        name: builtins.str,
        query: builtins.str,
        type: builtins.str,
        enable_logs_sample: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_samples: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        escalation_message: typing.Optional[builtins.str] = None,
        evaluation_delay: typing.Optional[jsii.Number] = None,
        force_delete: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        groupby_simple_monitor: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        group_retention_duration: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        include_tags: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        locked: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        monitor_thresholds: typing.Optional[typing.Union["MonitorMonitorThresholds", typing.Dict[builtins.str, typing.Any]]] = None,
        monitor_threshold_windows: typing.Optional[typing.Union["MonitorMonitorThresholdWindows", typing.Dict[builtins.str, typing.Any]]] = None,
        new_group_delay: typing.Optional[jsii.Number] = None,
        new_host_delay: typing.Optional[jsii.Number] = None,
        no_data_timeframe: typing.Optional[jsii.Number] = None,
        notification_preset_name: typing.Optional[builtins.str] = None,
        notify_audit: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        notify_by: typing.Optional[typing.Sequence[builtins.str]] = None,
        notify_no_data: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        on_missing_data: typing.Optional[builtins.str] = None,
        priority: typing.Optional[builtins.str] = None,
        renotify_interval: typing.Optional[jsii.Number] = None,
        renotify_occurrences: typing.Optional[jsii.Number] = None,
        renotify_statuses: typing.Optional[typing.Sequence[builtins.str]] = None,
        require_full_window: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        restricted_roles: typing.Optional[typing.Sequence[builtins.str]] = None,
        scheduling_options: typing.Optional[typing.Union["MonitorSchedulingOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        tags: typing.Optional[typing.Sequence[builtins.str]] = None,
        timeout_h: typing.Optional[jsii.Number] = None,
        validate: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        variables: typing.Optional[typing.Union["MonitorVariables", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param message: A message to include with notifications for this monitor. Email notifications can be sent to specific users by using the same ``@username`` notation as events. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/monitor#message Monitor#message}
        :param name: Name of Datadog monitor. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/monitor#name Monitor#name}
        :param query: The monitor query to notify on. Note this is not the same query you see in the UI and the syntax is different depending on the monitor type, please see the `API Reference <https://docs.datadoghq.com/api/v1/monitors/#create-a-monitor>`_ for details. ``terraform plan`` will validate query contents unless ``validate`` is set to ``false``. **Note:** APM latency data is now available as Distribution Metrics. Existing monitors have been migrated automatically but all terraformed monitors can still use the existing metrics. We strongly recommend updating monitor definitions to query the new metrics. To learn more, or to see examples of how to update your terraform definitions to utilize the new distribution metrics, see the `detailed doc <https://docs.datadoghq.com/tracing/guide/ddsketch_trace_metrics/>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/monitor#query Monitor#query}
        :param type: The type of the monitor. The mapping from these types to the types found in the Datadog Web UI can be found in the Datadog API `documentation page <https://docs.datadoghq.com/api/v1/monitors/#create-a-monitor>`_. Note: The monitor type cannot be changed after a monitor is created. Valid values are ``composite``, ``event alert``, ``log alert``, ``metric alert``, ``process alert``, ``query alert``, ``rum alert``, ``service check``, ``synthetics alert``, ``trace-analytics alert``, ``slo alert``, ``event-v2 alert``, ``audit alert``, ``ci-pipelines alert``, ``ci-tests alert``, ``error-tracking alert``, ``database-monitoring alert``, ``network-performance alert``, ``cost alert``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/monitor#type Monitor#type}
        :param enable_logs_sample: A boolean indicating whether or not to include a list of log values which triggered the alert. This is only used by log monitors. Defaults to ``false``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/monitor#enable_logs_sample Monitor#enable_logs_sample}
        :param enable_samples: Whether or not a list of samples which triggered the alert is included. This is only used by CI Test and Pipeline monitors. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/monitor#enable_samples Monitor#enable_samples}
        :param escalation_message: A message to include with a re-notification. Supports the ``@username`` notification allowed elsewhere. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/monitor#escalation_message Monitor#escalation_message}
        :param evaluation_delay: (Only applies to metric alert) Time (in seconds) to delay evaluation, as a non-negative integer. For example, if the value is set to ``300`` (5min), the ``timeframe`` is set to ``last_5m`` and the time is 7:00, the monitor will evaluate data from 6:50 to 6:55. This is useful for AWS CloudWatch and other backfilled metrics to ensure the monitor will always have data during evaluation. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/monitor#evaluation_delay Monitor#evaluation_delay}
        :param force_delete: A boolean indicating whether this monitor can be deleted even if it’s referenced by other resources (e.g. SLO, composite monitor). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/monitor#force_delete Monitor#force_delete}
        :param groupby_simple_monitor: Whether or not to trigger one alert if any source breaches a threshold. This is only used by log monitors. Defaults to ``false``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/monitor#groupby_simple_monitor Monitor#groupby_simple_monitor}
        :param group_retention_duration: The time span after which groups with missing data are dropped from the monitor state. The minimum value is one hour, and the maximum value is 72 hours. Example values are: 60m, 1h, and 2d. This option is only available for APM Trace Analytics, Audit Trail, CI, Error Tracking, Event, Logs, and RUM monitors. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/monitor#group_retention_duration Monitor#group_retention_duration}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/monitor#id Monitor#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param include_tags: A boolean indicating whether notifications from this monitor automatically insert its triggering tags into the title. Defaults to ``true``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/monitor#include_tags Monitor#include_tags}
        :param locked: A boolean indicating whether changes to this monitor should be restricted to the creator or admins. Defaults to ``false``. **Deprecated.** Use ``restricted_roles``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/monitor#locked Monitor#locked}
        :param monitor_thresholds: monitor_thresholds block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/monitor#monitor_thresholds Monitor#monitor_thresholds}
        :param monitor_threshold_windows: monitor_threshold_windows block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/monitor#monitor_threshold_windows Monitor#monitor_threshold_windows}
        :param new_group_delay: The time (in seconds) to skip evaluations for new groups. ``new_group_delay`` overrides ``new_host_delay`` if it is set to a nonzero value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/monitor#new_group_delay Monitor#new_group_delay}
        :param new_host_delay: **Deprecated**. See ``new_group_delay``. Time (in seconds) to allow a host to boot and applications to fully start before starting the evaluation of monitor results. Should be a non-negative integer. This value is ignored for simple monitors and monitors not grouped by host. The only case when this should be used is to override the default and set ``new_host_delay`` to zero for monitors grouped by host. **Deprecated.** Use ``new_group_delay`` except when setting ``new_host_delay`` to zero. Defaults to ``300``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/monitor#new_host_delay Monitor#new_host_delay}
        :param no_data_timeframe: The number of minutes before a monitor will notify when data stops reporting. We recommend at least 2x the monitor timeframe for metric alerts or 2 minutes for service checks. Defaults to ``10``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/monitor#no_data_timeframe Monitor#no_data_timeframe}
        :param notification_preset_name: Toggles the display of additional content sent in the monitor notification. Valid values are ``show_all``, ``hide_query``, ``hide_handles``, ``hide_all``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/monitor#notification_preset_name Monitor#notification_preset_name}
        :param notify_audit: A boolean indicating whether tagged users will be notified on changes to this monitor. Defaults to ``false``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/monitor#notify_audit Monitor#notify_audit}
        :param notify_by: Controls what granularity a monitor alerts on. Only available for monitors with groupings. For instance, a monitor grouped by ``cluster``, ``namespace``, and ``pod`` can be configured to only notify on each new ``cluster`` violating the alert conditions by setting ``notify_by`` to ``['cluster']``. Tags mentioned in ``notify_by`` must be a subset of the grouping tags in the query. For example, a query grouped by ``cluster`` and ``namespace`` cannot notify on ``region``. Setting ``notify_by`` to ``[*]`` configures the monitor to notify as a simple-alert. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/monitor#notify_by Monitor#notify_by}
        :param notify_no_data: A boolean indicating whether this monitor will notify when data stops reporting. Defaults to ``false``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/monitor#notify_no_data Monitor#notify_no_data}
        :param on_missing_data: Controls how groups or monitors are treated if an evaluation does not return any data points. The default option results in different behavior depending on the monitor query type. For monitors using ``Count`` queries, an empty monitor evaluation is treated as 0 and is compared to the threshold conditions. For monitors using any query type other than ``Count``, for example ``Gauge``, ``Measure``, or ``Rate``, the monitor shows the last known status. This option is not available for Service Check, Composite, or SLO monitors. Valid values are: ``show_no_data``, ``show_and_notify_no_data``, ``resolve``, and ``default``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/monitor#on_missing_data Monitor#on_missing_data}
        :param priority: Integer from 1 (high) to 5 (low) indicating alert severity. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/monitor#priority Monitor#priority}
        :param renotify_interval: The number of minutes after the last notification before a monitor will re-notify on the current status. It will only re-notify if it's not resolved. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/monitor#renotify_interval Monitor#renotify_interval}
        :param renotify_occurrences: The number of re-notification messages that should be sent on the current status. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/monitor#renotify_occurrences Monitor#renotify_occurrences}
        :param renotify_statuses: The types of statuses for which re-notification messages should be sent. Valid values are ``alert``, ``warn``, ``no data``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/monitor#renotify_statuses Monitor#renotify_statuses}
        :param require_full_window: A boolean indicating whether this monitor needs a full window of data before it's evaluated. Datadog strongly recommends you set this to ``false`` for sparse metrics, otherwise some evaluations may be skipped. If there's a custom_schedule set, ``require_full_window`` must be false and will be ignored. Defaults to ``true``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/monitor#require_full_window Monitor#require_full_window}
        :param restricted_roles: A list of unique role identifiers to define which roles are allowed to edit the monitor. Editing a monitor includes any updates to the monitor configuration, monitor deletion, and muting of the monitor for any amount of time. Roles unique identifiers can be pulled from the `Roles API <https://docs.datadoghq.com/api/latest/roles/#list-roles>`_ in the ``data.id`` field. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/monitor#restricted_roles Monitor#restricted_roles}
        :param scheduling_options: scheduling_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/monitor#scheduling_options Monitor#scheduling_options}
        :param tags: A list of tags to associate with your monitor. This can help you categorize and filter monitors in the manage monitors page of the UI. Note: it's not currently possible to filter by these tags when querying via the API Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/monitor#tags Monitor#tags}
        :param timeout_h: The number of hours of the monitor not reporting data before it automatically resolves from a triggered state. The minimum allowed value is 0 hours. The maximum allowed value is 24 hours. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/monitor#timeout_h Monitor#timeout_h}
        :param validate: If set to ``false``, skip the validation call done during plan. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/monitor#validate Monitor#validate}
        :param variables: variables block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/monitor#variables Monitor#variables}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(monitor_thresholds, dict):
            monitor_thresholds = MonitorMonitorThresholds(**monitor_thresholds)
        if isinstance(monitor_threshold_windows, dict):
            monitor_threshold_windows = MonitorMonitorThresholdWindows(**monitor_threshold_windows)
        if isinstance(scheduling_options, dict):
            scheduling_options = MonitorSchedulingOptions(**scheduling_options)
        if isinstance(variables, dict):
            variables = MonitorVariables(**variables)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7faa180b9afee8042b61effda690ef5720cfbd033bda86d7cd77236264b74315)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument message", value=message, expected_type=type_hints["message"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument query", value=query, expected_type=type_hints["query"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument enable_logs_sample", value=enable_logs_sample, expected_type=type_hints["enable_logs_sample"])
            check_type(argname="argument enable_samples", value=enable_samples, expected_type=type_hints["enable_samples"])
            check_type(argname="argument escalation_message", value=escalation_message, expected_type=type_hints["escalation_message"])
            check_type(argname="argument evaluation_delay", value=evaluation_delay, expected_type=type_hints["evaluation_delay"])
            check_type(argname="argument force_delete", value=force_delete, expected_type=type_hints["force_delete"])
            check_type(argname="argument groupby_simple_monitor", value=groupby_simple_monitor, expected_type=type_hints["groupby_simple_monitor"])
            check_type(argname="argument group_retention_duration", value=group_retention_duration, expected_type=type_hints["group_retention_duration"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument include_tags", value=include_tags, expected_type=type_hints["include_tags"])
            check_type(argname="argument locked", value=locked, expected_type=type_hints["locked"])
            check_type(argname="argument monitor_thresholds", value=monitor_thresholds, expected_type=type_hints["monitor_thresholds"])
            check_type(argname="argument monitor_threshold_windows", value=monitor_threshold_windows, expected_type=type_hints["monitor_threshold_windows"])
            check_type(argname="argument new_group_delay", value=new_group_delay, expected_type=type_hints["new_group_delay"])
            check_type(argname="argument new_host_delay", value=new_host_delay, expected_type=type_hints["new_host_delay"])
            check_type(argname="argument no_data_timeframe", value=no_data_timeframe, expected_type=type_hints["no_data_timeframe"])
            check_type(argname="argument notification_preset_name", value=notification_preset_name, expected_type=type_hints["notification_preset_name"])
            check_type(argname="argument notify_audit", value=notify_audit, expected_type=type_hints["notify_audit"])
            check_type(argname="argument notify_by", value=notify_by, expected_type=type_hints["notify_by"])
            check_type(argname="argument notify_no_data", value=notify_no_data, expected_type=type_hints["notify_no_data"])
            check_type(argname="argument on_missing_data", value=on_missing_data, expected_type=type_hints["on_missing_data"])
            check_type(argname="argument priority", value=priority, expected_type=type_hints["priority"])
            check_type(argname="argument renotify_interval", value=renotify_interval, expected_type=type_hints["renotify_interval"])
            check_type(argname="argument renotify_occurrences", value=renotify_occurrences, expected_type=type_hints["renotify_occurrences"])
            check_type(argname="argument renotify_statuses", value=renotify_statuses, expected_type=type_hints["renotify_statuses"])
            check_type(argname="argument require_full_window", value=require_full_window, expected_type=type_hints["require_full_window"])
            check_type(argname="argument restricted_roles", value=restricted_roles, expected_type=type_hints["restricted_roles"])
            check_type(argname="argument scheduling_options", value=scheduling_options, expected_type=type_hints["scheduling_options"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument timeout_h", value=timeout_h, expected_type=type_hints["timeout_h"])
            check_type(argname="argument validate", value=validate, expected_type=type_hints["validate"])
            check_type(argname="argument variables", value=variables, expected_type=type_hints["variables"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "message": message,
            "name": name,
            "query": query,
            "type": type,
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
        if enable_logs_sample is not None:
            self._values["enable_logs_sample"] = enable_logs_sample
        if enable_samples is not None:
            self._values["enable_samples"] = enable_samples
        if escalation_message is not None:
            self._values["escalation_message"] = escalation_message
        if evaluation_delay is not None:
            self._values["evaluation_delay"] = evaluation_delay
        if force_delete is not None:
            self._values["force_delete"] = force_delete
        if groupby_simple_monitor is not None:
            self._values["groupby_simple_monitor"] = groupby_simple_monitor
        if group_retention_duration is not None:
            self._values["group_retention_duration"] = group_retention_duration
        if id is not None:
            self._values["id"] = id
        if include_tags is not None:
            self._values["include_tags"] = include_tags
        if locked is not None:
            self._values["locked"] = locked
        if monitor_thresholds is not None:
            self._values["monitor_thresholds"] = monitor_thresholds
        if monitor_threshold_windows is not None:
            self._values["monitor_threshold_windows"] = monitor_threshold_windows
        if new_group_delay is not None:
            self._values["new_group_delay"] = new_group_delay
        if new_host_delay is not None:
            self._values["new_host_delay"] = new_host_delay
        if no_data_timeframe is not None:
            self._values["no_data_timeframe"] = no_data_timeframe
        if notification_preset_name is not None:
            self._values["notification_preset_name"] = notification_preset_name
        if notify_audit is not None:
            self._values["notify_audit"] = notify_audit
        if notify_by is not None:
            self._values["notify_by"] = notify_by
        if notify_no_data is not None:
            self._values["notify_no_data"] = notify_no_data
        if on_missing_data is not None:
            self._values["on_missing_data"] = on_missing_data
        if priority is not None:
            self._values["priority"] = priority
        if renotify_interval is not None:
            self._values["renotify_interval"] = renotify_interval
        if renotify_occurrences is not None:
            self._values["renotify_occurrences"] = renotify_occurrences
        if renotify_statuses is not None:
            self._values["renotify_statuses"] = renotify_statuses
        if require_full_window is not None:
            self._values["require_full_window"] = require_full_window
        if restricted_roles is not None:
            self._values["restricted_roles"] = restricted_roles
        if scheduling_options is not None:
            self._values["scheduling_options"] = scheduling_options
        if tags is not None:
            self._values["tags"] = tags
        if timeout_h is not None:
            self._values["timeout_h"] = timeout_h
        if validate is not None:
            self._values["validate"] = validate
        if variables is not None:
            self._values["variables"] = variables

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
    def message(self) -> builtins.str:
        '''A message to include with notifications for this monitor.

        Email notifications can be sent to specific users by using the same ``@username`` notation as events.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/monitor#message Monitor#message}
        '''
        result = self._values.get("message")
        assert result is not None, "Required property 'message' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Name of Datadog monitor.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/monitor#name Monitor#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def query(self) -> builtins.str:
        '''The monitor query to notify on.

        Note this is not the same query you see in the UI and the syntax is different depending on the monitor type, please see the `API Reference <https://docs.datadoghq.com/api/v1/monitors/#create-a-monitor>`_ for details. ``terraform plan`` will validate query contents unless ``validate`` is set to ``false``.

        **Note:** APM latency data is now available as Distribution Metrics. Existing monitors have been migrated automatically but all terraformed monitors can still use the existing metrics. We strongly recommend updating monitor definitions to query the new metrics. To learn more, or to see examples of how to update your terraform definitions to utilize the new distribution metrics, see the `detailed doc <https://docs.datadoghq.com/tracing/guide/ddsketch_trace_metrics/>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/monitor#query Monitor#query}
        '''
        result = self._values.get("query")
        assert result is not None, "Required property 'query' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> builtins.str:
        '''The type of the monitor.

        The mapping from these types to the types found in the Datadog Web UI can be found in the Datadog API `documentation page <https://docs.datadoghq.com/api/v1/monitors/#create-a-monitor>`_. Note: The monitor type cannot be changed after a monitor is created. Valid values are ``composite``, ``event alert``, ``log alert``, ``metric alert``, ``process alert``, ``query alert``, ``rum alert``, ``service check``, ``synthetics alert``, ``trace-analytics alert``, ``slo alert``, ``event-v2 alert``, ``audit alert``, ``ci-pipelines alert``, ``ci-tests alert``, ``error-tracking alert``, ``database-monitoring alert``, ``network-performance alert``, ``cost alert``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/monitor#type Monitor#type}
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def enable_logs_sample(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''A boolean indicating whether or not to include a list of log values which triggered the alert.

        This is only used by log monitors. Defaults to ``false``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/monitor#enable_logs_sample Monitor#enable_logs_sample}
        '''
        result = self._values.get("enable_logs_sample")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def enable_samples(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether or not a list of samples which triggered the alert is included.

        This is only used by CI Test and Pipeline monitors.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/monitor#enable_samples Monitor#enable_samples}
        '''
        result = self._values.get("enable_samples")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def escalation_message(self) -> typing.Optional[builtins.str]:
        '''A message to include with a re-notification. Supports the ``@username`` notification allowed elsewhere.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/monitor#escalation_message Monitor#escalation_message}
        '''
        result = self._values.get("escalation_message")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def evaluation_delay(self) -> typing.Optional[jsii.Number]:
        '''(Only applies to metric alert) Time (in seconds) to delay evaluation, as a non-negative integer.

        For example, if the value is set to ``300`` (5min), the ``timeframe`` is set to ``last_5m`` and the time is 7:00, the monitor will evaluate data from 6:50 to 6:55. This is useful for AWS CloudWatch and other backfilled metrics to ensure the monitor will always have data during evaluation.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/monitor#evaluation_delay Monitor#evaluation_delay}
        '''
        result = self._values.get("evaluation_delay")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def force_delete(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''A boolean indicating whether this monitor can be deleted even if it’s referenced by other resources (e.g. SLO, composite monitor).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/monitor#force_delete Monitor#force_delete}
        '''
        result = self._values.get("force_delete")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def groupby_simple_monitor(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether or not to trigger one alert if any source breaches a threshold.

        This is only used by log monitors. Defaults to ``false``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/monitor#groupby_simple_monitor Monitor#groupby_simple_monitor}
        '''
        result = self._values.get("groupby_simple_monitor")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def group_retention_duration(self) -> typing.Optional[builtins.str]:
        '''The time span after which groups with missing data are dropped from the monitor state.

        The minimum value is one hour, and the maximum value is 72 hours. Example values are: 60m, 1h, and 2d. This option is only available for APM Trace Analytics, Audit Trail, CI, Error Tracking, Event, Logs, and RUM monitors.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/monitor#group_retention_duration Monitor#group_retention_duration}
        '''
        result = self._values.get("group_retention_duration")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/monitor#id Monitor#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def include_tags(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''A boolean indicating whether notifications from this monitor automatically insert its triggering tags into the title. Defaults to ``true``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/monitor#include_tags Monitor#include_tags}
        '''
        result = self._values.get("include_tags")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def locked(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''A boolean indicating whether changes to this monitor should be restricted to the creator or admins.

        Defaults to ``false``. **Deprecated.** Use ``restricted_roles``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/monitor#locked Monitor#locked}
        '''
        result = self._values.get("locked")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def monitor_thresholds(self) -> typing.Optional["MonitorMonitorThresholds"]:
        '''monitor_thresholds block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/monitor#monitor_thresholds Monitor#monitor_thresholds}
        '''
        result = self._values.get("monitor_thresholds")
        return typing.cast(typing.Optional["MonitorMonitorThresholds"], result)

    @builtins.property
    def monitor_threshold_windows(
        self,
    ) -> typing.Optional["MonitorMonitorThresholdWindows"]:
        '''monitor_threshold_windows block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/monitor#monitor_threshold_windows Monitor#monitor_threshold_windows}
        '''
        result = self._values.get("monitor_threshold_windows")
        return typing.cast(typing.Optional["MonitorMonitorThresholdWindows"], result)

    @builtins.property
    def new_group_delay(self) -> typing.Optional[jsii.Number]:
        '''The time (in seconds) to skip evaluations for new groups.

        ``new_group_delay`` overrides ``new_host_delay`` if it is set to a nonzero value.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/monitor#new_group_delay Monitor#new_group_delay}
        '''
        result = self._values.get("new_group_delay")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def new_host_delay(self) -> typing.Optional[jsii.Number]:
        '''**Deprecated**.

        See ``new_group_delay``. Time (in seconds) to allow a host to boot and applications to fully start before starting the evaluation of monitor results. Should be a non-negative integer. This value is ignored for simple monitors and monitors not grouped by host. The only case when this should be used is to override the default and set ``new_host_delay`` to zero for monitors grouped by host. **Deprecated.** Use ``new_group_delay`` except when setting ``new_host_delay`` to zero. Defaults to ``300``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/monitor#new_host_delay Monitor#new_host_delay}
        '''
        result = self._values.get("new_host_delay")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def no_data_timeframe(self) -> typing.Optional[jsii.Number]:
        '''The number of minutes before a monitor will notify when data stops reporting.

        We recommend at least 2x the monitor timeframe for metric alerts or 2 minutes for service checks. Defaults to ``10``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/monitor#no_data_timeframe Monitor#no_data_timeframe}
        '''
        result = self._values.get("no_data_timeframe")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def notification_preset_name(self) -> typing.Optional[builtins.str]:
        '''Toggles the display of additional content sent in the monitor notification. Valid values are ``show_all``, ``hide_query``, ``hide_handles``, ``hide_all``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/monitor#notification_preset_name Monitor#notification_preset_name}
        '''
        result = self._values.get("notification_preset_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def notify_audit(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''A boolean indicating whether tagged users will be notified on changes to this monitor. Defaults to ``false``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/monitor#notify_audit Monitor#notify_audit}
        '''
        result = self._values.get("notify_audit")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def notify_by(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Controls what granularity a monitor alerts on.

        Only available for monitors with groupings. For instance, a monitor grouped by ``cluster``, ``namespace``, and ``pod`` can be configured to only notify on each new ``cluster`` violating the alert conditions by setting ``notify_by`` to ``['cluster']``. Tags mentioned in ``notify_by`` must be a subset of the grouping tags in the query. For example, a query grouped by ``cluster`` and ``namespace`` cannot notify on ``region``. Setting ``notify_by`` to ``[*]`` configures the monitor to notify as a simple-alert.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/monitor#notify_by Monitor#notify_by}
        '''
        result = self._values.get("notify_by")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def notify_no_data(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''A boolean indicating whether this monitor will notify when data stops reporting. Defaults to ``false``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/monitor#notify_no_data Monitor#notify_no_data}
        '''
        result = self._values.get("notify_no_data")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def on_missing_data(self) -> typing.Optional[builtins.str]:
        '''Controls how groups or monitors are treated if an evaluation does not return any data points.

        The default option results in different behavior depending on the monitor query type. For monitors using ``Count`` queries, an empty monitor evaluation is treated as 0 and is compared to the threshold conditions. For monitors using any query type other than ``Count``, for example ``Gauge``, ``Measure``, or ``Rate``, the monitor shows the last known status. This option is not available for Service Check, Composite, or SLO monitors. Valid values are: ``show_no_data``, ``show_and_notify_no_data``, ``resolve``, and ``default``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/monitor#on_missing_data Monitor#on_missing_data}
        '''
        result = self._values.get("on_missing_data")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def priority(self) -> typing.Optional[builtins.str]:
        '''Integer from 1 (high) to 5 (low) indicating alert severity.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/monitor#priority Monitor#priority}
        '''
        result = self._values.get("priority")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def renotify_interval(self) -> typing.Optional[jsii.Number]:
        '''The number of minutes after the last notification before a monitor will re-notify on the current status.

        It will only re-notify if it's not resolved.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/monitor#renotify_interval Monitor#renotify_interval}
        '''
        result = self._values.get("renotify_interval")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def renotify_occurrences(self) -> typing.Optional[jsii.Number]:
        '''The number of re-notification messages that should be sent on the current status.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/monitor#renotify_occurrences Monitor#renotify_occurrences}
        '''
        result = self._values.get("renotify_occurrences")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def renotify_statuses(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The types of statuses for which re-notification messages should be sent. Valid values are ``alert``, ``warn``, ``no data``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/monitor#renotify_statuses Monitor#renotify_statuses}
        '''
        result = self._values.get("renotify_statuses")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def require_full_window(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''A boolean indicating whether this monitor needs a full window of data before it's evaluated.

        Datadog strongly recommends you set this to ``false`` for sparse metrics, otherwise some evaluations may be skipped. If there's a custom_schedule set, ``require_full_window`` must be false and will be ignored. Defaults to ``true``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/monitor#require_full_window Monitor#require_full_window}
        '''
        result = self._values.get("require_full_window")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def restricted_roles(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of unique role identifiers to define which roles are allowed to edit the monitor.

        Editing a monitor includes any updates to the monitor configuration, monitor deletion, and muting of the monitor for any amount of time. Roles unique identifiers can be pulled from the `Roles API <https://docs.datadoghq.com/api/latest/roles/#list-roles>`_ in the ``data.id`` field.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/monitor#restricted_roles Monitor#restricted_roles}
        '''
        result = self._values.get("restricted_roles")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def scheduling_options(self) -> typing.Optional["MonitorSchedulingOptions"]:
        '''scheduling_options block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/monitor#scheduling_options Monitor#scheduling_options}
        '''
        result = self._values.get("scheduling_options")
        return typing.cast(typing.Optional["MonitorSchedulingOptions"], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of tags to associate with your monitor.

        This can help you categorize and filter monitors in the manage monitors page of the UI. Note: it's not currently possible to filter by these tags when querying via the API

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/monitor#tags Monitor#tags}
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def timeout_h(self) -> typing.Optional[jsii.Number]:
        '''The number of hours of the monitor not reporting data before it automatically resolves from a triggered state.

        The minimum allowed value is 0 hours. The maximum allowed value is 24 hours.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/monitor#timeout_h Monitor#timeout_h}
        '''
        result = self._values.get("timeout_h")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def validate(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If set to ``false``, skip the validation call done during plan.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/monitor#validate Monitor#validate}
        '''
        result = self._values.get("validate")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def variables(self) -> typing.Optional["MonitorVariables"]:
        '''variables block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/monitor#variables Monitor#variables}
        '''
        result = self._values.get("variables")
        return typing.cast(typing.Optional["MonitorVariables"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MonitorConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.monitor.MonitorMonitorThresholdWindows",
    jsii_struct_bases=[],
    name_mapping={
        "recovery_window": "recoveryWindow",
        "trigger_window": "triggerWindow",
    },
)
class MonitorMonitorThresholdWindows:
    def __init__(
        self,
        *,
        recovery_window: typing.Optional[builtins.str] = None,
        trigger_window: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param recovery_window: Describes how long an anomalous metric must be normal before the alert recovers. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/monitor#recovery_window Monitor#recovery_window}
        :param trigger_window: Describes how long a metric must be anomalous before an alert triggers. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/monitor#trigger_window Monitor#trigger_window}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5090a351d14e3ba4af4e23891d2be44df0976b0e9c973fbe8b751c57714202f2)
            check_type(argname="argument recovery_window", value=recovery_window, expected_type=type_hints["recovery_window"])
            check_type(argname="argument trigger_window", value=trigger_window, expected_type=type_hints["trigger_window"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if recovery_window is not None:
            self._values["recovery_window"] = recovery_window
        if trigger_window is not None:
            self._values["trigger_window"] = trigger_window

    @builtins.property
    def recovery_window(self) -> typing.Optional[builtins.str]:
        '''Describes how long an anomalous metric must be normal before the alert recovers.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/monitor#recovery_window Monitor#recovery_window}
        '''
        result = self._values.get("recovery_window")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def trigger_window(self) -> typing.Optional[builtins.str]:
        '''Describes how long a metric must be anomalous before an alert triggers.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/monitor#trigger_window Monitor#trigger_window}
        '''
        result = self._values.get("trigger_window")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MonitorMonitorThresholdWindows(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MonitorMonitorThresholdWindowsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.monitor.MonitorMonitorThresholdWindowsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c7a5ab0f7714e0e6ab3de3d3609ddb780090075d5af9bb102affbb50a26476b6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetRecoveryWindow")
    def reset_recovery_window(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRecoveryWindow", []))

    @jsii.member(jsii_name="resetTriggerWindow")
    def reset_trigger_window(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTriggerWindow", []))

    @builtins.property
    @jsii.member(jsii_name="recoveryWindowInput")
    def recovery_window_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "recoveryWindowInput"))

    @builtins.property
    @jsii.member(jsii_name="triggerWindowInput")
    def trigger_window_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "triggerWindowInput"))

    @builtins.property
    @jsii.member(jsii_name="recoveryWindow")
    def recovery_window(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "recoveryWindow"))

    @recovery_window.setter
    def recovery_window(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b42bc67bef784b6cd24a86659e484a3a9d764f216372a9ea41f711f6597244b1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "recoveryWindow", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="triggerWindow")
    def trigger_window(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "triggerWindow"))

    @trigger_window.setter
    def trigger_window(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__140342cc782309dc77adcba30c5279435cca2f305c80af9591d97cfd29f64fad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "triggerWindow", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[MonitorMonitorThresholdWindows]:
        return typing.cast(typing.Optional[MonitorMonitorThresholdWindows], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MonitorMonitorThresholdWindows],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__98cc07efac3c53463156ae1b7843a5610b99ca7ff24c646ae0bb3440acb46e73)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.monitor.MonitorMonitorThresholds",
    jsii_struct_bases=[],
    name_mapping={
        "critical": "critical",
        "critical_recovery": "criticalRecovery",
        "ok": "ok",
        "unknown": "unknown",
        "warning": "warning",
        "warning_recovery": "warningRecovery",
    },
)
class MonitorMonitorThresholds:
    def __init__(
        self,
        *,
        critical: typing.Optional[builtins.str] = None,
        critical_recovery: typing.Optional[builtins.str] = None,
        ok: typing.Optional[builtins.str] = None,
        unknown: typing.Optional[builtins.str] = None,
        warning: typing.Optional[builtins.str] = None,
        warning_recovery: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param critical: The monitor ``CRITICAL`` threshold. Must be a number. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/monitor#critical Monitor#critical}
        :param critical_recovery: The monitor ``CRITICAL`` recovery threshold. Must be a number. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/monitor#critical_recovery Monitor#critical_recovery}
        :param ok: The monitor ``OK`` threshold. Only supported in monitor type ``service check``. Must be a number. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/monitor#ok Monitor#ok}
        :param unknown: The monitor ``UNKNOWN`` threshold. Only supported in monitor type ``service check``. Must be a number. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/monitor#unknown Monitor#unknown}
        :param warning: The monitor ``WARNING`` threshold. Must be a number. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/monitor#warning Monitor#warning}
        :param warning_recovery: The monitor ``WARNING`` recovery threshold. Must be a number. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/monitor#warning_recovery Monitor#warning_recovery}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__460b75a9e4dcba5daa74ae8b30b26be67bfdaab21f25380c72d6f1005c6b6e3c)
            check_type(argname="argument critical", value=critical, expected_type=type_hints["critical"])
            check_type(argname="argument critical_recovery", value=critical_recovery, expected_type=type_hints["critical_recovery"])
            check_type(argname="argument ok", value=ok, expected_type=type_hints["ok"])
            check_type(argname="argument unknown", value=unknown, expected_type=type_hints["unknown"])
            check_type(argname="argument warning", value=warning, expected_type=type_hints["warning"])
            check_type(argname="argument warning_recovery", value=warning_recovery, expected_type=type_hints["warning_recovery"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if critical is not None:
            self._values["critical"] = critical
        if critical_recovery is not None:
            self._values["critical_recovery"] = critical_recovery
        if ok is not None:
            self._values["ok"] = ok
        if unknown is not None:
            self._values["unknown"] = unknown
        if warning is not None:
            self._values["warning"] = warning
        if warning_recovery is not None:
            self._values["warning_recovery"] = warning_recovery

    @builtins.property
    def critical(self) -> typing.Optional[builtins.str]:
        '''The monitor ``CRITICAL`` threshold. Must be a number.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/monitor#critical Monitor#critical}
        '''
        result = self._values.get("critical")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def critical_recovery(self) -> typing.Optional[builtins.str]:
        '''The monitor ``CRITICAL`` recovery threshold. Must be a number.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/monitor#critical_recovery Monitor#critical_recovery}
        '''
        result = self._values.get("critical_recovery")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ok(self) -> typing.Optional[builtins.str]:
        '''The monitor ``OK`` threshold. Only supported in monitor type ``service check``. Must be a number.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/monitor#ok Monitor#ok}
        '''
        result = self._values.get("ok")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def unknown(self) -> typing.Optional[builtins.str]:
        '''The monitor ``UNKNOWN`` threshold. Only supported in monitor type ``service check``. Must be a number.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/monitor#unknown Monitor#unknown}
        '''
        result = self._values.get("unknown")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def warning(self) -> typing.Optional[builtins.str]:
        '''The monitor ``WARNING`` threshold. Must be a number.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/monitor#warning Monitor#warning}
        '''
        result = self._values.get("warning")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def warning_recovery(self) -> typing.Optional[builtins.str]:
        '''The monitor ``WARNING`` recovery threshold. Must be a number.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/monitor#warning_recovery Monitor#warning_recovery}
        '''
        result = self._values.get("warning_recovery")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MonitorMonitorThresholds(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MonitorMonitorThresholdsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.monitor.MonitorMonitorThresholdsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6df1a56663bbb2305ec55be59865a503b4947bd883c0312ad9a2c779c13041f4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCritical")
    def reset_critical(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCritical", []))

    @jsii.member(jsii_name="resetCriticalRecovery")
    def reset_critical_recovery(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCriticalRecovery", []))

    @jsii.member(jsii_name="resetOk")
    def reset_ok(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOk", []))

    @jsii.member(jsii_name="resetUnknown")
    def reset_unknown(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUnknown", []))

    @jsii.member(jsii_name="resetWarning")
    def reset_warning(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWarning", []))

    @jsii.member(jsii_name="resetWarningRecovery")
    def reset_warning_recovery(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWarningRecovery", []))

    @builtins.property
    @jsii.member(jsii_name="criticalInput")
    def critical_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "criticalInput"))

    @builtins.property
    @jsii.member(jsii_name="criticalRecoveryInput")
    def critical_recovery_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "criticalRecoveryInput"))

    @builtins.property
    @jsii.member(jsii_name="okInput")
    def ok_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "okInput"))

    @builtins.property
    @jsii.member(jsii_name="unknownInput")
    def unknown_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "unknownInput"))

    @builtins.property
    @jsii.member(jsii_name="warningInput")
    def warning_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "warningInput"))

    @builtins.property
    @jsii.member(jsii_name="warningRecoveryInput")
    def warning_recovery_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "warningRecoveryInput"))

    @builtins.property
    @jsii.member(jsii_name="critical")
    def critical(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "critical"))

    @critical.setter
    def critical(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__08b41fd4be9f22c9d0bb5459c1ccb594b6b2ef484f7df9c9f68348c4289e880e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "critical", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="criticalRecovery")
    def critical_recovery(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "criticalRecovery"))

    @critical_recovery.setter
    def critical_recovery(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6a869b635289688e12a1c1e848879d2d46a1b4f09d37cd5650325aa8137454fd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "criticalRecovery", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ok")
    def ok(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ok"))

    @ok.setter
    def ok(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c3c7269feef98ad74f4e8542b72875281d68efcb2ee43068e888d7888d7d57ef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ok", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="unknown")
    def unknown(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "unknown"))

    @unknown.setter
    def unknown(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7bd534e2114d3355ebe3dc14d7d504ea0ac6d3acddee65c743ed999c82ad4ab2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "unknown", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="warning")
    def warning(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "warning"))

    @warning.setter
    def warning(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__de0d98d3c28a34a638cc088402aea04fa92043d6b2af106038d5d2eabbfd83dd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "warning", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="warningRecovery")
    def warning_recovery(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "warningRecovery"))

    @warning_recovery.setter
    def warning_recovery(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e386c5849661ed5b9f094caa819207bf3df1d379c3109aa5d9263e05e1a652c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "warningRecovery", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[MonitorMonitorThresholds]:
        return typing.cast(typing.Optional[MonitorMonitorThresholds], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[MonitorMonitorThresholds]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6489dfcb5ea8e4858c24a75636b71156ed9c735fe526b7d6699254ca110cc549)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.monitor.MonitorSchedulingOptions",
    jsii_struct_bases=[],
    name_mapping={
        "custom_schedule": "customSchedule",
        "evaluation_window": "evaluationWindow",
    },
)
class MonitorSchedulingOptions:
    def __init__(
        self,
        *,
        custom_schedule: typing.Optional[typing.Union["MonitorSchedulingOptionsCustomSchedule", typing.Dict[builtins.str, typing.Any]]] = None,
        evaluation_window: typing.Optional[typing.Union["MonitorSchedulingOptionsEvaluationWindow", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param custom_schedule: custom_schedule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/monitor#custom_schedule Monitor#custom_schedule}
        :param evaluation_window: evaluation_window block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/monitor#evaluation_window Monitor#evaluation_window}
        '''
        if isinstance(custom_schedule, dict):
            custom_schedule = MonitorSchedulingOptionsCustomSchedule(**custom_schedule)
        if isinstance(evaluation_window, dict):
            evaluation_window = MonitorSchedulingOptionsEvaluationWindow(**evaluation_window)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__971f06d362dd97d15c156fc933d0f523cec463ca978a0faf96fb0e9654f39abe)
            check_type(argname="argument custom_schedule", value=custom_schedule, expected_type=type_hints["custom_schedule"])
            check_type(argname="argument evaluation_window", value=evaluation_window, expected_type=type_hints["evaluation_window"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if custom_schedule is not None:
            self._values["custom_schedule"] = custom_schedule
        if evaluation_window is not None:
            self._values["evaluation_window"] = evaluation_window

    @builtins.property
    def custom_schedule(
        self,
    ) -> typing.Optional["MonitorSchedulingOptionsCustomSchedule"]:
        '''custom_schedule block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/monitor#custom_schedule Monitor#custom_schedule}
        '''
        result = self._values.get("custom_schedule")
        return typing.cast(typing.Optional["MonitorSchedulingOptionsCustomSchedule"], result)

    @builtins.property
    def evaluation_window(
        self,
    ) -> typing.Optional["MonitorSchedulingOptionsEvaluationWindow"]:
        '''evaluation_window block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/monitor#evaluation_window Monitor#evaluation_window}
        '''
        result = self._values.get("evaluation_window")
        return typing.cast(typing.Optional["MonitorSchedulingOptionsEvaluationWindow"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MonitorSchedulingOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.monitor.MonitorSchedulingOptionsCustomSchedule",
    jsii_struct_bases=[],
    name_mapping={"recurrence": "recurrence"},
)
class MonitorSchedulingOptionsCustomSchedule:
    def __init__(
        self,
        *,
        recurrence: typing.Union["MonitorSchedulingOptionsCustomScheduleRecurrence", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param recurrence: recurrence block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/monitor#recurrence Monitor#recurrence}
        '''
        if isinstance(recurrence, dict):
            recurrence = MonitorSchedulingOptionsCustomScheduleRecurrence(**recurrence)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e167319d29964080baffc837c39b8589c950b56294a2516e8a15eafe6516206)
            check_type(argname="argument recurrence", value=recurrence, expected_type=type_hints["recurrence"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "recurrence": recurrence,
        }

    @builtins.property
    def recurrence(self) -> "MonitorSchedulingOptionsCustomScheduleRecurrence":
        '''recurrence block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/monitor#recurrence Monitor#recurrence}
        '''
        result = self._values.get("recurrence")
        assert result is not None, "Required property 'recurrence' is missing"
        return typing.cast("MonitorSchedulingOptionsCustomScheduleRecurrence", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MonitorSchedulingOptionsCustomSchedule(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MonitorSchedulingOptionsCustomScheduleOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.monitor.MonitorSchedulingOptionsCustomScheduleOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f5ce94940d908f492210f4737d859c94270d887c8a83b5fcc7d16ffe25ddb09b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putRecurrence")
    def put_recurrence(
        self,
        *,
        rrule: builtins.str,
        timezone: builtins.str,
        start: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param rrule: Must be a valid ``rrule``. See API docs for supported fields. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/monitor#rrule Monitor#rrule}
        :param timezone: 'tz database' format. Example: ``America/New_York`` or ``UTC``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/monitor#timezone Monitor#timezone}
        :param start: Time to start recurrence cycle. Similar to DTSTART. Expected format 'YYYY-MM-DDThh:mm:ss'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/monitor#start Monitor#start}
        '''
        value = MonitorSchedulingOptionsCustomScheduleRecurrence(
            rrule=rrule, timezone=timezone, start=start
        )

        return typing.cast(None, jsii.invoke(self, "putRecurrence", [value]))

    @builtins.property
    @jsii.member(jsii_name="recurrence")
    def recurrence(
        self,
    ) -> "MonitorSchedulingOptionsCustomScheduleRecurrenceOutputReference":
        return typing.cast("MonitorSchedulingOptionsCustomScheduleRecurrenceOutputReference", jsii.get(self, "recurrence"))

    @builtins.property
    @jsii.member(jsii_name="recurrenceInput")
    def recurrence_input(
        self,
    ) -> typing.Optional["MonitorSchedulingOptionsCustomScheduleRecurrence"]:
        return typing.cast(typing.Optional["MonitorSchedulingOptionsCustomScheduleRecurrence"], jsii.get(self, "recurrenceInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[MonitorSchedulingOptionsCustomSchedule]:
        return typing.cast(typing.Optional[MonitorSchedulingOptionsCustomSchedule], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MonitorSchedulingOptionsCustomSchedule],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__02f61e7e1bb11bf7f1ca11e78cc9886704abb23800e7f1a9c69b10f0779ebcd2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.monitor.MonitorSchedulingOptionsCustomScheduleRecurrence",
    jsii_struct_bases=[],
    name_mapping={"rrule": "rrule", "timezone": "timezone", "start": "start"},
)
class MonitorSchedulingOptionsCustomScheduleRecurrence:
    def __init__(
        self,
        *,
        rrule: builtins.str,
        timezone: builtins.str,
        start: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param rrule: Must be a valid ``rrule``. See API docs for supported fields. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/monitor#rrule Monitor#rrule}
        :param timezone: 'tz database' format. Example: ``America/New_York`` or ``UTC``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/monitor#timezone Monitor#timezone}
        :param start: Time to start recurrence cycle. Similar to DTSTART. Expected format 'YYYY-MM-DDThh:mm:ss'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/monitor#start Monitor#start}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__546631682346d4655a49e379cc2b3ac338ed6d8900ca4ca019273b5899895cd6)
            check_type(argname="argument rrule", value=rrule, expected_type=type_hints["rrule"])
            check_type(argname="argument timezone", value=timezone, expected_type=type_hints["timezone"])
            check_type(argname="argument start", value=start, expected_type=type_hints["start"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "rrule": rrule,
            "timezone": timezone,
        }
        if start is not None:
            self._values["start"] = start

    @builtins.property
    def rrule(self) -> builtins.str:
        '''Must be a valid ``rrule``. See API docs for supported fields.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/monitor#rrule Monitor#rrule}
        '''
        result = self._values.get("rrule")
        assert result is not None, "Required property 'rrule' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def timezone(self) -> builtins.str:
        ''''tz database' format. Example: ``America/New_York`` or ``UTC``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/monitor#timezone Monitor#timezone}
        '''
        result = self._values.get("timezone")
        assert result is not None, "Required property 'timezone' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def start(self) -> typing.Optional[builtins.str]:
        '''Time to start recurrence cycle. Similar to DTSTART. Expected format 'YYYY-MM-DDThh:mm:ss'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/monitor#start Monitor#start}
        '''
        result = self._values.get("start")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MonitorSchedulingOptionsCustomScheduleRecurrence(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MonitorSchedulingOptionsCustomScheduleRecurrenceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.monitor.MonitorSchedulingOptionsCustomScheduleRecurrenceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bc436e31694278cf3e2996f5e488323eb79882b24c998da0fa6b934863ad6b22)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetStart")
    def reset_start(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStart", []))

    @builtins.property
    @jsii.member(jsii_name="rruleInput")
    def rrule_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "rruleInput"))

    @builtins.property
    @jsii.member(jsii_name="startInput")
    def start_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "startInput"))

    @builtins.property
    @jsii.member(jsii_name="timezoneInput")
    def timezone_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "timezoneInput"))

    @builtins.property
    @jsii.member(jsii_name="rrule")
    def rrule(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "rrule"))

    @rrule.setter
    def rrule(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__11dc38f4558ac3e21d76f4602d66588922b065c8090fca84fe0adec51bf790c9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rrule", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="start")
    def start(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "start"))

    @start.setter
    def start(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__04aa3e93825d2e59556a07dd327d4a681aab5b5abd3bdaa15f6e620506f3ada9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "start", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="timezone")
    def timezone(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "timezone"))

    @timezone.setter
    def timezone(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d6d76f8d2783c5fd361e1681e13a56654a4c3b805234d3646aa2791f3fc6ddf5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timezone", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[MonitorSchedulingOptionsCustomScheduleRecurrence]:
        return typing.cast(typing.Optional[MonitorSchedulingOptionsCustomScheduleRecurrence], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MonitorSchedulingOptionsCustomScheduleRecurrence],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__787210955bcd3b3187dd84713a5013220903e48d62a97b58da4ee86dabd40a5c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.monitor.MonitorSchedulingOptionsEvaluationWindow",
    jsii_struct_bases=[],
    name_mapping={
        "day_starts": "dayStarts",
        "hour_starts": "hourStarts",
        "month_starts": "monthStarts",
    },
)
class MonitorSchedulingOptionsEvaluationWindow:
    def __init__(
        self,
        *,
        day_starts: typing.Optional[builtins.str] = None,
        hour_starts: typing.Optional[jsii.Number] = None,
        month_starts: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param day_starts: The time of the day at which a one day cumulative evaluation window starts. Must be defined in UTC time in ``HH:mm`` format. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/monitor#day_starts Monitor#day_starts}
        :param hour_starts: The minute of the hour at which a one hour cumulative evaluation window starts. Must be between 0 and 59. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/monitor#hour_starts Monitor#hour_starts}
        :param month_starts: The day of the month at which a one month cumulative evaluation window starts. Must be a value of 1. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/monitor#month_starts Monitor#month_starts}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e3140222c30a686e4920eb573311a4874c149b26474dabf65a98172eb07b586)
            check_type(argname="argument day_starts", value=day_starts, expected_type=type_hints["day_starts"])
            check_type(argname="argument hour_starts", value=hour_starts, expected_type=type_hints["hour_starts"])
            check_type(argname="argument month_starts", value=month_starts, expected_type=type_hints["month_starts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if day_starts is not None:
            self._values["day_starts"] = day_starts
        if hour_starts is not None:
            self._values["hour_starts"] = hour_starts
        if month_starts is not None:
            self._values["month_starts"] = month_starts

    @builtins.property
    def day_starts(self) -> typing.Optional[builtins.str]:
        '''The time of the day at which a one day cumulative evaluation window starts.

        Must be defined in UTC time in ``HH:mm`` format.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/monitor#day_starts Monitor#day_starts}
        '''
        result = self._values.get("day_starts")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def hour_starts(self) -> typing.Optional[jsii.Number]:
        '''The minute of the hour at which a one hour cumulative evaluation window starts.

        Must be between 0 and 59.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/monitor#hour_starts Monitor#hour_starts}
        '''
        result = self._values.get("hour_starts")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def month_starts(self) -> typing.Optional[jsii.Number]:
        '''The day of the month at which a one month cumulative evaluation window starts.

        Must be a value of 1.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/monitor#month_starts Monitor#month_starts}
        '''
        result = self._values.get("month_starts")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MonitorSchedulingOptionsEvaluationWindow(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MonitorSchedulingOptionsEvaluationWindowOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.monitor.MonitorSchedulingOptionsEvaluationWindowOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7316d5b1e4225862332ee8f832875fbff62dca041536105e24d1047c5cf7a61a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetDayStarts")
    def reset_day_starts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDayStarts", []))

    @jsii.member(jsii_name="resetHourStarts")
    def reset_hour_starts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHourStarts", []))

    @jsii.member(jsii_name="resetMonthStarts")
    def reset_month_starts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMonthStarts", []))

    @builtins.property
    @jsii.member(jsii_name="dayStartsInput")
    def day_starts_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dayStartsInput"))

    @builtins.property
    @jsii.member(jsii_name="hourStartsInput")
    def hour_starts_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "hourStartsInput"))

    @builtins.property
    @jsii.member(jsii_name="monthStartsInput")
    def month_starts_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "monthStartsInput"))

    @builtins.property
    @jsii.member(jsii_name="dayStarts")
    def day_starts(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dayStarts"))

    @day_starts.setter
    def day_starts(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__df535e4ce82639f04ca3648e8d60aa1ca59ad97b42e52eed8ac8fb7ab481a219)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dayStarts", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="hourStarts")
    def hour_starts(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "hourStarts"))

    @hour_starts.setter
    def hour_starts(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e7f1785a3299ec9df34867d8336b0aaf93be160a53be614167ae48d2de161a31)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hourStarts", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="monthStarts")
    def month_starts(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "monthStarts"))

    @month_starts.setter
    def month_starts(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e5436627f1e4952169e7de67026561f82587cbac9e75f345c3611cdc4f02c1d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "monthStarts", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[MonitorSchedulingOptionsEvaluationWindow]:
        return typing.cast(typing.Optional[MonitorSchedulingOptionsEvaluationWindow], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MonitorSchedulingOptionsEvaluationWindow],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b0a8565e33e4a5b3502426b97b73f4ad52351f9e4f78f7a4b8f33626194aa3c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class MonitorSchedulingOptionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.monitor.MonitorSchedulingOptionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6fe268b70e78fb2caf26091f218f4a29e92722729a47528d5bfd6d06c716093e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putCustomSchedule")
    def put_custom_schedule(
        self,
        *,
        recurrence: typing.Union[MonitorSchedulingOptionsCustomScheduleRecurrence, typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param recurrence: recurrence block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/monitor#recurrence Monitor#recurrence}
        '''
        value = MonitorSchedulingOptionsCustomSchedule(recurrence=recurrence)

        return typing.cast(None, jsii.invoke(self, "putCustomSchedule", [value]))

    @jsii.member(jsii_name="putEvaluationWindow")
    def put_evaluation_window(
        self,
        *,
        day_starts: typing.Optional[builtins.str] = None,
        hour_starts: typing.Optional[jsii.Number] = None,
        month_starts: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param day_starts: The time of the day at which a one day cumulative evaluation window starts. Must be defined in UTC time in ``HH:mm`` format. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/monitor#day_starts Monitor#day_starts}
        :param hour_starts: The minute of the hour at which a one hour cumulative evaluation window starts. Must be between 0 and 59. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/monitor#hour_starts Monitor#hour_starts}
        :param month_starts: The day of the month at which a one month cumulative evaluation window starts. Must be a value of 1. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/monitor#month_starts Monitor#month_starts}
        '''
        value = MonitorSchedulingOptionsEvaluationWindow(
            day_starts=day_starts, hour_starts=hour_starts, month_starts=month_starts
        )

        return typing.cast(None, jsii.invoke(self, "putEvaluationWindow", [value]))

    @jsii.member(jsii_name="resetCustomSchedule")
    def reset_custom_schedule(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCustomSchedule", []))

    @jsii.member(jsii_name="resetEvaluationWindow")
    def reset_evaluation_window(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEvaluationWindow", []))

    @builtins.property
    @jsii.member(jsii_name="customSchedule")
    def custom_schedule(self) -> MonitorSchedulingOptionsCustomScheduleOutputReference:
        return typing.cast(MonitorSchedulingOptionsCustomScheduleOutputReference, jsii.get(self, "customSchedule"))

    @builtins.property
    @jsii.member(jsii_name="evaluationWindow")
    def evaluation_window(
        self,
    ) -> MonitorSchedulingOptionsEvaluationWindowOutputReference:
        return typing.cast(MonitorSchedulingOptionsEvaluationWindowOutputReference, jsii.get(self, "evaluationWindow"))

    @builtins.property
    @jsii.member(jsii_name="customScheduleInput")
    def custom_schedule_input(
        self,
    ) -> typing.Optional[MonitorSchedulingOptionsCustomSchedule]:
        return typing.cast(typing.Optional[MonitorSchedulingOptionsCustomSchedule], jsii.get(self, "customScheduleInput"))

    @builtins.property
    @jsii.member(jsii_name="evaluationWindowInput")
    def evaluation_window_input(
        self,
    ) -> typing.Optional[MonitorSchedulingOptionsEvaluationWindow]:
        return typing.cast(typing.Optional[MonitorSchedulingOptionsEvaluationWindow], jsii.get(self, "evaluationWindowInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[MonitorSchedulingOptions]:
        return typing.cast(typing.Optional[MonitorSchedulingOptions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[MonitorSchedulingOptions]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4cf93e66ebdeb45c97481c2289d0e0dc457f1517b9bd0462a43e2d2d2bb08ede)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.monitor.MonitorVariables",
    jsii_struct_bases=[],
    name_mapping={"cloud_cost_query": "cloudCostQuery", "event_query": "eventQuery"},
)
class MonitorVariables:
    def __init__(
        self,
        *,
        cloud_cost_query: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["MonitorVariablesCloudCostQuery", typing.Dict[builtins.str, typing.Any]]]]] = None,
        event_query: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["MonitorVariablesEventQuery", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param cloud_cost_query: cloud_cost_query block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/monitor#cloud_cost_query Monitor#cloud_cost_query}
        :param event_query: event_query block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/monitor#event_query Monitor#event_query}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0b819e35a1c43482ae486fcab52ee6f3e4d84c1e328719b8030901ffc654e73f)
            check_type(argname="argument cloud_cost_query", value=cloud_cost_query, expected_type=type_hints["cloud_cost_query"])
            check_type(argname="argument event_query", value=event_query, expected_type=type_hints["event_query"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if cloud_cost_query is not None:
            self._values["cloud_cost_query"] = cloud_cost_query
        if event_query is not None:
            self._values["event_query"] = event_query

    @builtins.property
    def cloud_cost_query(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MonitorVariablesCloudCostQuery"]]]:
        '''cloud_cost_query block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/monitor#cloud_cost_query Monitor#cloud_cost_query}
        '''
        result = self._values.get("cloud_cost_query")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MonitorVariablesCloudCostQuery"]]], result)

    @builtins.property
    def event_query(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MonitorVariablesEventQuery"]]]:
        '''event_query block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/monitor#event_query Monitor#event_query}
        '''
        result = self._values.get("event_query")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MonitorVariablesEventQuery"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MonitorVariables(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.monitor.MonitorVariablesCloudCostQuery",
    jsii_struct_bases=[],
    name_mapping={
        "data_source": "dataSource",
        "name": "name",
        "query": "query",
        "aggregator": "aggregator",
    },
)
class MonitorVariablesCloudCostQuery:
    def __init__(
        self,
        *,
        data_source: builtins.str,
        name: builtins.str,
        query: builtins.str,
        aggregator: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param data_source: The data source for cloud cost queries. Valid values are ``metrics``, ``cloud_cost``, ``datadog_usage``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/monitor#data_source Monitor#data_source}
        :param name: The name of the query for use in formulas. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/monitor#name Monitor#name}
        :param query: The cloud cost query definition. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/monitor#query Monitor#query}
        :param aggregator: The aggregation methods available for cloud cost queries. Valid values are ``avg``, ``sum``, ``max``, ``min``, ``last``, ``area``, ``l2norm``, ``percentile``, ``stddev``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/monitor#aggregator Monitor#aggregator}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__927fa7b32530cea599c51ebd0959a85a65c9e5d416785adb9cfe6f5d891417a4)
            check_type(argname="argument data_source", value=data_source, expected_type=type_hints["data_source"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument query", value=query, expected_type=type_hints["query"])
            check_type(argname="argument aggregator", value=aggregator, expected_type=type_hints["aggregator"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "data_source": data_source,
            "name": name,
            "query": query,
        }
        if aggregator is not None:
            self._values["aggregator"] = aggregator

    @builtins.property
    def data_source(self) -> builtins.str:
        '''The data source for cloud cost queries. Valid values are ``metrics``, ``cloud_cost``, ``datadog_usage``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/monitor#data_source Monitor#data_source}
        '''
        result = self._values.get("data_source")
        assert result is not None, "Required property 'data_source' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of the query for use in formulas.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/monitor#name Monitor#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def query(self) -> builtins.str:
        '''The cloud cost query definition.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/monitor#query Monitor#query}
        '''
        result = self._values.get("query")
        assert result is not None, "Required property 'query' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def aggregator(self) -> typing.Optional[builtins.str]:
        '''The aggregation methods available for cloud cost queries.

        Valid values are ``avg``, ``sum``, ``max``, ``min``, ``last``, ``area``, ``l2norm``, ``percentile``, ``stddev``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/monitor#aggregator Monitor#aggregator}
        '''
        result = self._values.get("aggregator")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MonitorVariablesCloudCostQuery(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MonitorVariablesCloudCostQueryList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.monitor.MonitorVariablesCloudCostQueryList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5554f6c885f9cffb343edf17c1b534140b7c222a8f2e37bde09d19f45abc1a34)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "MonitorVariablesCloudCostQueryOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e1044b75af865f2477eb115d8fcb25bf4dba53c8b444852c74e23a72d9b7b5a8)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("MonitorVariablesCloudCostQueryOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__674ea7f45a3cdffdb47cad0040327d74dd968846e7d24a2d257514a8c81c6e3f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__feb14d0c22edb9349482992056222afd5ebdbfdf1594425e30b08cfd64553ca2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1a7e1e6f3a4e0b187220c752840f51b0fe5872b26c1075fb0395240747e2e181)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorVariablesCloudCostQuery]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorVariablesCloudCostQuery]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorVariablesCloudCostQuery]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c2ec13f8788152ebda55a933b09ecc87e48fe570ef6f896d2ff3a385918c8ffa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class MonitorVariablesCloudCostQueryOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.monitor.MonitorVariablesCloudCostQueryOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__493058c831f1c28bf32e57696f7d791e3620d6d824d889cafe94ae29be5019c2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetAggregator")
    def reset_aggregator(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAggregator", []))

    @builtins.property
    @jsii.member(jsii_name="aggregatorInput")
    def aggregator_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "aggregatorInput"))

    @builtins.property
    @jsii.member(jsii_name="dataSourceInput")
    def data_source_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dataSourceInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="queryInput")
    def query_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "queryInput"))

    @builtins.property
    @jsii.member(jsii_name="aggregator")
    def aggregator(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "aggregator"))

    @aggregator.setter
    def aggregator(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c5ed6656407696a3d59608dadfcc2e2233ceface5aa764ee66cfab247bd0141)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "aggregator", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dataSource")
    def data_source(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dataSource"))

    @data_source.setter
    def data_source(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__807504ad27f089cd34953bb3fac438c5bc921b25e3a9317c0fbb9eebf0e4a38c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dataSource", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8b534428269e2863c813ee07d8b73be5bf00ce09e5c6f239dbe3aa3a1cca40fc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="query")
    def query(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "query"))

    @query.setter
    def query(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8778dc8180d415e93056aa8e0864381f68e384db6d5f24d16f499033841846b4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "query", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MonitorVariablesCloudCostQuery]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MonitorVariablesCloudCostQuery]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MonitorVariablesCloudCostQuery]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b01c3f99d4dafd92877730da6f4e8d75f000f1670766ec12fa758fa949ba26b6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.monitor.MonitorVariablesEventQuery",
    jsii_struct_bases=[],
    name_mapping={
        "compute": "compute",
        "data_source": "dataSource",
        "name": "name",
        "search": "search",
        "group_by": "groupBy",
        "indexes": "indexes",
    },
)
class MonitorVariablesEventQuery:
    def __init__(
        self,
        *,
        compute: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["MonitorVariablesEventQueryCompute", typing.Dict[builtins.str, typing.Any]]]],
        data_source: builtins.str,
        name: builtins.str,
        search: typing.Union["MonitorVariablesEventQuerySearch", typing.Dict[builtins.str, typing.Any]],
        group_by: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["MonitorVariablesEventQueryGroupBy", typing.Dict[builtins.str, typing.Any]]]]] = None,
        indexes: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param compute: compute block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/monitor#compute Monitor#compute}
        :param data_source: The data source for event platform-based queries. Valid values are ``rum``, ``ci_pipelines``, ``ci_tests``, ``audit``, ``events``, ``logs``, ``spans``, ``database_queries``, ``network``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/monitor#data_source Monitor#data_source}
        :param name: The name of query for use in formulas. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/monitor#name Monitor#name}
        :param search: search block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/monitor#search Monitor#search}
        :param group_by: group_by block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/monitor#group_by Monitor#group_by}
        :param indexes: An array of index names to query in the stream. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/monitor#indexes Monitor#indexes}
        '''
        if isinstance(search, dict):
            search = MonitorVariablesEventQuerySearch(**search)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a8e256114a402a0eaeff4f7fb11bf9f2ace84fd27c611af87cb3f92be443f625)
            check_type(argname="argument compute", value=compute, expected_type=type_hints["compute"])
            check_type(argname="argument data_source", value=data_source, expected_type=type_hints["data_source"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument search", value=search, expected_type=type_hints["search"])
            check_type(argname="argument group_by", value=group_by, expected_type=type_hints["group_by"])
            check_type(argname="argument indexes", value=indexes, expected_type=type_hints["indexes"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "compute": compute,
            "data_source": data_source,
            "name": name,
            "search": search,
        }
        if group_by is not None:
            self._values["group_by"] = group_by
        if indexes is not None:
            self._values["indexes"] = indexes

    @builtins.property
    def compute(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MonitorVariablesEventQueryCompute"]]:
        '''compute block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/monitor#compute Monitor#compute}
        '''
        result = self._values.get("compute")
        assert result is not None, "Required property 'compute' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MonitorVariablesEventQueryCompute"]], result)

    @builtins.property
    def data_source(self) -> builtins.str:
        '''The data source for event platform-based queries. Valid values are ``rum``, ``ci_pipelines``, ``ci_tests``, ``audit``, ``events``, ``logs``, ``spans``, ``database_queries``, ``network``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/monitor#data_source Monitor#data_source}
        '''
        result = self._values.get("data_source")
        assert result is not None, "Required property 'data_source' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of query for use in formulas.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/monitor#name Monitor#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def search(self) -> "MonitorVariablesEventQuerySearch":
        '''search block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/monitor#search Monitor#search}
        '''
        result = self._values.get("search")
        assert result is not None, "Required property 'search' is missing"
        return typing.cast("MonitorVariablesEventQuerySearch", result)

    @builtins.property
    def group_by(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MonitorVariablesEventQueryGroupBy"]]]:
        '''group_by block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/monitor#group_by Monitor#group_by}
        '''
        result = self._values.get("group_by")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MonitorVariablesEventQueryGroupBy"]]], result)

    @builtins.property
    def indexes(self) -> typing.Optional[typing.List[builtins.str]]:
        '''An array of index names to query in the stream.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/monitor#indexes Monitor#indexes}
        '''
        result = self._values.get("indexes")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MonitorVariablesEventQuery(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.monitor.MonitorVariablesEventQueryCompute",
    jsii_struct_bases=[],
    name_mapping={
        "aggregation": "aggregation",
        "interval": "interval",
        "metric": "metric",
    },
)
class MonitorVariablesEventQueryCompute:
    def __init__(
        self,
        *,
        aggregation: builtins.str,
        interval: typing.Optional[jsii.Number] = None,
        metric: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param aggregation: The aggregation methods for event platform queries. Valid values are ``count``, ``cardinality``, ``median``, ``pc75``, ``pc90``, ``pc95``, ``pc98``, ``pc99``, ``sum``, ``min``, ``max``, ``avg``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/monitor#aggregation Monitor#aggregation}
        :param interval: A time interval in milliseconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/monitor#interval Monitor#interval}
        :param metric: The measurable attribute to compute. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/monitor#metric Monitor#metric}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e3f2b9455ab943e41553db47759acdfe045c3285eb43a51aaaef0b537bdd7fc)
            check_type(argname="argument aggregation", value=aggregation, expected_type=type_hints["aggregation"])
            check_type(argname="argument interval", value=interval, expected_type=type_hints["interval"])
            check_type(argname="argument metric", value=metric, expected_type=type_hints["metric"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "aggregation": aggregation,
        }
        if interval is not None:
            self._values["interval"] = interval
        if metric is not None:
            self._values["metric"] = metric

    @builtins.property
    def aggregation(self) -> builtins.str:
        '''The aggregation methods for event platform queries.

        Valid values are ``count``, ``cardinality``, ``median``, ``pc75``, ``pc90``, ``pc95``, ``pc98``, ``pc99``, ``sum``, ``min``, ``max``, ``avg``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/monitor#aggregation Monitor#aggregation}
        '''
        result = self._values.get("aggregation")
        assert result is not None, "Required property 'aggregation' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def interval(self) -> typing.Optional[jsii.Number]:
        '''A time interval in milliseconds.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/monitor#interval Monitor#interval}
        '''
        result = self._values.get("interval")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def metric(self) -> typing.Optional[builtins.str]:
        '''The measurable attribute to compute.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/monitor#metric Monitor#metric}
        '''
        result = self._values.get("metric")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MonitorVariablesEventQueryCompute(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MonitorVariablesEventQueryComputeList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.monitor.MonitorVariablesEventQueryComputeList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b2d6f3364bc060f864132ccdf2d6dc79ac262877a3e7f53c203aabcb1c6dcb59)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "MonitorVariablesEventQueryComputeOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__53ef4e10beb13491c64c213b107466106a7ac635aac2c7c4c0c2a36dde30d78b)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("MonitorVariablesEventQueryComputeOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__092f670e07c0d72525c0144af7982d0e9ebec0bdd6ce1c7f272fdc33bb39202b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__427c4235fcc1de45b07efae3c0d3d2fa41528aa1bf762e08318ed88ddf038348)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8ff121b4db6fa55a9a75414ba41fe1d5916e991c983cdb77132994a4e8fa07b6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorVariablesEventQueryCompute]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorVariablesEventQueryCompute]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorVariablesEventQueryCompute]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cb4b0977635d0ab53970c50b6611a8434667290312f9b48cff99acb835b57b24)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class MonitorVariablesEventQueryComputeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.monitor.MonitorVariablesEventQueryComputeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__eba9c19d6874b6fe7cb4ca79f0f21cadb9a266869eab77de70d9f91d3eb237d0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetInterval")
    def reset_interval(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInterval", []))

    @jsii.member(jsii_name="resetMetric")
    def reset_metric(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMetric", []))

    @builtins.property
    @jsii.member(jsii_name="aggregationInput")
    def aggregation_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "aggregationInput"))

    @builtins.property
    @jsii.member(jsii_name="intervalInput")
    def interval_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "intervalInput"))

    @builtins.property
    @jsii.member(jsii_name="metricInput")
    def metric_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "metricInput"))

    @builtins.property
    @jsii.member(jsii_name="aggregation")
    def aggregation(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "aggregation"))

    @aggregation.setter
    def aggregation(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8c81f6a9b3b8f79bdc8317b3c1ddfc3527cad889bc7738d534b1a80c3353828b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "aggregation", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="interval")
    def interval(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "interval"))

    @interval.setter
    def interval(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e13473a3f1d57d4db4c66cfcaaedc9e53954800b69d5f913227033c7add9f1a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "interval", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="metric")
    def metric(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "metric"))

    @metric.setter
    def metric(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a1b4cca0aadf91eec5f40bb30c1d2bc4013bc246080ea123417209a181235d8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metric", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MonitorVariablesEventQueryCompute]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MonitorVariablesEventQueryCompute]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MonitorVariablesEventQueryCompute]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f61dd80d420b7844c07c05cccffa8539300c3bfbdf156844091778cd00e10a66)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.monitor.MonitorVariablesEventQueryGroupBy",
    jsii_struct_bases=[],
    name_mapping={"facet": "facet", "limit": "limit", "sort": "sort"},
)
class MonitorVariablesEventQueryGroupBy:
    def __init__(
        self,
        *,
        facet: builtins.str,
        limit: typing.Optional[jsii.Number] = None,
        sort: typing.Optional[typing.Union["MonitorVariablesEventQueryGroupBySort", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param facet: The event facet. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/monitor#facet Monitor#facet}
        :param limit: The number of groups to return. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/monitor#limit Monitor#limit}
        :param sort: sort block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/monitor#sort Monitor#sort}
        '''
        if isinstance(sort, dict):
            sort = MonitorVariablesEventQueryGroupBySort(**sort)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__23278dc2cf485ed3f14d723cb17940244f2eb40386b00919961b2df1ac1841a4)
            check_type(argname="argument facet", value=facet, expected_type=type_hints["facet"])
            check_type(argname="argument limit", value=limit, expected_type=type_hints["limit"])
            check_type(argname="argument sort", value=sort, expected_type=type_hints["sort"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "facet": facet,
        }
        if limit is not None:
            self._values["limit"] = limit
        if sort is not None:
            self._values["sort"] = sort

    @builtins.property
    def facet(self) -> builtins.str:
        '''The event facet.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/monitor#facet Monitor#facet}
        '''
        result = self._values.get("facet")
        assert result is not None, "Required property 'facet' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def limit(self) -> typing.Optional[jsii.Number]:
        '''The number of groups to return.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/monitor#limit Monitor#limit}
        '''
        result = self._values.get("limit")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def sort(self) -> typing.Optional["MonitorVariablesEventQueryGroupBySort"]:
        '''sort block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/monitor#sort Monitor#sort}
        '''
        result = self._values.get("sort")
        return typing.cast(typing.Optional["MonitorVariablesEventQueryGroupBySort"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MonitorVariablesEventQueryGroupBy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MonitorVariablesEventQueryGroupByList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.monitor.MonitorVariablesEventQueryGroupByList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8069cfa5e1ddb9635650f27964df9323942f56c3f7609bf1f1df5d719243bf1f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "MonitorVariablesEventQueryGroupByOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__af7331e2a5c3ace78ebac3c1bf220b1ae67335cec866b10f98a80419fe24bac4)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("MonitorVariablesEventQueryGroupByOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1ddf30d06482e5db8bf56eb5b52549f89229163802867a02e6ff0bf14b604f83)
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
            type_hints = typing.get_type_hints(_typecheckingstub__46c398a3f93fc3a5e0bd3b7d0ee5330ea17439030684f21cd6616c70480281a7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b0d2aececdc955f363706021066f8794e4baa6163bd8663aeec714340ada461b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorVariablesEventQueryGroupBy]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorVariablesEventQueryGroupBy]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorVariablesEventQueryGroupBy]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4448a2038fbe8c2375f5a79aa3aa0c3eab3744a64a4f73b6fb6f7bd72ce4a916)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class MonitorVariablesEventQueryGroupByOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.monitor.MonitorVariablesEventQueryGroupByOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8c38ab5cb89eab71d50ec4937dc2d126b8b201afded857d5b7118b9844983e28)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putSort")
    def put_sort(
        self,
        *,
        aggregation: builtins.str,
        metric: typing.Optional[builtins.str] = None,
        order: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param aggregation: The aggregation methods for the event platform queries. Valid values are ``count``, ``cardinality``, ``median``, ``pc75``, ``pc90``, ``pc95``, ``pc98``, ``pc99``, ``sum``, ``min``, ``max``, ``avg``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/monitor#aggregation Monitor#aggregation}
        :param metric: The metric used for sorting group by results. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/monitor#metric Monitor#metric}
        :param order: Direction of sort. Valid values are ``asc``, ``desc``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/monitor#order Monitor#order}
        '''
        value = MonitorVariablesEventQueryGroupBySort(
            aggregation=aggregation, metric=metric, order=order
        )

        return typing.cast(None, jsii.invoke(self, "putSort", [value]))

    @jsii.member(jsii_name="resetLimit")
    def reset_limit(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLimit", []))

    @jsii.member(jsii_name="resetSort")
    def reset_sort(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSort", []))

    @builtins.property
    @jsii.member(jsii_name="sort")
    def sort(self) -> "MonitorVariablesEventQueryGroupBySortOutputReference":
        return typing.cast("MonitorVariablesEventQueryGroupBySortOutputReference", jsii.get(self, "sort"))

    @builtins.property
    @jsii.member(jsii_name="facetInput")
    def facet_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "facetInput"))

    @builtins.property
    @jsii.member(jsii_name="limitInput")
    def limit_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "limitInput"))

    @builtins.property
    @jsii.member(jsii_name="sortInput")
    def sort_input(self) -> typing.Optional["MonitorVariablesEventQueryGroupBySort"]:
        return typing.cast(typing.Optional["MonitorVariablesEventQueryGroupBySort"], jsii.get(self, "sortInput"))

    @builtins.property
    @jsii.member(jsii_name="facet")
    def facet(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "facet"))

    @facet.setter
    def facet(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ce3c15e5cf35552d1ad4e2fdf80d67f9df8038fade4e3d0a6aa20127bb756c4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "facet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="limit")
    def limit(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "limit"))

    @limit.setter
    def limit(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__93f174cf750eb1c8fc9b7bbb731fa1051c7faa7b56da0d333d77066fce9e7984)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "limit", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MonitorVariablesEventQueryGroupBy]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MonitorVariablesEventQueryGroupBy]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MonitorVariablesEventQueryGroupBy]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a431d9c645980ebb35bdfe2a2d06e67a49da3ac5ab38e74342f3763f22790936)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.monitor.MonitorVariablesEventQueryGroupBySort",
    jsii_struct_bases=[],
    name_mapping={"aggregation": "aggregation", "metric": "metric", "order": "order"},
)
class MonitorVariablesEventQueryGroupBySort:
    def __init__(
        self,
        *,
        aggregation: builtins.str,
        metric: typing.Optional[builtins.str] = None,
        order: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param aggregation: The aggregation methods for the event platform queries. Valid values are ``count``, ``cardinality``, ``median``, ``pc75``, ``pc90``, ``pc95``, ``pc98``, ``pc99``, ``sum``, ``min``, ``max``, ``avg``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/monitor#aggregation Monitor#aggregation}
        :param metric: The metric used for sorting group by results. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/monitor#metric Monitor#metric}
        :param order: Direction of sort. Valid values are ``asc``, ``desc``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/monitor#order Monitor#order}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__83b0d3a2dbacec1e074762ea85b36324602a4cbc8d8037d1d77390874a68da56)
            check_type(argname="argument aggregation", value=aggregation, expected_type=type_hints["aggregation"])
            check_type(argname="argument metric", value=metric, expected_type=type_hints["metric"])
            check_type(argname="argument order", value=order, expected_type=type_hints["order"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "aggregation": aggregation,
        }
        if metric is not None:
            self._values["metric"] = metric
        if order is not None:
            self._values["order"] = order

    @builtins.property
    def aggregation(self) -> builtins.str:
        '''The aggregation methods for the event platform queries.

        Valid values are ``count``, ``cardinality``, ``median``, ``pc75``, ``pc90``, ``pc95``, ``pc98``, ``pc99``, ``sum``, ``min``, ``max``, ``avg``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/monitor#aggregation Monitor#aggregation}
        '''
        result = self._values.get("aggregation")
        assert result is not None, "Required property 'aggregation' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def metric(self) -> typing.Optional[builtins.str]:
        '''The metric used for sorting group by results.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/monitor#metric Monitor#metric}
        '''
        result = self._values.get("metric")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def order(self) -> typing.Optional[builtins.str]:
        '''Direction of sort. Valid values are ``asc``, ``desc``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/monitor#order Monitor#order}
        '''
        result = self._values.get("order")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MonitorVariablesEventQueryGroupBySort(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MonitorVariablesEventQueryGroupBySortOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.monitor.MonitorVariablesEventQueryGroupBySortOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c8f5106ae2ff7670931383b757a31b5837d1585baec0294274a054f1d8fb555f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetMetric")
    def reset_metric(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMetric", []))

    @jsii.member(jsii_name="resetOrder")
    def reset_order(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOrder", []))

    @builtins.property
    @jsii.member(jsii_name="aggregationInput")
    def aggregation_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "aggregationInput"))

    @builtins.property
    @jsii.member(jsii_name="metricInput")
    def metric_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "metricInput"))

    @builtins.property
    @jsii.member(jsii_name="orderInput")
    def order_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "orderInput"))

    @builtins.property
    @jsii.member(jsii_name="aggregation")
    def aggregation(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "aggregation"))

    @aggregation.setter
    def aggregation(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__af8e887f11edd341694d76d87c6560acd672c555369e58a63eb607b40d067d3e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "aggregation", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="metric")
    def metric(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "metric"))

    @metric.setter
    def metric(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c188f7a8e68c8ad9fd92d19a92e730314deab5fc5854f1888f80a9468f1d9de9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metric", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="order")
    def order(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "order"))

    @order.setter
    def order(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b9fc6226883ec8c35c73c44d23fc1bf6930b06923496753452bd171983554e7a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "order", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[MonitorVariablesEventQueryGroupBySort]:
        return typing.cast(typing.Optional[MonitorVariablesEventQueryGroupBySort], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MonitorVariablesEventQueryGroupBySort],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__08745aa71b8fd401064c10ae028dbe6149b394347b1a00705d7b00c5fa7aac99)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class MonitorVariablesEventQueryList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.monitor.MonitorVariablesEventQueryList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fc4fff32c4384c0ed74ebeb3f876016581ee7ac5b9abe1e818b479908ac0e95d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "MonitorVariablesEventQueryOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dfc9b81a38a38933f8e67f1c228d1da7f4eb72726a47e56e63c846ee26cf86f6)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("MonitorVariablesEventQueryOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d438b7e6c8138c789f5215e903d50e60143d5d75cb11a57c9d5249faf3653c8e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e01174b1eb98ec7fc4fa791ad15c5c6f0fcfbb12d2555323b74e94fcb2e30e4d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__17a2d52b1c60feaa7fc50eee7e342dc7fe23021e719d8ab3f13cb64c36ef9cda)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorVariablesEventQuery]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorVariablesEventQuery]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorVariablesEventQuery]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a85999369d5a5647f90a432a3937f9c451440a3eec1de950c5f2cf8489e158bc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class MonitorVariablesEventQueryOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.monitor.MonitorVariablesEventQueryOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__073eed7af2ea7d9c2571673da2859dc27457bb049eb8f9ab14e8182f5c65fdbf)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putCompute")
    def put_compute(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MonitorVariablesEventQueryCompute, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__211b7572e56210e2cc945dc8e3bbb8f6eadd5f6370ead82d2e9f31becabca427)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putCompute", [value]))

    @jsii.member(jsii_name="putGroupBy")
    def put_group_by(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MonitorVariablesEventQueryGroupBy, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4d05e92cfc5a951f34c173c587f36a2f695bfd2cde5ed2e3d09c314f77de0ed1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putGroupBy", [value]))

    @jsii.member(jsii_name="putSearch")
    def put_search(self, *, query: builtins.str) -> None:
        '''
        :param query: The events search string. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/monitor#query Monitor#query}
        '''
        value = MonitorVariablesEventQuerySearch(query=query)

        return typing.cast(None, jsii.invoke(self, "putSearch", [value]))

    @jsii.member(jsii_name="resetGroupBy")
    def reset_group_by(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGroupBy", []))

    @jsii.member(jsii_name="resetIndexes")
    def reset_indexes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIndexes", []))

    @builtins.property
    @jsii.member(jsii_name="compute")
    def compute(self) -> MonitorVariablesEventQueryComputeList:
        return typing.cast(MonitorVariablesEventQueryComputeList, jsii.get(self, "compute"))

    @builtins.property
    @jsii.member(jsii_name="groupBy")
    def group_by(self) -> MonitorVariablesEventQueryGroupByList:
        return typing.cast(MonitorVariablesEventQueryGroupByList, jsii.get(self, "groupBy"))

    @builtins.property
    @jsii.member(jsii_name="search")
    def search(self) -> "MonitorVariablesEventQuerySearchOutputReference":
        return typing.cast("MonitorVariablesEventQuerySearchOutputReference", jsii.get(self, "search"))

    @builtins.property
    @jsii.member(jsii_name="computeInput")
    def compute_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorVariablesEventQueryCompute]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorVariablesEventQueryCompute]]], jsii.get(self, "computeInput"))

    @builtins.property
    @jsii.member(jsii_name="dataSourceInput")
    def data_source_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dataSourceInput"))

    @builtins.property
    @jsii.member(jsii_name="groupByInput")
    def group_by_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorVariablesEventQueryGroupBy]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorVariablesEventQueryGroupBy]]], jsii.get(self, "groupByInput"))

    @builtins.property
    @jsii.member(jsii_name="indexesInput")
    def indexes_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "indexesInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="searchInput")
    def search_input(self) -> typing.Optional["MonitorVariablesEventQuerySearch"]:
        return typing.cast(typing.Optional["MonitorVariablesEventQuerySearch"], jsii.get(self, "searchInput"))

    @builtins.property
    @jsii.member(jsii_name="dataSource")
    def data_source(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dataSource"))

    @data_source.setter
    def data_source(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__02edd241c8793a08d9f3d3fca3771f9314069a1ce432137468b297ed4acd0e12)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dataSource", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="indexes")
    def indexes(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "indexes"))

    @indexes.setter
    def indexes(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5066e305f6bc1f22df5e607a3bbcff5f84f54290ee22013c95963c9533de9be3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "indexes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a2f15bd4eff6161bf143572d0d198de3736068b1fd6d2eab99a498699b3299d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MonitorVariablesEventQuery]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MonitorVariablesEventQuery]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MonitorVariablesEventQuery]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0e359388d7fab10b77b3f13098a55864534037d9448f5a1c177bdd9bd08f26f6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.monitor.MonitorVariablesEventQuerySearch",
    jsii_struct_bases=[],
    name_mapping={"query": "query"},
)
class MonitorVariablesEventQuerySearch:
    def __init__(self, *, query: builtins.str) -> None:
        '''
        :param query: The events search string. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/monitor#query Monitor#query}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d3c97529476e3c66b9024040bbde330fb1280c048c22816ea8cf1a072ada30d6)
            check_type(argname="argument query", value=query, expected_type=type_hints["query"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "query": query,
        }

    @builtins.property
    def query(self) -> builtins.str:
        '''The events search string.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/monitor#query Monitor#query}
        '''
        result = self._values.get("query")
        assert result is not None, "Required property 'query' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MonitorVariablesEventQuerySearch(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MonitorVariablesEventQuerySearchOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.monitor.MonitorVariablesEventQuerySearchOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__37dab745ef4ca27bbb1719155f9cc8631bf27b3c0364df115a0f3c4717c46c2a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2955c97150c92b7ae97b77ab7cae1175a9a5927e100336ef2b7b8878f22354b1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "query", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[MonitorVariablesEventQuerySearch]:
        return typing.cast(typing.Optional[MonitorVariablesEventQuerySearch], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MonitorVariablesEventQuerySearch],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__490a391b73200b8f172fbc219618f9e5a1f4a303282cf6bdc85dde130f406192)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class MonitorVariablesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.monitor.MonitorVariablesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e54e7ce78a4d6c98cdbfacd2c8f1a0fdb48497cb250046978e8f75a6ec5adcde)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putCloudCostQuery")
    def put_cloud_cost_query(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MonitorVariablesCloudCostQuery, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__25954f30ddf388006fb4c103fa45a5f6453c84bc5fd17c9e15ac7475f55d5ae7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putCloudCostQuery", [value]))

    @jsii.member(jsii_name="putEventQuery")
    def put_event_query(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MonitorVariablesEventQuery, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc472e1ff78dbdd688430a60e0b468bd4e3f3eb1aa0adb0188d83f446943497a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putEventQuery", [value]))

    @jsii.member(jsii_name="resetCloudCostQuery")
    def reset_cloud_cost_query(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCloudCostQuery", []))

    @jsii.member(jsii_name="resetEventQuery")
    def reset_event_query(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEventQuery", []))

    @builtins.property
    @jsii.member(jsii_name="cloudCostQuery")
    def cloud_cost_query(self) -> MonitorVariablesCloudCostQueryList:
        return typing.cast(MonitorVariablesCloudCostQueryList, jsii.get(self, "cloudCostQuery"))

    @builtins.property
    @jsii.member(jsii_name="eventQuery")
    def event_query(self) -> MonitorVariablesEventQueryList:
        return typing.cast(MonitorVariablesEventQueryList, jsii.get(self, "eventQuery"))

    @builtins.property
    @jsii.member(jsii_name="cloudCostQueryInput")
    def cloud_cost_query_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorVariablesCloudCostQuery]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorVariablesCloudCostQuery]]], jsii.get(self, "cloudCostQueryInput"))

    @builtins.property
    @jsii.member(jsii_name="eventQueryInput")
    def event_query_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorVariablesEventQuery]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorVariablesEventQuery]]], jsii.get(self, "eventQueryInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[MonitorVariables]:
        return typing.cast(typing.Optional[MonitorVariables], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[MonitorVariables]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e30e785cb52845cc324991355b60056663b9c99645e4fb47e36c40b07ba7e142)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "Monitor",
    "MonitorConfig",
    "MonitorMonitorThresholdWindows",
    "MonitorMonitorThresholdWindowsOutputReference",
    "MonitorMonitorThresholds",
    "MonitorMonitorThresholdsOutputReference",
    "MonitorSchedulingOptions",
    "MonitorSchedulingOptionsCustomSchedule",
    "MonitorSchedulingOptionsCustomScheduleOutputReference",
    "MonitorSchedulingOptionsCustomScheduleRecurrence",
    "MonitorSchedulingOptionsCustomScheduleRecurrenceOutputReference",
    "MonitorSchedulingOptionsEvaluationWindow",
    "MonitorSchedulingOptionsEvaluationWindowOutputReference",
    "MonitorSchedulingOptionsOutputReference",
    "MonitorVariables",
    "MonitorVariablesCloudCostQuery",
    "MonitorVariablesCloudCostQueryList",
    "MonitorVariablesCloudCostQueryOutputReference",
    "MonitorVariablesEventQuery",
    "MonitorVariablesEventQueryCompute",
    "MonitorVariablesEventQueryComputeList",
    "MonitorVariablesEventQueryComputeOutputReference",
    "MonitorVariablesEventQueryGroupBy",
    "MonitorVariablesEventQueryGroupByList",
    "MonitorVariablesEventQueryGroupByOutputReference",
    "MonitorVariablesEventQueryGroupBySort",
    "MonitorVariablesEventQueryGroupBySortOutputReference",
    "MonitorVariablesEventQueryList",
    "MonitorVariablesEventQueryOutputReference",
    "MonitorVariablesEventQuerySearch",
    "MonitorVariablesEventQuerySearchOutputReference",
    "MonitorVariablesOutputReference",
]

publication.publish()

def _typecheckingstub__03d752530da5a500b776a36d7bb2dfc57404c491f23b5196cf52d9deec0a993d(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    message: builtins.str,
    name: builtins.str,
    query: builtins.str,
    type: builtins.str,
    enable_logs_sample: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enable_samples: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    escalation_message: typing.Optional[builtins.str] = None,
    evaluation_delay: typing.Optional[jsii.Number] = None,
    force_delete: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    groupby_simple_monitor: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    group_retention_duration: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    include_tags: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    locked: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    monitor_thresholds: typing.Optional[typing.Union[MonitorMonitorThresholds, typing.Dict[builtins.str, typing.Any]]] = None,
    monitor_threshold_windows: typing.Optional[typing.Union[MonitorMonitorThresholdWindows, typing.Dict[builtins.str, typing.Any]]] = None,
    new_group_delay: typing.Optional[jsii.Number] = None,
    new_host_delay: typing.Optional[jsii.Number] = None,
    no_data_timeframe: typing.Optional[jsii.Number] = None,
    notification_preset_name: typing.Optional[builtins.str] = None,
    notify_audit: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    notify_by: typing.Optional[typing.Sequence[builtins.str]] = None,
    notify_no_data: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    on_missing_data: typing.Optional[builtins.str] = None,
    priority: typing.Optional[builtins.str] = None,
    renotify_interval: typing.Optional[jsii.Number] = None,
    renotify_occurrences: typing.Optional[jsii.Number] = None,
    renotify_statuses: typing.Optional[typing.Sequence[builtins.str]] = None,
    require_full_window: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    restricted_roles: typing.Optional[typing.Sequence[builtins.str]] = None,
    scheduling_options: typing.Optional[typing.Union[MonitorSchedulingOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    tags: typing.Optional[typing.Sequence[builtins.str]] = None,
    timeout_h: typing.Optional[jsii.Number] = None,
    validate: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    variables: typing.Optional[typing.Union[MonitorVariables, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__b15249212d54849270fa62a88a2fc2945d9c971610728df9f77f1dd018583e86(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81f8bf9e49030b5d383d179324967617c80b47d66c25bf8ffca99f3b8d912d39(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8340d3da1a091fa7c96cb62d406689deab438ff63063c1cc368ccc4bc22bcbad(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cdddae296bdc4ca4e7901bae00211aaf3e372b924063de1da6352146817ad3a2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e947460955ee77f41adba167010c6831a68353458127bc53ef62895214186920(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1f22ee04be8d02f3e5f17e4a1fbb7fd5d725cb4424e80c2961159409a189ddc(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__325235c7b12b9fd92cfd8af5e0ef60b3c94a2bc7146b53a6ef88a2241ede1567(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ae82f283395599aa52863ffd23cb17b690d32d223702cb3ccbc707b840abed8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33386788a4cf80d4118761b9dc6165be89c25285d457904aa5d10a271e32afc5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78b1ccab005bd762704465fa121c3e6e6b2841f65caed6a6722614a365f5703a(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29387954e743005838e858cc8ade6f246aca8b7159fea378ad779862ffffb8ca(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c2ca38574b162a31cc2e94a0eec2172022985a90478110641c9339851c1f22c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed18a1d689eacf09c858f1c31d18eb7684ef017871eff9f80d696b164436723a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5518c7add5bc89adf6c937b23dea14e182ff53a5ae77bb797d875ded363cd90(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0fc8c77298456e6070b6ff2abc888af064be80906b002bb5c9ba2fb338556aed(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__357287683238a9286f71794dc0de94d1a95adde6b954d1adf8e4756fccc0d849(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f67009a561d6fe51e8d77d9c4cdd957c5651ecc089b0410d450d1b090e806ba(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ffaf673280b156d724376e2518e7be13c8a49d5820fd148e1835d145921ef8e0(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__245ec3db4d968566c54423a52f811cccb975e906f67bb6bda1a649ecddc492f0(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd4037766595c563bf35d0f7459bd782b91b2c8006fa7f4186fd29cef79790f9(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3a23bf86e1137584d2547b5a79e5d1f5449786664ec8b2a242c40a9ba359200(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dce69cc7a405ce2fc0186e161a1e680cb8c4cd19eb0dc7e668177978ed9cd985(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa3b1655ea5f7a07bf8bdee4922c34100172507557e6491c5f50acf96260408f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1081324b3abca8958c5f0ed25494a029d150e5e28be5fcd79c1e38282647f939(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f364f7da306f36883ebac18f373870fdcdce1d7668cf34291ec05d755305d69(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d9ad5a4d8a5aacc6a36cf757f614acb83c05a6c2280edf39d5f096b2802411f(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b84b707bdaa6bd1a058f696c923aab3bfce769fd39faba082efe25ea6ceea36a(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75d9388eaa7398274281eba434f3342dc23d536cfe6ed6f53cc0dde7739fc21a(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf3f00b724397b82df625731c524cc348b18a9c83d6ea529516a0bbf1b27d12f(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29fb2f8478c7ee4e69c6d1319593ba7656e802d5278a62cb4be71d5b9e09f936(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df5d7430a7b3b60245bc0662ca8db68de84fe87f9d835dfa543f4a924c9a6e96(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a2c3244bee93836af124e02d0fa395c5165449b116b119a7d5db59a6ea731f5(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7faa180b9afee8042b61effda690ef5720cfbd033bda86d7cd77236264b74315(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    message: builtins.str,
    name: builtins.str,
    query: builtins.str,
    type: builtins.str,
    enable_logs_sample: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enable_samples: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    escalation_message: typing.Optional[builtins.str] = None,
    evaluation_delay: typing.Optional[jsii.Number] = None,
    force_delete: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    groupby_simple_monitor: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    group_retention_duration: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    include_tags: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    locked: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    monitor_thresholds: typing.Optional[typing.Union[MonitorMonitorThresholds, typing.Dict[builtins.str, typing.Any]]] = None,
    monitor_threshold_windows: typing.Optional[typing.Union[MonitorMonitorThresholdWindows, typing.Dict[builtins.str, typing.Any]]] = None,
    new_group_delay: typing.Optional[jsii.Number] = None,
    new_host_delay: typing.Optional[jsii.Number] = None,
    no_data_timeframe: typing.Optional[jsii.Number] = None,
    notification_preset_name: typing.Optional[builtins.str] = None,
    notify_audit: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    notify_by: typing.Optional[typing.Sequence[builtins.str]] = None,
    notify_no_data: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    on_missing_data: typing.Optional[builtins.str] = None,
    priority: typing.Optional[builtins.str] = None,
    renotify_interval: typing.Optional[jsii.Number] = None,
    renotify_occurrences: typing.Optional[jsii.Number] = None,
    renotify_statuses: typing.Optional[typing.Sequence[builtins.str]] = None,
    require_full_window: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    restricted_roles: typing.Optional[typing.Sequence[builtins.str]] = None,
    scheduling_options: typing.Optional[typing.Union[MonitorSchedulingOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    tags: typing.Optional[typing.Sequence[builtins.str]] = None,
    timeout_h: typing.Optional[jsii.Number] = None,
    validate: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    variables: typing.Optional[typing.Union[MonitorVariables, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5090a351d14e3ba4af4e23891d2be44df0976b0e9c973fbe8b751c57714202f2(
    *,
    recovery_window: typing.Optional[builtins.str] = None,
    trigger_window: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7a5ab0f7714e0e6ab3de3d3609ddb780090075d5af9bb102affbb50a26476b6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b42bc67bef784b6cd24a86659e484a3a9d764f216372a9ea41f711f6597244b1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__140342cc782309dc77adcba30c5279435cca2f305c80af9591d97cfd29f64fad(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98cc07efac3c53463156ae1b7843a5610b99ca7ff24c646ae0bb3440acb46e73(
    value: typing.Optional[MonitorMonitorThresholdWindows],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__460b75a9e4dcba5daa74ae8b30b26be67bfdaab21f25380c72d6f1005c6b6e3c(
    *,
    critical: typing.Optional[builtins.str] = None,
    critical_recovery: typing.Optional[builtins.str] = None,
    ok: typing.Optional[builtins.str] = None,
    unknown: typing.Optional[builtins.str] = None,
    warning: typing.Optional[builtins.str] = None,
    warning_recovery: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6df1a56663bbb2305ec55be59865a503b4947bd883c0312ad9a2c779c13041f4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__08b41fd4be9f22c9d0bb5459c1ccb594b6b2ef484f7df9c9f68348c4289e880e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a869b635289688e12a1c1e848879d2d46a1b4f09d37cd5650325aa8137454fd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3c7269feef98ad74f4e8542b72875281d68efcb2ee43068e888d7888d7d57ef(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7bd534e2114d3355ebe3dc14d7d504ea0ac6d3acddee65c743ed999c82ad4ab2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de0d98d3c28a34a638cc088402aea04fa92043d6b2af106038d5d2eabbfd83dd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e386c5849661ed5b9f094caa819207bf3df1d379c3109aa5d9263e05e1a652c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6489dfcb5ea8e4858c24a75636b71156ed9c735fe526b7d6699254ca110cc549(
    value: typing.Optional[MonitorMonitorThresholds],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__971f06d362dd97d15c156fc933d0f523cec463ca978a0faf96fb0e9654f39abe(
    *,
    custom_schedule: typing.Optional[typing.Union[MonitorSchedulingOptionsCustomSchedule, typing.Dict[builtins.str, typing.Any]]] = None,
    evaluation_window: typing.Optional[typing.Union[MonitorSchedulingOptionsEvaluationWindow, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e167319d29964080baffc837c39b8589c950b56294a2516e8a15eafe6516206(
    *,
    recurrence: typing.Union[MonitorSchedulingOptionsCustomScheduleRecurrence, typing.Dict[builtins.str, typing.Any]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5ce94940d908f492210f4737d859c94270d887c8a83b5fcc7d16ffe25ddb09b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02f61e7e1bb11bf7f1ca11e78cc9886704abb23800e7f1a9c69b10f0779ebcd2(
    value: typing.Optional[MonitorSchedulingOptionsCustomSchedule],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__546631682346d4655a49e379cc2b3ac338ed6d8900ca4ca019273b5899895cd6(
    *,
    rrule: builtins.str,
    timezone: builtins.str,
    start: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc436e31694278cf3e2996f5e488323eb79882b24c998da0fa6b934863ad6b22(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11dc38f4558ac3e21d76f4602d66588922b065c8090fca84fe0adec51bf790c9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04aa3e93825d2e59556a07dd327d4a681aab5b5abd3bdaa15f6e620506f3ada9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d6d76f8d2783c5fd361e1681e13a56654a4c3b805234d3646aa2791f3fc6ddf5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__787210955bcd3b3187dd84713a5013220903e48d62a97b58da4ee86dabd40a5c(
    value: typing.Optional[MonitorSchedulingOptionsCustomScheduleRecurrence],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e3140222c30a686e4920eb573311a4874c149b26474dabf65a98172eb07b586(
    *,
    day_starts: typing.Optional[builtins.str] = None,
    hour_starts: typing.Optional[jsii.Number] = None,
    month_starts: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7316d5b1e4225862332ee8f832875fbff62dca041536105e24d1047c5cf7a61a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df535e4ce82639f04ca3648e8d60aa1ca59ad97b42e52eed8ac8fb7ab481a219(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7f1785a3299ec9df34867d8336b0aaf93be160a53be614167ae48d2de161a31(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e5436627f1e4952169e7de67026561f82587cbac9e75f345c3611cdc4f02c1d(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b0a8565e33e4a5b3502426b97b73f4ad52351f9e4f78f7a4b8f33626194aa3c(
    value: typing.Optional[MonitorSchedulingOptionsEvaluationWindow],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6fe268b70e78fb2caf26091f218f4a29e92722729a47528d5bfd6d06c716093e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4cf93e66ebdeb45c97481c2289d0e0dc457f1517b9bd0462a43e2d2d2bb08ede(
    value: typing.Optional[MonitorSchedulingOptions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b819e35a1c43482ae486fcab52ee6f3e4d84c1e328719b8030901ffc654e73f(
    *,
    cloud_cost_query: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MonitorVariablesCloudCostQuery, typing.Dict[builtins.str, typing.Any]]]]] = None,
    event_query: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MonitorVariablesEventQuery, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__927fa7b32530cea599c51ebd0959a85a65c9e5d416785adb9cfe6f5d891417a4(
    *,
    data_source: builtins.str,
    name: builtins.str,
    query: builtins.str,
    aggregator: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5554f6c885f9cffb343edf17c1b534140b7c222a8f2e37bde09d19f45abc1a34(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1044b75af865f2477eb115d8fcb25bf4dba53c8b444852c74e23a72d9b7b5a8(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__674ea7f45a3cdffdb47cad0040327d74dd968846e7d24a2d257514a8c81c6e3f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__feb14d0c22edb9349482992056222afd5ebdbfdf1594425e30b08cfd64553ca2(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a7e1e6f3a4e0b187220c752840f51b0fe5872b26c1075fb0395240747e2e181(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2ec13f8788152ebda55a933b09ecc87e48fe570ef6f896d2ff3a385918c8ffa(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorVariablesCloudCostQuery]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__493058c831f1c28bf32e57696f7d791e3620d6d824d889cafe94ae29be5019c2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c5ed6656407696a3d59608dadfcc2e2233ceface5aa764ee66cfab247bd0141(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__807504ad27f089cd34953bb3fac438c5bc921b25e3a9317c0fbb9eebf0e4a38c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b534428269e2863c813ee07d8b73be5bf00ce09e5c6f239dbe3aa3a1cca40fc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8778dc8180d415e93056aa8e0864381f68e384db6d5f24d16f499033841846b4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b01c3f99d4dafd92877730da6f4e8d75f000f1670766ec12fa758fa949ba26b6(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MonitorVariablesCloudCostQuery]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8e256114a402a0eaeff4f7fb11bf9f2ace84fd27c611af87cb3f92be443f625(
    *,
    compute: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MonitorVariablesEventQueryCompute, typing.Dict[builtins.str, typing.Any]]]],
    data_source: builtins.str,
    name: builtins.str,
    search: typing.Union[MonitorVariablesEventQuerySearch, typing.Dict[builtins.str, typing.Any]],
    group_by: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MonitorVariablesEventQueryGroupBy, typing.Dict[builtins.str, typing.Any]]]]] = None,
    indexes: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e3f2b9455ab943e41553db47759acdfe045c3285eb43a51aaaef0b537bdd7fc(
    *,
    aggregation: builtins.str,
    interval: typing.Optional[jsii.Number] = None,
    metric: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b2d6f3364bc060f864132ccdf2d6dc79ac262877a3e7f53c203aabcb1c6dcb59(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53ef4e10beb13491c64c213b107466106a7ac635aac2c7c4c0c2a36dde30d78b(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__092f670e07c0d72525c0144af7982d0e9ebec0bdd6ce1c7f272fdc33bb39202b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__427c4235fcc1de45b07efae3c0d3d2fa41528aa1bf762e08318ed88ddf038348(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ff121b4db6fa55a9a75414ba41fe1d5916e991c983cdb77132994a4e8fa07b6(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb4b0977635d0ab53970c50b6611a8434667290312f9b48cff99acb835b57b24(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorVariablesEventQueryCompute]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eba9c19d6874b6fe7cb4ca79f0f21cadb9a266869eab77de70d9f91d3eb237d0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c81f6a9b3b8f79bdc8317b3c1ddfc3527cad889bc7738d534b1a80c3353828b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e13473a3f1d57d4db4c66cfcaaedc9e53954800b69d5f913227033c7add9f1a(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a1b4cca0aadf91eec5f40bb30c1d2bc4013bc246080ea123417209a181235d8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f61dd80d420b7844c07c05cccffa8539300c3bfbdf156844091778cd00e10a66(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MonitorVariablesEventQueryCompute]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__23278dc2cf485ed3f14d723cb17940244f2eb40386b00919961b2df1ac1841a4(
    *,
    facet: builtins.str,
    limit: typing.Optional[jsii.Number] = None,
    sort: typing.Optional[typing.Union[MonitorVariablesEventQueryGroupBySort, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8069cfa5e1ddb9635650f27964df9323942f56c3f7609bf1f1df5d719243bf1f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af7331e2a5c3ace78ebac3c1bf220b1ae67335cec866b10f98a80419fe24bac4(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ddf30d06482e5db8bf56eb5b52549f89229163802867a02e6ff0bf14b604f83(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46c398a3f93fc3a5e0bd3b7d0ee5330ea17439030684f21cd6616c70480281a7(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0d2aececdc955f363706021066f8794e4baa6163bd8663aeec714340ada461b(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4448a2038fbe8c2375f5a79aa3aa0c3eab3744a64a4f73b6fb6f7bd72ce4a916(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorVariablesEventQueryGroupBy]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c38ab5cb89eab71d50ec4937dc2d126b8b201afded857d5b7118b9844983e28(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ce3c15e5cf35552d1ad4e2fdf80d67f9df8038fade4e3d0a6aa20127bb756c4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93f174cf750eb1c8fc9b7bbb731fa1051c7faa7b56da0d333d77066fce9e7984(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a431d9c645980ebb35bdfe2a2d06e67a49da3ac5ab38e74342f3763f22790936(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MonitorVariablesEventQueryGroupBy]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83b0d3a2dbacec1e074762ea85b36324602a4cbc8d8037d1d77390874a68da56(
    *,
    aggregation: builtins.str,
    metric: typing.Optional[builtins.str] = None,
    order: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8f5106ae2ff7670931383b757a31b5837d1585baec0294274a054f1d8fb555f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af8e887f11edd341694d76d87c6560acd672c555369e58a63eb607b40d067d3e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c188f7a8e68c8ad9fd92d19a92e730314deab5fc5854f1888f80a9468f1d9de9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9fc6226883ec8c35c73c44d23fc1bf6930b06923496753452bd171983554e7a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__08745aa71b8fd401064c10ae028dbe6149b394347b1a00705d7b00c5fa7aac99(
    value: typing.Optional[MonitorVariablesEventQueryGroupBySort],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc4fff32c4384c0ed74ebeb3f876016581ee7ac5b9abe1e818b479908ac0e95d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dfc9b81a38a38933f8e67f1c228d1da7f4eb72726a47e56e63c846ee26cf86f6(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d438b7e6c8138c789f5215e903d50e60143d5d75cb11a57c9d5249faf3653c8e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e01174b1eb98ec7fc4fa791ad15c5c6f0fcfbb12d2555323b74e94fcb2e30e4d(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__17a2d52b1c60feaa7fc50eee7e342dc7fe23021e719d8ab3f13cb64c36ef9cda(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a85999369d5a5647f90a432a3937f9c451440a3eec1de950c5f2cf8489e158bc(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorVariablesEventQuery]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__073eed7af2ea7d9c2571673da2859dc27457bb049eb8f9ab14e8182f5c65fdbf(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__211b7572e56210e2cc945dc8e3bbb8f6eadd5f6370ead82d2e9f31becabca427(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MonitorVariablesEventQueryCompute, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d05e92cfc5a951f34c173c587f36a2f695bfd2cde5ed2e3d09c314f77de0ed1(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MonitorVariablesEventQueryGroupBy, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02edd241c8793a08d9f3d3fca3771f9314069a1ce432137468b297ed4acd0e12(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5066e305f6bc1f22df5e607a3bbcff5f84f54290ee22013c95963c9533de9be3(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a2f15bd4eff6161bf143572d0d198de3736068b1fd6d2eab99a498699b3299d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e359388d7fab10b77b3f13098a55864534037d9448f5a1c177bdd9bd08f26f6(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MonitorVariablesEventQuery]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3c97529476e3c66b9024040bbde330fb1280c048c22816ea8cf1a072ada30d6(
    *,
    query: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37dab745ef4ca27bbb1719155f9cc8631bf27b3c0364df115a0f3c4717c46c2a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2955c97150c92b7ae97b77ab7cae1175a9a5927e100336ef2b7b8878f22354b1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__490a391b73200b8f172fbc219618f9e5a1f4a303282cf6bdc85dde130f406192(
    value: typing.Optional[MonitorVariablesEventQuerySearch],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e54e7ce78a4d6c98cdbfacd2c8f1a0fdb48497cb250046978e8f75a6ec5adcde(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25954f30ddf388006fb4c103fa45a5f6453c84bc5fd17c9e15ac7475f55d5ae7(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MonitorVariablesCloudCostQuery, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc472e1ff78dbdd688430a60e0b468bd4e3f3eb1aa0adb0188d83f446943497a(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MonitorVariablesEventQuery, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e30e785cb52845cc324991355b60056663b9c99645e4fb47e36c40b07ba7e142(
    value: typing.Optional[MonitorVariables],
) -> None:
    """Type checking stubs"""
    pass
