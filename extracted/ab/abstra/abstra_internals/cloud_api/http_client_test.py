import unittest
from unittest.mock import MagicMock, patch

from abstra_internals.cloud_api.http_client import HTTPClient


def _client(*status_codes: int, **kwargs):
    """A client whose session answers with the given statuses, in order (the last
    one repeats), so a retry can be observed. Returns the session mock too, since
    the assertions are about how many requests actually went out."""
    client = HTTPClient(base_url="https://cloud-api.test/cli", **kwargs)
    responses = [MagicMock(status_code=code) for code in status_codes]
    session = MagicMock()
    session.request.side_effect = lambda *args, **kwargs: (
        responses.pop(0) if len(responses) > 1 else responses[0]
    )
    client._local.session = session
    return client, session


class TestHTTPClientUnauthorizedHook(unittest.TestCase):
    def test_calls_the_hook_with_the_credential_the_request_used(self):
        # The hook cannot read the current credential itself: concurrent requests
        # overlap, so it needs to know what this one actually presented.
        on_unauthorized = MagicMock(return_value=False)
        client, session = _client(
            401,
            base_headers_resolver=lambda: {"Api-Authorization": "Bearer sent"},
            on_unauthorized=on_unauthorized,
        )

        response = client.get("/api-keys/info")

        on_unauthorized.assert_called_once_with("Bearer sent")
        self.assertEqual(response.status_code, 401)

    def test_does_not_call_the_hook_on_other_statuses(self):
        for status_code in (200, 403, 404, 500):
            with self.subTest(status_code=status_code):
                on_unauthorized = MagicMock(return_value=False)
                client, session = _client(status_code, on_unauthorized=on_unauthorized)

                client.get("/api-keys/info")

                on_unauthorized.assert_not_called()

    def test_a_failing_hook_never_reaches_the_caller(self):
        on_unauthorized = MagicMock(side_effect=Exception("boom"))
        client, session = _client(401, on_unauthorized=on_unauthorized)

        with patch("abstra_internals.cloud_api.http_client.AbstraLogger") as logger:
            response = client.get("/api-keys/info")

        self.assertEqual(response.status_code, 401)
        logger.capture_exception.assert_called_once()

    def test_works_without_a_hook(self):
        client, session = _client(401)

        self.assertEqual(client.get("/api-keys/info").status_code, 401)


class TestHTTPClientRetryAfterRecovery(unittest.TestCase):
    def test_replays_the_request_once_when_credentials_were_replaced(self):
        client, session = _client(
            401, 200, on_unauthorized=MagicMock(return_value=True)
        )

        response = client.post("/ai-v2/stream", json={"a": 1})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(session.request.call_count, 2)
        # Same method, same URL, same body: a 401 means cloud-api rejected the
        # caller before doing any work, so the replay is the original request.
        first, second = session.request.call_args_list
        self.assertEqual(first.args, second.args)
        self.assertEqual(first.kwargs["json"], second.kwargs["json"])

    def test_does_not_replay_when_nothing_was_replaced(self):
        client, session = _client(
            401, 200, on_unauthorized=MagicMock(return_value=False)
        )

        response = client.post("/ai-v2/stream", json={"a": 1})

        self.assertEqual(response.status_code, 401)
        self.assertEqual(session.request.call_count, 1)

    def test_replay_overwrites_a_credential_the_caller_pinned(self):
        # Callers that resolve the credential themselves (the AI routes do) pass
        # the dead token in their own headers, and those win the merge — so the
        # replay has to overwrite it or it presents the same rejected token.
        tokens = iter(["Bearer dead", "Bearer live"])
        client, session = _client(
            401,
            200,
            base_headers_resolver=lambda: {"Api-Authorization": next(tokens)},
            on_unauthorized=MagicMock(return_value=True),
        )

        client.post(
            "/ai-v2/stream",
            headers={
                "Api-Authorization": "Bearer dead",
                "Web-Editor-Authorization": "Bearer session",
            },
        )

        first, second = session.request.call_args_list
        self.assertEqual(first.kwargs["headers"]["Api-Authorization"], "Bearer dead")
        self.assertEqual(second.kwargs["headers"]["Api-Authorization"], "Bearer live")
        # Everything else the caller sent survives the replay.
        self.assertEqual(
            second.kwargs["headers"]["Web-Editor-Authorization"], "Bearer session"
        )

    def test_a_replay_that_401s_again_is_not_replayed_forever(self):
        on_unauthorized = MagicMock(return_value=True)
        client, session = _client(401, on_unauthorized=on_unauthorized)

        response = client.get("/api-keys/info")

        self.assertEqual(response.status_code, 401)
        self.assertEqual(session.request.call_count, 2)
        on_unauthorized.assert_called_once()


if __name__ == "__main__":
    unittest.main()
