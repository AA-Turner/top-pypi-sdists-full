"""
Plugin for aws enforced state management
"""
import copy
import json
import pathlib
from typing import Any
from typing import Dict

import botocore.exceptions
from dict_tools.data import NamespaceDict


def __init__(hub):
    hub.esm.aws.ACCT = ["aws"]


async def get_state(hub, ctx) -> Dict[str, Any]:
    """
    Read this context's state from AWS S3 bucket. Return empty dict if the file key path does not exist in the bucket.

    Args:
        hub: The redistributed pop central hub.
        ctx: A dict with the keys/values for the execution of the Idem run located in
        `hub.idem.RUNS[ctx['run_name']]`.

    Returns:
        A dict containing all resource state records. Return empty dict if the file key path does not exist in the bucket.
    """
    esm_profile = await hub.esm.aws.generate_esm_profile(ctx)
    try:
        esm_ctx = _populate_esm_ctx(esm_profile, ctx)
        client = await hub.tool.boto3.client.get_client(esm_ctx, service_name="s3")
        content = client.get_object(
            Bucket=esm_profile.get("bucket"),
            Key=esm_profile.get("key"),
        )
        state = json.loads(content["Body"].read())
        return state
    except botocore.exceptions.ClientError as client_ex:
        if client_ex.response["Error"]["Code"] == "NoSuchKey":
            hub.log.debug(
                f"No state file found from S3 bucket {esm_profile.get('bucket')} using key {esm_profile.get('key')}"
            )
            return {}
        else:
            hub.log.error(
                f"Failed to retrieve state file from S3 bucket {esm_profile.get('bucket')} using key {esm_profile.get('key')}"
                f" with error {client_ex.response['Error']['Message']}"
            )
            raise client_ex
    except Exception as e:
        hub.log.error(
            f"Failed to retrieve state file from S3 bucket {esm_profile.get('bucket')} using key {esm_profile.get('key')}"
            f" with error {str(e)}"
        )
        raise e


async def set_state(hub, ctx, state: Dict[str, Any]):
    """
    Write the state to this context's cache_file

    Args:
        hub: The redistributed pop central hub.
        ctx: A dict with the keys/values for the execution of the Idem run located in
        `hub.idem.RUNS[ctx['run_name']]`.
        state: A dict containing all resource states that will be stored in S3 bucket.

    Returns:
        None if the operation succeeds. An exception will raise if the operation failed.
    """
    esm_profile = await hub.esm.aws.generate_esm_profile(ctx)
    try:
        esm_ctx = _populate_esm_ctx(esm_profile, ctx)
        ret = await hub.exec.boto3.client.s3.put_object(
            esm_ctx,
            Bucket=esm_profile.get("bucket"),
            Body=bytes(json.dumps(state, default=str), "utf-8"),
            Key=esm_profile.get("key"),
            ServerSideEncryption="AES256"
            if esm_profile.get("encrypt", False)
            else None,
        )
        if not ret["result"]:
            error_msg = (
                f"Failed to upload state file to S3 bucket {esm_profile.get('bucket')} as"
                f" {esm_profile.get('key')} with error {ret['comment']}"
            )
            raise RuntimeError(error_msg)
        else:
            hub.log.debug(
                f"Successfully upload state file to S3 bucket {esm_profile.get('bucket')} as"
                f" {esm_profile.get('key')}"
            )
            return
    except Exception as e:
        hub.log.error(str(e))
        raise e


async def generate_esm_profile(hub, ctx):
    esm_profile = ctx.acct.get("esm")
    # If there was no esm profile in ACCT then get it purely from hub.OPT.extras.aws.esm
    if not esm_profile:
        if (
            "extras" in hub.OPT.acct
            and hub.OPT.acct.extras
            and "aws" in hub.OPT.acct.extras
        ):
            esm_profile = hub.OPT.acct.extras.aws.get("esm")
    if not esm_profile:
        raise ValueError("ESM profile is required to support remote ESM storage.")
    if not esm_profile.get("dynamodb_table"):
        raise ValueError("dynamodb_table is required in ESM profile.")
    if not esm_profile.get("bucket"):
        raise ValueError("bucket is required in ESM profile.")
    if not esm_profile.get("key"):
        raise ValueError("key is required in ESM profile.")
    return esm_profile


