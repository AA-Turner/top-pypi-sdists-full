"""State module for managing Amazon WAFv2 Regex Pattern Set."""
import copy
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
    scope: str,
    regular_expression_list: List[
        make_dataclass("Regex", [("RegexString", str, field(default=None))])
    ],
    resource_id: str = None,
    description: str = None,
    tags: Dict[str, str] = None,
) -> Dict[str, Any]:
    """Creates a RegexPatternSet, which you reference in a RegexPatternSetReferenceStatement, to have WAF inspect a web
    request component for the specified patterns.

    Args:
        name(str): The name of the set. You cannot change the name after you create the set.
        resource_id(str, Optional): An identifier of the resource in the provider. Defaults to None.
        scope(str): Specifies whether this is for an Amazon CloudFront distribution or for a regional application. A
            regional application can be an Application Load Balancer (ALB), an Amazon API Gateway REST API,
            or an AppSync GraphQL API.  To work with CloudFront, you must also specify the Region US East
            (N. Virginia) as follows:    CLI - Specify the Region when you use the CloudFront scope:
            --scope=CLOUDFRONT --region=us-east-1.    API and SDKs - For all calls, use the Region endpoint
            us-east-1.
        description(str, Optional): A description of the set that helps with identification. Defaults to None.
        regular_expression_list(list): Array of regular expression strings.
            * RegexString (str, Optional): The string representing the regular expression.
        tags(dict, Optional): Dict in the format of {tag-key: tag-value}

    Request Syntax:
       .. code-block:: sls

          [regex-pattern-resource-id]:
              aws.wafv2.regex_pattern_set.present:
                - name: "string"
                - scope: "string"
                - regular_expression_list:
                    - RegexString: "string"
                - tags:
                    scope: "string"
                    name: "string"

    Returns:
        Dict[str, Any]

    Examples:
        .. code-block:: sls

            regex_pattern_set_name:
              aws.wafv2.regex_pattern_set.present:
                - name: regex_pattern_set_name
                - scope: CLOUDFRONT
                - regular_expression_list:
                    - RegexString: "idem-aws/$+"
                - tags:
                    scope: cloudfront-1
                    name: regex_pattern_set_name
    """
    result = dict(comment=[], old_state=None, new_state=None, name=name, result=True)
    before = None
    resource_updated = False
    is_invalid_scope_and_region = (
        hub.tool.aws.wafv2.regex_pattern_set.check_if_invalid_scope_and_region(
            ctx["acct"].get("region_name"), scope
        )
    )
    if is_invalid_scope_and_region:
        result["result"] = False
        result["comment"] += [is_invalid_scope_and_region]
        return result
    if resource_id:
        before = await hub.exec.aws.wafv2.regex_pattern_set.get(
            ctx=ctx, name=name, resource_id=resource_id, scope=scope
        )
        if not before["result"] or not before["ret"]:
            result["result"] = False
            result["comment"] = before["comment"]
            return result
        result["old_state"] = copy.deepcopy(before["ret"])
        plan_state = copy.deepcopy(result["old_state"])
        update_ret = await hub.tool.aws.wafv2.regex_pattern_set.update(
            ctx=ctx,
            current_state=result["old_state"],
            description=description,
            regular_expression_list=regular_expression_list,
        )
        result["comment"] = update_ret["comment"]
        result["result"] = update_ret["result"]
        resource_updated = bool(update_ret["ret"])
        if update_ret["ret"] and ctx.get("test", False):
            for modified_param in update_ret["ret"]:
                plan_state[modified_param] = update_ret["ret"][modified_param]
            result["comment"] += hub.tool.aws.comment_utils.would_update_comment(
                resource_type="aws.wafv2.regex_pattern_set", name=name
            )

        # update tags
        if tags is not None and tags != result["old_state"].get("tags"):
            update_tags_ret = await hub.tool.aws.wafv2.tag.update_tags(
                ctx=ctx,
                resource_arn=result["old_state"].get("arn"),
                old_tags=result["old_state"].get("tags"),
                new_tags=tags,
            )
            result["comment"] += update_tags_ret["comment"]
            result["result"] = result["result"] and update_tags_ret["result"]
            resource_updated = resource_updated or bool(update_tags_ret["ret"])

            if ctx.get("test", False) and update_tags_ret["ret"]:
                plan_state["tags"] = update_tags_ret["ret"]
    else:
        if ctx.get("test", False):
            result["new_state"] = hub.tool.aws.test_state_utils.generate_test_state(
                enforced_state={},
                desired_state={
                    "name": name,
                    "scope": scope,
                    "regular_expression_list": regular_expression_list,
                    "description": description,
                    "tags": tags,
                },
            )
            result["comment"] = hub.tool.aws.comment_utils.would_create_comment(
                resource_type="aws.wafv2.regex_pattern_set", name=name
            )
            return result
        ret = await hub.exec.boto3.client.wafv2.create_regex_pattern_set(
            ctx=ctx,
            Name=name,
            Scope=scope,
            Description=description,
            RegularExpressionList=regular_expression_list,
            Tags=hub.tool.aws.tag_utils.convert_tag_dict_to_list(tags)
            if tags
            else None,
        )
        result["result"] = ret["result"]
        if not result["result"]:
            result["comment"] = ret["comment"]
            return result
        resource_id = ret["ret"]["Summary"]["Id"]
        result["comment"] = hub.tool.aws.comment_utils.create_comment(
            resource_type="aws.wafv2.regex_pattern_set", name=name
        )
    if ctx.get("test", False):
        result["new_state"] = plan_state
    elif (not before) or resource_updated:
        after = await hub.exec.aws.wafv2.regex_pattern_set.get(
            ctx=ctx, name=name, resource_id=resource_id, scope=scope
        )
        if not after["result"]:
            result["result"] = False
            result["comment"] = after["comment"]
            return result
        result["new_state"] = copy.deepcopy(after["ret"])
    else:
        result["new_state"] = copy.deepcopy(result["old_state"])
    return result


