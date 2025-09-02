from collections import OrderedDict
from typing import Any
from typing import Dict
from typing import List


def convert_raw_db_subnet_group_to_present(
    hub,
    raw_resource: Dict[str, Any],
    idem_resource_name: str = None,
    tags: Dict[str, Any] = None,
) -> Dict[str, Any]:
    """
    Convert AWS returned data structure to correct idem db_subnet_group present state

     Args:
        hub: required for functions in hub
        raw_resource (Dict): The aws response to convert
        idem_resource_name (str, Optional): The idem name of the resource
        tags (Dict, Optional): The tags of the resource. Defaults to None.

    Returns: Valid idem state for db_subnet_group of type Dict['string', Any]
    """
    resource_id = raw_resource["DBSubnetGroupName"]
    raw_resource["Tags"] = tags
    resource_parameters = OrderedDict(
        {
            "DBSubnetGroupDescription": "db_subnet_group_description",
            "Subnets": "subnet_ids",
            "Tags": "tags",
            "DBSubnetGroupArn": "db_subnet_group_arn",
        }
    )
    resource_translated = {"name": idem_resource_name, "resource_id": resource_id}
    for parameter_raw, parameter_present in resource_parameters.items():
        if raw_resource.get(parameter_raw) is not None:
            if parameter_raw == "Subnets":
                resource_translated[parameter_present] = [
                    subnet["SubnetIdentifier"] for subnet in raw_resource.get("Subnets")
                ]
            else:
                resource_translated[parameter_present] = raw_resource.get(parameter_raw)

    return resource_translated


async def search_raw(
    hub, ctx, filters: List = None, DBSubnetGroupName: str = None
) -> Dict:
    """

    Args:
        filters(list, Optional):
        DBSubnetGroupName(str, Optional): Name of DB Subnet Group.

    Returns:
        {"result": True|False, "comment": A message List, "ret": Dict}
    """
    result = dict(comment=[], ret=None, result=True)
    syntax_validation = hub.tool.aws.search_utils.search_filter_syntax_validation(
        filters=filters
    )
    if not syntax_validation["result"]:
        result["result"] = False
        result["comment"] = list(syntax_validation["comment"])
        return result
    boto3_filter = hub.tool.aws.search_utils.convert_search_filter_to_boto3(
        filters=filters
    )
    ret = await hub.exec.boto3.client.docdb.describe_db_subnet_groups(
        ctx,
        Filters=boto3_filter,
        DBSubnetGroupName=DBSubnetGroupName,
    )
    result["result"] = ret["result"]
    result["comment"] = list(ret["comment"])
    result["ret"] = ret["ret"]
    return result
