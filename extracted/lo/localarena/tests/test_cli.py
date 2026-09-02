from __future__ import annotations

import contextlib
import io
import json
import tempfile
import unittest
from collections.abc import Mapping
from pathlib import Path
from unittest.mock import patch

from localarena.cli import _models_from_config, _tasks_from_config, main
from localarena.evaluation import ModelTarget
from localarena.generation import GenerationRequest, GenerationResult, ModelInfo
from localarena.providers import HttpResponse, create_provider as create_real_provider


class ConfigProvider:
    name = "llamacpp"

    def generate(self, request: GenerationRequest) -> GenerationResult:
        return GenerationResult(
            text="42" if request.model == "good" else "41",
            provider=self.name,
            model=request.model,
        )

    def list_models(self) -> tuple[ModelInfo, ...]:
        return (
            ModelInfo("good", self.name),
            ModelInfo("other", self.name),
        )


class TaskFileTests(unittest.TestCase):
    def test_task_files_are_resolved_relative_to_the_config(self) -> None:
        manifest = {
            "schema_version": 1,
            "name": "CLI pack",
            "version": "1",
            "license": "MIT",
            "tasks": [
                {
                    "id": "packed",
                    "prompt": "Reply with 42.",
                    "evaluator": {
                        "type": "match",
                        "expected": ["42"],
                    },
                }
            ],
        }
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "tasks.localarena").write_text(
                json.dumps(manifest),
                encoding="utf-8",
            )
            tasks = _tasks_from_config(
                {"task_files": ["tasks.localarena"]},
                (
                    ModelTarget(
                        "good",
                        ConfigProvider(),
                        "good",
                    ),
                ),
                base_directory=root,
            )

        self.assertEqual([task.id for task in tasks], ["packed"])
        provenance = tasks[0].metadata["localarena_task_pack"]
        self.assertEqual(provenance["version"], "1")


class RecordingTransport:
    def __init__(
        self,
        *,
        content: str = "42",
        status: int = 200,
        error_message: str = "request denied",
    ) -> None:
        self.content = content
        self.status = status
        self.error_message = error_message
        self.calls: list[dict[str, object]] = []

    def request(
        self,
        *,
        method: str,
        url: str,
        headers: Mapping[str, str],
        body: bytes | None,
        timeout: float,
        max_response_bytes: int,
    ) -> HttpResponse:
        payload = json.loads(body) if body is not None else None
        self.calls.append(
            {
                "method": method,
                "url": url,
                "authorization": headers.get("Authorization"),
                "payload": payload,
                "timeout": timeout,
                "max_response_bytes": max_response_bytes,
            }
        )
        if self.status >= 400:
            response_payload: object = {
                "error": {"message": self.error_message}
            }
        else:
            if not isinstance(payload, Mapping):
                raise AssertionError("generation request must be an object")
            response_payload = {
                "id": "chatcmpl-transport-fixture",
                "created": 123,
                "model": payload["model"],
                "choices": [
                    {
                        "index": 0,
                        "message": {
                            "role": "assistant",
                            "content": self.content,
                        },
                        "finish_reason": "stop",
                    }
                ],
                "usage": {
                    "prompt_tokens": 10,
                    "completion_tokens": 1,
                    "total_tokens": 11,
                },
            }
        return HttpResponse(
            status=self.status,
            headers={"Content-Type": "application/json"},
            body=json.dumps(response_payload, separators=(",", ":")).encode(),
        )


