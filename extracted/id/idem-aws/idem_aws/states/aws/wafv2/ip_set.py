"""State module for managing AWS WAFV2 IPSet."""
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
    ip_address_version: str,
    addresses: list,
    description: str = None,
    resource_id: str = None,
    tags: List[
        make_dataclass(
            """Tags associated with IPSet resources in wafv2""" "Tags",
            [("Key", str), ("Value", str, field(default=None))],
        )
    ] = None,
    lock_token: str = None,
) -> Dict[str, Any]:
    """Creates an AWS IPSet for AWS WAFV2.

    Args:
        name (str): The name of the IP set on AWS. You cannot change the name of an IPSet after you create it.

        scope (str): Specifies whether this is for an Amazon CloudFront distribution or for a regional
             application. A ``REGIONAL`` application can be an Application Load Balancer (ALB), an Amazon API Gateway
             REST API, or an AppSync GraphQL API.
             To work with CloudFront, you must also specify the Region US East (N. Virginia) as follows:
             CLI - Specify the Region when you use the CloudFront scope: ``--scope=CLOUDFRONT --region=us-east-1`` .
             API and SDKs - For all calls, use the Region endpoint us-east-1.

        description (str, Optional): A description of the IPSet that helps with identification.

        ip_address_version (str): The version of the IP addresses, either IPV4 or IPV6 .

        addresses (list): Contains an array of strings that specifies zero or more IP addresses or blocks of IP addresses in Classless Inter-Domain Routing (CIDR) notation. WAF supports all IPv4 and IPv6 CIDR ranges except for /0.

        resource_id(str, Optional): Needed to retrieve/update/delete description of an existing IPSet. It is a unique identifier for the set. This Id is returned in the responses to create and list commands.

        lock_token (str, Optional): A token used for optimistic locking. WAF returns a token to your get and list requests, to mark the state of the entity at the time of the request. To make changes to the entity associated with the token, you provide the token to operations like update and delete. WAF uses the token to ensure that no changes have been made to the entity since you last retrieved it. If a change has been made, the update fails with a WAFOptimisticLockException . If this happens, perform another get , and use the new token returned by that operation. Example address strings: To configure WAF to allow, block, or count requests that originated from the IP address 192.12.2.44, specify 192.12.2.44/32. To configure WAF to allow, block, or count requests that originated from IP addresses from 193.0.2.1 to 192.0.2.255, specify 192.0.2.0/24. To configure WAF to allow, block, or count requests that originated from the IP address 1111:0000:0000:0000:0000:0000:0000:0111, specify 1111:0000:0000:0000:0000:0000:0000:0111/128. To configure WAF to allow, block, or count requests that originated from IP addresses 1111:0000:0000:0000:0000:0000:0000:0000 to 1111:0000:0000:0000:ffff:ffff:ffff:ffff, specify 1111:0000:0000:0000:0000:0000:0000:0000/64. For more information about CIDR notation, see the Wikipedia entry Classless Inter-Domain Routing. Example JSON Addresses specifications: Empty array: "Addresses": [] Array with one address: "Addresses": ["192.0.2.44/32"] Array with three addresses: "Addresses": ["192.0.2.44/32", "192.0.2.0/24", "192.0.0.0/16"] INVALID specification: "Addresses": [""] INVALID(str) --

        tags (Dict or List, Optional): An array of key:value pairs to associate with the resource.

             Key (str): Part of the key:value pair that defines a tag. You can use a tag key to
             describe a category of information, such as ``"customer."`` Tag keys are case-sensitive.

             Value (str): Part of the key:value pair that defines a tag. You can use a tag value
             to describe a specific value within a category, such as "companyA" or "companyB." Tag values are case-sensitive.

    Request Syntax:
        .. code-block:: sls

            [my_idem_ip_set_present]:
                 aws.wafv2.ip_set.present:
                     - name: 'str'
                     - scope: 'str'
                     - ip_address_version: 'str'
                     - addresses: 'str'
                         - 192.0.1.0/24
                     - resource_id: 'str'
                     - description: 'str'
                     - tags:
                         - Key: 'str'
                         Value: 'str'


    Returns:
        Dict[str, Any]

    Example:
        .. code-block:: sls

         [my_idem_ip_set_present]:
             aws.wafv2.ip_set.present:
                 - name: test-wafv2-ip-set-1663200539
                 - scope: REGIONAL
                 - ip_address_version: IPV4
                 - addresses:
                     - 192.0.2.44/32
                     - 19.1.2.44/32
                 - resource_id: f547799f-e325-4876-9e0e-264d835eb3fd
                 - description: for testing idem plugin for IPSet.
                 - tags:
                     - Key: Name
                       Value: ipset-name
                     - Key: test-wafv2-ip-set-1663200539
                       Value: test-wafv2-ip-set-1663200539
    """
    result = dict(comment=[], old_state=None, new_state=None, name=name, result=True)
    resource_updated: bool = False
    if resource_id:
        # IPSet exists , update
        before_ret = await hub.exec.aws.wafv2.ip_set.get(
            ctx, name=name, scope=scope, resource_id=resource_id
        )
        if not before_ret["result"] or not before_ret["ret"]:
            result["result"] = False
            result["comment"] = before_ret["comment"]
            return result

        result["old_state"] = copy.deepcopy(before_ret["ret"])
        result["new_state"] = copy.deepcopy(result["old_state"])
        arn = before_ret["ret"]["arn"]
        old_tags = before_ret["ret"]["tags"]
        desired_state = {
            "name": name,
            "scope": scope,
            "resource_id": resource_id,
            "description": description,
            "addresses": addresses,
        }
        # Update IPSet
        update_ret = await hub.tool.aws.wafv2.ip_set_utils.update(
            ctx, name=name, current_state=before_ret["ret"], desired_state=desired_state
        )
        result["comment"] = update_ret["comment"]
        if not update_ret["result"]:
            result["result"] = False
            return result
        result["result"] = update_ret["result"]

        resource_updated = resource_updated or bool(update_ret["ret"])
        if update_ret["ret"] and ctx.get("test", False):
            result["new_state"].update(copy.deepcopy(update_ret["ret"]))

        # Update Tags
        if tags is not None and tags != result["old_state"].get("tags"):
            update_tags_ret = await hub.tool.aws.wafv2.tag.update_tags(
                ctx,
                resource_arn=arn,
                old_tags=old_tags,
                new_tags=tags,
            )
            result["comment"] += update_tags_ret["comment"]
            result["result"] = result["result"] and update_tags_ret["result"]
            if not update_tags_ret["result"]:
                result["result"] = False
                hub.log.debug(f"Failed updating tags for aws.wafv2.ip.set '{name}'")
                return result
            resource_updated = resource_updated or bool(update_tags_ret["ret"])
            if update_tags_ret["ret"] and ctx.get("test", False):
                result["new_state"]["tags"] = update_tags_ret["ret"]

        if ctx.get("test", False) and resource_updated:
            return result

    else:
        if ctx.get("test", False):
            result["new_state"] = hub.tool.aws.test_state_utils.generate_test_state(
                enforced_state={},
                desired_state={
                    "name": name,
                    "scope": scope,
                    "description": description,
                    "ip_address_version": ip_address_version,
                    "addresses": addresses,
                    "tags": tags,
                },
            )
            result["comment"] = hub.tool.aws.comment_utils.would_create_comment(
                resource_type="aws.wafv2.ip_set", name=name
            )
            return result
        else:
            # IPSet not present , create
            create_ret = await hub.exec.boto3.client.wafv2.create_ip_set(
                ctx,
                Name=name,
                Scope=scope,
                Description=description,
                IPAddressVersion=ip_address_version,
                Addresses=addresses,
                Tags=tags
                if type(tags) == list
                else hub.tool.aws.tag_utils.convert_tag_dict_to_list(tags),
            )
            if not create_ret["result"]:
                result["result"] = False
                result["comment"] = create_ret["comment"]
                return result
            resource_id = create_ret["ret"]["Summary"]["Id"]
            result["comment"] = hub.tool.aws.comment_utils.create_comment(
                resource_type="aws.wafv2.ip_set", name=name
            )

    if (not result["old_state"]) or resource_updated:
        after_ret = await hub.exec.aws.wafv2.ip_set.get(
            ctx, name=name, scope=scope, resource_id=resource_id
        )
        if not after_ret["result"]:
            result["result"] = False
            result["comment"] += after_ret["comment"]
            return result
        result["new_state"] = after_ret["ret"]
    else:
        result["new_state"] = copy.deepcopy(result["old_state"])
    return result


