"""Exec module for managing Amazon API Gateway Deployments."""


async def get(
    hub,
    ctx,
    resource_id: str,
    rest_api_id: str,
    name: str = None,
):
    """Get an API Gateway Deployments from AWS. If more than one resource is found, the first resource returned from AWS
    will be used. The function returns None when no resource is found.

    Args:
        resource_id(str):
            Resource ID of the AWS Deployment.

        rest_api_id(str):
            The string identifier of the associated RestApi.

        name(str, Optional):
            An Idem name of the API Gateway Deployment.

    Returns:
        .. code-block:: python

            {"result": True|False, "comment": A message List, "ret": Dict[str, Any]}

     Examples:

        Calling this exec module function from the cli with resource_id

        .. code-block:: bash

            idem exec aws.apigateway.deployment.get resource_id="resource_id" rest_api_id="rest_api_id"
            name="umanaged_deployment"


        Calling this exec module function from within a state module in pure python

        .. code-block:: yaml

            my_unmanaged_deployment:
              exec.run:
                - path: aws.apigateway.deployment.get
                - kwargs:
                    rest_api_id: 5hkdu2
                    resource_id: f8kils
                    name: test-deployments-name


    """

    result = dict(comment=[], ret=None, result=True)
    ret = await hub.exec.boto3.client.apigateway.get_deployment(
        ctx, restApiId=rest_api_id, deploymentId=resource_id
    )

    if not ret["result"]:
        if "NotFoundException" in str(ret["comment"]):
            result["comment"].append(
                hub.tool.aws.comment_utils.get_empty_comment(
                    resource_type="aws.apigateway.deployment", name=name
                )
            )
            result["comment"] += list(ret["comment"])
            return result
        result["comment"] += list(ret["comment"])
        result["result"] = False
        return result

    if not ret["ret"]:
        result["comment"].append(
            hub.tool.aws.comment_utils.get_empty_comment(
                resource_type="aws.apigateway.deployment", name=name
            )
        )
        return result

    else:
        result[
            "ret"
        ] = hub.tool.aws.apigateway.deployment.convert_raw_deployment_to_present(
            raw_resource=ret["ret"],
            resource_id=resource_id,
            rest_api_id=rest_api_id,
            idem_resource_name=name,
        )

    return result
