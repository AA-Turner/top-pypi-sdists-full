"""Exec module for managing Amazon Application Autoscaling scalable target."""
from typing import Dict
from typing import List


async def get(
    hub,
    ctx,
    name,
    service_namespace: str,
    scaling_resource_ids: List[str] = None,
    scalable_dimension: str = None,
) -> Dict:
    """Use an un-managed scaling target as a data-source. Supply one of the inputs as the filter.

    Args:
        name(str):
            The name of the Idem state.

        service_namespace(str):
            The namespace of the Amazon Web Services service that provides the resource.
            For a resource provided by your own application or service, use custom-resource instead.

        scalable_dimension(str):
            The scalable dimension. This string consists of the service namespace, resource type,
            and scaling property. ecs:service:DesiredCount

        scaling_resource_ids(list[str], Optional):
            The identifier of the resource associated with the scaling target.
            This string consists of the resource type and unique identifier.

    Returns:
        .. code-block:: python

            {"result": True|False, "comment": A message List, "ret": None|Dict}

    Examples:
        Calling this exec module function from the cli with service_namespace

        .. code-block:: bash

            idem exec aws.application_autoscaling.scalable_target.get service_namespace="service_namespace"

        Calling this exec module function from within a state module in pure python.

        .. code-block:: python

            async def state_function(hub, ctx, name, service_namespace, scaling_resource_id, scalable_dimension):
                before = await hub.exec.aws.application_autoscaling.scalable_target.get(
                ctx=ctx,
                name=name,
                service_namespace=service_namespace,
                scaling_resource_ids=[scaling_resource_id],
                scalable_dimension=scalable_dimension,
            )
    """
    result = dict(comment=[], ret=None, result=True)
    ret = await hub.exec.boto3.client[
        "application-autoscaling"
    ].describe_scalable_targets(
        ctx=ctx,
        ServiceNamespace=service_namespace,
        ResourceIds=scaling_resource_ids,
        ScalableDimension=scalable_dimension,
    )
    if not ret["result"]:
        result["comment"] = ret["comment"]
        result["result"] = False
        return result
    if not ret["ret"]["ScalableTargets"]:
        result["comment"].append(
            hub.tool.aws.comment_utils.get_empty_comment(
                resource_type="aws.application_autoscaling.scaling_target", name=name
            )
        )
        return result

    resource = ret["ret"]["ScalableTargets"][0]
    if len(ret["ret"]["ScalableTargets"]) > 1:
        result["comment"].append(
            f"More than one aws.application_autoscaling.scaling_target resource was found. Use resource {resource.get('ResourceId')}"
        )
    result[
        "ret"
    ] = hub.tool.aws.application_autoscaling.conversion_utils.convert_raw_scaling_target_to_present(
        ctx, raw_resource=resource, idem_resource_name=name
    )
    return result
