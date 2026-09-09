"""What an image declares has to be read before a template can inherit it.

Registry answers are stubbed: the reads under test are HTTP, and pinning them
against the live Docker Hub would make the suite slow, offline-fragile and
dependent on tags that move. The one thing a stub cannot establish is what a real
registry actually answers, so the status codes asserted here are the ones
measured against Docker Hub and recorded in ``_describe_failure`` -- and the
values were cross-checked field by field against the JS SDK reading the same
three real images.

Kept in step with the JS suite (`sdk-js/src/core/tests/template/imageConfig.test.ts`).
"""

import base64
import json
from typing import Any, Dict, List, Optional

import httpx
import pytest

from novita_sandbox.core.template.image_config import (
    READ_ATTEMPTS,
    clear_image_config_cache,
    effective_start_cmd,
    fetch_image_config,
    parse_image_ref,
    set_retry_backoff_for_tests,
    unsupported_base,
)


@pytest.fixture(autouse=True)
def _isolate():
    clear_image_config_cache()
    # The retry behaviour is asserted below; waiting the real 3s for it is not.
    restore = set_retry_backoff_for_tests(0.001)
    yield
    restore()
    clear_image_config_cache()


class _Recorder:
    """Routes stubbed replies by URL fragment and records what was asked."""

    def __init__(self, routes: List[Dict[str, Any]]):
        self.routes = routes
        self.urls: List[str] = []
        self.auth: List[Optional[str]] = []

    def __call__(self, request: httpx.Request) -> httpx.Response:
        url = str(request.url)
        self.urls.append(url)
        self.auth.append(request.headers.get("authorization"))
        for route in self.routes:
            if route["match"] in url:
                body = route.get("json", {})
                return httpx.Response(route.get("status", 200), json=body)
        return httpx.Response(404, json={"errors": [{"code": "NOT_FOUND"}]})


def _serve(monkeypatch, handler) -> None:
    """Answer every registry read this test makes with `handler`."""
    real_init = httpx.Client.__init__

    def patched_init(self, *args, **kwargs):
        kwargs["transport"] = httpx.MockTransport(handler)
        real_init(self, *args, **kwargs)

    monkeypatch.setattr(httpx.Client, "__init__", patched_init)


def _install(monkeypatch, routes: List[Dict[str, Any]]) -> _Recorder:
    """Serve `routes` for every registry read this test makes."""
    recorder = _Recorder(routes)
    _serve(monkeypatch, recorder)
    return recorder


TOKEN = {"match": "/token?", "json": {"token": "stub-token"}}


def _single_platform(declared: Dict[str, Any]) -> List[Dict[str, Any]]:
    """A single-platform image whose config blob declares `declared`."""
    return [
        TOKEN,
        {"match": "/manifests/", "json": {"config": {"digest": "sha256:cfg"}}},
        {"match": "/blobs/sha256:cfg", "json": {"config": declared}},
    ]


class TestParseImageRef:
    @pytest.mark.parametrize(
        "image,expected",
        [
            ("nginx", ("registry-1.docker.io", "library/nginx", "latest")),
            ("nginx:1.25", ("registry-1.docker.io", "library/nginx", "1.25")),
            ("org/app:dev", ("registry-1.docker.io", "org/app", "dev")),
            ("docker.io/org/app", ("registry-1.docker.io", "org/app", "latest")),
            ("docker.io/nginx", ("registry-1.docker.io", "library/nginx", "latest")),
            ("ghcr.io/org/app:dev", ("ghcr.io", "org/app", "dev")),
            ("ghcr.io/org/sub/app", ("ghcr.io", "org/sub/app", "latest")),
            ("localhost/app", ("localhost", "app", "latest")),
        ],
    )
    def test_splits(self, image, expected):
        assert parse_image_ref(image) == expected

    def test_reads_a_port_on_the_host_rather_than_as_a_tag(self):
        # The ':' here precedes a '/', so it cannot be a tag.
        assert parse_image_ref("reg:5000/app") == ("reg:5000", "app", "latest")

    def test_keeps_a_digest_pin_as_the_reference(self):
        assert parse_image_ref("reg:5000/app@sha256:abc") == (
            "reg:5000",
            "app",
            "sha256:abc",
        )

    def test_prefers_a_digest_over_a_tag(self):
        # '@' can only introduce a digest.
        assert parse_image_ref("org/app:1.2@sha256:abc")[2] == "sha256:abc"


