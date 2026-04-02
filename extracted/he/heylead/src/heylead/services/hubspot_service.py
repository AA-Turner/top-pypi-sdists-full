"""HubSpot CRM integration service.

Syncs HeyLead contacts and deals to HubSpot via their REST v3 API.
Uses httpx for async HTTP. Requires a HubSpot private app API key.

HubSpot API docs: https://developers.hubspot.com/docs/api/crm
"""

from __future__ import annotations

import json
import logging
from typing import Any

import httpx

logger = logging.getLogger(__name__)

_BASE_URL = "https://api.hubapi.com"
_TIMEOUT = 30.0


class HubSpotClient:
    """Async HubSpot CRM v3 client."""

    def __init__(self, api_key: str) -> None:
        self.api_key = api_key
        self._headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }

    async def _request(
        self, method: str, path: str, json_data: dict | None = None
    ) -> dict[str, Any]:
        """Make an authenticated request to HubSpot API."""
        url = f"{_BASE_URL}{path}"
        async with httpx.AsyncClient(timeout=_TIMEOUT) as client:
            resp = await client.request(
                method, url, headers=self._headers, json=json_data
            )
            if resp.status_code in (200, 201):
                return resp.json()
            elif resp.status_code == 409:
                # Conflict = already exists, try to extract existing ID
                body = resp.json() if resp.content else {}
                return {"conflict": True, "detail": body}
            else:
                error = resp.text[:500]
                logger.error("HubSpot %s %s failed (%d): %s", method, path, resp.status_code, error)
                raise HubSpotError(f"HubSpot API error ({resp.status_code}): {error}")

    # ── Contacts ──

    async def search_contact_by_linkedin(self, linkedin_url: str) -> dict | None:
        """Search for an existing HubSpot contact by LinkedIn URL."""
        data = {
            "filterGroups": [{
                "filters": [{
                    "propertyName": "hs_linkedinid",
                    "operator": "CONTAINS_TOKEN",
                    "value": linkedin_url.rstrip("/").split("/")[-1],
                }]
            }],
            "properties": ["firstname", "lastname", "email", "company", "jobtitle", "hs_linkedinid"],
            "limit": 1,
        }
        try:
            result = await self._request("POST", "/crm/v3/objects/contacts/search", data)
            results = result.get("results", [])
            return results[0] if results else None
        except HubSpotError:
            return None

    async def create_or_update_contact(
        self,
        name: str,
        email: str = "",
        title: str = "",
        company: str = "",
        linkedin_url: str = "",
    ) -> str:
        """Create or update a HubSpot contact. Returns the HubSpot contact ID."""
        # Split name into first/last
        parts = name.strip().split(None, 1)
        first_name = parts[0] if parts else name
        last_name = parts[1] if len(parts) > 1 else ""

        properties: dict[str, str] = {
            "firstname": first_name,
            "lastname": last_name,
        }
        if email:
            properties["email"] = email
        if title:
            properties["jobtitle"] = title
        if company:
            properties["company"] = company
        if linkedin_url:
            properties["hs_linkedinid"] = linkedin_url

        # Try to find existing contact first
        if linkedin_url:
            existing = await self.search_contact_by_linkedin(linkedin_url)
            if existing:
                contact_id = existing["id"]
                # Update existing
                await self._request(
                    "PATCH",
                    f"/crm/v3/objects/contacts/{contact_id}",
                    {"properties": properties},
                )
                logger.info("Updated HubSpot contact %s: %s", contact_id, name)
                return contact_id

        # Create new
        try:
            result = await self._request(
                "POST", "/crm/v3/objects/contacts", {"properties": properties}
            )
            contact_id = result.get("id", "")
            logger.info("Created HubSpot contact %s: %s", contact_id, name)
            return contact_id
        except HubSpotError as e:
            if "conflict" in str(e).lower() or "already exists" in str(e).lower():
                # Try to find by email
                if email:
                    try:
                        result = await self._request("GET", f"/crm/v3/objects/contacts/{email}?idProperty=email")
                        return result.get("id", "")
                    except HubSpotError:
                        pass
            raise

    # ── Deals ──

    async def create_deal(
        self,
        deal_name: str,
        stage: str = "closedwon",
        amount: str = "",
        contact_id: str = "",
        pipeline: str = "default",
    ) -> str:
        """Create a HubSpot deal. Returns the deal ID."""
        properties: dict[str, str] = {
            "dealname": deal_name,
            "dealstage": stage,
            "pipeline": pipeline,
        }
        if amount:
            properties["amount"] = amount

        result = await self._request(
            "POST", "/crm/v3/objects/deals", {"properties": properties}
        )
        deal_id = result.get("id", "")

        # Associate deal with contact
        if contact_id and deal_id:
            try:
                await self._request(
                    "PUT",
                    f"/crm/v3/objects/deals/{deal_id}/associations/contacts/{contact_id}/3",
                    None,
                )
            except HubSpotError as e:
                logger.warning("Deal-contact association failed: %s", e)

        logger.info("Created HubSpot deal %s: %s", deal_id, deal_name)
        return deal_id

    # ── Notes/Activities ──

    async def create_note(
        self, contact_id: str, body: str
    ) -> str:
        """Create a note associated with a contact."""
        result = await self._request(
            "POST",
            "/crm/v3/objects/notes",
            {
                "properties": {"hs_note_body": body, "hs_timestamp": ""},
                "associations": [{
                    "to": {"id": contact_id},
                    "types": [{"associationCategory": "HUBSPOT_DEFINED", "associationTypeId": 202}],
                }],
            },
        )
        note_id = result.get("id", "")
        logger.debug("Created HubSpot note %s for contact %s", note_id, contact_id)
        return note_id

    # ── Validation ──

    async def test_connection(self) -> bool:
        """Test if the API key is valid."""
        try:
            await self._request("GET", "/crm/v3/objects/contacts?limit=1")
            return True
        except HubSpotError:
            return False


class HubSpotError(Exception):
    """HubSpot API error."""
    pass
