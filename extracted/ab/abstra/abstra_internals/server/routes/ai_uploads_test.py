import io
import unittest
from unittest.mock import MagicMock, patch

import flask

from abstra_internals.server.routes.ai import get_editor_bp


def _no_op(f):
    return f


class TestAiUploadRoutes(unittest.TestCase):
    def setUp(self):
        self.editor_usage_patcher = patch(
            "abstra_internals.server.routes.ai.editor_usage", _no_op
        )
        self.editor_usage_patcher.start()

        self.mock_main = MagicMock()
        self.mock_ai_controller = MagicMock()
        self.controller_patcher = patch(
            "abstra_internals.server.routes.ai.AiController",
            return_value=self.mock_ai_controller,
        )
        self.controller_patcher.start()

        bp = get_editor_bp(self.mock_main)
        self.app = flask.Flask(__name__)
        self.app.register_blueprint(bp, url_prefix="/ai")
        self.client = self.app.test_client()

    def tearDown(self):
        self.controller_patcher.stop()
        self.editor_usage_patcher.stop()

    def test_upload_route_calls_controller_with_file_and_conversation_id(self):
        self.mock_ai_controller.save_uploaded_file.return_value = {
            "filePath": ".abstra/ai_uploads/conv-1/foo.txt",
            "fileName": "foo.txt",
            "fileSize": 3,
            "mimeType": "text/plain",
        }

        response = self.client.post(
            "/ai/upload",
            data={
                "conversationId": "conv-1",
                "file": (io.BytesIO(b"hi!"), "foo.txt"),
            },
            content_type="multipart/form-data",
        )

        self.assertEqual(response.status_code, 200)
        body = response.get_json()
        assert body is not None
        self.assertEqual(body["filePath"], ".abstra/ai_uploads/conv-1/foo.txt")
        self.mock_ai_controller.save_uploaded_file.assert_called_once()
        args, _ = self.mock_ai_controller.save_uploaded_file.call_args
        self.assertEqual(args[1], "conv-1")
        self.assertEqual(args[0].filename, "foo.txt")

    def test_upload_route_413_when_content_length_over_cap(self):
        with patch("abstra_internals.server.routes.ai.MAX_AI_UPLOAD_SIZE", 8):
            response = self.client.post(
                "/ai/upload",
                data={
                    "conversationId": "conv-1",
                    "file": (io.BytesIO(b"large body"), "foo.txt"),
                },
                content_type="multipart/form-data",
            )
        self.assertEqual(response.status_code, 413)
        self.assertEqual(response.json, {"error": "File too large (max 300MB)"})
        self.mock_ai_controller.save_uploaded_file.assert_not_called()

    def test_upload_route_400_when_file_missing(self):
        response = self.client.post(
            "/ai/upload",
            data={"conversationId": "conv-1"},
            content_type="multipart/form-data",
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json, {"error": "file and conversationId are required"}
        )

    def test_upload_route_400_when_conversation_id_missing(self):
        response = self.client.post(
            "/ai/upload",
            data={"file": (io.BytesIO(b"hi!"), "foo.txt")},
            content_type="multipart/form-data",
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json, {"error": "file and conversationId are required"}
        )

    def test_upload_route_500_when_controller_raises(self):
        self.mock_ai_controller.save_uploaded_file.side_effect = OSError("disk full")
        response = self.client.post(
            "/ai/upload",
            data={
                "conversationId": "conv-1",
                "file": (io.BytesIO(b"hi!"), "foo.txt"),
            },
            content_type="multipart/form-data",
        )
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {"error": "Failed to save attachment"})

    def test_delete_route_calls_controller(self):
        self.mock_ai_controller.delete_uploaded_file.return_value = None
        response = self.client.delete(
            "/ai/upload",
            json={"filePath": ".abstra/ai_uploads/conv-1/foo.txt"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"success": True})
        self.mock_ai_controller.delete_uploaded_file.assert_called_once_with(
            ".abstra/ai_uploads/conv-1/foo.txt"
        )

    def test_delete_route_400_when_file_path_missing(self):
        response = self.client.delete("/ai/upload", json={})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json, {"error": "filePath is required"})

    def test_delete_route_400_when_controller_raises_invalid_path(self):
        from abstra_internals.controllers.ai import InvalidUploadPathError

        self.mock_ai_controller.delete_uploaded_file.side_effect = (
            InvalidUploadPathError()
        )
        response = self.client.delete("/ai/upload", json={"filePath": "../escape.txt"})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json, {"error": "Invalid path"})

    def test_delete_route_500_when_controller_raises_unexpected(self):
        self.mock_ai_controller.delete_uploaded_file.side_effect = OSError("nope")
        response = self.client.delete(
            "/ai/upload", json={"filePath": ".abstra/ai_uploads/conv-1/foo.txt"}
        )
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {"error": "Failed to delete attachment"})


if __name__ == "__main__":
    unittest.main()
