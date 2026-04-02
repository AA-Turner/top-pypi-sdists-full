"""Tool: contacts — Manage the global contact base.

Search, browse, tag, note, and view cross-campaign history for all contacts.
One master record per person across all campaigns.
"""

from __future__ import annotations

import csv
import io
import json
import logging
import time
from datetime import datetime, timezone

from ..db import aio as db
from ..linkedin import get_account_id, get_linkedin_client
from ..formatter import source_badge, stars, table
from ..db.async_bridge import run_db

logger = logging.getLogger(__name__)


def _ts_to_date(ts: int | None) -> str:
    if not ts:
        return "—"
    dt = datetime.fromtimestamp(ts, tz=timezone.utc)
    return dt.strftime("%Y-%m-%d")


def _ts_to_relative(ts: int | None) -> str:
    if not ts:
        return "—"
    now = int(time.time())
    diff = now - ts
    days = abs(diff) // 86400
    if diff < 0:
        return f"in {days}d" if days > 0 else "just now"
    if days == 0:
        return "today"
    elif days == 1:
        return "yesterday"
    elif days < 30:
        return f"{days}d ago"
    elif days < 365:
        return f"{days // 30}mo ago"
    else:
        return f"{days // 365}y ago"


def _lifecycle_icon(stage: str) -> str:
    return {
        "prospect": "○",
        "contacted": "◔",
        "connected": "◑",
        "engaged": "◕",
        "customer": "●",
        "lost": "✗",
        "churned": "↻",
        "do_not_contact": "⊘",
    }.get(stage, "?")


async def run_contacts(
    action: str = "list",
    query: str = "",
    contact_id: str = "",
    lifecycle_stage: str = "",
    tag: str = "",
    note: str = "",
    min_fit_score: float = 0.0,
    limit: int = 25,
    format: str = "table",
) -> str:
    """Route contacts actions."""
    setup_done = await db.get_setting("setup_complete", False)
    if not setup_done:
        return "Setup required. Run setup_profile first."

    action = action.strip().lower()

    if action == "list":
        return await _handle_list(lifecycle_stage, tag, min_fit_score, limit)
    elif action == "search":
        return await _handle_search(query, lifecycle_stage, tag, min_fit_score, limit)
    elif action == "view":
        return await _handle_view(contact_id)
    elif action == "tag":
        return await _handle_tag(contact_id, tag)
    elif action == "note":
        return await _handle_note(contact_id, note)
    elif action == "stage":
        return await _handle_stage(contact_id, lifecycle_stage)
    elif action == "stats":
        return await _handle_stats()
    elif action == "export":
        return await _handle_export(lifecycle_stage, tag, format)
    elif action == "linkedin_search":
        return await _handle_linkedin_search(query, limit)
    elif action == "enrich":
        return await _handle_enrich(contact_id, query, limit)
    elif action == "find_duplicates":
        return await _handle_find_duplicates()
    elif action == "merge":
        return await _handle_merge(contact_id, query)
    elif action in ("my_connections", "search_connections"):
        return await _handle_my_connections(query, limit)
    else:
        return (
            f"Unknown action: {action!r}\n\n"
            "Available actions: list, search, view, tag, note, stage, stats, export, "
            "linkedin_search, enrich, find_duplicates, merge, my_connections"
        )


# ──────────────────────────────────────────────
# Action handlers
# ──────────────────────────────────────────────

async def _handle_list(
    lifecycle_stage: str, tag: str, min_fit_score: float, limit: int
) -> str:
    contacts = await db.search_global_contacts(
        lifecycle_stage=lifecycle_stage,
        tag=tag,
        min_fit_score=min_fit_score,
        limit=limit,
        order_by="updated_at DESC",
    )
    if not contacts:
        filters = []
        if lifecycle_stage:
            filters.append(f"stage={lifecycle_stage}")
        if tag:
            filters.append(f"tag={tag}")
        if min_fit_score > 0:
            filters.append(f"score>={min_fit_score}")
        filter_str = f" (filters: {', '.join(filters)})" if filters else ""
        return f"No contacts found{filter_str}.\n\nContacts are added automatically when you create campaigns."

    return _format_contact_list(contacts, limit)


