from __future__ import annotations

import ast
import functools
import re
import unicodedata
from collections.abc import Iterator
from typing import Any

from matrx_graph.errors import ExecutionError

# SECURITY — do NOT add ast.Attribute here, and do NOT expose builtins
# wholesale. This sandbox is secure *by construction*: with no attribute
# nodes there is no runtime-traversal primitive, so an author cannot reach
# __class__/__globals__/__subclasses__ to escape. In particular the classic
# str.format info-disclosure escape — e.g.
# "'{0.__class__.__init__.__globals__[...]}'.format(inputs)" — cannot even be
# SPELLED, because `.format` is attribute access (the format mini-language
# does getattr itself at RUNTIME, which is why an AST-level `_`-prefix check
# is not enough and why Attribute stays banned outright; a broadening that
# allowed it was reverted once already).
#
# Calls are the EXPLICIT SAFE-HELPER PRIMITIVE that comment always promised:
# `ast.Call` is admitted, but the walker below only accepts a call whose
# function is a BARE NAME in `_SAFE_HELPERS` — a frozen table of pure,
# non-traversing builtins (`len(inputs['x'])`, `min(a, b)`). No method calls
# (they'd need Attribute), no keywords, no unpacking, no user-reachable
# callables (`inputs['f'](…)` has a Subscript func and is rejected). Guards:
# test_human_input_sandbox_rejects_function_calls +
# test_sandbox_safe_helpers. Added 2026-08-17 because the podcast challenger
# workflows (W1's GATE 1 `len(...) >= 1000` floor, W2's keep-best guards,
# W4's prompt-list caps) need real length/number work at run time — W1 was
# seeded with `len(...)` in its gate and every run would have died on it.
def _coalesce(*values: Any) -> Any:
    """The first value that is not empty (None, "", a whitespace-only string, [], {}).

    When every value is empty, the LAST argument is the default and comes back as
    written — ``coalesce(x, '')`` is ``''`` and ``coalesce(x, [])`` is ``[]``, so the
    caller's fallback is never replaced by None (2026-10-28; it was None, and the
    CONVERSION-PLAYBOOK recorded the crash five times). With ONE argument there is no
    default: ``coalesce(x)`` is None when ``x`` is empty — live workflows use
    ``coalesce(x) is not None`` as "x has a value".

    0 and False ARE values — only absence counts as empty. Added 2026-10-26 for
    ``data.rules`` decision tables ("the name, else the title, else the url").
    """
    for value in values:
        if value is None or (isinstance(value, str) and not value.strip()) or (
                isinstance(value, (list, dict, tuple)) and len(value) == 0):
            continue
        return value
    return values[-1] if len(values) > 1 else None


def _text_arg(name: str, value: Any) -> str | None:
    if value is None or isinstance(value, str):
        return value
    raise ExecutionError(f"{name}() needs text, got a {type(value).__name__}.")


def _text_or_texts(name: str, value: Any, fn: Any) -> str | list[str] | None:
    """Apply ``fn`` to one text, or to every text in a list (a list in gives a list out).

    None stays None; a None ITEM in a list stays None. Any other item is refused with a
    sentence naming the helper and the position."""
    if isinstance(value, list | tuple):
        out: list[Any] = []
        for i, item in enumerate(value):
            if item is not None and not isinstance(item, str):
                raise ExecutionError(
                    f"{name}() needs text or a list of texts; item {i} is a {type(item).__name__}."
                )
            out.append(None if item is None else fn(item))
        return out
    text = _text_arg(name, value)
    return None if text is None else fn(text)


def _lower(value: Any) -> str | list[str] | None:
    """Lower case — one text, or each text in a list; None stays None. Added 2026-10-27 (generic-only gap)."""
    return _text_or_texts("lower", value, str.lower)


def _casefold(value: Any) -> str | list[str] | None:
    """The stronger case fold ("Straße" -> "strasse") — one text or each in a list; None stays None."""
    return _text_or_texts("casefold", value, str.casefold)


def _nfkc(value: Any) -> str | list[str] | None:
    """Unicode NFKC: compatibility forms become their plain letters (full-width "Ｃａｆé" -> "Café",
    the "ﬁ" ligature -> "fi", "①" -> "1"). Case and spacing are untouched. One text or a list."""
    return _text_or_texts("nfkc", value, lambda text: unicodedata.normalize("NFKC", text))


def _everyday_words(value: Any) -> list[str]:
    """The texts of a list that are also an everyday word — one alphabetic token that is an English
    word ("Atoms", "Render", "Stream"), each once, in order; None and empty items are skipped. The same
    test ``text.term_scan``'s ``everyday_words: auto`` uses, so a never-say list can mark the names that
    must match only as a proper name. Added 2026-10-28 (AI-visibility V5: competitors found in text)."""
    from matrx_utils.proper_names import everyday_word_terms

    items = [v for v in _scalar_list("everyday_words", value) if v is not None and str(v).strip()]
    return everyday_word_terms(items)


