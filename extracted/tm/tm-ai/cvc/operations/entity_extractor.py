"""
cvc.operations.entity_extractor — Lightweight NER + relationship mapper.

Foundation Horizon 2: "Relationship mapping: the soul tracks who the
user talks about. People referenced by name get entities with
relationships. 'My wife suggested X' → entity(Anjali, relationship=
partner, cited_in_commit=abc123). Over decades, this becomes the
social graph of a life."

Full NER is overkill for a hobbyist-class CLI tool. We use a
deterministic hybrid:

  1. Capitalized-name candidates — proper nouns in user's messages
     that pass a small stoplist (avoiding "I", "Monday", etc.)
  2. Pronoun/possessive co-reference — "my wife", "my partner",
     "my colleague" sets the relationship for the *next* named
     person in the same sentence.
  3. Possessive patterns — "my <relation> <Name>" or
     "<Name>'s <thing>" — directly assign relationships.
  4. Entity-type hinting — "the <project>", "in <City>" etc.

Output: list of ExtractedEntity dicts ready to merge into UserIdentity
Snapshot via the existing apply_soul_reasoning_response path.

This is intentionally PRAGMATIC — designed to ship, not to be
state-of-the-art NER. Caller can layer an LLM refinement pass on top.
"""
from __future__ import annotations

import logging
import re
import time
from dataclasses import dataclass, field
from typing import Any, Iterable

logger = logging.getLogger("cvc.entity_extractor")

# ── Stoplist: words that LOOK like proper nouns but aren't entities ─────
# hotfix/soul-entity-quality-2026-06-30 — the previous stoplist missed
# sentence-initial question words ("If", "What", "Where") and generic
# English adjectives that get capitalized at the start of a sentence
# ("Honestly", "Basically", "Actually"). Result: the Soul page rendered
# "The", "If", "What", "Honestly", "Soul", "Digital" as people. This
# list now covers those + a broader common-noun block + a "things
# only sometimes capitalized" block.
STOPWORDS: set[str] = {
    # Pronouns + determiners
    "I", "Me", "My", "Mine", "We", "Us", "Our", "You", "Your", "Yours",
    "He", "She", "It", "They", "Them", "Their", "Theirs",
    "This", "That", "These", "Those", "There", "Here", "Where", "When",
    "What", "Which", "Who", "Whom", "Whose", "Why", "How",
    "If", "Then", "Else", "Or", "And", "But", "So", "Yet", "Nor",
    "A", "An", "The", "Some", "Any", "All", "Each", "Every", "No",
    # Common sentence-initial adverbs that get capitalized
    "Honestly", "Basically", "Actually", "Definitely", "Probably",
    "Maybe", "Anyway", "However", "Therefore", "Otherwise", "Although",
    "Meanwhile", "Moreover", "Furthermore", "Nevertheless", "Nonetheless",
    "Consequently", "Subsequently", "Recently", "Previously", "Finally",
    "Unfortunately", "Fortunately", "Hopefully", "Apparently", "Obviously",
    "Essentially", "Practically", "Virtually", "Precisely", "Exactly",
    # Time words
    "Today", "Tomorrow", "Yesterday",
    "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday",
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December",
    # Places / common proper-noun noise
    "India", "USA", "UK", "US", "UAE", "EU",
    "World", "Earth", "Moon", "Sun", "Galaxy", "Universe",
    # Greetings / pleasantries
    "Hi", "Hello", "Hey", "Please", "Thanks", "Thank", "Sorry", "Sure",
    "Yes", "No", "OK", "Ok", "Okay", "True", "False", "Null", "None",
    "Good", "Bad", "Great", "Nice", "Fine", "Cool", "Awesome",
    # Generic software/dev nouns that get capitalized in docs
    "Internet", "Web", "Code", "Bug", "Test", "Tests", "File", "Files",
    "Line", "Lines", "Error", "Errors", "Function", "Method", "Class",
    "Project", "Workspace", "Workspace", "Folder", "Repo", "Branch",
    "Commit", "Commits", "Push", "Pull", "Merge", "Rebase", "Tag",
    "Module", "Package", "Library", "Framework", "Engine", "Service",
    "Server", "Client", "Database", "Table", "Column", "Row", "Field",
    "Variable", "Constant", "String", "Integer", "Boolean", "Array",
    "Loop", "Branch", "Switch", "Case", "Default", "Return", "Import",
    "Export", "Function", "Class", "Object", "Instance", "Property",
    # Tech stack
    "Markdown", "YAML", "JSON", "XML", "HTML", "CSS",
    "Python", "JavaScript", "TypeScript", "Rust", "Go", "Ruby", "Java",
    "C", "Cpp", "Swift", "Kotlin", "Dart", "PHP",
    # AI / CVC-specific (these are tools, not people)
    "CVC", "Sofia", "Hermes", "Claude", "GPT", "Gemini", "OpenAI",
    "Anthropic", "Minimax", "GLM", "Llama", "Copilot", "Sonnet",
    "Nemotron", "ChatGPT", "Grok",
    # CVC subsystem words that appear capitalized but aren't people
    "Soul", "Dashboard", "Gateway", "Agent", "Adapter", "Workspace",
    "Soulware", "Snapshot", "Snapshots", "Dream", "Dreams", "Letter",
    "Letters", "Correction", "Corrections", "Narrative", "Persona",
    "Personas", "Preservation", "Portal", "Overview", "Operations",
    # "Digital" / "Tech" — often part of role names, not people
    "Digital", "Tech", "Mobile", "Web", "Backend", "Frontend", "Fullstack",
    # Tech-org words
    "GitHub", "GitLab", "Bitbucket", "Vercel", "Netlify", "Heroku",
    "Google", "StackOverflow", "Twitter", "Facebook", "Instagram",
    "LinkedIn", "YouTube", "Apple", "Microsoft", "Amazon", "Netflix",
    # Misc
    "CEO", "CTO", "CMO", "CFO", "COO", "VP", "HR", "PR",
}


