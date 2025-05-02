r'''
# `aws_pipes_pipe`

Refer to the Terraform Registry for docs: [`aws_pipes_pipe`](https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe).
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


class PipesPipe(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.pipesPipe.PipesPipe",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe aws_pipes_pipe}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        role_arn: builtins.str,
        source: builtins.str,
        target: builtins.str,
        description: typing.Optional[builtins.str] = None,
        desired_state: typing.Optional[builtins.str] = None,
        enrichment: typing.Optional[builtins.str] = None,
        enrichment_parameters: typing.Optional[typing.Union["PipesPipeEnrichmentParameters", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        kms_key_identifier: typing.Optional[builtins.str] = None,
        log_configuration: typing.Optional[typing.Union["PipesPipeLogConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        name: typing.Optional[builtins.str] = None,
        name_prefix: typing.Optional[builtins.str] = None,
        source_parameters: typing.Optional[typing.Union["PipesPipeSourceParameters", typing.Dict[builtins.str, typing.Any]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        target_parameters: typing.Optional[typing.Union["PipesPipeTargetParameters", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["PipesPipeTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe aws_pipes_pipe} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#role_arn PipesPipe#role_arn}.
        :param source: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#source PipesPipe#source}.
        :param target: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#target PipesPipe#target}.
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#description PipesPipe#description}.
        :param desired_state: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#desired_state PipesPipe#desired_state}.
        :param enrichment: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#enrichment PipesPipe#enrichment}.
        :param enrichment_parameters: enrichment_parameters block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#enrichment_parameters PipesPipe#enrichment_parameters}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#id PipesPipe#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param kms_key_identifier: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#kms_key_identifier PipesPipe#kms_key_identifier}.
        :param log_configuration: log_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#log_configuration PipesPipe#log_configuration}
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#name PipesPipe#name}.
        :param name_prefix: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#name_prefix PipesPipe#name_prefix}.
        :param source_parameters: source_parameters block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#source_parameters PipesPipe#source_parameters}
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#tags PipesPipe#tags}.
        :param tags_all: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#tags_all PipesPipe#tags_all}.
        :param target_parameters: target_parameters block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#target_parameters PipesPipe#target_parameters}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#timeouts PipesPipe#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__25885b4e0fb316c42c6c2b5247fd1261829169b06d99c4566cf95bb674ef0a8c)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = PipesPipeConfig(
            role_arn=role_arn,
            source=source,
            target=target,
            description=description,
            desired_state=desired_state,
            enrichment=enrichment,
            enrichment_parameters=enrichment_parameters,
            id=id,
            kms_key_identifier=kms_key_identifier,
            log_configuration=log_configuration,
            name=name,
            name_prefix=name_prefix,
            source_parameters=source_parameters,
            tags=tags,
            tags_all=tags_all,
            target_parameters=target_parameters,
            timeouts=timeouts,
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
        '''Generates CDKTF code for importing a PipesPipe resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the PipesPipe to import.
        :param import_from_id: The id of the existing PipesPipe that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the PipesPipe to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ed0c64209bafa15ff4a6394e5192797fbc46297d1fe6b85f1ee939463112906c)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putEnrichmentParameters")
    def put_enrichment_parameters(
        self,
        *,
        http_parameters: typing.Optional[typing.Union["PipesPipeEnrichmentParametersHttpParameters", typing.Dict[builtins.str, typing.Any]]] = None,
        input_template: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param http_parameters: http_parameters block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#http_parameters PipesPipe#http_parameters}
        :param input_template: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#input_template PipesPipe#input_template}.
        '''
        value = PipesPipeEnrichmentParameters(
            http_parameters=http_parameters, input_template=input_template
        )

        return typing.cast(None, jsii.invoke(self, "putEnrichmentParameters", [value]))

    @jsii.member(jsii_name="putLogConfiguration")
    def put_log_configuration(
        self,
        *,
        level: builtins.str,
        cloudwatch_logs_log_destination: typing.Optional[typing.Union["PipesPipeLogConfigurationCloudwatchLogsLogDestination", typing.Dict[builtins.str, typing.Any]]] = None,
        firehose_log_destination: typing.Optional[typing.Union["PipesPipeLogConfigurationFirehoseLogDestination", typing.Dict[builtins.str, typing.Any]]] = None,
        include_execution_data: typing.Optional[typing.Sequence[builtins.str]] = None,
        s3_log_destination: typing.Optional[typing.Union["PipesPipeLogConfigurationS3LogDestination", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param level: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#level PipesPipe#level}.
        :param cloudwatch_logs_log_destination: cloudwatch_logs_log_destination block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#cloudwatch_logs_log_destination PipesPipe#cloudwatch_logs_log_destination}
        :param firehose_log_destination: firehose_log_destination block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#firehose_log_destination PipesPipe#firehose_log_destination}
        :param include_execution_data: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#include_execution_data PipesPipe#include_execution_data}.
        :param s3_log_destination: s3_log_destination block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#s3_log_destination PipesPipe#s3_log_destination}
        '''
        value = PipesPipeLogConfiguration(
            level=level,
            cloudwatch_logs_log_destination=cloudwatch_logs_log_destination,
            firehose_log_destination=firehose_log_destination,
            include_execution_data=include_execution_data,
            s3_log_destination=s3_log_destination,
        )

        return typing.cast(None, jsii.invoke(self, "putLogConfiguration", [value]))

    @jsii.member(jsii_name="putSourceParameters")
    def put_source_parameters(
        self,
        *,
        activemq_broker_parameters: typing.Optional[typing.Union["PipesPipeSourceParametersActivemqBrokerParameters", typing.Dict[builtins.str, typing.Any]]] = None,
        dynamodb_stream_parameters: typing.Optional[typing.Union["PipesPipeSourceParametersDynamodbStreamParameters", typing.Dict[builtins.str, typing.Any]]] = None,
        filter_criteria: typing.Optional[typing.Union["PipesPipeSourceParametersFilterCriteria", typing.Dict[builtins.str, typing.Any]]] = None,
        kinesis_stream_parameters: typing.Optional[typing.Union["PipesPipeSourceParametersKinesisStreamParameters", typing.Dict[builtins.str, typing.Any]]] = None,
        managed_streaming_kafka_parameters: typing.Optional[typing.Union["PipesPipeSourceParametersManagedStreamingKafkaParameters", typing.Dict[builtins.str, typing.Any]]] = None,
        rabbitmq_broker_parameters: typing.Optional[typing.Union["PipesPipeSourceParametersRabbitmqBrokerParameters", typing.Dict[builtins.str, typing.Any]]] = None,
        self_managed_kafka_parameters: typing.Optional[typing.Union["PipesPipeSourceParametersSelfManagedKafkaParameters", typing.Dict[builtins.str, typing.Any]]] = None,
        sqs_queue_parameters: typing.Optional[typing.Union["PipesPipeSourceParametersSqsQueueParameters", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param activemq_broker_parameters: activemq_broker_parameters block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#activemq_broker_parameters PipesPipe#activemq_broker_parameters}
        :param dynamodb_stream_parameters: dynamodb_stream_parameters block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#dynamodb_stream_parameters PipesPipe#dynamodb_stream_parameters}
        :param filter_criteria: filter_criteria block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#filter_criteria PipesPipe#filter_criteria}
        :param kinesis_stream_parameters: kinesis_stream_parameters block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#kinesis_stream_parameters PipesPipe#kinesis_stream_parameters}
        :param managed_streaming_kafka_parameters: managed_streaming_kafka_parameters block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#managed_streaming_kafka_parameters PipesPipe#managed_streaming_kafka_parameters}
        :param rabbitmq_broker_parameters: rabbitmq_broker_parameters block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#rabbitmq_broker_parameters PipesPipe#rabbitmq_broker_parameters}
        :param self_managed_kafka_parameters: self_managed_kafka_parameters block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#self_managed_kafka_parameters PipesPipe#self_managed_kafka_parameters}
        :param sqs_queue_parameters: sqs_queue_parameters block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#sqs_queue_parameters PipesPipe#sqs_queue_parameters}
        '''
        value = PipesPipeSourceParameters(
            activemq_broker_parameters=activemq_broker_parameters,
            dynamodb_stream_parameters=dynamodb_stream_parameters,
            filter_criteria=filter_criteria,
            kinesis_stream_parameters=kinesis_stream_parameters,
            managed_streaming_kafka_parameters=managed_streaming_kafka_parameters,
            rabbitmq_broker_parameters=rabbitmq_broker_parameters,
            self_managed_kafka_parameters=self_managed_kafka_parameters,
            sqs_queue_parameters=sqs_queue_parameters,
        )

        return typing.cast(None, jsii.invoke(self, "putSourceParameters", [value]))

    @jsii.member(jsii_name="putTargetParameters")
    def put_target_parameters(
        self,
        *,
        batch_job_parameters: typing.Optional[typing.Union["PipesPipeTargetParametersBatchJobParameters", typing.Dict[builtins.str, typing.Any]]] = None,
        cloudwatch_logs_parameters: typing.Optional[typing.Union["PipesPipeTargetParametersCloudwatchLogsParameters", typing.Dict[builtins.str, typing.Any]]] = None,
        ecs_task_parameters: typing.Optional[typing.Union["PipesPipeTargetParametersEcsTaskParameters", typing.Dict[builtins.str, typing.Any]]] = None,
        eventbridge_event_bus_parameters: typing.Optional[typing.Union["PipesPipeTargetParametersEventbridgeEventBusParameters", typing.Dict[builtins.str, typing.Any]]] = None,
        http_parameters: typing.Optional[typing.Union["PipesPipeTargetParametersHttpParameters", typing.Dict[builtins.str, typing.Any]]] = None,
        input_template: typing.Optional[builtins.str] = None,
        kinesis_stream_parameters: typing.Optional[typing.Union["PipesPipeTargetParametersKinesisStreamParameters", typing.Dict[builtins.str, typing.Any]]] = None,
        lambda_function_parameters: typing.Optional[typing.Union["PipesPipeTargetParametersLambdaFunctionParameters", typing.Dict[builtins.str, typing.Any]]] = None,
        redshift_data_parameters: typing.Optional[typing.Union["PipesPipeTargetParametersRedshiftDataParameters", typing.Dict[builtins.str, typing.Any]]] = None,
        sagemaker_pipeline_parameters: typing.Optional[typing.Union["PipesPipeTargetParametersSagemakerPipelineParameters", typing.Dict[builtins.str, typing.Any]]] = None,
        sqs_queue_parameters: typing.Optional[typing.Union["PipesPipeTargetParametersSqsQueueParameters", typing.Dict[builtins.str, typing.Any]]] = None,
        step_function_state_machine_parameters: typing.Optional[typing.Union["PipesPipeTargetParametersStepFunctionStateMachineParameters", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param batch_job_parameters: batch_job_parameters block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#batch_job_parameters PipesPipe#batch_job_parameters}
        :param cloudwatch_logs_parameters: cloudwatch_logs_parameters block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#cloudwatch_logs_parameters PipesPipe#cloudwatch_logs_parameters}
        :param ecs_task_parameters: ecs_task_parameters block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#ecs_task_parameters PipesPipe#ecs_task_parameters}
        :param eventbridge_event_bus_parameters: eventbridge_event_bus_parameters block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#eventbridge_event_bus_parameters PipesPipe#eventbridge_event_bus_parameters}
        :param http_parameters: http_parameters block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#http_parameters PipesPipe#http_parameters}
        :param input_template: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#input_template PipesPipe#input_template}.
        :param kinesis_stream_parameters: kinesis_stream_parameters block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#kinesis_stream_parameters PipesPipe#kinesis_stream_parameters}
        :param lambda_function_parameters: lambda_function_parameters block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#lambda_function_parameters PipesPipe#lambda_function_parameters}
        :param redshift_data_parameters: redshift_data_parameters block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#redshift_data_parameters PipesPipe#redshift_data_parameters}
        :param sagemaker_pipeline_parameters: sagemaker_pipeline_parameters block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#sagemaker_pipeline_parameters PipesPipe#sagemaker_pipeline_parameters}
        :param sqs_queue_parameters: sqs_queue_parameters block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#sqs_queue_parameters PipesPipe#sqs_queue_parameters}
        :param step_function_state_machine_parameters: step_function_state_machine_parameters block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#step_function_state_machine_parameters PipesPipe#step_function_state_machine_parameters}
        '''
        value = PipesPipeTargetParameters(
            batch_job_parameters=batch_job_parameters,
            cloudwatch_logs_parameters=cloudwatch_logs_parameters,
            ecs_task_parameters=ecs_task_parameters,
            eventbridge_event_bus_parameters=eventbridge_event_bus_parameters,
            http_parameters=http_parameters,
            input_template=input_template,
            kinesis_stream_parameters=kinesis_stream_parameters,
            lambda_function_parameters=lambda_function_parameters,
            redshift_data_parameters=redshift_data_parameters,
            sagemaker_pipeline_parameters=sagemaker_pipeline_parameters,
            sqs_queue_parameters=sqs_queue_parameters,
            step_function_state_machine_parameters=step_function_state_machine_parameters,
        )

        return typing.cast(None, jsii.invoke(self, "putTargetParameters", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#create PipesPipe#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#delete PipesPipe#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#update PipesPipe#update}.
        '''
        value = PipesPipeTimeouts(create=create, delete=delete, update=update)

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetDesiredState")
    def reset_desired_state(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDesiredState", []))

    @jsii.member(jsii_name="resetEnrichment")
    def reset_enrichment(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnrichment", []))

    @jsii.member(jsii_name="resetEnrichmentParameters")
    def reset_enrichment_parameters(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnrichmentParameters", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetKmsKeyIdentifier")
    def reset_kms_key_identifier(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKmsKeyIdentifier", []))

    @jsii.member(jsii_name="resetLogConfiguration")
    def reset_log_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLogConfiguration", []))

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @jsii.member(jsii_name="resetNamePrefix")
    def reset_name_prefix(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNamePrefix", []))

    @jsii.member(jsii_name="resetSourceParameters")
    def reset_source_parameters(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSourceParameters", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

    @jsii.member(jsii_name="resetTagsAll")
    def reset_tags_all(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTagsAll", []))

    @jsii.member(jsii_name="resetTargetParameters")
    def reset_target_parameters(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTargetParameters", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

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
    @jsii.member(jsii_name="enrichmentParameters")
    def enrichment_parameters(self) -> "PipesPipeEnrichmentParametersOutputReference":
        return typing.cast("PipesPipeEnrichmentParametersOutputReference", jsii.get(self, "enrichmentParameters"))

    @builtins.property
    @jsii.member(jsii_name="logConfiguration")
    def log_configuration(self) -> "PipesPipeLogConfigurationOutputReference":
        return typing.cast("PipesPipeLogConfigurationOutputReference", jsii.get(self, "logConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="sourceParameters")
    def source_parameters(self) -> "PipesPipeSourceParametersOutputReference":
        return typing.cast("PipesPipeSourceParametersOutputReference", jsii.get(self, "sourceParameters"))

    @builtins.property
    @jsii.member(jsii_name="targetParameters")
    def target_parameters(self) -> "PipesPipeTargetParametersOutputReference":
        return typing.cast("PipesPipeTargetParametersOutputReference", jsii.get(self, "targetParameters"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "PipesPipeTimeoutsOutputReference":
        return typing.cast("PipesPipeTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="desiredStateInput")
    def desired_state_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "desiredStateInput"))

    @builtins.property
    @jsii.member(jsii_name="enrichmentInput")
    def enrichment_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "enrichmentInput"))

    @builtins.property
    @jsii.member(jsii_name="enrichmentParametersInput")
    def enrichment_parameters_input(
        self,
    ) -> typing.Optional["PipesPipeEnrichmentParameters"]:
        return typing.cast(typing.Optional["PipesPipeEnrichmentParameters"], jsii.get(self, "enrichmentParametersInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="kmsKeyIdentifierInput")
    def kms_key_identifier_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "kmsKeyIdentifierInput"))

    @builtins.property
    @jsii.member(jsii_name="logConfigurationInput")
    def log_configuration_input(self) -> typing.Optional["PipesPipeLogConfiguration"]:
        return typing.cast(typing.Optional["PipesPipeLogConfiguration"], jsii.get(self, "logConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="namePrefixInput")
    def name_prefix_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "namePrefixInput"))

    @builtins.property
    @jsii.member(jsii_name="roleArnInput")
    def role_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "roleArnInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceInput")
    def source_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sourceInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceParametersInput")
    def source_parameters_input(self) -> typing.Optional["PipesPipeSourceParameters"]:
        return typing.cast(typing.Optional["PipesPipeSourceParameters"], jsii.get(self, "sourceParametersInput"))

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
    @jsii.member(jsii_name="targetInput")
    def target_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "targetInput"))

    @builtins.property
    @jsii.member(jsii_name="targetParametersInput")
    def target_parameters_input(self) -> typing.Optional["PipesPipeTargetParameters"]:
        return typing.cast(typing.Optional["PipesPipeTargetParameters"], jsii.get(self, "targetParametersInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "PipesPipeTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "PipesPipeTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d1d792de6252214cb180174ceee67d57cc44ab15d73ca19a9d5348be93dcde91)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="desiredState")
    def desired_state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "desiredState"))

    @desired_state.setter
    def desired_state(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__52ee1691aa8105ac9452371c12f8019b64d4401a54a30b63a26b791ba509d97b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "desiredState", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enrichment")
    def enrichment(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "enrichment"))

    @enrichment.setter
    def enrichment(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__961cb2fd2deb99e302a5ebc6a31289897c4cfd3b07560bed2e81bb4dc4053e8b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enrichment", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ce9cc79b7535a7182c02f917195a8062d24fab1422db949b37fbe3d72ec8347)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="kmsKeyIdentifier")
    def kms_key_identifier(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kmsKeyIdentifier"))

    @kms_key_identifier.setter
    def kms_key_identifier(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__00b8d214503c15d90fdb8fe580b468a06b7036aac4dd78f0e4038128e1b2e6a9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsKeyIdentifier", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b443ab7ab30202f38d825e8debde4e40a2880a594344d4603199da796acb88e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="namePrefix")
    def name_prefix(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "namePrefix"))

    @name_prefix.setter
    def name_prefix(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c1a30f830cf2edf50945c53e7f47fdadead73bc01ba9faae8028c2479c3fdc4a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "namePrefix", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="roleArn")
    def role_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "roleArn"))

    @role_arn.setter
    def role_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0faee8788df24e0f8222c7df89108b4b8af16d89bcab8234342e0ac657a9d544)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "roleArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="source")
    def source(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "source"))

    @source.setter
    def source(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4727e13a56e2bc3ed9ab10ca9775597703c6dc57191d492db05aa51e5d4d4cb7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "source", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__93090979eefd3db77df31dcdc5315ee12bf96501da990e34bc3b70c912b569ad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tagsAll")
    def tags_all(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tagsAll"))

    @tags_all.setter
    def tags_all(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c4ced249a2a92c449fe88378bc53c24d400362fc08d2dfd75a552460ac0189c8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tagsAll", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="target")
    def target(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "target"))

    @target.setter
    def target(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3d9ea5e619eff4677881205f48025c7a9df55e7fa58999bdd43bbb5720fb3498)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "target", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.pipesPipe.PipesPipeConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "role_arn": "roleArn",
        "source": "source",
        "target": "target",
        "description": "description",
        "desired_state": "desiredState",
        "enrichment": "enrichment",
        "enrichment_parameters": "enrichmentParameters",
        "id": "id",
        "kms_key_identifier": "kmsKeyIdentifier",
        "log_configuration": "logConfiguration",
        "name": "name",
        "name_prefix": "namePrefix",
        "source_parameters": "sourceParameters",
        "tags": "tags",
        "tags_all": "tagsAll",
        "target_parameters": "targetParameters",
        "timeouts": "timeouts",
    },
)
class PipesPipeConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        role_arn: builtins.str,
        source: builtins.str,
        target: builtins.str,
        description: typing.Optional[builtins.str] = None,
        desired_state: typing.Optional[builtins.str] = None,
        enrichment: typing.Optional[builtins.str] = None,
        enrichment_parameters: typing.Optional[typing.Union["PipesPipeEnrichmentParameters", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        kms_key_identifier: typing.Optional[builtins.str] = None,
        log_configuration: typing.Optional[typing.Union["PipesPipeLogConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        name: typing.Optional[builtins.str] = None,
        name_prefix: typing.Optional[builtins.str] = None,
        source_parameters: typing.Optional[typing.Union["PipesPipeSourceParameters", typing.Dict[builtins.str, typing.Any]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        target_parameters: typing.Optional[typing.Union["PipesPipeTargetParameters", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["PipesPipeTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#role_arn PipesPipe#role_arn}.
        :param source: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#source PipesPipe#source}.
        :param target: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#target PipesPipe#target}.
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#description PipesPipe#description}.
        :param desired_state: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#desired_state PipesPipe#desired_state}.
        :param enrichment: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#enrichment PipesPipe#enrichment}.
        :param enrichment_parameters: enrichment_parameters block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#enrichment_parameters PipesPipe#enrichment_parameters}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#id PipesPipe#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param kms_key_identifier: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#kms_key_identifier PipesPipe#kms_key_identifier}.
        :param log_configuration: log_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#log_configuration PipesPipe#log_configuration}
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#name PipesPipe#name}.
        :param name_prefix: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#name_prefix PipesPipe#name_prefix}.
        :param source_parameters: source_parameters block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#source_parameters PipesPipe#source_parameters}
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#tags PipesPipe#tags}.
        :param tags_all: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#tags_all PipesPipe#tags_all}.
        :param target_parameters: target_parameters block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#target_parameters PipesPipe#target_parameters}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#timeouts PipesPipe#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(enrichment_parameters, dict):
            enrichment_parameters = PipesPipeEnrichmentParameters(**enrichment_parameters)
        if isinstance(log_configuration, dict):
            log_configuration = PipesPipeLogConfiguration(**log_configuration)
        if isinstance(source_parameters, dict):
            source_parameters = PipesPipeSourceParameters(**source_parameters)
        if isinstance(target_parameters, dict):
            target_parameters = PipesPipeTargetParameters(**target_parameters)
        if isinstance(timeouts, dict):
            timeouts = PipesPipeTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ae38792413ea6deb395b6ee564a80d644beef47bef13eac262d03c08a6ec82f)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
            check_type(argname="argument source", value=source, expected_type=type_hints["source"])
            check_type(argname="argument target", value=target, expected_type=type_hints["target"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument desired_state", value=desired_state, expected_type=type_hints["desired_state"])
            check_type(argname="argument enrichment", value=enrichment, expected_type=type_hints["enrichment"])
            check_type(argname="argument enrichment_parameters", value=enrichment_parameters, expected_type=type_hints["enrichment_parameters"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument kms_key_identifier", value=kms_key_identifier, expected_type=type_hints["kms_key_identifier"])
            check_type(argname="argument log_configuration", value=log_configuration, expected_type=type_hints["log_configuration"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument name_prefix", value=name_prefix, expected_type=type_hints["name_prefix"])
            check_type(argname="argument source_parameters", value=source_parameters, expected_type=type_hints["source_parameters"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument tags_all", value=tags_all, expected_type=type_hints["tags_all"])
            check_type(argname="argument target_parameters", value=target_parameters, expected_type=type_hints["target_parameters"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "role_arn": role_arn,
            "source": source,
            "target": target,
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
        if description is not None:
            self._values["description"] = description
        if desired_state is not None:
            self._values["desired_state"] = desired_state
        if enrichment is not None:
            self._values["enrichment"] = enrichment
        if enrichment_parameters is not None:
            self._values["enrichment_parameters"] = enrichment_parameters
        if id is not None:
            self._values["id"] = id
        if kms_key_identifier is not None:
            self._values["kms_key_identifier"] = kms_key_identifier
        if log_configuration is not None:
            self._values["log_configuration"] = log_configuration
        if name is not None:
            self._values["name"] = name
        if name_prefix is not None:
            self._values["name_prefix"] = name_prefix
        if source_parameters is not None:
            self._values["source_parameters"] = source_parameters
        if tags is not None:
            self._values["tags"] = tags
        if tags_all is not None:
            self._values["tags_all"] = tags_all
        if target_parameters is not None:
            self._values["target_parameters"] = target_parameters
        if timeouts is not None:
            self._values["timeouts"] = timeouts

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
    def role_arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#role_arn PipesPipe#role_arn}.'''
        result = self._values.get("role_arn")
        assert result is not None, "Required property 'role_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def source(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#source PipesPipe#source}.'''
        result = self._values.get("source")
        assert result is not None, "Required property 'source' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def target(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#target PipesPipe#target}.'''
        result = self._values.get("target")
        assert result is not None, "Required property 'target' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#description PipesPipe#description}.'''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def desired_state(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#desired_state PipesPipe#desired_state}.'''
        result = self._values.get("desired_state")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enrichment(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#enrichment PipesPipe#enrichment}.'''
        result = self._values.get("enrichment")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enrichment_parameters(self) -> typing.Optional["PipesPipeEnrichmentParameters"]:
        '''enrichment_parameters block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#enrichment_parameters PipesPipe#enrichment_parameters}
        '''
        result = self._values.get("enrichment_parameters")
        return typing.cast(typing.Optional["PipesPipeEnrichmentParameters"], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#id PipesPipe#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kms_key_identifier(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#kms_key_identifier PipesPipe#kms_key_identifier}.'''
        result = self._values.get("kms_key_identifier")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def log_configuration(self) -> typing.Optional["PipesPipeLogConfiguration"]:
        '''log_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#log_configuration PipesPipe#log_configuration}
        '''
        result = self._values.get("log_configuration")
        return typing.cast(typing.Optional["PipesPipeLogConfiguration"], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#name PipesPipe#name}.'''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name_prefix(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#name_prefix PipesPipe#name_prefix}.'''
        result = self._values.get("name_prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def source_parameters(self) -> typing.Optional["PipesPipeSourceParameters"]:
        '''source_parameters block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#source_parameters PipesPipe#source_parameters}
        '''
        result = self._values.get("source_parameters")
        return typing.cast(typing.Optional["PipesPipeSourceParameters"], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#tags PipesPipe#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def tags_all(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#tags_all PipesPipe#tags_all}.'''
        result = self._values.get("tags_all")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def target_parameters(self) -> typing.Optional["PipesPipeTargetParameters"]:
        '''target_parameters block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#target_parameters PipesPipe#target_parameters}
        '''
        result = self._values.get("target_parameters")
        return typing.cast(typing.Optional["PipesPipeTargetParameters"], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["PipesPipeTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#timeouts PipesPipe#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["PipesPipeTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PipesPipeConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.pipesPipe.PipesPipeEnrichmentParameters",
    jsii_struct_bases=[],
    name_mapping={
        "http_parameters": "httpParameters",
        "input_template": "inputTemplate",
    },
)
class PipesPipeEnrichmentParameters:
    def __init__(
        self,
        *,
        http_parameters: typing.Optional[typing.Union["PipesPipeEnrichmentParametersHttpParameters", typing.Dict[builtins.str, typing.Any]]] = None,
        input_template: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param http_parameters: http_parameters block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#http_parameters PipesPipe#http_parameters}
        :param input_template: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#input_template PipesPipe#input_template}.
        '''
        if isinstance(http_parameters, dict):
            http_parameters = PipesPipeEnrichmentParametersHttpParameters(**http_parameters)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8fbf320aba8dbd20f7d453a8e0316774cdc90a626eaf2cc77a198299b686652d)
            check_type(argname="argument http_parameters", value=http_parameters, expected_type=type_hints["http_parameters"])
            check_type(argname="argument input_template", value=input_template, expected_type=type_hints["input_template"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if http_parameters is not None:
            self._values["http_parameters"] = http_parameters
        if input_template is not None:
            self._values["input_template"] = input_template

    @builtins.property
    def http_parameters(
        self,
    ) -> typing.Optional["PipesPipeEnrichmentParametersHttpParameters"]:
        '''http_parameters block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#http_parameters PipesPipe#http_parameters}
        '''
        result = self._values.get("http_parameters")
        return typing.cast(typing.Optional["PipesPipeEnrichmentParametersHttpParameters"], result)

    @builtins.property
    def input_template(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#input_template PipesPipe#input_template}.'''
        result = self._values.get("input_template")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PipesPipeEnrichmentParameters(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.pipesPipe.PipesPipeEnrichmentParametersHttpParameters",
    jsii_struct_bases=[],
    name_mapping={
        "header_parameters": "headerParameters",
        "path_parameter_values": "pathParameterValues",
        "query_string_parameters": "queryStringParameters",
    },
)
class PipesPipeEnrichmentParametersHttpParameters:
    def __init__(
        self,
        *,
        header_parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        path_parameter_values: typing.Optional[typing.Sequence[builtins.str]] = None,
        query_string_parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param header_parameters: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#header_parameters PipesPipe#header_parameters}.
        :param path_parameter_values: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#path_parameter_values PipesPipe#path_parameter_values}.
        :param query_string_parameters: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#query_string_parameters PipesPipe#query_string_parameters}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cbd132970f51dbc99f97a1a186ef62af2f3b7e9ce4d3bd4ce21c7351bf07057a)
            check_type(argname="argument header_parameters", value=header_parameters, expected_type=type_hints["header_parameters"])
            check_type(argname="argument path_parameter_values", value=path_parameter_values, expected_type=type_hints["path_parameter_values"])
            check_type(argname="argument query_string_parameters", value=query_string_parameters, expected_type=type_hints["query_string_parameters"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if header_parameters is not None:
            self._values["header_parameters"] = header_parameters
        if path_parameter_values is not None:
            self._values["path_parameter_values"] = path_parameter_values
        if query_string_parameters is not None:
            self._values["query_string_parameters"] = query_string_parameters

    @builtins.property
    def header_parameters(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#header_parameters PipesPipe#header_parameters}.'''
        result = self._values.get("header_parameters")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def path_parameter_values(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#path_parameter_values PipesPipe#path_parameter_values}.'''
        result = self._values.get("path_parameter_values")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def query_string_parameters(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#query_string_parameters PipesPipe#query_string_parameters}.'''
        result = self._values.get("query_string_parameters")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PipesPipeEnrichmentParametersHttpParameters(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PipesPipeEnrichmentParametersHttpParametersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.pipesPipe.PipesPipeEnrichmentParametersHttpParametersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7bba9d3c0bee6776cac32928c6874899d1319f63eaec2afc2d73b346502cbd34)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetHeaderParameters")
    def reset_header_parameters(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHeaderParameters", []))

    @jsii.member(jsii_name="resetPathParameterValues")
    def reset_path_parameter_values(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPathParameterValues", []))

    @jsii.member(jsii_name="resetQueryStringParameters")
    def reset_query_string_parameters(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetQueryStringParameters", []))

    @builtins.property
    @jsii.member(jsii_name="headerParametersInput")
    def header_parameters_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "headerParametersInput"))

    @builtins.property
    @jsii.member(jsii_name="pathParameterValuesInput")
    def path_parameter_values_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "pathParameterValuesInput"))

    @builtins.property
    @jsii.member(jsii_name="queryStringParametersInput")
    def query_string_parameters_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "queryStringParametersInput"))

    @builtins.property
    @jsii.member(jsii_name="headerParameters")
    def header_parameters(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "headerParameters"))

    @header_parameters.setter
    def header_parameters(
        self,
        value: typing.Mapping[builtins.str, builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__13177408a155d88521379f8cc1ed2a805a63a98338d6072ffbe0cee735f0af3a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "headerParameters", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="pathParameterValues")
    def path_parameter_values(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "pathParameterValues"))

    @path_parameter_values.setter
    def path_parameter_values(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e5ea9d1677d8eaeff18565394f374b4e6e1daf3570fffc9e42dd43926308a4a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pathParameterValues", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="queryStringParameters")
    def query_string_parameters(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "queryStringParameters"))

    @query_string_parameters.setter
    def query_string_parameters(
        self,
        value: typing.Mapping[builtins.str, builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa632411a740ce5d11a8022dfdc1842f067b3048d9daa5a28a0bbc125e1e7b34)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "queryStringParameters", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[PipesPipeEnrichmentParametersHttpParameters]:
        return typing.cast(typing.Optional[PipesPipeEnrichmentParametersHttpParameters], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[PipesPipeEnrichmentParametersHttpParameters],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fab9274754fc0802e84c1ccd55f127929c31b1467f27ac847085ac313ef49508)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class PipesPipeEnrichmentParametersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.pipesPipe.PipesPipeEnrichmentParametersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b40ba6703b2bdaef2d913896bc209b51e822c7901e2310db3c3294961c5a3ad5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putHttpParameters")
    def put_http_parameters(
        self,
        *,
        header_parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        path_parameter_values: typing.Optional[typing.Sequence[builtins.str]] = None,
        query_string_parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param header_parameters: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#header_parameters PipesPipe#header_parameters}.
        :param path_parameter_values: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#path_parameter_values PipesPipe#path_parameter_values}.
        :param query_string_parameters: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#query_string_parameters PipesPipe#query_string_parameters}.
        '''
        value = PipesPipeEnrichmentParametersHttpParameters(
            header_parameters=header_parameters,
            path_parameter_values=path_parameter_values,
            query_string_parameters=query_string_parameters,
        )

        return typing.cast(None, jsii.invoke(self, "putHttpParameters", [value]))

    @jsii.member(jsii_name="resetHttpParameters")
    def reset_http_parameters(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHttpParameters", []))

    @jsii.member(jsii_name="resetInputTemplate")
    def reset_input_template(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInputTemplate", []))

    @builtins.property
    @jsii.member(jsii_name="httpParameters")
    def http_parameters(
        self,
    ) -> PipesPipeEnrichmentParametersHttpParametersOutputReference:
        return typing.cast(PipesPipeEnrichmentParametersHttpParametersOutputReference, jsii.get(self, "httpParameters"))

    @builtins.property
    @jsii.member(jsii_name="httpParametersInput")
    def http_parameters_input(
        self,
    ) -> typing.Optional[PipesPipeEnrichmentParametersHttpParameters]:
        return typing.cast(typing.Optional[PipesPipeEnrichmentParametersHttpParameters], jsii.get(self, "httpParametersInput"))

    @builtins.property
    @jsii.member(jsii_name="inputTemplateInput")
    def input_template_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "inputTemplateInput"))

    @builtins.property
    @jsii.member(jsii_name="inputTemplate")
    def input_template(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "inputTemplate"))

    @input_template.setter
    def input_template(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c7ef9a6939594dcba8b4a6ac55ea6495f8d11325f8e4d8ed3e66de29c24964fa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "inputTemplate", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[PipesPipeEnrichmentParameters]:
        return typing.cast(typing.Optional[PipesPipeEnrichmentParameters], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[PipesPipeEnrichmentParameters],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__07479edcf7ebf79a59118f74d3bb573614e5e5da48f79f17c0171d5b74baf38e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.pipesPipe.PipesPipeLogConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "level": "level",
        "cloudwatch_logs_log_destination": "cloudwatchLogsLogDestination",
        "firehose_log_destination": "firehoseLogDestination",
        "include_execution_data": "includeExecutionData",
        "s3_log_destination": "s3LogDestination",
    },
)
class PipesPipeLogConfiguration:
    def __init__(
        self,
        *,
        level: builtins.str,
        cloudwatch_logs_log_destination: typing.Optional[typing.Union["PipesPipeLogConfigurationCloudwatchLogsLogDestination", typing.Dict[builtins.str, typing.Any]]] = None,
        firehose_log_destination: typing.Optional[typing.Union["PipesPipeLogConfigurationFirehoseLogDestination", typing.Dict[builtins.str, typing.Any]]] = None,
        include_execution_data: typing.Optional[typing.Sequence[builtins.str]] = None,
        s3_log_destination: typing.Optional[typing.Union["PipesPipeLogConfigurationS3LogDestination", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param level: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#level PipesPipe#level}.
        :param cloudwatch_logs_log_destination: cloudwatch_logs_log_destination block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#cloudwatch_logs_log_destination PipesPipe#cloudwatch_logs_log_destination}
        :param firehose_log_destination: firehose_log_destination block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#firehose_log_destination PipesPipe#firehose_log_destination}
        :param include_execution_data: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#include_execution_data PipesPipe#include_execution_data}.
        :param s3_log_destination: s3_log_destination block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#s3_log_destination PipesPipe#s3_log_destination}
        '''
        if isinstance(cloudwatch_logs_log_destination, dict):
            cloudwatch_logs_log_destination = PipesPipeLogConfigurationCloudwatchLogsLogDestination(**cloudwatch_logs_log_destination)
        if isinstance(firehose_log_destination, dict):
            firehose_log_destination = PipesPipeLogConfigurationFirehoseLogDestination(**firehose_log_destination)
        if isinstance(s3_log_destination, dict):
            s3_log_destination = PipesPipeLogConfigurationS3LogDestination(**s3_log_destination)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b02801f26948a8e88afc155de5519f99edd9b6f6faa28c861c09bd5e043071c9)
            check_type(argname="argument level", value=level, expected_type=type_hints["level"])
            check_type(argname="argument cloudwatch_logs_log_destination", value=cloudwatch_logs_log_destination, expected_type=type_hints["cloudwatch_logs_log_destination"])
            check_type(argname="argument firehose_log_destination", value=firehose_log_destination, expected_type=type_hints["firehose_log_destination"])
            check_type(argname="argument include_execution_data", value=include_execution_data, expected_type=type_hints["include_execution_data"])
            check_type(argname="argument s3_log_destination", value=s3_log_destination, expected_type=type_hints["s3_log_destination"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "level": level,
        }
        if cloudwatch_logs_log_destination is not None:
            self._values["cloudwatch_logs_log_destination"] = cloudwatch_logs_log_destination
        if firehose_log_destination is not None:
            self._values["firehose_log_destination"] = firehose_log_destination
        if include_execution_data is not None:
            self._values["include_execution_data"] = include_execution_data
        if s3_log_destination is not None:
            self._values["s3_log_destination"] = s3_log_destination

    @builtins.property
    def level(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#level PipesPipe#level}.'''
        result = self._values.get("level")
        assert result is not None, "Required property 'level' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def cloudwatch_logs_log_destination(
        self,
    ) -> typing.Optional["PipesPipeLogConfigurationCloudwatchLogsLogDestination"]:
        '''cloudwatch_logs_log_destination block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#cloudwatch_logs_log_destination PipesPipe#cloudwatch_logs_log_destination}
        '''
        result = self._values.get("cloudwatch_logs_log_destination")
        return typing.cast(typing.Optional["PipesPipeLogConfigurationCloudwatchLogsLogDestination"], result)

    @builtins.property
    def firehose_log_destination(
        self,
    ) -> typing.Optional["PipesPipeLogConfigurationFirehoseLogDestination"]:
        '''firehose_log_destination block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#firehose_log_destination PipesPipe#firehose_log_destination}
        '''
        result = self._values.get("firehose_log_destination")
        return typing.cast(typing.Optional["PipesPipeLogConfigurationFirehoseLogDestination"], result)

    @builtins.property
    def include_execution_data(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#include_execution_data PipesPipe#include_execution_data}.'''
        result = self._values.get("include_execution_data")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def s3_log_destination(
        self,
    ) -> typing.Optional["PipesPipeLogConfigurationS3LogDestination"]:
        '''s3_log_destination block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#s3_log_destination PipesPipe#s3_log_destination}
        '''
        result = self._values.get("s3_log_destination")
        return typing.cast(typing.Optional["PipesPipeLogConfigurationS3LogDestination"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PipesPipeLogConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.pipesPipe.PipesPipeLogConfigurationCloudwatchLogsLogDestination",
    jsii_struct_bases=[],
    name_mapping={"log_group_arn": "logGroupArn"},
)
class PipesPipeLogConfigurationCloudwatchLogsLogDestination:
    def __init__(self, *, log_group_arn: builtins.str) -> None:
        '''
        :param log_group_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#log_group_arn PipesPipe#log_group_arn}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5bf15e2b3b745fd1d37e6d09cb6c5d2ed192aad6656913d4090ffb284be056c9)
            check_type(argname="argument log_group_arn", value=log_group_arn, expected_type=type_hints["log_group_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "log_group_arn": log_group_arn,
        }

    @builtins.property
    def log_group_arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#log_group_arn PipesPipe#log_group_arn}.'''
        result = self._values.get("log_group_arn")
        assert result is not None, "Required property 'log_group_arn' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PipesPipeLogConfigurationCloudwatchLogsLogDestination(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PipesPipeLogConfigurationCloudwatchLogsLogDestinationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.pipesPipe.PipesPipeLogConfigurationCloudwatchLogsLogDestinationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4ba9acb450e5982386fb59516534cc694745c175e6d20d59021dff19f6c2d0b2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="logGroupArnInput")
    def log_group_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "logGroupArnInput"))

    @builtins.property
    @jsii.member(jsii_name="logGroupArn")
    def log_group_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "logGroupArn"))

    @log_group_arn.setter
    def log_group_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a464caf9117350afb45674c00a334e45d7cc1a5ac5558d77a5a9449036e31b6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "logGroupArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[PipesPipeLogConfigurationCloudwatchLogsLogDestination]:
        return typing.cast(typing.Optional[PipesPipeLogConfigurationCloudwatchLogsLogDestination], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[PipesPipeLogConfigurationCloudwatchLogsLogDestination],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bfb32aba766d43bc708f289507238262fbada67dcb7929df20d6ab1c97762b59)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.pipesPipe.PipesPipeLogConfigurationFirehoseLogDestination",
    jsii_struct_bases=[],
    name_mapping={"delivery_stream_arn": "deliveryStreamArn"},
)
class PipesPipeLogConfigurationFirehoseLogDestination:
    def __init__(self, *, delivery_stream_arn: builtins.str) -> None:
        '''
        :param delivery_stream_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#delivery_stream_arn PipesPipe#delivery_stream_arn}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a55dde54c23adc340c83767fd77cd6b674315bc531b89f16d0fd6538b4277377)
            check_type(argname="argument delivery_stream_arn", value=delivery_stream_arn, expected_type=type_hints["delivery_stream_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "delivery_stream_arn": delivery_stream_arn,
        }

    @builtins.property
    def delivery_stream_arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#delivery_stream_arn PipesPipe#delivery_stream_arn}.'''
        result = self._values.get("delivery_stream_arn")
        assert result is not None, "Required property 'delivery_stream_arn' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PipesPipeLogConfigurationFirehoseLogDestination(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PipesPipeLogConfigurationFirehoseLogDestinationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.pipesPipe.PipesPipeLogConfigurationFirehoseLogDestinationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b98dc63d9408ac10279db5c80e5f9e70231c7f32ba532bcfc09283ce53617020)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="deliveryStreamArnInput")
    def delivery_stream_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "deliveryStreamArnInput"))

    @builtins.property
    @jsii.member(jsii_name="deliveryStreamArn")
    def delivery_stream_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "deliveryStreamArn"))

    @delivery_stream_arn.setter
    def delivery_stream_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d4b0a933a65b4a7d6bef4f2d1c7aece6f5361ab872603da229097f42cfcb56f8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deliveryStreamArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[PipesPipeLogConfigurationFirehoseLogDestination]:
        return typing.cast(typing.Optional[PipesPipeLogConfigurationFirehoseLogDestination], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[PipesPipeLogConfigurationFirehoseLogDestination],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__67efbb6ac631919da8390e119e9d7ff6094978d278ecb89ebdbd6d0a7c4c9ab2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class PipesPipeLogConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.pipesPipe.PipesPipeLogConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0cbdbc9be271dc01da850640d30d1590b6c7db707fdaaa852cee168c39f72598)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putCloudwatchLogsLogDestination")
    def put_cloudwatch_logs_log_destination(
        self,
        *,
        log_group_arn: builtins.str,
    ) -> None:
        '''
        :param log_group_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#log_group_arn PipesPipe#log_group_arn}.
        '''
        value = PipesPipeLogConfigurationCloudwatchLogsLogDestination(
            log_group_arn=log_group_arn
        )

        return typing.cast(None, jsii.invoke(self, "putCloudwatchLogsLogDestination", [value]))

    @jsii.member(jsii_name="putFirehoseLogDestination")
    def put_firehose_log_destination(
        self,
        *,
        delivery_stream_arn: builtins.str,
    ) -> None:
        '''
        :param delivery_stream_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#delivery_stream_arn PipesPipe#delivery_stream_arn}.
        '''
        value = PipesPipeLogConfigurationFirehoseLogDestination(
            delivery_stream_arn=delivery_stream_arn
        )

        return typing.cast(None, jsii.invoke(self, "putFirehoseLogDestination", [value]))

    @jsii.member(jsii_name="putS3LogDestination")
    def put_s3_log_destination(
        self,
        *,
        bucket_name: builtins.str,
        bucket_owner: builtins.str,
        output_format: typing.Optional[builtins.str] = None,
        prefix: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param bucket_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#bucket_name PipesPipe#bucket_name}.
        :param bucket_owner: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#bucket_owner PipesPipe#bucket_owner}.
        :param output_format: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#output_format PipesPipe#output_format}.
        :param prefix: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#prefix PipesPipe#prefix}.
        '''
        value = PipesPipeLogConfigurationS3LogDestination(
            bucket_name=bucket_name,
            bucket_owner=bucket_owner,
            output_format=output_format,
            prefix=prefix,
        )

        return typing.cast(None, jsii.invoke(self, "putS3LogDestination", [value]))

    @jsii.member(jsii_name="resetCloudwatchLogsLogDestination")
    def reset_cloudwatch_logs_log_destination(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCloudwatchLogsLogDestination", []))

    @jsii.member(jsii_name="resetFirehoseLogDestination")
    def reset_firehose_log_destination(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFirehoseLogDestination", []))

    @jsii.member(jsii_name="resetIncludeExecutionData")
    def reset_include_execution_data(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIncludeExecutionData", []))

    @jsii.member(jsii_name="resetS3LogDestination")
    def reset_s3_log_destination(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetS3LogDestination", []))

    @builtins.property
    @jsii.member(jsii_name="cloudwatchLogsLogDestination")
    def cloudwatch_logs_log_destination(
        self,
    ) -> PipesPipeLogConfigurationCloudwatchLogsLogDestinationOutputReference:
        return typing.cast(PipesPipeLogConfigurationCloudwatchLogsLogDestinationOutputReference, jsii.get(self, "cloudwatchLogsLogDestination"))

    @builtins.property
    @jsii.member(jsii_name="firehoseLogDestination")
    def firehose_log_destination(
        self,
    ) -> PipesPipeLogConfigurationFirehoseLogDestinationOutputReference:
        return typing.cast(PipesPipeLogConfigurationFirehoseLogDestinationOutputReference, jsii.get(self, "firehoseLogDestination"))

    @builtins.property
    @jsii.member(jsii_name="s3LogDestination")
    def s3_log_destination(
        self,
    ) -> "PipesPipeLogConfigurationS3LogDestinationOutputReference":
        return typing.cast("PipesPipeLogConfigurationS3LogDestinationOutputReference", jsii.get(self, "s3LogDestination"))

    @builtins.property
    @jsii.member(jsii_name="cloudwatchLogsLogDestinationInput")
    def cloudwatch_logs_log_destination_input(
        self,
    ) -> typing.Optional[PipesPipeLogConfigurationCloudwatchLogsLogDestination]:
        return typing.cast(typing.Optional[PipesPipeLogConfigurationCloudwatchLogsLogDestination], jsii.get(self, "cloudwatchLogsLogDestinationInput"))

    @builtins.property
    @jsii.member(jsii_name="firehoseLogDestinationInput")
    def firehose_log_destination_input(
        self,
    ) -> typing.Optional[PipesPipeLogConfigurationFirehoseLogDestination]:
        return typing.cast(typing.Optional[PipesPipeLogConfigurationFirehoseLogDestination], jsii.get(self, "firehoseLogDestinationInput"))

    @builtins.property
    @jsii.member(jsii_name="includeExecutionDataInput")
    def include_execution_data_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "includeExecutionDataInput"))

    @builtins.property
    @jsii.member(jsii_name="levelInput")
    def level_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "levelInput"))

    @builtins.property
    @jsii.member(jsii_name="s3LogDestinationInput")
    def s3_log_destination_input(
        self,
    ) -> typing.Optional["PipesPipeLogConfigurationS3LogDestination"]:
        return typing.cast(typing.Optional["PipesPipeLogConfigurationS3LogDestination"], jsii.get(self, "s3LogDestinationInput"))

    @builtins.property
    @jsii.member(jsii_name="includeExecutionData")
    def include_execution_data(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "includeExecutionData"))

    @include_execution_data.setter
    def include_execution_data(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__09d55b3e57d1470ff2e5524b37a7e54aee59f3760d4fec3aa2944ffbcd986b0f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "includeExecutionData", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="level")
    def level(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "level"))

    @level.setter
    def level(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ed78a4e78c512b76784175ec88f622909c227fe774c4b02b8e9adc218289b9d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "level", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[PipesPipeLogConfiguration]:
        return typing.cast(typing.Optional[PipesPipeLogConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[PipesPipeLogConfiguration]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8fbd59ce893fa9744eff6b758b9bfb771d3d94d6f8753b6318dcf182e6d8c8f0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.pipesPipe.PipesPipeLogConfigurationS3LogDestination",
    jsii_struct_bases=[],
    name_mapping={
        "bucket_name": "bucketName",
        "bucket_owner": "bucketOwner",
        "output_format": "outputFormat",
        "prefix": "prefix",
    },
)
class PipesPipeLogConfigurationS3LogDestination:
    def __init__(
        self,
        *,
        bucket_name: builtins.str,
        bucket_owner: builtins.str,
        output_format: typing.Optional[builtins.str] = None,
        prefix: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param bucket_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#bucket_name PipesPipe#bucket_name}.
        :param bucket_owner: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#bucket_owner PipesPipe#bucket_owner}.
        :param output_format: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#output_format PipesPipe#output_format}.
        :param prefix: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#prefix PipesPipe#prefix}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__02e4e613e28b1792498e5263a66d3815a4b74daf0b60c03501834bc79ec1d584)
            check_type(argname="argument bucket_name", value=bucket_name, expected_type=type_hints["bucket_name"])
            check_type(argname="argument bucket_owner", value=bucket_owner, expected_type=type_hints["bucket_owner"])
            check_type(argname="argument output_format", value=output_format, expected_type=type_hints["output_format"])
            check_type(argname="argument prefix", value=prefix, expected_type=type_hints["prefix"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "bucket_name": bucket_name,
            "bucket_owner": bucket_owner,
        }
        if output_format is not None:
            self._values["output_format"] = output_format
        if prefix is not None:
            self._values["prefix"] = prefix

    @builtins.property
    def bucket_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#bucket_name PipesPipe#bucket_name}.'''
        result = self._values.get("bucket_name")
        assert result is not None, "Required property 'bucket_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def bucket_owner(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#bucket_owner PipesPipe#bucket_owner}.'''
        result = self._values.get("bucket_owner")
        assert result is not None, "Required property 'bucket_owner' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def output_format(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#output_format PipesPipe#output_format}.'''
        result = self._values.get("output_format")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def prefix(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#prefix PipesPipe#prefix}.'''
        result = self._values.get("prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PipesPipeLogConfigurationS3LogDestination(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PipesPipeLogConfigurationS3LogDestinationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.pipesPipe.PipesPipeLogConfigurationS3LogDestinationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__207d94b55df9ad699f475ea40474f83bc5d1f915df1a5a3ae4ca6bee1e784d7e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetOutputFormat")
    def reset_output_format(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOutputFormat", []))

    @jsii.member(jsii_name="resetPrefix")
    def reset_prefix(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPrefix", []))

    @builtins.property
    @jsii.member(jsii_name="bucketNameInput")
    def bucket_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bucketNameInput"))

    @builtins.property
    @jsii.member(jsii_name="bucketOwnerInput")
    def bucket_owner_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bucketOwnerInput"))

    @builtins.property
    @jsii.member(jsii_name="outputFormatInput")
    def output_format_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "outputFormatInput"))

    @builtins.property
    @jsii.member(jsii_name="prefixInput")
    def prefix_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "prefixInput"))

    @builtins.property
    @jsii.member(jsii_name="bucketName")
    def bucket_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bucketName"))

    @bucket_name.setter
    def bucket_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c59b6147fc51e3919526561631f8f67bf3551b459131eaa9ab80c46b42cf259d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bucketName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="bucketOwner")
    def bucket_owner(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bucketOwner"))

    @bucket_owner.setter
    def bucket_owner(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5960a44441a8d00d88af75376236a868d5e3f0470effbae14771fac1c840810d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bucketOwner", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="outputFormat")
    def output_format(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "outputFormat"))

    @output_format.setter
    def output_format(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b4a8912e5890fb6cf4e6e3691f310bba90bd6babab80320279fd72eb5ad2a6e9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "outputFormat", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="prefix")
    def prefix(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "prefix"))

    @prefix.setter
    def prefix(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__402013d3465e640d01228e02a9f058bd186faeeb9873929e74a7fabb02c0ef77)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "prefix", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[PipesPipeLogConfigurationS3LogDestination]:
        return typing.cast(typing.Optional[PipesPipeLogConfigurationS3LogDestination], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[PipesPipeLogConfigurationS3LogDestination],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8f32eee03b5abb06894f9fe9ed66890e0505182ec23f9359743f07f897d67b59)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.pipesPipe.PipesPipeSourceParameters",
    jsii_struct_bases=[],
    name_mapping={
        "activemq_broker_parameters": "activemqBrokerParameters",
        "dynamodb_stream_parameters": "dynamodbStreamParameters",
        "filter_criteria": "filterCriteria",
        "kinesis_stream_parameters": "kinesisStreamParameters",
        "managed_streaming_kafka_parameters": "managedStreamingKafkaParameters",
        "rabbitmq_broker_parameters": "rabbitmqBrokerParameters",
        "self_managed_kafka_parameters": "selfManagedKafkaParameters",
        "sqs_queue_parameters": "sqsQueueParameters",
    },
)
class PipesPipeSourceParameters:
    def __init__(
        self,
        *,
        activemq_broker_parameters: typing.Optional[typing.Union["PipesPipeSourceParametersActivemqBrokerParameters", typing.Dict[builtins.str, typing.Any]]] = None,
        dynamodb_stream_parameters: typing.Optional[typing.Union["PipesPipeSourceParametersDynamodbStreamParameters", typing.Dict[builtins.str, typing.Any]]] = None,
        filter_criteria: typing.Optional[typing.Union["PipesPipeSourceParametersFilterCriteria", typing.Dict[builtins.str, typing.Any]]] = None,
        kinesis_stream_parameters: typing.Optional[typing.Union["PipesPipeSourceParametersKinesisStreamParameters", typing.Dict[builtins.str, typing.Any]]] = None,
        managed_streaming_kafka_parameters: typing.Optional[typing.Union["PipesPipeSourceParametersManagedStreamingKafkaParameters", typing.Dict[builtins.str, typing.Any]]] = None,
        rabbitmq_broker_parameters: typing.Optional[typing.Union["PipesPipeSourceParametersRabbitmqBrokerParameters", typing.Dict[builtins.str, typing.Any]]] = None,
        self_managed_kafka_parameters: typing.Optional[typing.Union["PipesPipeSourceParametersSelfManagedKafkaParameters", typing.Dict[builtins.str, typing.Any]]] = None,
        sqs_queue_parameters: typing.Optional[typing.Union["PipesPipeSourceParametersSqsQueueParameters", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param activemq_broker_parameters: activemq_broker_parameters block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#activemq_broker_parameters PipesPipe#activemq_broker_parameters}
        :param dynamodb_stream_parameters: dynamodb_stream_parameters block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#dynamodb_stream_parameters PipesPipe#dynamodb_stream_parameters}
        :param filter_criteria: filter_criteria block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#filter_criteria PipesPipe#filter_criteria}
        :param kinesis_stream_parameters: kinesis_stream_parameters block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#kinesis_stream_parameters PipesPipe#kinesis_stream_parameters}
        :param managed_streaming_kafka_parameters: managed_streaming_kafka_parameters block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#managed_streaming_kafka_parameters PipesPipe#managed_streaming_kafka_parameters}
        :param rabbitmq_broker_parameters: rabbitmq_broker_parameters block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#rabbitmq_broker_parameters PipesPipe#rabbitmq_broker_parameters}
        :param self_managed_kafka_parameters: self_managed_kafka_parameters block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#self_managed_kafka_parameters PipesPipe#self_managed_kafka_parameters}
        :param sqs_queue_parameters: sqs_queue_parameters block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#sqs_queue_parameters PipesPipe#sqs_queue_parameters}
        '''
        if isinstance(activemq_broker_parameters, dict):
            activemq_broker_parameters = PipesPipeSourceParametersActivemqBrokerParameters(**activemq_broker_parameters)
        if isinstance(dynamodb_stream_parameters, dict):
            dynamodb_stream_parameters = PipesPipeSourceParametersDynamodbStreamParameters(**dynamodb_stream_parameters)
        if isinstance(filter_criteria, dict):
            filter_criteria = PipesPipeSourceParametersFilterCriteria(**filter_criteria)
        if isinstance(kinesis_stream_parameters, dict):
            kinesis_stream_parameters = PipesPipeSourceParametersKinesisStreamParameters(**kinesis_stream_parameters)
        if isinstance(managed_streaming_kafka_parameters, dict):
            managed_streaming_kafka_parameters = PipesPipeSourceParametersManagedStreamingKafkaParameters(**managed_streaming_kafka_parameters)
        if isinstance(rabbitmq_broker_parameters, dict):
            rabbitmq_broker_parameters = PipesPipeSourceParametersRabbitmqBrokerParameters(**rabbitmq_broker_parameters)
        if isinstance(self_managed_kafka_parameters, dict):
            self_managed_kafka_parameters = PipesPipeSourceParametersSelfManagedKafkaParameters(**self_managed_kafka_parameters)
        if isinstance(sqs_queue_parameters, dict):
            sqs_queue_parameters = PipesPipeSourceParametersSqsQueueParameters(**sqs_queue_parameters)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dcbc8316d12899e17f1c47829613f8657e3783b3ba9236dc91eae00478b1cb8a)
            check_type(argname="argument activemq_broker_parameters", value=activemq_broker_parameters, expected_type=type_hints["activemq_broker_parameters"])
            check_type(argname="argument dynamodb_stream_parameters", value=dynamodb_stream_parameters, expected_type=type_hints["dynamodb_stream_parameters"])
            check_type(argname="argument filter_criteria", value=filter_criteria, expected_type=type_hints["filter_criteria"])
            check_type(argname="argument kinesis_stream_parameters", value=kinesis_stream_parameters, expected_type=type_hints["kinesis_stream_parameters"])
            check_type(argname="argument managed_streaming_kafka_parameters", value=managed_streaming_kafka_parameters, expected_type=type_hints["managed_streaming_kafka_parameters"])
            check_type(argname="argument rabbitmq_broker_parameters", value=rabbitmq_broker_parameters, expected_type=type_hints["rabbitmq_broker_parameters"])
            check_type(argname="argument self_managed_kafka_parameters", value=self_managed_kafka_parameters, expected_type=type_hints["self_managed_kafka_parameters"])
            check_type(argname="argument sqs_queue_parameters", value=sqs_queue_parameters, expected_type=type_hints["sqs_queue_parameters"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if activemq_broker_parameters is not None:
            self._values["activemq_broker_parameters"] = activemq_broker_parameters
        if dynamodb_stream_parameters is not None:
            self._values["dynamodb_stream_parameters"] = dynamodb_stream_parameters
        if filter_criteria is not None:
            self._values["filter_criteria"] = filter_criteria
        if kinesis_stream_parameters is not None:
            self._values["kinesis_stream_parameters"] = kinesis_stream_parameters
        if managed_streaming_kafka_parameters is not None:
            self._values["managed_streaming_kafka_parameters"] = managed_streaming_kafka_parameters
        if rabbitmq_broker_parameters is not None:
            self._values["rabbitmq_broker_parameters"] = rabbitmq_broker_parameters
        if self_managed_kafka_parameters is not None:
            self._values["self_managed_kafka_parameters"] = self_managed_kafka_parameters
        if sqs_queue_parameters is not None:
            self._values["sqs_queue_parameters"] = sqs_queue_parameters

    @builtins.property
    def activemq_broker_parameters(
        self,
    ) -> typing.Optional["PipesPipeSourceParametersActivemqBrokerParameters"]:
        '''activemq_broker_parameters block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#activemq_broker_parameters PipesPipe#activemq_broker_parameters}
        '''
        result = self._values.get("activemq_broker_parameters")
        return typing.cast(typing.Optional["PipesPipeSourceParametersActivemqBrokerParameters"], result)

    @builtins.property
    def dynamodb_stream_parameters(
        self,
    ) -> typing.Optional["PipesPipeSourceParametersDynamodbStreamParameters"]:
        '''dynamodb_stream_parameters block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#dynamodb_stream_parameters PipesPipe#dynamodb_stream_parameters}
        '''
        result = self._values.get("dynamodb_stream_parameters")
        return typing.cast(typing.Optional["PipesPipeSourceParametersDynamodbStreamParameters"], result)

    @builtins.property
    def filter_criteria(
        self,
    ) -> typing.Optional["PipesPipeSourceParametersFilterCriteria"]:
        '''filter_criteria block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#filter_criteria PipesPipe#filter_criteria}
        '''
        result = self._values.get("filter_criteria")
        return typing.cast(typing.Optional["PipesPipeSourceParametersFilterCriteria"], result)

    @builtins.property
    def kinesis_stream_parameters(
        self,
    ) -> typing.Optional["PipesPipeSourceParametersKinesisStreamParameters"]:
        '''kinesis_stream_parameters block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#kinesis_stream_parameters PipesPipe#kinesis_stream_parameters}
        '''
        result = self._values.get("kinesis_stream_parameters")
        return typing.cast(typing.Optional["PipesPipeSourceParametersKinesisStreamParameters"], result)

    @builtins.property
    def managed_streaming_kafka_parameters(
        self,
    ) -> typing.Optional["PipesPipeSourceParametersManagedStreamingKafkaParameters"]:
        '''managed_streaming_kafka_parameters block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#managed_streaming_kafka_parameters PipesPipe#managed_streaming_kafka_parameters}
        '''
        result = self._values.get("managed_streaming_kafka_parameters")
        return typing.cast(typing.Optional["PipesPipeSourceParametersManagedStreamingKafkaParameters"], result)

    @builtins.property
    def rabbitmq_broker_parameters(
        self,
    ) -> typing.Optional["PipesPipeSourceParametersRabbitmqBrokerParameters"]:
        '''rabbitmq_broker_parameters block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#rabbitmq_broker_parameters PipesPipe#rabbitmq_broker_parameters}
        '''
        result = self._values.get("rabbitmq_broker_parameters")
        return typing.cast(typing.Optional["PipesPipeSourceParametersRabbitmqBrokerParameters"], result)

    @builtins.property
    def self_managed_kafka_parameters(
        self,
    ) -> typing.Optional["PipesPipeSourceParametersSelfManagedKafkaParameters"]:
        '''self_managed_kafka_parameters block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#self_managed_kafka_parameters PipesPipe#self_managed_kafka_parameters}
        '''
        result = self._values.get("self_managed_kafka_parameters")
        return typing.cast(typing.Optional["PipesPipeSourceParametersSelfManagedKafkaParameters"], result)

    @builtins.property
    def sqs_queue_parameters(
        self,
    ) -> typing.Optional["PipesPipeSourceParametersSqsQueueParameters"]:
        '''sqs_queue_parameters block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#sqs_queue_parameters PipesPipe#sqs_queue_parameters}
        '''
        result = self._values.get("sqs_queue_parameters")
        return typing.cast(typing.Optional["PipesPipeSourceParametersSqsQueueParameters"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PipesPipeSourceParameters(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.pipesPipe.PipesPipeSourceParametersActivemqBrokerParameters",
    jsii_struct_bases=[],
    name_mapping={
        "credentials": "credentials",
        "queue_name": "queueName",
        "batch_size": "batchSize",
        "maximum_batching_window_in_seconds": "maximumBatchingWindowInSeconds",
    },
)
class PipesPipeSourceParametersActivemqBrokerParameters:
    def __init__(
        self,
        *,
        credentials: typing.Union["PipesPipeSourceParametersActivemqBrokerParametersCredentials", typing.Dict[builtins.str, typing.Any]],
        queue_name: builtins.str,
        batch_size: typing.Optional[jsii.Number] = None,
        maximum_batching_window_in_seconds: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param credentials: credentials block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#credentials PipesPipe#credentials}
        :param queue_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#queue_name PipesPipe#queue_name}.
        :param batch_size: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#batch_size PipesPipe#batch_size}.
        :param maximum_batching_window_in_seconds: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#maximum_batching_window_in_seconds PipesPipe#maximum_batching_window_in_seconds}.
        '''
        if isinstance(credentials, dict):
            credentials = PipesPipeSourceParametersActivemqBrokerParametersCredentials(**credentials)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fe48769a069aa1248ef18604e7b3af6004ef90d6f124e0ce3f4e4061ddef8265)
            check_type(argname="argument credentials", value=credentials, expected_type=type_hints["credentials"])
            check_type(argname="argument queue_name", value=queue_name, expected_type=type_hints["queue_name"])
            check_type(argname="argument batch_size", value=batch_size, expected_type=type_hints["batch_size"])
            check_type(argname="argument maximum_batching_window_in_seconds", value=maximum_batching_window_in_seconds, expected_type=type_hints["maximum_batching_window_in_seconds"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "credentials": credentials,
            "queue_name": queue_name,
        }
        if batch_size is not None:
            self._values["batch_size"] = batch_size
        if maximum_batching_window_in_seconds is not None:
            self._values["maximum_batching_window_in_seconds"] = maximum_batching_window_in_seconds

    @builtins.property
    def credentials(
        self,
    ) -> "PipesPipeSourceParametersActivemqBrokerParametersCredentials":
        '''credentials block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#credentials PipesPipe#credentials}
        '''
        result = self._values.get("credentials")
        assert result is not None, "Required property 'credentials' is missing"
        return typing.cast("PipesPipeSourceParametersActivemqBrokerParametersCredentials", result)

    @builtins.property
    def queue_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#queue_name PipesPipe#queue_name}.'''
        result = self._values.get("queue_name")
        assert result is not None, "Required property 'queue_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def batch_size(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#batch_size PipesPipe#batch_size}.'''
        result = self._values.get("batch_size")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def maximum_batching_window_in_seconds(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#maximum_batching_window_in_seconds PipesPipe#maximum_batching_window_in_seconds}.'''
        result = self._values.get("maximum_batching_window_in_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PipesPipeSourceParametersActivemqBrokerParameters(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.pipesPipe.PipesPipeSourceParametersActivemqBrokerParametersCredentials",
    jsii_struct_bases=[],
    name_mapping={"basic_auth": "basicAuth"},
)
class PipesPipeSourceParametersActivemqBrokerParametersCredentials:
    def __init__(self, *, basic_auth: builtins.str) -> None:
        '''
        :param basic_auth: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#basic_auth PipesPipe#basic_auth}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a007bfd2dcddfa6d7bc0ddb94d871c0c97723f5d6386c55d4f331c534b7fc93)
            check_type(argname="argument basic_auth", value=basic_auth, expected_type=type_hints["basic_auth"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "basic_auth": basic_auth,
        }

    @builtins.property
    def basic_auth(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#basic_auth PipesPipe#basic_auth}.'''
        result = self._values.get("basic_auth")
        assert result is not None, "Required property 'basic_auth' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PipesPipeSourceParametersActivemqBrokerParametersCredentials(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PipesPipeSourceParametersActivemqBrokerParametersCredentialsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.pipesPipe.PipesPipeSourceParametersActivemqBrokerParametersCredentialsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d1dcf3b473cad9f6f4bd85bd550d3706f2fa273104b5050bf3688f32c8e93761)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="basicAuthInput")
    def basic_auth_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "basicAuthInput"))

    @builtins.property
    @jsii.member(jsii_name="basicAuth")
    def basic_auth(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "basicAuth"))

    @basic_auth.setter
    def basic_auth(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b2aa0a99508326a4b42b2504995438c04b291f5cbe03441c2ed9aa5c50f5e19a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "basicAuth", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[PipesPipeSourceParametersActivemqBrokerParametersCredentials]:
        return typing.cast(typing.Optional[PipesPipeSourceParametersActivemqBrokerParametersCredentials], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[PipesPipeSourceParametersActivemqBrokerParametersCredentials],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c976fb055fa7d6f514711c794f44c6dc16934142ffca3229eacb72c577e92c1f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class PipesPipeSourceParametersActivemqBrokerParametersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.pipesPipe.PipesPipeSourceParametersActivemqBrokerParametersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7df86d4ff0b0261d5c47ecceeb5d1a78ea563bb481c7c7604a1edfe76fc8181f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putCredentials")
    def put_credentials(self, *, basic_auth: builtins.str) -> None:
        '''
        :param basic_auth: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#basic_auth PipesPipe#basic_auth}.
        '''
        value = PipesPipeSourceParametersActivemqBrokerParametersCredentials(
            basic_auth=basic_auth
        )

        return typing.cast(None, jsii.invoke(self, "putCredentials", [value]))

    @jsii.member(jsii_name="resetBatchSize")
    def reset_batch_size(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBatchSize", []))

    @jsii.member(jsii_name="resetMaximumBatchingWindowInSeconds")
    def reset_maximum_batching_window_in_seconds(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaximumBatchingWindowInSeconds", []))

    @builtins.property
    @jsii.member(jsii_name="credentials")
    def credentials(
        self,
    ) -> PipesPipeSourceParametersActivemqBrokerParametersCredentialsOutputReference:
        return typing.cast(PipesPipeSourceParametersActivemqBrokerParametersCredentialsOutputReference, jsii.get(self, "credentials"))

    @builtins.property
    @jsii.member(jsii_name="batchSizeInput")
    def batch_size_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "batchSizeInput"))

    @builtins.property
    @jsii.member(jsii_name="credentialsInput")
    def credentials_input(
        self,
    ) -> typing.Optional[PipesPipeSourceParametersActivemqBrokerParametersCredentials]:
        return typing.cast(typing.Optional[PipesPipeSourceParametersActivemqBrokerParametersCredentials], jsii.get(self, "credentialsInput"))

    @builtins.property
    @jsii.member(jsii_name="maximumBatchingWindowInSecondsInput")
    def maximum_batching_window_in_seconds_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maximumBatchingWindowInSecondsInput"))

    @builtins.property
    @jsii.member(jsii_name="queueNameInput")
    def queue_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "queueNameInput"))

    @builtins.property
    @jsii.member(jsii_name="batchSize")
    def batch_size(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "batchSize"))

    @batch_size.setter
    def batch_size(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c471ae028f15b15b84633ea4340748f443882699a25b200f1db8a525ad51d9e4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "batchSize", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maximumBatchingWindowInSeconds")
    def maximum_batching_window_in_seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maximumBatchingWindowInSeconds"))

    @maximum_batching_window_in_seconds.setter
    def maximum_batching_window_in_seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__353ed11d2a6568413b5e5dc87159ad17fcd25638ec363fb72bfac09964da9991)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maximumBatchingWindowInSeconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="queueName")
    def queue_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "queueName"))

    @queue_name.setter
    def queue_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0d6889f28c037b6a8a431364c5f92511cb2faa33ff72a1e7c64e069eff1db48f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "queueName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[PipesPipeSourceParametersActivemqBrokerParameters]:
        return typing.cast(typing.Optional[PipesPipeSourceParametersActivemqBrokerParameters], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[PipesPipeSourceParametersActivemqBrokerParameters],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__69f4528ef97f521cbcc6385db693c7c954811dee9ff39c6f88ca34810b00acd7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.pipesPipe.PipesPipeSourceParametersDynamodbStreamParameters",
    jsii_struct_bases=[],
    name_mapping={
        "starting_position": "startingPosition",
        "batch_size": "batchSize",
        "dead_letter_config": "deadLetterConfig",
        "maximum_batching_window_in_seconds": "maximumBatchingWindowInSeconds",
        "maximum_record_age_in_seconds": "maximumRecordAgeInSeconds",
        "maximum_retry_attempts": "maximumRetryAttempts",
        "on_partial_batch_item_failure": "onPartialBatchItemFailure",
        "parallelization_factor": "parallelizationFactor",
    },
)
class PipesPipeSourceParametersDynamodbStreamParameters:
    def __init__(
        self,
        *,
        starting_position: builtins.str,
        batch_size: typing.Optional[jsii.Number] = None,
        dead_letter_config: typing.Optional[typing.Union["PipesPipeSourceParametersDynamodbStreamParametersDeadLetterConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        maximum_batching_window_in_seconds: typing.Optional[jsii.Number] = None,
        maximum_record_age_in_seconds: typing.Optional[jsii.Number] = None,
        maximum_retry_attempts: typing.Optional[jsii.Number] = None,
        on_partial_batch_item_failure: typing.Optional[builtins.str] = None,
        parallelization_factor: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param starting_position: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#starting_position PipesPipe#starting_position}.
        :param batch_size: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#batch_size PipesPipe#batch_size}.
        :param dead_letter_config: dead_letter_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#dead_letter_config PipesPipe#dead_letter_config}
        :param maximum_batching_window_in_seconds: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#maximum_batching_window_in_seconds PipesPipe#maximum_batching_window_in_seconds}.
        :param maximum_record_age_in_seconds: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#maximum_record_age_in_seconds PipesPipe#maximum_record_age_in_seconds}.
        :param maximum_retry_attempts: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#maximum_retry_attempts PipesPipe#maximum_retry_attempts}.
        :param on_partial_batch_item_failure: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#on_partial_batch_item_failure PipesPipe#on_partial_batch_item_failure}.
        :param parallelization_factor: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#parallelization_factor PipesPipe#parallelization_factor}.
        '''
        if isinstance(dead_letter_config, dict):
            dead_letter_config = PipesPipeSourceParametersDynamodbStreamParametersDeadLetterConfig(**dead_letter_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d92cf48e0a2e0ef243bfccefdb9bc34dcbbfae121dc39ca9b714761ce7dcc45)
            check_type(argname="argument starting_position", value=starting_position, expected_type=type_hints["starting_position"])
            check_type(argname="argument batch_size", value=batch_size, expected_type=type_hints["batch_size"])
            check_type(argname="argument dead_letter_config", value=dead_letter_config, expected_type=type_hints["dead_letter_config"])
            check_type(argname="argument maximum_batching_window_in_seconds", value=maximum_batching_window_in_seconds, expected_type=type_hints["maximum_batching_window_in_seconds"])
            check_type(argname="argument maximum_record_age_in_seconds", value=maximum_record_age_in_seconds, expected_type=type_hints["maximum_record_age_in_seconds"])
            check_type(argname="argument maximum_retry_attempts", value=maximum_retry_attempts, expected_type=type_hints["maximum_retry_attempts"])
            check_type(argname="argument on_partial_batch_item_failure", value=on_partial_batch_item_failure, expected_type=type_hints["on_partial_batch_item_failure"])
            check_type(argname="argument parallelization_factor", value=parallelization_factor, expected_type=type_hints["parallelization_factor"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "starting_position": starting_position,
        }
        if batch_size is not None:
            self._values["batch_size"] = batch_size
        if dead_letter_config is not None:
            self._values["dead_letter_config"] = dead_letter_config
        if maximum_batching_window_in_seconds is not None:
            self._values["maximum_batching_window_in_seconds"] = maximum_batching_window_in_seconds
        if maximum_record_age_in_seconds is not None:
            self._values["maximum_record_age_in_seconds"] = maximum_record_age_in_seconds
        if maximum_retry_attempts is not None:
            self._values["maximum_retry_attempts"] = maximum_retry_attempts
        if on_partial_batch_item_failure is not None:
            self._values["on_partial_batch_item_failure"] = on_partial_batch_item_failure
        if parallelization_factor is not None:
            self._values["parallelization_factor"] = parallelization_factor

    @builtins.property
    def starting_position(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#starting_position PipesPipe#starting_position}.'''
        result = self._values.get("starting_position")
        assert result is not None, "Required property 'starting_position' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def batch_size(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#batch_size PipesPipe#batch_size}.'''
        result = self._values.get("batch_size")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def dead_letter_config(
        self,
    ) -> typing.Optional["PipesPipeSourceParametersDynamodbStreamParametersDeadLetterConfig"]:
        '''dead_letter_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#dead_letter_config PipesPipe#dead_letter_config}
        '''
        result = self._values.get("dead_letter_config")
        return typing.cast(typing.Optional["PipesPipeSourceParametersDynamodbStreamParametersDeadLetterConfig"], result)

    @builtins.property
    def maximum_batching_window_in_seconds(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#maximum_batching_window_in_seconds PipesPipe#maximum_batching_window_in_seconds}.'''
        result = self._values.get("maximum_batching_window_in_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def maximum_record_age_in_seconds(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#maximum_record_age_in_seconds PipesPipe#maximum_record_age_in_seconds}.'''
        result = self._values.get("maximum_record_age_in_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def maximum_retry_attempts(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#maximum_retry_attempts PipesPipe#maximum_retry_attempts}.'''
        result = self._values.get("maximum_retry_attempts")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def on_partial_batch_item_failure(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#on_partial_batch_item_failure PipesPipe#on_partial_batch_item_failure}.'''
        result = self._values.get("on_partial_batch_item_failure")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def parallelization_factor(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#parallelization_factor PipesPipe#parallelization_factor}.'''
        result = self._values.get("parallelization_factor")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PipesPipeSourceParametersDynamodbStreamParameters(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.pipesPipe.PipesPipeSourceParametersDynamodbStreamParametersDeadLetterConfig",
    jsii_struct_bases=[],
    name_mapping={"arn": "arn"},
)
class PipesPipeSourceParametersDynamodbStreamParametersDeadLetterConfig:
    def __init__(self, *, arn: typing.Optional[builtins.str] = None) -> None:
        '''
        :param arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#arn PipesPipe#arn}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__17f3c9eb2a10c867822a87eb29ac10120ce1cc83bfd2afb6df1b9a27ff92b335)
            check_type(argname="argument arn", value=arn, expected_type=type_hints["arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if arn is not None:
            self._values["arn"] = arn

    @builtins.property
    def arn(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#arn PipesPipe#arn}.'''
        result = self._values.get("arn")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PipesPipeSourceParametersDynamodbStreamParametersDeadLetterConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PipesPipeSourceParametersDynamodbStreamParametersDeadLetterConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.pipesPipe.PipesPipeSourceParametersDynamodbStreamParametersDeadLetterConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e7ded94e35c7a465eb45ae9225448eebe251ffaa25f64b548def25a98636064a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetArn")
    def reset_arn(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetArn", []))

    @builtins.property
    @jsii.member(jsii_name="arnInput")
    def arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "arnInput"))

    @builtins.property
    @jsii.member(jsii_name="arn")
    def arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "arn"))

    @arn.setter
    def arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__50e5a17b48356ac1890c20772bcd9c347bb38ae8af90cac7d799a79b83c61d3e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "arn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[PipesPipeSourceParametersDynamodbStreamParametersDeadLetterConfig]:
        return typing.cast(typing.Optional[PipesPipeSourceParametersDynamodbStreamParametersDeadLetterConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[PipesPipeSourceParametersDynamodbStreamParametersDeadLetterConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__01a16692068c55565bb789940456ff099af860c71078f100e89f040808ad9ce3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class PipesPipeSourceParametersDynamodbStreamParametersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.pipesPipe.PipesPipeSourceParametersDynamodbStreamParametersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fb761fb2484ef69042220e529b2a5b6f10d0fc58c2087d04eabc712fe84b9a39)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putDeadLetterConfig")
    def put_dead_letter_config(
        self,
        *,
        arn: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#arn PipesPipe#arn}.
        '''
        value = PipesPipeSourceParametersDynamodbStreamParametersDeadLetterConfig(
            arn=arn
        )

        return typing.cast(None, jsii.invoke(self, "putDeadLetterConfig", [value]))

    @jsii.member(jsii_name="resetBatchSize")
    def reset_batch_size(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBatchSize", []))

    @jsii.member(jsii_name="resetDeadLetterConfig")
    def reset_dead_letter_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDeadLetterConfig", []))

    @jsii.member(jsii_name="resetMaximumBatchingWindowInSeconds")
    def reset_maximum_batching_window_in_seconds(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaximumBatchingWindowInSeconds", []))

    @jsii.member(jsii_name="resetMaximumRecordAgeInSeconds")
    def reset_maximum_record_age_in_seconds(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaximumRecordAgeInSeconds", []))

    @jsii.member(jsii_name="resetMaximumRetryAttempts")
    def reset_maximum_retry_attempts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaximumRetryAttempts", []))

    @jsii.member(jsii_name="resetOnPartialBatchItemFailure")
    def reset_on_partial_batch_item_failure(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOnPartialBatchItemFailure", []))

    @jsii.member(jsii_name="resetParallelizationFactor")
    def reset_parallelization_factor(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetParallelizationFactor", []))

    @builtins.property
    @jsii.member(jsii_name="deadLetterConfig")
    def dead_letter_config(
        self,
    ) -> PipesPipeSourceParametersDynamodbStreamParametersDeadLetterConfigOutputReference:
        return typing.cast(PipesPipeSourceParametersDynamodbStreamParametersDeadLetterConfigOutputReference, jsii.get(self, "deadLetterConfig"))

    @builtins.property
    @jsii.member(jsii_name="batchSizeInput")
    def batch_size_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "batchSizeInput"))

    @builtins.property
    @jsii.member(jsii_name="deadLetterConfigInput")
    def dead_letter_config_input(
        self,
    ) -> typing.Optional[PipesPipeSourceParametersDynamodbStreamParametersDeadLetterConfig]:
        return typing.cast(typing.Optional[PipesPipeSourceParametersDynamodbStreamParametersDeadLetterConfig], jsii.get(self, "deadLetterConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="maximumBatchingWindowInSecondsInput")
    def maximum_batching_window_in_seconds_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maximumBatchingWindowInSecondsInput"))

    @builtins.property
    @jsii.member(jsii_name="maximumRecordAgeInSecondsInput")
    def maximum_record_age_in_seconds_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maximumRecordAgeInSecondsInput"))

    @builtins.property
    @jsii.member(jsii_name="maximumRetryAttemptsInput")
    def maximum_retry_attempts_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maximumRetryAttemptsInput"))

    @builtins.property
    @jsii.member(jsii_name="onPartialBatchItemFailureInput")
    def on_partial_batch_item_failure_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "onPartialBatchItemFailureInput"))

    @builtins.property
    @jsii.member(jsii_name="parallelizationFactorInput")
    def parallelization_factor_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "parallelizationFactorInput"))

    @builtins.property
    @jsii.member(jsii_name="startingPositionInput")
    def starting_position_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "startingPositionInput"))

    @builtins.property
    @jsii.member(jsii_name="batchSize")
    def batch_size(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "batchSize"))

    @batch_size.setter
    def batch_size(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f41344a2516b5fd454889cca9bba545f8cb01c9d971c19b576e38e153ca5be98)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "batchSize", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maximumBatchingWindowInSeconds")
    def maximum_batching_window_in_seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maximumBatchingWindowInSeconds"))

    @maximum_batching_window_in_seconds.setter
    def maximum_batching_window_in_seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__656829594cc77b9a78b5cff97bc6f2ca94d92512e6177343d8348ec24048a6df)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maximumBatchingWindowInSeconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maximumRecordAgeInSeconds")
    def maximum_record_age_in_seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maximumRecordAgeInSeconds"))

    @maximum_record_age_in_seconds.setter
    def maximum_record_age_in_seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__222e6adcf702ca4f414e83ecfd99f50e76ab25847169cbdf1041b91296f399fb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maximumRecordAgeInSeconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maximumRetryAttempts")
    def maximum_retry_attempts(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maximumRetryAttempts"))

    @maximum_retry_attempts.setter
    def maximum_retry_attempts(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__edd065a8df1363617d07cd0d2f76d72714e678ca6c7328ad1cc7623fed9284ce)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maximumRetryAttempts", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="onPartialBatchItemFailure")
    def on_partial_batch_item_failure(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "onPartialBatchItemFailure"))

    @on_partial_batch_item_failure.setter
    def on_partial_batch_item_failure(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ff52de538bafbeb7e71ca13891c5361c68f1e7f6bc297c8f4b224d62991d13e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "onPartialBatchItemFailure", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="parallelizationFactor")
    def parallelization_factor(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "parallelizationFactor"))

    @parallelization_factor.setter
    def parallelization_factor(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0148b4c6f34c072615ab8cadaeeecbf7c51d82b97efa9a734a8ef52091689bb0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "parallelizationFactor", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="startingPosition")
    def starting_position(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "startingPosition"))

    @starting_position.setter
    def starting_position(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__711657a60e1c353f19d39dab211b02ef6ceeac547b469963a729fb8f0f4966e1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "startingPosition", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[PipesPipeSourceParametersDynamodbStreamParameters]:
        return typing.cast(typing.Optional[PipesPipeSourceParametersDynamodbStreamParameters], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[PipesPipeSourceParametersDynamodbStreamParameters],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dcce6d338df2b44dbd44eca65bacaac25fe9ccee03c93143c75966e3621af9a6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.pipesPipe.PipesPipeSourceParametersFilterCriteria",
    jsii_struct_bases=[],
    name_mapping={"filter": "filter"},
)
class PipesPipeSourceParametersFilterCriteria:
    def __init__(
        self,
        *,
        filter: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["PipesPipeSourceParametersFilterCriteriaFilter", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param filter: filter block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#filter PipesPipe#filter}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bab998576186e3754b673e6a5216b531cddcd21141daec63656614bc91e2cba5)
            check_type(argname="argument filter", value=filter, expected_type=type_hints["filter"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if filter is not None:
            self._values["filter"] = filter

    @builtins.property
    def filter(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["PipesPipeSourceParametersFilterCriteriaFilter"]]]:
        '''filter block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#filter PipesPipe#filter}
        '''
        result = self._values.get("filter")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["PipesPipeSourceParametersFilterCriteriaFilter"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PipesPipeSourceParametersFilterCriteria(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.pipesPipe.PipesPipeSourceParametersFilterCriteriaFilter",
    jsii_struct_bases=[],
    name_mapping={"pattern": "pattern"},
)
class PipesPipeSourceParametersFilterCriteriaFilter:
    def __init__(self, *, pattern: builtins.str) -> None:
        '''
        :param pattern: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#pattern PipesPipe#pattern}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2bdbffc64c44bea5b18a318ebd196bf2802c5d0c9c80a7d73d17aa00e83e5e7c)
            check_type(argname="argument pattern", value=pattern, expected_type=type_hints["pattern"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "pattern": pattern,
        }

    @builtins.property
    def pattern(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#pattern PipesPipe#pattern}.'''
        result = self._values.get("pattern")
        assert result is not None, "Required property 'pattern' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PipesPipeSourceParametersFilterCriteriaFilter(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PipesPipeSourceParametersFilterCriteriaFilterList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.pipesPipe.PipesPipeSourceParametersFilterCriteriaFilterList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__54cddf0a54308067c05cd625ae4707d1f36a7248262c52ba4a840e51adf9a3b5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "PipesPipeSourceParametersFilterCriteriaFilterOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bcf0cbfc078771a361c73b079326812a716bb1e5085a1365749bb1f0460cc43f)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("PipesPipeSourceParametersFilterCriteriaFilterOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__88176d401c8e67c1ce2a6bf5200b136d580f47ba959fca2392490984ccdb32bd)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fe0151a321d02bb243bb0b31df86fbdc31ded23fcc7418a4cfd46e313996ad30)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1edfa0bb2f5949a779aa866106abf60909ddaf37b8425b5881b8674a0139d28b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PipesPipeSourceParametersFilterCriteriaFilter]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PipesPipeSourceParametersFilterCriteriaFilter]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PipesPipeSourceParametersFilterCriteriaFilter]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac3ad3544c88f28a2ce01431fa1a400e206a7288b3553003b8063d298a80ba35)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class PipesPipeSourceParametersFilterCriteriaFilterOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.pipesPipe.PipesPipeSourceParametersFilterCriteriaFilterOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a19b143b126252ae83a7cbb886000999be981887c5a15daf89824bed43d4f165)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="patternInput")
    def pattern_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "patternInput"))

    @builtins.property
    @jsii.member(jsii_name="pattern")
    def pattern(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "pattern"))

    @pattern.setter
    def pattern(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c55df51f021dcd0aa119eacbb305af8fae170ab19dc863668a58b6779977ce19)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pattern", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PipesPipeSourceParametersFilterCriteriaFilter]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PipesPipeSourceParametersFilterCriteriaFilter]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PipesPipeSourceParametersFilterCriteriaFilter]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b0162f0c319d688308dfcc4d7bddac4ce3189dbd2961a834627e709e25f8c4b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class PipesPipeSourceParametersFilterCriteriaOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.pipesPipe.PipesPipeSourceParametersFilterCriteriaOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b087cc98eff2881bc14b129ad3c03c4bcf598d6dbde73c8793fcc14f5fd0324e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putFilter")
    def put_filter(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[PipesPipeSourceParametersFilterCriteriaFilter, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__035198805ae447b2139235e409c2a0cacc174a9d14f83a835d06717cd9dbade9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putFilter", [value]))

    @jsii.member(jsii_name="resetFilter")
    def reset_filter(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFilter", []))

    @builtins.property
    @jsii.member(jsii_name="filter")
    def filter(self) -> PipesPipeSourceParametersFilterCriteriaFilterList:
        return typing.cast(PipesPipeSourceParametersFilterCriteriaFilterList, jsii.get(self, "filter"))

    @builtins.property
    @jsii.member(jsii_name="filterInput")
    def filter_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PipesPipeSourceParametersFilterCriteriaFilter]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PipesPipeSourceParametersFilterCriteriaFilter]]], jsii.get(self, "filterInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[PipesPipeSourceParametersFilterCriteria]:
        return typing.cast(typing.Optional[PipesPipeSourceParametersFilterCriteria], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[PipesPipeSourceParametersFilterCriteria],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f2f599b83e70b342533f55157f928efe64c2c12e230627bf0699f0f961b5cec7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.pipesPipe.PipesPipeSourceParametersKinesisStreamParameters",
    jsii_struct_bases=[],
    name_mapping={
        "starting_position": "startingPosition",
        "batch_size": "batchSize",
        "dead_letter_config": "deadLetterConfig",
        "maximum_batching_window_in_seconds": "maximumBatchingWindowInSeconds",
        "maximum_record_age_in_seconds": "maximumRecordAgeInSeconds",
        "maximum_retry_attempts": "maximumRetryAttempts",
        "on_partial_batch_item_failure": "onPartialBatchItemFailure",
        "parallelization_factor": "parallelizationFactor",
        "starting_position_timestamp": "startingPositionTimestamp",
    },
)
class PipesPipeSourceParametersKinesisStreamParameters:
    def __init__(
        self,
        *,
        starting_position: builtins.str,
        batch_size: typing.Optional[jsii.Number] = None,
        dead_letter_config: typing.Optional[typing.Union["PipesPipeSourceParametersKinesisStreamParametersDeadLetterConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        maximum_batching_window_in_seconds: typing.Optional[jsii.Number] = None,
        maximum_record_age_in_seconds: typing.Optional[jsii.Number] = None,
        maximum_retry_attempts: typing.Optional[jsii.Number] = None,
        on_partial_batch_item_failure: typing.Optional[builtins.str] = None,
        parallelization_factor: typing.Optional[jsii.Number] = None,
        starting_position_timestamp: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param starting_position: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#starting_position PipesPipe#starting_position}.
        :param batch_size: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#batch_size PipesPipe#batch_size}.
        :param dead_letter_config: dead_letter_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#dead_letter_config PipesPipe#dead_letter_config}
        :param maximum_batching_window_in_seconds: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#maximum_batching_window_in_seconds PipesPipe#maximum_batching_window_in_seconds}.
        :param maximum_record_age_in_seconds: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#maximum_record_age_in_seconds PipesPipe#maximum_record_age_in_seconds}.
        :param maximum_retry_attempts: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#maximum_retry_attempts PipesPipe#maximum_retry_attempts}.
        :param on_partial_batch_item_failure: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#on_partial_batch_item_failure PipesPipe#on_partial_batch_item_failure}.
        :param parallelization_factor: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#parallelization_factor PipesPipe#parallelization_factor}.
        :param starting_position_timestamp: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#starting_position_timestamp PipesPipe#starting_position_timestamp}.
        '''
        if isinstance(dead_letter_config, dict):
            dead_letter_config = PipesPipeSourceParametersKinesisStreamParametersDeadLetterConfig(**dead_letter_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f9f90aa2e63904fe739da609d90b9710778f184e8ac87a68cf2b2f9d3abffe4)
            check_type(argname="argument starting_position", value=starting_position, expected_type=type_hints["starting_position"])
            check_type(argname="argument batch_size", value=batch_size, expected_type=type_hints["batch_size"])
            check_type(argname="argument dead_letter_config", value=dead_letter_config, expected_type=type_hints["dead_letter_config"])
            check_type(argname="argument maximum_batching_window_in_seconds", value=maximum_batching_window_in_seconds, expected_type=type_hints["maximum_batching_window_in_seconds"])
            check_type(argname="argument maximum_record_age_in_seconds", value=maximum_record_age_in_seconds, expected_type=type_hints["maximum_record_age_in_seconds"])
            check_type(argname="argument maximum_retry_attempts", value=maximum_retry_attempts, expected_type=type_hints["maximum_retry_attempts"])
            check_type(argname="argument on_partial_batch_item_failure", value=on_partial_batch_item_failure, expected_type=type_hints["on_partial_batch_item_failure"])
            check_type(argname="argument parallelization_factor", value=parallelization_factor, expected_type=type_hints["parallelization_factor"])
            check_type(argname="argument starting_position_timestamp", value=starting_position_timestamp, expected_type=type_hints["starting_position_timestamp"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "starting_position": starting_position,
        }
        if batch_size is not None:
            self._values["batch_size"] = batch_size
        if dead_letter_config is not None:
            self._values["dead_letter_config"] = dead_letter_config
        if maximum_batching_window_in_seconds is not None:
            self._values["maximum_batching_window_in_seconds"] = maximum_batching_window_in_seconds
        if maximum_record_age_in_seconds is not None:
            self._values["maximum_record_age_in_seconds"] = maximum_record_age_in_seconds
        if maximum_retry_attempts is not None:
            self._values["maximum_retry_attempts"] = maximum_retry_attempts
        if on_partial_batch_item_failure is not None:
            self._values["on_partial_batch_item_failure"] = on_partial_batch_item_failure
        if parallelization_factor is not None:
            self._values["parallelization_factor"] = parallelization_factor
        if starting_position_timestamp is not None:
            self._values["starting_position_timestamp"] = starting_position_timestamp

    @builtins.property
    def starting_position(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#starting_position PipesPipe#starting_position}.'''
        result = self._values.get("starting_position")
        assert result is not None, "Required property 'starting_position' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def batch_size(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#batch_size PipesPipe#batch_size}.'''
        result = self._values.get("batch_size")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def dead_letter_config(
        self,
    ) -> typing.Optional["PipesPipeSourceParametersKinesisStreamParametersDeadLetterConfig"]:
        '''dead_letter_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#dead_letter_config PipesPipe#dead_letter_config}
        '''
        result = self._values.get("dead_letter_config")
        return typing.cast(typing.Optional["PipesPipeSourceParametersKinesisStreamParametersDeadLetterConfig"], result)

    @builtins.property
    def maximum_batching_window_in_seconds(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#maximum_batching_window_in_seconds PipesPipe#maximum_batching_window_in_seconds}.'''
        result = self._values.get("maximum_batching_window_in_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def maximum_record_age_in_seconds(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#maximum_record_age_in_seconds PipesPipe#maximum_record_age_in_seconds}.'''
        result = self._values.get("maximum_record_age_in_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def maximum_retry_attempts(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#maximum_retry_attempts PipesPipe#maximum_retry_attempts}.'''
        result = self._values.get("maximum_retry_attempts")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def on_partial_batch_item_failure(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#on_partial_batch_item_failure PipesPipe#on_partial_batch_item_failure}.'''
        result = self._values.get("on_partial_batch_item_failure")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def parallelization_factor(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#parallelization_factor PipesPipe#parallelization_factor}.'''
        result = self._values.get("parallelization_factor")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def starting_position_timestamp(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#starting_position_timestamp PipesPipe#starting_position_timestamp}.'''
        result = self._values.get("starting_position_timestamp")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PipesPipeSourceParametersKinesisStreamParameters(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.pipesPipe.PipesPipeSourceParametersKinesisStreamParametersDeadLetterConfig",
    jsii_struct_bases=[],
    name_mapping={"arn": "arn"},
)
class PipesPipeSourceParametersKinesisStreamParametersDeadLetterConfig:
    def __init__(self, *, arn: typing.Optional[builtins.str] = None) -> None:
        '''
        :param arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#arn PipesPipe#arn}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2a783b1288042d64792bd0625205e0dcae484be3156fb61de08e9c24be7abe8e)
            check_type(argname="argument arn", value=arn, expected_type=type_hints["arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if arn is not None:
            self._values["arn"] = arn

    @builtins.property
    def arn(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#arn PipesPipe#arn}.'''
        result = self._values.get("arn")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PipesPipeSourceParametersKinesisStreamParametersDeadLetterConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PipesPipeSourceParametersKinesisStreamParametersDeadLetterConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.pipesPipe.PipesPipeSourceParametersKinesisStreamParametersDeadLetterConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__cc4b9cecafe3bbd6609e8b165396571c7412c99dab06a822812aa08cfab0ad38)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetArn")
    def reset_arn(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetArn", []))

    @builtins.property
    @jsii.member(jsii_name="arnInput")
    def arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "arnInput"))

    @builtins.property
    @jsii.member(jsii_name="arn")
    def arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "arn"))

    @arn.setter
    def arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bd4cfb4cafa06a1a80231088874652380c8ec46847aae0b634fab9fc6c408157)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "arn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[PipesPipeSourceParametersKinesisStreamParametersDeadLetterConfig]:
        return typing.cast(typing.Optional[PipesPipeSourceParametersKinesisStreamParametersDeadLetterConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[PipesPipeSourceParametersKinesisStreamParametersDeadLetterConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc6a73a69f0fae73912423ee3e46c7c0d0cf6b750ee1f78c912837f664ee1aa1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class PipesPipeSourceParametersKinesisStreamParametersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.pipesPipe.PipesPipeSourceParametersKinesisStreamParametersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e5ebfaca302acf1489f32b12b75ceb1396f118099a880ae760d45afeb932c524)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putDeadLetterConfig")
    def put_dead_letter_config(
        self,
        *,
        arn: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#arn PipesPipe#arn}.
        '''
        value = PipesPipeSourceParametersKinesisStreamParametersDeadLetterConfig(
            arn=arn
        )

        return typing.cast(None, jsii.invoke(self, "putDeadLetterConfig", [value]))

    @jsii.member(jsii_name="resetBatchSize")
    def reset_batch_size(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBatchSize", []))

    @jsii.member(jsii_name="resetDeadLetterConfig")
    def reset_dead_letter_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDeadLetterConfig", []))

    @jsii.member(jsii_name="resetMaximumBatchingWindowInSeconds")
    def reset_maximum_batching_window_in_seconds(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaximumBatchingWindowInSeconds", []))

    @jsii.member(jsii_name="resetMaximumRecordAgeInSeconds")
    def reset_maximum_record_age_in_seconds(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaximumRecordAgeInSeconds", []))

    @jsii.member(jsii_name="resetMaximumRetryAttempts")
    def reset_maximum_retry_attempts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaximumRetryAttempts", []))

    @jsii.member(jsii_name="resetOnPartialBatchItemFailure")
    def reset_on_partial_batch_item_failure(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOnPartialBatchItemFailure", []))

    @jsii.member(jsii_name="resetParallelizationFactor")
    def reset_parallelization_factor(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetParallelizationFactor", []))

    @jsii.member(jsii_name="resetStartingPositionTimestamp")
    def reset_starting_position_timestamp(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStartingPositionTimestamp", []))

    @builtins.property
    @jsii.member(jsii_name="deadLetterConfig")
    def dead_letter_config(
        self,
    ) -> PipesPipeSourceParametersKinesisStreamParametersDeadLetterConfigOutputReference:
        return typing.cast(PipesPipeSourceParametersKinesisStreamParametersDeadLetterConfigOutputReference, jsii.get(self, "deadLetterConfig"))

    @builtins.property
    @jsii.member(jsii_name="batchSizeInput")
    def batch_size_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "batchSizeInput"))

    @builtins.property
    @jsii.member(jsii_name="deadLetterConfigInput")
    def dead_letter_config_input(
        self,
    ) -> typing.Optional[PipesPipeSourceParametersKinesisStreamParametersDeadLetterConfig]:
        return typing.cast(typing.Optional[PipesPipeSourceParametersKinesisStreamParametersDeadLetterConfig], jsii.get(self, "deadLetterConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="maximumBatchingWindowInSecondsInput")
    def maximum_batching_window_in_seconds_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maximumBatchingWindowInSecondsInput"))

    @builtins.property
    @jsii.member(jsii_name="maximumRecordAgeInSecondsInput")
    def maximum_record_age_in_seconds_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maximumRecordAgeInSecondsInput"))

    @builtins.property
    @jsii.member(jsii_name="maximumRetryAttemptsInput")
    def maximum_retry_attempts_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maximumRetryAttemptsInput"))

    @builtins.property
    @jsii.member(jsii_name="onPartialBatchItemFailureInput")
    def on_partial_batch_item_failure_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "onPartialBatchItemFailureInput"))

    @builtins.property
    @jsii.member(jsii_name="parallelizationFactorInput")
    def parallelization_factor_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "parallelizationFactorInput"))

    @builtins.property
    @jsii.member(jsii_name="startingPositionInput")
    def starting_position_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "startingPositionInput"))

    @builtins.property
    @jsii.member(jsii_name="startingPositionTimestampInput")
    def starting_position_timestamp_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "startingPositionTimestampInput"))

    @builtins.property
    @jsii.member(jsii_name="batchSize")
    def batch_size(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "batchSize"))

    @batch_size.setter
    def batch_size(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f738618ca0b89e75f53166b45de6a856955dcad3a3907fc4cab7c056fd3d2009)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "batchSize", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maximumBatchingWindowInSeconds")
    def maximum_batching_window_in_seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maximumBatchingWindowInSeconds"))

    @maximum_batching_window_in_seconds.setter
    def maximum_batching_window_in_seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ad3eb1dd8e00e6544e815f58023dd293cc26eafb9541b4036b3b98dff9397d8e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maximumBatchingWindowInSeconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maximumRecordAgeInSeconds")
    def maximum_record_age_in_seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maximumRecordAgeInSeconds"))

    @maximum_record_age_in_seconds.setter
    def maximum_record_age_in_seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__183f7eee1b91f0bfd6a37f87c3992bfe171526c510f6774a972e671484e39390)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maximumRecordAgeInSeconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maximumRetryAttempts")
    def maximum_retry_attempts(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maximumRetryAttempts"))

    @maximum_retry_attempts.setter
    def maximum_retry_attempts(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__96fc560f690f0f3287dcdd84ba4e6b6211092a0094adc5841b6aef68a7153b64)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maximumRetryAttempts", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="onPartialBatchItemFailure")
    def on_partial_batch_item_failure(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "onPartialBatchItemFailure"))

    @on_partial_batch_item_failure.setter
    def on_partial_batch_item_failure(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__580872431b243ef4952bdc6533e29a8b06e785d79eed7c9c5ca2466b1301a6ca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "onPartialBatchItemFailure", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="parallelizationFactor")
    def parallelization_factor(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "parallelizationFactor"))

    @parallelization_factor.setter
    def parallelization_factor(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__299b8491480f0f7c231cd252f16bf76655a4284889ab7489132503eb84e72478)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "parallelizationFactor", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="startingPosition")
    def starting_position(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "startingPosition"))

    @starting_position.setter
    def starting_position(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b7bf03aa5a04ec166df98219ad2d09846b82419ccf034a4f910b851d4e8e2f53)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "startingPosition", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="startingPositionTimestamp")
    def starting_position_timestamp(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "startingPositionTimestamp"))

    @starting_position_timestamp.setter
    def starting_position_timestamp(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__962d6b3a14d2d4bc66fe485750e376eab811301e62a2048d66fc2a3ff0c39ad4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "startingPositionTimestamp", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[PipesPipeSourceParametersKinesisStreamParameters]:
        return typing.cast(typing.Optional[PipesPipeSourceParametersKinesisStreamParameters], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[PipesPipeSourceParametersKinesisStreamParameters],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__57903dc2a5a057fd493ab02052079074fbf3417a13dc93ea3c5992ad00c3d71d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.pipesPipe.PipesPipeSourceParametersManagedStreamingKafkaParameters",
    jsii_struct_bases=[],
    name_mapping={
        "topic_name": "topicName",
        "batch_size": "batchSize",
        "consumer_group_id": "consumerGroupId",
        "credentials": "credentials",
        "maximum_batching_window_in_seconds": "maximumBatchingWindowInSeconds",
        "starting_position": "startingPosition",
    },
)
class PipesPipeSourceParametersManagedStreamingKafkaParameters:
    def __init__(
        self,
        *,
        topic_name: builtins.str,
        batch_size: typing.Optional[jsii.Number] = None,
        consumer_group_id: typing.Optional[builtins.str] = None,
        credentials: typing.Optional[typing.Union["PipesPipeSourceParametersManagedStreamingKafkaParametersCredentials", typing.Dict[builtins.str, typing.Any]]] = None,
        maximum_batching_window_in_seconds: typing.Optional[jsii.Number] = None,
        starting_position: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param topic_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#topic_name PipesPipe#topic_name}.
        :param batch_size: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#batch_size PipesPipe#batch_size}.
        :param consumer_group_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#consumer_group_id PipesPipe#consumer_group_id}.
        :param credentials: credentials block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#credentials PipesPipe#credentials}
        :param maximum_batching_window_in_seconds: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#maximum_batching_window_in_seconds PipesPipe#maximum_batching_window_in_seconds}.
        :param starting_position: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#starting_position PipesPipe#starting_position}.
        '''
        if isinstance(credentials, dict):
            credentials = PipesPipeSourceParametersManagedStreamingKafkaParametersCredentials(**credentials)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d8e57f0bb431f01d39e9cae98d41d61c80f415d9a2978aa8ed68f2b287546a76)
            check_type(argname="argument topic_name", value=topic_name, expected_type=type_hints["topic_name"])
            check_type(argname="argument batch_size", value=batch_size, expected_type=type_hints["batch_size"])
            check_type(argname="argument consumer_group_id", value=consumer_group_id, expected_type=type_hints["consumer_group_id"])
            check_type(argname="argument credentials", value=credentials, expected_type=type_hints["credentials"])
            check_type(argname="argument maximum_batching_window_in_seconds", value=maximum_batching_window_in_seconds, expected_type=type_hints["maximum_batching_window_in_seconds"])
            check_type(argname="argument starting_position", value=starting_position, expected_type=type_hints["starting_position"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "topic_name": topic_name,
        }
        if batch_size is not None:
            self._values["batch_size"] = batch_size
        if consumer_group_id is not None:
            self._values["consumer_group_id"] = consumer_group_id
        if credentials is not None:
            self._values["credentials"] = credentials
        if maximum_batching_window_in_seconds is not None:
            self._values["maximum_batching_window_in_seconds"] = maximum_batching_window_in_seconds
        if starting_position is not None:
            self._values["starting_position"] = starting_position

    @builtins.property
    def topic_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#topic_name PipesPipe#topic_name}.'''
        result = self._values.get("topic_name")
        assert result is not None, "Required property 'topic_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def batch_size(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#batch_size PipesPipe#batch_size}.'''
        result = self._values.get("batch_size")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def consumer_group_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#consumer_group_id PipesPipe#consumer_group_id}.'''
        result = self._values.get("consumer_group_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def credentials(
        self,
    ) -> typing.Optional["PipesPipeSourceParametersManagedStreamingKafkaParametersCredentials"]:
        '''credentials block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#credentials PipesPipe#credentials}
        '''
        result = self._values.get("credentials")
        return typing.cast(typing.Optional["PipesPipeSourceParametersManagedStreamingKafkaParametersCredentials"], result)

    @builtins.property
    def maximum_batching_window_in_seconds(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#maximum_batching_window_in_seconds PipesPipe#maximum_batching_window_in_seconds}.'''
        result = self._values.get("maximum_batching_window_in_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def starting_position(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#starting_position PipesPipe#starting_position}.'''
        result = self._values.get("starting_position")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PipesPipeSourceParametersManagedStreamingKafkaParameters(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.pipesPipe.PipesPipeSourceParametersManagedStreamingKafkaParametersCredentials",
    jsii_struct_bases=[],
    name_mapping={
        "client_certificate_tls_auth": "clientCertificateTlsAuth",
        "sasl_scram512_auth": "saslScram512Auth",
    },
)
class PipesPipeSourceParametersManagedStreamingKafkaParametersCredentials:
    def __init__(
        self,
        *,
        client_certificate_tls_auth: typing.Optional[builtins.str] = None,
        sasl_scram512_auth: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param client_certificate_tls_auth: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#client_certificate_tls_auth PipesPipe#client_certificate_tls_auth}.
        :param sasl_scram512_auth: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#sasl_scram_512_auth PipesPipe#sasl_scram_512_auth}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5be1a7108fffe44a7f5b69eac1b0ebfd9c878d42148eba053def08fd7178a904)
            check_type(argname="argument client_certificate_tls_auth", value=client_certificate_tls_auth, expected_type=type_hints["client_certificate_tls_auth"])
            check_type(argname="argument sasl_scram512_auth", value=sasl_scram512_auth, expected_type=type_hints["sasl_scram512_auth"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if client_certificate_tls_auth is not None:
            self._values["client_certificate_tls_auth"] = client_certificate_tls_auth
        if sasl_scram512_auth is not None:
            self._values["sasl_scram512_auth"] = sasl_scram512_auth

    @builtins.property
    def client_certificate_tls_auth(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#client_certificate_tls_auth PipesPipe#client_certificate_tls_auth}.'''
        result = self._values.get("client_certificate_tls_auth")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sasl_scram512_auth(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#sasl_scram_512_auth PipesPipe#sasl_scram_512_auth}.'''
        result = self._values.get("sasl_scram512_auth")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PipesPipeSourceParametersManagedStreamingKafkaParametersCredentials(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PipesPipeSourceParametersManagedStreamingKafkaParametersCredentialsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.pipesPipe.PipesPipeSourceParametersManagedStreamingKafkaParametersCredentialsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__742613ba6577368178fa8e75b040402ddf937add134860870393d0987537a59f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetClientCertificateTlsAuth")
    def reset_client_certificate_tls_auth(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClientCertificateTlsAuth", []))

    @jsii.member(jsii_name="resetSaslScram512Auth")
    def reset_sasl_scram512_auth(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSaslScram512Auth", []))

    @builtins.property
    @jsii.member(jsii_name="clientCertificateTlsAuthInput")
    def client_certificate_tls_auth_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clientCertificateTlsAuthInput"))

    @builtins.property
    @jsii.member(jsii_name="saslScram512AuthInput")
    def sasl_scram512_auth_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "saslScram512AuthInput"))

    @builtins.property
    @jsii.member(jsii_name="clientCertificateTlsAuth")
    def client_certificate_tls_auth(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientCertificateTlsAuth"))

    @client_certificate_tls_auth.setter
    def client_certificate_tls_auth(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8453c7c2b7e07109195b142415695862342b272a31450fc32c42b15fa27409b4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientCertificateTlsAuth", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="saslScram512Auth")
    def sasl_scram512_auth(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "saslScram512Auth"))

    @sasl_scram512_auth.setter
    def sasl_scram512_auth(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__613cc338290b57a41552a3c01e74bc1b5b54ea104fed3bd34c668bed8ee06016)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "saslScram512Auth", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[PipesPipeSourceParametersManagedStreamingKafkaParametersCredentials]:
        return typing.cast(typing.Optional[PipesPipeSourceParametersManagedStreamingKafkaParametersCredentials], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[PipesPipeSourceParametersManagedStreamingKafkaParametersCredentials],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f89232c2a79e018347ef34fb8ea11c85b668542ba2694267837370537e9a8c0e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class PipesPipeSourceParametersManagedStreamingKafkaParametersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.pipesPipe.PipesPipeSourceParametersManagedStreamingKafkaParametersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__982867587ca5d9ab866c8d879b44b16d3588371a5b76095717b197691daaa7a5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putCredentials")
    def put_credentials(
        self,
        *,
        client_certificate_tls_auth: typing.Optional[builtins.str] = None,
        sasl_scram512_auth: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param client_certificate_tls_auth: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#client_certificate_tls_auth PipesPipe#client_certificate_tls_auth}.
        :param sasl_scram512_auth: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#sasl_scram_512_auth PipesPipe#sasl_scram_512_auth}.
        '''
        value = PipesPipeSourceParametersManagedStreamingKafkaParametersCredentials(
            client_certificate_tls_auth=client_certificate_tls_auth,
            sasl_scram512_auth=sasl_scram512_auth,
        )

        return typing.cast(None, jsii.invoke(self, "putCredentials", [value]))

    @jsii.member(jsii_name="resetBatchSize")
    def reset_batch_size(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBatchSize", []))

    @jsii.member(jsii_name="resetConsumerGroupId")
    def reset_consumer_group_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConsumerGroupId", []))

    @jsii.member(jsii_name="resetCredentials")
    def reset_credentials(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCredentials", []))

    @jsii.member(jsii_name="resetMaximumBatchingWindowInSeconds")
    def reset_maximum_batching_window_in_seconds(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaximumBatchingWindowInSeconds", []))

    @jsii.member(jsii_name="resetStartingPosition")
    def reset_starting_position(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStartingPosition", []))

    @builtins.property
    @jsii.member(jsii_name="credentials")
    def credentials(
        self,
    ) -> PipesPipeSourceParametersManagedStreamingKafkaParametersCredentialsOutputReference:
        return typing.cast(PipesPipeSourceParametersManagedStreamingKafkaParametersCredentialsOutputReference, jsii.get(self, "credentials"))

    @builtins.property
    @jsii.member(jsii_name="batchSizeInput")
    def batch_size_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "batchSizeInput"))

    @builtins.property
    @jsii.member(jsii_name="consumerGroupIdInput")
    def consumer_group_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "consumerGroupIdInput"))

    @builtins.property
    @jsii.member(jsii_name="credentialsInput")
    def credentials_input(
        self,
    ) -> typing.Optional[PipesPipeSourceParametersManagedStreamingKafkaParametersCredentials]:
        return typing.cast(typing.Optional[PipesPipeSourceParametersManagedStreamingKafkaParametersCredentials], jsii.get(self, "credentialsInput"))

    @builtins.property
    @jsii.member(jsii_name="maximumBatchingWindowInSecondsInput")
    def maximum_batching_window_in_seconds_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maximumBatchingWindowInSecondsInput"))

    @builtins.property
    @jsii.member(jsii_name="startingPositionInput")
    def starting_position_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "startingPositionInput"))

    @builtins.property
    @jsii.member(jsii_name="topicNameInput")
    def topic_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "topicNameInput"))

    @builtins.property
    @jsii.member(jsii_name="batchSize")
    def batch_size(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "batchSize"))

    @batch_size.setter
    def batch_size(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__078f543e8ec5695368c24058114962c550f3f4856833ef087141a8180154dfad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "batchSize", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="consumerGroupId")
    def consumer_group_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "consumerGroupId"))

    @consumer_group_id.setter
    def consumer_group_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ca0c428931e235840267b0b46153971e861037e2aaa2a1fc394f8ebb84aaeec0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "consumerGroupId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maximumBatchingWindowInSeconds")
    def maximum_batching_window_in_seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maximumBatchingWindowInSeconds"))

    @maximum_batching_window_in_seconds.setter
    def maximum_batching_window_in_seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f2bb3bcfeedba46c18feb5af6684d71a7e17ad556bfe81df7986568fdd9ec85)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maximumBatchingWindowInSeconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="startingPosition")
    def starting_position(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "startingPosition"))

    @starting_position.setter
    def starting_position(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__61f83ceafd4492b621b62ae0df2a65dd59863191eac8e59191a5955c13a4c174)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "startingPosition", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="topicName")
    def topic_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "topicName"))

    @topic_name.setter
    def topic_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a3ec5fed631762c85df9a0f756fcdad215efdfa329a5e13f4c826b73185cae2a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "topicName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[PipesPipeSourceParametersManagedStreamingKafkaParameters]:
        return typing.cast(typing.Optional[PipesPipeSourceParametersManagedStreamingKafkaParameters], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[PipesPipeSourceParametersManagedStreamingKafkaParameters],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6529b3ded0ec23e01d1f6120b98307919ff41913128ecd8a907cdbd93437c811)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class PipesPipeSourceParametersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.pipesPipe.PipesPipeSourceParametersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5a6ade3553dd1b8a7c1cadb5cfd61673112c6cf724fca73d996792be37581fb8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putActivemqBrokerParameters")
    def put_activemq_broker_parameters(
        self,
        *,
        credentials: typing.Union[PipesPipeSourceParametersActivemqBrokerParametersCredentials, typing.Dict[builtins.str, typing.Any]],
        queue_name: builtins.str,
        batch_size: typing.Optional[jsii.Number] = None,
        maximum_batching_window_in_seconds: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param credentials: credentials block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#credentials PipesPipe#credentials}
        :param queue_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#queue_name PipesPipe#queue_name}.
        :param batch_size: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#batch_size PipesPipe#batch_size}.
        :param maximum_batching_window_in_seconds: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#maximum_batching_window_in_seconds PipesPipe#maximum_batching_window_in_seconds}.
        '''
        value = PipesPipeSourceParametersActivemqBrokerParameters(
            credentials=credentials,
            queue_name=queue_name,
            batch_size=batch_size,
            maximum_batching_window_in_seconds=maximum_batching_window_in_seconds,
        )

        return typing.cast(None, jsii.invoke(self, "putActivemqBrokerParameters", [value]))

    @jsii.member(jsii_name="putDynamodbStreamParameters")
    def put_dynamodb_stream_parameters(
        self,
        *,
        starting_position: builtins.str,
        batch_size: typing.Optional[jsii.Number] = None,
        dead_letter_config: typing.Optional[typing.Union[PipesPipeSourceParametersDynamodbStreamParametersDeadLetterConfig, typing.Dict[builtins.str, typing.Any]]] = None,
        maximum_batching_window_in_seconds: typing.Optional[jsii.Number] = None,
        maximum_record_age_in_seconds: typing.Optional[jsii.Number] = None,
        maximum_retry_attempts: typing.Optional[jsii.Number] = None,
        on_partial_batch_item_failure: typing.Optional[builtins.str] = None,
        parallelization_factor: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param starting_position: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#starting_position PipesPipe#starting_position}.
        :param batch_size: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#batch_size PipesPipe#batch_size}.
        :param dead_letter_config: dead_letter_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#dead_letter_config PipesPipe#dead_letter_config}
        :param maximum_batching_window_in_seconds: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#maximum_batching_window_in_seconds PipesPipe#maximum_batching_window_in_seconds}.
        :param maximum_record_age_in_seconds: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#maximum_record_age_in_seconds PipesPipe#maximum_record_age_in_seconds}.
        :param maximum_retry_attempts: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#maximum_retry_attempts PipesPipe#maximum_retry_attempts}.
        :param on_partial_batch_item_failure: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#on_partial_batch_item_failure PipesPipe#on_partial_batch_item_failure}.
        :param parallelization_factor: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#parallelization_factor PipesPipe#parallelization_factor}.
        '''
        value = PipesPipeSourceParametersDynamodbStreamParameters(
            starting_position=starting_position,
            batch_size=batch_size,
            dead_letter_config=dead_letter_config,
            maximum_batching_window_in_seconds=maximum_batching_window_in_seconds,
            maximum_record_age_in_seconds=maximum_record_age_in_seconds,
            maximum_retry_attempts=maximum_retry_attempts,
            on_partial_batch_item_failure=on_partial_batch_item_failure,
            parallelization_factor=parallelization_factor,
        )

        return typing.cast(None, jsii.invoke(self, "putDynamodbStreamParameters", [value]))

    @jsii.member(jsii_name="putFilterCriteria")
    def put_filter_criteria(
        self,
        *,
        filter: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[PipesPipeSourceParametersFilterCriteriaFilter, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param filter: filter block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#filter PipesPipe#filter}
        '''
        value = PipesPipeSourceParametersFilterCriteria(filter=filter)

        return typing.cast(None, jsii.invoke(self, "putFilterCriteria", [value]))

    @jsii.member(jsii_name="putKinesisStreamParameters")
    def put_kinesis_stream_parameters(
        self,
        *,
        starting_position: builtins.str,
        batch_size: typing.Optional[jsii.Number] = None,
        dead_letter_config: typing.Optional[typing.Union[PipesPipeSourceParametersKinesisStreamParametersDeadLetterConfig, typing.Dict[builtins.str, typing.Any]]] = None,
        maximum_batching_window_in_seconds: typing.Optional[jsii.Number] = None,
        maximum_record_age_in_seconds: typing.Optional[jsii.Number] = None,
        maximum_retry_attempts: typing.Optional[jsii.Number] = None,
        on_partial_batch_item_failure: typing.Optional[builtins.str] = None,
        parallelization_factor: typing.Optional[jsii.Number] = None,
        starting_position_timestamp: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param starting_position: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#starting_position PipesPipe#starting_position}.
        :param batch_size: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#batch_size PipesPipe#batch_size}.
        :param dead_letter_config: dead_letter_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#dead_letter_config PipesPipe#dead_letter_config}
        :param maximum_batching_window_in_seconds: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#maximum_batching_window_in_seconds PipesPipe#maximum_batching_window_in_seconds}.
        :param maximum_record_age_in_seconds: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#maximum_record_age_in_seconds PipesPipe#maximum_record_age_in_seconds}.
        :param maximum_retry_attempts: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#maximum_retry_attempts PipesPipe#maximum_retry_attempts}.
        :param on_partial_batch_item_failure: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#on_partial_batch_item_failure PipesPipe#on_partial_batch_item_failure}.
        :param parallelization_factor: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#parallelization_factor PipesPipe#parallelization_factor}.
        :param starting_position_timestamp: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#starting_position_timestamp PipesPipe#starting_position_timestamp}.
        '''
        value = PipesPipeSourceParametersKinesisStreamParameters(
            starting_position=starting_position,
            batch_size=batch_size,
            dead_letter_config=dead_letter_config,
            maximum_batching_window_in_seconds=maximum_batching_window_in_seconds,
            maximum_record_age_in_seconds=maximum_record_age_in_seconds,
            maximum_retry_attempts=maximum_retry_attempts,
            on_partial_batch_item_failure=on_partial_batch_item_failure,
            parallelization_factor=parallelization_factor,
            starting_position_timestamp=starting_position_timestamp,
        )

        return typing.cast(None, jsii.invoke(self, "putKinesisStreamParameters", [value]))

    @jsii.member(jsii_name="putManagedStreamingKafkaParameters")
    def put_managed_streaming_kafka_parameters(
        self,
        *,
        topic_name: builtins.str,
        batch_size: typing.Optional[jsii.Number] = None,
        consumer_group_id: typing.Optional[builtins.str] = None,
        credentials: typing.Optional[typing.Union[PipesPipeSourceParametersManagedStreamingKafkaParametersCredentials, typing.Dict[builtins.str, typing.Any]]] = None,
        maximum_batching_window_in_seconds: typing.Optional[jsii.Number] = None,
        starting_position: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param topic_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#topic_name PipesPipe#topic_name}.
        :param batch_size: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#batch_size PipesPipe#batch_size}.
        :param consumer_group_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#consumer_group_id PipesPipe#consumer_group_id}.
        :param credentials: credentials block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#credentials PipesPipe#credentials}
        :param maximum_batching_window_in_seconds: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#maximum_batching_window_in_seconds PipesPipe#maximum_batching_window_in_seconds}.
        :param starting_position: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#starting_position PipesPipe#starting_position}.
        '''
        value = PipesPipeSourceParametersManagedStreamingKafkaParameters(
            topic_name=topic_name,
            batch_size=batch_size,
            consumer_group_id=consumer_group_id,
            credentials=credentials,
            maximum_batching_window_in_seconds=maximum_batching_window_in_seconds,
            starting_position=starting_position,
        )

        return typing.cast(None, jsii.invoke(self, "putManagedStreamingKafkaParameters", [value]))

    @jsii.member(jsii_name="putRabbitmqBrokerParameters")
    def put_rabbitmq_broker_parameters(
        self,
        *,
        credentials: typing.Union["PipesPipeSourceParametersRabbitmqBrokerParametersCredentials", typing.Dict[builtins.str, typing.Any]],
        queue_name: builtins.str,
        batch_size: typing.Optional[jsii.Number] = None,
        maximum_batching_window_in_seconds: typing.Optional[jsii.Number] = None,
        virtual_host: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param credentials: credentials block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#credentials PipesPipe#credentials}
        :param queue_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#queue_name PipesPipe#queue_name}.
        :param batch_size: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#batch_size PipesPipe#batch_size}.
        :param maximum_batching_window_in_seconds: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#maximum_batching_window_in_seconds PipesPipe#maximum_batching_window_in_seconds}.
        :param virtual_host: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#virtual_host PipesPipe#virtual_host}.
        '''
        value = PipesPipeSourceParametersRabbitmqBrokerParameters(
            credentials=credentials,
            queue_name=queue_name,
            batch_size=batch_size,
            maximum_batching_window_in_seconds=maximum_batching_window_in_seconds,
            virtual_host=virtual_host,
        )

        return typing.cast(None, jsii.invoke(self, "putRabbitmqBrokerParameters", [value]))

    @jsii.member(jsii_name="putSelfManagedKafkaParameters")
    def put_self_managed_kafka_parameters(
        self,
        *,
        topic_name: builtins.str,
        additional_bootstrap_servers: typing.Optional[typing.Sequence[builtins.str]] = None,
        batch_size: typing.Optional[jsii.Number] = None,
        consumer_group_id: typing.Optional[builtins.str] = None,
        credentials: typing.Optional[typing.Union["PipesPipeSourceParametersSelfManagedKafkaParametersCredentials", typing.Dict[builtins.str, typing.Any]]] = None,
        maximum_batching_window_in_seconds: typing.Optional[jsii.Number] = None,
        server_root_ca_certificate: typing.Optional[builtins.str] = None,
        starting_position: typing.Optional[builtins.str] = None,
        vpc: typing.Optional[typing.Union["PipesPipeSourceParametersSelfManagedKafkaParametersVpc", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param topic_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#topic_name PipesPipe#topic_name}.
        :param additional_bootstrap_servers: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#additional_bootstrap_servers PipesPipe#additional_bootstrap_servers}.
        :param batch_size: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#batch_size PipesPipe#batch_size}.
        :param consumer_group_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#consumer_group_id PipesPipe#consumer_group_id}.
        :param credentials: credentials block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#credentials PipesPipe#credentials}
        :param maximum_batching_window_in_seconds: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#maximum_batching_window_in_seconds PipesPipe#maximum_batching_window_in_seconds}.
        :param server_root_ca_certificate: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#server_root_ca_certificate PipesPipe#server_root_ca_certificate}.
        :param starting_position: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#starting_position PipesPipe#starting_position}.
        :param vpc: vpc block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#vpc PipesPipe#vpc}
        '''
        value = PipesPipeSourceParametersSelfManagedKafkaParameters(
            topic_name=topic_name,
            additional_bootstrap_servers=additional_bootstrap_servers,
            batch_size=batch_size,
            consumer_group_id=consumer_group_id,
            credentials=credentials,
            maximum_batching_window_in_seconds=maximum_batching_window_in_seconds,
            server_root_ca_certificate=server_root_ca_certificate,
            starting_position=starting_position,
            vpc=vpc,
        )

        return typing.cast(None, jsii.invoke(self, "putSelfManagedKafkaParameters", [value]))

    @jsii.member(jsii_name="putSqsQueueParameters")
    def put_sqs_queue_parameters(
        self,
        *,
        batch_size: typing.Optional[jsii.Number] = None,
        maximum_batching_window_in_seconds: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param batch_size: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#batch_size PipesPipe#batch_size}.
        :param maximum_batching_window_in_seconds: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#maximum_batching_window_in_seconds PipesPipe#maximum_batching_window_in_seconds}.
        '''
        value = PipesPipeSourceParametersSqsQueueParameters(
            batch_size=batch_size,
            maximum_batching_window_in_seconds=maximum_batching_window_in_seconds,
        )

        return typing.cast(None, jsii.invoke(self, "putSqsQueueParameters", [value]))

    @jsii.member(jsii_name="resetActivemqBrokerParameters")
    def reset_activemq_broker_parameters(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetActivemqBrokerParameters", []))

    @jsii.member(jsii_name="resetDynamodbStreamParameters")
    def reset_dynamodb_stream_parameters(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDynamodbStreamParameters", []))

    @jsii.member(jsii_name="resetFilterCriteria")
    def reset_filter_criteria(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFilterCriteria", []))

    @jsii.member(jsii_name="resetKinesisStreamParameters")
    def reset_kinesis_stream_parameters(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKinesisStreamParameters", []))

    @jsii.member(jsii_name="resetManagedStreamingKafkaParameters")
    def reset_managed_streaming_kafka_parameters(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetManagedStreamingKafkaParameters", []))

    @jsii.member(jsii_name="resetRabbitmqBrokerParameters")
    def reset_rabbitmq_broker_parameters(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRabbitmqBrokerParameters", []))

    @jsii.member(jsii_name="resetSelfManagedKafkaParameters")
    def reset_self_managed_kafka_parameters(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSelfManagedKafkaParameters", []))

    @jsii.member(jsii_name="resetSqsQueueParameters")
    def reset_sqs_queue_parameters(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSqsQueueParameters", []))

    @builtins.property
    @jsii.member(jsii_name="activemqBrokerParameters")
    def activemq_broker_parameters(
        self,
    ) -> PipesPipeSourceParametersActivemqBrokerParametersOutputReference:
        return typing.cast(PipesPipeSourceParametersActivemqBrokerParametersOutputReference, jsii.get(self, "activemqBrokerParameters"))

    @builtins.property
    @jsii.member(jsii_name="dynamodbStreamParameters")
    def dynamodb_stream_parameters(
        self,
    ) -> PipesPipeSourceParametersDynamodbStreamParametersOutputReference:
        return typing.cast(PipesPipeSourceParametersDynamodbStreamParametersOutputReference, jsii.get(self, "dynamodbStreamParameters"))

    @builtins.property
    @jsii.member(jsii_name="filterCriteria")
    def filter_criteria(self) -> PipesPipeSourceParametersFilterCriteriaOutputReference:
        return typing.cast(PipesPipeSourceParametersFilterCriteriaOutputReference, jsii.get(self, "filterCriteria"))

    @builtins.property
    @jsii.member(jsii_name="kinesisStreamParameters")
    def kinesis_stream_parameters(
        self,
    ) -> PipesPipeSourceParametersKinesisStreamParametersOutputReference:
        return typing.cast(PipesPipeSourceParametersKinesisStreamParametersOutputReference, jsii.get(self, "kinesisStreamParameters"))

    @builtins.property
    @jsii.member(jsii_name="managedStreamingKafkaParameters")
    def managed_streaming_kafka_parameters(
        self,
    ) -> PipesPipeSourceParametersManagedStreamingKafkaParametersOutputReference:
        return typing.cast(PipesPipeSourceParametersManagedStreamingKafkaParametersOutputReference, jsii.get(self, "managedStreamingKafkaParameters"))

    @builtins.property
    @jsii.member(jsii_name="rabbitmqBrokerParameters")
    def rabbitmq_broker_parameters(
        self,
    ) -> "PipesPipeSourceParametersRabbitmqBrokerParametersOutputReference":
        return typing.cast("PipesPipeSourceParametersRabbitmqBrokerParametersOutputReference", jsii.get(self, "rabbitmqBrokerParameters"))

    @builtins.property
    @jsii.member(jsii_name="selfManagedKafkaParameters")
    def self_managed_kafka_parameters(
        self,
    ) -> "PipesPipeSourceParametersSelfManagedKafkaParametersOutputReference":
        return typing.cast("PipesPipeSourceParametersSelfManagedKafkaParametersOutputReference", jsii.get(self, "selfManagedKafkaParameters"))

    @builtins.property
    @jsii.member(jsii_name="sqsQueueParameters")
    def sqs_queue_parameters(
        self,
    ) -> "PipesPipeSourceParametersSqsQueueParametersOutputReference":
        return typing.cast("PipesPipeSourceParametersSqsQueueParametersOutputReference", jsii.get(self, "sqsQueueParameters"))

    @builtins.property
    @jsii.member(jsii_name="activemqBrokerParametersInput")
    def activemq_broker_parameters_input(
        self,
    ) -> typing.Optional[PipesPipeSourceParametersActivemqBrokerParameters]:
        return typing.cast(typing.Optional[PipesPipeSourceParametersActivemqBrokerParameters], jsii.get(self, "activemqBrokerParametersInput"))

    @builtins.property
    @jsii.member(jsii_name="dynamodbStreamParametersInput")
    def dynamodb_stream_parameters_input(
        self,
    ) -> typing.Optional[PipesPipeSourceParametersDynamodbStreamParameters]:
        return typing.cast(typing.Optional[PipesPipeSourceParametersDynamodbStreamParameters], jsii.get(self, "dynamodbStreamParametersInput"))

    @builtins.property
    @jsii.member(jsii_name="filterCriteriaInput")
    def filter_criteria_input(
        self,
    ) -> typing.Optional[PipesPipeSourceParametersFilterCriteria]:
        return typing.cast(typing.Optional[PipesPipeSourceParametersFilterCriteria], jsii.get(self, "filterCriteriaInput"))

    @builtins.property
    @jsii.member(jsii_name="kinesisStreamParametersInput")
    def kinesis_stream_parameters_input(
        self,
    ) -> typing.Optional[PipesPipeSourceParametersKinesisStreamParameters]:
        return typing.cast(typing.Optional[PipesPipeSourceParametersKinesisStreamParameters], jsii.get(self, "kinesisStreamParametersInput"))

    @builtins.property
    @jsii.member(jsii_name="managedStreamingKafkaParametersInput")
    def managed_streaming_kafka_parameters_input(
        self,
    ) -> typing.Optional[PipesPipeSourceParametersManagedStreamingKafkaParameters]:
        return typing.cast(typing.Optional[PipesPipeSourceParametersManagedStreamingKafkaParameters], jsii.get(self, "managedStreamingKafkaParametersInput"))

    @builtins.property
    @jsii.member(jsii_name="rabbitmqBrokerParametersInput")
    def rabbitmq_broker_parameters_input(
        self,
    ) -> typing.Optional["PipesPipeSourceParametersRabbitmqBrokerParameters"]:
        return typing.cast(typing.Optional["PipesPipeSourceParametersRabbitmqBrokerParameters"], jsii.get(self, "rabbitmqBrokerParametersInput"))

    @builtins.property
    @jsii.member(jsii_name="selfManagedKafkaParametersInput")
    def self_managed_kafka_parameters_input(
        self,
    ) -> typing.Optional["PipesPipeSourceParametersSelfManagedKafkaParameters"]:
        return typing.cast(typing.Optional["PipesPipeSourceParametersSelfManagedKafkaParameters"], jsii.get(self, "selfManagedKafkaParametersInput"))

    @builtins.property
    @jsii.member(jsii_name="sqsQueueParametersInput")
    def sqs_queue_parameters_input(
        self,
    ) -> typing.Optional["PipesPipeSourceParametersSqsQueueParameters"]:
        return typing.cast(typing.Optional["PipesPipeSourceParametersSqsQueueParameters"], jsii.get(self, "sqsQueueParametersInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[PipesPipeSourceParameters]:
        return typing.cast(typing.Optional[PipesPipeSourceParameters], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[PipesPipeSourceParameters]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fd1b76f42c4984c4384302a8533169e6448dbdf8403b014d7fe876137b4eb681)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.pipesPipe.PipesPipeSourceParametersRabbitmqBrokerParameters",
    jsii_struct_bases=[],
    name_mapping={
        "credentials": "credentials",
        "queue_name": "queueName",
        "batch_size": "batchSize",
        "maximum_batching_window_in_seconds": "maximumBatchingWindowInSeconds",
        "virtual_host": "virtualHost",
    },
)
class PipesPipeSourceParametersRabbitmqBrokerParameters:
    def __init__(
        self,
        *,
        credentials: typing.Union["PipesPipeSourceParametersRabbitmqBrokerParametersCredentials", typing.Dict[builtins.str, typing.Any]],
        queue_name: builtins.str,
        batch_size: typing.Optional[jsii.Number] = None,
        maximum_batching_window_in_seconds: typing.Optional[jsii.Number] = None,
        virtual_host: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param credentials: credentials block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#credentials PipesPipe#credentials}
        :param queue_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#queue_name PipesPipe#queue_name}.
        :param batch_size: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#batch_size PipesPipe#batch_size}.
        :param maximum_batching_window_in_seconds: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#maximum_batching_window_in_seconds PipesPipe#maximum_batching_window_in_seconds}.
        :param virtual_host: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#virtual_host PipesPipe#virtual_host}.
        '''
        if isinstance(credentials, dict):
            credentials = PipesPipeSourceParametersRabbitmqBrokerParametersCredentials(**credentials)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8316a77d60c73d069acaa60480d7b2dd42d9bb5add3bb3db33aad7fcc5653fe8)
            check_type(argname="argument credentials", value=credentials, expected_type=type_hints["credentials"])
            check_type(argname="argument queue_name", value=queue_name, expected_type=type_hints["queue_name"])
            check_type(argname="argument batch_size", value=batch_size, expected_type=type_hints["batch_size"])
            check_type(argname="argument maximum_batching_window_in_seconds", value=maximum_batching_window_in_seconds, expected_type=type_hints["maximum_batching_window_in_seconds"])
            check_type(argname="argument virtual_host", value=virtual_host, expected_type=type_hints["virtual_host"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "credentials": credentials,
            "queue_name": queue_name,
        }
        if batch_size is not None:
            self._values["batch_size"] = batch_size
        if maximum_batching_window_in_seconds is not None:
            self._values["maximum_batching_window_in_seconds"] = maximum_batching_window_in_seconds
        if virtual_host is not None:
            self._values["virtual_host"] = virtual_host

    @builtins.property
    def credentials(
        self,
    ) -> "PipesPipeSourceParametersRabbitmqBrokerParametersCredentials":
        '''credentials block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#credentials PipesPipe#credentials}
        '''
        result = self._values.get("credentials")
        assert result is not None, "Required property 'credentials' is missing"
        return typing.cast("PipesPipeSourceParametersRabbitmqBrokerParametersCredentials", result)

    @builtins.property
    def queue_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#queue_name PipesPipe#queue_name}.'''
        result = self._values.get("queue_name")
        assert result is not None, "Required property 'queue_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def batch_size(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#batch_size PipesPipe#batch_size}.'''
        result = self._values.get("batch_size")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def maximum_batching_window_in_seconds(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#maximum_batching_window_in_seconds PipesPipe#maximum_batching_window_in_seconds}.'''
        result = self._values.get("maximum_batching_window_in_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def virtual_host(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#virtual_host PipesPipe#virtual_host}.'''
        result = self._values.get("virtual_host")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PipesPipeSourceParametersRabbitmqBrokerParameters(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.pipesPipe.PipesPipeSourceParametersRabbitmqBrokerParametersCredentials",
    jsii_struct_bases=[],
    name_mapping={"basic_auth": "basicAuth"},
)
class PipesPipeSourceParametersRabbitmqBrokerParametersCredentials:
    def __init__(self, *, basic_auth: builtins.str) -> None:
        '''
        :param basic_auth: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#basic_auth PipesPipe#basic_auth}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a743ed7fec946ec857124e7e6670cc58ee80e15db7964145a6aa4fffe890b953)
            check_type(argname="argument basic_auth", value=basic_auth, expected_type=type_hints["basic_auth"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "basic_auth": basic_auth,
        }

    @builtins.property
    def basic_auth(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#basic_auth PipesPipe#basic_auth}.'''
        result = self._values.get("basic_auth")
        assert result is not None, "Required property 'basic_auth' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PipesPipeSourceParametersRabbitmqBrokerParametersCredentials(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PipesPipeSourceParametersRabbitmqBrokerParametersCredentialsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.pipesPipe.PipesPipeSourceParametersRabbitmqBrokerParametersCredentialsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__dc234f6da4a42b71d3351920961f877624bfb7a7d8cb7dc5882bf7fe2ecd0c2a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="basicAuthInput")
    def basic_auth_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "basicAuthInput"))

    @builtins.property
    @jsii.member(jsii_name="basicAuth")
    def basic_auth(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "basicAuth"))

    @basic_auth.setter
    def basic_auth(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d415291bb78149ac0601b9fe3867eaeb6a287028e59fde668a0a60bf37b8ce74)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "basicAuth", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[PipesPipeSourceParametersRabbitmqBrokerParametersCredentials]:
        return typing.cast(typing.Optional[PipesPipeSourceParametersRabbitmqBrokerParametersCredentials], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[PipesPipeSourceParametersRabbitmqBrokerParametersCredentials],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__504dccfd46ba8c533d75278d9bc3db4b65e758c89be2acb458339c98f99f57d0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class PipesPipeSourceParametersRabbitmqBrokerParametersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.pipesPipe.PipesPipeSourceParametersRabbitmqBrokerParametersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4dc9d8d53e0c534d91046b63547d53861858afa8d31fad8e73c60a8c93d2b7e9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putCredentials")
    def put_credentials(self, *, basic_auth: builtins.str) -> None:
        '''
        :param basic_auth: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#basic_auth PipesPipe#basic_auth}.
        '''
        value = PipesPipeSourceParametersRabbitmqBrokerParametersCredentials(
            basic_auth=basic_auth
        )

        return typing.cast(None, jsii.invoke(self, "putCredentials", [value]))

    @jsii.member(jsii_name="resetBatchSize")
    def reset_batch_size(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBatchSize", []))

    @jsii.member(jsii_name="resetMaximumBatchingWindowInSeconds")
    def reset_maximum_batching_window_in_seconds(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaximumBatchingWindowInSeconds", []))

    @jsii.member(jsii_name="resetVirtualHost")
    def reset_virtual_host(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVirtualHost", []))

    @builtins.property
    @jsii.member(jsii_name="credentials")
    def credentials(
        self,
    ) -> PipesPipeSourceParametersRabbitmqBrokerParametersCredentialsOutputReference:
        return typing.cast(PipesPipeSourceParametersRabbitmqBrokerParametersCredentialsOutputReference, jsii.get(self, "credentials"))

    @builtins.property
    @jsii.member(jsii_name="batchSizeInput")
    def batch_size_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "batchSizeInput"))

    @builtins.property
    @jsii.member(jsii_name="credentialsInput")
    def credentials_input(
        self,
    ) -> typing.Optional[PipesPipeSourceParametersRabbitmqBrokerParametersCredentials]:
        return typing.cast(typing.Optional[PipesPipeSourceParametersRabbitmqBrokerParametersCredentials], jsii.get(self, "credentialsInput"))

    @builtins.property
    @jsii.member(jsii_name="maximumBatchingWindowInSecondsInput")
    def maximum_batching_window_in_seconds_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maximumBatchingWindowInSecondsInput"))

    @builtins.property
    @jsii.member(jsii_name="queueNameInput")
    def queue_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "queueNameInput"))

    @builtins.property
    @jsii.member(jsii_name="virtualHostInput")
    def virtual_host_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "virtualHostInput"))

    @builtins.property
    @jsii.member(jsii_name="batchSize")
    def batch_size(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "batchSize"))

    @batch_size.setter
    def batch_size(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d832636062a2385ff4217a349a3817a204cb201d1092e1b5f68a9c0fab7668e5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "batchSize", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maximumBatchingWindowInSeconds")
    def maximum_batching_window_in_seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maximumBatchingWindowInSeconds"))

    @maximum_batching_window_in_seconds.setter
    def maximum_batching_window_in_seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a51f5a4bc275163226a983fd8a26cbe64be7a8debc5d6e1c2cdf7d4dbceee62)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maximumBatchingWindowInSeconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="queueName")
    def queue_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "queueName"))

    @queue_name.setter
    def queue_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7ca494a282a45fd07e975c52e2f6d6393aefbb9d49ba25b31a87cf406980800d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "queueName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="virtualHost")
    def virtual_host(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "virtualHost"))

    @virtual_host.setter
    def virtual_host(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b39741fbded3d8fd9942a9593d7ae35a3f5d7589fe16d29570c39d15fc50e71d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "virtualHost", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[PipesPipeSourceParametersRabbitmqBrokerParameters]:
        return typing.cast(typing.Optional[PipesPipeSourceParametersRabbitmqBrokerParameters], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[PipesPipeSourceParametersRabbitmqBrokerParameters],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__25ca718af28d7d1b36311763d65b0f6f64879c29a865e4a0d45eefd193de51a2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.pipesPipe.PipesPipeSourceParametersSelfManagedKafkaParameters",
    jsii_struct_bases=[],
    name_mapping={
        "topic_name": "topicName",
        "additional_bootstrap_servers": "additionalBootstrapServers",
        "batch_size": "batchSize",
        "consumer_group_id": "consumerGroupId",
        "credentials": "credentials",
        "maximum_batching_window_in_seconds": "maximumBatchingWindowInSeconds",
        "server_root_ca_certificate": "serverRootCaCertificate",
        "starting_position": "startingPosition",
        "vpc": "vpc",
    },
)
class PipesPipeSourceParametersSelfManagedKafkaParameters:
    def __init__(
        self,
        *,
        topic_name: builtins.str,
        additional_bootstrap_servers: typing.Optional[typing.Sequence[builtins.str]] = None,
        batch_size: typing.Optional[jsii.Number] = None,
        consumer_group_id: typing.Optional[builtins.str] = None,
        credentials: typing.Optional[typing.Union["PipesPipeSourceParametersSelfManagedKafkaParametersCredentials", typing.Dict[builtins.str, typing.Any]]] = None,
        maximum_batching_window_in_seconds: typing.Optional[jsii.Number] = None,
        server_root_ca_certificate: typing.Optional[builtins.str] = None,
        starting_position: typing.Optional[builtins.str] = None,
        vpc: typing.Optional[typing.Union["PipesPipeSourceParametersSelfManagedKafkaParametersVpc", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param topic_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#topic_name PipesPipe#topic_name}.
        :param additional_bootstrap_servers: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#additional_bootstrap_servers PipesPipe#additional_bootstrap_servers}.
        :param batch_size: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#batch_size PipesPipe#batch_size}.
        :param consumer_group_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#consumer_group_id PipesPipe#consumer_group_id}.
        :param credentials: credentials block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#credentials PipesPipe#credentials}
        :param maximum_batching_window_in_seconds: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#maximum_batching_window_in_seconds PipesPipe#maximum_batching_window_in_seconds}.
        :param server_root_ca_certificate: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#server_root_ca_certificate PipesPipe#server_root_ca_certificate}.
        :param starting_position: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#starting_position PipesPipe#starting_position}.
        :param vpc: vpc block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#vpc PipesPipe#vpc}
        '''
        if isinstance(credentials, dict):
            credentials = PipesPipeSourceParametersSelfManagedKafkaParametersCredentials(**credentials)
        if isinstance(vpc, dict):
            vpc = PipesPipeSourceParametersSelfManagedKafkaParametersVpc(**vpc)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d3b7430a7afd15b9af60ac1e5c2bbb80d7691a2bd3ce5a3f6de6bb8f20438667)
            check_type(argname="argument topic_name", value=topic_name, expected_type=type_hints["topic_name"])
            check_type(argname="argument additional_bootstrap_servers", value=additional_bootstrap_servers, expected_type=type_hints["additional_bootstrap_servers"])
            check_type(argname="argument batch_size", value=batch_size, expected_type=type_hints["batch_size"])
            check_type(argname="argument consumer_group_id", value=consumer_group_id, expected_type=type_hints["consumer_group_id"])
            check_type(argname="argument credentials", value=credentials, expected_type=type_hints["credentials"])
            check_type(argname="argument maximum_batching_window_in_seconds", value=maximum_batching_window_in_seconds, expected_type=type_hints["maximum_batching_window_in_seconds"])
            check_type(argname="argument server_root_ca_certificate", value=server_root_ca_certificate, expected_type=type_hints["server_root_ca_certificate"])
            check_type(argname="argument starting_position", value=starting_position, expected_type=type_hints["starting_position"])
            check_type(argname="argument vpc", value=vpc, expected_type=type_hints["vpc"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "topic_name": topic_name,
        }
        if additional_bootstrap_servers is not None:
            self._values["additional_bootstrap_servers"] = additional_bootstrap_servers
        if batch_size is not None:
            self._values["batch_size"] = batch_size
        if consumer_group_id is not None:
            self._values["consumer_group_id"] = consumer_group_id
        if credentials is not None:
            self._values["credentials"] = credentials
        if maximum_batching_window_in_seconds is not None:
            self._values["maximum_batching_window_in_seconds"] = maximum_batching_window_in_seconds
        if server_root_ca_certificate is not None:
            self._values["server_root_ca_certificate"] = server_root_ca_certificate
        if starting_position is not None:
            self._values["starting_position"] = starting_position
        if vpc is not None:
            self._values["vpc"] = vpc

    @builtins.property
    def topic_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#topic_name PipesPipe#topic_name}.'''
        result = self._values.get("topic_name")
        assert result is not None, "Required property 'topic_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def additional_bootstrap_servers(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#additional_bootstrap_servers PipesPipe#additional_bootstrap_servers}.'''
        result = self._values.get("additional_bootstrap_servers")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def batch_size(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#batch_size PipesPipe#batch_size}.'''
        result = self._values.get("batch_size")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def consumer_group_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#consumer_group_id PipesPipe#consumer_group_id}.'''
        result = self._values.get("consumer_group_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def credentials(
        self,
    ) -> typing.Optional["PipesPipeSourceParametersSelfManagedKafkaParametersCredentials"]:
        '''credentials block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#credentials PipesPipe#credentials}
        '''
        result = self._values.get("credentials")
        return typing.cast(typing.Optional["PipesPipeSourceParametersSelfManagedKafkaParametersCredentials"], result)

    @builtins.property
    def maximum_batching_window_in_seconds(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#maximum_batching_window_in_seconds PipesPipe#maximum_batching_window_in_seconds}.'''
        result = self._values.get("maximum_batching_window_in_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def server_root_ca_certificate(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#server_root_ca_certificate PipesPipe#server_root_ca_certificate}.'''
        result = self._values.get("server_root_ca_certificate")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def starting_position(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#starting_position PipesPipe#starting_position}.'''
        result = self._values.get("starting_position")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def vpc(
        self,
    ) -> typing.Optional["PipesPipeSourceParametersSelfManagedKafkaParametersVpc"]:
        '''vpc block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#vpc PipesPipe#vpc}
        '''
        result = self._values.get("vpc")
        return typing.cast(typing.Optional["PipesPipeSourceParametersSelfManagedKafkaParametersVpc"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PipesPipeSourceParametersSelfManagedKafkaParameters(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.pipesPipe.PipesPipeSourceParametersSelfManagedKafkaParametersCredentials",
    jsii_struct_bases=[],
    name_mapping={
        "basic_auth": "basicAuth",
        "client_certificate_tls_auth": "clientCertificateTlsAuth",
        "sasl_scram256_auth": "saslScram256Auth",
        "sasl_scram512_auth": "saslScram512Auth",
    },
)
class PipesPipeSourceParametersSelfManagedKafkaParametersCredentials:
    def __init__(
        self,
        *,
        basic_auth: typing.Optional[builtins.str] = None,
        client_certificate_tls_auth: typing.Optional[builtins.str] = None,
        sasl_scram256_auth: typing.Optional[builtins.str] = None,
        sasl_scram512_auth: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param basic_auth: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#basic_auth PipesPipe#basic_auth}.
        :param client_certificate_tls_auth: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#client_certificate_tls_auth PipesPipe#client_certificate_tls_auth}.
        :param sasl_scram256_auth: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#sasl_scram_256_auth PipesPipe#sasl_scram_256_auth}.
        :param sasl_scram512_auth: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#sasl_scram_512_auth PipesPipe#sasl_scram_512_auth}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a1500725b1ae78a8f84bce66d1e29dd12d5f22bfddcc3b596b24091dfd4e88dd)
            check_type(argname="argument basic_auth", value=basic_auth, expected_type=type_hints["basic_auth"])
            check_type(argname="argument client_certificate_tls_auth", value=client_certificate_tls_auth, expected_type=type_hints["client_certificate_tls_auth"])
            check_type(argname="argument sasl_scram256_auth", value=sasl_scram256_auth, expected_type=type_hints["sasl_scram256_auth"])
            check_type(argname="argument sasl_scram512_auth", value=sasl_scram512_auth, expected_type=type_hints["sasl_scram512_auth"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if basic_auth is not None:
            self._values["basic_auth"] = basic_auth
        if client_certificate_tls_auth is not None:
            self._values["client_certificate_tls_auth"] = client_certificate_tls_auth
        if sasl_scram256_auth is not None:
            self._values["sasl_scram256_auth"] = sasl_scram256_auth
        if sasl_scram512_auth is not None:
            self._values["sasl_scram512_auth"] = sasl_scram512_auth

    @builtins.property
    def basic_auth(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#basic_auth PipesPipe#basic_auth}.'''
        result = self._values.get("basic_auth")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def client_certificate_tls_auth(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#client_certificate_tls_auth PipesPipe#client_certificate_tls_auth}.'''
        result = self._values.get("client_certificate_tls_auth")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sasl_scram256_auth(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#sasl_scram_256_auth PipesPipe#sasl_scram_256_auth}.'''
        result = self._values.get("sasl_scram256_auth")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sasl_scram512_auth(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#sasl_scram_512_auth PipesPipe#sasl_scram_512_auth}.'''
        result = self._values.get("sasl_scram512_auth")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PipesPipeSourceParametersSelfManagedKafkaParametersCredentials(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PipesPipeSourceParametersSelfManagedKafkaParametersCredentialsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.pipesPipe.PipesPipeSourceParametersSelfManagedKafkaParametersCredentialsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1b3a4748158a9dd7cd4b785e6807472804c2580d3723ceec6852e599d84af7bc)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetBasicAuth")
    def reset_basic_auth(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBasicAuth", []))

    @jsii.member(jsii_name="resetClientCertificateTlsAuth")
    def reset_client_certificate_tls_auth(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClientCertificateTlsAuth", []))

    @jsii.member(jsii_name="resetSaslScram256Auth")
    def reset_sasl_scram256_auth(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSaslScram256Auth", []))

    @jsii.member(jsii_name="resetSaslScram512Auth")
    def reset_sasl_scram512_auth(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSaslScram512Auth", []))

    @builtins.property
    @jsii.member(jsii_name="basicAuthInput")
    def basic_auth_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "basicAuthInput"))

    @builtins.property
    @jsii.member(jsii_name="clientCertificateTlsAuthInput")
    def client_certificate_tls_auth_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clientCertificateTlsAuthInput"))

    @builtins.property
    @jsii.member(jsii_name="saslScram256AuthInput")
    def sasl_scram256_auth_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "saslScram256AuthInput"))

    @builtins.property
    @jsii.member(jsii_name="saslScram512AuthInput")
    def sasl_scram512_auth_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "saslScram512AuthInput"))

    @builtins.property
    @jsii.member(jsii_name="basicAuth")
    def basic_auth(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "basicAuth"))

    @basic_auth.setter
    def basic_auth(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c6ea1c93f8b30c1a799b13dca5c436dba16ef2d46a435b7ead3892c308efa193)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "basicAuth", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clientCertificateTlsAuth")
    def client_certificate_tls_auth(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientCertificateTlsAuth"))

    @client_certificate_tls_auth.setter
    def client_certificate_tls_auth(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e201ae5cf724e274cc4ff2622aab1199b750b659acd4f91056bb03dd917702c6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientCertificateTlsAuth", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="saslScram256Auth")
    def sasl_scram256_auth(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "saslScram256Auth"))

    @sasl_scram256_auth.setter
    def sasl_scram256_auth(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__beaace34d524c54bacdcf234a3865d2343c98f3e8b4dfba4236c0afa24d0dfdb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "saslScram256Auth", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="saslScram512Auth")
    def sasl_scram512_auth(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "saslScram512Auth"))

    @sasl_scram512_auth.setter
    def sasl_scram512_auth(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d40efd6c57a46b7f83f8d91db716a92f02a6d1f04a1a5c498ff8acabf01b4b1e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "saslScram512Auth", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[PipesPipeSourceParametersSelfManagedKafkaParametersCredentials]:
        return typing.cast(typing.Optional[PipesPipeSourceParametersSelfManagedKafkaParametersCredentials], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[PipesPipeSourceParametersSelfManagedKafkaParametersCredentials],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__41dab4353b6254d5f87f291db2a37ed85d1b5bb8d3fc4be7bcd822f737ea404e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class PipesPipeSourceParametersSelfManagedKafkaParametersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.pipesPipe.PipesPipeSourceParametersSelfManagedKafkaParametersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__04693c6e201b25ab65959fcf69c85eee55d23e5b2e1e563c19193998d1c6e79a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putCredentials")
    def put_credentials(
        self,
        *,
        basic_auth: typing.Optional[builtins.str] = None,
        client_certificate_tls_auth: typing.Optional[builtins.str] = None,
        sasl_scram256_auth: typing.Optional[builtins.str] = None,
        sasl_scram512_auth: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param basic_auth: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#basic_auth PipesPipe#basic_auth}.
        :param client_certificate_tls_auth: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#client_certificate_tls_auth PipesPipe#client_certificate_tls_auth}.
        :param sasl_scram256_auth: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#sasl_scram_256_auth PipesPipe#sasl_scram_256_auth}.
        :param sasl_scram512_auth: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#sasl_scram_512_auth PipesPipe#sasl_scram_512_auth}.
        '''
        value = PipesPipeSourceParametersSelfManagedKafkaParametersCredentials(
            basic_auth=basic_auth,
            client_certificate_tls_auth=client_certificate_tls_auth,
            sasl_scram256_auth=sasl_scram256_auth,
            sasl_scram512_auth=sasl_scram512_auth,
        )

        return typing.cast(None, jsii.invoke(self, "putCredentials", [value]))

    @jsii.member(jsii_name="putVpc")
    def put_vpc(
        self,
        *,
        security_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
        subnets: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param security_groups: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#security_groups PipesPipe#security_groups}.
        :param subnets: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#subnets PipesPipe#subnets}.
        '''
        value = PipesPipeSourceParametersSelfManagedKafkaParametersVpc(
            security_groups=security_groups, subnets=subnets
        )

        return typing.cast(None, jsii.invoke(self, "putVpc", [value]))

    @jsii.member(jsii_name="resetAdditionalBootstrapServers")
    def reset_additional_bootstrap_servers(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAdditionalBootstrapServers", []))

    @jsii.member(jsii_name="resetBatchSize")
    def reset_batch_size(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBatchSize", []))

    @jsii.member(jsii_name="resetConsumerGroupId")
    def reset_consumer_group_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConsumerGroupId", []))

    @jsii.member(jsii_name="resetCredentials")
    def reset_credentials(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCredentials", []))

    @jsii.member(jsii_name="resetMaximumBatchingWindowInSeconds")
    def reset_maximum_batching_window_in_seconds(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaximumBatchingWindowInSeconds", []))

    @jsii.member(jsii_name="resetServerRootCaCertificate")
    def reset_server_root_ca_certificate(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetServerRootCaCertificate", []))

    @jsii.member(jsii_name="resetStartingPosition")
    def reset_starting_position(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStartingPosition", []))

    @jsii.member(jsii_name="resetVpc")
    def reset_vpc(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVpc", []))

    @builtins.property
    @jsii.member(jsii_name="credentials")
    def credentials(
        self,
    ) -> PipesPipeSourceParametersSelfManagedKafkaParametersCredentialsOutputReference:
        return typing.cast(PipesPipeSourceParametersSelfManagedKafkaParametersCredentialsOutputReference, jsii.get(self, "credentials"))

    @builtins.property
    @jsii.member(jsii_name="vpc")
    def vpc(
        self,
    ) -> "PipesPipeSourceParametersSelfManagedKafkaParametersVpcOutputReference":
        return typing.cast("PipesPipeSourceParametersSelfManagedKafkaParametersVpcOutputReference", jsii.get(self, "vpc"))

    @builtins.property
    @jsii.member(jsii_name="additionalBootstrapServersInput")
    def additional_bootstrap_servers_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "additionalBootstrapServersInput"))

    @builtins.property
    @jsii.member(jsii_name="batchSizeInput")
    def batch_size_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "batchSizeInput"))

    @builtins.property
    @jsii.member(jsii_name="consumerGroupIdInput")
    def consumer_group_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "consumerGroupIdInput"))

    @builtins.property
    @jsii.member(jsii_name="credentialsInput")
    def credentials_input(
        self,
    ) -> typing.Optional[PipesPipeSourceParametersSelfManagedKafkaParametersCredentials]:
        return typing.cast(typing.Optional[PipesPipeSourceParametersSelfManagedKafkaParametersCredentials], jsii.get(self, "credentialsInput"))

    @builtins.property
    @jsii.member(jsii_name="maximumBatchingWindowInSecondsInput")
    def maximum_batching_window_in_seconds_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maximumBatchingWindowInSecondsInput"))

    @builtins.property
    @jsii.member(jsii_name="serverRootCaCertificateInput")
    def server_root_ca_certificate_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serverRootCaCertificateInput"))

    @builtins.property
    @jsii.member(jsii_name="startingPositionInput")
    def starting_position_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "startingPositionInput"))

    @builtins.property
    @jsii.member(jsii_name="topicNameInput")
    def topic_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "topicNameInput"))

    @builtins.property
    @jsii.member(jsii_name="vpcInput")
    def vpc_input(
        self,
    ) -> typing.Optional["PipesPipeSourceParametersSelfManagedKafkaParametersVpc"]:
        return typing.cast(typing.Optional["PipesPipeSourceParametersSelfManagedKafkaParametersVpc"], jsii.get(self, "vpcInput"))

    @builtins.property
    @jsii.member(jsii_name="additionalBootstrapServers")
    def additional_bootstrap_servers(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "additionalBootstrapServers"))

    @additional_bootstrap_servers.setter
    def additional_bootstrap_servers(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c5197eea7f4283fa2c61ffc74f1c743011037ca0d54ee9fb06074fe3eb90b1a4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "additionalBootstrapServers", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="batchSize")
    def batch_size(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "batchSize"))

    @batch_size.setter
    def batch_size(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c42532397303b99f9fa02a9652bb710c0e1d1231f5c749c384f82060ad96047)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "batchSize", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="consumerGroupId")
    def consumer_group_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "consumerGroupId"))

    @consumer_group_id.setter
    def consumer_group_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7653a290a45ca691857cea8981dc85d019bb72591a1c7fb9e5c19c3f624a937a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "consumerGroupId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maximumBatchingWindowInSeconds")
    def maximum_batching_window_in_seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maximumBatchingWindowInSeconds"))

    @maximum_batching_window_in_seconds.setter
    def maximum_batching_window_in_seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c434acd7e570117dcef5bafcf94f0c026ebb7bdcf3a9243857aed8bc7de369b0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maximumBatchingWindowInSeconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="serverRootCaCertificate")
    def server_root_ca_certificate(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serverRootCaCertificate"))

    @server_root_ca_certificate.setter
    def server_root_ca_certificate(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2b11eeecf5daf0ed710f396f9705e4b3de41fd621ded2683b865c20ecd94329c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serverRootCaCertificate", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="startingPosition")
    def starting_position(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "startingPosition"))

    @starting_position.setter
    def starting_position(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f5319a052a0d9f84e5f77685353d89f88604f26d289a5aafe457c60b8c81d96)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "startingPosition", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="topicName")
    def topic_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "topicName"))

    @topic_name.setter
    def topic_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__20a36831e9845393173d8c5230dd73a99c707e8d90982ffb46f80cebd3a66072)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "topicName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[PipesPipeSourceParametersSelfManagedKafkaParameters]:
        return typing.cast(typing.Optional[PipesPipeSourceParametersSelfManagedKafkaParameters], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[PipesPipeSourceParametersSelfManagedKafkaParameters],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d45460a35c4fb94cc8960415a2a0521185a407b19fb74afbf63609bce77e991f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.pipesPipe.PipesPipeSourceParametersSelfManagedKafkaParametersVpc",
    jsii_struct_bases=[],
    name_mapping={"security_groups": "securityGroups", "subnets": "subnets"},
)
class PipesPipeSourceParametersSelfManagedKafkaParametersVpc:
    def __init__(
        self,
        *,
        security_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
        subnets: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param security_groups: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#security_groups PipesPipe#security_groups}.
        :param subnets: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#subnets PipesPipe#subnets}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc8672296bd558d9765ef7290d74c578eb5265277997f410de61d31e9b212221)
            check_type(argname="argument security_groups", value=security_groups, expected_type=type_hints["security_groups"])
            check_type(argname="argument subnets", value=subnets, expected_type=type_hints["subnets"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if security_groups is not None:
            self._values["security_groups"] = security_groups
        if subnets is not None:
            self._values["subnets"] = subnets

    @builtins.property
    def security_groups(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#security_groups PipesPipe#security_groups}.'''
        result = self._values.get("security_groups")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def subnets(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#subnets PipesPipe#subnets}.'''
        result = self._values.get("subnets")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PipesPipeSourceParametersSelfManagedKafkaParametersVpc(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PipesPipeSourceParametersSelfManagedKafkaParametersVpcOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.pipesPipe.PipesPipeSourceParametersSelfManagedKafkaParametersVpcOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__603c9b9e0f8a85aee969f4757c30595e5fff7196e763f4d398d85679d2b27c6b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetSecurityGroups")
    def reset_security_groups(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSecurityGroups", []))

    @jsii.member(jsii_name="resetSubnets")
    def reset_subnets(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSubnets", []))

    @builtins.property
    @jsii.member(jsii_name="securityGroupsInput")
    def security_groups_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "securityGroupsInput"))

    @builtins.property
    @jsii.member(jsii_name="subnetsInput")
    def subnets_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "subnetsInput"))

    @builtins.property
    @jsii.member(jsii_name="securityGroups")
    def security_groups(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "securityGroups"))

    @security_groups.setter
    def security_groups(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fbdce6eebf05b27f567d403ceb7f84c535e20e8f1503e7c4509ecef54e05e94c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "securityGroups", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="subnets")
    def subnets(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "subnets"))

    @subnets.setter
    def subnets(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ea567fde920ae2a26e6803c133cecea2c9da82b544c31d441a42ded71ab84e4b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subnets", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[PipesPipeSourceParametersSelfManagedKafkaParametersVpc]:
        return typing.cast(typing.Optional[PipesPipeSourceParametersSelfManagedKafkaParametersVpc], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[PipesPipeSourceParametersSelfManagedKafkaParametersVpc],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__455f05b907bf0105fb24fa938d84aad5144ed5ebf1b6fb67f1963685d36e1771)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.pipesPipe.PipesPipeSourceParametersSqsQueueParameters",
    jsii_struct_bases=[],
    name_mapping={
        "batch_size": "batchSize",
        "maximum_batching_window_in_seconds": "maximumBatchingWindowInSeconds",
    },
)
class PipesPipeSourceParametersSqsQueueParameters:
    def __init__(
        self,
        *,
        batch_size: typing.Optional[jsii.Number] = None,
        maximum_batching_window_in_seconds: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param batch_size: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#batch_size PipesPipe#batch_size}.
        :param maximum_batching_window_in_seconds: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#maximum_batching_window_in_seconds PipesPipe#maximum_batching_window_in_seconds}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c80bdde1bb2a2a7f80e049721cf3a1cf90ab695718d099b3aafa9eaa9d9c8e96)
            check_type(argname="argument batch_size", value=batch_size, expected_type=type_hints["batch_size"])
            check_type(argname="argument maximum_batching_window_in_seconds", value=maximum_batching_window_in_seconds, expected_type=type_hints["maximum_batching_window_in_seconds"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if batch_size is not None:
            self._values["batch_size"] = batch_size
        if maximum_batching_window_in_seconds is not None:
            self._values["maximum_batching_window_in_seconds"] = maximum_batching_window_in_seconds

    @builtins.property
    def batch_size(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#batch_size PipesPipe#batch_size}.'''
        result = self._values.get("batch_size")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def maximum_batching_window_in_seconds(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#maximum_batching_window_in_seconds PipesPipe#maximum_batching_window_in_seconds}.'''
        result = self._values.get("maximum_batching_window_in_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PipesPipeSourceParametersSqsQueueParameters(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PipesPipeSourceParametersSqsQueueParametersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.pipesPipe.PipesPipeSourceParametersSqsQueueParametersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__53a2dab28a324542f6e399d4f14340c296f64aba15d3798ad921156b83fde2ce)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetBatchSize")
    def reset_batch_size(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBatchSize", []))

    @jsii.member(jsii_name="resetMaximumBatchingWindowInSeconds")
    def reset_maximum_batching_window_in_seconds(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaximumBatchingWindowInSeconds", []))

    @builtins.property
    @jsii.member(jsii_name="batchSizeInput")
    def batch_size_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "batchSizeInput"))

    @builtins.property
    @jsii.member(jsii_name="maximumBatchingWindowInSecondsInput")
    def maximum_batching_window_in_seconds_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maximumBatchingWindowInSecondsInput"))

    @builtins.property
    @jsii.member(jsii_name="batchSize")
    def batch_size(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "batchSize"))

    @batch_size.setter
    def batch_size(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3dde29e16049cfc79a231784535e5c138a2fdc8d719237634b652a22500f0583)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "batchSize", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maximumBatchingWindowInSeconds")
    def maximum_batching_window_in_seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maximumBatchingWindowInSeconds"))

    @maximum_batching_window_in_seconds.setter
    def maximum_batching_window_in_seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5d4ccc392189585135aa591ea6fba9b5c2458b7a43363e8ed9e454d0e55d5ac3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maximumBatchingWindowInSeconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[PipesPipeSourceParametersSqsQueueParameters]:
        return typing.cast(typing.Optional[PipesPipeSourceParametersSqsQueueParameters], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[PipesPipeSourceParametersSqsQueueParameters],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0cbde1d4f5968864cc5e798f3d7ee6f421754a146c1f458f827b513ffb9e4cd4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.pipesPipe.PipesPipeTargetParameters",
    jsii_struct_bases=[],
    name_mapping={
        "batch_job_parameters": "batchJobParameters",
        "cloudwatch_logs_parameters": "cloudwatchLogsParameters",
        "ecs_task_parameters": "ecsTaskParameters",
        "eventbridge_event_bus_parameters": "eventbridgeEventBusParameters",
        "http_parameters": "httpParameters",
        "input_template": "inputTemplate",
        "kinesis_stream_parameters": "kinesisStreamParameters",
        "lambda_function_parameters": "lambdaFunctionParameters",
        "redshift_data_parameters": "redshiftDataParameters",
        "sagemaker_pipeline_parameters": "sagemakerPipelineParameters",
        "sqs_queue_parameters": "sqsQueueParameters",
        "step_function_state_machine_parameters": "stepFunctionStateMachineParameters",
    },
)
class PipesPipeTargetParameters:
    def __init__(
        self,
        *,
        batch_job_parameters: typing.Optional[typing.Union["PipesPipeTargetParametersBatchJobParameters", typing.Dict[builtins.str, typing.Any]]] = None,
        cloudwatch_logs_parameters: typing.Optional[typing.Union["PipesPipeTargetParametersCloudwatchLogsParameters", typing.Dict[builtins.str, typing.Any]]] = None,
        ecs_task_parameters: typing.Optional[typing.Union["PipesPipeTargetParametersEcsTaskParameters", typing.Dict[builtins.str, typing.Any]]] = None,
        eventbridge_event_bus_parameters: typing.Optional[typing.Union["PipesPipeTargetParametersEventbridgeEventBusParameters", typing.Dict[builtins.str, typing.Any]]] = None,
        http_parameters: typing.Optional[typing.Union["PipesPipeTargetParametersHttpParameters", typing.Dict[builtins.str, typing.Any]]] = None,
        input_template: typing.Optional[builtins.str] = None,
        kinesis_stream_parameters: typing.Optional[typing.Union["PipesPipeTargetParametersKinesisStreamParameters", typing.Dict[builtins.str, typing.Any]]] = None,
        lambda_function_parameters: typing.Optional[typing.Union["PipesPipeTargetParametersLambdaFunctionParameters", typing.Dict[builtins.str, typing.Any]]] = None,
        redshift_data_parameters: typing.Optional[typing.Union["PipesPipeTargetParametersRedshiftDataParameters", typing.Dict[builtins.str, typing.Any]]] = None,
        sagemaker_pipeline_parameters: typing.Optional[typing.Union["PipesPipeTargetParametersSagemakerPipelineParameters", typing.Dict[builtins.str, typing.Any]]] = None,
        sqs_queue_parameters: typing.Optional[typing.Union["PipesPipeTargetParametersSqsQueueParameters", typing.Dict[builtins.str, typing.Any]]] = None,
        step_function_state_machine_parameters: typing.Optional[typing.Union["PipesPipeTargetParametersStepFunctionStateMachineParameters", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param batch_job_parameters: batch_job_parameters block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#batch_job_parameters PipesPipe#batch_job_parameters}
        :param cloudwatch_logs_parameters: cloudwatch_logs_parameters block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#cloudwatch_logs_parameters PipesPipe#cloudwatch_logs_parameters}
        :param ecs_task_parameters: ecs_task_parameters block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#ecs_task_parameters PipesPipe#ecs_task_parameters}
        :param eventbridge_event_bus_parameters: eventbridge_event_bus_parameters block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#eventbridge_event_bus_parameters PipesPipe#eventbridge_event_bus_parameters}
        :param http_parameters: http_parameters block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#http_parameters PipesPipe#http_parameters}
        :param input_template: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#input_template PipesPipe#input_template}.
        :param kinesis_stream_parameters: kinesis_stream_parameters block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#kinesis_stream_parameters PipesPipe#kinesis_stream_parameters}
        :param lambda_function_parameters: lambda_function_parameters block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#lambda_function_parameters PipesPipe#lambda_function_parameters}
        :param redshift_data_parameters: redshift_data_parameters block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#redshift_data_parameters PipesPipe#redshift_data_parameters}
        :param sagemaker_pipeline_parameters: sagemaker_pipeline_parameters block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#sagemaker_pipeline_parameters PipesPipe#sagemaker_pipeline_parameters}
        :param sqs_queue_parameters: sqs_queue_parameters block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#sqs_queue_parameters PipesPipe#sqs_queue_parameters}
        :param step_function_state_machine_parameters: step_function_state_machine_parameters block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#step_function_state_machine_parameters PipesPipe#step_function_state_machine_parameters}
        '''
        if isinstance(batch_job_parameters, dict):
            batch_job_parameters = PipesPipeTargetParametersBatchJobParameters(**batch_job_parameters)
        if isinstance(cloudwatch_logs_parameters, dict):
            cloudwatch_logs_parameters = PipesPipeTargetParametersCloudwatchLogsParameters(**cloudwatch_logs_parameters)
        if isinstance(ecs_task_parameters, dict):
            ecs_task_parameters = PipesPipeTargetParametersEcsTaskParameters(**ecs_task_parameters)
        if isinstance(eventbridge_event_bus_parameters, dict):
            eventbridge_event_bus_parameters = PipesPipeTargetParametersEventbridgeEventBusParameters(**eventbridge_event_bus_parameters)
        if isinstance(http_parameters, dict):
            http_parameters = PipesPipeTargetParametersHttpParameters(**http_parameters)
        if isinstance(kinesis_stream_parameters, dict):
            kinesis_stream_parameters = PipesPipeTargetParametersKinesisStreamParameters(**kinesis_stream_parameters)
        if isinstance(lambda_function_parameters, dict):
            lambda_function_parameters = PipesPipeTargetParametersLambdaFunctionParameters(**lambda_function_parameters)
        if isinstance(redshift_data_parameters, dict):
            redshift_data_parameters = PipesPipeTargetParametersRedshiftDataParameters(**redshift_data_parameters)
        if isinstance(sagemaker_pipeline_parameters, dict):
            sagemaker_pipeline_parameters = PipesPipeTargetParametersSagemakerPipelineParameters(**sagemaker_pipeline_parameters)
        if isinstance(sqs_queue_parameters, dict):
            sqs_queue_parameters = PipesPipeTargetParametersSqsQueueParameters(**sqs_queue_parameters)
        if isinstance(step_function_state_machine_parameters, dict):
            step_function_state_machine_parameters = PipesPipeTargetParametersStepFunctionStateMachineParameters(**step_function_state_machine_parameters)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e25b60649e0a580dd3eb27efb3577835054a1013066fe69c7405ee9b0d17f6a2)
            check_type(argname="argument batch_job_parameters", value=batch_job_parameters, expected_type=type_hints["batch_job_parameters"])
            check_type(argname="argument cloudwatch_logs_parameters", value=cloudwatch_logs_parameters, expected_type=type_hints["cloudwatch_logs_parameters"])
            check_type(argname="argument ecs_task_parameters", value=ecs_task_parameters, expected_type=type_hints["ecs_task_parameters"])
            check_type(argname="argument eventbridge_event_bus_parameters", value=eventbridge_event_bus_parameters, expected_type=type_hints["eventbridge_event_bus_parameters"])
            check_type(argname="argument http_parameters", value=http_parameters, expected_type=type_hints["http_parameters"])
            check_type(argname="argument input_template", value=input_template, expected_type=type_hints["input_template"])
            check_type(argname="argument kinesis_stream_parameters", value=kinesis_stream_parameters, expected_type=type_hints["kinesis_stream_parameters"])
            check_type(argname="argument lambda_function_parameters", value=lambda_function_parameters, expected_type=type_hints["lambda_function_parameters"])
            check_type(argname="argument redshift_data_parameters", value=redshift_data_parameters, expected_type=type_hints["redshift_data_parameters"])
            check_type(argname="argument sagemaker_pipeline_parameters", value=sagemaker_pipeline_parameters, expected_type=type_hints["sagemaker_pipeline_parameters"])
            check_type(argname="argument sqs_queue_parameters", value=sqs_queue_parameters, expected_type=type_hints["sqs_queue_parameters"])
            check_type(argname="argument step_function_state_machine_parameters", value=step_function_state_machine_parameters, expected_type=type_hints["step_function_state_machine_parameters"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if batch_job_parameters is not None:
            self._values["batch_job_parameters"] = batch_job_parameters
        if cloudwatch_logs_parameters is not None:
            self._values["cloudwatch_logs_parameters"] = cloudwatch_logs_parameters
        if ecs_task_parameters is not None:
            self._values["ecs_task_parameters"] = ecs_task_parameters
        if eventbridge_event_bus_parameters is not None:
            self._values["eventbridge_event_bus_parameters"] = eventbridge_event_bus_parameters
        if http_parameters is not None:
            self._values["http_parameters"] = http_parameters
        if input_template is not None:
            self._values["input_template"] = input_template
        if kinesis_stream_parameters is not None:
            self._values["kinesis_stream_parameters"] = kinesis_stream_parameters
        if lambda_function_parameters is not None:
            self._values["lambda_function_parameters"] = lambda_function_parameters
        if redshift_data_parameters is not None:
            self._values["redshift_data_parameters"] = redshift_data_parameters
        if sagemaker_pipeline_parameters is not None:
            self._values["sagemaker_pipeline_parameters"] = sagemaker_pipeline_parameters
        if sqs_queue_parameters is not None:
            self._values["sqs_queue_parameters"] = sqs_queue_parameters
        if step_function_state_machine_parameters is not None:
            self._values["step_function_state_machine_parameters"] = step_function_state_machine_parameters

    @builtins.property
    def batch_job_parameters(
        self,
    ) -> typing.Optional["PipesPipeTargetParametersBatchJobParameters"]:
        '''batch_job_parameters block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#batch_job_parameters PipesPipe#batch_job_parameters}
        '''
        result = self._values.get("batch_job_parameters")
        return typing.cast(typing.Optional["PipesPipeTargetParametersBatchJobParameters"], result)

    @builtins.property
    def cloudwatch_logs_parameters(
        self,
    ) -> typing.Optional["PipesPipeTargetParametersCloudwatchLogsParameters"]:
        '''cloudwatch_logs_parameters block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#cloudwatch_logs_parameters PipesPipe#cloudwatch_logs_parameters}
        '''
        result = self._values.get("cloudwatch_logs_parameters")
        return typing.cast(typing.Optional["PipesPipeTargetParametersCloudwatchLogsParameters"], result)

    @builtins.property
    def ecs_task_parameters(
        self,
    ) -> typing.Optional["PipesPipeTargetParametersEcsTaskParameters"]:
        '''ecs_task_parameters block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#ecs_task_parameters PipesPipe#ecs_task_parameters}
        '''
        result = self._values.get("ecs_task_parameters")
        return typing.cast(typing.Optional["PipesPipeTargetParametersEcsTaskParameters"], result)

    @builtins.property
    def eventbridge_event_bus_parameters(
        self,
    ) -> typing.Optional["PipesPipeTargetParametersEventbridgeEventBusParameters"]:
        '''eventbridge_event_bus_parameters block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#eventbridge_event_bus_parameters PipesPipe#eventbridge_event_bus_parameters}
        '''
        result = self._values.get("eventbridge_event_bus_parameters")
        return typing.cast(typing.Optional["PipesPipeTargetParametersEventbridgeEventBusParameters"], result)

    @builtins.property
    def http_parameters(
        self,
    ) -> typing.Optional["PipesPipeTargetParametersHttpParameters"]:
        '''http_parameters block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#http_parameters PipesPipe#http_parameters}
        '''
        result = self._values.get("http_parameters")
        return typing.cast(typing.Optional["PipesPipeTargetParametersHttpParameters"], result)

    @builtins.property
    def input_template(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#input_template PipesPipe#input_template}.'''
        result = self._values.get("input_template")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kinesis_stream_parameters(
        self,
    ) -> typing.Optional["PipesPipeTargetParametersKinesisStreamParameters"]:
        '''kinesis_stream_parameters block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#kinesis_stream_parameters PipesPipe#kinesis_stream_parameters}
        '''
        result = self._values.get("kinesis_stream_parameters")
        return typing.cast(typing.Optional["PipesPipeTargetParametersKinesisStreamParameters"], result)

    @builtins.property
    def lambda_function_parameters(
        self,
    ) -> typing.Optional["PipesPipeTargetParametersLambdaFunctionParameters"]:
        '''lambda_function_parameters block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#lambda_function_parameters PipesPipe#lambda_function_parameters}
        '''
        result = self._values.get("lambda_function_parameters")
        return typing.cast(typing.Optional["PipesPipeTargetParametersLambdaFunctionParameters"], result)

    @builtins.property
    def redshift_data_parameters(
        self,
    ) -> typing.Optional["PipesPipeTargetParametersRedshiftDataParameters"]:
        '''redshift_data_parameters block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#redshift_data_parameters PipesPipe#redshift_data_parameters}
        '''
        result = self._values.get("redshift_data_parameters")
        return typing.cast(typing.Optional["PipesPipeTargetParametersRedshiftDataParameters"], result)

    @builtins.property
    def sagemaker_pipeline_parameters(
        self,
    ) -> typing.Optional["PipesPipeTargetParametersSagemakerPipelineParameters"]:
        '''sagemaker_pipeline_parameters block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#sagemaker_pipeline_parameters PipesPipe#sagemaker_pipeline_parameters}
        '''
        result = self._values.get("sagemaker_pipeline_parameters")
        return typing.cast(typing.Optional["PipesPipeTargetParametersSagemakerPipelineParameters"], result)

    @builtins.property
    def sqs_queue_parameters(
        self,
    ) -> typing.Optional["PipesPipeTargetParametersSqsQueueParameters"]:
        '''sqs_queue_parameters block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#sqs_queue_parameters PipesPipe#sqs_queue_parameters}
        '''
        result = self._values.get("sqs_queue_parameters")
        return typing.cast(typing.Optional["PipesPipeTargetParametersSqsQueueParameters"], result)

    @builtins.property
    def step_function_state_machine_parameters(
        self,
    ) -> typing.Optional["PipesPipeTargetParametersStepFunctionStateMachineParameters"]:
        '''step_function_state_machine_parameters block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#step_function_state_machine_parameters PipesPipe#step_function_state_machine_parameters}
        '''
        result = self._values.get("step_function_state_machine_parameters")
        return typing.cast(typing.Optional["PipesPipeTargetParametersStepFunctionStateMachineParameters"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PipesPipeTargetParameters(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.pipesPipe.PipesPipeTargetParametersBatchJobParameters",
    jsii_struct_bases=[],
    name_mapping={
        "job_definition": "jobDefinition",
        "job_name": "jobName",
        "array_properties": "arrayProperties",
        "container_overrides": "containerOverrides",
        "depends_on": "dependsOn",
        "parameters": "parameters",
        "retry_strategy": "retryStrategy",
    },
)
class PipesPipeTargetParametersBatchJobParameters:
    def __init__(
        self,
        *,
        job_definition: builtins.str,
        job_name: builtins.str,
        array_properties: typing.Optional[typing.Union["PipesPipeTargetParametersBatchJobParametersArrayProperties", typing.Dict[builtins.str, typing.Any]]] = None,
        container_overrides: typing.Optional[typing.Union["PipesPipeTargetParametersBatchJobParametersContainerOverrides", typing.Dict[builtins.str, typing.Any]]] = None,
        depends_on: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["PipesPipeTargetParametersBatchJobParametersDependsOn", typing.Dict[builtins.str, typing.Any]]]]] = None,
        parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        retry_strategy: typing.Optional[typing.Union["PipesPipeTargetParametersBatchJobParametersRetryStrategy", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param job_definition: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#job_definition PipesPipe#job_definition}.
        :param job_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#job_name PipesPipe#job_name}.
        :param array_properties: array_properties block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#array_properties PipesPipe#array_properties}
        :param container_overrides: container_overrides block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#container_overrides PipesPipe#container_overrides}
        :param depends_on: depends_on block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#depends_on PipesPipe#depends_on}
        :param parameters: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#parameters PipesPipe#parameters}.
        :param retry_strategy: retry_strategy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#retry_strategy PipesPipe#retry_strategy}
        '''
        if isinstance(array_properties, dict):
            array_properties = PipesPipeTargetParametersBatchJobParametersArrayProperties(**array_properties)
        if isinstance(container_overrides, dict):
            container_overrides = PipesPipeTargetParametersBatchJobParametersContainerOverrides(**container_overrides)
        if isinstance(retry_strategy, dict):
            retry_strategy = PipesPipeTargetParametersBatchJobParametersRetryStrategy(**retry_strategy)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__852eab64fec2c126813aee1d8abc1b4f3b5297f517874e4dfc13c3aa71a0a06d)
            check_type(argname="argument job_definition", value=job_definition, expected_type=type_hints["job_definition"])
            check_type(argname="argument job_name", value=job_name, expected_type=type_hints["job_name"])
            check_type(argname="argument array_properties", value=array_properties, expected_type=type_hints["array_properties"])
            check_type(argname="argument container_overrides", value=container_overrides, expected_type=type_hints["container_overrides"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument parameters", value=parameters, expected_type=type_hints["parameters"])
            check_type(argname="argument retry_strategy", value=retry_strategy, expected_type=type_hints["retry_strategy"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "job_definition": job_definition,
            "job_name": job_name,
        }
        if array_properties is not None:
            self._values["array_properties"] = array_properties
        if container_overrides is not None:
            self._values["container_overrides"] = container_overrides
        if depends_on is not None:
            self._values["depends_on"] = depends_on
        if parameters is not None:
            self._values["parameters"] = parameters
        if retry_strategy is not None:
            self._values["retry_strategy"] = retry_strategy

    @builtins.property
    def job_definition(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#job_definition PipesPipe#job_definition}.'''
        result = self._values.get("job_definition")
        assert result is not None, "Required property 'job_definition' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def job_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#job_name PipesPipe#job_name}.'''
        result = self._values.get("job_name")
        assert result is not None, "Required property 'job_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def array_properties(
        self,
    ) -> typing.Optional["PipesPipeTargetParametersBatchJobParametersArrayProperties"]:
        '''array_properties block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#array_properties PipesPipe#array_properties}
        '''
        result = self._values.get("array_properties")
        return typing.cast(typing.Optional["PipesPipeTargetParametersBatchJobParametersArrayProperties"], result)

    @builtins.property
    def container_overrides(
        self,
    ) -> typing.Optional["PipesPipeTargetParametersBatchJobParametersContainerOverrides"]:
        '''container_overrides block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#container_overrides PipesPipe#container_overrides}
        '''
        result = self._values.get("container_overrides")
        return typing.cast(typing.Optional["PipesPipeTargetParametersBatchJobParametersContainerOverrides"], result)

    @builtins.property
    def depends_on(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["PipesPipeTargetParametersBatchJobParametersDependsOn"]]]:
        '''depends_on block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#depends_on PipesPipe#depends_on}
        '''
        result = self._values.get("depends_on")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["PipesPipeTargetParametersBatchJobParametersDependsOn"]]], result)

    @builtins.property
    def parameters(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#parameters PipesPipe#parameters}.'''
        result = self._values.get("parameters")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def retry_strategy(
        self,
    ) -> typing.Optional["PipesPipeTargetParametersBatchJobParametersRetryStrategy"]:
        '''retry_strategy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#retry_strategy PipesPipe#retry_strategy}
        '''
        result = self._values.get("retry_strategy")
        return typing.cast(typing.Optional["PipesPipeTargetParametersBatchJobParametersRetryStrategy"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PipesPipeTargetParametersBatchJobParameters(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.pipesPipe.PipesPipeTargetParametersBatchJobParametersArrayProperties",
    jsii_struct_bases=[],
    name_mapping={"size": "size"},
)
class PipesPipeTargetParametersBatchJobParametersArrayProperties:
    def __init__(self, *, size: typing.Optional[jsii.Number] = None) -> None:
        '''
        :param size: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#size PipesPipe#size}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4ddd3dc657bcd23a41dc39c3b8ebb70519f9663195f910615c41328be9439bf5)
            check_type(argname="argument size", value=size, expected_type=type_hints["size"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if size is not None:
            self._values["size"] = size

    @builtins.property
    def size(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#size PipesPipe#size}.'''
        result = self._values.get("size")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PipesPipeTargetParametersBatchJobParametersArrayProperties(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PipesPipeTargetParametersBatchJobParametersArrayPropertiesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.pipesPipe.PipesPipeTargetParametersBatchJobParametersArrayPropertiesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__dc91d7eefad5f8654698ad31d47dd6d1b706a23bdb3750bb38d933715d4ffe09)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetSize")
    def reset_size(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSize", []))

    @builtins.property
    @jsii.member(jsii_name="sizeInput")
    def size_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "sizeInput"))

    @builtins.property
    @jsii.member(jsii_name="size")
    def size(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "size"))

    @size.setter
    def size(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b135119a85085af82b147f9275b66c172a06282cb94a0e8bb3edfc5d56475499)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "size", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[PipesPipeTargetParametersBatchJobParametersArrayProperties]:
        return typing.cast(typing.Optional[PipesPipeTargetParametersBatchJobParametersArrayProperties], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[PipesPipeTargetParametersBatchJobParametersArrayProperties],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c093b53cfb92179f3952148e18124f6d508b6c47f29cd8b03f056719bde93665)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.pipesPipe.PipesPipeTargetParametersBatchJobParametersContainerOverrides",
    jsii_struct_bases=[],
    name_mapping={
        "command": "command",
        "environment": "environment",
        "instance_type": "instanceType",
        "resource_requirement": "resourceRequirement",
    },
)
class PipesPipeTargetParametersBatchJobParametersContainerOverrides:
    def __init__(
        self,
        *,
        command: typing.Optional[typing.Sequence[builtins.str]] = None,
        environment: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["PipesPipeTargetParametersBatchJobParametersContainerOverridesEnvironment", typing.Dict[builtins.str, typing.Any]]]]] = None,
        instance_type: typing.Optional[builtins.str] = None,
        resource_requirement: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["PipesPipeTargetParametersBatchJobParametersContainerOverridesResourceRequirement", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param command: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#command PipesPipe#command}.
        :param environment: environment block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#environment PipesPipe#environment}
        :param instance_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#instance_type PipesPipe#instance_type}.
        :param resource_requirement: resource_requirement block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#resource_requirement PipesPipe#resource_requirement}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f1ac170bf1ee0e30a17909db976c096aa4ef5ec06543d76fb575e8b66a50d50e)
            check_type(argname="argument command", value=command, expected_type=type_hints["command"])
            check_type(argname="argument environment", value=environment, expected_type=type_hints["environment"])
            check_type(argname="argument instance_type", value=instance_type, expected_type=type_hints["instance_type"])
            check_type(argname="argument resource_requirement", value=resource_requirement, expected_type=type_hints["resource_requirement"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if command is not None:
            self._values["command"] = command
        if environment is not None:
            self._values["environment"] = environment
        if instance_type is not None:
            self._values["instance_type"] = instance_type
        if resource_requirement is not None:
            self._values["resource_requirement"] = resource_requirement

    @builtins.property
    def command(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#command PipesPipe#command}.'''
        result = self._values.get("command")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def environment(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["PipesPipeTargetParametersBatchJobParametersContainerOverridesEnvironment"]]]:
        '''environment block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#environment PipesPipe#environment}
        '''
        result = self._values.get("environment")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["PipesPipeTargetParametersBatchJobParametersContainerOverridesEnvironment"]]], result)

    @builtins.property
    def instance_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#instance_type PipesPipe#instance_type}.'''
        result = self._values.get("instance_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def resource_requirement(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["PipesPipeTargetParametersBatchJobParametersContainerOverridesResourceRequirement"]]]:
        '''resource_requirement block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#resource_requirement PipesPipe#resource_requirement}
        '''
        result = self._values.get("resource_requirement")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["PipesPipeTargetParametersBatchJobParametersContainerOverridesResourceRequirement"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PipesPipeTargetParametersBatchJobParametersContainerOverrides(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.pipesPipe.PipesPipeTargetParametersBatchJobParametersContainerOverridesEnvironment",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "value": "value"},
)
class PipesPipeTargetParametersBatchJobParametersContainerOverridesEnvironment:
    def __init__(
        self,
        *,
        name: typing.Optional[builtins.str] = None,
        value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#name PipesPipe#name}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#value PipesPipe#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d5e4dda516209273e910ba897162e255e6a562b0eefca3d8eefe73d2bc2c9ff)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if name is not None:
            self._values["name"] = name
        if value is not None:
            self._values["value"] = value

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#name PipesPipe#name}.'''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def value(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#value PipesPipe#value}.'''
        result = self._values.get("value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PipesPipeTargetParametersBatchJobParametersContainerOverridesEnvironment(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PipesPipeTargetParametersBatchJobParametersContainerOverridesEnvironmentList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.pipesPipe.PipesPipeTargetParametersBatchJobParametersContainerOverridesEnvironmentList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fcbb2d2da53979281a93f2220c9e6b969e8ff65693dc973837c0c10caeb5e4de)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "PipesPipeTargetParametersBatchJobParametersContainerOverridesEnvironmentOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f3dd3e4d426dd7dcd055c43cba2a80f56ff6998f9eb3fd97a15a562a7cdb4811)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("PipesPipeTargetParametersBatchJobParametersContainerOverridesEnvironmentOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3f70d7f6576dfc8f317e60f2424142fff37f10d7775a68fe2f7eef8f03ce72ba)
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
            type_hints = typing.get_type_hints(_typecheckingstub__be597ebd8a92bb25b963c7f33489684197192f3c7902b6dba1698fc60a047226)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a5966175abcd519c2017d8a2bda68893af16b9453b651c75150c61e9b8d7aad5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PipesPipeTargetParametersBatchJobParametersContainerOverridesEnvironment]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PipesPipeTargetParametersBatchJobParametersContainerOverridesEnvironment]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PipesPipeTargetParametersBatchJobParametersContainerOverridesEnvironment]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__db616837430933b851583c19c4adfeaec98a2a61c0d9dafd23371e473f147fd0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class PipesPipeTargetParametersBatchJobParametersContainerOverridesEnvironmentOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.pipesPipe.PipesPipeTargetParametersBatchJobParametersContainerOverridesEnvironmentOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5b8260b1f503c926056e2f9a091e4c8cf5caa1f37a8bab1dbf6cd9e1f6ac8192)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @jsii.member(jsii_name="resetValue")
    def reset_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetValue", []))

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
            type_hints = typing.get_type_hints(_typecheckingstub__ff44678ef7b9c4d6d73403852ecae9d5afa13b05edfb1f8f3887e72eddbb6aec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__115bb74add64a265cee9f499b7f746a26e731371a82f8c0fb5bd20294aa94919)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PipesPipeTargetParametersBatchJobParametersContainerOverridesEnvironment]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PipesPipeTargetParametersBatchJobParametersContainerOverridesEnvironment]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PipesPipeTargetParametersBatchJobParametersContainerOverridesEnvironment]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6eeb97217bef371fed0781235bce08f22a7f3937dd93b7c7a28ff050f19f7732)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class PipesPipeTargetParametersBatchJobParametersContainerOverridesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.pipesPipe.PipesPipeTargetParametersBatchJobParametersContainerOverridesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7bd758ca0e235463bebd2f207c36d3f9f64584207c0edb3713ef1a59abdc140f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putEnvironment")
    def put_environment(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[PipesPipeTargetParametersBatchJobParametersContainerOverridesEnvironment, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__96302104eb4a06db2bc910ae17e3f1ecf836ea458a7891f01fa2f1dd236a8817)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putEnvironment", [value]))

    @jsii.member(jsii_name="putResourceRequirement")
    def put_resource_requirement(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["PipesPipeTargetParametersBatchJobParametersContainerOverridesResourceRequirement", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__65a8d07ec52b1d38959511dd90d0489fae27f8dc38bfea7894d115e082e146b8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putResourceRequirement", [value]))

    @jsii.member(jsii_name="resetCommand")
    def reset_command(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCommand", []))

    @jsii.member(jsii_name="resetEnvironment")
    def reset_environment(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnvironment", []))

    @jsii.member(jsii_name="resetInstanceType")
    def reset_instance_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInstanceType", []))

    @jsii.member(jsii_name="resetResourceRequirement")
    def reset_resource_requirement(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetResourceRequirement", []))

    @builtins.property
    @jsii.member(jsii_name="environment")
    def environment(
        self,
    ) -> PipesPipeTargetParametersBatchJobParametersContainerOverridesEnvironmentList:
        return typing.cast(PipesPipeTargetParametersBatchJobParametersContainerOverridesEnvironmentList, jsii.get(self, "environment"))

    @builtins.property
    @jsii.member(jsii_name="resourceRequirement")
    def resource_requirement(
        self,
    ) -> "PipesPipeTargetParametersBatchJobParametersContainerOverridesResourceRequirementList":
        return typing.cast("PipesPipeTargetParametersBatchJobParametersContainerOverridesResourceRequirementList", jsii.get(self, "resourceRequirement"))

    @builtins.property
    @jsii.member(jsii_name="commandInput")
    def command_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "commandInput"))

    @builtins.property
    @jsii.member(jsii_name="environmentInput")
    def environment_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PipesPipeTargetParametersBatchJobParametersContainerOverridesEnvironment]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PipesPipeTargetParametersBatchJobParametersContainerOverridesEnvironment]]], jsii.get(self, "environmentInput"))

    @builtins.property
    @jsii.member(jsii_name="instanceTypeInput")
    def instance_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "instanceTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceRequirementInput")
    def resource_requirement_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["PipesPipeTargetParametersBatchJobParametersContainerOverridesResourceRequirement"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["PipesPipeTargetParametersBatchJobParametersContainerOverridesResourceRequirement"]]], jsii.get(self, "resourceRequirementInput"))

    @builtins.property
    @jsii.member(jsii_name="command")
    def command(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "command"))

    @command.setter
    def command(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f8bd4c9374f367974f47694c11124d465e73c2ad90bf861321f1ca301d10147f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "command", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="instanceType")
    def instance_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "instanceType"))

    @instance_type.setter
    def instance_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bfd2e06abc5f828bf6e5108f16406ef6ab2d8cecce02f5dcc958648a12fd8484)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "instanceType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[PipesPipeTargetParametersBatchJobParametersContainerOverrides]:
        return typing.cast(typing.Optional[PipesPipeTargetParametersBatchJobParametersContainerOverrides], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[PipesPipeTargetParametersBatchJobParametersContainerOverrides],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e7861f2df4c9f5b3698c1410fefc3934b16ae6fe52f1a3b9e8bb3790b28c491e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.pipesPipe.PipesPipeTargetParametersBatchJobParametersContainerOverridesResourceRequirement",
    jsii_struct_bases=[],
    name_mapping={"type": "type", "value": "value"},
)
class PipesPipeTargetParametersBatchJobParametersContainerOverridesResourceRequirement:
    def __init__(self, *, type: builtins.str, value: builtins.str) -> None:
        '''
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#type PipesPipe#type}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#value PipesPipe#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf041b0b059d02605f317b1f2d7c3813fb43bc95f08f02bfc3b811b49d5d586b)
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "type": type,
            "value": value,
        }

    @builtins.property
    def type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#type PipesPipe#type}.'''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#value PipesPipe#value}.'''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PipesPipeTargetParametersBatchJobParametersContainerOverridesResourceRequirement(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PipesPipeTargetParametersBatchJobParametersContainerOverridesResourceRequirementList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.pipesPipe.PipesPipeTargetParametersBatchJobParametersContainerOverridesResourceRequirementList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__414af0d908e39dd9eeb54b10f4cab97f3cad59d00a12cccf4eca36389b3579f8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "PipesPipeTargetParametersBatchJobParametersContainerOverridesResourceRequirementOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__82751e293af62a3c00f409c0de80515cc49c25774b5b6659be354cf1716154f0)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("PipesPipeTargetParametersBatchJobParametersContainerOverridesResourceRequirementOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__825f98a619d521338469de7c14e97f1fb290b4e1510acf1d1fd727fc0e4c7255)
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
            type_hints = typing.get_type_hints(_typecheckingstub__cea84ab65eaf711b470268c6164d3fa3f5a40bcbc51348cf9fa8c02e43b513bd)
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
            type_hints = typing.get_type_hints(_typecheckingstub__76e5db6070d0a96ec8c910618cd9584fde80d4f92568ca96a9482202af6423d5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PipesPipeTargetParametersBatchJobParametersContainerOverridesResourceRequirement]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PipesPipeTargetParametersBatchJobParametersContainerOverridesResourceRequirement]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PipesPipeTargetParametersBatchJobParametersContainerOverridesResourceRequirement]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bce43beacff946a0a16448aec9de8e5a4b1a1ec3173e45c32b992ba5af8bd12b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class PipesPipeTargetParametersBatchJobParametersContainerOverridesResourceRequirementOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.pipesPipe.PipesPipeTargetParametersBatchJobParametersContainerOverridesResourceRequirementOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a0cae1b4d00b66e28eaee70d85e47bd4dc6fe76c9b846e8abf706868b5f4f7d7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d9a98168740dee55eb4c96828085b9dda21a82a26ddca87278c013643d7e709b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__17d8e59539cd6e8e8b23907862aa0fedd7c7fb2dda5595f2ea78aef486cf0506)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PipesPipeTargetParametersBatchJobParametersContainerOverridesResourceRequirement]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PipesPipeTargetParametersBatchJobParametersContainerOverridesResourceRequirement]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PipesPipeTargetParametersBatchJobParametersContainerOverridesResourceRequirement]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f159057384c3884758da79a99e6e88aef6f7a27f4a146d08a9fa10345688c25)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.pipesPipe.PipesPipeTargetParametersBatchJobParametersDependsOn",
    jsii_struct_bases=[],
    name_mapping={"job_id": "jobId", "type": "type"},
)
class PipesPipeTargetParametersBatchJobParametersDependsOn:
    def __init__(
        self,
        *,
        job_id: typing.Optional[builtins.str] = None,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param job_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#job_id PipesPipe#job_id}.
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#type PipesPipe#type}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cb1fcc6fbd1f1e3758bdb48b6a3c81c883e0742b676f205d251f459156ddcc99)
            check_type(argname="argument job_id", value=job_id, expected_type=type_hints["job_id"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if job_id is not None:
            self._values["job_id"] = job_id
        if type is not None:
            self._values["type"] = type

    @builtins.property
    def job_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#job_id PipesPipe#job_id}.'''
        result = self._values.get("job_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#type PipesPipe#type}.'''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PipesPipeTargetParametersBatchJobParametersDependsOn(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PipesPipeTargetParametersBatchJobParametersDependsOnList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.pipesPipe.PipesPipeTargetParametersBatchJobParametersDependsOnList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8cb8a9945f0c608d5fcf7f383740bad9d60c4d3ef6de9e047c6ceaa753645549)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "PipesPipeTargetParametersBatchJobParametersDependsOnOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b33be7e84888a9f942edf1387249cfd6bedffd33bdd04f6305f5a67996bf1ad)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("PipesPipeTargetParametersBatchJobParametersDependsOnOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7103c233f381ad8baf55de37d4b750c2671c8a4dee9aa2d36cf3fe70438455c3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c0ee6e5bf4ab6d2e14e11196ff1668e33ff2fbeb370198de6b5f0b2bb5d9d01d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e0e0f049828f52c7c736c7d08b4f3ebff12de18ef9ab0002d7b89de641dda992)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PipesPipeTargetParametersBatchJobParametersDependsOn]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PipesPipeTargetParametersBatchJobParametersDependsOn]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PipesPipeTargetParametersBatchJobParametersDependsOn]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__64d3803627823b0ba1de0e2c1292956890018234d150b2bb2e62d47d11fbbf1f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class PipesPipeTargetParametersBatchJobParametersDependsOnOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.pipesPipe.PipesPipeTargetParametersBatchJobParametersDependsOnOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__df66a2368691a878c4ccbd7789ac1ecaf64ac0681d69eee8a3d05e201528d85c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetJobId")
    def reset_job_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetJobId", []))

    @jsii.member(jsii_name="resetType")
    def reset_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetType", []))

    @builtins.property
    @jsii.member(jsii_name="jobIdInput")
    def job_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "jobIdInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="jobId")
    def job_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "jobId"))

    @job_id.setter
    def job_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0d335e9cea51ea091f0162c67f13f1cb04aa4f0adbbd8a1a37964595ce2c284b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "jobId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__67a34d878e51345a09e209e1fe1387c8875bea81fe703f33e90f4024efd040a5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PipesPipeTargetParametersBatchJobParametersDependsOn]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PipesPipeTargetParametersBatchJobParametersDependsOn]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PipesPipeTargetParametersBatchJobParametersDependsOn]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d16a7862cd75343c11e4f415854833303c369fce5f244b245861ca0a95382c9a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class PipesPipeTargetParametersBatchJobParametersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.pipesPipe.PipesPipeTargetParametersBatchJobParametersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__51013534b1332acb48990f3bb973c2924a78c6e797aa2ef76c9cb96e73feb2f2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putArrayProperties")
    def put_array_properties(
        self,
        *,
        size: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param size: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#size PipesPipe#size}.
        '''
        value = PipesPipeTargetParametersBatchJobParametersArrayProperties(size=size)

        return typing.cast(None, jsii.invoke(self, "putArrayProperties", [value]))

    @jsii.member(jsii_name="putContainerOverrides")
    def put_container_overrides(
        self,
        *,
        command: typing.Optional[typing.Sequence[builtins.str]] = None,
        environment: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[PipesPipeTargetParametersBatchJobParametersContainerOverridesEnvironment, typing.Dict[builtins.str, typing.Any]]]]] = None,
        instance_type: typing.Optional[builtins.str] = None,
        resource_requirement: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[PipesPipeTargetParametersBatchJobParametersContainerOverridesResourceRequirement, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param command: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#command PipesPipe#command}.
        :param environment: environment block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#environment PipesPipe#environment}
        :param instance_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#instance_type PipesPipe#instance_type}.
        :param resource_requirement: resource_requirement block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#resource_requirement PipesPipe#resource_requirement}
        '''
        value = PipesPipeTargetParametersBatchJobParametersContainerOverrides(
            command=command,
            environment=environment,
            instance_type=instance_type,
            resource_requirement=resource_requirement,
        )

        return typing.cast(None, jsii.invoke(self, "putContainerOverrides", [value]))

    @jsii.member(jsii_name="putDependsOn")
    def put_depends_on(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[PipesPipeTargetParametersBatchJobParametersDependsOn, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__71f12f0271674aeb7757f64d64981e7840a1f1d0a5c1118b3201e94ebfa2db49)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putDependsOn", [value]))

    @jsii.member(jsii_name="putRetryStrategy")
    def put_retry_strategy(
        self,
        *,
        attempts: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param attempts: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#attempts PipesPipe#attempts}.
        '''
        value = PipesPipeTargetParametersBatchJobParametersRetryStrategy(
            attempts=attempts
        )

        return typing.cast(None, jsii.invoke(self, "putRetryStrategy", [value]))

    @jsii.member(jsii_name="resetArrayProperties")
    def reset_array_properties(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetArrayProperties", []))

    @jsii.member(jsii_name="resetContainerOverrides")
    def reset_container_overrides(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetContainerOverrides", []))

    @jsii.member(jsii_name="resetDependsOn")
    def reset_depends_on(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDependsOn", []))

    @jsii.member(jsii_name="resetParameters")
    def reset_parameters(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetParameters", []))

    @jsii.member(jsii_name="resetRetryStrategy")
    def reset_retry_strategy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRetryStrategy", []))

    @builtins.property
    @jsii.member(jsii_name="arrayProperties")
    def array_properties(
        self,
    ) -> PipesPipeTargetParametersBatchJobParametersArrayPropertiesOutputReference:
        return typing.cast(PipesPipeTargetParametersBatchJobParametersArrayPropertiesOutputReference, jsii.get(self, "arrayProperties"))

    @builtins.property
    @jsii.member(jsii_name="containerOverrides")
    def container_overrides(
        self,
    ) -> PipesPipeTargetParametersBatchJobParametersContainerOverridesOutputReference:
        return typing.cast(PipesPipeTargetParametersBatchJobParametersContainerOverridesOutputReference, jsii.get(self, "containerOverrides"))

    @builtins.property
    @jsii.member(jsii_name="dependsOn")
    def depends_on(self) -> PipesPipeTargetParametersBatchJobParametersDependsOnList:
        return typing.cast(PipesPipeTargetParametersBatchJobParametersDependsOnList, jsii.get(self, "dependsOn"))

    @builtins.property
    @jsii.member(jsii_name="retryStrategy")
    def retry_strategy(
        self,
    ) -> "PipesPipeTargetParametersBatchJobParametersRetryStrategyOutputReference":
        return typing.cast("PipesPipeTargetParametersBatchJobParametersRetryStrategyOutputReference", jsii.get(self, "retryStrategy"))

    @builtins.property
    @jsii.member(jsii_name="arrayPropertiesInput")
    def array_properties_input(
        self,
    ) -> typing.Optional[PipesPipeTargetParametersBatchJobParametersArrayProperties]:
        return typing.cast(typing.Optional[PipesPipeTargetParametersBatchJobParametersArrayProperties], jsii.get(self, "arrayPropertiesInput"))

    @builtins.property
    @jsii.member(jsii_name="containerOverridesInput")
    def container_overrides_input(
        self,
    ) -> typing.Optional[PipesPipeTargetParametersBatchJobParametersContainerOverrides]:
        return typing.cast(typing.Optional[PipesPipeTargetParametersBatchJobParametersContainerOverrides], jsii.get(self, "containerOverridesInput"))

    @builtins.property
    @jsii.member(jsii_name="dependsOnInput")
    def depends_on_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PipesPipeTargetParametersBatchJobParametersDependsOn]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PipesPipeTargetParametersBatchJobParametersDependsOn]]], jsii.get(self, "dependsOnInput"))

    @builtins.property
    @jsii.member(jsii_name="jobDefinitionInput")
    def job_definition_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "jobDefinitionInput"))

    @builtins.property
    @jsii.member(jsii_name="jobNameInput")
    def job_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "jobNameInput"))

    @builtins.property
    @jsii.member(jsii_name="parametersInput")
    def parameters_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "parametersInput"))

    @builtins.property
    @jsii.member(jsii_name="retryStrategyInput")
    def retry_strategy_input(
        self,
    ) -> typing.Optional["PipesPipeTargetParametersBatchJobParametersRetryStrategy"]:
        return typing.cast(typing.Optional["PipesPipeTargetParametersBatchJobParametersRetryStrategy"], jsii.get(self, "retryStrategyInput"))

    @builtins.property
    @jsii.member(jsii_name="jobDefinition")
    def job_definition(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "jobDefinition"))

    @job_definition.setter
    def job_definition(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__797e7e633a63e2e8d27237d97fc171cb744d9fc2baad1bc928dcd0be515f9446)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "jobDefinition", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="jobName")
    def job_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "jobName"))

    @job_name.setter
    def job_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__77ded11b2398f3827a9d3a680581acf75a380d2746da00c7413848fa8494b3dd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "jobName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="parameters")
    def parameters(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "parameters"))

    @parameters.setter
    def parameters(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ce87b886e35c57cead86d9572a85ce7f92fa0a11f6c6fce3f7929921ecd3dae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "parameters", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[PipesPipeTargetParametersBatchJobParameters]:
        return typing.cast(typing.Optional[PipesPipeTargetParametersBatchJobParameters], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[PipesPipeTargetParametersBatchJobParameters],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2fa24e01ff6140f3726c1b5ae60004e8566870a765af9b6f805b93d6e0cdf165)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.pipesPipe.PipesPipeTargetParametersBatchJobParametersRetryStrategy",
    jsii_struct_bases=[],
    name_mapping={"attempts": "attempts"},
)
class PipesPipeTargetParametersBatchJobParametersRetryStrategy:
    def __init__(self, *, attempts: typing.Optional[jsii.Number] = None) -> None:
        '''
        :param attempts: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#attempts PipesPipe#attempts}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d63beaea962f0fa96bc28232dfc753ddf27f99585639ce02314e799047e0e6f3)
            check_type(argname="argument attempts", value=attempts, expected_type=type_hints["attempts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if attempts is not None:
            self._values["attempts"] = attempts

    @builtins.property
    def attempts(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#attempts PipesPipe#attempts}.'''
        result = self._values.get("attempts")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PipesPipeTargetParametersBatchJobParametersRetryStrategy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PipesPipeTargetParametersBatchJobParametersRetryStrategyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.pipesPipe.PipesPipeTargetParametersBatchJobParametersRetryStrategyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__573dbbdb415955a0ea4747b82393cb9e4b10a6bbce7c74db49f7bcb42f90fbec)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAttempts")
    def reset_attempts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAttempts", []))

    @builtins.property
    @jsii.member(jsii_name="attemptsInput")
    def attempts_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "attemptsInput"))

    @builtins.property
    @jsii.member(jsii_name="attempts")
    def attempts(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "attempts"))

    @attempts.setter
    def attempts(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8810dc40a100e75db558dceab47eb12cb9cd5c31ae2b46184df4cbc19b08828c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "attempts", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[PipesPipeTargetParametersBatchJobParametersRetryStrategy]:
        return typing.cast(typing.Optional[PipesPipeTargetParametersBatchJobParametersRetryStrategy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[PipesPipeTargetParametersBatchJobParametersRetryStrategy],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__deba7d132bbfc95efdb1e26a6233cb315b260780d95bcf991ff2b820fd7fad4f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.pipesPipe.PipesPipeTargetParametersCloudwatchLogsParameters",
    jsii_struct_bases=[],
    name_mapping={"log_stream_name": "logStreamName", "timestamp": "timestamp"},
)
class PipesPipeTargetParametersCloudwatchLogsParameters:
    def __init__(
        self,
        *,
        log_stream_name: typing.Optional[builtins.str] = None,
        timestamp: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param log_stream_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#log_stream_name PipesPipe#log_stream_name}.
        :param timestamp: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#timestamp PipesPipe#timestamp}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__92cb6bdceee1f4568f4320e14cca8c5ea498cb8144f618cdf2b06fcd2e7814fb)
            check_type(argname="argument log_stream_name", value=log_stream_name, expected_type=type_hints["log_stream_name"])
            check_type(argname="argument timestamp", value=timestamp, expected_type=type_hints["timestamp"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if log_stream_name is not None:
            self._values["log_stream_name"] = log_stream_name
        if timestamp is not None:
            self._values["timestamp"] = timestamp

    @builtins.property
    def log_stream_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#log_stream_name PipesPipe#log_stream_name}.'''
        result = self._values.get("log_stream_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timestamp(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#timestamp PipesPipe#timestamp}.'''
        result = self._values.get("timestamp")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PipesPipeTargetParametersCloudwatchLogsParameters(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PipesPipeTargetParametersCloudwatchLogsParametersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.pipesPipe.PipesPipeTargetParametersCloudwatchLogsParametersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__839e718a5ba5d5ed4425b5113a0f51dd507ff2dca0282c0ff826afa4e3740a01)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetLogStreamName")
    def reset_log_stream_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLogStreamName", []))

    @jsii.member(jsii_name="resetTimestamp")
    def reset_timestamp(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimestamp", []))

    @builtins.property
    @jsii.member(jsii_name="logStreamNameInput")
    def log_stream_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "logStreamNameInput"))

    @builtins.property
    @jsii.member(jsii_name="timestampInput")
    def timestamp_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "timestampInput"))

    @builtins.property
    @jsii.member(jsii_name="logStreamName")
    def log_stream_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "logStreamName"))

    @log_stream_name.setter
    def log_stream_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6a94062f22ce01139c14258fe6cb27317c9ce5feaffed7949ccaf2d533bb0d93)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "logStreamName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="timestamp")
    def timestamp(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "timestamp"))

    @timestamp.setter
    def timestamp(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__137f76ae7ae10ced32011cadc5c9f53a1789248770b44e325618f3f2c0b95dcc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timestamp", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[PipesPipeTargetParametersCloudwatchLogsParameters]:
        return typing.cast(typing.Optional[PipesPipeTargetParametersCloudwatchLogsParameters], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[PipesPipeTargetParametersCloudwatchLogsParameters],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a26618cc9e98d91a35c9dcaaedff4757e6b603b7645b669b7292ac93cf5fc4b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.pipesPipe.PipesPipeTargetParametersEcsTaskParameters",
    jsii_struct_bases=[],
    name_mapping={
        "task_definition_arn": "taskDefinitionArn",
        "capacity_provider_strategy": "capacityProviderStrategy",
        "enable_ecs_managed_tags": "enableEcsManagedTags",
        "enable_execute_command": "enableExecuteCommand",
        "group": "group",
        "launch_type": "launchType",
        "network_configuration": "networkConfiguration",
        "overrides": "overrides",
        "placement_constraint": "placementConstraint",
        "placement_strategy": "placementStrategy",
        "platform_version": "platformVersion",
        "propagate_tags": "propagateTags",
        "reference_id": "referenceId",
        "tags": "tags",
        "task_count": "taskCount",
    },
)
class PipesPipeTargetParametersEcsTaskParameters:
    def __init__(
        self,
        *,
        task_definition_arn: builtins.str,
        capacity_provider_strategy: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["PipesPipeTargetParametersEcsTaskParametersCapacityProviderStrategy", typing.Dict[builtins.str, typing.Any]]]]] = None,
        enable_ecs_managed_tags: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_execute_command: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        group: typing.Optional[builtins.str] = None,
        launch_type: typing.Optional[builtins.str] = None,
        network_configuration: typing.Optional[typing.Union["PipesPipeTargetParametersEcsTaskParametersNetworkConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        overrides: typing.Optional[typing.Union["PipesPipeTargetParametersEcsTaskParametersOverrides", typing.Dict[builtins.str, typing.Any]]] = None,
        placement_constraint: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["PipesPipeTargetParametersEcsTaskParametersPlacementConstraint", typing.Dict[builtins.str, typing.Any]]]]] = None,
        placement_strategy: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["PipesPipeTargetParametersEcsTaskParametersPlacementStrategy", typing.Dict[builtins.str, typing.Any]]]]] = None,
        platform_version: typing.Optional[builtins.str] = None,
        propagate_tags: typing.Optional[builtins.str] = None,
        reference_id: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        task_count: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param task_definition_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#task_definition_arn PipesPipe#task_definition_arn}.
        :param capacity_provider_strategy: capacity_provider_strategy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#capacity_provider_strategy PipesPipe#capacity_provider_strategy}
        :param enable_ecs_managed_tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#enable_ecs_managed_tags PipesPipe#enable_ecs_managed_tags}.
        :param enable_execute_command: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#enable_execute_command PipesPipe#enable_execute_command}.
        :param group: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#group PipesPipe#group}.
        :param launch_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#launch_type PipesPipe#launch_type}.
        :param network_configuration: network_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#network_configuration PipesPipe#network_configuration}
        :param overrides: overrides block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#overrides PipesPipe#overrides}
        :param placement_constraint: placement_constraint block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#placement_constraint PipesPipe#placement_constraint}
        :param placement_strategy: placement_strategy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#placement_strategy PipesPipe#placement_strategy}
        :param platform_version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#platform_version PipesPipe#platform_version}.
        :param propagate_tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#propagate_tags PipesPipe#propagate_tags}.
        :param reference_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#reference_id PipesPipe#reference_id}.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#tags PipesPipe#tags}.
        :param task_count: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#task_count PipesPipe#task_count}.
        '''
        if isinstance(network_configuration, dict):
            network_configuration = PipesPipeTargetParametersEcsTaskParametersNetworkConfiguration(**network_configuration)
        if isinstance(overrides, dict):
            overrides = PipesPipeTargetParametersEcsTaskParametersOverrides(**overrides)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a10927bb2f07937e87192645c4c211eeee9124d5ae21a0be9d427bd855c92c7)
            check_type(argname="argument task_definition_arn", value=task_definition_arn, expected_type=type_hints["task_definition_arn"])
            check_type(argname="argument capacity_provider_strategy", value=capacity_provider_strategy, expected_type=type_hints["capacity_provider_strategy"])
            check_type(argname="argument enable_ecs_managed_tags", value=enable_ecs_managed_tags, expected_type=type_hints["enable_ecs_managed_tags"])
            check_type(argname="argument enable_execute_command", value=enable_execute_command, expected_type=type_hints["enable_execute_command"])
            check_type(argname="argument group", value=group, expected_type=type_hints["group"])
            check_type(argname="argument launch_type", value=launch_type, expected_type=type_hints["launch_type"])
            check_type(argname="argument network_configuration", value=network_configuration, expected_type=type_hints["network_configuration"])
            check_type(argname="argument overrides", value=overrides, expected_type=type_hints["overrides"])
            check_type(argname="argument placement_constraint", value=placement_constraint, expected_type=type_hints["placement_constraint"])
            check_type(argname="argument placement_strategy", value=placement_strategy, expected_type=type_hints["placement_strategy"])
            check_type(argname="argument platform_version", value=platform_version, expected_type=type_hints["platform_version"])
            check_type(argname="argument propagate_tags", value=propagate_tags, expected_type=type_hints["propagate_tags"])
            check_type(argname="argument reference_id", value=reference_id, expected_type=type_hints["reference_id"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument task_count", value=task_count, expected_type=type_hints["task_count"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "task_definition_arn": task_definition_arn,
        }
        if capacity_provider_strategy is not None:
            self._values["capacity_provider_strategy"] = capacity_provider_strategy
        if enable_ecs_managed_tags is not None:
            self._values["enable_ecs_managed_tags"] = enable_ecs_managed_tags
        if enable_execute_command is not None:
            self._values["enable_execute_command"] = enable_execute_command
        if group is not None:
            self._values["group"] = group
        if launch_type is not None:
            self._values["launch_type"] = launch_type
        if network_configuration is not None:
            self._values["network_configuration"] = network_configuration
        if overrides is not None:
            self._values["overrides"] = overrides
        if placement_constraint is not None:
            self._values["placement_constraint"] = placement_constraint
        if placement_strategy is not None:
            self._values["placement_strategy"] = placement_strategy
        if platform_version is not None:
            self._values["platform_version"] = platform_version
        if propagate_tags is not None:
            self._values["propagate_tags"] = propagate_tags
        if reference_id is not None:
            self._values["reference_id"] = reference_id
        if tags is not None:
            self._values["tags"] = tags
        if task_count is not None:
            self._values["task_count"] = task_count

    @builtins.property
    def task_definition_arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#task_definition_arn PipesPipe#task_definition_arn}.'''
        result = self._values.get("task_definition_arn")
        assert result is not None, "Required property 'task_definition_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def capacity_provider_strategy(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["PipesPipeTargetParametersEcsTaskParametersCapacityProviderStrategy"]]]:
        '''capacity_provider_strategy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#capacity_provider_strategy PipesPipe#capacity_provider_strategy}
        '''
        result = self._values.get("capacity_provider_strategy")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["PipesPipeTargetParametersEcsTaskParametersCapacityProviderStrategy"]]], result)

    @builtins.property
    def enable_ecs_managed_tags(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#enable_ecs_managed_tags PipesPipe#enable_ecs_managed_tags}.'''
        result = self._values.get("enable_ecs_managed_tags")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def enable_execute_command(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#enable_execute_command PipesPipe#enable_execute_command}.'''
        result = self._values.get("enable_execute_command")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def group(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#group PipesPipe#group}.'''
        result = self._values.get("group")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def launch_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#launch_type PipesPipe#launch_type}.'''
        result = self._values.get("launch_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def network_configuration(
        self,
    ) -> typing.Optional["PipesPipeTargetParametersEcsTaskParametersNetworkConfiguration"]:
        '''network_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#network_configuration PipesPipe#network_configuration}
        '''
        result = self._values.get("network_configuration")
        return typing.cast(typing.Optional["PipesPipeTargetParametersEcsTaskParametersNetworkConfiguration"], result)

    @builtins.property
    def overrides(
        self,
    ) -> typing.Optional["PipesPipeTargetParametersEcsTaskParametersOverrides"]:
        '''overrides block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#overrides PipesPipe#overrides}
        '''
        result = self._values.get("overrides")
        return typing.cast(typing.Optional["PipesPipeTargetParametersEcsTaskParametersOverrides"], result)

    @builtins.property
    def placement_constraint(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["PipesPipeTargetParametersEcsTaskParametersPlacementConstraint"]]]:
        '''placement_constraint block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#placement_constraint PipesPipe#placement_constraint}
        '''
        result = self._values.get("placement_constraint")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["PipesPipeTargetParametersEcsTaskParametersPlacementConstraint"]]], result)

    @builtins.property
    def placement_strategy(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["PipesPipeTargetParametersEcsTaskParametersPlacementStrategy"]]]:
        '''placement_strategy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#placement_strategy PipesPipe#placement_strategy}
        '''
        result = self._values.get("placement_strategy")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["PipesPipeTargetParametersEcsTaskParametersPlacementStrategy"]]], result)

    @builtins.property
    def platform_version(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#platform_version PipesPipe#platform_version}.'''
        result = self._values.get("platform_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def propagate_tags(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#propagate_tags PipesPipe#propagate_tags}.'''
        result = self._values.get("propagate_tags")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def reference_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#reference_id PipesPipe#reference_id}.'''
        result = self._values.get("reference_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#tags PipesPipe#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def task_count(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#task_count PipesPipe#task_count}.'''
        result = self._values.get("task_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PipesPipeTargetParametersEcsTaskParameters(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.pipesPipe.PipesPipeTargetParametersEcsTaskParametersCapacityProviderStrategy",
    jsii_struct_bases=[],
    name_mapping={
        "capacity_provider": "capacityProvider",
        "base": "base",
        "weight": "weight",
    },
)
class PipesPipeTargetParametersEcsTaskParametersCapacityProviderStrategy:
    def __init__(
        self,
        *,
        capacity_provider: builtins.str,
        base: typing.Optional[jsii.Number] = None,
        weight: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param capacity_provider: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#capacity_provider PipesPipe#capacity_provider}.
        :param base: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#base PipesPipe#base}.
        :param weight: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#weight PipesPipe#weight}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e3054ab06098c1579b8624eef97bc10a5ca5d492ae131c55f551b31651398e16)
            check_type(argname="argument capacity_provider", value=capacity_provider, expected_type=type_hints["capacity_provider"])
            check_type(argname="argument base", value=base, expected_type=type_hints["base"])
            check_type(argname="argument weight", value=weight, expected_type=type_hints["weight"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "capacity_provider": capacity_provider,
        }
        if base is not None:
            self._values["base"] = base
        if weight is not None:
            self._values["weight"] = weight

    @builtins.property
    def capacity_provider(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#capacity_provider PipesPipe#capacity_provider}.'''
        result = self._values.get("capacity_provider")
        assert result is not None, "Required property 'capacity_provider' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def base(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#base PipesPipe#base}.'''
        result = self._values.get("base")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def weight(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#weight PipesPipe#weight}.'''
        result = self._values.get("weight")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PipesPipeTargetParametersEcsTaskParametersCapacityProviderStrategy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PipesPipeTargetParametersEcsTaskParametersCapacityProviderStrategyList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.pipesPipe.PipesPipeTargetParametersEcsTaskParametersCapacityProviderStrategyList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4f8eb6987859b1b7620e695ba8c089af9e01bccc83c985627a1d02b2b2e499fb)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "PipesPipeTargetParametersEcsTaskParametersCapacityProviderStrategyOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__628a625db3e68eeb2ba4cddcd333ddfc6b82a81c349ceab63d2e50124afc9f3d)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("PipesPipeTargetParametersEcsTaskParametersCapacityProviderStrategyOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3904b9b6a72171d373b7f14a31bfd550e99a63dc91d3a5ca7cbb80ac888a132d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2884c5c1f570f0ed79819dddbd903cbc52dda5a6f8f08df51f1ea6d27b662c66)
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
            type_hints = typing.get_type_hints(_typecheckingstub__40de0881de1df407d2d6bd7f2599f5b89b47ad7efb7e099685862285e2217b01)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PipesPipeTargetParametersEcsTaskParametersCapacityProviderStrategy]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PipesPipeTargetParametersEcsTaskParametersCapacityProviderStrategy]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PipesPipeTargetParametersEcsTaskParametersCapacityProviderStrategy]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__652e26d712adef431ddfee122ccafcd779b41d340548a245a0f42c02938787db)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class PipesPipeTargetParametersEcsTaskParametersCapacityProviderStrategyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.pipesPipe.PipesPipeTargetParametersEcsTaskParametersCapacityProviderStrategyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6ee7f7b5b0062f5c440e676a8f53a912d8ac0d926c74e7635326785bc01d1c09)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetBase")
    def reset_base(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBase", []))

    @jsii.member(jsii_name="resetWeight")
    def reset_weight(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWeight", []))

    @builtins.property
    @jsii.member(jsii_name="baseInput")
    def base_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "baseInput"))

    @builtins.property
    @jsii.member(jsii_name="capacityProviderInput")
    def capacity_provider_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "capacityProviderInput"))

    @builtins.property
    @jsii.member(jsii_name="weightInput")
    def weight_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "weightInput"))

    @builtins.property
    @jsii.member(jsii_name="base")
    def base(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "base"))

    @base.setter
    def base(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__34fe5515ad3d67ff0e2aa2ece7d829c0f30876652c038c928ec00e417ba906ae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "base", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="capacityProvider")
    def capacity_provider(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "capacityProvider"))

    @capacity_provider.setter
    def capacity_provider(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e060b9cb866e7134a200b1ac0ba87d53db27009e756247b4c6fc0aac9159b7e0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "capacityProvider", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="weight")
    def weight(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "weight"))

    @weight.setter
    def weight(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__53823e7e6e20f8a6982266aa3d85b83761f55c1f9ccc4f2c6510ca057fd4be4f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "weight", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PipesPipeTargetParametersEcsTaskParametersCapacityProviderStrategy]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PipesPipeTargetParametersEcsTaskParametersCapacityProviderStrategy]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PipesPipeTargetParametersEcsTaskParametersCapacityProviderStrategy]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__410023db1584cd6fc23a393d7bc13fd671862c6a029c6b152d0f09318a8376d0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.pipesPipe.PipesPipeTargetParametersEcsTaskParametersNetworkConfiguration",
    jsii_struct_bases=[],
    name_mapping={"aws_vpc_configuration": "awsVpcConfiguration"},
)
class PipesPipeTargetParametersEcsTaskParametersNetworkConfiguration:
    def __init__(
        self,
        *,
        aws_vpc_configuration: typing.Optional[typing.Union["PipesPipeTargetParametersEcsTaskParametersNetworkConfigurationAwsVpcConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param aws_vpc_configuration: aws_vpc_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#aws_vpc_configuration PipesPipe#aws_vpc_configuration}
        '''
        if isinstance(aws_vpc_configuration, dict):
            aws_vpc_configuration = PipesPipeTargetParametersEcsTaskParametersNetworkConfigurationAwsVpcConfiguration(**aws_vpc_configuration)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1fc2b8249449876cb4162c17a6ed2f7421423e512b39833c49f0692d4cabba2c)
            check_type(argname="argument aws_vpc_configuration", value=aws_vpc_configuration, expected_type=type_hints["aws_vpc_configuration"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if aws_vpc_configuration is not None:
            self._values["aws_vpc_configuration"] = aws_vpc_configuration

    @builtins.property
    def aws_vpc_configuration(
        self,
    ) -> typing.Optional["PipesPipeTargetParametersEcsTaskParametersNetworkConfigurationAwsVpcConfiguration"]:
        '''aws_vpc_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#aws_vpc_configuration PipesPipe#aws_vpc_configuration}
        '''
        result = self._values.get("aws_vpc_configuration")
        return typing.cast(typing.Optional["PipesPipeTargetParametersEcsTaskParametersNetworkConfigurationAwsVpcConfiguration"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PipesPipeTargetParametersEcsTaskParametersNetworkConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.pipesPipe.PipesPipeTargetParametersEcsTaskParametersNetworkConfigurationAwsVpcConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "assign_public_ip": "assignPublicIp",
        "security_groups": "securityGroups",
        "subnets": "subnets",
    },
)
class PipesPipeTargetParametersEcsTaskParametersNetworkConfigurationAwsVpcConfiguration:
    def __init__(
        self,
        *,
        assign_public_ip: typing.Optional[builtins.str] = None,
        security_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
        subnets: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param assign_public_ip: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#assign_public_ip PipesPipe#assign_public_ip}.
        :param security_groups: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#security_groups PipesPipe#security_groups}.
        :param subnets: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#subnets PipesPipe#subnets}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f9b8458583630fb2f880e88b55f83ac32157f7113c6682ede3e0f3e81ea9844)
            check_type(argname="argument assign_public_ip", value=assign_public_ip, expected_type=type_hints["assign_public_ip"])
            check_type(argname="argument security_groups", value=security_groups, expected_type=type_hints["security_groups"])
            check_type(argname="argument subnets", value=subnets, expected_type=type_hints["subnets"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if assign_public_ip is not None:
            self._values["assign_public_ip"] = assign_public_ip
        if security_groups is not None:
            self._values["security_groups"] = security_groups
        if subnets is not None:
            self._values["subnets"] = subnets

    @builtins.property
    def assign_public_ip(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#assign_public_ip PipesPipe#assign_public_ip}.'''
        result = self._values.get("assign_public_ip")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def security_groups(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#security_groups PipesPipe#security_groups}.'''
        result = self._values.get("security_groups")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def subnets(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#subnets PipesPipe#subnets}.'''
        result = self._values.get("subnets")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PipesPipeTargetParametersEcsTaskParametersNetworkConfigurationAwsVpcConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PipesPipeTargetParametersEcsTaskParametersNetworkConfigurationAwsVpcConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.pipesPipe.PipesPipeTargetParametersEcsTaskParametersNetworkConfigurationAwsVpcConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__dfd6418bd28eac93b85b0276515f7c1914dfa27da7a08ec25fd6ec740f78a36b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAssignPublicIp")
    def reset_assign_public_ip(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAssignPublicIp", []))

    @jsii.member(jsii_name="resetSecurityGroups")
    def reset_security_groups(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSecurityGroups", []))

    @jsii.member(jsii_name="resetSubnets")
    def reset_subnets(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSubnets", []))

    @builtins.property
    @jsii.member(jsii_name="assignPublicIpInput")
    def assign_public_ip_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "assignPublicIpInput"))

    @builtins.property
    @jsii.member(jsii_name="securityGroupsInput")
    def security_groups_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "securityGroupsInput"))

    @builtins.property
    @jsii.member(jsii_name="subnetsInput")
    def subnets_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "subnetsInput"))

    @builtins.property
    @jsii.member(jsii_name="assignPublicIp")
    def assign_public_ip(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "assignPublicIp"))

    @assign_public_ip.setter
    def assign_public_ip(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__010b39ac5e2e088b48c069664121387845c4175c141fde2996434537b1a058ab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "assignPublicIp", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="securityGroups")
    def security_groups(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "securityGroups"))

    @security_groups.setter
    def security_groups(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f54445fdd27b1c2121b7972d51a4fd0a081e43fe218b596a95b61ee082c568f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "securityGroups", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="subnets")
    def subnets(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "subnets"))

    @subnets.setter
    def subnets(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__80139aea94394ff48f6371f024a0c8fdd4d7b67b289bee562f7ba78e7ab72a05)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subnets", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[PipesPipeTargetParametersEcsTaskParametersNetworkConfigurationAwsVpcConfiguration]:
        return typing.cast(typing.Optional[PipesPipeTargetParametersEcsTaskParametersNetworkConfigurationAwsVpcConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[PipesPipeTargetParametersEcsTaskParametersNetworkConfigurationAwsVpcConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__70ba973fb9a3119f5b4f73742f71ed8de183e8346150c610b76fe4cca1faeb3e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class PipesPipeTargetParametersEcsTaskParametersNetworkConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.pipesPipe.PipesPipeTargetParametersEcsTaskParametersNetworkConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c232c20104e5803542017368abd0dd178fff0a77e21dee1e1b870ff34e47e098)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAwsVpcConfiguration")
    def put_aws_vpc_configuration(
        self,
        *,
        assign_public_ip: typing.Optional[builtins.str] = None,
        security_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
        subnets: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param assign_public_ip: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#assign_public_ip PipesPipe#assign_public_ip}.
        :param security_groups: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#security_groups PipesPipe#security_groups}.
        :param subnets: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#subnets PipesPipe#subnets}.
        '''
        value = PipesPipeTargetParametersEcsTaskParametersNetworkConfigurationAwsVpcConfiguration(
            assign_public_ip=assign_public_ip,
            security_groups=security_groups,
            subnets=subnets,
        )

        return typing.cast(None, jsii.invoke(self, "putAwsVpcConfiguration", [value]))

    @jsii.member(jsii_name="resetAwsVpcConfiguration")
    def reset_aws_vpc_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAwsVpcConfiguration", []))

    @builtins.property
    @jsii.member(jsii_name="awsVpcConfiguration")
    def aws_vpc_configuration(
        self,
    ) -> PipesPipeTargetParametersEcsTaskParametersNetworkConfigurationAwsVpcConfigurationOutputReference:
        return typing.cast(PipesPipeTargetParametersEcsTaskParametersNetworkConfigurationAwsVpcConfigurationOutputReference, jsii.get(self, "awsVpcConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="awsVpcConfigurationInput")
    def aws_vpc_configuration_input(
        self,
    ) -> typing.Optional[PipesPipeTargetParametersEcsTaskParametersNetworkConfigurationAwsVpcConfiguration]:
        return typing.cast(typing.Optional[PipesPipeTargetParametersEcsTaskParametersNetworkConfigurationAwsVpcConfiguration], jsii.get(self, "awsVpcConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[PipesPipeTargetParametersEcsTaskParametersNetworkConfiguration]:
        return typing.cast(typing.Optional[PipesPipeTargetParametersEcsTaskParametersNetworkConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[PipesPipeTargetParametersEcsTaskParametersNetworkConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c58857f52ae2350aa0ebbc4d8c613ce1618e1f1355a3e78233e8d6ec46b20b78)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class PipesPipeTargetParametersEcsTaskParametersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.pipesPipe.PipesPipeTargetParametersEcsTaskParametersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__83a8b37d06f8b34f5ff3f6de4fd2eb1ca3408aa1268f715d20927efe099ae0b9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putCapacityProviderStrategy")
    def put_capacity_provider_strategy(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[PipesPipeTargetParametersEcsTaskParametersCapacityProviderStrategy, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0bee473c8a1626a6d837f95dc4ccaeeaaa1ad57eeb9db65b5e4c8dd57a727414)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putCapacityProviderStrategy", [value]))

    @jsii.member(jsii_name="putNetworkConfiguration")
    def put_network_configuration(
        self,
        *,
        aws_vpc_configuration: typing.Optional[typing.Union[PipesPipeTargetParametersEcsTaskParametersNetworkConfigurationAwsVpcConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param aws_vpc_configuration: aws_vpc_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#aws_vpc_configuration PipesPipe#aws_vpc_configuration}
        '''
        value = PipesPipeTargetParametersEcsTaskParametersNetworkConfiguration(
            aws_vpc_configuration=aws_vpc_configuration
        )

        return typing.cast(None, jsii.invoke(self, "putNetworkConfiguration", [value]))

    @jsii.member(jsii_name="putOverrides")
    def put_overrides(
        self,
        *,
        container_override: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["PipesPipeTargetParametersEcsTaskParametersOverridesContainerOverride", typing.Dict[builtins.str, typing.Any]]]]] = None,
        cpu: typing.Optional[builtins.str] = None,
        ephemeral_storage: typing.Optional[typing.Union["PipesPipeTargetParametersEcsTaskParametersOverridesEphemeralStorage", typing.Dict[builtins.str, typing.Any]]] = None,
        execution_role_arn: typing.Optional[builtins.str] = None,
        inference_accelerator_override: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["PipesPipeTargetParametersEcsTaskParametersOverridesInferenceAcceleratorOverride", typing.Dict[builtins.str, typing.Any]]]]] = None,
        memory: typing.Optional[builtins.str] = None,
        task_role_arn: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param container_override: container_override block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#container_override PipesPipe#container_override}
        :param cpu: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#cpu PipesPipe#cpu}.
        :param ephemeral_storage: ephemeral_storage block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#ephemeral_storage PipesPipe#ephemeral_storage}
        :param execution_role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#execution_role_arn PipesPipe#execution_role_arn}.
        :param inference_accelerator_override: inference_accelerator_override block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#inference_accelerator_override PipesPipe#inference_accelerator_override}
        :param memory: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#memory PipesPipe#memory}.
        :param task_role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#task_role_arn PipesPipe#task_role_arn}.
        '''
        value = PipesPipeTargetParametersEcsTaskParametersOverrides(
            container_override=container_override,
            cpu=cpu,
            ephemeral_storage=ephemeral_storage,
            execution_role_arn=execution_role_arn,
            inference_accelerator_override=inference_accelerator_override,
            memory=memory,
            task_role_arn=task_role_arn,
        )

        return typing.cast(None, jsii.invoke(self, "putOverrides", [value]))

    @jsii.member(jsii_name="putPlacementConstraint")
    def put_placement_constraint(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["PipesPipeTargetParametersEcsTaskParametersPlacementConstraint", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__06bb5b354ce90d6827be6f159baba09f938b3d0ecba4331be394f8cd674f2f26)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putPlacementConstraint", [value]))

    @jsii.member(jsii_name="putPlacementStrategy")
    def put_placement_strategy(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["PipesPipeTargetParametersEcsTaskParametersPlacementStrategy", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fd86ab2df8fed220b31f06f5eb7ee78f07f1e5a15c1b238ec9b0d997ae9ac950)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putPlacementStrategy", [value]))

    @jsii.member(jsii_name="resetCapacityProviderStrategy")
    def reset_capacity_provider_strategy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCapacityProviderStrategy", []))

    @jsii.member(jsii_name="resetEnableEcsManagedTags")
    def reset_enable_ecs_managed_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnableEcsManagedTags", []))

    @jsii.member(jsii_name="resetEnableExecuteCommand")
    def reset_enable_execute_command(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnableExecuteCommand", []))

    @jsii.member(jsii_name="resetGroup")
    def reset_group(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGroup", []))

    @jsii.member(jsii_name="resetLaunchType")
    def reset_launch_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLaunchType", []))

    @jsii.member(jsii_name="resetNetworkConfiguration")
    def reset_network_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNetworkConfiguration", []))

    @jsii.member(jsii_name="resetOverrides")
    def reset_overrides(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOverrides", []))

    @jsii.member(jsii_name="resetPlacementConstraint")
    def reset_placement_constraint(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPlacementConstraint", []))

    @jsii.member(jsii_name="resetPlacementStrategy")
    def reset_placement_strategy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPlacementStrategy", []))

    @jsii.member(jsii_name="resetPlatformVersion")
    def reset_platform_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPlatformVersion", []))

    @jsii.member(jsii_name="resetPropagateTags")
    def reset_propagate_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPropagateTags", []))

    @jsii.member(jsii_name="resetReferenceId")
    def reset_reference_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetReferenceId", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

    @jsii.member(jsii_name="resetTaskCount")
    def reset_task_count(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTaskCount", []))

    @builtins.property
    @jsii.member(jsii_name="capacityProviderStrategy")
    def capacity_provider_strategy(
        self,
    ) -> PipesPipeTargetParametersEcsTaskParametersCapacityProviderStrategyList:
        return typing.cast(PipesPipeTargetParametersEcsTaskParametersCapacityProviderStrategyList, jsii.get(self, "capacityProviderStrategy"))

    @builtins.property
    @jsii.member(jsii_name="networkConfiguration")
    def network_configuration(
        self,
    ) -> PipesPipeTargetParametersEcsTaskParametersNetworkConfigurationOutputReference:
        return typing.cast(PipesPipeTargetParametersEcsTaskParametersNetworkConfigurationOutputReference, jsii.get(self, "networkConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="overrides")
    def overrides(
        self,
    ) -> "PipesPipeTargetParametersEcsTaskParametersOverridesOutputReference":
        return typing.cast("PipesPipeTargetParametersEcsTaskParametersOverridesOutputReference", jsii.get(self, "overrides"))

    @builtins.property
    @jsii.member(jsii_name="placementConstraint")
    def placement_constraint(
        self,
    ) -> "PipesPipeTargetParametersEcsTaskParametersPlacementConstraintList":
        return typing.cast("PipesPipeTargetParametersEcsTaskParametersPlacementConstraintList", jsii.get(self, "placementConstraint"))

    @builtins.property
    @jsii.member(jsii_name="placementStrategy")
    def placement_strategy(
        self,
    ) -> "PipesPipeTargetParametersEcsTaskParametersPlacementStrategyList":
        return typing.cast("PipesPipeTargetParametersEcsTaskParametersPlacementStrategyList", jsii.get(self, "placementStrategy"))

    @builtins.property
    @jsii.member(jsii_name="capacityProviderStrategyInput")
    def capacity_provider_strategy_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PipesPipeTargetParametersEcsTaskParametersCapacityProviderStrategy]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PipesPipeTargetParametersEcsTaskParametersCapacityProviderStrategy]]], jsii.get(self, "capacityProviderStrategyInput"))

    @builtins.property
    @jsii.member(jsii_name="enableEcsManagedTagsInput")
    def enable_ecs_managed_tags_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enableEcsManagedTagsInput"))

    @builtins.property
    @jsii.member(jsii_name="enableExecuteCommandInput")
    def enable_execute_command_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enableExecuteCommandInput"))

    @builtins.property
    @jsii.member(jsii_name="groupInput")
    def group_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "groupInput"))

    @builtins.property
    @jsii.member(jsii_name="launchTypeInput")
    def launch_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "launchTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="networkConfigurationInput")
    def network_configuration_input(
        self,
    ) -> typing.Optional[PipesPipeTargetParametersEcsTaskParametersNetworkConfiguration]:
        return typing.cast(typing.Optional[PipesPipeTargetParametersEcsTaskParametersNetworkConfiguration], jsii.get(self, "networkConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="overridesInput")
    def overrides_input(
        self,
    ) -> typing.Optional["PipesPipeTargetParametersEcsTaskParametersOverrides"]:
        return typing.cast(typing.Optional["PipesPipeTargetParametersEcsTaskParametersOverrides"], jsii.get(self, "overridesInput"))

    @builtins.property
    @jsii.member(jsii_name="placementConstraintInput")
    def placement_constraint_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["PipesPipeTargetParametersEcsTaskParametersPlacementConstraint"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["PipesPipeTargetParametersEcsTaskParametersPlacementConstraint"]]], jsii.get(self, "placementConstraintInput"))

    @builtins.property
    @jsii.member(jsii_name="placementStrategyInput")
    def placement_strategy_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["PipesPipeTargetParametersEcsTaskParametersPlacementStrategy"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["PipesPipeTargetParametersEcsTaskParametersPlacementStrategy"]]], jsii.get(self, "placementStrategyInput"))

    @builtins.property
    @jsii.member(jsii_name="platformVersionInput")
    def platform_version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "platformVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="propagateTagsInput")
    def propagate_tags_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "propagateTagsInput"))

    @builtins.property
    @jsii.member(jsii_name="referenceIdInput")
    def reference_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "referenceIdInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsInput")
    def tags_input(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "tagsInput"))

    @builtins.property
    @jsii.member(jsii_name="taskCountInput")
    def task_count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "taskCountInput"))

    @builtins.property
    @jsii.member(jsii_name="taskDefinitionArnInput")
    def task_definition_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "taskDefinitionArnInput"))

    @builtins.property
    @jsii.member(jsii_name="enableEcsManagedTags")
    def enable_ecs_managed_tags(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enableEcsManagedTags"))

    @enable_ecs_managed_tags.setter
    def enable_ecs_managed_tags(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__61bc854840ba2bdde4558fcb6f94e01b89972b9fd50a5fcbc2c9a6e71412bd89)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableEcsManagedTags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enableExecuteCommand")
    def enable_execute_command(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enableExecuteCommand"))

    @enable_execute_command.setter
    def enable_execute_command(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__640684d59f87fef187f1479ebedbfb4eddd07232f447238bfb1b5ad5bc15ea22)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableExecuteCommand", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="group")
    def group(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "group"))

    @group.setter
    def group(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ab81024c0453103829c471eaa5e0b324a6b9c8c56196cf9c983437feb1f5167b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "group", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="launchType")
    def launch_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "launchType"))

    @launch_type.setter
    def launch_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ee095285772cc13718aaeed248a07215aad2b5c6e5cbffddef007edb7318456)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "launchType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="platformVersion")
    def platform_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "platformVersion"))

    @platform_version.setter
    def platform_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e6cd133e8b68fe993e286ff23d6a437698d4d16ab6382f004ba5089d74aafc1f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "platformVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="propagateTags")
    def propagate_tags(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "propagateTags"))

    @propagate_tags.setter
    def propagate_tags(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__518d3b93e3afd06579015c73487c69f8320c6b6f6ad63febdb4d71cccc1f0c69)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "propagateTags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="referenceId")
    def reference_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "referenceId"))

    @reference_id.setter
    def reference_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e3a76c86c13231a60aa7b9817e7b41b4615bfb1146f310dc3f66b70b3309ff10)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "referenceId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3b5d6b626b3653ccb77cdfe518f03e1c9ea6f38194ecb88c272ab31ce6b97e2d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="taskCount")
    def task_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "taskCount"))

    @task_count.setter
    def task_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e6e5cfa4486319b9c9cddd4ec38b0b1906abfbbf69226a0bc62d921982a43acc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "taskCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="taskDefinitionArn")
    def task_definition_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "taskDefinitionArn"))

    @task_definition_arn.setter
    def task_definition_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__430db9d230553615464f25a9c16d98ed4a40f21ebf9cd6bdddce6752e8365289)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "taskDefinitionArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[PipesPipeTargetParametersEcsTaskParameters]:
        return typing.cast(typing.Optional[PipesPipeTargetParametersEcsTaskParameters], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[PipesPipeTargetParametersEcsTaskParameters],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b785d36f60d64f808bdfdf81a23d611f852e933c190ce9b6d288a1590f5a0f20)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.pipesPipe.PipesPipeTargetParametersEcsTaskParametersOverrides",
    jsii_struct_bases=[],
    name_mapping={
        "container_override": "containerOverride",
        "cpu": "cpu",
        "ephemeral_storage": "ephemeralStorage",
        "execution_role_arn": "executionRoleArn",
        "inference_accelerator_override": "inferenceAcceleratorOverride",
        "memory": "memory",
        "task_role_arn": "taskRoleArn",
    },
)
class PipesPipeTargetParametersEcsTaskParametersOverrides:
    def __init__(
        self,
        *,
        container_override: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["PipesPipeTargetParametersEcsTaskParametersOverridesContainerOverride", typing.Dict[builtins.str, typing.Any]]]]] = None,
        cpu: typing.Optional[builtins.str] = None,
        ephemeral_storage: typing.Optional[typing.Union["PipesPipeTargetParametersEcsTaskParametersOverridesEphemeralStorage", typing.Dict[builtins.str, typing.Any]]] = None,
        execution_role_arn: typing.Optional[builtins.str] = None,
        inference_accelerator_override: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["PipesPipeTargetParametersEcsTaskParametersOverridesInferenceAcceleratorOverride", typing.Dict[builtins.str, typing.Any]]]]] = None,
        memory: typing.Optional[builtins.str] = None,
        task_role_arn: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param container_override: container_override block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#container_override PipesPipe#container_override}
        :param cpu: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#cpu PipesPipe#cpu}.
        :param ephemeral_storage: ephemeral_storage block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#ephemeral_storage PipesPipe#ephemeral_storage}
        :param execution_role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#execution_role_arn PipesPipe#execution_role_arn}.
        :param inference_accelerator_override: inference_accelerator_override block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#inference_accelerator_override PipesPipe#inference_accelerator_override}
        :param memory: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#memory PipesPipe#memory}.
        :param task_role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#task_role_arn PipesPipe#task_role_arn}.
        '''
        if isinstance(ephemeral_storage, dict):
            ephemeral_storage = PipesPipeTargetParametersEcsTaskParametersOverridesEphemeralStorage(**ephemeral_storage)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4ac387ac47f50cd31aabbffeaaf9e2fc5a32808fc03bd77b08282ea770548299)
            check_type(argname="argument container_override", value=container_override, expected_type=type_hints["container_override"])
            check_type(argname="argument cpu", value=cpu, expected_type=type_hints["cpu"])
            check_type(argname="argument ephemeral_storage", value=ephemeral_storage, expected_type=type_hints["ephemeral_storage"])
            check_type(argname="argument execution_role_arn", value=execution_role_arn, expected_type=type_hints["execution_role_arn"])
            check_type(argname="argument inference_accelerator_override", value=inference_accelerator_override, expected_type=type_hints["inference_accelerator_override"])
            check_type(argname="argument memory", value=memory, expected_type=type_hints["memory"])
            check_type(argname="argument task_role_arn", value=task_role_arn, expected_type=type_hints["task_role_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if container_override is not None:
            self._values["container_override"] = container_override
        if cpu is not None:
            self._values["cpu"] = cpu
        if ephemeral_storage is not None:
            self._values["ephemeral_storage"] = ephemeral_storage
        if execution_role_arn is not None:
            self._values["execution_role_arn"] = execution_role_arn
        if inference_accelerator_override is not None:
            self._values["inference_accelerator_override"] = inference_accelerator_override
        if memory is not None:
            self._values["memory"] = memory
        if task_role_arn is not None:
            self._values["task_role_arn"] = task_role_arn

    @builtins.property
    def container_override(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["PipesPipeTargetParametersEcsTaskParametersOverridesContainerOverride"]]]:
        '''container_override block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#container_override PipesPipe#container_override}
        '''
        result = self._values.get("container_override")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["PipesPipeTargetParametersEcsTaskParametersOverridesContainerOverride"]]], result)

    @builtins.property
    def cpu(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#cpu PipesPipe#cpu}.'''
        result = self._values.get("cpu")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ephemeral_storage(
        self,
    ) -> typing.Optional["PipesPipeTargetParametersEcsTaskParametersOverridesEphemeralStorage"]:
        '''ephemeral_storage block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#ephemeral_storage PipesPipe#ephemeral_storage}
        '''
        result = self._values.get("ephemeral_storage")
        return typing.cast(typing.Optional["PipesPipeTargetParametersEcsTaskParametersOverridesEphemeralStorage"], result)

    @builtins.property
    def execution_role_arn(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#execution_role_arn PipesPipe#execution_role_arn}.'''
        result = self._values.get("execution_role_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def inference_accelerator_override(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["PipesPipeTargetParametersEcsTaskParametersOverridesInferenceAcceleratorOverride"]]]:
        '''inference_accelerator_override block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#inference_accelerator_override PipesPipe#inference_accelerator_override}
        '''
        result = self._values.get("inference_accelerator_override")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["PipesPipeTargetParametersEcsTaskParametersOverridesInferenceAcceleratorOverride"]]], result)

    @builtins.property
    def memory(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#memory PipesPipe#memory}.'''
        result = self._values.get("memory")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def task_role_arn(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#task_role_arn PipesPipe#task_role_arn}.'''
        result = self._values.get("task_role_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PipesPipeTargetParametersEcsTaskParametersOverrides(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.pipesPipe.PipesPipeTargetParametersEcsTaskParametersOverridesContainerOverride",
    jsii_struct_bases=[],
    name_mapping={
        "command": "command",
        "cpu": "cpu",
        "environment": "environment",
        "environment_file": "environmentFile",
        "memory": "memory",
        "memory_reservation": "memoryReservation",
        "name": "name",
        "resource_requirement": "resourceRequirement",
    },
)
class PipesPipeTargetParametersEcsTaskParametersOverridesContainerOverride:
    def __init__(
        self,
        *,
        command: typing.Optional[typing.Sequence[builtins.str]] = None,
        cpu: typing.Optional[jsii.Number] = None,
        environment: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["PipesPipeTargetParametersEcsTaskParametersOverridesContainerOverrideEnvironment", typing.Dict[builtins.str, typing.Any]]]]] = None,
        environment_file: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["PipesPipeTargetParametersEcsTaskParametersOverridesContainerOverrideEnvironmentFile", typing.Dict[builtins.str, typing.Any]]]]] = None,
        memory: typing.Optional[jsii.Number] = None,
        memory_reservation: typing.Optional[jsii.Number] = None,
        name: typing.Optional[builtins.str] = None,
        resource_requirement: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["PipesPipeTargetParametersEcsTaskParametersOverridesContainerOverrideResourceRequirement", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param command: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#command PipesPipe#command}.
        :param cpu: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#cpu PipesPipe#cpu}.
        :param environment: environment block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#environment PipesPipe#environment}
        :param environment_file: environment_file block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#environment_file PipesPipe#environment_file}
        :param memory: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#memory PipesPipe#memory}.
        :param memory_reservation: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#memory_reservation PipesPipe#memory_reservation}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#name PipesPipe#name}.
        :param resource_requirement: resource_requirement block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#resource_requirement PipesPipe#resource_requirement}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__44c3465e2e1a0ad67478b883021c7d3e3e703d92f92412ccd839de71b12544eb)
            check_type(argname="argument command", value=command, expected_type=type_hints["command"])
            check_type(argname="argument cpu", value=cpu, expected_type=type_hints["cpu"])
            check_type(argname="argument environment", value=environment, expected_type=type_hints["environment"])
            check_type(argname="argument environment_file", value=environment_file, expected_type=type_hints["environment_file"])
            check_type(argname="argument memory", value=memory, expected_type=type_hints["memory"])
            check_type(argname="argument memory_reservation", value=memory_reservation, expected_type=type_hints["memory_reservation"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument resource_requirement", value=resource_requirement, expected_type=type_hints["resource_requirement"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if command is not None:
            self._values["command"] = command
        if cpu is not None:
            self._values["cpu"] = cpu
        if environment is not None:
            self._values["environment"] = environment
        if environment_file is not None:
            self._values["environment_file"] = environment_file
        if memory is not None:
            self._values["memory"] = memory
        if memory_reservation is not None:
            self._values["memory_reservation"] = memory_reservation
        if name is not None:
            self._values["name"] = name
        if resource_requirement is not None:
            self._values["resource_requirement"] = resource_requirement

    @builtins.property
    def command(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#command PipesPipe#command}.'''
        result = self._values.get("command")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def cpu(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#cpu PipesPipe#cpu}.'''
        result = self._values.get("cpu")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def environment(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["PipesPipeTargetParametersEcsTaskParametersOverridesContainerOverrideEnvironment"]]]:
        '''environment block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#environment PipesPipe#environment}
        '''
        result = self._values.get("environment")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["PipesPipeTargetParametersEcsTaskParametersOverridesContainerOverrideEnvironment"]]], result)

    @builtins.property
    def environment_file(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["PipesPipeTargetParametersEcsTaskParametersOverridesContainerOverrideEnvironmentFile"]]]:
        '''environment_file block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#environment_file PipesPipe#environment_file}
        '''
        result = self._values.get("environment_file")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["PipesPipeTargetParametersEcsTaskParametersOverridesContainerOverrideEnvironmentFile"]]], result)

    @builtins.property
    def memory(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#memory PipesPipe#memory}.'''
        result = self._values.get("memory")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def memory_reservation(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#memory_reservation PipesPipe#memory_reservation}.'''
        result = self._values.get("memory_reservation")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#name PipesPipe#name}.'''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def resource_requirement(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["PipesPipeTargetParametersEcsTaskParametersOverridesContainerOverrideResourceRequirement"]]]:
        '''resource_requirement block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#resource_requirement PipesPipe#resource_requirement}
        '''
        result = self._values.get("resource_requirement")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["PipesPipeTargetParametersEcsTaskParametersOverridesContainerOverrideResourceRequirement"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PipesPipeTargetParametersEcsTaskParametersOverridesContainerOverride(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.pipesPipe.PipesPipeTargetParametersEcsTaskParametersOverridesContainerOverrideEnvironment",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "value": "value"},
)
class PipesPipeTargetParametersEcsTaskParametersOverridesContainerOverrideEnvironment:
    def __init__(
        self,
        *,
        name: typing.Optional[builtins.str] = None,
        value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#name PipesPipe#name}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#value PipesPipe#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9c353db5b3df47a752e90aae20866fd5fd10669aed355d1c1ecb7bc24ba2756c)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if name is not None:
            self._values["name"] = name
        if value is not None:
            self._values["value"] = value

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#name PipesPipe#name}.'''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def value(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#value PipesPipe#value}.'''
        result = self._values.get("value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PipesPipeTargetParametersEcsTaskParametersOverridesContainerOverrideEnvironment(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.pipesPipe.PipesPipeTargetParametersEcsTaskParametersOverridesContainerOverrideEnvironmentFile",
    jsii_struct_bases=[],
    name_mapping={"type": "type", "value": "value"},
)
class PipesPipeTargetParametersEcsTaskParametersOverridesContainerOverrideEnvironmentFile:
    def __init__(self, *, type: builtins.str, value: builtins.str) -> None:
        '''
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#type PipesPipe#type}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#value PipesPipe#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7deb8e4dfd5859a3031fca249e11f3088592b23f16b8133ad50aa72c08adc50d)
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "type": type,
            "value": value,
        }

    @builtins.property
    def type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#type PipesPipe#type}.'''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#value PipesPipe#value}.'''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PipesPipeTargetParametersEcsTaskParametersOverridesContainerOverrideEnvironmentFile(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PipesPipeTargetParametersEcsTaskParametersOverridesContainerOverrideEnvironmentFileList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.pipesPipe.PipesPipeTargetParametersEcsTaskParametersOverridesContainerOverrideEnvironmentFileList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__94f419e6e3fa8ebd2b5732191be59454ea01ea4f75baca95d4e4bead5ce58a1b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "PipesPipeTargetParametersEcsTaskParametersOverridesContainerOverrideEnvironmentFileOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__171a4d9d334fe5e961b6302a4beb70043862c7329d14acb5cd92061b4e503030)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("PipesPipeTargetParametersEcsTaskParametersOverridesContainerOverrideEnvironmentFileOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__94faab71442c52ad68de5f4e3f1065630c73b03159f7fa61a2a28386f1f8781a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0f336010c6a0fea2d9d2a822db427163e0d4888dad33445c76cd36a114b873ef)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1c2adc133b14399ec7b828e00d3cc0cf7bd859d42ac1fca3c73507b80530a3d8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PipesPipeTargetParametersEcsTaskParametersOverridesContainerOverrideEnvironmentFile]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PipesPipeTargetParametersEcsTaskParametersOverridesContainerOverrideEnvironmentFile]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PipesPipeTargetParametersEcsTaskParametersOverridesContainerOverrideEnvironmentFile]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d8868e9d9d8b4930ea67f68896c9ed11cb3a99ebd6001757fcafba1ac70d49f0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class PipesPipeTargetParametersEcsTaskParametersOverridesContainerOverrideEnvironmentFileOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.pipesPipe.PipesPipeTargetParametersEcsTaskParametersOverridesContainerOverrideEnvironmentFileOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7142b71b5f0fdd9bd3cbef94ede6669af2a7a5611b4ce1e5294427ae37b64a4e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f8f65f007ba1aed2a9aa4815c040a413ee543953f27ad152e866df149ea9bfc1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d102aa1b25f663bf183f20e7f43ae8d50c481ff19925e4a839885d74cd33864)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PipesPipeTargetParametersEcsTaskParametersOverridesContainerOverrideEnvironmentFile]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PipesPipeTargetParametersEcsTaskParametersOverridesContainerOverrideEnvironmentFile]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PipesPipeTargetParametersEcsTaskParametersOverridesContainerOverrideEnvironmentFile]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d5e70d4955e41feb522f3841b6b841680da7abea163b687d0e7da95dda3b6ea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class PipesPipeTargetParametersEcsTaskParametersOverridesContainerOverrideEnvironmentList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.pipesPipe.PipesPipeTargetParametersEcsTaskParametersOverridesContainerOverrideEnvironmentList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__064f733ac9292aec1474dced67f351bf85804e4342c3efcc3bab21bc68e8ee68)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "PipesPipeTargetParametersEcsTaskParametersOverridesContainerOverrideEnvironmentOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__085d22c9be9a58afb9d26429b1a52f0300436da0694c6fa31316a9f4bc2f142b)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("PipesPipeTargetParametersEcsTaskParametersOverridesContainerOverrideEnvironmentOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d2bb51a19fe9d987ef78536f65132cf79728d2acda490ca43286769250b7434)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2898044a7ba2ccd596bd9e397bf8c863f8fa3e0ccb7fe75d53de84c16674d5a5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__18fb433a4b05b9e426a8fb07fff590027cbefc36e4b32e9152f5b7bcaed6ae84)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PipesPipeTargetParametersEcsTaskParametersOverridesContainerOverrideEnvironment]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PipesPipeTargetParametersEcsTaskParametersOverridesContainerOverrideEnvironment]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PipesPipeTargetParametersEcsTaskParametersOverridesContainerOverrideEnvironment]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__06585f411ff2824a114fa02925c7f9306f6de4ea1184ca2fb2ea0431ab2dc61b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class PipesPipeTargetParametersEcsTaskParametersOverridesContainerOverrideEnvironmentOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.pipesPipe.PipesPipeTargetParametersEcsTaskParametersOverridesContainerOverrideEnvironmentOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8b1f75268dafbfbba1e51309d15037cbf89de6b93d603ee0405507e68d0c4615)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @jsii.member(jsii_name="resetValue")
    def reset_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetValue", []))

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
            type_hints = typing.get_type_hints(_typecheckingstub__630349e5bf2f6489c741f0bd6c8492d85adc978969dbcb466fdc0a04f73930e9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ef804e773760530113fd1f001eb735b268056e2abffb7a2e4b0c330edcdd94f6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PipesPipeTargetParametersEcsTaskParametersOverridesContainerOverrideEnvironment]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PipesPipeTargetParametersEcsTaskParametersOverridesContainerOverrideEnvironment]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PipesPipeTargetParametersEcsTaskParametersOverridesContainerOverrideEnvironment]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__206b7e37f6ad5103621c4c0aad8f267a1ef2280b1e6e88626ab35b59b7f84cee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class PipesPipeTargetParametersEcsTaskParametersOverridesContainerOverrideList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.pipesPipe.PipesPipeTargetParametersEcsTaskParametersOverridesContainerOverrideList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__94f54d1ddc2282f1973f5fa55036a47d25714e709e300e41b82b6a11e9204289)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "PipesPipeTargetParametersEcsTaskParametersOverridesContainerOverrideOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a09a9a350509602679170b6abad44345b58ff85e3f42c2de31dda53e8c36f06f)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("PipesPipeTargetParametersEcsTaskParametersOverridesContainerOverrideOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__53ff8a32807818312d89ec45983c87d40ce00b49e179fb872d3d717a8d9cac48)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5230b63083b46b01d19265e8ffdb3912c6f5f6c61771f27b7882864677fbb733)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2e45344d2406b91b732fbb506566e50304738cd32cf626a24b628a7d053e35b5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PipesPipeTargetParametersEcsTaskParametersOverridesContainerOverride]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PipesPipeTargetParametersEcsTaskParametersOverridesContainerOverride]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PipesPipeTargetParametersEcsTaskParametersOverridesContainerOverride]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__714386a7c8b05d6c449494c79f228dd9dec206eeabb4355ecfc0afb51ad68e96)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class PipesPipeTargetParametersEcsTaskParametersOverridesContainerOverrideOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.pipesPipe.PipesPipeTargetParametersEcsTaskParametersOverridesContainerOverrideOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a0fa5834778a6a75cfd2aacf8b39ce4b681b9ef5c5033068d1bd5b74527b37e6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putEnvironment")
    def put_environment(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[PipesPipeTargetParametersEcsTaskParametersOverridesContainerOverrideEnvironment, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7de78d9cd508ac7c0084aa292b8e344cb97fcc278f8fbddbd5c74da1b848e966)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putEnvironment", [value]))

    @jsii.member(jsii_name="putEnvironmentFile")
    def put_environment_file(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[PipesPipeTargetParametersEcsTaskParametersOverridesContainerOverrideEnvironmentFile, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3bc0fd450a5a6805d75cd917e2a95a953ce08278d8cbc97821052e6d1dd6d869)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putEnvironmentFile", [value]))

    @jsii.member(jsii_name="putResourceRequirement")
    def put_resource_requirement(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["PipesPipeTargetParametersEcsTaskParametersOverridesContainerOverrideResourceRequirement", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1abf6a3f887999f97cefdcc6fd4b012c63eda956ae94080797dd7f1386b3ee15)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putResourceRequirement", [value]))

    @jsii.member(jsii_name="resetCommand")
    def reset_command(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCommand", []))

    @jsii.member(jsii_name="resetCpu")
    def reset_cpu(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCpu", []))

    @jsii.member(jsii_name="resetEnvironment")
    def reset_environment(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnvironment", []))

    @jsii.member(jsii_name="resetEnvironmentFile")
    def reset_environment_file(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnvironmentFile", []))

    @jsii.member(jsii_name="resetMemory")
    def reset_memory(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMemory", []))

    @jsii.member(jsii_name="resetMemoryReservation")
    def reset_memory_reservation(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMemoryReservation", []))

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @jsii.member(jsii_name="resetResourceRequirement")
    def reset_resource_requirement(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetResourceRequirement", []))

    @builtins.property
    @jsii.member(jsii_name="environment")
    def environment(
        self,
    ) -> PipesPipeTargetParametersEcsTaskParametersOverridesContainerOverrideEnvironmentList:
        return typing.cast(PipesPipeTargetParametersEcsTaskParametersOverridesContainerOverrideEnvironmentList, jsii.get(self, "environment"))

    @builtins.property
    @jsii.member(jsii_name="environmentFile")
    def environment_file(
        self,
    ) -> PipesPipeTargetParametersEcsTaskParametersOverridesContainerOverrideEnvironmentFileList:
        return typing.cast(PipesPipeTargetParametersEcsTaskParametersOverridesContainerOverrideEnvironmentFileList, jsii.get(self, "environmentFile"))

    @builtins.property
    @jsii.member(jsii_name="resourceRequirement")
    def resource_requirement(
        self,
    ) -> "PipesPipeTargetParametersEcsTaskParametersOverridesContainerOverrideResourceRequirementList":
        return typing.cast("PipesPipeTargetParametersEcsTaskParametersOverridesContainerOverrideResourceRequirementList", jsii.get(self, "resourceRequirement"))

    @builtins.property
    @jsii.member(jsii_name="commandInput")
    def command_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "commandInput"))

    @builtins.property
    @jsii.member(jsii_name="cpuInput")
    def cpu_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "cpuInput"))

    @builtins.property
    @jsii.member(jsii_name="environmentFileInput")
    def environment_file_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PipesPipeTargetParametersEcsTaskParametersOverridesContainerOverrideEnvironmentFile]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PipesPipeTargetParametersEcsTaskParametersOverridesContainerOverrideEnvironmentFile]]], jsii.get(self, "environmentFileInput"))

    @builtins.property
    @jsii.member(jsii_name="environmentInput")
    def environment_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PipesPipeTargetParametersEcsTaskParametersOverridesContainerOverrideEnvironment]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PipesPipeTargetParametersEcsTaskParametersOverridesContainerOverrideEnvironment]]], jsii.get(self, "environmentInput"))

    @builtins.property
    @jsii.member(jsii_name="memoryInput")
    def memory_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "memoryInput"))

    @builtins.property
    @jsii.member(jsii_name="memoryReservationInput")
    def memory_reservation_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "memoryReservationInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceRequirementInput")
    def resource_requirement_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["PipesPipeTargetParametersEcsTaskParametersOverridesContainerOverrideResourceRequirement"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["PipesPipeTargetParametersEcsTaskParametersOverridesContainerOverrideResourceRequirement"]]], jsii.get(self, "resourceRequirementInput"))

    @builtins.property
    @jsii.member(jsii_name="command")
    def command(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "command"))

    @command.setter
    def command(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1269eb602d369e9f050b9999bcd760cfd04178505b132b5c13ef4093dea82e61)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "command", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="cpu")
    def cpu(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "cpu"))

    @cpu.setter
    def cpu(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a90c7f785101d0163b95623601c96aec77b40bf44f0568563a6b8522c771a3be)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cpu", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="memory")
    def memory(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "memory"))

    @memory.setter
    def memory(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e8770f8935dc7a48778e30b98b70df4945eb537351360e915016db6a336fc1c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "memory", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="memoryReservation")
    def memory_reservation(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "memoryReservation"))

    @memory_reservation.setter
    def memory_reservation(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__31e55bdf82d2c8a33126daa37290e2b8780bf69710003825e916d58bcc2f2142)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "memoryReservation", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b3c0a25c3796398524e655208ff97088c582255424e92e6b890d3c90919148ef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PipesPipeTargetParametersEcsTaskParametersOverridesContainerOverride]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PipesPipeTargetParametersEcsTaskParametersOverridesContainerOverride]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PipesPipeTargetParametersEcsTaskParametersOverridesContainerOverride]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__997b7d29c11cb74588d178a73f03cd1f6c640354495b37e3f80c03dc2f3ca7f7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.pipesPipe.PipesPipeTargetParametersEcsTaskParametersOverridesContainerOverrideResourceRequirement",
    jsii_struct_bases=[],
    name_mapping={"type": "type", "value": "value"},
)
class PipesPipeTargetParametersEcsTaskParametersOverridesContainerOverrideResourceRequirement:
    def __init__(self, *, type: builtins.str, value: builtins.str) -> None:
        '''
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#type PipesPipe#type}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#value PipesPipe#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e30058607c59693a8c3f51b72d14ab763d9b9a19ef7ca22cf9f75993af55c74)
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "type": type,
            "value": value,
        }

    @builtins.property
    def type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#type PipesPipe#type}.'''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#value PipesPipe#value}.'''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PipesPipeTargetParametersEcsTaskParametersOverridesContainerOverrideResourceRequirement(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PipesPipeTargetParametersEcsTaskParametersOverridesContainerOverrideResourceRequirementList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.pipesPipe.PipesPipeTargetParametersEcsTaskParametersOverridesContainerOverrideResourceRequirementList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5713faf23bb840afa9a131eaa6266aec0fde67a0444755c5dce45512b9ac33de)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "PipesPipeTargetParametersEcsTaskParametersOverridesContainerOverrideResourceRequirementOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__953e5cdec6ecdbcb26ba26f9cb13e04c700a36e1d6d49eb14e594c4ad8152f72)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("PipesPipeTargetParametersEcsTaskParametersOverridesContainerOverrideResourceRequirementOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__71d0240dce2705bf639e38ba45b698149e7ca9190492a4b923beaeecc1b8232c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d7ca3881a1dbf8373a07adb5f87c0d4a3ea28c43fd103faa6bf5b8cb843eb20e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__54787da8d5e2312046feb8af74fc917c19a3eef65d4388238c40298b04285e04)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PipesPipeTargetParametersEcsTaskParametersOverridesContainerOverrideResourceRequirement]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PipesPipeTargetParametersEcsTaskParametersOverridesContainerOverrideResourceRequirement]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PipesPipeTargetParametersEcsTaskParametersOverridesContainerOverrideResourceRequirement]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8378673f965d446c523440fafe1752605ea9dc32a0b3e1728d4c89b888dbbca7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class PipesPipeTargetParametersEcsTaskParametersOverridesContainerOverrideResourceRequirementOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.pipesPipe.PipesPipeTargetParametersEcsTaskParametersOverridesContainerOverrideResourceRequirementOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3f3cc298218a7b0398bdcfd7151f006eb12d854fd7419f29c48c7e5b36823559)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__04cf999030e5679afc7f124cd680ae3ef43649c2813e4cef07d25e372b1a15a6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f4fa382640bfa858879e04f8a59d9910c18f1455d5a296a002733790db33773)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PipesPipeTargetParametersEcsTaskParametersOverridesContainerOverrideResourceRequirement]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PipesPipeTargetParametersEcsTaskParametersOverridesContainerOverrideResourceRequirement]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PipesPipeTargetParametersEcsTaskParametersOverridesContainerOverrideResourceRequirement]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f95c8a62c40ad486de1dcb3df6982222f15664895eb28714bbe0f6222832cdff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.pipesPipe.PipesPipeTargetParametersEcsTaskParametersOverridesEphemeralStorage",
    jsii_struct_bases=[],
    name_mapping={"size_in_gib": "sizeInGib"},
)
class PipesPipeTargetParametersEcsTaskParametersOverridesEphemeralStorage:
    def __init__(self, *, size_in_gib: jsii.Number) -> None:
        '''
        :param size_in_gib: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#size_in_gib PipesPipe#size_in_gib}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__04943886594d4324b4399e634b207c085c2d38d5fe78996f2f3a9eff03824595)
            check_type(argname="argument size_in_gib", value=size_in_gib, expected_type=type_hints["size_in_gib"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "size_in_gib": size_in_gib,
        }

    @builtins.property
    def size_in_gib(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#size_in_gib PipesPipe#size_in_gib}.'''
        result = self._values.get("size_in_gib")
        assert result is not None, "Required property 'size_in_gib' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PipesPipeTargetParametersEcsTaskParametersOverridesEphemeralStorage(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PipesPipeTargetParametersEcsTaskParametersOverridesEphemeralStorageOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.pipesPipe.PipesPipeTargetParametersEcsTaskParametersOverridesEphemeralStorageOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e4727baec25cfeaa289a12f9e49fa7cee012834882e2f3c5de5e296f47c0a316)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="sizeInGibInput")
    def size_in_gib_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "sizeInGibInput"))

    @builtins.property
    @jsii.member(jsii_name="sizeInGib")
    def size_in_gib(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "sizeInGib"))

    @size_in_gib.setter
    def size_in_gib(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d521518619ad80499293a05b5601c4c2a5aba0f0b7e38e684230de299df30e07)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sizeInGib", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[PipesPipeTargetParametersEcsTaskParametersOverridesEphemeralStorage]:
        return typing.cast(typing.Optional[PipesPipeTargetParametersEcsTaskParametersOverridesEphemeralStorage], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[PipesPipeTargetParametersEcsTaskParametersOverridesEphemeralStorage],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__41ff7ec93b0ccc21fd86b7134f2303997ad2b720de382633613d0717d1df5f48)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.pipesPipe.PipesPipeTargetParametersEcsTaskParametersOverridesInferenceAcceleratorOverride",
    jsii_struct_bases=[],
    name_mapping={"device_name": "deviceName", "device_type": "deviceType"},
)
class PipesPipeTargetParametersEcsTaskParametersOverridesInferenceAcceleratorOverride:
    def __init__(
        self,
        *,
        device_name: typing.Optional[builtins.str] = None,
        device_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param device_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#device_name PipesPipe#device_name}.
        :param device_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#device_type PipesPipe#device_type}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__30addbea279eec224a18bc4bee6c2d6bd9ad2e103daa5285198eee69ef73de11)
            check_type(argname="argument device_name", value=device_name, expected_type=type_hints["device_name"])
            check_type(argname="argument device_type", value=device_type, expected_type=type_hints["device_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if device_name is not None:
            self._values["device_name"] = device_name
        if device_type is not None:
            self._values["device_type"] = device_type

    @builtins.property
    def device_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#device_name PipesPipe#device_name}.'''
        result = self._values.get("device_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def device_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#device_type PipesPipe#device_type}.'''
        result = self._values.get("device_type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PipesPipeTargetParametersEcsTaskParametersOverridesInferenceAcceleratorOverride(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PipesPipeTargetParametersEcsTaskParametersOverridesInferenceAcceleratorOverrideList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.pipesPipe.PipesPipeTargetParametersEcsTaskParametersOverridesInferenceAcceleratorOverrideList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c08cc0fd4e58cfa2e3ab599fff4a6dd826c8fe3dd703613e960d9189aa4038a0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "PipesPipeTargetParametersEcsTaskParametersOverridesInferenceAcceleratorOverrideOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d145520feaa137e3cf5488cc3dd51f9ccbe48662af5a15532c068134c00e7720)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("PipesPipeTargetParametersEcsTaskParametersOverridesInferenceAcceleratorOverrideOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__836c76c83e62e63598e0d6a73ce6f6cb0f976db1c29e36cabaf97b80a5e1b0d5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a6db8c6839789aa4628079ee92b2daea3958fbf0f19647d08f8224f899735ddc)
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
            type_hints = typing.get_type_hints(_typecheckingstub__edf8d0d49732d10ce0933e45aaec4123f81531c2df6f305b88752b441318230a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PipesPipeTargetParametersEcsTaskParametersOverridesInferenceAcceleratorOverride]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PipesPipeTargetParametersEcsTaskParametersOverridesInferenceAcceleratorOverride]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PipesPipeTargetParametersEcsTaskParametersOverridesInferenceAcceleratorOverride]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3cd3bab2ab762e977caced576f0be223df12c0068100926c8930e9bc03272551)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class PipesPipeTargetParametersEcsTaskParametersOverridesInferenceAcceleratorOverrideOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.pipesPipe.PipesPipeTargetParametersEcsTaskParametersOverridesInferenceAcceleratorOverrideOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__393baf92f942c6546ce8fc8ae44ce1ab04820c88de8a44dc4ba4ca47b77b472c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetDeviceName")
    def reset_device_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDeviceName", []))

    @jsii.member(jsii_name="resetDeviceType")
    def reset_device_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDeviceType", []))

    @builtins.property
    @jsii.member(jsii_name="deviceNameInput")
    def device_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "deviceNameInput"))

    @builtins.property
    @jsii.member(jsii_name="deviceTypeInput")
    def device_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "deviceTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="deviceName")
    def device_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "deviceName"))

    @device_name.setter
    def device_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bcf4fc29c04573e9126db13442fbb63778749d030f0d18efd766dc65229ca3c5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deviceName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="deviceType")
    def device_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "deviceType"))

    @device_type.setter
    def device_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__42d02c7242017ba0c87570298e8d7b5035f2ee3078284c0fbfc6835bd30b6762)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deviceType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PipesPipeTargetParametersEcsTaskParametersOverridesInferenceAcceleratorOverride]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PipesPipeTargetParametersEcsTaskParametersOverridesInferenceAcceleratorOverride]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PipesPipeTargetParametersEcsTaskParametersOverridesInferenceAcceleratorOverride]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6589aef7566f0c5a6213b2d973c4c3c62f1164a94dacc5be21f0b3dbaec08010)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class PipesPipeTargetParametersEcsTaskParametersOverridesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.pipesPipe.PipesPipeTargetParametersEcsTaskParametersOverridesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__03bc2f6c84da3d493bb55275b939525c59b3379d5f463f50ccab036b1b65228b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putContainerOverride")
    def put_container_override(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[PipesPipeTargetParametersEcsTaskParametersOverridesContainerOverride, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f043c37f7d6ad13f402a4bf57a8b2224320b1f9e6e68bd3f6b7d251575e6c6f1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putContainerOverride", [value]))

    @jsii.member(jsii_name="putEphemeralStorage")
    def put_ephemeral_storage(self, *, size_in_gib: jsii.Number) -> None:
        '''
        :param size_in_gib: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#size_in_gib PipesPipe#size_in_gib}.
        '''
        value = PipesPipeTargetParametersEcsTaskParametersOverridesEphemeralStorage(
            size_in_gib=size_in_gib
        )

        return typing.cast(None, jsii.invoke(self, "putEphemeralStorage", [value]))

    @jsii.member(jsii_name="putInferenceAcceleratorOverride")
    def put_inference_accelerator_override(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[PipesPipeTargetParametersEcsTaskParametersOverridesInferenceAcceleratorOverride, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ad99a10d2e4d3c1884e39d227c03dd176e971f679109dee8680f50fa1bc0379)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putInferenceAcceleratorOverride", [value]))

    @jsii.member(jsii_name="resetContainerOverride")
    def reset_container_override(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetContainerOverride", []))

    @jsii.member(jsii_name="resetCpu")
    def reset_cpu(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCpu", []))

    @jsii.member(jsii_name="resetEphemeralStorage")
    def reset_ephemeral_storage(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEphemeralStorage", []))

    @jsii.member(jsii_name="resetExecutionRoleArn")
    def reset_execution_role_arn(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExecutionRoleArn", []))

    @jsii.member(jsii_name="resetInferenceAcceleratorOverride")
    def reset_inference_accelerator_override(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInferenceAcceleratorOverride", []))

    @jsii.member(jsii_name="resetMemory")
    def reset_memory(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMemory", []))

    @jsii.member(jsii_name="resetTaskRoleArn")
    def reset_task_role_arn(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTaskRoleArn", []))

    @builtins.property
    @jsii.member(jsii_name="containerOverride")
    def container_override(
        self,
    ) -> PipesPipeTargetParametersEcsTaskParametersOverridesContainerOverrideList:
        return typing.cast(PipesPipeTargetParametersEcsTaskParametersOverridesContainerOverrideList, jsii.get(self, "containerOverride"))

    @builtins.property
    @jsii.member(jsii_name="ephemeralStorage")
    def ephemeral_storage(
        self,
    ) -> PipesPipeTargetParametersEcsTaskParametersOverridesEphemeralStorageOutputReference:
        return typing.cast(PipesPipeTargetParametersEcsTaskParametersOverridesEphemeralStorageOutputReference, jsii.get(self, "ephemeralStorage"))

    @builtins.property
    @jsii.member(jsii_name="inferenceAcceleratorOverride")
    def inference_accelerator_override(
        self,
    ) -> PipesPipeTargetParametersEcsTaskParametersOverridesInferenceAcceleratorOverrideList:
        return typing.cast(PipesPipeTargetParametersEcsTaskParametersOverridesInferenceAcceleratorOverrideList, jsii.get(self, "inferenceAcceleratorOverride"))

    @builtins.property
    @jsii.member(jsii_name="containerOverrideInput")
    def container_override_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PipesPipeTargetParametersEcsTaskParametersOverridesContainerOverride]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PipesPipeTargetParametersEcsTaskParametersOverridesContainerOverride]]], jsii.get(self, "containerOverrideInput"))

    @builtins.property
    @jsii.member(jsii_name="cpuInput")
    def cpu_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cpuInput"))

    @builtins.property
    @jsii.member(jsii_name="ephemeralStorageInput")
    def ephemeral_storage_input(
        self,
    ) -> typing.Optional[PipesPipeTargetParametersEcsTaskParametersOverridesEphemeralStorage]:
        return typing.cast(typing.Optional[PipesPipeTargetParametersEcsTaskParametersOverridesEphemeralStorage], jsii.get(self, "ephemeralStorageInput"))

    @builtins.property
    @jsii.member(jsii_name="executionRoleArnInput")
    def execution_role_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "executionRoleArnInput"))

    @builtins.property
    @jsii.member(jsii_name="inferenceAcceleratorOverrideInput")
    def inference_accelerator_override_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PipesPipeTargetParametersEcsTaskParametersOverridesInferenceAcceleratorOverride]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PipesPipeTargetParametersEcsTaskParametersOverridesInferenceAcceleratorOverride]]], jsii.get(self, "inferenceAcceleratorOverrideInput"))

    @builtins.property
    @jsii.member(jsii_name="memoryInput")
    def memory_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "memoryInput"))

    @builtins.property
    @jsii.member(jsii_name="taskRoleArnInput")
    def task_role_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "taskRoleArnInput"))

    @builtins.property
    @jsii.member(jsii_name="cpu")
    def cpu(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cpu"))

    @cpu.setter
    def cpu(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__21d2839f9e0d4eca424b7fd69d244d477025ad0c8c5ae928f193c2a7c42f2959)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cpu", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="executionRoleArn")
    def execution_role_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "executionRoleArn"))

    @execution_role_arn.setter
    def execution_role_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f0c45cdaef80ee7930248dadd739ef2fcf6ac4332c7ce809ec3a435b74c975b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "executionRoleArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="memory")
    def memory(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "memory"))

    @memory.setter
    def memory(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__26abb5b65456a46d9d7295253e93a404fb77dec72cf7d9b61a0bc3054b199a57)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "memory", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="taskRoleArn")
    def task_role_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "taskRoleArn"))

    @task_role_arn.setter
    def task_role_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a2ca0ffe7c2dba5760413039bb68ace6a89ef374eec0fa323f090796dc51e749)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "taskRoleArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[PipesPipeTargetParametersEcsTaskParametersOverrides]:
        return typing.cast(typing.Optional[PipesPipeTargetParametersEcsTaskParametersOverrides], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[PipesPipeTargetParametersEcsTaskParametersOverrides],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__673916a154a9584cf9f90d33146195505b895db567bf1617e039f06a52a6f317)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.pipesPipe.PipesPipeTargetParametersEcsTaskParametersPlacementConstraint",
    jsii_struct_bases=[],
    name_mapping={"expression": "expression", "type": "type"},
)
class PipesPipeTargetParametersEcsTaskParametersPlacementConstraint:
    def __init__(
        self,
        *,
        expression: typing.Optional[builtins.str] = None,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param expression: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#expression PipesPipe#expression}.
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#type PipesPipe#type}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__21263f747c2f061b3f5deac8bcbb2b7962a6b2ad8db634d918312d2d5a586f0d)
            check_type(argname="argument expression", value=expression, expected_type=type_hints["expression"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if expression is not None:
            self._values["expression"] = expression
        if type is not None:
            self._values["type"] = type

    @builtins.property
    def expression(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#expression PipesPipe#expression}.'''
        result = self._values.get("expression")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#type PipesPipe#type}.'''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PipesPipeTargetParametersEcsTaskParametersPlacementConstraint(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PipesPipeTargetParametersEcsTaskParametersPlacementConstraintList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.pipesPipe.PipesPipeTargetParametersEcsTaskParametersPlacementConstraintList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c021b6aac1bb0146f4c17b402fbfa9dd716eef60777638b8b2b5367a545cdc23)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "PipesPipeTargetParametersEcsTaskParametersPlacementConstraintOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__754c8c50e22082248f50ba5bfc6c850c185ab40a952105448d658553b0511574)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("PipesPipeTargetParametersEcsTaskParametersPlacementConstraintOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6fed425be2461316b4efaa3722fcc07220576834e469054c5705b1afe58f4290)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1c03698c2c1a0a787505cde1aa3ed6545fad6b21b4d983b324ec7d6cedb78656)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e402ab9f5d81f1ecf08249a4139244713b93482c0755a885bfeb24f854e7acb1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PipesPipeTargetParametersEcsTaskParametersPlacementConstraint]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PipesPipeTargetParametersEcsTaskParametersPlacementConstraint]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PipesPipeTargetParametersEcsTaskParametersPlacementConstraint]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ebe11210f39f01cd15fabba7fa24bd647a8394546638302783cd2032754bd29)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class PipesPipeTargetParametersEcsTaskParametersPlacementConstraintOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.pipesPipe.PipesPipeTargetParametersEcsTaskParametersPlacementConstraintOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__727162056886e8b68a9c2658f62842fffa492fbeebb9da0b1ccb600ff9d52c2f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetExpression")
    def reset_expression(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExpression", []))

    @jsii.member(jsii_name="resetType")
    def reset_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetType", []))

    @builtins.property
    @jsii.member(jsii_name="expressionInput")
    def expression_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "expressionInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="expression")
    def expression(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "expression"))

    @expression.setter
    def expression(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f3e7ea4f0acf8b4c9337813e701e1d7ad2ef2333592e4d31ee5588894b998863)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "expression", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__23ebf930a8deb049d4c375a6571e9ff3ee8076e9233979ad0c5f46bc642bb2e4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PipesPipeTargetParametersEcsTaskParametersPlacementConstraint]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PipesPipeTargetParametersEcsTaskParametersPlacementConstraint]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PipesPipeTargetParametersEcsTaskParametersPlacementConstraint]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a576607aeff5ee59079f8f5ff4e439354a69ba1d4cac8407ccea4e453cc8408)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.pipesPipe.PipesPipeTargetParametersEcsTaskParametersPlacementStrategy",
    jsii_struct_bases=[],
    name_mapping={"field": "field", "type": "type"},
)
class PipesPipeTargetParametersEcsTaskParametersPlacementStrategy:
    def __init__(
        self,
        *,
        field: typing.Optional[builtins.str] = None,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param field: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#field PipesPipe#field}.
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#type PipesPipe#type}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f1e39f2c960c6ec4b3717e0f58fa0dc719d6405af8d8a09c7de11a466ef50b76)
            check_type(argname="argument field", value=field, expected_type=type_hints["field"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if field is not None:
            self._values["field"] = field
        if type is not None:
            self._values["type"] = type

    @builtins.property
    def field(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#field PipesPipe#field}.'''
        result = self._values.get("field")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#type PipesPipe#type}.'''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PipesPipeTargetParametersEcsTaskParametersPlacementStrategy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PipesPipeTargetParametersEcsTaskParametersPlacementStrategyList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.pipesPipe.PipesPipeTargetParametersEcsTaskParametersPlacementStrategyList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__108ce08b5dec3855d3ec449d097dc7a4a99b3c73aa1670c84d0ed2c0e206eae2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "PipesPipeTargetParametersEcsTaskParametersPlacementStrategyOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a2d5324b0f2b134a3b517bef1d23eda5d6090ed7b18a6fc8f3b7ce7bd539be79)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("PipesPipeTargetParametersEcsTaskParametersPlacementStrategyOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd694b286a30c7321fdb0f05cbc62ce6fd363903e0aa9d4d7739d85b292ec99a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8c2b28405d4da6f758a13123705a075ec144310bbc605ec45b8110c1e59120ed)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a26d8b316555609a0c2163d831764b69b3cca50cb59371e3c269c95db6eb353b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PipesPipeTargetParametersEcsTaskParametersPlacementStrategy]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PipesPipeTargetParametersEcsTaskParametersPlacementStrategy]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PipesPipeTargetParametersEcsTaskParametersPlacementStrategy]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__944ca590a32e389ea0fd8061c2cbe1d4431e7efc3dea58f673c961e101b91358)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class PipesPipeTargetParametersEcsTaskParametersPlacementStrategyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.pipesPipe.PipesPipeTargetParametersEcsTaskParametersPlacementStrategyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__aab9e3b3fd42c12881aa8baa2f26a35354869a16eff745486de996d4bf2f21e3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetField")
    def reset_field(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetField", []))

    @jsii.member(jsii_name="resetType")
    def reset_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetType", []))

    @builtins.property
    @jsii.member(jsii_name="fieldInput")
    def field_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "fieldInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="field")
    def field(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "field"))

    @field.setter
    def field(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8c45248b0c7839c3f57c994201982c922431d4f53b9144bde001f918a7e730b3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "field", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e49769fe77e3bce7a6abeeef5162f260a46675c95f33b3700e1795e25fade98)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PipesPipeTargetParametersEcsTaskParametersPlacementStrategy]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PipesPipeTargetParametersEcsTaskParametersPlacementStrategy]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PipesPipeTargetParametersEcsTaskParametersPlacementStrategy]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__95956394b91e5a0be0098b88d9d514b85a934b078be7e5619de03ddafa96840b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.pipesPipe.PipesPipeTargetParametersEventbridgeEventBusParameters",
    jsii_struct_bases=[],
    name_mapping={
        "detail_type": "detailType",
        "endpoint_id": "endpointId",
        "resources": "resources",
        "source": "source",
        "time": "time",
    },
)
class PipesPipeTargetParametersEventbridgeEventBusParameters:
    def __init__(
        self,
        *,
        detail_type: typing.Optional[builtins.str] = None,
        endpoint_id: typing.Optional[builtins.str] = None,
        resources: typing.Optional[typing.Sequence[builtins.str]] = None,
        source: typing.Optional[builtins.str] = None,
        time: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param detail_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#detail_type PipesPipe#detail_type}.
        :param endpoint_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#endpoint_id PipesPipe#endpoint_id}.
        :param resources: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#resources PipesPipe#resources}.
        :param source: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#source PipesPipe#source}.
        :param time: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#time PipesPipe#time}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ceb20f73aaf0c1f8e98a651471be42a8e1403056b2ea308bec4ebaca40bbde9b)
            check_type(argname="argument detail_type", value=detail_type, expected_type=type_hints["detail_type"])
            check_type(argname="argument endpoint_id", value=endpoint_id, expected_type=type_hints["endpoint_id"])
            check_type(argname="argument resources", value=resources, expected_type=type_hints["resources"])
            check_type(argname="argument source", value=source, expected_type=type_hints["source"])
            check_type(argname="argument time", value=time, expected_type=type_hints["time"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if detail_type is not None:
            self._values["detail_type"] = detail_type
        if endpoint_id is not None:
            self._values["endpoint_id"] = endpoint_id
        if resources is not None:
            self._values["resources"] = resources
        if source is not None:
            self._values["source"] = source
        if time is not None:
            self._values["time"] = time

    @builtins.property
    def detail_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#detail_type PipesPipe#detail_type}.'''
        result = self._values.get("detail_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def endpoint_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#endpoint_id PipesPipe#endpoint_id}.'''
        result = self._values.get("endpoint_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def resources(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#resources PipesPipe#resources}.'''
        result = self._values.get("resources")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def source(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#source PipesPipe#source}.'''
        result = self._values.get("source")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def time(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#time PipesPipe#time}.'''
        result = self._values.get("time")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PipesPipeTargetParametersEventbridgeEventBusParameters(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PipesPipeTargetParametersEventbridgeEventBusParametersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.pipesPipe.PipesPipeTargetParametersEventbridgeEventBusParametersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__402996c793351fb877e099ed13bebb516ae5ca50d46995acad17c1c5c8e8c693)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetDetailType")
    def reset_detail_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDetailType", []))

    @jsii.member(jsii_name="resetEndpointId")
    def reset_endpoint_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEndpointId", []))

    @jsii.member(jsii_name="resetResources")
    def reset_resources(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetResources", []))

    @jsii.member(jsii_name="resetSource")
    def reset_source(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSource", []))

    @jsii.member(jsii_name="resetTime")
    def reset_time(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTime", []))

    @builtins.property
    @jsii.member(jsii_name="detailTypeInput")
    def detail_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "detailTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="endpointIdInput")
    def endpoint_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "endpointIdInput"))

    @builtins.property
    @jsii.member(jsii_name="resourcesInput")
    def resources_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "resourcesInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceInput")
    def source_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sourceInput"))

    @builtins.property
    @jsii.member(jsii_name="timeInput")
    def time_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "timeInput"))

    @builtins.property
    @jsii.member(jsii_name="detailType")
    def detail_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "detailType"))

    @detail_type.setter
    def detail_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9924d4102e67dc715f8bb758ee85f54383601e355f8524912b72af161ab722d6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "detailType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="endpointId")
    def endpoint_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "endpointId"))

    @endpoint_id.setter
    def endpoint_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f82c6484924709997eafa792ad9af99cef082d0aa8bde6ef3db2db000e721db8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "endpointId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resources")
    def resources(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "resources"))

    @resources.setter
    def resources(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3085112edb69d2139df5f426c3088f8688b9d6ffc59a2d1b0dfb83250650e58a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resources", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="source")
    def source(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "source"))

    @source.setter
    def source(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4253f82bcdeb368906945b7fcb2fde96811ade2eda8fa7b9c62ffad9b018c16d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "source", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="time")
    def time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "time"))

    @time.setter
    def time(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5dc2c46d471f289d976fa06b8ff331afe7c1cefdfd9207b990f4c44272d79f18)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "time", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[PipesPipeTargetParametersEventbridgeEventBusParameters]:
        return typing.cast(typing.Optional[PipesPipeTargetParametersEventbridgeEventBusParameters], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[PipesPipeTargetParametersEventbridgeEventBusParameters],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__67f499567f73bd7d7526409a032a22ce92337be868f252469f830bbdf6bdcf5e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.pipesPipe.PipesPipeTargetParametersHttpParameters",
    jsii_struct_bases=[],
    name_mapping={
        "header_parameters": "headerParameters",
        "path_parameter_values": "pathParameterValues",
        "query_string_parameters": "queryStringParameters",
    },
)
class PipesPipeTargetParametersHttpParameters:
    def __init__(
        self,
        *,
        header_parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        path_parameter_values: typing.Optional[typing.Sequence[builtins.str]] = None,
        query_string_parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param header_parameters: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#header_parameters PipesPipe#header_parameters}.
        :param path_parameter_values: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#path_parameter_values PipesPipe#path_parameter_values}.
        :param query_string_parameters: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#query_string_parameters PipesPipe#query_string_parameters}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a53c08ddfee005f4c6c9be762197b0f7ba0d61f1d74234d37698197972c18453)
            check_type(argname="argument header_parameters", value=header_parameters, expected_type=type_hints["header_parameters"])
            check_type(argname="argument path_parameter_values", value=path_parameter_values, expected_type=type_hints["path_parameter_values"])
            check_type(argname="argument query_string_parameters", value=query_string_parameters, expected_type=type_hints["query_string_parameters"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if header_parameters is not None:
            self._values["header_parameters"] = header_parameters
        if path_parameter_values is not None:
            self._values["path_parameter_values"] = path_parameter_values
        if query_string_parameters is not None:
            self._values["query_string_parameters"] = query_string_parameters

    @builtins.property
    def header_parameters(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#header_parameters PipesPipe#header_parameters}.'''
        result = self._values.get("header_parameters")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def path_parameter_values(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#path_parameter_values PipesPipe#path_parameter_values}.'''
        result = self._values.get("path_parameter_values")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def query_string_parameters(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#query_string_parameters PipesPipe#query_string_parameters}.'''
        result = self._values.get("query_string_parameters")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PipesPipeTargetParametersHttpParameters(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PipesPipeTargetParametersHttpParametersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.pipesPipe.PipesPipeTargetParametersHttpParametersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fdab0e20b00e94e757965d41d9cbc6b6284b2b31f9f2fccd840025e4db092451)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetHeaderParameters")
    def reset_header_parameters(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHeaderParameters", []))

    @jsii.member(jsii_name="resetPathParameterValues")
    def reset_path_parameter_values(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPathParameterValues", []))

    @jsii.member(jsii_name="resetQueryStringParameters")
    def reset_query_string_parameters(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetQueryStringParameters", []))

    @builtins.property
    @jsii.member(jsii_name="headerParametersInput")
    def header_parameters_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "headerParametersInput"))

    @builtins.property
    @jsii.member(jsii_name="pathParameterValuesInput")
    def path_parameter_values_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "pathParameterValuesInput"))

    @builtins.property
    @jsii.member(jsii_name="queryStringParametersInput")
    def query_string_parameters_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "queryStringParametersInput"))

    @builtins.property
    @jsii.member(jsii_name="headerParameters")
    def header_parameters(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "headerParameters"))

    @header_parameters.setter
    def header_parameters(
        self,
        value: typing.Mapping[builtins.str, builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__88d0cafca54902b2e6f0eeae0062e25adf146321fb60eb24538e08f1310189ca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "headerParameters", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="pathParameterValues")
    def path_parameter_values(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "pathParameterValues"))

    @path_parameter_values.setter
    def path_parameter_values(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8af7f5c717d366597ae2851c53a75bf648bc3ff71bfd7c7464439167f8125fa3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pathParameterValues", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="queryStringParameters")
    def query_string_parameters(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "queryStringParameters"))

    @query_string_parameters.setter
    def query_string_parameters(
        self,
        value: typing.Mapping[builtins.str, builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__77cc151fbbf2447d3970d037be09b1344e5e379c781cd8590b9afb51e019f671)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "queryStringParameters", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[PipesPipeTargetParametersHttpParameters]:
        return typing.cast(typing.Optional[PipesPipeTargetParametersHttpParameters], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[PipesPipeTargetParametersHttpParameters],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d2e4bc25adf3c8e91dcad8bd77ac1088a1dd507b5915e92353e603c16e131e22)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.pipesPipe.PipesPipeTargetParametersKinesisStreamParameters",
    jsii_struct_bases=[],
    name_mapping={"partition_key": "partitionKey"},
)
class PipesPipeTargetParametersKinesisStreamParameters:
    def __init__(self, *, partition_key: builtins.str) -> None:
        '''
        :param partition_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#partition_key PipesPipe#partition_key}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b8ad854c9fee85d1cf9279680e48cd94c51fa4351d8e3cd2b3bcb84af9be82c)
            check_type(argname="argument partition_key", value=partition_key, expected_type=type_hints["partition_key"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "partition_key": partition_key,
        }

    @builtins.property
    def partition_key(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#partition_key PipesPipe#partition_key}.'''
        result = self._values.get("partition_key")
        assert result is not None, "Required property 'partition_key' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PipesPipeTargetParametersKinesisStreamParameters(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PipesPipeTargetParametersKinesisStreamParametersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.pipesPipe.PipesPipeTargetParametersKinesisStreamParametersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__511ae4c5c514935fbe7373d5468483f1614d551efe080b3b352b412cef23dd24)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="partitionKeyInput")
    def partition_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "partitionKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="partitionKey")
    def partition_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "partitionKey"))

    @partition_key.setter
    def partition_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__951986154bc1899f94b49fadfb756620051a834a82f9ee5d7a5e0e3ac636cc45)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "partitionKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[PipesPipeTargetParametersKinesisStreamParameters]:
        return typing.cast(typing.Optional[PipesPipeTargetParametersKinesisStreamParameters], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[PipesPipeTargetParametersKinesisStreamParameters],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3571a8d6256001855b739cdedd8abed33f06f98f4daabd5de179f3921d1ca7a1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.pipesPipe.PipesPipeTargetParametersLambdaFunctionParameters",
    jsii_struct_bases=[],
    name_mapping={"invocation_type": "invocationType"},
)
class PipesPipeTargetParametersLambdaFunctionParameters:
    def __init__(self, *, invocation_type: builtins.str) -> None:
        '''
        :param invocation_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#invocation_type PipesPipe#invocation_type}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e2c048e988a30e56ad344b92a8690aeeda6b72f0a1682c07b512dd9697845aa9)
            check_type(argname="argument invocation_type", value=invocation_type, expected_type=type_hints["invocation_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "invocation_type": invocation_type,
        }

    @builtins.property
    def invocation_type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#invocation_type PipesPipe#invocation_type}.'''
        result = self._values.get("invocation_type")
        assert result is not None, "Required property 'invocation_type' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PipesPipeTargetParametersLambdaFunctionParameters(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PipesPipeTargetParametersLambdaFunctionParametersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.pipesPipe.PipesPipeTargetParametersLambdaFunctionParametersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9e0f058398315d6843eb18117863f298cee2d2a22e038df3c4243b337cf06aae)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="invocationTypeInput")
    def invocation_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "invocationTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="invocationType")
    def invocation_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "invocationType"))

    @invocation_type.setter
    def invocation_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ed8032ad1fddb9f3f3d9bbf48d253806aad1d5102892472e18a8932ea1aa9d7b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "invocationType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[PipesPipeTargetParametersLambdaFunctionParameters]:
        return typing.cast(typing.Optional[PipesPipeTargetParametersLambdaFunctionParameters], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[PipesPipeTargetParametersLambdaFunctionParameters],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__201ad64e69e9aeb599e02da8e742444c02a888625095d9c5383423b9dcc24c0b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class PipesPipeTargetParametersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.pipesPipe.PipesPipeTargetParametersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f2ca21234829a6f65175c5008140cefad75372153f2503dc37ca1430616bcf38)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putBatchJobParameters")
    def put_batch_job_parameters(
        self,
        *,
        job_definition: builtins.str,
        job_name: builtins.str,
        array_properties: typing.Optional[typing.Union[PipesPipeTargetParametersBatchJobParametersArrayProperties, typing.Dict[builtins.str, typing.Any]]] = None,
        container_overrides: typing.Optional[typing.Union[PipesPipeTargetParametersBatchJobParametersContainerOverrides, typing.Dict[builtins.str, typing.Any]]] = None,
        depends_on: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[PipesPipeTargetParametersBatchJobParametersDependsOn, typing.Dict[builtins.str, typing.Any]]]]] = None,
        parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        retry_strategy: typing.Optional[typing.Union[PipesPipeTargetParametersBatchJobParametersRetryStrategy, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param job_definition: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#job_definition PipesPipe#job_definition}.
        :param job_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#job_name PipesPipe#job_name}.
        :param array_properties: array_properties block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#array_properties PipesPipe#array_properties}
        :param container_overrides: container_overrides block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#container_overrides PipesPipe#container_overrides}
        :param depends_on: depends_on block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#depends_on PipesPipe#depends_on}
        :param parameters: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#parameters PipesPipe#parameters}.
        :param retry_strategy: retry_strategy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#retry_strategy PipesPipe#retry_strategy}
        '''
        value = PipesPipeTargetParametersBatchJobParameters(
            job_definition=job_definition,
            job_name=job_name,
            array_properties=array_properties,
            container_overrides=container_overrides,
            depends_on=depends_on,
            parameters=parameters,
            retry_strategy=retry_strategy,
        )

        return typing.cast(None, jsii.invoke(self, "putBatchJobParameters", [value]))

    @jsii.member(jsii_name="putCloudwatchLogsParameters")
    def put_cloudwatch_logs_parameters(
        self,
        *,
        log_stream_name: typing.Optional[builtins.str] = None,
        timestamp: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param log_stream_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#log_stream_name PipesPipe#log_stream_name}.
        :param timestamp: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#timestamp PipesPipe#timestamp}.
        '''
        value = PipesPipeTargetParametersCloudwatchLogsParameters(
            log_stream_name=log_stream_name, timestamp=timestamp
        )

        return typing.cast(None, jsii.invoke(self, "putCloudwatchLogsParameters", [value]))

    @jsii.member(jsii_name="putEcsTaskParameters")
    def put_ecs_task_parameters(
        self,
        *,
        task_definition_arn: builtins.str,
        capacity_provider_strategy: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[PipesPipeTargetParametersEcsTaskParametersCapacityProviderStrategy, typing.Dict[builtins.str, typing.Any]]]]] = None,
        enable_ecs_managed_tags: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_execute_command: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        group: typing.Optional[builtins.str] = None,
        launch_type: typing.Optional[builtins.str] = None,
        network_configuration: typing.Optional[typing.Union[PipesPipeTargetParametersEcsTaskParametersNetworkConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
        overrides: typing.Optional[typing.Union[PipesPipeTargetParametersEcsTaskParametersOverrides, typing.Dict[builtins.str, typing.Any]]] = None,
        placement_constraint: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[PipesPipeTargetParametersEcsTaskParametersPlacementConstraint, typing.Dict[builtins.str, typing.Any]]]]] = None,
        placement_strategy: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[PipesPipeTargetParametersEcsTaskParametersPlacementStrategy, typing.Dict[builtins.str, typing.Any]]]]] = None,
        platform_version: typing.Optional[builtins.str] = None,
        propagate_tags: typing.Optional[builtins.str] = None,
        reference_id: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        task_count: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param task_definition_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#task_definition_arn PipesPipe#task_definition_arn}.
        :param capacity_provider_strategy: capacity_provider_strategy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#capacity_provider_strategy PipesPipe#capacity_provider_strategy}
        :param enable_ecs_managed_tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#enable_ecs_managed_tags PipesPipe#enable_ecs_managed_tags}.
        :param enable_execute_command: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#enable_execute_command PipesPipe#enable_execute_command}.
        :param group: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#group PipesPipe#group}.
        :param launch_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#launch_type PipesPipe#launch_type}.
        :param network_configuration: network_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#network_configuration PipesPipe#network_configuration}
        :param overrides: overrides block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#overrides PipesPipe#overrides}
        :param placement_constraint: placement_constraint block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#placement_constraint PipesPipe#placement_constraint}
        :param placement_strategy: placement_strategy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#placement_strategy PipesPipe#placement_strategy}
        :param platform_version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#platform_version PipesPipe#platform_version}.
        :param propagate_tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#propagate_tags PipesPipe#propagate_tags}.
        :param reference_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#reference_id PipesPipe#reference_id}.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#tags PipesPipe#tags}.
        :param task_count: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#task_count PipesPipe#task_count}.
        '''
        value = PipesPipeTargetParametersEcsTaskParameters(
            task_definition_arn=task_definition_arn,
            capacity_provider_strategy=capacity_provider_strategy,
            enable_ecs_managed_tags=enable_ecs_managed_tags,
            enable_execute_command=enable_execute_command,
            group=group,
            launch_type=launch_type,
            network_configuration=network_configuration,
            overrides=overrides,
            placement_constraint=placement_constraint,
            placement_strategy=placement_strategy,
            platform_version=platform_version,
            propagate_tags=propagate_tags,
            reference_id=reference_id,
            tags=tags,
            task_count=task_count,
        )

        return typing.cast(None, jsii.invoke(self, "putEcsTaskParameters", [value]))

    @jsii.member(jsii_name="putEventbridgeEventBusParameters")
    def put_eventbridge_event_bus_parameters(
        self,
        *,
        detail_type: typing.Optional[builtins.str] = None,
        endpoint_id: typing.Optional[builtins.str] = None,
        resources: typing.Optional[typing.Sequence[builtins.str]] = None,
        source: typing.Optional[builtins.str] = None,
        time: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param detail_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#detail_type PipesPipe#detail_type}.
        :param endpoint_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#endpoint_id PipesPipe#endpoint_id}.
        :param resources: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#resources PipesPipe#resources}.
        :param source: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#source PipesPipe#source}.
        :param time: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#time PipesPipe#time}.
        '''
        value = PipesPipeTargetParametersEventbridgeEventBusParameters(
            detail_type=detail_type,
            endpoint_id=endpoint_id,
            resources=resources,
            source=source,
            time=time,
        )

        return typing.cast(None, jsii.invoke(self, "putEventbridgeEventBusParameters", [value]))

    @jsii.member(jsii_name="putHttpParameters")
    def put_http_parameters(
        self,
        *,
        header_parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        path_parameter_values: typing.Optional[typing.Sequence[builtins.str]] = None,
        query_string_parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param header_parameters: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#header_parameters PipesPipe#header_parameters}.
        :param path_parameter_values: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#path_parameter_values PipesPipe#path_parameter_values}.
        :param query_string_parameters: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#query_string_parameters PipesPipe#query_string_parameters}.
        '''
        value = PipesPipeTargetParametersHttpParameters(
            header_parameters=header_parameters,
            path_parameter_values=path_parameter_values,
            query_string_parameters=query_string_parameters,
        )

        return typing.cast(None, jsii.invoke(self, "putHttpParameters", [value]))

    @jsii.member(jsii_name="putKinesisStreamParameters")
    def put_kinesis_stream_parameters(self, *, partition_key: builtins.str) -> None:
        '''
        :param partition_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#partition_key PipesPipe#partition_key}.
        '''
        value = PipesPipeTargetParametersKinesisStreamParameters(
            partition_key=partition_key
        )

        return typing.cast(None, jsii.invoke(self, "putKinesisStreamParameters", [value]))

    @jsii.member(jsii_name="putLambdaFunctionParameters")
    def put_lambda_function_parameters(self, *, invocation_type: builtins.str) -> None:
        '''
        :param invocation_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#invocation_type PipesPipe#invocation_type}.
        '''
        value = PipesPipeTargetParametersLambdaFunctionParameters(
            invocation_type=invocation_type
        )

        return typing.cast(None, jsii.invoke(self, "putLambdaFunctionParameters", [value]))

    @jsii.member(jsii_name="putRedshiftDataParameters")
    def put_redshift_data_parameters(
        self,
        *,
        database: builtins.str,
        sqls: typing.Sequence[builtins.str],
        db_user: typing.Optional[builtins.str] = None,
        secret_manager_arn: typing.Optional[builtins.str] = None,
        statement_name: typing.Optional[builtins.str] = None,
        with_event: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param database: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#database PipesPipe#database}.
        :param sqls: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#sqls PipesPipe#sqls}.
        :param db_user: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#db_user PipesPipe#db_user}.
        :param secret_manager_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#secret_manager_arn PipesPipe#secret_manager_arn}.
        :param statement_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#statement_name PipesPipe#statement_name}.
        :param with_event: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#with_event PipesPipe#with_event}.
        '''
        value = PipesPipeTargetParametersRedshiftDataParameters(
            database=database,
            sqls=sqls,
            db_user=db_user,
            secret_manager_arn=secret_manager_arn,
            statement_name=statement_name,
            with_event=with_event,
        )

        return typing.cast(None, jsii.invoke(self, "putRedshiftDataParameters", [value]))

    @jsii.member(jsii_name="putSagemakerPipelineParameters")
    def put_sagemaker_pipeline_parameters(
        self,
        *,
        pipeline_parameter: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["PipesPipeTargetParametersSagemakerPipelineParametersPipelineParameter", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param pipeline_parameter: pipeline_parameter block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#pipeline_parameter PipesPipe#pipeline_parameter}
        '''
        value = PipesPipeTargetParametersSagemakerPipelineParameters(
            pipeline_parameter=pipeline_parameter
        )

        return typing.cast(None, jsii.invoke(self, "putSagemakerPipelineParameters", [value]))

    @jsii.member(jsii_name="putSqsQueueParameters")
    def put_sqs_queue_parameters(
        self,
        *,
        message_deduplication_id: typing.Optional[builtins.str] = None,
        message_group_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param message_deduplication_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#message_deduplication_id PipesPipe#message_deduplication_id}.
        :param message_group_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#message_group_id PipesPipe#message_group_id}.
        '''
        value = PipesPipeTargetParametersSqsQueueParameters(
            message_deduplication_id=message_deduplication_id,
            message_group_id=message_group_id,
        )

        return typing.cast(None, jsii.invoke(self, "putSqsQueueParameters", [value]))

    @jsii.member(jsii_name="putStepFunctionStateMachineParameters")
    def put_step_function_state_machine_parameters(
        self,
        *,
        invocation_type: builtins.str,
    ) -> None:
        '''
        :param invocation_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#invocation_type PipesPipe#invocation_type}.
        '''
        value = PipesPipeTargetParametersStepFunctionStateMachineParameters(
            invocation_type=invocation_type
        )

        return typing.cast(None, jsii.invoke(self, "putStepFunctionStateMachineParameters", [value]))

    @jsii.member(jsii_name="resetBatchJobParameters")
    def reset_batch_job_parameters(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBatchJobParameters", []))

    @jsii.member(jsii_name="resetCloudwatchLogsParameters")
    def reset_cloudwatch_logs_parameters(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCloudwatchLogsParameters", []))

    @jsii.member(jsii_name="resetEcsTaskParameters")
    def reset_ecs_task_parameters(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEcsTaskParameters", []))

    @jsii.member(jsii_name="resetEventbridgeEventBusParameters")
    def reset_eventbridge_event_bus_parameters(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEventbridgeEventBusParameters", []))

    @jsii.member(jsii_name="resetHttpParameters")
    def reset_http_parameters(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHttpParameters", []))

    @jsii.member(jsii_name="resetInputTemplate")
    def reset_input_template(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInputTemplate", []))

    @jsii.member(jsii_name="resetKinesisStreamParameters")
    def reset_kinesis_stream_parameters(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKinesisStreamParameters", []))

    @jsii.member(jsii_name="resetLambdaFunctionParameters")
    def reset_lambda_function_parameters(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLambdaFunctionParameters", []))

    @jsii.member(jsii_name="resetRedshiftDataParameters")
    def reset_redshift_data_parameters(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRedshiftDataParameters", []))

    @jsii.member(jsii_name="resetSagemakerPipelineParameters")
    def reset_sagemaker_pipeline_parameters(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSagemakerPipelineParameters", []))

    @jsii.member(jsii_name="resetSqsQueueParameters")
    def reset_sqs_queue_parameters(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSqsQueueParameters", []))

    @jsii.member(jsii_name="resetStepFunctionStateMachineParameters")
    def reset_step_function_state_machine_parameters(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStepFunctionStateMachineParameters", []))

    @builtins.property
    @jsii.member(jsii_name="batchJobParameters")
    def batch_job_parameters(
        self,
    ) -> PipesPipeTargetParametersBatchJobParametersOutputReference:
        return typing.cast(PipesPipeTargetParametersBatchJobParametersOutputReference, jsii.get(self, "batchJobParameters"))

    @builtins.property
    @jsii.member(jsii_name="cloudwatchLogsParameters")
    def cloudwatch_logs_parameters(
        self,
    ) -> PipesPipeTargetParametersCloudwatchLogsParametersOutputReference:
        return typing.cast(PipesPipeTargetParametersCloudwatchLogsParametersOutputReference, jsii.get(self, "cloudwatchLogsParameters"))

    @builtins.property
    @jsii.member(jsii_name="ecsTaskParameters")
    def ecs_task_parameters(
        self,
    ) -> PipesPipeTargetParametersEcsTaskParametersOutputReference:
        return typing.cast(PipesPipeTargetParametersEcsTaskParametersOutputReference, jsii.get(self, "ecsTaskParameters"))

    @builtins.property
    @jsii.member(jsii_name="eventbridgeEventBusParameters")
    def eventbridge_event_bus_parameters(
        self,
    ) -> PipesPipeTargetParametersEventbridgeEventBusParametersOutputReference:
        return typing.cast(PipesPipeTargetParametersEventbridgeEventBusParametersOutputReference, jsii.get(self, "eventbridgeEventBusParameters"))

    @builtins.property
    @jsii.member(jsii_name="httpParameters")
    def http_parameters(self) -> PipesPipeTargetParametersHttpParametersOutputReference:
        return typing.cast(PipesPipeTargetParametersHttpParametersOutputReference, jsii.get(self, "httpParameters"))

    @builtins.property
    @jsii.member(jsii_name="kinesisStreamParameters")
    def kinesis_stream_parameters(
        self,
    ) -> PipesPipeTargetParametersKinesisStreamParametersOutputReference:
        return typing.cast(PipesPipeTargetParametersKinesisStreamParametersOutputReference, jsii.get(self, "kinesisStreamParameters"))

    @builtins.property
    @jsii.member(jsii_name="lambdaFunctionParameters")
    def lambda_function_parameters(
        self,
    ) -> PipesPipeTargetParametersLambdaFunctionParametersOutputReference:
        return typing.cast(PipesPipeTargetParametersLambdaFunctionParametersOutputReference, jsii.get(self, "lambdaFunctionParameters"))

    @builtins.property
    @jsii.member(jsii_name="redshiftDataParameters")
    def redshift_data_parameters(
        self,
    ) -> "PipesPipeTargetParametersRedshiftDataParametersOutputReference":
        return typing.cast("PipesPipeTargetParametersRedshiftDataParametersOutputReference", jsii.get(self, "redshiftDataParameters"))

    @builtins.property
    @jsii.member(jsii_name="sagemakerPipelineParameters")
    def sagemaker_pipeline_parameters(
        self,
    ) -> "PipesPipeTargetParametersSagemakerPipelineParametersOutputReference":
        return typing.cast("PipesPipeTargetParametersSagemakerPipelineParametersOutputReference", jsii.get(self, "sagemakerPipelineParameters"))

    @builtins.property
    @jsii.member(jsii_name="sqsQueueParameters")
    def sqs_queue_parameters(
        self,
    ) -> "PipesPipeTargetParametersSqsQueueParametersOutputReference":
        return typing.cast("PipesPipeTargetParametersSqsQueueParametersOutputReference", jsii.get(self, "sqsQueueParameters"))

    @builtins.property
    @jsii.member(jsii_name="stepFunctionStateMachineParameters")
    def step_function_state_machine_parameters(
        self,
    ) -> "PipesPipeTargetParametersStepFunctionStateMachineParametersOutputReference":
        return typing.cast("PipesPipeTargetParametersStepFunctionStateMachineParametersOutputReference", jsii.get(self, "stepFunctionStateMachineParameters"))

    @builtins.property
    @jsii.member(jsii_name="batchJobParametersInput")
    def batch_job_parameters_input(
        self,
    ) -> typing.Optional[PipesPipeTargetParametersBatchJobParameters]:
        return typing.cast(typing.Optional[PipesPipeTargetParametersBatchJobParameters], jsii.get(self, "batchJobParametersInput"))

    @builtins.property
    @jsii.member(jsii_name="cloudwatchLogsParametersInput")
    def cloudwatch_logs_parameters_input(
        self,
    ) -> typing.Optional[PipesPipeTargetParametersCloudwatchLogsParameters]:
        return typing.cast(typing.Optional[PipesPipeTargetParametersCloudwatchLogsParameters], jsii.get(self, "cloudwatchLogsParametersInput"))

    @builtins.property
    @jsii.member(jsii_name="ecsTaskParametersInput")
    def ecs_task_parameters_input(
        self,
    ) -> typing.Optional[PipesPipeTargetParametersEcsTaskParameters]:
        return typing.cast(typing.Optional[PipesPipeTargetParametersEcsTaskParameters], jsii.get(self, "ecsTaskParametersInput"))

    @builtins.property
    @jsii.member(jsii_name="eventbridgeEventBusParametersInput")
    def eventbridge_event_bus_parameters_input(
        self,
    ) -> typing.Optional[PipesPipeTargetParametersEventbridgeEventBusParameters]:
        return typing.cast(typing.Optional[PipesPipeTargetParametersEventbridgeEventBusParameters], jsii.get(self, "eventbridgeEventBusParametersInput"))

    @builtins.property
    @jsii.member(jsii_name="httpParametersInput")
    def http_parameters_input(
        self,
    ) -> typing.Optional[PipesPipeTargetParametersHttpParameters]:
        return typing.cast(typing.Optional[PipesPipeTargetParametersHttpParameters], jsii.get(self, "httpParametersInput"))

    @builtins.property
    @jsii.member(jsii_name="inputTemplateInput")
    def input_template_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "inputTemplateInput"))

    @builtins.property
    @jsii.member(jsii_name="kinesisStreamParametersInput")
    def kinesis_stream_parameters_input(
        self,
    ) -> typing.Optional[PipesPipeTargetParametersKinesisStreamParameters]:
        return typing.cast(typing.Optional[PipesPipeTargetParametersKinesisStreamParameters], jsii.get(self, "kinesisStreamParametersInput"))

    @builtins.property
    @jsii.member(jsii_name="lambdaFunctionParametersInput")
    def lambda_function_parameters_input(
        self,
    ) -> typing.Optional[PipesPipeTargetParametersLambdaFunctionParameters]:
        return typing.cast(typing.Optional[PipesPipeTargetParametersLambdaFunctionParameters], jsii.get(self, "lambdaFunctionParametersInput"))

    @builtins.property
    @jsii.member(jsii_name="redshiftDataParametersInput")
    def redshift_data_parameters_input(
        self,
    ) -> typing.Optional["PipesPipeTargetParametersRedshiftDataParameters"]:
        return typing.cast(typing.Optional["PipesPipeTargetParametersRedshiftDataParameters"], jsii.get(self, "redshiftDataParametersInput"))

    @builtins.property
    @jsii.member(jsii_name="sagemakerPipelineParametersInput")
    def sagemaker_pipeline_parameters_input(
        self,
    ) -> typing.Optional["PipesPipeTargetParametersSagemakerPipelineParameters"]:
        return typing.cast(typing.Optional["PipesPipeTargetParametersSagemakerPipelineParameters"], jsii.get(self, "sagemakerPipelineParametersInput"))

    @builtins.property
    @jsii.member(jsii_name="sqsQueueParametersInput")
    def sqs_queue_parameters_input(
        self,
    ) -> typing.Optional["PipesPipeTargetParametersSqsQueueParameters"]:
        return typing.cast(typing.Optional["PipesPipeTargetParametersSqsQueueParameters"], jsii.get(self, "sqsQueueParametersInput"))

    @builtins.property
    @jsii.member(jsii_name="stepFunctionStateMachineParametersInput")
    def step_function_state_machine_parameters_input(
        self,
    ) -> typing.Optional["PipesPipeTargetParametersStepFunctionStateMachineParameters"]:
        return typing.cast(typing.Optional["PipesPipeTargetParametersStepFunctionStateMachineParameters"], jsii.get(self, "stepFunctionStateMachineParametersInput"))

    @builtins.property
    @jsii.member(jsii_name="inputTemplate")
    def input_template(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "inputTemplate"))

    @input_template.setter
    def input_template(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a03ef4a5195a1a2584c06d5c71b54a65b45577878415bb885984968017eaaa2a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "inputTemplate", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[PipesPipeTargetParameters]:
        return typing.cast(typing.Optional[PipesPipeTargetParameters], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[PipesPipeTargetParameters]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e27205f49fb0e0982a51167a268a3f45a880ca8861af00f6747902b643082765)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.pipesPipe.PipesPipeTargetParametersRedshiftDataParameters",
    jsii_struct_bases=[],
    name_mapping={
        "database": "database",
        "sqls": "sqls",
        "db_user": "dbUser",
        "secret_manager_arn": "secretManagerArn",
        "statement_name": "statementName",
        "with_event": "withEvent",
    },
)
class PipesPipeTargetParametersRedshiftDataParameters:
    def __init__(
        self,
        *,
        database: builtins.str,
        sqls: typing.Sequence[builtins.str],
        db_user: typing.Optional[builtins.str] = None,
        secret_manager_arn: typing.Optional[builtins.str] = None,
        statement_name: typing.Optional[builtins.str] = None,
        with_event: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param database: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#database PipesPipe#database}.
        :param sqls: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#sqls PipesPipe#sqls}.
        :param db_user: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#db_user PipesPipe#db_user}.
        :param secret_manager_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#secret_manager_arn PipesPipe#secret_manager_arn}.
        :param statement_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#statement_name PipesPipe#statement_name}.
        :param with_event: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#with_event PipesPipe#with_event}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d78d05895dcf7c4be41786c64d7407028bb9478d3677dcdd7fa7ba76fa0f77f9)
            check_type(argname="argument database", value=database, expected_type=type_hints["database"])
            check_type(argname="argument sqls", value=sqls, expected_type=type_hints["sqls"])
            check_type(argname="argument db_user", value=db_user, expected_type=type_hints["db_user"])
            check_type(argname="argument secret_manager_arn", value=secret_manager_arn, expected_type=type_hints["secret_manager_arn"])
            check_type(argname="argument statement_name", value=statement_name, expected_type=type_hints["statement_name"])
            check_type(argname="argument with_event", value=with_event, expected_type=type_hints["with_event"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "database": database,
            "sqls": sqls,
        }
        if db_user is not None:
            self._values["db_user"] = db_user
        if secret_manager_arn is not None:
            self._values["secret_manager_arn"] = secret_manager_arn
        if statement_name is not None:
            self._values["statement_name"] = statement_name
        if with_event is not None:
            self._values["with_event"] = with_event

    @builtins.property
    def database(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#database PipesPipe#database}.'''
        result = self._values.get("database")
        assert result is not None, "Required property 'database' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def sqls(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#sqls PipesPipe#sqls}.'''
        result = self._values.get("sqls")
        assert result is not None, "Required property 'sqls' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def db_user(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#db_user PipesPipe#db_user}.'''
        result = self._values.get("db_user")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def secret_manager_arn(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#secret_manager_arn PipesPipe#secret_manager_arn}.'''
        result = self._values.get("secret_manager_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def statement_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#statement_name PipesPipe#statement_name}.'''
        result = self._values.get("statement_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def with_event(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#with_event PipesPipe#with_event}.'''
        result = self._values.get("with_event")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PipesPipeTargetParametersRedshiftDataParameters(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PipesPipeTargetParametersRedshiftDataParametersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.pipesPipe.PipesPipeTargetParametersRedshiftDataParametersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a5ef1e673ecccc48c3c469477ab11c98e5aeb2aa5093fe078077d7f78707b08f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetDbUser")
    def reset_db_user(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDbUser", []))

    @jsii.member(jsii_name="resetSecretManagerArn")
    def reset_secret_manager_arn(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSecretManagerArn", []))

    @jsii.member(jsii_name="resetStatementName")
    def reset_statement_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStatementName", []))

    @jsii.member(jsii_name="resetWithEvent")
    def reset_with_event(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWithEvent", []))

    @builtins.property
    @jsii.member(jsii_name="databaseInput")
    def database_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "databaseInput"))

    @builtins.property
    @jsii.member(jsii_name="dbUserInput")
    def db_user_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dbUserInput"))

    @builtins.property
    @jsii.member(jsii_name="secretManagerArnInput")
    def secret_manager_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "secretManagerArnInput"))

    @builtins.property
    @jsii.member(jsii_name="sqlsInput")
    def sqls_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "sqlsInput"))

    @builtins.property
    @jsii.member(jsii_name="statementNameInput")
    def statement_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "statementNameInput"))

    @builtins.property
    @jsii.member(jsii_name="withEventInput")
    def with_event_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "withEventInput"))

    @builtins.property
    @jsii.member(jsii_name="database")
    def database(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "database"))

    @database.setter
    def database(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__04ed052ccd6a3f1cbd4c514c041887a3e42c037bbcb02cf3ab645327f19bd074)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "database", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dbUser")
    def db_user(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dbUser"))

    @db_user.setter
    def db_user(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5798e15acd72738f1eb1834b1fcbd0c004c4ec6191903175eb238edb722c2052)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dbUser", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="secretManagerArn")
    def secret_manager_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "secretManagerArn"))

    @secret_manager_arn.setter
    def secret_manager_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0d492467f736fb7864cc13e7f1db3263673d56d9156b4f8f7fbbdf9e524d6be2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secretManagerArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sqls")
    def sqls(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "sqls"))

    @sqls.setter
    def sqls(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0e7d1c790c6d3310ac48643810dfd8ec446ddeb460388e9bc12a99654754ed2b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sqls", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="statementName")
    def statement_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "statementName"))

    @statement_name.setter
    def statement_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6920fde12ff3eeefe82ee9090acc7cbb60f5e18deda77f9bbf26ea987fb1d155)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "statementName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="withEvent")
    def with_event(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "withEvent"))

    @with_event.setter
    def with_event(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f69f2da9f4ef917ccae7167145b90a7bca1560eba9577c7b788800653636252)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "withEvent", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[PipesPipeTargetParametersRedshiftDataParameters]:
        return typing.cast(typing.Optional[PipesPipeTargetParametersRedshiftDataParameters], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[PipesPipeTargetParametersRedshiftDataParameters],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a4293d05ba08d13632877bfbcf45e44820e77f44deaa47dd38cdeff6174d519)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.pipesPipe.PipesPipeTargetParametersSagemakerPipelineParameters",
    jsii_struct_bases=[],
    name_mapping={"pipeline_parameter": "pipelineParameter"},
)
class PipesPipeTargetParametersSagemakerPipelineParameters:
    def __init__(
        self,
        *,
        pipeline_parameter: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["PipesPipeTargetParametersSagemakerPipelineParametersPipelineParameter", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param pipeline_parameter: pipeline_parameter block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#pipeline_parameter PipesPipe#pipeline_parameter}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bdfa8c05bd8b0a402d1a770d39e5ab6082f65eab93f6f4d210180b5935010b14)
            check_type(argname="argument pipeline_parameter", value=pipeline_parameter, expected_type=type_hints["pipeline_parameter"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if pipeline_parameter is not None:
            self._values["pipeline_parameter"] = pipeline_parameter

    @builtins.property
    def pipeline_parameter(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["PipesPipeTargetParametersSagemakerPipelineParametersPipelineParameter"]]]:
        '''pipeline_parameter block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#pipeline_parameter PipesPipe#pipeline_parameter}
        '''
        result = self._values.get("pipeline_parameter")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["PipesPipeTargetParametersSagemakerPipelineParametersPipelineParameter"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PipesPipeTargetParametersSagemakerPipelineParameters(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PipesPipeTargetParametersSagemakerPipelineParametersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.pipesPipe.PipesPipeTargetParametersSagemakerPipelineParametersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__74b4bba2c4d69fc20e83d0a2a9944c52a6aa4f784362acaa7351efce5ff1fedc)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putPipelineParameter")
    def put_pipeline_parameter(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["PipesPipeTargetParametersSagemakerPipelineParametersPipelineParameter", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f01e43813226d14d318218365fa7e8f4fe723a1c34d626650af9a0ae2d9b57f2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putPipelineParameter", [value]))

    @jsii.member(jsii_name="resetPipelineParameter")
    def reset_pipeline_parameter(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPipelineParameter", []))

    @builtins.property
    @jsii.member(jsii_name="pipelineParameter")
    def pipeline_parameter(
        self,
    ) -> "PipesPipeTargetParametersSagemakerPipelineParametersPipelineParameterList":
        return typing.cast("PipesPipeTargetParametersSagemakerPipelineParametersPipelineParameterList", jsii.get(self, "pipelineParameter"))

    @builtins.property
    @jsii.member(jsii_name="pipelineParameterInput")
    def pipeline_parameter_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["PipesPipeTargetParametersSagemakerPipelineParametersPipelineParameter"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["PipesPipeTargetParametersSagemakerPipelineParametersPipelineParameter"]]], jsii.get(self, "pipelineParameterInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[PipesPipeTargetParametersSagemakerPipelineParameters]:
        return typing.cast(typing.Optional[PipesPipeTargetParametersSagemakerPipelineParameters], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[PipesPipeTargetParametersSagemakerPipelineParameters],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7d7c8fcf9372dbe0419e0720eec6b8b296292d0ad6aad5460da1eb655d092402)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.pipesPipe.PipesPipeTargetParametersSagemakerPipelineParametersPipelineParameter",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "value": "value"},
)
class PipesPipeTargetParametersSagemakerPipelineParametersPipelineParameter:
    def __init__(self, *, name: builtins.str, value: builtins.str) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#name PipesPipe#name}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#value PipesPipe#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e3d347ae0926e0c8a0e87dd45ecea7f8a6f970bb4303764fe12714f47174a847)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "value": value,
        }

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#name PipesPipe#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#value PipesPipe#value}.'''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PipesPipeTargetParametersSagemakerPipelineParametersPipelineParameter(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PipesPipeTargetParametersSagemakerPipelineParametersPipelineParameterList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.pipesPipe.PipesPipeTargetParametersSagemakerPipelineParametersPipelineParameterList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7be6e7ed9ef3b393b023b7fdf3e4405f6f15dadb366e98b51c094950883c4c22)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "PipesPipeTargetParametersSagemakerPipelineParametersPipelineParameterOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__370a718eebf64f79c09f4b0abdd7a9d506c371e50a90314f5038b6ce1d3954e7)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("PipesPipeTargetParametersSagemakerPipelineParametersPipelineParameterOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a0c28707b861244fea748a564ef21852e5d974396be60f671c035b1061dc1bf)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9a80c98f72b72ab017fd103b43347451e6722e410af45a6df204dbd9e334d410)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4b7013f559dcb9c7ab14e9effda67fe7f007ba6a2caaf9fc63492ae3e1570367)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PipesPipeTargetParametersSagemakerPipelineParametersPipelineParameter]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PipesPipeTargetParametersSagemakerPipelineParametersPipelineParameter]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PipesPipeTargetParametersSagemakerPipelineParametersPipelineParameter]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7d48962109c308a91499676e9f7cb602fa5ed0565304e8baad2fe20d1808d00b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class PipesPipeTargetParametersSagemakerPipelineParametersPipelineParameterOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.pipesPipe.PipesPipeTargetParametersSagemakerPipelineParametersPipelineParameterOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__518167028175f95ec1cd4b2cfbbb58c0c14726956b6cdb5e0f2da4e6734770d1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__70395200aa9ef20da5ece600b047c17703cd305d06bb18b56965a73121376498)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6afe41331e46632bb0d1a92b092f364fde4927ada50241295a7c1d3bf61a6b8a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PipesPipeTargetParametersSagemakerPipelineParametersPipelineParameter]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PipesPipeTargetParametersSagemakerPipelineParametersPipelineParameter]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PipesPipeTargetParametersSagemakerPipelineParametersPipelineParameter]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__939895f58a0f0e1d973eff909cf281f1f322fff7bf167c3d72c9c16571de1394)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.pipesPipe.PipesPipeTargetParametersSqsQueueParameters",
    jsii_struct_bases=[],
    name_mapping={
        "message_deduplication_id": "messageDeduplicationId",
        "message_group_id": "messageGroupId",
    },
)
class PipesPipeTargetParametersSqsQueueParameters:
    def __init__(
        self,
        *,
        message_deduplication_id: typing.Optional[builtins.str] = None,
        message_group_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param message_deduplication_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#message_deduplication_id PipesPipe#message_deduplication_id}.
        :param message_group_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#message_group_id PipesPipe#message_group_id}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0225a7bc3afb9955fa2e36de932615f8065209227addf717580831b405b40abc)
            check_type(argname="argument message_deduplication_id", value=message_deduplication_id, expected_type=type_hints["message_deduplication_id"])
            check_type(argname="argument message_group_id", value=message_group_id, expected_type=type_hints["message_group_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if message_deduplication_id is not None:
            self._values["message_deduplication_id"] = message_deduplication_id
        if message_group_id is not None:
            self._values["message_group_id"] = message_group_id

    @builtins.property
    def message_deduplication_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#message_deduplication_id PipesPipe#message_deduplication_id}.'''
        result = self._values.get("message_deduplication_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def message_group_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#message_group_id PipesPipe#message_group_id}.'''
        result = self._values.get("message_group_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PipesPipeTargetParametersSqsQueueParameters(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PipesPipeTargetParametersSqsQueueParametersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.pipesPipe.PipesPipeTargetParametersSqsQueueParametersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d41c2b0c69a1dbeaa18a9c6183420a87cc0a2d829d2d3884e546868e8a5e7eaa)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetMessageDeduplicationId")
    def reset_message_deduplication_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMessageDeduplicationId", []))

    @jsii.member(jsii_name="resetMessageGroupId")
    def reset_message_group_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMessageGroupId", []))

    @builtins.property
    @jsii.member(jsii_name="messageDeduplicationIdInput")
    def message_deduplication_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "messageDeduplicationIdInput"))

    @builtins.property
    @jsii.member(jsii_name="messageGroupIdInput")
    def message_group_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "messageGroupIdInput"))

    @builtins.property
    @jsii.member(jsii_name="messageDeduplicationId")
    def message_deduplication_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "messageDeduplicationId"))

    @message_deduplication_id.setter
    def message_deduplication_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f1fd6b3e687d99c7d4d9de78e0abdabcb568695239c6ad8cf6f573200b137ef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "messageDeduplicationId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="messageGroupId")
    def message_group_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "messageGroupId"))

    @message_group_id.setter
    def message_group_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7dbed2561946dec4f1c97fd6754da78a1908f6081ab325712b4819a70b04da7a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "messageGroupId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[PipesPipeTargetParametersSqsQueueParameters]:
        return typing.cast(typing.Optional[PipesPipeTargetParametersSqsQueueParameters], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[PipesPipeTargetParametersSqsQueueParameters],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__48a9824408dbeb1b21381c0c4fa37b41158b7add9bb2c272c6b21401b11d0d6c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.pipesPipe.PipesPipeTargetParametersStepFunctionStateMachineParameters",
    jsii_struct_bases=[],
    name_mapping={"invocation_type": "invocationType"},
)
class PipesPipeTargetParametersStepFunctionStateMachineParameters:
    def __init__(self, *, invocation_type: builtins.str) -> None:
        '''
        :param invocation_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#invocation_type PipesPipe#invocation_type}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a17cfd8c8eb38f5d17d00b9b6ee1099659462765412e1c399d2c88483ac31327)
            check_type(argname="argument invocation_type", value=invocation_type, expected_type=type_hints["invocation_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "invocation_type": invocation_type,
        }

    @builtins.property
    def invocation_type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#invocation_type PipesPipe#invocation_type}.'''
        result = self._values.get("invocation_type")
        assert result is not None, "Required property 'invocation_type' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PipesPipeTargetParametersStepFunctionStateMachineParameters(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PipesPipeTargetParametersStepFunctionStateMachineParametersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.pipesPipe.PipesPipeTargetParametersStepFunctionStateMachineParametersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4032e2c059454173ac8a3195dc0feae01563c04e2ca57247a04e467056bd1e64)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="invocationTypeInput")
    def invocation_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "invocationTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="invocationType")
    def invocation_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "invocationType"))

    @invocation_type.setter
    def invocation_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c7bf74406346278b895858304a90a6952807bd5bb304e1f6a247bf6d99cf48f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "invocationType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[PipesPipeTargetParametersStepFunctionStateMachineParameters]:
        return typing.cast(typing.Optional[PipesPipeTargetParametersStepFunctionStateMachineParameters], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[PipesPipeTargetParametersStepFunctionStateMachineParameters],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e5347518bd7bdfea70350605dd301c719c4c31878be48f96ca8b56503c5f399)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.pipesPipe.PipesPipeTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class PipesPipeTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#create PipesPipe#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#delete PipesPipe#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#update PipesPipe#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__742afe7f12563567c423902c40a2b73b5e13f6bb33c01290a4b65fbc478b6992)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#create PipesPipe#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#delete PipesPipe#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/pipes_pipe#update PipesPipe#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PipesPipeTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PipesPipeTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.pipesPipe.PipesPipeTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__95f0d4ede926f93991376eaea63d1cdd543ed9bf351ee80a110055b1c7bca605)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0bf135e922a1940b0157a6ffbb6c05791e7a7f48651f4b4b71220f2c98a19746)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__84cd45701e0985a10f42c8247959f7b4e02c0a52c98feb55f37963c2f8566679)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f135d1ecc05f8a0aff5b5d27bcfe4d6bb7b7d0ffac28f829c1369565ce2ffa69)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PipesPipeTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PipesPipeTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PipesPipeTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a7c5bb979d6645cc857a8d4bcd25187e245501c9682ff41fe2207796268b4a87)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "PipesPipe",
    "PipesPipeConfig",
    "PipesPipeEnrichmentParameters",
    "PipesPipeEnrichmentParametersHttpParameters",
    "PipesPipeEnrichmentParametersHttpParametersOutputReference",
    "PipesPipeEnrichmentParametersOutputReference",
    "PipesPipeLogConfiguration",
    "PipesPipeLogConfigurationCloudwatchLogsLogDestination",
    "PipesPipeLogConfigurationCloudwatchLogsLogDestinationOutputReference",
    "PipesPipeLogConfigurationFirehoseLogDestination",
    "PipesPipeLogConfigurationFirehoseLogDestinationOutputReference",
    "PipesPipeLogConfigurationOutputReference",
    "PipesPipeLogConfigurationS3LogDestination",
    "PipesPipeLogConfigurationS3LogDestinationOutputReference",
    "PipesPipeSourceParameters",
    "PipesPipeSourceParametersActivemqBrokerParameters",
    "PipesPipeSourceParametersActivemqBrokerParametersCredentials",
    "PipesPipeSourceParametersActivemqBrokerParametersCredentialsOutputReference",
    "PipesPipeSourceParametersActivemqBrokerParametersOutputReference",
    "PipesPipeSourceParametersDynamodbStreamParameters",
    "PipesPipeSourceParametersDynamodbStreamParametersDeadLetterConfig",
    "PipesPipeSourceParametersDynamodbStreamParametersDeadLetterConfigOutputReference",
    "PipesPipeSourceParametersDynamodbStreamParametersOutputReference",
    "PipesPipeSourceParametersFilterCriteria",
    "PipesPipeSourceParametersFilterCriteriaFilter",
    "PipesPipeSourceParametersFilterCriteriaFilterList",
    "PipesPipeSourceParametersFilterCriteriaFilterOutputReference",
    "PipesPipeSourceParametersFilterCriteriaOutputReference",
    "PipesPipeSourceParametersKinesisStreamParameters",
    "PipesPipeSourceParametersKinesisStreamParametersDeadLetterConfig",
    "PipesPipeSourceParametersKinesisStreamParametersDeadLetterConfigOutputReference",
    "PipesPipeSourceParametersKinesisStreamParametersOutputReference",
    "PipesPipeSourceParametersManagedStreamingKafkaParameters",
    "PipesPipeSourceParametersManagedStreamingKafkaParametersCredentials",
    "PipesPipeSourceParametersManagedStreamingKafkaParametersCredentialsOutputReference",
    "PipesPipeSourceParametersManagedStreamingKafkaParametersOutputReference",
    "PipesPipeSourceParametersOutputReference",
    "PipesPipeSourceParametersRabbitmqBrokerParameters",
    "PipesPipeSourceParametersRabbitmqBrokerParametersCredentials",
    "PipesPipeSourceParametersRabbitmqBrokerParametersCredentialsOutputReference",
    "PipesPipeSourceParametersRabbitmqBrokerParametersOutputReference",
    "PipesPipeSourceParametersSelfManagedKafkaParameters",
    "PipesPipeSourceParametersSelfManagedKafkaParametersCredentials",
    "PipesPipeSourceParametersSelfManagedKafkaParametersCredentialsOutputReference",
    "PipesPipeSourceParametersSelfManagedKafkaParametersOutputReference",
    "PipesPipeSourceParametersSelfManagedKafkaParametersVpc",
    "PipesPipeSourceParametersSelfManagedKafkaParametersVpcOutputReference",
    "PipesPipeSourceParametersSqsQueueParameters",
    "PipesPipeSourceParametersSqsQueueParametersOutputReference",
    "PipesPipeTargetParameters",
    "PipesPipeTargetParametersBatchJobParameters",
    "PipesPipeTargetParametersBatchJobParametersArrayProperties",
    "PipesPipeTargetParametersBatchJobParametersArrayPropertiesOutputReference",
    "PipesPipeTargetParametersBatchJobParametersContainerOverrides",
    "PipesPipeTargetParametersBatchJobParametersContainerOverridesEnvironment",
    "PipesPipeTargetParametersBatchJobParametersContainerOverridesEnvironmentList",
    "PipesPipeTargetParametersBatchJobParametersContainerOverridesEnvironmentOutputReference",
    "PipesPipeTargetParametersBatchJobParametersContainerOverridesOutputReference",
    "PipesPipeTargetParametersBatchJobParametersContainerOverridesResourceRequirement",
    "PipesPipeTargetParametersBatchJobParametersContainerOverridesResourceRequirementList",
    "PipesPipeTargetParametersBatchJobParametersContainerOverridesResourceRequirementOutputReference",
    "PipesPipeTargetParametersBatchJobParametersDependsOn",
    "PipesPipeTargetParametersBatchJobParametersDependsOnList",
    "PipesPipeTargetParametersBatchJobParametersDependsOnOutputReference",
    "PipesPipeTargetParametersBatchJobParametersOutputReference",
    "PipesPipeTargetParametersBatchJobParametersRetryStrategy",
    "PipesPipeTargetParametersBatchJobParametersRetryStrategyOutputReference",
    "PipesPipeTargetParametersCloudwatchLogsParameters",
    "PipesPipeTargetParametersCloudwatchLogsParametersOutputReference",
    "PipesPipeTargetParametersEcsTaskParameters",
    "PipesPipeTargetParametersEcsTaskParametersCapacityProviderStrategy",
    "PipesPipeTargetParametersEcsTaskParametersCapacityProviderStrategyList",
    "PipesPipeTargetParametersEcsTaskParametersCapacityProviderStrategyOutputReference",
    "PipesPipeTargetParametersEcsTaskParametersNetworkConfiguration",
    "PipesPipeTargetParametersEcsTaskParametersNetworkConfigurationAwsVpcConfiguration",
    "PipesPipeTargetParametersEcsTaskParametersNetworkConfigurationAwsVpcConfigurationOutputReference",
    "PipesPipeTargetParametersEcsTaskParametersNetworkConfigurationOutputReference",
    "PipesPipeTargetParametersEcsTaskParametersOutputReference",
    "PipesPipeTargetParametersEcsTaskParametersOverrides",
    "PipesPipeTargetParametersEcsTaskParametersOverridesContainerOverride",
    "PipesPipeTargetParametersEcsTaskParametersOverridesContainerOverrideEnvironment",
    "PipesPipeTargetParametersEcsTaskParametersOverridesContainerOverrideEnvironmentFile",
    "PipesPipeTargetParametersEcsTaskParametersOverridesContainerOverrideEnvironmentFileList",
    "PipesPipeTargetParametersEcsTaskParametersOverridesContainerOverrideEnvironmentFileOutputReference",
    "PipesPipeTargetParametersEcsTaskParametersOverridesContainerOverrideEnvironmentList",
    "PipesPipeTargetParametersEcsTaskParametersOverridesContainerOverrideEnvironmentOutputReference",
    "PipesPipeTargetParametersEcsTaskParametersOverridesContainerOverrideList",
    "PipesPipeTargetParametersEcsTaskParametersOverridesContainerOverrideOutputReference",
    "PipesPipeTargetParametersEcsTaskParametersOverridesContainerOverrideResourceRequirement",
    "PipesPipeTargetParametersEcsTaskParametersOverridesContainerOverrideResourceRequirementList",
    "PipesPipeTargetParametersEcsTaskParametersOverridesContainerOverrideResourceRequirementOutputReference",
    "PipesPipeTargetParametersEcsTaskParametersOverridesEphemeralStorage",
    "PipesPipeTargetParametersEcsTaskParametersOverridesEphemeralStorageOutputReference",
    "PipesPipeTargetParametersEcsTaskParametersOverridesInferenceAcceleratorOverride",
    "PipesPipeTargetParametersEcsTaskParametersOverridesInferenceAcceleratorOverrideList",
    "PipesPipeTargetParametersEcsTaskParametersOverridesInferenceAcceleratorOverrideOutputReference",
    "PipesPipeTargetParametersEcsTaskParametersOverridesOutputReference",
    "PipesPipeTargetParametersEcsTaskParametersPlacementConstraint",
    "PipesPipeTargetParametersEcsTaskParametersPlacementConstraintList",
    "PipesPipeTargetParametersEcsTaskParametersPlacementConstraintOutputReference",
    "PipesPipeTargetParametersEcsTaskParametersPlacementStrategy",
    "PipesPipeTargetParametersEcsTaskParametersPlacementStrategyList",
    "PipesPipeTargetParametersEcsTaskParametersPlacementStrategyOutputReference",
    "PipesPipeTargetParametersEventbridgeEventBusParameters",
    "PipesPipeTargetParametersEventbridgeEventBusParametersOutputReference",
    "PipesPipeTargetParametersHttpParameters",
    "PipesPipeTargetParametersHttpParametersOutputReference",
    "PipesPipeTargetParametersKinesisStreamParameters",
    "PipesPipeTargetParametersKinesisStreamParametersOutputReference",
    "PipesPipeTargetParametersLambdaFunctionParameters",
    "PipesPipeTargetParametersLambdaFunctionParametersOutputReference",
    "PipesPipeTargetParametersOutputReference",
    "PipesPipeTargetParametersRedshiftDataParameters",
    "PipesPipeTargetParametersRedshiftDataParametersOutputReference",
    "PipesPipeTargetParametersSagemakerPipelineParameters",
    "PipesPipeTargetParametersSagemakerPipelineParametersOutputReference",
    "PipesPipeTargetParametersSagemakerPipelineParametersPipelineParameter",
    "PipesPipeTargetParametersSagemakerPipelineParametersPipelineParameterList",
    "PipesPipeTargetParametersSagemakerPipelineParametersPipelineParameterOutputReference",
    "PipesPipeTargetParametersSqsQueueParameters",
    "PipesPipeTargetParametersSqsQueueParametersOutputReference",
    "PipesPipeTargetParametersStepFunctionStateMachineParameters",
    "PipesPipeTargetParametersStepFunctionStateMachineParametersOutputReference",
    "PipesPipeTimeouts",
    "PipesPipeTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__25885b4e0fb316c42c6c2b5247fd1261829169b06d99c4566cf95bb674ef0a8c(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    role_arn: builtins.str,
    source: builtins.str,
    target: builtins.str,
    description: typing.Optional[builtins.str] = None,
    desired_state: typing.Optional[builtins.str] = None,
    enrichment: typing.Optional[builtins.str] = None,
    enrichment_parameters: typing.Optional[typing.Union[PipesPipeEnrichmentParameters, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    kms_key_identifier: typing.Optional[builtins.str] = None,
    log_configuration: typing.Optional[typing.Union[PipesPipeLogConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    name: typing.Optional[builtins.str] = None,
    name_prefix: typing.Optional[builtins.str] = None,
    source_parameters: typing.Optional[typing.Union[PipesPipeSourceParameters, typing.Dict[builtins.str, typing.Any]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    target_parameters: typing.Optional[typing.Union[PipesPipeTargetParameters, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[PipesPipeTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__ed0c64209bafa15ff4a6394e5192797fbc46297d1fe6b85f1ee939463112906c(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1d792de6252214cb180174ceee67d57cc44ab15d73ca19a9d5348be93dcde91(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52ee1691aa8105ac9452371c12f8019b64d4401a54a30b63a26b791ba509d97b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__961cb2fd2deb99e302a5ebc6a31289897c4cfd3b07560bed2e81bb4dc4053e8b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ce9cc79b7535a7182c02f917195a8062d24fab1422db949b37fbe3d72ec8347(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00b8d214503c15d90fdb8fe580b468a06b7036aac4dd78f0e4038128e1b2e6a9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b443ab7ab30202f38d825e8debde4e40a2880a594344d4603199da796acb88e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1a30f830cf2edf50945c53e7f47fdadead73bc01ba9faae8028c2479c3fdc4a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0faee8788df24e0f8222c7df89108b4b8af16d89bcab8234342e0ac657a9d544(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4727e13a56e2bc3ed9ab10ca9775597703c6dc57191d492db05aa51e5d4d4cb7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93090979eefd3db77df31dcdc5315ee12bf96501da990e34bc3b70c912b569ad(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4ced249a2a92c449fe88378bc53c24d400362fc08d2dfd75a552460ac0189c8(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d9ea5e619eff4677881205f48025c7a9df55e7fa58999bdd43bbb5720fb3498(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ae38792413ea6deb395b6ee564a80d644beef47bef13eac262d03c08a6ec82f(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    role_arn: builtins.str,
    source: builtins.str,
    target: builtins.str,
    description: typing.Optional[builtins.str] = None,
    desired_state: typing.Optional[builtins.str] = None,
    enrichment: typing.Optional[builtins.str] = None,
    enrichment_parameters: typing.Optional[typing.Union[PipesPipeEnrichmentParameters, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    kms_key_identifier: typing.Optional[builtins.str] = None,
    log_configuration: typing.Optional[typing.Union[PipesPipeLogConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    name: typing.Optional[builtins.str] = None,
    name_prefix: typing.Optional[builtins.str] = None,
    source_parameters: typing.Optional[typing.Union[PipesPipeSourceParameters, typing.Dict[builtins.str, typing.Any]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    target_parameters: typing.Optional[typing.Union[PipesPipeTargetParameters, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[PipesPipeTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8fbf320aba8dbd20f7d453a8e0316774cdc90a626eaf2cc77a198299b686652d(
    *,
    http_parameters: typing.Optional[typing.Union[PipesPipeEnrichmentParametersHttpParameters, typing.Dict[builtins.str, typing.Any]]] = None,
    input_template: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cbd132970f51dbc99f97a1a186ef62af2f3b7e9ce4d3bd4ce21c7351bf07057a(
    *,
    header_parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    path_parameter_values: typing.Optional[typing.Sequence[builtins.str]] = None,
    query_string_parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7bba9d3c0bee6776cac32928c6874899d1319f63eaec2afc2d73b346502cbd34(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13177408a155d88521379f8cc1ed2a805a63a98338d6072ffbe0cee735f0af3a(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e5ea9d1677d8eaeff18565394f374b4e6e1daf3570fffc9e42dd43926308a4a(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa632411a740ce5d11a8022dfdc1842f067b3048d9daa5a28a0bbc125e1e7b34(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fab9274754fc0802e84c1ccd55f127929c31b1467f27ac847085ac313ef49508(
    value: typing.Optional[PipesPipeEnrichmentParametersHttpParameters],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b40ba6703b2bdaef2d913896bc209b51e822c7901e2310db3c3294961c5a3ad5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7ef9a6939594dcba8b4a6ac55ea6495f8d11325f8e4d8ed3e66de29c24964fa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__07479edcf7ebf79a59118f74d3bb573614e5e5da48f79f17c0171d5b74baf38e(
    value: typing.Optional[PipesPipeEnrichmentParameters],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b02801f26948a8e88afc155de5519f99edd9b6f6faa28c861c09bd5e043071c9(
    *,
    level: builtins.str,
    cloudwatch_logs_log_destination: typing.Optional[typing.Union[PipesPipeLogConfigurationCloudwatchLogsLogDestination, typing.Dict[builtins.str, typing.Any]]] = None,
    firehose_log_destination: typing.Optional[typing.Union[PipesPipeLogConfigurationFirehoseLogDestination, typing.Dict[builtins.str, typing.Any]]] = None,
    include_execution_data: typing.Optional[typing.Sequence[builtins.str]] = None,
    s3_log_destination: typing.Optional[typing.Union[PipesPipeLogConfigurationS3LogDestination, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5bf15e2b3b745fd1d37e6d09cb6c5d2ed192aad6656913d4090ffb284be056c9(
    *,
    log_group_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ba9acb450e5982386fb59516534cc694745c175e6d20d59021dff19f6c2d0b2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a464caf9117350afb45674c00a334e45d7cc1a5ac5558d77a5a9449036e31b6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bfb32aba766d43bc708f289507238262fbada67dcb7929df20d6ab1c97762b59(
    value: typing.Optional[PipesPipeLogConfigurationCloudwatchLogsLogDestination],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a55dde54c23adc340c83767fd77cd6b674315bc531b89f16d0fd6538b4277377(
    *,
    delivery_stream_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b98dc63d9408ac10279db5c80e5f9e70231c7f32ba532bcfc09283ce53617020(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4b0a933a65b4a7d6bef4f2d1c7aece6f5361ab872603da229097f42cfcb56f8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67efbb6ac631919da8390e119e9d7ff6094978d278ecb89ebdbd6d0a7c4c9ab2(
    value: typing.Optional[PipesPipeLogConfigurationFirehoseLogDestination],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0cbdbc9be271dc01da850640d30d1590b6c7db707fdaaa852cee168c39f72598(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09d55b3e57d1470ff2e5524b37a7e54aee59f3760d4fec3aa2944ffbcd986b0f(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ed78a4e78c512b76784175ec88f622909c227fe774c4b02b8e9adc218289b9d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8fbd59ce893fa9744eff6b758b9bfb771d3d94d6f8753b6318dcf182e6d8c8f0(
    value: typing.Optional[PipesPipeLogConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02e4e613e28b1792498e5263a66d3815a4b74daf0b60c03501834bc79ec1d584(
    *,
    bucket_name: builtins.str,
    bucket_owner: builtins.str,
    output_format: typing.Optional[builtins.str] = None,
    prefix: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__207d94b55df9ad699f475ea40474f83bc5d1f915df1a5a3ae4ca6bee1e784d7e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c59b6147fc51e3919526561631f8f67bf3551b459131eaa9ab80c46b42cf259d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5960a44441a8d00d88af75376236a868d5e3f0470effbae14771fac1c840810d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4a8912e5890fb6cf4e6e3691f310bba90bd6babab80320279fd72eb5ad2a6e9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__402013d3465e640d01228e02a9f058bd186faeeb9873929e74a7fabb02c0ef77(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f32eee03b5abb06894f9fe9ed66890e0505182ec23f9359743f07f897d67b59(
    value: typing.Optional[PipesPipeLogConfigurationS3LogDestination],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dcbc8316d12899e17f1c47829613f8657e3783b3ba9236dc91eae00478b1cb8a(
    *,
    activemq_broker_parameters: typing.Optional[typing.Union[PipesPipeSourceParametersActivemqBrokerParameters, typing.Dict[builtins.str, typing.Any]]] = None,
    dynamodb_stream_parameters: typing.Optional[typing.Union[PipesPipeSourceParametersDynamodbStreamParameters, typing.Dict[builtins.str, typing.Any]]] = None,
    filter_criteria: typing.Optional[typing.Union[PipesPipeSourceParametersFilterCriteria, typing.Dict[builtins.str, typing.Any]]] = None,
    kinesis_stream_parameters: typing.Optional[typing.Union[PipesPipeSourceParametersKinesisStreamParameters, typing.Dict[builtins.str, typing.Any]]] = None,
    managed_streaming_kafka_parameters: typing.Optional[typing.Union[PipesPipeSourceParametersManagedStreamingKafkaParameters, typing.Dict[builtins.str, typing.Any]]] = None,
    rabbitmq_broker_parameters: typing.Optional[typing.Union[PipesPipeSourceParametersRabbitmqBrokerParameters, typing.Dict[builtins.str, typing.Any]]] = None,
    self_managed_kafka_parameters: typing.Optional[typing.Union[PipesPipeSourceParametersSelfManagedKafkaParameters, typing.Dict[builtins.str, typing.Any]]] = None,
    sqs_queue_parameters: typing.Optional[typing.Union[PipesPipeSourceParametersSqsQueueParameters, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe48769a069aa1248ef18604e7b3af6004ef90d6f124e0ce3f4e4061ddef8265(
    *,
    credentials: typing.Union[PipesPipeSourceParametersActivemqBrokerParametersCredentials, typing.Dict[builtins.str, typing.Any]],
    queue_name: builtins.str,
    batch_size: typing.Optional[jsii.Number] = None,
    maximum_batching_window_in_seconds: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a007bfd2dcddfa6d7bc0ddb94d871c0c97723f5d6386c55d4f331c534b7fc93(
    *,
    basic_auth: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1dcf3b473cad9f6f4bd85bd550d3706f2fa273104b5050bf3688f32c8e93761(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b2aa0a99508326a4b42b2504995438c04b291f5cbe03441c2ed9aa5c50f5e19a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c976fb055fa7d6f514711c794f44c6dc16934142ffca3229eacb72c577e92c1f(
    value: typing.Optional[PipesPipeSourceParametersActivemqBrokerParametersCredentials],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7df86d4ff0b0261d5c47ecceeb5d1a78ea563bb481c7c7604a1edfe76fc8181f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c471ae028f15b15b84633ea4340748f443882699a25b200f1db8a525ad51d9e4(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__353ed11d2a6568413b5e5dc87159ad17fcd25638ec363fb72bfac09964da9991(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d6889f28c037b6a8a431364c5f92511cb2faa33ff72a1e7c64e069eff1db48f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69f4528ef97f521cbcc6385db693c7c954811dee9ff39c6f88ca34810b00acd7(
    value: typing.Optional[PipesPipeSourceParametersActivemqBrokerParameters],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d92cf48e0a2e0ef243bfccefdb9bc34dcbbfae121dc39ca9b714761ce7dcc45(
    *,
    starting_position: builtins.str,
    batch_size: typing.Optional[jsii.Number] = None,
    dead_letter_config: typing.Optional[typing.Union[PipesPipeSourceParametersDynamodbStreamParametersDeadLetterConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    maximum_batching_window_in_seconds: typing.Optional[jsii.Number] = None,
    maximum_record_age_in_seconds: typing.Optional[jsii.Number] = None,
    maximum_retry_attempts: typing.Optional[jsii.Number] = None,
    on_partial_batch_item_failure: typing.Optional[builtins.str] = None,
    parallelization_factor: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__17f3c9eb2a10c867822a87eb29ac10120ce1cc83bfd2afb6df1b9a27ff92b335(
    *,
    arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7ded94e35c7a465eb45ae9225448eebe251ffaa25f64b548def25a98636064a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50e5a17b48356ac1890c20772bcd9c347bb38ae8af90cac7d799a79b83c61d3e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__01a16692068c55565bb789940456ff099af860c71078f100e89f040808ad9ce3(
    value: typing.Optional[PipesPipeSourceParametersDynamodbStreamParametersDeadLetterConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb761fb2484ef69042220e529b2a5b6f10d0fc58c2087d04eabc712fe84b9a39(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f41344a2516b5fd454889cca9bba545f8cb01c9d971c19b576e38e153ca5be98(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__656829594cc77b9a78b5cff97bc6f2ca94d92512e6177343d8348ec24048a6df(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__222e6adcf702ca4f414e83ecfd99f50e76ab25847169cbdf1041b91296f399fb(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__edd065a8df1363617d07cd0d2f76d72714e678ca6c7328ad1cc7623fed9284ce(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ff52de538bafbeb7e71ca13891c5361c68f1e7f6bc297c8f4b224d62991d13e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0148b4c6f34c072615ab8cadaeeecbf7c51d82b97efa9a734a8ef52091689bb0(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__711657a60e1c353f19d39dab211b02ef6ceeac547b469963a729fb8f0f4966e1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dcce6d338df2b44dbd44eca65bacaac25fe9ccee03c93143c75966e3621af9a6(
    value: typing.Optional[PipesPipeSourceParametersDynamodbStreamParameters],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bab998576186e3754b673e6a5216b531cddcd21141daec63656614bc91e2cba5(
    *,
    filter: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[PipesPipeSourceParametersFilterCriteriaFilter, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2bdbffc64c44bea5b18a318ebd196bf2802c5d0c9c80a7d73d17aa00e83e5e7c(
    *,
    pattern: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54cddf0a54308067c05cd625ae4707d1f36a7248262c52ba4a840e51adf9a3b5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bcf0cbfc078771a361c73b079326812a716bb1e5085a1365749bb1f0460cc43f(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88176d401c8e67c1ce2a6bf5200b136d580f47ba959fca2392490984ccdb32bd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe0151a321d02bb243bb0b31df86fbdc31ded23fcc7418a4cfd46e313996ad30(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1edfa0bb2f5949a779aa866106abf60909ddaf37b8425b5881b8674a0139d28b(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac3ad3544c88f28a2ce01431fa1a400e206a7288b3553003b8063d298a80ba35(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PipesPipeSourceParametersFilterCriteriaFilter]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a19b143b126252ae83a7cbb886000999be981887c5a15daf89824bed43d4f165(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c55df51f021dcd0aa119eacbb305af8fae170ab19dc863668a58b6779977ce19(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b0162f0c319d688308dfcc4d7bddac4ce3189dbd2961a834627e709e25f8c4b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PipesPipeSourceParametersFilterCriteriaFilter]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b087cc98eff2881bc14b129ad3c03c4bcf598d6dbde73c8793fcc14f5fd0324e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__035198805ae447b2139235e409c2a0cacc174a9d14f83a835d06717cd9dbade9(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[PipesPipeSourceParametersFilterCriteriaFilter, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2f599b83e70b342533f55157f928efe64c2c12e230627bf0699f0f961b5cec7(
    value: typing.Optional[PipesPipeSourceParametersFilterCriteria],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f9f90aa2e63904fe739da609d90b9710778f184e8ac87a68cf2b2f9d3abffe4(
    *,
    starting_position: builtins.str,
    batch_size: typing.Optional[jsii.Number] = None,
    dead_letter_config: typing.Optional[typing.Union[PipesPipeSourceParametersKinesisStreamParametersDeadLetterConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    maximum_batching_window_in_seconds: typing.Optional[jsii.Number] = None,
    maximum_record_age_in_seconds: typing.Optional[jsii.Number] = None,
    maximum_retry_attempts: typing.Optional[jsii.Number] = None,
    on_partial_batch_item_failure: typing.Optional[builtins.str] = None,
    parallelization_factor: typing.Optional[jsii.Number] = None,
    starting_position_timestamp: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a783b1288042d64792bd0625205e0dcae484be3156fb61de08e9c24be7abe8e(
    *,
    arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc4b9cecafe3bbd6609e8b165396571c7412c99dab06a822812aa08cfab0ad38(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd4cfb4cafa06a1a80231088874652380c8ec46847aae0b634fab9fc6c408157(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc6a73a69f0fae73912423ee3e46c7c0d0cf6b750ee1f78c912837f664ee1aa1(
    value: typing.Optional[PipesPipeSourceParametersKinesisStreamParametersDeadLetterConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5ebfaca302acf1489f32b12b75ceb1396f118099a880ae760d45afeb932c524(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f738618ca0b89e75f53166b45de6a856955dcad3a3907fc4cab7c056fd3d2009(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad3eb1dd8e00e6544e815f58023dd293cc26eafb9541b4036b3b98dff9397d8e(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__183f7eee1b91f0bfd6a37f87c3992bfe171526c510f6774a972e671484e39390(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96fc560f690f0f3287dcdd84ba4e6b6211092a0094adc5841b6aef68a7153b64(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__580872431b243ef4952bdc6533e29a8b06e785d79eed7c9c5ca2466b1301a6ca(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__299b8491480f0f7c231cd252f16bf76655a4284889ab7489132503eb84e72478(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b7bf03aa5a04ec166df98219ad2d09846b82419ccf034a4f910b851d4e8e2f53(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__962d6b3a14d2d4bc66fe485750e376eab811301e62a2048d66fc2a3ff0c39ad4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57903dc2a5a057fd493ab02052079074fbf3417a13dc93ea3c5992ad00c3d71d(
    value: typing.Optional[PipesPipeSourceParametersKinesisStreamParameters],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8e57f0bb431f01d39e9cae98d41d61c80f415d9a2978aa8ed68f2b287546a76(
    *,
    topic_name: builtins.str,
    batch_size: typing.Optional[jsii.Number] = None,
    consumer_group_id: typing.Optional[builtins.str] = None,
    credentials: typing.Optional[typing.Union[PipesPipeSourceParametersManagedStreamingKafkaParametersCredentials, typing.Dict[builtins.str, typing.Any]]] = None,
    maximum_batching_window_in_seconds: typing.Optional[jsii.Number] = None,
    starting_position: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5be1a7108fffe44a7f5b69eac1b0ebfd9c878d42148eba053def08fd7178a904(
    *,
    client_certificate_tls_auth: typing.Optional[builtins.str] = None,
    sasl_scram512_auth: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__742613ba6577368178fa8e75b040402ddf937add134860870393d0987537a59f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8453c7c2b7e07109195b142415695862342b272a31450fc32c42b15fa27409b4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__613cc338290b57a41552a3c01e74bc1b5b54ea104fed3bd34c668bed8ee06016(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f89232c2a79e018347ef34fb8ea11c85b668542ba2694267837370537e9a8c0e(
    value: typing.Optional[PipesPipeSourceParametersManagedStreamingKafkaParametersCredentials],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__982867587ca5d9ab866c8d879b44b16d3588371a5b76095717b197691daaa7a5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__078f543e8ec5695368c24058114962c550f3f4856833ef087141a8180154dfad(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca0c428931e235840267b0b46153971e861037e2aaa2a1fc394f8ebb84aaeec0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f2bb3bcfeedba46c18feb5af6684d71a7e17ad556bfe81df7986568fdd9ec85(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61f83ceafd4492b621b62ae0df2a65dd59863191eac8e59191a5955c13a4c174(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3ec5fed631762c85df9a0f756fcdad215efdfa329a5e13f4c826b73185cae2a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6529b3ded0ec23e01d1f6120b98307919ff41913128ecd8a907cdbd93437c811(
    value: typing.Optional[PipesPipeSourceParametersManagedStreamingKafkaParameters],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a6ade3553dd1b8a7c1cadb5cfd61673112c6cf724fca73d996792be37581fb8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd1b76f42c4984c4384302a8533169e6448dbdf8403b014d7fe876137b4eb681(
    value: typing.Optional[PipesPipeSourceParameters],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8316a77d60c73d069acaa60480d7b2dd42d9bb5add3bb3db33aad7fcc5653fe8(
    *,
    credentials: typing.Union[PipesPipeSourceParametersRabbitmqBrokerParametersCredentials, typing.Dict[builtins.str, typing.Any]],
    queue_name: builtins.str,
    batch_size: typing.Optional[jsii.Number] = None,
    maximum_batching_window_in_seconds: typing.Optional[jsii.Number] = None,
    virtual_host: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a743ed7fec946ec857124e7e6670cc58ee80e15db7964145a6aa4fffe890b953(
    *,
    basic_auth: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc234f6da4a42b71d3351920961f877624bfb7a7d8cb7dc5882bf7fe2ecd0c2a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d415291bb78149ac0601b9fe3867eaeb6a287028e59fde668a0a60bf37b8ce74(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__504dccfd46ba8c533d75278d9bc3db4b65e758c89be2acb458339c98f99f57d0(
    value: typing.Optional[PipesPipeSourceParametersRabbitmqBrokerParametersCredentials],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4dc9d8d53e0c534d91046b63547d53861858afa8d31fad8e73c60a8c93d2b7e9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d832636062a2385ff4217a349a3817a204cb201d1092e1b5f68a9c0fab7668e5(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a51f5a4bc275163226a983fd8a26cbe64be7a8debc5d6e1c2cdf7d4dbceee62(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ca494a282a45fd07e975c52e2f6d6393aefbb9d49ba25b31a87cf406980800d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b39741fbded3d8fd9942a9593d7ae35a3f5d7589fe16d29570c39d15fc50e71d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25ca718af28d7d1b36311763d65b0f6f64879c29a865e4a0d45eefd193de51a2(
    value: typing.Optional[PipesPipeSourceParametersRabbitmqBrokerParameters],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3b7430a7afd15b9af60ac1e5c2bbb80d7691a2bd3ce5a3f6de6bb8f20438667(
    *,
    topic_name: builtins.str,
    additional_bootstrap_servers: typing.Optional[typing.Sequence[builtins.str]] = None,
    batch_size: typing.Optional[jsii.Number] = None,
    consumer_group_id: typing.Optional[builtins.str] = None,
    credentials: typing.Optional[typing.Union[PipesPipeSourceParametersSelfManagedKafkaParametersCredentials, typing.Dict[builtins.str, typing.Any]]] = None,
    maximum_batching_window_in_seconds: typing.Optional[jsii.Number] = None,
    server_root_ca_certificate: typing.Optional[builtins.str] = None,
    starting_position: typing.Optional[builtins.str] = None,
    vpc: typing.Optional[typing.Union[PipesPipeSourceParametersSelfManagedKafkaParametersVpc, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1500725b1ae78a8f84bce66d1e29dd12d5f22bfddcc3b596b24091dfd4e88dd(
    *,
    basic_auth: typing.Optional[builtins.str] = None,
    client_certificate_tls_auth: typing.Optional[builtins.str] = None,
    sasl_scram256_auth: typing.Optional[builtins.str] = None,
    sasl_scram512_auth: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b3a4748158a9dd7cd4b785e6807472804c2580d3723ceec6852e599d84af7bc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6ea1c93f8b30c1a799b13dca5c436dba16ef2d46a435b7ead3892c308efa193(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e201ae5cf724e274cc4ff2622aab1199b750b659acd4f91056bb03dd917702c6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__beaace34d524c54bacdcf234a3865d2343c98f3e8b4dfba4236c0afa24d0dfdb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d40efd6c57a46b7f83f8d91db716a92f02a6d1f04a1a5c498ff8acabf01b4b1e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41dab4353b6254d5f87f291db2a37ed85d1b5bb8d3fc4be7bcd822f737ea404e(
    value: typing.Optional[PipesPipeSourceParametersSelfManagedKafkaParametersCredentials],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04693c6e201b25ab65959fcf69c85eee55d23e5b2e1e563c19193998d1c6e79a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5197eea7f4283fa2c61ffc74f1c743011037ca0d54ee9fb06074fe3eb90b1a4(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c42532397303b99f9fa02a9652bb710c0e1d1231f5c749c384f82060ad96047(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7653a290a45ca691857cea8981dc85d019bb72591a1c7fb9e5c19c3f624a937a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c434acd7e570117dcef5bafcf94f0c026ebb7bdcf3a9243857aed8bc7de369b0(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b11eeecf5daf0ed710f396f9705e4b3de41fd621ded2683b865c20ecd94329c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f5319a052a0d9f84e5f77685353d89f88604f26d289a5aafe457c60b8c81d96(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20a36831e9845393173d8c5230dd73a99c707e8d90982ffb46f80cebd3a66072(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d45460a35c4fb94cc8960415a2a0521185a407b19fb74afbf63609bce77e991f(
    value: typing.Optional[PipesPipeSourceParametersSelfManagedKafkaParameters],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc8672296bd558d9765ef7290d74c578eb5265277997f410de61d31e9b212221(
    *,
    security_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
    subnets: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__603c9b9e0f8a85aee969f4757c30595e5fff7196e763f4d398d85679d2b27c6b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fbdce6eebf05b27f567d403ceb7f84c535e20e8f1503e7c4509ecef54e05e94c(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea567fde920ae2a26e6803c133cecea2c9da82b544c31d441a42ded71ab84e4b(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__455f05b907bf0105fb24fa938d84aad5144ed5ebf1b6fb67f1963685d36e1771(
    value: typing.Optional[PipesPipeSourceParametersSelfManagedKafkaParametersVpc],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c80bdde1bb2a2a7f80e049721cf3a1cf90ab695718d099b3aafa9eaa9d9c8e96(
    *,
    batch_size: typing.Optional[jsii.Number] = None,
    maximum_batching_window_in_seconds: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53a2dab28a324542f6e399d4f14340c296f64aba15d3798ad921156b83fde2ce(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3dde29e16049cfc79a231784535e5c138a2fdc8d719237634b652a22500f0583(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d4ccc392189585135aa591ea6fba9b5c2458b7a43363e8ed9e454d0e55d5ac3(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0cbde1d4f5968864cc5e798f3d7ee6f421754a146c1f458f827b513ffb9e4cd4(
    value: typing.Optional[PipesPipeSourceParametersSqsQueueParameters],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e25b60649e0a580dd3eb27efb3577835054a1013066fe69c7405ee9b0d17f6a2(
    *,
    batch_job_parameters: typing.Optional[typing.Union[PipesPipeTargetParametersBatchJobParameters, typing.Dict[builtins.str, typing.Any]]] = None,
    cloudwatch_logs_parameters: typing.Optional[typing.Union[PipesPipeTargetParametersCloudwatchLogsParameters, typing.Dict[builtins.str, typing.Any]]] = None,
    ecs_task_parameters: typing.Optional[typing.Union[PipesPipeTargetParametersEcsTaskParameters, typing.Dict[builtins.str, typing.Any]]] = None,
    eventbridge_event_bus_parameters: typing.Optional[typing.Union[PipesPipeTargetParametersEventbridgeEventBusParameters, typing.Dict[builtins.str, typing.Any]]] = None,
    http_parameters: typing.Optional[typing.Union[PipesPipeTargetParametersHttpParameters, typing.Dict[builtins.str, typing.Any]]] = None,
    input_template: typing.Optional[builtins.str] = None,
    kinesis_stream_parameters: typing.Optional[typing.Union[PipesPipeTargetParametersKinesisStreamParameters, typing.Dict[builtins.str, typing.Any]]] = None,
    lambda_function_parameters: typing.Optional[typing.Union[PipesPipeTargetParametersLambdaFunctionParameters, typing.Dict[builtins.str, typing.Any]]] = None,
    redshift_data_parameters: typing.Optional[typing.Union[PipesPipeTargetParametersRedshiftDataParameters, typing.Dict[builtins.str, typing.Any]]] = None,
    sagemaker_pipeline_parameters: typing.Optional[typing.Union[PipesPipeTargetParametersSagemakerPipelineParameters, typing.Dict[builtins.str, typing.Any]]] = None,
    sqs_queue_parameters: typing.Optional[typing.Union[PipesPipeTargetParametersSqsQueueParameters, typing.Dict[builtins.str, typing.Any]]] = None,
    step_function_state_machine_parameters: typing.Optional[typing.Union[PipesPipeTargetParametersStepFunctionStateMachineParameters, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__852eab64fec2c126813aee1d8abc1b4f3b5297f517874e4dfc13c3aa71a0a06d(
    *,
    job_definition: builtins.str,
    job_name: builtins.str,
    array_properties: typing.Optional[typing.Union[PipesPipeTargetParametersBatchJobParametersArrayProperties, typing.Dict[builtins.str, typing.Any]]] = None,
    container_overrides: typing.Optional[typing.Union[PipesPipeTargetParametersBatchJobParametersContainerOverrides, typing.Dict[builtins.str, typing.Any]]] = None,
    depends_on: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[PipesPipeTargetParametersBatchJobParametersDependsOn, typing.Dict[builtins.str, typing.Any]]]]] = None,
    parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    retry_strategy: typing.Optional[typing.Union[PipesPipeTargetParametersBatchJobParametersRetryStrategy, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ddd3dc657bcd23a41dc39c3b8ebb70519f9663195f910615c41328be9439bf5(
    *,
    size: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc91d7eefad5f8654698ad31d47dd6d1b706a23bdb3750bb38d933715d4ffe09(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b135119a85085af82b147f9275b66c172a06282cb94a0e8bb3edfc5d56475499(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c093b53cfb92179f3952148e18124f6d508b6c47f29cd8b03f056719bde93665(
    value: typing.Optional[PipesPipeTargetParametersBatchJobParametersArrayProperties],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1ac170bf1ee0e30a17909db976c096aa4ef5ec06543d76fb575e8b66a50d50e(
    *,
    command: typing.Optional[typing.Sequence[builtins.str]] = None,
    environment: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[PipesPipeTargetParametersBatchJobParametersContainerOverridesEnvironment, typing.Dict[builtins.str, typing.Any]]]]] = None,
    instance_type: typing.Optional[builtins.str] = None,
    resource_requirement: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[PipesPipeTargetParametersBatchJobParametersContainerOverridesResourceRequirement, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d5e4dda516209273e910ba897162e255e6a562b0eefca3d8eefe73d2bc2c9ff(
    *,
    name: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fcbb2d2da53979281a93f2220c9e6b969e8ff65693dc973837c0c10caeb5e4de(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3dd3e4d426dd7dcd055c43cba2a80f56ff6998f9eb3fd97a15a562a7cdb4811(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f70d7f6576dfc8f317e60f2424142fff37f10d7775a68fe2f7eef8f03ce72ba(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be597ebd8a92bb25b963c7f33489684197192f3c7902b6dba1698fc60a047226(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5966175abcd519c2017d8a2bda68893af16b9453b651c75150c61e9b8d7aad5(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db616837430933b851583c19c4adfeaec98a2a61c0d9dafd23371e473f147fd0(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PipesPipeTargetParametersBatchJobParametersContainerOverridesEnvironment]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b8260b1f503c926056e2f9a091e4c8cf5caa1f37a8bab1dbf6cd9e1f6ac8192(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff44678ef7b9c4d6d73403852ecae9d5afa13b05edfb1f8f3887e72eddbb6aec(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__115bb74add64a265cee9f499b7f746a26e731371a82f8c0fb5bd20294aa94919(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6eeb97217bef371fed0781235bce08f22a7f3937dd93b7c7a28ff050f19f7732(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PipesPipeTargetParametersBatchJobParametersContainerOverridesEnvironment]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7bd758ca0e235463bebd2f207c36d3f9f64584207c0edb3713ef1a59abdc140f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96302104eb4a06db2bc910ae17e3f1ecf836ea458a7891f01fa2f1dd236a8817(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[PipesPipeTargetParametersBatchJobParametersContainerOverridesEnvironment, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65a8d07ec52b1d38959511dd90d0489fae27f8dc38bfea7894d115e082e146b8(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[PipesPipeTargetParametersBatchJobParametersContainerOverridesResourceRequirement, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f8bd4c9374f367974f47694c11124d465e73c2ad90bf861321f1ca301d10147f(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bfd2e06abc5f828bf6e5108f16406ef6ab2d8cecce02f5dcc958648a12fd8484(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7861f2df4c9f5b3698c1410fefc3934b16ae6fe52f1a3b9e8bb3790b28c491e(
    value: typing.Optional[PipesPipeTargetParametersBatchJobParametersContainerOverrides],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf041b0b059d02605f317b1f2d7c3813fb43bc95f08f02bfc3b811b49d5d586b(
    *,
    type: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__414af0d908e39dd9eeb54b10f4cab97f3cad59d00a12cccf4eca36389b3579f8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__82751e293af62a3c00f409c0de80515cc49c25774b5b6659be354cf1716154f0(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__825f98a619d521338469de7c14e97f1fb290b4e1510acf1d1fd727fc0e4c7255(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cea84ab65eaf711b470268c6164d3fa3f5a40bcbc51348cf9fa8c02e43b513bd(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76e5db6070d0a96ec8c910618cd9584fde80d4f92568ca96a9482202af6423d5(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bce43beacff946a0a16448aec9de8e5a4b1a1ec3173e45c32b992ba5af8bd12b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PipesPipeTargetParametersBatchJobParametersContainerOverridesResourceRequirement]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0cae1b4d00b66e28eaee70d85e47bd4dc6fe76c9b846e8abf706868b5f4f7d7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d9a98168740dee55eb4c96828085b9dda21a82a26ddca87278c013643d7e709b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__17d8e59539cd6e8e8b23907862aa0fedd7c7fb2dda5595f2ea78aef486cf0506(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f159057384c3884758da79a99e6e88aef6f7a27f4a146d08a9fa10345688c25(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PipesPipeTargetParametersBatchJobParametersContainerOverridesResourceRequirement]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb1fcc6fbd1f1e3758bdb48b6a3c81c883e0742b676f205d251f459156ddcc99(
    *,
    job_id: typing.Optional[builtins.str] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8cb8a9945f0c608d5fcf7f383740bad9d60c4d3ef6de9e047c6ceaa753645549(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b33be7e84888a9f942edf1387249cfd6bedffd33bdd04f6305f5a67996bf1ad(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7103c233f381ad8baf55de37d4b750c2671c8a4dee9aa2d36cf3fe70438455c3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0ee6e5bf4ab6d2e14e11196ff1668e33ff2fbeb370198de6b5f0b2bb5d9d01d(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e0e0f049828f52c7c736c7d08b4f3ebff12de18ef9ab0002d7b89de641dda992(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64d3803627823b0ba1de0e2c1292956890018234d150b2bb2e62d47d11fbbf1f(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PipesPipeTargetParametersBatchJobParametersDependsOn]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df66a2368691a878c4ccbd7789ac1ecaf64ac0681d69eee8a3d05e201528d85c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d335e9cea51ea091f0162c67f13f1cb04aa4f0adbbd8a1a37964595ce2c284b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67a34d878e51345a09e209e1fe1387c8875bea81fe703f33e90f4024efd040a5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d16a7862cd75343c11e4f415854833303c369fce5f244b245861ca0a95382c9a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PipesPipeTargetParametersBatchJobParametersDependsOn]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__51013534b1332acb48990f3bb973c2924a78c6e797aa2ef76c9cb96e73feb2f2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71f12f0271674aeb7757f64d64981e7840a1f1d0a5c1118b3201e94ebfa2db49(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[PipesPipeTargetParametersBatchJobParametersDependsOn, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__797e7e633a63e2e8d27237d97fc171cb744d9fc2baad1bc928dcd0be515f9446(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77ded11b2398f3827a9d3a680581acf75a380d2746da00c7413848fa8494b3dd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ce87b886e35c57cead86d9572a85ce7f92fa0a11f6c6fce3f7929921ecd3dae(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2fa24e01ff6140f3726c1b5ae60004e8566870a765af9b6f805b93d6e0cdf165(
    value: typing.Optional[PipesPipeTargetParametersBatchJobParameters],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d63beaea962f0fa96bc28232dfc753ddf27f99585639ce02314e799047e0e6f3(
    *,
    attempts: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__573dbbdb415955a0ea4747b82393cb9e4b10a6bbce7c74db49f7bcb42f90fbec(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8810dc40a100e75db558dceab47eb12cb9cd5c31ae2b46184df4cbc19b08828c(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__deba7d132bbfc95efdb1e26a6233cb315b260780d95bcf991ff2b820fd7fad4f(
    value: typing.Optional[PipesPipeTargetParametersBatchJobParametersRetryStrategy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92cb6bdceee1f4568f4320e14cca8c5ea498cb8144f618cdf2b06fcd2e7814fb(
    *,
    log_stream_name: typing.Optional[builtins.str] = None,
    timestamp: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__839e718a5ba5d5ed4425b5113a0f51dd507ff2dca0282c0ff826afa4e3740a01(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a94062f22ce01139c14258fe6cb27317c9ce5feaffed7949ccaf2d533bb0d93(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__137f76ae7ae10ced32011cadc5c9f53a1789248770b44e325618f3f2c0b95dcc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a26618cc9e98d91a35c9dcaaedff4757e6b603b7645b669b7292ac93cf5fc4b(
    value: typing.Optional[PipesPipeTargetParametersCloudwatchLogsParameters],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a10927bb2f07937e87192645c4c211eeee9124d5ae21a0be9d427bd855c92c7(
    *,
    task_definition_arn: builtins.str,
    capacity_provider_strategy: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[PipesPipeTargetParametersEcsTaskParametersCapacityProviderStrategy, typing.Dict[builtins.str, typing.Any]]]]] = None,
    enable_ecs_managed_tags: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enable_execute_command: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    group: typing.Optional[builtins.str] = None,
    launch_type: typing.Optional[builtins.str] = None,
    network_configuration: typing.Optional[typing.Union[PipesPipeTargetParametersEcsTaskParametersNetworkConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    overrides: typing.Optional[typing.Union[PipesPipeTargetParametersEcsTaskParametersOverrides, typing.Dict[builtins.str, typing.Any]]] = None,
    placement_constraint: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[PipesPipeTargetParametersEcsTaskParametersPlacementConstraint, typing.Dict[builtins.str, typing.Any]]]]] = None,
    placement_strategy: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[PipesPipeTargetParametersEcsTaskParametersPlacementStrategy, typing.Dict[builtins.str, typing.Any]]]]] = None,
    platform_version: typing.Optional[builtins.str] = None,
    propagate_tags: typing.Optional[builtins.str] = None,
    reference_id: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    task_count: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e3054ab06098c1579b8624eef97bc10a5ca5d492ae131c55f551b31651398e16(
    *,
    capacity_provider: builtins.str,
    base: typing.Optional[jsii.Number] = None,
    weight: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f8eb6987859b1b7620e695ba8c089af9e01bccc83c985627a1d02b2b2e499fb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__628a625db3e68eeb2ba4cddcd333ddfc6b82a81c349ceab63d2e50124afc9f3d(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3904b9b6a72171d373b7f14a31bfd550e99a63dc91d3a5ca7cbb80ac888a132d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2884c5c1f570f0ed79819dddbd903cbc52dda5a6f8f08df51f1ea6d27b662c66(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40de0881de1df407d2d6bd7f2599f5b89b47ad7efb7e099685862285e2217b01(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__652e26d712adef431ddfee122ccafcd779b41d340548a245a0f42c02938787db(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PipesPipeTargetParametersEcsTaskParametersCapacityProviderStrategy]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ee7f7b5b0062f5c440e676a8f53a912d8ac0d926c74e7635326785bc01d1c09(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34fe5515ad3d67ff0e2aa2ece7d829c0f30876652c038c928ec00e417ba906ae(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e060b9cb866e7134a200b1ac0ba87d53db27009e756247b4c6fc0aac9159b7e0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53823e7e6e20f8a6982266aa3d85b83761f55c1f9ccc4f2c6510ca057fd4be4f(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__410023db1584cd6fc23a393d7bc13fd671862c6a029c6b152d0f09318a8376d0(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PipesPipeTargetParametersEcsTaskParametersCapacityProviderStrategy]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1fc2b8249449876cb4162c17a6ed2f7421423e512b39833c49f0692d4cabba2c(
    *,
    aws_vpc_configuration: typing.Optional[typing.Union[PipesPipeTargetParametersEcsTaskParametersNetworkConfigurationAwsVpcConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f9b8458583630fb2f880e88b55f83ac32157f7113c6682ede3e0f3e81ea9844(
    *,
    assign_public_ip: typing.Optional[builtins.str] = None,
    security_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
    subnets: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dfd6418bd28eac93b85b0276515f7c1914dfa27da7a08ec25fd6ec740f78a36b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__010b39ac5e2e088b48c069664121387845c4175c141fde2996434537b1a058ab(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f54445fdd27b1c2121b7972d51a4fd0a081e43fe218b596a95b61ee082c568f(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80139aea94394ff48f6371f024a0c8fdd4d7b67b289bee562f7ba78e7ab72a05(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__70ba973fb9a3119f5b4f73742f71ed8de183e8346150c610b76fe4cca1faeb3e(
    value: typing.Optional[PipesPipeTargetParametersEcsTaskParametersNetworkConfigurationAwsVpcConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c232c20104e5803542017368abd0dd178fff0a77e21dee1e1b870ff34e47e098(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c58857f52ae2350aa0ebbc4d8c613ce1618e1f1355a3e78233e8d6ec46b20b78(
    value: typing.Optional[PipesPipeTargetParametersEcsTaskParametersNetworkConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83a8b37d06f8b34f5ff3f6de4fd2eb1ca3408aa1268f715d20927efe099ae0b9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0bee473c8a1626a6d837f95dc4ccaeeaaa1ad57eeb9db65b5e4c8dd57a727414(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[PipesPipeTargetParametersEcsTaskParametersCapacityProviderStrategy, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__06bb5b354ce90d6827be6f159baba09f938b3d0ecba4331be394f8cd674f2f26(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[PipesPipeTargetParametersEcsTaskParametersPlacementConstraint, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd86ab2df8fed220b31f06f5eb7ee78f07f1e5a15c1b238ec9b0d997ae9ac950(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[PipesPipeTargetParametersEcsTaskParametersPlacementStrategy, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61bc854840ba2bdde4558fcb6f94e01b89972b9fd50a5fcbc2c9a6e71412bd89(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__640684d59f87fef187f1479ebedbfb4eddd07232f447238bfb1b5ad5bc15ea22(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab81024c0453103829c471eaa5e0b324a6b9c8c56196cf9c983437feb1f5167b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ee095285772cc13718aaeed248a07215aad2b5c6e5cbffddef007edb7318456(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6cd133e8b68fe993e286ff23d6a437698d4d16ab6382f004ba5089d74aafc1f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__518d3b93e3afd06579015c73487c69f8320c6b6f6ad63febdb4d71cccc1f0c69(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e3a76c86c13231a60aa7b9817e7b41b4615bfb1146f310dc3f66b70b3309ff10(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b5d6b626b3653ccb77cdfe518f03e1c9ea6f38194ecb88c272ab31ce6b97e2d(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6e5cfa4486319b9c9cddd4ec38b0b1906abfbbf69226a0bc62d921982a43acc(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__430db9d230553615464f25a9c16d98ed4a40f21ebf9cd6bdddce6752e8365289(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b785d36f60d64f808bdfdf81a23d611f852e933c190ce9b6d288a1590f5a0f20(
    value: typing.Optional[PipesPipeTargetParametersEcsTaskParameters],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ac387ac47f50cd31aabbffeaaf9e2fc5a32808fc03bd77b08282ea770548299(
    *,
    container_override: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[PipesPipeTargetParametersEcsTaskParametersOverridesContainerOverride, typing.Dict[builtins.str, typing.Any]]]]] = None,
    cpu: typing.Optional[builtins.str] = None,
    ephemeral_storage: typing.Optional[typing.Union[PipesPipeTargetParametersEcsTaskParametersOverridesEphemeralStorage, typing.Dict[builtins.str, typing.Any]]] = None,
    execution_role_arn: typing.Optional[builtins.str] = None,
    inference_accelerator_override: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[PipesPipeTargetParametersEcsTaskParametersOverridesInferenceAcceleratorOverride, typing.Dict[builtins.str, typing.Any]]]]] = None,
    memory: typing.Optional[builtins.str] = None,
    task_role_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44c3465e2e1a0ad67478b883021c7d3e3e703d92f92412ccd839de71b12544eb(
    *,
    command: typing.Optional[typing.Sequence[builtins.str]] = None,
    cpu: typing.Optional[jsii.Number] = None,
    environment: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[PipesPipeTargetParametersEcsTaskParametersOverridesContainerOverrideEnvironment, typing.Dict[builtins.str, typing.Any]]]]] = None,
    environment_file: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[PipesPipeTargetParametersEcsTaskParametersOverridesContainerOverrideEnvironmentFile, typing.Dict[builtins.str, typing.Any]]]]] = None,
    memory: typing.Optional[jsii.Number] = None,
    memory_reservation: typing.Optional[jsii.Number] = None,
    name: typing.Optional[builtins.str] = None,
    resource_requirement: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[PipesPipeTargetParametersEcsTaskParametersOverridesContainerOverrideResourceRequirement, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c353db5b3df47a752e90aae20866fd5fd10669aed355d1c1ecb7bc24ba2756c(
    *,
    name: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7deb8e4dfd5859a3031fca249e11f3088592b23f16b8133ad50aa72c08adc50d(
    *,
    type: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94f419e6e3fa8ebd2b5732191be59454ea01ea4f75baca95d4e4bead5ce58a1b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__171a4d9d334fe5e961b6302a4beb70043862c7329d14acb5cd92061b4e503030(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94faab71442c52ad68de5f4e3f1065630c73b03159f7fa61a2a28386f1f8781a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f336010c6a0fea2d9d2a822db427163e0d4888dad33445c76cd36a114b873ef(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c2adc133b14399ec7b828e00d3cc0cf7bd859d42ac1fca3c73507b80530a3d8(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8868e9d9d8b4930ea67f68896c9ed11cb3a99ebd6001757fcafba1ac70d49f0(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PipesPipeTargetParametersEcsTaskParametersOverridesContainerOverrideEnvironmentFile]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7142b71b5f0fdd9bd3cbef94ede6669af2a7a5611b4ce1e5294427ae37b64a4e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f8f65f007ba1aed2a9aa4815c040a413ee543953f27ad152e866df149ea9bfc1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d102aa1b25f663bf183f20e7f43ae8d50c481ff19925e4a839885d74cd33864(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d5e70d4955e41feb522f3841b6b841680da7abea163b687d0e7da95dda3b6ea(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PipesPipeTargetParametersEcsTaskParametersOverridesContainerOverrideEnvironmentFile]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__064f733ac9292aec1474dced67f351bf85804e4342c3efcc3bab21bc68e8ee68(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__085d22c9be9a58afb9d26429b1a52f0300436da0694c6fa31316a9f4bc2f142b(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d2bb51a19fe9d987ef78536f65132cf79728d2acda490ca43286769250b7434(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2898044a7ba2ccd596bd9e397bf8c863f8fa3e0ccb7fe75d53de84c16674d5a5(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18fb433a4b05b9e426a8fb07fff590027cbefc36e4b32e9152f5b7bcaed6ae84(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__06585f411ff2824a114fa02925c7f9306f6de4ea1184ca2fb2ea0431ab2dc61b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PipesPipeTargetParametersEcsTaskParametersOverridesContainerOverrideEnvironment]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b1f75268dafbfbba1e51309d15037cbf89de6b93d603ee0405507e68d0c4615(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__630349e5bf2f6489c741f0bd6c8492d85adc978969dbcb466fdc0a04f73930e9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef804e773760530113fd1f001eb735b268056e2abffb7a2e4b0c330edcdd94f6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__206b7e37f6ad5103621c4c0aad8f267a1ef2280b1e6e88626ab35b59b7f84cee(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PipesPipeTargetParametersEcsTaskParametersOverridesContainerOverrideEnvironment]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94f54d1ddc2282f1973f5fa55036a47d25714e709e300e41b82b6a11e9204289(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a09a9a350509602679170b6abad44345b58ff85e3f42c2de31dda53e8c36f06f(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53ff8a32807818312d89ec45983c87d40ce00b49e179fb872d3d717a8d9cac48(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5230b63083b46b01d19265e8ffdb3912c6f5f6c61771f27b7882864677fbb733(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e45344d2406b91b732fbb506566e50304738cd32cf626a24b628a7d053e35b5(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__714386a7c8b05d6c449494c79f228dd9dec206eeabb4355ecfc0afb51ad68e96(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PipesPipeTargetParametersEcsTaskParametersOverridesContainerOverride]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0fa5834778a6a75cfd2aacf8b39ce4b681b9ef5c5033068d1bd5b74527b37e6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7de78d9cd508ac7c0084aa292b8e344cb97fcc278f8fbddbd5c74da1b848e966(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[PipesPipeTargetParametersEcsTaskParametersOverridesContainerOverrideEnvironment, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3bc0fd450a5a6805d75cd917e2a95a953ce08278d8cbc97821052e6d1dd6d869(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[PipesPipeTargetParametersEcsTaskParametersOverridesContainerOverrideEnvironmentFile, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1abf6a3f887999f97cefdcc6fd4b012c63eda956ae94080797dd7f1386b3ee15(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[PipesPipeTargetParametersEcsTaskParametersOverridesContainerOverrideResourceRequirement, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1269eb602d369e9f050b9999bcd760cfd04178505b132b5c13ef4093dea82e61(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a90c7f785101d0163b95623601c96aec77b40bf44f0568563a6b8522c771a3be(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e8770f8935dc7a48778e30b98b70df4945eb537351360e915016db6a336fc1c(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31e55bdf82d2c8a33126daa37290e2b8780bf69710003825e916d58bcc2f2142(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3c0a25c3796398524e655208ff97088c582255424e92e6b890d3c90919148ef(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__997b7d29c11cb74588d178a73f03cd1f6c640354495b37e3f80c03dc2f3ca7f7(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PipesPipeTargetParametersEcsTaskParametersOverridesContainerOverride]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e30058607c59693a8c3f51b72d14ab763d9b9a19ef7ca22cf9f75993af55c74(
    *,
    type: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5713faf23bb840afa9a131eaa6266aec0fde67a0444755c5dce45512b9ac33de(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__953e5cdec6ecdbcb26ba26f9cb13e04c700a36e1d6d49eb14e594c4ad8152f72(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71d0240dce2705bf639e38ba45b698149e7ca9190492a4b923beaeecc1b8232c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d7ca3881a1dbf8373a07adb5f87c0d4a3ea28c43fd103faa6bf5b8cb843eb20e(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54787da8d5e2312046feb8af74fc917c19a3eef65d4388238c40298b04285e04(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8378673f965d446c523440fafe1752605ea9dc32a0b3e1728d4c89b888dbbca7(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PipesPipeTargetParametersEcsTaskParametersOverridesContainerOverrideResourceRequirement]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f3cc298218a7b0398bdcfd7151f006eb12d854fd7419f29c48c7e5b36823559(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04cf999030e5679afc7f124cd680ae3ef43649c2813e4cef07d25e372b1a15a6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f4fa382640bfa858879e04f8a59d9910c18f1455d5a296a002733790db33773(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f95c8a62c40ad486de1dcb3df6982222f15664895eb28714bbe0f6222832cdff(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PipesPipeTargetParametersEcsTaskParametersOverridesContainerOverrideResourceRequirement]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04943886594d4324b4399e634b207c085c2d38d5fe78996f2f3a9eff03824595(
    *,
    size_in_gib: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4727baec25cfeaa289a12f9e49fa7cee012834882e2f3c5de5e296f47c0a316(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d521518619ad80499293a05b5601c4c2a5aba0f0b7e38e684230de299df30e07(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41ff7ec93b0ccc21fd86b7134f2303997ad2b720de382633613d0717d1df5f48(
    value: typing.Optional[PipesPipeTargetParametersEcsTaskParametersOverridesEphemeralStorage],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30addbea279eec224a18bc4bee6c2d6bd9ad2e103daa5285198eee69ef73de11(
    *,
    device_name: typing.Optional[builtins.str] = None,
    device_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c08cc0fd4e58cfa2e3ab599fff4a6dd826c8fe3dd703613e960d9189aa4038a0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d145520feaa137e3cf5488cc3dd51f9ccbe48662af5a15532c068134c00e7720(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__836c76c83e62e63598e0d6a73ce6f6cb0f976db1c29e36cabaf97b80a5e1b0d5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a6db8c6839789aa4628079ee92b2daea3958fbf0f19647d08f8224f899735ddc(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__edf8d0d49732d10ce0933e45aaec4123f81531c2df6f305b88752b441318230a(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3cd3bab2ab762e977caced576f0be223df12c0068100926c8930e9bc03272551(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PipesPipeTargetParametersEcsTaskParametersOverridesInferenceAcceleratorOverride]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__393baf92f942c6546ce8fc8ae44ce1ab04820c88de8a44dc4ba4ca47b77b472c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bcf4fc29c04573e9126db13442fbb63778749d030f0d18efd766dc65229ca3c5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42d02c7242017ba0c87570298e8d7b5035f2ee3078284c0fbfc6835bd30b6762(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6589aef7566f0c5a6213b2d973c4c3c62f1164a94dacc5be21f0b3dbaec08010(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PipesPipeTargetParametersEcsTaskParametersOverridesInferenceAcceleratorOverride]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03bc2f6c84da3d493bb55275b939525c59b3379d5f463f50ccab036b1b65228b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f043c37f7d6ad13f402a4bf57a8b2224320b1f9e6e68bd3f6b7d251575e6c6f1(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[PipesPipeTargetParametersEcsTaskParametersOverridesContainerOverride, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ad99a10d2e4d3c1884e39d227c03dd176e971f679109dee8680f50fa1bc0379(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[PipesPipeTargetParametersEcsTaskParametersOverridesInferenceAcceleratorOverride, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__21d2839f9e0d4eca424b7fd69d244d477025ad0c8c5ae928f193c2a7c42f2959(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f0c45cdaef80ee7930248dadd739ef2fcf6ac4332c7ce809ec3a435b74c975b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26abb5b65456a46d9d7295253e93a404fb77dec72cf7d9b61a0bc3054b199a57(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2ca0ffe7c2dba5760413039bb68ace6a89ef374eec0fa323f090796dc51e749(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__673916a154a9584cf9f90d33146195505b895db567bf1617e039f06a52a6f317(
    value: typing.Optional[PipesPipeTargetParametersEcsTaskParametersOverrides],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__21263f747c2f061b3f5deac8bcbb2b7962a6b2ad8db634d918312d2d5a586f0d(
    *,
    expression: typing.Optional[builtins.str] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c021b6aac1bb0146f4c17b402fbfa9dd716eef60777638b8b2b5367a545cdc23(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__754c8c50e22082248f50ba5bfc6c850c185ab40a952105448d658553b0511574(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6fed425be2461316b4efaa3722fcc07220576834e469054c5705b1afe58f4290(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c03698c2c1a0a787505cde1aa3ed6545fad6b21b4d983b324ec7d6cedb78656(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e402ab9f5d81f1ecf08249a4139244713b93482c0755a885bfeb24f854e7acb1(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ebe11210f39f01cd15fabba7fa24bd647a8394546638302783cd2032754bd29(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PipesPipeTargetParametersEcsTaskParametersPlacementConstraint]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__727162056886e8b68a9c2658f62842fffa492fbeebb9da0b1ccb600ff9d52c2f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3e7ea4f0acf8b4c9337813e701e1d7ad2ef2333592e4d31ee5588894b998863(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__23ebf930a8deb049d4c375a6571e9ff3ee8076e9233979ad0c5f46bc642bb2e4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a576607aeff5ee59079f8f5ff4e439354a69ba1d4cac8407ccea4e453cc8408(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PipesPipeTargetParametersEcsTaskParametersPlacementConstraint]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1e39f2c960c6ec4b3717e0f58fa0dc719d6405af8d8a09c7de11a466ef50b76(
    *,
    field: typing.Optional[builtins.str] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__108ce08b5dec3855d3ec449d097dc7a4a99b3c73aa1670c84d0ed2c0e206eae2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2d5324b0f2b134a3b517bef1d23eda5d6090ed7b18a6fc8f3b7ce7bd539be79(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd694b286a30c7321fdb0f05cbc62ce6fd363903e0aa9d4d7739d85b292ec99a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c2b28405d4da6f758a13123705a075ec144310bbc605ec45b8110c1e59120ed(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a26d8b316555609a0c2163d831764b69b3cca50cb59371e3c269c95db6eb353b(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__944ca590a32e389ea0fd8061c2cbe1d4431e7efc3dea58f673c961e101b91358(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PipesPipeTargetParametersEcsTaskParametersPlacementStrategy]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aab9e3b3fd42c12881aa8baa2f26a35354869a16eff745486de996d4bf2f21e3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c45248b0c7839c3f57c994201982c922431d4f53b9144bde001f918a7e730b3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e49769fe77e3bce7a6abeeef5162f260a46675c95f33b3700e1795e25fade98(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__95956394b91e5a0be0098b88d9d514b85a934b078be7e5619de03ddafa96840b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PipesPipeTargetParametersEcsTaskParametersPlacementStrategy]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ceb20f73aaf0c1f8e98a651471be42a8e1403056b2ea308bec4ebaca40bbde9b(
    *,
    detail_type: typing.Optional[builtins.str] = None,
    endpoint_id: typing.Optional[builtins.str] = None,
    resources: typing.Optional[typing.Sequence[builtins.str]] = None,
    source: typing.Optional[builtins.str] = None,
    time: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__402996c793351fb877e099ed13bebb516ae5ca50d46995acad17c1c5c8e8c693(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9924d4102e67dc715f8bb758ee85f54383601e355f8524912b72af161ab722d6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f82c6484924709997eafa792ad9af99cef082d0aa8bde6ef3db2db000e721db8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3085112edb69d2139df5f426c3088f8688b9d6ffc59a2d1b0dfb83250650e58a(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4253f82bcdeb368906945b7fcb2fde96811ade2eda8fa7b9c62ffad9b018c16d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5dc2c46d471f289d976fa06b8ff331afe7c1cefdfd9207b990f4c44272d79f18(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67f499567f73bd7d7526409a032a22ce92337be868f252469f830bbdf6bdcf5e(
    value: typing.Optional[PipesPipeTargetParametersEventbridgeEventBusParameters],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a53c08ddfee005f4c6c9be762197b0f7ba0d61f1d74234d37698197972c18453(
    *,
    header_parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    path_parameter_values: typing.Optional[typing.Sequence[builtins.str]] = None,
    query_string_parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fdab0e20b00e94e757965d41d9cbc6b6284b2b31f9f2fccd840025e4db092451(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88d0cafca54902b2e6f0eeae0062e25adf146321fb60eb24538e08f1310189ca(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8af7f5c717d366597ae2851c53a75bf648bc3ff71bfd7c7464439167f8125fa3(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77cc151fbbf2447d3970d037be09b1344e5e379c781cd8590b9afb51e019f671(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2e4bc25adf3c8e91dcad8bd77ac1088a1dd507b5915e92353e603c16e131e22(
    value: typing.Optional[PipesPipeTargetParametersHttpParameters],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b8ad854c9fee85d1cf9279680e48cd94c51fa4351d8e3cd2b3bcb84af9be82c(
    *,
    partition_key: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__511ae4c5c514935fbe7373d5468483f1614d551efe080b3b352b412cef23dd24(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__951986154bc1899f94b49fadfb756620051a834a82f9ee5d7a5e0e3ac636cc45(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3571a8d6256001855b739cdedd8abed33f06f98f4daabd5de179f3921d1ca7a1(
    value: typing.Optional[PipesPipeTargetParametersKinesisStreamParameters],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2c048e988a30e56ad344b92a8690aeeda6b72f0a1682c07b512dd9697845aa9(
    *,
    invocation_type: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e0f058398315d6843eb18117863f298cee2d2a22e038df3c4243b337cf06aae(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed8032ad1fddb9f3f3d9bbf48d253806aad1d5102892472e18a8932ea1aa9d7b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__201ad64e69e9aeb599e02da8e742444c02a888625095d9c5383423b9dcc24c0b(
    value: typing.Optional[PipesPipeTargetParametersLambdaFunctionParameters],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2ca21234829a6f65175c5008140cefad75372153f2503dc37ca1430616bcf38(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a03ef4a5195a1a2584c06d5c71b54a65b45577878415bb885984968017eaaa2a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e27205f49fb0e0982a51167a268a3f45a880ca8861af00f6747902b643082765(
    value: typing.Optional[PipesPipeTargetParameters],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d78d05895dcf7c4be41786c64d7407028bb9478d3677dcdd7fa7ba76fa0f77f9(
    *,
    database: builtins.str,
    sqls: typing.Sequence[builtins.str],
    db_user: typing.Optional[builtins.str] = None,
    secret_manager_arn: typing.Optional[builtins.str] = None,
    statement_name: typing.Optional[builtins.str] = None,
    with_event: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5ef1e673ecccc48c3c469477ab11c98e5aeb2aa5093fe078077d7f78707b08f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04ed052ccd6a3f1cbd4c514c041887a3e42c037bbcb02cf3ab645327f19bd074(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5798e15acd72738f1eb1834b1fcbd0c004c4ec6191903175eb238edb722c2052(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d492467f736fb7864cc13e7f1db3263673d56d9156b4f8f7fbbdf9e524d6be2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e7d1c790c6d3310ac48643810dfd8ec446ddeb460388e9bc12a99654754ed2b(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6920fde12ff3eeefe82ee9090acc7cbb60f5e18deda77f9bbf26ea987fb1d155(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f69f2da9f4ef917ccae7167145b90a7bca1560eba9577c7b788800653636252(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a4293d05ba08d13632877bfbcf45e44820e77f44deaa47dd38cdeff6174d519(
    value: typing.Optional[PipesPipeTargetParametersRedshiftDataParameters],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bdfa8c05bd8b0a402d1a770d39e5ab6082f65eab93f6f4d210180b5935010b14(
    *,
    pipeline_parameter: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[PipesPipeTargetParametersSagemakerPipelineParametersPipelineParameter, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74b4bba2c4d69fc20e83d0a2a9944c52a6aa4f784362acaa7351efce5ff1fedc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f01e43813226d14d318218365fa7e8f4fe723a1c34d626650af9a0ae2d9b57f2(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[PipesPipeTargetParametersSagemakerPipelineParametersPipelineParameter, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d7c8fcf9372dbe0419e0720eec6b8b296292d0ad6aad5460da1eb655d092402(
    value: typing.Optional[PipesPipeTargetParametersSagemakerPipelineParameters],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e3d347ae0926e0c8a0e87dd45ecea7f8a6f970bb4303764fe12714f47174a847(
    *,
    name: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7be6e7ed9ef3b393b023b7fdf3e4405f6f15dadb366e98b51c094950883c4c22(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__370a718eebf64f79c09f4b0abdd7a9d506c371e50a90314f5038b6ce1d3954e7(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a0c28707b861244fea748a564ef21852e5d974396be60f671c035b1061dc1bf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a80c98f72b72ab017fd103b43347451e6722e410af45a6df204dbd9e334d410(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b7013f559dcb9c7ab14e9effda67fe7f007ba6a2caaf9fc63492ae3e1570367(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d48962109c308a91499676e9f7cb602fa5ed0565304e8baad2fe20d1808d00b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PipesPipeTargetParametersSagemakerPipelineParametersPipelineParameter]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__518167028175f95ec1cd4b2cfbbb58c0c14726956b6cdb5e0f2da4e6734770d1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__70395200aa9ef20da5ece600b047c17703cd305d06bb18b56965a73121376498(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6afe41331e46632bb0d1a92b092f364fde4927ada50241295a7c1d3bf61a6b8a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__939895f58a0f0e1d973eff909cf281f1f322fff7bf167c3d72c9c16571de1394(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PipesPipeTargetParametersSagemakerPipelineParametersPipelineParameter]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0225a7bc3afb9955fa2e36de932615f8065209227addf717580831b405b40abc(
    *,
    message_deduplication_id: typing.Optional[builtins.str] = None,
    message_group_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d41c2b0c69a1dbeaa18a9c6183420a87cc0a2d829d2d3884e546868e8a5e7eaa(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f1fd6b3e687d99c7d4d9de78e0abdabcb568695239c6ad8cf6f573200b137ef(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7dbed2561946dec4f1c97fd6754da78a1908f6081ab325712b4819a70b04da7a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__48a9824408dbeb1b21381c0c4fa37b41158b7add9bb2c272c6b21401b11d0d6c(
    value: typing.Optional[PipesPipeTargetParametersSqsQueueParameters],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a17cfd8c8eb38f5d17d00b9b6ee1099659462765412e1c399d2c88483ac31327(
    *,
    invocation_type: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4032e2c059454173ac8a3195dc0feae01563c04e2ca57247a04e467056bd1e64(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c7bf74406346278b895858304a90a6952807bd5bb304e1f6a247bf6d99cf48f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e5347518bd7bdfea70350605dd301c719c4c31878be48f96ca8b56503c5f399(
    value: typing.Optional[PipesPipeTargetParametersStepFunctionStateMachineParameters],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__742afe7f12563567c423902c40a2b73b5e13f6bb33c01290a4b65fbc478b6992(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__95f0d4ede926f93991376eaea63d1cdd543ed9bf351ee80a110055b1c7bca605(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0bf135e922a1940b0157a6ffbb6c05791e7a7f48651f4b4b71220f2c98a19746(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__84cd45701e0985a10f42c8247959f7b4e02c0a52c98feb55f37963c2f8566679(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f135d1ecc05f8a0aff5b5d27bcfe4d6bb7b7d0ffac28f829c1369565ce2ffa69(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a7c5bb979d6645cc857a8d4bcd25187e245501c9682ff41fe2207796268b4a87(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PipesPipeTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
