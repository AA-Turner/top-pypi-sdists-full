"""MemPalace — structured memory for pw-agent.

Two-tier storage:
  1. Project memory:  ~/.config/pw-agent/memory/<project_hash>/
     Per-project knowledge units (auto-extracted from conversations).
  2. Global memory:   ~/.config/pw-agent/memory/global/
     Cross-project user preferences, role, communication style.
     Survives moving between projects so pw-agent always knows who
     it's talking to.

Both tiers use Ollama embeddings + cosine similarity retrieval. The
global tier is queried alongside project memory and merged into the
prompt context.
"""

import json
import hashlib
import os
import time
from typing import Optional

import numpy as np
import requests

DEFAULT_MEMORY_DIR = os.path.expanduser("~/.config/pw-agent/memory")
GLOBAL_MEMORY_DIR_NAME = "global"  # subdir under DEFAULT_MEMORY_DIR for cross-project facts

# Embedding config
EMBED_MODEL = "nomic-embed-text"  # Tiny, fast, 300MB — falls back to LLM if not available
EMBED_FALLBACK = True  # Use the active LLM for embeddings if embed model not available
EMBED_DIM = 768  # nomic-embed-text dimension (auto-detected on first use)

# Retrieval config
TOP_K = 5  # Number of knowledge units to retrieve per query
MIN_SIMILARITY = 0.55  # Minimum cosine similarity to include in retrieval
MAX_CONTEXT_CHARS = 3000  # Max chars of memory to inject into prompt

# Curation config (Mem0-style session-end extraction)
DEDUP_SIMILARITY = 0.85  # Above this, treat as candidate duplicate — ask LLM to reconcile
VALID_CATEGORIES = {"project-fact", "user-pref", "gotcha", "decision"}
# Compact category codes for small-model JSON (c = category, f = fact)
CATEGORY_ALIASES = {
    "pf": "project-fact", "project-fact": "project-fact", "project": "project-fact",
    "up": "user-pref",    "user-pref": "user-pref",     "pref": "user-pref",
    "g":  "gotcha",       "gotcha": "gotcha",
    "d":  "decision",     "decision": "decision",       "dec": "decision",
}


class KnowledgeUnit:
    """A single piece of knowledge extracted from a conversation."""

    def __init__(self, content: str, source: str = "", tags: list[str] = None,
                 timestamp: float = None, unit_id: str = None):
        self.id = unit_id or hashlib.md5(content.encode()).hexdigest()[:12]
        self.content = content
        self.source = source  # e.g. "conversation", "file:path/to/file.py", "tool:bash"
        self.tags = tags or []
        self.timestamp = timestamp or time.time()

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "content": self.content,
            "source": self.source,
            "tags": self.tags,
            "timestamp": self.timestamp,
        }

    @classmethod
    def from_dict(cls, d: dict) -> "KnowledgeUnit":
        return cls(
            content=d["content"],
            source=d.get("source", ""),
            tags=d.get("tags", []),
            timestamp=d.get("timestamp", 0),
            unit_id=d.get("id"),
        )


