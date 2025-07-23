r'''
# `google_storage_transfer_job`

Refer to the Terraform Registry for docs: [`google_storage_transfer_job`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job).
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


class StorageTransferJob(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.storageTransferJob.StorageTransferJob",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job google_storage_transfer_job}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        description: builtins.str,
        event_stream: typing.Optional[typing.Union["StorageTransferJobEventStream", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        logging_config: typing.Optional[typing.Union["StorageTransferJobLoggingConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        name: typing.Optional[builtins.str] = None,
        notification_config: typing.Optional[typing.Union["StorageTransferJobNotificationConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        project: typing.Optional[builtins.str] = None,
        replication_spec: typing.Optional[typing.Union["StorageTransferJobReplicationSpec", typing.Dict[builtins.str, typing.Any]]] = None,
        schedule: typing.Optional[typing.Union["StorageTransferJobSchedule", typing.Dict[builtins.str, typing.Any]]] = None,
        status: typing.Optional[builtins.str] = None,
        transfer_spec: typing.Optional[typing.Union["StorageTransferJobTransferSpec", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job google_storage_transfer_job} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param description: Unique description to identify the Transfer Job. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#description StorageTransferJob#description}
        :param event_stream: event_stream block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#event_stream StorageTransferJob#event_stream}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#id StorageTransferJob#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param logging_config: logging_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#logging_config StorageTransferJob#logging_config}
        :param name: The name of the Transfer Job. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#name StorageTransferJob#name}
        :param notification_config: notification_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#notification_config StorageTransferJob#notification_config}
        :param project: The project in which the resource belongs. If it is not provided, the provider project is used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#project StorageTransferJob#project}
        :param replication_spec: replication_spec block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#replication_spec StorageTransferJob#replication_spec}
        :param schedule: schedule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#schedule StorageTransferJob#schedule}
        :param status: Status of the job. Default: ENABLED. NOTE: The effect of the new job status takes place during a subsequent job run. For example, if you change the job status from ENABLED to DISABLED, and an operation spawned by the transfer is running, the status change would not affect the current operation. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#status StorageTransferJob#status}
        :param transfer_spec: transfer_spec block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#transfer_spec StorageTransferJob#transfer_spec}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__604dde1ca05a28e0d0eadc9cd78311419a134cd77555ce647ed1a5d12bc6d06a)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = StorageTransferJobConfig(
            description=description,
            event_stream=event_stream,
            id=id,
            logging_config=logging_config,
            name=name,
            notification_config=notification_config,
            project=project,
            replication_spec=replication_spec,
            schedule=schedule,
            status=status,
            transfer_spec=transfer_spec,
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
        '''Generates CDKTF code for importing a StorageTransferJob resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the StorageTransferJob to import.
        :param import_from_id: The id of the existing StorageTransferJob that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the StorageTransferJob to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__70670f5bc5ecb71ce90d9b0414f836a3cb56a784a2388ca55db699b23b9d4b00)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putEventStream")
    def put_event_stream(
        self,
        *,
        name: builtins.str,
        event_stream_expiration_time: typing.Optional[builtins.str] = None,
        event_stream_start_time: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: Specifies a unique name of the resource such as AWS SQS ARN in the form 'arn:aws:sqs:region:account_id:queue_name', or Pub/Sub subscription resource name in the form 'projects/{project}/subscriptions/{sub}'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#name StorageTransferJob#name}
        :param event_stream_expiration_time: Specifies the data and time at which Storage Transfer Service stops listening for events from this stream. After this time, any transfers in progress will complete, but no new transfers are initiated Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#event_stream_expiration_time StorageTransferJob#event_stream_expiration_time}
        :param event_stream_start_time: Specifies the date and time that Storage Transfer Service starts listening for events from this stream. If no start time is specified or start time is in the past, Storage Transfer Service starts listening immediately Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#event_stream_start_time StorageTransferJob#event_stream_start_time}
        '''
        value = StorageTransferJobEventStream(
            name=name,
            event_stream_expiration_time=event_stream_expiration_time,
            event_stream_start_time=event_stream_start_time,
        )

        return typing.cast(None, jsii.invoke(self, "putEventStream", [value]))

    @jsii.member(jsii_name="putLoggingConfig")
    def put_logging_config(
        self,
        *,
        enable_on_prem_gcs_transfer_logs: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        log_actions: typing.Optional[typing.Sequence[builtins.str]] = None,
        log_action_states: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param enable_on_prem_gcs_transfer_logs: For transfers with a PosixFilesystem source, this option enables the Cloud Storage transfer logs for this transfer. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#enable_on_prem_gcs_transfer_logs StorageTransferJob#enable_on_prem_gcs_transfer_logs}
        :param log_actions: Specifies the actions to be logged. Not supported for transfers with PosifxFilesystem data sources; use enable_on_prem_gcs_transfer_logs instead. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#log_actions StorageTransferJob#log_actions}
        :param log_action_states: States in which logActions are logged. Not supported for transfers with PosifxFilesystem data sources; use enable_on_prem_gcs_transfer_logs instead. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#log_action_states StorageTransferJob#log_action_states}
        '''
        value = StorageTransferJobLoggingConfig(
            enable_on_prem_gcs_transfer_logs=enable_on_prem_gcs_transfer_logs,
            log_actions=log_actions,
            log_action_states=log_action_states,
        )

        return typing.cast(None, jsii.invoke(self, "putLoggingConfig", [value]))

    @jsii.member(jsii_name="putNotificationConfig")
    def put_notification_config(
        self,
        *,
        payload_format: builtins.str,
        pubsub_topic: builtins.str,
        event_types: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param payload_format: The desired format of the notification message payloads. One of "NONE" or "JSON". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#payload_format StorageTransferJob#payload_format}
        :param pubsub_topic: The Topic.name of the Pub/Sub topic to which to publish notifications. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#pubsub_topic StorageTransferJob#pubsub_topic}
        :param event_types: Event types for which a notification is desired. If empty, send notifications for all event types. The valid types are "TRANSFER_OPERATION_SUCCESS", "TRANSFER_OPERATION_FAILED", "TRANSFER_OPERATION_ABORTED". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#event_types StorageTransferJob#event_types}
        '''
        value = StorageTransferJobNotificationConfig(
            payload_format=payload_format,
            pubsub_topic=pubsub_topic,
            event_types=event_types,
        )

        return typing.cast(None, jsii.invoke(self, "putNotificationConfig", [value]))

    @jsii.member(jsii_name="putReplicationSpec")
    def put_replication_spec(
        self,
        *,
        gcs_data_sink: typing.Optional[typing.Union["StorageTransferJobReplicationSpecGcsDataSink", typing.Dict[builtins.str, typing.Any]]] = None,
        gcs_data_source: typing.Optional[typing.Union["StorageTransferJobReplicationSpecGcsDataSource", typing.Dict[builtins.str, typing.Any]]] = None,
        object_conditions: typing.Optional[typing.Union["StorageTransferJobReplicationSpecObjectConditions", typing.Dict[builtins.str, typing.Any]]] = None,
        transfer_options: typing.Optional[typing.Union["StorageTransferJobReplicationSpecTransferOptions", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param gcs_data_sink: gcs_data_sink block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#gcs_data_sink StorageTransferJob#gcs_data_sink}
        :param gcs_data_source: gcs_data_source block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#gcs_data_source StorageTransferJob#gcs_data_source}
        :param object_conditions: object_conditions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#object_conditions StorageTransferJob#object_conditions}
        :param transfer_options: transfer_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#transfer_options StorageTransferJob#transfer_options}
        '''
        value = StorageTransferJobReplicationSpec(
            gcs_data_sink=gcs_data_sink,
            gcs_data_source=gcs_data_source,
            object_conditions=object_conditions,
            transfer_options=transfer_options,
        )

        return typing.cast(None, jsii.invoke(self, "putReplicationSpec", [value]))

    @jsii.member(jsii_name="putSchedule")
    def put_schedule(
        self,
        *,
        schedule_start_date: typing.Union["StorageTransferJobScheduleScheduleStartDate", typing.Dict[builtins.str, typing.Any]],
        repeat_interval: typing.Optional[builtins.str] = None,
        schedule_end_date: typing.Optional[typing.Union["StorageTransferJobScheduleScheduleEndDate", typing.Dict[builtins.str, typing.Any]]] = None,
        start_time_of_day: typing.Optional[typing.Union["StorageTransferJobScheduleStartTimeOfDay", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param schedule_start_date: schedule_start_date block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#schedule_start_date StorageTransferJob#schedule_start_date}
        :param repeat_interval: Interval between the start of each scheduled transfer. If unspecified, the default value is 24 hours. This value may not be less than 1 hour. A duration in seconds with up to nine fractional digits, terminated by 's'. Example: "3.5s". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#repeat_interval StorageTransferJob#repeat_interval}
        :param schedule_end_date: schedule_end_date block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#schedule_end_date StorageTransferJob#schedule_end_date}
        :param start_time_of_day: start_time_of_day block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#start_time_of_day StorageTransferJob#start_time_of_day}
        '''
        value = StorageTransferJobSchedule(
            schedule_start_date=schedule_start_date,
            repeat_interval=repeat_interval,
            schedule_end_date=schedule_end_date,
            start_time_of_day=start_time_of_day,
        )

        return typing.cast(None, jsii.invoke(self, "putSchedule", [value]))

    @jsii.member(jsii_name="putTransferSpec")
    def put_transfer_spec(
        self,
        *,
        aws_s3_data_source: typing.Optional[typing.Union["StorageTransferJobTransferSpecAwsS3DataSource", typing.Dict[builtins.str, typing.Any]]] = None,
        azure_blob_storage_data_source: typing.Optional[typing.Union["StorageTransferJobTransferSpecAzureBlobStorageDataSource", typing.Dict[builtins.str, typing.Any]]] = None,
        gcs_data_sink: typing.Optional[typing.Union["StorageTransferJobTransferSpecGcsDataSink", typing.Dict[builtins.str, typing.Any]]] = None,
        gcs_data_source: typing.Optional[typing.Union["StorageTransferJobTransferSpecGcsDataSource", typing.Dict[builtins.str, typing.Any]]] = None,
        hdfs_data_source: typing.Optional[typing.Union["StorageTransferJobTransferSpecHdfsDataSource", typing.Dict[builtins.str, typing.Any]]] = None,
        http_data_source: typing.Optional[typing.Union["StorageTransferJobTransferSpecHttpDataSource", typing.Dict[builtins.str, typing.Any]]] = None,
        object_conditions: typing.Optional[typing.Union["StorageTransferJobTransferSpecObjectConditions", typing.Dict[builtins.str, typing.Any]]] = None,
        posix_data_sink: typing.Optional[typing.Union["StorageTransferJobTransferSpecPosixDataSink", typing.Dict[builtins.str, typing.Any]]] = None,
        posix_data_source: typing.Optional[typing.Union["StorageTransferJobTransferSpecPosixDataSource", typing.Dict[builtins.str, typing.Any]]] = None,
        sink_agent_pool_name: typing.Optional[builtins.str] = None,
        source_agent_pool_name: typing.Optional[builtins.str] = None,
        transfer_options: typing.Optional[typing.Union["StorageTransferJobTransferSpecTransferOptions", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param aws_s3_data_source: aws_s3_data_source block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#aws_s3_data_source StorageTransferJob#aws_s3_data_source}
        :param azure_blob_storage_data_source: azure_blob_storage_data_source block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#azure_blob_storage_data_source StorageTransferJob#azure_blob_storage_data_source}
        :param gcs_data_sink: gcs_data_sink block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#gcs_data_sink StorageTransferJob#gcs_data_sink}
        :param gcs_data_source: gcs_data_source block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#gcs_data_source StorageTransferJob#gcs_data_source}
        :param hdfs_data_source: hdfs_data_source block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#hdfs_data_source StorageTransferJob#hdfs_data_source}
        :param http_data_source: http_data_source block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#http_data_source StorageTransferJob#http_data_source}
        :param object_conditions: object_conditions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#object_conditions StorageTransferJob#object_conditions}
        :param posix_data_sink: posix_data_sink block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#posix_data_sink StorageTransferJob#posix_data_sink}
        :param posix_data_source: posix_data_source block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#posix_data_source StorageTransferJob#posix_data_source}
        :param sink_agent_pool_name: Specifies the agent pool name associated with the posix data source. When unspecified, the default name is used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#sink_agent_pool_name StorageTransferJob#sink_agent_pool_name}
        :param source_agent_pool_name: Specifies the agent pool name associated with the posix data source. When unspecified, the default name is used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#source_agent_pool_name StorageTransferJob#source_agent_pool_name}
        :param transfer_options: transfer_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#transfer_options StorageTransferJob#transfer_options}
        '''
        value = StorageTransferJobTransferSpec(
            aws_s3_data_source=aws_s3_data_source,
            azure_blob_storage_data_source=azure_blob_storage_data_source,
            gcs_data_sink=gcs_data_sink,
            gcs_data_source=gcs_data_source,
            hdfs_data_source=hdfs_data_source,
            http_data_source=http_data_source,
            object_conditions=object_conditions,
            posix_data_sink=posix_data_sink,
            posix_data_source=posix_data_source,
            sink_agent_pool_name=sink_agent_pool_name,
            source_agent_pool_name=source_agent_pool_name,
            transfer_options=transfer_options,
        )

        return typing.cast(None, jsii.invoke(self, "putTransferSpec", [value]))

    @jsii.member(jsii_name="resetEventStream")
    def reset_event_stream(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEventStream", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetLoggingConfig")
    def reset_logging_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLoggingConfig", []))

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @jsii.member(jsii_name="resetNotificationConfig")
    def reset_notification_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNotificationConfig", []))

    @jsii.member(jsii_name="resetProject")
    def reset_project(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProject", []))

    @jsii.member(jsii_name="resetReplicationSpec")
    def reset_replication_spec(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetReplicationSpec", []))

    @jsii.member(jsii_name="resetSchedule")
    def reset_schedule(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSchedule", []))

    @jsii.member(jsii_name="resetStatus")
    def reset_status(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStatus", []))

    @jsii.member(jsii_name="resetTransferSpec")
    def reset_transfer_spec(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTransferSpec", []))

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
    @jsii.member(jsii_name="creationTime")
    def creation_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "creationTime"))

    @builtins.property
    @jsii.member(jsii_name="deletionTime")
    def deletion_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "deletionTime"))

    @builtins.property
    @jsii.member(jsii_name="eventStream")
    def event_stream(self) -> "StorageTransferJobEventStreamOutputReference":
        return typing.cast("StorageTransferJobEventStreamOutputReference", jsii.get(self, "eventStream"))

    @builtins.property
    @jsii.member(jsii_name="lastModificationTime")
    def last_modification_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "lastModificationTime"))

    @builtins.property
    @jsii.member(jsii_name="loggingConfig")
    def logging_config(self) -> "StorageTransferJobLoggingConfigOutputReference":
        return typing.cast("StorageTransferJobLoggingConfigOutputReference", jsii.get(self, "loggingConfig"))

    @builtins.property
    @jsii.member(jsii_name="notificationConfig")
    def notification_config(
        self,
    ) -> "StorageTransferJobNotificationConfigOutputReference":
        return typing.cast("StorageTransferJobNotificationConfigOutputReference", jsii.get(self, "notificationConfig"))

    @builtins.property
    @jsii.member(jsii_name="replicationSpec")
    def replication_spec(self) -> "StorageTransferJobReplicationSpecOutputReference":
        return typing.cast("StorageTransferJobReplicationSpecOutputReference", jsii.get(self, "replicationSpec"))

    @builtins.property
    @jsii.member(jsii_name="schedule")
    def schedule(self) -> "StorageTransferJobScheduleOutputReference":
        return typing.cast("StorageTransferJobScheduleOutputReference", jsii.get(self, "schedule"))

    @builtins.property
    @jsii.member(jsii_name="transferSpec")
    def transfer_spec(self) -> "StorageTransferJobTransferSpecOutputReference":
        return typing.cast("StorageTransferJobTransferSpecOutputReference", jsii.get(self, "transferSpec"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="eventStreamInput")
    def event_stream_input(self) -> typing.Optional["StorageTransferJobEventStream"]:
        return typing.cast(typing.Optional["StorageTransferJobEventStream"], jsii.get(self, "eventStreamInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="loggingConfigInput")
    def logging_config_input(
        self,
    ) -> typing.Optional["StorageTransferJobLoggingConfig"]:
        return typing.cast(typing.Optional["StorageTransferJobLoggingConfig"], jsii.get(self, "loggingConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="notificationConfigInput")
    def notification_config_input(
        self,
    ) -> typing.Optional["StorageTransferJobNotificationConfig"]:
        return typing.cast(typing.Optional["StorageTransferJobNotificationConfig"], jsii.get(self, "notificationConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="replicationSpecInput")
    def replication_spec_input(
        self,
    ) -> typing.Optional["StorageTransferJobReplicationSpec"]:
        return typing.cast(typing.Optional["StorageTransferJobReplicationSpec"], jsii.get(self, "replicationSpecInput"))

    @builtins.property
    @jsii.member(jsii_name="scheduleInput")
    def schedule_input(self) -> typing.Optional["StorageTransferJobSchedule"]:
        return typing.cast(typing.Optional["StorageTransferJobSchedule"], jsii.get(self, "scheduleInput"))

    @builtins.property
    @jsii.member(jsii_name="statusInput")
    def status_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "statusInput"))

    @builtins.property
    @jsii.member(jsii_name="transferSpecInput")
    def transfer_spec_input(self) -> typing.Optional["StorageTransferJobTransferSpec"]:
        return typing.cast(typing.Optional["StorageTransferJobTransferSpec"], jsii.get(self, "transferSpecInput"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b483074f400562bcc10f134813a4e32c8b2eb1781548cb51a9944a5a7758f6d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0e3064fd2589fdf6619f06091bb32992194c3f99e74f5e56097d0141e72fff26)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__47128417076e48e19d2bf000abbbaf4d51cbd1243e233f128a8a340728a550f0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f863572eaade88173fd667d45896dd44ff3c8c2f9db5a63d46274cd80f8f1d0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "status"))

    @status.setter
    def status(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__32d13d6bdccd1e488087f39d659df6104839f743d1c7892faafc74ccd0900c57)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "status", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.storageTransferJob.StorageTransferJobConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "description": "description",
        "event_stream": "eventStream",
        "id": "id",
        "logging_config": "loggingConfig",
        "name": "name",
        "notification_config": "notificationConfig",
        "project": "project",
        "replication_spec": "replicationSpec",
        "schedule": "schedule",
        "status": "status",
        "transfer_spec": "transferSpec",
    },
)
class StorageTransferJobConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        description: builtins.str,
        event_stream: typing.Optional[typing.Union["StorageTransferJobEventStream", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        logging_config: typing.Optional[typing.Union["StorageTransferJobLoggingConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        name: typing.Optional[builtins.str] = None,
        notification_config: typing.Optional[typing.Union["StorageTransferJobNotificationConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        project: typing.Optional[builtins.str] = None,
        replication_spec: typing.Optional[typing.Union["StorageTransferJobReplicationSpec", typing.Dict[builtins.str, typing.Any]]] = None,
        schedule: typing.Optional[typing.Union["StorageTransferJobSchedule", typing.Dict[builtins.str, typing.Any]]] = None,
        status: typing.Optional[builtins.str] = None,
        transfer_spec: typing.Optional[typing.Union["StorageTransferJobTransferSpec", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param description: Unique description to identify the Transfer Job. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#description StorageTransferJob#description}
        :param event_stream: event_stream block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#event_stream StorageTransferJob#event_stream}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#id StorageTransferJob#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param logging_config: logging_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#logging_config StorageTransferJob#logging_config}
        :param name: The name of the Transfer Job. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#name StorageTransferJob#name}
        :param notification_config: notification_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#notification_config StorageTransferJob#notification_config}
        :param project: The project in which the resource belongs. If it is not provided, the provider project is used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#project StorageTransferJob#project}
        :param replication_spec: replication_spec block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#replication_spec StorageTransferJob#replication_spec}
        :param schedule: schedule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#schedule StorageTransferJob#schedule}
        :param status: Status of the job. Default: ENABLED. NOTE: The effect of the new job status takes place during a subsequent job run. For example, if you change the job status from ENABLED to DISABLED, and an operation spawned by the transfer is running, the status change would not affect the current operation. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#status StorageTransferJob#status}
        :param transfer_spec: transfer_spec block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#transfer_spec StorageTransferJob#transfer_spec}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(event_stream, dict):
            event_stream = StorageTransferJobEventStream(**event_stream)
        if isinstance(logging_config, dict):
            logging_config = StorageTransferJobLoggingConfig(**logging_config)
        if isinstance(notification_config, dict):
            notification_config = StorageTransferJobNotificationConfig(**notification_config)
        if isinstance(replication_spec, dict):
            replication_spec = StorageTransferJobReplicationSpec(**replication_spec)
        if isinstance(schedule, dict):
            schedule = StorageTransferJobSchedule(**schedule)
        if isinstance(transfer_spec, dict):
            transfer_spec = StorageTransferJobTransferSpec(**transfer_spec)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__740ad737fa45784b1c1563b5d1543a9ed33431538cc7585d37dd89670e91bbd6)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument event_stream", value=event_stream, expected_type=type_hints["event_stream"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument logging_config", value=logging_config, expected_type=type_hints["logging_config"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument notification_config", value=notification_config, expected_type=type_hints["notification_config"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument replication_spec", value=replication_spec, expected_type=type_hints["replication_spec"])
            check_type(argname="argument schedule", value=schedule, expected_type=type_hints["schedule"])
            check_type(argname="argument status", value=status, expected_type=type_hints["status"])
            check_type(argname="argument transfer_spec", value=transfer_spec, expected_type=type_hints["transfer_spec"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "description": description,
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
        if event_stream is not None:
            self._values["event_stream"] = event_stream
        if id is not None:
            self._values["id"] = id
        if logging_config is not None:
            self._values["logging_config"] = logging_config
        if name is not None:
            self._values["name"] = name
        if notification_config is not None:
            self._values["notification_config"] = notification_config
        if project is not None:
            self._values["project"] = project
        if replication_spec is not None:
            self._values["replication_spec"] = replication_spec
        if schedule is not None:
            self._values["schedule"] = schedule
        if status is not None:
            self._values["status"] = status
        if transfer_spec is not None:
            self._values["transfer_spec"] = transfer_spec

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
    def description(self) -> builtins.str:
        '''Unique description to identify the Transfer Job.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#description StorageTransferJob#description}
        '''
        result = self._values.get("description")
        assert result is not None, "Required property 'description' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def event_stream(self) -> typing.Optional["StorageTransferJobEventStream"]:
        '''event_stream block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#event_stream StorageTransferJob#event_stream}
        '''
        result = self._values.get("event_stream")
        return typing.cast(typing.Optional["StorageTransferJobEventStream"], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#id StorageTransferJob#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def logging_config(self) -> typing.Optional["StorageTransferJobLoggingConfig"]:
        '''logging_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#logging_config StorageTransferJob#logging_config}
        '''
        result = self._values.get("logging_config")
        return typing.cast(typing.Optional["StorageTransferJobLoggingConfig"], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the Transfer Job.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#name StorageTransferJob#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def notification_config(
        self,
    ) -> typing.Optional["StorageTransferJobNotificationConfig"]:
        '''notification_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#notification_config StorageTransferJob#notification_config}
        '''
        result = self._values.get("notification_config")
        return typing.cast(typing.Optional["StorageTransferJobNotificationConfig"], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''The project in which the resource belongs. If it is not provided, the provider project is used.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#project StorageTransferJob#project}
        '''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def replication_spec(self) -> typing.Optional["StorageTransferJobReplicationSpec"]:
        '''replication_spec block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#replication_spec StorageTransferJob#replication_spec}
        '''
        result = self._values.get("replication_spec")
        return typing.cast(typing.Optional["StorageTransferJobReplicationSpec"], result)

    @builtins.property
    def schedule(self) -> typing.Optional["StorageTransferJobSchedule"]:
        '''schedule block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#schedule StorageTransferJob#schedule}
        '''
        result = self._values.get("schedule")
        return typing.cast(typing.Optional["StorageTransferJobSchedule"], result)

    @builtins.property
    def status(self) -> typing.Optional[builtins.str]:
        '''Status of the job.

        Default: ENABLED. NOTE: The effect of the new job status takes place during a subsequent job run. For example, if you change the job status from ENABLED to DISABLED, and an operation spawned by the transfer is running, the status change would not affect the current operation.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#status StorageTransferJob#status}
        '''
        result = self._values.get("status")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def transfer_spec(self) -> typing.Optional["StorageTransferJobTransferSpec"]:
        '''transfer_spec block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#transfer_spec StorageTransferJob#transfer_spec}
        '''
        result = self._values.get("transfer_spec")
        return typing.cast(typing.Optional["StorageTransferJobTransferSpec"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StorageTransferJobConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.storageTransferJob.StorageTransferJobEventStream",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "event_stream_expiration_time": "eventStreamExpirationTime",
        "event_stream_start_time": "eventStreamStartTime",
    },
)
class StorageTransferJobEventStream:
    def __init__(
        self,
        *,
        name: builtins.str,
        event_stream_expiration_time: typing.Optional[builtins.str] = None,
        event_stream_start_time: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: Specifies a unique name of the resource such as AWS SQS ARN in the form 'arn:aws:sqs:region:account_id:queue_name', or Pub/Sub subscription resource name in the form 'projects/{project}/subscriptions/{sub}'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#name StorageTransferJob#name}
        :param event_stream_expiration_time: Specifies the data and time at which Storage Transfer Service stops listening for events from this stream. After this time, any transfers in progress will complete, but no new transfers are initiated Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#event_stream_expiration_time StorageTransferJob#event_stream_expiration_time}
        :param event_stream_start_time: Specifies the date and time that Storage Transfer Service starts listening for events from this stream. If no start time is specified or start time is in the past, Storage Transfer Service starts listening immediately Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#event_stream_start_time StorageTransferJob#event_stream_start_time}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__48041b3a819c6f62ef03bf6defd68d8fb07ddd4f5266ffc2c5daa1f436c4ddb1)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument event_stream_expiration_time", value=event_stream_expiration_time, expected_type=type_hints["event_stream_expiration_time"])
            check_type(argname="argument event_stream_start_time", value=event_stream_start_time, expected_type=type_hints["event_stream_start_time"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }
        if event_stream_expiration_time is not None:
            self._values["event_stream_expiration_time"] = event_stream_expiration_time
        if event_stream_start_time is not None:
            self._values["event_stream_start_time"] = event_stream_start_time

    @builtins.property
    def name(self) -> builtins.str:
        '''Specifies a unique name of the resource such as AWS SQS ARN in the form 'arn:aws:sqs:region:account_id:queue_name', or Pub/Sub subscription resource name in the form 'projects/{project}/subscriptions/{sub}'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#name StorageTransferJob#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def event_stream_expiration_time(self) -> typing.Optional[builtins.str]:
        '''Specifies the data and time at which Storage Transfer Service stops listening for events from this stream.

        After this time, any transfers in progress will complete, but no new transfers are initiated

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#event_stream_expiration_time StorageTransferJob#event_stream_expiration_time}
        '''
        result = self._values.get("event_stream_expiration_time")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def event_stream_start_time(self) -> typing.Optional[builtins.str]:
        '''Specifies the date and time that Storage Transfer Service starts listening for events from this stream.

        If no start time is specified or start time is in the past, Storage Transfer Service starts listening immediately

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#event_stream_start_time StorageTransferJob#event_stream_start_time}
        '''
        result = self._values.get("event_stream_start_time")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StorageTransferJobEventStream(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class StorageTransferJobEventStreamOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.storageTransferJob.StorageTransferJobEventStreamOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__22dbb68d4c01844ce62d4db03f2ee354faaddc10251a318d94656276dd6920a0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetEventStreamExpirationTime")
    def reset_event_stream_expiration_time(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEventStreamExpirationTime", []))

    @jsii.member(jsii_name="resetEventStreamStartTime")
    def reset_event_stream_start_time(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEventStreamStartTime", []))

    @builtins.property
    @jsii.member(jsii_name="eventStreamExpirationTimeInput")
    def event_stream_expiration_time_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "eventStreamExpirationTimeInput"))

    @builtins.property
    @jsii.member(jsii_name="eventStreamStartTimeInput")
    def event_stream_start_time_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "eventStreamStartTimeInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="eventStreamExpirationTime")
    def event_stream_expiration_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "eventStreamExpirationTime"))

    @event_stream_expiration_time.setter
    def event_stream_expiration_time(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bdb5e574be986d5a1947d95d1b230cae2390478a785075ff82654a2d304f0fb3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "eventStreamExpirationTime", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="eventStreamStartTime")
    def event_stream_start_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "eventStreamStartTime"))

    @event_stream_start_time.setter
    def event_stream_start_time(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5d9efc1ca7f8278ad9c84d7a1644f5c7b660fd46d4ee54d4472ef514dde80aa4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "eventStreamStartTime", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e7194355bdf2d69d5722006235e1d67d84745e240f7195673a4d5ed2e35162a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[StorageTransferJobEventStream]:
        return typing.cast(typing.Optional[StorageTransferJobEventStream], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[StorageTransferJobEventStream],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__44bde1e4e9f2ec4ac317c1071bb54751f3ce46ac645e414c9788376f2223d767)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.storageTransferJob.StorageTransferJobLoggingConfig",
    jsii_struct_bases=[],
    name_mapping={
        "enable_on_prem_gcs_transfer_logs": "enableOnPremGcsTransferLogs",
        "log_actions": "logActions",
        "log_action_states": "logActionStates",
    },
)
class StorageTransferJobLoggingConfig:
    def __init__(
        self,
        *,
        enable_on_prem_gcs_transfer_logs: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        log_actions: typing.Optional[typing.Sequence[builtins.str]] = None,
        log_action_states: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param enable_on_prem_gcs_transfer_logs: For transfers with a PosixFilesystem source, this option enables the Cloud Storage transfer logs for this transfer. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#enable_on_prem_gcs_transfer_logs StorageTransferJob#enable_on_prem_gcs_transfer_logs}
        :param log_actions: Specifies the actions to be logged. Not supported for transfers with PosifxFilesystem data sources; use enable_on_prem_gcs_transfer_logs instead. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#log_actions StorageTransferJob#log_actions}
        :param log_action_states: States in which logActions are logged. Not supported for transfers with PosifxFilesystem data sources; use enable_on_prem_gcs_transfer_logs instead. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#log_action_states StorageTransferJob#log_action_states}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__97a19045f96d78d06d5208c1f2f56c719f1831ec65c3bcb4c8686c351b496765)
            check_type(argname="argument enable_on_prem_gcs_transfer_logs", value=enable_on_prem_gcs_transfer_logs, expected_type=type_hints["enable_on_prem_gcs_transfer_logs"])
            check_type(argname="argument log_actions", value=log_actions, expected_type=type_hints["log_actions"])
            check_type(argname="argument log_action_states", value=log_action_states, expected_type=type_hints["log_action_states"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if enable_on_prem_gcs_transfer_logs is not None:
            self._values["enable_on_prem_gcs_transfer_logs"] = enable_on_prem_gcs_transfer_logs
        if log_actions is not None:
            self._values["log_actions"] = log_actions
        if log_action_states is not None:
            self._values["log_action_states"] = log_action_states

    @builtins.property
    def enable_on_prem_gcs_transfer_logs(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''For transfers with a PosixFilesystem source, this option enables the Cloud Storage transfer logs for this transfer.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#enable_on_prem_gcs_transfer_logs StorageTransferJob#enable_on_prem_gcs_transfer_logs}
        '''
        result = self._values.get("enable_on_prem_gcs_transfer_logs")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def log_actions(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Specifies the actions to be logged. Not supported for transfers with PosifxFilesystem data sources; use enable_on_prem_gcs_transfer_logs instead.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#log_actions StorageTransferJob#log_actions}
        '''
        result = self._values.get("log_actions")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def log_action_states(self) -> typing.Optional[typing.List[builtins.str]]:
        '''States in which logActions are logged. Not supported for transfers with PosifxFilesystem data sources; use enable_on_prem_gcs_transfer_logs instead.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#log_action_states StorageTransferJob#log_action_states}
        '''
        result = self._values.get("log_action_states")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StorageTransferJobLoggingConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class StorageTransferJobLoggingConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.storageTransferJob.StorageTransferJobLoggingConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__04c259e2ecc4d7577c4a0789dbfa2f9bf9d298af6d684dd58c5f6c68d895c979)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetEnableOnPremGcsTransferLogs")
    def reset_enable_on_prem_gcs_transfer_logs(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnableOnPremGcsTransferLogs", []))

    @jsii.member(jsii_name="resetLogActions")
    def reset_log_actions(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLogActions", []))

    @jsii.member(jsii_name="resetLogActionStates")
    def reset_log_action_states(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLogActionStates", []))

    @builtins.property
    @jsii.member(jsii_name="enableOnPremGcsTransferLogsInput")
    def enable_on_prem_gcs_transfer_logs_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enableOnPremGcsTransferLogsInput"))

    @builtins.property
    @jsii.member(jsii_name="logActionsInput")
    def log_actions_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "logActionsInput"))

    @builtins.property
    @jsii.member(jsii_name="logActionStatesInput")
    def log_action_states_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "logActionStatesInput"))

    @builtins.property
    @jsii.member(jsii_name="enableOnPremGcsTransferLogs")
    def enable_on_prem_gcs_transfer_logs(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enableOnPremGcsTransferLogs"))

    @enable_on_prem_gcs_transfer_logs.setter
    def enable_on_prem_gcs_transfer_logs(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ad35f5b941101334fdba41daa8e6f36138d584ba5afd180be09dfe69bd25c125)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableOnPremGcsTransferLogs", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="logActions")
    def log_actions(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "logActions"))

    @log_actions.setter
    def log_actions(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__89c70e478571dd4ba6904d8d1a9d32551b656aa1972b2943e05e2e35d83f24f8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "logActions", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="logActionStates")
    def log_action_states(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "logActionStates"))

    @log_action_states.setter
    def log_action_states(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__71654c1ddbe89185675ee096241c8a43d6b0a7e048a6e733b8f465097754c4e4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "logActionStates", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[StorageTransferJobLoggingConfig]:
        return typing.cast(typing.Optional[StorageTransferJobLoggingConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[StorageTransferJobLoggingConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__929457f6b1a13b41a817e522196b982218dcc1fd73de8afd22bd4f49e31fb5b7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.storageTransferJob.StorageTransferJobNotificationConfig",
    jsii_struct_bases=[],
    name_mapping={
        "payload_format": "payloadFormat",
        "pubsub_topic": "pubsubTopic",
        "event_types": "eventTypes",
    },
)
class StorageTransferJobNotificationConfig:
    def __init__(
        self,
        *,
        payload_format: builtins.str,
        pubsub_topic: builtins.str,
        event_types: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param payload_format: The desired format of the notification message payloads. One of "NONE" or "JSON". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#payload_format StorageTransferJob#payload_format}
        :param pubsub_topic: The Topic.name of the Pub/Sub topic to which to publish notifications. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#pubsub_topic StorageTransferJob#pubsub_topic}
        :param event_types: Event types for which a notification is desired. If empty, send notifications for all event types. The valid types are "TRANSFER_OPERATION_SUCCESS", "TRANSFER_OPERATION_FAILED", "TRANSFER_OPERATION_ABORTED". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#event_types StorageTransferJob#event_types}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__39f876b24cbf33ea9cfc5d7bbc8af8361b054125b2cd24159595aaa968c8d0b1)
            check_type(argname="argument payload_format", value=payload_format, expected_type=type_hints["payload_format"])
            check_type(argname="argument pubsub_topic", value=pubsub_topic, expected_type=type_hints["pubsub_topic"])
            check_type(argname="argument event_types", value=event_types, expected_type=type_hints["event_types"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "payload_format": payload_format,
            "pubsub_topic": pubsub_topic,
        }
        if event_types is not None:
            self._values["event_types"] = event_types

    @builtins.property
    def payload_format(self) -> builtins.str:
        '''The desired format of the notification message payloads. One of "NONE" or "JSON".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#payload_format StorageTransferJob#payload_format}
        '''
        result = self._values.get("payload_format")
        assert result is not None, "Required property 'payload_format' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def pubsub_topic(self) -> builtins.str:
        '''The Topic.name of the Pub/Sub topic to which to publish notifications.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#pubsub_topic StorageTransferJob#pubsub_topic}
        '''
        result = self._values.get("pubsub_topic")
        assert result is not None, "Required property 'pubsub_topic' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def event_types(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Event types for which a notification is desired.

        If empty, send notifications for all event types. The valid types are "TRANSFER_OPERATION_SUCCESS", "TRANSFER_OPERATION_FAILED", "TRANSFER_OPERATION_ABORTED".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#event_types StorageTransferJob#event_types}
        '''
        result = self._values.get("event_types")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StorageTransferJobNotificationConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class StorageTransferJobNotificationConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.storageTransferJob.StorageTransferJobNotificationConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__db98b0a9f7e0c0a7d5349b2a2274df84c77d18b1662fe449a18c11e83d9190eb)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetEventTypes")
    def reset_event_types(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEventTypes", []))

    @builtins.property
    @jsii.member(jsii_name="eventTypesInput")
    def event_types_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "eventTypesInput"))

    @builtins.property
    @jsii.member(jsii_name="payloadFormatInput")
    def payload_format_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "payloadFormatInput"))

    @builtins.property
    @jsii.member(jsii_name="pubsubTopicInput")
    def pubsub_topic_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pubsubTopicInput"))

    @builtins.property
    @jsii.member(jsii_name="eventTypes")
    def event_types(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "eventTypes"))

    @event_types.setter
    def event_types(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8131351a83d749d77320e2a4cadc7ce851076e6a86ebe867d3842cba71941508)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "eventTypes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="payloadFormat")
    def payload_format(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "payloadFormat"))

    @payload_format.setter
    def payload_format(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6a16bc9a7653f7a6bf7df394d9081c26d32c9e812031c4a1ec36428dff9e1183)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "payloadFormat", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="pubsubTopic")
    def pubsub_topic(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "pubsubTopic"))

    @pubsub_topic.setter
    def pubsub_topic(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ccda11c16c2c8dcd8f8a75d194a6be0f29ea5a7c162185cf11744ccbed559e5a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pubsubTopic", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[StorageTransferJobNotificationConfig]:
        return typing.cast(typing.Optional[StorageTransferJobNotificationConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[StorageTransferJobNotificationConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8b1f15d32aa63b27797f79cf3e26d4819d21bed0622034a3f95cedb09d467272)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.storageTransferJob.StorageTransferJobReplicationSpec",
    jsii_struct_bases=[],
    name_mapping={
        "gcs_data_sink": "gcsDataSink",
        "gcs_data_source": "gcsDataSource",
        "object_conditions": "objectConditions",
        "transfer_options": "transferOptions",
    },
)
class StorageTransferJobReplicationSpec:
    def __init__(
        self,
        *,
        gcs_data_sink: typing.Optional[typing.Union["StorageTransferJobReplicationSpecGcsDataSink", typing.Dict[builtins.str, typing.Any]]] = None,
        gcs_data_source: typing.Optional[typing.Union["StorageTransferJobReplicationSpecGcsDataSource", typing.Dict[builtins.str, typing.Any]]] = None,
        object_conditions: typing.Optional[typing.Union["StorageTransferJobReplicationSpecObjectConditions", typing.Dict[builtins.str, typing.Any]]] = None,
        transfer_options: typing.Optional[typing.Union["StorageTransferJobReplicationSpecTransferOptions", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param gcs_data_sink: gcs_data_sink block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#gcs_data_sink StorageTransferJob#gcs_data_sink}
        :param gcs_data_source: gcs_data_source block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#gcs_data_source StorageTransferJob#gcs_data_source}
        :param object_conditions: object_conditions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#object_conditions StorageTransferJob#object_conditions}
        :param transfer_options: transfer_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#transfer_options StorageTransferJob#transfer_options}
        '''
        if isinstance(gcs_data_sink, dict):
            gcs_data_sink = StorageTransferJobReplicationSpecGcsDataSink(**gcs_data_sink)
        if isinstance(gcs_data_source, dict):
            gcs_data_source = StorageTransferJobReplicationSpecGcsDataSource(**gcs_data_source)
        if isinstance(object_conditions, dict):
            object_conditions = StorageTransferJobReplicationSpecObjectConditions(**object_conditions)
        if isinstance(transfer_options, dict):
            transfer_options = StorageTransferJobReplicationSpecTransferOptions(**transfer_options)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e67a99cce8a9779c5b10a6d37389d369bb25c038db1b64969221d24e61f01845)
            check_type(argname="argument gcs_data_sink", value=gcs_data_sink, expected_type=type_hints["gcs_data_sink"])
            check_type(argname="argument gcs_data_source", value=gcs_data_source, expected_type=type_hints["gcs_data_source"])
            check_type(argname="argument object_conditions", value=object_conditions, expected_type=type_hints["object_conditions"])
            check_type(argname="argument transfer_options", value=transfer_options, expected_type=type_hints["transfer_options"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if gcs_data_sink is not None:
            self._values["gcs_data_sink"] = gcs_data_sink
        if gcs_data_source is not None:
            self._values["gcs_data_source"] = gcs_data_source
        if object_conditions is not None:
            self._values["object_conditions"] = object_conditions
        if transfer_options is not None:
            self._values["transfer_options"] = transfer_options

    @builtins.property
    def gcs_data_sink(
        self,
    ) -> typing.Optional["StorageTransferJobReplicationSpecGcsDataSink"]:
        '''gcs_data_sink block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#gcs_data_sink StorageTransferJob#gcs_data_sink}
        '''
        result = self._values.get("gcs_data_sink")
        return typing.cast(typing.Optional["StorageTransferJobReplicationSpecGcsDataSink"], result)

    @builtins.property
    def gcs_data_source(
        self,
    ) -> typing.Optional["StorageTransferJobReplicationSpecGcsDataSource"]:
        '''gcs_data_source block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#gcs_data_source StorageTransferJob#gcs_data_source}
        '''
        result = self._values.get("gcs_data_source")
        return typing.cast(typing.Optional["StorageTransferJobReplicationSpecGcsDataSource"], result)

    @builtins.property
    def object_conditions(
        self,
    ) -> typing.Optional["StorageTransferJobReplicationSpecObjectConditions"]:
        '''object_conditions block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#object_conditions StorageTransferJob#object_conditions}
        '''
        result = self._values.get("object_conditions")
        return typing.cast(typing.Optional["StorageTransferJobReplicationSpecObjectConditions"], result)

    @builtins.property
    def transfer_options(
        self,
    ) -> typing.Optional["StorageTransferJobReplicationSpecTransferOptions"]:
        '''transfer_options block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#transfer_options StorageTransferJob#transfer_options}
        '''
        result = self._values.get("transfer_options")
        return typing.cast(typing.Optional["StorageTransferJobReplicationSpecTransferOptions"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StorageTransferJobReplicationSpec(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.storageTransferJob.StorageTransferJobReplicationSpecGcsDataSink",
    jsii_struct_bases=[],
    name_mapping={"bucket_name": "bucketName", "path": "path"},
)
class StorageTransferJobReplicationSpecGcsDataSink:
    def __init__(
        self,
        *,
        bucket_name: builtins.str,
        path: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param bucket_name: Google Cloud Storage bucket name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#bucket_name StorageTransferJob#bucket_name}
        :param path: Google Cloud Storage path in bucket to transfer. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#path StorageTransferJob#path}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b54fa5e9047adba5340a7ac5bacf2f9c621971bbe38d5ac3dc3b39d826c3e9d6)
            check_type(argname="argument bucket_name", value=bucket_name, expected_type=type_hints["bucket_name"])
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "bucket_name": bucket_name,
        }
        if path is not None:
            self._values["path"] = path

    @builtins.property
    def bucket_name(self) -> builtins.str:
        '''Google Cloud Storage bucket name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#bucket_name StorageTransferJob#bucket_name}
        '''
        result = self._values.get("bucket_name")
        assert result is not None, "Required property 'bucket_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def path(self) -> typing.Optional[builtins.str]:
        '''Google Cloud Storage path in bucket to transfer.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#path StorageTransferJob#path}
        '''
        result = self._values.get("path")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StorageTransferJobReplicationSpecGcsDataSink(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class StorageTransferJobReplicationSpecGcsDataSinkOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.storageTransferJob.StorageTransferJobReplicationSpecGcsDataSinkOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5a868dbfa8da6cd55df1df6de892a5e688f2ca0b14c5e14c8e494e340157062f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetPath")
    def reset_path(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPath", []))

    @builtins.property
    @jsii.member(jsii_name="bucketNameInput")
    def bucket_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bucketNameInput"))

    @builtins.property
    @jsii.member(jsii_name="pathInput")
    def path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pathInput"))

    @builtins.property
    @jsii.member(jsii_name="bucketName")
    def bucket_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bucketName"))

    @bucket_name.setter
    def bucket_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1cafd87b9b0aa51ed9e4f314b611adb75ee0f31d1a4c02f5bf413505bc6c90ee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bucketName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="path")
    def path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "path"))

    @path.setter
    def path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a1a48eef67e0dbe46ab897b631715f5103801946b6005e13a7290039309693e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "path", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[StorageTransferJobReplicationSpecGcsDataSink]:
        return typing.cast(typing.Optional[StorageTransferJobReplicationSpecGcsDataSink], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[StorageTransferJobReplicationSpecGcsDataSink],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e8d80c335944a31680da659aacfa96b09d43c129e7217904e8c244393abf7b8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.storageTransferJob.StorageTransferJobReplicationSpecGcsDataSource",
    jsii_struct_bases=[],
    name_mapping={"bucket_name": "bucketName", "path": "path"},
)
class StorageTransferJobReplicationSpecGcsDataSource:
    def __init__(
        self,
        *,
        bucket_name: builtins.str,
        path: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param bucket_name: Google Cloud Storage bucket name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#bucket_name StorageTransferJob#bucket_name}
        :param path: Google Cloud Storage path in bucket to transfer. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#path StorageTransferJob#path}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f0aa838cc3ba0129b0e14be75cebb3822f865e325b0bd6cefcdc719c617e2b7b)
            check_type(argname="argument bucket_name", value=bucket_name, expected_type=type_hints["bucket_name"])
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "bucket_name": bucket_name,
        }
        if path is not None:
            self._values["path"] = path

    @builtins.property
    def bucket_name(self) -> builtins.str:
        '''Google Cloud Storage bucket name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#bucket_name StorageTransferJob#bucket_name}
        '''
        result = self._values.get("bucket_name")
        assert result is not None, "Required property 'bucket_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def path(self) -> typing.Optional[builtins.str]:
        '''Google Cloud Storage path in bucket to transfer.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#path StorageTransferJob#path}
        '''
        result = self._values.get("path")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StorageTransferJobReplicationSpecGcsDataSource(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class StorageTransferJobReplicationSpecGcsDataSourceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.storageTransferJob.StorageTransferJobReplicationSpecGcsDataSourceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__012003b9432c9e6f73ccb29ec8d451642c0a4c4b387264fb5adc3f691b3f1e7a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetPath")
    def reset_path(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPath", []))

    @builtins.property
    @jsii.member(jsii_name="bucketNameInput")
    def bucket_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bucketNameInput"))

    @builtins.property
    @jsii.member(jsii_name="pathInput")
    def path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pathInput"))

    @builtins.property
    @jsii.member(jsii_name="bucketName")
    def bucket_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bucketName"))

    @bucket_name.setter
    def bucket_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__489f5f6eceb04adabb057e3558959811d77826b9278449c114d5dad01f1f265f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bucketName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="path")
    def path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "path"))

    @path.setter
    def path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b7042e540acf7671ce097faccdb8d4f14c90be3232a88004e3b93649a11cabe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "path", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[StorageTransferJobReplicationSpecGcsDataSource]:
        return typing.cast(typing.Optional[StorageTransferJobReplicationSpecGcsDataSource], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[StorageTransferJobReplicationSpecGcsDataSource],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8dd9a8b681d4bbc8432614e11fc01a13696e4b81d0783d1fe5aee2274745c488)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.storageTransferJob.StorageTransferJobReplicationSpecObjectConditions",
    jsii_struct_bases=[],
    name_mapping={
        "exclude_prefixes": "excludePrefixes",
        "include_prefixes": "includePrefixes",
        "last_modified_before": "lastModifiedBefore",
        "last_modified_since": "lastModifiedSince",
        "max_time_elapsed_since_last_modification": "maxTimeElapsedSinceLastModification",
        "min_time_elapsed_since_last_modification": "minTimeElapsedSinceLastModification",
    },
)
class StorageTransferJobReplicationSpecObjectConditions:
    def __init__(
        self,
        *,
        exclude_prefixes: typing.Optional[typing.Sequence[builtins.str]] = None,
        include_prefixes: typing.Optional[typing.Sequence[builtins.str]] = None,
        last_modified_before: typing.Optional[builtins.str] = None,
        last_modified_since: typing.Optional[builtins.str] = None,
        max_time_elapsed_since_last_modification: typing.Optional[builtins.str] = None,
        min_time_elapsed_since_last_modification: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param exclude_prefixes: exclude_prefixes must follow the requirements described for include_prefixes. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#exclude_prefixes StorageTransferJob#exclude_prefixes}
        :param include_prefixes: If include_refixes is specified, objects that satisfy the object conditions must have names that start with one of the include_prefixes and that do not start with any of the exclude_prefixes. If include_prefixes is not specified, all objects except those that have names starting with one of the exclude_prefixes must satisfy the object conditions. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#include_prefixes StorageTransferJob#include_prefixes}
        :param last_modified_before: If specified, only objects with a "last modification time" before this timestamp and objects that don't have a "last modification time" are transferred. A timestamp in RFC3339 UTC "Zulu" format, with nanosecond resolution and up to nine fractional digits. Examples: "2014-10-02T15:01:23Z" and "2014-10-02T15:01:23.045123456Z". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#last_modified_before StorageTransferJob#last_modified_before}
        :param last_modified_since: If specified, only objects with a "last modification time" on or after this timestamp and objects that don't have a "last modification time" are transferred. A timestamp in RFC3339 UTC "Zulu" format, with nanosecond resolution and up to nine fractional digits. Examples: "2014-10-02T15:01:23Z" and "2014-10-02T15:01:23.045123456Z". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#last_modified_since StorageTransferJob#last_modified_since}
        :param max_time_elapsed_since_last_modification: A duration in seconds with up to nine fractional digits, terminated by 's'. Example: "3.5s". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#max_time_elapsed_since_last_modification StorageTransferJob#max_time_elapsed_since_last_modification}
        :param min_time_elapsed_since_last_modification: A duration in seconds with up to nine fractional digits, terminated by 's'. Example: "3.5s". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#min_time_elapsed_since_last_modification StorageTransferJob#min_time_elapsed_since_last_modification}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__793be15b9fee1b6718ec6192eee7e6730ea40343cdce13d295edbd6205ef8db9)
            check_type(argname="argument exclude_prefixes", value=exclude_prefixes, expected_type=type_hints["exclude_prefixes"])
            check_type(argname="argument include_prefixes", value=include_prefixes, expected_type=type_hints["include_prefixes"])
            check_type(argname="argument last_modified_before", value=last_modified_before, expected_type=type_hints["last_modified_before"])
            check_type(argname="argument last_modified_since", value=last_modified_since, expected_type=type_hints["last_modified_since"])
            check_type(argname="argument max_time_elapsed_since_last_modification", value=max_time_elapsed_since_last_modification, expected_type=type_hints["max_time_elapsed_since_last_modification"])
            check_type(argname="argument min_time_elapsed_since_last_modification", value=min_time_elapsed_since_last_modification, expected_type=type_hints["min_time_elapsed_since_last_modification"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if exclude_prefixes is not None:
            self._values["exclude_prefixes"] = exclude_prefixes
        if include_prefixes is not None:
            self._values["include_prefixes"] = include_prefixes
        if last_modified_before is not None:
            self._values["last_modified_before"] = last_modified_before
        if last_modified_since is not None:
            self._values["last_modified_since"] = last_modified_since
        if max_time_elapsed_since_last_modification is not None:
            self._values["max_time_elapsed_since_last_modification"] = max_time_elapsed_since_last_modification
        if min_time_elapsed_since_last_modification is not None:
            self._values["min_time_elapsed_since_last_modification"] = min_time_elapsed_since_last_modification

    @builtins.property
    def exclude_prefixes(self) -> typing.Optional[typing.List[builtins.str]]:
        '''exclude_prefixes must follow the requirements described for include_prefixes.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#exclude_prefixes StorageTransferJob#exclude_prefixes}
        '''
        result = self._values.get("exclude_prefixes")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def include_prefixes(self) -> typing.Optional[typing.List[builtins.str]]:
        '''If include_refixes is specified, objects that satisfy the object conditions must have names that start with one of the include_prefixes and that do not start with any of the exclude_prefixes.

        If include_prefixes is not specified, all objects except those that have names starting with one of the exclude_prefixes must satisfy the object conditions.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#include_prefixes StorageTransferJob#include_prefixes}
        '''
        result = self._values.get("include_prefixes")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def last_modified_before(self) -> typing.Optional[builtins.str]:
        '''If specified, only objects with a "last modification time" before this timestamp and objects that don't have a "last modification time" are transferred.

        A timestamp in RFC3339 UTC "Zulu" format, with nanosecond resolution and up to nine fractional digits. Examples: "2014-10-02T15:01:23Z" and "2014-10-02T15:01:23.045123456Z".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#last_modified_before StorageTransferJob#last_modified_before}
        '''
        result = self._values.get("last_modified_before")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def last_modified_since(self) -> typing.Optional[builtins.str]:
        '''If specified, only objects with a "last modification time" on or after this timestamp and objects that don't have a "last modification time" are transferred.

        A timestamp in RFC3339 UTC "Zulu" format, with nanosecond resolution and up to nine fractional digits. Examples: "2014-10-02T15:01:23Z" and "2014-10-02T15:01:23.045123456Z".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#last_modified_since StorageTransferJob#last_modified_since}
        '''
        result = self._values.get("last_modified_since")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def max_time_elapsed_since_last_modification(self) -> typing.Optional[builtins.str]:
        '''A duration in seconds with up to nine fractional digits, terminated by 's'. Example: "3.5s".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#max_time_elapsed_since_last_modification StorageTransferJob#max_time_elapsed_since_last_modification}
        '''
        result = self._values.get("max_time_elapsed_since_last_modification")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def min_time_elapsed_since_last_modification(self) -> typing.Optional[builtins.str]:
        '''A duration in seconds with up to nine fractional digits, terminated by 's'. Example: "3.5s".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#min_time_elapsed_since_last_modification StorageTransferJob#min_time_elapsed_since_last_modification}
        '''
        result = self._values.get("min_time_elapsed_since_last_modification")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StorageTransferJobReplicationSpecObjectConditions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class StorageTransferJobReplicationSpecObjectConditionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.storageTransferJob.StorageTransferJobReplicationSpecObjectConditionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__18dba7a078bea08b9b4b80f49d3507a63c41a6470d2125e799b403726f1a5a6b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetExcludePrefixes")
    def reset_exclude_prefixes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExcludePrefixes", []))

    @jsii.member(jsii_name="resetIncludePrefixes")
    def reset_include_prefixes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIncludePrefixes", []))

    @jsii.member(jsii_name="resetLastModifiedBefore")
    def reset_last_modified_before(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLastModifiedBefore", []))

    @jsii.member(jsii_name="resetLastModifiedSince")
    def reset_last_modified_since(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLastModifiedSince", []))

    @jsii.member(jsii_name="resetMaxTimeElapsedSinceLastModification")
    def reset_max_time_elapsed_since_last_modification(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxTimeElapsedSinceLastModification", []))

    @jsii.member(jsii_name="resetMinTimeElapsedSinceLastModification")
    def reset_min_time_elapsed_since_last_modification(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMinTimeElapsedSinceLastModification", []))

    @builtins.property
    @jsii.member(jsii_name="excludePrefixesInput")
    def exclude_prefixes_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "excludePrefixesInput"))

    @builtins.property
    @jsii.member(jsii_name="includePrefixesInput")
    def include_prefixes_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "includePrefixesInput"))

    @builtins.property
    @jsii.member(jsii_name="lastModifiedBeforeInput")
    def last_modified_before_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "lastModifiedBeforeInput"))

    @builtins.property
    @jsii.member(jsii_name="lastModifiedSinceInput")
    def last_modified_since_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "lastModifiedSinceInput"))

    @builtins.property
    @jsii.member(jsii_name="maxTimeElapsedSinceLastModificationInput")
    def max_time_elapsed_since_last_modification_input(
        self,
    ) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "maxTimeElapsedSinceLastModificationInput"))

    @builtins.property
    @jsii.member(jsii_name="minTimeElapsedSinceLastModificationInput")
    def min_time_elapsed_since_last_modification_input(
        self,
    ) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "minTimeElapsedSinceLastModificationInput"))

    @builtins.property
    @jsii.member(jsii_name="excludePrefixes")
    def exclude_prefixes(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "excludePrefixes"))

    @exclude_prefixes.setter
    def exclude_prefixes(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__633725c421ccea19600c4ad15e2fd291c907949a3f03255cc569b7af5be8d7a0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "excludePrefixes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="includePrefixes")
    def include_prefixes(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "includePrefixes"))

    @include_prefixes.setter
    def include_prefixes(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__552dc747bae4b025e7d5572af5887e719920a25d6a27be04233ea8c128daa6bc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "includePrefixes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="lastModifiedBefore")
    def last_modified_before(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "lastModifiedBefore"))

    @last_modified_before.setter
    def last_modified_before(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b45d5a013279db78b34814e21e2ecdbdcc3a757f55ee9c8c9ee6d8f65d389cd1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "lastModifiedBefore", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="lastModifiedSince")
    def last_modified_since(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "lastModifiedSince"))

    @last_modified_since.setter
    def last_modified_since(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__af757d49a9a57fef24a40e3de2375048bd978bd1270c07c06be6a709a0f5daf4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "lastModifiedSince", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxTimeElapsedSinceLastModification")
    def max_time_elapsed_since_last_modification(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "maxTimeElapsedSinceLastModification"))

    @max_time_elapsed_since_last_modification.setter
    def max_time_elapsed_since_last_modification(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e656c30ab04469a001c1412024e1a0dbd4a36cbaf28bc474ded0fedac2e9b355)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxTimeElapsedSinceLastModification", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="minTimeElapsedSinceLastModification")
    def min_time_elapsed_since_last_modification(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "minTimeElapsedSinceLastModification"))

    @min_time_elapsed_since_last_modification.setter
    def min_time_elapsed_since_last_modification(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d559af2931e28d7cc1056b973630d49546894e03eb671af6720fb1dc576772be)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minTimeElapsedSinceLastModification", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[StorageTransferJobReplicationSpecObjectConditions]:
        return typing.cast(typing.Optional[StorageTransferJobReplicationSpecObjectConditions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[StorageTransferJobReplicationSpecObjectConditions],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7bb9936e05a8dc973d511e03e6ea24362008dc6283bcf05e3fcbfc693d353f79)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class StorageTransferJobReplicationSpecOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.storageTransferJob.StorageTransferJobReplicationSpecOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e03a9ed5177a11c6f48d6673b1adb4b1305747dd5b20784dafc70881e4cea9fe)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putGcsDataSink")
    def put_gcs_data_sink(
        self,
        *,
        bucket_name: builtins.str,
        path: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param bucket_name: Google Cloud Storage bucket name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#bucket_name StorageTransferJob#bucket_name}
        :param path: Google Cloud Storage path in bucket to transfer. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#path StorageTransferJob#path}
        '''
        value = StorageTransferJobReplicationSpecGcsDataSink(
            bucket_name=bucket_name, path=path
        )

        return typing.cast(None, jsii.invoke(self, "putGcsDataSink", [value]))

    @jsii.member(jsii_name="putGcsDataSource")
    def put_gcs_data_source(
        self,
        *,
        bucket_name: builtins.str,
        path: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param bucket_name: Google Cloud Storage bucket name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#bucket_name StorageTransferJob#bucket_name}
        :param path: Google Cloud Storage path in bucket to transfer. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#path StorageTransferJob#path}
        '''
        value = StorageTransferJobReplicationSpecGcsDataSource(
            bucket_name=bucket_name, path=path
        )

        return typing.cast(None, jsii.invoke(self, "putGcsDataSource", [value]))

    @jsii.member(jsii_name="putObjectConditions")
    def put_object_conditions(
        self,
        *,
        exclude_prefixes: typing.Optional[typing.Sequence[builtins.str]] = None,
        include_prefixes: typing.Optional[typing.Sequence[builtins.str]] = None,
        last_modified_before: typing.Optional[builtins.str] = None,
        last_modified_since: typing.Optional[builtins.str] = None,
        max_time_elapsed_since_last_modification: typing.Optional[builtins.str] = None,
        min_time_elapsed_since_last_modification: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param exclude_prefixes: exclude_prefixes must follow the requirements described for include_prefixes. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#exclude_prefixes StorageTransferJob#exclude_prefixes}
        :param include_prefixes: If include_refixes is specified, objects that satisfy the object conditions must have names that start with one of the include_prefixes and that do not start with any of the exclude_prefixes. If include_prefixes is not specified, all objects except those that have names starting with one of the exclude_prefixes must satisfy the object conditions. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#include_prefixes StorageTransferJob#include_prefixes}
        :param last_modified_before: If specified, only objects with a "last modification time" before this timestamp and objects that don't have a "last modification time" are transferred. A timestamp in RFC3339 UTC "Zulu" format, with nanosecond resolution and up to nine fractional digits. Examples: "2014-10-02T15:01:23Z" and "2014-10-02T15:01:23.045123456Z". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#last_modified_before StorageTransferJob#last_modified_before}
        :param last_modified_since: If specified, only objects with a "last modification time" on or after this timestamp and objects that don't have a "last modification time" are transferred. A timestamp in RFC3339 UTC "Zulu" format, with nanosecond resolution and up to nine fractional digits. Examples: "2014-10-02T15:01:23Z" and "2014-10-02T15:01:23.045123456Z". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#last_modified_since StorageTransferJob#last_modified_since}
        :param max_time_elapsed_since_last_modification: A duration in seconds with up to nine fractional digits, terminated by 's'. Example: "3.5s". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#max_time_elapsed_since_last_modification StorageTransferJob#max_time_elapsed_since_last_modification}
        :param min_time_elapsed_since_last_modification: A duration in seconds with up to nine fractional digits, terminated by 's'. Example: "3.5s". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#min_time_elapsed_since_last_modification StorageTransferJob#min_time_elapsed_since_last_modification}
        '''
        value = StorageTransferJobReplicationSpecObjectConditions(
            exclude_prefixes=exclude_prefixes,
            include_prefixes=include_prefixes,
            last_modified_before=last_modified_before,
            last_modified_since=last_modified_since,
            max_time_elapsed_since_last_modification=max_time_elapsed_since_last_modification,
            min_time_elapsed_since_last_modification=min_time_elapsed_since_last_modification,
        )

        return typing.cast(None, jsii.invoke(self, "putObjectConditions", [value]))

    @jsii.member(jsii_name="putTransferOptions")
    def put_transfer_options(
        self,
        *,
        delete_objects_from_source_after_transfer: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        delete_objects_unique_in_sink: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        metadata_options: typing.Optional[typing.Union["StorageTransferJobReplicationSpecTransferOptionsMetadataOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        overwrite_objects_already_existing_in_sink: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        overwrite_when: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param delete_objects_from_source_after_transfer: Whether objects should be deleted from the source after they are transferred to the sink. Note that this option and delete_objects_unique_in_sink are mutually exclusive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#delete_objects_from_source_after_transfer StorageTransferJob#delete_objects_from_source_after_transfer}
        :param delete_objects_unique_in_sink: Whether objects that exist only in the sink should be deleted. Note that this option and delete_objects_from_source_after_transfer are mutually exclusive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#delete_objects_unique_in_sink StorageTransferJob#delete_objects_unique_in_sink}
        :param metadata_options: metadata_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#metadata_options StorageTransferJob#metadata_options}
        :param overwrite_objects_already_existing_in_sink: Whether overwriting objects that already exist in the sink is allowed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#overwrite_objects_already_existing_in_sink StorageTransferJob#overwrite_objects_already_existing_in_sink}
        :param overwrite_when: When to overwrite objects that already exist in the sink. If not set, overwrite behavior is determined by overwriteObjectsAlreadyExistingInSink. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#overwrite_when StorageTransferJob#overwrite_when}
        '''
        value = StorageTransferJobReplicationSpecTransferOptions(
            delete_objects_from_source_after_transfer=delete_objects_from_source_after_transfer,
            delete_objects_unique_in_sink=delete_objects_unique_in_sink,
            metadata_options=metadata_options,
            overwrite_objects_already_existing_in_sink=overwrite_objects_already_existing_in_sink,
            overwrite_when=overwrite_when,
        )

        return typing.cast(None, jsii.invoke(self, "putTransferOptions", [value]))

    @jsii.member(jsii_name="resetGcsDataSink")
    def reset_gcs_data_sink(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGcsDataSink", []))

    @jsii.member(jsii_name="resetGcsDataSource")
    def reset_gcs_data_source(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGcsDataSource", []))

    @jsii.member(jsii_name="resetObjectConditions")
    def reset_object_conditions(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetObjectConditions", []))

    @jsii.member(jsii_name="resetTransferOptions")
    def reset_transfer_options(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTransferOptions", []))

    @builtins.property
    @jsii.member(jsii_name="gcsDataSink")
    def gcs_data_sink(
        self,
    ) -> StorageTransferJobReplicationSpecGcsDataSinkOutputReference:
        return typing.cast(StorageTransferJobReplicationSpecGcsDataSinkOutputReference, jsii.get(self, "gcsDataSink"))

    @builtins.property
    @jsii.member(jsii_name="gcsDataSource")
    def gcs_data_source(
        self,
    ) -> StorageTransferJobReplicationSpecGcsDataSourceOutputReference:
        return typing.cast(StorageTransferJobReplicationSpecGcsDataSourceOutputReference, jsii.get(self, "gcsDataSource"))

    @builtins.property
    @jsii.member(jsii_name="objectConditions")
    def object_conditions(
        self,
    ) -> StorageTransferJobReplicationSpecObjectConditionsOutputReference:
        return typing.cast(StorageTransferJobReplicationSpecObjectConditionsOutputReference, jsii.get(self, "objectConditions"))

    @builtins.property
    @jsii.member(jsii_name="transferOptions")
    def transfer_options(
        self,
    ) -> "StorageTransferJobReplicationSpecTransferOptionsOutputReference":
        return typing.cast("StorageTransferJobReplicationSpecTransferOptionsOutputReference", jsii.get(self, "transferOptions"))

    @builtins.property
    @jsii.member(jsii_name="gcsDataSinkInput")
    def gcs_data_sink_input(
        self,
    ) -> typing.Optional[StorageTransferJobReplicationSpecGcsDataSink]:
        return typing.cast(typing.Optional[StorageTransferJobReplicationSpecGcsDataSink], jsii.get(self, "gcsDataSinkInput"))

    @builtins.property
    @jsii.member(jsii_name="gcsDataSourceInput")
    def gcs_data_source_input(
        self,
    ) -> typing.Optional[StorageTransferJobReplicationSpecGcsDataSource]:
        return typing.cast(typing.Optional[StorageTransferJobReplicationSpecGcsDataSource], jsii.get(self, "gcsDataSourceInput"))

    @builtins.property
    @jsii.member(jsii_name="objectConditionsInput")
    def object_conditions_input(
        self,
    ) -> typing.Optional[StorageTransferJobReplicationSpecObjectConditions]:
        return typing.cast(typing.Optional[StorageTransferJobReplicationSpecObjectConditions], jsii.get(self, "objectConditionsInput"))

    @builtins.property
    @jsii.member(jsii_name="transferOptionsInput")
    def transfer_options_input(
        self,
    ) -> typing.Optional["StorageTransferJobReplicationSpecTransferOptions"]:
        return typing.cast(typing.Optional["StorageTransferJobReplicationSpecTransferOptions"], jsii.get(self, "transferOptionsInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[StorageTransferJobReplicationSpec]:
        return typing.cast(typing.Optional[StorageTransferJobReplicationSpec], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[StorageTransferJobReplicationSpec],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__142d51934a5b8bb3919d14b8e348cf43c8984d6667441fe1c75aff1909dc8b4b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.storageTransferJob.StorageTransferJobReplicationSpecTransferOptions",
    jsii_struct_bases=[],
    name_mapping={
        "delete_objects_from_source_after_transfer": "deleteObjectsFromSourceAfterTransfer",
        "delete_objects_unique_in_sink": "deleteObjectsUniqueInSink",
        "metadata_options": "metadataOptions",
        "overwrite_objects_already_existing_in_sink": "overwriteObjectsAlreadyExistingInSink",
        "overwrite_when": "overwriteWhen",
    },
)
class StorageTransferJobReplicationSpecTransferOptions:
    def __init__(
        self,
        *,
        delete_objects_from_source_after_transfer: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        delete_objects_unique_in_sink: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        metadata_options: typing.Optional[typing.Union["StorageTransferJobReplicationSpecTransferOptionsMetadataOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        overwrite_objects_already_existing_in_sink: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        overwrite_when: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param delete_objects_from_source_after_transfer: Whether objects should be deleted from the source after they are transferred to the sink. Note that this option and delete_objects_unique_in_sink are mutually exclusive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#delete_objects_from_source_after_transfer StorageTransferJob#delete_objects_from_source_after_transfer}
        :param delete_objects_unique_in_sink: Whether objects that exist only in the sink should be deleted. Note that this option and delete_objects_from_source_after_transfer are mutually exclusive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#delete_objects_unique_in_sink StorageTransferJob#delete_objects_unique_in_sink}
        :param metadata_options: metadata_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#metadata_options StorageTransferJob#metadata_options}
        :param overwrite_objects_already_existing_in_sink: Whether overwriting objects that already exist in the sink is allowed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#overwrite_objects_already_existing_in_sink StorageTransferJob#overwrite_objects_already_existing_in_sink}
        :param overwrite_when: When to overwrite objects that already exist in the sink. If not set, overwrite behavior is determined by overwriteObjectsAlreadyExistingInSink. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#overwrite_when StorageTransferJob#overwrite_when}
        '''
        if isinstance(metadata_options, dict):
            metadata_options = StorageTransferJobReplicationSpecTransferOptionsMetadataOptions(**metadata_options)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e8aafd453dc117b43656f594071a0fae9389eeffe6caee7c340e715dea52ed63)
            check_type(argname="argument delete_objects_from_source_after_transfer", value=delete_objects_from_source_after_transfer, expected_type=type_hints["delete_objects_from_source_after_transfer"])
            check_type(argname="argument delete_objects_unique_in_sink", value=delete_objects_unique_in_sink, expected_type=type_hints["delete_objects_unique_in_sink"])
            check_type(argname="argument metadata_options", value=metadata_options, expected_type=type_hints["metadata_options"])
            check_type(argname="argument overwrite_objects_already_existing_in_sink", value=overwrite_objects_already_existing_in_sink, expected_type=type_hints["overwrite_objects_already_existing_in_sink"])
            check_type(argname="argument overwrite_when", value=overwrite_when, expected_type=type_hints["overwrite_when"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if delete_objects_from_source_after_transfer is not None:
            self._values["delete_objects_from_source_after_transfer"] = delete_objects_from_source_after_transfer
        if delete_objects_unique_in_sink is not None:
            self._values["delete_objects_unique_in_sink"] = delete_objects_unique_in_sink
        if metadata_options is not None:
            self._values["metadata_options"] = metadata_options
        if overwrite_objects_already_existing_in_sink is not None:
            self._values["overwrite_objects_already_existing_in_sink"] = overwrite_objects_already_existing_in_sink
        if overwrite_when is not None:
            self._values["overwrite_when"] = overwrite_when

    @builtins.property
    def delete_objects_from_source_after_transfer(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether objects should be deleted from the source after they are transferred to the sink.

        Note that this option and delete_objects_unique_in_sink are mutually exclusive.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#delete_objects_from_source_after_transfer StorageTransferJob#delete_objects_from_source_after_transfer}
        '''
        result = self._values.get("delete_objects_from_source_after_transfer")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def delete_objects_unique_in_sink(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether objects that exist only in the sink should be deleted.

        Note that this option and delete_objects_from_source_after_transfer are mutually exclusive.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#delete_objects_unique_in_sink StorageTransferJob#delete_objects_unique_in_sink}
        '''
        result = self._values.get("delete_objects_unique_in_sink")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def metadata_options(
        self,
    ) -> typing.Optional["StorageTransferJobReplicationSpecTransferOptionsMetadataOptions"]:
        '''metadata_options block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#metadata_options StorageTransferJob#metadata_options}
        '''
        result = self._values.get("metadata_options")
        return typing.cast(typing.Optional["StorageTransferJobReplicationSpecTransferOptionsMetadataOptions"], result)

    @builtins.property
    def overwrite_objects_already_existing_in_sink(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether overwriting objects that already exist in the sink is allowed.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#overwrite_objects_already_existing_in_sink StorageTransferJob#overwrite_objects_already_existing_in_sink}
        '''
        result = self._values.get("overwrite_objects_already_existing_in_sink")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def overwrite_when(self) -> typing.Optional[builtins.str]:
        '''When to overwrite objects that already exist in the sink. If not set, overwrite behavior is determined by overwriteObjectsAlreadyExistingInSink.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#overwrite_when StorageTransferJob#overwrite_when}
        '''
        result = self._values.get("overwrite_when")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StorageTransferJobReplicationSpecTransferOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.storageTransferJob.StorageTransferJobReplicationSpecTransferOptionsMetadataOptions",
    jsii_struct_bases=[],
    name_mapping={
        "acl": "acl",
        "gid": "gid",
        "kms_key": "kmsKey",
        "mode": "mode",
        "storage_class": "storageClass",
        "symlink": "symlink",
        "temporary_hold": "temporaryHold",
        "time_created": "timeCreated",
        "uid": "uid",
    },
)
class StorageTransferJobReplicationSpecTransferOptionsMetadataOptions:
    def __init__(
        self,
        *,
        acl: typing.Optional[builtins.str] = None,
        gid: typing.Optional[builtins.str] = None,
        kms_key: typing.Optional[builtins.str] = None,
        mode: typing.Optional[builtins.str] = None,
        storage_class: typing.Optional[builtins.str] = None,
        symlink: typing.Optional[builtins.str] = None,
        temporary_hold: typing.Optional[builtins.str] = None,
        time_created: typing.Optional[builtins.str] = None,
        uid: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param acl: Specifies how each object's ACLs should be preserved for transfers between Google Cloud Storage buckets. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#acl StorageTransferJob#acl}
        :param gid: Specifies how each file's POSIX group ID (GID) attribute should be handled by the transfer. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#gid StorageTransferJob#gid}
        :param kms_key: Specifies how each object's Cloud KMS customer-managed encryption key (CMEK) is preserved for transfers between Google Cloud Storage buckets. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#kms_key StorageTransferJob#kms_key}
        :param mode: Specifies how each file's mode attribute should be handled by the transfer. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#mode StorageTransferJob#mode}
        :param storage_class: Specifies the storage class to set on objects being transferred to Google Cloud Storage buckets. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#storage_class StorageTransferJob#storage_class}
        :param symlink: Specifies how symlinks should be handled by the transfer. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#symlink StorageTransferJob#symlink}
        :param temporary_hold: SSpecifies how each object's temporary hold status should be preserved for transfers between Google Cloud Storage buckets. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#temporary_hold StorageTransferJob#temporary_hold}
        :param time_created: Specifies how each object's timeCreated metadata is preserved for transfers. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#time_created StorageTransferJob#time_created}
        :param uid: Specifies how each file's POSIX user ID (UID) attribute should be handled by the transfer. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#uid StorageTransferJob#uid}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__130a5b8c681559809fea1ef66632ff905a07c1e957945e9531f96439c6b85bad)
            check_type(argname="argument acl", value=acl, expected_type=type_hints["acl"])
            check_type(argname="argument gid", value=gid, expected_type=type_hints["gid"])
            check_type(argname="argument kms_key", value=kms_key, expected_type=type_hints["kms_key"])
            check_type(argname="argument mode", value=mode, expected_type=type_hints["mode"])
            check_type(argname="argument storage_class", value=storage_class, expected_type=type_hints["storage_class"])
            check_type(argname="argument symlink", value=symlink, expected_type=type_hints["symlink"])
            check_type(argname="argument temporary_hold", value=temporary_hold, expected_type=type_hints["temporary_hold"])
            check_type(argname="argument time_created", value=time_created, expected_type=type_hints["time_created"])
            check_type(argname="argument uid", value=uid, expected_type=type_hints["uid"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if acl is not None:
            self._values["acl"] = acl
        if gid is not None:
            self._values["gid"] = gid
        if kms_key is not None:
            self._values["kms_key"] = kms_key
        if mode is not None:
            self._values["mode"] = mode
        if storage_class is not None:
            self._values["storage_class"] = storage_class
        if symlink is not None:
            self._values["symlink"] = symlink
        if temporary_hold is not None:
            self._values["temporary_hold"] = temporary_hold
        if time_created is not None:
            self._values["time_created"] = time_created
        if uid is not None:
            self._values["uid"] = uid

    @builtins.property
    def acl(self) -> typing.Optional[builtins.str]:
        '''Specifies how each object's ACLs should be preserved for transfers between Google Cloud Storage buckets.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#acl StorageTransferJob#acl}
        '''
        result = self._values.get("acl")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def gid(self) -> typing.Optional[builtins.str]:
        '''Specifies how each file's POSIX group ID (GID) attribute should be handled by the transfer.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#gid StorageTransferJob#gid}
        '''
        result = self._values.get("gid")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kms_key(self) -> typing.Optional[builtins.str]:
        '''Specifies how each object's Cloud KMS customer-managed encryption key (CMEK) is preserved for transfers between Google Cloud Storage buckets.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#kms_key StorageTransferJob#kms_key}
        '''
        result = self._values.get("kms_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def mode(self) -> typing.Optional[builtins.str]:
        '''Specifies how each file's mode attribute should be handled by the transfer.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#mode StorageTransferJob#mode}
        '''
        result = self._values.get("mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def storage_class(self) -> typing.Optional[builtins.str]:
        '''Specifies the storage class to set on objects being transferred to Google Cloud Storage buckets.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#storage_class StorageTransferJob#storage_class}
        '''
        result = self._values.get("storage_class")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def symlink(self) -> typing.Optional[builtins.str]:
        '''Specifies how symlinks should be handled by the transfer.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#symlink StorageTransferJob#symlink}
        '''
        result = self._values.get("symlink")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def temporary_hold(self) -> typing.Optional[builtins.str]:
        '''SSpecifies how each object's temporary hold status should be preserved for transfers between Google Cloud Storage buckets.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#temporary_hold StorageTransferJob#temporary_hold}
        '''
        result = self._values.get("temporary_hold")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def time_created(self) -> typing.Optional[builtins.str]:
        '''Specifies how each object's timeCreated metadata is preserved for transfers.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#time_created StorageTransferJob#time_created}
        '''
        result = self._values.get("time_created")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def uid(self) -> typing.Optional[builtins.str]:
        '''Specifies how each file's POSIX user ID (UID) attribute should be handled by the transfer.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#uid StorageTransferJob#uid}
        '''
        result = self._values.get("uid")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StorageTransferJobReplicationSpecTransferOptionsMetadataOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class StorageTransferJobReplicationSpecTransferOptionsMetadataOptionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.storageTransferJob.StorageTransferJobReplicationSpecTransferOptionsMetadataOptionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__901a15c8cca6347e121102ced1355b91d94f51d4ec0f7637c0e709b037e9ce3c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAcl")
    def reset_acl(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAcl", []))

    @jsii.member(jsii_name="resetGid")
    def reset_gid(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGid", []))

    @jsii.member(jsii_name="resetKmsKey")
    def reset_kms_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKmsKey", []))

    @jsii.member(jsii_name="resetMode")
    def reset_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMode", []))

    @jsii.member(jsii_name="resetStorageClass")
    def reset_storage_class(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStorageClass", []))

    @jsii.member(jsii_name="resetSymlink")
    def reset_symlink(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSymlink", []))

    @jsii.member(jsii_name="resetTemporaryHold")
    def reset_temporary_hold(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTemporaryHold", []))

    @jsii.member(jsii_name="resetTimeCreated")
    def reset_time_created(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeCreated", []))

    @jsii.member(jsii_name="resetUid")
    def reset_uid(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUid", []))

    @builtins.property
    @jsii.member(jsii_name="aclInput")
    def acl_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "aclInput"))

    @builtins.property
    @jsii.member(jsii_name="gidInput")
    def gid_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "gidInput"))

    @builtins.property
    @jsii.member(jsii_name="kmsKeyInput")
    def kms_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "kmsKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="modeInput")
    def mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "modeInput"))

    @builtins.property
    @jsii.member(jsii_name="storageClassInput")
    def storage_class_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "storageClassInput"))

    @builtins.property
    @jsii.member(jsii_name="symlinkInput")
    def symlink_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "symlinkInput"))

    @builtins.property
    @jsii.member(jsii_name="temporaryHoldInput")
    def temporary_hold_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "temporaryHoldInput"))

    @builtins.property
    @jsii.member(jsii_name="timeCreatedInput")
    def time_created_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "timeCreatedInput"))

    @builtins.property
    @jsii.member(jsii_name="uidInput")
    def uid_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "uidInput"))

    @builtins.property
    @jsii.member(jsii_name="acl")
    def acl(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "acl"))

    @acl.setter
    def acl(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a0f3c1aa5abc023228c43761a68d8f3c0070ff03cbd7948806858e628cfb36ff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "acl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="gid")
    def gid(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "gid"))

    @gid.setter
    def gid(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__45454aa9fee575e77f8a0c748e95cfb2debbd69dd6c5b23a2e3834d708b8d91c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "gid", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="kmsKey")
    def kms_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kmsKey"))

    @kms_key.setter
    def kms_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bd2b09a51c3bfa000c04c4297465d19170c0c015b9a43566b1f4f66b1b55c5f9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="mode")
    def mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mode"))

    @mode.setter
    def mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__90ead3cb853d6f4ad3d57a3ba2c22c3757ace7cc1531e6cb51b19349e29afe83)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="storageClass")
    def storage_class(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "storageClass"))

    @storage_class.setter
    def storage_class(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ac41b050e748c9a97ec418e4b8beb61fd9dd625cc4d769bc46969fcd9304076)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "storageClass", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="symlink")
    def symlink(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "symlink"))

    @symlink.setter
    def symlink(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b089e5ceb26a8e5439c04d38ad36051a759e2caf232b5597c00306ab93168a3b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "symlink", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="temporaryHold")
    def temporary_hold(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "temporaryHold"))

    @temporary_hold.setter
    def temporary_hold(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__68e22df7e4a8cccd4ca3847c71299fd3a9258c96ee445340f5eb7fdabe9fb31b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "temporaryHold", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="timeCreated")
    def time_created(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "timeCreated"))

    @time_created.setter
    def time_created(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dab4ad522de4a3bc894523f453db6dc93feeb29dd7c7a1525c61a277ef2ed706)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timeCreated", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="uid")
    def uid(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "uid"))

    @uid.setter
    def uid(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__37ef0e62b6adb096de787e407d0124f0e99c4b0de40cce79f186efc4811e0131)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "uid", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[StorageTransferJobReplicationSpecTransferOptionsMetadataOptions]:
        return typing.cast(typing.Optional[StorageTransferJobReplicationSpecTransferOptionsMetadataOptions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[StorageTransferJobReplicationSpecTransferOptionsMetadataOptions],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e03b70aa1b87dc44e0525e6e809915b38a86578721197cee522169c76bffd2bf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class StorageTransferJobReplicationSpecTransferOptionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.storageTransferJob.StorageTransferJobReplicationSpecTransferOptionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9986d842e538369a6f11a760a6576c9b1443ca501ee1b4654ac82b5ff823591f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putMetadataOptions")
    def put_metadata_options(
        self,
        *,
        acl: typing.Optional[builtins.str] = None,
        gid: typing.Optional[builtins.str] = None,
        kms_key: typing.Optional[builtins.str] = None,
        mode: typing.Optional[builtins.str] = None,
        storage_class: typing.Optional[builtins.str] = None,
        symlink: typing.Optional[builtins.str] = None,
        temporary_hold: typing.Optional[builtins.str] = None,
        time_created: typing.Optional[builtins.str] = None,
        uid: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param acl: Specifies how each object's ACLs should be preserved for transfers between Google Cloud Storage buckets. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#acl StorageTransferJob#acl}
        :param gid: Specifies how each file's POSIX group ID (GID) attribute should be handled by the transfer. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#gid StorageTransferJob#gid}
        :param kms_key: Specifies how each object's Cloud KMS customer-managed encryption key (CMEK) is preserved for transfers between Google Cloud Storage buckets. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#kms_key StorageTransferJob#kms_key}
        :param mode: Specifies how each file's mode attribute should be handled by the transfer. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#mode StorageTransferJob#mode}
        :param storage_class: Specifies the storage class to set on objects being transferred to Google Cloud Storage buckets. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#storage_class StorageTransferJob#storage_class}
        :param symlink: Specifies how symlinks should be handled by the transfer. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#symlink StorageTransferJob#symlink}
        :param temporary_hold: SSpecifies how each object's temporary hold status should be preserved for transfers between Google Cloud Storage buckets. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#temporary_hold StorageTransferJob#temporary_hold}
        :param time_created: Specifies how each object's timeCreated metadata is preserved for transfers. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#time_created StorageTransferJob#time_created}
        :param uid: Specifies how each file's POSIX user ID (UID) attribute should be handled by the transfer. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#uid StorageTransferJob#uid}
        '''
        value = StorageTransferJobReplicationSpecTransferOptionsMetadataOptions(
            acl=acl,
            gid=gid,
            kms_key=kms_key,
            mode=mode,
            storage_class=storage_class,
            symlink=symlink,
            temporary_hold=temporary_hold,
            time_created=time_created,
            uid=uid,
        )

        return typing.cast(None, jsii.invoke(self, "putMetadataOptions", [value]))

    @jsii.member(jsii_name="resetDeleteObjectsFromSourceAfterTransfer")
    def reset_delete_objects_from_source_after_transfer(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDeleteObjectsFromSourceAfterTransfer", []))

    @jsii.member(jsii_name="resetDeleteObjectsUniqueInSink")
    def reset_delete_objects_unique_in_sink(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDeleteObjectsUniqueInSink", []))

    @jsii.member(jsii_name="resetMetadataOptions")
    def reset_metadata_options(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMetadataOptions", []))

    @jsii.member(jsii_name="resetOverwriteObjectsAlreadyExistingInSink")
    def reset_overwrite_objects_already_existing_in_sink(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOverwriteObjectsAlreadyExistingInSink", []))

    @jsii.member(jsii_name="resetOverwriteWhen")
    def reset_overwrite_when(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOverwriteWhen", []))

    @builtins.property
    @jsii.member(jsii_name="metadataOptions")
    def metadata_options(
        self,
    ) -> StorageTransferJobReplicationSpecTransferOptionsMetadataOptionsOutputReference:
        return typing.cast(StorageTransferJobReplicationSpecTransferOptionsMetadataOptionsOutputReference, jsii.get(self, "metadataOptions"))

    @builtins.property
    @jsii.member(jsii_name="deleteObjectsFromSourceAfterTransferInput")
    def delete_objects_from_source_after_transfer_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "deleteObjectsFromSourceAfterTransferInput"))

    @builtins.property
    @jsii.member(jsii_name="deleteObjectsUniqueInSinkInput")
    def delete_objects_unique_in_sink_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "deleteObjectsUniqueInSinkInput"))

    @builtins.property
    @jsii.member(jsii_name="metadataOptionsInput")
    def metadata_options_input(
        self,
    ) -> typing.Optional[StorageTransferJobReplicationSpecTransferOptionsMetadataOptions]:
        return typing.cast(typing.Optional[StorageTransferJobReplicationSpecTransferOptionsMetadataOptions], jsii.get(self, "metadataOptionsInput"))

    @builtins.property
    @jsii.member(jsii_name="overwriteObjectsAlreadyExistingInSinkInput")
    def overwrite_objects_already_existing_in_sink_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "overwriteObjectsAlreadyExistingInSinkInput"))

    @builtins.property
    @jsii.member(jsii_name="overwriteWhenInput")
    def overwrite_when_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "overwriteWhenInput"))

    @builtins.property
    @jsii.member(jsii_name="deleteObjectsFromSourceAfterTransfer")
    def delete_objects_from_source_after_transfer(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "deleteObjectsFromSourceAfterTransfer"))

    @delete_objects_from_source_after_transfer.setter
    def delete_objects_from_source_after_transfer(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__08c8df261c1f1641513937f237cf5da428e48febb8cd9e75bfaf507768c72128)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deleteObjectsFromSourceAfterTransfer", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="deleteObjectsUniqueInSink")
    def delete_objects_unique_in_sink(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "deleteObjectsUniqueInSink"))

    @delete_objects_unique_in_sink.setter
    def delete_objects_unique_in_sink(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__22dc567e4c12d21d4c226e174b02b8d1fc28df37218090a08e34521679ee3467)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deleteObjectsUniqueInSink", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="overwriteObjectsAlreadyExistingInSink")
    def overwrite_objects_already_existing_in_sink(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "overwriteObjectsAlreadyExistingInSink"))

    @overwrite_objects_already_existing_in_sink.setter
    def overwrite_objects_already_existing_in_sink(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__abc6b47a4ad1956aa8c7256fafae00479c97659b6dac792b583cb934c6b39fff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "overwriteObjectsAlreadyExistingInSink", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="overwriteWhen")
    def overwrite_when(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "overwriteWhen"))

    @overwrite_when.setter
    def overwrite_when(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2cdce1a19b4d7ae0e1f84ac9efc8e48b9276d9988fbd4f0f3360b8926184a705)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "overwriteWhen", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[StorageTransferJobReplicationSpecTransferOptions]:
        return typing.cast(typing.Optional[StorageTransferJobReplicationSpecTransferOptions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[StorageTransferJobReplicationSpecTransferOptions],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__80531a138e745d345915baf077d9c428609ba3e9a93739058398b2c180b725fb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.storageTransferJob.StorageTransferJobSchedule",
    jsii_struct_bases=[],
    name_mapping={
        "schedule_start_date": "scheduleStartDate",
        "repeat_interval": "repeatInterval",
        "schedule_end_date": "scheduleEndDate",
        "start_time_of_day": "startTimeOfDay",
    },
)
class StorageTransferJobSchedule:
    def __init__(
        self,
        *,
        schedule_start_date: typing.Union["StorageTransferJobScheduleScheduleStartDate", typing.Dict[builtins.str, typing.Any]],
        repeat_interval: typing.Optional[builtins.str] = None,
        schedule_end_date: typing.Optional[typing.Union["StorageTransferJobScheduleScheduleEndDate", typing.Dict[builtins.str, typing.Any]]] = None,
        start_time_of_day: typing.Optional[typing.Union["StorageTransferJobScheduleStartTimeOfDay", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param schedule_start_date: schedule_start_date block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#schedule_start_date StorageTransferJob#schedule_start_date}
        :param repeat_interval: Interval between the start of each scheduled transfer. If unspecified, the default value is 24 hours. This value may not be less than 1 hour. A duration in seconds with up to nine fractional digits, terminated by 's'. Example: "3.5s". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#repeat_interval StorageTransferJob#repeat_interval}
        :param schedule_end_date: schedule_end_date block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#schedule_end_date StorageTransferJob#schedule_end_date}
        :param start_time_of_day: start_time_of_day block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#start_time_of_day StorageTransferJob#start_time_of_day}
        '''
        if isinstance(schedule_start_date, dict):
            schedule_start_date = StorageTransferJobScheduleScheduleStartDate(**schedule_start_date)
        if isinstance(schedule_end_date, dict):
            schedule_end_date = StorageTransferJobScheduleScheduleEndDate(**schedule_end_date)
        if isinstance(start_time_of_day, dict):
            start_time_of_day = StorageTransferJobScheduleStartTimeOfDay(**start_time_of_day)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__55f63d7886224c7c5beae3376ea76fd9d40a0f79aec94d9e27d5fc05b192484b)
            check_type(argname="argument schedule_start_date", value=schedule_start_date, expected_type=type_hints["schedule_start_date"])
            check_type(argname="argument repeat_interval", value=repeat_interval, expected_type=type_hints["repeat_interval"])
            check_type(argname="argument schedule_end_date", value=schedule_end_date, expected_type=type_hints["schedule_end_date"])
            check_type(argname="argument start_time_of_day", value=start_time_of_day, expected_type=type_hints["start_time_of_day"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "schedule_start_date": schedule_start_date,
        }
        if repeat_interval is not None:
            self._values["repeat_interval"] = repeat_interval
        if schedule_end_date is not None:
            self._values["schedule_end_date"] = schedule_end_date
        if start_time_of_day is not None:
            self._values["start_time_of_day"] = start_time_of_day

    @builtins.property
    def schedule_start_date(self) -> "StorageTransferJobScheduleScheduleStartDate":
        '''schedule_start_date block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#schedule_start_date StorageTransferJob#schedule_start_date}
        '''
        result = self._values.get("schedule_start_date")
        assert result is not None, "Required property 'schedule_start_date' is missing"
        return typing.cast("StorageTransferJobScheduleScheduleStartDate", result)

    @builtins.property
    def repeat_interval(self) -> typing.Optional[builtins.str]:
        '''Interval between the start of each scheduled transfer.

        If unspecified, the default value is 24 hours. This value may not be less than 1 hour. A duration in seconds with up to nine fractional digits, terminated by 's'. Example: "3.5s".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#repeat_interval StorageTransferJob#repeat_interval}
        '''
        result = self._values.get("repeat_interval")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def schedule_end_date(
        self,
    ) -> typing.Optional["StorageTransferJobScheduleScheduleEndDate"]:
        '''schedule_end_date block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#schedule_end_date StorageTransferJob#schedule_end_date}
        '''
        result = self._values.get("schedule_end_date")
        return typing.cast(typing.Optional["StorageTransferJobScheduleScheduleEndDate"], result)

    @builtins.property
    def start_time_of_day(
        self,
    ) -> typing.Optional["StorageTransferJobScheduleStartTimeOfDay"]:
        '''start_time_of_day block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#start_time_of_day StorageTransferJob#start_time_of_day}
        '''
        result = self._values.get("start_time_of_day")
        return typing.cast(typing.Optional["StorageTransferJobScheduleStartTimeOfDay"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StorageTransferJobSchedule(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class StorageTransferJobScheduleOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.storageTransferJob.StorageTransferJobScheduleOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3fe42e68c683edc4298cedff50bd249989056966deb1778da33db489a3bd87fa)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putScheduleEndDate")
    def put_schedule_end_date(
        self,
        *,
        day: jsii.Number,
        month: jsii.Number,
        year: jsii.Number,
    ) -> None:
        '''
        :param day: Day of month. Must be from 1 to 31 and valid for the year and month. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#day StorageTransferJob#day}
        :param month: Month of year. Must be from 1 to 12. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#month StorageTransferJob#month}
        :param year: Year of date. Must be from 1 to 9999. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#year StorageTransferJob#year}
        '''
        value = StorageTransferJobScheduleScheduleEndDate(
            day=day, month=month, year=year
        )

        return typing.cast(None, jsii.invoke(self, "putScheduleEndDate", [value]))

    @jsii.member(jsii_name="putScheduleStartDate")
    def put_schedule_start_date(
        self,
        *,
        day: jsii.Number,
        month: jsii.Number,
        year: jsii.Number,
    ) -> None:
        '''
        :param day: Day of month. Must be from 1 to 31 and valid for the year and month. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#day StorageTransferJob#day}
        :param month: Month of year. Must be from 1 to 12. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#month StorageTransferJob#month}
        :param year: Year of date. Must be from 1 to 9999. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#year StorageTransferJob#year}
        '''
        value = StorageTransferJobScheduleScheduleStartDate(
            day=day, month=month, year=year
        )

        return typing.cast(None, jsii.invoke(self, "putScheduleStartDate", [value]))

    @jsii.member(jsii_name="putStartTimeOfDay")
    def put_start_time_of_day(
        self,
        *,
        hours: jsii.Number,
        minutes: jsii.Number,
        nanos: jsii.Number,
        seconds: jsii.Number,
    ) -> None:
        '''
        :param hours: Hours of day in 24 hour format. Should be from 0 to 23. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#hours StorageTransferJob#hours}
        :param minutes: Minutes of hour of day. Must be from 0 to 59. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#minutes StorageTransferJob#minutes}
        :param nanos: Fractions of seconds in nanoseconds. Must be from 0 to 999,999,999. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#nanos StorageTransferJob#nanos}
        :param seconds: Seconds of minutes of the time. Must normally be from 0 to 59. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#seconds StorageTransferJob#seconds}
        '''
        value = StorageTransferJobScheduleStartTimeOfDay(
            hours=hours, minutes=minutes, nanos=nanos, seconds=seconds
        )

        return typing.cast(None, jsii.invoke(self, "putStartTimeOfDay", [value]))

    @jsii.member(jsii_name="resetRepeatInterval")
    def reset_repeat_interval(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRepeatInterval", []))

    @jsii.member(jsii_name="resetScheduleEndDate")
    def reset_schedule_end_date(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetScheduleEndDate", []))

    @jsii.member(jsii_name="resetStartTimeOfDay")
    def reset_start_time_of_day(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStartTimeOfDay", []))

    @builtins.property
    @jsii.member(jsii_name="scheduleEndDate")
    def schedule_end_date(
        self,
    ) -> "StorageTransferJobScheduleScheduleEndDateOutputReference":
        return typing.cast("StorageTransferJobScheduleScheduleEndDateOutputReference", jsii.get(self, "scheduleEndDate"))

    @builtins.property
    @jsii.member(jsii_name="scheduleStartDate")
    def schedule_start_date(
        self,
    ) -> "StorageTransferJobScheduleScheduleStartDateOutputReference":
        return typing.cast("StorageTransferJobScheduleScheduleStartDateOutputReference", jsii.get(self, "scheduleStartDate"))

    @builtins.property
    @jsii.member(jsii_name="startTimeOfDay")
    def start_time_of_day(
        self,
    ) -> "StorageTransferJobScheduleStartTimeOfDayOutputReference":
        return typing.cast("StorageTransferJobScheduleStartTimeOfDayOutputReference", jsii.get(self, "startTimeOfDay"))

    @builtins.property
    @jsii.member(jsii_name="repeatIntervalInput")
    def repeat_interval_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "repeatIntervalInput"))

    @builtins.property
    @jsii.member(jsii_name="scheduleEndDateInput")
    def schedule_end_date_input(
        self,
    ) -> typing.Optional["StorageTransferJobScheduleScheduleEndDate"]:
        return typing.cast(typing.Optional["StorageTransferJobScheduleScheduleEndDate"], jsii.get(self, "scheduleEndDateInput"))

    @builtins.property
    @jsii.member(jsii_name="scheduleStartDateInput")
    def schedule_start_date_input(
        self,
    ) -> typing.Optional["StorageTransferJobScheduleScheduleStartDate"]:
        return typing.cast(typing.Optional["StorageTransferJobScheduleScheduleStartDate"], jsii.get(self, "scheduleStartDateInput"))

    @builtins.property
    @jsii.member(jsii_name="startTimeOfDayInput")
    def start_time_of_day_input(
        self,
    ) -> typing.Optional["StorageTransferJobScheduleStartTimeOfDay"]:
        return typing.cast(typing.Optional["StorageTransferJobScheduleStartTimeOfDay"], jsii.get(self, "startTimeOfDayInput"))

    @builtins.property
    @jsii.member(jsii_name="repeatInterval")
    def repeat_interval(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "repeatInterval"))

    @repeat_interval.setter
    def repeat_interval(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__311dd224d352e272405cc7ef1b4a9c2d4c7f6467c46deb13ffb9d0c2a17b192e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "repeatInterval", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[StorageTransferJobSchedule]:
        return typing.cast(typing.Optional[StorageTransferJobSchedule], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[StorageTransferJobSchedule],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a9753e4e62939e44b4bfcaf6b9d08a1e388520db855e4fe27df9490892c7cd34)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.storageTransferJob.StorageTransferJobScheduleScheduleEndDate",
    jsii_struct_bases=[],
    name_mapping={"day": "day", "month": "month", "year": "year"},
)
class StorageTransferJobScheduleScheduleEndDate:
    def __init__(
        self,
        *,
        day: jsii.Number,
        month: jsii.Number,
        year: jsii.Number,
    ) -> None:
        '''
        :param day: Day of month. Must be from 1 to 31 and valid for the year and month. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#day StorageTransferJob#day}
        :param month: Month of year. Must be from 1 to 12. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#month StorageTransferJob#month}
        :param year: Year of date. Must be from 1 to 9999. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#year StorageTransferJob#year}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b014353fa247d8249f322677c5c26125ac592047e40540a8ff5616a0c700bcdc)
            check_type(argname="argument day", value=day, expected_type=type_hints["day"])
            check_type(argname="argument month", value=month, expected_type=type_hints["month"])
            check_type(argname="argument year", value=year, expected_type=type_hints["year"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "day": day,
            "month": month,
            "year": year,
        }

    @builtins.property
    def day(self) -> jsii.Number:
        '''Day of month. Must be from 1 to 31 and valid for the year and month.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#day StorageTransferJob#day}
        '''
        result = self._values.get("day")
        assert result is not None, "Required property 'day' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def month(self) -> jsii.Number:
        '''Month of year. Must be from 1 to 12.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#month StorageTransferJob#month}
        '''
        result = self._values.get("month")
        assert result is not None, "Required property 'month' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def year(self) -> jsii.Number:
        '''Year of date. Must be from 1 to 9999.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#year StorageTransferJob#year}
        '''
        result = self._values.get("year")
        assert result is not None, "Required property 'year' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StorageTransferJobScheduleScheduleEndDate(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class StorageTransferJobScheduleScheduleEndDateOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.storageTransferJob.StorageTransferJobScheduleScheduleEndDateOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__32c439158c8eafd04319dfa19143bd6f93717ffdf65286097d98dfddf6db5b9e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="dayInput")
    def day_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "dayInput"))

    @builtins.property
    @jsii.member(jsii_name="monthInput")
    def month_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "monthInput"))

    @builtins.property
    @jsii.member(jsii_name="yearInput")
    def year_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "yearInput"))

    @builtins.property
    @jsii.member(jsii_name="day")
    def day(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "day"))

    @day.setter
    def day(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee51bcbc21ac4ab535e408c6d0525b582a51c5685065c68ecd7f81aa0d91777c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "day", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="month")
    def month(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "month"))

    @month.setter
    def month(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__579b5ca37619e19f1d5fc638a1203cd6f300fa5eb5863c6006fd39be503e7a82)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "month", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="year")
    def year(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "year"))

    @year.setter
    def year(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__63b3b80958fad956ee4f08018bf26d26a3c881ceaee53df817edaa4c3806ba07)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "year", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[StorageTransferJobScheduleScheduleEndDate]:
        return typing.cast(typing.Optional[StorageTransferJobScheduleScheduleEndDate], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[StorageTransferJobScheduleScheduleEndDate],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__676994805373d0d7d149e7ba33b964c468001b8fb32bdee26aada89fb6b8fe9d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.storageTransferJob.StorageTransferJobScheduleScheduleStartDate",
    jsii_struct_bases=[],
    name_mapping={"day": "day", "month": "month", "year": "year"},
)
class StorageTransferJobScheduleScheduleStartDate:
    def __init__(
        self,
        *,
        day: jsii.Number,
        month: jsii.Number,
        year: jsii.Number,
    ) -> None:
        '''
        :param day: Day of month. Must be from 1 to 31 and valid for the year and month. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#day StorageTransferJob#day}
        :param month: Month of year. Must be from 1 to 12. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#month StorageTransferJob#month}
        :param year: Year of date. Must be from 1 to 9999. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#year StorageTransferJob#year}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f5cf825abfa5ce3ffa096e28c3587b41093d998532fc9e6c3066ead43bfad6f4)
            check_type(argname="argument day", value=day, expected_type=type_hints["day"])
            check_type(argname="argument month", value=month, expected_type=type_hints["month"])
            check_type(argname="argument year", value=year, expected_type=type_hints["year"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "day": day,
            "month": month,
            "year": year,
        }

    @builtins.property
    def day(self) -> jsii.Number:
        '''Day of month. Must be from 1 to 31 and valid for the year and month.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#day StorageTransferJob#day}
        '''
        result = self._values.get("day")
        assert result is not None, "Required property 'day' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def month(self) -> jsii.Number:
        '''Month of year. Must be from 1 to 12.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#month StorageTransferJob#month}
        '''
        result = self._values.get("month")
        assert result is not None, "Required property 'month' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def year(self) -> jsii.Number:
        '''Year of date. Must be from 1 to 9999.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#year StorageTransferJob#year}
        '''
        result = self._values.get("year")
        assert result is not None, "Required property 'year' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StorageTransferJobScheduleScheduleStartDate(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class StorageTransferJobScheduleScheduleStartDateOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.storageTransferJob.StorageTransferJobScheduleScheduleStartDateOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__40c7a80e67a54a4a64a62f573a05d53981366fddc2de36459e5a7e0c69b7dc02)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="dayInput")
    def day_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "dayInput"))

    @builtins.property
    @jsii.member(jsii_name="monthInput")
    def month_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "monthInput"))

    @builtins.property
    @jsii.member(jsii_name="yearInput")
    def year_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "yearInput"))

    @builtins.property
    @jsii.member(jsii_name="day")
    def day(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "day"))

    @day.setter
    def day(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b659fd6aa05af8de6beacd1d95db2dd95ad68c159f9109d4269505ac333273a3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "day", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="month")
    def month(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "month"))

    @month.setter
    def month(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__11c17b30246f46d51f1fefef3cb03f4daaaa91bc47eb1e625b2acbb8a90f596e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "month", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="year")
    def year(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "year"))

    @year.setter
    def year(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__372a9cb94cc520993323802c8bce30c1b3f85b0176e8f79f90ddc3cd09ad3599)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "year", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[StorageTransferJobScheduleScheduleStartDate]:
        return typing.cast(typing.Optional[StorageTransferJobScheduleScheduleStartDate], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[StorageTransferJobScheduleScheduleStartDate],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fdbb25cc510d24ab7df919827765b6f4b9e177d0654f896efa10cde1ff8b030d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.storageTransferJob.StorageTransferJobScheduleStartTimeOfDay",
    jsii_struct_bases=[],
    name_mapping={
        "hours": "hours",
        "minutes": "minutes",
        "nanos": "nanos",
        "seconds": "seconds",
    },
)
class StorageTransferJobScheduleStartTimeOfDay:
    def __init__(
        self,
        *,
        hours: jsii.Number,
        minutes: jsii.Number,
        nanos: jsii.Number,
        seconds: jsii.Number,
    ) -> None:
        '''
        :param hours: Hours of day in 24 hour format. Should be from 0 to 23. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#hours StorageTransferJob#hours}
        :param minutes: Minutes of hour of day. Must be from 0 to 59. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#minutes StorageTransferJob#minutes}
        :param nanos: Fractions of seconds in nanoseconds. Must be from 0 to 999,999,999. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#nanos StorageTransferJob#nanos}
        :param seconds: Seconds of minutes of the time. Must normally be from 0 to 59. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#seconds StorageTransferJob#seconds}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__059cd2d958dec2e4894561178446d0f7c4c4ec860e40f4ad2f4f4e21feacb6e3)
            check_type(argname="argument hours", value=hours, expected_type=type_hints["hours"])
            check_type(argname="argument minutes", value=minutes, expected_type=type_hints["minutes"])
            check_type(argname="argument nanos", value=nanos, expected_type=type_hints["nanos"])
            check_type(argname="argument seconds", value=seconds, expected_type=type_hints["seconds"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "hours": hours,
            "minutes": minutes,
            "nanos": nanos,
            "seconds": seconds,
        }

    @builtins.property
    def hours(self) -> jsii.Number:
        '''Hours of day in 24 hour format. Should be from 0 to 23.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#hours StorageTransferJob#hours}
        '''
        result = self._values.get("hours")
        assert result is not None, "Required property 'hours' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def minutes(self) -> jsii.Number:
        '''Minutes of hour of day. Must be from 0 to 59.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#minutes StorageTransferJob#minutes}
        '''
        result = self._values.get("minutes")
        assert result is not None, "Required property 'minutes' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def nanos(self) -> jsii.Number:
        '''Fractions of seconds in nanoseconds. Must be from 0 to 999,999,999.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#nanos StorageTransferJob#nanos}
        '''
        result = self._values.get("nanos")
        assert result is not None, "Required property 'nanos' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def seconds(self) -> jsii.Number:
        '''Seconds of minutes of the time. Must normally be from 0 to 59.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#seconds StorageTransferJob#seconds}
        '''
        result = self._values.get("seconds")
        assert result is not None, "Required property 'seconds' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StorageTransferJobScheduleStartTimeOfDay(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class StorageTransferJobScheduleStartTimeOfDayOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.storageTransferJob.StorageTransferJobScheduleStartTimeOfDayOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d738e598a916dd592967b641458d371523beee596e999bd9e528c3c97f0730eb)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="hoursInput")
    def hours_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "hoursInput"))

    @builtins.property
    @jsii.member(jsii_name="minutesInput")
    def minutes_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "minutesInput"))

    @builtins.property
    @jsii.member(jsii_name="nanosInput")
    def nanos_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "nanosInput"))

    @builtins.property
    @jsii.member(jsii_name="secondsInput")
    def seconds_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "secondsInput"))

    @builtins.property
    @jsii.member(jsii_name="hours")
    def hours(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "hours"))

    @hours.setter
    def hours(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__278c7a29da1caffbef5d1f7a0b4dffe312c7feba1fceac2e08357950832ceebc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hours", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="minutes")
    def minutes(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "minutes"))

    @minutes.setter
    def minutes(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c7795f90f2169993008dadc5b451108def1c67ef0423112a425f45dee31dfa36)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minutes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="nanos")
    def nanos(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "nanos"))

    @nanos.setter
    def nanos(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a930101317af07f9c72342e377c373ea1c59dd4bba0a7f948b5e2474e6b7fdb9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nanos", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="seconds")
    def seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "seconds"))

    @seconds.setter
    def seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fba8c13181605b2293ff75cb1835b140ac344133e2ca33acd22820e758059efe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "seconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[StorageTransferJobScheduleStartTimeOfDay]:
        return typing.cast(typing.Optional[StorageTransferJobScheduleStartTimeOfDay], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[StorageTransferJobScheduleStartTimeOfDay],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b39cc734fb9bdab90a79e2eb279cfbeada388b3be97bb9e6a33ee5bd422c0c66)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.storageTransferJob.StorageTransferJobTransferSpec",
    jsii_struct_bases=[],
    name_mapping={
        "aws_s3_data_source": "awsS3DataSource",
        "azure_blob_storage_data_source": "azureBlobStorageDataSource",
        "gcs_data_sink": "gcsDataSink",
        "gcs_data_source": "gcsDataSource",
        "hdfs_data_source": "hdfsDataSource",
        "http_data_source": "httpDataSource",
        "object_conditions": "objectConditions",
        "posix_data_sink": "posixDataSink",
        "posix_data_source": "posixDataSource",
        "sink_agent_pool_name": "sinkAgentPoolName",
        "source_agent_pool_name": "sourceAgentPoolName",
        "transfer_options": "transferOptions",
    },
)
class StorageTransferJobTransferSpec:
    def __init__(
        self,
        *,
        aws_s3_data_source: typing.Optional[typing.Union["StorageTransferJobTransferSpecAwsS3DataSource", typing.Dict[builtins.str, typing.Any]]] = None,
        azure_blob_storage_data_source: typing.Optional[typing.Union["StorageTransferJobTransferSpecAzureBlobStorageDataSource", typing.Dict[builtins.str, typing.Any]]] = None,
        gcs_data_sink: typing.Optional[typing.Union["StorageTransferJobTransferSpecGcsDataSink", typing.Dict[builtins.str, typing.Any]]] = None,
        gcs_data_source: typing.Optional[typing.Union["StorageTransferJobTransferSpecGcsDataSource", typing.Dict[builtins.str, typing.Any]]] = None,
        hdfs_data_source: typing.Optional[typing.Union["StorageTransferJobTransferSpecHdfsDataSource", typing.Dict[builtins.str, typing.Any]]] = None,
        http_data_source: typing.Optional[typing.Union["StorageTransferJobTransferSpecHttpDataSource", typing.Dict[builtins.str, typing.Any]]] = None,
        object_conditions: typing.Optional[typing.Union["StorageTransferJobTransferSpecObjectConditions", typing.Dict[builtins.str, typing.Any]]] = None,
        posix_data_sink: typing.Optional[typing.Union["StorageTransferJobTransferSpecPosixDataSink", typing.Dict[builtins.str, typing.Any]]] = None,
        posix_data_source: typing.Optional[typing.Union["StorageTransferJobTransferSpecPosixDataSource", typing.Dict[builtins.str, typing.Any]]] = None,
        sink_agent_pool_name: typing.Optional[builtins.str] = None,
        source_agent_pool_name: typing.Optional[builtins.str] = None,
        transfer_options: typing.Optional[typing.Union["StorageTransferJobTransferSpecTransferOptions", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param aws_s3_data_source: aws_s3_data_source block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#aws_s3_data_source StorageTransferJob#aws_s3_data_source}
        :param azure_blob_storage_data_source: azure_blob_storage_data_source block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#azure_blob_storage_data_source StorageTransferJob#azure_blob_storage_data_source}
        :param gcs_data_sink: gcs_data_sink block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#gcs_data_sink StorageTransferJob#gcs_data_sink}
        :param gcs_data_source: gcs_data_source block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#gcs_data_source StorageTransferJob#gcs_data_source}
        :param hdfs_data_source: hdfs_data_source block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#hdfs_data_source StorageTransferJob#hdfs_data_source}
        :param http_data_source: http_data_source block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#http_data_source StorageTransferJob#http_data_source}
        :param object_conditions: object_conditions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#object_conditions StorageTransferJob#object_conditions}
        :param posix_data_sink: posix_data_sink block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#posix_data_sink StorageTransferJob#posix_data_sink}
        :param posix_data_source: posix_data_source block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#posix_data_source StorageTransferJob#posix_data_source}
        :param sink_agent_pool_name: Specifies the agent pool name associated with the posix data source. When unspecified, the default name is used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#sink_agent_pool_name StorageTransferJob#sink_agent_pool_name}
        :param source_agent_pool_name: Specifies the agent pool name associated with the posix data source. When unspecified, the default name is used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#source_agent_pool_name StorageTransferJob#source_agent_pool_name}
        :param transfer_options: transfer_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#transfer_options StorageTransferJob#transfer_options}
        '''
        if isinstance(aws_s3_data_source, dict):
            aws_s3_data_source = StorageTransferJobTransferSpecAwsS3DataSource(**aws_s3_data_source)
        if isinstance(azure_blob_storage_data_source, dict):
            azure_blob_storage_data_source = StorageTransferJobTransferSpecAzureBlobStorageDataSource(**azure_blob_storage_data_source)
        if isinstance(gcs_data_sink, dict):
            gcs_data_sink = StorageTransferJobTransferSpecGcsDataSink(**gcs_data_sink)
        if isinstance(gcs_data_source, dict):
            gcs_data_source = StorageTransferJobTransferSpecGcsDataSource(**gcs_data_source)
        if isinstance(hdfs_data_source, dict):
            hdfs_data_source = StorageTransferJobTransferSpecHdfsDataSource(**hdfs_data_source)
        if isinstance(http_data_source, dict):
            http_data_source = StorageTransferJobTransferSpecHttpDataSource(**http_data_source)
        if isinstance(object_conditions, dict):
            object_conditions = StorageTransferJobTransferSpecObjectConditions(**object_conditions)
        if isinstance(posix_data_sink, dict):
            posix_data_sink = StorageTransferJobTransferSpecPosixDataSink(**posix_data_sink)
        if isinstance(posix_data_source, dict):
            posix_data_source = StorageTransferJobTransferSpecPosixDataSource(**posix_data_source)
        if isinstance(transfer_options, dict):
            transfer_options = StorageTransferJobTransferSpecTransferOptions(**transfer_options)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6bbf9b3dd51c8b4ee6e7edc92253208967dad3ece396e6d244cb71486070b418)
            check_type(argname="argument aws_s3_data_source", value=aws_s3_data_source, expected_type=type_hints["aws_s3_data_source"])
            check_type(argname="argument azure_blob_storage_data_source", value=azure_blob_storage_data_source, expected_type=type_hints["azure_blob_storage_data_source"])
            check_type(argname="argument gcs_data_sink", value=gcs_data_sink, expected_type=type_hints["gcs_data_sink"])
            check_type(argname="argument gcs_data_source", value=gcs_data_source, expected_type=type_hints["gcs_data_source"])
            check_type(argname="argument hdfs_data_source", value=hdfs_data_source, expected_type=type_hints["hdfs_data_source"])
            check_type(argname="argument http_data_source", value=http_data_source, expected_type=type_hints["http_data_source"])
            check_type(argname="argument object_conditions", value=object_conditions, expected_type=type_hints["object_conditions"])
            check_type(argname="argument posix_data_sink", value=posix_data_sink, expected_type=type_hints["posix_data_sink"])
            check_type(argname="argument posix_data_source", value=posix_data_source, expected_type=type_hints["posix_data_source"])
            check_type(argname="argument sink_agent_pool_name", value=sink_agent_pool_name, expected_type=type_hints["sink_agent_pool_name"])
            check_type(argname="argument source_agent_pool_name", value=source_agent_pool_name, expected_type=type_hints["source_agent_pool_name"])
            check_type(argname="argument transfer_options", value=transfer_options, expected_type=type_hints["transfer_options"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if aws_s3_data_source is not None:
            self._values["aws_s3_data_source"] = aws_s3_data_source
        if azure_blob_storage_data_source is not None:
            self._values["azure_blob_storage_data_source"] = azure_blob_storage_data_source
        if gcs_data_sink is not None:
            self._values["gcs_data_sink"] = gcs_data_sink
        if gcs_data_source is not None:
            self._values["gcs_data_source"] = gcs_data_source
        if hdfs_data_source is not None:
            self._values["hdfs_data_source"] = hdfs_data_source
        if http_data_source is not None:
            self._values["http_data_source"] = http_data_source
        if object_conditions is not None:
            self._values["object_conditions"] = object_conditions
        if posix_data_sink is not None:
            self._values["posix_data_sink"] = posix_data_sink
        if posix_data_source is not None:
            self._values["posix_data_source"] = posix_data_source
        if sink_agent_pool_name is not None:
            self._values["sink_agent_pool_name"] = sink_agent_pool_name
        if source_agent_pool_name is not None:
            self._values["source_agent_pool_name"] = source_agent_pool_name
        if transfer_options is not None:
            self._values["transfer_options"] = transfer_options

    @builtins.property
    def aws_s3_data_source(
        self,
    ) -> typing.Optional["StorageTransferJobTransferSpecAwsS3DataSource"]:
        '''aws_s3_data_source block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#aws_s3_data_source StorageTransferJob#aws_s3_data_source}
        '''
        result = self._values.get("aws_s3_data_source")
        return typing.cast(typing.Optional["StorageTransferJobTransferSpecAwsS3DataSource"], result)

    @builtins.property
    def azure_blob_storage_data_source(
        self,
    ) -> typing.Optional["StorageTransferJobTransferSpecAzureBlobStorageDataSource"]:
        '''azure_blob_storage_data_source block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#azure_blob_storage_data_source StorageTransferJob#azure_blob_storage_data_source}
        '''
        result = self._values.get("azure_blob_storage_data_source")
        return typing.cast(typing.Optional["StorageTransferJobTransferSpecAzureBlobStorageDataSource"], result)

    @builtins.property
    def gcs_data_sink(
        self,
    ) -> typing.Optional["StorageTransferJobTransferSpecGcsDataSink"]:
        '''gcs_data_sink block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#gcs_data_sink StorageTransferJob#gcs_data_sink}
        '''
        result = self._values.get("gcs_data_sink")
        return typing.cast(typing.Optional["StorageTransferJobTransferSpecGcsDataSink"], result)

    @builtins.property
    def gcs_data_source(
        self,
    ) -> typing.Optional["StorageTransferJobTransferSpecGcsDataSource"]:
        '''gcs_data_source block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#gcs_data_source StorageTransferJob#gcs_data_source}
        '''
        result = self._values.get("gcs_data_source")
        return typing.cast(typing.Optional["StorageTransferJobTransferSpecGcsDataSource"], result)

    @builtins.property
    def hdfs_data_source(
        self,
    ) -> typing.Optional["StorageTransferJobTransferSpecHdfsDataSource"]:
        '''hdfs_data_source block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#hdfs_data_source StorageTransferJob#hdfs_data_source}
        '''
        result = self._values.get("hdfs_data_source")
        return typing.cast(typing.Optional["StorageTransferJobTransferSpecHdfsDataSource"], result)

    @builtins.property
    def http_data_source(
        self,
    ) -> typing.Optional["StorageTransferJobTransferSpecHttpDataSource"]:
        '''http_data_source block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#http_data_source StorageTransferJob#http_data_source}
        '''
        result = self._values.get("http_data_source")
        return typing.cast(typing.Optional["StorageTransferJobTransferSpecHttpDataSource"], result)

    @builtins.property
    def object_conditions(
        self,
    ) -> typing.Optional["StorageTransferJobTransferSpecObjectConditions"]:
        '''object_conditions block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#object_conditions StorageTransferJob#object_conditions}
        '''
        result = self._values.get("object_conditions")
        return typing.cast(typing.Optional["StorageTransferJobTransferSpecObjectConditions"], result)

    @builtins.property
    def posix_data_sink(
        self,
    ) -> typing.Optional["StorageTransferJobTransferSpecPosixDataSink"]:
        '''posix_data_sink block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#posix_data_sink StorageTransferJob#posix_data_sink}
        '''
        result = self._values.get("posix_data_sink")
        return typing.cast(typing.Optional["StorageTransferJobTransferSpecPosixDataSink"], result)

    @builtins.property
    def posix_data_source(
        self,
    ) -> typing.Optional["StorageTransferJobTransferSpecPosixDataSource"]:
        '''posix_data_source block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#posix_data_source StorageTransferJob#posix_data_source}
        '''
        result = self._values.get("posix_data_source")
        return typing.cast(typing.Optional["StorageTransferJobTransferSpecPosixDataSource"], result)

    @builtins.property
    def sink_agent_pool_name(self) -> typing.Optional[builtins.str]:
        '''Specifies the agent pool name associated with the posix data source. When unspecified, the default name is used.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#sink_agent_pool_name StorageTransferJob#sink_agent_pool_name}
        '''
        result = self._values.get("sink_agent_pool_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def source_agent_pool_name(self) -> typing.Optional[builtins.str]:
        '''Specifies the agent pool name associated with the posix data source. When unspecified, the default name is used.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#source_agent_pool_name StorageTransferJob#source_agent_pool_name}
        '''
        result = self._values.get("source_agent_pool_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def transfer_options(
        self,
    ) -> typing.Optional["StorageTransferJobTransferSpecTransferOptions"]:
        '''transfer_options block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#transfer_options StorageTransferJob#transfer_options}
        '''
        result = self._values.get("transfer_options")
        return typing.cast(typing.Optional["StorageTransferJobTransferSpecTransferOptions"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StorageTransferJobTransferSpec(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.storageTransferJob.StorageTransferJobTransferSpecAwsS3DataSource",
    jsii_struct_bases=[],
    name_mapping={
        "bucket_name": "bucketName",
        "aws_access_key": "awsAccessKey",
        "managed_private_network": "managedPrivateNetwork",
        "path": "path",
        "role_arn": "roleArn",
    },
)
class StorageTransferJobTransferSpecAwsS3DataSource:
    def __init__(
        self,
        *,
        bucket_name: builtins.str,
        aws_access_key: typing.Optional[typing.Union["StorageTransferJobTransferSpecAwsS3DataSourceAwsAccessKey", typing.Dict[builtins.str, typing.Any]]] = None,
        managed_private_network: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        path: typing.Optional[builtins.str] = None,
        role_arn: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param bucket_name: S3 Bucket name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#bucket_name StorageTransferJob#bucket_name}
        :param aws_access_key: aws_access_key block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#aws_access_key StorageTransferJob#aws_access_key}
        :param managed_private_network: Egress bytes over a Google-managed private network. This network is shared between other users of Storage Transfer Service. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#managed_private_network StorageTransferJob#managed_private_network}
        :param path: S3 Bucket path in bucket to transfer. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#path StorageTransferJob#path}
        :param role_arn: The Amazon Resource Name (ARN) of the role to support temporary credentials via 'AssumeRoleWithWebIdentity'. For more information about ARNs, see `IAM ARNs <https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_identifiers.html#identifiers-arns>`_. When a role ARN is provided, Transfer Service fetches temporary credentials for the session using a 'AssumeRoleWithWebIdentity' call for the provided role using the [GoogleServiceAccount][] for this project. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#role_arn StorageTransferJob#role_arn}
        '''
        if isinstance(aws_access_key, dict):
            aws_access_key = StorageTransferJobTransferSpecAwsS3DataSourceAwsAccessKey(**aws_access_key)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d93ddf36043d9da4ccee494c94a40fca3bf1a740c3b4342643b2c68576375b14)
            check_type(argname="argument bucket_name", value=bucket_name, expected_type=type_hints["bucket_name"])
            check_type(argname="argument aws_access_key", value=aws_access_key, expected_type=type_hints["aws_access_key"])
            check_type(argname="argument managed_private_network", value=managed_private_network, expected_type=type_hints["managed_private_network"])
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
            check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "bucket_name": bucket_name,
        }
        if aws_access_key is not None:
            self._values["aws_access_key"] = aws_access_key
        if managed_private_network is not None:
            self._values["managed_private_network"] = managed_private_network
        if path is not None:
            self._values["path"] = path
        if role_arn is not None:
            self._values["role_arn"] = role_arn

    @builtins.property
    def bucket_name(self) -> builtins.str:
        '''S3 Bucket name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#bucket_name StorageTransferJob#bucket_name}
        '''
        result = self._values.get("bucket_name")
        assert result is not None, "Required property 'bucket_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def aws_access_key(
        self,
    ) -> typing.Optional["StorageTransferJobTransferSpecAwsS3DataSourceAwsAccessKey"]:
        '''aws_access_key block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#aws_access_key StorageTransferJob#aws_access_key}
        '''
        result = self._values.get("aws_access_key")
        return typing.cast(typing.Optional["StorageTransferJobTransferSpecAwsS3DataSourceAwsAccessKey"], result)

    @builtins.property
    def managed_private_network(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Egress bytes over a Google-managed private network. This network is shared between other users of Storage Transfer Service.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#managed_private_network StorageTransferJob#managed_private_network}
        '''
        result = self._values.get("managed_private_network")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def path(self) -> typing.Optional[builtins.str]:
        '''S3 Bucket path in bucket to transfer.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#path StorageTransferJob#path}
        '''
        result = self._values.get("path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def role_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the role to support temporary credentials via 'AssumeRoleWithWebIdentity'.

        For more information about ARNs, see `IAM ARNs <https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_identifiers.html#identifiers-arns>`_. When a role ARN is provided, Transfer Service fetches temporary credentials for the session using a 'AssumeRoleWithWebIdentity' call for the provided role using the [GoogleServiceAccount][] for this project.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#role_arn StorageTransferJob#role_arn}
        '''
        result = self._values.get("role_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StorageTransferJobTransferSpecAwsS3DataSource(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.storageTransferJob.StorageTransferJobTransferSpecAwsS3DataSourceAwsAccessKey",
    jsii_struct_bases=[],
    name_mapping={
        "access_key_id": "accessKeyId",
        "secret_access_key": "secretAccessKey",
    },
)
class StorageTransferJobTransferSpecAwsS3DataSourceAwsAccessKey:
    def __init__(
        self,
        *,
        access_key_id: builtins.str,
        secret_access_key: builtins.str,
    ) -> None:
        '''
        :param access_key_id: AWS Key ID. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#access_key_id StorageTransferJob#access_key_id}
        :param secret_access_key: AWS Secret Access Key. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#secret_access_key StorageTransferJob#secret_access_key}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d74111a4db2942c3a22c28358392a18696b9ddfb95515d97207631524c4ed27c)
            check_type(argname="argument access_key_id", value=access_key_id, expected_type=type_hints["access_key_id"])
            check_type(argname="argument secret_access_key", value=secret_access_key, expected_type=type_hints["secret_access_key"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "access_key_id": access_key_id,
            "secret_access_key": secret_access_key,
        }

    @builtins.property
    def access_key_id(self) -> builtins.str:
        '''AWS Key ID.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#access_key_id StorageTransferJob#access_key_id}
        '''
        result = self._values.get("access_key_id")
        assert result is not None, "Required property 'access_key_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def secret_access_key(self) -> builtins.str:
        '''AWS Secret Access Key.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#secret_access_key StorageTransferJob#secret_access_key}
        '''
        result = self._values.get("secret_access_key")
        assert result is not None, "Required property 'secret_access_key' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StorageTransferJobTransferSpecAwsS3DataSourceAwsAccessKey(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class StorageTransferJobTransferSpecAwsS3DataSourceAwsAccessKeyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.storageTransferJob.StorageTransferJobTransferSpecAwsS3DataSourceAwsAccessKeyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__008f1c1eb63940e88987b1986ecc5c8c49c253fc6e43be0883938d7ed428a082)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="accessKeyIdInput")
    def access_key_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "accessKeyIdInput"))

    @builtins.property
    @jsii.member(jsii_name="secretAccessKeyInput")
    def secret_access_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "secretAccessKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="accessKeyId")
    def access_key_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "accessKeyId"))

    @access_key_id.setter
    def access_key_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bd6d447626279486282bffe81b0f2da5b82f7c84118683b7f144ab63e994d2f8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accessKeyId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="secretAccessKey")
    def secret_access_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "secretAccessKey"))

    @secret_access_key.setter
    def secret_access_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__510ed705248c1a32d30adedb168bbcf07ed2c3c598b08cbcab335bfffd820d11)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secretAccessKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[StorageTransferJobTransferSpecAwsS3DataSourceAwsAccessKey]:
        return typing.cast(typing.Optional[StorageTransferJobTransferSpecAwsS3DataSourceAwsAccessKey], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[StorageTransferJobTransferSpecAwsS3DataSourceAwsAccessKey],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a2e4bc13b5aa803c1e7fa228f9e26154a6daef1ae25f2971f2dc085b3b03bd45)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class StorageTransferJobTransferSpecAwsS3DataSourceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.storageTransferJob.StorageTransferJobTransferSpecAwsS3DataSourceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f51cf5c37cd970d6b9e7d722e4a6a9fe8544f277cc13b81b126399b58b95954d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAwsAccessKey")
    def put_aws_access_key(
        self,
        *,
        access_key_id: builtins.str,
        secret_access_key: builtins.str,
    ) -> None:
        '''
        :param access_key_id: AWS Key ID. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#access_key_id StorageTransferJob#access_key_id}
        :param secret_access_key: AWS Secret Access Key. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#secret_access_key StorageTransferJob#secret_access_key}
        '''
        value = StorageTransferJobTransferSpecAwsS3DataSourceAwsAccessKey(
            access_key_id=access_key_id, secret_access_key=secret_access_key
        )

        return typing.cast(None, jsii.invoke(self, "putAwsAccessKey", [value]))

    @jsii.member(jsii_name="resetAwsAccessKey")
    def reset_aws_access_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAwsAccessKey", []))

    @jsii.member(jsii_name="resetManagedPrivateNetwork")
    def reset_managed_private_network(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetManagedPrivateNetwork", []))

    @jsii.member(jsii_name="resetPath")
    def reset_path(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPath", []))

    @jsii.member(jsii_name="resetRoleArn")
    def reset_role_arn(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRoleArn", []))

    @builtins.property
    @jsii.member(jsii_name="awsAccessKey")
    def aws_access_key(
        self,
    ) -> StorageTransferJobTransferSpecAwsS3DataSourceAwsAccessKeyOutputReference:
        return typing.cast(StorageTransferJobTransferSpecAwsS3DataSourceAwsAccessKeyOutputReference, jsii.get(self, "awsAccessKey"))

    @builtins.property
    @jsii.member(jsii_name="awsAccessKeyInput")
    def aws_access_key_input(
        self,
    ) -> typing.Optional[StorageTransferJobTransferSpecAwsS3DataSourceAwsAccessKey]:
        return typing.cast(typing.Optional[StorageTransferJobTransferSpecAwsS3DataSourceAwsAccessKey], jsii.get(self, "awsAccessKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="bucketNameInput")
    def bucket_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bucketNameInput"))

    @builtins.property
    @jsii.member(jsii_name="managedPrivateNetworkInput")
    def managed_private_network_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "managedPrivateNetworkInput"))

    @builtins.property
    @jsii.member(jsii_name="pathInput")
    def path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pathInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__9dc1f4d61d2da5cb705980781bce6dac09c2237b0a117e6c00f83f3cde6841b1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bucketName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="managedPrivateNetwork")
    def managed_private_network(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "managedPrivateNetwork"))

    @managed_private_network.setter
    def managed_private_network(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__605883f0c7169039cac4d616a8e7821c1ed934fa7a5a2ca00d993d7e33481191)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "managedPrivateNetwork", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="path")
    def path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "path"))

    @path.setter
    def path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4347ea4df73e7f541f836d4d324d3d7b0d0dc1a93e1c3e26d467ae992de7184a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "path", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="roleArn")
    def role_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "roleArn"))

    @role_arn.setter
    def role_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__290d209fdadc4991b9667e5eb1f9f4f163ba94a01959e7dbfac25886a33bd5e5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "roleArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[StorageTransferJobTransferSpecAwsS3DataSource]:
        return typing.cast(typing.Optional[StorageTransferJobTransferSpecAwsS3DataSource], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[StorageTransferJobTransferSpecAwsS3DataSource],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ac1bb0fa3e8f514745057c112825dfdd16105efebb1aa5b3b128a52c2c09f7b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.storageTransferJob.StorageTransferJobTransferSpecAzureBlobStorageDataSource",
    jsii_struct_bases=[],
    name_mapping={
        "azure_credentials": "azureCredentials",
        "container": "container",
        "storage_account": "storageAccount",
        "path": "path",
    },
)
class StorageTransferJobTransferSpecAzureBlobStorageDataSource:
    def __init__(
        self,
        *,
        azure_credentials: typing.Union["StorageTransferJobTransferSpecAzureBlobStorageDataSourceAzureCredentials", typing.Dict[builtins.str, typing.Any]],
        container: builtins.str,
        storage_account: builtins.str,
        path: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param azure_credentials: azure_credentials block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#azure_credentials StorageTransferJob#azure_credentials}
        :param container: The container to transfer from the Azure Storage account. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#container StorageTransferJob#container}
        :param storage_account: The name of the Azure Storage account. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#storage_account StorageTransferJob#storage_account}
        :param path: Root path to transfer objects. Must be an empty string or full path name that ends with a '/'. This field is treated as an object prefix. As such, it should generally not begin with a '/'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#path StorageTransferJob#path}
        '''
        if isinstance(azure_credentials, dict):
            azure_credentials = StorageTransferJobTransferSpecAzureBlobStorageDataSourceAzureCredentials(**azure_credentials)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9631493f405ce52e93d5bfbac85bbcdca6aba46fb07980ace00d3d79d80e5015)
            check_type(argname="argument azure_credentials", value=azure_credentials, expected_type=type_hints["azure_credentials"])
            check_type(argname="argument container", value=container, expected_type=type_hints["container"])
            check_type(argname="argument storage_account", value=storage_account, expected_type=type_hints["storage_account"])
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "azure_credentials": azure_credentials,
            "container": container,
            "storage_account": storage_account,
        }
        if path is not None:
            self._values["path"] = path

    @builtins.property
    def azure_credentials(
        self,
    ) -> "StorageTransferJobTransferSpecAzureBlobStorageDataSourceAzureCredentials":
        '''azure_credentials block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#azure_credentials StorageTransferJob#azure_credentials}
        '''
        result = self._values.get("azure_credentials")
        assert result is not None, "Required property 'azure_credentials' is missing"
        return typing.cast("StorageTransferJobTransferSpecAzureBlobStorageDataSourceAzureCredentials", result)

    @builtins.property
    def container(self) -> builtins.str:
        '''The container to transfer from the Azure Storage account.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#container StorageTransferJob#container}
        '''
        result = self._values.get("container")
        assert result is not None, "Required property 'container' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def storage_account(self) -> builtins.str:
        '''The name of the Azure Storage account.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#storage_account StorageTransferJob#storage_account}
        '''
        result = self._values.get("storage_account")
        assert result is not None, "Required property 'storage_account' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def path(self) -> typing.Optional[builtins.str]:
        '''Root path to transfer objects.

        Must be an empty string or full path name that ends with a '/'. This field is treated as an object prefix. As such, it should generally not begin with a '/'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#path StorageTransferJob#path}
        '''
        result = self._values.get("path")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StorageTransferJobTransferSpecAzureBlobStorageDataSource(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.storageTransferJob.StorageTransferJobTransferSpecAzureBlobStorageDataSourceAzureCredentials",
    jsii_struct_bases=[],
    name_mapping={"sas_token": "sasToken"},
)
class StorageTransferJobTransferSpecAzureBlobStorageDataSourceAzureCredentials:
    def __init__(self, *, sas_token: builtins.str) -> None:
        '''
        :param sas_token: Azure shared access signature. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#sas_token StorageTransferJob#sas_token}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c73d9ef285f21b6688ec1694295dc363c4215809bd13718c091281b82c636b5)
            check_type(argname="argument sas_token", value=sas_token, expected_type=type_hints["sas_token"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "sas_token": sas_token,
        }

    @builtins.property
    def sas_token(self) -> builtins.str:
        '''Azure shared access signature.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#sas_token StorageTransferJob#sas_token}
        '''
        result = self._values.get("sas_token")
        assert result is not None, "Required property 'sas_token' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StorageTransferJobTransferSpecAzureBlobStorageDataSourceAzureCredentials(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class StorageTransferJobTransferSpecAzureBlobStorageDataSourceAzureCredentialsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.storageTransferJob.StorageTransferJobTransferSpecAzureBlobStorageDataSourceAzureCredentialsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__537c2d115473b9853c78b1a6d0beeabb140e013effa7425293ecf8764df169c3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="sasTokenInput")
    def sas_token_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sasTokenInput"))

    @builtins.property
    @jsii.member(jsii_name="sasToken")
    def sas_token(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sasToken"))

    @sas_token.setter
    def sas_token(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2138191a4cc1c56946bb3cada771d1bc1ec71e3e351321744ca8634d48376519)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sasToken", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[StorageTransferJobTransferSpecAzureBlobStorageDataSourceAzureCredentials]:
        return typing.cast(typing.Optional[StorageTransferJobTransferSpecAzureBlobStorageDataSourceAzureCredentials], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[StorageTransferJobTransferSpecAzureBlobStorageDataSourceAzureCredentials],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c7c947af68b79e745500c876c245cb987ba07ebab90b1f9b78d0f91cc67c6339)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class StorageTransferJobTransferSpecAzureBlobStorageDataSourceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.storageTransferJob.StorageTransferJobTransferSpecAzureBlobStorageDataSourceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0bddec689664ade62f15badd02cec60580af32554431ea398cfad777a0f309a4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAzureCredentials")
    def put_azure_credentials(self, *, sas_token: builtins.str) -> None:
        '''
        :param sas_token: Azure shared access signature. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#sas_token StorageTransferJob#sas_token}
        '''
        value = StorageTransferJobTransferSpecAzureBlobStorageDataSourceAzureCredentials(
            sas_token=sas_token
        )

        return typing.cast(None, jsii.invoke(self, "putAzureCredentials", [value]))

    @jsii.member(jsii_name="resetPath")
    def reset_path(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPath", []))

    @builtins.property
    @jsii.member(jsii_name="azureCredentials")
    def azure_credentials(
        self,
    ) -> StorageTransferJobTransferSpecAzureBlobStorageDataSourceAzureCredentialsOutputReference:
        return typing.cast(StorageTransferJobTransferSpecAzureBlobStorageDataSourceAzureCredentialsOutputReference, jsii.get(self, "azureCredentials"))

    @builtins.property
    @jsii.member(jsii_name="azureCredentialsInput")
    def azure_credentials_input(
        self,
    ) -> typing.Optional[StorageTransferJobTransferSpecAzureBlobStorageDataSourceAzureCredentials]:
        return typing.cast(typing.Optional[StorageTransferJobTransferSpecAzureBlobStorageDataSourceAzureCredentials], jsii.get(self, "azureCredentialsInput"))

    @builtins.property
    @jsii.member(jsii_name="containerInput")
    def container_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "containerInput"))

    @builtins.property
    @jsii.member(jsii_name="pathInput")
    def path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pathInput"))

    @builtins.property
    @jsii.member(jsii_name="storageAccountInput")
    def storage_account_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "storageAccountInput"))

    @builtins.property
    @jsii.member(jsii_name="container")
    def container(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "container"))

    @container.setter
    def container(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d577adeede63751c6ee002b02a15839551ae41114a6912aaf380dcf0de6e3a47)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "container", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="path")
    def path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "path"))

    @path.setter
    def path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__15a500bab5f786f47b1e9bee1cdd21ac9df97f66bb20c3e72842e1d747e29e88)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "path", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="storageAccount")
    def storage_account(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "storageAccount"))

    @storage_account.setter
    def storage_account(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__85585828ef1eb148b7639d76f42656771f7572e30ac1b155c83747ab0174e61b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "storageAccount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[StorageTransferJobTransferSpecAzureBlobStorageDataSource]:
        return typing.cast(typing.Optional[StorageTransferJobTransferSpecAzureBlobStorageDataSource], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[StorageTransferJobTransferSpecAzureBlobStorageDataSource],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__847afd8fd4a38fec1eadbee51ca8e4679e8862e387c7fd6cfc496e3c84f063e8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.storageTransferJob.StorageTransferJobTransferSpecGcsDataSink",
    jsii_struct_bases=[],
    name_mapping={"bucket_name": "bucketName", "path": "path"},
)
class StorageTransferJobTransferSpecGcsDataSink:
    def __init__(
        self,
        *,
        bucket_name: builtins.str,
        path: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param bucket_name: Google Cloud Storage bucket name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#bucket_name StorageTransferJob#bucket_name}
        :param path: Google Cloud Storage path in bucket to transfer. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#path StorageTransferJob#path}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__815fda8744fae5b0dc0b2edc7549907abbbb517b4bc1fc2974d71592780ab2dd)
            check_type(argname="argument bucket_name", value=bucket_name, expected_type=type_hints["bucket_name"])
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "bucket_name": bucket_name,
        }
        if path is not None:
            self._values["path"] = path

    @builtins.property
    def bucket_name(self) -> builtins.str:
        '''Google Cloud Storage bucket name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#bucket_name StorageTransferJob#bucket_name}
        '''
        result = self._values.get("bucket_name")
        assert result is not None, "Required property 'bucket_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def path(self) -> typing.Optional[builtins.str]:
        '''Google Cloud Storage path in bucket to transfer.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#path StorageTransferJob#path}
        '''
        result = self._values.get("path")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StorageTransferJobTransferSpecGcsDataSink(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class StorageTransferJobTransferSpecGcsDataSinkOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.storageTransferJob.StorageTransferJobTransferSpecGcsDataSinkOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0db24c451a7c6807743bf0a61b917c78b650cf9410ebda3d021a925050d576a6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetPath")
    def reset_path(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPath", []))

    @builtins.property
    @jsii.member(jsii_name="bucketNameInput")
    def bucket_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bucketNameInput"))

    @builtins.property
    @jsii.member(jsii_name="pathInput")
    def path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pathInput"))

    @builtins.property
    @jsii.member(jsii_name="bucketName")
    def bucket_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bucketName"))

    @bucket_name.setter
    def bucket_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eb022aeb4a48d524ed1fce3cda844764615931ce3c68625aec81fb94d6b6b520)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bucketName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="path")
    def path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "path"))

    @path.setter
    def path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0d5b2e85b33d5561efcbf5c12821d1fec1bd2578614ef8dcfd2cc2c842cab67a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "path", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[StorageTransferJobTransferSpecGcsDataSink]:
        return typing.cast(typing.Optional[StorageTransferJobTransferSpecGcsDataSink], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[StorageTransferJobTransferSpecGcsDataSink],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__36a36bc165274959496ddc17206367ac5bce0b95683ced6da275f9920ef9fb70)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.storageTransferJob.StorageTransferJobTransferSpecGcsDataSource",
    jsii_struct_bases=[],
    name_mapping={"bucket_name": "bucketName", "path": "path"},
)
class StorageTransferJobTransferSpecGcsDataSource:
    def __init__(
        self,
        *,
        bucket_name: builtins.str,
        path: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param bucket_name: Google Cloud Storage bucket name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#bucket_name StorageTransferJob#bucket_name}
        :param path: Google Cloud Storage path in bucket to transfer. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#path StorageTransferJob#path}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__86239c255f9be3bca3e65c311ffc44c2f8dae9a763bd18870ea3eeb77d254bca)
            check_type(argname="argument bucket_name", value=bucket_name, expected_type=type_hints["bucket_name"])
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "bucket_name": bucket_name,
        }
        if path is not None:
            self._values["path"] = path

    @builtins.property
    def bucket_name(self) -> builtins.str:
        '''Google Cloud Storage bucket name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#bucket_name StorageTransferJob#bucket_name}
        '''
        result = self._values.get("bucket_name")
        assert result is not None, "Required property 'bucket_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def path(self) -> typing.Optional[builtins.str]:
        '''Google Cloud Storage path in bucket to transfer.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#path StorageTransferJob#path}
        '''
        result = self._values.get("path")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StorageTransferJobTransferSpecGcsDataSource(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class StorageTransferJobTransferSpecGcsDataSourceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.storageTransferJob.StorageTransferJobTransferSpecGcsDataSourceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__28cd1eed876bb5ce18d7a856a3ae95302c3b6d6e1f40ab9bd4024fd3a8904c90)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetPath")
    def reset_path(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPath", []))

    @builtins.property
    @jsii.member(jsii_name="bucketNameInput")
    def bucket_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bucketNameInput"))

    @builtins.property
    @jsii.member(jsii_name="pathInput")
    def path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pathInput"))

    @builtins.property
    @jsii.member(jsii_name="bucketName")
    def bucket_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bucketName"))

    @bucket_name.setter
    def bucket_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__76ce5152127f587d16544a2ac175f4e982bb63065400f5ddc6c60004d2573fff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bucketName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="path")
    def path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "path"))

    @path.setter
    def path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2417c14cbcfca7afb29f87612b113b47b6636007c6f1c8761cfa06adb3f6c195)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "path", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[StorageTransferJobTransferSpecGcsDataSource]:
        return typing.cast(typing.Optional[StorageTransferJobTransferSpecGcsDataSource], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[StorageTransferJobTransferSpecGcsDataSource],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__168ef1727e8879e5ffbfb5a0057b4f55e674e78b1490866d21e03a12a5fcbc39)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.storageTransferJob.StorageTransferJobTransferSpecHdfsDataSource",
    jsii_struct_bases=[],
    name_mapping={"path": "path"},
)
class StorageTransferJobTransferSpecHdfsDataSource:
    def __init__(self, *, path: builtins.str) -> None:
        '''
        :param path: Directory path to the filesystem. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#path StorageTransferJob#path}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c89d601fc16d1ff8dc15b212f5492a253caf53dbc09ad74e6614b8c22e58a04e)
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "path": path,
        }

    @builtins.property
    def path(self) -> builtins.str:
        '''Directory path to the filesystem.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#path StorageTransferJob#path}
        '''
        result = self._values.get("path")
        assert result is not None, "Required property 'path' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StorageTransferJobTransferSpecHdfsDataSource(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class StorageTransferJobTransferSpecHdfsDataSourceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.storageTransferJob.StorageTransferJobTransferSpecHdfsDataSourceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2c5349d4a88fc3fcc95f0c828d7e5346bb85d9856309a4229098660fd53e6caf)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="pathInput")
    def path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pathInput"))

    @builtins.property
    @jsii.member(jsii_name="path")
    def path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "path"))

    @path.setter
    def path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c2d8c5e9bfd2f13d1760e593d8a219c84f81b223a98f7fecd5a5125747fe8789)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "path", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[StorageTransferJobTransferSpecHdfsDataSource]:
        return typing.cast(typing.Optional[StorageTransferJobTransferSpecHdfsDataSource], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[StorageTransferJobTransferSpecHdfsDataSource],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__47fb3a374d3dd832c941f003587de179563f065982f32195c90fc14b094170ec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.storageTransferJob.StorageTransferJobTransferSpecHttpDataSource",
    jsii_struct_bases=[],
    name_mapping={"list_url": "listUrl"},
)
class StorageTransferJobTransferSpecHttpDataSource:
    def __init__(self, *, list_url: builtins.str) -> None:
        '''
        :param list_url: The URL that points to the file that stores the object list entries. This file must allow public access. Currently, only URLs with HTTP and HTTPS schemes are supported. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#list_url StorageTransferJob#list_url}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2098d774200ad0345b31686e4d7db166d8141faaf12387c218a9087babdfd19b)
            check_type(argname="argument list_url", value=list_url, expected_type=type_hints["list_url"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "list_url": list_url,
        }

    @builtins.property
    def list_url(self) -> builtins.str:
        '''The URL that points to the file that stores the object list entries.

        This file must allow public access. Currently, only URLs with HTTP and HTTPS schemes are supported.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#list_url StorageTransferJob#list_url}
        '''
        result = self._values.get("list_url")
        assert result is not None, "Required property 'list_url' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StorageTransferJobTransferSpecHttpDataSource(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class StorageTransferJobTransferSpecHttpDataSourceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.storageTransferJob.StorageTransferJobTransferSpecHttpDataSourceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5b25b7ebf8ac225f9b1e3b1c942926e7691256c4f25071f9ec6c40b16eeaa122)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="listUrlInput")
    def list_url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "listUrlInput"))

    @builtins.property
    @jsii.member(jsii_name="listUrl")
    def list_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "listUrl"))

    @list_url.setter
    def list_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eae53a10506eac7a94ad96edbe8e3dc8497611488f254b76523a66404b8eac8d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "listUrl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[StorageTransferJobTransferSpecHttpDataSource]:
        return typing.cast(typing.Optional[StorageTransferJobTransferSpecHttpDataSource], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[StorageTransferJobTransferSpecHttpDataSource],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__125bf4b1ee8c31afce7dabb178cd0dde980c45a955583fc111af99768748367c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.storageTransferJob.StorageTransferJobTransferSpecObjectConditions",
    jsii_struct_bases=[],
    name_mapping={
        "exclude_prefixes": "excludePrefixes",
        "include_prefixes": "includePrefixes",
        "last_modified_before": "lastModifiedBefore",
        "last_modified_since": "lastModifiedSince",
        "max_time_elapsed_since_last_modification": "maxTimeElapsedSinceLastModification",
        "min_time_elapsed_since_last_modification": "minTimeElapsedSinceLastModification",
    },
)
class StorageTransferJobTransferSpecObjectConditions:
    def __init__(
        self,
        *,
        exclude_prefixes: typing.Optional[typing.Sequence[builtins.str]] = None,
        include_prefixes: typing.Optional[typing.Sequence[builtins.str]] = None,
        last_modified_before: typing.Optional[builtins.str] = None,
        last_modified_since: typing.Optional[builtins.str] = None,
        max_time_elapsed_since_last_modification: typing.Optional[builtins.str] = None,
        min_time_elapsed_since_last_modification: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param exclude_prefixes: exclude_prefixes must follow the requirements described for include_prefixes. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#exclude_prefixes StorageTransferJob#exclude_prefixes}
        :param include_prefixes: If include_refixes is specified, objects that satisfy the object conditions must have names that start with one of the include_prefixes and that do not start with any of the exclude_prefixes. If include_prefixes is not specified, all objects except those that have names starting with one of the exclude_prefixes must satisfy the object conditions. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#include_prefixes StorageTransferJob#include_prefixes}
        :param last_modified_before: If specified, only objects with a "last modification time" before this timestamp and objects that don't have a "last modification time" are transferred. A timestamp in RFC3339 UTC "Zulu" format, with nanosecond resolution and up to nine fractional digits. Examples: "2014-10-02T15:01:23Z" and "2014-10-02T15:01:23.045123456Z". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#last_modified_before StorageTransferJob#last_modified_before}
        :param last_modified_since: If specified, only objects with a "last modification time" on or after this timestamp and objects that don't have a "last modification time" are transferred. A timestamp in RFC3339 UTC "Zulu" format, with nanosecond resolution and up to nine fractional digits. Examples: "2014-10-02T15:01:23Z" and "2014-10-02T15:01:23.045123456Z". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#last_modified_since StorageTransferJob#last_modified_since}
        :param max_time_elapsed_since_last_modification: A duration in seconds with up to nine fractional digits, terminated by 's'. Example: "3.5s". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#max_time_elapsed_since_last_modification StorageTransferJob#max_time_elapsed_since_last_modification}
        :param min_time_elapsed_since_last_modification: A duration in seconds with up to nine fractional digits, terminated by 's'. Example: "3.5s". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#min_time_elapsed_since_last_modification StorageTransferJob#min_time_elapsed_since_last_modification}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__abc345f6867071ad7910365636724e3c70085cbde7732c594c382ed3a0aba63b)
            check_type(argname="argument exclude_prefixes", value=exclude_prefixes, expected_type=type_hints["exclude_prefixes"])
            check_type(argname="argument include_prefixes", value=include_prefixes, expected_type=type_hints["include_prefixes"])
            check_type(argname="argument last_modified_before", value=last_modified_before, expected_type=type_hints["last_modified_before"])
            check_type(argname="argument last_modified_since", value=last_modified_since, expected_type=type_hints["last_modified_since"])
            check_type(argname="argument max_time_elapsed_since_last_modification", value=max_time_elapsed_since_last_modification, expected_type=type_hints["max_time_elapsed_since_last_modification"])
            check_type(argname="argument min_time_elapsed_since_last_modification", value=min_time_elapsed_since_last_modification, expected_type=type_hints["min_time_elapsed_since_last_modification"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if exclude_prefixes is not None:
            self._values["exclude_prefixes"] = exclude_prefixes
        if include_prefixes is not None:
            self._values["include_prefixes"] = include_prefixes
        if last_modified_before is not None:
            self._values["last_modified_before"] = last_modified_before
        if last_modified_since is not None:
            self._values["last_modified_since"] = last_modified_since
        if max_time_elapsed_since_last_modification is not None:
            self._values["max_time_elapsed_since_last_modification"] = max_time_elapsed_since_last_modification
        if min_time_elapsed_since_last_modification is not None:
            self._values["min_time_elapsed_since_last_modification"] = min_time_elapsed_since_last_modification

    @builtins.property
    def exclude_prefixes(self) -> typing.Optional[typing.List[builtins.str]]:
        '''exclude_prefixes must follow the requirements described for include_prefixes.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#exclude_prefixes StorageTransferJob#exclude_prefixes}
        '''
        result = self._values.get("exclude_prefixes")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def include_prefixes(self) -> typing.Optional[typing.List[builtins.str]]:
        '''If include_refixes is specified, objects that satisfy the object conditions must have names that start with one of the include_prefixes and that do not start with any of the exclude_prefixes.

        If include_prefixes is not specified, all objects except those that have names starting with one of the exclude_prefixes must satisfy the object conditions.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#include_prefixes StorageTransferJob#include_prefixes}
        '''
        result = self._values.get("include_prefixes")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def last_modified_before(self) -> typing.Optional[builtins.str]:
        '''If specified, only objects with a "last modification time" before this timestamp and objects that don't have a "last modification time" are transferred.

        A timestamp in RFC3339 UTC "Zulu" format, with nanosecond resolution and up to nine fractional digits. Examples: "2014-10-02T15:01:23Z" and "2014-10-02T15:01:23.045123456Z".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#last_modified_before StorageTransferJob#last_modified_before}
        '''
        result = self._values.get("last_modified_before")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def last_modified_since(self) -> typing.Optional[builtins.str]:
        '''If specified, only objects with a "last modification time" on or after this timestamp and objects that don't have a "last modification time" are transferred.

        A timestamp in RFC3339 UTC "Zulu" format, with nanosecond resolution and up to nine fractional digits. Examples: "2014-10-02T15:01:23Z" and "2014-10-02T15:01:23.045123456Z".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#last_modified_since StorageTransferJob#last_modified_since}
        '''
        result = self._values.get("last_modified_since")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def max_time_elapsed_since_last_modification(self) -> typing.Optional[builtins.str]:
        '''A duration in seconds with up to nine fractional digits, terminated by 's'. Example: "3.5s".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#max_time_elapsed_since_last_modification StorageTransferJob#max_time_elapsed_since_last_modification}
        '''
        result = self._values.get("max_time_elapsed_since_last_modification")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def min_time_elapsed_since_last_modification(self) -> typing.Optional[builtins.str]:
        '''A duration in seconds with up to nine fractional digits, terminated by 's'. Example: "3.5s".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#min_time_elapsed_since_last_modification StorageTransferJob#min_time_elapsed_since_last_modification}
        '''
        result = self._values.get("min_time_elapsed_since_last_modification")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StorageTransferJobTransferSpecObjectConditions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class StorageTransferJobTransferSpecObjectConditionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.storageTransferJob.StorageTransferJobTransferSpecObjectConditionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ed5f4e4be62599b31c22a8508e26b134deaa446e311a9eca33764409ef287329)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetExcludePrefixes")
    def reset_exclude_prefixes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExcludePrefixes", []))

    @jsii.member(jsii_name="resetIncludePrefixes")
    def reset_include_prefixes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIncludePrefixes", []))

    @jsii.member(jsii_name="resetLastModifiedBefore")
    def reset_last_modified_before(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLastModifiedBefore", []))

    @jsii.member(jsii_name="resetLastModifiedSince")
    def reset_last_modified_since(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLastModifiedSince", []))

    @jsii.member(jsii_name="resetMaxTimeElapsedSinceLastModification")
    def reset_max_time_elapsed_since_last_modification(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxTimeElapsedSinceLastModification", []))

    @jsii.member(jsii_name="resetMinTimeElapsedSinceLastModification")
    def reset_min_time_elapsed_since_last_modification(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMinTimeElapsedSinceLastModification", []))

    @builtins.property
    @jsii.member(jsii_name="excludePrefixesInput")
    def exclude_prefixes_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "excludePrefixesInput"))

    @builtins.property
    @jsii.member(jsii_name="includePrefixesInput")
    def include_prefixes_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "includePrefixesInput"))

    @builtins.property
    @jsii.member(jsii_name="lastModifiedBeforeInput")
    def last_modified_before_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "lastModifiedBeforeInput"))

    @builtins.property
    @jsii.member(jsii_name="lastModifiedSinceInput")
    def last_modified_since_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "lastModifiedSinceInput"))

    @builtins.property
    @jsii.member(jsii_name="maxTimeElapsedSinceLastModificationInput")
    def max_time_elapsed_since_last_modification_input(
        self,
    ) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "maxTimeElapsedSinceLastModificationInput"))

    @builtins.property
    @jsii.member(jsii_name="minTimeElapsedSinceLastModificationInput")
    def min_time_elapsed_since_last_modification_input(
        self,
    ) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "minTimeElapsedSinceLastModificationInput"))

    @builtins.property
    @jsii.member(jsii_name="excludePrefixes")
    def exclude_prefixes(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "excludePrefixes"))

    @exclude_prefixes.setter
    def exclude_prefixes(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__37198acc4a279eb626ff4a01f9fab5aadf9a2764aa01900997da848f8ed35c8d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "excludePrefixes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="includePrefixes")
    def include_prefixes(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "includePrefixes"))

    @include_prefixes.setter
    def include_prefixes(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b0c0f68382513c753e9412acaeaf89c3a74dc155de83c45b6c1d262e369e2ff3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "includePrefixes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="lastModifiedBefore")
    def last_modified_before(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "lastModifiedBefore"))

    @last_modified_before.setter
    def last_modified_before(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e169acc93896af2a19832fbfda04cb9f3ad6c7c5dca1b02b34265905aab8c1a5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "lastModifiedBefore", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="lastModifiedSince")
    def last_modified_since(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "lastModifiedSince"))

    @last_modified_since.setter
    def last_modified_since(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a82a1061e301d213a597d155d27b66ab5ef1a407f0d879460590b60e497acdce)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "lastModifiedSince", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxTimeElapsedSinceLastModification")
    def max_time_elapsed_since_last_modification(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "maxTimeElapsedSinceLastModification"))

    @max_time_elapsed_since_last_modification.setter
    def max_time_elapsed_since_last_modification(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f0bdfbe52c2c76cf4b881d7ae232b93b1555ea8af58406c51c7079e39632fda)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxTimeElapsedSinceLastModification", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="minTimeElapsedSinceLastModification")
    def min_time_elapsed_since_last_modification(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "minTimeElapsedSinceLastModification"))

    @min_time_elapsed_since_last_modification.setter
    def min_time_elapsed_since_last_modification(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2eee49c17d5bda25dcb4e2e4feed574ce9c49116642da6a969e14ac3fb4e4aa0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minTimeElapsedSinceLastModification", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[StorageTransferJobTransferSpecObjectConditions]:
        return typing.cast(typing.Optional[StorageTransferJobTransferSpecObjectConditions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[StorageTransferJobTransferSpecObjectConditions],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2303a57990661f2d5543f6a61c14cb8288c46326ac1f30517cb9d8b09a9cca51)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class StorageTransferJobTransferSpecOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.storageTransferJob.StorageTransferJobTransferSpecOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fe7d007dae2fd9574de4c52509234d882253aa863992b2acb456fd886a16cdcb)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAwsS3DataSource")
    def put_aws_s3_data_source(
        self,
        *,
        bucket_name: builtins.str,
        aws_access_key: typing.Optional[typing.Union[StorageTransferJobTransferSpecAwsS3DataSourceAwsAccessKey, typing.Dict[builtins.str, typing.Any]]] = None,
        managed_private_network: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        path: typing.Optional[builtins.str] = None,
        role_arn: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param bucket_name: S3 Bucket name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#bucket_name StorageTransferJob#bucket_name}
        :param aws_access_key: aws_access_key block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#aws_access_key StorageTransferJob#aws_access_key}
        :param managed_private_network: Egress bytes over a Google-managed private network. This network is shared between other users of Storage Transfer Service. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#managed_private_network StorageTransferJob#managed_private_network}
        :param path: S3 Bucket path in bucket to transfer. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#path StorageTransferJob#path}
        :param role_arn: The Amazon Resource Name (ARN) of the role to support temporary credentials via 'AssumeRoleWithWebIdentity'. For more information about ARNs, see `IAM ARNs <https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_identifiers.html#identifiers-arns>`_. When a role ARN is provided, Transfer Service fetches temporary credentials for the session using a 'AssumeRoleWithWebIdentity' call for the provided role using the [GoogleServiceAccount][] for this project. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#role_arn StorageTransferJob#role_arn}
        '''
        value = StorageTransferJobTransferSpecAwsS3DataSource(
            bucket_name=bucket_name,
            aws_access_key=aws_access_key,
            managed_private_network=managed_private_network,
            path=path,
            role_arn=role_arn,
        )

        return typing.cast(None, jsii.invoke(self, "putAwsS3DataSource", [value]))

    @jsii.member(jsii_name="putAzureBlobStorageDataSource")
    def put_azure_blob_storage_data_source(
        self,
        *,
        azure_credentials: typing.Union[StorageTransferJobTransferSpecAzureBlobStorageDataSourceAzureCredentials, typing.Dict[builtins.str, typing.Any]],
        container: builtins.str,
        storage_account: builtins.str,
        path: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param azure_credentials: azure_credentials block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#azure_credentials StorageTransferJob#azure_credentials}
        :param container: The container to transfer from the Azure Storage account. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#container StorageTransferJob#container}
        :param storage_account: The name of the Azure Storage account. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#storage_account StorageTransferJob#storage_account}
        :param path: Root path to transfer objects. Must be an empty string or full path name that ends with a '/'. This field is treated as an object prefix. As such, it should generally not begin with a '/'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#path StorageTransferJob#path}
        '''
        value = StorageTransferJobTransferSpecAzureBlobStorageDataSource(
            azure_credentials=azure_credentials,
            container=container,
            storage_account=storage_account,
            path=path,
        )

        return typing.cast(None, jsii.invoke(self, "putAzureBlobStorageDataSource", [value]))

    @jsii.member(jsii_name="putGcsDataSink")
    def put_gcs_data_sink(
        self,
        *,
        bucket_name: builtins.str,
        path: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param bucket_name: Google Cloud Storage bucket name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#bucket_name StorageTransferJob#bucket_name}
        :param path: Google Cloud Storage path in bucket to transfer. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#path StorageTransferJob#path}
        '''
        value = StorageTransferJobTransferSpecGcsDataSink(
            bucket_name=bucket_name, path=path
        )

        return typing.cast(None, jsii.invoke(self, "putGcsDataSink", [value]))

    @jsii.member(jsii_name="putGcsDataSource")
    def put_gcs_data_source(
        self,
        *,
        bucket_name: builtins.str,
        path: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param bucket_name: Google Cloud Storage bucket name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#bucket_name StorageTransferJob#bucket_name}
        :param path: Google Cloud Storage path in bucket to transfer. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#path StorageTransferJob#path}
        '''
        value = StorageTransferJobTransferSpecGcsDataSource(
            bucket_name=bucket_name, path=path
        )

        return typing.cast(None, jsii.invoke(self, "putGcsDataSource", [value]))

    @jsii.member(jsii_name="putHdfsDataSource")
    def put_hdfs_data_source(self, *, path: builtins.str) -> None:
        '''
        :param path: Directory path to the filesystem. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#path StorageTransferJob#path}
        '''
        value = StorageTransferJobTransferSpecHdfsDataSource(path=path)

        return typing.cast(None, jsii.invoke(self, "putHdfsDataSource", [value]))

    @jsii.member(jsii_name="putHttpDataSource")
    def put_http_data_source(self, *, list_url: builtins.str) -> None:
        '''
        :param list_url: The URL that points to the file that stores the object list entries. This file must allow public access. Currently, only URLs with HTTP and HTTPS schemes are supported. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#list_url StorageTransferJob#list_url}
        '''
        value = StorageTransferJobTransferSpecHttpDataSource(list_url=list_url)

        return typing.cast(None, jsii.invoke(self, "putHttpDataSource", [value]))

    @jsii.member(jsii_name="putObjectConditions")
    def put_object_conditions(
        self,
        *,
        exclude_prefixes: typing.Optional[typing.Sequence[builtins.str]] = None,
        include_prefixes: typing.Optional[typing.Sequence[builtins.str]] = None,
        last_modified_before: typing.Optional[builtins.str] = None,
        last_modified_since: typing.Optional[builtins.str] = None,
        max_time_elapsed_since_last_modification: typing.Optional[builtins.str] = None,
        min_time_elapsed_since_last_modification: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param exclude_prefixes: exclude_prefixes must follow the requirements described for include_prefixes. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#exclude_prefixes StorageTransferJob#exclude_prefixes}
        :param include_prefixes: If include_refixes is specified, objects that satisfy the object conditions must have names that start with one of the include_prefixes and that do not start with any of the exclude_prefixes. If include_prefixes is not specified, all objects except those that have names starting with one of the exclude_prefixes must satisfy the object conditions. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#include_prefixes StorageTransferJob#include_prefixes}
        :param last_modified_before: If specified, only objects with a "last modification time" before this timestamp and objects that don't have a "last modification time" are transferred. A timestamp in RFC3339 UTC "Zulu" format, with nanosecond resolution and up to nine fractional digits. Examples: "2014-10-02T15:01:23Z" and "2014-10-02T15:01:23.045123456Z". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#last_modified_before StorageTransferJob#last_modified_before}
        :param last_modified_since: If specified, only objects with a "last modification time" on or after this timestamp and objects that don't have a "last modification time" are transferred. A timestamp in RFC3339 UTC "Zulu" format, with nanosecond resolution and up to nine fractional digits. Examples: "2014-10-02T15:01:23Z" and "2014-10-02T15:01:23.045123456Z". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#last_modified_since StorageTransferJob#last_modified_since}
        :param max_time_elapsed_since_last_modification: A duration in seconds with up to nine fractional digits, terminated by 's'. Example: "3.5s". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#max_time_elapsed_since_last_modification StorageTransferJob#max_time_elapsed_since_last_modification}
        :param min_time_elapsed_since_last_modification: A duration in seconds with up to nine fractional digits, terminated by 's'. Example: "3.5s". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#min_time_elapsed_since_last_modification StorageTransferJob#min_time_elapsed_since_last_modification}
        '''
        value = StorageTransferJobTransferSpecObjectConditions(
            exclude_prefixes=exclude_prefixes,
            include_prefixes=include_prefixes,
            last_modified_before=last_modified_before,
            last_modified_since=last_modified_since,
            max_time_elapsed_since_last_modification=max_time_elapsed_since_last_modification,
            min_time_elapsed_since_last_modification=min_time_elapsed_since_last_modification,
        )

        return typing.cast(None, jsii.invoke(self, "putObjectConditions", [value]))

    @jsii.member(jsii_name="putPosixDataSink")
    def put_posix_data_sink(self, *, root_directory: builtins.str) -> None:
        '''
        :param root_directory: Root directory path to the filesystem. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#root_directory StorageTransferJob#root_directory}
        '''
        value = StorageTransferJobTransferSpecPosixDataSink(
            root_directory=root_directory
        )

        return typing.cast(None, jsii.invoke(self, "putPosixDataSink", [value]))

    @jsii.member(jsii_name="putPosixDataSource")
    def put_posix_data_source(self, *, root_directory: builtins.str) -> None:
        '''
        :param root_directory: Root directory path to the filesystem. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#root_directory StorageTransferJob#root_directory}
        '''
        value = StorageTransferJobTransferSpecPosixDataSource(
            root_directory=root_directory
        )

        return typing.cast(None, jsii.invoke(self, "putPosixDataSource", [value]))

    @jsii.member(jsii_name="putTransferOptions")
    def put_transfer_options(
        self,
        *,
        delete_objects_from_source_after_transfer: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        delete_objects_unique_in_sink: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        metadata_options: typing.Optional[typing.Union["StorageTransferJobTransferSpecTransferOptionsMetadataOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        overwrite_objects_already_existing_in_sink: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        overwrite_when: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param delete_objects_from_source_after_transfer: Whether objects should be deleted from the source after they are transferred to the sink. Note that this option and delete_objects_unique_in_sink are mutually exclusive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#delete_objects_from_source_after_transfer StorageTransferJob#delete_objects_from_source_after_transfer}
        :param delete_objects_unique_in_sink: Whether objects that exist only in the sink should be deleted. Note that this option and delete_objects_from_source_after_transfer are mutually exclusive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#delete_objects_unique_in_sink StorageTransferJob#delete_objects_unique_in_sink}
        :param metadata_options: metadata_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#metadata_options StorageTransferJob#metadata_options}
        :param overwrite_objects_already_existing_in_sink: Whether overwriting objects that already exist in the sink is allowed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#overwrite_objects_already_existing_in_sink StorageTransferJob#overwrite_objects_already_existing_in_sink}
        :param overwrite_when: When to overwrite objects that already exist in the sink. If not set, overwrite behavior is determined by overwriteObjectsAlreadyExistingInSink. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#overwrite_when StorageTransferJob#overwrite_when}
        '''
        value = StorageTransferJobTransferSpecTransferOptions(
            delete_objects_from_source_after_transfer=delete_objects_from_source_after_transfer,
            delete_objects_unique_in_sink=delete_objects_unique_in_sink,
            metadata_options=metadata_options,
            overwrite_objects_already_existing_in_sink=overwrite_objects_already_existing_in_sink,
            overwrite_when=overwrite_when,
        )

        return typing.cast(None, jsii.invoke(self, "putTransferOptions", [value]))

    @jsii.member(jsii_name="resetAwsS3DataSource")
    def reset_aws_s3_data_source(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAwsS3DataSource", []))

    @jsii.member(jsii_name="resetAzureBlobStorageDataSource")
    def reset_azure_blob_storage_data_source(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAzureBlobStorageDataSource", []))

    @jsii.member(jsii_name="resetGcsDataSink")
    def reset_gcs_data_sink(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGcsDataSink", []))

    @jsii.member(jsii_name="resetGcsDataSource")
    def reset_gcs_data_source(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGcsDataSource", []))

    @jsii.member(jsii_name="resetHdfsDataSource")
    def reset_hdfs_data_source(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHdfsDataSource", []))

    @jsii.member(jsii_name="resetHttpDataSource")
    def reset_http_data_source(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHttpDataSource", []))

    @jsii.member(jsii_name="resetObjectConditions")
    def reset_object_conditions(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetObjectConditions", []))

    @jsii.member(jsii_name="resetPosixDataSink")
    def reset_posix_data_sink(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPosixDataSink", []))

    @jsii.member(jsii_name="resetPosixDataSource")
    def reset_posix_data_source(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPosixDataSource", []))

    @jsii.member(jsii_name="resetSinkAgentPoolName")
    def reset_sink_agent_pool_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSinkAgentPoolName", []))

    @jsii.member(jsii_name="resetSourceAgentPoolName")
    def reset_source_agent_pool_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSourceAgentPoolName", []))

    @jsii.member(jsii_name="resetTransferOptions")
    def reset_transfer_options(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTransferOptions", []))

    @builtins.property
    @jsii.member(jsii_name="awsS3DataSource")
    def aws_s3_data_source(
        self,
    ) -> StorageTransferJobTransferSpecAwsS3DataSourceOutputReference:
        return typing.cast(StorageTransferJobTransferSpecAwsS3DataSourceOutputReference, jsii.get(self, "awsS3DataSource"))

    @builtins.property
    @jsii.member(jsii_name="azureBlobStorageDataSource")
    def azure_blob_storage_data_source(
        self,
    ) -> StorageTransferJobTransferSpecAzureBlobStorageDataSourceOutputReference:
        return typing.cast(StorageTransferJobTransferSpecAzureBlobStorageDataSourceOutputReference, jsii.get(self, "azureBlobStorageDataSource"))

    @builtins.property
    @jsii.member(jsii_name="gcsDataSink")
    def gcs_data_sink(self) -> StorageTransferJobTransferSpecGcsDataSinkOutputReference:
        return typing.cast(StorageTransferJobTransferSpecGcsDataSinkOutputReference, jsii.get(self, "gcsDataSink"))

    @builtins.property
    @jsii.member(jsii_name="gcsDataSource")
    def gcs_data_source(
        self,
    ) -> StorageTransferJobTransferSpecGcsDataSourceOutputReference:
        return typing.cast(StorageTransferJobTransferSpecGcsDataSourceOutputReference, jsii.get(self, "gcsDataSource"))

    @builtins.property
    @jsii.member(jsii_name="hdfsDataSource")
    def hdfs_data_source(
        self,
    ) -> StorageTransferJobTransferSpecHdfsDataSourceOutputReference:
        return typing.cast(StorageTransferJobTransferSpecHdfsDataSourceOutputReference, jsii.get(self, "hdfsDataSource"))

    @builtins.property
    @jsii.member(jsii_name="httpDataSource")
    def http_data_source(
        self,
    ) -> StorageTransferJobTransferSpecHttpDataSourceOutputReference:
        return typing.cast(StorageTransferJobTransferSpecHttpDataSourceOutputReference, jsii.get(self, "httpDataSource"))

    @builtins.property
    @jsii.member(jsii_name="objectConditions")
    def object_conditions(
        self,
    ) -> StorageTransferJobTransferSpecObjectConditionsOutputReference:
        return typing.cast(StorageTransferJobTransferSpecObjectConditionsOutputReference, jsii.get(self, "objectConditions"))

    @builtins.property
    @jsii.member(jsii_name="posixDataSink")
    def posix_data_sink(
        self,
    ) -> "StorageTransferJobTransferSpecPosixDataSinkOutputReference":
        return typing.cast("StorageTransferJobTransferSpecPosixDataSinkOutputReference", jsii.get(self, "posixDataSink"))

    @builtins.property
    @jsii.member(jsii_name="posixDataSource")
    def posix_data_source(
        self,
    ) -> "StorageTransferJobTransferSpecPosixDataSourceOutputReference":
        return typing.cast("StorageTransferJobTransferSpecPosixDataSourceOutputReference", jsii.get(self, "posixDataSource"))

    @builtins.property
    @jsii.member(jsii_name="transferOptions")
    def transfer_options(
        self,
    ) -> "StorageTransferJobTransferSpecTransferOptionsOutputReference":
        return typing.cast("StorageTransferJobTransferSpecTransferOptionsOutputReference", jsii.get(self, "transferOptions"))

    @builtins.property
    @jsii.member(jsii_name="awsS3DataSourceInput")
    def aws_s3_data_source_input(
        self,
    ) -> typing.Optional[StorageTransferJobTransferSpecAwsS3DataSource]:
        return typing.cast(typing.Optional[StorageTransferJobTransferSpecAwsS3DataSource], jsii.get(self, "awsS3DataSourceInput"))

    @builtins.property
    @jsii.member(jsii_name="azureBlobStorageDataSourceInput")
    def azure_blob_storage_data_source_input(
        self,
    ) -> typing.Optional[StorageTransferJobTransferSpecAzureBlobStorageDataSource]:
        return typing.cast(typing.Optional[StorageTransferJobTransferSpecAzureBlobStorageDataSource], jsii.get(self, "azureBlobStorageDataSourceInput"))

    @builtins.property
    @jsii.member(jsii_name="gcsDataSinkInput")
    def gcs_data_sink_input(
        self,
    ) -> typing.Optional[StorageTransferJobTransferSpecGcsDataSink]:
        return typing.cast(typing.Optional[StorageTransferJobTransferSpecGcsDataSink], jsii.get(self, "gcsDataSinkInput"))

    @builtins.property
    @jsii.member(jsii_name="gcsDataSourceInput")
    def gcs_data_source_input(
        self,
    ) -> typing.Optional[StorageTransferJobTransferSpecGcsDataSource]:
        return typing.cast(typing.Optional[StorageTransferJobTransferSpecGcsDataSource], jsii.get(self, "gcsDataSourceInput"))

    @builtins.property
    @jsii.member(jsii_name="hdfsDataSourceInput")
    def hdfs_data_source_input(
        self,
    ) -> typing.Optional[StorageTransferJobTransferSpecHdfsDataSource]:
        return typing.cast(typing.Optional[StorageTransferJobTransferSpecHdfsDataSource], jsii.get(self, "hdfsDataSourceInput"))

    @builtins.property
    @jsii.member(jsii_name="httpDataSourceInput")
    def http_data_source_input(
        self,
    ) -> typing.Optional[StorageTransferJobTransferSpecHttpDataSource]:
        return typing.cast(typing.Optional[StorageTransferJobTransferSpecHttpDataSource], jsii.get(self, "httpDataSourceInput"))

    @builtins.property
    @jsii.member(jsii_name="objectConditionsInput")
    def object_conditions_input(
        self,
    ) -> typing.Optional[StorageTransferJobTransferSpecObjectConditions]:
        return typing.cast(typing.Optional[StorageTransferJobTransferSpecObjectConditions], jsii.get(self, "objectConditionsInput"))

    @builtins.property
    @jsii.member(jsii_name="posixDataSinkInput")
    def posix_data_sink_input(
        self,
    ) -> typing.Optional["StorageTransferJobTransferSpecPosixDataSink"]:
        return typing.cast(typing.Optional["StorageTransferJobTransferSpecPosixDataSink"], jsii.get(self, "posixDataSinkInput"))

    @builtins.property
    @jsii.member(jsii_name="posixDataSourceInput")
    def posix_data_source_input(
        self,
    ) -> typing.Optional["StorageTransferJobTransferSpecPosixDataSource"]:
        return typing.cast(typing.Optional["StorageTransferJobTransferSpecPosixDataSource"], jsii.get(self, "posixDataSourceInput"))

    @builtins.property
    @jsii.member(jsii_name="sinkAgentPoolNameInput")
    def sink_agent_pool_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sinkAgentPoolNameInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceAgentPoolNameInput")
    def source_agent_pool_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sourceAgentPoolNameInput"))

    @builtins.property
    @jsii.member(jsii_name="transferOptionsInput")
    def transfer_options_input(
        self,
    ) -> typing.Optional["StorageTransferJobTransferSpecTransferOptions"]:
        return typing.cast(typing.Optional["StorageTransferJobTransferSpecTransferOptions"], jsii.get(self, "transferOptionsInput"))

    @builtins.property
    @jsii.member(jsii_name="sinkAgentPoolName")
    def sink_agent_pool_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sinkAgentPoolName"))

    @sink_agent_pool_name.setter
    def sink_agent_pool_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0b9ec6e74139e852776fe92e89db967a2bb8bc81d967784df59afa638b31fe27)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sinkAgentPoolName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sourceAgentPoolName")
    def source_agent_pool_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sourceAgentPoolName"))

    @source_agent_pool_name.setter
    def source_agent_pool_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__78e2ce8c9db511301ce32a5dcf0cd45f9b17970247ca8961b179362ce314bf12)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sourceAgentPoolName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[StorageTransferJobTransferSpec]:
        return typing.cast(typing.Optional[StorageTransferJobTransferSpec], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[StorageTransferJobTransferSpec],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eb15d07a2d4744a8b59f9bac46900a8f0865c2810fb24f8f36f31f1fe11f3166)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.storageTransferJob.StorageTransferJobTransferSpecPosixDataSink",
    jsii_struct_bases=[],
    name_mapping={"root_directory": "rootDirectory"},
)
class StorageTransferJobTransferSpecPosixDataSink:
    def __init__(self, *, root_directory: builtins.str) -> None:
        '''
        :param root_directory: Root directory path to the filesystem. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#root_directory StorageTransferJob#root_directory}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__61ba7ff40892bfc17203cf46584d6dd8b4d9199db78bc4b070870741f19378ac)
            check_type(argname="argument root_directory", value=root_directory, expected_type=type_hints["root_directory"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "root_directory": root_directory,
        }

    @builtins.property
    def root_directory(self) -> builtins.str:
        '''Root directory path to the filesystem.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#root_directory StorageTransferJob#root_directory}
        '''
        result = self._values.get("root_directory")
        assert result is not None, "Required property 'root_directory' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StorageTransferJobTransferSpecPosixDataSink(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class StorageTransferJobTransferSpecPosixDataSinkOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.storageTransferJob.StorageTransferJobTransferSpecPosixDataSinkOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7f8bc947a84d04a6e8771c850761cfb25ddb5cbc15dfe36ff5e827366c5b7bcb)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="rootDirectoryInput")
    def root_directory_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "rootDirectoryInput"))

    @builtins.property
    @jsii.member(jsii_name="rootDirectory")
    def root_directory(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "rootDirectory"))

    @root_directory.setter
    def root_directory(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e7235633d6417ef7eef0c1255756cf122d6348c9d96d72b17e051d685c5a5993)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rootDirectory", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[StorageTransferJobTransferSpecPosixDataSink]:
        return typing.cast(typing.Optional[StorageTransferJobTransferSpecPosixDataSink], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[StorageTransferJobTransferSpecPosixDataSink],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__347f8bd6d6a46fa3de77c0398d7b9ef3f0bafb4cdd8eaefc78872ef8cd456c1b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.storageTransferJob.StorageTransferJobTransferSpecPosixDataSource",
    jsii_struct_bases=[],
    name_mapping={"root_directory": "rootDirectory"},
)
class StorageTransferJobTransferSpecPosixDataSource:
    def __init__(self, *, root_directory: builtins.str) -> None:
        '''
        :param root_directory: Root directory path to the filesystem. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#root_directory StorageTransferJob#root_directory}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fb57375009c266bf2e22183a93e97e46c0aa5b3f76293012435114556fa1d2f7)
            check_type(argname="argument root_directory", value=root_directory, expected_type=type_hints["root_directory"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "root_directory": root_directory,
        }

    @builtins.property
    def root_directory(self) -> builtins.str:
        '''Root directory path to the filesystem.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#root_directory StorageTransferJob#root_directory}
        '''
        result = self._values.get("root_directory")
        assert result is not None, "Required property 'root_directory' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StorageTransferJobTransferSpecPosixDataSource(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class StorageTransferJobTransferSpecPosixDataSourceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.storageTransferJob.StorageTransferJobTransferSpecPosixDataSourceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e6ff6254e38587aa26350f21be3e495ede269b0b0450d929a94d4726cabba6e7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="rootDirectoryInput")
    def root_directory_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "rootDirectoryInput"))

    @builtins.property
    @jsii.member(jsii_name="rootDirectory")
    def root_directory(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "rootDirectory"))

    @root_directory.setter
    def root_directory(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__434213e16d3f9e6afbf2466710bab1d0d2c59d8cd397ead4a6776d74c7fd00d0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rootDirectory", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[StorageTransferJobTransferSpecPosixDataSource]:
        return typing.cast(typing.Optional[StorageTransferJobTransferSpecPosixDataSource], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[StorageTransferJobTransferSpecPosixDataSource],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1059c1ddafdcc893a15eb34fd13b94ae30820e22a01f27e5f9a9a90f0be72a51)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.storageTransferJob.StorageTransferJobTransferSpecTransferOptions",
    jsii_struct_bases=[],
    name_mapping={
        "delete_objects_from_source_after_transfer": "deleteObjectsFromSourceAfterTransfer",
        "delete_objects_unique_in_sink": "deleteObjectsUniqueInSink",
        "metadata_options": "metadataOptions",
        "overwrite_objects_already_existing_in_sink": "overwriteObjectsAlreadyExistingInSink",
        "overwrite_when": "overwriteWhen",
    },
)
class StorageTransferJobTransferSpecTransferOptions:
    def __init__(
        self,
        *,
        delete_objects_from_source_after_transfer: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        delete_objects_unique_in_sink: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        metadata_options: typing.Optional[typing.Union["StorageTransferJobTransferSpecTransferOptionsMetadataOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        overwrite_objects_already_existing_in_sink: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        overwrite_when: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param delete_objects_from_source_after_transfer: Whether objects should be deleted from the source after they are transferred to the sink. Note that this option and delete_objects_unique_in_sink are mutually exclusive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#delete_objects_from_source_after_transfer StorageTransferJob#delete_objects_from_source_after_transfer}
        :param delete_objects_unique_in_sink: Whether objects that exist only in the sink should be deleted. Note that this option and delete_objects_from_source_after_transfer are mutually exclusive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#delete_objects_unique_in_sink StorageTransferJob#delete_objects_unique_in_sink}
        :param metadata_options: metadata_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#metadata_options StorageTransferJob#metadata_options}
        :param overwrite_objects_already_existing_in_sink: Whether overwriting objects that already exist in the sink is allowed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#overwrite_objects_already_existing_in_sink StorageTransferJob#overwrite_objects_already_existing_in_sink}
        :param overwrite_when: When to overwrite objects that already exist in the sink. If not set, overwrite behavior is determined by overwriteObjectsAlreadyExistingInSink. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#overwrite_when StorageTransferJob#overwrite_when}
        '''
        if isinstance(metadata_options, dict):
            metadata_options = StorageTransferJobTransferSpecTransferOptionsMetadataOptions(**metadata_options)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__35dc738a77c2ccef9d8078757f150ae8799845ececeb8809535c55e0e4723796)
            check_type(argname="argument delete_objects_from_source_after_transfer", value=delete_objects_from_source_after_transfer, expected_type=type_hints["delete_objects_from_source_after_transfer"])
            check_type(argname="argument delete_objects_unique_in_sink", value=delete_objects_unique_in_sink, expected_type=type_hints["delete_objects_unique_in_sink"])
            check_type(argname="argument metadata_options", value=metadata_options, expected_type=type_hints["metadata_options"])
            check_type(argname="argument overwrite_objects_already_existing_in_sink", value=overwrite_objects_already_existing_in_sink, expected_type=type_hints["overwrite_objects_already_existing_in_sink"])
            check_type(argname="argument overwrite_when", value=overwrite_when, expected_type=type_hints["overwrite_when"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if delete_objects_from_source_after_transfer is not None:
            self._values["delete_objects_from_source_after_transfer"] = delete_objects_from_source_after_transfer
        if delete_objects_unique_in_sink is not None:
            self._values["delete_objects_unique_in_sink"] = delete_objects_unique_in_sink
        if metadata_options is not None:
            self._values["metadata_options"] = metadata_options
        if overwrite_objects_already_existing_in_sink is not None:
            self._values["overwrite_objects_already_existing_in_sink"] = overwrite_objects_already_existing_in_sink
        if overwrite_when is not None:
            self._values["overwrite_when"] = overwrite_when

    @builtins.property
    def delete_objects_from_source_after_transfer(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether objects should be deleted from the source after they are transferred to the sink.

        Note that this option and delete_objects_unique_in_sink are mutually exclusive.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#delete_objects_from_source_after_transfer StorageTransferJob#delete_objects_from_source_after_transfer}
        '''
        result = self._values.get("delete_objects_from_source_after_transfer")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def delete_objects_unique_in_sink(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether objects that exist only in the sink should be deleted.

        Note that this option and delete_objects_from_source_after_transfer are mutually exclusive.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#delete_objects_unique_in_sink StorageTransferJob#delete_objects_unique_in_sink}
        '''
        result = self._values.get("delete_objects_unique_in_sink")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def metadata_options(
        self,
    ) -> typing.Optional["StorageTransferJobTransferSpecTransferOptionsMetadataOptions"]:
        '''metadata_options block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#metadata_options StorageTransferJob#metadata_options}
        '''
        result = self._values.get("metadata_options")
        return typing.cast(typing.Optional["StorageTransferJobTransferSpecTransferOptionsMetadataOptions"], result)

    @builtins.property
    def overwrite_objects_already_existing_in_sink(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether overwriting objects that already exist in the sink is allowed.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#overwrite_objects_already_existing_in_sink StorageTransferJob#overwrite_objects_already_existing_in_sink}
        '''
        result = self._values.get("overwrite_objects_already_existing_in_sink")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def overwrite_when(self) -> typing.Optional[builtins.str]:
        '''When to overwrite objects that already exist in the sink. If not set, overwrite behavior is determined by overwriteObjectsAlreadyExistingInSink.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#overwrite_when StorageTransferJob#overwrite_when}
        '''
        result = self._values.get("overwrite_when")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StorageTransferJobTransferSpecTransferOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.storageTransferJob.StorageTransferJobTransferSpecTransferOptionsMetadataOptions",
    jsii_struct_bases=[],
    name_mapping={
        "acl": "acl",
        "gid": "gid",
        "kms_key": "kmsKey",
        "mode": "mode",
        "storage_class": "storageClass",
        "symlink": "symlink",
        "temporary_hold": "temporaryHold",
        "time_created": "timeCreated",
        "uid": "uid",
    },
)
class StorageTransferJobTransferSpecTransferOptionsMetadataOptions:
    def __init__(
        self,
        *,
        acl: typing.Optional[builtins.str] = None,
        gid: typing.Optional[builtins.str] = None,
        kms_key: typing.Optional[builtins.str] = None,
        mode: typing.Optional[builtins.str] = None,
        storage_class: typing.Optional[builtins.str] = None,
        symlink: typing.Optional[builtins.str] = None,
        temporary_hold: typing.Optional[builtins.str] = None,
        time_created: typing.Optional[builtins.str] = None,
        uid: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param acl: Specifies how each object's ACLs should be preserved for transfers between Google Cloud Storage buckets. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#acl StorageTransferJob#acl}
        :param gid: Specifies how each file's POSIX group ID (GID) attribute should be handled by the transfer. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#gid StorageTransferJob#gid}
        :param kms_key: Specifies how each object's Cloud KMS customer-managed encryption key (CMEK) is preserved for transfers between Google Cloud Storage buckets. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#kms_key StorageTransferJob#kms_key}
        :param mode: Specifies how each file's mode attribute should be handled by the transfer. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#mode StorageTransferJob#mode}
        :param storage_class: Specifies the storage class to set on objects being transferred to Google Cloud Storage buckets. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#storage_class StorageTransferJob#storage_class}
        :param symlink: Specifies how symlinks should be handled by the transfer. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#symlink StorageTransferJob#symlink}
        :param temporary_hold: SSpecifies how each object's temporary hold status should be preserved for transfers between Google Cloud Storage buckets. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#temporary_hold StorageTransferJob#temporary_hold}
        :param time_created: Specifies how each object's timeCreated metadata is preserved for transfers. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#time_created StorageTransferJob#time_created}
        :param uid: Specifies how each file's POSIX user ID (UID) attribute should be handled by the transfer. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#uid StorageTransferJob#uid}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__06ca662aead81df30d51115ef7a8cd7e2e69bcd5749662866127fc92817af565)
            check_type(argname="argument acl", value=acl, expected_type=type_hints["acl"])
            check_type(argname="argument gid", value=gid, expected_type=type_hints["gid"])
            check_type(argname="argument kms_key", value=kms_key, expected_type=type_hints["kms_key"])
            check_type(argname="argument mode", value=mode, expected_type=type_hints["mode"])
            check_type(argname="argument storage_class", value=storage_class, expected_type=type_hints["storage_class"])
            check_type(argname="argument symlink", value=symlink, expected_type=type_hints["symlink"])
            check_type(argname="argument temporary_hold", value=temporary_hold, expected_type=type_hints["temporary_hold"])
            check_type(argname="argument time_created", value=time_created, expected_type=type_hints["time_created"])
            check_type(argname="argument uid", value=uid, expected_type=type_hints["uid"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if acl is not None:
            self._values["acl"] = acl
        if gid is not None:
            self._values["gid"] = gid
        if kms_key is not None:
            self._values["kms_key"] = kms_key
        if mode is not None:
            self._values["mode"] = mode
        if storage_class is not None:
            self._values["storage_class"] = storage_class
        if symlink is not None:
            self._values["symlink"] = symlink
        if temporary_hold is not None:
            self._values["temporary_hold"] = temporary_hold
        if time_created is not None:
            self._values["time_created"] = time_created
        if uid is not None:
            self._values["uid"] = uid

    @builtins.property
    def acl(self) -> typing.Optional[builtins.str]:
        '''Specifies how each object's ACLs should be preserved for transfers between Google Cloud Storage buckets.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#acl StorageTransferJob#acl}
        '''
        result = self._values.get("acl")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def gid(self) -> typing.Optional[builtins.str]:
        '''Specifies how each file's POSIX group ID (GID) attribute should be handled by the transfer.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#gid StorageTransferJob#gid}
        '''
        result = self._values.get("gid")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kms_key(self) -> typing.Optional[builtins.str]:
        '''Specifies how each object's Cloud KMS customer-managed encryption key (CMEK) is preserved for transfers between Google Cloud Storage buckets.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#kms_key StorageTransferJob#kms_key}
        '''
        result = self._values.get("kms_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def mode(self) -> typing.Optional[builtins.str]:
        '''Specifies how each file's mode attribute should be handled by the transfer.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#mode StorageTransferJob#mode}
        '''
        result = self._values.get("mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def storage_class(self) -> typing.Optional[builtins.str]:
        '''Specifies the storage class to set on objects being transferred to Google Cloud Storage buckets.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#storage_class StorageTransferJob#storage_class}
        '''
        result = self._values.get("storage_class")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def symlink(self) -> typing.Optional[builtins.str]:
        '''Specifies how symlinks should be handled by the transfer.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#symlink StorageTransferJob#symlink}
        '''
        result = self._values.get("symlink")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def temporary_hold(self) -> typing.Optional[builtins.str]:
        '''SSpecifies how each object's temporary hold status should be preserved for transfers between Google Cloud Storage buckets.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#temporary_hold StorageTransferJob#temporary_hold}
        '''
        result = self._values.get("temporary_hold")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def time_created(self) -> typing.Optional[builtins.str]:
        '''Specifies how each object's timeCreated metadata is preserved for transfers.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#time_created StorageTransferJob#time_created}
        '''
        result = self._values.get("time_created")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def uid(self) -> typing.Optional[builtins.str]:
        '''Specifies how each file's POSIX user ID (UID) attribute should be handled by the transfer.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#uid StorageTransferJob#uid}
        '''
        result = self._values.get("uid")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StorageTransferJobTransferSpecTransferOptionsMetadataOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class StorageTransferJobTransferSpecTransferOptionsMetadataOptionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.storageTransferJob.StorageTransferJobTransferSpecTransferOptionsMetadataOptionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ccedf58d8e8feebac6d36241032e422a423a3d0974af27091242e6c58c7ec3fa)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAcl")
    def reset_acl(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAcl", []))

    @jsii.member(jsii_name="resetGid")
    def reset_gid(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGid", []))

    @jsii.member(jsii_name="resetKmsKey")
    def reset_kms_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKmsKey", []))

    @jsii.member(jsii_name="resetMode")
    def reset_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMode", []))

    @jsii.member(jsii_name="resetStorageClass")
    def reset_storage_class(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStorageClass", []))

    @jsii.member(jsii_name="resetSymlink")
    def reset_symlink(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSymlink", []))

    @jsii.member(jsii_name="resetTemporaryHold")
    def reset_temporary_hold(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTemporaryHold", []))

    @jsii.member(jsii_name="resetTimeCreated")
    def reset_time_created(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeCreated", []))

    @jsii.member(jsii_name="resetUid")
    def reset_uid(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUid", []))

    @builtins.property
    @jsii.member(jsii_name="aclInput")
    def acl_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "aclInput"))

    @builtins.property
    @jsii.member(jsii_name="gidInput")
    def gid_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "gidInput"))

    @builtins.property
    @jsii.member(jsii_name="kmsKeyInput")
    def kms_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "kmsKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="modeInput")
    def mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "modeInput"))

    @builtins.property
    @jsii.member(jsii_name="storageClassInput")
    def storage_class_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "storageClassInput"))

    @builtins.property
    @jsii.member(jsii_name="symlinkInput")
    def symlink_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "symlinkInput"))

    @builtins.property
    @jsii.member(jsii_name="temporaryHoldInput")
    def temporary_hold_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "temporaryHoldInput"))

    @builtins.property
    @jsii.member(jsii_name="timeCreatedInput")
    def time_created_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "timeCreatedInput"))

    @builtins.property
    @jsii.member(jsii_name="uidInput")
    def uid_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "uidInput"))

    @builtins.property
    @jsii.member(jsii_name="acl")
    def acl(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "acl"))

    @acl.setter
    def acl(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__322abf62d753901b8968a1a856d5727b835fd28a77295218959cf28893f14025)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "acl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="gid")
    def gid(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "gid"))

    @gid.setter
    def gid(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ddfa0f811c3240050e6ae16c974f2b96df3818d936d2d7f31a1dbe7fec8ff31)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "gid", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="kmsKey")
    def kms_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kmsKey"))

    @kms_key.setter
    def kms_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__294126e609b81240b97cff9cc2dd8439f31ec74ab1063dbdef2f51f3f2defdfe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="mode")
    def mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mode"))

    @mode.setter
    def mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__44f7ac288acdd7fa1a4860f283f5e477793ea412beba33678c6b8f845a011552)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="storageClass")
    def storage_class(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "storageClass"))

    @storage_class.setter
    def storage_class(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a617c66f113e77250955b160b067e790b79d15d590486de1fa4bc5076120f81f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "storageClass", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="symlink")
    def symlink(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "symlink"))

    @symlink.setter
    def symlink(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d007f130950d870e1364d098b1b41eb1339a6aceb5309b854e0c97986acd01f5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "symlink", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="temporaryHold")
    def temporary_hold(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "temporaryHold"))

    @temporary_hold.setter
    def temporary_hold(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a011a41deb42aaf045eddee7ca59de58223f036e6725b0e3c30c07369c5ba99c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "temporaryHold", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="timeCreated")
    def time_created(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "timeCreated"))

    @time_created.setter
    def time_created(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e5c6e6d21682a1a8e429cb8eb716e1e2951c95dc09c3d71be9ea142c8ffa1396)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timeCreated", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="uid")
    def uid(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "uid"))

    @uid.setter
    def uid(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e867becaaa2e9ef041d68e700cd924fd4098962346bd1c94a2c134d1274f7407)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "uid", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[StorageTransferJobTransferSpecTransferOptionsMetadataOptions]:
        return typing.cast(typing.Optional[StorageTransferJobTransferSpecTransferOptionsMetadataOptions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[StorageTransferJobTransferSpecTransferOptionsMetadataOptions],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a124c94b098be646371f7398cc0063443ac5c6f8a713e786d8fcad2276e05111)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class StorageTransferJobTransferSpecTransferOptionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.storageTransferJob.StorageTransferJobTransferSpecTransferOptionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__44fc6eacdfa1845c7dad6cd4f994e10d56336f4ceee480e536cb7d4c2b001cec)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putMetadataOptions")
    def put_metadata_options(
        self,
        *,
        acl: typing.Optional[builtins.str] = None,
        gid: typing.Optional[builtins.str] = None,
        kms_key: typing.Optional[builtins.str] = None,
        mode: typing.Optional[builtins.str] = None,
        storage_class: typing.Optional[builtins.str] = None,
        symlink: typing.Optional[builtins.str] = None,
        temporary_hold: typing.Optional[builtins.str] = None,
        time_created: typing.Optional[builtins.str] = None,
        uid: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param acl: Specifies how each object's ACLs should be preserved for transfers between Google Cloud Storage buckets. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#acl StorageTransferJob#acl}
        :param gid: Specifies how each file's POSIX group ID (GID) attribute should be handled by the transfer. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#gid StorageTransferJob#gid}
        :param kms_key: Specifies how each object's Cloud KMS customer-managed encryption key (CMEK) is preserved for transfers between Google Cloud Storage buckets. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#kms_key StorageTransferJob#kms_key}
        :param mode: Specifies how each file's mode attribute should be handled by the transfer. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#mode StorageTransferJob#mode}
        :param storage_class: Specifies the storage class to set on objects being transferred to Google Cloud Storage buckets. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#storage_class StorageTransferJob#storage_class}
        :param symlink: Specifies how symlinks should be handled by the transfer. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#symlink StorageTransferJob#symlink}
        :param temporary_hold: SSpecifies how each object's temporary hold status should be preserved for transfers between Google Cloud Storage buckets. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#temporary_hold StorageTransferJob#temporary_hold}
        :param time_created: Specifies how each object's timeCreated metadata is preserved for transfers. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#time_created StorageTransferJob#time_created}
        :param uid: Specifies how each file's POSIX user ID (UID) attribute should be handled by the transfer. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_transfer_job#uid StorageTransferJob#uid}
        '''
        value = StorageTransferJobTransferSpecTransferOptionsMetadataOptions(
            acl=acl,
            gid=gid,
            kms_key=kms_key,
            mode=mode,
            storage_class=storage_class,
            symlink=symlink,
            temporary_hold=temporary_hold,
            time_created=time_created,
            uid=uid,
        )

        return typing.cast(None, jsii.invoke(self, "putMetadataOptions", [value]))

    @jsii.member(jsii_name="resetDeleteObjectsFromSourceAfterTransfer")
    def reset_delete_objects_from_source_after_transfer(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDeleteObjectsFromSourceAfterTransfer", []))

    @jsii.member(jsii_name="resetDeleteObjectsUniqueInSink")
    def reset_delete_objects_unique_in_sink(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDeleteObjectsUniqueInSink", []))

    @jsii.member(jsii_name="resetMetadataOptions")
    def reset_metadata_options(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMetadataOptions", []))

    @jsii.member(jsii_name="resetOverwriteObjectsAlreadyExistingInSink")
    def reset_overwrite_objects_already_existing_in_sink(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOverwriteObjectsAlreadyExistingInSink", []))

    @jsii.member(jsii_name="resetOverwriteWhen")
    def reset_overwrite_when(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOverwriteWhen", []))

    @builtins.property
    @jsii.member(jsii_name="metadataOptions")
    def metadata_options(
        self,
    ) -> StorageTransferJobTransferSpecTransferOptionsMetadataOptionsOutputReference:
        return typing.cast(StorageTransferJobTransferSpecTransferOptionsMetadataOptionsOutputReference, jsii.get(self, "metadataOptions"))

    @builtins.property
    @jsii.member(jsii_name="deleteObjectsFromSourceAfterTransferInput")
    def delete_objects_from_source_after_transfer_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "deleteObjectsFromSourceAfterTransferInput"))

    @builtins.property
    @jsii.member(jsii_name="deleteObjectsUniqueInSinkInput")
    def delete_objects_unique_in_sink_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "deleteObjectsUniqueInSinkInput"))

    @builtins.property
    @jsii.member(jsii_name="metadataOptionsInput")
    def metadata_options_input(
        self,
    ) -> typing.Optional[StorageTransferJobTransferSpecTransferOptionsMetadataOptions]:
        return typing.cast(typing.Optional[StorageTransferJobTransferSpecTransferOptionsMetadataOptions], jsii.get(self, "metadataOptionsInput"))

    @builtins.property
    @jsii.member(jsii_name="overwriteObjectsAlreadyExistingInSinkInput")
    def overwrite_objects_already_existing_in_sink_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "overwriteObjectsAlreadyExistingInSinkInput"))

    @builtins.property
    @jsii.member(jsii_name="overwriteWhenInput")
    def overwrite_when_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "overwriteWhenInput"))

    @builtins.property
    @jsii.member(jsii_name="deleteObjectsFromSourceAfterTransfer")
    def delete_objects_from_source_after_transfer(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "deleteObjectsFromSourceAfterTransfer"))

    @delete_objects_from_source_after_transfer.setter
    def delete_objects_from_source_after_transfer(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7ddcec5f5634f945fa6f30b0d15ddf1a3554cbc65815c9225f6bbbc5388e2d51)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deleteObjectsFromSourceAfterTransfer", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="deleteObjectsUniqueInSink")
    def delete_objects_unique_in_sink(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "deleteObjectsUniqueInSink"))

    @delete_objects_unique_in_sink.setter
    def delete_objects_unique_in_sink(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d7dc5f9f10cf928487ef07c1cd001083527778f29bd841b606860ce345de00a7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deleteObjectsUniqueInSink", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="overwriteObjectsAlreadyExistingInSink")
    def overwrite_objects_already_existing_in_sink(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "overwriteObjectsAlreadyExistingInSink"))

    @overwrite_objects_already_existing_in_sink.setter
    def overwrite_objects_already_existing_in_sink(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b0c6bc1144bf0293571119beb0b84001601a70665636ee517f94591ee9d2bffa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "overwriteObjectsAlreadyExistingInSink", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="overwriteWhen")
    def overwrite_when(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "overwriteWhen"))

    @overwrite_when.setter
    def overwrite_when(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__532ff2556a017658406a7d0a1a99217d712433388e44c0fdb45530a86352df66)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "overwriteWhen", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[StorageTransferJobTransferSpecTransferOptions]:
        return typing.cast(typing.Optional[StorageTransferJobTransferSpecTransferOptions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[StorageTransferJobTransferSpecTransferOptions],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d6b2e3b4c35ad897517af7d172af288e2abe4ca8c41ef59631bdc64e28a1417d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "StorageTransferJob",
    "StorageTransferJobConfig",
    "StorageTransferJobEventStream",
    "StorageTransferJobEventStreamOutputReference",
    "StorageTransferJobLoggingConfig",
    "StorageTransferJobLoggingConfigOutputReference",
    "StorageTransferJobNotificationConfig",
    "StorageTransferJobNotificationConfigOutputReference",
    "StorageTransferJobReplicationSpec",
    "StorageTransferJobReplicationSpecGcsDataSink",
    "StorageTransferJobReplicationSpecGcsDataSinkOutputReference",
    "StorageTransferJobReplicationSpecGcsDataSource",
    "StorageTransferJobReplicationSpecGcsDataSourceOutputReference",
    "StorageTransferJobReplicationSpecObjectConditions",
    "StorageTransferJobReplicationSpecObjectConditionsOutputReference",
    "StorageTransferJobReplicationSpecOutputReference",
    "StorageTransferJobReplicationSpecTransferOptions",
    "StorageTransferJobReplicationSpecTransferOptionsMetadataOptions",
    "StorageTransferJobReplicationSpecTransferOptionsMetadataOptionsOutputReference",
    "StorageTransferJobReplicationSpecTransferOptionsOutputReference",
    "StorageTransferJobSchedule",
    "StorageTransferJobScheduleOutputReference",
    "StorageTransferJobScheduleScheduleEndDate",
    "StorageTransferJobScheduleScheduleEndDateOutputReference",
    "StorageTransferJobScheduleScheduleStartDate",
    "StorageTransferJobScheduleScheduleStartDateOutputReference",
    "StorageTransferJobScheduleStartTimeOfDay",
    "StorageTransferJobScheduleStartTimeOfDayOutputReference",
    "StorageTransferJobTransferSpec",
    "StorageTransferJobTransferSpecAwsS3DataSource",
    "StorageTransferJobTransferSpecAwsS3DataSourceAwsAccessKey",
    "StorageTransferJobTransferSpecAwsS3DataSourceAwsAccessKeyOutputReference",
    "StorageTransferJobTransferSpecAwsS3DataSourceOutputReference",
    "StorageTransferJobTransferSpecAzureBlobStorageDataSource",
    "StorageTransferJobTransferSpecAzureBlobStorageDataSourceAzureCredentials",
    "StorageTransferJobTransferSpecAzureBlobStorageDataSourceAzureCredentialsOutputReference",
    "StorageTransferJobTransferSpecAzureBlobStorageDataSourceOutputReference",
    "StorageTransferJobTransferSpecGcsDataSink",
    "StorageTransferJobTransferSpecGcsDataSinkOutputReference",
    "StorageTransferJobTransferSpecGcsDataSource",
    "StorageTransferJobTransferSpecGcsDataSourceOutputReference",
    "StorageTransferJobTransferSpecHdfsDataSource",
    "StorageTransferJobTransferSpecHdfsDataSourceOutputReference",
    "StorageTransferJobTransferSpecHttpDataSource",
    "StorageTransferJobTransferSpecHttpDataSourceOutputReference",
    "StorageTransferJobTransferSpecObjectConditions",
    "StorageTransferJobTransferSpecObjectConditionsOutputReference",
    "StorageTransferJobTransferSpecOutputReference",
    "StorageTransferJobTransferSpecPosixDataSink",
    "StorageTransferJobTransferSpecPosixDataSinkOutputReference",
    "StorageTransferJobTransferSpecPosixDataSource",
    "StorageTransferJobTransferSpecPosixDataSourceOutputReference",
    "StorageTransferJobTransferSpecTransferOptions",
    "StorageTransferJobTransferSpecTransferOptionsMetadataOptions",
    "StorageTransferJobTransferSpecTransferOptionsMetadataOptionsOutputReference",
    "StorageTransferJobTransferSpecTransferOptionsOutputReference",
]

publication.publish()

def _typecheckingstub__604dde1ca05a28e0d0eadc9cd78311419a134cd77555ce647ed1a5d12bc6d06a(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    description: builtins.str,
    event_stream: typing.Optional[typing.Union[StorageTransferJobEventStream, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    logging_config: typing.Optional[typing.Union[StorageTransferJobLoggingConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    name: typing.Optional[builtins.str] = None,
    notification_config: typing.Optional[typing.Union[StorageTransferJobNotificationConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    project: typing.Optional[builtins.str] = None,
    replication_spec: typing.Optional[typing.Union[StorageTransferJobReplicationSpec, typing.Dict[builtins.str, typing.Any]]] = None,
    schedule: typing.Optional[typing.Union[StorageTransferJobSchedule, typing.Dict[builtins.str, typing.Any]]] = None,
    status: typing.Optional[builtins.str] = None,
    transfer_spec: typing.Optional[typing.Union[StorageTransferJobTransferSpec, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__70670f5bc5ecb71ce90d9b0414f836a3cb56a784a2388ca55db699b23b9d4b00(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b483074f400562bcc10f134813a4e32c8b2eb1781548cb51a9944a5a7758f6d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e3064fd2589fdf6619f06091bb32992194c3f99e74f5e56097d0141e72fff26(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__47128417076e48e19d2bf000abbbaf4d51cbd1243e233f128a8a340728a550f0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f863572eaade88173fd667d45896dd44ff3c8c2f9db5a63d46274cd80f8f1d0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__32d13d6bdccd1e488087f39d659df6104839f743d1c7892faafc74ccd0900c57(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__740ad737fa45784b1c1563b5d1543a9ed33431538cc7585d37dd89670e91bbd6(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    description: builtins.str,
    event_stream: typing.Optional[typing.Union[StorageTransferJobEventStream, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    logging_config: typing.Optional[typing.Union[StorageTransferJobLoggingConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    name: typing.Optional[builtins.str] = None,
    notification_config: typing.Optional[typing.Union[StorageTransferJobNotificationConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    project: typing.Optional[builtins.str] = None,
    replication_spec: typing.Optional[typing.Union[StorageTransferJobReplicationSpec, typing.Dict[builtins.str, typing.Any]]] = None,
    schedule: typing.Optional[typing.Union[StorageTransferJobSchedule, typing.Dict[builtins.str, typing.Any]]] = None,
    status: typing.Optional[builtins.str] = None,
    transfer_spec: typing.Optional[typing.Union[StorageTransferJobTransferSpec, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__48041b3a819c6f62ef03bf6defd68d8fb07ddd4f5266ffc2c5daa1f436c4ddb1(
    *,
    name: builtins.str,
    event_stream_expiration_time: typing.Optional[builtins.str] = None,
    event_stream_start_time: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22dbb68d4c01844ce62d4db03f2ee354faaddc10251a318d94656276dd6920a0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bdb5e574be986d5a1947d95d1b230cae2390478a785075ff82654a2d304f0fb3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d9efc1ca7f8278ad9c84d7a1644f5c7b660fd46d4ee54d4472ef514dde80aa4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e7194355bdf2d69d5722006235e1d67d84745e240f7195673a4d5ed2e35162a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44bde1e4e9f2ec4ac317c1071bb54751f3ce46ac645e414c9788376f2223d767(
    value: typing.Optional[StorageTransferJobEventStream],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97a19045f96d78d06d5208c1f2f56c719f1831ec65c3bcb4c8686c351b496765(
    *,
    enable_on_prem_gcs_transfer_logs: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    log_actions: typing.Optional[typing.Sequence[builtins.str]] = None,
    log_action_states: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04c259e2ecc4d7577c4a0789dbfa2f9bf9d298af6d684dd58c5f6c68d895c979(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad35f5b941101334fdba41daa8e6f36138d584ba5afd180be09dfe69bd25c125(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89c70e478571dd4ba6904d8d1a9d32551b656aa1972b2943e05e2e35d83f24f8(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71654c1ddbe89185675ee096241c8a43d6b0a7e048a6e733b8f465097754c4e4(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__929457f6b1a13b41a817e522196b982218dcc1fd73de8afd22bd4f49e31fb5b7(
    value: typing.Optional[StorageTransferJobLoggingConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39f876b24cbf33ea9cfc5d7bbc8af8361b054125b2cd24159595aaa968c8d0b1(
    *,
    payload_format: builtins.str,
    pubsub_topic: builtins.str,
    event_types: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db98b0a9f7e0c0a7d5349b2a2274df84c77d18b1662fe449a18c11e83d9190eb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8131351a83d749d77320e2a4cadc7ce851076e6a86ebe867d3842cba71941508(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a16bc9a7653f7a6bf7df394d9081c26d32c9e812031c4a1ec36428dff9e1183(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ccda11c16c2c8dcd8f8a75d194a6be0f29ea5a7c162185cf11744ccbed559e5a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b1f15d32aa63b27797f79cf3e26d4819d21bed0622034a3f95cedb09d467272(
    value: typing.Optional[StorageTransferJobNotificationConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e67a99cce8a9779c5b10a6d37389d369bb25c038db1b64969221d24e61f01845(
    *,
    gcs_data_sink: typing.Optional[typing.Union[StorageTransferJobReplicationSpecGcsDataSink, typing.Dict[builtins.str, typing.Any]]] = None,
    gcs_data_source: typing.Optional[typing.Union[StorageTransferJobReplicationSpecGcsDataSource, typing.Dict[builtins.str, typing.Any]]] = None,
    object_conditions: typing.Optional[typing.Union[StorageTransferJobReplicationSpecObjectConditions, typing.Dict[builtins.str, typing.Any]]] = None,
    transfer_options: typing.Optional[typing.Union[StorageTransferJobReplicationSpecTransferOptions, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b54fa5e9047adba5340a7ac5bacf2f9c621971bbe38d5ac3dc3b39d826c3e9d6(
    *,
    bucket_name: builtins.str,
    path: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a868dbfa8da6cd55df1df6de892a5e688f2ca0b14c5e14c8e494e340157062f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1cafd87b9b0aa51ed9e4f314b611adb75ee0f31d1a4c02f5bf413505bc6c90ee(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a1a48eef67e0dbe46ab897b631715f5103801946b6005e13a7290039309693e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e8d80c335944a31680da659aacfa96b09d43c129e7217904e8c244393abf7b8(
    value: typing.Optional[StorageTransferJobReplicationSpecGcsDataSink],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0aa838cc3ba0129b0e14be75cebb3822f865e325b0bd6cefcdc719c617e2b7b(
    *,
    bucket_name: builtins.str,
    path: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__012003b9432c9e6f73ccb29ec8d451642c0a4c4b387264fb5adc3f691b3f1e7a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__489f5f6eceb04adabb057e3558959811d77826b9278449c114d5dad01f1f265f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b7042e540acf7671ce097faccdb8d4f14c90be3232a88004e3b93649a11cabe(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8dd9a8b681d4bbc8432614e11fc01a13696e4b81d0783d1fe5aee2274745c488(
    value: typing.Optional[StorageTransferJobReplicationSpecGcsDataSource],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__793be15b9fee1b6718ec6192eee7e6730ea40343cdce13d295edbd6205ef8db9(
    *,
    exclude_prefixes: typing.Optional[typing.Sequence[builtins.str]] = None,
    include_prefixes: typing.Optional[typing.Sequence[builtins.str]] = None,
    last_modified_before: typing.Optional[builtins.str] = None,
    last_modified_since: typing.Optional[builtins.str] = None,
    max_time_elapsed_since_last_modification: typing.Optional[builtins.str] = None,
    min_time_elapsed_since_last_modification: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18dba7a078bea08b9b4b80f49d3507a63c41a6470d2125e799b403726f1a5a6b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__633725c421ccea19600c4ad15e2fd291c907949a3f03255cc569b7af5be8d7a0(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__552dc747bae4b025e7d5572af5887e719920a25d6a27be04233ea8c128daa6bc(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b45d5a013279db78b34814e21e2ecdbdcc3a757f55ee9c8c9ee6d8f65d389cd1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af757d49a9a57fef24a40e3de2375048bd978bd1270c07c06be6a709a0f5daf4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e656c30ab04469a001c1412024e1a0dbd4a36cbaf28bc474ded0fedac2e9b355(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d559af2931e28d7cc1056b973630d49546894e03eb671af6720fb1dc576772be(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7bb9936e05a8dc973d511e03e6ea24362008dc6283bcf05e3fcbfc693d353f79(
    value: typing.Optional[StorageTransferJobReplicationSpecObjectConditions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e03a9ed5177a11c6f48d6673b1adb4b1305747dd5b20784dafc70881e4cea9fe(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__142d51934a5b8bb3919d14b8e348cf43c8984d6667441fe1c75aff1909dc8b4b(
    value: typing.Optional[StorageTransferJobReplicationSpec],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8aafd453dc117b43656f594071a0fae9389eeffe6caee7c340e715dea52ed63(
    *,
    delete_objects_from_source_after_transfer: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    delete_objects_unique_in_sink: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    metadata_options: typing.Optional[typing.Union[StorageTransferJobReplicationSpecTransferOptionsMetadataOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    overwrite_objects_already_existing_in_sink: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    overwrite_when: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__130a5b8c681559809fea1ef66632ff905a07c1e957945e9531f96439c6b85bad(
    *,
    acl: typing.Optional[builtins.str] = None,
    gid: typing.Optional[builtins.str] = None,
    kms_key: typing.Optional[builtins.str] = None,
    mode: typing.Optional[builtins.str] = None,
    storage_class: typing.Optional[builtins.str] = None,
    symlink: typing.Optional[builtins.str] = None,
    temporary_hold: typing.Optional[builtins.str] = None,
    time_created: typing.Optional[builtins.str] = None,
    uid: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__901a15c8cca6347e121102ced1355b91d94f51d4ec0f7637c0e709b037e9ce3c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0f3c1aa5abc023228c43761a68d8f3c0070ff03cbd7948806858e628cfb36ff(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45454aa9fee575e77f8a0c748e95cfb2debbd69dd6c5b23a2e3834d708b8d91c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd2b09a51c3bfa000c04c4297465d19170c0c015b9a43566b1f4f66b1b55c5f9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__90ead3cb853d6f4ad3d57a3ba2c22c3757ace7cc1531e6cb51b19349e29afe83(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ac41b050e748c9a97ec418e4b8beb61fd9dd625cc4d769bc46969fcd9304076(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b089e5ceb26a8e5439c04d38ad36051a759e2caf232b5597c00306ab93168a3b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68e22df7e4a8cccd4ca3847c71299fd3a9258c96ee445340f5eb7fdabe9fb31b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dab4ad522de4a3bc894523f453db6dc93feeb29dd7c7a1525c61a277ef2ed706(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37ef0e62b6adb096de787e407d0124f0e99c4b0de40cce79f186efc4811e0131(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e03b70aa1b87dc44e0525e6e809915b38a86578721197cee522169c76bffd2bf(
    value: typing.Optional[StorageTransferJobReplicationSpecTransferOptionsMetadataOptions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9986d842e538369a6f11a760a6576c9b1443ca501ee1b4654ac82b5ff823591f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__08c8df261c1f1641513937f237cf5da428e48febb8cd9e75bfaf507768c72128(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22dc567e4c12d21d4c226e174b02b8d1fc28df37218090a08e34521679ee3467(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__abc6b47a4ad1956aa8c7256fafae00479c97659b6dac792b583cb934c6b39fff(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2cdce1a19b4d7ae0e1f84ac9efc8e48b9276d9988fbd4f0f3360b8926184a705(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80531a138e745d345915baf077d9c428609ba3e9a93739058398b2c180b725fb(
    value: typing.Optional[StorageTransferJobReplicationSpecTransferOptions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__55f63d7886224c7c5beae3376ea76fd9d40a0f79aec94d9e27d5fc05b192484b(
    *,
    schedule_start_date: typing.Union[StorageTransferJobScheduleScheduleStartDate, typing.Dict[builtins.str, typing.Any]],
    repeat_interval: typing.Optional[builtins.str] = None,
    schedule_end_date: typing.Optional[typing.Union[StorageTransferJobScheduleScheduleEndDate, typing.Dict[builtins.str, typing.Any]]] = None,
    start_time_of_day: typing.Optional[typing.Union[StorageTransferJobScheduleStartTimeOfDay, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3fe42e68c683edc4298cedff50bd249989056966deb1778da33db489a3bd87fa(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__311dd224d352e272405cc7ef1b4a9c2d4c7f6467c46deb13ffb9d0c2a17b192e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9753e4e62939e44b4bfcaf6b9d08a1e388520db855e4fe27df9490892c7cd34(
    value: typing.Optional[StorageTransferJobSchedule],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b014353fa247d8249f322677c5c26125ac592047e40540a8ff5616a0c700bcdc(
    *,
    day: jsii.Number,
    month: jsii.Number,
    year: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__32c439158c8eafd04319dfa19143bd6f93717ffdf65286097d98dfddf6db5b9e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee51bcbc21ac4ab535e408c6d0525b582a51c5685065c68ecd7f81aa0d91777c(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__579b5ca37619e19f1d5fc638a1203cd6f300fa5eb5863c6006fd39be503e7a82(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63b3b80958fad956ee4f08018bf26d26a3c881ceaee53df817edaa4c3806ba07(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__676994805373d0d7d149e7ba33b964c468001b8fb32bdee26aada89fb6b8fe9d(
    value: typing.Optional[StorageTransferJobScheduleScheduleEndDate],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5cf825abfa5ce3ffa096e28c3587b41093d998532fc9e6c3066ead43bfad6f4(
    *,
    day: jsii.Number,
    month: jsii.Number,
    year: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40c7a80e67a54a4a64a62f573a05d53981366fddc2de36459e5a7e0c69b7dc02(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b659fd6aa05af8de6beacd1d95db2dd95ad68c159f9109d4269505ac333273a3(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11c17b30246f46d51f1fefef3cb03f4daaaa91bc47eb1e625b2acbb8a90f596e(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__372a9cb94cc520993323802c8bce30c1b3f85b0176e8f79f90ddc3cd09ad3599(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fdbb25cc510d24ab7df919827765b6f4b9e177d0654f896efa10cde1ff8b030d(
    value: typing.Optional[StorageTransferJobScheduleScheduleStartDate],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__059cd2d958dec2e4894561178446d0f7c4c4ec860e40f4ad2f4f4e21feacb6e3(
    *,
    hours: jsii.Number,
    minutes: jsii.Number,
    nanos: jsii.Number,
    seconds: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d738e598a916dd592967b641458d371523beee596e999bd9e528c3c97f0730eb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__278c7a29da1caffbef5d1f7a0b4dffe312c7feba1fceac2e08357950832ceebc(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7795f90f2169993008dadc5b451108def1c67ef0423112a425f45dee31dfa36(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a930101317af07f9c72342e377c373ea1c59dd4bba0a7f948b5e2474e6b7fdb9(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fba8c13181605b2293ff75cb1835b140ac344133e2ca33acd22820e758059efe(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b39cc734fb9bdab90a79e2eb279cfbeada388b3be97bb9e6a33ee5bd422c0c66(
    value: typing.Optional[StorageTransferJobScheduleStartTimeOfDay],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6bbf9b3dd51c8b4ee6e7edc92253208967dad3ece396e6d244cb71486070b418(
    *,
    aws_s3_data_source: typing.Optional[typing.Union[StorageTransferJobTransferSpecAwsS3DataSource, typing.Dict[builtins.str, typing.Any]]] = None,
    azure_blob_storage_data_source: typing.Optional[typing.Union[StorageTransferJobTransferSpecAzureBlobStorageDataSource, typing.Dict[builtins.str, typing.Any]]] = None,
    gcs_data_sink: typing.Optional[typing.Union[StorageTransferJobTransferSpecGcsDataSink, typing.Dict[builtins.str, typing.Any]]] = None,
    gcs_data_source: typing.Optional[typing.Union[StorageTransferJobTransferSpecGcsDataSource, typing.Dict[builtins.str, typing.Any]]] = None,
    hdfs_data_source: typing.Optional[typing.Union[StorageTransferJobTransferSpecHdfsDataSource, typing.Dict[builtins.str, typing.Any]]] = None,
    http_data_source: typing.Optional[typing.Union[StorageTransferJobTransferSpecHttpDataSource, typing.Dict[builtins.str, typing.Any]]] = None,
    object_conditions: typing.Optional[typing.Union[StorageTransferJobTransferSpecObjectConditions, typing.Dict[builtins.str, typing.Any]]] = None,
    posix_data_sink: typing.Optional[typing.Union[StorageTransferJobTransferSpecPosixDataSink, typing.Dict[builtins.str, typing.Any]]] = None,
    posix_data_source: typing.Optional[typing.Union[StorageTransferJobTransferSpecPosixDataSource, typing.Dict[builtins.str, typing.Any]]] = None,
    sink_agent_pool_name: typing.Optional[builtins.str] = None,
    source_agent_pool_name: typing.Optional[builtins.str] = None,
    transfer_options: typing.Optional[typing.Union[StorageTransferJobTransferSpecTransferOptions, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d93ddf36043d9da4ccee494c94a40fca3bf1a740c3b4342643b2c68576375b14(
    *,
    bucket_name: builtins.str,
    aws_access_key: typing.Optional[typing.Union[StorageTransferJobTransferSpecAwsS3DataSourceAwsAccessKey, typing.Dict[builtins.str, typing.Any]]] = None,
    managed_private_network: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    path: typing.Optional[builtins.str] = None,
    role_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d74111a4db2942c3a22c28358392a18696b9ddfb95515d97207631524c4ed27c(
    *,
    access_key_id: builtins.str,
    secret_access_key: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__008f1c1eb63940e88987b1986ecc5c8c49c253fc6e43be0883938d7ed428a082(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd6d447626279486282bffe81b0f2da5b82f7c84118683b7f144ab63e994d2f8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__510ed705248c1a32d30adedb168bbcf07ed2c3c598b08cbcab335bfffd820d11(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2e4bc13b5aa803c1e7fa228f9e26154a6daef1ae25f2971f2dc085b3b03bd45(
    value: typing.Optional[StorageTransferJobTransferSpecAwsS3DataSourceAwsAccessKey],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f51cf5c37cd970d6b9e7d722e4a6a9fe8544f277cc13b81b126399b58b95954d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9dc1f4d61d2da5cb705980781bce6dac09c2237b0a117e6c00f83f3cde6841b1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__605883f0c7169039cac4d616a8e7821c1ed934fa7a5a2ca00d993d7e33481191(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4347ea4df73e7f541f836d4d324d3d7b0d0dc1a93e1c3e26d467ae992de7184a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__290d209fdadc4991b9667e5eb1f9f4f163ba94a01959e7dbfac25886a33bd5e5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ac1bb0fa3e8f514745057c112825dfdd16105efebb1aa5b3b128a52c2c09f7b(
    value: typing.Optional[StorageTransferJobTransferSpecAwsS3DataSource],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9631493f405ce52e93d5bfbac85bbcdca6aba46fb07980ace00d3d79d80e5015(
    *,
    azure_credentials: typing.Union[StorageTransferJobTransferSpecAzureBlobStorageDataSourceAzureCredentials, typing.Dict[builtins.str, typing.Any]],
    container: builtins.str,
    storage_account: builtins.str,
    path: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c73d9ef285f21b6688ec1694295dc363c4215809bd13718c091281b82c636b5(
    *,
    sas_token: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__537c2d115473b9853c78b1a6d0beeabb140e013effa7425293ecf8764df169c3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2138191a4cc1c56946bb3cada771d1bc1ec71e3e351321744ca8634d48376519(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7c947af68b79e745500c876c245cb987ba07ebab90b1f9b78d0f91cc67c6339(
    value: typing.Optional[StorageTransferJobTransferSpecAzureBlobStorageDataSourceAzureCredentials],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0bddec689664ade62f15badd02cec60580af32554431ea398cfad777a0f309a4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d577adeede63751c6ee002b02a15839551ae41114a6912aaf380dcf0de6e3a47(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15a500bab5f786f47b1e9bee1cdd21ac9df97f66bb20c3e72842e1d747e29e88(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85585828ef1eb148b7639d76f42656771f7572e30ac1b155c83747ab0174e61b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__847afd8fd4a38fec1eadbee51ca8e4679e8862e387c7fd6cfc496e3c84f063e8(
    value: typing.Optional[StorageTransferJobTransferSpecAzureBlobStorageDataSource],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__815fda8744fae5b0dc0b2edc7549907abbbb517b4bc1fc2974d71592780ab2dd(
    *,
    bucket_name: builtins.str,
    path: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0db24c451a7c6807743bf0a61b917c78b650cf9410ebda3d021a925050d576a6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb022aeb4a48d524ed1fce3cda844764615931ce3c68625aec81fb94d6b6b520(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d5b2e85b33d5561efcbf5c12821d1fec1bd2578614ef8dcfd2cc2c842cab67a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36a36bc165274959496ddc17206367ac5bce0b95683ced6da275f9920ef9fb70(
    value: typing.Optional[StorageTransferJobTransferSpecGcsDataSink],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86239c255f9be3bca3e65c311ffc44c2f8dae9a763bd18870ea3eeb77d254bca(
    *,
    bucket_name: builtins.str,
    path: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28cd1eed876bb5ce18d7a856a3ae95302c3b6d6e1f40ab9bd4024fd3a8904c90(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76ce5152127f587d16544a2ac175f4e982bb63065400f5ddc6c60004d2573fff(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2417c14cbcfca7afb29f87612b113b47b6636007c6f1c8761cfa06adb3f6c195(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__168ef1727e8879e5ffbfb5a0057b4f55e674e78b1490866d21e03a12a5fcbc39(
    value: typing.Optional[StorageTransferJobTransferSpecGcsDataSource],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c89d601fc16d1ff8dc15b212f5492a253caf53dbc09ad74e6614b8c22e58a04e(
    *,
    path: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c5349d4a88fc3fcc95f0c828d7e5346bb85d9856309a4229098660fd53e6caf(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2d8c5e9bfd2f13d1760e593d8a219c84f81b223a98f7fecd5a5125747fe8789(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__47fb3a374d3dd832c941f003587de179563f065982f32195c90fc14b094170ec(
    value: typing.Optional[StorageTransferJobTransferSpecHdfsDataSource],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2098d774200ad0345b31686e4d7db166d8141faaf12387c218a9087babdfd19b(
    *,
    list_url: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b25b7ebf8ac225f9b1e3b1c942926e7691256c4f25071f9ec6c40b16eeaa122(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eae53a10506eac7a94ad96edbe8e3dc8497611488f254b76523a66404b8eac8d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__125bf4b1ee8c31afce7dabb178cd0dde980c45a955583fc111af99768748367c(
    value: typing.Optional[StorageTransferJobTransferSpecHttpDataSource],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__abc345f6867071ad7910365636724e3c70085cbde7732c594c382ed3a0aba63b(
    *,
    exclude_prefixes: typing.Optional[typing.Sequence[builtins.str]] = None,
    include_prefixes: typing.Optional[typing.Sequence[builtins.str]] = None,
    last_modified_before: typing.Optional[builtins.str] = None,
    last_modified_since: typing.Optional[builtins.str] = None,
    max_time_elapsed_since_last_modification: typing.Optional[builtins.str] = None,
    min_time_elapsed_since_last_modification: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed5f4e4be62599b31c22a8508e26b134deaa446e311a9eca33764409ef287329(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37198acc4a279eb626ff4a01f9fab5aadf9a2764aa01900997da848f8ed35c8d(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0c0f68382513c753e9412acaeaf89c3a74dc155de83c45b6c1d262e369e2ff3(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e169acc93896af2a19832fbfda04cb9f3ad6c7c5dca1b02b34265905aab8c1a5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a82a1061e301d213a597d155d27b66ab5ef1a407f0d879460590b60e497acdce(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f0bdfbe52c2c76cf4b881d7ae232b93b1555ea8af58406c51c7079e39632fda(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2eee49c17d5bda25dcb4e2e4feed574ce9c49116642da6a969e14ac3fb4e4aa0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2303a57990661f2d5543f6a61c14cb8288c46326ac1f30517cb9d8b09a9cca51(
    value: typing.Optional[StorageTransferJobTransferSpecObjectConditions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe7d007dae2fd9574de4c52509234d882253aa863992b2acb456fd886a16cdcb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b9ec6e74139e852776fe92e89db967a2bb8bc81d967784df59afa638b31fe27(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78e2ce8c9db511301ce32a5dcf0cd45f9b17970247ca8961b179362ce314bf12(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb15d07a2d4744a8b59f9bac46900a8f0865c2810fb24f8f36f31f1fe11f3166(
    value: typing.Optional[StorageTransferJobTransferSpec],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61ba7ff40892bfc17203cf46584d6dd8b4d9199db78bc4b070870741f19378ac(
    *,
    root_directory: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f8bc947a84d04a6e8771c850761cfb25ddb5cbc15dfe36ff5e827366c5b7bcb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7235633d6417ef7eef0c1255756cf122d6348c9d96d72b17e051d685c5a5993(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__347f8bd6d6a46fa3de77c0398d7b9ef3f0bafb4cdd8eaefc78872ef8cd456c1b(
    value: typing.Optional[StorageTransferJobTransferSpecPosixDataSink],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb57375009c266bf2e22183a93e97e46c0aa5b3f76293012435114556fa1d2f7(
    *,
    root_directory: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6ff6254e38587aa26350f21be3e495ede269b0b0450d929a94d4726cabba6e7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__434213e16d3f9e6afbf2466710bab1d0d2c59d8cd397ead4a6776d74c7fd00d0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1059c1ddafdcc893a15eb34fd13b94ae30820e22a01f27e5f9a9a90f0be72a51(
    value: typing.Optional[StorageTransferJobTransferSpecPosixDataSource],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__35dc738a77c2ccef9d8078757f150ae8799845ececeb8809535c55e0e4723796(
    *,
    delete_objects_from_source_after_transfer: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    delete_objects_unique_in_sink: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    metadata_options: typing.Optional[typing.Union[StorageTransferJobTransferSpecTransferOptionsMetadataOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    overwrite_objects_already_existing_in_sink: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    overwrite_when: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__06ca662aead81df30d51115ef7a8cd7e2e69bcd5749662866127fc92817af565(
    *,
    acl: typing.Optional[builtins.str] = None,
    gid: typing.Optional[builtins.str] = None,
    kms_key: typing.Optional[builtins.str] = None,
    mode: typing.Optional[builtins.str] = None,
    storage_class: typing.Optional[builtins.str] = None,
    symlink: typing.Optional[builtins.str] = None,
    temporary_hold: typing.Optional[builtins.str] = None,
    time_created: typing.Optional[builtins.str] = None,
    uid: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ccedf58d8e8feebac6d36241032e422a423a3d0974af27091242e6c58c7ec3fa(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__322abf62d753901b8968a1a856d5727b835fd28a77295218959cf28893f14025(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ddfa0f811c3240050e6ae16c974f2b96df3818d936d2d7f31a1dbe7fec8ff31(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__294126e609b81240b97cff9cc2dd8439f31ec74ab1063dbdef2f51f3f2defdfe(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44f7ac288acdd7fa1a4860f283f5e477793ea412beba33678c6b8f845a011552(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a617c66f113e77250955b160b067e790b79d15d590486de1fa4bc5076120f81f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d007f130950d870e1364d098b1b41eb1339a6aceb5309b854e0c97986acd01f5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a011a41deb42aaf045eddee7ca59de58223f036e6725b0e3c30c07369c5ba99c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5c6e6d21682a1a8e429cb8eb716e1e2951c95dc09c3d71be9ea142c8ffa1396(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e867becaaa2e9ef041d68e700cd924fd4098962346bd1c94a2c134d1274f7407(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a124c94b098be646371f7398cc0063443ac5c6f8a713e786d8fcad2276e05111(
    value: typing.Optional[StorageTransferJobTransferSpecTransferOptionsMetadataOptions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44fc6eacdfa1845c7dad6cd4f994e10d56336f4ceee480e536cb7d4c2b001cec(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ddcec5f5634f945fa6f30b0d15ddf1a3554cbc65815c9225f6bbbc5388e2d51(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d7dc5f9f10cf928487ef07c1cd001083527778f29bd841b606860ce345de00a7(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0c6bc1144bf0293571119beb0b84001601a70665636ee517f94591ee9d2bffa(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__532ff2556a017658406a7d0a1a99217d712433388e44c0fdb45530a86352df66(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d6b2e3b4c35ad897517af7d172af288e2abe4ca8c41ef59631bdc64e28a1417d(
    value: typing.Optional[StorageTransferJobTransferSpecTransferOptions],
) -> None:
    """Type checking stubs"""
    pass
