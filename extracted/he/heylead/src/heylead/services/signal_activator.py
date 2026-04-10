"""Signal activator — converts high-scoring signals into outreach actions.

The core engine that turns signal intelligence into revenue. Processes
classified signals and triggers contextual outreach based on composite
score thresholds:

Tier 1 (score >= 0.7 + outreach intent): Auto-create contact + outreach
Tier 2 (score >= 0.5 + boost intent): Add to best-matching campaign
Tier 3 (score >= 0.3, existing contact): Boost engagement priority
Below threshold: Mark as actioned, no outreach

All signal-triggered outreaches carry signal context that gets injected
into message generation for natural, contextual personalization.

Runs every 15 minutes via the scheduler.
"""

from __future__ import annotations

import json
import logging
import time
from typing import Any

from ..db.async_bridge import run_db

logger = logging.getLogger(__name__)

# ── Runtime threshold override cache (DB-backed, 5-min TTL) ──
_threshold_override_cache: dict[str, float] = {}
_threshold_override_ts: float = 0.0
_THRESHOLD_CACHE_TTL = 300


def _get_effective_threshold(name: str, default: float) -> float:
    """DB override > constant. Cached with 5-min TTL."""
    global _threshold_override_cache, _threshold_override_ts
    now = time.time()
    if now - _threshold_override_ts > _THRESHOLD_CACHE_TTL:
        try:
            from ..db.signal_queries import get_threshold_overrides
            _threshold_override_cache = get_threshold_overrides()
        except Exception:
            pass
        _threshold_override_ts = now
    return _threshold_override_cache.get(name, default)


def invalidate_threshold_cache() -> None:
    """Force cache refresh on next call."""
    global _threshold_override_ts
    _threshold_override_ts = 0.0


