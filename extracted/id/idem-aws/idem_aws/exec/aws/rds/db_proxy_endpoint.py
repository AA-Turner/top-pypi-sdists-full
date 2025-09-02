"""Exec module for managing Rds Db Proxy Endpoints."""
from dataclasses import field
from dataclasses import make_dataclass
from typing import Any
from typing import Dict
from typing import List

__contracts__ = ["soft_fail"]

__func_alias__ = {"list_": "list"}

create_waiter_acceptors = [
    {
        "matcher": "pathAll",
        "expected": "available",
        "state": "success",
        "argument": "DBProxyEndpoints[].Status",
    },
    {
        "matcher": "pathAll",
        "expected": "creating",
        "state": "retry",
        "argument": "DBProxyEndpoints[].Status",
    },
]

update_waiter_acceptors = [
    {
        "matcher": "pathAll",
        "expected": "available",
        "state": "success",
        "argument": "DBProxyEndpoints[].Status",
    },
    {
        "matcher": "pathAll",
        "expected": "modifying",
        "state": "retry",
        "argument": "DBProxyEndpoints[].Status",
    },
    {
        "matcher": "pathAll",
        "expected": "resetting-master-credentials",
        "state": "retry",
        "argument": "DBProxyEndpoints[].Status",
    },
    {
        "matcher": "pathAll",
        "expected": "renaming",
        "state": "retry",
        "argument": "DBProxyEndpoints[].Status",
    },
    {
        "matcher": "pathAll",
        "expected": "upgrading",
        "state": "retry",
        "argument": "DBProxyEndpoints[].Status",
    },
]
delete_waiter_acceptors = [
    {
        "matcher": "error",
        "expected": "DBProxyEndpointNotFoundFault",
        "state": "success",
        "argument": "Error.Code",
    },
    {
        "matcher": "pathAll",
        "expected": "available",
        "state": "retry",
        "argument": "DBProxyEndpoints[].Status",
    },
    {
        "matcher": "pathAll",
        "expected": "deleting",
        "state": "retry",
        "argument": "DBProxyEndpoints[].Status",
    },
]


async def get(
    hub,
    ctx,
    resource_id: str = None,
    db_proxy_name: str = None,
    filters: List[
        make_dataclass("Filter", [("Name", str), ("Values", List[str])])
    ] = None,
    name: str = None,
) -> Dict[str, Any]:
    """

    Returns information about DB proxy endpoints.

    Args:
        resource_id(str, Optional): The name of a DB proxy endpoint to describe. If you omit this parameter, the output includes
            information about all DB proxy endpoints associated with the specified proxy. Defaults to None.

        db_proxy_name(str, Optional): The name of the DB proxy whose endpoints you want to describe. If you omit this parameter, the
            output includes information about all DB proxy endpoints associated with all your DB proxies. Defaults to None.


        filters(List[dict[str, Any]], Optional): This parameter is not currently supported. Defaults to None.

            * Name (str): The name of the filter. Filter names are case-sensitive.

            * Values (List[str]): One or more filter values. Filter values are case-sensitive.

        name(str, Optional): Idem name of the resource. Defaults to None.

    Returns:
        Dict[str, Any]

    Examples:
        Resource State:

        .. code-block:: sls

            unmanaged_resource:
              exec.run:
                - path: aws.rds.db_proxy_endpoint.get
                - kwargs:
                  resource_id: value

        Exec call from the CLI:

        .. code-block:: bash

            idem exec aws.rds.db_proxy_endpoint.get resource_id=value
    """

    result = dict(comment=[], ret=None, result=True)

    get_db_proxy_endpoint = await hub.exec.boto3.client.rds.describe_db_proxy_endpoints(
        ctx=ctx,
        **{
            "DBProxyName": db_proxy_name,
            "DBProxyEndpointName": resource_id,
            "Filters": filters,
        },
    )

    # Case: Error
    if not get_db_proxy_endpoint["result"]:
        # Do not return success=false when it is not found.
        # Most of the resources would return "*NotFound*" type of exception when it is 404
        if "DBProxyEndpointNotFoundFault" in str(
            get_db_proxy_endpoint["comment"]
        ) or "DBProxyNotFoundFault" in str(get_db_proxy_endpoint["comment"]):
            result["comment"].append(
                hub.tool.aws.comment_utils.get_empty_comment(
                    resource_type="aws.rds.db_proxy_endpoint", name=resource_id
                )
            )
            result["comment"].append(get_db_proxy_endpoint["comment"])
            return result

        result["comment"].append(get_db_proxy_endpoint["comment"])
        result["result"] = False
        return result

    # Case: Empty results
    if not get_db_proxy_endpoint["ret"]:
        result["comment"].append(
            hub.tool.aws.comment_utils.get_empty_comment(
                resource_type="aws.rds.db_proxy_endpoint", name=resource_id
            )
        )
        return result

    if len(get_db_proxy_endpoint["ret"]["DBProxyEndpoints"]) > 1:
        result["comment"].append(
            hub.tool.aws.comment_utils.find_more_than_one(
                resource_id=resource_id, resource_type="aws.rds.db_proxy_endpoint"
            )
        )

    raw_resource = get_db_proxy_endpoint["ret"]["DBProxyEndpoints"][0]

    result[
        "ret"
    ] = await hub.tool.aws.rds.db_proxy_endpoint.convert_raw_resource_to_present_async(
        ctx=ctx,
        resource_id=resource_id
        if resource_id
        else raw_resource.get("DBProxyEndpointName"),
        raw_resource=raw_resource,
        idem_resource_name=name,
    )

    return result


