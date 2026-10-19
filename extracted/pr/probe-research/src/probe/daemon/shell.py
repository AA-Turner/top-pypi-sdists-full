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

import asyncio
import os
import re
import shlex
import shutil
import signal
import stat
import sys
import tempfile
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable, Iterator, Sequence

from probe.harness import get_registry
from probe.sdk.config import DAEMON_SHELL_CONFIG

__all__ = ["ShellResult", "Step", "Verdict", "classify", "minimal_env", "read_refusal", "run"]


@dataclass(frozen=True)
class Step:
    """One pipeline of a compound command that has `probe` commands in it
    (`Verdict.steps`). The caller runs the steps in order itself, never bash."""

    before: str  # "" for the first; else "&&", "||" or ";" (a newline is ";")
    text: str  # the pipeline as written (what a shell step runs, and what is shown)
    #: A pipeline that starts with `probe ...`: its argv, for the probe tool's checks.
    probe_argv: list[str] | None = None
    #: The rest of that pipeline (`probe run list | jq .items` -> "jq .items"),
    #: fed the probe command's stdout; None when it is not piped on.
    filter: str | None = None
    #: The probe command's stderr: "keep" (shown after the filter's output),
    #: "merge" (`2>&1`: into the filter too) or "drop" (`2>/dev/null`).
    stderr: str = "keep"
    #: A lone `cd FOLDER`: the folder (`~` expanded), which the caller moves into.
    cd: str | None = None


@dataclass(frozen=True)
class Verdict:
    safe: bool  # may run at once
    reason: str  # "" when safe; else one plain sentence why it needs the researcher's yes
    # Set when the WHOLE command is a single `probe ...` call (the argv after the
    # word `probe`); `safe` is then False with reason "probe command", and the
    # caller routes it to its own pre-check.
    probe_argv: list[str] | None = None
    # The text a quoted heredoc feeds that probe command (`probe draft edit PATH
    # <<'EOF'`, `_probe_heredoc`): the caller hands it to the command as stdin.
    probe_stdin: str | None = None
    # Set when the command is several commands and some are `probe ...` calls:
    # the caller runs them one by one (`Step`), each probe command through its
    # own pre-check and each other part as a command of its own.
    steps: list[Step] | None = None
    # Set when the command is the one allowed write, `cat > FILE <<'TAG'`: the
    # resolved FILE and the body it writes, so the caller can scan the body and
    # hold a write to the team note (the verdict alone says only "safe").
    note_target: str | None = None
    note_body: str | None = None
    note_append: bool = False  # `>>`: the body is added to the end of FILE
    # True: refused outright (`_Never`) -- not a question, not even in bypass mode.
    refused: bool = False
    # True: one flag away from safe (`_Fix`) -- not a question; the daemon adds it.
    fixable: bool = False
    # True on a question (neither safe nor refused): a word of the command, or a
    # path-shaped piece of one, names a credential-shaped file (`_secret`), or the
    # command can't be read word by word (`_Checker.names_credential`). Such a
    # question is the researcher's alone: never put to Jev (`tools._jev_approval`).
    credential: bool = False
    # True on a question about a read Jev can't judge (`_Checker.names_private`): a
    # path inside a hidden file or folder, or a whole tree's contents. Also never
    # put to Jev: its `no_secrets` scores these like any harmless read.
    private: bool = False


@dataclass
class ShellResult:
    exit_code: int | None  # None when the time limit killed it
    output: str  # stdout and stderr together, capped
    truncated: bool
    timed_out: bool
    #: Why `run` stopped it early (its `watch` said so), or None.
    stopped: str | None = None
    #: False: stopped before the launch, so nothing ran (`_run_shell_write` logs it not run).
    started: bool = True


# --- the lists -------------------------------------------------------------

_LINUX = sys.platform.startswith("linux")

#: Never open their arguments as files, so the arguments are not path-checked.
_NO_FILES = frozenset(
    {"echo", "expr", "false", "id", "pwd", "seq", "tr", "true", "uname", "whoami", "which"}
)
#: What may follow a note's text and still leave it data: a plain `probe ...`
#: (the push) and filters on its output that read text and never run a file
#: (`| grep -i url | head -2`), named bare (`./head` is any program). Anything
#: else after it (`. ./x.sh`, `bash x.sh`, an `rg --pre`) could run the file
#: the heredoc just wrote.
_COPIES_ONLY_AFTER = frozenset({"cut", "grep", "head", "tail", "wc"})
#: Print a digest of each file they are given. Their options are a list of what
#: runs at once, as jq's are (one it doesn't hold asks): the algorithm, the
#: digest length, the read mode, the line style. -c / --check opens every file a
#: checksum file names, which the check never sees; the options that only matter
#: with it (--quiet --status --strict --warn --ignore-missing) and the ones that
#: frame or encode the lines differently (-z, shasum -0, cksum --raw --base64)
#: are nothing the daemon needs. Each: (flag letters, letters that take a value,
#: long options).
_DIGESTS: dict[str, tuple[str, str, tuple[str, ...]]] = {
    **dict.fromkeys(("md5sum", "sha1sum", "sha224sum", "sha256sum", "sha384sum", "sha512sum"),
                    ("bt", "", ("--binary", "--text", "--tag", "--help", "--version"))),
    "b2sum": ("bt", "l", ("--binary", "--text", "--length", "--tag", "--help", "--version")),
    "cksum": ("", "al", ("--algorithm", "--length", "--tag", "--untagged", "--help", "--version")),
    # A Perl script (macOS's too) whose Getopt::Long also reads `+c` as -c and a long
    # option in any case (`--CHECK`): the list matches exact case, and a `+` word asks
    # of every program here (a `sha256sum` wrapper may run shasum).
    "shasum": ("btU", "a", ("--algorithm", "--binary", "--text", "--UNIVERSAL", "--tag", "--help", "--version")),
}  # fmt: skip
#: gzip and gunzip as readers only, their options a list as the digests' are: the
#: decompressed text to stdout (gzip -cd, gunzip -c), a list (-l) or a test (-t),
#: quietly or not. Anything else asks: no -c writes a file, gzip -c without -d
#: compresses (bytes the output scrubber can't read), -r reads a whole tree, -f
#: copies what isn't compressed, -S reads other names. zcat is `gzip -cd`.
_GZIP_FLAGS = "cdltqvhV"
_GZIP_LONGS = {"--stdout": "c", "--to-stdout": "c", "--decompress": "d", "--uncompress": "d", "--list": "l",
               "--test": "t", "--quiet": "q", "--verbose": "v", "--help": "h", "--version": "V"}
#: Read the files they are given; an option that writes or runs something is
#: refused, and gzip and the digests run only with the options their lists hold.
_READERS = frozenset(
    {"cat", "cut", "diff", "du", "grep", "gunzip", "gzip", "head", "ls", "nl", "paste", "stat", "tail", "wc",
     *_DIGESTS}
)
#: Codex allows these on Linux only (their BSD versions differ). zcat too: macOS's
#: (compress's) reads NAME.Z for every NAME it is given, a file the check never sees.
_LINUX_ONLY = frozenset({"numfmt", "tac", "zcat"})
#: The read programs: a file or folder they name may be outside the working folders
#: (`_check_path`'s `anywhere`), past the places that still ask or are never read.
_READ_ANYWHERE = _READERS | {"find", "jq", "numfmt", "rg", "sort", "tac", "tr", "uniq", "zcat"}
#: How far a read program reaches outside the working folders (`anywhere`). None:
#: nowhere (every other program, git included). _FILES: one ordinary file with one
#: name (`_outside`; a folder there would be read whole). _NAMES: a file or folder,
#: for its names and metadata (ls, stat, cd, find's tests). _TREE: a folder walked
#: for names (find, du, ls -R), unless the walk goes through $HOME or a credential.
_FILES, _NAMES, _TREE = "files", "names", "tree"
#: Checked by their own method below.
_SPECIAL = frozenset({"base64", "cd", "find", "git", "jq", "rg", "sed", "sort", "uniq"})
#: Bash builtins: PATH is never consulted for them.
_BUILTINS = frozenset({"cd", "echo", "false", "pwd", "true"})

_WRAPPERS = frozenset(
    {
        ".", "bash", "builtin", "busybox", "chroot", "command", "dash", "doas", "env", "eval",
        "exec", "fish", "flock", "ionice", "ksh", "nice", "nohup", "parallel", "script",
        "setsid", "sh", "source", "stdbuf", "strace", "su", "sudo", "time", "timeout",
        "unshare", "watch", "xargs", "zsh",
    }
)  # fmt: skip

