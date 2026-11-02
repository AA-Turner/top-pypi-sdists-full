"""Trust rule: paired lines whose only change is type annotations.

Telling a type-annotation ``:`` from a suite / dict / ternary / lambda /
object-value / case-label colon is a lexing question, so we tokenize the line
(see `tokens.py`) and reason about token *roles*, not bytes.

The rule uses a **delta** model: rather than erasing the "trivial" part and
hoping the rest matches, it diffs the two sides' token sequences and trusts only
when *every* changed token is flagged as part of an annotation — default-deny, so
an unrecognized change is never hidden. Token roles come from the span detectors
(`_py_spans`/`_ts_spans`), which flag a token only when it is *definitely* inside
an annotation. The paired-line scaffolding it shares with `_style` (equal counts,
indentation guard, tokenize-or-decline) lives in `delta.py`.
"""

from __future__ import annotations

import difflib
import keyword
from itertools import pairwise

from ..diff import DiffFile, DiffHunk
from .delta import paired_changed_lines, paired_token_delta
from .helpers import extension
from .labels import Trust
from .tokens import CLOSE_BRACKETS, OP, OPEN_BRACKETS, WORD, Token

# Narrower than the style/reflow core: only the languages the tokenizer models
# with an annotation grammar. Must stay a subset of `tokens._COMMENTS` keys — a
# lang added here without a tokenizer entry would silently mis-lex, not decline.
_ANNOTATION_LANGS = frozenset(("py", "ts", "tsx"))

Span = tuple[int, int]  # a [start, end) char range covering an annotation


def _type_span_to(tokens: list[Token], colon: int, stops: tuple[str, ...]) -> Span:
    """Span from just before `tokens[colon]` (the `:`/`->`) to the end of the type
    that follows — the type ends at a top-level token in `stops`, at the closer of
    the bracket it sits inside, or at the line's end. Shared by every annotation
    context (Python params/returns/vars, TS params/vars)."""
    start = tokens[colon - 1].end
    depth = 0
    type_end = tokens[colon].end
    j, n = colon + 1, len(tokens)
    while j < n:
        tk = tokens[j]
        if depth == 0 and tk.kind == OP and tk.text in stops:
            break
        if tk.kind == OP and tk.text in OPEN_BRACKETS:
            depth += 1
        elif tk.kind == OP and tk.text in CLOSE_BRACKETS:
            if depth == 0:
                break
            depth -= 1
        type_end = tk.end
        j += 1
    return (start, type_end)


# --- Python ---


def _py_var_spans(tokens: list[Token]) -> list[Span]:
    """The `: TYPE` span of a `NAME: TYPE = value` annotated ASSIGNMENT.

    Requires a top-level `=`: a bare `NAME: X` (no assignment) is ambiguous — a
    statement-level type declaration vs a dict/keyed entry whose `{` opened on an
    earlier line — and stripping a dict value would hide a real data change, so we
    leave a bare colon alone. The span runs from just after NAME to the end of the
    last type token before the `=`."""
    depth = 0
    for i in range(2, len(tokens)):
        t = tokens[i]
        if t.kind == OP and t.text in OPEN_BRACKETS:
            depth += 1
        elif t.kind == OP and t.text in CLOSE_BRACKETS:
            depth -= 1
        elif depth == 0 and t.kind == OP and t.text == "=":
            return [(tokens[0].end, tokens[i - 1].end)]
    return []  # no top-level '=' -> bare/ambiguous annotation, leave it


def _py_def_spans(tokens: list[Token]) -> list[Span]:
    """The param (`a: T`) and return (`-> T`) annotation spans of a def line.

    A parameter type runs to the next top-level `,` or the closing `)`; a return
    type runs to the suite `:` — both computed by the shared `_type_span_to`.
    Bails (strips nothing) if the signature contains a `lambda`, whose body colon
    would otherwise read as a param annotation. Colons only count as parameter
    annotations INSIDE the parameter parens: once they close, a depth-1 colon is
    in some other bracket on the line (a dict or slice in a one-line def body,
    e.g. `def f(): return {"timeout": 30}`) and must stay unflagged so a value
    change there is never trusted."""
    if any(t.kind == WORD and t.text == "lambda" for t in tokens):
        return []
    spans: list[Span] = []
    depth = 0
    params_closed = False
    for i, t in enumerate(tokens):
        if t.kind != OP:
            continue
        if t.text == ":" and depth == 1 and not params_closed:
            # a parameter annotation — stop at the next param `,`, the closing `)`,
            # or a default-value `=` (else the default would be swallowed too)
            spans.append(_type_span_to(tokens, i, (",", "=")))
        elif t.text == "->" and depth == 0:
            spans.append(_type_span_to(tokens, i, (":",)))  # the return annotation
        elif t.text in OPEN_BRACKETS:
            depth += 1
        elif t.text in CLOSE_BRACKETS:
            depth -= 1
            if depth == 0:
                params_closed = True  # the def's parameter list has ended
    return spans


def _py_spans(tokens: list[Token]) -> list[Span]:
    if not tokens:
        return []
    first = tokens[0]
    if first.kind == WORD and first.text in ("def", "async"):
        return _py_def_spans(tokens)
    # An annotated assignment `NAME: TYPE`: a leading identifier (not a keyword,
    # so not `if`/`for`/`lambda`/…) immediately followed by a colon.
    if (
        first.kind == WORD
        and not keyword.iskeyword(first.text)
        and len(tokens) >= 2
        and tokens[1].kind == OP
        and tokens[1].text == ":"
    ):
        return _py_var_spans(tokens)
    return []


