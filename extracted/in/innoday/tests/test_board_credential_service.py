"""Tests for src.services.board_credential_service."""

import json
from unittest.mock import MagicMock, patch

import pytest

from src.domain.board import BoardType
from src.services.board_credential_service import (
    OAUTH_TOKEN_SENTINEL,
    get_board_credential_payload,
    legacy_token_to_payload,
    payload_to_legacy_token,
    set_board_credential,
)


class TestLegacyTokenToPayload:
    def test_jira_splits_email_and_api_token(self):
        payload = legacy_token_to_payload(
            BoardType.JIRA, "karl@example.com:ATATT123abc"
        )
        assert payload == {"email": "karl@example.com", "api_token": "ATATT123abc"}

    def test_jira_preserves_colons_inside_api_token(self):
        """maxsplit=1: only the first colon splits, so a colon-containing
        API token round-trips losslessly."""
        payload = legacy_token_to_payload(
            BoardType.JIRA, "karl@example.com:tok:en:parts"
        )
        assert payload == {"email": "karl@example.com", "api_token": "tok:en:parts"}

    def test_jira_raises_without_colon(self):
        with pytest.raises(ValueError, match="email:api_token"):
            legacy_token_to_payload(BoardType.JIRA, "no-colon-here")

    def test_trello_splits_api_key_and_token(self):
        payload = legacy_token_to_payload(BoardType.TRELLO, "key123:token456")
        assert payload == {"api_key": "key123", "token": "token456"}

    def test_trello_raises_without_colon(self):
        with pytest.raises(ValueError, match="api_key:token"):
            legacy_token_to_payload(BoardType.TRELLO, "no-colon-here")

    def test_linear_wraps_raw_token(self):
        payload = legacy_token_to_payload(BoardType.LINEAR, "lin_api_abc123")
        assert payload == {"token": "lin_api_abc123"}

    def test_notion_wraps_raw_token(self):
        payload = legacy_token_to_payload(BoardType.NOTION, "secret_abc123")
        assert payload == {"token": "secret_abc123"}


class TestPayloadToLegacyToken:
    def test_jira_reconstructs_colon_format(self):
        token = payload_to_legacy_token(
            BoardType.JIRA, {"email": "karl@example.com", "api_token": "abc"}
        )
        assert token == "karl@example.com:abc"

    def test_trello_reconstructs_colon_format(self):
        token = payload_to_legacy_token(
            BoardType.TRELLO, {"api_key": "key123", "token": "token456"}
        )
        assert token == "key123:token456"

    def test_linear_returns_raw_token(self):
        token = payload_to_legacy_token(BoardType.LINEAR, {"token": "lin_api_abc123"})
        assert token == "lin_api_abc123"

    def test_jira_oauth_payload_returns_sentinel_instead_of_keyerror(self):
        """An OAuth-credentialed Jira board's payload has no email/api_token
        to reconstruct -- must return OAUTH_TOKEN_SENTINEL, not KeyError,
        so callers (BoardSyncService._get_adapter) can route to the OAuth
        refresh path instead of crashing."""
        token = payload_to_legacy_token(
            BoardType.JIRA,
            {
                "auth_type": "oauth2",
                "access_token": "at",
                "refresh_token": "rt",
                "cloud_id": "cloud-1",
                "expires_at": "2026-01-01T00:00:00+00:00",
            },
        )
        assert token == OAUTH_TOKEN_SENTINEL
        # test_jira_reconstructs_colon_format above already covers that a
        # plain Basic Auth payload (no auth_type key) is unaffected by this
        # check -- not duplicating that assertion here.

    def test_jira_oauth_payload_missing_required_field_raises_keyerror(self):
        """A malformed/partially-written OAuth payload (e.g. auth_type set
        before the rest of the fields) must fail loudly and specifically
        HERE -- not silently return the sentinel and let some downstream
        reader (ensure_fresh_jira_token's own bare payload[...] lookups)
        raise a confusing, unhandled KeyError far from the point of
        detection."""
        with pytest.raises(KeyError, match="cloud_id"):
            payload_to_legacy_token(
                BoardType.JIRA,
                {
                    "auth_type": "oauth2",
                    "access_token": "at",
                    "refresh_token": "rt",
                    # cloud_id and expires_at missing
                },
            )


