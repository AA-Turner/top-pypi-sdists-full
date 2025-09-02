""" State module for managing Kinesis Stream. """
import copy
from dataclasses import field
from dataclasses import make_dataclass
from typing import Any
from typing import Dict
from typing import List

__contracts__ = ["resource"]

ENCRYPTION_KMS_TYPE = "KMS"


async def present(
    hub,
    ctx,
    name: str,
    resource_id: str = None,
    shard_count: int = None,
    stream_mode_details: make_dataclass(
        "StreamModeDetails", [("StreamMode", str)]
    ) = None,
    shard_level_metrics: List = None,
    retention_period_hours: int = None,
    encryption_type: str = None,
    key_id: str = None,
    stream_arn: str = None,
    tags: Dict[str, str] = None,
    timeout: make_dataclass(
        "Timeout",
        [
            (
                "create",
                make_dataclass(
                    "CreateTimeout",
                    [
                        ("delay", int, field(default=10)),
                        ("max_attempts", int, field(default=18)),
                    ],
                ),
                field(default=None),
            ),
            (
                "update",
                make_dataclass(
                    "UpdateTimeout",
                    [
                        ("delay", int, field(default=18)),
                        ("max_attempts", int, field(default=18)),
                    ],
                ),
                field(default=None),
            ),
        ],
    ) = None,
) -> Dict[str, Any]:
    """Creates a Kinesis data stream. A stream captures and transports data records that are continuously emitted from
    different data sources or producers.

    Scale-out within a stream is explicitly supported by means of shards, which are uniquely identified groups of data
    records in a stream. You specify and control the number of shards that a stream is composed of. Each shard can
    support reads up to five transactions per second, up to a maximum data read total of 2 MiB per second. Each shard
    can support writes up to 1,000 records per second, up to a maximum data write total of 1 MiB per second. If the
    amount of data input increases or decreases, you can add or remove shards. The stream name identifies the stream.
    The name is scoped to the Amazon Web Services account used by the application. It is also scoped by Amazon Web
    Services Region. That is, two streams in two different accounts can have the same name, and two streams in the same
    account, but in two different Regions, can have the same name. CreateStream is an asynchronous operation. Upon
    receiving a CreateStream request, Kinesis Data Streams immediately returns and sets the stream status to CREATING.
    After the stream is created, Kinesis Data Streams sets the stream status to ACTIVE. You should perform read and
    write operations only on an ACTIVE stream. Enables enhanced Kinesis data stream monitoring for shard-level metrics.

    You receive a LimitExceededException when making a CreateStream request when you try to do one of the following:
        a. Have more than five streams in the CREATING state at any point in time.
        b. Create more shards than are authorized for your account.

    Args:
        name(str):
            An Idem name of the resource.

        resource_id(str, Optional):
            An identifier of the resource in the provider. Defaults to None.

        shard_count(int, Optional):
            The number of shards that the stream will use. The throughput of the stream is a function of the number of
            shards; more shards are required for greater provisioned throughput. Defaults to None.

        stream_mode_details(dict[str, Any], Optional):
            Indicates the capacity mode of the data stream. Currently, in Kinesis Data Streams, you can choose between
            an on-demand capacity mode and a provisioned capacity mode for your data streams. Defaults to None.

                * StreamMode (str):
                    Specifies the capacity mode to which you want to set your data stream. Currently, in KinesisData
                    Streams, you can choose between an on-demand capacity mode and a provisioned capacity mode for your
                    data streams.

        shard_level_metrics(list, Optional):
            List of shard-level metrics to disable/ enable. The following are the valid shard-level metrics.
            The value "ALL" enables every metric.
                * IncomingBytes
                * IncomingRecords
                * OutgoingBytes
                * OutgoingRecords
                * WriteProvisionedThroughputExceeded
                * ReadProvisionedThroughputExceeded
                * IteratorAgeMilliseconds
                * ALL

        retention_period_hours(int, Optional):
            IncreaseStreamRetentionPeriod:
                1. Increases the Kinesis data stream's retention period, which is the length of time data records are
                   accessible after they are added to the stream.
                2. If you choose a longer stream retention period, this operation increases the time period during which
                   records that have not yet expired are accessible.
                3. However, it does not make previous, expired data (older than the stream's previous retention period)
                   accessible after the operation has been called.
                4. For example, if a stream's retention period is set to 24 hours and is increased to 168 hours, any
                   data that is older than 24 hours remains inaccessible to consumer applications.

            DecreaseStreamRetentionPeriod:
                1. Decreases the Kinesis data stream's retention period, which is the length of time data records are
                   accessible after they are added to the stream. The minimum value of a stream's retention period is 24
                   hours.

                2. This operation may result in lost data. For example, if the stream's retention period is 48 hours and
                   is decreased to 24 hours, any data already in the stream that is older than 24 hours is inaccessible.

            * The maximum value of a stream's retention period is 8760 hours (365 days).
            * The minimum value of a stream's retention period is 24 hours.

        encryption_type(str, Optional):
            The encryption type to use. The only valid value is KMS .

        key_id (str, Optional):
            The GUID for the customer-managed Amazon Web Services KMS key to use for encryption. This value can
            be a globally unique identifier, a fully specified Amazon Resource Name (ARN) to either an alias or
            a key, or an alias name prefixed by "alias/".

            You can also use a master key owned by Kinesis Data Streams by specifying the alias aws/kinesis.
                * Key ARN example:
                    arn:aws:kms:us-east-1:45678908712456908:key/1818191-7839-9034-3456-45678908712456908
                * Alias ARN example:
                    arn:aws:kms:us-east-1:45678908712456908:alias/MyAliasName
                * Globally unique key ID example:
                    181910-119191-9034-3456-45678908712456908
                * Alias name example:
                    alias/MyAliasName
                * Master key owned by Kinesis Data Streams:
                    alias/aws/kinesis

        stream_arn(str, Optional):
            Specifies the ARN of the data stream whose capacity mode you want to update.

        tags(dict[str, str], Optional):
            The tags to assign to the stream. Defaults to None.
                * Key (str): The key of the tag.
                * Value (str, Optional): The value of the tag.

        timeout(dict, Optional):
            Timeout configuration for AWS Kinesis Stream.

            * create (*dict, Optional*):
                Timeout configuration when creating an AWS Kinesis Stream.

                * delay (*int, Optional*):
                    The amount of time in seconds to wait between attempts. Default value is ``10``.
                * max_attempts (*int, Optional*):
                    Max attempts of waiting for change. Default value is ``18``.

            * update (*dict, Optional*):
                Timeout configuration when updating an AWS Kinesis Stream.

                * delay (*int, Optional*):
                    The amount of time in seconds to wait between attempts. Default value is ``10``.
                * max_attempts (*int, Optional*):
                    Max attempts of waiting for change. Default value is ``18``.


    Request Syntax:
        .. code-block:: sls

            [stream-name]:
              aws.kinesis.stream.present:
                - name: "string"
                - shard_count: "int"
                - resource_id: "string"
                - stream_mode_details: "list"
                - shard_level_metrics: "list"
                - retention_period_hours: "int"
                - encryption_type: "string"
                - key_id: "string"
                - tags:
                    - 'string': "string"
                - timeout:
                    create:
                      delay: int
                      max_attemps: int
                    update:
                      delay: int
                      max_attemps: int


    Returns:
      Dict[str, Any]

    Examples:
        .. code-block:: sls

            stream_is_present:
              aws.kinesis.stream.present:
                - name: 'my-stream'
                - resource_id: 'arn:aws:kinesis:us-west-2:740563969943:stream/test-stream'
                - shard_count: 123
                - stream_mode_details:
                    StreamMode: PROVISIONED
                - shard_level_metrics:
                    - IncomingBytes
                    - IncomingRecords
                    - OutgoingBytes
                    - OutgoingRecords
                    - WriteProvisionedThroughputExceeded
                    - ReadProvisionedThroughputExceeded
                    - IteratorAgeMilliseconds
                    - ALL
                - retention_period_hours: 123
                - encryption_type: 'KMS'
                - key_id: arn:aws:kms:us-east-1:908738389389012:key/234590-7839-9034-3456-9087389389012
                - tags:
                    name: my-stream
                - timeout:
                    create:
                        delay: 10
                        max_attempts: 18
                    update:
                        delay: 10
                        max_attempts: 18
    """
    result = dict(comment=[], old_state=None, new_state=None, name=name, result=True)
    plan_state = {}
    before = None
    resource_updated = False
    if resource_id:
        before = await hub.exec.aws.kinesis.stream.get(
            ctx=ctx, name=name, resource_id=resource_id
        )
        if not before["result"] or not before["ret"]:
            result["result"] = False
            result["comment"] = before["comment"]
            return result
        result["old_state"] = copy.deepcopy(before["ret"])
        plan_state = copy.deepcopy(result["old_state"])
        input_params = {
            "shard_count": shard_count,
            "shard_level_metrics": shard_level_metrics,
            "stream_mode_details": stream_mode_details,
            "retention_period_hours": retention_period_hours,
            "encryption_type": encryption_type,
            "key_id": key_id,
            "tags": tags,
            "arn": stream_arn,
        }
        update_return = await hub.tool.aws.kinesis.stream.update(
            ctx=ctx,
            name=name,
            current_state=result["old_state"],
            input_map=input_params,
            plan_state=plan_state,
            resource_id=resource_id,
            timeout=timeout,
        )
        result["comment"] = update_return["comment"]
        if not update_return["result"]:
            result["result"] = False
            return result
        resource_updated = bool(update_return["ret"])
        if resource_updated:
            if ctx.get("test", False):
                result["comment"] += hub.tool.aws.comment_utils.would_update_comment(
                    resource_type="aws.kinesis.stream", name=name
                )
            else:
                result["comment"] += hub.tool.aws.comment_utils.update_comment(
                    resource_type="aws.kinesis.stream", name=name
                )

        if tags is not None and tags != result["old_state"].get("tags"):
            # Update tags
            update_tags = await hub.tool.aws.kinesis.tag.update(
                ctx=ctx,
                resource_id=resource_id,
                old_tags=result["old_state"]["tags"],
                new_tags=tags,
            )
            result["comment"] += update_tags["comment"]
            result["result"] = update_tags["result"]
            resource_updated = resource_updated or bool(update_tags["ret"])
            if ctx.get("test", False) and update_tags["ret"]:
                plan_state["tags"] = update_tags["ret"]
    else:
        if ctx.get("test", False):
            result["new_state"] = hub.tool.aws.test_state_utils.generate_test_state(
                enforced_state={},
                desired_state={
                    "name": name,
                    "shard_count": shard_count,
                    "stream_mode_details": stream_mode_details,
                    "shard_level_metrics": shard_level_metrics,
                    "retention_period_hours": retention_period_hours,
                    "encryption_type": encryption_type,
                    "key_id": key_id,
                    "tags": tags,
                },
            )
            result["comment"] = hub.tool.aws.comment_utils.would_create_comment(
                resource_type="aws.kinesis.stream", name=name
            )
            return result
        ret = await hub.exec.boto3.client.kinesis.create_stream(
            ctx,
            StreamName=name,
            ShardCount=shard_count,
            StreamModeDetails=stream_mode_details,
        )
        if not ret["result"] and not ret["ret"]:
            result["comment"] = ret["comment"]
            result["result"] = False
            return result
        result["comment"] = hub.tool.aws.comment_utils.create_comment(
            resource_type="aws.kinesis.stream", name=name
        )
        resource_id = name

        waiter_ret = await hub.tool.aws.kinesis.stream.kinesis_waiter(
            ctx, name, timeout, "create"
        )
        if not waiter_ret["result"]:
            result["result"] = False
            result["comment"] += [waiter_ret["comment"]]
            return result

        if tags:
            ret = await hub.exec.boto3.client.kinesis.add_tags_to_stream(
                ctx,
                StreamName=resource_id,
                Tags=tags,
            )
            if not ret["result"] and not ret["ret"]:
                result["comment"] += [ret["comment"]]
                result["result"] = False
                return result
            result["comment"] += ["Added tags to Stream."]

        if encryption_type is not None and encryption_type == ENCRYPTION_KMS_TYPE:
            if key_id:
                ret = await hub.exec.boto3.client.kinesis.start_stream_encryption(
                    ctx,
                    StreamName=resource_id,
                    EncryptionType=encryption_type,
                    KeyId=key_id,
                )
                if not ret["result"] and not ret["ret"]:
                    result["comment"] += ret["comment"]
                    result["result"] = False
                    return result
                result["comment"] += ["Stream encryption started."]
                waiter_ret = await hub.tool.aws.kinesis.stream.kinesis_waiter(
                    ctx, name, timeout, "create"
                )
                if not waiter_ret["result"]:
                    result["result"] = False
                    result["comment"] += waiter_ret["comment"]
                    return result

        if shard_level_metrics:
            enable_metrics = (
                await hub.exec.boto3.client.kinesis.enable_enhanced_monitoring(
                    ctx,
                    StreamName=resource_id,
                    ShardLevelMetrics=shard_level_metrics,
                )
            )
            if not enable_metrics["result"]:
                result["comment"] += enable_metrics["comment"]
                result["result"] = False
                return result
            result["comment"] += ["Enabled Enhanced Monitoring for ShardLevelMetrics."]
            waiter_ret = await hub.tool.aws.kinesis.stream.kinesis_waiter(
                ctx, name, timeout, "create"
            )
            if not waiter_ret["result"]:
                result["result"] = False
                result["comment"] += waiter_ret["comment"]
                return result

    if ctx.get("test", False):
        result["new_state"] = plan_state
    elif (not result["old_state"]) or resource_updated:
        after = await hub.exec.aws.kinesis.stream.get(
            ctx=ctx, name=name, resource_id=resource_id
        )
        if not after["result"] or not after["ret"]:
            result["result"] = False
            result["comment"] += after["comment"]
            return result
        result["new_state"] = copy.deepcopy(after["ret"])
    else:
        result["new_state"] = copy.deepcopy(result["old_state"])
    return result