async def _handle_search(
    query: str, lifecycle_stage: str, tag: str, min_fit_score: float, limit: int
) -> str:
    if not query:
        return "Search query is required. Usage: contacts(action='search', query='CEO fintech')"

    contacts = await db.search_global_contacts(
        query=query,
        lifecycle_stage=lifecycle_stage,
        tag=tag,
        min_fit_score=min_fit_score,
        limit=limit,
    )
    if not contacts:
        return f"No contacts found matching '{query}'."

    return _format_contact_list(contacts, limit, title=f"Search: \"{query}\"")


async def _handle_view(contact_id: str) -> str:
    if not contact_id:
        return "contact_id is required. Usage: contacts(action='view', contact_id='...')"

    history = await db.get_cross_campaign_history(contact_id)
    if not history:
        return f"Contact {contact_id!r} not found."

    gc = history["global_contact"]
    campaigns = history["campaigns"]
    signals = history["signals"]

    lines = [
        f"Contact: {gc['name']}",
        "=" * 60,
        "",
        f"  Title:     {gc.get('title') or '—'}",
        f"  Company:   {gc.get('company') or '—'}",
        f"  LinkedIn:  {('[Profile](' + gc['linkedin_url'] + ')') if gc.get('linkedin_url') else gc.get('linkedin_id') or '—'}",
        f"  Email:     {gc.get('email') or '—'}",
        f"  Location:  {gc.get('location') or '—'}",
        "",
        f"  Lifecycle: {_lifecycle_icon(gc.get('lifecycle_stage', 'prospect'))} {gc.get('lifecycle_stage', 'prospect')}",
        f"  Fit Score: {stars(gc.get('fit_score') or 0)} ({gc.get('fit_score', 0):.2f})",
        f"  Source:    {source_badge(gc.get('source', 'search'), gc.get('source_detail', ''))}",
        f"  First seen:     {_ts_to_date(gc.get('created_at'))}",
        f"  Last activity:  {_ts_to_relative(gc.get('last_interaction_at'))}",
        f"  Campaigns:      {gc.get('total_campaigns', 0)}",
    ]

    # Tags
    tags = json.loads(gc.get("tags_json") or "[]")
    if tags:
        lines.append(f"  Tags:      {', '.join(tags)}")

    # Notes
    notes = json.loads(gc.get("notes_json") or "[]")
    if notes:
        lines.append("")
        lines.append("  Notes:")
        for n in notes[-5:]:  # Show last 5
            lines.append(f"    [{_ts_to_date(n.get('created_at'))}] {n.get('text', '')}")

    # Enriched profile data
    _append_enriched_profile(lines, gc)

    # Campaign history
    if campaigns:
        lines.append("")
        lines.append(f"Campaign History ({len(campaigns)} campaigns)")
        lines.append("-" * 60)
        for camp in campaigns:
            outreach = camp.get("outreach") or {}
            status = outreach.get("status", "—")
            msgs = camp.get("messages", [])
            engs = camp.get("engagements", [])
            lines.append(
                f"  {camp['campaign_name']} ({camp.get('campaign_status', '?')})"
            )
            lines.append(
                f"    Status: {status}  |  "
                f"Fit: {camp.get('fit_score', 0):.2f}  |  "
                f"Messages: {len(msgs)}  |  Engagements: {len(engs)}"
            )

            # Show messages
            for msg in msgs[-3:]:  # Last 3 messages
                role = "You" if msg.get("role") == "sdr" else "Them"
                text = (msg.get("text") or "")[:80]
                lines.append(f"      [{role}] {text}")

            # Show engagements
            for eng in engs[-2:]:  # Last 2 engagements
                atype = eng.get("action_type", "?")
                text = (eng.get("text") or eng.get("reaction_type") or "")[:60]
                lines.append(f"      [{atype}] {text}")

    # Signals
    if signals:
        lines.append("")
        lines.append(f"Buying Signals ({len(signals)})")
        lines.append("-" * 60)
        for sig in signals[:5]:
            stype = sig.get("signal_type", "?")
            content = (sig.get("content") or "")[:60]
            when = _ts_to_relative(sig.get("detected_at"))
            lines.append(f"  [{stype}] {content} ({when})")

    lines.append("")
    lines.append(f"ID: {contact_id}")
    return "\n".join(lines)