# ── Common English verbs that get capitalized at sentence start ────
# hotfix/soul-values-and-cleanup-2026-06-30 — the previous stoplist
# missed verbs like "For", "Merging", "Verify", "Show", "Prepare"
# because they aren't typical stopwords but ARE verbs that show up
# at the start of imperative sentences in dev chat. Adding a small
# verb lemma list here kills them.
_VERB_STOPS: set[str] = {
    # Common imperative / present-tense verbs that get sentence-capped
    "Do", "Does", "Did", "Doing",
    "Make", "Makes", "Making", "Made",
    "Get", "Gets", "Getting", "Got",
    "Set", "Sets", "Setting",
    "Go", "Goes", "Going", "Gone",
    "Run", "Runs", "Running", "Ran",
    "Fix", "Fixes", "Fixing", "Fixed",
    "Send", "Sends", "Sending", "Sent",
    "Take", "Takes", "Taking", "Took",
    "Put", "Puts", "Putting",
    "Let", "Lets", "Letting",
    "Try", "Tries", "Trying", "Tried",
    "Keep", "Keeps", "Keeping", "Kept",
    "Hold", "Holds", "Holding", "Held",
    "Save", "Saves", "Saving", "Saved",
    "Load", "Loads", "Loading", "Loaded",
    "Move", "Moves", "Moving", "Moved",
    "Add", "Adds", "Adding", "Added",
    "Read", "Reads", "Reading",
    "Write", "Writes", "Writing", "Wrote", "Written",
    "Update", "Updates", "Updating", "Updated",
    "Delete", "Deletes", "Deleting", "Deleted",
    "Create", "Creates", "Creating", "Created",
    "Build", "Builds", "Building", "Built",
    "Ship", "Ships", "Shipping", "Shipped",
    "Deploy", "Deploys", "Deploying", "Deployed",
    "Push", "Pushes", "Pushing", "Pushed",
    "Pull", "Pulls", "Pulling", "Pulled",
    "Merge", "Merges", "Merging", "Merged",
    "Branch", "Branches", "Branching",
    "Commit", "Commits", "Committing",
    "Verify", "Verifies", "Verifying", "Verified",
    "Validate", "Validates", "Validating", "Validated",
    "Show", "Shows", "Showing", "Showed", "Shown",
    "Hide", "Hides", "Hiding", "Hid",
    "Open", "Opens", "Opening", "Opened",
    "Close", "Closes", "Closing", "Closed",
    "Start", "Starts", "Starting", "Started",
    "Stop", "Stops", "Stopping", "Stopped",
    "End", "Ends", "Ending", "Ended",
    "Check", "Checks", "Checking", "Checked",
    "Confirm", "Confirms", "Confirming", "Confirmed",
    "Cancel", "Cancels", "Canceling", "Cancelled",
    "Apply", "Applies", "Applying", "Applied",
    "Use", "Uses", "Using", "Used",
    "Test", "Tests", "Testing", "Tested",
    "Watch", "Watches", "Watching", "Watched",
    "Look", "Looks", "Looking", "Looked",
    "Find", "Finds", "Finding", "Found",
    "Search", "Searches", "Searching", "Searched",
    "Learn", "Learns", "Learning", "Learned",
    "Teach", "Teaches", "Teaching", "Taught",
    "Help", "Helps", "Helping", "Helped",
    "Need", "Needs", "Needing", "Needed",
    "Want", "Wants", "Wanting", "Wanted",
    "Have", "Has", "Having", "Had",
    "Say", "Says", "Saying", "Said",
    "Tell", "Tells", "Telling", "Told",
    "Ask", "Asks", "Asking", "Asked",
    "Think", "Thinks", "Thinking", "Thought",
    "Know", "Knows", "Knowing", "Knew", "Known",
    "See", "Sees", "Seeing", "Saw", "Seen",
    "Understand", "Understands", "Understanding", "Understood",
    "Hear", "Hears", "Hearing", "Heard",
    "Feel", "Feels", "Feeling", "Felt",
    "Bring", "Brings", "Bringing", "Brought",
    "Leave", "Leaves", "Leaving", "Left",
    "Stay", "Stays", "Staying", "Stayed",
    "Come", "Comes", "Coming", "Came",
    "Give", "Gives", "Giving", "Gave", "Given",
    "Take", "Took", "Taken",
    "Prepare", "Prepares", "Preparing", "Prepared",
    "Plan", "Plans", "Planning", "Planned",
    "For",  # very common sentence-starter: "For now...", "For the record..."
    "Not",  # "Not just X, but Y"
    "Also", "Just", "Still", "Already", "Yet",
    "Even", "Only", "Both", "Either", "Neither",
    # Imperative / modal / auxiliary verbs that get capitalized at start
    "Manual",  # "Manual cleanup..."
    "Can", "Could", "Would", "Should", "Might", "Must", "May", "Will",
    "Is", "Are", "Was", "Were", "Been", "Being", "Be",
    "Has", "Have", "Had",
    "Does", "Did",  # already in DO/DOES block above
    "One", "Two", "Three",  # sentence-starter numerals
    "There", "Here",  # already in stoplist via "There" but reaffirm as verbs
    "Now", "Then", "Once", "Ever", "Never", "Always", "Often", "Sometimes",
}