# --- TypeScript ---


def _ts_var_span(tokens: list[Token]) -> list[Span]:
    """The `: TYPE` span of a `const/let/var NAME: TYPE` declaration.

    The span stops at a top-level `,` as well as `=`: in a multi-declarator
    statement (`let x: number, other: string`) the comma ends the first
    declarator, and running past it would flag the NEXT declarator's name as
    annotation — letting a rename hide as a type change."""
    if not (
        tokens and tokens[0].kind == WORD and tokens[0].text in ("const", "let", "var")
    ):
        return []
    depth = 0
    for i, t in enumerate(tokens):
        if t.kind == OP and t.text in OPEN_BRACKETS:
            depth += 1
        elif t.kind == OP and t.text in CLOSE_BRACKETS:
            depth -= 1
        elif depth == 0 and t.kind == OP and t.text == "=":
            return []  # a value assignment reached before any annotation
        elif depth == 0 and t.kind == OP and t.text == ":":
            return [_type_span_to(tokens, i, ("=", ","))]
    return []


def _ts_param_spans(tokens: list[Token]) -> list[Span]:
    """The `a: T` param annotation spans of a `function` signature.

    Bails on any `?` in the line — an optional marker (`a?: T`) or a ternary in a
    default value — rather than risk mistaking a ternary colon for an annotation."""
    if any(t.kind == OP and t.text == "?" for t in tokens):
        return []
    spans: list[Span] = []
    stack: list[str] = []
    i, n = 0, len(tokens)
    while i < n:
        t = tokens[i]
        if t.kind == OP and t.text in OPEN_BRACKETS:
            stack.append(t.text)
        elif t.kind == OP and t.text in CLOSE_BRACKETS:
            if stack:
                stack.pop()
        elif t.kind == OP and t.text == ":" and stack and stack[-1] == "(":
            spans.append(_type_span_to(tokens, i, (",", "=")))
        i += 1
    return spans


def _ts_spans(tokens: list[Token]) -> list[Span]:
    if var_span := _ts_var_span(tokens):
        return var_span
    if any(t.kind == WORD and t.text == "function" for t in tokens):
        return _ts_param_spans(tokens)
    return []


# --- Delta classifier + the rule ---


def _span_has_call(tokens: list[Token], start: int, end: int) -> bool:
    """Does this annotation span contain a call — `NAME(`, `)(`, or `](`?

    An annotation is trusted on the premise that it is runtime-inert (erasable
    type info). That premise breaks when the type region contains a call: an
    `Annotated[User, Depends(require_admin)]` dependency, a Pydantic
    `Field(gt=0, le=1000)`, a `Query(max_length=50)` validator, or a
    module-level annotation that is itself evaluated. Their arguments ARE
    runtime behavior, so a change inside them (require_admin -> require_login,
    le=1000 -> le=100000) is a real change, not a type edit — the span must not
    be trusted."""
    in_span = [t for t in tokens if start <= t.start and t.end <= end]
    for prev, cur in pairwise(in_span):
        if (
            cur.kind == OP
            and cur.text == "("
            and (prev.kind == WORD or (prev.kind == OP and prev.text in ")]"))
        ):
            return True
    return False


def _annotation_token_flags(tokens: list[Token], ext: str) -> list[bool]:
    """Per token: does it lie within a type-annotation span (the `:`/`->` plus the
    type that follows)? A token is flagged only when it is *definitely* part of an
    annotation, so an unflagged token that changed always defeats the rule."""
    spans = _py_spans(tokens) if ext == "py" else _ts_spans(tokens)
    # Drop any span containing a call — its arguments are runtime-active, so a
    # change there is a real behavior change, not an erasable type edit.
    spans = [s for s in spans if not _span_has_call(tokens, *s)]
    return [
        any(start <= tok.start and tok.end <= end for start, end in spans)
        for tok in tokens
    ]


def _annotation_delta(
    old_tokens: list[Token], new_tokens: list[Token], ext: str
) -> bool | None:
    """Compare one line pair: True if it differs ONLY in type-annotation tokens,
    False if token-identical, None if a non-annotation token changed. Every
    changed token, on either side, must fall inside a flagged annotation span."""
    old_ann = _annotation_token_flags(old_tokens, ext)
    new_ann = _annotation_token_flags(new_tokens, ext)
    matcher = difflib.SequenceMatcher(
        a=[t.text for t in old_tokens], b=[t.text for t in new_tokens], autojunk=False
    )
    changed = False
    for op, i1, i2, j1, j2 in matcher.get_opcodes():
        if op == "equal":
            continue
        changed = True
        if not all(old_ann[i1:i2]) or not all(new_ann[j1:j2]):
            return None  # a non-annotation token changed — a real edit
    return changed


def _type_annotations(file: DiffFile, hunk: DiffHunk) -> Trust | None:
    """Paired lines whose entire token-level delta is type annotations."""
    ext = extension(file)
    if ext not in _ANNOTATION_LANGS:
        return None
    pairs = paired_changed_lines(hunk)
    if pairs is None:
        return None
    changed = paired_token_delta(
        pairs, ext, lambda old, new, o, n: _annotation_delta(o, n, ext)
    )
    return Trust.TYPE_ANNOTATIONS_MODIFIED if changed else None
