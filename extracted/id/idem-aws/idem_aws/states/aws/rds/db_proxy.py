"""States module for managing Rds Db Proxys."""
import copy
from dataclasses import field
from dataclasses import make_dataclass
from typing import Any
from typing import Dict
from typing import List

from dict_tools import differ

__contracts__ = ["resource"]


async def present(
    hub,
    ctx,
    name: str,
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
    resource_id: str = None,
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

        name(str): Idem name of the resource.

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

        resource_id(str, Optional): Db_proxy unique ID. Defaults to None.

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

    Example:
        .. code-block:: sls


          idem_test_aws.rds.db_proxy_is_present:
              aws.rds.db_proxy.present:
              - db_proxy_name: string
              - engine_family: string
              - auth:
                - auth_scheme: string
                  client_password_auth_type: string
                  description: string
                  iam_auth: string
                  secret_arn: string
                  user_name: string
              - role_arn: string
              - vpc_subnet_ids:
                - value
              - vpc_security_group_ids:
                - value
              - require_tls: bool
              - idle_client_timeout: int
              - debug_logging: bool
              - tags:
                - key: string
                  value: string


    """

    result = dict(
        comment=[], old_state={}, new_state={}, name=name, result=True, rerun_data=None
    )

    desired_state = {
        k: v
        for k, v in locals().items()
        if k not in ("hub", "ctx", "kwargs", "result") and v is not None
    }

    current_state = None

    if resource_id:
        before = await hub.exec.aws.rds.db_proxy.get(
            ctx, name=name, resource_id=resource_id
        )
        if not before["result"] or not before["ret"]:
            result["result"] = False
            result["comment"] = before["comment"]
            return result

        result["old_state"] = current_state = copy.deepcopy(before["ret"])
        result["comment"] += hub.tool.aws.comment_utils.already_exists_comment(
            resource_type="aws.rds.db_proxy", name=name
        )

    if current_state:
        # If there are changes in desired state from existing state
        changes = differ.deep_diff(
            current_state if current_state else {}, desired_state
        )

        if bool(changes.get("new")):
            if ctx.test:
                result["new_state"] = hub.tool.aws.test_state_utils.generate_test_state(
                    enforced_state={}, desired_state=desired_state
                )
                result["comment"] += hub.tool.aws.comment_utils.would_update_comment(
                    resource_type="aws.rds.db_proxy", name=name
                )
                return result
            else:
                # Update the resource
                update_ret = await hub.exec.aws.rds.db_proxy.update(
                    ctx,
                    resource_id=resource_id,
                    new_db_proxy_name=db_proxy_name,
                    auth=auth,
                    require_tls=require_tls,
                    idle_client_timeout=idle_client_timeout,
                    debug_logging=debug_logging,
                    role_arn=role_arn,
                    security_groups=vpc_security_group_ids,
                    name=name,
                    tags=tags,
                )
                result["result"] = update_ret["result"]

                if result["result"]:
                    resource_id = update_ret["ret"].get("resource_id", resource_id)
                    result["comment"] += hub.tool.aws.comment_utils.update_comment(
                        resource_type="aws.rds.db_proxy", name=name
                    )
                else:
                    result["comment"] += update_ret["comment"]
    else:
        if ctx.get("test", False):
            result["new_state"] = hub.tool.aws.test_state_utils.generate_test_state(
                enforced_state={}, desired_state=desired_state
            )
            result["comment"] += hub.tool.aws.comment_utils.would_create_comment(
                resource_type="aws.rds.db_proxy", name=name
            )
            return result

        create_ret = await hub.exec.aws.rds.db_proxy.create(
            ctx, **desired_state, timeout=timeout
        )
        result["result"] = create_ret["result"]

        if result["result"]:
            result["comment"] = hub.tool.aws.comment_utils.create_comment(
                resource_type="aws.rds.db_proxy", name=name
            )

            resource_id = create_ret["ret"].get("resource_id")
            # Safeguard for any future errors so that the resource_id is saved in the ESM
            result["new_state"] = dict(name=name, resource_id=resource_id)
        else:
            result["comment"].append(create_ret["comment"])

    if not result["result"]:
        # If there is any failure in create/update, it should reconcile.
        # The type of data is less important here to use default reconciliation
        # If there are no changes for 3 runs with rerun_data, then it will come out of execution
        result["rerun_data"] = dict(name=name, resource_id=resource_id)

    after = await hub.exec.aws.rds.db_proxy.get(ctx, name=name, resource_id=resource_id)
    result["new_state"] = after.ret
    return result


async def absent(
    hub,
    ctx,
    name: str,
    resource_id: str = None,
    timeout: make_dataclass(
        """Specifies timeout for deletion of DB Proxy.""" "Timeout",
        [
            (
                "delete",
                make_dataclass(
                    "DeleteTimeout",
                    [
                        ("delay", int, field(default=40)),
                        ("max_attempts", int, field(default=60)),
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
        name(str): Idem name of the resource.

        resource_id(str, Optional): Db_proxy unique ID. Defaults to None.

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

    Example:
        .. code-block:: sls

            idem_test_aws.rds.db_proxy_is_absent:
              aws.rds.db_proxy.absent:
              - db_proxy_name: string


    """

    result = dict(
        comment=[], old_state={}, new_state={}, name=name, result=True, rerun_data=None
    )

    if not resource_id:
        resource_id = (ctx.old_state or {}).get("resource_id")

    # This is to make absent idempotent. If absent is run again, it would be a no-op
    if not resource_id:
        result["comment"] += hub.tool.aws.comment_utils.already_absent_comment(
            resource_type="aws.rds.db_proxy", name=name
        )
        return result

    before = await hub.exec.aws.rds.db_proxy.get(
        ctx, name=name, resource_id=resource_id
    )

    # Case: Error
    if not before["result"]:
        result["result"] = False
        result["comment"] = before["comment"]
        return result

    # Case: Not Found
    if not before["ret"]:
        result["comment"] += hub.tool.aws.comment_utils.already_absent_comment(
            resource_type="aws.rds.db_proxy", name=name
        )
        return result

    result["old_state"] = before["ret"]
    if ctx.get("test", False):
        result["comment"] += hub.tool.aws.comment_utils.would_delete_comment(
            resource_type="aws.rds.db_proxy", name=name
        )
        return result

    delete_ret = await hub.exec.aws.rds.db_proxy.delete(
        ctx, name=name, resource_id=resource_id, timeout=timeout
    )

    result["result"] = delete_ret["result"]

    if not result["result"]:
        # If there is any failure in delete, it should reconcile.
        # The type of data is less important here to use default reconciliation
        # If there are no changes for 3 runs with rerun_data, then it will come out of execution
        result["rerun_data"] = resource_id
        result["comment"].append(delete_ret["comment"])
    else:
        result["comment"] += hub.tool.aws.comment_utils.delete_comment(
            resource_type="aws.rds.db_proxy", name=name
        )
    return result


async def describe(hub, ctx) -> Dict[str, Dict[str, Any]]:
    """
    Describe the resource in a way that can be recreated/managed with the corresponding "present" function

    Returns information about DB proxies.

    Returns:
        Dict[str, Any]

    Example:

        .. code-block:: bash

            $ idem describe aws.rds.db_proxy
    """

    result = {}
    ret = await hub.exec.aws.rds.db_proxy.list(ctx)

    if not ret or not ret["result"]:
        hub.log.warning(f"Could not describe aws.rds.db_proxy {ret['comment']}")
        return result

    for resource in ret["ret"]:
        resource_id = resource.get("resource_id")
        result[resource_id] = {
            "aws.rds.db_proxy.present": [
                {parameter_key: parameter_value}
                for parameter_key, parameter_value in resource.items()
            ]
        }
    return result
