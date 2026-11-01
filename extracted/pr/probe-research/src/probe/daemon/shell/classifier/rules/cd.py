"""rule for cd: the target must be a working folder."""

from __future__ import annotations
from probe.daemon.shell.classifier.refusals import _Refuse
from probe.daemon.shell.parse import _Part, _Word, _cd_word
from probe.daemon.shell.safe_lists import _NAMES


class CdRuleMixin:
    """Part of _Checker: its methods run with `self` the _Checker; compose() folds them into _Checker."""

    def _cd(self, args: list[_Word], cands: list[str]) -> None:
        word = _cd_word(_Part([_Word("cd", "cd"), *args], [], ""))
        if word is None:
            raise _Refuse("cd takes exactly one folder (no options, no bare `cd`, no `cd -`).")
        # A folder a read program could name: what runs there is checked in it (`_walk`).
        self._check_path(word.value, word.tilde, cands, logical=True, verb="It moves into", anywhere=_NAMES)
