"""Offline customer regressions for environment lifetime and registry reads."""
import base64
import json
import re
import subprocess

import httpx
import pytest

from novita_sandbox import TemplateBase
from novita_sandbox.core.template import main as template_main
from novita_sandbox.core.template import image_config
from novita_sandbox.core.template.env_files import (
    PROFILE_PATH,
    ENVIRONMENT_PATH,
    SCRIPT_PATH,
    BASE_ENV_PATH,
)
from novita_sandbox.core.template.image_config import ImageConfig


def serialize(template):
    return json.loads(TemplateBase.to_json(template))


def run_environment(template, tmp_path, names, base_profile="", base_env=None):
    payload = serialize(template)
    command = next(
        s["args"][0] for s in payload["steps"] if SCRIPT_PATH in " ".join(s["args"])
    )
    encoded = re.search(
        r"echo ([A-Za-z0-9+/=]+) \| (?:command -p )?base64 -d", command
    ).group(1)
    profile, environment = tmp_path / "profile", tmp_path / "environment"
    profile.write_text(base_profile)
    environment.write_text("")
    initial = {"PATH": "/usr/bin:/bin", **(base_env or {})}
    final = dict(initial)
    snapshot = tmp_path / "base-env"
    if any(BASE_ENV_PATH in step["args"][0] for step in payload["steps"]):
        snapshot.write_text("old")
        snapshot.chmod(0o644)
    for step in payload["steps"]:
        if step["type"] == "RUN" and BASE_ENV_PATH in step["args"][0]:
            subprocess.run(
                [
                    "/bin/sh",
                    "-c",
                    step["args"][0].replace(BASE_ENV_PATH, str(snapshot)),
                ],
                env=initial,
                check=True,
                capture_output=True,
            )
            assert snapshot.stat().st_mode & 0o777 == 0o600
        if step["type"] == "ENV":
            final.update(
                {
                    k: v
                    for k, v in zip(step["args"][::2], step["args"][1::2])
                    if k != "PATH"
                }
            )
    script = (
        base64.b64decode(encoded)
        .decode()
        .replace(PROFILE_PATH, str(profile))
        .replace(ENVIRONMENT_PATH, str(environment))
        .replace(BASE_ENV_PATH, str(snapshot))
    )
    subprocess.run(
        ["/bin/sh", "-c", script], env=final, check=True, capture_output=True
    )
    assert not snapshot.exists()
    result = subprocess.run(
        [
            "/bin/sh",
            "-c",
            '. "$1"; shift; for name; do eval \'printf "%s\\0" "${\'"$name"\'-}"\'; done',
            "sh",
            str(profile),
            *names,
        ],
        env={"PATH": "/usr/bin:/bin"},
        check=True,
        capture_output=True,
    )
    return (
        dict(zip(names, result.stdout.decode().split("\0")[:-1])),
        environment.read_text(),
        profile.read_text(),
    )


@pytest.fixture
def image(monkeypatch):
    monkeypatch.setattr(
        template_main,
        "fetch_image_config",
        lambda *a, **kw: ImageConfig(
            env={"PATH": "/usr/bin:/bin", "PRICE": "cost$5"},
            workdir="/app",
            cmd=["./start"],
        ),
    )


def test_default_envs_remain_build_only():
    data = serialize(
        TemplateBase().from_template("base").set_envs({"BUILD_TOKEN": "fixture"})
    )
    assert any(s["type"] == "ENV" for s in data["steps"])
    assert not any(SCRIPT_PATH in " ".join(s["args"]) for s in data["steps"])


def test_dockerfile_arg_is_build_only_but_env_is_runtime(image, tmp_path):
    template = TemplateBase().from_dockerfile(
        "FROM registry.test/app\nARG BUILD_TOKEN=fixture\nENV APP=worker\n"
    )
    values, environment, profile = run_environment(
        template, tmp_path, ["BUILD_TOKEN", "APP"]
    )
    assert values == {"BUILD_TOKEN": "", "APP": "worker"}
    assert "BUILD_TOKEN" not in environment and "BUILD_TOKEN" not in profile


def test_repeated_path_extensions_keep_order(image, tmp_path):
    template = (
        TemplateBase()
        .from_image("registry.test/app")
        .set_envs({"PATH": "/first:$PATH"}, runtime=True)
        .set_envs({"PATH": "/second:$PATH"}, runtime=True)
    )
    values, _, _ = run_environment(template, tmp_path, ["PATH", "PRICE"])
    assert values == {"PATH": "/second:/first:/usr/bin:/bin", "PRICE": "cost$5"}