def _collapse_spaces(value: Any) -> str | list[str] | None:
    """Every run of whitespace becomes one space, ends trimmed ("  a \n b " -> "a b"). One text or a list."""
    return _text_or_texts("collapse_spaces", value, lambda text: " ".join(text.split()))


def _affix(name: str, value: Any, affix: Any) -> bool:
    text = _text_arg(name, value)
    if text is None:
        return False
    options = tuple(affix) if isinstance(affix, list | tuple) else (affix,)
    if not all(isinstance(o, str) for o in options):
        raise ExecutionError(f"{name}() compares with text or a list of texts.")
    return text.startswith(options) if name == "startswith" else text.endswith(options)


def _startswith(value: Any, prefix: Any) -> bool:
    """True when the text starts with the prefix (or any of a list); None is never a match."""
    return _affix("startswith", value, prefix)


def _url_path(value: Any) -> str | None:
    """The path of a web address, no query string or fragment ("https://a.com/x/y?q=1" -> "/x/y";
    "https://a.com" -> "/"). None stays None; text that is no address gives "". Added 2026-10-27 with
    ``url_depth`` and ``matches``: pages kinded by their path words (Choose pages to read), links grouped by
    section (a site map), redirects compared path to path (a migration check).

    Only text with a scheme ("https://…") or a leading "//" is read as an address with a host. Any other
    text is a PATH: "about/team" -> "/about/team" (depth 2), "/x?q=1" -> "/x". A bare "example.com/x" is
    therefore the path "/example.com/x" - write "https://example.com/x" for an address."""
    from urllib.parse import urlsplit

    text = _text_arg("url_path", value)
    if text is None:
        return None
    text = text.strip()
    if not text:
        return ""
    try:
        if "://" in text or text.startswith("//"):
            return urlsplit(text).path or "/"
        return urlsplit(text if text.startswith("/") else f"/{text}").path or "/"
    except ValueError:
        return ""


def _url_depth(value: Any) -> int | None:
    """How many path segments a web address (or a path) has: "https://a.com/" -> 0, "/x/y/" -> 2."""
    path = _url_path(value)
    if path is None:
        return None
    return len([part for part in path.split("/") if part])


def _matches(value: Any, pattern: Any, ignore_case: Any = False) -> bool:
    """True when the text contains a match of the regular expression (checked by the platform's safe-pattern
    rules; ``ignore_case`` True ignores case). None is never a match."""
    text = _text_arg("matches", value)
    if text is None:
        return False
    if not isinstance(pattern, str) or not pattern:
        raise ExecutionError("matches() takes a non-empty pattern text.")
    return _compiled(pattern, bool(ignore_case), "matches").search(text) is not None


@functools.lru_cache(maxsize=256)
def _compiled(pattern: str, ignore_case: bool, name: str) -> re.Pattern[str]:
    """The safe-compiled pattern; a refusal names the function the author called (``name``)."""
    from matrx_graph.safe_regex import UnsafePatternError, compile_safe

    try:
        return compile_safe(pattern, ignore_case=ignore_case)
    except UnsafePatternError as exc:
        raise ExecutionError(f"{name}(): {exc}") from exc


def _max_parts(name: str, value: Any) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise ExecutionError(f"{name}() takes a whole number of splits (-1 = all).")
    return value


def _split(value: Any, sep: Any, max_splits: Any = -1) -> list[str]:
    """The text cut at every ``sep`` (``split('a, b, c', ', ')`` -> ["a", "b", "c"]); the third argument caps
    the cuts (``split('k=v=w', '=', 1)`` -> ["k", "v=w"], -1 = all). None gives []. Added 2026-10-28 (no
    method calls in expressions, so "the parts of this text" needed a step of its own). Users: a "City, ST"
    field into city and state; a breadcrumb "Home > Shop > Shoes" into its levels; a "key=value" tag."""
    text = _text_arg("split", value)
    if not isinstance(sep, str) or not sep:
        raise ExecutionError("split() takes a non-empty separator text.")
    return [] if text is None else text.split(sep, _max_parts("split", max_splits))


def _replace(value: Any, old: Any, new: Any) -> str | list[str] | None:
    """Every ``old`` in the text becomes ``new`` (``replace('a-b-c', '-', ' ')`` -> "a b c"); one text or each
    text in a list; None stays None. Users: a slug back into words; "&amp;" left in scraped text into "&";
    a phone number's dashes removed before comparing."""
    if not isinstance(old, str) or not old or not isinstance(new, str):
        raise ExecutionError("replace() takes a non-empty text to find and a replacement text.")
    return _text_or_texts("replace", value, lambda text: text.replace(old, new))


def _before(value: Any, sep: Any) -> str | None:
    """The text before the FIRST ``sep``, or the whole text when ``sep`` is absent (``before('jo@x.com', '@')``
    -> "jo"). None stays None. Users: a name before " - " in a page title; an email's local part; a product
    name before " | " in a listing."""
    text = _text_arg("before", value)
    if not isinstance(sep, str) or not sep:
        raise ExecutionError("before() takes a non-empty separator text.")
    return None if text is None else text.split(sep, 1)[0]


