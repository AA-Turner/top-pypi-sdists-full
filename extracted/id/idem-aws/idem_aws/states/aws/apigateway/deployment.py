"""State module for managing Amazon API Gateway Deployments."""
import copy
from dataclasses import field
from dataclasses import make_dataclass
from typing import Any
from typing import Dict

__contracts__ = ["resource"]


async def present(
    hub,
    ctx,
    name: str,
    rest_api_id: str,
    resource_id: str = None,
    stage_name: str = None,
    stage_description: str = None,
    description: str = None,
    cache_cluster_enabled: bool = None,
    cache_cluster_size: str = None,
    variables: Dict = None,
    canary_settings: make_dataclass(
        "canarySettings",
        [
            ("percentTraffic", str),
            ("stageVariableOverrides", Dict, field(default=None)),
        ],
    ) = None,
    tracing_enabled: bool = None,
) -> Dict[str, Any]:
    """Creates an API Gateway Deployment resource.

    Args:
        name(str):
            An Idem name of the resource.

        rest_api_id(str):
            The string identifier of the associated RestApi.

        resource_id(str, Optional):
            AWS API Gateway Deployment ID.

        stage_name(str, Optional):
            The name of the Stage resource for the Deployment resource to create. This parameter is only valid during
            creation. Defaults to None.

        stage_description(str, Optional):
            The description of the Stage resource for the Deployment resource to create. This parameter is only valid
            during creation. Defaults to None.

        description(str, Optional):
            The description for the Deployment resource to create. Defaults to None.

        cache_cluster_enabled(bool, Optional):
            Enables a cache cluster for the Stage resource specified in the input. This parameter is only valid during
            creation. Defaults to None.

        cache_cluster_size(str, Optional):
            Specifies the cache cluster size for the Stage resource specified in the input, if a cache cluster is enabled.
            This parameter is only valid during creation. Defaults to None.

        variables(dict, Optional):
            A map that defines the stage variables for the Stage resource that is associated with the new deployment.
            Variable names can have alphanumeric and underscore characters, and the values must match [A-Za-z0-9-._~:/?#&=,]+.
            This parameter is only valid during creation. Defaults to None.

        canary_settings(dict, Optional):
            The input configuration for the canary deployment when the deployment is a canary release deployment. This
            parameter is only valid during creation. Defaults to None.

        tracing_enabled(bool, Optional):
            Specifies whether active tracing with X-ray is enabled for the Stage. This parameter is only valid during
            creation. Defaults to None.

    Request Syntax:
        .. code-block:: sls

            [idem_test_aws_apigateway_deployment]:
            aws.apigateway.deployment.present:
                - name: 'string'
                - resource_id: 'string'
                - stage_name: 'string'
                - stage_description: 'string'
                - description: 'string'
                - cache_cluster_enabled: bool
                - cache_cluster_size: 'string'
                - variables:
                - 'string' : 'string'
                - canary_settings:
                - percentTraffic: float
                - stageVariableOverrides:
                    - 'string: 'string'
                useStageCache: bool
                - tracing_enabled: bool


    Returns:
        Dict[str, Any]

    Examples:
        .. code-block:: sls

            resource_is_present:
              aws.apigateway.deployment.present:
                - name: value
                - rest_api_id: value
    """
    result = dict(comment=[], old_state=None, new_state=None, name=name, result=True)

    before = None
    resource_updated = False
    if resource_id:
        before = await hub.exec.aws.apigateway.deployment.get(
            ctx,
            rest_api_id=rest_api_id,
            resource_id=resource_id,
            name=name,
        )
        if not before["result"] or not before["ret"]:
            result["comment"] = before["comment"]
            result["result"] = False
            return result

        result["old_state"] = before["ret"]
        result["new_state"] = copy.deepcopy(result["old_state"])

        updatable_parameters = {
            "description": description,
        }

        update_deployment_ret = await hub.tool.aws.apigateway.deployment.update(
            ctx,
            old_state=result["old_state"],
            updatable_parameters=updatable_parameters,
        )

        result["comment"] += update_deployment_ret["comment"]

        if not update_deployment_ret["result"]:
            result["result"] = False
            return result
        resource_updated = bool(update_deployment_ret["ret"])

    else:
        if ctx.get("test", False):
            result["new_state"] = hub.tool.aws.test_state_utils.generate_test_state(
                enforced_state={},
                desired_state={
                    "name": name,
                    "resource_id": resource_id,
                    "description": description,
                    "rest_api_id": rest_api_id,
                    "stage_name": stage_name,
                    "stage_description": stage_description,
                    "cache_cluster_enabled": cache_cluster_enabled,
                    "cache_cluster_size": cache_cluster_size,
                    "variables": variables,
                    "canary_settings": canary_settings,
                    "tracing_enabled": tracing_enabled,
                },
            )
            result["comment"] = hub.tool.aws.comment_utils.would_create_comment(
                resource_type="aws.apigateway.deployment", name=name
            )
            return result

        ret = await hub.exec.boto3.client.apigateway.create_deployment(
            ctx,
            restApiId=rest_api_id,
            stageName=stage_name,
            stageDescription=stage_description,
            description=description,
            cacheClusterEnabled=cache_cluster_enabled,
            cacheCluserSize=cache_cluster_size,
            variables=variables,
            canarySettings=canary_settings,
            tracingEnabled=tracing_enabled,
        )
        result["result"] = ret["result"]
        if not result["result"]:
            result["comment"] = ret["comment"]
            return result

        resource_id = ret["ret"]["id"]
        result["comment"] = hub.tool.aws.comment_utils.create_comment(
            resource_type="aws.apigateway.deployment", name=name
        )

    if (not before) or resource_updated:
        after = await hub.exec.aws.apigateway.deployment.get(
            ctx,
            name=name,
            resource_id=resource_id,
            rest_api_id=rest_api_id,
        )
        if not (after["result"] and after["ret"]):
            result["result"] = False
            result["comment"] += after["comment"]
            return result

        result["new_state"] = after["ret"]
    else:
        result["new_state"] = copy.deepcopy(result["old_state"])
    return result


