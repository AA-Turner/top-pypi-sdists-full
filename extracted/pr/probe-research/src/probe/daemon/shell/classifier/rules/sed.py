"""rule for sed: `sed -n Np` / `M,Np` only."""

from __future__ import annotations
import re
from probe.daemon.shell.classifier.refusals import _Refuse
from probe.daemon.shell.parse import _Word
_SED_PRINT = re.compile(r"[0-9]+(,[0-9]+)?p")  # Codex: /^(\d+,)?\d+p$/


class SedRuleMixin:
    """Part of _Checker: its methods run with `self` the _Checker; compose() folds them into _Checker."""

    def _sed(self, args: list[_Word], cands: list[str]) -> None:
        # Codex: `sed -n {N|M,N}p [FILE]`, nothing else. Ours: the FILE may not be an option.
        values = [w.value for w in args]
        if not (
            2 <= len(values) <= 3 and values[0] == "-n" and _SED_PRINT.fullmatch(values[1])
        ):
            raise _Refuse("Of sed, only `sed -n 5p` / `sed -n 1,5p` is safe.")
        if len(values) == 3:
            if values[2].startswith("-") and values[2] != "-":
                raise _Refuse("sed -n Np takes a file there, not an option (-e can write files).")
            self._check_path(args[2].value, args[2].tilde, cands)
