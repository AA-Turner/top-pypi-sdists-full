"""
cvc.cogs.registry — Persistence + lookup for compiled Cogs.

Storage layout (under ``<cvc_root>/cogs/``)::

    cogs/
      index.json          # flat metadata index, loaded into memory
      <id[:2]>/<id[2:]>.json  # full Cog envelope (one file per Cog)
      chroma/             # optional vector index of signature embeddings

The registry is intentionally decoupled from :class:`cvc.core.database.ContextDatabase`.
A Cog can outlive any single workspace and is meant to be portable across
checkouts and swarms.

Lookup is a two-step funnel:

1. **Vector pre-filter** (ChromaDB) — retrieves top-K Cogs by cosine
   similarity of the intent summary against the query intent.
2. **Structural filter** — input-schema compatibility + eligibility
   thresholds (``success_rate_ewma``, promoted state).

If ChromaDB is unavailable or the collection is empty, the registry falls
back to lexical token-overlap scoring so that tests and offline installs
still work.
"""

from __future__ import annotations

import json
import logging
import threading
from pathlib import Path
from typing import Any

from cvc.cogs.models import Cog

logger = logging.getLogger("cvc.cogs.registry")


# ---------------------------------------------------------------------------
# Vector index (optional, ChromaDB-backed)
# ---------------------------------------------------------------------------


class CogVectorIndex:
    """Optional ChromaDB collection for Cog signature embeddings."""

    def __init__(self, persist_dir: Path, *, enabled: bool = True) -> None:
        self._enabled = enabled
        self._persist_dir = persist_dir
        self._collection: Any = None
        self._tried_init = False

    def _ensure(self) -> None:
        if self._tried_init or not self._enabled:
            return
        self._tried_init = True
        try:
            import chromadb  # type: ignore[import-untyped]

            self._persist_dir.mkdir(parents=True, exist_ok=True)
            client = chromadb.PersistentClient(path=str(self._persist_dir))
            self._collection = client.get_or_create_collection(
                name="cvc_cogs", metadata={"hnsw:space": "cosine"}
            )
        except Exception as exc:
            logger.warning("CogVectorIndex disabled (chromadb unavailable): %s", exc)
            self._collection = None

    @property
    def available(self) -> bool:
        self._ensure()
        return self._collection is not None

    def add(self, cog_id: str, intent_summary: str, metadata: dict[str, Any]) -> None:
        if not self.available:
            return
        safe_meta: dict[str, Any] = {}
        for k, v in metadata.items():
            if isinstance(v, (str, int, float, bool)):
                safe_meta[k] = v
            else:
                safe_meta[k] = str(v)
        try:
            self._collection.upsert(ids=[cog_id], documents=[intent_summary], metadatas=[safe_meta])
        except Exception as exc:
            logger.warning("CogVectorIndex.add failed: %s", exc)

    def search(self, intent: str, n: int = 5) -> list[tuple[str, float]]:
        """Return ``[(cog_id, cosine_distance), ...]`` sorted by distance ascending."""
        if not self.available or not intent.strip():
            return []
        try:
            res = self._collection.query(query_texts=[intent], n_results=n)
        except Exception as exc:
            logger.warning("CogVectorIndex.search failed: %s", exc)
            return []
        ids = res.get("ids", [[]])[0]
        dists = res.get("distances", [[]])[0] if res.get("distances") else [0.0] * len(ids)
        return list(zip(ids, dists, strict=False))

    def delete(self, cog_id: str) -> None:
        if not self.available:
            return
        try:
            self._collection.delete(ids=[cog_id])
        except Exception as exc:
            logger.warning("CogVectorIndex.delete failed: %s", exc)


# ---------------------------------------------------------------------------
# Registry
# ---------------------------------------------------------------------------


def _tokenize(text: str) -> set[str]:
    return {t for t in text.lower().replace("-", " ").replace("_", " ").split() if t}


def _lexical_similarity(a: str, b: str) -> float:
    ta, tb = _tokenize(a), _tokenize(b)
    if not ta or not tb:
        return 0.0
    return len(ta & tb) / max(1, len(ta | tb))


