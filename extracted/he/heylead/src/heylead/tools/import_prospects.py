"""Tool: import_prospects — Import prospects from CSV data into a campaign.

Parses CSV text with flexible column mapping, deduplicates against
existing contacts and LinkedIn connections, scores prospects, and
creates contact + outreach records in the campaign.
"""

from __future__ import annotations

import csv
import io
import json
import logging
from typing import Any

from ..db.queries import (
    assign_variant,
    create_outreach,
    find_active_campaign,
    get_setting,
    list_ab_tests,
    list_campaigns,
    save_contact,
)
from ..formatter import table
from ..linkedin import get_account_id, get_linkedin_client
from ..services.dedup_service import (
    dedup_prospects,
    fetch_connection_ids,
    format_dedup_summary,
    get_all_known_linkedin_ids,
)
from ..services.icp_match_scorer import compute_icp_match
from ..db.async_bridge import run_db

logger = logging.getLogger(__name__)

# Auto-detected column name mappings (case-insensitive)
_COLUMN_ALIASES: dict[str, list[str]] = {
    "name": ["name", "full_name", "fullname", "contact_name", "person", "lead"],
    "title": ["title", "job_title", "jobtitle", "position", "role"],
    "company": ["company", "company_name", "companyname", "organization", "org"],
    "linkedin_url": [
        "linkedin_url", "linkedin", "profile_url", "profileurl",
        "linkedin_profile", "url", "link",
    ],
    "linkedin_id": ["linkedin_id", "linkedinid", "public_id", "publicid", "slug"],
    "email": ["email", "email_address", "emailaddress", "e-mail"],
    "location": ["location", "city", "region", "country", "geo"],
}


def _detect_columns(headers: list[str]) -> dict[str, int]:
    """Map CSV column headers to known field names. Returns {field: col_index}."""
    mapping: dict[str, int] = {}
    normalized = [h.strip().lower().replace(" ", "_").replace("-", "_") for h in headers]

    for field, aliases in _COLUMN_ALIASES.items():
        for alias in aliases:
            if alias in normalized:
                mapping[field] = normalized.index(alias)
                break

    return mapping


def _parse_csv_rows(
    csv_data: str, mapping: dict[str, int]
) -> list[dict[str, str]]:
    """Parse CSV rows into prospect dicts using the detected column mapping."""
    reader = csv.reader(io.StringIO(csv_data))
    # Skip header row
    try:
        next(reader)
    except StopIteration:
        return []

    prospects: list[dict[str, str]] = []
    for row_num, row in enumerate(reader, start=2):
        if not row or all(not cell.strip() for cell in row):
            continue  # Skip empty rows

        prospect: dict[str, str] = {}
        for field, col_idx in mapping.items():
            if col_idx < len(row):
                prospect[field] = row[col_idx].strip()

        # Validate: must have name + at least one of title/company/linkedin_url
        name = prospect.get("name", "").strip()
        if not name:
            logger.debug("Row %d skipped: no name", row_num)
            continue

        has_context = (
            prospect.get("title")
            or prospect.get("company")
            or prospect.get("linkedin_url")
        )
        if not has_context:
            logger.debug("Row %d skipped: no title/company/linkedin_url", row_num)
            continue

        # Normalize LinkedIn URL → extract linkedin_id
        url = prospect.get("linkedin_url", "")
        if url and not prospect.get("linkedin_id"):
            # Extract public_id from URL like https://linkedin.com/in/john-doe
            slug = url.rstrip("/").split("/in/")[-1].split("/")[0].split("?")[0]
            if slug and slug != url:
                prospect["linkedin_id"] = slug

        prospects.append(prospect)

    return prospects


def _score_imported_prospect(prospect: dict[str, str]) -> float:
    """Score an imported prospect based on data completeness (0.0-1.0)."""
    score = 0.0
    max_score = 0.0

    # Has name (always true at this point)
    max_score += 1.0
    score += 1.0

    # Has title
    max_score += 2.0
    if prospect.get("title"):
        score += 2.0

    # Has company
    max_score += 1.5
    if prospect.get("company"):
        score += 1.5

    # Has LinkedIn URL
    max_score += 2.0
    if prospect.get("linkedin_url") or prospect.get("linkedin_id"):
        score += 2.0

    # Has email
    max_score += 1.0
    if prospect.get("email"):
        score += 1.0

    # Has location
    max_score += 0.5
    if prospect.get("location"):
        score += 0.5

    return round(score / max_score, 2) if max_score > 0 else 0.0