# ── Owner skip-list ────────────────────────────────────────────────
# hotfix/soul-values-and-cleanup-2026-06-30 — the user's own name
# shouldn't show up as a person-entity in their own soul model. The
# AI cleanup pass will populate this from user_model.name + a few
# common variants ("Jai", "jaimeena", "@mannuking1019", etc.) at
# runtime; we hard-code the most common ones here so the heuristic
# pass can drop them immediately, before the AI cleanup runs.
OWNER_SKIP_NAMES: set[str] = {
    "Jai", "Jaimeena", "Meena", "Mannuking", "Mannu",
    # Jai's handles
    "I", "Me", "My",
}


def _is_owner_name(name: str) -> bool:
    """Return True if ``name`` is one of the user's own handles /
    display names. We never record the user as a 'mentioned person'
    in their own soul model — the soul is theirs, they are the
    silent author."""
    if not name:
        return False
    n = name.strip()
    if not n:
        return False
    if n in OWNER_SKIP_NAMES:
        return True
    # Compare lowercase stripped
    if n.lower() in {s.lower() for s in OWNER_SKIP_NAMES}:
        return True
    return False


# Stopwords union: hard rejects + verb rejects.
EFFECTIVE_STOPWORDS: set[str] = STOPWORDS | _VERB_STOPS


