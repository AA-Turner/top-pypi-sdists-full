"""Tests for DealCloudRelationshipIntelligence class."""

from datetime import datetime
from unittest.mock import MagicMock, patch

from dealcloud_sdk.relationshipintelligence.dealcloud_ri import (
    RI_MAILBOX_STATUS_ERROR,
    DealCloudRelationshipIntelligence,
    ri_mailbox_response_failed,
    ri_mailbox_responses_all_succeeded,
)

# Relationship Intelligence API requires ri_import scope (https://api.docs.dealcloud.com/docs/token).
RI_IMPORT_SCOPE = ("data", "user_management", "ri_import")


class TestDealCloudRIInit:
    """Tests for initialization."""

    @patch("dealcloud_sdk.base.dealcloud_base.RestClient")
    def test_init_sets_ri_url(self, mock_client_class):
        """Test that init sets RI URL."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client_class.return_value = mock_client

        ri = DealCloudRelationshipIntelligence(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
            scope=RI_IMPORT_SCOPE,
        )

        assert ri._ri_url == "https://test.dealcloud.com/api/rest/v4/ri/import"
        assert "ri_import" in ri._scope


class TestEmailImport:
    """Tests for email import (Swagger: RiEmailMailboxVm / RiEmailVm)."""

    @patch("dealcloud_sdk.base.dealcloud_base.RestClient")
    def test_import_emails(self, mock_client_class):
        """Test import_emails sends array of RiEmailMailboxVm."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.post.return_value = [{"userId": 1, "status": 1}]
        mock_client_class.return_value = mock_client

        ri = DealCloudRelationshipIntelligence(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
            scope=RI_IMPORT_SCOPE,
        )

        mailboxes = [
            {
                "userId": 100,
                "handlerType": 1,
                "emails": [
                    {
                        "uniqueId": "m1",
                        "sentDate": "2024-01-15T10:30:00Z",
                        "sender": {"address": "sender@gmail.co"},
                        "recipientsTo": [{"address": "recipient@gmail.co"}],
                    }
                ],
            }
        ]
        result = ri.import_emails(mailboxes)

        assert result == [{"userId": 1, "status": 1}]
        sent = mock_client.post.call_args[1]["json"]
        assert len(sent) == 1
        assert sent[0]["userId"] == 100
        assert sent[0]["handlerType"] == 1
        assert sent[0]["emails"][0]["uniqueId"] == "m1"
        assert sent[0]["emails"][0]["sender"]["address"] == "sender@gmail.co"

    @patch("dealcloud_sdk.base.dealcloud_base.RestClient")
    def test_import_email(self, mock_client_class):
        """Test import_email convenience builds one RiEmailMailboxVm with one RiEmailVm."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.post.return_value = [{"userId": 1, "status": 1}]
        mock_client_class.return_value = mock_client

        ri = DealCloudRelationshipIntelligence(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
            scope=RI_IMPORT_SCOPE,
        )

        result = ri.import_email(
            user_id=100,
            handler_type=2,
            unique_id="m1",
            sent_date=datetime(2024, 1, 15, 10, 30),
            sender_address="sender@gmail.co",
            recipients_to=["recipient@gmail.co"],
        )

        assert result == [{"userId": 1, "status": 1}]
        payload = mock_client.post.call_args[1]["json"]
        assert len(payload) == 1
        mb = payload[0]
        assert mb["userId"] == 100
        assert mb["handlerType"] == 2
        assert len(mb["emails"]) == 1
        em = mb["emails"][0]
        assert em["uniqueId"] == "m1"
        assert em["sender"]["address"] == "sender@gmail.co"
        assert em["recipientsTo"][0]["address"] == "recipient@gmail.co"

    @patch("dealcloud_sdk.base.dealcloud_base.RestClient")
    def test_import_email_with_optional_fields(self, mock_client_class):
        """Test import_email with sender_name, recipients_cc, modified_date."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {}
        mock_client_class.return_value = mock_client

        ri = DealCloudRelationshipIntelligence(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
            scope=RI_IMPORT_SCOPE,
        )

        ri.import_email(
            user_id=100,
            handler_type=1,
            unique_id="m1",
            sent_date=datetime(2024, 1, 15),
            sender_address="sender@gmail.co",
            recipients_to=["to@gmail.co"],
            sender_name="Sender",
            recipients_cc=["cc@gmail.co"],
            modified_date=datetime(2024, 1, 15, 12, 0),
        )

        payload = mock_client.post.call_args[1]["json"]
        em = payload[0]["emails"][0]
        assert em["sender"]["name"] == "Sender"
        assert em["recipientsCc"][0]["address"] == "cc@gmail.co"
        assert "modifiedDate" in em


