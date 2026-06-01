"""Multi-provider support for codrninja."""

import json
import os
from abc import ABC, abstractmethod
from typing import Dict, Iterator, List, Optional, Any

import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

from .auth import OAuthFlow, TokenManager


# ── OpenAI Responses API helpers ──────────────────────────────────────────────

_RESPONSES_API_MODELS = frozenset({
    "gpt-5.5", "gpt-5.4", "gpt-5.4-mini", "gpt-5.3-codex",
    "gpt-5.3-codex-spark", "gpt-5.2", "gpt-5",
    "codex-mini-latest", "codex-davinci-002",
})

CODEX_RESPONSES_ENDPOINT = "https://chatgpt.com/backend-api/codex/responses"

_CODEX_OAUTH_SUPPORTED = frozenset({"gpt-5.5"})


def _needs_responses_api(model: str) -> bool:
    return model in _RESPONSES_API_MODELS or model.startswith("gpt-5")


def _get_model_config(model: str) -> dict:
    if model.startswith("gpt-5"):
        return {"system_mode": "developer"}
    return {"system_mode": "system"}


def _codrninja_version() -> str:
    try:
        import importlib.metadata
        return importlib.metadata.version("codrninja")
    except Exception:
        return "1.5"


def _convert_messages_to_responses_input(messages: list, model: str) -> tuple:
    mode = _get_model_config(model)["system_mode"]
    input_arr: list = []
    instructions = ""
    for msg in messages:
        role = msg.get("role", "")
        content = msg.get("content", "")
        if not isinstance(content, str):
            content = ""
        if role == "system":
            if mode == "developer":
                instructions = content
            else:
                input_arr.append({"role": "system", "content": content})
        elif role == "user":
            input_arr.append({"role": "user", "content": [{"type": "input_text", "text": content}]})
        elif role == "assistant":
            input_arr.append({"role": "assistant", "content": [{"type": "output_text", "text": content}]})
    return input_arr, instructions


class BaseProvider(ABC):

    def __init__(self, config: Dict[str, Any]):
        self.config = config

    @abstractmethod
    def chat(self, messages: List[Dict], model: Optional[str] = None) -> Dict[str, Any]:
        pass

    @abstractmethod
    def chat_stream(self, messages: List[Dict], model: Optional[str] = None) -> Iterator[Dict[str, Any]]:
        """Yield dicts: {'delta': str, 'model': str, 'tokens_input': int, 'tokens_output': int, 'done': bool}"""
        pass

    @abstractmethod
    def list_models(self) -> List[str]:
        pass

    @abstractmethod
    def get_default_model(self) -> str:
        pass


# ── Ollama ────────────────────────────────────────────────────────────────────

