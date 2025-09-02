"""Exec module for managing Amazon API Gateway Stage."""


async def get(
    hub,
    ctx,
    resource_id: str,
):
    """Get an API Gateway Stage from AWS. If more than one resource is found, the first resource returned from AWS
        will be used. The function returns None when no resource is found.

    Args:
        resource_id(str):
            Idem Resource ID that is generated once the resource is created,
                formatted as: <rest_api_id>-<name>.

    Returns:
        .. code-block:: python

            {"result": True|False, "comment": A message List, "ret": Dict[str, Any]}

    Examples:

        Calling this exec module function from the cli with resource_id

        .. code-block:: bash

            idem exec aws.apigateway.stage.get resource_id="resource_id"


        Calling this exec module function from within a state module in pure python

        .. code-block:: yaml

            my_unmanaged_stack:
              exec.run:
                - path: aws.apigateway.stage.get
                - kwargs:
                    resource_id: '<rest_api_id>-<name>'

    """

    result = dict(comment=[], ret=None, result=True)
    if resource_id and len(resource_id.split("-")) == 2:
        rest_api_id, name = resource_id.split("-")
        ret = await hub.exec.boto3.client.apigateway.get_stage(
            ctx, restApiId=rest_api_id, stageName=name
        )

        if not ret["result"]:
            if "NotFoundException" in str(ret["comment"]):
                result["comment"].append(
                    hub.tool.aws.comment_utils.get_empty_comment(
                        resource_type="aws.apigateway.stage", name=name
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
                    resource_type="aws.apigateway.stage", name=name
                )
            )
            return result

        else:
            result["ret"] = hub.tool.aws.apigateway.stage.convert_raw_stage_to_present(
                raw_resource=ret["ret"],
                resource_id=resource_id,
            )

        return result

    else:
        result["comment"].append(
            f"Invalid Resource ID '{resource_id}'. Resource ID should be of format <rest_api_id>-<name>.",
        )
        result["result"] = False
        return result
