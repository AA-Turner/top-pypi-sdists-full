"""Tool: edit_campaign — Edit campaign settings after creation.

Allows changing the campaign name, mode, voice settings, warm-up sequence,
follow-up cadence, engagement behavior, and timing preferences.
"""

from __future__ import annotations

import json
import logging

from ..db import aio as db
from ..services.cloud_sync import sync_campaign_settings

logger = logging.getLogger(__name__)

# Valid values for new settings
_VALID_ENGAGEMENT_MODES = frozenset({"auto", "comment_only", "react_only"})
_VALID_ACTIVE_DAYS = frozenset(range(7))  # 0=Mon ... 6=Sun


async def run_edit_campaign(
    campaign_id: str = "",
    name: str = "",
    mode: str = "",
    booking_link: str = "",
    offerings: str = "",
    case_studies: str = "",
    social_proofs: str = "",
    campaign_preferences: str = "",
    voice_mode: str = "",
    voice_noise: str = "",
    voice_humanize: str = "",
    open_to_work_mode: str = "",
    # Warm-up sequence toggles
    enable_profile_views: str = "",
    enable_follows: str = "",
    enable_endorsements: str = "",
    enable_engagements: str = "",
    enable_followups: str = "",
    enable_auto_replies: str = "",
    enable_invitations: str = "",
    # Engagement settings
    engagement_mode: str = "",
    # Follow-up settings
    max_followups: int = 0,
    followup_delay_days: str = "",
    # Invite settings
    withdraw_stale_invites: str = "",
    stale_invite_days: int = 0,
    # Send timing
    send_in_business_hours: str = "",
    active_days: str = "",
) -> str:
    """Edit a campaign's settings.

    Args:
        campaign_id: Which campaign to edit. Edits the first active campaign if empty.
        name: New campaign name. Leave empty to keep current name.
        mode: New mode: "copilot" or "autopilot". Leave empty to keep current mode.
        booking_link: Calendar/booking URL for positive reply auto-responses.
        offerings: What you offer (products, services, value props).
        case_studies: Brief case studies or success stories.
        social_proofs: Social proof (logos, metrics, testimonials).
        campaign_preferences: Custom messaging preferences (tone, topics to avoid, etc.).
        voice_mode: Voice memo mode: "text_only", "voice_only", "mixed", or "ab_test".
        voice_noise: Ambient noise type: "office", "cafe", "street", "quiet", "none", "auto".
        voice_humanize: Voice text humanization: "on" or "off".
        open_to_work_mode: OTW badge control: "off", "on_for_inbound", "off_for_outbound".
        enable_follows: Follow prospects before inviting: "on" or "off".
        enable_endorsements: Endorse skills before inviting: "on" or "off".
        enable_engagements: Comment/react on posts before inviting: "on" or "off".
        enable_followups: Send follow-up DMs after connection: "on" or "off".
        enable_invitations: Send connection invitations: "on" or "off".
            When off, campaign only DMs existing connections (no invitations sent).
        engagement_mode: Engagement style: "auto" (30% react/70% comment),
            "comment_only", or "react_only".
        max_followups: Max follow-up messages (1-5). 0 to keep current.
        followup_delay_days: Custom day intervals as comma-separated list
            (e.g., "1,3,7,14"). Leave empty to keep current.
        withdraw_stale_invites: Auto-withdraw stale invites: "on" or "off".
        stale_invite_days: Days before withdrawing stale invites (7-60). 0 to keep current.
        send_in_business_hours: Respect prospect's business hours: "on" or "off".
        active_days: Active send days as comma-separated numbers (0=Mon, 6=Sun).
            E.g., "0,1,2,3,4" for weekdays. Leave empty to keep current.
    """

    # ── Pre-checks ──
    setup_done = await db.get_setting("setup_complete", False)
    if not setup_done:
        return (
            "Setup required before editing campaigns.\n\n"
            "Please run setup_profile first."
        )

    has_context_fields = any([offerings, case_studies, social_proofs, campaign_preferences])
    has_voice_settings = any([voice_noise, voice_humanize])
    has_toggle_settings = any([
        enable_follows, enable_endorsements, enable_engagements, enable_followups,
        enable_auto_replies, enable_invitations,
    ])
    has_engagement_settings = bool(engagement_mode)
    has_followup_settings = max_followups > 0 or bool(followup_delay_days)
    has_invite_settings = bool(withdraw_stale_invites) or stale_invite_days > 0
    has_timing_settings = bool(send_in_business_hours) or bool(active_days)

    has_any = (
        name or mode or booking_link or voice_mode
        or has_context_fields or has_voice_settings or open_to_work_mode
        or has_toggle_settings or has_engagement_settings
        or has_followup_settings or has_invite_settings or has_timing_settings
    )

    if not has_any:
        return (
            "Nothing to change.\n\n"
            "Provide at least one of:\n"
            "  name: New campaign name\n"
            "  mode: \"copilot\" or \"autopilot\"\n"
            "  booking_link: Calendar URL for reply auto-responses\n"
            "  voice_mode: text_only, voice_only, mixed, or ab_test\n"
            "  voice_noise: office, cafe, street, quiet, none, auto\n"
            "  voice_humanize: on or off\n"
            "\n"
            "  Warm-up sequence:\n"
            "  enable_follows: on or off\n"
            "  enable_endorsements: on or off\n"
            "  enable_engagements: on or off\n"
            "  enable_followups: on or off\n"
            "  enable_auto_replies: on or off\n"
            "  enable_invitations: on or off\n"
            "\n"
            "  Engagement:\n"
            "  engagement_mode: auto, comment_only, or react_only\n"
            "\n"
            "  Follow-ups:\n"
            "  max_followups: 1-5\n"
            "  followup_delay_days: e.g. \"1,3,7,14\"\n"
            "\n"
            "  Invites:\n"
            "  withdraw_stale_invites: on or off\n"
            "  stale_invite_days: 7-60\n"
            "\n"
            "  Timing:\n"
            "  send_in_business_hours: on or off\n"
            "  active_days: e.g. \"0,1,2,3,4\" (0=Mon, 6=Sun)"
        )

    # ── Validate mode ──
    if mode and mode not in ("copilot", "autopilot"):
        return (
            f"Invalid mode: '{mode}'\n\n"
            "Must be 'copilot' or 'autopilot'."
        )

    # ── Validate voice_mode ──
    if voice_mode:
        from ..constants import VALID_VOICE_MODES
        if voice_mode not in VALID_VOICE_MODES:
            return (
                f"Invalid voice_mode: '{voice_mode}'\n\n"
                "Must be one of: text_only, voice_only, mixed, ab_test"
            )

    # ── Validate voice_noise ──
    if voice_noise:
        from ..constants import VALID_NOISE_TYPES
        if voice_noise not in VALID_NOISE_TYPES:
            return (
                f"Invalid voice_noise: '{voice_noise}'\n\n"
                "Must be one of: office, cafe, street, quiet, none, auto"
            )

    # ── Validate voice_humanize ──
    if voice_humanize and voice_humanize not in ("on", "off"):
        return (
            f"Invalid voice_humanize: '{voice_humanize}'\n\n"
            "Must be 'on' or 'off'."
        )

    # ── Validate on/off toggles ──
    for label, val in [
        ("enable_profile_views", enable_profile_views),
        ("enable_follows", enable_follows),
        ("enable_endorsements", enable_endorsements),
        ("enable_engagements", enable_engagements),
        ("enable_followups", enable_followups),
        ("enable_auto_replies", enable_auto_replies),
        ("enable_invitations", enable_invitations),
        ("withdraw_stale_invites", withdraw_stale_invites),
        ("send_in_business_hours", send_in_business_hours),
    ]:
        if val and val not in ("on", "off"):
            return f"Invalid {label}: '{val}'. Must be 'on' or 'off'."

    # ── Validate engagement_mode ──
    if engagement_mode and engagement_mode not in _VALID_ENGAGEMENT_MODES:
        return (
            f"Invalid engagement_mode: '{engagement_mode}'\n\n"
            "Must be one of: auto, comment_only, react_only"
        )

    # ── Validate max_followups ──
    if max_followups and (max_followups < 1 or max_followups > 5):
        return "Invalid max_followups: must be between 1 and 5."

    # ── Validate followup_delay_days ──
    parsed_followup_days: list[int] | None = None
    if followup_delay_days:
        try:
            parsed_followup_days = sorted([int(d.strip()) for d in followup_delay_days.split(",")])
            if not parsed_followup_days or any(d < 1 or d > 90 for d in parsed_followup_days):
                return "Invalid followup_delay_days: each value must be between 1 and 90."
        except ValueError:
            return "Invalid followup_delay_days: must be comma-separated numbers (e.g., '1,3,7,14')."

    # ── Validate stale_invite_days ──
    if stale_invite_days and (stale_invite_days < 7 or stale_invite_days > 60):
        return "Invalid stale_invite_days: must be between 7 and 60."

    # ── Validate active_days ──
    parsed_active_days: list[int] | None = None
    if active_days:
        try:
            parsed_active_days = sorted(set(int(d.strip()) for d in active_days.split(",")))
            if not parsed_active_days or any(d not in _VALID_ACTIVE_DAYS for d in parsed_active_days):
                return "Invalid active_days: each value must be 0-6 (0=Mon, 6=Sun)."
        except ValueError:
            return "Invalid active_days: must be comma-separated numbers (e.g., '0,1,2,3,4')."

    # ── Resolve campaign ──
    campaign, err = await db.find_active_campaign(campaign_id)
    if not campaign and not campaign_id:
        # Fallback: try any campaign (not just active)
        campaigns = await db.list_campaigns()
        if not campaigns:
            return (
                "No campaigns to edit.\n\n"
                "Create one first: create_campaign(\"your target description\")"
            )
        campaign = campaigns[0]
    elif not campaign:
        return err
    campaign_id = campaign["id"]

    # ── Apply changes ──
    changes: dict[str, str] = {}
    change_descriptions: list[str] = []

    old_name = campaign.get("name", "")
    old_mode = campaign.get("mode", "autopilot")

    if name and name != old_name:
        changes["name"] = name
        change_descriptions.append(f"Name: '{old_name}' -> '{name}'")

    if mode and mode != old_mode and mode == "autopilot":
        changes["mode"] = "autopilot"
        change_descriptions.append(f"Mode: {old_mode} -> Autopilot")

    # Parse config_json once
    config_json = campaign.get("config_json", "{}")
    try:
        config = json.loads(config_json) if config_json else {}
    except (json.JSONDecodeError, TypeError):
        config = {}

    if booking_link:
        old_booking = config.get("booking_link", "")
        if booking_link != old_booking:
            config["booking_link"] = booking_link
            change_descriptions.append(f"Booking link: {booking_link}")

    if voice_mode:
        old_voice = config.get("voice_mode", "text_only")
        if voice_mode != old_voice:
            config["voice_mode"] = voice_mode
            change_descriptions.append(f"Voice mode: {old_voice} -> {voice_mode}")

    if voice_noise:
        old_noise = config.get("voice_noise_type", "auto")
        if voice_noise != old_noise:
            config["voice_noise_type"] = voice_noise
            change_descriptions.append(f"Voice noise: {old_noise} -> {voice_noise}")

    if voice_humanize:
        humanize_bool = voice_humanize == "on"
        old_humanize = config.get("voice_humanize", True)
        if humanize_bool != old_humanize:
            config["voice_humanize"] = humanize_bool
            change_descriptions.append(f"Voice humanize: {'on' if old_humanize else 'off'} -> {voice_humanize}")

    if open_to_work_mode:
        valid_otw = {"off", "on_for_inbound", "off_for_outbound"}
        if open_to_work_mode not in valid_otw:
            return f"Invalid open_to_work_mode. Must be one of: {', '.join(sorted(valid_otw))}"
        old_otw = config.get("open_to_work_mode", "off")
        if open_to_work_mode != old_otw:
            config["open_to_work_mode"] = open_to_work_mode
            change_descriptions.append(f"Open to Work: {old_otw} -> {open_to_work_mode}")

    # ── Warm-up sequence toggles ──
    _TOGGLE_LABELS = {
        "enable_profile_views": "Profile views",
        "enable_follows": "Follows",
        "enable_endorsements": "Endorsements",
        "enable_engagements": "Engagements",
        "enable_followups": "Follow-ups",
        "enable_auto_replies": "Auto-replies",
        "enable_invitations": "Invitations",
        "withdraw_stale_invites": "Withdraw stale invites",
        "send_in_business_hours": "Business hours",
    }
    for key, val in [
        ("enable_profile_views", enable_profile_views),
        ("enable_follows", enable_follows),
        ("enable_endorsements", enable_endorsements),
        ("enable_engagements", enable_engagements),
        ("enable_followups", enable_followups),
        ("enable_auto_replies", enable_auto_replies),
        ("enable_invitations", enable_invitations),
        ("withdraw_stale_invites", withdraw_stale_invites),
        ("send_in_business_hours", send_in_business_hours),
    ]:
        if val:
            new_bool = val == "on"
            old_bool = config.get(key, True)
            if new_bool != old_bool:
                config[key] = new_bool
                label = _TOGGLE_LABELS[key]
                change_descriptions.append(f"{label}: {'on' if old_bool else 'off'} -> {val}")

    # ── Engagement mode ──
    if engagement_mode:
        old_em = config.get("engagement_mode", "auto")
        if engagement_mode != old_em:
            config["engagement_mode"] = engagement_mode
            change_descriptions.append(f"Engagement mode: {old_em} -> {engagement_mode}")

    # ── Follow-up settings ──
    if max_followups:
        old_mf = config.get("max_followups", 5)
        if max_followups != old_mf:
            config["max_followups"] = max_followups
            change_descriptions.append(f"Max follow-ups: {old_mf} -> {max_followups}")

    if parsed_followup_days is not None:
        old_fd = config.get("followup_delay_days", [1, 7, 14, 21, 28])
        if parsed_followup_days != old_fd:
            config["followup_delay_days"] = parsed_followup_days
            change_descriptions.append(
                f"Follow-up schedule: {','.join(map(str, old_fd))} -> {','.join(map(str, parsed_followup_days))} days"
            )

    # ── Stale invite days ──
    if stale_invite_days:
        old_sid = config.get("stale_invite_days", 21)
        if stale_invite_days != old_sid:
            config["stale_invite_days"] = stale_invite_days
            change_descriptions.append(f"Stale invite days: {old_sid} -> {stale_invite_days}")

    # ── Active days ──
    if parsed_active_days is not None:
        old_ad = config.get("active_days", [0, 1, 2, 3, 4])
        if parsed_active_days != old_ad:
            config["active_days"] = parsed_active_days
            day_names = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
            old_str = ",".join(day_names[d] for d in old_ad)
            new_str = ",".join(day_names[d] for d in parsed_active_days)
            change_descriptions.append(f"Active days: {old_str} -> {new_str}")

    # Commit config_json changes if any
    config_updated = json.dumps(config)
    if config_updated != (config_json or "{}"):
        changes["config_json"] = config_updated

    # ── Update context fields (offerings, case_studies, social_proofs, preferences) ──
    if has_context_fields:
        existing_ctx = await db.get_campaign_context(campaign_id)
        ctx_changed = False
        if offerings:
            existing_ctx["offerings"] = offerings
            ctx_changed = True
            change_descriptions.append(f"Offerings: {offerings[:80]}{'...' if len(offerings) > 80 else ''}")
        if case_studies:
            existing_ctx["case_studies"] = case_studies
            ctx_changed = True
            change_descriptions.append(f"Case studies: {case_studies[:80]}{'...' if len(case_studies) > 80 else ''}")
        if social_proofs:
            existing_ctx["social_proofs"] = social_proofs
            ctx_changed = True
            change_descriptions.append(f"Social proofs: {social_proofs[:80]}{'...' if len(social_proofs) > 80 else ''}")
        if campaign_preferences:
            existing_ctx["campaign_preferences"] = campaign_preferences
            ctx_changed = True
            change_descriptions.append(f"Preferences: {campaign_preferences[:80]}{'...' if len(campaign_preferences) > 80 else ''}")
        if ctx_changed:
            changes["context_json"] = json.dumps(existing_ctx)

    if not changes:
        return (
            f"No changes needed for '{old_name}'.\n"
            "The campaign already has those settings."
        )

    await db.update_campaign(campaign_id, **changes)

    # ── Log warmup changes so optimizer respects user decisions ──
    warmup_keys = {"enable_profile_views", "enable_follows", "enable_endorsements", "enable_engagements"}
    warmup_changed = {k for k, v in [
        ("enable_profile_views", enable_profile_views),
        ("enable_follows", enable_follows),
        ("enable_endorsements", enable_endorsements),
        ("enable_engagements", enable_engagements),
    ] if v}
    if warmup_changed:
        try:
            from ..db.signal_queries import save_optimization_history
            from ..db.async_bridge import run_db as _run_db
            for key in warmup_changed:
                val = locals()[key]
                await _run_db(
                    save_optimization_history,
                    optimization_type="user_changed_warmup",
                    target=f"{old_name}::{key}",
                    before_value=str(config.get(key, True)),
                    after_value=val,
                    reason="User manually changed campaign warmup setting",
                )
        except Exception:
            pass  # Don't block campaign edit if logging fails

    # ── Sync settings to backend ──
    # Build a settings dict matching the backend's PATCH /campaigns/{id}/settings schema
    sync_settings: dict[str, str | int] = {}
    for key, val in (
        ("enable_profile_views", enable_profile_views),
        ("enable_follows", enable_follows),
        ("enable_endorsements", enable_endorsements),
        ("enable_engagements", enable_engagements),
        ("enable_followups", enable_followups),
        ("enable_auto_replies", enable_auto_replies),
        ("enable_invitations", enable_invitations),
        ("withdraw_stale_invites", withdraw_stale_invites),
        ("send_in_business_hours", send_in_business_hours),
    ):
        if val:
            sync_settings[key] = val
    if engagement_mode:
        sync_settings["engagement_mode"] = engagement_mode
    if max_followups:
        sync_settings["max_followups"] = max_followups
    if followup_delay_days:
        sync_settings["followup_delay_days"] = followup_delay_days
    if active_days:
        sync_settings["active_days"] = active_days
    if voice_mode:
        sync_settings["voice_mode"] = voice_mode
    if voice_noise:
        sync_settings["voice_noise"] = voice_noise
    if voice_humanize:
        sync_settings["voice_humanize"] = voice_humanize

    if sync_settings:
        synced = await sync_campaign_settings(campaign_id, sync_settings)
        if not synced:
            logger.warning("Could not sync settings for campaign %s to backend", campaign_id)

    # ── Format result ──
    output = [
        f"Updated campaign '{changes.get('name', old_name)}':\n",
    ]
    for desc in change_descriptions:
        output.append(f"   {desc}")
    output.append("")

    # Mode-specific hints
    if mode == "autopilot" and old_mode == "copilot":
        output.append(
            "Autopilot is now active. Messages will be sent automatically "
            "after passing validation."
        )
    # Copilot mode removed — all campaigns are autopilot

    return "\n".join(output)
