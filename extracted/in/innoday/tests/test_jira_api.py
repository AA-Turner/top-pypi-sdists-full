"""
Tests for JiraAPI and the shared ADF (Atlassian Document Format) helpers.

Three bugs fixed together here, all confirmed live against a real Jira Cloud
instance:
1. create_ticket sent a plain string for `description` -- Jira Cloud's v3
   API rejects this with 400 "not valid Atlassian Document Format (ADF)
   content". Fixed via plain_text_to_adf().
2. _map_issue_to_ticket passed the raw ADF dict straight into
   Ticket.description (a plain string column) -- crashed with
   psycopg2.ProgrammingError: can't adapt type 'dict'. Fixed via
   adf_to_plain_text().
3. Failed issue creation was silently swallowed (bare `return None`, no
   logging) -- fixed by logging the response status/body before returning.
"""

from unittest.mock import AsyncMock, MagicMock, patch

import httpx
import pytest

from src.api.jira_api import JiraAPI, adf_to_plain_text, plain_text_to_adf


def make_api():
    return JiraAPI(
        base_url="https://example.atlassian.net",
        email="me@example.com",
        api_token="token123",
    )


class TestPlainTextToAdf:
    def test_wraps_text_in_minimal_adf_document(self):
        result = plain_text_to_adf("Some description")
        assert result == {
            "type": "doc",
            "version": 1,
            "content": [
                {
                    "type": "paragraph",
                    "content": [{"type": "text", "text": "Some description"}],
                }
            ],
        }


class TestAdfToPlainText:
    def test_extracts_text_from_single_paragraph(self):
        adf = {
            "type": "doc",
            "version": 1,
            "content": [
                {"type": "paragraph", "content": [{"type": "text", "text": "Hello"}]}
            ],
        }
        assert adf_to_plain_text(adf) == "Hello"

    def test_joins_multiple_paragraphs_with_newline(self):
        adf = {
            "type": "doc",
            "version": 1,
            "content": [
                {"type": "paragraph", "content": [{"type": "text", "text": "Line 1"}]},
                {"type": "paragraph", "content": [{"type": "text", "text": "Line 2"}]},
            ],
        }
        assert adf_to_plain_text(adf) == "Line 1\nLine 2"

    def test_passes_through_plain_string_unchanged(self):
        assert adf_to_plain_text("already plain text") == "already plain text"

    def test_returns_empty_string_for_empty_input(self):
        assert adf_to_plain_text("") == ""
        assert adf_to_plain_text(None) == ""


@pytest.mark.asyncio
class TestCreateTicketAdfWrapping:
    async def test_description_is_wrapped_in_adf_before_posting(self):
        api = make_api()
        create_response = MagicMock(status_code=201)
        create_response.json.return_value = {"key": "TEST-1"}
        get_response = MagicMock(status_code=200)
        get_response.json.return_value = {
            "key": "TEST-1",
            "fields": {
                "summary": "A ticket",
                "status": {"name": "To Do"},
                "created": "2026-07-01T00:00:00.000+0000",
                "updated": "2026-07-01T00:00:00.000+0000",
            },
        }

        with (
            patch.object(
                httpx.AsyncClient, "post", new_callable=AsyncMock
            ) as mock_post,
            patch.object(httpx.AsyncClient, "get", new_callable=AsyncMock) as mock_get,
        ):
            mock_post.return_value = create_response
            mock_get.return_value = get_response

            await api.create_ticket(
                project_key="TEST", summary="A ticket", description="Plain description"
            )

            sent_json = mock_post.call_args.kwargs["json"]
            assert sent_json["fields"]["description"] == plain_text_to_adf(
                "Plain description"
            )

    async def test_creation_failure_logs_status_and_body_not_silently_none(self):
        api = make_api()
        error_response = MagicMock(status_code=400, text='{"errors":"bad request"}')

        with (
            patch.object(
                httpx.AsyncClient, "post", new_callable=AsyncMock
            ) as mock_post,
            patch("src.api.jira_api.logger") as mock_logger,
        ):
            mock_post.return_value = error_response

            result = await api.create_ticket(project_key="TEST", summary="A ticket")

            assert result is None
            mock_logger.error.assert_called_once()
            assert "400" in mock_logger.error.call_args[0][0]


@pytest.mark.asyncio
class TestMapIssueToTicketAdfDecoding:
    async def test_adf_description_is_decoded_to_plain_string(self):
        api = make_api()
        issue = {
            "key": "TEST-2",
            "fields": {
                "summary": "A ticket",
                "status": {"name": "To Do"},
                "created": "2026-07-01T00:00:00.000+0000",
                "updated": "2026-07-01T00:00:00.000+0000",
                "description": {
                    "type": "doc",
                    "version": 1,
                    "content": [
                        {
                            "type": "paragraph",
                            "content": [{"type": "text", "text": "From Jira"}],
                        }
                    ],
                },
            },
        }

        ticket = api._map_issue_to_ticket(issue)

        assert ticket.description == "From Jira"
        assert isinstance(ticket.description, str)


class TestJiraAPIOAuthMode:
    """
    JiraAPI must support a second construction path: access_token +
    cloud_id instead of email + api_token. In OAuth mode, base_url becomes
    https://api.atlassian.com/ex/jira/{cloud_id} and auth becomes a Bearer
    header instead of the (email, api_token) tuple passed to httpx's
    auth= kwarg. Basic Auth construction/behavior must be completely
    unaffected.
    """

    def test_oauth_mode_sets_bearer_header_and_cloud_id_base_url(self):
        api = JiraAPI(access_token="access-abc", cloud_id="cloud-123")

        assert api.base_url == "https://api.atlassian.com/ex/jira/cloud-123"
        assert api.headers["Authorization"] == "Bearer access-abc"
        assert api.auth is None

    def test_basic_auth_mode_unaffected_by_oauth_support(self):
        api = make_api()

        assert api.auth == ("me@example.com", "token123")
        assert "Authorization" not in api.headers
        assert api.base_url == "https://example.atlassian.net"

    def test_oauth_mode_requires_both_access_token_and_cloud_id(self):
        with pytest.raises(ValueError):
            JiraAPI(access_token="access-abc")

        with pytest.raises(ValueError):
            JiraAPI(cloud_id="cloud-123")

    @pytest.mark.asyncio
    async def test_oauth_mode_sends_bearer_auth_on_requests_not_basic_tuple(self):
        api = JiraAPI(access_token="access-abc", cloud_id="cloud-123")

        get_response = MagicMock(status_code=200)
        get_response.json.return_value = {"issues": [], "total": 0}

        with patch.object(httpx.AsyncClient, "get", new_callable=AsyncMock) as mock_get:
            mock_get.return_value = get_response
            await api.get_tickets_by_board("80")

        call_kwargs = mock_get.call_args.kwargs
        assert call_kwargs.get("auth") is None
        assert call_kwargs["headers"]["Authorization"] == "Bearer access-abc"
        called_url = mock_get.call_args.args[0]
        assert called_url.startswith("https://api.atlassian.com/ex/jira/cloud-123/")
