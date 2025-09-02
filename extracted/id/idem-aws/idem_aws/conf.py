CLI_CONFIG = {
    # pop-create options
    "services": {
        "subcommands": ["aws"],
        "dyne": "pop_create",
    },
    "service_resources": {
        "subcommands": ["aws"],
        "dyne": "pop_create",
    },
    "sync_sls_name_and_name_tag": {
        "action": "store_true",
        "subcommands": ["state"],
        "dyne": "idem",
    },
}
CONFIG = {
    # pop-create options
    "services": {
        "default": [],
        "nargs": "*",
        "help": "The cloud services to target, defaults to all",
        "dyne": "pop_create",
    },
    "service_resources": {
        "default": [],
        "nargs": "*",
        "help": "The cloud service resources to target in autogen, defaults to all",
        "dyne": "pop_create",
    },
    "sync_sls_name_and_name_tag": {
        "default": False,
        "help": "If set to true, tags for a resource will be modified to use the SLS name as a Name tag",
        "dyne": "idem",
    },
}
SUBCOMMANDS = {
    "aws": {
        "help": "Create idem_aws state modules by parsing boto3",
        "dyne": "pop_create",
    },
}
DYNE = {
    "acct": ["acct"],
    "exec": ["exec"],
    "pop_create": ["autogen"],
    "states": ["states"],
    "tool": ["tool"],
    "esm": ["esm"],
    "reconcile": ["reconcile"],
}
