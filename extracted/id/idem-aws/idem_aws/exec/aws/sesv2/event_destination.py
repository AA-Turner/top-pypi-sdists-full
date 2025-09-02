"""Get and List methods for AWS SES Event destination."""
from typing import Any
from typing import Dict

__func_alias__ = {"list_": "list"}


async def get(
    hub, ctx, configuration_set_name: str, resource_id: str = None
) -> Dict[str, Any]:
    """Retrieve event destinations that are associated with a configuration set.

    Args:
        configuration_set_name(str):
            The name of the configuration set.
        resource_id(str, Optional):
            A name that identifies the event destination within the configuration set.

    Returns:
        .. code-block:: bash

            {"result": True|False, "comment": ["A list"], "ret": None|Dict}


    Examples:
        Calling this exec module function from the cli

        .. code-block:: bash

            idem exec aws.sesv2.event_destination.get configuration_set_name=config_set_name resource_id=event_destination_name


        Calling this exec module function from within a state module

        .. code-block:: python

            async def state_function(hub, ctx, name, resource_id, configuration_set_name, **kwargs):
                ret = await hub.exec.aws.sesv2.event_destination.get(ctx=ctx,
                                                                     resource_id=resource_id,
                                                                     configuration_set_name=configuration_set_name)
    """
    ret = {"result": True, "comment": [], "ret": {}}
    config_dest = (
        await hub.exec.boto3.client.sesv2.get_configuration_set_event_destinations(
            ctx, ConfigurationSetName=configuration_set_name
        )
    )
    if not config_dest.get("result"):
        ret["comment"] = config_dest["comment"]
        ret["result"] = False
        return ret
    for d in config_dest.get("ret", {}).get("EventDestinations", []):
        if resource_id and d["Name"] != resource_id:
            continue
        ret[
            "ret"
        ] = hub.tool.aws.sesv2.conversion_utils.convert_raw_event_destination_to_present(
            configuration_set_name=configuration_set_name,
            raw_resource=d,
            name=resource_id,
        )
        break
    if not ret["ret"]:
        ret["comment"].append(
            hub.tool.aws.comment_utils.get_empty_comment(
                resource_type="aws.sesv2.event_destination", name=resource_id
            )
        )
    return ret


async def list_(hub, ctx) -> Dict[str, Any]:
    """Retrieve a list of event destinations that are associated with a configuration set.

    Returns:
        .. code-block:: bash

            {"result": True|False, "comment": ["A list"], "ret": None|Dict}


    Examples:
        Calling this exec module function from the cli

        .. code-block:: bash

            idem exec aws.sesv2.event_destination.list


        Calling this exec module function from within a state module

        .. code-block:: python

            async def state_function(hub, ctx, name, resource_id, configuration_set_name, **kwargs):
                ret = await hub.exec.aws.sesv2.event_destination.list(ctx=ctx)
    """
    result = {"result": True, "comment": [], "ret": {}}
    ret = await hub.exec.boto3.client.sesv2.list_configuration_sets(ctx)

    if not ret["result"]:
        hub.log.error(f"Could not list configuration sets {ret['comment']}")
        result["comment"] = ret["comment"]
        result["result"] = False
        return result

    for name in ret["ret"].get("ConfigurationSets", []):
        resp = (
            await hub.exec.boto3.client.sesv2.get_configuration_set_event_destinations(
                ctx, ConfigurationSetName=name
            )
        )
        for e in resp["ret"].get("EventDestinations", []):
            new_event_destination = [
                {"name": e["Name"]},
                {"resource_id": e["Name"]},
                {"configuration_set_name": name},
                {"event_destination": e.pop("Name") and e.copy()},
            ]
            result["ret"][name] = {
                "aws.sesv2.event_destination.present": new_event_destination
            }
    if not result["ret"]:
        result["comment"].append(
            hub.tool.aws.comment_utils.list_empty_comment(
                resource_type="aws.sesv2.event_destination", name=""
            )
        )
    return result