class TestRoundTrip:
    """Regression: JSON storage must not corrupt tokens with colons, quotes,
    or other special characters embedded in the secret portion."""

    @pytest.mark.parametrize(
        "board_type,original_token",
        [
            (BoardType.JIRA, "karl@example.com:ATATT3xFfGF0abc:def=ghi/jkl+mno"),
            (BoardType.JIRA, 'karl@example.com:token"with"quotes'),
            (BoardType.TRELLO, "a1b2c3:xyz:123:456"),
            (BoardType.LINEAR, "lin_api_YBsY2hzyuIm6aWzRYvzVu368v4cRMEAKcUDJpx2n"),
            (BoardType.NOTION, "secret_with:colon:chars"),
        ],
    )
    def test_legacy_to_payload_to_legacy_is_lossless(self, board_type, original_token):
        payload = legacy_token_to_payload(board_type, original_token)
        reconstructed = payload_to_legacy_token(board_type, payload)
        assert reconstructed == original_token

    @pytest.mark.parametrize(
        "board_type,original_token",
        [
            (BoardType.JIRA, "karl@example.com:token:with:colons"),
            (BoardType.TRELLO, "key:token/with+special=chars"),
            (BoardType.LINEAR, "lin_api_test"),
        ],
    )
    def test_payload_survives_json_serialization(self, board_type, original_token):
        payload = legacy_token_to_payload(board_type, original_token)
        serialized = json.dumps(payload)
        deserialized = json.loads(serialized)
        assert deserialized == payload
        assert payload_to_legacy_token(board_type, deserialized) == original_token


class TestJiraOAuthPayloadDiscriminator:
    """
    Jira credential payloads now come in two shapes, discriminated by
    `auth_type`: legacy Basic Auth ({"email", "api_token"}, auth_type
    absent or "basic") and OAuth 2.0 3LO ({"auth_type": "oauth2",
    "access_token", "refresh_token", "expires_at", "cloud_id", "site_url"}).
    legacy_token_to_payload/payload_to_legacy_token remain the Basic-Auth
    round-trip helpers; OAuth payloads are constructed/read directly as
    dicts elsewhere (jira_oauth_service.py) since they don't come from a
    colon-joined header token.
    """

    def test_basic_payload_has_no_auth_type_key_by_default(self):
        """Existing rows/behavior: legacy_token_to_payload doesn't stamp
        auth_type -- backward compat relies on treating an absent key as
        'basic' wherever payloads are consumed."""
        payload = legacy_token_to_payload(BoardType.JIRA, "a@b.com:tok123")
        assert "auth_type" not in payload

    def test_oauth2_payload_round_trips_through_json_unchanged(self):
        oauth_payload = {
            "auth_type": "oauth2",
            "access_token": "access-abc",
            "refresh_token": "refresh-xyz",
            "expires_at": "2026-07-10T12:00:00+00:00",
            "cloud_id": "cloud-123",
            "site_url": "https://example.atlassian.net",
        }
        serialized = json.dumps(oauth_payload)
        deserialized = json.loads(serialized)
        assert deserialized == oauth_payload

    def test_set_board_credential_persists_oauth2_payload_shape(self):
        session = MagicMock()

        set_board_credential(
            session,
            board_registration_id="board-1",
            organization_id="org-1",
            board_type=BoardType.JIRA,
            payload={
                "auth_type": "oauth2",
                "access_token": "access-abc",
                "refresh_token": "refresh-xyz",
                "expires_at": "2026-07-10T12:00:00+00:00",
                "cloud_id": "cloud-123",
                "site_url": "https://example.atlassian.net",
            },
        )

        params = session.exec.call_args.kwargs["params"]
        stored = json.loads(params["payload_json"])
        assert stored["auth_type"] == "oauth2"
        assert stored["access_token"] == "access-abc"
        assert stored["refresh_token"] == "refresh-xyz"
        assert stored["cloud_id"] == "cloud-123"

    def test_get_board_credential_payload_returns_oauth2_shape_intact(self):
        session = MagicMock()
        oauth_payload = {
            "auth_type": "oauth2",
            "access_token": "access-abc",
            "refresh_token": "refresh-xyz",
            "expires_at": "2026-07-10T12:00:00+00:00",
            "cloud_id": "cloud-123",
            "site_url": "https://example.atlassian.net",
        }
        session.exec.return_value.first.return_value = (json.dumps(oauth_payload),)

        result = get_board_credential_payload(session, "board-1")

        assert result == oauth_payload

    def test_payload_to_legacy_token_still_works_for_basic_jira_rows(self):
        """Existing Basic Auth rows predate auth_type entirely -- the
        legacy conversion path must keep working unmodified for them."""
        token = payload_to_legacy_token(
            BoardType.JIRA, {"email": "a@b.com", "api_token": "tok123"}
        )
        assert token == "a@b.com:tok123"


