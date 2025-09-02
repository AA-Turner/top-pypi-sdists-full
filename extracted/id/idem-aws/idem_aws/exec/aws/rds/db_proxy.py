"""
Exec module for managing Rds Db Proxys.
"""
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
        "argument": "DBProxies[].Status",
    },
    {
        "matcher": "pathAll",
        "expected": "creating",
        "state": "retry",
        "argument": "DBProxies[].Status",
    },
]

update_waiter_acceptors = [
    {
        "matcher": "pathAll",
        "expected": "available",
        "state": "success",
        "argument": "DBProxies[].Status",
    },
    {
        "matcher": "pathAll",
        "expected": "modifying",
        "state": "retry",
        "argument": "DBProxies[].Status",
    },
    {
        "matcher": "pathAll",
        "expected": "resetting-master-credentials",
        "state": "retry",
        "argument": "DBProxies[].Status",
    },
    {
        "matcher": "pathAll",
        "expected": "renaming",
        "state": "retry",
        "argument": "DBProxies[].Status",
    },
    {
        "matcher": "pathAll",
        "expected": "upgrading",
        "state": "retry",
        "argument": "DBProxies[].Status",
    },
]
delete_waiter_acceptors = [
    {
        "matcher": "error",
        "expected": "DBProxyNotFoundFault",
        "state": "success",
        "argument": "Error.Code",
    },
    {
        "matcher": "pathAll",
        "expected": "available",
        "state": "retry",
        "argument": "DBProxies[].Status",
    },
    {
        "matcher": "pathAll",
        "expected": "deleting",
        "state": "retry",
        "argument": "DBProxies[].Status",
    },
]


async def get(
    hub,
    ctx,
    resource_id: str,
    filters: List[
        make_dataclass("Filter", [("Name", str), ("Values", List[str])])
    ] = None,
    name: str = None,
) -> Dict[str, Any]:
    """

    Returns information about DB proxies.

    Args:
        resource_id(str): Db_proxy unique ID. The name of the DB proxy.

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
                - path: aws.rds.db_proxy.get
                - kwargs:
                  resource_id: value

        Exec call from the CLI:

        .. code-block:: bash

            idem exec aws.rds.db_proxy.get resource_id=value
    """

    result = dict(comment=[], ret=None, result=True)
    get_rds_db_proxy = await hub.exec.boto3.client.rds.describe_db_proxies(
        ctx=ctx, DBProxyName=resource_id, Filters=filters
    )
    # Case: Error
    if not get_rds_db_proxy["result"]:
        # Do not return success=false when it is not found.
        # Most of the resources would return "*NotFound*" type of exception when it is 404
        if "DBProxyNotFoundFault" in str(get_rds_db_proxy["comment"]):
            result["comment"].append(
                hub.tool.aws.comment_utils.get_empty_comment(
                    resource_type="aws.rds.db_proxy", name=resource_id
                )
            )
            result["comment"].append(get_rds_db_proxy["comment"])
            return result

        result["comment"].append(get_rds_db_proxy["comment"])
        result["result"] = False
        return result

    # Case: Empty results
    if not get_rds_db_proxy["ret"]:
        result["comment"].append(
            hub.tool.aws.comment_utils.get_empty_comment(
                resource_type="aws.rds.db_proxy", name=resource_id
            )
        )
        return result

    if len(get_rds_db_proxy["ret"]["DBProxies"]) > 1:
        result["comment"].append(
            hub.tool.aws.comment_utils.find_more_than_one(
                resource_id=resource_id, resource_type="aws.rds.db_proxy"
            )
        )

    raw_resource = get_rds_db_proxy["ret"]["DBProxies"][0]

    result[
        "ret"
    ] = await hub.tool.aws.rds.db_proxy.convert_raw_resource_to_present_async(
        ctx=ctx,
        resource_id=resource_id,
        raw_resource=raw_resource,
        idem_resource_name=name,
    )

    return result


