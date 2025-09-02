"""Tool module for managing Amazon S3 bucket logging configuration."""
from typing import Any
from typing import Dict
from typing import List

from dict_tools import data


async def update(
    hub,
    ctx,
    resource_id: str,
    before: Dict[str, Any],
    bucket_logging_status: Dict[str, Any],
):
    """Updates the logging configuration for the S3 bucket.

    Args:
        resource_id:
            AWS S3 bucket name.

        before(Dict):
            Existing resource parameters in Amazon Web Services.

        bucket_logging_status(Dict):
            Logging configuration.

    Returns:
        {"result": True|False, "comment": A message Tuple, "ret": Dict}
    """
    result = dict(comment=[], result=True, ret=None)

    # check and create payload for creating logging configurations to avoid redundant calls
    logging_diff = hub.tool.aws.s3.bucket_logging.get_logging_configuration_diff(
        bucket_logging_status, before
    )

    if logging_diff:
        result["ret"] = {}

        if not ctx.get("test", False):
            update_ret = await hub.exec.boto3.client.s3.put_bucket_logging(
                ctx=ctx, Bucket=resource_id, BucketLoggingStatus=bucket_logging_status
            )
            if not update_ret["result"]:
                result["comment"] = update_ret["comment"]
                result["result"] = False
                return result
            result["comment"] = hub.tool.aws.comment_utils.update_comment(
                resource_type="aws.s3.bucket_logging", name=resource_id
            )
        result["ret"]["bucket_logging_status"] = bucket_logging_status

    return result


def get_logging_configuration_diff(
    hub, new_logging_config: Dict[str, List], old_state: Dict[str, List]
) -> Dict[str, List]:
    """This functions helps in comparing two dicts.

    It compares each key value in both the dicts and return diff logging configuration.

    Args:
        new_logging_config(Dict[str, List]):
            New logging configuration attributes.

        old_state(Dict[str, List]):
            Old idem state used to retrieve old logging configuration attributes.

    Returns:
        {Resultant logging dictionary}
    """
    old_state_logging = old_state.get("bucket_logging_status")

    old_state_logging = old_state_logging if old_state_logging is not None else {}

    return data.recursive_diff(new_logging_config, old_state_logging, ignore_order=True)
