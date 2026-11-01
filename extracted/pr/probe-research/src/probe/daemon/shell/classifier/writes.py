"""compound commands with probe steps, `probe draft edit` heredocs and the one allowed note write."""

from __future__ import annotations
import os
from probe.daemon.shell.bookkeeping import _fold, is_bookkeeping
from probe.daemon.shell.classifier.refusals import _Never, _R_HEREDOC, _Refuse
from probe.daemon.shell.parse import (
    PROBE_HEREDOC_SHAPES,
    PROBE_STDIN_COMMANDS,
    R_PROBE_HEREDOC,
    R_PROBE_HEREDOC_TAIL,
    _HEREDOC_TAG,
    _Op,
    _Part,
    _Word,
    _cd_word,
    _expand,
    _is_probe,
    _text,
    _tokenize,
)
from probe.daemon.shell.verdict import Step, Verdict
from probe.daemon.shell.words import _inside, _norm


class ProbeStepsMixin:
    """Part of _Checker: its methods run with `self` the _Checker; compose() folds them into _Checker."""

    def _steps(self, parts: list[_Part]) -> list[Step]:
        """A compound command with `probe` in it, as the pipelines its caller runs
        in order. Refused outright (every mode): a probe command that is not the
        first of its pipeline (it would read piped input) and a probe command
        redirected anywhere but `2>&1` / `2>/dev/null`."""
        pipelines: list[list[_Part]] = []
        for part in parts:
            if part.before == "|" and pipelines:
                pipelines[-1].append(part)
            else:
                pipelines.append([part])
        if any(op.op in ("<<", "<<-") for part in parts for op, _ in part.redirects):
            raise _Never("A heredoc can't go in a chained command with probe (its lines would run as commands).")
        steps = []
        for pipeline in pipelines:
            first = pipeline[0]
            before = ";" if first.before == "\n" else first.before
            if first.words and first.words[0].value == "cd" and (
                    len(pipeline) > 1 or first.redirects or _cd_word(first) is None):
                raise _Never("In a chained command, cd takes one folder and nothing else.")
            text = " | ".join(_text(p) for p in pipeline)
            if any(_is_probe(p) for p in pipeline[1:]):
                raise _Never("A probe command reads no piped input.")
            if _is_probe(first):
                stderr = "keep"
                for op, target in first.redirects:
                    if op.fd == "2" and op.op == ">&" and target.value == "1":
                        stderr = "merge"
                    elif op.fd == "2" and op.op == ">" and target.value == "/dev/null" and not target.tilde:
                        stderr = "drop"
                    else:
                        raise _Never("A probe command's output is never redirected to or from a file (only 2>&1 "
                                     "and 2>/dev/null).")
                steps.append(Step(before, text, probe_argv=[_expand(w, self.home) for w in first.words[1:]],
                                  filter=" | ".join(_text(p) for p in pipeline[1:]) or None, stderr=stderr))
                continue
            folder = _cd_word(first) if len(pipeline) == 1 and not first.redirects else None
            steps.append(Step(before, text, cd=_expand(folder, self.home) if folder is not None else None))
        return steps

    def _probe_heredoc(self, command: str) -> Verdict | None:
        """`probe draft edit PATH <<'TAG'` ... `TAG`, the whole command: the one
        probe command a heredoc may feed (`PROBE_STDIN_COMMANDS`). The daemon runs
        it itself, never bash, and hands it the body as stdin, so nothing in the
        body is ever read as a command. None for any other command; a refusal for
        a probe command fed in another shape (an unquoted tag, a pipe, text after
        the closing line) -- refused in EVERY mode (`_Never`): a refusal here comes
        before the every-mode checks (`_never_heredoc`, `_never_raw`), so a plain
        `_Refuse` would let bypass mode run the whole text with bash, whatever
        follows the closing line."""
        first, newline, body = command.partition("\n")
        if not newline or "<<" not in first:
            return None
        try:
            toks = _tokenize(first)
        except _Refuse:
            return None
        if not (toks and isinstance(toks[0], _Word) and toks[0].value == "probe"):
            return None
        words = [t.value for t in toks[1:] if isinstance(t, _Word)]
        which = tuple(words[:2])
        if which not in PROBE_STDIN_COMMANDS:
            return None
        if (len(toks) < 3 or not isinstance(toks[-2], _Op) or toks[-2].op not in ("<<", "<<-")
                or toks[-2].fd is not None or not isinstance(toks[-1], _Word)
                or any(isinstance(t, _Op) for t in toks[:-2])):
            raise _Never(R_PROBE_HEREDOC.format(shape=PROBE_HEREDOC_SHAPES[which]))
        op, tag = toks[-2].op, toks[-1]
        name = tag.value
        if not (_HEREDOC_TAG.fullmatch(name) and tag.raw in (f"'{name}'", f'"{name}"')):
            raise _Never("The heredoc's delimiter must be quoted (<<'EOF').")
        lines = body.split("\n")
        for k, line in enumerate(lines):
            if (line.lstrip("\t") if op == "<<-" else line) == name:
                if "\n".join(lines[k + 1 :]).strip():
                    raise _Never(R_PROBE_HEREDOC_TAIL.format(command=" ".join(which)))
                break
        else:
            raise _Never(f"The heredoc is never closed by a line reading {name}.")
        kept = lines[:k]
        if op == "<<-":
            kept = [line.lstrip("\t") for line in kept]
        argv = [_expand(t, self.home) for t in toks[1:-2] if isinstance(t, _Word)]
        return Verdict(False, "probe command", probe_argv=argv, probe_stdin="\n".join(kept) + ("\n" if k else ""))

    def _note_write(self, command: str) -> Verdict | None:
        """The one write allowed: `cat > FILE <<'TAG'` ... `TAG`, FILE inside write_dirs."""
        first, newline, body = command.partition("\n")
        if not newline or "<<" not in first:
            return None
        try:
            toks = _tokenize(first)
        except _Refuse:
            return None
        if not any(isinstance(t, _Op) and t.op in ("<<", "<<-") for t in toks):
            return None
        # A heredoc in any other shape is refused here, before its body is ever tokenized.
        if len(toks) != 5 or not (isinstance(toks[0], _Word) and toks[0].value == "cat"):
            raise _Refuse(_R_HEREDOC)
        target: _Word | None = None
        append = False
        heredoc: tuple[str, _Word] | None = None
        for op, word in ((toks[1], toks[2]), (toks[3], toks[4])):
            if not isinstance(op, _Op) or not isinstance(word, _Word) or op.fd is not None:
                raise _Refuse(_R_HEREDOC)
            if op.op in (">", ">>") and target is None:
                target, append = word, op.op == ">>"
            elif op.op in ("<<", "<<-") and heredoc is None:
                heredoc = (op.op, word)
            else:
                raise _Refuse(_R_HEREDOC)
        if target is None or heredoc is None:
            raise _Refuse(_R_HEREDOC)
        op, tag = heredoc
        name = tag.value
        if not (_HEREDOC_TAG.fullmatch(name) and tag.raw in (f"'{name}'", f'"{name}"')):
            raise _Refuse(
                "The heredoc's delimiter must be quoted (<<'EOF')."
            )
        lines = body.split("\n")
        for k, line in enumerate(lines):
            if (line.lstrip("\t") if op == "<<-" else line) == name:
                if "\n".join(lines[k + 1 :]).strip():
                    raise _Refuse(
                        "Something follows the heredoc - a note write must be the whole command."
                    )
                break
        else:
            raise _Refuse(f"The heredoc is never closed by a line reading {name}.")
        real = self._check_write(target)
        self._program("cat")  # the write runs `cat` through PATH like any other command
        text = "\n".join(lines[:k])
        if op == "<<-":
            text = "\n".join(line.lstrip("\t") for line in lines[:k])
        return Verdict(True, "", note_target=real, note_body=text + ("\n" if k else ""), note_append=append)

    def _check_write(self, word: _Word) -> str:
        shown = word.value
        joined = os.path.join(self.cwd, _expand(word, self.home))
        lex, real = _norm(joined), os.path.realpath(joined)
        if not self.write_dirs:
            raise _Refuse(f"It writes {shown}, and no folder is open for writing.")
        if self._protected(lex) or self._protected(real):
            raise _Never(f"It writes {shown}: Probe's own key or state, or a credential folder.")
        if self._secret(lex) or self._secret(real):
            raise _Refuse(f"It writes {shown}, which looks like a credential or Probe's key file.")
        if os.path.isdir(real) or not os.path.isdir(os.path.dirname(real)):
            raise _Refuse(f"It writes {shown}, which isn't a file in an existing folder.")
        inside = [d for d in self.write_dirs if _inside(_fold(real), _fold(d)) and _fold(real) != _fold(d)]
        if inside and (is_bookkeeping(os.path.basename(real)) or is_bookkeeping(os.path.basename(lex))):
            # Never, not Refuse: bypass mode approves a Refuse, and this one guards the erasure check.
            raise _Never(f"It writes {shown}: a checkout's base copy, version or lock, which only `probe` writes.")
        if not any(_inside(real, d) and real != d for d in self.write_dirs):
            # (On macOS and Windows a folder spelled in other case is the same folder:
            # its bookkeeping was refused just above, in every mode.)
            raise _Refuse(f"It writes {shown}, outside the folders open for writing.")
        if is_bookkeeping(os.path.basename(real)) or is_bookkeeping(os.path.basename(lex)):
            # Never, not Refuse: bypass mode approves a Refuse, and this one guards the erasure check.
            raise _Never(f"It writes {shown}: a checkout's base copy, version or lock, which only `probe` writes.")
        return real
