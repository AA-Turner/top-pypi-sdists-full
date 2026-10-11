"""
Relationship Intelligence API operations for DealCloud.

The Relationship Intelligence (RI) API enables:
- Importing email interaction data
- Importing meeting/calendar data
- Reading import status and RI settings

Published v4 paths under ``/api/rest/v4/ri/import`` are only ``emails``, ``meetings``,
``status``, and ``settings`` (see repo ``swagger.json``). Do not add SDK helpers for
paths that are not in that spec.

See: https://api.docs.dealcloud.com/docs - Relationship Intelligence API

**Import POST responses (emails / meetings):** Swagger defines HTTP **200** with a JSON array of
**RiMailboxResponseVm**. Each row has ``status`` (**RiMailboxStatus** enum **1**, **2**, or **3**;
**3** is the error outcome), ``statusText``, ``operationStats``, ``warnings``, and ``errors``
(**RiProblemVm**). Mailbox-level issues—including empty or missing mailbox—are expressed in those
fields; the HTTP status remains **200**. Non-empty ``warnings`` does not imply ``status == 3``.
Callers should inspect each row (or use :func:`ri_mailbox_response_failed` /
:func:`ri_mailbox_responses_all_succeeded`).
"""

from datetime import datetime
from typing import Any, Optional, List, Union

from ..backups.dealcloud_backups import DealCloudBackups

# RiMailboxStatus enum (swagger): 1 | 2 | 3 — 3 is the error outcome for a mailbox row.
RI_MAILBOX_STATUS_ERROR = 3


def ri_mailbox_response_failed(row: dict[str, Any]) -> bool:
    """
    Return True if a single **RiMailboxResponseVm** dict reports failure.

    POST ``/ri/import/emails`` and ``/meetings`` return HTTP **200** with an array of
    these rows; mailbox-level problems use ``status`` / ``statusText`` / ``errors``,
    not HTTP 4xx. Inspect each row after ``import_emails`` / ``import_meeting`` (or use
    :func:`ri_mailbox_responses_all_succeeded`).
    """
    if not isinstance(row, dict):
        return True
    errs = row.get("errors")
    if isinstance(errs, list) and len(errs) > 0:
        return True
    if row.get("status") == RI_MAILBOX_STATUS_ERROR:
        return True
    stxt = row.get("statusText")
    if isinstance(stxt, str) and stxt.strip().lower() == "error":
        return True
    return False


def ri_mailbox_responses_all_succeeded(rows: List[dict[str, Any]]) -> bool:
    """
    True if ``rows`` is non-empty and every element is a successful RiMailboxResponseVm
    (:func:`ri_mailbox_response_failed` is False for each).
    """
    if not rows:
        return False
    return not any(ri_mailbox_response_failed(r) for r in rows)


def _email_address_vm(address: str, name: Optional[str] = None) -> dict:
    """Build EmailAddressVm: { address, name? } per Swagger."""
    out = {"address": address}
    if name is not None:
        out["name"] = name
    return out


def _attendee_vm(address: str, name: Optional[str] = None, is_accepted: bool = True) -> dict:
    """Build RiAttendeeVm: { isAccepted, address, name? } per Swagger."""
    out = {"address": address, "isAccepted": is_accepted}
    if name is not None:
        out["name"] = name
    return out