async def absent(
    hub,
    ctx,
    name: str,
    rest_api_id: str = None,
    resource_id: str = None,
) -> Dict[str, Any]:
    """Deletes a Deployment resource.

    Deleting a deployment will only succeed if there are no Stage resources associated with it.

    Args:
        name(str):
            An Idem name of the resource.

        rest_api_id(str, Optional):
            The string identifier of the associated RestApi.

        resource_id(str, Optional):
            AWS API Gateway Deployment ID. Idem automatically considers this resource being absent if this field is not
            specified.

    Returns:
        Dict[str, Any]

    Examples:
        .. code-block:: sls

            resource_is_absent:
              aws.apigateway.deployment.absent:
                - name: value
                - resource_id: value
                - rest_api_id: value
    """
    result = dict(comment=[], old_state=None, new_state=None, name=name, result=True)

    if not resource_id:
        # if resource_id isn't specified, the resource is considered to be absent.
        result["comment"] = hub.tool.aws.comment_utils.already_absent_comment(
            resource_type="aws.apigateway.deployment", name=name
        )
        return result

    if not rest_api_id:
        result["comment"] = result[
            "comment"
        ] = hub.tool.aws.comment_utils.missing_args_for_absent_comment(
            resource_type="aws.apigateway.deployment", name=name, args=["rest_api_id"]
        )
        result["result"] = False
        return result

    before_ret = await hub.exec.aws.apigateway.deployment.get(
        ctx,
        name=name,
        resource_id=resource_id,
        rest_api_id=rest_api_id,
    )

    if not before_ret["result"]:
        result["result"] = False
        result["comment"] = before_ret["comment"]
        return result

    if not before_ret["ret"]:
        result["comment"] = hub.tool.aws.comment_utils.already_absent_comment(
            resource_type="aws.apigateway.deployment", name=name
        )
        return result

    elif ctx.get("test", False):
        result["old_state"] = before_ret["ret"]
        result["comment"] = hub.tool.aws.comment_utils.would_delete_comment(
            resource_type="aws.apigateway.deployment", name=name
        )
        return result

    else:
        result["old_state"] = before_ret["ret"]
        delete_ret = await hub.exec.boto3.client.apigateway.delete_deployment(
            ctx, restApiId=rest_api_id, deploymentId=resource_id
        )

        if not delete_ret["result"]:
            result["result"] = False
            result["comment"] = delete_ret["comment"]
            return result

        result["comment"] = hub.tool.aws.comment_utils.delete_comment(
            resource_type="aws.apigateway.deployment", name=name
        )
    return result


async def describe(hub, ctx) -> Dict[str, Dict[str, Any]]:
    """Describe the API Gateway Deployments.

    Returns a list of apigateway.deployment descriptions

    Returns:
        Dict[str, Any]


    Examples:
        .. code-block:: bash

            $ idem describe aws.apigateway.deployment

    """
    result = {}

    get_rest_apis_ret = await hub.exec.boto3.client.apigateway.get_rest_apis(ctx)
    if not get_rest_apis_ret["result"]:
        hub.log.warning(f"Could not get Rest Apis {get_rest_apis_ret['comment']}")
        return result

    if get_rest_apis_ret["ret"]["items"] is not None:
        for rest_api in get_rest_apis_ret["ret"]["items"]:
            rest_api_id = rest_api.get("id")
            get_deployments_ret = (
                await hub.exec.boto3.client.apigateway.get_deployments(
                    ctx, restApiId=rest_api_id
                )
            )
            if not get_deployments_ret["result"]:
                hub.log.debug(
                    f"Could not describe deployments for Rest API {get_deployments_ret['comment']}. Skipping this resource "
                    f"and continuing."
                )
                continue

            for deployment in get_deployments_ret["ret"]["items"]:
                resource_id = deployment.get("id")
                resource_translated = hub.tool.aws.apigateway.deployment.convert_raw_deployment_to_present(
                    raw_resource=deployment,
                    resource_id=resource_id,
                    rest_api_id=rest_api_id,
                )
                result[resource_translated["resource_id"]] = {
                    "aws.apigateway.deployment.present": [
                        {parameter_key: parameter_value}
                        for parameter_key, parameter_value in resource_translated.items()
                    ]
                }

    return result