async def absent(
    hub,
    ctx,
    name: str,
    resource_id: str = None,
    enforce_consumer_deletion: bool = None,
    timeout: make_dataclass(
        "Timeout",
        [
            (
                "delete",
                make_dataclass(
                    "DeleteTimeout",
                    [
                        ("delay", int, field(default=10)),
                        ("max_attempts", int, field(default=18)),
                    ],
                ),
                field(default=None),
            )
        ],
    ) = None,
) -> Dict[str, Any]:
    """Deletes a Kinesis data stream and all its shards and data. You must shut down any applications that are
    operating on the stream before you delete the stream.

    If an application attempts to operate on a deleted stream, it receives the exception ResourceNotFoundException. If
    the stream is in the ACTIVE state, you can delete it. After a DeleteStream request, the specified stream is in the
    DELETING state until Kinesis Data Streams completes the deletion.

    Note: Kinesis Data Streams might continue to accept data read and write operations, such as PutRecord, PutRecords,
    and GetRecords, on a stream in the DELETING state until the stream deletion is complete.

    When you delete a stream, any shards in that stream are also deleted, and any tags are dissociated from the stream.
    You can use the DescribeStreamSummary operation to check the state of the stream, which is returned in StreamStatus.
    DeleteStream has a limit of five transactions per second and per account.

    Args:
        name(str):
            An Idem name of the resource.

        resource_id(str, Optional):
            An identifier of the resource in the provider.

        enforce_consumer_deletion(bool, Optional):
            If this parameter is unset (null) or if you set it to false, and the stream has registered consumers, the
            call to DeleteStream fails with a ResourceInUseException. Defaults to None.

        timeout(dict, Optional):
            Timeout configuration for AWS Kinesis Stream.

            * delete (*dict, Optional*):
                Timeout configuration when deleting an AWS Kinesis Stream.

                * delay (*int, Optional*):
                    The amount of time in seconds to wait between attempts. Default value is ``10``.
                * max_attempts (*int, Optional*):
                    Max attempts of waiting for change. Default value is ``18``.

    Request Syntax:
      .. code-block:: sls

           [stream-name]:
              aws.kinesis.stream.absent:
                - name: "string"
                - resource_id: "string"
                - enforce_consumer_deletion: "boolean"
                - timeout:
                    delete:
                      delay: int
                      max_attemps: int

    Returns:
      Dict[str, Any]

    Examples:
        .. code-block:: sls

            resource_is_absent:
              aws.kinesis.stream.absent:
                - name: value
                - resource_id: value
                - enforce_consumer_deletion: TRUE|FALSE
    """
    result = dict(comment=[], old_state=None, new_state=None, name=name, result=True)
    if not resource_id:
        result["comment"] = hub.tool.aws.comment_utils.already_absent_comment(
            resource_type="aws.kinesis.stream", name=name
        )
        return result
    before = await hub.exec.aws.kinesis.stream.get(
        ctx=ctx, name=name, resource_id=resource_id
    )
    if not before["result"]:
        result["comment"] = before["comment"]
        result["result"] = False
        return result

    if not before["ret"]:
        result["comment"] = hub.tool.aws.comment_utils.already_absent_comment(
            resource_type="aws.kinesis.stream", name=name
        )
    else:
        result["old_state"] = before["ret"]
        if ctx.get("test", False):
            result["comment"] = hub.tool.aws.comment_utils.would_delete_comment(
                resource_type="aws.kinesis.stream", name=name
            )
            return result
        else:
            ret = await hub.exec.boto3.client.kinesis.delete_stream(
                ctx,
                StreamName=resource_id,
                EnforceConsumerDeletion=enforce_consumer_deletion,
            )
            if not ret["result"]:
                result["comment"] = before["comment"]
                result["result"] = False
                return result
            result["comment"] = hub.tool.aws.comment_utils.delete_comment(
                resource_type="aws.kinesis.stream", name=name
            )
            waiter_ret = await hub.tool.aws.kinesis.stream.kinesis_waiter(
                ctx,
                name,
                timeout,
                "delete",
                waiter_type="stream_not_exists",
            )
            if not waiter_ret["result"]:
                result["result"] = False
                result["comment"] += waiter_ret["comment"]
                return result
    return result


async def describe(hub, ctx) -> Dict[str, Dict[str, Any]]:
    """Pass required params to get a Kinesis stream resource.

    Describe the resource in a way that can be recreated/managed with the corresponding "present" function.

    Returns:
        Dict[str, Any]

    Examples:
        .. code-block:: bash

            $ idem describe aws.kinesis.stream
    """
    result = {}
    streams = await hub.exec.boto3.client.kinesis.list_streams(ctx)
    if not streams["result"]:
        hub.log.warning(
            f"Could not describe aws.kinesis.stream(s): {streams['comment']}"
        )
        return result

    if streams["ret"].get("StreamNames"):
        for stream in streams["ret"].get("StreamNames"):
            stream_summary = await hub.exec.aws.kinesis.stream.get(
                ctx=ctx, name=stream, resource_id=stream
            )
            if not stream_summary["result"]:
                hub.log.debug(
                    f"Could not describe aws.kinesis.stream '{stream}: {stream_summary['comment']}"
                )
                continue
            resource_converted = stream_summary["ret"]
            result[resource_converted["resource_id"]] = {
                "aws.kinesis.stream.present": [
                    {parameter_key: parameter_value}
                    for parameter_key, parameter_value in resource_converted.items()
                ]
            }
    return result
