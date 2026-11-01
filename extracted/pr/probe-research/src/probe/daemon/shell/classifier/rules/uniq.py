"""rule for uniq: input only, never an output file."""

from __future__ import annotations
from probe.daemon.shell.classifier.refusals import _Refuse
from probe.daemon.shell.parse import _Word
from probe.daemon.shell.safe_lists import _FILES
from probe.daemon.shell.words import _long, _short_letters


class UniqRuleMixin:
    """Part of _Checker: its methods run with `self` the _Checker; compose() folds them into _Checker."""

    def _uniq(self, args: list[_Word], cands: list[str]) -> None:
        names = 0
        skip_next = False
        names_only = False
        for w in args:
            v = w.value
            if skip_next:
                skip_next = False
            elif w.synthetic:
                pass  # an option's value, not a second file
            elif names_only or v == "-" or not v.startswith("-"):
                names += 1
            elif v == "--":
                names_only = True
            elif v.startswith("--"):
                skip_next = "=" not in v and bool(
                    _long(v, ("--skip-fields", "--skip-chars", "--check-chars"))
                )
            else:
                letters = _short_letters(v, "fsw")
                skip_next = bool(letters) and letters[-1] in "fsw" and len(letters) == len(v) - 1
        if names > 1:
            raise _Refuse("uniq with a second file name writes its output there.")
        self._args(args, cands, anywhere=_FILES)