class CliTests(unittest.TestCase):
    def test_run_executes_config_and_writes_results_and_report(self) -> None:
        config = {
            "name": "CLI run",
            "concurrency": 2,
            "models": [
                {
                    "name": "good",
                    "provider": "llamacpp",
                    "model": "good",
                },
                {
                    "name": "other",
                    "provider": "llamacpp",
                    "model": "other",
                },
            ],
            "tasks": [
                {
                    "id": "math",
                    "prompt": "Six times seven?",
                    "evaluator": {"type": "exact", "expected": "42"},
                }
            ],
        }
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            config_path = root / "config.json"
            results_path = root / "results.json"
            report_path = root / "report.html"
            config_path.write_text(json.dumps(config))

            with (
                patch("localarena.cli.create_provider", return_value=ConfigProvider()),
                contextlib.redirect_stdout(io.StringIO()),
                contextlib.redirect_stderr(io.StringIO()),
            ):
                code = main(
                    [
                        "run",
                        str(config_path),
                        "--output",
                        str(results_path),
                        "--report",
                        str(report_path),
                    ]
                )

            self.assertEqual(code, 0)
            payload = json.loads(results_path.read_text())
            self.assertEqual(len(payload["records"]), 2)
            self.assertEqual(payload["summary"][0]["name"], "good")
            self.assertFalse(payload["include_content"])
            self.assertIsNone(payload["records"][0]["generation"]["text"])
            self.assertIn("Task matrix", report_path.read_text())
            self.assertNotIn("base_url", results_path.read_text())

    def test_models_lists_discovered_ids(self) -> None:
        output = io.StringIO()
        with (
            patch("localarena.cli.create_provider", return_value=ConfigProvider()),
            contextlib.redirect_stdout(output),
        ):
            code = main(["models", "llamacpp"])
        self.assertEqual(code, 0)
        self.assertEqual(output.getvalue().splitlines(), ["good", "other"])

    def test_quickstart_runs_scored_live_call_and_writes_safe_outputs(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            results_path = root / "results.json"
            report_path = root / "report.html"
            output = io.StringIO()

            with (
                patch(
                    "localarena.cli.create_provider",
                    return_value=ConfigProvider(),
                ) as create,
                contextlib.redirect_stdout(output),
                contextlib.redirect_stderr(io.StringIO()),
            ):
                code = main(
                    [
                        "quickstart",
                        "ollama",
                        "good",
                        "--output",
                        str(results_path),
                        "--report",
                        str(report_path),
                    ]
                )

            self.assertEqual(code, 0)
            create.assert_called_once()
            self.assertEqual(create.call_args.args, ("ollama",))
            self.assertEqual(create.call_args.kwargs["base_url"], None)
            self.assertEqual(create.call_args.kwargs["api_key"], None)
            payload = json.loads(results_path.read_text())
            self.assertEqual(len(payload["records"]), 1)
            self.assertEqual(payload["records"][0]["score"]["value"], 1)
            self.assertTrue(payload["records"][0]["score"]["passed"])
            self.assertFalse(payload["include_content"])
            self.assertIsNone(payload["records"][0]["generation"]["text"])
            serialized = results_path.read_text()
            self.assertNotIn("Reply with exactly", serialized)
            self.assertNotIn("base_url", serialized)
            self.assertIn("Task matrix", report_path.read_text())
            self.assertIn("score=1.000", output.getvalue())
            self.assertIn(f"Results: {results_path}", output.getvalue())
            self.assertIn(f"Report: {report_path}", output.getvalue())

    def test_quickstart_supports_every_profile_and_explicit_credentials(
        self,
    ) -> None:
        profiles = (
            "llamacpp",
            "ollama",
            "lmstudio",
            "openrouter",
            "openai",
            "custom",
        )
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for profile in profiles:
                with self.subTest(profile=profile):
                    arguments = [
                        "quickstart",
                        profile,
                        "good",
                        "--output",
                        str(root / f"{profile}.json"),
                        "--report",
                        str(root / f"{profile}.html"),
                    ]
                    if profile == "custom":
                        arguments.extend(
                            [
                                "--base-url",
                                "https://inference.example.com/v1",
                                "--api-key-env",
                                "LOCALARENA_TEST_KEY",
                            ]
                        )
                    with (
                        patch.dict(
                            "os.environ",
                            {"LOCALARENA_TEST_KEY": "runtime-secret"},
                            clear=True,
                        ),
                        patch(
                            "localarena.cli.create_provider",
                            return_value=ConfigProvider(),
                        ) as create,
                        contextlib.redirect_stdout(io.StringIO()),
                        contextlib.redirect_stderr(io.StringIO()),
                    ):
                        code = main(arguments)

                    self.assertEqual(code, 0)
                    self.assertEqual(create.call_args.args, (profile,))
                    if profile == "custom":
                        self.assertEqual(
                            create.call_args.kwargs["base_url"],
                            "https://inference.example.com/v1",
                        )
                        self.assertEqual(
                            create.call_args.kwargs["api_key"],
                            "runtime-secret",
                        )
                        self.assertNotIn(
                            "runtime-secret",
                            (root / f"{profile}.json").read_text(),
                        )

    def test_quickstart_profiles_serialize_compatible_http_requests(
        self,
    ) -> None:
        profiles = (
            "llamacpp",
            "ollama",
            "lmstudio",
            "openrouter",
            "openai",
            "custom",
        )
        transport = RecordingTransport()

        def create_with_transport(
            profile: str,
            **kwargs: object,
        ) -> object:
            return create_real_provider(
                profile,
                transport=transport,
                **kwargs,
            )

        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            base_url = "https://fixture.example/v1"
            with patch.dict(
                "os.environ",
                {"LOCALARENA_DOC_TEST_KEY": "fixture-secret"},
                clear=True,
            ), patch(
                "localarena.cli.create_provider",
                side_effect=create_with_transport,
            ):
                for profile in profiles:
                    with (
                        self.subTest(profile=profile),
                        contextlib.redirect_stdout(io.StringIO()),
                        contextlib.redirect_stderr(io.StringIO()),
                    ):
                        code = main(
                            [
                                "quickstart",
                                profile,
                                f"{profile}-model",
                                "--base-url",
                                base_url,
                                "--api-key-env",
                                "LOCALARENA_DOC_TEST_KEY",
                                "--output",
                                str(root / f"{profile}.json"),
                                "--report",
                                str(root / f"{profile}.html"),
                            ]
                        )
                        self.assertEqual(code, 0)
                        payload = json.loads(
                            (root / f"{profile}.json").read_text()
                        )
                        self.assertEqual(payload["records"][0]["status"], "ok")
                        self.assertEqual(
                            payload["records"][0]["score"]["value"],
                            1,
                        )
                        serialized = (root / f"{profile}.json").read_text()
                        self.assertNotIn("fixture-secret", serialized)
                        self.assertNotIn(base_url, serialized)

            self.assertEqual(len(transport.calls), len(profiles))
            for profile, call in zip(
                profiles,
                transport.calls,
                strict=True,
            ):
                self.assertEqual(
                    call["url"],
                    "https://fixture.example/v1/chat/completions",
                )
                self.assertEqual(
                    call["authorization"],
                    "Bearer fixture-secret",
                )
                payload = call["payload"]
                self.assertEqual(payload["model"], f"{profile}-model")
                self.assertFalse(payload["stream"])
                token_field = (
                    "max_completion_tokens"
                    if profile == "openai"
                    else "max_tokens"
                )
                self.assertEqual(payload[token_field], 512)

    def test_quickstart_provider_failure_prints_safe_guidance(self) -> None:
        secret = "runtime-fixture-secret"
        base_url = "https://fixture.example/v1"
        rejected_detail = (
            f"credential {secret} was denied by {base_url}"
        )
        transport = RecordingTransport(
            status=401,
            error_message=rejected_detail,
        )

        def create_with_transport(
            profile: str,
            **kwargs: object,
        ) -> object:
            return create_real_provider(
                profile,
                transport=transport,
                **kwargs,
            )

        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            results_path = root / "results.json"
            report_path = root / "report.html"
            output = io.StringIO()
            errors = io.StringIO()
            with (
                patch.dict(
                    "os.environ",
                    {"LOCALARENA_TEST_KEY": secret},
                    clear=True,
                ),
                patch(
                    "localarena.cli.create_provider",
                    side_effect=create_with_transport,
                ),
                contextlib.redirect_stdout(output),
                contextlib.redirect_stderr(errors),
            ):
                code = main(
                    [
                        "quickstart",
                        "custom",
                        "fixture-model",
                        "--base-url",
                        base_url,
                        "--api-key-env",
                        "LOCALARENA_TEST_KEY",
                        "--output",
                        str(results_path),
                        "--report",
                        str(report_path),
                    ]
                )

            self.assertEqual(code, 2)
            payload = json.loads(results_path.read_text())
            record = payload["records"][0]
            self.assertEqual(record["status"], "generation_error")
            self.assertEqual(
                record["error"],
                "ProviderAuthError: details not retained",
            )
            self.assertEqual(record["error_metadata"]["status_code"], 401)
            self.assertTrue(report_path.exists())
            diagnostics = errors.getvalue()
            self.assertIn(
                "Quickstart error: ProviderAuthError (HTTP 401)",
                diagnostics,
            )
            self.assertIn("check the key and model access", diagnostics)
            for rendered in (
                results_path.read_text(),
                report_path.read_text(),
                output.getvalue(),
                diagnostics,
            ):
                self.assertNotIn(secret, rendered)
                self.assertNotIn(base_url, rendered)
                self.assertNotIn(rejected_detail, rendered)

    def test_quickstart_scorer_mismatch_is_a_successful_evaluation(
        self,
    ) -> None:
        transport = RecordingTransport(content="41")

        def create_with_transport(
            profile: str,
            **kwargs: object,
        ) -> object:
            return create_real_provider(
                profile,
                transport=transport,
                **kwargs,
            )

        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            results_path = root / "results.json"
            output = io.StringIO()
            with (
                patch(
                    "localarena.cli.create_provider",
                    side_effect=create_with_transport,
                ),
                contextlib.redirect_stdout(output),
                contextlib.redirect_stderr(io.StringIO()),
            ):
                code = main(
                    [
                        "quickstart",
                        "llamacpp",
                        "fixture-model",
                        "--base-url",
                        "https://fixture.example/v1",
                        "--output",
                        str(results_path),
                        "--report",
                        str(root / "report.html"),
                    ]
                )

            self.assertEqual(code, 0)
            record = json.loads(results_path.read_text())["records"][0]
            self.assertEqual(record["status"], "ok")
            self.assertEqual(record["score"]["value"], 0)
            self.assertFalse(record["score"]["passed"])
            self.assertIn("score=0.000", output.getvalue())
            self.assertIn("errors=0", output.getvalue())

    def test_quickstart_rejects_identical_output_and_report_paths(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "same-output"
            errors = io.StringIO()
            with (
                patch("localarena.cli.create_provider") as create,
                contextlib.redirect_stderr(errors),
                self.assertRaises(SystemExit) as raised,
            ):
                main(
                    [
                        "quickstart",
                        "llamacpp",
                        "fixture-model",
                        "--output",
                        str(path),
                        "--report",
                        str(path),
                    ]
                )

            self.assertEqual(raised.exception.code, 2)
            create.assert_not_called()
            self.assertFalse(path.exists())
            self.assertIn(
                "--output and --report must be different paths",
                errors.getvalue(),
            )

    def test_quickstart_include_content_is_explicit(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            results_path = root / "results.json"
            with (
                patch(
                    "localarena.cli.create_provider",
                    return_value=ConfigProvider(),
                ),
                contextlib.redirect_stdout(io.StringIO()),
                contextlib.redirect_stderr(io.StringIO()),
            ):
                code = main(
                    [
                        "quickstart",
                        "llamacpp",
                        "good",
                        "--include-content",
                        "--output",
                        str(results_path),
                        "--report",
                        str(root / "report.html"),
                    ]
                )

            self.assertEqual(code, 0)
            payload = json.loads(results_path.read_text())
            self.assertTrue(payload["include_content"])
            self.assertEqual(payload["records"][0]["generation"]["text"], "42")
            self.assertIn(
                "Reply with exactly",
                payload["tasks"][0]["messages"][0]["content"],
            )

    def test_include_content_flag_is_explicit(self) -> None:
        config = {
            "models": [
                {
                    "name": "good",
                    "provider": "llamacpp",
                    "model": "good",
                }
            ],
            "tasks": [{"id": "task", "prompt": "private prompt"}],
        }
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            config_path = root / "config.json"
            results_path = root / "results.json"
            config_path.write_text(json.dumps(config))
            with (
                patch(
                    "localarena.cli.create_provider",
                    return_value=ConfigProvider(),
                ),
                contextlib.redirect_stdout(io.StringIO()),
                contextlib.redirect_stderr(io.StringIO()),
            ):
                code = main(
                    [
                        "run",
                        str(config_path),
                        "--output",
                        str(results_path),
                        "--include-content",
                    ]
                )

            self.assertEqual(code, 0)
            payload = json.loads(results_path.read_text())
            self.assertTrue(payload["include_content"])
            self.assertEqual(payload["records"][0]["generation"]["text"], "42")

    def test_judge_only_model_is_not_a_contestant(self) -> None:
        config = {
            "models": [
                {
                    "name": "candidate",
                    "provider": "llamacpp",
                    "model": "good",
                },
                {
                    "name": "judge",
                    "provider": "ollama",
                    "model": "judge",
                    "judge_only": True,
                },
            ],
            "tasks": [
                {
                    "id": "task",
                    "prompt": "prompt",
                    "evaluator": {
                        "type": "model_judge",
                        "model": "judge",
                    },
                }
            ],
        }
        with patch(
            "localarena.cli.create_provider",
            return_value=ConfigProvider(),
        ):
            candidates, targets = _models_from_config(config)
            tasks = _tasks_from_config(config, targets)

        self.assertEqual([target.name for target in candidates], ["candidate"])
        self.assertEqual([target.name for target in targets], ["candidate", "judge"])
        self.assertEqual(tasks[0].evaluator.target.name, "judge")

    def test_config_rejects_literal_api_keys(self) -> None:
        config = {
            "models": [
                {
                    "name": "unsafe",
                    "provider": "openrouter",
                    "model": "model",
                    "api_key": "do-not-store-this",
                }
            ],
            "tasks": [{"id": "task", "prompt": "prompt"}],
        }
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            config_path = root / "config.json"
            config_path.write_text(json.dumps(config))
            with (
                contextlib.redirect_stderr(io.StringIO()),
                self.assertRaises(SystemExit) as raised,
            ):
                main(
                    [
                        "run",
                        str(config_path),
                        "--output",
                        str(root / "results.json"),
                    ]
                )
        self.assertEqual(raised.exception.code, 2)

    def test_config_rejects_unknown_fields_and_literal_secret_headers(self) -> None:
        configs = (
            {
                "models": [
                    {
                        "name": "typo",
                        "provider": "llamacpp",
                        "model": "model",
                        "parameters": {"max_token": 12},
                    }
                ],
                "tasks": [{"id": "task", "prompt": "prompt"}],
            },
            {
                "models": [
                    {
                        "name": "unsafe",
                        "provider": "custom",
                        "base_url": "https://example.com/v1",
                        "model": "model",
                        "headers": {"X-API-Key": "do-not-store-this"},
                    }
                ],
                "tasks": [{"id": "task", "prompt": "prompt"}],
            },
        )

        for config in configs:
            with self.subTest(config=config):
                with tempfile.TemporaryDirectory() as directory:
                    root = Path(directory)
                    config_path = root / "config.json"
                    config_path.write_text(json.dumps(config))
                    with (
                        contextlib.redirect_stderr(io.StringIO()),
                        self.assertRaises(SystemExit) as raised,
                    ):
                        main(
                            [
                                "run",
                                str(config_path),
                                "--output",
                                str(root / "results.json"),
                            ]
                        )
                self.assertEqual(raised.exception.code, 2)


if __name__ == "__main__":
    unittest.main()
