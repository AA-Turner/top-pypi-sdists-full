import typing as t


def parse_permission_args(resource_str: str) -> t.Dict[str, str]:
    """
    Parse permission arguments from a resource string.

    Args:
        resource_str: String containing resource and optional permission args
            in the format: resource/arg1,arg2,{key1=val1,key2=val2}

    Returns:
        Dictionary of permission arguments
    """
    # Check for multiple argument blocks
    if resource_str.count("{") > 1:
        raise ValueError(
            f"Invalid permission string '{resource_str}'. "
            "Multiple argument blocks found"
        )
    if ",{" not in resource_str:
        return {}

    args_str = resource_str.split(",{", 1)[1]
    if not args_str.endswith("}"):
        raise ValueError(
            f"Invalid permission string '{resource_str}' ",
            "Missing closing brace",
        )
    args_str = args_str[:-1]  # Remove closing brace

    args = {}
    if args_str:
        for arg in args_str.split(","):
            if "=" not in arg:
                raise ValueError(
                    f"Invalid argument format in '{resource_str}'. "
                    "Expected key=value"
                )
            key, value = arg.split("=")
            args[key.strip()] = value.strip()

    return args


def parse_body(body: t.List[str]) -> t.List[t.Dict[str, t.Any]]:
    """Parse the body of a role definition."""
    clauses = []
    for clause in body:
        if ":" in clause:
            # This is a permission
            actions_str, resource_str = clause.split(":")

            # Extract permission arguments if present
            perm_args = parse_permission_args(resource_str)
            # Clean up resource string by removing argument block if present
            resource_str = resource_str.split("{")[0]

            resource_name, _, _ = resource_str.partition("/")
            actions = set(actions_str.split("+"))
            clauses.append(
                {
                    "type": "permission",
                    "actions": actions,
                    "resource_name": resource_name,
                    "args": perm_args,
                }
            )
        else:
            # This is a sub-role
            clauses.append({"type": "sub_role", "sub_role_name": clause})
    return clauses


def parse_permission(clause: str) -> t.Dict[str, t.Any]:
    """Parse a permission clause into its components.

    Format: action:resource/arg1,arg2,arg3,{key1=val1,key2=val2}

    Optional curly braces contain permission arg key-value pairs.
    A comma before the curly braces is required if args are present.
    """
    action_str, _, resource_str = clause.partition(":")
    actions = action_str.split("+") if action_str else []

    # Extract permission arguments if present
    perm_args = parse_permission_args(resource_str)
    # Clean up resource string by removing argument block if present
    resource_str = resource_str.split(",{")[0]

    resource_name, _, args_str = resource_str.partition("/")
    resource_args = args_str.split(",") if args_str else []

    return {
        "type": "permission",
        "actions": actions,
        "resource_name": resource_name,
        "resource_args": resource_args,
        "args": perm_args,
    }


def parse_sub_role(clause: str) -> t.Dict[str, t.Any]:
    sub_role, sep, sub_role_args_str = clause.partition("/")
    sub_role_args = sub_role_args_str.split(",") if sub_role_args_str else []
    return {
        "type": "role",
        "sub_role_name": sub_role,
        "sub_role_args": sub_role_args,
    }