async def list_(
    hub,
    ctx,
    db_proxy_name: str = None,
    resource_id: str = None,
    filters: List[
        make_dataclass("Filter", [("Name", str), ("Values", List[str])])
    ] = None,
    name: str = None,
) -> Dict[str, Any]:
    """
    Returns information about DB proxy endpoints.

    Args:
        db_proxy_name(str, Optional): The name of the DB proxy whose endpoints you want to describe. If you omit this parameter, the
            output includes information about all DB proxy endpoints associated with all your DB proxies. Defaults to None.

        resource_id(str, Optional): The name of a DB proxy endpoint to describe. If you omit this parameter, the output includes
            information about all DB proxy endpoints associated with the specified proxy. Defaults to None.

        filters(List[dict[str, Any]], Optional): This parameter is not currently supported. Defaults to None.

            * Name (str): The name of the filter. Filter names are case-sensitive.

            * Values (List[str]): One or more filter values. Filter values are case-sensitive.

        name(str, Optional): Idem name of the resource. Defaults to None.

    Returns:
        Dict[str, Any]

    Examples:

        Resource State:

        .. code-block:: sls

            unmanaged_resources:
              exec.run:
                - path: aws.rds.db_proxy_endpoint.list
                - kwargs:


        Exec call from the CLI:

        .. code-block:: bash

            idem exec aws.rds.db_proxy_endpoint.list

        Describe call from the CLI:

        .. code-block:: bash

            $ idem describe aws.rds.db_proxy_endpoint

    """

    result = dict(comment=[], ret=[], result=True)

    ret = await hub.exec.boto3.client.rds.describe_db_proxy_endpoints(
        ctx=ctx,
        **{
            "DBProxyName": db_proxy_name,
            "DBProxyEndpointName": resource_id,
            "Filters": filters,
            "name": name,
        },
    )

    if not ret["result"]:
        result["comment"].append(ret["comment"])
        result["result"] = False
        return result

    if not ret["ret"].get("DBProxyEndpoints"):
        result["comment"].append(
            hub.tool.aws.comment_utils.list_empty_comment(
                resource_type="aws.rds.db_proxy_endpoint", name=None
            )
        )
        return result

    for resource in ret["ret"]["DBProxyEndpoints"]:
        result["ret"].append(
            await hub.tool.aws.rds.db_proxy_endpoint.convert_raw_resource_to_present_async(
                ctx=ctx,
                resource_id=resource.get("DBProxyEndpointName"),
                raw_resource=resource,
                idem_resource_name=name
                if name
                else resource.get("DBProxyEndpointName"),
            )
        )
    return result


