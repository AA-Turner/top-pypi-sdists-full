import unittest
from unittest.mock import MagicMock, patch

from abstra_internals.interface.sdk.messages import _get_user_jwt_from_context


class TestGetUserJwtFromContext(unittest.TestCase):
    def test_returns_user_jwt_from_context(self):
        mock_ctx = MagicMock()
        mock_ctx.user_jwt = "test-jwt-123"

        with patch(
            "abstra_internals.interface.sdk.messages.SDKContextStore"
        ) as mock_store:
            mock_store.get_by_thread.return_value = mock_ctx
            result = _get_user_jwt_from_context()

        self.assertEqual(result, "test-jwt-123")

    def test_returns_none_when_user_jwt_is_none(self):
        mock_ctx = MagicMock()
        mock_ctx.user_jwt = None

        with patch(
            "abstra_internals.interface.sdk.messages.SDKContextStore"
        ) as mock_store:
            mock_store.get_by_thread.return_value = mock_ctx
            result = _get_user_jwt_from_context()

        self.assertIsNone(result)

    def test_returns_none_on_exception(self):
        with patch(
            "abstra_internals.interface.sdk.messages.SDKContextStore"
        ) as mock_store:
            mock_store.get_by_thread.side_effect = Exception("No context")
            result = _get_user_jwt_from_context()

        self.assertIsNone(result)


class TestSendEmailPassesUserJwt(unittest.TestCase):
    @patch("abstra_internals.interface.sdk.messages._get_user_jwt_from_context")
    @patch("abstra_internals.interface.sdk.messages.SDKContextStore")
    @patch("abstra_internals.interface.sdk.messages.message_template")
    def test_passes_user_jwt_to_repository(
        self, mock_template, mock_store, mock_get_jwt
    ):
        mock_get_jwt.return_value = "test-jwt-456"
        mock_email_params = MagicMock()
        mock_template.generate_email.return_value = mock_email_params
        mock_ctx = MagicMock()
        mock_store.get_by_thread.return_value = mock_ctx

        from abstra_internals.interface.sdk.messages import send_email

        send_email("test@example.com", "Hello")

        mock_ctx.repositories.email.send.assert_called_once_with(
            mock_email_params, user_jwt="test-jwt-456"
        )

    @patch("abstra_internals.interface.sdk.messages._get_user_jwt_from_context")
    @patch("abstra_internals.interface.sdk.messages.SDKContextStore")
    @patch("abstra_internals.interface.sdk.messages.message_template")
    def test_passes_none_when_no_jwt(self, mock_template, mock_store, mock_get_jwt):
        mock_get_jwt.return_value = None
        mock_email_params = MagicMock()
        mock_template.generate_email.return_value = mock_email_params
        mock_ctx = MagicMock()
        mock_store.get_by_thread.return_value = mock_ctx

        from abstra_internals.interface.sdk.messages import send_email

        send_email("test@example.com", "Hello")

        mock_ctx.repositories.email.send.assert_called_once_with(
            mock_email_params, user_jwt=None
        )


if __name__ == "__main__":
    unittest.main()