async def activate_pending_signals() -> str:
    """Process classified signals and trigger appropriate outreach actions.

    For each classified signal:
    1. Compute prospect-level composite score
    2. Route by score tier → create outreach / add to campaign / boost priority
    3. Build signal context for message injection
    4. Update signal status to 'actioned' with action_taken

    Returns summary string.
    """
    from ..constants import (
        SIGNAL_AUTO_OUTREACH_THRESHOLD,
        SIGNAL_BEHAVIORAL_AUTO_THRESHOLD,
        SIGNAL_BEHAVIORAL_TYPES,
        SIGNAL_BOOST_INTENTS,
        SIGNAL_BOOST_THRESHOLD,
        SIGNAL_HOT_SKIP_WARMUP_THRESHOLD,
        SIGNAL_ICP_MATCH_THRESHOLD,
        SIGNAL_ICP_MIN_OVERLAP,
        SIGNAL_OUTREACH_INTENTS,
        SIGNAL_STATUS_CLASSIFIED,
        SIGNAL_WARM_THRESHOLD,
    )
    from ..services.icp_match_scorer import compute_icp_match
    from ..db.queries import (
        create_outreach,
        list_campaigns,
        save_contact,
        save_contact_analysis,
        update_contact,
    )
    from ..db.signal_queries import (
        get_contact_by_linkedin_id,
        list_intent_events,
        list_signals,
        update_signal,
        upsert_signal_account,
    )
    from ..services.signal_scorer import (
        compute_prospect_signal_score,
        detect_all_compound_intents,
    )

    now = int(time.time())

    # Run compound intent detection before activation so stacked signals
    # produce intent events that inform scoring in the loop below.
    try:
        compound_summary = await run_db(detect_all_compound_intents)
        logger.debug("Compound intent pass: %s", compound_summary)
    except Exception as exc:
        logger.warning("Compound intent detection failed: %s", exc)

    # Fetch classified signals (not yet actioned)
    signals = await run_db(list_signals, status=SIGNAL_STATUS_CLASSIFIED, limit=30)

    # Fallback: pick up stale "new" signals (>30 min old) if classification missed them
    if not signals:
        from ..constants import SIGNAL_STATUS_NEW
        stale_cutoff = now - 1800  # 30 minutes
        new_signals = await run_db(list_signals, status=SIGNAL_STATUS_NEW, limit=15)
        signals = [
            s for s in new_signals
            if (s.get("detected_at", 0) or 0) < stale_cutoff
        ]
        if signals:
            logger.info(
                "Processing %d stale 'new' signals (classification may have failed)",
                len(signals),
            )

    if not signals:
        return "No signals to activate."

    # Get active campaigns for ICP matching
    active_campaigns = await run_db(list_campaigns, status="active")

    # Track results
    outreaches_created = 0
    campaigns_added = 0
    priorities_boosted = 0
    below_threshold = 0
    skipped = 0

    # Track linkedin_ids we've already processed in this batch (dedup)
    processed_ids: set[str] = set()

    for sig in signals:
        signal_id = sig["id"]
        linkedin_id = sig.get("linkedin_id", "")
        intent = sig.get("intent", "unknown")
        confidence = sig.get("confidence", 0) or 0

        if not linkedin_id:
            # Can't create outreach without LinkedIn identifier
            await run_db(update_signal,
                signal_id,
                status="actioned",
                action_taken="no_linkedin_id",
                actioned_at=now,
            )
            skipped += 1
            continue

        # Dedup within this batch
        if linkedin_id in processed_ids:
            await run_db(update_signal,
                signal_id,
                status="actioned",
                action_taken="batch_dedup",
                actioned_at=now,
            )
            skipped += 1
            continue
        processed_ids.add(linkedin_id)

        # Compute prospect-level composite score
        score_result = await run_db(compute_prospect_signal_score, linkedin_id, now)
        composite_score = score_result.get("composite_score", 0)

        # Apply compound intent boost: if the prospect has active intent events,
        # use the highest compound event score as a floor for the composite score.
        try:
            intent_events = await run_db(list_intent_events, linkedin_id=linkedin_id, active_only=True)
            if intent_events:
                best_intent = max(ie.get("composite_score", 0) for ie in intent_events)
                if best_intent > composite_score:
                    logger.debug(
                        "Compound intent boost for %s: %.2f → %.2f (%s)",
                        linkedin_id, composite_score, best_intent,
                        intent_events[0].get("event_type", ""),
                    )
                    composite_score = best_intent
        except Exception as exc:
            logger.debug("Intent event lookup failed for %s: %s", linkedin_id, exc)

        # Check if this person is already in a campaign
        existing_contact = await run_db(get_contact_by_linkedin_id, linkedin_id)

        # Build signal context for message injection
        signal_context = _build_signal_context(sig)

        # Skip signals where the engagement hook is empty — means we
        # couldn't build a specific enough message (e.g. company_change
        # with no new_company metadata).  Avoids embarrassing generics.
        if not signal_context.get("engagement_hook"):
            angle = signal_context.get("signal_angle", "")
            if angle in (
                "congrats_new_company",
                "congrats_promotion",
                "congrats_reconnect",
            ):
                await run_db(update_signal,
                    signal_id,
                    status="dismissed",
                    action_taken="insufficient_metadata",
                    actioned_at=now,
                )
                skipped += 1
                logger.info(
                    "Skipping %s signal for %s: no engagement hook (angle=%s)",
                    sig.get("signal_type"), sig.get("prospect_name"), angle,
                )
                continue

        # Enrich context with compound intent if available
        try:
            if intent_events:
                top_event = intent_events[0]
                signal_context["compound_intent"] = {
                    "event_type": top_event.get("event_type", ""),
                    "score": top_event.get("composite_score", 0),
                    "signal_types": top_event.get("signal_types_list", []),
                }
                # Provide richer engagement hook based on compound pattern
                compound_hook = _build_compound_hook(top_event)
                if compound_hook:
                    signal_context["engagement_hook"] = compound_hook
        except Exception:
            pass  # intent_events may not be defined if lookup failed

        # ── Hot Signal Fast-Track ──
        # Certain signal+intent combos are so strong they should trigger outreach
        # regardless of composite score. E.g. a CTO posting "leaving Salesloft".
        signal_type = sig.get("signal_type", "")
        metadata = _parse_metadata(sig)

        if signal_type == "competitor_mention":
            mention_ctx = metadata.get("mention_context", "general")
            if mention_ctx in ("switching_from", "evaluating", "complaint"):
                composite_score = max(composite_score, SIGNAL_AUTO_OUTREACH_THRESHOLD)
                logger.info(
                    "Hot fast-track: competitor %s (%s) for %s",
                    metadata.get("competitor_name", "?"), mention_ctx,
                    sig.get("prospect_name", "Unknown"),
                )
        elif signal_type in ("company_change", "promotion") and intent in SIGNAL_OUTREACH_INTENTS:
            composite_score = max(composite_score, SIGNAL_AUTO_OUTREACH_THRESHOLD)
        elif signal_type == "headline_intent":
            intent_cats = metadata.get("intent_categories", [])
            if any(cat in ("hiring", "evaluating") for cat in intent_cats):
                composite_score = max(composite_score, SIGNAL_AUTO_OUTREACH_THRESHOLD)
        # Backward compat for old job_change signals still in DB
        elif signal_type == "job_change" and intent in SIGNAL_OUTREACH_INTENTS:
            composite_score = max(composite_score, SIGNAL_AUTO_OUTREACH_THRESHOLD)
        elif intent == "buying_signal" and confidence >= 0.75:
            composite_score = max(composite_score, SIGNAL_AUTO_OUTREACH_THRESHOLD)

        # ── Experiment variant assignment ──
        # If an active signal threshold experiment exists for this campaign,
        # override thresholds based on assigned variant (control/treatment).
        exp_auto_threshold = SIGNAL_AUTO_OUTREACH_THRESHOLD
        exp_boost_threshold = SIGNAL_BOOST_THRESHOLD
        exp_warm_threshold = SIGNAL_WARM_THRESHOLD
        try:
            campaign_id_for_exp = (
                existing_contact.get("campaign_id")
                if existing_contact
                else sig.get("campaign_id")
            )
            if campaign_id_for_exp:
                variant, overrides = await run_db(_get_experiment_thresholds,
                    campaign_id_for_exp, signal_id,
                )
                if overrides:
                    exp_auto_threshold = overrides.get(
                        "auto_outreach", exp_auto_threshold,
                    )
                    exp_boost_threshold = overrides.get(
                        "boost", exp_boost_threshold,
                    )
                    exp_warm_threshold = overrides.get(
                        "warm", exp_warm_threshold,
                    )
                    # Tag signal with experiment variant
                    await run_db(update_signal, signal_id, experiment_variant=variant)
        except Exception:
            pass  # Experiment failure doesn't block activation

        # ── Tier 1: Auto-outreach (score >= threshold + outreach intent) ──
        if (
            composite_score >= exp_auto_threshold
            and intent in SIGNAL_OUTREACH_INTENTS
        ):
            if existing_contact:
                # Already in a campaign — boost priority instead of creating duplicate
                await run_db(_boost_existing_contact, existing_contact, signal_context, composite_score, now)
                await run_db(update_signal,
                    signal_id,
                    status="actioned",
                    action_taken="priority_boosted_existing",
                    actioned_at=now,
                )
                priorities_boosted += 1
            else:
                # Find best-matching campaign via ICP overlap
                campaign_id = _match_best_campaign(sig, active_campaigns)
                if not campaign_id:
                    await run_db(update_signal,
                        signal_id,
                        status="actioned",
                        action_taken="no_matching_campaign",
                        actioned_at=now,
                    )
                    skipped += 1
                    continue

                # ICP validation: score prospect against campaign ICP
                matched_camp = next(
                    (c for c in active_campaigns if c["id"] == campaign_id), None
                )
                icp_score = 0.3  # Neutral default when no campaign ICP
                if matched_camp:
                    icp_result = compute_icp_match(
                        {
                            "title": sig.get("prospect_title") or "",
                            "company": _extract_company(sig),
                            "linkedin_id": linkedin_id,
                        },
                        matched_camp.get("icp_json"),
                    )
                    icp_score = icp_result["icp_match_score"]
                    if icp_score < SIGNAL_ICP_MATCH_THRESHOLD:
                        await run_db(update_signal,
                            signal_id,
                            status="actioned",
                            action_taken="icp_mismatch",
                            actioned_at=now,
                        )
                        skipped += 1
                        logger.debug(
                            "Signal %s: ICP mismatch (score=%.2f) for %s",
                            signal_id, icp_score, sig.get("prospect_name"),
                        )
                        continue

                # Create contact + outreach (fit_score = ICP match, not signal strength)
                contact_id = await run_db(save_contact,
                    campaign_id=campaign_id,
                    name=sig.get("prospect_name") or "Unknown",
                    title=sig.get("prospect_title") or "",
                    company=_extract_company(sig),
                    linkedin_url=f"https://www.linkedin.com/in/{linkedin_id}",
                    linkedin_id=linkedin_id,
                    fit_score=max(icp_score, 0.1),
                )

                # Set contact source to signal_discovery
                try:
                    def _set_source(cid):
                        from ..db.schema import get_db
                        db = get_db()
                        db.execute(
                            "UPDATE contacts SET source = ? WHERE id = ?",
                            ("signal_discovery", cid),
                        )
                        db.commit()
                        db.close()
                    await run_db(_set_source, contact_id)
                except Exception:
                    pass

                # Save signal context to analysis_json for message generation
                await run_db(save_contact_analysis, contact_id, {
                    "signal_context": signal_context,
                    "summary": signal_context.get("engagement_hook", ""),
                    "pain_points": signal_context.get("pain_points", []),
                })

                # Determine if hot signal should skip warm-up
                next_action = None
                if composite_score >= SIGNAL_HOT_SKIP_WARMUP_THRESHOLD:
                    next_action = "signal_hot_skip_warmup"

                outreach_id = await run_db(create_outreach,
                    campaign_id=campaign_id,
                    contact_id=contact_id,
                    status="pending",
                    signal_id=signal_id,
                )

                # Mark hot skip in outreach next_action
                if next_action:
                    from ..db.queries import update_outreach
                    await run_db(update_outreach, outreach_id, next_action=next_action)

                # Update signal account
                await run_db(upsert_signal_account,
                    linkedin_id=linkedin_id,
                    prospect_name=sig.get("prospect_name"),
                    company=_extract_company(sig),
                )

                await run_db(update_signal,
                    signal_id,
                    status="actioned",
                    action_taken="outreach_created",
                    actioned_at=now,
                )
                outreaches_created += 1

                logger.info(
                    "Signal activation: created outreach for %s (score=%.2f, signal=%s%s)",
                    sig.get("prospect_name", "Unknown"),
                    composite_score,
                    sig.get("signal_type", ""),
                    " [HOT-SKIP]" if next_action else "",
                )

        # ── Tier 1b: Behavioral signals (profile_view, company_follower, etc.)
        # These express direct interest in YOU — bypass text-intent gate when ICP-matched.
        # Use lower threshold since behavioral signals inherently have weaker scoring
        # (no text content → confidence was historically low).
        elif (
            composite_score >= SIGNAL_BEHAVIORAL_AUTO_THRESHOLD
            and sig.get("signal_type") in SIGNAL_BEHAVIORAL_TYPES
            and not existing_contact
        ):
            campaign_id = _match_best_campaign(sig, active_campaigns)
            if not campaign_id:
                await run_db(update_signal,
                    signal_id,
                    status="actioned",
                    action_taken="no_matching_campaign",
                    actioned_at=now,
                )
                skipped += 1
                continue

            # ICP validation — behavioral signals need stronger ICP match to compensate
            # for weaker intent signal.
            from ..constants import SIGNAL_BEHAVIORAL_ICP_THRESHOLD
            matched_camp = next(
                (c for c in active_campaigns if c["id"] == campaign_id), None
            )
            icp_score = 0.0
            if matched_camp:
                icp_result = compute_icp_match(
                    {
                        "title": sig.get("prospect_title") or "",
                        "company": _extract_company(sig),
                        "linkedin_id": linkedin_id,
                    },
                    matched_camp.get("icp_json"),
                )
                icp_score = icp_result["icp_match_score"]

            if icp_score < SIGNAL_BEHAVIORAL_ICP_THRESHOLD:
                await run_db(update_signal,
                    signal_id,
                    status="actioned",
                    action_taken="behavioral_icp_mismatch",
                    actioned_at=now,
                )
                skipped += 1
                continue

            # Create outreach
            contact_id = await run_db(save_contact,
                campaign_id=campaign_id,
                name=sig.get("prospect_name") or "Unknown",
                title=sig.get("prospect_title") or "",
                company=_extract_company(sig),
                linkedin_url=f"https://www.linkedin.com/in/{linkedin_id}",
                linkedin_id=linkedin_id,
                fit_score=max(icp_score, 0.1),
            )

            await run_db(save_contact_analysis, contact_id, {
                "signal_context": signal_context,
                "summary": signal_context.get("engagement_hook", ""),
                "pain_points": signal_context.get("pain_points", []),
            })

            outreach_id = await run_db(create_outreach,
                campaign_id=campaign_id,
                contact_id=contact_id,
                status="pending",
                signal_id=signal_id,
            )

            await run_db(upsert_signal_account,
                linkedin_id=linkedin_id,
                prospect_name=sig.get("prospect_name"),
                company=_extract_company(sig),
            )

            await run_db(update_signal,
                signal_id,
                status="actioned",
                action_taken="behavioral_outreach_created",
                actioned_at=now,
            )
            outreaches_created += 1

            logger.info(
                "Signal activation: behavioral outreach for %s (score=%.2f, icp=%.2f, signal=%s)",
                sig.get("prospect_name", "Unknown"),
                composite_score,
                icp_score,
                sig.get("signal_type", ""),
            )

        # ── Tier 2: Add to campaign (score >= boost threshold + boost intent) ──
        elif (
            composite_score >= exp_boost_threshold
            and intent in SIGNAL_BOOST_INTENTS
        ):
            if existing_contact:
                await run_db(_boost_existing_contact, existing_contact, signal_context, composite_score, now)
                await run_db(update_signal,
                    signal_id,
                    status="actioned",
                    action_taken="priority_boosted_existing",
                    actioned_at=now,
                )
                priorities_boosted += 1
            else:
                campaign_id = _match_best_campaign(sig, active_campaigns)
                if not campaign_id:
                    await run_db(update_signal,
                        signal_id,
                        status="actioned",
                        action_taken="no_matching_campaign",
                        actioned_at=now,
                    )
                    skipped += 1
                    continue

                # ICP validation for Tier 2 signals
                matched_camp = next(
                    (c for c in active_campaigns if c["id"] == campaign_id), None
                )
                icp_score = 0.3  # Neutral default when no campaign ICP
                if matched_camp:
                    icp_result = compute_icp_match(
                        {
                            "title": sig.get("prospect_title") or "",
                            "company": _extract_company(sig),
                            "linkedin_id": linkedin_id,
                        },
                        matched_camp.get("icp_json"),
                    )
                    icp_score = icp_result["icp_match_score"]
                    if icp_score < SIGNAL_ICP_MATCH_THRESHOLD:
                        await run_db(update_signal,
                            signal_id,
                            status="actioned",
                            action_taken="icp_mismatch",
                            actioned_at=now,
                        )
                        skipped += 1
                        continue

                # fit_score = ICP match, not signal strength
                contact_id = await run_db(save_contact,
                    campaign_id=campaign_id,
                    name=sig.get("prospect_name") or "Unknown",
                    title=sig.get("prospect_title") or "",
                    company=_extract_company(sig),
                    linkedin_url=f"https://www.linkedin.com/in/{linkedin_id}",
                    linkedin_id=linkedin_id,
                    fit_score=max(icp_score, 0.1),
                )

                try:
                    def _set_source(cid):
                        from ..db.schema import get_db
                        db = get_db()
                        db.execute(
                            "UPDATE contacts SET source = ? WHERE id = ?",
                            ("signal_discovery", cid),
                        )
                        db.commit()
                        db.close()
                    await run_db(_set_source, contact_id)
                except Exception:
                    pass

                await run_db(save_contact_analysis, contact_id, {
                    "signal_context": signal_context,
                    "summary": signal_context.get("engagement_hook", ""),
                    "pain_points": signal_context.get("pain_points", []),
                })

                await run_db(
                    create_outreach,
                    campaign_id=campaign_id,
                    contact_id=contact_id,
                    status="pending",
                    signal_id=signal_id,
                )

                await run_db(upsert_signal_account,
                    linkedin_id=linkedin_id,
                    prospect_name=sig.get("prospect_name"),
                    company=_extract_company(sig),
                )

                await run_db(update_signal,
                    signal_id,
                    status="actioned",
                    action_taken="campaign_added",
                    actioned_at=now,
                )
                campaigns_added += 1

                logger.info(
                    "Signal activation: added %s to campaign (score=%.2f, signal=%s)",
                    sig.get("prospect_name", "Unknown"),
                    composite_score,
                    sig.get("signal_type", ""),
                )

        # ── Tier 3: Boost existing (score >= warm threshold, already in campaign) ──
        elif composite_score >= exp_warm_threshold and existing_contact:
            await run_db(_boost_existing_contact, existing_contact, signal_context, composite_score, now)
            await run_db(update_signal,
                signal_id,
                status="actioned",
                action_taken="priority_boosted",
                actioned_at=now,
            )
            priorities_boosted += 1

        # ── Below threshold ──
        else:
            await run_db(update_signal,
                signal_id,
                status="actioned",
                action_taken="below_threshold",
                actioned_at=now,
            )
            below_threshold += 1

    # Build summary
    parts = []
    if outreaches_created:
        parts.append(f"{outreaches_created} outreaches created")
    if campaigns_added:
        parts.append(f"{campaigns_added} added to campaigns")
    if priorities_boosted:
        parts.append(f"{priorities_boosted} priorities boosted")
    if below_threshold:
        parts.append(f"{below_threshold} below threshold")
    if skipped:
        parts.append(f"{skipped} skipped")

    if not parts:
        return "No signals processed."

    return f"Signal activation: {', '.join(parts)}"