def _after(value: Any, sep: Any) -> str | None:
    """The text after the FIRST ``sep``, or "" when ``sep`` is absent (``after('jo@x.com', '@')`` -> "x.com").
    None stays None. Users: an email's domain; the value of "Size: XL"; the site name after " | " in a title."""
    text = _text_arg("after", value)
    if not isinstance(sep, str) or not sep:
        raise ExecutionError("after() takes a non-empty separator text.")
    if text is None:
        return None
    _head, found, tail = text.partition(sep)
    return tail if found else ""


def _regex_split(value: Any, pattern: Any, max_splits: Any = -1) -> list[str]:
    """The text cut at every match of a regular expression (safe-pattern rules, as ``matches``):
    ``regex_split('a, b;c', '[,;] *')`` -> ["a", "b", "c"]; the third argument caps the cuts (-1 = all).
    None gives []. A pattern with a ``( )`` group ALSO returns each captured separator between the parts
    (``regex_split('a1b2c', '([0-9])')`` -> ["a", "1", "b", "2", "c"]); write ``(?: )`` to group without
    keeping it. Users: a tag list typed with mixed commas and semicolons; an address on mixed line
    breaks; sentences cut at ". " / "! " / "? "."""
    text = _text_arg("regex_split", value)
    if not isinstance(pattern, str) or not pattern:
        raise ExecutionError("regex_split() takes a non-empty pattern text.")
    if text is None:
        return []
    cap = _max_parts("regex_split", max_splits)
    if cap == 0:
        return [text]
    return _compiled(pattern, False, "regex_split").split(text, maxsplit=0 if cap < 0 else cap)


def _regex_replace(value: Any, pattern: Any, new: Any) -> str | list[str] | None:
    """Every match of a regular expression (safe-pattern rules) becomes ``new`` — taken literally, never a
    group reference (``regex_replace('a  b\tc', '\\s+', ' ')`` -> "a b c"). One text or each text in a list;
    None stays None. Users: phone digits only ('[^0-9]' -> ''); tracking parameters cut from links; runs
    of spaces in scraped text collapsed."""
    if not isinstance(pattern, str) or not pattern or not isinstance(new, str):
        raise ExecutionError("regex_replace() takes a non-empty pattern text and a replacement text.")
    compiled = _compiled(pattern, False, "regex_replace")
    return _text_or_texts("regex_replace", value, lambda text: compiled.sub(lambda _m: new, text))


def _url_host(value: Any) -> str | None:
    """The host of a web address, lower case, without ``www.`` ("https://www.Example.com/a?b" -> "example.com";
    "example.com/shop" -> "example.com"). None stays None; text that is no address gives "". Added 2026-10-27
    (generic-only gap: "the host of this link" could not be read, so a weak name could not be anchored by the
    person's own outbound link)."""
    from urllib.parse import urlsplit

    text = _text_arg("url_host", value)
    if text is None:
        return None
    text = text.strip()
    if not text:
        return ""
    try:
        host = urlsplit(text if "://" in text else f"https://{text}").hostname or ""
    except ValueError:
        return ""
    host = host.lower()
    return host[4:] if host.startswith("www.") else host


def _on_site(value: Any, sites: Any) -> bool:
    """True when the address or host is one of the sites, or a subdomain of one ("shop.patagonia.com" is on
    "patagonia.com"; "notpatagonia.com" is not). Both sides read through ``url_host`` (lower case, ``www.``
    dropped); ``sites`` is text or a list of texts; None is never a match. Added 2026-10-27 (generic-only gap:
    "the host is the target or ends with .target" needed a second list of dotted targets)."""
    host = _url_host(value)
    if not host:
        return False
    options = list(sites) if isinstance(sites, list | tuple) else [sites]
    if not all(isinstance(o, str) or o is None for o in options):
        raise ExecutionError("on_site() compares with a site or a list of sites.")
    for option in options:
        site = _url_host(option)
        if site and (host == site or host.endswith("." + site)):
            return True
    return False


def _endswith(value: Any, suffix: Any) -> bool:
    """True when the text ends with the suffix (or any of a list); None is never a match."""
    return _affix("endswith", value, suffix)


def _scalar_list(name: str, value: Any) -> list[Any]:
    if value is None:
        return []
    if not isinstance(value, list | tuple):
        raise ExecutionError(f"{name}() compares two lists; got a {type(value).__name__}.")
    if any(isinstance(v, dict | list | tuple) for v in value):
        raise ExecutionError(
            f"{name}() compares lists of plain values (ids, names, numbers), not records. "
            "Pick the field first upstream (e.g. a data.map_template) and compare those."
        )
    return list(value)


def _intersection(a: Any, b: Any) -> list[Any]:
    """Items of ``a`` that are also in ``b``, in ``a``'s order. None reads as []. 2026-10-27."""
    left, right = _scalar_list("intersection", a), set(_scalar_list("intersection", b))
    return [v for v in left if v in right]