class OllamaProvider(BaseProvider):

    def _base_url(self) -> str:
        url = self.config.get("url", "http://localhost:11434")
        if not url.startswith("http://") and not url.startswith("https://"):
            url = "http://" + url
        return url.rstrip("/")

    def _api_key(self) -> str:
        return self.config.get("api_key") or os.environ.get("OLLAMA_API_KEY", "")

    def _auth_headers(self) -> dict:
        key = self._api_key()
        if key:
            return {"Authorization": f"Bearer {key}"}
        return {}

    def _payload(self, messages, model, stream: bool) -> dict:
        payload = {
            "model": model or self.config.get("model") or "",
            "messages": messages,
            "stream": stream,
        }
        if not self._api_key():  # only for local Ollama
            reasoning = self.config.get("reasoning_level", "medium")
            num_ctx_map = {"none": 4096, "low": 8192, "medium": 16384, "high": 32768}
            num_ctx = self.config.get("num_ctx") or num_ctx_map.get(reasoning, 16384)
            payload["options"] = {
                "temperature": self.config.get("temperature", 0.7),
                "num_predict": self.config.get("max_tokens", 16384),
                "num_ctx": num_ctx,
            }
        return payload

    def chat(self, messages: List[Dict], model: Optional[str] = None) -> Dict[str, Any]:
        model = model or self.config.get("model") or ""
        try:
            r = requests.post(
                f"{self._base_url()}/api/chat",
                json=self._payload(messages, model, stream=False),
                headers=self._auth_headers(),
                timeout=300,
            )
            r.raise_for_status()
            data = r.json()
            return {
                "content": data.get("message", {}).get("content", ""),
                "model": model,
                "tokens_input": data.get("prompt_eval_count", 0),
                "tokens_output": data.get("eval_count", 0),
                "done": True,
            }
        except requests.exceptions.ConnectionError:
            return {"error": f"Cannot connect to Ollama at {self._base_url()}", "content": ""}
        except Exception as e:
            return {"error": str(e), "content": ""}

    def chat_stream(self, messages: List[Dict], model: Optional[str] = None) -> Iterator[Dict[str, Any]]:
        model = model or self.config.get("model") or ""
        try:
            with requests.post(
                f"{self._base_url()}/api/chat",
                json=self._payload(messages, model, stream=True),
                headers=self._auth_headers(),
                stream=True,
                timeout=300,
            ) as r:
                r.raise_for_status()
                tokens_in = tokens_out = 0
                for raw in r.iter_lines():
                    if not raw:
                        continue
                    try:
                        data = json.loads(raw)
                    except json.JSONDecodeError:
                        continue
                    if data.get("error"):
                        yield {"error": data["error"], "delta": "", "done": True}
                        return
                    delta = data.get("message", {}).get("content", "")
                    tokens_in = data.get("prompt_eval_count", tokens_in)
                    tokens_out = data.get("eval_count", tokens_out)
                    if delta:
                        yield {"delta": delta, "model": model, "tokens_input": tokens_in,
                               "tokens_output": tokens_out, "done": False}
                    if data.get("done"):
                        yield {"delta": "", "model": model, "tokens_input": tokens_in,
                               "tokens_output": tokens_out, "done": True}
                        return
        except Exception as e:
            yield {"error": str(e), "delta": "", "done": True}

    def list_models(self) -> List[str]:
        api_key = self._api_key()
        # Try official ollama Python client first
        try:
            from ollama import Client as OllamaClient
            headers = {}
            if api_key:
                headers["Authorization"] = f"Bearer {api_key}"
            client = OllamaClient(host=self._base_url(), headers=headers)
            result = client.list()
            models = result.get("models") or []
            return [m.get("model") or m.get("name", "") for m in models if m.get("model") or m.get("name")]
        except ImportError:
            pass
        except Exception:
            pass
        # Fallback: direct HTTP to /api/tags
        try:
            r = requests.get(
                f"{self._base_url()}/api/tags",
                headers=self._auth_headers(),
                timeout=10,
            )
            return [m["name"] for m in r.json().get("models", [])]
        except Exception:
            return []

    def get_default_model(self) -> str:
        return self.config.get("model") or ""


# ── OAuth-capable base ────────────────────────────────────────────────────────

class OAuthCapableProvider(BaseProvider):
    oauth_env_var: str = ""

    def _auth_headers(self) -> Dict[str, str]:
        access_token = self.config.get("access_token")
        if access_token:
            return {"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"}
        api_key = self.config.get("api_key") or os.environ.get(self.oauth_env_var)
        if not api_key:
            return {}
        return self._api_key_headers(api_key)

    @abstractmethod
    def _api_key_headers(self, api_key: str) -> Dict[str, str]:
        pass


# ── OpenAI ────────────────────────────────────────────────────────────────────

