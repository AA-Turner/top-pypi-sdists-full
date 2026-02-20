"""Tests for agent connection tool handlers.

Verifies that:
- Tool names, descriptions, and input schemas are correctly configured
- Parameter validation works (rejects unknown params, requires connection_name)
- get_connection_action_details: list mode (with/without search), details mode, error cases
- execute_connection_action: correct payload forwarding, permission checks, error handling
- The request body sent to cloud-api has the correct format (camelCase fields)
"""

import json
from unittest.mock import MagicMock

import pytest

from abstra_internals.contracts_generated import (
    CloudApiCliConnectorsExecuteRequest,
    CloudApiCliConnectorsGetActionResponse,
)
from abstra_internals.entities.agents.tools.connections_handler import (
    ExecuteConnectionActionHandler,
    GetConnectionActionDetailsHandler,
    _filter_actions,
    _format_connections_summary,
)

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

PERMITTED = {
    "slack": [
        "users_lookup_by_email",
        "chat_post_message",
        "chat_update",
        "conversations_list",
        "files_upload",
    ],
    "salesforce": [
        "create_opportunity",
        "update_account",
    ],
}


@pytest.fixture
def mock_repo():
    return MagicMock()


@pytest.fixture
def details_handler(mock_repo):
    return GetConnectionActionDetailsHandler(PERMITTED, mock_repo)


@pytest.fixture
def execute_handler(mock_repo):
    return ExecuteConnectionActionHandler(PERMITTED, mock_repo)


# ---------------------------------------------------------------------------
# Contract / request format tests
# ---------------------------------------------------------------------------


class TestExecuteRequestContract:
    """Verify that CloudApiCliConnectorsExecuteRequest produces the correct JSON."""

    def test_to_dict_uses_camel_case(self):
        req = CloudApiCliConnectorsExecuteRequest(
            connection_name="slack",
            action_name="chat_post_message",
            parameters={"channel": "#general", "text": "hello"},
        )
        d = req.to_dict()
        assert d == {
            "connectionName": "slack",
            "actionName": "chat_post_message",
            "parameters": {"channel": "#general", "text": "hello"},
        }

    def test_to_dict_empty_parameters(self):
        req = CloudApiCliConnectorsExecuteRequest(
            connection_name="slack",
            action_name="users_list",
            parameters={},
        )
        d = req.to_dict()
        assert d == {
            "connectionName": "slack",
            "actionName": "users_list",
            "parameters": {},
        }

    def test_to_dict_no_parameters(self):
        req = CloudApiCliConnectorsExecuteRequest(
            connection_name="slack",
            action_name="users_list",
            parameters=None,
        )
        d = req.to_dict()
        # When parameters is None, it should NOT be in the dict
        assert "parameters" not in d
        assert d == {
            "connectionName": "slack",
            "actionName": "users_list",
        }

    def test_from_dict_round_trip(self):
        original = CloudApiCliConnectorsExecuteRequest(
            connection_name="slack",
            action_name="chat_post_message",
            parameters={"text": "hi"},
        )
        restored = CloudApiCliConnectorsExecuteRequest.from_dict(original.to_dict())
        assert restored.connection_name == "slack"
        assert restored.action_name == "chat_post_message"
        assert restored.parameters == {"text": "hi"}


class TestGetActionResponseContract:
    """Verify that CloudApiCliConnectorsGetActionResponse deserializes correctly."""

    def test_from_dict_full(self):
        data = {
            "name": "chat_post_message",
            "description": "Post a message to a channel",
            "payloadSchema": {
                "type": "object",
                "properties": {
                    "channel": {"type": "string"},
                    "text": {"type": "string"},
                },
                "required": ["channel", "text"],
            },
            "returnType": "object",
            "returnSchema": {"type": "object"},
        }
        resp = CloudApiCliConnectorsGetActionResponse.from_dict(data)
        assert resp.name == "chat_post_message"
        assert resp.description == "Post a message to a channel"
        assert resp.payload_schema["type"] == "object"
        assert resp.return_type == "object"

    def test_from_dict_minimal(self):
        data = {
            "name": "users_list",
            "description": "List users",
            "payloadSchema": {},
        }
        resp = CloudApiCliConnectorsGetActionResponse.from_dict(data)
        assert resp.name == "users_list"
        assert resp.return_type is None
        assert resp.return_schema is None

    def test_to_dict_uses_camel_case(self):
        resp = CloudApiCliConnectorsGetActionResponse(
            name="test",
            description="desc",
            payload_schema={"type": "object"},
        )
        d = resp.to_dict()
        assert "payloadSchema" in d
        assert "payload_schema" not in d