class TestFetchImageConfig:
    def test_reads_what_the_image_declares(self, monkeypatch):
        _install(
            monkeypatch,
            _single_platform(
                {
                    "Env": ["PATH=/opt/venv/bin:/usr/bin", "LANG=C.UTF-8"],
                    "WorkingDir": "/data",
                    "Entrypoint": ["docker-entrypoint.sh"],
                    "Cmd": ["redis-server"],
                }
            ),
        )

        config = fetch_image_config("redis:7")

        assert config.env == {"PATH": "/opt/venv/bin:/usr/bin", "LANG": "C.UTF-8"}
        assert config.workdir == "/data"
        assert config.entrypoint == ["docker-entrypoint.sh"]
        assert config.cmd == ["redis-server"]
        assert config.error is None

    def test_keeps_every_field_present_when_nothing_is_declared(self, monkeypatch):
        # A caller should never have to tell "no config" from "read failed"
        # structurally; `error` says which it was.
        _install(monkeypatch, _single_platform({}))

        config = fetch_image_config("scratch-ish:1")

        assert (config.env, config.workdir, config.entrypoint, config.cmd) == (
            {},
            None,
            [],
            [],
        )
        assert config.error is None

    def test_drops_env_vars_describing_the_build_machine(self, monkeypatch):
        # Carrying HOSTNAME or HOME over would fight the sandbox's own setup.
        _install(
            monkeypatch,
            _single_platform(
                {"Env": ["PATH=/usr/bin", "HOSTNAME=buildkit-7f", "HOME=/root", "TERM=dumb"]}
            ),
        )

        assert list(fetch_image_config("x:1").env) == ["PATH"]

    def test_ignores_an_env_entry_with_no_separator(self, monkeypatch):
        _install(monkeypatch, _single_platform({"Env": ["MALFORMED", "OK=1"]}))

        assert fetch_image_config("x:1").env == {"OK": "1"}

    def test_keeps_an_empty_value(self, monkeypatch):
        # Different from an absent one.
        _install(monkeypatch, _single_platform({"Env": ["EMPTY="]}))

        assert fetch_image_config("x:1").env == {"EMPTY": ""}

    def test_keeps_equals_inside_a_value(self, monkeypatch):
        _install(monkeypatch, _single_platform({"Env": ["OPTS=-Da=1 -Db=2"]}))

        assert fetch_image_config("x:1").env["OPTS"] == "-Da=1 -Db=2"

    def test_reads_an_empty_workingdir_as_unset(self, monkeypatch):
        _install(monkeypatch, _single_platform({"WorkingDir": ""}))

        assert fetch_image_config("x:1").workdir is None


class TestMultiArchResolution:
    INDEX = {
        "manifests": [
            {"digest": "sha256:arm", "platform": {"os": "linux", "architecture": "arm64"}},
            {"digest": "sha256:amd", "platform": {"os": "linux", "architecture": "amd64"}},
        ]
    }

    def test_follows_the_linux_amd64_entry(self, monkeypatch):
        # Sandboxes are amd64.
        recorder = _install(
            monkeypatch,
            [
                TOKEN,
                {"match": "/manifests/7", "json": self.INDEX},
                {
                    "match": "/manifests/sha256:amd",
                    "json": {"config": {"digest": "sha256:cfg"}},
                },
                {"match": "/blobs/sha256:cfg", "json": {"config": {"Env": ["A=1"]}}},
            ],
        )

        assert fetch_image_config("redis:7").env == {"A": "1"}
        assert not any("sha256:arm" in u for u in recorder.urls)

    def test_reports_no_amd64_variant_as_unusable(self, monkeypatch):
        # Worth catching before a build: the build would fail for the same reason,
        # minutes later, and a retry cannot change the answer.
        _install(
            monkeypatch,
            [
                TOKEN,
                {
                    "match": "/manifests/",
                    "json": {
                        "manifests": [
                            {
                                "digest": "sha256:a",
                                "platform": {"os": "linux", "architecture": "arm64"},
                            }
                        ]
                    },
                },
            ],
        )

        config = fetch_image_config("arm-only:1")

        assert "no linux/amd64 variant" in config.unusable
        assert "linux/arm64" in config.unusable
        assert config.error == config.unusable

    def test_does_not_offer_attestation_entries_as_a_platform(self, monkeypatch):
        # `unknown/unknown` entries are attestations, not runnable images.
        _install(
            monkeypatch,
            [
                TOKEN,
                {
                    "match": "/manifests/",
                    "json": {
                        "manifests": [
                            {
                                "digest": "sha256:a",
                                "platform": {"os": "linux", "architecture": "arm64"},
                            },
                            {
                                "digest": "sha256:b",
                                "platform": {"os": "unknown", "architecture": "unknown"},
                            },
                        ]
                    },
                },
            ],
        )

        assert "unknown" not in fetch_image_config("arm-only:1").unusable

    def test_reports_a_manifest_naming_no_config_blob(self, monkeypatch):
        _install(monkeypatch, [TOKEN, {"match": "/manifests/", "json": {}}])

        assert "no config blob" in fetch_image_config("odd:1").error


