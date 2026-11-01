"""rule for find: no -exec/-delete/-fprint family, every start folder checked."""

from __future__ import annotations
from probe.daemon.shell.classifier.refusals import _Refuse
from probe.daemon.shell.parse import _Word
from probe.daemon.shell.safe_lists import (
    _FIND_LEADING,
    _FIND_PATTERNS,
    _FIND_UNSAFE,
    _FIND_UNSAFE_OURS,
    _NAMES,
    _TREE,
)


class FindRuleMixin:
    """Part of _Checker: its methods run with `self` the _Checker; compose() folds them into _Checker."""

    def _find(self, args: list[_Word], cands: list[str]) -> None:
        values = [w.value for w in args]
        for v in values:
            if v in _FIND_UNSAFE:
                raise _Refuse(f"find {v} can run commands, delete files or write files.")
            if v in _FIND_UNSAFE_OURS:
                why = "reads a list of start folders" if v == "-files0-from" else "follows symlinks"
                raise _Refuse(f"find {v} {why} the check can't see.")
        # find [-H] [-P] [-D opts] [-Olevel] [--] [start folder...] [expression]; BSD find
        # (macOS) also takes -E -X -d -s -x, in clusters, and `-f PATH`, a start folder.
        k, starts, walks_cwd = 0, 0, False
        while k < len(values):
            v = values[k]
            if v == "--":
                k += 1
                break
            if v == "-D":
                k += 2
                continue
            if v.startswith("-O"):
                k += 1
                continue
            flags = _FIND_LEADING.fullmatch(v)
            if not flags or not (flags.group(1) or flags.group(2) is not None):
                break
            if "L" in flags.group(1):
                raise _Refuse(f"find {v} follows symlinks the check can't see.")
            k += 1
            if flags.group(2) is None:
                continue
            if flags.group(2):  # `-f/etc`: BSD's start folder, or GNU's test (`-fstype`), which walks `.`
                self._check_path(flags.group(2), False, cands, anywhere=_TREE)
                walks_cwd = True
            elif k < len(args):
                self._check_path(args[k].value, args[k].tilde, cands, anywhere=_TREE)
                k += 1
            starts += 1
        while k < len(values) and values[k][:1] not in ("-", "(", ")", "!", ","):
            if args[k].synthetic:
                k += 1
                continue
            self._check_path(args[k].value, args[k].tilde, cands, anywhere=_TREE)
            starts += 1
            k += 1
        if not starts or walks_cwd:
            self._require_cwd(cands, "find with no start folder", anywhere=_TREE)
        self._args(args, cands, word_options=_FIND_PATTERNS, anywhere=_NAMES)
