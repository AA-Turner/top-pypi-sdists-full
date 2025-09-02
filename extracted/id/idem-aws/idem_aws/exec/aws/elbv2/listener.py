from typing import Dict


async def get(
    hub,
    ctx,
    name: str,
    resource_id: str = None,
    load_balancer_arn: str = None,
) -> Dict:
    """
    Pass required params to get a target group resource.

    Users can specify one of the following two to fetch results: ARN of the load balancer, or an ARN of the listener.
    Here ARN of the listener takes precedence during search i.e. if both the fields from above are present, search is
    done with LB arn.

    Args:
        name(str):
            The name of the Idem state.

        resource_id(str, Optional):
            AWS ElasticLoadBalancingv2 Listener ARN to identify the listener resource.

        load_balancer_arn((str, Optional):
            The Amazon Resource Name (ARN) of the ElasticLoadBalancingv2 load balancer.
    """
    result = dict(comment=[], ret=None, result=True)
    ret = await hub.tool.aws.elbv2.listener.search_raw(
        ctx=ctx,
        resource_id=resource_id,
        load_balancer_arn=load_balancer_arn,
    )
    if not ret["result"]:
        if "ListenerNotFoundException" in str(ret["comment"]):
            result["comment"].append(
                hub.tool.aws.comment_utils.get_empty_comment(
                    resource_type="aws.elbv2.listener", name=name
                )
            )
            result["comment"] += list(ret["comment"])
            return result
        result["comment"] += list(ret["comment"])
        result["result"] = False
        return result
    if not ret["ret"]["Listeners"]:
        result["comment"].append(
            hub.tool.aws.comment_utils.get_empty_comment(
                resource_type="aws.elbv2.listener", name=name
            )
        )
        return result

    resource_id = ret["ret"]["Listeners"][0].get("ListenerArn")
    if len(ret["ret"]["Listeners"]) > 1:
        result["comment"].append(
            f"More than one aws.elbv2.listener resource was found. Use resource {resource_id}"
        )
    tags = certificates = []
    tags_ret = await hub.exec.boto3.client.elbv2.describe_tags(
        ctx, ResourceArns=[resource_id]
    )
    if not tags_ret["result"]:
        result["comment"] = list(tags_ret["comment"])
        result["result"] = False
        return result
    else:
        if tags_ret["ret"] and tags_ret.get("ret")["TagDescriptions"]:
            tags = (tags_ret["ret"]["TagDescriptions"][0]).get("Tags")

    # Listeners of type other than HTTPS & TLS don't need a certificate associated
    # with them. When this call is executed for such listeners, it returns 'False'.
    certificates_ret = await hub.exec.boto3.client.elbv2.describe_listener_certificates(
        ctx, ListenerArn=resource_id
    )
    if not certificates_ret["result"]:
        result["comment"] = list(certificates_ret["comment"])
    else:
        if certificates_ret.get("ret") and certificates_ret.get("ret").get(
            "Certificates"
        ):
            certificates = certificates_ret["ret"].get("Certificates")

    result["ret"] = hub.tool.aws.elbv2.conversion_utils.convert_raw_listener_to_present(
        raw_resource=ret["ret"]["Listeners"][0],
        idem_resource_name=name,
        tags=hub.tool.aws.tag_utils.convert_tag_list_to_dict(tags),
        certificates=certificates,
    )
    return result