def _build_signal_context(signal: dict[str, Any]) -> dict[str, Any]:
    """Build signal context dict for injection into prospect_analysis.

    This dict gets stored in contact.analysis_json and is picked up
    by `_build_intelligence_text()` in message_generator.py to create
    natural, contextual outreach messages.
    """
    signal_type = signal.get("signal_type", "unknown")
    content = signal.get("content", "")
    intent = signal.get("intent", "unknown")
    detected_at = signal.get("detected_at", 0)
    metadata = _parse_metadata(signal)

    # Determine signal angle
    angle = _get_signal_angle(signal_type, intent, metadata)

    # Build engagement hook based on signal type
    hook = _build_engagement_hook(signal_type, content, metadata, angle)

    # Extract pain points from classifier output
    pain_points = []
    reasoning = signal.get("reasoning", "")
    if reasoning:
        # Classifier may have embedded pain points in reasoning
        pain_points = metadata.get("pain_points_detected", [])

    # Time ago
    now = int(time.time())
    age_seconds = max(0, now - detected_at) if detected_at else 0
    if age_seconds < 3600:
        detected_ago = f"{age_seconds // 60} minutes ago"
    elif age_seconds < 86400:
        detected_ago = f"{age_seconds // 3600} hours ago"
    else:
        detected_ago = f"{age_seconds // 86400} days ago"

    return {
        "signal_type": signal_type,
        "signal_summary": content[:200] if content else "",
        "engagement_hook": hook,
        "signal_angle": angle,
        "detected_ago": detected_ago,
        "pain_points": pain_points,
        "keywords_matched": metadata.get("keywords_matched", []),
        "DO_NOT": (
            "Don't quote their posts directly. "
            "Don't mention you 'saw' or 'noticed' or 'came across'. "
            "Reference the topic naturally as a shared interest."
        ),
    }


