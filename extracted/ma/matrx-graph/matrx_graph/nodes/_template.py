"""Shared ``$item`` / ``$in`` template substitution for list-shaping nodes.

One audit surface for the placeholder mini-language used by ``control.map``
(per-dispatch payload shaping), ``data.map_template`` (list reshaping), and
``text.render_list`` (list → text rendering):

* ``"$item"`` — the whole current list element.
* ``"$item.<dot.path>"`` — a path into the element (digit segments index lists).
* ``"$item.<path>.{<sibling>}"`` — an INDIRECT segment: ``{sibling}`` is
  resolved against the same root and its value becomes the segment, so
  ``"$item.choices.{correct_index}"`` picks the choice the element points at.
* ``{$item.<path>}`` as an indirect segment — a value inside the element names the
  segment (``"$in.jobs.{$item.item_index}.id"``).
* ``{$index}`` / ``{$item}`` as an indirect segment — the element's position, or
  the (scalar) element itself: ``"$in.saved.{$index}.id"`` reads the SAME
  position of a second list, so two index-aligned lists (pages and the records
  written for them) zip without a join node; ``"$in.jobs.{$item}"`` follows an
  element that IS a position into another list.
* ``"$in"`` / ``"$in.<dot.path>"`` — the hosting node's OTHER inputs (everything
  delivered on its edges besides the list itself), so constants and upstream
  values can be attached to every produced element without a join node.
* ``"$index"`` — the element's 0-based position in the list (an int).
* ``{"$cycle": [a, b, c]}`` — ROUND-ROBIN a literal pool across the fan-out:
  element i gets ``pool[i % len(pool)]``. The one operation position-aware
  templating actually needs and no dot-path can reach, because the pool is
  written in the template rather than living in the data. Pool entries are
  themselves substituted, so ``{"$cycle": ["$item.a", "fixed"]}`` works.
  Written for per-item **Mandate rotation** across a work-queue fan-out
  (W7's five image Mandates), where one mandate for every render means every
  image bursts at the same provider.

* ``{"$optional": "<ref>", "default": <value>}`` — the ONE way to say a field may be
  absent: the ref resolves as usual, and when its path does not resolve the element
  gets ``default`` (``null`` when omitted) instead of failing the step. Written for
  kinds whose items carry a field only sometimes (a quiz's ``options`` exist on a
  multiple-choice question, not on a short-answer one). The absence is declared in
  the template, never inferred: a plain ref still fails loudly.

* ``{"$format": "/decks/{in.saved.deck.0.id}?card={item.id}"}`` — one TEXT built from
  values: each ``{item.<path>}`` / ``{in.<path>}`` / ``{index}`` placeholder is replaced
  by that value (a non-text value as JSON). A placeholder whose path is missing or null
  FAILS like any ref (``TemplatePathMissing``, so ``$optional`` around it works) — a link
  to ``/decks/`` is worse than no link. ``"optional": true`` renders a missing value as
  empty text instead (display text that may lack a part); ``"encode": "url"``
  percent-encodes each inserted value (never by default). Written for links and labels a
  record stores (a kit member's ``href``), which no ref alone can build.

* ``"$in.chunks.[chunk_id={$item}].content"`` — a SELECTOR segment: the first element of
  the list whose field equals the value (literal, or ``{$item}`` / ``{$item.path}`` /
  ``{$index}`` / ``{other.path}``); none matching is a missing path (``$optional`` works).

* ``{"$uuid5": ["order", "$in.shop_id", "$item.sku"]}`` — a STABLE ID derived from values:
  each part is substituted and the result hashed as ``uuid5(namespace, text)``. The same values
  always give the same id, so two runs filing the same thing write ONE record on that id (Save
  Records' unique key) instead of racing a find-then-add. ``namespace`` defaults to the URL
  namespace and is a LITERAL (a UUID written in the template, never a ref).
  ``"join"`` says how the parts become the text: ``"json"`` (the default) encodes them as one
  JSON list, so no two different value lists collide and ``true`` stays ``true``;
  ``"colon"`` writes ``str(value)`` joined with ``:`` (a bool as ``True``, ``["a:b", "c"]`` and
  ``["a", "b:c"]`` give the same id) — LEGACY-COMPATIBLE, only for ids that must equal ids
  older code already wrote that way (``uuid5(NAMESPACE_URL, f"{a}:{b}:{c}")``).
  A missing, null or blank (whitespace-only) part FAILS (``TemplatePathMissing``) — an id built
  from a blank collides; a list or record part is refused. Any other key is refused.

* ``{"$run": "id"}`` — the RUN's own identity, read-only: ``"id"`` (this run),
  ``"workflow_id"`` (the workflow it runs) or ``"step_id"`` (the step substituting the
  template). The same names and the same ``RUN_REF_FIELDS`` as a step input's ``$run``
  (``types/variables.py``); here it reaches templates held in a step's settings, which the
  input pass never scans. ``$format`` reads the same values as ``{run.id}``. Uses:
  PROVENANCE on saved records (``"metadata": {"run_id": {"$run": "id"}}`` — which run and
  step filed each study-kit output, news story or testimony); an IDEMPOTENCY id per run
  (``{"$uuid5": ["brand.choice", {"$run": "id"}, "$item.key"]}`` — a retried step lands on
  the same rows, a new run makes new ones); a LINK back to the run in a notification
  (``{"$format": "/workflows/{run.workflow_id}/runs/{run.id}"}``). An unknown name, or a
  caller that hands no run (a unit test, a dry run, ``control.work_seed``'s key), is REFUSED
  (``ExecutionError``, never ``TemplatePathMissing``, so neither ``$optional`` nor
  ``$format``'s ``"optional": true`` hides it), like ``$in`` with no namespace and ``$index``
  with no position: a record stamped with a null run looks stamped and is not. The one
  blank: in ``$format`` with ``"optional": true``, a KNOWN name whose value is null in this
  run (``workflow_id`` of an unsaved workflow) renders as empty text. ``{"$run": …}`` takes
  nothing beside the name — ``"default"`` or any other key is refused. A ``data.once`` step
  should not read ``$run``: in its inputs it changes the reuse key every run (never reused);
  in its settings it is outside the key (a reused result carries the FIRST run's id) —
  validation warns.

``$index`` and ``$cycle`` need a position: a caller that substitutes without
one (``index=None`` — e.g. ``control.work_seed``'s key template, which shapes a
single item at a time) raises rather than inventing 0.

A path that does not resolve raises ``ExecutionError`` (parks, recoverable) —
never a silent None.
"""

