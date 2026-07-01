"""
cvc.agent.api_docs — Input Grounding Layer: API Documentation Registry & Cache.

The #1 cause of AI agent hallucination is generating code against APIs they
*think* they know from training data. This module solves it at the INPUT:
give the agent correct, current API documentation BEFORE it writes code.

Architecture:
  - Local doc registry at ~/.cvc/docs/ (curated markdown, versioned)
  - Per-project doc cache at .cvc/docs/ (fetched on demand)
  - Structured annotations at ~/.cvc/doc_annotations/ (gotchas, tips)
  - Integration with Context Hub (chub) when available
  - Auto-detection of APIs from project manifests
  - Progressive disclosure: summary first, details on demand

This is the "preventive" approach to hallucination — complementing CVC's
existing "preservative" approach (committed context, lessons.md, autopilot).
"""

from __future__ import annotations

import json
import logging
import os
import re
import shutil
import subprocess
from cvc._subprocess_compat import HIDDEN_KW
import time
from pathlib import Path
from typing import Any

from cvc.core.models import get_global_config_dir

logger = logging.getLogger("cvc.agent.api_docs")

# ---------------------------------------------------------------------------
# Directory layout
# ---------------------------------------------------------------------------

DOCS_DIR = "docs"                        # Under ~/.cvc/docs/ (global cache)
ANNOTATIONS_DIR = "doc_annotations"      # Under ~/.cvc/doc_annotations/
PROJECT_DOCS_DIR = "docs"                # Under .cvc/docs/ (project-level)

# Max sizes to prevent context bloat
MAX_DOC_SIZE = 50_000          # chars — hard cap on a single doc
MAX_SUMMARY_SIZE = 5_000       # chars — for auto-injection summaries
MAX_ANNOTATION_SIZE = 2_000    # chars — per annotation
MAX_CACHED_DOCS = 200          # total cached doc files


def _global_docs_dir() -> Path:
    """Global doc cache directory."""
    d = get_global_config_dir() / DOCS_DIR
    d.mkdir(parents=True, exist_ok=True)
    return d


def _global_annotations_dir() -> Path:
    """Global annotation storage."""
    d = get_global_config_dir() / ANNOTATIONS_DIR
    d.mkdir(parents=True, exist_ok=True)
    return d


def _project_docs_dir(workspace: Path) -> Path:
    """Project-level doc cache under .cvc/docs/."""
    d = workspace / ".cvc" / PROJECT_DOCS_DIR
    d.mkdir(parents=True, exist_ok=True)
    return d


# ---------------------------------------------------------------------------
# Doc Registry Index
# ---------------------------------------------------------------------------

_REGISTRY_FILE = "registry.json"


def _load_registry() -> dict[str, Any]:
    """Load the global doc registry index."""
    path = _global_docs_dir() / _REGISTRY_FILE
    if path.exists():
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            return {"docs": {}, "version": "1.0.0"}
    return {"docs": {}, "version": "1.0.0"}


def _save_registry(registry: dict[str, Any]) -> None:
    """Save the global doc registry index."""
    path = _global_docs_dir() / _REGISTRY_FILE
    path.write_text(json.dumps(registry, indent=2), encoding="utf-8")


# ---------------------------------------------------------------------------
# Core API: Search, Fetch, Annotate
# ---------------------------------------------------------------------------

def search_docs(query: str, limit: int = 10) -> list[dict[str, Any]]:
    """
    Search for available API documentation.

    Searches across:
    1. Local cached docs (global + project)
    2. Context Hub (chub) if installed
    3. Built-in doc index

    Returns a list of matches with id, name, description, source.
    """
    results: list[dict[str, Any]] = []
    query_lower = query.lower()
    words = query_lower.split()

    # 1. Search local registry
    registry = _load_registry()
    for doc_id, doc_meta in registry.get("docs", {}).items():
        score = _score_doc(doc_id, doc_meta, query_lower, words)
        if score > 0:
            results.append({
                "id": doc_id,
                "name": doc_meta.get("name", doc_id),
                "description": doc_meta.get("description", ""),
                "language": doc_meta.get("language", ""),
                "version": doc_meta.get("version", ""),
                "source": "local",
                "score": score,
            })

    # 2. Try Context Hub (chub) if available
    chub_results = _search_chub(query)
    for r in chub_results:
        # Avoid duplicates
        if not any(x["id"] == r["id"] for x in results):
            results.append(r)

    # Sort by score descending
    results.sort(key=lambda x: x.get("score", 0), reverse=True)
    return results[:limit]


