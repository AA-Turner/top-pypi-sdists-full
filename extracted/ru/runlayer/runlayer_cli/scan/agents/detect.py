"""Framework detection scoring engine.

Given a discovered :class:`~runlayer_cli.scan.agents.discover.AgentUnit`, score
every framework in the registry (``signatures.json``) by combining four evidence
channels:

* declared dependencies in the manifest (strongest signal),
* generic shared dependencies (weak signal),
* canonical import statements found in source,
* canonical API symbols found in source.

The highest-scoring framework wins. The result (:class:`DiscoveredAgent`) carries
a confidence (share of total evidence mass), a relative margin over the
runner-up, the concrete evidence behind the decision, and a stable fingerprint
for per-org catalog dedupe.

A second, at-rest install channel (e.g. OpenClaw) constructs
:class:`DiscoveredAgent` objects directly via :func:`build_install_agent` rather
than through the scorer. Runtime liveness for those agents is classified by the
shared process channel.

Standard-library only (plus the RE2 ``regex_safe`` wrapper).
"""

from __future__ import annotations

import hashlib
import time
from collections.abc import Callable, Iterable, Mapping, Sequence
from dataclasses import dataclass, field
from functools import lru_cache
from pathlib import Path

from runlayer_cli import regex_safe
from runlayer_cli.scan.agents.discover import AgentUnit, discover
from runlayer_cli.scan.agents.languages import language_family
from runlayer_cli.scan.agents.manifests import (
    ManifestInfo,
    manifest_ecosystem,
    manifest_kind,
    normalize_dep,
)
from runlayer_cli.scan.agents.redact import redact_basename, sanitize_path
from runlayer_cli.scan.agents.registry import (
    FrameworkSignature,
    Registry,
    load_registry,
)

# Score multiplier applied when a framework's language family is incompatible
# with the unit's detected languages. Soft (not zero) so it only breaks ties.
INCOMPATIBLE_LANGUAGE_PENALTY = 0.1
MIN_DETECTION_SCORE = 2
SINGLE_EVIDENCE_CONFIDENCE_CAP = 0.75

# Detection channels.
METHOD_STATIC = "static"
METHOD_INSTALL = "install"

# The backend agent-report contract requires a non-null language, but
# install-channel agents (e.g. OpenClaw) carry none. The wire payload substitutes
# this sentinel so those agents still ingest; detection/display keep ``None``.
UNKNOWN_LANGUAGE = "unknown"


@dataclass
class Evidence:
    """A single matched detection signal."""

    kind: str  # package_dep | shared_dep | import | symbol | install_artifact | ...
    value: str
    source: str  # file where the signal was found, or an install-marker label

    def to_dict(self) -> dict:
        return {"kind": self.kind, "value": self.value, "source": self.source}


@dataclass
class FrameworkScore:
    """Per-framework scoring breakdown for one unit (kept for explainability)."""

    framework_id: str
    display_name: str
    language: str
    score: float
    raw_score: float
    language_compatible: bool
    counts: dict[str, int]
    evidence: list[Evidence] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "framework_id": self.framework_id,
            "display_name": self.display_name,
            "language": self.language,
            "score": round(self.score, 3),
            "raw_score": round(self.raw_score, 3),
            "language_compatible": self.language_compatible,
            "counts": self.counts,
            "evidence": [e.to_dict() for e in self.evidence],
        }


