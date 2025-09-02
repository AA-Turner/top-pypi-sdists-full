from collections import OrderedDict
from typing import Any
from typing import Dict


async def search_raw(
    hub,
    ctx,
    name: str,
) -> Dict:
    """
    Provides a summarized description of the specified Kinesis data stream without the shard list. The information
    returned includes the stream name, Amazon Resource Name (ARN), status, record retention period, approximate
    creation time, monitoring, encryption details, and open shard count.

    Args:
        name(str):
            AWS Kinesis Stream name to uniquely identify the resource.

    Returns:
        {"result": True|False, "comment": A message List, "ret": Dict}

    """
    result = dict(comment=[], ret=None, result=True)
    ret = await hub.exec.boto3.client.kinesis.describe_stream_summary(
        ctx,
        StreamName=name,
    )
    result["result"] = ret["result"]
    result["comment"] = list(ret["comment"])
    result["ret"] = ret["ret"]
    return result


async def update(
    hub,
    ctx,
    name: str,
    current_state: Dict[str, Any],
    input_map: Dict[str, Any],
    resource_id: str,
    plan_state: Dict[str, Any],
    timeout: Dict[str, Any],
):
    """
    If the input supplied retention is less than the existing, here we decerase the Kinesis data stream's retention
    period, which is the length of time data records are accessible after they are added to the stream. The minimum
    value of a stream's retention period is 24 hours. This operation may result in lost data. For example, if the
    stream's retention period is 48 hours and is decreased to 24 hours, any data already in the stream that is older
    than 24 hours is inaccessible. Conversely, if the input retention is more than the existing, then we increase
    Kinesis data stream's retention period, which is the length of time data records are accessible after they are
    added to the stream. The maximum value of a stream's retention period is 8760 hours (365 days). If you choose a
    longer stream retention period, this operation increases the time period during which records that have not yet
    expired are accessible. However, it does not make previous, expired data (older than the stream's previous retention
     period) accessible after the operation has been called. For example, if a stream's retention period is set to 24
    hours and is increased to 168 hours, any data that is older than 24 hours remains inaccessible to consumer
    applications. Checks to see if enhanced monitoring needs to be enabled/ disabled for certain ShardLevelMetrics.
    Enables or updates server-side encryption using an Amazon Web Services KMS key for a specified stream. Starting/
    stopping encryption is an asynchronous operation. Upon receiving the request, Kinesis Data Streams returns
    immediately and sets the status of the stream to UPDATING . After the update is complete, Kinesis Data Streams sets
    the status of the stream back to ACTIVE . Updating or applying encryption normally takes a few seconds to complete,
    but it can take minutes. You can continue to read and write data to your stream while its status is UPDATING . Once
    status of the stream is ACTIVE , encryption begins for records written to the stream. API Limits: You can
    successfully apply a new Amazon Web Services KMS key for server-side encryption 25 times in a rolling 24-hour period.
    Note: It can take up to 5 seconds after the stream is in an ACTIVE status before all records written to the stream
    are encrypted. After you enable encryption, you can verify that encryption is applied by inspecting the API response
     from PutRecord or PutRecords. Disables server-side encryption for a specified stream. Updates the shard count of
    the specified stream to the specified number of shards.
    This operation has the following default limits. By default, you cannot do the following:
        a. Scale more than ten times per rolling 24-hour period per stream
        b. Scale up to more than double your current shard count for a stream
        c. Scale down below half your current shard count for a stream
        d. Scale up to more than 10000 shards in a stream
        e. Scale a stream with more than 10000 shards down unless the result is less than 10000 shards
        f. Scale up to more than the shard limit for your account

    Updates the capacity mode of the data stream. Currently, in Kinesis Data Streams, you can choose between an
    on-demand capacity mode and a provisioned capacity mode for your data stream.

    Args:
        name(str):
            The name of the AWS ElasticLoadBalancingv2 Listener.

        current_state(dict[str, Any]):
            response returned by describe on an AWS ElasticLoadBalancingv2 Listener

        input_map(dict[str, Any]):
            a dictionary with newly passed values of params.

        resource_id(str):
            AWS ElasticLoadBalancingv2 Listener Amazon Resource Name (ARN).

        plan_state(dict[str, Any]):
            idem --test state for update on AWS ElasticLoadBalancingv2 Listener.

        timeout(dict, Optional): Timeout configuration for waiting for Aws Certificate to get issued.
            * describe (Dict) -- Timeout configuration for describing certificate
                * delay (int, Optional): The amount of time in seconds to wait between attempts.
                * max_attempts (int, Optional): Customized timeout configuration containing delay and max attempts.
    Returns:
        {"result": True|False, "comment": A message List, "ret": None}
    """
    result = dict(comment=[], result=True, ret=[])
    if not ctx.get("test", False):
        if input_map.get("shard_count"):
            if current_state.get("shard_count") and (
                input_map.get("shard_count") != current_state.get("shard_count")
            ):
                update_shard_count = (
                    await hub.exec.boto3.client.kinesis.update_shard_count(
                        ctx,
                        StreamName=resource_id,
                        TargetShardCount=input_map.get("shard_count"),
                        ScalingType="UNIFORM_SCALING",
                    )
                )
                if not update_shard_count["result"] and not update_shard_count["ret"]:
                    result["comment"] = list(update_shard_count["comment"])
                    result["result"] = False
                    return result
                result["comment"].append("Updated Shard Count.")
                result["ret"].append(
                    {
                        "update_shard_count": update_shard_count["ret"].get(
                            "TargetShardCount"
                        )
                    }
                )
                waiter_ret = await hub.tool.aws.kinesis.stream.kinesis_waiter(
                    ctx, name, timeout, "update"
                )
                if not waiter_ret["result"]:
                    result["result"] = False
                    result["comment"] += waiter_ret["comment"]
                    return result

        if input_map.get("stream_mode_details"):
            if current_state.get("stream_mode_details") and (
                input_map.get("stream_mode_details")
                != current_state.get("stream_mode_details")
            ):
                update_stream_mode = (
                    await hub.exec.boto3.client.kinesis.update_stream_mode(
                        ctx,
                        StreamARN=input_map.get("arn"),
                        StreamModeDetails=input_map.get("stream_mode_details"),
                    )
                )
                if not update_stream_mode["result"] and not update_stream_mode["ret"]:
                    result["comment"] = list(update_stream_mode["comment"])
                    result["result"] = False
                    return result
                result["comment"].append("Updated Stream Mode.")
                result["ret"].append(
                    {"update_stream_mode": input_map.get("stream_mode_details")}
                )
                waiter_ret = await hub.tool.aws.kinesis.stream.kinesis_waiter(
                    ctx, name, timeout, "update"
                )
                if not waiter_ret["result"]:
                    result["result"] = False
                    result["comment"] += waiter_ret["comment"]
                    return result

        if input_map.get("retention_period_hours"):
            current_retention_period = current_state.get("retention_period_hours")
            if current_retention_period != input_map.get("retention_period_hours"):
                if current_retention_period < input_map.get("retention_period_hours"):
                    increase_period = await hub.exec.boto3.client.kinesis.increase_stream_retention_period(
                        ctx,
                        StreamName=resource_id,
                        RetentionPeriodHours=input_map.get("retention_period_hours"),
                    )
                    if not increase_period["result"] and not increase_period["ret"]:
                        result["comment"] = list(increase_period["comment"])
                        result["result"] = False
                        return result
                    result["comment"].append("Increased Retention Period.")
                    result["ret"].append(
                        {
                            "increase_stream_retention_period": input_map.get(
                                "retention_period_hours"
                            )
                        }
                    )
                    waiter_ret = await hub.tool.aws.kinesis.stream.kinesis_waiter(
                        ctx, name, timeout, "update"
                    )
                    if not waiter_ret["result"]:
                        result["result"] = False
                        result["comment"] += waiter_ret["comment"]
                        return result

                else:
                    decrease_period = await hub.exec.boto3.client.kinesis.decrease_stream_retention_period(
                        ctx,
                        StreamName=resource_id,
                        RetentionPeriodHours=input_map.get("retention_period_hours"),
                    )
                    if not decrease_period["result"] and not decrease_period["ret"]:
                        result["comment"] = list(decrease_period["comment"])
                        result["result"] = False
                        return result
                    result["comment"].append("Decreased Retention Period.")
                    result["ret"].append(
                        {
                            "decrease_stream_retention_period": input_map.get(
                                "retention_period_hours"
                            )
                        }
                    )
                    waiter_ret = await hub.tool.aws.kinesis.stream.kinesis_waiter(
                        ctx, name, timeout, "update"
                    )
                    if not waiter_ret["result"]:
                        result["result"] = False
                        result["comment"] += waiter_ret["comment"]
                        return result

        if input_map.get("shard_level_metrics"):
            if not current_state.get("shard_level_metrics") or set(
                current_state.get("shard_level_metrics")
            ) != set(input_map.get("shard_level_metrics")):
                to_disable = list(
                    set(current_state.get("shard_level_metrics", []))
                    - set(input_map.get("shard_level_metrics"))
                )
                to_enable = list(
                    set(input_map.get("shard_level_metrics"))
                    - set(current_state.get("shard_level_metrics", []))
                )

                if to_disable:
                    disable_metrics = (
                        await hub.exec.boto3.client.kinesis.disable_enhanced_monitoring(
                            ctx,
                            StreamName=resource_id,
                            ShardLevelMetrics=to_disable,
                        )
                    )
                    if not disable_metrics["result"]:
                        result["comment"] += list(disable_metrics["comment"])
                        result["result"] = False
                        return result
                    result["comment"].append(
                        "Disabled Enhanced Monitoring for ShardLevelMetrics."
                    )
                    result["ret"].append(
                        {
                            "disable_metrics": disable_metrics["ret"][
                                "DesiredShardLevelMetrics"
                            ]
                        }
                    )
                    waiter_ret = await hub.tool.aws.kinesis.stream.kinesis_waiter(
                        ctx, name, timeout, "update"
                    )
                    if not waiter_ret["result"]:
                        result["result"] = False
                        result["comment"] += waiter_ret["comment"]
                        return result

                if to_enable:
                    enable_metrics = (
                        await hub.exec.boto3.client.kinesis.enable_enhanced_monitoring(
                            ctx,
                            StreamName=resource_id,
                            ShardLevelMetrics=to_enable,
                        )
                    )
                    if not enable_metrics["result"]:
                        result["comment"] += list(enable_metrics["comment"])
                        result["result"] = False
                        return result
                    result["comment"].append(
                        "Enabled Enhanced Monitoring for ShardLevelMetrics."
                    )
                    result["ret"].append(
                        {
                            "enable_metrics": enable_metrics["ret"][
                                "DesiredShardLevelMetrics"
                            ]
                        }
                    )
                    waiter_ret = await hub.tool.aws.kinesis.stream.kinesis_waiter(
                        ctx, name, timeout, "update"
                    )
                    if not waiter_ret["result"]:
                        result["result"] = False
                        result["comment"] += waiter_ret["comment"]
                        return result

        if input_map.get("encryption_type"):
            if input_map.get("encryption_type") == "NONE":
                if current_state.get("encryption_type") == "KMS":
                    stop_encryption = (
                        await hub.exec.boto3.client.kinesis.stop_stream_encryption(
                            ctx,
                            StreamName=resource_id,
                            EncryptionType="KMS",
                            KeyId=input_map.get("key_id"),
                        )
                    )
                    if not stop_encryption["result"]:
                        result["comment"] += list(stop_encryption["comment"])
                        result["result"] = False
                        return result
                    result["comment"].append("Stopped Stream Encryption.")
                    result["ret"].append(
                        {"stop_stream_encryption": input_map.get("encryption_type")}
                    )
                    waiter_ret = await hub.tool.aws.kinesis.stream.kinesis_waiter(
                        ctx, name, timeout, "update"
                    )
                    if not waiter_ret["result"]:
                        result["result"] = False
                        result["comment"] += waiter_ret["comment"]
                        return result

            elif input_map.get("encryption_type") == "KMS":
                if current_state.get("encryption_type") == "NONE":
                    start_encryption = (
                        await hub.exec.boto3.client.kinesis.start_stream_encryption(
                            ctx,
                            StreamName=resource_id,
                            EncryptionType="KMS",
                            KeyId=input_map.get("key_id"),
                        )
                    )
                    if not start_encryption["result"]:
                        result["comment"] += list(start_encryption["comment"])
                        result["result"] = False
                        return result
                    result["comment"].append("Started Stream Encryption.")
                    result["ret"].append(
                        {"start_stream_encryption": input_map.get("encryption_type")}
                    )
                    waiter_ret = await hub.tool.aws.kinesis.stream.kinesis_waiter(
                        ctx, name, timeout, "update"
                    )
                    if not waiter_ret["result"]:
                        result["result"] = False
                        result["comment"] += waiter_ret["comment"]
                        return result

                else:
                    if current_state.get("key_id") != input_map.get("key_id"):
                        start_encryption = (
                            await hub.exec.boto3.client.kinesis.start_stream_encryption(
                                ctx,
                                StreamName=resource_id,
                                EncryptionType="KMS",
                                KeyId=input_map.get("key_id"),
                            )
                        )
                        if not start_encryption["result"]:
                            result["comment"] += list(start_encryption["comment"])
                            result["result"] = False
                            return result
                        result["comment"].append("Started Stream Encryption.")
                        result["ret"].append(
                            {
                                "start_stream_encryption": input_map.get(
                                    "encryption_type"
                                )
                            }
                        )
                        waiter_ret = await hub.tool.aws.kinesis.stream.kinesis_waiter(
                            ctx, name, timeout, "update"
                        )
                        if not waiter_ret["result"]:
                            result["result"] = False
                            result["comment"] += waiter_ret["comment"]
                            return result
    else:
        update_params = OrderedDict(
            {
                "name": name,
                "shard_count": input_map.get("shard_count"),
                "stream_mode_details": input_map.get("stream_mode_details"),
                "shard_level_metrics": input_map.get("shard_level_metrics"),
                "retention_period_hours": input_map.get("retention_period_hours"),
                "encryption_type": input_map.get("encryption_type"),
                "key_id": input_map.get("key_id"),
                "resource_id": resource_id,
                "tags": input_map.get("tags"),
            }
        )
        for key, value in update_params.items():
            if value is not None:
                plan_state[key] = value
        result["ret"] = plan_state
    return result