def _difference(a: Any, b: Any) -> list[Any]:
    """Items of ``a`` that are not in ``b``, in ``a``'s order. None reads as []."""
    left, right = _scalar_list("difference", a), set(_scalar_list("difference", b))
    return [v for v in left if v not in right]


def _contains_any(a: Any, b: Any) -> bool:
    """True when any item of ``a`` is in ``b``."""
    right = set(_scalar_list("contains_any", b))
    return any(v in right for v in _scalar_list("contains_any", a))


def _contains_all(a: Any, b: Any) -> bool:
    """True when every item of ``a`` is in ``b`` (an empty ``a`` is)."""
    right = set(_scalar_list("contains_all", b))
    return all(v in right for v in _scalar_list("contains_all", a))


def _join(separator: Any, items: Any) -> str:
    """The texts joined by ``separator`` (``join(', ', ['a', None, 'b'])`` -> "a, b"); a None item is
    skipped, any other non-text item is refused with its position. Added 2026-10-27 with list loops
    (PRIMITIVES-LIST-EXPRESSIONS.md)."""
    sep = _text_arg("join", separator) or ""
    parts: list[str] = []
    for i, item in enumerate(items if items is not None else []):
        if item is None:
            continue
        if not isinstance(item, str):
            raise ExecutionError(f"join() needs texts; item {i} is a {type(item).__name__}.")
        parts.append(item)
    return sep.join(parts)


def _get(value: Any, path: Any, default: Any = None) -> Any:
    """The field at ``path`` (dot-separated keys; a whole-number part indexes a list), or ``default``
    when any part is missing or the value there is None (``get(p, 'title', '')``). "" / 0 / False ARE
    values. Added 2026-10-27 for the `x['k'] if 'k' in x and x['k'] else d` guard
    (PRIMITIVES-LIST-EXPRESSIONS.md § get)."""
    if not isinstance(path, str) or not path:
        raise ExecutionError("get() needs a text path, like get(inputs, 'page.title', '').")
    for part in path.split("."):
        if isinstance(value, dict) and part in value:
            value = value[part]
        elif isinstance(value, list | tuple) and part.isascii() and part.isdigit() and int(part) < len(value):
            value = value[int(part)]
        else:
            return default
    return default if value is None else value


def _loop_source(name: str, value: Any) -> list[Any] | tuple[Any, ...] | dict[Any, Any] | set[Any]:
    """What a loop or ``enumerate``/``zip`` may go over: a list, tuple, set, or a dict (its keys).
    Text is refused: looping over its characters is never what a workflow means."""
    if isinstance(value, list | tuple | dict | set | frozenset):
        return value
    what = "text" if isinstance(value, str) else type(value).__name__
    raise ExecutionError(f"{name}: can only loop over a list (or a dict's keys); got {what}.")


def _enumerate(items: Any) -> list[list[Any]]:
    """``[[0, a], [1, b], …]`` — each item with its position (``for i, x in enumerate(...)``)."""
    return [[i, item] for i, item in enumerate(_loop_source("enumerate()", items))]


def _zip(*lists: Any) -> list[list[Any]]:
    """``[[a0, b0], [a1, b1], …]`` — lists paired by position, as long as the shortest."""
    return [list(row) for row in zip(*(_loop_source("zip()", value) for value in lists), strict=False)]


def _word_count(value: Any) -> int:
    """Words in a text — THE ONE counter ``text.word_count`` and the length checks use."""
    from matrx_graph.checks import text_metrics

    text = _text_arg("word_count", value)
    return 0 if text is None else int(text_metrics(text)["words"])


def _sha256(value: Any) -> str:
    """Hex sha256 of a text's UTF-8 bytes — the same digest ``crypto.hash`` (sha256) gives."""
    import hashlib

    text = _text_arg("sha256", value)
    return hashlib.sha256((text or "").encode("utf-8")).hexdigest()


def _sha1(value: Any) -> str:
    """Hex sha1 of a text's UTF-8 bytes. Not for secrets: it reproduces keys stored by code that
    hashed with sha1 (Smart Add's ``description:`` / ``address:`` evidence keys are
    ``sha1(collapse_spaces(lower(text)))[:12]``, ``matrx_social.identity.field_key``), so a
    workflow's key meets the one an earlier round stored. Added 2026-10-28."""
    import hashlib

    text = _text_arg("sha1", value)
    return hashlib.sha1((text or "").encode("utf-8")).hexdigest()  # noqa: S324 — a key, not a secret


def _fill(template: Any, item: Any, index: Any = None, extra: Any = None) -> Any:
    """A ``data.map_template`` template filled for one item — THE SAME function the step uses, so a
    folded template reads exactly as the step did (``$item`` / ``$index`` / ``$in`` / ``$optional`` /
    ``$format``; ``$run`` is refused here, as in any template that has no run)."""
    from matrx_graph.nodes._template import substitute_template

    if extra is not None and not isinstance(extra, dict):
        raise ExecutionError("fill() takes the other inputs as a record (its 4th value).")
    return substitute_template(template, item, index=index if isinstance(index, int) else None, extra=extra)