def test_prior_build_arg_value_is_used_by_runtime_env(image, tmp_path):
    template = TemplateBase().from_dockerfile(
        "FROM registry.test/app\nARG ROOT=/first\nENV SAVE=$ROOT\nARG ROOT=/second\n"
    )
    values, environment, _ = run_environment(template, tmp_path, ["ROOT", "SAVE"])
    assert values == {"ROOT": "", "SAVE": "/first"}
    assert "ROOT=" not in environment


def test_one_env_group_expands_against_previous_group(image, tmp_path):
    template = TemplateBase().from_dockerfile(
        "FROM registry.test/app\nENV A=first\nENV A=second B=$A\n"
    )
    values, _, _ = run_environment(template, tmp_path, ["A", "B"])
    assert values == {"A": "second", "B": "first"}


@pytest.mark.parametrize("path", ["/custom/bin", ""])
def test_runtime_path_does_not_break_writer(tmp_path, path):
    template = (
        TemplateBase()
        .from_template("base")
        .set_envs({"PATH": path, "APP": "worker"}, runtime=True)
    )
    values, environment, _ = run_environment(template, tmp_path, ["PATH", "APP"])
    assert values == {"PATH": path, "APP": "worker"}
    assert f"PATH={path}\n" in environment


def test_multiline_and_internal_variable_names_survive(tmp_path):
    template = (
        TemplateBase()
        .from_template("base")
        .set_envs(
            {"v": "literal", "NEXT": "$v", "TEXT": "quote'line\n\n"}, runtime=True
        )
    )
    values, _, _ = run_environment(template, tmp_path, ["v", "NEXT", "TEXT"])
    assert values == {"v": "literal", "NEXT": "", "TEXT": "quote'line\n\n"}


def test_workdir_precedes_user_steps_and_explicit_override(image):
    template = (
        TemplateBase()
        .from_image("registry.test/app")
        .run_cmd("pwd")
        .set_workdir("/override")
        .run_cmd("pwd")
    )
    steps = serialize(template)["steps"]
    assert [
        (s["type"], s["args"][0])
        for s in steps
        if SCRIPT_PATH not in " ".join(s["args"])
    ] == [("WORKDIR", "/app"), ("RUN", "pwd"), ("WORKDIR", "/override"), ("RUN", "pwd")]


def test_source_switch_drops_only_inherited_config(image, tmp_path):
    template = TemplateBase()
    serialize(template.from_image("registry.test/app"))
    data = serialize(template.from_template("base"))
    assert data["fromTemplate"] == "base" and "startCmd" not in data
    assert not any(
        s["type"] == "WORKDIR" or SCRIPT_PATH in " ".join(s["args"])
        for s in data["steps"]
    )


@pytest.fixture
def registry(monkeypatch):
    state = {"healthy": True, "revision": "one", "requests": []}

    def handle(request):
        state["requests"].append(request.url.path)
        if not state["healthy"]:
            return httpx.Response(503)
        if "/manifests/" in request.url.path:
            return httpx.Response(
                200, json={"config": {"digest": "sha256:" + state["revision"]}}
            )
        return httpx.Response(
            200, json={"config": {"Env": ["REVISION=" + state["revision"]]}}
        )

    monkeypatch.setattr(
        image_config,
        "_open_client",
        lambda *a, **kw: httpx.Client(transport=httpx.MockTransport(handle)),
    )
    monkeypatch.setattr(image_config.time, "sleep", lambda _: None)
    image_config.clear_image_config_cache()
    yield state
    image_config.clear_image_config_cache()


def test_registry_recovers_after_transient_failure(registry):
    registry["healthy"] = False
    assert image_config.fetch_image_config("registry.test/app:latest").error
    registry["healthy"] = True
    assert image_config.fetch_image_config("registry.test/app:latest").env == {
        "REVISION": "one"
    }


def test_mutable_tags_are_rechecked(registry):
    assert image_config.fetch_image_config("registry.test/app:latest").env == {
        "REVISION": "one"
    }
    registry["revision"] = "two"
    assert image_config.fetch_image_config("registry.test/app:latest").env == {
        "REVISION": "two"
    }


def test_digest_cache_returns_caller_owned_copies(registry):
    first = image_config.fetch_image_config("registry.test/app@sha256:fixed")
    first.env["REVISION"] = "caller edit"
    registry["healthy"] = False
    assert image_config.fetch_image_config("registry.test/app@sha256:fixed").env == {
        "REVISION": "one"
    }


def test_same_builder_can_retry_failed_registry_read(registry):
    registry["healthy"] = False
    template = TemplateBase().from_image("registry.test/app", on_config_failure="raise")
    with pytest.raises(Exception, match="503"):
        serialize(template)
    registry["healthy"] = True
    data = serialize(template)
    assert any(SCRIPT_PATH in " ".join(s["args"]) for s in data["steps"])
    assert template._template.image_config_failure() is None