async def _handle_tag(contact_id: str, tag: str) -> str:
    if not contact_id:
        return "contact_id is required. Usage: contacts(action='tag', contact_id='...', tag='enterprise')"
    if not tag:
        return "tag is required. Prefix with '-' to remove. Examples: 'enterprise', '-enterprise'"

    gc = await db.get_global_contact(contact_id)
    if not gc:
        return f"Contact {contact_id!r} not found."

    if tag.startswith("-"):
        remove_tag = tag[1:].strip()
        await db.remove_global_contact_tag(contact_id, remove_tag)
        return f"Removed tag '{remove_tag}' from {gc['name']}."
    else:
        await db.add_global_contact_tag(contact_id, tag)
        return f"Added tag '{tag.strip().lower()}' to {gc['name']}."


async def _handle_note(contact_id: str, note: str) -> str:
    if not contact_id:
        return "contact_id is required. Usage: contacts(action='note', contact_id='...', note='...')"
    if not note:
        return "note text is required."

    gc = await db.get_global_contact(contact_id)
    if not gc:
        return f"Contact {contact_id!r} not found."

    await db.add_global_contact_note(contact_id, note)
    return f"Note added to {gc['name']}."


async def _handle_stage(contact_id: str, lifecycle_stage: str) -> str:
    if not contact_id:
        return "contact_id is required. Usage: contacts(action='stage', contact_id='...', lifecycle_stage='customer')"
    if not lifecycle_stage:
        return (
            "lifecycle_stage is required. Options: "
            "prospect, contacted, connected, engaged, customer, lost, churned, do_not_contact"
        )

    gc = await db.get_global_contact(contact_id)
    if not gc:
        return f"Contact {contact_id!r} not found."

    old_stage = gc.get("lifecycle_stage", "prospect")
    await db.update_global_contact_lifecycle(contact_id, lifecycle_stage)

    # Re-read to check if it actually changed
    gc2 = await db.get_global_contact(contact_id)
    new_stage = gc2.get("lifecycle_stage", old_stage) if gc2 else old_stage

    if new_stage == old_stage and lifecycle_stage != old_stage:
        return (
            f"Cannot change {gc['name']} from '{old_stage}' to '{lifecycle_stage}' "
            f"(lifecycle only promotes forward)."
        )

    return f"Updated {gc['name']}: {old_stage} -> {new_stage}"


async def _handle_stats() -> str:
    stats = await db.get_global_contact_stats()

    if stats["total"] == 0:
        return "No contacts in the global base yet.\n\nContacts are added automatically when you create campaigns."

    lines = [
        "Contact Base",
        "=" * 50,
        "",
        f"  Total contacts: {stats['total']}",
        "",
        "  By Lifecycle:",
    ]

    for stage, count in stats["by_lifecycle"].items():
        icon = _lifecycle_icon(stage)
        lines.append(f"    {icon} {stage}: {count}")

    if stats["by_source"]:
        from ..constants import SOURCE_LABELS
        lines.append("")
        lines.append("  By Source:")
        for src, count in stats["by_source"].items():
            label = SOURCE_LABELS.get(src, src.replace("_", " ").title())
            lines.append(f"    {label}: {count}")

    if stats["top_tags"]:
        lines.append("")
        lines.append("  Top Tags:")
        for tag_name, count in stats["top_tags"]:
            lines.append(f"    #{tag_name}: {count}")

    return "\n".join(lines)


