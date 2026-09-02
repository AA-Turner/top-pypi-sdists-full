from __future__ import annotations

import asyncio
import copy
import json
import pickle
import socket
import unittest
from collections.abc import Mapping
from urllib.error import URLError

from localarena.errors import (
    ProviderAuthError,
    ProviderConfigurationError,
    ProviderRateLimitError,
    ProviderResponseError,
)
from localarena.generation import (
    ChatMessage,
    GenerationRequest,
    GenerationResult,
    ModelInfo,
    TokenUsage,
)
from localarena.providers import (
    HttpResponse,
    OpenAICompatibleProvider,
    RequestPolicy,
    create_provider,
    provider_names,
)


def json_response(
    payload: object,
    *,
    status: int = 200,
    headers: Mapping[str, str] | None = None,
) -> HttpResponse:
    return HttpResponse(
        status=status,
        headers={} if headers is None else headers,
        body=json.dumps(payload, separators=(",", ":")).encode(),
    )


def completion_response(
    text: object = "Hello",
    *,
    model: str = "served-model",
) -> HttpResponse:
    return json_response(
        {
            "id": "chatcmpl-test",
            "created": 123,
            "model": model,
            "service_tier": "default",
            "system_fingerprint": "fp_test",
            "choices": [
                {
                    "index": 0,
                    "message": {"role": "assistant", "content": text},
                    "finish_reason": "stop",
                }
            ],
            "usage": {
                "prompt_tokens": 7,
                "completion_tokens": 3,
                "total_tokens": 10,
                "prompt_tokens_details": {"cached_tokens": 2},
                "completion_tokens_details": {"reasoning_tokens": 1},
            },
            "timings": {"predicted_per_second": 42.5},
        }
    )


class FakeTransport:
    def __init__(self, *outcomes: HttpResponse | BaseException) -> None:
        self.outcomes = list(outcomes)
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
        self.calls.append(
            {
                "method": method,
                "url": url,
                "headers": dict(headers),
                "body": body,
                "timeout": timeout,
                "max_response_bytes": max_response_bytes,
            }
        )
        if not self.outcomes:
            raise AssertionError("unexpected transport request")
        outcome = self.outcomes.pop(0)
        if isinstance(outcome, BaseException):
            raise outcome
        return outcome


class GenerationRecordTests(unittest.TestCase):
    def test_request_is_immutable_and_rejects_reserved_extra_fields(self) -> None:
        extra = {"top_p": 0.9, "nested": {"items": [1]}}
        request = GenerationRequest(
            model="model-a",
            messages=[ChatMessage("user", "Hello")],
            stop=["END"],
            extra_body=extra,
        )
        extra["nested"]["items"].append(2)  # type: ignore[index,union-attr]

        self.assertEqual(request.stop, ("END",))
        self.assertEqual(request.extra_body["nested"]["items"], (1,))  # type: ignore[index]
        with self.assertRaises(TypeError):
            request.extra_body["new"] = True  # type: ignore[index]
        with self.assertRaises(ValueError):
            GenerationRequest(
                "model",
                [ChatMessage("user", "x")],
                extra_body={"stream": True},
            )
        with self.assertRaises(ValueError):
            GenerationRequest(
                "model",
                [ChatMessage("user", "x")],
                extra_body={"max_completion_tokens": 10},
            )
        self.assertIs(copy.deepcopy(request), request)

    def test_generation_records_are_json_safe_and_detached(self) -> None:
        metadata = {"nested": [{"value": 1}]}
        result = GenerationResult(
            text="answer",
            provider="custom",
            model="model",
            usage=TokenUsage(input_tokens=2, output_tokens=3, total_tokens=5),
            metadata=metadata,
        )
        metadata["nested"][0]["value"] = 99
        snapshot = result.to_dict()

        self.assertEqual(snapshot["metadata"]["nested"][0]["value"], 1)  # type: ignore[index]
        snapshot["metadata"]["nested"][0]["value"] = 7  # type: ignore[index]
        self.assertEqual(result.to_dict()["metadata"]["nested"][0]["value"], 1)  # type: ignore[index]
        self.assertIs(copy.deepcopy(result), result)

    def test_message_and_usage_validation_is_strict(self) -> None:
        with self.assertRaises(TypeError):
            ChatMessage([], "x")  # type: ignore[arg-type]
        with self.assertRaises(ValueError):
            ChatMessage("tool", "x")  # type: ignore[arg-type]
        with self.assertRaises(ValueError):
            GenerationRequest("model", [])
        with self.assertRaises(ValueError):
            TokenUsage(input_tokens=-1)
        with self.assertRaises(ValueError):
            TokenUsage(input_tokens=10**20)
        with self.assertRaises(ValueError):
            GenerationResult(
                text="answer",
                provider="custom",
                model="model",
                attempts=10**20,
            )


