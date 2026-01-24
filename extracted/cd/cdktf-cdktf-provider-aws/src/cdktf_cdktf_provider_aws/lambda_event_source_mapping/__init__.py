r'''
# `aws_lambda_event_source_mapping`

Refer to the Terraform Registry for docs: [`aws_lambda_event_source_mapping`](https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/lambda_event_source_mapping).
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


class LambdaEventSourceMapping(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.lambdaEventSourceMapping.LambdaEventSourceMapping",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/lambda_event_source_mapping aws_lambda_event_source_mapping}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        function_name: builtins.str,
        amazon_managed_kafka_event_source_config: typing.Optional[typing.Union["LambdaEventSourceMappingAmazonManagedKafkaEventSourceConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        batch_size: typing.Optional[jsii.Number] = None,
        bisect_batch_on_function_error: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        destination_config: typing.Optional[typing.Union["LambdaEventSourceMappingDestinationConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        document_db_event_source_config: typing.Optional[typing.Union["LambdaEventSourceMappingDocumentDbEventSourceConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        event_source_arn: typing.Optional[builtins.str] = None,
        filter_criteria: typing.Optional[typing.Union["LambdaEventSourceMappingFilterCriteria", typing.Dict[builtins.str, typing.Any]]] = None,
        function_response_types: typing.Optional[typing.Sequence[builtins.str]] = None,
        id: typing.Optional[builtins.str] = None,
        kms_key_arn: typing.Optional[builtins.str] = None,
        maximum_batching_window_in_seconds: typing.Optional[jsii.Number] = None,
        maximum_record_age_in_seconds: typing.Optional[jsii.Number] = None,
        maximum_retry_attempts: typing.Optional[jsii.Number] = None,
        metrics_config: typing.Optional[typing.Union["LambdaEventSourceMappingMetricsConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        parallelization_factor: typing.Optional[jsii.Number] = None,
        provisioned_poller_config: typing.Optional[typing.Union["LambdaEventSourceMappingProvisionedPollerConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        queues: typing.Optional[typing.Sequence[builtins.str]] = None,
        region: typing.Optional[builtins.str] = None,
        scaling_config: typing.Optional[typing.Union["LambdaEventSourceMappingScalingConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        self_managed_event_source: typing.Optional[typing.Union["LambdaEventSourceMappingSelfManagedEventSource", typing.Dict[builtins.str, typing.Any]]] = None,
        self_managed_kafka_event_source_config: typing.Optional[typing.Union["LambdaEventSourceMappingSelfManagedKafkaEventSourceConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        source_access_configuration: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["LambdaEventSourceMappingSourceAccessConfiguration", typing.Dict[builtins.str, typing.Any]]]]] = None,
        starting_position: typing.Optional[builtins.str] = None,
        starting_position_timestamp: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        topics: typing.Optional[typing.Sequence[builtins.str]] = None,
        tumbling_window_in_seconds: typing.Optional[jsii.Number] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/lambda_event_source_mapping aws_lambda_event_source_mapping} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param function_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/lambda_event_source_mapping#function_name LambdaEventSourceMapping#function_name}.
        :param amazon_managed_kafka_event_source_config: amazon_managed_kafka_event_source_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/lambda_event_source_mapping#amazon_managed_kafka_event_source_config LambdaEventSourceMapping#amazon_managed_kafka_event_source_config}
        :param batch_size: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/lambda_event_source_mapping#batch_size LambdaEventSourceMapping#batch_size}.
        :param bisect_batch_on_function_error: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/lambda_event_source_mapping#bisect_batch_on_function_error LambdaEventSourceMapping#bisect_batch_on_function_error}.
        :param destination_config: destination_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/lambda_event_source_mapping#destination_config LambdaEventSourceMapping#destination_config}
        :param document_db_event_source_config: document_db_event_source_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/lambda_event_source_mapping#document_db_event_source_config LambdaEventSourceMapping#document_db_event_source_config}
        :param enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/lambda_event_source_mapping#enabled LambdaEventSourceMapping#enabled}.
        :param event_source_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/lambda_event_source_mapping#event_source_arn LambdaEventSourceMapping#event_source_arn}.
        :param filter_criteria: filter_criteria block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/lambda_event_source_mapping#filter_criteria LambdaEventSourceMapping#filter_criteria}
        :param function_response_types: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/lambda_event_source_mapping#function_response_types LambdaEventSourceMapping#function_response_types}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/lambda_event_source_mapping#id LambdaEventSourceMapping#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param kms_key_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/lambda_event_source_mapping#kms_key_arn LambdaEventSourceMapping#kms_key_arn}.
        :param maximum_batching_window_in_seconds: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/lambda_event_source_mapping#maximum_batching_window_in_seconds LambdaEventSourceMapping#maximum_batching_window_in_seconds}.
        :param maximum_record_age_in_seconds: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/lambda_event_source_mapping#maximum_record_age_in_seconds LambdaEventSourceMapping#maximum_record_age_in_seconds}.
        :param maximum_retry_attempts: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/lambda_event_source_mapping#maximum_retry_attempts LambdaEventSourceMapping#maximum_retry_attempts}.
        :param metrics_config: metrics_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/lambda_event_source_mapping#metrics_config LambdaEventSourceMapping#metrics_config}
        :param parallelization_factor: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/lambda_event_source_mapping#parallelization_factor LambdaEventSourceMapping#parallelization_factor}.
        :param provisioned_poller_config: provisioned_poller_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/lambda_event_source_mapping#provisioned_poller_config LambdaEventSourceMapping#provisioned_poller_config}
        :param queues: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/lambda_event_source_mapping#queues LambdaEventSourceMapping#queues}.
        :param region: Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/lambda_event_source_mapping#region LambdaEventSourceMapping#region}
        :param scaling_config: scaling_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/lambda_event_source_mapping#scaling_config LambdaEventSourceMapping#scaling_config}
        :param self_managed_event_source: self_managed_event_source block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/lambda_event_source_mapping#self_managed_event_source LambdaEventSourceMapping#self_managed_event_source}
        :param self_managed_kafka_event_source_config: self_managed_kafka_event_source_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/lambda_event_source_mapping#self_managed_kafka_event_source_config LambdaEventSourceMapping#self_managed_kafka_event_source_config}
        :param source_access_configuration: source_access_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/lambda_event_source_mapping#source_access_configuration LambdaEventSourceMapping#source_access_configuration}
        :param starting_position: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/lambda_event_source_mapping#starting_position LambdaEventSourceMapping#starting_position}.
        :param starting_position_timestamp: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/lambda_event_source_mapping#starting_position_timestamp LambdaEventSourceMapping#starting_position_timestamp}.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/lambda_event_source_mapping#tags LambdaEventSourceMapping#tags}.
        :param tags_all: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/lambda_event_source_mapping#tags_all LambdaEventSourceMapping#tags_all}.
        :param topics: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/lambda_event_source_mapping#topics LambdaEventSourceMapping#topics}.
        :param tumbling_window_in_seconds: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/lambda_event_source_mapping#tumbling_window_in_seconds LambdaEventSourceMapping#tumbling_window_in_seconds}.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a47aa757339e69266d744016f1501724d691ed438cc3614599356c063048c58)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = LambdaEventSourceMappingConfig(
            function_name=function_name,
            amazon_managed_kafka_event_source_config=amazon_managed_kafka_event_source_config,
            batch_size=batch_size,
            bisect_batch_on_function_error=bisect_batch_on_function_error,
            destination_config=destination_config,
            document_db_event_source_config=document_db_event_source_config,
            enabled=enabled,
            event_source_arn=event_source_arn,
            filter_criteria=filter_criteria,
            function_response_types=function_response_types,
            id=id,
            kms_key_arn=kms_key_arn,
            maximum_batching_window_in_seconds=maximum_batching_window_in_seconds,
            maximum_record_age_in_seconds=maximum_record_age_in_seconds,
            maximum_retry_attempts=maximum_retry_attempts,
            metrics_config=metrics_config,
            parallelization_factor=parallelization_factor,
            provisioned_poller_config=provisioned_poller_config,
            queues=queues,
            region=region,
            scaling_config=scaling_config,
            self_managed_event_source=self_managed_event_source,
            self_managed_kafka_event_source_config=self_managed_kafka_event_source_config,
            source_access_configuration=source_access_configuration,
            starting_position=starting_position,
            starting_position_timestamp=starting_position_timestamp,
            tags=tags,
            tags_all=tags_all,
            topics=topics,
            tumbling_window_in_seconds=tumbling_window_in_seconds,
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
        '''Generates CDKTF code for importing a LambdaEventSourceMapping resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the LambdaEventSourceMapping to import.
        :param import_from_id: The id of the existing LambdaEventSourceMapping that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/lambda_event_source_mapping#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the LambdaEventSourceMapping to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eea8d2c5ee08d34f355c98fd659c6fe71200fbc91bb8d39c5bb0f36c148cf2aa)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putAmazonManagedKafkaEventSourceConfig")
    def put_amazon_managed_kafka_event_source_config(
        self,
        *,
        consumer_group_id: typing.Optional[builtins.str] = None,
        schema_registry_config: typing.Optional[typing.Union["LambdaEventSourceMappingAmazonManagedKafkaEventSourceConfigSchemaRegistryConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param consumer_group_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/lambda_event_source_mapping#consumer_group_id LambdaEventSourceMapping#consumer_group_id}.
        :param schema_registry_config: schema_registry_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/lambda_event_source_mapping#schema_registry_config LambdaEventSourceMapping#schema_registry_config}
        '''
        value = LambdaEventSourceMappingAmazonManagedKafkaEventSourceConfig(
            consumer_group_id=consumer_group_id,
            schema_registry_config=schema_registry_config,
        )

        return typing.cast(None, jsii.invoke(self, "putAmazonManagedKafkaEventSourceConfig", [value]))

    @jsii.member(jsii_name="putDestinationConfig")
    def put_destination_config(
        self,
        *,
        on_failure: typing.Optional[typing.Union["LambdaEventSourceMappingDestinationConfigOnFailure", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param on_failure: on_failure block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/lambda_event_source_mapping#on_failure LambdaEventSourceMapping#on_failure}
        '''
        value = LambdaEventSourceMappingDestinationConfig(on_failure=on_failure)

        return typing.cast(None, jsii.invoke(self, "putDestinationConfig", [value]))

    @jsii.member(jsii_name="putDocumentDbEventSourceConfig")
    def put_document_db_event_source_config(
        self,
        *,
        database_name: builtins.str,
        collection_name: typing.Optional[builtins.str] = None,
        full_document: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param database_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/lambda_event_source_mapping#database_name LambdaEventSourceMapping#database_name}.
        :param collection_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/lambda_event_source_mapping#collection_name LambdaEventSourceMapping#collection_name}.
        :param full_document: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/lambda_event_source_mapping#full_document LambdaEventSourceMapping#full_document}.
        '''
        value = LambdaEventSourceMappingDocumentDbEventSourceConfig(
            database_name=database_name,
            collection_name=collection_name,
            full_document=full_document,
        )

        return typing.cast(None, jsii.invoke(self, "putDocumentDbEventSourceConfig", [value]))

    @jsii.member(jsii_name="putFilterCriteria")
    def put_filter_criteria(
        self,
        *,
        filter: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["LambdaEventSourceMappingFilterCriteriaFilter", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param filter: filter block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/lambda_event_source_mapping#filter LambdaEventSourceMapping#filter}
        '''
        value = LambdaEventSourceMappingFilterCriteria(filter=filter)

        return typing.cast(None, jsii.invoke(self, "putFilterCriteria", [value]))

    @jsii.member(jsii_name="putMetricsConfig")
    def put_metrics_config(self, *, metrics: typing.Sequence[builtins.str]) -> None:
        '''
        :param metrics: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/lambda_event_source_mapping#metrics LambdaEventSourceMapping#metrics}.
        '''
        value = LambdaEventSourceMappingMetricsConfig(metrics=metrics)

        return typing.cast(None, jsii.invoke(self, "putMetricsConfig", [value]))

    @jsii.member(jsii_name="putProvisionedPollerConfig")
    def put_provisioned_poller_config(
        self,
        *,
        maximum_pollers: typing.Optional[jsii.Number] = None,
        minimum_pollers: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param maximum_pollers: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/lambda_event_source_mapping#maximum_pollers LambdaEventSourceMapping#maximum_pollers}.
        :param minimum_pollers: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/lambda_event_source_mapping#minimum_pollers LambdaEventSourceMapping#minimum_pollers}.
        '''
        value = LambdaEventSourceMappingProvisionedPollerConfig(
            maximum_pollers=maximum_pollers, minimum_pollers=minimum_pollers
        )

        return typing.cast(None, jsii.invoke(self, "putProvisionedPollerConfig", [value]))

    @jsii.member(jsii_name="putScalingConfig")
    def put_scaling_config(
        self,
        *,
        maximum_concurrency: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param maximum_concurrency: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/lambda_event_source_mapping#maximum_concurrency LambdaEventSourceMapping#maximum_concurrency}.
        '''
        value = LambdaEventSourceMappingScalingConfig(
            maximum_concurrency=maximum_concurrency
        )

        return typing.cast(None, jsii.invoke(self, "putScalingConfig", [value]))

    @jsii.member(jsii_name="putSelfManagedEventSource")
    def put_self_managed_event_source(
        self,
        *,
        endpoints: typing.Mapping[builtins.str, builtins.str],
    ) -> None:
        '''
        :param endpoints: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/lambda_event_source_mapping#endpoints LambdaEventSourceMapping#endpoints}.
        '''
        value = LambdaEventSourceMappingSelfManagedEventSource(endpoints=endpoints)

        return typing.cast(None, jsii.invoke(self, "putSelfManagedEventSource", [value]))

    @jsii.member(jsii_name="putSelfManagedKafkaEventSourceConfig")
    def put_self_managed_kafka_event_source_config(
        self,
        *,
        consumer_group_id: typing.Optional[builtins.str] = None,
        schema_registry_config: typing.Optional[typing.Union["LambdaEventSourceMappingSelfManagedKafkaEventSourceConfigSchemaRegistryConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param consumer_group_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/lambda_event_source_mapping#consumer_group_id LambdaEventSourceMapping#consumer_group_id}.
        :param schema_registry_config: schema_registry_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/lambda_event_source_mapping#schema_registry_config LambdaEventSourceMapping#schema_registry_config}
        '''
        value = LambdaEventSourceMappingSelfManagedKafkaEventSourceConfig(
            consumer_group_id=consumer_group_id,
            schema_registry_config=schema_registry_config,
        )

        return typing.cast(None, jsii.invoke(self, "putSelfManagedKafkaEventSourceConfig", [value]))

    @jsii.member(jsii_name="putSourceAccessConfiguration")
    def put_source_access_configuration(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["LambdaEventSourceMappingSourceAccessConfiguration", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cbca3ef7ec0a8a1ad9afd45f93ea620f3993ef54f83d3249a3bb02da154137a0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putSourceAccessConfiguration", [value]))

    @jsii.member(jsii_name="resetAmazonManagedKafkaEventSourceConfig")
    def reset_amazon_managed_kafka_event_source_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAmazonManagedKafkaEventSourceConfig", []))

    @jsii.member(jsii_name="resetBatchSize")
    def reset_batch_size(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBatchSize", []))

    @jsii.member(jsii_name="resetBisectBatchOnFunctionError")
    def reset_bisect_batch_on_function_error(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBisectBatchOnFunctionError", []))

    @jsii.member(jsii_name="resetDestinationConfig")
    def reset_destination_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDestinationConfig", []))

    @jsii.member(jsii_name="resetDocumentDbEventSourceConfig")
    def reset_document_db_event_source_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDocumentDbEventSourceConfig", []))

    @jsii.member(jsii_name="resetEnabled")
    def reset_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnabled", []))

    @jsii.member(jsii_name="resetEventSourceArn")
    def reset_event_source_arn(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEventSourceArn", []))

    @jsii.member(jsii_name="resetFilterCriteria")
    def reset_filter_criteria(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFilterCriteria", []))

    @jsii.member(jsii_name="resetFunctionResponseTypes")
    def reset_function_response_types(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFunctionResponseTypes", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetKmsKeyArn")
    def reset_kms_key_arn(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKmsKeyArn", []))

    @jsii.member(jsii_name="resetMaximumBatchingWindowInSeconds")
    def reset_maximum_batching_window_in_seconds(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaximumBatchingWindowInSeconds", []))

    @jsii.member(jsii_name="resetMaximumRecordAgeInSeconds")
    def reset_maximum_record_age_in_seconds(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaximumRecordAgeInSeconds", []))

    @jsii.member(jsii_name="resetMaximumRetryAttempts")
    def reset_maximum_retry_attempts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaximumRetryAttempts", []))

    @jsii.member(jsii_name="resetMetricsConfig")
    def reset_metrics_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMetricsConfig", []))

    @jsii.member(jsii_name="resetParallelizationFactor")
    def reset_parallelization_factor(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetParallelizationFactor", []))

    @jsii.member(jsii_name="resetProvisionedPollerConfig")
    def reset_provisioned_poller_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProvisionedPollerConfig", []))

    @jsii.member(jsii_name="resetQueues")
    def reset_queues(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetQueues", []))

    @jsii.member(jsii_name="resetRegion")
    def reset_region(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegion", []))

    @jsii.member(jsii_name="resetScalingConfig")
    def reset_scaling_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetScalingConfig", []))

    @jsii.member(jsii_name="resetSelfManagedEventSource")
    def reset_self_managed_event_source(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSelfManagedEventSource", []))

    @jsii.member(jsii_name="resetSelfManagedKafkaEventSourceConfig")
    def reset_self_managed_kafka_event_source_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSelfManagedKafkaEventSourceConfig", []))

    @jsii.member(jsii_name="resetSourceAccessConfiguration")
    def reset_source_access_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSourceAccessConfiguration", []))

    @jsii.member(jsii_name="resetStartingPosition")
    def reset_starting_position(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStartingPosition", []))

    @jsii.member(jsii_name="resetStartingPositionTimestamp")
    def reset_starting_position_timestamp(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStartingPositionTimestamp", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

    @jsii.member(jsii_name="resetTagsAll")
    def reset_tags_all(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTagsAll", []))

    @jsii.member(jsii_name="resetTopics")
    def reset_topics(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTopics", []))

    @jsii.member(jsii_name="resetTumblingWindowInSeconds")
    def reset_tumbling_window_in_seconds(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTumblingWindowInSeconds", []))

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
    @jsii.member(jsii_name="amazonManagedKafkaEventSourceConfig")
    def amazon_managed_kafka_event_source_config(
        self,
    ) -> "LambdaEventSourceMappingAmazonManagedKafkaEventSourceConfigOutputReference":
        return typing.cast("LambdaEventSourceMappingAmazonManagedKafkaEventSourceConfigOutputReference", jsii.get(self, "amazonManagedKafkaEventSourceConfig"))

    @builtins.property
    @jsii.member(jsii_name="arn")
    def arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "arn"))

    @builtins.property
    @jsii.member(jsii_name="destinationConfig")
    def destination_config(
        self,
    ) -> "LambdaEventSourceMappingDestinationConfigOutputReference":
        return typing.cast("LambdaEventSourceMappingDestinationConfigOutputReference", jsii.get(self, "destinationConfig"))

    @builtins.property
    @jsii.member(jsii_name="documentDbEventSourceConfig")
    def document_db_event_source_config(
        self,
    ) -> "LambdaEventSourceMappingDocumentDbEventSourceConfigOutputReference":
        return typing.cast("LambdaEventSourceMappingDocumentDbEventSourceConfigOutputReference", jsii.get(self, "documentDbEventSourceConfig"))

    @builtins.property
    @jsii.member(jsii_name="filterCriteria")
    def filter_criteria(
        self,
    ) -> "LambdaEventSourceMappingFilterCriteriaOutputReference":
        return typing.cast("LambdaEventSourceMappingFilterCriteriaOutputReference", jsii.get(self, "filterCriteria"))

    @builtins.property
    @jsii.member(jsii_name="functionArn")
    def function_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "functionArn"))

    @builtins.property
    @jsii.member(jsii_name="lastModified")
    def last_modified(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "lastModified"))

    @builtins.property
    @jsii.member(jsii_name="lastProcessingResult")
    def last_processing_result(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "lastProcessingResult"))

    @builtins.property
    @jsii.member(jsii_name="metricsConfig")
    def metrics_config(self) -> "LambdaEventSourceMappingMetricsConfigOutputReference":
        return typing.cast("LambdaEventSourceMappingMetricsConfigOutputReference", jsii.get(self, "metricsConfig"))

    @builtins.property
    @jsii.member(jsii_name="provisionedPollerConfig")
    def provisioned_poller_config(
        self,
    ) -> "LambdaEventSourceMappingProvisionedPollerConfigOutputReference":
        return typing.cast("LambdaEventSourceMappingProvisionedPollerConfigOutputReference", jsii.get(self, "provisionedPollerConfig"))

    @builtins.property
    @jsii.member(jsii_name="scalingConfig")
    def scaling_config(self) -> "LambdaEventSourceMappingScalingConfigOutputReference":
        return typing.cast("LambdaEventSourceMappingScalingConfigOutputReference", jsii.get(self, "scalingConfig"))

    @builtins.property
    @jsii.member(jsii_name="selfManagedEventSource")
    def self_managed_event_source(
        self,
    ) -> "LambdaEventSourceMappingSelfManagedEventSourceOutputReference":
        return typing.cast("LambdaEventSourceMappingSelfManagedEventSourceOutputReference", jsii.get(self, "selfManagedEventSource"))

    @builtins.property
    @jsii.member(jsii_name="selfManagedKafkaEventSourceConfig")
    def self_managed_kafka_event_source_config(
        self,
    ) -> "LambdaEventSourceMappingSelfManagedKafkaEventSourceConfigOutputReference":
        return typing.cast("LambdaEventSourceMappingSelfManagedKafkaEventSourceConfigOutputReference", jsii.get(self, "selfManagedKafkaEventSourceConfig"))

    @builtins.property
    @jsii.member(jsii_name="sourceAccessConfiguration")
    def source_access_configuration(
        self,
    ) -> "LambdaEventSourceMappingSourceAccessConfigurationList":
        return typing.cast("LambdaEventSourceMappingSourceAccessConfigurationList", jsii.get(self, "sourceAccessConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="state")
    def state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "state"))

    @builtins.property
    @jsii.member(jsii_name="stateTransitionReason")
    def state_transition_reason(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "stateTransitionReason"))

    @builtins.property
    @jsii.member(jsii_name="uuid")
    def uuid(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "uuid"))

    @builtins.property
    @jsii.member(jsii_name="amazonManagedKafkaEventSourceConfigInput")
    def amazon_managed_kafka_event_source_config_input(
        self,
    ) -> typing.Optional["LambdaEventSourceMappingAmazonManagedKafkaEventSourceConfig"]:
        return typing.cast(typing.Optional["LambdaEventSourceMappingAmazonManagedKafkaEventSourceConfig"], jsii.get(self, "amazonManagedKafkaEventSourceConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="batchSizeInput")
    def batch_size_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "batchSizeInput"))

    @builtins.property
    @jsii.member(jsii_name="bisectBatchOnFunctionErrorInput")
    def bisect_batch_on_function_error_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "bisectBatchOnFunctionErrorInput"))

    @builtins.property
    @jsii.member(jsii_name="destinationConfigInput")
    def destination_config_input(
        self,
    ) -> typing.Optional["LambdaEventSourceMappingDestinationConfig"]:
        return typing.cast(typing.Optional["LambdaEventSourceMappingDestinationConfig"], jsii.get(self, "destinationConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="documentDbEventSourceConfigInput")
    def document_db_event_source_config_input(
        self,
    ) -> typing.Optional["LambdaEventSourceMappingDocumentDbEventSourceConfig"]:
        return typing.cast(typing.Optional["LambdaEventSourceMappingDocumentDbEventSourceConfig"], jsii.get(self, "documentDbEventSourceConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="enabledInput")
    def enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enabledInput"))

    @builtins.property
    @jsii.member(jsii_name="eventSourceArnInput")
    def event_source_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "eventSourceArnInput"))

    @builtins.property
    @jsii.member(jsii_name="filterCriteriaInput")
    def filter_criteria_input(
        self,
    ) -> typing.Optional["LambdaEventSourceMappingFilterCriteria"]:
        return typing.cast(typing.Optional["LambdaEventSourceMappingFilterCriteria"], jsii.get(self, "filterCriteriaInput"))

    @builtins.property
    @jsii.member(jsii_name="functionNameInput")
    def function_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "functionNameInput"))

    @builtins.property
    @jsii.member(jsii_name="functionResponseTypesInput")
    def function_response_types_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "functionResponseTypesInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="kmsKeyArnInput")
    def kms_key_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "kmsKeyArnInput"))

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
    @jsii.member(jsii_name="metricsConfigInput")
    def metrics_config_input(
        self,
    ) -> typing.Optional["LambdaEventSourceMappingMetricsConfig"]:
        return typing.cast(typing.Optional["LambdaEventSourceMappingMetricsConfig"], jsii.get(self, "metricsConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="parallelizationFactorInput")
    def parallelization_factor_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "parallelizationFactorInput"))

    @builtins.property
    @jsii.member(jsii_name="provisionedPollerConfigInput")
    def provisioned_poller_config_input(
        self,
    ) -> typing.Optional["LambdaEventSourceMappingProvisionedPollerConfig"]:
        return typing.cast(typing.Optional["LambdaEventSourceMappingProvisionedPollerConfig"], jsii.get(self, "provisionedPollerConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="queuesInput")
    def queues_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "queuesInput"))

    @builtins.property
    @jsii.member(jsii_name="regionInput")
    def region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regionInput"))

    @builtins.property
    @jsii.member(jsii_name="scalingConfigInput")
    def scaling_config_input(
        self,
    ) -> typing.Optional["LambdaEventSourceMappingScalingConfig"]:
        return typing.cast(typing.Optional["LambdaEventSourceMappingScalingConfig"], jsii.get(self, "scalingConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="selfManagedEventSourceInput")
    def self_managed_event_source_input(
        self,
    ) -> typing.Optional["LambdaEventSourceMappingSelfManagedEventSource"]:
        return typing.cast(typing.Optional["LambdaEventSourceMappingSelfManagedEventSource"], jsii.get(self, "selfManagedEventSourceInput"))

    @builtins.property
    @jsii.member(jsii_name="selfManagedKafkaEventSourceConfigInput")
    def self_managed_kafka_event_source_config_input(
        self,
    ) -> typing.Optional["LambdaEventSourceMappingSelfManagedKafkaEventSourceConfig"]:
        return typing.cast(typing.Optional["LambdaEventSourceMappingSelfManagedKafkaEventSourceConfig"], jsii.get(self, "selfManagedKafkaEventSourceConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceAccessConfigurationInput")
    def source_access_configuration_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["LambdaEventSourceMappingSourceAccessConfiguration"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["LambdaEventSourceMappingSourceAccessConfiguration"]]], jsii.get(self, "sourceAccessConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="startingPositionInput")
    def starting_position_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "startingPositionInput"))

    @builtins.property
    @jsii.member(jsii_name="startingPositionTimestampInput")
    def starting_position_timestamp_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "startingPositionTimestampInput"))

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
    @jsii.member(jsii_name="topicsInput")
    def topics_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "topicsInput"))

    @builtins.property
    @jsii.member(jsii_name="tumblingWindowInSecondsInput")
    def tumbling_window_in_seconds_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "tumblingWindowInSecondsInput"))

    @builtins.property
    @jsii.member(jsii_name="batchSize")
    def batch_size(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "batchSize"))

    @batch_size.setter
    def batch_size(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__541561415b9451234dacc6dcb3a8b7a5fe5fd4a7af017fb0f870e1133ddc8646)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "batchSize", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="bisectBatchOnFunctionError")
    def bisect_batch_on_function_error(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "bisectBatchOnFunctionError"))

    @bisect_batch_on_function_error.setter
    def bisect_batch_on_function_error(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ad19047a73254501ebee29526fb3b3ad7cda341fd1a4cd8b5086fa0f976d6612)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bisectBatchOnFunctionError", value) # pyright: ignore[reportArgumentType]

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
            type_hints = typing.get_type_hints(_typecheckingstub__ad70d04d1e3f4cf084aa26ef29f1c7c59724e7c8f8976d27fdbc698db3e55742)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="eventSourceArn")
    def event_source_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "eventSourceArn"))

    @event_source_arn.setter
    def event_source_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__25dc16d1d8da84542069b020c23aec363f4216cc95a98064d54479c7dab33671)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "eventSourceArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="functionName")
    def function_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "functionName"))

    @function_name.setter
    def function_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8c5007634a0b77af02f6cadca8b2bcbbf8db9b6272bd817bc2fce50c7cb023f3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "functionName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="functionResponseTypes")
    def function_response_types(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "functionResponseTypes"))

    @function_response_types.setter
    def function_response_types(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f1bd5ee9b15aa474173407dbbfbf9105cbeaa5930dedf098446736fd5afff22)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "functionResponseTypes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__39050b5f603238cbae08d6e92e8499f00f28afbb26311d2e2847848f7c3e7591)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="kmsKeyArn")
    def kms_key_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kmsKeyArn"))

    @kms_key_arn.setter
    def kms_key_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ef2617f2c1ca86215d5aa08948cb8ce3c0f25742d311827dd7853747d1a20f24)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsKeyArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maximumBatchingWindowInSeconds")
    def maximum_batching_window_in_seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maximumBatchingWindowInSeconds"))

    @maximum_batching_window_in_seconds.setter
    def maximum_batching_window_in_seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__007a021ea006cac974f544b05437524be45ecbbea5b8a78164d858df1dc784e7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maximumBatchingWindowInSeconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maximumRecordAgeInSeconds")
    def maximum_record_age_in_seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maximumRecordAgeInSeconds"))

    @maximum_record_age_in_seconds.setter
    def maximum_record_age_in_seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf5f5ae47a9906e08465db2184f08779fa1689cac2e02f711eb8c53f6f79d981)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maximumRecordAgeInSeconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maximumRetryAttempts")
    def maximum_retry_attempts(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maximumRetryAttempts"))

    @maximum_retry_attempts.setter
    def maximum_retry_attempts(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a3d838cef1136da132b8bc289f46ead1c226ed7f67d9c262aee72948e00c30a1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maximumRetryAttempts", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="parallelizationFactor")
    def parallelization_factor(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "parallelizationFactor"))

    @parallelization_factor.setter
    def parallelization_factor(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__287ea91a1d6fb462d2b2456cdd406eb601a97f2e9ed98fa645d53ae38934ef73)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "parallelizationFactor", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="queues")
    def queues(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "queues"))

    @queues.setter
    def queues(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__46b7dc53557152da3e91935d8f0830c85c6557f96bccb8abe011af284497cd7a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "queues", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__95c097ac28a73f90f126727828c925fcf62485bfc4aa6a8532f808271809b4ef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="startingPosition")
    def starting_position(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "startingPosition"))

    @starting_position.setter
    def starting_position(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d34d647942528ee7ce024140746bc344b6c6ac28931ecc0006604fcd0e246a10)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "startingPosition", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="startingPositionTimestamp")
    def starting_position_timestamp(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "startingPositionTimestamp"))

    @starting_position_timestamp.setter
    def starting_position_timestamp(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__60b0493ea45885b9b7252fcddb33c43c5209138dda3596a7e1c80907cdbf97fb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "startingPositionTimestamp", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a39f0dcd86e82622cde53a8f58cdad8e10a19eacf50c8ee402a2819d9808b6f0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tagsAll")
    def tags_all(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tagsAll"))

    @tags_all.setter
    def tags_all(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2a1169e5dc647d74632c5b9344a5ce70df99d14c1e4e58593f07d8a4a19b3fd7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tagsAll", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="topics")
    def topics(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "topics"))

    @topics.setter
    def topics(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7d057d80fb2aaa0997a9ee926dbe4dac093c30664f420d247f34f0689c8a100b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "topics", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tumblingWindowInSeconds")
    def tumbling_window_in_seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "tumblingWindowInSeconds"))

    @tumbling_window_in_seconds.setter
    def tumbling_window_in_seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__57fc9d9b567503596648cb9a88e55911cf97c51725effa41974546916a0638b3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tumblingWindowInSeconds", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.lambdaEventSourceMapping.LambdaEventSourceMappingAmazonManagedKafkaEventSourceConfig",
    jsii_struct_bases=[],
    name_mapping={
        "consumer_group_id": "consumerGroupId",
        "schema_registry_config": "schemaRegistryConfig",
    },
)
class LambdaEventSourceMappingAmazonManagedKafkaEventSourceConfig:
    def __init__(
        self,
        *,
        consumer_group_id: typing.Optional[builtins.str] = None,
        schema_registry_config: typing.Optional[typing.Union["LambdaEventSourceMappingAmazonManagedKafkaEventSourceConfigSchemaRegistryConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param consumer_group_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/lambda_event_source_mapping#consumer_group_id LambdaEventSourceMapping#consumer_group_id}.
        :param schema_registry_config: schema_registry_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/lambda_event_source_mapping#schema_registry_config LambdaEventSourceMapping#schema_registry_config}
        '''
        if isinstance(schema_registry_config, dict):
            schema_registry_config = LambdaEventSourceMappingAmazonManagedKafkaEventSourceConfigSchemaRegistryConfig(**schema_registry_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ae07895fe3063469b17db40b7a275858ff5d4c6bffee563124c804bda7c3861)
            check_type(argname="argument consumer_group_id", value=consumer_group_id, expected_type=type_hints["consumer_group_id"])
            check_type(argname="argument schema_registry_config", value=schema_registry_config, expected_type=type_hints["schema_registry_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if consumer_group_id is not None:
            self._values["consumer_group_id"] = consumer_group_id
        if schema_registry_config is not None:
            self._values["schema_registry_config"] = schema_registry_config

    @builtins.property
    def consumer_group_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/lambda_event_source_mapping#consumer_group_id LambdaEventSourceMapping#consumer_group_id}.'''
        result = self._values.get("consumer_group_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def schema_registry_config(
        self,
    ) -> typing.Optional["LambdaEventSourceMappingAmazonManagedKafkaEventSourceConfigSchemaRegistryConfig"]:
        '''schema_registry_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/lambda_event_source_mapping#schema_registry_config LambdaEventSourceMapping#schema_registry_config}
        '''
        result = self._values.get("schema_registry_config")
        return typing.cast(typing.Optional["LambdaEventSourceMappingAmazonManagedKafkaEventSourceConfigSchemaRegistryConfig"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LambdaEventSourceMappingAmazonManagedKafkaEventSourceConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LambdaEventSourceMappingAmazonManagedKafkaEventSourceConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.lambdaEventSourceMapping.LambdaEventSourceMappingAmazonManagedKafkaEventSourceConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3357452e9a4b48f8661e21aa1beb11ae1098859cc02011d784871e61b0bd1ab2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putSchemaRegistryConfig")
    def put_schema_registry_config(
        self,
        *,
        access_config: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["LambdaEventSourceMappingAmazonManagedKafkaEventSourceConfigSchemaRegistryConfigAccessConfig", typing.Dict[builtins.str, typing.Any]]]]] = None,
        event_record_format: typing.Optional[builtins.str] = None,
        schema_registry_uri: typing.Optional[builtins.str] = None,
        schema_validation_config: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["LambdaEventSourceMappingAmazonManagedKafkaEventSourceConfigSchemaRegistryConfigSchemaValidationConfig", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param access_config: access_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/lambda_event_source_mapping#access_config LambdaEventSourceMapping#access_config}
        :param event_record_format: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/lambda_event_source_mapping#event_record_format LambdaEventSourceMapping#event_record_format}.
        :param schema_registry_uri: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/lambda_event_source_mapping#schema_registry_uri LambdaEventSourceMapping#schema_registry_uri}.
        :param schema_validation_config: schema_validation_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/lambda_event_source_mapping#schema_validation_config LambdaEventSourceMapping#schema_validation_config}
        '''
        value = LambdaEventSourceMappingAmazonManagedKafkaEventSourceConfigSchemaRegistryConfig(
            access_config=access_config,
            event_record_format=event_record_format,
            schema_registry_uri=schema_registry_uri,
            schema_validation_config=schema_validation_config,
        )

        return typing.cast(None, jsii.invoke(self, "putSchemaRegistryConfig", [value]))

    @jsii.member(jsii_name="resetConsumerGroupId")
    def reset_consumer_group_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConsumerGroupId", []))

    @jsii.member(jsii_name="resetSchemaRegistryConfig")
    def reset_schema_registry_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSchemaRegistryConfig", []))

    @builtins.property
    @jsii.member(jsii_name="schemaRegistryConfig")
    def schema_registry_config(
        self,
    ) -> "LambdaEventSourceMappingAmazonManagedKafkaEventSourceConfigSchemaRegistryConfigOutputReference":
        return typing.cast("LambdaEventSourceMappingAmazonManagedKafkaEventSourceConfigSchemaRegistryConfigOutputReference", jsii.get(self, "schemaRegistryConfig"))

    @builtins.property
    @jsii.member(jsii_name="consumerGroupIdInput")
    def consumer_group_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "consumerGroupIdInput"))

    @builtins.property
    @jsii.member(jsii_name="schemaRegistryConfigInput")
    def schema_registry_config_input(
        self,
    ) -> typing.Optional["LambdaEventSourceMappingAmazonManagedKafkaEventSourceConfigSchemaRegistryConfig"]:
        return typing.cast(typing.Optional["LambdaEventSourceMappingAmazonManagedKafkaEventSourceConfigSchemaRegistryConfig"], jsii.get(self, "schemaRegistryConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="consumerGroupId")
    def consumer_group_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "consumerGroupId"))

    @consumer_group_id.setter
    def consumer_group_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b1bbd65537fdf9a8bed47da88de63a4724981a8abad1ec09f1ca2dc00d76ccf9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "consumerGroupId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[LambdaEventSourceMappingAmazonManagedKafkaEventSourceConfig]:
        return typing.cast(typing.Optional[LambdaEventSourceMappingAmazonManagedKafkaEventSourceConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[LambdaEventSourceMappingAmazonManagedKafkaEventSourceConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__241b103203a35602f493d8495dce6ae9d90c439c6faa223564d7a63305710b64)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.lambdaEventSourceMapping.LambdaEventSourceMappingAmazonManagedKafkaEventSourceConfigSchemaRegistryConfig",
    jsii_struct_bases=[],
    name_mapping={
        "access_config": "accessConfig",
        "event_record_format": "eventRecordFormat",
        "schema_registry_uri": "schemaRegistryUri",
        "schema_validation_config": "schemaValidationConfig",
    },
)
class LambdaEventSourceMappingAmazonManagedKafkaEventSourceConfigSchemaRegistryConfig:
    def __init__(
        self,
        *,
        access_config: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["LambdaEventSourceMappingAmazonManagedKafkaEventSourceConfigSchemaRegistryConfigAccessConfig", typing.Dict[builtins.str, typing.Any]]]]] = None,
        event_record_format: typing.Optional[builtins.str] = None,
        schema_registry_uri: typing.Optional[builtins.str] = None,
        schema_validation_config: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["LambdaEventSourceMappingAmazonManagedKafkaEventSourceConfigSchemaRegistryConfigSchemaValidationConfig", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param access_config: access_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/lambda_event_source_mapping#access_config LambdaEventSourceMapping#access_config}
        :param event_record_format: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/lambda_event_source_mapping#event_record_format LambdaEventSourceMapping#event_record_format}.
        :param schema_registry_uri: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/lambda_event_source_mapping#schema_registry_uri LambdaEventSourceMapping#schema_registry_uri}.
        :param schema_validation_config: schema_validation_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/lambda_event_source_mapping#schema_validation_config LambdaEventSourceMapping#schema_validation_config}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a1228503797be6f1fb7ee84671caddc1d96ccb035289d8de7c6cf9f6c984d080)
            check_type(argname="argument access_config", value=access_config, expected_type=type_hints["access_config"])
            check_type(argname="argument event_record_format", value=event_record_format, expected_type=type_hints["event_record_format"])
            check_type(argname="argument schema_registry_uri", value=schema_registry_uri, expected_type=type_hints["schema_registry_uri"])
            check_type(argname="argument schema_validation_config", value=schema_validation_config, expected_type=type_hints["schema_validation_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if access_config is not None:
            self._values["access_config"] = access_config
        if event_record_format is not None:
            self._values["event_record_format"] = event_record_format
        if schema_registry_uri is not None:
            self._values["schema_registry_uri"] = schema_registry_uri
        if schema_validation_config is not None:
            self._values["schema_validation_config"] = schema_validation_config

    @builtins.property
    def access_config(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["LambdaEventSourceMappingAmazonManagedKafkaEventSourceConfigSchemaRegistryConfigAccessConfig"]]]:
        '''access_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/lambda_event_source_mapping#access_config LambdaEventSourceMapping#access_config}
        '''
        result = self._values.get("access_config")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["LambdaEventSourceMappingAmazonManagedKafkaEventSourceConfigSchemaRegistryConfigAccessConfig"]]], result)

    @builtins.property
    def event_record_format(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/lambda_event_source_mapping#event_record_format LambdaEventSourceMapping#event_record_format}.'''
        result = self._values.get("event_record_format")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def schema_registry_uri(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/lambda_event_source_mapping#schema_registry_uri LambdaEventSourceMapping#schema_registry_uri}.'''
        result = self._values.get("schema_registry_uri")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def schema_validation_config(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["LambdaEventSourceMappingAmazonManagedKafkaEventSourceConfigSchemaRegistryConfigSchemaValidationConfig"]]]:
        '''schema_validation_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/lambda_event_source_mapping#schema_validation_config LambdaEventSourceMapping#schema_validation_config}
        '''
        result = self._values.get("schema_validation_config")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["LambdaEventSourceMappingAmazonManagedKafkaEventSourceConfigSchemaRegistryConfigSchemaValidationConfig"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LambdaEventSourceMappingAmazonManagedKafkaEventSourceConfigSchemaRegistryConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.lambdaEventSourceMapping.LambdaEventSourceMappingAmazonManagedKafkaEventSourceConfigSchemaRegistryConfigAccessConfig",
    jsii_struct_bases=[],
    name_mapping={"type": "type", "uri": "uri"},
)
class LambdaEventSourceMappingAmazonManagedKafkaEventSourceConfigSchemaRegistryConfigAccessConfig:
    def __init__(
        self,
        *,
        type: typing.Optional[builtins.str] = None,
        uri: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/lambda_event_source_mapping#type LambdaEventSourceMapping#type}.
        :param uri: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/lambda_event_source_mapping#uri LambdaEventSourceMapping#uri}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9439b3a1f6b624d452711bc1b4072e5ad4709bf627d0f5e42b144e48eefe1ff1)
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument uri", value=uri, expected_type=type_hints["uri"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if type is not None:
            self._values["type"] = type
        if uri is not None:
            self._values["uri"] = uri

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/lambda_event_source_mapping#type LambdaEventSourceMapping#type}.'''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def uri(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/lambda_event_source_mapping#uri LambdaEventSourceMapping#uri}.'''
        result = self._values.get("uri")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LambdaEventSourceMappingAmazonManagedKafkaEventSourceConfigSchemaRegistryConfigAccessConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LambdaEventSourceMappingAmazonManagedKafkaEventSourceConfigSchemaRegistryConfigAccessConfigList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.lambdaEventSourceMapping.LambdaEventSourceMappingAmazonManagedKafkaEventSourceConfigSchemaRegistryConfigAccessConfigList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5ff9494978ec5560b507caf669052b5a124a00e70e99d36fdfeabf3c423cd5fd)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "LambdaEventSourceMappingAmazonManagedKafkaEventSourceConfigSchemaRegistryConfigAccessConfigOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8cd212c066733892ac2f3c061249f48df6b45c4d64272f06fcb238ad883e8f33)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("LambdaEventSourceMappingAmazonManagedKafkaEventSourceConfigSchemaRegistryConfigAccessConfigOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dcddf575110667e2f1ecfae2853c2157e61be54499449b173e43c8b0bf3d7a80)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7f3796a43e4e289ff638f3852159c36c185f642c1de05fd40509a8ee9f847081)
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
            type_hints = typing.get_type_hints(_typecheckingstub__342802512fb8c4a67f2aeabf3298720ed2c6a419c8925c8a89f3bd0311275ffb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LambdaEventSourceMappingAmazonManagedKafkaEventSourceConfigSchemaRegistryConfigAccessConfig]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LambdaEventSourceMappingAmazonManagedKafkaEventSourceConfigSchemaRegistryConfigAccessConfig]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LambdaEventSourceMappingAmazonManagedKafkaEventSourceConfigSchemaRegistryConfigAccessConfig]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a5c8c1d37bc8498378e230d6706158029f3f338a0e189082c87fb5f6cd7fe6c0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class LambdaEventSourceMappingAmazonManagedKafkaEventSourceConfigSchemaRegistryConfigAccessConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.lambdaEventSourceMapping.LambdaEventSourceMappingAmazonManagedKafkaEventSourceConfigSchemaRegistryConfigAccessConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ec31a9cae0e5bd64c6b40f69ad6ee7df35afc62cd605318e86ad6f2e45e89d53)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetType")
    def reset_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetType", []))

    @jsii.member(jsii_name="resetUri")
    def reset_uri(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUri", []))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="uriInput")
    def uri_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "uriInput"))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c1a055200d74fabbb10b904a2a3ac60e17c38c3bc64e215b6025a85ceb5e210c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="uri")
    def uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "uri"))

    @uri.setter
    def uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__96961dfe44954843fcbe469268db6fa64365e7bc704c236f5dade2e4070f4b54)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "uri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LambdaEventSourceMappingAmazonManagedKafkaEventSourceConfigSchemaRegistryConfigAccessConfig]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LambdaEventSourceMappingAmazonManagedKafkaEventSourceConfigSchemaRegistryConfigAccessConfig]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LambdaEventSourceMappingAmazonManagedKafkaEventSourceConfigSchemaRegistryConfigAccessConfig]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc6eba6d2672c96c16de1ad747ece15f532c4b05cbc617ad60de024de733f72d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class LambdaEventSourceMappingAmazonManagedKafkaEventSourceConfigSchemaRegistryConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.lambdaEventSourceMapping.LambdaEventSourceMappingAmazonManagedKafkaEventSourceConfigSchemaRegistryConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0c2ce45696a4d4f4884210e621e2096f7a585eb7543218ba7a92e5a1caad3eaa)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAccessConfig")
    def put_access_config(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[LambdaEventSourceMappingAmazonManagedKafkaEventSourceConfigSchemaRegistryConfigAccessConfig, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__409a99b2353ee73a231c34d8d0fd3df0a28e7aa4442a1694a15837b7c940e57e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putAccessConfig", [value]))

    @jsii.member(jsii_name="putSchemaValidationConfig")
    def put_schema_validation_config(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["LambdaEventSourceMappingAmazonManagedKafkaEventSourceConfigSchemaRegistryConfigSchemaValidationConfig", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e12f30e799da5c8df543a64ed5045d5ca16c2aff83a89ef42362b734d97d15c0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putSchemaValidationConfig", [value]))

    @jsii.member(jsii_name="resetAccessConfig")
    def reset_access_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAccessConfig", []))

    @jsii.member(jsii_name="resetEventRecordFormat")
    def reset_event_record_format(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEventRecordFormat", []))

    @jsii.member(jsii_name="resetSchemaRegistryUri")
    def reset_schema_registry_uri(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSchemaRegistryUri", []))

    @jsii.member(jsii_name="resetSchemaValidationConfig")
    def reset_schema_validation_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSchemaValidationConfig", []))

    @builtins.property
    @jsii.member(jsii_name="accessConfig")
    def access_config(
        self,
    ) -> LambdaEventSourceMappingAmazonManagedKafkaEventSourceConfigSchemaRegistryConfigAccessConfigList:
        return typing.cast(LambdaEventSourceMappingAmazonManagedKafkaEventSourceConfigSchemaRegistryConfigAccessConfigList, jsii.get(self, "accessConfig"))

    @builtins.property
    @jsii.member(jsii_name="schemaValidationConfig")
    def schema_validation_config(
        self,
    ) -> "LambdaEventSourceMappingAmazonManagedKafkaEventSourceConfigSchemaRegistryConfigSchemaValidationConfigList":
        return typing.cast("LambdaEventSourceMappingAmazonManagedKafkaEventSourceConfigSchemaRegistryConfigSchemaValidationConfigList", jsii.get(self, "schemaValidationConfig"))

    @builtins.property
    @jsii.member(jsii_name="accessConfigInput")
    def access_config_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LambdaEventSourceMappingAmazonManagedKafkaEventSourceConfigSchemaRegistryConfigAccessConfig]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LambdaEventSourceMappingAmazonManagedKafkaEventSourceConfigSchemaRegistryConfigAccessConfig]]], jsii.get(self, "accessConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="eventRecordFormatInput")
    def event_record_format_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "eventRecordFormatInput"))

    @builtins.property
    @jsii.member(jsii_name="schemaRegistryUriInput")
    def schema_registry_uri_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "schemaRegistryUriInput"))

    @builtins.property
    @jsii.member(jsii_name="schemaValidationConfigInput")
    def schema_validation_config_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["LambdaEventSourceMappingAmazonManagedKafkaEventSourceConfigSchemaRegistryConfigSchemaValidationConfig"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["LambdaEventSourceMappingAmazonManagedKafkaEventSourceConfigSchemaRegistryConfigSchemaValidationConfig"]]], jsii.get(self, "schemaValidationConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="eventRecordFormat")
    def event_record_format(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "eventRecordFormat"))

    @event_record_format.setter
    def event_record_format(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0242f9a854bf10317f39c8c7aac19b8493e7d705478bcdc802d49b5ae17675a2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "eventRecordFormat", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="schemaRegistryUri")
    def schema_registry_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "schemaRegistryUri"))

    @schema_registry_uri.setter
    def schema_registry_uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bafd529b50fdc62b8f211210a3e197809075bc97fb833d08dbebf3c6ca8fca7a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "schemaRegistryUri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[LambdaEventSourceMappingAmazonManagedKafkaEventSourceConfigSchemaRegistryConfig]:
        return typing.cast(typing.Optional[LambdaEventSourceMappingAmazonManagedKafkaEventSourceConfigSchemaRegistryConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[LambdaEventSourceMappingAmazonManagedKafkaEventSourceConfigSchemaRegistryConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c914fb09d08a44aa3aab0e6103157903794054ed0acd0244ab9497429d736aa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.lambdaEventSourceMapping.LambdaEventSourceMappingAmazonManagedKafkaEventSourceConfigSchemaRegistryConfigSchemaValidationConfig",
    jsii_struct_bases=[],
    name_mapping={"attribute": "attribute"},
)
class LambdaEventSourceMappingAmazonManagedKafkaEventSourceConfigSchemaRegistryConfigSchemaValidationConfig:
    def __init__(self, *, attribute: typing.Optional[builtins.str] = None) -> None:
        '''
        :param attribute: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/lambda_event_source_mapping#attribute LambdaEventSourceMapping#attribute}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__706d41aa498034f15f6e499755770b0656324eda2504effd714ff32454b5ee21)
            check_type(argname="argument attribute", value=attribute, expected_type=type_hints["attribute"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if attribute is not None:
            self._values["attribute"] = attribute

    @builtins.property
    def attribute(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/lambda_event_source_mapping#attribute LambdaEventSourceMapping#attribute}.'''
        result = self._values.get("attribute")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LambdaEventSourceMappingAmazonManagedKafkaEventSourceConfigSchemaRegistryConfigSchemaValidationConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LambdaEventSourceMappingAmazonManagedKafkaEventSourceConfigSchemaRegistryConfigSchemaValidationConfigList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.lambdaEventSourceMapping.LambdaEventSourceMappingAmazonManagedKafkaEventSourceConfigSchemaRegistryConfigSchemaValidationConfigList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5aae456001749e806d28c535f045e0891f6f1b30248717344d32ffd82cd78d66)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "LambdaEventSourceMappingAmazonManagedKafkaEventSourceConfigSchemaRegistryConfigSchemaValidationConfigOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__924b8ec357102a191cc46f317fa6e869f57b4c4fa044b8ab9f55c996c1008362)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("LambdaEventSourceMappingAmazonManagedKafkaEventSourceConfigSchemaRegistryConfigSchemaValidationConfigOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b1970c3ae4889754beec49df7a38bc7c1fd388b634c4206f00af76687e4865fb)
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
            type_hints = typing.get_type_hints(_typecheckingstub__636105ddd2569e4d550b21f7e69276e32e98beacfaf0a5862e79d3aa6128bb04)
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
            type_hints = typing.get_type_hints(_typecheckingstub__18e677f6cc2aa33e2dab9cbbe1da71dd6351a0c37db6140372e6ab55f21b0f62)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LambdaEventSourceMappingAmazonManagedKafkaEventSourceConfigSchemaRegistryConfigSchemaValidationConfig]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LambdaEventSourceMappingAmazonManagedKafkaEventSourceConfigSchemaRegistryConfigSchemaValidationConfig]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LambdaEventSourceMappingAmazonManagedKafkaEventSourceConfigSchemaRegistryConfigSchemaValidationConfig]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6fd7ed7588e47a3084980edb377c07d2f8085a9ac46e1fa5482cdc00962d80c2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class LambdaEventSourceMappingAmazonManagedKafkaEventSourceConfigSchemaRegistryConfigSchemaValidationConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.lambdaEventSourceMapping.LambdaEventSourceMappingAmazonManagedKafkaEventSourceConfigSchemaRegistryConfigSchemaValidationConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3574d634b835dd3f34c924f6d865e399691fa0d4be95aefad89327ca838f498a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetAttribute")
    def reset_attribute(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAttribute", []))

    @builtins.property
    @jsii.member(jsii_name="attributeInput")
    def attribute_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "attributeInput"))

    @builtins.property
    @jsii.member(jsii_name="attribute")
    def attribute(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "attribute"))

    @attribute.setter
    def attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ebea400851b96720d66e6aaa6029f6edda3577ab160d89524c4c3006693be08c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "attribute", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LambdaEventSourceMappingAmazonManagedKafkaEventSourceConfigSchemaRegistryConfigSchemaValidationConfig]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LambdaEventSourceMappingAmazonManagedKafkaEventSourceConfigSchemaRegistryConfigSchemaValidationConfig]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LambdaEventSourceMappingAmazonManagedKafkaEventSourceConfigSchemaRegistryConfigSchemaValidationConfig]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0dd5ddf2b8a0b162c0751ab600550314512e618502c64a22e3aedaa596a5d3c3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.lambdaEventSourceMapping.LambdaEventSourceMappingConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "function_name": "functionName",
        "amazon_managed_kafka_event_source_config": "amazonManagedKafkaEventSourceConfig",
        "batch_size": "batchSize",
        "bisect_batch_on_function_error": "bisectBatchOnFunctionError",
        "destination_config": "destinationConfig",
        "document_db_event_source_config": "documentDbEventSourceConfig",
        "enabled": "enabled",
        "event_source_arn": "eventSourceArn",
        "filter_criteria": "filterCriteria",
        "function_response_types": "functionResponseTypes",
        "id": "id",
        "kms_key_arn": "kmsKeyArn",
        "maximum_batching_window_in_seconds": "maximumBatchingWindowInSeconds",
        "maximum_record_age_in_seconds": "maximumRecordAgeInSeconds",
        "maximum_retry_attempts": "maximumRetryAttempts",
        "metrics_config": "metricsConfig",
        "parallelization_factor": "parallelizationFactor",
        "provisioned_poller_config": "provisionedPollerConfig",
        "queues": "queues",
        "region": "region",
        "scaling_config": "scalingConfig",
        "self_managed_event_source": "selfManagedEventSource",
        "self_managed_kafka_event_source_config": "selfManagedKafkaEventSourceConfig",
        "source_access_configuration": "sourceAccessConfiguration",
        "starting_position": "startingPosition",
        "starting_position_timestamp": "startingPositionTimestamp",
        "tags": "tags",
        "tags_all": "tagsAll",
        "topics": "topics",
        "tumbling_window_in_seconds": "tumblingWindowInSeconds",
    },
)
class LambdaEventSourceMappingConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        function_name: builtins.str,
        amazon_managed_kafka_event_source_config: typing.Optional[typing.Union[LambdaEventSourceMappingAmazonManagedKafkaEventSourceConfig, typing.Dict[builtins.str, typing.Any]]] = None,
        batch_size: typing.Optional[jsii.Number] = None,
        bisect_batch_on_function_error: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        destination_config: typing.Optional[typing.Union["LambdaEventSourceMappingDestinationConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        document_db_event_source_config: typing.Optional[typing.Union["LambdaEventSourceMappingDocumentDbEventSourceConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        event_source_arn: typing.Optional[builtins.str] = None,
        filter_criteria: typing.Optional[typing.Union["LambdaEventSourceMappingFilterCriteria", typing.Dict[builtins.str, typing.Any]]] = None,
        function_response_types: typing.Optional[typing.Sequence[builtins.str]] = None,
        id: typing.Optional[builtins.str] = None,
        kms_key_arn: typing.Optional[builtins.str] = None,
        maximum_batching_window_in_seconds: typing.Optional[jsii.Number] = None,
        maximum_record_age_in_seconds: typing.Optional[jsii.Number] = None,
        maximum_retry_attempts: typing.Optional[jsii.Number] = None,
        metrics_config: typing.Optional[typing.Union["LambdaEventSourceMappingMetricsConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        parallelization_factor: typing.Optional[jsii.Number] = None,
        provisioned_poller_config: typing.Optional[typing.Union["LambdaEventSourceMappingProvisionedPollerConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        queues: typing.Optional[typing.Sequence[builtins.str]] = None,
        region: typing.Optional[builtins.str] = None,
        scaling_config: typing.Optional[typing.Union["LambdaEventSourceMappingScalingConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        self_managed_event_source: typing.Optional[typing.Union["LambdaEventSourceMappingSelfManagedEventSource", typing.Dict[builtins.str, typing.Any]]] = None,
        self_managed_kafka_event_source_config: typing.Optional[typing.Union["LambdaEventSourceMappingSelfManagedKafkaEventSourceConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        source_access_configuration: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["LambdaEventSourceMappingSourceAccessConfiguration", typing.Dict[builtins.str, typing.Any]]]]] = None,
        starting_position: typing.Optional[builtins.str] = None,
        starting_position_timestamp: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        topics: typing.Optional[typing.Sequence[builtins.str]] = None,
        tumbling_window_in_seconds: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param function_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/lambda_event_source_mapping#function_name LambdaEventSourceMapping#function_name}.
        :param amazon_managed_kafka_event_source_config: amazon_managed_kafka_event_source_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/lambda_event_source_mapping#amazon_managed_kafka_event_source_config LambdaEventSourceMapping#amazon_managed_kafka_event_source_config}
        :param batch_size: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/lambda_event_source_mapping#batch_size LambdaEventSourceMapping#batch_size}.
        :param bisect_batch_on_function_error: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/lambda_event_source_mapping#bisect_batch_on_function_error LambdaEventSourceMapping#bisect_batch_on_function_error}.
        :param destination_config: destination_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/lambda_event_source_mapping#destination_config LambdaEventSourceMapping#destination_config}
        :param document_db_event_source_config: document_db_event_source_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/lambda_event_source_mapping#document_db_event_source_config LambdaEventSourceMapping#document_db_event_source_config}
        :param enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/lambda_event_source_mapping#enabled LambdaEventSourceMapping#enabled}.
        :param event_source_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/lambda_event_source_mapping#event_source_arn LambdaEventSourceMapping#event_source_arn}.
        :param filter_criteria: filter_criteria block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/lambda_event_source_mapping#filter_criteria LambdaEventSourceMapping#filter_criteria}
        :param function_response_types: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/lambda_event_source_mapping#function_response_types LambdaEventSourceMapping#function_response_types}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/lambda_event_source_mapping#id LambdaEventSourceMapping#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param kms_key_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/lambda_event_source_mapping#kms_key_arn LambdaEventSourceMapping#kms_key_arn}.
        :param maximum_batching_window_in_seconds: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/lambda_event_source_mapping#maximum_batching_window_in_seconds LambdaEventSourceMapping#maximum_batching_window_in_seconds}.
        :param maximum_record_age_in_seconds: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/lambda_event_source_mapping#maximum_record_age_in_seconds LambdaEventSourceMapping#maximum_record_age_in_seconds}.
        :param maximum_retry_attempts: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/lambda_event_source_mapping#maximum_retry_attempts LambdaEventSourceMapping#maximum_retry_attempts}.
        :param metrics_config: metrics_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/lambda_event_source_mapping#metrics_config LambdaEventSourceMapping#metrics_config}
        :param parallelization_factor: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/lambda_event_source_mapping#parallelization_factor LambdaEventSourceMapping#parallelization_factor}.
        :param provisioned_poller_config: provisioned_poller_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/lambda_event_source_mapping#provisioned_poller_config LambdaEventSourceMapping#provisioned_poller_config}
        :param queues: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/lambda_event_source_mapping#queues LambdaEventSourceMapping#queues}.
        :param region: Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/lambda_event_source_mapping#region LambdaEventSourceMapping#region}
        :param scaling_config: scaling_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/lambda_event_source_mapping#scaling_config LambdaEventSourceMapping#scaling_config}
        :param self_managed_event_source: self_managed_event_source block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/lambda_event_source_mapping#self_managed_event_source LambdaEventSourceMapping#self_managed_event_source}
        :param self_managed_kafka_event_source_config: self_managed_kafka_event_source_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/lambda_event_source_mapping#self_managed_kafka_event_source_config LambdaEventSourceMapping#self_managed_kafka_event_source_config}
        :param source_access_configuration: source_access_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/lambda_event_source_mapping#source_access_configuration LambdaEventSourceMapping#source_access_configuration}
        :param starting_position: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/lambda_event_source_mapping#starting_position LambdaEventSourceMapping#starting_position}.
        :param starting_position_timestamp: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/lambda_event_source_mapping#starting_position_timestamp LambdaEventSourceMapping#starting_position_timestamp}.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/lambda_event_source_mapping#tags LambdaEventSourceMapping#tags}.
        :param tags_all: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/lambda_event_source_mapping#tags_all LambdaEventSourceMapping#tags_all}.
        :param topics: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/lambda_event_source_mapping#topics LambdaEventSourceMapping#topics}.
        :param tumbling_window_in_seconds: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/lambda_event_source_mapping#tumbling_window_in_seconds LambdaEventSourceMapping#tumbling_window_in_seconds}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(amazon_managed_kafka_event_source_config, dict):
            amazon_managed_kafka_event_source_config = LambdaEventSourceMappingAmazonManagedKafkaEventSourceConfig(**amazon_managed_kafka_event_source_config)
        if isinstance(destination_config, dict):
            destination_config = LambdaEventSourceMappingDestinationConfig(**destination_config)
        if isinstance(document_db_event_source_config, dict):
            document_db_event_source_config = LambdaEventSourceMappingDocumentDbEventSourceConfig(**document_db_event_source_config)
        if isinstance(filter_criteria, dict):
            filter_criteria = LambdaEventSourceMappingFilterCriteria(**filter_criteria)
        if isinstance(metrics_config, dict):
            metrics_config = LambdaEventSourceMappingMetricsConfig(**metrics_config)
        if isinstance(provisioned_poller_config, dict):
            provisioned_poller_config = LambdaEventSourceMappingProvisionedPollerConfig(**provisioned_poller_config)
        if isinstance(scaling_config, dict):
            scaling_config = LambdaEventSourceMappingScalingConfig(**scaling_config)
        if isinstance(self_managed_event_source, dict):
            self_managed_event_source = LambdaEventSourceMappingSelfManagedEventSource(**self_managed_event_source)
        if isinstance(self_managed_kafka_event_source_config, dict):
            self_managed_kafka_event_source_config = LambdaEventSourceMappingSelfManagedKafkaEventSourceConfig(**self_managed_kafka_event_source_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__64877458e53fece918bfc3ada09bc9c10e559b190aa510fbe6c6c28a73b186fa)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument function_name", value=function_name, expected_type=type_hints["function_name"])
            check_type(argname="argument amazon_managed_kafka_event_source_config", value=amazon_managed_kafka_event_source_config, expected_type=type_hints["amazon_managed_kafka_event_source_config"])
            check_type(argname="argument batch_size", value=batch_size, expected_type=type_hints["batch_size"])
            check_type(argname="argument bisect_batch_on_function_error", value=bisect_batch_on_function_error, expected_type=type_hints["bisect_batch_on_function_error"])
            check_type(argname="argument destination_config", value=destination_config, expected_type=type_hints["destination_config"])
            check_type(argname="argument document_db_event_source_config", value=document_db_event_source_config, expected_type=type_hints["document_db_event_source_config"])
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument event_source_arn", value=event_source_arn, expected_type=type_hints["event_source_arn"])
            check_type(argname="argument filter_criteria", value=filter_criteria, expected_type=type_hints["filter_criteria"])
            check_type(argname="argument function_response_types", value=function_response_types, expected_type=type_hints["function_response_types"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument kms_key_arn", value=kms_key_arn, expected_type=type_hints["kms_key_arn"])
            check_type(argname="argument maximum_batching_window_in_seconds", value=maximum_batching_window_in_seconds, expected_type=type_hints["maximum_batching_window_in_seconds"])
            check_type(argname="argument maximum_record_age_in_seconds", value=maximum_record_age_in_seconds, expected_type=type_hints["maximum_record_age_in_seconds"])
            check_type(argname="argument maximum_retry_attempts", value=maximum_retry_attempts, expected_type=type_hints["maximum_retry_attempts"])
            check_type(argname="argument metrics_config", value=metrics_config, expected_type=type_hints["metrics_config"])
            check_type(argname="argument parallelization_factor", value=parallelization_factor, expected_type=type_hints["parallelization_factor"])
            check_type(argname="argument provisioned_poller_config", value=provisioned_poller_config, expected_type=type_hints["provisioned_poller_config"])
            check_type(argname="argument queues", value=queues, expected_type=type_hints["queues"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument scaling_config", value=scaling_config, expected_type=type_hints["scaling_config"])
            check_type(argname="argument self_managed_event_source", value=self_managed_event_source, expected_type=type_hints["self_managed_event_source"])
            check_type(argname="argument self_managed_kafka_event_source_config", value=self_managed_kafka_event_source_config, expected_type=type_hints["self_managed_kafka_event_source_config"])
            check_type(argname="argument source_access_configuration", value=source_access_configuration, expected_type=type_hints["source_access_configuration"])
            check_type(argname="argument starting_position", value=starting_position, expected_type=type_hints["starting_position"])
            check_type(argname="argument starting_position_timestamp", value=starting_position_timestamp, expected_type=type_hints["starting_position_timestamp"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument tags_all", value=tags_all, expected_type=type_hints["tags_all"])
            check_type(argname="argument topics", value=topics, expected_type=type_hints["topics"])
            check_type(argname="argument tumbling_window_in_seconds", value=tumbling_window_in_seconds, expected_type=type_hints["tumbling_window_in_seconds"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "function_name": function_name,
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
        if amazon_managed_kafka_event_source_config is not None:
            self._values["amazon_managed_kafka_event_source_config"] = amazon_managed_kafka_event_source_config
        if batch_size is not None:
            self._values["batch_size"] = batch_size
        if bisect_batch_on_function_error is not None:
            self._values["bisect_batch_on_function_error"] = bisect_batch_on_function_error
        if destination_config is not None:
            self._values["destination_config"] = destination_config
        if document_db_event_source_config is not None:
            self._values["document_db_event_source_config"] = document_db_event_source_config
        if enabled is not None:
            self._values["enabled"] = enabled
        if event_source_arn is not None:
            self._values["event_source_arn"] = event_source_arn
        if filter_criteria is not None:
            self._values["filter_criteria"] = filter_criteria
        if function_response_types is not None:
            self._values["function_response_types"] = function_response_types
        if id is not None:
            self._values["id"] = id
        if kms_key_arn is not None:
            self._values["kms_key_arn"] = kms_key_arn
        if maximum_batching_window_in_seconds is not None:
            self._values["maximum_batching_window_in_seconds"] = maximum_batching_window_in_seconds
        if maximum_record_age_in_seconds is not None:
            self._values["maximum_record_age_in_seconds"] = maximum_record_age_in_seconds
        if maximum_retry_attempts is not None:
            self._values["maximum_retry_attempts"] = maximum_retry_attempts
        if metrics_config is not None:
            self._values["metrics_config"] = metrics_config
        if parallelization_factor is not None:
            self._values["parallelization_factor"] = parallelization_factor
        if provisioned_poller_config is not None:
            self._values["provisioned_poller_config"] = provisioned_poller_config
        if queues is not None:
            self._values["queues"] = queues
        if region is not None:
            self._values["region"] = region
        if scaling_config is not None:
            self._values["scaling_config"] = scaling_config
        if self_managed_event_source is not None:
            self._values["self_managed_event_source"] = self_managed_event_source
        if self_managed_kafka_event_source_config is not None:
            self._values["self_managed_kafka_event_source_config"] = self_managed_kafka_event_source_config
        if source_access_configuration is not None:
            self._values["source_access_configuration"] = source_access_configuration
        if starting_position is not None:
            self._values["starting_position"] = starting_position
        if starting_position_timestamp is not None:
            self._values["starting_position_timestamp"] = starting_position_timestamp
        if tags is not None:
            self._values["tags"] = tags
        if tags_all is not None:
            self._values["tags_all"] = tags_all
        if topics is not None:
            self._values["topics"] = topics
        if tumbling_window_in_seconds is not None:
            self._values["tumbling_window_in_seconds"] = tumbling_window_in_seconds

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
    def function_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/lambda_event_source_mapping#function_name LambdaEventSourceMapping#function_name}.'''
        result = self._values.get("function_name")
        assert result is not None, "Required property 'function_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def amazon_managed_kafka_event_source_config(
        self,
    ) -> typing.Optional[LambdaEventSourceMappingAmazonManagedKafkaEventSourceConfig]:
        '''amazon_managed_kafka_event_source_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/lambda_event_source_mapping#amazon_managed_kafka_event_source_config LambdaEventSourceMapping#amazon_managed_kafka_event_source_config}
        '''
        result = self._values.get("amazon_managed_kafka_event_source_config")
        return typing.cast(typing.Optional[LambdaEventSourceMappingAmazonManagedKafkaEventSourceConfig], result)

    @builtins.property
    def batch_size(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/lambda_event_source_mapping#batch_size LambdaEventSourceMapping#batch_size}.'''
        result = self._values.get("batch_size")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def bisect_batch_on_function_error(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/lambda_event_source_mapping#bisect_batch_on_function_error LambdaEventSourceMapping#bisect_batch_on_function_error}.'''
        result = self._values.get("bisect_batch_on_function_error")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def destination_config(
        self,
    ) -> typing.Optional["LambdaEventSourceMappingDestinationConfig"]:
        '''destination_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/lambda_event_source_mapping#destination_config LambdaEventSourceMapping#destination_config}
        '''
        result = self._values.get("destination_config")
        return typing.cast(typing.Optional["LambdaEventSourceMappingDestinationConfig"], result)

    @builtins.property
    def document_db_event_source_config(
        self,
    ) -> typing.Optional["LambdaEventSourceMappingDocumentDbEventSourceConfig"]:
        '''document_db_event_source_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/lambda_event_source_mapping#document_db_event_source_config LambdaEventSourceMapping#document_db_event_source_config}
        '''
        result = self._values.get("document_db_event_source_config")
        return typing.cast(typing.Optional["LambdaEventSourceMappingDocumentDbEventSourceConfig"], result)

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/lambda_event_source_mapping#enabled LambdaEventSourceMapping#enabled}.'''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def event_source_arn(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/lambda_event_source_mapping#event_source_arn LambdaEventSourceMapping#event_source_arn}.'''
        result = self._values.get("event_source_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def filter_criteria(
        self,
    ) -> typing.Optional["LambdaEventSourceMappingFilterCriteria"]:
        '''filter_criteria block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/lambda_event_source_mapping#filter_criteria LambdaEventSourceMapping#filter_criteria}
        '''
        result = self._values.get("filter_criteria")
        return typing.cast(typing.Optional["LambdaEventSourceMappingFilterCriteria"], result)

    @builtins.property
    def function_response_types(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/lambda_event_source_mapping#function_response_types LambdaEventSourceMapping#function_response_types}.'''
        result = self._values.get("function_response_types")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/lambda_event_source_mapping#id LambdaEventSourceMapping#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kms_key_arn(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/lambda_event_source_mapping#kms_key_arn LambdaEventSourceMapping#kms_key_arn}.'''
        result = self._values.get("kms_key_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def maximum_batching_window_in_seconds(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/lambda_event_source_mapping#maximum_batching_window_in_seconds LambdaEventSourceMapping#maximum_batching_window_in_seconds}.'''
        result = self._values.get("maximum_batching_window_in_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def maximum_record_age_in_seconds(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/lambda_event_source_mapping#maximum_record_age_in_seconds LambdaEventSourceMapping#maximum_record_age_in_seconds}.'''
        result = self._values.get("maximum_record_age_in_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def maximum_retry_attempts(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/lambda_event_source_mapping#maximum_retry_attempts LambdaEventSourceMapping#maximum_retry_attempts}.'''
        result = self._values.get("maximum_retry_attempts")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def metrics_config(
        self,
    ) -> typing.Optional["LambdaEventSourceMappingMetricsConfig"]:
        '''metrics_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/lambda_event_source_mapping#metrics_config LambdaEventSourceMapping#metrics_config}
        '''
        result = self._values.get("metrics_config")
        return typing.cast(typing.Optional["LambdaEventSourceMappingMetricsConfig"], result)

    @builtins.property
    def parallelization_factor(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/lambda_event_source_mapping#parallelization_factor LambdaEventSourceMapping#parallelization_factor}.'''
        result = self._values.get("parallelization_factor")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def provisioned_poller_config(
        self,
    ) -> typing.Optional["LambdaEventSourceMappingProvisionedPollerConfig"]:
        '''provisioned_poller_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/lambda_event_source_mapping#provisioned_poller_config LambdaEventSourceMapping#provisioned_poller_config}
        '''
        result = self._values.get("provisioned_poller_config")
        return typing.cast(typing.Optional["LambdaEventSourceMappingProvisionedPollerConfig"], result)

    @builtins.property
    def queues(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/lambda_event_source_mapping#queues LambdaEventSourceMapping#queues}.'''
        result = self._values.get("queues")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/lambda_event_source_mapping#region LambdaEventSourceMapping#region}
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def scaling_config(
        self,
    ) -> typing.Optional["LambdaEventSourceMappingScalingConfig"]:
        '''scaling_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/lambda_event_source_mapping#scaling_config LambdaEventSourceMapping#scaling_config}
        '''
        result = self._values.get("scaling_config")
        return typing.cast(typing.Optional["LambdaEventSourceMappingScalingConfig"], result)

    @builtins.property
    def self_managed_event_source(
        self,
    ) -> typing.Optional["LambdaEventSourceMappingSelfManagedEventSource"]:
        '''self_managed_event_source block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/lambda_event_source_mapping#self_managed_event_source LambdaEventSourceMapping#self_managed_event_source}
        '''
        result = self._values.get("self_managed_event_source")
        return typing.cast(typing.Optional["LambdaEventSourceMappingSelfManagedEventSource"], result)

    @builtins.property
    def self_managed_kafka_event_source_config(
        self,
    ) -> typing.Optional["LambdaEventSourceMappingSelfManagedKafkaEventSourceConfig"]:
        '''self_managed_kafka_event_source_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/lambda_event_source_mapping#self_managed_kafka_event_source_config LambdaEventSourceMapping#self_managed_kafka_event_source_config}
        '''
        result = self._values.get("self_managed_kafka_event_source_config")
        return typing.cast(typing.Optional["LambdaEventSourceMappingSelfManagedKafkaEventSourceConfig"], result)

    @builtins.property
    def source_access_configuration(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["LambdaEventSourceMappingSourceAccessConfiguration"]]]:
        '''source_access_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/lambda_event_source_mapping#source_access_configuration LambdaEventSourceMapping#source_access_configuration}
        '''
        result = self._values.get("source_access_configuration")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["LambdaEventSourceMappingSourceAccessConfiguration"]]], result)

    @builtins.property
    def starting_position(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/lambda_event_source_mapping#starting_position LambdaEventSourceMapping#starting_position}.'''
        result = self._values.get("starting_position")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def starting_position_timestamp(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/lambda_event_source_mapping#starting_position_timestamp LambdaEventSourceMapping#starting_position_timestamp}.'''
        result = self._values.get("starting_position_timestamp")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/lambda_event_source_mapping#tags LambdaEventSourceMapping#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def tags_all(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/lambda_event_source_mapping#tags_all LambdaEventSourceMapping#tags_all}.'''
        result = self._values.get("tags_all")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def topics(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/lambda_event_source_mapping#topics LambdaEventSourceMapping#topics}.'''
        result = self._values.get("topics")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def tumbling_window_in_seconds(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/lambda_event_source_mapping#tumbling_window_in_seconds LambdaEventSourceMapping#tumbling_window_in_seconds}.'''
        result = self._values.get("tumbling_window_in_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LambdaEventSourceMappingConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.lambdaEventSourceMapping.LambdaEventSourceMappingDestinationConfig",
    jsii_struct_bases=[],
    name_mapping={"on_failure": "onFailure"},
)
class LambdaEventSourceMappingDestinationConfig:
    def __init__(
        self,
        *,
        on_failure: typing.Optional[typing.Union["LambdaEventSourceMappingDestinationConfigOnFailure", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param on_failure: on_failure block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/lambda_event_source_mapping#on_failure LambdaEventSourceMapping#on_failure}
        '''
        if isinstance(on_failure, dict):
            on_failure = LambdaEventSourceMappingDestinationConfigOnFailure(**on_failure)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__34c9f0b388f168ec909930e18b64b0a89faae7ed714a8203b33b39f48bab681d)
            check_type(argname="argument on_failure", value=on_failure, expected_type=type_hints["on_failure"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if on_failure is not None:
            self._values["on_failure"] = on_failure

    @builtins.property
    def on_failure(
        self,
    ) -> typing.Optional["LambdaEventSourceMappingDestinationConfigOnFailure"]:
        '''on_failure block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/lambda_event_source_mapping#on_failure LambdaEventSourceMapping#on_failure}
        '''
        result = self._values.get("on_failure")
        return typing.cast(typing.Optional["LambdaEventSourceMappingDestinationConfigOnFailure"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LambdaEventSourceMappingDestinationConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.lambdaEventSourceMapping.LambdaEventSourceMappingDestinationConfigOnFailure",
    jsii_struct_bases=[],
    name_mapping={"destination_arn": "destinationArn"},
)
class LambdaEventSourceMappingDestinationConfigOnFailure:
    def __init__(self, *, destination_arn: builtins.str) -> None:
        '''
        :param destination_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/lambda_event_source_mapping#destination_arn LambdaEventSourceMapping#destination_arn}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__576a0eba521c801c96c7b1d9547be6e63b7785dee36315d6db7b6a0550009ad5)
            check_type(argname="argument destination_arn", value=destination_arn, expected_type=type_hints["destination_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "destination_arn": destination_arn,
        }

    @builtins.property
    def destination_arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/lambda_event_source_mapping#destination_arn LambdaEventSourceMapping#destination_arn}.'''
        result = self._values.get("destination_arn")
        assert result is not None, "Required property 'destination_arn' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LambdaEventSourceMappingDestinationConfigOnFailure(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LambdaEventSourceMappingDestinationConfigOnFailureOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.lambdaEventSourceMapping.LambdaEventSourceMappingDestinationConfigOnFailureOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__630832b3b534625a424221bfde5f786d1f1ffddad0ec9ee2a876df687e46e79f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="destinationArnInput")
    def destination_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "destinationArnInput"))

    @builtins.property
    @jsii.member(jsii_name="destinationArn")
    def destination_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "destinationArn"))

    @destination_arn.setter
    def destination_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d22489075dff3e3357b483770d6dc55130727cbc7b3314afe0c6aeb655319289)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "destinationArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[LambdaEventSourceMappingDestinationConfigOnFailure]:
        return typing.cast(typing.Optional[LambdaEventSourceMappingDestinationConfigOnFailure], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[LambdaEventSourceMappingDestinationConfigOnFailure],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6a40dd6edecd910b3198907903ed7799a03005028da09ae5c3710c7263d48230)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class LambdaEventSourceMappingDestinationConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.lambdaEventSourceMapping.LambdaEventSourceMappingDestinationConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3ca1586fcbfe56ac8f4bc2aa11b4c789896b8f4134a70754c4671233ee4f5f50)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putOnFailure")
    def put_on_failure(self, *, destination_arn: builtins.str) -> None:
        '''
        :param destination_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/lambda_event_source_mapping#destination_arn LambdaEventSourceMapping#destination_arn}.
        '''
        value = LambdaEventSourceMappingDestinationConfigOnFailure(
            destination_arn=destination_arn
        )

        return typing.cast(None, jsii.invoke(self, "putOnFailure", [value]))

    @jsii.member(jsii_name="resetOnFailure")
    def reset_on_failure(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOnFailure", []))

    @builtins.property
    @jsii.member(jsii_name="onFailure")
    def on_failure(
        self,
    ) -> LambdaEventSourceMappingDestinationConfigOnFailureOutputReference:
        return typing.cast(LambdaEventSourceMappingDestinationConfigOnFailureOutputReference, jsii.get(self, "onFailure"))

    @builtins.property
    @jsii.member(jsii_name="onFailureInput")
    def on_failure_input(
        self,
    ) -> typing.Optional[LambdaEventSourceMappingDestinationConfigOnFailure]:
        return typing.cast(typing.Optional[LambdaEventSourceMappingDestinationConfigOnFailure], jsii.get(self, "onFailureInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[LambdaEventSourceMappingDestinationConfig]:
        return typing.cast(typing.Optional[LambdaEventSourceMappingDestinationConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[LambdaEventSourceMappingDestinationConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0b8f60294131cc23ff467227e1e80d5a38227b46da9e8e8c60bfb37f82aa8c95)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.lambdaEventSourceMapping.LambdaEventSourceMappingDocumentDbEventSourceConfig",
    jsii_struct_bases=[],
    name_mapping={
        "database_name": "databaseName",
        "collection_name": "collectionName",
        "full_document": "fullDocument",
    },
)
class LambdaEventSourceMappingDocumentDbEventSourceConfig:
    def __init__(
        self,
        *,
        database_name: builtins.str,
        collection_name: typing.Optional[builtins.str] = None,
        full_document: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param database_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/lambda_event_source_mapping#database_name LambdaEventSourceMapping#database_name}.
        :param collection_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/lambda_event_source_mapping#collection_name LambdaEventSourceMapping#collection_name}.
        :param full_document: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/lambda_event_source_mapping#full_document LambdaEventSourceMapping#full_document}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__99fa1653eab5203440a24027f6fb7cd266c7bc10e8f42c1b67ae900538c4fac1)
            check_type(argname="argument database_name", value=database_name, expected_type=type_hints["database_name"])
            check_type(argname="argument collection_name", value=collection_name, expected_type=type_hints["collection_name"])
            check_type(argname="argument full_document", value=full_document, expected_type=type_hints["full_document"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "database_name": database_name,
        }
        if collection_name is not None:
            self._values["collection_name"] = collection_name
        if full_document is not None:
            self._values["full_document"] = full_document

    @builtins.property
    def database_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/lambda_event_source_mapping#database_name LambdaEventSourceMapping#database_name}.'''
        result = self._values.get("database_name")
        assert result is not None, "Required property 'database_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def collection_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/lambda_event_source_mapping#collection_name LambdaEventSourceMapping#collection_name}.'''
        result = self._values.get("collection_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def full_document(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/lambda_event_source_mapping#full_document LambdaEventSourceMapping#full_document}.'''
        result = self._values.get("full_document")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LambdaEventSourceMappingDocumentDbEventSourceConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LambdaEventSourceMappingDocumentDbEventSourceConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.lambdaEventSourceMapping.LambdaEventSourceMappingDocumentDbEventSourceConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__20326743b33fd54d103c07b4e264198d02ea760f78b0e852d9267a264f005a72)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCollectionName")
    def reset_collection_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCollectionName", []))

    @jsii.member(jsii_name="resetFullDocument")
    def reset_full_document(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFullDocument", []))

    @builtins.property
    @jsii.member(jsii_name="collectionNameInput")
    def collection_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "collectionNameInput"))

    @builtins.property
    @jsii.member(jsii_name="databaseNameInput")
    def database_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "databaseNameInput"))

    @builtins.property
    @jsii.member(jsii_name="fullDocumentInput")
    def full_document_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "fullDocumentInput"))

    @builtins.property
    @jsii.member(jsii_name="collectionName")
    def collection_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "collectionName"))

    @collection_name.setter
    def collection_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c7a3a3fab328428684a37a1cf5a6dcffbb0bc82a76331b01b8a52db8b0672271)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "collectionName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="databaseName")
    def database_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "databaseName"))

    @database_name.setter
    def database_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__25cece1eac8e663801c2bb8b66f9cb5684881601052875ce3f33c88c14dc3006)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "databaseName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="fullDocument")
    def full_document(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "fullDocument"))

    @full_document.setter
    def full_document(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a9c3828bf1d72615c8c70bfa86d5f6236cb7b087db482303f90d69e56ec156cb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fullDocument", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[LambdaEventSourceMappingDocumentDbEventSourceConfig]:
        return typing.cast(typing.Optional[LambdaEventSourceMappingDocumentDbEventSourceConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[LambdaEventSourceMappingDocumentDbEventSourceConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__850de99fa14e73763e2c5a882085650b1a4e46ad862627bd8795acecbc1055dc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.lambdaEventSourceMapping.LambdaEventSourceMappingFilterCriteria",
    jsii_struct_bases=[],
    name_mapping={"filter": "filter"},
)
class LambdaEventSourceMappingFilterCriteria:
    def __init__(
        self,
        *,
        filter: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["LambdaEventSourceMappingFilterCriteriaFilter", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param filter: filter block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/lambda_event_source_mapping#filter LambdaEventSourceMapping#filter}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d530693652faef12942656056ae1f83a1f26c650fdda463d012d77ba0938fadb)
            check_type(argname="argument filter", value=filter, expected_type=type_hints["filter"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if filter is not None:
            self._values["filter"] = filter

    @builtins.property
    def filter(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["LambdaEventSourceMappingFilterCriteriaFilter"]]]:
        '''filter block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/lambda_event_source_mapping#filter LambdaEventSourceMapping#filter}
        '''
        result = self._values.get("filter")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["LambdaEventSourceMappingFilterCriteriaFilter"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LambdaEventSourceMappingFilterCriteria(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.lambdaEventSourceMapping.LambdaEventSourceMappingFilterCriteriaFilter",
    jsii_struct_bases=[],
    name_mapping={"pattern": "pattern"},
)
class LambdaEventSourceMappingFilterCriteriaFilter:
    def __init__(self, *, pattern: typing.Optional[builtins.str] = None) -> None:
        '''
        :param pattern: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/lambda_event_source_mapping#pattern LambdaEventSourceMapping#pattern}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2eaa4309d2e4ea68d137970b0d83165fe3985ebb4115164a7e2a3154ad8dfbfd)
            check_type(argname="argument pattern", value=pattern, expected_type=type_hints["pattern"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if pattern is not None:
            self._values["pattern"] = pattern

    @builtins.property
    def pattern(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/lambda_event_source_mapping#pattern LambdaEventSourceMapping#pattern}.'''
        result = self._values.get("pattern")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LambdaEventSourceMappingFilterCriteriaFilter(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LambdaEventSourceMappingFilterCriteriaFilterList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.lambdaEventSourceMapping.LambdaEventSourceMappingFilterCriteriaFilterList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1d706b5ee3016a7a4ec9c9eadfbc14972d08c40fbcf17ffb761b1c7275c744e5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "LambdaEventSourceMappingFilterCriteriaFilterOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1175ebc8244990f76740bc49fb76932046078924e37d8f1692ce9bf28a07d7e9)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("LambdaEventSourceMappingFilterCriteriaFilterOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8f053edf2d14673ea9287bdb68915dc2dfc815f22a29ff944c2e0dc414dffad3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__aa126ca9964bd3aa4fcb977332863782ad6ae733b6d3751c885280f21ffe98ad)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0c371c6014487911232332acb2e8eeac5c1569af1b2464330d3014d5e21ef694)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LambdaEventSourceMappingFilterCriteriaFilter]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LambdaEventSourceMappingFilterCriteriaFilter]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LambdaEventSourceMappingFilterCriteriaFilter]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4fdb04d9150902e1b8a2871fbd91e652493a1766a47ef9f3c0595a283979a0cb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class LambdaEventSourceMappingFilterCriteriaFilterOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.lambdaEventSourceMapping.LambdaEventSourceMappingFilterCriteriaFilterOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f501d48e5274adca1b7fcc603ac574a40c9a2dc8779689d6a1928974b68423a7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetPattern")
    def reset_pattern(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPattern", []))

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
            type_hints = typing.get_type_hints(_typecheckingstub__214652ec66555668b8bc5a979d45f9b2df52dc741b0765be58a0a239c663407a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pattern", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LambdaEventSourceMappingFilterCriteriaFilter]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LambdaEventSourceMappingFilterCriteriaFilter]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LambdaEventSourceMappingFilterCriteriaFilter]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d64bf7f51af4a6978326e1aef1f95a6ad437ee14d4282c65c5b4dfb403739cda)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class LambdaEventSourceMappingFilterCriteriaOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.lambdaEventSourceMapping.LambdaEventSourceMappingFilterCriteriaOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bf90e99296b6b0836dcd21cfedbd96cba0de8817c28b86fe45e5a81d3e9a4a52)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putFilter")
    def put_filter(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[LambdaEventSourceMappingFilterCriteriaFilter, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2fed9484a7553309c5a38b3ad891206d0ade480e84f9da82d9b030b886c21c93)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putFilter", [value]))

    @jsii.member(jsii_name="resetFilter")
    def reset_filter(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFilter", []))

    @builtins.property
    @jsii.member(jsii_name="filter")
    def filter(self) -> LambdaEventSourceMappingFilterCriteriaFilterList:
        return typing.cast(LambdaEventSourceMappingFilterCriteriaFilterList, jsii.get(self, "filter"))

    @builtins.property
    @jsii.member(jsii_name="filterInput")
    def filter_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LambdaEventSourceMappingFilterCriteriaFilter]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LambdaEventSourceMappingFilterCriteriaFilter]]], jsii.get(self, "filterInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[LambdaEventSourceMappingFilterCriteria]:
        return typing.cast(typing.Optional[LambdaEventSourceMappingFilterCriteria], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[LambdaEventSourceMappingFilterCriteria],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d1a02ab1e31c47b64c90e7cc7060e5f525711e57eba08e73753d9d15400fd741)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.lambdaEventSourceMapping.LambdaEventSourceMappingMetricsConfig",
    jsii_struct_bases=[],
    name_mapping={"metrics": "metrics"},
)
class LambdaEventSourceMappingMetricsConfig:
    def __init__(self, *, metrics: typing.Sequence[builtins.str]) -> None:
        '''
        :param metrics: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/lambda_event_source_mapping#metrics LambdaEventSourceMapping#metrics}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__64e547c770e46f89a09d7d5dcefa3091605d53a49520ddc5ca8700dc17db212a)
            check_type(argname="argument metrics", value=metrics, expected_type=type_hints["metrics"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "metrics": metrics,
        }

    @builtins.property
    def metrics(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/lambda_event_source_mapping#metrics LambdaEventSourceMapping#metrics}.'''
        result = self._values.get("metrics")
        assert result is not None, "Required property 'metrics' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LambdaEventSourceMappingMetricsConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LambdaEventSourceMappingMetricsConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.lambdaEventSourceMapping.LambdaEventSourceMappingMetricsConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__79c5a68212d6b4d3cc7a331786fe68ee7ada1b2459f9474bfac8cfc438332749)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="metricsInput")
    def metrics_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "metricsInput"))

    @builtins.property
    @jsii.member(jsii_name="metrics")
    def metrics(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "metrics"))

    @metrics.setter
    def metrics(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__80f3c4b232e970168fa9c86102ad01599df0151390a6f7c039eba0b1b730713f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metrics", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[LambdaEventSourceMappingMetricsConfig]:
        return typing.cast(typing.Optional[LambdaEventSourceMappingMetricsConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[LambdaEventSourceMappingMetricsConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ad63dfc73e4b9ffd71b3c05a57799616605f3193f799c87948393abd665230b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.lambdaEventSourceMapping.LambdaEventSourceMappingProvisionedPollerConfig",
    jsii_struct_bases=[],
    name_mapping={
        "maximum_pollers": "maximumPollers",
        "minimum_pollers": "minimumPollers",
    },
)
class LambdaEventSourceMappingProvisionedPollerConfig:
    def __init__(
        self,
        *,
        maximum_pollers: typing.Optional[jsii.Number] = None,
        minimum_pollers: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param maximum_pollers: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/lambda_event_source_mapping#maximum_pollers LambdaEventSourceMapping#maximum_pollers}.
        :param minimum_pollers: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/lambda_event_source_mapping#minimum_pollers LambdaEventSourceMapping#minimum_pollers}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__285eb7a002851c3c34556637a5863c987eab1abbf787e75d54f204251fb57d1b)
            check_type(argname="argument maximum_pollers", value=maximum_pollers, expected_type=type_hints["maximum_pollers"])
            check_type(argname="argument minimum_pollers", value=minimum_pollers, expected_type=type_hints["minimum_pollers"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if maximum_pollers is not None:
            self._values["maximum_pollers"] = maximum_pollers
        if minimum_pollers is not None:
            self._values["minimum_pollers"] = minimum_pollers

    @builtins.property
    def maximum_pollers(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/lambda_event_source_mapping#maximum_pollers LambdaEventSourceMapping#maximum_pollers}.'''
        result = self._values.get("maximum_pollers")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def minimum_pollers(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/lambda_event_source_mapping#minimum_pollers LambdaEventSourceMapping#minimum_pollers}.'''
        result = self._values.get("minimum_pollers")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LambdaEventSourceMappingProvisionedPollerConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LambdaEventSourceMappingProvisionedPollerConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.lambdaEventSourceMapping.LambdaEventSourceMappingProvisionedPollerConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4789baee5d183a45c52a283967e86b6913e7eb15518148e72aa2b61d3e97e70b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetMaximumPollers")
    def reset_maximum_pollers(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaximumPollers", []))

    @jsii.member(jsii_name="resetMinimumPollers")
    def reset_minimum_pollers(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMinimumPollers", []))

    @builtins.property
    @jsii.member(jsii_name="maximumPollersInput")
    def maximum_pollers_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maximumPollersInput"))

    @builtins.property
    @jsii.member(jsii_name="minimumPollersInput")
    def minimum_pollers_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "minimumPollersInput"))

    @builtins.property
    @jsii.member(jsii_name="maximumPollers")
    def maximum_pollers(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maximumPollers"))

    @maximum_pollers.setter
    def maximum_pollers(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c15e1cb1a4eabdc71986191828c4355aefc2ee3f799ba427ed79764755c02941)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maximumPollers", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="minimumPollers")
    def minimum_pollers(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "minimumPollers"))

    @minimum_pollers.setter
    def minimum_pollers(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__49d0b4af5239628b7ed93bcc90d23b520483db5658a93e142869194bde73f194)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minimumPollers", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[LambdaEventSourceMappingProvisionedPollerConfig]:
        return typing.cast(typing.Optional[LambdaEventSourceMappingProvisionedPollerConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[LambdaEventSourceMappingProvisionedPollerConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e9241e875fdee5d7e44c685e727390f279e6815867c92c0b7f9b0095cb2a434)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.lambdaEventSourceMapping.LambdaEventSourceMappingScalingConfig",
    jsii_struct_bases=[],
    name_mapping={"maximum_concurrency": "maximumConcurrency"},
)
class LambdaEventSourceMappingScalingConfig:
    def __init__(
        self,
        *,
        maximum_concurrency: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param maximum_concurrency: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/lambda_event_source_mapping#maximum_concurrency LambdaEventSourceMapping#maximum_concurrency}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d74d6f22823d4447bd30c4463f74cf13e167dc8c449028d50cc2571556d00f80)
            check_type(argname="argument maximum_concurrency", value=maximum_concurrency, expected_type=type_hints["maximum_concurrency"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if maximum_concurrency is not None:
            self._values["maximum_concurrency"] = maximum_concurrency

    @builtins.property
    def maximum_concurrency(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/lambda_event_source_mapping#maximum_concurrency LambdaEventSourceMapping#maximum_concurrency}.'''
        result = self._values.get("maximum_concurrency")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LambdaEventSourceMappingScalingConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LambdaEventSourceMappingScalingConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.lambdaEventSourceMapping.LambdaEventSourceMappingScalingConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e9b48af60d6343448e06c116989d5aa002180650fe257206020f8134659c6fef)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetMaximumConcurrency")
    def reset_maximum_concurrency(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaximumConcurrency", []))

    @builtins.property
    @jsii.member(jsii_name="maximumConcurrencyInput")
    def maximum_concurrency_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maximumConcurrencyInput"))

    @builtins.property
    @jsii.member(jsii_name="maximumConcurrency")
    def maximum_concurrency(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maximumConcurrency"))

    @maximum_concurrency.setter
    def maximum_concurrency(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a4605cb1b88ec7bf7621087fb659a47bd1cfc7f0ac5b3920670ba31c8c53c09)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maximumConcurrency", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[LambdaEventSourceMappingScalingConfig]:
        return typing.cast(typing.Optional[LambdaEventSourceMappingScalingConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[LambdaEventSourceMappingScalingConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eb9b597563dd679048f132a566cdb4d9caed9f1522b1421e84556b5f7060e685)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.lambdaEventSourceMapping.LambdaEventSourceMappingSelfManagedEventSource",
    jsii_struct_bases=[],
    name_mapping={"endpoints": "endpoints"},
)
class LambdaEventSourceMappingSelfManagedEventSource:
    def __init__(
        self,
        *,
        endpoints: typing.Mapping[builtins.str, builtins.str],
    ) -> None:
        '''
        :param endpoints: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/lambda_event_source_mapping#endpoints LambdaEventSourceMapping#endpoints}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6f718d9f0c61db275ede06a61fe886dc168521189524bb83565d3da9c025c48e)
            check_type(argname="argument endpoints", value=endpoints, expected_type=type_hints["endpoints"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "endpoints": endpoints,
        }

    @builtins.property
    def endpoints(self) -> typing.Mapping[builtins.str, builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/lambda_event_source_mapping#endpoints LambdaEventSourceMapping#endpoints}.'''
        result = self._values.get("endpoints")
        assert result is not None, "Required property 'endpoints' is missing"
        return typing.cast(typing.Mapping[builtins.str, builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LambdaEventSourceMappingSelfManagedEventSource(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LambdaEventSourceMappingSelfManagedEventSourceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.lambdaEventSourceMapping.LambdaEventSourceMappingSelfManagedEventSourceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8bbba2764bd988b4a816a46955500ec7a6c7dceed523e5314b7a48586e45340a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="endpointsInput")
    def endpoints_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "endpointsInput"))

    @builtins.property
    @jsii.member(jsii_name="endpoints")
    def endpoints(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "endpoints"))

    @endpoints.setter
    def endpoints(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a076c1f8baac0f9ff5ba3dd8e69a900b577e74be7cfbec5ccc8f488fec1896c6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "endpoints", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[LambdaEventSourceMappingSelfManagedEventSource]:
        return typing.cast(typing.Optional[LambdaEventSourceMappingSelfManagedEventSource], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[LambdaEventSourceMappingSelfManagedEventSource],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ca82dd2b84242acad82c6883bebd93cea9346581689399f883727e4d44589776)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.lambdaEventSourceMapping.LambdaEventSourceMappingSelfManagedKafkaEventSourceConfig",
    jsii_struct_bases=[],
    name_mapping={
        "consumer_group_id": "consumerGroupId",
        "schema_registry_config": "schemaRegistryConfig",
    },
)
class LambdaEventSourceMappingSelfManagedKafkaEventSourceConfig:
    def __init__(
        self,
        *,
        consumer_group_id: typing.Optional[builtins.str] = None,
        schema_registry_config: typing.Optional[typing.Union["LambdaEventSourceMappingSelfManagedKafkaEventSourceConfigSchemaRegistryConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param consumer_group_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/lambda_event_source_mapping#consumer_group_id LambdaEventSourceMapping#consumer_group_id}.
        :param schema_registry_config: schema_registry_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/lambda_event_source_mapping#schema_registry_config LambdaEventSourceMapping#schema_registry_config}
        '''
        if isinstance(schema_registry_config, dict):
            schema_registry_config = LambdaEventSourceMappingSelfManagedKafkaEventSourceConfigSchemaRegistryConfig(**schema_registry_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__552f5accfcb9ea14c92bd78af097762e0ae1236cab5d2bb2ad88f563414bb309)
            check_type(argname="argument consumer_group_id", value=consumer_group_id, expected_type=type_hints["consumer_group_id"])
            check_type(argname="argument schema_registry_config", value=schema_registry_config, expected_type=type_hints["schema_registry_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if consumer_group_id is not None:
            self._values["consumer_group_id"] = consumer_group_id
        if schema_registry_config is not None:
            self._values["schema_registry_config"] = schema_registry_config

    @builtins.property
    def consumer_group_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/lambda_event_source_mapping#consumer_group_id LambdaEventSourceMapping#consumer_group_id}.'''
        result = self._values.get("consumer_group_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def schema_registry_config(
        self,
    ) -> typing.Optional["LambdaEventSourceMappingSelfManagedKafkaEventSourceConfigSchemaRegistryConfig"]:
        '''schema_registry_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/lambda_event_source_mapping#schema_registry_config LambdaEventSourceMapping#schema_registry_config}
        '''
        result = self._values.get("schema_registry_config")
        return typing.cast(typing.Optional["LambdaEventSourceMappingSelfManagedKafkaEventSourceConfigSchemaRegistryConfig"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LambdaEventSourceMappingSelfManagedKafkaEventSourceConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LambdaEventSourceMappingSelfManagedKafkaEventSourceConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.lambdaEventSourceMapping.LambdaEventSourceMappingSelfManagedKafkaEventSourceConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c6356265f44a9462aff0a0bd5cf3e3da9ce2261f824f5f7b98d1fb4c80bbd090)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putSchemaRegistryConfig")
    def put_schema_registry_config(
        self,
        *,
        access_config: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["LambdaEventSourceMappingSelfManagedKafkaEventSourceConfigSchemaRegistryConfigAccessConfig", typing.Dict[builtins.str, typing.Any]]]]] = None,
        event_record_format: typing.Optional[builtins.str] = None,
        schema_registry_uri: typing.Optional[builtins.str] = None,
        schema_validation_config: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["LambdaEventSourceMappingSelfManagedKafkaEventSourceConfigSchemaRegistryConfigSchemaValidationConfig", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param access_config: access_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/lambda_event_source_mapping#access_config LambdaEventSourceMapping#access_config}
        :param event_record_format: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/lambda_event_source_mapping#event_record_format LambdaEventSourceMapping#event_record_format}.
        :param schema_registry_uri: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/lambda_event_source_mapping#schema_registry_uri LambdaEventSourceMapping#schema_registry_uri}.
        :param schema_validation_config: schema_validation_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/lambda_event_source_mapping#schema_validation_config LambdaEventSourceMapping#schema_validation_config}
        '''
        value = LambdaEventSourceMappingSelfManagedKafkaEventSourceConfigSchemaRegistryConfig(
            access_config=access_config,
            event_record_format=event_record_format,
            schema_registry_uri=schema_registry_uri,
            schema_validation_config=schema_validation_config,
        )

        return typing.cast(None, jsii.invoke(self, "putSchemaRegistryConfig", [value]))

    @jsii.member(jsii_name="resetConsumerGroupId")
    def reset_consumer_group_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConsumerGroupId", []))

    @jsii.member(jsii_name="resetSchemaRegistryConfig")
    def reset_schema_registry_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSchemaRegistryConfig", []))

    @builtins.property
    @jsii.member(jsii_name="schemaRegistryConfig")
    def schema_registry_config(
        self,
    ) -> "LambdaEventSourceMappingSelfManagedKafkaEventSourceConfigSchemaRegistryConfigOutputReference":
        return typing.cast("LambdaEventSourceMappingSelfManagedKafkaEventSourceConfigSchemaRegistryConfigOutputReference", jsii.get(self, "schemaRegistryConfig"))

    @builtins.property
    @jsii.member(jsii_name="consumerGroupIdInput")
    def consumer_group_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "consumerGroupIdInput"))

    @builtins.property
    @jsii.member(jsii_name="schemaRegistryConfigInput")
    def schema_registry_config_input(
        self,
    ) -> typing.Optional["LambdaEventSourceMappingSelfManagedKafkaEventSourceConfigSchemaRegistryConfig"]:
        return typing.cast(typing.Optional["LambdaEventSourceMappingSelfManagedKafkaEventSourceConfigSchemaRegistryConfig"], jsii.get(self, "schemaRegistryConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="consumerGroupId")
    def consumer_group_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "consumerGroupId"))

    @consumer_group_id.setter
    def consumer_group_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d8e960270f5884b70648a3fbbbed56d1d11a13b177ec49f5c07bbf4b60b5495b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "consumerGroupId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[LambdaEventSourceMappingSelfManagedKafkaEventSourceConfig]:
        return typing.cast(typing.Optional[LambdaEventSourceMappingSelfManagedKafkaEventSourceConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[LambdaEventSourceMappingSelfManagedKafkaEventSourceConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f35651559ea6accdc41caeff6ea91750ce0e9c62392d3992ac409086f2b8948)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.lambdaEventSourceMapping.LambdaEventSourceMappingSelfManagedKafkaEventSourceConfigSchemaRegistryConfig",
    jsii_struct_bases=[],
    name_mapping={
        "access_config": "accessConfig",
        "event_record_format": "eventRecordFormat",
        "schema_registry_uri": "schemaRegistryUri",
        "schema_validation_config": "schemaValidationConfig",
    },
)
class LambdaEventSourceMappingSelfManagedKafkaEventSourceConfigSchemaRegistryConfig:
    def __init__(
        self,
        *,
        access_config: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["LambdaEventSourceMappingSelfManagedKafkaEventSourceConfigSchemaRegistryConfigAccessConfig", typing.Dict[builtins.str, typing.Any]]]]] = None,
        event_record_format: typing.Optional[builtins.str] = None,
        schema_registry_uri: typing.Optional[builtins.str] = None,
        schema_validation_config: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["LambdaEventSourceMappingSelfManagedKafkaEventSourceConfigSchemaRegistryConfigSchemaValidationConfig", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param access_config: access_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/lambda_event_source_mapping#access_config LambdaEventSourceMapping#access_config}
        :param event_record_format: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/lambda_event_source_mapping#event_record_format LambdaEventSourceMapping#event_record_format}.
        :param schema_registry_uri: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/lambda_event_source_mapping#schema_registry_uri LambdaEventSourceMapping#schema_registry_uri}.
        :param schema_validation_config: schema_validation_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/lambda_event_source_mapping#schema_validation_config LambdaEventSourceMapping#schema_validation_config}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4091136fcb90bd3f2a82bc4622d711625efb0702680ad1cc3fd6129fe80938f2)
            check_type(argname="argument access_config", value=access_config, expected_type=type_hints["access_config"])
            check_type(argname="argument event_record_format", value=event_record_format, expected_type=type_hints["event_record_format"])
            check_type(argname="argument schema_registry_uri", value=schema_registry_uri, expected_type=type_hints["schema_registry_uri"])
            check_type(argname="argument schema_validation_config", value=schema_validation_config, expected_type=type_hints["schema_validation_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if access_config is not None:
            self._values["access_config"] = access_config
        if event_record_format is not None:
            self._values["event_record_format"] = event_record_format
        if schema_registry_uri is not None:
            self._values["schema_registry_uri"] = schema_registry_uri
        if schema_validation_config is not None:
            self._values["schema_validation_config"] = schema_validation_config

    @builtins.property
    def access_config(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["LambdaEventSourceMappingSelfManagedKafkaEventSourceConfigSchemaRegistryConfigAccessConfig"]]]:
        '''access_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/lambda_event_source_mapping#access_config LambdaEventSourceMapping#access_config}
        '''
        result = self._values.get("access_config")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["LambdaEventSourceMappingSelfManagedKafkaEventSourceConfigSchemaRegistryConfigAccessConfig"]]], result)

    @builtins.property
    def event_record_format(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/lambda_event_source_mapping#event_record_format LambdaEventSourceMapping#event_record_format}.'''
        result = self._values.get("event_record_format")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def schema_registry_uri(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/lambda_event_source_mapping#schema_registry_uri LambdaEventSourceMapping#schema_registry_uri}.'''
        result = self._values.get("schema_registry_uri")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def schema_validation_config(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["LambdaEventSourceMappingSelfManagedKafkaEventSourceConfigSchemaRegistryConfigSchemaValidationConfig"]]]:
        '''schema_validation_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/lambda_event_source_mapping#schema_validation_config LambdaEventSourceMapping#schema_validation_config}
        '''
        result = self._values.get("schema_validation_config")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["LambdaEventSourceMappingSelfManagedKafkaEventSourceConfigSchemaRegistryConfigSchemaValidationConfig"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LambdaEventSourceMappingSelfManagedKafkaEventSourceConfigSchemaRegistryConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.lambdaEventSourceMapping.LambdaEventSourceMappingSelfManagedKafkaEventSourceConfigSchemaRegistryConfigAccessConfig",
    jsii_struct_bases=[],
    name_mapping={"type": "type", "uri": "uri"},
)
class LambdaEventSourceMappingSelfManagedKafkaEventSourceConfigSchemaRegistryConfigAccessConfig:
    def __init__(
        self,
        *,
        type: typing.Optional[builtins.str] = None,
        uri: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/lambda_event_source_mapping#type LambdaEventSourceMapping#type}.
        :param uri: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/lambda_event_source_mapping#uri LambdaEventSourceMapping#uri}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ae2345971cf9293785fda02130e7db8eb6b99ed8574446874582d3d0a0ca9a80)
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument uri", value=uri, expected_type=type_hints["uri"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if type is not None:
            self._values["type"] = type
        if uri is not None:
            self._values["uri"] = uri

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/lambda_event_source_mapping#type LambdaEventSourceMapping#type}.'''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def uri(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/lambda_event_source_mapping#uri LambdaEventSourceMapping#uri}.'''
        result = self._values.get("uri")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LambdaEventSourceMappingSelfManagedKafkaEventSourceConfigSchemaRegistryConfigAccessConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LambdaEventSourceMappingSelfManagedKafkaEventSourceConfigSchemaRegistryConfigAccessConfigList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.lambdaEventSourceMapping.LambdaEventSourceMappingSelfManagedKafkaEventSourceConfigSchemaRegistryConfigAccessConfigList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e6284230dceb744bc128cf944fe93397abd5e968705d9f1075dee9767735dfa5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "LambdaEventSourceMappingSelfManagedKafkaEventSourceConfigSchemaRegistryConfigAccessConfigOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__319fc4b2d39eb6c2f7527a836d90305e768acace33e538c79f6c4a7b3cd6240c)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("LambdaEventSourceMappingSelfManagedKafkaEventSourceConfigSchemaRegistryConfigAccessConfigOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__58925c2a19812652cbb71db7b9ed4219d06c3df69d6fa8bfdf6dc0fcbc4ccb64)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2a7ad005fb1ca8b7c0966aee5704c64404d3fa1996e1bca0b6f691724877dc8c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0aba0afc7ce0e69d6ad215e4979c71a95c32e4168ae296224cfd4082fa3b0886)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LambdaEventSourceMappingSelfManagedKafkaEventSourceConfigSchemaRegistryConfigAccessConfig]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LambdaEventSourceMappingSelfManagedKafkaEventSourceConfigSchemaRegistryConfigAccessConfig]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LambdaEventSourceMappingSelfManagedKafkaEventSourceConfigSchemaRegistryConfigAccessConfig]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__da40e67cf3027e978160db7d9fed93e5da7f0fd2286d5f711e551eb135813962)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class LambdaEventSourceMappingSelfManagedKafkaEventSourceConfigSchemaRegistryConfigAccessConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.lambdaEventSourceMapping.LambdaEventSourceMappingSelfManagedKafkaEventSourceConfigSchemaRegistryConfigAccessConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f36ba9d7cbe90874472cb80660909f45cf623774eec0fac6ebcfdc2a59aee1d4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetType")
    def reset_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetType", []))

    @jsii.member(jsii_name="resetUri")
    def reset_uri(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUri", []))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="uriInput")
    def uri_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "uriInput"))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__93126c0cff3eb239b0c76fc007d6d87cb2ecd07a647e3df71782bdb2f0d71e8a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="uri")
    def uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "uri"))

    @uri.setter
    def uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e94c251504deb20b785832f3b3048d71c0e0236a12ff1c4fef93f80bb37c66a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "uri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LambdaEventSourceMappingSelfManagedKafkaEventSourceConfigSchemaRegistryConfigAccessConfig]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LambdaEventSourceMappingSelfManagedKafkaEventSourceConfigSchemaRegistryConfigAccessConfig]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LambdaEventSourceMappingSelfManagedKafkaEventSourceConfigSchemaRegistryConfigAccessConfig]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__13a047d414e35735a53eb3b4489876fd5156615cdbb935ac93d15015aaff1b82)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class LambdaEventSourceMappingSelfManagedKafkaEventSourceConfigSchemaRegistryConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.lambdaEventSourceMapping.LambdaEventSourceMappingSelfManagedKafkaEventSourceConfigSchemaRegistryConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__649071ac98193455135cce0cd4ec6b8399e254fa52013bba6c3a86585ea9b16d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAccessConfig")
    def put_access_config(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[LambdaEventSourceMappingSelfManagedKafkaEventSourceConfigSchemaRegistryConfigAccessConfig, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3b26351d072b6afa487c395a95a085179262b63229af2b0eaaf35dec4c75e00b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putAccessConfig", [value]))

    @jsii.member(jsii_name="putSchemaValidationConfig")
    def put_schema_validation_config(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["LambdaEventSourceMappingSelfManagedKafkaEventSourceConfigSchemaRegistryConfigSchemaValidationConfig", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e006640b840713c14a96954a5ac2826f67e23317c213869fa9573555cf8d8ad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putSchemaValidationConfig", [value]))

    @jsii.member(jsii_name="resetAccessConfig")
    def reset_access_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAccessConfig", []))

    @jsii.member(jsii_name="resetEventRecordFormat")
    def reset_event_record_format(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEventRecordFormat", []))

    @jsii.member(jsii_name="resetSchemaRegistryUri")
    def reset_schema_registry_uri(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSchemaRegistryUri", []))

    @jsii.member(jsii_name="resetSchemaValidationConfig")
    def reset_schema_validation_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSchemaValidationConfig", []))

    @builtins.property
    @jsii.member(jsii_name="accessConfig")
    def access_config(
        self,
    ) -> LambdaEventSourceMappingSelfManagedKafkaEventSourceConfigSchemaRegistryConfigAccessConfigList:
        return typing.cast(LambdaEventSourceMappingSelfManagedKafkaEventSourceConfigSchemaRegistryConfigAccessConfigList, jsii.get(self, "accessConfig"))

    @builtins.property
    @jsii.member(jsii_name="schemaValidationConfig")
    def schema_validation_config(
        self,
    ) -> "LambdaEventSourceMappingSelfManagedKafkaEventSourceConfigSchemaRegistryConfigSchemaValidationConfigList":
        return typing.cast("LambdaEventSourceMappingSelfManagedKafkaEventSourceConfigSchemaRegistryConfigSchemaValidationConfigList", jsii.get(self, "schemaValidationConfig"))

    @builtins.property
    @jsii.member(jsii_name="accessConfigInput")
    def access_config_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LambdaEventSourceMappingSelfManagedKafkaEventSourceConfigSchemaRegistryConfigAccessConfig]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LambdaEventSourceMappingSelfManagedKafkaEventSourceConfigSchemaRegistryConfigAccessConfig]]], jsii.get(self, "accessConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="eventRecordFormatInput")
    def event_record_format_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "eventRecordFormatInput"))

    @builtins.property
    @jsii.member(jsii_name="schemaRegistryUriInput")
    def schema_registry_uri_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "schemaRegistryUriInput"))

    @builtins.property
    @jsii.member(jsii_name="schemaValidationConfigInput")
    def schema_validation_config_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["LambdaEventSourceMappingSelfManagedKafkaEventSourceConfigSchemaRegistryConfigSchemaValidationConfig"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["LambdaEventSourceMappingSelfManagedKafkaEventSourceConfigSchemaRegistryConfigSchemaValidationConfig"]]], jsii.get(self, "schemaValidationConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="eventRecordFormat")
    def event_record_format(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "eventRecordFormat"))

    @event_record_format.setter
    def event_record_format(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bc5315d585c228e62cf3ab1cfda6ca3425906ad0f23f26e9a5fcde530053a87d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "eventRecordFormat", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="schemaRegistryUri")
    def schema_registry_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "schemaRegistryUri"))

    @schema_registry_uri.setter
    def schema_registry_uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__42b79e4a061f5609d5150c390057c125e7c6e8a3f319b48b77a5b76a58894936)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "schemaRegistryUri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[LambdaEventSourceMappingSelfManagedKafkaEventSourceConfigSchemaRegistryConfig]:
        return typing.cast(typing.Optional[LambdaEventSourceMappingSelfManagedKafkaEventSourceConfigSchemaRegistryConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[LambdaEventSourceMappingSelfManagedKafkaEventSourceConfigSchemaRegistryConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0dcd21e333a0a669c9ec805ed4cc1f8e89249ead26ea72d70dc3a1a13e19907f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.lambdaEventSourceMapping.LambdaEventSourceMappingSelfManagedKafkaEventSourceConfigSchemaRegistryConfigSchemaValidationConfig",
    jsii_struct_bases=[],
    name_mapping={"attribute": "attribute"},
)
class LambdaEventSourceMappingSelfManagedKafkaEventSourceConfigSchemaRegistryConfigSchemaValidationConfig:
    def __init__(self, *, attribute: typing.Optional[builtins.str] = None) -> None:
        '''
        :param attribute: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/lambda_event_source_mapping#attribute LambdaEventSourceMapping#attribute}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eea22668e8fea4cc7ef953eb2cbf279d675a93f856c12642f2a3da6496cac49b)
            check_type(argname="argument attribute", value=attribute, expected_type=type_hints["attribute"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if attribute is not None:
            self._values["attribute"] = attribute

    @builtins.property
    def attribute(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/lambda_event_source_mapping#attribute LambdaEventSourceMapping#attribute}.'''
        result = self._values.get("attribute")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LambdaEventSourceMappingSelfManagedKafkaEventSourceConfigSchemaRegistryConfigSchemaValidationConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LambdaEventSourceMappingSelfManagedKafkaEventSourceConfigSchemaRegistryConfigSchemaValidationConfigList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.lambdaEventSourceMapping.LambdaEventSourceMappingSelfManagedKafkaEventSourceConfigSchemaRegistryConfigSchemaValidationConfigList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d005504f203da63ce3b12e4497bb20761397493bcbb7477d782afdd5620e91a9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "LambdaEventSourceMappingSelfManagedKafkaEventSourceConfigSchemaRegistryConfigSchemaValidationConfigOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a85f0319ed20d500ac7659fe9c2248184df201c8e01a28551bd8372e235c650)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("LambdaEventSourceMappingSelfManagedKafkaEventSourceConfigSchemaRegistryConfigSchemaValidationConfigOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce8bbc17bd9f0c0abb8b0414a396e4c29951c904d1cb5bc6c32acdcc8496a77b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4a35dbf88d9ba3870153f22ca1370e614e00b76a73e592e66851ea5ee0f3c232)
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
            type_hints = typing.get_type_hints(_typecheckingstub__133f00ae0a10da8bde0d683c6e3777d76470032228c871d81b6ad444eef2300a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LambdaEventSourceMappingSelfManagedKafkaEventSourceConfigSchemaRegistryConfigSchemaValidationConfig]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LambdaEventSourceMappingSelfManagedKafkaEventSourceConfigSchemaRegistryConfigSchemaValidationConfig]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LambdaEventSourceMappingSelfManagedKafkaEventSourceConfigSchemaRegistryConfigSchemaValidationConfig]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__05d22328803e023f320240bb26e2d03a3dfd41fd2c7476919b5f154ae262438f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class LambdaEventSourceMappingSelfManagedKafkaEventSourceConfigSchemaRegistryConfigSchemaValidationConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.lambdaEventSourceMapping.LambdaEventSourceMappingSelfManagedKafkaEventSourceConfigSchemaRegistryConfigSchemaValidationConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2cdb761e7be4ea69fded6680c1008be363033b23b585d37dcda1864b2f557df7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetAttribute")
    def reset_attribute(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAttribute", []))

    @builtins.property
    @jsii.member(jsii_name="attributeInput")
    def attribute_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "attributeInput"))

    @builtins.property
    @jsii.member(jsii_name="attribute")
    def attribute(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "attribute"))

    @attribute.setter
    def attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__03443e0e9e0f33ea7f578dd1ac326e25c00969dab5162849caf7f8b6700ed35c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "attribute", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LambdaEventSourceMappingSelfManagedKafkaEventSourceConfigSchemaRegistryConfigSchemaValidationConfig]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LambdaEventSourceMappingSelfManagedKafkaEventSourceConfigSchemaRegistryConfigSchemaValidationConfig]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LambdaEventSourceMappingSelfManagedKafkaEventSourceConfigSchemaRegistryConfigSchemaValidationConfig]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6fb920fd0a17699c0bef047fd39a21dcb38dffd450e0c321ee00380b215c6837)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.lambdaEventSourceMapping.LambdaEventSourceMappingSourceAccessConfiguration",
    jsii_struct_bases=[],
    name_mapping={"type": "type", "uri": "uri"},
)
class LambdaEventSourceMappingSourceAccessConfiguration:
    def __init__(self, *, type: builtins.str, uri: builtins.str) -> None:
        '''
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/lambda_event_source_mapping#type LambdaEventSourceMapping#type}.
        :param uri: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/lambda_event_source_mapping#uri LambdaEventSourceMapping#uri}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f749b47122b9bf8627a73e0d68e5a12071defd185889c6b9ee5024d6d0c56ea)
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument uri", value=uri, expected_type=type_hints["uri"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "type": type,
            "uri": uri,
        }

    @builtins.property
    def type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/lambda_event_source_mapping#type LambdaEventSourceMapping#type}.'''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def uri(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/lambda_event_source_mapping#uri LambdaEventSourceMapping#uri}.'''
        result = self._values.get("uri")
        assert result is not None, "Required property 'uri' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LambdaEventSourceMappingSourceAccessConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LambdaEventSourceMappingSourceAccessConfigurationList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.lambdaEventSourceMapping.LambdaEventSourceMappingSourceAccessConfigurationList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b8985b422c6d88695b44d933886ca9236f32f376829c246b1e7e4f8bd9fb0c6f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "LambdaEventSourceMappingSourceAccessConfigurationOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3117b2e2f4b8c616c5d264161ea71f205c9701d6f1194bd911b60fc3e2532446)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("LambdaEventSourceMappingSourceAccessConfigurationOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__09481dd8d0fb3245e87c3a245d04ad5551bc07042668b540b4d99249ddd29acc)
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
            type_hints = typing.get_type_hints(_typecheckingstub__94cf9718d242637fcc2263e8bd7fa6113232cd77ad3331c35acbbb244616b686)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bf65c356a4bc87ab20d9a5752ecf6033bfdca646bf56efe47922d4fdfe27562e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LambdaEventSourceMappingSourceAccessConfiguration]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LambdaEventSourceMappingSourceAccessConfiguration]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LambdaEventSourceMappingSourceAccessConfiguration]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__765cea81bf496ba1278e49377193052e975811a5f5751600a86f4ce142ee14c3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class LambdaEventSourceMappingSourceAccessConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.lambdaEventSourceMapping.LambdaEventSourceMappingSourceAccessConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f9c89a4840a4763b1e73653623afb28787f2069fae0f8c4db3f43215aec63322)
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
    @jsii.member(jsii_name="uriInput")
    def uri_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "uriInput"))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ebeffa72cc48a3625370697e7bd01c77b8bec050369175e629c752caed6cd786)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="uri")
    def uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "uri"))

    @uri.setter
    def uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__70eb273fc598e283b663c20be432cb6f94be8b6d5caf501372dd5a423329b91e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "uri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LambdaEventSourceMappingSourceAccessConfiguration]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LambdaEventSourceMappingSourceAccessConfiguration]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LambdaEventSourceMappingSourceAccessConfiguration]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa0313df950f6ce97798b4c90f261a746c6902efc9988912c017a7ce589b97e7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "LambdaEventSourceMapping",
    "LambdaEventSourceMappingAmazonManagedKafkaEventSourceConfig",
    "LambdaEventSourceMappingAmazonManagedKafkaEventSourceConfigOutputReference",
    "LambdaEventSourceMappingAmazonManagedKafkaEventSourceConfigSchemaRegistryConfig",
    "LambdaEventSourceMappingAmazonManagedKafkaEventSourceConfigSchemaRegistryConfigAccessConfig",
    "LambdaEventSourceMappingAmazonManagedKafkaEventSourceConfigSchemaRegistryConfigAccessConfigList",
    "LambdaEventSourceMappingAmazonManagedKafkaEventSourceConfigSchemaRegistryConfigAccessConfigOutputReference",
    "LambdaEventSourceMappingAmazonManagedKafkaEventSourceConfigSchemaRegistryConfigOutputReference",
    "LambdaEventSourceMappingAmazonManagedKafkaEventSourceConfigSchemaRegistryConfigSchemaValidationConfig",
    "LambdaEventSourceMappingAmazonManagedKafkaEventSourceConfigSchemaRegistryConfigSchemaValidationConfigList",
    "LambdaEventSourceMappingAmazonManagedKafkaEventSourceConfigSchemaRegistryConfigSchemaValidationConfigOutputReference",
    "LambdaEventSourceMappingConfig",
    "LambdaEventSourceMappingDestinationConfig",
    "LambdaEventSourceMappingDestinationConfigOnFailure",
    "LambdaEventSourceMappingDestinationConfigOnFailureOutputReference",
    "LambdaEventSourceMappingDestinationConfigOutputReference",
    "LambdaEventSourceMappingDocumentDbEventSourceConfig",
    "LambdaEventSourceMappingDocumentDbEventSourceConfigOutputReference",
    "LambdaEventSourceMappingFilterCriteria",
    "LambdaEventSourceMappingFilterCriteriaFilter",
    "LambdaEventSourceMappingFilterCriteriaFilterList",
    "LambdaEventSourceMappingFilterCriteriaFilterOutputReference",
    "LambdaEventSourceMappingFilterCriteriaOutputReference",
    "LambdaEventSourceMappingMetricsConfig",
    "LambdaEventSourceMappingMetricsConfigOutputReference",
    "LambdaEventSourceMappingProvisionedPollerConfig",
    "LambdaEventSourceMappingProvisionedPollerConfigOutputReference",
    "LambdaEventSourceMappingScalingConfig",
    "LambdaEventSourceMappingScalingConfigOutputReference",
    "LambdaEventSourceMappingSelfManagedEventSource",
    "LambdaEventSourceMappingSelfManagedEventSourceOutputReference",
    "LambdaEventSourceMappingSelfManagedKafkaEventSourceConfig",
    "LambdaEventSourceMappingSelfManagedKafkaEventSourceConfigOutputReference",
    "LambdaEventSourceMappingSelfManagedKafkaEventSourceConfigSchemaRegistryConfig",
    "LambdaEventSourceMappingSelfManagedKafkaEventSourceConfigSchemaRegistryConfigAccessConfig",
    "LambdaEventSourceMappingSelfManagedKafkaEventSourceConfigSchemaRegistryConfigAccessConfigList",
    "LambdaEventSourceMappingSelfManagedKafkaEventSourceConfigSchemaRegistryConfigAccessConfigOutputReference",
    "LambdaEventSourceMappingSelfManagedKafkaEventSourceConfigSchemaRegistryConfigOutputReference",
    "LambdaEventSourceMappingSelfManagedKafkaEventSourceConfigSchemaRegistryConfigSchemaValidationConfig",
    "LambdaEventSourceMappingSelfManagedKafkaEventSourceConfigSchemaRegistryConfigSchemaValidationConfigList",
    "LambdaEventSourceMappingSelfManagedKafkaEventSourceConfigSchemaRegistryConfigSchemaValidationConfigOutputReference",
    "LambdaEventSourceMappingSourceAccessConfiguration",
    "LambdaEventSourceMappingSourceAccessConfigurationList",
    "LambdaEventSourceMappingSourceAccessConfigurationOutputReference",
]