async def _handle_export(lifecycle_stage: str, tag: str, fmt: str) -> str:
    contacts = await db.search_global_contacts(
        lifecycle_stage=lifecycle_stage,
        tag=tag,
        limit=1000,
        order_by="name ASC",
    )

    if not contacts:
        return "No contacts to export."

    if fmt == "json":
        # Strip large blobs for export
        export = []
        for c in contacts:
            export.append({
                "id": c["id"],
                "name": c.get("name") or "",
                "title": c.get("title") or "",
                "company": c.get("company") or "",
                "linkedin_url": c.get("linkedin_url") or "",
                "email": c.get("email") or "",
                "location": c.get("location") or "",
                "lifecycle_stage": c.get("lifecycle_stage") or "prospect",
                "fit_score": c.get("fit_score") or 0.0,
                "tags": json.loads(c.get("tags_json") or "[]"),
                "total_campaigns": c.get("total_campaigns") or 0,
                "source": c.get("source") or "",
            })
        return json.dumps(export, indent=2)

    elif fmt == "csv":
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow([
            "Name", "Title", "Company", "LinkedIn URL", "Email",
            "Location", "Lifecycle", "Fit Score", "Tags", "Campaigns", "Source",
        ])
        for c in contacts:
            tags = json.loads(c.get("tags_json") or "[]")
            writer.writerow([
                c.get("name") or "",
                c.get("title") or "",
                c.get("company") or "",
                c.get("linkedin_url") or "",
                c.get("email") or "",
                c.get("location") or "",
                c.get("lifecycle_stage") or "prospect",
                f"{c.get('fit_score', 0):.2f}",
                "; ".join(tags),
                c.get("total_campaigns") or 0,
                c.get("source") or "",
            ])
        return output.getvalue()

    else:
        # Default: markdown table
        headers = ["Name", "Company", "Stage", "Fit", "Campaigns"]
        rows = []
        for c in contacts[:50]:  # Cap table at 50 rows
            rows.append([
                (c.get("name") or "?")[:25],
                (c.get("company") or "—")[:20],
                f"{_lifecycle_icon(c.get('lifecycle_stage', 'prospect'))} {c.get('lifecycle_stage', 'prospect')}",
                stars(c.get("fit_score") or 0),
                str(c.get("total_campaigns") or 0),
            ])

        result = table(headers, rows)
        total = len(contacts)
        if total > 50:
            result += f"\n\n... and {total - 50} more. Use format='csv' or format='json' for full export."
        return result


def _append_enriched_profile(lines: list[str], gc: dict) -> None:
    """Append enriched profile details from profile_json if available."""
    raw = gc.get("profile_json") or ""
    if not raw:
        return
    try:
        profile = json.loads(raw)
    except (json.JSONDecodeError, TypeError):
        return

    # Only show section if we have rich data (not just basic search fields)
    rich_keys = {"contact_info", "connections_count", "summary", "experience",
                 "education", "skills", "follower_count", "websites"}
    if not rich_keys & set(profile.keys()):
        return

    lines.append("")
    lines.append("Enriched Profile")
    lines.append("-" * 60)

    # Contact info
    ci = profile.get("contact_info") or {}
    emails = ci.get("emails") or []
    phones = ci.get("phones") or []
    addresses = ci.get("adresses") or ci.get("addresses") or []
    if emails:
        lines.append(f"  Email:    {', '.join(emails)}")
    if phones:
        lines.append(f"  Phone:    {', '.join(phones)}")
    if addresses:
        lines.append(f"  Address:  {', '.join(addresses)}")

    # Summary / About
    summary = profile.get("summary") or ""
    if summary:
        lines.append("")
        lines.append("  About:")
        for chunk in [summary[i:i+76] for i in range(0, len(summary), 76)][:5]:
            lines.append(f"    {chunk}")
        if len(summary) > 380:
            lines.append("    ...")

    # Network stats
    stats_parts = []
    conn = profile.get("connections_count")
    if conn:
        stats_parts.append(f"{conn} connections")
    followers = profile.get("follower_count")
    if followers:
        stats_parts.append(f"{followers} followers")
    shared = profile.get("shared_connections_count")
    if shared:
        stats_parts.append(f"{shared} shared")
    distance = profile.get("network_distance") or ""
    if distance:
        stats_parts.append(distance.replace("_", " ").lower())
    if stats_parts:
        lines.append(f"  Network:  {' | '.join(stats_parts)}")

    # Websites
    websites = profile.get("websites") or []
    if websites:
        lines.append(f"  Websites: {', '.join(websites[:3])}")

    # Experience
    experience = profile.get("experience") or []
    if experience:
        lines.append("")
        lines.append("  Experience:")
        for exp in experience[:3]:
            title = exp.get("title") or ""
            company = exp.get("company") or exp.get("company_name") or ""
            start = exp.get("start_date") or exp.get("start") or ""
            end = exp.get("end_date") or exp.get("end") or "Present"
            entry = f"    {title}"
            if company:
                entry += f" @ {company}"
            if start:
                entry += f" ({start} - {end})"
            lines.append(entry)
        if len(experience) > 3:
            lines.append(f"    ... +{len(experience) - 3} more")

    # Education
    education = profile.get("education") or []
    if education:
        lines.append("")
        lines.append("  Education:")
        for edu in education[:3]:
            school = edu.get("school") or edu.get("school_name") or ""
            degree = edu.get("degree") or edu.get("degree_name") or ""
            field = edu.get("field") or edu.get("field_of_study") or ""
            entry = f"    {school}"
            if degree or field:
                entry += f" — {', '.join(filter(None, [degree, field]))}"
            lines.append(entry)

    # Skills
    skills = profile.get("skills") or []
    if skills:
        skill_names = [s if isinstance(s, str) else s.get("name", "") for s in skills[:10]]
        lines.append(f"  Skills:   {', '.join(filter(None, skill_names))}")
        if len(skills) > 10:
            lines.append(f"            ... +{len(skills) - 10} more")

    # Certifications
    certs = profile.get("certifications") or []
    if certs:
        cert_names = [c.get("name", "") for c in certs[:3]]
        lines.append(f"  Certs:    {', '.join(filter(None, cert_names))}")

    # Languages
    languages = profile.get("languages") or []
    if languages:
        lang_strs = []
        for lang in languages[:5]:
            name = lang if isinstance(lang, str) else lang.get("name", "")
            if name:
                lang_strs.append(name)
        if lang_strs:
            lines.append(f"  Languages: {', '.join(lang_strs)}")

    # Flags
    flags = []
    if profile.get("is_premium"):
        flags.append("Premium")
    if profile.get("is_creator"):
        flags.append("Creator")
    if profile.get("is_influencer"):
        flags.append("Influencer")
    if profile.get("is_open_profile"):
        flags.append("Open Profile")
    if flags:
        lines.append(f"  Flags:    {', '.join(flags)}")


