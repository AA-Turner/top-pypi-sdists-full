"""Second-stage attribute decode -- the four producer shapes, normalized once.

A chained classifier (``vehicle_type_classification.py:1-20``: a ViT after the vehicle
detector, under one multi-model deployment) emits its decode *on the detection*, in one of
four shapes that legacy re-implements per usecase:

* ``heads`` -- an additive, multi-attribute map: ``{"vehicle_type": {"label": ..., "confidence":
  ..., "top_k": [...]}}``;
* flat ``label`` + ``class_confidence`` on the detection itself;
* flat ``top_k`` only, the winner being the highest-confidence entry
  (``_winning_top_k``, byte-identical in ``vehicle_type_classification.py:55``,
  ``age_detection.py:54``, ``gender_detection.py`` and ``age_gender_detection.py`` -- this
  module is the one copy);
* a raw ``predictor_output`` logit vector plus an index-to-label map, softmaxed locally
  (``_predictor_output_to_vehicle_type``, ``vehicle_type_classification.py:71-86``).

Per ``vehicle_type_classification.py:17-19``, the decode is deliberately defensive across all
four because the producer contract was never finalized -- "not finalized until the multi-model
chaining is wired (pending sync with Tanush)". Accepting all four here, rather than guessing
one, is P0/P2 of ``classification-primitives.md``.

Like :mod:`matrice_analytics.engine.intake.classification`, this runs in the deployment's
worker **before** :meth:`~matrice_analytics.engine.runtime.session.Session.process_frame`, and
is deliberately not a registered primitive: it turns a producer envelope into the flat
``attributes`` spelling :func:`~matrice_analytics.engine.runtime.session._to_attributes`
already reads, and nothing in ``engine/primitives`` should know this producer exists::

    detections = attach_attributes(raw, specs=[AttributeSpec("vehicle_type", ...)])
    outcome = session.process_frame(detections, frame_ts=...)

Envelope handling (``_iter_detections``) is the same three shapes
``vehicle_type_classification._attach_vehicle_type_attributes`` walks (:147): a bare list,
``{"detections": [...]}``, and a ``frame_id -> list`` mapping (matching
``_normalize_yolo_results``'s own envelope handling, so a caller need not know which shape it
has before calling either).
"""

from __future__ import annotations

import math
import re
from collections.abc import Iterator, Mapping, Sequence
from dataclasses import dataclass, field
from typing import Any, Final

__all__ = ["AttributeSpec", "attach_attributes", "decode_attribute"]

_ATTRIBUTES_KEY: Final[str] = "attributes"
"""The flat key this module writes and ``Session._to_attributes`` reads."""


@dataclass(frozen=True)
class AttributeSpec:
    """How to decode one attribute from one producer.

    ``index_to_label`` exists only for the ``predictor_output`` shape and for a producer that
    hands back a bare class index instead of a label. It is consulted with **both** an int and
    a str key: a JSON-delivered mapping carries ``"817"`` and an in-code default carries
    ``817``, and trying only one silently misses every mapping from the other source
    (``vehicle_type_classification.py:78-80``).
    """

    name: str
    """The attribute's name on the detection, e.g. ``"vehicle_type"``."""

    head: str | None = None
    """The key inside ``heads`` to read, defaulting to :attr:`name`."""

    index_to_label: Mapping[int | str, str] = field(default_factory=dict)
    """Class index -> label, for shape 4 and for bare-index labels."""

    numeric: bool = False
    """True for a numeric attribute (``age``): the decoded value is kept as a number in the
    label slot's string form and banded by ``attribute_band`` rather than counted by value.
    """


def attach_attributes(raw: Any, specs: Sequence[AttributeSpec]) -> Any:
    """Decode every spec onto each detection in ``raw``, in place, and return it.

    Handles the same three envelopes as the legacy attach helpers
    (``vehicle_type_classification.py:144-174``): a bare list, ``{"detections": [...]}``, and
    a ``frame_id -> list`` mapping. A detection that carries nothing decodable is left without
    the key -- **never** given an ``"unknown"`` placeholder, because "the classifier said
    nothing" and "the classifier said unknown" are different facts and only the first one is a
    chain outage.
    """
    for det in _iter_detections(raw):
        decoded = {
            spec.name: ref for spec in specs if (ref := decode_attribute(det, spec)) is not None
        }
        if decoded:
            det[_ATTRIBUTES_KEY] = {
                name: {"label": ref[0], "confidence": ref[1]} for name, ref in decoded.items()
            }
    return raw


