"""Tests for the @uses_connectors decorator and ConnectorSlot.

Verifies that connector metadata is correctly attached
to the workflow class regardless of decorator ordering.
"""

from __future__ import annotations

from mistralai.workflows import get_workflow_definition, workflow
from mistralai.workflows.plugins.mistralai.connectors import connector, uses_connectors
from mistralai.workflows.plugins.mistralai.connectors.client import ToolCallClient
from mistralai.workflows.plugins.mistralai.connectors.constants import (
    CONNECTORS_KEY,
    MISTRALAI_PLUGIN_KEY,
)
from mistralai.workflows.plugins.mistralai.connectors.decorator import ConnectorSlot

slack = connector("slack")
github = connector("github", auto_auth=False)
jira = connector("jira", credentials_name="jira_service_account")


class TestUsesConnectorsBeforeDefine:
    """@uses_connectors applied BEFORE @workflow.define."""

    def test_plugin_metadata_attached(self) -> None:
        @workflow.define(name="test-connectors-before-define")
        @uses_connectors(slack)
        class MyWorkflow:
            @workflow.entrypoint
            async def run(self) -> str:
                return "done"

        defn = get_workflow_definition(MyWorkflow)
        assert defn.plugin_metadata is not None
        connectors = defn.plugin_metadata[MISTRALAI_PLUGIN_KEY][CONNECTORS_KEY]
        assert len(connectors) == 1
        assert connectors[0]["connector_name"] == "slack"
        assert connectors[0]["auto_auth"] is True

    def test_multiple_connectors(self) -> None:
        @workflow.define(name="test-multi-connectors-before")
        @uses_connectors(slack, github)
        class MyWorkflow:
            @workflow.entrypoint
            async def run(self) -> str:
                return "done"

        defn = get_workflow_definition(MyWorkflow)
        connectors = defn.plugin_metadata[MISTRALAI_PLUGIN_KEY][CONNECTORS_KEY]
        assert len(connectors) == 2
        names = {c["connector_name"] for c in connectors}
        assert names == {"slack", "github"}

    def test_auto_auth_false_preserved(self) -> None:
        @workflow.define(name="test-auto-auth-false-before")
        @uses_connectors(github)
        class MyWorkflow:
            @workflow.entrypoint
            async def run(self) -> str:
                return "done"

        defn = get_workflow_definition(MyWorkflow)
        connectors = defn.plugin_metadata[MISTRALAI_PLUGIN_KEY][CONNECTORS_KEY]
        assert connectors[0]["auto_auth"] is False

    def test_credentials_name_preserved(self) -> None:
        @workflow.define(name="test-credentials-name-before")
        @uses_connectors(jira)
        class MyWorkflow:
            @workflow.entrypoint
            async def run(self) -> str:
                return "done"

        defn = get_workflow_definition(MyWorkflow)
        connectors = defn.plugin_metadata[MISTRALAI_PLUGIN_KEY][CONNECTORS_KEY]
        assert connectors[0]["credentials_name"] == "jira_service_account"

    def test_credentials_name_omitted_when_none(self) -> None:
        @workflow.define(name="test-credentials-name-none-before")
        @uses_connectors(slack)
        class MyWorkflow:
            @workflow.entrypoint
            async def run(self) -> str:
                return "done"

        defn = get_workflow_definition(MyWorkflow)
        connectors = defn.plugin_metadata[MISTRALAI_PLUGIN_KEY][CONNECTORS_KEY]
        assert "credentials_name" not in connectors[0]

    def test_metadata_present(self) -> None:
        @workflow.define(name="test-both-before")
        @uses_connectors(slack, github)
        class MyWorkflow:
            @workflow.entrypoint
            async def run(self) -> str:
                return "done"

        defn = get_workflow_definition(MyWorkflow)
        assert defn.plugin_metadata is not None
        connectors = defn.plugin_metadata[MISTRALAI_PLUGIN_KEY][CONNECTORS_KEY]
        assert len(connectors) == 2
        names = {c["connector_name"] for c in connectors}
        assert names == {"slack", "github"}


class TestUsesConnectorsAfterDefine:
    """@uses_connectors applied AFTER @workflow.define."""

    def test_plugin_metadata_attached(self) -> None:
        @uses_connectors(slack)
        @workflow.define(name="test-connectors-after-define")
        class MyWorkflow:
            @workflow.entrypoint
            async def run(self) -> str:
                return "done"

        defn = get_workflow_definition(MyWorkflow)
        assert defn.plugin_metadata is not None
        connectors = defn.plugin_metadata[MISTRALAI_PLUGIN_KEY][CONNECTORS_KEY]
        assert len(connectors) == 1
        assert connectors[0]["connector_name"] == "slack"

    def test_multiple_connectors(self) -> None:
        @uses_connectors(slack, github)
        @workflow.define(name="test-multi-connectors-after")
        class MyWorkflow:
            @workflow.entrypoint
            async def run(self) -> str:
                return "done"

        defn = get_workflow_definition(MyWorkflow)
        connectors = defn.plugin_metadata[MISTRALAI_PLUGIN_KEY][CONNECTORS_KEY]
        assert len(connectors) == 2

    def test_metadata_present(self) -> None:
        @uses_connectors(slack, github)
        @workflow.define(name="test-both-after")
        class MyWorkflow:
            @workflow.entrypoint
            async def run(self) -> str:
                return "done"

        defn = get_workflow_definition(MyWorkflow)
        assert defn.plugin_metadata is not None


class TestNoConnectors:
    def test_no_plugin_metadata(self) -> None:
        @workflow.define(name="test-no-connectors")
        class MyWorkflow:
            @workflow.entrypoint
            async def run(self) -> str:
                return "done"

        defn = get_workflow_definition(MyWorkflow)
        assert defn.plugin_metadata is None


class TestConnectorSlot:
    def test_call_returns_tool_call_client(self) -> None:
        slot = ConnectorSlot("github")
        client = slot()
        assert isinstance(client, ToolCallClient)
        assert client.connector_name == "github"

    def test_call_passes_credentials_name(self) -> None:
        slot = ConnectorSlot("jira", credentials_name="jira_sa")
        client = slot()
        assert client._credentials_name == "jira_sa"

    def test_to_metadata_basic(self) -> None:
        slot = ConnectorSlot("slack")
        assert slot.to_metadata() == {"connector_name": "slack", "auto_auth": True}

    def test_to_metadata_with_credentials_name(self) -> None:
        slot = ConnectorSlot("jira", credentials_name="jira_sa")
        assert slot.to_metadata()["credentials_name"] == "jira_sa"

    def test_to_metadata_with_allow_mcp_ui(self) -> None:
        slot = ConnectorSlot("slack", allow_mcp_ui=True)
        assert slot.to_metadata()["allow_mcp_ui"] is True

    def test_to_metadata_omits_credentials_when_none(self) -> None:
        assert "credentials_name" not in ConnectorSlot("slack").to_metadata()


class TestConnectorFactory:
    def test_returns_connector_slot(self) -> None:
        slot = connector("slack")
        assert isinstance(slot, ConnectorSlot)

    def test_passes_all_params(self) -> None:
        slot = connector(
            "jira",
            auto_auth=False,
            credentials_name="sa",
            allow_mcp_ui=True,
        )
        assert slot.auto_auth is False
        assert slot.credentials_name == "sa"
        assert slot.allow_mcp_ui is True