class TestMeetingImport:
    """Tests for meeting import (Swagger: RiMeetingMailboxVm / RiMeetingVm)."""

    @patch("dealcloud_sdk.base.dealcloud_base.RestClient")
    def test_import_meetings(self, mock_client_class):
        """Test import_meetings sends array of RiMeetingMailboxVm."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.post.return_value = [{"userId": 1, "status": 1}]
        mock_client_class.return_value = mock_client

        ri = DealCloudRelationshipIntelligence(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
            scope=RI_IMPORT_SCOPE,
        )

        mailboxes = [
            {
                "userId": 100,
                "meetings": [
                    {
                        "uniqueId": "mtg1",
                        "startDate": "2024-01-15T14:00:00Z",
                        "organizer": {"address": "organizer@gmail.co"},
                        "requiredAttendees": [{"address": "attendee@gmail.co", "isAccepted": True}],
                    }
                ],
            }
        ]
        result = ri.import_meetings(mailboxes)

        assert result == [{"userId": 1, "status": 1}]
        sent = mock_client.post.call_args[1]["json"]
        assert sent[0]["userId"] == 100
        assert sent[0]["meetings"][0]["uniqueId"] == "mtg1"
        assert sent[0]["meetings"][0]["organizer"]["address"] == "organizer@gmail.co"

    @patch("dealcloud_sdk.base.dealcloud_base.RestClient")
    def test_import_meeting(self, mock_client_class):
        """Test import_meeting convenience builds one RiMeetingMailboxVm with one RiMeetingVm."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.post.return_value = [{"userId": 1, "status": 1}]
        mock_client_class.return_value = mock_client

        ri = DealCloudRelationshipIntelligence(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
            scope=RI_IMPORT_SCOPE,
        )

        result = ri.import_meeting(
            user_id=100,
            unique_id="mtg1",
            start_date=datetime(2024, 1, 15, 14, 0),
            organizer_address="organizer@gmail.co",
            required_attendees=["attendee@gmail.co"],
        )

        assert result == [{"userId": 1, "status": 1}]
        payload = mock_client.post.call_args[1]["json"]
        assert payload[0]["userId"] == 100
        mt = payload[0]["meetings"][0]
        assert mt["uniqueId"] == "mtg1"
        assert mt["organizer"]["address"] == "organizer@gmail.co"
        assert mt["requiredAttendees"][0]["address"] == "attendee@gmail.co"
        assert mt["requiredAttendees"][0]["isAccepted"] is True

    @patch("dealcloud_sdk.base.dealcloud_base.RestClient")
    def test_import_meeting_with_optional_attendees(self, mock_client_class):
        """Test import_meeting with organizer_name and optional_attendees."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {}
        mock_client_class.return_value = mock_client

        ri = DealCloudRelationshipIntelligence(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
            scope=RI_IMPORT_SCOPE,
        )

        ri.import_meeting(
            user_id=100,
            unique_id="mtg1",
            start_date=datetime(2024, 1, 15, 14, 0),
            organizer_address="org@gmail.co",
            required_attendees=["req@gmail.co"],
            organizer_name="Organizer",
            optional_attendees=["opt@gmail.co"],
        )

        payload = mock_client.post.call_args[1]["json"]
        mt = payload[0]["meetings"][0]
        assert mt["organizer"]["name"] == "Organizer"
        assert mt["optionalAttendees"][0]["address"] == "opt@gmail.co"


class TestProcessingStatus:
    """Tests for processing status (Swagger: array of RiMailboxStatusVm)."""

    @patch("dealcloud_sdk.base.dealcloud_base.RestClient")
    def test_get_processing_status(self, mock_client_class):
        """Test get_processing_status returns list of RiMailboxStatusVm."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.get.return_value = [
            {
                "userId": 1,
                "emailAddress": "u1@example.com",
                "lastEmailSyncDate": None,
                "lastMeetingSyncDate": None,
            },
        ]
        mock_client_class.return_value = mock_client

        ri = DealCloudRelationshipIntelligence(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
            scope=RI_IMPORT_SCOPE,
        )

        result = ri.get_processing_status()
        assert len(result) == 1
        assert result[0]["userId"] == 1
        assert result[0]["emailAddress"] == "u1@example.com"

    @patch("dealcloud_sdk.base.dealcloud_base.RestClient")
    def test_get_processing_status_with_user_ids(self, mock_client_class):
        """Test get_processing_status with user_ids query param."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {}
        mock_client.get.return_value = []
        mock_client_class.return_value = mock_client

        ri = DealCloudRelationshipIntelligence(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
            scope=RI_IMPORT_SCOPE,
        )
        ri.get_processing_status(user_ids=[1, 2])
        call_url = mock_client.get.call_args[0][0]
        assert "userIds=1,2" in call_url


class TestSettings:
    """Tests for RI settings."""

    @patch("dealcloud_sdk.base.dealcloud_base.RestClient")
    def test_get_settings(self, mock_client_class):
        """Test get_settings."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.get.return_value = {
            "historicalPeriodInMonths": 12,
            "syncLevel": 1,
            "isEmailCollectionEnabled": True,
            "isMeetingCollectionEnabled": True,
        }
        mock_client_class.return_value = mock_client

        ri = DealCloudRelationshipIntelligence(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
            scope=RI_IMPORT_SCOPE,
        )

        result = ri.get_settings()
        assert result["isEmailCollectionEnabled"] is True