class OpenAICompatibleProviderTests(unittest.TestCase):
    def test_construction_is_side_effect_free_and_generation_is_normalized(
        self,
    ) -> None:
        transport = FakeTransport(completion_response())
        secret = "plain-secret-value-1234"
        provider = OpenAICompatibleProvider(
            "http://localhost:8080/v1/",
            secret,
            name="llamacpp",
            headers={"X-Title": "LocalArena"},
            policy=RequestPolicy(timeout=4, max_attempts=1),
            transport=transport,
        )

        self.assertEqual(transport.calls, [])
        self.assertNotIn(secret, repr(provider))
        self.assertNotIn("localhost", repr(provider))
        with self.assertRaisesRegex(TypeError, "cannot be serialized"):
            pickle.dumps(provider)

        result = provider.generate(
            GenerationRequest(
                model="requested-model",
                messages=(
                    ChatMessage("system", "Be concise."),
                    ChatMessage("user", "Hello"),
                ),
                max_tokens=64,
                temperature=0.2,
                seed=7,
                stop=("END",),
                extra_body={"top_p": 0.9},
            )
        )

        self.assertEqual(len(transport.calls), 1)
        call = transport.calls[0]
        self.assertEqual(call["method"], "POST")
        self.assertEqual(
            call["url"],
            "http://localhost:8080/v1/chat/completions",
        )
        headers = call["headers"]
        self.assertEqual(headers["Authorization"], f"Bearer {secret}")  # type: ignore[index]
        self.assertEqual(headers["X-Title"], "LocalArena")  # type: ignore[index]
        payload = json.loads(call["body"])  # type: ignore[arg-type]
        self.assertEqual(
            payload,
            {
                "model": "requested-model",
                "messages": [
                    {"role": "system", "content": "Be concise."},
                    {"role": "user", "content": "Hello"},
                ],
                "stream": False,
                "max_tokens": 64,
                "temperature": 0.2,
                "seed": 7,
                "stop": ["END"],
                "top_p": 0.9,
            },
        )

        self.assertEqual(result.text, "Hello")
        self.assertEqual(result.provider, "llamacpp")
        self.assertEqual(result.model, "requested-model")
        self.assertEqual(result.response_model, "served-model")
        self.assertEqual(result.response_id, "chatcmpl-test")
        self.assertEqual(result.finish_reason, "stop")
        self.assertEqual(result.usage.input_tokens, 7)
        self.assertEqual(result.usage.output_tokens, 3)
        self.assertEqual(result.usage.total_tokens, 10)
        self.assertEqual(result.usage.cached_input_tokens, 2)
        self.assertEqual(result.usage.reasoning_tokens, 1)
        self.assertEqual(result.attempts, 1)
        serialized = json.dumps(result.to_dict())
        self.assertNotIn(secret, serialized)
        self.assertNotIn("localhost", serialized)

    def test_text_content_parts_and_request_id_header_are_supported(self) -> None:
        response = completion_response(
            [
                {"type": "text", "text": "one"},
                {"type": "output_text", "text": " two"},
            ]
        )
        response = HttpResponse(
            status=response.status,
            headers={"X-Request-ID": "req-header"},
            body=response.body.replace(
                b'"id":"chatcmpl-test",',
                b"",
            ),
        )
        provider = OpenAICompatibleProvider(
            "http://localhost:8080/v1",
            transport=FakeTransport(response),
            policy=RequestPolicy(max_attempts=1),
        )

        result = provider.generate(
            GenerationRequest("model", [ChatMessage("user", "hello")])
        )

        self.assertEqual(result.text, "one two")
        self.assertEqual(result.response_id, "req-header")

    def test_model_listing_uses_the_models_endpoint(self) -> None:
        transport = FakeTransport(
            json_response(
                {
                    "object": "list",
                    "data": [
                        {
                            "id": "z-model",
                            "name": "Zed",
                            "owned_by": "local",
                            "created": 12,
                            "context_length": 4096,
                            "ignored": "not copied",
                        },
                        {"id": "a-model", "object": "model"},
                    ],
                }
            )
        )
        provider = OpenAICompatibleProvider(
            "http://localhost:9000/api/v1",
            api_key="local-key-1234",
            name="custom",
            transport=transport,
            policy=RequestPolicy(max_attempts=1),
        )

        models = provider.list_models()

        self.assertEqual(
            models,
            (
                ModelInfo(
                    "z-model",
                    "custom",
                    "Zed",
                    {
                        "owned_by": "local",
                        "created": 12,
                        "context_length": 4096,
                    },
                ),
                ModelInfo("a-model", "custom"),
            ),
        )
        self.assertEqual(
            transport.calls[0]["url"],
            "http://localhost:9000/api/v1/models",
        )
        self.assertIsNone(transport.calls[0]["body"])

    def test_async_methods_delegate_without_implicit_streaming(self) -> None:
        transport = FakeTransport(
            completion_response("async"),
            json_response({"data": [{"id": "model"}]}),
        )
        provider = OpenAICompatibleProvider(
            "http://localhost:8080/v1",
            transport=transport,
            policy=RequestPolicy(max_attempts=1),
        )

        async def exercise() -> tuple[GenerationResult, tuple[ModelInfo, ...]]:
            generated = await provider.agenerate(
                GenerationRequest("model", [ChatMessage("user", "hello")])
            )
            models = await provider.alist_models()
            return generated, models

        generated, models = asyncio.run(exercise())

        self.assertEqual(generated.text, "async")
        self.assertEqual(models[0].id, "model")
        payload = json.loads(transport.calls[0]["body"])  # type: ignore[arg-type]
        self.assertIs(payload["stream"], False)

    def test_retry_is_bounded_and_attempt_count_is_reported(self) -> None:
        transport = FakeTransport(
            URLError(socket.timeout("secret socket detail")),
            completion_response("recovered"),
        )
        provider = OpenAICompatibleProvider(
            "http://localhost:8080/v1",
            transport=transport,
            policy=RequestPolicy(
                timeout=1,
                max_attempts=2,
                backoff_seconds=0,
                max_backoff_seconds=0,
            ),
        )

        result = provider.generate(
            GenerationRequest("model", [ChatMessage("user", "hello")])
        )

        self.assertEqual(result.text, "recovered")
        self.assertEqual(result.attempts, 2)
        self.assertEqual(len(transport.calls), 2)

    def test_rate_limit_retries_then_raises_typed_error(self) -> None:
        response = json_response(
            {"error": {"message": "slow down"}},
            status=429,
            headers={"Retry-After": "0"},
        )
        transport = FakeTransport(response, response)
        provider = OpenAICompatibleProvider(
            "http://localhost:8080/v1",
            transport=transport,
            policy=RequestPolicy(
                max_attempts=2,
                backoff_seconds=0,
                max_backoff_seconds=0,
            ),
        )

        with self.assertRaises(ProviderRateLimitError) as captured:
            provider.list_models()

        self.assertEqual(captured.exception.status_code, 429)
        self.assertEqual(captured.exception.attempts, 2)
        self.assertTrue(captured.exception.retryable)
        self.assertEqual(len(transport.calls), 2)

    def test_non_retryable_failure_does_not_retry_and_redacts_secrets(self) -> None:
        secret = "plain-secret-value-1234"
        base_url = "https://private.example.test/v1"
        transport = FakeTransport(
            json_response(
                {
                    "error": {
                        "message": (
                            f"bad key {secret} at {base_url}; "
                            "Authorization: Bearer sk-proj-leakedvalue123"
                        )
                    }
                },
                status=401,
            )
        )
        provider = OpenAICompatibleProvider(
            base_url,
            secret,
            headers={"X-Custom-Token": "header-secret-5678"},
            transport=transport,
            policy=RequestPolicy(max_attempts=3, backoff_seconds=0),
        )

        with self.assertRaises(ProviderAuthError) as captured:
            provider.list_models()

        message = str(captured.exception)
        self.assertNotIn(secret, message)
        self.assertNotIn(base_url, message)
        self.assertNotIn("sk-proj-leakedvalue123", message)
        self.assertIn("<redacted>", message)
        self.assertEqual(len(transport.calls), 1)

    def test_response_size_and_shape_are_bounded(self) -> None:
        oversized = HttpResponse(200, {}, b"x" * 11)
        provider = OpenAICompatibleProvider(
            "http://localhost:8080/v1",
            transport=FakeTransport(oversized),
            policy=RequestPolicy(
                max_attempts=1,
                max_response_bytes=10,
            ),
        )
        with self.assertRaisesRegex(ProviderResponseError, "size limit"):
            provider.list_models()

        invalid = OpenAICompatibleProvider(
            "http://localhost:8080/v1",
            transport=FakeTransport(HttpResponse(200, {}, b"not-json")),
            policy=RequestPolicy(max_attempts=1),
        )
        with self.assertRaisesRegex(ProviderResponseError, "invalid model list"):
            invalid.list_models()

        bad_completion = OpenAICompatibleProvider(
            "http://localhost:8080/v1",
            transport=FakeTransport(json_response({"choices": []})),
            policy=RequestPolicy(max_attempts=1),
        )
        with self.assertRaisesRegex(
            ProviderResponseError,
            "invalid chat completion",
        ):
            bad_completion.generate(
                GenerationRequest("model", [ChatMessage("user", "hello")])
            )

    def test_base_urls_and_custom_headers_are_validated(self) -> None:
        invalid_urls = (
            "ftp://localhost/v1",
            "http://user:pass@localhost/v1",
            "http://localhost/v1?key=secret",
            "http://localhost/v1#fragment",
            "http://localhost:not-a-port/v1",
            " http://localhost/v1",
            "http://localhost/a path/v1",
            "relative/v1",
        )
        for url in invalid_urls:
            with self.subTest(url=url):
                with self.assertRaises((TypeError, ValueError)):
                    OpenAICompatibleProvider(url)

        with self.assertRaises(ValueError):
            OpenAICompatibleProvider(
                "http://localhost/v1",
                headers={"Authorization": "Bearer another-key"},
            )
        with self.assertRaises(ValueError):
            OpenAICompatibleProvider(
                "http://localhost/v1",
                headers={"Host": "different.example"},
            )
        with self.assertRaises(ValueError):
            OpenAICompatibleProvider(
                "http://localhost/v1",
                headers={"X-Test": "value\r\nInjected: true"},
            )