def _get_signal_angle(
    signal_type: str,
    intent: str,
    metadata: dict[str, Any],
) -> str:
    """Determine the outreach angle based on signal characteristics."""
    if signal_type == "company_change":
        return "congrats_new_company"

    if signal_type == "promotion":
        return "congrats_promotion"

    if signal_type == "headline_intent":
        intent_cats = metadata.get("intent_categories", [])
        if "hiring" in intent_cats:
            return "hiring_partnership"
        if "evaluating" in intent_cats:
            return "solution_alignment"
        if "building" in intent_cats:
            return "builder_connection"
        return "contextual_reference"

    if signal_type == "headline_change":
        return "contextual_reference"

    # Backward compat for old job_change signals
    if signal_type == "job_change":
        return "congrats_reconnect"

    if signal_type == "competitor_mention":
        mention_context = metadata.get("mention_context", "general")
        if mention_context in ("switching_from", "evaluating", "complaint"):
            return "competitive_displacement"
        return "contextual_reference"

    if signal_type == "keyword_mention" and intent == "pain_point":
        return "pain_point_alignment"

    if signal_type == "prospect_post" and intent == "buying_signal":
        return "buying_intent_response"

    if signal_type == "profile_view":
        # Phase 4: ICP-matching viewers get a more targeted angle
        if metadata.get("is_icp_match"):
            return "icp_profile_viewer"
        return "reciprocal_interest"

    if signal_type == "commenter_match":
        return "shared_engagement"

    if signal_type == "hiring_surge":
        return "growth_partnership"

    if signal_type in ("funding_event", "news_event"):
        return "milestone_congrats"

    # Granular news signal angles (Phase 1)
    if signal_type == "news_funding":
        return "congrats_funding"

    if signal_type == "news_acquisition":
        return "congrats_acquisition"

    if signal_type == "news_exec_hire":
        return "congrats_exec_hire"

    if signal_type == "news_expansion":
        return "congrats_expansion"

    if signal_type == "news_product_launch":
        return "congrats_product_launch"

    if signal_type == "news_layoffs":
        return "empathy_restructuring"

    # Company page engagement angles (Phase 2)
    if signal_type == "company_post_comment":
        return "company_page_engagement"

    if signal_type == "company_post_reaction":
        return "company_page_engagement"

    if signal_type == "company_follower":
        return "company_follower_outreach"

    # Website visitor tracking angles (Phase 3)
    if signal_type == "website_high_intent":
        return "website_high_intent_outreach"

    if signal_type == "website_visit":
        return "website_visitor_outreach"

    return "contextual_reference"


