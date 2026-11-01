"""rule for rg: no --pre/--search-zip/hostname-bin, no-ignore limits."""

from __future__ import annotations
from probe.daemon.shell.classifier.refusals import _Refuse
from probe.daemon.shell.parse import _Word
from probe.daemon.shell.safe_lists import (
    _FILES,
    _RG_NO_IGNORE,
    _RG_SELECTORS,
    _RG_UNSAFE_WITHOUT_ARGS,
    _RG_UNSAFE_WITH_ARGS,
    _RG_VALUE_LETTERS,
    _TEXT_OPTIONS,
)
from probe.daemon.shell.words import _long, _options, _short_letters


class RgRuleMixin:
    """Part of _Checker: its methods run with `self` the _Checker; compose() folds them into _Checker."""

    def _rg(self, args: list[_Word], cands: list[str]) -> None:
        for v in (w.value for w in args):  # Codex's rule, verbatim: any argument
            if v in _RG_UNSAFE_WITHOUT_ARGS or any(
                v == opt or v.startswith(f"{opt}=") for opt in _RG_UNSAFE_WITH_ARGS
            ):
                raise _Refuse(f"rg {v.split('=')[0]} runs another program.")
        unrestricted = 0
        for v in _options(args):  # ours: abbreviations, clusters, symlinks, hidden files

            bad = _long(v, (*_RG_UNSAFE_WITH_ARGS, "--search-zip", "--follow", "--hidden"))
            letters = _short_letters(v, _RG_VALUE_LETTERS)
            if bad in (*_RG_UNSAFE_WITH_ARGS, "--search-zip") or "z" in letters:
                raise _Refuse(f"rg {bad or '-z'} runs another program.")
            if bad == "--follow" or "L" in letters:
                raise _Refuse("rg -L follows symlinks out of the working folders.")
            if bad == "--hidden" or "." in letters:
                raise _Refuse("rg --hidden reads hidden files, which may hold credentials.")
            if _long(v, _RG_SELECTORS) or "g" in letters or "t" in letters:
                raise _Refuse(
                    "rg -g / --glob / -t / --type-add / --ignore-file can pick hidden and ignored files by name."
                )
            unrestricted += letters.count("u") + (_long(v, ("--unrestricted",)) is not None)
            if unrestricted >= 2:
                raise _Refuse("rg -uu reads hidden files, which may hold credentials.")
            if unrestricted or _long(v, _RG_NO_IGNORE):
                raise _Refuse(
                    "rg -u / --no-ignore reads ignored and hidden files (.env files and keys usually are)."
                )
        self._slices("rg", _options(args), args)
        self._require_cwd(cands, "rg")  # searched whole: it must be a working folder
        self._args(args, cands, text_options=_TEXT_OPTIONS["rg"], anywhere=_FILES)
