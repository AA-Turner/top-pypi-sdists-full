"""Converters — the ONE primitive for "data in shape A becomes data in shape B".

Contract: ``common-docs/systems/architecture/converters/FEATURE.md``.

A **source format** is a known arrival shape (a TikTok profile page saved in a browser, a
ScrapeCreators ``/v2/tiktok/video`` answer, a Bright Data ``tiktok_posts`` row). A **target** is the
shape it becomes (``social_capture``, ``social_post``, ``social.captured_post``, a registered kind).
A **converter** is one versioned, pure mapping from exactly one source format to exactly one target.
The graph is many-to-many: many sources reach one target, one source feeds many targets, and
converters chain (``tiktok.page_html`` → ``social_capture`` → ``social_post``).

Everything here is pure — no network, no database, no AI, nothing from ``aidream``. A host
registers its definitions on :data:`REGISTRY` (or its own :class:`ConverterRegistry`) and owns
persistence (run ledger, provenance on stored rows, replay over stored raw payloads).

Rules the registry enforces:

* **One id, one mapping.** Registering a second, different function under an existing id raises —
  two mappings answering to one name is the defect this primitive exists to end. Re-registering the
  SAME function (a module re-import) is a no-op.
* **Every converter names a real source format.** Unknown source ids raise at registration.
* **Provenance is automatic.** :meth:`ConverterRegistry.convert` returns the output with a
  :class:`Provenance` (converter id, version, code fingerprint, input hash, time). ``code_sha``
  changes whenever the implementation's source changes, so a stored row can be found and replayed
  when its converter improved — even if nobody bumped ``version``.
* **Detection is declared, never guessed.** A source format's ``detect`` predicate answers "is this
  payload mine?" from the payload's CONTENT; a caller that already knows the format passes
  ``hints={"format": id}``. Two claimants is never resolved silently: ``convert_to`` refuses with
  :class:`AmbiguousSource` naming them.
* **Targets are declared.** A converter's target must be a registered :class:`Target`: a registered
  kind slug and/or a contract model the output is validated against.
* **Failures are recorded, never lost.** ``convert`` catches the mapping's exception and returns a
  ``failed`` Conversion; a ``many`` hop that fails on item N keeps every other item and names N.
"""

from __future__ import annotations

import hashlib
import inspect
import json
from collections import deque
from collections.abc import Callable, Iterable, Mapping
from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any

from pydantic import BaseModel, ConfigDict

from matrx_graph.content_ir.audit import TranslationReport

Detect = Callable[[Any, Mapping[str, Any]], bool]
ConvertFn = Callable[[Any, Mapping[str, Any]], Any]


class ConverterError(ValueError):
    """A registration or lookup the registry refuses (duplicate id, unknown format, no path)."""


class AmbiguousSource(ConverterError):
    """More than one source format claims a payload; the caller must name one (``hints["format"]``)."""

    def __init__(self, claimants: list[str]) -> None:
        self.claimants = claimants
        super().__init__(f"{len(claimants)} source formats claim this payload: {', '.join(claimants)}")


@dataclass(frozen=True)
class Target:
    """A shape converters may produce. ``kind`` names the registered content-ir kind it is (or feeds);
    ``contract`` is the model every output item must validate as. At least one is required."""

    id: str
    label: str
    kind: str | None = None
    contract: type[BaseModel] | None = None
    description: str = ""


@dataclass(frozen=True)
class SourceFormat:
    """One known arrival shape.

    ``id`` is ``<origin>.<what>`` in snake_case (``tiktok.page_html``,
    ``scrapecreators.tiktok.video``). ``detect`` is optional: a format without one is matched only
    when the caller names it in ``hints["format"]``.
    """

    id: str
    label: str
    description: str = ""
    media_type: str = "application/json"
    detect: Detect | None = None
    #: Set for an organization's own (database-defined) format: only payloads converted for that
    #: organization (``hints["organization_id"]``) are ever detected as it.
    organization_id: str | None = None