def fetch_doc(
    doc_id: str,
    *,
    language: str = "",
    version: str = "",
    workspace: Path | None = None,
    section: str = "",
) -> str:
    """
    Fetch API documentation content by ID.

    Resolution order:
    1. Project-level cache (.cvc/docs/)
    2. Global cache (~/.cvc/docs/)
    3. Context Hub (chub get)
    4. Error with suggestions

    Parameters
    ----------
    doc_id : str
        Identifier like "openai/chat", "stripe/api", "anthropic/sdk"
    language : str
        Language variant: "python", "javascript", etc.
    version : str
        Specific version
    section : str
        Fetch only a specific section/file within the doc
    """
    # 1. Check project cache
    if workspace:
        content = _read_cached_doc(
            _project_docs_dir(workspace), doc_id, language, version
        )
        if content:
            return _append_annotation(doc_id, content, section)

    # 2. Check global cache
    content = _read_cached_doc(_global_docs_dir(), doc_id, language, version)
    if content:
        return _append_annotation(doc_id, content, section)

    # 3. Try Context Hub CLI
    content = _fetch_from_chub(doc_id, language, version)
    if content:
        _cache_doc(_global_docs_dir(), doc_id, content, language, version)
        return _append_annotation(doc_id, content, section)

    # 4. Try Context Hub public GitHub registry (works without chub installed)
    content = _fetch_from_github_registry(doc_id, language)
    if content:
        _cache_doc(_global_docs_dir(), doc_id, content, language, version)
        return _append_annotation(doc_id, content, section)

    # 5. Not found
    suggestions = search_docs(doc_id.split("/")[-1] if "/" in doc_id else doc_id, limit=3)
    suggestion_text = ""
    if suggestions:
        suggestion_text = "\n\nDid you mean:\n" + "\n".join(
            f"  - {s['id']}: {s['description']}" for s in suggestions
        )
    return (
        f"No documentation found for '{doc_id}'.{suggestion_text}\n\n"
        "Tips:\n"
        "  - Run `cvc docs search <keyword>` to find available doc IDs\n"
        "  - Run `cvc docs import <file.md> <doc-id>` to import your own docs\n"
        "  - Install Context Hub for a larger registry: npm install -g @aisuite/chub"
    )


