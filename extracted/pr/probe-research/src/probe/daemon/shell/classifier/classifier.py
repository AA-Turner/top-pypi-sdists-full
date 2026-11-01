"""the checker: walk every part of a command, refuse or pass it, and hand each program to its rule."""

from __future__ import annotations
import os
import shutil
from pathlib import Path
from typing import Callable, Sequence
from ....foundation.compose.compose import compose
from probe.daemon.shell.classifier.never import NeverRulesMixin
from probe.daemon.shell.classifier.paths import PathRulesMixin
from probe.daemon.shell.classifier.refusals import _Fix, _Never, _R_HEREDOC, _R_SCRAMBLE, _Refuse
from probe.daemon.shell.classifier.rules.base64 import Base64RuleMixin
from probe.daemon.shell.classifier.rules.cd import CdRuleMixin
from probe.daemon.shell.classifier.rules.find import FindRuleMixin
from probe.daemon.shell.classifier.rules.git import GitRuleMixin
from probe.daemon.shell.classifier.rules.jq import JqRuleMixin
from probe.daemon.shell.classifier.rules.reader import ReaderRuleMixin
from probe.daemon.shell.classifier.rules.rg import RgRuleMixin
from probe.daemon.shell.classifier.rules.sed import SedRuleMixin
from probe.daemon.shell.classifier.rules.sort import SortRuleMixin
from probe.daemon.shell.classifier.rules.uniq import UniqRuleMixin
from probe.daemon.shell.classifier.writes import ProbeStepsMixin
from probe.daemon.shell.parse import (
    _ASSIGNMENT,
    _Op,
    _Part,
    _Word,
    _expand,
    _is_probe,
    _split,
    _tokenize,
    _walk,
)
from probe.daemon.shell.safe_lists import (
    _BUILTINS,
    _FILES,
    _HOME_SECRETS,
    _LINUX,
    _LINUX_ONLY,
    _NO_FILES,
    _READERS,
    _READ_ANYWHERE,
    _SPECIAL,
    _WRAPPERS,
    _moved_harness_files,
)
from probe.daemon.shell.verdict import Verdict
from probe.daemon.shell.words import _canon, _clean_path, _dashdash_as_value, _inside, _norm, _spellings


# --- the classifier --------------------------------------------------------


