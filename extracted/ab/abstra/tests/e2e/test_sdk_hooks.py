import json
from io import BytesIO
from uuid import uuid4

from tests.fixtures import BaseTest

code_headers = """
import abstra.hooks as ah

body, query, headers = ah.get_request()

ah.send_response(headers["authorization"])
"""

code_multipart = """
import json
import abstra.hooks as ah

body, query, headers = ah.get_request()

ah.send_response(json.dumps(body))
"""

code_multipart_raw = """
import abstra.hooks as ah

body, query, headers = ah.get_raw_request()

ah.send_response(body)
"""


class TestHooksSDK(BaseTest):
    def setUp(self) -> None:
        super().setUp()
        self.hook = self.controller.create_hook("New hook", "hook.py")
        self.client = self.get_editor_flask_client()

    def test_insensitive_headers(self):
        random = uuid4().hex

        self.hook.file_path.write_text(code_headers)
        response = self.client.post(
            f"/_hooks/{self.hook.path}", headers={"Authorization": random}
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_data(as_text=True), random)

    def test_multipart_text_fields(self):
        self.hook.file_path.write_text(code_multipart)
        response = self.client.post(
            f"/_hooks/{self.hook.path}",
            data={"name": "alice", "age": "30"},
            content_type="multipart/form-data",
        )

        self.assertEqual(response.status_code, 200)
        parts = json.loads(response.get_data(as_text=True))
        by_name = {p["name"]: p["value"] for p in parts}
        self.assertEqual(by_name["name"], "alice")
        self.assertEqual(by_name["age"], "30")

    def test_multipart_with_file(self):
        self.hook.file_path.write_text(code_multipart)
        file_content = b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR"  # binary data
        response = self.client.post(
            f"/_hooks/{self.hook.path}",
            data={
                "title": "my upload",
                "file": (BytesIO(file_content), "image.png", "image/png"),
            },
            content_type="multipart/form-data",
        )

        self.assertEqual(response.status_code, 200)
        parts = json.loads(response.get_data(as_text=True))
        self.assertEqual(len(parts), 2)

        title_part = next(part for part in parts if part["name"] == "title")
        file_part = next(part for part in parts if part["name"] == "file")

        # text field
        self.assertEqual(title_part["value"], "my upload")
        # file field
        self.assertEqual(file_part["filename"], "image.png")
        self.assertEqual(file_part["content_type"], "image/png")
        self.assertIn("content", file_part)

        import base64

        decoded = base64.b64decode(file_part["content"])
        self.assertEqual(decoded, file_content)

    def test_multipart_raw_request(self):
        self.hook.file_path.write_text(code_multipart_raw)
        response = self.client.post(
            f"/_hooks/{self.hook.path}",
            data={"key": "value"},
            content_type="multipart/form-data",
        )

        self.assertEqual(response.status_code, 200)
        raw_body = response.get_data(as_text=True)
        self.assertIn("Content-Disposition", raw_body)
        self.assertIn("key", raw_body)
