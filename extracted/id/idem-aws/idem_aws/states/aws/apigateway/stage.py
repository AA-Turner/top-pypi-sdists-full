"""State module for managing Amazon API Gateway Stages."""
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
    deployment_id: str,
    resource_id: str = None,
    description: str = None,
    cache_cluster_enabled: bool = None,
    cache_cluster_size: str = None,
    variables: dict = None,
    documentation_version: str = None,
    canary_settings: make_dataclass(
        "canarySettings",
        [
            ("percentTraffic", float),
            ("stageVariableOverrides", Dict, field(default=None)),
            ("deploymentId", str, field(default=None)),
        ],
    ) = None,
    tracing_enabled: bool = None,
    tags: dict = None,
):
    """Creates a new API Gateway Stage or modifies an existing one.

    Args:
        name(str):
            An Idem name of the resource. Stage names can only contain alphanumeric characters, hyphens, and underscores.
            Maximum length is 128 characters.

        rest_api_id(str):
            The string identifier of the associated RestApi.

        deployment_id(str):
            The identifier of the Deployment resource for the Stage resource.

        resource_id(str, Optional):
            AWS API Gateway Stage ID, in the form of '<rest_api_id>-<name>'.

        description(str, Optional):
            The description of the Stage resource.

        cache_cluster_enabled(bool, Optional):
            Whether cache clustering is enabled for the stage.

        cache_cluster_size(str, Optional):
            The stage's cache cluster size.

        variables(dict, Optional):
            A map that defines the stage variables for the new Stage resource. Variable names can have alphanumeric and
            underscore characters, and the values must match [A-Za-z0-9-._~:/?#&=,]+ .

        documentation_version(str, Optional):
            The version of the associated API documentation.

        canary_settings(dict, Optional):
            The canary deployment settings of this stage.

            * percentTraffic (float) --
            The percent (0-100) of traffic diverted to a canary deployment.

            * deploymentId (string) --
            The ID of the canary deployment.

            * stageVariableOverrides (dict) --
            Stage variables overridden for a canary release deployment, including new stage variables introduced in the
            canary. These stage variables are represented as a string-to-string map between stage variable names and
            their values. Dict of string: string.

            * useStageCache (boolean) --
            A Boolean flag to indicate whether the canary deployment uses the stage cache or not.

        tracing_enabled(bool, Optional):
            Specifies whether active tracing with X-ray is enabled for the Stage.

        tags(dict, Optional):
            The key-value map of strings. The valid character set is [a-zA-Z+-=._:/]. The tag key can be up to 128
            characters and must not start with aws: . The tag value can be up to 256 characters.

    Request Syntax:
        [idem_test_aws_apigateway_stage]:
          aws.apigateway.stage.present:
            - name: 'string'
            - description: 'string'
            - rest_api_id: 'string'
            - deployment_id: 'string'
            - resource_id: 'string-string'
            - cache_cluster_enabled: bool
            - cache_cluster_size: 'string'
            - variables:
                - 'string' : 'string'
            - canary_settings:
                - percentTraffic: float
                - deploymentId: 'string'
                - useStageCache: bool
            - tracing_enabled: bool
            - document_version: 'string'
            - tags:
                - 'string': 'string'

    Returns:
        Dict[str, Any]

    Examples:
        .. code-block:: sls

            resource_is_present:
              aws.apigateway.stage.present:
                - name: value
                - rest_api_id: value
                - deployment_id: value

    """

    result = dict(comment=[], old_state=None, new_state=None, name=name, result=True)

    before = None
    resource_updated = False

    if resource_id:
        before = await hub.exec.aws.apigateway.stage.get(
            ctx,
            resource_id=resource_id,
        )

        if not before["result"] or not before["ret"]:
            result["comment"] = before["comment"]
            result["result"] = False
            return result

        result["old_state"] = before["ret"]
        result["new_state"] = copy.deepcopy(result["old_state"])

        updateable_parameters = {
            "cache_cluster_enabled": cache_cluster_enabled,
            "cache_cluster_size": cache_cluster_size,
            "deployment_id": deployment_id,
            "description": description,
            "variables": variables,
            "tracing_enabled": tracing_enabled,
        }

        update_stage_ret = await hub.tool.aws.apigateway.stage.update(
            ctx,
            old_state=result["old_state"],
            updateable_parameters=updateable_parameters,
        )

        result["comment"] += update_stage_ret["comment"]

        if not update_stage_ret["result"]:
            result["result"] = False
            return result
        resource_updated = bool(update_stage_ret["ret"])
        if resource_updated and ctx.get("test", False):
            result["new_state"] = update_stage_ret["ret"]

        resource_arn = hub.tool.aws.arn_utils.build(
            service="apigateway",
            region=ctx["acct"]["region_name"],
            resource="/restapis/" + rest_api_id + "/stages/" + name,
        )

        if tags is not None and tags != result["old_state"].get("tags", {}):
            update_tags_ret = await hub.tool.aws.apigateway.tag.update(
                ctx,
                resource_arn=resource_arn,
                old_tags=result["old_state"].get("tags", {}),
                new_tags=tags,
            )
            if not update_tags_ret["result"]:
                result["result"] = False
                result["comment"] = update_tags_ret["comment"]
                return result
            result["comment"] += update_tags_ret["comment"]

            resource_updated = resource_updated or update_tags_ret["result"]
            if resource_updated and ctx.get("test", False):
                result["new_state"]["tags"] = (
                    update_tags_ret["ret"] if update_tags_ret["ret"] else None
                )

    else:
        if ctx.get("test", False):
            result["new_state"] = hub.tool.aws.test_state_utils.generate_test_state(
                enforced_state={},
                desired_state={
                    "name": name,
                    "resource_id": resource_id,
                    "description": description,
                    "rest_api_id": rest_api_id,
                    "deployment_id": deployment_id,
                    "cache_cluster_enabled": cache_cluster_enabled,
                    "cache_cluster_size": cache_cluster_size,
                    "variables": variables,
                    "canary_settings": canary_settings,
                    "tracing_enabled": tracing_enabled,
                    "documentation_version": documentation_version,
                    "tags": tags,
                },
            )
            result["comment"] = hub.tool.aws.comment_utils.would_create_comment(
                resource_type="aws.apigateway.stage", name=name
            )
            return result

        resource_id = f"{rest_api_id}-{name}"

        ret = await hub.exec.boto3.client.apigateway.create_stage(
            ctx,
            restApiId=rest_api_id,
            stageName=name,
            deploymentId=deployment_id,
            description=description,
            cacheClusterEnabled=cache_cluster_enabled,
            cacheClusterSize=cache_cluster_size,
            variables=variables,
            documentationVersion=documentation_version,
            tracingEnabled=tracing_enabled,
            canarySettings=canary_settings,
            tags=tags,
        )
        result["result"] = ret["result"]
        if not result["result"]:
            result["comment"] = ret["comment"]
            return result

        result["comment"] = hub.tool.aws.comment_utils.create_comment(
            resource_type="aws.apigateway.stage", name=name
        )

    if ctx.get("test", False) and resource_updated:
        return result

    elif (not before) or resource_updated:
        after = await hub.exec.aws.apigateway.stage.get(
            ctx,
            resource_id=resource_id,
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
    resource_id: str = None,
) -> Dict[str, Any]:
    """Deletes a Stage resource.

    Args:
        name(str):
            An Idem name of the resource.

        resource_id(str, Optional):
            AWS API Gateway Stage ID. Idem automatically considers this resource being absent if this field is not
            specified. in the form of '<rest_api_id>-<name>'

    Returns:
        Dict[str, Any]

    Examples:

        .. code-block:: sls

            resource_is_absent:
              aws.apigateway.stage.absent:
                - name: value
                - resource_id: value
    """

    result = dict(comment=[], old_state=None, new_state=None, name=name, result=True)

    if not resource_id:
        # if resource_id isn't specified, the resource is considered to be absent.
        result["comment"] = hub.tool.aws.comment_utils.already_absent_comment(
            resource_type="aws.apigateway.stage", name=name
        )
        return result

    before_ret = await hub.exec.aws.apigateway.stage.get(
        ctx,
        resource_id=resource_id,
    )

    if not before_ret["result"]:
        result["result"] = False
        result["comment"] = before_ret["comment"]
        return result

    if not before_ret["ret"]:
        result["comment"] = hub.tool.aws.comment_utils.already_absent_comment(
            resource_type="aws.apigateway.stage", name=name
        )
        return result

    elif ctx.get("test", False):
        result["old_state"] = before_ret["ret"]
        result["comment"] = hub.tool.aws.comment_utils.would_delete_comment(
            resource_type="aws.apigateway.stage", name=name
        )
        return result

    else:
        rest_api_id, name = resource_id.split("-")
        result["old_state"] = before_ret["ret"]
        delete_ret = await hub.exec.boto3.client.apigateway.delete_stage(
            ctx, restApiId=rest_api_id, stageName=name
        )

        if not delete_ret["result"]:
            result["result"] = False
            result["comment"] = delete_ret["comment"]
            return result

        result["comment"] = hub.tool.aws.comment_utils.delete_comment(
            resource_type="aws.apigateway.stage", name=name
        )
    return result


async def describe(hub, ctx) -> Dict[str, Dict[str, Any]]:
    """Describe the API Gateway Stages.

    Returns a list of apigateway.stage descriptions

    Returns:
        Dict[str, Any]


    Examples:

        .. code-block:: bash

            $ idem describe aws.apigateway.stage

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
                resource_id = deployment.get("resource_id")
                get_stages = await hub.exec.boto3.client.apigateway.get_stages(
                    ctx,
                    restApiId=rest_api_id,
                    deploymentId=resource_id,
                )
                if not get_stages["result"]:
                    hub.log.warning(f"Could not get Stages {get_stages['comment']}")
                    continue

                for stage in get_stages["ret"]["item"]:
                    stage_name = stage.get("stageName")
                    stage_id = f"{rest_api_id}-{stage_name}"
                    resource_translated = (
                        hub.tool.aws.apigateway.stage.convert_raw_stage_to_present(
                            raw_resource=stage,
                            resource_id=stage_id,
                        )
                    )
                    result[resource_translated["resource_id"]] = {
                        "aws.apigateway.stage.present": [
                            {parameter_key: parameter_value}
                            for parameter_key, parameter_value in resource_translated.items()
                        ]
                    }

    return result