from __future__ import annotations

import json
import re
from typing import Any
from urllib.parse import quote
from uuid import NAMESPACE_URL, UUID, uuid5

from matrx_graph.errors import ExecutionError
from matrx_graph.types.variables import RUN_REF_FIELDS, RUN_REF_KEY, is_run_ref


class TemplatePathMissing(ExecutionError):
    """A template path names data that is not there. The ONLY failure ``$optional`` absorbs:
    a misspelled operator, a bad ``$cycle`` or any other wiring error still raises."""

_PLACEHOLDER = re.compile(r"\{([A-Za-z0-9_.]+)(?::(n|count|join))?\}")
#: ``{#path}…{/path}`` repeats its body for each element of the list at ``path`` (once
#: for a single value, never for a missing / null / empty one); ``{^path}…{/path}``
#: renders its body only when ``path`` is missing or empty. Mustache sections.
_SECTION = re.compile(r"\{([#^])([^{}\n]+?)\}(.*?)\{/\2\}", re.DOTALL)

_NO_ITEM = object()


def _segments(path: str) -> list[str]:
    """Split a dot-path, keeping a braced segment whole (``{$item.item_index}``)."""
    parts: list[str] = []
    depth = 0
    current = ""
    for ch in path:
        if ch == "." and depth == 0:
            parts.append(current)
            current = ""
            continue
        depth += (ch == "{") - (ch == "}")
        current += ch
    parts.append(current)
    return parts


