"""may this path be read: protected, secret, private, hidden, outside the working folders, one ordinary file."""

from __future__ import annotations
import os
import stat
from typing import Sequence
from probe.daemon.shell.bookkeeping import packaged_file
from probe.daemon.shell.classifier.refusals import _Never, _Refuse
from probe.daemon.shell.held import _PATH_PIECES, _held_commands, _held_dirs, _held_resolve, _tree_read
from probe.daemon.shell.parse import _Word
from probe.daemon.shell.safe_lists import (
    _HARNESS_FILES,
    _HISTORY_NAMES,
    _NAMES,
    _SECRET_NAMES,
    _SYSTEM_PRIVATE,
    _TREE,
)
from probe.daemon.shell.words import _canon, _hidden, _inside, _norm
_OUTSIDE = "outside the working folders"


class PathRulesMixin:
    """Part of _Checker: its methods run with `self` the _Checker; compose() folds them into _Checker."""

    # -- paths --

    def _protected(self, path: str) -> bool:
        """Inside Probe's config, the daemon's state, or a home credential folder, in
        any spelling (`_canon`)."""
        canon = _canon(path)
        return any(_inside(canon, prefix) for prefix in self.protected_canon)

    def _secret(self, path: str) -> bool:
        if self._protected(path) or self._private(path):
            return True
        # In any case: macOS's disks read client.PEM as client.pem.
        name = os.path.basename(path).casefold()
        return (
            name.startswith((".env", "id_"))
            or name.endswith((".pem", ".key"))
            or name in _SECRET_NAMES
        )

    def _private(self, path: str) -> str | None:
        """What is private like a credential wherever it is, as a clause, else None:
        shell and REPL history, and `_SYSTEM_PRIVATE`'s places, in any spelling."""
        canon = _canon(path)
        if os.path.basename(canon) in _HISTORY_NAMES:
            return "shell or REPL history, which keeps the passwords and keys typed into it"
        return next((what for place, what in _SYSTEM_PRIVATE if _inside(canon, place)), None)

    def names_private(self, command: str) -> bool:
        """Is `command` a read Jev can't judge (`Verdict.private`)? A word of it,
        or a path-shaped piece of one, lands in a hidden file or folder (below a
        working folder when inside one, from `/` when not; the coding agent's
        instruction files excepted), or it reads a whole tree's contents (`rg`,
        `grep -r`, `diff -r`). True when the command can't be read word by word."""
        commands = _held_commands(command)
        if commands is None:
            return True
        dirs = _held_dirs(commands, self.cwd, self.home)
        for c in commands:
            if _tree_read(c.words):
                return True
            for word in [*c.words, *c.stdin, *c.targets]:
                for piece in {word, *_PATH_PIECES.split(word)}:
                    # Only what exists: a piece of code (`.read()` in `python3 -c`) is no path.
                    if piece and any(self._in_hidden(real) and os.path.lexists(real)
                                     for real in _held_resolve(piece, dirs, self.home)):
                        return True
        return False

    def _in_hidden(self, real: str) -> bool:
        if self._harness(real):
            return False
        root = next((r for r in self.roots if _inside(real, r)), "")
        comps = [c for c in real[len(root):].split("/") if c]
        return any(c.startswith(".") for c in comps)

    def names_credential(self, command: str) -> bool:
        """Does any word of `command`, or a path-shaped piece of one
        (`open('.env')`, `--key=id_rsa`), name a credential-shaped file
        (`_secret`: `.env*`, `id_*`, `*.pem`, `*.key`, `.netrc`..., a home
        credential folder, Probe's key and state), in any folder a `cd` may
        reach? Every word, not only the one the checks stopped at: `cat
        outside.txt .env` is asked about `outside.txt`. True when the command
        can't be read word by word."""
        commands = _held_commands(command)
        if commands is None:
            return True
        dirs = _held_dirs(commands, self.cwd, self.home)
        for c in commands:
            for word in [*c.words, *c.stdin, *c.targets]:
                for piece in {word, *_PATH_PIECES.split(word)}:
                    if piece and any(self._secret(real) for real in _held_resolve(piece, dirs, self.home)):
                        return True
        return False

    def _harness(self, real: str) -> bool:
        """The coding agent's own instructions and memory, read-only (S7)."""
        if real in self.moved_harness_files:
            return True
        if not real.startswith(self.home_real + "/"):
            return False
        rel = real[len(self.home_real) + 1 :].split("/")
        if rel in _HARNESS_FILES:
            return True
        if rel[:2] == [".claude", "skills"]:
            rest = rel[2:]
        elif len(rel) >= 4 and rel[:2] == [".claude", "projects"] and rel[3] == "memory":
            rest = rel[4:]
        else:
            return False
        return not any(comp.startswith(".") for comp in rest)

    def _place(self, real: str, anywhere: str | None = None) -> str | None:
        """None when `real` may be read; else how it fails, as a clause. `anywhere`: a
        read program's reach outside the working folders (`_outside`)."""
        if self._harness(real):
            return None
        if any(_inside(real, d) for d in self.write_dirs):
            return None  # the checked-out Probe notes: the daemon reads what it writes
        if any(_inside(real, d) for d in self.read_dirs):
            return None
        hidden = None
        for root in self.roots:
            if not _inside(real, root):
                continue
            comps = [c for c in real[len(root) :].split("/") if c]
            bad = _hidden(comps, real)
            if bad is None:
                return None
            hidden = bad
        if hidden:
            return f"inside a hidden folder ({hidden})"
        return _OUTSIDE if anywhere is None or self.inside_only else self._outside(real, anywhere)

    def _outside(self, real: str, anywhere: str) -> str | None:
        """A read program's read outside the working folders: None when it runs at
        once; else how it fails, as a clause. Hidden names and macOS's app data ask
        wherever they are out here, and a walk for names asks when it would go
        through $HOME or a credential place. (What a content read reads is
        `_content`'s.)"""
        hidden = next((comp for comp in real.split("/") if comp.startswith(".")), None)
        if hidden:
            return f"{_OUTSIDE}, and {hidden} is hidden"
        canon = _canon(real)
        if any(_inside(canon, place) for place in self.app_data):
            return "macOS app data (~/Library: cookies, mail, messages, keychains)"
        if anywhere == _TREE and os.path.isdir(real):
            folded = real.casefold()
            through = next((shown for place, shown in self.walk_private
                            if _inside(place, folded) or _inside(place, canon)), None)
            if through:
                return f"{_OUTSIDE}, and a walk of it goes through {through}"
        return None

    def _content(self, real: str, outside: bool) -> str | None:
        """A file a content read names must be one ordinary file with one name,
        inside the working folders too (what a walk reaches is not checked here):
        a pipe or socket waits for what someone writes (or is a device), and a
        second name (a hard link: realpath can't see that ~/.ssh/id_rsa is it) may
        be a credential's. Outside them, a folder would be read whole and a name
        nothing is at can't be checked either. None when it may be read; else how
        it fails, as a clause."""
        try:
            st = os.stat(real)
        except OSError:
            return f"{_OUTSIDE}, and no file there can be checked" if outside else None
        if stat.S_ISDIR(st.st_mode):
            return f"a folder {_OUTSIDE}, and every file in it would be read" if outside else None
        if not stat.S_ISREG(st.st_mode):
            return "not an ordinary file (a pipe, a socket or a device)"
        if st.st_nlink > 1 and not (any(_inside(real, d) for d in self.read_dirs) and packaged_file(real)):
            # Not a file the installed package put in the read-only folders (the
            # Probe skills): an installer that links from its cache (uv) gives each
            # a second name there, and its RECORD names it with its hash.
            return f"the file has {st.st_nlink} names (hard links): another may be a credential's"
        return None

    def _check_path(
        self,
        text: str,
        tilde: bool,
        cands: list[str],
        *,
        logical: bool = False,
        verb: str = "It reads",
        anywhere: str | None = None,
    ) -> None:
        path = self.home + text[1:] if tilde else text
        for cand in cands:
            joined = os.path.join(cand, path)
            lex = _norm(joined)
            reals = {os.path.realpath(joined)}
            if logical:  # `cd` goes to the logical path when it can
                reals.add(os.path.realpath(lex))
            for real in sorted(reals):
                if self._protected(lex) or self._protected(real):
                    raise _Never(f"{verb} {text}: Probe's own key or state, or a credential folder.")
                if self.hidden is not None and (self.hidden(lex) or self.hidden(real)):
                    raise _Never(f"{verb} {text}: a .probe.config sets it to off, so Probe never reads it.")
                # Both spellings: /dev/stdin resolves in THIS process, bash's is the command's.
                private = self._private(lex) or self._private(real)
                if private:
                    raise _Refuse(f"{verb} {text}: {private}.")
                if self._secret(lex) or self._secret(real):
                    raise _Refuse(
                        f"{verb} {text}, which looks like a credential or Probe's key file."
                    )
                problem = self._place(real, anywhere)
                if problem is None and anywhere not in (_NAMES, _TREE):  # what it reads is the file's text
                    problem = self._content(real, outside=self._place(real) is not None)
                if problem:
                    raise _Refuse(f"{verb} {text}: {problem}.")

    def _maybe_path(self, text: str, tilde: bool, cands: list[str], anywhere: str | None = None) -> None:
        """Check `text` if it could name a file."""
        if not text:
            return
        if (
            tilde
            or "/" in text
            or text[0] in ".~"
            or any(os.path.lexists(os.path.join(c, text)) for c in cands)
        ):
            self._check_path(text, tilde, cands, anywhere=anywhere)

    def _args(
        self,
        words: Sequence[_Word],
        cands: list[str],
        *,
        text_options: Sequence[str] = (),
        word_options: Sequence[str] = (),
        anywhere: str | None = None,
    ) -> None:
        """Check every argument that could name a file a reader opens (`anywhere`: as
        far as `_check_path` lets it reach outside the working folders)."""
        skip_next = False
        names_only = False  # after `--`
        for w in words:
            v = w.value
            if skip_next:
                skip_next = False
                continue
            if names_only or v == "-" or not v.startswith("-"):
                if v != "-":
                    self._maybe_path(v, w.tilde, cands, anywhere)
                continue
            if v == "--":
                names_only = True
                continue
            if v in word_options:
                skip_next = True
                continue
            if v.startswith("--"):
                name, eq, value = v.partition("=")
                if name in text_options:
                    skip_next = not eq
                    continue
                if eq:
                    self._maybe_path(value, False, cands, anywhere)
            else:
                if v[:2] in text_options:
                    skip_next = len(v) == 2
                    continue
                for k in range(2, len(v)):  # a value attached to a short option: -fFILE
                    self._maybe_path(v[k:], False, cands, anywhere)
            # A tool that stops reading options early would open the word itself.
            self._maybe_path(v, False, cands, anywhere)

    def _require_cwd(self, cands: list[str], what: str, *, anywhere: str | None = None) -> None:
        """`what` (ls, rg, git...) reads the current folder: it must be a working folder,
        or for ls, du and find (`anywhere`) a folder they could be given by name."""
        for cand in cands:
            real = os.path.realpath(cand)
            if self._protected(real):
                raise _Never(f"It reads the current folder {cand}: Probe's own key or state, or a credential folder.")
            problem = self._private(_norm(cand)) or self._private(real)
            problem = problem or ("a credential folder" if self._secret(real) else None)
            problem = problem or self._place(real, anywhere)
            if problem:
                raise _Refuse(f"It reads the current folder {cand}: {problem}.")