async def create(
    hub,
    ctx,
    db_proxy_name: str,
    db_proxy_endpoint_name: str,
    vpc_subnet_ids: List[str],
    vpc_security_group_ids: List[str] = None,
    target_role: str = None,
    tags: Dict[str, str] = None,
    resource_id: str = None,
    name: str = None,
    timeout: make_dataclass(
        """Timeout configuration.""" "Timeout",
        [
            (
                "create",
                make_dataclass(
                    "CreateTimeout",
                    [
                        ("delay", int, field(default=None)),
                        ("max_attempts", int, field(default=None)),
                    ],
                ),
                field(default=None),
            ),
            (
                "update",
                make_dataclass(
                    "UpdateTimeout",
                    [
                        ("delay", int, field(default=None)),
                        ("max_attempts", int, field(default=None)),
                    ],
                ),
                field(default=None),
            ),
        ],
    ) = None,
) -> Dict[str, Any]:
    """
    Creates a DBProxyEndpoint. Only applies to proxies that are associated with Aurora DB clusters. You can use DB
    proxy endpoints to specify read/write or read-only access to the DB cluster. You can also use DB proxy endpoints
    to access a DB proxy through a different VPC than the proxy's default VPC.

    Args:
        db_proxy_name(str): The name of the DB proxy associated with the DB proxy endpoint that you create.

        db_proxy_endpoint_name(str): The name of the DB proxy endpoint to create.

        vpc_subnet_ids(List[str]): The VPC subnet IDs for the DB proxy endpoint that you create. You can specify a different set of
            subnet IDs than for the original DB proxy.

        vpc_security_group_ids(List[str], Optional): The VPC security group IDs for the DB proxy endpoint that you create. You can specify a
            different set of security group IDs than for the original DB proxy. The default is the default
            security group for the VPC. Defaults to None.

        target_role(str, Optional): A value that indicates whether the DB proxy endpoint can be used for read/write or read-only
            operations. The default is READ_WRITE. The only role that proxies for RDS for Microsoft SQL
            Server support is READ_WRITE. Defaults to None.

        tags(Dict[str, str], Optional): The tags to apply to the resource.

        resource_id(str, Optional): Db_proxy_endpoint unique ID. Defaults to None.

        name(str, Optional): Idem name of the resource. Defaults to None.

        timeout(dict, Optional):
            Timeout configuration for create/update of AWS DB Cluster.

            * create (*dict, Optional*):
                Timeout configuration for creating DB Cluster.

                * delay(*int, Optional*):
                    The amount of time in seconds to wait between attempts.

                * max_attempts(*int, Optional*):
                    Customized timeout configuration containing delay and max attempts.

            * update(*dict, Optional*):
                Timeout configuration for updating DB Cluster

                * delay(*int, Optional*):
                    The amount of time in seconds to wait between attempts.

                * max_attempts(*int, Optional*):
                    Customized timeout configuration containing delay and max attempts.

    Returns:
        Dict[str, Any]

    Examples:
        Using in a state:

        .. code-block:: sls

            resource_is_present:
              aws.rds.db_proxy_endpoint.present:
                - db_proxy_name: value
                - db_proxy_endpoint_name: value
                - vpc_subnet_ids: value

        Exec call from the CLI:

        .. code-block:: bash

            idem exec aws.rds.db_proxy_endpoint.create db_proxy_name=value, db_proxy_endpoint_name=value, vpc_subnet_ids=value
    """

    result = dict(comment=[], ret={}, result=True)

    desired_state = {
        k: v
        for k, v in locals().items()
        if k not in ("hub", "ctx", "kwargs", "result") and v is not None
    }

    resource_to_raw_input_mapping = {
        "db_proxy_name": "DBProxyName",
        "db_proxy_endpoint_name": "DBProxyEndpointName",
        "vpc_subnet_ids": "VpcSubnetIds",
        "vpc_security_group_ids": "VpcSecurityGroupIds",
        "target_role": "TargetRole",
    }

    payload = {}
    for key, value in desired_state.items():
        if key in resource_to_raw_input_mapping.keys() and value is not None:
            payload[resource_to_raw_input_mapping[key]] = desired_state.get(key)
    if tags:
        payload["Tags"] = hub.tool.aws.tag_utils.convert_tag_dict_to_list(tags)

    ret = await hub.exec.boto3.client.rds.create_db_proxy_endpoint(ctx, **payload)

    result["result"] = ret["result"]
    if not result["result"]:
        result["comment"] += ret["comment"]
        return result

    raw_resource = ret["ret"].get("DBProxyEndpoint", {})
    result["ret"]["resource_id"] = raw_resource.get("DBProxyEndpointName")
    result["ret"]["name"] = name

    waiter_config = hub.tool.aws.waiter_utils.create_waiter_config(
        default_delay=20,
        default_max_attempts=40,
        timeout_config=timeout.get("create") if timeout else None,
    )
    cluster_waiter = hub.tool.boto3.custom_waiter.waiter_wrapper(
        name="DBProxyEndpointCreated",
        operation="DescribeDBProxyEndpoints",
        argument=["DBProxyEndpoints[].Status"],
        acceptors=create_waiter_acceptors,
        client=await hub.tool.boto3.client.get_client(ctx, "rds"),
    )
    try:
        await hub.tool.boto3.client.wait(
            ctx,
            "rds",
            "DBProxyEndpointCreated",
            cluster_waiter,
            DBProxyEndpointName=result["ret"]["resource_id"],
            WaiterConfig=waiter_config,
        )
    except Exception as e:
        result["comment"] += [str(e)]
        result["result"] = False
        return result

    result["comment"] += hub.tool.aws.comment_utils.create_comment(
        resource_type="aws.rds.db_proxy_endpoint", name=name
    )

    return result


