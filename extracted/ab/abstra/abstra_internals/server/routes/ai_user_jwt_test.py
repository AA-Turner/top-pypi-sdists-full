import unittest
from unittest.mock import MagicMock, patch

import flask

from abstra_internals.server.routes.ai import get_editor_bp


class TestAiRoutesUserJwt(unittest.TestCase):
    def setUp(self):
        self.app = flask.Flask(__name__)
        self.mock_controller = MagicMock()
        bp = get_editor_bp(self.mock_controller)
        self.app.register_blueprint(bp, url_prefix="/ai")
        self.client = self.app.test_client()

    @patch("abstra_internals.server.routes.ai.editor_usage", lambda f: f)
    def _make_app(self):
        """Helper to create app without editor_usage decorator interference."""
        app = flask.Flask(__name__)
        mock_controller = MagicMock()
        bp = get_editor_bp(mock_controller)
        app.register_blueprint(bp, url_prefix="/ai")
        return app, mock_controller

    @patch("abstra_internals.server.routes.ai.editor_usage", lambda f: f)
    def test_stream_route_passes_jwt_from_cookie(self):
        app = flask.Flask(__name__)
        mock_main = MagicMock()
        mock_ai_controller = MagicMock()
        mock_ai_controller.send_ai_message.return_value = iter([b"data"])

        with patch(
            "abstra_internals.server.routes.ai.AiController",
            return_value=mock_ai_controller,
        ):
            bp = get_editor_bp(mock_main)
            app.register_blueprint(bp, url_prefix="/ai")

        client = app.test_client()
        client.set_cookie("editor_auth", "test-jwt-123")
        response = client.post(
            "/ai/stream",
            json={
                "conversationId": "c1",
                "content": [{"type": "text", "text": "hello"}],
                "context": {},
            },
        )

        self.assertEqual(response.status_code, 200)
        call_kwargs = mock_ai_controller.send_ai_message.call_args
        self.assertEqual(call_kwargs.kwargs.get("user_jwt"), "test-jwt-123")

    @patch("abstra_internals.server.routes.ai.editor_usage", lambda f: f)
    def test_stream_route_passes_none_without_cookie(self):
        app = flask.Flask(__name__)
        mock_main = MagicMock()
        mock_ai_controller = MagicMock()
        mock_ai_controller.send_ai_message.return_value = iter([b"data"])

        with patch(
            "abstra_internals.server.routes.ai.AiController",
            return_value=mock_ai_controller,
        ):
            bp = get_editor_bp(mock_main)
            app.register_blueprint(bp, url_prefix="/ai")

        client = app.test_client()
        response = client.post(
            "/ai/stream",
            json={
                "conversationId": "c1",
                "content": [{"type": "text", "text": "hello"}],
                "context": {},
            },
        )

        self.assertEqual(response.status_code, 200)
        call_kwargs = mock_ai_controller.send_ai_message.call_args
        self.assertIsNone(call_kwargs.kwargs.get("user_jwt"))

    @patch("abstra_internals.server.routes.ai.editor_usage", lambda f: f)
    def test_history_route_passes_jwt_from_cookie(self):
        app = flask.Flask(__name__)
        mock_main = MagicMock()
        mock_ai_controller = MagicMock()
        mock_ai_controller.get_history.return_value = []

        with patch(
            "abstra_internals.server.routes.ai.AiController",
            return_value=mock_ai_controller,
        ):
            bp = get_editor_bp(mock_main)
            app.register_blueprint(bp, url_prefix="/ai")

        client = app.test_client()
        client.set_cookie("editor_auth", "test-jwt-456")
        response = client.get("/ai/history")

        self.assertEqual(response.status_code, 200)
        call_kwargs = mock_ai_controller.get_history.call_args
        self.assertEqual(call_kwargs.kwargs.get("user_jwt"), "test-jwt-456")

    @patch("abstra_internals.server.routes.ai.editor_usage", lambda f: f)
    def test_checkpoints_route_passes_jwt_from_cookie(self):
        app = flask.Flask(__name__)
        mock_main = MagicMock()
        mock_ai_controller = MagicMock()
        mock_ai_controller.get_checkpoints.return_value = [{"userMessageId": "msg-1"}]

        with patch(
            "abstra_internals.server.routes.ai.AiController",
            return_value=mock_ai_controller,
        ):
            bp = get_editor_bp(mock_main)
            app.register_blueprint(bp, url_prefix="/ai")

        client = app.test_client()
        client.set_cookie("editor_auth", "test-jwt-checkpoints")
        response = client.get("/ai/checkpoints/conv-1")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.get_json(), {"checkpoints": [{"userMessageId": "msg-1"}]}
        )
        call_kwargs = mock_ai_controller.get_checkpoints.call_args
        self.assertEqual(call_kwargs.args[0], "conv-1")
        self.assertEqual(call_kwargs.kwargs.get("user_jwt"), "test-jwt-checkpoints")

    @patch("abstra_internals.server.routes.ai.editor_usage", lambda f: f)
    def test_rewind_route_passes_jwt_from_cookie(self):
        app = flask.Flask(__name__)
        mock_main = MagicMock()
        mock_ai_controller = MagicMock()
        mock_ai_controller.rewind_conversation.return_value = {"messages": []}

        with patch(
            "abstra_internals.server.routes.ai.AiController",
            return_value=mock_ai_controller,
        ):
            bp = get_editor_bp(mock_main)
            app.register_blueprint(bp, url_prefix="/ai")

        client = app.test_client()
        client.set_cookie("editor_auth", "test-jwt-rewind")
        response = client.post(
            "/ai/rewind",
            json={"conversationId": "conv-1", "userMessageId": "msg-1"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {"messages": []})
        call_kwargs = mock_ai_controller.rewind_conversation.call_args
        self.assertEqual(call_kwargs.args[:2], ("conv-1", "msg-1"))
        self.assertEqual(call_kwargs.kwargs.get("user_jwt"), "test-jwt-rewind")

    @patch("abstra_internals.server.routes.ai.editor_usage", lambda f: f)
    def test_rewind_route_returns_400_for_missing_ids(self):
        app = flask.Flask(__name__)
        mock_main = MagicMock()
        mock_ai_controller = MagicMock()

        with patch(
            "abstra_internals.server.routes.ai.AiController",
            return_value=mock_ai_controller,
        ):
            bp = get_editor_bp(mock_main)
            app.register_blueprint(bp, url_prefix="/ai")

        response = app.test_client().post(
            "/ai/rewind", json={"conversationId": "conv-1"}
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.get_json())
        mock_ai_controller.rewind_conversation.assert_not_called()

    @patch("abstra_internals.server.routes.ai.editor_usage", lambda f: f)
    def test_create_thread_passes_jwt_from_cookie(self):
        app = flask.Flask(__name__)
        mock_main = MagicMock()
        mock_ai_controller = MagicMock()
        mock_thread = MagicMock()
        mock_thread.to_dict.return_value = {"id": "t1"}
        mock_ai_controller.create_thread.return_value = mock_thread

        with patch(
            "abstra_internals.server.routes.ai.AiController",
            return_value=mock_ai_controller,
        ):
            bp = get_editor_bp(mock_main)
            app.register_blueprint(bp, url_prefix="/ai")

        client = app.test_client()
        client.set_cookie("editor_auth", "test-jwt-789")
        response = client.post("/ai/thread")

        self.assertEqual(response.status_code, 200)
        call_kwargs = mock_ai_controller.create_thread.call_args
        self.assertEqual(call_kwargs.kwargs.get("user_jwt"), "test-jwt-789")

    @patch("abstra_internals.server.routes.ai.editor_usage", lambda f: f)
    def test_delete_thread_passes_jwt_from_cookie(self):
        app = flask.Flask(__name__)
        mock_main = MagicMock()
        mock_ai_controller = MagicMock()

        with patch(
            "abstra_internals.server.routes.ai.AiController",
            return_value=mock_ai_controller,
        ):
            bp = get_editor_bp(mock_main)
            app.register_blueprint(bp, url_prefix="/ai")

        client = app.test_client()
        client.set_cookie("editor_auth", "test-jwt-del")
        response = client.delete("/ai/thread/some-thread-id")

        self.assertEqual(response.status_code, 200)
        call_kwargs = mock_ai_controller.delete_thread.call_args
        self.assertEqual(call_kwargs.kwargs.get("user_jwt"), "test-jwt-del")

    @patch("abstra_internals.server.routes.ai.editor_usage", lambda f: f)
    def test_abort_passes_jwt_from_cookie(self):
        app = flask.Flask(__name__)
        mock_main = MagicMock()
        mock_ai_controller = MagicMock()

        with patch(
            "abstra_internals.server.routes.ai.AiController",
            return_value=mock_ai_controller,
        ):
            bp = get_editor_bp(mock_main)
            app.register_blueprint(bp, url_prefix="/ai")

        client = app.test_client()
        client.set_cookie("editor_auth", "test-jwt-abort")
        response = client.post("/ai/abort", json={"langGraphThreadId": "t1"})

        self.assertEqual(response.status_code, 200)
        call_kwargs = mock_ai_controller.abort_thread.call_args
        self.assertEqual(call_kwargs.kwargs.get("user_jwt"), "test-jwt-abort")

    @patch("abstra_internals.server.routes.ai.editor_usage", lambda f: f)
    def test_start_conversation_passes_jwt_from_cookie(self):
        app = flask.Flask(__name__)
        mock_main = MagicMock()
        mock_ai_controller = MagicMock()
        mock_ai_controller.start_conversation.return_value = {"id": "conv1"}

        with patch(
            "abstra_internals.server.routes.ai.AiController",
            return_value=mock_ai_controller,
        ):
            bp = get_editor_bp(mock_main)
            app.register_blueprint(bp, url_prefix="/ai")

        client = app.test_client()
        client.set_cookie("editor_auth", "test-jwt-conv")
        response = client.post("/ai/start-conversation")

        self.assertEqual(response.status_code, 200)
        call_kwargs = mock_ai_controller.start_conversation.call_args
        self.assertEqual(call_kwargs.kwargs.get("user_jwt"), "test-jwt-conv")
