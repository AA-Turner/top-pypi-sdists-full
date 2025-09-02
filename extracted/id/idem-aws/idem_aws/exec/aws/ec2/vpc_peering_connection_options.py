"""Exec module for managing VPC Peering Connection Options."""
from typing import Dict
from typing import List


async def get(
    hub,
    ctx,
    name: str,
    resource_id: str = None,
    filters: List = None,
) -> Dict:
    """Get EC2 vpc peering connection options from AWS account.

    Use an un-managed VPC peering connection options as a data-source.
    Supply one of the inputs as the filter.

    Args:
        name(str):
            The name of the Idem state.

        resource_id(str, Optional):
            AWS VPC peering connection id to identify the resource.

        filters(list, Optional):
            One or more filters: for example, tag :<key>, tag-key.
            A complete list of filters can be found at
            https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Client.describe_vpc_peering_connections

    Examples:
        Calling from the CLI:

        .. code-block:: bash

            $ idem exec aws.ec2.vpc_peering_connection_options.get

        Using in a state:

        .. code-block:: yaml

            my_unmanaged_resource:
              exec.run:
                - path: ec2.vpc_peering_connection_options.get
                - kwargs:
                    name: some-idem-resource-name
                    resource_id: some-resource-id
                    filters:
                      - name: 'vpc-peering-connection-id'
                        values:
                          - "pcx-ae89ce9b"
                      - name: 'tag:Name'
                        values:
                          - "my_unmanaged_resource"
    """
    result = await hub.tool.aws.ec2.vpc_peering_connection_utils.get_vpc_peering_connection_raw(
        ctx, name, resource_id, "aws.ec2.vpc_peering_connection_options", filters
    )
    raw_resource = result["ret"]

    result[
        "ret"
    ] = hub.tool.aws.ec2.conversion_utils.convert_raw_vpc_peering_connection_options_to_present(
        raw_resource=raw_resource, idem_resource_name=name
    )

    return result
