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

Kept behaviourally identical to the JS SDK's ``template/envFiles.ts``: a template
built through either SDK has to end up with the same environment.
"""

import base64
import re
from typing import Dict, List, Optional, Tuple

#: Where the login-shell copy is written.
PROFILE_PATH = "/etc/profile.d/99-image-env.sh"

#: Where the pam_env copy is written.
ENVIRONMENT_PATH = "/etc/environment"

#: Where the generated script is staged during the build.
SCRIPT_PATH = "/tmp/.novita-image-env.sh"

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
        # `$(` would be command substitution; `$NAME` and `${NAME}` stay live.
        .replace("$(", "\\$(")
    )
    return f'"{escaped}"'


def env_files_script(envs: Dict[str, str]) -> str:
    """The shell script that writes both files.

    Runs during the build. For each variable it expands the declared value
    against the build's live environment, then writes the result to both files --
    quoted *differently*, which is why this is not one write:

    - profile.d is sourced by a shell, so the expanded value is single-quoted
      with ``'`` rewritten as ``'\\''``. Single quotes are the only shell quoting
      with no escapes inside them, so this is exact for any byte -- including
      ``$``, backticks and backslashes, all of which ``"..."`` would interpret.
      Writing ``KEY="value"`` here is a green that hides a wrong value: the build
      succeeds, the sandbox boots, and ``JAVA_OPTS=-Xmx2g -Dname="my app"`` holds
      something else.
    - /etc/environment is read by pam_env, which has no escape syntax at all. It
      strips one leading and one trailing quote without scanning the interior, so
      the value is written bare; and it is line-based with no continuation, so a
      value containing a newline cannot be represented there and is left to the
      profile.d copy rather than written as a corrupt second entry.
    """
    lines = ["set -e", f": > {PROFILE_PATH}", f": > {ENVIRONMENT_PATH}"]

    for name, declared in envs.items():
        lines.extend(
            [
                # Expand the declared value here, against the build's environment.
                f"v={expandable_double_quote(declared)}",
                # Export before moving on, so a later value can reference this one
                # -- `ENV VIRTUAL_ENV=/opt/venv PYTHONPATH=$VIRTUAL_ENV/lib` is
                # ordinary, and the platform's own ENV handling cannot be relied on
                # for it (it ignores PATH entirely).
                f'export {name}="$v"',
                # profile.d: single-quoted, any embedded quote closed and reopened.
                f"printf \"export {name}='%s'\\n\" "
                f"\"$(printf '%s' \"$v\" | sed \"s/'/'\\\\\\\\''/g\")\""
                f" >> {PROFILE_PATH}",
                # pam_env: bare, and only when it can represent the value at all.
                'case "$v" in',
                "  *'\"'*) v= ;;",
                "esac",
                f"[ -n \"$v\" ] && [ \"$(printf '%s' \"$v\" | wc -l)\" -eq 0 ] && "
                f"printf '{name}=%s\\n' \"$v\" >> {ENVIRONMENT_PATH}",
                # The `[ ... ] &&` above exits non-zero when the value is skipped,
                # which would abort the script under `set -e`.
                "true",
            ]
        )

    lines.append(f"chmod 0644 {PROFILE_PATH} {ENVIRONMENT_PATH}")
    return "\n".join(lines)


def env_files_command(envs: Dict[str, str]) -> Tuple[Optional[str], List[str]]:
    """The single build command that stages and runs :func:`env_files_script`.

    base64 rather than passing the script inline: it travels through the build's
    own shell before anything reads it, and base64 is the only form that survives
    that leg intact regardless of what it contains.

    Must run as root: the Dockerfile parser leaves the build as ``user``
    (measured: ``[builder 7/8] USER user``), which cannot write to ``/etc``.

    Returns ``(None, skipped)`` when no name can be carried over, so the caller
    adds no layer at all.
    """
    usable, skipped = partition_env_names(list(envs.keys()))
    if not usable:
        return None, skipped

    script = env_files_script({name: envs[name] for name in usable})
    encoded = base64.b64encode(script.encode("utf-8")).decode("ascii")

    command = " && ".join(
        [
            f"echo {encoded} | base64 -d > {SCRIPT_PATH}",
            f"sh {SCRIPT_PATH}",
            f"rm -f {SCRIPT_PATH}",
        ]
    )
    return command, skipped