def _build_engagement_hook(
    signal_type: str,
    content: str,
    metadata: dict[str, Any],
    angle: str,
) -> str:
    """Build a suggested engagement hook for the message generator.

    Returns a natural conversation starter that references the signal
    without being creepy.
    """
    if angle == "congrats_new_company":
        new_title = metadata.get("new_title", "")
        new_company = metadata.get("new_company", "")
        if new_title and new_company:
            return f"Congrats on the {new_title} role at {new_company}!"
        elif new_company:
            return f"Congrats on joining {new_company}!"
        # No specific company/title → suppress (avoid embarrassing generic)
        return ""

    if angle == "congrats_promotion":
        new_title = metadata.get("new_title", "")
        company = metadata.get("company", "")
        if new_title and company:
            return f"Congrats on the {new_title} promotion at {company}!"
        elif new_title:
            return f"Congrats on the promotion to {new_title}!"
        # No specific title → suppress
        return ""

    if angle == "hiring_partnership":
        return "Sounds like you're growing the team — exciting times!"

    if angle == "solution_alignment":
        return "It sounds like you're rethinking your approach — always a great time to explore options"

    if angle == "builder_connection":
        return "Love the builder energy — would be great to connect"

    # Backward compat for old job_change signals
    if angle == "congrats_reconnect":
        new_title = metadata.get("new_title", "")
        new_company = metadata.get("new_company", "")
        if new_title and new_company:
            return f"Congrats on the {new_title} role at {new_company}!"
        elif new_company:
            return f"Congrats on joining {new_company}!"
        # No specific metadata → suppress
        return ""

    if angle == "competitive_displacement":
        competitor = metadata.get("competitor_name", "")
        if competitor:
            return f"Sounds like you're exploring alternatives to {competitor}"
        return "Sounds like you're evaluating new solutions"

    if angle == "pain_point_alignment":
        keyword = metadata.get("keyword", "")
        if keyword:
            return f"Noticed the conversation around {keyword} — it's a challenge many teams face"
        return "Your perspective on this challenge resonates"

    if angle == "buying_intent_response":
        # Extract a brief topic from content
        topic = _extract_topic(content)
        if topic:
            return f"Your take on {topic} aligns with what we're seeing in the market"
        return "Your insights on this topic really resonate"

    if angle == "icp_profile_viewer":
        company = metadata.get("viewer_company", "")
        if company:
            return f"Noticed you checked us out — {company} seems like a great fit"
        return "Noticed you've been checking us out — would love to connect"

    if angle == "reciprocal_interest":
        return "We seem to be in similar circles"

    if angle == "shared_engagement":
        return "Great discussion — your perspective stood out"

    if angle == "growth_partnership":
        company = metadata.get("company", "")
        if company:
            return f"Exciting growth at {company}!"
        return "Impressive team growth!"

    if angle == "milestone_congrats":
        return "Congrats on the milestone!"

    # Granular news engagement hooks (Phase 1)
    if angle == "congrats_funding":
        company = metadata.get("company_name", "")
        if company:
            return f"Congrats to {company} on the funding round — exciting times ahead!"
        return "Congrats on the funding round!"

    if angle == "congrats_acquisition":
        company = metadata.get("company_name", "")
        if company:
            return f"Big moves at {company} — transitions like this open up interesting opportunities"
        return "Big moves — transitions like this open up interesting opportunities"

    if angle == "congrats_exec_hire":
        company = metadata.get("company_name", "")
        if company:
            return f"Exciting leadership changes at {company} — new energy always drives fresh thinking"
        return "New leadership always brings fresh perspective"

    if angle == "congrats_expansion":
        company = metadata.get("company_name", "")
        if company:
            return f"Great to see {company} expanding — growth mode is always energizing"
        return "Growth mode is always energizing!"

    if angle == "congrats_product_launch":
        company = metadata.get("company_name", "")
        if company:
            return f"Saw {company}'s latest launch — interesting direction"
        return "Interesting product direction!"

    if angle == "empathy_restructuring":
        company = metadata.get("company_name", "")
        if company:
            return f"Transitions at {company} can be challenging — hope things stabilize soon"
        return "Transitions can be tough — hope things settle well"

    # Company page engagement hooks (Phase 2)
    if angle == "company_page_engagement":
        post_text = metadata.get("post_text", "")
        topic = _extract_topic(post_text) if post_text else ""
        if topic:
            return f"Your thoughts on {topic} resonated — great perspective"
        return "Great engagement on our recent post — would love to connect"

    if angle == "company_follower_outreach":
        return "Thanks for following us — always great to connect with people in the space"

    # Website visitor tracking hooks (Phase 3)
    if angle == "website_high_intent_outreach":
        page = metadata.get("page_url", "")
        company = metadata.get("company_name", "")
        if company:
            return f"Noticed {company} has been exploring our solutions — would love to chat"
        return "Looks like you've been checking us out — happy to answer any questions"

    if angle == "website_visitor_outreach":
        company = metadata.get("company_name", "")
        if company:
            return f"I see {company} in our space — thought it'd be great to connect"
        return "Came across your profile and thought we might have some synergies"

    # Default contextual reference
    topic = _extract_topic(content)
    if topic:
        return f"Your work around {topic} caught my attention"
    return "Your background is impressive"


