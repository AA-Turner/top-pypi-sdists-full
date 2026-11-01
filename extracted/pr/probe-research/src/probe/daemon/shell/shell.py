# Portions of this module (the known-safe command list and the rules for `find`,
# `rg`, `sed`, `base64`) are a Python port of OpenAI's Codex CLI, and
# agent/tests/test_daemon_shell.py ports that file's unit tests:
#     openai/codex  codex-rs/shell-command/src/command_safety/is_safe_command.rs
#     at 9ca99b51713066681cce211184c0ff9035496979, the parent of 942af8447
#     (2026-08-19), the commit that retired the file.
# Copyright OpenAI. Licensed under the Apache License, Version 2.0; you may not
# use those portions except in compliance with the License. You may obtain a copy
# at http://www.apache.org/licenses/LICENSE-2.0. Changes from the original are
# listed in the module docstring under "Where this differs from Codex".
"""The daemon's shell (daemon v2, D15 / S9 / E6): what runs at once, and how it runs.

The daemon gets a real `shell(command)` tool. Before anything runs, `classify`
reads the command as text, in plain code, and returns a `Verdict`:

    safe          every piece is on the safe list with allowed options, and every
                  file it names may be read (Files, below): it runs at once
    not safe      anything else: the caller asks the researcher, showing `reason`
    probe_argv    the whole command is one `probe ...` call: the caller sends it to
                  the checks every `probe` command gets; it is never run from here
    steps         several commands, some of them `probe ...` calls (`cd x && probe
                  ...`, `probe run list | jq ...`): the caller runs them in order
                  itself (`Step`), each probe command through those checks and each
                  other part classified and run (or asked about) on its own. Bash
                  never sees a probe command; and the environment `run` gives a
                  command has no Probe config, so a `probe` it starts has no key.

The safe list, from Codex CLI (header above): cat cd cut echo expr false grep head
id ls nl paste pwd seq stat tail tr true uname uniq wc which whoami, plus
numfmt and tac on Linux; `diff` (not recursive); `find` without -exec -execdir -ok -okdir -delete -fls
-fprint -fprint0 -fprintf; `rg` without --pre --hostname-bin --search-zip -z;
`sed -n Np` / `sed -n M,Np` only; `base64 -d` without -o / --output. Ours: `sort`
without output, temp-folder or helper-program options; `jq` without file-reading
options (--rawfile --slurpfile -f/--from-file -L/--library-path, import/include);
git read verbs: status, log, diff, show, blame, `branch --show-current`,
rev-parse, ls-files. The digest programs (shasum sha1sum sha224sum sha256sum
sha384sum sha512sum md5sum b2sum cksum) with only the options that pick the
algorithm, the digest length, the read mode and the line style: anything else
asks, -c / --check first (it opens every file a checksum file names, which the
check never sees), and so does a word starting with + (shasum, a Perl script,
reads `+c` as -c).
`du` without --files0-from, -X / --exclude-from (they read a file), -L -H -D
--dereference (they follow symlinks out of the folders) or -0 / --null.
`gzip` and `gunzip` as readers only, with only the options their list holds:
`gzip -cd` / `gunzip -c` print what they decompress, -l lists, -t tests; a bare
gzip or gunzip writes a file, `gzip -c` alone compresses (bytes the output
scrubber can't read), -r reads a whole tree, and a name that is not a file asks
(gzip would read NAME.gz in its place). `zcat`, the same reader, on Linux only:
macOS's adds .Z to every name it is given.

How a command is read:
- It is split on |, &&, ||, ; and newlines, and every piece must pass.
- Refused anywhere: `$` outside single quotes (variables, $(...), $((...))),
  backticks, parentheses (subshells, process substitution), a background `&`,
  unquoted * ? [ (a glob could expand to a path the check never saw), an unquoted
  { or } anywhere but the whole word `{}` (a brace expands to other paths),
  `#` comments, `X=1 cmd`, wrappers that run another command (bash -c, env, sudo,
  xargs, nohup, timeout, ...), a program named by its path (./cat, /bin/cat), and
  a name that PATH resolves to a program inside the working folders.
- Redirects: `2>&1`-style and `> /dev/null` only; `< file` is checked as a
  file the program reads. Other writes, heredocs and here-strings are refused,
  except one form for editing checked-out Probe notes: the whole command is
  `cat > FILE <<'TAG'` (or >>, <<-, "TAG") with a QUOTED delimiter, so bash
  expands nothing in the body, and FILE inside `write_dirs`. The body is data;
  it is never read as commands.

Files. Every argument that could name a file (it has a /, starts with . or ~,
names something that exists, or is an option's attached value) is resolved the
way the kernel would (~, the current folder, `cd`, symlinks followed), and is
read without a question where:
- it lands inside a working folder or the starting folder ($HOME, and any
  folder above it, never counts as one); or
- the program is a READ program (cat head tail nl wc stat ls find du diff grep
  rg cut paste sort uniq tr tac numfmt jq, the digests, gzip / gunzip / zcat as
  readers, and `cd` to a folder they then read), anywhere on the machine, with
  these exceptions outside the working folders, which ask: a hidden file or
  folder (any part of its path starting with .); ~/Library, macOS's app data
  (cookies, mail, messages, keychains); for a content reader, a folder
  (`rg x DIR`, `cat DIR`: every file in it read) and a name nothing is at;
  and a walk for names (`find`, `du`, `ls -R`) of a folder that holds $HOME
  or a credential place (`find ~`, `du -sh /`). Names and metadata of any
  other tree run (`ls`, `find`, `du`). Commands that read the current folder
  by themselves follow the same rules: `ls`, `du` and `find` with no name read
  it as if named (and when a word may be an option's value instead: `ls -R
  --ig /tmp`, `ls -RaI /tmp` walk it), while `rg` with no path and git need it
  inside.
Anywhere, inside the working folders too, a file a content read NAMES (an
argument or a `<`) must be an ordinary file with one name: a pipe, socket or
device asks, and so does a file with a second name (a hard link, which
realpath can't see through to ~/.ssh/id_rsa). A pnpm or uv tree hard-linked
from a store into a repository therefore asks for a read of a named file's
text: accepted friction. The files a search walks to inside the working
folders (`rg KEY nested`) are not checked one by one.
Never read at once, even inside (Probe's key and state, the home credential
folders and `off` paths are refused in every mode; the rest asks):
credential-shaped paths (~/.ssh ~/.aws ~/.gnupg ~/.config/gcloud ~/.kube
~/.docker ~/.netrc ~/.pgpass ~/.git-credentials, Probe's config and key files,
anything in `protected`, .env* files, *.pem, *.key, id_*, in any case),
shell and REPL history (.zsh_history .bash_history .sh_history .python_history
.node_repl_history .psql_history .mysql_history .sqlite_history .lesshst
.viminfo), /proc (a process's environment, command line, memory, open files;
the kernel's), /sys, /dev, a container's secrets (/run/secrets), a user's
runtime files (/run/user), /etc/shadow, /etc/gshadow and /etc/ssh, a path a
`.probe.config` sets `off`, and hidden folders. The one exception is the
coding agent's own instructions and memory, read-only: ~/.claude/CLAUDE.md,
~/.claude/projects/*/memory/**, ~/.claude/skills/**, ~/.codex/AGENTS.md,
~/.pi/agent/AGENTS.md, and CLAUDE.md / CLAUDE.local.md / AGENTS.md anywhere in
the working folders. The checked-out Probe notes (`write_dirs`) may be read
too, by any reader. Every place here is matched in every spelling macOS gives
it: any case (its disks ignore it, and realpath keeps a name as written),
/System/Volumes/Data/... (the data volume's firmlink) and /private/etc,
/private/var, /private/tmp.
Not covered, by design of a check that reads a command's text before bash runs
it: a bind mount of a private place, a second path to it no check here can
see; a hard link to a key that a folder walk inside the working folders
reaches (`rg KEY nested` over `nested/k`, a second name of ~/.ssh/id_rsa: only
named files are stat-ed); and a swap between the check and the open (a file
replaced by a symlink to a key after its stat), since there is no checked file
descriptor to hand bash.

Recursive readers. `grep -r` and `diff -r` read every file below a folder, keys
and .env files included, so they ask; `rg` without -u / --no-ignore skips hidden
and ignored files, and is the way to search a tree. git can print a file's
contents from history: a `REV:path` and a pathspec whose name is a credential's
or a hidden file's ask as well.

git. Codex took git off its list because a repository's own settings can make a
read run programs. We keep the read verbs and take those programs away twice:
the classifier requires `--no-textconv --no-ext-diff` on log / show / diff (and
`--no-textconv` on blame), refuses -c, --output, --no-index, --ext-diff,
--textconv, --show-signature, and a repository that starts outside the working
folders; `run` gives git a config that turns hooks, fsmonitor, the pager,
external diff, ssh, every network protocol, signature checks and submodule
recursion off, and blanks every filter / diff driver program the repository
defines (a clean filter runs during `git status`).

`run` executes a command with `/bin/bash --noprofile --norc`, a minimal
environment (no Probe token, no API keys: nothing from the parent but PATH and
HOME), a time limit that kills the whole process group, and an output cap that
keeps the head and the tail.

Where this differs from Codex:
- git read verbs are allowed (Codex: never), hardened as above.
- `grep -R`, `rg -L/--follow`, `find -L/-follow` and `ls -R` with -L /
  --dereference are refused: they follow symlinks out of the working folders.
  find's start folders are read past its leading options and a `--` (GNU's
  -H -P -D -O, BSD's -E -X -d -s -x and `-f PATH`, in clusters as macOS reads
  them), and each is checked as a walk.
  `rg --hidden`/`-.`/`-u`/`--no-ignore` are refused: they read hidden or
  ignored files (.env, keys), which `cat` may not.
  `grep -r` is refused (use rg). `find -files0-from` is refused.
- `uniq IN OUT` is refused: the second name is an output file uniq writes.
- `sed -n Np` with an option in the file slot (`sed -n 1p -ewFILE`) is refused:
  `-e` turns `w` into a write.
- A program named by its path is refused; Codex looked only at the basename,
  so `./cat` (any script called cat) passed.
- Codex unwrapped `bash -lc SCRIPT`; our tool receives SCRIPT itself, so the
  wrappers are refused and SCRIPT is what gets checked.
- File arguments are checked (Codex relied on its sandbox for that): inside the
  working folders, or for a read program anywhere but the places that ask or
  are never read (Files, above). Short-option clusters are read (`rg -nz`), and
  long options match GNU-style abbreviations (`--out=` is `--output=`).
- `2>&1`, `> /dev/null`, and `< file` are allowed (a file outside the folders
  only into a read program); Codex refused every redirect.
- `base64` only decodes: encoding turns a file's text (a key in it included)
  into characters the output scrubber cannot recognise. (`xxd`, `od`, `hexdump`
  were never on the list.) For the same reason `rev` asks, `tr` asks when what
  it reads may come from a file (a `<`, or a pipe from anything but `echo`-like
  programs), and so does a jq program using @base64 @base32 @uri @sh, format()
  or explode. Printing text in PIECES hides a key the same way, so these ask
  whatever they read: `cut -c/-b`, `head -c`/`tail -c` (and the old `-5c`),
  `grep -o`, `rg -o`, `rg -r`, and jq string slicing (`.[m:n]`, split, sub,
  gsub, ltrimstr, rtrimstr, match, capture, scan, implode, ascii_*case).
  Not covered: `cut -d X -f N` with an arbitrary delimiter, jq `reverse` on a
  string, and one-bit oracles (`grep -c`, jq `test`, `index`).
- `rg -g/--glob/--iglob`, `-t/--type`, `--type-add` and `--ignore-file` ask:
  a glob, a type (`-t sh` matches `.zshenv`) or an ignore file's `!` line
  selects hidden and ignored files (.env, keys) by name, past rg's own skipping.
- A `--` right after an option may be that option's VALUE (`rg -e -- --hidden`:
  rg searches for "--", then reads --hidden as an option). Such a command is
  checked both ways, as the end of the options and as a value, and runs only if
  both readings pass.
"""

