"""
cvc.cogs.sdcp — Semantic Delta Context Protocol.

For the LLM calls the Cognitive Cache cannot short-circuit, SDCP shrinks the
payload by shipping only atoms that are

* highly relevant to the current task (above a relevance threshold), AND
* not already present in the provider-side prompt cache (tracked by atom
  hash + last task hash the atom was sent under).

Stable atoms (system prompt, project conventions, durable user preferences)
are kept in a prefix that hits Anthropic ``cache_control`` / Google
``cachedContent``.  CVC already wires these markers in its adapters; SDCP
simply decides *what* goes in each bucket.

Embeddings are optional.  If the caller passes an embedding-equipped
``CogVectorIndex`` or a custom scorer, SDCP uses cosine similarity.  Without
one, it falls back to lexical token-overlap (Jaccard), which is coarse but
free and deterministic.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass, field
from typing import Callable


@dataclass
class ContextAtom:
    """A single quantum of context — an excerpt of a file, a prior message,
    a distilled fact, a tool output, etc."""

    content: str
    kind: str = "generic"
    source: str = ""
    atom_hash: str = ""
    last_sent_task_hash: str = ""
    pinned: bool = False
    tags: list[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        if not self.atom_hash:
            self.atom_hash = hashlib.sha256(self.content.encode("utf-8")).hexdigest()[:16]


Scorer = Callable[[str, str], float]


def _tokenize(text: str) -> set[str]:
    return {t for t in text.lower().replace("-", " ").replace("_", " ").split() if t}


def jaccard_scorer(a: str, b: str) -> float:
    ta, tb = _tokenize(a), _tokenize(b)
    if not ta or not tb:
        return 0.0
    return len(ta & tb) / max(1, len(ta | tb))


def _task_hash(task: str) -> str:
    return hashlib.sha256(task.encode("utf-8")).hexdigest()[:16]


@dataclass
class DeltaPlan:
    """Result of an SDCP diff. The suffix is what actually ships new bytes."""

    prefix_stable: list[ContextAtom] = field(default_factory=list)
    suffix_new: list[ContextAtom] = field(default_factory=list)
    dropped: list[ContextAtom] = field(default_factory=list)
    task_hash: str = ""

    @property
    def total_atoms(self) -> int:
        return len(self.prefix_stable) + len(self.suffix_new)

    def tokens_estimate(self) -> int:
        """Rough token-equivalent of the new payload (chars / 4)."""
        return sum(max(1, len(a.content) // 4) for a in self.suffix_new)


class SemanticDeltaContext:
    """
    Relevance-diff assembler.

    Parameters
    ----------
    relevance_threshold:
        Minimum score (0–1) for an atom to be INCLUDED at all.
    novelty_threshold:
        Minimum score difference above what is already cached to SHIP the
        atom rather than rely on cache.  If 0, any relevant atom is shipped
        unless already cached for this exact task.
    scorer:
        ``(query, content) -> float`` — defaults to Jaccard overlap.
    """

    def __init__(
        self,
        *,
        relevance_threshold: float = 0.08,
        novelty_threshold: float = 0.0,
        scorer: Scorer | None = None,
    ) -> None:
        self.relevance_threshold = relevance_threshold
        self.novelty_threshold = novelty_threshold
        self.scorer: Scorer = scorer or jaccard_scorer

    def diff(
        self,
        atoms: list[ContextAtom],
        task_intent: str,
    ) -> DeltaPlan:
        """
        Compute the SDCP plan for one LLM turn.

        * Pinned atoms (system prompt, durable conventions) always go in the
          stable prefix, regardless of score — these benefit from provider
          prompt caching.
        * Other atoms are scored for relevance; atoms below the threshold
          are dropped.
        * Remaining atoms are shipped in the suffix UNLESS they were already
          sent under this exact task hash (no novelty), in which case the
          provider's cache covers them and we skip re-transmission.
        """
        th = _task_hash(task_intent)
        plan = DeltaPlan(task_hash=th)
        for atom in atoms:
            if atom.pinned:
                plan.prefix_stable.append(atom)
                continue
            score = self.scorer(task_intent, atom.content)
            if score < self.relevance_threshold:
                plan.dropped.append(atom)
                continue
            already_sent = atom.last_sent_task_hash == th
            if already_sent and self.novelty_threshold <= 0:
                plan.dropped.append(atom)
                continue
            atom.last_sent_task_hash = th
            plan.suffix_new.append(atom)
        return plan
