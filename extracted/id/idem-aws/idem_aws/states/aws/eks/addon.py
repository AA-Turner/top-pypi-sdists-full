"""State module for managing EKS Addon."""
import copy
from dataclasses import field
from dataclasses import make_dataclass
from typing import Any
from typing import Dict

__contracts__ = ["resource"]

TREQ = {
    "absent": {
        "require": [
            "aws.ec2.subnet.absent",
            "aws.iam.role.absent",
            "aws.iam.role_policy_attachment.absent",
            "aws.eks.cluster.absent",
        ],
    },
    "present": {
        "require": [
            "aws.ec2.subnet.present",
            "aws.iam.role.present",
            "aws.iam.role_policy_attachment.present",
            "aws.eks.cluster.present",
        ],
    },
}


async def present(
    hub,
    ctx,
    name: str,
    cluster_name: str,
    addon_version: str,
    resource_id: str = None,
    service_account_role_arn: str = None,
    resolve_conflicts: str = "OVERWRITE",
    tags: Dict[str, str] = None,
    timeout: make_dataclass(
        "Timeout",
        [
            (
                "create",
                make_dataclass(
                    "CreateTimeout",
                    [
                        ("delay", int, field(default=10)),
                        ("max_attempts", int, field(default=60)),
                    ],
                ),
                field(default=None),
            ),
            (
                "update",
                make_dataclass(
                    "UpdateTimeout",
                    [
                        ("delay", int, field(default=10)),
                        ("max_attempts", int, field(default=60)),
                    ],
                ),
                field(default=None),
            ),
        ],
    ) = None,
) -> Dict[str, Any]:
    """Creates an Amazon EKS add-on.

    Amazon EKS add-ons help to automate the provisioning and lifecycle management of common operational software for Amazon
    EKS clusters. Amazon EKS add-ons require clusters running version 1.18 or  because Amazon EKS add-ons rely on the
    Server-side Apply Kubernetes feature, which is only available in Kubernetes 1.18 and later. For more information, see
    Amazon EKS add-ons in the Amazon EKS User Guide.

    Args:
        name(str):
            An Idem name of the EKS addon resource.

        resource_id(str, Optional):
            AWS EKS addon name.

        cluster_name(str):
            The name of the cluster to create the add-on for

        addon_version(str):
            The version of the add-on. The version must match one of the versions returned
            by ` DescribeAddonVersions

        service_account_role_arn(str, Optional):
            The Amazon Resource Name (ARN) of an existing IAM role to bind to the add-on's
            service account. The role must be assigned the IAM permissions required by the add-on. If you don't specify
            an existing IAM role, then the add-on uses the permissions assigned to the node IAM role.

        resolve_conflicts(str, Optional):
            How to resolve parameter value conflicts when migrating an existing add-on
            to an Amazon EKS add-on

        tags(dict, Optional):
            The metadata to apply to the cluster to assist with categorization and organization.
            Each tag consists of a key and an Optional value. You define both

        timeout(dict, Optional):
            Timeout configuration for creating or updating addon.

            * create (dict):
                Timeout configuration for creating addon
                * delay(int, default=10): The amount of time in seconds to wait between attempts.
                * max_attempts(int, default=60): Customized timeout configuration containing delay and max attempts.

            * update (str):
                Timeout configuration for updating addon
                * delay(int, default=10): The amount of time in seconds to wait between attempts.
                * max_attempts(int, default=60): Customized timeout configuration containing delay and max attempts.
    Request Syntax:
        .. code-block:: sls

            [eks-addon-name]:
              aws.eks.addon.present:
                - cluster_name: 'string'
                - addon_version: 'string'
                - resource_id: 'string'
                - service_account_role_arn: 'string'
                - resolve_conflicts: 'string'
                - tags:
                  - 'string': 'string'
                - timeout:
                  create:
                    delay: 'integer'
                    max_attempts: 'integer'
                  update:
                    delay: 'integer'
                    max_attempts: 'integer

    Returns:
        Dict[str, Any]

    Examples:
        .. code-block:: sls

            kube-proxy:
              aws.eks.addon.present:
                - cluster_name: eks-12j44i4k
                - addon_version: v1.19.8-eksbuild.1
                - resource_id: kube-proxy
                - service_account_role_arn: arn:role-ejwew124
                - resolve_conflicts: "OVERWRITE"
                - tags:
                  - Name: eks-addon-name
    """

    result = dict(comment=[], old_state=None, new_state=None, name=name, result=True)
    before = None
    resource_updated = False
    if resource_id:
        before = await hub.exec.boto3.client.eks.describe_addon(
            ctx, clusterName=cluster_name, addonName=name
        )
        if not before["result"]:
            if not ("ResourceNotFoundException" in before["comment"][0]):
                result["result"] = False
                result["comment"] = before["comment"]
                return result

    if before and before["ret"]:
        try:
            result[
                "old_state"
            ] = hub.tool.aws.eks.conversion_utils.convert_raw_addon_to_present(
                raw_resource=before["ret"]["addon"], idem_resource_name=name
            )
            plan_state = copy.deepcopy(result["old_state"])
            client_request_token = result["old_state"].get("client_request_token", None)

            update_ret = await hub.tool.aws.eks.addon.update_addon(
                ctx=ctx,
                name=name,
                before=result["old_state"],
                addon_version=addon_version,
                service_account_role_arn=service_account_role_arn,
                resolve_conflicts=resolve_conflicts,
                client_request_token=client_request_token,
                timeout=timeout,
            )
            result["comment"] = update_ret["comment"]
            result["result"] = update_ret["result"]
            resource_updated = bool(update_ret["ret"])

            if update_ret["ret"] and ctx.get("test", False):
                result["comment"] += [f"Would update aws.eks.addon '{name}'"]
                for addon_param in update_ret["ret"]:
                    plan_state[addon_param] = update_ret["ret"][addon_param]

            if tags is not None:
                # Update tags
                update_tags_ret = await hub.tool.aws.eks.tag.update_eks_tags(
                    ctx=ctx,
                    resource_arn=result["old_state"].get("addon_arn"),
                    old_tags=result["old_state"].get("tags"),
                    new_tags=tags,
                )

            result["comment"] += update_tags_ret["comment"]
            result["result"] = result["result"] and update_tags_ret["result"]
            resource_updated = resource_updated or bool(update_tags_ret["ret"])
            if ctx.get("test", False) and update_tags_ret["ret"]:
                plan_state["tags"] = update_tags_ret["ret"].get("tags")
        except hub.tool.boto3.exception.ClientError as e:
            result["comment"] += [f"{e.__class__.__name__}: {e}"]
            result["result"] = False
    else:
        if ctx.get("test", False):
            result["new_state"] = hub.tool.aws.test_state_utils.generate_test_state(
                enforced_state={},
                desired_state={
                    "name": name,
                    "cluster_name": cluster_name,
                    "addon_version": addon_version,
                    "service_account_role_arn": service_account_role_arn,
                    "resolve_conflicts": resolve_conflicts,
                    "tags": tags,
                },
            )
            result["comment"] = hub.tool.aws.comment_utils.would_create_comment(
                resource_type="aws.eks.addon", name=name
            )
            return result
        try:
            ret = await hub.exec.boto3.client.eks.create_addon(
                ctx,
                clusterName=cluster_name,
                addonName=name,
                addonVersion=addon_version,
                serviceAccountRoleArn=service_account_role_arn,
                resolveConflicts=resolve_conflicts,
                tags=tags,
            )
            result["result"] = ret["result"]
            if not result["result"]:
                result["comment"] = ret["comment"]
                return result

            resource_id = ret["ret"]["addon"]["addonName"]
            waiter_config = hub.tool.aws.waiter_utils.create_waiter_config(
                default_delay=60,
                default_max_attempts=40,
                timeout_config=timeout.get("create") if timeout else None,
            )
            hub.log.debug(f"Waiting on creating aws.eks.addon '{name}'")
            try:
                await hub.tool.boto3.client.wait(
                    ctx,
                    "eks",
                    "addon_active",
                    addonName=resource_id,
                    clusterName=cluster_name,
                    WaiterConfig=waiter_config,
                )
            except Exception as e:
                result["comment"] += [str(e)]
                result["result"] = False
            result["comment"] = hub.tool.aws.comment_utils.create_comment(
                resource_type="aws.eks.addon", name=name
            )
        except Exception as e:
            result["comment"] += [f"{e.__class__.__name__}: {e}"]
            result["result"] = False
            return result

    try:
        if ctx.get("test", False):
            result["new_state"] = plan_state
        elif (not before) or resource_updated:
            after = await hub.exec.boto3.client.eks.describe_addon(
                ctx, clusterName=cluster_name, addonName=resource_id
            )
            result[
                "new_state"
            ] = hub.tool.aws.eks.conversion_utils.convert_raw_addon_to_present(
                raw_resource=after["ret"]["addon"], idem_resource_name=name
            )
        else:
            result["new_state"] = copy.deepcopy(result["old_state"])
    except Exception as e:
        result["comment"] += [str(e)]
        result["result"] = False
    return result


async def absent(
    hub,
    ctx,
    name: str,
    cluster_name: str = None,
    resource_id: str = None,
    preserve: bool = False,
    timeout: Dict = None,
) -> Dict[str, Any]:
    """
    Delete an Amazon EKS add-on.

    When you remove the add-on, it will also be deleted from the cluster. You can always manually start an add-on on the
    cluster using the Kubernetes API.

    Args:

        name(str):
            An Idem name of the EKS addon resource.

        cluster_name(str, Optional):
            The name of the cluster to delete the add-on from.

        resource_id(str, Optional):
            AWS EKS addon name. Idem automatically considers this resource being absent if this field is not specified.

        preserve(bool, Optional):
            Specifying this option preserves the add-on software on your cluster but Amazon EKS stops managing any
            settings for the add-on. If an IAM account is associated with the add-on, it is not removed.

        timeout(dict, Optional):
            Timeout configuration for creating or updating cluster.

            * delete (dict):
                Timeout configuration for deleting cluster
                * delay: The amount of time in seconds to wait between attempts.
                * max_attempts: Customized timeout configuration containing delay and max attempts.

    Request syntax:
        .. code-block:: sls

            [idem-eks-addon-name]:
              aws.eks.addon.absent:
                - cluster_name: 'string'
                - resource_id: 'string'
                - preserve: bool

    Returns:
        Dict[str, Any]

    Examples:
        .. code-block:: sls

            kube-proxy:
              aws.eks.addon.absent:
                - cluster_name: eks-cluster-1
                - resource_id: kube-proxy
                - preserve: True
    """

    result = dict(comment=[], old_state=None, new_state=None, name=name, result=True)
    if not resource_id:
        result["comment"] = hub.tool.aws.comment_utils.already_absent_comment(
            resource_type="aws.eks.addon", name=name
        )
        return result

    if not cluster_name:
        result["comment"] = hub.tool.aws.comment_utils.missing_args_for_absent_comment(
            resource_type="aws.eks.addon", name=name, args=["cluster_name"]
        )
        result["result"] = False
        return result

    before = await hub.exec.boto3.client.eks.describe_addon(
        ctx, clusterName=cluster_name, addonName=resource_id
    )

    if not before["ret"]:
        result["comment"] = hub.tool.aws.comment_utils.already_absent_comment(
            resource_type="aws.eks.addon", name=name
        )
    elif ctx.get("test", False):
        result[
            "old_state"
        ] = hub.tool.aws.eks.conversion_utils.convert_raw_addon_to_present(
            raw_resource=before["ret"]["addon"], idem_resource_name=name
        )
        result["comment"] = hub.tool.aws.comment_utils.would_delete_comment(
            resource_type="aws.eks.addon", name=name
        )
        return result
    else:
        result[
            "old_state"
        ] = hub.tool.aws.eks.conversion_utils.convert_raw_addon_to_present(
            raw_resource=before["ret"]["addon"], idem_resource_name=name
        )
        try:
            ret = await hub.exec.boto3.client.eks.delete_addon(
                ctx, clusterName=cluster_name, addonName=resource_id, preserve=preserve
            )
            result["result"] = ret["result"]
            if not result["result"]:
                result["comment"] = ret["comment"]
                result["result"] = False
                return result
            else:
                waiter_config = hub.tool.aws.waiter_utils.create_waiter_config(
                    default_delay=60,
                    default_max_attempts=40,
                    timeout_config=timeout.get("delete") if timeout else None,
                )
                try:
                    await hub.tool.boto3.client.wait(
                        ctx,
                        "eks",
                        "addon_deleted",
                        addonName=resource_id,
                        clusterName=cluster_name,
                        WaiterConfig=waiter_config,
                    )
                except Exception as e:
                    result["comment"] += [str(e)]
                    result["result"] = False
            result["comment"] = result[
                "comment"
            ] + hub.tool.aws.comment_utils.delete_comment(
                resource_type="aws.eks.addon", name=name
            )
        except hub.tool.boto3.exception.ClientError as e:
            result["comment"] += [f"{e.__class__.__name__}: {e}"]

    return result


async def describe(hub, ctx) -> Dict[str, Dict[str, Any]]:
    """
    Describe the resource in a way that can be recreated/managed with the corresponding "present" function

    Lists the available add-ons.

    Returns:
        Dict[str, Any]

    Examples:
        .. code-block:: bash

            $ idem describe aws.eks.addon

    """

    result = {}
    cluster_ret = await hub.exec.boto3.client.eks.list_clusters(ctx)
    if not cluster_ret["result"]:
        hub.log.warning(f"Could not describe cluster {cluster_ret['comment']}")
        return {}
    cluster_addons = []
    try:
        for name in cluster_ret["ret"]["clusters"]:
            addon_ret = await hub.exec.boto3.client.eks.list_addons(
                ctx, clusterName=name
            )
            if not addon_ret["result"]:
                hub.log.debug(
                    f"Could not describe cluster addons for cluster {name}, Error:  {addon_ret['comment']}"
                )
                continue
            for addon in addon_ret["ret"]["addons"]:
                cluster_addons.append({"name": name, "addon": addon})
    except Exception as e:
        result["comment"] = str(e)
        result["result"] = False
        return result

    for cluster_addon in cluster_addons:
        cluster_name = cluster_addon["name"]
        current_addon = cluster_addon["addon"]
        resource_id = f"{cluster_name}-{current_addon}"
        describe_ret = await hub.exec.boto3.client.eks.describe_addon(
            ctx, clusterName=cluster_name, addonName=current_addon
        )
        if not describe_ret["result"] or not describe_ret["ret"]:
            hub.log.warning(
                f"Could not describe addon {name}, Error:  {describe_ret['comment']}"
            )
            continue
        add_on = describe_ret["ret"]["addon"]
        resource_translated = (
            hub.tool.aws.eks.conversion_utils.convert_raw_addon_to_present(
                raw_resource=add_on, idem_resource_name=resource_id
            )
        )
        result[resource_id] = {
            "aws.eks.addon.present": [
                {parameter_key: parameter_value}
                for parameter_key, parameter_value in resource_translated.items()
            ]
        }

    return result