class TestGetBoardCredentialPayload:
    def test_returns_parsed_payload_when_found(self):
        session = MagicMock()
        session.exec.return_value.first.return_value = (
            json.dumps({"token": "lin_api_abc"}),
        )

        result = get_board_credential_payload(session, "board-1")

        assert result == {"token": "lin_api_abc"}

    def test_returns_none_when_no_credential_stored(self):
        session = MagicMock()
        session.exec.return_value.first.return_value = (None,)

        result = get_board_credential_payload(session, "board-1")

        assert result is None

    def test_returns_none_when_query_yields_no_row(self):
        session = MagicMock()
        session.exec.return_value.first.return_value = None

        result = get_board_credential_payload(session, "board-1")

        assert result is None

    def test_returns_none_and_logs_on_invalid_json(self):
        session = MagicMock()
        session.exec.return_value.first.return_value = ("not valid json {{{",)

        with patch("src.services.board_credential_service.logger") as mock_logger:
            result = get_board_credential_payload(session, "board-1")

        assert result is None
        mock_logger.error.assert_called_once()

    def test_passes_board_registration_id_as_param(self):
        session = MagicMock()
        session.exec.return_value.first.return_value = (None,)

        get_board_credential_payload(session, "board-xyz")

        call_kwargs = session.exec.call_args.kwargs
        assert call_kwargs["params"] == {"board_registration_id": "board-xyz"}


class TestSetBoardCredential:
    def test_calls_sql_function_with_serialized_payload(self):
        session = MagicMock()

        set_board_credential(
            session,
            board_registration_id="board-1",
            organization_id="org-1",
            board_type=BoardType.LINEAR,
            payload={"token": "lin_api_abc"},
        )

        call_kwargs = session.exec.call_args.kwargs
        params = call_kwargs["params"]
        assert params["board_registration_id"] == "board-1"
        assert params["organization_id"] == "org-1"
        assert params["board_type"] == "linear"
        assert json.loads(params["payload_json"]) == {"token": "lin_api_abc"}
        session.commit.assert_called_once()

    def test_accepts_plain_string_board_type(self):
        """board_type may be passed as a raw string (e.g. from a DB-loaded
        BoardRegistration.board_type that isn't strictly the enum)."""
        session = MagicMock()

        set_board_credential(
            session,
            board_registration_id="board-1",
            organization_id="org-1",
            board_type="jira",
            payload={"email": "a@b.com", "api_token": "x"},
        )

        params = session.exec.call_args.kwargs["params"]
        assert params["board_type"] == "jira"
