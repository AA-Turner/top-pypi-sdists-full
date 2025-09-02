"""Exec module for managing Amazon API Rest APIs."""


async def get(hub, ctx, name: str, resource_id: str):
    """Returns a rest api, including their root resource id.

    Args:
        name (str): idem name associated with this resource_id.

        resource_id (str): id of the specific rest_api to look up.

    Returns:
        dict[str, Any]:
            Returns details of a rest_api.

    Examples:

        .. code-block:: bash

            idem exec aws.apigateway.rest_api.get name=test_rest_api resource_id=xvwtynovjx --output json

                Call from code:

        .. code-block:: python

            async def my_func(hub, ctx, name:str, resource_id:str):
                await hub.exec.aws.apigateway.rest_api.get(ctx, name, resource_id, api_id)

        Normally, rest_api would be managed via aws.apigateway.rest_api.present, but using get in a state is possible:

        .. code-block:: yaml

            my_unmanaged_rest_api:
              exec.run:
                - path: aws.apigateway.rest_api.get
                - kwargs:
                    name: my_resource
                    resource_id: resource_id

    """
    result = dict(comment=[], ret=None, result=True)

    # find the rest_api
    partial_rest_api = await hub.exec.boto3.client.apigateway.get_rest_api(
        ctx, restApiId=resource_id
    )
    if not partial_rest_api["result"]:
        result["comment"] += partial_rest_api["comment"]
        result["result"] = False
        return result

    # find the id for the root resource ("/").
    resources = await hub.exec.boto3.client.apigateway.get_resources(
        ctx, restApiId=resource_id
    )
    if not resources["result"]:
        result["comment"] += [
            f"Unable to load root resource for rest_api '{partial_rest_api['ret']['name']}'. "
            f"This is likely a temporary issue."
        ]
        result["comment"] += resources["comment"]
        result["result"] = False
        return result
    root_resource_id = None
    for resource in resources["ret"]["items"]:
        if resource["path"] == "/":
            root_resource_id = resource["id"]
            break
    partial_rest_api["ret"]["rootResourceId"] = root_resource_id

    # convert to expected format
    result["ret"] = hub.tool.aws.apigateway.rest_api.convert_raw_rest_api_to_present(
        partial_rest_api["ret"], idem_resource_name=name
    )

    return result