async def list_(
    hub,
    ctx,
    resource_id: str = None,
    filters: List[
        make_dataclass("Filter", [("Name", str), ("Values", List[str])])
    ] = None,
    name: str = None,
) -> Dict[str, Any]:
    """
    Returns information about DB proxies.

    Args:
        resource_id(str, Optional): The name of the DB proxy. If you omit this parameter, the output includes information about all
            DB proxies owned by your Amazon Web Services account ID. Defaults to None.

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
                - path: aws.rds.db_proxy.list
                - kwargs:


        Exec call from the CLI:

        .. code-block:: bash

            idem exec aws.rds.db_proxy.list

        Describe call from the CLI:

        .. code-block:: bash

            $ idem describe aws.rds.db_proxy

    """

    result = dict(comment=[], ret=[], result=True)

    ret = await hub.exec.boto3.client.rds.describe_db_proxies(
        ctx=ctx, DBProxyName=resource_id, Filters=filters
    )

    if not ret["result"]:
        result["comment"].append(ret["comment"])
        result["result"] = False
        return result

    if not ret["ret"].get("DBProxies"):
        result["comment"].append(
            hub.tool.aws.comment_utils.list_empty_comment(
                resource_type="aws.rds.db_proxy", name=name
            )
        )
        return result

    for resource in ret["ret"]["DBProxies"]:
        result["ret"].append(
            await hub.tool.aws.rds.db_proxy.convert_raw_resource_to_present_async(
                ctx=ctx,
                resource_id=resource["DBProxyName"],
                raw_resource=resource,
                idem_resource_name=resource["DBProxyName"],
            )
        )
    return result


