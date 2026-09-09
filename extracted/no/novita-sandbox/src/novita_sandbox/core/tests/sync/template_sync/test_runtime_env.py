"""The ENV instruction alone only reaches the build.

Measured against template `wu9ol3m99x5h2d9y63rc`, built from a Dockerfile
declaring `ENV PATH=/opt/venv/bin:$PATH`: the build logged
`[builder 4/8] ENV PATH /opt/venv/bin:$PATH`, and the sandbox reported
`PATH=/usr/local/bin:/usr/bin:/bin:...` with `/etc/environment` empty. These
tests pin the extra layer that closes that gap.

Kept in step with the JS suite (`sdk-js/src/core/tests/template/runtimeEnv.test.ts`)
-- a template built through either SDK has to end up with the same environment.
"""

import base64
import re
import subprocess
import tempfile
from pathlib import Path
from typing import Dict, List, Tuple

from novita_sandbox.core.template.env_files import (
    ENVIRONMENT_PATH,
    PROFILE_PATH,
    SCRIPT_PATH,
    env_files_command,
    env_files_script,
    partition_env_names,
    unsettable_env_name,
)
from novita_sandbox.core.template.main import TemplateBase


def _round_trip(
    declared: Dict[str, str], build_env: Dict[str, str] = None
) -> Tuple[Dict[str, str], str]:
    """Run the generated script the way the build does, then read the values back
    the way a login shell would.

    This is the check that matters. A wrong value still builds and still boots,
    so only reading it back catches it: writing the declared string verbatim was
    measured to fail the build with exit status 127, and `KEY="value"` silently
    expands `$HOME` and executes backticks at login.
    """
    build_env = build_env or {}
    tmp = Path(tempfile.mkdtemp(prefix="envfiles-"))
    profile_path = tmp / "profile.sh"
    environment_path = tmp / "environment"

    names = list(declared.keys())
    script = (
        env_files_script(declared)
        .replace(PROFILE_PATH, str(profile_path))
        .replace(ENVIRONMENT_PATH, str(environment_path))
    )

    def quote(value: str) -> str:
        return "'" + value.replace("'", "'\\''") + "'"

    # The build's own environment, as the ENV layers would have left it.
    preamble = "\n".join(f"export {k}={quote(v)}" for k, v in build_env.items())
    run_path = tmp / "run.sh"
    run_path.write_text(f"{preamble}\n{script}\n")
    subprocess.run(["sh", str(run_path)], check=True, capture_output=True)

    # NUL-separated so a value containing a newline survives the read-back.
    readback = subprocess.run(
        [
            "bash",
            "-c",
            f"set -a; . {profile_path}; set +a; "
            + "; ".join(f"printf '%s\\x00' \"${k}\"" for k in names),
        ],
        check=True,
        capture_output=True,
        text=True,
    ).stdout.split("\0")[:-1]

    return dict(zip(names, readback)), environment_path.read_text()