async def absent(
    hub, ctx, name: str, scope: str, resource_id: str = None
) -> Dict[str, Any]:
    """Deletes the IPSet for the AWS WAFV2 associated with a Web ACL.

    Args:
        name(str):
            The name of the IP set. You cannot change the name of an IPSet after you create it.
        scope(str):
            Specifies whether this is for an Amazon CloudFront distribution or for a Regional application.
            A ``Regional`` application can be an Application Load Balancer (ALB), an Amazon API Gateway REST API, or an AppSync GraphQL API.
            To work with CloudFront, you must also specify the Region US East (N. Virginia) as follows:
            CLI - Specify the Region when you use the CloudFront scope: ``--scope=CLOUDFRONT --region=us-east-1`` .
            API and SDKs - For all calls, use the Region endpoint us-east-1.
            For regional applications, you can use any of the endpoints in the list. A regional application can be an
            Application Load Balancer (ALB), an Amazon API Gateway REST API, an AppSync GraphQL API, or an Amazon Cognito user pool.
            For Amazon CloudFront applications, you must use the API endpoint listed for US East (N. Virginia): us-east-1.
        resource_id(str, Optional):
            A unique identifier for the set. This ID is returned in the responses to create and list commands.
            You provide it to operations like update and delete. Idem automatically considers this resource being absent
            if this field is not specified.

    Request Syntax:
        .. code-block:: sls

            [my_idem_ip_set_absent_test]:
                aws.wafv2.ip_set.absent:
                    - name: 'string'
                    - scope: 'string'
                    - resource_id: 'string'

    Returns:
        Dict[str, Any]

    Examples:
        .. code-block:: sls

            [my_idem_ip_set_absent_test]:
                aws.wafv2.ip_set.absent:
                    - name: test-wafv2-ip-set-1663200539
                    - scope: REGIONAL
                    - resource_id: f547799f-e325-4876-9e0e-264d835eb3fd
    """
    result = dict(comment=[], old_state=None, new_state=None, name=name, result=True)
    if not resource_id:
        result["comment"] = hub.tool.aws.comment_utils.already_absent_comment(
            resource_type="aws.wafv2.ip_set", name=name
        )
        return result
    before = await hub.exec.aws.wafv2.ip_set.get(
        ctx,
        name=name,
        scope=scope,
        resource_id=resource_id,
    )
    if not before["result"]:
        result["comment"] = before["comment"]
        result["result"] = False
        return result
    if not before["ret"]:
        result["comment"] = hub.tool.aws.comment_utils.already_absent_comment(
            resource_type="aws.wafv2.ip_set", name=name
        )
    elif ctx.get("test", False):
        result["old_state"] = before["ret"]
        result["comment"] = hub.tool.aws.comment_utils.would_delete_comment(
            resource_type="aws.wafv2.ip_set", name=name
        )
        return result
    else:
        lock_token = before["ret"]["lock_token"]
        result["old_state"] = before["ret"]
        delete_ret = await hub.exec.boto3.client.wafv2.delete_ip_set(
            ctx, Name=name, Scope=scope, Id=resource_id, LockToken=lock_token
        )
        result["result"] = delete_ret["result"]
        if not result["result"]:
            result["comment"] = delete_ret["comment"]
            result["result"] = False
            return result
        result["comment"] = hub.tool.aws.comment_utils.delete_comment(
            resource_type="aws.wafv2.ip_set", name=name
        )
    return result


async def describe(hub, ctx) -> Dict[str, Dict[str, Any]]:
    """The goal of the describe function is to provide users a way to generate an SLS output.

    This sls output can be used to regenerate or update the IPSet resource on AWS.

    Returns:
        Dict[str, Dict[str, Any]]

    Examples:
        Calling from the CLI:
            .. code-block:: bash

                idem describe aws.wafv2.ip_set --acct-profile <environment>
    """
    result = {}
    scopes = ["CLOUDFRONT", "REGIONAL"]
    for scope in scopes:
        ret = await hub.exec.aws.wafv2.ip_set.list(ctx, scope=scope)
        if not ret["result"]:
            hub.log.warning(f"Could not list ip_set " f"{ret['comment']}")
            continue
        for ip_set in ret["ret"]:
            ipset_name = ip_set["ret"]["name"]
            result[ipset_name] = {
                "aws.wafv2.ip_set.present": [
                    {parameter_key: parameter_value}
                    for parameter_key, parameter_value in ip_set["ret"].items()
                ]
            }
    return result
