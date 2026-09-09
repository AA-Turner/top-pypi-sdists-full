"""`from_image` records a reference; the platform pulls the image server-side.

So nothing ever read the image's config, and everything ``docker run`` would have
inherited from it -- PATH, WORKDIR, the effective command -- was absent from the
sandbox. These tests pin what the builder now restores, and the precedence it
restores it under.

Kept in step with the JS suite
(`sdk-js/src/core/tests/template/inheritImageConfig.test.ts`).
"""

import base64
import json
import re
from typing import Any, Dict, Optional

import httpx
import pytest

from novita_sandbox.core.template.env_files import SCRIPT_PATH
from novita_sandbox.core.template.image_config import clear_image_config_cache
from novita_sandbox.core.template.main import TemplateBase


@pytest.fixture(autouse=True)
def _isolate():
    clear_image_config_cache()
    yield
    clear_image_config_cache()


def _serve(monkeypatch, handler) -> None:
    real_init = httpx.Client.__init__

    def patched_init(self, *args, **kwargs):
        kwargs["transport"] = httpx.MockTransport(handler)
        real_init(self, *args, **kwargs)

    monkeypatch.setattr(httpx.Client, "__init__", patched_init)


def _stub_image(monkeypatch, declared: Dict[str, Any], seen: Optional[list] = None):
    """Serve one image config, however the reader chooses to ask for it."""

    def handler(request):
        url = str(request.url)
        if seen is not None:
            seen.append(request.headers.get("authorization"))
        if "/token?" in url:
            return httpx.Response(200, json={"token": "t"})
        if "/manifests/" in url:
            return httpx.Response(200, json={"config": {"digest": "sha256:c"}})
        return httpx.Response(200, json={"config": declared})

    _serve(monkeypatch, handler)


def _stub_unreadable(monkeypatch, status: int = 401):
    """Fail every read, the way an unreachable or private registry does."""
    _serve(monkeypatch, lambda request: httpx.Response(status))


def _stub_no_network(monkeypatch) -> Dict[str, int]:
    """Count reads, and fail any that happen. For the paths that must not read."""
    calls = {"n": 0}

    def handler(request):
        calls["n"] += 1
        return httpx.Response(500)

    _serve(monkeypatch, handler)
    return calls


def _serialized(builder) -> Dict[str, Any]:
    """The template as the platform will receive it.

    Takes the builder that `from_image` returned: `to_json` reads through
    `._template`, so handing it the TemplateBase itself does not work.
    """
    return json.loads(TemplateBase.to_json(builder))


def _runtime_env_script(payload: Dict[str, Any]) -> str:
    """The runtime-env script, decoded back out of its RUN step."""
    for step in payload["steps"]:
        if step["type"] == "RUN" and SCRIPT_PATH in step["args"][0]:
            encoded = re.search(r"echo ([A-Za-z0-9+/=]+) \| base64 -d", step["args"][0])
            return base64.b64decode(encoded.group(1)).decode()
    return ""


class TestInheritingWhatTheImageDeclares:
    def test_carries_the_image_env_into_the_runtime_env_files(self, monkeypatch):
        # The acceptance case: an image whose toolchain lives on its own PATH
        # looked installed and behaved as though it were not.
        _stub_image(
            monkeypatch, {"Env": ["PATH=/opt/venv/bin:/usr/bin", "LANG=C.UTF-8"]}
        )

        t = TemplateBase()
        b = t.from_image("python:3.11-slim")

        script = _runtime_env_script(_serialized(b))
        assert "export PATH=" in script
        assert "/opt/venv/bin:/usr/bin" in script
        assert "LANG" in script

    def test_adopts_the_image_workdir(self, monkeypatch):
        _stub_image(monkeypatch, {"WorkingDir": "/data"})

        t = TemplateBase()
        b = t.from_image("redis:7")

        steps = _serialized(b)["steps"]
        assert any(s["type"] == "WORKDIR" and s["args"][0] == "/data" for s in steps)

    def test_adopts_entrypoint_and_cmd_as_the_start_command(self, monkeypatch):
        _stub_image(
            monkeypatch,
            {"Entrypoint": ["docker-entrypoint.sh"], "Cmd": ["redis-server"]},
        )

        t = TemplateBase()
        b = t.from_image("redis:7")

        payload = _serialized(b)
        assert payload["startCmd"] == "docker-entrypoint.sh redis-server"
        # set_start_cmd needs a readiness check; the SDK's Dockerfile parser pairs
        # it with the same timer, so the two paths agree.
        assert payload.get("readyCmd")

    def test_leaves_a_bare_shell_when_the_image_declares_no_command(self, monkeypatch):
        _stub_image(monkeypatch, {"Env": ["A=1"]})

        t = TemplateBase()
        b = t.from_image("scratch-ish:1")

        assert "startCmd" not in _serialized(b)