async def update(
    hub,
    ctx,
    resource_id: str,
    tags: Dict[str, str] = None,
    db_proxy_endpoint_name: str = None,
    new_db_proxy_endpoint_name: str = None,
    vpc_security_group_ids: List[str] = None,
    name: str = None,
    timeout: make_dataclass(
        """Timeout configuration.""" "Timeout",
        [
            (
                "create",
                make_dataclass(
                    "CreateTimeout",
                    [
                        ("delay", int, field(default=None)),
                        ("max_attempts", int, field(default=None)),
                    ],
                ),
                field(default=None),
            ),
            (
                "update",
                make_dataclass(
                    "UpdateTimeout",
                    [
                        ("delay", int, field(default=None)),
                        ("max_attempts", int, field(default=None)),
                    ],
                ),
                field(default=None),
            ),
        ],
    ) = None,
) -> Dict[str, Any]:
    """
    Changes the settings for an existing DB proxy endpoint.

    Args:
        resource_id(str): The name of the DB proxy associated with the DB proxy endpoint that you want to modify.

        tags(dict, Optional): The tags to apply to the resource. Defaults to None.

        db_proxy_endpoint_name(str, Optional): Name of the DBProxyEndpoint.

        new_db_proxy_endpoint_name(str, Optional): The new identifier for the DBProxyEndpoint. An identifier must begin with a letter and must
            contain only ASCII letters, digits, and hyphens; it can't end with a hyphen or contain two
            consecutive hyphens. Defaults to None.

        vpc_security_group_ids(List[str], Optional): The VPC security group IDs for the DB proxy endpoint. When the DB proxy endpoint uses a
            different VPC than the original proxy, you also specify a different set of security group IDs
            than for the original proxy. Defaults to None.

        name(str, Optional): Idem name of the resource. Defaults to None.

        timeout(dict, Optional):
            Timeout configuration for create/update of AWS DB Cluster.

            * create (*dict, Optional*):
                Timeout configuration for creating DB Cluster.

                * delay(*int, Optional*):
                    The amount of time in seconds to wait between attempts.

                * max_attempts(*int, Optional*):
                    Customized timeout configuration containing delay and max attempts.

            * update(*dict, Optional*):
                Timeout configuration for updating DB Cluster

                * delay(*int, Optional*):
                    The amount of time in seconds to wait between attempts.

                * max_attempts(*int, Optional*):
                    Customized timeout configuration containing delay and max attempts.

    Returns:
        Dict[str, Any]

    Examples:
        Using in a state:

        .. code-block:: sls

            resource_is_present:
              aws.rds.db_proxy_endpoint.present:
                - db_proxy_endpoint_name: value
                - tags: value
                - resource_id: value

        Exec call from the CLI:

        .. code-block:: bash

            idem exec aws.rds.db_proxy_endpoint.update db_proxy_endpoint_name=value, tags=value, resource_id=value
    """

    result = dict(comment=[], ret={}, result=True)

    desired_state = {
        k: v
        for k, v in locals().items()
        if k not in ("hub", "ctx", "kwargs", "result") and v is not None
    }

    payload = {}

    resource_to_raw_input_mapping = {
        "resource_id": "DBProxyEndpointName",
        "new_db_proxy_endpoint_name": "NewDBProxyEndpointName",
        "vpc_security_group_ids": "VpcSecurityGroupIds",
    }

    for key, value in desired_state.items():
        if key in resource_to_raw_input_mapping.keys() and value is not None:
            payload[resource_to_raw_input_mapping[key]] = desired_state.get(key)

    if payload:
        ret = await hub.exec.boto3.client.rds.modify_db_proxy_endpoint(ctx, **payload)
        if not ret["result"]:
            result["result"] = False
            result["comment"].append(
                f"Could not update aws.rds.db_proxy_endpoint '{name}'",
            )
            result["comment"].append(ret["comment"])
            return result

        result["comment"] += hub.tool.aws.comment_utils.update_comment(
            resource_type="aws.rds.db_proxy_endpoint", name=name
        )
        raw_resource = ret["ret"].get("DBProxyEndpoint", {})
        result["ret"]["resource_id"] = raw_resource.get("DBProxyEndpointName")
        get_tags_ret = await hub.tool.aws.rds.tag.get_tags_for_resource(
            ctx, resource_arn=raw_resource.get("DBProxyEndpointArn")
        )

        if get_tags_ret["result"]:
            current_tags = get_tags_ret.get("ret", {})
            update_tags_ret = await hub.tool.aws.rds.tag.update_tags(
                ctx,
                resource_arn=raw_resource.get("DBProxyEndpointArn"),
                old_tags=current_tags,
                new_tags=tags,
            )
            if not update_tags_ret["result"]:
                result["result"] = False
                result["comment"] += update_tags_ret["comment"]
                return result

        result["ret"]["resource_id"] = resource_id
        result["ret"]["name"] = name

        waiter_config = hub.tool.aws.waiter_utils.create_waiter_config(
            default_delay=20,
            default_max_attempts=40,
            timeout_config=timeout.get("update") if timeout else None,
        )
        cluster_waiter = hub.tool.boto3.custom_waiter.waiter_wrapper(
            name="DBProxyEndpointUpdated",
            operation="DescribeDBProxyEndpoints",
            argument=["DBProxyEndpoints[].Status"],
            acceptors=update_waiter_acceptors,
            client=await hub.tool.boto3.client.get_client(ctx, "rds"),
        )
        try:
            await hub.tool.boto3.client.wait(
                ctx,
                "rds",
                "DBProxyEndpointUpdated",
                cluster_waiter,
                DBProxyEndpointName=result["ret"]["resource_id"],
                WaiterConfig=waiter_config,
            )
        except Exception as e:
            result["comment"] += [str(e)]
            result["result"] = False
            return result

    return result


