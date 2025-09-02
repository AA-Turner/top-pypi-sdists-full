import copy
from typing import Any
from typing import Dict
from typing import List


async def update_tags(
    hub,
    ctx,
    resource_id,
    old_tags: Dict[str, Any],
    new_tags: Dict[str, Any],
):
    """
    Update tags of AWS IAM OpenID Connect Provider

    Args:
        resource_id (str):
            The Amazon Resource Name (ARN) of the IAM OpenID Connect provider

        old_tags (dict):
            Dict of old tags

        new_tags (dict):
            Dict of new tags

    Returns:
        Dict[str, Any]:
            Dict of updated tags

    Examples:
        Calling this exec module function from the cli with filters

        .. code-block:: bash

            idem exec aws.iam.open_id_connect_provider.update_tags name="my_resource" old_tags="{}" new_tags="{}"

        Using in a state:

        .. code-block:: yaml

            my_unmanaged_resource:
              exec.run:
                - path: aws.iam.open_id_connect_provider.update_tags
                - kwargs:
                    name: my_resource
                    old_tags: {}
                    new_tags: {}
    """
    tags_to_add = {}
    tags_to_remove = {}
    if new_tags is not None:
        tags_to_remove, tags_to_add = hub.tool.aws.tag_utils.diff_tags_dict(
            old_tags=old_tags, new_tags=new_tags
        )

    result = dict(comment=[], result=True, ret=None)
    if (not tags_to_remove) and (not tags_to_add):
        result["ret"] = copy.deepcopy(old_tags if old_tags else {})
        return result

    if tags_to_remove:
        if not ctx.get("test", False):
            delete_ret = await hub.exec.boto3.client.iam.untag_open_id_connect_provider(
                ctx,
                OpenIDConnectProviderArn=resource_id,
                TagKeys=list(tags_to_remove.keys()),
            )
            if not delete_ret["result"]:
                result["comment"] = delete_ret["comment"]
                result["result"] = False
                return result

    if tags_to_add:
        if not ctx.get("test", False):
            add_ret = await hub.exec.boto3.client.iam.tag_open_id_connect_provider(
                ctx,
                OpenIDConnectProviderArn=resource_id,
                Tags=hub.tool.aws.tag_utils.convert_tag_dict_to_list(tags=tags_to_add),
            )
            if not add_ret["result"]:
                result["comment"] = add_ret["comment"]
                result["result"] = False
                return result

    result["ret"] = new_tags
    if ctx.get("test", False):
        result["comment"] = hub.tool.aws.comment_utils.would_update_tags_comment(
            tags_to_remove=tags_to_remove, tags_to_add=tags_to_add
        )
    else:
        result["comment"] = hub.tool.aws.comment_utils.update_tags_comment(
            tags_to_remove=tags_to_remove, tags_to_add=tags_to_add
        )
    return result


async def update_thumbprints(
    hub,
    ctx,
    resource_id,
    old_thumbprints: List[str],
    new_thumbprints: List[str],
):
    """
    Update thumbprints of AWS IAM OpenID Connect Provider

    Args:
        resource_id (str):
            The Amazon Resource Name (ARN) of the IAM OpenID Connect provider

        old_thumbprints (list):
            List of old thumbprints

        new_thumbprints (list):
            List of new thumbprints

    Returns:
        Dict[str, Any]:
            List of updated thumbprints

    Examples:
        Calling this exec module function from the cli with filters

        .. code-block:: bash

            idem exec aws.iam.open_id_connect_provider.update_thumbprints name="my_resource" old_thumbprints="[]" new_thumbprints="[]"

        Using in a state:

        .. code-block:: yaml

            my_unmanaged_resource:
              exec.run:
                - path: aws.iam.open_id_connect_provider.update_thumbprints
                - kwargs:
                    name: my_resource
                    old_thumbprints: []
                    new_thumbprints: []
    """
    result = dict(comment=[], result=True, ret=None)
    if not ctx.get("test", False):
        update_ret = (
            await hub.exec.boto3.client.iam.update_open_id_connect_provider_thumbprint(
                ctx=ctx,
                OpenIDConnectProviderArn=resource_id,
                ThumbprintList=new_thumbprints,
            )
        )
        if not update_ret["result"]:
            result["comment"] = update_ret["comment"]
            result["result"] = False
            return result

    result["ret"] = {"thumbprint_list": new_thumbprints}
    if ctx.get("test", False):
        result["comment"] = [f"Would update thumbprints: {new_thumbprints}"]
    else:
        result["comment"] = [f"Updated thumbprints: {new_thumbprints}"]
    return result


async def update_client_ids(
    hub,
    ctx,
    resource_id,
    old_client_ids: List[str],
    new_client_ids: List[str],
):
    """
    Update clientIDs of AWS IAM OpenID Connect Provider

    Args:
        resource_id (str):
            The Amazon Resource Name (ARN) of the IAM OpenID Connect provider

        old_client_ids (list):
            List of old clientIDs

        new_client_ids (list):
            List of new clientIDs

    Returns:
        Dict[str, Any]:
            List of updated client_ids

    Examples:
        Calling this exec module function from the cli with filters

        .. code-block:: bash

            idem exec aws.iam.open_id_connect_provider.update_client_ids name="my_resource" old_client_ids="[]" new_client_ids="[]"

        Using in a state:

        .. code-block:: yaml

            my_unmanaged_resource:
              exec.run:
                - path: aws.iam.open_id_connect_provider.update_client_ids
                - kwargs:
                    name: my_resource
                    old_client_ids: []
                    new_client_ids: []
    """
    old_clients_list = copy.deepcopy(old_client_ids)
    clients_result = copy.deepcopy(old_clients_list)

    clients_to_add = list(set(new_client_ids).difference(old_client_ids))
    clients_to_remove = list(set(old_client_ids).difference(new_client_ids))

    result = dict(comment=[], result=True, ret=None)
    if (not clients_to_remove) and (not clients_to_add):
        return result

    if clients_to_remove:
        if not ctx.get("test", False):
            for client in clients_to_remove:
                delete_ret = await hub.exec.boto3.client.iam.remove_client_id_from_open_id_connect_provider(
                    ctx, OpenIDConnectProviderArn=resource_id, ClientID=client
                )
                if not delete_ret["result"]:
                    result["comment"] = delete_ret["comment"]
                    result["result"] = False
                    return result
        [clients_result.remove(key) for key in clients_to_remove]

    if clients_to_add:
        if not ctx.get("test", False):
            for client in clients_to_add:
                add_ret = await hub.exec.boto3.client.iam.add_client_id_to_open_id_connect_provider(
                    ctx, OpenIDConnectProviderArn=resource_id, ClientID=client
                )
                if not add_ret["result"]:
                    result["comment"] = add_ret["comment"]
                    result["result"] = False
                    return result

    result["ret"] = {"client_id_list": clients_result + clients_to_add}
    if ctx.get("test", False):
        result["comment"] += [
            f"Would update clientIDs: Add ({clients_to_add}) Remove ({clients_to_remove})"
        ]
    else:
        result["comment"] += [
            f"Updated clientIDs: Add ({clients_to_add}) Remove ({clients_to_remove})"
        ]
    return result