publication.publish()

def _typecheckingstub__4a47aa757339e69266d744016f1501724d691ed438cc3614599356c063048c58(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    function_name: builtins.str,
    amazon_managed_kafka_event_source_config: typing.Optional[typing.Union[LambdaEventSourceMappingAmazonManagedKafkaEventSourceConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    batch_size: typing.Optional[jsii.Number] = None,
    bisect_batch_on_function_error: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    destination_config: typing.Optional[typing.Union[LambdaEventSourceMappingDestinationConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    document_db_event_source_config: typing.Optional[typing.Union[LambdaEventSourceMappingDocumentDbEventSourceConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    event_source_arn: typing.Optional[builtins.str] = None,
    filter_criteria: typing.Optional[typing.Union[LambdaEventSourceMappingFilterCriteria, typing.Dict[builtins.str, typing.Any]]] = None,
    function_response_types: typing.Optional[typing.Sequence[builtins.str]] = None,
    id: typing.Optional[builtins.str] = None,
    kms_key_arn: typing.Optional[builtins.str] = None,
    maximum_batching_window_in_seconds: typing.Optional[jsii.Number] = None,
    maximum_record_age_in_seconds: typing.Optional[jsii.Number] = None,
    maximum_retry_attempts: typing.Optional[jsii.Number] = None,
    metrics_config: typing.Optional[typing.Union[LambdaEventSourceMappingMetricsConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    parallelization_factor: typing.Optional[jsii.Number] = None,
    provisioned_poller_config: typing.Optional[typing.Union[LambdaEventSourceMappingProvisionedPollerConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    queues: typing.Optional[typing.Sequence[builtins.str]] = None,
    region: typing.Optional[builtins.str] = None,
    scaling_config: typing.Optional[typing.Union[LambdaEventSourceMappingScalingConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    self_managed_event_source: typing.Optional[typing.Union[LambdaEventSourceMappingSelfManagedEventSource, typing.Dict[builtins.str, typing.Any]]] = None,
    self_managed_kafka_event_source_config: typing.Optional[typing.Union[LambdaEventSourceMappingSelfManagedKafkaEventSourceConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    source_access_configuration: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[LambdaEventSourceMappingSourceAccessConfiguration, typing.Dict[builtins.str, typing.Any]]]]] = None,
    starting_position: typing.Optional[builtins.str] = None,
    starting_position_timestamp: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    topics: typing.Optional[typing.Sequence[builtins.str]] = None,
    tumbling_window_in_seconds: typing.Optional[jsii.Number] = None,
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

def _typecheckingstub__eea8d2c5ee08d34f355c98fd659c6fe71200fbc91bb8d39c5bb0f36c148cf2aa(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cbca3ef7ec0a8a1ad9afd45f93ea620f3993ef54f83d3249a3bb02da154137a0(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[LambdaEventSourceMappingSourceAccessConfiguration, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__541561415b9451234dacc6dcb3a8b7a5fe5fd4a7af017fb0f870e1133ddc8646(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad19047a73254501ebee29526fb3b3ad7cda341fd1a4cd8b5086fa0f976d6612(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad70d04d1e3f4cf084aa26ef29f1c7c59724e7c8f8976d27fdbc698db3e55742(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25dc16d1d8da84542069b020c23aec363f4216cc95a98064d54479c7dab33671(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c5007634a0b77af02f6cadca8b2bcbbf8db9b6272bd817bc2fce50c7cb023f3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f1bd5ee9b15aa474173407dbbfbf9105cbeaa5930dedf098446736fd5afff22(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39050b5f603238cbae08d6e92e8499f00f28afbb26311d2e2847848f7c3e7591(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef2617f2c1ca86215d5aa08948cb8ce3c0f25742d311827dd7853747d1a20f24(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__007a021ea006cac974f544b05437524be45ecbbea5b8a78164d858df1dc784e7(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf5f5ae47a9906e08465db2184f08779fa1689cac2e02f711eb8c53f6f79d981(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3d838cef1136da132b8bc289f46ead1c226ed7f67d9c262aee72948e00c30a1(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__287ea91a1d6fb462d2b2456cdd406eb601a97f2e9ed98fa645d53ae38934ef73(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46b7dc53557152da3e91935d8f0830c85c6557f96bccb8abe011af284497cd7a(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__95c097ac28a73f90f126727828c925fcf62485bfc4aa6a8532f808271809b4ef(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d34d647942528ee7ce024140746bc344b6c6ac28931ecc0006604fcd0e246a10(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60b0493ea45885b9b7252fcddb33c43c5209138dda3596a7e1c80907cdbf97fb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a39f0dcd86e82622cde53a8f58cdad8e10a19eacf50c8ee402a2819d9808b6f0(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a1169e5dc647d74632c5b9344a5ce70df99d14c1e4e58593f07d8a4a19b3fd7(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d057d80fb2aaa0997a9ee926dbe4dac093c30664f420d247f34f0689c8a100b(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57fc9d9b567503596648cb9a88e55911cf97c51725effa41974546916a0638b3(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ae07895fe3063469b17db40b7a275858ff5d4c6bffee563124c804bda7c3861(
    *,
    consumer_group_id: typing.Optional[builtins.str] = None,
    schema_registry_config: typing.Optional[typing.Union[LambdaEventSourceMappingAmazonManagedKafkaEventSourceConfigSchemaRegistryConfig, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3357452e9a4b48f8661e21aa1beb11ae1098859cc02011d784871e61b0bd1ab2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1bbd65537fdf9a8bed47da88de63a4724981a8abad1ec09f1ca2dc00d76ccf9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__241b103203a35602f493d8495dce6ae9d90c439c6faa223564d7a63305710b64(
    value: typing.Optional[LambdaEventSourceMappingAmazonManagedKafkaEventSourceConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1228503797be6f1fb7ee84671caddc1d96ccb035289d8de7c6cf9f6c984d080(
    *,
    access_config: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[LambdaEventSourceMappingAmazonManagedKafkaEventSourceConfigSchemaRegistryConfigAccessConfig, typing.Dict[builtins.str, typing.Any]]]]] = None,
    event_record_format: typing.Optional[builtins.str] = None,
    schema_registry_uri: typing.Optional[builtins.str] = None,
    schema_validation_config: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[LambdaEventSourceMappingAmazonManagedKafkaEventSourceConfigSchemaRegistryConfigSchemaValidationConfig, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9439b3a1f6b624d452711bc1b4072e5ad4709bf627d0f5e42b144e48eefe1ff1(
    *,
    type: typing.Optional[builtins.str] = None,
    uri: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ff9494978ec5560b507caf669052b5a124a00e70e99d36fdfeabf3c423cd5fd(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8cd212c066733892ac2f3c061249f48df6b45c4d64272f06fcb238ad883e8f33(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dcddf575110667e2f1ecfae2853c2157e61be54499449b173e43c8b0bf3d7a80(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f3796a43e4e289ff638f3852159c36c185f642c1de05fd40509a8ee9f847081(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__342802512fb8c4a67f2aeabf3298720ed2c6a419c8925c8a89f3bd0311275ffb(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5c8c1d37bc8498378e230d6706158029f3f338a0e189082c87fb5f6cd7fe6c0(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LambdaEventSourceMappingAmazonManagedKafkaEventSourceConfigSchemaRegistryConfigAccessConfig]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec31a9cae0e5bd64c6b40f69ad6ee7df35afc62cd605318e86ad6f2e45e89d53(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1a055200d74fabbb10b904a2a3ac60e17c38c3bc64e215b6025a85ceb5e210c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96961dfe44954843fcbe469268db6fa64365e7bc704c236f5dade2e4070f4b54(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc6eba6d2672c96c16de1ad747ece15f532c4b05cbc617ad60de024de733f72d(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LambdaEventSourceMappingAmazonManagedKafkaEventSourceConfigSchemaRegistryConfigAccessConfig]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c2ce45696a4d4f4884210e621e2096f7a585eb7543218ba7a92e5a1caad3eaa(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__409a99b2353ee73a231c34d8d0fd3df0a28e7aa4442a1694a15837b7c940e57e(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[LambdaEventSourceMappingAmazonManagedKafkaEventSourceConfigSchemaRegistryConfigAccessConfig, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e12f30e799da5c8df543a64ed5045d5ca16c2aff83a89ef42362b734d97d15c0(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[LambdaEventSourceMappingAmazonManagedKafkaEventSourceConfigSchemaRegistryConfigSchemaValidationConfig, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0242f9a854bf10317f39c8c7aac19b8493e7d705478bcdc802d49b5ae17675a2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bafd529b50fdc62b8f211210a3e197809075bc97fb833d08dbebf3c6ca8fca7a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c914fb09d08a44aa3aab0e6103157903794054ed0acd0244ab9497429d736aa(
    value: typing.Optional[LambdaEventSourceMappingAmazonManagedKafkaEventSourceConfigSchemaRegistryConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__706d41aa498034f15f6e499755770b0656324eda2504effd714ff32454b5ee21(
    *,
    attribute: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5aae456001749e806d28c535f045e0891f6f1b30248717344d32ffd82cd78d66(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__924b8ec357102a191cc46f317fa6e869f57b4c4fa044b8ab9f55c996c1008362(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1970c3ae4889754beec49df7a38bc7c1fd388b634c4206f00af76687e4865fb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__636105ddd2569e4d550b21f7e69276e32e98beacfaf0a5862e79d3aa6128bb04(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18e677f6cc2aa33e2dab9cbbe1da71dd6351a0c37db6140372e6ab55f21b0f62(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6fd7ed7588e47a3084980edb377c07d2f8085a9ac46e1fa5482cdc00962d80c2(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LambdaEventSourceMappingAmazonManagedKafkaEventSourceConfigSchemaRegistryConfigSchemaValidationConfig]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3574d634b835dd3f34c924f6d865e399691fa0d4be95aefad89327ca838f498a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ebea400851b96720d66e6aaa6029f6edda3577ab160d89524c4c3006693be08c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0dd5ddf2b8a0b162c0751ab600550314512e618502c64a22e3aedaa596a5d3c3(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LambdaEventSourceMappingAmazonManagedKafkaEventSourceConfigSchemaRegistryConfigSchemaValidationConfig]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64877458e53fece918bfc3ada09bc9c10e559b190aa510fbe6c6c28a73b186fa(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    function_name: builtins.str,
    amazon_managed_kafka_event_source_config: typing.Optional[typing.Union[LambdaEventSourceMappingAmazonManagedKafkaEventSourceConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    batch_size: typing.Optional[jsii.Number] = None,
    bisect_batch_on_function_error: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    destination_config: typing.Optional[typing.Union[LambdaEventSourceMappingDestinationConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    document_db_event_source_config: typing.Optional[typing.Union[LambdaEventSourceMappingDocumentDbEventSourceConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    event_source_arn: typing.Optional[builtins.str] = None,
    filter_criteria: typing.Optional[typing.Union[LambdaEventSourceMappingFilterCriteria, typing.Dict[builtins.str, typing.Any]]] = None,
    function_response_types: typing.Optional[typing.Sequence[builtins.str]] = None,
    id: typing.Optional[builtins.str] = None,
    kms_key_arn: typing.Optional[builtins.str] = None,
    maximum_batching_window_in_seconds: typing.Optional[jsii.Number] = None,
    maximum_record_age_in_seconds: typing.Optional[jsii.Number] = None,
    maximum_retry_attempts: typing.Optional[jsii.Number] = None,
    metrics_config: typing.Optional[typing.Union[LambdaEventSourceMappingMetricsConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    parallelization_factor: typing.Optional[jsii.Number] = None,
    provisioned_poller_config: typing.Optional[typing.Union[LambdaEventSourceMappingProvisionedPollerConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    queues: typing.Optional[typing.Sequence[builtins.str]] = None,
    region: typing.Optional[builtins.str] = None,
    scaling_config: typing.Optional[typing.Union[LambdaEventSourceMappingScalingConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    self_managed_event_source: typing.Optional[typing.Union[LambdaEventSourceMappingSelfManagedEventSource, typing.Dict[builtins.str, typing.Any]]] = None,
    self_managed_kafka_event_source_config: typing.Optional[typing.Union[LambdaEventSourceMappingSelfManagedKafkaEventSourceConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    source_access_configuration: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[LambdaEventSourceMappingSourceAccessConfiguration, typing.Dict[builtins.str, typing.Any]]]]] = None,
    starting_position: typing.Optional[builtins.str] = None,
    starting_position_timestamp: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    topics: typing.Optional[typing.Sequence[builtins.str]] = None,
    tumbling_window_in_seconds: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34c9f0b388f168ec909930e18b64b0a89faae7ed714a8203b33b39f48bab681d(
    *,
    on_failure: typing.Optional[typing.Union[LambdaEventSourceMappingDestinationConfigOnFailure, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__576a0eba521c801c96c7b1d9547be6e63b7785dee36315d6db7b6a0550009ad5(
    *,
    destination_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__630832b3b534625a424221bfde5f786d1f1ffddad0ec9ee2a876df687e46e79f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d22489075dff3e3357b483770d6dc55130727cbc7b3314afe0c6aeb655319289(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a40dd6edecd910b3198907903ed7799a03005028da09ae5c3710c7263d48230(
    value: typing.Optional[LambdaEventSourceMappingDestinationConfigOnFailure],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ca1586fcbfe56ac8f4bc2aa11b4c789896b8f4134a70754c4671233ee4f5f50(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b8f60294131cc23ff467227e1e80d5a38227b46da9e8e8c60bfb37f82aa8c95(
    value: typing.Optional[LambdaEventSourceMappingDestinationConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99fa1653eab5203440a24027f6fb7cd266c7bc10e8f42c1b67ae900538c4fac1(
    *,
    database_name: builtins.str,
    collection_name: typing.Optional[builtins.str] = None,
    full_document: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20326743b33fd54d103c07b4e264198d02ea760f78b0e852d9267a264f005a72(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7a3a3fab328428684a37a1cf5a6dcffbb0bc82a76331b01b8a52db8b0672271(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25cece1eac8e663801c2bb8b66f9cb5684881601052875ce3f33c88c14dc3006(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9c3828bf1d72615c8c70bfa86d5f6236cb7b087db482303f90d69e56ec156cb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__850de99fa14e73763e2c5a882085650b1a4e46ad862627bd8795acecbc1055dc(
    value: typing.Optional[LambdaEventSourceMappingDocumentDbEventSourceConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d530693652faef12942656056ae1f83a1f26c650fdda463d012d77ba0938fadb(
    *,
    filter: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[LambdaEventSourceMappingFilterCriteriaFilter, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2eaa4309d2e4ea68d137970b0d83165fe3985ebb4115164a7e2a3154ad8dfbfd(
    *,
    pattern: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d706b5ee3016a7a4ec9c9eadfbc14972d08c40fbcf17ffb761b1c7275c744e5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1175ebc8244990f76740bc49fb76932046078924e37d8f1692ce9bf28a07d7e9(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f053edf2d14673ea9287bdb68915dc2dfc815f22a29ff944c2e0dc414dffad3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa126ca9964bd3aa4fcb977332863782ad6ae733b6d3751c885280f21ffe98ad(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c371c6014487911232332acb2e8eeac5c1569af1b2464330d3014d5e21ef694(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4fdb04d9150902e1b8a2871fbd91e652493a1766a47ef9f3c0595a283979a0cb(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LambdaEventSourceMappingFilterCriteriaFilter]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f501d48e5274adca1b7fcc603ac574a40c9a2dc8779689d6a1928974b68423a7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__214652ec66555668b8bc5a979d45f9b2df52dc741b0765be58a0a239c663407a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d64bf7f51af4a6978326e1aef1f95a6ad437ee14d4282c65c5b4dfb403739cda(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LambdaEventSourceMappingFilterCriteriaFilter]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf90e99296b6b0836dcd21cfedbd96cba0de8817c28b86fe45e5a81d3e9a4a52(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2fed9484a7553309c5a38b3ad891206d0ade480e84f9da82d9b030b886c21c93(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[LambdaEventSourceMappingFilterCriteriaFilter, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1a02ab1e31c47b64c90e7cc7060e5f525711e57eba08e73753d9d15400fd741(
    value: typing.Optional[LambdaEventSourceMappingFilterCriteria],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64e547c770e46f89a09d7d5dcefa3091605d53a49520ddc5ca8700dc17db212a(
    *,
    metrics: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79c5a68212d6b4d3cc7a331786fe68ee7ada1b2459f9474bfac8cfc438332749(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80f3c4b232e970168fa9c86102ad01599df0151390a6f7c039eba0b1b730713f(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ad63dfc73e4b9ffd71b3c05a57799616605f3193f799c87948393abd665230b(
    value: typing.Optional[LambdaEventSourceMappingMetricsConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__285eb7a002851c3c34556637a5863c987eab1abbf787e75d54f204251fb57d1b(
    *,
    maximum_pollers: typing.Optional[jsii.Number] = None,
    minimum_pollers: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4789baee5d183a45c52a283967e86b6913e7eb15518148e72aa2b61d3e97e70b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c15e1cb1a4eabdc71986191828c4355aefc2ee3f799ba427ed79764755c02941(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__49d0b4af5239628b7ed93bcc90d23b520483db5658a93e142869194bde73f194(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e9241e875fdee5d7e44c685e727390f279e6815867c92c0b7f9b0095cb2a434(
    value: typing.Optional[LambdaEventSourceMappingProvisionedPollerConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d74d6f22823d4447bd30c4463f74cf13e167dc8c449028d50cc2571556d00f80(
    *,
    maximum_concurrency: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9b48af60d6343448e06c116989d5aa002180650fe257206020f8134659c6fef(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a4605cb1b88ec7bf7621087fb659a47bd1cfc7f0ac5b3920670ba31c8c53c09(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb9b597563dd679048f132a566cdb4d9caed9f1522b1421e84556b5f7060e685(
    value: typing.Optional[LambdaEventSourceMappingScalingConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f718d9f0c61db275ede06a61fe886dc168521189524bb83565d3da9c025c48e(
    *,
    endpoints: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8bbba2764bd988b4a816a46955500ec7a6c7dceed523e5314b7a48586e45340a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a076c1f8baac0f9ff5ba3dd8e69a900b577e74be7cfbec5ccc8f488fec1896c6(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca82dd2b84242acad82c6883bebd93cea9346581689399f883727e4d44589776(
    value: typing.Optional[LambdaEventSourceMappingSelfManagedEventSource],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__552f5accfcb9ea14c92bd78af097762e0ae1236cab5d2bb2ad88f563414bb309(
    *,
    consumer_group_id: typing.Optional[builtins.str] = None,
    schema_registry_config: typing.Optional[typing.Union[LambdaEventSourceMappingSelfManagedKafkaEventSourceConfigSchemaRegistryConfig, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6356265f44a9462aff0a0bd5cf3e3da9ce2261f824f5f7b98d1fb4c80bbd090(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8e960270f5884b70648a3fbbbed56d1d11a13b177ec49f5c07bbf4b60b5495b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f35651559ea6accdc41caeff6ea91750ce0e9c62392d3992ac409086f2b8948(
    value: typing.Optional[LambdaEventSourceMappingSelfManagedKafkaEventSourceConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4091136fcb90bd3f2a82bc4622d711625efb0702680ad1cc3fd6129fe80938f2(
    *,
    access_config: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[LambdaEventSourceMappingSelfManagedKafkaEventSourceConfigSchemaRegistryConfigAccessConfig, typing.Dict[builtins.str, typing.Any]]]]] = None,
    event_record_format: typing.Optional[builtins.str] = None,
    schema_registry_uri: typing.Optional[builtins.str] = None,
    schema_validation_config: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[LambdaEventSourceMappingSelfManagedKafkaEventSourceConfigSchemaRegistryConfigSchemaValidationConfig, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae2345971cf9293785fda02130e7db8eb6b99ed8574446874582d3d0a0ca9a80(
    *,
    type: typing.Optional[builtins.str] = None,
    uri: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6284230dceb744bc128cf944fe93397abd5e968705d9f1075dee9767735dfa5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__319fc4b2d39eb6c2f7527a836d90305e768acace33e538c79f6c4a7b3cd6240c(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__58925c2a19812652cbb71db7b9ed4219d06c3df69d6fa8bfdf6dc0fcbc4ccb64(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a7ad005fb1ca8b7c0966aee5704c64404d3fa1996e1bca0b6f691724877dc8c(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0aba0afc7ce0e69d6ad215e4979c71a95c32e4168ae296224cfd4082fa3b0886(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da40e67cf3027e978160db7d9fed93e5da7f0fd2286d5f711e551eb135813962(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LambdaEventSourceMappingSelfManagedKafkaEventSourceConfigSchemaRegistryConfigAccessConfig]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f36ba9d7cbe90874472cb80660909f45cf623774eec0fac6ebcfdc2a59aee1d4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93126c0cff3eb239b0c76fc007d6d87cb2ecd07a647e3df71782bdb2f0d71e8a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e94c251504deb20b785832f3b3048d71c0e0236a12ff1c4fef93f80bb37c66a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13a047d414e35735a53eb3b4489876fd5156615cdbb935ac93d15015aaff1b82(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LambdaEventSourceMappingSelfManagedKafkaEventSourceConfigSchemaRegistryConfigAccessConfig]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__649071ac98193455135cce0cd4ec6b8399e254fa52013bba6c3a86585ea9b16d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b26351d072b6afa487c395a95a085179262b63229af2b0eaaf35dec4c75e00b(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[LambdaEventSourceMappingSelfManagedKafkaEventSourceConfigSchemaRegistryConfigAccessConfig, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e006640b840713c14a96954a5ac2826f67e23317c213869fa9573555cf8d8ad(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[LambdaEventSourceMappingSelfManagedKafkaEventSourceConfigSchemaRegistryConfigSchemaValidationConfig, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc5315d585c228e62cf3ab1cfda6ca3425906ad0f23f26e9a5fcde530053a87d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42b79e4a061f5609d5150c390057c125e7c6e8a3f319b48b77a5b76a58894936(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0dcd21e333a0a669c9ec805ed4cc1f8e89249ead26ea72d70dc3a1a13e19907f(
    value: typing.Optional[LambdaEventSourceMappingSelfManagedKafkaEventSourceConfigSchemaRegistryConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eea22668e8fea4cc7ef953eb2cbf279d675a93f856c12642f2a3da6496cac49b(
    *,
    attribute: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d005504f203da63ce3b12e4497bb20761397493bcbb7477d782afdd5620e91a9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a85f0319ed20d500ac7659fe9c2248184df201c8e01a28551bd8372e235c650(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce8bbc17bd9f0c0abb8b0414a396e4c29951c904d1cb5bc6c32acdcc8496a77b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a35dbf88d9ba3870153f22ca1370e614e00b76a73e592e66851ea5ee0f3c232(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__133f00ae0a10da8bde0d683c6e3777d76470032228c871d81b6ad444eef2300a(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05d22328803e023f320240bb26e2d03a3dfd41fd2c7476919b5f154ae262438f(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LambdaEventSourceMappingSelfManagedKafkaEventSourceConfigSchemaRegistryConfigSchemaValidationConfig]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2cdb761e7be4ea69fded6680c1008be363033b23b585d37dcda1864b2f557df7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03443e0e9e0f33ea7f578dd1ac326e25c00969dab5162849caf7f8b6700ed35c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6fb920fd0a17699c0bef047fd39a21dcb38dffd450e0c321ee00380b215c6837(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LambdaEventSourceMappingSelfManagedKafkaEventSourceConfigSchemaRegistryConfigSchemaValidationConfig]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f749b47122b9bf8627a73e0d68e5a12071defd185889c6b9ee5024d6d0c56ea(
    *,
    type: builtins.str,
    uri: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8985b422c6d88695b44d933886ca9236f32f376829c246b1e7e4f8bd9fb0c6f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3117b2e2f4b8c616c5d264161ea71f205c9701d6f1194bd911b60fc3e2532446(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09481dd8d0fb3245e87c3a245d04ad5551bc07042668b540b4d99249ddd29acc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94cf9718d242637fcc2263e8bd7fa6113232cd77ad3331c35acbbb244616b686(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf65c356a4bc87ab20d9a5752ecf6033bfdca646bf56efe47922d4fdfe27562e(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__765cea81bf496ba1278e49377193052e975811a5f5751600a86f4ce142ee14c3(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LambdaEventSourceMappingSourceAccessConfiguration]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9c89a4840a4763b1e73653623afb28787f2069fae0f8c4db3f43215aec63322(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ebeffa72cc48a3625370697e7bd01c77b8bec050369175e629c752caed6cd786(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__70eb273fc598e283b663c20be432cb6f94be8b6d5caf501372dd5a423329b91e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa0313df950f6ce97798b4c90f261a746c6902efc9988912c017a7ce589b97e7(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LambdaEventSourceMappingSourceAccessConfiguration]],
) -> None:
    """Type checking stubs"""
    pass
