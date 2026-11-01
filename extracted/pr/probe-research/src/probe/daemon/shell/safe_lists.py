"""the safe lists: programs, allowed options, secret/private/harness file names (data, plus the harness-file mover)."""

from __future__ import annotations
import os
import re
import sys

from probe.foundation.harness_registry import get_registry


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