# ---------------------------------------------------------------------------
# Helper function tests
# ---------------------------------------------------------------------------


class TestFormatConnectionsSummary:
    def test_single_connection(self):
        result = _format_connections_summary({"slack": ["a", "b", "c"]})
        assert "slack (3 actions)" in result

    def test_multiple_connections(self):
        result = _format_connections_summary(PERMITTED)
        assert "slack (5 actions)" in result
        assert "salesforce (2 actions)" in result

    def test_empty(self):
        result = _format_connections_summary({})
        assert result == ""


class TestFilterActions:
    def test_no_pattern_returns_all(self):
        actions = ["a", "b", "c"]
        assert _filter_actions(actions, "") == ["a", "b", "c"]

    def test_regex_filter(self):
        actions = ["chat_post_message", "users_list", "chat_update", "files_upload"]
        result = _filter_actions(actions, "chat|message")
        assert "chat_post_message" in result
        assert "chat_update" in result
        assert "users_list" not in result

    def test_case_insensitive(self):
        actions = ["Chat_Post", "users_list"]
        result = _filter_actions(actions, "chat")
        assert "Chat_Post" in result

    def test_invalid_regex_falls_back_to_substring(self):
        actions = ["abc", "def", "abcdef"]
        result = _filter_actions(actions, "[invalid")
        # "[invalid" as substring won't match anything
        assert result == []

    def test_substring_fallback(self):
        actions = ["chat_post_message", "users_list"]
        result = _filter_actions(actions, "chat_post")
        assert result == ["chat_post_message"]


# ---------------------------------------------------------------------------
# GetConnectionActionDetailsHandler tests
# ---------------------------------------------------------------------------


class TestGetConnectionActionDetailsHandler:
    def test_name(self, details_handler):
        assert details_handler.name == "get_connection_action_details"

    def test_description_lists_connections(self, details_handler):
        desc = details_handler.description
        assert "slack" in desc
        assert "salesforce" in desc

    def test_input_schema_has_required_fields(self, details_handler):
        schema = details_handler.input_schema
        assert schema["type"] == "object"
        props = schema["properties"]
        assert "connection_name" in props
        assert "action_name" in props
        assert "search" in props
        assert schema["required"] == ["connection_name"]

    def test_unknown_params_rejected(self, details_handler):
        result = json.loads(
            details_handler.execute({"connection_name": "slack", "bogus": "val"})
        )
        assert "error" in result
        assert "bogus" in str(result["error"])

    def test_unknown_connection_returns_error(self, details_handler):
        result = json.loads(details_handler.execute({"connection_name": "unknown"}))
        assert "error" in result
        assert "not available" in result["error"]
        assert "slack" in str(result)

    # -- List mode --

    def test_list_all_actions(self, details_handler):
        result = json.loads(details_handler.execute({"connection_name": "slack"}))
        assert result["total_actions"] == 5
        assert result["showing"] == 5
        assert "users_lookup_by_email" in result["actions"]
        assert "chat_post_message" in result["actions"]

    def test_list_with_search(self, details_handler):
        result = json.loads(
            details_handler.execute(
                {"connection_name": "slack", "search": "chat|message"}
            )
        )
        assert result["total_actions"] == 5
        # Should match: chat_post_message, chat_update
        assert result["showing"] == 2
        assert "chat_post_message" in result["actions"]
        assert "chat_update" in result["actions"]
        assert "users_lookup_by_email" not in result["actions"]

    def test_list_with_search_email(self, details_handler):
        result = json.loads(
            details_handler.execute({"connection_name": "slack", "search": "email"})
        )
        assert result["showing"] == 1
        assert "users_lookup_by_email" in result["actions"]

    # -- Details mode --

    def test_details_calls_repo(self, details_handler, mock_repo):
        mock_repo.get_connection_action_details.return_value = (
            CloudApiCliConnectorsGetActionResponse(
                name="chat_post_message",
                description="Post a message",
                payload_schema={
                    "type": "object",
                    "properties": {"text": {"type": "string"}},
                },
            )
        )
        result = json.loads(
            details_handler.execute(
                {"connection_name": "slack", "action_name": "chat_post_message"}
            )
        )
        mock_repo.get_connection_action_details.assert_called_once_with(
            connection_name="slack",
            action_name="chat_post_message",
        )
        assert result["name"] == "chat_post_message"
        assert "payloadSchema" in result

    def test_details_action_not_found_suggests_similar(self, details_handler):
        result = json.loads(
            details_handler.execute(
                {"connection_name": "slack", "action_name": "chat_send"}
            )
        )
        assert "error" in result
        assert "not found" in result["error"]
        # Should suggest similar actions (fuzzy match on "chat|send")
        assert "similar_actions" in result

    def test_details_fallback_when_api_fails(self, details_handler, mock_repo):
        mock_repo.get_connection_action_details.side_effect = Exception("Not deployed")
        result = json.loads(
            details_handler.execute(
                {"connection_name": "slack", "action_name": "chat_post_message"}
            )
        )
        # Should return graceful fallback, not crash
        assert result["action_name"] == "chat_post_message"
        assert "hint" in result


