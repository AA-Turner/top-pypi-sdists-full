"""LLM client — talks to Ollama via PastaWater broker or directly to a brain."""

import json
import os
import time
import requests
from typing import Iterator


DEFAULT_API_URL = "https://pastawater.io"

# Embedding-only models (nomic-embed-text, bge-*, e5-*, gte-*) are filtered
# from "which chat model is loaded" detection — they return empty on /api/chat.
_EMBED_MARKERS = ("embed", "bge-", "-bge", "e5-", "-e5", "gte-", "-gte")

# How long to trust the last /api/ps result before re-querying in direct mode.
# Short enough to catch a mid-session model swap within a couple of seconds.
# Tokens aren't streamed through chat_stream recursively, so we won't hammer
# the brain — one probe per user-triggered LLM call at most.
_REALIGN_TTL_SECONDS = 2.0


class LLMClient:
    """Client that talks to Ollama via PastaWater broker API or direct brain connection."""

    def __init__(
        self,
        token: str = "",
        device_id: str = "",
        slot: int = 0,
        model: str = "",
        api_url: str = DEFAULT_API_URL,
        brain_url: str = "",
        brain_key: str = "",
    ):
        self.token = token
        self.device_id = device_id
        self.slot = slot
        self.model = model
        self.api_url = api_url.rstrip("/")
        self.brain_url = brain_url.rstrip("/") if brain_url else ""
        self.brain_key = brain_key
        self.direct_mode = bool(brain_url)
        # When True, _realign_model leaves self.model alone. Set by pw_agent
        # when the user passes --model X — they explicitly chose a model and
        # don't want auto-realign overriding it (e.g. with the dashboard's
        # last_known_chat_model). Ollama auto-loads X on the next /api/chat.
        self.model_locked = False

        self.session = requests.Session()
        self.session.headers["Content-Type"] = "application/json"
        self._active_response = None  # Track active streaming response for abort
        # Auth: PW token works for both cloud API and local brain proxy
        if token:
            self.session.headers["Authorization"] = f"Bearer {token}"
        if brain_key:
            self.session.headers["X-Controller-API-Key"] = brain_key
        # Last time we re-queried /api/ps to confirm our cached model matches
        # what's actually resident. Zero means "never" — forces a check on the
        # first chat call so a stale client.model from config doesn't drive
        # Ollama into a silent model swap.
        self._last_realign_ts = 0.0
        # Background realign thread — Agent.run() fires this at turn entry
        # so the /api/ps probe overlaps with the ~500-1500ms of embed calls
        # that precede chat_stream. By the time /api/chat is hit, the probe
        # has usually completed and self.model is already aligned; chat_stream
        # then skips the synchronous fallback.
        self._realign_thread = None

    def abort(self):
        """Abort the active streaming request."""
        if self._active_response:
            try:
                self._active_response.close()
            except Exception:
                pass
            self._active_response = None

    def chat(self, messages: list[dict], temperature: float = 0.3, context_length: int = 8192, thinking: bool = False) -> str:
        """Send messages and return the full response text."""
        chunks = []
        for chunk in self.chat_stream(messages, temperature, context_length, thinking=thinking):
            chunks.append(chunk)
        return "".join(chunks)

    def realign_async(self):
        """Kick off the /api/ps probe in a background thread so it overlaps
        with the memory/codebase embed calls at the start of each turn.
        Zero user-perceived latency: by the time chat_stream hits /api/chat,
        self.model has already been aligned (usually). Safe to call at the
        top of Agent.run() on every turn.

        Skipped when a probe is already in flight or when the TTL hasn't
        expired yet.
        """
        if not self.direct_mode:
            return
        existing = self._realign_thread
        if existing is not None and existing.is_alive():
            return
        if time.time() - self._last_realign_ts < _REALIGN_TTL_SECONDS:
            return
        import threading
        t = threading.Thread(target=self._realign_model, daemon=True, name="llm-realign")
        self._realign_thread = t
        t.start()

    def _realign_model(self):
        """Read-only model alignment: set self.model to whatever Ollama
        actually has resident right now. pw-agent must NEVER cause Ollama
        to swap or load a model — that's the dashboard's job. If nothing
        is resident we clear self.model so chat_stream refuses to send
        /api/chat (which would implicitly trigger a load).

        Invariant upheld: pw-agent only ever sends /api/chat with a model
        name that /api/ps currently reports as loaded. A stale cached
        value from config can never leak into the wire request.

        Only runs in direct mode; cached for ~10s so mid-turn streaming
        doesn't hammer the brain.
        """
        if not self.direct_mode:
            return self.model
        if self.model_locked:
            return self.model
        now = time.time()
        if now - self._last_realign_ts < _REALIGN_TTL_SECONDS:
            return self.model
        self._last_realign_ts = now
        try:
            resp = self.session.get(f"{self.brain_url}/api/ps", timeout=3)
            if resp.status_code != 200:
                return self.model
            body = resp.json()
            models = body.get("models", []) or []
            chat_models = [
                m.get("name") for m in models
                if m.get("name") and not any(mk in m["name"].lower() for mk in _EMBED_MARKERS)
            ]
            # Brain's authoritative record of the model the user picked in
            # the dashboard UI (set via "Switch model" → persisted to
            # last_known_chat_model). This beats whatever is currently
            # resident in Ollama, because any client — including a stale
            # pw-agent instance with the wrong cached config — can force a
            # swap by sending /api/chat with a different model name. The
            # resident state is therefore untrustworthy; the user's UI
            # choice is the single source of truth.
            last_known = body.get("last_known_chat_model") or ""
            if last_known and any(mk in last_known.lower() for mk in _EMBED_MARKERS):
                last_known = ""

            if last_known:
                # Trust the user's explicit UI pick. Even if Ollama currently
                # has a different model loaded (possibly loaded by another
                # caller by accident), we send requests for last_known so
                # Ollama converges back to it.
                if self.model != last_known:
                    old = self.model
                    self.model = last_known
                    try:
                        import sys as _sys
                        _sys.stderr.write(f"[pw-agent] aligned to user's UI pick: {old or '(none)'} → {last_known}\n")
                        _sys.stderr.flush()
                    except Exception:
                        pass
                return self.model

            # No brain-recorded choice yet. Fall back to whatever's resident.
            # If nothing is currently resident (Ollama idle-unloaded after the
            # 5-min default), keep the cached/configured value — Ollama will
            # auto-load it on the next /api/chat call. Previously we cleared
            # self.model here and chat_stream refused to send, forcing the
            # user to bounce to the dashboard. The "read-only invariant" was
            # over-protection: any /api/chat request with a model name
            # implicitly triggers a load anyway, so guarding self.model
            # achieved nothing while creating constant friction.
            if not chat_models:
                if self.model:
                    try:
                        import sys as _sys
                        _sys.stderr.write(f"[pw-agent] no chat model resident — Ollama will load {self.model} on first request\n")
                        _sys.stderr.flush()
                    except Exception:
                        pass
                return self.model
            if self.model in chat_models:
                return self.model
            if len(chat_models) == 1:
                new_model = chat_models[0]
            else:
                sized = [(m.get("name"), m.get("size_vram") or 0) for m in models
                         if m.get("name") in chat_models]
                sized.sort(key=lambda x: -x[1])
                new_model = sized[0][0]
            old = self.model
            self.model = new_model
            try:
                import sys as _sys
                _sys.stderr.write(f"[pw-agent] realigned model: {old or '(none)'} → {new_model}\n")
                _sys.stderr.flush()
            except Exception:
                pass
            return new_model
        except Exception:
            return self.model

    def chat_stream(self, messages: list[dict], temperature: float = 0.3, context_length: int = 8192, thinking: bool = False) -> Iterator[str]:
        """Stream chat tokens from Ollama."""
        if self.direct_mode:
            # Wait for any in-flight realign probe (kicked off by
            # Agent.run() during the embed phase) up to 100ms, then fall
            # back to a synchronous probe if nothing ever ran.
            t = self._realign_thread
            if t is not None and t.is_alive():
                t.join(timeout=0.1)
            if self._last_realign_ts == 0.0:
                self._realign_model()
            # If we still have no model name after realign, the user hasn't
            # configured one and the brain has never seen one loaded — that's
            # the only case worth refusing. (Previously this also fired when
            # Ollama was idle-empty, forcing a dashboard trip on every fresh
            # session — the read-only invariant was over-protection because
            # /api/chat implicitly loads the requested model anyway. Ollama
            # auto-loads self.model on receipt; first request takes ~10s but
            # subsequent ones are warm.)
            if not self.model:
                yield ("[Error: No chat model configured. "
                       "Set one in your pw-agent config or start one from "
                       "the GPU Setup dashboard so the brain records it.]")
                return
            yield from self._stream_direct(messages, temperature, context_length, thinking=thinking)
        else:
            yield from self._stream_broker(messages, temperature, context_length, thinking=thinking)

    def _stream_direct(self, messages: list[dict], temperature: float, context_length: int, thinking: bool = False) -> Iterator[str]:
        """Stream directly from brain's Ollama endpoint."""
        model_lower = self.model.lower()
        is_gemma = "gemma" in model_lower

        # Only gemma4 reliably returns populated content via /api/chat
        # with think:<bool>. The qwen3.x family (3.5 all sizes, 3.6) all
        # hit Ollama bugs on that path — empty content, EOF mid-stream,
        # or the entire answer routed into the thinking field. Route
        # qwen3.x through /api/generate raw with <|im_start|>/<|im_end|>
        # ChatML; their reasoning emits inline as <think>...</think>
        # which agent.py's regex strips before display.
        # qwen3.x models have specific Ollama /api/chat bugs:
        # - qwen3.5 (all sizes): EOF mid-stream or answer routed to thinking field
        # - qwen3.6: empty content returned from /api/chat
        # These two families need /api/generate with raw ChatML prompt to work
        # reliably. Every other model family uses /api/chat so Ollama applies
        # the model's native template server-side. In particular:
        # - Phi / gpt-oss models use <|end|>/<|start|> tokens, NOT ChatML —
        #   sending raw ChatML to them produces garbled Phi-token output.
        # - GLM-4.x uses its own [gMASK]<sop> template — already needed /api/chat.
        # - Gemma uses <start_of_turn>/<end_of_turn> — already needed /api/chat.
        # By defaulting to /api/chat we handle all "unknown" model families
        # (Phi, Mistral, LLaMA, etc.) without needing per-family detection.
        is_qwen3x_avoid_chat = (
            model_lower.startswith("qwen3.5")
            or model_lower.startswith("qwen3.6")
        )
        is_glm = model_lower.startswith("glm")
        is_thinking_model = is_gemma  # only gemma uses think: true via /api/chat
        ask_for_thinking = bool(thinking) and is_thinking_model

        # Sampling defaults shared by both direct-brain endpoints. Ollama's
        # built-in defaults (repeat_penalty=1.1, repeat_last_n=64) are too
        # weak for larger models — glm-4.7-flash in particular falls into
        # "I apologize for..." / "I'll implement the..." repetition loops
        # without stronger penalties. top_p/top_k cap the tail so low-temp
        # sampling doesn't get locked on a single token. These match the
        # broker-path defaults that the cloud /playground/generate/async
        # route already applies server-side.
        base_options = {
            "temperature": temperature,
            "num_ctx": context_length,
            "num_predict": 4096,
            "repeat_penalty": 1.15,
            "repeat_last_n": 256,
            "top_p": 0.9,
            "top_k": 40,
        }
        # Gemma's chat template uses <end_of_turn> as the turn terminator.
        # Ollama doesn't always honour it from the modelfile, so we force it
        # via the "stop" option. Without this, Gemma keeps generating the
        # next user turn + its own reply in a loop, leaking template tokens
        # into the output stream (observed in multi-agent group chats).
        if is_gemma:
            base_options["stop"] = ["<end_of_turn>", "<start_of_turn>"]
        if is_qwen3x_avoid_chat:
            # /api/generate with raw ChatML: works around qwen3.x Ollama bugs.
            # qwen3.x reasons inline as <think>...</think> which agent.py strips.
            raw_prompt = self._flatten_messages(messages)
            payload = {
                "model": self.model,
                "prompt": raw_prompt,
                "raw": True,
                "stream": True,
                "options": base_options,
            }
            endpoint = "/api/generate"
        else:
            # /api/chat: Ollama applies the model's native template server-side.
            # Correct for GLM, Gemma, Phi/gpt-oss, Mistral, LLaMA, and any
            # other model whose template differs from ChatML. Sending raw ChatML
            # to non-ChatML models (e.g. Phi) causes garbled special-token output.
            payload = {
                "model": self.model,
                "messages": messages,
                "stream": True,
                "options": base_options,
            }
            # Only send `think` for models that honor it. Sending
            # `think: false` to non-thinking models (like glm-4.7-flash)
            # has been seen to return empty content. Omit entirely unless
            # we actually want reasoning routed into the thinking field.
            if ask_for_thinking:
                payload["think"] = True
            endpoint = "/api/chat"

        # Retry transient errors (brain restart / container bounce / brief
        # auth-cache miss after a container recycle). Brain restarts clear
        # its in-memory token cache momentarily; next request re-validates.
        import time as _time
        resp = None
        for attempt in range(3):
            try:
                resp = self.session.post(
                    f"{self.brain_url}{endpoint}",
                    json=payload,
                    stream=True,
                    timeout=300,
                )
            except requests.exceptions.ConnectionError:
                if attempt < 2:
                    _time.sleep(1.5 * (attempt + 1))
                    continue
                yield f"[Error: Could not connect to brain at {self.brain_url}]"
                return
            except requests.exceptions.Timeout:
                yield "[Error: Request timed out]"
                return
            # 401: brain auth cache just got cleared (post-restart). Sleep
            # and retry once — token is still valid, brain just needs to
            # re-verify. Same for 502/503/504 gateway bounces.
            if resp.status_code in (401, 502, 503, 504) and attempt < 2:
                try:
                    resp.close()
                except Exception:
                    pass
                _time.sleep(1.5 * (attempt + 1))
                continue
            break

        if resp is None or resp.status_code != 200:
            code = resp.status_code if resp is not None else "no response"
            yield f"[Error: Brain returned {code}]"
            return

        self._active_response = resp
        for line in resp.iter_lines():
            if not line:
                continue
            try:
                data = json.loads(line)
                # Check for thinking field
                if thinking:
                    thinking_text = data.get("message", {}).get("thinking", "")
                    if thinking_text:
                        yield f"[think]{thinking_text}[/think]"
                # /api/chat uses message.content, /api/generate uses response
                if "message" in data:
                    msg = data["message"]
                    content = msg.get("content", "")
                    # Native Ollama tool_calls — serialize into the
                    # <tool_call>{...}</tool_call> text format that the
                    # agent's parser knows about. Without this, gemma /
                    # qwen3 tool-call responses come through as empty
                    # content and pw-agent prints "Empty response".
                    tool_calls = msg.get("tool_calls") or []
                    if tool_calls and not content:
                        for tc in tool_calls:
                            fn = (tc or {}).get("function") or {}
                            name = fn.get("name", "")
                            args = fn.get("arguments", {})
                            # GLM-4.x has two broken formats we have to unwrap:
                            #
                            # 1. JSON stuffed into name:
                            #      name = '{"tool":"write_file","args":{...}}'
                            #      args = {}
                            #
                            # 2. Python function-call syntax split across
                            #    name + args:
                            #      name = 'write_file(path="docs/smoke/README.md",'
                            #      args = {'content="..."': ''}
                            #    (Ollama greedily captures identifier + first
                            #    arg into `name`, then stuffs each remaining
                            #    kwarg into `arguments` as a bare-string key.)
                            #
                            # Without recovery pw-agent sees name as a 100-char
                            # "Unknown tool" string, emits an error tool_result,
                            # and the model bails with an empty retry — exact
                            # failure mode that left a callbyte task with only
                            # write_file run and nothing committed.
                            raw_name_for_log = name
                            if isinstance(name, str) and name.lstrip().startswith("{"):
                                try:
                                    parsed = json.loads(name)
                                    if isinstance(parsed, dict) and "tool" in parsed:
                                        name = parsed.get("tool", "")
                                        args = parsed.get("args", args) or args
                                except json.JSONDecodeError:
                                    pass
                            elif isinstance(name, str) and "(" in name:
                                # Python function-call syntax. Pull the bare
                                # identifier out as the real tool name; merge
                                # any partial first-arg back into args.
                                import re as _re
                                m = _re.match(r'\s*([A-Za-z_][A-Za-z0-9_]*)\s*\((.*)$', name, _re.DOTALL)
                                if m:
                                    real_name = m.group(1)
                                    rest = m.group(2).rstrip(",").strip()
                                    recovered_args = {}
                                    # First-arg fragment from the name tail
                                    first = _re.match(r'([A-Za-z_][A-Za-z0-9_]*)\s*=\s*"((?:[^"\\]|\\.)*)"', rest, _re.DOTALL)
                                    if first:
                                        try:
                                            recovered_args[first.group(1)] = json.loads('"' + first.group(2) + '"')
                                        except Exception:
                                            recovered_args[first.group(1)] = first.group(2)
                                    # Remaining kwargs landed in args as bare-string keys.
                                    if isinstance(args, dict):
                                        for k, v in args.items():
                                            if isinstance(k, str) and "=" in k:
                                                kk, _, vv = k.partition("=")
                                                kk = kk.strip()
                                                vv = vv.strip().rstrip(")").rstrip(",").strip()
                                                if vv.startswith('"') and vv.endswith('"'):
                                                    try:
                                                        recovered_args[kk] = json.loads(vv)
                                                    except Exception:
                                                        recovered_args[kk] = vv[1:-1]
                                                else:
                                                    recovered_args[kk] = vv
                                            elif isinstance(k, str) and k:
                                                recovered_args[k] = v
                                    name = real_name
                                    args = recovered_args
                                    if os.environ.get("PW_DEBUG"):
                                        import sys as _sys
                                        _sys.stderr.write(f"[pw-agent] recovered glm pycall-syntax tool_call: raw={raw_name_for_log[:80]!r} → tool={name!r}\n")
                            if isinstance(args, str):
                                try:
                                    args = json.loads(args)
                                except Exception:
                                    args = {"_raw": args}
                            # Variant 3: name was salvaged (e.g. "write_file")
                            # but Ollama crammed the ENTIRE arg list into a
                            # single bare-string key of `arguments`:
                            #   args = {'"docs/smoke/README.md", content: "..."': ''}
                            # This is glm emitting mixed positional + named
                            # args: write_file("docs/smoke/README.md", content: "...").
                            # Tokenise the bare key back into a proper dict,
                            # mapping leading positional arg to the tool's
                            # first parameter (path for file tools, command
                            # for bash). Without this the tool dispatch sees
                            # args={} and write_file fails "missing path".
                            if (isinstance(args, dict) and len(args) == 1
                                and isinstance(name, str) and name):
                                only_key = next(iter(args.keys()))
                                if (isinstance(only_key, str)
                                    and ("=" in only_key or ":" in only_key or '"' in only_key)
                                    and not only_key.startswith("_")):
                                    import re as _re2
                                    recovered = {}
                                    rest = only_key.strip()
                                    # Leading positional quoted arg
                                    pos = _re2.match(r'^\s*"((?:[^"\\]|\\.)*)"\s*(?:,|$)', rest, _re2.DOTALL)
                                    if pos:
                                        try:
                                            first_positional = json.loads('"' + pos.group(1) + '"')
                                        except Exception:
                                            first_positional = pos.group(1)
                                        # Map to tool's first param by name convention
                                        first_param = {
                                            "bash": "command",
                                            "grep": "pattern",
                                            "list_files": "path",
                                        }.get(name, "path")
                                        recovered[first_param] = first_positional
                                        rest = rest[pos.end():]
                                    # Remaining `key: "value"` or `key="value"` pairs
                                    for m in _re2.finditer(
                                        r'([A-Za-z_][A-Za-z0-9_]*)\s*[:=]\s*"((?:[^"\\]|\\.)*)"',
                                        rest, _re2.DOTALL
                                    ):
                                        try:
                                            recovered[m.group(1)] = json.loads('"' + m.group(2) + '"')
                                        except Exception:
                                            recovered[m.group(1)] = m.group(2)
                                    if recovered:
                                        args = recovered
                                        if os.environ.get("PW_DEBUG"):
                                            import sys as _sys
                                            _sys.stderr.write(f"[pw-agent] recovered glm single-key-args: tool={name!r} keys={list(recovered)}\n")
                            # pw-agent's parser (_parse_tool_call in agent.py)
                                # expects {"tool": ..., "args": ...} — NOT the
                                # OpenAI {"name": ..., "arguments": ...} format.
                                # Emitting the wrong shape made _normalize_tool_call
                                # return the raw dict with no "tool" key, parser
                                # failed, and the model's text got treated as a
                                # final answer with zero tool_use events.
                            payload_text = json.dumps({"tool": name, "args": args})
                            content = f"<tool_call>{payload_text}</tool_call>"
                else:
                    content = data.get("response", "")
                if content:
                    yield content
                if data.get("done"):
                    return
            except json.JSONDecodeError:
                continue

    def _flatten_messages(self, messages: list[dict]) -> str:
        """Flatten chat messages into a prompt string using the model's native template.

        Different model families use different chat templates:
        - Qwen/DeepSeek: ChatML (<|im_start|>role\ncontent<|im_end|>)
        - Gemma: <start_of_turn>role\ncontent<end_of_turn>
        - Llama: [INST] content [/INST]
        """
        model_lower = self.model.lower()

        # Ollama ChatML / Gemma templates only recognise three roles:
        # system, user, assistant. Custom roles we add to conversation
        # (notably "tool_result") pass through as `<|im_start|>tool_result`
        # which the model can't parse — seen in the wild as "I don't see
        # previous task context" when a tool_result was in history.
        # Normalise every non-standard role to "user" so the model sees
        # tool output / hook context as continued user turns.
        def _norm(role: str) -> str:
            if role in ("system", "user", "assistant"):
                return role
            return "user"

        if "gemma" in model_lower:
            # Gemma format
            parts = []
            for msg in messages:
                role = _norm(msg.get("role", "user"))
                content = msg.get("content", "")
                # Gemma uses "user" and "model" (not "assistant")
                gemma_role = "model" if role == "assistant" else role
                if role == "system":
                    # Gemma has no system role — prepend to first user message
                    parts.append(f"<start_of_turn>user\n{content}<end_of_turn>")
                else:
                    parts.append(f"<start_of_turn>{gemma_role}\n{content}<end_of_turn>")
            parts.append("<start_of_turn>model\n")
            return "\n".join(parts)
        else:
            # ChatML format (Qwen, DeepSeek, most Ollama models)
            parts = []
            for msg in messages:
                role = _norm(msg.get("role", "user"))
                content = msg.get("content", "")
                parts.append(f"<|im_start|>{role}\n{content}<|im_end|>")
            parts.append("<|im_start|>assistant\n")
            return "\n".join(parts)

    def _stream_broker(self, messages: list[dict], temperature: float, context_length: int, thinking: bool = False) -> Iterator[str]:
        """Submit task asynchronously and poll for completion to avoid EOF/timeouts."""
        import time

        payload = {
            "model": "llm-chat",
            "slot": self.slot,
            "messages": messages,
            "llm_model": self.model,
            "temperature": temperature,
            "max_tokens": 4096,
            "context_length": context_length,
        }
        # Only include the `thinking` field when the model can honor it
        # RELIABLY via the broker path's /api/chat + stream:false call.
        # Models omitted because the broker path blows up:
        #   - qwen2.5 / qwen3-coder  → Ollama: "does not support thinking"
        #   - qwen3.5 (all sizes)    → EOF mid-response on think:true via
        #                              /api/chat + stream:false
        #   - qwen3.6                → empty content on /api/chat thinking
        # Only gemma4 handles it cleanly. For everyone else, let the brain
        # default to its raw-prompt /api/generate path which avoids the
        # Ollama /api/chat bugs entirely.
        model_lower = self.model.lower()
        model_supports_think = "gemma" in model_lower
        if model_supports_think:
            payload["thinking"] = thinking

        # 1. Submit the task asynchronously (with retry on transient errors)
        task_id = None
        max_retries = 3
        for attempt in range(max_retries):
            try:
                resp = self.session.post(
                    f"{self.api_url}/api/v1/playground/generate/async",
                    json=payload,
                    timeout=30,
                )
                if resp.status_code in (200, 202):
                    data = resp.json()
                    if data.get("success"):
                        task_id = data.get("task_id")
                        break
                    err = data.get("error", "")
                    # Retryable: slot resolution failures, device offline
                    if attempt < max_retries - 1 and ("resolve device" in err or "offline" in err):
                        time.sleep(2 * (attempt + 1))
                        continue
                    yield f"[Error: {err}]"
                    return
                elif resp.status_code in (502, 503, 504):
                    # Gateway errors — retry
                    if attempt < max_retries - 1:
                        time.sleep(2 * (attempt + 1))
                        continue
                    yield f"[Error: API returned {resp.status_code} after {max_retries} retries]"
                    return
                elif resp.status_code == 400:
                    # Broker returns 400 when it can't resolve the slot→device
                    # link (Redis cache briefly empty during container
                    # re-registration) or when the device is marked offline.
                    # The brain's 30s heartbeat repopulates the slot_link, so
                    # a short retry usually succeeds without user action.
                    try:
                        err = resp.json().get("error", "")
                    except Exception:
                        err = resp.text[:200]
                    if attempt < max_retries - 1 and ("resolve device" in err or "offline" in err):
                        time.sleep(2 * (attempt + 1))
                        continue
                    yield f"[Error: API returned 400: {err}]"
                    return
                else:
                    yield f"[Error: API returned {resp.status_code}: {resp.text[:200]}]"
                    return
            except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
                if attempt < max_retries - 1:
                    time.sleep(2 * (attempt + 1))
                    continue
                yield f"[Error: Connection failed after {max_retries} retries]"
                return
            except Exception as e:
                yield f"[Error: {str(e)}]"
                return

        if not task_id:
            yield "[Error: No task_id returned from broker]"
            return

        # 2. Poll for result
        # Most LLM tasks take 5-60s. We'll poll every 1-2s.
        max_wait = 300 # 5 minutes
        start_time = time.time()

        # Add a subtle indicator that we are polling
        import sys

        while time.time() - start_time < max_wait:
            try:
                # Use a fresh request for polling to avoid session stickiness issues
                poll_resp = self.session.get(
                    f"{self.api_url}/api/v1/playground/tasks/{task_id}",
                    timeout=10
                )
                if poll_resp.status_code == 200:
                    poll_data = poll_resp.json()
                    status = poll_data.get("status")

                    if status == "completed":
                        result = poll_data.get("result", {})
                        # Yield thinking content first (if present)
                        thinking_text = result.get("thinking", "")
                        if thinking_text:
                            yield f"[think]{thinking_text}[/think]"
                        text = result.get("text", "") or result.get("response", "") or ""
                        if not text and os.environ.get("PW_DEBUG"):
                            import sys
                            sys.stderr.write(f"DEBUG poll result: {str(result)[:300]}\n")
                        yield text
                        return

                    if status == "failed":
                        err = poll_data.get("error", "Generation failed")
                        if os.environ.get("PW_DEBUG"):
                            import sys
                            sys.stderr.write(f"DEBUG task failed: {err}\n")
                            sys.stderr.write(f"DEBUG full: {str(poll_data)[:500]}\n")
                        yield f"[Error: {err}]"
                        return

                elif poll_resp.status_code in (502, 503, 504):
                    # Gateway / service-unavailable during poll — most often
                    # Cloud Run bouncing the broker instance (liveness probe
                    # timeout → restart → new instance, ~5-10s gap). The task
                    # is still in Redis/PubSub, just the poll endpoint is
                    # momentarily down. Keep polling silently; only bail if
                    # the outer max_wait timer expires.
                    pass
                elif poll_resp.status_code != 404:
                    # Other 4xx/5xx — real failure, not transient. Report.
                    try:
                        err_data = poll_resp.json()
                        err_msg = err_data.get("error", f"Status {poll_resp.status_code}")
                    except:
                        err_msg = f"Status {poll_resp.status_code}"
                    yield f"[Error: Polling failed: {err_msg}]"
                    return

            except Exception:
                pass # Continue polling on transient network errors

            time.sleep(1.5)

        yield "[Error: Task timed out after 5 minutes]"

    def list_devices(self) -> list:
        """List online GPU devices with running LLM."""
        if self.direct_mode:
            # Enrich the stub with real brain /status data when reachable so
            # /models can show GPU name + VRAM. Falls back to placeholders if
            # the brain is offline or auth fails.
            device_name = "local"
            gpu_name = "direct"
            vram_gb = 0.0
            try:
                ctrl_headers = {}
                if self.token:
                    ctrl_headers["Authorization"] = f"Bearer {self.token}"
                    ctrl_headers["X-Controller-API-Key"] = self.token
                sr = self.session.get(f"{self.brain_url}/status", headers=ctrl_headers, timeout=3)
                if sr.status_code == 200:
                    sd = sr.json()
                    device_name = sd.get("device_name") or device_name
                    gi = sd.get("gpu_info") or {}
                    gpu_name = gi.get("name") or gpu_name
                    vram_gb = round((gi.get("memory_total_mb") or 0) / 1024, 1)
            except Exception:
                pass
            return [{
                "slot": 0,
                "device_id": "local",
                "device_name": device_name,
                "gpu": gpu_name,
                "vram_gb": vram_gb,
                "llm_model": self.model,
            }]

        try:
            resp = self.session.get(f"{self.api_url}/api/user/byog/slots", timeout=15)
            if resp.status_code != 200:
                return []
            data = resp.json()
            if not data.get("success"):
                return []

            devices = []
            for s in data.get("slots", []):
                if not s.get("online"):
                    continue
                running = s.get("running_services", [])
                if "llm" in running:
                    devices.append({
                        "slot": s.get("slot_number"),
                        "device_id": s.get("device_id", ""),
                        "device_name": s.get("device_name", "Unknown"),
                        "gpu": s.get("gpu_info", {}).get("name", "Unknown"),
                        "vram_gb": round(s.get("gpu_info", {}).get("memory_total_mb", 0) / 1024, 1),
                        "llm_model": s.get("llm_current_model") or "ollama",
                    })
            return devices
        except Exception:
            return []

    def test_connection(self) -> tuple[bool, str]:
        """Test connectivity and return (ok, message)."""
        if self.direct_mode:
            try:
                resp = self.session.get(f"{self.brain_url}/api/tags", timeout=10)
                if resp.status_code != 200:
                    return False, f"Brain returned {resp.status_code}"
                data = resp.json()
                models = [m["name"] for m in data.get("models", [])]
                if self.model and self.model not in models:
                    available = ", ".join(models[:5]) or "none"
                    return False, f"Model '{self.model}' not found. Available: {available}"
                return True, f"Connected to brain at {self.brain_url} ({self.model})"
            except requests.exceptions.ConnectionError:
                return False, f"Could not connect to {self.brain_url}"
            except Exception as e:
                return False, str(e)

        # Cloud mode — find our slot
        try:
            resp = self.session.get(f"{self.api_url}/api/user/byog/slots", timeout=15)
            if resp.status_code == 401:
                return False, "Invalid API token"
            if resp.status_code != 200:
                return False, f"API error: {resp.status_code}"

            data = resp.json()
            if not data.get("success"):
                return False, data.get("error", "API error")

            for s in data.get("slots", []):
                if s.get("slot_number") == self.slot:
                    if not s.get("online"):
                        return False, f"Slot {self.slot} is offline"
                    if "llm" not in s.get("running_services", []):
                        return False, f"Slot {self.slot} has no LLM running"
                    gpu = s.get("gpu_info", {}).get("name", "unknown")
                    model = s.get("llm_current_model") or self.model or "ollama"
                    return True, f"Connected to {model} on {gpu} (slot {self.slot})"

            return False, f"Slot {self.slot} not found"
        except requests.exceptions.ConnectionError:
            return False, f"Could not connect to {self.api_url}"
        except Exception as e:
            return False, str(e)