async def run_import_prospects(
    campaign_id: str = "",
    csv_data: str = "",
    linkedin_enrich: bool = False,
) -> str:
    """Import prospects from CSV data into a campaign."""

    # Check setup
    setup_done = await run_db(get_setting, "setup_complete", False)
    if not setup_done:
        return "Setup required. Run setup_profile first."

    if not csv_data.strip():
        return (
            "**import_prospects** — Import prospects from CSV data.\n\n"
            "**Usage**: Pass CSV text with prospect data.\n\n"
            "**Supported columns** (auto-detected, case-insensitive):\n"
            "- `Name` (required)\n"
            "- `Title` / `Job Title` / `Position`\n"
            "- `Company` / `Organization`\n"
            "- `LinkedIn URL` / `LinkedIn` / `Profile URL`\n"
            "- `Email` / `Email Address`\n"
            "- `Location` / `City`\n\n"
            "**Example**:\n"
            "```\n"
            "Name,Title,Company,LinkedIn URL\n"
            "John Doe,CTO,Acme Corp,https://linkedin.com/in/johndoe\n"
            "Jane Smith,VP Engineering,TechCo,https://linkedin.com/in/janesmith\n"
            "```\n\n"
            "Must have name + at least one of: title, company, or LinkedIn URL."
        )

    # Resolve campaign
    campaign, err = await run_db(find_active_campaign, campaign_id)
    if not campaign and not campaign_id:
        campaigns = await run_db(list_campaigns)
        if campaigns:
            campaign = campaigns[0]

    if not campaign:
        return err or "No campaign found. Create one first with create_campaign."

    campaign_id = campaign["id"]
    campaign_name = campaign.get("name", "")

    # Parse CSV
    lines = csv_data.strip().split("\n")
    if len(lines) < 2:
        return "CSV must have at least a header row and one data row."

    # Detect column mapping from header
    reader = csv.reader(io.StringIO(lines[0]))
    headers = next(reader, [])
    mapping = _detect_columns(headers)

    if "name" not in mapping:
        return (
            f"Could not detect a 'Name' column in headers: {headers}\n\n"
            "Make sure your CSV has a column named 'Name', 'Full Name', or 'Contact Name'."
        )

    # Parse all rows
    prospects = _parse_csv_rows(csv_data, mapping)
    if not prospects:
        return "No valid prospect rows found. Each row needs: name + at least one of title/company/LinkedIn URL."

    # Deduplication
    known_ids = await run_db(get_all_known_linkedin_ids)
    connection_ids: set[str] = set()

    try:
        account_id = get_account_id()
        if account_id:
            client = get_linkedin_client()
            connection_ids = await fetch_connection_ids(client, account_id, max_pages=5)
    except Exception as e:
        logger.warning("Connection fetch for dedup failed: %s", e)

    # Convert prospects to dedup-compatible format
    dedup_ready = []
    for p in prospects:
        dedup_ready.append({
            "name": p.get("name", ""),
            "title": p.get("title", ""),
            "company": p.get("company", ""),
            "linkedin_url": p.get("linkedin_url", ""),
            "public_id": p.get("linkedin_id", ""),
            "provider_id": "",
            "email": p.get("email", ""),
            "location": p.get("location", ""),
        })

    filtered, dedup_stats = dedup_prospects(dedup_ready, known_ids, connection_ids)
    dedup_summary = format_dedup_summary(dedup_stats)

    if not filtered:
        return (
            f"All {len(prospects)} prospects were filtered by deduplication.\n\n"
            f"{dedup_summary}\n\n"
            "All imported prospects are either existing connections or already in campaigns."
        )

    # Score and sort — use ICP match if campaign has ICP data
    campaign_icp_json = campaign.get("icp_json", "")
    for p in filtered:
        if campaign_icp_json:
            result = compute_icp_match(p, campaign_icp_json)
            p["_fit_score"] = result["icp_match_score"]
        else:
            p["_fit_score"] = _score_imported_prospect(p)
    filtered.sort(key=lambda p: p.get("_fit_score", 0), reverse=True)

    # Optional: LinkedIn enrichment
    enriched_count = 0
    if linkedin_enrich:
        try:
            account_id = get_account_id()
            client = get_linkedin_client()
            for p in filtered[:50]:  # Cap at 50 to avoid rate limits
                lid = p.get("linkedin_id") or p.get("public_id") or ""
                if not lid:
                    continue
                try:
                    profile = await client.get_profile(account_id, lid)
                    if profile and isinstance(profile, dict):
                        p["_profile_json"] = json.dumps(profile)
                        if not p.get("title") and profile.get("headline"):
                            p["title"] = profile["headline"]
                        if not p.get("company"):
                            headline = profile.get("headline", "")
                            if " at " in headline:
                                p["company"] = headline.rsplit(" at ", 1)[1]
                        enriched_count += 1
                except Exception as e:
                    logger.debug("Enrich failed for %s: %s", lid, e)
        except Exception as e:
            logger.warning("LinkedIn enrichment setup failed: %s", e)

    # Insert contacts + outreaches
    has_ab_test = bool( await run_db(list_ab_tests, campaign_id, status="running"))
    imported = 0
    _csv_detail = f"CSV ({len(filtered)} rows)"
    for p in filtered:
        contact_id = await run_db(save_contact, campaign_id=campaign_id,
            name=p.get("name", ""),
            title=p.get("title", ""),
            company=p.get("company", ""),
            linkedin_url=p.get("linkedin_url", ""),
            linkedin_id=p.get("linkedin_id") or p.get("public_id") or "",
            profile_json=p.get("_profile_json", ""),
            fit_score=p.get("_fit_score", 0.0),
            source="csv_import",
            source_detail=_csv_detail,)
        variant = await run_db(assign_variant, campaign_id) if has_ab_test else None
        await run_db(create_outreach, campaign_id=campaign_id, contact_id=contact_id, variant=variant)
        imported += 1

    # Build summary
    parts: list[str] = []
    parts.append(f"## ✅ Imported {imported} Prospects")
    parts.append(f"**Campaign**: {campaign_name}")
    parts.append(f"**CSV rows parsed**: {len(prospects)}")

    if dedup_summary:
        parts.append(f"**Dedup**: {dedup_summary}")

    if enriched_count:
        parts.append(f"**LinkedIn enriched**: {enriched_count}")

    # Show sample of imported prospects
    parts.append("")
    sample = filtered[:10]
    headers_out = ["Name", "Title", "Company", "Fit"]
    rows_out = []
    for p in sample:
        rows_out.append([
            p.get("name", "")[:25],
            (p.get("title") or "—")[:30],
            (p.get("company") or "—")[:20],
            f"{p.get('_fit_score', 0):.0%}",
        ])
    parts.append(table(headers_out, rows_out))

    if len(filtered) > 10:
        parts.append(f"... and {len(filtered) - 10} more")

    parts.append("")
    parts.append("**Next**: Run `generate_and_send()` to start outreach, or `show_status()` to review.")

    return "\n".join(parts)