async def delete(
    hub,
    ctx,
    resource_id: str,
    name: str = None,
    timeout: make_dataclass(
        """Timeout configuration.""" "Timeout",
        [
            (
                "delete",
                make_dataclass(
                    "DeleteTimeout",
                    [
                        ("delay", int, field(default=None)),
                        ("max_attempts", int, field(default=None)),
                    ],
                ),
                field(default=None),
            ),
        ],
    ) = None,
) -> Dict[str, Any]:
    """
    Deletes a DBProxyEndpoint. Doing so removes the ability to access the DB proxy using the endpoint that you
    defined. The endpoint that you delete might have provided capabilities such as read/write or read-only
    operations, or using a different VPC than the DB proxy's default VPC.

    Args:
        resource_id(str): The name of the DB proxy endpoint to delete.

        name(str, Optional): Idem name of the resource. Defaults to None.

        timeout(dict, Optional):
            Timeout configuration for create/update of AWS DB Proxy Endpoint.

            * delete (*dict, Optional*):
                Timeout configuration for deleting DB Cluster.

                * delay(*int, Optional*):
                    The amount of time in seconds to wait between attempts.

                * max_attempts(*int, Optional*):
                    Customized timeout configuration containing delay and max attempts.

    Returns:
        Dict[str, Any]

    Examples:
        Resource State:

        .. code-block:: sls

            resource_is_absent:
              aws.rds.db_proxy_endpoint.absent:
                - resource_id: value

        Exec call from the CLI:

        .. code-block:: bash

            idem exec aws.rds.db_proxy_endpoint.delete resource_id=value
    """

    result = dict(comment=[], ret=None, result=True)

    delete_ret = await hub.exec.boto3.client.rds.delete_db_proxy_endpoint(
        ctx,
        **{"DBProxyEndpointName": resource_id},
    )

    result["result"] = delete_ret["result"]

    if not result["result"]:
        result["comment"] = delete_ret["comment"]
        result["result"] = False
        return result

    waiter_config = hub.tool.aws.waiter_utils.create_waiter_config(
        default_delay=20,
        default_max_attempts=40,
        timeout_config=timeout.get("delete") if timeout else None,
    )
    cluster_waiter = hub.tool.boto3.custom_waiter.waiter_wrapper(
        name="DBProxyEndpointDeleted",
        operation="DescribeDBProxyEndpoints",
        argument=["DBProxyEndpoints[].Status"],
        acceptors=delete_waiter_acceptors,
        client=await hub.tool.boto3.client.get_client(ctx, "rds"),
    )
    try:
        await hub.tool.boto3.client.wait(
            ctx,
            "rds",
            "DBProxyEndpointDeleted",
            cluster_waiter,
            DBProxyEndpointName=resource_id,
            WaiterConfig=waiter_config,
        )
    except Exception as e:
        result["comment"] += [str(e)]
        result["result"] = False
        return result

    result["comment"] = hub.tool.aws.comment_utils.delete_comment(
        resource_type="aws.rds.db_proxy_endpoint", name=name
    )

    return result
