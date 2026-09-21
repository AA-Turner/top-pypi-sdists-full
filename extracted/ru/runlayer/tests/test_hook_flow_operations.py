"""Every installed hook event that can deny is recorded as an enforcement flow.

The fleet hook-failure alerts are scoped to ``cli.hook_pre_tool`` /
``cli.hook_post_tool`` because only those flows can fail closed. An
enforcement hook spooled as ``cli.hook_event`` would hide a deny outage from
them, so the flow operation is checked against what each client installs.
"""

from collections.abc import Mapping

import pytest

from runlayer_cli.hook.clients import Client, normalize_event_name
from runlayer_cli.hook.dispatch import _hook_operation
from runlayer_cli.hook_install.clients import _ENFORCEMENT_HOOKS, _PIPELINE_HOOKS

_ENFORCEMENT_OPERATIONS = frozenset({"cli.hook_pre_tool", "cli.hook_post_tool"})
_OBSERVATIONAL_OPERATIONS = frozenset({"cli.hook_event", "cli.hook_stop"})


def _installed(table: Mapping[Client, tuple[str, ...]]) -> set[tuple[str, str]]:
    return {(client.value, name) for client, names in table.items() for name in names}


# Some clients register PostToolUse / PermissionRequest telemetry-only. The flow
# operation follows the event, not the installing client, so a pipeline
# registration of an event that is an enforcement hook elsewhere is still an
# enforcement flow.
_ENFORCEMENT_EVENTS = frozenset(
    normalize_event_name(name) for _, name in _installed(_ENFORCEMENT_HOOKS)
)


@pytest.mark.parametrize(
    ("client", "name"),
    sorted(_installed(_ENFORCEMENT_HOOKS) | _installed(_PIPELINE_HOOKS)),
)
def test_installed_hook_records_flow_by_deny_capability(client: str, name: str) -> None:
    event = normalize_event_name(name)
    expected = (
        _ENFORCEMENT_OPERATIONS
        if event in _ENFORCEMENT_EVENTS
        else _OBSERVATIONAL_OPERATIONS
    )
    operation = _hook_operation(event)
    assert operation in expected, (client, name, event, operation)
