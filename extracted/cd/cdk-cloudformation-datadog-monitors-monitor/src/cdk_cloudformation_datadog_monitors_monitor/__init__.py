'''
# datadog-monitors-monitor

> AWS CDK [L1 construct](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html) and data structures for the [AWS CloudFormation Registry](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/registry.html) type `Datadog::Monitors::Monitor` v4.8.0.

## Description

Datadog Monitor 4.8.0

## Usage

In order to use this library, you will need to activate this AWS CloudFormation Registry type in your account. You can do this via the AWS Management Console or using the [AWS CLI](https://aws.amazon.com/cli/) using the following command:

```sh
aws cloudformation activate-type \
  --type-name Datadog::Monitors::Monitor \
  --publisher-id 7171b96e5d207b947eb72ca9ce05247c246de623 \
  --type RESOURCE \
  --execution-role-arn ROLE-ARN
```

Alternatively:

```sh
aws cloudformation activate-type \
  --public-type-arn arn:aws:cloudformation:us-east-1::type/resource/7171b96e5d207b947eb72ca9ce05247c246de623/Datadog-Monitors-Monitor \
  --execution-role-arn ROLE-ARN
```

You can find more information about activating this type in the [AWS CloudFormation documentation](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/registry-public.html).

## Feedback

This library is auto-generated and published to all supported programming languages by the [cdklabs/cdk-cloudformation](https://github.com/cdklabs/cdk-cloudformation) project based on the API schema published for `Datadog::Monitors::Monitor`.

* Issues related to this generated library should be [reported here](https://github.com/cdklabs/cdk-cloudformation/issues/new?title=Issue+with+%40cdk-cloudformation%2Fdatadog-monitors-monitor+v4.8.0).
* Issues related to `Datadog::Monitors::Monitor` should be reported to the [publisher](undefined).

## License

Distributed under the Apache-2.0 License.
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

from typeguard import check_type

from ._jsii import *

import aws_cdk as _aws_cdk_ceddda9d
import constructs as _constructs_77d1e7e8


class CfnMonitor(
    _aws_cdk_ceddda9d.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdk-cloudformation/datadog-monitors-monitor.CfnMonitor",
):
    '''A CloudFormation ``Datadog::Monitors::Monitor``.

    :cloudformationResource: Datadog::Monitors::Monitor
    :link: http://unknown-url
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        query: builtins.str,
        type: "CfnMonitorPropsType",
        cloudformation_options: typing.Optional[typing.Union["CloudformationOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        creator: typing.Optional[typing.Union["Creator", typing.Dict[builtins.str, typing.Any]]] = None,
        message: typing.Optional[builtins.str] = None,
        multi: typing.Optional[builtins.bool] = None,
        name: typing.Optional[builtins.str] = None,
        options: typing.Optional[typing.Union["MonitorOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        priority: typing.Optional[jsii.Number] = None,
        restricted_roles: typing.Optional[typing.Sequence[builtins.str]] = None,
        tags: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''Create a new ``Datadog::Monitors::Monitor``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param query: The monitor query.
        :param type: The type of the monitor.
        :param cloudformation_options: Cloudformation specific options. This is only used by the Cloudformation resource.
        :param creator: 
        :param message: A message to include with notifications for the monitor.
        :param multi: Whether or not the monitor is multi alert.
        :param name: Name of the monitor.
        :param options: The monitor options.
        :param priority: Integer from 1 (high) to 5 (low) indicating alert severity.
        :param restricted_roles: A list of unique role identifiers to define which roles are allowed to edit the monitor. The unique identifiers for all roles can be pulled from the `Roles API <https://docs.datadoghq.com/api/latest/roles/#list-roles>`_ and are located in the ``data.id`` field. Editing a monitor includes any updates to the monitor configuration, monitor deletion, and muting of the monitor for any amount of time. ``restricted_roles`` is the successor of ``locked``. For more information about ``locked`` and ``restricted_roles``, see the `monitor options docs <https://docs.datadoghq.com/monitors/guide/monitor_api_options/#permissions-options>`_.
        :param tags: Tags associated with the monitor.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f282a849d0258c7c00bf6bb5adfaf5888d8d58a6ea859cf96cb55870363cea9)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnMonitorProps(
            query=query,
            type=type,
            cloudformation_options=cloudformation_options,
            creator=creator,
            message=message,
            multi=multi,
            name=name,
            options=options,
            priority=priority,
            restricted_roles=restricted_roles,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrCreated")
    def attr_created(self) -> builtins.str:
        '''Attribute ``Datadog::Monitors::Monitor.Created``.

        :link: http://unknown-url
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrCreated"))

    @builtins.property
    @jsii.member(jsii_name="attrDeleted")
    def attr_deleted(self) -> builtins.str:
        '''Attribute ``Datadog::Monitors::Monitor.Deleted``.

        :link: http://unknown-url
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrDeleted"))

    @builtins.property
    @jsii.member(jsii_name="attrId")
    def attr_id(self) -> jsii.Number:
        '''Attribute ``Datadog::Monitors::Monitor.Id``.

        :link: http://unknown-url
        '''
        return typing.cast(jsii.Number, jsii.get(self, "attrId"))

    @builtins.property
    @jsii.member(jsii_name="attrModified")
    def attr_modified(self) -> builtins.str:
        '''Attribute ``Datadog::Monitors::Monitor.Modified``.

        :link: http://unknown-url
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrModified"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def props(self) -> "CfnMonitorProps":
        '''Resource props.'''
        return typing.cast("CfnMonitorProps", jsii.get(self, "props"))


@jsii.data_type(
    jsii_type="@cdk-cloudformation/datadog-monitors-monitor.CfnMonitorProps",
    jsii_struct_bases=[],
    name_mapping={
        "query": "query",
        "type": "type",
        "cloudformation_options": "cloudformationOptions",
        "creator": "creator",
        "message": "message",
        "multi": "multi",
        "name": "name",
        "options": "options",
        "priority": "priority",
        "restricted_roles": "restrictedRoles",
        "tags": "tags",
    },
)
class CfnMonitorProps:
    def __init__(
        self,
        *,
        query: builtins.str,
        type: "CfnMonitorPropsType",
        cloudformation_options: typing.Optional[typing.Union["CloudformationOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        creator: typing.Optional[typing.Union["Creator", typing.Dict[builtins.str, typing.Any]]] = None,
        message: typing.Optional[builtins.str] = None,
        multi: typing.Optional[builtins.bool] = None,
        name: typing.Optional[builtins.str] = None,
        options: typing.Optional[typing.Union["MonitorOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        priority: typing.Optional[jsii.Number] = None,
        restricted_roles: typing.Optional[typing.Sequence[builtins.str]] = None,
        tags: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''Datadog Monitor 4.8.0.

        :param query: The monitor query.
        :param type: The type of the monitor.
        :param cloudformation_options: Cloudformation specific options. This is only used by the Cloudformation resource.
        :param creator: 
        :param message: A message to include with notifications for the monitor.
        :param multi: Whether or not the monitor is multi alert.
        :param name: Name of the monitor.
        :param options: The monitor options.
        :param priority: Integer from 1 (high) to 5 (low) indicating alert severity.
        :param restricted_roles: A list of unique role identifiers to define which roles are allowed to edit the monitor. The unique identifiers for all roles can be pulled from the `Roles API <https://docs.datadoghq.com/api/latest/roles/#list-roles>`_ and are located in the ``data.id`` field. Editing a monitor includes any updates to the monitor configuration, monitor deletion, and muting of the monitor for any amount of time. ``restricted_roles`` is the successor of ``locked``. For more information about ``locked`` and ``restricted_roles``, see the `monitor options docs <https://docs.datadoghq.com/monitors/guide/monitor_api_options/#permissions-options>`_.
        :param tags: Tags associated with the monitor.

        :schema: CfnMonitorProps
        '''
        if isinstance(cloudformation_options, dict):
            cloudformation_options = CloudformationOptions(**cloudformation_options)
        if isinstance(creator, dict):
            creator = Creator(**creator)
        if isinstance(options, dict):
            options = MonitorOptions(**options)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b250b503cf3a08db9d357fada826dc16015ba9e60db0e9ae681c949469261fd)
            check_type(argname="argument query", value=query, expected_type=type_hints["query"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument cloudformation_options", value=cloudformation_options, expected_type=type_hints["cloudformation_options"])
            check_type(argname="argument creator", value=creator, expected_type=type_hints["creator"])
            check_type(argname="argument message", value=message, expected_type=type_hints["message"])
            check_type(argname="argument multi", value=multi, expected_type=type_hints["multi"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument options", value=options, expected_type=type_hints["options"])
            check_type(argname="argument priority", value=priority, expected_type=type_hints["priority"])
            check_type(argname="argument restricted_roles", value=restricted_roles, expected_type=type_hints["restricted_roles"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "query": query,
            "type": type,
        }
        if cloudformation_options is not None:
            self._values["cloudformation_options"] = cloudformation_options
        if creator is not None:
            self._values["creator"] = creator
        if message is not None:
            self._values["message"] = message
        if multi is not None:
            self._values["multi"] = multi
        if name is not None:
            self._values["name"] = name
        if options is not None:
            self._values["options"] = options
        if priority is not None:
            self._values["priority"] = priority
        if restricted_roles is not None:
            self._values["restricted_roles"] = restricted_roles
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def query(self) -> builtins.str:
        '''The monitor query.

        :schema: CfnMonitorProps#Query
        '''
        result = self._values.get("query")
        assert result is not None, "Required property 'query' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> "CfnMonitorPropsType":
        '''The type of the monitor.

        :schema: CfnMonitorProps#Type
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast("CfnMonitorPropsType", result)

    @builtins.property
    def cloudformation_options(self) -> typing.Optional["CloudformationOptions"]:
        '''Cloudformation specific options.

        This is only used by the Cloudformation resource.

        :schema: CfnMonitorProps#CloudformationOptions
        '''
        result = self._values.get("cloudformation_options")
        return typing.cast(typing.Optional["CloudformationOptions"], result)

    @builtins.property
    def creator(self) -> typing.Optional["Creator"]:
        '''
        :schema: CfnMonitorProps#Creator
        '''
        result = self._values.get("creator")
        return typing.cast(typing.Optional["Creator"], result)

    @builtins.property
    def message(self) -> typing.Optional[builtins.str]:
        '''A message to include with notifications for the monitor.

        :schema: CfnMonitorProps#Message
        '''
        result = self._values.get("message")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def multi(self) -> typing.Optional[builtins.bool]:
        '''Whether or not the monitor is multi alert.

        :schema: CfnMonitorProps#Multi
        '''
        result = self._values.get("multi")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Name of the monitor.

        :schema: CfnMonitorProps#Name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def options(self) -> typing.Optional["MonitorOptions"]:
        '''The monitor options.

        :schema: CfnMonitorProps#Options
        '''
        result = self._values.get("options")
        return typing.cast(typing.Optional["MonitorOptions"], result)

    @builtins.property
    def priority(self) -> typing.Optional[jsii.Number]:
        '''Integer from 1 (high) to 5 (low) indicating alert severity.

        :schema: CfnMonitorProps#Priority
        '''
        result = self._values.get("priority")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def restricted_roles(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of unique role identifiers to define which roles are allowed to edit the monitor.

        The unique identifiers for all roles can be pulled from the `Roles API <https://docs.datadoghq.com/api/latest/roles/#list-roles>`_ and are located in the ``data.id`` field. Editing a monitor includes any updates to the monitor configuration, monitor deletion, and muting of the monitor for any amount of time. ``restricted_roles`` is the successor of ``locked``. For more information about ``locked`` and ``restricted_roles``, see the `monitor options docs <https://docs.datadoghq.com/monitors/guide/monitor_api_options/#permissions-options>`_.

        :schema: CfnMonitorProps#RestrictedRoles
        '''
        result = self._values.get("restricted_roles")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Tags associated with the monitor.

        :schema: CfnMonitorProps#Tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnMonitorProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(
    jsii_type="@cdk-cloudformation/datadog-monitors-monitor.CfnMonitorPropsType"
)
class CfnMonitorPropsType(enum.Enum):
    '''The type of the monitor.

    :schema: CfnMonitorPropsType
    '''

    AUDIT_ALERT = "AUDIT_ALERT"
    '''audit alert.'''
    COMPOSITE = "COMPOSITE"
    '''composite.'''
    EVENT_ALERT = "EVENT_ALERT"
    '''event alert.'''
    EVENT_HYPHEN_V2_ALERT = "EVENT_HYPHEN_V2_ALERT"
    '''event-v2 alert.'''
    LOG_ALERT = "LOG_ALERT"
    '''log alert.'''
    METRIC_ALERT = "METRIC_ALERT"
    '''metric alert.'''
    PROCESS_ALERT = "PROCESS_ALERT"
    '''process alert.'''
    QUERY_ALERT = "QUERY_ALERT"
    '''query alert.'''
    SERVICE_CHECK = "SERVICE_CHECK"
    '''service check.'''
    SYNTHETICS_ALERT = "SYNTHETICS_ALERT"
    '''synthetics alert.'''
    TRACE_HYPHEN_ANALYTICS_ALERT = "TRACE_HYPHEN_ANALYTICS_ALERT"
    '''trace-analytics alert.'''
    SLO_ALERT = "SLO_ALERT"
    '''slo alert.'''
    RUM_ALERT = "RUM_ALERT"
    '''rum alert.'''
    CI_HYPHEN_PIPELINES_ALERT = "CI_HYPHEN_PIPELINES_ALERT"
    '''ci-pipelines alert.'''
    ERROR_HYPHEN_TRACKING_ALERT = "ERROR_HYPHEN_TRACKING_ALERT"
    '''error-tracking alert.'''
    CI_HYPHEN_TESTS_ALERT = "CI_HYPHEN_TESTS_ALERT"
    '''ci-tests alert.'''


@jsii.data_type(
    jsii_type="@cdk-cloudformation/datadog-monitors-monitor.CloudformationOptions",
    jsii_struct_bases=[],
    name_mapping={"lowercase_query": "lowercaseQuery"},
)
class CloudformationOptions:
    def __init__(
        self,
        *,
        lowercase_query: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param lowercase_query: Whether or not to convert monitor query to lowercase when checking for drift.

        :schema: CloudformationOptions
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__98590a687a31b5d4477e712130bcebbddba886b5dd298e667d974c7f1b680d62)
            check_type(argname="argument lowercase_query", value=lowercase_query, expected_type=type_hints["lowercase_query"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if lowercase_query is not None:
            self._values["lowercase_query"] = lowercase_query

    @builtins.property
    def lowercase_query(self) -> typing.Optional[builtins.bool]:
        '''Whether or not to convert monitor query to lowercase when checking for drift.

        :schema: CloudformationOptions#LowercaseQuery
        '''
        result = self._values.get("lowercase_query")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudformationOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdk-cloudformation/datadog-monitors-monitor.Creator",
    jsii_struct_bases=[],
    name_mapping={"email": "email", "handle": "handle", "name": "name"},
)
class Creator:
    def __init__(
        self,
        *,
        email: typing.Optional[builtins.str] = None,
        handle: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param email: Email of the creator of the monitor.
        :param handle: Handle of the creator of the monitor.
        :param name: Name of the creator of the monitor.

        :schema: Creator
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d5afe2b8f1151f0f40371462dd579b9cfa7efda301b6f260a034f1526916e4b)
            check_type(argname="argument email", value=email, expected_type=type_hints["email"])
            check_type(argname="argument handle", value=handle, expected_type=type_hints["handle"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if email is not None:
            self._values["email"] = email
        if handle is not None:
            self._values["handle"] = handle
        if name is not None:
            self._values["name"] = name

    @builtins.property
    def email(self) -> typing.Optional[builtins.str]:
        '''Email of the creator of the monitor.

        :schema: Creator#Email
        '''
        result = self._values.get("email")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def handle(self) -> typing.Optional[builtins.str]:
        '''Handle of the creator of the monitor.

        :schema: Creator#Handle
        '''
        result = self._values.get("handle")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Name of the creator of the monitor.

        :schema: Creator#Name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Creator(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(
    jsii_type="@cdk-cloudformation/datadog-monitors-monitor.MonitorNotificationPresetName"
)
class MonitorNotificationPresetName(enum.Enum):
    '''Toggles the display of additional content sent in the monitor notification.

    :schema: MonitorNotificationPresetName
    '''

    SHOW_UNDERSCORE_ALL = "SHOW_UNDERSCORE_ALL"
    '''show_all.'''
    HIDE_UNDERSCORE_QUERY = "HIDE_UNDERSCORE_QUERY"
    '''hide_query.'''
    HIDE_UNDERSCORE_HANDLES = "HIDE_UNDERSCORE_HANDLES"
    '''hide_handles.'''
    HIDE_UNDERSCORE_ALL = "HIDE_UNDERSCORE_ALL"
    '''hide_all.'''


@jsii.enum(
    jsii_type="@cdk-cloudformation/datadog-monitors-monitor.MonitorOnMissingData"
)
class MonitorOnMissingData(enum.Enum):
    '''Controls how groups or monitors are treated if an evaluation does not return any data points.

    The default option results in different behavior depending on the monitor query type.
    For monitors using Count queries, an empty monitor evaluation is treated as 0 and is compared to the threshold conditions.
    For monitors using any query type other than Count, for example Gauge, Measure, or Rate, the monitor shows the last known status.
    This option is only available for APM Trace Analytics, Audit Trail, CI, Error Tracking, Event, Logs, and RUM monitors.

    :schema: MonitorOnMissingData
    '''

    DEFAULT = "DEFAULT"
    '''default.'''
    SHOW_UNDERSCORE_NO_UNDERSCORE_DATA = "SHOW_UNDERSCORE_NO_UNDERSCORE_DATA"
    '''show_no_data.'''
    SHOW_UNDERSCORE_AND_UNDERSCORE_NOTIFY_UNDERSCORE_NO_UNDERSCORE_DATA = "SHOW_UNDERSCORE_AND_UNDERSCORE_NOTIFY_UNDERSCORE_NO_UNDERSCORE_DATA"
    '''show_and_notify_no_data.'''
    RESOLVE = "RESOLVE"
    '''resolve.'''


@jsii.data_type(
    jsii_type="@cdk-cloudformation/datadog-monitors-monitor.MonitorOptions",
    jsii_struct_bases=[],
    name_mapping={
        "enable_logs_sample": "enableLogsSample",
        "enable_samples": "enableSamples",
        "escalation_message": "escalationMessage",
        "evaluation_delay": "evaluationDelay",
        "group_retention_duration": "groupRetentionDuration",
        "include_tags": "includeTags",
        "locked": "locked",
        "min_failure_duration": "minFailureDuration",
        "min_location_failed": "minLocationFailed",
        "new_group_delay": "newGroupDelay",
        "new_host_delay": "newHostDelay",
        "no_data_timeframe": "noDataTimeframe",
        "notification_preset_name": "notificationPresetName",
        "notify_audit": "notifyAudit",
        "notify_by": "notifyBy",
        "notify_no_data": "notifyNoData",
        "on_missing_data": "onMissingData",
        "renotify_interval": "renotifyInterval",
        "renotify_occurrences": "renotifyOccurrences",
        "renotify_statuses": "renotifyStatuses",
        "require_full_window": "requireFullWindow",
        "scheduling_options": "schedulingOptions",
        "synthetics_check_id": "syntheticsCheckId",
        "thresholds": "thresholds",
        "threshold_windows": "thresholdWindows",
        "timeout_h": "timeoutH",
        "variables": "variables",
    },
)
class MonitorOptions:
    def __init__(
        self,
        *,
        enable_logs_sample: typing.Optional[builtins.bool] = None,
        enable_samples: typing.Optional[builtins.bool] = None,
        escalation_message: typing.Optional[builtins.str] = None,
        evaluation_delay: typing.Optional[jsii.Number] = None,
        group_retention_duration: typing.Optional[builtins.str] = None,
        include_tags: typing.Optional[builtins.bool] = None,
        locked: typing.Optional[builtins.bool] = None,
        min_failure_duration: typing.Optional[jsii.Number] = None,
        min_location_failed: typing.Optional[jsii.Number] = None,
        new_group_delay: typing.Optional[jsii.Number] = None,
        new_host_delay: typing.Optional[jsii.Number] = None,
        no_data_timeframe: typing.Optional[jsii.Number] = None,
        notification_preset_name: typing.Optional[MonitorNotificationPresetName] = None,
        notify_audit: typing.Optional[builtins.bool] = None,
        notify_by: typing.Optional[typing.Sequence[builtins.str]] = None,
        notify_no_data: typing.Optional[builtins.bool] = None,
        on_missing_data: typing.Optional[MonitorOnMissingData] = None,
        renotify_interval: typing.Optional[jsii.Number] = None,
        renotify_occurrences: typing.Optional[jsii.Number] = None,
        renotify_statuses: typing.Optional[typing.Sequence["MonitorOptionsRenotifyStatuses"]] = None,
        require_full_window: typing.Optional[builtins.bool] = None,
        scheduling_options: typing.Optional[typing.Union["MonitorSchedulingOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        synthetics_check_id: typing.Optional[jsii.Number] = None,
        thresholds: typing.Optional[typing.Union["MonitorThresholds", typing.Dict[builtins.str, typing.Any]]] = None,
        threshold_windows: typing.Optional[typing.Union["MonitorThresholdWindows", typing.Dict[builtins.str, typing.Any]]] = None,
        timeout_h: typing.Optional[jsii.Number] = None,
        variables: typing.Optional[typing.Sequence[typing.Any]] = None,
    ) -> None:
        '''
        :param enable_logs_sample: Whether or not to include a sample of the logs.
        :param enable_samples: Whether or not to send a list of samples when the monitor triggers. This is only used by CI Test and Pipeline monitors.
        :param escalation_message: Message to include with a re-notification when renotify_interval is set.
        :param evaluation_delay: Time in seconds to delay evaluation.
        :param group_retention_duration: The time span after which groups with missing data are dropped from the monitor state. The minimum value is one hour, and the maximum value is 72 hours. Example values are: "60m", "1h", and "2d". This option is only available for APM Trace Analytics, Audit Trail, CI, Error Tracking, Event, Logs, and RUM monitors.
        :param include_tags: Whether or not to include triggering tags into notification title.
        :param locked: Whether or not changes to this monitor should be restricted to the creator or admins.
        :param min_failure_duration: How long the test should be in failure before alerting (integer, number of seconds, max 7200).
        :param min_location_failed: Number of locations allowed to fail before triggering alert.
        :param new_group_delay: Time (in seconds) to skip evaluations for new groups. For example, this option can be used to skip evaluations for new hosts while they initialize. Must be a non negative integer.
        :param new_host_delay: Time in seconds to allow a host to start reporting data before starting the evaluation of monitor results.
        :param no_data_timeframe: Number of minutes data stopped reporting before notifying.
        :param notification_preset_name: 
        :param notify_audit: A Boolean indicating whether tagged users is notified on changes to this monitor.
        :param notify_by: Controls what granularity a monitor alerts on. Only available for monitors with groupings. For instance, a monitor grouped by ``cluster``, ``namespace``, and ``pod`` can be configured to only notify on each new ``cluster`` violating the alert conditions by setting ``notify_by`` to ``["cluster"]``. Tags mentioned in ``notify_by`` must be a subset of the grouping tags in the query. For example, a query grouped by ``cluster`` and ``namespace`` cannot notify on ``region``. Setting ``notify_by`` to ``[*]`` configures the monitor to notify as a simple-alert.
        :param notify_no_data: Whether or not to notify when data stops reporting.
        :param on_missing_data: 
        :param renotify_interval: Number of minutes after the last notification before the monitor re-notifies on the current status.
        :param renotify_occurrences: The number of times re-notification messages should be sent on the current status at the provided re-notification interval.
        :param renotify_statuses: The types of monitor statuses for which re-notification messages are sent.
        :param require_full_window: Whether or not the monitor requires a full window of data before it is evaluated.
        :param scheduling_options: 
        :param synthetics_check_id: ID of the corresponding synthetics check.
        :param thresholds: The threshold definitions.
        :param threshold_windows: The threshold window definitions.
        :param timeout_h: Number of hours of the monitor not reporting data before it automatically resolves.
        :param variables: List of requests that can be used in the monitor query.

        :schema: MonitorOptions
        '''
        if isinstance(scheduling_options, dict):
            scheduling_options = MonitorSchedulingOptions(**scheduling_options)
        if isinstance(thresholds, dict):
            thresholds = MonitorThresholds(**thresholds)
        if isinstance(threshold_windows, dict):
            threshold_windows = MonitorThresholdWindows(**threshold_windows)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__78f4431522a5d2fdafd31ea8fca3d54dc4a7c104d932702aadab68b0c39f8666)
            check_type(argname="argument enable_logs_sample", value=enable_logs_sample, expected_type=type_hints["enable_logs_sample"])
            check_type(argname="argument enable_samples", value=enable_samples, expected_type=type_hints["enable_samples"])
            check_type(argname="argument escalation_message", value=escalation_message, expected_type=type_hints["escalation_message"])
            check_type(argname="argument evaluation_delay", value=evaluation_delay, expected_type=type_hints["evaluation_delay"])
            check_type(argname="argument group_retention_duration", value=group_retention_duration, expected_type=type_hints["group_retention_duration"])
            check_type(argname="argument include_tags", value=include_tags, expected_type=type_hints["include_tags"])
            check_type(argname="argument locked", value=locked, expected_type=type_hints["locked"])
            check_type(argname="argument min_failure_duration", value=min_failure_duration, expected_type=type_hints["min_failure_duration"])
            check_type(argname="argument min_location_failed", value=min_location_failed, expected_type=type_hints["min_location_failed"])
            check_type(argname="argument new_group_delay", value=new_group_delay, expected_type=type_hints["new_group_delay"])
            check_type(argname="argument new_host_delay", value=new_host_delay, expected_type=type_hints["new_host_delay"])
            check_type(argname="argument no_data_timeframe", value=no_data_timeframe, expected_type=type_hints["no_data_timeframe"])
            check_type(argname="argument notification_preset_name", value=notification_preset_name, expected_type=type_hints["notification_preset_name"])
            check_type(argname="argument notify_audit", value=notify_audit, expected_type=type_hints["notify_audit"])
            check_type(argname="argument notify_by", value=notify_by, expected_type=type_hints["notify_by"])
            check_type(argname="argument notify_no_data", value=notify_no_data, expected_type=type_hints["notify_no_data"])
            check_type(argname="argument on_missing_data", value=on_missing_data, expected_type=type_hints["on_missing_data"])
            check_type(argname="argument renotify_interval", value=renotify_interval, expected_type=type_hints["renotify_interval"])
            check_type(argname="argument renotify_occurrences", value=renotify_occurrences, expected_type=type_hints["renotify_occurrences"])
            check_type(argname="argument renotify_statuses", value=renotify_statuses, expected_type=type_hints["renotify_statuses"])
            check_type(argname="argument require_full_window", value=require_full_window, expected_type=type_hints["require_full_window"])
            check_type(argname="argument scheduling_options", value=scheduling_options, expected_type=type_hints["scheduling_options"])
            check_type(argname="argument synthetics_check_id", value=synthetics_check_id, expected_type=type_hints["synthetics_check_id"])
            check_type(argname="argument thresholds", value=thresholds, expected_type=type_hints["thresholds"])
            check_type(argname="argument threshold_windows", value=threshold_windows, expected_type=type_hints["threshold_windows"])
            check_type(argname="argument timeout_h", value=timeout_h, expected_type=type_hints["timeout_h"])
            check_type(argname="argument variables", value=variables, expected_type=type_hints["variables"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if enable_logs_sample is not None:
            self._values["enable_logs_sample"] = enable_logs_sample
        if enable_samples is not None:
            self._values["enable_samples"] = enable_samples
        if escalation_message is not None:
            self._values["escalation_message"] = escalation_message
        if evaluation_delay is not None:
            self._values["evaluation_delay"] = evaluation_delay
        if group_retention_duration is not None:
            self._values["group_retention_duration"] = group_retention_duration
        if include_tags is not None:
            self._values["include_tags"] = include_tags
        if locked is not None:
            self._values["locked"] = locked
        if min_failure_duration is not None:
            self._values["min_failure_duration"] = min_failure_duration
        if min_location_failed is not None:
            self._values["min_location_failed"] = min_location_failed
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
        if renotify_interval is not None:
            self._values["renotify_interval"] = renotify_interval
        if renotify_occurrences is not None:
            self._values["renotify_occurrences"] = renotify_occurrences
        if renotify_statuses is not None:
            self._values["renotify_statuses"] = renotify_statuses
        if require_full_window is not None:
            self._values["require_full_window"] = require_full_window
        if scheduling_options is not None:
            self._values["scheduling_options"] = scheduling_options
        if synthetics_check_id is not None:
            self._values["synthetics_check_id"] = synthetics_check_id
        if thresholds is not None:
            self._values["thresholds"] = thresholds
        if threshold_windows is not None:
            self._values["threshold_windows"] = threshold_windows
        if timeout_h is not None:
            self._values["timeout_h"] = timeout_h
        if variables is not None:
            self._values["variables"] = variables

    @builtins.property
    def enable_logs_sample(self) -> typing.Optional[builtins.bool]:
        '''Whether or not to include a sample of the logs.

        :schema: MonitorOptions#EnableLogsSample
        '''
        result = self._values.get("enable_logs_sample")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def enable_samples(self) -> typing.Optional[builtins.bool]:
        '''Whether or not to send a list of samples when the monitor triggers.

        This is only used by CI Test and Pipeline monitors.

        :schema: MonitorOptions#EnableSamples
        '''
        result = self._values.get("enable_samples")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def escalation_message(self) -> typing.Optional[builtins.str]:
        '''Message to include with a re-notification when renotify_interval is set.

        :schema: MonitorOptions#EscalationMessage
        '''
        result = self._values.get("escalation_message")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def evaluation_delay(self) -> typing.Optional[jsii.Number]:
        '''Time in seconds to delay evaluation.

        :schema: MonitorOptions#EvaluationDelay
        '''
        result = self._values.get("evaluation_delay")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def group_retention_duration(self) -> typing.Optional[builtins.str]:
        '''The time span after which groups with missing data are dropped from the monitor state.

        The minimum value is one hour, and the maximum value is 72 hours.
        Example values are: "60m", "1h", and "2d".
        This option is only available for APM Trace Analytics, Audit Trail, CI, Error Tracking, Event, Logs, and RUM monitors.

        :schema: MonitorOptions#GroupRetentionDuration
        '''
        result = self._values.get("group_retention_duration")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def include_tags(self) -> typing.Optional[builtins.bool]:
        '''Whether or not to include triggering tags into notification title.

        :schema: MonitorOptions#IncludeTags
        '''
        result = self._values.get("include_tags")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def locked(self) -> typing.Optional[builtins.bool]:
        '''Whether or not changes to this monitor should be restricted to the creator or admins.

        :schema: MonitorOptions#Locked
        '''
        result = self._values.get("locked")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def min_failure_duration(self) -> typing.Optional[jsii.Number]:
        '''How long the test should be in failure before alerting (integer, number of seconds, max 7200).

        :schema: MonitorOptions#MinFailureDuration
        '''
        result = self._values.get("min_failure_duration")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def min_location_failed(self) -> typing.Optional[jsii.Number]:
        '''Number of locations allowed to fail before triggering alert.

        :schema: MonitorOptions#MinLocationFailed
        '''
        result = self._values.get("min_location_failed")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def new_group_delay(self) -> typing.Optional[jsii.Number]:
        '''Time (in seconds) to skip evaluations for new groups.

        For example, this option can be used to skip evaluations for new hosts while they initialize. Must be a non negative integer.

        :schema: MonitorOptions#NewGroupDelay
        '''
        result = self._values.get("new_group_delay")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def new_host_delay(self) -> typing.Optional[jsii.Number]:
        '''Time in seconds to allow a host to start reporting data before starting the evaluation of monitor results.

        :schema: MonitorOptions#NewHostDelay
        '''
        result = self._values.get("new_host_delay")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def no_data_timeframe(self) -> typing.Optional[jsii.Number]:
        '''Number of minutes data stopped reporting before notifying.

        :schema: MonitorOptions#NoDataTimeframe
        '''
        result = self._values.get("no_data_timeframe")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def notification_preset_name(
        self,
    ) -> typing.Optional[MonitorNotificationPresetName]:
        '''
        :schema: MonitorOptions#NotificationPresetName
        '''
        result = self._values.get("notification_preset_name")
        return typing.cast(typing.Optional[MonitorNotificationPresetName], result)

    @builtins.property
    def notify_audit(self) -> typing.Optional[builtins.bool]:
        '''A Boolean indicating whether tagged users is notified on changes to this monitor.

        :schema: MonitorOptions#NotifyAudit
        '''
        result = self._values.get("notify_audit")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def notify_by(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Controls what granularity a monitor alerts on.

        Only available for monitors with groupings.
        For instance, a monitor grouped by ``cluster``, ``namespace``, and ``pod`` can be configured to only notify on each new ``cluster`` violating the alert conditions by setting ``notify_by`` to ``["cluster"]``.
        Tags mentioned in ``notify_by`` must be a subset of the grouping tags in the query.
        For example, a query grouped by ``cluster`` and ``namespace`` cannot notify on ``region``.
        Setting ``notify_by`` to ``[*]`` configures the monitor to notify as a simple-alert.

        :schema: MonitorOptions#NotifyBy
        '''
        result = self._values.get("notify_by")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def notify_no_data(self) -> typing.Optional[builtins.bool]:
        '''Whether or not to notify when data stops reporting.

        :schema: MonitorOptions#NotifyNoData
        '''
        result = self._values.get("notify_no_data")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def on_missing_data(self) -> typing.Optional[MonitorOnMissingData]:
        '''
        :schema: MonitorOptions#OnMissingData
        '''
        result = self._values.get("on_missing_data")
        return typing.cast(typing.Optional[MonitorOnMissingData], result)

    @builtins.property
    def renotify_interval(self) -> typing.Optional[jsii.Number]:
        '''Number of minutes after the last notification before the monitor re-notifies on the current status.

        :schema: MonitorOptions#RenotifyInterval
        '''
        result = self._values.get("renotify_interval")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def renotify_occurrences(self) -> typing.Optional[jsii.Number]:
        '''The number of times re-notification messages should be sent on the current status at the provided re-notification interval.

        :schema: MonitorOptions#RenotifyOccurrences
        '''
        result = self._values.get("renotify_occurrences")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def renotify_statuses(
        self,
    ) -> typing.Optional[typing.List["MonitorOptionsRenotifyStatuses"]]:
        '''The types of monitor statuses for which re-notification messages are sent.

        :schema: MonitorOptions#RenotifyStatuses
        '''
        result = self._values.get("renotify_statuses")
        return typing.cast(typing.Optional[typing.List["MonitorOptionsRenotifyStatuses"]], result)

    @builtins.property
    def require_full_window(self) -> typing.Optional[builtins.bool]:
        '''Whether or not the monitor requires a full window of data before it is evaluated.

        :schema: MonitorOptions#RequireFullWindow
        '''
        result = self._values.get("require_full_window")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def scheduling_options(self) -> typing.Optional["MonitorSchedulingOptions"]:
        '''
        :schema: MonitorOptions#SchedulingOptions
        '''
        result = self._values.get("scheduling_options")
        return typing.cast(typing.Optional["MonitorSchedulingOptions"], result)

    @builtins.property
    def synthetics_check_id(self) -> typing.Optional[jsii.Number]:
        '''ID of the corresponding synthetics check.

        :schema: MonitorOptions#SyntheticsCheckID
        '''
        result = self._values.get("synthetics_check_id")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def thresholds(self) -> typing.Optional["MonitorThresholds"]:
        '''The threshold definitions.

        :schema: MonitorOptions#Thresholds
        '''
        result = self._values.get("thresholds")
        return typing.cast(typing.Optional["MonitorThresholds"], result)

    @builtins.property
    def threshold_windows(self) -> typing.Optional["MonitorThresholdWindows"]:
        '''The threshold window definitions.

        :schema: MonitorOptions#ThresholdWindows
        '''
        result = self._values.get("threshold_windows")
        return typing.cast(typing.Optional["MonitorThresholdWindows"], result)

    @builtins.property
    def timeout_h(self) -> typing.Optional[jsii.Number]:
        '''Number of hours of the monitor not reporting data before it automatically resolves.

        :schema: MonitorOptions#TimeoutH
        '''
        result = self._values.get("timeout_h")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def variables(self) -> typing.Optional[typing.List[typing.Any]]:
        '''List of requests that can be used in the monitor query.

        :schema: MonitorOptions#Variables
        '''
        result = self._values.get("variables")
        return typing.cast(typing.Optional[typing.List[typing.Any]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MonitorOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(
    jsii_type="@cdk-cloudformation/datadog-monitors-monitor.MonitorOptionsRenotifyStatuses"
)
class MonitorOptionsRenotifyStatuses(enum.Enum):
    '''
    :schema: MonitorOptionsRenotifyStatuses
    '''

    ALERT = "ALERT"
    '''alert.'''
    NO_DATA = "NO_DATA"
    '''no data.'''
    WARN = "WARN"
    '''warn.'''


@jsii.data_type(
    jsii_type="@cdk-cloudformation/datadog-monitors-monitor.MonitorSchedulingOptions",
    jsii_struct_bases=[],
    name_mapping={"evaluation_window": "evaluationWindow"},
)
class MonitorSchedulingOptions:
    def __init__(
        self,
        *,
        evaluation_window: typing.Optional[typing.Union["MonitorSchedulingOptionsEvaluationWindow", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''Configuration options for scheduling.

        :param evaluation_window: 

        :schema: MonitorSchedulingOptions
        '''
        if isinstance(evaluation_window, dict):
            evaluation_window = MonitorSchedulingOptionsEvaluationWindow(**evaluation_window)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__df3bd89691b70fe1f6861c110d4d796b098ad9203d69d599177be23be28d32c3)
            check_type(argname="argument evaluation_window", value=evaluation_window, expected_type=type_hints["evaluation_window"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if evaluation_window is not None:
            self._values["evaluation_window"] = evaluation_window

    @builtins.property
    def evaluation_window(
        self,
    ) -> typing.Optional["MonitorSchedulingOptionsEvaluationWindow"]:
        '''
        :schema: MonitorSchedulingOptions#EvaluationWindow
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
    jsii_type="@cdk-cloudformation/datadog-monitors-monitor.MonitorSchedulingOptionsEvaluationWindow",
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
        '''Configuration options for the evaluation window.

        If ``hour_starts`` is set, no other fields may be set. Otherwise, ``day_starts`` and ``month_starts`` must be set together.

        :param day_starts: The time of the day at which a one day cumulative evaluation window starts. Must be defined in UTC time in ``HH:mm`` format.
        :param hour_starts: The minute of the hour at which a one hour cumulative evaluation window starts.
        :param month_starts: The day of the month at which a one month cumulative evaluation window starts.

        :schema: MonitorSchedulingOptionsEvaluationWindow
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cbea4e24a36be3bbaaa00e68ad56410a6c88f9a6db8c6e0ae6834bb09f5597d3)
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

        :schema: MonitorSchedulingOptionsEvaluationWindow#DayStarts
        '''
        result = self._values.get("day_starts")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def hour_starts(self) -> typing.Optional[jsii.Number]:
        '''The minute of the hour at which a one hour cumulative evaluation window starts.

        :schema: MonitorSchedulingOptionsEvaluationWindow#HourStarts
        '''
        result = self._values.get("hour_starts")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def month_starts(self) -> typing.Optional[jsii.Number]:
        '''The day of the month at which a one month cumulative evaluation window starts.

        :schema: MonitorSchedulingOptionsEvaluationWindow#MonthStarts
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


@jsii.data_type(
    jsii_type="@cdk-cloudformation/datadog-monitors-monitor.MonitorThresholdWindows",
    jsii_struct_bases=[],
    name_mapping={
        "recovery_window": "recoveryWindow",
        "trigger_window": "triggerWindow",
    },
)
class MonitorThresholdWindows:
    def __init__(
        self,
        *,
        recovery_window: typing.Optional[builtins.str] = None,
        trigger_window: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param recovery_window: How long an anomalous metric must be normal before recovering from an alert state.
        :param trigger_window: How long a metric must be anomalous before triggering an alert.

        :schema: MonitorThresholdWindows
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4bec5c7b2de332869828ae048461bfc40d78182b11c4ac0f0ae4e194e397145b)
            check_type(argname="argument recovery_window", value=recovery_window, expected_type=type_hints["recovery_window"])
            check_type(argname="argument trigger_window", value=trigger_window, expected_type=type_hints["trigger_window"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if recovery_window is not None:
            self._values["recovery_window"] = recovery_window
        if trigger_window is not None:
            self._values["trigger_window"] = trigger_window

    @builtins.property
    def recovery_window(self) -> typing.Optional[builtins.str]:
        '''How long an anomalous metric must be normal before recovering from an alert state.

        :schema: MonitorThresholdWindows#RecoveryWindow
        '''
        result = self._values.get("recovery_window")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def trigger_window(self) -> typing.Optional[builtins.str]:
        '''How long a metric must be anomalous before triggering an alert.

        :schema: MonitorThresholdWindows#TriggerWindow
        '''
        result = self._values.get("trigger_window")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MonitorThresholdWindows(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdk-cloudformation/datadog-monitors-monitor.MonitorThresholds",
    jsii_struct_bases=[],
    name_mapping={
        "critical": "critical",
        "critical_recovery": "criticalRecovery",
        "ok": "ok",
        "warning": "warning",
        "warning_recovery": "warningRecovery",
    },
)
class MonitorThresholds:
    def __init__(
        self,
        *,
        critical: typing.Optional[jsii.Number] = None,
        critical_recovery: typing.Optional[jsii.Number] = None,
        ok: typing.Optional[jsii.Number] = None,
        warning: typing.Optional[jsii.Number] = None,
        warning_recovery: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param critical: Threshold value for triggering an alert.
        :param critical_recovery: Threshold value for recovering from an alert state.
        :param ok: Threshold value for recovering from an alert state.
        :param warning: Threshold value for triggering a warning.
        :param warning_recovery: Threshold value for recovering from a warning state.

        :schema: MonitorThresholds
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e289f3046fe353d6356bef23b661cea846ef3def854667c6aaeba7a3e4bf9c9d)
            check_type(argname="argument critical", value=critical, expected_type=type_hints["critical"])
            check_type(argname="argument critical_recovery", value=critical_recovery, expected_type=type_hints["critical_recovery"])
            check_type(argname="argument ok", value=ok, expected_type=type_hints["ok"])
            check_type(argname="argument warning", value=warning, expected_type=type_hints["warning"])
            check_type(argname="argument warning_recovery", value=warning_recovery, expected_type=type_hints["warning_recovery"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if critical is not None:
            self._values["critical"] = critical
        if critical_recovery is not None:
            self._values["critical_recovery"] = critical_recovery
        if ok is not None:
            self._values["ok"] = ok
        if warning is not None:
            self._values["warning"] = warning
        if warning_recovery is not None:
            self._values["warning_recovery"] = warning_recovery

    @builtins.property
    def critical(self) -> typing.Optional[jsii.Number]:
        '''Threshold value for triggering an alert.

        :schema: MonitorThresholds#Critical
        '''
        result = self._values.get("critical")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def critical_recovery(self) -> typing.Optional[jsii.Number]:
        '''Threshold value for recovering from an alert state.

        :schema: MonitorThresholds#CriticalRecovery
        '''
        result = self._values.get("critical_recovery")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def ok(self) -> typing.Optional[jsii.Number]:
        '''Threshold value for recovering from an alert state.

        :schema: MonitorThresholds#OK
        '''
        result = self._values.get("ok")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def warning(self) -> typing.Optional[jsii.Number]:
        '''Threshold value for triggering a warning.

        :schema: MonitorThresholds#Warning
        '''
        result = self._values.get("warning")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def warning_recovery(self) -> typing.Optional[jsii.Number]:
        '''Threshold value for recovering from a warning state.

        :schema: MonitorThresholds#WarningRecovery
        '''
        result = self._values.get("warning_recovery")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MonitorThresholds(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CfnMonitor",
    "CfnMonitorProps",
    "CfnMonitorPropsType",
    "CloudformationOptions",
    "Creator",
    "MonitorNotificationPresetName",
    "MonitorOnMissingData",
    "MonitorOptions",
    "MonitorOptionsRenotifyStatuses",
    "MonitorSchedulingOptions",
    "MonitorSchedulingOptionsEvaluationWindow",
    "MonitorThresholdWindows",
    "MonitorThresholds",
]

publication.publish()

def _typecheckingstub__9f282a849d0258c7c00bf6bb5adfaf5888d8d58a6ea859cf96cb55870363cea9(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    query: builtins.str,
    type: CfnMonitorPropsType,
    cloudformation_options: typing.Optional[typing.Union[CloudformationOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    creator: typing.Optional[typing.Union[Creator, typing.Dict[builtins.str, typing.Any]]] = None,
    message: typing.Optional[builtins.str] = None,
    multi: typing.Optional[builtins.bool] = None,
    name: typing.Optional[builtins.str] = None,
    options: typing.Optional[typing.Union[MonitorOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    priority: typing.Optional[jsii.Number] = None,
    restricted_roles: typing.Optional[typing.Sequence[builtins.str]] = None,
    tags: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b250b503cf3a08db9d357fada826dc16015ba9e60db0e9ae681c949469261fd(
    *,
    query: builtins.str,
    type: CfnMonitorPropsType,
    cloudformation_options: typing.Optional[typing.Union[CloudformationOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    creator: typing.Optional[typing.Union[Creator, typing.Dict[builtins.str, typing.Any]]] = None,
    message: typing.Optional[builtins.str] = None,
    multi: typing.Optional[builtins.bool] = None,
    name: typing.Optional[builtins.str] = None,
    options: typing.Optional[typing.Union[MonitorOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    priority: typing.Optional[jsii.Number] = None,
    restricted_roles: typing.Optional[typing.Sequence[builtins.str]] = None,
    tags: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98590a687a31b5d4477e712130bcebbddba886b5dd298e667d974c7f1b680d62(
    *,
    lowercase_query: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d5afe2b8f1151f0f40371462dd579b9cfa7efda301b6f260a034f1526916e4b(
    *,
    email: typing.Optional[builtins.str] = None,
    handle: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78f4431522a5d2fdafd31ea8fca3d54dc4a7c104d932702aadab68b0c39f8666(
    *,
    enable_logs_sample: typing.Optional[builtins.bool] = None,
    enable_samples: typing.Optional[builtins.bool] = None,
    escalation_message: typing.Optional[builtins.str] = None,
    evaluation_delay: typing.Optional[jsii.Number] = None,
    group_retention_duration: typing.Optional[builtins.str] = None,
    include_tags: typing.Optional[builtins.bool] = None,
    locked: typing.Optional[builtins.bool] = None,
    min_failure_duration: typing.Optional[jsii.Number] = None,
    min_location_failed: typing.Optional[jsii.Number] = None,
    new_group_delay: typing.Optional[jsii.Number] = None,
    new_host_delay: typing.Optional[jsii.Number] = None,
    no_data_timeframe: typing.Optional[jsii.Number] = None,
    notification_preset_name: typing.Optional[MonitorNotificationPresetName] = None,
    notify_audit: typing.Optional[builtins.bool] = None,
    notify_by: typing.Optional[typing.Sequence[builtins.str]] = None,
    notify_no_data: typing.Optional[builtins.bool] = None,
    on_missing_data: typing.Optional[MonitorOnMissingData] = None,
    renotify_interval: typing.Optional[jsii.Number] = None,
    renotify_occurrences: typing.Optional[jsii.Number] = None,
    renotify_statuses: typing.Optional[typing.Sequence[MonitorOptionsRenotifyStatuses]] = None,
    require_full_window: typing.Optional[builtins.bool] = None,
    scheduling_options: typing.Optional[typing.Union[MonitorSchedulingOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    synthetics_check_id: typing.Optional[jsii.Number] = None,
    thresholds: typing.Optional[typing.Union[MonitorThresholds, typing.Dict[builtins.str, typing.Any]]] = None,
    threshold_windows: typing.Optional[typing.Union[MonitorThresholdWindows, typing.Dict[builtins.str, typing.Any]]] = None,
    timeout_h: typing.Optional[jsii.Number] = None,
    variables: typing.Optional[typing.Sequence[typing.Any]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df3bd89691b70fe1f6861c110d4d796b098ad9203d69d599177be23be28d32c3(
    *,
    evaluation_window: typing.Optional[typing.Union[MonitorSchedulingOptionsEvaluationWindow, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cbea4e24a36be3bbaaa00e68ad56410a6c88f9a6db8c6e0ae6834bb09f5597d3(
    *,
    day_starts: typing.Optional[builtins.str] = None,
    hour_starts: typing.Optional[jsii.Number] = None,
    month_starts: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4bec5c7b2de332869828ae048461bfc40d78182b11c4ac0f0ae4e194e397145b(
    *,
    recovery_window: typing.Optional[builtins.str] = None,
    trigger_window: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e289f3046fe353d6356bef23b661cea846ef3def854667c6aaeba7a3e4bf9c9d(
    *,
    critical: typing.Optional[jsii.Number] = None,
    critical_recovery: typing.Optional[jsii.Number] = None,
    ok: typing.Optional[jsii.Number] = None,
    warning: typing.Optional[jsii.Number] = None,
    warning_recovery: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass
