"""This module defines the present, absent and describe functionality for AWS document db cluster parameter group"""
from dataclasses import field
from dataclasses import make_dataclass
from typing import Any
from typing import Dict
from typing import List

__contracts__ = ["resource"]

RESOURCE_TYPE = "aws.docdb.db_cluster_parameter_group"


async def present(
    hub,
    ctx,
    name: str,
    db_parameter_group_family: str,
    description: str,
    resource_id: str = None,
    parameters: List[
        make_dataclass(
            """DB Parameter group configuration.""" "Parameter",
            [
                ("ParameterName", str),
                ("ParameterValue", str),
                ("ApplyMethod", str, field(default=None)),
                ("Description", str, field(default=None)),
                ("Source", str, field(default=None)),
                ("ApplyType", str, field(default=None)),
                ("DataType", str, field(default=None)),
                ("AllowedValues", str, field(default=None)),
                ("MinimumEngineVersion", str, field(default=None)),
                ("SupportedEngineModes", List[str], field(default=None)),
            ],
        )
    ] = None,
    tags: Dict[str, Any] = None,
) -> Dict[str, Any]:
    """Creates a new cluster parameter group.

    Parameters in a cluster parameter group apply to all of the instances in a cluster.

    A cluster parameter group is initially created with the default parameters for the database engine used by instances
    in the cluster. In Amazon DocumentDB, you cannot make modifications directly to the default.docdb3.6 cluster
    parameter group. If your Amazon DocumentDB cluster is using the default cluster parameter group and you want to
    modify a value in it, you must first create a new parameter group or copy an existing parameter group , modify it,
    and then apply the modified parameter group to your cluster. For the new cluster parameter group and associated
    settings to take effect, you must then reboot the instances in the cluster without failover. For more information,
    see Modifying Amazon DocumentDB Cluster Parameter Groups.

    Args:
        name(str):
            DBClusterParameterGroupName parameter on the resource. This value is stored as a lowercase string.
            This is also used as idem name.
        db_parameter_group_family(str):
            The cluster parameter group family name.
        description(str):
            The description for the DB cluster parameter group.
        resource_id(str, Optional):
            DBClusterParameterGroupName of the resource. Defaults to None.
        parameters(list, Optional): parameters in the DB cluster parameter group. Defaults to None.
            These parameters can only be modified.
            To modify more than one parameter, submit a list of the following: ParameterName, ParameterValue, and
            ApplyMethod. A maximum of 20 parameters can be modified in a single request.

            .. note::
                Changes to dynamic parameters are applied immediately. Changes to static parameters require a reboot
                without failover to the DB cluster associated with the parameter group before the change can take
                effect.

            .. warning::
                After you create a cluster parameter group, you should wait at least 5 minutes before creating your
                first cluster that uses that cluster parameter group as the default parameter group. This allows
                Amazon DocumentDB to fully complete the create action before the parameter group is used as the default
                for a new cluster. This step is especially important for parameters that are critical when creating the
                default database for a cluster, such as the character set for the default database defined by the
                character_set_database parameter.

            Below are the attributes available for parameters:

            Type: object dict(Describes a parameter)

            * ParameterName (str):
                Specifies the name of the parameter.
            * ParameterValue (str):
                Specifies the value of the parameter.
            * Description (str, Optional):
                provides a description of the parameter.
            * Source (str, Optional):
                Indicates the source of the parameter value.
            * ApplyType (str, Optional):
                Specifies the engine specific parameters type.
            * DataType (str, Optional):
                Specifies the valid data type for the parameter.
            * AllowedValues (str, Optional):
                Specifies the valid range of values for the parameter.
            * MinimumEngineVersion (str, Optional):
                The earliest engine version to which the parameter can apply.
            * ApplyMethod (str, Optional):
                Indicates when to apply parameter updates.
            * SupportedEngineModes (list, Optional):
                The valid DB engine modes.
        tags(dict, Optional):
            The tags to be assigned to the new DB cluster parameter group. Defaults to None.

    Request Syntax:
        .. code-block:: sls

            [idem_test_aws_docdb_db_cluster_parameter_group]:
              aws.docdb.db_cluster_parameter_group.present:
              - db_cluster_parameter_group_arn: 'string'
              - db_parameter_group_family: 'string'
              - description: 'string'
              - name: 'string'
              - parameters:
                - AllowedValues: 'string'
                  ApplyMethod: 'string'
                  ApplyType: 'string'
                  DataType: 'string'
                  Description: 'string'
                  IsModifiable: 'string'
                  ParameterName: 'string'
                  Source: 'string'


    Examples:
        .. code-block:: sls

            default.aurora5.6:
              aws.docdb.db_cluster_parameter_group.present:
              - db_cluster_parameter_group_arn: arn:aws:rds:ca-central-1:746014882121:cluster-pg:default.aurora5.6
              -  db_parameter_group_family: aurora5.6
              -  description: Default cluster parameter group for aurora5.6
              -  name: default.aurora5.6
              -  parameters:
                - AllowedValues: 0,1
                  ApplyMethod: pending-reboot
                  ApplyType: static
                  DataType: boolean
                  Description: Controls whether user-defined functions that have only an xxx symbol
                    for the main function can be loaded
                  IsModifiable: false
                  ParameterName: allow-suspicious-udfs
                  Source: engine-default

    """

    result = dict(comment=[], old_state=None, new_state=None, name=name, result=True)
    desired_state = {
        "name": name,
        "resource_id": name,
        "db_parameter_group_family": db_parameter_group_family,
        "description": description,
        "parameters": parameters,
        "tags": tags,
    }
    is_created = False

    if not resource_id:
        # if there is no resource_id, it is expected that we create the resource
        # if this is test run, just generate the new state and set in result
        if ctx.get("test", False):
            result["new_state"] = hub.tool.aws.test_state_utils.generate_test_state(
                enforced_state={}, desired_state=desired_state
            )
            resource_id = desired_state["resource_id"]
            result["comment"] = hub.tool.aws.comment_utils.would_create_comment(
                resource_type=RESOURCE_TYPE, name=name
            )
        else:
            # if this is not a test run, create the real resource
            create_db_cluster_parameter_group_result = (
                await hub.exec.boto3.client.docdb.create_db_cluster_parameter_group(
                    ctx,
                    DBClusterParameterGroupName=name,
                    DBParameterGroupFamily=db_parameter_group_family,
                    Description=description,
                    Tags=hub.tool.aws.tag_utils.convert_tag_dict_to_list(tags)
                    if tags
                    else None,
                )
            )

            # if create failed, fail the request
            if not create_db_cluster_parameter_group_result["result"]:
                result["comment"] = create_db_cluster_parameter_group_result["comment"]
                result["resul"] = False
                return result
            result["comment"] = hub.tool.aws.comment_utils.create_comment(
                resource_type=RESOURCE_TYPE, name=name
            )
            resource_id = create_db_cluster_parameter_group_result["ret"][
                "DBClusterParameterGroup"
            ]["DBClusterParameterGroupName"]
        is_created = True

    update_db_cluster_parameter_group_result = (
        await hub.tool.aws.docdb.db_cluster_parameter_group.update(
            ctx,
            name=name,
            resource_id=resource_id,
            desired_state=desired_state,
            is_created=is_created,
        )
    )

    if not (
        update_db_cluster_parameter_group_result
        and update_db_cluster_parameter_group_result["result"]
        and update_db_cluster_parameter_group_result["new_state"]
    ):
        result["result"] = False
        result["comment"] = update_db_cluster_parameter_group_result["comment"]
        return result

    result["old_state"] = update_db_cluster_parameter_group_result["old_state"]
    result["new_state"] = update_db_cluster_parameter_group_result["new_state"]
    # update the result comment if the resource is not being created
    if not is_created:
        result["comment"] = update_db_cluster_parameter_group_result["comment"]

    return result


