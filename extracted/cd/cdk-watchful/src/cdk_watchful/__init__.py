'''
---


### ✨ Have you heard of <a href="https://github.com/cdklabs/cdk-monitoring-constructs">cdk-monitoring-constructs</a>? ✨</span>

Watchful on steroids. Check it out! 🔝

---


# cdk-watchful

> Watching your CDK back since 2019

Watchful is an [AWS CDK](https://github.com/awslabs/aws-cdk) construct library that makes it easy
to monitor CDK apps. It automatically synthesizes alarms and dashboards for supported AWS resources.

```python
# my_table: dynamodb.Table
# my_function: lambda.Function
# my_rest_api: apigw.RestApi


wf = Watchful(self, "watchful")
wf.watch_dynamo_table("My Cute Little Table", my_table)
wf.watch_lambda_function("My Function", my_function)
wf.watch_api_gateway("My REST API", my_rest_api)
```

And...

![](https://raw.githubusercontent.com/eladb/cdk-watchful/master/example/sample.png)

## Initialize

To get started, just define a `Watchful` construct in your CDK app.
You can initialize using an email address, SQS ARN or both:

```python
import aws_cdk.aws_sns as sns
import aws_cdk.aws_sqs as sqs


alarm_sqs = sqs.Queue.from_queue_arn(self, "AlarmQueue", "arn:aws:sqs:us-east-1:444455556666:alarm-queue")
alarm_sns = sns.Topic.from_topic_arn(self, "AlarmTopic", "arn:aws:sns:us-east-2:444455556666:MyTopic")

wf = Watchful(self, "watchful",
    alarm_email="your@email.com",
    alarm_sqs=alarm_sqs,
    alarm_sns=alarm_sns,
    alarm_action_arns=["arn:aws:sqs:us-east-1:444455556666:alarm-queue"]
)
```

## Add Resources

Watchful manages a central dashboard and configures default alarming for:

* Amazon DynamoDB: `watchful.watchDynamoTable`
* AWS Lambda: `watchful.watchLambdaFunction`
* Amazon API Gateway: `watchful.watchApiGateway`
* [Request yours](https://github.com/eladb/cdk-watchful/issues/new)

## Watching Scopes

Watchful can also watch complete CDK construct scopes. It will automatically
discover all watchable resources within that scope (recursively), add them
to your dashboard and configure alarms for them.

```python
# storage_layer: Stack
# wf: Watchful


wf.watch_scope(storage_layer)
```

## Example

See a more complete [example](https://github.com/eladb/cdk-watchful/blob/master/example/index.ts).

## Contributing

Contributions of all kinds are welcome and celebrated. Raise an issue, submit a PR, do the right thing.

To set up a dev environment:

1. Clone this repo
2. `yarn`

Development workflow (change code and run tests automatically):

```shell
yarn test:watch
```

Build (like CI):

```shell
yarn build
```

And then publish as a PR.

## License

[Apache 2.0](https://github.com/eladb/cdk-watchful/blob/master/LICENSE)
'''
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
import aws_cdk.aws_apigateway as _aws_cdk_aws_apigateway_ceddda9d
import aws_cdk.aws_cloudwatch as _aws_cdk_aws_cloudwatch_ceddda9d
import aws_cdk.aws_dynamodb as _aws_cdk_aws_dynamodb_ceddda9d
import aws_cdk.aws_ecs as _aws_cdk_aws_ecs_ceddda9d
import aws_cdk.aws_elasticloadbalancingv2 as _aws_cdk_aws_elasticloadbalancingv2_ceddda9d
import aws_cdk.aws_lambda as _aws_cdk_aws_lambda_ceddda9d
import aws_cdk.aws_rds as _aws_cdk_aws_rds_ceddda9d
import aws_cdk.aws_sns as _aws_cdk_aws_sns_ceddda9d
import aws_cdk.aws_sqs as _aws_cdk_aws_sqs_ceddda9d
import aws_cdk.aws_stepfunctions as _aws_cdk_aws_stepfunctions_ceddda9d
import constructs as _constructs_77d1e7e8