def resolve_path(
    root: Any, path: str, *, label: str, index: int | None = None, item: Any = _NO_ITEM
) -> Any:
    val = root
    walked: list[str] = []
    for part in _segments(path):
        if len(part) > 2 and part[0] == "{" and part[-1] == "}":
            # Indirect segment: '{other_field}' resolves that field against the
            # SAME root and uses its value as this segment. Written for the
            # commonest LLM output shape there is -- a list plus a sibling index
            # into it ('choices' + 'correct_index'), which no static dot-path
            # can reach. Pure data traversal, single segment, no dots inside.
            inner = part[1:-1]
            if inner == "$index":
                if index is None:
                    raise ExecutionError(
                        f"template path '{label}.{path}' uses {{$index}} where the caller "
                        "supplies no item position."
                    )
                part = str(index)
            elif inner.startswith("$item.") and item is not _NO_ITEM:
                # A path INTO the element names the segment: '$in.jobs.{$item.item_index}'
                # reads the job a hole report points at, without a reshape step between.
                part = str(resolve_path(item, inner[len("$item."):], label="$item", index=index))
            elif inner == "$item":
                if item is _NO_ITEM or isinstance(item, (dict, list)) or item is None:
                    raise ExecutionError(
                        f"template path '{label}.{path}' uses {{$item}} but the element is "
                        f"{_describe(None if item is _NO_ITEM else item)}, not a key or position."
                    )
                part = str(item)
            else:
                part = str(resolve_path(root, inner, label=label, index=index, item=item))
        if len(part) > 2 and part[0] == "[" and part[-1] == "]" and "=" in part:
            # A SELECTOR segment: '[chunk_id={$item}]' is the first element of the list whose
            # field equals the value — a join by id, which no position or dot-path can reach.
            field, _, want = part[1:-1].partition("=")
            if len(want) > 2 and want[0] == "{" and want[-1] == "}":
                ref = want[1:-1]
                if ref == "$index" and index is not None:
                    want = str(index)
                elif ref == "$item" and item is not _NO_ITEM and not isinstance(item, (dict, list)):
                    want = str(item)
                elif ref.startswith("$item.") and item is not _NO_ITEM:
                    want = str(resolve_path(item, ref[len("$item."):], label="$item", index=index))
                else:
                    want = str(resolve_path(root, ref, label=label, index=index, item=item))
            hits = [el for el in val if isinstance(el, dict) and str(el.get(field)) == want] if isinstance(val, list) else []
            if not hits:
                raise TemplatePathMissing(
                    f"template path '{label}.{path}': no element of the list has {field} = {want!r}."
                )
            val = hits[0]
            walked.append(part)
            continue
        try:
            if isinstance(val, list):
                val = val[int(part)]
            elif isinstance(val, dict):
                val = val[part]
            else:
                raise KeyError(part)
        except (KeyError, IndexError, ValueError) as e:
            where = f" for item {index}" if index is not None else ""
            raise TemplatePathMissing(
                f"template path '{label}.{path}' does not resolve{where}: "
                f"segment '{part}' is missing or not indexable. "
                + _miss_remedy(val, part, label=label, walked=walked, index=index)
            ) from e
        walked.append(part)
    return val


#: How many of a failing container's keys the error message lists before it
#: says how many more there are.
_KEY_LIST_CAP = 25

#: Keys that hold a step result's STRUCTURED payload. When the missing segment
#: turns up inside one of these on the same object, the remedy is the nested
#: path — the ``gather_result.values`` mistake (RAW per-item results mapped
#: where ``structured_outputs`` was meant) lands here every time.
_NESTED_RESULT_KEYS: tuple[str, ...] = ("structured_output", "output", "result", "data")

#: Sibling collections a gather step offers beside ``values``, named in the
#: remedy when the failing element looks like a raw agent result.
_AGENT_RESULT_MARKERS: tuple[str, ...] = ("structured_output", "final_text", "messages")