from __future__ import annotations
import os
from pathlib import Path
from typing import Callable, Sequence
from probe.daemon.shell.classifier.classifier import _Checker
from probe.daemon.shell.classifier.refusals import _Fix, _Never, _Refuse
from probe.daemon.shell.held import _PATH_PIECES, _held_resolve, _tree_read
from probe.daemon.shell.parse import _split, _tokenize
from probe.daemon.shell.verdict import Verdict


def classify(
    command: str,
    *,
    workdirs: list[Path],
    home: Path,
    cwd: Path,
    protected: Sequence[Path] = (),
    write_dirs: Sequence[Path] = (),
    piped_input: bool = False,
    hidden: Callable[[str], bool] | None = None,
    off_inside: Callable[[str], bool] | None = None,
    read_dirs: Sequence[Path] = (),
    inside_only: bool = False,
) -> Verdict:
    """Decide, without running anything, whether `command` may run at once.

    `home` must be the $HOME the command will run with (`minimal_env` passes the
    daemon's own); `~` is expanded with it. `write_dirs` are the only folders the
    note-writing heredoc may write into. `piped_input`: its stdin is another
    command's output that may hold a file's text (a compound's `probe ... | X`).
    `read_dirs`: folders read programs may read, never write (the Probe skills).
    `inside_only`: no read reaches outside the working folders (the reader).
    """
    refused = _config_refusal(command, cwd, hidden, off_inside)
    if refused:
        return Verdict(False, refused, refused=True)
    checker = _Checker(
        workdirs=workdirs, home=home, cwd=cwd, protected=protected, write_dirs=write_dirs, hidden=hidden,
        read_dirs=read_dirs, inside_only=inside_only,
    )
    try:
        return checker.classify(command, piped_input)
    except _Never as refusal:
        return Verdict(False, str(refusal), refused=True)
    except _Fix as refusal:
        return Verdict(False, str(refusal), fixable=True)
    except _Refuse as refusal:
        return Verdict(False, str(refusal), credential=checker.names_credential(command),
                       private=checker.names_private(command))