async def kinesis_waiter(
    hub,
    ctx,
    name: str,
    timeout: Dict,
    operation_type: str,
    waiter_type: str = None,
):
    """

    Waiter to wait for the Kinesis Stream to become active.

        Args:
           name(str): An Idem name of the resource.
           timeout(Dict, Optional): Timeout configuration for creating or updating Kinesis Stream.
            * create (Dict) -- Timeout configuration for creating Kinesis Stream
                * delay(int, default=10) -- The amount of time in seconds to wait between attempts.
                * max_attempts(int, default=18) -- Customized timeout configuration containing delay and max attempts.
            * update (str) -- Timeout configuration for updating Kinesis Stream
                * delay(int, default=10) -- The amount of time in seconds to wait between attempts.
                * max_attempts(int, default=18) -- Customized timeout configuration containing delay and max attempts.
            * operation_type(str): create or update operation
            * waiter_type(str): StreamNotExists or StreamExists

        Returns:
            Dict[str, Any]
    """

    result = dict(comment=[], result=True, ret={})
    if not waiter_type:
        waiter_type = "stream_exists"
    waiter_config = hub.tool.aws.waiter_utils.create_waiter_config(
        default_delay=10,
        default_max_attempts=18,
        timeout_config=timeout.get(operation_type) if timeout else None,
    )
    hub.log.debug(f"Waiting on aws.kinesis.stream '{name}' to become active")
    try:
        await hub.tool.boto3.client.wait(
            ctx,
            "kinesis",
            waiter_type,
            StreamName=name,
            WaiterConfig=waiter_config,
        )
    except Exception as e:
        result["comment"] += list(str(e))
        result["result"] = False
    return result
