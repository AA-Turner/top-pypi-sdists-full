"""State module for managing Amazon WAF v2 web ACL associations."""
import asyncio
import copy
from typing import Any
from typing import Dict

__contracts__ = ["resource"]


async def present(
    hub,
    ctx,
    name: str,
    web_acl_arn: str,
    resource_arn: str,
    resource_id: str = None,
) -> Dict[str, Any]:
    """Associates a web ACL with a regional application resource, to protect the resource.

    A regional application can be an Application Load Balancer (ALB), an Amazon API Gateway REST API, an AppSync GraphQL API,
    or an Amazon Cognito user pool.

    Args:
        name(str):
            An Idem name of the resource.
        resource_id(str, Optional):
            The Amazon Resource Name (ARN) of the resource associated with the web ACL.
        web_acl_arn(str):
            The Amazon Resource Name (ARN) of the web ACL that you want to associate with the resource.
        resource_arn(str):
            The Amazon Resource Name (ARN) of the resource to associate with the web ACL.
            The ARN must be in one of the following formats:

            * For an Application Load Balancer: ``arn:aws:elasticloadbalancing:region:account-id:loadbalancer/app/load-balancer-name/load-balancer-id``
            * For an Amazon API Gateway REST API: ``arn:aws:apigateway:region::/restapis/api-id/stages/stage-name``
            * For an AppSync GraphQL API: ``arn:aws:appsync:region:account-id:apis/GraphQLApiId``
            * For an Amazon Cognito user pool: ``arn:aws:cognito-idp:region:account-id:userpool/user-pool-id``

    Returns:
        Dict[str, Any]

    Request syntax:
      .. code-block:: sls

        [idem_test_aws_wafv2_associate_web_acl]:
          aws.wafv2.associate_web_acl.present:
            - name: 'string'
            - resource_id: 'string'
            - web_acl_arn: 'string'
            - resource_arn: 'string'

    Returns:
        Dict[str, Any]

    Examples:
        .. code-block:: sls

            idem_test_aws_wafv2_associate_web_acl:
              aws.wafv2.associate_web_acl.present:
                - name: 'idem_test_associate_web_acl'
                - web_acl_arn: 'arn:aws:wafv2:us-west-2:123456789012:regional/webacl/idem_test_web_acl/e3706582-69b0-4487-97b6-63f82b8a3147'
                - resource_arn: 'arn:aws:apigateway:us-west-2::/restapis/1234567890/stages/dev'
    """
    result = dict(comment=[], old_state=None, new_state=None, name=name, result=True)
    before = await hub.exec.boto3.client.wafv2.get_web_acl_for_resource(
        ctx, ResourceArn=resource_arn
    )
    if not before["result"]:
        result["result"] = False
        result["comment"] = before["comment"]
        return result
    if before["ret"].get("WebACL", None):
        result[
            "old_state"
        ] = hub.tool.aws.wafv2.conversion_utils.convert_raw_web_acl_resource_association_to_present(
            web_acl_arn=web_acl_arn, resource_arn=resource_arn, idem_resource_name=name
        )
        result["new_state"] = copy.deepcopy(result["old_state"])
        result["comment"] += [f"aws.waf.web_acl_association '{name}' already exists"]
    else:
        if ctx.get("test", False):
            result["new_state"] = hub.tool.aws.test_state_utils.generate_test_state(
                enforced_state={},
                desired_state={
                    "name": name,
                    "web_acl_arn": web_acl_arn,
                    "resource_arn": resource_arn,
                },
            )
            result["comment"] += [f"Would create aws.waf.web_acl_association '{name}'"]
            return result
        for i in range(5):
            # Handling association to a newly created web ACL
            ret = await hub.exec.boto3.client.wafv2.associate_web_acl(
                ctx,
                WebACLArn=web_acl_arn,
                ResourceArn=resource_arn,
            )
            if ret["result"]:
                break
            else:
                # Waiting for web_acl to be in consumable state
                if "WAFUnavailableEntityException" in str(ret["comment"]):
                    await asyncio.sleep(60)
        result["result"] = ret["result"]
        if not result["result"]:
            result["comment"] += ret["comment"]
            return result
        result["comment"] += [f"Created aws.waf.web_acl_association '{name}'"]
        result[
            "new_state"
        ] = hub.tool.aws.wafv2.conversion_utils.convert_raw_web_acl_resource_association_to_present(
            web_acl_arn=web_acl_arn, resource_arn=resource_arn, idem_resource_name=name
        )
    return result


