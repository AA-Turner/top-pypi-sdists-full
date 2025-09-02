from typing import List

import botocore.client
import botocore.docs.docstring
import botocore.exceptions
import botocore.model

__func_alias__ = {"type_": "type"}

from dict_tools.data import NamespaceDict


def parse(
    hub, param: "botocore.model.Shape", required: bool, parsed_nested_params: List[str]
):
    docstring = hub.tool.format.html.parse(param.documentation)
    ret = NamespaceDict(
        **{
            "required": required,
            "default": None,
            "target_type": "mapping",
            "target": "kwargs",
            "param_type": hub.pop_create.aws.param.type(param),
            "doc": "\n            ".join(
                hub.tool.format.wrap.wrap(
                    docstring,
                    width=96,
                )
            ),
        }
    )

    member = None
    if isinstance(param, botocore.model.StructureShape):
        member = param
    elif param.type_name == "list" and isinstance(
        param.member, botocore.model.StructureShape
    ):
        member = param.member
    elif param.type_name == "map" and isinstance(
        param.value, botocore.model.StructureShape
    ):
        member = param.value

    if member:
        # Avoid infinite recursion
        if member.name in parsed_nested_params:
            # Set param_type to ForwardRef({parsed_nested_param_type})
            ret["param_type"] = ret["param_type"].format(f"'{member.name}'")
            return ret
        parsed_nested_params.append(member.name)

        ret["member"] = {
            "name": member.name,
            "params": {
                k: parse(hub, v, k in member.required_members, parsed_nested_params)
                for k, v in member.members.items()
            },
        }
    return ret


def type_(hub, param: "botocore.model.Shape"):
    if param is None:
        return None
    if param.type_name == "string":
        return "str"
    elif param.type_name == "map":
        return f"Dict[{hub.pop_create.aws.param.type(param.key)}, {hub.pop_create.aws.param.type(param.value)}]"
    elif param.type_name == "structure":
        return "{}"
    elif param.type_name == "list":
        return f"List[{hub.pop_create.aws.param.type(param.member)}]"
    elif param.type_name == "boolean":
        return "bool"
    elif param.type_name in ("integer", "long"):
        return "int"
    elif param.type_name in ("float", "double"):
        return "float"
    elif param.type_name == "timestamp":
        return "datetime"
    elif param.type_name == "blob":
        return "ByteString"
    else:
        raise NameError(param.type_name)


def add_snaked_name_to_param(hub, params: dict):
    for k, param_data in params.items():
        if k == "name" and param_data.target_type == "arg":
            continue

        snaked = hub.tool.format.case.snake(k)
        unclashed_name = hub.tool.format.keyword.unclash(snaked) or snaked
        snaked = unclashed_name.replace(" ", "_").replace("-", "_").strip(". ")
        param_data["snaked"] = snaked