class OpenAIProvider(OAuthCapableProvider):
    oauth_env_var = "OPENAI_API_KEY"
    _BASE = "https://api.openai.com/v1"

    def _api_key_headers(self, api_key: str) -> Dict[str, str]:
        return {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}

    def _oauth_headers(self, access_token: str) -> Dict[str, str]:
        import sys
        # Codex backend requires lowercase "authorization" with NO "Bearer " prefix
        h: Dict[str, str] = {
            "authorization": access_token,
            "Content-Type": "application/json",
            "originator": "opencode",
            "User-Agent": f"codrninja/{_codrninja_version()} ({sys.platform.capitalize()})",
        }
        account_id = self.config.get("account_id") or self.config.get("accountId")
        if account_id:
            h["ChatGPT-Account-Id"] = account_id
        return h

    def _auth_headers(self) -> Dict[str, str]:
        access_token = self.config.get("access_token")
        if access_token:
            return self._oauth_headers(access_token)
        api_key = self.config.get("api_key") or os.environ.get(self.oauth_env_var)
        if not api_key:
            return {}
        return self._api_key_headers(api_key)

    def _is_oauth(self) -> bool:
        return bool(self.config.get("access_token"))

    def chat(self, messages: List[Dict], model: Optional[str] = None) -> Dict[str, Any]:
        headers = self._auth_headers()
        if not headers:
            return {"error": "OpenAI API key not set. Use /provider to configure.", "content": ""}
        model = model or self.config.get("model", "gpt-4o")
        try:
            r = requests.post(
                f"{self._BASE}/chat/completions",
                headers=headers,
                json={"model": model, "messages": messages,
                      "temperature": self.config.get("temperature", 0.7),
                      "max_tokens": self.config.get("max_tokens", 4096)},
                timeout=300,
            )
            r.raise_for_status()
            data = r.json()
            choice = data.get("choices", [{}])[0]
            usage = data.get("usage", {})
            return {
                "content": choice.get("message", {}).get("content", ""),
                "model": data.get("model", model),
                "tokens_input": usage.get("prompt_tokens", 0),
                "tokens_output": usage.get("completion_tokens", 0),
                "done": True,
            }
        except Exception as e:
            return {"error": str(e), "content": ""}

    def chat_stream(self, messages: List[Dict], model: Optional[str] = None) -> Iterator[Dict[str, Any]]:
        headers = self._auth_headers()
        if not headers:
            yield {"error": "OpenAI API key not set.", "delta": "", "done": True}
            return
        model = model or self.config.get("model", "gpt-4o")

        if self._is_oauth():
            codex_model = model if model in _CODEX_OAUTH_SUPPORTED else "gpt-5.5"
            yield from self._responses_api_stream(messages, codex_model, headers)
            return

        try:
            with requests.post(
                f"{self._BASE}/chat/completions",
                headers=headers,
                json={"model": model, "messages": messages,
                      "temperature": self.config.get("temperature", 0.7),
                      "max_tokens": self.config.get("max_tokens", 4096),
                      "stream": True},
                stream=True,
                timeout=300,
            ) as r:
                r.raise_for_status()
                actual_model = model
                tokens_in = tokens_out = 0
                for raw in r.iter_lines():
                    if not raw:
                        continue
                    line = raw.decode("utf-8") if isinstance(raw, bytes) else raw
                    if not line.startswith("data: "):
                        continue
                    payload = line[6:].strip()
                    if payload == "[DONE]":
                        yield {"delta": "", "model": actual_model,
                               "tokens_input": tokens_in, "tokens_output": tokens_out, "done": True}
                        return
                    try:
                        data = json.loads(payload)
                    except json.JSONDecodeError:
                        continue
                    if data.get("error"):
                        yield {"error": data["error"] if isinstance(data["error"], str) else str(data["error"]), "delta": "", "done": True}
                        return
                    actual_model = data.get("model", actual_model)
                    usage = data.get("usage") or {}
                    tokens_in = usage.get("prompt_tokens", tokens_in)
                    tokens_out = usage.get("completion_tokens", tokens_out)
                    delta = (data.get("choices") or [{}])[0].get("delta", {}).get("content") or ""
                    if delta:
                        yield {"delta": delta, "model": actual_model,
                               "tokens_input": tokens_in, "tokens_output": tokens_out, "done": False}
        except Exception as e:
            yield {"error": str(e), "delta": "", "done": True}

    def _responses_api_stream(self, messages: List[Dict], model: str, headers: Dict) -> Iterator[Dict[str, Any]]:
        input_arr, instructions = _convert_messages_to_responses_input(messages, model)
        payload: Dict[str, Any] = {
            "model": model,
            "input": input_arr,
            "instructions": instructions or "You are a helpful assistant.",
            "store": False,
            "stream": True,
        }
        try:
            with requests.post(
                CODEX_RESPONSES_ENDPOINT,
                headers=headers,
                json=payload,
                stream=True,
                timeout=300,
                verify=False,
            ) as r:
                r.raise_for_status()
                tokens_in = tokens_out = 0
                for raw in r.iter_lines():
                    if not raw:
                        continue
                    line = raw.decode("utf-8") if isinstance(raw, bytes) else raw
                    if not line.startswith("data: "):
                        continue
                    data_str = line[6:]
                    if data_str == "[DONE]":
                        break
                    try:
                        chunk = json.loads(data_str)
                    except json.JSONDecodeError:
                        continue
                    t = chunk.get("type", "")
                    if t == "response.output_text.delta":
                        delta = chunk.get("delta", "")
                        if delta:
                            yield {"delta": delta, "model": model,
                                   "tokens_input": tokens_in, "tokens_output": tokens_out, "done": False}
                    elif t in ("response.completed", "response.incomplete"):
                        usage = chunk.get("response", {}).get("usage", {})
                        tokens_in = usage.get("input_tokens", tokens_in)
                        tokens_out = usage.get("output_tokens", tokens_out)
                        break
                    elif t == "error":
                        yield {"error": str(chunk), "delta": "", "done": True}
                        return
                yield {"delta": "", "model": model,
                       "tokens_input": tokens_in, "tokens_output": tokens_out, "done": True}
        except Exception as e:
            yield {"error": str(e), "delta": "", "done": True}

    def list_models(self) -> List[str]:
        try:
            headers = self._auth_headers()
            if headers:
                r = requests.get(f"{self._BASE}/models", headers=headers, timeout=8)
                if r.ok:
                    ids = sorted(
                        m["id"] for m in r.json().get("data", [])
                        if any(m["id"].startswith(p) for p in ("gpt-", "o1", "o3", "o4", "codex"))
                    )
                    if ids:
                        return ids
        except Exception:
            pass
        return [
            "gpt-5.5", "gpt-5.4", "gpt-5.4-mini", "gpt-5.3-codex", "gpt-5.2", "gpt-5",
            "gpt-4.5",
            "gpt-4.1", "gpt-4.1-mini", "gpt-4.1-nano",
            "gpt-4o", "gpt-4o-mini",
            "o1", "o1-mini", "o1-pro",
            "o3", "o3-mini", "o4-mini",
            "codex-mini-latest",
        ]

    def get_default_model(self) -> str:
        return self.config.get("model", "gpt-4o")