@dataclass
class DiscoveredAgent:
    """The detection outcome for one agent location.

    ``framework_id`` is ``None`` when no framework signal was found -- the
    location is reported as ``unknown`` (not an agent) rather than guessed.
    """

    location: str
    name: str
    framework_id: str | None
    display_name: str | None
    language: str | None
    confidence: float
    margin: float
    score: float
    runner_up: str | None
    runner_up_score: float
    detection_method: str
    evidence: list[Evidence]
    manifests: list[str] = field(default_factory=list)
    languages: list[str] = field(default_factory=list)
    agent_fingerprint: str | None = None
    scores: list[FrameworkScore] = field(default_factory=list)

    @property
    def is_agent(self) -> bool:
        return self.framework_id is not None

    def to_dict(self, *, top_n: int = 3) -> dict:
        return {
            "location": self.location,
            "name": self.name,
            "framework_id": self.framework_id,
            "display_name": self.display_name,
            "language": self.language,
            "confidence": round(self.confidence, 3),
            "margin": round(self.margin, 3),
            "score": round(self.score, 3),
            "runner_up": self.runner_up,
            "runner_up_score": round(self.runner_up_score, 3),
            "detection_method": self.detection_method,
            "agent_fingerprint": self.agent_fingerprint,
            "manifests": self.manifests,
            "languages": self.languages,
            "evidence": [e.to_dict() for e in self.evidence],
            "scores": [s.to_dict() for s in self.scores[:top_n]],
        }

    def to_api_payload(self, *, usernames: Sequence[str] = ()) -> dict:
        """Redacted per-agent submission payload for ``POST /ai-watch/agents``.

        Carries only non-sensitive identity + sanitized evidence -- never file
        contents or environment variables (which are never collected). The
        location and evidence values are scrubbed of home usernames / URL
        credentials / embedded secrets, and evidence sources are reduced to
        basenames. ``language`` falls back to :data:`UNKNOWN_LANGUAGE` because the
        backend requires a non-null value while install-channel agents carry none.

        ``usernames`` is the report's authoritative path owner(s) (device
        context), threaded into :func:`sanitize_path` so the account name is
        redacted even outside the standard home layout.

        Only meaningful on a real agent (:attr:`is_agent`); a no-signal location
        has a ``None`` fingerprint the backend rejects, so callers filter first.
        """
        return {
            "agent_fingerprint": self.agent_fingerprint,
            "framework_id": self.framework_id,
            "language": self.language or UNKNOWN_LANGUAGE,
            "root_path": sanitize_path(self.location, usernames=usernames),
            "confidence": round(self.confidence, 3),
            "manifest_files": self.manifests,
            "evidence": [
                {
                    "kind": e.kind,
                    "value": sanitize_path(e.value, usernames=usernames),
                    "source": redact_basename(e.source),
                }
                for e in self.evidence
            ],
        }


def compute_fingerprint(
    framework_id: str, language: str | None, markers: Iterable[str]
) -> str:
    """Stable identity hash over framework + language + normalized markers.

    Ephemeral data (host, absolute path, timestamps) is intentionally excluded so
    the same agent project deduplicates across machines in a per-org catalog.
    Markers are sorted so ordering never changes the hash.
    """
    payload = "\x1f".join(
        [framework_id, language or "", *sorted({m for m in markers if m})]
    )
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def _is_word_char(ch: str) -> bool:
    return ch.isalnum() or ch == "_"


@lru_cache(maxsize=4096)
def _needle_pattern(needle: str) -> regex_safe.Pattern:
    """Word-boundary-anchored matcher for an import/symbol needle.

    Plain substring search lets ``tool`` match ``tools`` -- and lets any token
    hit inside comments, strings, or unrelated identifiers -- inflating scores
    and making signatures hard to tune (F7). Anchor an identifier boundary on
    each *word-char* edge of the needle, so ``tool`` matches ``tool`` but not
    ``tools``/``mytool``; edges that are already punctuation (``openai(``,
    ``@scope/pkg``) keep matching verbatim. Patterns are cached -- the same
    handful of needles is searched across every source file of every unit.

    RE2 has no lookaround, so the old zero-width guards
    ``(?<![A-Za-z0-9_])needle(?![A-Za-z0-9_])`` are spelled in consuming form:
    ``(?:\\A|[^A-Za-z0-9_])needle(?:[^A-Za-z0-9_]|\\z)``. A boundary char is
    consumed by the match, which is fine because the only consumer is the
    boolean ``pattern.search(...)`` in :meth:`Detector._source_match` — match
    EXISTENCE is identical to the lookaround form (a hit at payload position
    ``i`` exists iff the char before/after is absent or non-word in both
    spellings). Do not start reading spans off this pattern.
    """
    if not needle:
        # Matches nothing: `\z` (end of text) can never be followed by a
        # char, on any input including "". (RE2 rejects the old stdlib
        # `(?!x)x` sentinel — negative lookahead.)
        return regex_safe.compile(r"\z.")
    prefix = r"(?:\A|[^A-Za-z0-9_])" if _is_word_char(needle[0]) else ""
    suffix = r"(?:[^A-Za-z0-9_]|\z)" if _is_word_char(needle[-1]) else ""
    return regex_safe.compile(prefix + regex_safe.escape(needle) + suffix)


