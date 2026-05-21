"""Spec → ProjectPlan decomposer.

The first stage of the dynamic builder pipeline. Takes a free-form task
description (the user's spec) and produces a structured `ProjectPlan`
with a list of `Feature` objects and a `StackProfile`. Both are derived
from the spec via the LLM with deterministic fallback for malformed
output so the pipeline never aborts.

This replaces the hardcoded `plan_*()` functions in `principal_engineer`
which always returned the same file list regardless of the spec — the
root cause of the "I asked for an AI ad platform and got generic
login/register" failure mode.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from typing import Callable, Literal


GenerateFn = Callable[[str], str]
Layer = Literal["frontend", "backend", "shared", "infra"]

_VALID_LAYERS: tuple[Layer, ...] = ("frontend", "backend", "shared", "infra")


@dataclass
class Feature:
    """A single user-facing or infrastructure capability.

    `acceptance` items become the basis of generated tests in the TDD
    loop, so they should be checkable observations, not vibes.
    """

    name: str  # slug, e.g. "campaign_builder"
    description: str  # one-line human summary
    layer: Layer  # routes the feature to frontend/, backend/, etc.
    acceptance: list[str] = field(default_factory=list)


@dataclass
class StackProfile:
    """Frameworks chosen for each tier. None = not present in this project."""

    frontend: str | None = None  # e.g. "react", "react-native-web", "nextjs"
    backend: str | None = None  # e.g. "fastapi", "django", "spring-boot"
    database: str | None = None  # e.g. "postgres", "sqlite", "mongo"
    cache: str | None = None  # e.g. "redis", "memcached"
    queue: str | None = None  # e.g. "celery", "rq", "sqs"


@dataclass
class ProjectPlan:
    title: str
    features: list[Feature]
    stack: StackProfile
    # task_type routes the rest of the pipeline. "webapp" = existing
    # behavior (frontend/backend scaffold). "game" = sage/games pipeline
    # (engine adapter + asset generators). Default preserves backwards
    # compatibility for every existing caller.
    task_type: str = "webapp"
    # When `task_type == "game"`, this holds the parsed GameRequest so the
    # caller doesn't need to re-parse the prompt. None for non-game tasks.
    game_request: "object | None" = None  # forward ref, optional


# ──────────────────────── parsing helpers ───────────────────────────────


_JSON_FENCE = re.compile(r"```(?:json)?\s*(.+?)\s*```", re.DOTALL)


def _slugify(name: str) -> str:
    """Normalise a feature name to a safe lower_snake_case slug."""
    s = re.sub(r"[^A-Za-z0-9]+", "_", name.strip()).strip("_").lower()
    return s or "feature"


def _extract_json_block(text: str) -> str:
    """Pull a JSON array/object out of LLM output that may be wrapped in prose."""
    if not text:
        return ""
    # Try fenced code block first
    m = _JSON_FENCE.search(text)
    if m:
        return m.group(1)
    # Otherwise find the first { or [ and matching closer
    for opener, closer in (("[", "]"), ("{", "}")):
        start = text.find(opener)
        end = text.rfind(closer)
        if start != -1 and end != -1 and end > start:
            return text[start : end + 1]
    return text


def parse_features_json(raw: str) -> list[Feature]:
    """Parse a JSON array of feature dicts. Returns [] on malformed input.

    Resilient to: prose wrapping, code fences, missing fields, invalid
    layer values. Each entry must have a `name` to be kept.
    """
    block = _extract_json_block(raw)
    if not block:
        return []
    try:
        data = json.loads(block)
    except (json.JSONDecodeError, ValueError):
        return []
    if not isinstance(data, list):
        return []
    out: list[Feature] = []
    for entry in data:
        if not isinstance(entry, dict):
            continue
        name_raw = entry.get("name")
        if not name_raw or not isinstance(name_raw, str):
            continue
        layer = entry.get("layer", "backend")
        if layer not in _VALID_LAYERS:
            layer = "backend"
        acceptance = entry.get("acceptance") or []
        if not isinstance(acceptance, list):
            acceptance = []
        out.append(
            Feature(
                name=_slugify(name_raw),
                description=str(entry.get("description", "")),
                layer=layer,  # type: ignore[arg-type]
                acceptance=[str(a) for a in acceptance],
            )
        )
    return out


def parse_stack_json(raw: str) -> StackProfile:
    """Parse a JSON object describing the stack. Returns defaults on bad input."""
    block = _extract_json_block(raw)
    if not block:
        return StackProfile()
    try:
        data = json.loads(block)
    except (json.JSONDecodeError, ValueError):
        return StackProfile()
    if not isinstance(data, dict):
        return StackProfile()

    def _get(key: str) -> str | None:
        val = data.get(key)
        if isinstance(val, str) and val.strip():
            return val.strip().lower()
        return None

    # Normalize frontend aliases — LLMs often return "react-native" but the
    # canonical key throughout sage is "react-native-web" (Expo SDK with web
    # support). Any mobile-first React Native value should map there.
    _FRONTEND_ALIASES: dict[str, str] = {
        "react-native": "react-native-web",
        "reactnative": "react-native-web",
        "expo": "react-native-web",
        "expo-router": "react-native-web",
    }
    raw_frontend = _get("frontend")
    frontend = _FRONTEND_ALIASES.get(raw_frontend or "", raw_frontend)

    return StackProfile(
        frontend=frontend,
        backend=_get("backend"),
        database=_get("database"),
        cache=_get("cache"),
        queue=_get("queue"),
    )


# ──────────────────────── extraction (LLM-driven) ───────────────────────


_FEATURES_PROMPT = """You are decomposing a software project spec into features.