def _describe(value: Any) -> str:
    if isinstance(value, dict):
        keys = [str(k) for k in value]
        shown = keys[:_KEY_LIST_CAP]
        more = f" (+{len(keys) - len(shown)} more)" if len(keys) > len(shown) else ""
        if not keys:
            return "an object with no keys at all"
        return f"an object with keys {shown}{more}"
    if isinstance(value, list):
        return f"a list of {len(value)} element(s) — index it with a digit segment"
    if value is None:
        return "null"
    return f"a {type(value).__name__}"


def _miss_remedy(
    value: Any,
    part: str,
    *,
    label: str,
    walked: list[str],
    index: int | None,
) -> str:
    """The remedy half of a failed template path: what IS there, and where the
    wanted field actually lives.

    Nothing fails silently and no error is a dead end: the old message said only
    "missing or not indexable", which told an author nothing about a shape they
    never saw. This one names the available keys, and when the field they asked
    for sits one level down (a raw agent result carrying it inside
    ``structured_output``) it names that exact path — the Newsroom Desk failure,
    2026-09-12.
    """
    subject = f"Item {index} is" if index is not None else "The value there is"
    parts = [f"{subject} {_describe(value)}."]
    if isinstance(value, dict):
        prefix = "".join(f"{seg}." for seg in walked)
        for key in (*_NESTED_RESULT_KEYS, *(k for k in value if k not in _NESTED_RESULT_KEYS)):
            nested = value.get(key) if key in value else None
            if isinstance(nested, dict) and part in nested:
                parts.append(
                    f"'{part}' IS present at '{label}.{prefix}{key}.{part}' — "
                    f"point the template there."
                )
                break
        if any(marker in value for marker in _AGENT_RESULT_MARKERS):
            parts.append(
                "This element is a RAW step result (it carries "
                f"{sorted(m for m in _AGENT_RESULT_MARKERS if m in value)}). A gather "
                "step offers `structured_outputs` and `final_texts` beside `values` — "
                "map the list from one of those instead of reaching into raw results."
            )
    return " ".join(parts)