class CogRegistry:
    """Filesystem-backed store + in-memory index for Cogs."""

    def __init__(
        self,
        cvc_root: Path,
        *,
        vector_enabled: bool = True,
    ) -> None:
        self.root = Path(cvc_root) / "cogs"
        self.root.mkdir(parents=True, exist_ok=True)
        self._index_path = self.root / "index.json"
        self._lock = threading.RLock()
        self._index: dict[str, dict[str, Any]] = {}
        self._load_index()
        self.vectors = CogVectorIndex(self.root / "chroma", enabled=vector_enabled)

    # -- storage primitives -----------------------------------------------

    def _cog_path(self, cog_id: str) -> Path:
        return self.root / cog_id[:2] / f"{cog_id[2:]}.json"

    def _load_index(self) -> None:
        if not self._index_path.exists():
            self._index = {}
            return
        try:
            data = json.loads(self._index_path.read_text(encoding="utf-8"))
            if isinstance(data, dict):
                self._index = data
        except Exception as exc:
            logger.warning("CogRegistry index corrupt, rebuilding: %s", exc)
            self._index = {}

    def _flush_index(self) -> None:
        tmp = self._index_path.with_suffix(".json.tmp")
        tmp.write_text(
            json.dumps(self._index, indent=2, sort_keys=True),
            encoding="utf-8",
        )
        tmp.replace(self._index_path)

    # -- public API --------------------------------------------------------

    def save(self, cog: Cog) -> Cog:
        """Persist *cog* (creates or updates). Returns the stored Cog."""
        if not cog.cog_id:
            cog.recompute_id()
        with self._lock:
            path = self._cog_path(cog.cog_id)
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(
                json.dumps(cog.model_dump(mode="json"), indent=2, sort_keys=True),
                encoding="utf-8",
            )
            self._index[cog.cog_id] = {
                "cog_id": cog.cog_id,
                "version": cog.version,
                "intent_summary": cog.signature.intent_summary,
                "tags": list(cog.signature.tags),
                "kind": cog.body.kind.value,
                "created_at": cog.created_at,
                "agent_id": cog.agent_id,
                "promoted": cog.telemetry.promoted,
                "success_rate_ewma": cog.telemetry.success_rate_ewma,
                "invocations": cog.telemetry.invocations,
                "tokens_saved_cumulative": cog.telemetry.tokens_saved_cumulative,
                "supersedes": cog.supersedes,
                "superseded_by": cog.superseded_by,
            }
            self._flush_index()
        self.vectors.add(
            cog.cog_id,
            cog.signature.intent_summary,
            {
                "agent_id": cog.agent_id,
                "promoted": int(cog.telemetry.promoted),
                "tags": ",".join(cog.signature.tags),
            },
        )
        return cog

    def get(self, cog_id: str) -> Cog | None:
        path = self._cog_path(cog_id)
        if not path.exists():
            return None
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            return Cog.model_validate(data)
        except Exception as exc:
            logger.warning("CogRegistry.get(%s) failed: %s", cog_id[:12], exc)
            return None

    def list_ids(self) -> list[str]:
        with self._lock:
            return list(self._index.keys())

    def list_summary(self) -> list[dict[str, Any]]:
        with self._lock:
            return list(self._index.values())

    def delete(self, cog_id: str) -> bool:
        with self._lock:
            path = self._cog_path(cog_id)
            removed = False
            if path.exists():
                path.unlink()
                removed = True
            if cog_id in self._index:
                del self._index[cog_id]
                self._flush_index()
                removed = True
        self.vectors.delete(cog_id)
        return removed

    def update_telemetry(self, cog: Cog) -> None:
        """Persist telemetry changes without recomputing cog_id."""
        self.save(cog)

    # -- lookup ------------------------------------------------------------

    def lookup_candidates(
        self,
        intent: str,
        *,
        n: int = 5,
    ) -> list[tuple[Cog, float]]:
        """
        Return up to *n* candidate Cogs ranked by similarity (lower = better).

        Returns ``[(cog, distance)]`` where distance is cosine distance
        (0.0–2.0) if vector search is available, else (1 - lexical_jaccard).
        """
        results: list[tuple[Cog, float]] = []
        seen: set[str] = set()

        if self.vectors.available:
            for cog_id, dist in self.vectors.search(intent, n=n):
                cog = self.get(cog_id)
                if cog is None:
                    continue
                results.append((cog, float(dist)))
                seen.add(cog_id)

        if len(results) < n:
            summaries = self.list_summary()
            scored: list[tuple[str, float]] = []
            for summary in summaries:
                cog_id = summary["cog_id"]
                if cog_id in seen:
                    continue
                sim = _lexical_similarity(intent, summary.get("intent_summary", ""))
                scored.append((cog_id, 1.0 - sim))
            scored.sort(key=lambda x: x[1])
            for cog_id, dist in scored[: max(0, n - len(results))]:
                cog = self.get(cog_id)
                if cog is not None:
                    results.append((cog, dist))

        results.sort(key=lambda x: x[1])
        return results[:n]

    def schema_matches(self, cog: Cog, inputs: dict[str, Any]) -> bool:
        """
        Check whether *inputs* satisfies the Cog's input schema.

        The schema is a flat ``{field: type_name}`` dict.  ``type_name`` is one
        of ``"str"``, ``"int"``, ``"float"``, ``"bool"``, ``"list"``, ``"dict"``,
        or ``"any"``.  Unknown types pass through.
        """
        schema = cog.signature.input_schema or {}
        if not schema:
            return True
        type_map: dict[str, tuple[type, ...]] = {
            "str": (str,),
            "int": (int,),
            "float": (float, int),
            "bool": (bool,),
            "list": (list,),
            "dict": (dict,),
        }
        for field, type_name in schema.items():
            if field not in inputs:
                return False
            expected = type_map.get(type_name)
            if expected is None:
                continue
            if not isinstance(inputs[field], expected):
                return False
        return True
