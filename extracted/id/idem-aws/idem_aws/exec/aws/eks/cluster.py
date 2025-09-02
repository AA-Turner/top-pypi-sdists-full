"""Exec module for managing EKS cluster."""


async def get(hub, ctx, name, resource_id: str):
    """Provides details about a specific cluster.

     Args:
         name (str):
             The name of the Idem state.

         resource_id (str):
             EKS cluster id to identify the resource.

    Returns:
         Dict[str, Any]:
             Returns ami in present format

     Examples:
         Calling this exec module function from the cli

         .. code-block:: bash

             idem exec aws.eks.cluster.get name="my_resource"

         Using in a state:

         .. code-block:: yaml

             my_unmanaged_resource:
               exec.run:
                 - path: aws.eks.cluster.get
                 - kwargs:
                     name: my_resource
    """
    result = dict(comment=[], ret=None, result=True)

    ret = await hub.exec.boto3.client.eks.describe_cluster(ctx, name=resource_id)

    if not ret["result"]:
        if "" in str(ret["comment"]) or "ResourceNotFoundException" in str(
            ret["comment"]
        ):
            result["comment"].append(
                hub.tool.aws.comment_utils.get_empty_comment(
                    resource_type="aws.eks.cluster", name=name
                )
            )
            result["comment"] += list(ret["comment"])
            return result
        # Failed to retrieve
        result["comment"] += list(ret["comment"])
        result["result"] = False
        return result

    result["ret"] = hub.tool.aws.eks.conversion_utils.convert_raw_cluster_to_present(
        raw_resource=ret["ret"]["cluster"],
        idem_resource_name=name,
    )

    return result
