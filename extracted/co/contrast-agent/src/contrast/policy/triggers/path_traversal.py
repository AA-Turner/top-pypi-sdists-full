# Copyright © 2026 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from contrast.agent.assess.rules.dataflow_rule import DataflowRule
from contrast.agent.policy.registry import register_trigger_rule
from contrast.agent.policy.utils import CompositeNode


DISALLOWED_TAGS = [
    "CUSTOM_ENCODED_PATH_TRAVERSAL",
    "CUSTOM_ENCODED",
    "CUSTOM_VALIDATED_PATH_TRAVERSAL",
    "CUSTOM_VALIDATED",
    "LIMITED_CHARS",
    "NO_CONTROL_CHARS",
    "SAFE_PATH",
    "BASE64_ENCODED",
    "CSS_ENCODED",
    "CSV_ENCODED",
    "HTML_ENCODED",
    "JAVASCRIPT_ENCODED",
    "JAVA_ENCODED",
    "LDAP_ENCODED",
    "OS_ENCODED",
    "URL_ENCODED",
    "VBSCRIPT_ENCODED",
    "XML_ENCODED",
    "XPATH_ENCODED",
]


path_traversal_triggers = [
    {
        "module": "builtins",
        "method_name": "open",
        "source": "ARG_0,KWARG:file",
        "protect_mode": True,
    },
    CompositeNode(
        {
            "module": "os",
            "protect_mode": True,
        },
        [
            {
                "method_name": [
                    "open",
                    "unlink",
                    "remove",
                    "rmdir",
                    "chdir",
                    "chroot",
                ],
                "source": "ARG_0,KWARG:path",
            },
            {
                "method_name": [
                    "rename",
                    "link",
                    "symlink",
                    "replace",
                ],
                "source": "ARG_0,ARG_1,KWARG:src,KWARG:dst",
            },
            {
                "method_name": "renames",
                "source": "ARG_0,ARG_1,KWARG:old,KWARG:new",
            },
            {
                "method_name": [
                    "mkdir",
                    "chmod",
                    "lchmod",
                    "access",
                    "chflags",
                    "lchflags",
                    "truncate",
                    "utime",
                    "chown",
                    "lchown",
                    "setxattr",  # Linux only
                    "removexattr",  # Linux only
                ],
                "source": "ARG_0,KWARG:path",
            },
            {
                "method_name": "makedirs",
                "source": "ARG_0,KWARG:name",
            },
            {
                "method_name": ["walk", "fwalk"],
                "source": "ARG_0,KWARG:top",
            },
        ],
    ),
    CompositeNode(
        {
            "module": "shutil",
            "protect_mode": True,
        },
        [
            {
                "method_name": "rmtree",
                "source": "ARG_0,KWARG:path",
            },
            {
                "method_name": [
                    "copyfile",
                    "copymode",
                    "copystat",
                    "copy",
                    "copy2",
                    "copytree",
                    "move",
                ],
                "source": "ARG_0,ARG_1,KWARG:src,KWARG:dst",
            },
            {
                "method_name": "chown",
                "source": "ARG_0,KWARG:path",
            },
            {
                "method_name": "make_archive",
                "source": "ARG_0,ARG_2,ARG_3,KWARG:base_name,KWARG:root_dir,KWARG:base_dir",
            },
            {
                "method_name": "unpack_archive",
                "source": "ARG_0,ARG_1,KWARG:filename,KWARG:extract_dir",
            },
        ],
    ),
    {
        "module": [f"dbm.{name}" for name in ["ndbm", "gnu"]],
        "method_name": "open",
        # This function takes no kwargs
        "source": "ARG_0",
        "protect_mode": True,
    },
    {
        "module": "dbm.dumb",
        "method_name": "open",
        "source": "ARG_0,KWARG:file",
        "protect_mode": True,
    },
]


register_trigger_rule(
    DataflowRule.from_nodes(
        "path-traversal",
        path_traversal_triggers,
        disallowed_tags=DISALLOWED_TAGS,
    )
)