class DealCloudRelationshipIntelligence(DealCloudBackups):
    """
    One link in the linear inheritance chain; parent order is for composition
    (single DealCloud client gets all features), not dependency. Avoids mixins.
    Relationship Intelligence API operations.
    
    Provides email and meeting data import for relationship scoring.
    """
    
    @property
    def relationship_intelligence_url(self) -> str:
        """
        Get the Relationship Intelligence API base URL.
        
        Use this for custom RI API calls not covered by SDK methods.
        
        Returns:
            str: RI API URL (e.g., "https://site.dealcloud.com/api/rest/v4/ri/import")
        
        Example:
            >>> # Custom RI endpoint call
            >>> url = f"{dc.ri_url}/analytics"
            >>> response = dc.client.get(url)
        """
        return self._ri_url
    
    # =========================================================================
    # Email Import (payloads per Swagger: RiEmailMailboxVm / RiEmailVm / EmailAddressVm)
    # =========================================================================
    
    def import_emails(
        self,
        mailboxes: List[dict],
    ) -> List[dict]:
        """
        Import email interaction data for relationship scoring.
        
        POST /api/rest/v4/ri/import/emails
        
        Request body is an array of RiEmailMailboxVm per Swagger:
        - userId (int)
        - handlerType (int, RiHandlerType: 1 | 2 | 3)
        - emails: array of RiEmailVm:
          - uniqueId (string)
          - sentDate (date-time string)
          - modifiedDate (date-time string, optional)
          - sender: { address, name? } (EmailAddressVm)
          - recipientsTo: [ { address, name? } ]
          - recipientsCc: [ { address, name? } ] (optional)
        
        Returns:
            List of RiMailboxResponseVm (userId, status, statusText, operationStats, warnings, errors).

        Note:
            ``status`` is **RiMailboxStatus** (swagger: **1**, **2**, or **3**; **3** is error—see
            ``RI_MAILBOX_STATUS_ERROR``). HTTP **200** is returned even when a row reports failure or
            non-empty ``errors`` / ``warnings``; inspect each row or use
            :func:`ri_mailbox_response_failed` / :func:`ri_mailbox_responses_all_succeeded`.
        """
        url = f"{self._ri_url}/emails"
        return self._client.post(url, json=mailboxes)
    
    def import_email(
        self,
        user_id: int,
        handler_type: int,
        unique_id: str,
        sent_date: datetime,
        sender_address: str,
        recipients_to: List[Union[str, dict]],
        sender_name: Optional[str] = None,
        recipients_cc: Optional[List[Union[str, dict]]] = None,
        modified_date: Optional[datetime] = None,
    ) -> List[dict]:
        """
        Import a single email (convenience): builds one RiEmailMailboxVm with one RiEmailVm.
        
        Args:
            user_id: DealCloud user ID (mailbox owner).
            handler_type: RiHandlerType (1, 2, or 3 per Swagger).
            unique_id: Unique message id (RiEmailVm.uniqueId).
            sent_date: When the email was sent.
            sender_address: Sender email address.
            recipients_to: To recipients (strings or {address, name?} dicts).
            sender_name: Optional sender display name.
            recipients_cc: Optional CC recipients (strings or {address, name?} dicts).
            modified_date: Optional modified date (RiEmailVm.modifiedDate).
        
        Returns:
            List of RiMailboxResponseVm (same as import_emails). See :func:`import_emails` Note
            on HTTP 200 vs per-row status / errors.
        """
        def to_address_vm(x: Union[str, dict]) -> dict:
            if isinstance(x, str):
                return _email_address_vm(x)
            return {"address": x["address"], **({} if x.get("name") is None else {"name": x["name"]})}

        email: dict = {
            "uniqueId": unique_id,
            "sentDate": sent_date.isoformat(),
            "sender": _email_address_vm(sender_address, sender_name),
            "recipientsTo": [to_address_vm(r) for r in recipients_to],
        }
        if recipients_cc:
            email["recipientsCc"] = [to_address_vm(r) for r in recipients_cc]
        if modified_date is not None:
            email["modifiedDate"] = modified_date.isoformat()

        mailbox = {
            "userId": user_id,
            "handlerType": handler_type,
            "emails": [email],
        }
        return self.import_emails([mailbox])
    
    # =========================================================================
    # Meeting Import (payloads per Swagger: RiMeetingMailboxVm / RiMeetingVm / RiAttendeeVm)
    # =========================================================================
    
    def import_meetings(
        self,
        mailboxes: List[dict],
    ) -> List[dict]:
        """
        Import meeting data for relationship scoring.
        
        POST /api/rest/v4/ri/import/meetings
        
        Request body is an array of RiMeetingMailboxVm per Swagger:
        - userId (int)
        - meetings: array of RiMeetingVm:
          - uniqueId (string)
          - startDate (date-time string)
          - organizer: { address, name? } (EmailAddressVm)
          - requiredAttendees: [ { isAccepted, address, name? } ] (optional)
          - optionalAttendees: [ { isAccepted, address, name? } ] (optional)
        
        Returns:
            List of RiMailboxResponseVm (same shape as :func:`import_emails`).

        Note:
            Same as :func:`import_emails` (HTTP **200** + per-row ``status`` / ``errors`` / ``warnings``).
        """
        url = f"{self._ri_url}/meetings"
        return self._client.post(url, json=mailboxes)
    
    def import_meeting(
        self,
        user_id: int,
        unique_id: str,
        start_date: datetime,
        organizer_address: str,
        required_attendees: List[Union[str, dict]],
        organizer_name: Optional[str] = None,
        optional_attendees: Optional[List[Union[str, dict]]] = None,
        is_accepted: bool = True,
    ) -> List[dict]:
        """
        Import a single meeting (convenience): builds one RiMeetingMailboxVm with one RiMeetingVm.
        
        Args:
            user_id: DealCloud user ID (mailbox owner).
            unique_id: Unique meeting id (RiMeetingVm.uniqueId).
            start_date: Meeting start time.
            organizer_address: Organizer email address.
            required_attendees: Required attendees (strings or {address, name?} dicts).
            organizer_name: Optional organizer display name.
            optional_attendees: Optional attendees (strings or {address, name?} dicts).
            is_accepted: Value for RiAttendeeVm.isAccepted on all attendees.
        
        Returns:
            List of RiMailboxResponseVm (same as import_meetings). See :func:`import_emails` Note.
        """
        def to_attendee_vm(x: Union[str, dict]) -> dict:
            if isinstance(x, str):
                return _attendee_vm(x, is_accepted=is_accepted)
            addr = x.get("address", "")
            return _attendee_vm(addr, x.get("name"), is_accepted=x.get("isAccepted", is_accepted))

        meeting: dict = {
            "uniqueId": unique_id,
            "startDate": start_date.isoformat(),
            "organizer": _email_address_vm(organizer_address, organizer_name),
            "requiredAttendees": [to_attendee_vm(a) for a in required_attendees],
        }
        if optional_attendees:
            meeting["optionalAttendees"] = [to_attendee_vm(a) for a in optional_attendees]

        mailbox = {
            "userId": user_id,
            "meetings": [meeting],
        }
        return self.import_meetings([mailbox])
    
    # =========================================================================
    # Processing Status
    # =========================================================================
    
    def get_processing_status(
        self,
        user_ids: Optional[List[int]] = None,
    ) -> List[dict]:
        """
        Get status of imported data processing per mailbox.
        
        GET /api/rest/v4/ri/import/status
        
        Args:
            user_ids: Optional list of user IDs to filter (query param userIds).
        
        Returns:
            List of RiMailboxStatusVm: userId, emailAddress, lastEmailSyncDate, lastMeetingSyncDate.
        """
        url = f"{self._ri_url}/status"
        if user_ids is not None:
            url = f"{url}?userIds={','.join(map(str, user_ids))}"
        return self._client.get(url)

    # =========================================================================
    # Settings
    # =========================================================================
    
    def get_settings(self) -> dict:
        """
        Get Relationship Intelligence configuration.
        
        GET /api/rest/v4/ri/import/settings
        
        Returns:
            RiSettingsVm per Swagger: historicalPeriodInMonths, syncLevel,
            isSignatureCollectionEnabled, isEmailCollectionEnabled, isMeetingCollectionEnabled.
        """
        url = f"{self._ri_url}/settings"
        return self._client.get(url)