@dataclass(frozen=True)
class Converter:
    """One versioned mapping: ``source`` format → ``target`` shape.

    ``fn(payload, hints)`` returns the target value — a model, a dict, or (``many=True``) a list of
    them. When ``returns_report`` is set it returns ``(output, TranslationReport)`` (the key-audit
    contract of ``content_ir.audit``). ``impl`` is the function whose source fingerprints the
    mapping (defaults to ``fn``; set it when ``fn`` is a thin adapter around a library function).
    ``samples`` are repo-relative paths of REAL captured payloads this converter must handle.
    """

    id: str
    source: str
    target: str
    version: int
    fn: ConvertFn
    label: str = ""
    description: str = ""
    target_kind: str | None = None
    many: bool = False
    returns_report: bool = False
    impl: Callable[..., Any] | None = None
    samples: tuple[str, ...] = ()
    #: Loads a sample file into the payload ``fn`` takes (default: parse JSON).
    sample_loader: Callable[[str], Any] | None = None
    #: Extra modules whose source is part of the mapping (helpers ``impl`` calls from other modules).
    code_modules: tuple[str, ...] = ()
    #: An organization's own converter (database-defined). None = a platform converter.
    organization_id: str | None = None
    #: Fingerprint for a mapping that is DATA, not code (a database-defined spec): used instead of source.
    spec_sha: str | None = None
    code_sha: str = field(default="", compare=False)

    def describe(self) -> dict[str, Any]:
        impl = self.impl or self.fn
        return {
            "id": self.id,
            "source": self.source,
            "target": self.target,
            "version": self.version,
            "code_sha": self.code_sha,
            "label": self.label or self.id,
            "description": self.description,
            "target_kind": self.target_kind,
            "many": self.many,
            "impl": f"{getattr(impl, '__module__', '?')}.{getattr(impl, '__qualname__', '?')}",
            "samples": list(self.samples),
            "organization_id": self.organization_id,
            "defined_in": "database" if self.spec_sha else "code",
        }


class Provenance(BaseModel):
    """Which converter made a value. Stamped on every converted row (``metadata.converted_by``)."""

    model_config = ConfigDict(extra="forbid")

    converter: str
    version: int
    code_sha: str
    source_format: str
    target: str
    input_sha256: str | None = None
    converted_at: str

    def stamp(self) -> dict[str, Any]:
        """The compact form stored on rows: enough to find and replay it, nothing more."""
        return {"converter": self.converter, "version": self.version, "code_sha": self.code_sha,
                "input_sha256": self.input_sha256, "converted_at": self.converted_at}


@dataclass
class Conversion:
    """One converter applied to one payload (or, for an item-wise hop, to each item of a list)."""

    converter: Converter
    output: Any
    provenance: Provenance
    report: TranslationReport | None = None
    #: ``[{"index": n | None, "error": "<Type>: <message>"}]`` — n is the input item that failed.
    failures: list[dict[str, Any]] = field(default_factory=list)
    #: Source formats that claimed the payload when it was detected (empty when the caller named it).
    claimants: list[str] = field(default_factory=list)
    #: The exceptions behind ``failures`` (same order), for a caller that must re-raise the original.
    errors: list[BaseException] = field(default_factory=list, repr=False)

    @property
    def items(self) -> list[Any]:
        if self.output is None:
            return []
        return list(self.output) if isinstance(self.output, list) else [self.output]

    @property
    def status(self) -> str:
        """``ok`` (no failure) · ``partial`` (some items failed) · ``failed`` (nothing came out)."""
        if not self.failures:
            return "ok"
        return "partial" if self.items else "failed"


def code_fingerprint(fn: Callable[..., Any], modules: Iterable[str] = ()) -> str:
    """sha256 (12 hex) of the source of ``fn``'s WHOLE module plus every named module.

    A mapping is its function and the helpers beside it, so the module is fingerprinted, not just the
    function; helpers living elsewhere are named in ``Converter.code_modules``.
    """
    from matrx_utils.module_loading import load_declared_module

    parts: list[str] = []
    for name in (getattr(fn, "__module__", None), *modules):
        if not name:
            continue
        try:
            parts.append(inspect.getsource(load_declared_module(name)))
        except (OSError, TypeError, ImportError):
            parts.append(name)
    if not parts:
        parts.append(f"{getattr(fn, '__qualname__', repr(fn))}")
    parts.append(getattr(fn, "__qualname__", ""))
    return hashlib.sha256("\n".join(parts).encode()).hexdigest()[:12]


