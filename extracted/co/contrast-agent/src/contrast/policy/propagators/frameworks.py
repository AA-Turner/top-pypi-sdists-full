# Copyright © 2026 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from contrast.agent.policy.registry import register_propagation_nodes
from contrast.agent.policy.utils import CompositeNode


framework_propagators = [
    {
        "module": "starlette.staticfiles",
        "class_name": "StaticFiles",
        "method_name": "lookup_path",
        "source": "ARG_0,KWARG:path",
        "target": "RETURN",
        "action": "STARLETTE_LOOKUP_PATH",
        "tags": ["SAFE_PATH"],
    },
    {
        "module": "bottle",
        "method_name": "html_escape",
        "source": "ARG_0,KWARG:string",
        "target": "RETURN",
        "action": "SPLAT",
        "tags": ["HTML_ENCODED"],
        "untags": ["HTML_DECODED"],
    },
    {
        "module": "django.utils.html",
        "method_name": "escape",
        "source": "ARG_0,KWARG:text",
        "target": "RETURN",
        "action": "SPLAT",
        "tags": ["HTML_ENCODED"],
        "untags": ["HTML_DECODED"],
    },
    {
        # Special deadzoned patch implemented outside of policy
        "module": "django.utils.safestring",
        "method_name": "mark_safe",
        "source": "ARG_0,KWARG:s",
        "target": "RETURN",
        "action": "KEEP",
        "policy_patch": False,
    },
    {
        "module": "django.utils._os",
        "method_name": "safe_join",
        "source": "ALL_ARGS",
        "target": "RETURN",
        "action": "SAFE_JOIN_DJANGO",
        "tags": ["SAFE_PATH"],
    },
    {
        "module": "django.core.files.storage",  # for django<4.2
        "class_name": "Storage",
        "method_name": "get_available_name",
        "source": "ARG_0,KWARG:name",
        "target": "RETURN",
        "action": "SPLAT",
        "tags": ["SAFE_PATH"],
    },
    {
        "module": "django.core.files.storage.base",  # for django>=4.2
        "class_name": "Storage",
        "method_name": "get_available_name",
        "source": "ARG_0,KWARG:name",
        "target": "RETURN",
        "action": "SPLAT",
        "tags": ["SAFE_PATH"],
    },
    {
        "module": "django.db.models.base",
        "class_name": "Model",
        "method_name": "__init__",
        "source": "ALL_KWARGS",
        "target": "OBJ",
        "action": "DB_WRITE",
        "tags": ["DATABASE_WRITE"],
    },
    {
        # This is a deadzone property patch. See drf_patches.py.
        # source, target, and action here have no real meaning
        "module": "rest_framework.response",
        "class_name": "Response",
        "method_name": "rendered_content",
        "source": "ARG_0",
        "target": "RETURN",
        "action": "deadzone (placeholder)",
        "policy_patch": False,
    },
    {
        "module": "html",
        "method_name": "escape",
        "source": "ARG_0,KWARG:s",
        "target": "RETURN",
        "action": "SPLAT",
        "tags": ["HTML_ENCODED"],
        "untags": ["HTML_DECODED"],
    },
    {
        # This function was removed in Quart 0.18. There is no sanitizer for python object to json string conversion
        # https://github.com/pallets/quart/compare/0.17.0...0.18.3#diff-8544903fbe8454006675de99682a15abd67c106228ba1864f19b9b379ded9acaL73
        "module": "quart.json",
        "method_name": "htmlsafe_dumps",
        "source": "ARG_0,KWARG:object_",
        "target": "RETURN",
        "action": "SPLAT",
        "tags": ["HTML_ENCODED"],
        "untags": ["HTML_DECODED"],
    },
    {
        # escape_silent must  be patched in addition to escape because if the
        # C-implemented version of this is used we won't patch the internal
        # call (to the C-implemented `escape`)
        "module": "markupsafe",
        # markupsafe includes both a C implementation and a native python implementation
        # These methods accept a kwarg in the native implementation only
        "method_name": ["escape", "escape_silent"],
        "source": "ARG_0,KWARG:s",
        "target": "RETURN",
        "action": "ENCODE_HTML_SPLAT",
        "tags": ["HTML_ENCODED"],
        "untags": ["HTML_DECODED"],
    },
    {
        # markupsafe includes both a C implementation and a native python implementation",
        # soft_str() accepts a kwarg in the native implementation only",
        "module": "markupsafe",
        "method_name": "soft_str",
        "source": "ARG_0,KWARG:s",
        "target": "RETURN",
        "action": "SPLAT",
    },
    CompositeNode(
        {
            "module": "falcon.util.uri",
            "target": "RETURN",
            "action": "SPLAT",
        },
        [
            {
                "method_name": ["encode", "encode_value"],
                "source": "ARG_0,KWARG:uri",
                "tags": ["URL_ENCODED"],
            },
            {
                "method_name": "decode",
                "source": "ARG_0,KWARG:encoded_uri",
                "untags": ["URL_ENCODED"],
            },
            {
                "method_name": "unquote_string",
                "source": "ARG_0,KWARG:quoted",
                "untags": ["URL_ENCODED"],
            },
        ],
    ),
    {
        "module": "falcon.util.misc",
        "method_name": "secure_filename",
        "source": "ARG_0",
        "target": "RETURN",
        "action": "SPLAT",
        # XPATH_ENCODED means that the string is path-traversal safe, but
        # it is still UNTRUSTED because it may be dangerous for other rules
        "tags": ["XPATH_ENCODED"],
    },
    {
        "module": "werkzeug.security",
        "method_name": "safe_join",
        "source": "ALL_ARGS",
        "target": "RETURN",
        "action": "SAFE_JOIN",
        "tags": ["SAFE_PATH"],
    },
    CompositeNode(
        {
            "module": "werkzeug.utils",
            "target": "RETURN",
        },
        [
            {
                "method_name": "secure_filename",
                "source": "ARG_0,KWARG:filename",
                "action": "SPLAT",
                # XPATH_ENCODED means that the string is path-traversal safe, but
                # it is still UNTRUSTED because it may be dangerous for other rules
                "tags": ["XPATH_ENCODED"],
            },
            {
                "method_name": "escape",
                "source": "ARG_0,KWARG:s",
                "action": "ENCODE_HTML_SPLAT",
                "tags": ["HTML_ENCODED"],
                "untags": ["HTML_DECODED"],
            },
        ],
    ),
    {
        "module": "flask.helpers",
        "method_name": "safe_join",
        "source": "ALL_ARGS",
        "target": "RETURN",
        "action": "SAFE_JOIN",
        "tags": ["SAFE_PATH"],
    },
]

register_propagation_nodes(framework_propagators)