# ── Anthropic ─────────────────────────────────────────────────────────────────

class AnthropicProvider(OAuthCapableProvider):
    oauth_env_var = "ANTHROPIC_API_KEY"
    _BASE = "https://api.anthropic.com/v1"

    def _api_key_headers(self, api_key: str) -> Dict[str, str]:
        # Tokens from `claude setup-token` start with sk-ant-oat (OAuth Access Token).
        # Requires Bearer auth + two beta flags + CLI identity headers.
        if api_key.startswith("sk-ant-oat"):
            return {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
                "anthropic-version": "2023-06-01",
                "anthropic-beta": "claude-code-20250219,oauth-2025-04-20",
                "user-agent": "claude-cli/1.0.57 (external, cli)",
                "x-app": "cli",
            }
        return {"x-api-key": api_key, "Content-Type": "application/json",
                "anthropic-version": "2023-06-01"}

    def _auth_headers(self) -> Dict[str, str]:
        headers = super()._auth_headers()
        if headers.get("Authorization"):
            headers["anthropic-version"] = "2023-06-01"
            headers.setdefault("anthropic-beta", "claude-code-20250219,oauth-2025-04-20")
            headers.setdefault("user-agent", "claude-cli/1.0.57 (external, cli)")
            headers.setdefault("x-app", "cli")
        return headers

    # Models that support extended thinking
    _THINKING_MODELS = ("claude-3-7", "claude-sonnet-4-6", "claude-opus-4-7", "claude-sonnet-4-5")
    _THINKING_BUDGET = {"low": 1024, "medium": 8000, "high": 32000}

    def _supports_thinking(self, model: str) -> bool:
        return any(t in model for t in self._THINKING_MODELS)

    # Required identity prefix when authenticating with an OAuth / setup token.
    # Without this, Anthropic rejects requests as 401/429 — the API only allows
    # OAuth-issued tokens for the "Claude Code" client identity.
    _CLAUDE_CODE_SYSTEM_PREFIX = "You are Claude Code, Anthropic's official CLI for Claude."

    def _is_oauth_auth(self) -> bool:
        if self.config.get("access_token"):
            return True
        api_key = self.config.get("api_key") or os.environ.get(self.oauth_env_var) or ""
        return api_key.startswith("sk-ant-oat")

    def _split_messages(self, messages):
        system = ""
        user_msgs = []
        for m in messages:
            if m["role"] == "system":
                system = m["content"]
            else:
                user_msgs.append({"role": m["role"], "content": m["content"]})
        return system, user_msgs

    def _build_payload(self, messages, model, stream: bool) -> dict:
        system, user_msgs = self._split_messages(messages)
        level = self.config.get("reasoning_level", "medium")
        max_tokens = self.config.get("max_tokens", 8192)
        payload: dict = {
            "model": model,
            "max_tokens": max_tokens,
            "messages": user_msgs,
        }
        if stream:
            payload["stream"] = True
        if self._is_oauth_auth():
            # OAuth tokens require system as a block array — identity block must be
            # first and standalone (concatenating into one string causes 400).
            system_blocks: list = [{"type": "text", "text": self._CLAUDE_CODE_SYSTEM_PREFIX}]
            if system:
                if system.startswith(self._CLAUDE_CODE_SYSTEM_PREFIX):
                    extra = system[len(self._CLAUDE_CODE_SYSTEM_PREFIX):].strip()
                    if extra:
                        system_blocks.append({"type": "text", "text": extra})
                else:
                    system_blocks.append({"type": "text", "text": system})
            payload["system"] = system_blocks
        elif system:
            payload["system"] = system
        if level != "none" and self._supports_thinking(model):
            budget = self._THINKING_BUDGET.get(level, 8000)
            if budget >= max_tokens:
                payload["max_tokens"] = budget + 2048
            payload["thinking"] = {"type": "enabled", "budget_tokens": budget}
        else:
            payload["temperature"] = self.config.get("temperature", 0.7)
        return payload

    @staticmethod
    def _extract_text(content_blocks) -> str:
        """Return only text blocks, skip thinking blocks."""
        return "".join(b.get("text", "") for b in content_blocks if b.get("type") == "text")

    def chat(self, messages: List[Dict], model: Optional[str] = None) -> Dict[str, Any]:
        headers = self._auth_headers()
        if not headers:
            return {"error": "Anthropic API key not set. Use /provider to configure.", "content": ""}
        model = model or self.config.get("model", "claude-sonnet-4-6")
        try:
            r = requests.post(
                f"{self._BASE}/messages",
                headers=headers,
                json=self._build_payload(messages, model, stream=False),
                timeout=300,
            )
            r.raise_for_status()
            data = r.json()
            usage = data.get("usage", {})
            return {
                "content": self._extract_text(data.get("content", [])),
                "model": data.get("model", model),
                "tokens_input": usage.get("input_tokens", 0),
                "tokens_output": usage.get("output_tokens", 0),
                "done": True,
            }
        except Exception as e:
            return {"error": str(e), "content": ""}

    def chat_stream(self, messages: List[Dict], model: Optional[str] = None) -> Iterator[Dict[str, Any]]:
        headers = self._auth_headers()
        if not headers:
            yield {"error": "Anthropic API key not set.", "delta": "", "done": True}
            return
        model = model or self.config.get("model", "claude-sonnet-4-6")
        try:
            with requests.post(
                f"{self._BASE}/messages",
                headers={**headers, "anthropic-version": "2023-06-01"},
                json=self._build_payload(messages, model, stream=True),
                stream=True,
                timeout=300,
            ) as r:
                r.raise_for_status()
                tokens_in = tokens_out = 0
                actual_model = model
                # track current block type so we skip thinking deltas
                current_block_type = "text"
                for raw in r.iter_lines():
                    if not raw:
                        continue
                    line = raw.decode("utf-8") if isinstance(raw, bytes) else raw
                    if line.startswith("data: "):
                        try:
                            data = json.loads(line[6:])
                        except json.JSONDecodeError:
                            continue
                        t = data.get("type", "")
                        if t == "error":
                            err_info = data.get("error", {})
                            err_msg = err_info.get("message", str(err_info)) if isinstance(err_info, dict) else str(err_info)
                            yield {"error": err_msg, "delta": "", "done": True}
                            return
                        if t == "content_block_start":
                            current_block_type = data.get("content_block", {}).get("type", "text")
                        elif t == "content_block_delta":
                            if current_block_type == "text":
                                delta = data.get("delta", {}).get("text", "")
                                if delta:
                                    yield {"delta": delta, "model": actual_model,
                                           "tokens_input": tokens_in, "tokens_output": tokens_out, "done": False}
                            # skip thinking_delta silently
                        elif t == "message_delta":
                            usage = data.get("usage", {})
                            tokens_out = usage.get("output_tokens", tokens_out)
                        elif t == "message_start":
                            msg = data.get("message", {})
                            actual_model = msg.get("model", actual_model)
                            usage = msg.get("usage", {})
                            tokens_in = usage.get("input_tokens", tokens_in)
                            # Yield early so callers get input token count immediately
                            if tokens_in:
                                yield {"delta": "", "model": actual_model,
                                       "tokens_input": tokens_in, "tokens_output": 0, "done": False}
                        elif t == "message_stop":
                            yield {"delta": "", "model": actual_model,
                                   "tokens_input": tokens_in, "tokens_output": tokens_out, "done": True}
                            return
        except Exception as e:
            yield {"error": str(e), "delta": "", "done": True}

    def list_models(self) -> List[str]:
        return [
            "claude-opus-4-7",
            "claude-sonnet-4-6",
            "claude-haiku-4-5",
            "claude-3-7-sonnet-20250219",
            "claude-3-5-sonnet-20241022",
            "claude-3-5-haiku-20241022",
            "claude-3-opus-20240229",
            "claude-3-haiku-20240307",
        ]

    def get_default_model(self) -> str:
        return self.config.get("model", "claude-sonnet-4-6")