#: Option values that are text (delimiters, patterns, formats), never a file.
_TEXT_OPTIONS: dict[str, tuple[str, ...]] = {
    "cut": ("-d", "--delimiter", "--output-delimiter"),
    "diff": ("-I", "--ignore-matching-lines", "--label", "-L", "--line-format", "--old-line-format",
             "--new-line-format", "--unchanged-line-format", "--old-group-format", "--new-group-format",
             "--changed-group-format", "--unchanged-group-format", "-F", "--show-function-line"),
    "du": ("-B", "--block-size", "-d", "--max-depth", "-t", "--threshold", "--exclude", "--time-style"),
    "grep": ("-e", "--regexp", "--include", "--exclude", "--exclude-dir", "--label",
             "--group-separator"),
    "ls": ("-I", "--ignore", "--hide", "--time-style"),  # BSD ls (macOS) reads -I as a flag (`_reader`)
    "nl": ("-d", "--section-delimiter", "-s", "--number-separator"),
    "paste": ("-d", "--delimiters"),
    "rg": ("-e", "--regexp", "-g", "--glob", "--iglob", "-t", "--type", "-T", "--type-not",
           "--type-add", "-r", "--replace", "--path-separator", "--context-separator",
           "--field-match-separator", "--field-context-separator", "--colors", "--pre-glob"),
    "sort": ("-t", "--field-separator", "-k", "--key"),
    "stat": ("-c", "--format", "--printf"),
}  # fmt: skip

# Codex's own lists, verbatim.
_FIND_UNSAFE = (
    "-exec", "-execdir", "-ok", "-okdir",  # run arbitrary commands
    "-delete",  # deletes matching files
    "-fls", "-fprint", "-fprint0", "-fprintf",  # write pathnames to a file
)  # fmt: skip
_RG_UNSAFE_WITH_ARGS = ("--pre", "--hostname-bin")  # run a command
_RG_UNSAFE_WITHOUT_ARGS = ("--search-zip", "-z")  # call decompression tools
#: rg options that stop it skipping ignored files (.env and keys are usually ignored).
_RG_NO_IGNORE = ("--no-ignore", "--no-ignore-vcs", "--no-ignore-dot", "--no-ignore-files", "--no-ignore-global",
                 "--no-ignore-parent", "--no-ignore-exclude", "--unrestricted")
_BASE64_UNSAFE = ("-o", "--output")
#: rg options that select files by name past its hidden/ignored skipping (a glob
#: `-g .env`, a type `-t sh` matching `.zshenv`, an ignore file's `!.env`).
_RG_SELECTORS = ("--glob", "--iglob", "--type", "--type-add", "--ignore-file")

# Ours.
_FIND_UNSAFE_OURS = ("-L", "-follow", "-files0-from")
#: A word of find's leading options: GNU's -H -L -P, BSD's -E -X -d -s -x too, in a
#: cluster, ending in BSD's -f whose value (attached, or the next word) is a start
#: folder. Group 2: None without -f.
_FIND_LEADING = re.compile(r"-([EHLPXdsx]*)(?:f(.*))?")
#: find predicates whose value is a pattern or a format, not a file.
_FIND_PATTERNS = (
    "-name", "-iname", "-path", "-ipath", "-wholename", "-iwholename", "-regex", "-iregex",
    "-lname", "-ilname", "-printf", "-regextype", "-fstype", "-user", "-group",
)  # fmt: skip
_GREP_VALUE_LETTERS = "efmABCdD"
_RG_VALUE_LETTERS = "ABCEMTdefgjmrt"
_SORT_VALUE_LETTERS = "koStT"
_DU_VALUE_LETTERS = "BdtX"
#: ls's and du's short options that take a value, GNU's and BSD's (BSD ls -D FORMAT,
#: BSD du -I MASK), for which word may be a value rather than a name (`_listed`).
_LISTED_VALUE_LETTERS = {"ls": "DITw", "du": "BIXdt"}
_JQ_SHORT_FLAGS = frozenset("nrjascCMSRehVb")
_JQ_LONG_FLAGS = frozenset(
    {
        "--seq", "--stream", "--stream-errors", "--slurp", "--raw-input", "--null-input",
        "--compact-output", "--tab", "--color-output", "--monochrome-output", "--ascii-output",
        "--unbuffered", "--sort-keys", "--raw-output", "--raw-output0", "--join-output",
        "--exit-status", "--binary", "--help", "--version", "--build-configuration",
    }
)  # fmt: skip
_JQ_FILE_OPTIONS = ("--rawfile", "--slurpfile", "--from-file", "--library-path")
_JQ_MODULES = re.compile(r"\b(import|include|modulemeta)\b")
#: jq builtins that re-encode text, so a key in a file reads as something the output scrubber cannot recognise.
_JQ_ENCODERS = re.compile(r"@(base64|base32|uri|sh)\b|(?<![\w.$])(format\s*\(|explode\b)")
#: jq that prints PART of a string: a slice `.[m:n]` (of an array too: the two
#: cannot be told apart from the program), and the builtins that cut, strip,
#: re-case or rebuild a string. A key printed in pieces, or without its prefix,
#: is something the output scrubber cannot recognise.
_JQ_SLICERS = re.compile(
    r"\[[^\[\]{}\"]*:[^\[\]{}\"]*\]|(?<![\w.$])(splits?|g?sub|[lr]?trimstr|match|capture|scan|implode"
    r"|reverse|ascii_(down|up)case)\b"
)

_GIT_VERBS = ("status", "log", "diff", "show", "blame", "branch", "rev-parse", "ls-files")
_GIT_GLOBAL_OK = frozenset(
    {"--no-pager", "-P", "--no-optional-locks", "--literal-pathspecs", "--no-replace-objects"}
)
_GIT_DENIED = {
    "--output": "writes to a file",
    "--ext-diff": "runs the repository's external diff program",
    "--textconv": "runs the repository's textconv programs",
    "--show-signature": "runs gpg",
    "--no-index": "compares files outside the repository",
    "--submodule": "runs git inside submodules without these safeguards",
    "--open-files-in-pager": "runs a pager",
}
_GIT_NEEDS = {
    "log": ("--no-textconv", "--no-ext-diff"),
    "show": ("--no-textconv", "--no-ext-diff"),
    "diff": ("--no-textconv", "--no-ext-diff"),
    "blame": ("--no-textconv",),
}

#: Credential-shaped places under $HOME (plus Probe's own config and key files).
_HOME_SECRETS = (
    ".ssh", ".aws", ".gnupg", ".config/gcloud", ".kube", ".docker", ".netrc", ".pgpass",
    ".git-credentials", ".config/probe",
)  # fmt: skip
_SECRET_NAMES = frozenset({".netrc", ".pgpass", ".git-credentials", ".pypirc", ".npmrc"})
#: Shell and REPL history: every command typed, the passwords and keys in them too.
_HISTORY_NAMES = frozenset({
    ".zsh_history", ".bash_history", ".sh_history", ".python_history", ".node_repl_history", ".psql_history",
    ".mysql_history", ".sqlite_history", ".lesshst", ".viminfo",
})
#: Private like a credential wherever they are (`_private`), in `_canon`'s spelling:
#: devices, the kernel's and every process's own files (environment, memory, open
#: files), the secrets a container is given, a user's runtime files, and the
#: system's own keys and password hashes.
_SYSTEM_PRIVATE = (
    ("/dev", "a device (/dev)"),
    ("/proc", "a process's or the kernel's own files (/proc)"),
    ("/sys", "the kernel's own files (/sys)"),
    ("/run/secrets", "a container's secrets (/run/secrets)"),
    ("/var/run/secrets", "a container's secrets (/var/run/secrets)"),
    # XDG_RUNTIME_DIR: the session's sockets and keyrings, podman's registry login.
    ("/run/user", "a user's runtime files (/run/user: sockets, keyrings, registry logins)"),
    # Readable by root only, and a daemon may run as root (a cloud GPU box, a container).
    ("/etc/shadow", "the system's password hashes"),
    ("/etc/gshadow", "the system's password hashes"),
    ("/etc/ssh", "the machine's SSH keys (/etc/ssh)"),
)
#: macOS's second spellings of one place, folded: the data volume's firmlink
#: (/System/Volumes/Data/Users/x is /Users/x), which realpath keeps as written, and
#: the /private folders /etc, /var and /tmp link to, which a command may name
#: itself. `_canon` takes them off, in this order.
_MACOS_ALIASES = (("/system/volumes/data", ""), ("/private/etc", "/etc"), ("/private/var", "/var"),
                  ("/private/tmp", "/tmp"))
