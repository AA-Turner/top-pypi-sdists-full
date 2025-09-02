from typing import Dict

__contracts__ = ["soft_fail"]


def build(
    hub,
    ctx,
    service: str,
    resource: str,
    partition: str = "aws",
    region: str = None,
    account_id: str = None,
) -> Dict:
    """
    Returns the ARN string from parameters.

    Args:
        hub: The redistributed pop central hub.
        ctx: The context.
        service(str): The service namespace that identifies the AWS product (for example, Amazon S3, IAM, or Amazon RDS). For a list of
                namespaces, see http://docs.aws.amazon.com/general/latest/gr/aws-arns-and-namespaces.html#genref-aws-service-namespaces.
        resource(str): The content of this part of the ARN varies by service. It often includes an indicator of the type of resource —
                for example, an IAM user or Amazon RDS database - followed by a slash (/) or a colon (:), followed by the
                resource name itself. Some services allows paths for resource names, as described in
                http://docs.aws.amazon.com/general/latest/gr/aws-arns-and-namespaces.html#arns-paths.
        partition(str, Optional): The partition that the resource is in. For standard AWS regions, the partition is "aws" (default).
                If you have resources in other partitions, the partition is "aws-partitionname". For example, the partition for resources
                in the China (Beijing) region is "aws-cn".
        region(str, Optional): The region the resource resides in. Note that the ARNs for some resources do not require a region, so this
                component might be omitted.
        account_id(str, Optional): The ID of the AWS account that owns the resource, without the hyphens. For example, 123456789012. Note that the
                ARNs for some resources don't require an account number, so this component might be omitted.

    .. code-block:: bash

        $ idem exec aws.arn.build service=ec2 region=us-west-2 resource=my-resource
    """
    ret = dict(comment=[], result=True, ret=None)

    arn = hub.tool.aws.arn_utils.build(
        partition=partition,
        service=service,
        region=region,
        account_id=account_id,
        resource=resource,
    )
    ret["ret"] = arn

    return ret


def parse(hub, ctx, arn: str) -> Dict:
    """
    Parses the provided AWS ARN and returns its components.

    Args:
        hub: The redistributed pop central hub.
        ctx: The context.
        arn(str): The AWS ARN.

    .. code-block:: bash

        $ idem exec aws.arn.parse arn=arn:aws:ec2:us-west-2:accountid:resource
    """
    ret = dict(comment=[], result=True, ret=None)

    try:
        parts = hub.tool.aws.arn_utils.parse(arn=arn)
    except TypeError as e:
        ret["result"] = False
        ret["comment"] += [str(e)]
        return ret

    ret["ret"] = parts

    return ret