async def absent(
    hub,
    ctx,
    name: str,
    resource_id: str = None,
) -> Dict[str, Any]:
    """Disassociates the specified regional resource from any existing web ACL association.

    A resource can have at most one web ACL association. A regional application can be an Application Load Balancer (ALB),
    an Amazon API Gateway REST API, an AppSync GraphQL API, or an Amazon Cognito user pool.

    Args:
        name(str):
            An Idem name of the resource.
        resource_id(str, Optional):
            The Amazon Resource Name (ARN) of the resource associated with the web ACL.

            .. warning::
              Idem automatically considers this resource being absent if this field is not specified.

    Returns:
        Dict[str, Any]

    Request syntax:
      .. code-block:: sls

        [idem_test_aws_wafv2_associate_web_acl]:
          aws.wafv2.associate_web_acl.absent:
            - name: 'string'
            - resource_id: 'string'

    Returns:
        Dict[str, Any]

    Examples:
        .. code-block:: sls

            idem_test_aws_wafv2_associate_web_acl:
              aws.wafv2.associate_web_acl.absent:
                - name: 'idem_test_associate_web_acl'
                - resource_id: 'arn:aws:apigateway:us-west-2::/restapis/1234567890/stages/dev'
    """
    result = dict(comment=[], old_state=None, new_state=None, name=name, result=True)
    if not resource_id:
        result["comment"] = hub.tool.aws.comment_utils.already_absent_comment(
            resource_type="aws.wafv2.associate_web_acl", name=name
        )
        return result
    before = await hub.exec.boto3.client.wafv2.get_web_acl_for_resource(
        ctx, ResourceArn=resource_id
    )
    if not before["result"]:
        if "Invalid type" in str(before["comment"]):
            result["comment"] = hub.tool.aws.comment_utils.already_absent_comment(
                resource_type="aws.wafv2.associate_web_acl", name=name
            )
        else:
            result["result"] = False
            result["comment"] = before["comment"]
        return result
    if before["ret"]:
        before = before["ret"].get("WebACL", None)
    if before is None:
        result["comment"] = hub.tool.aws.comment_utils.already_absent_comment(
            resource_type="aws.wafv2.associate_web_acl", name=name
        )
    else:
        web_acl_arn = before["ARN"]
        result[
            "old_state"
        ] = hub.tool.aws.wafv2.conversion_utils.convert_raw_web_acl_resource_association_to_present(
            web_acl_arn=web_acl_arn, resource_arn=resource_id, idem_resource_name=name
        )
        if ctx.get("test", False):
            result["comment"] += [
                f"Would disassociate aws.waf.web_acl_association '{name}'"
            ]
            return result
        else:
            ret = await hub.exec.boto3.client.wafv2.disassociate_web_acl(
                ctx,
                ResourceArn=resource_id,
            )
            result["result"] = ret["result"]
            if not result["result"]:
                result["comment"] = ret["comment"]
                result["result"] = False
                return result
            result["comment"] += [f"Deleted aws.waf.web_acl_association '{name}'"]
    return result


async def describe(hub, ctx) -> Dict[str, Dict[str, Any]]:
    """Describes AWS WAF v2 regional resources associations with web ACLs in a way that can be recreated/managed with the corresponding "present" function.

    Returns:
        Dict[str, Dict[str, Any]]

    Examples:
        .. code-block:: bash

            $ idem describe aws.wafv2.associate_web_acl
    """
    result = {}
    web_acls = await hub.exec.boto3.client.wafv2.list_web_acls(ctx, Scope="REGIONAL")
    resource_types = ["APPLICATION_LOAD_BALANCER", "API_GATEWAY", "APPSYNC"]
    if not web_acls["result"]:
        hub.log.warning(f"Could not retrieve list_web_acls {web_acls['comment']}")
        return {}

    web_acl_list = web_acls["ret"]["WebACLs"]
    for web_acl in web_acl_list:
        web_acl_arn = web_acl["ARN"]
        for resource_type in resource_types:
            resource_for_web_acl = (
                await hub.exec.boto3.client.wafv2.list_resources_for_web_acl(
                    ctx, WebACLArn=web_acl_arn, ResourceType=resource_type
                )
            )
            if not resource_for_web_acl["result"]:
                hub.log.debug(
                    f"Could not retrieve resource for web_acl {web_acls['comment']}"
                )
                continue
            for resource_arn in resource_for_web_acl["ret"]["ResourceArns"]:
                translated_resource = hub.tool.aws.wafv2.conversion_utils.convert_raw_web_acl_resource_association_to_present(
                    web_acl_arn=web_acl_arn,
                    resource_arn=resource_arn,
                    idem_resource_name=resource_arn,
                )
                result[translated_resource["resource_id"]] = {
                    "aws.wafv2.associate_web_acl.present": [
                        {parameter_key: parameter_value}
                        for parameter_key, parameter_value in translated_resource.items()
                    ]
                }

    return result
