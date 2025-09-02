from typing import Any
from typing import Dict
from typing import List

from dict_tools import data


async def search_raw(
    hub,
    ctx,
    resource_id: str = None,
    load_balancer_arn: str = None,
) -> Dict:
    """
    1. Describes specified listeners or the listeners for the specified Application Load Balancer,
        Network Load Balancer or Gateway Load Balancer.
    2. You must specify either a load balancer or one or more listeners. The return will be in the same
        format as what boto3 api returns.
    3. Here, resource_id get higher priority in search than load_balancer_arn i.e. if both load_balancer_arn
        and resource_id are not None, search is done with resource_id than load_balancer_arn.

    Args:
        resource_id(str, Optional):
            AWS ELBv2 Listener ARN to identify the resource.

        load_balancer_arn(str, Optional):
            The Amazon Resource Name (ARN) of the load balancer.

    Returns:
        {"result": True|False, "comment": A message List, "ret": Dict}

    """
    ret = result = dict(comment=[], ret=None, result=True)
    if resource_id:
        ret = await hub.exec.boto3.client.elbv2.describe_listeners(
            ctx,
            ListenerArns=[resource_id],
        )
    elif load_balancer_arn:
        ret = await hub.exec.boto3.client.elbv2.describe_listeners(
            ctx,
            LoadBalancerArn=load_balancer_arn,
        )
    result["result"] = ret["result"]
    result["comment"] = list(ret["comment"])
    result["ret"] = ret["ret"]
    return result


async def update(
    hub,
    ctx,
    name: str,
    current_state: Dict[str, Any],
    input_map: Dict[str, Any],
    resource_id: str,
):
    """
    1. Replaces the specified properties of the specified listener. Any property that is not updated, remains unchanged.
    2. Changing the protocol from HTTPS to HTTP, or from TLS to TCP, removes the security policy and default certificate
       properties. If you change the protocol from HTTP to HTTPS, or from TCP to TLS, you must add the security policy
       and default certificate properties.
    3. To add an item to a list, remove an item from a list, or update an item in a list, you must provide the entire
       list. For example, to add an action, specify a list with the current actions plus the new action.
    4. Adds the specified SSL server certificate to the certificate list for the specified HTTPS/ TLS listener. If the
       certificate in already in the certificate list, the call is successful but the certificate is not added again.
    5. Removes the specified certificate from the certificate list for the specified HTTPS or TLS listener.

    Args:
        name(str):
            The name of the AWS ElasticLoadBalancingv2 Listener.

        current_state(dict[str, Any]):
            response returned by describe on an AWS ElasticLoadBalancingv2 Listener

        input_map(dict[str, Any]):
            a dictionary with newly passed values of params.

        resource_id(str):
            AWS ElasticLoadBalancingv2 Listener Amazon Resource Name (ARN).

    Returns:
        {"result": True|False, "comment": A message List, "ret": None}
    """
    result = dict(comment=[], result=True, ret=[])
    if input_map:
        update = {}
        modify_params = {
            "Port": "port",
            "Protocol": "protocol",
            "SslPolicy": "ssl_policy",
            "AlpnPolicy": "alpn_policy",
            "Certificates": "default_certificates",
        }
        hub.log.debug(
            f"Current state of ELBv2 Listener '{name}' with resource id '{resource_id}' before update: {current_state}"
        )
        for param_raw, param_present in modify_params.items():
            if input_map.get(param_present) is not None and current_state.get(
                param_present
            ) != input_map.get(param_present):
                update[param_raw] = input_map[param_present]

        if len(input_map.get("default_actions")) == len(
            current_state.get("default_actions")
        ):
            ret = are_default_actions_identical(
                old_actions=current_state.get("default_actions"),
                new_actions=input_map.get("default_actions"),
            )
            if not ret["result"]:
                update["DefaultActions"] = input_map["default_actions"]
        else:
            update["DefaultActions"] = input_map["default_actions"]

        hub.log.debug(
            f"Params to modify for ELBv2 Listener '{name}' with resource id '{resource_id}': {update}"
        )
        if update:
            if not ctx.get("test", False):
                modify_listener = await hub.exec.boto3.client.elbv2.modify_listener(
                    ctx,
                    ListenerArn=resource_id,
                    **update,
                )
                if not modify_listener["result"]:
                    result["comment"] = list(modify_listener["comment"])
                    result["result"] = False
                    return result
                result["comment"].append("Modified Listener.")
                result["ret"].append(
                    {
                        "Key": "modify_listener",
                        "Value": modify_listener["ret"]["Listeners"][0],
                    }
                )
            else:
                for key, val in update.items():
                    result["ret"].append(
                        {
                            "Key": modify_params.get(key),
                            "Value": val,
                        }
                    )

    if input_map.get("certificates"):
        ret = compare_certificates(
            old_certificates=current_state.get("certificates"),
            new_certificates=input_map.get("certificates"),
        )
        if not ctx.get("test", False):
            if ret["ret"]:
                if ret["ret"].get("to_remove"):
                    remove_certificates = (
                        await hub.exec.boto3.client.elbv2.remove_listener_certificates(
                            ctx,
                            ListenerArn=resource_id,
                            Certificates=ret["ret"]["to_remove"],
                        )
                    )
                    if not remove_certificates["result"]:
                        result["comment"] += list(remove_certificates["comment"])
                        result["result"] = False
                        return result
                    result["comment"].append("Removed Certificates.")
                    hub.log.debug(
                        f"Removed Certificates for ELBv2 Listener '{name}' with resource id '{resource_id}':"
                        f" {ret['ret'].get('to_remove')}"
                    )
                    result["ret"].append(
                        {"remove_certificates": remove_certificates["ret"]}
                    )

                if ret["ret"].get("to_add"):
                    add_certificates = (
                        await hub.exec.boto3.client.elbv2.add_listener_certificates(
                            ctx,
                            ListenerArn=resource_id,
                            Certificates=ret["ret"]["to_add"],
                        )
                    )
                    if not add_certificates["result"]:
                        result["comment"] += list(add_certificates["comment"])
                        result["result"] = False
                        return result
                    result["comment"].append("Added Certificates.")
                    hub.log.debug(
                        f"Added Certificates for ELBv2 Listener '{name}' with resource id '{resource_id}': "
                        f"{ret['ret'].get('to_add')}"
                    )
                    result["ret"].append(
                        {"Key": "certificates", "Value": ret["ret"]["to_add"]}
                    )
        else:
            if ret["ret"].get("to_add"):
                result["ret"].append(
                    {"Key": "certificates", "Value": ret["ret"]["to_add"]}
                )
    return result


