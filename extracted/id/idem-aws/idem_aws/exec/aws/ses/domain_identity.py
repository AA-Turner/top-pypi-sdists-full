"""Exec module for managing SES Domain Identity."""

__func_alias__ = {"list_": "list"}


async def get(hub, ctx, resource_id: str):
    """Get SES domain identity from AWS account.

    Get a single domain identity from AWS.

    Args:
        resource_id (str):
            The domain identity.
    Returns:
        Dict[str, Any]:
            Returns domain identity in present format

    Examples:
        Calling this exec module function from the cli

        .. code-block:: bash

            idem exec aws.ses.domain_identity.get resource_id="example.com"

        Using in a state:

        .. code-block:: yaml

            my_unmanaged_resource:
              exec.run:
                - path: aws.ses.domain_identity.get
                - kwargs:
                    resource_id:"example.com"
    """

    result = dict(comment=[], ret=None, result=True)

    ret = await hub.exec.aws.ses.domain_identity.list(ctx, [resource_id])

    if not ret["result"]:
        result["comment"] += list(ret["comment"])
        result["result"] = False
        return result

    if len(ret["ret"]) != 0:
        result["ret"] = ret["ret"][0]

    return result


async def list_(hub, ctx, identities: list = None):
    """List SES domain identities from AWS account.

    Fetch a list of domain identities from AWS. The function returns empty list when no resource is found.

    Args:
        identities (str, Optional):
            The domain identities.
            If no identity is specified, it will return all the identities present in AWS account.

    Returns:
        Dict[str, Any]:
            Return domain identities in present format

    Examples:
        Calling this exec module function from the cli

        .. code-block:: bash

            idem exec aws.ses.domain_identity.list identity=["example.com"]

        Using in a state:

        .. code-block:: yaml

            my_unmanaged_resource:
              exec.run:
                - path: aws.ses.domain_identity.list
                - kwargs:
                    identity:"example.com"
    """
    result = dict(comment=[], ret=[], result=True)

    if not identities:
        ret_list = await hub.exec.boto3.client.ses.list_identities(ctx)

        if not ret_list["result"]:
            result["comment"] += list(ret_list["comment"])
            result["result"] = False
            hub.log.debug(f"Could not list identities {ret_list['comment']}")
            return result

        if not ret_list.get("ret"):
            result["comment"] += ["No domain identities present"]
            return result
        identities = ret_list["ret"].get("Identities")

    ret = await hub.exec.boto3.client.ses.get_identity_verification_attributes(
        ctx, Identities=identities
    )

    if not ret["result"]:
        result["comment"] += list(ret["comment"])
        result["result"] = False
        return result

    identities = ret["ret"]["VerificationAttributes"]

    for identity in identities:
        result["ret"].append(
            hub.tool.aws.ses.conversion_utils.convert_raw_domain_identity_to_present(
                ctx,
                raw_resource=identity,
            )
        )

    return result
