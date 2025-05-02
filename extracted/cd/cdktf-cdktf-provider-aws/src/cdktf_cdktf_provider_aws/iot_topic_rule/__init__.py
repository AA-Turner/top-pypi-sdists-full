r'''
# `aws_iot_topic_rule`

Refer to the Terraform Registry for docs: [`aws_iot_topic_rule`](https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule).
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


class IotTopicRule(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.iotTopicRule.IotTopicRule",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule aws_iot_topic_rule}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        name: builtins.str,
        sql: builtins.str,
        sql_version: builtins.str,
        cloudwatch_alarm: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["IotTopicRuleCloudwatchAlarm", typing.Dict[builtins.str, typing.Any]]]]] = None,
        cloudwatch_logs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["IotTopicRuleCloudwatchLogs", typing.Dict[builtins.str, typing.Any]]]]] = None,
        cloudwatch_metric: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["IotTopicRuleCloudwatchMetric", typing.Dict[builtins.str, typing.Any]]]]] = None,
        description: typing.Optional[builtins.str] = None,
        dynamodb: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["IotTopicRuleDynamodb", typing.Dict[builtins.str, typing.Any]]]]] = None,
        dynamodbv2: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["IotTopicRuleDynamodbv2", typing.Dict[builtins.str, typing.Any]]]]] = None,
        elasticsearch: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["IotTopicRuleElasticsearch", typing.Dict[builtins.str, typing.Any]]]]] = None,
        error_action: typing.Optional[typing.Union["IotTopicRuleErrorAction", typing.Dict[builtins.str, typing.Any]]] = None,
        firehose: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["IotTopicRuleFirehose", typing.Dict[builtins.str, typing.Any]]]]] = None,
        http: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["IotTopicRuleHttp", typing.Dict[builtins.str, typing.Any]]]]] = None,
        id: typing.Optional[builtins.str] = None,
        iot_analytics: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["IotTopicRuleIotAnalytics", typing.Dict[builtins.str, typing.Any]]]]] = None,
        iot_events: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["IotTopicRuleIotEvents", typing.Dict[builtins.str, typing.Any]]]]] = None,
        kafka: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["IotTopicRuleKafka", typing.Dict[builtins.str, typing.Any]]]]] = None,
        kinesis: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["IotTopicRuleKinesis", typing.Dict[builtins.str, typing.Any]]]]] = None,
        lambda_: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["IotTopicRuleLambda", typing.Dict[builtins.str, typing.Any]]]]] = None,
        republish: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["IotTopicRuleRepublish", typing.Dict[builtins.str, typing.Any]]]]] = None,
        s3: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["IotTopicRuleS3", typing.Dict[builtins.str, typing.Any]]]]] = None,
        sns: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["IotTopicRuleSns", typing.Dict[builtins.str, typing.Any]]]]] = None,
        sqs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["IotTopicRuleSqs", typing.Dict[builtins.str, typing.Any]]]]] = None,
        step_functions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["IotTopicRuleStepFunctions", typing.Dict[builtins.str, typing.Any]]]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timestream: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["IotTopicRuleTimestream", typing.Dict[builtins.str, typing.Any]]]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule aws_iot_topic_rule} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#enabled IotTopicRule#enabled}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#name IotTopicRule#name}.
        :param sql: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#sql IotTopicRule#sql}.
        :param sql_version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#sql_version IotTopicRule#sql_version}.
        :param cloudwatch_alarm: cloudwatch_alarm block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#cloudwatch_alarm IotTopicRule#cloudwatch_alarm}
        :param cloudwatch_logs: cloudwatch_logs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#cloudwatch_logs IotTopicRule#cloudwatch_logs}
        :param cloudwatch_metric: cloudwatch_metric block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#cloudwatch_metric IotTopicRule#cloudwatch_metric}
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#description IotTopicRule#description}.
        :param dynamodb: dynamodb block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#dynamodb IotTopicRule#dynamodb}
        :param dynamodbv2: dynamodbv2 block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#dynamodbv2 IotTopicRule#dynamodbv2}
        :param elasticsearch: elasticsearch block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#elasticsearch IotTopicRule#elasticsearch}
        :param error_action: error_action block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#error_action IotTopicRule#error_action}
        :param firehose: firehose block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#firehose IotTopicRule#firehose}
        :param http: http block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#http IotTopicRule#http}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#id IotTopicRule#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param iot_analytics: iot_analytics block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#iot_analytics IotTopicRule#iot_analytics}
        :param iot_events: iot_events block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#iot_events IotTopicRule#iot_events}
        :param kafka: kafka block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#kafka IotTopicRule#kafka}
        :param kinesis: kinesis block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#kinesis IotTopicRule#kinesis}
        :param lambda_: lambda block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#lambda IotTopicRule#lambda}
        :param republish: republish block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#republish IotTopicRule#republish}
        :param s3: s3 block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#s3 IotTopicRule#s3}
        :param sns: sns block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#sns IotTopicRule#sns}
        :param sqs: sqs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#sqs IotTopicRule#sqs}
        :param step_functions: step_functions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#step_functions IotTopicRule#step_functions}
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#tags IotTopicRule#tags}.
        :param tags_all: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#tags_all IotTopicRule#tags_all}.
        :param timestream: timestream block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#timestream IotTopicRule#timestream}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8970063958eb0f6bf4cf03a61afc279069c72b111ef178751456f29c2dcbca01)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = IotTopicRuleConfig(
            enabled=enabled,
            name=name,
            sql=sql,
            sql_version=sql_version,
            cloudwatch_alarm=cloudwatch_alarm,
            cloudwatch_logs=cloudwatch_logs,
            cloudwatch_metric=cloudwatch_metric,
            description=description,
            dynamodb=dynamodb,
            dynamodbv2=dynamodbv2,
            elasticsearch=elasticsearch,
            error_action=error_action,
            firehose=firehose,
            http=http,
            id=id,
            iot_analytics=iot_analytics,
            iot_events=iot_events,
            kafka=kafka,
            kinesis=kinesis,
            lambda_=lambda_,
            republish=republish,
            s3=s3,
            sns=sns,
            sqs=sqs,
            step_functions=step_functions,
            tags=tags,
            tags_all=tags_all,
            timestream=timestream,
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
        '''Generates CDKTF code for importing a IotTopicRule resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the IotTopicRule to import.
        :param import_from_id: The id of the existing IotTopicRule that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the IotTopicRule to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__07891052e4dfd16458e3c2bbe8879734446fe703cb2bc96cac6baa460888f937)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putCloudwatchAlarm")
    def put_cloudwatch_alarm(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["IotTopicRuleCloudwatchAlarm", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4d75910e333fba2f691b0d5bc6cf9417cc31457e92251ec4adf31a2114af3a4c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putCloudwatchAlarm", [value]))

    @jsii.member(jsii_name="putCloudwatchLogs")
    def put_cloudwatch_logs(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["IotTopicRuleCloudwatchLogs", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__05f1825846214f9237779f4359ba81f64f7b8ed228fbff5f56deb6bce0a7ec9d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putCloudwatchLogs", [value]))

    @jsii.member(jsii_name="putCloudwatchMetric")
    def put_cloudwatch_metric(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["IotTopicRuleCloudwatchMetric", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__41ceb9d80125030fc606b37a1ab39c7ec55a0911080608c6479b167276aff770)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putCloudwatchMetric", [value]))

    @jsii.member(jsii_name="putDynamodb")
    def put_dynamodb(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["IotTopicRuleDynamodb", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f1619bd2b8e6aa2fc94f8fd9f73a3a6b2dff272f0d48c254285ca12c8f3f655d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putDynamodb", [value]))

    @jsii.member(jsii_name="putDynamodbv2")
    def put_dynamodbv2(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["IotTopicRuleDynamodbv2", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cda972003f852e1e047e690ee3cd27d0d7142ecefc9a72ecc95befa85e2a4f4c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putDynamodbv2", [value]))

    @jsii.member(jsii_name="putElasticsearch")
    def put_elasticsearch(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["IotTopicRuleElasticsearch", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fb385d0e37e2208fb99f375d6b15502ed154fe5a9319755b784a4a212b02a339)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putElasticsearch", [value]))

    @jsii.member(jsii_name="putErrorAction")
    def put_error_action(
        self,
        *,
        cloudwatch_alarm: typing.Optional[typing.Union["IotTopicRuleErrorActionCloudwatchAlarm", typing.Dict[builtins.str, typing.Any]]] = None,
        cloudwatch_logs: typing.Optional[typing.Union["IotTopicRuleErrorActionCloudwatchLogs", typing.Dict[builtins.str, typing.Any]]] = None,
        cloudwatch_metric: typing.Optional[typing.Union["IotTopicRuleErrorActionCloudwatchMetric", typing.Dict[builtins.str, typing.Any]]] = None,
        dynamodb: typing.Optional[typing.Union["IotTopicRuleErrorActionDynamodb", typing.Dict[builtins.str, typing.Any]]] = None,
        dynamodbv2: typing.Optional[typing.Union["IotTopicRuleErrorActionDynamodbv2", typing.Dict[builtins.str, typing.Any]]] = None,
        elasticsearch: typing.Optional[typing.Union["IotTopicRuleErrorActionElasticsearch", typing.Dict[builtins.str, typing.Any]]] = None,
        firehose: typing.Optional[typing.Union["IotTopicRuleErrorActionFirehose", typing.Dict[builtins.str, typing.Any]]] = None,
        http: typing.Optional[typing.Union["IotTopicRuleErrorActionHttp", typing.Dict[builtins.str, typing.Any]]] = None,
        iot_analytics: typing.Optional[typing.Union["IotTopicRuleErrorActionIotAnalytics", typing.Dict[builtins.str, typing.Any]]] = None,
        iot_events: typing.Optional[typing.Union["IotTopicRuleErrorActionIotEvents", typing.Dict[builtins.str, typing.Any]]] = None,
        kafka: typing.Optional[typing.Union["IotTopicRuleErrorActionKafka", typing.Dict[builtins.str, typing.Any]]] = None,
        kinesis: typing.Optional[typing.Union["IotTopicRuleErrorActionKinesis", typing.Dict[builtins.str, typing.Any]]] = None,
        lambda_: typing.Optional[typing.Union["IotTopicRuleErrorActionLambda", typing.Dict[builtins.str, typing.Any]]] = None,
        republish: typing.Optional[typing.Union["IotTopicRuleErrorActionRepublish", typing.Dict[builtins.str, typing.Any]]] = None,
        s3: typing.Optional[typing.Union["IotTopicRuleErrorActionS3", typing.Dict[builtins.str, typing.Any]]] = None,
        sns: typing.Optional[typing.Union["IotTopicRuleErrorActionSns", typing.Dict[builtins.str, typing.Any]]] = None,
        sqs: typing.Optional[typing.Union["IotTopicRuleErrorActionSqs", typing.Dict[builtins.str, typing.Any]]] = None,
        step_functions: typing.Optional[typing.Union["IotTopicRuleErrorActionStepFunctions", typing.Dict[builtins.str, typing.Any]]] = None,
        timestream: typing.Optional[typing.Union["IotTopicRuleErrorActionTimestream", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param cloudwatch_alarm: cloudwatch_alarm block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#cloudwatch_alarm IotTopicRule#cloudwatch_alarm}
        :param cloudwatch_logs: cloudwatch_logs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#cloudwatch_logs IotTopicRule#cloudwatch_logs}
        :param cloudwatch_metric: cloudwatch_metric block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#cloudwatch_metric IotTopicRule#cloudwatch_metric}
        :param dynamodb: dynamodb block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#dynamodb IotTopicRule#dynamodb}
        :param dynamodbv2: dynamodbv2 block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#dynamodbv2 IotTopicRule#dynamodbv2}
        :param elasticsearch: elasticsearch block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#elasticsearch IotTopicRule#elasticsearch}
        :param firehose: firehose block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#firehose IotTopicRule#firehose}
        :param http: http block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#http IotTopicRule#http}
        :param iot_analytics: iot_analytics block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#iot_analytics IotTopicRule#iot_analytics}
        :param iot_events: iot_events block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#iot_events IotTopicRule#iot_events}
        :param kafka: kafka block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#kafka IotTopicRule#kafka}
        :param kinesis: kinesis block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#kinesis IotTopicRule#kinesis}
        :param lambda_: lambda block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#lambda IotTopicRule#lambda}
        :param republish: republish block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#republish IotTopicRule#republish}
        :param s3: s3 block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#s3 IotTopicRule#s3}
        :param sns: sns block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#sns IotTopicRule#sns}
        :param sqs: sqs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#sqs IotTopicRule#sqs}
        :param step_functions: step_functions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#step_functions IotTopicRule#step_functions}
        :param timestream: timestream block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#timestream IotTopicRule#timestream}
        '''
        value = IotTopicRuleErrorAction(
            cloudwatch_alarm=cloudwatch_alarm,
            cloudwatch_logs=cloudwatch_logs,
            cloudwatch_metric=cloudwatch_metric,
            dynamodb=dynamodb,
            dynamodbv2=dynamodbv2,
            elasticsearch=elasticsearch,
            firehose=firehose,
            http=http,
            iot_analytics=iot_analytics,
            iot_events=iot_events,
            kafka=kafka,
            kinesis=kinesis,
            lambda_=lambda_,
            republish=republish,
            s3=s3,
            sns=sns,
            sqs=sqs,
            step_functions=step_functions,
            timestream=timestream,
        )

        return typing.cast(None, jsii.invoke(self, "putErrorAction", [value]))

    @jsii.member(jsii_name="putFirehose")
    def put_firehose(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["IotTopicRuleFirehose", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__21ebcc20b66a6b75a0524ea4b00eddc076f8a461dac0117bcd04653008004bb6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putFirehose", [value]))

    @jsii.member(jsii_name="putHttp")
    def put_http(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["IotTopicRuleHttp", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c0c5cbad31d09269d73168d071a6dc644a6fc7a8bb3045fe9eee180ebc6d5e36)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putHttp", [value]))

    @jsii.member(jsii_name="putIotAnalytics")
    def put_iot_analytics(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["IotTopicRuleIotAnalytics", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d5ab200fea93b95224a14b18b7aade3c9b67a039d980889cc30eef099f403cca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putIotAnalytics", [value]))

    @jsii.member(jsii_name="putIotEvents")
    def put_iot_events(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["IotTopicRuleIotEvents", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__802a2bdc13bd2639969df7482fa282b0788236b72443e995f033984665e67149)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putIotEvents", [value]))

    @jsii.member(jsii_name="putKafka")
    def put_kafka(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["IotTopicRuleKafka", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ae5c1dae3e98ee0bdd4b00a645c87e2d2af52cbee0518bae11357fb91d7fa3d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putKafka", [value]))

    @jsii.member(jsii_name="putKinesis")
    def put_kinesis(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["IotTopicRuleKinesis", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bc79a9ff29a7453aa9907c08bc239c9da0ca92cedaed3e394762cf3c6b4c34f3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putKinesis", [value]))

    @jsii.member(jsii_name="putLambda")
    def put_lambda(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["IotTopicRuleLambda", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__18c043324e82d256c60ac5dadb1158b5f682abb78d6cb8025d199c9c5f892f80)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putLambda", [value]))

    @jsii.member(jsii_name="putRepublish")
    def put_republish(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["IotTopicRuleRepublish", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__602282092e12dd922f44f1910eec1d7933c18d3224bb66c9cb86bb2a33e97e3d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putRepublish", [value]))

    @jsii.member(jsii_name="putS3")
    def put_s3(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["IotTopicRuleS3", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9cb6984e2e0244d3c7471b869bbfc610bc1820cb81f98f461a816e7db30ecfa3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putS3", [value]))

    @jsii.member(jsii_name="putSns")
    def put_sns(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["IotTopicRuleSns", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7ceb0b7dca719b71ef483c079f2655b5915ec1ec3fc11d5a9f0a84bd97fc0374)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putSns", [value]))

    @jsii.member(jsii_name="putSqs")
    def put_sqs(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["IotTopicRuleSqs", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__60650706897f0e42d1bc3a8ffb5f3b3cd971eab113a568df57b48b75270d0cf8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putSqs", [value]))

    @jsii.member(jsii_name="putStepFunctions")
    def put_step_functions(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["IotTopicRuleStepFunctions", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1dabb8f6030e62a76e328b9954a76b87aa3814daae40bd17b2357afc90936d6f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putStepFunctions", [value]))

    @jsii.member(jsii_name="putTimestream")
    def put_timestream(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["IotTopicRuleTimestream", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__901369fb361cdf03e678310b7948457aee14d381ad5d21445821496b99d95550)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putTimestream", [value]))

    @jsii.member(jsii_name="resetCloudwatchAlarm")
    def reset_cloudwatch_alarm(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCloudwatchAlarm", []))

    @jsii.member(jsii_name="resetCloudwatchLogs")
    def reset_cloudwatch_logs(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCloudwatchLogs", []))

    @jsii.member(jsii_name="resetCloudwatchMetric")
    def reset_cloudwatch_metric(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCloudwatchMetric", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetDynamodb")
    def reset_dynamodb(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDynamodb", []))

    @jsii.member(jsii_name="resetDynamodbv2")
    def reset_dynamodbv2(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDynamodbv2", []))

    @jsii.member(jsii_name="resetElasticsearch")
    def reset_elasticsearch(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetElasticsearch", []))

    @jsii.member(jsii_name="resetErrorAction")
    def reset_error_action(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetErrorAction", []))

    @jsii.member(jsii_name="resetFirehose")
    def reset_firehose(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFirehose", []))

    @jsii.member(jsii_name="resetHttp")
    def reset_http(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHttp", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetIotAnalytics")
    def reset_iot_analytics(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIotAnalytics", []))

    @jsii.member(jsii_name="resetIotEvents")
    def reset_iot_events(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIotEvents", []))

    @jsii.member(jsii_name="resetKafka")
    def reset_kafka(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKafka", []))

    @jsii.member(jsii_name="resetKinesis")
    def reset_kinesis(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKinesis", []))

    @jsii.member(jsii_name="resetLambda")
    def reset_lambda(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLambda", []))

    @jsii.member(jsii_name="resetRepublish")
    def reset_republish(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRepublish", []))

    @jsii.member(jsii_name="resetS3")
    def reset_s3(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetS3", []))

    @jsii.member(jsii_name="resetSns")
    def reset_sns(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSns", []))

    @jsii.member(jsii_name="resetSqs")
    def reset_sqs(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSqs", []))

    @jsii.member(jsii_name="resetStepFunctions")
    def reset_step_functions(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStepFunctions", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

    @jsii.member(jsii_name="resetTagsAll")
    def reset_tags_all(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTagsAll", []))

    @jsii.member(jsii_name="resetTimestream")
    def reset_timestream(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimestream", []))

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
    @jsii.member(jsii_name="arn")
    def arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "arn"))

    @builtins.property
    @jsii.member(jsii_name="cloudwatchAlarm")
    def cloudwatch_alarm(self) -> "IotTopicRuleCloudwatchAlarmList":
        return typing.cast("IotTopicRuleCloudwatchAlarmList", jsii.get(self, "cloudwatchAlarm"))

    @builtins.property
    @jsii.member(jsii_name="cloudwatchLogs")
    def cloudwatch_logs(self) -> "IotTopicRuleCloudwatchLogsList":
        return typing.cast("IotTopicRuleCloudwatchLogsList", jsii.get(self, "cloudwatchLogs"))

    @builtins.property
    @jsii.member(jsii_name="cloudwatchMetric")
    def cloudwatch_metric(self) -> "IotTopicRuleCloudwatchMetricList":
        return typing.cast("IotTopicRuleCloudwatchMetricList", jsii.get(self, "cloudwatchMetric"))

    @builtins.property
    @jsii.member(jsii_name="dynamodb")
    def dynamodb(self) -> "IotTopicRuleDynamodbList":
        return typing.cast("IotTopicRuleDynamodbList", jsii.get(self, "dynamodb"))

    @builtins.property
    @jsii.member(jsii_name="dynamodbv2")
    def dynamodbv2(self) -> "IotTopicRuleDynamodbv2List":
        return typing.cast("IotTopicRuleDynamodbv2List", jsii.get(self, "dynamodbv2"))

    @builtins.property
    @jsii.member(jsii_name="elasticsearch")
    def elasticsearch(self) -> "IotTopicRuleElasticsearchList":
        return typing.cast("IotTopicRuleElasticsearchList", jsii.get(self, "elasticsearch"))

    @builtins.property
    @jsii.member(jsii_name="errorAction")
    def error_action(self) -> "IotTopicRuleErrorActionOutputReference":
        return typing.cast("IotTopicRuleErrorActionOutputReference", jsii.get(self, "errorAction"))

    @builtins.property
    @jsii.member(jsii_name="firehose")
    def firehose(self) -> "IotTopicRuleFirehoseList":
        return typing.cast("IotTopicRuleFirehoseList", jsii.get(self, "firehose"))

    @builtins.property
    @jsii.member(jsii_name="http")
    def http(self) -> "IotTopicRuleHttpList":
        return typing.cast("IotTopicRuleHttpList", jsii.get(self, "http"))

    @builtins.property
    @jsii.member(jsii_name="iotAnalytics")
    def iot_analytics(self) -> "IotTopicRuleIotAnalyticsList":
        return typing.cast("IotTopicRuleIotAnalyticsList", jsii.get(self, "iotAnalytics"))

    @builtins.property
    @jsii.member(jsii_name="iotEvents")
    def iot_events(self) -> "IotTopicRuleIotEventsList":
        return typing.cast("IotTopicRuleIotEventsList", jsii.get(self, "iotEvents"))

    @builtins.property
    @jsii.member(jsii_name="kafka")
    def kafka(self) -> "IotTopicRuleKafkaList":
        return typing.cast("IotTopicRuleKafkaList", jsii.get(self, "kafka"))

    @builtins.property
    @jsii.member(jsii_name="kinesis")
    def kinesis(self) -> "IotTopicRuleKinesisList":
        return typing.cast("IotTopicRuleKinesisList", jsii.get(self, "kinesis"))

    @builtins.property
    @jsii.member(jsii_name="lambda")
    def lambda_(self) -> "IotTopicRuleLambdaList":
        return typing.cast("IotTopicRuleLambdaList", jsii.get(self, "lambda"))

    @builtins.property
    @jsii.member(jsii_name="republish")
    def republish(self) -> "IotTopicRuleRepublishList":
        return typing.cast("IotTopicRuleRepublishList", jsii.get(self, "republish"))

    @builtins.property
    @jsii.member(jsii_name="s3")
    def s3(self) -> "IotTopicRuleS3List":
        return typing.cast("IotTopicRuleS3List", jsii.get(self, "s3"))

    @builtins.property
    @jsii.member(jsii_name="sns")
    def sns(self) -> "IotTopicRuleSnsList":
        return typing.cast("IotTopicRuleSnsList", jsii.get(self, "sns"))

    @builtins.property
    @jsii.member(jsii_name="sqs")
    def sqs(self) -> "IotTopicRuleSqsList":
        return typing.cast("IotTopicRuleSqsList", jsii.get(self, "sqs"))

    @builtins.property
    @jsii.member(jsii_name="stepFunctions")
    def step_functions(self) -> "IotTopicRuleStepFunctionsList":
        return typing.cast("IotTopicRuleStepFunctionsList", jsii.get(self, "stepFunctions"))

    @builtins.property
    @jsii.member(jsii_name="timestream")
    def timestream(self) -> "IotTopicRuleTimestreamList":
        return typing.cast("IotTopicRuleTimestreamList", jsii.get(self, "timestream"))

    @builtins.property
    @jsii.member(jsii_name="cloudwatchAlarmInput")
    def cloudwatch_alarm_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["IotTopicRuleCloudwatchAlarm"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["IotTopicRuleCloudwatchAlarm"]]], jsii.get(self, "cloudwatchAlarmInput"))

    @builtins.property
    @jsii.member(jsii_name="cloudwatchLogsInput")
    def cloudwatch_logs_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["IotTopicRuleCloudwatchLogs"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["IotTopicRuleCloudwatchLogs"]]], jsii.get(self, "cloudwatchLogsInput"))

    @builtins.property
    @jsii.member(jsii_name="cloudwatchMetricInput")
    def cloudwatch_metric_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["IotTopicRuleCloudwatchMetric"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["IotTopicRuleCloudwatchMetric"]]], jsii.get(self, "cloudwatchMetricInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="dynamodbInput")
    def dynamodb_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["IotTopicRuleDynamodb"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["IotTopicRuleDynamodb"]]], jsii.get(self, "dynamodbInput"))

    @builtins.property
    @jsii.member(jsii_name="dynamodbv2Input")
    def dynamodbv2_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["IotTopicRuleDynamodbv2"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["IotTopicRuleDynamodbv2"]]], jsii.get(self, "dynamodbv2Input"))

    @builtins.property
    @jsii.member(jsii_name="elasticsearchInput")
    def elasticsearch_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["IotTopicRuleElasticsearch"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["IotTopicRuleElasticsearch"]]], jsii.get(self, "elasticsearchInput"))

    @builtins.property
    @jsii.member(jsii_name="enabledInput")
    def enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enabledInput"))

    @builtins.property
    @jsii.member(jsii_name="errorActionInput")
    def error_action_input(self) -> typing.Optional["IotTopicRuleErrorAction"]:
        return typing.cast(typing.Optional["IotTopicRuleErrorAction"], jsii.get(self, "errorActionInput"))

    @builtins.property
    @jsii.member(jsii_name="firehoseInput")
    def firehose_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["IotTopicRuleFirehose"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["IotTopicRuleFirehose"]]], jsii.get(self, "firehoseInput"))

    @builtins.property
    @jsii.member(jsii_name="httpInput")
    def http_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["IotTopicRuleHttp"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["IotTopicRuleHttp"]]], jsii.get(self, "httpInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="iotAnalyticsInput")
    def iot_analytics_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["IotTopicRuleIotAnalytics"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["IotTopicRuleIotAnalytics"]]], jsii.get(self, "iotAnalyticsInput"))

    @builtins.property
    @jsii.member(jsii_name="iotEventsInput")
    def iot_events_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["IotTopicRuleIotEvents"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["IotTopicRuleIotEvents"]]], jsii.get(self, "iotEventsInput"))

    @builtins.property
    @jsii.member(jsii_name="kafkaInput")
    def kafka_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["IotTopicRuleKafka"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["IotTopicRuleKafka"]]], jsii.get(self, "kafkaInput"))

    @builtins.property
    @jsii.member(jsii_name="kinesisInput")
    def kinesis_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["IotTopicRuleKinesis"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["IotTopicRuleKinesis"]]], jsii.get(self, "kinesisInput"))

    @builtins.property
    @jsii.member(jsii_name="lambdaInput")
    def lambda_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["IotTopicRuleLambda"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["IotTopicRuleLambda"]]], jsii.get(self, "lambdaInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="republishInput")
    def republish_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["IotTopicRuleRepublish"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["IotTopicRuleRepublish"]]], jsii.get(self, "republishInput"))

    @builtins.property
    @jsii.member(jsii_name="s3Input")
    def s3_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["IotTopicRuleS3"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["IotTopicRuleS3"]]], jsii.get(self, "s3Input"))

    @builtins.property
    @jsii.member(jsii_name="snsInput")
    def sns_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["IotTopicRuleSns"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["IotTopicRuleSns"]]], jsii.get(self, "snsInput"))

    @builtins.property
    @jsii.member(jsii_name="sqlInput")
    def sql_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sqlInput"))

    @builtins.property
    @jsii.member(jsii_name="sqlVersionInput")
    def sql_version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sqlVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="sqsInput")
    def sqs_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["IotTopicRuleSqs"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["IotTopicRuleSqs"]]], jsii.get(self, "sqsInput"))

    @builtins.property
    @jsii.member(jsii_name="stepFunctionsInput")
    def step_functions_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["IotTopicRuleStepFunctions"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["IotTopicRuleStepFunctions"]]], jsii.get(self, "stepFunctionsInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsAllInput")
    def tags_all_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "tagsAllInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsInput")
    def tags_input(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "tagsInput"))

    @builtins.property
    @jsii.member(jsii_name="timestreamInput")
    def timestream_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["IotTopicRuleTimestream"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["IotTopicRuleTimestream"]]], jsii.get(self, "timestreamInput"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f4c2b2d28d848243c51f5ccc1c643d9264e8555ea818f9c0e6b258c838f850f6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1af983abaf0cf236dffe6f5ce3dcedb7b6ccc1f59206fdb0a8728b68c41b3d51)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce035f1a4fa8e41e5f0de5c1395e0796644486722f57bb7893d42ec178aad327)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__621198ba6abc0a0777236fd9236e11a4518f06fb7141c4be80ac0edbac431f36)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sql")
    def sql(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sql"))

    @sql.setter
    def sql(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5d57d46a8702002be22c00306e0f6fd2b87021c590a33c67c78885abe2019d9d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sql", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sqlVersion")
    def sql_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sqlVersion"))

    @sql_version.setter
    def sql_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f08852130141c9567a2645badc54d1d623961edbc64709a94a3dca54602b835)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sqlVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cb26afdebd349df458a87eb44916b354298defb605cc1921dda0e8677c440cfd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tagsAll")
    def tags_all(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tagsAll"))

    @tags_all.setter
    def tags_all(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__be5f7a57aea09f44be296f94c688533482dc3d5fa12d1a54078744d9b8a36667)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tagsAll", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.iotTopicRule.IotTopicRuleCloudwatchAlarm",
    jsii_struct_bases=[],
    name_mapping={
        "alarm_name": "alarmName",
        "role_arn": "roleArn",
        "state_reason": "stateReason",
        "state_value": "stateValue",
    },
)
class IotTopicRuleCloudwatchAlarm:
    def __init__(
        self,
        *,
        alarm_name: builtins.str,
        role_arn: builtins.str,
        state_reason: builtins.str,
        state_value: builtins.str,
    ) -> None:
        '''
        :param alarm_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#alarm_name IotTopicRule#alarm_name}.
        :param role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#role_arn IotTopicRule#role_arn}.
        :param state_reason: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#state_reason IotTopicRule#state_reason}.
        :param state_value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#state_value IotTopicRule#state_value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f80cad964ea1794363a30c075aa9b7d54844d7e9b326843217e380085924d3ab)
            check_type(argname="argument alarm_name", value=alarm_name, expected_type=type_hints["alarm_name"])
            check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
            check_type(argname="argument state_reason", value=state_reason, expected_type=type_hints["state_reason"])
            check_type(argname="argument state_value", value=state_value, expected_type=type_hints["state_value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "alarm_name": alarm_name,
            "role_arn": role_arn,
            "state_reason": state_reason,
            "state_value": state_value,
        }

    @builtins.property
    def alarm_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#alarm_name IotTopicRule#alarm_name}.'''
        result = self._values.get("alarm_name")
        assert result is not None, "Required property 'alarm_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def role_arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#role_arn IotTopicRule#role_arn}.'''
        result = self._values.get("role_arn")
        assert result is not None, "Required property 'role_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def state_reason(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#state_reason IotTopicRule#state_reason}.'''
        result = self._values.get("state_reason")
        assert result is not None, "Required property 'state_reason' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def state_value(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#state_value IotTopicRule#state_value}.'''
        result = self._values.get("state_value")
        assert result is not None, "Required property 'state_value' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IotTopicRuleCloudwatchAlarm(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class IotTopicRuleCloudwatchAlarmList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.iotTopicRule.IotTopicRuleCloudwatchAlarmList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7fc0b2ce2a1c9de004494f114cd23a4e6fed37728e1c88d81ea4f1303289a366)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "IotTopicRuleCloudwatchAlarmOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ad54e6bc07b5701524af251abf9644fcdcae1f94a7315ccbcef771d22e27ee7)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("IotTopicRuleCloudwatchAlarmOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__11566d6d82d209c437913bdcb0dba0cea2eb82eb48f741d10fa6473d8161653c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9f25a4fab2c8cf8a5ddf3140a4065c020c4552ed0214d0315af143c39b8437d9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f2f308506a63554ce60a213a199783f01fb096e912cc4c26f0ecae3f3fedfbd7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotTopicRuleCloudwatchAlarm]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotTopicRuleCloudwatchAlarm]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotTopicRuleCloudwatchAlarm]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7fb4bca6948a655376b0801c2337b00bae8b671032ba735aeb64f8da25c742a0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class IotTopicRuleCloudwatchAlarmOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.iotTopicRule.IotTopicRuleCloudwatchAlarmOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__423b0f50d67b29f01eead7c923329fb54febdf08904be3a64ca3bce7f7416234)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="alarmNameInput")
    def alarm_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "alarmNameInput"))

    @builtins.property
    @jsii.member(jsii_name="roleArnInput")
    def role_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "roleArnInput"))

    @builtins.property
    @jsii.member(jsii_name="stateReasonInput")
    def state_reason_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "stateReasonInput"))

    @builtins.property
    @jsii.member(jsii_name="stateValueInput")
    def state_value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "stateValueInput"))

    @builtins.property
    @jsii.member(jsii_name="alarmName")
    def alarm_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "alarmName"))

    @alarm_name.setter
    def alarm_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__56729d3ba5fc93d5c15e682c45a2342f9db9c157f30e1505d20784d0a341bd77)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "alarmName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="roleArn")
    def role_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "roleArn"))

    @role_arn.setter
    def role_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__145480f6801807cbf3fa91c58f223ec5390e29d4033a9c3f03790102039e0d9c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "roleArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="stateReason")
    def state_reason(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "stateReason"))

    @state_reason.setter
    def state_reason(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c30757486b76f645ed9379118153f25c2474cbcde9f8a53986f9447143b071db)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "stateReason", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="stateValue")
    def state_value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "stateValue"))

    @state_value.setter
    def state_value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9fed69a99387675f3a659329b8ace0ccc6c96240bee350be1c9a7b07ba5ea2e1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "stateValue", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IotTopicRuleCloudwatchAlarm]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IotTopicRuleCloudwatchAlarm]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IotTopicRuleCloudwatchAlarm]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9eb064f57b6319cdaa1ac8ce19265ae196aad42a1a3542ba35c3695df81051e0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.iotTopicRule.IotTopicRuleCloudwatchLogs",
    jsii_struct_bases=[],
    name_mapping={
        "log_group_name": "logGroupName",
        "role_arn": "roleArn",
        "batch_mode": "batchMode",
    },
)
class IotTopicRuleCloudwatchLogs:
    def __init__(
        self,
        *,
        log_group_name: builtins.str,
        role_arn: builtins.str,
        batch_mode: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param log_group_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#log_group_name IotTopicRule#log_group_name}.
        :param role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#role_arn IotTopicRule#role_arn}.
        :param batch_mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#batch_mode IotTopicRule#batch_mode}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__76561102d918397c1716ad8540000c6bf0c0165120ead2b5716d0c53bbfe9070)
            check_type(argname="argument log_group_name", value=log_group_name, expected_type=type_hints["log_group_name"])
            check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
            check_type(argname="argument batch_mode", value=batch_mode, expected_type=type_hints["batch_mode"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "log_group_name": log_group_name,
            "role_arn": role_arn,
        }
        if batch_mode is not None:
            self._values["batch_mode"] = batch_mode

    @builtins.property
    def log_group_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#log_group_name IotTopicRule#log_group_name}.'''
        result = self._values.get("log_group_name")
        assert result is not None, "Required property 'log_group_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def role_arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#role_arn IotTopicRule#role_arn}.'''
        result = self._values.get("role_arn")
        assert result is not None, "Required property 'role_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def batch_mode(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#batch_mode IotTopicRule#batch_mode}.'''
        result = self._values.get("batch_mode")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IotTopicRuleCloudwatchLogs(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class IotTopicRuleCloudwatchLogsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.iotTopicRule.IotTopicRuleCloudwatchLogsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9aeaab1f8f8ebfb12b89985d842d0c98c9cca16ee008e22ba22e74176ed4c971)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "IotTopicRuleCloudwatchLogsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e929628524e8b7bcd89e3405dfb515d06a2380f0f93356de0334f613daa79a6)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("IotTopicRuleCloudwatchLogsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ff0c0b1d021904b3c62abf26a3bb0d499d4c3412f43e517730af804358ff46f7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__cedb774b04fa1b2407786949d7fa39416b7e1ca17a3e314ee363e3b71984ad4c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__50bcaae84ba976947676dd6bfbd00a9490354e1cb0ca6d3804abd4e5b5e82c23)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotTopicRuleCloudwatchLogs]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotTopicRuleCloudwatchLogs]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotTopicRuleCloudwatchLogs]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__49eb653b4486e056b9652f792792b5ea1e69e2b44507c986820ed000fd53964c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class IotTopicRuleCloudwatchLogsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.iotTopicRule.IotTopicRuleCloudwatchLogsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__cf51dccee4aaaf55b0e8a8ed059bf8c7b56a82514e63060944c7cde8fd6cdbc0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetBatchMode")
    def reset_batch_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBatchMode", []))

    @builtins.property
    @jsii.member(jsii_name="batchModeInput")
    def batch_mode_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "batchModeInput"))

    @builtins.property
    @jsii.member(jsii_name="logGroupNameInput")
    def log_group_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "logGroupNameInput"))

    @builtins.property
    @jsii.member(jsii_name="roleArnInput")
    def role_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "roleArnInput"))

    @builtins.property
    @jsii.member(jsii_name="batchMode")
    def batch_mode(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "batchMode"))

    @batch_mode.setter
    def batch_mode(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1594a04b1eb992ae3817c5a797e56e91e258ac5d276e93d3229dcb01219c84d1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "batchMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="logGroupName")
    def log_group_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "logGroupName"))

    @log_group_name.setter
    def log_group_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d4f00a3274e84ec178dbd93b918cb55b63ccfafc46ce3ea12839f7b2d499e38)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "logGroupName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="roleArn")
    def role_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "roleArn"))

    @role_arn.setter
    def role_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ad113744adcaa349f77d4bf09c7a33250271cd40e102299b0da24801780b3b0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "roleArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IotTopicRuleCloudwatchLogs]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IotTopicRuleCloudwatchLogs]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IotTopicRuleCloudwatchLogs]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b572b3d2d07b874c7868e7d573aa703086c5878485659875c2ffa059197b0bfd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.iotTopicRule.IotTopicRuleCloudwatchMetric",
    jsii_struct_bases=[],
    name_mapping={
        "metric_name": "metricName",
        "metric_namespace": "metricNamespace",
        "metric_unit": "metricUnit",
        "metric_value": "metricValue",
        "role_arn": "roleArn",
        "metric_timestamp": "metricTimestamp",
    },
)
class IotTopicRuleCloudwatchMetric:
    def __init__(
        self,
        *,
        metric_name: builtins.str,
        metric_namespace: builtins.str,
        metric_unit: builtins.str,
        metric_value: builtins.str,
        role_arn: builtins.str,
        metric_timestamp: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param metric_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#metric_name IotTopicRule#metric_name}.
        :param metric_namespace: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#metric_namespace IotTopicRule#metric_namespace}.
        :param metric_unit: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#metric_unit IotTopicRule#metric_unit}.
        :param metric_value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#metric_value IotTopicRule#metric_value}.
        :param role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#role_arn IotTopicRule#role_arn}.
        :param metric_timestamp: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#metric_timestamp IotTopicRule#metric_timestamp}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__19931c16274872697d258287b0c631350ebe4a7b1c054f46b62c5c43a6ba0fab)
            check_type(argname="argument metric_name", value=metric_name, expected_type=type_hints["metric_name"])
            check_type(argname="argument metric_namespace", value=metric_namespace, expected_type=type_hints["metric_namespace"])
            check_type(argname="argument metric_unit", value=metric_unit, expected_type=type_hints["metric_unit"])
            check_type(argname="argument metric_value", value=metric_value, expected_type=type_hints["metric_value"])
            check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
            check_type(argname="argument metric_timestamp", value=metric_timestamp, expected_type=type_hints["metric_timestamp"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "metric_name": metric_name,
            "metric_namespace": metric_namespace,
            "metric_unit": metric_unit,
            "metric_value": metric_value,
            "role_arn": role_arn,
        }
        if metric_timestamp is not None:
            self._values["metric_timestamp"] = metric_timestamp

    @builtins.property
    def metric_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#metric_name IotTopicRule#metric_name}.'''
        result = self._values.get("metric_name")
        assert result is not None, "Required property 'metric_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def metric_namespace(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#metric_namespace IotTopicRule#metric_namespace}.'''
        result = self._values.get("metric_namespace")
        assert result is not None, "Required property 'metric_namespace' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def metric_unit(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#metric_unit IotTopicRule#metric_unit}.'''
        result = self._values.get("metric_unit")
        assert result is not None, "Required property 'metric_unit' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def metric_value(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#metric_value IotTopicRule#metric_value}.'''
        result = self._values.get("metric_value")
        assert result is not None, "Required property 'metric_value' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def role_arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#role_arn IotTopicRule#role_arn}.'''
        result = self._values.get("role_arn")
        assert result is not None, "Required property 'role_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def metric_timestamp(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#metric_timestamp IotTopicRule#metric_timestamp}.'''
        result = self._values.get("metric_timestamp")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IotTopicRuleCloudwatchMetric(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class IotTopicRuleCloudwatchMetricList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.iotTopicRule.IotTopicRuleCloudwatchMetricList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__19d1e6d48c6fdf3aa8e07765ca542041083c7bc308770de2348f2e006585f474)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "IotTopicRuleCloudwatchMetricOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee135e846f6a9548522b4d8628d62298272d06ab28a041e044e5933a694a8bb7)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("IotTopicRuleCloudwatchMetricOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6447120f3379ce076a80a25250153fc8028ffe3c9a94bce451d72b83b6dc142b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__cf6da84f71c96551736eb3a08880cc2bfa5a92941f77336bbaeb9a6062d348d0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4aacd560e0a606c52e882f73969845b3c69d5baf674ecac4532e36342ecdb0ad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotTopicRuleCloudwatchMetric]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotTopicRuleCloudwatchMetric]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotTopicRuleCloudwatchMetric]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d5904fc2e80d2005371de9d212467b696c8e5a97586eaf2037acf28f0c4113b5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class IotTopicRuleCloudwatchMetricOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.iotTopicRule.IotTopicRuleCloudwatchMetricOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__84bd7432c8ad2dea5fa6719f31121f8b3bb510b892cce94bf414ff75fce432b2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetMetricTimestamp")
    def reset_metric_timestamp(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMetricTimestamp", []))

    @builtins.property
    @jsii.member(jsii_name="metricNameInput")
    def metric_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "metricNameInput"))

    @builtins.property
    @jsii.member(jsii_name="metricNamespaceInput")
    def metric_namespace_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "metricNamespaceInput"))

    @builtins.property
    @jsii.member(jsii_name="metricTimestampInput")
    def metric_timestamp_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "metricTimestampInput"))

    @builtins.property
    @jsii.member(jsii_name="metricUnitInput")
    def metric_unit_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "metricUnitInput"))

    @builtins.property
    @jsii.member(jsii_name="metricValueInput")
    def metric_value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "metricValueInput"))

    @builtins.property
    @jsii.member(jsii_name="roleArnInput")
    def role_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "roleArnInput"))

    @builtins.property
    @jsii.member(jsii_name="metricName")
    def metric_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "metricName"))

    @metric_name.setter
    def metric_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__46418cca82bf7a4030c32ef9192c5a458641ea95a4a8300b3c676305e3a372b8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metricName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="metricNamespace")
    def metric_namespace(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "metricNamespace"))

    @metric_namespace.setter
    def metric_namespace(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a6ec03b55983c9ceedd592c2964228f060462125d15d374cbea090cb8cb7ded8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metricNamespace", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="metricTimestamp")
    def metric_timestamp(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "metricTimestamp"))

    @metric_timestamp.setter
    def metric_timestamp(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a299e010e576017e083083b825d87a3d9773c0a1bd844c85fe2a2ae398bda5d1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metricTimestamp", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="metricUnit")
    def metric_unit(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "metricUnit"))

    @metric_unit.setter
    def metric_unit(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5329c379dbff8d6b8195572cb4a12094c85e7d259dbdf12f57677e68e46bb4de)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metricUnit", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="metricValue")
    def metric_value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "metricValue"))

    @metric_value.setter
    def metric_value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e459559b8954c07fe55b7d1c6a721c31b2627e67931dc06d858e6b21ef2b497)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metricValue", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="roleArn")
    def role_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "roleArn"))

    @role_arn.setter
    def role_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d0fce85eed23cbcf0254e06001e9f1aee32a01c0ee2b3ee70c5e0441f6aa4718)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "roleArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IotTopicRuleCloudwatchMetric]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IotTopicRuleCloudwatchMetric]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IotTopicRuleCloudwatchMetric]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f2cbdb615c232b2083dd61d441c54a16a40ff25f3450c411c57e78558042523a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.iotTopicRule.IotTopicRuleConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "enabled": "enabled",
        "name": "name",
        "sql": "sql",
        "sql_version": "sqlVersion",
        "cloudwatch_alarm": "cloudwatchAlarm",
        "cloudwatch_logs": "cloudwatchLogs",
        "cloudwatch_metric": "cloudwatchMetric",
        "description": "description",
        "dynamodb": "dynamodb",
        "dynamodbv2": "dynamodbv2",
        "elasticsearch": "elasticsearch",
        "error_action": "errorAction",
        "firehose": "firehose",
        "http": "http",
        "id": "id",
        "iot_analytics": "iotAnalytics",
        "iot_events": "iotEvents",
        "kafka": "kafka",
        "kinesis": "kinesis",
        "lambda_": "lambda",
        "republish": "republish",
        "s3": "s3",
        "sns": "sns",
        "sqs": "sqs",
        "step_functions": "stepFunctions",
        "tags": "tags",
        "tags_all": "tagsAll",
        "timestream": "timestream",
    },
)
class IotTopicRuleConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        name: builtins.str,
        sql: builtins.str,
        sql_version: builtins.str,
        cloudwatch_alarm: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[IotTopicRuleCloudwatchAlarm, typing.Dict[builtins.str, typing.Any]]]]] = None,
        cloudwatch_logs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[IotTopicRuleCloudwatchLogs, typing.Dict[builtins.str, typing.Any]]]]] = None,
        cloudwatch_metric: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[IotTopicRuleCloudwatchMetric, typing.Dict[builtins.str, typing.Any]]]]] = None,
        description: typing.Optional[builtins.str] = None,
        dynamodb: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["IotTopicRuleDynamodb", typing.Dict[builtins.str, typing.Any]]]]] = None,
        dynamodbv2: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["IotTopicRuleDynamodbv2", typing.Dict[builtins.str, typing.Any]]]]] = None,
        elasticsearch: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["IotTopicRuleElasticsearch", typing.Dict[builtins.str, typing.Any]]]]] = None,
        error_action: typing.Optional[typing.Union["IotTopicRuleErrorAction", typing.Dict[builtins.str, typing.Any]]] = None,
        firehose: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["IotTopicRuleFirehose", typing.Dict[builtins.str, typing.Any]]]]] = None,
        http: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["IotTopicRuleHttp", typing.Dict[builtins.str, typing.Any]]]]] = None,
        id: typing.Optional[builtins.str] = None,
        iot_analytics: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["IotTopicRuleIotAnalytics", typing.Dict[builtins.str, typing.Any]]]]] = None,
        iot_events: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["IotTopicRuleIotEvents", typing.Dict[builtins.str, typing.Any]]]]] = None,
        kafka: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["IotTopicRuleKafka", typing.Dict[builtins.str, typing.Any]]]]] = None,
        kinesis: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["IotTopicRuleKinesis", typing.Dict[builtins.str, typing.Any]]]]] = None,
        lambda_: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["IotTopicRuleLambda", typing.Dict[builtins.str, typing.Any]]]]] = None,
        republish: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["IotTopicRuleRepublish", typing.Dict[builtins.str, typing.Any]]]]] = None,
        s3: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["IotTopicRuleS3", typing.Dict[builtins.str, typing.Any]]]]] = None,
        sns: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["IotTopicRuleSns", typing.Dict[builtins.str, typing.Any]]]]] = None,
        sqs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["IotTopicRuleSqs", typing.Dict[builtins.str, typing.Any]]]]] = None,
        step_functions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["IotTopicRuleStepFunctions", typing.Dict[builtins.str, typing.Any]]]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timestream: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["IotTopicRuleTimestream", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#enabled IotTopicRule#enabled}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#name IotTopicRule#name}.
        :param sql: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#sql IotTopicRule#sql}.
        :param sql_version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#sql_version IotTopicRule#sql_version}.
        :param cloudwatch_alarm: cloudwatch_alarm block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#cloudwatch_alarm IotTopicRule#cloudwatch_alarm}
        :param cloudwatch_logs: cloudwatch_logs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#cloudwatch_logs IotTopicRule#cloudwatch_logs}
        :param cloudwatch_metric: cloudwatch_metric block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#cloudwatch_metric IotTopicRule#cloudwatch_metric}
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#description IotTopicRule#description}.
        :param dynamodb: dynamodb block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#dynamodb IotTopicRule#dynamodb}
        :param dynamodbv2: dynamodbv2 block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#dynamodbv2 IotTopicRule#dynamodbv2}
        :param elasticsearch: elasticsearch block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#elasticsearch IotTopicRule#elasticsearch}
        :param error_action: error_action block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#error_action IotTopicRule#error_action}
        :param firehose: firehose block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#firehose IotTopicRule#firehose}
        :param http: http block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#http IotTopicRule#http}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#id IotTopicRule#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param iot_analytics: iot_analytics block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#iot_analytics IotTopicRule#iot_analytics}
        :param iot_events: iot_events block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#iot_events IotTopicRule#iot_events}
        :param kafka: kafka block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#kafka IotTopicRule#kafka}
        :param kinesis: kinesis block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#kinesis IotTopicRule#kinesis}
        :param lambda_: lambda block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#lambda IotTopicRule#lambda}
        :param republish: republish block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#republish IotTopicRule#republish}
        :param s3: s3 block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#s3 IotTopicRule#s3}
        :param sns: sns block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#sns IotTopicRule#sns}
        :param sqs: sqs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#sqs IotTopicRule#sqs}
        :param step_functions: step_functions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#step_functions IotTopicRule#step_functions}
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#tags IotTopicRule#tags}.
        :param tags_all: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#tags_all IotTopicRule#tags_all}.
        :param timestream: timestream block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#timestream IotTopicRule#timestream}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(error_action, dict):
            error_action = IotTopicRuleErrorAction(**error_action)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__79143a22ba041c9eea32ef371eed79b12fab42325e6871a29a93e1cd5b715234)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument sql", value=sql, expected_type=type_hints["sql"])
            check_type(argname="argument sql_version", value=sql_version, expected_type=type_hints["sql_version"])
            check_type(argname="argument cloudwatch_alarm", value=cloudwatch_alarm, expected_type=type_hints["cloudwatch_alarm"])
            check_type(argname="argument cloudwatch_logs", value=cloudwatch_logs, expected_type=type_hints["cloudwatch_logs"])
            check_type(argname="argument cloudwatch_metric", value=cloudwatch_metric, expected_type=type_hints["cloudwatch_metric"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument dynamodb", value=dynamodb, expected_type=type_hints["dynamodb"])
            check_type(argname="argument dynamodbv2", value=dynamodbv2, expected_type=type_hints["dynamodbv2"])
            check_type(argname="argument elasticsearch", value=elasticsearch, expected_type=type_hints["elasticsearch"])
            check_type(argname="argument error_action", value=error_action, expected_type=type_hints["error_action"])
            check_type(argname="argument firehose", value=firehose, expected_type=type_hints["firehose"])
            check_type(argname="argument http", value=http, expected_type=type_hints["http"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument iot_analytics", value=iot_analytics, expected_type=type_hints["iot_analytics"])
            check_type(argname="argument iot_events", value=iot_events, expected_type=type_hints["iot_events"])
            check_type(argname="argument kafka", value=kafka, expected_type=type_hints["kafka"])
            check_type(argname="argument kinesis", value=kinesis, expected_type=type_hints["kinesis"])
            check_type(argname="argument lambda_", value=lambda_, expected_type=type_hints["lambda_"])
            check_type(argname="argument republish", value=republish, expected_type=type_hints["republish"])
            check_type(argname="argument s3", value=s3, expected_type=type_hints["s3"])
            check_type(argname="argument sns", value=sns, expected_type=type_hints["sns"])
            check_type(argname="argument sqs", value=sqs, expected_type=type_hints["sqs"])
            check_type(argname="argument step_functions", value=step_functions, expected_type=type_hints["step_functions"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument tags_all", value=tags_all, expected_type=type_hints["tags_all"])
            check_type(argname="argument timestream", value=timestream, expected_type=type_hints["timestream"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "enabled": enabled,
            "name": name,
            "sql": sql,
            "sql_version": sql_version,
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
        if cloudwatch_alarm is not None:
            self._values["cloudwatch_alarm"] = cloudwatch_alarm
        if cloudwatch_logs is not None:
            self._values["cloudwatch_logs"] = cloudwatch_logs
        if cloudwatch_metric is not None:
            self._values["cloudwatch_metric"] = cloudwatch_metric
        if description is not None:
            self._values["description"] = description
        if dynamodb is not None:
            self._values["dynamodb"] = dynamodb
        if dynamodbv2 is not None:
            self._values["dynamodbv2"] = dynamodbv2
        if elasticsearch is not None:
            self._values["elasticsearch"] = elasticsearch
        if error_action is not None:
            self._values["error_action"] = error_action
        if firehose is not None:
            self._values["firehose"] = firehose
        if http is not None:
            self._values["http"] = http
        if id is not None:
            self._values["id"] = id
        if iot_analytics is not None:
            self._values["iot_analytics"] = iot_analytics
        if iot_events is not None:
            self._values["iot_events"] = iot_events
        if kafka is not None:
            self._values["kafka"] = kafka
        if kinesis is not None:
            self._values["kinesis"] = kinesis
        if lambda_ is not None:
            self._values["lambda_"] = lambda_
        if republish is not None:
            self._values["republish"] = republish
        if s3 is not None:
            self._values["s3"] = s3
        if sns is not None:
            self._values["sns"] = sns
        if sqs is not None:
            self._values["sqs"] = sqs
        if step_functions is not None:
            self._values["step_functions"] = step_functions
        if tags is not None:
            self._values["tags"] = tags
        if tags_all is not None:
            self._values["tags_all"] = tags_all
        if timestream is not None:
            self._values["timestream"] = timestream

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
    def enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#enabled IotTopicRule#enabled}.'''
        result = self._values.get("enabled")
        assert result is not None, "Required property 'enabled' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#name IotTopicRule#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def sql(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#sql IotTopicRule#sql}.'''
        result = self._values.get("sql")
        assert result is not None, "Required property 'sql' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def sql_version(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#sql_version IotTopicRule#sql_version}.'''
        result = self._values.get("sql_version")
        assert result is not None, "Required property 'sql_version' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def cloudwatch_alarm(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotTopicRuleCloudwatchAlarm]]]:
        '''cloudwatch_alarm block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#cloudwatch_alarm IotTopicRule#cloudwatch_alarm}
        '''
        result = self._values.get("cloudwatch_alarm")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotTopicRuleCloudwatchAlarm]]], result)

    @builtins.property
    def cloudwatch_logs(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotTopicRuleCloudwatchLogs]]]:
        '''cloudwatch_logs block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#cloudwatch_logs IotTopicRule#cloudwatch_logs}
        '''
        result = self._values.get("cloudwatch_logs")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotTopicRuleCloudwatchLogs]]], result)

    @builtins.property
    def cloudwatch_metric(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotTopicRuleCloudwatchMetric]]]:
        '''cloudwatch_metric block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#cloudwatch_metric IotTopicRule#cloudwatch_metric}
        '''
        result = self._values.get("cloudwatch_metric")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotTopicRuleCloudwatchMetric]]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#description IotTopicRule#description}.'''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def dynamodb(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["IotTopicRuleDynamodb"]]]:
        '''dynamodb block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#dynamodb IotTopicRule#dynamodb}
        '''
        result = self._values.get("dynamodb")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["IotTopicRuleDynamodb"]]], result)

    @builtins.property
    def dynamodbv2(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["IotTopicRuleDynamodbv2"]]]:
        '''dynamodbv2 block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#dynamodbv2 IotTopicRule#dynamodbv2}
        '''
        result = self._values.get("dynamodbv2")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["IotTopicRuleDynamodbv2"]]], result)

    @builtins.property
    def elasticsearch(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["IotTopicRuleElasticsearch"]]]:
        '''elasticsearch block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#elasticsearch IotTopicRule#elasticsearch}
        '''
        result = self._values.get("elasticsearch")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["IotTopicRuleElasticsearch"]]], result)

    @builtins.property
    def error_action(self) -> typing.Optional["IotTopicRuleErrorAction"]:
        '''error_action block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#error_action IotTopicRule#error_action}
        '''
        result = self._values.get("error_action")
        return typing.cast(typing.Optional["IotTopicRuleErrorAction"], result)

    @builtins.property
    def firehose(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["IotTopicRuleFirehose"]]]:
        '''firehose block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#firehose IotTopicRule#firehose}
        '''
        result = self._values.get("firehose")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["IotTopicRuleFirehose"]]], result)

    @builtins.property
    def http(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["IotTopicRuleHttp"]]]:
        '''http block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#http IotTopicRule#http}
        '''
        result = self._values.get("http")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["IotTopicRuleHttp"]]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#id IotTopicRule#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def iot_analytics(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["IotTopicRuleIotAnalytics"]]]:
        '''iot_analytics block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#iot_analytics IotTopicRule#iot_analytics}
        '''
        result = self._values.get("iot_analytics")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["IotTopicRuleIotAnalytics"]]], result)

    @builtins.property
    def iot_events(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["IotTopicRuleIotEvents"]]]:
        '''iot_events block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#iot_events IotTopicRule#iot_events}
        '''
        result = self._values.get("iot_events")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["IotTopicRuleIotEvents"]]], result)

    @builtins.property
    def kafka(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["IotTopicRuleKafka"]]]:
        '''kafka block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#kafka IotTopicRule#kafka}
        '''
        result = self._values.get("kafka")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["IotTopicRuleKafka"]]], result)

    @builtins.property
    def kinesis(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["IotTopicRuleKinesis"]]]:
        '''kinesis block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#kinesis IotTopicRule#kinesis}
        '''
        result = self._values.get("kinesis")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["IotTopicRuleKinesis"]]], result)

    @builtins.property
    def lambda_(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["IotTopicRuleLambda"]]]:
        '''lambda block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#lambda IotTopicRule#lambda}
        '''
        result = self._values.get("lambda_")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["IotTopicRuleLambda"]]], result)

    @builtins.property
    def republish(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["IotTopicRuleRepublish"]]]:
        '''republish block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#republish IotTopicRule#republish}
        '''
        result = self._values.get("republish")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["IotTopicRuleRepublish"]]], result)

    @builtins.property
    def s3(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["IotTopicRuleS3"]]]:
        '''s3 block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#s3 IotTopicRule#s3}
        '''
        result = self._values.get("s3")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["IotTopicRuleS3"]]], result)

    @builtins.property
    def sns(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["IotTopicRuleSns"]]]:
        '''sns block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#sns IotTopicRule#sns}
        '''
        result = self._values.get("sns")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["IotTopicRuleSns"]]], result)

    @builtins.property
    def sqs(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["IotTopicRuleSqs"]]]:
        '''sqs block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#sqs IotTopicRule#sqs}
        '''
        result = self._values.get("sqs")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["IotTopicRuleSqs"]]], result)

    @builtins.property
    def step_functions(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["IotTopicRuleStepFunctions"]]]:
        '''step_functions block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#step_functions IotTopicRule#step_functions}
        '''
        result = self._values.get("step_functions")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["IotTopicRuleStepFunctions"]]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#tags IotTopicRule#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def tags_all(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#tags_all IotTopicRule#tags_all}.'''
        result = self._values.get("tags_all")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def timestream(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["IotTopicRuleTimestream"]]]:
        '''timestream block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#timestream IotTopicRule#timestream}
        '''
        result = self._values.get("timestream")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["IotTopicRuleTimestream"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IotTopicRuleConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.iotTopicRule.IotTopicRuleDynamodb",
    jsii_struct_bases=[],
    name_mapping={
        "hash_key_field": "hashKeyField",
        "hash_key_value": "hashKeyValue",
        "role_arn": "roleArn",
        "table_name": "tableName",
        "hash_key_type": "hashKeyType",
        "operation": "operation",
        "payload_field": "payloadField",
        "range_key_field": "rangeKeyField",
        "range_key_type": "rangeKeyType",
        "range_key_value": "rangeKeyValue",
    },
)
class IotTopicRuleDynamodb:
    def __init__(
        self,
        *,
        hash_key_field: builtins.str,
        hash_key_value: builtins.str,
        role_arn: builtins.str,
        table_name: builtins.str,
        hash_key_type: typing.Optional[builtins.str] = None,
        operation: typing.Optional[builtins.str] = None,
        payload_field: typing.Optional[builtins.str] = None,
        range_key_field: typing.Optional[builtins.str] = None,
        range_key_type: typing.Optional[builtins.str] = None,
        range_key_value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param hash_key_field: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#hash_key_field IotTopicRule#hash_key_field}.
        :param hash_key_value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#hash_key_value IotTopicRule#hash_key_value}.
        :param role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#role_arn IotTopicRule#role_arn}.
        :param table_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#table_name IotTopicRule#table_name}.
        :param hash_key_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#hash_key_type IotTopicRule#hash_key_type}.
        :param operation: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#operation IotTopicRule#operation}.
        :param payload_field: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#payload_field IotTopicRule#payload_field}.
        :param range_key_field: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#range_key_field IotTopicRule#range_key_field}.
        :param range_key_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#range_key_type IotTopicRule#range_key_type}.
        :param range_key_value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#range_key_value IotTopicRule#range_key_value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__22c3100b34d960b81cc420672a70182be62148af182e9f3a4a7a978dfefd7772)
            check_type(argname="argument hash_key_field", value=hash_key_field, expected_type=type_hints["hash_key_field"])
            check_type(argname="argument hash_key_value", value=hash_key_value, expected_type=type_hints["hash_key_value"])
            check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
            check_type(argname="argument table_name", value=table_name, expected_type=type_hints["table_name"])
            check_type(argname="argument hash_key_type", value=hash_key_type, expected_type=type_hints["hash_key_type"])
            check_type(argname="argument operation", value=operation, expected_type=type_hints["operation"])
            check_type(argname="argument payload_field", value=payload_field, expected_type=type_hints["payload_field"])
            check_type(argname="argument range_key_field", value=range_key_field, expected_type=type_hints["range_key_field"])
            check_type(argname="argument range_key_type", value=range_key_type, expected_type=type_hints["range_key_type"])
            check_type(argname="argument range_key_value", value=range_key_value, expected_type=type_hints["range_key_value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "hash_key_field": hash_key_field,
            "hash_key_value": hash_key_value,
            "role_arn": role_arn,
            "table_name": table_name,
        }
        if hash_key_type is not None:
            self._values["hash_key_type"] = hash_key_type
        if operation is not None:
            self._values["operation"] = operation
        if payload_field is not None:
            self._values["payload_field"] = payload_field
        if range_key_field is not None:
            self._values["range_key_field"] = range_key_field
        if range_key_type is not None:
            self._values["range_key_type"] = range_key_type
        if range_key_value is not None:
            self._values["range_key_value"] = range_key_value

    @builtins.property
    def hash_key_field(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#hash_key_field IotTopicRule#hash_key_field}.'''
        result = self._values.get("hash_key_field")
        assert result is not None, "Required property 'hash_key_field' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def hash_key_value(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#hash_key_value IotTopicRule#hash_key_value}.'''
        result = self._values.get("hash_key_value")
        assert result is not None, "Required property 'hash_key_value' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def role_arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#role_arn IotTopicRule#role_arn}.'''
        result = self._values.get("role_arn")
        assert result is not None, "Required property 'role_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def table_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#table_name IotTopicRule#table_name}.'''
        result = self._values.get("table_name")
        assert result is not None, "Required property 'table_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def hash_key_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#hash_key_type IotTopicRule#hash_key_type}.'''
        result = self._values.get("hash_key_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def operation(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#operation IotTopicRule#operation}.'''
        result = self._values.get("operation")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def payload_field(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#payload_field IotTopicRule#payload_field}.'''
        result = self._values.get("payload_field")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def range_key_field(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#range_key_field IotTopicRule#range_key_field}.'''
        result = self._values.get("range_key_field")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def range_key_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#range_key_type IotTopicRule#range_key_type}.'''
        result = self._values.get("range_key_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def range_key_value(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#range_key_value IotTopicRule#range_key_value}.'''
        result = self._values.get("range_key_value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IotTopicRuleDynamodb(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class IotTopicRuleDynamodbList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.iotTopicRule.IotTopicRuleDynamodbList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fa8834151932991cb06f43fea73661c56f96800811dca71d20ce01083c380919)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "IotTopicRuleDynamodbOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__92ffcc3095620130b75eaa7f1d18bf6a0080744275acb2ade415c48599199395)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("IotTopicRuleDynamodbOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f1f52b8cd18c2e40c7551bc6fd01b4d1cc348861569559451c054599ad4f8182)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d94f7e43958e67170fdecbc8055c89da284aeeafedbebd76fc04fb0e77177765)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bcfdadfa49808c05efb86e4a188573be99320567ef44c5e0670d6d5c9b1b5e83)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotTopicRuleDynamodb]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotTopicRuleDynamodb]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotTopicRuleDynamodb]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__177f5f934c5ab7b4cd8bb7c8b8fa32839a70ee6256e4e19ff5f93fda9189156d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class IotTopicRuleDynamodbOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.iotTopicRule.IotTopicRuleDynamodbOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__052a732588371805c94bd72722c6112b4bc87b8191a863492b195499c59ab86c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetHashKeyType")
    def reset_hash_key_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHashKeyType", []))

    @jsii.member(jsii_name="resetOperation")
    def reset_operation(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOperation", []))

    @jsii.member(jsii_name="resetPayloadField")
    def reset_payload_field(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPayloadField", []))

    @jsii.member(jsii_name="resetRangeKeyField")
    def reset_range_key_field(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRangeKeyField", []))

    @jsii.member(jsii_name="resetRangeKeyType")
    def reset_range_key_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRangeKeyType", []))

    @jsii.member(jsii_name="resetRangeKeyValue")
    def reset_range_key_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRangeKeyValue", []))

    @builtins.property
    @jsii.member(jsii_name="hashKeyFieldInput")
    def hash_key_field_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "hashKeyFieldInput"))

    @builtins.property
    @jsii.member(jsii_name="hashKeyTypeInput")
    def hash_key_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "hashKeyTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="hashKeyValueInput")
    def hash_key_value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "hashKeyValueInput"))

    @builtins.property
    @jsii.member(jsii_name="operationInput")
    def operation_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "operationInput"))

    @builtins.property
    @jsii.member(jsii_name="payloadFieldInput")
    def payload_field_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "payloadFieldInput"))

    @builtins.property
    @jsii.member(jsii_name="rangeKeyFieldInput")
    def range_key_field_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "rangeKeyFieldInput"))

    @builtins.property
    @jsii.member(jsii_name="rangeKeyTypeInput")
    def range_key_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "rangeKeyTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="rangeKeyValueInput")
    def range_key_value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "rangeKeyValueInput"))

    @builtins.property
    @jsii.member(jsii_name="roleArnInput")
    def role_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "roleArnInput"))

    @builtins.property
    @jsii.member(jsii_name="tableNameInput")
    def table_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tableNameInput"))

    @builtins.property
    @jsii.member(jsii_name="hashKeyField")
    def hash_key_field(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "hashKeyField"))

    @hash_key_field.setter
    def hash_key_field(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ddb45da7df9924a79ef94c7f086ae4711cb7578362927914ff14f5a203cbdad7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hashKeyField", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="hashKeyType")
    def hash_key_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "hashKeyType"))

    @hash_key_type.setter
    def hash_key_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__53ba42ad39d7fc6e9b97251156725af5f5d54962a35e3ad0c98838ff02670e28)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hashKeyType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="hashKeyValue")
    def hash_key_value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "hashKeyValue"))

    @hash_key_value.setter
    def hash_key_value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ff46e31673192af32e51c598657d261a86ec4cc237965cfd02fb18784424417c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hashKeyValue", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="operation")
    def operation(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "operation"))

    @operation.setter
    def operation(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2c1223a116daf3b235be35b89af1b6b7222896203756d970596ee49c3fc882b3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "operation", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="payloadField")
    def payload_field(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "payloadField"))

    @payload_field.setter
    def payload_field(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a36becd3740b98121bd36dc7f1a1dd0e3ed116c07f693d00e06f2d1971ec876)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "payloadField", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="rangeKeyField")
    def range_key_field(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "rangeKeyField"))

    @range_key_field.setter
    def range_key_field(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__abc7970fd1a61d2b2ec03bfc86dd46acc17a92e78cd7ea03e9f84703adc922da)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rangeKeyField", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="rangeKeyType")
    def range_key_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "rangeKeyType"))

    @range_key_type.setter
    def range_key_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__00510fc6ace6370735892b94c32df9c0d1daf21ec5979dc395bb97c92efc1292)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rangeKeyType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="rangeKeyValue")
    def range_key_value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "rangeKeyValue"))

    @range_key_value.setter
    def range_key_value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__37855fc02838a52efcfd6a11c72d791f1accc068752906cfb86bc0687002023d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rangeKeyValue", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="roleArn")
    def role_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "roleArn"))

    @role_arn.setter
    def role_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__442e11f4126f9b640e9fe94f5c48d7471aed5037982657a0c0385ea750de4f91)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "roleArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tableName")
    def table_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tableName"))

    @table_name.setter
    def table_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b04308f3c7092005dc735554db20991967accdf1d6eb0fa8d264104109107af)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tableName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IotTopicRuleDynamodb]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IotTopicRuleDynamodb]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IotTopicRuleDynamodb]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f748855ac08bc423e06f192bd458b199fd4a278925d171c5ccaf0d169882e06)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.iotTopicRule.IotTopicRuleDynamodbv2",
    jsii_struct_bases=[],
    name_mapping={"role_arn": "roleArn", "put_item": "putItem"},
)
class IotTopicRuleDynamodbv2:
    def __init__(
        self,
        *,
        role_arn: builtins.str,
        put_item: typing.Optional[typing.Union["IotTopicRuleDynamodbv2PutItem", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#role_arn IotTopicRule#role_arn}.
        :param put_item: put_item block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#put_item IotTopicRule#put_item}
        '''
        if isinstance(put_item, dict):
            put_item = IotTopicRuleDynamodbv2PutItem(**put_item)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__62daf13af5aac5699378f7ce8e0323d6511dc6846bab3ea09beacf5a0388e3f8)
            check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
            check_type(argname="argument put_item", value=put_item, expected_type=type_hints["put_item"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "role_arn": role_arn,
        }
        if put_item is not None:
            self._values["put_item"] = put_item

    @builtins.property
    def role_arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#role_arn IotTopicRule#role_arn}.'''
        result = self._values.get("role_arn")
        assert result is not None, "Required property 'role_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def put_item(self) -> typing.Optional["IotTopicRuleDynamodbv2PutItem"]:
        '''put_item block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#put_item IotTopicRule#put_item}
        '''
        result = self._values.get("put_item")
        return typing.cast(typing.Optional["IotTopicRuleDynamodbv2PutItem"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IotTopicRuleDynamodbv2(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class IotTopicRuleDynamodbv2List(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.iotTopicRule.IotTopicRuleDynamodbv2List",
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
            type_hints = typing.get_type_hints(_typecheckingstub__219e540e2f072f12683a6e8eedcc550e1a5dee24c3c3391366f555791769d26a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "IotTopicRuleDynamodbv2OutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9c4a72440118e1093c6e533b72a90a36766d58ea867aa3fcbd9a9f8d7cda7854)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("IotTopicRuleDynamodbv2OutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f27d74caf7df9666017cd4a62f5fbb24159ee1d30daa9806526ef322f631267c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__efbbbb3946fe5d0a6632612062c408bf00cc0470f4b09424cdf4e0c2bc166327)
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
            type_hints = typing.get_type_hints(_typecheckingstub__61537d4f0d630f3663c72a70968b10c556b0e4524eed787cd4173c4e12ccc19c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotTopicRuleDynamodbv2]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotTopicRuleDynamodbv2]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotTopicRuleDynamodbv2]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__619a43024d80d2590d0263d956febf146537dcfc3f53d22b9ebb256cb8890dbb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class IotTopicRuleDynamodbv2OutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.iotTopicRule.IotTopicRuleDynamodbv2OutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a7995c1a3786cde3536cbb9c02ba0567b7d421ea2b0c15b9876e512dab923ca2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putPutItem")
    def put_put_item(self, *, table_name: builtins.str) -> None:
        '''
        :param table_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#table_name IotTopicRule#table_name}.
        '''
        value = IotTopicRuleDynamodbv2PutItem(table_name=table_name)

        return typing.cast(None, jsii.invoke(self, "putPutItem", [value]))

    @jsii.member(jsii_name="resetPutItem")
    def reset_put_item(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPutItem", []))

    @builtins.property
    @jsii.member(jsii_name="putItem")
    def put_item(self) -> "IotTopicRuleDynamodbv2PutItemOutputReference":
        return typing.cast("IotTopicRuleDynamodbv2PutItemOutputReference", jsii.get(self, "putItem"))

    @builtins.property
    @jsii.member(jsii_name="putItemInput")
    def put_item_input(self) -> typing.Optional["IotTopicRuleDynamodbv2PutItem"]:
        return typing.cast(typing.Optional["IotTopicRuleDynamodbv2PutItem"], jsii.get(self, "putItemInput"))

    @builtins.property
    @jsii.member(jsii_name="roleArnInput")
    def role_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "roleArnInput"))

    @builtins.property
    @jsii.member(jsii_name="roleArn")
    def role_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "roleArn"))

    @role_arn.setter
    def role_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c0dac94056b69bde5a6f271a4c65b6d1b7dd8a840546e72d7a3083059f3d065a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "roleArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IotTopicRuleDynamodbv2]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IotTopicRuleDynamodbv2]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IotTopicRuleDynamodbv2]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__00dd34b29c2fd0693ffed132977d6d2573126dc2a5df0d566abf3593175e19ef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.iotTopicRule.IotTopicRuleDynamodbv2PutItem",
    jsii_struct_bases=[],
    name_mapping={"table_name": "tableName"},
)
class IotTopicRuleDynamodbv2PutItem:
    def __init__(self, *, table_name: builtins.str) -> None:
        '''
        :param table_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#table_name IotTopicRule#table_name}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__77bc4ab141d48c3bc032a5cb5b76a3b175fd3f5ee3655d84df475862cb45ff58)
            check_type(argname="argument table_name", value=table_name, expected_type=type_hints["table_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "table_name": table_name,
        }

    @builtins.property
    def table_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#table_name IotTopicRule#table_name}.'''
        result = self._values.get("table_name")
        assert result is not None, "Required property 'table_name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IotTopicRuleDynamodbv2PutItem(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class IotTopicRuleDynamodbv2PutItemOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.iotTopicRule.IotTopicRuleDynamodbv2PutItemOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__842a0b1147773300406ce0d036ec519682eda30eadccf71540c3931a7cf58c49)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="tableNameInput")
    def table_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tableNameInput"))

    @builtins.property
    @jsii.member(jsii_name="tableName")
    def table_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tableName"))

    @table_name.setter
    def table_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc1539f3e331c3f1ad210c24468485f3e96cbf740f69088eb7c47049988614b5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tableName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[IotTopicRuleDynamodbv2PutItem]:
        return typing.cast(typing.Optional[IotTopicRuleDynamodbv2PutItem], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[IotTopicRuleDynamodbv2PutItem],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__82bcb5de017af6bd9c493e135277e5f11e58d58a9e866b0daf9e4a088dfc49a1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.iotTopicRule.IotTopicRuleElasticsearch",
    jsii_struct_bases=[],
    name_mapping={
        "endpoint": "endpoint",
        "id": "id",
        "index": "index",
        "role_arn": "roleArn",
        "type": "type",
    },
)
class IotTopicRuleElasticsearch:
    def __init__(
        self,
        *,
        endpoint: builtins.str,
        id: builtins.str,
        index: builtins.str,
        role_arn: builtins.str,
        type: builtins.str,
    ) -> None:
        '''
        :param endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#endpoint IotTopicRule#endpoint}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#id IotTopicRule#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param index: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#index IotTopicRule#index}.
        :param role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#role_arn IotTopicRule#role_arn}.
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#type IotTopicRule#type}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__85248bb147339c0a761a11368cc36850e675754c092614956f29c191ce83453a)
            check_type(argname="argument endpoint", value=endpoint, expected_type=type_hints["endpoint"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
            check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "endpoint": endpoint,
            "id": id,
            "index": index,
            "role_arn": role_arn,
            "type": type,
        }

    @builtins.property
    def endpoint(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#endpoint IotTopicRule#endpoint}.'''
        result = self._values.get("endpoint")
        assert result is not None, "Required property 'endpoint' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#id IotTopicRule#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        assert result is not None, "Required property 'id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def index(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#index IotTopicRule#index}.'''
        result = self._values.get("index")
        assert result is not None, "Required property 'index' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def role_arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#role_arn IotTopicRule#role_arn}.'''
        result = self._values.get("role_arn")
        assert result is not None, "Required property 'role_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#type IotTopicRule#type}.'''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IotTopicRuleElasticsearch(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class IotTopicRuleElasticsearchList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.iotTopicRule.IotTopicRuleElasticsearchList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__390cfbe9caf31143d67982b77ba3398d5db3912659ff58b539c543ad329a8470)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "IotTopicRuleElasticsearchOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__332cc3eeedb252068e2c2f6007c594f312144f6795779a2bb217a80882ea6b8e)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("IotTopicRuleElasticsearchOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__21d9c9d7d268c528ae7f94808420b3c801c635de51641ee0e81e07c0060506e4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3eabfeae4b048f323ab019bbeb0a4baa38b52ccf1c708e7e8b2695f7265f923d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__aa86dd3df0b4412c98c7aafebba49d631f1d7062568dc10e5d7826f7ad120e26)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotTopicRuleElasticsearch]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotTopicRuleElasticsearch]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotTopicRuleElasticsearch]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2235187eaf52e5ae6c943aa5015e37c5b0c13cceb91ca63c2cf38572ebd663a2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class IotTopicRuleElasticsearchOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.iotTopicRule.IotTopicRuleElasticsearchOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__927a9b6f8831430d4b511d2811db3cce5dd3ce1998d4cdcbc13224f6b265009d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="endpointInput")
    def endpoint_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "endpointInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="indexInput")
    def index_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "indexInput"))

    @builtins.property
    @jsii.member(jsii_name="roleArnInput")
    def role_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "roleArnInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="endpoint")
    def endpoint(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "endpoint"))

    @endpoint.setter
    def endpoint(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__47a529b121a8b6a398651caa66ff29bfe3f86e1a95025139f41b9bc7b099a6f7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "endpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc010db433ce71b7486800ca4abb21a15d4780fd42379d452a579afe6fdd11b4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="index")
    def index(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "index"))

    @index.setter
    def index(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0e68a618119ac60043834a67f329284c78c1356c43e7cb39288ce03529755504)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "index", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="roleArn")
    def role_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "roleArn"))

    @role_arn.setter
    def role_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6fc890eae303a9905a9cd9dd9a2d4d54f44dc49ffb231e158baec07fbbff4bfd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "roleArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__55c043ede332b77b071da5f45286a0c6c07f28a3c64a744d3ee662ac81d1fb24)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IotTopicRuleElasticsearch]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IotTopicRuleElasticsearch]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IotTopicRuleElasticsearch]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__545a1e84c722158d4845742b7d35799ac2381ad1ca406837a638431d260a2a35)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.iotTopicRule.IotTopicRuleErrorAction",
    jsii_struct_bases=[],
    name_mapping={
        "cloudwatch_alarm": "cloudwatchAlarm",
        "cloudwatch_logs": "cloudwatchLogs",
        "cloudwatch_metric": "cloudwatchMetric",
        "dynamodb": "dynamodb",
        "dynamodbv2": "dynamodbv2",
        "elasticsearch": "elasticsearch",
        "firehose": "firehose",
        "http": "http",
        "iot_analytics": "iotAnalytics",
        "iot_events": "iotEvents",
        "kafka": "kafka",
        "kinesis": "kinesis",
        "lambda_": "lambda",
        "republish": "republish",
        "s3": "s3",
        "sns": "sns",
        "sqs": "sqs",
        "step_functions": "stepFunctions",
        "timestream": "timestream",
    },
)
class IotTopicRuleErrorAction:
    def __init__(
        self,
        *,
        cloudwatch_alarm: typing.Optional[typing.Union["IotTopicRuleErrorActionCloudwatchAlarm", typing.Dict[builtins.str, typing.Any]]] = None,
        cloudwatch_logs: typing.Optional[typing.Union["IotTopicRuleErrorActionCloudwatchLogs", typing.Dict[builtins.str, typing.Any]]] = None,
        cloudwatch_metric: typing.Optional[typing.Union["IotTopicRuleErrorActionCloudwatchMetric", typing.Dict[builtins.str, typing.Any]]] = None,
        dynamodb: typing.Optional[typing.Union["IotTopicRuleErrorActionDynamodb", typing.Dict[builtins.str, typing.Any]]] = None,
        dynamodbv2: typing.Optional[typing.Union["IotTopicRuleErrorActionDynamodbv2", typing.Dict[builtins.str, typing.Any]]] = None,
        elasticsearch: typing.Optional[typing.Union["IotTopicRuleErrorActionElasticsearch", typing.Dict[builtins.str, typing.Any]]] = None,
        firehose: typing.Optional[typing.Union["IotTopicRuleErrorActionFirehose", typing.Dict[builtins.str, typing.Any]]] = None,
        http: typing.Optional[typing.Union["IotTopicRuleErrorActionHttp", typing.Dict[builtins.str, typing.Any]]] = None,
        iot_analytics: typing.Optional[typing.Union["IotTopicRuleErrorActionIotAnalytics", typing.Dict[builtins.str, typing.Any]]] = None,
        iot_events: typing.Optional[typing.Union["IotTopicRuleErrorActionIotEvents", typing.Dict[builtins.str, typing.Any]]] = None,
        kafka: typing.Optional[typing.Union["IotTopicRuleErrorActionKafka", typing.Dict[builtins.str, typing.Any]]] = None,
        kinesis: typing.Optional[typing.Union["IotTopicRuleErrorActionKinesis", typing.Dict[builtins.str, typing.Any]]] = None,
        lambda_: typing.Optional[typing.Union["IotTopicRuleErrorActionLambda", typing.Dict[builtins.str, typing.Any]]] = None,
        republish: typing.Optional[typing.Union["IotTopicRuleErrorActionRepublish", typing.Dict[builtins.str, typing.Any]]] = None,
        s3: typing.Optional[typing.Union["IotTopicRuleErrorActionS3", typing.Dict[builtins.str, typing.Any]]] = None,
        sns: typing.Optional[typing.Union["IotTopicRuleErrorActionSns", typing.Dict[builtins.str, typing.Any]]] = None,
        sqs: typing.Optional[typing.Union["IotTopicRuleErrorActionSqs", typing.Dict[builtins.str, typing.Any]]] = None,
        step_functions: typing.Optional[typing.Union["IotTopicRuleErrorActionStepFunctions", typing.Dict[builtins.str, typing.Any]]] = None,
        timestream: typing.Optional[typing.Union["IotTopicRuleErrorActionTimestream", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param cloudwatch_alarm: cloudwatch_alarm block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#cloudwatch_alarm IotTopicRule#cloudwatch_alarm}
        :param cloudwatch_logs: cloudwatch_logs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#cloudwatch_logs IotTopicRule#cloudwatch_logs}
        :param cloudwatch_metric: cloudwatch_metric block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#cloudwatch_metric IotTopicRule#cloudwatch_metric}
        :param dynamodb: dynamodb block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#dynamodb IotTopicRule#dynamodb}
        :param dynamodbv2: dynamodbv2 block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#dynamodbv2 IotTopicRule#dynamodbv2}
        :param elasticsearch: elasticsearch block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#elasticsearch IotTopicRule#elasticsearch}
        :param firehose: firehose block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#firehose IotTopicRule#firehose}
        :param http: http block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#http IotTopicRule#http}
        :param iot_analytics: iot_analytics block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#iot_analytics IotTopicRule#iot_analytics}
        :param iot_events: iot_events block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#iot_events IotTopicRule#iot_events}
        :param kafka: kafka block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#kafka IotTopicRule#kafka}
        :param kinesis: kinesis block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#kinesis IotTopicRule#kinesis}
        :param lambda_: lambda block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#lambda IotTopicRule#lambda}
        :param republish: republish block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#republish IotTopicRule#republish}
        :param s3: s3 block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#s3 IotTopicRule#s3}
        :param sns: sns block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#sns IotTopicRule#sns}
        :param sqs: sqs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#sqs IotTopicRule#sqs}
        :param step_functions: step_functions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#step_functions IotTopicRule#step_functions}
        :param timestream: timestream block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#timestream IotTopicRule#timestream}
        '''
        if isinstance(cloudwatch_alarm, dict):
            cloudwatch_alarm = IotTopicRuleErrorActionCloudwatchAlarm(**cloudwatch_alarm)
        if isinstance(cloudwatch_logs, dict):
            cloudwatch_logs = IotTopicRuleErrorActionCloudwatchLogs(**cloudwatch_logs)
        if isinstance(cloudwatch_metric, dict):
            cloudwatch_metric = IotTopicRuleErrorActionCloudwatchMetric(**cloudwatch_metric)
        if isinstance(dynamodb, dict):
            dynamodb = IotTopicRuleErrorActionDynamodb(**dynamodb)
        if isinstance(dynamodbv2, dict):
            dynamodbv2 = IotTopicRuleErrorActionDynamodbv2(**dynamodbv2)
        if isinstance(elasticsearch, dict):
            elasticsearch = IotTopicRuleErrorActionElasticsearch(**elasticsearch)
        if isinstance(firehose, dict):
            firehose = IotTopicRuleErrorActionFirehose(**firehose)
        if isinstance(http, dict):
            http = IotTopicRuleErrorActionHttp(**http)
        if isinstance(iot_analytics, dict):
            iot_analytics = IotTopicRuleErrorActionIotAnalytics(**iot_analytics)
        if isinstance(iot_events, dict):
            iot_events = IotTopicRuleErrorActionIotEvents(**iot_events)
        if isinstance(kafka, dict):
            kafka = IotTopicRuleErrorActionKafka(**kafka)
        if isinstance(kinesis, dict):
            kinesis = IotTopicRuleErrorActionKinesis(**kinesis)
        if isinstance(lambda_, dict):
            lambda_ = IotTopicRuleErrorActionLambda(**lambda_)
        if isinstance(republish, dict):
            republish = IotTopicRuleErrorActionRepublish(**republish)
        if isinstance(s3, dict):
            s3 = IotTopicRuleErrorActionS3(**s3)
        if isinstance(sns, dict):
            sns = IotTopicRuleErrorActionSns(**sns)
        if isinstance(sqs, dict):
            sqs = IotTopicRuleErrorActionSqs(**sqs)
        if isinstance(step_functions, dict):
            step_functions = IotTopicRuleErrorActionStepFunctions(**step_functions)
        if isinstance(timestream, dict):
            timestream = IotTopicRuleErrorActionTimestream(**timestream)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bed9afd42f9d12d79e1db0e5a9c43e0a0f3b58e034660e13ee4da4b2232b46a5)
            check_type(argname="argument cloudwatch_alarm", value=cloudwatch_alarm, expected_type=type_hints["cloudwatch_alarm"])
            check_type(argname="argument cloudwatch_logs", value=cloudwatch_logs, expected_type=type_hints["cloudwatch_logs"])
            check_type(argname="argument cloudwatch_metric", value=cloudwatch_metric, expected_type=type_hints["cloudwatch_metric"])
            check_type(argname="argument dynamodb", value=dynamodb, expected_type=type_hints["dynamodb"])
            check_type(argname="argument dynamodbv2", value=dynamodbv2, expected_type=type_hints["dynamodbv2"])
            check_type(argname="argument elasticsearch", value=elasticsearch, expected_type=type_hints["elasticsearch"])
            check_type(argname="argument firehose", value=firehose, expected_type=type_hints["firehose"])
            check_type(argname="argument http", value=http, expected_type=type_hints["http"])
            check_type(argname="argument iot_analytics", value=iot_analytics, expected_type=type_hints["iot_analytics"])
            check_type(argname="argument iot_events", value=iot_events, expected_type=type_hints["iot_events"])
            check_type(argname="argument kafka", value=kafka, expected_type=type_hints["kafka"])
            check_type(argname="argument kinesis", value=kinesis, expected_type=type_hints["kinesis"])
            check_type(argname="argument lambda_", value=lambda_, expected_type=type_hints["lambda_"])
            check_type(argname="argument republish", value=republish, expected_type=type_hints["republish"])
            check_type(argname="argument s3", value=s3, expected_type=type_hints["s3"])
            check_type(argname="argument sns", value=sns, expected_type=type_hints["sns"])
            check_type(argname="argument sqs", value=sqs, expected_type=type_hints["sqs"])
            check_type(argname="argument step_functions", value=step_functions, expected_type=type_hints["step_functions"])
            check_type(argname="argument timestream", value=timestream, expected_type=type_hints["timestream"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if cloudwatch_alarm is not None:
            self._values["cloudwatch_alarm"] = cloudwatch_alarm
        if cloudwatch_logs is not None:
            self._values["cloudwatch_logs"] = cloudwatch_logs
        if cloudwatch_metric is not None:
            self._values["cloudwatch_metric"] = cloudwatch_metric
        if dynamodb is not None:
            self._values["dynamodb"] = dynamodb
        if dynamodbv2 is not None:
            self._values["dynamodbv2"] = dynamodbv2
        if elasticsearch is not None:
            self._values["elasticsearch"] = elasticsearch
        if firehose is not None:
            self._values["firehose"] = firehose
        if http is not None:
            self._values["http"] = http
        if iot_analytics is not None:
            self._values["iot_analytics"] = iot_analytics
        if iot_events is not None:
            self._values["iot_events"] = iot_events
        if kafka is not None:
            self._values["kafka"] = kafka
        if kinesis is not None:
            self._values["kinesis"] = kinesis
        if lambda_ is not None:
            self._values["lambda_"] = lambda_
        if republish is not None:
            self._values["republish"] = republish
        if s3 is not None:
            self._values["s3"] = s3
        if sns is not None:
            self._values["sns"] = sns
        if sqs is not None:
            self._values["sqs"] = sqs
        if step_functions is not None:
            self._values["step_functions"] = step_functions
        if timestream is not None:
            self._values["timestream"] = timestream

    @builtins.property
    def cloudwatch_alarm(
        self,
    ) -> typing.Optional["IotTopicRuleErrorActionCloudwatchAlarm"]:
        '''cloudwatch_alarm block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#cloudwatch_alarm IotTopicRule#cloudwatch_alarm}
        '''
        result = self._values.get("cloudwatch_alarm")
        return typing.cast(typing.Optional["IotTopicRuleErrorActionCloudwatchAlarm"], result)

    @builtins.property
    def cloudwatch_logs(
        self,
    ) -> typing.Optional["IotTopicRuleErrorActionCloudwatchLogs"]:
        '''cloudwatch_logs block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#cloudwatch_logs IotTopicRule#cloudwatch_logs}
        '''
        result = self._values.get("cloudwatch_logs")
        return typing.cast(typing.Optional["IotTopicRuleErrorActionCloudwatchLogs"], result)

    @builtins.property
    def cloudwatch_metric(
        self,
    ) -> typing.Optional["IotTopicRuleErrorActionCloudwatchMetric"]:
        '''cloudwatch_metric block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#cloudwatch_metric IotTopicRule#cloudwatch_metric}
        '''
        result = self._values.get("cloudwatch_metric")
        return typing.cast(typing.Optional["IotTopicRuleErrorActionCloudwatchMetric"], result)

    @builtins.property
    def dynamodb(self) -> typing.Optional["IotTopicRuleErrorActionDynamodb"]:
        '''dynamodb block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#dynamodb IotTopicRule#dynamodb}
        '''
        result = self._values.get("dynamodb")
        return typing.cast(typing.Optional["IotTopicRuleErrorActionDynamodb"], result)

    @builtins.property
    def dynamodbv2(self) -> typing.Optional["IotTopicRuleErrorActionDynamodbv2"]:
        '''dynamodbv2 block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#dynamodbv2 IotTopicRule#dynamodbv2}
        '''
        result = self._values.get("dynamodbv2")
        return typing.cast(typing.Optional["IotTopicRuleErrorActionDynamodbv2"], result)

    @builtins.property
    def elasticsearch(self) -> typing.Optional["IotTopicRuleErrorActionElasticsearch"]:
        '''elasticsearch block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#elasticsearch IotTopicRule#elasticsearch}
        '''
        result = self._values.get("elasticsearch")
        return typing.cast(typing.Optional["IotTopicRuleErrorActionElasticsearch"], result)

    @builtins.property
    def firehose(self) -> typing.Optional["IotTopicRuleErrorActionFirehose"]:
        '''firehose block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#firehose IotTopicRule#firehose}
        '''
        result = self._values.get("firehose")
        return typing.cast(typing.Optional["IotTopicRuleErrorActionFirehose"], result)

    @builtins.property
    def http(self) -> typing.Optional["IotTopicRuleErrorActionHttp"]:
        '''http block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#http IotTopicRule#http}
        '''
        result = self._values.get("http")
        return typing.cast(typing.Optional["IotTopicRuleErrorActionHttp"], result)

    @builtins.property
    def iot_analytics(self) -> typing.Optional["IotTopicRuleErrorActionIotAnalytics"]:
        '''iot_analytics block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#iot_analytics IotTopicRule#iot_analytics}
        '''
        result = self._values.get("iot_analytics")
        return typing.cast(typing.Optional["IotTopicRuleErrorActionIotAnalytics"], result)

    @builtins.property
    def iot_events(self) -> typing.Optional["IotTopicRuleErrorActionIotEvents"]:
        '''iot_events block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#iot_events IotTopicRule#iot_events}
        '''
        result = self._values.get("iot_events")
        return typing.cast(typing.Optional["IotTopicRuleErrorActionIotEvents"], result)

    @builtins.property
    def kafka(self) -> typing.Optional["IotTopicRuleErrorActionKafka"]:
        '''kafka block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#kafka IotTopicRule#kafka}
        '''
        result = self._values.get("kafka")
        return typing.cast(typing.Optional["IotTopicRuleErrorActionKafka"], result)

    @builtins.property
    def kinesis(self) -> typing.Optional["IotTopicRuleErrorActionKinesis"]:
        '''kinesis block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#kinesis IotTopicRule#kinesis}
        '''
        result = self._values.get("kinesis")
        return typing.cast(typing.Optional["IotTopicRuleErrorActionKinesis"], result)

    @builtins.property
    def lambda_(self) -> typing.Optional["IotTopicRuleErrorActionLambda"]:
        '''lambda block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#lambda IotTopicRule#lambda}
        '''
        result = self._values.get("lambda_")
        return typing.cast(typing.Optional["IotTopicRuleErrorActionLambda"], result)

    @builtins.property
    def republish(self) -> typing.Optional["IotTopicRuleErrorActionRepublish"]:
        '''republish block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#republish IotTopicRule#republish}
        '''
        result = self._values.get("republish")
        return typing.cast(typing.Optional["IotTopicRuleErrorActionRepublish"], result)

    @builtins.property
    def s3(self) -> typing.Optional["IotTopicRuleErrorActionS3"]:
        '''s3 block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#s3 IotTopicRule#s3}
        '''
        result = self._values.get("s3")
        return typing.cast(typing.Optional["IotTopicRuleErrorActionS3"], result)

    @builtins.property
    def sns(self) -> typing.Optional["IotTopicRuleErrorActionSns"]:
        '''sns block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#sns IotTopicRule#sns}
        '''
        result = self._values.get("sns")
        return typing.cast(typing.Optional["IotTopicRuleErrorActionSns"], result)

    @builtins.property
    def sqs(self) -> typing.Optional["IotTopicRuleErrorActionSqs"]:
        '''sqs block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#sqs IotTopicRule#sqs}
        '''
        result = self._values.get("sqs")
        return typing.cast(typing.Optional["IotTopicRuleErrorActionSqs"], result)

    @builtins.property
    def step_functions(self) -> typing.Optional["IotTopicRuleErrorActionStepFunctions"]:
        '''step_functions block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#step_functions IotTopicRule#step_functions}
        '''
        result = self._values.get("step_functions")
        return typing.cast(typing.Optional["IotTopicRuleErrorActionStepFunctions"], result)

    @builtins.property
    def timestream(self) -> typing.Optional["IotTopicRuleErrorActionTimestream"]:
        '''timestream block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#timestream IotTopicRule#timestream}
        '''
        result = self._values.get("timestream")
        return typing.cast(typing.Optional["IotTopicRuleErrorActionTimestream"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IotTopicRuleErrorAction(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.iotTopicRule.IotTopicRuleErrorActionCloudwatchAlarm",
    jsii_struct_bases=[],
    name_mapping={
        "alarm_name": "alarmName",
        "role_arn": "roleArn",
        "state_reason": "stateReason",
        "state_value": "stateValue",
    },
)
class IotTopicRuleErrorActionCloudwatchAlarm:
    def __init__(
        self,
        *,
        alarm_name: builtins.str,
        role_arn: builtins.str,
        state_reason: builtins.str,
        state_value: builtins.str,
    ) -> None:
        '''
        :param alarm_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#alarm_name IotTopicRule#alarm_name}.
        :param role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#role_arn IotTopicRule#role_arn}.
        :param state_reason: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#state_reason IotTopicRule#state_reason}.
        :param state_value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#state_value IotTopicRule#state_value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b83d8476ae22b1c65f01786a598701333ed2b69fb621cec167b0261f3369d4f2)
            check_type(argname="argument alarm_name", value=alarm_name, expected_type=type_hints["alarm_name"])
            check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
            check_type(argname="argument state_reason", value=state_reason, expected_type=type_hints["state_reason"])
            check_type(argname="argument state_value", value=state_value, expected_type=type_hints["state_value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "alarm_name": alarm_name,
            "role_arn": role_arn,
            "state_reason": state_reason,
            "state_value": state_value,
        }

    @builtins.property
    def alarm_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#alarm_name IotTopicRule#alarm_name}.'''
        result = self._values.get("alarm_name")
        assert result is not None, "Required property 'alarm_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def role_arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#role_arn IotTopicRule#role_arn}.'''
        result = self._values.get("role_arn")
        assert result is not None, "Required property 'role_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def state_reason(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#state_reason IotTopicRule#state_reason}.'''
        result = self._values.get("state_reason")
        assert result is not None, "Required property 'state_reason' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def state_value(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#state_value IotTopicRule#state_value}.'''
        result = self._values.get("state_value")
        assert result is not None, "Required property 'state_value' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IotTopicRuleErrorActionCloudwatchAlarm(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class IotTopicRuleErrorActionCloudwatchAlarmOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.iotTopicRule.IotTopicRuleErrorActionCloudwatchAlarmOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__762df605998f5f70bbc60ba53cc58a393ee90b36a150c8cfe95dc1867202a8ba)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="alarmNameInput")
    def alarm_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "alarmNameInput"))

    @builtins.property
    @jsii.member(jsii_name="roleArnInput")
    def role_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "roleArnInput"))

    @builtins.property
    @jsii.member(jsii_name="stateReasonInput")
    def state_reason_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "stateReasonInput"))

    @builtins.property
    @jsii.member(jsii_name="stateValueInput")
    def state_value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "stateValueInput"))

    @builtins.property
    @jsii.member(jsii_name="alarmName")
    def alarm_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "alarmName"))

    @alarm_name.setter
    def alarm_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__68438aeca9f46681171eb7ba723318fbd8ea11a2eaa6dd96b89811a3938f3763)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "alarmName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="roleArn")
    def role_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "roleArn"))

    @role_arn.setter
    def role_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__23b2217c7ef545cbeda02403597143c77e2fdd40abbacdac5b34f96c86dcba39)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "roleArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="stateReason")
    def state_reason(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "stateReason"))

    @state_reason.setter
    def state_reason(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5fcfb23e800e0403f181f7f8f2d1a4c2738ba49588f43b2a292716379843d66c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "stateReason", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="stateValue")
    def state_value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "stateValue"))

    @state_value.setter
    def state_value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__81be8922e2c21f86cc8cd9b62f8a360bde2e609710ecc751193d61b2bdb0ce91)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "stateValue", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[IotTopicRuleErrorActionCloudwatchAlarm]:
        return typing.cast(typing.Optional[IotTopicRuleErrorActionCloudwatchAlarm], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[IotTopicRuleErrorActionCloudwatchAlarm],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b93c2a37648d2b48c416b0fa80e574e2b5286f73d054b5cf003a1225d5888f1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.iotTopicRule.IotTopicRuleErrorActionCloudwatchLogs",
    jsii_struct_bases=[],
    name_mapping={
        "log_group_name": "logGroupName",
        "role_arn": "roleArn",
        "batch_mode": "batchMode",
    },
)
class IotTopicRuleErrorActionCloudwatchLogs:
    def __init__(
        self,
        *,
        log_group_name: builtins.str,
        role_arn: builtins.str,
        batch_mode: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param log_group_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#log_group_name IotTopicRule#log_group_name}.
        :param role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#role_arn IotTopicRule#role_arn}.
        :param batch_mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#batch_mode IotTopicRule#batch_mode}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c9334e9260d7d7332c2116c48d7f4a6581536a7045f4ab5bb47a60828af1939f)
            check_type(argname="argument log_group_name", value=log_group_name, expected_type=type_hints["log_group_name"])
            check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
            check_type(argname="argument batch_mode", value=batch_mode, expected_type=type_hints["batch_mode"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "log_group_name": log_group_name,
            "role_arn": role_arn,
        }
        if batch_mode is not None:
            self._values["batch_mode"] = batch_mode

    @builtins.property
    def log_group_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#log_group_name IotTopicRule#log_group_name}.'''
        result = self._values.get("log_group_name")
        assert result is not None, "Required property 'log_group_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def role_arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#role_arn IotTopicRule#role_arn}.'''
        result = self._values.get("role_arn")
        assert result is not None, "Required property 'role_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def batch_mode(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#batch_mode IotTopicRule#batch_mode}.'''
        result = self._values.get("batch_mode")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IotTopicRuleErrorActionCloudwatchLogs(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class IotTopicRuleErrorActionCloudwatchLogsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.iotTopicRule.IotTopicRuleErrorActionCloudwatchLogsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__51819e7dc308c3409309bd6f0b96e9a7c11110825debc77653a1e74239716cc5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetBatchMode")
    def reset_batch_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBatchMode", []))

    @builtins.property
    @jsii.member(jsii_name="batchModeInput")
    def batch_mode_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "batchModeInput"))

    @builtins.property
    @jsii.member(jsii_name="logGroupNameInput")
    def log_group_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "logGroupNameInput"))

    @builtins.property
    @jsii.member(jsii_name="roleArnInput")
    def role_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "roleArnInput"))

    @builtins.property
    @jsii.member(jsii_name="batchMode")
    def batch_mode(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "batchMode"))

    @batch_mode.setter
    def batch_mode(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__00e3365bc51f589e5b59935a6ae94ea6304d0c455b691c872323d54d47fcc403)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "batchMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="logGroupName")
    def log_group_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "logGroupName"))

    @log_group_name.setter
    def log_group_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc4bbeb509bbbaf51b31d0c76e6990a1956e56b46058343294cdabf820331253)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "logGroupName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="roleArn")
    def role_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "roleArn"))

    @role_arn.setter
    def role_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fca05b519b6ba9e3f82d638875722bc68f0a964065bf8066da5a12d78fdb7362)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "roleArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[IotTopicRuleErrorActionCloudwatchLogs]:
        return typing.cast(typing.Optional[IotTopicRuleErrorActionCloudwatchLogs], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[IotTopicRuleErrorActionCloudwatchLogs],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a711555c59bfa0005145ded599cbcde28deed4ecc7b50d9ad2d206d3d064dfc6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.iotTopicRule.IotTopicRuleErrorActionCloudwatchMetric",
    jsii_struct_bases=[],
    name_mapping={
        "metric_name": "metricName",
        "metric_namespace": "metricNamespace",
        "metric_unit": "metricUnit",
        "metric_value": "metricValue",
        "role_arn": "roleArn",
        "metric_timestamp": "metricTimestamp",
    },
)
class IotTopicRuleErrorActionCloudwatchMetric:
    def __init__(
        self,
        *,
        metric_name: builtins.str,
        metric_namespace: builtins.str,
        metric_unit: builtins.str,
        metric_value: builtins.str,
        role_arn: builtins.str,
        metric_timestamp: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param metric_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#metric_name IotTopicRule#metric_name}.
        :param metric_namespace: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#metric_namespace IotTopicRule#metric_namespace}.
        :param metric_unit: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#metric_unit IotTopicRule#metric_unit}.
        :param metric_value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#metric_value IotTopicRule#metric_value}.
        :param role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#role_arn IotTopicRule#role_arn}.
        :param metric_timestamp: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#metric_timestamp IotTopicRule#metric_timestamp}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__23e4cfa1c5925f865b4f4df75c68460fcefa151d9a66c0a6d2533c4277e2d73d)
            check_type(argname="argument metric_name", value=metric_name, expected_type=type_hints["metric_name"])
            check_type(argname="argument metric_namespace", value=metric_namespace, expected_type=type_hints["metric_namespace"])
            check_type(argname="argument metric_unit", value=metric_unit, expected_type=type_hints["metric_unit"])
            check_type(argname="argument metric_value", value=metric_value, expected_type=type_hints["metric_value"])
            check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
            check_type(argname="argument metric_timestamp", value=metric_timestamp, expected_type=type_hints["metric_timestamp"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "metric_name": metric_name,
            "metric_namespace": metric_namespace,
            "metric_unit": metric_unit,
            "metric_value": metric_value,
            "role_arn": role_arn,
        }
        if metric_timestamp is not None:
            self._values["metric_timestamp"] = metric_timestamp

    @builtins.property
    def metric_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#metric_name IotTopicRule#metric_name}.'''
        result = self._values.get("metric_name")
        assert result is not None, "Required property 'metric_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def metric_namespace(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#metric_namespace IotTopicRule#metric_namespace}.'''
        result = self._values.get("metric_namespace")
        assert result is not None, "Required property 'metric_namespace' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def metric_unit(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#metric_unit IotTopicRule#metric_unit}.'''
        result = self._values.get("metric_unit")
        assert result is not None, "Required property 'metric_unit' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def metric_value(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#metric_value IotTopicRule#metric_value}.'''
        result = self._values.get("metric_value")
        assert result is not None, "Required property 'metric_value' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def role_arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#role_arn IotTopicRule#role_arn}.'''
        result = self._values.get("role_arn")
        assert result is not None, "Required property 'role_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def metric_timestamp(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#metric_timestamp IotTopicRule#metric_timestamp}.'''
        result = self._values.get("metric_timestamp")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IotTopicRuleErrorActionCloudwatchMetric(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class IotTopicRuleErrorActionCloudwatchMetricOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.iotTopicRule.IotTopicRuleErrorActionCloudwatchMetricOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fa550d0f71c63f2583b2046b9c6fbfc6c13efde3396d4695b77554bac0f137ae)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetMetricTimestamp")
    def reset_metric_timestamp(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMetricTimestamp", []))

    @builtins.property
    @jsii.member(jsii_name="metricNameInput")
    def metric_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "metricNameInput"))

    @builtins.property
    @jsii.member(jsii_name="metricNamespaceInput")
    def metric_namespace_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "metricNamespaceInput"))

    @builtins.property
    @jsii.member(jsii_name="metricTimestampInput")
    def metric_timestamp_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "metricTimestampInput"))

    @builtins.property
    @jsii.member(jsii_name="metricUnitInput")
    def metric_unit_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "metricUnitInput"))

    @builtins.property
    @jsii.member(jsii_name="metricValueInput")
    def metric_value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "metricValueInput"))

    @builtins.property
    @jsii.member(jsii_name="roleArnInput")
    def role_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "roleArnInput"))

    @builtins.property
    @jsii.member(jsii_name="metricName")
    def metric_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "metricName"))

    @metric_name.setter
    def metric_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__85d82326271b61f45ae6e06ecf762dbe1df29fd592087c5b259496de2661f796)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metricName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="metricNamespace")
    def metric_namespace(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "metricNamespace"))

    @metric_namespace.setter
    def metric_namespace(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c3a862401990990c836293e1c9f1fbad492e57fed17469043322c0d00020d88e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metricNamespace", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="metricTimestamp")
    def metric_timestamp(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "metricTimestamp"))

    @metric_timestamp.setter
    def metric_timestamp(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d358126f1dd7700012b88cc461cb52beca0a719fd7f7d7d49ee829653ba076ee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metricTimestamp", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="metricUnit")
    def metric_unit(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "metricUnit"))

    @metric_unit.setter
    def metric_unit(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__32e75bf68f51408d0a32f67f9ac6dd70e97e0603bd3edb726368dbe4b8edc8eb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metricUnit", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="metricValue")
    def metric_value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "metricValue"))

    @metric_value.setter
    def metric_value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__083fe30ccc0f64ea832a07075e6968831c3487f903b3bd7c385ed3d6bb2fa980)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metricValue", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="roleArn")
    def role_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "roleArn"))

    @role_arn.setter
    def role_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a0d6f96c5da36cbb0d84a7ab89818fd40a0525c04d263fd0a8bafc9fdcbadb37)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "roleArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[IotTopicRuleErrorActionCloudwatchMetric]:
        return typing.cast(typing.Optional[IotTopicRuleErrorActionCloudwatchMetric], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[IotTopicRuleErrorActionCloudwatchMetric],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__741329ce47b85482a09bf2df9afc6d5d27a022e8bc32e5ebd25548bf5d162a15)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.iotTopicRule.IotTopicRuleErrorActionDynamodb",
    jsii_struct_bases=[],
    name_mapping={
        "hash_key_field": "hashKeyField",
        "hash_key_value": "hashKeyValue",
        "role_arn": "roleArn",
        "table_name": "tableName",
        "hash_key_type": "hashKeyType",
        "operation": "operation",
        "payload_field": "payloadField",
        "range_key_field": "rangeKeyField",
        "range_key_type": "rangeKeyType",
        "range_key_value": "rangeKeyValue",
    },
)
class IotTopicRuleErrorActionDynamodb:
    def __init__(
        self,
        *,
        hash_key_field: builtins.str,
        hash_key_value: builtins.str,
        role_arn: builtins.str,
        table_name: builtins.str,
        hash_key_type: typing.Optional[builtins.str] = None,
        operation: typing.Optional[builtins.str] = None,
        payload_field: typing.Optional[builtins.str] = None,
        range_key_field: typing.Optional[builtins.str] = None,
        range_key_type: typing.Optional[builtins.str] = None,
        range_key_value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param hash_key_field: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#hash_key_field IotTopicRule#hash_key_field}.
        :param hash_key_value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#hash_key_value IotTopicRule#hash_key_value}.
        :param role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#role_arn IotTopicRule#role_arn}.
        :param table_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#table_name IotTopicRule#table_name}.
        :param hash_key_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#hash_key_type IotTopicRule#hash_key_type}.
        :param operation: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#operation IotTopicRule#operation}.
        :param payload_field: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#payload_field IotTopicRule#payload_field}.
        :param range_key_field: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#range_key_field IotTopicRule#range_key_field}.
        :param range_key_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#range_key_type IotTopicRule#range_key_type}.
        :param range_key_value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#range_key_value IotTopicRule#range_key_value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cdf3d6f6173501ff4e94e9a3d604d43248e8d5f0b3ef51aa7c388e9e54b2d296)
            check_type(argname="argument hash_key_field", value=hash_key_field, expected_type=type_hints["hash_key_field"])
            check_type(argname="argument hash_key_value", value=hash_key_value, expected_type=type_hints["hash_key_value"])
            check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
            check_type(argname="argument table_name", value=table_name, expected_type=type_hints["table_name"])
            check_type(argname="argument hash_key_type", value=hash_key_type, expected_type=type_hints["hash_key_type"])
            check_type(argname="argument operation", value=operation, expected_type=type_hints["operation"])
            check_type(argname="argument payload_field", value=payload_field, expected_type=type_hints["payload_field"])
            check_type(argname="argument range_key_field", value=range_key_field, expected_type=type_hints["range_key_field"])
            check_type(argname="argument range_key_type", value=range_key_type, expected_type=type_hints["range_key_type"])
            check_type(argname="argument range_key_value", value=range_key_value, expected_type=type_hints["range_key_value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "hash_key_field": hash_key_field,
            "hash_key_value": hash_key_value,
            "role_arn": role_arn,
            "table_name": table_name,
        }
        if hash_key_type is not None:
            self._values["hash_key_type"] = hash_key_type
        if operation is not None:
            self._values["operation"] = operation
        if payload_field is not None:
            self._values["payload_field"] = payload_field
        if range_key_field is not None:
            self._values["range_key_field"] = range_key_field
        if range_key_type is not None:
            self._values["range_key_type"] = range_key_type
        if range_key_value is not None:
            self._values["range_key_value"] = range_key_value

    @builtins.property
    def hash_key_field(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#hash_key_field IotTopicRule#hash_key_field}.'''
        result = self._values.get("hash_key_field")
        assert result is not None, "Required property 'hash_key_field' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def hash_key_value(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#hash_key_value IotTopicRule#hash_key_value}.'''
        result = self._values.get("hash_key_value")
        assert result is not None, "Required property 'hash_key_value' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def role_arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#role_arn IotTopicRule#role_arn}.'''
        result = self._values.get("role_arn")
        assert result is not None, "Required property 'role_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def table_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#table_name IotTopicRule#table_name}.'''
        result = self._values.get("table_name")
        assert result is not None, "Required property 'table_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def hash_key_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#hash_key_type IotTopicRule#hash_key_type}.'''
        result = self._values.get("hash_key_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def operation(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#operation IotTopicRule#operation}.'''
        result = self._values.get("operation")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def payload_field(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#payload_field IotTopicRule#payload_field}.'''
        result = self._values.get("payload_field")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def range_key_field(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#range_key_field IotTopicRule#range_key_field}.'''
        result = self._values.get("range_key_field")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def range_key_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#range_key_type IotTopicRule#range_key_type}.'''
        result = self._values.get("range_key_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def range_key_value(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#range_key_value IotTopicRule#range_key_value}.'''
        result = self._values.get("range_key_value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IotTopicRuleErrorActionDynamodb(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class IotTopicRuleErrorActionDynamodbOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.iotTopicRule.IotTopicRuleErrorActionDynamodbOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a876b7f79fbb4f67156b714e75be69845f8c71ba7abfed56c274d5bf854a7f76)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetHashKeyType")
    def reset_hash_key_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHashKeyType", []))

    @jsii.member(jsii_name="resetOperation")
    def reset_operation(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOperation", []))

    @jsii.member(jsii_name="resetPayloadField")
    def reset_payload_field(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPayloadField", []))

    @jsii.member(jsii_name="resetRangeKeyField")
    def reset_range_key_field(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRangeKeyField", []))

    @jsii.member(jsii_name="resetRangeKeyType")
    def reset_range_key_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRangeKeyType", []))

    @jsii.member(jsii_name="resetRangeKeyValue")
    def reset_range_key_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRangeKeyValue", []))

    @builtins.property
    @jsii.member(jsii_name="hashKeyFieldInput")
    def hash_key_field_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "hashKeyFieldInput"))

    @builtins.property
    @jsii.member(jsii_name="hashKeyTypeInput")
    def hash_key_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "hashKeyTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="hashKeyValueInput")
    def hash_key_value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "hashKeyValueInput"))

    @builtins.property
    @jsii.member(jsii_name="operationInput")
    def operation_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "operationInput"))

    @builtins.property
    @jsii.member(jsii_name="payloadFieldInput")
    def payload_field_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "payloadFieldInput"))

    @builtins.property
    @jsii.member(jsii_name="rangeKeyFieldInput")
    def range_key_field_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "rangeKeyFieldInput"))

    @builtins.property
    @jsii.member(jsii_name="rangeKeyTypeInput")
    def range_key_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "rangeKeyTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="rangeKeyValueInput")
    def range_key_value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "rangeKeyValueInput"))

    @builtins.property
    @jsii.member(jsii_name="roleArnInput")
    def role_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "roleArnInput"))

    @builtins.property
    @jsii.member(jsii_name="tableNameInput")
    def table_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tableNameInput"))

    @builtins.property
    @jsii.member(jsii_name="hashKeyField")
    def hash_key_field(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "hashKeyField"))

    @hash_key_field.setter
    def hash_key_field(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__53bb332ee999c81902a3b96aa24d51192fefe8e8ad812ae8d95ac41d903c7bf5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hashKeyField", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="hashKeyType")
    def hash_key_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "hashKeyType"))

    @hash_key_type.setter
    def hash_key_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f757a385613356d1cf129adb44a15cf4927b6e6c2f1396df6cc12996741f8924)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hashKeyType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="hashKeyValue")
    def hash_key_value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "hashKeyValue"))

    @hash_key_value.setter
    def hash_key_value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__847b182e6c33d6d02c3e9467b304a22c63c5ffac9945de64f36b70dc7d94a11c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hashKeyValue", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="operation")
    def operation(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "operation"))

    @operation.setter
    def operation(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c2f32b06c06cdf0ea35e8afc1be9d76afedfbd0e86ee51688cdb33cccddcc5ed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "operation", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="payloadField")
    def payload_field(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "payloadField"))

    @payload_field.setter
    def payload_field(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__09eaf2d1d46fddb2be567ecf1ae4881d18e1c7c22261c7d93f86067fb7e63679)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "payloadField", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="rangeKeyField")
    def range_key_field(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "rangeKeyField"))

    @range_key_field.setter
    def range_key_field(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__53f4f127ee8458894713a73b578bb9536aad40cdb80a165e6c1581ed7e5dd0ad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rangeKeyField", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="rangeKeyType")
    def range_key_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "rangeKeyType"))

    @range_key_type.setter
    def range_key_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d553d9593a49a96c6433541627c3e50321672dbc663d0faf01d2ca8bb73be40f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rangeKeyType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="rangeKeyValue")
    def range_key_value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "rangeKeyValue"))

    @range_key_value.setter
    def range_key_value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1ef41dda0e872881bc65602419b49f79d5292042f5dda613b0f26d5e47faae4c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rangeKeyValue", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="roleArn")
    def role_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "roleArn"))

    @role_arn.setter
    def role_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__264c6c07fb8ea8fd7ebc88a86d9ce82addfef9f15aa7c014cdb5ae5affed769e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "roleArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tableName")
    def table_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tableName"))

    @table_name.setter
    def table_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f3e59c0b0a398eed2467df16e4e8766ee60e7e8cf585b87aedba63cc77bac6f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tableName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[IotTopicRuleErrorActionDynamodb]:
        return typing.cast(typing.Optional[IotTopicRuleErrorActionDynamodb], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[IotTopicRuleErrorActionDynamodb],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8de412efbaa91eb54b4617199ebcaec34561804f1852fc5d7fa83b2e6c1600ea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.iotTopicRule.IotTopicRuleErrorActionDynamodbv2",
    jsii_struct_bases=[],
    name_mapping={"role_arn": "roleArn", "put_item": "putItem"},
)
class IotTopicRuleErrorActionDynamodbv2:
    def __init__(
        self,
        *,
        role_arn: builtins.str,
        put_item: typing.Optional[typing.Union["IotTopicRuleErrorActionDynamodbv2PutItem", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#role_arn IotTopicRule#role_arn}.
        :param put_item: put_item block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#put_item IotTopicRule#put_item}
        '''
        if isinstance(put_item, dict):
            put_item = IotTopicRuleErrorActionDynamodbv2PutItem(**put_item)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bc12c12a46fa57c8a98f9c12ff52a529bb4c861b0c9df1798b049102a9137028)
            check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
            check_type(argname="argument put_item", value=put_item, expected_type=type_hints["put_item"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "role_arn": role_arn,
        }
        if put_item is not None:
            self._values["put_item"] = put_item

    @builtins.property
    def role_arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#role_arn IotTopicRule#role_arn}.'''
        result = self._values.get("role_arn")
        assert result is not None, "Required property 'role_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def put_item(self) -> typing.Optional["IotTopicRuleErrorActionDynamodbv2PutItem"]:
        '''put_item block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#put_item IotTopicRule#put_item}
        '''
        result = self._values.get("put_item")
        return typing.cast(typing.Optional["IotTopicRuleErrorActionDynamodbv2PutItem"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IotTopicRuleErrorActionDynamodbv2(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class IotTopicRuleErrorActionDynamodbv2OutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.iotTopicRule.IotTopicRuleErrorActionDynamodbv2OutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c9ecdcd50884fe336b3f08e41d4e6ba409bb5207d0a3aa771ee09fc5ba9e5a51)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putPutItem")
    def put_put_item(self, *, table_name: builtins.str) -> None:
        '''
        :param table_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#table_name IotTopicRule#table_name}.
        '''
        value = IotTopicRuleErrorActionDynamodbv2PutItem(table_name=table_name)

        return typing.cast(None, jsii.invoke(self, "putPutItem", [value]))

    @jsii.member(jsii_name="resetPutItem")
    def reset_put_item(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPutItem", []))

    @builtins.property
    @jsii.member(jsii_name="putItem")
    def put_item(self) -> "IotTopicRuleErrorActionDynamodbv2PutItemOutputReference":
        return typing.cast("IotTopicRuleErrorActionDynamodbv2PutItemOutputReference", jsii.get(self, "putItem"))

    @builtins.property
    @jsii.member(jsii_name="putItemInput")
    def put_item_input(
        self,
    ) -> typing.Optional["IotTopicRuleErrorActionDynamodbv2PutItem"]:
        return typing.cast(typing.Optional["IotTopicRuleErrorActionDynamodbv2PutItem"], jsii.get(self, "putItemInput"))

    @builtins.property
    @jsii.member(jsii_name="roleArnInput")
    def role_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "roleArnInput"))

    @builtins.property
    @jsii.member(jsii_name="roleArn")
    def role_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "roleArn"))

    @role_arn.setter
    def role_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__067e66649898bcb3163b191bb64bd0e5f31f9f70ea845d6c2d2bb23385dc7d75)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "roleArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[IotTopicRuleErrorActionDynamodbv2]:
        return typing.cast(typing.Optional[IotTopicRuleErrorActionDynamodbv2], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[IotTopicRuleErrorActionDynamodbv2],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7ce212cdd6b794ef4df836e5a3b710109f9408a56793e4515fea4f7581e1b2d7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.iotTopicRule.IotTopicRuleErrorActionDynamodbv2PutItem",
    jsii_struct_bases=[],
    name_mapping={"table_name": "tableName"},
)
class IotTopicRuleErrorActionDynamodbv2PutItem:
    def __init__(self, *, table_name: builtins.str) -> None:
        '''
        :param table_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#table_name IotTopicRule#table_name}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5cf7b3aa537109d156f8a80480362954f4bda9e7068113c0d72dc0954fe0d393)
            check_type(argname="argument table_name", value=table_name, expected_type=type_hints["table_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "table_name": table_name,
        }

    @builtins.property
    def table_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#table_name IotTopicRule#table_name}.'''
        result = self._values.get("table_name")
        assert result is not None, "Required property 'table_name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IotTopicRuleErrorActionDynamodbv2PutItem(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class IotTopicRuleErrorActionDynamodbv2PutItemOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.iotTopicRule.IotTopicRuleErrorActionDynamodbv2PutItemOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6a9ef8321c527358823fee37c908b1ca0e1dd02b15cedb47525ae57a2cd83ca5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="tableNameInput")
    def table_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tableNameInput"))

    @builtins.property
    @jsii.member(jsii_name="tableName")
    def table_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tableName"))

    @table_name.setter
    def table_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee9c0076ed7be13baef6d2fd29afb0e24178f36df3a22617bc940a23f0c863d7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tableName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[IotTopicRuleErrorActionDynamodbv2PutItem]:
        return typing.cast(typing.Optional[IotTopicRuleErrorActionDynamodbv2PutItem], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[IotTopicRuleErrorActionDynamodbv2PutItem],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ca66137312c4f5ed6af41b8382348ea1888be5a30b285d2876507a10ef70595d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.iotTopicRule.IotTopicRuleErrorActionElasticsearch",
    jsii_struct_bases=[],
    name_mapping={
        "endpoint": "endpoint",
        "id": "id",
        "index": "index",
        "role_arn": "roleArn",
        "type": "type",
    },
)
class IotTopicRuleErrorActionElasticsearch:
    def __init__(
        self,
        *,
        endpoint: builtins.str,
        id: builtins.str,
        index: builtins.str,
        role_arn: builtins.str,
        type: builtins.str,
    ) -> None:
        '''
        :param endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#endpoint IotTopicRule#endpoint}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#id IotTopicRule#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param index: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#index IotTopicRule#index}.
        :param role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#role_arn IotTopicRule#role_arn}.
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#type IotTopicRule#type}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__840e7c6d0056e32d130c885aefc1eb19eeaa9f3dcb701b03b74c38bbc4e5244d)
            check_type(argname="argument endpoint", value=endpoint, expected_type=type_hints["endpoint"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
            check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "endpoint": endpoint,
            "id": id,
            "index": index,
            "role_arn": role_arn,
            "type": type,
        }

    @builtins.property
    def endpoint(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#endpoint IotTopicRule#endpoint}.'''
        result = self._values.get("endpoint")
        assert result is not None, "Required property 'endpoint' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#id IotTopicRule#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        assert result is not None, "Required property 'id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def index(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#index IotTopicRule#index}.'''
        result = self._values.get("index")
        assert result is not None, "Required property 'index' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def role_arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#role_arn IotTopicRule#role_arn}.'''
        result = self._values.get("role_arn")
        assert result is not None, "Required property 'role_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#type IotTopicRule#type}.'''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IotTopicRuleErrorActionElasticsearch(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class IotTopicRuleErrorActionElasticsearchOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.iotTopicRule.IotTopicRuleErrorActionElasticsearchOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7ee7f10284f6d654649d6d0cc79b7e647601147c5dd60a0ee532d6dd5e18efb1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="endpointInput")
    def endpoint_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "endpointInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="indexInput")
    def index_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "indexInput"))

    @builtins.property
    @jsii.member(jsii_name="roleArnInput")
    def role_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "roleArnInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="endpoint")
    def endpoint(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "endpoint"))

    @endpoint.setter
    def endpoint(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac99f1346fd034b98c4456cad868bc9ccc7f3dbfc7b7539a074a5c8bc4fd2143)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "endpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f707d0b3b5545d91ebf926e89cd1636bc499fe4058c0fe5f245e2d3ced88e3ba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="index")
    def index(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "index"))

    @index.setter
    def index(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__64e7c931c4c7aef7f694290d296760fd66f91b1f482f5325769ee59e6ac3c2ef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "index", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="roleArn")
    def role_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "roleArn"))

    @role_arn.setter
    def role_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dca9ac62731d8547b624887442ace081b64a1252cb971b5fe0d72065dd7503e9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "roleArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bd0f646bda18e32a3c70115891fdef7f258fda96d9d7e1de2ea5193ce24838ef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[IotTopicRuleErrorActionElasticsearch]:
        return typing.cast(typing.Optional[IotTopicRuleErrorActionElasticsearch], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[IotTopicRuleErrorActionElasticsearch],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__01dc5bfcea5ed57da0cfcba498c80f3b669705fa6b954ffd021121d3b6f55d00)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.iotTopicRule.IotTopicRuleErrorActionFirehose",
    jsii_struct_bases=[],
    name_mapping={
        "delivery_stream_name": "deliveryStreamName",
        "role_arn": "roleArn",
        "batch_mode": "batchMode",
        "separator": "separator",
    },
)
class IotTopicRuleErrorActionFirehose:
    def __init__(
        self,
        *,
        delivery_stream_name: builtins.str,
        role_arn: builtins.str,
        batch_mode: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        separator: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param delivery_stream_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#delivery_stream_name IotTopicRule#delivery_stream_name}.
        :param role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#role_arn IotTopicRule#role_arn}.
        :param batch_mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#batch_mode IotTopicRule#batch_mode}.
        :param separator: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#separator IotTopicRule#separator}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__330b61a74f2a390ab516ce7f6fe6e676a44f00449479e4289c91d7443e406175)
            check_type(argname="argument delivery_stream_name", value=delivery_stream_name, expected_type=type_hints["delivery_stream_name"])
            check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
            check_type(argname="argument batch_mode", value=batch_mode, expected_type=type_hints["batch_mode"])
            check_type(argname="argument separator", value=separator, expected_type=type_hints["separator"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "delivery_stream_name": delivery_stream_name,
            "role_arn": role_arn,
        }
        if batch_mode is not None:
            self._values["batch_mode"] = batch_mode
        if separator is not None:
            self._values["separator"] = separator

    @builtins.property
    def delivery_stream_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#delivery_stream_name IotTopicRule#delivery_stream_name}.'''
        result = self._values.get("delivery_stream_name")
        assert result is not None, "Required property 'delivery_stream_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def role_arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#role_arn IotTopicRule#role_arn}.'''
        result = self._values.get("role_arn")
        assert result is not None, "Required property 'role_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def batch_mode(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#batch_mode IotTopicRule#batch_mode}.'''
        result = self._values.get("batch_mode")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def separator(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#separator IotTopicRule#separator}.'''
        result = self._values.get("separator")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IotTopicRuleErrorActionFirehose(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class IotTopicRuleErrorActionFirehoseOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.iotTopicRule.IotTopicRuleErrorActionFirehoseOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bac4fd12347d48674446165032b6e41c5d2fce4bc064eef9b2d00d89e9dc8353)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetBatchMode")
    def reset_batch_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBatchMode", []))

    @jsii.member(jsii_name="resetSeparator")
    def reset_separator(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSeparator", []))

    @builtins.property
    @jsii.member(jsii_name="batchModeInput")
    def batch_mode_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "batchModeInput"))

    @builtins.property
    @jsii.member(jsii_name="deliveryStreamNameInput")
    def delivery_stream_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "deliveryStreamNameInput"))

    @builtins.property
    @jsii.member(jsii_name="roleArnInput")
    def role_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "roleArnInput"))

    @builtins.property
    @jsii.member(jsii_name="separatorInput")
    def separator_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "separatorInput"))

    @builtins.property
    @jsii.member(jsii_name="batchMode")
    def batch_mode(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "batchMode"))

    @batch_mode.setter
    def batch_mode(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a4f1ec22843866bb33374196efadeb23f255ea1dea7db2e2ac8ac2e0adb0556b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "batchMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="deliveryStreamName")
    def delivery_stream_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "deliveryStreamName"))

    @delivery_stream_name.setter
    def delivery_stream_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e2e638f9698ff2c3a786e8ffa340a876ce8c32e090b0d03ce2a1de67ea1a6cf6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deliveryStreamName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="roleArn")
    def role_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "roleArn"))

    @role_arn.setter
    def role_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9949d27419ad2b4f515beb326698dd164ee48b3f42da4cb65b3d4dacc94d67a9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "roleArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="separator")
    def separator(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "separator"))

    @separator.setter
    def separator(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__05920209c1643ce0378c5a78fe4dffba4db6fcf879f59a7343c17d41bb9c7fe3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "separator", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[IotTopicRuleErrorActionFirehose]:
        return typing.cast(typing.Optional[IotTopicRuleErrorActionFirehose], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[IotTopicRuleErrorActionFirehose],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f91f8e81734ab2c27a3f912d183c6fbecabe445fed35030ccabf8f7dd13abd16)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.iotTopicRule.IotTopicRuleErrorActionHttp",
    jsii_struct_bases=[],
    name_mapping={
        "url": "url",
        "confirmation_url": "confirmationUrl",
        "http_header": "httpHeader",
    },
)
class IotTopicRuleErrorActionHttp:
    def __init__(
        self,
        *,
        url: builtins.str,
        confirmation_url: typing.Optional[builtins.str] = None,
        http_header: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["IotTopicRuleErrorActionHttpHttpHeader", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param url: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#url IotTopicRule#url}.
        :param confirmation_url: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#confirmation_url IotTopicRule#confirmation_url}.
        :param http_header: http_header block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#http_header IotTopicRule#http_header}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f7cf00ed0a952fc9c6bd8b7615dbb7caac01e185fdbb15e4c5d732ab62479081)
            check_type(argname="argument url", value=url, expected_type=type_hints["url"])
            check_type(argname="argument confirmation_url", value=confirmation_url, expected_type=type_hints["confirmation_url"])
            check_type(argname="argument http_header", value=http_header, expected_type=type_hints["http_header"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "url": url,
        }
        if confirmation_url is not None:
            self._values["confirmation_url"] = confirmation_url
        if http_header is not None:
            self._values["http_header"] = http_header

    @builtins.property
    def url(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#url IotTopicRule#url}.'''
        result = self._values.get("url")
        assert result is not None, "Required property 'url' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def confirmation_url(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#confirmation_url IotTopicRule#confirmation_url}.'''
        result = self._values.get("confirmation_url")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def http_header(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["IotTopicRuleErrorActionHttpHttpHeader"]]]:
        '''http_header block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#http_header IotTopicRule#http_header}
        '''
        result = self._values.get("http_header")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["IotTopicRuleErrorActionHttpHttpHeader"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IotTopicRuleErrorActionHttp(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.iotTopicRule.IotTopicRuleErrorActionHttpHttpHeader",
    jsii_struct_bases=[],
    name_mapping={"key": "key", "value": "value"},
)
class IotTopicRuleErrorActionHttpHttpHeader:
    def __init__(self, *, key: builtins.str, value: builtins.str) -> None:
        '''
        :param key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#key IotTopicRule#key}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#value IotTopicRule#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__44d35616c84712d38a443b1901dac1eeb179abc30116edbf10555660b974d7a0)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "key": key,
            "value": value,
        }

    @builtins.property
    def key(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#key IotTopicRule#key}.'''
        result = self._values.get("key")
        assert result is not None, "Required property 'key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#value IotTopicRule#value}.'''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IotTopicRuleErrorActionHttpHttpHeader(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class IotTopicRuleErrorActionHttpHttpHeaderList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.iotTopicRule.IotTopicRuleErrorActionHttpHttpHeaderList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__aba04ef60ba918cd0f507ec75ad85f32b72fb0588b0b9d2b2bc86a960e84cd79)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "IotTopicRuleErrorActionHttpHttpHeaderOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9353daa3e851582c94affbf67f11906b604adc1c35f02b78f7ed4183e7b5f364)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("IotTopicRuleErrorActionHttpHttpHeaderOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0336bb57332c077439a6419e78d26eaacbfacc7d34e61daac13b22eaf42d1d0a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__56a8c7401c0cc9e0005994ebc0b2941011827d2dc027d31330997bb35a9059ab)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1a910d7d8e57ab407fc9711fd1188480b8c12fbf3879db43f5f8dbb138675ee8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotTopicRuleErrorActionHttpHttpHeader]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotTopicRuleErrorActionHttpHttpHeader]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotTopicRuleErrorActionHttpHttpHeader]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f4440af0a0a25a2da58dff03658b6ef7dda4dc36c4e212e3e2429e47b4aa8adc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class IotTopicRuleErrorActionHttpHttpHeaderOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.iotTopicRule.IotTopicRuleErrorActionHttpHttpHeaderOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ff232d7eb13cc70c62b509c3a622264271c115ae9f7b0ad235d95cf95ce31c0b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="keyInput")
    def key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "key"))

    @key.setter
    def key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ceac0f8aec76fdab40e57ce93a584f8b97a22d4302eb4cc76618daae24337b9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__52430a1f50309c5b31e6dd385f0851b17b06544494b02e69f87c0858e900a995)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IotTopicRuleErrorActionHttpHttpHeader]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IotTopicRuleErrorActionHttpHttpHeader]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IotTopicRuleErrorActionHttpHttpHeader]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d503da18c765d45d9913cd81384fd7fee26415477dab310d0ac6c4d6286453ee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class IotTopicRuleErrorActionHttpOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.iotTopicRule.IotTopicRuleErrorActionHttpOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0262b928090da9cf00d9146c107ba18ce8d5fc5a1713e12a78734295b470088b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putHttpHeader")
    def put_http_header(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[IotTopicRuleErrorActionHttpHttpHeader, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ea656763299d21f11a78a78969ffeef2007e8a85fe8aa61aa2e7ad1fc1ed7a73)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putHttpHeader", [value]))

    @jsii.member(jsii_name="resetConfirmationUrl")
    def reset_confirmation_url(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConfirmationUrl", []))

    @jsii.member(jsii_name="resetHttpHeader")
    def reset_http_header(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHttpHeader", []))

    @builtins.property
    @jsii.member(jsii_name="httpHeader")
    def http_header(self) -> IotTopicRuleErrorActionHttpHttpHeaderList:
        return typing.cast(IotTopicRuleErrorActionHttpHttpHeaderList, jsii.get(self, "httpHeader"))

    @builtins.property
    @jsii.member(jsii_name="confirmationUrlInput")
    def confirmation_url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "confirmationUrlInput"))

    @builtins.property
    @jsii.member(jsii_name="httpHeaderInput")
    def http_header_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotTopicRuleErrorActionHttpHttpHeader]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotTopicRuleErrorActionHttpHttpHeader]]], jsii.get(self, "httpHeaderInput"))

    @builtins.property
    @jsii.member(jsii_name="urlInput")
    def url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "urlInput"))

    @builtins.property
    @jsii.member(jsii_name="confirmationUrl")
    def confirmation_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "confirmationUrl"))

    @confirmation_url.setter
    def confirmation_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c0c8f7ec397887061bc35c7e6ad2fe447f790d4cb87f0bd240c072d582b538d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "confirmationUrl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="url")
    def url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "url"))

    @url.setter
    def url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__75541107967f66eba2b35367750afd8dd36acc9a8cc854e5e03075fd7b7f0429)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "url", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[IotTopicRuleErrorActionHttp]:
        return typing.cast(typing.Optional[IotTopicRuleErrorActionHttp], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[IotTopicRuleErrorActionHttp],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__38047dc630dfa2b033641e2acb51678e3dafbfc16b920fa3e08844c4ab733a11)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.iotTopicRule.IotTopicRuleErrorActionIotAnalytics",
    jsii_struct_bases=[],
    name_mapping={
        "channel_name": "channelName",
        "role_arn": "roleArn",
        "batch_mode": "batchMode",
    },
)
class IotTopicRuleErrorActionIotAnalytics:
    def __init__(
        self,
        *,
        channel_name: builtins.str,
        role_arn: builtins.str,
        batch_mode: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param channel_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#channel_name IotTopicRule#channel_name}.
        :param role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#role_arn IotTopicRule#role_arn}.
        :param batch_mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#batch_mode IotTopicRule#batch_mode}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e9265a72e9cbfbfac33a1e39f761d7181a3938385cb6b7a13a7d25b098b86aa)
            check_type(argname="argument channel_name", value=channel_name, expected_type=type_hints["channel_name"])
            check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
            check_type(argname="argument batch_mode", value=batch_mode, expected_type=type_hints["batch_mode"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "channel_name": channel_name,
            "role_arn": role_arn,
        }
        if batch_mode is not None:
            self._values["batch_mode"] = batch_mode

    @builtins.property
    def channel_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#channel_name IotTopicRule#channel_name}.'''
        result = self._values.get("channel_name")
        assert result is not None, "Required property 'channel_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def role_arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#role_arn IotTopicRule#role_arn}.'''
        result = self._values.get("role_arn")
        assert result is not None, "Required property 'role_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def batch_mode(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#batch_mode IotTopicRule#batch_mode}.'''
        result = self._values.get("batch_mode")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IotTopicRuleErrorActionIotAnalytics(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class IotTopicRuleErrorActionIotAnalyticsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.iotTopicRule.IotTopicRuleErrorActionIotAnalyticsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f2dd74647d63223c836410d85a63b728456b550bb3c62bea1e6ea9ce496115d4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetBatchMode")
    def reset_batch_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBatchMode", []))

    @builtins.property
    @jsii.member(jsii_name="batchModeInput")
    def batch_mode_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "batchModeInput"))

    @builtins.property
    @jsii.member(jsii_name="channelNameInput")
    def channel_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "channelNameInput"))

    @builtins.property
    @jsii.member(jsii_name="roleArnInput")
    def role_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "roleArnInput"))

    @builtins.property
    @jsii.member(jsii_name="batchMode")
    def batch_mode(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "batchMode"))

    @batch_mode.setter
    def batch_mode(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1a6e7575cee1ee38fbb17507df4bbca66d4dc2a6108ab04e8dcfeb265d64ce6c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "batchMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="channelName")
    def channel_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "channelName"))

    @channel_name.setter
    def channel_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__819cd865a52fd8bb251e8776ffa37248aae0bc2e97dcf53de31997541168e56d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "channelName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="roleArn")
    def role_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "roleArn"))

    @role_arn.setter
    def role_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__35af257378fac8e3498c3ba8b0415aecfd7712ce75cac4fdaaa8fc14d616e774)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "roleArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[IotTopicRuleErrorActionIotAnalytics]:
        return typing.cast(typing.Optional[IotTopicRuleErrorActionIotAnalytics], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[IotTopicRuleErrorActionIotAnalytics],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d43bc97d6961cc319eb3961eb59b56396d3d90d286bf6639da28055b461c79e3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.iotTopicRule.IotTopicRuleErrorActionIotEvents",
    jsii_struct_bases=[],
    name_mapping={
        "input_name": "inputName",
        "role_arn": "roleArn",
        "batch_mode": "batchMode",
        "message_id": "messageId",
    },
)
class IotTopicRuleErrorActionIotEvents:
    def __init__(
        self,
        *,
        input_name: builtins.str,
        role_arn: builtins.str,
        batch_mode: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        message_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param input_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#input_name IotTopicRule#input_name}.
        :param role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#role_arn IotTopicRule#role_arn}.
        :param batch_mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#batch_mode IotTopicRule#batch_mode}.
        :param message_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#message_id IotTopicRule#message_id}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2cfc6f618fa93430480b67fb7522d955976525d5b665f6060b985654a7b77d14)
            check_type(argname="argument input_name", value=input_name, expected_type=type_hints["input_name"])
            check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
            check_type(argname="argument batch_mode", value=batch_mode, expected_type=type_hints["batch_mode"])
            check_type(argname="argument message_id", value=message_id, expected_type=type_hints["message_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "input_name": input_name,
            "role_arn": role_arn,
        }
        if batch_mode is not None:
            self._values["batch_mode"] = batch_mode
        if message_id is not None:
            self._values["message_id"] = message_id

    @builtins.property
    def input_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#input_name IotTopicRule#input_name}.'''
        result = self._values.get("input_name")
        assert result is not None, "Required property 'input_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def role_arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#role_arn IotTopicRule#role_arn}.'''
        result = self._values.get("role_arn")
        assert result is not None, "Required property 'role_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def batch_mode(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#batch_mode IotTopicRule#batch_mode}.'''
        result = self._values.get("batch_mode")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def message_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#message_id IotTopicRule#message_id}.'''
        result = self._values.get("message_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IotTopicRuleErrorActionIotEvents(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class IotTopicRuleErrorActionIotEventsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.iotTopicRule.IotTopicRuleErrorActionIotEventsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__26c2ab1fb4295f218b110c95c790d234824a616ba0dc6200e5190f3e9399969d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetBatchMode")
    def reset_batch_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBatchMode", []))

    @jsii.member(jsii_name="resetMessageId")
    def reset_message_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMessageId", []))

    @builtins.property
    @jsii.member(jsii_name="batchModeInput")
    def batch_mode_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "batchModeInput"))

    @builtins.property
    @jsii.member(jsii_name="inputNameInput")
    def input_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "inputNameInput"))

    @builtins.property
    @jsii.member(jsii_name="messageIdInput")
    def message_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "messageIdInput"))

    @builtins.property
    @jsii.member(jsii_name="roleArnInput")
    def role_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "roleArnInput"))

    @builtins.property
    @jsii.member(jsii_name="batchMode")
    def batch_mode(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "batchMode"))

    @batch_mode.setter
    def batch_mode(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__67a7a3c26680c34c13035abfd20f7fffeabe71f508dfb56760ed82e4e7d3fbbf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "batchMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="inputName")
    def input_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "inputName"))

    @input_name.setter
    def input_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd9140956fa786db48e1245a8c5ecd1956f7da7938f078541b2bc0fc663bdc6d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "inputName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="messageId")
    def message_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "messageId"))

    @message_id.setter
    def message_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eedc4d31f78c95edb8e412280d1fb91bf9ebd8655faaf0283c0cfde2c9da52eb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "messageId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="roleArn")
    def role_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "roleArn"))

    @role_arn.setter
    def role_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b0c1f50a92ddda07e5e5484ca8a4a3de4fbb2864fe33a94cb9271d7a8dab62af)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "roleArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[IotTopicRuleErrorActionIotEvents]:
        return typing.cast(typing.Optional[IotTopicRuleErrorActionIotEvents], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[IotTopicRuleErrorActionIotEvents],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a6a7dfeeb26cb62b01da990feff88bb2c28530c9dd13fb34f403513c7e51a845)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.iotTopicRule.IotTopicRuleErrorActionKafka",
    jsii_struct_bases=[],
    name_mapping={
        "client_properties": "clientProperties",
        "destination_arn": "destinationArn",
        "topic": "topic",
        "header": "header",
        "key": "key",
        "partition": "partition",
    },
)
class IotTopicRuleErrorActionKafka:
    def __init__(
        self,
        *,
        client_properties: typing.Mapping[builtins.str, builtins.str],
        destination_arn: builtins.str,
        topic: builtins.str,
        header: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["IotTopicRuleErrorActionKafkaHeader", typing.Dict[builtins.str, typing.Any]]]]] = None,
        key: typing.Optional[builtins.str] = None,
        partition: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param client_properties: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#client_properties IotTopicRule#client_properties}.
        :param destination_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#destination_arn IotTopicRule#destination_arn}.
        :param topic: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#topic IotTopicRule#topic}.
        :param header: header block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#header IotTopicRule#header}
        :param key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#key IotTopicRule#key}.
        :param partition: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#partition IotTopicRule#partition}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f4d7669d7e9eaa125ac1da6332267c0f14a7804d9bd87579c95beae05aee1aea)
            check_type(argname="argument client_properties", value=client_properties, expected_type=type_hints["client_properties"])
            check_type(argname="argument destination_arn", value=destination_arn, expected_type=type_hints["destination_arn"])
            check_type(argname="argument topic", value=topic, expected_type=type_hints["topic"])
            check_type(argname="argument header", value=header, expected_type=type_hints["header"])
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument partition", value=partition, expected_type=type_hints["partition"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "client_properties": client_properties,
            "destination_arn": destination_arn,
            "topic": topic,
        }
        if header is not None:
            self._values["header"] = header
        if key is not None:
            self._values["key"] = key
        if partition is not None:
            self._values["partition"] = partition

    @builtins.property
    def client_properties(self) -> typing.Mapping[builtins.str, builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#client_properties IotTopicRule#client_properties}.'''
        result = self._values.get("client_properties")
        assert result is not None, "Required property 'client_properties' is missing"
        return typing.cast(typing.Mapping[builtins.str, builtins.str], result)

    @builtins.property
    def destination_arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#destination_arn IotTopicRule#destination_arn}.'''
        result = self._values.get("destination_arn")
        assert result is not None, "Required property 'destination_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def topic(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#topic IotTopicRule#topic}.'''
        result = self._values.get("topic")
        assert result is not None, "Required property 'topic' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def header(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["IotTopicRuleErrorActionKafkaHeader"]]]:
        '''header block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#header IotTopicRule#header}
        '''
        result = self._values.get("header")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["IotTopicRuleErrorActionKafkaHeader"]]], result)

    @builtins.property
    def key(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#key IotTopicRule#key}.'''
        result = self._values.get("key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def partition(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#partition IotTopicRule#partition}.'''
        result = self._values.get("partition")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IotTopicRuleErrorActionKafka(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.iotTopicRule.IotTopicRuleErrorActionKafkaHeader",
    jsii_struct_bases=[],
    name_mapping={"key": "key", "value": "value"},
)
class IotTopicRuleErrorActionKafkaHeader:
    def __init__(self, *, key: builtins.str, value: builtins.str) -> None:
        '''
        :param key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#key IotTopicRule#key}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#value IotTopicRule#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f3e01acf4398c7e499a6ab467b595c0a4e6c58a6ab8309a69eb996b12e8888f)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "key": key,
            "value": value,
        }

    @builtins.property
    def key(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#key IotTopicRule#key}.'''
        result = self._values.get("key")
        assert result is not None, "Required property 'key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#value IotTopicRule#value}.'''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IotTopicRuleErrorActionKafkaHeader(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class IotTopicRuleErrorActionKafkaHeaderList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.iotTopicRule.IotTopicRuleErrorActionKafkaHeaderList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8fbdb671bf8a4c05812ff6a7296ec8616d1e1ddefe2323748a7285e0f851d907)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "IotTopicRuleErrorActionKafkaHeaderOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__de55a6761d5410cc9f46fb417237b021f1b202971ed82a614fd4788dd62a0e48)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("IotTopicRuleErrorActionKafkaHeaderOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__adafaec1c36591fea4a81c1bfa928f4878db834aae65c063462ec322ddfbb516)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8f5f651c997e4c16d582aa28610a7a72bf99bb9bf022ceec5e264bc12bfae113)
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
            type_hints = typing.get_type_hints(_typecheckingstub__41c9ebadc8017176aa1ce66e9d34158190a69d967383e23523bd312c60cbe8e7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotTopicRuleErrorActionKafkaHeader]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotTopicRuleErrorActionKafkaHeader]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotTopicRuleErrorActionKafkaHeader]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__061e3772059f4fd8a37182390e4dd7505c42a59b7118fb5f5e9ab535fa31d2ad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class IotTopicRuleErrorActionKafkaHeaderOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.iotTopicRule.IotTopicRuleErrorActionKafkaHeaderOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__74e1ac3c85d1fd687a7ba383dad3379078fff418c6bcc48391e2964abb40ac90)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="keyInput")
    def key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "key"))

    @key.setter
    def key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1a847b4706f93afda1b0d87d5d5d3dfd7929b837df1f9de5e00be1a8fbaecadb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b8d1674b53fe03c4dfcd41bf42f03edd8398db98ab8a005d18ed56f666b8f402)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IotTopicRuleErrorActionKafkaHeader]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IotTopicRuleErrorActionKafkaHeader]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IotTopicRuleErrorActionKafkaHeader]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__89bae9fb1978d79cdb7abffc04fa396bce09c87ac4009ff862401fcfe375b879)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class IotTopicRuleErrorActionKafkaOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.iotTopicRule.IotTopicRuleErrorActionKafkaOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8031c1c9439d79f97f3e5a02597f113c1c0df16969de90cf33e7666d8f3ab915)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putHeader")
    def put_header(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[IotTopicRuleErrorActionKafkaHeader, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c024281db7dddf6b1220a9d96ece3107f55cc706c714d194101fd73a7da9056)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putHeader", [value]))

    @jsii.member(jsii_name="resetHeader")
    def reset_header(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHeader", []))

    @jsii.member(jsii_name="resetKey")
    def reset_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKey", []))

    @jsii.member(jsii_name="resetPartition")
    def reset_partition(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPartition", []))

    @builtins.property
    @jsii.member(jsii_name="header")
    def header(self) -> IotTopicRuleErrorActionKafkaHeaderList:
        return typing.cast(IotTopicRuleErrorActionKafkaHeaderList, jsii.get(self, "header"))

    @builtins.property
    @jsii.member(jsii_name="clientPropertiesInput")
    def client_properties_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "clientPropertiesInput"))

    @builtins.property
    @jsii.member(jsii_name="destinationArnInput")
    def destination_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "destinationArnInput"))

    @builtins.property
    @jsii.member(jsii_name="headerInput")
    def header_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotTopicRuleErrorActionKafkaHeader]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotTopicRuleErrorActionKafkaHeader]]], jsii.get(self, "headerInput"))

    @builtins.property
    @jsii.member(jsii_name="keyInput")
    def key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyInput"))

    @builtins.property
    @jsii.member(jsii_name="partitionInput")
    def partition_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "partitionInput"))

    @builtins.property
    @jsii.member(jsii_name="topicInput")
    def topic_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "topicInput"))

    @builtins.property
    @jsii.member(jsii_name="clientProperties")
    def client_properties(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "clientProperties"))

    @client_properties.setter
    def client_properties(
        self,
        value: typing.Mapping[builtins.str, builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c05e3272f96fb5fa72b1301ae43ced78f6d02d2d743e3b2fcfd40968b7dee77e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientProperties", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="destinationArn")
    def destination_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "destinationArn"))

    @destination_arn.setter
    def destination_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5152b9590315cf97d3d1eb105c568bf53688239bfaed5f1cd21d25e5c290ee5a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "destinationArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "key"))

    @key.setter
    def key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bddc7a4a42d7d6d02ac67a2abf7ab3dfe7718b02ad5c9608ad2998c2ac271260)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="partition")
    def partition(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "partition"))

    @partition.setter
    def partition(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a4a7f5c4466648c670a073cf49383e7aa4454a59c12c56e8292986df329df48a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "partition", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="topic")
    def topic(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "topic"))

    @topic.setter
    def topic(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__97cc864d05fb68a3ac183e1b797eef0b7f04827fe35ee8447ba0dc42f1441f8c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "topic", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[IotTopicRuleErrorActionKafka]:
        return typing.cast(typing.Optional[IotTopicRuleErrorActionKafka], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[IotTopicRuleErrorActionKafka],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf4ee05c6bce37e622a5673e0b200e5048e0c84feef6a28aac2aeb9be75dd8f4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.iotTopicRule.IotTopicRuleErrorActionKinesis",
    jsii_struct_bases=[],
    name_mapping={
        "role_arn": "roleArn",
        "stream_name": "streamName",
        "partition_key": "partitionKey",
    },
)
class IotTopicRuleErrorActionKinesis:
    def __init__(
        self,
        *,
        role_arn: builtins.str,
        stream_name: builtins.str,
        partition_key: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#role_arn IotTopicRule#role_arn}.
        :param stream_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#stream_name IotTopicRule#stream_name}.
        :param partition_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#partition_key IotTopicRule#partition_key}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e21737535f3015cf1fbdfe49e3fe8fe6e99d25b8623dc1a077422ec47a67e2a)
            check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
            check_type(argname="argument stream_name", value=stream_name, expected_type=type_hints["stream_name"])
            check_type(argname="argument partition_key", value=partition_key, expected_type=type_hints["partition_key"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "role_arn": role_arn,
            "stream_name": stream_name,
        }
        if partition_key is not None:
            self._values["partition_key"] = partition_key

    @builtins.property
    def role_arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#role_arn IotTopicRule#role_arn}.'''
        result = self._values.get("role_arn")
        assert result is not None, "Required property 'role_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def stream_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#stream_name IotTopicRule#stream_name}.'''
        result = self._values.get("stream_name")
        assert result is not None, "Required property 'stream_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def partition_key(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#partition_key IotTopicRule#partition_key}.'''
        result = self._values.get("partition_key")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IotTopicRuleErrorActionKinesis(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class IotTopicRuleErrorActionKinesisOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.iotTopicRule.IotTopicRuleErrorActionKinesisOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0799c6bc46d4a2d16754114e6090a4c2b2521ef0dda7fb72b6ba30e6e750f64f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetPartitionKey")
    def reset_partition_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPartitionKey", []))

    @builtins.property
    @jsii.member(jsii_name="partitionKeyInput")
    def partition_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "partitionKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="roleArnInput")
    def role_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "roleArnInput"))

    @builtins.property
    @jsii.member(jsii_name="streamNameInput")
    def stream_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "streamNameInput"))

    @builtins.property
    @jsii.member(jsii_name="partitionKey")
    def partition_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "partitionKey"))

    @partition_key.setter
    def partition_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b396db0d63b3ebbfc850f17452760a5a61b53853b023e56524f2c1a78d7025da)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "partitionKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="roleArn")
    def role_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "roleArn"))

    @role_arn.setter
    def role_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b868c6f0472f074ea735f4e3241bf6188876a95ccae9ec87f2dd44da05982b03)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "roleArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="streamName")
    def stream_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "streamName"))

    @stream_name.setter
    def stream_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa0be88ecf5c2346109072c7a4e74c040b17e66800f1576980d82f961bb5976d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "streamName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[IotTopicRuleErrorActionKinesis]:
        return typing.cast(typing.Optional[IotTopicRuleErrorActionKinesis], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[IotTopicRuleErrorActionKinesis],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2913c77f58c716b85ecaa59894f6b2e8a2ef85f4f0b7b56e0ff6797e95788c3e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.iotTopicRule.IotTopicRuleErrorActionLambda",
    jsii_struct_bases=[],
    name_mapping={"function_arn": "functionArn"},
)
class IotTopicRuleErrorActionLambda:
    def __init__(self, *, function_arn: builtins.str) -> None:
        '''
        :param function_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#function_arn IotTopicRule#function_arn}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f385034edbfe04235c2656de1531112c05524d8c9b39bdd2bb7dcdfe47b8463a)
            check_type(argname="argument function_arn", value=function_arn, expected_type=type_hints["function_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "function_arn": function_arn,
        }

    @builtins.property
    def function_arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#function_arn IotTopicRule#function_arn}.'''
        result = self._values.get("function_arn")
        assert result is not None, "Required property 'function_arn' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IotTopicRuleErrorActionLambda(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class IotTopicRuleErrorActionLambdaOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.iotTopicRule.IotTopicRuleErrorActionLambdaOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__61db101dfb1e05993638e96037a2d721d2fb8216ca83981b1966d8d211cd2359)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="functionArnInput")
    def function_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "functionArnInput"))

    @builtins.property
    @jsii.member(jsii_name="functionArn")
    def function_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "functionArn"))

    @function_arn.setter
    def function_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f5bde8f174461287395141a31b0e783471e2d53f34d3d1316985c842f74a1144)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "functionArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[IotTopicRuleErrorActionLambda]:
        return typing.cast(typing.Optional[IotTopicRuleErrorActionLambda], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[IotTopicRuleErrorActionLambda],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c1c0d00a069d59ab1598a3a2c456bfd57c2819a18c0d072c8b448c5a815fa21f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class IotTopicRuleErrorActionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.iotTopicRule.IotTopicRuleErrorActionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__00ebeeab15e3325819fcc40ea15eea7090fcdbcd860f1671d42d63291a5aa96c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putCloudwatchAlarm")
    def put_cloudwatch_alarm(
        self,
        *,
        alarm_name: builtins.str,
        role_arn: builtins.str,
        state_reason: builtins.str,
        state_value: builtins.str,
    ) -> None:
        '''
        :param alarm_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#alarm_name IotTopicRule#alarm_name}.
        :param role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#role_arn IotTopicRule#role_arn}.
        :param state_reason: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#state_reason IotTopicRule#state_reason}.
        :param state_value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#state_value IotTopicRule#state_value}.
        '''
        value = IotTopicRuleErrorActionCloudwatchAlarm(
            alarm_name=alarm_name,
            role_arn=role_arn,
            state_reason=state_reason,
            state_value=state_value,
        )

        return typing.cast(None, jsii.invoke(self, "putCloudwatchAlarm", [value]))

    @jsii.member(jsii_name="putCloudwatchLogs")
    def put_cloudwatch_logs(
        self,
        *,
        log_group_name: builtins.str,
        role_arn: builtins.str,
        batch_mode: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param log_group_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#log_group_name IotTopicRule#log_group_name}.
        :param role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#role_arn IotTopicRule#role_arn}.
        :param batch_mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#batch_mode IotTopicRule#batch_mode}.
        '''
        value = IotTopicRuleErrorActionCloudwatchLogs(
            log_group_name=log_group_name, role_arn=role_arn, batch_mode=batch_mode
        )

        return typing.cast(None, jsii.invoke(self, "putCloudwatchLogs", [value]))

    @jsii.member(jsii_name="putCloudwatchMetric")
    def put_cloudwatch_metric(
        self,
        *,
        metric_name: builtins.str,
        metric_namespace: builtins.str,
        metric_unit: builtins.str,
        metric_value: builtins.str,
        role_arn: builtins.str,
        metric_timestamp: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param metric_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#metric_name IotTopicRule#metric_name}.
        :param metric_namespace: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#metric_namespace IotTopicRule#metric_namespace}.
        :param metric_unit: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#metric_unit IotTopicRule#metric_unit}.
        :param metric_value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#metric_value IotTopicRule#metric_value}.
        :param role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#role_arn IotTopicRule#role_arn}.
        :param metric_timestamp: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#metric_timestamp IotTopicRule#metric_timestamp}.
        '''
        value = IotTopicRuleErrorActionCloudwatchMetric(
            metric_name=metric_name,
            metric_namespace=metric_namespace,
            metric_unit=metric_unit,
            metric_value=metric_value,
            role_arn=role_arn,
            metric_timestamp=metric_timestamp,
        )

        return typing.cast(None, jsii.invoke(self, "putCloudwatchMetric", [value]))

    @jsii.member(jsii_name="putDynamodb")
    def put_dynamodb(
        self,
        *,
        hash_key_field: builtins.str,
        hash_key_value: builtins.str,
        role_arn: builtins.str,
        table_name: builtins.str,
        hash_key_type: typing.Optional[builtins.str] = None,
        operation: typing.Optional[builtins.str] = None,
        payload_field: typing.Optional[builtins.str] = None,
        range_key_field: typing.Optional[builtins.str] = None,
        range_key_type: typing.Optional[builtins.str] = None,
        range_key_value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param hash_key_field: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#hash_key_field IotTopicRule#hash_key_field}.
        :param hash_key_value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#hash_key_value IotTopicRule#hash_key_value}.
        :param role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#role_arn IotTopicRule#role_arn}.
        :param table_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#table_name IotTopicRule#table_name}.
        :param hash_key_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#hash_key_type IotTopicRule#hash_key_type}.
        :param operation: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#operation IotTopicRule#operation}.
        :param payload_field: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#payload_field IotTopicRule#payload_field}.
        :param range_key_field: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#range_key_field IotTopicRule#range_key_field}.
        :param range_key_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#range_key_type IotTopicRule#range_key_type}.
        :param range_key_value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#range_key_value IotTopicRule#range_key_value}.
        '''
        value = IotTopicRuleErrorActionDynamodb(
            hash_key_field=hash_key_field,
            hash_key_value=hash_key_value,
            role_arn=role_arn,
            table_name=table_name,
            hash_key_type=hash_key_type,
            operation=operation,
            payload_field=payload_field,
            range_key_field=range_key_field,
            range_key_type=range_key_type,
            range_key_value=range_key_value,
        )

        return typing.cast(None, jsii.invoke(self, "putDynamodb", [value]))

    @jsii.member(jsii_name="putDynamodbv2")
    def put_dynamodbv2(
        self,
        *,
        role_arn: builtins.str,
        put_item: typing.Optional[typing.Union[IotTopicRuleErrorActionDynamodbv2PutItem, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#role_arn IotTopicRule#role_arn}.
        :param put_item: put_item block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#put_item IotTopicRule#put_item}
        '''
        value = IotTopicRuleErrorActionDynamodbv2(role_arn=role_arn, put_item=put_item)

        return typing.cast(None, jsii.invoke(self, "putDynamodbv2", [value]))

    @jsii.member(jsii_name="putElasticsearch")
    def put_elasticsearch(
        self,
        *,
        endpoint: builtins.str,
        id: builtins.str,
        index: builtins.str,
        role_arn: builtins.str,
        type: builtins.str,
    ) -> None:
        '''
        :param endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#endpoint IotTopicRule#endpoint}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#id IotTopicRule#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param index: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#index IotTopicRule#index}.
        :param role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#role_arn IotTopicRule#role_arn}.
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#type IotTopicRule#type}.
        '''
        value = IotTopicRuleErrorActionElasticsearch(
            endpoint=endpoint, id=id, index=index, role_arn=role_arn, type=type
        )

        return typing.cast(None, jsii.invoke(self, "putElasticsearch", [value]))

    @jsii.member(jsii_name="putFirehose")
    def put_firehose(
        self,
        *,
        delivery_stream_name: builtins.str,
        role_arn: builtins.str,
        batch_mode: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        separator: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param delivery_stream_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#delivery_stream_name IotTopicRule#delivery_stream_name}.
        :param role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#role_arn IotTopicRule#role_arn}.
        :param batch_mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#batch_mode IotTopicRule#batch_mode}.
        :param separator: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#separator IotTopicRule#separator}.
        '''
        value = IotTopicRuleErrorActionFirehose(
            delivery_stream_name=delivery_stream_name,
            role_arn=role_arn,
            batch_mode=batch_mode,
            separator=separator,
        )

        return typing.cast(None, jsii.invoke(self, "putFirehose", [value]))

    @jsii.member(jsii_name="putHttp")
    def put_http(
        self,
        *,
        url: builtins.str,
        confirmation_url: typing.Optional[builtins.str] = None,
        http_header: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[IotTopicRuleErrorActionHttpHttpHeader, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param url: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#url IotTopicRule#url}.
        :param confirmation_url: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#confirmation_url IotTopicRule#confirmation_url}.
        :param http_header: http_header block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#http_header IotTopicRule#http_header}
        '''
        value = IotTopicRuleErrorActionHttp(
            url=url, confirmation_url=confirmation_url, http_header=http_header
        )

        return typing.cast(None, jsii.invoke(self, "putHttp", [value]))

    @jsii.member(jsii_name="putIotAnalytics")
    def put_iot_analytics(
        self,
        *,
        channel_name: builtins.str,
        role_arn: builtins.str,
        batch_mode: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param channel_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#channel_name IotTopicRule#channel_name}.
        :param role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#role_arn IotTopicRule#role_arn}.
        :param batch_mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#batch_mode IotTopicRule#batch_mode}.
        '''
        value = IotTopicRuleErrorActionIotAnalytics(
            channel_name=channel_name, role_arn=role_arn, batch_mode=batch_mode
        )

        return typing.cast(None, jsii.invoke(self, "putIotAnalytics", [value]))

    @jsii.member(jsii_name="putIotEvents")
    def put_iot_events(
        self,
        *,
        input_name: builtins.str,
        role_arn: builtins.str,
        batch_mode: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        message_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param input_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#input_name IotTopicRule#input_name}.
        :param role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#role_arn IotTopicRule#role_arn}.
        :param batch_mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#batch_mode IotTopicRule#batch_mode}.
        :param message_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#message_id IotTopicRule#message_id}.
        '''
        value = IotTopicRuleErrorActionIotEvents(
            input_name=input_name,
            role_arn=role_arn,
            batch_mode=batch_mode,
            message_id=message_id,
        )

        return typing.cast(None, jsii.invoke(self, "putIotEvents", [value]))

    @jsii.member(jsii_name="putKafka")
    def put_kafka(
        self,
        *,
        client_properties: typing.Mapping[builtins.str, builtins.str],
        destination_arn: builtins.str,
        topic: builtins.str,
        header: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[IotTopicRuleErrorActionKafkaHeader, typing.Dict[builtins.str, typing.Any]]]]] = None,
        key: typing.Optional[builtins.str] = None,
        partition: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param client_properties: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#client_properties IotTopicRule#client_properties}.
        :param destination_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#destination_arn IotTopicRule#destination_arn}.
        :param topic: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#topic IotTopicRule#topic}.
        :param header: header block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#header IotTopicRule#header}
        :param key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#key IotTopicRule#key}.
        :param partition: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#partition IotTopicRule#partition}.
        '''
        value = IotTopicRuleErrorActionKafka(
            client_properties=client_properties,
            destination_arn=destination_arn,
            topic=topic,
            header=header,
            key=key,
            partition=partition,
        )

        return typing.cast(None, jsii.invoke(self, "putKafka", [value]))

    @jsii.member(jsii_name="putKinesis")
    def put_kinesis(
        self,
        *,
        role_arn: builtins.str,
        stream_name: builtins.str,
        partition_key: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#role_arn IotTopicRule#role_arn}.
        :param stream_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#stream_name IotTopicRule#stream_name}.
        :param partition_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#partition_key IotTopicRule#partition_key}.
        '''
        value = IotTopicRuleErrorActionKinesis(
            role_arn=role_arn, stream_name=stream_name, partition_key=partition_key
        )

        return typing.cast(None, jsii.invoke(self, "putKinesis", [value]))

    @jsii.member(jsii_name="putLambda")
    def put_lambda(self, *, function_arn: builtins.str) -> None:
        '''
        :param function_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#function_arn IotTopicRule#function_arn}.
        '''
        value = IotTopicRuleErrorActionLambda(function_arn=function_arn)

        return typing.cast(None, jsii.invoke(self, "putLambda", [value]))

    @jsii.member(jsii_name="putRepublish")
    def put_republish(
        self,
        *,
        role_arn: builtins.str,
        topic: builtins.str,
        qos: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#role_arn IotTopicRule#role_arn}.
        :param topic: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#topic IotTopicRule#topic}.
        :param qos: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#qos IotTopicRule#qos}.
        '''
        value = IotTopicRuleErrorActionRepublish(
            role_arn=role_arn, topic=topic, qos=qos
        )

        return typing.cast(None, jsii.invoke(self, "putRepublish", [value]))

    @jsii.member(jsii_name="putS3")
    def put_s3(
        self,
        *,
        bucket_name: builtins.str,
        key: builtins.str,
        role_arn: builtins.str,
        canned_acl: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param bucket_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#bucket_name IotTopicRule#bucket_name}.
        :param key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#key IotTopicRule#key}.
        :param role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#role_arn IotTopicRule#role_arn}.
        :param canned_acl: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#canned_acl IotTopicRule#canned_acl}.
        '''
        value = IotTopicRuleErrorActionS3(
            bucket_name=bucket_name, key=key, role_arn=role_arn, canned_acl=canned_acl
        )

        return typing.cast(None, jsii.invoke(self, "putS3", [value]))

    @jsii.member(jsii_name="putSns")
    def put_sns(
        self,
        *,
        role_arn: builtins.str,
        target_arn: builtins.str,
        message_format: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#role_arn IotTopicRule#role_arn}.
        :param target_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#target_arn IotTopicRule#target_arn}.
        :param message_format: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#message_format IotTopicRule#message_format}.
        '''
        value = IotTopicRuleErrorActionSns(
            role_arn=role_arn, target_arn=target_arn, message_format=message_format
        )

        return typing.cast(None, jsii.invoke(self, "putSns", [value]))

    @jsii.member(jsii_name="putSqs")
    def put_sqs(
        self,
        *,
        queue_url: builtins.str,
        role_arn: builtins.str,
        use_base64: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        '''
        :param queue_url: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#queue_url IotTopicRule#queue_url}.
        :param role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#role_arn IotTopicRule#role_arn}.
        :param use_base64: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#use_base64 IotTopicRule#use_base64}.
        '''
        value = IotTopicRuleErrorActionSqs(
            queue_url=queue_url, role_arn=role_arn, use_base64=use_base64
        )

        return typing.cast(None, jsii.invoke(self, "putSqs", [value]))

    @jsii.member(jsii_name="putStepFunctions")
    def put_step_functions(
        self,
        *,
        role_arn: builtins.str,
        state_machine_name: builtins.str,
        execution_name_prefix: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#role_arn IotTopicRule#role_arn}.
        :param state_machine_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#state_machine_name IotTopicRule#state_machine_name}.
        :param execution_name_prefix: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#execution_name_prefix IotTopicRule#execution_name_prefix}.
        '''
        value = IotTopicRuleErrorActionStepFunctions(
            role_arn=role_arn,
            state_machine_name=state_machine_name,
            execution_name_prefix=execution_name_prefix,
        )

        return typing.cast(None, jsii.invoke(self, "putStepFunctions", [value]))

    @jsii.member(jsii_name="putTimestream")
    def put_timestream(
        self,
        *,
        database_name: builtins.str,
        dimension: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["IotTopicRuleErrorActionTimestreamDimension", typing.Dict[builtins.str, typing.Any]]]],
        role_arn: builtins.str,
        table_name: builtins.str,
        timestamp: typing.Optional[typing.Union["IotTopicRuleErrorActionTimestreamTimestamp", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param database_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#database_name IotTopicRule#database_name}.
        :param dimension: dimension block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#dimension IotTopicRule#dimension}
        :param role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#role_arn IotTopicRule#role_arn}.
        :param table_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#table_name IotTopicRule#table_name}.
        :param timestamp: timestamp block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#timestamp IotTopicRule#timestamp}
        '''
        value = IotTopicRuleErrorActionTimestream(
            database_name=database_name,
            dimension=dimension,
            role_arn=role_arn,
            table_name=table_name,
            timestamp=timestamp,
        )

        return typing.cast(None, jsii.invoke(self, "putTimestream", [value]))

    @jsii.member(jsii_name="resetCloudwatchAlarm")
    def reset_cloudwatch_alarm(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCloudwatchAlarm", []))

    @jsii.member(jsii_name="resetCloudwatchLogs")
    def reset_cloudwatch_logs(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCloudwatchLogs", []))

    @jsii.member(jsii_name="resetCloudwatchMetric")
    def reset_cloudwatch_metric(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCloudwatchMetric", []))

    @jsii.member(jsii_name="resetDynamodb")
    def reset_dynamodb(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDynamodb", []))

    @jsii.member(jsii_name="resetDynamodbv2")
    def reset_dynamodbv2(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDynamodbv2", []))

    @jsii.member(jsii_name="resetElasticsearch")
    def reset_elasticsearch(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetElasticsearch", []))

    @jsii.member(jsii_name="resetFirehose")
    def reset_firehose(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFirehose", []))

    @jsii.member(jsii_name="resetHttp")
    def reset_http(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHttp", []))

    @jsii.member(jsii_name="resetIotAnalytics")
    def reset_iot_analytics(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIotAnalytics", []))

    @jsii.member(jsii_name="resetIotEvents")
    def reset_iot_events(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIotEvents", []))

    @jsii.member(jsii_name="resetKafka")
    def reset_kafka(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKafka", []))

    @jsii.member(jsii_name="resetKinesis")
    def reset_kinesis(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKinesis", []))

    @jsii.member(jsii_name="resetLambda")
    def reset_lambda(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLambda", []))

    @jsii.member(jsii_name="resetRepublish")
    def reset_republish(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRepublish", []))

    @jsii.member(jsii_name="resetS3")
    def reset_s3(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetS3", []))

    @jsii.member(jsii_name="resetSns")
    def reset_sns(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSns", []))

    @jsii.member(jsii_name="resetSqs")
    def reset_sqs(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSqs", []))

    @jsii.member(jsii_name="resetStepFunctions")
    def reset_step_functions(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStepFunctions", []))

    @jsii.member(jsii_name="resetTimestream")
    def reset_timestream(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimestream", []))

    @builtins.property
    @jsii.member(jsii_name="cloudwatchAlarm")
    def cloudwatch_alarm(self) -> IotTopicRuleErrorActionCloudwatchAlarmOutputReference:
        return typing.cast(IotTopicRuleErrorActionCloudwatchAlarmOutputReference, jsii.get(self, "cloudwatchAlarm"))

    @builtins.property
    @jsii.member(jsii_name="cloudwatchLogs")
    def cloudwatch_logs(self) -> IotTopicRuleErrorActionCloudwatchLogsOutputReference:
        return typing.cast(IotTopicRuleErrorActionCloudwatchLogsOutputReference, jsii.get(self, "cloudwatchLogs"))

    @builtins.property
    @jsii.member(jsii_name="cloudwatchMetric")
    def cloudwatch_metric(
        self,
    ) -> IotTopicRuleErrorActionCloudwatchMetricOutputReference:
        return typing.cast(IotTopicRuleErrorActionCloudwatchMetricOutputReference, jsii.get(self, "cloudwatchMetric"))

    @builtins.property
    @jsii.member(jsii_name="dynamodb")
    def dynamodb(self) -> IotTopicRuleErrorActionDynamodbOutputReference:
        return typing.cast(IotTopicRuleErrorActionDynamodbOutputReference, jsii.get(self, "dynamodb"))

    @builtins.property
    @jsii.member(jsii_name="dynamodbv2")
    def dynamodbv2(self) -> IotTopicRuleErrorActionDynamodbv2OutputReference:
        return typing.cast(IotTopicRuleErrorActionDynamodbv2OutputReference, jsii.get(self, "dynamodbv2"))

    @builtins.property
    @jsii.member(jsii_name="elasticsearch")
    def elasticsearch(self) -> IotTopicRuleErrorActionElasticsearchOutputReference:
        return typing.cast(IotTopicRuleErrorActionElasticsearchOutputReference, jsii.get(self, "elasticsearch"))

    @builtins.property
    @jsii.member(jsii_name="firehose")
    def firehose(self) -> IotTopicRuleErrorActionFirehoseOutputReference:
        return typing.cast(IotTopicRuleErrorActionFirehoseOutputReference, jsii.get(self, "firehose"))

    @builtins.property
    @jsii.member(jsii_name="http")
    def http(self) -> IotTopicRuleErrorActionHttpOutputReference:
        return typing.cast(IotTopicRuleErrorActionHttpOutputReference, jsii.get(self, "http"))

    @builtins.property
    @jsii.member(jsii_name="iotAnalytics")
    def iot_analytics(self) -> IotTopicRuleErrorActionIotAnalyticsOutputReference:
        return typing.cast(IotTopicRuleErrorActionIotAnalyticsOutputReference, jsii.get(self, "iotAnalytics"))

    @builtins.property
    @jsii.member(jsii_name="iotEvents")
    def iot_events(self) -> IotTopicRuleErrorActionIotEventsOutputReference:
        return typing.cast(IotTopicRuleErrorActionIotEventsOutputReference, jsii.get(self, "iotEvents"))

    @builtins.property
    @jsii.member(jsii_name="kafka")
    def kafka(self) -> IotTopicRuleErrorActionKafkaOutputReference:
        return typing.cast(IotTopicRuleErrorActionKafkaOutputReference, jsii.get(self, "kafka"))

    @builtins.property
    @jsii.member(jsii_name="kinesis")
    def kinesis(self) -> IotTopicRuleErrorActionKinesisOutputReference:
        return typing.cast(IotTopicRuleErrorActionKinesisOutputReference, jsii.get(self, "kinesis"))

    @builtins.property
    @jsii.member(jsii_name="lambda")
    def lambda_(self) -> IotTopicRuleErrorActionLambdaOutputReference:
        return typing.cast(IotTopicRuleErrorActionLambdaOutputReference, jsii.get(self, "lambda"))

    @builtins.property
    @jsii.member(jsii_name="republish")
    def republish(self) -> "IotTopicRuleErrorActionRepublishOutputReference":
        return typing.cast("IotTopicRuleErrorActionRepublishOutputReference", jsii.get(self, "republish"))

    @builtins.property
    @jsii.member(jsii_name="s3")
    def s3(self) -> "IotTopicRuleErrorActionS3OutputReference":
        return typing.cast("IotTopicRuleErrorActionS3OutputReference", jsii.get(self, "s3"))

    @builtins.property
    @jsii.member(jsii_name="sns")
    def sns(self) -> "IotTopicRuleErrorActionSnsOutputReference":
        return typing.cast("IotTopicRuleErrorActionSnsOutputReference", jsii.get(self, "sns"))

    @builtins.property
    @jsii.member(jsii_name="sqs")
    def sqs(self) -> "IotTopicRuleErrorActionSqsOutputReference":
        return typing.cast("IotTopicRuleErrorActionSqsOutputReference", jsii.get(self, "sqs"))

    @builtins.property
    @jsii.member(jsii_name="stepFunctions")
    def step_functions(self) -> "IotTopicRuleErrorActionStepFunctionsOutputReference":
        return typing.cast("IotTopicRuleErrorActionStepFunctionsOutputReference", jsii.get(self, "stepFunctions"))

    @builtins.property
    @jsii.member(jsii_name="timestream")
    def timestream(self) -> "IotTopicRuleErrorActionTimestreamOutputReference":
        return typing.cast("IotTopicRuleErrorActionTimestreamOutputReference", jsii.get(self, "timestream"))

    @builtins.property
    @jsii.member(jsii_name="cloudwatchAlarmInput")
    def cloudwatch_alarm_input(
        self,
    ) -> typing.Optional[IotTopicRuleErrorActionCloudwatchAlarm]:
        return typing.cast(typing.Optional[IotTopicRuleErrorActionCloudwatchAlarm], jsii.get(self, "cloudwatchAlarmInput"))

    @builtins.property
    @jsii.member(jsii_name="cloudwatchLogsInput")
    def cloudwatch_logs_input(
        self,
    ) -> typing.Optional[IotTopicRuleErrorActionCloudwatchLogs]:
        return typing.cast(typing.Optional[IotTopicRuleErrorActionCloudwatchLogs], jsii.get(self, "cloudwatchLogsInput"))

    @builtins.property
    @jsii.member(jsii_name="cloudwatchMetricInput")
    def cloudwatch_metric_input(
        self,
    ) -> typing.Optional[IotTopicRuleErrorActionCloudwatchMetric]:
        return typing.cast(typing.Optional[IotTopicRuleErrorActionCloudwatchMetric], jsii.get(self, "cloudwatchMetricInput"))

    @builtins.property
    @jsii.member(jsii_name="dynamodbInput")
    def dynamodb_input(self) -> typing.Optional[IotTopicRuleErrorActionDynamodb]:
        return typing.cast(typing.Optional[IotTopicRuleErrorActionDynamodb], jsii.get(self, "dynamodbInput"))

    @builtins.property
    @jsii.member(jsii_name="dynamodbv2Input")
    def dynamodbv2_input(self) -> typing.Optional[IotTopicRuleErrorActionDynamodbv2]:
        return typing.cast(typing.Optional[IotTopicRuleErrorActionDynamodbv2], jsii.get(self, "dynamodbv2Input"))

    @builtins.property
    @jsii.member(jsii_name="elasticsearchInput")
    def elasticsearch_input(
        self,
    ) -> typing.Optional[IotTopicRuleErrorActionElasticsearch]:
        return typing.cast(typing.Optional[IotTopicRuleErrorActionElasticsearch], jsii.get(self, "elasticsearchInput"))

    @builtins.property
    @jsii.member(jsii_name="firehoseInput")
    def firehose_input(self) -> typing.Optional[IotTopicRuleErrorActionFirehose]:
        return typing.cast(typing.Optional[IotTopicRuleErrorActionFirehose], jsii.get(self, "firehoseInput"))

    @builtins.property
    @jsii.member(jsii_name="httpInput")
    def http_input(self) -> typing.Optional[IotTopicRuleErrorActionHttp]:
        return typing.cast(typing.Optional[IotTopicRuleErrorActionHttp], jsii.get(self, "httpInput"))

    @builtins.property
    @jsii.member(jsii_name="iotAnalyticsInput")
    def iot_analytics_input(
        self,
    ) -> typing.Optional[IotTopicRuleErrorActionIotAnalytics]:
        return typing.cast(typing.Optional[IotTopicRuleErrorActionIotAnalytics], jsii.get(self, "iotAnalyticsInput"))

    @builtins.property
    @jsii.member(jsii_name="iotEventsInput")
    def iot_events_input(self) -> typing.Optional[IotTopicRuleErrorActionIotEvents]:
        return typing.cast(typing.Optional[IotTopicRuleErrorActionIotEvents], jsii.get(self, "iotEventsInput"))

    @builtins.property
    @jsii.member(jsii_name="kafkaInput")
    def kafka_input(self) -> typing.Optional[IotTopicRuleErrorActionKafka]:
        return typing.cast(typing.Optional[IotTopicRuleErrorActionKafka], jsii.get(self, "kafkaInput"))

    @builtins.property
    @jsii.member(jsii_name="kinesisInput")
    def kinesis_input(self) -> typing.Optional[IotTopicRuleErrorActionKinesis]:
        return typing.cast(typing.Optional[IotTopicRuleErrorActionKinesis], jsii.get(self, "kinesisInput"))

    @builtins.property
    @jsii.member(jsii_name="lambdaInput")
    def lambda_input(self) -> typing.Optional[IotTopicRuleErrorActionLambda]:
        return typing.cast(typing.Optional[IotTopicRuleErrorActionLambda], jsii.get(self, "lambdaInput"))

    @builtins.property
    @jsii.member(jsii_name="republishInput")
    def republish_input(self) -> typing.Optional["IotTopicRuleErrorActionRepublish"]:
        return typing.cast(typing.Optional["IotTopicRuleErrorActionRepublish"], jsii.get(self, "republishInput"))

    @builtins.property
    @jsii.member(jsii_name="s3Input")
    def s3_input(self) -> typing.Optional["IotTopicRuleErrorActionS3"]:
        return typing.cast(typing.Optional["IotTopicRuleErrorActionS3"], jsii.get(self, "s3Input"))

    @builtins.property
    @jsii.member(jsii_name="snsInput")
    def sns_input(self) -> typing.Optional["IotTopicRuleErrorActionSns"]:
        return typing.cast(typing.Optional["IotTopicRuleErrorActionSns"], jsii.get(self, "snsInput"))

    @builtins.property
    @jsii.member(jsii_name="sqsInput")
    def sqs_input(self) -> typing.Optional["IotTopicRuleErrorActionSqs"]:
        return typing.cast(typing.Optional["IotTopicRuleErrorActionSqs"], jsii.get(self, "sqsInput"))

    @builtins.property
    @jsii.member(jsii_name="stepFunctionsInput")
    def step_functions_input(
        self,
    ) -> typing.Optional["IotTopicRuleErrorActionStepFunctions"]:
        return typing.cast(typing.Optional["IotTopicRuleErrorActionStepFunctions"], jsii.get(self, "stepFunctionsInput"))

    @builtins.property
    @jsii.member(jsii_name="timestreamInput")
    def timestream_input(self) -> typing.Optional["IotTopicRuleErrorActionTimestream"]:
        return typing.cast(typing.Optional["IotTopicRuleErrorActionTimestream"], jsii.get(self, "timestreamInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[IotTopicRuleErrorAction]:
        return typing.cast(typing.Optional[IotTopicRuleErrorAction], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[IotTopicRuleErrorAction]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c95adaa71b14572919497c31eae0eb39084f3470bcf6016fac9b53462122a7bf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.iotTopicRule.IotTopicRuleErrorActionRepublish",
    jsii_struct_bases=[],
    name_mapping={"role_arn": "roleArn", "topic": "topic", "qos": "qos"},
)
class IotTopicRuleErrorActionRepublish:
    def __init__(
        self,
        *,
        role_arn: builtins.str,
        topic: builtins.str,
        qos: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#role_arn IotTopicRule#role_arn}.
        :param topic: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#topic IotTopicRule#topic}.
        :param qos: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#qos IotTopicRule#qos}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a6712977dc19982d34c3a5bb1c3c1349ca9d07b6e3cd96bb200cfd3d9d05c1ff)
            check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
            check_type(argname="argument topic", value=topic, expected_type=type_hints["topic"])
            check_type(argname="argument qos", value=qos, expected_type=type_hints["qos"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "role_arn": role_arn,
            "topic": topic,
        }
        if qos is not None:
            self._values["qos"] = qos

    @builtins.property
    def role_arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#role_arn IotTopicRule#role_arn}.'''
        result = self._values.get("role_arn")
        assert result is not None, "Required property 'role_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def topic(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#topic IotTopicRule#topic}.'''
        result = self._values.get("topic")
        assert result is not None, "Required property 'topic' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def qos(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#qos IotTopicRule#qos}.'''
        result = self._values.get("qos")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IotTopicRuleErrorActionRepublish(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class IotTopicRuleErrorActionRepublishOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.iotTopicRule.IotTopicRuleErrorActionRepublishOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7565623ee5052a29b96b8bdd3cbf18f3344e9c5df29b4b1957b4d09ac95cdf81)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetQos")
    def reset_qos(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetQos", []))

    @builtins.property
    @jsii.member(jsii_name="qosInput")
    def qos_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "qosInput"))

    @builtins.property
    @jsii.member(jsii_name="roleArnInput")
    def role_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "roleArnInput"))

    @builtins.property
    @jsii.member(jsii_name="topicInput")
    def topic_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "topicInput"))

    @builtins.property
    @jsii.member(jsii_name="qos")
    def qos(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "qos"))

    @qos.setter
    def qos(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__72847506256fa8cf23dcb496119df88b82c774b33406bea5e5f29fa12a5f7439)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "qos", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="roleArn")
    def role_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "roleArn"))

    @role_arn.setter
    def role_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5458d50298e2253967a2112d540b09a4caf6bd2e245f4cbf25682ae0c96d2c99)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "roleArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="topic")
    def topic(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "topic"))

    @topic.setter
    def topic(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9975036502933aea8ffb862fa75b24cc742675337191a268f87f2303ad7bd646)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "topic", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[IotTopicRuleErrorActionRepublish]:
        return typing.cast(typing.Optional[IotTopicRuleErrorActionRepublish], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[IotTopicRuleErrorActionRepublish],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__84a071b12b6e35a9e424cf593263acee3f575b0af018ece556e5d8d36b838c61)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.iotTopicRule.IotTopicRuleErrorActionS3",
    jsii_struct_bases=[],
    name_mapping={
        "bucket_name": "bucketName",
        "key": "key",
        "role_arn": "roleArn",
        "canned_acl": "cannedAcl",
    },
)
class IotTopicRuleErrorActionS3:
    def __init__(
        self,
        *,
        bucket_name: builtins.str,
        key: builtins.str,
        role_arn: builtins.str,
        canned_acl: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param bucket_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#bucket_name IotTopicRule#bucket_name}.
        :param key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#key IotTopicRule#key}.
        :param role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#role_arn IotTopicRule#role_arn}.
        :param canned_acl: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#canned_acl IotTopicRule#canned_acl}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ec28e16ed6cf830ca9d64fb3849688526c0b226b430403fcb0be648b224b4a3a)
            check_type(argname="argument bucket_name", value=bucket_name, expected_type=type_hints["bucket_name"])
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
            check_type(argname="argument canned_acl", value=canned_acl, expected_type=type_hints["canned_acl"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "bucket_name": bucket_name,
            "key": key,
            "role_arn": role_arn,
        }
        if canned_acl is not None:
            self._values["canned_acl"] = canned_acl

    @builtins.property
    def bucket_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#bucket_name IotTopicRule#bucket_name}.'''
        result = self._values.get("bucket_name")
        assert result is not None, "Required property 'bucket_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def key(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#key IotTopicRule#key}.'''
        result = self._values.get("key")
        assert result is not None, "Required property 'key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def role_arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#role_arn IotTopicRule#role_arn}.'''
        result = self._values.get("role_arn")
        assert result is not None, "Required property 'role_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def canned_acl(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#canned_acl IotTopicRule#canned_acl}.'''
        result = self._values.get("canned_acl")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IotTopicRuleErrorActionS3(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class IotTopicRuleErrorActionS3OutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.iotTopicRule.IotTopicRuleErrorActionS3OutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f0ab642389342987d96055dcee623c9a23a99440380cdb3ddb0154561fd16700)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCannedAcl")
    def reset_canned_acl(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCannedAcl", []))

    @builtins.property
    @jsii.member(jsii_name="bucketNameInput")
    def bucket_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bucketNameInput"))

    @builtins.property
    @jsii.member(jsii_name="cannedAclInput")
    def canned_acl_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cannedAclInput"))

    @builtins.property
    @jsii.member(jsii_name="keyInput")
    def key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyInput"))

    @builtins.property
    @jsii.member(jsii_name="roleArnInput")
    def role_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "roleArnInput"))

    @builtins.property
    @jsii.member(jsii_name="bucketName")
    def bucket_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bucketName"))

    @bucket_name.setter
    def bucket_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ff7b2d101f0604dd8416385824811837e0f799ca3ad0ae3c7a276d03746880e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bucketName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="cannedAcl")
    def canned_acl(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cannedAcl"))

    @canned_acl.setter
    def canned_acl(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__69d2d5eb1a0b0ab3847273a235b18d909aef9f0c0762607d7a826f2483ca7068)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cannedAcl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "key"))

    @key.setter
    def key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f0efa9685f72d303b5ff9490ef93040ee7fa29e366ee728b69bf2e3790a47d3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="roleArn")
    def role_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "roleArn"))

    @role_arn.setter
    def role_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d987cdfe88d3b27766029731c82433813cf7d4e27414cd973110f302ddb6fc23)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "roleArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[IotTopicRuleErrorActionS3]:
        return typing.cast(typing.Optional[IotTopicRuleErrorActionS3], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[IotTopicRuleErrorActionS3]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ff1fe4667fa474d495f6882fbd4fb3415b1d8bab8a2528e78d2fa87dbadc2a80)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.iotTopicRule.IotTopicRuleErrorActionSns",
    jsii_struct_bases=[],
    name_mapping={
        "role_arn": "roleArn",
        "target_arn": "targetArn",
        "message_format": "messageFormat",
    },
)
class IotTopicRuleErrorActionSns:
    def __init__(
        self,
        *,
        role_arn: builtins.str,
        target_arn: builtins.str,
        message_format: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#role_arn IotTopicRule#role_arn}.
        :param target_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#target_arn IotTopicRule#target_arn}.
        :param message_format: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#message_format IotTopicRule#message_format}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e108faee455394cfc067c91f0e679b286ff8789dc184da16b9bdbf0ab9aae60f)
            check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
            check_type(argname="argument target_arn", value=target_arn, expected_type=type_hints["target_arn"])
            check_type(argname="argument message_format", value=message_format, expected_type=type_hints["message_format"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "role_arn": role_arn,
            "target_arn": target_arn,
        }
        if message_format is not None:
            self._values["message_format"] = message_format

    @builtins.property
    def role_arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#role_arn IotTopicRule#role_arn}.'''
        result = self._values.get("role_arn")
        assert result is not None, "Required property 'role_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def target_arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#target_arn IotTopicRule#target_arn}.'''
        result = self._values.get("target_arn")
        assert result is not None, "Required property 'target_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def message_format(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#message_format IotTopicRule#message_format}.'''
        result = self._values.get("message_format")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IotTopicRuleErrorActionSns(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class IotTopicRuleErrorActionSnsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.iotTopicRule.IotTopicRuleErrorActionSnsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__97e6f1a87498a265bcb9ddfb2011593650c36f0af5302e39ebc17330f47c0ad4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetMessageFormat")
    def reset_message_format(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMessageFormat", []))

    @builtins.property
    @jsii.member(jsii_name="messageFormatInput")
    def message_format_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "messageFormatInput"))

    @builtins.property
    @jsii.member(jsii_name="roleArnInput")
    def role_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "roleArnInput"))

    @builtins.property
    @jsii.member(jsii_name="targetArnInput")
    def target_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "targetArnInput"))

    @builtins.property
    @jsii.member(jsii_name="messageFormat")
    def message_format(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "messageFormat"))

    @message_format.setter
    def message_format(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__65167ce645e7b4e7ccb09affd26fb29a3701ac33f5c6d8fa1d6da7194f03e63e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "messageFormat", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="roleArn")
    def role_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "roleArn"))

    @role_arn.setter
    def role_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b601d1eda660c75b29fc413157dd3656d0529d0937132276b1930176bc005042)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "roleArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="targetArn")
    def target_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "targetArn"))

    @target_arn.setter
    def target_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__db80adc2f41c253b7d1b0e4b68b88ebbe09d14815480b1c20a1488248bf64993)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "targetArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[IotTopicRuleErrorActionSns]:
        return typing.cast(typing.Optional[IotTopicRuleErrorActionSns], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[IotTopicRuleErrorActionSns],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0233c7a96c6a307d365f4fed98c94d730400e85daa7d6c0888918cf45029f309)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.iotTopicRule.IotTopicRuleErrorActionSqs",
    jsii_struct_bases=[],
    name_mapping={
        "queue_url": "queueUrl",
        "role_arn": "roleArn",
        "use_base64": "useBase64",
    },
)
class IotTopicRuleErrorActionSqs:
    def __init__(
        self,
        *,
        queue_url: builtins.str,
        role_arn: builtins.str,
        use_base64: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        '''
        :param queue_url: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#queue_url IotTopicRule#queue_url}.
        :param role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#role_arn IotTopicRule#role_arn}.
        :param use_base64: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#use_base64 IotTopicRule#use_base64}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__50c850353ddd6e0a599b8475622d3867c868ec41f35c7e47fd698fe111f7195f)
            check_type(argname="argument queue_url", value=queue_url, expected_type=type_hints["queue_url"])
            check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
            check_type(argname="argument use_base64", value=use_base64, expected_type=type_hints["use_base64"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "queue_url": queue_url,
            "role_arn": role_arn,
            "use_base64": use_base64,
        }

    @builtins.property
    def queue_url(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#queue_url IotTopicRule#queue_url}.'''
        result = self._values.get("queue_url")
        assert result is not None, "Required property 'queue_url' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def role_arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#role_arn IotTopicRule#role_arn}.'''
        result = self._values.get("role_arn")
        assert result is not None, "Required property 'role_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def use_base64(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#use_base64 IotTopicRule#use_base64}.'''
        result = self._values.get("use_base64")
        assert result is not None, "Required property 'use_base64' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IotTopicRuleErrorActionSqs(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class IotTopicRuleErrorActionSqsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.iotTopicRule.IotTopicRuleErrorActionSqsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8d0636926e3861d560a40349d7669e3222a54b936ee12086a398340f422747d5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="queueUrlInput")
    def queue_url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "queueUrlInput"))

    @builtins.property
    @jsii.member(jsii_name="roleArnInput")
    def role_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "roleArnInput"))

    @builtins.property
    @jsii.member(jsii_name="useBase64Input")
    def use_base64_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "useBase64Input"))

    @builtins.property
    @jsii.member(jsii_name="queueUrl")
    def queue_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "queueUrl"))

    @queue_url.setter
    def queue_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__60f8355ea47492b5f137f4de1598f05469441556a6d2406845f1504270d1331b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "queueUrl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="roleArn")
    def role_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "roleArn"))

    @role_arn.setter
    def role_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba3010fe2faf630b5ed43c26d94d112a47316f56eea969c457697f39895dc804)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "roleArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="useBase64")
    def use_base64(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "useBase64"))

    @use_base64.setter
    def use_base64(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8142167db08dcf918db39d3527097ab62fddf763b31b86d270948ddf9194e852)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "useBase64", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[IotTopicRuleErrorActionSqs]:
        return typing.cast(typing.Optional[IotTopicRuleErrorActionSqs], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[IotTopicRuleErrorActionSqs],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__300b2d0ddb9ca90609a76274ed47cf29691237a843ec036b874ccee453f03fab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.iotTopicRule.IotTopicRuleErrorActionStepFunctions",
    jsii_struct_bases=[],
    name_mapping={
        "role_arn": "roleArn",
        "state_machine_name": "stateMachineName",
        "execution_name_prefix": "executionNamePrefix",
    },
)
class IotTopicRuleErrorActionStepFunctions:
    def __init__(
        self,
        *,
        role_arn: builtins.str,
        state_machine_name: builtins.str,
        execution_name_prefix: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#role_arn IotTopicRule#role_arn}.
        :param state_machine_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#state_machine_name IotTopicRule#state_machine_name}.
        :param execution_name_prefix: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#execution_name_prefix IotTopicRule#execution_name_prefix}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8269367c088c29125e7c8759563a43ed35850f7dfc531be70dd654cf27b561fa)
            check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
            check_type(argname="argument state_machine_name", value=state_machine_name, expected_type=type_hints["state_machine_name"])
            check_type(argname="argument execution_name_prefix", value=execution_name_prefix, expected_type=type_hints["execution_name_prefix"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "role_arn": role_arn,
            "state_machine_name": state_machine_name,
        }
        if execution_name_prefix is not None:
            self._values["execution_name_prefix"] = execution_name_prefix

    @builtins.property
    def role_arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#role_arn IotTopicRule#role_arn}.'''
        result = self._values.get("role_arn")
        assert result is not None, "Required property 'role_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def state_machine_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#state_machine_name IotTopicRule#state_machine_name}.'''
        result = self._values.get("state_machine_name")
        assert result is not None, "Required property 'state_machine_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def execution_name_prefix(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#execution_name_prefix IotTopicRule#execution_name_prefix}.'''
        result = self._values.get("execution_name_prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IotTopicRuleErrorActionStepFunctions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class IotTopicRuleErrorActionStepFunctionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.iotTopicRule.IotTopicRuleErrorActionStepFunctionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7c0aff059c817a5bb2aa16ef672e23cfab9ea19fcb6ccac0b3e5fa4c9071a656)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetExecutionNamePrefix")
    def reset_execution_name_prefix(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExecutionNamePrefix", []))

    @builtins.property
    @jsii.member(jsii_name="executionNamePrefixInput")
    def execution_name_prefix_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "executionNamePrefixInput"))

    @builtins.property
    @jsii.member(jsii_name="roleArnInput")
    def role_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "roleArnInput"))

    @builtins.property
    @jsii.member(jsii_name="stateMachineNameInput")
    def state_machine_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "stateMachineNameInput"))

    @builtins.property
    @jsii.member(jsii_name="executionNamePrefix")
    def execution_name_prefix(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "executionNamePrefix"))

    @execution_name_prefix.setter
    def execution_name_prefix(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ad3510cb67b7bb8df875c630bc6aac84dbefa45bd3b17c9daa843df62b31137)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "executionNamePrefix", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="roleArn")
    def role_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "roleArn"))

    @role_arn.setter
    def role_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4fdbc0db41896c9772c5712ebd1713691ba530690b3dd433a19dbee2c927a18b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "roleArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="stateMachineName")
    def state_machine_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "stateMachineName"))

    @state_machine_name.setter
    def state_machine_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7baf611fdb54e384950e20ca0dfd77f4ad4e7b7b004c2c4c029079e2dfbdc573)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "stateMachineName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[IotTopicRuleErrorActionStepFunctions]:
        return typing.cast(typing.Optional[IotTopicRuleErrorActionStepFunctions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[IotTopicRuleErrorActionStepFunctions],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__05ad922ce4ce7455c8c1b3c5270811c18663de0225e04963a1db0391279cb500)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.iotTopicRule.IotTopicRuleErrorActionTimestream",
    jsii_struct_bases=[],
    name_mapping={
        "database_name": "databaseName",
        "dimension": "dimension",
        "role_arn": "roleArn",
        "table_name": "tableName",
        "timestamp": "timestamp",
    },
)
class IotTopicRuleErrorActionTimestream:
    def __init__(
        self,
        *,
        database_name: builtins.str,
        dimension: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["IotTopicRuleErrorActionTimestreamDimension", typing.Dict[builtins.str, typing.Any]]]],
        role_arn: builtins.str,
        table_name: builtins.str,
        timestamp: typing.Optional[typing.Union["IotTopicRuleErrorActionTimestreamTimestamp", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param database_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#database_name IotTopicRule#database_name}.
        :param dimension: dimension block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#dimension IotTopicRule#dimension}
        :param role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#role_arn IotTopicRule#role_arn}.
        :param table_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#table_name IotTopicRule#table_name}.
        :param timestamp: timestamp block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#timestamp IotTopicRule#timestamp}
        '''
        if isinstance(timestamp, dict):
            timestamp = IotTopicRuleErrorActionTimestreamTimestamp(**timestamp)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c3ebd267f6add216c21f4f9b3ef299a69609c26b09ee33b411a7f093566f636)
            check_type(argname="argument database_name", value=database_name, expected_type=type_hints["database_name"])
            check_type(argname="argument dimension", value=dimension, expected_type=type_hints["dimension"])
            check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
            check_type(argname="argument table_name", value=table_name, expected_type=type_hints["table_name"])
            check_type(argname="argument timestamp", value=timestamp, expected_type=type_hints["timestamp"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "database_name": database_name,
            "dimension": dimension,
            "role_arn": role_arn,
            "table_name": table_name,
        }
        if timestamp is not None:
            self._values["timestamp"] = timestamp

    @builtins.property
    def database_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#database_name IotTopicRule#database_name}.'''
        result = self._values.get("database_name")
        assert result is not None, "Required property 'database_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def dimension(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["IotTopicRuleErrorActionTimestreamDimension"]]:
        '''dimension block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#dimension IotTopicRule#dimension}
        '''
        result = self._values.get("dimension")
        assert result is not None, "Required property 'dimension' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["IotTopicRuleErrorActionTimestreamDimension"]], result)

    @builtins.property
    def role_arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#role_arn IotTopicRule#role_arn}.'''
        result = self._values.get("role_arn")
        assert result is not None, "Required property 'role_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def table_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#table_name IotTopicRule#table_name}.'''
        result = self._values.get("table_name")
        assert result is not None, "Required property 'table_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def timestamp(
        self,
    ) -> typing.Optional["IotTopicRuleErrorActionTimestreamTimestamp"]:
        '''timestamp block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#timestamp IotTopicRule#timestamp}
        '''
        result = self._values.get("timestamp")
        return typing.cast(typing.Optional["IotTopicRuleErrorActionTimestreamTimestamp"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IotTopicRuleErrorActionTimestream(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.iotTopicRule.IotTopicRuleErrorActionTimestreamDimension",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "value": "value"},
)
class IotTopicRuleErrorActionTimestreamDimension:
    def __init__(self, *, name: builtins.str, value: builtins.str) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#name IotTopicRule#name}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#value IotTopicRule#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c70fae2411c45f757f16d6e8e6d00f841a08842d27504cf32b9f64f2809cf48d)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "value": value,
        }

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#name IotTopicRule#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#value IotTopicRule#value}.'''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IotTopicRuleErrorActionTimestreamDimension(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class IotTopicRuleErrorActionTimestreamDimensionList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.iotTopicRule.IotTopicRuleErrorActionTimestreamDimensionList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a8c81e59ee190108befde35635970715fc5423e1db2d095b30161dfa18e2daa1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "IotTopicRuleErrorActionTimestreamDimensionOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__982ec7d09023002404cc73d8159e55b6025886a3679e266f68c2f145e0a0d67d)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("IotTopicRuleErrorActionTimestreamDimensionOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__991db1d46a9d2438799da21b41828e745819010748cc76392721cd4e51878600)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8509c41c3154734aaacd4252cce7551079aeb10a81c3b70529ca8e3aca688c88)
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
            type_hints = typing.get_type_hints(_typecheckingstub__eb8993732696614d9e2b2a689096a7c1a1814ea110e9a9a2fde35a12eba21c18)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotTopicRuleErrorActionTimestreamDimension]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotTopicRuleErrorActionTimestreamDimension]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotTopicRuleErrorActionTimestreamDimension]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ceaef9f5fcdc998040c342e87584306c565ddf6594855f82033e0d3d248752e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class IotTopicRuleErrorActionTimestreamDimensionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.iotTopicRule.IotTopicRuleErrorActionTimestreamDimensionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1af7602a5f9f4fc793979ccbb864334e651b3b9a9f8809d08fe3e78ab998e0c5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d20aa3212c1763007de7c34ca4f7cc75813e8f5c1b2e915ba3792309449c9fad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__937edbc0201646e580d20d1eb10f7d989dfa0cc84890c25685ba013171fbd758)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IotTopicRuleErrorActionTimestreamDimension]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IotTopicRuleErrorActionTimestreamDimension]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IotTopicRuleErrorActionTimestreamDimension]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__07b559559def85ddcb4c190257793d038b3e148acf005f6d79cb9b72ec2368e0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class IotTopicRuleErrorActionTimestreamOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.iotTopicRule.IotTopicRuleErrorActionTimestreamOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3516b468f11c6196878fd6aa636ade91378e582163242364940287c44de9ea44)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putDimension")
    def put_dimension(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[IotTopicRuleErrorActionTimestreamDimension, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9cfde3822a87f8679fcaf07410cddcf2935277d6296340e206373a523b442d00)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putDimension", [value]))

    @jsii.member(jsii_name="putTimestamp")
    def put_timestamp(self, *, unit: builtins.str, value: builtins.str) -> None:
        '''
        :param unit: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#unit IotTopicRule#unit}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#value IotTopicRule#value}.
        '''
        value_ = IotTopicRuleErrorActionTimestreamTimestamp(unit=unit, value=value)

        return typing.cast(None, jsii.invoke(self, "putTimestamp", [value_]))

    @jsii.member(jsii_name="resetTimestamp")
    def reset_timestamp(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimestamp", []))

    @builtins.property
    @jsii.member(jsii_name="dimension")
    def dimension(self) -> IotTopicRuleErrorActionTimestreamDimensionList:
        return typing.cast(IotTopicRuleErrorActionTimestreamDimensionList, jsii.get(self, "dimension"))

    @builtins.property
    @jsii.member(jsii_name="timestamp")
    def timestamp(self) -> "IotTopicRuleErrorActionTimestreamTimestampOutputReference":
        return typing.cast("IotTopicRuleErrorActionTimestreamTimestampOutputReference", jsii.get(self, "timestamp"))

    @builtins.property
    @jsii.member(jsii_name="databaseNameInput")
    def database_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "databaseNameInput"))

    @builtins.property
    @jsii.member(jsii_name="dimensionInput")
    def dimension_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotTopicRuleErrorActionTimestreamDimension]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotTopicRuleErrorActionTimestreamDimension]]], jsii.get(self, "dimensionInput"))

    @builtins.property
    @jsii.member(jsii_name="roleArnInput")
    def role_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "roleArnInput"))

    @builtins.property
    @jsii.member(jsii_name="tableNameInput")
    def table_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tableNameInput"))

    @builtins.property
    @jsii.member(jsii_name="timestampInput")
    def timestamp_input(
        self,
    ) -> typing.Optional["IotTopicRuleErrorActionTimestreamTimestamp"]:
        return typing.cast(typing.Optional["IotTopicRuleErrorActionTimestreamTimestamp"], jsii.get(self, "timestampInput"))

    @builtins.property
    @jsii.member(jsii_name="databaseName")
    def database_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "databaseName"))

    @database_name.setter
    def database_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f2fbafd0b0e01c226560d2402d440140bba1f195d2650a39c2cfcf4a64afb27c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "databaseName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="roleArn")
    def role_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "roleArn"))

    @role_arn.setter
    def role_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__921c87ea9f25b34efe4fc1d35a2733d648d49380279d6fb50967dff898c8592c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "roleArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tableName")
    def table_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tableName"))

    @table_name.setter
    def table_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__de15e6e977552d0438fb53542946f9960352aff9ee5957b805b2678da2153e70)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tableName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[IotTopicRuleErrorActionTimestream]:
        return typing.cast(typing.Optional[IotTopicRuleErrorActionTimestream], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[IotTopicRuleErrorActionTimestream],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a5f46914e81963adfb178842808cdf7df91b102031f297f9f3e29de69c75a5fd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.iotTopicRule.IotTopicRuleErrorActionTimestreamTimestamp",
    jsii_struct_bases=[],
    name_mapping={"unit": "unit", "value": "value"},
)
class IotTopicRuleErrorActionTimestreamTimestamp:
    def __init__(self, *, unit: builtins.str, value: builtins.str) -> None:
        '''
        :param unit: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#unit IotTopicRule#unit}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#value IotTopicRule#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__60349f463024dc1254030de3655e613eb9cce4fa5c14ac21b000ff23b2d78ee0)
            check_type(argname="argument unit", value=unit, expected_type=type_hints["unit"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "unit": unit,
            "value": value,
        }

    @builtins.property
    def unit(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#unit IotTopicRule#unit}.'''
        result = self._values.get("unit")
        assert result is not None, "Required property 'unit' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#value IotTopicRule#value}.'''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IotTopicRuleErrorActionTimestreamTimestamp(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class IotTopicRuleErrorActionTimestreamTimestampOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.iotTopicRule.IotTopicRuleErrorActionTimestreamTimestampOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5fbfa2392f79a32a758c83a3ce00922a85e0e400740f1a1f33c88c64bd43ba46)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="unitInput")
    def unit_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "unitInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="unit")
    def unit(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "unit"))

    @unit.setter
    def unit(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__472fef77d786e74f3ef3db399270bc33d4c174341c1285d6ac319d8422aba08a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "unit", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa0aec99568431fffe865bfd2aa899b3991a066f0d196677128c92bc3c7bb56c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[IotTopicRuleErrorActionTimestreamTimestamp]:
        return typing.cast(typing.Optional[IotTopicRuleErrorActionTimestreamTimestamp], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[IotTopicRuleErrorActionTimestreamTimestamp],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c8b84df9a0d954d311e4a2a62f9991c3dcd28afd70e86d3ac89e980252b29dc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.iotTopicRule.IotTopicRuleFirehose",
    jsii_struct_bases=[],
    name_mapping={
        "delivery_stream_name": "deliveryStreamName",
        "role_arn": "roleArn",
        "batch_mode": "batchMode",
        "separator": "separator",
    },
)
class IotTopicRuleFirehose:
    def __init__(
        self,
        *,
        delivery_stream_name: builtins.str,
        role_arn: builtins.str,
        batch_mode: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        separator: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param delivery_stream_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#delivery_stream_name IotTopicRule#delivery_stream_name}.
        :param role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#role_arn IotTopicRule#role_arn}.
        :param batch_mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#batch_mode IotTopicRule#batch_mode}.
        :param separator: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#separator IotTopicRule#separator}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f2407f32762933e02b48ee5c96c26b0f4208c15249e5a8522dff696849f7818)
            check_type(argname="argument delivery_stream_name", value=delivery_stream_name, expected_type=type_hints["delivery_stream_name"])
            check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
            check_type(argname="argument batch_mode", value=batch_mode, expected_type=type_hints["batch_mode"])
            check_type(argname="argument separator", value=separator, expected_type=type_hints["separator"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "delivery_stream_name": delivery_stream_name,
            "role_arn": role_arn,
        }
        if batch_mode is not None:
            self._values["batch_mode"] = batch_mode
        if separator is not None:
            self._values["separator"] = separator

    @builtins.property
    def delivery_stream_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#delivery_stream_name IotTopicRule#delivery_stream_name}.'''
        result = self._values.get("delivery_stream_name")
        assert result is not None, "Required property 'delivery_stream_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def role_arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#role_arn IotTopicRule#role_arn}.'''
        result = self._values.get("role_arn")
        assert result is not None, "Required property 'role_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def batch_mode(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#batch_mode IotTopicRule#batch_mode}.'''
        result = self._values.get("batch_mode")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def separator(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#separator IotTopicRule#separator}.'''
        result = self._values.get("separator")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IotTopicRuleFirehose(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class IotTopicRuleFirehoseList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.iotTopicRule.IotTopicRuleFirehoseList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bd8c00e703ae2ef23ad68d264dd63ae2759469de58a5585824529221bb822c70)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "IotTopicRuleFirehoseOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ad241da3600abc0227fe14d3fde678a9cb7d12f055fa1d60f61546604abf8fa)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("IotTopicRuleFirehoseOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2db7e8393961f419375e3c0ac48c9d762f2f17b70f1b105dbcdecf08f5ce271c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__da7c3f95518033a3b47813a3decda43cf7364abc1758093bce4660c3b186306f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__60d0f3a41c50977f3e0e007e7f952c533ac351aaf994bd42199014245eed8206)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotTopicRuleFirehose]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotTopicRuleFirehose]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotTopicRuleFirehose]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__54653508a0f23c37ef1ee2811f529b3ce58d0b815bde0b6e3c0488b1ad8ea2f5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class IotTopicRuleFirehoseOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.iotTopicRule.IotTopicRuleFirehoseOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b2910edb15f5326f6ee6de192cd9f658801180756afcaa1c0a4f56bdf8b4d321)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetBatchMode")
    def reset_batch_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBatchMode", []))

    @jsii.member(jsii_name="resetSeparator")
    def reset_separator(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSeparator", []))

    @builtins.property
    @jsii.member(jsii_name="batchModeInput")
    def batch_mode_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "batchModeInput"))

    @builtins.property
    @jsii.member(jsii_name="deliveryStreamNameInput")
    def delivery_stream_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "deliveryStreamNameInput"))

    @builtins.property
    @jsii.member(jsii_name="roleArnInput")
    def role_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "roleArnInput"))

    @builtins.property
    @jsii.member(jsii_name="separatorInput")
    def separator_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "separatorInput"))

    @builtins.property
    @jsii.member(jsii_name="batchMode")
    def batch_mode(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "batchMode"))

    @batch_mode.setter
    def batch_mode(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b5abea5451e4b82b622c5fa6a0095f3a639371af2973d9d9e75dec5906188d71)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "batchMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="deliveryStreamName")
    def delivery_stream_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "deliveryStreamName"))

    @delivery_stream_name.setter
    def delivery_stream_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__000816dd917b8ad9e94a7bd36de746bd3bd46a24601ad25349a3ccf9fb246596)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deliveryStreamName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="roleArn")
    def role_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "roleArn"))

    @role_arn.setter
    def role_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc6e3b3983fbed11c7fb063311429b1ae96eee49ca27e50775e504386cf8d2ba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "roleArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="separator")
    def separator(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "separator"))

    @separator.setter
    def separator(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bc639e92d9303f80b3fd84c581763c07bd453998989ac0e3e3234e56d872f479)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "separator", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IotTopicRuleFirehose]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IotTopicRuleFirehose]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IotTopicRuleFirehose]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eb8d0a09d3056e257477ae8057b36f17c529a32eaac18f7aaca4594c933292b9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.iotTopicRule.IotTopicRuleHttp",
    jsii_struct_bases=[],
    name_mapping={
        "url": "url",
        "confirmation_url": "confirmationUrl",
        "http_header": "httpHeader",
    },
)
class IotTopicRuleHttp:
    def __init__(
        self,
        *,
        url: builtins.str,
        confirmation_url: typing.Optional[builtins.str] = None,
        http_header: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["IotTopicRuleHttpHttpHeader", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param url: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#url IotTopicRule#url}.
        :param confirmation_url: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#confirmation_url IotTopicRule#confirmation_url}.
        :param http_header: http_header block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#http_header IotTopicRule#http_header}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b7693bff804c71775bd3d89dbf4e1621eb8ae75f3f2aea2e26e1b3cf9d5a4e8)
            check_type(argname="argument url", value=url, expected_type=type_hints["url"])
            check_type(argname="argument confirmation_url", value=confirmation_url, expected_type=type_hints["confirmation_url"])
            check_type(argname="argument http_header", value=http_header, expected_type=type_hints["http_header"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "url": url,
        }
        if confirmation_url is not None:
            self._values["confirmation_url"] = confirmation_url
        if http_header is not None:
            self._values["http_header"] = http_header

    @builtins.property
    def url(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#url IotTopicRule#url}.'''
        result = self._values.get("url")
        assert result is not None, "Required property 'url' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def confirmation_url(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#confirmation_url IotTopicRule#confirmation_url}.'''
        result = self._values.get("confirmation_url")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def http_header(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["IotTopicRuleHttpHttpHeader"]]]:
        '''http_header block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#http_header IotTopicRule#http_header}
        '''
        result = self._values.get("http_header")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["IotTopicRuleHttpHttpHeader"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IotTopicRuleHttp(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.iotTopicRule.IotTopicRuleHttpHttpHeader",
    jsii_struct_bases=[],
    name_mapping={"key": "key", "value": "value"},
)
class IotTopicRuleHttpHttpHeader:
    def __init__(self, *, key: builtins.str, value: builtins.str) -> None:
        '''
        :param key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#key IotTopicRule#key}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#value IotTopicRule#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b1c2689d60da128f35e7f5fe2d90c0378e06da2618deb611e8d9290e0a06acbb)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "key": key,
            "value": value,
        }

    @builtins.property
    def key(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#key IotTopicRule#key}.'''
        result = self._values.get("key")
        assert result is not None, "Required property 'key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#value IotTopicRule#value}.'''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IotTopicRuleHttpHttpHeader(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class IotTopicRuleHttpHttpHeaderList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.iotTopicRule.IotTopicRuleHttpHttpHeaderList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a34c2d4aa7f23fccce4a675d76b83165c1f7d922ea2e7e0f94c43832564e7da3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "IotTopicRuleHttpHttpHeaderOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__48c62089f281397d7ba95d04792ab28f3ae69ba653f042769a2ebcda7f92ce51)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("IotTopicRuleHttpHttpHeaderOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__916c723df55492d8443a9d9b4e5305464db363aa9783d0ab226b06621debdcd1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ea2aaace01dc568855c5c5657300cff18f291863d50079876de9e9ea6341be35)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5b37a349447483d828f837ae4aa6945bc7308adf6e73b94adbf693ec19075158)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotTopicRuleHttpHttpHeader]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotTopicRuleHttpHttpHeader]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotTopicRuleHttpHttpHeader]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7027ac58eb5000e114b4527cbd8deade56ff42250aa7d0116d759ad11497e9f5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class IotTopicRuleHttpHttpHeaderOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.iotTopicRule.IotTopicRuleHttpHttpHeaderOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f1a15933d5a8722d268596a6ea346250d4666ac593626566a0564cb0972575ca)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="keyInput")
    def key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "key"))

    @key.setter
    def key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d9e08f06e6cdae5fc46c18ca6978bb8f9bd9b11baa68eef7ffb68140503aa770)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__29c5a1ed545e7c1d5b594640c758ba0e49bda775fb8fe4f665769778da6a44b9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IotTopicRuleHttpHttpHeader]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IotTopicRuleHttpHttpHeader]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IotTopicRuleHttpHttpHeader]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__37509a7e37c622e3e3bbedb248671bb8048382d2f8f33db8af1266a9d1bb1fdb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class IotTopicRuleHttpList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.iotTopicRule.IotTopicRuleHttpList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e746a50b794be0c43ecb2ef77d94f666b0bae62a19834f8aeabca9ee1d639544)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "IotTopicRuleHttpOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6ad72b3417f0ef3c5a9b1db26d0e07ac9f23a2acf6863446c205025f39dc64dd)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("IotTopicRuleHttpOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__32e9b7da06afa094406085f7662cb7cbc1da4b3a10aee810d7468ea75f825f53)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3a2f38a6e2c4d7a04fe59f8d1121127588742cf910bc7d6866d1a52ead7f3857)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f8b756d651745b6f8931069d2d4fec1f702cd278ef56918226be07fbdf360f37)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotTopicRuleHttp]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotTopicRuleHttp]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotTopicRuleHttp]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f0d229974f062af3e75a2cd481be2f547be21a3e81aaea5d1a40f7f8807e7631)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class IotTopicRuleHttpOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.iotTopicRule.IotTopicRuleHttpOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__85e7df63b8dcbc1d54574480030be31f7f69014577f19352ba951599eb8b1646)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putHttpHeader")
    def put_http_header(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[IotTopicRuleHttpHttpHeader, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d550a67f0b051e890ef192632772dba92ffb047e9d70da1ab5d5516aa1c8aab0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putHttpHeader", [value]))

    @jsii.member(jsii_name="resetConfirmationUrl")
    def reset_confirmation_url(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConfirmationUrl", []))

    @jsii.member(jsii_name="resetHttpHeader")
    def reset_http_header(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHttpHeader", []))

    @builtins.property
    @jsii.member(jsii_name="httpHeader")
    def http_header(self) -> IotTopicRuleHttpHttpHeaderList:
        return typing.cast(IotTopicRuleHttpHttpHeaderList, jsii.get(self, "httpHeader"))

    @builtins.property
    @jsii.member(jsii_name="confirmationUrlInput")
    def confirmation_url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "confirmationUrlInput"))

    @builtins.property
    @jsii.member(jsii_name="httpHeaderInput")
    def http_header_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotTopicRuleHttpHttpHeader]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotTopicRuleHttpHttpHeader]]], jsii.get(self, "httpHeaderInput"))

    @builtins.property
    @jsii.member(jsii_name="urlInput")
    def url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "urlInput"))

    @builtins.property
    @jsii.member(jsii_name="confirmationUrl")
    def confirmation_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "confirmationUrl"))

    @confirmation_url.setter
    def confirmation_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cef607251c4e17e8e9bdd7e6daa961d386a265d8c611b022af76dd7313b4a691)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "confirmationUrl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="url")
    def url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "url"))

    @url.setter
    def url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d09fbc02f28e25a4a9f41f3721b06d1881f471fd883c66c97891950ac568e5db)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "url", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IotTopicRuleHttp]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IotTopicRuleHttp]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IotTopicRuleHttp]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__036e72a6b9a8997134dcd7df2f9bd808d1dd5805dc0c6418994e869471719fbd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.iotTopicRule.IotTopicRuleIotAnalytics",
    jsii_struct_bases=[],
    name_mapping={
        "channel_name": "channelName",
        "role_arn": "roleArn",
        "batch_mode": "batchMode",
    },
)
class IotTopicRuleIotAnalytics:
    def __init__(
        self,
        *,
        channel_name: builtins.str,
        role_arn: builtins.str,
        batch_mode: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param channel_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#channel_name IotTopicRule#channel_name}.
        :param role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#role_arn IotTopicRule#role_arn}.
        :param batch_mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#batch_mode IotTopicRule#batch_mode}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1acf89f79d408b274ae5967e6b763d40db11503039a6aebec89d8bb37930785c)
            check_type(argname="argument channel_name", value=channel_name, expected_type=type_hints["channel_name"])
            check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
            check_type(argname="argument batch_mode", value=batch_mode, expected_type=type_hints["batch_mode"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "channel_name": channel_name,
            "role_arn": role_arn,
        }
        if batch_mode is not None:
            self._values["batch_mode"] = batch_mode

    @builtins.property
    def channel_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#channel_name IotTopicRule#channel_name}.'''
        result = self._values.get("channel_name")
        assert result is not None, "Required property 'channel_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def role_arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#role_arn IotTopicRule#role_arn}.'''
        result = self._values.get("role_arn")
        assert result is not None, "Required property 'role_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def batch_mode(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#batch_mode IotTopicRule#batch_mode}.'''
        result = self._values.get("batch_mode")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IotTopicRuleIotAnalytics(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class IotTopicRuleIotAnalyticsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.iotTopicRule.IotTopicRuleIotAnalyticsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b78895159e3231756c8376cf5d85bf11dbda1937d004dd2d603cdbb243ee955c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "IotTopicRuleIotAnalyticsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a41c7dd6679b1c5be29b6f58f5913f1764b430ff95f2df08a8a435a7103309df)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("IotTopicRuleIotAnalyticsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0b042196e20d437a01a53b01fa0369216ef8814ecea0a259711649f359ff6e98)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5952699a1aee4491c694007b80ba19ebe607561cf2f929ca39b2eefc8bd08540)
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
            type_hints = typing.get_type_hints(_typecheckingstub__09e2be84255838cb72ac08cab2eafb67da0862571049d9870cf7321db069c59e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotTopicRuleIotAnalytics]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotTopicRuleIotAnalytics]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotTopicRuleIotAnalytics]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a334f35249b0fcdc2406292cf31915fb8ff1fb7907246ce2391684985c7eaccb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class IotTopicRuleIotAnalyticsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.iotTopicRule.IotTopicRuleIotAnalyticsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__114ce77b3d84f21f4edfb668e07eb8a1e855a767866401203f075c65e7838f37)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetBatchMode")
    def reset_batch_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBatchMode", []))

    @builtins.property
    @jsii.member(jsii_name="batchModeInput")
    def batch_mode_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "batchModeInput"))

    @builtins.property
    @jsii.member(jsii_name="channelNameInput")
    def channel_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "channelNameInput"))

    @builtins.property
    @jsii.member(jsii_name="roleArnInput")
    def role_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "roleArnInput"))

    @builtins.property
    @jsii.member(jsii_name="batchMode")
    def batch_mode(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "batchMode"))

    @batch_mode.setter
    def batch_mode(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5cd441144845f04ccc3114cf7550568a72446945e971c49e48e8f34d289ec04c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "batchMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="channelName")
    def channel_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "channelName"))

    @channel_name.setter
    def channel_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9694ba7a400a3412577f18bac0dc378c9f91aa71fb20c6ed8f0c0acf47ab7dc5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "channelName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="roleArn")
    def role_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "roleArn"))

    @role_arn.setter
    def role_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__14765ae0f13d1aee6f032868eb018654490ebbf995f141d61947fac140071106)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "roleArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IotTopicRuleIotAnalytics]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IotTopicRuleIotAnalytics]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IotTopicRuleIotAnalytics]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__10dc05a64531bb23b6a8cdf66dcb710363bd630b5394d8d93c781570b283968b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.iotTopicRule.IotTopicRuleIotEvents",
    jsii_struct_bases=[],
    name_mapping={
        "input_name": "inputName",
        "role_arn": "roleArn",
        "batch_mode": "batchMode",
        "message_id": "messageId",
    },
)
class IotTopicRuleIotEvents:
    def __init__(
        self,
        *,
        input_name: builtins.str,
        role_arn: builtins.str,
        batch_mode: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        message_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param input_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#input_name IotTopicRule#input_name}.
        :param role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#role_arn IotTopicRule#role_arn}.
        :param batch_mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#batch_mode IotTopicRule#batch_mode}.
        :param message_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#message_id IotTopicRule#message_id}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aeff6e9656d7547f81022f8d1a99aa1943253ce3d900767f1fe71b16be240fe4)
            check_type(argname="argument input_name", value=input_name, expected_type=type_hints["input_name"])
            check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
            check_type(argname="argument batch_mode", value=batch_mode, expected_type=type_hints["batch_mode"])
            check_type(argname="argument message_id", value=message_id, expected_type=type_hints["message_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "input_name": input_name,
            "role_arn": role_arn,
        }
        if batch_mode is not None:
            self._values["batch_mode"] = batch_mode
        if message_id is not None:
            self._values["message_id"] = message_id

    @builtins.property
    def input_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#input_name IotTopicRule#input_name}.'''
        result = self._values.get("input_name")
        assert result is not None, "Required property 'input_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def role_arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#role_arn IotTopicRule#role_arn}.'''
        result = self._values.get("role_arn")
        assert result is not None, "Required property 'role_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def batch_mode(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#batch_mode IotTopicRule#batch_mode}.'''
        result = self._values.get("batch_mode")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def message_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#message_id IotTopicRule#message_id}.'''
        result = self._values.get("message_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IotTopicRuleIotEvents(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class IotTopicRuleIotEventsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.iotTopicRule.IotTopicRuleIotEventsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__def002fd30694e7233cf79bb1cd6fb0f7716dc4b80a12f29838a0894930ad32d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "IotTopicRuleIotEventsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__880f7e07d545515147db0349f63a5c5047aabe00062d31f8b5a890842de92056)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("IotTopicRuleIotEventsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4b612806ba8b8026a2fb0ff1c5ed7672c612811bd21d78f365c834b6f9b0ab81)
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
            type_hints = typing.get_type_hints(_typecheckingstub__101f2b4fc26b130dc7acd8d453f5bddc425d3243c3d99c3677544aa3efab1f42)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8f2ad6bf560c0761f7c9e61603d55653f366a8f7c1ee1ba6ef346f8cab842be5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotTopicRuleIotEvents]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotTopicRuleIotEvents]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotTopicRuleIotEvents]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__892b7b19483c9d794634cf2a0d0fd34e27c4ad38a55fdeeafdd32b76db099a4e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class IotTopicRuleIotEventsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.iotTopicRule.IotTopicRuleIotEventsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fd0766f6578011c35afc07a5d4802eea591bc289b13ec684b62de7678bc8c84e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetBatchMode")
    def reset_batch_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBatchMode", []))

    @jsii.member(jsii_name="resetMessageId")
    def reset_message_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMessageId", []))

    @builtins.property
    @jsii.member(jsii_name="batchModeInput")
    def batch_mode_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "batchModeInput"))

    @builtins.property
    @jsii.member(jsii_name="inputNameInput")
    def input_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "inputNameInput"))

    @builtins.property
    @jsii.member(jsii_name="messageIdInput")
    def message_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "messageIdInput"))

    @builtins.property
    @jsii.member(jsii_name="roleArnInput")
    def role_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "roleArnInput"))

    @builtins.property
    @jsii.member(jsii_name="batchMode")
    def batch_mode(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "batchMode"))

    @batch_mode.setter
    def batch_mode(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d3cd1977b7269de584d909ef59bbf415511eb78afa564d69c4c2d1bf9cc7636c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "batchMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="inputName")
    def input_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "inputName"))

    @input_name.setter
    def input_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3bb4e0045e0973228567a91481f5b68d1c499614ff0b8d97749e408ecfd138e6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "inputName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="messageId")
    def message_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "messageId"))

    @message_id.setter
    def message_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__30fb9bd6daac8266013a23ad7930dfa9b088ca50a855e74a2dd1c6944937b8ba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "messageId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="roleArn")
    def role_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "roleArn"))

    @role_arn.setter
    def role_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__96dfaaa3a03da07e3dc083411d66f9a6d1d930b95eebcf4443c5fedc76a7fef9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "roleArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IotTopicRuleIotEvents]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IotTopicRuleIotEvents]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IotTopicRuleIotEvents]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce077b5b3797497c6ac8e4c099604f4f056223f4c03c701a901434b1561651bc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.iotTopicRule.IotTopicRuleKafka",
    jsii_struct_bases=[],
    name_mapping={
        "client_properties": "clientProperties",
        "destination_arn": "destinationArn",
        "topic": "topic",
        "header": "header",
        "key": "key",
        "partition": "partition",
    },
)
class IotTopicRuleKafka:
    def __init__(
        self,
        *,
        client_properties: typing.Mapping[builtins.str, builtins.str],
        destination_arn: builtins.str,
        topic: builtins.str,
        header: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["IotTopicRuleKafkaHeader", typing.Dict[builtins.str, typing.Any]]]]] = None,
        key: typing.Optional[builtins.str] = None,
        partition: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param client_properties: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#client_properties IotTopicRule#client_properties}.
        :param destination_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#destination_arn IotTopicRule#destination_arn}.
        :param topic: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#topic IotTopicRule#topic}.
        :param header: header block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#header IotTopicRule#header}
        :param key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#key IotTopicRule#key}.
        :param partition: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#partition IotTopicRule#partition}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a420929f6d1e25cac17b8e20ed8e24f94fdc5410ace45789faf10cf6aa96a166)
            check_type(argname="argument client_properties", value=client_properties, expected_type=type_hints["client_properties"])
            check_type(argname="argument destination_arn", value=destination_arn, expected_type=type_hints["destination_arn"])
            check_type(argname="argument topic", value=topic, expected_type=type_hints["topic"])
            check_type(argname="argument header", value=header, expected_type=type_hints["header"])
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument partition", value=partition, expected_type=type_hints["partition"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "client_properties": client_properties,
            "destination_arn": destination_arn,
            "topic": topic,
        }
        if header is not None:
            self._values["header"] = header
        if key is not None:
            self._values["key"] = key
        if partition is not None:
            self._values["partition"] = partition

    @builtins.property
    def client_properties(self) -> typing.Mapping[builtins.str, builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#client_properties IotTopicRule#client_properties}.'''
        result = self._values.get("client_properties")
        assert result is not None, "Required property 'client_properties' is missing"
        return typing.cast(typing.Mapping[builtins.str, builtins.str], result)

    @builtins.property
    def destination_arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#destination_arn IotTopicRule#destination_arn}.'''
        result = self._values.get("destination_arn")
        assert result is not None, "Required property 'destination_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def topic(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#topic IotTopicRule#topic}.'''
        result = self._values.get("topic")
        assert result is not None, "Required property 'topic' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def header(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["IotTopicRuleKafkaHeader"]]]:
        '''header block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#header IotTopicRule#header}
        '''
        result = self._values.get("header")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["IotTopicRuleKafkaHeader"]]], result)

    @builtins.property
    def key(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#key IotTopicRule#key}.'''
        result = self._values.get("key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def partition(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#partition IotTopicRule#partition}.'''
        result = self._values.get("partition")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IotTopicRuleKafka(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.iotTopicRule.IotTopicRuleKafkaHeader",
    jsii_struct_bases=[],
    name_mapping={"key": "key", "value": "value"},
)
class IotTopicRuleKafkaHeader:
    def __init__(self, *, key: builtins.str, value: builtins.str) -> None:
        '''
        :param key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#key IotTopicRule#key}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#value IotTopicRule#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__25d0681d690b89709549241f10e3923c2991022c3309411b2c1a69a79ae07446)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "key": key,
            "value": value,
        }

    @builtins.property
    def key(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#key IotTopicRule#key}.'''
        result = self._values.get("key")
        assert result is not None, "Required property 'key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#value IotTopicRule#value}.'''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IotTopicRuleKafkaHeader(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class IotTopicRuleKafkaHeaderList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.iotTopicRule.IotTopicRuleKafkaHeaderList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__adadd697a8bd7eac8c48e308365cbb45b27598d4f8a04156f0a1dd200cb298ed)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "IotTopicRuleKafkaHeaderOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f5a893fbc53cf5a5eb302b3a7699804f16343c7f3ff5847c0fadc57156e015c2)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("IotTopicRuleKafkaHeaderOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e7814510af36bd0388f211c58254e0644ea0634a71108bd236b2965ce077bab)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9925b5e3295515359ae2e7855530c9b748505560e6075618e0f80e07b821032c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__270891820abe2987cd5ac7a986495a3d447fbbbdca5bb504c8b1b0237d26e0b0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotTopicRuleKafkaHeader]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotTopicRuleKafkaHeader]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotTopicRuleKafkaHeader]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__279dbe30f4208bd28f9147f83b69224c898ee70798e9760fa81a0e59b1f6930d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class IotTopicRuleKafkaHeaderOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.iotTopicRule.IotTopicRuleKafkaHeaderOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4cbd9aa2d8798cbbf3e992aec7225a4acc411bfc0240c56b8f449cb6f05f3fe4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="keyInput")
    def key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "key"))

    @key.setter
    def key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__10de02a0f59e8a68383e628ff583727942295a70c299b493484b2a8740f0fe22)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ba82e8f800afd469bbcdf317e8d60d9e748375c78fbac1ffee1665a27fcdf1b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IotTopicRuleKafkaHeader]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IotTopicRuleKafkaHeader]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IotTopicRuleKafkaHeader]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__793319732c41af1f0a4a816c626c5887f40799e0f50202a7ef883f9fb3b2d41e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class IotTopicRuleKafkaList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.iotTopicRule.IotTopicRuleKafkaList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ef5ddfcc2a6a149a9d1324d31e9d72a6cf6de397e0e40665b33aa4dd5d7fe2de)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "IotTopicRuleKafkaOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9fae381e6b362edab0a2916ad952523cd2b9d896134d843f5ebd7170accd5d10)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("IotTopicRuleKafkaOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cceb81dda95a2781d6fc2e89e28d2d08e46690b4dbfa427b4dcdecf4c4d3f77c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7ea111d39843d2a9e03714325cdff315a35fb00f1759411a290cf3b687d0f131)
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
            type_hints = typing.get_type_hints(_typecheckingstub__96e6fed207fa57d74716da3d7f4ae736efb29c6254dd2ee3903707bc2ab3deb8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotTopicRuleKafka]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotTopicRuleKafka]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotTopicRuleKafka]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1eebbed7424610481a2094a0172d936ab9d51e8f9ab768d74a735787c49548ba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class IotTopicRuleKafkaOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.iotTopicRule.IotTopicRuleKafkaOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ed1248b399c98113e2e41c70c2418aa026a007f9594dc548da4766c36360ba2a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putHeader")
    def put_header(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[IotTopicRuleKafkaHeader, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9876d62d9567165ca90caef0356e5a9235447b8611959d620874ca253f0bec7f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putHeader", [value]))

    @jsii.member(jsii_name="resetHeader")
    def reset_header(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHeader", []))

    @jsii.member(jsii_name="resetKey")
    def reset_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKey", []))

    @jsii.member(jsii_name="resetPartition")
    def reset_partition(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPartition", []))

    @builtins.property
    @jsii.member(jsii_name="header")
    def header(self) -> IotTopicRuleKafkaHeaderList:
        return typing.cast(IotTopicRuleKafkaHeaderList, jsii.get(self, "header"))

    @builtins.property
    @jsii.member(jsii_name="clientPropertiesInput")
    def client_properties_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "clientPropertiesInput"))

    @builtins.property
    @jsii.member(jsii_name="destinationArnInput")
    def destination_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "destinationArnInput"))

    @builtins.property
    @jsii.member(jsii_name="headerInput")
    def header_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotTopicRuleKafkaHeader]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotTopicRuleKafkaHeader]]], jsii.get(self, "headerInput"))

    @builtins.property
    @jsii.member(jsii_name="keyInput")
    def key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyInput"))

    @builtins.property
    @jsii.member(jsii_name="partitionInput")
    def partition_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "partitionInput"))

    @builtins.property
    @jsii.member(jsii_name="topicInput")
    def topic_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "topicInput"))

    @builtins.property
    @jsii.member(jsii_name="clientProperties")
    def client_properties(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "clientProperties"))

    @client_properties.setter
    def client_properties(
        self,
        value: typing.Mapping[builtins.str, builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d18e62d8102228baed8ab17ea9a475f7a17ebf7c5442b9779444bf04ee82cb5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientProperties", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="destinationArn")
    def destination_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "destinationArn"))

    @destination_arn.setter
    def destination_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__48b7a2461b163506fab8f19d747a3b96f7c542eb397f65ed2f42e581de392bca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "destinationArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "key"))

    @key.setter
    def key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__87cb32d4570ad3cb83494ccd78f6b23f46a477bb4d127435c4bc88f049d3e8ef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="partition")
    def partition(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "partition"))

    @partition.setter
    def partition(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b29a2924c8af3a49721358b0c955eb9530cb355ea838f0693e47cf611f26695)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "partition", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="topic")
    def topic(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "topic"))

    @topic.setter
    def topic(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3dc5ee960bc7a30255caef46ac350b4bcf4786577e9171102e5d44b8a782c039)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "topic", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IotTopicRuleKafka]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IotTopicRuleKafka]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IotTopicRuleKafka]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__811e83960191fafb13d93f83e143f80263a84dc77d48a79ade67f7585a01265c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.iotTopicRule.IotTopicRuleKinesis",
    jsii_struct_bases=[],
    name_mapping={
        "role_arn": "roleArn",
        "stream_name": "streamName",
        "partition_key": "partitionKey",
    },
)
class IotTopicRuleKinesis:
    def __init__(
        self,
        *,
        role_arn: builtins.str,
        stream_name: builtins.str,
        partition_key: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#role_arn IotTopicRule#role_arn}.
        :param stream_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#stream_name IotTopicRule#stream_name}.
        :param partition_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#partition_key IotTopicRule#partition_key}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__062385a302701e6a2156135f177b9b337064838f46ad3cdc3f954ee38d02a482)
            check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
            check_type(argname="argument stream_name", value=stream_name, expected_type=type_hints["stream_name"])
            check_type(argname="argument partition_key", value=partition_key, expected_type=type_hints["partition_key"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "role_arn": role_arn,
            "stream_name": stream_name,
        }
        if partition_key is not None:
            self._values["partition_key"] = partition_key

    @builtins.property
    def role_arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#role_arn IotTopicRule#role_arn}.'''
        result = self._values.get("role_arn")
        assert result is not None, "Required property 'role_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def stream_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#stream_name IotTopicRule#stream_name}.'''
        result = self._values.get("stream_name")
        assert result is not None, "Required property 'stream_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def partition_key(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#partition_key IotTopicRule#partition_key}.'''
        result = self._values.get("partition_key")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IotTopicRuleKinesis(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class IotTopicRuleKinesisList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.iotTopicRule.IotTopicRuleKinesisList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c59616133323149c17d1530f2e12ff95abbbc5c917a16b4c022655335f000082)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "IotTopicRuleKinesisOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__becf579c1bd05084bba0af79adefe1d2ac65fd06269d9526680c6fbc434b2391)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("IotTopicRuleKinesisOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b5d2dfb20848ed84fd3c49f776fd9b453efa16bc92305486012d52e706213c0e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b81c457dcf50188550e0d02990402c3b779cf3ac358c7555ada6f8fc837a1001)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0b668fcbd77f093393e64406b21b96bf8cbf0aaf5a010c8fa34c423d27046a43)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotTopicRuleKinesis]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotTopicRuleKinesis]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotTopicRuleKinesis]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__50833ef6f1cdd625d6ee5484fabd38a200b5f5fa14fc2eb8d7b82f0159facfb8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class IotTopicRuleKinesisOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.iotTopicRule.IotTopicRuleKinesisOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__09a8015b4eb688b3a57bb7581a2474636bb02d0261ba4ba38f5aa1f8ed143490)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetPartitionKey")
    def reset_partition_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPartitionKey", []))

    @builtins.property
    @jsii.member(jsii_name="partitionKeyInput")
    def partition_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "partitionKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="roleArnInput")
    def role_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "roleArnInput"))

    @builtins.property
    @jsii.member(jsii_name="streamNameInput")
    def stream_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "streamNameInput"))

    @builtins.property
    @jsii.member(jsii_name="partitionKey")
    def partition_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "partitionKey"))

    @partition_key.setter
    def partition_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aec69ef14d4df6404eebecac945451ffd4eed8227419e83b61f4789029c7cebe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "partitionKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="roleArn")
    def role_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "roleArn"))

    @role_arn.setter
    def role_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a5aa8a532cc2f92331083a4eabb6d96cabd4283b08e80999a898a39f96e1f9b4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "roleArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="streamName")
    def stream_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "streamName"))

    @stream_name.setter
    def stream_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__579bee74dc3aa791fb656746baf324f0b9288e6f36211ae7c7f795b3ed7abf1a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "streamName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IotTopicRuleKinesis]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IotTopicRuleKinesis]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IotTopicRuleKinesis]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8c5e8af74d58dda39300c013e04b4e912ecc78dd471e9a598ee050730f1108c0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.iotTopicRule.IotTopicRuleLambda",
    jsii_struct_bases=[],
    name_mapping={"function_arn": "functionArn"},
)
class IotTopicRuleLambda:
    def __init__(self, *, function_arn: builtins.str) -> None:
        '''
        :param function_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#function_arn IotTopicRule#function_arn}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__84e7b3a0537f489d04dfd1b914e393a11a109c4d3fe34cccb51445de35d3adf3)
            check_type(argname="argument function_arn", value=function_arn, expected_type=type_hints["function_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "function_arn": function_arn,
        }

    @builtins.property
    def function_arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#function_arn IotTopicRule#function_arn}.'''
        result = self._values.get("function_arn")
        assert result is not None, "Required property 'function_arn' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IotTopicRuleLambda(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class IotTopicRuleLambdaList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.iotTopicRule.IotTopicRuleLambdaList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__dfb35d19ddd5bfd955aa43ca0fbc16378bf3ddb4c59e3b17a000e711fa46a863)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "IotTopicRuleLambdaOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e7f7e130c45283b58dc229ca5a5ea4394760a2ddb0cbb5a5388f2bc99320c1e3)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("IotTopicRuleLambdaOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c046fc1824325e9e68f6389ac90e5434c00785b5ff2b69753bb2076da7aaa141)
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
            type_hints = typing.get_type_hints(_typecheckingstub__39291bcce80a45d818676ccd4fe3705652151caba4baafe9c0cd1b0813128f23)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f59ceef137dc4e12098dcef39887a32f704dd48d08ea8d0154191455275428e8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotTopicRuleLambda]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotTopicRuleLambda]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotTopicRuleLambda]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eabd6e3ce34589309d680a7eaf8c75924ea2318b3abcfa5d0f012a634dde0776)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class IotTopicRuleLambdaOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.iotTopicRule.IotTopicRuleLambdaOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__643699ec2dc6868e56f0033ec40d9d20dc07d3b5f782bcfd334727a1acb48248)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="functionArnInput")
    def function_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "functionArnInput"))

    @builtins.property
    @jsii.member(jsii_name="functionArn")
    def function_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "functionArn"))

    @function_arn.setter
    def function_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__60e7451b07f4db559f8e555641bcbe82f7a12fe058709faecc85e126d999ef14)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "functionArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IotTopicRuleLambda]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IotTopicRuleLambda]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IotTopicRuleLambda]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8b6b55888e1677887ac01cf25f6804162f3c900b99bec3523d79f44fdde6417f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.iotTopicRule.IotTopicRuleRepublish",
    jsii_struct_bases=[],
    name_mapping={"role_arn": "roleArn", "topic": "topic", "qos": "qos"},
)
class IotTopicRuleRepublish:
    def __init__(
        self,
        *,
        role_arn: builtins.str,
        topic: builtins.str,
        qos: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#role_arn IotTopicRule#role_arn}.
        :param topic: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#topic IotTopicRule#topic}.
        :param qos: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#qos IotTopicRule#qos}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1cb8cbb0bc8a283ba49a3854d9eb0fb622b2a8e6fcabb701df589d4b809efd56)
            check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
            check_type(argname="argument topic", value=topic, expected_type=type_hints["topic"])
            check_type(argname="argument qos", value=qos, expected_type=type_hints["qos"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "role_arn": role_arn,
            "topic": topic,
        }
        if qos is not None:
            self._values["qos"] = qos

    @builtins.property
    def role_arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#role_arn IotTopicRule#role_arn}.'''
        result = self._values.get("role_arn")
        assert result is not None, "Required property 'role_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def topic(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#topic IotTopicRule#topic}.'''
        result = self._values.get("topic")
        assert result is not None, "Required property 'topic' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def qos(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#qos IotTopicRule#qos}.'''
        result = self._values.get("qos")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IotTopicRuleRepublish(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class IotTopicRuleRepublishList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.iotTopicRule.IotTopicRuleRepublishList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__35beaab1d030efd7319396d103d69292be2614d8402f3c599cf74d7c62623cee)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "IotTopicRuleRepublishOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c7020105450733742cd7655f130de697c3a9e06c194614bf44e783955e15457a)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("IotTopicRuleRepublishOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d1eba2d6ed5958efc283b28944a6123b81d00734acceb2e0c6582fb6aa1c120a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2a211f53d99dd5bf4b76c97cfd35926c738f083ab72161d0425f63f74a0854e1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__874ad9b4fc46a8f0797da9da9b1ead20fb21f2e4a1323299472385ce4022bd70)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotTopicRuleRepublish]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotTopicRuleRepublish]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotTopicRuleRepublish]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2df5ec5c78f6364d3877893853d168031f78861ddc6ae30957f1872737cb460c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class IotTopicRuleRepublishOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.iotTopicRule.IotTopicRuleRepublishOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__87df998ab5f692926bafaf3700e429e046630c353e789bbb32dbf751c567b602)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetQos")
    def reset_qos(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetQos", []))

    @builtins.property
    @jsii.member(jsii_name="qosInput")
    def qos_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "qosInput"))

    @builtins.property
    @jsii.member(jsii_name="roleArnInput")
    def role_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "roleArnInput"))

    @builtins.property
    @jsii.member(jsii_name="topicInput")
    def topic_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "topicInput"))

    @builtins.property
    @jsii.member(jsii_name="qos")
    def qos(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "qos"))

    @qos.setter
    def qos(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6a3165dac74885a66eaa73d3c7b77b06901bca48b025bd08a333e040fbf53e77)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "qos", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="roleArn")
    def role_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "roleArn"))

    @role_arn.setter
    def role_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e755b94197fa41473202e7aa6661772032e7a27920963929ca463f65ea0578a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "roleArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="topic")
    def topic(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "topic"))

    @topic.setter
    def topic(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ef89fe3fcd1c53306caf557ce1856817601db083efeec144e98e22b17e36cb41)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "topic", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IotTopicRuleRepublish]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IotTopicRuleRepublish]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IotTopicRuleRepublish]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c215249cbda990d781e3a502a924adc052132a487a5894ee5d2fe1f930e1ef5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.iotTopicRule.IotTopicRuleS3",
    jsii_struct_bases=[],
    name_mapping={
        "bucket_name": "bucketName",
        "key": "key",
        "role_arn": "roleArn",
        "canned_acl": "cannedAcl",
    },
)
class IotTopicRuleS3:
    def __init__(
        self,
        *,
        bucket_name: builtins.str,
        key: builtins.str,
        role_arn: builtins.str,
        canned_acl: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param bucket_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#bucket_name IotTopicRule#bucket_name}.
        :param key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#key IotTopicRule#key}.
        :param role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#role_arn IotTopicRule#role_arn}.
        :param canned_acl: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#canned_acl IotTopicRule#canned_acl}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a4a09c9b8cc7e35ca17f0a9286ec3f59731bcc7198e7d281eb4ab2a75d688283)
            check_type(argname="argument bucket_name", value=bucket_name, expected_type=type_hints["bucket_name"])
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
            check_type(argname="argument canned_acl", value=canned_acl, expected_type=type_hints["canned_acl"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "bucket_name": bucket_name,
            "key": key,
            "role_arn": role_arn,
        }
        if canned_acl is not None:
            self._values["canned_acl"] = canned_acl

    @builtins.property
    def bucket_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#bucket_name IotTopicRule#bucket_name}.'''
        result = self._values.get("bucket_name")
        assert result is not None, "Required property 'bucket_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def key(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#key IotTopicRule#key}.'''
        result = self._values.get("key")
        assert result is not None, "Required property 'key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def role_arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#role_arn IotTopicRule#role_arn}.'''
        result = self._values.get("role_arn")
        assert result is not None, "Required property 'role_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def canned_acl(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#canned_acl IotTopicRule#canned_acl}.'''
        result = self._values.get("canned_acl")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IotTopicRuleS3(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class IotTopicRuleS3List(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.iotTopicRule.IotTopicRuleS3List",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b0280766fc39d7bdc6b610345b334639c0aab4178991fbadbbe7c56fec9d4e38)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "IotTopicRuleS3OutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__26a617da386fa36d707e4e33ddee2042a3d58545f2faa35e69168433fe9e7399)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("IotTopicRuleS3OutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__441f899d3ca2c8bc4126d502a43780d856eec26dccfdd2363a53d4aee6a5a4ec)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d3fc97e6048e5390539cad97adc5eb7ea9cbefb2d1e7128918b636aaa1f32ba6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ae3ef95f375ff8d285d6d9185bd1635d27ef6af65b0944c68dc7177292e0ba24)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotTopicRuleS3]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotTopicRuleS3]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotTopicRuleS3]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a3ad80abe39885dc08e4acc6819c0eef5a00f05fd60c6432c2b3b089109d9127)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class IotTopicRuleS3OutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.iotTopicRule.IotTopicRuleS3OutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0727da25686dd666ad96bc620c6f93f9c53594b57ad37978aca7b5daa643b9ba)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetCannedAcl")
    def reset_canned_acl(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCannedAcl", []))

    @builtins.property
    @jsii.member(jsii_name="bucketNameInput")
    def bucket_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bucketNameInput"))

    @builtins.property
    @jsii.member(jsii_name="cannedAclInput")
    def canned_acl_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cannedAclInput"))

    @builtins.property
    @jsii.member(jsii_name="keyInput")
    def key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyInput"))

    @builtins.property
    @jsii.member(jsii_name="roleArnInput")
    def role_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "roleArnInput"))

    @builtins.property
    @jsii.member(jsii_name="bucketName")
    def bucket_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bucketName"))

    @bucket_name.setter
    def bucket_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2dda05853d79bb63a301294a7080a14a02a1b59494b1c27dc8ecc60c83fa8cad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bucketName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="cannedAcl")
    def canned_acl(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cannedAcl"))

    @canned_acl.setter
    def canned_acl(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__665e4945c5fd322f919d5118699ccf16cef90bbcfd6b26b61290c1714c03e9e4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cannedAcl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "key"))

    @key.setter
    def key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4eac30268a29a4549d6d4423f9294ca4fc5f180a9604e4280a4de83fcb36a7cd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="roleArn")
    def role_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "roleArn"))

    @role_arn.setter
    def role_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e57294801010771cf6c7c203c7a8a7452ebee9899fa135e9eec73c0350e4df0e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "roleArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IotTopicRuleS3]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IotTopicRuleS3]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IotTopicRuleS3]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e9d1ffbfeff2a0e42933364f4a265f573f2c612454485256feaa5bbcfc477a8b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.iotTopicRule.IotTopicRuleSns",
    jsii_struct_bases=[],
    name_mapping={
        "role_arn": "roleArn",
        "target_arn": "targetArn",
        "message_format": "messageFormat",
    },
)
class IotTopicRuleSns:
    def __init__(
        self,
        *,
        role_arn: builtins.str,
        target_arn: builtins.str,
        message_format: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#role_arn IotTopicRule#role_arn}.
        :param target_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#target_arn IotTopicRule#target_arn}.
        :param message_format: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#message_format IotTopicRule#message_format}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3dd8545051208d4cf8fd4be5be794c494d937a8f172a1c8d54592fdbbfa89e7c)
            check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
            check_type(argname="argument target_arn", value=target_arn, expected_type=type_hints["target_arn"])
            check_type(argname="argument message_format", value=message_format, expected_type=type_hints["message_format"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "role_arn": role_arn,
            "target_arn": target_arn,
        }
        if message_format is not None:
            self._values["message_format"] = message_format

    @builtins.property
    def role_arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#role_arn IotTopicRule#role_arn}.'''
        result = self._values.get("role_arn")
        assert result is not None, "Required property 'role_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def target_arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#target_arn IotTopicRule#target_arn}.'''
        result = self._values.get("target_arn")
        assert result is not None, "Required property 'target_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def message_format(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#message_format IotTopicRule#message_format}.'''
        result = self._values.get("message_format")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IotTopicRuleSns(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class IotTopicRuleSnsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.iotTopicRule.IotTopicRuleSnsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__aaa6c30505948fedc87312903160863197a4bac2c9595f6624a3e5b89cecf967)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "IotTopicRuleSnsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2bdab9c72d230aa483bbc82392c4202f89067bec505bc3490eda36c48d9be97a)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("IotTopicRuleSnsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0fa9eef7adc7dc88acb544fa217c59a4fa51276682e23f5f06a076af54202ae8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f7f67825877be63195323021fa1869aa0e9816ac6065c6f13ced19371b4e6cc7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ca96bacd1c1d03054d7ae5cab349d336050bf7e7c9b42e3f28b5bf811c1e9fa1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotTopicRuleSns]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotTopicRuleSns]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotTopicRuleSns]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d51b8701dd4019f17f6d6b9ab7be0581637aa53459e7f8f6e3ee3d4d5091a106)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class IotTopicRuleSnsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.iotTopicRule.IotTopicRuleSnsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__17ab219720df1de953b74fe6a03ad77dcb91b6483b4111669e104e2b8ef2631d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetMessageFormat")
    def reset_message_format(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMessageFormat", []))

    @builtins.property
    @jsii.member(jsii_name="messageFormatInput")
    def message_format_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "messageFormatInput"))

    @builtins.property
    @jsii.member(jsii_name="roleArnInput")
    def role_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "roleArnInput"))

    @builtins.property
    @jsii.member(jsii_name="targetArnInput")
    def target_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "targetArnInput"))

    @builtins.property
    @jsii.member(jsii_name="messageFormat")
    def message_format(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "messageFormat"))

    @message_format.setter
    def message_format(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e1d6a228bc0298bc359cefb6c5352c24ad33f221c5ae078b80ca36251e3517e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "messageFormat", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="roleArn")
    def role_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "roleArn"))

    @role_arn.setter
    def role_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f5fcf9b617f87b8389663fa505bd33e445e4ec0588b220f5436e97cfc6c6c43d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "roleArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="targetArn")
    def target_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "targetArn"))

    @target_arn.setter
    def target_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0983f86413cbc80a67f5ea729fcec65c10fb57f0eadb450d1bfcd8d20a021bd7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "targetArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IotTopicRuleSns]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IotTopicRuleSns]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IotTopicRuleSns]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e9a16f448b7b7e99b72183f6e821283f85981c71c03af5edcba2d547d5e6223c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.iotTopicRule.IotTopicRuleSqs",
    jsii_struct_bases=[],
    name_mapping={
        "queue_url": "queueUrl",
        "role_arn": "roleArn",
        "use_base64": "useBase64",
    },
)
class IotTopicRuleSqs:
    def __init__(
        self,
        *,
        queue_url: builtins.str,
        role_arn: builtins.str,
        use_base64: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        '''
        :param queue_url: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#queue_url IotTopicRule#queue_url}.
        :param role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#role_arn IotTopicRule#role_arn}.
        :param use_base64: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#use_base64 IotTopicRule#use_base64}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__87be092475616b2a595901ac2b1ceb45a42327fb8789d611fba9a053c686664e)
            check_type(argname="argument queue_url", value=queue_url, expected_type=type_hints["queue_url"])
            check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
            check_type(argname="argument use_base64", value=use_base64, expected_type=type_hints["use_base64"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "queue_url": queue_url,
            "role_arn": role_arn,
            "use_base64": use_base64,
        }

    @builtins.property
    def queue_url(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#queue_url IotTopicRule#queue_url}.'''
        result = self._values.get("queue_url")
        assert result is not None, "Required property 'queue_url' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def role_arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#role_arn IotTopicRule#role_arn}.'''
        result = self._values.get("role_arn")
        assert result is not None, "Required property 'role_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def use_base64(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#use_base64 IotTopicRule#use_base64}.'''
        result = self._values.get("use_base64")
        assert result is not None, "Required property 'use_base64' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IotTopicRuleSqs(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class IotTopicRuleSqsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.iotTopicRule.IotTopicRuleSqsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__594433d2c8cd7084e8c1a05fd71e0d59ca3a8133f319ac7fd5222c56c356d412)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "IotTopicRuleSqsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd6714795b19aeb1579e4d43ae979fca095ef9746ad76b4dda0fe96558d86a4e)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("IotTopicRuleSqsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c3f664b074f5c5aa7afa3aa638d9f7e18da9e810ffa65fdb0867d0ce5748044)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ecbc1f1772f50fd00aa659a980430ec9605b95e85652393cbfcaa115405425a3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d29a64b2e4cadcf526adbba02b6edf6c662ba8aaada84f78c89185bbaddc7515)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotTopicRuleSqs]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotTopicRuleSqs]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotTopicRuleSqs]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5cea5ce6c73a618cb2f568275c434e105979ce30be3ae8d31e32057e89e3abcf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class IotTopicRuleSqsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.iotTopicRule.IotTopicRuleSqsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9c9f5e8902a2b05ab046a56c3ec3d19d8763f400691870454074703189d6a1cb)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="queueUrlInput")
    def queue_url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "queueUrlInput"))

    @builtins.property
    @jsii.member(jsii_name="roleArnInput")
    def role_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "roleArnInput"))

    @builtins.property
    @jsii.member(jsii_name="useBase64Input")
    def use_base64_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "useBase64Input"))

    @builtins.property
    @jsii.member(jsii_name="queueUrl")
    def queue_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "queueUrl"))

    @queue_url.setter
    def queue_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__75f1d6ca4173a6f7b5bf8f7af0c8d4003204adcd69a199ec9bf7c6005e7f8770)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "queueUrl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="roleArn")
    def role_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "roleArn"))

    @role_arn.setter
    def role_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dbc46ccded0b4bd945d012ff9d3a8b752a85e2163c590d7e58a776df0f2b1a11)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "roleArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="useBase64")
    def use_base64(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "useBase64"))

    @use_base64.setter
    def use_base64(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__80a3474b825487a8a3e0a7cea85880d59e0a3690df7a48f49058893ed7504532)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "useBase64", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IotTopicRuleSqs]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IotTopicRuleSqs]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IotTopicRuleSqs]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ed097d87f222b2ec52400c7283de5b3c894445ff0f391641817742540b39c977)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.iotTopicRule.IotTopicRuleStepFunctions",
    jsii_struct_bases=[],
    name_mapping={
        "role_arn": "roleArn",
        "state_machine_name": "stateMachineName",
        "execution_name_prefix": "executionNamePrefix",
    },
)
class IotTopicRuleStepFunctions:
    def __init__(
        self,
        *,
        role_arn: builtins.str,
        state_machine_name: builtins.str,
        execution_name_prefix: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#role_arn IotTopicRule#role_arn}.
        :param state_machine_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#state_machine_name IotTopicRule#state_machine_name}.
        :param execution_name_prefix: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#execution_name_prefix IotTopicRule#execution_name_prefix}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a791bfa4239d12237434677830c9f9194e5bef70c35dc356b34c685b1e02a296)
            check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
            check_type(argname="argument state_machine_name", value=state_machine_name, expected_type=type_hints["state_machine_name"])
            check_type(argname="argument execution_name_prefix", value=execution_name_prefix, expected_type=type_hints["execution_name_prefix"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "role_arn": role_arn,
            "state_machine_name": state_machine_name,
        }
        if execution_name_prefix is not None:
            self._values["execution_name_prefix"] = execution_name_prefix

    @builtins.property
    def role_arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#role_arn IotTopicRule#role_arn}.'''
        result = self._values.get("role_arn")
        assert result is not None, "Required property 'role_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def state_machine_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#state_machine_name IotTopicRule#state_machine_name}.'''
        result = self._values.get("state_machine_name")
        assert result is not None, "Required property 'state_machine_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def execution_name_prefix(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#execution_name_prefix IotTopicRule#execution_name_prefix}.'''
        result = self._values.get("execution_name_prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IotTopicRuleStepFunctions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class IotTopicRuleStepFunctionsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.iotTopicRule.IotTopicRuleStepFunctionsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__01e43c7a4576626c4260b0f0746f6b45a336572053916f5d180865e6ecfb10c0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "IotTopicRuleStepFunctionsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ad0e869c1335d63e3fcfbe8240aa6fbdbc0ba91f05412941c9037fa27d7496f2)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("IotTopicRuleStepFunctionsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__832ae843de3e059baee0b14984014c3dcf704857aebd399d62d2f63da639f872)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5ba3dcc5bd613962ccc1694d59a2622d8a2724c3390f4aa09c3f4f296ad92344)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ccb4dbcce7ab65e60a3aae96d26c3955f129672c3eec8bdf6412909c96a46bc8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotTopicRuleStepFunctions]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotTopicRuleStepFunctions]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotTopicRuleStepFunctions]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bb06507fef79c324f48420bf29d81519af389f76f62b834a63f72118970ef781)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class IotTopicRuleStepFunctionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.iotTopicRule.IotTopicRuleStepFunctionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a3efd9745cea5f85dd3b4da86d0e4f17d997890bb69be07e127a52de42476d1d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetExecutionNamePrefix")
    def reset_execution_name_prefix(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExecutionNamePrefix", []))

    @builtins.property
    @jsii.member(jsii_name="executionNamePrefixInput")
    def execution_name_prefix_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "executionNamePrefixInput"))

    @builtins.property
    @jsii.member(jsii_name="roleArnInput")
    def role_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "roleArnInput"))

    @builtins.property
    @jsii.member(jsii_name="stateMachineNameInput")
    def state_machine_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "stateMachineNameInput"))

    @builtins.property
    @jsii.member(jsii_name="executionNamePrefix")
    def execution_name_prefix(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "executionNamePrefix"))

    @execution_name_prefix.setter
    def execution_name_prefix(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__92cc29d83a0abc553928215a9b1d6c4a1285ef04f7ee4f43e42fcb112fee6a9f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "executionNamePrefix", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="roleArn")
    def role_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "roleArn"))

    @role_arn.setter
    def role_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e516c173476439356434a328695472b1c712da7240d8cf1ba56b43295699cc94)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "roleArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="stateMachineName")
    def state_machine_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "stateMachineName"))

    @state_machine_name.setter
    def state_machine_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__429ad679b8ca07b2374626e849ed1b43eee5c0839813fdea2e76682005e63a40)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "stateMachineName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IotTopicRuleStepFunctions]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IotTopicRuleStepFunctions]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IotTopicRuleStepFunctions]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c2381b969c7b0ad41a27d834ff539a3447367fe18bc786a25130875ac8ec55d0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.iotTopicRule.IotTopicRuleTimestream",
    jsii_struct_bases=[],
    name_mapping={
        "database_name": "databaseName",
        "dimension": "dimension",
        "role_arn": "roleArn",
        "table_name": "tableName",
        "timestamp": "timestamp",
    },
)
class IotTopicRuleTimestream:
    def __init__(
        self,
        *,
        database_name: builtins.str,
        dimension: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["IotTopicRuleTimestreamDimension", typing.Dict[builtins.str, typing.Any]]]],
        role_arn: builtins.str,
        table_name: builtins.str,
        timestamp: typing.Optional[typing.Union["IotTopicRuleTimestreamTimestamp", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param database_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#database_name IotTopicRule#database_name}.
        :param dimension: dimension block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#dimension IotTopicRule#dimension}
        :param role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#role_arn IotTopicRule#role_arn}.
        :param table_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#table_name IotTopicRule#table_name}.
        :param timestamp: timestamp block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#timestamp IotTopicRule#timestamp}
        '''
        if isinstance(timestamp, dict):
            timestamp = IotTopicRuleTimestreamTimestamp(**timestamp)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__37bf62ba9b3390f2287f2dbe483ded0b2e36329f74ccec7c0e3cee7e1474f156)
            check_type(argname="argument database_name", value=database_name, expected_type=type_hints["database_name"])
            check_type(argname="argument dimension", value=dimension, expected_type=type_hints["dimension"])
            check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
            check_type(argname="argument table_name", value=table_name, expected_type=type_hints["table_name"])
            check_type(argname="argument timestamp", value=timestamp, expected_type=type_hints["timestamp"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "database_name": database_name,
            "dimension": dimension,
            "role_arn": role_arn,
            "table_name": table_name,
        }
        if timestamp is not None:
            self._values["timestamp"] = timestamp

    @builtins.property
    def database_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#database_name IotTopicRule#database_name}.'''
        result = self._values.get("database_name")
        assert result is not None, "Required property 'database_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def dimension(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["IotTopicRuleTimestreamDimension"]]:
        '''dimension block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#dimension IotTopicRule#dimension}
        '''
        result = self._values.get("dimension")
        assert result is not None, "Required property 'dimension' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["IotTopicRuleTimestreamDimension"]], result)

    @builtins.property
    def role_arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#role_arn IotTopicRule#role_arn}.'''
        result = self._values.get("role_arn")
        assert result is not None, "Required property 'role_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def table_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#table_name IotTopicRule#table_name}.'''
        result = self._values.get("table_name")
        assert result is not None, "Required property 'table_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def timestamp(self) -> typing.Optional["IotTopicRuleTimestreamTimestamp"]:
        '''timestamp block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#timestamp IotTopicRule#timestamp}
        '''
        result = self._values.get("timestamp")
        return typing.cast(typing.Optional["IotTopicRuleTimestreamTimestamp"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IotTopicRuleTimestream(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.iotTopicRule.IotTopicRuleTimestreamDimension",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "value": "value"},
)
class IotTopicRuleTimestreamDimension:
    def __init__(self, *, name: builtins.str, value: builtins.str) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#name IotTopicRule#name}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#value IotTopicRule#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dbbf6291fb1070bb7e53cabaf8c4b8625f06aa1bfd2fed4aa9f7ed77ab5a841f)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "value": value,
        }

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#name IotTopicRule#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#value IotTopicRule#value}.'''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IotTopicRuleTimestreamDimension(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class IotTopicRuleTimestreamDimensionList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.iotTopicRule.IotTopicRuleTimestreamDimensionList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7552bbd00412d3918bcd88beaade7fb140a3cc550fa1bf25b2b04e2331209b2d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "IotTopicRuleTimestreamDimensionOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__44a2a1b10f4d5394118ccccabe1213054bf38ff5f85ecf65a645b55dd365e7da)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("IotTopicRuleTimestreamDimensionOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b4193d015b2b3a21dcb91278c7142c229fbc52f823d52dd0f49757a5082f1e06)
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
            type_hints = typing.get_type_hints(_typecheckingstub__dd87436712578b32c2243f3d2721cc1f51bfdccae77fcc5b9ed66f1fc218a691)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c00f5c0f7ae27121a7747e7d0bff8c8b6bbfc30a746088d82906ece46c0b32bc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotTopicRuleTimestreamDimension]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotTopicRuleTimestreamDimension]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotTopicRuleTimestreamDimension]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__97356ca1a16f3ff5f218cd6af81f3e202ec3b79f62521f1d57c0600ce82ba2fe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class IotTopicRuleTimestreamDimensionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.iotTopicRule.IotTopicRuleTimestreamDimensionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__815dfd0b998940e52b7e73c20315d9561e8b24c8b4a9d84e38a0748df0479d78)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7102cb2bb14de0686c2b007b56aca72c06f7e8105f96911c09840ad0cff9fdc6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1660c65a32940b42352eb7fafc6faedb466a7a13dc3a0d38c48c298274140f01)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IotTopicRuleTimestreamDimension]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IotTopicRuleTimestreamDimension]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IotTopicRuleTimestreamDimension]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1dbdc44196665cda518f92fcbfbf3f3dd933a248057af7b374d757f38e9433ef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class IotTopicRuleTimestreamList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.iotTopicRule.IotTopicRuleTimestreamList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2223545299273a6043fbe787cf39d7f0b4ba350dbbd0fc24efc40738348a6ead)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "IotTopicRuleTimestreamOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a51c2ddcd45c0ac23e441063e5b7883a9ad5c8084ad91b19e5506ca23ad9d58)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("IotTopicRuleTimestreamOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__456edab77c14b9d7dea8e61aa3d84de9085d4c68f4a3cea09394da57898849eb)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b8ce3cc0f6e4328f441a68c088cb31701391b55496266a4d2f3b6f239d358c2f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__49b762295fa640cb3a08ccdb522ae268b9e6a9db559e50fdb494d9b7f7b4d7a3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotTopicRuleTimestream]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotTopicRuleTimestream]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotTopicRuleTimestream]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c2b073b051f8b09e033bebd67a0655e5281883a01694cb200aa6bca7624f60c0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class IotTopicRuleTimestreamOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.iotTopicRule.IotTopicRuleTimestreamOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f749026ec5db96778046ccfabdc3204f96528950fdf8f0bd60015665dfd7a5c9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putDimension")
    def put_dimension(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[IotTopicRuleTimestreamDimension, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f7cc6d79a3d1bea5d9ef4753853458d2e0c6ff6b9e66fb7e7bba695ef3285266)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putDimension", [value]))

    @jsii.member(jsii_name="putTimestamp")
    def put_timestamp(self, *, unit: builtins.str, value: builtins.str) -> None:
        '''
        :param unit: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#unit IotTopicRule#unit}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#value IotTopicRule#value}.
        '''
        value_ = IotTopicRuleTimestreamTimestamp(unit=unit, value=value)

        return typing.cast(None, jsii.invoke(self, "putTimestamp", [value_]))

    @jsii.member(jsii_name="resetTimestamp")
    def reset_timestamp(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimestamp", []))

    @builtins.property
    @jsii.member(jsii_name="dimension")
    def dimension(self) -> IotTopicRuleTimestreamDimensionList:
        return typing.cast(IotTopicRuleTimestreamDimensionList, jsii.get(self, "dimension"))

    @builtins.property
    @jsii.member(jsii_name="timestamp")
    def timestamp(self) -> "IotTopicRuleTimestreamTimestampOutputReference":
        return typing.cast("IotTopicRuleTimestreamTimestampOutputReference", jsii.get(self, "timestamp"))

    @builtins.property
    @jsii.member(jsii_name="databaseNameInput")
    def database_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "databaseNameInput"))

    @builtins.property
    @jsii.member(jsii_name="dimensionInput")
    def dimension_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotTopicRuleTimestreamDimension]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotTopicRuleTimestreamDimension]]], jsii.get(self, "dimensionInput"))

    @builtins.property
    @jsii.member(jsii_name="roleArnInput")
    def role_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "roleArnInput"))

    @builtins.property
    @jsii.member(jsii_name="tableNameInput")
    def table_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tableNameInput"))

    @builtins.property
    @jsii.member(jsii_name="timestampInput")
    def timestamp_input(self) -> typing.Optional["IotTopicRuleTimestreamTimestamp"]:
        return typing.cast(typing.Optional["IotTopicRuleTimestreamTimestamp"], jsii.get(self, "timestampInput"))

    @builtins.property
    @jsii.member(jsii_name="databaseName")
    def database_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "databaseName"))

    @database_name.setter
    def database_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__45c07a6f425f5a36e6c19d45b7873c652d8a048b80547f0d39148ad13f76a905)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "databaseName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="roleArn")
    def role_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "roleArn"))

    @role_arn.setter
    def role_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__71e259ff4d73e7afc70b0ca296e49b5728005005f46cbee66452bd7953975f79)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "roleArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tableName")
    def table_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tableName"))

    @table_name.setter
    def table_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__579bbb0f75262734a2484f3522c041000c85f2467f76889489e1257cbb1caf7f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tableName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IotTopicRuleTimestream]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IotTopicRuleTimestream]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IotTopicRuleTimestream]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0fbb26c73307a07ae292db0be29fe7322bf2bfc6311ca949f4d33390d4c17a52)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.iotTopicRule.IotTopicRuleTimestreamTimestamp",
    jsii_struct_bases=[],
    name_mapping={"unit": "unit", "value": "value"},
)
class IotTopicRuleTimestreamTimestamp:
    def __init__(self, *, unit: builtins.str, value: builtins.str) -> None:
        '''
        :param unit: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#unit IotTopicRule#unit}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#value IotTopicRule#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0deb5be66a882a98babc505c71c21d4a35989a29b1d1c495ddfc07f50c138e09)
            check_type(argname="argument unit", value=unit, expected_type=type_hints["unit"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "unit": unit,
            "value": value,
        }

    @builtins.property
    def unit(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#unit IotTopicRule#unit}.'''
        result = self._values.get("unit")
        assert result is not None, "Required property 'unit' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/iot_topic_rule#value IotTopicRule#value}.'''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IotTopicRuleTimestreamTimestamp(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class IotTopicRuleTimestreamTimestampOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.iotTopicRule.IotTopicRuleTimestreamTimestampOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__642cd6aacf6f04dfd726eebf48e34e70179caeafd853f53b6e5a31e4994bf15a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="unitInput")
    def unit_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "unitInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="unit")
    def unit(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "unit"))

    @unit.setter
    def unit(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ca137af8ca309589033bf32d449a5446091ea39cabbaa611ce6aa996d89948e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "unit", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6af01097b751c2c1518fbaadd5365d74b9850a83c8c60010cee0553b5506833a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[IotTopicRuleTimestreamTimestamp]:
        return typing.cast(typing.Optional[IotTopicRuleTimestreamTimestamp], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[IotTopicRuleTimestreamTimestamp],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4edd5db0df430bad3db1f61c0e881162fded813fea9698daf5580b406733c978)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "IotTopicRule",
    "IotTopicRuleCloudwatchAlarm",
    "IotTopicRuleCloudwatchAlarmList",
    "IotTopicRuleCloudwatchAlarmOutputReference",
    "IotTopicRuleCloudwatchLogs",
    "IotTopicRuleCloudwatchLogsList",
    "IotTopicRuleCloudwatchLogsOutputReference",
    "IotTopicRuleCloudwatchMetric",
    "IotTopicRuleCloudwatchMetricList",
    "IotTopicRuleCloudwatchMetricOutputReference",
    "IotTopicRuleConfig",
    "IotTopicRuleDynamodb",
    "IotTopicRuleDynamodbList",
    "IotTopicRuleDynamodbOutputReference",
    "IotTopicRuleDynamodbv2",
    "IotTopicRuleDynamodbv2List",
    "IotTopicRuleDynamodbv2OutputReference",
    "IotTopicRuleDynamodbv2PutItem",
    "IotTopicRuleDynamodbv2PutItemOutputReference",
    "IotTopicRuleElasticsearch",
    "IotTopicRuleElasticsearchList",
    "IotTopicRuleElasticsearchOutputReference",
    "IotTopicRuleErrorAction",
    "IotTopicRuleErrorActionCloudwatchAlarm",
    "IotTopicRuleErrorActionCloudwatchAlarmOutputReference",
    "IotTopicRuleErrorActionCloudwatchLogs",
    "IotTopicRuleErrorActionCloudwatchLogsOutputReference",
    "IotTopicRuleErrorActionCloudwatchMetric",
    "IotTopicRuleErrorActionCloudwatchMetricOutputReference",
    "IotTopicRuleErrorActionDynamodb",
    "IotTopicRuleErrorActionDynamodbOutputReference",
    "IotTopicRuleErrorActionDynamodbv2",
    "IotTopicRuleErrorActionDynamodbv2OutputReference",
    "IotTopicRuleErrorActionDynamodbv2PutItem",
    "IotTopicRuleErrorActionDynamodbv2PutItemOutputReference",
    "IotTopicRuleErrorActionElasticsearch",
    "IotTopicRuleErrorActionElasticsearchOutputReference",
    "IotTopicRuleErrorActionFirehose",
    "IotTopicRuleErrorActionFirehoseOutputReference",
    "IotTopicRuleErrorActionHttp",
    "IotTopicRuleErrorActionHttpHttpHeader",
    "IotTopicRuleErrorActionHttpHttpHeaderList",
    "IotTopicRuleErrorActionHttpHttpHeaderOutputReference",
    "IotTopicRuleErrorActionHttpOutputReference",
    "IotTopicRuleErrorActionIotAnalytics",
    "IotTopicRuleErrorActionIotAnalyticsOutputReference",
    "IotTopicRuleErrorActionIotEvents",
    "IotTopicRuleErrorActionIotEventsOutputReference",
    "IotTopicRuleErrorActionKafka",
    "IotTopicRuleErrorActionKafkaHeader",
    "IotTopicRuleErrorActionKafkaHeaderList",
    "IotTopicRuleErrorActionKafkaHeaderOutputReference",
    "IotTopicRuleErrorActionKafkaOutputReference",
    "IotTopicRuleErrorActionKinesis",
    "IotTopicRuleErrorActionKinesisOutputReference",
    "IotTopicRuleErrorActionLambda",
    "IotTopicRuleErrorActionLambdaOutputReference",
    "IotTopicRuleErrorActionOutputReference",
    "IotTopicRuleErrorActionRepublish",
    "IotTopicRuleErrorActionRepublishOutputReference",
    "IotTopicRuleErrorActionS3",
    "IotTopicRuleErrorActionS3OutputReference",
    "IotTopicRuleErrorActionSns",
    "IotTopicRuleErrorActionSnsOutputReference",
    "IotTopicRuleErrorActionSqs",
    "IotTopicRuleErrorActionSqsOutputReference",
    "IotTopicRuleErrorActionStepFunctions",
    "IotTopicRuleErrorActionStepFunctionsOutputReference",
    "IotTopicRuleErrorActionTimestream",
    "IotTopicRuleErrorActionTimestreamDimension",
    "IotTopicRuleErrorActionTimestreamDimensionList",
    "IotTopicRuleErrorActionTimestreamDimensionOutputReference",
    "IotTopicRuleErrorActionTimestreamOutputReference",
    "IotTopicRuleErrorActionTimestreamTimestamp",
    "IotTopicRuleErrorActionTimestreamTimestampOutputReference",
    "IotTopicRuleFirehose",
    "IotTopicRuleFirehoseList",
    "IotTopicRuleFirehoseOutputReference",
    "IotTopicRuleHttp",
    "IotTopicRuleHttpHttpHeader",
    "IotTopicRuleHttpHttpHeaderList",
    "IotTopicRuleHttpHttpHeaderOutputReference",
    "IotTopicRuleHttpList",
    "IotTopicRuleHttpOutputReference",
    "IotTopicRuleIotAnalytics",
    "IotTopicRuleIotAnalyticsList",
    "IotTopicRuleIotAnalyticsOutputReference",
    "IotTopicRuleIotEvents",
    "IotTopicRuleIotEventsList",
    "IotTopicRuleIotEventsOutputReference",
    "IotTopicRuleKafka",
    "IotTopicRuleKafkaHeader",
    "IotTopicRuleKafkaHeaderList",
    "IotTopicRuleKafkaHeaderOutputReference",
    "IotTopicRuleKafkaList",
    "IotTopicRuleKafkaOutputReference",
    "IotTopicRuleKinesis",
    "IotTopicRuleKinesisList",
    "IotTopicRuleKinesisOutputReference",
    "IotTopicRuleLambda",
    "IotTopicRuleLambdaList",
    "IotTopicRuleLambdaOutputReference",
    "IotTopicRuleRepublish",
    "IotTopicRuleRepublishList",
    "IotTopicRuleRepublishOutputReference",
    "IotTopicRuleS3",
    "IotTopicRuleS3List",
    "IotTopicRuleS3OutputReference",
    "IotTopicRuleSns",
    "IotTopicRuleSnsList",
    "IotTopicRuleSnsOutputReference",
    "IotTopicRuleSqs",
    "IotTopicRuleSqsList",
    "IotTopicRuleSqsOutputReference",
    "IotTopicRuleStepFunctions",
    "IotTopicRuleStepFunctionsList",
    "IotTopicRuleStepFunctionsOutputReference",
    "IotTopicRuleTimestream",
    "IotTopicRuleTimestreamDimension",
    "IotTopicRuleTimestreamDimensionList",
    "IotTopicRuleTimestreamDimensionOutputReference",
    "IotTopicRuleTimestreamList",
    "IotTopicRuleTimestreamOutputReference",
    "IotTopicRuleTimestreamTimestamp",
    "IotTopicRuleTimestreamTimestampOutputReference",
]

publication.publish()

def _typecheckingstub__8970063958eb0f6bf4cf03a61afc279069c72b111ef178751456f29c2dcbca01(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    name: builtins.str,
    sql: builtins.str,
    sql_version: builtins.str,
    cloudwatch_alarm: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[IotTopicRuleCloudwatchAlarm, typing.Dict[builtins.str, typing.Any]]]]] = None,
    cloudwatch_logs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[IotTopicRuleCloudwatchLogs, typing.Dict[builtins.str, typing.Any]]]]] = None,
    cloudwatch_metric: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[IotTopicRuleCloudwatchMetric, typing.Dict[builtins.str, typing.Any]]]]] = None,
    description: typing.Optional[builtins.str] = None,
    dynamodb: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[IotTopicRuleDynamodb, typing.Dict[builtins.str, typing.Any]]]]] = None,
    dynamodbv2: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[IotTopicRuleDynamodbv2, typing.Dict[builtins.str, typing.Any]]]]] = None,
    elasticsearch: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[IotTopicRuleElasticsearch, typing.Dict[builtins.str, typing.Any]]]]] = None,
    error_action: typing.Optional[typing.Union[IotTopicRuleErrorAction, typing.Dict[builtins.str, typing.Any]]] = None,
    firehose: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[IotTopicRuleFirehose, typing.Dict[builtins.str, typing.Any]]]]] = None,
    http: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[IotTopicRuleHttp, typing.Dict[builtins.str, typing.Any]]]]] = None,
    id: typing.Optional[builtins.str] = None,
    iot_analytics: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[IotTopicRuleIotAnalytics, typing.Dict[builtins.str, typing.Any]]]]] = None,
    iot_events: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[IotTopicRuleIotEvents, typing.Dict[builtins.str, typing.Any]]]]] = None,
    kafka: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[IotTopicRuleKafka, typing.Dict[builtins.str, typing.Any]]]]] = None,
    kinesis: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[IotTopicRuleKinesis, typing.Dict[builtins.str, typing.Any]]]]] = None,
    lambda_: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[IotTopicRuleLambda, typing.Dict[builtins.str, typing.Any]]]]] = None,
    republish: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[IotTopicRuleRepublish, typing.Dict[builtins.str, typing.Any]]]]] = None,
    s3: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[IotTopicRuleS3, typing.Dict[builtins.str, typing.Any]]]]] = None,
    sns: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[IotTopicRuleSns, typing.Dict[builtins.str, typing.Any]]]]] = None,
    sqs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[IotTopicRuleSqs, typing.Dict[builtins.str, typing.Any]]]]] = None,
    step_functions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[IotTopicRuleStepFunctions, typing.Dict[builtins.str, typing.Any]]]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timestream: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[IotTopicRuleTimestream, typing.Dict[builtins.str, typing.Any]]]]] = None,
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

def _typecheckingstub__07891052e4dfd16458e3c2bbe8879734446fe703cb2bc96cac6baa460888f937(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d75910e333fba2f691b0d5bc6cf9417cc31457e92251ec4adf31a2114af3a4c(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[IotTopicRuleCloudwatchAlarm, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05f1825846214f9237779f4359ba81f64f7b8ed228fbff5f56deb6bce0a7ec9d(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[IotTopicRuleCloudwatchLogs, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41ceb9d80125030fc606b37a1ab39c7ec55a0911080608c6479b167276aff770(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[IotTopicRuleCloudwatchMetric, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1619bd2b8e6aa2fc94f8fd9f73a3a6b2dff272f0d48c254285ca12c8f3f655d(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[IotTopicRuleDynamodb, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cda972003f852e1e047e690ee3cd27d0d7142ecefc9a72ecc95befa85e2a4f4c(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[IotTopicRuleDynamodbv2, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb385d0e37e2208fb99f375d6b15502ed154fe5a9319755b784a4a212b02a339(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[IotTopicRuleElasticsearch, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__21ebcc20b66a6b75a0524ea4b00eddc076f8a461dac0117bcd04653008004bb6(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[IotTopicRuleFirehose, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0c5cbad31d09269d73168d071a6dc644a6fc7a8bb3045fe9eee180ebc6d5e36(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[IotTopicRuleHttp, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5ab200fea93b95224a14b18b7aade3c9b67a039d980889cc30eef099f403cca(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[IotTopicRuleIotAnalytics, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__802a2bdc13bd2639969df7482fa282b0788236b72443e995f033984665e67149(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[IotTopicRuleIotEvents, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ae5c1dae3e98ee0bdd4b00a645c87e2d2af52cbee0518bae11357fb91d7fa3d(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[IotTopicRuleKafka, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc79a9ff29a7453aa9907c08bc239c9da0ca92cedaed3e394762cf3c6b4c34f3(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[IotTopicRuleKinesis, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18c043324e82d256c60ac5dadb1158b5f682abb78d6cb8025d199c9c5f892f80(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[IotTopicRuleLambda, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__602282092e12dd922f44f1910eec1d7933c18d3224bb66c9cb86bb2a33e97e3d(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[IotTopicRuleRepublish, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9cb6984e2e0244d3c7471b869bbfc610bc1820cb81f98f461a816e7db30ecfa3(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[IotTopicRuleS3, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ceb0b7dca719b71ef483c079f2655b5915ec1ec3fc11d5a9f0a84bd97fc0374(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[IotTopicRuleSns, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60650706897f0e42d1bc3a8ffb5f3b3cd971eab113a568df57b48b75270d0cf8(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[IotTopicRuleSqs, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1dabb8f6030e62a76e328b9954a76b87aa3814daae40bd17b2357afc90936d6f(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[IotTopicRuleStepFunctions, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__901369fb361cdf03e678310b7948457aee14d381ad5d21445821496b99d95550(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[IotTopicRuleTimestream, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4c2b2d28d848243c51f5ccc1c643d9264e8555ea818f9c0e6b258c838f850f6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1af983abaf0cf236dffe6f5ce3dcedb7b6ccc1f59206fdb0a8728b68c41b3d51(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce035f1a4fa8e41e5f0de5c1395e0796644486722f57bb7893d42ec178aad327(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__621198ba6abc0a0777236fd9236e11a4518f06fb7141c4be80ac0edbac431f36(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d57d46a8702002be22c00306e0f6fd2b87021c590a33c67c78885abe2019d9d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f08852130141c9567a2645badc54d1d623961edbc64709a94a3dca54602b835(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb26afdebd349df458a87eb44916b354298defb605cc1921dda0e8677c440cfd(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be5f7a57aea09f44be296f94c688533482dc3d5fa12d1a54078744d9b8a36667(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f80cad964ea1794363a30c075aa9b7d54844d7e9b326843217e380085924d3ab(
    *,
    alarm_name: builtins.str,
    role_arn: builtins.str,
    state_reason: builtins.str,
    state_value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7fc0b2ce2a1c9de004494f114cd23a4e6fed37728e1c88d81ea4f1303289a366(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ad54e6bc07b5701524af251abf9644fcdcae1f94a7315ccbcef771d22e27ee7(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11566d6d82d209c437913bdcb0dba0cea2eb82eb48f741d10fa6473d8161653c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f25a4fab2c8cf8a5ddf3140a4065c020c4552ed0214d0315af143c39b8437d9(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2f308506a63554ce60a213a199783f01fb096e912cc4c26f0ecae3f3fedfbd7(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7fb4bca6948a655376b0801c2337b00bae8b671032ba735aeb64f8da25c742a0(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotTopicRuleCloudwatchAlarm]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__423b0f50d67b29f01eead7c923329fb54febdf08904be3a64ca3bce7f7416234(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__56729d3ba5fc93d5c15e682c45a2342f9db9c157f30e1505d20784d0a341bd77(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__145480f6801807cbf3fa91c58f223ec5390e29d4033a9c3f03790102039e0d9c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c30757486b76f645ed9379118153f25c2474cbcde9f8a53986f9447143b071db(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9fed69a99387675f3a659329b8ace0ccc6c96240bee350be1c9a7b07ba5ea2e1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9eb064f57b6319cdaa1ac8ce19265ae196aad42a1a3542ba35c3695df81051e0(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IotTopicRuleCloudwatchAlarm]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76561102d918397c1716ad8540000c6bf0c0165120ead2b5716d0c53bbfe9070(
    *,
    log_group_name: builtins.str,
    role_arn: builtins.str,
    batch_mode: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9aeaab1f8f8ebfb12b89985d842d0c98c9cca16ee008e22ba22e74176ed4c971(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e929628524e8b7bcd89e3405dfb515d06a2380f0f93356de0334f613daa79a6(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff0c0b1d021904b3c62abf26a3bb0d499d4c3412f43e517730af804358ff46f7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cedb774b04fa1b2407786949d7fa39416b7e1ca17a3e314ee363e3b71984ad4c(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50bcaae84ba976947676dd6bfbd00a9490354e1cb0ca6d3804abd4e5b5e82c23(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__49eb653b4486e056b9652f792792b5ea1e69e2b44507c986820ed000fd53964c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotTopicRuleCloudwatchLogs]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf51dccee4aaaf55b0e8a8ed059bf8c7b56a82514e63060944c7cde8fd6cdbc0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1594a04b1eb992ae3817c5a797e56e91e258ac5d276e93d3229dcb01219c84d1(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d4f00a3274e84ec178dbd93b918cb55b63ccfafc46ce3ea12839f7b2d499e38(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ad113744adcaa349f77d4bf09c7a33250271cd40e102299b0da24801780b3b0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b572b3d2d07b874c7868e7d573aa703086c5878485659875c2ffa059197b0bfd(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IotTopicRuleCloudwatchLogs]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19931c16274872697d258287b0c631350ebe4a7b1c054f46b62c5c43a6ba0fab(
    *,
    metric_name: builtins.str,
    metric_namespace: builtins.str,
    metric_unit: builtins.str,
    metric_value: builtins.str,
    role_arn: builtins.str,
    metric_timestamp: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19d1e6d48c6fdf3aa8e07765ca542041083c7bc308770de2348f2e006585f474(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee135e846f6a9548522b4d8628d62298272d06ab28a041e044e5933a694a8bb7(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6447120f3379ce076a80a25250153fc8028ffe3c9a94bce451d72b83b6dc142b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf6da84f71c96551736eb3a08880cc2bfa5a92941f77336bbaeb9a6062d348d0(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4aacd560e0a606c52e882f73969845b3c69d5baf674ecac4532e36342ecdb0ad(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5904fc2e80d2005371de9d212467b696c8e5a97586eaf2037acf28f0c4113b5(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotTopicRuleCloudwatchMetric]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__84bd7432c8ad2dea5fa6719f31121f8b3bb510b892cce94bf414ff75fce432b2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46418cca82bf7a4030c32ef9192c5a458641ea95a4a8300b3c676305e3a372b8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a6ec03b55983c9ceedd592c2964228f060462125d15d374cbea090cb8cb7ded8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a299e010e576017e083083b825d87a3d9773c0a1bd844c85fe2a2ae398bda5d1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5329c379dbff8d6b8195572cb4a12094c85e7d259dbdf12f57677e68e46bb4de(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e459559b8954c07fe55b7d1c6a721c31b2627e67931dc06d858e6b21ef2b497(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0fce85eed23cbcf0254e06001e9f1aee32a01c0ee2b3ee70c5e0441f6aa4718(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2cbdb615c232b2083dd61d441c54a16a40ff25f3450c411c57e78558042523a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IotTopicRuleCloudwatchMetric]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79143a22ba041c9eea32ef371eed79b12fab42325e6871a29a93e1cd5b715234(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    name: builtins.str,
    sql: builtins.str,
    sql_version: builtins.str,
    cloudwatch_alarm: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[IotTopicRuleCloudwatchAlarm, typing.Dict[builtins.str, typing.Any]]]]] = None,
    cloudwatch_logs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[IotTopicRuleCloudwatchLogs, typing.Dict[builtins.str, typing.Any]]]]] = None,
    cloudwatch_metric: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[IotTopicRuleCloudwatchMetric, typing.Dict[builtins.str, typing.Any]]]]] = None,
    description: typing.Optional[builtins.str] = None,
    dynamodb: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[IotTopicRuleDynamodb, typing.Dict[builtins.str, typing.Any]]]]] = None,
    dynamodbv2: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[IotTopicRuleDynamodbv2, typing.Dict[builtins.str, typing.Any]]]]] = None,
    elasticsearch: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[IotTopicRuleElasticsearch, typing.Dict[builtins.str, typing.Any]]]]] = None,
    error_action: typing.Optional[typing.Union[IotTopicRuleErrorAction, typing.Dict[builtins.str, typing.Any]]] = None,
    firehose: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[IotTopicRuleFirehose, typing.Dict[builtins.str, typing.Any]]]]] = None,
    http: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[IotTopicRuleHttp, typing.Dict[builtins.str, typing.Any]]]]] = None,
    id: typing.Optional[builtins.str] = None,
    iot_analytics: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[IotTopicRuleIotAnalytics, typing.Dict[builtins.str, typing.Any]]]]] = None,
    iot_events: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[IotTopicRuleIotEvents, typing.Dict[builtins.str, typing.Any]]]]] = None,
    kafka: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[IotTopicRuleKafka, typing.Dict[builtins.str, typing.Any]]]]] = None,
    kinesis: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[IotTopicRuleKinesis, typing.Dict[builtins.str, typing.Any]]]]] = None,
    lambda_: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[IotTopicRuleLambda, typing.Dict[builtins.str, typing.Any]]]]] = None,
    republish: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[IotTopicRuleRepublish, typing.Dict[builtins.str, typing.Any]]]]] = None,
    s3: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[IotTopicRuleS3, typing.Dict[builtins.str, typing.Any]]]]] = None,
    sns: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[IotTopicRuleSns, typing.Dict[builtins.str, typing.Any]]]]] = None,
    sqs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[IotTopicRuleSqs, typing.Dict[builtins.str, typing.Any]]]]] = None,
    step_functions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[IotTopicRuleStepFunctions, typing.Dict[builtins.str, typing.Any]]]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timestream: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[IotTopicRuleTimestream, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22c3100b34d960b81cc420672a70182be62148af182e9f3a4a7a978dfefd7772(
    *,
    hash_key_field: builtins.str,
    hash_key_value: builtins.str,
    role_arn: builtins.str,
    table_name: builtins.str,
    hash_key_type: typing.Optional[builtins.str] = None,
    operation: typing.Optional[builtins.str] = None,
    payload_field: typing.Optional[builtins.str] = None,
    range_key_field: typing.Optional[builtins.str] = None,
    range_key_type: typing.Optional[builtins.str] = None,
    range_key_value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa8834151932991cb06f43fea73661c56f96800811dca71d20ce01083c380919(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92ffcc3095620130b75eaa7f1d18bf6a0080744275acb2ade415c48599199395(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1f52b8cd18c2e40c7551bc6fd01b4d1cc348861569559451c054599ad4f8182(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d94f7e43958e67170fdecbc8055c89da284aeeafedbebd76fc04fb0e77177765(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bcfdadfa49808c05efb86e4a188573be99320567ef44c5e0670d6d5c9b1b5e83(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__177f5f934c5ab7b4cd8bb7c8b8fa32839a70ee6256e4e19ff5f93fda9189156d(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotTopicRuleDynamodb]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__052a732588371805c94bd72722c6112b4bc87b8191a863492b195499c59ab86c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ddb45da7df9924a79ef94c7f086ae4711cb7578362927914ff14f5a203cbdad7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53ba42ad39d7fc6e9b97251156725af5f5d54962a35e3ad0c98838ff02670e28(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff46e31673192af32e51c598657d261a86ec4cc237965cfd02fb18784424417c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c1223a116daf3b235be35b89af1b6b7222896203756d970596ee49c3fc882b3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a36becd3740b98121bd36dc7f1a1dd0e3ed116c07f693d00e06f2d1971ec876(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__abc7970fd1a61d2b2ec03bfc86dd46acc17a92e78cd7ea03e9f84703adc922da(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00510fc6ace6370735892b94c32df9c0d1daf21ec5979dc395bb97c92efc1292(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37855fc02838a52efcfd6a11c72d791f1accc068752906cfb86bc0687002023d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__442e11f4126f9b640e9fe94f5c48d7471aed5037982657a0c0385ea750de4f91(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b04308f3c7092005dc735554db20991967accdf1d6eb0fa8d264104109107af(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f748855ac08bc423e06f192bd458b199fd4a278925d171c5ccaf0d169882e06(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IotTopicRuleDynamodb]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62daf13af5aac5699378f7ce8e0323d6511dc6846bab3ea09beacf5a0388e3f8(
    *,
    role_arn: builtins.str,
    put_item: typing.Optional[typing.Union[IotTopicRuleDynamodbv2PutItem, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__219e540e2f072f12683a6e8eedcc550e1a5dee24c3c3391366f555791769d26a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c4a72440118e1093c6e533b72a90a36766d58ea867aa3fcbd9a9f8d7cda7854(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f27d74caf7df9666017cd4a62f5fbb24159ee1d30daa9806526ef322f631267c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__efbbbb3946fe5d0a6632612062c408bf00cc0470f4b09424cdf4e0c2bc166327(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61537d4f0d630f3663c72a70968b10c556b0e4524eed787cd4173c4e12ccc19c(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__619a43024d80d2590d0263d956febf146537dcfc3f53d22b9ebb256cb8890dbb(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotTopicRuleDynamodbv2]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a7995c1a3786cde3536cbb9c02ba0567b7d421ea2b0c15b9876e512dab923ca2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0dac94056b69bde5a6f271a4c65b6d1b7dd8a840546e72d7a3083059f3d065a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00dd34b29c2fd0693ffed132977d6d2573126dc2a5df0d566abf3593175e19ef(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IotTopicRuleDynamodbv2]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77bc4ab141d48c3bc032a5cb5b76a3b175fd3f5ee3655d84df475862cb45ff58(
    *,
    table_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__842a0b1147773300406ce0d036ec519682eda30eadccf71540c3931a7cf58c49(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc1539f3e331c3f1ad210c24468485f3e96cbf740f69088eb7c47049988614b5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__82bcb5de017af6bd9c493e135277e5f11e58d58a9e866b0daf9e4a088dfc49a1(
    value: typing.Optional[IotTopicRuleDynamodbv2PutItem],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85248bb147339c0a761a11368cc36850e675754c092614956f29c191ce83453a(
    *,
    endpoint: builtins.str,
    id: builtins.str,
    index: builtins.str,
    role_arn: builtins.str,
    type: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__390cfbe9caf31143d67982b77ba3398d5db3912659ff58b539c543ad329a8470(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__332cc3eeedb252068e2c2f6007c594f312144f6795779a2bb217a80882ea6b8e(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__21d9c9d7d268c528ae7f94808420b3c801c635de51641ee0e81e07c0060506e4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3eabfeae4b048f323ab019bbeb0a4baa38b52ccf1c708e7e8b2695f7265f923d(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa86dd3df0b4412c98c7aafebba49d631f1d7062568dc10e5d7826f7ad120e26(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2235187eaf52e5ae6c943aa5015e37c5b0c13cceb91ca63c2cf38572ebd663a2(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotTopicRuleElasticsearch]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__927a9b6f8831430d4b511d2811db3cce5dd3ce1998d4cdcbc13224f6b265009d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__47a529b121a8b6a398651caa66ff29bfe3f86e1a95025139f41b9bc7b099a6f7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc010db433ce71b7486800ca4abb21a15d4780fd42379d452a579afe6fdd11b4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e68a618119ac60043834a67f329284c78c1356c43e7cb39288ce03529755504(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6fc890eae303a9905a9cd9dd9a2d4d54f44dc49ffb231e158baec07fbbff4bfd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__55c043ede332b77b071da5f45286a0c6c07f28a3c64a744d3ee662ac81d1fb24(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__545a1e84c722158d4845742b7d35799ac2381ad1ca406837a638431d260a2a35(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IotTopicRuleElasticsearch]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bed9afd42f9d12d79e1db0e5a9c43e0a0f3b58e034660e13ee4da4b2232b46a5(
    *,
    cloudwatch_alarm: typing.Optional[typing.Union[IotTopicRuleErrorActionCloudwatchAlarm, typing.Dict[builtins.str, typing.Any]]] = None,
    cloudwatch_logs: typing.Optional[typing.Union[IotTopicRuleErrorActionCloudwatchLogs, typing.Dict[builtins.str, typing.Any]]] = None,
    cloudwatch_metric: typing.Optional[typing.Union[IotTopicRuleErrorActionCloudwatchMetric, typing.Dict[builtins.str, typing.Any]]] = None,
    dynamodb: typing.Optional[typing.Union[IotTopicRuleErrorActionDynamodb, typing.Dict[builtins.str, typing.Any]]] = None,
    dynamodbv2: typing.Optional[typing.Union[IotTopicRuleErrorActionDynamodbv2, typing.Dict[builtins.str, typing.Any]]] = None,
    elasticsearch: typing.Optional[typing.Union[IotTopicRuleErrorActionElasticsearch, typing.Dict[builtins.str, typing.Any]]] = None,
    firehose: typing.Optional[typing.Union[IotTopicRuleErrorActionFirehose, typing.Dict[builtins.str, typing.Any]]] = None,
    http: typing.Optional[typing.Union[IotTopicRuleErrorActionHttp, typing.Dict[builtins.str, typing.Any]]] = None,
    iot_analytics: typing.Optional[typing.Union[IotTopicRuleErrorActionIotAnalytics, typing.Dict[builtins.str, typing.Any]]] = None,
    iot_events: typing.Optional[typing.Union[IotTopicRuleErrorActionIotEvents, typing.Dict[builtins.str, typing.Any]]] = None,
    kafka: typing.Optional[typing.Union[IotTopicRuleErrorActionKafka, typing.Dict[builtins.str, typing.Any]]] = None,
    kinesis: typing.Optional[typing.Union[IotTopicRuleErrorActionKinesis, typing.Dict[builtins.str, typing.Any]]] = None,
    lambda_: typing.Optional[typing.Union[IotTopicRuleErrorActionLambda, typing.Dict[builtins.str, typing.Any]]] = None,
    republish: typing.Optional[typing.Union[IotTopicRuleErrorActionRepublish, typing.Dict[builtins.str, typing.Any]]] = None,
    s3: typing.Optional[typing.Union[IotTopicRuleErrorActionS3, typing.Dict[builtins.str, typing.Any]]] = None,
    sns: typing.Optional[typing.Union[IotTopicRuleErrorActionSns, typing.Dict[builtins.str, typing.Any]]] = None,
    sqs: typing.Optional[typing.Union[IotTopicRuleErrorActionSqs, typing.Dict[builtins.str, typing.Any]]] = None,
    step_functions: typing.Optional[typing.Union[IotTopicRuleErrorActionStepFunctions, typing.Dict[builtins.str, typing.Any]]] = None,
    timestream: typing.Optional[typing.Union[IotTopicRuleErrorActionTimestream, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b83d8476ae22b1c65f01786a598701333ed2b69fb621cec167b0261f3369d4f2(
    *,
    alarm_name: builtins.str,
    role_arn: builtins.str,
    state_reason: builtins.str,
    state_value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__762df605998f5f70bbc60ba53cc58a393ee90b36a150c8cfe95dc1867202a8ba(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68438aeca9f46681171eb7ba723318fbd8ea11a2eaa6dd96b89811a3938f3763(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__23b2217c7ef545cbeda02403597143c77e2fdd40abbacdac5b34f96c86dcba39(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5fcfb23e800e0403f181f7f8f2d1a4c2738ba49588f43b2a292716379843d66c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81be8922e2c21f86cc8cd9b62f8a360bde2e609710ecc751193d61b2bdb0ce91(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b93c2a37648d2b48c416b0fa80e574e2b5286f73d054b5cf003a1225d5888f1(
    value: typing.Optional[IotTopicRuleErrorActionCloudwatchAlarm],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9334e9260d7d7332c2116c48d7f4a6581536a7045f4ab5bb47a60828af1939f(
    *,
    log_group_name: builtins.str,
    role_arn: builtins.str,
    batch_mode: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__51819e7dc308c3409309bd6f0b96e9a7c11110825debc77653a1e74239716cc5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00e3365bc51f589e5b59935a6ae94ea6304d0c455b691c872323d54d47fcc403(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc4bbeb509bbbaf51b31d0c76e6990a1956e56b46058343294cdabf820331253(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fca05b519b6ba9e3f82d638875722bc68f0a964065bf8066da5a12d78fdb7362(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a711555c59bfa0005145ded599cbcde28deed4ecc7b50d9ad2d206d3d064dfc6(
    value: typing.Optional[IotTopicRuleErrorActionCloudwatchLogs],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__23e4cfa1c5925f865b4f4df75c68460fcefa151d9a66c0a6d2533c4277e2d73d(
    *,
    metric_name: builtins.str,
    metric_namespace: builtins.str,
    metric_unit: builtins.str,
    metric_value: builtins.str,
    role_arn: builtins.str,
    metric_timestamp: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa550d0f71c63f2583b2046b9c6fbfc6c13efde3396d4695b77554bac0f137ae(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85d82326271b61f45ae6e06ecf762dbe1df29fd592087c5b259496de2661f796(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3a862401990990c836293e1c9f1fbad492e57fed17469043322c0d00020d88e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d358126f1dd7700012b88cc461cb52beca0a719fd7f7d7d49ee829653ba076ee(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__32e75bf68f51408d0a32f67f9ac6dd70e97e0603bd3edb726368dbe4b8edc8eb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__083fe30ccc0f64ea832a07075e6968831c3487f903b3bd7c385ed3d6bb2fa980(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0d6f96c5da36cbb0d84a7ab89818fd40a0525c04d263fd0a8bafc9fdcbadb37(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__741329ce47b85482a09bf2df9afc6d5d27a022e8bc32e5ebd25548bf5d162a15(
    value: typing.Optional[IotTopicRuleErrorActionCloudwatchMetric],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cdf3d6f6173501ff4e94e9a3d604d43248e8d5f0b3ef51aa7c388e9e54b2d296(
    *,
    hash_key_field: builtins.str,
    hash_key_value: builtins.str,
    role_arn: builtins.str,
    table_name: builtins.str,
    hash_key_type: typing.Optional[builtins.str] = None,
    operation: typing.Optional[builtins.str] = None,
    payload_field: typing.Optional[builtins.str] = None,
    range_key_field: typing.Optional[builtins.str] = None,
    range_key_type: typing.Optional[builtins.str] = None,
    range_key_value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a876b7f79fbb4f67156b714e75be69845f8c71ba7abfed56c274d5bf854a7f76(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53bb332ee999c81902a3b96aa24d51192fefe8e8ad812ae8d95ac41d903c7bf5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f757a385613356d1cf129adb44a15cf4927b6e6c2f1396df6cc12996741f8924(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__847b182e6c33d6d02c3e9467b304a22c63c5ffac9945de64f36b70dc7d94a11c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2f32b06c06cdf0ea35e8afc1be9d76afedfbd0e86ee51688cdb33cccddcc5ed(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09eaf2d1d46fddb2be567ecf1ae4881d18e1c7c22261c7d93f86067fb7e63679(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53f4f127ee8458894713a73b578bb9536aad40cdb80a165e6c1581ed7e5dd0ad(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d553d9593a49a96c6433541627c3e50321672dbc663d0faf01d2ca8bb73be40f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ef41dda0e872881bc65602419b49f79d5292042f5dda613b0f26d5e47faae4c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__264c6c07fb8ea8fd7ebc88a86d9ce82addfef9f15aa7c014cdb5ae5affed769e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f3e59c0b0a398eed2467df16e4e8766ee60e7e8cf585b87aedba63cc77bac6f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8de412efbaa91eb54b4617199ebcaec34561804f1852fc5d7fa83b2e6c1600ea(
    value: typing.Optional[IotTopicRuleErrorActionDynamodb],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc12c12a46fa57c8a98f9c12ff52a529bb4c861b0c9df1798b049102a9137028(
    *,
    role_arn: builtins.str,
    put_item: typing.Optional[typing.Union[IotTopicRuleErrorActionDynamodbv2PutItem, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9ecdcd50884fe336b3f08e41d4e6ba409bb5207d0a3aa771ee09fc5ba9e5a51(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__067e66649898bcb3163b191bb64bd0e5f31f9f70ea845d6c2d2bb23385dc7d75(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ce212cdd6b794ef4df836e5a3b710109f9408a56793e4515fea4f7581e1b2d7(
    value: typing.Optional[IotTopicRuleErrorActionDynamodbv2],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5cf7b3aa537109d156f8a80480362954f4bda9e7068113c0d72dc0954fe0d393(
    *,
    table_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a9ef8321c527358823fee37c908b1ca0e1dd02b15cedb47525ae57a2cd83ca5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee9c0076ed7be13baef6d2fd29afb0e24178f36df3a22617bc940a23f0c863d7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca66137312c4f5ed6af41b8382348ea1888be5a30b285d2876507a10ef70595d(
    value: typing.Optional[IotTopicRuleErrorActionDynamodbv2PutItem],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__840e7c6d0056e32d130c885aefc1eb19eeaa9f3dcb701b03b74c38bbc4e5244d(
    *,
    endpoint: builtins.str,
    id: builtins.str,
    index: builtins.str,
    role_arn: builtins.str,
    type: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ee7f10284f6d654649d6d0cc79b7e647601147c5dd60a0ee532d6dd5e18efb1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac99f1346fd034b98c4456cad868bc9ccc7f3dbfc7b7539a074a5c8bc4fd2143(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f707d0b3b5545d91ebf926e89cd1636bc499fe4058c0fe5f245e2d3ced88e3ba(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64e7c931c4c7aef7f694290d296760fd66f91b1f482f5325769ee59e6ac3c2ef(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dca9ac62731d8547b624887442ace081b64a1252cb971b5fe0d72065dd7503e9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd0f646bda18e32a3c70115891fdef7f258fda96d9d7e1de2ea5193ce24838ef(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__01dc5bfcea5ed57da0cfcba498c80f3b669705fa6b954ffd021121d3b6f55d00(
    value: typing.Optional[IotTopicRuleErrorActionElasticsearch],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__330b61a74f2a390ab516ce7f6fe6e676a44f00449479e4289c91d7443e406175(
    *,
    delivery_stream_name: builtins.str,
    role_arn: builtins.str,
    batch_mode: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    separator: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bac4fd12347d48674446165032b6e41c5d2fce4bc064eef9b2d00d89e9dc8353(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4f1ec22843866bb33374196efadeb23f255ea1dea7db2e2ac8ac2e0adb0556b(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2e638f9698ff2c3a786e8ffa340a876ce8c32e090b0d03ce2a1de67ea1a6cf6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9949d27419ad2b4f515beb326698dd164ee48b3f42da4cb65b3d4dacc94d67a9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05920209c1643ce0378c5a78fe4dffba4db6fcf879f59a7343c17d41bb9c7fe3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f91f8e81734ab2c27a3f912d183c6fbecabe445fed35030ccabf8f7dd13abd16(
    value: typing.Optional[IotTopicRuleErrorActionFirehose],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7cf00ed0a952fc9c6bd8b7615dbb7caac01e185fdbb15e4c5d732ab62479081(
    *,
    url: builtins.str,
    confirmation_url: typing.Optional[builtins.str] = None,
    http_header: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[IotTopicRuleErrorActionHttpHttpHeader, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44d35616c84712d38a443b1901dac1eeb179abc30116edbf10555660b974d7a0(
    *,
    key: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aba04ef60ba918cd0f507ec75ad85f32b72fb0588b0b9d2b2bc86a960e84cd79(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9353daa3e851582c94affbf67f11906b604adc1c35f02b78f7ed4183e7b5f364(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0336bb57332c077439a6419e78d26eaacbfacc7d34e61daac13b22eaf42d1d0a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__56a8c7401c0cc9e0005994ebc0b2941011827d2dc027d31330997bb35a9059ab(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a910d7d8e57ab407fc9711fd1188480b8c12fbf3879db43f5f8dbb138675ee8(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4440af0a0a25a2da58dff03658b6ef7dda4dc36c4e212e3e2429e47b4aa8adc(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotTopicRuleErrorActionHttpHttpHeader]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff232d7eb13cc70c62b509c3a622264271c115ae9f7b0ad235d95cf95ce31c0b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ceac0f8aec76fdab40e57ce93a584f8b97a22d4302eb4cc76618daae24337b9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52430a1f50309c5b31e6dd385f0851b17b06544494b02e69f87c0858e900a995(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d503da18c765d45d9913cd81384fd7fee26415477dab310d0ac6c4d6286453ee(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IotTopicRuleErrorActionHttpHttpHeader]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0262b928090da9cf00d9146c107ba18ce8d5fc5a1713e12a78734295b470088b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea656763299d21f11a78a78969ffeef2007e8a85fe8aa61aa2e7ad1fc1ed7a73(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[IotTopicRuleErrorActionHttpHttpHeader, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c0c8f7ec397887061bc35c7e6ad2fe447f790d4cb87f0bd240c072d582b538d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75541107967f66eba2b35367750afd8dd36acc9a8cc854e5e03075fd7b7f0429(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38047dc630dfa2b033641e2acb51678e3dafbfc16b920fa3e08844c4ab733a11(
    value: typing.Optional[IotTopicRuleErrorActionHttp],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e9265a72e9cbfbfac33a1e39f761d7181a3938385cb6b7a13a7d25b098b86aa(
    *,
    channel_name: builtins.str,
    role_arn: builtins.str,
    batch_mode: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2dd74647d63223c836410d85a63b728456b550bb3c62bea1e6ea9ce496115d4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a6e7575cee1ee38fbb17507df4bbca66d4dc2a6108ab04e8dcfeb265d64ce6c(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__819cd865a52fd8bb251e8776ffa37248aae0bc2e97dcf53de31997541168e56d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__35af257378fac8e3498c3ba8b0415aecfd7712ce75cac4fdaaa8fc14d616e774(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d43bc97d6961cc319eb3961eb59b56396d3d90d286bf6639da28055b461c79e3(
    value: typing.Optional[IotTopicRuleErrorActionIotAnalytics],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2cfc6f618fa93430480b67fb7522d955976525d5b665f6060b985654a7b77d14(
    *,
    input_name: builtins.str,
    role_arn: builtins.str,
    batch_mode: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    message_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26c2ab1fb4295f218b110c95c790d234824a616ba0dc6200e5190f3e9399969d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67a7a3c26680c34c13035abfd20f7fffeabe71f508dfb56760ed82e4e7d3fbbf(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd9140956fa786db48e1245a8c5ecd1956f7da7938f078541b2bc0fc663bdc6d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eedc4d31f78c95edb8e412280d1fb91bf9ebd8655faaf0283c0cfde2c9da52eb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0c1f50a92ddda07e5e5484ca8a4a3de4fbb2864fe33a94cb9271d7a8dab62af(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a6a7dfeeb26cb62b01da990feff88bb2c28530c9dd13fb34f403513c7e51a845(
    value: typing.Optional[IotTopicRuleErrorActionIotEvents],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4d7669d7e9eaa125ac1da6332267c0f14a7804d9bd87579c95beae05aee1aea(
    *,
    client_properties: typing.Mapping[builtins.str, builtins.str],
    destination_arn: builtins.str,
    topic: builtins.str,
    header: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[IotTopicRuleErrorActionKafkaHeader, typing.Dict[builtins.str, typing.Any]]]]] = None,
    key: typing.Optional[builtins.str] = None,
    partition: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f3e01acf4398c7e499a6ab467b595c0a4e6c58a6ab8309a69eb996b12e8888f(
    *,
    key: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8fbdb671bf8a4c05812ff6a7296ec8616d1e1ddefe2323748a7285e0f851d907(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de55a6761d5410cc9f46fb417237b021f1b202971ed82a614fd4788dd62a0e48(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__adafaec1c36591fea4a81c1bfa928f4878db834aae65c063462ec322ddfbb516(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f5f651c997e4c16d582aa28610a7a72bf99bb9bf022ceec5e264bc12bfae113(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41c9ebadc8017176aa1ce66e9d34158190a69d967383e23523bd312c60cbe8e7(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__061e3772059f4fd8a37182390e4dd7505c42a59b7118fb5f5e9ab535fa31d2ad(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotTopicRuleErrorActionKafkaHeader]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74e1ac3c85d1fd687a7ba383dad3379078fff418c6bcc48391e2964abb40ac90(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a847b4706f93afda1b0d87d5d5d3dfd7929b837df1f9de5e00be1a8fbaecadb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8d1674b53fe03c4dfcd41bf42f03edd8398db98ab8a005d18ed56f666b8f402(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89bae9fb1978d79cdb7abffc04fa396bce09c87ac4009ff862401fcfe375b879(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IotTopicRuleErrorActionKafkaHeader]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8031c1c9439d79f97f3e5a02597f113c1c0df16969de90cf33e7666d8f3ab915(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c024281db7dddf6b1220a9d96ece3107f55cc706c714d194101fd73a7da9056(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[IotTopicRuleErrorActionKafkaHeader, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c05e3272f96fb5fa72b1301ae43ced78f6d02d2d743e3b2fcfd40968b7dee77e(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5152b9590315cf97d3d1eb105c568bf53688239bfaed5f1cd21d25e5c290ee5a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bddc7a4a42d7d6d02ac67a2abf7ab3dfe7718b02ad5c9608ad2998c2ac271260(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4a7f5c4466648c670a073cf49383e7aa4454a59c12c56e8292986df329df48a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97cc864d05fb68a3ac183e1b797eef0b7f04827fe35ee8447ba0dc42f1441f8c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf4ee05c6bce37e622a5673e0b200e5048e0c84feef6a28aac2aeb9be75dd8f4(
    value: typing.Optional[IotTopicRuleErrorActionKafka],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e21737535f3015cf1fbdfe49e3fe8fe6e99d25b8623dc1a077422ec47a67e2a(
    *,
    role_arn: builtins.str,
    stream_name: builtins.str,
    partition_key: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0799c6bc46d4a2d16754114e6090a4c2b2521ef0dda7fb72b6ba30e6e750f64f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b396db0d63b3ebbfc850f17452760a5a61b53853b023e56524f2c1a78d7025da(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b868c6f0472f074ea735f4e3241bf6188876a95ccae9ec87f2dd44da05982b03(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa0be88ecf5c2346109072c7a4e74c040b17e66800f1576980d82f961bb5976d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2913c77f58c716b85ecaa59894f6b2e8a2ef85f4f0b7b56e0ff6797e95788c3e(
    value: typing.Optional[IotTopicRuleErrorActionKinesis],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f385034edbfe04235c2656de1531112c05524d8c9b39bdd2bb7dcdfe47b8463a(
    *,
    function_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61db101dfb1e05993638e96037a2d721d2fb8216ca83981b1966d8d211cd2359(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5bde8f174461287395141a31b0e783471e2d53f34d3d1316985c842f74a1144(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1c0d00a069d59ab1598a3a2c456bfd57c2819a18c0d072c8b448c5a815fa21f(
    value: typing.Optional[IotTopicRuleErrorActionLambda],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00ebeeab15e3325819fcc40ea15eea7090fcdbcd860f1671d42d63291a5aa96c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c95adaa71b14572919497c31eae0eb39084f3470bcf6016fac9b53462122a7bf(
    value: typing.Optional[IotTopicRuleErrorAction],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a6712977dc19982d34c3a5bb1c3c1349ca9d07b6e3cd96bb200cfd3d9d05c1ff(
    *,
    role_arn: builtins.str,
    topic: builtins.str,
    qos: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7565623ee5052a29b96b8bdd3cbf18f3344e9c5df29b4b1957b4d09ac95cdf81(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72847506256fa8cf23dcb496119df88b82c774b33406bea5e5f29fa12a5f7439(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5458d50298e2253967a2112d540b09a4caf6bd2e245f4cbf25682ae0c96d2c99(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9975036502933aea8ffb862fa75b24cc742675337191a268f87f2303ad7bd646(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__84a071b12b6e35a9e424cf593263acee3f575b0af018ece556e5d8d36b838c61(
    value: typing.Optional[IotTopicRuleErrorActionRepublish],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec28e16ed6cf830ca9d64fb3849688526c0b226b430403fcb0be648b224b4a3a(
    *,
    bucket_name: builtins.str,
    key: builtins.str,
    role_arn: builtins.str,
    canned_acl: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0ab642389342987d96055dcee623c9a23a99440380cdb3ddb0154561fd16700(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ff7b2d101f0604dd8416385824811837e0f799ca3ad0ae3c7a276d03746880e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69d2d5eb1a0b0ab3847273a235b18d909aef9f0c0762607d7a826f2483ca7068(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f0efa9685f72d303b5ff9490ef93040ee7fa29e366ee728b69bf2e3790a47d3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d987cdfe88d3b27766029731c82433813cf7d4e27414cd973110f302ddb6fc23(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff1fe4667fa474d495f6882fbd4fb3415b1d8bab8a2528e78d2fa87dbadc2a80(
    value: typing.Optional[IotTopicRuleErrorActionS3],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e108faee455394cfc067c91f0e679b286ff8789dc184da16b9bdbf0ab9aae60f(
    *,
    role_arn: builtins.str,
    target_arn: builtins.str,
    message_format: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97e6f1a87498a265bcb9ddfb2011593650c36f0af5302e39ebc17330f47c0ad4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65167ce645e7b4e7ccb09affd26fb29a3701ac33f5c6d8fa1d6da7194f03e63e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b601d1eda660c75b29fc413157dd3656d0529d0937132276b1930176bc005042(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db80adc2f41c253b7d1b0e4b68b88ebbe09d14815480b1c20a1488248bf64993(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0233c7a96c6a307d365f4fed98c94d730400e85daa7d6c0888918cf45029f309(
    value: typing.Optional[IotTopicRuleErrorActionSns],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50c850353ddd6e0a599b8475622d3867c868ec41f35c7e47fd698fe111f7195f(
    *,
    queue_url: builtins.str,
    role_arn: builtins.str,
    use_base64: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d0636926e3861d560a40349d7669e3222a54b936ee12086a398340f422747d5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60f8355ea47492b5f137f4de1598f05469441556a6d2406845f1504270d1331b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba3010fe2faf630b5ed43c26d94d112a47316f56eea969c457697f39895dc804(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8142167db08dcf918db39d3527097ab62fddf763b31b86d270948ddf9194e852(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__300b2d0ddb9ca90609a76274ed47cf29691237a843ec036b874ccee453f03fab(
    value: typing.Optional[IotTopicRuleErrorActionSqs],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8269367c088c29125e7c8759563a43ed35850f7dfc531be70dd654cf27b561fa(
    *,
    role_arn: builtins.str,
    state_machine_name: builtins.str,
    execution_name_prefix: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c0aff059c817a5bb2aa16ef672e23cfab9ea19fcb6ccac0b3e5fa4c9071a656(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ad3510cb67b7bb8df875c630bc6aac84dbefa45bd3b17c9daa843df62b31137(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4fdbc0db41896c9772c5712ebd1713691ba530690b3dd433a19dbee2c927a18b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7baf611fdb54e384950e20ca0dfd77f4ad4e7b7b004c2c4c029079e2dfbdc573(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05ad922ce4ce7455c8c1b3c5270811c18663de0225e04963a1db0391279cb500(
    value: typing.Optional[IotTopicRuleErrorActionStepFunctions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c3ebd267f6add216c21f4f9b3ef299a69609c26b09ee33b411a7f093566f636(
    *,
    database_name: builtins.str,
    dimension: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[IotTopicRuleErrorActionTimestreamDimension, typing.Dict[builtins.str, typing.Any]]]],
    role_arn: builtins.str,
    table_name: builtins.str,
    timestamp: typing.Optional[typing.Union[IotTopicRuleErrorActionTimestreamTimestamp, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c70fae2411c45f757f16d6e8e6d00f841a08842d27504cf32b9f64f2809cf48d(
    *,
    name: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8c81e59ee190108befde35635970715fc5423e1db2d095b30161dfa18e2daa1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__982ec7d09023002404cc73d8159e55b6025886a3679e266f68c2f145e0a0d67d(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__991db1d46a9d2438799da21b41828e745819010748cc76392721cd4e51878600(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8509c41c3154734aaacd4252cce7551079aeb10a81c3b70529ca8e3aca688c88(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb8993732696614d9e2b2a689096a7c1a1814ea110e9a9a2fde35a12eba21c18(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ceaef9f5fcdc998040c342e87584306c565ddf6594855f82033e0d3d248752e(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotTopicRuleErrorActionTimestreamDimension]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1af7602a5f9f4fc793979ccbb864334e651b3b9a9f8809d08fe3e78ab998e0c5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d20aa3212c1763007de7c34ca4f7cc75813e8f5c1b2e915ba3792309449c9fad(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__937edbc0201646e580d20d1eb10f7d989dfa0cc84890c25685ba013171fbd758(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__07b559559def85ddcb4c190257793d038b3e148acf005f6d79cb9b72ec2368e0(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IotTopicRuleErrorActionTimestreamDimension]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3516b468f11c6196878fd6aa636ade91378e582163242364940287c44de9ea44(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9cfde3822a87f8679fcaf07410cddcf2935277d6296340e206373a523b442d00(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[IotTopicRuleErrorActionTimestreamDimension, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2fbafd0b0e01c226560d2402d440140bba1f195d2650a39c2cfcf4a64afb27c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__921c87ea9f25b34efe4fc1d35a2733d648d49380279d6fb50967dff898c8592c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de15e6e977552d0438fb53542946f9960352aff9ee5957b805b2678da2153e70(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5f46914e81963adfb178842808cdf7df91b102031f297f9f3e29de69c75a5fd(
    value: typing.Optional[IotTopicRuleErrorActionTimestream],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60349f463024dc1254030de3655e613eb9cce4fa5c14ac21b000ff23b2d78ee0(
    *,
    unit: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5fbfa2392f79a32a758c83a3ce00922a85e0e400740f1a1f33c88c64bd43ba46(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__472fef77d786e74f3ef3db399270bc33d4c174341c1285d6ac319d8422aba08a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa0aec99568431fffe865bfd2aa899b3991a066f0d196677128c92bc3c7bb56c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c8b84df9a0d954d311e4a2a62f9991c3dcd28afd70e86d3ac89e980252b29dc(
    value: typing.Optional[IotTopicRuleErrorActionTimestreamTimestamp],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f2407f32762933e02b48ee5c96c26b0f4208c15249e5a8522dff696849f7818(
    *,
    delivery_stream_name: builtins.str,
    role_arn: builtins.str,
    batch_mode: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    separator: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd8c00e703ae2ef23ad68d264dd63ae2759469de58a5585824529221bb822c70(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ad241da3600abc0227fe14d3fde678a9cb7d12f055fa1d60f61546604abf8fa(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2db7e8393961f419375e3c0ac48c9d762f2f17b70f1b105dbcdecf08f5ce271c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da7c3f95518033a3b47813a3decda43cf7364abc1758093bce4660c3b186306f(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60d0f3a41c50977f3e0e007e7f952c533ac351aaf994bd42199014245eed8206(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54653508a0f23c37ef1ee2811f529b3ce58d0b815bde0b6e3c0488b1ad8ea2f5(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotTopicRuleFirehose]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b2910edb15f5326f6ee6de192cd9f658801180756afcaa1c0a4f56bdf8b4d321(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b5abea5451e4b82b622c5fa6a0095f3a639371af2973d9d9e75dec5906188d71(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__000816dd917b8ad9e94a7bd36de746bd3bd46a24601ad25349a3ccf9fb246596(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc6e3b3983fbed11c7fb063311429b1ae96eee49ca27e50775e504386cf8d2ba(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc639e92d9303f80b3fd84c581763c07bd453998989ac0e3e3234e56d872f479(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb8d0a09d3056e257477ae8057b36f17c529a32eaac18f7aaca4594c933292b9(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IotTopicRuleFirehose]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b7693bff804c71775bd3d89dbf4e1621eb8ae75f3f2aea2e26e1b3cf9d5a4e8(
    *,
    url: builtins.str,
    confirmation_url: typing.Optional[builtins.str] = None,
    http_header: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[IotTopicRuleHttpHttpHeader, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1c2689d60da128f35e7f5fe2d90c0378e06da2618deb611e8d9290e0a06acbb(
    *,
    key: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a34c2d4aa7f23fccce4a675d76b83165c1f7d922ea2e7e0f94c43832564e7da3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__48c62089f281397d7ba95d04792ab28f3ae69ba653f042769a2ebcda7f92ce51(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__916c723df55492d8443a9d9b4e5305464db363aa9783d0ab226b06621debdcd1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea2aaace01dc568855c5c5657300cff18f291863d50079876de9e9ea6341be35(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b37a349447483d828f837ae4aa6945bc7308adf6e73b94adbf693ec19075158(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7027ac58eb5000e114b4527cbd8deade56ff42250aa7d0116d759ad11497e9f5(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotTopicRuleHttpHttpHeader]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1a15933d5a8722d268596a6ea346250d4666ac593626566a0564cb0972575ca(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d9e08f06e6cdae5fc46c18ca6978bb8f9bd9b11baa68eef7ffb68140503aa770(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29c5a1ed545e7c1d5b594640c758ba0e49bda775fb8fe4f665769778da6a44b9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37509a7e37c622e3e3bbedb248671bb8048382d2f8f33db8af1266a9d1bb1fdb(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IotTopicRuleHttpHttpHeader]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e746a50b794be0c43ecb2ef77d94f666b0bae62a19834f8aeabca9ee1d639544(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ad72b3417f0ef3c5a9b1db26d0e07ac9f23a2acf6863446c205025f39dc64dd(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__32e9b7da06afa094406085f7662cb7cbc1da4b3a10aee810d7468ea75f825f53(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a2f38a6e2c4d7a04fe59f8d1121127588742cf910bc7d6866d1a52ead7f3857(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f8b756d651745b6f8931069d2d4fec1f702cd278ef56918226be07fbdf360f37(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0d229974f062af3e75a2cd481be2f547be21a3e81aaea5d1a40f7f8807e7631(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotTopicRuleHttp]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85e7df63b8dcbc1d54574480030be31f7f69014577f19352ba951599eb8b1646(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d550a67f0b051e890ef192632772dba92ffb047e9d70da1ab5d5516aa1c8aab0(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[IotTopicRuleHttpHttpHeader, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cef607251c4e17e8e9bdd7e6daa961d386a265d8c611b022af76dd7313b4a691(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d09fbc02f28e25a4a9f41f3721b06d1881f471fd883c66c97891950ac568e5db(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__036e72a6b9a8997134dcd7df2f9bd808d1dd5805dc0c6418994e869471719fbd(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IotTopicRuleHttp]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1acf89f79d408b274ae5967e6b763d40db11503039a6aebec89d8bb37930785c(
    *,
    channel_name: builtins.str,
    role_arn: builtins.str,
    batch_mode: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b78895159e3231756c8376cf5d85bf11dbda1937d004dd2d603cdbb243ee955c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a41c7dd6679b1c5be29b6f58f5913f1764b430ff95f2df08a8a435a7103309df(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b042196e20d437a01a53b01fa0369216ef8814ecea0a259711649f359ff6e98(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5952699a1aee4491c694007b80ba19ebe607561cf2f929ca39b2eefc8bd08540(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09e2be84255838cb72ac08cab2eafb67da0862571049d9870cf7321db069c59e(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a334f35249b0fcdc2406292cf31915fb8ff1fb7907246ce2391684985c7eaccb(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotTopicRuleIotAnalytics]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__114ce77b3d84f21f4edfb668e07eb8a1e855a767866401203f075c65e7838f37(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5cd441144845f04ccc3114cf7550568a72446945e971c49e48e8f34d289ec04c(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9694ba7a400a3412577f18bac0dc378c9f91aa71fb20c6ed8f0c0acf47ab7dc5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14765ae0f13d1aee6f032868eb018654490ebbf995f141d61947fac140071106(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10dc05a64531bb23b6a8cdf66dcb710363bd630b5394d8d93c781570b283968b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IotTopicRuleIotAnalytics]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aeff6e9656d7547f81022f8d1a99aa1943253ce3d900767f1fe71b16be240fe4(
    *,
    input_name: builtins.str,
    role_arn: builtins.str,
    batch_mode: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    message_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__def002fd30694e7233cf79bb1cd6fb0f7716dc4b80a12f29838a0894930ad32d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__880f7e07d545515147db0349f63a5c5047aabe00062d31f8b5a890842de92056(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b612806ba8b8026a2fb0ff1c5ed7672c612811bd21d78f365c834b6f9b0ab81(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__101f2b4fc26b130dc7acd8d453f5bddc425d3243c3d99c3677544aa3efab1f42(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f2ad6bf560c0761f7c9e61603d55653f366a8f7c1ee1ba6ef346f8cab842be5(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__892b7b19483c9d794634cf2a0d0fd34e27c4ad38a55fdeeafdd32b76db099a4e(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotTopicRuleIotEvents]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd0766f6578011c35afc07a5d4802eea591bc289b13ec684b62de7678bc8c84e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3cd1977b7269de584d909ef59bbf415511eb78afa564d69c4c2d1bf9cc7636c(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3bb4e0045e0973228567a91481f5b68d1c499614ff0b8d97749e408ecfd138e6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30fb9bd6daac8266013a23ad7930dfa9b088ca50a855e74a2dd1c6944937b8ba(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96dfaaa3a03da07e3dc083411d66f9a6d1d930b95eebcf4443c5fedc76a7fef9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce077b5b3797497c6ac8e4c099604f4f056223f4c03c701a901434b1561651bc(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IotTopicRuleIotEvents]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a420929f6d1e25cac17b8e20ed8e24f94fdc5410ace45789faf10cf6aa96a166(
    *,
    client_properties: typing.Mapping[builtins.str, builtins.str],
    destination_arn: builtins.str,
    topic: builtins.str,
    header: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[IotTopicRuleKafkaHeader, typing.Dict[builtins.str, typing.Any]]]]] = None,
    key: typing.Optional[builtins.str] = None,
    partition: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25d0681d690b89709549241f10e3923c2991022c3309411b2c1a69a79ae07446(
    *,
    key: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__adadd697a8bd7eac8c48e308365cbb45b27598d4f8a04156f0a1dd200cb298ed(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5a893fbc53cf5a5eb302b3a7699804f16343c7f3ff5847c0fadc57156e015c2(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e7814510af36bd0388f211c58254e0644ea0634a71108bd236b2965ce077bab(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9925b5e3295515359ae2e7855530c9b748505560e6075618e0f80e07b821032c(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__270891820abe2987cd5ac7a986495a3d447fbbbdca5bb504c8b1b0237d26e0b0(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__279dbe30f4208bd28f9147f83b69224c898ee70798e9760fa81a0e59b1f6930d(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotTopicRuleKafkaHeader]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4cbd9aa2d8798cbbf3e992aec7225a4acc411bfc0240c56b8f449cb6f05f3fe4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10de02a0f59e8a68383e628ff583727942295a70c299b493484b2a8740f0fe22(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ba82e8f800afd469bbcdf317e8d60d9e748375c78fbac1ffee1665a27fcdf1b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__793319732c41af1f0a4a816c626c5887f40799e0f50202a7ef883f9fb3b2d41e(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IotTopicRuleKafkaHeader]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef5ddfcc2a6a149a9d1324d31e9d72a6cf6de397e0e40665b33aa4dd5d7fe2de(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9fae381e6b362edab0a2916ad952523cd2b9d896134d843f5ebd7170accd5d10(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cceb81dda95a2781d6fc2e89e28d2d08e46690b4dbfa427b4dcdecf4c4d3f77c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ea111d39843d2a9e03714325cdff315a35fb00f1759411a290cf3b687d0f131(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96e6fed207fa57d74716da3d7f4ae736efb29c6254dd2ee3903707bc2ab3deb8(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1eebbed7424610481a2094a0172d936ab9d51e8f9ab768d74a735787c49548ba(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotTopicRuleKafka]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed1248b399c98113e2e41c70c2418aa026a007f9594dc548da4766c36360ba2a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9876d62d9567165ca90caef0356e5a9235447b8611959d620874ca253f0bec7f(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[IotTopicRuleKafkaHeader, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d18e62d8102228baed8ab17ea9a475f7a17ebf7c5442b9779444bf04ee82cb5(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__48b7a2461b163506fab8f19d747a3b96f7c542eb397f65ed2f42e581de392bca(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87cb32d4570ad3cb83494ccd78f6b23f46a477bb4d127435c4bc88f049d3e8ef(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b29a2924c8af3a49721358b0c955eb9530cb355ea838f0693e47cf611f26695(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3dc5ee960bc7a30255caef46ac350b4bcf4786577e9171102e5d44b8a782c039(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__811e83960191fafb13d93f83e143f80263a84dc77d48a79ade67f7585a01265c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IotTopicRuleKafka]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__062385a302701e6a2156135f177b9b337064838f46ad3cdc3f954ee38d02a482(
    *,
    role_arn: builtins.str,
    stream_name: builtins.str,
    partition_key: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c59616133323149c17d1530f2e12ff95abbbc5c917a16b4c022655335f000082(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__becf579c1bd05084bba0af79adefe1d2ac65fd06269d9526680c6fbc434b2391(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b5d2dfb20848ed84fd3c49f776fd9b453efa16bc92305486012d52e706213c0e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b81c457dcf50188550e0d02990402c3b779cf3ac358c7555ada6f8fc837a1001(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b668fcbd77f093393e64406b21b96bf8cbf0aaf5a010c8fa34c423d27046a43(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50833ef6f1cdd625d6ee5484fabd38a200b5f5fa14fc2eb8d7b82f0159facfb8(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotTopicRuleKinesis]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09a8015b4eb688b3a57bb7581a2474636bb02d0261ba4ba38f5aa1f8ed143490(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aec69ef14d4df6404eebecac945451ffd4eed8227419e83b61f4789029c7cebe(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5aa8a532cc2f92331083a4eabb6d96cabd4283b08e80999a898a39f96e1f9b4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__579bee74dc3aa791fb656746baf324f0b9288e6f36211ae7c7f795b3ed7abf1a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c5e8af74d58dda39300c013e04b4e912ecc78dd471e9a598ee050730f1108c0(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IotTopicRuleKinesis]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__84e7b3a0537f489d04dfd1b914e393a11a109c4d3fe34cccb51445de35d3adf3(
    *,
    function_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dfb35d19ddd5bfd955aa43ca0fbc16378bf3ddb4c59e3b17a000e711fa46a863(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7f7e130c45283b58dc229ca5a5ea4394760a2ddb0cbb5a5388f2bc99320c1e3(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c046fc1824325e9e68f6389ac90e5434c00785b5ff2b69753bb2076da7aaa141(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39291bcce80a45d818676ccd4fe3705652151caba4baafe9c0cd1b0813128f23(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f59ceef137dc4e12098dcef39887a32f704dd48d08ea8d0154191455275428e8(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eabd6e3ce34589309d680a7eaf8c75924ea2318b3abcfa5d0f012a634dde0776(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotTopicRuleLambda]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__643699ec2dc6868e56f0033ec40d9d20dc07d3b5f782bcfd334727a1acb48248(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60e7451b07f4db559f8e555641bcbe82f7a12fe058709faecc85e126d999ef14(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b6b55888e1677887ac01cf25f6804162f3c900b99bec3523d79f44fdde6417f(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IotTopicRuleLambda]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1cb8cbb0bc8a283ba49a3854d9eb0fb622b2a8e6fcabb701df589d4b809efd56(
    *,
    role_arn: builtins.str,
    topic: builtins.str,
    qos: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__35beaab1d030efd7319396d103d69292be2614d8402f3c599cf74d7c62623cee(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7020105450733742cd7655f130de697c3a9e06c194614bf44e783955e15457a(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1eba2d6ed5958efc283b28944a6123b81d00734acceb2e0c6582fb6aa1c120a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a211f53d99dd5bf4b76c97cfd35926c738f083ab72161d0425f63f74a0854e1(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__874ad9b4fc46a8f0797da9da9b1ead20fb21f2e4a1323299472385ce4022bd70(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2df5ec5c78f6364d3877893853d168031f78861ddc6ae30957f1872737cb460c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotTopicRuleRepublish]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87df998ab5f692926bafaf3700e429e046630c353e789bbb32dbf751c567b602(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a3165dac74885a66eaa73d3c7b77b06901bca48b025bd08a333e040fbf53e77(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e755b94197fa41473202e7aa6661772032e7a27920963929ca463f65ea0578a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef89fe3fcd1c53306caf557ce1856817601db083efeec144e98e22b17e36cb41(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c215249cbda990d781e3a502a924adc052132a487a5894ee5d2fe1f930e1ef5(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IotTopicRuleRepublish]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4a09c9b8cc7e35ca17f0a9286ec3f59731bcc7198e7d281eb4ab2a75d688283(
    *,
    bucket_name: builtins.str,
    key: builtins.str,
    role_arn: builtins.str,
    canned_acl: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0280766fc39d7bdc6b610345b334639c0aab4178991fbadbbe7c56fec9d4e38(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26a617da386fa36d707e4e33ddee2042a3d58545f2faa35e69168433fe9e7399(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__441f899d3ca2c8bc4126d502a43780d856eec26dccfdd2363a53d4aee6a5a4ec(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3fc97e6048e5390539cad97adc5eb7ea9cbefb2d1e7128918b636aaa1f32ba6(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae3ef95f375ff8d285d6d9185bd1635d27ef6af65b0944c68dc7177292e0ba24(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3ad80abe39885dc08e4acc6819c0eef5a00f05fd60c6432c2b3b089109d9127(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotTopicRuleS3]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0727da25686dd666ad96bc620c6f93f9c53594b57ad37978aca7b5daa643b9ba(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2dda05853d79bb63a301294a7080a14a02a1b59494b1c27dc8ecc60c83fa8cad(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__665e4945c5fd322f919d5118699ccf16cef90bbcfd6b26b61290c1714c03e9e4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4eac30268a29a4549d6d4423f9294ca4fc5f180a9604e4280a4de83fcb36a7cd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e57294801010771cf6c7c203c7a8a7452ebee9899fa135e9eec73c0350e4df0e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9d1ffbfeff2a0e42933364f4a265f573f2c612454485256feaa5bbcfc477a8b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IotTopicRuleS3]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3dd8545051208d4cf8fd4be5be794c494d937a8f172a1c8d54592fdbbfa89e7c(
    *,
    role_arn: builtins.str,
    target_arn: builtins.str,
    message_format: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aaa6c30505948fedc87312903160863197a4bac2c9595f6624a3e5b89cecf967(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2bdab9c72d230aa483bbc82392c4202f89067bec505bc3490eda36c48d9be97a(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0fa9eef7adc7dc88acb544fa217c59a4fa51276682e23f5f06a076af54202ae8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7f67825877be63195323021fa1869aa0e9816ac6065c6f13ced19371b4e6cc7(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca96bacd1c1d03054d7ae5cab349d336050bf7e7c9b42e3f28b5bf811c1e9fa1(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d51b8701dd4019f17f6d6b9ab7be0581637aa53459e7f8f6e3ee3d4d5091a106(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotTopicRuleSns]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__17ab219720df1de953b74fe6a03ad77dcb91b6483b4111669e104e2b8ef2631d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e1d6a228bc0298bc359cefb6c5352c24ad33f221c5ae078b80ca36251e3517e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5fcf9b617f87b8389663fa505bd33e445e4ec0588b220f5436e97cfc6c6c43d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0983f86413cbc80a67f5ea729fcec65c10fb57f0eadb450d1bfcd8d20a021bd7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9a16f448b7b7e99b72183f6e821283f85981c71c03af5edcba2d547d5e6223c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IotTopicRuleSns]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87be092475616b2a595901ac2b1ceb45a42327fb8789d611fba9a053c686664e(
    *,
    queue_url: builtins.str,
    role_arn: builtins.str,
    use_base64: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__594433d2c8cd7084e8c1a05fd71e0d59ca3a8133f319ac7fd5222c56c356d412(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd6714795b19aeb1579e4d43ae979fca095ef9746ad76b4dda0fe96558d86a4e(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c3f664b074f5c5aa7afa3aa638d9f7e18da9e810ffa65fdb0867d0ce5748044(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ecbc1f1772f50fd00aa659a980430ec9605b95e85652393cbfcaa115405425a3(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d29a64b2e4cadcf526adbba02b6edf6c662ba8aaada84f78c89185bbaddc7515(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5cea5ce6c73a618cb2f568275c434e105979ce30be3ae8d31e32057e89e3abcf(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotTopicRuleSqs]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c9f5e8902a2b05ab046a56c3ec3d19d8763f400691870454074703189d6a1cb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75f1d6ca4173a6f7b5bf8f7af0c8d4003204adcd69a199ec9bf7c6005e7f8770(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dbc46ccded0b4bd945d012ff9d3a8b752a85e2163c590d7e58a776df0f2b1a11(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80a3474b825487a8a3e0a7cea85880d59e0a3690df7a48f49058893ed7504532(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed097d87f222b2ec52400c7283de5b3c894445ff0f391641817742540b39c977(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IotTopicRuleSqs]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a791bfa4239d12237434677830c9f9194e5bef70c35dc356b34c685b1e02a296(
    *,
    role_arn: builtins.str,
    state_machine_name: builtins.str,
    execution_name_prefix: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__01e43c7a4576626c4260b0f0746f6b45a336572053916f5d180865e6ecfb10c0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad0e869c1335d63e3fcfbe8240aa6fbdbc0ba91f05412941c9037fa27d7496f2(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__832ae843de3e059baee0b14984014c3dcf704857aebd399d62d2f63da639f872(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ba3dcc5bd613962ccc1694d59a2622d8a2724c3390f4aa09c3f4f296ad92344(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ccb4dbcce7ab65e60a3aae96d26c3955f129672c3eec8bdf6412909c96a46bc8(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb06507fef79c324f48420bf29d81519af389f76f62b834a63f72118970ef781(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotTopicRuleStepFunctions]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3efd9745cea5f85dd3b4da86d0e4f17d997890bb69be07e127a52de42476d1d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92cc29d83a0abc553928215a9b1d6c4a1285ef04f7ee4f43e42fcb112fee6a9f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e516c173476439356434a328695472b1c712da7240d8cf1ba56b43295699cc94(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__429ad679b8ca07b2374626e849ed1b43eee5c0839813fdea2e76682005e63a40(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2381b969c7b0ad41a27d834ff539a3447367fe18bc786a25130875ac8ec55d0(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IotTopicRuleStepFunctions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37bf62ba9b3390f2287f2dbe483ded0b2e36329f74ccec7c0e3cee7e1474f156(
    *,
    database_name: builtins.str,
    dimension: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[IotTopicRuleTimestreamDimension, typing.Dict[builtins.str, typing.Any]]]],
    role_arn: builtins.str,
    table_name: builtins.str,
    timestamp: typing.Optional[typing.Union[IotTopicRuleTimestreamTimestamp, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dbbf6291fb1070bb7e53cabaf8c4b8625f06aa1bfd2fed4aa9f7ed77ab5a841f(
    *,
    name: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7552bbd00412d3918bcd88beaade7fb140a3cc550fa1bf25b2b04e2331209b2d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44a2a1b10f4d5394118ccccabe1213054bf38ff5f85ecf65a645b55dd365e7da(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4193d015b2b3a21dcb91278c7142c229fbc52f823d52dd0f49757a5082f1e06(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd87436712578b32c2243f3d2721cc1f51bfdccae77fcc5b9ed66f1fc218a691(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c00f5c0f7ae27121a7747e7d0bff8c8b6bbfc30a746088d82906ece46c0b32bc(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97356ca1a16f3ff5f218cd6af81f3e202ec3b79f62521f1d57c0600ce82ba2fe(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotTopicRuleTimestreamDimension]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__815dfd0b998940e52b7e73c20315d9561e8b24c8b4a9d84e38a0748df0479d78(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7102cb2bb14de0686c2b007b56aca72c06f7e8105f96911c09840ad0cff9fdc6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1660c65a32940b42352eb7fafc6faedb466a7a13dc3a0d38c48c298274140f01(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1dbdc44196665cda518f92fcbfbf3f3dd933a248057af7b374d757f38e9433ef(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IotTopicRuleTimestreamDimension]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2223545299273a6043fbe787cf39d7f0b4ba350dbbd0fc24efc40738348a6ead(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a51c2ddcd45c0ac23e441063e5b7883a9ad5c8084ad91b19e5506ca23ad9d58(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__456edab77c14b9d7dea8e61aa3d84de9085d4c68f4a3cea09394da57898849eb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8ce3cc0f6e4328f441a68c088cb31701391b55496266a4d2f3b6f239d358c2f(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__49b762295fa640cb3a08ccdb522ae268b9e6a9db559e50fdb494d9b7f7b4d7a3(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2b073b051f8b09e033bebd67a0655e5281883a01694cb200aa6bca7624f60c0(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotTopicRuleTimestream]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f749026ec5db96778046ccfabdc3204f96528950fdf8f0bd60015665dfd7a5c9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7cc6d79a3d1bea5d9ef4753853458d2e0c6ff6b9e66fb7e7bba695ef3285266(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[IotTopicRuleTimestreamDimension, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45c07a6f425f5a36e6c19d45b7873c652d8a048b80547f0d39148ad13f76a905(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71e259ff4d73e7afc70b0ca296e49b5728005005f46cbee66452bd7953975f79(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__579bbb0f75262734a2484f3522c041000c85f2467f76889489e1257cbb1caf7f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0fbb26c73307a07ae292db0be29fe7322bf2bfc6311ca949f4d33390d4c17a52(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IotTopicRuleTimestream]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0deb5be66a882a98babc505c71c21d4a35989a29b1d1c495ddfc07f50c138e09(
    *,
    unit: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__642cd6aacf6f04dfd726eebf48e34e70179caeafd853f53b6e5a31e4994bf15a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ca137af8ca309589033bf32d449a5446091ea39cabbaa611ce6aa996d89948e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6af01097b751c2c1518fbaadd5365d74b9850a83c8c60010cee0553b5506833a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4edd5db0df430bad3db1f61c0e881162fded813fea9698daf5580b406733c978(
    value: typing.Optional[IotTopicRuleTimestreamTimestamp],
) -> None:
    """Type checking stubs"""
    pass