def compare_certificates(
    old_certificates: List[Dict[str, Any]] = None,
    new_certificates: List[Dict[str, Any]] = None,
):
    """
    Compares old_certificates and new_certificates and return the new list of certificates that need to be updated.

    Args:
        old_certificates(list[dict[str, Any]]):
            Existing list of certificates to be removed from AWS ElasticLoadBalancingv2 Listener.

        new_certificates(list[dict[str, Any]]):
            Newer list of certificates to be added to AWS ElasticLoadBalancingv2 Listener.

    Returns: Dict[str, Dict]

    """
    result = dict(ret=None)
    to_remove = []
    to_add = []
    old_certificates_map = {
        certificate.get("CertificateArn"): certificate
        for certificate in old_certificates or []
    }
    if new_certificates is not None:
        for certificate in new_certificates:
            if certificate.get("CertificateArn") in old_certificates_map:
                del old_certificates_map[certificate.get("CertificateArn")]
            else:
                to_add.append(certificate)
        to_remove = list(old_certificates_map.values())
        result["ret"] = {"to_add": to_add, "to_remove": to_remove}
    return result


def are_default_actions_identical(
    old_actions: List[Dict[str, Any]] = None,
    new_actions: List[Dict[str, Any]] = None,
):
    """
    Compares old_actions and new_actions and return the new list of default_actions that need to be updated.

    Args:
        old_actions(list[dict[str, Any]]):
            Existing list of default_actions to be removed from AWS ElasticLoadBalancingv2 Listener.

        new_actions(list[dict[str, Any]]):
            Newer list of default_actions to be added to AWS ElasticLoadBalancingv2 Listener.

    Returns: Dict[str, Dict]

    """
    result = dict(result=False)
    for new_action in new_actions:
        is_found = False
        for old_action in old_actions:
            if new_action.get("Type") == old_action.get("Type"):
                is_found = True
                if len(old_action) != len(new_action):
                    return result

                for key, value in old_action.items():
                    if new_action.get(key):
                        if isinstance(value, Dict):
                            if data.recursive_diff(
                                value, new_action.get(key), ignore_order=True
                            ):
                                return result
                        elif value != new_action.get(key):
                            return result
                    else:
                        return result
        if not is_found:
            return result
    result["result"] = True
    return result