#: Harness instruction files allowed even inside a hidden folder of a working folder.
_HARNESS_NAMES = frozenset({"CLAUDE.md", "CLAUDE.local.md", "AGENTS.md"})
_HARNESS_FILES = (
    [".claude", "CLAUDE.md"], [".codex", "AGENTS.md"], [".pi", "agent", "AGENTS.md"], [".kimi-code", "AGENTS.md"],
)  # fmt: skip


def _moved_harness_files() -> frozenset[str]:
    """Each harness's own instruction file where its home override puts it
    (`$KIMI_CODE_HOME/AGENTS.md`), outside $HOME as well: read-only, like the
    ones `_HARNESS_FILES` lists under $HOME."""
    found: set[str] = set()
    for harness in get_registry().all():
        name = (harness.instructions or {}).get("global")
        if not harness.home or not isinstance(name, str) or not name:
            continue
        if not (os.environ.get(harness.home["env"]) or "").strip():
            continue
        home = harness.home_dir()
        if home is not None:
            found.add(os.path.realpath(str(home / name)))
    return frozenset(found)


#: The probe commands a quoted heredoc may feed (`_Checker._probe_heredoc`), and
#: what a probe heredoc in another shape answers (NEW wording,
#: tests/fixtures/daemon_prompts/tools/bash-replies.NEW.md).
PROBE_STDIN_COMMANDS = (("draft", "edit"), ("daemon", "task"))
#: The whole-command shape of each, as the refusals name it.
PROBE_HEREDOC_SHAPES = {("draft", "edit"): "probe draft edit PATH <<'EOF'", ("daemon", "task"): "probe daemon task <<'EOF'"}
R_PROBE_HEREDOC = "A probe heredoc must be the whole command: `{shape}`, the text, then a line reading EOF."
R_PROBE_HEREDOC_TAIL = "Something follows the heredoc - `probe {command}` with its text must be the whole command."
R_PROBE_HEREDOC_CHAINED = "`probe {command}` with its heredoc must be the whole command: run the rest in another call."
_ASSIGNMENT = re.compile(r"[A-Za-z_][A-Za-z0-9_]*\+?=")
_SED_PRINT = re.compile(r"[0-9]+(,[0-9]+)?p")  # Codex: /^(\d+,)?\d+p$/
_HEREDOC_TAG = re.compile(r"[A-Za-z_][A-Za-z0-9_]*")
_CONTROL = frozenset({"|", "&&", "||", ";", "\n"})

_R_DOLLAR = "`$` is allowed only inside single quotes."
_R_HEREDOC = (
    "Heredocs are allowed only as `cat > FILE <<'TAG'` into the notes folder, as the whole command."
)
#: The one shape a file write takes (the tools name it when a note write is refused).
R_HEREDOC = _R_HEREDOC
_R_BRACE = "An unquoted `{` or `}` can expand to other paths or group commands."
_R_SCRAMBLE = (
    "{what} changes text (a key included) into characters the output scrubber can't recognise."
)
_R_SLICE = (
    "{what} prints text in pieces, and a piece of a key is something the scrubber can't recognise."
)
_R_GREP_R = (
    "grep -r reads every file under the folder, .env files and keys included."
)
_OUTSIDE = "outside the working folders"


class _Refuse(Exception):
    """Raised inside the classifier; the message is the Verdict's reason."""


class _Fix(_Refuse):
    """A read one flag away from safe (`git log` without `--no-textconv
    --no-ext-diff`): not a question for the researcher -- the daemon adds the
    flag itself -- so it answers "not run" with what to add (bypass mode runs it)."""


class _Never(_Refuse):
    """A refusal no one can wave through: never held as a question, and not
    auto-approved in bypass mode either. For what would step around the daemon's
    own guarded paths -- Probe's key and state files, and `probe` run from the
    shell instead of the probe tool (its pre-check, lease and logbook)."""


# --- reading the command ---------------------------------------------------


@dataclass(frozen=True)
class _Word:
    value: str  # after quote removal
    raw: str  # as written
    tilde: bool = False  # starts with an unquoted ~ that bash expands to $HOME
    #: The empty VALUE `_dashdash_as_value` puts where a `--` was: never a name or a path.
    synthetic: bool = False


@dataclass(frozen=True)
class _Op:
    op: str  # a control operator (_CONTROL) or a redirect ("<", ">", ">>", ">&", "<<", ...)
    fd: str | None = None  # the digits written before a redirect ("2" in 2>&1)


@dataclass
class _Part:
    words: list[_Word]
    redirects: list[tuple[_Op, _Word]]
    before: str  # the control operator in front of it ("" for the first)


def _tokenize(s: str) -> list[_Word | _Op]:
    """Split a command the way bash would, refusing every construct it can't vouch for."""
    out: list[_Word | _Op] = []
    buf: list[str] = []
    start = -1  # where the current word began (-1: no word yet)
    quoted = False  # the current word has a quoted part
    tilde = False
    i, n = 0, len(s)

    def end_word(at: int) -> None:
        nonlocal buf, start, quoted, tilde
        if start >= 0:
            out.append(_Word("".join(buf), s[start:at], tilde))
        buf, start, quoted, tilde = [], -1, False, False

    while i < n:
        c = s[i]
        if c in " \t":
            end_word(i)
            i += 1
        elif c == "\n":
            end_word(i)
            # A newline right after |, && or || continues the command.
            if not (out and isinstance(out[-1], _Op) and out[-1].op in ("|", "&&", "||")):
                out.append(_Op("\n"))
            i += 1
        elif c == "\\":
            if i + 1 >= n:
                raise _Refuse("The command ends with a stray backslash.")
            if s[i + 1] == "\n":  # line continuation
                i += 2
                continue
            if start < 0:
                start = i
            buf.append(s[i + 1])
            quoted = True
            i += 2
        elif c == "'":
            if start < 0:
                start = i
            j = s.find("'", i + 1)
            if j < 0:
                raise _Refuse("A single quote is never closed.")
            buf.append(s[i + 1 : j])
            quoted = True
            i = j + 1
        elif c == '"':
            if start < 0:
                start = i
            quoted = True
            j = i + 1
            while True:
                if j >= n:
                    raise _Refuse("A double quote is never closed.")
                d = s[j]
                if d == '"':
                    break
                if d == "$":
                    raise _Refuse(_R_DOLLAR)
                if d == "`":
                    raise _Refuse("Backticks run a command inside the command.")
                if d == "\\" and j + 1 < n and s[j + 1] in '$`"\\\n':
                    if s[j + 1] != "\n":
                        buf.append(s[j + 1])
                    j += 2
                    continue
                buf.append(d)
                j += 1
            i = j + 1
        elif c == "$":
            raise _Refuse(_R_DOLLAR)
        elif c == "`":
            raise _Refuse("Backticks run a command inside the command.")
        elif c in "*?[":
            raise _Refuse(
                f"An unquoted `{c}` is a glob - it could match paths the check never saw."
            )
        elif c == "{" and start < 0 and s.startswith("{}", i) and (i + 2 == n or s[i + 2] in " \t\n;|&<>"):
            # The whole word `{}` (find's placeholder) never expands. Anywhere else a
            # brace may: `a{b,c}`, `{x..y}`, a `{` left open for a later word.
            start = i
            buf.append("{}")
            i += 2
        elif c in "{}":
            raise _Refuse(_R_BRACE)
        elif c in "()":
            raise _Refuse("Parentheses start a subshell, a group or a process substitution.")
        elif c == "#" and start < 0:
            raise _Refuse("Comments (#) aren't allowed.")
        elif c == "~" and start < 0:
            nxt = s[i + 1] if i + 1 < n else ""
            if nxt and nxt not in "/ \t\n;|&<>":
                raise _Refuse("`~name`, `~+` and `~-` expand to other folders.")
            start, tilde = i, True
            buf.append("~")
            i += 1
        elif c == "~" and s[i - 1] in "=:":
            raise _Refuse("A `~` after `=` or `:` can expand to $HOME.")
        elif c == ";":
            end_word(i)
            if s.startswith((";;", ";&"), i):
                raise _Refuse("`;;` and `;&` belong to case statements, which aren't allowed.")
            out.append(_Op(";"))
            i += 1
        elif c == "&":
            end_word(i)
            for op in ("&&", "&>>", "&>"):
                if s.startswith(op, i):
                    out.append(_Op(op))
                    i += len(op)
                    break
            else:
                raise _Refuse("A single `&` runs a command in the background.")
        elif c == "|":
            end_word(i)
            if s.startswith("||", i):
                out.append(_Op("||"))
                i += 2
            else:  # `|&` pipes stderr too: still a pipe
                out.append(_Op("|"))
                i += 2 if s.startswith("|&", i) else 1
        elif c in "<>":
            word = "".join(buf)
            fd = None
            if start >= 0 and not quoted and re.fullmatch(r"[0-9]+", word):
                fd = word  # `2>`: the digits belong to the redirect
                buf, start, quoted, tilde = [], -1, False, False
            else:
                end_word(i)
            ops = (">>", ">&", ">|", ">") if c == ">" else ("<<<", "<<-", "<<", "<&", "<>", "<")
            op = next(o for o in ops if s.startswith(o, i))
            out.append(_Op(op, fd))
            i += len(op)
        else:
            if start < 0:
                start = i
            buf.append(c)
            i += 1
    end_word(n)
    return out


