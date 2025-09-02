from typing import Any
from typing import Dict
from typing import List


async def modify_db_parameter_group(
    hub,
    ctx,
    resource_name,
    old_parameters: List[Dict[str, Any]],
    new_parameters: List[Dict[str, Any]],
):
    """
    Modifies the parameters of a DB parameter group.
    Up to 20 parameters can be modified in a single call.

    Args:
        hub:
        ctx:
        resource_name: aws resource name
        old_parameters: list of old parameters, each with ParameterName , ParameterValue , and ApplyMethod
        new_parameters: list of new parameters, each with ParameterName , ParameterValue , and ApplyMethod

    Returns:
        ret contains the full list of parameters after modification
        {"result": True|False, "comment": "A message", "ret": None}

    """
    parameters_to_modify = _get_parameters_to_modify(old_parameters, new_parameters)

    result = dict(comment=[], result=True, ret=None)
    if not parameters_to_modify:
        return result
    else:
        if not ctx.get("test", False):
            update_parameters_ret = (
                await hub.exec.boto3.client.rds.modify_db_parameter_group(
                    ctx,
                    DBParameterGroupName=resource_name,
                    Parameters=parameters_to_modify,
                )
            )
            if not update_parameters_ret["result"]:
                result["comment"] = update_parameters_ret["comment"]
                result["result"] = False
                return result

        result["ret"] = {
            "parameters": _merge_params(old_parameters, parameters_to_modify)
        }
        result["comment"] += [
            f"Update parameters: Modified {[key.get('ParameterName') for key in parameters_to_modify]}"
        ]
    return result


async def modify_db_cluster_parameter_group(
    hub,
    ctx,
    resource_name,
    old_parameters: List[Dict[str, Any]],
    new_parameters: List[Dict[str, Any]],
):
    """
    Modifies the parameters of a DB cluster parameter group
    Up to 20 parameters can be modified in a single call.

    Args:
        hub:
        ctx:
        resource_name: aws resource name
        old_parameters: list of old parameters, each with ParameterName , ParameterValue , and ApplyMethod
        new_parameters: list of new parameters, each with ParameterName , ParameterValue , and ApplyMethod

    Returns:
        ret contains the full list of parameters after modification
        {"result": True|False, "comment": "A message", "ret": None}

    """
    parameters_to_modify = _get_parameters_to_modify(old_parameters, new_parameters)

    result = dict(comment=[], result=True, ret=None)
    if not parameters_to_modify:
        return result
    else:
        if not ctx.get("test", False):
            update_parameters_ret = (
                await hub.exec.boto3.client.rds.modify_db_cluster_parameter_group(
                    ctx,
                    DBClusterParameterGroupName=resource_name,
                    Parameters=parameters_to_modify,
                )
            )
            if not update_parameters_ret["result"]:
                result["comment"] = update_parameters_ret["comment"]
                result["result"] = False
                return result

        result["ret"] = {
            "parameters": _merge_params(old_parameters, parameters_to_modify)
        }
        result["comment"] += [
            f"Update parameters: Modified {[key.get('ParameterName') for key in parameters_to_modify]}"
        ]
    return result


def _get_parameters_to_modify(
    old_parameters: List[Dict[str, Any]], new_parameters: List[Dict[str, Any]]
):
    parameters_to_modify = []
    old_parameters_map = {
        parameter.get("ParameterName"): parameter for parameter in old_parameters or []
    }

    if new_parameters is not None:
        for parameter in new_parameters:
            if parameter.get("ParameterName") in old_parameters_map:
                name = parameter.get("ParameterName")
                if parameter.get("ParameterValue") != old_parameters_map.get(name).get(
                    "ParameterValue"
                ) or parameter.get("ApplyMethod") != old_parameters_map.get(name).get(
                    "ApplyMethod"
                ):
                    parameters_to_modify.append(parameter)
            else:
                parameters_to_modify.append(parameter)

    return parameters_to_modify


def _merge_params(
    old_parameters: List[Dict[str, Any]], changed_parameters: List[Dict[str, Any]]
):
    # Merge the new parameter value on top of the old values
    old_parameters_map = {
        parameter.get("ParameterName"): parameter for parameter in old_parameters or []
    }

    if changed_parameters:
        for new_param in changed_parameters:
            param_name = new_param.get("ParameterName")
            if param_name in old_parameters_map:
                old_parameters_map[param_name] = {
                    "ParameterName": param_name,
                    "ParameterValue": new_param.get("ParameterValue"),
                    "ApplyMethod": new_param.get("ApplyMethod"),
                }
            else:
                old_parameters_map = {
                    param_name: {
                        "ParameterName": param_name,
                        "ParameterValue": new_param.get("ParameterValue"),
                        "ApplyMethod": new_param.get("ApplyMethod"),
                    }
                }

    return list(old_parameters_map.values())