def payload_sha256(payload: Any) -> str | None:
    """A stable hash of the input (str/bytes as-is, everything else as sorted JSON)."""
    if payload is None:
        return None
    if isinstance(payload, bytes):
        data = payload
    elif isinstance(payload, str):
        data = payload.encode()
    elif isinstance(payload, BaseModel):
        data = payload.model_dump_json().encode()
    else:
        try:
            data = json.dumps(payload, sort_keys=True, default=str).encode()
        except (TypeError, ValueError):
            data = repr(payload).encode()
    return hashlib.sha256(data).hexdigest()


class ConverterRegistry:
    """The registry: formats, converters, detection, chaining and running."""

    def __init__(self) -> None:
        self._formats: dict[str, SourceFormat] = {}
        self._converters: dict[str, Converter] = {}
        self._targets: dict[str, Target] = {}

    def register_target(self, target: Target) -> Target:
        if target.kind is None and target.contract is None:
            raise ConverterError(f"target {target.id!r} names neither a kind nor a contract model")
        old = self._targets.get(target.id)
        if old is not None and (old.kind, old.contract) != (target.kind, target.contract):
            raise ConverterError(f"target {target.id!r} is already registered differently")
        self._targets[target.id] = target
        return target

    def target(self, target_id: str) -> Target | None:
        return self._targets.get(target_id)

    # ── registration ────────────────────────────────────────────────────────────────────────
    def unregister(self, converter_id: str) -> None:
        """Drop a converter (and its source format when nothing else uses it) — database-defined ones only."""
        conv = self._converters.get(converter_id)
        if conv is None:
            return
        if conv.spec_sha is None:
            raise ConverterError(f"converter {converter_id!r} is defined in code and cannot be unregistered")
        del self._converters[converter_id]
        if not any(c.source == conv.source for c in self._converters.values()):
            self._formats.pop(conv.source, None)

    def register_format(self, fmt: SourceFormat) -> SourceFormat:
        old = self._formats.get(fmt.id)
        if old is not None and old != fmt and fmt.organization_id is None and _qual(old.detect) != _qual(fmt.detect):
            raise ConverterError(f"source format {fmt.id!r} is already registered differently")
        self._formats[fmt.id] = fmt
        return fmt

    def register(self, conv: Converter) -> Converter:
        if not conv.id or not conv.source or not conv.target:
            raise ConverterError("a converter needs an id, a source format and a target")
        if conv.version < 1:
            raise ConverterError(f"converter {conv.id!r}: version starts at 1")
        if conv.target not in self._targets:
            raise ConverterError(f"converter {conv.id!r}: target {conv.target!r} is not a registered target")
        if conv.source not in self._formats and not self._is_target(conv.source):
            raise ConverterError(
                f"converter {conv.id!r}: source {conv.source!r} is neither a registered source "
                f"format nor another converter's target — register the format first")
        sha = conv.spec_sha or code_fingerprint(conv.impl or conv.fn, conv.code_modules)
        conv = _with(conv, code_sha=sha)
        old = self._converters.get(conv.id)
        if old is not None and conv.spec_sha is None and (_qual(old.impl or old.fn) != _qual(conv.impl or conv.fn)
                                                          or (old.source, old.target) != (conv.source, conv.target)):
            raise ConverterError(f"converter id {conv.id!r} is already registered to a different mapping")
        self._converters[conv.id] = conv
        return conv

    def _is_target(self, shape: str) -> bool:
        return any(c.target == shape for c in self._converters.values())

    # ── lookup ──────────────────────────────────────────────────────────────────────────────
    def formats(self) -> list[SourceFormat]:
        return sorted(self._formats.values(), key=lambda f: f.id)

    def converters(self) -> list[Converter]:
        return sorted(self._converters.values(), key=lambda c: c.id)

    def get(self, converter_id: str) -> Converter:
        try:
            return self._converters[converter_id]
        except KeyError:
            raise ConverterError(f"no converter {converter_id!r}") from None

    def format(self, format_id: str) -> SourceFormat | None:
        return self._formats.get(format_id)

    def for_source(self, source: str) -> list[Converter]:
        return [c for c in self.converters() if c.source == source]

    def for_target(self, target: str) -> list[Converter]:
        return [c for c in self.converters() if c.target == target]

    def targets(self) -> list[str]:
        return sorted({c.target for c in self._converters.values()})

    def target_defs(self) -> list[Target]:
        return sorted(self._targets.values(), key=lambda t: t.id)

    # ── detection ───────────────────────────────────────────────────────────────────────────
    def detect(self, payload: Any, hints: Mapping[str, Any] | None = None) -> list[str]:
        """Every source format that claims this payload. A named ``hints["format"]`` wins outright."""
        hints = hints or {}
        named = hints.get("format")
        if named:
            fmt = self._formats.get(named)
            if fmt is not None and fmt.organization_id is not None and fmt.organization_id != hints.get("organization_id"):
                return []
            return [named] if fmt is not None or self._is_target(named) else []
        out: list[str] = []
        org = hints.get("organization_id")
        for fmt in self.formats():
            if fmt.detect is None or (fmt.organization_id is not None and fmt.organization_id != org):
                continue
            try:
                if fmt.detect(payload, hints):
                    out.append(fmt.id)
            except Exception:  # noqa: BLE001 — a broken detector is a non-match, never a crash
                continue
        return out

    def match(self, payload: Any, hints: Mapping[str, Any] | None = None, *,
              target: str | None = None) -> list[Converter]:
        """Given this payload: the converters that apply (optionally only those reaching ``target``)."""
        found: list[Converter] = []
        for fmt in self.detect(payload, hints):
            for conv in self.for_source(fmt):
                if target is None or conv.target == target:
                    found.append(conv)
        return found

    def path(self, source: str, target: str) -> list[Converter]:
        """The shortest converter chain from ``source`` to ``target`` (``[]`` when they are equal)."""
        if source == target:
            return []
        seen = {source}
        queue: deque[tuple[str, list[Converter]]] = deque([(source, [])])
        while queue:
            shape, chain = queue.popleft()
            for conv in self.for_source(shape):
                if conv.target in seen:
                    continue
                nxt = [*chain, conv]
                if conv.target == target:
                    return nxt
                seen.add(conv.target)
                queue.append((conv.target, nxt))
        raise ConverterError(f"no converter chain from {source!r} to {target!r}")

    # ── running ─────────────────────────────────────────────────────────────────────────────
    def convert(self, converter: str | Converter, payload: Any,
                hints: Mapping[str, Any] | None = None, *, item_wise: bool = False) -> Conversion:
        """Run one converter. Never raises for a mapping error: the Conversion says ``failed``.

        ``item_wise=True`` runs the converter once per item of ``payload`` (a list) and joins the
        results; an item that fails is recorded by index and the rest are kept.
        """
        conv = self.get(converter) if isinstance(converter, str) else converter
        hints = dict(hints or {})
        prov = Provenance(converter=conv.id, version=conv.version, code_sha=conv.code_sha,
                          source_format=conv.source, target=conv.target,
                          input_sha256=payload_sha256(payload),
                          converted_at=datetime.now(UTC).isoformat())
        failures: list[dict[str, Any]] = []
        errors: list[BaseException] = []
        report: TranslationReport | None = None
        inputs = list(payload) if item_wise else [payload]
        out: list[Any] = []
        for i, one in enumerate(inputs):
            try:
                raw = conv.fn(one, hints)
                if conv.returns_report:
                    raw, report = raw
                got = list(raw) if (conv.many and raw is not None) else ([] if raw is None else [raw])
                out.extend(self._checked(conv, got))
            except Exception as exc:  # noqa: BLE001 — a mapping error is a recorded outcome
                failures.append({"index": i if item_wise else None, "error": f"{type(exc).__name__}: {exc}"[:500]})
                errors.append(exc)
        single = not (conv.many or item_wise)
        output: Any = (out[0] if out else None) if single else out
        return Conversion(converter=conv, output=output, provenance=prov, report=report, failures=failures,
                          errors=errors)

    def _checked(self, conv: Converter, items: list[Any]) -> list[Any]:
        target = self._targets.get(conv.target)
        model = target.contract if target else None
        if model is None:
            return items
        for i in items:  # validated, never reshaped: the output stays what the mapping returned
            if not isinstance(i, model):
                model.model_validate(i)
        return items

    def convert_to(self, payload: Any, target: str, hints: Mapping[str, Any] | None = None,
                   *, source: str | None = None) -> list[Conversion]:
        """Detect (or take ``source``), find the chain to ``target``, run it. One Conversion per hop.

        After a hop that yields a list (``many``), the next hop runs once per item. Two claimants for
        the payload raise :class:`AmbiguousSource`. The chain stops at a hop that produced nothing.
        """
        hints = dict(hints or {})
        claimants: list[str] = []
        if source is None:
            claimants = self.detect(payload, hints)
            if not claimants:
                raise ConverterError("no registered source format claims this payload")
            if len(claimants) > 1:
                raise AmbiguousSource(claimants)
            source = claimants[0]
        chain = self.path(source, target)
        out: list[Conversion] = []
        current: Any = payload
        listy = False
        for conv in chain:
            step = self.convert(conv, current, hints, item_wise=listy)
            if not out:
                step.claimants = claimants
            out.append(step)
            if step.status == "failed":
                break
            current = step.output
            listy = conv.many or listy
        return out


