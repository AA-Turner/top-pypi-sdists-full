"""rule for jq: no file-reading options or module imports."""

from __future__ import annotations
from probe.daemon.shell.classifier.refusals import _R_SCRAMBLE, _Refuse
from probe.daemon.shell.classifier.rules.reader import _R_SLICE
from probe.daemon.shell.parse import _Word
from probe.daemon.shell.safe_lists import (
    _FILES,
    _JQ_ENCODERS,
    _JQ_FILE_OPTIONS,
    _JQ_LONG_FLAGS,
    _JQ_MODULES,
    _JQ_SHORT_FLAGS,
    _JQ_SLICERS,
)


class JqRuleMixin:
    """Part of _Checker: its methods run with `self` the _Checker; compose() folds them into _Checker."""

    def _jq(self, args: list[_Word], cands: list[str]) -> None:
        program_seen = False
        string_args = False  # after --args / --jsonargs, positionals are strings
        names_only = False
        skip = 0
        for w in args:
            v = w.value
            if skip:
                skip -= 1
                continue
            if w.synthetic:
                continue  # an option's value, neither the program nor a file
            if not names_only and v.startswith("-") and v != "-":
                if v == "--":
                    names_only = True
                elif v.startswith("--"):
                    name = v.split("=", 1)[0]
                    if name in _JQ_FILE_OPTIONS:
                        raise _Refuse(f"jq {name} reads a file the check can't place.")
                    if v in ("--arg", "--argjson"):
                        skip = 2
                    elif v == "--indent":
                        skip = 1
                    elif v in ("--args", "--jsonargs"):
                        string_args = True
                    elif v not in _JQ_LONG_FLAGS:
                        raise _Refuse(f"The jq option {v} isn't on the safe list.")
                elif "f" in v[1:] or "L" in v[1:]:
                    raise _Refuse("jq -f / -L read files the check can't place.")
                elif any(ch not in _JQ_SHORT_FLAGS for ch in v[1:]):
                    raise _Refuse(f"The jq option {v} isn't on the safe list.")
                continue
            if not program_seen:
                program_seen = True
                if _JQ_MODULES.search(v):
                    raise _Refuse("jq import / include load files from jq's library folders.")
                if _JQ_ENCODERS.search(v):
                    raise _Refuse(_R_SCRAMBLE.format(what="jq's @base64 / @base32 / @uri / @sh / format / explode"))
                if _JQ_SLICERS.search(v):
                    raise _Refuse(_R_SLICE.format(what="jq's string slicing (.[m:n], split, sub, ltrimstr, match...)"))
            elif not string_args:
                self._check_path(v, w.tilde, cands, anywhere=_FILES)