class MemoryStore:
    """Local memory store. Defaults to per-project, but can also be a
    global cross-project store when scope='global'."""

    def __init__(self, project_dir: str, ollama_url: str = "http://localhost:11434",
                 memory_dir: str = "", scope: str = "project", auth_token: str = ""):
        self.project_dir = os.path.abspath(project_dir)
        self.ollama_url = ollama_url
        self.memory_dir = memory_dir or DEFAULT_MEMORY_DIR
        self.scope = scope
        # When talking to a PastaWater brain's Ollama proxy, all routes
        # (/api/embed, /api/tags, /api/chat) require a bearer token. Raw
        # local Ollama ignores the header harmlessly.
        self.auth_token = auth_token

        if scope == "global":
            # Cross-project user preferences live at memory/global/
            self.store_path = os.path.join(self.memory_dir, GLOBAL_MEMORY_DIR_NAME)
        else:
            # Project-specific storage path
            project_hash = hashlib.md5(self.project_dir.encode()).hexdigest()[:12]
            self.store_path = os.path.join(self.memory_dir, project_hash)
        os.makedirs(self.store_path, exist_ok=True)

        # Load existing data
        self.units: list[KnowledgeUnit] = []
        self.vectors: Optional[np.ndarray] = None
        self._embed_dim: Optional[int] = None
        self._embed_model: Optional[str] = None
        self._load()

    def _units_path(self) -> str:
        return os.path.join(self.store_path, "units.json")

    def _vectors_path(self) -> str:
        return os.path.join(self.store_path, "vectors.npy")

    def _index_path(self) -> str:
        return os.path.join(self.store_path, "index.json")

    def _load(self):
        """Load units and vectors from disk."""
        units_path = self._units_path()
        if os.path.exists(units_path):
            try:
                with open(units_path, "r") as f:
                    data = json.load(f)
                self.units = [KnowledgeUnit.from_dict(d) for d in data]
            except (json.JSONDecodeError, KeyError):
                self.units = []

        vectors_path = self._vectors_path()
        if os.path.exists(vectors_path):
            try:
                self.vectors = np.load(vectors_path)
                self._embed_dim = self.vectors.shape[1] if len(self.vectors.shape) > 1 else None
            except Exception:
                self.vectors = None

        # Load index for metadata
        index_path = self._index_path()
        if os.path.exists(index_path):
            try:
                with open(index_path, "r") as f:
                    idx = json.load(f)
                self._embed_model = idx.get("embed_model")
                self._embed_dim = idx.get("embed_dim", self._embed_dim)
            except Exception:
                pass

    def _save(self):
        """Persist units and vectors to disk."""
        with open(self._units_path(), "w") as f:
            json.dump([u.to_dict() for u in self.units], f, indent=2)

        if self.vectors is not None and len(self.vectors) > 0:
            np.save(self._vectors_path(), self.vectors)

        with open(self._index_path(), "w") as f:
            json.dump({
                "project_dir": self.project_dir,
                "embed_model": self._embed_model,
                "embed_dim": self._embed_dim,
                "unit_count": len(self.units),
                "last_updated": time.time(),
            }, f, indent=2)

    def _embed(self, texts: list[str]) -> Optional[np.ndarray]:
        """Get embeddings from Ollama. Returns array of shape (N, dim) or None.

        Retries up to 3x with backoff on cold-start / VRAM swap. On a
        constrained GPU the embed model may need to evict the chat model
        first, which can take 10-20 s. Ollama returns 503 while loading
        and may also throw connection errors — retry both."""
        model = self._embed_model or EMBED_MODEL
        last_err = None

        headers = {"Authorization": f"Bearer {self.auth_token}"} if self.auth_token else {}
        for attempt in range(3):  # up to 3 tries
            try:
                resp = requests.post(
                    f"{self.ollama_url}/api/embed",
                    json={"model": model, "input": texts},
                    headers=headers,
                    timeout=120,  # tolerates slow reload + embed on big batch
                )
                if resp.status_code == 200:
                    data = resp.json()
                    embeddings = data.get("embeddings", [])
                    if embeddings:
                        arr = np.array(embeddings, dtype=np.float32)
                        self._embed_model = model
                        self._embed_dim = arr.shape[1]
                        return arr
                    last_err = f"200 but empty embeddings"
                else:
                    last_err = f"HTTP {resp.status_code}"
            except Exception as e:
                last_err = str(e)
            # Back off between attempts: 2s, 5s
            if attempt < 2:
                time.sleep(2 if attempt == 0 else 5)
        return None

    def add(self, content: str, source: str = "", tags: list[str] = None) -> bool:
        """Add a knowledge unit to the store."""
        # Skip duplicates (same content hash)
        unit = KnowledgeUnit(content=content, source=source, tags=tags)
        if any(u.id == unit.id for u in self.units):
            return False

        # Get embedding
        embedding = self._embed([content])
        if embedding is None:
            # Store without embedding — can be embedded later
            self.units.append(unit)
            self._save()
            return True

        # Append to vectors
        if self.vectors is None or len(self.vectors) == 0:
            self.vectors = embedding
        else:
            # Handle dimension mismatch (model changed)
            if embedding.shape[1] != self.vectors.shape[1]:
                # Re-embed everything with new model
                self.vectors = embedding
                self.units = [unit]
                self._save()
                return True
            self.vectors = np.vstack([self.vectors, embedding])

        self.units.append(unit)
        self._save()
        return True

    def retrieve(self, query: str, top_k: int = TOP_K) -> list[tuple[KnowledgeUnit, float]]:
        """Retrieve the most relevant knowledge units for a query."""
        if not self.units or self.vectors is None or len(self.vectors) == 0:
            return []

        # Embed the query
        query_vec = self._embed([query])
        if query_vec is None:
            return []

        # Cosine similarity
        query_norm = query_vec / (np.linalg.norm(query_vec, axis=1, keepdims=True) + 1e-8)
        store_norm = self.vectors / (np.linalg.norm(self.vectors, axis=1, keepdims=True) + 1e-8)
        similarities = (store_norm @ query_norm.T).flatten()

        # Top-K above threshold
        indices = np.argsort(similarities)[::-1][:top_k]
        results = []
        for idx in indices:
            sim = float(similarities[idx])
            if sim >= MIN_SIMILARITY:
                results.append((self.units[idx], sim))

        return results

    def format_context(self, query: str) -> tuple[str, list]:
        """Retrieve and format relevant memories for injection into the prompt.

        Returns a (context_str, raw_hits) tuple so the caller can derive stats
        from ``raw_hits`` without issuing a second embed round-trip.
        ``raw_hits`` is the same list[tuple[KnowledgeUnit, float]] returned by
        ``retrieve()``.
        """
        results = self.retrieve(query)
        if not results:
            return "", []

        header = "## User profile (cross-project):" if self.scope == "global" else "## Relevant memories from previous sessions:"
        lines = [header]
        total_chars = 0
        for unit, score in results:
            entry = f"- [{unit.source}] {unit.content}"
            if total_chars + len(entry) > MAX_CONTEXT_CHARS:
                break
            lines.append(entry)
            total_chars += len(entry)

        return "\n".join(lines), results

    @property
    def size(self) -> int:
        return len(self.units)

    def size_summary(self) -> dict:
        """Rough bookkeeping for the /memory UI + startup growth warning.
        disk_bytes includes only units.json + vectors.npy (the real data)."""
        disk_bytes = 0
        for fname in ("units.json", "vectors.npy"):
            p = os.path.join(self.store_path, fname)
            if os.path.exists(p):
                try:
                    disk_bytes += os.path.getsize(p)
                except OSError:
                    pass
        oldest = min((u.timestamp for u in self.units), default=0)
        age_days = int((time.time() - oldest) / 86400) if oldest else 0
        return {"units": len(self.units), "disk_bytes": disk_bytes, "age_days": age_days}

    def growth_warning(self) -> Optional[str]:
        """Return a short warning string when the store is getting large,
        else None. Thresholds are generous — nobody with <500 units needs
        to hear about it."""
        s = self.size_summary()
        if s["units"] >= 1000 or s["disk_bytes"] >= 50 * 1024 * 1024:
            return f"{s['units']} memories · {s['disk_bytes']//(1024*1024)} MB — consider /memory prune or /memory forget <id>"
        if s["units"] >= 500:
            return f"{s['units']} memories stored — getting large; /memory recall to inspect, /memory prune to reset"
        return None