def test_quoted_dockerfile_values_do_not_split_at_embedded_equals(image, tmp_path):
    template = TemplateBase().from_dockerfile(
        'FROM registry.test/app\nENV A="hello B=world" B="two words"\n'
    )
    values, _, _ = run_environment(template, tmp_path, ["A", "B"])
    assert values == {"A": "hello B=world", "B": "two words"}


def test_runtime_value_is_not_replaced_by_later_build_only_value(image, tmp_path):
    template = TemplateBase().from_dockerfile(
        "FROM registry.test/app\nENV TOKEN=runtime\nARG TOKEN=build-only\n"
    )
    values, environment, profile = run_environment(template, tmp_path, ["TOKEN"])
    assert values == {"TOKEN": "runtime"}
    assert "build-only" not in environment and "build-only" not in profile


def test_forward_reference_cannot_read_later_build_secret(tmp_path):
    template = (
        TemplateBase()
        .from_template("base")
        .set_envs({"EARLY": "$LATER"}, runtime=True)
        .set_envs({"LATER": "build-only"})
    )
    values, environment, profile = run_environment(template, tmp_path, ["EARLY"])
    assert values == {"EARLY": ""}
    assert "build-only" not in profile


def test_same_builder_refreshes_mutable_image_and_removes_old_commands(monkeypatch):
    configs = iter(
        [
            ImageConfig(env={"OLD": "one"}, workdir="/first", cmd=["./start"]),
            ImageConfig(env={"NEW": "two"}),
        ]
    )
    monkeypatch.setattr(
        template_main, "fetch_image_config", lambda *a, **kw: next(configs)
    )
    template = TemplateBase().from_image("registry.test/app:latest")
    first = serialize(template)
    assert first["startCmd"] == "./start"
    second = serialize(template)
    assert "startCmd" not in second and "readyCmd" not in second
    assert not any(step["type"] == "WORKDIR" for step in second["steps"])
    assert template._template._image_envs == {"NEW": "two"}


def test_base_environment_expansion_preserves_platform_values(tmp_path):
    from novita_sandbox.core.template.env_files import env_files_script

    profile, environment = tmp_path / "profile", tmp_path / "environment"
    script = (
        env_files_script({}, env_groups=[({"HOME": "$HOME/app", "APP": "$HOME"}, True)])
        .replace(PROFILE_PATH, str(profile))
        .replace(ENVIRONMENT_PATH, str(environment))
    )
    subprocess.run(
        ["/bin/sh", "-c", script],
        env={"PATH": "/usr/bin:/bin", "HOME": "/home/user"},
        check=True,
        capture_output=True,
    )
    assert "HOME=/home/user/app\n" in environment.read_text()
    assert "APP=/home/user\n" in environment.read_text()


def test_snapshot_preserves_real_base_values_before_final_build_env(tmp_path):
    template = (
        TemplateBase()
        .from_template("base")
        .set_envs(
            {
                "HOME": "$HOME/app",
                "APP": "$HOME",
                "TEXT": "$TEXT",
                "EMPTY": "$EMPTY",
                "EARLY": "$LATER",
            },
            runtime=True,
        )
        .set_envs({"LATER": "build-only"})
    )
    values, _, profile = run_environment(
        template,
        tmp_path,
        ["HOME", "APP", "TEXT", "EMPTY", "EARLY"],
        base_env={"HOME": "/home/user", "TEXT": "quote'line\n\n", "EMPTY": ""},
    )
    assert values == {
        "HOME": "/home/user/app",
        "APP": "/home/user",
        "TEXT": "quote'line\n\n",
        "EMPTY": "",
        "EARLY": "",
    }
    assert "build-only" not in profile


def test_failed_refresh_drops_previously_inherited_config(monkeypatch):
    configs = iter(
        [
            ImageConfig(env={"OLD": "one"}, workdir="/first", cmd=["./start"]),
            ImageConfig(env={}, error="offline"),
        ]
    )
    monkeypatch.setattr(
        template_main, "fetch_image_config", lambda *a, **kw: next(configs)
    )
    template = TemplateBase().from_image(
        "registry.test/app:latest", on_config_failure="ignore"
    )
    serialize(template)
    second = serialize(template)
    assert "startCmd" not in second and "readyCmd" not in second
    assert second["steps"] == []


def test_missing_base_snapshot_fails_instead_of_using_final_env(tmp_path):
    from novita_sandbox.core.template.env_files import env_files_script

    script = env_files_script(
        {},
        env_groups=[({"EARLY": "$LATER"}, True)],
        base_env_path=str(tmp_path / "missing"),
    )
    result = subprocess.run(["/bin/sh", "-c", script], capture_output=True)
    assert result.returncode != 0
