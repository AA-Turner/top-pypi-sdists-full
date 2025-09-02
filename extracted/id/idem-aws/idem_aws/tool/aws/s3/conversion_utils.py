import json
from typing import Any
from typing import Dict


def convert_raw_bucket_notification_to_present(
    hub, raw_resource: Dict[str, Any], bucket_name: str
) -> Dict[str, Any]:
    """Convert the s3 bucket notification configurations response to a common format

    Args:
        raw_resource(dict):
            Dictionary of s3 bucket notification configurations

        bucket_name(str):
            Name of the bucket on which notification needs to be configured.

    Returns:
        A dictionary of s3 bucket notification configurations
    """
    translated_resource = {}
    raw_resource.pop("ResponseMetadata", None)

    if raw_resource:
        translated_resource["name"] = bucket_name
        translated_resource["resource_id"] = bucket_name + "-notifications"
        translated_resource["notifications"] = json.loads(json.dumps(raw_resource))
    return translated_resource


def convert_raw_bucket_logging_to_present(
    hub, ctx, raw_resource: Dict[str, Any], bucket_name: str
) -> Dict[str, Any]:
    """Convert the s3 bucket logging configurations response to a common format

    Args:
        raw_resource(dict):
            Dictionary of s3 bucket logging configurations

        bucket_name(str):
            Name of the bucket on which logging needs to be configured.

    Returns:
        A dictionary of s3 bucket logging configurations
    """
    translated_resource = {}
    raw_resource.pop("ResponseMetadata", None)

    if raw_resource:
        translated_resource["name"] = bucket_name
        translated_resource["resource_id"] = bucket_name
        translated_resource["bucket_logging_status"] = json.loads(
            json.dumps(raw_resource)
        )
    return translated_resource


async def convert_raw_s3_to_present_async(
    hub, ctx, idem_resource_name: str = None
) -> Dict[str, Any]:
    """Convert the s3 bucket configurations response to a common format

    Args:
        idem_resource_name(str, Optional):
            Name of the bucket.

    Returns:
        Dict[str, Any]
    """
    resource_translated = {
        "name": idem_resource_name,
        "resource_id": idem_resource_name,
    }

    ret = await hub.exec.boto3.client.s3.get_object_lock_configuration(
        ctx, Bucket=idem_resource_name
    )
    if not ret["result"] and "ObjectLockConfigurationNotFoundError" not in str(
        ret["comment"]
    ):
        # Continue if there is ObjectLockConfigurationNotFoundError exception else
        # throw an exception
        raise Exception(ret["comment"])

    if ret["result"]:
        if ret["ret"]["ObjectLockConfiguration"]["ObjectLockEnabled"] == "Enabled":
            resource_translated["object_lock_enabled_for_bucket"] = True
            # Added the object_lock_configuration for put_object_lock_configuration operation.
            resource_translated["object_lock_configuration"] = json.loads(
                json.dumps(ret["ret"]["ObjectLockConfiguration"])
            )
        else:
            resource_translated["object_lock_enabled_for_bucket"] = False
    ret = await hub.exec.boto3.client.s3.get_bucket_location(
        ctx, Bucket=idem_resource_name
    )
    if not ret["result"]:
        raise Exception(ret["comment"])
    if ret["result"] and ret["ret"]["LocationConstraint"]:
        resource_translated["create_bucket_configuration"] = {
            "LocationConstraint": ret["ret"]["LocationConstraint"]
        }
    ret = await hub.exec.boto3.client.s3.get_bucket_ownership_controls(
        ctx, Bucket=idem_resource_name
    )
    if not ret["result"] and "OwnershipControlsNotFoundError" not in str(
        ret["comment"]
    ):
        # Continue if there is OwnershipControlsNotFoundError exception else
        # throw an exception
        raise Exception(ret["comment"])

    if (
        ret["result"]
        and ret["ret"]["OwnershipControls"]
        and ret["ret"]["OwnershipControls"]["Rules"][0]["ObjectOwnership"]
    ):
        resource_translated["object_ownership"] = ret["ret"]["OwnershipControls"][
            "Rules"
        ][0]["ObjectOwnership"]
    ret = await hub.exec.boto3.client.s3.get_bucket_acl(ctx, Bucket=idem_resource_name)
    if not ret["result"] and "AccessControlListNotSupported" not in str(ret["comment"]):
        # Continue if there is AccessControlListNotSupported exception else
        # throw an exception
        raise Exception(ret["comment"])

        # checking first element in grants because for no permissions API returns empty array
    grant_full_control = ""
    grant_read = ""
    grant_read_acp = ""
    grant_write = ""
    grant_write_acp = ""

    if ret["result"] and ret["ret"]["Grants"][0]["Permission"]:
        for grant in ret["ret"]["Grants"]:
            if grant["Permission"]:
                grantee = grant["Grantee"]
                if grant["Permission"] == "FULL_CONTROL":
                    grant_full_control = hub.tool.aws.s3.s3_utils.get_grantee_payload(
                        grant_full_control, grantee
                    )
                elif grant["Permission"] == "READ":
                    grant_read = hub.tool.aws.s3.s3_utils.get_grantee_payload(
                        grant_read, grantee
                    )
                elif grant["Permission"] == "READ_ACP":
                    grant_read_acp = hub.tool.aws.s3.s3_utils.get_grantee_payload(
                        grant_read_acp, grantee
                    )
                elif grant["Permission"] == "WRITE":
                    grant_write = hub.tool.aws.s3.s3_utils.get_grantee_payload(
                        grant_write, grantee
                    )
                elif grant["Permission"] == "WRITE_ACP":
                    grant_write_acp = hub.tool.aws.s3.s3_utils.get_grantee_payload(
                        grant_write_acp, grantee
                    )

    if grant_full_control:
        resource_translated["grant_full_control"] = grant_full_control

    if grant_read:
        resource_translated["grant_read"] = grant_read

    if grant_read_acp:
        resource_translated["grant_read_acp"] = grant_read_acp

    if grant_write:
        resource_translated["grant_write"] = grant_write

    if grant_write_acp:
        resource_translated["grant_write_acp"] = grant_write_acp

    ret = await hub.exec.boto3.client.s3.get_bucket_tagging(
        ctx, Bucket=idem_resource_name
    )
    if not ret["result"] and "NoSuchTagSet" not in str(ret["comment"]):
        # Added error message check to continue if there is NoSuchTagSet exception else return the result
        raise Exception(ret["comment"])

    if ret["result"] and ret["ret"]["TagSet"]:
        resource_translated["tags"] = hub.tool.aws.tag_utils.convert_tag_list_to_dict(
            ret["ret"]["TagSet"]
        )
    return resource_translated