async def absent(
    hub, ctx, name: str, scope: str, resource_id: str = None
) -> Dict[str, Any]:
    """Deletes the specified RegexPatternSet.

    Args:
        name(str): The name of the set. You cannot change the name after you create the set.
        resource_id(str, Optional): A unique identifier for the set. This ID is returned in the responses
            to create and list commands. You provide it to operations like update and delete.
            Idem automatically considers this resource being absent if this field is not specified. Defaults to None.
        scope(str): Specifies whether this is for an Amazon CloudFront distribution or for a regional application. A
            regional application can be an Application Load Balancer (ALB), an Amazon API Gateway REST API,
            or an AppSync GraphQL API.  To work with CloudFront, you must also specify the Region US East
            (N. Virginia) as follows:    CLI - Specify the Region when you use the CloudFront scope:
            --scope=CLOUDFRONT --region=us-east-1.    API and SDKs - For all calls, use the Region endpoint
            us-east-1.

    Request Syntax:
       .. code-block:: sls

          [regex-pattern-resource-id]:
              aws.wafv2.regex_pattern_set.absent:
                - name: "string"
                - scope: "string"
                - resource_id: "string"

    Returns:
        Dict[str, Any]

    Examples:

        .. code-block:: sls

            regex_pattern_set_name:
              aws.wafv2.regex_pattern_set.absent:
                - name: regex_pattern_set_name
                - resource_id: value
                - scope: CLOUDFRONT
    """

    result = dict(comment=[], old_state=None, new_state=None, name=name, result=True)
    if not resource_id:
        result["comment"] = hub.tool.aws.comment_utils.already_absent_comment(
            resource_type="aws.wafv2.regex_pattern_set", name=name
        )
        return result
    before = await hub.exec.aws.wafv2.regex_pattern_set.get(
        ctx=ctx, name=name, resource_id=resource_id, scope=scope
    )
    if not before["result"]:
        result["result"] = False
        result["comment"] = before["comment"]
        return result
    if not before["ret"]:
        result["comment"] = hub.tool.aws.comment_utils.already_absent_comment(
            resource_type="aws.wafv2.regex_pattern_set", name=name
        )
    elif ctx.get("test", False):
        result["old_state"] = before["ret"]
        result["comment"] = hub.tool.aws.comment_utils.would_delete_comment(
            resource_type="aws.wafv2.regex_pattern_set", name=name
        )
    else:
        result["old_state"] = before["ret"]
        ret = await hub.exec.boto3.client.wafv2.delete_regex_pattern_set(
            ctx=ctx,
            Name=name,
            Scope=scope,
            Id=resource_id,
            LockToken=before["ret"]["LockToken"],
        )
        result["result"] = ret["result"]
        if not result["result"]:
            result["comment"] = ret["comment"]
            result["result"] = False
            return result
        result["comment"] = hub.tool.aws.comment_utils.delete_comment(
            resource_type="aws.wafv2.regex_pattern_set", name=name
        )
    return result


async def describe(hub, ctx) -> Dict[str, Dict[str, Any]]:
    """Describe the resource in a way that can be recreated/managed with the
        corresponding "present" function

    Returns:
        Dict[str, Any]

    Examples:

        .. code-block:: bash

            $ idem describe aws.wafv2.regex_pattern_set
    """

    result = {}
    # Two types are scopes are allowed if the region is us-east-1 else only REGIONAL is allowed
    scopes_allowed = (
        ["CLOUDFRONT", "REGIONAL"]
        if ctx["acct"].get("region_name") == "us-east-1"
        else ["REGIONAL"]
    )

    for scope in scopes_allowed:
        ret = await hub.exec.boto3.client.wafv2.list_regex_pattern_sets(
            ctx=ctx, Scope=scope
        )

        if not ret["result"]:
            hub.log.warning(
                f"Could not describe wafv2 regex_pattern_set for scope {scope} {ret['comment']}"
            )
            continue

        for regex_pattern_set in ret["ret"]["RegexPatternSets"]:
            get_regex_ret = await hub.exec.aws.wafv2.regex_pattern_set.get(
                ctx=ctx,
                name=regex_pattern_set["Name"],
                resource_id=regex_pattern_set["Id"],
                scope=scope,
            )
            if not get_regex_ret["result"]:
                hub.log.debug(
                    f"Could not describe wafv2 regex_pattern_set for scope {regex_pattern_set['Name']} {get_regex_ret['comment']}"
                )
                continue
            resource_translated = get_regex_ret["ret"]
            # LockToken is not needed in describe.
            if "LockToken" in resource_translated:
                resource_translated.pop("LockToken")
            result[resource_translated["resource_id"]] = {
                "aws.wafv2.regex_pattern_set.present": [
                    {parameter_key: parameter_value}
                    for parameter_key, parameter_value in resource_translated.items()
                ]
            }
    return result
