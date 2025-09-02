"""State module for managing Amazon KMS Alias."""
import copy
from typing import Any
from typing import Dict

__contracts__ = ["resource"]

TREQ = {
    "absent": {
        "require": [
            "aws.kms.key.absent",
        ],
    },
    "present": {
        "require": [
            "aws.kms.key.present",
        ],
    },
}


async def present(
    hub, ctx, name: str, target_key_id: str, resource_id: str = None
) -> Dict[str, Any]:
    """Creates a friendly name for a KMS key.

    You can associate the alias with any customer managed key in the same Amazon Web Services Region.
    Each alias is associated with only one KMS key at a time, but a KMS key can have multiple aliases.
    A valid KMS key is required. You can't create an alias without a KMS key.

    The alias must be unique in the account and Region, but you can have aliases with the same name in different Regions

    Args:
        name(str):
            The name of the alias. This value must begin with ``alias/`` followed by a name, such as ``alias/ExampleAlias``.
            The AliasName value must be string of 1-256 characters. It can contain only alphanumeric characters, forward slashes (``/``),
            underscores (``_``), and dashes (``-``). The alias name cannot begin with ``alias/aws/``. The ``alias/aws/`` prefix is reserved
            for Amazon Web Services managed keys.
        target_key_id(str):
            Associates the alias with the specified customer managed key . The KMS key must be in the same Amazon Web Services Region..
        resource_id(str, Optional):
            The name of the alias in Amazon Web Services.

    Request Syntax:
      .. code-block:: sls

        [idem_test_aws_kms_alias]:
          aws.kms.alias.present:
            - name: 'string'
            - target_key_id: 'string'
            - resource_id: 'string'

    Returns:
        Dict[str, Any]

    Examples:
        .. code-block:: sls

            idem_test_aws_kms_alias:
              aws.kms.alias.present:
                  - name: alias/my-kms-key
                  - target_key_id: 1234abcd-12ab-34cd-56ef-1234567890ab
    """
    result = dict(comment=[], old_state=None, new_state=None, name=name, result=True)
    # check if alias name already exists
    before = None
    if resource_id is not None:
        before = await hub.tool.aws.kms.alias.get_alias_by_name(
            ctx, resource_id if resource_id else name
        )
    is_alias_applied = False

    if before and before["result"]:
        result["comment"] += [f"aws.kms.alias '{name}' already exists."]
        result[
            "old_state"
        ] = hub.tool.aws.kms.conversion_utils.convert_raw_key_alias_to_present(
            raw_resource=before["ret"]
        )
        plan_state = copy.deepcopy(result["old_state"])
        # alias already exists with that name. Update alias if target key is different
        if result["old_state"].get("target_key_id") != target_key_id:
            try:
                if not ctx.get("test", False):
                    update_ret = await hub.exec.boto3.client.kms.update_alias(
                        ctx, AliasName=name, TargetKeyId=target_key_id
                    )
                    result["result"] = update_ret["result"]
                    if not result["result"]:
                        result["comment"] += update_ret["comment"]
                        return result
                    result["comment"] += [
                        f"Updated alias of KMS key {target_key_id} to {name}"
                    ]
                    is_alias_applied = True
                else:
                    result["comment"] += [f"Would update aws.kms.alias {name}"]
                    plan_state["target_key_id"] = target_key_id

            except hub.tool.boto3.exception.ClientError as e:
                result["comment"] += [f"{e.__class__.__name__}: {e}"]
                result["result"] = False
                return result
        else:
            result["comment"] += [
                f"KMS Alias '{name}' is already associated with the KMS target key '{target_key_id}'"
            ]
    else:
        # No alias exists with that name. create new alias
        result["comment"] += [f"aws.kms.alias '{name}' does not exists."]
        if ctx.get("test", False):
            result["new_state"] = hub.tool.aws.test_state_utils.generate_test_state(
                enforced_state={},
                desired_state={
                    "name": name,
                    "target_key_id": target_key_id,
                },
            )
            result["comment"] += [f"Would create aws.kms.alias {name}"]
            return result

        try:
            ret = await hub.exec.boto3.client.kms.create_alias(
                ctx, AliasName=name, TargetKeyId=target_key_id
            )
            result["result"] = ret["result"]
            if not result["result"]:
                result["comment"] += ret["comment"]
                return result
            result["comment"] += [
                f"Created aws.kms.alias {name} for KMS key aws.kms.key {target_key_id}"
            ]
            is_alias_applied = True
        except hub.tool.boto3.exception.ClientError as e:
            result["comment"] += [f"{e.__class__.__name__}: {e}"]
            result["result"] = False
            return result
    try:
        if ctx.get("test", False):
            result["new_state"] = plan_state
        # get new state only if we create or modify alias
        elif is_alias_applied:
            after = await hub.tool.aws.kms.alias.get_alias_by_name(ctx, name)
            if after["result"] and after.get("ret"):
                result[
                    "new_state"
                ] = hub.tool.aws.kms.conversion_utils.convert_raw_key_alias_to_present(
                    raw_resource=after["ret"]
                )
            else:
                result["comment"] += after["comment"]
                result["result"] = False
        else:
            result["new_state"] = copy.deepcopy(result["old_state"])
    except Exception as e:
        result["comment"] += [str(e)]
        result["result"] = False
    return result