# ── OpenRouter ────────────────────────────────────────────────────────────────

class OpenRouterProvider(BaseProvider):
    _BASE = "https://openrouter.ai/api/v1"

    def _headers(self) -> Dict[str, str]:
        api_key = self.config.get("api_key") or os.environ.get("OPENROUTER_API_KEY", "")
        return {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}

    def _build_payload(self, messages, model, stream: bool) -> dict:
        level = self.config.get("reasoning_level", "medium")
        payload: dict = {
            "model": model,
            "messages": messages,
            "temperature": self.config.get("temperature", 0.7),
            "max_tokens": self.config.get("max_tokens", 4096),
        }
        if stream:
            payload["stream"] = True
            payload["stream_options"] = {"include_usage": True}
        if level != "none":
            payload["reasoning"] = {"effort": level if level in ("low", "medium", "high") else "medium"}
        return payload

    def chat(self, messages: List[Dict], model: Optional[str] = None) -> Dict[str, Any]:
        if not (self.config.get("api_key") or os.environ.get("OPENROUTER_API_KEY")):
            return {"error": "OpenRouter API key not set. Use /provider to configure.", "content": ""}
        model = model or self.config.get("model", "openai/gpt-4o")
        try:
            r = requests.post(
                f"{self._BASE}/chat/completions",
                headers=self._headers(),
                json=self._build_payload(messages, model, stream=False),
                timeout=300,
            )
            r.raise_for_status()
            data = r.json()
            choice = data.get("choices", [{}])[0]
            usage = data.get("usage", {})
            return {
                "content": choice.get("message", {}).get("content", ""),
                "model": data.get("model", model),
                "tokens_input": usage.get("prompt_tokens", 0),
                "tokens_output": usage.get("completion_tokens", 0),
                "done": True,
            }
        except Exception as e:
            return {"error": str(e), "content": ""}

    def chat_stream(self, messages: List[Dict], model: Optional[str] = None) -> Iterator[Dict[str, Any]]:
        if not (self.config.get("api_key") or os.environ.get("OPENROUTER_API_KEY")):
            yield {"error": "OpenRouter API key not set.", "delta": "", "done": True}
            return
        model = model or self.config.get("model", "openai/gpt-4o")
        try:
            with requests.post(
                f"{self._BASE}/chat/completions",
                headers=self._headers(),
                json=self._build_payload(messages, model, stream=True),
                stream=True,
                timeout=300,
            ) as r:
                r.raise_for_status()
                actual_model = model
                tokens_in = tokens_out = 0
                for raw in r.iter_lines():
                    if not raw:
                        continue
                    line = raw.decode("utf-8") if isinstance(raw, bytes) else raw
                    if not line.startswith("data: "):
                        continue
                    payload = line[6:].strip()
                    if payload == "[DONE]":
                        yield {"delta": "", "model": actual_model,
                               "tokens_input": tokens_in, "tokens_output": tokens_out, "done": True}
                        return
                    try:
                        data = json.loads(payload)
                    except json.JSONDecodeError:
                        continue
                    if data.get("error"):
                        yield {"error": data["error"] if isinstance(data["error"], str) else str(data["error"]), "delta": "", "done": True}
                        return
                    actual_model = data.get("model", actual_model)
                    usage = data.get("usage") or {}
                    tokens_in = usage.get("prompt_tokens", tokens_in)
                    tokens_out = usage.get("completion_tokens", tokens_out)
                    delta = (data.get("choices") or [{}])[0].get("delta", {}).get("content") or ""
                    if delta:
                        yield {"delta": delta, "model": actual_model,
                               "tokens_input": tokens_in, "tokens_output": tokens_out, "done": False}
        except Exception as e:
            yield {"error": str(e), "delta": "", "done": True}

    def list_models(self) -> List[str]:
        try:
            r = requests.get(f"{self._BASE}/models",
                             headers=self._headers(), timeout=8)
            if r.ok:
                return sorted(m["id"] for m in r.json().get("data", []))
        except Exception:
            pass
        return ["openai/gpt-4o", "openai/gpt-4.1", "anthropic/claude-sonnet-4-6",
                "google/gemini-2.5-pro", "meta-llama/llama-3.3-70b-instruct"]

    def get_default_model(self) -> str:
        return self.config.get("model", "openai/gpt-4o")


