"""Calls a type checker must accept, and calls it must reject.

Not a test module. ``test_request_annotations.py`` runs mypy over this file
with ``--warn-unused-ignores``, so every ``# type: ignore[code]`` below asserts
that mypy reports exactly that error on that line, and every other line asserts
that it reports nothing.
"""

from __future__ import annotations

from typing import Literal

from typing_extensions import assert_type

from composio_client import AsyncComposio, Composio
from composio_client.types.link_create_response import LinkCreateResponse
from composio_client.types.tool_router.session_create_response import (
    ConfigToolkitsDisabled,
    ConfigToolkitsEnabled,
    ConfigToolkitsRequireApproval,
)
from composio_client.types.tool_router.session_execute_response import (
    SessionExecuteBlockedResponse,
    SessionExecuteInputRequiredResponse,
    SessionExecuteResponse,
)
from composio_client.types.tool_router.session_proxy_execute_response import (
    SessionProxyExecuteBlockedResponse,
    SessionProxyExecuteInputRequiredResponse,
    SessionProxyExecuteResponse,
)
from composio_client.types.trigger_instances.manage_update_params import ManageUpdateParams


def released_operations(client: Composio) -> None:
    # The Stainless flat form, typed with the annotations Stainless declared.
    assert_type(client.link.create(auth_config_id="ac_1", user_id="user_1"), LinkCreateResponse)
    # A required field the runtime would refuse is refused statically too.
    client.link.create(user_id="user_1")  # type: ignore[call-overload]
    # So is a value of the wrong type.
    client.link.create(auth_config_id=1, user_id="user_1")  # type: ignore[call-overload]
    # A captured Literal.
    client.connected_accounts.list(order_direction="asc")
    client.connected_accounts.list(order_direction="upward")  # type: ignore[arg-type]
    # A Literal member the spec added after the capture.
    client.tool_router.session.execute_meta("sess_1", slug="COMPOSIO_SUBMIT_FEEDBACK")
    # The raw and streaming twins carry the same signatures.
    client.link.with_raw_response.create(user_id="user_1")  # type: ignore[call-overload]
    client.link.with_streaming_response.create(user_id="user_1")  # type: ignore[call-overload]