class TestFailuresACallerCanActOn:
    def test_a_404_on_hub_is_a_naming_mistake(self, monkeypatch):
        # Measured: `library/REDIS` answers 404 -- it case-folds onto a real repo,
        # so the repository resolved and the thing named did not.
        _install(monkeypatch, [TOKEN, {"match": "/manifests/", "status": 404}])

        config = fetch_image_config("REDIS:7")

        assert "no such image" in config.unusable
        assert "case-sensitive" in config.unusable

    def test_a_401_in_the_library_namespace_is_a_typo(self, monkeypatch):
        # Measured, and the opposite way round from the obvious guess: a plain typo
        # like `library/nginxx` answers 401. The `library/` namespace has no
        # private repositories, so nothing there can 401 for another reason.
        _install(monkeypatch, [TOKEN, {"match": "/manifests/", "status": 401}])

        config = fetch_image_config("nginxx-typo:1")

        assert "no such image" in config.unusable
        assert "typo" in config.unusable

    def test_a_401_with_credentials_does_not_blame_the_spelling(self, monkeypatch):
        # Measured against Docker Hub: `redis:7` with a wrong password and
        # `rediss:7` with a right one both answer 401, so the read cannot tell them
        # apart. The anonymous message names the spelling, which for a correct name
        # sends the reader to the wrong place entirely.
        _install(monkeypatch, [TOKEN, {"match": "/manifests/", "status": 401}])

        config = fetch_image_config("redis:7", "u", "wrong")

        assert "credentials" in config.error
        # Still not unusable: a corrected password makes this very reference work.
        assert config.unusable is None

    def test_a_401_elsewhere_stays_ambiguous(self, monkeypatch):
        # An absent repository and a private one answer byte-identically.
        _install(monkeypatch, [TOKEN, {"match": "/manifests/", "status": 401}])

        config = fetch_image_config("ghcr.io/org/private:1")

        assert "401" in config.error
        # Not unusable: with credentials the same read may well succeed.
        assert config.unusable is None

    def test_a_401_on_a_hub_org_repository_stays_ambiguous(self, monkeypatch):
        _install(monkeypatch, [TOKEN, {"match": "/manifests/", "status": 401}])

        assert fetch_image_config("someorg/private:1").unusable is None

    def test_reports_a_network_failure_as_data(self, monkeypatch):
        # One unreachable registry must not abort a batch conversion.
        def boom(request):
            raise httpx.ConnectError("getaddrinfo ENOTFOUND")

        _serve(monkeypatch, boom)

        config = fetch_image_config("x:1")

        assert "ENOTFOUND" in config.error
        assert config.env == {}

    def test_retries_a_503_and_uses_the_answer_that_arrives(self, monkeypatch):
        attempts = {"n": 0}

        def handler(request):
            url = str(request.url)
            if "/token?" in url:
                return httpx.Response(200, json={"token": "t"})
            if "/manifests/" in url:
                attempts["n"] += 1
                if attempts["n"] == 1:
                    return httpx.Response(503, headers={"retry-after": "0"})
                return httpx.Response(200, json={"config": {"digest": "sha256:cfg"}})
            return httpx.Response(200, json={"config": {"Env": ["A=1"]}})

        _serve(monkeypatch, handler)

        assert fetch_image_config("x:1").env == {"A": "1"}
        assert attempts["n"] == 2

    def test_does_not_retry_a_404(self, monkeypatch):
        # An answer rather than a hiccup.
        manifests = {"n": 0}

        def handler(request):
            if "/token?" in str(request.url):
                return httpx.Response(200, json={"token": "t"})
            manifests["n"] += 1
            return httpx.Response(404)

        _serve(monkeypatch, handler)

        fetch_image_config("nope:1")

        assert manifests["n"] == 1


