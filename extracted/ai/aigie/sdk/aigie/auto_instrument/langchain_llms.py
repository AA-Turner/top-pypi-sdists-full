"""Auto-instrumentation for LangChain chat-model classes.

Patches the ``invoke``/``ainvoke`` of each LangChain chat model in
``_LANGCHAIN_LLM_TARGETS`` so a model used outside a traced chain still produces a span.

Split out of ``llm.py`` unchanged: that file was over the 500-line policy, and the
Gemini work had to touch it. This block was the largest self-contained unit in it, so
moving it is what buys the rest of the file room to be edited at all.
"""

from __future__ import annotations

import contextlib
import functools
from typing import Any

from aigie.auto_instrument.llm import _is_aigie_callback, _patched_modules, logger

# (module, class, canonical provider). Imported lazily; missing packages are skipped.
_LANGCHAIN_LLM_TARGETS = [
    # --- Tier 1: Most common providers ---
    ("langchain_openai", "ChatOpenAI", "openai"),
    ("langchain_anthropic", "ChatAnthropic", "anthropic"),
    ("langchain_google_genai", "ChatGoogleGenerativeAI", "gemini"),
    # --- AWS Bedrock ---
    ("langchain_aws", "ChatBedrock", "bedrock"),
    ("langchain_aws", "ChatBedrockConverse", "bedrock"),
    # --- Groq ---
    ("langchain_groq", "ChatGroq", "groq"),
    # --- Mistral ---
    ("langchain_mistralai", "ChatMistralAI", "mistral"),
    # --- Cohere ---
    ("langchain_cohere", "ChatCohere", "cohere"),
    # --- Fireworks ---
    ("langchain_fireworks", "ChatFireworks", "fireworks"),
    # --- Together AI ---
    ("langchain_together", "ChatTogether", "together"),
    # --- NVIDIA NIM ---
    ("langchain_nvidia_ai_endpoints", "ChatNVIDIA", "nvidia"),
    # --- AI21 ---
    ("langchain_ai21", "ChatAI21", "ai21"),
    # --- DeepSeek (via openai-compatible or dedicated package) ---
    ("langchain_deepseek", "ChatDeepSeek", "deepseek"),
    # --- Ollama (local models) ---
    ("langchain_ollama", "ChatOllama", "ollama"),
    # --- Azure OpenAI ---
    ("langchain_openai", "AzureChatOpenAI", "azure_openai"),
    # --- Google Vertex AI ---
    ("langchain_google_vertexai", "ChatVertexAI", "vertex_ai"),
    # --- Hugging Face ---
    ("langchain_huggingface", "ChatHuggingFace", "huggingface"),
    # --- xAI (Grok) ---
    ("langchain_xai", "ChatXAI", "xai"),
    # --- Cerebras ---
    ("langchain_cerebras", "ChatCerebras", "cerebras"),
    # --- Sambanova ---
    ("langchain_sambanova", "ChatSambaNovaCloud", "sambanova"),
]


def _patch_langchain_llms() -> None:
    """Patch LangChain LLM classes to auto-inject callbacks.

    Covers all major LLM providers to ensure interception and tracing
    work regardless of which provider the customer uses — including
    fallback chains (e.g. Bedrock → Groq).
    """
    patched_count = 0
    for module_path, class_name, provider in _LANGCHAIN_LLM_TARGETS:
        try:
            module = __import__(module_path, fromlist=[class_name])
            llm_class = getattr(module, class_name, None)
            if llm_class is None:
                continue
            if llm_class in _patched_modules:
                continue
            _patch_langchain_llm_class(llm_class, provider)
            _patched_modules.add(llm_class)
            patched_count += 1
        except ImportError:
            pass  # Provider package not installed — skip silently
        except Exception as e:
            logger.debug(f"Failed to patch {module_path}.{class_name}: {e}")

    if patched_count:
        logger.debug(f"Patched {patched_count} LangChain LLM classes for auto-instrumentation")


