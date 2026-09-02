"""Tests for update target transport and verified downloads."""

from __future__ import annotations

import hashlib
from pathlib import Path

import httpx
import pytest

import runlayer_cli.update_source as update_source
from runlayer_cli.update_contract import (
    Artifact,
    TargetRelease,
    UpdateContractError,
)
from runlayer_cli.update_source import (
    ArtifactVerificationError,
    BackendUpdateSource,
    SUPPORTED_PACKAGES,
)


def _source(handler) -> BackendUpdateSource:
    transport = httpx.MockTransport(handler)
    return BackendUpdateSource(
        host="https://runlayer.example.com/",
        org_api_key="rl_org_secret",
        client_factory=lambda **kwargs: httpx.Client(transport=transport, **kwargs),
    )


def test_supports_separate_desktop_distribution_package() -> None:
    assert SUPPORTED_PACKAGES == frozenset({"cli", "desktop", "ai-watch"})


def test_fetches_resolved_target_with_org_key() -> None:
    payload = b"installer"
    digest = hashlib.sha256(payload).hexdigest()

    def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.path == "/api/v1/binary-packages/targets"
        assert request.headers["x-runlayer-api-key"] == "rl_org_secret"
        assert request.headers["accept-encoding"] == "identity"
        return httpx.Response(
            200,
            json={
                "data": [
                    {"package": "cli", "resolved_target": None},
                    {
                        "package": "ai-watch",
                        "resolved_target": {
                            "version": "2.0.0",
                            "released_at": "2026-07-01T00:00:00Z",
                            "prerelease": False,
                            "artifacts": [
                                {
                                    "platform": "macos",
                                    "arch": "arm64",
                                    "filename": "aiwatch-2.0.0-macos-arm64.pkg",
                                    "sha256": digest,
                                    "size_bytes": len(payload),
                                    "format": "pkg",
                                }
                            ],
                        },
                    },
                ]
            },
        )

    assert _source(handler).fetch_target("ai-watch", variant=None) == TargetRelease(
        version="2.0.0",
        artifacts=(
            Artifact(
                platform="macos",
                arch="arm64",
                filename="aiwatch-2.0.0-macos-arm64.pkg",
                sha256=digest,
                size_bytes=len(payload),
                format="pkg",
            ),
        ),
    )


def test_requests_variant_targets_when_variant_is_set() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.path == "/api/v1/binary-packages/targets"
        assert request.url.params["variant"] == "glibc2.17"
        return httpx.Response(
            200,
            json={"data": [{"package": "cli", "resolved_target": None}]},
        )

    assert _source(handler).fetch_target("cli", variant="glibc2.17") is None


def test_omits_variant_param_for_standard_installs() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        assert "variant" not in request.url.params
        return httpx.Response(
            200,
            json={"data": [{"package": "cli", "resolved_target": None}]},
        )

    assert _source(handler).fetch_target("cli", variant=None) is None


def test_never_follows_redirects_with_org_key() -> None:
    requested_hosts: list[str] = []

    def handler(request: httpx.Request) -> httpx.Response:
        requested_hosts.append(request.url.host)
        if request.url.host == "runlayer.example.com":
            return httpx.Response(
                302,
                headers={"location": "https://untrusted.example.com/target"},
            )
        return httpx.Response(200, json={"data": []})

    with pytest.raises(httpx.HTTPStatusError):
        _source(handler).fetch_target("ai-watch", variant=None)

    assert requested_hosts == ["runlayer.example.com"]


def test_stops_reading_oversized_target_response() -> None:
    class OversizeTargetStream(httpx.SyncByteStream):
        def __init__(self) -> None:
            self.requested_second_chunk = False

        def __iter__(self):
            yield b"x" * (1024 * 1024 + 1)
            self.requested_second_chunk = True
            yield b"more bytes must not be consumed"

    stream = OversizeTargetStream()

    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, stream=stream)

    with pytest.raises(UpdateContractError, match="maximum"):
        _source(handler).fetch_target("ai-watch", variant=None)

    assert stream.requested_second_chunk is False


def test_rejects_oversized_target_before_download(tmp_path: Path) -> None:
    requests: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        return httpx.Response(500)

    artifact = Artifact(
        "macos",
        "arm64",
        "agent.pkg",
        "0" * 64,
        512 * 1024 * 1024 + 1,
        "pkg",
    )

    with pytest.raises(ArtifactVerificationError, match="maximum"):
        _source(handler).download("ai-watch", "2.0.0", artifact, tmp_path / "agent.pkg")

    assert requests == []


