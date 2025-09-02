"""State module for AWS Neptune DB Parameter group."""
from dataclasses import field
from dataclasses import make_dataclass
from typing import Any
from typing import Dict
from typing import List

__contracts__ = ["resource"]

RESOURCE_TYPE = "aws.neptune.db_parameter_group"


async def present(
    hub,
    ctx,
    name: str,
    resource_id: str = None,
    *,
    db_parameter_group_family: str,
    description: str,
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
    """Creates a new DB parameter group.

    A DB parameter group is initially created with the default parameters for the
    database engine used by the DB instance. To provide custom values for any of the parameters, you must modify the
    group after creating it using ModifyDBParameterGroup. Once you've created a DB parameter group, you need to
    associate it with your DB instance using ModifyDBInstance. When you associate a new DB parameter group with a
    running DB instance, you need to reboot the DB instance without failover for the new DB parameter group and
    associated settings to take effect.  After you create a DB parameter group, you should wait at least 5 minutes
    before creating your first DB instance that uses that DB parameter group as the default parameter group. This
    allows Amazon Neptune to fully complete the create action before the parameter group is used as the default for
    a new DB instance. This is especially important for parameters that are critical when creating the default
    database for a DB instance, such as the character set for the default database defined by the
    character_set_database parameter. You can use the Parameter Groups option of the Amazon Neptune console or the
    DescribeDBParameters command to verify that your DB parameter group has been created or modified.

    Args:
        name(str):
            An idem name of the resource.
        db_parameter_group_family(str):
            The DB parameter group family name. A DB parameter group can be associated with one and only one
            DB parameter group family, and can be applied only to a DB instance running a database engine
            and engine version compatible with that DB parameter group family.
        parameters(list, Optional):
            An array of parameter names, values, and the apply method for the parameter update.
            At least one parameter name, value, and apply method must be supplied; subsequent arguments are optional. Defaults to None.
        resource_id(str, Optional):
            AWS DBParameterGroup Name. Defaults to None.
        description(str):
            The description for the DB parameter group.
        tags(dict or list, Optional):
            Dict in the format of {tag-key: tag-value} or List of tags in the format of
            [{"Key": tag-key, "Value": tag-value}] to associate with the DB parameter group.
            Each tag consists of a key name and an associated value. Defaults to None.

            * Key (str, Optional):
                The key of the tag. Constraints: Tag keys are case-sensitive and accept a maximum of 127 Unicode
                characters. May not begin with aws:.

            * Value(str, Optional):
                The value of the tag. Constraints: Tag values are case-sensitive and accept a maximum of 256
                Unicode characters.

    Request Syntax:
        .. code-block:: sls

            [idem_test_aws_neptune_db_parameter_group]:
                aws.neptune.db_parameter_group.present:
                    - name: 'string'
                    - db_parameter_group_family: 'string'
                    - parameters:
                        - AllowedValues: 'string'
                          ApplyMethod: 'string'
                          ApplyType: 'string'
                          DataType: 'string'
                          Description: 'string'
                          IsModifiable: 'string'
                          MinimumEngineVersion: 'string'
                          ParameterName: 'string'
                          ParameterValue: 'string'
                          Source: 'string'
                    - resource_id: 'string'
                    - description: 'string'
                    - tags:
                        - Key: 'string'
                          Value: 'string'
                        - Key: 'string'
                          Value: 'string'

    Returns:
        Dict[str, Dict[str,Any]]

    Examples:
        .. code-block:: sls

            resource_is_present:
              aws.neptune.db_parameter_group.present:
                - name: value
                - db_parameter_group_name: value
                - db_parameter_group_family: value
                - description: value
                - parameters:
                  - AllowedValues: 10-2147483647
                    ApplyMethod: pending-reboot
                    ApplyType: static
                    DataType: integer
                    Description: Graph query timeout (ms).
                    IsModifiable: true
                    MinimumEngineVersion: 1.0.1.0
                    ParameterName: neptune_query_timeout
                    ParameterValue: '120001'
                    Source: user
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
    # set a flag to keep track if the resource is newly created
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
            create_db_parameter_group_result = (
                await hub.exec.boto3.client.neptune.create_db_parameter_group(
                    ctx,
                    DBParameterGroupName=name,
                    DBParameterGroupFamily=db_parameter_group_family,
                    Description=description,
                    Tags=hub.tool.aws.tag_utils.convert_tag_dict_to_list(tags)
                    if tags
                    else None,
                )
            )
            # if create failed, fail the request
            if not create_db_parameter_group_result["result"]:
                result["comment"] = create_db_parameter_group_result["comment"]
                result["result"] = False
                return result
            result["comment"] = hub.tool.aws.comment_utils.create_comment(
                resource_type=RESOURCE_TYPE, name=name
            )
            resource_id = create_db_parameter_group_result["ret"]["DBParameterGroup"][
                "DBParameterGroupName"
            ]
        is_created = True

    # The argument "parameters" can only be modified as per AWS docs, so if user specifies
    # this during create, idem will first create the db_parameter_group and then modify its parameters
    # P.S. There is no way to create these parameters as per AWS doc.
    update_db_parameter_group_result = (
        await hub.tool.aws.neptune.db_parameter_group.update(
            ctx,
            name=name,
            resource_id=resource_id,
            desired_state=desired_state,
            is_created=is_created,
        )
    )
    if not (
        update_db_parameter_group_result
        and update_db_parameter_group_result["result"]
        and update_db_parameter_group_result["new_state"]
    ):
        result["result"] = False
        result["comment"] = update_db_parameter_group_result["comment"]
        return result

    result["old_state"] = update_db_parameter_group_result["old_state"]
    result["new_state"] = update_db_parameter_group_result["new_state"]
    # update the result comment if the resource is not being created
    if not is_created:
        result["comment"] = update_db_parameter_group_result["comment"]

    return result


async def absent(hub, ctx, name: str, resource_id: str = None) -> Dict[str, Any]:
    """Deletes a specified DBParameterGroup.

    The DBParameterGroup to be deleted can't be associated with any DB
    instances.

    Args:
        name(str):
            An idem name of the resource.
        resource_id(str, Optional):
            AWS Neptune DB Parameter Group Name. Defaults to None
            Idem automatically considers this resource as absent if this field is not specified.

    Request Syntax:
        .. code-block:: sls

            [idem_test_aws_neptune_db_parameter_group]:
                aws.neptune.db_parameter_group.absent:
                    - name: 'string'
                    - resource_id: 'string'

    Returns:
        Dict[str, Dict[str,Any]]

    Examples:
        .. code-block:: sls

            resource_is_absent:
              aws.neptune.db_parameter_group.absent:
                - name: value
                - resource_id: value
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

    before = await hub.exec.aws.neptune.db_parameter_group.get(
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
        ret = await hub.exec.boto3.client.neptune.delete_db_parameter_group(
            ctx,
            DBParameterGroupName=resource_id,
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

    Returns a list of DBParameterGroup descriptions.

    Returns:
        Dict[str, Dict[str,Any]]

    Examples:
        .. code-block:: bash

            $ idem describe aws.neptune.db_parameter_group
    """
    result = {}
    ret = await hub.exec.aws.neptune.db_parameter_group.list(
        ctx, name="aws.neptune.db_parameter_group.describe"
    )
    if not ret["result"]:
        hub.log.warning(f"Could not describe {RESOURCE_TYPE} {ret['comment']}")
        return result

    for resource in ret["ret"]:
        result[resource.get("resource_id")] = {
            "aws.neptune.db_parameter_group.present": [resource]
        }
    return result