def _patch_langchain_llm_class(llm_class: Any, provider: str) -> None:
    """Patch a LangChain LLM class to auto-inject callbacks and interception hooks.

    This provides full auto-instrumentation:
    1. Pre-call interception (blocking, validation)
    2. Tracing (spans, metrics)
    3. Post-call interception (quality checks, recommendations)
    """
    original_ainvoke = getattr(llm_class, "ainvoke", None)
    original_invoke = getattr(llm_class, "invoke", None)

    def _convert_messages_to_dict(messages) -> list:
        """Convert LangChain messages to dict format for interception."""
        if isinstance(messages, str):
            return [{"role": "user", "content": messages}]
        if hasattr(messages, "to_messages"):
            messages = messages.to_messages()
        elif not isinstance(messages, (list, tuple)):
            messages = [messages]

        messages_dict = []
        for msg in messages:
            if hasattr(msg, "type"):
                role = msg.type
            elif hasattr(msg, "__class__"):
                role = msg.__class__.__name__.replace("Message", "").lower()
            else:
                role = "user"
            content = msg.content if hasattr(msg, "content") else str(msg)
            messages_dict.append({"role": role, "content": content})
        return messages_dict

    if original_ainvoke:

        @functools.wraps(original_ainvoke)
        async def traced_ainvoke(self, messages, config=None, **kwargs):
            """Intercepted version of LLM ainvoke.

            Automatically runs pre/post-call interception hooks.
            Tracing is handled by LangChain's callback mechanism.
            """
            from aigie.client import get_aigie

            aigie = get_aigie()

            # Recursion guard: skip instrumentation if already inside an LLM wrapper
            from aigie.auto_instrument.trace import (
                is_in_llm_instrumentation,
                set_llm_instrumentation,
            )

            if is_in_llm_instrumentation():
                return await original_ainvoke(self, messages, config=config, **kwargs)

            set_llm_instrumentation(True)
            try:
                model_name = getattr(self, "model_name", None) or getattr(self, "model", "unknown")

                # Convert messages for interception
                messages_dict = _convert_messages_to_dict(messages)

                # Tracing: check if AigieCallbackHandler is present in config.
                # If callbacks handle tracing, we skip span creation here to avoid duplicates.
                # If no callbacks, we create a span so the LLM call is visible on the platform.
                _has_aigie_callback = False
                _fallback_span = None
                if config and isinstance(config, dict):
                    callbacks = config.get("callbacks")
                    if callbacks is not None:
                        # callbacks may be a list or an AsyncCallbackManager/CallbackManager
                        if isinstance(callbacks, list):
                            cb_list = callbacks
                        else:
                            cb_list = list(getattr(callbacks, "handlers", []))
                            cb_list += list(getattr(callbacks, "inheritable_handlers", []))
                        for cb in cb_list:
                            if _is_aigie_callback(cb):
                                _has_aigie_callback = True
                                break
                # Also skip fallback span when callback context is active (LangGraph/LangChain
                # callbacks handle tracing even if not visible in this config dict)
                from aigie.auto_instrument.trace import is_in_callback_context

                if (
                    not _has_aigie_callback
                    and not is_in_callback_context()
                    and aigie
                    and aigie._initialized
                ):
                    try:
                        from aigie.auto_instrument.trace import get_or_create_trace

                        trace = await get_or_create_trace(
                            name=f"LLM Call: {provider}",
                            metadata={"provider": provider, "type": "llm"},
                        )
                        if trace:
                            _fallback_span = trace.span(
                                f"LLM: {provider} - {model_name}", type="llm"
                            )
                            await _fallback_span.__aenter__()
                            _fallback_span.set_input(
                                {
                                    "provider": provider,
                                    "model": model_name,
                                    "messages": messages_dict[:5],
                                }
                            )
                    except Exception as e:
                        logger.debug(f"Fallback span creation error (continuing): {e}")

                # Make the actual LLM call.
                last_response = await original_ainvoke(self, messages, config=config, **kwargs)

                # Close fallback span on success
                if _fallback_span:
                    try:
                        response_content = (
                            last_response.content
                            if hasattr(last_response, "content")
                            else str(last_response)[:500]
                        )
                        _fallback_span.set_output(
                            {
                                "provider": provider,
                                "model": model_name,
                                "content": response_content[:500],
                            }
                        )
                        await _fallback_span.__aexit__(None, None, None)
                    except Exception as e:
                        logger.debug(f"Fallback span close error: {e}")

                return last_response
            except Exception as exc:
                # Close fallback span on error
                if _fallback_span:
                    try:
                        _fallback_span.set_output(
                            {
                                "error": str(exc),
                                "error_type": type(exc).__name__,
                                "provider": provider,
                                "model": model_name,
                            }
                        )
                        await _fallback_span.__aexit__(type(exc), exc, exc.__traceback__)
                    except Exception:
                        pass
                raise
            finally:
                set_llm_instrumentation(False)

        llm_class.ainvoke = traced_ainvoke

    if original_invoke:

        @functools.wraps(original_invoke)
        def traced_invoke(self, messages, config=None, **kwargs):
            """Intercepted version of LLM invoke (sync).

            Automatically runs pre/post-call interception hooks.
            Tracing is handled by LangChain's callback mechanism.
            """
            from aigie.client import get_aigie

            aigie = get_aigie()

            from aigie.auto_instrument.trace import (
                is_in_llm_instrumentation,
                set_llm_instrumentation,
            )

            if is_in_llm_instrumentation():
                return original_invoke(self, messages, config=config, **kwargs)

            set_llm_instrumentation(True)
            try:
                model_name = getattr(self, "model_name", None) or getattr(self, "model", "unknown")

                # Convert messages for interception
                messages_dict = _convert_messages_to_dict(messages)

                # Tracing: check if AigieCallbackHandler is present in config.
                _has_aigie_callback = False
                _fallback_span = None
                if config and isinstance(config, dict):
                    callbacks = config.get("callbacks")
                    if callbacks is not None:
                        # callbacks can be a list, AsyncCallbackManager, or CallbackManager
                        cb_list = (
                            callbacks
                            if isinstance(callbacks, list)
                            else getattr(callbacks, "handlers", [])
                        )
                        for cb in cb_list:
                            if _is_aigie_callback(cb):
                                _has_aigie_callback = True
                                break
                # Also skip fallback span when callback context is active (LangGraph/LangChain
                # callbacks handle tracing even if not visible in this config dict)
                from aigie.auto_instrument.trace import is_in_callback_context

                if (
                    not _has_aigie_callback
                    and not is_in_callback_context()
                    and aigie
                    and aigie._initialized
                ):
                    try:
                        from aigie.auto_instrument.trace import get_or_create_trace_sync

                        trace = get_or_create_trace_sync(
                            name=f"LLM Call: {provider}",
                            metadata={"provider": provider, "type": "llm"},
                        )
                        if trace:
                            _fallback_span = trace.span(
                                f"LLM: {provider} - {model_name}", type="llm"
                            )
                            _fallback_span.set_input(
                                {
                                    "provider": provider,
                                    "model": model_name,
                                    "messages": messages_dict[:5],
                                }
                            )
                    except Exception as e:
                        logger.debug(f"Fallback span creation error (continuing): {e}")

                # Make the actual LLM call.
                response = original_invoke(self, messages, config=config, **kwargs)

                # Close fallback span on success
                if _fallback_span:
                    try:
                        response_content = (
                            response.content
                            if hasattr(response, "content")
                            else str(response)[:500]
                        )
                        _fallback_span.set_output(
                            {
                                "provider": provider,
                                "model": model_name,
                                "content": response_content[:500],
                            }
                        )
                    except Exception as e:
                        logger.debug(f"Fallback span close error: {e}")

                return response
            except Exception as exc:
                # Close fallback span on error
                if _fallback_span:
                    with contextlib.suppress(Exception):
                        _fallback_span.set_output(
                            {
                                "error": str(exc),
                                "error_type": type(exc).__name__,
                                "provider": provider,
                                "model": model_name,
                            }
                        )
                raise
            finally:
                set_llm_instrumentation(False)

        llm_class.invoke = traced_invoke