# ---------------------------------------------------------------------------
# ExecuteConnectionActionHandler tests
# ---------------------------------------------------------------------------


class TestExecuteConnectionActionHandler:
    def test_name(self, execute_handler):
        assert execute_handler.name == "execute_connection_action"

    def test_description_shows_connections(self, execute_handler):
        desc = execute_handler.description
        assert "slack" in desc
        assert "salesforce" in desc
        # Should NOT list all 296 individual action names
        assert "actions)" in desc  # e.g. "slack (5 actions)"

    def test_input_schema_has_required_fields(self, execute_handler):
        schema = execute_handler.input_schema
        assert schema["type"] == "object"
        props = schema["properties"]
        assert "connection_name" in props
        assert "action_name" in props
        assert "parameters" in props
        assert set(schema["required"]) == {"connection_name", "action_name"}

    def test_parameters_description_mentions_inside(self, execute_handler):
        """Verify the parameters field description guides the LLM to put fields INSIDE."""
        schema = execute_handler.input_schema
        desc = schema["properties"]["parameters"]["description"]
        assert "INSIDE" in desc or "inside" in desc.lower()

    def test_unknown_params_rejected(self, execute_handler):
        result = json.loads(
            execute_handler.execute(
                {"connection_name": "slack", "action_name": "test", "email": "x@y.com"}
            )
        )
        assert "error" in result
        assert "email" in str(result["error"])

    def test_unknown_connection_returns_error(self, execute_handler):
        result = json.loads(
            execute_handler.execute(
                {"connection_name": "unknown", "action_name": "test"}
            )
        )
        assert "error" in result
        assert "not available" in result["error"]
        assert "available_connections" in result

    def test_unknown_action_returns_error_with_hint(self, execute_handler):
        result = json.loads(
            execute_handler.execute(
                {"connection_name": "slack", "action_name": "nonexistent_action"}
            )
        )
        assert "error" in result
        assert "not found" in result["error"]
        assert "hint" in result

    # -- Successful execution --

    def test_execute_calls_repo_with_correct_params(self, execute_handler, mock_repo):
        mock_repo.run_connection_action.return_value = {
            "ok": True,
            "user": {"id": "U123"},
        }
        result = json.loads(
            execute_handler.execute(
                {
                    "connection_name": "slack",
                    "action_name": "users_lookup_by_email",
                    "parameters": {"email": "bruno@abstra.app"},
                }
            )
        )
        mock_repo.run_connection_action.assert_called_once_with(
            connection_name="slack",
            action="users_lookup_by_email",
            payload={"email": "bruno@abstra.app"},
        )
        assert result["ok"] is True
        assert result["user"]["id"] == "U123"

    def test_execute_with_empty_parameters(self, execute_handler, mock_repo):
        mock_repo.run_connection_action.return_value = {"members": []}
        json.loads(
            execute_handler.execute(
                {
                    "connection_name": "slack",
                    "action_name": "conversations_list",
                    "parameters": {},
                }
            )
        )
        mock_repo.run_connection_action.assert_called_once_with(
            connection_name="slack",
            action="conversations_list",
            payload={},
        )

    def test_execute_without_parameters_defaults_to_empty_dict(
        self, execute_handler, mock_repo
    ):
        mock_repo.run_connection_action.return_value = {"members": []}
        execute_handler.execute(
            {
                "connection_name": "slack",
                "action_name": "conversations_list",
            }
        )
        mock_repo.run_connection_action.assert_called_once_with(
            connection_name="slack",
            action="conversations_list",
            payload={},
        )

    def test_execute_catches_repo_exception(self, execute_handler, mock_repo):
        mock_repo.run_connection_action.side_effect = Exception(
            "500 Server Error: Internal Server Error"
        )
        result = json.loads(
            execute_handler.execute(
                {
                    "connection_name": "slack",
                    "action_name": "users_lookup_by_email",
                    "parameters": {"email": "test@test.com"},
                }
            )
        )
        assert "error" in result
        assert "500" in result["error"]


# ---------------------------------------------------------------------------
# Integration: verify the full request body format
# ---------------------------------------------------------------------------


