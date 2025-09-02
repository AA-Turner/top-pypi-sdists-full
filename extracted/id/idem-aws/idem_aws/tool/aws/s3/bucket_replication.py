"""Tool module for managing Amazon S3 bucket replication."""
from typing import Any
from typing import Dict
from typing import List

from dict_tools import data


async def update(
    hub, ctx, resource_id: str, before: Dict[str, Any], role: str, rules: List
):
    """Updates the replication configuration for the S3 bucket.

    Update the replication configuration for provided bucket.

    Args:
        resource_id:
            AWS S3 bucket name.

        before(Dict):
            Existing resource parameters in Amazon Web Services.

        role(str):
            The Amazon Resource Name (ARN) of the Identity and Access Management (IAM) role that Amazon S3
            assumes when replicating objects.

        rules(List):
            A container for one or more replication rules. A replication configuration must have at least
            one rule and can contain a maximum of 1,000 rules.

    Returns:
        {"result": True|False, "comment": A message Tuple, "ret": Dict}

    """
    result = dict(comment=[], result=True, ret=None)
    update_payload = {}
    payload = {}

    if role and role != before.get("role"):
        update_payload["Role"] = role
        payload["Role"] = role
    else:
        payload["Role"] = before.get("role")

    if rules:
        before_rule_map = {}
        rule_map = {}

        for rule in before["rules"]:
            before_rule_map[rule["ID"]] = rule

        for rule in rules:
            rule_map[rule["ID"]] = rule

        rule_diff = data.recursive_diff(before_rule_map, rule_map, ignore_order=True)

        if rule_diff:
            update_payload["Rules"] = rules
            payload["Rules"] = rules
        else:
            payload["Rules"] = before.get("rules")

    if update_payload:
        result["ret"] = {}

        if not ctx.get("test", False):
            update_ret = await hub.exec.boto3.client.s3.put_bucket_replication(
                ctx=ctx,
                Bucket=resource_id,
                ReplicationConfiguration=payload,
            )
            if not update_ret["result"]:
                result["comment"] = update_ret["comment"]
                result["result"] = False
                return result
            result["comment"] = hub.tool.aws.comment_utils.update_comment(
                resource_type="aws.s3.bucket_replication", name=resource_id
            )
        if "Role" in update_payload:
            result["ret"]["role"] = update_payload["Role"]
        if "Rules" in update_payload:
            result["ret"]["rules"] = update_payload["Rules"]

    return result
