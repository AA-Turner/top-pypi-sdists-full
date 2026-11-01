"""rule for sort: no output, temp-folder or compress-program options."""

from __future__ import annotations
from probe.daemon.shell.classifier.refusals import _Refuse
from probe.daemon.shell.parse import _Word
from probe.daemon.shell.safe_lists import _SORT_VALUE_LETTERS
from probe.daemon.shell.words import _long, _options, _short_letters


class SortRuleMixin:
    """Part of _Checker: its methods run with `self` the _Checker; compose() folds them into _Checker."""

    def _sort(self, args: list[_Word], cands: list[str]) -> None:
        for v in _options(args):
            bad = _long(v, ("--output", "--compress-program", "--temporary-directory"))
            letters = _short_letters(v, _SORT_VALUE_LETTERS)
            if bad == "--compress-program":
                raise _Refuse("sort --compress-program runs another program.")
            if bad or "o" in letters or "T" in letters:
                raise _Refuse("sort -o / -T writes files.")
        self._reader("sort", args, cands)