@pytest.mark.parametrize("version", [".", "..", "1/2", "1\\2", "%2F"])
def test_rejects_unsafe_version_before_download(tmp_path: Path, version: str) -> None:
    requests: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        return httpx.Response(500)

    artifact = Artifact("macos", "arm64", "agent.pkg", "0" * 64, 1, "pkg")

    with pytest.raises(ArtifactVerificationError, match="version"):
        _source(handler).download("ai-watch", version, artifact, tmp_path / "agent.pkg")

    assert requests == []


def test_download_verifies_header_and_bytes(tmp_path: Path) -> None:
    payload = b"signed installer bytes"
    digest = hashlib.sha256(payload).hexdigest()
    artifact = Artifact("macos", "arm64", "agent 2.0.pkg", digest, len(payload), "pkg")

    def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.path == (
            "/api/v1/binary-packages/ai-watch/2.0.0/agent 2.0.pkg"
        )
        assert request.headers["x-runlayer-api-key"] == "rl_org_secret"
        return httpx.Response(
            200,
            headers={"x-runlayer-sha256": digest},
            stream=httpx.ByteStream(payload),
        )

    destination = tmp_path / "agent.pkg"
    _source(handler).download("ai-watch", "2.0.0", artifact, destination)

    assert destination.read_bytes() == payload


def test_download_supports_long_artifact_filename(tmp_path: Path) -> None:
    payload = b"installer"
    digest = hashlib.sha256(payload).hexdigest()
    filename = f"{'a' * 240}.pkg"
    artifact = Artifact("macos", "arm64", filename, digest, len(payload), "pkg")

    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(
            200,
            headers={"x-runlayer-sha256": digest},
            stream=httpx.ByteStream(payload),
        )

    destination = tmp_path / filename
    _source(handler).download("ai-watch", "2.0.0", artifact, destination)

    assert destination.read_bytes() == payload
    assert list(tmp_path.iterdir()) == [destination]


@pytest.mark.parametrize(
    ("response_header", "response_body"),
    [
        (None, b"signed installer bytes"),
        ("f" * 64, b"signed installer bytes"),
        (
            hashlib.sha256(b"signed installer bytes").hexdigest(),
            b"tampered payload!!!!!",
        ),
    ],
)
def test_rejects_missing_or_mismatched_sha256(
    tmp_path: Path,
    response_header: str | None,
    response_body: bytes,
) -> None:
    expected = b"signed installer bytes"
    digest = hashlib.sha256(expected).hexdigest()
    artifact = Artifact("macos", "arm64", "agent.pkg", digest, len(expected), "pkg")

    def handler(request: httpx.Request) -> httpx.Response:
        headers = (
            {"x-runlayer-sha256": response_header}
            if response_header is not None
            else {}
        )
        return httpx.Response(
            200,
            headers=headers,
            stream=httpx.ByteStream(response_body),
        )

    destination = tmp_path / "agent.pkg"
    with pytest.raises(ArtifactVerificationError):
        _source(handler).download("ai-watch", "2.0.0", artifact, destination)

    assert not destination.exists()


def test_stops_streaming_when_declared_size_is_exceeded(tmp_path: Path) -> None:
    payload = b"1234"
    digest = hashlib.sha256(payload).hexdigest()
    artifact = Artifact("macos", "arm64", "agent.pkg", digest, len(payload), "pkg")

    class OversizeStream(httpx.SyncByteStream):
        def __init__(self) -> None:
            self.requested_second_chunk = False

        def __iter__(self):
            yield b"12345"
            self.requested_second_chunk = True
            yield b"more bytes must not be consumed"

    stream = OversizeStream()

    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(
            200,
            headers={"x-runlayer-sha256": digest},
            stream=stream,
        )

    destination = tmp_path / "agent.pkg"
    with pytest.raises(ArtifactVerificationError, match="size"):
        _source(handler).download("ai-watch", "2.0.0", artifact, destination)

    assert stream.requested_second_chunk is False
    assert not destination.exists()


def test_stops_streaming_after_total_download_deadline(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    payload = b"installer"
    digest = hashlib.sha256(payload).hexdigest()
    artifact = Artifact("macos", "arm64", "agent.pkg", digest, len(payload), "pkg")
    ticks = iter([0.0, 901.0])
    monkeypatch.setattr(update_source, "_monotonic", ticks.__next__)

    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(
            200,
            headers={"x-runlayer-sha256": digest},
            stream=httpx.ByteStream(payload),
        )

    destination = tmp_path / "agent.pkg"
    with pytest.raises(ArtifactVerificationError, match="deadline"):
        _source(handler).download("ai-watch", "2.0.0", artifact, destination)

    assert not destination.exists()
