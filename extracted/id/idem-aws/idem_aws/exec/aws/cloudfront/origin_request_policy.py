"""Exec module for managing Amazon Cloudfront Origin request Policy."""

__func_alias__ = {"list_": "list"}

from typing import Dict


async def get(
    hub,
    ctx,
    name,
    resource_id: str = None,
) -> Dict:
    """Gets Cloudfront origin request policy from AWS account.

    Args:
        name(str):
            The name of the Idem state.

        resource_id(str, Optional):
            AWS cloudfront origin request policy id to identify the resource.

    Returns:
        Dict[str, Any]

    Examples:
        Calling this exec module function from the cli with resource_id

        .. code-block:: bash

            idem exec aws.cloudfront.origin_request_policy.get name="idem_name" resource_id="resource_id"

        Using in a state:

        .. code-block:: yaml

            my_unmanaged_resource:
              exec.run:
                - path: aws.cloudfront.origin_request_policy.get
                - kwargs:
                    name: my_resource
                    resource_id: resource_id
    """

    result = dict(comment=[], ret=None, result=True)

    ret_list = await hub.exec.aws.cloudfront.origin_request_policy.list(ctx)

    if not ret_list["result"]:
        result["comment"] += list(ret_list["comment"])
        result["result"] = False
        hub.log.debug(f"Could not list origin request policies {ret_list['comment']}")
        return result

    if not ret_list.get("ret"):
        result["comment"] += ["No origin request policy present"]
        return result

    for policy in ret_list["ret"]:
        if (resource_id and policy.get("resource_id") == resource_id) or policy.get(
            "name"
        ) == name:
            result["ret"] = policy
            break

    if not result["ret"]:
        result["comment"] += [f"origin request policy '{name}' not present"]

    return result


async def list_(
    hub,
    ctx,
) -> Dict:
    """Lists all Cloudfront origin request policies.

    Returns:
        Dict[str, Any]

    Examples:
        Calling this exec module function from the cli with resource_id

        .. code-block:: bash

            idem exec aws.cloudfront.origin_request_policy.list

        Using in a state:

        .. code-block:: yaml

            my_unmanaged_resource:
              exec.run:
                - path: aws.cloudfront.origin_request_policy.get

    """

    result = dict(comment=[], ret=[], result=True)

    ret_list = await hub.exec.boto3.client.cloudfront.list_origin_request_policies(ctx)

    if not ret_list["result"]:
        result["comment"] += list(ret_list["comment"])
        result["result"] = False
        hub.log.debug(f"Could not list origin request policies {ret_list['comment']}")
        return result

    if not ret_list.get("ret"):
        result["comment"] += ["No origin request policy present"]
        return result

    items = ret_list["ret"]["OriginRequestPolicyList"]["Items"]

    for item in items:
        policy_id = item["OriginRequestPolicy"]["Id"]
        name = item["OriginRequestPolicy"]["OriginRequestPolicyConfig"]["Name"]

        ret = await hub.exec.boto3.client.cloudfront.get_origin_request_policy(
            ctx, Id=policy_id
        )
        if not ret["result"]:
            if "NoSuchOriginRequestPolicy" in str(ret["comment"]):
                result["comment"].append(
                    hub.tool.aws.comment_utils.get_empty_comment(
                        resource_type="aws.cloudfront.origin_request_policy", name=name
                    )
                )

            result["comment"] += list(ret["comment"])
            result["result"] = False
            continue

        if not ret["ret"]["OriginRequestPolicy"]:
            result["comment"].append(
                hub.tool.aws.comment_utils.get_empty_comment(
                    resource_type="aws.cloudfront.origin_request_policy", name=name
                )
            )
            continue

        ret["ret"]["OriginRequestPolicy"]["ETag"] = ret["ret"]["ETag"]

        result["ret"].append(
            hub.tool.aws.cloudfront.conversion_utils.convert_raw_origin_request_policy_to_present(
                ctx,
                raw_resource=ret["ret"]["OriginRequestPolicy"],
                idem_resource_name=name,
            )
        )

    return result