class TestTheReadCache:
    def test_reads_a_reference_once_per_process(self, monkeypatch):
        recorder = _install(monkeypatch, _single_platform({"Env": ["A=1"]}))

        fetch_image_config("redis:7")
        fetch_image_config("redis:7")

        assert len([u for u in recorder.urls if "/blobs/" in u]) == 1

    def test_hands_out_a_copy(self, monkeypatch):
        # Neither the answer handed out first nor one that came *from* the cache
        # may reach the stored copy -- copying on store alone would miss the second.
        _install(monkeypatch, _single_platform({"Env": ["A=1"]}))

        first = fetch_image_config("redis:7")
        first.env["A"] = "mutated-by-first"
        first.entrypoint.append("injected-by-first")

        second = fetch_image_config("redis:7")
        assert second.env == {"A": "1"}
        assert second.entrypoint == []

        second.env["A"] = "mutated-by-second"
        second.entrypoint.append("injected-by-second")

        third = fetch_image_config("redis:7")
        assert third.env == {"A": "1"}
        assert third.entrypoint == []

    def test_keys_on_the_credentials(self, monkeypatch):
        # An anonymous and an authenticated read of the same private repository are
        # different questions. Caching only the reference would hand the caller who
        # supplied credentials the earlier anonymous failure.
        state = {"authenticated": False}

        def handler(request):
            url = str(request.url)
            header = request.headers.get("authorization", "")
            if "/token?" in url:
                state["authenticated"] = header.startswith("Basic ")
                return httpx.Response(
                    200, json={"token": "private" if state["authenticated"] else "anon"}
                )
            if not state["authenticated"]:
                return httpx.Response(401)
            if "/manifests/" in url:
                return httpx.Response(200, json={"config": {"digest": "sha256:cfg"}})
            return httpx.Response(200, json={"config": {"Env": ["SECRET=1"]}})

        _serve(monkeypatch, handler)

        anon = fetch_image_config("ghcr.io/org/p:1")
        assert "401" in anon.error

        authed = fetch_image_config("ghcr.io/org/p:1", username="u", password="p")
        assert authed.env == {"SECRET": "1"}

    def test_is_cleared_on_request(self, monkeypatch):
        recorder = _install(monkeypatch, _single_platform({"Env": ["A=1"]}))

        fetch_image_config("redis:7")
        clear_image_config_cache()
        fetch_image_config("redis:7")

        assert len([u for u in recorder.urls if "/blobs/" in u]) == 2


class TestAuthentication:
    def test_asks_hub_for_a_pull_scoped_token_and_carries_it(self, monkeypatch):
        recorder = _install(monkeypatch, _single_platform({}))

        fetch_image_config("nginx")

        token = next(u for u in recorder.urls if "/token?" in u)
        assert "auth.docker.io" in token
        assert "scope=repository:library/nginx:pull" in token
        assert recorder.auth[-1] == "Bearer stub-token"

    def test_sends_basic_auth_to_a_registry_handing_out_no_token(self, monkeypatch):
        # A private registry takes the credentials through unchanged.
        recorder = _install(
            monkeypatch,
            [
                {"match": "/manifests/", "json": {"config": {"digest": "sha256:cfg"}}},
                {"match": "/blobs/", "json": {"config": {}}},
            ],
        )

        fetch_image_config("reg.internal:5000/app:1", username="u", password="p")

        expected = "Basic " + base64.b64encode(b"u:p").decode("ascii")
        assert recorder.auth and all(h == expected for h in recorder.auth)

    def test_does_not_spend_the_retry_budget_on_the_token(self, monkeypatch):
        # Measured: retrying both the token and the read turned one offline
        # registry into six requests and six seconds of backoff. The token has a
        # fallback -- anonymous or basic auth -- so it gets one attempt.
        calls = {"token": 0, "manifest": 0}

        def handler(request):
            url = str(request.url)
            if "/token?" in url:
                calls["token"] += 1
                return httpx.Response(503)
            calls["manifest"] += 1
            return httpx.Response(503)

        _serve(monkeypatch, handler)

        fetch_image_config("nginx")

        assert calls["token"] == 1
        assert calls["manifest"] == READ_ATTEMPTS

    def test_reads_on_when_the_token_endpoint_fails(self, monkeypatch):
        # Basic auth may already suffice.
        _install(
            monkeypatch,
            [
                {"match": "/token?", "status": 500},
                {"match": "/manifests/", "json": {"config": {"digest": "sha256:cfg"}}},
                {"match": "/blobs/", "json": {"config": {"Env": ["A=1"]}}},
            ],
        )

        assert fetch_image_config("nginx").env == {"A": "1"}


