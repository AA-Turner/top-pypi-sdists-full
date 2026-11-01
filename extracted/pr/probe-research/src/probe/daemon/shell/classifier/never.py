"""the every-mode refusals no one can wave through (settings, bookkeeping, code text, protected writes)."""

from __future__ import annotations
import os
import re
from probe.daemon.shell.bookkeeping import _TOKENS, _could_be_bookkeeping, _fold, _unquoted
from probe.daemon.shell.classifier.refusals import _Never, _Refuse
from probe.daemon.shell.held import _SHELL_RUNNERS, _WRAPPER_VALUES, _runner
from probe.daemon.shell.parse import (
    PROBE_STDIN_COMMANDS,
    R_PROBE_HEREDOC_CHAINED,
    _ASSIGNMENT,
    _CODE_ARGS,
    _EMBEDDED_PROBE,
    _PROC_SELF,
    _Part,
    _is_probe,
    _never_setting,
    _split,
    _stderr_only,
    _text,
    _tokenize,
)
from probe.daemon.shell.safe_lists import _COPIES_ONLY_AFTER, _READERS, _WRAPPERS
from probe.daemon.shell.words import _inside


class NeverRulesMixin:
    """Part of _Checker: its methods run with `self` the _Checker; compose() folds them into _Checker."""

    def _never(self, parts: list[_Part], depth: int = 0) -> None:
        """What no mode runs, looked for in every part that is not a plain probe
        command: Probe's key or state named anywhere in it, and every way the
        shell could reach Probe with a key -- a probe started through another
        program (`env`, `timeout`, `xargs`, `sh -c`, `eval`, inline code), a
        Probe setting set or unset (`PROBE_CONFIG_PATH=...`, `env -u`, `unset`),
        and an environment wiped (`env -i`), which would drop the shell's
        key-less config. The shell has no Probe key on purpose: the daemon writes
        to Probe only through its probe tool."""
        for k, part in enumerate(parts):
            if _is_probe(part) and depth == 0:
                continue  # the probe tool's own path, with every check
            texts = [_text(part), *(w.value for w in part.words), *(t.value for _, t in part.redirects)]
            for form in self._protected_forms():
                if any(form in text for text in texts):
                    raise _Never(f"It names {form}: Probe's own key or state, or a credential folder.")
            self._never_words([w.value for w in part.words], depth)
            if any(op.op in ("<<", "<<-") for op, _ in part.redirects):
                # The lines after a heredoc are its text, not commands: read them as text.
                rest = " ".join(_text(p) for p in parts[k + 1 :])
                for form in self._protected_forms():
                    if form in rest:
                        raise _Never(f"It names {form}: Probe's own key or state, or a credential folder.")
                return

    def _never_bookkeeping(self, command: str) -> None:
        """No mode touches a checkout's bookkeeping (`_BOOKKEEPING`) in the
        folders open for writing: a command line naming one of those folders and
        such a file is refused before anything else reads it, so neither an
        unquoted heredoc nor bypass mode gets past it (`_check_write` alone sat
        behind the quoted-heredoc check). A heredoc's body is data, not read."""
        first = command.partition("\n")[0]
        text = _fold(_unquoted(first if "<<" in first else command))
        if not any(_could_be_bookkeeping(tok.rstrip("/").rsplit("/", 1)[-1]) for tok in _TOKENS.findall(text)):
            return
        forms: set[str] = set()
        for folder in self.write_dirs:
            forms.add(folder)
            for home in (self.home, self.home_real):
                if _inside(folder, home) and folder != home:
                    rel = os.path.relpath(folder, home)
                    forms |= {f"~/{rel}", f"$HOME/{rel}", f"${{HOME}}/{rel}"}
        cwd = _fold(os.path.realpath(self.cwd))
        if (any(_fold(form) in text for form in forms)
                or any(_inside(cwd, _fold(d)) for d in self.write_dirs)):
            raise _Never("It names a checkout's base copy, version or lock in Probe's notes or summaries, which "
                         "only `probe` writes.")

    def _never_heredoc(self, command: str) -> None:
        """The every-mode refusals for a heredoc `_note_write` refused, piece by
        piece as bash runs it. Its first line and the lines after the closing one
        are commands. The body is data only when a quoted tag feeds it to a lone
        `cat` or `tee` (bash expands nothing; the program only copies it) AND no
        line after it can run the file it wrote (`_COPIES_ONLY_AFTER`); code
        otherwise: `bash <<'EOF'`, `cat <<'EOF' | sh`, `... EOF` then `. ./x.sh`,
        or an unquoted tag, which runs its `$(...)`. Reading a note's text as
        commands would refuse ordinary prose ("env", PROBE_RUN_ID) for a reason
        that is not the daemon's mistake."""
        first, _, rest = command.partition("\n")
        parts = _split(_tokenize(first))  # `_note_write` read this line already
        for part in parts:  # one by one: `_never` stops reading at a heredoc
            if _is_probe(part):  # as the steps path refuses it: its lines would run as commands
                which = tuple(w.value for w in part.words[1:3])
                if which in PROBE_STDIN_COMMANDS:
                    raise _Never(R_PROBE_HEREDOC_CHAINED.format(command=" ".join(which)))
                raise _Never("A heredoc can't go in a chained command with probe (its lines would run as commands).")
            self._never([part])
        found = next(((op, tag) for part in parts for op, tag in part.redirects if op.op in ("<<", "<<-")), None)
        if found is None:
            self._never_raw(command)
            return
        op, tag = found
        lines = rest.split("\n")
        body, tail = lines, []
        for k, line in enumerate(lines):
            if (line.lstrip("\t") if op.op == "<<-" else line) == tag.value:
                body, tail = lines[:k], lines[k + 1 :]
                break
        copies_only = True  # nothing after the closing line runs a file
        if "\n".join(tail).strip():
            try:
                tail_parts = _split(_tokenize("\n".join(tail)))
            except _Never:
                raise
            except _Refuse:
                self._never_raw("\n".join(tail))
                copies_only = False
            else:
                self._never(tail_parts)
                copies_only = all(
                    part.words and all(_stderr_only(op, target) for op, target in part.redirects)
                    and (_is_probe(part) or part.words[0].value in _COPIES_ONLY_AFTER)
                    for part in tail_parts
                )
        program = parts[0].words[0].value if len(parts) == 1 and parts[0].words else ""
        quoted = tag.raw in (f"'{tag.value}'", f'"{tag.value}"')
        if not (quoted and copies_only and os.path.basename(program) in ("cat", "tee")):
            self._never_code("\n".join(body), 1)
        if not copies_only:
            # A line after it may run the file the heredoc wrote (`. ./x.sh`), and
            # the body alone may not name probe (`unset ${v}_CONFIG_PATH`) while
            # a plain probe after it does: read as one script, which it is.
            self._never_raw(command)

    def _never_raw(self, command: str) -> None:
        """The every-mode refusals for a command too complex to read word by word:
        Probe's key or state named anywhere, a Probe setting, `env -i`, and `probe`
        anywhere as a word (a probe command runs only as a command of its own,
        which is always readable)."""
        bare = re.sub(r"[\"'\\]", "", command)
        for form in self._protected_forms():
            if form in command or form in bare:
                raise _Never(f"It names {form}: Probe's own key or state, or a credential folder.")
        setting = re.search(r"\bPROBE_[A-Z0-9_]+", bare)
        if setting:
            raise _Never(f"It names {setting.group(0)}, Probe's own setting. The shell has no Probe key - Probe "
                         "writes go through `probe`.")
        if re.search(r"(?<![\w.-])env\s+(\S+\s+)*?(-[0v]*i\w*|--ignore-environment|-)(\s|$)", bare):
            raise _Never("`env -i` wipes the environment, and with it the shell's key-less Probe config.")
        if re.search(r"(?<![\w./-])probe(?![\w./-])", bare):
            raise _Never("A command the check can't read names probe.")

    def _protected_forms(self) -> list[str]:
        """Probe's key/state and the credential folders as a command can write them."""
        forms: list[str] = []
        for prefix in self.secret_prefixes:
            forms.append(prefix)
            for home in (self.home, self.home_real):
                if _inside(prefix, home) and prefix != home:
                    rel = os.path.relpath(prefix, home)
                    forms += [f"~/{rel}", f"$HOME/{rel}", f"${{HOME}}/{rel}"]
            if _inside(prefix, self.cwd) and prefix != self.cwd:
                forms.append(os.path.relpath(prefix, self.cwd))
        return sorted(set(forms), key=len, reverse=True)

    def _never_code(self, code: str, depth: int) -> None:
        """Command text another program runs (`bash -c`, `eval`, `env -S`)."""
        try:
            parts = _split(_tokenize(code))
        except _Refuse:
            self._never_raw(code)
            return
        self._never(parts, depth)

    def _never_words(self, words: list[str], depth: int) -> None:
        program0 = next((os.path.basename(w) for w in words if not _ASSIGNMENT.match(w)), "")
        # Text only a text tool reads (a search pattern, a file to print) may name
        # anything; every other program's words may be code it runs.
        text_tool = program0 in _READERS or program0 in ("rg", "jq", "sort", "uniq", "echo")
        for word in words:
            if _PROC_SELF.search(word):
                raise _Never(f"It names {_PROC_SELF.search(word).group(0)}, a path the check can't follow.")
            if not text_tool:
                if "PROBE_" in word:
                    raise _Never("It names a Probe setting (PROBE_...) for another program. The shell has no Probe "
                                 "key.")
                if program0 in _CODE_ARGS and word != words[0] and _EMBEDDED_PROBE.search(word):
                    raise _Never("This command hands a probe command line to another program.")
        if program0 == "find":  # -exec / -execdir / -ok / -okdir run the words up to `;` or `+`
            for k, word in enumerate(words):
                if word in ("-exec", "-execdir", "-ok", "-okdir") and depth < 3:
                    end = next((j for j in range(k + 1, len(words)) if words[j] in (";", "+", "\\;")), len(words))
                    run = words[k + 1 : end]
                    if run and os.path.basename(run[0]) == "probe":
                        raise _Never("find -exec starts probe.")
                    self._never_words(run, depth + 1)
        k = 0
        via: str | None = None
        while k < len(words) and _ASSIGNMENT.match(words[k]):
            _never_setting(words[k].split("=", 1)[0].rstrip("+"))
            k += 1
        while k < len(words) and os.path.basename(words[k]) in _WRAPPERS:
            via = os.path.basename(words[k])
            rest = words[k + 1 :]
            if via == "eval" or via in _SHELL_RUNNERS:
                if via == "eval":
                    code = rest
                else:  # the word after -c (or a cluster holding c: -lc, -ec)
                    at = next((i for i, w in enumerate(rest) if re.fullmatch(r"-[A-Za-z]*c[A-Za-z]*", w)), None)
                    code = rest[at + 1 : at + 2] if at is not None else []
                if code and depth < 3:
                    self._never_code(" ".join(code), depth + 1)
                return
            k += 1
            while k < len(words) and (words[k].startswith(("-", "+")) or _ASSIGNMENT.match(words[k])
                                      or re.fullmatch(r"[0-9.]+[smhd]?", words[k])):
                flag = words[k]
                if _ASSIGNMENT.match(flag):
                    _never_setting(flag.split("=", 1)[0].rstrip("+"))
                elif via == "env" and (flag in ("-", "--ignore-environment")
                                       or re.fullmatch(r"-[0v]*i[0-9A-Za-z]*", flag)):
                    raise _Never("`env -i` wipes the environment, and with it the shell's key-less Probe config.")
                elif via == "env" and flag.startswith(("-u", "--unset")):
                    named = flag.split("=", 1)[1] if "=" in flag else flag[2:] if flag.startswith("-u") else ""
                    named = named or (words[k + 1] if k + 1 < len(words) else "")
                    _never_setting(named)
                elif via == "env" and flag in ("-S", "--split-string") and k + 1 < len(words) and depth < 3:
                    self._never_code(words[k + 1], depth + 1)
                k += 2 if flag in _WRAPPER_VALUES else 1
        if k >= len(words):
            return
        program = os.path.basename(words[k])
        rest = words[k + 1 :]
        if program in ("unset", "export", "declare", "typeset", "readonly", "local"):
            for word in rest:
                _never_setting(word.split("=", 1)[0].rstrip("+"))
            return
        if program == "probe" and (via or depth):
            raise _Never(f"`probe` runs only as a command of its own, never through `{via or 'a shell'}`.")
        family = _runner(program)
        if family in ("python", "perl", "node", "ruby"):
            code = " ".join(rest)
            if "PROBE_" in code or re.search(r"""["']probe["']""", code):
                raise _Never(f"Its {program} code starts probe or touches a Probe setting.")
