"""State module for managing acl policy for S3 bucket."""
import copy
import json
from dataclasses import field
from dataclasses import make_dataclass
from typing import Any
from typing import Dict
from typing import List

__contracts__ = ["resource"]


async def present(
    hub,
    ctx,
    name: str,
    access_control_policy: make_dataclass(
        "AccessControlPolicy",
        [
            (
                "Grants",
                List[
                    make_dataclass(
                        "Grant",
                        [
                            (
                                "Grantee",
                                make_dataclass(
                                    "Grantee",
                                    [
                                        ("DisplayName", str, field(default=None)),
                                        ("EmailAddress", str, field(default=None)),
                                        ("ID", str, field(default=None)),
                                        ("Type", str, field(default=None)),
                                        ("URI", str, field(default=None)),
                                    ],
                                ),
                                field(default=None),
                            ),
                            ("Permission", str, field(default=None)),
                        ],
                    )
                ],
                field(default=None),
            ),
            (
                "Owner",
                make_dataclass(
                    "Owner",
                    [
                        ("DisplayName", str, field(default=None)),
                        ("ID", str, field(default=None)),
                    ],
                ),
                field(default=None),
            ),
        ],
    ),
    resource_id: str = None,
) -> Dict[str, Any]:
    """Create/Update the ACL policy for S3 bucket.

    Amazon S3 access control lists (ACLs) enable you to manage access to bucket and objects. Each bucket and object
    has an ACL attached to it as a subresource. It defines which AWS accounts or groups are granted access and the type
    of access. When a request is received against a resource, Amazon S3 checks the corresponding ACL to verify that the
    requester has the necessary access permissions.


    Args:
        name(str):
            The bucket name on which ACL gets apply.

        resource_id(str, Optional):
            Name of the S3 bucket.

        access_control_policy(dict):
            Contains the elements that set the ACL permissions for an object per grantee.

            * Grants (list[dict[str, Any]], Optional):
                A list of grants.

                * Grantee (dict[str, Any], Optional):
                    The person being granted permissions.

                    * DisplayName (str, Optional):
                        Screen name of the grantee.

                    * EmailAddress (str, Optional):
                        Email address of the grantee.  Using email addresses to specify a grantee is only supported in
                        the following Amazon Web Services Regions:    US East (N. Virginia)   US West (N. California)
                        US West (Oregon)    Asia Pacific (Singapore)   Asia Pacific (Sydney)   Asia Pacific (Tokyo)
                        Europe (Ireland)   South America (São Paulo)   For a list of all the Amazon S3 supported Regions
                        and endpoints, see Regions and Endpoints in the Amazon Web Services General Reference.
                    * ID (str, Optional):
                        The canonical user ID of the grantee.

                    * Type (str):
                        Type of grantee

                    * URI (str, Optional):
                        URI of the grantee group.

                * Permission (str, Optional):
                    Specifies the permission given to the grantee.

            * Owner (dict, Optional):
                Container for the bucket owner's display name and ID.

                * DisplayName (str, Optional):
                    Container for the display name of the owner.

                * ID (str, Optional):
                    Container for the ID of the owner.

    Request Syntax:
        .. code-block:: yaml

            [bucket_name]:
              aws.s3.bucket_acl.present:
              - name: "string"
              - resource_id: "string"
              - access_control_policy:
                  Grants:
                    - Grantee:
                        DisplayName: [string]
                        EmailAddress: [string]
                        ID: [string]
                        Type: [string]
                        URI: [string]
                      Permission: [string]
                  Owner:
                    DisplayName: [string]
                    ID: [string]

    Returns:
        dict[str, Any]

    Examples:
        .. code-block:: yaml

            resource_is_present:
              aws.s3.bucket_acl.present:
                - name: value
                - access_control_policy: value
    """
    result = dict(comment=[], old_state=None, new_state=None, name=name, result=True)
    resource_updated = False

    if resource_id:
        before_ret = await hub.exec.aws.s3.bucket_acl.get(
            ctx=ctx, resource_id=resource_id, name=name
        )
        if not before_ret["result"] or not before_ret["ret"]:
            result["result"] = False
            result["comment"] = before_ret["comment"]
            return result

        result["old_state"] = copy.deepcopy(before_ret["ret"])
        result["new_state"] = copy.deepcopy(result["old_state"])

        update_bucket_acl = await hub.tool.aws.s3.bucket_acl.update(
            ctx,
            resource_id=resource_id,
            raw_resource=before_ret["ret"],
            access_control_policy=access_control_policy,
        )
        result["comment"] += update_bucket_acl["comment"]
        if not update_bucket_acl["result"]:
            result["result"] = False
            return result

        if not update_bucket_acl["ret"]:
            result["comment"] = hub.tool.aws.comment_utils.already_exists_comment(
                resource_type="aws.s3.bucket_acl", name=name
            )

        if update_bucket_acl["ret"] and ctx.get("test", False):
            result["new_state"].update(update_bucket_acl["ret"])
            result["comment"] += hub.tool.aws.comment_utils.would_update_comment(
                resource_type="aws.s3.bucket_acl", name=name
            )
        resource_updated = resource_updated or bool(update_bucket_acl["ret"])
        if resource_updated and ctx.get("test", False):
            return result
    else:
        if ctx.get("test", False):
            result["new_state"] = hub.tool.aws.test_state_utils.generate_test_state(
                enforced_state={},
                desired_state={
                    "name": name,
                    "access_control_policy": access_control_policy,
                    "resource_id": name,
                },
            )
            result["comment"] = hub.tool.aws.comment_utils.would_create_comment(
                resource_type="aws.s3.bucket_acl", name=name
            )
            return result

        create_ret = await hub.exec.boto3.client.s3.put_bucket_acl(
            ctx,
            Bucket=name,
            AccessControlPolicy=access_control_policy,
        )
        if not create_ret["result"]:
            result["result"] = False
            result["comment"] = create_ret["comment"]
            return result

        result["comment"] = hub.tool.aws.comment_utils.create_comment(
            resource_type="aws.s3.bucket_acl", name=name
        )
        resource_id = name

    if (not result["old_state"]) or resource_updated:
        after_ret = await hub.exec.aws.s3.bucket_acl.get(
            ctx=ctx, resource_id=resource_id, name=name
        )
        if not after_ret["result"] or not after_ret["ret"]:
            result["result"] = False
            result["comment"] += after_ret["comment"]
            return result
        result["new_state"] = after_ret["ret"]

    return result