class TestEffectiveStartCmd:
    def test_joins_entrypoint_and_cmd_the_way_docker_composes_them(self):
        assert (
            effective_start_cmd(["docker-entrypoint.sh"], ["redis-server"])
            == "docker-entrypoint.sh redis-server"
        )

    def test_uses_whichever_one_the_image_declares(self):
        assert effective_start_cmd([], ["nginx", "-g", "daemon off;"]) == (
            "nginx -g 'daemon off;'"
        )
        assert effective_start_cmd(["/init"], []) == "/init"

    def test_preserves_exec_form_argument_boundaries_and_shell_metacharacters(self):
        assert effective_start_cmd(["sh", "-c"], ['printf \'%s\' "$HOME"']) == (
            "sh -c 'printf '\\''%s'\\'' \"$HOME\"'"
        )

    def test_returns_none_when_the_image_declares_neither(self):
        # The sandbox is then left as a bare shell rather than given an empty command.
        assert effective_start_cmd([], []) is None


class TestAnUnusableProxy:
    """httpx reads ALL_PROXY/HTTPS_PROXY from the environment and refuses to
    construct for a ``socks5://`` one unless the optional ``socksio`` package is
    installed. Measured on a machine with ``all_proxy=socks5://...``: every read
    failed with "the 'socksio' package is not installed" while the JS SDK on the
    same machine read the same images fine, because Node's fetch ignores those
    variables. A silent template with no ENV is exactly what this must not produce.
    """

    def test_falls_back_to_a_direct_connection(self, monkeypatch):
        from novita_sandbox.core.template import image_config

        attempts = {"n": 0}
        real_client = httpx.Client

        def fake_client(*args, **kwargs):
            attempts["n"] += 1
            # The first construction is the one that reads the environment.
            if not kwargs.get("trust_env", True) is False:
                raise ImportError(
                    "Using SOCKS proxy, but the 'socksio' package is not installed."
                )
            return real_client(
                *args,
                **kwargs,
                transport=httpx.MockTransport(_Recorder(_single_platform({"Env": ["A=1"]}))),
            )

        monkeypatch.setattr(image_config.httpx, "Client", fake_client)

        config = fetch_image_config("redis:7")

        assert config.env == {"A": "1"}
        assert config.error is None
        # Tried the environment's proxy first, then without it.
        assert attempts["n"] == 2

    def test_reports_the_failure_when_even_a_direct_read_fails(self, monkeypatch):
        from novita_sandbox.core.template import image_config

        def always_import_error(*args, **kwargs):
            raise ImportError("socksio missing and no way round it")

        monkeypatch.setattr(image_config.httpx, "Client", always_import_error)

        config = fetch_image_config("redis:7")

        assert "socksio" in config.error


