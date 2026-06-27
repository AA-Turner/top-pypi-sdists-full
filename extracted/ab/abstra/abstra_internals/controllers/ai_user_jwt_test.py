import unittest
from unittest.mock import MagicMock, patch

from abstra_internals.controllers.ai import AiController


class TestAiControllerUserJwt(unittest.TestCase):
    def setUp(self):
        self.mock_main_controller = MagicMock()
        self.mock_repos = MagicMock()
        self.mock_main_controller.repositories = self.mock_repos
        self.controller = AiController(self.mock_main_controller)

    @patch("abstra_internals.controllers.ai.resolve_headers")
    def test_get_history_without_jwt_does_not_add_header(self, mock_resolve):
        mock_resolve.return_value = {"Api-Authorization": "Bearer api-key"}
        self.controller.get_history(10, 0)
        call_args = self.mock_repos.ai.get_history.call_args
        headers_passed = call_args[0][0]
        self.assertNotIn("Web-Editor-Authorization", headers_passed)

    @patch("abstra_internals.controllers.ai.resolve_headers")
    def test_get_history_with_jwt_adds_header(self, mock_resolve):
        mock_resolve.return_value = {"Api-Authorization": "Bearer api-key"}
        self.controller.get_history(10, 0, user_jwt="my-jwt")
        call_args = self.mock_repos.ai.get_history.call_args
        headers_passed = call_args[0][0]
        self.assertIn("Web-Editor-Authorization", headers_passed)
        self.assertEqual(headers_passed["Web-Editor-Authorization"], "Bearer my-jwt")

    @patch("abstra_internals.controllers.ai.resolve_headers")
    def test_get_checkpoints_without_headers_returns_none(self, mock_resolve):
        mock_resolve.return_value = None

        result = self.controller.get_checkpoints("conv-1")

        self.assertIsNone(result)
        self.mock_repos.ai.get_checkpoints.assert_not_called()

    @patch("abstra_internals.controllers.ai.resolve_headers")
    def test_get_checkpoints_with_jwt_adds_header(self, mock_resolve):
        mock_resolve.return_value = {"Api-Authorization": "Bearer api-key"}

        self.controller.get_checkpoints("conv-1", user_jwt="my-jwt")

        call_args = self.mock_repos.ai.get_checkpoints.call_args
        headers_passed = call_args[0][0]
        self.assertEqual(headers_passed["Web-Editor-Authorization"], "Bearer my-jwt")

    @patch("abstra_internals.controllers.ai.resolve_headers")
    def test_rewind_conversation_with_jwt_adds_header(self, mock_resolve):
        mock_resolve.return_value = {"Api-Authorization": "Bearer api-key"}

        self.controller.rewind_conversation("conv-1", "user-msg-1", user_jwt="my-jwt")

        call_args = self.mock_repos.ai.rewind_conversation.call_args
        headers_passed = call_args[0][0]
        self.assertEqual(headers_passed["Web-Editor-Authorization"], "Bearer my-jwt")

    @patch("abstra_internals.controllers.ai.resolve_headers")
    def test_get_checkpoints_without_jwt_does_not_add_header(self, mock_resolve):
        mock_resolve.return_value = {"Api-Authorization": "Bearer api-key"}

        self.controller.get_checkpoints("conv-1")

        call_args = self.mock_repos.ai.get_checkpoints.call_args
        headers_passed = call_args[0][0]
        self.assertNotIn("Web-Editor-Authorization", headers_passed)

    @patch("abstra_internals.controllers.ai.resolve_headers")
    def test_rewind_conversation_without_jwt_does_not_add_header(self, mock_resolve):
        mock_resolve.return_value = {"Api-Authorization": "Bearer api-key"}

        self.controller.rewind_conversation("conv-1", "user-msg-1")

        call_args = self.mock_repos.ai.rewind_conversation.call_args
        headers_passed = call_args[0][0]
        self.assertNotIn("Web-Editor-Authorization", headers_passed)

    @patch("abstra_internals.controllers.ai.resolve_headers")
    def test_create_thread_with_jwt_adds_header(self, mock_resolve):
        mock_resolve.return_value = {"Api-Authorization": "Bearer api-key"}
        self.controller.create_thread(user_jwt="my-jwt")
        call_args = self.mock_repos.ai.create_thread.call_args
        headers_passed = call_args[0][0]
        self.assertIn("Web-Editor-Authorization", headers_passed)
        self.assertEqual(headers_passed["Web-Editor-Authorization"], "Bearer my-jwt")

    @patch("abstra_internals.controllers.ai.resolve_headers")
    def test_delete_thread_with_jwt_adds_header(self, mock_resolve):
        mock_resolve.return_value = {"Api-Authorization": "Bearer api-key"}
        self.controller.delete_thread("thread-1", user_jwt="my-jwt")
        call_args = self.mock_repos.ai.delete_thread.call_args
        headers_passed = call_args[0][0]
        self.assertIn("Web-Editor-Authorization", headers_passed)
        self.assertEqual(headers_passed["Web-Editor-Authorization"], "Bearer my-jwt")

    @patch("abstra_internals.controllers.ai.resolve_headers")
    def test_abort_thread_with_jwt_adds_header(self, mock_resolve):
        mock_resolve.return_value = {"Api-Authorization": "Bearer api-key"}
        self.controller.abort_thread("thread-1", user_jwt="my-jwt")
        call_args = self.mock_repos.ai.abort_thread.call_args
        headers_passed = call_args[0][0]
        self.assertIn("Web-Editor-Authorization", headers_passed)
        self.assertEqual(headers_passed["Web-Editor-Authorization"], "Bearer my-jwt")

    @patch("abstra_internals.controllers.ai.get_tunnel_secret_key", return_value="sk")
    @patch("abstra_internals.controllers.ai.get_session_path", return_value="/s")
    @patch(
        "abstra_internals.controllers.ai.get_local_package_version",
        return_value="0.0.0",
    )
    def test_send_ai_message_propagates_jwt_to_repository(self, *_):
        self.mock_repos.ai.get_ai_messages.return_value = iter([b"data"])
        self.mock_repos.linter.find_issues_in_codebase.return_value = []

        body = MagicMock()
        body.content = []
        body.conversation_id = "conv-1"
        body.context = {}
        body.human_approval = None
        body.tool_calls_approval = None
        body.browser_tools = None
        body.browser_tool_responses = None

        list(self.controller.send_ai_message(body, user_jwt="my-jwt"))

        call_kwargs = self.mock_repos.ai.get_ai_messages.call_args
        self.assertEqual(call_kwargs.kwargs.get("user_jwt"), "my-jwt")

    @patch("abstra_internals.controllers.ai.get_tunnel_secret_key")
    @patch("abstra_internals.controllers.ai.get_session_path")
    def test_start_conversation_propagates_jwt_to_repository(
        self, mock_session, mock_secret
    ):
        mock_secret.return_value = "secret"
        mock_session.return_value = "/session"
        self.mock_repos.ai.start_conversation.return_value = {"id": "conv1"}

        self.controller.start_conversation(user_jwt="my-jwt")

        call_kwargs = self.mock_repos.ai.start_conversation.call_args
        self.assertEqual(call_kwargs.kwargs.get("user_jwt"), "my-jwt")
