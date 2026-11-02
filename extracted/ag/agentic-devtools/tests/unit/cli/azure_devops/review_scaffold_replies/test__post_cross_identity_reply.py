"""Tests for _post_cross_identity_reply."""

from unittest.mock import MagicMock

from agentic_devtools.cli.azure_devops.review_scaffold_replies import _post_cross_identity_reply


class TestPostCrossIdentityReply:
    """Tests for cross-identity reply posting."""

    def test_posts_marked_content_and_returns_comment_id(self):
        requests_mock = MagicMock()
        response = MagicMock()
        response.raise_for_status = MagicMock()
        response.json.return_value = {"id": 42}
        requests_mock.post.return_value = response

        result = _post_cross_identity_reply(
            requests_mock, {"Authorization": "******"}, "https://api/threads", 10, "Hello"
        )

        assert result == 42
        assert requests_mock.post.call_args.kwargs["json"] == {
            "content": "<!-- agdt-review:v1 mode:cross-identity-update -->\n**[Cross-identity update]**\n\nHello",
            "commentType": "text",
        }
