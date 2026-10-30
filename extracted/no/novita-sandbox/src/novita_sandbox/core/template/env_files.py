"""Make a template's environment variables visible at *runtime*, not just at
build time.

`set_envs` records an ENV instruction. Two things were measured about it, and
neither reports an error:

**The build's ENV does not reach the sandbox.** Template
`wu9ol3m99x5h2d9y63rc`, built from a Dockerfile declaring
`ENV PATH=/opt/venv/bin:$PATH`::

    build log      [builder 4/8] ENV PATH /opt/venv/bin:$PATH   (layer created)
    sandbox        PATH=/usr/local/bin:/usr/bin:/bin:...        (venv absent)
    which python3  /usr/local/bin/python3                       (not the venv)
    import requests -> exit 1                                   (installed, unreachable)

A login shell and ``sh -c`` saw the same thing, and ``/etc/environment`` was
empty. So the environment is written to the filesystem, where the sandbox's own
shell startup reads it back -- twice, because neither file covers both cases:

    /etc/profile.d/99-image-env.sh   sourced by login shells
    /etc/environment                 read by pam_env, covers non-login execution

**The platform silently ignores an ENV instruction for PATH.** Template
`s9kk2s1dhfgcqmf94785` set ``PATH=/opt/venv/bin:$PATH`` and ``PROBE_LITERAL=x``
in one instruction; the next build step reported::

    SEEN_PATH=[/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin]
    SEEN_LITERAL=[x]

-- PATH untouched, not even holding a literal ``$PATH``, while the other
variable took effect. So the value cannot simply be read back out of the build
environment: for PATH that reads the platform's own value, and PATH is where a
venv or conda prefix lives -- the case this exists to fix.

The declared string is therefore carried into the build and its variable
references are expanded *there*. Writing the declared string verbatim instead
breaks the build outright::

    [builder 9/9] RUN ... export PATH='/opt/venv/bin:$PATH' ...   (step ok)
    [finalize]    Build failed: configuration script failed: exit status 127

PATH held a literal ``$PATH``, so the next command was not found.

Uses the same runtime files as the standard SDK, while preserving base-template
values and distinguishing registry literals from builder declarations.
"""

import base64
import re
import shlex
from typing import Dict, List, Optional, Tuple

#: Where the login-shell copy is written.
PROFILE_PATH = "/etc/profile.d/99-image-env.sh"

#: Where the pam_env copy is written.
ENVIRONMENT_PATH = "/etc/environment"

#: Where the generated script is staged during the build.
SCRIPT_PATH = "/tmp/.novita-image-env.sh"

# Kept out of /tmp because user build steps commonly clear it.
BASE_ENV_PATH = "/etc/.novita-image-env-base.sh"

_NAME_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")


def unsettable_env_name(name: str) -> bool:
    """True when no shell can set this name, so it cannot be restored at runtime.

    ``export A B='v'`` is two statements, so carrying over a name with a space in
    it would set something other than what was asked for. Reported rather than
    written, so a caller is not told a variable survived when it did not.
    """
    return not _NAME_RE.match(name)


def partition_env_names(names: List[str]) -> Tuple[List[str], List[str]]:
    """Split names into ``(usable, skipped)``; ``skipped`` is sorted."""
    usable: List[str] = []
    skipped: List[str] = []
    for name in names:
        if unsettable_env_name(name):
            skipped.append(name)
        else:
            usable.append(name)
    return usable, sorted(skipped)


def expandable_double_quote(value: str) -> str:
    """Quote a declared value for the generated script, leaving ``$VAR`` live.

    The value is emitted inside a double-quoted shell word, so ``$VAR`` and
    ``${VAR}`` expand against the build's environment -- which is the whole
    point, since ``/opt/venv/bin:$PATH`` only means anything there.

    Backticks, ``$(``, ``"`` and ``\\`` are escaped, so a value cannot run a
    command or end the word. Command substitution is deliberately *not* honoured:
    a value is data, and ``PATH=$(curl ...)`` executing during someone else's
    build is not a feature. Docker expands only variable references here too.
    """
    escaped = (
        # Backslash first, so the escapes added below are not re-escaped.
        value.replace("\\", "\\\\")
        .replace('"', '\\"')
        .replace("`", "\\`")
    )
    # Only named references are declarations. Positional/special parameters and
    # command substitution remain literal data.
    escaped = re.sub(r"\$(?![A-Za-z_]|\{[A-Za-z_][A-Za-z0-9_]*\})", r"\\$", escaped)
    return f'"{escaped}"'