def decode_attribute(det: Mapping[str, Any], spec: AttributeSpec) -> tuple[str, float] | None:
    """One detection, one spec -> ``(label, confidence)`` or ``None``.

    Shapes tried in this order, matching legacy:

    1. ``heads[spec.head or spec.name]`` -> ``{label, confidence}``, else its ``top_k``;
    2. flat ``label`` + ``class_confidence``;
    3. flat ``top_k``;
    4. raw ``predictor_output`` logits + :attr:`AttributeSpec.index_to_label`.

    Returns ``None`` when nothing resolves, **including** when a bare class index does not
    resolve through ``index_to_label`` -- legacy drops that case rather than publishing the
    index as a label (``vehicle_type_classification.py:121-131``), and a dashboard legend
    reading ``817`` is worse than a missing row.
    """
    heads = det.get("heads")
    if isinstance(heads, Mapping):
        head = heads.get(spec.head or spec.name)
        if isinstance(head, Mapping):
            resolved = _label_and_confidence(head, spec)
            if resolved is not None:
                return resolved

    resolved = _label_and_confidence(det, spec)
    if resolved is not None:
        return resolved

    logits = det.get("predictor_output")
    if isinstance(logits, Sequence) and not isinstance(logits, (str, bytes)) and logits:
        return _from_logits([float(v) for v in logits], spec)
    return None


def _label_and_confidence(src: Mapping[str, Any], spec: AttributeSpec) -> tuple[str, float] | None:
    """``{label, confidence}``, then ``{label, class_confidence}``, then the ``top_k`` winner."""
    label = src.get("label")
    conf = src.get("confidence", src.get("class_confidence"))
    if not _usable(label):
        win = _winning_top_k(src.get("top_k"))
        if win is None:
            return None
        label, conf = win.get("label"), win.get("confidence")
    if not _usable(label):
        return None
    resolved = _resolve_label(label, spec)
    if resolved is None:
        return None
    return resolved, _as_confidence(conf)


def _winning_top_k(top_k: Any) -> Mapping[str, Any] | None:
    """The highest-confidence entry of a ``top_k`` list, or ``None``.

    The one copy of a function that exists four times in ``post_processing/usecases``. A
    missing ``confidence`` reads ``0.0`` rather than being skipped, so a top_k list whose
    entries carry only labels still yields its first entry rather than nothing.
    """
    if not isinstance(top_k, Sequence) or isinstance(top_k, (str, bytes)):
        return None
    best: Mapping[str, Any] | None = None
    best_conf = -1.0
    for entry in top_k:
        if not isinstance(entry, Mapping) or "label" not in entry:
            continue
        conf = _as_confidence(entry.get("confidence"))
        if conf > best_conf:
            best, best_conf = entry, conf
    return best


def _from_logits(logits: Sequence[float], spec: AttributeSpec) -> tuple[str, float] | None:
    """Argmax + softmax over a raw logit vector (shape 4).

    ``math.exp`` over a shifted vector rather than the raw one: legacy
    (``vehicle_type_classification.py:83-85``) exponentiates the raw logits, which overflows
    to ``inf`` for a vector with a large positive component and then publishes ``nan`` for the
    confidence -- an F1 violation, a non-finite value that kills the whole aggregation window
    (companion doc §8.4/§18). Subtracting the max is the standard fix and changes no result.
    """
    best_idx = max(range(len(logits)), key=logits.__getitem__)
    label = _resolve_index(best_idx, spec)
    if label is None:
        return None
    peak = logits[best_idx]
    exp_vals = [math.exp(v - peak) for v in logits]
    total = sum(exp_vals)
    return label, (exp_vals[best_idx] / total) if total > 0.0 else 0.0


