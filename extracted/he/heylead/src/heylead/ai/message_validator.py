"""6-stage message validation pipeline.

Ensures every outreach message passes quality checks before sending.
From the spec: "Your 56 prompt versions and 5-stage validation pipeline
are not features — they are THE product."

Stages:
1. Length check (≤200 chars for regular LinkedIn)
2. Salesy language detection
3. AI-tell patterns detection
4. Voice consistency check
5. Generic phrase detection
6. Specificity check (catches messages that could be sent to anyone)
"""

from __future__ import annotations

import logging
import re
from typing import Any

logger = logging.getLogger(__name__)

# ──────────────────────────────────────────────
# Stage 2: Salesy language blocklist
# ──────────────────────────────────────────────

SALESY_PHRASES = [
    "leverage",
    "synergy",
    "exciting opportunity",
    "game-changer",
    "cutting-edge",
    "revolutionary",
    "transform your",
    "skyrocket",
    "unlock the power",
    "world-class",
    "best-in-class",
    "take your business to the next level",
    "scale your",
    "maximize your",
    "disruptive",
    "paradigm shift",
    "thought leader",
    "low-hanging fruit",
    "value proposition",
    "circle back",
    "move the needle",
    "boil the ocean",
    "deep dive",
    "hop on a call",
    "hop on a quick call",
    "let's connect",
    "would love to connect",
    "pick your brain",
    "touch base",
    "quick chat",
    "quick question",
    "no-brainer",
    # v63 additions — refined from 56 production iterations
    "innovative",
    "leaders",
    "landscape",
    "fast-paced",
    "optimize",
    "unlock",
    "robust",
    "streamline",
    "actionable insights",
    "state of the art",
    "frictionless",
    "next-gen",
    "empower",
    "enable",
]

# ──────────────────────────────────────────────
# Stage 3: AI-tell patterns
# ──────────────────────────────────────────────

AI_TELL_PATTERNS = [
    r"^I noticed (you|your|that you)",
    r"^I came across your",
    r"^I saw your (profile|post|article)",
    r"^I was impressed by",
    r"^Hope this message finds you",
    r"^I'm reaching out because",
    r"^I'd love to",
    r"^I stumbled upon",
    r"^Your work on .+ caught my (eye|attention)",
    r"^As a fellow",
    r"I believe (we|our|I) can",
    r"I'm confident that",
    r"I'm sure you're busy",
    r"Don't hesitate to",
    r"Feel free to",
    r"Looking forward to",
    r"Best regards",
    r"Warm regards",
    r"Kind regards",
    # v63 additions — hard guardrails from production
    r"\u2014",  # em dash — (v63 hard guardrail: "Do not use em dashes")
    r"we've helped similar",  # v63: "Do not use 'we've helped similar companies'"
    # Generic AI questions that provide no value
    r"How do you see .+ (changing|impacting|evolving|shaping)",
    r"Where do you see .+ (heading|going|evolving)",
    r"What's your (take|approach|perspective) on",
    r"How are you (using|leveraging|approaching) AI",
]

# v63 guardrail: "DO NOT USE THE WORD 'hope' IN YOUR FIRST 3 SENTENCES"
HOPE_IN_OPENING_PATTERN = re.compile(r"\bhope\b", re.IGNORECASE)

# v63 guardrail: role/title mentions
ROLE_TITLE_PATTERNS = [
    r"\b(ceo|cto|cfo|coo|cmo|vp|svp|evp|founder|co-founder|manager|director|head of|analyst|executive)\b",
]

# v63 guardrail: industry/domain mentions
INDUSTRY_PATTERNS = [
    r"\b(finance|fintech|tech|healthcare|sustainability|erp|saas|ai|blockchain)\b",
]

# ──────────────────────────────────────────────
# Stage 5: Generic phrases
# ──────────────────────────────────────────────

GENERIC_PHRASES = [
    "in your industry",
    "in your field",
    "in your space",
    "professionals like you",
    "leaders like you",
    "people like you",
    "your company",  # Too vague — should name the company
    "your role",
    "your position",
    "mutual connections",
    "shared interests",
]

# ──────────────────────────────────────────────
# Stage 6: Specificity check — catches messages that could be sent to anyone
# ──────────────────────────────────────────────

GENERIC_OPENER_PATTERNS = [
    r"^it takes courage",
    r"^building something from (scratch|zero|the ground)",
    r"what's your biggest (priority|challenge|focus)",
    r"what keeps you up at night",
    r"how's business going",
    r"how's everything going",
    r"what's on your plate",
    r"what are you working on",
    r"what drives you",
    r"what motivates you",
    r"curious what you think about",
    r"what's your take on the (market|industry|space)",
    r"how do you stay ahead",
    r"what's next for you",
]