# hotfix/soul-values-and-cleanup-2026-06-30 — runtime-injected owner
# name. The CLI / dashboard can set this when it knows who the user
# is (e.g. from user_model.name or session metadata). Until then we
# fall back to the OWNER_SKIP_NAMES hardcoded list.
_USER_NAME_FROM_MODEL: str = ""


def set_owner_name(name: str) -> None:
    """Inject the user's display name into the owner skip-list at
    runtime. Called once per process when the gateway knows who the
    user is (e.g. from the loaded user_model). Safe to call
    repeatedly; safe to call with empty/None."""
    global _USER_NAME_FROM_MODEL
    if name:
        _USER_NAME_FROM_MODEL = str(name).strip()
        OWNER_SKIP_NAMES.add(_USER_NAME_FROM_MODEL)


# ── Soft-stopwords: capitalized-but-usually-not-people ──────────────
# Lower-confidence. The extractor still records them but with very
# low confidence and an ``entity_type`` override. Used by the entity
# type hint to disambiguate "Soul" (the soul, a subsystem) from "Sofia"
# (a person).
SOFT_NAME_OVERRIDES: dict[str, str] = {
    "Soul": "system",
    "Dashboard": "system",
    "Gateway": "system",
    "Adapter": "system",
    "Snapshot": "system",
    "Soulware": "system",
    "Digital": "role",      # "Digital CMO" etc.
    "Backend": "role",
    "Frontend": "role",
    "Fullstack": "role",
    "Mobile": "role",
}

# ── Relationship vocabulary ─────────────────────────────────────────────
# Maps user phrases to canonical Entity.relationship values.
RELATIONSHIP_PATTERNS: list[tuple[re.Pattern, str]] = [
    # Family
    (re.compile(r"\bmy\s+wife\b", re.I), "wife"),
    (re.compile(r"\bmy\s+husband\b", re.I), "husband"),
    (re.compile(r"\bmy\s+partner\b", re.I), "partner"),
    (re.compile(r"\bmy\s+(?:girl|boy)?friend\b", re.I), "partner"),
    (re.compile(r"\bmy\s+(?:mum|mom|mother|ma)\b", re.I), "mother"),
    (re.compile(r"\bmy\s+(?:dad|father|pa|papa)\b", re.I), "father"),
    (re.compile(r"\bmy\s+(?:sis|sister)\b", re.I), "sister"),
    (re.compile(r"\bmy\s+(?:bro|brother)\b", re.I), "brother"),
    (re.compile(r"\bmy\s+(?:son|daughter|kid|child)\b", re.I), "child"),
    (re.compile(r"\bmy\s+(?:uncle|aunt)\b", re.I), "uncle_or_aunt"),
    (re.compile(r"\bmy\s+(?:cousin|nephew|niece)\b", re.I), "extended_family"),
    # Work
    (re.compile(r"\bmy\s+(?:colleague|coworker|co-?worker)\b", re.I), "colleague"),
    (re.compile(r"\bmy\s+(?:boss|manager|lead)\b", re.I), "manager"),
    (re.compile(r"\bmy\s+(?:client|customer)\b", re.I), "client"),
    (re.compile(r"\bmy\s+(?:teammate|co-?founder)\b", re.I), "cofounder"),
    (re.compile(r"\bmy\s+cto\b", re.I), "colleague"),
    (re.compile(r"\bmy\s+cmo\b", re.I), "colleague"),
    # Pets
    (re.compile(r"\bmy\s+(?:dog|puppy)\b", re.I), "dog"),
    (re.compile(r"\bmy\s+(?:cat|kitten)\b", re.I), "cat"),
    (re.compile(r"\bmy\s+(?:pet|bird|fish|hamster)\b", re.I), "pet"),
]