def _split(tokens: list[_Word | _Op]) -> list[_Part]:
    """Group tokens into commands joined by control operators."""
    parts: list[_Part] = []
    words: list[_Word] = []
    redirects: list[tuple[_Op, _Word]] = []
    before = ""
    pending: _Op | None = None
    for tok in tokens:
        if isinstance(tok, _Word):
            if pending is not None:
                redirects.append((pending, tok))
                pending = None
            else:
                words.append(tok)
            continue
        if pending is not None:
            raise _Refuse(f"The redirect `{pending.op}` has no target.")
        if tok.op not in _CONTROL:
            pending = tok
            continue
        parts.append(_Part(words, redirects, before))
        words, redirects, before = [], [], tok.op
    if pending is not None:
        raise _Refuse(f"The redirect `{pending.op}` has no target.")
    parts.append(_Part(words, redirects, before))

    # Bash accepts empty commands around `;` and newlines (`ls;`); anything else is broken.
    kept: list[_Part] = []
    for k, part in enumerate(parts):
        if part.words or part.redirects:
            kept.append(part)
            continue
        after = parts[k + 1].before if k + 1 < len(parts) else ""
        if part.before not in ("", ";", "\n") or after not in ("", ";", "\n"):
            raise _Refuse("An operator (|, &&, ||) has no command on one side.")
    if not kept:
        raise _Refuse("The command is empty.")
    return kept


def _cd_word(part: _Part) -> _Word | None:
    """The folder of a plain `cd FOLDER` (None for anything else)."""
    words = part.words
    if not words or words[0].value != "cd":
        return None
    args = words[1:]
    if args and args[0].value == "--":
        args = args[1:]
    if len(args) != 1 or not args[0].value or args[0].value.startswith("-"):
        return None
    return args[0]


def _expand(word: _Word, home: str) -> str:
    return home + word.value[1:] if word.tilde else word.value


#: A process's own folders (`/proc/self/cwd/..`, `/proc/1234/root`, `/dev/fd/3`): the
#: check resolves them in ITS process, bash in the command's.
_PROC_SELF = re.compile(r"/proc/(self|thread-self|[0-9]+)(/|$)|/dev/fd/")
#: A probe command line inside one word (`awk 'BEGIN{system("probe run list")}'`,
#: `git -c core.pager='probe ...'`): `probe` then a lowercase subcommand.
_EMBEDDED_PROBE = re.compile(r"(?<![\w./-])probe\s+[a-z]")
#: Programs that run text in their arguments as commands (`awk system()`, `git -c
#: core.pager=`, `su -c`, `ssh host CMD`...). Only theirs are read for a probe
#: command line: "linear probe accuracy" is an ordinary phrase in ML work.
_CODE_ARGS = frozenset({"awk", "gawk", "mawk", "nawk", "busybox", "doas", "flock", "git", "make", "parallel",
                        "screen", "script", "ssh", "su", "sudo", "tmux", "watch"})


def _never_setting(name: str) -> None:
    """A Probe setting (`PROBE_*`) set, unset or exported by the shell: never run."""
    if name.startswith("PROBE_"):
        raise _Never(f"It sets or unsets {name}, Probe's own setting. The shell has no Probe key - Probe writes go "
                     "through `probe`.")


def _stderr_only(op: _Op, target: _Word) -> bool:
    """`2>&1` or `2>/dev/null`: the redirects a probe step may carry."""
    return op.fd == "2" and ((op.op == ">&" and target.value == "1")
                             or (op.op == ">" and target.value == "/dev/null" and not target.tilde))


def _is_probe(part: _Part) -> bool:
    return bool(part.words) and part.words[0].value == "probe"


def _text(part: _Part) -> str:
    """One command as bash reads it, from the words as written (quotes kept)."""
    redirects = [f"{op.fd or ''}{op.op}{target.raw}" for op, target in part.redirects]
    return " ".join([w.raw for w in part.words] + redirects)


def _walk(parts: list[_Part], start: str, home: str) -> Iterator[tuple[_Part, list[str]]]:
    """Yield each command with the folders it may run in, following `cd`.

    A folder is kept as bash would see it (a `cd` goes to the logical path, or to
    the physical one if that fails); every check resolves it with realpath. After
    `&&` only the folder a successful `cd` reached counts; after `;`, `||` or a
    newline, every folder reached so far does (the `cd` may have failed); the
    sides of a pipeline run in subshells, so a `cd` there moves nothing.
    """
    seen = [start]
    success = [start]
    previous = [start]
    for k, part in enumerate(parts):
        if part.before == "&&":
            cands = success
        elif part.before == "|":
            cands = previous
        else:
            cands = list(seen)
        yield part, cands
        piped = part.before == "|" or (k + 1 < len(parts) and parts[k + 1].before == "|")
        target = None if piped else _cd_word(part)
        if target is None:
            success = cands
        else:
            path = _expand(target, home)
            success = []
            for cand in cands:
                joined = os.path.join(cand, path)
                for folder in (os.path.normpath(joined), os.path.realpath(joined)):
                    if folder not in success:
                        success.append(folder)
            seen += [f for f in success if f not in seen]
        previous = cands


# --- small helpers ---------------------------------------------------------


def _inside(path: str, root: str) -> bool:
    return path == root or path.startswith(root.rstrip("/") + "/")


def _norm(path: str) -> str:
    path = os.path.normpath(path)
    return "/" + path.lstrip("/") if path.startswith("//") else path


def _canon(path: str) -> str:
    """One spelling for one place, for the private and credential checks: folded to
    one case (macOS's disks ignore it, and realpath keeps a name as written:
    ~/library is ~/Library there) and with macOS's second spellings taken off
    (`_MACOS_ALIASES`: /private/etc/ssh is /etc/ssh)."""
    out = path.casefold()
    for alias, real in _MACOS_ALIASES:
        if out == alias or out.startswith(alias + "/"):
            out = real + out[len(alias) :]
    return out or "/"


def _spellings(path: str) -> list[str]:
    """Every spelling of `path` (`_canon`'s) a folder above it may be named by: a walk
    of /System/Volumes or /private goes through it by its second spelling."""
    canon = _canon(path)
    forms = [canon, *(alias + canon[len(real) :] for alias, real in _MACOS_ALIASES
                      if real and (canon == real or canon.startswith(real + "/")))]
    return sorted({form for spelled in forms for form in (spelled, _MACOS_ALIASES[0][0] + spelled)})


def _long(arg: str, names: Sequence[str]) -> str | None:
    """The listed long option `arg` spells, counting GNU abbreviations (`--out=` is `--output=`)."""
    if not arg.startswith("--") or arg == "--":
        return None
    given = arg.split("=", 1)[0]
    for name in names:
        if name == given or (len(given) > 2 and name.startswith(given)):
            return name
    return None


def _short_letters(arg: str, value_letters: str) -> str:
    """The option letters of a cluster like `-rn`, up to the first one that takes a value."""
    if len(arg) < 2 or arg[0] != "-" or arg[1] == "-":
        return ""
    letters = []
    for ch in arg[1:]:
        letters.append(ch)
        if ch in value_letters:
            break
    return "".join(letters)


def _options(words: Sequence[_Word]) -> list[str]:
    """The arguments before a `--` (after it, everything is a name, never an option)."""
    out = []
    for w in words:
        if w.value == "--":
            break
        out.append(w.value)
    return out


def _dashdash_as_value(words: Sequence[_Word]) -> list[_Word] | None:
    """The same words, reading every `--` that comes right after an option as that
    option's VALUE (an empty one), so what follows it is read as options again.

    Whether `-e --` ends the options or hands `--` to `-e` depends on each
    option's arity, which the lists here do not know in full. So the caller
    checks both readings; None when no `--` is in that position."""
    out = list(words)
    changed = False
    for k in range(1, len(out)):
        prev = out[k - 1].value
        if out[k].value == "--" and prev.startswith("-") and prev not in ("-", "--"):
            out[k] = _Word("", "''", synthetic=True)
            changed = True
    return out if changed else None