def _instant(name: str, value: Any) -> Any:
    """An ISO-8601 date/time (text, or a datetime) as a datetime; None stays None. A "Z" suffix is UTC."""
    from datetime import datetime

    if value is None or value == "":
        return None
    if isinstance(value, datetime):
        return value
    if not isinstance(value, str):
        raise ExecutionError(f"{name}() takes an ISO-8601 date/time text, got {type(value).__name__}.")
    try:
        return datetime.fromisoformat(value.strip().replace("Z", "+00:00"))
    except ValueError as exc:
        raise ExecutionError(f"{name}() could not read {value!r} as an ISO-8601 date/time.") from exc


def _seconds_between(start: Any, end: Any) -> float | None:
    """Seconds from ``start`` to ``end`` (negative when ``end`` is earlier); None when either is missing.
    Both ISO-8601. Two times must both carry a timezone or both not. Users: a recording's length from its row
    timestamps; elapsed time into a meeting for a transcript line's [mm:ss]; an SLA check ("answered within
    an hour")."""
    a, b = _instant("seconds_between", start), _instant("seconds_between", end)
    if a is None or b is None:
        return None
    if (a.tzinfo is None) != (b.tzinfo is None):
        raise ExecutionError("seconds_between() takes two times that both have a timezone, or neither.")
    return (b - a).total_seconds()


def _add_seconds(value: Any, seconds: Any) -> str | None:
    """``value`` shifted by ``seconds`` (a number, negative goes back), as ISO-8601 with the same timezone;
    None stays None. Users: a transcript segment's start = the recording's start + its offset; a deadline =
    now + a setting; a window's end from its start."""
    from datetime import timedelta

    instant = _instant("add_seconds", value)
    if instant is None:
        return None
    if isinstance(seconds, bool) or not isinstance(seconds, (int, float)):
        raise ExecutionError("add_seconds() takes a number of seconds as its second value.")
    return (instant + timedelta(seconds=float(seconds))).isoformat()


_SAFE_HELPERS: dict[str, Any] = {
    "abs": abs,
    "add_seconds": _add_seconds,
    "after": _after,
    "all": all,
    "any": any,
    "before": _before,
    "bool": bool,
    "casefold": _casefold,
    "coalesce": _coalesce,
    "collapse_spaces": _collapse_spaces,
    "contains_all": _contains_all,
    "contains_any": _contains_any,
    "difference": _difference,
    "endswith": _endswith,
    "enumerate": _enumerate,
    "everyday_words": _everyday_words,
    "fill": _fill,
    "float": float,
    "get": _get,
    "int": int,
    "intersection": _intersection,
    "join": _join,
    "len": len,
    "lower": _lower,
    "max": max,
    "min": min,
    "nfkc": _nfkc,
    "on_site": _on_site,
    "regex_replace": _regex_replace,
    "regex_split": _regex_split,
    "sha1": _sha1,
    "sha256": _sha256,
    "replace": _replace,
    "round": round,
    "seconds_between": _seconds_between,
    "sorted": sorted,
    "split": _split,
    "startswith": _startswith,
    "str": str,
    "sum": sum,
    "matches": _matches,
    "url_depth": _url_depth,
    "url_host": _url_host,
    "url_path": _url_path,
    "word_count": _word_count,
    "zip": _zip,
}

#: Helpers a generator expression may feed (``sum(r['n'] for r in inputs['rows'])``). A generator is
#: never a value on its own: a bare one would reach channels as a live object.
_GENERATOR_CONSUMERS = frozenset({"all", "any", "join", "max", "min", "sorted", "sum"})

#: List loops (comprehensions), 2026-10-27 — PRIMITIVES-LIST-EXPRESSIONS.md. At most this many ``for``
#: clauses in one comprehension, and comprehensions nested this deep (one inside another counts 2).
MAX_LOOP_CLAUSES = 2
MAX_LOOP_DEPTH = 2

#: The ``workflow.expression.max_loop_steps`` knob's starting value (the mirror used when the host has
#: bound no reader): items all the loops of ONE evaluation may go over in total.
STARTING_MAX_LOOP_STEPS = 100_000

_COMPREHENSIONS = (ast.ListComp, ast.SetComp, ast.DictComp, ast.GeneratorExp)

