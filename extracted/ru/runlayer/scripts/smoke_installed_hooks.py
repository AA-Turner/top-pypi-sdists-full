"""Exercise wheel-installed CLI/SDK hooks without credentials or network access.

Run outside the checkout with the artifact environment's interpreter and ``-I``.
This intentionally needs no pytest or editable development dependencies.
"""

from __future__ import annotations

import gzip
import importlib
import importlib.metadata
import json
from contextlib import nullcontext
from pathlib import Path
from types import SimpleNamespace
import unittest
from unittest.mock import patch

import httpx

from runlayer_cli.aiwatch_config_cache import parse_aiwatch_config
from runlayer_cli.hook import relay, transcript_stream


class InstalledHooksSmoke(unittest.TestCase):
    def test_packages_are_installed_artifacts(self) -> None:
        for name, module_name in (
            ("runlayer", "runlayer_cli"),
            ("runlayer-hooks-sdk", "runlayer_sdk"),
        ):
            with self.subTest(package=name):
                dist = importlib.metadata.distribution(name)
                direct_url = json.loads(dist.read_text("direct_url.json") or "{}")
                self.assertFalse(direct_url.get("dir_info", {}).get("editable"))
                module = importlib.import_module(module_name)
                self.assertTrue(
                    Path(module.__file__)
                    .resolve()
                    .is_relative_to(Path(dist.locate_file("")).resolve()),
                    f"{name} is imported from outside its installed distribution",
                )
        requirement = next(
            value
            for value in importlib.metadata.requires("runlayer") or []
            if value.startswith("runlayer-hooks-sdk==")
        )
        self.assertEqual(
            importlib.metadata.version("runlayer-hooks-sdk"),
            requirement.removeprefix("runlayer-hooks-sdk=="),
        )

    def test_relay_posts_identity_and_gzip(self) -> None:
        payload = json.dumps({"text": "hook transport smoke " * 2000})
        for target, endpoint in (
            ("enforce", "/api/v1/hooks/cursor"),
            ("tool-pre", "/api/v1/hooks/tool/pre"),
            ("tool-post", "/api/v1/hooks/tool/post"),
            ("event", "/api/v1/hooks/events"),
            ("mcp-usage", "/api/v1/hooks/mcp-usage"),
        ):
            for compress in (False, True):
                with self.subTest(target=target, compress=compress):
                    requests: list[httpx.Request] = []

                    def respond(request: httpx.Request) -> httpx.Response:
                        requests.append(request)
                        return httpx.Response(200, text="{}")

                    with (
                        httpx.Client(transport=httpx.MockTransport(respond)) as client,
                        patch.object(
                            relay, "http_client", return_value=nullcontext(client)
                        ),
                        patch.object(relay, "_compression_rejected_by_backend", False),
                    ):
                        result = relay._post(
                            "https://hooks.invalid",
                            "smoke-key",
                            payload,
                            target=target,
                            prepared=True,
                            compress=compress,
                            encodings=("gzip",),
                        )
                    self.assertEqual(result, "{}")
                    self.assertEqual(len(requests), 1)
                    request = requests[0]
                    self.assertEqual(request.url.path, endpoint)
                    self.assertEqual(request.headers["x-runlayer-api-key"], "smoke-key")
                    self.assertEqual(
                        request.headers.get("Content-Encoding"),
                        "gzip" if compress else None,
                    )
                    content = (
                        gzip.decompress(request.content)
                        if compress
                        else request.content
                    )
                    self.assertEqual(content, payload.encode())

    def test_transcript_posts_identity_and_gzip(self) -> None:
        payload = {"text": "transcript transport smoke " * 2000}
        for compress in (False, True):
            with self.subTest(compress=compress):
                requests: list[httpx.Request] = []

                def respond(request: httpx.Request) -> httpx.Response:
                    requests.append(request)
                    return httpx.Response(200, text="{}")

                config = SimpleNamespace(
                    default_host="https://hooks.invalid",
                    get_secret_for_host=lambda _: "smoke-key",
                )
                with (
                    httpx.Client(transport=httpx.MockTransport(respond)) as client,
                    patch.object(transcript_stream, "load_config", return_value=config),
                    patch.object(
                        transcript_stream, "read_managed_config", return_value={}
                    ),
                    patch.object(transcript_stream, "http_client", return_value=client),
                    patch.object(
                        relay, "compression_policy", return_value=(compress, ("gzip",))
                    ),
                    patch.object(relay, "_compression_rejected_by_backend", False),
                ):
                    poster = transcript_stream._HTTPEventPoster(debug=False)
                    try:
                        poster("claude_code", "transcript", payload)
                    finally:
                        poster.close()
                self.assertEqual(len(requests), 1)
                request = requests[0]
                self.assertEqual(request.url.path, "/api/v1/hooks/events")
                self.assertEqual(
                    request.headers.get("Content-Encoding"),
                    "gzip" if compress else None,
                )
                content = (
                    gzip.decompress(request.content) if compress else request.content
                )
                self.assertEqual(json.loads(content)["payload"], payload)

    def test_config_accepts_advertised_encodings(self) -> None:
        config = parse_aiwatch_config(
            {
                "version": 1,
                "mode": "monitor",
                "sessions": True,
                "detect_processes": False,
                "detect_containers": False,
                "project_depth": 1,
                "project_timeout": 1,
                "hook_wire_encodings": ["zstd", "gzip", "unknown"],
            }
        )
        self.assertEqual(config["hook_wire_encodings"], ("zstd", "gzip"))


if __name__ == "__main__":
    unittest.main(verbosity=2)
