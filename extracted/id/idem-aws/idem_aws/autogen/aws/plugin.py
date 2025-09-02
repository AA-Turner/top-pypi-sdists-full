"""Build plugin metadata which can be used by pop-create for plugin code generation"""
from typing import Any
from typing import Dict

from dict_tools.data import NamespaceDict


def create_resource_plugin(
    hub,
    ctx,
    shared_resource_data: dict,
) -> Dict[str, Any]:
    """
    Create CloudSpecPlugin with exec/state/tool functions
    """
    aws_service_name = shared_resource_data.get("aws_service_name")

    plugin = {
        "doc": f"\nTODO: Update generated documentation based on official AWS docs for the service https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/{aws_service_name}.html",
        "imports": [
            "import copy",
            "from dataclasses import field",
            "from dataclasses import make_dataclass",
            "from dict_tools import differ",
            "from typing import List",
            "from typing import Any",
            "from typing import Dict",
        ],
        "functions": NamespaceDict(),
    }

    plugin["functions"]["get"] = hub.pop_create.aws.plugin.generate_get(
        shared_resource_data["functions"]
    )

    create = hub.pop_create.aws.plugin.generate_present(
        shared_resource_data["functions"]
    )
    plugin["functions"]["create"] = create
    plugin["functions"]["present"] = create

    list_ = hub.pop_create.aws.plugin.generate_list(shared_resource_data["functions"])
    plugin["functions"]["list"] = list_
    plugin["functions"]["describe"] = list_

    delete = hub.pop_create.aws.plugin.generate_absent(
        shared_resource_data["functions"]
    )
    plugin["functions"]["delete"] = delete
    plugin["functions"]["absent"] = delete

    plugin["functions"]["update"] = hub.pop_create.aws.plugin.generate_update(
        shared_resource_data["functions"]
    )

    plugin["functions"][
        "convert_raw_resource_to_present_async"
    ] = hub.pop_create.aws.plugin.generate_convert_raw_to_present(
        shared_resource_data.get("resource_name"),
        shared_resource_data["functions"].get("get"),
    )

    # Add all tools function
    non_reserved_functions = {
        func_name: func_data
        for func_name, func_data in shared_resource_data["functions"].items()
        if func_name not in ["get", "create", "delete", "update", "list"]
    }

    for func_name, func_data in non_reserved_functions.items():
        plugin["functions"][func_name] = func_data

    # Add all tests functions
    plugin = hub.pop_create.aws.plugin.add_tests_functions(plugin)

    return plugin


def create_tags_plugin(
    hub,
    aws_service_name: str,
    tag_functions: dict,
) -> Dict[str, Any]:
    """
    Create tags CloudSpecPlugin for the service
    """
    plugin = {
        "doc": f"Tags related functions for AWS service '{aws_service_name}'.",
        "imports": [
            "import copy",
            "from dataclasses import field",
            "from dataclasses import make_dataclass",
            "from typing import List",
            "from typing import Any",
            "from typing import Dict",
        ],
        "functions": NamespaceDict(
            get_tags_for_resource=hub.pop_create.aws.plugin.generate_get_tags_for_resource(
                tag_functions
            ),
            update_tags=hub.pop_create.aws.plugin.generate_update_tags(tag_functions),
        ),
    }

    return plugin


def create_service_plugin(
    hub,
    aws_service_name: str,
    service_functions: dict,
) -> Dict[str, Any]:
    """
    Create CloudSpecPlugin for the service
    """
    plugin = {
        "doc": f"Functions for AWS service '{aws_service_name}'.",
        "imports": [
            "from dataclasses import field",
            "from dataclasses import make_dataclass",
            "from typing import List",
            "from typing import Any",
            "from typing import Dict",
        ],
        "functions": service_functions,
    }

    return plugin


def generate_get(hub, shared_resource_data):
    get_function_definition = shared_resource_data.get("get", {})
    params = get_function_definition.get("params", {})
    return {
        "doc": f"\n{get_function_definition.get('doc', '')}",
        "params": params,
        "hardcoded": dict(
            **get_function_definition.get("hardcoded", {}),
        ),
    }


def generate_list(hub, shared_resource_data):
    describe_function_definition = shared_resource_data.get("list", {})
    params = describe_function_definition.get("params", {})
    return {
        "doc": f"{describe_function_definition.get('doc', '')}",
        "params": params,
        "hardcoded": dict(
            **describe_function_definition.get("hardcoded", {}),
        ),
    }


def generate_update(hub, shared_resource_data):
    update_function_definition = shared_resource_data.get("update", {})
    params = update_function_definition.get("params", {})
    if "Name" in params:
        # it gets added by default in header params by pop-create
        params.pop("Name")
    if "tags" not in params.keys():
        params["tags"] = hub.pop_create.aws.known_params.TAGS_PARAMETER.copy()
    return {
        "doc": f"{update_function_definition.get('doc', '')}",
        "params": params,
        "hardcoded": dict(
            **update_function_definition.get("hardcoded", {}),
        ),
    }