_ALLOWED_NODES: tuple[type[ast.AST], ...] = (
    ast.Expression,
    ast.BoolOp,
    ast.BinOp,
    ast.UnaryOp,
    ast.Compare,
    ast.Constant,
    ast.Name,
    ast.Load,
    ast.Subscript,
    # Pure data slicing (`inputs['prompts'][:5]`) — no call, no traversal.
    ast.Slice,
    # Conditional expressions (`a if cond else b`) — pure control, no escape
    # surface, and the natural shape of a keep-best guard.
    ast.IfExp,
    # Safe-helper calls ONLY — see _SAFE_HELPERS + the walker's func check.
    ast.Call,
    ast.Tuple,
    ast.List,
    ast.Dict,
    ast.Set,
    ast.And,
    ast.Or,
    ast.Not,
    ast.Eq,
    ast.NotEq,
    ast.Lt,
    ast.LtE,
    ast.Gt,
    ast.GtE,
    ast.In,
    ast.NotIn,
    ast.Is,
    ast.IsNot,
    ast.Add,
    ast.Sub,
    ast.Mult,
    ast.Div,
    ast.Mod,
    ast.FloorDiv,
    # ast.Pow deliberately EXCLUDED: `10**10**10` computes an exponential
    # tower before any timeout can fire — a one-line CPU/memory DoS. There
    # is no eval-time guard possible (CPython evaluates the literal power
    # eagerly), so exponentiation is banned from the sandbox surface.
    ast.USub,
    ast.UAdd,
    ast.Invert,
    # List loops: ``[x for x in …]``, ``{k: v for …}``, ``{x for …}``, and a generator only as the
    # argument of an aggregating helper. ``Store`` exists only on a loop's own target of plain names
    # (checked in ``_check_scopes``); every iterable is counted against the loop budget at run time.
    *_COMPREHENSIONS,
    ast.comprehension,
    ast.Store,
)


def validate_expression(expr: str) -> ast.Expression:
    """Parse + AST-walk `expr` against the sandbox rules — NO data needed.

    Raises ExecutionError with the exact runtime complaint on any disallowed
    construct, so authoring surfaces (the workflow-plans emit/resolve gate)
    can refuse a doomed expression BEFORE it persists instead of letting the
    run discover it. This is the same walk `safe_eval` runs — extracting it
    keeps the sandbox a single audit surface. Returns the parsed Expression
    so `safe_eval` can compile it without re-parsing.
    """
    try:
        parsed = ast.parse(expr, mode="eval")
    except SyntaxError as e:
        raise ExecutionError(f"Invalid expression syntax: {e}") from e

    for node in ast.walk(parsed):
        if not isinstance(node, _ALLOWED_NODES):
            raise ExecutionError(f"Disallowed expression element {type(node).__name__!r}. {DIALECT}")
        if isinstance(node, ast.Call):
            # The safe-helper primitive: the ONLY legal call is a bare
            # whitelisted name with plain positional args. A func that is a
            # Subscript (`inputs['f'](…)`) or anything else is rejected, and
            # method calls are impossible outright (Attribute isn't allowed).
            if not isinstance(node.func, ast.Name) or node.func.id not in _SAFE_HELPERS:
                raise ExecutionError(
                    "Disallowed call target. Only the safe helpers "
                    f"({', '.join(sorted(_SAFE_HELPERS))}) may be called."
                )
            if node.keywords:
                raise ExecutionError("Disallowed keyword arguments in safe-helper call.")
            for arg in node.args:
                if isinstance(arg, ast.GeneratorExp) and node.func.id not in _GENERATOR_CONSUMERS:
                    raise ExecutionError(
                        f"A generator `(x for x in …)` can only feed {', '.join(sorted(_GENERATOR_CONSUMERS))}; "
                        f"use a list `[x for x in …]` for {node.func.id}()."
                    )
    _check_scopes(parsed.body, frozenset(), 0, parent_call=False)
    return parsed


#: The expression language in one sentence — the refusal text, and what authoring guides quote.
DIALECT = (
    "Permitted: constants, arithmetic, comparison, boolean ops, list/dict/tuple/set literals, "
    "subscripts/slices, conditional expressions (a if c else b), list loops "
    f"([x for x in L if c], {{k: v for k, v in L}}, at most {MAX_LOOP_CLAUSES} `for` per loop and "
    f"{MAX_LOOP_DEPTH} levels; a generator (x for x in L) only inside "
    f"{', '.join(sorted(_GENERATOR_CONSUMERS))}), safe-helper calls "
    f"({', '.join(sorted(_SAFE_HELPERS))}), and the `inputs` variable. "
    "No attribute access (x.y), no other names, no keyword arguments."
)


def _check_target(target: ast.expr) -> set[str]:
    """A loop's target: a plain name or a tuple of plain names, none shadowing `inputs` or a helper."""
    names = [target] if isinstance(target, ast.Name) else list(getattr(target, "elts", []))
    if not isinstance(target, ast.Name | ast.Tuple) or not all(isinstance(n, ast.Name) for n in names):
        raise ExecutionError(
            "A list loop's variable must be a plain name or names (`for x in …`, `for k, v in …`)."
        )
    bound: set[str] = set()
    for n in names:
        assert isinstance(n, ast.Name)
        if n.id == "inputs" or n.id in _SAFE_HELPERS or n.id.startswith("_"):
            raise ExecutionError(
                f"Loop variable {n.id!r} is not allowed: it may not be `inputs`, a helper name, or start with '_'."
            )
        bound.add(n.id)
    return bound