def _extract_topic(content: str) -> str:
    """Extract a brief topic phrase from signal content.

    Returns first meaningful phrase (up to 50 chars) or empty string.
    """
    if not content:
        return ""
    # Take first sentence or 50 chars, whichever is shorter
    content = content.strip()
    # Find first sentence boundary
    for delim in [".", "!", "?", "\n"]:
        idx = content.find(delim)
        if 10 < idx < 80:
            return content[:idx].strip()
    # Fallback: first 50 chars at word boundary
    if len(content) > 50:
        truncated = content[:50]
        last_space = truncated.rfind(" ")
        if last_space > 20:
            return truncated[:last_space].strip()
    return content[:50].strip() if content else ""


def _match_best_campaign(
    signal: dict[str, Any],
    campaigns: list[dict[str, Any]],
) -> str | None:
    """Find the best-matching campaign for a signal based on ICP overlap.

    Uses keyword overlap between signal content/metadata and campaign ICP.
    Falls back to the most recent autopilot campaign if no strong match.
    """
    from ..constants import SIGNAL_ICP_MIN_OVERLAP

    if not campaigns:
        return None

    content = (signal.get("content") or "").lower()
    prospect_title = (signal.get("prospect_title") or "").lower()
    metadata = _parse_metadata(signal)
    keyword = (metadata.get("keyword") or "").lower()

    # Combine text for matching
    match_text = f"{content} {prospect_title} {keyword}"

    best_campaign_id = None
    best_overlap = 0.0

    for camp in campaigns:
        icp_raw = camp.get("icp_json", "")
        if not icp_raw:
            continue

        try:
            icp_data = json.loads(icp_raw) if isinstance(icp_raw, str) else icp_raw
        except (json.JSONDecodeError, TypeError):
            continue

        # Extract keywords from ICP
        icp_keywords: set[str] = set()
        if isinstance(icp_data, dict):
            # Single ICP
            _extract_icp_keywords(icp_data, icp_keywords)
        elif isinstance(icp_data, list):
            # Multiple personas
            for persona in icp_data:
                if isinstance(persona, dict):
                    _extract_icp_keywords(persona, icp_keywords)

        if not icp_keywords:
            continue

        # Compute overlap
        matched = sum(1 for kw in icp_keywords if kw.lower() in match_text)
        overlap = matched / len(icp_keywords) if icp_keywords else 0

        if overlap > best_overlap:
            best_overlap = overlap
            best_campaign_id = camp["id"]

    # If overlap meets minimum, use it
    if best_campaign_id and best_overlap >= SIGNAL_ICP_MIN_OVERLAP:
        return best_campaign_id

    # Fallback: most recent autopilot campaign
    autopilot_campaigns = [c for c in campaigns if c.get("mode") == "autopilot"]
    if autopilot_campaigns:
        # Sort by created_at descending
        autopilot_campaigns.sort(key=lambda c: c.get("created_at", 0), reverse=True)
        return autopilot_campaigns[0]["id"]

    # Last resort: any active campaign
    return campaigns[0]["id"] if campaigns else None