class ValidationResult:
    """Result of the 5-stage message validation."""

    def __init__(self) -> None:
        self.is_valid = True
        self.issues: list[str] = []
        self.warnings: list[str] = []
        self.stage_results: dict[str, bool] = {}

    def fail(self, stage: str, reason: str) -> None:
        self.is_valid = False
        self.issues.append(f"[{stage}] {reason}")
        self.stage_results[stage] = False

    def warn(self, stage: str, reason: str) -> None:
        self.warnings.append(f"[{stage}] {reason}")

    def pass_stage(self, stage: str) -> None:
        self.stage_results[stage] = True


def validate_message(
    message: str,
    voice_signature: dict[str, Any] | None = None,
    max_chars: int = 200,
) -> ValidationResult:
    """Run the 5-stage validation pipeline on a message.

    Args:
        message: The generated message text
        voice_signature: User's voice analysis (for stage 4)
        max_chars: Character limit (200 regular, 300 Sales Nav)

    Returns:
        ValidationResult with pass/fail and details
    """
    result = ValidationResult()
    msg_lower = message.lower().strip()

    # ── Stage 1: Length check ──
    if len(message) > max_chars:
        result.fail("Length", f"Message is {len(message)} chars (max {max_chars})")
    elif len(message) < 20:
        result.fail("Length", f"Message is too short ({len(message)} chars) — needs personalization")
    else:
        result.pass_stage("Length")

    # ── Stage 2: Salesy language ──
    found_salesy = [phrase for phrase in SALESY_PHRASES if phrase in msg_lower]
    if found_salesy:
        result.fail("Salesy", f"Contains salesy phrases: {', '.join(found_salesy[:3])}")
    else:
        result.pass_stage("Salesy")

    # ── Stage 3: AI-tell patterns ──
    found_ai_tells = []
    for pattern in AI_TELL_PATTERNS:
        if re.search(pattern, message, re.IGNORECASE):
            found_ai_tells.append(pattern.replace(r"^", "").replace("\\", ""))
    if found_ai_tells:
        result.fail("AI-tells", f"Sounds AI-generated: matches {len(found_ai_tells)} known patterns")
    else:
        result.pass_stage("AI-tells")

    # ── Stage 3b: v63 guardrails — "hope" in opening, roles, industries ──
    # Check "hope" in first 3 sentences (v63 hard rule)
    sentences = re.split(r'[.!?]+', message, maxsplit=3)
    opening_text = " ".join(sentences[:3])
    if HOPE_IN_OPENING_PATTERN.search(opening_text):
        result.warn("v63-Guardrails", 'Uses "hope" in opening sentences (v63 rule: avoid in first 3)')

    # Check role/title mentions (v63: no roles, titles, seniority, acronyms)
    for pattern in ROLE_TITLE_PATTERNS:
        if re.search(pattern, msg_lower):
            result.warn("v63-Guardrails", "Mentions job roles/titles (v63 rule: no role references)")
            break

    # Check industry/domain mentions (v63: no sector labels)
    for pattern in INDUSTRY_PATTERNS:
        if re.search(pattern, msg_lower):
            result.warn("v63-Guardrails", "Mentions industry/domain (v63 rule: no sector labels)")
            break

    # ── Stage 4: Voice consistency ──
    if voice_signature:
        formality = voice_signature.get("formality_level", 5)
        no_go = voice_signature.get("no_go", "").lower()

        # Check formality mismatch
        has_exclamation = "!" in message
        has_emoji = bool(re.search(r"[\U0001f600-\U0001f650]", message))

        if formality >= 8 and (has_exclamation or has_emoji):
            result.warn("Voice", "Message is too casual for this user's formal tone")

        if formality <= 3 and not has_exclamation and len(message) > 150:
            result.warn("Voice", "Message is too formal for this user's casual tone")

        # Check no-go words
        if no_go:
            no_go_words = [w.strip() for w in no_go.split(",")]
            found_nogo = [w for w in no_go_words if w and w in msg_lower]
            if found_nogo:
                result.fail("Voice", f"Uses no-go words: {', '.join(found_nogo)}")
            else:
                result.pass_stage("Voice")
        else:
            result.pass_stage("Voice")
    else:
        result.pass_stage("Voice")

    # ── Stage 5: Generic phrases ──
    found_generic = [phrase for phrase in GENERIC_PHRASES if phrase in msg_lower]
    if found_generic:
        result.warn("Generic", f"Contains generic phrases: {', '.join(found_generic[:2])}")
    result.pass_stage("Generic")

    # ── Stage 6: Specificity check (outreach messages only, not replies/followups) ──
    if max_chars <= 200:  # Only for connection requests (200 char limit)
        found_generic_openers = []
        for pattern in GENERIC_OPENER_PATTERNS:
            if re.search(pattern, msg_lower):
                found_generic_openers.append(pattern.replace(r"^", "").replace("\\", ""))
        if found_generic_openers:
            result.fail(
                "Specificity",
                "Message uses a generic opener that could be sent to anyone — "
                "needs a concrete reference to the prospect's profile or situation"
            )
        else:
            result.pass_stage("Specificity")
    else:
        result.pass_stage("Specificity")

    return result