async def _handle_linkedin_search(query: str, limit: int) -> str:
    """Search LinkedIn for people by name/title/company."""
    if not query:
        return (
            "Search query is required.\n"
            "Usage: contacts(action='linkedin_search', query='John Smith Google')\n"
            "You can search by name, title, company, or any combination."
        )

    account_id = get_account_id()
    if not account_id:
        return (
            "No LinkedIn account connected.\n\n"
            "Run setup_profile first to connect your LinkedIn account."
        )

    client = get_linkedin_client()
    count = min(limit, 25)

    try:
        results, _cursor = await client.search_people(
            account_id=account_id,
            keywords=query,
            count=count,
        )

        if not results:
            return f"No LinkedIn profiles found for '{query}'."

        # Enrich each result with full LinkedIn profile
        enriched_count = 0
        for person in results:
            lid = person.get("provider_id") or person.get("public_id") or ""
            if not lid:
                continue
            try:
                profile = await client.get_profile(account_id, lid)
                if profile and isinstance(profile, dict):
                    person["_profile_json"] = json.dumps(profile)
                    if not person.get("title") and profile.get("headline"):
                        person["title"] = profile["headline"]
                    if not person.get("company"):
                        headline = profile.get("headline", "")
                        if " at " in headline:
                            person["company"] = headline.rsplit(" at ", 1)[1]
                    enriched_count += 1
            except Exception as e:
                logger.debug("Enrich failed for %s: %s", lid, e)

        # Fetch recent posts for enriched profiles (posts-on-enrichment)
        posts_fetched = 0
        for person in results:
            lid = person.get("provider_id") or person.get("public_id") or ""
            if not lid:
                continue
            try:
                posts = await client.get_user_posts(account_id, lid, limit=10)
                if posts and not (isinstance(posts[0], dict) and "_status_code" in posts[0]):
                    for post in posts:
                        pid = post.get("id", "")
                        txt = post.get("text", "")
                        if pid and txt:
                            await db.upsert_post(
                                pid,
                                author_linkedin_id=lid,
                                author_name=person.get("name", ""),
                                text=txt[:2000],
                                metrics_json=json.dumps(post.get("metrics", {})),
                                source="enrichment",
                            )
                            posts_fetched += 1
            except Exception:
                pass  # Post fetch failure doesn't block search results
        if posts_fetched:
            logger.info("Fetched %d posts during enrichment for %d profiles", posts_fetched, len(results))
    except Exception as e:
        return f"LinkedIn search failed: {e}"
    finally:
        await client.close()

    # Save results to global_contacts
    saved_ids = []
    for person in results:
        linkedin_id = person.get("provider_id") or person.get("public_id") or ""
        if not linkedin_id:
            continue
        try:
            gid = await db.upsert_global_contact(
                linkedin_id=linkedin_id,
                name=person.get("name", ""),
                title=person.get("title", ""),
                company=person.get("company", ""),
                linkedin_url=person.get("linkedin_url", ""),
                location=person.get("location", ""),
                profile_json=person.get("_profile_json", ""),
                source="linkedin_lookup",
                source_detail=f"Search: {query[:80]}",
            )
            saved_ids.append(gid)
        except Exception:
            logger.warning("Failed to save LinkedIn result to global contacts", exc_info=True)

    # Format output
    lines = [
        f"LinkedIn Search: \"{query}\"",
        "=" * 50,
        "",
    ]

    for i, person in enumerate(results, 1):
        name = person.get("name") or "?"
        headline = person.get("headline") or ""
        company = person.get("company") or ""
        title_str = person.get("title") or ""
        location = person.get("location") or ""
        url = person.get("linkedin_url") or ""

        lines.append(f"{i}. {name}")
        if headline:
            lines.append(f"   {headline}")
        elif title_str:
            detail = title_str
            if company:
                detail += f" at {company}"
            lines.append(f"   {detail}")
        if location:
            lines.append(f"   Location: {location}")
        if url:
            lines.append(f"   {url}")
        lines.append("")

    total = len(results)
    saved = len(saved_ids)
    enrich_summary = f"Found {total} results, enriched {enriched_count} profiles"
    if posts_fetched:
        enrich_summary += f", fetched {posts_fetched} posts"
    enrich_summary += "."
    lines.append(enrich_summary)
    if saved > 0:
        lines.append(
            f"Saved {saved} to your contact base (source: linkedin_lookup). "
            "Use contacts(action='search') to find them, or tag/note them."
        )

    return "\n".join(lines)