def _config_refusal(command: str, cwd: Path, hidden: Callable[[str], bool] | None,
                    off_inside: Callable[[str], bool] | None) -> str | None:
    """`.probe.config`: a command that reads an `off` file its words name only
    bare (`cat secret.txt`), or a whole tree holding one (`rg x .`, `grep -r`,
    `find`, `ls -R`, a repo-wide `git diff`), is refused in every mode: its output
    cannot be trusted to name what it read (`rg -I`). The tree is looked for where
    bash runs the read (`command_reads`: a `cd` in a pipeline moves nothing but
    may, as its last part under `shopt -s lastpipe`, add a folder), and a
    tree read printing no file names (`rg -I`, `grep -h`) from every folder it may
    run in. Named files are checked again, with everything else, by
    `_Checker._check_path`."""
    if hidden is None and off_inside is None:
        return None
    from probe.shared.harness.session_filter import command_bases, command_reads, drops_file_names, named_off

    files, trees = command_reads(command, str(cwd))
    for path in files:
        if hidden is not None and hidden(path):
            return f"It reads {path}: a .probe.config sets it to off, so Probe never reads it."
    if hidden is not None:
        class _Hidden:
            def check(self, path, **_kw):
                return type("V", (), {"hidden": hidden(str(path))})()

        if named_off(command, command_bases(command, str(cwd)), _Hidden(), lambda name, base: [name]):
            return "It names a file a .probe.config sets to off, so Probe never reads it."
    if trees and drops_file_names(command):
        # `rg -I` / `grep -h` drop the file names the output filter goes by, so a tree read
        # of theirs is checked from every folder a `cd` in it may have left it in.
        trees = [*trees, *(base for base in command_bases(command, str(cwd)) if base not in trees)]
    for tree in trees:
        if off_inside is not None and off_inside(tree):
            return (f"It reads every file below {tree}, which holds a path a .probe.config sets to off or is "
                    "too big to check, so Probe never runs it. Name the files, or a smaller folder that "
                    "holds none of them.")
    return None