Output a JSON array. Each entry must have:
  - name: short slug (e.g. "campaign_builder", "ad_content_generator")
  - description: one-line summary
  - layer: one of "frontend", "backend", "shared", "infra"
  - acceptance: array of testable observations (each should be checkable
                by a single automated test — not vibes)

Rules:
  - Produce AT LEAST ONE feature per numbered section, lettered section, or
    distinct topic in the spec. If the spec has 15 sections, produce ≥15
    features.
  - Split big sections into multiple finer features (e.g. "Analytics
    Dashboard with 18 metrics" → one feature per metric or per metric
    group).
  - Group every feature into the correct layer (UI screens → frontend,
    API endpoints / data models / business logic → backend, shared types
    / utilities → shared, Docker/CI/secrets → infra).
  - Output ONLY the JSON array. No prose.

Spec:
{spec}
"""


_STACK_PROMPT = """You are choosing the technical stack for a software spec.

Output a single JSON object with these string keys (or null):
  - frontend: framework name — MUST be one of the exact strings below:
              "react-native-web" — React Native + Expo SDK (iOS/Android/Web). Use
                  this for ANY spec mentioning React Native, Expo, mobile app,
                  cross-platform app. NEVER use "react-native" (wrong key).
              "react" — plain Vite+React web app (no mobile)
              "nextjs" — Next.js SSR web app
              "vue", "svelte" — other web frameworks
              "flutter" — Dart/Flutter
              "ios-swift" — native iOS Swift
              "android-compose" — Jetpack Compose Android
              null — if the project has no frontend
  - backend:  framework name (e.g. "fastapi", "django", "spring-boot",
              "express", "rust-axum", "go-microservices") or null
  - database: db name (e.g. "postgres", "mysql", "sqlite", "mongo") or null
  - cache:    cache name (e.g. "redis", "memcached") or null
  - queue:    queue name (e.g. "celery", "rq", "sqs", "kafka") or null

IMPORTANT: For React Native / mobile / cross-platform apps ALWAYS output
"react-native-web" (NOT "react-native", NOT "expo"). This is the canonical key.

Prefer the explicit choices in the spec. If the spec is ambiguous, pick
the most common production-grade option for that domain.

Output ONLY the JSON object. No prose.