async def _handle_my_connections(query: str, limit: int = 25) -> str:
    """Search locally-synced 1st-degree LinkedIn connections."""
    from ..db.async_bridge import run_db
    from ..db.connection_queries import (
        get_connection_sync_status,
        list_all_connections,
        search_my_connections,
    )
    from ..services.connection_sync import FULL_SYNC_STALE_SECONDS

    # Resolve account_id
    account_id = await db.get_setting("unipile_account_id", "")
    if not account_id:
        return "No LinkedIn account connected. Run setup_profile first."

    # Check sync status
    status = await run_db(get_connection_sync_status, account_id)

    # Auto-sync if never synced or stale
    needs_sync = (
        not status["synced"]
        or (status["age_seconds"] is not None and status["age_seconds"] > FULL_SYNC_STALE_SECONDS)
    )
    if needs_sync:
        try:
            from ..linkedin import get_linkedin_client
            from ..services.connection_sync import sync_connections

            client = get_linkedin_client()
            synced = await sync_connections(client, account_id, force=True)
            # Refresh status after sync
            status = await run_db(get_connection_sync_status, account_id)
            if synced == 0 and not status["synced"]:
                return (
                    "Connection sync completed but no connections found. "
                    "Your LinkedIn account may need to be reconnected."
                )
        except Exception as e:
            if not status["synced"]:
                return f"Failed to sync connections: {e}\n\nTry again or run `network(action='sync')` first."
            # If we have stale data, proceed with it
            logger.warning("Connection sync failed, using stale data: %s", e)

    # Search or list
    if query.strip():
        results = await run_db(search_my_connections, query.strip(), account_id, limit)
    else:
        results = await run_db(list_all_connections, account_id, limit)

    if not results:
        if query.strip():
            return f"No 1st-degree connections matching '{query}'. You have {status['count']:,} connections synced."
        return "No connections synced yet."

    # Format results
    lines = [
        f"Your 1st-Degree Connections" + (f" matching '{query}'" if query.strip() else ""),
        "=" * 50,
        "",
    ]

    for i, c in enumerate(results, 1):
        name = c.get("name") or "Unknown"
        headline = c.get("headline") or ""
        company = c.get("company") or ""
        location = c.get("location") or ""
        profile_url = c.get("profile_url") or ""
        public_id = c.get("public_id") or ""

        # Build profile URL from public_id if missing
        if not profile_url and public_id:
            profile_url = f"https://www.linkedin.com/in/{public_id}"

        lines.append(f"{i}. **{name}**")
        if headline:
            lines.append(f"   {headline}")
        elif company:
            lines.append(f"   {company}")
        if location:
            lines.append(f"   Location: {location}")
        if profile_url:
            lines.append(f"   {profile_url}")
        lines.append("")

    # Footer
    age_str = ""
    if status["age_seconds"] is not None:
        hours = status["age_seconds"] // 3600
        if hours < 1:
            age_str = f"{status['age_seconds'] // 60}m ago"
        elif hours < 24:
            age_str = f"{hours}h ago"
        else:
            age_str = f"{hours // 24}d ago"
    lines.append(
        f"Showing {len(results)} of {status['count']:,} connections"
        + (f" (synced {age_str})" if age_str else "")
    )

    return "\n".join(lines)


