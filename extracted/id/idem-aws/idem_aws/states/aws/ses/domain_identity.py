"""State module for managing SES Domain Identity."""
import copy
from typing import Any
from typing import Dict

__contracts__ = ["resource"]


async def present(
    hub,
    ctx,
    name: str,
    domain: str,
    resource_id: str = None,
) -> Dict[str, Any]:
    """Adds a domain to the list of identities for your Amazon SES account in the current AWS Region and attempts to verify it.

    Args:
        name(str):
            An Idem name to identify SES Domain Identity resource.

        domain(str):
            The domain to be verified.

        resource_id(str, Optional):
            The domain name.

    Request Syntax:
        .. code-block:: sls

            [domain_identity-resource-id]:
              aws.ses.domain_identity.present:
                - name: "string"
                - domain: "string"

    Returns:
        Dict[str, Any]

    Examples:

        .. code-block:: sls

            example.com:
              aws.ses.domain_identity.present:
                - name: example.com
                - domain: example.com

    """
    result = dict(comment=[], old_state=None, new_state=None, name=name, result=True)
    before = None

    if resource_id:
        before = await hub.exec.aws.ses.domain_identity.get(
            ctx, resource_id=resource_id
        )
        if not before["result"]:
            result["comment"] = before["comment"]
            result["result"] = before["result"]
            return result

    if before and before.get("ret"):
        result["old_state"] = before["ret"].copy()
        result["comment"] = hub.tool.aws.comment_utils.already_exists_comment(
            resource_type="aws.ses.domain_identity", name=name
        )
        result["new_state"] = copy.deepcopy(result["old_state"])
    else:
        if ctx.get("test", False):
            result["new_state"] = hub.tool.aws.test_state_utils.generate_test_state(
                enforced_state={},
                desired_state={
                    "name": name,
                    "domain": domain,
                },
            )
            result["comment"] += hub.tool.aws.comment_utils.would_create_comment(
                resource_type="aws.ses.domain_identity", name=name
            )
            return result

        ret = await hub.exec.boto3.client.ses.verify_domain_identity(
            ctx,
            Domain=domain,
        )
        if not ret["result"]:
            result["comment"] += ret["comment"]
            result["result"] = False
            return result

        after = await hub.exec.aws.ses.domain_identity.get(ctx, resource_id=domain)
        result["comment"] += hub.tool.aws.comment_utils.create_comment(
            resource_type="aws.ses.domain_identity", name=name
        )
        result["new_state"] = after.get("ret")
        if not ret["result"]:
            result["comment"] += ret["comment"]
            result["result"] = False
            return result

    return result


async def absent(hub, ctx, name: str, resource_id: str = None) -> Dict[str, Any]:
    """Deletes the specified identity

    Args:
        name(str):
            An Idem name to identify SES Domain Identity resource.

        resource_id(str, Optional):
            The domain name.
            Idem automatically considers this resource being absent if this field is not specified.

    Request Syntax:
        .. code-block:: sls

            [domain_identity-resource-id]:
              aws.ses.domain_identity.absent:
                - name: "string"
                - resource_id: "string"

    Returns:
        Dict[str, Any]

    Examples:

        .. code-block:: sls

            example.com:
              aws.ses.domain_identity.absent:
                - name: example.com
                - domain: example.com
    """
    result = dict(comment=[], old_state=None, new_state=None, name=name, result=True)
    if not resource_id:
        result["comment"] = hub.tool.aws.comment_utils.already_absent_comment(
            resource_type="aws.ses.domain_identity", name=name
        )
        return result

    before = await hub.exec.aws.ses.domain_identity.get(ctx, resource_id)
    if not before["result"]:
        result["comment"] = before["comment"]
        result["result"] = False
        return result

    if not before["ret"]:
        result["comment"] = hub.tool.aws.comment_utils.already_absent_comment(
            resource_type="aws.ses.domain_identity", name=name
        )
    else:
        result["old_state"] = before["ret"]

        if ctx.get("test", False):
            result["comment"] = hub.tool.aws.comment_utils.would_delete_comment(
                resource_type="aws.ses.domain_identity", name=name
            )
            return result
        # delete the SES Domain Identity

        response = await hub.exec.boto3.client.ses.delete_identity(
            ctx,
            Identity=resource_id,
        )
        if not response["result"]:
            result["comment"] += [
                f"Error deleting aws.ses.domain_identity '{resource_id}': {response['comment']}"
            ]
            result["result"] = False
            return result
        result["comment"] = hub.tool.aws.comment_utils.delete_comment(
            resource_type="aws.ses.domain_identity", name=name
        )
    return result


async def describe(hub, ctx) -> Dict[str, Dict[str, Any]]:
    """Describe the resource in a way that can be recreated/managed with the corresponding "present" function.

    Returns:
        Dict[str, Any]

    Examples:
        .. code-block:: bash

            idem describe aws.ses.domain_identity
    """

    result = {}

    ret = await hub.exec.aws.ses.domain_identity.list(ctx)
    if not ret["result"]:
        result["comment"] += list(ret["comment"])
        result["result"] = False
        return result

    for identity in ret["ret"]:
        resource_id = identity.get("resource_id")

        result[resource_id] = {
            "aws.ses.domain_identity.present": [
                {parameter_key: parameter_value}
                for parameter_key, parameter_value in identity.items()
            ]
        }

    return result
