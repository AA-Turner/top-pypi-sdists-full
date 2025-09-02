from collections import OrderedDict
from typing import Any
from typing import Dict


def convert_raw_service_linked_role_to_present(
    hub, raw_resource: Dict[str, Any]
) -> Dict[str, Any]:
    resource_parameters = OrderedDict(
        {"RoleName": "name", "Description": "description", "Arn": "arn"}
    )

    # RoleName is the unique identifier for policy so it is set as resource_id
    translated_resource = {"resource_id": raw_resource.get("RoleName")}
    for parameter_raw, parameter_present in resource_parameters.items():
        if parameter_raw in raw_resource:
            translated_resource[parameter_present] = raw_resource.get(parameter_raw)

    if raw_resource.get("Tags") is not None:
        translated_resource["tags"] = hub.tool.aws.tag_utils.convert_tag_list_to_dict(
            raw_resource.get("Tags")
        )

    name = raw_resource.get("RoleName")
    # If custom suffix was added in service-linked role name,
    # Then format of role name will be like -> DefaultServiceLinkedRoleName + "_" + custom_suffix
    if "_" in name:
        translated_resource["custom_suffix"] = name[name.index("_") + 1 :]
    translated_resource["service_name"] = raw_resource.get("Arn").split("/")[-2]

    return translated_resource