_EXTRACT_PROMPT = """You are a memory curator for a coding assistant. Review the conversation and extract 0-10 DURABLE facts worth remembering in future sessions.

Each fact must fit exactly one category:
- pf (project-fact): concrete fact about THIS codebase — library versions, file paths, service ports, conventions
- up (user-pref): a durable user preference — coding style, review habits, communication choices
- g  (gotcha): a painful lesson or trap — "X breaks when Y", "don't do Z because…"
- d  (decision): an architectural decision made — "chose A over B because…", "renamed X to Y"

STRICT RULES:
- Skip transient debugging steps (errors that got fixed, temp logs, tool output)
- Skip chitchat, greetings, generic advice
- Skip things a future reader can see by reading the code (obvious function signatures etc.)
- One sentence per fact, concrete and specific, no hedging
- Start with a verb or noun, NOT "The user" or "This project"
- If nothing durable was learned, return exactly: []

Output ONLY valid JSON, no prose, no code fences:
[{{"c":"<code>","f":"<one sentence>"}}, ...]

Where <code> is one of: pf, up, g, d

Conversation:
---
{conversation}
---

JSON:"""


_DEDUP_PROMPT = """You are reconciling a new memory fact against a similar existing one.

EXISTING: {existing}
NEW:      {new}

Pick ONE action:
- keep: the existing fact is still correct and more complete, drop the new one
- replace: the new fact supersedes the existing one (newer info, corrects it)
- merge: combine into one sentence that captures both details

Respond ONLY with JSON, no prose:
{{"a":"keep"}}  OR  {{"a":"replace"}}  OR  {{"a":"merge","f":"<merged sentence>"}}
"""