# ──────────────────────────────────────────────
# Follow-Up Specific Validation
# ──────────────────────────────────────────────

LAZY_FOLLOWUP_PHRASES = [
    "just following up",
    "circling back",
    "touching base",
    "checking in",
    "wanted to follow up",
    "just wanted to check",
    "just checking in",
    "bumping this",
    "any thoughts on",
    "did you get a chance",
    "have you had a chance",
    "wanted to circle back",
]


def validate_followup(
    message: str,
    voice_signature: dict[str, Any] | None = None,
    previous_messages: list[str] | None = None,
    max_chars: int = 500,
) -> ValidationResult:
    """Validate a follow-up DM message.

    Extends the standard validation with:
    - Higher character limit (500 vs 200)
    - Lazy follow-up phrase detection
    - Repetition check against previous messages

    Args:
        message: The generated follow-up message text
        voice_signature: User's voice analysis (for voice consistency)
        previous_messages: List of previous message texts (for repetition check)
        max_chars: Character limit (default 500 for DMs)

    Returns:
        ValidationResult with pass/fail and details
    """
    # Run base validation with the higher char limit
    result = validate_message(message, voice_signature, max_chars)

    msg_lower = message.lower().strip()

    # ── Extra Stage: Lazy follow-up phrases ──
    found_lazy = [phrase for phrase in LAZY_FOLLOWUP_PHRASES if phrase in msg_lower]
    if found_lazy:
        result.fail("LazyFollowUp", f"Uses lazy follow-up phrases: {', '.join(found_lazy[:2])}")
    else:
        result.pass_stage("LazyFollowUp")

    # ── Extra Stage: Repetition check ──
    if previous_messages:
        for prev in previous_messages:
            if not prev:
                continue
            prev_lower = prev.lower().strip()
            # Check for significant overlap (>50% of words in common)
            new_words = set(msg_lower.split())
            prev_words = set(prev_lower.split())
            if not new_words or not prev_words:
                continue
            overlap = len(new_words & prev_words)
            overlap_ratio = overlap / min(len(new_words), len(prev_words))
            if overlap_ratio > 0.6:
                result.fail(
                    "Repetition",
                    f"Message is too similar to a previous message ({overlap_ratio:.0%} word overlap)"
                )
                break
        else:
            result.pass_stage("Repetition")
    else:
        result.pass_stage("Repetition")

    return result


# ──────────────────────────────────────────────
# Comment Specific Validation
# ──────────────────────────────────────────────

COMMENT_SALESY_PHRASES = [
    "we offer",
    "our product",
    "our service",
    "our solution",
    "our platform",
    "our tool",
    "check out",
    "have you tried",
    "you should try",
    "we help",
    "we specialize",
    "reach out to me",
    "feel free to dm",
    "send me a message",
    "book a call",
    "schedule a call",
    "let me know if",
    "happy to help",
    "love to chat",
]


def validate_comment(
    comment: str,
    voice_signature: dict[str, Any] | None = None,
    max_chars: int = 200,
) -> ValidationResult:
    """Validate a post comment.

    Extends the standard validation with:
    - Lower character limit (200 vs 500)
    - Comment-specific salesy detection (product mentions, CTAs)
    - No repetition check needed (comments are one-offs)

    Args:
        comment: The generated comment text
        voice_signature: User's voice analysis (for voice consistency)
        max_chars: Character limit (default 200)

    Returns:
        ValidationResult with pass/fail and details
    """
    # Run base validation with comment char limit
    result = validate_message(comment, voice_signature, max_chars)

    comment_lower = comment.lower().strip()

    # ── Extra Stage: Comment-specific salesy phrases ──
    found_comment_salesy = [
        phrase for phrase in COMMENT_SALESY_PHRASES if phrase in comment_lower
    ]
    if found_comment_salesy:
        result.fail(
            "CommentSalesy",
            f"Comment contains promotional language: {', '.join(found_comment_salesy[:2])}"
        )
    else:
        result.pass_stage("CommentSalesy")

    return result