class Detector:
    """Scores agent units against the framework registry."""

    def __init__(self, registry: Registry):
        self.weights = registry.weights
        self.frameworks: tuple[FrameworkSignature, ...] = registry.frameworks
        # Precompute each framework's package ecosystem from its manifest token,
        # and index frameworks by ecosystem + language family so detect() only
        # scores the handful that could plausibly match a unit instead of the
        # whole registry (F3: drops the O(units x frameworks x sources) loop to
        # O(units x candidates x sources)).
        self._ecosystems: dict[str, str] = {}
        self._by_ecosystem: dict[str, list[FrameworkSignature]] = {}
        self._by_family: dict[str, list[FrameworkSignature]] = {}
        for fw in self.frameworks:
            token = fw.manifest_files[0]
            kind = manifest_kind(token) or token
            ecosystem = manifest_ecosystem(kind)
            self._ecosystems[fw.framework_id] = ecosystem
            self._by_ecosystem.setdefault(ecosystem, []).append(fw)
            family = language_family(fw.language)
            if family is not None:
                self._by_family.setdefault(family, []).append(fw)

    def detect(self, unit: AgentUnit) -> DiscoveredAgent:
        unit_families: set[str] = {
            family
            for lang in unit.languages
            if (family := language_family(lang)) is not None
        }

        scores = [
            self._score_framework(unit, fw, unit_families)
            for fw in self._candidates(unit, unit_families)
        ]
        scores.sort(key=lambda s: s.score, reverse=True)

        positives = [s for s in scores if s.score >= MIN_DETECTION_SCORE]
        manifests = sorted({m.path.name for m in unit.manifests})
        languages = sorted(unit.languages)

        if not positives:
            return DiscoveredAgent(
                location=str(unit.root),
                name=unit.name,
                framework_id=None,
                display_name=None,
                language=None,
                confidence=0.0,
                margin=0.0,
                score=0.0,
                runner_up=None,
                runner_up_score=0.0,
                detection_method=METHOD_STATIC,
                evidence=[],
                manifests=manifests,
                languages=languages,
                agent_fingerprint=None,
                scores=scores,
            )

        top = positives[0]
        runner = positives[1] if len(positives) > 1 else None
        total = sum(s.score for s in positives)
        confidence = top.score / total if total else 0.0
        if len(top.evidence) == 1:
            confidence = min(confidence, SINGLE_EVIDENCE_CONFIDENCE_CAP)
        runner_score = runner.score if runner else 0.0
        margin = (top.score - runner_score) / top.score if top.score else 0.0

        fingerprint = compute_fingerprint(
            top.framework_id, top.language, self._identity_markers(unit)
        )

        return DiscoveredAgent(
            location=str(unit.root),
            name=unit.name,
            framework_id=top.framework_id,
            display_name=top.display_name,
            language=top.language,
            confidence=confidence,
            margin=margin,
            score=top.score,
            runner_up=runner.framework_id if runner else None,
            runner_up_score=runner_score,
            detection_method=METHOD_STATIC,
            evidence=top.evidence,
            manifests=manifests,
            languages=languages,
            agent_fingerprint=fingerprint,
            scores=scores,
        )

    @staticmethod
    def _identity_markers(unit: AgentUnit) -> list[str]:
        """Normalized project markers for the fingerprint.

        Prefer the normalized dependency set (stable across machines); fall back
        to the project-root basename for manifest-less source units.
        """
        deps = sorted(unit.deps)
        return deps if deps else [unit.root.name]

    def _candidates(
        self, unit: AgentUnit, unit_families: set[str]
    ) -> list[FrameworkSignature]:
        """Frameworks worth scoring for ``unit``.

        Only frameworks whose package ecosystem matches one of the unit's
        manifests, or whose language family matches one of the unit's languages,
        can plausibly match -- everything else scores zero (or a penalized
        near-zero on a stray cross-language substring). A unit with no manifests
        and no recognized language has no signal, so no candidates. Registry
        order is preserved for stable, explainable score lists.
        """
        selected: set[str] = set()
        for ecosystem in unit.ecosystems:
            selected.update(
                fw.framework_id for fw in self._by_ecosystem.get(ecosystem, ())
            )
        for family in unit_families:
            selected.update(fw.framework_id for fw in self._by_family.get(family, ()))
        return [fw for fw in self.frameworks if fw.framework_id in selected]

    def _score_framework(
        self, unit: AgentUnit, fw: FrameworkSignature, unit_families: set[str]
    ) -> FrameworkScore:
        ecosystem = self._ecosystems[fw.framework_id]
        evidence: list[Evidence] = []
        counts = {"package_dep": 0, "shared_dep": 0, "import": 0, "symbol": 0}

        for dep in fw.package_deps:
            source = self._dep_source(unit, normalize_dep(dep, ecosystem))
            if source:
                evidence.append(Evidence("package_dep", dep, source))
                counts["package_dep"] += 1

        for dep in fw.shared_deps:
            source = self._dep_source(unit, normalize_dep(dep, ecosystem))
            if source:
                evidence.append(Evidence("shared_dep", dep, source))
                counts["shared_dep"] += 1

        for needle in fw.imports:
            source = self._source_match(unit, needle)
            if source:
                evidence.append(Evidence("import", needle, source))
                counts["import"] += 1

        for needle in fw.symbols:
            source = self._source_match(unit, needle)
            if source:
                evidence.append(Evidence("symbol", needle, source))
                counts["symbol"] += 1

        raw = float(
            counts["package_dep"] * self.weights["package_dep"]
            + counts["shared_dep"] * self.weights["shared_dep"]
            + counts["import"] * self.weights["import"]
            + counts["symbol"] * self.weights["symbol"]
        )

        family = language_family(fw.language)
        compatible = (not unit_families) or (family in unit_families)
        score = raw if compatible else raw * INCOMPATIBLE_LANGUAGE_PENALTY

        return FrameworkScore(
            framework_id=fw.framework_id,
            display_name=fw.display_name,
            language=fw.language,
            score=score,
            raw_score=raw,
            language_compatible=compatible,
            counts=counts,
            evidence=evidence,
        )

    @staticmethod
    def _dep_source(unit: AgentUnit, normalized_dep: str) -> str | None:
        for manifest in unit.manifests:
            if normalized_dep in manifest.deps:
                return manifest.path.name
        return None

    @staticmethod
    def _source_match(unit: AgentUnit, needle: str) -> str | None:
        pattern = _needle_pattern(needle)
        for source_file in unit.sources:
            if pattern.search(source_file.text):
                return source_file.path.name
        return None