@compose
class _Checker(
    NeverRulesMixin,
    ProbeStepsMixin,
    PathRulesMixin,
    ReaderRuleMixin,
    GitRuleMixin,
    FindRuleMixin,
    RgRuleMixin,
    JqRuleMixin,
    SedRuleMixin,
    SortRuleMixin,
    UniqRuleMixin,
    Base64RuleMixin,
    CdRuleMixin,
):
    def __init__(
        self,
        *,
        workdirs: Sequence[Path],
        home: Path,
        cwd: Path,
        protected: Sequence[Path],
        write_dirs: Sequence[Path],
        read_dirs: Sequence[Path] = (),
        hidden: Callable[[str], bool] | None = None,
        inside_only: bool = False,
    ) -> None:
        #: A path a `.probe.config` sets to `off`: Probe never reads it, in any mode.
        self.hidden = hidden
        #: The daemon's reader: no read program reaches outside the working folders
        #: (and the places `_place` opens besides), as its `read` tool never did.
        self.inside_only = inside_only
        self.home = _norm(os.path.abspath(str(home)))
        self.home_real = os.path.realpath(self.home)
        self.cwd = os.path.realpath(str(cwd))
        homes = (self.home, self.home_real)
        self.roots: list[str] = []
        for folder in [*workdirs, cwd]:
            real = os.path.realpath(str(folder))
            # $HOME itself, and every folder above it, is never a working folder.
            if not any(_inside(h, real) for h in homes) and real not in self.roots:
                self.roots.append(real)
        self.write_dirs = [os.path.realpath(str(d)) for d in write_dirs]
        # Read-only folders: the Probe skills (the file reader's, and the `bash`
        # tool set's shell: `toolset`).
        self.read_dirs = [os.path.realpath(str(d)) for d in read_dirs]
        secrets = [os.path.join(h, name) for h in homes for name in _HOME_SECRETS]
        # Probe's config wherever it lives: $XDG_CONFIG_HOME, else ~/.config (the
        # CLI's own fallback), and an explicit PROBE_CONFIG_PATH.
        secrets.append(os.path.join(os.environ.get("XDG_CONFIG_HOME") or os.path.join(self.home, ".config"), "probe"))
        if os.environ.get("PROBE_CONFIG_PATH"):
            secrets.append(os.environ["PROBE_CONFIG_PATH"])
        secrets += [str(p) for p in protected]
        self.secret_prefixes = sorted(
            {v for p in secrets for v in (_norm(os.path.abspath(p)), os.path.realpath(p))}
        )
        # A read outside the working folders runs at once, so what it must not reach is
        # matched in one spelling (`_canon`), whatever spelling the command uses.
        self.protected_canon = sorted({_canon(p) for p in self.secret_prefixes})
        self.app_data = sorted({_canon(os.path.join(h, "Library")) for h in homes})
        #: What a walk for names outside the working folders must not go through, and how
        #: it is named: $HOME (its hidden folders, history, ~/Library) and the credential
        #: places wherever they are, in every spelling a folder above them may use
        #: (`_spellings`). A walk of / or /Users goes through $HOME.
        places = [*(("your home folder (~)", h) for h in homes), *((p, p) for p in self.secret_prefixes)]
        self.walk_private = [(form, shown) for shown, path in places for form in _spellings(path)]
        self.moved_harness_files = _moved_harness_files()

    # -- whole command --

    def classify(self, command: str, piped_input: bool = False) -> Verdict:
        if not command.strip():
            raise _Refuse("The command is empty.")
        if "\0" in command:
            raise _Refuse("The command contains a NUL byte.")
        self._never_bookkeeping(command)
        fed = self._probe_heredoc(command)
        if fed is not None:
            return fed
        try:
            note = self._note_write(command)
        except _Refuse as refusal:
            if not isinstance(refusal, (_Never, _Fix)):
                # A heredoc in a refused shape is asked about, and bypass mode runs
                # what is asked: the every-mode refusals first, over each piece as
                # bash runs it. They were skipped here, so a write to Probe's config
                # placed after a note's text ran in bypass mode (#2227).
                try:
                    self._never_heredoc(command)
                except _Never:
                    raise
                except _Refuse:
                    # Its pieces can't be read (`cat <<'EOF' |` ends the line on an
                    # operator): the whole command, as for any unreadable one.
                    self._never_raw(command)
            raise
        if note is not None:
            return note
        try:
            parts = _split(_tokenize(command))
        except _Refuse:
            # Too much bash to read (`$`, `&`, braces...), so asked about -- and bypass
            # mode runs what is asked: the every-mode refusals on its raw text first.
            self._never_raw(command)
            raise
        # The every-mode refusals first, over EVERY part: the checks below stop at
        # the first part they would ask about, and bypass mode runs what is asked.
        if any(op.op in ("<<", "<<-") for part in parts for op, _ in part.redirects):
            # A heredoc that is not on the first line (`echo hi` then `bash <<'EOF'`):
            # `_never` reads no further than its tag, and its body may be code bash
            # runs. Every allowed heredoc shape (`_note_write`, `_probe_heredoc`) puts
            # it on the first line, so this one is asked about -- and bypass mode runs
            # what is asked: the every-mode refusals over the whole raw text first.
            self._never_raw(command)
        self._never(parts)
        if any(_is_probe(p) for p in parts):
            if len(parts) == 1 and not parts[0].redirects:
                argv = [_expand(w, self.home) for w in parts[0].words[1:]]
                return Verdict(False, "probe command", probe_argv=argv)
            return Verdict(False, "probe commands among others", steps=self._steps(parts))
        carries = piped_input  # the previous command's output may hold a file's text
        for k, (part, cands) in enumerate(_walk(parts, self.cwd, self.home)):
            name = part.words[0].value if part.words else ""
            piped = part.before == "|" or (k == 0 and piped_input)
            fed = any(op.op == "<" for op, _ in part.redirects) or (piped and carries)
            if name == "tr" and fed:
                raise _Refuse(_R_SCRAMBLE.format(what="tr reading a file's text"))
            self._part(part, cands)
            carries = fed or name not in _NO_FILES
        return Verdict(True, "")

    # -- one command --

    def _part(self, part: _Part, cands: list[str]) -> None:
        name = part.words[0].value if part.words else ""
        for op, target in part.redirects:
            # What `<` opens is what the program reads: a read program's may be outside.
            self._redirect(op, target, cands, anywhere=_FILES if name in _READ_ANYWHERE else None)
        if not part.words:
            raise _Refuse("A redirect has no command in front of it.")
        args = part.words[1:]
        if _ASSIGNMENT.match(name):
            raise _Refuse(f"It sets an environment variable ({name.split('=')[0]}=...) first.")
        if "/" in name:
            raise _Refuse(
                f"`{name}` names a program by its path - only safe programs, by name, run at once."
            )
        if name in _WRAPPERS:
            raise _Refuse(f"`{name}` runs another command, so the check can't see what it does.")
        if name == "rev":
            raise _Refuse(_R_SCRAMBLE.format(what="rev"))
        linux_only = name in _LINUX_ONLY and _LINUX
        if not (name in _NO_FILES or name in _READERS or name in _SPECIAL or linux_only):
            raise _Refuse(f"`{name}` isn't on the safe list.")
        self._program(name)
        if name in _NO_FILES or name == "numfmt":
            return
        readings = [args]
        as_value = _dashdash_as_value(args)
        if as_value is not None:
            readings.append(as_value)
        for words in readings:
            if name in _READERS or name in ("tac", "zcat"):
                self._reader(name, words, cands)
            else:
                getattr(self, f"_{name}")(words, cands)

    def _program(self, name: str) -> None:
        if name in _BUILTINS:
            return
        found = shutil.which(name, path=_clean_path(os.environ.get("PATH")))
        if found:
            real = os.path.realpath(found)
            if any(_inside(real, root) for root in self.roots):
                raise _Refuse(
                    f"`{name}` is a program inside the working folders ({real})."
                )

    def _redirect(self, op: _Op, target: _Word, cands: list[str], *, anywhere: str | None = None) -> None:
        if op.op in (">", ">>", ">|", "&>", "&>>"):
            if target.value == "/dev/null" and not target.tilde:
                return
            raise _Refuse(f"It writes output to a file ({op.op} {target.value}).")
        if op.op == ">&":
            if target.value in ("1", "2"):
                return
            raise _Refuse(f"`>&{target.value}` sends output to a file - only 2>&1-style is allowed.")
        if op.op == "<":
            self._check_path(target.value, target.tilde, cands, anywhere=anywhere)
            return
        if op.op in ("<<", "<<-"):
            raise _Refuse(_R_HEREDOC)
        if op.op == "<<<":
            raise _Refuse("Here-strings (<<<) aren't allowed.")
        raise _Refuse(f"The redirect `{op.op}` isn't allowed.")