def read_refusal(
    path: str,
    *,
    workdirs: list[Path],
    home: Path,
    cwd: Path,
    protected: Sequence[Path] = (),
    write_dirs: Sequence[Path] = (),
    read_dirs: Sequence[Path] = (),
    hidden: Callable[[str], bool] | None = None,
) -> tuple[str, bool] | None:
    """Why the daemon's file reader may not read `path` at once, or None: the
    rules of a safe `cat PATH` inside the working folders (or the checked-out
    notes, the coding agent's instructions and memory; never a hidden folder, a
    credential-shaped name, Probe's own key and state), and the read-only
    `read_dirs` (the Probe skills) besides. Not the shell's reach outside the
    working folders: the reader stays in them. `(reason, never)`: `never` when no
    mode may read it (Probe's own key and state)."""
    checker = _Checker(workdirs=workdirs, home=home, cwd=cwd, protected=protected, write_dirs=write_dirs,
                       read_dirs=read_dirs, hidden=hidden)
    try:
        checker._check_path(path, path == "~" or path.startswith("~/"), [checker.cwd])
    except _Never as refusal:
        return str(refusal), True
    except _Refuse as refusal:
        return str(refusal), False
    return None


def strict_names(command: str, *, workdirs: list[Path], home: Path, cwd: Path, protected: Sequence[Path] = (),
                 write_dirs: Sequence[Path] = ()) -> tuple[bool, bool] | None:
    """`(credential, private)` as the checker's STRICT reading reads `command`
    (`_split(_tokenize(...))`): each part's words, and its redirects' targets,
    resolved against the folder the `cd DIR`s before it lead to, every
    path-shaped piece of each word too. The lenient scans
    (`_Checker.names_credential`, `names_private`) can be led astray by a
    quoted `'>'`, which they take for a redirect, swallowing the `;` and the
    `cd` after it. None when the strict reading refuses the command."""
    try:
        parts = _split(_tokenize(command))
    except _Refuse:
        return None
    checker = _Checker(workdirs=list(workdirs), home=home, cwd=cwd, protected=protected, write_dirs=write_dirs)
    here, home_s = os.path.realpath(cwd), str(home)
    credential = private = False
    for part in parts:
        words = [w.value for w in part.words]
        if words[:1] == ["cd"] and len(words) == 2:
            target = home_s + words[1][1:] if words[1] == "~" or words[1].startswith("~/") else words[1]
            here = os.path.realpath(os.path.join(here, target))
            continue
        private = private or _tree_read(words)
        for word in [*words, *(t.value for _op, t in part.redirects)]:
            for piece in {word, *_PATH_PIECES.split(word)}:
                for real in _held_resolve(piece, [here], home_s) if piece else ():
                    credential = credential or checker._secret(real)
                    private = private or (checker._in_hidden(real) and os.path.lexists(real))
    return credential, private