# Posessive-style: "Name's wife" → relationship mapping
POSSESSIVE_NAME_RE = re.compile(
    r"\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)'s\s+([a-z]+)\b"
)


@dataclass
class ExtractedEntity:
    """A candidate entity pulled out of one user message."""

    name: str
    entity_type: str = "person"
    relationship: str = ""
    context_snippet: str = ""
    source_message_idx: int = -1
    confidence: float = 0.5
    attributes: dict[str, str] = field(default_factory=dict)


def _looks_like_name(token: str) -> bool:
    """Capitalized, ≥2 chars, alphabetic, not in stoplist.

    hotfix/soul-entity-quality-2026-06-30 — also rejects:
      - single-character tokens (e.g. "A" from "A link")
      - common adverbs / conjunctions that escape the stoplist via
        unusual capitalisation (defensive double-check)
    """
    if not token or len(token) < 2:
        return False
    if not token[0].isupper():
        return False
    if not all(c.isalpha() or c == "-" or c == "'" for c in token):
        return False
    if token in EFFECTIVE_STOPWORDS or token.lower() in {s.lower() for s in EFFECTIVE_STOPWORDS}:
        return False
    # Reject ALL-CAPS (likely acronyms)
    if token.isupper() and len(token) > 2:
        return False
    return True


def _looks_like_project(token: str) -> bool:
    """Detect PascalCase / camelCase compound words like 'HydroPlus',
    'NextCloud', 'lvl360', 'iPhone'.

    Used as a positive signal (not a filter) — overrides the default
    ``person`` type when matched. Capital letters mid-word indicate
    an identifier that humans use as a brand or project name."""
    if not token or len(token) < 3:
        return False
    # PascalCase: lower→upper transition (HydroPlus, NextCloud, WebUI)
    if re.search(r"[a-z][A-Z]", token):
        return True
    # All-lowercase identifier with embedded digits (lvl360, node18)
    if token.islower() and re.search(r"\d", token):
        return True
    # Mixed alphanumeric where digits appear (e.g. "VSCode", "Web3")
    return False


def _looks_like_role(token: str) -> bool:
    """Detect role/title tokens: 'CMO', 'CTO', 'CEO' (acronyms in
    ALL-CAPS length 2-4). The stoplist already filters these for
    PERSON extraction, but the type hint still wants to recognise
    them so e.g. 'Ajay is the Digital CMO' classifies CMO as role,
    not as a person."""
    if not token or len(token) > 4 or len(token) < 2:
        return False
    return token.isupper() and token.isalpha()


def _sentence_split(text: str) -> list[str]:
    """Crude sentence splitter — enough for relationship co-reference."""
    parts = re.split(r"(?<=[.!?])\s+", text)
    return [p.strip() for p in parts if p.strip()]


def _scan_sentence_for_relationship(sentence: str) -> tuple[str, int]:
    """Find the first matching relationship phrase and return its end index.

    Returns (relationship, end_position_in_sentence).
    """
    for pattern, rel in RELATIONSHIP_PATTERNS:
        m = pattern.search(sentence)
        if m:
            return rel, m.end()
    return "", -1