def convert_raw_public_access_block_to_present(
    hub, bucket_name: str, public_access_block_configuration: Dict
) -> Dict[str, Any]:
    translated_resource = {
        "name": f"{bucket_name}-public-access-block",
        "bucket": bucket_name,
        "public_access_block_configuration": json.loads(
            json.dumps(public_access_block_configuration)
        ),
        "resource_id": bucket_name,
    }
    return translated_resource


def convert_raw_bucket_policy_to_present(
    hub, raw_resource: Dict[str, Any], bucket: str, name: str
) -> Dict[str, Any]:
    """Util function to convert the s3 bucket policy response to a common format.

    Args:
        raw_resource(Dict[str, Any]):
            S3 bucket policy response.

        bucket(str):
            Name of the bucket on which policy needs to be configured.

        name(str):
            The name of the idem resource.

    Returns:
        A dictionary of s3 bucket notification configurations
    """
    translated_resource = {}
    raw_resource.pop("ResponseMetadata", None)

    if raw_resource:
        translated_resource["name"] = name
        translated_resource["resource_id"] = bucket + "-policy"
        translated_resource["bucket"] = bucket
        translated_resource["policy"] = raw_resource["Policy"]
    return translated_resource


def convert_raw_bucket_replication_to_present(
    hub, ctx, raw_resource: Dict[str, Any], bucket_name: str
) -> Dict[str, Any]:
    """Convert the s3 bucket replication configurations response to a common format.

    Args:
        raw_resource(dict[str, Any]):
            Dictionary of s3 bucket replication configurations.

        bucket_name(str):
            Name of the bucket on which replication needs to be configured.

    Returns:
        A dictionary of s3 bucket replication configurations
    """
    translated_resource = {}
    raw_resource.pop("ResponseMetadata", None)

    if raw_resource:
        translated_resource["name"] = bucket_name
        translated_resource["resource_id"] = bucket_name
        translated_resource["role"] = raw_resource["ReplicationConfiguration"]["Role"]
        translated_resource["rules"] = raw_resource["ReplicationConfiguration"]["Rules"]
    return translated_resource


def convert_raw_acl_policy_to_present(
    hub, raw_resource: Dict[str, Any], bucket_name: str
) -> Dict[str, Any]:
    """Util function to convert the s3 bucket policy response to a common format.

    Args:
        raw_resource(dict[str, Any]):
            S3 bucket policy response.

        bucket_name(str):
            Name of the bucket on which policy needs to be configured.

    Returns:
        A dictionary of s3 bucket notification configurations
    """
    translated_resource = {}
    raw_resource.pop("ResponseMetadata", None)

    if raw_resource:
        translated_resource["resource_id"] = bucket_name
        translated_resource["name"] = bucket_name
        translated_resource["access_control_policy"] = json.loads(
            json.dumps(raw_resource)
        )

    return translated_resource