def _format_conversation_for_extraction(conversation: list[dict], max_chars: int = 12000) -> str:
    """Flatten a conversation into a compact transcript for the extractor prompt.
    Strips tool-call JSON noise — the curator needs the CONTENT not the mechanics."""
    lines = []
    total = 0
    for msg in conversation:
        role = msg.get("role", "")
        content = str(msg.get("content", "")).strip()
        if not content:
            continue
        # Strip embedded tool-call JSON so the curator sees reasoning, not syntax.
        if role == "assistant":
            content = _strip_tool_syntax(content)
            if not content:
                continue
        elif role == "tool_result":
            # Keep only the first 400 chars of tool output — enough to judge relevance.
            content = content[:400]
        line = f"{role.upper()}: {content}"
        if total + len(line) > max_chars:
            break
        lines.append(line)
        total += len(line)
    return "\n\n".join(lines)


def _strip_tool_syntax(text: str) -> str:
    """Remove <tool_call>…</tool_call> and ACTION:{…} blocks, leave prose."""
    import re
    text = re.sub(r"<tool_call>[\s\S]*?</tool_call>", "", text)
    text = re.sub(r"ACTION:\s*\{[\s\S]*?\}", "", text)
    return text.strip()


def _parse_extraction_json(raw: str) -> list[dict]:
    """Extract the JSON array from a model response. Small models often
    wrap JSON in prose or code fences — we find the first [ and last ]."""
    if not raw:
        return []
    raw = raw.strip()
    # Strip code fences if present
    if raw.startswith("```"):
        raw = raw.split("```", 2)[1] if "```" in raw[3:] else raw[3:]
        if raw.startswith("json"):
            raw = raw[4:]
    # Find outer array brackets
    start = raw.find("[")
    end = raw.rfind("]")
    if start < 0 or end < 0 or end <= start:
        return []
    try:
        parsed = json.loads(raw[start:end + 1])
        if not isinstance(parsed, list):
            return []
        return [x for x in parsed if isinstance(x, dict)]
    except (json.JSONDecodeError, ValueError):
        return []


def extract_durable_memories(conversation: list[dict], client) -> list[dict]:
    """Ask the active LLM to distill the conversation into durable facts.

    Returns a list of {"content": str, "source": category, "tags": []}
    ready to feed to MemoryStore.dedup_and_store(). Returns [] if the
    conversation has nothing durable OR the LLM is unreachable."""
    if not client or not conversation:
        return []

    # Skip tiny conversations — nothing worth distilling
    substantive = [m for m in conversation
                   if m.get("role") in ("assistant", "user")
                   and len(str(m.get("content", "")).strip()) > 20]
    if len(substantive) < 2:
        return []

    transcript = _format_conversation_for_extraction(conversation)
    if not transcript:
        return []

    prompt = _EXTRACT_PROMPT.format(conversation=transcript)

    try:
        raw = client.chat(
            messages=[{"role": "user", "content": prompt}],
            temperature=0.1,
            context_length=16384,
        )
    except Exception:
        return []

    raw_facts = _parse_extraction_json(raw)
    units = []
    for item in raw_facts:
        cat_raw = str(item.get("c") or item.get("category") or "").strip().lower()
        fact = str(item.get("f") or item.get("fact") or item.get("content") or "").strip()
        category = CATEGORY_ALIASES.get(cat_raw)
        if not category or not fact or len(fact) < 10 or len(fact) > 400:
            continue
        units.append({
            "content": fact,
            "source": category,
            "tags": [category],
        })
    return units