# ──────────────────────────────────────────────
# Formatting helpers
# ──────────────────────────────────────────────

def _format_contact_list(
    contacts: list[dict], limit: int, title: str = "Contact Base"
) -> str:
    lines = [title, "=" * 50, ""]

    for c in contacts:
        stage = c.get("lifecycle_stage", "prospect")
        icon = _lifecycle_icon(stage)
        name = c.get("name") or "?"
        company = c.get("company") or ""
        title_str = c.get("title") or ""
        score = c.get("fit_score") or 0.0
        tags = json.loads(c.get("tags_json") or "[]")

        line1 = f"{icon} {name}"
        if company:
            line1 += f" @ {company}"
        lines.append(line1)

        details = f"   {stage}"
        if title_str:
            details += f"  |  {title_str[:40]}"
        details += f"  |  {stars(score)}"
        if tags:
            details += f"  |  #{', #'.join(tags[:3])}"
        lines.append(details)
        lines.append(f"   ID: {c['id']}")
        lines.append("")

    total = len(contacts)
    if total >= limit:
        lines.append(f"Showing {limit} contacts. Use limit= to see more, or action='search' to filter.")
    else:
        lines.append(f"Total: {total} contacts")
    return "\n".join(lines)


# ──────────────────────────────────────────────
# Enrichment handler
# ──────────────────────────────────────────────

