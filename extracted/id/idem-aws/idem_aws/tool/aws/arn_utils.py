from typing import Dict

ARN_PREFIX = "arn"
ARN_DELIMITER = ":"


def build(
    hub,
    *,
    partition: str = "aws",
    service: str,
    region: str = None,
    account_id: str = None,
    resource: str,
) -> str:
    """
    Creates an AWS ARN from parameters.

    Args:
        hub: The redistributed pop central hub.
        partition(str, Optional): The partition that the resource is in. For standard AWS regions, the partition is "aws" (default).
                If you have resources in other partitions, the partition is "aws-partitionname". For example, the partition for resources
                in the China (Beijing) region is "aws-cn".
        service(str): The service namespace that identifies the AWS product (for example, Amazon S3, IAM, or Amazon RDS). For a list of
                namespaces, see http://docs.aws.amazon.com/general/latest/gr/aws-arns-and-namespaces.html#genref-aws-service-namespaces.
        region(str, Optional): The region the resource resides in. Note that the ARNs for some resources do not require a region, so this
                component might be omitted.
        account_id(str, Optional): The ID of the AWS account that owns the resource, without the hyphens. For example, 123456789012. Note that the
                ARNs for some resources don't require an account number, so this component might be omitted.
        resource(str): The content of this part of the ARN varies by service. It often includes an indicator of the type of resource —
                for example, an IAM user or Amazon RDS database - followed by a slash (/) or a colon (:), followed by the
                resource name itself. Some services allows paths for resource names, as described in
                http://docs.aws.amazon.com/general/latest/gr/aws-arns-and-namespaces.html#arns-paths.

    Returns:
        The ARN (str)
    """
    return (
        ARN_PREFIX
        + ARN_DELIMITER
        + partition
        + ARN_DELIMITER
        + service
        + ARN_DELIMITER
        + str(region or "")
        + ARN_DELIMITER
        + str(account_id or "")
        + ARN_DELIMITER
        + str(resource or "")
    )


def parse(hub, arn: str) -> Dict:
    """
    Parses the provided AWS ARN and returns its components.

    Args:
        hub: The redistributed pop central hub.
        arn(str): The AWS ARN.

    Returns:
        The ARN parts (Dict):
          partition: The partition that the resource is in.
          service: The service namespace that identifies the AWS product.
          region: The region the resource resides in.
          account_id: The ID of the AWS account that owns the resource, without the hyphens.
          resource: The resource.
    """
    parts = arn.split(ARN_DELIMITER)

    if len(parts) < 6:
        raise TypeError(f"Invalid AWS ARN {arn}")

    arn_parts = {
        "partition": parts[1],
        "service": parts[2],
        "region": parts[3],
        "account_id": parts[4],
        "resource": ":".join(parts[5:]),
    }

    return arn_parts


def get_resource_name(hub, arn: str) -> str:
    """
    Get the resource name from a provided AWS ARN.

    The resource part of an AWS ARN may include a name for the resource:
        arn:partition:service:region:account-id:resource-type:resource-name:qualifier

    Args:
        hub: The redistributed pop central hub.
        arn(str): The AWS ARN.

    Returns:
        str: The resource name.
    """
    parts = arn.split(ARN_DELIMITER)
    if len(parts) < 7 or not parts[6]:
        return ""
    return parts[6]


def get_qualifier(hub, arn: str) -> str:
    """
    Get the qualifier from a provided AWS ARN.

    The resource part of an AWS ARN may include a qualifier for the resource such as a version:
        arn:partition:service:region:account-id:resource-type:resource-name:qualifier

    Args:
        hub: The redistributed pop central hub.
        arn(str): The AWS ARN.

    Returns:
        str: The qualifier.
    """
    parts = arn.split(ARN_DELIMITER)
    if len(parts) < 8 or not parts[7]:
        return ""
    return parts[7]
