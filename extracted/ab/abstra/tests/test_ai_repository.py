import json
import unittest
from unittest.mock import MagicMock

import requests

from abstra_internals.repositories.ai import ProductionAIRepository


def _make_response(
    payload, status_code: int = 200, content_type: str = "application/json"
) -> requests.Response:
    """Build a real requests.Response so .ok / .reason / .json() behave like prod."""
    response = requests.Response()
    response.status_code = status_code
    response.reason = (
        requests.status_codes._codes.get(status_code, ("",))[0]
        .replace("_", " ")
        .title()
        or "Unknown"
    )
    if isinstance(payload, (bytes, bytearray)):
        response._content = payload
    elif isinstance(payload, str):
        response._content = payload.encode("utf-8")
    else:
        response._content = json.dumps(payload).encode("utf-8")
    response.headers["Content-Type"] = content_type
    return response


class TestProductionAIRepositoryParseDocument(unittest.TestCase):
    def setUp(self):
        self.mock_client = MagicMock()
        self.repo = ProductionAIRepository(client=self.mock_client)

    def test_returns_parsed_payload_on_success(self):
        self.mock_client.post.return_value = _make_response({"foo": "bar"})

        result = self.repo.parse_document("invoice", b"<pdf>", "application/pdf")

        self.assertEqual(result, {"foo": "bar"})

    def test_includes_cloud_api_error_message_on_http_error(self):
        """
        Regression: the previous implementation called response.raise_for_status()
        which drops the response body, leaving the user with a generic
        "502 Server Error: Bad Gateway" instead of the actionable message
        cloud-api returns. parse_document should surface the body's error
        field in the exception so users can act on it without consulting
        the document_ai_log table.
        """
        self.mock_client.post.return_value = _make_response(
            {
                "error": "Failed to parse document via invoice: Invalid date format: 01 April - 30 April, 2026"
            },
            status_code=400,
        )

        with self.assertRaises(requests.HTTPError) as ctx:
            self.repo.parse_document("invoice", b"<pdf>", "application/pdf")

        self.assertIn(
            "Invalid date format: 01 April - 30 April, 2026", str(ctx.exception)
        )
        self.assertIn("400", str(ctx.exception))
        self.assertIsNotNone(ctx.exception.response)

    def test_falls_back_to_response_text_when_body_is_not_json(self):
        self.mock_client.post.return_value = _make_response(
            "<html>Bad Gateway</html>",
            status_code=502,
            content_type="text/html",
        )

        with self.assertRaises(requests.HTTPError) as ctx:
            self.repo.parse_document("invoice", b"<pdf>", "application/pdf")

        self.assertIn("502", str(ctx.exception))
        self.assertIn("Bad Gateway", str(ctx.exception))

    def test_falls_back_to_response_text_when_json_lacks_error_field(self):
        self.mock_client.post.return_value = _make_response(
            {"detail": "something else"},
            status_code=500,
        )

        with self.assertRaises(requests.HTTPError) as ctx:
            self.repo.parse_document("invoice", b"<pdf>", "application/pdf")

        self.assertIn("500", str(ctx.exception))
        self.assertIn("something else", str(ctx.exception))


if __name__ == "__main__":
    unittest.main()