def _stringify(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value
    return json.dumps(value, ensure_ascii=False, default=str)


def stable_id(parts: Any, *, namespace: Any = None, join: Any = None) -> str:
    """``$uuid5``: the id ``uuid5(namespace, text)`` — the same values always name the same
    record. ``join="json"`` (default) makes ``text`` the parts as one JSON list (collision-free);
    ``join="colon"`` makes it ``":".join(str(p))``, matching ids older code wrote with f-strings.
    ``namespace`` defaults to the URL namespace."""
    if join not in (None, "json", "colon"):
        raise ExecutionError(f"template ref '$uuid5' join must be 'json' or 'colon'; got {join!r}.")
    if not isinstance(parts, list) or not parts:
        raise ExecutionError(
            f"template ref '$uuid5' needs a non-empty list of values; got {type(parts).__name__}."
        )
    nested = [i for i, part in enumerate(parts) if isinstance(part, (list, dict))]
    if nested:
        raise ExecutionError(
            f"template ref '$uuid5': value(s) at position {nested} are a list or record — an id is "
            "built from single values; name the field inside it."
        )
    blank = [i for i, part in enumerate(parts) if part is None or not str(part).strip()]
    if blank:
        raise TemplatePathMissing(
            f"template ref '$uuid5': value(s) at position {blank} are empty — an id built from "
            "a blank would be shared by every record missing it."
        )
    try:
        space = NAMESPACE_URL if namespace in (None, "") else UUID(str(namespace))
    except ValueError:
        raise ExecutionError(f"template ref '$uuid5' namespace must be a UUID; got {namespace!r}.") from None
    if join == "colon":
        # Legacy-compatible: str() of each value joined with ':' (f"{a}:{b}"), collisions included.
        return str(uuid5(space, ":".join(str(p) for p in parts)))
    return str(uuid5(space, json.dumps(parts, ensure_ascii=False, separators=(",", ":"), default=str)))


def render_template_string(
    template: str,
    root: Any,
    *,
    whole_key: str = "item",
    max_chars: int | None = None,
    missing: str = "empty",
    encode: Any = None,
) -> tuple[str, bool]:
    """Interpolate ``{dot.path}`` placeholders in ``template`` against ``root``.

    ``{dot.path:n}`` renders a number with thousands separators (1,000) — only when asked.
    ``{dot.path:count}`` renders how many entries a list/object holds (a text's length; null is 0).
    ``{dot.path:join}`` renders a list as plain text, its entries separated by " · " (a text stays
    as written; null is empty) — the readable way to show a list in a sentence.

    ``{<whole_key>}`` inserts the whole root value. A missing path renders as
    '' — string templating stays best-effort and never parks a run. Non-string
    values are JSON-encoded. ``max_chars`` bounds each interpolated VALUE
    (appending '…'). Returns ``(text, truncated)``. ``missing="raise"`` makes a
    missing or null path raise ``TemplatePathMissing`` instead (``$format``);
    ``encode`` transforms each inserted value (``$format``'s ``"encode": "url"``).

    Shared by ``text.render_list`` (per-item rendering) and
    ``control.human_input`` (prompt / default-answer interpolation) so the
    placeholder language cannot drift between nodes.
    """
    truncated = False

    if "{#" in template or "{^" in template:
        template, truncated = _render_sections(template, root, max_chars=max_chars)

    def _sub(match: re.Match[str]) -> str:
        nonlocal truncated
        path = match.group(1)
        if path == whole_key:
            value = root
        else:
            try:
                value = resolve_path(root, path, label="{}")
            except TemplatePathMissing:
                if missing == "raise":
                    raise
                return ""
            except Exception:
                if missing == "raise":
                    raise
                return ""
            if value is None and missing == "raise":
                raise TemplatePathMissing(f"template placeholder '{{{path}}}' is null.")
        # ``{path:n}`` — the template ASKS for a person-facing number (1,000). Never by
        # default: a year or an id must render as written ("2026", never "2,026").
        if match.group(2) == "n" and isinstance(value, (int, float)) and not isinstance(value, bool):
            text = f"{value:,}"
        elif match.group(2) == "join" and isinstance(value, list):
            text = " · ".join(_stringify(v) for v in value if v not in (None, ""))
        elif match.group(2) == "count":
            # ``{path:count}`` — how many: a list's or object's entries, a text's characters;
            # null counts 0 ("some calls failed ({item.failed:count})").
            if isinstance(value, (list, dict, str)):
                text = str(len(value))
            else:
                text = "0" if value is None else _stringify(value)
        else:
            text = _stringify(value)
        if max_chars is not None and len(text) > max_chars:
            truncated = True
            text = text[:max_chars] + "…"
        return encode(text) if encode is not None else text

    return _PLACEHOLDER.sub(_sub, template), truncated


def _render_sections(template: str, root: Any, *, max_chars: int | None) -> tuple[str, bool]:
    """Expand every ``{#path}…{/path}`` / ``{^path}…{/path}`` section of ``template``.

    Inside a ``#`` section the element is the root: ``{item}`` is the element itself and
    ``{field}`` reads a field of it (``{#key_facts}- {item}\n{/key_facts}``,
    ``{#findings}- {finding}\n{/findings}``). The path is a connection source
    (``matrx_graph.paths``), so ``{#snippets[0:5]}`` takes the first five.
    """
    from matrx_graph.paths import resolve_path as resolve_source

    truncated = False

    def _section(match: re.Match[str]) -> str:
        nonlocal truncated
        mark, path, body = match.group(1), match.group(2).strip(), match.group(3)
        found, value = resolve_source(root, path)
        empty = not found or value is None or value == "" or value == [] or value == {} or value is False
        if mark == "^":
            return _render_sections(body, root, max_chars=max_chars)[0] if empty else ""
        if empty:
            return ""
        parts: list[str] = []
        for element in value if isinstance(value, list) else [value]:
            text, cut = render_template_string(body, element, whole_key="item", max_chars=max_chars)
            parts.append(text)
            truncated = truncated or cut
        return "".join(parts)

    return _SECTION.sub(_section, template), truncated


def run_facts_of(ctx: Any) -> dict[str, Any] | None:
    """The run identity a step hands its templates (``ctx.run_facts``); None for a bare call
    with no context, so every ``$run`` in the template is refused rather than guessed."""
    return getattr(ctx, "run_facts", None)


def _check_run_name(name: Any, run: dict[str, Any] | None) -> None:
    """Refuse (``ExecutionError`` — never absorbed by ``$optional``) an unknown ``$run`` name,
    or any ``$run`` where the caller hands no run."""
    if name not in RUN_REF_FIELDS:
        raise ExecutionError(
            f"template ref '$run': {name!r} is not something a run offers. "
            f"Use one of: {sorted(RUN_REF_FIELDS)}."
        )
    if run is None:
        raise ExecutionError(
            f"template ref '$run': '{name}' used but no run is available here — this template "
            "is filled without the run (a dry run, a bare call, control.work_seed's key, a "
            f"template that arrived on a connection). Write it as a step input instead "
            f"({{\"$run\": \"{name}\"}} in the step's inputs), which the scheduler fills before "
            "the step runs."
        )


def _run_fact(name: str, run: dict[str, Any] | None) -> str:
    _check_run_name(name, run)
    value = (run or {}).get(name)
    if not value:
        raise ExecutionError(
            f"template ref '$run': '{name}' has no value in this run (a run of an unsaved "
            "workflow has no workflow_id) — a record stamped with a blank looks stamped and is not."
        )
    return str(value)


def substitute_template(
    template: Any,
    item: Any,
    *,
    index: int | None = None,
    extra: dict[str, Any] | None = None,
    run: dict[str, Any] | None = None,
) -> Any:
    """Recursively substitute ``$item`` / ``$in`` / ``$run`` refs inside ``template``.

    ``extra`` is the ``$in`` namespace (the hosting node's other inputs);
    when it is None, ``$in`` refs raise. ``run`` is the run's identity
    (``ctx.run_facts``); when it is None, ``$run`` refs raise.
    """
    if isinstance(template, str):
        if template == "$item":
            return item
        if template == "$index":
            if index is None:
                raise ExecutionError(
                    "template ref '$index' used where the caller supplies no item "
                    "position — it is only available in per-element templates."
                )
            return index
        if template.startswith("$item."):
            return resolve_path(
                item, template[len("$item.") :], label="$item", index=index, item=item
            )
        if template == "$in":
            if extra is None:
                raise ExecutionError("template ref '$in' used but no input namespace is available.")
            return extra
        if template.startswith("$in."):
            if extra is None:
                raise ExecutionError(
                    f"template ref '{template}' used but no input namespace is available."
                )
            return resolve_path(
                extra, template[len("$in.") :], label="$in", index=index, item=item
            )
        return template
    if isinstance(template, dict):
        if is_run_ref(template):
            return _run_fact(template[RUN_REF_KEY], run)
        if RUN_REF_KEY in template:
            raise ExecutionError(
                "template ref '$run' is written alone, a name and nothing beside it: "
                f'{{"$run": "id"}}. Got keys {sorted(template)} — a default for the run\'s own '
                "identity would stamp records with a made-up run, so there is none."
            )
        if "$optional" in template and set(template) <= {"$optional", "default"}:
            try:
                return substitute_template(template["$optional"], item, index=index, extra=extra, run=run)
            except TemplatePathMissing:
                return substitute_template(template.get("default"), item, index=index, extra=extra, run=run)
        if "$format" in template and set(template) <= {"$format", "optional", "encode"}:
            text = template["$format"]
            if not isinstance(text, str):
                raise ExecutionError(
                    f"template ref '$format' needs a text with {{...}} placeholders; got {type(text).__name__}."
                )
            encoding = template.get("encode")
            if encoding not in (None, "url"):
                raise ExecutionError(f"template ref '$format' encode must be 'url'; got {encoding!r}.")
            # A {run.<name>} placeholder is checked BEFORE rendering: an unknown name or no run
            # is a refusal neither "optional" nor $optional absorbs (same as the bare $run form);
            # only a KNOWN name whose value is null (workflow_id of an unsaved workflow) is a
            # missing value — blank under "optional": true.
            for placeholder in _PLACEHOLDER.finditer(text):
                path = placeholder.group(1)
                if path == "run" or path.startswith("run."):
                    _check_run_name(path[len("run.") :].split(".", 1)[0], run)
            root: dict[str, Any] = {"item": None if item is _NO_ITEM else item, "in": extra or {}}
            if index is not None:
                root["index"] = index
            if run is not None:
                root["run"] = {k: v for k, v in run.items() if k in RUN_REF_FIELDS and v}
            try:
                return render_template_string(
                    text,
                    root,
                    whole_key="\x00",
                    missing="empty" if template.get("optional") is True else "raise",
                    encode=(lambda v: quote(v, safe="")) if encoding == "url" else None,
                )[0]
            except TemplatePathMissing as e:
                raise TemplatePathMissing(
                    f"template ref '$format' {text!r}: {e} Mark it \"optional\": true when a missing "
                    "value may render as empty text."
                ) from e
        if "$uuid5" in template:
            extra_keys = sorted(set(template) - {"$uuid5", "namespace", "join"})
            if extra_keys:
                raise ExecutionError(
                    f"template ref '$uuid5' takes only 'namespace' and 'join' beside it; got {extra_keys}."
                )
            return stable_id(
                substitute_template(template["$uuid5"], item, index=index, extra=extra, run=run),
                namespace=template.get("namespace"),
                join=template.get("join"),
            )
        if len(template) == 1 and "$cycle" in template:
            pool = template["$cycle"]
            if not isinstance(pool, list) or not pool:
                raise ExecutionError(
                    "template ref '$cycle' needs a non-empty list to rotate; "
                    f"got {type(pool).__name__}."
                )
            if index is None:
                raise ExecutionError(
                    "template ref '$cycle' used where the caller supplies no item "
                    "position — it is only available in per-element templates."
                )
            return substitute_template(pool[index % len(pool)], item, index=index, extra=extra, run=run)
        return {
            k: substitute_template(v, item, index=index, extra=extra, run=run) for k, v in template.items()
        }
    if isinstance(template, list):
        return [substitute_template(v, item, index=index, extra=extra, run=run) for v in template]
    return template


#: A ``$in.<name>`` (or ``{in.<name>}`` inside a ``$format``) reference; group 1 is the top-level name.
_IN_REFERENCE = re.compile(r"(?:\$in\.|\{in\.)([A-Za-z_][A-Za-z0-9_]*)")

#: The class attribute an OPEN input model (``extra="allow"``) sets to say its extras are only
#: the values some of its own fields read by name: ``IN_READ_FIELDS = ("match",)`` means "an
#: extra input is one ``match`` reads as ``$in.<name>``" (Find Records). An open model without
#: it reads ANY extra (a transform's ``inputs['audience']``).
IN_READ_FIELDS = "in_read_fields"


def in_names_read(template: Any) -> set[str] | None:
    """The top-level ``$in`` names a template reads; None when it reads the whole ``$in``."""
    text = json.dumps(template, default=str)
    if '"$in"' in text:
        return None
    return set(_IN_REFERENCE.findall(text))


def extras_read(schema: Any, values: Any) -> set[str] | None:
    """The extra (undeclared-field) input names a step's input model reads, given its authored
    values. ``set()`` for a closed model; the names its ``IN_READ_FIELDS`` read as ``$in.<name>``
    for a model that declares them; None (any name) for an open model that does not say, or a
    declared field that reads the whole ``$in``. THE ONE RULE both the scheduler (which run
    inputs an entry step is handed) and the model's own typo refusal use."""
    config = getattr(schema, "model_config", None) or {}
    if config.get("extra") != "allow":
        return set()
    fields = getattr(schema, IN_READ_FIELDS, None)
    if not fields:
        return None
    values = values if isinstance(values, dict) else {}
    read: set[str] = set()
    for field in fields:
        names = in_names_read(values.get(field))
        if names is None:
            return None
        read |= names
    return read
