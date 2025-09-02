"""Tool module for managing Amazon S3 bucket encryption."""
import asyncio
import json
from typing import Any
from typing import Dict
from typing import List


def convert_raw_bucket_encryption_to_present(
    hub, bucket: str, raw_resource: Dict[str, Any], idem_resource_name: str = None
) -> Dict[str, Any]:
    """Converts an AWS S3 bucket encryption resource to a common idem present state.

    Args:
        bucket(str):
            The S3 bucket name in Amazon Web Services.

        raw_resource(Dict[str, Any]):
            The AWS response to convert.

        idem_resource_name(str, Optional):
            An Idem name of the resource.

    Returns:
        Dict[str, Any]: Common idem present state.
    """
    raw_resource.pop("ResponseMetadata", None)

    resource_translated = {
        "name": idem_resource_name if idem_resource_name else f"{bucket}-encryption",
        "resource_id": bucket,
        "bucket": bucket,
        "server_side_encryption_configuration": json.loads(
            json.dumps(raw_resource.get("ServerSideEncryptionConfiguration"))
        ),
    }

    return resource_translated


def is_bucket_encryption_configuration_identical(
    hub,
    new_configuration: Dict[str, List],
    old_configuration: Dict[str, List],
) -> bool:
    """Compares the new and old bucket encryption configurations.

    Args:
        new_encryption_configuration(Dict[str, Any]):
            The new bucket encryption configuration parameters.

        old_encryption_configuration(Dict[str, Any]):
            The old bucket encryption configuration parameters.

    Returns:
        bool: true if there are no differences between the new and old bucket encryption configurations.
    """
    new_server_side_encryption_configuration = new_configuration.get(
        "server_side_encryption_configuration", {}
    )
    old_server_side_encryption_configuration = old_configuration.get(
        "server_side_encryption_configuration", {}
    )

    new_rules_configuration = new_server_side_encryption_configuration.get("Rules", [])
    old_rules_configuration = old_server_side_encryption_configuration.get("Rules", [])
    if not hub.tool.aws.s3.bucket_encryption.are_bucket_server_side_encryption_rules_identical(
        new_rules_configuration, old_rules_configuration
    ):
        return False

    return True


def are_bucket_server_side_encryption_rules_identical(
    hub,
    new_rules: List,
    old_rules: List,
) -> bool:
    """Compares the new and old bucket server side encryption rules.

    Args:
        new_rules(List):
            The new bucket server side encryption rules.

        old_rules(List):
            The old bucket server side encryption rules.

    Returns:
        bool: true if there are no differences between the new and old bucket server side encryption rules.
    """
    if (new_rules is None or len(new_rules) == 0) and (
        old_rules is None or len(old_rules) == 0
    ):
        return True
    if (
        new_rules is None
        or len(new_rules) == 0
        or old_rules is None
        or len(old_rules) == 0
    ):
        return False

    diff = [
        i for i in new_rules + old_rules if i not in new_rules or i not in old_rules
    ]

    return len(diff) == 0


async def wait_for_updates(
    hub,
    ctx,
    bucket: str,
    server_side_encryption_configuration: Dict[str, List],
    timeout: Dict = None,
) -> Dict[str, Any]:
    """Waits for an AWS S3 bucket encryption configuration to be updated.

    Args:
        bucket(str):
            The name of the S3 bucket in Amazon Web Services.

        server_side_encryption_configuration(Dict):
            The expected encryption configuration for the S3 bucket.

        timeout(Dict, Optional):
            Timeout configuration for updating the S3 bucket encryption configuration.
                * delay (int, Optional): The amount of time in seconds to wait between attempts. Defaults to 4 seconds.
                * max_attempts (int, Optional): Maximum attempts of waiting for the update. Defaults to 30 attempts.

    Returns:
        Dict[str, Any]: Common idem present state.
    """
    result = dict(comment=[], result=True, ret=None)

    delay = timeout.get("delay", 4) if timeout else 4
    max_attempts = timeout.get("max_attempts", 30) if timeout else 30

    count = 1
    while count <= max_attempts:
        hub.log.info(
            f"Waiting for S3 bucket '{bucket}' encryption configuration to be updated for the {count} time."
        )
        await asyncio.sleep(delay)

        get_bucket_encryption_ret = (
            await hub.exec.boto3.client.s3.get_bucket_encryption(ctx, Bucket=bucket)
        )
        if not get_bucket_encryption_ret["result"]:
            result["result"] = False
            result["comment"] = get_bucket_encryption_ret["comment"]
            return result

        actual_encryption_configuration = {
            "server_side_encryption_configuration": json.loads(
                json.dumps(
                    get_bucket_encryption_ret.get("ret").get(
                        "ServerSideEncryptionConfiguration", {}
                    )
                )
            ),
        }
        expected_encryption_configuration = {
            "server_side_encryption_configuration": server_side_encryption_configuration,
        }

        if hub.tool.aws.s3.bucket_encryption.is_bucket_encryption_configuration_identical(
            expected_encryption_configuration, actual_encryption_configuration
        ):
            result["ret"] = get_bucket_encryption_ret["ret"]
            return result

        count = count + 1

    result["result"] = False
    result["comment"] += [
        f"Timed out waiting for S3 bucket '{bucket}' encryption configuration to be updated."
    ]
    return result