Spec:
{spec}
"""


def _truncate_for_prompt(spec: str, max_chars: int = 6000) -> str:
    """Keep large specs from blowing the LLM context window.

    Strategy: keep head and tail (specs usually have the title and
    feature list at top, summary/requirements at bottom). Loses middle
    detail but never crashes.
    """
    if len(spec) <= max_chars:
        return spec
    half = max_chars // 2 - 50
    return spec[:half] + "\n\n...[truncated]...\n\n" + spec[-half:]


def extract_features(spec: str, generate: GenerateFn, *, max_retries: int = 3) -> list[Feature]:
    """Get the feature list, retrying on malformed JSON, falling back to keywords."""
    prompt = _FEATURES_PROMPT.format(spec=_truncate_for_prompt(spec))
    last_raw = ""
    for _ in range(max_retries):
        raw = generate(prompt)
        last_raw = raw
        features = parse_features_json(raw)
        if features:
            return features
    # All LLM attempts failed — fall back to spec-only heuristic so we
    # never return an empty plan. The user explicitly wants every
    # numbered section to become a feature.
    return _heuristic_features(spec) or _heuristic_features(last_raw) or [
        Feature(name="core", description="Primary feature set", layer="backend")
    ]


def extract_stack(spec: str, generate: GenerateFn, *, max_retries: int = 3) -> StackProfile:
    """Get the stack profile, retrying on bad JSON, falling back to keyword detection."""
    prompt = _STACK_PROMPT.format(spec=_truncate_for_prompt(spec))
    for _ in range(max_retries):
        raw = generate(prompt)
        stack = parse_stack_json(raw)
        # Accept the LLM stack only if it picked at least one tier.
        if stack.frontend or stack.backend:
            return stack
    return _heuristic_stack(spec)


def decompose_spec(spec: str, generate: GenerateFn) -> ProjectPlan:
    """Top-level entry: spec text → ProjectPlan.

    Classifies task_type up front. Game prompts skip the webapp-style
    feature/stack decomposition because the game pipeline does its own
    decomposition keyed on engine + genre.
    """
    # Game-prompt detection runs before feature extraction. We pass the
    # `generate` callable so the detector's LLM fallback can fire on
    # ambiguous prompts. Regex-first inside, so the common path is cheap.
    from sage.games.detector import classify_prompt
    task_type, game_request = classify_prompt(spec, generate=generate)
    if task_type == "game":
        return ProjectPlan(
            title=_derive_title(spec) or "Sage Game",
            features=[],
            stack=StackProfile(),
            task_type="game",
            game_request=game_request,
        )

    features = extract_features(spec, generate)
    stack = extract_stack(spec, generate)
    title = _derive_title(spec)
    return ProjectPlan(
        title=title, features=features, stack=stack, task_type="webapp",
    )


# ──────────────────────── heuristic fallbacks ───────────────────────────


_TITLE_RE = re.compile(r"^\s*(?:#\s+)?(.{5,80}?)[\n.:]", re.MULTILINE)


def _derive_title(spec: str) -> str:
    """Pull a title from the first non-trivial line of the spec."""
    if not spec:
        return "project"
    m = _TITLE_RE.search(spec.strip())
    if m:
        candidate = m.group(1).strip()
        if candidate and len(candidate) > 4:
            return candidate
    return spec.strip().split("\n", 1)[0].strip()[:80] or "project"


# Map of (keyword pattern, default-layer, default-acceptance-template) per
# common feature concept. The fallback walks the spec, finds every match,
# and emits a Feature for each.
_FEATURE_KEYWORDS: tuple[tuple[re.Pattern[str], str, Layer, str], ...] = (
    (re.compile(r"\b(?:user\s+)?registration\b", re.I), "registration",
     "backend", "POST /auth/register creates a user and returns success"),
    (re.compile(r"\blogin\b|\bsign[- ]?in\b", re.I), "login",
     "backend", "POST /auth/login returns a JWT for valid credentials"),
    (re.compile(r"\b(?:jwt|oauth2?|authentication)\b", re.I), "authentication",
     "backend", "Protected routes require a valid JWT"),
    (re.compile(r"\brbac\b|role[- ]based", re.I), "rbac",
     "backend", "Roles gate access to admin endpoints"),
    (re.compile(r"\bdashboard\b", re.I), "dashboard",
     "frontend", "Dashboard renders KPI cards from the API"),
    (re.compile(r"\bcampaign\s+builder\b", re.I), "campaign_builder",
     "backend", "POST /campaigns creates a campaign with objective + audience"),
    (re.compile(r"\bad\s+content\b|content\s+generator", re.I), "ad_content_generator",
     "backend", "POST /content/generate returns headlines + body copy"),
    (re.compile(r"social\s+media\s+management", re.I), "social_media_management",
     "backend", "POST /social/connect links an account, GET /social/accounts lists them"),
    (re.compile(r"content\s+calendar|posting\s+schedule", re.I), "content_calendar",
     "backend", "GET /calendar returns scheduled posts grouped by date"),
    (re.compile(r"\bseo\b|search\s+engine", re.I), "seo_tools",
     "backend", "POST /seo/brief returns a content brief for a keyword"),
    (re.compile(r"\baso\b|app\s+store\s+optimization", re.I), "aso_tools",
     "backend", "POST /aso/title returns app title suggestions"),
    (re.compile(r"\banalytics\b|metrics", re.I), "analytics",
     "backend", "GET /metrics returns time-series CTR/CPC/CPA"),
    (re.compile(r"optimization\s+agent|auto.*optimi", re.I), "optimization_agent",
     "backend", "POST /agent/run produces actionable recommendations"),
    (re.compile(r"webhook", re.I), "webhooks",
     "backend", "POST /webhooks/{provider} dispatches to the matching handler"),
    (re.compile(r"\bbilling\b|stripe|subscription", re.I), "billing",
     "backend", "POST /billing/subscribe creates a Stripe subscription"),
    (re.compile(r"\bnotification", re.I), "notifications",
     "backend", "GET /notifications returns unread items"),
    (re.compile(r"\bsettings\b", re.I), "settings",
     "frontend", "Settings screen lets the user update profile fields"),
    (re.compile(r"\btraffic\b|growth", re.I), "traffic_growth",
     "backend", "POST /traffic/analyze returns growth recommendations"),
    (re.compile(r"\bintegration\b|api\s+connect", re.I), "integrations",
     "backend", "GET /integrations lists available providers"),
)


_NUMBERED_SECTION_RE = re.compile(
    r"(?m)^\s*(?:\d+[.)]|[-*])\s+([A-Z][^\n]{3,80})"
)


def _heuristic_features(spec: str) -> list[Feature]:
    """Keyword + section-header extraction used when the LLM fails entirely.

    Two strategies, both contribute:
      1. Numbered/bulleted section headers → one feature per section.
      2. Keyword matches → one feature per matched concept.
    Results are deduped by slug.
    """
    if not spec:
        return []
    seen: dict[str, Feature] = {}

    for match in _NUMBERED_SECTION_RE.finditer(spec):
        header = match.group(1).strip()
        slug = _slugify(header)
        if slug not in seen:
            layer: Layer = "frontend" if re.search(
                r"dashboard|screen|view|ui\b", header, re.I
            ) else "backend"
            seen[slug] = Feature(
                name=slug,
                description=header,
                layer=layer,
                acceptance=[f"{header} is implemented per the spec"],
            )

    for pattern, slug, layer, acceptance in _FEATURE_KEYWORDS:
        if pattern.search(spec) and slug not in seen:
            seen[slug] = Feature(
                name=slug,
                description=slug.replace("_", " ").title(),
                layer=layer,
                acceptance=[acceptance],
            )
    return list(seen.values())


# Keyword-based stack detection mirrors `principal_engineer.detect_stack`
# but produces a `StackProfile` (frontend + backend), not a single label.
_FRONTEND_KEYWORDS: tuple[tuple[str, list[str]], ...] = (
    ("react-native-web", [
        "react native", "react-native", "expo", "expo-router", "expo router",
        "react native web", "react-native-web",
    ]),
    ("nextjs", ["next.js", "nextjs", "next js"]),
    ("flutter", ["flutter", "dart app"]),
    ("ios-swift", ["ios swift", "swiftui", "swift app"]),
    ("android-compose", ["jetpack compose", "kotlin android"]),
    ("vue", ["vue.js", "vuejs", " vue ", "nuxt"]),
    ("svelte", ["svelte", "sveltekit"]),
    ("react", [" react ", "react ", "vite react", "react typescript", "react ts"]),
)

_BACKEND_KEYWORDS: tuple[tuple[str, list[str]], ...] = (
    ("fastapi", ["fastapi", "uvicorn", "starlette"]),
    ("django", ["django", "drf"]),
    ("spring-boot", ["spring boot", "spring-boot"]),
    ("rust-axum", ["axum", "actix"]),
    ("go-microservices", ["gin framework", "go microservice", "golang"]),
    ("express", ["express.js", " express ", "node backend"]),
    ("rails", ["ruby on rails", "rails api"]),
    ("laravel", ["laravel"]),
    ("dotnet", [".net", "asp.net"]),
)

_DB_KEYWORDS: tuple[tuple[str, list[str]], ...] = (
    ("postgres", ["postgres", "postgresql"]),
    ("mysql", ["mysql"]),
    ("mongo", ["mongo", "mongodb"]),
    ("sqlite", ["sqlite"]),
)

_CACHE_KEYWORDS: tuple[tuple[str, list[str]], ...] = (
    ("redis", ["redis"]),
    ("memcached", ["memcached"]),
)

_QUEUE_KEYWORDS: tuple[tuple[str, list[str]], ...] = (
    ("celery", ["celery"]),
    ("rq", [" rq ", "redis queue"]),
    ("sqs", ["amazon sqs", " sqs "]),
    ("kafka", ["kafka"]),
)


def _match_first(spec_lower: str, table: tuple[tuple[str, list[str]], ...]) -> str | None:
    for name, kws in table:
        if any(kw in spec_lower for kw in kws):
            return name
    return None


def _heuristic_stack(spec: str) -> StackProfile:
    lower = " " + spec.lower() + " "
    return StackProfile(
        frontend=_match_first(lower, _FRONTEND_KEYWORDS),
        backend=_match_first(lower, _BACKEND_KEYWORDS),
        database=_match_first(lower, _DB_KEYWORDS),
        cache=_match_first(lower, _CACHE_KEYWORDS),
        queue=_match_first(lower, _QUEUE_KEYWORDS),
    )


__all__ = [
    "Feature",
    "GenerateFn",
    "ProjectPlan",
    "StackProfile",
    "decompose_spec",
    "extract_features",
    "extract_stack",
    "parse_features_json",
    "parse_stack_json",
]
