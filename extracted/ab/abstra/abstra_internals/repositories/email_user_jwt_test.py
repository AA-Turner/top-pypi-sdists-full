import unittest
from unittest.mock import MagicMock, patch

from abstra_internals.repositories.email import EmailParams, EmailRepository


class TestEmailRepositorySendWithUserJwt(unittest.TestCase):
    @patch("abstra_internals.repositories.email.resolve_headers")
    def test_adds_web_editor_authorization_header_when_user_jwt_provided(
        self, mock_resolve_headers
    ):
        mock_resolve_headers.return_value = {"Api-Authorization": "Bearer api-key"}
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_client.post.return_value = mock_response

        repo = EmailRepository(client=mock_client)
        params = EmailParams(
            kind="message",
            to=["test@example.com"],
            subject="Test",
            body="Hello",
            attachments=[],
            is_html=False,
        )

        repo.send(params, user_jwt="test-jwt-123")

        mock_client.post.assert_called_once()
        call_kwargs = mock_client.post.call_args.kwargs
        self.assertEqual(
            call_kwargs["headers"]["Web-Editor-Authorization"], "Bearer test-jwt-123"
        )
        self.assertEqual(call_kwargs["headers"]["Api-Authorization"], "Bearer api-key")

    @patch("abstra_internals.repositories.email.resolve_headers")
    def test_does_not_add_header_when_user_jwt_is_none(self, mock_resolve_headers):
        mock_resolve_headers.return_value = {"Api-Authorization": "Bearer api-key"}
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_client.post.return_value = mock_response

        repo = EmailRepository(client=mock_client)
        params = EmailParams(
            kind="message",
            to=["test@example.com"],
            subject="Test",
            body="Hello",
            attachments=[],
            is_html=False,
        )

        repo.send(params, user_jwt=None)

        mock_client.post.assert_called_once()
        call_kwargs = mock_client.post.call_args.kwargs
        self.assertNotIn("Web-Editor-Authorization", call_kwargs["headers"])
        self.assertEqual(call_kwargs["headers"]["Api-Authorization"], "Bearer api-key")

    @patch("abstra_internals.repositories.email.resolve_headers")
    def test_works_when_resolve_headers_returns_none(self, mock_resolve_headers):
        mock_resolve_headers.return_value = None
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_client.post.return_value = mock_response

        repo = EmailRepository(client=mock_client)
        params = EmailParams(
            kind="message",
            to=["test@example.com"],
            subject="Test",
            body="Hello",
            attachments=[],
            is_html=False,
        )

        repo.send(params, user_jwt="test-jwt-456")

        mock_client.post.assert_called_once()
        call_kwargs = mock_client.post.call_args.kwargs
        self.assertEqual(
            call_kwargs["headers"]["Web-Editor-Authorization"], "Bearer test-jwt-456"
        )


if __name__ == "__main__":
    unittest.main()
