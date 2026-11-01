"""rule for the plain readers (cat, head, tail, wc, ls, du, gzip, digests...): options, slices, every name read."""

from __future__ import annotations
import os
import re
from typing import Sequence
from probe.daemon.shell.classifier.refusals import _Refuse
from probe.daemon.shell.parse import _Word, _expand
from probe.daemon.shell.safe_lists import (
    _DIGESTS,
    _DU_VALUE_LETTERS,
    _FILES,
    _GREP_VALUE_LETTERS,
    _GZIP_FLAGS,
    _GZIP_LONGS,
    _LINUX,
    _LISTED_VALUE_LETTERS,
    _NAMES,
    _RG_VALUE_LETTERS,
    _TEXT_OPTIONS,
    _TREE,
)
from probe.daemon.shell.words import _long, _options, _positionals, _short_letters
_R_SLICE = (
    "{what} prints text in pieces, and a piece of a key is something the scrubber can't recognise."
)
_R_GREP_R = (
    "grep -r reads every file under the folder, .env files and keys included."
)


class ReaderRuleMixin:
    """Part of _Checker: its methods run with `self` the _Checker; compose() folds them into _Checker."""

    # -- the commands --

    def _slices(self, name: str, options: list[str], args: list[_Word] | None = None) -> None:
        """Options that print part of a line: characters or bytes (`cut -c/-b`,
        `head -c`, `tail -c`, and head/tail's old `-5c`), only the match (`grep -o`,
        `rg -o`), or a rewrite of it (`rg -r`). Asked whatever the input: its words
        cannot say whether that is a file's text."""
        what = None
        for v in options:
            if name == "cut" and (_long(v, ("--bytes", "--characters")) or set(_short_letters(v, "bcdf")) & {"b", "c"}):
                what = f"cut {v}"
            elif name in ("head", "tail") and (_long(v, ("--bytes",)) or "c" in _short_letters(v, "cn")
                                               or re.match(r"-[0-9]+[bkm]", v)):
                what = f"{name} {v}"
            elif name == "grep" and (_long(v, ("--only-matching",)) or "o" in _short_letters(v, _GREP_VALUE_LETTERS)):
                what = f"grep {v}"
            elif name == "rg" and (_long(v, ("--only-matching", "--replace"))
                                   or set(_short_letters(v, _RG_VALUE_LETTERS)) & {"o", "r"}):
                what = f"rg {v.split('=', 1)[0]}"
            elif name == "rg" and _long(v, ("--max-columns-preview",)):
                what = "rg --max-columns-preview"
            elif name == "diff" and (_long(v, ("--side-by-side", "--width")) or set(_short_letters(v, "CUDFILSWXx"))
                                     & {"y", "W"}):
                what = f"diff {v.split('=', 1)[0]}"
            if what:
                raise _Refuse(_R_SLICE.format(what=what))
        words = [w.value for w in args or []]
        if name in ("head", "tail"):
            for v in words:  # the obsolete `tail +5c` / `head -5c` forms, a word of their own
                if re.fullmatch(r"[+-][0-9]+[bckm]", v):
                    raise _Refuse(_R_SLICE.format(what=f"{name} {v}"))
        if name == "cut":
            # A field cut on a delimiter a key can hold (`-d-`, `-d_`) prints the key without its prefix.
            for k, v in enumerate(words):
                value = None
                if v == "-d" or v == "--delimiter":
                    value = words[k + 1] if k + 1 < len(words) else ""
                elif v.startswith("--delimiter="):
                    value = v.split("=", 1)[1]
                elif v.startswith("-d"):
                    value = v[2:]
                if value is not None and value not in (",", "\t", " ", ";", "|", "/"):
                    raise _Refuse(_R_SLICE.format(what=f"cut -d {value!r}"))

    def _reader(self, name: str, args: list[_Word], cands: list[str]) -> None:
        options = _options(args)
        text_options = _TEXT_OPTIONS.get(name, ())
        if name == "ls" and not _LINUX:
            # BSD ls (macOS) reads -I as a flag, so the word after it is a name it lists.
            text_options = tuple(o for o in text_options if o != "-I")
        self._slices(name, options, args)
        if name in ("gzip", "gunzip", "zcat"):
            self._gzip(name, options, args, cands)
        if name in ("wc", "sort") and any(_long(v, ("--files0-from",)) for v in options):
            raise _Refuse(f"`{name} --files0-from` reads a list of files the check never sees.")
        if name in _DIGESTS:
            flags, values, longs = _DIGESTS[name]
            for v in options:
                if v.startswith("+"):  # shasum's, and a wrapper's that runs it (`sha256sum` on a Mac)
                    what = "shasum" if name == "shasum" else f"{name} (when it runs shasum)"
                    raise _Refuse(f"{what} reads {v} as an option: `+c` is -c, which opens files the check never "
                                  "sees.")
                if not v.startswith("-") or v == "-":
                    continue
                letters = _short_letters(v, values)
                if "c" in letters or _long(v, ("--check",)):
                    raise _Refuse(f"{name} -c / --check opens every file a checksum file names, which the check never "
                                  "sees.")
                if not (_long(v, longs) if v.startswith("--") else set(letters) <= set(flags + values)):
                    raise _Refuse(f"`{name} {v.split('=', 1)[0]}` isn't on the safe list: of its options only the "
                                  "algorithm, the digest length, the read mode and the line style run at once.")
        if name == "du":
            for v in options:
                bad = _long(v, ("--exclude-from", "--files0-from", "--dereference", "--dereference-args", "--null"))
                if bad == "--exclude-from" and v.split("=", 1)[0] == "--exclude":
                    bad = None  # spelled out, a pattern; any shorter spelling could be either
                letters = _short_letters(v, _DU_VALUE_LETTERS)
                if bad in ("--exclude-from", "--files0-from") or "X" in letters:
                    raise _Refuse(f"du {bad or '-X'} reads names or patterns from a file the check never sees.")
                if bad in ("--dereference", "--dereference-args") or set(letters) & {"L", "H", "D"}:
                    raise _Refuse("du -L / -H / -D / --dereference follows symlinks out of the working folders.")
                if bad == "--null" or "0" in letters:
                    raise _Refuse("du -0 / --null prints its names NUL-separated on one line, past the line-based "
                                  "checks on its output.")
            self._listed("du", args, cands, text_options, _TREE)
        if name == "grep":
            for v in options:
                letters = _short_letters(v, _GREP_VALUE_LETTERS)
                if "R" in letters or _long(v, ("--dereference-recursive",)):
                    raise _Refuse("grep -R follows symlinks out of the working folders.")
                if "r" in letters or _long(v, ("--recursive",)):
                    raise _Refuse(_R_GREP_R)
            # `-d ACTION` / `--directories=ACTION`, attached or its own word: GNU grep takes
            # any unambiguous start of `recurse` (`-d rec`, `--dir rec`) and BSD's any case,
            # and with no name either walks the current folder. Only `read` and `skip` run.
            for k, w in enumerate(args):
                v, value = w.value, None
                if v == "--":
                    break
                if _long(v, ("--directories",)):
                    value = v.split("=", 1)[1] if "=" in v else None
                    value = value if value is not None else (args[k + 1].value if k + 1 < len(args) else "")
                elif v.startswith("-") and not v.startswith("--"):
                    letters = _short_letters(v, _GREP_VALUE_LETTERS)
                    if letters.endswith("d"):
                        value = v[1 + len(letters):] or (args[k + 1].value if k + 1 < len(args) else "")
                if value is not None and value not in ("read", "skip"):
                    raise _Refuse(_R_GREP_R)
        if name == "diff":
            for v in options:
                if "r" in _short_letters(v, "CUDFILSWXx") or _long(v, ("--recursive", "--new-file",
                                                                         "--unidirectional-new-file")) \
                        or "N" in _short_letters(v, "CUDFILSWXx"):
                    raise _Refuse("diff -r reads every file under a folder, keys included.")
                if "l" in _short_letters(v, "CUDFILSWXx") or _long(v, ("--paginate",)):
                    raise _Refuse("diff -l passes its output through `pr`, a program PATH picks.")
            for word in _positionals(args, _TEXT_OPTIONS["diff"]):
                path = _expand(word, self.home)
                if any(os.path.isdir(os.path.join(c, path)) for c in cands):
                    raise _Refuse(f"diff of the folder {word.value} reads every file in it.")
        if name == "ls":
            # A cluster is read whole: which letters take a value differs between GNU and BSD ls.
            letters = "".join(v[1:] for v in options if v.startswith("-") and not v.startswith("--"))
            recursive = "R" in letters or any(_long(v, ("--recursive",)) for v in options)
            if recursive and ("L" in letters or any(_long(v, ("--dereference",)) for v in options)):
                raise _Refuse("ls -R -L follows symlinks out of the working folders.")
            self._listed("ls", args, cands, text_options, _TREE if recursive else _NAMES)
        self._args(args, cands, text_options=text_options,
                   anywhere=_NAMES if name in ("du", "ls", "stat") else _FILES)

    def _listed(self, name: str, args: list[_Word], cands: list[str], text_options: Sequence[str],
                anywhere: str) -> None:
        """ls and du: every name they are given is a folder or file they read, so each
        is checked as a path (a value of an option the list doesn't know then lands in
        the current folder and is checked there); with none, they read the current
        folder. Given a word that may be an option's value instead, they read the
        current folder, so that is checked too: any word after an abbreviated option
        that takes a value (`ls -R --ig /tmp` is `--ignore=/tmp`; the word is still
        checked as a name as well: `du --time` takes none), and for a walk (`du`,
        `ls -R`) a word that names no folder here (`du --max 1`, `ls -R --sort size`)."""
        names = _positionals(args, text_options)
        for word in names:
            self._check_path(word.value, word.tilde, cands, anywhere=anywhere)
        longs = [o for o in text_options if o.startswith("--")]
        walked = any(v.startswith("--") and "=" not in v and v not in text_options and _long(v, longs)
                     for v in _options(args))
        # Read the other way too: a short cluster ending in a letter that takes a value
        # (`-RaI /tmp`: GNU's -I PATTERN) takes the next word, so no name may be left.
        left, skip, names_only = 0, False, False
        for w in args:
            v = w.value
            if skip or w.synthetic:
                skip = False
            elif names_only or v == "-" or not v.startswith("-"):
                left += 1
            elif v == "--":
                names_only = True
            elif v.startswith("--"):
                skip = "=" not in v and bool(_long(v, longs))
            else:
                skip = v[-1] in _LISTED_VALUE_LETTERS[name]
        walked = walked or not left
        if anywhere == _TREE and not walked:
            plain = [w.value for w in names if not w.tilde and not w.value.startswith("/")]
            walked = not all(os.path.isdir(os.path.join(c, v)) for v in plain for c in cands)
        if not names or walked:
            self._require_cwd(cands, name, anywhere=anywhere)

    def _gzip(self, name: str, options: list[str], args: list[_Word], cands: list[str]) -> None:
        """gzip, gunzip and zcat as readers only (`_GZIP_FLAGS`); and every name they
        are given must be a file: for one that isn't there, they read NAME.gz (or .z,
        .tgz...) in its place, a file the check never sees."""
        letters = ""
        for v in options:
            if not v.startswith("-") or v == "-":
                continue
            long = _long(v, tuple(_GZIP_LONGS)) if v.startswith("--") and "=" not in v else None
            if long:
                letters += _GZIP_LONGS[long]
            elif v.startswith("--") or not set(v[1:]) <= set(_GZIP_FLAGS):
                raise _Refuse(f"`{name} {v.split('=', 1)[0]}` isn't on the safe list: of its options only -c, -d, "
                              "-l, -t, -q and -v run at once.")
            else:
                letters += v[1:]
        reads = name == "zcat" or "l" in letters or "t" in letters or (
            "c" in letters and (name == "gunzip" or "d" in letters))
        if not reads:
            raise _Refuse(f"`{name}` runs at once only as a reader (gzip -cd, gunzip -c, -l, -t): this writes a file, "
                          "or compresses one into bytes the output scrubber can't read.")
        for word in _positionals(args, ()):
            path = _expand(word, self.home)
            if word.value != "-" and not all(os.path.isfile(os.path.join(c, path)) for c in cands):
                raise _Refuse(f"{name} {word.value}: it names no file here, so {name} would read {word.value}.gz or "
                              "another name in its place, which the check never sees.")