def _extract_names_in_text(sentence: str, after_pos: int = 0) -> list[tuple[str, int]]:
    """Find capitalized names in the sentence after the given position.

    Returns [(name, absolute_position_in_sentence)].

    hotfix/soul-entity-quality-2026-06-30 — extended to recognise
    PascalCase (``HydroPlus``), camelCase (``webUI``), and lowercase
    identifier-with-digits (``lvl360``, ``node18``). These are common
    project / product names in dev chat and were dropped by the
    previous "Capital + lowercase only" regex.
    """
    results: list[tuple[str, int]] = []
    rest = sentence[after_pos:]
    # 1. PascalCase / multi-word proper noun: FirstName or FirstName LastName
    #    OR PascalCase identifier (HydroPlus, NextCloud)
    for m in re.finditer(
        r"\b([A-Z][a-zA-Z0-9]*(?:[A-Z][a-z]*)*(?:\s+[A-Z][a-zA-Z0-9]*)?)\b",
        rest,
    ):
        name = m.group(1)
        # First token (and last token if multi-word) must look like a name
        first = name.split()[0]
        last = name.split()[-1]
        if _looks_like_name(first) or _looks_like_project(first) or first in SOFT_NAME_OVERRIDES:
            if _looks_like_name(last) or _looks_like_project(last) or last in SOFT_NAME_OVERRIDES:
                results.append((name, m.start() + after_pos))
    # 2. Lowercase identifier with embedded digits (lvl360, node18)
    for m in re.finditer(r"\b([a-z][a-z0-9]*\d[a-z0-9]*)\b", rest):
        name = m.group(1)
        # Drop obvious non-entities: pure numbers, very short, common words
        if len(name) < 3:
            continue
        if name in {"the", "and", "for", "with"}:
            continue
        results.append((name, m.start() + after_pos))
    return results


def _entity_type_hint(sentence: str, name: str) -> str:
    """Guess entity_type from sentence context + name shape.

    hotfix/soul-entity-quality-2026-06-30 — the previous version only
    matched a handful of weak patterns and defaulted EVERYTHING to
    ``person``. New priority order:

      1. Soft override (e.g. "Soul" → "system", "Digital" → "role")
      2. PascalCase / camelCase / lvl360-shaped name → "project"
      3. ALL-CAPS acronym 2-4 chars → "role"
      4. Sentence-context patterns:
         - "build/ship/wrote X app/service/library" → project
         - "in/at/from X" or city verbs → place
         - "my dog/cat/pet" → pet
         - "company/startup/org" → organization
      5. Default → person
    """
    s = sentence.lower()

    # 1. Soft overrides (Soul → system, Digital → role)
    if name in SOFT_NAME_OVERRIDES:
        return SOFT_NAME_OVERRIDES[name]

    # 2. Project-shape names
    if _looks_like_project(name):
        return "project"

    # 3. Acronym roles (CMO, CTO, CEO, VP)
    if _looks_like_role(name):
        return "role"

    # 4. Context patterns
    if re.search(
        r"\b(?:app|service|system|tool|library|framework|portal|product|project)\b",
        s,
    ) and re.search(r"\b(build|ship|wrote|built|coded|launched|deployed|own)\b", s):
        return "project"
    if re.search(r"\b(?:in|at|from|live in|moved to|visited)\s+" + re.escape(name.lower()), s):
        return "place"
    if re.search(r"\b(?:dog|cat|pet|puppy|kitten)\b", s):
        return "pet"
    if re.search(r"\b(?:company|startup|team|org|organization)\b", s):
        return "organization"
    return "person"