class ProviderPresetTests(unittest.TestCase):
    def test_exact_named_profiles_and_aliases_are_available(self) -> None:
        self.assertEqual(
            provider_names(),
            (
                "llamacpp",
                "ollama",
                "lmstudio",
                "openrouter",
                "openai",
                "custom",
            ),
        )
        for profile, expected_name in (
            ("llamacpp", "llamacpp"),
            ("llama.cpp", "llamacpp"),
            ("llama-cpp", "llamacpp"),
            ("ollama", "ollama"),
            ("lmstudio", "lmstudio"),
            ("lm-studio", "lmstudio"),
        ):
            with self.subTest(profile=profile):
                provider = create_provider(profile, env={})
                self.assertEqual(provider.name, expected_name)

    def test_local_profiles_never_reuse_cloud_credentials(self) -> None:
        cases = (
            ("llamacpp", "http://127.0.0.1:8080/v1/models"),
            ("ollama", "http://127.0.0.1:11434/v1/models"),
            ("lmstudio", "http://127.0.0.1:1234/v1/models"),
        )
        for profile, expected_url in cases:
            with self.subTest(profile=profile):
                transport = FakeTransport(json_response({"data": []}))
                provider = create_provider(
                    profile,
                    env={
                        "OPENAI_API_KEY": "cloud-secret-should-not-be-used",
                        "OPENROUTER_API_KEY": "other-cloud-secret",
                    },
                    transport=transport,
                    policy=RequestPolicy(max_attempts=1),
                )
                provider.list_models()
                self.assertEqual(transport.calls[0]["url"], expected_url)
                self.assertNotIn(
                    "Authorization",
                    transport.calls[0]["headers"],  # type: ignore[operator]
                )

    def test_cloud_profiles_use_only_their_own_credentials(self) -> None:
        openai_transport = FakeTransport(completion_response())
        openai = create_provider(
            "openai",
            env={
                "OPENAI_API_KEY": "openai-secret-1234",
                "OPENROUTER_API_KEY": "wrong-secret-5678",
            },
            transport=openai_transport,
            policy=RequestPolicy(max_attempts=1),
        )
        openai.generate(
            GenerationRequest("model", [ChatMessage("user", "hello")])
        )
        openai_call = openai_transport.calls[0]
        self.assertEqual(
            openai_call["url"],
            "https://api.openai.com/v1/chat/completions",
        )
        self.assertEqual(
            openai_call["headers"]["Authorization"],  # type: ignore[index]
            "Bearer openai-secret-1234",
        )
        openai_payload = json.loads(openai_call["body"])  # type: ignore[arg-type]
        self.assertEqual(openai_payload["max_completion_tokens"], 512)
        self.assertNotIn("max_tokens", openai_payload)

        router_transport = FakeTransport(json_response({"data": []}))
        router = create_provider(
            "openrouter",
            env={
                "OPENAI_API_KEY": "wrong-secret-1234",
                "OPENROUTER_API_KEY": "router-secret-5678",
            },
            transport=router_transport,
            policy=RequestPolicy(max_attempts=1),
        )
        router.list_models()
        self.assertEqual(
            router_transport.calls[0]["url"],
            "https://openrouter.ai/api/v1/models",
        )
        self.assertEqual(
            router_transport.calls[0]["headers"]["Authorization"],  # type: ignore[index]
            "Bearer router-secret-5678",
        )

    def test_custom_is_explicit_and_does_not_read_cloud_environment(self) -> None:
        with self.assertRaises(ProviderConfigurationError):
            create_provider("custom", env={"OPENAI_API_KEY": "cloud-secret"})
        with self.assertRaises(ProviderConfigurationError):
            create_provider("openai", env={})
        with self.assertRaises(ProviderConfigurationError):
            create_provider("unknown", env={})

        transport = FakeTransport(json_response({"data": []}))
        custom = create_provider(
            "custom",
            base_url="http://localhost:7777/custom/v1",
            env={"OPENAI_API_KEY": "cloud-secret-should-not-be-used"},
            transport=transport,
            policy=RequestPolicy(max_attempts=1),
        )
        custom.list_models()
        self.assertNotIn(
            "Authorization",
            transport.calls[0]["headers"],  # type: ignore[operator]
        )

    def test_explicit_values_override_environment_values(self) -> None:
        transport = FakeTransport(json_response({"data": []}))
        provider = create_provider(
            "openrouter",
            base_url="https://router.example.test/api/v1",
            api_key="explicit-secret-1234",
            env={
                "LOCALARENA_OPENROUTER_BASE_URL": "https://wrong.example/v1",
                "OPENROUTER_API_KEY": "wrong-secret-5678",
            },
            transport=transport,
            policy=RequestPolicy(max_attempts=1),
        )
        provider.list_models()

        call = transport.calls[0]
        self.assertEqual(
            call["url"],
            "https://router.example.test/api/v1/models",
        )
        self.assertEqual(
            call["headers"]["Authorization"],  # type: ignore[index]
            "Bearer explicit-secret-1234",
        )

    def test_cloud_keys_are_not_implicitly_forwarded_to_custom_endpoints(
        self,
    ) -> None:
        with self.assertRaises(ProviderConfigurationError) as captured:
            create_provider(
                "openai",
                base_url="http://localhost:9000/v1",
                env={"OPENAI_API_KEY": "cloud-secret-must-stay-cloud-side"},
            )
        self.assertIn("LOCALARENA_OPENAI_API_KEY", str(captured.exception))
        self.assertNotIn("cloud-secret-must-stay-cloud-side", str(captured.exception))

        transport = FakeTransport(json_response({"data": []}))
        provider = create_provider(
            "openai",
            base_url="http://localhost:9000/v1",
            env={
                "OPENAI_API_KEY": "cloud-secret-must-stay-cloud-side",
                "LOCALARENA_OPENAI_API_KEY": "deliberate-local-secret",
            },
            transport=transport,
            policy=RequestPolicy(max_attempts=1),
        )
        provider.list_models()
        self.assertEqual(
            transport.calls[0]["headers"]["Authorization"],  # type: ignore[index]
            "Bearer deliberate-local-secret",
        )


if __name__ == "__main__":
    unittest.main()