def _positionals(words: Sequence[_Word], text_options: Sequence[str]) -> list[_Word]:
    """The arguments that are names, not options or a text option's separate value."""
    out: list[_Word] = []
    skip_next = False
    names_only = False
    for w in words:
        v = w.value
        if skip_next:
            skip_next = False
        elif w.synthetic:
            pass  # an option's value, not a name
        elif names_only or v == "-" or not v.startswith("-"):
            out.append(w)
        elif v == "--":
            names_only = True
        elif v in text_options:
            skip_next = True
    return out


def _hidden(comps: list[str], real: str) -> str | None:
    """The hidden folder in a path below a working folder, if any."""
    if comps and comps[-1] in _HARNESS_NAMES:
        return None
    for comp in comps[:-1]:
        if comp.startswith("."):
            return comp
    if comps and comps[-1].startswith(".") and os.path.isdir(real):
        return comps[-1]
    return None


def _clean_path(value: str | None) -> str:
    """The parent's PATH without empty or relative entries (a `.` there would run ./cat)."""
    entries: list[str] = []
    for entry in (value or "").split(os.pathsep):
        if entry and os.path.isabs(entry) and entry not in entries:
            entries.append(entry)
    return os.pathsep.join(entries) or os.defpath


# --- the classifier --------------------------------------------------------


class _Checker:
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

    def _cd(self, args: list[_Word], cands: list[str]) -> None:
        word = _cd_word(_Part([_Word("cd", "cd"), *args], [], ""))
        if word is None:
            raise _Refuse("cd takes exactly one folder (no options, no bare `cd`, no `cd -`).")
        # A folder a read program could name: what runs there is checked in it (`_walk`).
        self._check_path(word.value, word.tilde, cands, logical=True, verb="It moves into", anywhere=_NAMES)

    def _find(self, args: list[_Word], cands: list[str]) -> None:
        values = [w.value for w in args]
        for v in values:
            if v in _FIND_UNSAFE:
                raise _Refuse(f"find {v} can run commands, delete files or write files.")
            if v in _FIND_UNSAFE_OURS:
                why = "reads a list of start folders" if v == "-files0-from" else "follows symlinks"
                raise _Refuse(f"find {v} {why} the check can't see.")
        # find [-H] [-P] [-D opts] [-Olevel] [--] [start folder...] [expression]; BSD find
        # (macOS) also takes -E -X -d -s -x, in clusters, and `-f PATH`, a start folder.
        k, starts, walks_cwd = 0, 0, False
        while k < len(values):
            v = values[k]
            if v == "--":
                k += 1
                break
            if v == "-D":
                k += 2
                continue
            if v.startswith("-O"):
                k += 1
                continue
            flags = _FIND_LEADING.fullmatch(v)
            if not flags or not (flags.group(1) or flags.group(2) is not None):
                break
            if "L" in flags.group(1):
                raise _Refuse(f"find {v} follows symlinks the check can't see.")
            k += 1
            if flags.group(2) is None:
                continue
            if flags.group(2):  # `-f/etc`: BSD's start folder, or GNU's test (`-fstype`), which walks `.`
                self._check_path(flags.group(2), False, cands, anywhere=_TREE)
                walks_cwd = True
            elif k < len(args):
                self._check_path(args[k].value, args[k].tilde, cands, anywhere=_TREE)
                k += 1
            starts += 1
        while k < len(values) and values[k][:1] not in ("-", "(", ")", "!", ","):
            if args[k].synthetic:
                k += 1
                continue
            self._check_path(args[k].value, args[k].tilde, cands, anywhere=_TREE)
            starts += 1
            k += 1
        if not starts or walks_cwd:
            self._require_cwd(cands, "find with no start folder", anywhere=_TREE)
        self._args(args, cands, word_options=_FIND_PATTERNS, anywhere=_NAMES)

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

    def _base64(self, args: list[_Word], cands: list[str]) -> None:
        for v in (w.value for w in args):  # Codex's rule, verbatim: any argument
            if v in _BASE64_UNSAFE or v.startswith("--output=") or (
                v.startswith("-o") and v != "-o"
            ):
                raise _Refuse("base64 -o / --output writes to a file.")
        decode = False
        for v in _options(args):  # ours: abbreviations (--out=) and clusters (-do)
            if _long(v, ("--output",)) or "o" in _short_letters(v, "biow"):
                raise _Refuse("base64 -o / --output writes to a file.")
            decode = decode or bool(_long(v, ("--decode",))) or "d" in _short_letters(v, "w")
        if not decode:
            raise _Refuse(
                "base64 encoding changes text (a key included) into characters the scrubber can't recognise - "
                "only `base64 -d` runs at once."
            )
        self._args(args, cands)

    def _sort(self, args: list[_Word], cands: list[str]) -> None:
        for v in _options(args):
            bad = _long(v, ("--output", "--compress-program", "--temporary-directory"))
            letters = _short_letters(v, _SORT_VALUE_LETTERS)
            if bad == "--compress-program":
                raise _Refuse("sort --compress-program runs another program.")
            if bad or "o" in letters or "T" in letters:
                raise _Refuse("sort -o / -T writes files.")
        self._reader("sort", args, cands)

    def _uniq(self, args: list[_Word], cands: list[str]) -> None:
        names = 0
        skip_next = False
        names_only = False
        for w in args:
            v = w.value
            if skip_next:
                skip_next = False
            elif w.synthetic:
                pass  # an option's value, not a second file
            elif names_only or v == "-" or not v.startswith("-"):
                names += 1
            elif v == "--":
                names_only = True
            elif v.startswith("--"):
                skip_next = "=" not in v and bool(
                    _long(v, ("--skip-fields", "--skip-chars", "--check-chars"))
                )
            else:
                letters = _short_letters(v, "fsw")
                skip_next = bool(letters) and letters[-1] in "fsw" and len(letters) == len(v) - 1
        if names > 1:
            raise _Refuse("uniq with a second file name writes its output there.")
        self._args(args, cands, anywhere=_FILES)

    def _jq(self, args: list[_Word], cands: list[str]) -> None:
        program_seen = False
        string_args = False  # after --args / --jsonargs, positionals are strings
        names_only = False
        skip = 0
        for w in args:
            v = w.value
            if skip:
                skip -= 1
                continue
            if w.synthetic:
                continue  # an option's value, neither the program nor a file
            if not names_only and v.startswith("-") and v != "-":
                if v == "--":
                    names_only = True
                elif v.startswith("--"):
                    name = v.split("=", 1)[0]
                    if name in _JQ_FILE_OPTIONS:
                        raise _Refuse(f"jq {name} reads a file the check can't place.")
                    if v in ("--arg", "--argjson"):
                        skip = 2
                    elif v == "--indent":
                        skip = 1
                    elif v in ("--args", "--jsonargs"):
                        string_args = True
                    elif v not in _JQ_LONG_FLAGS:
                        raise _Refuse(f"The jq option {v} isn't on the safe list.")
                elif "f" in v[1:] or "L" in v[1:]:
                    raise _Refuse("jq -f / -L read files the check can't place.")
                elif any(ch not in _JQ_SHORT_FLAGS for ch in v[1:]):
                    raise _Refuse(f"The jq option {v} isn't on the safe list.")
                continue
            if not program_seen:
                program_seen = True
                if _JQ_MODULES.search(v):
                    raise _Refuse("jq import / include load files from jq's library folders.")
                if _JQ_ENCODERS.search(v):
                    raise _Refuse(_R_SCRAMBLE.format(what="jq's @base64 / @base32 / @uri / @sh / format / explode"))
                if _JQ_SLICERS.search(v):
                    raise _Refuse(_R_SLICE.format(what="jq's string slicing (.[m:n], split, sub, ltrimstr, match...)"))
            elif not string_args:
                self._check_path(v, w.tilde, cands, anywhere=_FILES)

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
    from probe.daemon.exclusions import command_bases, command_reads, drops_file_names, named_off

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


# --- what a held command runs ----------------------------------------------
#
# A command that is NOT safe is shown to the researcher and runs on their yes.
# The question shows its words; a script it runs is a file whose text the words
# do not show. So the daemon never asks to run a file in the folders it writes
# without a question (`names_writable`), and a script anywhere else is hashed
# into the question and re-hashed before the yes runs (`held_scripts`). Both
# read the command leniently (it need not pass `classify`), best effort.