def extract_from_message(text: str, message_idx: int = 0) -> list[ExtractedEntity]:
    """Extract entities from one user message.

    Algorithm:
      1. Split into sentences
      2. For each sentence, find relationship phrases
      3. Find the FIRST named entity after the relationship position
         (not all names — only the one being related to)
      4. Also scan for bare names (no relationship → lower confidence)
    """
    if not text or not text.strip():
        return []
    results: list[ExtractedEntity] = []

    # hotfix/soul-values-and-cleanup-2026-06-30 — drop the user's own
    # name (and handles) from extraction. The soul shouldn't track the
    # user as a 'mentioned person' — they ARE the soul's owner.
    if text and _USER_NAME_FROM_MODEL:
        OWNER_SKIP_NAMES.add(_USER_NAME_FROM_MODEL)

    for sentence in _sentence_split(text):
        rel, rel_end = _scan_sentence_for_relationship(sentence)
        # Names WITH a relationship (high confidence) — ONLY the first name
        # immediately after the relationship phrase is the referent.
        # Other names in the same sentence get bare-name treatment.
        first_rel_name: tuple[str, int] | None = None
        if rel:
            names_after_rel = _extract_names_in_text(sentence, after_pos=rel_end)
            if names_after_rel:
                name, pos = names_after_rel[0]
                first_rel_name = (name, pos)
                results.append(
                    ExtractedEntity(
                        name=name,
                        entity_type=_entity_type_hint(sentence, name),
                        relationship=rel,
                        context_snippet=sentence[:200],
                        source_message_idx=message_idx,
                        confidence=0.8 if rel in {"wife", "husband", "partner", "mother", "father", "child"} else 0.6,
                    )
                )

        # Possessive pattern: "Anjali's project" → Anjali owns something
        for m in POSSESSIVE_NAME_RE.finditer(sentence):
            owner, thing = m.group(1), m.group(2)
            if _looks_like_name(owner):
                # Skip if we already attached a relationship to this name
                if first_rel_name and first_rel_name[0] == owner:
                    continue
                # hotfix/soul-values-and-cleanup-2026-06-30 — also
                # drop the user's own name from possessive extractions.
                if _is_owner_name(owner):
                    continue
                results.append(
                    ExtractedEntity(
                        name=owner,
                        entity_type="person",
                        relationship="known_person",
                        context_snippet=sentence[:200],
                        source_message_idx=message_idx,
                        confidence=0.5,
                        attributes={"possessive_thing": thing},
                    )
                )

        # Bare names (no relation) — names in this sentence that
        # weren't already tagged with a relationship.
        for name, _ in _extract_names_in_text(sentence, after_pos=0):
            if first_rel_name and first_rel_name[0] == name:
                continue  # already tagged
            # hotfix/soul-values-and-cleanup-2026-06-30 — drop the
            # user's own name and any tokens that match a soft-override
            # type but the user never wants as a person entity
            # (system/role tokens).
            if _is_owner_name(name):
                continue
            results.append(
                ExtractedEntity(
                    name=name,
                    entity_type=_entity_type_hint(sentence, name),
                    relationship="mentioned",
                    context_snippet=sentence[:200],
                    source_message_idx=message_idx,
                    confidence=0.3,
                )
            )

    return results


def extract_from_session(messages: Iterable[dict]) -> list[ExtractedEntity]:
    """Extract entities from a full session (user messages only)."""
    out: list[ExtractedEntity] = []
    seen: dict[str, ExtractedEntity] = {}  # dedup by name

    for i, m in enumerate(messages):
        if m.get("role") not in ("user", "human"):
            continue
        text = m.get("content") or ""
        for ent in extract_from_message(text, message_idx=i):
            key = ent.name.lower()
            if key not in seen:
                seen[key] = ent
            else:
                # Keep the highest-confidence extraction
                if ent.confidence > seen[key].confidence:
                    seen[key] = ent
                # Bump mention_count via attributes
                seen[key].attributes["mention_count"] = str(
                    int(seen[key].attributes.get("mention_count", "1")) + 1
                )
    return list(seen.values())