# ── Claude CLI ───────────────────────────────────────────────────────────────

class ClaudeCliProvider(BaseProvider):
    """Routes via the local `claude` binary — uses your Claude Code subscription, no API key needed."""

    MODELS = [
        "claude-opus-4-7",
        "claude-sonnet-4-6",
        "claude-haiku-4-5",
        "claude-3-7-sonnet-20250219",
        "claude-3-5-sonnet-20241022",
        "claude-3-5-haiku-20241022",
    ]

    def _binary(self) -> str:
        import shutil
        return self.config.get("binary") or shutil.which("claude") or "claude"

    def chat(self, messages: List[Dict], model: Optional[str] = None) -> Dict[str, Any]:
        content = ""
        tokens_in = tokens_out = 0
        for chunk in self.chat_stream(messages, model):
            if chunk.get("error"):
                return {"error": chunk["error"], "content": ""}
            content += chunk.get("delta", "")
            tokens_in = chunk.get("tokens_input", tokens_in)
            tokens_out = chunk.get("tokens_output", tokens_out)
        return {
            "content": content,
            "model": model or self.get_default_model(),
            "tokens_input": tokens_in,
            "tokens_output": tokens_out,
            "done": True,
        }

    def chat_stream(self, messages: List[Dict], model: Optional[str] = None) -> Iterator[Dict[str, Any]]:
        import subprocess, json as _json
        binary = self._binary()
        model = model or self.get_default_model()
        prompt = messages[-1]["content"] if messages else ""
        cmd = [
            binary, "--print",
            "--output-format", "stream-json",
            "--verbose",
            "--model", model,
            "--dangerously-skip-permissions",
        ]
        tokens_in = tokens_out = 0
        try:
            proc = subprocess.Popen(
                cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                stderr=subprocess.DEVNULL, text=True,
            )
            proc.stdin.write(prompt)
            proc.stdin.close()
            for line in proc.stdout:
                line = line.strip()
                if not line:
                    continue
                try:
                    obj = _json.loads(line)
                except ValueError:
                    continue
                typ = obj.get("type", "")
                if typ == "assistant":
                    for block in obj.get("message", {}).get("content", []):
                        if block.get("type") == "text":
                            yield {"delta": block["text"], "model": model,
                                   "tokens_input": tokens_in, "tokens_output": tokens_out, "done": False}
                elif typ == "result":
                    usage = obj.get("usage", {})
                    tokens_in = usage.get("input_tokens", 0)
                    tokens_out = usage.get("output_tokens", 0)
            proc.wait()
        except FileNotFoundError:
            yield {"delta": "[claude CLI not found — install Claude Code first]",
                   "model": model, "tokens_input": 0, "tokens_output": 0, "done": False}
        yield {"delta": "", "model": model, "tokens_input": tokens_in, "tokens_output": tokens_out, "done": True}

    def list_models(self) -> List[str]:
        return self.MODELS

    def get_default_model(self) -> str:
        return self.config.get("model", "claude-sonnet-4-6")