class TestADockerfileBase:
    def test_inherits_env_the_dockerfile_does_not_declare(self, monkeypatch):
        # The parser records only what the Dockerfile states, so a Dockerfile
        # relying on its base image's environment -- the ordinary case, since
        # ``docker build`` inherits it -- got none of it. Measured on the real
        # platform with ``FROM continuumio/miniconda3:latest``: the sandbox
        # reported PATH=/opt/conda/condabin:/usr/local/bin:... with /opt/conda/bin
        # absent, so ``which conda`` failed while /opt/conda/bin/conda existed.
        _stub_image(monkeypatch, {"Env": ["PATH=/opt/conda/bin:/usr/bin", "LANG=C.UTF-8"]})

        t = TemplateBase()
        b = t.from_dockerfile(
            "FROM continuumio/miniconda3:latest\nRUN conda --version\n"
        )

        script = _runtime_env_script(_serialized(b))
        assert "/opt/conda/bin" in script
        assert "C.UTF-8" in script

    def test_the_dockerfile_own_env_wins(self, monkeypatch):
        _stub_image(monkeypatch, {"Env": ["PATH=/opt/conda/bin:/usr/bin", "LANG=C.UTF-8"]})

        t = TemplateBase()
        b = t.from_dockerfile(
            "FROM continuumio/miniconda3:latest\nENV PATH=/my/bin:$PATH\n"
        )

        script = _runtime_env_script(_serialized(b))
        # One assignment, the Dockerfile's, with $PATH left live for the build.
        assert 'v="/my/bin:$PATH"' in script
        assert "/opt/conda/bin" not in script
        # A name the Dockerfile did not touch still comes from the image.
        assert "C.UTF-8" in script

    def test_keeps_the_workdir_the_parser_set(self, monkeypatch):
        # The parser always sets one, and a Dockerfile's own WORKDIR wins.
        _stub_image(
            monkeypatch, {"Env": ["A=1"], "WorkingDir": "/image-workdir"}
        )

        t = TemplateBase()
        b = t.from_dockerfile("FROM python:3.11-slim\nWORKDIR /app\n")

        dirs = [s for s in _serialized(b)["steps"] if s["type"] == "WORKDIR"]
        assert "/image-workdir" not in [d["args"][0] for d in dirs]


class TestTheCallerWinsOverTheImage:
    def test_keeps_a_caller_value_for_a_name_the_image_also_declares(self, monkeypatch):
        # Same precedence a Dockerfile has over its own base image.
        _stub_image(monkeypatch, {"Env": ["PATH=/image/bin"]})

        t = TemplateBase()
        b = t.from_image("python:3.11-slim").set_envs({"PATH": "/caller/bin"})

        script = _runtime_env_script(_serialized(b))
        assert "/caller/bin" in script
        assert "/image/bin" not in script

    def test_keeps_both_when_the_names_do_not_collide(self, monkeypatch):
        _stub_image(monkeypatch, {"Env": ["LANG=C.UTF-8"]})

        t = TemplateBase()
        b = t.from_image("python:3.11-slim").set_envs({"MINE": "1"})

        script = _runtime_env_script(_serialized(b))
        assert "LANG" in script
        assert "MINE" in script

    def test_does_not_add_a_workdir_when_the_caller_set_one(self, monkeypatch):
        _stub_image(monkeypatch, {"WorkingDir": "/data"})

        t = TemplateBase()
        b = t.from_image("redis:7").set_workdir("/app")

        dirs = [s["args"][0] for s in _serialized(b)["steps"] if s["type"] == "WORKDIR"]
        assert dirs == ["/app"]

    def test_does_not_override_a_caller_start_command(self, monkeypatch):
        _stub_image(
            monkeypatch,
            {"Entrypoint": ["docker-entrypoint.sh"], "Cmd": ["redis-server"]},
        )

        t = TemplateBase()
        b = t.from_image("redis:7").set_start_cmd("my-server", "true")

        assert _serialized(b)["startCmd"] == "my-server"