async def enter(hub, ctx):
    """
    Verify that only one process can access the same enforced state record file in S3 bucket.
    Set a lock by performing an atomic operation to put the file key to DynamoDB.
    If esm profile is not specified in credential profile. Then we try to find it from the Idem config.
    The config file should have the following structure:

      extras:
        aws:
          esm:
            bucket: idem-storage-bucket-name
            dynamodb_table: idem-esm-lock-table-name
            key: /my-file-path/my-esm-cache.json
            encrypt: True

    Args:
        hub: The redistributed pop central hub.
        ctx: A dict with the keys/values for the execution of the Idem run located in
        `hub.idem.RUNS[ctx['run_name']]`.

    Returns:
        None if lock has been acquired successfully. Raise exception if lock was failed to be acquired
    """
    esm_profile = await hub.esm.aws.generate_esm_profile(ctx)
    try:
        # Put item with conditional expression to acquire the lock. The conditional check and put operation is atomic.
        # This ensures that the S3 bucket file can be locked properly.
        esm_ctx = _populate_esm_ctx(esm_profile, ctx)
        db_resource = await hub.tool.boto3.resource.create(
            esm_ctx, "dynamodb", "Table", esm_profile.get("dynamodb_table")
        )
        db_resource.put_item(
            Item={"LockID": f"{esm_profile.get('bucket')}/{esm_profile.get('key')}"},
            ConditionExpression="attribute_not_exists(#r)",
            ExpressionAttributeNames={"#r": "LockID"},
        )
        # Lock acquired
        return
    except botocore.exceptions.ClientError as e:
        # Another exception than ConditionalCheckFailedException was caught, raise as-is
        if e.response["Error"]["Code"] != "ConditionalCheckFailedException":
            raise e
        else:
            # If conditional check failed, it means the lock cannot be acquired because it is already locked
            raise ValueError(
                f"File {esm_profile.get('bucket')}/{esm_profile.get('key')}"
                f" has been locked by another user/process."
            )


async def exit_(hub, ctx, handle: pathlib.Path, exception: Exception):
    """
    Release the db lock and handle errors

    Args:
        hub: The redistributed pop central hub.
        ctx: A dict with the keys/values for the execution of the Idem run located in
        `hub.idem.RUNS[ctx['run_name']]`.
        handle: This parameter is inherited from Idem. It is not being used in Idem-aws plugin.
        exception: Error.

    Returns:
        None if file lock has been released. Raise Exception if any failure happened.
    """
    esm_profile = await hub.esm.aws.generate_esm_profile(ctx)
    if exception:
        hub.log.error(f"{exception.__class__.__name__}: {exception}")
    if esm_profile is None:
        raise ValueError("ESM profile is required to support remote ESM storage.")
    try:
        # Delete item with conditional expression to release the lock
        esm_ctx = _populate_esm_ctx(esm_profile, ctx)
        db_resource = await hub.tool.boto3.resource.create(
            esm_ctx, "dynamodb", "Table", esm_profile.get("dynamodb_table")
        )
        db_resource.delete_item(
            Key={"LockID": f"{esm_profile.get('bucket')}/{esm_profile.get('key')}"},
            ConditionExpression="attribute_exists(#r)",
            ExpressionAttributeNames={"#r": "LockID"},
        )
        # Lock released
        return
    except botocore.exceptions.ClientError as e:
        # Another exception than ConditionalCheckFailedException was caught, raise as-is
        if e.response["Error"]["Code"] != "ConditionalCheckFailedException":
            raise e
        else:
            # Else, lock has been released
            hub.log.debug(
                f"Lock {esm_profile.get('bucket')}/{esm_profile.get('key')}"
                f" has been previously released."
            )
            return


def _populate_esm_ctx(esm_profile: dict, ctx: dict):
    # If esm has a region_name, we should use it when connecting to the dynamodb
    if esm_profile.get("region_name") is not None and esm_profile.get(
        "region_name"
    ) != ctx.get("acct", {}).get("region_name"):
        esm_ctx = NamespaceDict(copy.deepcopy(ctx))
        esm_ctx["acct"]["region_name"] = esm_profile.get("region_name")
        return esm_ctx

    return ctx