async def absent(
    hub,
    ctx,
    name: str,
    resource_id: str = None,
) -> Dict[str, Any]:
    """

    Deletes a specified cluster parameter group. The cluster parameter group to be deleted can't be associated with any clusters.

    Args:
        name(str):
            DBClusterParameterGroupName parameter on the resource.
            This is also used as idem name.
        resource_id(str, Optional):
            DBClusterParameterGroupName of the resource. Defaults to None.
            Idem automatically considers the resource being absent if resource_id is not specified.

            Constraints: Must match the name of an existing DBClusterParameterGroupName.

    Examples:
        .. code-block:: sls

            resource_is_absent:
              aws.docdb.db_cluster_parameter_group.absent:
                - name: 'test-db-clus-param-group'
                - resource_id: 'test-db-clus-param-group'

    """
    already_absent_msg = hub.tool.aws.comment_utils.already_absent_comment(
        resource_type=RESOURCE_TYPE, name=name
    )
    result = dict(
        comment=already_absent_msg,
        old_state=None,
        new_state=None,
        name=name,
        result=True,
    )

    if not resource_id:
        return result

    before = await hub.exec.aws.docdb.db_cluster_parameter_group.get(
        ctx, name=name, resource_id=resource_id
    )

    if not before["result"]:
        result["comment"] = before["comment"]
        result["result"] = False
        return result
    if not before["ret"]:
        return result
    elif ctx.get("test", False):
        result["old_state"] = before["ret"]
        result["comment"] = hub.tool.aws.comment_utils.would_delete_comment(
            resource_type=RESOURCE_TYPE, name=name
        )
        return result
    else:
        result["old_state"] = before["ret"]
        ret = await hub.exec.boto3.client.docdb.delete_db_cluster_parameter_group(
            ctx,
            DBClusterParameterGroupName=resource_id,
        )
        result["result"] = ret["result"]
        if not result["result"]:
            result["comment"] = ret["comment"]
            return result
        result["comment"] = hub.tool.aws.comment_utils.delete_comment(
            resource_type=RESOURCE_TYPE, name=name
        )
        return result


async def describe(hub, ctx) -> Dict[str, Dict[str, Any]]:
    """Describe the resource in a way that can be recreated/managed with the corresponding "present" function.

    Returns a list of DBClusterParameterGroup.

    Examples:
        .. code-block:: bash

            $ idem describe aws.docdb.db_cluster_parameter_group

    """
    result = {}
    ret = await hub.exec.aws.docdb.db_cluster_parameter_group.list(ctx)
    if not ret["result"]:
        hub.log.warning(f"Could not describe {RESOURCE_TYPE} {ret['comment']}")
        return result

    for resource in ret["ret"]:
        result[resource.get("resource_id")] = {
            "aws.docdb.db_cluster_parameter_group.present": [resource]
        }
    return result