_SHELL_RUNNERS = frozenset({"bash", "sh", "zsh", "dash", "ksh", "fish"})
_RUNNER_FAMILY = (
    (re.compile(r"(python|pypy)[0-9.]*"), "python"),
    (re.compile(r"perl[0-9.]*"), "perl"),
    (re.compile(r"node(js)?"), "node"),
    (re.compile(r"ruby[0-9.]*"), "ruby"),
)
#: Per family: options whose next word is a value (never the script), and options
#: after which no script file follows (the code is on the command line).
_RUNNER_OPTIONS: dict[str, tuple[frozenset[str], frozenset[str]]] = {
    "shell": (frozenset({"-o", "-O", "+o", "+O", "--rcfile", "--init-file"}), frozenset({"-c"})),
    "python": (frozenset({"-W", "-X", "--check-hash-based-pycs"}), frozenset({"-c", "-m"})),
    "perl": (frozenset({"-I", "-M", "-m", "-x"}), frozenset({"-e", "-E"})),
    "node": (frozenset({"-r", "--require", "--import", "--loader", "--experimental-loader", "-C", "--conditions",
                        "--input-type"}), frozenset({"-e", "--eval", "-p", "--print"})),
    "ruby": (frozenset({"-I", "-r", "-C", "-E", "-F"}), frozenset({"-e"})),
}  # fmt: skip
#: A wrapper's options whose next word is a value (`sudo -u root`, `timeout -s KILL`).
_WRAPPER_VALUES = frozenset({"-u", "-g", "-C", "-D", "-h", "-p", "-r", "-t", "-U", "-S", "-s", "-k", "-n", "-i",
                             "-o", "-e", "-w"})  # fmt: skip
_PUNCT = frozenset("();<>|&")
#: What splits a word into the pieces a path may hide in (`open('.env')`,
#: `--key=id_rsa`, `a.pem,b.pem`): the characters a file name in practice never holds.
_PATH_PIECES = re.compile(r"[^\w.~/+@%-]+")


@dataclass
class _Held:
    words: list[str]
    stdin: list[str]  # the targets of its `<` redirects
    piped: bool  # after a `|`: its input is the previous command's output
    #: The targets of its other redirects (`> f`, `>> ~/.zshrc`): files it writes,
    #: which a scan of what a command names must see too.
    targets: list[str] = field(default_factory=list)


def _tree_read(words: list[str]) -> bool:
    """Does this simple command read a whole tree's contents? Any `rg` (it
    searches a tree unless every name is a file); `grep`/`egrep`/`fgrep`/`diff`
    with anything that can mean recursive, read wider than the programs do, so
    a false yes only asks: a short cluster holding `r` or `R` anywhere (a `--`
    may be an option's value: `grep -e -- -r .`), a long option any prefix of
    `--recursive` or `--dereference-recursive` from `--rec` / `--der` on, and
    any word holding `recurse` (`-d recurse`, `--directories=recurse`)."""
    while words and "=" in words[0] and not words[0].startswith("-"):  # `X=1 grep -rn ...`
        words = words[1:]
    if not words:
        return False
    name = os.path.basename(words[0])
    if name == "rg":
        return True
    if name not in ("grep", "egrep", "fgrep", "diff"):
        return False
    for word in words[1:]:
        if "recurse" in word or (len(word) >= 3 and "recurse".startswith(word.split("=")[-1].lstrip("-"))):
            return True  # `-d recurse`, `--directories=recurse`, and GNU's prefixes of it (`-d rec`)
        if name != "diff" and (word in ("-d", "-D") or word.startswith(("-d", "--d"))):
            return True  # grep's `-d ACTION` / `--directories=ACTION` / `--devices`: read wide, it only asks
        if word.startswith("--"):
            opt = word.split("=", 1)[0]
            if (len(opt) >= 5 and "--recursive".startswith(opt)) or (
                    len(opt) >= 5 and "--dereference-recursive".startswith(opt)):
                return True
        elif word.startswith("-") and ("r" in word[1:] or "R" in word[1:]):
            return True
    return False


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


def _held_commands(command: str) -> list[_Held] | None:
    """The simple commands of `command`, read the way `shlex` reads them (quotes
    removed, `$` and globs left as text, every newline a separator); None when
    it cannot be read (an unclosed quote)."""
    lex = shlex.shlex(command.replace("\n", " ; "), posix=True, punctuation_chars=True)
    lex.whitespace_split = True
    lex.commenters = ""
    try:
        tokens = list(lex)
    except ValueError:
        return None
    out = [_Held([], [], False)]
    k = 0
    while k < len(tokens):
        tok = tokens[k]
        if tok and set(tok) <= _PUNCT:
            if "<" in tok or ">" in tok:  # a redirect: the next word is its target
                target = tokens[k + 1] if k + 1 < len(tokens) else ""
                if tok == "<" and target:
                    out[-1].stdin.append(target)
                elif target:
                    out[-1].targets.append(target)
                k += 2
                continue
            out.append(_Held([], [], tok in ("|", "|&")))
        else:
            out[-1].words.append(tok)
        k += 1
    return [c for c in out if c.words]


def _held_dirs(commands: list[_Held], cwd: str, home: str) -> list[str]:
    """Every folder the command may run in: its own, and every `cd` / `pushd` target
    (read against all the folders seen so far: an over-approximation). A `cd` in a
    pipeline moves nothing in bash, and is counted all the same: that only adds a
    folder to look in (its own is never dropped), the safe side for what this
    feeds (`names_writable`, `held_scripts`)."""
    dirs = [cwd]
    for c in commands:
        if c.words[0] in ("cd", "pushd") and len(c.words) > 1:
            for real in _held_resolve(c.words[-1], dirs, home):
                if real not in dirs:
                    dirs.append(real)
    return dirs


def _held_resolve(word: str, dirs: list[str], home: str) -> list[str]:
    if word == "~" or word.startswith("~/"):
        word = home + word[1:]
    out: list[str] = []
    for d in dirs:
        joined = os.path.join(d, word)
        for path in (_norm(joined), os.path.realpath(joined)):
            if path not in out:
                out.append(path)
    return out


#: The files `probe` keeps beside a checked-out document (`note_sync.Paths`: the
#: base copy, its version and owner, the lock; `summary_cli`'s visuals version):
#: never the daemon's to write. A forged version would push stale text past the
#: server's concurrent-edit and erasure checks.
_BOOKKEEPING = (".base", ".meta.json", ".lock", ".owner")
#: Any case: macOS and Windows file systems ignore it, so `X.BASE` is `X.base`.
_BOOKKEEPING_NAMED = re.compile(r"""[^\s'"`;|&<>()=]*(?:\.base|\.meta\.json|\.lock|\.owner)(?=$|[\s'"`;|&<>()])""", re.I)


def _record_hashes() -> dict[str, str]:
    """Real path -> sha256 (RECORD's urlsafe base64) of every file the installed
    `probe-research` package lists in its RECORD; empty when it has none."""
    global _RECORD
    if _RECORD is None:
        found: dict[str, str] = {}
        try:
            from importlib import metadata

            dist = metadata.distribution("probe-research")
            for entry in dist.files or []:
                if entry.hash is not None and entry.hash.mode == "sha256":
                    found[os.path.realpath(str(dist.locate_file(entry)))] = entry.hash.value
        except Exception:  # noqa: BLE001 -- no package metadata: no file is the package's
            found = {}
        _RECORD = found
    return _RECORD


_RECORD: dict[str, str] | None = None


def packaged_file(real: str) -> bool:
    """Is `real` a file of the installed package, as its RECORD lists it: the
    path AND its content (sha256)? A second name another file was given there
    (a hard link to a key) does not hash alike."""
    import base64
    import hashlib

    want = _record_hashes().get(real)
    if want is None:
        return False
    try:
        with open(real, "rb") as handle:
            digest = hashlib.sha256(handle.read(4 * 1024 * 1024 + 1)).digest()
    except OSError:
        return False
    return base64.urlsafe_b64encode(digest).rstrip(b"=").decode() == want


#: Words of a command line, as the bookkeeping ban reads them (quotes already gone).
_TOKENS = re.compile(r"[^\s;|&<>()=]+")
#: What can stand for other characters in a name: globs, braces, expansions.
_STANDS_IN = "?*[{$`"


def _unquoted(text: str) -> str:
    """`text` without quotes and backslashes, as bash joins the pieces of a word
    (`x.md.ba''se`, `x.md.ba\\se`, `x.md."BASE"` are all `x.md.base`)."""
    return re.sub(r"[\"'\\]", "", text)


def _fold(path: str) -> str:
    """`path` without case where the file system ignores it (macOS, Windows):
    `~/.local/STATE/probe/notes` is the notes folder there."""
    return path.casefold() if sys.platform == "darwin" or os.name == "nt" else path


