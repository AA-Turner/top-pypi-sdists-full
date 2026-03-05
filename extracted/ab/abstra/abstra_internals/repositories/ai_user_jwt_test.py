import unittest
from unittest.mock import MagicMock, patch

from abstra_internals.contracts_generated import CloudApiCliAiV2StreamRequest
from abstra_internals.repositories.ai import LocalAIRepository


class TestLocalAIRepositoryUserJwt(unittest.TestCase):
    def setUp(self):
        self.mock_client = MagicMock()
        self.repo = LocalAIRepository(self.mock_client)

    @patch("abstra_internals.repositories.ai.resolve_headers")
    def test_get_ai_messages_without_jwt_does_not_add_header(self, mock_resolve):
        mock_resolve.return_value = {"Api-Authorization": "Bearer api-key"}
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.iter_content.return_value = iter([b"data"])
        self.mock_client.post.return_value = mock_response

        req = MagicMock(spec=CloudApiCliAiV2StreamRequest)
        req.to_dict.return_value = {"conversation_id": "c1"}

        list(self.repo.get_ai_messages(req))

        call_kwargs = self.mock_client.post.call_args
        headers_sent = call_kwargs.kwargs.get("headers") or call_kwargs[1].get(
            "headers"
        )
        self.assertNotIn("Web-Editor-Authorization", headers_sent)

    @patch("abstra_internals.repositories.ai.resolve_headers")
    def test_get_ai_messages_with_jwt_adds_header(self, mock_resolve):
        mock_resolve.return_value = {"Api-Authorization": "Bearer api-key"}
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.iter_content.return_value = iter([b"data"])
        self.mock_client.post.return_value = mock_response

        req = MagicMock(spec=CloudApiCliAiV2StreamRequest)
        req.to_dict.return_value = {"conversation_id": "c1"}

        list(self.repo.get_ai_messages(req, user_jwt="my-jwt-token"))

        call_kwargs = self.mock_client.post.call_args
        headers_sent = call_kwargs.kwargs.get("headers") or call_kwargs[1].get(
            "headers"
        )
        self.assertIn("Web-Editor-Authorization", headers_sent)
        self.assertEqual(
            headers_sent["Web-Editor-Authorization"], "Bearer my-jwt-token"
        )

    def test_start_conversation_without_jwt_does_not_add_header(self):
        mock_response = MagicMock()
        mock_response.json.return_value = {"id": "conv1"}
        self.mock_client.post.return_value = mock_response

        self.repo.start_conversation(
            secret_key="secret", tunnel_session_path="/session"
        )

        call_kwargs = self.mock_client.post.call_args
        # Without user_jwt, headers should not contain Web-Editor-Authorization
        headers_sent = call_kwargs.kwargs.get("headers", {})
        self.assertNotIn("Web-Editor-Authorization", headers_sent)

    def test_start_conversation_with_jwt_adds_header(self):
        mock_response = MagicMock()
        mock_response.json.return_value = {"id": "conv1"}
        self.mock_client.post.return_value = mock_response

        self.repo.start_conversation(
            secret_key="secret",
            tunnel_session_path="/session",
            user_jwt="my-jwt-token",
        )

        call_kwargs = self.mock_client.post.call_args
        headers_sent = call_kwargs.kwargs.get("headers") or call_kwargs[1].get(
            "headers"
        )
        self.assertIn("Web-Editor-Authorization", headers_sent)
        self.assertEqual(
            headers_sent["Web-Editor-Authorization"], "Bearer my-jwt-token"
        )
