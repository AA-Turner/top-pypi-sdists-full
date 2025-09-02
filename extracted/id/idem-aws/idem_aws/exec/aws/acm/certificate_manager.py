"""Exec module for managing managing ACM certificates."""
from typing import Dict


async def get(
    hub,
    ctx,
    name: str,
    resource_id: str,
) -> Dict:
    """Retrieves the specified ACM certificate.

    Use an un-managed ACM certificate as a data-source.

    Args:
        name(str):
            The name of the Idem state.

        resource_id(str):
            The Amazon Resource Name (ARN) of certificate to identify the resource.

    Returns:
        Dict[str, Any]:
            Returns certificate_manager in present format

    Examples:
        Calling this exec module function from the cli with resource_id

        .. code-block:: bash

            idem exec aws.acm.certificate_manager.get name="unmanaged_certificate" resource_id="resource_id"

        Using in a state:

        .. code-block:: yaml

            my_unmanaged_resource:
              exec.run:
                - path: aws.acm.certificate_manager.get
                - kwargs:
                    name: my_resource
                    resource_id: resource_id

    """
    result = dict(comment=[], ret=None, result=True)
    ret = await hub.exec.boto3.client.acm.describe_certificate(
        ctx, CertificateArn=resource_id
    )

    if not ret["result"]:
        if "ResourceNotFoundException" in str(ret["comment"]):
            result["comment"].append(
                hub.tool.aws.comment_utils.get_empty_comment(
                    resource_type="aws.acm.certificate_manager", name=name
                )
            )
            result["comment"] += list(ret["comment"])
            return result
        result["comment"] += list(ret["comment"])
        result["result"] = False
        return result

    if ret["ret"]:
        result = (
            await hub.tool.aws.acm.conversion_utils.convert_raw_acm_to_present_async(
                ctx,
                raw_resource=ret["ret"].get("Certificate"),
                idem_resource_name=name,
            )
        )

    return result