async def _handle_enrich(contact_id: str, query: str, limit: int) -> str:
    """Enrich contacts with full LinkedIn profiles and recent posts.

    Single contact mode: provide contact_id.
    Batch mode: provide query to search global_contacts missing profile_json.
    """
    import json as _json

    from ..linkedin import get_linkedin_client

    client = get_linkedin_client()
    account_id = ""
    try:
        from ..config import get_config
        cfg = get_config()
        account_id = cfg.get("account_id", "")
    except Exception:
        pass
    if not account_id:
        try:
            accounts = await client.list_accounts()
            if accounts:
                account_id = accounts[0].get("id", "")
        except Exception:
            pass
    if not account_id:
        return "No LinkedIn account configured. Run setup_profile() first."

    targets: list[dict] = []

    if contact_id:
        gc = await db.get_global_contact(contact_id)
        if not gc:
            return f"Contact not found: {contact_id}"
        targets = [gc]
    elif query:
        results = await db.search_global_contacts(query=query, limit=limit or 10)
        # Filter to those missing enrichment
        targets = [r for r in results if not r.get("profile_json")]
        if not targets:
            return f"No un-enriched contacts found matching \"{query}\". They may already be enriched."
    else:
        return "Provide contact_id for single enrichment, or query for batch enrichment."

    enriched_count = 0
    lines = ["Enrichment Results", "=" * 40, ""]

    for gc in targets:
        lid = gc.get("linkedin_id") or ""
        # Try to extract provider_id from existing profile_json
        if gc.get("profile_json") and not contact_id:
            continue  # Skip already enriched (unless explicitly requested by contact_id)
        if not lid:
            try:
                pj = _json.loads(gc.get("profile_json") or "{}")
                lid = pj.get("provider_id", "")
            except (ValueError, TypeError):
                pass
        if not lid:
            lines.append(f"  Skipped {gc.get('name', '?')}: no LinkedIn ID")
            continue

        try:
            profile = await client.get_profile(account_id, lid)
            if not profile or not isinstance(profile, dict):
                lines.append(f"  Skipped {gc.get('name', '?')}: profile not found")
                continue

            profile_json = _json.dumps(profile)
            title = profile.get("title") or profile.get("headline") or gc.get("title", "")
            company = profile.get("company") or gc.get("company", "")
            location = profile.get("location") or gc.get("location", "")

            await db.upsert_global_contact(
                linkedin_id=lid,
                name=gc.get("name") or profile.get("name", ""),
                title=title,
                company=company,
                linkedin_url=gc.get("linkedin_url", ""),
                location=location,
                profile_json=profile_json,
                source="enrichment",
            )

            # Fetch posts
            posts_count = 0
            try:
                from ..db.post_queries import upsert_post
                posts = await client.get_user_posts(account_id, lid, limit=10)
                if posts and isinstance(posts, list):
                    for post in posts:
                        pid = post.get("id", "")
                        txt = post.get("text", "")
                        if pid and txt:
                            await run_db(upsert_post, pid,
                                author_linkedin_id=lid,
                                author_name=gc.get("name", ""),
                                text=txt[:2000],
                                metrics_json=_json.dumps(post.get("metrics", {})),
                                source="enrichment",)
                            posts_count += 1
            except Exception:
                pass

            enriched_count += 1
            name = gc.get("name") or profile.get("name", "?")
            lines.append(f"  {enriched_count}. {name}")
            if title:
                lines.append(f"     Title: {title}")
            if company:
                lines.append(f"     Company: {company}")
            if location:
                lines.append(f"     Location: {location}")
            skills = profile.get("skills", [])
            if skills:
                skill_names = [s.get("name", s) if isinstance(s, dict) else str(s) for s in skills[:5]]
                lines.append(f"     Skills: {', '.join(skill_names)}")
            if posts_count:
                lines.append(f"     Posts fetched: {posts_count}")
            lines.append("")

        except Exception as e:
            lines.append(f"  Failed {gc.get('name', '?')}: {e}")

        # Rate limit
        if len(targets) > 1:
            import asyncio
            await asyncio.sleep(1.0)

    await client.close()

    lines.append(f"Enriched {enriched_count}/{len(targets)} contacts.")
    if enriched_count > 0:
        lines.append("Use contacts(action='view', contact_id='...') to see full enriched profiles.")

    return "\n".join(lines)


# ──────────────────────────────────────────────
# Duplicate detection & merging handlers
# ──────────────────────────────────────────────

def _handle_find_duplicates() -> str:
    """Find duplicate global contacts that share the same provider_id."""
    dupes = find_duplicate_global_contacts()
    if not dupes:
        return "No duplicate contacts found."

    lines = [f"Found **{len(dupes)} duplicate contact pair(s)**:\n"]
    for d in dupes:
        lines.append(f"  - **{d['keep_name']}** (keep: `{d['keep_id'][:8]}…`)")
        lines.append(f"    ↔ **{d['merge_name']}** (merge: `{d['merge_id'][:8]}…`)")
        lines.append(f"    provider_id: `{d['provider_id']}`")
        lines.append("")

    lines.append("To merge: `contacts(action='merge', contact_id='<keep_id>', query='<merge_id>')`")
    return "\n".join(lines)


def _handle_merge(keep_id: str, merge_id: str) -> str:
    """Merge two global contact records."""
    if not keep_id or not merge_id:
        return "Both contact_id (keep) and query (merge) are required.\n\nUsage: `contacts(action='merge', contact_id='<keep_id>', query='<merge_id>')`"

    if keep_id == merge_id:
        return "Cannot merge a contact with itself."

    success = merge_global_contacts(keep_id, merge_id)
    if success:
        return f"Merged contact `{merge_id[:8]}…` into `{keep_id[:8]}…` successfully.\n\nAll campaign history has been consolidated."
    else:
        return "Merge failed — one or both contact IDs not found. Use `contacts(action='find_duplicates')` to find valid pairs."