# ── Manager ───────────────────────────────────────────────────────────────────

class ProviderManager:

    PROVIDERS = {
        "ollama":      OllamaProvider,
        "openai":      OpenAIProvider,
        "anthropic":   AnthropicProvider,
        "openrouter":  OpenRouterProvider,
        "claude-cli":  ClaudeCliProvider,
    }

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.current_provider = config.get("provider", "ollama")
        self.token_manager = TokenManager()
        self.oauth_buffer_minutes = int(config.get("oauth", {}).get("refresh_buffer_minutes", 5))

    def _provider_config(self, name: str) -> Dict[str, Any]:
        return dict(self.config.get("providers", {}).get(name, {}))

    def _inject_oauth(self, name: str, cfg: Dict[str, Any]) -> Dict[str, Any]:
        if name not in {"openai", "anthropic"}:
            return cfg
        tokens = self.token_manager.get_tokens(name)
        if not tokens:
            return cfg
        if self.token_manager.is_token_expired(tokens, buffer_minutes=self.oauth_buffer_minutes):
            rt = tokens.get("refresh_token")
            if rt:
                try:
                    refreshed = OAuthFlow(name).refresh(rt, metadata=tokens.get("metadata", {}))
                    if not refreshed.get("refresh_token"):
                        refreshed["refresh_token"] = rt
                    self.token_manager.store_tokens(name, refreshed)
                    tokens = refreshed
                except Exception:
                    pass
        if tokens.get("access_token"):
            cfg["access_token"] = tokens["access_token"]
        return cfg

    def get_provider(self, name: Optional[str] = None) -> BaseProvider:
        name = name or self.current_provider
        if name not in self.PROVIDERS:
            raise ValueError(f"Unknown provider: {name}. Available: {list(self.PROVIDERS.keys())}")
        return self.PROVIDERS[name](self._inject_oauth(name, self._provider_config(name)))

    def set_provider(self, name: str):
        if name not in self.PROVIDERS:
            raise ValueError(f"Unknown provider: {name}")
        self.current_provider = name

    def list_providers(self) -> List[str]:
        return list(self.PROVIDERS.keys())

    def list_models(self, provider: Optional[str] = None) -> List[str]:
        return self.get_provider(provider).list_models()