# Extend MemoryStore with curated-add semantics
def _dedup_and_store(self, new_facts: list[dict], client=None) -> dict:
    """Semantic ADD/UPDATE/REPLACE/IGNORE for a batch of curated facts.

    For each new fact:
      - Embed it, find its nearest existing unit.
      - If similarity < DEDUP_SIMILARITY: ADD.
      - If similarity >= DEDUP_SIMILARITY and client given: ask LLM to reconcile.
      - If similarity >= DEDUP_SIMILARITY and no client: IGNORE (conservative).

    Returns {"added": N, "replaced": M, "merged": K, "ignored": J}."""
    counts = {"added": 0, "replaced": 0, "merged": 0, "ignored": 0}
    if not new_facts:
        return counts

    # BATCH EMBED upfront — one Ollama call for all facts instead of N.
    # Avoids VRAM thrashing: on constrained GPUs Ollama may evict the chat
    # model to load the embed model, and doing it per-fact = N evict/reload
    # cycles = timeouts. One batched call = one reload for the whole set.
    contents = [str(f.get("content", "")).strip() for f in new_facts]
    embeds = None
    non_empty_mask = [bool(c) for c in contents]
    non_empty_contents = [c for c in contents if c]
    if non_empty_contents:
        embeds = self._embed(non_empty_contents)

    # Map back to per-fact index in the embeds array
    embed_idx = 0
    for fact_i, fact in enumerate(new_facts):
        content = contents[fact_i]
        if not content:
            continue

        new_vec = None
        if embeds is not None and embed_idx < len(embeds):
            new_vec = embeds[embed_idx:embed_idx + 1]
            embed_idx += 1

        if new_vec is None:
            # Embed service unavailable — fall back to plain add (stores without vector).
            if self.add(content, source=fact.get("source", ""), tags=fact.get("tags", [])):
                counts["added"] += 1
            continue

        # Check nearest existing unit
        if self.vectors is None or len(self.vectors) == 0:
            self._raw_add(content, new_vec, fact.get("source", ""), fact.get("tags", []))
            counts["added"] += 1
            continue

        store_norm = self.vectors / (np.linalg.norm(self.vectors, axis=1, keepdims=True) + 1e-8)
        new_norm = new_vec / (np.linalg.norm(new_vec, axis=1, keepdims=True) + 1e-8)
        sims = (store_norm @ new_norm.T).flatten()
        nearest_idx = int(np.argmax(sims))
        nearest_sim = float(sims[nearest_idx])

        if nearest_sim < DEDUP_SIMILARITY:
            # Genuinely new fact — add
            self._raw_add(content, new_vec, fact.get("source", ""), fact.get("tags", []))
            counts["added"] += 1
            continue

        # Candidate duplicate. Without an LLM client, be conservative — ignore.
        if not client:
            counts["ignored"] += 1
            continue

        # Ask the LLM to pick keep / replace / merge
        existing_unit = self.units[nearest_idx]
        prompt = _DEDUP_PROMPT.format(existing=existing_unit.content, new=content)
        try:
            raw = client.chat(
                messages=[{"role": "user", "content": prompt}],
                temperature=0.0,
                context_length=4096,
            )
        except Exception:
            counts["ignored"] += 1
            continue

        action, merged_text = _parse_dedup_decision(raw)
        if action == "replace":
            self._replace_at(nearest_idx, content, new_vec, fact.get("source", ""), fact.get("tags", []))
            counts["replaced"] += 1
        elif action == "merge" and merged_text:
            merged_vec = self._embed([merged_text])
            if merged_vec is not None:
                self._replace_at(nearest_idx, merged_text, merged_vec, fact.get("source", ""), fact.get("tags", []))
                counts["merged"] += 1
            else:
                counts["ignored"] += 1
        else:
            # "keep" or unparseable — drop the new one
            counts["ignored"] += 1

    self._save()
    return counts