async def absent(
    hub,
    ctx,
    name: str,
    resource_id: str = None,
) -> Dict[str, Any]:
    """Deletes associated ACL policy for an S3 bucket.

    This action cannot be possible as AWS does not provide an API to dissociate the ACL from S3 bucket,
    The ACL policy will be deleted post the bucket gets deleted.

    Args:
        name(str):
            An S3 bucket name.

        resource_id(str, Optional):
            An identifier of the resource in the provider.

    Request Syntax:
        .. code-block:: yaml

            [bucket_name]:
              aws.s3.bucket_acl.absent:
                - name: "string"
                - resource_id: "string"
    Returns:
        dict[str, Any]

    Examples:
        .. code-block:: yaml

            resource_is_absent:
              aws.s3.bucket_acl.absent:
                - name: value
                - resource_id: value
    """
    result = dict(comment=[], old_state=None, new_state=None, name=name, result=True)

    before_ret = await hub.exec.aws.s3.bucket_acl.get(
        ctx=ctx, resource_id=resource_id, name=name
    )

    if not before_ret["result"] or not before_ret["ret"]:
        result["comment"] = hub.tool.aws.comment_utils.already_absent_comment(
            resource_type="aws.s3.bucket_acl", name=name
        )
    else:
        result["old_state"] = copy.deepcopy(before_ret["ret"])
        result[
            "comment"
        ] = f"This action cannot be possible as AWS does not provide an API to dissociate the ACL from S3 bucket, The ACL policy will be deleted post '{name}' bucket gets deleted."

    return result


async def describe(hub, ctx) -> Dict[str, Dict[str, Any]]:
    """Gets information about the ACL policy attached to S3 bucket.

    Describe the resource in a way that can be recreated/managed with the corresponding "present" function

    Returns:
        dict[str, Any]

    Examples:
        .. code-block:: bash

            $ idem describe aws.s3.bucket_acl
    """
    result = {}
    # To describe the ACL policy of all the buckets, we first need to list all the buckets,
    # then get the ACL policy for each bucket
    ret = await hub.exec.boto3.client.s3.list_buckets(ctx)
    if not ret["result"]:
        hub.log.warning(f"Could not describe bucket_acl {ret['comment']}")
        return {}

    for bucket in ret["ret"]["Buckets"]:
        bucket_name = bucket.get("Name")
        # get acl policy for each bucket
        acl_policy = await hub.exec.aws.s3.bucket_acl.get(
            ctx=ctx, resource_id=bucket_name, name=bucket_name
        )
        if acl_policy["result"]:
            policy_translated = json.loads(json.dumps(acl_policy["ret"]))

            result[bucket_name + "-bucket_acl"] = {
                "aws.s3.bucket_acl.present": [policy_translated]
            }

    return result
