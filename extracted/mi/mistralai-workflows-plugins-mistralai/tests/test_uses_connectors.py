"""Tests for the @uses_connectors decorator and ConnectorSlot.

Verifies that connector metadata is correctly attached
to the workflow class regardless of decorator ordering.
"""

from __future__ import annotations

import pytest

from mistralai.workflows import get_workflow_definition, workflow
from mistralai.workflows.core._graph import _CONNECTORS_META_KEY, _MISTRALAI_PLUGIN_KEY
from mistralai.workflows.core.definition.workflow_definition import is_workflow_on_behalf_of
from mistralai.workflows.plugins.mistralai.connectors import (
    ConnectorError,
    connector,
    uses_connectors,
)
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

    def test_duplicate_connector_name_rejected(self) -> None:
        with pytest.raises(ConnectorError, match="duplicate connector_name"):

            @workflow.define(name="test-duplicate-connectors-before")
            @uses_connectors(connector("github"), connector("github", run_as="deployment"))
            class MyWorkflow:
                @workflow.entrypoint
                async def run(self) -> str:
                    return "done"


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
        assert client._run_as is None

    def test_call_passes_credentials_name(self) -> None:
        slot = ConnectorSlot("jira", credentials_name="jira_sa")
        client = slot()
        assert client._credentials_name == "jira_sa"

    def test_to_metadata_basic(self) -> None:
        slot = ConnectorSlot("slack")
        assert slot.to_metadata() == {
            "connector_name": "slack",
            "auto_auth": True,
            "run_as": "auto",
        }

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


class TestConnectorRunAs:
    def test_defaults_to_auto(self) -> None:
        slot = connector("slack")
        assert slot.run_as.value == "auto"

    def test_auto_run_as(self) -> None:
        slot = connector("slack", run_as="auto")
        assert slot.run_as.value == "auto"

    def test_deployment_run_as(self) -> None:
        slot = connector("slack", run_as="deployment")
        assert slot.run_as.value == "deployment"

    @pytest.mark.parametrize("run_as", ["auto", "deployment"])
    def test_to_metadata_emits_run_as(self, run_as: str) -> None:
        assert connector("slack", run_as=run_as).to_metadata()["run_as"] == run_as

    def test_call_forwards_run_as_to_client(self) -> None:
        client = connector("slack", run_as="deployment")()
        assert client._run_as.value == "deployment"

    def test_call_forwards_explicit_auto_run_as_to_client(self) -> None:
        client = connector("slack", run_as="auto")()
        assert client._run_as.value == "auto"

    def test_invalid_run_as_raises(self) -> None:
        with pytest.raises(ValueError):
            connector("slack", run_as="nope")  # type: ignore[arg-type]

    def test_deployment_run_as_with_credentials_name_allowed(self) -> None:
        slot = connector("slack", run_as="deployment", credentials_name="my-token")
        assert slot.run_as.value == "deployment"
        assert slot.credentials_name == "my-token"

    def test_auto_run_as_with_credentials_name_allowed(self) -> None:
        slot = connector("slack", run_as="auto", credentials_name="my-token")
        assert slot.credentials_name == "my-token"


class TestRunAsDoesNotAffectOnBehalfOf:
    def test_auto_run_as_does_not_enable_obo(self) -> None:
        @workflow.define(name="test-obo-auto")
        @uses_connectors(connector("github", run_as="auto"))
        class MyWorkflow:
            @workflow.entrypoint
            async def run(self) -> str:
                return "done"

        assert get_workflow_definition(MyWorkflow).on_behalf_of is False
        assert is_workflow_on_behalf_of("test-obo-auto") is False

    def test_default_run_as_does_not_enable_obo(self) -> None:
        @workflow.define(name="test-obo-default")
        @uses_connectors(connector("github"))
        class MyWorkflow:
            @workflow.entrypoint
            async def run(self) -> str:
                return "done"

        assert get_workflow_definition(MyWorkflow).on_behalf_of is False

    def test_deployment_run_as_does_not_enable_obo(self) -> None:
        @workflow.define(name="test-obo-deployment")
        @uses_connectors(connector("slack", run_as="deployment"))
        class MyWorkflow:
            @workflow.entrypoint
            async def run(self) -> str:
                return "done"

        assert get_workflow_definition(MyWorkflow).on_behalf_of is False
        assert is_workflow_on_behalf_of("test-obo-deployment") is False

    def test_explicit_obo_preserved_with_auto(self) -> None:
        @workflow.define(name="test-obo-explicit", on_behalf_of=True)
        @uses_connectors(connector("github", run_as="auto"))
        class MyWorkflow:
            @workflow.entrypoint
            async def run(self) -> str:
                return "done"

        assert get_workflow_definition(MyWorkflow).on_behalf_of is True


class TestConnectorConstantsInSync:
    """`mistralai.workflows.core._graph` duck-types the plugin metadata keys instead of
    importing the plugin; these assertions fail loudly if either side drifts."""

    def test_plugin_key_matches_core(self) -> None:
        assert _MISTRALAI_PLUGIN_KEY == MISTRALAI_PLUGIN_KEY

    def test_connectors_key_matches_core(self) -> None:
        assert _CONNECTORS_META_KEY == CONNECTORS_KEY