def _resolve_label(label: Any, spec: AttributeSpec) -> str | None:
    """A producer label -> a real label, mapping a bare index through ``index_to_label``."""
    if isinstance(label, (int, float)) and not isinstance(label, bool):
        return _resolve_index(int(label), spec)
    text = str(label).strip()
    if spec.numeric:
        return text if _is_number(text) else None
    if text.lstrip("-").isdigit():
        return _resolve_index(int(text), spec)
    return _normalize_label(text)


def _resolve_index(index: int, spec: AttributeSpec) -> str | None:
    """``index_to_label`` with **both** key types tried (``:78-80``)."""
    label = spec.index_to_label.get(index) or spec.index_to_label.get(str(index))
    return _normalize_label(label) if label else None


def _normalize_label(text: str) -> str | None:
    """An identifier-safe spelling of a decoded (non-numeric) label, or ``None`` if nothing
    identifier-safe is left.

    ``metrics[].source``'s shape validator (``engine/manifest/models.py``
    ``MetricSpec._check_source_shape``) rejects any whitespace outright, so a multi-word
    producer label (e.g. the real ``vehicle_type_index_to_category`` entry ``"fire engine"``)
    could be counted by ``attribute_count`` but never addressed as a named dashboard metric --
    found while validating a real ``vehicle_type_classification`` app.yaml against the real
    loader, not assumed from ``classification-primitives.md`` §7's example (which only
    flagged this for ``derived[].expr``, not ``metrics[].source``).

    Runs of anything outside ``[A-Za-z0-9_]`` collapse to one underscore; leading/trailing
    underscores are stripped, so ``"fire engine"`` -> ``"fire_engine"`` and
    ``"bicycle-built-for-two"`` -> ``"bicycle_built_for_two"``. A label that normalizes to
    nothing (all punctuation) is dropped as unusable rather than published unnormalized --
    falling back to the raw spelling here would silently reintroduce the same gap for that
    one case.
    """
    normalized = re.sub(r"[^A-Za-z0-9_]+", "_", text).strip("_")
    return normalized or None


def _usable(label: Any) -> bool:
    """Whether ``label`` is worth trying to resolve at all."""
    if label is None:
        return False
    if isinstance(label, str):
        return bool(label.strip())
    return isinstance(label, (int, float)) and not isinstance(label, bool)


def _as_confidence(value: Any) -> float:
    """Read a confidence-shaped value as a float 0-1-ish, treating anything unusable as
    ``0.0`` -- the conservative reading (:class:`~matrice_analytics.engine.primitives.base.
    AttributeRef`'s own docstring: an absent confidence must never pass a ``min_confidence``
    gate)."""
    if isinstance(value, bool):
        return float(int(value))
    if isinstance(value, (int, float)):
        return float(value)
    return 0.0


def _is_number(text: str) -> bool:
    """Whether ``text`` parses as a float, for :attr:`AttributeSpec.numeric`."""
    try:
        float(text)
    except ValueError:
        return False
    return True


def _iter_detections(raw: Any) -> Iterator[dict[str, Any]]:
    """Walk the same three envelopes
    ``vehicle_type_classification._attach_vehicle_type_attributes`` does (``:155-174``),
    yielding each mutable detection dict found so the caller can decode onto it in place.

    * ``{"detections": [...]}`` -- the wrapped form;
    * a bare list -- detections directly;
    * a ``frame_id -> list | dict`` mapping -- the per-frame form used when a producer batches
      several frames' detections in one payload.

    Anything that is not a ``dict`` entry is skipped rather than raised on: a malformed entry
    here is the producer's problem, not intake's, and ``decode_attribute`` already treats "no
    usable field" as an honest ``None``.
    """
    if isinstance(raw, Mapping) and isinstance(raw.get("detections"), list):
        for det in raw["detections"]:
            if isinstance(det, dict):
                yield det
        return
    if isinstance(raw, list):
        for det in raw:
            if isinstance(det, dict):
                yield det
        return
    if isinstance(raw, Mapping):
        for value in raw.values():
            if isinstance(value, list):
                for det in value:
                    if isinstance(det, dict):
                        yield det
            elif isinstance(value, dict):
                yield value