def build_install_agent(
    *,
    framework_id: str,
    display_name: str,
    location: str,
    evidence: list[Evidence],
    language: str | None = None,
    markers: Iterable[str] | None = None,
    confidence: float = 1.0,
) -> DiscoveredAgent:
    """Construct a :class:`DiscoveredAgent` for an install-detected agent.

    At-rest install detection (binary / state / config / app artifacts) is a
    separate channel from the static scorer: the match is deterministic, so
    confidence defaults to ``1.0`` and the runner-up margin is the full score.
    """
    fingerprint = compute_fingerprint(
        framework_id, language, markers if markers is not None else []
    )
    return DiscoveredAgent(
        location=location,
        name=Path(location).name or framework_id,
        framework_id=framework_id,
        display_name=display_name,
        language=language,
        confidence=confidence,
        margin=1.0,
        score=float(len(evidence)),
        runner_up=None,
        runner_up_score=0.0,
        detection_method=METHOD_INSTALL,
        evidence=evidence,
        manifests=[],
        languages=[language] if language else [],
        agent_fingerprint=fingerprint,
        scores=[],
    )


def load_detector(signatures_path: str | Path | None = None) -> Detector:
    """Build a :class:`Detector` from the (default or given) signature registry."""
    return Detector(load_registry(signatures_path))


def _fingerprint_collisions(
    detections: Sequence[tuple[DiscoveredAgent, AgentUnit]],
) -> list[list[tuple[DiscoveredAgent, AgentUnit]]]:
    by_fingerprint: dict[
        str,
        list[tuple[DiscoveredAgent, AgentUnit]],
    ] = {}
    for detection, unit in detections:
        if detection.agent_fingerprint is not None:
            by_fingerprint.setdefault(detection.agent_fingerprint, []).append(
                (detection, unit)
            )
    return [
        group
        for group in by_fingerprint.values()
        if len({detection.location for detection, _unit in group}) > 1
    ]