class TestEnvFilesScriptAgainstRealShell:
    # The PATH the platform leaves the build with: it ignores an ENV instruction
    # for PATH (measured, template s9kk2s1dhfgcqmf94785), so this is what a
    # declared `$PATH` reference must expand against.
    PLATFORM_PATH = "/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin"

    def test_declared_path_reference_expands_to_build_path(self):
        # The case this whole module exists for. Written verbatim instead, the
        # build failed with exit status 127.
        profile, _ = _round_trip(
            {"PATH": "/opt/venv/bin:$PATH"}, {"PATH": self.PLATFORM_PATH}
        )
        assert profile["PATH"] == f"/opt/venv/bin:{self.PLATFORM_PATH}"

    def test_later_value_can_reference_an_earlier_one(self):
        # `ENV VIRTUAL_ENV=/opt/venv PYTHONPATH=$VIRTUAL_ENV/lib` is ordinary, and
        # the platform's ENV handling cannot be relied on to have applied the first.
        profile, _ = _round_trip(
            {"VIRTUAL_ENV": "/opt/venv", "PYTHONPATH": "${VIRTUAL_ENV}/lib"}
        )
        assert profile["PYTHONPATH"] == "/opt/venv/lib"

    def test_reference_to_unset_expands_to_empty(self):
        profile, _ = _round_trip({"V": "x:$NOTHING_IS_SET_HERE"})
        assert profile["V"] == "x:"

    # Values measured as broken when the file was written as KEY="value": the
    # quote was lost, $HOME expanded at login, and `id` executed at login.
    def test_awkward_values_survive_verbatim(self):
        for value in [
            '-Xmx2g -Dname="my app"',
            "`id`",
            "$(id)",
            "C:\\path\\to",
            "it's",
            "line1\nline2",
            "",
            "  leading and trailing  ",
        ]:
            profile, _ = _round_trip({"V": value})
            assert profile["V"] == value, f"value {value!r} did not survive"

    def test_command_substitution_is_not_executed(self):
        # A value is data. `PATH=$(curl ...)` running during a build is not a
        # feature, and Docker expands only variable references here too.
        profile, _ = _round_trip({"V": "$(echo pwned)"})
        assert profile["V"] == "$(echo pwned)"

    def test_backtick_command_is_not_executed(self):
        profile, _ = _round_trip({"V": "`echo pwned`"})
        assert profile["V"] == "`echo pwned`"


class TestEnvironmentCopy:
    def test_holds_bare_values(self):
        # pam_env strips one layer of quotes, so the value is written bare.
        _, environment = _round_trip({"MSG": "it's fine"})
        assert "MSG=it's fine\n" in environment

    def test_omits_a_value_with_a_newline(self):
        # Line-based with no continuation: the second line would be malformed.
        profile, environment = _round_trip({"MULTI": "a\nb"})
        assert "MULTI" not in environment
        # The login shell still sees it.
        assert profile["MULTI"] == "a\nb"

    def test_omits_a_value_with_a_double_quote(self):
        # pam_env strips one leading and one trailing quote without scanning the
        # interior, so `KEY="say "hi""` would yield `say "hi`.
        profile, environment = _round_trip({"QUOTED": 'say "hi"'})
        assert "QUOTED" not in environment
        assert profile["QUOTED"] == 'say "hi"'

    def test_a_skipped_value_does_not_abort_the_script(self):
        # The script runs under `set -e`, so a skip must not look like a failure.
        _, environment = _round_trip({"BAD": "a\nb", "AFTER": "ok"})
        assert "AFTER=ok\n" in environment


class TestUnsettableEnvName:
    def test_rejects_names_no_shell_can_set(self):
        for name in ["A B", "1ABC", "A-B", "A.B", ""]:
            assert unsettable_env_name(name), name

    def test_accepts_identifiers(self):
        for name in ["PATH", "_PRIVATE", "PY3_HOME", "my_var"]:
            assert not unsettable_env_name(name), name

    def test_partition_splits_and_sorts_skipped(self):
        assert partition_env_names(["PATH", "Z Z", "HOME", "A B"]) == (
            ["PATH", "HOME"],
            ["A B", "Z Z"],
        )


def _env_writes(steps: List[dict]) -> List[Tuple[dict, str]]:
    """The RUN steps writing the runtime env files, decoded back to the script."""
    out = []
    for step in steps:
        if step["type"] != "RUN" or SCRIPT_PATH not in step["args"][0]:
            continue
        encoded = re.search(r"echo ([A-Za-z0-9+/=]+) \| base64 -d", step["args"][0])
        out.append((step, base64.b64decode(encoded.group(1)).decode()))
    return out