def additive_operations(client: Composio) -> None:
    configs = client.session_configs.list(limit=5, archived=False)
    assert_type(configs.items[0].id, str)
    client.session_configs.retrieve("sc_1")
    session = client.tool_router.session.create(
        user_id="user_1",
        instant={"toolkits": {"enable": ["github"]}, "return_instant_charge": True},
        workbench={"enable_tool_execution": True},
    )
    assert_type(session.config.instant is False, bool)
    assert session.config.instant is not False
    assert_type(session.config.instant.return_instant_charge, bool)
    assert session.config.workbench is not None
    assert_type(session.config.workbench.tool_execution_enabled, bool | None)
    client.tool_router.session.create(user_id="u", instant={"return_instant_charge": "yes"})  # type: ignore[call-overload]
    executed = client.tool_router.session.execute("sess_1", tool_slug="GITHUB_X")
    assert_type(
        executed, SessionExecuteResponse | SessionExecuteBlockedResponse | SessionExecuteInputRequiredResponse
    )
    if executed.result_type == "input_required":
        assert_type(executed, SessionExecuteInputRequiredResponse)
        assert_type(executed.request_state, str | None)
    elif executed.result_type == "blocked":
        assert_type(executed, SessionExecuteBlockedResponse)
        assert_type(executed.message, str)
    else:
        assert_type(executed, SessionExecuteResponse)
        assert_type(executed.log_id, str)
    proxied = client.tool_router.session.proxy_execute(
        "sess_1", toolkit_slug="gmail", endpoint="/messages", method="GET"
    )
    if proxied.result_type == "input_required":
        assert_type(proxied, SessionProxyExecuteInputRequiredResponse)
    elif proxied.result_type == "blocked":
        assert_type(proxied, SessionProxyExecuteBlockedResponse)
    else:
        assert_type(proxied, SessionProxyExecuteResponse)
        assert_type(proxied.status, float)
    # The `...Response` name is still a class: constructible and subclassable.
    assert_type(SessionExecuteResponse(data={}, log_id="l"), SessionExecuteResponse)

    class Mine(SessionExecuteResponse): ...

    assert_type(Mine(data={}, log_id="l").result_type, Literal["completed", "failed"] | None)
    client.tool_router.session.create(user_id="u", workbench={"enable_tool_execution": "yes"})  # type: ignore[call-overload]
    client.tool_router.session.patch("sess_1", experimental={"session_config_id": "sc_1"})
    # A union variant the spec added after the capture is accepted, on the
    # request side and as a narrowable class on the response side.
    approval = client.tool_router.session.create(
        user_id="u",
        toolkits={"require_approval": ["github"]},
        tools={"github": {"require_approval": ["GITHUB_X"]}, "gmail": {"enable": ["GMAIL_X"]}},
    )
    client.tool_router.session.patch("sess_1", toolkits={"require_approval": ["github"]})
    client.tool_router.session.create(user_id="u", toolkits={"require_approvals": ["github"]})  # type: ignore[call-overload]
    if isinstance(approval.config.toolkits, ConfigToolkitsRequireApproval):
        assert_type(approval.config.toolkits.require_approval, list[str])
    assert_type(
        approval.config.toolkits,
        ConfigToolkitsEnabled | ConfigToolkitsDisabled | ConfigToolkitsRequireApproval | None,
    )
    client.trigger_instances.manage.update("tr_1", egress_url=None, user_id="u")
    egress_update: ManageUpdateParams = {"egress_url": None, "user_id": "u"}
    client.trigger_instances.manage.update("tr_1", **egress_update)
    # A nested object is a TypedDict in the operation's own params module.
    client.org.owner.project.create(
        name="project",
        config={
            "is_2FA_enabled": True,
            "mask_secret_keys_in_connected_account": False,
            "log_visibility_setting": "show_all",
        },
    )
    client.org.owner.project.create(name="project", config={"is_2FA_enabled": "yes"})  # type: ignore[call-overload]
    # A path parameter is a string.
    client.logs.retrieve_tool_execution(1)  # type: ignore[arg-type]


def pre_release_forms(client: Composio) -> None:
    # The aggregate forms MIGRATION.md still promises type-check through their own stubs.
    client.link.create({"auth_config_id": "ac_1", "user_id": "user_1"})
    client.tool_router.session.config_history("sess_1", query={"limit": 25})
    client.tool_router.session.files.list("sess_1", "mount_1")
    client.tool_router.session.files.list("mount_1", session_id="sess_1")
    client.tool_router.session.files.list("mount_1")  # type: ignore[call-overload]
    client.tool_router.session.files.delete("sess_1", "mount_1", {"mount_relative_path": "/file.txt"})
    client.tool_router.session.files.delete("sess_1", "mount_1", body={"mount_relative_path": "/file.txt"})
    client.tool_router.session.files.delete("sess_1", "mount_1", mount_relative_path="/file.txt")
    client.tool_router.session.files.delete("sess_1", "mount_1")  # type: ignore[call-overload]
    client.tool_router.session.files.delete(  # type: ignore[call-overload]
        "sess_1", "mount_1", {"mount_relative_path": "/file.txt"}, object()
    )
    client.tools.list(query="github")
    client.tools.list(query={"limit": 1})
    client.tools.proxy({"endpoint": "/repos", "method": "GET"})
    client.tools.proxy(endpoint="/repos", method="GET")
    client.tools.proxy(method="GET")  # type: ignore[call-overload]


async def async_operations(client: AsyncComposio) -> None:
    await client.session_configs.list(limit=5)
    await client.session_configs.retrieve("sc_1")
    await client.tool_router.session.create(
        user_id="u", instant=False, workbench={"enable_tool_execution": True}
    )
    assert_type(await client.link.create(auth_config_id="ac_1", user_id="user_1"), LinkCreateResponse)
    await client.link.create(user_id="user_1")  # type: ignore[call-overload]