class TestRiMailboxResponseHelpers:
    """Unit tests for RiMailboxResponseVm helpers (swagger: HTTP 200 + per-row status/errors)."""

    def test_failed_when_status_error_and_errors(self):
        row = {
            "userId": 0,
            "status": 3,
            "statusText": "Error",
            "errors": [{"type": 1, "description": "Can not find the mailbox"}],
        }
        assert row["status"] == RI_MAILBOX_STATUS_ERROR
        assert ri_mailbox_response_failed(row) is True

    def test_failed_non_dict(self):
        assert ri_mailbox_response_failed("x") is True  # type: ignore[arg-type]

    def test_failed_status_text_error_only(self):
        assert ri_mailbox_response_failed({"statusText": "Error", "status": 0}) is True

    def test_ok_status_1_no_errors(self):
        assert (
            ri_mailbox_response_failed(
                {"userId": 1, "status": 1, "statusText": "OK", "errors": []},
            )
            is False
        )

    def test_ok_empty_errors_none(self):
        assert ri_mailbox_response_failed({"userId": 1, "status": 1, "statusText": None}) is False

    def test_all_succeeded_requires_non_empty(self):
        assert ri_mailbox_responses_all_succeeded([]) is False
        assert ri_mailbox_responses_all_succeeded([{"status": 1, "errors": None}]) is True

    def test_all_succeeded_false_if_any_failed(self):
        ok = {"status": 1, "errors": None}
        bad = {"status": 3, "statusText": "Error"}
        assert ri_mailbox_responses_all_succeeded([ok, bad]) is False