def _check_scopes(node: ast.AST, scope: frozenset[str], depth: int, *, parent_call: bool) -> None:
    """Names resolve only to `inputs`, a helper, or a loop variable of an ENCLOSING loop; ``Store``
    appears only on loop targets; loops respect the clause and depth limits; a generator stands only
    as an aggregating helper's argument."""
    if isinstance(node, _COMPREHENSIONS):
        if isinstance(node, ast.GeneratorExp) and not parent_call:
            raise ExecutionError(
                "A generator `(x for x in …)` is not a value; write a list `[x for x in …]` or put it "
                f"inside {', '.join(sorted(_GENERATOR_CONSUMERS))}."
            )
        if depth + 1 > MAX_LOOP_DEPTH:
            raise ExecutionError(f"List loops may nest at most {MAX_LOOP_DEPTH} levels deep.")
        if len(node.generators) > MAX_LOOP_CLAUSES:
            raise ExecutionError(f"A list loop may have at most {MAX_LOOP_CLAUSES} `for` clauses.")
        inner = scope
        for gen in node.generators:
            if gen.is_async:
                raise ExecutionError("`async for` is not allowed.")
            # The iterable is read in the scope BEFORE this clause binds its variable.
            _check_scopes(gen.iter, inner, depth + 1, parent_call=False)
            inner = inner | _check_target(gen.target)
            for cond in gen.ifs:
                _check_scopes(cond, inner, depth + 1, parent_call=False)
        parts = [node.key, node.value] if isinstance(node, ast.DictComp) else [node.elt]
        for part in parts:
            _check_scopes(part, inner, depth + 1, parent_call=False)
        return
    if isinstance(node, ast.Name):
        if isinstance(node.ctx, ast.Store):
            raise ExecutionError("Assignment is not allowed; only a list loop binds a name.")
        if node.id != "inputs" and node.id not in _SAFE_HELPERS and node.id not in scope:
            raise ExecutionError(
                f"Disallowed name {node.id!r}. Only `inputs`, the safe helpers "
                f"({', '.join(sorted(_SAFE_HELPERS))}) and a loop's own variables are exposed."
            )
        return
    if isinstance(getattr(node, "ctx", None), ast.Store):
        raise ExecutionError("Assignment is not allowed; only a list loop binds a name.")
    if isinstance(node, ast.Call):
        for arg in node.args:
            _check_scopes(arg, scope, depth, parent_call=True)
        return
    for child in ast.iter_child_nodes(node):
        _check_scopes(child, scope, depth, parent_call=False)


class _LoopGuard(ast.NodeTransformer):
    """Wraps every loop's iterable in ``__loop(…)`` so each item is counted against the budget.
    The name is injected per evaluation and cannot be spelled by an author (leading '_' is refused)."""

    def visit_comprehension(self, node: ast.comprehension) -> ast.comprehension:
        self.generic_visit(node)
        node.iter = ast.Call(func=ast.Name(id="__loop", ctx=ast.Load()), args=[node.iter], keywords=[])
        return node


#: The host's reader for ``workflow.expression`` knobs (a ``key -> value`` callable over the primed
#: snapshot); None → the starting value, announced once.
_expression_knob_reader: Any = None
_loop_budget_announced = False


def configure_expression_knobs(reader: Any) -> None:
    """Bind the host's reader for the ``workflow.expression`` feature (aidream: knob_raw_sync)."""
    global _expression_knob_reader, _loop_budget_announced
    _expression_knob_reader = reader
    _loop_budget_announced = False


def max_loop_steps() -> int:
    """The live ``workflow.expression.max_loop_steps`` knob; loud once, then the starting value."""
    global _loop_budget_announced
    if _expression_knob_reader is not None:
        try:
            return max(1, int(_expression_knob_reader("max_loop_steps")))
        except Exception as exc:  # noqa: BLE001 - announced degradation, never a crash in an expression
            reason = f"reader failed: {exc!r}"
    else:
        reason = "no host reader bound (configure_expression_knobs)"
    if not _loop_budget_announced:
        _loop_budget_announced = True
        import sys

        print(
            f"[matrx_graph] workflow.expression.max_loop_steps: {reason}; using the starting value "
            f"{STARTING_MAX_LOOP_STEPS}, which an admin cannot change until it is bound",
            file=sys.stderr,
        )
    return STARTING_MAX_LOOP_STEPS


def _loop_counter(budget: int) -> Any:
    used = [0]

    def loop(value: Any) -> Any:
        for item in _loop_source("A list loop", value):
            used[0] += 1
            if used[0] > budget:
                raise ExecutionError(
                    f"This expression loops over more than {budget} items in total (the "
                    "workflow.expression max_loop_steps setting). Narrow the lists first, or raise the setting."
                )
            yield item

    return loop