async def absent(hub, ctx, name: str, resource_id: str = None) -> Dict[str, Any]:
    """Deletes an AWS KMS alias.

    Because an alias is not a property of a KMS key, you can delete and change the aliases of a KMS key without
    affecting the KMS key.

    Args:
        name(str):
            The name of the alias.
        resource_id(str, Optional):
            The name of the alias in Amazon Web Services.

    Returns:
        Dict[str, Any]

    Request Syntax:
      .. code-block:: sls

        [idem_test_aws_kms_alias]:
          aws.kms.alias.absent:
            - name: 'string'
            - resource_id: 'string'

    Examples:
        .. code-block:: sls

            idem_test_aws_kms_alias:
              aws.kms.alias.absent:
                - name: alias/my-kms-key
                - resource_id: alias/my-kms-key
    """
    result = dict(comment=[], old_state=None, new_state=None, name=name, result=True)
    if not resource_id:
        result["comment"] = hub.tool.aws.comment_utils.already_absent_comment(
            resource_type="aws.kms.alias", name=name
        )
        return result
    before = await hub.tool.aws.kms.alias.get_alias_by_name(
        ctx, (resource_id if resource_id else name)
    )
    if not before["result"]:
        result["result"] = False
        result["comment"] += before["comment"]
        return result

    if not before["ret"]:
        result["comment"] += [f"aws.kms.policy '{name}' already absent"]
    elif ctx.get("test", False):
        result[
            "old_state"
        ] = hub.tool.aws.kms.conversion_utils.convert_raw_key_alias_to_present(
            raw_resource=before["ret"]
        )
        result["comment"] += [f"Would delete aws.kms.alias '{name}'"]
    else:
        result[
            "old_state"
        ] = hub.tool.aws.kms.conversion_utils.convert_raw_key_alias_to_present(
            raw_resource=before["ret"]
        )
        try:
            ret = await hub.exec.boto3.client.kms.delete_alias(
                ctx, AliasName=(resource_id if resource_id else name)
            )
            result["result"] = ret["result"]
            if not result["result"]:
                result["comment"] += ret["comment"]
                result["result"] = False
                return result
            result["comment"] += [f"aws.kms.alias '{name}' is deleted"]
        except hub.tool.boto3.exception.ClientError as e:
            result["comment"] += [f"{e.__class__.__name__}: {e}"]

    return result


async def describe(hub, ctx) -> Dict[str, Dict[str, Any]]:
    """Describes AWS KMS alias in a way that can be recreated/managed with the corresponding "present" function.

    Returns:
        Dict[str, Dict[str, Any]]

    Examples:
        .. code-block:: bash

            $ idem describe aws.kms.alias
    """
    result = {}
    ret = await hub.exec.boto3.client.kms.list_aliases(ctx)

    if not ret["result"]:
        hub.log.warning(f"Could not describe aws.kms.alias {ret['comment']}")
        return {}

    for key in ret["ret"]["Aliases"]:
        # Remove AWS reserved aliases as we cannot modify them using present/absent
        if key.get("AliasName") is not None and "alias/aws/" in key.get("AliasName"):
            continue
        # Get alias details to match the 'present' function parameters
        translated_resource = (
            hub.tool.aws.kms.conversion_utils.convert_raw_key_alias_to_present(
                raw_resource=key
            )
        )
        result[translated_resource["resource_id"]] = {
            "aws.kms.alias.present": [
                {parameter_key: parameter_value}
                for parameter_key, parameter_value in translated_resource.items()
            ]
        }

    return result