class TestSetEnvsRuntimeVisibility:
    def test_emits_both_the_build_env_and_a_runtime_write(self):
        t = TemplateBase()
        t.from_image("python:3.11-slim").set_envs({"PATH": "/opt/venv/bin:/usr/bin"})

        steps = t._serialize(t._instructions)["steps"]

        # Build-time behaviour is unchanged: the ENV step is still there.
        assert any(s["type"] == "ENV" for s in steps)
        # And the value is now also written where a sandbox will read it back.
        writes = _env_writes(steps)
        assert len(writes) == 1
        assert PROFILE_PATH in writes[0][1]
        assert ENVIRONMENT_PATH in writes[0][1]

    def test_leaves_a_var_reference_for_the_build_to_expand(self):
        t = TemplateBase()
        t.from_image("python:3.11-slim").set_envs({"PATH": "/opt/venv/bin:$PATH"})

        _, script = _env_writes(t._serialize(t._instructions)["steps"])[0]

        assert "/opt/venv/bin:$PATH" in script

    def test_writes_as_root(self):
        # Measured: the Dockerfile parser ends a build with
        # `[builder 7/8] USER user`, which cannot write to /etc.
        t = TemplateBase()
        builder = t.from_image("python:3.11-slim")
        builder.set_user("user")
        builder.set_envs({"FOO": "bar"})

        step, _ = _env_writes(t._serialize(t._instructions)["steps"])[0]

        assert step["args"][1] == "root"

    def test_appends_the_write_last(self):
        t = TemplateBase()
        builder = t.from_image("python:3.11-slim")
        builder.set_envs({"FOO": "bar"})
        builder.set_user("user")

        steps = t._serialize(t._instructions)["steps"]

        assert steps[-1]["type"] == "RUN"
        assert SCRIPT_PATH in steps[-1]["args"][0]
        assert steps[-1]["args"][1] == "root"

    def test_one_layer_holds_every_call(self):
        t = TemplateBase()
        builder = t.from_image("python:3.11-slim")
        builder.set_envs({"A": "1"})
        builder.set_envs({"B": "2"})

        writes = _env_writes(t._serialize(t._instructions)["steps"])

        # A per-call write would have the second clobber the first's file.
        assert len(writes) == 1
        assert "A=" in writes[0][1]
        assert "B=" in writes[0][1]

    def test_a_later_call_wins_for_a_repeated_name(self):
        t = TemplateBase()
        builder = t.from_image("python:3.11-slim")
        builder.set_envs({"PATH": "/first"})
        builder.set_envs({"PATH": "/second"})

        _, script = _env_writes(t._serialize(t._instructions)["steps"])[0]

        assert "/second" in script
        assert "/first" not in script

    def test_skips_a_name_no_shell_can_set(self):
        # `export A B='v'` is two statements, so carrying this over would set
        # something other than what was asked for.
        t = TemplateBase()
        t.from_image("python:3.11-slim").set_envs({"A B": "v"})

        steps = t._serialize(t._instructions)["steps"]

        assert any(s["type"] == "ENV" for s in steps)
        assert _env_writes(steps) == []

    def test_adds_nothing_when_no_environment_was_set(self):
        t = TemplateBase()
        t.from_image("python:3.11-slim")

        assert _env_writes(t._serialize(t._instructions)["steps"]) == []

    def test_does_not_duplicate_the_layer_when_serialized_twice(self):
        t = TemplateBase()
        t.from_image("python:3.11-slim").set_envs({"FOO": "bar"})

        t._serialize(t._instructions)
        assert len(_env_writes(t._serialize(t._instructions)["steps"])) == 1

    def test_covers_env_declared_in_a_dockerfile(self):
        t = TemplateBase()
        t.from_dockerfile("FROM python:3.11-slim\nENV PATH=/opt/venv/bin:$PATH\n")

        writes = _env_writes(t._serialize(t._instructions)["steps"])

        assert len(writes) == 1
        assert "/opt/venv/bin:$PATH" in writes[0][1]


class TestJsParity:
    def test_command_shape_matches_the_js_sdk(self):
        command, skipped = env_files_command({"PATH": "/opt/venv/bin"})

        assert command is not None
        assert "base64 -d >" in command
        assert "rm -f" in command
        assert skipped == []

    def test_no_command_when_every_name_is_unsettable(self):
        command, skipped = env_files_command({"A B": "v"})

        assert command is None
        assert skipped == ["A B"]

    def test_no_command_for_an_empty_set(self):
        assert env_files_command({})[0] is None
