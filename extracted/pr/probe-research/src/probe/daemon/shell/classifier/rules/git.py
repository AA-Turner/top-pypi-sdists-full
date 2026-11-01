"""rule for git read verbs: allowed verbs and flags, history paths, the repository must start inside."""

from __future__ import annotations
import os
from typing import Sequence
from probe.daemon.shell.classifier.refusals import _Fix, _Never, _Refuse
from probe.daemon.shell.parse import _Word, _expand
from probe.daemon.shell.safe_lists import _GIT_DENIED, _GIT_GLOBAL_OK, _GIT_NEEDS, _GIT_VERBS
from probe.daemon.shell.words import _long, _options, _short_letters


class GitRuleMixin:
    """Part of _Checker: its methods run with `self` the _Checker; compose() folds them into _Checker."""

    def _git(self, args: list[_Word], cands: list[str]) -> None:
        dirs = list(cands)
        k = 0
        while k < len(args) and args[k].value.startswith("-"):
            v = args[k].value
            if v == "-C" and k + 1 < len(args):
                target = args[k + 1]
                self._check_path(target.value, target.tilde, dirs, verb="It runs git in")
                path = _expand(target, self.home)
                dirs = sorted({os.path.realpath(os.path.join(d, path)) for d in dirs})
                k += 2
            elif v in _GIT_GLOBAL_OK:
                k += 1
            elif v.startswith(("-c", "--config-env")):
                raise _Refuse("git -c can switch on a pager, hooks or other programs.")
            else:
                raise _Refuse(f"The git option {v} isn't on the safe list.")
        if k == len(args):
            raise _Refuse("git without a read verb isn't on the safe list.")
        verb, rest = args[k].value, args[k + 1 :]
        if verb not in _GIT_VERBS:
            raise _Refuse(
                f"git {verb} isn't a read-only git verb (status, log, diff, show, blame, branch --show-current, "
                "rev-parse, ls-files)."
            )
        for folder in dirs:
            self._require_cwd([folder], "git")
            self._git_repository(folder)
        options = _options(rest)
        for v in options:
            bad = _long(v, tuple(_GIT_DENIED))
            if bad:
                raise _Refuse(f"git {verb} {v} isn't allowed: it {_GIT_DENIED[bad]}.")
        if verb == "branch" and [w.value for w in rest] != ["--show-current"]:
            raise _Refuse("Of git branch, only `git branch --show-current` is safe.")
        if verb == "status" and any(
            _long(v, ("--verbose",)) or "v" in _short_letters(v, "u") for v in options
        ):
            raise _Refuse("git status -v prints diffs.")
        needs = _GIT_NEEDS.get(verb, ())
        if any(flag not in options for flag in needs):
            raise _Fix(
                f"git {verb} needs {' '.join(needs)} so the repository's settings can't run programs."
            )
        self._git_names(verb, rest)
        self._args(rest, dirs)

    def _git_names(self, verb: str, rest: Sequence[_Word]) -> None:
        """git prints files from HISTORY too, where the path checks can't look: a
        `REV:path` and a pathspec are refused when their NAME is a credential's or a
        hidden file's, whether or not the file still exists in the work tree."""
        names_only = False
        for word in rest:
            v = word.value
            if v == "--":
                names_only = True
                continue
            if v.startswith("-") and not names_only:
                continue
            path = v.split(":", 1)[1] if ":" in v and not names_only else v
            path = path.lstrip("/").removeprefix("./")
            if not path:
                continue
            comps = [c for c in path.split("/") if c]
            hidden = next((c for c in comps[:-1] if c.startswith(".") and c not in (".", "..")), None)
            if self._secret(path):
                raise _Refuse(f"git {verb} {v} names a file credentials are kept in.")
            if self.hidden is not None and self.hidden(os.path.join(self.cwd, path)):
                raise _Never(f"git {verb} {v}: a .probe.config sets it to off, so Probe never reads it.")
            if hidden:
                raise _Refuse(f"git {verb} {v} names something inside a hidden folder ({hidden}).")

    def _git_repository(self, folder: str) -> None:
        """git looks upward for `.git`: the repository it finds must start inside."""
        path = folder
        while True:
            if os.path.lexists(os.path.join(path, ".git")):
                problem = self._place(path)
                if problem:
                    raise _Refuse(f"git would read the repository at {path}: {problem}.")
                return
            parent = os.path.dirname(path)
            if parent == path:
                return
            path = parent