class TestWhenTheImageConfigCannotBeRead:
    def test_still_builds_and_records_why_the_config_is_missing(self, monkeypatch):
        # One unreachable registry must not fail a batch conversion. But a
        # template silently missing the image's PATH is the failure this exists to
        # prevent, so it cannot pass unmentioned -- and to_json has no log
        # channel, so a dry run or a CLI conversion can only see it if recorded.
        _stub_unreadable(monkeypatch)

        t = TemplateBase()
        b = t.from_image("ghcr.io/org/private:1")
        payload = _serialized(b)

        assert payload["fromImage"] == "ghcr.io/org/private:1"
        assert "401" in t.image_config_failure()["error"]

    def test_reports_nothing_when_the_config_was_read(self, monkeypatch):
        _stub_image(monkeypatch, {"Env": ["A=1"]})

        t = TemplateBase()
        b = t.from_image("python:3.11-slim")
        _serialized(b)

        assert t.image_config_failure() is None

    def test_marks_an_image_that_cannot_be_used_here(self, monkeypatch):
        # A retry cannot change this, and the build would fail for the same reason
        # minutes later, so a batch should skip rather than build.
        def handler(request):
            if "/token?" in str(request.url):
                return httpx.Response(200, json={"token": "t"})
            return httpx.Response(
                200,
                json={
                    "manifests": [
                        {
                            "digest": "sha256:a",
                            "platform": {"os": "linux", "architecture": "arm64"},
                        }
                    ]
                },
            )

        _serve(monkeypatch, handler)

        t = TemplateBase()
        b = t.from_image("arm-only:1")
        _serialized(b)

        assert "amd64" in t.image_config_failure()["unusable"]

    def test_adds_no_runtime_env_layer_it_has_nothing_to_write(self, monkeypatch):
        _stub_unreadable(monkeypatch)

        t = TemplateBase()
        b = t.from_image("ghcr.io/org/private:1")

        assert _runtime_env_script(_serialized(b)) == ""

    def test_still_carries_the_environment_the_caller_set(self, monkeypatch):
        _stub_unreadable(monkeypatch)

        t = TemplateBase()
        b = t.from_image("ghcr.io/org/private:1").set_envs({"MINE": "1"})

        assert "MINE" in _runtime_env_script(_serialized(b))


class TestWhenTheReadDoesNotApply:
    def test_reads_nothing_for_a_template_base(self, monkeypatch):
        # A template base already carries its config.
        calls = _stub_no_network(monkeypatch)

        t = TemplateBase()
        b = t.from_template("some-template")
        _serialized(b)

        assert calls["n"] == 0

    def test_reads_nothing_when_the_caller_opts_out(self, monkeypatch):
        calls = _stub_no_network(monkeypatch)

        t = TemplateBase()
        b = t.from_image("python:3.11-slim", inherit_config=False)
        _serialized(b)

        assert calls["n"] == 0

    def test_reads_once_even_when_serialized_twice(self, monkeypatch):
        # A second read would re-apply the image's values over anything the caller
        # set in between.
        reads = {"n": 0}

        def handler(request):
            url = str(request.url)
            if "/token?" in url:
                return httpx.Response(200, json={"token": "t"})
            if "/manifests/" in url:
                return httpx.Response(200, json={"config": {"digest": "sha256:c"}})
            reads["n"] += 1
            return httpx.Response(200, json={"config": {"Env": ["A=1"]}})

        _serve(monkeypatch, handler)

        t = TemplateBase()
        b = t.from_image("python:3.11-slim")
        _serialized(b)
        _serialized(b)

        assert reads["n"] == 1

    def test_does_not_re_apply_the_image_value_over_one_set_later(self, monkeypatch):
        _stub_image(monkeypatch, {"Env": ["PATH=/image/bin"]})

        t = TemplateBase()
        b = t.from_image("python:3.11-slim")
        _serialized(b)
        b.set_envs({"PATH": "/set/later"})

        assert "/set/later" in _runtime_env_script(_serialized(b))

    def test_adds_no_second_workdir_when_serialized_twice(self, monkeypatch):
        # WORKDIR is appended to the instruction list, so a duplicate would be a
        # second step rather than an overwrite. Measured: what prevents it is the
        # "caller already set one" check, which sees the step the first pass
        # added -- the read-once flag and the process cache both also stop it, so
        # this holds if any one of the three is removed. Asserted with the cache
        # cleared so it is at least not the cache alone.
        _stub_image(monkeypatch, {"WorkingDir": "/data"})

        t = TemplateBase()
        b = t.from_image("redis:7")
        _serialized(b)
        clear_image_config_cache()

        dirs = [s for s in _serialized(b)["steps"] if s["type"] == "WORKDIR"]
        assert len(dirs) == 1


class TestCredentials:
    def test_reads_a_private_image_with_the_credentials_given(self, monkeypatch):
        seen: list = []
        _stub_image(monkeypatch, {"Env": ["SECRET_PATH=/private/bin"]}, seen=seen)

        t = TemplateBase()
        b = t.from_image("ghcr.io/org/private:1", username="u", password="p")

        assert "/private/bin" in _runtime_env_script(_serialized(b))
        expected = "Basic " + base64.b64encode(b"u:p").decode("ascii")
        assert expected in seen