async def create(
    hub,
    ctx,
    db_proxy_name: str,
    engine_family: str,
    auth: List[
        make_dataclass(
            "UserAuthConfig",
            [
                ("Description", str, field(default=None)),
                ("UserName", str, field(default=None)),
                ("AuthScheme", str, field(default=None)),
                ("SecretArn", str, field(default=None)),
                ("IAMAuth", str, field(default=None)),
                ("ClientPasswordAuthType", str, field(default=None)),
            ],
        )
    ],
    role_arn: str,
    vpc_subnet_ids: List[str],
    vpc_security_group_ids: List[str] = None,
    require_tls: bool = None,
    idle_client_timeout: int = None,
    debug_logging: bool = None,
    tags: Dict[str, str] = None,
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
    Creates a new DB proxy.

    Args:
        db_proxy_name(str): The identifier for the proxy. This name must be unique for all proxies owned by your Amazon Web
            Services account in the specified Amazon Web Services Region. An identifier must begin with a
            letter and must contain only ASCII letters, digits, and hyphens; it can't end with a hyphen or
            contain two consecutive hyphens.

        engine_family(str): The kinds of databases that the proxy can connect to. This value determines which database
            network protocol the proxy recognizes when it interprets network traffic to and from the
            database. For Aurora MySQL, RDS for MariaDB, and RDS for MySQL databases, specify MYSQL. For
            Aurora PostgreSQL and RDS for PostgreSQL databases, specify POSTGRESQL. For RDS for Microsoft
            SQL Server, specify SQLSERVER.

        auth(List[dict[str, Any]]): The authorization mechanism that the proxy uses.

            * Description (str, Optional): A user-specified description about the authentication used by a proxy to log in as a specific
            database user.

            * UserName (str, Optional): The name of the database user to which the proxy connects.

            * AuthScheme (str, Optional): The type of authentication that the proxy uses for connections from the proxy to the underlying
            database.

            * SecretArn (str, Optional): The Amazon Resource Name (ARN) representing the secret that the proxy uses to authenticate to
            the RDS DB instance or Aurora DB cluster. These secrets are stored within Amazon Secrets
            Manager.

            * IAMAuth (str, Optional): Whether to require or disallow Amazon Web Services Identity and Access Management (IAM)
            authentication for connections to the proxy. The ENABLED value is valid only for proxies with
            RDS for Microsoft SQL Server.

            * ClientPasswordAuthType (str, Optional): The type of authentication the proxy uses for connections from clients.

        role_arn(str): The Amazon Resource Name (ARN) of the IAM role that the proxy uses to access secrets in Amazon
            Web Services Secrets Manager.

        vpc_subnet_ids(List[str]): One or more VPC subnet IDs to associate with the new proxy.

        vpc_security_group_ids(List[str], Optional): One or more VPC security group IDs to associate with the new proxy. Defaults to None.

        require_tls(bool, Optional): A Boolean parameter that specifies whether Transport Layer Security (TLS) encryption is required
            for connections to the proxy. By enabling this setting, you can enforce encrypted TLS
            connections to the proxy. Defaults to None.

        idle_client_timeout(int, Optional): The number of seconds that a connection to the proxy can be inactive before the proxy
            disconnects it. You can set this value higher or lower than the connection timeout limit for the
            associated database. Defaults to None.

        debug_logging(bool, Optional): Whether the proxy includes detailed information about SQL statements in its logs. This
            information helps you to debug issues involving SQL behavior or the performance and scalability
            of the proxy connections. The debug information includes the text of SQL statements that you
            submit through the proxy. Thus, only enable this setting when needed for debugging, and only
            when you have security measures in place to safeguard any sensitive information that appears in
            the logs. Defaults to None.

        tags(Dict[str, str], Optional): The tags to apply to the resource.

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
              aws.rds.db_proxy.present:
                - db_proxy_name: value
                - engine_family: value
                - auth: value
                - role_arn: value
                - vpc_subnet_ids: value

        Exec call from the CLI:

        .. code-block:: bash

            idem exec aws.rds.db_proxy.create db_proxy_name=value, engine_family=value, auth=value, role_arn=value, vpc_subnet_ids=value
    """

    result = dict(comment=[], ret={}, result=True)

    desired_state = {
        k: v
        for k, v in locals().items()
        if k not in ("hub", "ctx", "kwargs", "result") and v is not None
    }

    resource_to_raw_input_mapping = {
        "db_proxy_name": "DBProxyName",
        "engine_family": "EngineFamily",
        "auth": "Auth",
        "role_arn": "RoleArn",
        "vpc_subnet_ids": "VpcSubnetIds",
        "vpc_security_group_ids": "VpcSecurityGroupIds",
        "require_tls": "RequireTLS",
        "idle_client_timeout": "IdleClientTimeout",
        "debug_logging": "DebugLogging",
    }

    payload = {}
    for key, value in desired_state.items():
        if key in resource_to_raw_input_mapping.keys() and value is not None:
            payload[resource_to_raw_input_mapping[key]] = desired_state.get(key)

    if tags:
        payload["Tags"] = hub.tool.aws.tag_utils.convert_tag_dict_to_list(tags)

    ret = await hub.exec.boto3.client.rds.create_db_proxy(ctx, **payload)

    result["result"] = ret["result"]
    if not result["result"]:
        result["comment"] += ret["comment"]
        return result
    raw_resource = ret["ret"].get("DBProxy", {})
    result["ret"]["resource_id"] = raw_resource.get("DBProxyName")
    result["ret"]["name"] = name

    waiter_config = hub.tool.aws.waiter_utils.create_waiter_config(
        default_delay=20,
        default_max_attempts=40,
        timeout_config=timeout.get("create") if timeout else None,
    )
    cluster_waiter = hub.tool.boto3.custom_waiter.waiter_wrapper(
        name="DBProxyCreated",
        operation="DescribeDBProxies",
        argument=["DBProxies[].Status"],
        acceptors=create_waiter_acceptors,
        client=await hub.tool.boto3.client.get_client(ctx, "rds"),
    )
    try:
        await hub.tool.boto3.client.wait(
            ctx,
            "rds",
            "DBProxyCreated",
            cluster_waiter,
            DBProxyName=result["ret"]["resource_id"],
            WaiterConfig=waiter_config,
        )
    except Exception as e:
        result["comment"] += [str(e)]
        result["result"] = False
        return result

    result["comment"] += hub.tool.aws.comment_utils.create_comment(
        resource_type="aws.rds.db_proxy", name=name
    )

    return result


async def update(
    hub,
    ctx,
    resource_id: str,
    new_db_proxy_name: str = None,
    auth: List[
        make_dataclass(
            "UserAuthConfig",
            [
                ("Description", str, field(default=None)),
                ("UserName", str, field(default=None)),
                ("AuthScheme", str, field(default=None)),
                ("SecretArn", str, field(default=None)),
                ("IAMAuth", str, field(default=None)),
                ("ClientPasswordAuthType", str, field(default=None)),
            ],
        )
    ] = None,
    require_tls: bool = None,
    idle_client_timeout: int = None,
    debug_logging: bool = None,
    role_arn: str = None,
    security_groups: List[str] = None,
    name: str = None,
    tags: Dict[str, str] = None,
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
    Changes the settings for an existing DB proxy.

    Args:

        resource_id(str): Db_proxy unique ID.

        new_db_proxy_name(str, Optional): The new identifier for the DBProxy. An identifier must begin with a letter and must contain only
            ASCII letters, digits, and hyphens; it can't end with a hyphen or contain two consecutive
            hyphens. Defaults to None.

        auth(List[dict[str, Any]], Optional): The new authentication settings for the DBProxy. Defaults to None.

            * Description (str, Optional): A user-specified description about the authentication used by a proxy to log in as a specific
            database user.

            * UserName (str, Optional): The name of the database user to which the proxy connects.

            * AuthScheme (str, Optional): The type of authentication that the proxy uses for connections from the proxy to the underlying
            database.

            * SecretArn (str, Optional): The Amazon Resource Name (ARN) representing the secret that the proxy uses to authenticate to
            the RDS DB instance or Aurora DB cluster. These secrets are stored within Amazon Secrets
            Manager.

            * IAMAuth (str, Optional): Whether to require or disallow Amazon Web Services Identity and Access Management (IAM)
            authentication for connections to the proxy. The ENABLED value is valid only for proxies with
            RDS for Microsoft SQL Server.

            * ClientPasswordAuthType (str, Optional): The type of authentication the proxy uses for connections from clients.

        require_tls(bool, Optional): Whether Transport Layer Security (TLS) encryption is required for connections to the proxy. By
            enabling this setting, you can enforce encrypted TLS connections to the proxy, even if the
            associated database doesn't use TLS. Defaults to None.

        idle_client_timeout(int, Optional): The number of seconds that a connection to the proxy can be inactive before the proxy
            disconnects it. You can set this value higher or lower than the connection timeout limit for the
            associated database. Defaults to None.

        debug_logging(bool, Optional): Whether the proxy includes detailed information about SQL statements in its logs. This
            information helps you to debug issues involving SQL behavior or the performance and scalability
            of the proxy connections. The debug information includes the text of SQL statements that you
            submit through the proxy. Thus, only enable this setting when needed for debugging, and only
            when you have security measures in place to safeguard any sensitive information that appears in
            the logs. Defaults to None.

        role_arn(str, Optional): The Amazon Resource Name (ARN) of the IAM role that the proxy uses to access secrets in Amazon
            Web Services Secrets Manager. Defaults to None.

        security_groups(List[str], Optional): The new list of security groups for the DBProxy. Defaults to None.

        name(str, Optional): Idem name of the resource. Defaults to None.

        tags(Dict[str, str], Optional): The tags to apply to the resource.

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
              aws.rds.db_proxy.present:
                - db_proxy_name: value
                - tags: value
                - resource_id: value

        Exec call from the CLI:

        .. code-block:: bash

            idem exec aws.rds.db_proxy.update db_proxy_name=value, tags=value, resource_id=value
    """

    result = dict(comment=[], ret={}, result=True)

    desired_state = {
        k: v
        for k, v in locals().items()
        if k not in ("hub", "ctx", "kwargs", "result") and v is not None
    }

    payload = {}

    resource_to_raw_input_mapping = {
        "resource_id": "DBProxyName",
        "new_db_proxy_name": "NewDBProxyName",
        "auth": "Auth",
        "require_tls": "RequireTLS",
        "idle_client_timeout": "IdleClientTimeout",
        "debug_logging": "DebugLogging",
        "role_arn": "RoleArn",
        "security_groups": "SecurityGroups",
    }

    for key, value in desired_state.items():
        if key in resource_to_raw_input_mapping.keys() and value is not None:
            payload[resource_to_raw_input_mapping[key]] = desired_state.get(key)

    if payload:
        ret = await hub.exec.boto3.client.rds.modify_db_proxy(ctx, **payload)
        if not ret["result"]:
            result["result"] = False
            result["comment"].append(
                f"Could not update aws.rds.db_proxy '{name}'",
            )
            result["comment"] += ret["comment"]
            return result

        raw_resource = ret["ret"].get("DBProxy", {})
        result["comment"] += hub.tool.aws.comment_utils.update_comment(
            resource_type="aws.rds.db_proxy", name=name
        )

        get_tags_ret = await hub.tool.aws.rds.tag.get_tags_for_resource(
            ctx, resource_arn=raw_resource.get("DBProxyArn")
        )

        if get_tags_ret["result"]:
            current_tags = get_tags_ret.get("ret", {})
            update_tags_ret = await hub.tool.aws.rds.tag.update_tags(
                ctx,
                resource_arn=raw_resource.get("DBProxyArn"),
                old_tags=current_tags,
                new_tags=tags,
            )
            if not update_tags_ret["result"]:
                result["result"] = False
                result["comment"] += update_tags_ret["comment"]
                return result

        result["ret"]["resource_id"] = raw_resource.get("DBProxyName")
        result["ret"]["name"] = name

        waiter_config = hub.tool.aws.waiter_utils.create_waiter_config(
            default_delay=20,
            default_max_attempts=40,
            timeout_config=timeout.get("update") if timeout else None,
        )
        cluster_waiter = hub.tool.boto3.custom_waiter.waiter_wrapper(
            name="DBProxyUpdated",
            operation="DescribeDBProxies",
            argument=["DBProxies[].Status"],
            acceptors=update_waiter_acceptors,
            client=await hub.tool.boto3.client.get_client(ctx, "rds"),
        )
        try:
            await hub.tool.boto3.client.wait(
                ctx,
                "rds",
                "DBProxyUpdated",
                cluster_waiter,
                DBProxyName=result["ret"]["resource_id"],
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
    Deletes an existing DB proxy.

    Args:
        resource_id(str): Db_proxy unique ID.

        name(str, Optional): Idem name of the resource. Defaults to None.

        timeout(dict, Optional):
            Timeout configuration for delete of AWS RDS DB Proxy.

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
              aws.rds.db_proxy.absent:
                - db_proxy_name: value
                - resource_id: value

        Exec call from the CLI:

        .. code-block:: bash

            idem exec aws.rds.db_proxy.delete db_proxy_name=value, resource_id=value
    """

    result = dict(comment=[], ret=None, result=True)

    delete_ret = await hub.exec.boto3.client.rds.delete_db_proxy(
        ctx, **{"DBProxyName": resource_id}
    )

    result["result"] = delete_ret["result"]

    if not result["result"]:
        result["comment"] = delete_ret["comment"]
        result["result"] = False
        return result

    result["comment"] += hub.tool.aws.comment_utils.delete_comment(
        resource_type="aws.rds.db_proxy", name=name
    )

    waiter_config = hub.tool.aws.waiter_utils.create_waiter_config(
        default_delay=20,
        default_max_attempts=40,
        timeout_config=timeout.get("delete") if timeout else None,
    )
    cluster_waiter = hub.tool.boto3.custom_waiter.waiter_wrapper(
        name="DBProxyDeleted",
        operation="DescribeDBProxies",
        argument=["DBProxies[].Status"],
        acceptors=delete_waiter_acceptors,
        client=await hub.tool.boto3.client.get_client(ctx, "rds"),
    )
    try:
        await hub.tool.boto3.client.wait(
            ctx,
            "rds",
            "DBProxyDeleted",
            cluster_waiter,
            DBProxyName=resource_id,
            WaiterConfig=waiter_config,
        )
    except Exception as e:
        result["comment"] += [str(e)]
        result["result"] = False
        return result

    return result