class TestUnsupportedBase:
    """The base OS check.

    Every blob below is the real ``history`` / ``Labels`` / ``Env`` of the named
    image, read from the registry, paired with the measured build outcome:
    debian/ubuntu images reached ready, the rest failed with
    ``error waiting for provisioning sandbox: exit status: 1``.

    Kept in step with the JS suite (`imageConfig.test.ts`).
    """

    BUILDS = [
        ("debian:12", True, {"history": [{"created_by": "# debian.sh --arch 'amd64' out/ 'bookworm' '@1785715200'"}]}),
        (
            "ubuntu:22.04",
            True,
            {
                "history": [{"created_by": "/bin/sh -c #(nop)  ARG RELEASE"}],
                "config": {"Labels": {"org.opencontainers.image.version": "22.04"}},
            },
        ),
        (
            "python:3.11-slim",
            True,
            {
                "history": [
                    {"created_by": "# debian.sh --arch 'amd64' out/ 'trixie' '@1785715200'"},
                    {"created_by": "RUN /bin/sh -c apt-get update && apt-get install -y ca-certificates"},
                ]
            },
        ),
        ("alpine:3.20", False, {"history": [{"created_by": "ADD alpine-minirootfs-3.20.10-x86_64.tar.gz / # buildkit"}]}),
        (
            "nginx:alpine",
            False,
            {
                "history": [
                    {"created_by": "ADD alpine-minirootfs-3.24.1-x86_64.tar.gz / # buildkit"},
                    {"created_by": "RUN /bin/sh -c apk add --no-cache nginx"},
                ],
                "config": {"Labels": {"maintainer": "NGINX Docker Maintainers <docker-maint@nginx.com>"}},
            },
        ),
        ("busybox:1.36", False, {"history": [{"created_by": "BusyBox 1.36.1 (glibc), Debian 13"}]}),
        (
            "fedora:40",
            False,
            {
                "history": [{"created_by": "LABEL maintainer=Clement Verna <cverna@fedoraproject.org>"}],
                "config": {"Env": ["PATH=/usr/bin", "DISTTAG=f40container", "FGC=f40"]},
            },
        ),
        (
            "opensuse/leap:15",
            False,
            {
                "history": [{"created_by": "KIWI 10.2.33"}],
                "config": {"Labels": {"org.opensuse.reference": "registry.opensuse.org/opensuse/leap:15.6.7.73"}},
            },
        ),
    ]

    def test_never_rejects_an_image_measured_to_build(self):
        # The asymmetry that matters: a missed image costs a failed build, a
        # wrongly rejected one cannot be built at all through this SDK.
        for image, builds, blob in self.BUILDS:
            if builds:
                assert unsupported_base(blob) is None, f"{image} was rejected"

    def test_identifies_the_bases_it_can(self):
        detected = {
            image: unsupported_base(blob)
            for image, builds, blob in self.BUILDS
            if not builds
        }
        assert detected == {
            "alpine:3.20": "Alpine (musl)",
            "nginx:alpine": "Alpine (musl)",
            "busybox:1.36": "BusyBox",
            "fedora:40": "RPM-based (Fedora/RHEL/Rocky)",
            "opensuse/leap:15": "SUSE",
        }

    def test_does_not_read_debian_in_a_busybox_banner_as_apt_evidence(self):
        # busybox:1.36's history is literally "BusyBox 1.36.1 (glibc), Debian 13",
        # and it cannot be provisioned. Matching a bare "debian" would clear it.
        assert (
            unsupported_base({"history": [{"created_by": "BusyBox 1.36.1 (glibc), Debian 13"}]})
            == "BusyBox"
        )

    def test_apt_evidence_wins_over_an_alpine_build_stage(self):
        assert (
            unsupported_base(
                {
                    "history": [
                        {"created_by": "ADD alpine-minirootfs-3.20.0-x86_64.tar.gz / # buildkit"},
                        {"created_by": "# debian.sh --arch 'amd64' out/ 'bookworm'"},
                    ]
                }
            )
            is None
        )

    def test_says_nothing_about_an_image_it_cannot_classify(self):
        # rockylinux:9's real blob: one ADD, no labels, bash CMD --
        # indistinguishable from images that work, so the build is the backstop.
        assert (
            unsupported_base(
                {"history": [{"created_by": "ADD layer.tar.xz / # buildkit"}, {"created_by": 'CMD ["/bin/bash"]'}]}
            )
            is None
        )

    def test_handles_a_blob_with_no_history_or_config(self):
        assert unsupported_base({}) is None


class TestRetryOverADeadConnection:
    """A retry has to discard the connection that just failed.

    Measured against Docker Hub's blob CDN: one reset made all three attempts fail
    with ``[Errno 54] Connection reset by peer`` about 50ms apart -- httpx keeps
    the pool alive and handed the same dead connection back each time. The read
    then returned a config with no environment, silently, and the JS SDK read the
    same image fine on the same machine.
    """

    def test_retries_only_after_dropping_the_pooled_connection(self):
        from novita_sandbox.core.template.image_config import _registry_get

        pool_closed = {"n": 0}
        attempts = {"n": 0}

        class FakePool:
            def close(self):
                pool_closed["n"] += 1

        class FakeTransport:
            _pool = FakePool()

        class FakeClient:
            _transport = FakeTransport()

            def get(self, url, headers=None):
                attempts["n"] += 1
                # Fails while the dead connection is still pooled, exactly as the
                # real client did; succeeds once it has been dropped.
                if pool_closed["n"] == 0:
                    raise httpx.ConnectError("[Errno 54] Connection reset by peer")
                return httpx.Response(200, json={"config": {"Env": ["A=1"]}})

        set_retry_backoff_for_tests(0.001)
        body = _registry_get(FakeClient(), "https://registry/v2/x/blobs/sha256:ab", {})

        assert body == {"config": {"Env": ["A=1"]}}
        assert attempts["n"] == 2
        assert pool_closed["n"] == 1

    def test_a_missing_pool_attribute_does_not_break_the_retry(self):
        # Reaching into `_transport._pool` is not public API. A future httpx that
        # renames it must degrade to a plain retry, not raise.
        from novita_sandbox.core.template.image_config import _discard_connections

        class Bare:
            pass

        _discard_connections(Bare())  # must not raise