def _extract_icp_keywords(icp_data: dict[str, Any], keywords: set[str]) -> None:
    """Extract searchable keywords from an ICP persona dict."""
    # Pain points
    for pp in icp_data.get("pain_points", []):
        if isinstance(pp, str):
            keywords.add(pp.lower())
        elif isinstance(pp, dict):
            keywords.add((pp.get("pain", "") or pp.get("description", "")).lower())

    # Keywords
    for kw in icp_data.get("keywords", []):
        if isinstance(kw, str):
            keywords.add(kw.lower())

    # Industries
    for ind in icp_data.get("industries", []):
        if isinstance(ind, str):
            keywords.add(ind.lower())

    # Job titles
    for jt in icp_data.get("job_titles", []):
        if isinstance(jt, str):
            keywords.add(jt.lower())

    # Target description
    target = icp_data.get("target_description", "") or icp_data.get("name", "")
    if target:
        for word in target.lower().split():
            if len(word) > 4:  # Skip short words
                keywords.add(word)


def _boost_existing_contact(
    contact: dict[str, Any],
    signal_context: dict[str, Any],
    composite_score: float,
    now: int,
) -> None:
    """Boost an existing contact's priority and inject signal context."""
    from ..db.queries import get_contact_analysis, save_contact_analysis, update_contact

    contact_id = contact["id"]
    current_fit = contact.get("fit_score", 0) or 0

    # Boost fit_score: add a fraction of composite score (both on 0-1 scale)
    boosted = min(current_fit + composite_score * 0.2, 1.0)
    if boosted > current_fit:
        update_contact(contact_id, fit_score=boosted)

    # Merge signal context into analysis_json
    existing_analysis = get_contact_analysis(contact_id) or {}
    existing_analysis["signal_context"] = signal_context

    # Merge pain points
    existing_pains = existing_analysis.get("pain_points", [])
    new_pains = signal_context.get("pain_points", [])
    if new_pains:
        merged_pains = list(set(existing_pains) | set(new_pains))
        existing_analysis["pain_points"] = merged_pains[:5]

    save_contact_analysis(contact_id, existing_analysis)




