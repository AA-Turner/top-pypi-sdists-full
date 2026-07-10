import unittest
from unittest.mock import MagicMock

from abstra_internals.repositories.editor_auth import (
    ProductionEditorAuthRepository,
    WebEditorAuthRepository,
)


def make_response(ok: bool = True, json_body=None, status_code: int = 200):
    response = MagicMock()
    response.ok = ok
    response.status_code = status_code
    response.json.return_value = json_body if json_body is not None else {}
    return response


class TestWebEditorAuthRepository(unittest.TestCase):
    def test_returns_renewed_token(self):
        client = MagicMock()
        client.post.return_value = make_response(json_body={"token": "new-token"})
        repository = WebEditorAuthRepository(client=client)

        self.assertEqual(repository.renew_token("old-token"), "new-token")
        client.post.assert_called_once_with(
            endpoint="/web-editor/renew-token",
            headers={"Web-Editor-Authorization": "Bearer old-token"},
        )

    def test_returns_none_on_error_response(self):
        client = MagicMock()
        client.post.return_value = make_response(ok=False, status_code=401)
        repository = WebEditorAuthRepository(client=client)

        self.assertIsNone(repository.renew_token("expired-token"))

    def test_returns_none_when_token_is_missing_from_response(self):
        client = MagicMock()
        client.post.return_value = make_response(json_body={})
        repository = WebEditorAuthRepository(client=client)

        self.assertIsNone(repository.renew_token("old-token"))

    def test_returns_none_on_exception(self):
        client = MagicMock()
        client.post.side_effect = Exception("network down")
        repository = WebEditorAuthRepository(client=client)

        self.assertIsNone(repository.renew_token("old-token"))


class TestProductionEditorAuthRepository(unittest.TestCase):
    def test_renew_token_is_a_noop(self):
        self.assertIsNone(ProductionEditorAuthRepository().renew_token("any-token"))


if __name__ == "__main__":
    unittest.main()