def cleanup_snapshot_entities(snapshot) -> tuple[int, int]:
    """hotfix/soul-values-and-cleanup-2026-06-30 — purge garbage that
    predates our stopword / owner / soft-override filters.

    Runs against an in-memory ``UserIdentitySnapshot`` (NOT disk). The
    caller decides whether to persist the cleaned snapshot. Three
    passes:

      1. Drop any entity whose name matches the current EFFECTIVE_STOPWORDS
         (capitalised or not). Kills ``The``, ``Honestly``, ``If``,
         ``What``, ``Where``, ``Soul``, ``Digital``, etc.
      2. Drop any entity whose name matches the OWNER skip-list
         (``Jai``, ``Jaimeena``, ``Me`` …). The owner is never a
         'mentioned person' in their own soul.
      3. Reclassify any entity whose name matches SOFT_NAME_OVERRIDES
         to the right ``entity_type`` (Soul→system, Digital→role). Even
         if we kept these, they'd be wrong as ``person``.
      4. Dedup by lowercase name — collapse Jai/Jai/Jai into one row,
         merging mention_count and last_mentioned.

    Returns ``(dropped_count, merged_count)``.
    """
    if snapshot is None:
        return (0, 0)
    try:
        from cvc.core.user_model import Entity  # noqa: F401
    except Exception:
        pass

    lowered_stops = {s.lower() for s in EFFECTIVE_STOPWORDS}
    lowered_owner = {s.lower() for s in OWNER_SKIP_NAMES}

    before = list(snapshot.entities)
    after: list = []
    by_key: dict[str, Any] = {}
    dropped = 0
    merged = 0

    # Lowercase so we drop "Jai" / "jAi" / "JAI" alike
    for ent in before:
        name = (ent.name or "").strip()
        if not name:
            dropped += 1
            continue
        lname = name.lower()

        # Pass 1+2: drop stopwords and owner names
        if lname in lowered_stops or lname in lowered_owner:
            dropped += 1
            continue

        # Pass 3: reclassify soft overrides — keep the entity but fix type
        if name in SOFT_NAME_OVERRIDES:
            ent.entity_type = SOFT_NAME_OVERRIDES[name]
            # Anything that ended up as "person" but is a system/role
            # token is misleading on the Soul page — drop it. Soul/Dashboard
            # are not entities, they're tools.
            if SOFT_NAME_OVERRIDES[name] in {"system"} and ent.relationship in (
                "mentioned",
                "",
                "known_person",
            ):
                # Drop subsystems from the entity list entirely
                dropped += 1
                continue
        # Acronym roles (CMO/CTO/CEO) — never a 'person' on the soul page
        if _looks_like_role(name) and ent.entity_type == "person":
            ent.entity_type = "role"

        # Pass 4: dedup by lowercase name
        if lname in by_key:
            existing = by_key[lname]
            existing.mention_count = int(existing.mention_count or 1) + int(
                ent.mention_count or 1
            )
            existing.last_mentioned = max(
                float(existing.last_mentioned or 0),
                float(ent.last_mentioned or 0),
            )
            # Upgrade relationship if we now know it better
            if (
                ent.relationship
                and ent.relationship not in ("mentioned", "")
                and (
                    not existing.relationship
                    or existing.relationship in ("mentioned", "known_person")
                )
            ):
                existing.relationship = ent.relationship
            # Merge context snippets (cap at 5)
            seen_snippets = set(existing.context_snippets or [])
            for s in ent.context_snippets or []:
                if s and s not in seen_snippets and len(existing.context_snippets) < 5:
                    existing.context_snippets.append(s)
                    seen_snippets.add(s)
            merged += 1
            continue

        by_key[lname] = ent
        after.append(ent)

    snapshot.entities = after
    if dropped or merged:
        logger.info(
            "entity_extractor.cleanup_snapshot_entities: dropped=%d merged=%d (before=%d after=%d)",
            dropped,
            merged,
            len(before),
            len(after),
        )
    return (dropped, merged)


def merge_into_snapshot(extracted: list[ExtractedEntity], snapshot) -> int:
    """Merge extracted entities into a UserIdentitySnapshot, dedup by name.

    Returns the count of NEW entities added (existing ones get mention_count
    bumped).
    """
    added = 0
    from cvc.core.user_model import Entity

    # Index existing entities by lowercased name
    existing = {e.name.lower(): e for e in snapshot.entities}

    for ext in extracted:
        key = ext.name.lower()
        if key in existing:
            # Bump mention count
            e = existing[key]
            e.mention_count = int(e.mention_count or 1) + 1
            e.last_mentioned = time.time()
            # Upgrade relationship if we now know it better
            if ext.relationship and ext.relationship not in ("mentioned", "") and (
                not e.relationship or e.relationship in ("mentioned", "known_person")
            ):
                e.relationship = ext.relationship
            # Append context snippet (cap at 5)
            if ext.context_snippet and len(e.context_snippets) < 5:
                e.context_snippets.append(ext.context_snippet)
            continue
        # Add new entity
        snapshot.entities.append(
            Entity(
                name=ext.name,
                entity_type=ext.entity_type,
                relationship=ext.relationship,
                context_snippets=[ext.context_snippet] if ext.context_snippet else [],
                attributes=ext.attributes,
            )
        )
        added += 1
    return added