@jsii.interface(jsii_type="cdk-watchful.IWatchful")
class IWatchful(typing_extensions.Protocol):
    '''
    :stability: experimental
    '''

    @jsii.member(jsii_name="addAlarm")
    def add_alarm(self, alarm: _aws_cdk_aws_cloudwatch_ceddda9d.IAlarm) -> None:
        '''
        :param alarm: -

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="addSection")
    def add_section(
        self,
        title: builtins.str,
        *,
        links: typing.Optional[typing.Sequence[typing.Union["QuickLink", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''
        :param title: -
        :param links: 

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="addWidgets")
    def add_widgets(self, *widgets: _aws_cdk_aws_cloudwatch_ceddda9d.IWidget) -> None:
        '''
        :param widgets: -

        :stability: experimental
        '''
        ...


class _IWatchfulProxy:
    '''
    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "cdk-watchful.IWatchful"

    @jsii.member(jsii_name="addAlarm")
    def add_alarm(self, alarm: _aws_cdk_aws_cloudwatch_ceddda9d.IAlarm) -> None:
        '''
        :param alarm: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7d18083d7541e3f81cf482ce05d307f18f64607c08aab670a121bd626443015b)
            check_type(argname="argument alarm", value=alarm, expected_type=type_hints["alarm"])
        return typing.cast(None, jsii.invoke(self, "addAlarm", [alarm]))

    @jsii.member(jsii_name="addSection")
    def add_section(
        self,
        title: builtins.str,
        *,
        links: typing.Optional[typing.Sequence[typing.Union["QuickLink", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''
        :param title: -
        :param links: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4cf210aea2d147e6b96aa16918ad9377592550fdee7809de8b94ae0337452073)
            check_type(argname="argument title", value=title, expected_type=type_hints["title"])
        options = SectionOptions(links=links)

        return typing.cast(None, jsii.invoke(self, "addSection", [title, options]))

    @jsii.member(jsii_name="addWidgets")
    def add_widgets(self, *widgets: _aws_cdk_aws_cloudwatch_ceddda9d.IWidget) -> None:
        '''
        :param widgets: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__590f1205141b383cfe196149d2716a94cd091a40dbf666d9c07487847b6f0bbb)
            check_type(argname="argument widgets", value=widgets, expected_type=typing.Tuple[type_hints["widgets"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast(None, jsii.invoke(self, "addWidgets", [*widgets]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IWatchful).__jsii_proxy_class__ = lambda : _IWatchfulProxy


@jsii.data_type(
    jsii_type="cdk-watchful.QuickLink",
    jsii_struct_bases=[],
    name_mapping={"title": "title", "url": "url"},
)
class QuickLink:
    def __init__(self, *, title: builtins.str, url: builtins.str) -> None:
        '''
        :param title: 
        :param url: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7cc0a132a71b0666adac532b07b7e9ef7ba799a6d4217acc83ec82b0ba772527)
            check_type(argname="argument title", value=title, expected_type=type_hints["title"])
            check_type(argname="argument url", value=url, expected_type=type_hints["url"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "title": title,
            "url": url,
        }

    @builtins.property
    def title(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        result = self._values.get("title")
        assert result is not None, "Required property 'title' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def url(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        result = self._values.get("url")
        assert result is not None, "Required property 'url' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "QuickLink(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-watchful.SectionOptions",
    jsii_struct_bases=[],
    name_mapping={"links": "links"},
)
class SectionOptions:
    def __init__(
        self,
        *,
        links: typing.Optional[typing.Sequence[typing.Union[QuickLink, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''
        :param links: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7fb1a4c9454f37ad6accc1c8ddcd1626e85ed52787ae2e20667554ff2d9d0c19)
            check_type(argname="argument links", value=links, expected_type=type_hints["links"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if links is not None:
            self._values["links"] = links

    @builtins.property
    def links(self) -> typing.Optional[typing.List[QuickLink]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("links")
        return typing.cast(typing.Optional[typing.List[QuickLink]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SectionOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class WatchApiGateway(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-watchful.WatchApiGateway",
):
    '''
    :stability: experimental
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        rest_api: _aws_cdk_aws_apigateway_ceddda9d.RestApi,
        title: builtins.str,
        watchful: IWatchful,
        cache_graph: typing.Optional[builtins.bool] = None,
        server_error_threshold: typing.Optional[jsii.Number] = None,
        watched_operations: typing.Optional[typing.Sequence[typing.Union["WatchedOperation", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param rest_api: (experimental) The API Gateway REST API that is being watched.
        :param title: (experimental) The title of this section.
        :param watchful: (experimental) The Watchful instance to add widgets into.
        :param cache_graph: (experimental) Include a dashboard graph for caching metrics. Default: false
        :param server_error_threshold: (experimental) Alarm when 5XX errors reach this threshold over 5 minutes. Default: 1 any 5xx HTTP response will trigger the alarm
        :param watched_operations: (experimental) A list of operations to monitor separately. Default: - only API-level monitoring is added.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4dffce348291255de623b50cc32f7b24de1702a38d6708f3d2be1b0463194bde)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = WatchApiGatewayProps(
            rest_api=rest_api,
            title=title,
            watchful=watchful,
            cache_graph=cache_graph,
            server_error_threshold=server_error_threshold,
            watched_operations=watched_operations,
        )

        jsii.create(self.__class__, self, [scope, id, props])


@jsii.data_type(
    jsii_type="cdk-watchful.WatchApiGatewayOptions",
    jsii_struct_bases=[],
    name_mapping={
        "cache_graph": "cacheGraph",
        "server_error_threshold": "serverErrorThreshold",
        "watched_operations": "watchedOperations",
    },
)
class WatchApiGatewayOptions:
    def __init__(
        self,
        *,
        cache_graph: typing.Optional[builtins.bool] = None,
        server_error_threshold: typing.Optional[jsii.Number] = None,
        watched_operations: typing.Optional[typing.Sequence[typing.Union["WatchedOperation", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''
        :param cache_graph: (experimental) Include a dashboard graph for caching metrics. Default: false
        :param server_error_threshold: (experimental) Alarm when 5XX errors reach this threshold over 5 minutes. Default: 1 any 5xx HTTP response will trigger the alarm
        :param watched_operations: (experimental) A list of operations to monitor separately. Default: - only API-level monitoring is added.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__81186eaf281e06f86d075cf2dda80d173551899867cd26312dcd571a089a558b)
            check_type(argname="argument cache_graph", value=cache_graph, expected_type=type_hints["cache_graph"])
            check_type(argname="argument server_error_threshold", value=server_error_threshold, expected_type=type_hints["server_error_threshold"])
            check_type(argname="argument watched_operations", value=watched_operations, expected_type=type_hints["watched_operations"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if cache_graph is not None:
            self._values["cache_graph"] = cache_graph
        if server_error_threshold is not None:
            self._values["server_error_threshold"] = server_error_threshold
        if watched_operations is not None:
            self._values["watched_operations"] = watched_operations

    @builtins.property
    def cache_graph(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Include a dashboard graph for caching metrics.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("cache_graph")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def server_error_threshold(self) -> typing.Optional[jsii.Number]:
        '''(experimental) Alarm when 5XX errors reach this threshold over 5 minutes.

        :default: 1 any 5xx HTTP response will trigger the alarm

        :stability: experimental
        '''
        result = self._values.get("server_error_threshold")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def watched_operations(self) -> typing.Optional[typing.List["WatchedOperation"]]:
        '''(experimental) A list of operations to monitor separately.

        :default: - only API-level monitoring is added.

        :stability: experimental
        '''
        result = self._values.get("watched_operations")
        return typing.cast(typing.Optional[typing.List["WatchedOperation"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WatchApiGatewayOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-watchful.WatchApiGatewayProps",
    jsii_struct_bases=[WatchApiGatewayOptions],
    name_mapping={
        "cache_graph": "cacheGraph",
        "server_error_threshold": "serverErrorThreshold",
        "watched_operations": "watchedOperations",
        "rest_api": "restApi",
        "title": "title",
        "watchful": "watchful",
    },
)
class WatchApiGatewayProps(WatchApiGatewayOptions):
    def __init__(
        self,
        *,
        cache_graph: typing.Optional[builtins.bool] = None,
        server_error_threshold: typing.Optional[jsii.Number] = None,
        watched_operations: typing.Optional[typing.Sequence[typing.Union["WatchedOperation", typing.Dict[builtins.str, typing.Any]]]] = None,
        rest_api: _aws_cdk_aws_apigateway_ceddda9d.RestApi,
        title: builtins.str,
        watchful: IWatchful,
    ) -> None:
        '''
        :param cache_graph: (experimental) Include a dashboard graph for caching metrics. Default: false
        :param server_error_threshold: (experimental) Alarm when 5XX errors reach this threshold over 5 minutes. Default: 1 any 5xx HTTP response will trigger the alarm
        :param watched_operations: (experimental) A list of operations to monitor separately. Default: - only API-level monitoring is added.
        :param rest_api: (experimental) The API Gateway REST API that is being watched.
        :param title: (experimental) The title of this section.
        :param watchful: (experimental) The Watchful instance to add widgets into.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4beb71a19ca36730c44158b65cd3b514ea335d51cbdf34ccfbeb7de2c5a6cde1)
            check_type(argname="argument cache_graph", value=cache_graph, expected_type=type_hints["cache_graph"])
            check_type(argname="argument server_error_threshold", value=server_error_threshold, expected_type=type_hints["server_error_threshold"])
            check_type(argname="argument watched_operations", value=watched_operations, expected_type=type_hints["watched_operations"])
            check_type(argname="argument rest_api", value=rest_api, expected_type=type_hints["rest_api"])
            check_type(argname="argument title", value=title, expected_type=type_hints["title"])
            check_type(argname="argument watchful", value=watchful, expected_type=type_hints["watchful"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "rest_api": rest_api,
            "title": title,
            "watchful": watchful,
        }
        if cache_graph is not None:
            self._values["cache_graph"] = cache_graph
        if server_error_threshold is not None:
            self._values["server_error_threshold"] = server_error_threshold
        if watched_operations is not None:
            self._values["watched_operations"] = watched_operations

    @builtins.property
    def cache_graph(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Include a dashboard graph for caching metrics.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("cache_graph")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def server_error_threshold(self) -> typing.Optional[jsii.Number]:
        '''(experimental) Alarm when 5XX errors reach this threshold over 5 minutes.

        :default: 1 any 5xx HTTP response will trigger the alarm

        :stability: experimental
        '''
        result = self._values.get("server_error_threshold")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def watched_operations(self) -> typing.Optional[typing.List["WatchedOperation"]]:
        '''(experimental) A list of operations to monitor separately.

        :default: - only API-level monitoring is added.

        :stability: experimental
        '''
        result = self._values.get("watched_operations")
        return typing.cast(typing.Optional[typing.List["WatchedOperation"]], result)

    @builtins.property
    def rest_api(self) -> _aws_cdk_aws_apigateway_ceddda9d.RestApi:
        '''(experimental) The API Gateway REST API that is being watched.

        :stability: experimental
        '''
        result = self._values.get("rest_api")
        assert result is not None, "Required property 'rest_api' is missing"
        return typing.cast(_aws_cdk_aws_apigateway_ceddda9d.RestApi, result)

    @builtins.property
    def title(self) -> builtins.str:
        '''(experimental) The title of this section.

        :stability: experimental
        '''
        result = self._values.get("title")
        assert result is not None, "Required property 'title' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def watchful(self) -> IWatchful:
        '''(experimental) The Watchful instance to add widgets into.

        :stability: experimental
        '''
        result = self._values.get("watchful")
        assert result is not None, "Required property 'watchful' is missing"
        return typing.cast(IWatchful, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WatchApiGatewayProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class WatchDynamoTable(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-watchful.WatchDynamoTable",
):
    '''
    :stability: experimental
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        table: _aws_cdk_aws_dynamodb_ceddda9d.Table,
        title: builtins.str,
        watchful: IWatchful,
        read_capacity_threshold_percent: typing.Optional[jsii.Number] = None,
        write_capacity_threshold_percent: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param table: 
        :param title: 
        :param watchful: 
        :param read_capacity_threshold_percent: (experimental) Threshold for read capacity alarm (percentage). Default: 80
        :param write_capacity_threshold_percent: (experimental) Threshold for read capacity alarm (percentage). Default: 80

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__93540066afa1674f8a3dae1aa92222651bf070ad92e1416a1cda5abbd383f0a9)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = WatchDynamoTableProps(
            table=table,
            title=title,
            watchful=watchful,
            read_capacity_threshold_percent=read_capacity_threshold_percent,
            write_capacity_threshold_percent=write_capacity_threshold_percent,
        )

        jsii.create(self.__class__, self, [scope, id, props])


@jsii.data_type(
    jsii_type="cdk-watchful.WatchDynamoTableOptions",
    jsii_struct_bases=[],
    name_mapping={
        "read_capacity_threshold_percent": "readCapacityThresholdPercent",
        "write_capacity_threshold_percent": "writeCapacityThresholdPercent",
    },
)
class WatchDynamoTableOptions:
    def __init__(
        self,
        *,
        read_capacity_threshold_percent: typing.Optional[jsii.Number] = None,
        write_capacity_threshold_percent: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param read_capacity_threshold_percent: (experimental) Threshold for read capacity alarm (percentage). Default: 80
        :param write_capacity_threshold_percent: (experimental) Threshold for read capacity alarm (percentage). Default: 80

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__72119e08dbb6fe92ee77609b57f3ab38b3f314670a53c2fdf208d56b43527c2a)
            check_type(argname="argument read_capacity_threshold_percent", value=read_capacity_threshold_percent, expected_type=type_hints["read_capacity_threshold_percent"])
            check_type(argname="argument write_capacity_threshold_percent", value=write_capacity_threshold_percent, expected_type=type_hints["write_capacity_threshold_percent"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if read_capacity_threshold_percent is not None:
            self._values["read_capacity_threshold_percent"] = read_capacity_threshold_percent
        if write_capacity_threshold_percent is not None:
            self._values["write_capacity_threshold_percent"] = write_capacity_threshold_percent

    @builtins.property
    def read_capacity_threshold_percent(self) -> typing.Optional[jsii.Number]:
        '''(experimental) Threshold for read capacity alarm (percentage).

        :default: 80

        :stability: experimental
        '''
        result = self._values.get("read_capacity_threshold_percent")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def write_capacity_threshold_percent(self) -> typing.Optional[jsii.Number]:
        '''(experimental) Threshold for read capacity alarm (percentage).

        :default: 80

        :stability: experimental
        '''
        result = self._values.get("write_capacity_threshold_percent")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WatchDynamoTableOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-watchful.WatchDynamoTableProps",
    jsii_struct_bases=[WatchDynamoTableOptions],
    name_mapping={
        "read_capacity_threshold_percent": "readCapacityThresholdPercent",
        "write_capacity_threshold_percent": "writeCapacityThresholdPercent",
        "table": "table",
        "title": "title",
        "watchful": "watchful",
    },
)
class WatchDynamoTableProps(WatchDynamoTableOptions):
    def __init__(
        self,
        *,
        read_capacity_threshold_percent: typing.Optional[jsii.Number] = None,
        write_capacity_threshold_percent: typing.Optional[jsii.Number] = None,
        table: _aws_cdk_aws_dynamodb_ceddda9d.Table,
        title: builtins.str,
        watchful: IWatchful,
    ) -> None:
        '''
        :param read_capacity_threshold_percent: (experimental) Threshold for read capacity alarm (percentage). Default: 80
        :param write_capacity_threshold_percent: (experimental) Threshold for read capacity alarm (percentage). Default: 80
        :param table: 
        :param title: 
        :param watchful: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__692ff4756198d2d44be2a21d7e23974b81ce26953bc1861b2a517984c4b18c1e)
            check_type(argname="argument read_capacity_threshold_percent", value=read_capacity_threshold_percent, expected_type=type_hints["read_capacity_threshold_percent"])
            check_type(argname="argument write_capacity_threshold_percent", value=write_capacity_threshold_percent, expected_type=type_hints["write_capacity_threshold_percent"])
            check_type(argname="argument table", value=table, expected_type=type_hints["table"])
            check_type(argname="argument title", value=title, expected_type=type_hints["title"])
            check_type(argname="argument watchful", value=watchful, expected_type=type_hints["watchful"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "table": table,
            "title": title,
            "watchful": watchful,
        }
        if read_capacity_threshold_percent is not None:
            self._values["read_capacity_threshold_percent"] = read_capacity_threshold_percent
        if write_capacity_threshold_percent is not None:
            self._values["write_capacity_threshold_percent"] = write_capacity_threshold_percent

    @builtins.property
    def read_capacity_threshold_percent(self) -> typing.Optional[jsii.Number]:
        '''(experimental) Threshold for read capacity alarm (percentage).

        :default: 80

        :stability: experimental
        '''
        result = self._values.get("read_capacity_threshold_percent")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def write_capacity_threshold_percent(self) -> typing.Optional[jsii.Number]:
        '''(experimental) Threshold for read capacity alarm (percentage).

        :default: 80

        :stability: experimental
        '''
        result = self._values.get("write_capacity_threshold_percent")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def table(self) -> _aws_cdk_aws_dynamodb_ceddda9d.Table:
        '''
        :stability: experimental
        '''
        result = self._values.get("table")
        assert result is not None, "Required property 'table' is missing"
        return typing.cast(_aws_cdk_aws_dynamodb_ceddda9d.Table, result)

    @builtins.property
    def title(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        result = self._values.get("title")
        assert result is not None, "Required property 'title' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def watchful(self) -> IWatchful:
        '''
        :stability: experimental
        '''
        result = self._values.get("watchful")
        assert result is not None, "Required property 'watchful' is missing"
        return typing.cast(IWatchful, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WatchDynamoTableProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class WatchEcsService(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-watchful.WatchEcsService",
):
    '''
    :stability: experimental
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        target_group: _aws_cdk_aws_elasticloadbalancingv2_ceddda9d.ApplicationTargetGroup,
        title: builtins.str,
        watchful: IWatchful,
        ec2_service: typing.Optional[_aws_cdk_aws_ecs_ceddda9d.Ec2Service] = None,
        fargate_service: typing.Optional[_aws_cdk_aws_ecs_ceddda9d.FargateService] = None,
        cpu_maximum_threshold_percent: typing.Optional[jsii.Number] = None,
        memory_maximum_threshold_percent: typing.Optional[jsii.Number] = None,
        requests_error_rate_threshold: typing.Optional[jsii.Number] = None,
        requests_threshold: typing.Optional[jsii.Number] = None,
        target_response_time_threshold: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param target_group: 
        :param title: 
        :param watchful: 
        :param ec2_service: 
        :param fargate_service: 
        :param cpu_maximum_threshold_percent: (experimental) Threshold for the Cpu Maximum utilization. Default: 80
        :param memory_maximum_threshold_percent: (experimental) Threshold for the Memory Maximum utilization. Default: - 0.
        :param requests_error_rate_threshold: (experimental) Threshold for the Number of Request Errors. Default: - 0.
        :param requests_threshold: (experimental) Threshold for the Number of Requests. Default: - 0.
        :param target_response_time_threshold: (experimental) Threshold for the Target Response Time. Default: - 0.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__66cc0b5a8c93329e091a2b01f6f3d9d11eeaf52ca9592d84cd5b6994b2a590c5)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = WatchEcsServiceProps(
            target_group=target_group,
            title=title,
            watchful=watchful,
            ec2_service=ec2_service,
            fargate_service=fargate_service,
            cpu_maximum_threshold_percent=cpu_maximum_threshold_percent,
            memory_maximum_threshold_percent=memory_maximum_threshold_percent,
            requests_error_rate_threshold=requests_error_rate_threshold,
            requests_threshold=requests_threshold,
            target_response_time_threshold=target_response_time_threshold,
        )

        jsii.create(self.__class__, self, [scope, id, props])


@jsii.data_type(
    jsii_type="cdk-watchful.WatchEcsServiceOptions",
    jsii_struct_bases=[],
    name_mapping={
        "cpu_maximum_threshold_percent": "cpuMaximumThresholdPercent",
        "memory_maximum_threshold_percent": "memoryMaximumThresholdPercent",
        "requests_error_rate_threshold": "requestsErrorRateThreshold",
        "requests_threshold": "requestsThreshold",
        "target_response_time_threshold": "targetResponseTimeThreshold",
    },
)
class WatchEcsServiceOptions:
    def __init__(
        self,
        *,
        cpu_maximum_threshold_percent: typing.Optional[jsii.Number] = None,
        memory_maximum_threshold_percent: typing.Optional[jsii.Number] = None,
        requests_error_rate_threshold: typing.Optional[jsii.Number] = None,
        requests_threshold: typing.Optional[jsii.Number] = None,
        target_response_time_threshold: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param cpu_maximum_threshold_percent: (experimental) Threshold for the Cpu Maximum utilization. Default: 80
        :param memory_maximum_threshold_percent: (experimental) Threshold for the Memory Maximum utilization. Default: - 0.
        :param requests_error_rate_threshold: (experimental) Threshold for the Number of Request Errors. Default: - 0.
        :param requests_threshold: (experimental) Threshold for the Number of Requests. Default: - 0.
        :param target_response_time_threshold: (experimental) Threshold for the Target Response Time. Default: - 0.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__50ffd7689126fc30d39d2077edb2938978e4621d3f0f80562b041af1143fe3a9)
            check_type(argname="argument cpu_maximum_threshold_percent", value=cpu_maximum_threshold_percent, expected_type=type_hints["cpu_maximum_threshold_percent"])
            check_type(argname="argument memory_maximum_threshold_percent", value=memory_maximum_threshold_percent, expected_type=type_hints["memory_maximum_threshold_percent"])
            check_type(argname="argument requests_error_rate_threshold", value=requests_error_rate_threshold, expected_type=type_hints["requests_error_rate_threshold"])
            check_type(argname="argument requests_threshold", value=requests_threshold, expected_type=type_hints["requests_threshold"])
            check_type(argname="argument target_response_time_threshold", value=target_response_time_threshold, expected_type=type_hints["target_response_time_threshold"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if cpu_maximum_threshold_percent is not None:
            self._values["cpu_maximum_threshold_percent"] = cpu_maximum_threshold_percent
        if memory_maximum_threshold_percent is not None:
            self._values["memory_maximum_threshold_percent"] = memory_maximum_threshold_percent
        if requests_error_rate_threshold is not None:
            self._values["requests_error_rate_threshold"] = requests_error_rate_threshold
        if requests_threshold is not None:
            self._values["requests_threshold"] = requests_threshold
        if target_response_time_threshold is not None:
            self._values["target_response_time_threshold"] = target_response_time_threshold

    @builtins.property
    def cpu_maximum_threshold_percent(self) -> typing.Optional[jsii.Number]:
        '''(experimental) Threshold for the Cpu Maximum utilization.

        :default: 80

        :stability: experimental
        '''
        result = self._values.get("cpu_maximum_threshold_percent")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def memory_maximum_threshold_percent(self) -> typing.Optional[jsii.Number]:
        '''(experimental) Threshold for the Memory Maximum utilization.

        :default:

        -
        0.

        :stability: experimental
        '''
        result = self._values.get("memory_maximum_threshold_percent")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def requests_error_rate_threshold(self) -> typing.Optional[jsii.Number]:
        '''(experimental) Threshold for the Number of Request Errors.

        :default:

        -
        0.

        :stability: experimental
        '''
        result = self._values.get("requests_error_rate_threshold")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def requests_threshold(self) -> typing.Optional[jsii.Number]:
        '''(experimental) Threshold for the Number of Requests.

        :default:

        -
        0.

        :stability: experimental
        '''
        result = self._values.get("requests_threshold")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def target_response_time_threshold(self) -> typing.Optional[jsii.Number]:
        '''(experimental) Threshold for the Target Response Time.

        :default:

        -
        0.

        :stability: experimental
        '''
        result = self._values.get("target_response_time_threshold")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WatchEcsServiceOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-watchful.WatchEcsServiceProps",
    jsii_struct_bases=[WatchEcsServiceOptions],
    name_mapping={
        "cpu_maximum_threshold_percent": "cpuMaximumThresholdPercent",
        "memory_maximum_threshold_percent": "memoryMaximumThresholdPercent",
        "requests_error_rate_threshold": "requestsErrorRateThreshold",
        "requests_threshold": "requestsThreshold",
        "target_response_time_threshold": "targetResponseTimeThreshold",
        "target_group": "targetGroup",
        "title": "title",
        "watchful": "watchful",
        "ec2_service": "ec2Service",
        "fargate_service": "fargateService",
    },
)
class WatchEcsServiceProps(WatchEcsServiceOptions):
    def __init__(
        self,
        *,
        cpu_maximum_threshold_percent: typing.Optional[jsii.Number] = None,
        memory_maximum_threshold_percent: typing.Optional[jsii.Number] = None,
        requests_error_rate_threshold: typing.Optional[jsii.Number] = None,
        requests_threshold: typing.Optional[jsii.Number] = None,
        target_response_time_threshold: typing.Optional[jsii.Number] = None,
        target_group: _aws_cdk_aws_elasticloadbalancingv2_ceddda9d.ApplicationTargetGroup,
        title: builtins.str,
        watchful: IWatchful,
        ec2_service: typing.Optional[_aws_cdk_aws_ecs_ceddda9d.Ec2Service] = None,
        fargate_service: typing.Optional[_aws_cdk_aws_ecs_ceddda9d.FargateService] = None,
    ) -> None:
        '''
        :param cpu_maximum_threshold_percent: (experimental) Threshold for the Cpu Maximum utilization. Default: 80
        :param memory_maximum_threshold_percent: (experimental) Threshold for the Memory Maximum utilization. Default: - 0.
        :param requests_error_rate_threshold: (experimental) Threshold for the Number of Request Errors. Default: - 0.
        :param requests_threshold: (experimental) Threshold for the Number of Requests. Default: - 0.
        :param target_response_time_threshold: (experimental) Threshold for the Target Response Time. Default: - 0.
        :param target_group: 
        :param title: 
        :param watchful: 
        :param ec2_service: 
        :param fargate_service: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a550a07d3f0b4b54887066fa76ac5383cb624f4233d34f4fd3583a1446342f2a)
            check_type(argname="argument cpu_maximum_threshold_percent", value=cpu_maximum_threshold_percent, expected_type=type_hints["cpu_maximum_threshold_percent"])
            check_type(argname="argument memory_maximum_threshold_percent", value=memory_maximum_threshold_percent, expected_type=type_hints["memory_maximum_threshold_percent"])
            check_type(argname="argument requests_error_rate_threshold", value=requests_error_rate_threshold, expected_type=type_hints["requests_error_rate_threshold"])
            check_type(argname="argument requests_threshold", value=requests_threshold, expected_type=type_hints["requests_threshold"])
            check_type(argname="argument target_response_time_threshold", value=target_response_time_threshold, expected_type=type_hints["target_response_time_threshold"])
            check_type(argname="argument target_group", value=target_group, expected_type=type_hints["target_group"])
            check_type(argname="argument title", value=title, expected_type=type_hints["title"])
            check_type(argname="argument watchful", value=watchful, expected_type=type_hints["watchful"])
            check_type(argname="argument ec2_service", value=ec2_service, expected_type=type_hints["ec2_service"])
            check_type(argname="argument fargate_service", value=fargate_service, expected_type=type_hints["fargate_service"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "target_group": target_group,
            "title": title,
            "watchful": watchful,
        }
        if cpu_maximum_threshold_percent is not None:
            self._values["cpu_maximum_threshold_percent"] = cpu_maximum_threshold_percent
        if memory_maximum_threshold_percent is not None:
            self._values["memory_maximum_threshold_percent"] = memory_maximum_threshold_percent
        if requests_error_rate_threshold is not None:
            self._values["requests_error_rate_threshold"] = requests_error_rate_threshold
        if requests_threshold is not None:
            self._values["requests_threshold"] = requests_threshold
        if target_response_time_threshold is not None:
            self._values["target_response_time_threshold"] = target_response_time_threshold
        if ec2_service is not None:
            self._values["ec2_service"] = ec2_service
        if fargate_service is not None:
            self._values["fargate_service"] = fargate_service

    @builtins.property
    def cpu_maximum_threshold_percent(self) -> typing.Optional[jsii.Number]:
        '''(experimental) Threshold for the Cpu Maximum utilization.

        :default: 80

        :stability: experimental
        '''
        result = self._values.get("cpu_maximum_threshold_percent")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def memory_maximum_threshold_percent(self) -> typing.Optional[jsii.Number]:
        '''(experimental) Threshold for the Memory Maximum utilization.

        :default:

        -
        0.

        :stability: experimental
        '''
        result = self._values.get("memory_maximum_threshold_percent")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def requests_error_rate_threshold(self) -> typing.Optional[jsii.Number]:
        '''(experimental) Threshold for the Number of Request Errors.

        :default:

        -
        0.

        :stability: experimental
        '''
        result = self._values.get("requests_error_rate_threshold")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def requests_threshold(self) -> typing.Optional[jsii.Number]:
        '''(experimental) Threshold for the Number of Requests.

        :default:

        -
        0.

        :stability: experimental
        '''
        result = self._values.get("requests_threshold")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def target_response_time_threshold(self) -> typing.Optional[jsii.Number]:
        '''(experimental) Threshold for the Target Response Time.

        :default:

        -
        0.

        :stability: experimental
        '''
        result = self._values.get("target_response_time_threshold")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def target_group(
        self,
    ) -> _aws_cdk_aws_elasticloadbalancingv2_ceddda9d.ApplicationTargetGroup:
        '''
        :stability: experimental
        '''
        result = self._values.get("target_group")
        assert result is not None, "Required property 'target_group' is missing"
        return typing.cast(_aws_cdk_aws_elasticloadbalancingv2_ceddda9d.ApplicationTargetGroup, result)

    @builtins.property
    def title(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        result = self._values.get("title")
        assert result is not None, "Required property 'title' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def watchful(self) -> IWatchful:
        '''
        :stability: experimental
        '''
        result = self._values.get("watchful")
        assert result is not None, "Required property 'watchful' is missing"
        return typing.cast(IWatchful, result)

    @builtins.property
    def ec2_service(self) -> typing.Optional[_aws_cdk_aws_ecs_ceddda9d.Ec2Service]:
        '''
        :stability: experimental
        '''
        result = self._values.get("ec2_service")
        return typing.cast(typing.Optional[_aws_cdk_aws_ecs_ceddda9d.Ec2Service], result)

    @builtins.property
    def fargate_service(
        self,
    ) -> typing.Optional[_aws_cdk_aws_ecs_ceddda9d.FargateService]:
        '''
        :stability: experimental
        '''
        result = self._values.get("fargate_service")
        return typing.cast(typing.Optional[_aws_cdk_aws_ecs_ceddda9d.FargateService], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WatchEcsServiceProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class WatchLambdaFunction(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-watchful.WatchLambdaFunction",
):
    '''
    :stability: experimental
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        fn: _aws_cdk_aws_lambda_ceddda9d.Function,
        title: builtins.str,
        watchful: IWatchful,
        duration_threshold_percent: typing.Optional[jsii.Number] = None,
        errors_per_minute_threshold: typing.Optional[jsii.Number] = None,
        throttles_per_minute_threshold: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param fn: 
        :param title: 
        :param watchful: 
        :param duration_threshold_percent: (experimental) Threshold for the duration alarm as percentage of the function's timeout value. If this is set to 50%, the alarm will be set when p99 latency of the function exceeds 50% of the function's timeout setting. Default: 80
        :param errors_per_minute_threshold: (experimental) Number of allowed errors per minute. If there are more errors than that, an alarm will trigger. Default: 0
        :param throttles_per_minute_threshold: (experimental) Number of allowed throttles per minute. Default: 0

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__429a2cc615c769d2215ffe2fb7bf1476baec5e87d95b11f2f2b15a343349d97c)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = WatchLambdaFunctionProps(
            fn=fn,
            title=title,
            watchful=watchful,
            duration_threshold_percent=duration_threshold_percent,
            errors_per_minute_threshold=errors_per_minute_threshold,
            throttles_per_minute_threshold=throttles_per_minute_threshold,
        )

        jsii.create(self.__class__, self, [scope, id, props])


@jsii.data_type(
    jsii_type="cdk-watchful.WatchLambdaFunctionOptions",
    jsii_struct_bases=[],
    name_mapping={
        "duration_threshold_percent": "durationThresholdPercent",
        "errors_per_minute_threshold": "errorsPerMinuteThreshold",
        "throttles_per_minute_threshold": "throttlesPerMinuteThreshold",
    },
)
class WatchLambdaFunctionOptions:
    def __init__(
        self,
        *,
        duration_threshold_percent: typing.Optional[jsii.Number] = None,
        errors_per_minute_threshold: typing.Optional[jsii.Number] = None,
        throttles_per_minute_threshold: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param duration_threshold_percent: (experimental) Threshold for the duration alarm as percentage of the function's timeout value. If this is set to 50%, the alarm will be set when p99 latency of the function exceeds 50% of the function's timeout setting. Default: 80
        :param errors_per_minute_threshold: (experimental) Number of allowed errors per minute. If there are more errors than that, an alarm will trigger. Default: 0
        :param throttles_per_minute_threshold: (experimental) Number of allowed throttles per minute. Default: 0

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c8ec627af1492d940e32839754e3c7a756ecd09f39c0a072c61172f493089be)
            check_type(argname="argument duration_threshold_percent", value=duration_threshold_percent, expected_type=type_hints["duration_threshold_percent"])
            check_type(argname="argument errors_per_minute_threshold", value=errors_per_minute_threshold, expected_type=type_hints["errors_per_minute_threshold"])
            check_type(argname="argument throttles_per_minute_threshold", value=throttles_per_minute_threshold, expected_type=type_hints["throttles_per_minute_threshold"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if duration_threshold_percent is not None:
            self._values["duration_threshold_percent"] = duration_threshold_percent
        if errors_per_minute_threshold is not None:
            self._values["errors_per_minute_threshold"] = errors_per_minute_threshold
        if throttles_per_minute_threshold is not None:
            self._values["throttles_per_minute_threshold"] = throttles_per_minute_threshold

    @builtins.property
    def duration_threshold_percent(self) -> typing.Optional[jsii.Number]:
        '''(experimental) Threshold for the duration alarm as percentage of the function's timeout value.

        If this is set to 50%, the alarm will be set when p99 latency of the
        function exceeds 50% of the function's timeout setting.

        :default: 80

        :stability: experimental
        '''
        result = self._values.get("duration_threshold_percent")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def errors_per_minute_threshold(self) -> typing.Optional[jsii.Number]:
        '''(experimental) Number of allowed errors per minute.

        If there are more errors than that, an alarm will trigger.

        :default: 0

        :stability: experimental
        '''
        result = self._values.get("errors_per_minute_threshold")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def throttles_per_minute_threshold(self) -> typing.Optional[jsii.Number]:
        '''(experimental) Number of allowed throttles per minute.

        :default: 0

        :stability: experimental
        '''
        result = self._values.get("throttles_per_minute_threshold")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WatchLambdaFunctionOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-watchful.WatchLambdaFunctionProps",
    jsii_struct_bases=[WatchLambdaFunctionOptions],
    name_mapping={
        "duration_threshold_percent": "durationThresholdPercent",
        "errors_per_minute_threshold": "errorsPerMinuteThreshold",
        "throttles_per_minute_threshold": "throttlesPerMinuteThreshold",
        "fn": "fn",
        "title": "title",
        "watchful": "watchful",
    },
)
class WatchLambdaFunctionProps(WatchLambdaFunctionOptions):
    def __init__(
        self,
        *,
        duration_threshold_percent: typing.Optional[jsii.Number] = None,
        errors_per_minute_threshold: typing.Optional[jsii.Number] = None,
        throttles_per_minute_threshold: typing.Optional[jsii.Number] = None,
        fn: _aws_cdk_aws_lambda_ceddda9d.Function,
        title: builtins.str,
        watchful: IWatchful,
    ) -> None:
        '''
        :param duration_threshold_percent: (experimental) Threshold for the duration alarm as percentage of the function's timeout value. If this is set to 50%, the alarm will be set when p99 latency of the function exceeds 50% of the function's timeout setting. Default: 80
        :param errors_per_minute_threshold: (experimental) Number of allowed errors per minute. If there are more errors than that, an alarm will trigger. Default: 0
        :param throttles_per_minute_threshold: (experimental) Number of allowed throttles per minute. Default: 0
        :param fn: 
        :param title: 
        :param watchful: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d8c569e0c54cd7730b6905d48e90b1aede79ac96817f2aa8096d98695b5780d)
            check_type(argname="argument duration_threshold_percent", value=duration_threshold_percent, expected_type=type_hints["duration_threshold_percent"])
            check_type(argname="argument errors_per_minute_threshold", value=errors_per_minute_threshold, expected_type=type_hints["errors_per_minute_threshold"])
            check_type(argname="argument throttles_per_minute_threshold", value=throttles_per_minute_threshold, expected_type=type_hints["throttles_per_minute_threshold"])
            check_type(argname="argument fn", value=fn, expected_type=type_hints["fn"])
            check_type(argname="argument title", value=title, expected_type=type_hints["title"])
            check_type(argname="argument watchful", value=watchful, expected_type=type_hints["watchful"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "fn": fn,
            "title": title,
            "watchful": watchful,
        }
        if duration_threshold_percent is not None:
            self._values["duration_threshold_percent"] = duration_threshold_percent
        if errors_per_minute_threshold is not None:
            self._values["errors_per_minute_threshold"] = errors_per_minute_threshold
        if throttles_per_minute_threshold is not None:
            self._values["throttles_per_minute_threshold"] = throttles_per_minute_threshold

    @builtins.property
    def duration_threshold_percent(self) -> typing.Optional[jsii.Number]:
        '''(experimental) Threshold for the duration alarm as percentage of the function's timeout value.

        If this is set to 50%, the alarm will be set when p99 latency of the
        function exceeds 50% of the function's timeout setting.

        :default: 80

        :stability: experimental
        '''
        result = self._values.get("duration_threshold_percent")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def errors_per_minute_threshold(self) -> typing.Optional[jsii.Number]:
        '''(experimental) Number of allowed errors per minute.

        If there are more errors than that, an alarm will trigger.

        :default: 0

        :stability: experimental
        '''
        result = self._values.get("errors_per_minute_threshold")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def throttles_per_minute_threshold(self) -> typing.Optional[jsii.Number]:
        '''(experimental) Number of allowed throttles per minute.

        :default: 0

        :stability: experimental
        '''
        result = self._values.get("throttles_per_minute_threshold")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def fn(self) -> _aws_cdk_aws_lambda_ceddda9d.Function:
        '''
        :stability: experimental
        '''
        result = self._values.get("fn")
        assert result is not None, "Required property 'fn' is missing"
        return typing.cast(_aws_cdk_aws_lambda_ceddda9d.Function, result)

    @builtins.property
    def title(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        result = self._values.get("title")
        assert result is not None, "Required property 'title' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def watchful(self) -> IWatchful:
        '''
        :stability: experimental
        '''
        result = self._values.get("watchful")
        assert result is not None, "Required property 'watchful' is missing"
        return typing.cast(IWatchful, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WatchLambdaFunctionProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class WatchRdsAurora(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-watchful.WatchRdsAurora",
):
    '''
    :stability: experimental
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        cluster: _aws_cdk_aws_rds_ceddda9d.DatabaseCluster,
        title: builtins.str,
        watchful: IWatchful,
        cpu_maximum_threshold_percent: typing.Optional[jsii.Number] = None,
        db_buffer_cache_minimum_threshold: typing.Optional[jsii.Number] = None,
        db_connections_maximum_threshold: typing.Optional[jsii.Number] = None,
        db_replica_lag_maximum_threshold: typing.Optional[jsii.Number] = None,
        db_throughput_maximum_threshold: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param cluster: 
        :param title: 
        :param watchful: 
        :param cpu_maximum_threshold_percent: (experimental) Threshold for the Cpu Maximum utilization. Default: 80
        :param db_buffer_cache_minimum_threshold: (experimental) Threshold for the Minimum Db Buffer Cache. Default: - 0.
        :param db_connections_maximum_threshold: (experimental) Threshold for the Maximum Db Connections. Default: - 0.
        :param db_replica_lag_maximum_threshold: (experimental) Threshold for the Maximum Db ReplicaLag. Default: - 0.
        :param db_throughput_maximum_threshold: (experimental) Threshold for the Maximum Db Throughput. Default: - 0.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__76a745a0fc50edadaef32f7bff924046bb7874cfadfd2149bed0cd76a7bc0258)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = WatchRdsAuroraProps(
            cluster=cluster,
            title=title,
            watchful=watchful,
            cpu_maximum_threshold_percent=cpu_maximum_threshold_percent,
            db_buffer_cache_minimum_threshold=db_buffer_cache_minimum_threshold,
            db_connections_maximum_threshold=db_connections_maximum_threshold,
            db_replica_lag_maximum_threshold=db_replica_lag_maximum_threshold,
            db_throughput_maximum_threshold=db_throughput_maximum_threshold,
        )

        jsii.create(self.__class__, self, [scope, id, props])


@jsii.data_type(
    jsii_type="cdk-watchful.WatchRdsAuroraOptions",
    jsii_struct_bases=[],
    name_mapping={
        "cpu_maximum_threshold_percent": "cpuMaximumThresholdPercent",
        "db_buffer_cache_minimum_threshold": "dbBufferCacheMinimumThreshold",
        "db_connections_maximum_threshold": "dbConnectionsMaximumThreshold",
        "db_replica_lag_maximum_threshold": "dbReplicaLagMaximumThreshold",
        "db_throughput_maximum_threshold": "dbThroughputMaximumThreshold",
    },
)
class WatchRdsAuroraOptions:
    def __init__(
        self,
        *,
        cpu_maximum_threshold_percent: typing.Optional[jsii.Number] = None,
        db_buffer_cache_minimum_threshold: typing.Optional[jsii.Number] = None,
        db_connections_maximum_threshold: typing.Optional[jsii.Number] = None,
        db_replica_lag_maximum_threshold: typing.Optional[jsii.Number] = None,
        db_throughput_maximum_threshold: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param cpu_maximum_threshold_percent: (experimental) Threshold for the Cpu Maximum utilization. Default: 80
        :param db_buffer_cache_minimum_threshold: (experimental) Threshold for the Minimum Db Buffer Cache. Default: - 0.
        :param db_connections_maximum_threshold: (experimental) Threshold for the Maximum Db Connections. Default: - 0.
        :param db_replica_lag_maximum_threshold: (experimental) Threshold for the Maximum Db ReplicaLag. Default: - 0.
        :param db_throughput_maximum_threshold: (experimental) Threshold for the Maximum Db Throughput. Default: - 0.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__85f245665543cf75cc1ae7d280a4a0571dfc337140a2b43a09115250db30da45)
            check_type(argname="argument cpu_maximum_threshold_percent", value=cpu_maximum_threshold_percent, expected_type=type_hints["cpu_maximum_threshold_percent"])
            check_type(argname="argument db_buffer_cache_minimum_threshold", value=db_buffer_cache_minimum_threshold, expected_type=type_hints["db_buffer_cache_minimum_threshold"])
            check_type(argname="argument db_connections_maximum_threshold", value=db_connections_maximum_threshold, expected_type=type_hints["db_connections_maximum_threshold"])
            check_type(argname="argument db_replica_lag_maximum_threshold", value=db_replica_lag_maximum_threshold, expected_type=type_hints["db_replica_lag_maximum_threshold"])
            check_type(argname="argument db_throughput_maximum_threshold", value=db_throughput_maximum_threshold, expected_type=type_hints["db_throughput_maximum_threshold"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if cpu_maximum_threshold_percent is not None:
            self._values["cpu_maximum_threshold_percent"] = cpu_maximum_threshold_percent
        if db_buffer_cache_minimum_threshold is not None:
            self._values["db_buffer_cache_minimum_threshold"] = db_buffer_cache_minimum_threshold
        if db_connections_maximum_threshold is not None:
            self._values["db_connections_maximum_threshold"] = db_connections_maximum_threshold
        if db_replica_lag_maximum_threshold is not None:
            self._values["db_replica_lag_maximum_threshold"] = db_replica_lag_maximum_threshold
        if db_throughput_maximum_threshold is not None:
            self._values["db_throughput_maximum_threshold"] = db_throughput_maximum_threshold

    @builtins.property
    def cpu_maximum_threshold_percent(self) -> typing.Optional[jsii.Number]:
        '''(experimental) Threshold for the Cpu Maximum utilization.

        :default: 80

        :stability: experimental
        '''
        result = self._values.get("cpu_maximum_threshold_percent")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def db_buffer_cache_minimum_threshold(self) -> typing.Optional[jsii.Number]:
        '''(experimental) Threshold for the Minimum Db Buffer Cache.

        :default:

        -
        0.

        :stability: experimental
        '''
        result = self._values.get("db_buffer_cache_minimum_threshold")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def db_connections_maximum_threshold(self) -> typing.Optional[jsii.Number]:
        '''(experimental) Threshold for the Maximum Db Connections.

        :default:

        -
        0.

        :stability: experimental
        '''
        result = self._values.get("db_connections_maximum_threshold")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def db_replica_lag_maximum_threshold(self) -> typing.Optional[jsii.Number]:
        '''(experimental) Threshold for the Maximum Db ReplicaLag.

        :default:

        -
        0.

        :stability: experimental
        '''
        result = self._values.get("db_replica_lag_maximum_threshold")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def db_throughput_maximum_threshold(self) -> typing.Optional[jsii.Number]:
        '''(experimental) Threshold for the Maximum Db Throughput.

        :default:

        -
        0.

        :stability: experimental
        '''
        result = self._values.get("db_throughput_maximum_threshold")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WatchRdsAuroraOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-watchful.WatchRdsAuroraProps",
    jsii_struct_bases=[WatchRdsAuroraOptions],
    name_mapping={
        "cpu_maximum_threshold_percent": "cpuMaximumThresholdPercent",
        "db_buffer_cache_minimum_threshold": "dbBufferCacheMinimumThreshold",
        "db_connections_maximum_threshold": "dbConnectionsMaximumThreshold",
        "db_replica_lag_maximum_threshold": "dbReplicaLagMaximumThreshold",
        "db_throughput_maximum_threshold": "dbThroughputMaximumThreshold",
        "cluster": "cluster",
        "title": "title",
        "watchful": "watchful",
    },
)
class WatchRdsAuroraProps(WatchRdsAuroraOptions):
    def __init__(
        self,
        *,
        cpu_maximum_threshold_percent: typing.Optional[jsii.Number] = None,
        db_buffer_cache_minimum_threshold: typing.Optional[jsii.Number] = None,
        db_connections_maximum_threshold: typing.Optional[jsii.Number] = None,
        db_replica_lag_maximum_threshold: typing.Optional[jsii.Number] = None,
        db_throughput_maximum_threshold: typing.Optional[jsii.Number] = None,
        cluster: _aws_cdk_aws_rds_ceddda9d.DatabaseCluster,
        title: builtins.str,
        watchful: IWatchful,
    ) -> None:
        '''
        :param cpu_maximum_threshold_percent: (experimental) Threshold for the Cpu Maximum utilization. Default: 80
        :param db_buffer_cache_minimum_threshold: (experimental) Threshold for the Minimum Db Buffer Cache. Default: - 0.
        :param db_connections_maximum_threshold: (experimental) Threshold for the Maximum Db Connections. Default: - 0.
        :param db_replica_lag_maximum_threshold: (experimental) Threshold for the Maximum Db ReplicaLag. Default: - 0.
        :param db_throughput_maximum_threshold: (experimental) Threshold for the Maximum Db Throughput. Default: - 0.
        :param cluster: 
        :param title: 
        :param watchful: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__561c9c2f686b4e6d4b2e3afdf9cad715205020fa4ed4843ae6111a10d6e04253)
            check_type(argname="argument cpu_maximum_threshold_percent", value=cpu_maximum_threshold_percent, expected_type=type_hints["cpu_maximum_threshold_percent"])
            check_type(argname="argument db_buffer_cache_minimum_threshold", value=db_buffer_cache_minimum_threshold, expected_type=type_hints["db_buffer_cache_minimum_threshold"])
            check_type(argname="argument db_connections_maximum_threshold", value=db_connections_maximum_threshold, expected_type=type_hints["db_connections_maximum_threshold"])
            check_type(argname="argument db_replica_lag_maximum_threshold", value=db_replica_lag_maximum_threshold, expected_type=type_hints["db_replica_lag_maximum_threshold"])
            check_type(argname="argument db_throughput_maximum_threshold", value=db_throughput_maximum_threshold, expected_type=type_hints["db_throughput_maximum_threshold"])
            check_type(argname="argument cluster", value=cluster, expected_type=type_hints["cluster"])
            check_type(argname="argument title", value=title, expected_type=type_hints["title"])
            check_type(argname="argument watchful", value=watchful, expected_type=type_hints["watchful"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "cluster": cluster,
            "title": title,
            "watchful": watchful,
        }
        if cpu_maximum_threshold_percent is not None:
            self._values["cpu_maximum_threshold_percent"] = cpu_maximum_threshold_percent
        if db_buffer_cache_minimum_threshold is not None:
            self._values["db_buffer_cache_minimum_threshold"] = db_buffer_cache_minimum_threshold
        if db_connections_maximum_threshold is not None:
            self._values["db_connections_maximum_threshold"] = db_connections_maximum_threshold
        if db_replica_lag_maximum_threshold is not None:
            self._values["db_replica_lag_maximum_threshold"] = db_replica_lag_maximum_threshold
        if db_throughput_maximum_threshold is not None:
            self._values["db_throughput_maximum_threshold"] = db_throughput_maximum_threshold

    @builtins.property
    def cpu_maximum_threshold_percent(self) -> typing.Optional[jsii.Number]:
        '''(experimental) Threshold for the Cpu Maximum utilization.

        :default: 80

        :stability: experimental
        '''
        result = self._values.get("cpu_maximum_threshold_percent")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def db_buffer_cache_minimum_threshold(self) -> typing.Optional[jsii.Number]:
        '''(experimental) Threshold for the Minimum Db Buffer Cache.

        :default:

        -
        0.

        :stability: experimental
        '''
        result = self._values.get("db_buffer_cache_minimum_threshold")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def db_connections_maximum_threshold(self) -> typing.Optional[jsii.Number]:
        '''(experimental) Threshold for the Maximum Db Connections.

        :default:

        -
        0.

        :stability: experimental
        '''
        result = self._values.get("db_connections_maximum_threshold")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def db_replica_lag_maximum_threshold(self) -> typing.Optional[jsii.Number]:
        '''(experimental) Threshold for the Maximum Db ReplicaLag.

        :default:

        -
        0.

        :stability: experimental
        '''
        result = self._values.get("db_replica_lag_maximum_threshold")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def db_throughput_maximum_threshold(self) -> typing.Optional[jsii.Number]:
        '''(experimental) Threshold for the Maximum Db Throughput.

        :default:

        -
        0.

        :stability: experimental
        '''
        result = self._values.get("db_throughput_maximum_threshold")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def cluster(self) -> _aws_cdk_aws_rds_ceddda9d.DatabaseCluster:
        '''
        :stability: experimental
        '''
        result = self._values.get("cluster")
        assert result is not None, "Required property 'cluster' is missing"
        return typing.cast(_aws_cdk_aws_rds_ceddda9d.DatabaseCluster, result)

    @builtins.property
    def title(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        result = self._values.get("title")
        assert result is not None, "Required property 'title' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def watchful(self) -> IWatchful:
        '''
        :stability: experimental
        '''
        result = self._values.get("watchful")
        assert result is not None, "Required property 'watchful' is missing"
        return typing.cast(IWatchful, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WatchRdsAuroraProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class WatchStateMachine(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-watchful.WatchStateMachine",
):
    '''
    :stability: experimental
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        state_machine: _aws_cdk_aws_stepfunctions_ceddda9d.StateMachine,
        title: builtins.str,
        watchful: IWatchful,
        metric_failed_threshold: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param state_machine: 
        :param title: 
        :param watchful: 
        :param metric_failed_threshold: (experimental) Alarm when execution failures reach this threshold over 1 minute. Default: 1 any execution failure will trigger the alarm

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__125259c5c53b70d8c810c76fc4a108526d5990c627d97f0ed0cf533f56da4b77)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = WatchStateMachineProps(
            state_machine=state_machine,
            title=title,
            watchful=watchful,
            metric_failed_threshold=metric_failed_threshold,
        )

        jsii.create(self.__class__, self, [scope, id, props])


@jsii.data_type(
    jsii_type="cdk-watchful.WatchStateMachineOptions",
    jsii_struct_bases=[],
    name_mapping={"metric_failed_threshold": "metricFailedThreshold"},
)
class WatchStateMachineOptions:
    def __init__(
        self,
        *,
        metric_failed_threshold: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param metric_failed_threshold: (experimental) Alarm when execution failures reach this threshold over 1 minute. Default: 1 any execution failure will trigger the alarm

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__68e3e081e4f633ec6d9114fb3aa07047d9644a1157dbd3cb9052cc8cbff02390)
            check_type(argname="argument metric_failed_threshold", value=metric_failed_threshold, expected_type=type_hints["metric_failed_threshold"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if metric_failed_threshold is not None:
            self._values["metric_failed_threshold"] = metric_failed_threshold

    @builtins.property
    def metric_failed_threshold(self) -> typing.Optional[jsii.Number]:
        '''(experimental) Alarm when execution failures reach this threshold over 1 minute.

        :default: 1 any execution failure will trigger the alarm

        :stability: experimental
        '''
        result = self._values.get("metric_failed_threshold")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WatchStateMachineOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-watchful.WatchStateMachineProps",
    jsii_struct_bases=[WatchStateMachineOptions],
    name_mapping={
        "metric_failed_threshold": "metricFailedThreshold",
        "state_machine": "stateMachine",
        "title": "title",
        "watchful": "watchful",
    },
)
class WatchStateMachineProps(WatchStateMachineOptions):
    def __init__(
        self,
        *,
        metric_failed_threshold: typing.Optional[jsii.Number] = None,
        state_machine: _aws_cdk_aws_stepfunctions_ceddda9d.StateMachine,
        title: builtins.str,
        watchful: IWatchful,
    ) -> None:
        '''
        :param metric_failed_threshold: (experimental) Alarm when execution failures reach this threshold over 1 minute. Default: 1 any execution failure will trigger the alarm
        :param state_machine: 
        :param title: 
        :param watchful: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__297a4bfa8fa52e0093aab696e5addca75990afcf727bf5c7343a686845e28cc8)
            check_type(argname="argument metric_failed_threshold", value=metric_failed_threshold, expected_type=type_hints["metric_failed_threshold"])
            check_type(argname="argument state_machine", value=state_machine, expected_type=type_hints["state_machine"])
            check_type(argname="argument title", value=title, expected_type=type_hints["title"])
            check_type(argname="argument watchful", value=watchful, expected_type=type_hints["watchful"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "state_machine": state_machine,
            "title": title,
            "watchful": watchful,
        }
        if metric_failed_threshold is not None:
            self._values["metric_failed_threshold"] = metric_failed_threshold

    @builtins.property
    def metric_failed_threshold(self) -> typing.Optional[jsii.Number]:
        '''(experimental) Alarm when execution failures reach this threshold over 1 minute.

        :default: 1 any execution failure will trigger the alarm

        :stability: experimental
        '''
        result = self._values.get("metric_failed_threshold")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def state_machine(self) -> _aws_cdk_aws_stepfunctions_ceddda9d.StateMachine:
        '''
        :stability: experimental
        '''
        result = self._values.get("state_machine")
        assert result is not None, "Required property 'state_machine' is missing"
        return typing.cast(_aws_cdk_aws_stepfunctions_ceddda9d.StateMachine, result)

    @builtins.property
    def title(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        result = self._values.get("title")
        assert result is not None, "Required property 'title' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def watchful(self) -> IWatchful:
        '''
        :stability: experimental
        '''
        result = self._values.get("watchful")
        assert result is not None, "Required property 'watchful' is missing"
        return typing.cast(IWatchful, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WatchStateMachineProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-watchful.WatchedOperation",
    jsii_struct_bases=[],
    name_mapping={"http_method": "httpMethod", "resource_path": "resourcePath"},
)
class WatchedOperation:
    def __init__(
        self,
        *,
        http_method: builtins.str,
        resource_path: builtins.str,
    ) -> None:
        '''(experimental) An operation (path and method) worth monitoring.

        :param http_method: (experimental) The HTTP method for the operation (GET, POST, ...).
        :param resource_path: (experimental) The REST API path for this operation (/, /resource/{id}, ...).

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e4b42e617171dedf1b6259f9dd2b52fac00e067fc7699f78fb24cc14bddf2aec)
            check_type(argname="argument http_method", value=http_method, expected_type=type_hints["http_method"])
            check_type(argname="argument resource_path", value=resource_path, expected_type=type_hints["resource_path"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "http_method": http_method,
            "resource_path": resource_path,
        }

    @builtins.property
    def http_method(self) -> builtins.str:
        '''(experimental) The HTTP method for the operation (GET, POST, ...).

        :stability: experimental
        '''
        result = self._values.get("http_method")
        assert result is not None, "Required property 'http_method' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def resource_path(self) -> builtins.str:
        '''(experimental) The REST API path for this operation (/, /resource/{id}, ...).

        :stability: experimental
        '''
        result = self._values.get("resource_path")
        assert result is not None, "Required property 'resource_path' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WatchedOperation(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(IWatchful)
class Watchful(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-watchful.Watchful",
):
    '''
    :stability: experimental
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        alarm_action_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
        alarm_actions: typing.Optional[typing.Sequence[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction]] = None,
        alarm_email: typing.Optional[builtins.str] = None,
        alarm_sns: typing.Optional[_aws_cdk_aws_sns_ceddda9d.ITopic] = None,
        alarm_sqs: typing.Optional[_aws_cdk_aws_sqs_ceddda9d.IQueue] = None,
        dashboard: typing.Optional[builtins.bool] = None,
        dashboard_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param alarm_action_arns: (experimental) ARNs of actions to perform when alarms go off. These actions are in addition to email/sqs/sns. Default: [] You can use ``alarmActions`` instead as a strongly-typed alternative.
        :param alarm_actions: (experimental) CloudWatch alarm actions to perform when alarms go off. These actions are in addition to email/sqs/sns.
        :param alarm_email: (experimental) Email address to send alarms to. Default: - alarms are not sent to an email recipient.
        :param alarm_sns: (experimental) SNS topic to send alarms to. Default: - alarms are not sent to an SNS Topic.
        :param alarm_sqs: (experimental) SQS queue to send alarms to. Default: - alarms are not sent to an SQS queue.
        :param dashboard: (experimental) Whether to generate CloudWatch dashboards. Default: true
        :param dashboard_name: (experimental) The name of the CloudWatch dashboard generated by Watchful. Default: - auto-generated

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7564a98e4b044f8676d7939c4da2025d97eb0194bce396ab765f27b0f0adbe5d)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = WatchfulProps(
            alarm_action_arns=alarm_action_arns,
            alarm_actions=alarm_actions,
            alarm_email=alarm_email,
            alarm_sns=alarm_sns,
            alarm_sqs=alarm_sqs,
            dashboard=dashboard,
            dashboard_name=dashboard_name,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="addAlarm")
    def add_alarm(self, alarm: _aws_cdk_aws_cloudwatch_ceddda9d.IAlarm) -> None:
        '''
        :param alarm: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e2198727e4ee335e57849731e35a1f290056825dc749fac2021196c88241ed59)
            check_type(argname="argument alarm", value=alarm, expected_type=type_hints["alarm"])
        return typing.cast(None, jsii.invoke(self, "addAlarm", [alarm]))

    @jsii.member(jsii_name="addSection")
    def add_section(
        self,
        title: builtins.str,
        *,
        links: typing.Optional[typing.Sequence[typing.Union[QuickLink, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''
        :param title: -
        :param links: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc48bd65e1cc426a4ef26a93e6ecfd4496e6b2d1e631c8e1a15f95f4cfad06d4)
            check_type(argname="argument title", value=title, expected_type=type_hints["title"])
        options = SectionOptions(links=links)

        return typing.cast(None, jsii.invoke(self, "addSection", [title, options]))

    @jsii.member(jsii_name="addWidgets")
    def add_widgets(self, *widgets: _aws_cdk_aws_cloudwatch_ceddda9d.IWidget) -> None:
        '''
        :param widgets: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a38739559ff69bca7c8cc62caf01325d7b75ca29640d987ebd87981ab212fbc6)
            check_type(argname="argument widgets", value=widgets, expected_type=typing.Tuple[type_hints["widgets"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast(None, jsii.invoke(self, "addWidgets", [*widgets]))

    @jsii.member(jsii_name="watchApiGateway")
    def watch_api_gateway(
        self,
        title: builtins.str,
        rest_api: _aws_cdk_aws_apigateway_ceddda9d.RestApi,
        *,
        cache_graph: typing.Optional[builtins.bool] = None,
        server_error_threshold: typing.Optional[jsii.Number] = None,
        watched_operations: typing.Optional[typing.Sequence[typing.Union[WatchedOperation, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> WatchApiGateway:
        '''
        :param title: -
        :param rest_api: -
        :param cache_graph: (experimental) Include a dashboard graph for caching metrics. Default: false
        :param server_error_threshold: (experimental) Alarm when 5XX errors reach this threshold over 5 minutes. Default: 1 any 5xx HTTP response will trigger the alarm
        :param watched_operations: (experimental) A list of operations to monitor separately. Default: - only API-level monitoring is added.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8c443a383639717c77674d40d3b055a45984d6d217eb42208530310f5ebeffce)
            check_type(argname="argument title", value=title, expected_type=type_hints["title"])
            check_type(argname="argument rest_api", value=rest_api, expected_type=type_hints["rest_api"])
        options = WatchApiGatewayOptions(
            cache_graph=cache_graph,
            server_error_threshold=server_error_threshold,
            watched_operations=watched_operations,
        )

        return typing.cast(WatchApiGateway, jsii.invoke(self, "watchApiGateway", [title, rest_api, options]))

    @jsii.member(jsii_name="watchDynamoTable")
    def watch_dynamo_table(
        self,
        title: builtins.str,
        table: _aws_cdk_aws_dynamodb_ceddda9d.Table,
        *,
        read_capacity_threshold_percent: typing.Optional[jsii.Number] = None,
        write_capacity_threshold_percent: typing.Optional[jsii.Number] = None,
    ) -> WatchDynamoTable:
        '''
        :param title: -
        :param table: -
        :param read_capacity_threshold_percent: (experimental) Threshold for read capacity alarm (percentage). Default: 80
        :param write_capacity_threshold_percent: (experimental) Threshold for read capacity alarm (percentage). Default: 80

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e2eab1523884528dc3f2b11381e7e427a70dd06bfd5de863d30d0aa033d81cc6)
            check_type(argname="argument title", value=title, expected_type=type_hints["title"])
            check_type(argname="argument table", value=table, expected_type=type_hints["table"])
        options = WatchDynamoTableOptions(
            read_capacity_threshold_percent=read_capacity_threshold_percent,
            write_capacity_threshold_percent=write_capacity_threshold_percent,
        )

        return typing.cast(WatchDynamoTable, jsii.invoke(self, "watchDynamoTable", [title, table, options]))

    @jsii.member(jsii_name="watchEc2Ecs")
    def watch_ec2_ecs(
        self,
        title: builtins.str,
        ec2_service: _aws_cdk_aws_ecs_ceddda9d.Ec2Service,
        target_group: _aws_cdk_aws_elasticloadbalancingv2_ceddda9d.ApplicationTargetGroup,
        *,
        cpu_maximum_threshold_percent: typing.Optional[jsii.Number] = None,
        memory_maximum_threshold_percent: typing.Optional[jsii.Number] = None,
        requests_error_rate_threshold: typing.Optional[jsii.Number] = None,
        requests_threshold: typing.Optional[jsii.Number] = None,
        target_response_time_threshold: typing.Optional[jsii.Number] = None,
    ) -> WatchEcsService:
        '''
        :param title: -
        :param ec2_service: -
        :param target_group: -
        :param cpu_maximum_threshold_percent: (experimental) Threshold for the Cpu Maximum utilization. Default: 80
        :param memory_maximum_threshold_percent: (experimental) Threshold for the Memory Maximum utilization. Default: - 0.
        :param requests_error_rate_threshold: (experimental) Threshold for the Number of Request Errors. Default: - 0.
        :param requests_threshold: (experimental) Threshold for the Number of Requests. Default: - 0.
        :param target_response_time_threshold: (experimental) Threshold for the Target Response Time. Default: - 0.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a570aa382f762cfddf7b6cbde8b935d2af4087da53e13faafc0abb20eafaba65)
            check_type(argname="argument title", value=title, expected_type=type_hints["title"])
            check_type(argname="argument ec2_service", value=ec2_service, expected_type=type_hints["ec2_service"])
            check_type(argname="argument target_group", value=target_group, expected_type=type_hints["target_group"])
        options = WatchEcsServiceOptions(
            cpu_maximum_threshold_percent=cpu_maximum_threshold_percent,
            memory_maximum_threshold_percent=memory_maximum_threshold_percent,
            requests_error_rate_threshold=requests_error_rate_threshold,
            requests_threshold=requests_threshold,
            target_response_time_threshold=target_response_time_threshold,
        )

        return typing.cast(WatchEcsService, jsii.invoke(self, "watchEc2Ecs", [title, ec2_service, target_group, options]))

    @jsii.member(jsii_name="watchFargateEcs")
    def watch_fargate_ecs(
        self,
        title: builtins.str,
        fargate_service: _aws_cdk_aws_ecs_ceddda9d.FargateService,
        target_group: _aws_cdk_aws_elasticloadbalancingv2_ceddda9d.ApplicationTargetGroup,
        *,
        cpu_maximum_threshold_percent: typing.Optional[jsii.Number] = None,
        memory_maximum_threshold_percent: typing.Optional[jsii.Number] = None,
        requests_error_rate_threshold: typing.Optional[jsii.Number] = None,
        requests_threshold: typing.Optional[jsii.Number] = None,
        target_response_time_threshold: typing.Optional[jsii.Number] = None,
    ) -> WatchEcsService:
        '''
        :param title: -
        :param fargate_service: -
        :param target_group: -
        :param cpu_maximum_threshold_percent: (experimental) Threshold for the Cpu Maximum utilization. Default: 80
        :param memory_maximum_threshold_percent: (experimental) Threshold for the Memory Maximum utilization. Default: - 0.
        :param requests_error_rate_threshold: (experimental) Threshold for the Number of Request Errors. Default: - 0.
        :param requests_threshold: (experimental) Threshold for the Number of Requests. Default: - 0.
        :param target_response_time_threshold: (experimental) Threshold for the Target Response Time. Default: - 0.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4012b8ed38cdbc11cfd4bc404f63fb1efa3142774e054942ffe56628244f6d7f)
            check_type(argname="argument title", value=title, expected_type=type_hints["title"])
            check_type(argname="argument fargate_service", value=fargate_service, expected_type=type_hints["fargate_service"])
            check_type(argname="argument target_group", value=target_group, expected_type=type_hints["target_group"])
        options = WatchEcsServiceOptions(
            cpu_maximum_threshold_percent=cpu_maximum_threshold_percent,
            memory_maximum_threshold_percent=memory_maximum_threshold_percent,
            requests_error_rate_threshold=requests_error_rate_threshold,
            requests_threshold=requests_threshold,
            target_response_time_threshold=target_response_time_threshold,
        )

        return typing.cast(WatchEcsService, jsii.invoke(self, "watchFargateEcs", [title, fargate_service, target_group, options]))

    @jsii.member(jsii_name="watchLambdaFunction")
    def watch_lambda_function(
        self,
        title: builtins.str,
        fn: _aws_cdk_aws_lambda_ceddda9d.Function,
        *,
        duration_threshold_percent: typing.Optional[jsii.Number] = None,
        errors_per_minute_threshold: typing.Optional[jsii.Number] = None,
        throttles_per_minute_threshold: typing.Optional[jsii.Number] = None,
    ) -> WatchLambdaFunction:
        '''
        :param title: -
        :param fn: -
        :param duration_threshold_percent: (experimental) Threshold for the duration alarm as percentage of the function's timeout value. If this is set to 50%, the alarm will be set when p99 latency of the function exceeds 50% of the function's timeout setting. Default: 80
        :param errors_per_minute_threshold: (experimental) Number of allowed errors per minute. If there are more errors than that, an alarm will trigger. Default: 0
        :param throttles_per_minute_threshold: (experimental) Number of allowed throttles per minute. Default: 0

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5a4904fba7e78fc09a6690c3cc08c6b2149ef0ad4fb8a5aa7ffd5214d78b3451)
            check_type(argname="argument title", value=title, expected_type=type_hints["title"])
            check_type(argname="argument fn", value=fn, expected_type=type_hints["fn"])
        options = WatchLambdaFunctionOptions(
            duration_threshold_percent=duration_threshold_percent,
            errors_per_minute_threshold=errors_per_minute_threshold,
            throttles_per_minute_threshold=throttles_per_minute_threshold,
        )

        return typing.cast(WatchLambdaFunction, jsii.invoke(self, "watchLambdaFunction", [title, fn, options]))

    @jsii.member(jsii_name="watchRdsAuroraCluster")
    def watch_rds_aurora_cluster(
        self,
        title: builtins.str,
        cluster: _aws_cdk_aws_rds_ceddda9d.DatabaseCluster,
        *,
        cpu_maximum_threshold_percent: typing.Optional[jsii.Number] = None,
        db_buffer_cache_minimum_threshold: typing.Optional[jsii.Number] = None,
        db_connections_maximum_threshold: typing.Optional[jsii.Number] = None,
        db_replica_lag_maximum_threshold: typing.Optional[jsii.Number] = None,
        db_throughput_maximum_threshold: typing.Optional[jsii.Number] = None,
    ) -> WatchRdsAurora:
        '''
        :param title: -
        :param cluster: -
        :param cpu_maximum_threshold_percent: (experimental) Threshold for the Cpu Maximum utilization. Default: 80
        :param db_buffer_cache_minimum_threshold: (experimental) Threshold for the Minimum Db Buffer Cache. Default: - 0.
        :param db_connections_maximum_threshold: (experimental) Threshold for the Maximum Db Connections. Default: - 0.
        :param db_replica_lag_maximum_threshold: (experimental) Threshold for the Maximum Db ReplicaLag. Default: - 0.
        :param db_throughput_maximum_threshold: (experimental) Threshold for the Maximum Db Throughput. Default: - 0.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0fd82650cf8c0d95dcc6fd4b9d44c6ba7bfe500dd497b586c07d735f393540c7)
            check_type(argname="argument title", value=title, expected_type=type_hints["title"])
            check_type(argname="argument cluster", value=cluster, expected_type=type_hints["cluster"])
        options = WatchRdsAuroraOptions(
            cpu_maximum_threshold_percent=cpu_maximum_threshold_percent,
            db_buffer_cache_minimum_threshold=db_buffer_cache_minimum_threshold,
            db_connections_maximum_threshold=db_connections_maximum_threshold,
            db_replica_lag_maximum_threshold=db_replica_lag_maximum_threshold,
            db_throughput_maximum_threshold=db_throughput_maximum_threshold,
        )

        return typing.cast(WatchRdsAurora, jsii.invoke(self, "watchRdsAuroraCluster", [title, cluster, options]))

    @jsii.member(jsii_name="watchScope")
    def watch_scope(
        self,
        scope: _constructs_77d1e7e8.Construct,
        *,
        api_gateway: typing.Optional[builtins.bool] = None,
        dynamodb: typing.Optional[builtins.bool] = None,
        ec2ecs: typing.Optional[builtins.bool] = None,
        fargateecs: typing.Optional[builtins.bool] = None,
        lambda_: typing.Optional[builtins.bool] = None,
        rdsaurora: typing.Optional[builtins.bool] = None,
        state_machine: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param scope: -
        :param api_gateway: (experimental) Automatically watch API Gateway APIs in the scope. Default: true
        :param dynamodb: (experimental) Automatically watch all Amazon DynamoDB tables in the scope. Default: true
        :param ec2ecs: (experimental) Automatically watch ApplicationLoadBalanced EC2 Ecs Services in the scope (using ECS Pattern). Default: true
        :param fargateecs: (experimental) Automatically watch ApplicationLoadBalanced Fargate Ecs Services in the scope (using ECS Pattern). Default: true
        :param lambda_: (experimental) Automatically watch AWS Lambda functions in the scope. Default: true
        :param rdsaurora: (experimental) Automatically watch RDS Aurora clusters in the scope. Default: true
        :param state_machine: (experimental) Automatically watch AWS state machines in the scope. Default: true

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a534f488fc35b6330ed8a66990a07e8dce87ba70c70083ca5ccb8bb982ef1de3)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
        options = WatchfulAspectProps(
            api_gateway=api_gateway,
            dynamodb=dynamodb,
            ec2ecs=ec2ecs,
            fargateecs=fargateecs,
            lambda_=lambda_,
            rdsaurora=rdsaurora,
            state_machine=state_machine,
        )

        return typing.cast(None, jsii.invoke(self, "watchScope", [scope, options]))

    @jsii.member(jsii_name="watchStateMachine")
    def watch_state_machine(
        self,
        title: builtins.str,
        state_machine: _aws_cdk_aws_stepfunctions_ceddda9d.StateMachine,
        *,
        metric_failed_threshold: typing.Optional[jsii.Number] = None,
    ) -> WatchStateMachine:
        '''
        :param title: -
        :param state_machine: -
        :param metric_failed_threshold: (experimental) Alarm when execution failures reach this threshold over 1 minute. Default: 1 any execution failure will trigger the alarm

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1a909168e32be61e26336586d2aa49e1379e3aeea23928e9715502a96f2c8d83)
            check_type(argname="argument title", value=title, expected_type=type_hints["title"])
            check_type(argname="argument state_machine", value=state_machine, expected_type=type_hints["state_machine"])
        options = WatchStateMachineOptions(
            metric_failed_threshold=metric_failed_threshold
        )

        return typing.cast(WatchStateMachine, jsii.invoke(self, "watchStateMachine", [title, state_machine, options]))


@jsii.implements(_aws_cdk_ceddda9d.IAspect)
class WatchfulAspect(metaclass=jsii.JSIIMeta, jsii_type="cdk-watchful.WatchfulAspect"):
    '''(experimental) A CDK aspect that can automatically watch all resources within a scope.

    :stability: experimental
    '''

    def __init__(
        self,
        watchful: Watchful,
        *,
        api_gateway: typing.Optional[builtins.bool] = None,
        dynamodb: typing.Optional[builtins.bool] = None,
        ec2ecs: typing.Optional[builtins.bool] = None,
        fargateecs: typing.Optional[builtins.bool] = None,
        lambda_: typing.Optional[builtins.bool] = None,
        rdsaurora: typing.Optional[builtins.bool] = None,
        state_machine: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''(experimental) Defines a watchful aspect.

        :param watchful: The watchful to add those resources to.
        :param api_gateway: (experimental) Automatically watch API Gateway APIs in the scope. Default: true
        :param dynamodb: (experimental) Automatically watch all Amazon DynamoDB tables in the scope. Default: true
        :param ec2ecs: (experimental) Automatically watch ApplicationLoadBalanced EC2 Ecs Services in the scope (using ECS Pattern). Default: true
        :param fargateecs: (experimental) Automatically watch ApplicationLoadBalanced Fargate Ecs Services in the scope (using ECS Pattern). Default: true
        :param lambda_: (experimental) Automatically watch AWS Lambda functions in the scope. Default: true
        :param rdsaurora: (experimental) Automatically watch RDS Aurora clusters in the scope. Default: true
        :param state_machine: (experimental) Automatically watch AWS state machines in the scope. Default: true

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__80dfcd3cce42fa0ea903c7285a2b839e46b053ab1cd0a1f3d972fb6b6173a652)
            check_type(argname="argument watchful", value=watchful, expected_type=type_hints["watchful"])
        props = WatchfulAspectProps(
            api_gateway=api_gateway,
            dynamodb=dynamodb,
            ec2ecs=ec2ecs,
            fargateecs=fargateecs,
            lambda_=lambda_,
            rdsaurora=rdsaurora,
            state_machine=state_machine,
        )

        jsii.create(self.__class__, self, [watchful, props])

    @jsii.member(jsii_name="visit")
    def visit(self, node: _constructs_77d1e7e8.IConstruct) -> None:
        '''(experimental) All aspects can visit an IConstruct.

        :param node: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__076bb3367ef7233087eb63e2f3f698ea80e1862dbb6ac729a5bf4612b5486db6)
            check_type(argname="argument node", value=node, expected_type=type_hints["node"])
        return typing.cast(None, jsii.invoke(self, "visit", [node]))


@jsii.data_type(
    jsii_type="cdk-watchful.WatchfulAspectProps",
    jsii_struct_bases=[],
    name_mapping={
        "api_gateway": "apiGateway",
        "dynamodb": "dynamodb",
        "ec2ecs": "ec2ecs",
        "fargateecs": "fargateecs",
        "lambda_": "lambda",
        "rdsaurora": "rdsaurora",
        "state_machine": "stateMachine",
    },
)
class WatchfulAspectProps:
    def __init__(
        self,
        *,
        api_gateway: typing.Optional[builtins.bool] = None,
        dynamodb: typing.Optional[builtins.bool] = None,
        ec2ecs: typing.Optional[builtins.bool] = None,
        fargateecs: typing.Optional[builtins.bool] = None,
        lambda_: typing.Optional[builtins.bool] = None,
        rdsaurora: typing.Optional[builtins.bool] = None,
        state_machine: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param api_gateway: (experimental) Automatically watch API Gateway APIs in the scope. Default: true
        :param dynamodb: (experimental) Automatically watch all Amazon DynamoDB tables in the scope. Default: true
        :param ec2ecs: (experimental) Automatically watch ApplicationLoadBalanced EC2 Ecs Services in the scope (using ECS Pattern). Default: true
        :param fargateecs: (experimental) Automatically watch ApplicationLoadBalanced Fargate Ecs Services in the scope (using ECS Pattern). Default: true
        :param lambda_: (experimental) Automatically watch AWS Lambda functions in the scope. Default: true
        :param rdsaurora: (experimental) Automatically watch RDS Aurora clusters in the scope. Default: true
        :param state_machine: (experimental) Automatically watch AWS state machines in the scope. Default: true

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e6a9147c3f37fca972904f2ae3b116f2def8614de6af707df3d7df594ea1866)
            check_type(argname="argument api_gateway", value=api_gateway, expected_type=type_hints["api_gateway"])
            check_type(argname="argument dynamodb", value=dynamodb, expected_type=type_hints["dynamodb"])
            check_type(argname="argument ec2ecs", value=ec2ecs, expected_type=type_hints["ec2ecs"])
            check_type(argname="argument fargateecs", value=fargateecs, expected_type=type_hints["fargateecs"])
            check_type(argname="argument lambda_", value=lambda_, expected_type=type_hints["lambda_"])
            check_type(argname="argument rdsaurora", value=rdsaurora, expected_type=type_hints["rdsaurora"])
            check_type(argname="argument state_machine", value=state_machine, expected_type=type_hints["state_machine"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if api_gateway is not None:
            self._values["api_gateway"] = api_gateway
        if dynamodb is not None:
            self._values["dynamodb"] = dynamodb
        if ec2ecs is not None:
            self._values["ec2ecs"] = ec2ecs
        if fargateecs is not None:
            self._values["fargateecs"] = fargateecs
        if lambda_ is not None:
            self._values["lambda_"] = lambda_
        if rdsaurora is not None:
            self._values["rdsaurora"] = rdsaurora
        if state_machine is not None:
            self._values["state_machine"] = state_machine

    @builtins.property
    def api_gateway(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Automatically watch API Gateway APIs in the scope.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("api_gateway")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def dynamodb(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Automatically watch all Amazon DynamoDB tables in the scope.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("dynamodb")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def ec2ecs(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Automatically watch ApplicationLoadBalanced EC2 Ecs Services in the scope (using ECS Pattern).

        :default: true

        :stability: experimental
        '''
        result = self._values.get("ec2ecs")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def fargateecs(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Automatically watch ApplicationLoadBalanced Fargate Ecs Services in the scope (using ECS Pattern).

        :default: true

        :stability: experimental
        '''
        result = self._values.get("fargateecs")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def lambda_(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Automatically watch AWS Lambda functions in the scope.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("lambda_")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def rdsaurora(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Automatically watch RDS Aurora clusters in the scope.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("rdsaurora")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def state_machine(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Automatically watch AWS state machines in the scope.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("state_machine")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WatchfulAspectProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-watchful.WatchfulProps",
    jsii_struct_bases=[],
    name_mapping={
        "alarm_action_arns": "alarmActionArns",
        "alarm_actions": "alarmActions",
        "alarm_email": "alarmEmail",
        "alarm_sns": "alarmSns",
        "alarm_sqs": "alarmSqs",
        "dashboard": "dashboard",
        "dashboard_name": "dashboardName",
    },
)
class WatchfulProps:
    def __init__(
        self,
        *,
        alarm_action_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
        alarm_actions: typing.Optional[typing.Sequence[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction]] = None,
        alarm_email: typing.Optional[builtins.str] = None,
        alarm_sns: typing.Optional[_aws_cdk_aws_sns_ceddda9d.ITopic] = None,
        alarm_sqs: typing.Optional[_aws_cdk_aws_sqs_ceddda9d.IQueue] = None,
        dashboard: typing.Optional[builtins.bool] = None,
        dashboard_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param alarm_action_arns: (experimental) ARNs of actions to perform when alarms go off. These actions are in addition to email/sqs/sns. Default: [] You can use ``alarmActions`` instead as a strongly-typed alternative.
        :param alarm_actions: (experimental) CloudWatch alarm actions to perform when alarms go off. These actions are in addition to email/sqs/sns.
        :param alarm_email: (experimental) Email address to send alarms to. Default: - alarms are not sent to an email recipient.
        :param alarm_sns: (experimental) SNS topic to send alarms to. Default: - alarms are not sent to an SNS Topic.
        :param alarm_sqs: (experimental) SQS queue to send alarms to. Default: - alarms are not sent to an SQS queue.
        :param dashboard: (experimental) Whether to generate CloudWatch dashboards. Default: true
        :param dashboard_name: (experimental) The name of the CloudWatch dashboard generated by Watchful. Default: - auto-generated

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__68ab34a313d0fee3655d7baea55fd6167242c5a82652b059700a4f0247666a0b)
            check_type(argname="argument alarm_action_arns", value=alarm_action_arns, expected_type=type_hints["alarm_action_arns"])
            check_type(argname="argument alarm_actions", value=alarm_actions, expected_type=type_hints["alarm_actions"])
            check_type(argname="argument alarm_email", value=alarm_email, expected_type=type_hints["alarm_email"])
            check_type(argname="argument alarm_sns", value=alarm_sns, expected_type=type_hints["alarm_sns"])
            check_type(argname="argument alarm_sqs", value=alarm_sqs, expected_type=type_hints["alarm_sqs"])
            check_type(argname="argument dashboard", value=dashboard, expected_type=type_hints["dashboard"])
            check_type(argname="argument dashboard_name", value=dashboard_name, expected_type=type_hints["dashboard_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if alarm_action_arns is not None:
            self._values["alarm_action_arns"] = alarm_action_arns
        if alarm_actions is not None:
            self._values["alarm_actions"] = alarm_actions
        if alarm_email is not None:
            self._values["alarm_email"] = alarm_email
        if alarm_sns is not None:
            self._values["alarm_sns"] = alarm_sns
        if alarm_sqs is not None:
            self._values["alarm_sqs"] = alarm_sqs
        if dashboard is not None:
            self._values["dashboard"] = dashboard
        if dashboard_name is not None:
            self._values["dashboard_name"] = dashboard_name

    @builtins.property
    def alarm_action_arns(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) ARNs of actions to perform when alarms go off.

        These actions are in
        addition to email/sqs/sns.

        :default:

        []

        You can use ``alarmActions`` instead as a strongly-typed alternative.

        :stability: experimental
        '''
        result = self._values.get("alarm_action_arns")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def alarm_actions(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction]]:
        '''(experimental) CloudWatch alarm actions to perform when alarms go off.

        These actions are
        in addition to email/sqs/sns.

        :stability: experimental
        '''
        result = self._values.get("alarm_actions")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction]], result)

    @builtins.property
    def alarm_email(self) -> typing.Optional[builtins.str]:
        '''(experimental) Email address to send alarms to.

        :default: - alarms are not sent to an email recipient.

        :stability: experimental
        '''
        result = self._values.get("alarm_email")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def alarm_sns(self) -> typing.Optional[_aws_cdk_aws_sns_ceddda9d.ITopic]:
        '''(experimental) SNS topic to send alarms to.

        :default: - alarms are not sent to an SNS Topic.

        :stability: experimental
        '''
        result = self._values.get("alarm_sns")
        return typing.cast(typing.Optional[_aws_cdk_aws_sns_ceddda9d.ITopic], result)

    @builtins.property
    def alarm_sqs(self) -> typing.Optional[_aws_cdk_aws_sqs_ceddda9d.IQueue]:
        '''(experimental) SQS queue to send alarms to.

        :default: - alarms are not sent to an SQS queue.

        :stability: experimental
        '''
        result = self._values.get("alarm_sqs")
        return typing.cast(typing.Optional[_aws_cdk_aws_sqs_ceddda9d.IQueue], result)

    @builtins.property
    def dashboard(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether to generate CloudWatch dashboards.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("dashboard")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def dashboard_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name of the CloudWatch dashboard generated by Watchful.

        :default: - auto-generated

        :stability: experimental
        '''
        result = self._values.get("dashboard_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WatchfulProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "IWatchful",
    "QuickLink",
    "SectionOptions",
    "WatchApiGateway",
    "WatchApiGatewayOptions",
    "WatchApiGatewayProps",
    "WatchDynamoTable",
    "WatchDynamoTableOptions",
    "WatchDynamoTableProps",
    "WatchEcsService",
    "WatchEcsServiceOptions",
    "WatchEcsServiceProps",
    "WatchLambdaFunction",
    "WatchLambdaFunctionOptions",
    "WatchLambdaFunctionProps",
    "WatchRdsAurora",
    "WatchRdsAuroraOptions",
    "WatchRdsAuroraProps",
    "WatchStateMachine",
    "WatchStateMachineOptions",
    "WatchStateMachineProps",
    "WatchedOperation",
    "Watchful",
    "WatchfulAspect",
    "WatchfulAspectProps",
    "WatchfulProps",
]

publication.publish()

def _typecheckingstub__7d18083d7541e3f81cf482ce05d307f18f64607c08aab670a121bd626443015b(
    alarm: _aws_cdk_aws_cloudwatch_ceddda9d.IAlarm,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4cf210aea2d147e6b96aa16918ad9377592550fdee7809de8b94ae0337452073(
    title: builtins.str,
    *,
    links: typing.Optional[typing.Sequence[typing.Union[QuickLink, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__590f1205141b383cfe196149d2716a94cd091a40dbf666d9c07487847b6f0bbb(
    *widgets: _aws_cdk_aws_cloudwatch_ceddda9d.IWidget,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7cc0a132a71b0666adac532b07b7e9ef7ba799a6d4217acc83ec82b0ba772527(
    *,
    title: builtins.str,
    url: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7fb1a4c9454f37ad6accc1c8ddcd1626e85ed52787ae2e20667554ff2d9d0c19(
    *,
    links: typing.Optional[typing.Sequence[typing.Union[QuickLink, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4dffce348291255de623b50cc32f7b24de1702a38d6708f3d2be1b0463194bde(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    rest_api: _aws_cdk_aws_apigateway_ceddda9d.RestApi,
    title: builtins.str,
    watchful: IWatchful,
    cache_graph: typing.Optional[builtins.bool] = None,
    server_error_threshold: typing.Optional[jsii.Number] = None,
    watched_operations: typing.Optional[typing.Sequence[typing.Union[WatchedOperation, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81186eaf281e06f86d075cf2dda80d173551899867cd26312dcd571a089a558b(
    *,
    cache_graph: typing.Optional[builtins.bool] = None,
    server_error_threshold: typing.Optional[jsii.Number] = None,
    watched_operations: typing.Optional[typing.Sequence[typing.Union[WatchedOperation, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4beb71a19ca36730c44158b65cd3b514ea335d51cbdf34ccfbeb7de2c5a6cde1(
    *,
    cache_graph: typing.Optional[builtins.bool] = None,
    server_error_threshold: typing.Optional[jsii.Number] = None,
    watched_operations: typing.Optional[typing.Sequence[typing.Union[WatchedOperation, typing.Dict[builtins.str, typing.Any]]]] = None,
    rest_api: _aws_cdk_aws_apigateway_ceddda9d.RestApi,
    title: builtins.str,
    watchful: IWatchful,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93540066afa1674f8a3dae1aa92222651bf070ad92e1416a1cda5abbd383f0a9(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    table: _aws_cdk_aws_dynamodb_ceddda9d.Table,
    title: builtins.str,
    watchful: IWatchful,
    read_capacity_threshold_percent: typing.Optional[jsii.Number] = None,
    write_capacity_threshold_percent: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72119e08dbb6fe92ee77609b57f3ab38b3f314670a53c2fdf208d56b43527c2a(
    *,
    read_capacity_threshold_percent: typing.Optional[jsii.Number] = None,
    write_capacity_threshold_percent: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__692ff4756198d2d44be2a21d7e23974b81ce26953bc1861b2a517984c4b18c1e(
    *,
    read_capacity_threshold_percent: typing.Optional[jsii.Number] = None,
    write_capacity_threshold_percent: typing.Optional[jsii.Number] = None,
    table: _aws_cdk_aws_dynamodb_ceddda9d.Table,
    title: builtins.str,
    watchful: IWatchful,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66cc0b5a8c93329e091a2b01f6f3d9d11eeaf52ca9592d84cd5b6994b2a590c5(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    target_group: _aws_cdk_aws_elasticloadbalancingv2_ceddda9d.ApplicationTargetGroup,
    title: builtins.str,
    watchful: IWatchful,
    ec2_service: typing.Optional[_aws_cdk_aws_ecs_ceddda9d.Ec2Service] = None,
    fargate_service: typing.Optional[_aws_cdk_aws_ecs_ceddda9d.FargateService] = None,
    cpu_maximum_threshold_percent: typing.Optional[jsii.Number] = None,
    memory_maximum_threshold_percent: typing.Optional[jsii.Number] = None,
    requests_error_rate_threshold: typing.Optional[jsii.Number] = None,
    requests_threshold: typing.Optional[jsii.Number] = None,
    target_response_time_threshold: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50ffd7689126fc30d39d2077edb2938978e4621d3f0f80562b041af1143fe3a9(
    *,
    cpu_maximum_threshold_percent: typing.Optional[jsii.Number] = None,
    memory_maximum_threshold_percent: typing.Optional[jsii.Number] = None,
    requests_error_rate_threshold: typing.Optional[jsii.Number] = None,
    requests_threshold: typing.Optional[jsii.Number] = None,
    target_response_time_threshold: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a550a07d3f0b4b54887066fa76ac5383cb624f4233d34f4fd3583a1446342f2a(
    *,
    cpu_maximum_threshold_percent: typing.Optional[jsii.Number] = None,
    memory_maximum_threshold_percent: typing.Optional[jsii.Number] = None,
    requests_error_rate_threshold: typing.Optional[jsii.Number] = None,
    requests_threshold: typing.Optional[jsii.Number] = None,
    target_response_time_threshold: typing.Optional[jsii.Number] = None,
    target_group: _aws_cdk_aws_elasticloadbalancingv2_ceddda9d.ApplicationTargetGroup,
    title: builtins.str,
    watchful: IWatchful,
    ec2_service: typing.Optional[_aws_cdk_aws_ecs_ceddda9d.Ec2Service] = None,
    fargate_service: typing.Optional[_aws_cdk_aws_ecs_ceddda9d.FargateService] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__429a2cc615c769d2215ffe2fb7bf1476baec5e87d95b11f2f2b15a343349d97c(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    fn: _aws_cdk_aws_lambda_ceddda9d.Function,
    title: builtins.str,
    watchful: IWatchful,
    duration_threshold_percent: typing.Optional[jsii.Number] = None,
    errors_per_minute_threshold: typing.Optional[jsii.Number] = None,
    throttles_per_minute_threshold: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c8ec627af1492d940e32839754e3c7a756ecd09f39c0a072c61172f493089be(
    *,
    duration_threshold_percent: typing.Optional[jsii.Number] = None,
    errors_per_minute_threshold: typing.Optional[jsii.Number] = None,
    throttles_per_minute_threshold: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d8c569e0c54cd7730b6905d48e90b1aede79ac96817f2aa8096d98695b5780d(
    *,
    duration_threshold_percent: typing.Optional[jsii.Number] = None,
    errors_per_minute_threshold: typing.Optional[jsii.Number] = None,
    throttles_per_minute_threshold: typing.Optional[jsii.Number] = None,
    fn: _aws_cdk_aws_lambda_ceddda9d.Function,
    title: builtins.str,
    watchful: IWatchful,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76a745a0fc50edadaef32f7bff924046bb7874cfadfd2149bed0cd76a7bc0258(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    cluster: _aws_cdk_aws_rds_ceddda9d.DatabaseCluster,
    title: builtins.str,
    watchful: IWatchful,
    cpu_maximum_threshold_percent: typing.Optional[jsii.Number] = None,
    db_buffer_cache_minimum_threshold: typing.Optional[jsii.Number] = None,
    db_connections_maximum_threshold: typing.Optional[jsii.Number] = None,
    db_replica_lag_maximum_threshold: typing.Optional[jsii.Number] = None,
    db_throughput_maximum_threshold: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85f245665543cf75cc1ae7d280a4a0571dfc337140a2b43a09115250db30da45(
    *,
    cpu_maximum_threshold_percent: typing.Optional[jsii.Number] = None,
    db_buffer_cache_minimum_threshold: typing.Optional[jsii.Number] = None,
    db_connections_maximum_threshold: typing.Optional[jsii.Number] = None,
    db_replica_lag_maximum_threshold: typing.Optional[jsii.Number] = None,
    db_throughput_maximum_threshold: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__561c9c2f686b4e6d4b2e3afdf9cad715205020fa4ed4843ae6111a10d6e04253(
    *,
    cpu_maximum_threshold_percent: typing.Optional[jsii.Number] = None,
    db_buffer_cache_minimum_threshold: typing.Optional[jsii.Number] = None,
    db_connections_maximum_threshold: typing.Optional[jsii.Number] = None,
    db_replica_lag_maximum_threshold: typing.Optional[jsii.Number] = None,
    db_throughput_maximum_threshold: typing.Optional[jsii.Number] = None,
    cluster: _aws_cdk_aws_rds_ceddda9d.DatabaseCluster,
    title: builtins.str,
    watchful: IWatchful,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__125259c5c53b70d8c810c76fc4a108526d5990c627d97f0ed0cf533f56da4b77(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    state_machine: _aws_cdk_aws_stepfunctions_ceddda9d.StateMachine,
    title: builtins.str,
    watchful: IWatchful,
    metric_failed_threshold: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68e3e081e4f633ec6d9114fb3aa07047d9644a1157dbd3cb9052cc8cbff02390(
    *,
    metric_failed_threshold: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__297a4bfa8fa52e0093aab696e5addca75990afcf727bf5c7343a686845e28cc8(
    *,
    metric_failed_threshold: typing.Optional[jsii.Number] = None,
    state_machine: _aws_cdk_aws_stepfunctions_ceddda9d.StateMachine,
    title: builtins.str,
    watchful: IWatchful,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4b42e617171dedf1b6259f9dd2b52fac00e067fc7699f78fb24cc14bddf2aec(
    *,
    http_method: builtins.str,
    resource_path: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7564a98e4b044f8676d7939c4da2025d97eb0194bce396ab765f27b0f0adbe5d(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    alarm_action_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
    alarm_actions: typing.Optional[typing.Sequence[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction]] = None,
    alarm_email: typing.Optional[builtins.str] = None,
    alarm_sns: typing.Optional[_aws_cdk_aws_sns_ceddda9d.ITopic] = None,
    alarm_sqs: typing.Optional[_aws_cdk_aws_sqs_ceddda9d.IQueue] = None,
    dashboard: typing.Optional[builtins.bool] = None,
    dashboard_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2198727e4ee335e57849731e35a1f290056825dc749fac2021196c88241ed59(
    alarm: _aws_cdk_aws_cloudwatch_ceddda9d.IAlarm,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc48bd65e1cc426a4ef26a93e6ecfd4496e6b2d1e631c8e1a15f95f4cfad06d4(
    title: builtins.str,
    *,
    links: typing.Optional[typing.Sequence[typing.Union[QuickLink, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a38739559ff69bca7c8cc62caf01325d7b75ca29640d987ebd87981ab212fbc6(
    *widgets: _aws_cdk_aws_cloudwatch_ceddda9d.IWidget,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c443a383639717c77674d40d3b055a45984d6d217eb42208530310f5ebeffce(
    title: builtins.str,
    rest_api: _aws_cdk_aws_apigateway_ceddda9d.RestApi,
    *,
    cache_graph: typing.Optional[builtins.bool] = None,
    server_error_threshold: typing.Optional[jsii.Number] = None,
    watched_operations: typing.Optional[typing.Sequence[typing.Union[WatchedOperation, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2eab1523884528dc3f2b11381e7e427a70dd06bfd5de863d30d0aa033d81cc6(
    title: builtins.str,
    table: _aws_cdk_aws_dynamodb_ceddda9d.Table,
    *,
    read_capacity_threshold_percent: typing.Optional[jsii.Number] = None,
    write_capacity_threshold_percent: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a570aa382f762cfddf7b6cbde8b935d2af4087da53e13faafc0abb20eafaba65(
    title: builtins.str,
    ec2_service: _aws_cdk_aws_ecs_ceddda9d.Ec2Service,
    target_group: _aws_cdk_aws_elasticloadbalancingv2_ceddda9d.ApplicationTargetGroup,
    *,
    cpu_maximum_threshold_percent: typing.Optional[jsii.Number] = None,
    memory_maximum_threshold_percent: typing.Optional[jsii.Number] = None,
    requests_error_rate_threshold: typing.Optional[jsii.Number] = None,
    requests_threshold: typing.Optional[jsii.Number] = None,
    target_response_time_threshold: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4012b8ed38cdbc11cfd4bc404f63fb1efa3142774e054942ffe56628244f6d7f(
    title: builtins.str,
    fargate_service: _aws_cdk_aws_ecs_ceddda9d.FargateService,
    target_group: _aws_cdk_aws_elasticloadbalancingv2_ceddda9d.ApplicationTargetGroup,
    *,
    cpu_maximum_threshold_percent: typing.Optional[jsii.Number] = None,
    memory_maximum_threshold_percent: typing.Optional[jsii.Number] = None,
    requests_error_rate_threshold: typing.Optional[jsii.Number] = None,
    requests_threshold: typing.Optional[jsii.Number] = None,
    target_response_time_threshold: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a4904fba7e78fc09a6690c3cc08c6b2149ef0ad4fb8a5aa7ffd5214d78b3451(
    title: builtins.str,
    fn: _aws_cdk_aws_lambda_ceddda9d.Function,
    *,
    duration_threshold_percent: typing.Optional[jsii.Number] = None,
    errors_per_minute_threshold: typing.Optional[jsii.Number] = None,
    throttles_per_minute_threshold: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0fd82650cf8c0d95dcc6fd4b9d44c6ba7bfe500dd497b586c07d735f393540c7(
    title: builtins.str,
    cluster: _aws_cdk_aws_rds_ceddda9d.DatabaseCluster,
    *,
    cpu_maximum_threshold_percent: typing.Optional[jsii.Number] = None,
    db_buffer_cache_minimum_threshold: typing.Optional[jsii.Number] = None,
    db_connections_maximum_threshold: typing.Optional[jsii.Number] = None,
    db_replica_lag_maximum_threshold: typing.Optional[jsii.Number] = None,
    db_throughput_maximum_threshold: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a534f488fc35b6330ed8a66990a07e8dce87ba70c70083ca5ccb8bb982ef1de3(
    scope: _constructs_77d1e7e8.Construct,
    *,
    api_gateway: typing.Optional[builtins.bool] = None,
    dynamodb: typing.Optional[builtins.bool] = None,
    ec2ecs: typing.Optional[builtins.bool] = None,
    fargateecs: typing.Optional[builtins.bool] = None,
    lambda_: typing.Optional[builtins.bool] = None,
    rdsaurora: typing.Optional[builtins.bool] = None,
    state_machine: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a909168e32be61e26336586d2aa49e1379e3aeea23928e9715502a96f2c8d83(
    title: builtins.str,
    state_machine: _aws_cdk_aws_stepfunctions_ceddda9d.StateMachine,
    *,
    metric_failed_threshold: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80dfcd3cce42fa0ea903c7285a2b839e46b053ab1cd0a1f3d972fb6b6173a652(
    watchful: Watchful,
    *,
    api_gateway: typing.Optional[builtins.bool] = None,
    dynamodb: typing.Optional[builtins.bool] = None,
    ec2ecs: typing.Optional[builtins.bool] = None,
    fargateecs: typing.Optional[builtins.bool] = None,
    lambda_: typing.Optional[builtins.bool] = None,
    rdsaurora: typing.Optional[builtins.bool] = None,
    state_machine: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__076bb3367ef7233087eb63e2f3f698ea80e1862dbb6ac729a5bf4612b5486db6(
    node: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e6a9147c3f37fca972904f2ae3b116f2def8614de6af707df3d7df594ea1866(
    *,
    api_gateway: typing.Optional[builtins.bool] = None,
    dynamodb: typing.Optional[builtins.bool] = None,
    ec2ecs: typing.Optional[builtins.bool] = None,
    fargateecs: typing.Optional[builtins.bool] = None,
    lambda_: typing.Optional[builtins.bool] = None,
    rdsaurora: typing.Optional[builtins.bool] = None,
    state_machine: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68ab34a313d0fee3655d7baea55fd6167242c5a82652b059700a4f0247666a0b(
    *,
    alarm_action_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
    alarm_actions: typing.Optional[typing.Sequence[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction]] = None,
    alarm_email: typing.Optional[builtins.str] = None,
    alarm_sns: typing.Optional[_aws_cdk_aws_sns_ceddda9d.ITopic] = None,
    alarm_sqs: typing.Optional[_aws_cdk_aws_sqs_ceddda9d.IQueue] = None,
    dashboard: typing.Optional[builtins.bool] = None,
    dashboard_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