# ──────────────────────────────────────────────
# Reply Specific Validation
# ──────────────────────────────────────────────

PUSHY_REPLY_PHRASES = [
    "i understand but",
    "i understand, but",
    "hear me out",
    "just give me",
    "five minutes of your time",
    "i think you're missing",
    "what if i told you",
    "but what about",
    "reconsider",
    "change your mind",
    "one more thing",
    "before you go",
    "at least consider",
    "maybe if you",
    "are you sure",
    "you might want to",
]


def validate_reply(
    message: str,
    voice_signature: dict[str, Any] | None = None,
    sentiment: str = "neutral",
    previous_messages: list[str] | None = None,
    max_chars: int = 500,
) -> ValidationResult:
    """Validate a reply message with sentiment-specific rules.

    Extends the standard validation with:
    - Lazy follow-up phrase detection (reused from follow-up validation)
    - Repetition check against previous messages
    - Pushy phrase detection for negative-sentiment replies
    - Conciseness warning for negative-sentiment replies

    Args:
        message: The generated reply message text
        voice_signature: User's voice analysis (for voice consistency)
        sentiment: The prospect's reply sentiment (positive, question, negative, neutral)
        previous_messages: List of previous SDR message texts (for repetition check)
        max_chars: Character limit (default 500 for DMs, 200 for negative)

    Returns:
        ValidationResult with pass/fail and details
    """
    # For negative sentiment, enforce shorter limit
    effective_max = min(max_chars, 200) if sentiment == "negative" else max_chars

    # Run base validation with the appropriate char limit
    result = validate_message(message, voice_signature, effective_max)

    msg_lower = message.lower().strip()

    # ── Extra Stage: Lazy follow-up phrases ──
    found_lazy = [phrase for phrase in LAZY_FOLLOWUP_PHRASES if phrase in msg_lower]
    if found_lazy:
        result.fail("LazyFollowUp", f"Uses lazy follow-up phrases: {', '.join(found_lazy[:2])}")
    else:
        result.pass_stage("LazyFollowUp")

    # ── Extra Stage: Repetition check ──
    if previous_messages:
        for prev in previous_messages:
            if not prev:
                continue
            prev_lower = prev.lower().strip()
            new_words = set(msg_lower.split())
            prev_words = set(prev_lower.split())
            if not new_words or not prev_words:
                continue
            overlap = len(new_words & prev_words)
            overlap_ratio = overlap / min(len(new_words), len(prev_words))
            if overlap_ratio > 0.6:
                result.fail(
                    "Repetition",
                    f"Reply is too similar to a previous message ({overlap_ratio:.0%} word overlap)"
                )
                break
        else:
            result.pass_stage("Repetition")
    else:
        result.pass_stage("Repetition")

    # ── Extra Stage: Pushy phrases (negative sentiment only) ──
    if sentiment == "negative":
        found_pushy = [phrase for phrase in PUSHY_REPLY_PHRASES if phrase in msg_lower]
        if found_pushy:
            result.fail(
                "PushyReply",
                f"Reply tries to overcome objections: {', '.join(found_pushy[:2])}"
            )
        else:
            result.pass_stage("PushyReply")

        # Warn if negative reply is too long (even if under max_chars)
        if len(message) > 150:
            result.warn("Conciseness", "Negative replies should be concise (1-2 sentences)")
    else:
        result.pass_stage("PushyReply")

    # ── Extra Stage: Email-style sign-offs ──
    # LinkedIn DMs should never end with "- Name" or "Best, Name" — it's a
    # classic bot tell. We still strip them in reply_pipeline.strip_signature
    # as a last-resort safety net, but failing here means the Fix stage gets
    # a chance to regenerate a clean message instead.
    _signoff_patterns = [
        r"[-\u2013\u2014]+\s*[A-Z][a-zA-Z'\-]{0,20}\s*\.?\s*$",
        r"\b(?:best|cheers|thanks|regards|kind regards|warm regards|sincerely)"
        r"[,.!]?\s*(?:[A-Z][a-zA-Z'\-]{0,20})?\s*\.?\s*$",
    ]
    _stripped = message.strip()
    for _pat in _signoff_patterns:
        if re.search(_pat, _stripped, re.IGNORECASE):
            result.fail(
                "Signoff",
                "Reply ends with an email-style signature — LinkedIn DMs don't sign off"
            )
            break
    else:
        result.pass_stage("Signoff")

    return result