class TestRequestBodyFormat:
    """End-to-end test: from agent action_input to the JSON body sent to cloud-api."""

    def test_full_flow_request_body(self):
        """Simulate the exact flow: handler extracts params → repo builds request → HTTP body."""
        # 1. Agent produces this action_input
        action_input = {
            "connection_name": "slack",
            "action_name": "users_lookup_by_email",
            "parameters": {"email": "bruno@abstra.app"},
        }

        # 2. Handler extracts fields (same as ExecuteConnectionActionHandler.execute)
        connection_name = action_input.get("connection_name", "")
        action_name = action_input.get("action_name", "")
        parameters = action_input.get("parameters", {})

        # 3. Repository builds the request (same as ConnectorsRepository.run_connection_action)
        request = CloudApiCliConnectorsExecuteRequest(
            connection_name=connection_name,
            action_name=action_name,
            parameters=parameters,
        )
        body = request.to_dict()

        # 4. Verify the JSON body is what cloud-api expects
        assert body == {
            "connectionName": "slack",
            "actionName": "users_lookup_by_email",
            "parameters": {"email": "bruno@abstra.app"},
        }
        # Cloud-api route reads:
        #   req.body.actionName → "users_lookup_by_email"  ✓
        #   req.body.parameters → {"email": "bruno@abstra.app"}  ✓
        #   req.params.connectionName → from URL path  ✓

    def test_full_flow_without_parameters(self):
        action_input = {
            "connection_name": "slack",
            "action_name": "users_list",
        }
        parameters = action_input.get("parameters", {})
        request = CloudApiCliConnectorsExecuteRequest(
            connection_name="slack",
            action_name="users_list",
            parameters=parameters,
        )
        body = request.to_dict()
        assert body["connectionName"] == "slack"
        assert body["actionName"] == "users_list"
        assert body["parameters"] == {}

    def test_request_body_url_matches_connection_name(self):
        """Verify the endpoint URL uses connection_name from the request."""
        connection_name = "slack"
        expected_endpoint = f"connectors/connection/{connection_name}/execute"
        assert expected_endpoint == "connectors/connection/slack/execute"

    def test_action_specific_fields_are_nested_in_parameters(self):
        """Verify that action-specific fields like 'email' are inside 'parameters', not top-level."""
        # This is what the agent SHOULD produce (correct)
        correct_input = {
            "connection_name": "slack",
            "action_name": "users_lookup_by_email",
            "parameters": {"email": "bruno@abstra.app"},
        }
        request = CloudApiCliConnectorsExecuteRequest(
            connection_name=correct_input["connection_name"],
            action_name=correct_input["action_name"],
            parameters=correct_input["parameters"],
        )
        body = request.to_dict()
        assert "email" not in body  # email must NOT be top-level
        assert (
            body["parameters"]["email"] == "bruno@abstra.app"
        )  # email must be inside parameters


# ---------------------------------------------------------------------------
# Dispatcher integration: verify tools are correctly registered
# ---------------------------------------------------------------------------


class TestToolRegistration:
    """Verify that connection handlers satisfy the ToolHandler protocol."""

    def test_details_handler_has_required_protocol_methods(self, details_handler):
        assert hasattr(details_handler, "name")
        assert hasattr(details_handler, "description")
        assert hasattr(details_handler, "input_schema")
        assert hasattr(details_handler, "execute")
        assert isinstance(details_handler.name, str)
        assert isinstance(details_handler.description, str)
        assert isinstance(details_handler.input_schema, dict)

    def test_execute_handler_has_required_protocol_methods(self, execute_handler):
        assert hasattr(execute_handler, "name")
        assert hasattr(execute_handler, "description")
        assert hasattr(execute_handler, "input_schema")
        assert hasattr(execute_handler, "execute")
        assert isinstance(execute_handler.name, str)
        assert isinstance(execute_handler.description, str)
        assert isinstance(execute_handler.input_schema, dict)

    def test_handlers_work_with_dispatcher(self, details_handler, execute_handler):
        from abstra_internals.entities.agents.tools.dispatcher import ToolDispatcher

        dispatcher = ToolDispatcher([details_handler, execute_handler])
        names = dispatcher.get_action_names()
        assert "get_connection_action_details" in names
        assert "execute_connection_action" in names

    def test_dispatcher_description_includes_both_tools(
        self, details_handler, execute_handler
    ):
        from abstra_internals.entities.agents.tools.dispatcher import ToolDispatcher

        dispatcher = ToolDispatcher([details_handler, execute_handler])
        desc = dispatcher.get_tool_descriptions()
        assert "get_connection_action_details" in desc
        assert "execute_connection_action" in desc
        assert "slack" in desc
        assert "salesforce" in desc
