# Copyright © 2025 Contrast Security, Inc.
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
    return cmd_exec + file_open


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