def _extract_company(signal: dict[str, Any]) -> str:
    """Extract company name from signal metadata or content."""
    metadata = _parse_metadata(signal)
    company = metadata.get("new_company") or metadata.get("company") or ""
    if not company:
        # Try to extract from prospect title
        title = signal.get("prospect_title") or ""
        if " at " in title:
            company = title.split(" at ")[-1].strip()
    return company


def _parse_metadata(signal: dict[str, Any]) -> dict[str, Any]:
    """Safely parse signal metadata_json."""
    raw = signal.get("metadata_json", "")
    if not raw:
        return {}
    try:
        return json.loads(raw) if isinstance(raw, str) else raw
    except (json.JSONDecodeError, TypeError):
        return {}


def _build_compound_hook(intent_event: dict[str, Any]) -> str:
    """Build an engagement hook tailored to a compound intent event.

    Compound events represent multiple layered buying signals, so the
    hook should reflect the richer context naturally.
    """
    event_type = intent_event.get("event_type", "")
    company = intent_event.get("company", "")

    hooks: dict[str, str] = {
        "new_leader_building": (
            f"Exciting times at {company} — building out the team!"
            if company
            else "Exciting to see the team growth!"
        ),
        "active_evaluation": (
            "Sounds like you're evaluating solutions in this space"
        ),
        "engaged_thought_leader": (
            "Your perspective in the conversation really stood out"
        ),
        "growth_mode": (
            f"Great momentum at {company}!"
            if company
            else "Impressive growth trajectory!"
        ),
        "new_role_exploring": (
            "Congrats on the new role — always interesting to hear "
            "how new leaders approach the first 90 days"
        ),
        "new_role_evaluating": (
            "Congrats on the new role — a fresh look at your tech stack "
            "can be a great early win"
        ),
        "funded_and_searching": (
            f"Congrats on the fundraise at {company}!"
            if company
            else "Congrats on the recent fundraise!"
        ),
        "vocal_evaluator": (
            "Your analysis of the market options is really insightful"
        ),
        "promoted_and_building": (
            f"Congrats on the promotion — building out the team at {company}!"
            if company
            else "Congrats on the promotion — exciting growth ahead!"
        ),
        "promoted_and_exploring": (
            "Congrats on the promotion — always a good time to reassess the toolstack"
        ),
        "active_market_participant": (
            "Sounds like you're actively exploring the space"
        ),
        "hiring_and_signaling": (
            f"Impressive growth at {company} — building out the team!"
            if company
            else "Impressive growth trajectory!"
        ),
    }

    return hooks.get(event_type, "")


def _get_experiment_thresholds(
    campaign_id: str,
    signal_id: str,
) -> tuple[str, dict[str, float] | None]:
    """Check for active signal threshold experiments and return variant + overrides.

    Uses a deterministic hash of signal_id to assign control/treatment variant.
    Returns ("control", None) if no experiment is active.
    """
    import hashlib
    import json as _json

    from ..db.schema import get_db

    db = get_db()
    row = db.execute(
        """SELECT id, control_config, treatment_config
           FROM signal_experiments
           WHERE campaign_id = ? AND status = 'running'
             AND experiment_type = 'threshold'
           LIMIT 1""",
        (campaign_id,),
    ).fetchone()
    db.close()

    if not row:
        return ("control", None)

    # Deterministic variant assignment: hash signal_id → even=control, odd=treatment
    h = int(hashlib.md5(signal_id.encode()).hexdigest(), 16)
    variant = "treatment" if h % 2 else "control"

    config_str = row["treatment_config"] if variant == "treatment" else row["control_config"]
    try:
        config = _json.loads(config_str)
    except (_json.JSONDecodeError, TypeError):
        return ("control", None)

    return (variant, config)