def annotate_doc(doc_id: str, note: str) -> dict[str, Any]:
    """
    Attach a persistent annotation (gotcha, tip, workaround) to an API doc.

    Annotations are saved locally and auto-appended on future doc fetches.
    This is how the agent learns from experience with specific APIs.
    """
    if len(note) > MAX_ANNOTATION_SIZE:
        note = note[:MAX_ANNOTATION_SIZE]

    ann_dir = _global_annotations_dir()
    safe_id = doc_id.replace("/", "--")
    ann_path = ann_dir / f"{safe_id}.json"

    # Load existing or create new
    existing: dict[str, Any] = {}
    if ann_path.exists():
        try:
            existing = json.loads(ann_path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            pass

    if "annotations" not in existing:
        existing = {
            "doc_id": doc_id,
            "annotations": [],
            "created_at": time.time(),
        }

    existing["annotations"].append({
        "note": note,
        "timestamp": time.time(),
    })
    existing["updated_at"] = time.time()

    ann_path.write_text(json.dumps(existing, indent=2), encoding="utf-8")

    return {
        "status": "saved",
        "doc_id": doc_id,
        "total_annotations": len(existing["annotations"]),
    }


def clear_annotation(doc_id: str) -> dict[str, Any]:
    """Remove all annotations for a doc."""
    ann_dir = _global_annotations_dir()
    safe_id = doc_id.replace("/", "--")
    ann_path = ann_dir / f"{safe_id}.json"
    if ann_path.exists():
        ann_path.unlink()
        return {"status": "cleared", "doc_id": doc_id}
    return {"status": "not_found", "doc_id": doc_id}


def list_annotations() -> list[dict[str, Any]]:
    """List all annotated docs."""
    ann_dir = _global_annotations_dir()
    results = []
    if not ann_dir.exists():
        return results
    for f in ann_dir.glob("*.json"):
        try:
            data = json.loads(f.read_text(encoding="utf-8"))
            results.append({
                "doc_id": data.get("doc_id", f.stem.replace("--", "/")),
                "count": len(data.get("annotations", [])),
                "updated_at": data.get("updated_at", 0),
            })
        except (json.JSONDecodeError, OSError):
            continue
    return results


def get_annotation(doc_id: str) -> list[dict[str, Any]]:
    """Get annotations for a specific doc."""
    ann_dir = _global_annotations_dir()
    safe_id = doc_id.replace("/", "--")
    ann_path = ann_dir / f"{safe_id}.json"
    if not ann_path.exists():
        return []
    try:
        data = json.loads(ann_path.read_text(encoding="utf-8"))
        return data.get("annotations", [])
    except (json.JSONDecodeError, OSError):
        return []


# ---------------------------------------------------------------------------
# Auto-detect relevant APIs from project manifests
# ---------------------------------------------------------------------------

# Mapping of package names → doc IDs for auto-detection
_PACKAGE_DOC_MAP: dict[str, str] = {
    # Python packages
    "openai": "openai/chat",
    "anthropic": "anthropic/sdk",
    "stripe": "stripe/api",
    "firebase-admin": "firebase/admin",
    "google-cloud-storage": "aws/s3",  # closest available
    "boto3": "aws/sdk",
    "fastapi": "python/fastapi",
    "django": "python/django",
    "flask": "python/flask",
    "sqlalchemy": "python/sqlalchemy",
    "prisma": "prisma/client",
    "langchain": "langchain/core",
    "langchain-core": "langchain/core",
    "chromadb": "chromadb/client",
    "pinecone-client": "pinecone/sdk",
    "pinecone": "pinecone/sdk",
    "supabase": "supabase/client",
    "redis": "redis/client",
    "playwright": "playwright/python",
    "sentry-sdk": "sentry/sdk",
    "slack-sdk": "slack/sdk",
    "twilio": "twilio/api",
    "sendgrid": "sendgrid/api",
    "google-generativeai": "gemini/api",
    "cohere": "cohere/api",
    "huggingface-hub": "huggingface/sdk",
    "qdrant-client": "qdrant/client",
    "weaviate-client": "weaviate/client",
    "meilisearch": "meilisearch/client",
    "elasticsearch": "elasticsearch/client",
    "motor": "mongodb/atlas",
    "pymongo": "mongodb/atlas",
    "jira": "jira/api",
    "notion-client": "notion/api",
    "asana": "asana/api",
    "hubspot": "hubspot/api",
    "kafka-python": "kafka/sdk",
    "aiokafka": "kafka/sdk",
    "pika": "rabbitmq/sdk",
    "replicate": "replicate/api",
    "elevenlabs": "elevenlabs/tts",
    "deepgram-sdk": "deepgram/speech",
    "assemblyai": "assemblyai/sdk",
    "airtable-python-wrapper": "airtable/api",
    "plaid": "plaid/api",
    # npm packages
    "@stripe/stripe-js": "stripe/api",
    "@openai/api": "openai/chat",
    "openai": "openai/chat",
    "@anthropic-ai/sdk": "anthropic/sdk",
    "firebase": "firebase/web",
    "@supabase/supabase-js": "supabase/client",
    "next": "vercel/platform",
    "@prisma/client": "prisma/client",
    "express": "node/express",
    "axios": "node/axios",
    "@slack/web-api": "slack/sdk",
    "discord.js": "discord/bot",
    "twilio": "twilio/api",
    "@sendgrid/mail": "sendgrid/api",
    "@sentry/node": "sentry/sdk",
    "@amplitude/analytics-node": "amplitude/sdk",
    "kafkajs": "kafka/sdk",
    "ioredis": "redis/client",
    "mongoose": "mongodb/atlas",
    "@notionhq/client": "notion/api",
    "hubspot": "hubspot/api",
    "weaviate-ts-client": "weaviate/client",
    "cloudflare": "cloudflare/workers",
}


def detect_project_apis(workspace: Path) -> list[dict[str, str]]:
    """
    Detect APIs used in the project by scanning manifests.

    Returns list of {package, doc_id} for packages that have known docs.
    """
    detected: list[dict[str, str]] = []
    seen_ids: set[str] = set()

    # Python: pyproject.toml, requirements.txt
    for manifest in ["pyproject.toml", "requirements.txt", "setup.py", "setup.cfg"]:
        manifest_path = workspace / manifest
        if manifest_path.exists():
            try:
                text = manifest_path.read_text(encoding="utf-8")
                for pkg, doc_id in _PACKAGE_DOC_MAP.items():
                    if pkg in text and doc_id not in seen_ids:
                        detected.append({"package": pkg, "doc_id": doc_id})
                        seen_ids.add(doc_id)
            except OSError:
                continue

    # Node: package.json
    pkg_json = workspace / "package.json"
    if pkg_json.exists():
        try:
            data = json.loads(pkg_json.read_text(encoding="utf-8"))
            all_deps = {
                **data.get("dependencies", {}),
                **data.get("devDependencies", {}),
            }
            for pkg, doc_id in _PACKAGE_DOC_MAP.items():
                if pkg in all_deps and doc_id not in seen_ids:
                    detected.append({"package": pkg, "doc_id": doc_id})
                    seen_ids.add(doc_id)
        except (json.JSONDecodeError, OSError):
            pass

    return detected


def build_api_context(workspace: Path) -> str:
    """
    Build a context summary of detected APIs for system prompt injection.

    This is the key integration point — detected APIs + any annotations
    are included in the system prompt so the agent is AWARE of what
    documentation is available before it starts coding.
    """
    detected = detect_project_apis(workspace)
    if not detected:
        return ""

    lines = ["## Available API Documentation (Input Grounding)"]
    lines.append(
        "The following APIs are detected in this project. "
        "Use `fetch_docs` to get current documentation BEFORE writing code "
        "against these APIs. Do NOT rely on training knowledge for API shapes."
    )
    lines.append("")

    for api in detected:
        doc_id = api["doc_id"]
        pkg = api["package"]
        annotations = get_annotation(doc_id)
        ann_text = ""
        if annotations:
            latest = annotations[-1]["note"]
            ann_text = f" ⚠️ Note: {latest[:100]}"
        lines.append(f"  - **{doc_id}** (from `{pkg}`){ann_text}")

    lines.append("")
    lines.append(
        "Run `fetch_docs <id>` before generating code for any of these APIs."
    )

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Local doc import
# ---------------------------------------------------------------------------

def import_doc(
    doc_id: str,
    content: str,
    *,
    name: str = "",
    description: str = "",
    language: str = "",
    version: str = "",
) -> dict[str, Any]:
    """
    Import/register a local documentation file.

    Used for:
    - Team-specific internal API docs
    - Custom framework documentation
    - Any docs not available via Context Hub
    """
    if len(content) > MAX_DOC_SIZE:
        content = content[:MAX_DOC_SIZE] + "\n\n[... truncated — doc exceeds size limit]"

    # Validate doc_id format
    if not re.match(r'^[a-zA-Z0-9._\-/]+$', doc_id):
        return {"status": "error", "message": "Invalid doc_id. Use alphanumeric, hyphens, underscores, dots, and slashes."}

    # Save content
    _cache_doc(_global_docs_dir(), doc_id, content, language, version)

    # Update registry
    registry = _load_registry()
    registry["docs"][doc_id] = {
        "name": name or doc_id.split("/")[-1],
        "description": description,
        "language": language,
        "version": version,
        "source": "local",
        "imported_at": time.time(),
        "size": len(content),
    }
    _save_registry(registry)

    return {
        "status": "imported",
        "doc_id": doc_id,
        "size": len(content),
    }


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _score_doc(
    doc_id: str,
    meta: dict[str, Any],
    query: str,
    words: list[str],
) -> int:
    """Score a doc against a search query."""
    score = 0
    id_lower = doc_id.lower()
    name_lower = meta.get("name", "").lower()
    desc_lower = meta.get("description", "").lower()

    # Exact ID match
    if id_lower == query:
        return 100

    # ID contains query
    if query in id_lower:
        score += 50

    # Name match
    if query in name_lower:
        score += 40

    # Word-level matching
    for word in words:
        if word in id_lower:
            score += 10
        if word in name_lower:
            score += 10
        if word in desc_lower:
            score += 5
        # Tag matching
        for tag in meta.get("tags", []):
            if word in tag.lower():
                score += 15

    return score


def _read_cached_doc(
    cache_dir: Path,
    doc_id: str,
    language: str,
    version: str,
) -> str | None:
    """Read a cached doc file."""
    safe_id = doc_id.replace("/", os.sep)
    parts = [safe_id]
    if language:
        parts.append(language)
    if version:
        parts.append(version)

    # Try exact path
    doc_path = cache_dir / os.sep.join(parts) / "DOC.md"
    if doc_path.exists():
        try:
            return doc_path.read_text(encoding="utf-8")[:MAX_DOC_SIZE]
        except OSError:
            return None

    # Try without version/language subdirs
    doc_path = cache_dir / safe_id / "DOC.md"
    if doc_path.exists():
        try:
            return doc_path.read_text(encoding="utf-8")[:MAX_DOC_SIZE]
        except OSError:
            return None

    # Try flat file
    flat_path = cache_dir / f"{doc_id.replace('/', '--')}.md"
    if flat_path.exists():
        try:
            return flat_path.read_text(encoding="utf-8")[:MAX_DOC_SIZE]
        except OSError:
            return None

    return None


def _cache_doc(
    cache_dir: Path,
    doc_id: str,
    content: str,
    language: str,
    version: str,
) -> None:
    """Cache a doc file locally."""
    safe_id = doc_id.replace("/", os.sep)
    parts = [safe_id]
    if language:
        parts.append(language)
    if version:
        parts.append(version)

    doc_dir = cache_dir / os.sep.join(parts)
    doc_dir.mkdir(parents=True, exist_ok=True)
    doc_path = doc_dir / "DOC.md"
    doc_path.write_text(content[:MAX_DOC_SIZE], encoding="utf-8")


def _append_annotation(doc_id: str, content: str, section: str = "") -> str:
    """Append any saved annotations to doc content."""
    annotations = get_annotation(doc_id)

    # If section filter, extract just that section
    if section and content:
        content = _extract_section(content, section)

    if not annotations:
        return content

    ann_text = "\n\n---\n## Agent Annotations (Learned from Experience)\n"
    for ann in annotations[-5:]:  # Last 5 annotations
        ann_text += f"\n- {ann['note']}\n"

    return content + ann_text


def _extract_section(content: str, section: str) -> str:
    """Extract a specific markdown section from content."""
    section_lower = section.lower()
    lines = content.split("\n")
    result: list[str] = []
    capturing = False
    capture_level = 0

    for line in lines:
        # Check for heading
        heading_match = re.match(r'^(#{1,6})\s+(.+)', line)
        if heading_match:
            level = len(heading_match.group(1))
            title = heading_match.group(2).strip().lower()

            if section_lower in title:
                capturing = True
                capture_level = level
                result.append(line)
                continue

            if capturing and level <= capture_level:
                break

        if capturing:
            result.append(line)

    if result:
        return "\n".join(result)
    return f"Section '{section}' not found in document. Available sections can be found in the full document."


# ---------------------------------------------------------------------------
# Context Hub GitHub public registry (no CLI required)
# ---------------------------------------------------------------------------

# Base URL for Context Hub's curated API documentation on GitHub
_CHUB_GITHUB_BASE = "https://raw.githubusercontent.com/andrewyng/context-hub/main/content"

# Map CVC doc IDs → Context Hub "{provider}/docs/{product}" path
# Structure is always: content/{provider}/docs/{product}/{language}/DOC.md
#                   or: content/{provider}/docs/{product}/DOC.md
_CHUB_PATH_MAP: dict[str, str] = {
    # AI / LLMs
    "openai/chat":          "openai/docs/chat",
    "anthropic/sdk":        "anthropic/docs/claude-api",
    "gemini/api":           "gemini/docs/genai",
    "deepseek/api":         "deepseek/docs/llm",
    "cohere/api":           "cohere/docs/llm",
    "huggingface/sdk":      "huggingface/docs/transformers",
    "replicate/api":        "replicate/docs/model-hosting",
    "elevenlabs/tts":       "elevenlabs/docs/text-to-speech",
    "deepgram/speech":      "deepgram/docs/speech",
    "assemblyai/sdk":       "assemblyai/docs/transcription",
    # Payments
    "stripe/api":           "stripe/docs/api",
    "stripe/payments":      "stripe/docs/payments",
    "paypal/api":           "paypal/docs/checkout",
    "braintree/api":        "braintree/docs/gateway",
    "square/api":           "square/docs/payments",
    "razorpay/api":         "razorpay/docs/payments",
    # Databases / Vector DBs
    "chromadb/client":      "chromadb/docs/embeddings-db",
    "pinecone/sdk":         "pinecone/docs/sdk",
    "supabase/client":      "supabase/docs/client",
    "redis/client":         "redis/docs/key-value",
    "mongodb/atlas":        "mongodb/docs/atlas",
    "prisma/client":        "prisma/docs/orm",
    "qdrant/client":        "qdrant/docs/vector-search",
    "weaviate/client":      "weaviate/docs/vector-db",
    "meilisearch/client":   "meilisearch/docs/search",
    "elasticsearch/client": "elasticsearch/docs/search",
    "cockroachdb/client":   "cockroachdb/docs/distributed-db",
    "airtable/api":         "airtable/docs/database",
    # Cloud / Infrastructure
    "aws/sdk":              "aws/docs/s3",
    "aws/s3":               "aws/docs/s3",
    "google/bigquery":      "google/docs/bigquery",
    "cloudflare/workers":   "cloudflare/docs/workers",
    "vercel/platform":      "vercel/docs/platform",
    # Auth
    "firebase/admin":       "firebase/docs/auth",
    "firebase/web":         "firebase/docs/auth",
    "auth0/sdk":            "auth0/docs/identity",
    "okta/sdk":             "okta/docs/identity",
    "clerk/sdk":            "clerk/docs/auth",
    "stytch/sdk":           "stytch/docs/auth",
    # Messaging / Email
    "slack/sdk":            "slack/docs/workspace",
    "discord/bot":          "discord/docs/bot",
    "sendgrid/api":         "sendgrid/docs/email-api",
    "twilio/api":           "twilio/docs/messaging",
    "mailchimp/api":        "mailchimp/docs/marketing",
    "resend/api":           "resend/docs/email",
    "postmark/api":         "postmark/docs/transactional-email",
    # Analytics / Monitoring
    "amplitude/sdk":        "amplitude/docs/analytics",
    "datadog/sdk":          "datadog/docs/monitoring",
    "sentry/sdk":           "sentry/docs/error-tracking",
    "launchdarkly/sdk":     "launchdarkly/docs/feature-flags",
    # Project Management / CRM
    "jira/api":             "jira/docs/issues",
    "notion/api":           "notion/docs/workspace-api",
    "asana/api":            "asana/docs/tasks",
    "linear/api":           "linear/docs/tracker",
    "hubspot/api":          "hubspot/docs/crm",
    "salesforce/api":       "salesforce/docs/crm",
    "zendesk/api":          "zendesk/docs/support",
    "intercom/api":         "intercom/docs/messaging",
    "atlassian/confluence": "atlassian/docs/confluence",
    # Other
    "kafka/sdk":            "kafka/docs/streaming",
    "rabbitmq/sdk":         "rabbitmq/docs/message-queue",
    "github/octokit":       "github/docs/octokit",
    "shopify/api":          "shopify/docs/storefront",
    "plaid/api":            "plaid/docs/banking",
    "microsoft/onedrive":   "microsoft/docs/onedrive",
    "deepl/api":            "deepl/docs/translation",
    "livekit/sdk":          "livekit/docs/realtime",
    "directus/api":         "directus/docs/headless-cms",
    "landingai/sdk":        "landingai-ade/docs/sdk",
}


def _fetch_from_github_registry(doc_id: str, language: str = "") -> str | None:
    """
    Fetch documentation from Context Hub's public GitHub repository.

    Works without the `chub` CLI installed. Uses the real directory structure:
      content/{provider}/docs/{product}/{language}/DOC.md
      content/{provider}/docs/{product}/DOC.md
    """
    try:
        import httpx
    except ImportError:
        return None

    chub_path = _CHUB_PATH_MAP.get(doc_id)
    if not chub_path:
        return None

    # Build candidate URLs: prefer the requested language, then python, then flat no-language
    candidate_urls: list[str] = []
    if language and language not in ("python", ""):
        candidate_urls.append(f"{_CHUB_GITHUB_BASE}/{chub_path}/{language}/DOC.md")
    candidate_urls.append(f"{_CHUB_GITHUB_BASE}/{chub_path}/python/DOC.md")
    candidate_urls.append(f"{_CHUB_GITHUB_BASE}/{chub_path}/DOC.md")

    for url in candidate_urls:
        try:
            response = httpx.get(url, timeout=10, follow_redirects=True)
            if response.status_code == 200 and response.text.strip():
                logger.debug("Fetched '%s' from Context Hub GitHub (%s)", doc_id, url)
                return response.text.strip()
        except Exception:
            continue

    return None


# ---------------------------------------------------------------------------
# Context Hub (chub) integration
# ---------------------------------------------------------------------------

def _chub_available() -> bool:
    """Check if `chub` CLI is installed."""
    return shutil.which("chub") is not None


def _search_chub(query: str) -> list[dict[str, Any]]:
    """Search Context Hub if available."""
    if not _chub_available():
        return []

    try:
        result = subprocess.run(
            ["chub", "search", query, "--json"],
            capture_output=True,
            text=True,
            timeout=10,
                    **HIDDEN_KW,
        )
        if result.returncode != 0:
            return []

        data = json.loads(result.stdout)
        results = []
        for entry in data.get("results", [])[:10]:
            results.append({
                "id": entry.get("id", ""),
                "name": entry.get("name", ""),
                "description": entry.get("description", ""),
                "language": "",
                "version": "",
                "source": "chub",
                "score": entry.get("_score", 50),
            })
        return results
    except (subprocess.TimeoutExpired, json.JSONDecodeError, OSError):
        return []


def _fetch_from_chub(
    doc_id: str,
    language: str = "",
    version: str = "",
) -> str | None:
    """Fetch a doc from Context Hub."""
    if not _chub_available():
        return None

    cmd = ["chub", "get", doc_id]
    if language:
        cmd.extend(["--lang", language])
    if version:
        cmd.extend(["--version", version])

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=15,
                    **HIDDEN_KW,
        )
        if result.returncode == 0 and result.stdout.strip():
            return result.stdout.strip()
        return None
    except (subprocess.TimeoutExpired, OSError):
        return None