def safe_eval(expr: str, inputs: dict[str, Any]) -> Any:
    """Evaluate a restricted-Python expression against a single name: `inputs`.

    Allowed: constants, arithmetic, comparison, boolean ops, subscripts and
    slices, conditional expressions, literals (list/dict/tuple/set), and calls
    to the frozen safe-helper table (`len`, `min`, `max`, `int`, `str`, …).
    Disallowed: attribute access (ALWAYS — it is the escape primitive), any
    other call target, keywords/unpacking in calls, any name other than
    `inputs` and the helpers, imports, control flow, exponentiation.

    Used by control.branch / control.loop (result coerced to bool), data.rules,
    data.assert, data.filter, and data.transform (result passed through).
    Shared here so the sandbox stays a single audit surface rather than
    drifting per-node. The parse/walk half is `validate_expression`, callable
    without data by authoring-time gates.
    """
    parsed = validate_expression(expr)
    namespace: dict[str, Any] = {"__builtins__": {}, "inputs": inputs, **_SAFE_HELPERS}
    has_loops = any(isinstance(node, ast.comprehension) for node in ast.walk(parsed))
    if has_loops:
        # ONE globals dict: a generator expression is its own scope and reads `inputs` and the
        # helpers from globals (a separate locals dict would leave them unresolved inside it).
        parsed = ast.fix_missing_locations(_LoopGuard().visit(parsed))
        namespace["__loop"] = _loop_counter(max_loop_steps())
    compiled = compile(parsed, "<matrx-graph-sandbox>", "eval")
    result = eval(compiled, namespace)  # noqa: S307
    if isinstance(result, Iterator):
        raise ExecutionError("An expression's result cannot be a generator; write a list `[x for x in …]`.")
    return result


# ---------------------------------------------------------------------------
# The scalar-binding trap — why `bind_item` exists (2026-09-12, W58).
#
# Several call sites evaluate an expression once PER ITEM (data.filter) or per
# delivered payload (conditional edges). The sandbox exposes exactly one name,
# so a non-dict payload has to be wrapped: `{"value": item}`. That wrapping is
# invisible to the author, and it turns any expression that uses `inputs` as a
# WHOLE VALUE into a constant:
#
#     items    = ["only-restraint-calls-out-rage", ...]   (14 real rule ids)
#     bound    = {"value": "only-restraint-calls-out-rage"}
#     `('|' + str(inputs) + '|') not in '|...|'`
#            -> "|{'value': 'only-restraint-calls-out-rage'}|" not in "|...|"
#            -> True, for every id that ever existed.
#
# That is the production incident of 2026-09-12 16:37Z (run
# 5f461187-32ba-4e6a-9ef8-5b5640677dd7): a citation gate reported kept=14,
# dropped=0 over 14 ids that were ALL in its own 200-id list, and a correct
# run was refused as "cited a rule that does not exist". No exception fired —
# `str` is a safe helper and `in` over two strings is legal — so the predicate
# was not wrong, it was INERT. The author's "fix", `inputs in [...]`, is the
# same defect with the sign flipped: a dict is never in a list of strings, so
# it answers False for every item and the gate silently stops gating.
#
# An inert predicate is the worst failure mode a gate can have, so the sandbox
# refuses to produce one: when the payload had to be wrapped, an expression
# that reads bare `inputs` FAILS the step and names the construct. Comparing a
# scalar item is spelled `inputs['value']`.
# ---------------------------------------------------------------------------

SCALAR_BINDING_KEY = "value"


def uses_bare_inputs(expr: str | ast.Expression) -> bool:
    """True when `inputs` is read as a whole value, not as a subscript base.

    `inputs['value'] > 1` is False (every `inputs` is a Subscript base);
    `str(inputs)`, `inputs in [...]`, `inputs == 'x'`, `len(inputs)` are True.
    """
    parsed = validate_expression(expr) if isinstance(expr, str) else expr
    subscripted: set[int] = {
        id(node.value)
        for node in ast.walk(parsed)
        if isinstance(node, ast.Subscript) and isinstance(node.value, ast.Name)
    }
    return any(
        isinstance(node, ast.Name) and node.id == "inputs" and id(node) not in subscripted
        for node in ast.walk(parsed)
    )


def bind_item(expr: str, item: Any, *, where: str) -> dict[str, Any]:
    """Bind one per-item payload to the sandbox's single `inputs` name.

    A dict binds as itself. A scalar (str/int/list/None/…) has to be wrapped as
    ``{"value": item}`` — and because that wrapper is invisible to whoever wrote
    the expression, an expression that reads bare `inputs` would silently be
    evaluated against the WRAPPER instead of the item, returning the same answer
    for every item. That is refused here with the construct named, never
    evaluated into a constant. See the block comment above.
    """
    if isinstance(item, dict):
        return item
    if uses_bare_inputs(expr):
        raise ExecutionError(
            f"{where}: the expression {expr!r} reads `inputs` as a whole value, but "
            f"this payload is a {type(item).__name__}, which the sandbox can only "
            f"bind as {{'{SCALAR_BINDING_KEY}': <the {type(item).__name__}>}}. "
            f"`inputs` would therefore be that wrapper dict and never the "
            f"{type(item).__name__} itself, so the expression would return the SAME "
            f"answer for every payload — an inert test that passes or fails "
            f"everything. Compare the payload itself: write "
            f"`inputs['{SCALAR_BINDING_KEY}']` wherever you wrote bare `inputs` "
            f"(e.g. `inputs['{SCALAR_BINDING_KEY}'] in ['a', 'b']`)."
        )
    return {SCALAR_BINDING_KEY: item}
