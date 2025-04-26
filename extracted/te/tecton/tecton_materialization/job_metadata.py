# This is Spark specific job_metadata module. See common.job_metadata for common functions

import logging
import time
from typing import Optional

from tecton_core.id_helper import IdHelper
from tecton_materialization.common.job_metadata import IDEMPOTENCE_KEY_ATTRIBUTE
from tecton_materialization.common.job_metadata import LAST_UPDATED_ATTRIBUTE
from tecton_materialization.common.job_metadata import RUN_ID_PREFIX
from tecton_materialization.common.job_metadata import TTL_ATTRIBUTE
from tecton_materialization.common.job_metadata import TTL_DURATION_SECONDS
from tecton_materialization.common.job_metadata import VALUE_ATTRIBUTE
from tecton_materialization.common.job_metadata import JobMetadataClient
from tecton_materialization.materialization_utils import get_statsd_client
from tecton_proto.materialization.job_metadata__client_pb2 import JobMetadata
from tecton_proto.materialization.job_metadata__client_pb2 import JobMetadataTableType


__all__ = (
    "write_checkpoint",
    "is_checkpoint_complete",
    "check_spark_job_uniqueness",
)

try:
    import boto3
    from botocore.errorfactory import ClientError

    from tecton_materialization.common.job_metadata_aws import _dynamodb_client
except ImportError:
    # not available and unused in dataproc
    boto3 = None
    ClientError = None
    _dynamodb_client = None

logger = logging.getLogger(__name__)


# TODO(Alex): Migrate checkpointing into JMT
# We use task as the idempotence key for checkpointing because we don't need to recompute the same tiles already processed within the same task.
# In a different task, they may correspond to a different store type, or be an overwrite, so we'd want to still process them.
# The run_id isn't required but could be useful for debugging.
def write_checkpoint(spark, materialization_task_params, anchor_time, run_id):
    dynamodb = _dynamodb_client(materialization_task_params)
    table = materialization_task_params.spark_job_execution_table
    idempotence_key = materialization_task_params.materialization_task_id + "@" + str(anchor_time)
    now_seconds = int(time.time())
    statsd_client = get_statsd_client(spark)
    dynamodb.put_item(
        TableName=table,
        Item={
            IDEMPOTENCE_KEY_ATTRIBUTE: {"S": idempotence_key},
            VALUE_ATTRIBUTE: {"S": f"{RUN_ID_PREFIX}{run_id}"},
            TTL_ATTRIBUTE: {"N": str(now_seconds + TTL_DURATION_SECONDS)},
            LAST_UPDATED_ATTRIBUTE: {"N": str(now_seconds)},
        },
    )
    statsd_client.incr("materialization.checkpoint_write", 1)


def is_checkpoint_complete(spark, materialization_task_params, anchor_time):
    dynamodb = _dynamodb_client(materialization_task_params)
    table = materialization_task_params.spark_job_execution_table
    idempotence_key = materialization_task_params.materialization_task_id + "@" + str(anchor_time)
    now_seconds = int(time.time())
    statsd_client = get_statsd_client(spark)
    try:
        dynamodb.put_item(
            TableName=table,
            Item={
                IDEMPOTENCE_KEY_ATTRIBUTE: {"S": idempotence_key},
                VALUE_ATTRIBUTE: {"S": ""},
                TTL_ATTRIBUTE: {"N": str(now_seconds + TTL_DURATION_SECONDS)},
                LAST_UPDATED_ATTRIBUTE: {"N": str(now_seconds)},
            },
            ConditionExpression=f"attribute_not_exists({IDEMPOTENCE_KEY_ATTRIBUTE}) OR #val = :val",
            ExpressionAttributeNames={"#val": VALUE_ATTRIBUTE},
            ExpressionAttributeValues={":val": {"S": ""}},
        )
        statsd_client.incr("materialization.checkpoint_check_incomplete", 1)
        return False
    except ClientError as e:
        # Condition failed means we've previously committed the checkpoint
        if e.response["Error"]["Code"] == "ConditionalCheckFailedException":
            statsd_client.incr("materialization.checkpoint_check_complete", 1)
            return True
        else:
            raise e


def check_spark_job_uniqueness(
    materialization_task_params,
    run_id,
    spark,
    step,
    skip_legacy_execution_table_check,
    job_metadata_client: JobMetadataClient,
):
    if step not in (1, None):
        return
    if (
        not skip_legacy_execution_table_check
        and materialization_task_params.job_metadata_table_type != JobMetadataTableType.JOB_METADATA_TABLE_TYPE_GCS
    ):
        dynamodb = _dynamodb_client(materialization_task_params)
        table = materialization_task_params.spark_job_execution_table
        idempotence_key = materialization_task_params.idempotence_key

        # TODO: remove once job_metadata_table is enabled everywhere
        statsd_client = get_statsd_client(spark)
        try:
            existing_record = dynamodb.get_item(
                TableName=table,
                Key={IDEMPOTENCE_KEY_ATTRIBUTE: {"S": idempotence_key}},
                ConsistentRead=True,
            ).get("Item", None)
            statsd_client.incr("materialization.dynamo_get_item_success", 1)
        except ClientError:
            existing_record = None
            statsd_client.incr("materialization.dynamo_get_item_errors", 1)

        try:
            now_seconds = int(time.time())
            dynamodb.put_item(
                TableName=table,
                Item={
                    IDEMPOTENCE_KEY_ATTRIBUTE: {"S": idempotence_key},
                    VALUE_ATTRIBUTE: {"S": f"{RUN_ID_PREFIX}{run_id}"},
                    TTL_ATTRIBUTE: {"N": str(now_seconds + TTL_DURATION_SECONDS)},
                    LAST_UPDATED_ATTRIBUTE: {"N": str(now_seconds)},
                },
                ConditionExpression=f"attribute_not_exists({IDEMPOTENCE_KEY_ATTRIBUTE})",
            )
        except ClientError as e:
            if e.response["Error"]["Code"] == "ConditionalCheckFailedException":
                if existing_record:
                    logger.error(f"Existing Spark unique key record found: {existing_record}")
                else:
                    logger.error(f"Conditional check failed, but no record found for {idempotence_key}")
                msg = f"Value is already set for idempotence_key: {idempotence_key}"
                raise RuntimeError(msg) from e
            raise e

    # TODO: remove above code and remove jobidempotencemanager code once NEW_JOB_EXECUTION_TABLE migration is done
    # after all customers have dynamodb:GetItem permission
    def updater(job_metadata: JobMetadata) -> Optional[JobMetadata]:
        new_proto = JobMetadata()
        new_proto.CopyFrom(job_metadata)
        if new_proto.spark_execution_info.HasField("run_id"):
            attempt_id = IdHelper.to_string(materialization_task_params.attempt_id)
            msg = f"Value is already set for attempt_id: {attempt_id}: {new_proto.spark_execution_info.run_id}"
            raise RuntimeError(msg)
        elif new_proto.spark_execution_info.is_revoked:
            msg = "Job cancelled by orchestrator before lock acquired"
            raise RuntimeError(msg)
        new_proto.spark_execution_info.run_id = run_id
        return new_proto

    if materialization_task_params.HasField("job_metadata_table"):
        job_metadata_client.update(updater)