def env_files_script(
    envs: Dict[str, str],
    literal_envs: Optional[Dict[str, str]] = None,
    env_groups: Optional[List[Tuple[Dict[str, str], bool]]] = None,
    base_env_path: Optional[str] = None,
) -> str:
    """Evaluate declarations in order and persist only runtime values.

    Arguments to each function call are expanded before any assignment in that
    group. Build-only declarations affect subsequent expansion but never write
    runtime files. POSIX command -p keeps helpers independent of the target PATH.
    """
    groups = (
        env_groups
        if env_groups is not None
        else [({name: value}, True) for name, value in envs.items()]
    )
    lines = [
        "set -e",
        # A builder restores the snapshot taken before user ENV instructions.
        # Standalone calls without a snapshot use their current base environment.
        f". {shlex.quote(base_env_path)}" if base_env_path else ":",
        f"command -p rm -f {shlex.quote(base_env_path)}" if base_env_path else ":",
        f'if [ -f "{PROFILE_PATH}" ]; then . "{PROFILE_PATH}"; fi',
        f'command -p touch "{PROFILE_PATH}" "{ENVIRONMENT_PATH}"',
        "__novita_build_env() {",
        '  while [ "$#" -gt 0 ]; do export "$1=$2"; shift 2; done',
        "}",
        "__novita_runtime_env() {",
        '  while [ "$#" -gt 0 ]; do',
        '    export "$1=$2"',
        # Avoid command substitution: it strips trailing newlines from values.
        f'    printf "export %s=\'" "$1" >> {PROFILE_PATH}',
        f"""    printf '%s' "$2" | command -p sed "s/'/'\\\\\\\\''/g" >> {PROFILE_PATH}""",
        f"""    printf "'\\n" >> {PROFILE_PATH}""",
        f'    command -p sed "/^$1=/d" {ENVIRONMENT_PATH} > {ENVIRONMENT_PATH}.tmp',
        f"    command -p cat {ENVIRONMENT_PATH}.tmp > {ENVIRONMENT_PATH}",
        f"    command -p rm -f {ENVIRONMENT_PATH}.tmp",
        '    case "$2" in',
        "      *'\"'*) ;;",
        f"""      *) if [ "$(printf '%s' "$2" | command -p wc -l)" -eq 0 ]; then printf '%s=%s\\n' "$1" "$2" >> {ENVIRONMENT_PATH}; fi ;;""",
        "    esac",
        "    shift 2",
        "  done",
        "}",
    ]
    if literal_envs:
        lines.append(
            "__novita_runtime_env "
            + " ".join(
                f"{name} {shlex.quote(value)}" for name, value in literal_envs.items()
            )
        )
    groups = (
        env_groups
        if env_groups is not None
        else [({name: value}, True) for name, value in envs.items()]
    )
    for declarations, runtime in groups:
        if declarations:
            function = "__novita_runtime_env" if runtime else "__novita_build_env"
            lines.append(
                function
                + " "
                + " ".join(
                    f"{name} {expandable_double_quote(value)}"
                    for name, value in declarations.items()
                )
            )
    lines.append(f"command -p chmod 0644 {PROFILE_PATH} {ENVIRONMENT_PATH}")
    return "\n".join(lines)


def env_files_command(
    envs: Dict[str, str],
    literal_envs: Optional[Dict[str, str]] = None,
    env_groups: Optional[List[Tuple[Dict[str, str], bool]]] = None,
    base_env_path: Optional[str] = None,
) -> Tuple[Optional[str], List[str]]:
    """Stage the runtime writer as root, preserving declaration boundaries."""
    literal_envs = literal_envs or {}
    groups = (
        env_groups
        if env_groups is not None
        else [({name: value}, True) for name, value in envs.items()]
    )
    names = list(
        dict.fromkeys([*literal_envs, *(name for group, _ in groups for name in group)])
    )
    usable, skipped = partition_env_names(names)
    usable_set = set(usable)
    literals = {
        name: value for name, value in literal_envs.items() if name in usable_set
    }
    filtered_groups = [
        ({name: value for name, value in group.items() if name in usable_set}, runtime)
        for group, runtime in groups
    ]
    if not literals and not any(
        group and runtime for group, runtime in filtered_groups
    ):
        return None, skipped
    script = env_files_script({}, literals, filtered_groups, base_env_path)
    encoded = base64.b64encode(script.encode("utf-8")).decode("ascii")

    command = " && ".join(
        [
            f"echo {encoded} | command -p base64 -d > {SCRIPT_PATH}",
            f"command -p sh {SCRIPT_PATH}",
            f"command -p rm -f {SCRIPT_PATH}",
        ]
    )
    return command, skipped


def env_snapshot_command(
    env_groups: List[Tuple[Dict[str, str], bool]]
) -> Optional[str]:
    """Capture declared names before build ENV instructions can change them."""
    names, _ = partition_env_names(
        list(dict.fromkeys(name for group, _ in env_groups for name in group))
    )
    if not names:
        return None
    lines = ["set -e", "umask 077", f": > {BASE_ENV_PATH}", f"command -p chmod 0600 {BASE_ENV_PATH}"]
    for name in names:
        lines.extend(
            [
                f'if [ "${{{name}+x}}" = x ]; then',
                f'  printf "export {name}=\'" >> {BASE_ENV_PATH}',
                f"""    printf '%s' "${{{name}}}" | command -p sed "s/'/'\\\\\\\\''/g" >> {BASE_ENV_PATH}""",
                f"""  printf "'\\n" >> {BASE_ENV_PATH}""",
                "else",
                f"  printf 'unset {name}\\n' >> {BASE_ENV_PATH}",
                "fi",
            ]
        )
    return "command -p sh -c " + shlex.quote("\n".join(lines))