def _shortest_unique_path_suffixes(units: Sequence[AgentUnit]) -> list[str]:
    """Return normalized minimal path suffixes that distinguish ``units``."""
    paths = [Path(unit.root) for unit in units]
    parts_by_path: list[tuple[str, ...]] = []
    for path in paths:
        parts = path.parts
        if path.anchor and parts and parts[0] == path.anchor:
            parts = parts[1:]
        parts_by_path.append(parts)

    for width in range(1, max(map(len, parts_by_path), default=0) + 1):
        suffixes = ["/".join(parts[-width:]) for parts in parts_by_path]
        if len(set(suffixes)) == len(suffixes):
            return suffixes
    return [path.as_posix().lstrip("/") for path in paths]


def _disambiguate_fingerprint_collisions(
    detections: Sequence[tuple[DiscoveredAgent, AgentUnit]],
) -> None:
    """Add stable project identity only where dependency fingerprints collide."""
    for group in _fingerprint_collisions(detections):
        for detection, unit in group:
            if detection.framework_id is None:
                continue
            markers = [
                *Detector._identity_markers(unit),
                f"root:{unit.root.name}",
            ]
            detection.agent_fingerprint = compute_fingerprint(
                detection.framework_id,
                detection.language,
                markers,
            )

    for group in _fingerprint_collisions(detections):
        suffixes = _shortest_unique_path_suffixes([unit for _detection, unit in group])
        for (detection, unit), suffix in zip(group, suffixes, strict=True):
            if detection.framework_id is None:
                continue
            markers = [
                *Detector._identity_markers(unit),
                f"root:{unit.root.name}",
                f"path:{suffix}",
            ]
            detection.agent_fingerprint = compute_fingerprint(
                detection.framework_id,
                detection.language,
                markers,
            )


def collect_agents(
    roots: Iterable[str | Path],
    *,
    detector: Detector | None = None,
    min_confidence: float = 0.0,
    include_unknown: bool = False,
    seed_manifests: Mapping[Path, ManifestInfo] | None = None,
    deadline: float | None = None,
    checkpoint: Callable[[], None] | None = None,
) -> list[DiscoveredAgent]:
    """Discover units under each root and run static framework detection.

    Returns detected agents (deduplicated by location) at or above
    ``min_confidence``. When ``include_unknown`` is set, no-signal units are
    returned too (useful for reporting skipped locations).

    ``seed_manifests`` (resolved path -> parsed :class:`ManifestInfo`) is passed
    through to :func:`discover` so manifests the crawl already parsed are reused
    rather than re-parsed by the walk.

    ``deadline`` is an optional :func:`time.monotonic` cutoff shared across all
    roots so the whole static scan stays within its time budget: roots not yet
    reached are skipped, and it is threaded into :func:`discover` so a single
    large root's walk is bounded too. Best-effort -- partial results are still
    returned.

    Scoring is sequential: :meth:`Detector.detect` is CPU-bound regex over
    pre-loaded source text, and CPython's ``re`` engine holds the GIL for the
    match, so a thread pool does not parallelize it (benchmarked ~1.0x). The
    sequential loop stays within the deadline just as well, without the
    submit/window/drain bookkeeping.
    """
    detector = detector or load_detector()
    results: list[DiscoveredAgent] = []
    detected_units: list[tuple[DiscoveredAgent, AgentUnit]] = []
    seen: set[str] = set()
    for root in roots:
        if deadline is not None and time.monotonic() >= deadline:
            break
        for unit in discover(
            root,
            seed_manifests=seed_manifests,
            deadline=deadline,
            checkpoint=checkpoint,
        ):
            # Scoring each unit (regex over every source file) is itself work, so
            # honor the deadline between units too -- otherwise a root that
            # yielded many units before the cutoff would score them all past it.
            if checkpoint is not None:
                checkpoint()
            if deadline is not None and time.monotonic() >= deadline:
                break
            detection = detector.detect(unit)
            # Source text is only needed for scoring; disambiguation below uses
            # manifests/root only. Release it so retained memory tracks scored
            # metadata, not every unit's full source content.
            unit.sources = []
            if detection.location in seen:
                continue
            seen.add(detection.location)
            if detection.is_agent:
                detected_units.append((detection, unit))
            if detection.is_agent and detection.confidence >= min_confidence:
                results.append(detection)
            elif include_unknown and not detection.is_agent:
                results.append(detection)
    _disambiguate_fingerprint_collisions(detected_units)
    results.sort(key=lambda d: d.location)
    return results