def _could_be_bookkeeping(name: str) -> bool:
    """Could this file name, as written, be a checkout's bookkeeping file? Its
    suffix in any case, or a glob, brace or expansion that could expand to one
    (`x.md.bas?`, `x.md.ba[s]e`, `x.md.b*`, `x.md.ba{s,}e`)."""
    import fnmatch

    folded = name.casefold()
    if folded.endswith(_BOOKKEEPING):
        return True
    if not any(c in folded for c in _STANDS_IN):
        return False
    if any(c in folded for c in "{$`"):
        return True  # expands to what the text does not show
    literal = re.split(r"[?*\[]", folded, maxsplit=1)[0]
    return any(fnmatch.fnmatchcase(literal + suffix[j:], folded)
               for suffix in _BOOKKEEPING for j in range(len(suffix) + 1)
               if (literal + suffix[j:]).endswith(suffix))


def is_bookkeeping(name: str) -> bool:
    """A checkout's base copy, version or lock (`_BOOKKEEPING`), in any case."""
    return name.casefold().endswith(_BOOKKEEPING)


def names_writable(command: str, *, cwd: Path, home: Path, folders: Sequence[Path]) -> str | None:
    """A word of `command` naming `folders` (the notes the daemon writes without a
    question) or a file in them, else None. Such a command is never asked: a yes
    to it could run text nobody was shown. Read broadly on purpose: every word
    (and the parts of `--opt=VALUE` / `A:B`), in every folder a `cd` may reach,
    and the folders' paths anywhere in the text."""
    home_s = _norm(os.path.abspath(str(home)))
    roots: list[str] = []
    for folder in folders:
        for path in (_norm(os.path.abspath(str(folder))), os.path.realpath(str(folder))):
            if path not in roots:
                roots.append(path)
    if not roots:
        return None
    for root in roots:
        forms = [root]
        if _inside(root, home_s) and root != home_s:
            rel = root[len(home_s) + 1 :]
            forms += [f"~/{rel}", f"$HOME/{rel}", f"${{HOME}}/{rel}"]
        if any(form in command for form in forms):
            return root
    commands = _held_commands(command)
    if commands is None:
        return None  # the caller refuses a command it cannot read (`held_scripts`)
    dirs = _held_dirs(commands, os.path.realpath(str(cwd)), home_s)
    for c in commands:
        for word in [*c.words, *c.stdin, *c.targets]:
            for piece in {word, *re.split(r"[=:]", word)}:
                if not piece:
                    continue
                for real in _held_resolve(piece, dirs, home_s):
                    if any(_inside(real, root) for root in roots):
                        return real
    return None


def _runner(name: str) -> str | None:
    if name in _SHELL_RUNNERS:
        return "shell"
    return next((family for pattern, family in _RUNNER_FAMILY if pattern.fullmatch(name)), None)


def held_scripts(command: str, *, cwd: Path, home: Path) -> list[str] | None:
    """The files `command` runs as code, whose text its words do not show: a
    program named by its path (`./run.sh`), `source FILE` / `. FILE`, the script
    of bash / sh / zsh / python / perl / node / ruby (behind env, sudo, nohup,
    timeout...), and what such an interpreter reads on stdin when it has no
    script (`bash < f`, `cat f | python`). Realpaths, whether or not they exist
    yet, in every folder a `cd` may reach. None when the command cannot be read."""
    commands = _held_commands(command)
    if commands is None:
        return None
    home_s = _norm(os.path.abspath(str(home)))
    dirs = _held_dirs(commands, os.path.realpath(str(cwd)), home_s)
    found: list[str] = []

    def add(word: str) -> None:
        for real in _held_resolve(word, dirs, home_s):
            if real not in found:
                found.append(real)

    def scan(words: list[str], c: _Held, previous: list[_Held], depth: int) -> None:
        k = 0
        while k < len(words) and _ASSIGNMENT.match(words[k]):
            k += 1
        # Wrappers run the rest: env, sudo, nohup, timeout 10, nice -n 5, xargs...
        while k < len(words) and os.path.basename(words[k]) in _WRAPPERS - _SHELL_RUNNERS - {".", "source"}:
            if words[k] == "eval" and depth < 3:  # its words are one command line
                for n in _held_commands(" ".join(words[k + 1 :])) or []:
                    scan(n.words, n, [], depth + 1)
                return
            k += 1
            while k < len(words) and (words[k].startswith(("-", "+")) or _ASSIGNMENT.match(words[k])
                                      or re.fullmatch(r"[0-9.]+[smhd]?", words[k])):
                if words[k] == "-c" and k + 1 < len(words) and depth < 3:
                    nested = _held_commands(words[k + 1]) or []
                    for n in nested:
                        scan(n.words, n, [], depth + 1)
                    return
                k += 2 if words[k] in _WRAPPER_VALUES else 1
        if k >= len(words):
            return
        program = words[k]
        if "/" in program:
            add(program)
        name = os.path.basename(program)
        rest = words[k + 1 :]
        if name in (".", "source"):
            if rest:
                add(rest[0])
            return
        family = _runner(name)
        if family is None:
            return
        values, code = _RUNNER_OPTIONS[family]
        j = 0
        while j < len(rest):
            word = rest[j]
            # `-c`, or a cluster ending in it (`bash -lc`, `perl -ne`, `python -Bc`).
            if word in code or (word[:1] == "-" and word[1:2] not in ("-", "") and f"-{word[-1]}" in code):
                if family == "shell" and j + 1 < len(rest) and depth < 3:
                    for n in _held_commands(rest[j + 1]) or []:
                        scan(n.words, n, [], depth + 1)
                return
            if word in values:
                j += 2
                continue
            if word in ("-", "-s") or word == "--":
                j += 1
                if word == "--" and j < len(rest):
                    add(rest[j])
                    return
                continue
            if word.startswith(("-", "+")):
                j += 1
                continue
            add(word)
            return
        # No script on the command line: it reads its code from stdin.
        for target in c.stdin:
            add(target)
        if c.piped:
            for p in previous:
                for word in [*p.words[1:], *p.stdin]:
                    if not word.startswith("-") and any(os.path.isfile(r) for r in _held_resolve(word, dirs, home_s)):
                        add(word)

    pipeline: list[_Held] = []
    for c in commands:
        pipeline = [*pipeline, c] if c.piped else [c]
        scan(c.words, c, pipeline[:-1], 0)
    return found


# --- the runner ------------------------------------------------------------

#: git settings forced on every command (the highest-precedence config level).
_GIT_CONFIG = (
    ("core.hooksPath", "/dev/null"),
    ("core.fsmonitor", "false"),
    ("core.pager", "cat"),
    ("diff.external", ""),
    ("core.sshCommand", "false"),
    ("protocol.allow", "never"),
    ("log.showSignature", "false"),
    ("gpg.program", "false"),
    ("gpg.openpgp.program", "false"),
    ("gpg.x509.program", "false"),
    ("gpg.ssh.program", "false"),
    ("diff.ignoreSubmodules", "all"),
    ("status.submoduleSummary", "false"),
    ("submodule.recurse", "false"),
)
#: Per-driver programs a repository can name; `run` blanks every one it defines.
_GIT_DRIVER_KEYS = r"^(filter|diff)\..+\.(clean|smudge|process|textconv|command)$"


#: A config path that never exists, so a `probe` run by the daemon's shell has no key.
NO_PROBE_CONFIG = DAEMON_SHELL_CONFIG


def minimal_env(env_extra: dict[str, str] | None = None) -> dict[str, str]:
    """The whole environment a command gets: nothing from the parent but PATH and HOME.

    No Probe token, no API keys, no BASH_ENV (bash would source it), no GIT_DIR.
    And no Probe config: `PROBE_CONFIG_PATH` names a file that does not exist, so a
    `probe` started from here has no key and writes nothing -- the daemon writes to
    Probe only through its probe tool (pre-check, lease, logbook), even when bypass
    mode runs whatever the shell is given.
    """
    env = {
        "PATH": _clean_path(os.environ.get("PATH")),
        "HOME": os.environ.get("HOME") or str(Path.home()),
        "LANG": "C.UTF-8",
        "LC_ALL": "C.UTF-8",
        "TERM": "dumb",
        "NO_COLOR": "1",
        # `python -c` imports nothing from the folder it runs in (Python 3.11+), and
        # writes no `.pyc`: a command Jev approved runs only the code its text shows.
        "PYTHONSAFEPATH": "1",
        "PYTHONDONTWRITEBYTECODE": "1",
        "PAGER": "cat",
        "GIT_PAGER": "cat",
        "GIT_TERMINAL_PROMPT": "0",
        "GIT_CONFIG_NOSYSTEM": "1",
        "GIT_OPTIONAL_LOCKS": "0",  # reads never rewrite the index (no post-index-change hook)
        "GIT_CONFIG_COUNT": str(len(_GIT_CONFIG)),
        "PROBE_CONFIG_PATH": NO_PROBE_CONFIG,
        "PROBE_TELEMETRY": "off",
    }
    for n, (key, value) in enumerate(_GIT_CONFIG):
        env[f"GIT_CONFIG_KEY_{n}"] = key
        env[f"GIT_CONFIG_VALUE_{n}"] = value
    if env_extra:
        env.update(env_extra)
    return env