def load_sample(conv: Converter, sample: str, root: str | None = None) -> Any:
    """Load one of ``conv.samples``. ``"path/file.json#a/0/b"`` digs to that pointer inside the file.

    A converter with its own ``sample_loader`` receives the full sample string (pointer included).
    """
    from pathlib import Path

    if conv.sample_loader is not None:
        return conv.sample_loader(str(Path(root) / sample) if root else sample)
    rel, _, pointer = sample.partition("#")
    path = Path(root) / rel if root else Path(rel)
    data: Any = json.loads(path.read_text())
    for part in [p for p in pointer.split("/") if p]:
        data = data[int(part)] if isinstance(data, list) else data[part]
    return data


def _qual(fn: Any) -> str:
    return f"{getattr(fn, '__module__', '')}.{getattr(fn, '__qualname__', repr(fn))}" if fn else ""


def _with(conv: Converter, **changes: Any) -> Converter:
    from dataclasses import replace

    return replace(conv, **changes)


#: The process-wide registry hosts register onto.
REGISTRY = ConverterRegistry()


def register_targets(targets: Iterable[Target], registry: ConverterRegistry = REGISTRY) -> None:
    for t in targets:
        registry.register_target(t)


def register_formats(formats: Iterable[SourceFormat], registry: ConverterRegistry = REGISTRY) -> None:
    for fmt in formats:
        registry.register_format(fmt)


def converter(*, id: str, source: str, target: str, version: int, label: str = "", description: str = "",
              target_kind: str | None = None, many: bool = False, returns_report: bool = False,
              samples: Iterable[str] = (), sample_loader: Callable[[str], Any] | None = None,
              registry: ConverterRegistry = REGISTRY) -> Callable[[ConvertFn], ConvertFn]:
    """Decorator: register ``fn(payload, hints)`` as a converter and return it unchanged."""

    def wrap(fn: ConvertFn) -> ConvertFn:
        registry.register(Converter(id=id, source=source, target=target, version=version, fn=fn, label=label,
                                    description=description, target_kind=target_kind, many=many,
                                    returns_report=returns_report, samples=tuple(samples),
                                    sample_loader=sample_loader))
        return fn

    return wrap


__all__ = [
    "REGISTRY", "AmbiguousSource", "Conversion", "ConvertFn", "Converter", "ConverterError", "ConverterRegistry",
    "Detect", "Provenance", "SourceFormat", "Target", "code_fingerprint", "converter", "load_sample", "payload_sha256",
    "register_formats", "register_targets",
]