def _parse_dedup_decision(raw: str) -> tuple[str, Optional[str]]:
    """Parse {'a': 'keep'|'replace'|'merge', 'f': '...'} from model output."""
    if not raw:
        return ("ignore", None)
    raw = raw.strip()
    if raw.startswith("```"):
        raw = raw.split("```", 2)[1] if "```" in raw[3:] else raw[3:]
        if raw.startswith("json"):
            raw = raw[4:]
    start = raw.find("{")
    end = raw.rfind("}")
    if start < 0 or end <= start:
        return ("ignore", None)
    try:
        obj = json.loads(raw[start:end + 1])
    except (json.JSONDecodeError, ValueError):
        return ("ignore", None)
    action = str(obj.get("a") or obj.get("action") or "").strip().lower()
    if action not in ("keep", "replace", "merge"):
        return ("ignore", None)
    if action == "merge":
        merged = str(obj.get("f") or obj.get("merged") or "").strip()
        if not merged or len(merged) < 10 or len(merged) > 400:
            return ("ignore", None)
        return ("merge", merged)
    return (action, None)


def _raw_add(self, content: str, embedding: np.ndarray, source: str, tags: list) -> None:
    """Append a unit + its precomputed embedding without re-embedding."""
    unit = KnowledgeUnit(content=content, source=source, tags=tags)
    if self.vectors is None or len(self.vectors) == 0:
        self.vectors = embedding
    elif embedding.shape[1] != self.vectors.shape[1]:
        # Dimension mismatch — reset store (embedding model changed mid-session)
        self.vectors = embedding
        self.units = [unit]
        return
    else:
        self.vectors = np.vstack([self.vectors, embedding])
    self.units.append(unit)


def _replace_at(self, idx: int, content: str, embedding: np.ndarray, source: str, tags: list) -> None:
    """In-place replace unit at idx with new content + embedding (preserves ID for stability)."""
    if idx < 0 or idx >= len(self.units):
        return
    old = self.units[idx]
    new_unit = KnowledgeUnit(content=content, source=source, tags=tags,
                             timestamp=time.time(), unit_id=old.id)
    self.units[idx] = new_unit
    if self.vectors is not None and embedding.shape[1] == self.vectors.shape[1]:
        self.vectors[idx] = embedding[0]


# Attach the new methods to MemoryStore
MemoryStore.dedup_and_store = _dedup_and_store
MemoryStore._raw_add = _raw_add
MemoryStore._replace_at = _replace_at


def extract_knowledge(conversation: list[dict], existing_units: list[KnowledgeUnit]) -> list[dict]:
    """DEPRECATED: legacy heuristic extractor. Kept for callers that haven't
    migrated to extract_durable_memories() yet.

    Simple extraction: pull out key facts from assistant responses and
    tool results. No LLM call needed — just heuristics.
    """
    existing_ids = {u.id for u in existing_units}
    new_units = []

    for i, msg in enumerate(conversation):
        role = msg.get("role", "")
        content = msg.get("content", "")

        if not content or len(content) < 50:
            continue

        if role == "assistant":
            # Skip tool calls — they're actions, not knowledge
            if "<tool_call>" in content or "ACTION:" in content:
                continue
            # Skip very short responses
            if len(content) < 100:
                continue

            # Extract the assistant's substantive response as a knowledge unit
            # Truncate to keep units focused
            text = content[:500].strip()
            unit_id = hashlib.md5(text.encode()).hexdigest()[:12]
            if unit_id not in existing_ids:
                new_units.append({
                    "content": text,
                    "source": "conversation",
                    "tags": [],
                })

        elif role == "tool_result":
            # Extract file reads and command outputs as knowledge
            if content.startswith("Result:"):
                result_text = content[7:].strip()
                if len(result_text) > 50:
                    # Determine source from previous assistant message
                    source = "tool"
                    if i > 0:
                        prev = conversation[i - 1].get("content", "")
                        if "read_file" in prev:
                            source = "file"
                        elif "bash" in prev:
                            source = "bash"
                        elif "list_files" in prev:
                            source = "listing"

                    text = result_text[:500].strip()
                    unit_id = hashlib.md5(text.encode()).hexdigest()[:12]
                    if unit_id not in existing_ids:
                        new_units.append({
                            "content": text,
                            "source": source,
                            "tags": [],
                        })

    return new_units
