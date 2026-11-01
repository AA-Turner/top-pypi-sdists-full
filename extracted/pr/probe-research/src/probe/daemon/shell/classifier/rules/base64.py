"""rule for base64: decode/encode to stdout, no -o/--output."""

from __future__ import annotations
from probe.daemon.shell.classifier.refusals import _Refuse
from probe.daemon.shell.parse import _Word
from probe.daemon.shell.safe_lists import _BASE64_UNSAFE
from probe.daemon.shell.words import _long, _options, _short_letters


class Base64RuleMixin:
    """Part of _Checker: its methods run with `self` the _Checker; compose() folds them into _Checker."""

    def _base64(self, args: list[_Word], cands: list[str]) -> None:
        for v in (w.value for w in args):  # Codex's rule, verbatim: any argument
            if v in _BASE64_UNSAFE or v.startswith("--output=") or (
                v.startswith("-o") and v != "-o"
            ):
                raise _Refuse("base64 -o / --output writes to a file.")
        decode = False
        for v in _options(args):  # ours: abbreviations (--out=) and clusters (-do)
            if _long(v, ("--output",)) or "o" in _short_letters(v, "biow"):
                raise _Refuse("base64 -o / --output writes to a file.")
            decode = decode or bool(_long(v, ("--decode",))) or "d" in _short_letters(v, "w")
        if not decode:
            raise _Refuse(
                "base64 encoding changes text (a key included) into characters the scrubber can't recognise - "
                "only `base64 -d` runs at once."
            )
        self._args(args, cands)