def _git_dirs(command: str, cwd: str, home: str) -> set[str]:
    """The folders git may run in during `command` (best effort; for blanking drivers)."""
    try:
        parts = _split(_tokenize(command))
    except _Refuse:
        return {cwd} if re.search(r"\bgit\b", command) else set()
    dirs: set[str] = set()
    for part, cands in _walk(parts, cwd, home):
        words = part.words
        if not words or os.path.basename(words[0].value) != "git":
            continue
        here = {os.path.realpath(c) for c in cands}
        k = 1
        while k < len(words) and words[k].value.startswith("-"):
            if words[k].value == "-C" and k + 1 < len(words):
                path = _expand(words[k + 1], home)
                here = {os.path.realpath(os.path.join(d, path)) for d in here}
                k += 1
            k += 1
        dirs |= here
    return {d for d in dirs if os.path.isdir(d)}


async def _blank_git_drivers(env: dict[str, str], dirs: set[str]) -> None:
    """Add a blank value for every filter / diff driver program the repositories define.

    A clean filter runs inside `git status` and `git diff`, and there is no flag
    to turn it off; a blank command is skipped. `git config` itself runs nothing.
    """
    keys: set[str] = set()
    for folder in sorted(dirs):
        try:
            proc = await asyncio.create_subprocess_exec(
                "git", "config", "-z", "--get-regexp", _GIT_DRIVER_KEYS,
                cwd=folder, env=env, stdin=asyncio.subprocess.DEVNULL,
                stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.DEVNULL,
            )  # fmt: skip
        except OSError:
            return  # no git: nothing to protect
        try:
            out, _ = await asyncio.wait_for(proc.communicate(), 10)
        except TimeoutError:
            proc.kill()
            await proc.wait()
            continue
        for entry in out.decode("utf-8", "replace").split("\0"):
            key = entry.split("\n", 1)[0]
            if key:
                keys.add(key)
    n = int(env.get("GIT_CONFIG_COUNT", "0"))
    for key in sorted(keys):
        env[f"GIT_CONFIG_KEY_{n}"] = key
        env[f"GIT_CONFIG_VALUE_{n}"] = ""
        n += 1
    env["GIT_CONFIG_COUNT"] = str(n)


class _Capture:
    """Keeps the first and last `keep` bytes of a stream, counting the rest."""

    def __init__(self, keep: int) -> None:
        self.keep = keep
        self.head = bytearray()
        self.tail = bytearray()
        self.total = 0

    def feed(self, chunk: bytes) -> None:
        self.total += len(chunk)
        room = self.keep - len(self.head)
        if room > 0:
            self.head += chunk[:room]
            chunk = chunk[room:]
        if chunk:
            self.tail += chunk
            if len(self.tail) > self.keep:
                del self.tail[: len(self.tail) - self.keep]

    def text(self, max_chars: int) -> tuple[str, bool]:
        dropped = self.total - len(self.head) - len(self.tail)
        if dropped == 0:
            full = (self.head + self.tail).decode("utf-8", "replace")
            if len(full) <= max_chars:
                return full, False
            head_text, tail_text = full, full
        else:
            head_text = self.head.decode("utf-8", "replace")
            tail_text = self.tail.decode("utf-8", "replace")
        half = max(max_chars // 2, 1)
        head_text, tail_text = head_text[:half], tail_text[-half:]
        kept = len(head_text.encode()) + len(tail_text.encode())
        marker = f"\n[... {max(self.total - kept, 0)} bytes of output left out ...]\n"
        return head_text + marker + tail_text, True


def _kill_group(proc: asyncio.subprocess.Process) -> None:
    try:
        os.killpg(proc.pid, signal.SIGKILL)
    except (ProcessLookupError, PermissionError):
        pass


#: How often `run` asks its `watch` whether the command may go on.
WATCH_POLL_S = 1.0
#: How long a killed process group is waited for before `run` gives up on reaping it.
REAP_S = 5.0


async def stop_group(proc: asyncio.subprocess.Process, reader: asyncio.Future | None = None) -> None:
    """Kill the command's whole process group and reap it (bounded), whatever
    else is happening: also on the way out of a cancelled task, so a bite cut
    short at the session's end leaves nothing running behind it."""
    _kill_group(proc)
    cancelled = False  # a cancellation that arrives meanwhile is passed on once the group is reaped
    if reader is not None:
        try:
            await asyncio.wait({reader}, timeout=REAP_S)
        except asyncio.CancelledError:
            cancelled = True
        if not reader.done():
            reader.cancel()
        elif not reader.cancelled():
            reader.exception()  # retrieved: a pipe error of a killed command is not news
    try:
        await asyncio.wait_for(proc.wait(), REAP_S)
    except asyncio.CancelledError:
        cancelled = True
    except (TimeoutError, OSError):
        pass  # a group that will not die in time: it was killed, and the loop reaps it later
    if cancelled:
        raise asyncio.CancelledError


async def run(
    command: str,
    *,
    cwd: Path,
    timeout_s: float = 60,
    max_output_chars: int = 30_000,
    env_extra: dict[str, str] | None = None,
    watch: Callable[[], str | None] | None = None,
    stdin: bytes | None = None,
) -> ShellResult:
    """Run a command `classify` passed (or the researcher approved).

    `/bin/bash --noprofile --norc`, `minimal_env()`, stdin closed (or `stdin`'s
    bytes, from an unlinked temporary file: a probe command's output fed to a
    filter), stdout and stderr together. At `timeout_s` the whole process group is killed. `watch`,
    asked right before the launch and every `WATCH_POLL_S` while it runs, returns
    why it must stop now (the daemon's lease: the researcher moved the switch) or
    None; nothing is started, or the group is killed, and the result says so in
    `stopped`. A cancelled caller kills and
    reaps the group before the cancellation goes on.
    """
    env = minimal_env(env_extra)
    dirs = _git_dirs(command, os.path.realpath(str(cwd)), env["HOME"])
    if dirs:
        await _blank_git_drivers(env, dirs)
    # Asked once more right before the launch: preparing git awaited subprocesses,
    # and the answer may have changed meanwhile. A stop now starts nothing.
    stopped = watch() if watch is not None else None
    if stopped is not None:
        return ShellResult(exit_code=None, output="", truncated=False, timed_out=False, stopped=stopped,
                           started=False)
    source = None
    if stdin is not None:
        source = tempfile.TemporaryFile()
        source.write(stdin)
        source.seek(0)
    try:
        proc = await asyncio.create_subprocess_exec(
            "/bin/bash", "--noprofile", "--norc", "-c", "--", command,
            cwd=str(cwd), env=env, stdin=source if source is not None else asyncio.subprocess.DEVNULL,
            stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.STDOUT,
            start_new_session=True,  # its own process group, so a timeout kills everything
        )  # fmt: skip
    finally:
        if source is not None:
            source.close()  # the command holds its own copy of the file
    capture = _Capture(max(max_output_chars, 1) * 2)

    async def pump() -> None:
        assert proc.stdout is not None
        while chunk := await proc.stdout.read(65536):
            capture.feed(chunk)
        await proc.wait()

    reader = asyncio.ensure_future(pump())
    loop = asyncio.get_running_loop()
    deadline = loop.time() + timeout_s
    timed_out = False
    try:
        while True:
            left = deadline - loop.time()
            if left <= 0:
                timed_out = True
                break
            done, _ = await asyncio.wait({reader}, timeout=min(WATCH_POLL_S, left) if watch else left)
            if done:
                reader.result()
                break
            if watch is not None:
                stopped = watch()
                if stopped is not None:
                    break
    except BaseException:
        await stop_group(proc, reader)
        raise
    if timed_out or stopped is not None:
        await stop_group(proc, reader)
    output, truncated = capture.text(max_output_chars)
    return ShellResult(
        exit_code=None if (timed_out or stopped is not None) else proc.returncode,
        output=output,
        truncated=truncated,
        timed_out=timed_out,
        stopped=stopped,
    )
