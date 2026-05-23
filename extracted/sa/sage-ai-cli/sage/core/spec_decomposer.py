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
    queue: str | None = None  # e.g. "celery", "bullmq", "rq", "sqs"
    # Extended runtime/packaging metadata from the spec
    js_runtime: str = "node"      # "bun" | "node" — JS runtime for frontend + workers
    pypi_package: bool = False    # True when backend should be pip-installable
    ssr: bool = False             # True when web SSR is required


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

    # Normalize frontend aliases
    _FRONTEND_ALIASES: dict[str, str] = {
        "react-native": "react-native-web",
        "reactnative": "react-native-web",
        "expo": "react-native-web",
        "expo-router": "react-native-web",
    }
    raw_frontend = _get("frontend")
    frontend = _FRONTEND_ALIASES.get(raw_frontend or "", raw_frontend)

    # Extract extras: js_runtime, pypi_package, ssr
    extras = data.get("extras") or {}
    if not isinstance(extras, dict):
        extras = {}
    js_runtime_raw = (extras.get("js_runtime") or "node").strip().lower()
    js_runtime = "bun" if js_runtime_raw == "bun" else "node"
    pypi_package = bool(extras.get("pypi_package", False))
    ssr = bool(extras.get("ssr", False))

    # Also detect bun/pypi from top-level spec text fallback
    # (in case LLM puts js_runtime at top level instead of extras)
    if not js_runtime == "bun" and _get("js_runtime") == "bun":
        js_runtime = "bun"
    if not pypi_package and str(data.get("pypi_package", "")).lower() in ("true", "yes", "1"):
        pypi_package = True

    return StackProfile(
        frontend=frontend,
        backend=_get("backend"),
        database=_get("database"),
        cache=_get("cache"),
        queue=_get("queue"),
        js_runtime=js_runtime,
        pypi_package=pypi_package,
        ssr=ssr,
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

## Technology Dictionary (reference before choosing)

**Bun.js / Bun**: A fast JavaScript runtime + bundler + package manager (like Node.js but faster).
  - Use `bun install` instead of `npm install`
  - Use `bun run dev` / `bun run build` instead of `npm run`
  - Docker image: `oven/bun:1` (NOT `node:`)
  - BullMQ workers run under Bun (TypeScript, `import { Worker } from 'bullmq'`)
  - When spec says "use Bun instead of Node" or "use Bun.js": set js_runtime="bun"

**PyPI packaging**: Distributing a Python package to pip/PyPI.
  - Requires `pyproject.toml` with `[build-system]` and `[project]` sections
  - Built with `python -m build`, published with `twine upload`
  - NOT the same as "use Python" — it means the backend should be installable via `pip install`
  - When spec says "package via PyPI" or "distribute via PyPI": set pypi_package=true in extras

**BullMQ**: Redis-based job queue for Node.js / Bun.js (TypeScript)
  - Different from Python's Celery — this runs in the JS runtime (Bun or Node)
  - Workers are TypeScript files: `new Worker('queue-name', async (job) => { ... })`

**TimescaleDB**: PostgreSQL extension for time-series data
  - Same `postgres` connection string, just enable the extension
  - Use for analytics, metrics, event streams

**RunwayML**: AI video generation API (not self-hosted)

**Stable Diffusion**: AI image generation (can be self-hosted or via API)

Output a single JSON object with these string keys (or null):
  - frontend: framework name — MUST be one of:
              "react-native-web" — React Native + Expo SDK (iOS/Android/Web). Use
                  this for ANY spec mentioning React Native, Expo, mobile app.
                  When spec also mentions Bun.js SSR: STILL use "react-native-web",
                  and set js_runtime="bun" in extras.
              "react" — plain web app (no mobile)
              "nextjs" — Next.js SSR
              null — no frontend
  - backend:  "fastapi", "django", "express", "go-microservices", "rust-axum", etc. or null
  - database: "postgres", "mysql", "sqlite", "mongo", "timescaledb" or null
  - cache:    "redis", "memcached" or null
  - queue:    "bullmq" (JS/Bun queue), "celery" (Python), "rq", "kafka" or null
  - extras:   object with optional fields:
              - js_runtime: "bun" | "node" (default "node") — set to "bun" if spec says Bun.js
              - pypi_package: true/false — set true if spec says distribute via PyPI
              - ssr: true/false — set true if spec requires server-side rendering

IMPORTANT: For React Native / mobile / cross-platform apps ALWAYS output "react-native-web".
When Bun.js is mentioned, set js_runtime="bun" in extras — do NOT change the frontend key.

Output ONLY the JSON object. No prose.

Spec:
{spec}
"""


def _truncate_for_prompt(spec: str, max_chars: int = 14000) -> str:
    """Keep large specs from blowing the LLM context window.

    Strategy: keep first 6000 chars, summarize section headers from the
    middle, then keep last 4000 chars. This preserves the overall
    structure (title + intro, all section names, closing requirements)
    rather than blindly discarding content from the middle.
    """
    if len(spec) <= max_chars:
        return spec

    head_chars = 6000
    tail_chars = 4000
    head = spec[:head_chars]
    tail = spec[-tail_chars:]

    # Summarise section headers from the middle so the LLM knows what
    # was truncated (lines starting with # or a numbered-section pattern).
    middle = spec[head_chars : len(spec) - tail_chars]
    _SECTION_HEADER_RE = re.compile(
        r"^[ \t]*(?:#{1,4}[ \t]+\S|(?:\d+[.)]\s+[A-Z]))", re.MULTILINE
    )
    middle_headers = _SECTION_HEADER_RE.findall(middle)
    if middle_headers:
        # Collect full header lines from the middle block
        header_lines = [
            line.strip()
            for line in middle.splitlines()
            if _SECTION_HEADER_RE.match(line)
        ]
        summary = "\n".join(header_lines[:60])  # cap at 60 headers
        middle_note = (
            f"\n\n...[middle truncated — section headings below]...\n{summary}\n"
        )
    else:
        middle_note = "\n\n...[middle truncated]...\n"

    return head + middle_note + tail


def extract_features(spec: str, generate: GenerateFn, *, max_retries: int = 3) -> list[Feature]:
    """Get the feature list, retrying on malformed JSON, falling back to keywords."""
    # NOTE: Use str.replace() — NEVER .format(). The prompt template contains
    # literal `{ Worker }` and `{ ... }` in code examples that .format() would
    # misinterpret as named placeholders and raise KeyError(' Worker '), which
    # silently kills the entire principal build pipeline.
    prompt = _FEATURES_PROMPT.replace("{spec}", _truncate_for_prompt(spec, max_chars=14000))
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
    # Use str.replace() not .format() — see extract_features() for why.
    prompt = _STACK_PROMPT.replace("{spec}", _truncate_for_prompt(spec))
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
