# Copyright © 2026 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from typing import TypedDict

# Unfortunately, TypedDicts do not currently support arbitrary extra keys in addition to
# required keys, so we cannot use one here.
EventDict = dict
"""
Part of a v2 policy definition that contains any metadata required to build event
handler functions. At minimum, has an event `name` key.
"""


class PolicyDefinition(TypedDict):
    """
    v2 policy definition for a group of functions that share an event type. Used for
    literal contrast-defined policy.

    Try to keep this easily JSON-serializable in case we want to support receiving
    policy definitions from external sources in the future.
    """

    module: str
    method_names: list[str]
    event: EventDict


def definitions() -> list[PolicyDefinition]:
    """
    Returns a list of all v2 policy definitions.
    """
    return cmd_exec + file_open + authn + authz + outbound_request + graphql_request


cmd_exec: list[PolicyDefinition] = [
    {
        "module": "os",
        "method_names": ["system"],
        "event": {
            "name": "cmd-exec",
            "cmd": "command",
        },
    },
    {
        "module": "subprocess",
        "method_names": ["Popen.__init__"],
        "event": {
            "name": "cmd-exec",
            "cmd": "executable",
            "args": "args",
            "shell": "shell",
        },
    },
    {
        "module": "os",
        "method_names": ["spawnv", "spawnvp", "spawnve", "spawnvpe"],
        "event": {
            "name": "cmd-exec",
            "args": "args",
            # There could be an argument that we should include "file" as the "cmd".
            # This will often be the same as args[0] though, and we don't want the command
            # string to stutter. Using just "args" is likely to be closer to the user's
            # intent.
        },
    },
]

file_open: list[PolicyDefinition] = [
    {
        "module": "builtins",
        "method_names": ["open"],
        "event": {
            "name": "file-open",
            "file": "file",
            "flags": "mode",
        },
    },
    {
        "module": "os",
        "method_names": ["open"],
        "event": {
            "name": "file-open",
            "file": "path",
            "flags": "flags",
        },
    },
    {
        "module": "dbm.dumb",
        "method_names": ["open"],
        "event": {
            "name": "file-open",
            "file": "file",
            "flags": "flag",
            "dbm": True,
        },
    },
    {
        "module": "dbm.gnu",
        "method_names": ["open"],
        "event": {
            "name": "file-open",
            "file": "filename",
            "flags": "flags",
            "dbm": True,
        },
    },
    {
        "module": "dbm.ndbm",
        "method_names": ["open"],
        "event": {
            "name": "file-open",
            "file": "filename",
            "flags": "flags",
            "dbm": True,
        },
    },
]

authn: list[PolicyDefinition] = [
    {
        "module": "django.contrib.auth",
        "method_names": ["authenticate", "aauthenticate"],
        "event": {
            "name": "django-authn",
            "mechanisms": ["token", "password"],
        },
    },
    {
        "module": "django.contrib.auth",
        "method_names": ["get_user", "aget_user"],
        "event": {
            "name": "django-session-authn",
            "mechanism": "token",
        },
    },
    {
        "module": "starlette.middleware.authentication",
        "method_names": ["AuthenticationMiddleware.__call__"],
        "event": {
            "name": "starlette-authn",
        },
    },
]

authz: list[PolicyDefinition] = [
    {
        "module": "django.contrib.auth.models",
        "method_names": [
            "PermissionsMixin.has_perm",
            "PermissionsMixin.ahas_perm",
            "AnonymousUser.has_perm",
            "AnonymousUser.ahas_perm",
        ],
        "event": {
            "name": "authz",
            "dac_perm": "perm",
        },
    },
    {
        "module": "django.contrib.auth.models",
        "method_names": [
            "PermissionsMixin.has_module_perms",
            "PermissionsMixin.ahas_module_perms",
        ],
        "event": {
            "name": "authz",
            "dac_perm": "app_label",
        },
    },
    {
        "module": "django.contrib.auth.models",
        "method_names": [
            "AnonymousUser.has_module_perms",
            "AnonymousUser.ahas_module_perms",
        ],
        "event": {
            "name": "authz",
            "dac_perm": "module",
        },
    },
    {
        "module": "django.contrib.auth.models",
        "method_names": ["UserManager.with_perm"],
        "event": {
            "name": "authz",
            "dac_perm": "perm",
        },
    },
    {
        "module": "starlette.authentication",
        "method_names": ["has_required_scope"],
        "event": {
            "name": "authz",
            "dac_perms": "scopes",
        },
    },
]

outbound_request: list[PolicyDefinition] = [
    {
        "module": "urllib.request",
        "method_names": ["urlopen"],
        "event": {
            "name": "outbound-request",
            "url": "url",
        },
    },
    {
        "module": "http.client",
        "method_names": ["HTTPConnection.putrequest"],
        "event": {
            "name": "outbound-request-http.client",  # special case for http.client
        },
    },
    {
        "module": "httpx._client",
        "method_names": ["BaseClient.build_request"],
        "event": {
            "name": "outbound-request",
            "url": "url",  # str | httpx.URL
        },
    },
    {
        "module": "aiohttp",
        "method_names": ["ClientSession._request"],
        "event": {
            "name": "outbound-request",
            "url": "str_or_url",  # str | yarl.URL
        },
    },
    {
        "module": "requests.sessions",
        "method_names": [
            "Session.request",
        ],
        "event": {
            "name": "outbound-request",
            "url": "url",
        },
    },
]

graphql_request: list[PolicyDefinition] = [
    {
        "module": "ariadne.graphql",
        "method_names": ["parse_query"],
        "event": {
            "name": "graphql-request",
        },
    }
]
