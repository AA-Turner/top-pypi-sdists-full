"""Exec module for managing Amazon Elasticsearch Service Domain"""


async def get(
    hub,
    ctx,
    name: str,
    resource_id: str,
):
    """Get the domain configuration information about the specified Elasticsearch domain

    Args:
        name(str): An Idem name of the resource.
        resource_id(str): The name of the Elasticsearch domain.

    Returns:
        .. code-block:: python

           {"result": True|False, "comment": A message List, "ret": None|Dict}

    Examples:
        Using in a state:

        .. code-block:: yaml

            my_unmanaged_resource:
              exec.run:
                - path: aws.es.elasticsearch_domain.get
                - kwargs:
                    name: my_resource
                    resource_id: resource_id

        Calling this exec function from the cli with resource_id:

        .. code-block:: bash

            idem exec aws.es.elasticsearch_domain.get resource_id="resource_id" name="name"

    """
    result = dict(comment=[], ret=None, result=True)

    get_domain_ret = await hub.exec.boto3.client.es.describe_elasticsearch_domain(
        ctx, DomainName=resource_id
    )

    if not get_domain_ret["result"]:
        if "ResourceNotFoundException" in str(get_domain_ret["comment"]):
            result["comment"].append(
                hub.tool.aws.comment_utils.get_empty_comment(
                    resource_type="aws.es.elasticsearch_domain", name=name
                )
            )
            result["comment"] += list(get_domain_ret["comment"])
            return result
        result["result"] = False
        result["comment"] = list(get_domain_ret["comment"])
        return result

    elasticsearch_domain = get_domain_ret["ret"].get("DomainStatus")
    arn = elasticsearch_domain.get("ARN")

    tags_ret = await hub.exec.boto3.client.es.list_tags(ctx, ARN=arn)
    tags = []
    if not tags_ret["result"]:
        result["comment"] = list(tags_ret["comment"])
        result["result"] = False
        return result
    else:
        if tags_ret["ret"] and tags_ret.get("ret").get("TagList"):
            tags = tags_ret.get("ret").get("TagList")

    result[
        "ret"
    ] = hub.tool.aws.es.elasticsearch_domain.convert_raw_elasticsearch_domain_to_present(
        elasticsearch_domain,
        tags=hub.tool.aws.tag_utils.convert_tag_list_to_dict(tags),
    )

    return result