def generate_present(hub, shared_resource_data):
    create_function_definition = shared_resource_data.get("create", {})
    params = create_function_definition.get("params", {})
    if "Name" in params:
        # it gets added by default in header params by pop-create
        params.pop("Name")

    if "Tags" not in params.keys():
        params["tags"] = hub.pop_create.aws.known_params.TAGS_PARAMETER.copy()
    return {
        "doc": f"{create_function_definition.get('doc', '')}",
        "params": params,
        "hardcoded": dict(
            **create_function_definition.get("hardcoded", {}),
        ),
    }


def generate_absent(hub, shared_resource_data):
    delete_function_definition = shared_resource_data.get("delete", {})
    return {
        "doc": f"{delete_function_definition.get('doc', '')}",
        "params": delete_function_definition.get("params", {}),
        "hardcoded": dict(
            **delete_function_definition.get("hardcoded", {}),
        ),
    }


def generate_get_tags_for_resource(hub, tag_functions):
    list_tags_function_definition = tag_functions.get("list_tags", {})
    return {
        "doc": f"Get tags for a given resource.\n",
        "params": dict(
            resource_id=hub.pop_create.aws.known_params.RESOURCE_ID_PARAMETER.copy(),
        ),
        "hardcoded": dict(
            **list_tags_function_definition.get("hardcoded", {}),
        ),
    }


def generate_update_tags(hub, tag_functions):
    update_tags_function_definition = tag_functions.get("update_tags", {})
    if update_tags_function_definition:
        return {
            "doc": f"Updates tags for a given resource.\n",
            "params": update_tags_function_definition["params"],
            "hardcoded": dict(
                update_tags_boto3_function=update_tags_function_definition.get(
                    "hardcoded", {}
                ).get("boto3_function"),
                update_tags_input_params=update_tags_function_definition.get(
                    "params", {}
                ).keys(),
                single_update=True,
            ),
        }
    else:
        untag_resource_function_definition = tag_functions.get("untag_resource", {})
        tag_resource_function_definition = tag_functions.get("tag_resource", {})
        return {
            "doc": f"Updates tags for a given resource.\n",
            "params": dict(
                resource_id=hub.pop_create.aws.known_params.RESOURCE_ID_PARAMETER.copy(),
                old_tags=hub.pop_create.aws.known_params.OLD_TAGS_PARAMETER.copy(),
                new_tags=hub.pop_create.aws.known_params.NEW_TAGS_PARAMETER.copy(),
            ),
            "hardcoded": dict(
                untag_resource_boto3_function=untag_resource_function_definition.get(
                    "hardcoded", {}
                ).get("boto3_function"),
                untag_resource_input_params=list(
                    untag_resource_function_definition.get("params", {}).keys()
                ),
                untag_resource_documentation=untag_resource_function_definition.get(
                    "hardcoded", {}
                ).get("boto3_documentation"),
                tag_resource_boto3_function=tag_resource_function_definition.get(
                    "hardcoded", {}
                ).get("boto3_function"),
                tag_resource_input_params=list(
                    tag_resource_function_definition.get("params", {}).keys()
                ),
                tag_resource_documentation=tag_resource_function_definition.get(
                    "hardcoded", {}
                ).get("boto3_documentation"),
                single_update=False,
            ),
        }


def generate_convert_raw_to_present(
    hub, resource_name: str, get_function_definition: dict
):
    return {
        "doc": f"Convert raw resource of {resource_name} type into present format.\n",
        "params": dict(
            idem_resource_name=hub.pop_create.aws.known_params.NAME_PARAMETER.copy(),
            resource_id=hub.pop_create.aws.known_params.RESOURCE_ID_PARAMETER.copy(),
            raw_resource=hub.pop_create.aws.known_params.RAW_RESOURCE_PARAMETER.copy(),
        ),
        "hardcoded": dict(
            **get_function_definition.get("hardcoded", {}),
        )
        if get_function_definition
        else {},
    }


def add_tests_functions(hub, plugin: dict):
    functions = plugin.get("functions", {}).copy()
    for func_name, func_data in functions.items():
        if func_name in ["get", "list", "create", "update", "delete"]:
            test_module_type = "exec"
        elif func_name in ["present", "absent", "describe"]:
            test_module_type = "states"
        else:
            test_module_type = "tool"

        plugin["functions"][f"test_{func_name}"] = {
            "doc": "",
            "hardcoded": {
                "resource_name": func_data.get("hardcoded", {}).get("resource_name"),
                "aws_service_name": func_data.get("hardcoded", {}).get(
                    "aws_service_name"
                ),
                # This is critical to derive rendering location
                "test_module_type": test_module_type,
                # Add calling method's metadata such as name, call params etc.
                "method_call_name": func_name,
                "method_call_params": func_data.get("params"),
            },
        }

    return plugin
