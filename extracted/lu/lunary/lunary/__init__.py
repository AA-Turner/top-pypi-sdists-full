import os
import logging
import json
import asyncio
from collections.abc import Iterable, Iterator, Mapping

logger = logging.getLogger(__name__)
logger.setLevel(logging.WARNING)

if os.getenv("LUNARY_VERBOSE") == "True" or os.getenv("LUNARY_VERBOSE") == "true":
    # TODO: later, allow the user to keep the global handlers in verbose mode
    # TODO: the verbose mode should be taken from config, and be dynamic if config changes
    handler = logging.StreamHandler()
    handler.setLevel(logging.DEBUG)
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)
    logger.propagate = False # Avoid the global logging config to prevent verbose logs to be logged

from inspect import signature, isawaitable
import traceback, copy, time, chevron, aiohttp, copy
from functools import wraps


from packaging import version
from importlib.metadata import PackageNotFoundError
from contextvars import ContextVar
from datetime import datetime, timezone
from typing import Optional, Any, Callable, Union, Dict
import jsonpickle
from pydantic import BaseModel
import humps

from .exceptions import *
from .parsers import (
    PydanticHandler,
    default_input_parser,
    default_output_parser,
    filter_params,
    is_openai_omitted,
    method_input_parser,
)
from .openai_utils import (
    OpenAIChatStreamAccumulator,
    OpenAIResponsesStreamAccumulator,
    OpenAIResponsesUtils,
    OpenAIUtils,
)
from .anthropic_utils import AnthropicUtils
from .ibm_utils import IBMUtils
from .event_queue import EventQueue
from .thread import Thread
from .utils import clean_nones, create_uuid_from_string
from .config import get_config, set_config
from .run_manager import RunManager

from .users import (
    user_ctx,
    user_props_ctx,
    identify,
)  # DO NOT REMOVE `identify` import
from .tags import tags_ctx, tags  # DO NOT REMOVE `tags` import
from .parent import parent_ctx, parent # DO NOT REMOVE `parent` import
from .project import project_ctx  # DO NOT REMOVE `project` import



event_queue_ctx = ContextVar("event_queue_ctx")
event_queue_ctx.set(EventQueue())
queue = event_queue_ctx.get()

run_manager = RunManager()

from contextvars import ContextVar

class LunaryException(Exception):
    pass

jsonpickle.handlers.register(BaseModel, PydanticHandler, base=True)

def config(
    app_id: str | None = None,
    verbose: str | None = None,
    api_url: str | None = None,
    disable_ssl_verify: bool | None = None,
    ssl_verify: bool | str | None = None,
):
    set_config(app_id, verbose, api_url, disable_ssl_verify, ssl_verify)


def get_parent_run_id(parent_run_id: str, run_type: str, app_id: str, run_id: str):
    if parent_run_id == "None":
        parent_run_id = None

    parent_from_ctx = parent_ctx.get().get("message_id") if parent_ctx.get() else None
    if not parent_run_id and parent_from_ctx and run_type != "thread":
        return str(create_uuid_from_string(str(parent_from_ctx) + str(app_id)))

    if parent_run_id:
        return str(create_uuid_from_string(str(parent_run_id) + str(app_id)))

    if parent_run_id is not None:
        return str(create_uuid_from_string(str(parent_run_id) + str(app_id)))


def track_event(
    run_type,
    event_name,
    run_id: str,
    parent_run_id=None,
    name=None,
    input=None,
    output=None,
    message=None,
    error=None,
    token_usage=None,
    user_id=None,
    user_props=None,
    tags=None,
    timestamp=None,
    thread_tags=None,
    feedback=None,
    template_id=None,
    metadata=None,
    params=None,
    runtime=None,
    app_id=None, 
    api_url=None,
    callback_queue=None,
    thread_metadata=None
):
    try:
        config = get_config()
        custom_app_id = app_id
        project_id = app_id or config.app_id # used to generate a unique run_id 
        api_url = api_url or config.api_url


        parent_run_id = get_parent_run_id(
            parent_run_id, run_type, app_id=project_id, run_id=run_id
        )
        # We need to generate a UUID that is unique by run_id / project_id pair in case of multiple concurrent callback handler use
        run_id = str(create_uuid_from_string(str(run_id) + str(project_id)))

        event = {
            "event": event_name,
            "type": run_type,
            "name": name,
            "userId": user_id or user_ctx.get(),
            "userProps": user_props or user_props_ctx.get(),
            "tags": tags or tags_ctx.get(),
            "threadTags": thread_tags,
            "runId": run_id,
            "parentRunId": parent_run_id,
            "timestamp": timestamp or datetime.now(timezone.utc).isoformat(),
            "message": message,
            "input": input,
            "output": output,
            "error": error,
            "feedback": feedback,
            "runtime": runtime or "lunary-py",
            "tokensUsage": token_usage,
            "metadata": metadata,
            "params": params,
            "templateId": template_id,
            "appId": custom_app_id, # should only be set when a custom app_id is provided, otherwise the app_id is set in consumer.py 
            "threadMetadata": thread_metadata
        }

        if callback_queue is not None:
            callback_queue.append(event)
        else:
            queue.append(event)

        if config.verbose:
            try:
                serialized_event = jsonpickle.encode(clean_nones(event), unpicklable=False, indent=4)
                logger.debug(f"\nAdd event: {serialized_event}\n")
            except Exception as e:
                logger.exception(f"Could not serialize event: {event}")


    except Exception as e:
        logger.exception("Error in `track_event`")


class _TrackedOpenAISyncStream:
    def __init__(
        self,
        stream,
        accumulator,
        run_id,
        name,
        type,
        add_item,
        is_completed,
        error_for_outcome,
        has_authoritative_outcome=None,
        terminal_claim=None,
    ):
        self._stream = stream
        self._accumulator = accumulator
        self._run_id = run_id
        self._name = name
        self._type = type
        self._add_item = add_item
        self._is_completed = is_completed
        self._error_for_outcome = error_for_outcome
        self._has_authoritative_outcome = (
            has_authoritative_outcome or (lambda: False)
        )
        self._finalized = False
        self._terminal_emitted = False
        self._provider_errors_delegated = False
        self._provider_operation_active = False
        self._terminal_claim = terminal_claim or (lambda: True)

    @property
    def response(self):
        return getattr(self._stream, "response")

    def __iter__(self):
        return self

    def __next__(self):
        if self._finalized:
            raise StopIteration
        self._provider_operation_active = True
        try:
            item = next(self._stream)
            self._add_item(item)
            return item
        except StopIteration:
            self._finalize(eof=True)
            raise
        except BaseException:
            self._finalize_provider_failure(eof=False)
            raise
        finally:
            self._provider_operation_active = False

    def _close_provider(self):
        close = getattr(self._stream, "close", None)
        if callable(close):
            self._provider_operation_active = True
            try:
                return close()
            finally:
                self._provider_operation_active = False
        return None

    def delegate_provider_errors(self):
        self._provider_errors_delegated = True

    def _emit_outcome(self, *, eof):
        if self._terminal_emitted:
            return
        self._terminal_emitted = True
        self._finalized = True
        if not self._terminal_claim():
            return
        if self._is_completed():
            track_event(
                self._type,
                "end",
                self._run_id,
                name=self._name,
                output=self._accumulator.output(),
                token_usage=self._accumulator.token_usage(),
            )
            return
        track_event(
            self._type,
            "error",
            self._run_id,
            name=self._name,
            output=self._accumulator.output(),
            token_usage=self._accumulator.token_usage(),
            error=self._error_for_outcome(eof=eof),
        )

    def _emit_provider_failure(self, *, eof):
        if self._has_authoritative_outcome():
            self._emit_outcome(eof=eof)
            return
        self._finalized = True
        if self._terminal_emitted or self._provider_errors_delegated:
            return
        self._terminal_emitted = True
        if not self._terminal_claim():
            return
        track_event(
            self._type,
            "error",
            self._run_id,
            name=self._name,
            error=_openai_provider_stream_error(),
        )

    def _finalize_provider_failure(self, *, eof):
        if self._finalized:
            return
        self._finalized = True
        try:
            self._close_provider()
        except BaseException:
            logger.exception("Error closing OpenAI stream after failure")
        self._emit_provider_failure(eof=eof)

    def _finalize(self, *, eof):
        if self._finalized:
            return
        self._finalized = True
        try:
            self._close_provider()
        except BaseException:
            self._emit_provider_failure(eof=eof)
            raise
        self._emit_outcome(eof=eof)

    def close(self):
        return self._finalize(eof=False)

    def __enter__(self):
        return self

    def __exit__(self, _exc_type, _exc, _exc_tb):
        if _exc_type is None:
            self.close()
            return False
        if self._finalized:
            return False
        try:
            self.close()
        except BaseException:
            logger.exception(
                "Error closing OpenAI stream while propagating an exception"
            )
        return False

    def __getattr__(self, key):
        return getattr(self._stream, key)


def _chat_stream_error(accumulator, *, eof):
    return {
        "code": "chat_stream_incomplete" if eof else "stream_cancelled",
        "message": (
            "OpenAI Chat Completions stream ended without finish_reason"
            if eof
            else "OpenAI Chat Completions stream closed before completion"
        ),
    }


def _openai_provider_stream_error():
    return {
        "code": "provider_stream_error",
        "message": "OpenAI provider stream failed",
    }


def default_stream_handler(fn, run_id, name, type, *args, **kwargs):
    stream = fn(*args, **kwargs)
    accumulator = OpenAIChatStreamAccumulator(kwargs.get("n", 1))
    return _TrackedOpenAISyncStream(
        stream,
        accumulator,
        run_id,
        name,
        type,
        accumulator.add_chunk,
        accumulator.has_terminal_choice_state,
        lambda *, eof: _chat_stream_error(accumulator, eof=eof),
    )


def openai_responses_stream_handler(fn, run_id, name, type, *args, **kwargs):
    stream = fn(*args, **kwargs)
    accumulator = OpenAIResponsesStreamAccumulator()
    return _TrackedOpenAISyncStream(
        stream,
        accumulator,
        run_id,
        name,
        type,
        accumulator.add_event,
        accumulator.should_emit_end,
        accumulator.error,
        accumulator.has_terminal_response,
    )


def _ensure_list_size(items, index):
    while len(items) <= index:
        items.append(None)


def _anthropic_build_content_block(block):
    serialized = AnthropicUtils.serialize_value(block)

    if isinstance(serialized, dict):
        if serialized.get("type") in {"tool_use", "server_tool_use"}:
            serialized.setdefault("input", {})
            serialized["_partial_input_json"] = ""
        return serialized

    return {"type": "text", "text": serialized}


def _anthropic_update_content_block(block, delta):
    serialized_delta = AnthropicUtils.serialize_value(delta)
    if not isinstance(serialized_delta, dict):
        return

    delta_type = serialized_delta.get("type")

    if delta_type == "text_delta":
        block["text"] = (block.get("text") or "") + serialized_delta.get("text", "")
        return

    if delta_type == "thinking_delta":
        block["thinking"] = (block.get("thinking") or "") + serialized_delta.get("thinking", "")
        return

    if delta_type == "signature_delta":
        block["signature"] = serialized_delta.get("signature")
        return

    if delta_type == "input_json_delta":
        partial_json = serialized_delta.get("partial_json", "")
        input_buffer = (block.get("_partial_input_json") or "") + partial_json
        block["_partial_input_json"] = input_buffer

        try:
            block["input"] = json.loads(input_buffer)
        except Exception:
            pass
        return

    for key, value in serialized_delta.items():
        if key == "type":
            continue
        if isinstance(value, str) and isinstance(block.get(key), str):
            block[key] = block.get(key, "") + value
        else:
            block[key] = value


def _anthropic_finalize_content_blocks(content_blocks):
    finalized_blocks = []
    for block in content_blocks:
        if not block:
            continue

        finalized_block = dict(block)
        finalized_block.pop("_partial_input_json", None)
        finalized_blocks.append(finalized_block)

    return finalized_blocks


def _anthropic_update_usage(token_usage, usage):
    parsed_usage = AnthropicUtils.parse_usage(usage)
    if not parsed_usage:
        return

    token_usage.update(parsed_usage)


def _anthropic_build_stream_result(content_blocks, token_usage, state):
    output = {
        "role": state.get("role") or "assistant",
        "content": _anthropic_finalize_content_blocks(content_blocks),
    }

    if state.get("message_id") is not None:
        output["id"] = state["message_id"]

    if state.get("model") is not None:
        output["model"] = state["model"]

    if state.get("stop_reason") is not None:
        output["stop_reason"] = state["stop_reason"]

    if state.get("stop_sequence") is not None:
        output["stop_sequence"] = state["stop_sequence"]

    return {
        "output": output,
        "tokensUsage": token_usage,
        "metadata": {
            key: value
            for key, value in {
                "messageId": state.get("message_id"),
                "stopReason": state.get("stop_reason"),
                "stopSequence": state.get("stop_sequence"),
                "serviceTier": state.get("service_tier"),
                "inferenceGeo": state.get("inference_geo"),
                "cacheCreationInputTokens": state.get("cache_creation_input_tokens"),
                "cacheReadInputTokens": state.get("cache_read_input_tokens"),
            }.items()
            if value is not None
        }
        or None,
    }


def _anthropic_consume_stream_event(event, content_blocks, token_usage, state):
    event_type = AnthropicUtils.get_property(event, "type")

    if event_type == "message_start":
        message = AnthropicUtils.get_property(event, "message")
        state["role"] = AnthropicUtils.get_property(message, "role") or state["role"]
        state["message_id"] = AnthropicUtils.get_property(message, "id") or state.get("message_id")
        state["model"] = AnthropicUtils.get_property(message, "model") or state.get("model")
        _anthropic_update_usage(token_usage, AnthropicUtils.get_property(message, "usage"))
        usage = AnthropicUtils.get_property(message, "usage")
        if usage is not None:
            state["service_tier"] = AnthropicUtils.get_property(usage, "service_tier") or state.get("service_tier")
            state["inference_geo"] = AnthropicUtils.get_property(usage, "inference_geo") or state.get("inference_geo")
            state["cache_creation_input_tokens"] = AnthropicUtils.get_property(
                usage, "cache_creation_input_tokens"
            )
            state["cache_read_input_tokens"] = AnthropicUtils.get_property(
                usage, "cache_read_input_tokens"
            )
        return

    if event_type == "content_block_start":
        index = AnthropicUtils.get_property(event, "index", 0)
        _ensure_list_size(content_blocks, index)
        content_blocks[index] = _anthropic_build_content_block(
            AnthropicUtils.get_property(event, "content_block")
        )
        return

    if event_type == "content_block_delta":
        index = AnthropicUtils.get_property(event, "index", 0)
        _ensure_list_size(content_blocks, index)

        if content_blocks[index] is None:
            content_blocks[index] = {"type": "text", "text": ""}

        _anthropic_update_content_block(
            content_blocks[index],
            AnthropicUtils.get_property(event, "delta"),
        )
        return

    if event_type == "message_delta":
        delta = AnthropicUtils.get_property(event, "delta")
        if delta:
            stop_reason = AnthropicUtils.get_property(delta, "stop_reason")
            if stop_reason is not None:
                state["stop_reason"] = stop_reason

            stop_sequence = AnthropicUtils.get_property(delta, "stop_sequence")
            if stop_sequence is not None:
                state["stop_sequence"] = stop_sequence

        _anthropic_update_usage(token_usage, AnthropicUtils.get_property(event, "usage"))
        usage = AnthropicUtils.get_property(event, "usage")
        if usage is not None:
            if AnthropicUtils.get_property(usage, "cache_creation_input_tokens") is not None:
                state["cache_creation_input_tokens"] = AnthropicUtils.get_property(
                    usage, "cache_creation_input_tokens"
                )
            if AnthropicUtils.get_property(usage, "cache_read_input_tokens") is not None:
                state["cache_read_input_tokens"] = AnthropicUtils.get_property(
                    usage, "cache_read_input_tokens"
                )
        return


class _TrackedAnthropicEventStream:
    def __init__(self, stream, run_id, name, type, app_id=None):
        self._stream = stream
        self._iterator = iter(stream)
        self._run_id = run_id
        self._name = name
        self._type = type
        self._app_id = app_id
        self._finished = False
        self._content_blocks = []
        self._token_usage = {"prompt": None, "completion": None}
        self._state = {
            "role": "assistant",
            "message_id": None,
            "model": None,
            "stop_reason": None,
            "stop_sequence": None,
            "service_tier": None,
            "inference_geo": None,
            "cache_creation_input_tokens": None,
            "cache_read_input_tokens": None,
        }

    def _close_stream(self):
        close = getattr(self._stream, "close", None)
        if callable(close):
            close()

    def _finalize(self):
        if self._finished:
            return

        parsed_output = _anthropic_build_stream_result(
            self._content_blocks, self._token_usage, self._state
        )
        track_event(
            self._type,
            "end",
            self._run_id,
            name=self._name,
            output=parsed_output["output"],
            token_usage=parsed_output["tokensUsage"],
            metadata=parsed_output["metadata"],
            app_id=self._app_id,
        )
        self._finished = True
        run_manager.end_run(self._run_id)

    def _track_error(self, error):
        if self._finished:
            return

        track_event(
            self._type,
            "error",
            self._run_id,
            error={"message": str(error), "stack": traceback.format_exc()},
            app_id=self._app_id,
        )
        self._finished = True
        run_manager.end_run(self._run_id)

    def __iter__(self):
        return self

    def __next__(self):
        try:
            event = next(self._iterator)
        except StopIteration:
            try:
                self._close_stream()
            finally:
                self._finalize()
            raise
        except Exception as exc:
            try:
                self._close_stream()
            except Exception:
                logger.exception("Error closing Anthropic stream after failure")
            self._track_error(exc)
            raise

        _anthropic_consume_stream_event(
            event, self._content_blocks, self._token_usage, self._state
        )
        return event

    def __enter__(self):
        enter = getattr(self._stream, "__enter__", None)
        if callable(enter):
            entered = enter()
            if entered is not None:
                self._stream = entered
                self._iterator = iter(entered)
        return self

    def __exit__(self, exc_type, exc, exc_tb):
        try:
            exit_method = getattr(self._stream, "__exit__", None)
            if callable(exit_method):
                return exit_method(exc_type, exc, exc_tb)
        except Exception as exit_error:
            self._track_error(exit_error)
            raise
        finally:
            self._finalize()

    def close(self):
        try:
            return self._close_stream()
        except Exception as exc:
            self._track_error(exc)
            raise
        finally:
            self._finalize()

    def __getattr__(self, key):
        return getattr(self._stream, key)


class _TrackedAsyncAnthropicEventStream:
    def __init__(self, stream, run_id, name, type, app_id=None):
        self._stream = stream
        self._iterator = None
        self._run_id = run_id
        self._name = name
        self._type = type
        self._app_id = app_id
        self._finished = False
        self._content_blocks = []
        self._token_usage = {"prompt": None, "completion": None}
        self._state = {
            "role": "assistant",
            "message_id": None,
            "model": None,
            "stop_reason": None,
            "stop_sequence": None,
            "service_tier": None,
            "inference_geo": None,
            "cache_creation_input_tokens": None,
            "cache_read_input_tokens": None,
        }

    def _ensure_iterator(self):
        if self._iterator is None:
            self._iterator = self._stream.__aiter__()
        return self._iterator

    async def _close_stream(self):
        close = getattr(self._stream, "close", None)
        if callable(close):
            result = close()
            if isawaitable(result):
                await result

    def _finalize(self):
        if self._finished:
            return

        parsed_output = _anthropic_build_stream_result(
            self._content_blocks, self._token_usage, self._state
        )
        track_event(
            self._type,
            "end",
            self._run_id,
            name=self._name,
            output=parsed_output["output"],
            token_usage=parsed_output["tokensUsage"],
            metadata=parsed_output["metadata"],
            app_id=self._app_id,
        )
        self._finished = True
        run_manager.end_run(self._run_id)

    def _track_error(self, error):
        if self._finished:
            return

        track_event(
            self._type,
            "error",
            self._run_id,
            error={"message": str(error), "stack": traceback.format_exc()},
            app_id=self._app_id,
        )
        self._finished = True
        run_manager.end_run(self._run_id)

    def __aiter__(self):
        return self

    async def __anext__(self):
        try:
            event = await self._ensure_iterator().__anext__()
        except StopAsyncIteration:
            try:
                await self._close_stream()
            finally:
                self._finalize()
            raise
        except Exception as exc:
            try:
                await self._close_stream()
            except Exception:
                logger.exception("Error closing Anthropic async stream after failure")
            self._track_error(exc)
            raise

        _anthropic_consume_stream_event(
            event, self._content_blocks, self._token_usage, self._state
        )
        return event

    async def __aenter__(self):
        enter = getattr(self._stream, "__aenter__", None)
        if callable(enter):
            entered = await enter()
            if entered is not None:
                self._stream = entered
                self._iterator = entered.__aiter__()
        return self

    async def __aexit__(self, exc_type, exc, exc_tb):
        try:
            exit_method = getattr(self._stream, "__aexit__", None)
            if callable(exit_method):
                return await exit_method(exc_type, exc, exc_tb)
        except Exception as exit_error:
            self._track_error(exit_error)
            raise
        finally:
            self._finalize()

    async def close(self):
        try:
            return await self._close_stream()
        except Exception as exc:
            self._track_error(exc)
            raise
        finally:
            self._finalize()

    def __getattr__(self, key):
        return getattr(self._stream, key)


def anthropic_stream_handler(fn, run_id, name, type, *args, **kwargs):
    return _TrackedAnthropicEventStream(
        fn(*args, **kwargs), run_id, name, type
    )


class _TrackedOpenAIAsyncStream:
    def __init__(
        self,
        stream,
        accumulator,
        run_id,
        name,
        type,
        add_item,
        is_completed,
        error_for_outcome,
        has_authoritative_outcome=None,
        terminal_claim=None,
    ):
        self._stream = stream
        self._accumulator = accumulator
        self._run_id = run_id
        self._name = name
        self._type = type
        self._add_item = add_item
        self._is_completed = is_completed
        self._error_for_outcome = error_for_outcome
        self._has_authoritative_outcome = (
            has_authoritative_outcome or (lambda: False)
        )
        self._finalized = False
        self._terminal_emitted = False
        self._terminal_suppressed = False
        self._provider_close_complete = False
        self._provider_errors_delegated = False
        self._provider_operation_active = False
        self._terminal_claim = terminal_claim or (lambda: True)

    @property
    def response(self):
        return getattr(self._stream, "response")

    def __aiter__(self):
        return self

    async def __anext__(self):
        if self._finalized:
            raise StopAsyncIteration
        self._provider_operation_active = True
        try:
            item = await self._stream.__anext__()
            self._add_item(item)
            return item
        except StopAsyncIteration:
            await self._finalize(eof=True)
            raise
        except asyncio.CancelledError:
            try:
                await self._close_provider()
            except BaseException:
                logger.exception(
                    "Error closing OpenAI async stream after cancellation"
                )
            self._emit_outcome(eof=False)
            raise
        except BaseException:
            await self._finalize_provider_failure(eof=False)
            raise
        finally:
            self._provider_operation_active = False

    async def _close_provider(self):
        if self._provider_close_complete:
            return None
        close = getattr(self._stream, "aclose", None)
        if not callable(close):
            close = getattr(self._stream, "close", None)
        if callable(close):
            self._provider_operation_active = True
            try:
                close_result = close()
                if isawaitable(close_result):
                    result = await close_result
                    self._provider_close_complete = True
                    return result
            finally:
                self._provider_operation_active = False
        self._provider_close_complete = True
        return None

    def delegate_provider_errors(self):
        self._provider_errors_delegated = True

    def _emit_provider_failure(self, *, eof):
        if self._has_authoritative_outcome():
            self._emit_outcome(eof=eof)
            return
        self._finalized = True
        if self._terminal_emitted or self._provider_errors_delegated:
            self._terminal_suppressed = True
            return
        self._terminal_emitted = True
        if not self._terminal_claim():
            return
        track_event(
            self._type,
            "error",
            self._run_id,
            name=self._name,
            error=_openai_provider_stream_error(),
        )

    async def _finalize_provider_failure(self, *, eof):
        if self._finalized:
            return
        self._finalized = True
        try:
            await self._close_provider()
        except BaseException:
            logger.exception("Error closing OpenAI async stream after failure")
        self._emit_provider_failure(eof=eof)

    def _emit_outcome(self, *, eof):
        if self._terminal_emitted or self._terminal_suppressed:
            return
        self._finalized = True
        self._terminal_emitted = True
        if not self._terminal_claim():
            return
        if self._is_completed():
            track_event(
                self._type,
                "end",
                self._run_id,
                name=self._name,
                output=self._accumulator.output(),
                token_usage=self._accumulator.token_usage(),
            )
        else:
            track_event(
                self._type,
                "error",
                self._run_id,
                name=self._name,
                output=self._accumulator.output(),
                token_usage=self._accumulator.token_usage(),
                error=self._error_for_outcome(eof=eof),
            )

    async def _finalize(self, *, eof):
        try:
            await self._close_provider()
        except asyncio.CancelledError:
            self._emit_outcome(eof=eof)
            raise
        except BaseException:
            self._emit_provider_failure(eof=eof)
            raise
        self._emit_outcome(eof=eof)

    async def close(self):
        return await self._finalize(eof=False)

    async def aclose(self):
        return await self.close()

    async def __aenter__(self):
        return self

    async def __aexit__(self, _exc_type, _exc, _exc_tb):
        if _exc_type is None:
            await self.close()
            return False
        if self._finalized:
            return False
        try:
            await self.close()
        except BaseException:
            logger.exception(
                "Error closing OpenAI async stream while propagating an exception"
            )
        return False

    def __getattr__(self, key):
        return getattr(self._stream, key)


async def async_stream_handler(fn, run_id, name, type, *args, **kwargs):
    stream = await fn(*args, **kwargs)
    accumulator = OpenAIChatStreamAccumulator(kwargs.get("n", 1))
    return _TrackedOpenAIAsyncStream(
        stream,
        accumulator,
        run_id,
        name,
        type,
        accumulator.add_chunk,
        accumulator.has_terminal_choice_state,
        lambda *, eof: _chat_stream_error(accumulator, eof=eof),
    )


async def async_openai_responses_stream_handler(
    fn, run_id, name, type, *args, **kwargs
):
    stream = await fn(*args, **kwargs)
    accumulator = OpenAIResponsesStreamAccumulator()
    return _TrackedOpenAIAsyncStream(
        stream,
        accumulator,
        run_id,
        name,
        type,
        accumulator.add_event,
        accumulator.should_emit_end,
        accumulator.error,
        accumulator.has_terminal_response,
    )


async def async_anthropic_stream_handler(fn, run_id, name, type, *args, **kwargs):
    stream = await fn(*args, **kwargs)
    return _TrackedAsyncAnthropicEventStream(stream, run_id, name, type)


def _merge_parsed_input_params(params, parsed_input):
    """Merge parser provenance, honoring explicit provider-shape overrides."""
    merged = copy.deepcopy(params)
    if not isinstance(parsed_input, dict):
        return merged
    extra = parsed_input.get("extra")
    if not isinstance(extra, dict):
        return merged
    for key, value in extra.items():
        merged.setdefault(key, copy.deepcopy(value))
    overrides = parsed_input.get("param_overrides")
    if isinstance(overrides, dict):
        for key, value in overrides.items():
            merged[key] = copy.deepcopy(value)
    omissions = parsed_input.get("param_omissions")
    if isinstance(omissions, (list, tuple, set)):
        for key in omissions:
            merged.pop(key, None)
    return merged


_MAX_TEMPLATE_VERSION_ID = 2_147_483_647


def _extract_template_version_id(kwargs):
    """Return only canonical template-version provenance from request headers."""
    if not isinstance(kwargs, Mapping):
        return None

    headers = kwargs.get("extra_headers")
    if not isinstance(headers, Mapping):
        return None

    value = headers.get("Template-Id")
    if isinstance(value, bool):
        return None
    if isinstance(value, int):
        return str(value) if 0 < value <= _MAX_TEMPLATE_VERSION_ID else None
    if (
        not isinstance(value, str)
        or not value.isascii()
        or not value.isdecimal()
        or value.startswith("0")
    ):
        return None

    parsed = int(value)
    return value if parsed <= _MAX_TEMPLATE_VERSION_ID else None


def _prepare_tracked_helper_context(
    args,
    kwargs,
    *,
    name=None,
    user_id=None,
    user_props=None,
    tags=None,
    input_parser=default_input_parser,
    preserve_metadata: bool = False,
):
    tracked_kwargs = copy.copy(kwargs)
    parent_run_id = tracked_kwargs.pop("parent", run_manager.current_run_id)
    metadata = (
        tracked_kwargs.get("metadata")
        if preserve_metadata
        else tracked_kwargs.pop("metadata", None)
    )
    parsed_input = input_parser(*args, **tracked_kwargs)
    params = _merge_parsed_input_params(
        filter_params(tracked_kwargs), parsed_input
    )

    return tracked_kwargs, {
        "finished": False,
        "name": name or parsed_input["name"],
        "input": parsed_input["input"],
        "metadata": metadata,
        "params": params,
        "parent_run_id": parent_run_id,
        "template_id": _extract_template_version_id(tracked_kwargs),
        "user_id": tracked_kwargs.pop("user_id", None) or user_ctx.get() or user_id,
        "user_props": tracked_kwargs.pop("user_props", None)
        or user_props
        or user_props_ctx.get(),
        "tags": tracked_kwargs.pop("tags", None) or tags or tags_ctx.get(),
    }


def _start_tracked_helper_run(context, type, app_id=None):
    if context.get("run") is not None:
        return context["run"]

    run = run_manager.start_run(parent_run_id=context["parent_run_id"])
    context["run"] = run

    track_event(
        type,
        "start",
        run_id=run.id,
        parent_run_id=context["parent_run_id"],
        input=context["input"],
        name=context["name"],
        user_id=context["user_id"],
        user_props=context["user_props"],
        params=context["params"],
        metadata=context["metadata"],
        tags=context["tags"],
        template_id=context["template_id"],
        app_id=app_id,
    )

    return run


def _get_anthropic_stream_snapshot(stream):
    try:
        for key, value in vars(stream).items():
            if key.endswith("__final_message_snapshot"):
                return value
    except Exception:
        logger.exception("Error reading Anthropic stream snapshot")

    return None


def _parse_tracked_helper_output(output_parser, output):
    if output is None:
        return {"output": None, "tokensUsage": None, "metadata": None}

    try:
        return output_parser(output, True)
    except Exception:
        logger.exception("Error parsing Anthropic helper output")
        return {"output": AnthropicUtils.serialize_value(output), "tokensUsage": None, "metadata": None}


def _track_tracked_helper_end(context, type, output_parser, output, app_id=None):
    if context.get("finished") or context.get("run") is None:
        return

    parsed_output = _parse_tracked_helper_output(output_parser, output)

    track_event(
        type,
        "end",
        context["run"].id,
        name=context["name"],
        output=parsed_output["output"],
        token_usage=parsed_output["tokensUsage"],
        metadata=parsed_output.get("metadata"),
        app_id=app_id,
    )

    context["finished"] = True
    run_manager.end_run(context["run"].id)


def _track_tracked_helper_error(context, type, error, app_id=None):
    if context.get("finished") or context.get("run") is None:
        return

    track_event(
        type,
        "error",
        context["run"].id,
        error={"message": str(error), "stack": traceback.format_exc()},
        app_id=app_id,
    )

    context["finished"] = True
    run_manager.end_run(context["run"].id)


class _TrackedAnthropicStream:
    def __init__(self, stream, context, type, output_parser, app_id=None):
        self._stream = stream
        self._context = context
        self._type = type
        self._output_parser = output_parser
        self._app_id = app_id
        self.text_stream = self._text_stream()

    def _finalize_from_snapshot(self):
        _track_tracked_helper_end(
            self._context,
            self._type,
            self._output_parser,
            _get_anthropic_stream_snapshot(self._stream),
            app_id=self._app_id,
        )

    def __iter__(self):
        return self

    def __next__(self):
        try:
            return next(self._stream)
        except StopIteration:
            self._finalize_from_snapshot()
            raise
        except Exception as exc:
            _track_tracked_helper_error(
                self._context, self._type, exc, app_id=self._app_id
            )
            raise

    def _text_stream(self):
        try:
            for text in self._stream.text_stream:
                yield text
            self._finalize_from_snapshot()
        except Exception as exc:
            _track_tracked_helper_error(
                self._context, self._type, exc, app_id=self._app_id
            )
            raise

    def close(self):
        try:
            return self._stream.close()
        finally:
            self._finalize_from_snapshot()

    def get_final_message(self):
        try:
            message = self._stream.get_final_message()
        except Exception as exc:
            _track_tracked_helper_error(
                self._context, self._type, exc, app_id=self._app_id
            )
            raise

        _track_tracked_helper_end(
            self._context,
            self._type,
            self._output_parser,
            message,
            app_id=self._app_id,
        )
        return message

    def get_final_text(self):
        try:
            text = self._stream.get_final_text()
        except Exception as exc:
            _track_tracked_helper_error(
                self._context, self._type, exc, app_id=self._app_id
            )
            raise

        self._finalize_from_snapshot()
        return text

    def until_done(self):
        try:
            return self._stream.until_done()
        except Exception as exc:
            _track_tracked_helper_error(
                self._context, self._type, exc, app_id=self._app_id
            )
            raise
        finally:
            self._finalize_from_snapshot()

    def __getattr__(self, key):
        return getattr(self._stream, key)


class _TrackedAnthropicStreamManager:
    def __init__(self, manager, context, type, output_parser, app_id=None):
        self._manager = manager
        self._context = context
        self._type = type
        self._output_parser = output_parser
        self._app_id = app_id
        self._stream = None

    def __enter__(self):
        _start_tracked_helper_run(self._context, self._type, app_id=self._app_id)

        try:
            stream = self._manager.__enter__()
        except Exception as exc:
            _track_tracked_helper_error(
                self._context, self._type, exc, app_id=self._app_id
            )
            raise

        self._stream = _TrackedAnthropicStream(
            stream,
            self._context,
            self._type,
            self._output_parser,
            app_id=self._app_id,
        )
        return self._stream

    def __exit__(self, exc_type, exc, exc_tb):
        try:
            return self._manager.__exit__(exc_type, exc, exc_tb)
        except Exception as exit_error:
            _track_tracked_helper_error(
                self._context, self._type, exit_error, app_id=self._app_id
            )
            raise
        finally:
            if self._stream is not None:
                self._stream._finalize_from_snapshot()

    def __getattr__(self, key):
        return getattr(self._manager, key)


class _TrackedAsyncAnthropicStream:
    def __init__(self, stream, context, type, output_parser, app_id=None):
        self._stream = stream
        self._context = context
        self._type = type
        self._output_parser = output_parser
        self._app_id = app_id
        self.text_stream = self._text_stream()

    def _finalize_from_snapshot(self):
        _track_tracked_helper_end(
            self._context,
            self._type,
            self._output_parser,
            _get_anthropic_stream_snapshot(self._stream),
            app_id=self._app_id,
        )

    def __aiter__(self):
        return self

    async def __anext__(self):
        try:
            return await self._stream.__anext__()
        except StopAsyncIteration:
            self._finalize_from_snapshot()
            raise
        except Exception as exc:
            _track_tracked_helper_error(
                self._context, self._type, exc, app_id=self._app_id
            )
            raise

    async def _text_stream(self):
        try:
            async for text in self._stream.text_stream:
                yield text
            self._finalize_from_snapshot()
        except Exception as exc:
            _track_tracked_helper_error(
                self._context, self._type, exc, app_id=self._app_id
            )
            raise

    async def close(self):
        try:
            return await self._stream.close()
        finally:
            self._finalize_from_snapshot()

    async def get_final_message(self):
        try:
            message = await self._stream.get_final_message()
        except Exception as exc:
            _track_tracked_helper_error(
                self._context, self._type, exc, app_id=self._app_id
            )
            raise

        _track_tracked_helper_end(
            self._context,
            self._type,
            self._output_parser,
            message,
            app_id=self._app_id,
        )
        return message

    async def get_final_text(self):
        try:
            text = await self._stream.get_final_text()
        except Exception as exc:
            _track_tracked_helper_error(
                self._context, self._type, exc, app_id=self._app_id
            )
            raise

        self._finalize_from_snapshot()
        return text

    async def until_done(self):
        try:
            return await self._stream.until_done()
        except Exception as exc:
            _track_tracked_helper_error(
                self._context, self._type, exc, app_id=self._app_id
            )
            raise
        finally:
            self._finalize_from_snapshot()

    def __getattr__(self, key):
        return getattr(self._stream, key)


class _TrackedAsyncAnthropicStreamManager:
    def __init__(self, manager, context, type, output_parser, app_id=None):
        self._manager = manager
        self._context = context
        self._type = type
        self._output_parser = output_parser
        self._app_id = app_id
        self._stream = None

    async def __aenter__(self):
        _start_tracked_helper_run(self._context, self._type, app_id=self._app_id)

        try:
            stream = await self._manager.__aenter__()
        except Exception as exc:
            _track_tracked_helper_error(
                self._context, self._type, exc, app_id=self._app_id
            )
            raise

        self._stream = _TrackedAsyncAnthropicStream(
            stream,
            self._context,
            self._type,
            self._output_parser,
            app_id=self._app_id,
        )
        return self._stream

    async def __aexit__(self, exc_type, exc, exc_tb):
        try:
            return await self._manager.__aexit__(exc_type, exc, exc_tb)
        except Exception as exit_error:
            _track_tracked_helper_error(
                self._context, self._type, exit_error, app_id=self._app_id
            )
            raise
        finally:
            if self._stream is not None:
                self._stream._finalize_from_snapshot()

    def __getattr__(self, key):
        return getattr(self._manager, key)


def _set_anthropic_helper_context(user_id=None, user_props=None, tags=None):
    tokens = []

    if user_id is not None:
        tokens.append((user_ctx, user_ctx.set(user_id)))

    if user_props is not None:
        tokens.append((user_props_ctx, user_props_ctx.set(user_props)))

    if tags is not None:
        tokens.append((tags_ctx, tags_ctx.set(tags)))

    return tokens


def _reset_anthropic_helper_context(tokens):
    for ctx_var, token in reversed(tokens):
        ctx_var.reset(token)


def _call_with_anthropic_helper_context(context, fn, *args, **kwargs):
    tokens = _set_anthropic_helper_context(
        context.get("user_id"),
        context.get("user_props"),
        context.get("tags"),
    )
    try:
        return fn(*args, **kwargs)
    finally:
        _reset_anthropic_helper_context(tokens)


async def _acall_with_anthropic_helper_context(context, fn, *args, **kwargs):
    tokens = _set_anthropic_helper_context(
        context.get("user_id"),
        context.get("user_props"),
        context.get("tags"),
    )
    try:
        return await fn(*args, **kwargs)
    finally:
        _reset_anthropic_helper_context(tokens)


class _TrackedAnthropicToolRunner:
    def __init__(self, runner, context):
        self._runner = runner
        self._context = context
        self._iterator = None

    def __iter__(self):
        if self._iterator is None:
            self._iterator = _call_with_anthropic_helper_context(
                self._context, iter, self._runner
            )
        return self

    def __next__(self):
        if self._iterator is None:
            self._iterator = _call_with_anthropic_helper_context(
                self._context, iter, self._runner
            )
        return _call_with_anthropic_helper_context(
            self._context, next, self._iterator
        )

    def __getattr__(self, key):
        attr = getattr(self._runner, key)

        if callable(attr):
            def wrapped(*args, **kwargs):
                return _call_with_anthropic_helper_context(
                    self._context, attr, *args, **kwargs
                )

            return wrapped

        return attr


class _TrackedAsyncAnthropicToolRunner:
    def __init__(self, runner, context):
        self._runner = runner
        self._context = context
        self._iterator = None

    def __aiter__(self):
        if self._iterator is None:
            self._iterator = self._runner.__aiter__()
        return self

    async def __anext__(self):
        if self._iterator is None:
            self._iterator = self._runner.__aiter__()
        return await _acall_with_anthropic_helper_context(
            self._context, self._iterator.__anext__
        )

    def __getattr__(self, key):
        attr = getattr(self._runner, key)

        if callable(attr):
            async def wrapped(*args, **kwargs):
                async def invoke():
                    result = attr(*args, **kwargs)
                    if isawaitable(result):
                        return await result
                    return result

                return await _acall_with_anthropic_helper_context(
                    self._context, invoke
                )

            return wrapped

        return attr


def wrap_anthropic_tool_runner(fn, user_id=None, user_props=None, tags=None):
    @wraps(fn)
    def sync_wrapper(*args, **kwargs):
        context = {
            "user_id": kwargs.pop("user_id", None) or user_ctx.get() or user_id,
            "user_props": kwargs.pop("user_props", None)
            or user_props
            or user_props_ctx.get(),
            "tags": kwargs.pop("tags", None) or tags or tags_ctx.get(),
        }
        kwargs.pop("parent", None)

        runner = _call_with_anthropic_helper_context(context, fn, *args, **kwargs)
        return _TrackedAnthropicToolRunner(runner, context)

    return sync_wrapper


def wrap_async_anthropic_tool_runner(fn, user_id=None, user_props=None, tags=None):
    @wraps(fn)
    async def async_wrapper(*args, **kwargs):
        context = {
            "user_id": kwargs.pop("user_id", None) or user_ctx.get() or user_id,
            "user_props": kwargs.pop("user_props", None)
            or user_props
            or user_props_ctx.get(),
            "tags": kwargs.pop("tags", None) or tags or tags_ctx.get(),
        }
        kwargs.pop("parent", None)

        runner = await _acall_with_anthropic_helper_context(
            context, fn, *args, **kwargs
        )
        return _TrackedAsyncAnthropicToolRunner(runner, context)

    return async_wrapper


def wrap_anthropic_stream_manager(
    fn,
    type=None,
    name=None,
    user_id=None,
    user_props=None,
    tags=None,
    input_parser=default_input_parser,
    output_parser=default_output_parser,
    app_id=None,
    preserve_metadata: bool = False,
):
    @wraps(fn)
    def sync_wrapper(*args, **kwargs):
        tracked_kwargs, context = _prepare_tracked_helper_context(
            args,
            kwargs,
            name=name,
            user_id=user_id,
            user_props=user_props,
            tags=tags,
            input_parser=input_parser,
            preserve_metadata=preserve_metadata,
        )
        manager = fn(*args, **tracked_kwargs)
        return _TrackedAnthropicStreamManager(
            manager,
            context,
            type,
            output_parser,
            app_id=app_id,
        )

    return sync_wrapper


def wrap_async_anthropic_stream_manager(
    fn,
    type=None,
    name=None,
    user_id=None,
    user_props=None,
    tags=None,
    input_parser=default_input_parser,
    output_parser=default_output_parser,
    app_id=None,
    preserve_metadata: bool = False,
):
    @wraps(fn)
    def async_wrapper(*args, **kwargs):
        tracked_kwargs, context = _prepare_tracked_helper_context(
            args,
            kwargs,
            name=name,
            user_id=user_id,
            user_props=user_props,
            tags=tags,
            input_parser=input_parser,
            preserve_metadata=preserve_metadata,
        )
        manager = fn(*args, **tracked_kwargs)
        return _TrackedAsyncAnthropicStreamManager(
            manager,
            context,
            type,
            output_parser,
            app_id=app_id,
        )

    return async_wrapper


def ibm_stream_handler(fn, run_id, name, type, *args, **kwargs):
    try:
        stream = fn(*args, **kwargs)

        content = ""
        tool_call = {} ## TODO: handle multiple tool calls in response
        prompt_tokens = 0
        completion_tokens = 0

        for chunk in stream:
            prompt_tokens = chunk['usage']['prompt_tokens']
            completion_tokens = chunk['usage'].get('completion_tokens', 0)

            delta = chunk['choices'][0]['delta']
            content += delta.get('content', '')

            if 'tool_calls' in delta:
                if delta['tool_calls'][0].get('id'):
                    tool_call['id'] = delta['tool_calls'][0]['id']
                if delta['tool_calls'][0].get('type'):
                    tool_call['type'] = delta['tool_calls'][0]['type']
                if delta['tool_calls'][0].get('function'):
                    if tool_call.get('function') is None:
                        tool_call['function'] = {
                            "name": '',
                            "arguments": ''
                        }
                    tool_call['function']["name"] += delta['tool_calls'][0]['function']['name']
                    tool_call['function']["arguments"] += delta['tool_calls'][0]['function']['arguments']

            yield chunk
    finally:
        stream.close()

    output = {
        "role": "assistant",
        "content": content,
        "tool_calls": [tool_call] if tool_call else None
    } 
    token_usage = {
        "prompt": prompt_tokens,
        "completion": completion_tokens
    }
    track_event(
        type,
        "end",
        run_id,
        name=name,
        output=output,
        token_usage=token_usage
    )
    return


class _OpenAISyncResponseProxy:
    def __init__(self, response, close_stream):
        self._response = response
        self._close_stream = close_stream

    def close(self):
        return self._close_stream()

    def __getattr__(self, key):
        return getattr(self._response, key)


class _ManagedOpenAISyncStream:
    def __init__(
        self, stream, run_id, type, name, app_id, terminal_claim=None
    ):
        self._stream = stream
        self._stream.delegate_provider_errors()
        self._run_id = run_id
        self._type = type
        self._name = name
        self._app_id = app_id
        self._error_tracked = False
        self._response_proxy = None
        self._terminal_claim = terminal_claim or (lambda: True)

    @property
    def __class__(self):
        return self._stream._stream.__class__

    @property
    def response(self):
        if self._response_proxy is None:
            self._response_proxy = _OpenAISyncResponseProxy(
                self._stream.response, self.close
            )
        return self._response_proxy

    def __iter__(self):
        return self

    def __next__(self):
        try:
            return next(self._stream)
        except StopIteration:
            raise
        except Exception:
            if not getattr(self._stream, "_terminal_emitted", False):
                self._track_provider_error()
            raise

    def _track_provider_error(self):
        if self._error_tracked:
            return
        self._error_tracked = True
        if not self._terminal_claim():
            return
        track_event(
            self._type,
            "error",
            self._run_id,
            name=self._name,
            error=_openai_provider_stream_error(),
            app_id=self._app_id,
        )

    def close(self):
        try:
            return self._stream.close()
        except Exception:
            if not getattr(self._stream, "_terminal_emitted", False):
                self._track_provider_error()
            raise

    def __enter__(self):
        return self

    def __exit__(self, _exc_type, _exc, _exc_tb):
        if _exc_type is None:
            self.close()
            return False
        if getattr(self._stream, "_finalized", False):
            return False
        try:
            self.close()
        except BaseException:
            logger.exception(
                "Error closing managed OpenAI stream while propagating an exception"
            )
        return False

    def __getattr__(self, key):
        return getattr(self._stream, key)


class _OpenAIAsyncResponseProxy:
    def __init__(self, response, close_stream):
        self._response = response
        self._close_stream = close_stream

    async def aclose(self):
        return await self._close_stream()

    def __getattr__(self, key):
        return getattr(self._response, key)


class _ManagedOpenAIAsyncStream:
    def __init__(
        self, stream, run_id, type, name, app_id, terminal_claim=None
    ):
        self._stream = stream
        self._stream.delegate_provider_errors()
        self._run_id = run_id
        self._type = type
        self._name = name
        self._app_id = app_id
        self._error_tracked = False
        self._response_proxy = None
        self._terminal_claim = terminal_claim or (lambda: True)

    @property
    def __class__(self):
        return self._stream._stream.__class__

    @property
    def response(self):
        if self._response_proxy is None:
            self._response_proxy = _OpenAIAsyncResponseProxy(
                self._stream.response, self.aclose
            )
        return self._response_proxy

    def __aiter__(self):
        return self

    async def __anext__(self):
        try:
            return await self._stream.__anext__()
        except StopAsyncIteration:
            raise
        except asyncio.CancelledError:
            raise
        except Exception:
            if not getattr(self._stream, "_terminal_emitted", False):
                self._track_provider_error()
            raise

    def _track_provider_error(self):
        if self._error_tracked:
            return
        self._error_tracked = True
        if not self._terminal_claim():
            return
        track_event(
            self._type,
            "error",
            self._run_id,
            name=self._name,
            error=_openai_provider_stream_error(),
            app_id=self._app_id,
        )

    async def close(self):
        try:
            return await self._stream.close()
        except asyncio.CancelledError:
            raise
        except Exception:
            if not getattr(self._stream, "_terminal_emitted", False):
                self._track_provider_error()
            raise

    async def aclose(self):
        return await self.close()

    async def __aenter__(self):
        return self

    async def __aexit__(self, _exc_type, _exc, _exc_tb):
        if _exc_type is None:
            await self.close()
            return False
        if getattr(self._stream, "_finalized", False):
            return False
        try:
            await self.close()
        except BaseException:
            logger.exception(
                "Error closing managed OpenAI async stream while propagating an exception"
            )
        return False

    def __getattr__(self, key):
        return getattr(self._stream, key)


_OPENAI_METADATA_MISSING = object()
_OPENAI_STREAM_TRACKING_METADATA_KEY = object()
_OPENAI_STREAM_LUNARY_CONTROLS_KEY = object()
_OPENAI_LUNARY_CONTROL_KEYS = (
    "parent",
    "user_id",
    "user_props",
    "tags",
)


class _OpenAIFailedIterable(Iterator):
    _lunary_capture_unavailable_reason = "materialization_failed"

    def __init__(self, items, error):
        self._items = iter(items)
        self._error = error
        self._raised = False

    def __next__(self):
        try:
            return next(self._items)
        except StopIteration:
            if self._raised:
                raise
            self._raised = True
            raise self._error


def _materialize_openai_iterables(kwargs, fields):
    for key in fields:
        value = kwargs.get(key, _OPENAI_METADATA_MISSING)
        if (
            isinstance(value, (list, tuple, str, bytes, Mapping))
            or not isinstance(value, Iterable)
        ):
            continue

        materialized = []
        try:
            materialized.extend(value)
        except Exception as error:
            kwargs[key] = _OpenAIFailedIterable(materialized, error)
        else:
            kwargs[key] = materialized


def _stream_entry_error_payload(
    error, *, stream_handler, openai_metadata
):
    if openai_metadata or stream_handler in {
        default_stream_handler,
        openai_responses_stream_handler,
        async_stream_handler,
        async_openai_responses_stream_handler,
    }:
        return _openai_provider_stream_error()
    return {"message": str(error), "stack": traceback.format_exc()}


def _extract_call_metadata(
    kwargs,
    *,
    preserve_metadata: bool,
    openai_metadata: bool,
):
    extra_body = kwargs.get("extra_body")
    if (
        isinstance(extra_body, Mapping)
        and _OPENAI_STREAM_TRACKING_METADATA_KEY in extra_body
    ):
        metadata = extra_body[_OPENAI_STREAM_TRACKING_METADATA_KEY]
        cleaned_extra_body = {
            key: value
            for key, value in extra_body.items()
            if key is not _OPENAI_STREAM_TRACKING_METADATA_KEY
        }
        if cleaned_extra_body:
            kwargs["extra_body"] = cleaned_extra_body
        else:
            kwargs.pop("extra_body", None)
        return None if is_openai_omitted(metadata) else metadata

    if openai_metadata:
        metadata = kwargs.pop("metadata", None)
        provider_metadata = kwargs.pop(
            "openai_metadata", _OPENAI_METADATA_MISSING
        )
        if provider_metadata is not _OPENAI_METADATA_MISSING:
            kwargs["metadata"] = provider_metadata
        return None if is_openai_omitted(metadata) else metadata

    if preserve_metadata:
        metadata = kwargs.get("metadata")
        return None if is_openai_omitted(metadata) else metadata

    metadata = kwargs.pop("metadata", None)
    return None if is_openai_omitted(metadata) else metadata


def _restore_openai_stream_lunary_controls(kwargs):
    extra_body = kwargs.get("extra_body")
    if (
        not isinstance(extra_body, Mapping)
        or _OPENAI_STREAM_LUNARY_CONTROLS_KEY not in extra_body
    ):
        return

    controls = extra_body[_OPENAI_STREAM_LUNARY_CONTROLS_KEY]
    cleaned_extra_body = {
        key: value
        for key, value in extra_body.items()
        if key is not _OPENAI_STREAM_LUNARY_CONTROLS_KEY
    }
    if cleaned_extra_body:
        kwargs["extra_body"] = cleaned_extra_body
    else:
        kwargs.pop("extra_body", None)

    if not isinstance(controls, Mapping):
        return
    for key in _OPENAI_LUNARY_CONTROL_KEYS:
        if key in controls:
            kwargs.setdefault(key, controls[key])


def _wrap_openai_stream_metadata(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        lunary_controls = {
            key: kwargs.pop(key)
            for key in _OPENAI_LUNARY_CONTROL_KEYS
            if key in kwargs
        }
        provider_metadata = kwargs.pop(
            "openai_metadata", _OPENAI_METADATA_MISSING
        )
        existing_response = (
            "response_id" in kwargs
            and not is_openai_omitted(kwargs["response_id"])
        )
        if (
            existing_response
            and provider_metadata is not _OPENAI_METADATA_MISSING
        ):
            raise TypeError(
                "openai_metadata is not supported when streaming an "
                "existing response"
            )

        tracking_metadata = _OPENAI_METADATA_MISSING
        if existing_response:
            tracking_metadata = kwargs.pop(
                "metadata", _OPENAI_METADATA_MISSING
            )
            if (
                tracking_metadata is _OPENAI_METADATA_MISSING
                and not lunary_controls
            ):
                return fn(*args, **kwargs)
        else:
            if (
                provider_metadata is _OPENAI_METADATA_MISSING
                and not lunary_controls
            ):
                return fn(*args, **kwargs)
            if provider_metadata is not _OPENAI_METADATA_MISSING:
                tracking_metadata = kwargs.pop("metadata", None)

        extra_body = kwargs.get("extra_body")
        if extra_body is None or is_openai_omitted(extra_body):
            extra_body = {}
        elif isinstance(extra_body, Mapping):
            extra_body = dict(extra_body)
        else:
            raise TypeError("extra_body must be a mapping")
        if tracking_metadata is not _OPENAI_METADATA_MISSING:
            extra_body[_OPENAI_STREAM_TRACKING_METADATA_KEY] = tracking_metadata
        if lunary_controls:
            extra_body[_OPENAI_STREAM_LUNARY_CONTROLS_KEY] = lunary_controls
        kwargs["extra_body"] = extra_body
        if (
            not existing_response
            and provider_metadata is not _OPENAI_METADATA_MISSING
        ):
            kwargs["metadata"] = provider_metadata
        return fn(*args, **kwargs)

    return wrapper


def _raw_response_unparsed_error(*, streamed_response):
    if streamed_response:
        return {
            "code": "stream_cancelled",
            "message": "OpenAI response stream closed before parsing",
        }
    return {
        "code": "raw_response_unparsed",
        "message": "OpenAI raw response was not parsed",
    }


class _OpenAIDeferredResponseTracker:
    def __init__(
        self,
        args,
        kwargs,
        *,
        input_parser,
        output_parser,
        openai_iterable_fields,
        responses_api,
        async_client,
        streamed_response,
    ):
        self._args = args
        self._kwargs = copy.copy(kwargs)
        self._input_parser = input_parser
        self._output_parser = output_parser
        self._openai_iterable_fields = openai_iterable_fields
        self._responses_api = responses_api
        self._async_client = async_client
        self._streamed_response = streamed_response
        self._explicit_parent = self._kwargs.pop(
            "parent", _OPENAI_METADATA_MISSING
        )
        self._explicit_user_id = self._kwargs.pop("user_id", None)
        self._explicit_user_props = self._kwargs.pop("user_props", None)
        self._explicit_tags = self._kwargs.pop("tags", None)
        try:
            self._metadata = _extract_call_metadata(
                self._kwargs,
                preserve_metadata=False,
                openai_metadata=True,
            )
        except Exception as error:
            logger.exception(error)
            self._metadata = None

        self._run = None
        self._request_scope_open = False
        self._name = None
        self._finished = False
        self._managed_stream = None
        self._managed_streams = {}
        self._linked_stream_responses = set()
        self._closing_managed_stream = False

    @property
    def provider_kwargs(self):
        return self._kwargs

    def materialize_iterables(self, request_func=None):
        if not self._openai_iterable_fields:
            return

        _materialize_openai_iterables(
            self._kwargs, self._openai_iterable_fields
        )
        request_kwargs = getattr(request_func, "keywords", None)
        if not isinstance(request_kwargs, dict):
            return
        for field in self._openai_iterable_fields:
            if field in self._kwargs and field in request_kwargs:
                request_kwargs[field] = self._kwargs[field]

    def start_request(self):
        if self._run is not None:
            return

        parent_run_id = (
            run_manager.current_run_id
            if self._explicit_parent is _OPENAI_METADATA_MISSING
            else self._explicit_parent
        )
        self._run = run_manager.start_run(parent_run_id=parent_run_id)
        self._request_scope_open = True
        parsed_input = {"name": None, "input": None}
        params = {}
        try:
            params = filter_params(self._kwargs)
            parsed_input = self._input_parser(*self._args, **self._kwargs)
            params = _merge_parsed_input_params(params, parsed_input)
        except Exception as error:
            logger.exception(error)

        self._name = parsed_input.get("name")
        try:
            track_event(
                "llm",
                "start",
                run_id=self._run.id,
                parent_run_id=parent_run_id,
                input=parsed_input.get("input"),
                name=self._name,
                user_id=self._explicit_user_id or user_ctx.get(),
                user_props=(
                    self._explicit_user_props or user_props_ctx.get()
                ),
                params=params,
                metadata=self._metadata,
                tags=self._explicit_tags or tags_ctx.get(),
                template_id=_extract_template_version_id(self._kwargs),
            )
        except Exception as error:
            logger.exception(error)

    def end_request_scope(self):
        if not self._request_scope_open:
            return
        self._request_scope_open = False
        run_manager.end_run(self._run.id)

    def _track_error(self, error=None):
        if self._finished or self._run is None:
            return
        self._finished = True
        try:
            track_event(
                "llm",
                "error",
                self._run.id,
                name=self._name,
                error=error or _openai_provider_stream_error(),
            )
        except Exception as tracking_error:
            logger.exception(tracking_error)

    def track_provider_error(self):
        self._track_error(_openai_provider_stream_error())

    def _track_parsed_response(self, response):
        if self._finished:
            return
        try:
            parsed_output = self._output_parser(response, False)
        except Exception as error:
            logger.exception(error)
            self._track_error(
                {
                    "code": "response_parse_error",
                    "message": "OpenAI response could not be recorded",
                }
            )
            return

        self._finished = True
        event = "end"
        error = None
        if self._responses_api:
            status = OpenAIUtils.get_property(response, "status")
            if status == "failed":
                event = "error"
                provider_error = OpenAIUtils.serialize_value(
                    OpenAIUtils.get_property(response, "error")
                )
                if not isinstance(provider_error, dict):
                    provider_error = {}
                error = {
                    "code": provider_error.get("code")
                    or "response_failed",
                    "message": provider_error.get("message")
                    or "OpenAI response failed",
                }

        payload = {
            "name": self._name,
            "output": parsed_output["output"],
            "token_usage": parsed_output["tokensUsage"],
            "metadata": parsed_output.get("metadata"),
        }
        if error is not None:
            payload["error"] = error
        try:
            track_event("llm", event, self._run.id, **payload)
        except Exception as tracking_error:
            logger.exception(tracking_error)

    def _manage_parsed_stream(self, stream):
        stream_key = id(stream)
        existing = self._managed_streams.get(stream_key)
        if existing is not None:
            self._managed_stream = existing
            return existing

        if self._responses_api:
            accumulator = OpenAIResponsesStreamAccumulator()
            if self._async_client:
                tracked = _TrackedOpenAIAsyncStream(
                    stream,
                    accumulator,
                    self._run.id,
                    self._name,
                    "llm",
                    accumulator.add_event,
                    accumulator.should_emit_end,
                    accumulator.error,
                    accumulator.has_terminal_response,
                    self._claim_stream_terminal,
                )
                self._managed_stream = _ManagedOpenAIAsyncStream(
                    tracked,
                    self._run.id,
                    "llm",
                    self._name,
                    None,
                    self._claim_stream_terminal,
                )
            else:
                tracked = _TrackedOpenAISyncStream(
                    stream,
                    accumulator,
                    self._run.id,
                    self._name,
                    "llm",
                    accumulator.add_event,
                    accumulator.should_emit_end,
                    accumulator.error,
                    accumulator.has_terminal_response,
                    self._claim_stream_terminal,
                )
                self._managed_stream = _ManagedOpenAISyncStream(
                    tracked,
                    self._run.id,
                    "llm",
                    self._name,
                    None,
                    self._claim_stream_terminal,
                )
        else:
            accumulator = OpenAIChatStreamAccumulator(
                self._kwargs.get("n", 1)
            )
            if self._async_client:
                tracked = _TrackedOpenAIAsyncStream(
                    stream,
                    accumulator,
                    self._run.id,
                    self._name,
                    "llm",
                    accumulator.add_chunk,
                    accumulator.has_terminal_choice_state,
                    lambda *, eof: _chat_stream_error(
                        accumulator, eof=eof
                    ),
                    terminal_claim=self._claim_stream_terminal,
                )
                self._managed_stream = _ManagedOpenAIAsyncStream(
                    tracked,
                    self._run.id,
                    "llm",
                    self._name,
                    None,
                    self._claim_stream_terminal,
                )
            else:
                tracked = _TrackedOpenAISyncStream(
                    stream,
                    accumulator,
                    self._run.id,
                    self._name,
                    "llm",
                    accumulator.add_chunk,
                    accumulator.has_terminal_choice_state,
                    lambda *, eof: _chat_stream_error(
                        accumulator, eof=eof
                    ),
                    terminal_claim=self._claim_stream_terminal,
                )
                self._managed_stream = _ManagedOpenAISyncStream(
                    tracked,
                    self._run.id,
                    "llm",
                    self._name,
                    None,
                    self._claim_stream_terminal,
                )

        self._managed_streams[stream_key] = self._managed_stream
        self._link_managed_stream_response(stream)
        return self._managed_stream

    def _claim_stream_terminal(self):
        if self._finished:
            return False
        self._finished = True
        return True

    def _link_managed_stream_response(self, stream):
        response = getattr(stream, "response", None)
        if response is None:
            return

        self._managed_stream._response_proxy = response
        response_key = id(response)
        if response_key in self._linked_stream_responses:
            return
        self._linked_stream_responses.add(response_key)
        close_name = "aclose" if self._async_client else "close"
        close = getattr(response, close_name, None)
        if not callable(close):
            return

        @wraps(close)
        def tracked_response_close(*args, **kwargs):
            tracked_streams = (
                getattr(managed, "_stream", None)
                for managed in self._managed_streams.values()
            )
            if self._finished or any(
                getattr(tracked, "_provider_operation_active", False)
                or getattr(tracked, "_terminal_emitted", False)
                for tracked in tracked_streams
            ):
                return close(*args, **kwargs)
            return self._managed_stream.close()

        try:
            setattr(response, close_name, tracked_response_close)
        except Exception as error:
            logger.exception(error)

    def parsed(self, response):
        if self._kwargs.get("stream") is True and (
            hasattr(response, "__aiter__")
            if self._async_client
            else hasattr(response, "__iter__")
        ):
            return self._manage_parsed_stream(response)
        self._track_parsed_response(response)
        return response

    def _managed_stream_terminal_emitted(self):
        if self._managed_stream is None:
            return False
        tracked = getattr(self._managed_stream, "_stream", None)
        return bool(getattr(tracked, "_terminal_emitted", False))

    def instrument(self, response):
        parse = getattr(response, "parse", None)
        if callable(parse):

            @wraps(parse)
            def tracked_parse(*args, **kwargs):
                try:
                    parsed = parse(*args, **kwargs)
                except BaseException:
                    self.track_provider_error()
                    raise

                if isawaitable(parsed):

                    async def await_and_track():
                        try:
                            result = await parsed
                        except BaseException:
                            self.track_provider_error()
                            raise
                        return self.parsed(result)

                    return await_and_track()
                return self.parsed(parsed)

            try:
                response.parse = tracked_parse
            except Exception as error:
                logger.exception(error)

        close = getattr(response, "close", None)
        if callable(close):

            @wraps(close)
            def tracked_close(*args, **kwargs):
                if self._closing_managed_stream or self._finished:
                    return close(*args, **kwargs)

                if self._managed_stream_terminal_emitted():
                    self._finished = True
                    return close(*args, **kwargs)

                if self._managed_stream is not None:
                    self._closing_managed_stream = True
                    try:
                        result = self._managed_stream.close()
                    finally:
                        self._closing_managed_stream = False
                    if isawaitable(result):

                        async def await_managed_close():
                            try:
                                return await result
                            finally:
                                if self._managed_stream_terminal_emitted():
                                    self._finished = True

                        return await_managed_close()
                    if self._managed_stream_terminal_emitted():
                        self._finished = True
                    return result

                try:
                    result = close(*args, **kwargs)
                except BaseException:
                    self.track_provider_error()
                    raise

                if isawaitable(result):

                    async def await_close_and_track():
                        try:
                            close_result = await result
                        except BaseException:
                            self.track_provider_error()
                            raise
                        self._track_error(
                            _raw_response_unparsed_error(
                                streamed_response=self._streamed_response
                            )
                        )
                        return close_result

                    return await_close_and_track()

                self._track_error(
                    _raw_response_unparsed_error(
                        streamed_response=self._streamed_response
                    )
                )
                return result

            try:
                response.close = tracked_close
            except Exception as error:
                logger.exception(error)

        return response


def _wrap_openai_raw_response_method(
    fn,
    *,
    input_parser,
    output_parser,
    openai_iterable_fields=(),
    responses_api=False,
    async_client=False,
    stream_only=False,
):
    if getattr(fn, "_lunary_deferred_response_wrapper", False):
        return fn

    if async_client:

        @wraps(fn)
        async def async_wrapper(*args, **kwargs):
            if stream_only and kwargs.get("stream") is not True:
                return await fn(*args, **kwargs)
            tracker = _OpenAIDeferredResponseTracker(
                args,
                kwargs,
                input_parser=input_parser,
                output_parser=output_parser,
                openai_iterable_fields=openai_iterable_fields,
                responses_api=responses_api,
                async_client=True,
                streamed_response=False,
            )
            tracker.materialize_iterables()
            tracker.start_request()
            try:
                response = await fn(*args, **tracker.provider_kwargs)
            except BaseException:
                tracker.track_provider_error()
                raise
            finally:
                tracker.end_request_scope()
            return tracker.instrument(response)

        async_wrapper._lunary_deferred_response_wrapper = True
        return async_wrapper

    @wraps(fn)
    def sync_wrapper(*args, **kwargs):
        if stream_only and kwargs.get("stream") is not True:
            return fn(*args, **kwargs)
        tracker = _OpenAIDeferredResponseTracker(
            args,
            kwargs,
            input_parser=input_parser,
            output_parser=output_parser,
            openai_iterable_fields=openai_iterable_fields,
            responses_api=responses_api,
            async_client=False,
            streamed_response=False,
        )
        tracker.materialize_iterables()
        tracker.start_request()
        try:
            response = fn(*args, **tracker.provider_kwargs)
        except BaseException:
            tracker.track_provider_error()
            raise
        finally:
            tracker.end_request_scope()
        return tracker.instrument(response)

    sync_wrapper._lunary_deferred_response_wrapper = True
    return sync_wrapper


def _wrap_openai_streaming_response_method(
    fn,
    *,
    input_parser,
    output_parser,
    openai_iterable_fields=(),
    responses_api=False,
    async_client=False,
    stream_only=False,
):
    if getattr(fn, "_lunary_deferred_response_wrapper", False):
        return fn

    @wraps(fn)
    def wrapper(*args, **kwargs):
        if stream_only and kwargs.get("stream") is not True:
            return fn(*args, **kwargs)
        tracker = _OpenAIDeferredResponseTracker(
            args,
            kwargs,
            input_parser=input_parser,
            output_parser=output_parser,
            openai_iterable_fields=openai_iterable_fields,
            responses_api=responses_api,
            async_client=async_client,
            streamed_response=True,
        )
        manager = fn(*args, **tracker.provider_kwargs)

        if async_client:
            api_request = getattr(manager, "_api_request", None)
            if api_request is None:
                return manager
            close_request = getattr(api_request, "close", None)
            if callable(close_request):
                close_request()

            async def tracked_request():
                tracker.materialize_iterables()
                tracker.start_request()
                try:
                    request_manager = fn(
                        *args, **tracker.provider_kwargs
                    )
                    request = getattr(
                        request_manager, "_api_request", request_manager
                    )
                    response = await request
                except BaseException:
                    tracker.track_provider_error()
                    raise
                finally:
                    tracker.end_request_scope()
                return tracker.instrument(response)

            manager._api_request = tracked_request()
            return manager

        request_func = getattr(manager, "_request_func", None)
        if not callable(request_func):
            return manager

        @wraps(request_func)
        def tracked_request():
            tracker.materialize_iterables(request_func)
            tracker.start_request()
            try:
                response = request_func()
            except BaseException:
                tracker.track_provider_error()
                raise
            finally:
                tracker.end_request_scope()
            return tracker.instrument(response)

        manager._request_func = tracked_request
        return manager

    wrapper._lunary_deferred_response_wrapper = True
    return wrapper


def _monitor_openai_raw_response_surfaces(
    resource,
    *,
    input_parser,
    output_parser,
    openai_iterable_fields=(),
    responses_api=False,
    async_client=False,
    method_names=("create", "parse"),
    method_input_parsers=None,
    stream_only_method_names=(),
):
    try:
        raw_resource = getattr(resource, "with_raw_response", None)
    except Exception:
        raw_resource = None
    try:
        streaming_resource = getattr(
            resource, "with_streaming_response", None
        )
    except Exception:
        streaming_resource = None

    for method_name in method_names:
        method_input_parser = (
            (method_input_parsers or {}).get(method_name, input_parser)
        )
        stream_only = method_name in stream_only_method_names
        raw_method = getattr(raw_resource, method_name, None)
        if callable(raw_method):
            try:
                setattr(
                    raw_resource,
                    method_name,
                    _wrap_openai_raw_response_method(
                        raw_method,
                        input_parser=method_input_parser,
                        output_parser=output_parser,
                        openai_iterable_fields=openai_iterable_fields,
                        responses_api=responses_api,
                        async_client=async_client,
                        stream_only=stream_only,
                    ),
                )
            except Exception as error:
                logger.exception(error)

        streaming_method = getattr(
            streaming_resource, method_name, None
        )
        if callable(streaming_method):
            try:
                setattr(
                    streaming_resource,
                    method_name,
                    _wrap_openai_streaming_response_method(
                        streaming_method,
                        input_parser=method_input_parser,
                        output_parser=output_parser,
                        openai_iterable_fields=openai_iterable_fields,
                        responses_api=responses_api,
                        async_client=async_client,
                        stream_only=stream_only,
                    ),
                )
            except Exception as error:
                logger.exception(error)


def wrap(
    fn,
    type=None,
    run_id=None,
    name=None,
    user_id=None,
    user_props=None,
    tags=None,
    input_parser=default_input_parser,
    output_parser=default_output_parser,
    app_id=None,
    stream: bool = False,
    preserve_metadata: bool = False,
    stream_passthrough: bool = False,
    stream_handler=default_stream_handler, # TODO: this is not the default, it's only used for OpenAI, so pass it directly in monitor()
    openai_metadata: bool = False,
    openai_iterable_fields=(),
):
    def sync_wrapper(*args, **kwargs):
        _restore_openai_stream_lunary_controls(kwargs)
        if openai_iterable_fields:
            _materialize_openai_iterables(kwargs, openai_iterable_fields)
        output = None
        should_stream = stream or kwargs.get("stream", False)
        parsed_input = {"name": name, "input": None}

        parent_run_id = kwargs.pop("parent", run_manager.current_run_id)
        explicit_user_id = kwargs.pop("user_id", None)
        explicit_user_props = kwargs.pop("user_props", None)
        explicit_tags = kwargs.pop("tags", None)
        run = run_manager.start_run(run_id, parent_run_id)
        stream_run_managed = False

        try:
            try:
                metadata = _extract_call_metadata(
                    kwargs,
                    preserve_metadata=preserve_metadata,
                    openai_metadata=openai_metadata,
                )
                params = filter_params(kwargs)
                parsed_input = input_parser(*args, **kwargs)
                params = _merge_parsed_input_params(params, parsed_input)

                track_event(
                    type,
                    "start",
                    run_id=run.id,
                    parent_run_id=parent_run_id,
                    input=parsed_input["input"],
                    name=name or parsed_input["name"],
                    user_id=explicit_user_id or user_ctx.get() or user_id,
                    user_props=explicit_user_props
                    or user_props
                    or user_props_ctx.get(),
                    params=params,
                    metadata=metadata,
                    tags=explicit_tags or tags or tags_ctx.get(),
                    template_id=_extract_template_version_id(kwargs),
                    app_id=app_id,
                )
            except Exception as e:
                logger.exception(e)

            if should_stream == True:
                try:
                    stream_obj = stream_handler(
                        fn, run.id, name or parsed_input["name"], type, *args, **kwargs
                    )
                    stream_run_managed = True
                except Exception as e:
                    track_event(
                        type,
                        "error",
                        run.id,
                        error=_stream_entry_error_payload(
                            e,
                            stream_handler=stream_handler,
                            openai_metadata=openai_metadata,
                        ),
                        app_id=app_id,
                    )
                    raise e

                if stream_passthrough:
                    return stream_obj

                if isinstance(stream_obj, _TrackedOpenAISyncStream):
                    managed_stream = _ManagedOpenAISyncStream(
                        stream_obj,
                        run.id,
                        type,
                        name or parsed_input["name"],
                        app_id,
                    )
                    run_manager.end_run(run.id)
                    return managed_stream

                def tracked_stream():
                    try:
                        for chunk in stream_obj:
                            yield chunk
                    except Exception as e:
                        track_event(
                            type,
                            "error",
                            run.id,
                            error={"message": str(e), "stack": traceback.format_exc()},
                            app_id=app_id,
                        )
                        raise e
                    finally:
                        try:
                            close = getattr(stream_obj, "close", None)
                            if callable(close):
                                close()
                        finally:
                            run_manager.end_run(run.id)

                return tracked_stream()

            try:
                output = fn(*args, **kwargs)

            except Exception as e:
                track_event(
                    type,
                    "error",
                    run.id,
                    error={"message": str(e), "stack": traceback.format_exc()},
                    app_id=app_id,
                )

                # rethrow error
                raise e

            try:
                parsed_output = output_parser(output, stream)

                track_event(
                    type,
                    "end",
                    run.id,
                    name=name
                    or parsed_input[
                        "name"
                    ],  # Need name in case need to compute tokens usage server side
                    output=parsed_output["output"],
                    token_usage=parsed_output["tokensUsage"],
                    metadata=parsed_output.get("metadata"),
                    app_id=app_id
                )
                return output
            except Exception as e:
                logger.exception(e)
            finally:
                return output
        finally:
            if not stream_run_managed:
                run_manager.end_run(run.id)

    return sync_wrapper


def async_wrap(
    fn,
    type=None,
    name=None,
    user_id=None,
    user_props=None,
    tags=None,
    input_parser=default_input_parser,
    output_parser=default_output_parser,
    app_id=None,
    stream: bool = False,
    preserve_metadata: bool = False,
    stream_passthrough: bool = False,
    stream_handler=async_stream_handler,
    openai_metadata: bool = False,
    openai_iterable_fields=(),
):
    async def wrapper(*args, **kwargs):
        _restore_openai_stream_lunary_controls(kwargs)
        if openai_iterable_fields:
            _materialize_openai_iterables(kwargs, openai_iterable_fields)

        async def async_wrapper(*args, **kwargs):
            output = None
            parsed_input = {"name": name, "input": None}

            parent_run_id = kwargs.pop("parent", run_manager.current_run_id)
            explicit_user_id = kwargs.pop("user_id", None)
            explicit_user_props = kwargs.pop("user_props", None)
            explicit_tags = kwargs.pop("tags", None)
            run = run_manager.start_run(parent_run_id=parent_run_id)


            try:
                try:
                    metadata = _extract_call_metadata(
                        kwargs,
                        preserve_metadata=preserve_metadata,
                        openai_metadata=openai_metadata,
                    )
                    params = filter_params(kwargs)
                    parsed_input = input_parser(*args, **kwargs)
                    params = _merge_parsed_input_params(params, parsed_input)

                    track_event(
                        type,
                        "start",
                        run_id=run.id,
                        parent_run_id=parent_run_id,
                        input=parsed_input["input"],
                        name=name or parsed_input["name"],
                        user_id=explicit_user_id or user_ctx.get() or user_id,
                        user_props=explicit_user_props
                        or user_props
                        or user_props_ctx.get(),
                        params=params,
                        metadata=metadata,
                        tags=explicit_tags or tags or tags_ctx.get(),
                        template_id=_extract_template_version_id(kwargs),
                        app_id=app_id,
                    )
                except Exception as e:
                    logger.exception(e)

                try:
                    output = await fn(*args, **kwargs)

                except Exception as e:
                    track_event(
                        type,
                        "error",
                        run.id,
                        error={"message": str(e), "stack": traceback.format_exc()},
                        app_id=app_id,
                    )

                    # rethrow error
                    raise e

                try:
                    parsed_output = output_parser(output, kwargs.get("stream", False))

                    track_event(
                        type,
                        "end",
                        run.id,
                        name=name
                        or parsed_input[
                            "name"
                        ],  # Need name in case need to compute tokens usage server side
                        output=parsed_output["output"],
                        token_usage=parsed_output["tokensUsage"],
                        metadata=parsed_output.get("metadata"),
                        app_id=app_id
                    )
                    return output
                except Exception as e:
                    logger.exception(e)
                finally:
                    return output
            finally:
                run_manager.end_run(run.id)

        async def async_stream_wrapper(*args, **kwargs):
            parent_run_id = kwargs.pop("parent", run_manager.current_run_id)
            explicit_user_id = kwargs.pop("user_id", None)
            explicit_user_props = kwargs.pop("user_props", None)
            explicit_tags = kwargs.pop("tags", None)
            run = run_manager.start_run(parent_run_id=parent_run_id)
            parsed_input = {"name": name, "input": None}
            stream_run_managed = False

            try:
                try:
                    metadata = _extract_call_metadata(
                        kwargs,
                        preserve_metadata=preserve_metadata,
                        openai_metadata=openai_metadata,
                    )
                    params = filter_params(kwargs)
                    parsed_input = input_parser(*args, **kwargs)
                    params = _merge_parsed_input_params(params, parsed_input)

                    track_event(
                        type,
                        "start",
                        run_id=run.id,
                        parent_run_id=parent_run_id,
                        input=parsed_input["input"],
                        name=name or parsed_input["name"],
                        user_id=explicit_user_id or user_ctx.get() or user_id,
                        user_props=explicit_user_props
                        or user_props
                        or user_props_ctx.get(),
                        tags=explicit_tags or tags or tags_ctx.get(),
                        params=params,
                        metadata=metadata,
                        template_id=_extract_template_version_id(kwargs),
                        app_id=app_id
                    )
                except Exception as e:
                    logger.exception(e)

                try:
                    stream_obj = stream_handler(
                        fn, run.id, name or parsed_input["name"], type, *args, **kwargs
                    )
                    if isawaitable(stream_obj):
                        stream_obj = await stream_obj
                    stream_run_managed = True
                except Exception as e:
                    track_event(
                        type,
                        "error",
                        run.id,
                        error=_stream_entry_error_payload(
                            e,
                            stream_handler=stream_handler,
                            openai_metadata=openai_metadata,
                        ),
                        app_id=app_id,
                    )
                    raise e

                if stream_passthrough:
                    return stream_obj

                if isinstance(stream_obj, _TrackedOpenAIAsyncStream):
                    managed_stream = _ManagedOpenAIAsyncStream(
                        stream_obj,
                        run.id,
                        type,
                        name or parsed_input["name"],
                        app_id,
                    )
                    run_manager.end_run(run.id)
                    return managed_stream

                async def tracked_stream():
                    try:
                        async for chunk in stream_obj:
                            yield chunk
                    except Exception as e:
                        track_event(
                            type,
                            "error",
                            run.id,
                            error={"message": str(e), "stack": traceback.format_exc()},
                            app_id=app_id,
                        )
                        raise e
                    finally:
                        try:
                            close = getattr(stream_obj, "aclose", None)
                            if not callable(close):
                                close = getattr(stream_obj, "close", None)
                            if callable(close):
                                close_result = close()
                                if isawaitable(close_result):
                                    await close_result
                        finally:
                            run_manager.end_run(run.id)

                return tracked_stream()
            finally:
                if not stream_run_managed:
                    run_manager.end_run(run.id)

        should_stream = stream or kwargs.get("stream", False)
        if should_stream == True:
            return await async_stream_wrapper(*args, **kwargs)
        else:
            return await async_wrapper(*args, **kwargs)

    return wrapper


def _wrap_openai_responses_retrieve(fn):
    tracked = wrap(
        fn,
        "llm",
        input_parser=OpenAIResponsesUtils.parse_retrieve_input,
        output_parser=OpenAIResponsesUtils.parse_output,
        stream_handler=openai_responses_stream_handler,
    )

    @wraps(fn)
    def wrapper(*args, **kwargs):
        if kwargs.get("stream") is True:
            return tracked(*args, **kwargs)
        return fn(*args, **kwargs)

    return wrapper


def _wrap_async_openai_responses_retrieve(fn):
    tracked = async_wrap(
        fn,
        "llm",
        input_parser=OpenAIResponsesUtils.parse_retrieve_input,
        output_parser=OpenAIResponsesUtils.parse_output,
        stream_handler=async_openai_responses_stream_handler,
    )

    @wraps(fn)
    async def wrapper(*args, **kwargs):
        if kwargs.get("stream") is True:
            return await tracked(*args, **kwargs)
        return await fn(*args, **kwargs)

    return wrapper


def monitor(object):
    try:
        package_name = object.__class__.__module__.split(".")[0]

        if package_name == "ibm_watsonx_ai":
            installed_version = importlib.metadata.version("ibm-watsonx-ai")
            if version.parse(installed_version) >= version.parse("1.0.0"):
                model_name= object.model_id.split('/')[1]
                object.chat = wrap(
                    object.chat,
                    "llm",
                    input_parser=IBMUtils.parse_input,
                    output_parser=IBMUtils.parse_output,
                    name=model_name,
                )
                object.chat_stream = wrap(
                    object.chat_stream,
                    "llm",
                    input_parser=IBMUtils.parse_input,
                    output_parser=IBMUtils.parse_output,
                    name=model_name,
                    stream=True,
                    stream_handler=ibm_stream_handler,
                )
                object.achat = async_wrap(
                    object.achat,
                    "llm",
                    input_parser=IBMUtils.parse_input,
                    output_parser=IBMUtils.parse_output,
                    name=model_name,
                )
            else:
                logger.warning("Version 1.0.0 or higher of ibm-watsonx-ai is required")
            return

        if package_name == "openai":    
            installed_version = importlib.metadata.version("openai")
            if version.parse(installed_version) >= version.parse("1.0.0"):
                client_name = getattr(type(object), "__name__", None)
                if client_name == "openai" or client_name == "OpenAI" or client_name == "AzureOpenAI":
                    try:
                        _monitor_openai_raw_response_surfaces(
                            object.chat.completions,
                            input_parser=OpenAIUtils.parse_input,
                            output_parser=OpenAIUtils.parse_output,
                            openai_iterable_fields=(
                                "messages",
                                "tools",
                                "functions",
                            ),
                        )
                        object.chat.completions.create = wrap(
                            object.chat.completions.create,
                            "llm",
                            input_parser=OpenAIUtils.parse_input,
                            output_parser=OpenAIUtils.parse_output,
                            openai_metadata=True,
                            openai_iterable_fields=(
                                "messages",
                                "tools",
                                "functions",
                            ),
                        )
                        chat_parse = getattr(
                            object.chat.completions, "parse", None
                        )
                        if callable(chat_parse):
                            object.chat.completions.parse = wrap(
                                chat_parse,
                                "llm",
                                input_parser=OpenAIUtils.parse_input,
                                output_parser=OpenAIUtils.parse_output,
                                openai_metadata=True,
                                openai_iterable_fields=(
                                    "messages",
                                    "tools",
                                    "functions",
                                ),
                            )
                        chat_stream = getattr(
                            object.chat.completions, "stream", None
                        )
                        if callable(chat_stream):
                            object.chat.completions.stream = (
                                _wrap_openai_stream_metadata(chat_stream)
                            )
                    except Exception as e:
                        logger.warning(
                            "Please use `lunary.monitor(openai)` or `lunary.monitor(client)` after setting the OpenAI api key"
                        )

                    responses_api = getattr(object, "responses", None)
                    if callable(getattr(responses_api, "create", None)):
                        _monitor_openai_raw_response_surfaces(
                            responses_api,
                            input_parser=OpenAIResponsesUtils.parse_input,
                            output_parser=OpenAIResponsesUtils.parse_output,
                            openai_iterable_fields=("tools",),
                            responses_api=True,
                            method_names=("create", "parse", "retrieve"),
                            method_input_parsers={
                                "retrieve": OpenAIResponsesUtils.parse_retrieve_input
                            },
                            stream_only_method_names=("retrieve",),
                        )
                        object.responses.create = wrap(
                            object.responses.create,
                            "llm",
                            input_parser=OpenAIResponsesUtils.parse_input,
                            output_parser=OpenAIResponsesUtils.parse_output,
                            openai_metadata=True,
                            stream_handler=openai_responses_stream_handler,
                            openai_iterable_fields=("tools",),
                        )
                    responses_parse = getattr(responses_api, "parse", None)
                    if callable(responses_parse):
                        object.responses.parse = wrap(
                            responses_parse,
                            "llm",
                            input_parser=OpenAIResponsesUtils.parse_input,
                            output_parser=OpenAIResponsesUtils.parse_output,
                            openai_metadata=True,
                            openai_iterable_fields=("tools",),
                        )
                    responses_retrieve = getattr(
                        responses_api, "retrieve", None
                    )
                    if callable(responses_retrieve):
                        object.responses.retrieve = (
                            _wrap_openai_responses_retrieve(
                                responses_retrieve
                            )
                        )
                    responses_stream = getattr(responses_api, "stream", None)
                    if callable(responses_stream):
                        object.responses.stream = (
                            _wrap_openai_stream_metadata(responses_stream)
                        )
                elif client_name == "AsyncOpenAI" or client_name == "AsyncAzureOpenAI":
                    _monitor_openai_raw_response_surfaces(
                        object.chat.completions,
                        input_parser=OpenAIUtils.parse_input,
                        output_parser=OpenAIUtils.parse_output,
                        openai_iterable_fields=(
                            "messages",
                            "tools",
                            "functions",
                        ),
                        async_client=True,
                    )
                    object.chat.completions.create = async_wrap(
                        object.chat.completions.create,
                        "llm",
                        input_parser=OpenAIUtils.parse_input,
                        output_parser=OpenAIUtils.parse_output,
                        openai_metadata=True,
                        openai_iterable_fields=(
                            "messages",
                            "tools",
                            "functions",
                        ),
                    )
                    chat_parse = getattr(
                        object.chat.completions, "parse", None
                    )
                    if callable(chat_parse):
                        object.chat.completions.parse = async_wrap(
                            chat_parse,
                            "llm",
                            input_parser=OpenAIUtils.parse_input,
                            output_parser=OpenAIUtils.parse_output,
                            openai_metadata=True,
                            openai_iterable_fields=(
                                "messages",
                                "tools",
                                "functions",
                            ),
                        )
                    chat_stream = getattr(
                        object.chat.completions, "stream", None
                    )
                    if callable(chat_stream):
                        object.chat.completions.stream = (
                            _wrap_openai_stream_metadata(chat_stream)
                        )

                    responses_api = getattr(object, "responses", None)
                    if callable(getattr(responses_api, "create", None)):
                        _monitor_openai_raw_response_surfaces(
                            responses_api,
                            input_parser=OpenAIResponsesUtils.parse_input,
                            output_parser=OpenAIResponsesUtils.parse_output,
                            openai_iterable_fields=("tools",),
                            responses_api=True,
                            async_client=True,
                            method_names=("create", "parse", "retrieve"),
                            method_input_parsers={
                                "retrieve": OpenAIResponsesUtils.parse_retrieve_input
                            },
                            stream_only_method_names=("retrieve",),
                        )
                        object.responses.create = async_wrap(
                            object.responses.create,
                            "llm",
                            input_parser=OpenAIResponsesUtils.parse_input,
                            output_parser=OpenAIResponsesUtils.parse_output,
                            openai_metadata=True,
                            stream_handler=async_openai_responses_stream_handler,
                            openai_iterable_fields=("tools",),
                        )
                    responses_parse = getattr(responses_api, "parse", None)
                    if callable(responses_parse):
                        object.responses.parse = async_wrap(
                            responses_parse,
                            "llm",
                            input_parser=OpenAIResponsesUtils.parse_input,
                            output_parser=OpenAIResponsesUtils.parse_output,
                            openai_metadata=True,
                            openai_iterable_fields=("tools",),
                        )
                    responses_retrieve = getattr(
                        responses_api, "retrieve", None
                    )
                    if callable(responses_retrieve):
                        object.responses.retrieve = (
                            _wrap_async_openai_responses_retrieve(
                                responses_retrieve
                            )
                        )
                    responses_stream = getattr(responses_api, "stream", None)
                    if callable(responses_stream):
                        object.responses.stream = (
                            _wrap_openai_stream_metadata(responses_stream)
                        )
                return

        if package_name == "anthropic":
            client_name = getattr(type(object), "__name__", None)
            messages_api = getattr(object, "messages", None)
            create_fn = getattr(messages_api, "create", None)

            if not callable(create_fn):
                return

            if client_name and client_name.startswith("Async"):
                object.messages.create = async_wrap(
                    object.messages.create,
                    "llm",
                    input_parser=AnthropicUtils.parse_input,
                    output_parser=AnthropicUtils.parse_output,
                    preserve_metadata=True,
                    stream_passthrough=True,
                    stream_handler=async_anthropic_stream_handler,
                )
                if callable(getattr(messages_api, "parse", None)):
                    object.messages.parse = async_wrap(
                        object.messages.parse,
                        "llm",
                        input_parser=AnthropicUtils.parse_input,
                        output_parser=AnthropicUtils.parse_output,
                        preserve_metadata=True,
                    )
                if callable(getattr(messages_api, "stream", None)):
                    object.messages.stream = wrap_async_anthropic_stream_manager(
                        object.messages.stream,
                        "llm",
                        input_parser=AnthropicUtils.parse_input,
                        output_parser=AnthropicUtils.parse_output,
                        preserve_metadata=True,
                    )
            else:
                object.messages.create = wrap(
                    object.messages.create,
                    "llm",
                    input_parser=AnthropicUtils.parse_input,
                    output_parser=AnthropicUtils.parse_output,
                    preserve_metadata=True,
                    stream_passthrough=True,
                    stream_handler=anthropic_stream_handler,
                )
                if callable(getattr(messages_api, "parse", None)):
                    object.messages.parse = wrap(
                        object.messages.parse,
                        "llm",
                        input_parser=AnthropicUtils.parse_input,
                        output_parser=AnthropicUtils.parse_output,
                        preserve_metadata=True,
                    )
                if callable(getattr(messages_api, "stream", None)):
                    object.messages.stream = wrap_anthropic_stream_manager(
                        object.messages.stream,
                        "llm",
                        input_parser=AnthropicUtils.parse_input,
                        output_parser=AnthropicUtils.parse_output,
                        preserve_metadata=True,
                    )

            beta_messages_api = getattr(getattr(object, "beta", None), "messages", None)
            if beta_messages_api is not None:
                if client_name and client_name.startswith("Async"):
                    if callable(getattr(beta_messages_api, "create", None)):
                        object.beta.messages.create = async_wrap(
                            object.beta.messages.create,
                            "llm",
                            input_parser=AnthropicUtils.parse_input,
                            output_parser=AnthropicUtils.parse_output,
                            preserve_metadata=True,
                            stream_passthrough=True,
                            stream_handler=async_anthropic_stream_handler,
                        )
                    if callable(getattr(beta_messages_api, "parse", None)):
                        object.beta.messages.parse = async_wrap(
                            object.beta.messages.parse,
                            "llm",
                            input_parser=AnthropicUtils.parse_input,
                            output_parser=AnthropicUtils.parse_output,
                            preserve_metadata=True,
                        )
                    if callable(getattr(beta_messages_api, "stream", None)):
                        object.beta.messages.stream = wrap_async_anthropic_stream_manager(
                            object.beta.messages.stream,
                            "llm",
                            input_parser=AnthropicUtils.parse_input,
                            output_parser=AnthropicUtils.parse_output,
                            preserve_metadata=True,
                        )
                    if callable(getattr(beta_messages_api, "tool_runner", None)):
                        object.beta.messages.tool_runner = wrap_async_anthropic_tool_runner(
                            object.beta.messages.tool_runner
                        )
                else:
                    if callable(getattr(beta_messages_api, "create", None)):
                        object.beta.messages.create = wrap(
                            object.beta.messages.create,
                            "llm",
                            input_parser=AnthropicUtils.parse_input,
                            output_parser=AnthropicUtils.parse_output,
                            preserve_metadata=True,
                            stream_passthrough=True,
                            stream_handler=anthropic_stream_handler,
                        )
                    if callable(getattr(beta_messages_api, "parse", None)):
                        object.beta.messages.parse = wrap(
                            object.beta.messages.parse,
                            "llm",
                            input_parser=AnthropicUtils.parse_input,
                            output_parser=AnthropicUtils.parse_output,
                            preserve_metadata=True,
                        )
                    if callable(getattr(beta_messages_api, "stream", None)):
                        object.beta.messages.stream = wrap_anthropic_stream_manager(
                            object.beta.messages.stream,
                            "llm",
                            input_parser=AnthropicUtils.parse_input,
                            output_parser=AnthropicUtils.parse_output,
                            preserve_metadata=True,
                        )
                    if callable(getattr(beta_messages_api, "tool_runner", None)):
                        object.beta.messages.tool_runner = wrap_anthropic_tool_runner(
                            object.beta.messages.tool_runner
                        )
            return
    except PackageNotFoundError:
        logger.warning(
            "You need to install a supported client package such as `openai`, `anthropic`, or `ibm-watsonx-ai` to monitor your LLM calls."
        )


def agent(name=None, user_id=None, user_props=None, tags=None, app_id=None):
    def decorator(fn):
        return wrap(
            fn,
            "agent",
            name=name or fn.__name__,
            user_id=user_id,
            user_props=user_props,
            tags=tags,
            input_parser=default_input_parser,
            app_id=app_id
        )

    return decorator

def chain(
    name: Optional[str] = None,
    user_id: Optional[str] = None,
    user_props: Optional[dict] = None,
    tags: Optional[list] = None,
    app_id: Optional[str] = None,
    input_arg: Optional[str] = None
):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            if input_arg is not None:
                from inspect import signature
                sig = signature(fn)
                param_names = list(sig.parameters.keys())
                
                input_value = None
                
                if input_arg in param_names:
                    arg_index = param_names.index(input_arg)
                    if arg_index < len(args):
                        input_value = args[arg_index]
                
                if input_arg in kwargs:
                    input_value = kwargs[input_arg]
                
                if input_value is None:
                    raise ValueError(f"Specified input argument '{input_arg}' not found in function call")
                
                parsed_input = {"input": input_value}
            else:
                raw_input = default_input_parser(*args, **kwargs)
                parsed_input = {"input": raw_input}
            
            return wrap(
                fn,
                "chain",
                name=name or fn.__name__,
                user_id=user_id,
                user_props=user_props,
                tags=tags,
                input_parser=lambda *a, **kw: parsed_input,
                app_id=app_id
            )(*args, **kwargs)
        
        return wrapper
    return decorator

def class_chain(
    name: Optional[str] = None,
    user_id: Optional[str] = None,
    user_props: Optional[dict] = None,
    tags: Optional[list] = None,
    app_id: Optional[str | Callable] = None,
    input_arg: Optional[str] = None
):
    def decorator(fn):
        @wraps(fn)
        def wrapper(self, *args, **kwargs):
            actual_app_id = app_id(self) if callable(app_id) else app_id

            if input_arg is not None:
                sig = signature(fn)
                param_names = list(sig.parameters.keys())[1:]  # Skip 'self'
                
                input_value = None
                
                if input_arg in param_names:
                    arg_index = param_names.index(input_arg)
                    if arg_index < len(args):
                        input_value = args[arg_index]
                
                if input_arg in kwargs:
                    input_value = kwargs[input_arg]
                
                if input_value is None:
                    raise ValueError(f"Specified input argument '{input_arg}' not found in method call")
                
                parsed_input = {"input": input_value}
                custom_parser = lambda self, *a, **kw: parsed_input
            else:
                custom_parser = lambda self, *a, **kw: {"input": method_input_parser(self, *a, **kw)}

            return wrap(
                fn,
                "chain",
                name=name or fn.__name__,
                user_id=user_id,
                user_props=user_props,
                tags=tags,
                input_parser=custom_parser,
                app_id=actual_app_id
            )(self, *args, **kwargs)
        return wrapper
    return decorator

def tool(name=None, user_id=None, user_props=None, tags=None, app_id=None):
    def decorator(fn):
        return wrap(
            fn,
            "tool",
            name=name or fn.__name__,
            user_id=user_id,
            user_props=user_props,
            tags=tags,
            input_parser=default_input_parser,
            app_id=app_id
        )

    return decorator


try:
    import importlib.metadata
    import logging
    import os
    import traceback
    import warnings
    from contextvars import ContextVar
    from typing import Any, Dict, List, Union, cast, Sequence, Optional, TypedDict
    from uuid import UUID

    import requests
    from langchain_core.agents import AgentFinish
    from langchain_core.callbacks import BaseCallbackHandler
    from langchain_core.messages import BaseMessage, BaseMessageChunk, ToolMessage
    from langchain_core.documents import Document
    from langchain_core.outputs import LLMResult
    from langchain_core.load import dumps
    from packaging.version import parse


    DEFAULT_API_URL = "https://api.lunary.ai"

    user_ctx = ContextVar[Union[str, None]]("user_ctx", default=None)
    user_props_ctx = ContextVar[Union[str, None]]("user_props_ctx", default=None)

    spans: Dict[str, Any] = {}

    class UserContextManager:
        """Context manager for Lunary user context."""

        def __init__(self, user_id: str, user_props: Any = None) -> None:
            user_ctx.set(user_id)
            user_props_ctx.set(user_props)

        def __enter__(self) -> Any:
            pass

        def __exit__(self, exc_type: Any, exc_value: Any, exc_tb: Any) -> Any:
            user_ctx.set(None)
            user_props_ctx.set(None)

    def identify(user_id: str, user_props: Any = None) -> UserContextManager:
        """Builds a Lunary UserContextManager

        Parameters:
            - `user_id`: The user id.
            - `user_props`: The user properties.

        Returns:
            A context manager that sets the user context.
        """
        return UserContextManager(user_id, user_props)

    # Sentinel used to distinguish:
    # 1. LangChain did not provide `kwargs["inputs"]` at all
    # 2. LangChain did provide it, but the parsed value is `None`
    # We only backfill the chain end input in case (2).
    _MISSING = object()

    def _serialize(data: Any):
        if data is None:
            return None

        if hasattr(data, "messages"):
            return _serialize(data.messages)
        if isinstance(data, BaseMessage) or isinstance(data, BaseMessageChunk):
            return _parse_lc_message(data)
        elif isinstance(data, dict):
            return {key: _serialize(value) for key, value in data.items()}
        elif isinstance(data, list):
            if len(data) == 1:
                return _serialize(data[0])
            else:
                return [_serialize(item) for item in data]
        elif isinstance(data, (str, int, float, bool)):
            return data
        else:
            return dumps(data)

    def _parse_input(raw_input: Any) -> Any:
        serialized = _serialize(raw_input)
        if isinstance(serialized, dict):
            if "input" in serialized:
                return serialized["input"]

        return serialized

    def _parse_output(raw_output: dict) -> Any:
        serialized = _serialize(raw_output)
        if isinstance(serialized, dict):
            if "output" in serialized:
                return serialized["output"]

        return serialized

    def _parse_end_inputs(kwargs: Dict[str, Any]) -> Any:
        if "inputs" not in kwargs:
            return _MISSING

        return _parse_input(kwargs.get("inputs"))

    def _merge_langchain_invocation_params(
        invocation_params: Any, serialized: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Detach callback params and use serialized kwargs only as defaults."""
        params = (
            copy.deepcopy(invocation_params)
            if isinstance(invocation_params, dict)
            else {}
        )
        serialized_kwargs = serialized.get("kwargs", {})
        if not isinstance(serialized_kwargs, dict):
            return params
        for key, value in serialized_kwargs.items():
            params.setdefault(key, copy.deepcopy(value))
        return params

    def _parse_lc_role(
        role: str,
    ) -> str:
        if role == "human":
            return "user"
        elif role == "ai":
            return "assistant"
        else:
            return role

    def _get_user_id(metadata: Any) -> Any:
        if user_ctx.get() is not None:
            return user_ctx.get()

        metadata = metadata or {}
        user_id = metadata.get("user_id")
        return user_id

    def _get_user_props(metadata: Any) -> Any:
        if user_props_ctx.get() is not None:
            return user_props_ctx.get()

        metadata = metadata or {}
        return metadata.get("user_props", None)

    def _parse_tool_call(tool_call: Dict[str, Any]):
        arguments = tool_call.get("args")
        if not isinstance(arguments, str):
            arguments = json.dumps(
                arguments,
                sort_keys=True,
                separators=(",", ":"),
                ensure_ascii=False,
                allow_nan=False,
            )
        tool_call = {
            "id": tool_call.get("id"),
            "type": "function",
            "function": {
                "name": tool_call.get("name"),
                "arguments": arguments,
            },
        }
        return tool_call

    def _parse_tool_message(tool_message: ToolMessage):
        tool_message = {
            "role": "tool",
            "content": getattr(tool_message, "content", None),
            "name": getattr(tool_message, "name", None),
            "tool_call_id": getattr(tool_message, "tool_call_id", None),
        }
        return tool_message

    def _parse_lc_message(message: BaseMessage) -> Dict[str, Any]:
        if message.type == "tool":
            return _parse_tool_message(message)

        parsed = {"content": message.content, "role": _parse_lc_role(message.type)}

        # For tool calls in input
        tool_calls = getattr(message, "tool_calls", None)
        if tool_calls:
            parsed["tool_calls"] = [
                _parse_tool_call(tool_call) for tool_call in tool_calls
            ]

        # For tool calls in output
        keys = ["function_call", "tool_calls", "tool_call_id", "name"]
        parsed.update(
            {
                key: cast(Any, message.additional_kwargs.get(key))
                for key in keys
                if message.additional_kwargs.get(key) is not None
            }
        )

        return parsed

    def _parse_lc_messages(
        messages: Union[List[BaseMessage], Any]
    ) -> List[Dict[str, Any]]:
        return [_parse_lc_message(message) for message in messages]

    class IgnoreRule(TypedDict, total=False):
        type: str
        name: List[str]
        ignore_children: bool

    class LunaryCallbackHandler(BaseCallbackHandler):
        """Callback Handler for Lunary`.

        #### Parameters:
            - `app_id`: The app id of the app you want to report to. Defaults to
            `None`, which means that `LUNARY_PUBLIC_KEY` will be used.
            - `api_url`: The url of the Lunary API. Defaults to `None`,
            which means that either `LUNARY_API_URL` environment variable
            or `https://api.lunary.ai` will be used.
            - `ignore`: List of rules to filter out events. Each rule can specify:
                - `type`: The type of event to ignore (e.g., "agent", "tool", "llm", "chain")
                - `name`: List of names to ignore (supports wildcards with *)
                - `ignore_children`: Whether to ignore children of matching runs (default: True)
                Events matching these rules will not be sent to Lunary. By default, children
                of ignored runs are also ignored unless `ignore_children` is set to False.

        #### Raises:
            - `ValueError`: if `app_id` is not provided either as an
            argument or as an environment variable.
            - `ConnectionError`: if the connection to the API fails.


        #### Example:
        ```python
        from langchain_openai.chat_models import ChatOpenAI
        from lunary import LunaryCallbackHandler

        handler = LunaryCallbackHandler(ignore=[
            {"type": "agent", "name": ["ResearchAgent", "DebugAgent"]},
            {"type": "tool", "name": ["search_*", "debug_*"]},
            {"name": ["_internal_*"]},  # Matches any type
            {"type": "chain", "name": ["DebugChain"], "ignore_children": False}  # Ignore chain but track its children
        ])
        llm = ChatOpenAI(callbacks=[handler],
                    metadata={"userId": "user-123"})
        llm.predict("Hello, how are you?")
        ```
        """

        __app_id: str
        __api_url: str
        __ignore_rules: List[IgnoreRule]

        def __init__(
            self,
            app_id: Union[str, None] = None,
            api_url: Union[str, None] = None,
            ignore: Union[List[IgnoreRule], None] = None,
        ) -> None:
            super().__init__()
            config = get_config()
            try:
                import lunary

                self.__lunary_version = importlib.metadata.version("lunary")
                self.__track_event = lunary.track_event

            except ImportError:
                logger.warning(
                    """To use the Lunary callback handler you need to 
                    have the `lunary` Python package installed. Please install it 
                    with `pip install lunary`"""
                )
                self.__has_valid_config = False
                return

            if parse(self.__lunary_version) < parse("0.0.32"):
                logger.warning(
                    f"""The installed `lunary` version is
                    {self.__lunary_version}
                    but `LunaryCallbackHandler` requires at least version 0.1.1
                    upgrade `lunary` with `pip install --upgrade lunary`"""
                )
                self.__has_valid_config = False

            self.__has_valid_config = True

            self.__app_id = app_id or config.app_id
            if self.__app_id is None:
                logger.warning(
                    """app_id must be provided either as an argument or 
                    as an environment variable"""
                )
                self.__has_valid_config = False

            self.__api_url = api_url or config.api_url or None
            self.__ignore_rules = ignore or []

            self.queue = queue

            if self.__has_valid_config is False:
                return None

        def _get_matching_ignore_rule(self, run_type: str = None, name: str = None) -> Union[IgnoreRule, None]:
            """
            Find the first matching ignore rule for the given run type and name.
            Returns the matching rule or None if no match.
            """
            if not self.__ignore_rules:
                return None
                
            for rule in self.__ignore_rules:
                rule_type = rule.get("type")
                if rule_type == "agent":
                    rule_type = "chain"  # Agents are treated as chains in Lunary
                if rule_type and run_type and rule_type != run_type:
                    continue
                
                if "name" in rule and isinstance(rule["name"], list):
                    if name and self._matches_any_pattern(name, rule["name"]):
                        return rule
            
            return None

        def _should_ignore_run(self, run_id: str, run_type: str = None, name: str = None) -> bool:
            """
            Check if a run should be ignored based on filtering rules or parent hierarchy.
            Returns True if the run or any of its ancestors should be ignored.
            """
            # Check if this run matches any ignore rule
            matching_rule = self._get_matching_ignore_rule(run_type, name)
            if matching_rule:
                return True
            
            # Check parent hierarchy for inherited ignoring
            run = run_manager.runs.get(str(run_id))
            while run and run.parent_run_id:
                parent = run_manager.runs.get(run.parent_run_id)
                if parent and hasattr(parent, '_ignored') and parent._ignored:
                    # Check if parent has ignore_children=False
                    if hasattr(parent, '_ignore_children') and not parent._ignore_children:
                        # Parent is ignored but doesn't ignore children, so this run is not ignored
                        return False
                    return True
                run = parent
            
            return False
        
        def _matches_any_pattern(self, name: str, patterns: List[str]) -> bool:
            """Check if name matches any of the patterns (supports * wildcard)."""
            import fnmatch
            for pattern in patterns:
                if fnmatch.fnmatch(name, pattern):
                    return True
            return False

        def on_llm_start(
            self,
            serialized: Dict[str, Any],
            prompts: List[str],
            *,
            run_id: UUID,
            parent_run_id: Union[UUID, None] = None,
            tags: Union[List[str], None] = None,
            metadata: Union[Dict[str, Any], None] = None,
            **kwargs: Any,
        ) -> None:
            try:
                # if parent_run_id is None:
                #     parent_run_id = run_manager.current_run_id
                run = run_manager.start_run(run_id, parent_run_id)
                
                user_id = _get_user_id(metadata)
                user_props = _get_user_props(metadata)

                params = _merge_langchain_invocation_params(
                    kwargs.get("invocation_params"), serialized
                )

                name = (
                    metadata.get("model_name") # custom model name 
                    or metadata.get("ls_model_name") # for Azure OpenAI
                    or params.get("model")
                    or params.get("model_name")
                    or params.get("model_id")
                    or params.get("deployment_name")
                    or params.get("azure_deployment")
                )
                
                if self._should_ignore_run(run.id, run_type="llm"):
                    self.__track_event(
                        "llm",
                        "start",
                        run_id=run.id,
                        parent_run_id=run.parent_run_id,
                        name=name,
                        input="__NOT_INGESTED__",
                        output="__NOT_INGESTED__",
                        app_id=self.__app_id,
                        api_url=self.__api_url,
                        callback_queue=self.queue,
                        runtime="langchain-py",
                    )
                    return

                if not name and "anthropic" in params.get("_type"):
                    name = "claude-2"

                params = filter_params(params)
                input = _parse_input(prompts)

                self.__track_event(
                    "llm",
                    "start",
                    user_id=user_id,
                    run_id=run.id,
                    parent_run_id=run.parent_run_id,
                    name=name,
                    input=input,
                    tags=tags,
                    metadata=metadata,
                    params=params,
                    user_props=user_props,
                    app_id=self.__app_id,
                    api_url=self.__api_url,
                    callback_queue=self.queue,
                    runtime="langchain-py",
                )
            except Exception as e:
                logger.exception(f"An error occurred in `on_llm_start`: {e}")

        def on_chat_model_start(
            self,
            serialized: Dict[str, Any],
            messages: List[List[BaseMessage]],
            *,
            run_id: UUID,
            parent_run_id: Union[UUID, None] = None,
            tags: Union[List[str], None] = None,
            metadata: Union[Dict[str, Any], None] = None,
            **kwargs: Any,
        ) -> Any:
            try:
                # if parent_run_id is None:
                #     parent_run_id = run_manager.current_run_id
                run = run_manager.start_run(run_id, parent_run_id)
                
                user_id = _get_user_id(metadata)
                user_props = _get_user_props(metadata)

                params = _merge_langchain_invocation_params(
                    kwargs.get("invocation_params"), serialized
                )

                name = (
                    metadata.get("model_name") # custom model name
                    or metadata.get("ls_model_name") # for Azure OpenAI
                    or params.get("model")
                    or params.get("model_name")
                    or params.get("model_id")
                    or params.get("deployment_name")
                    or params.get("azure_deployment")
                )
                
                if self._should_ignore_run(run.id, run_type="llm"):
                    self.__track_event(
                        "llm",
                        "start",
                        run_id=run.id,
                        parent_run_id=run.parent_run_id,
                        name=name,
                        input="__NOT_INGESTED__",
                        output="__NOT_INGESTED__",
                        app_id=self.__app_id,
                        api_url=self.__api_url,
                        callback_queue=self.queue,
                        runtime="langchain-py",
                    )
                    return

                if not name and "anthropic" in params.get("_type"):
                    name = "claude-2"

                params = filter_params(params)
                input = _parse_lc_messages(messages[0])

                self.__track_event(
                    "llm",
                    "start",
                    user_id=user_id,
                    run_id=run.id,
                    parent_run_id=run.parent_run_id,
                    name=name,
                    input=input,
                    tags=tags,
                    metadata=metadata,
                    params=params,
                    user_props=user_props,
                    app_id=self.__app_id,
                    api_url=self.__api_url,
                    callback_queue=self.queue,
                    runtime="langchain-py",
                )
            except Exception as e:
                logger.exception(f"An error occurred in `on_chat_model_start`: {e}")

        def on_llm_end(
            self,
            response: LLMResult,
            *,
            run_id: UUID,
            parent_run_id: Union[UUID, None] = None,
            **kwargs: Any,
        ) -> None:
            try:
                if self._should_ignore_run(str(run_id), run_type="llm"):
                    self.__track_event(
                        "llm",
                        "end",
                        run_id=str(run_id),
                        input="__NOT_INGESTED__",
                        output="__NOT_INGESTED__",
                        app_id=self.__app_id,
                        api_url=self.__api_url,
                        callback_queue=self.queue,
                        runtime="langchain-py",
                    )
                    run_manager.end_run(run_id)
                    return
                    
                run_id = run_manager.end_run(run_id)

                token_usage = (response.llm_output or {}).get("token_usage", {})

                parsed_output: Any = [
                    (
                        _parse_lc_message(generation.message)
                        if hasattr(generation, "message")
                        else generation.text
                    )
                    for generation in response.generations[0]
                ]

                # if it's an array of 1, just parse the first element
                if len(parsed_output) == 1:
                    parsed_output = parsed_output[0]

                self.__track_event(
                    "llm",
                    "end",
                    run_id=run_id,
                    output=parsed_output,
                    token_usage={
                        "prompt": token_usage.get("prompt_tokens"),
                        "completion": token_usage.get("completion_tokens"),
                        "promptCached": token_usage.get("prompt_tokens_details", {}).get("cached_tokens", 0)
                    },
                    app_id=self.__app_id,
                    api_url=self.__api_url,
                    callback_queue=self.queue,
                    runtime="langchain-py",
                )
            except Exception as e:
                logger.exception(f"An error occurred in `on_llm_end`: {e}")

        def on_tool_start(
            self,
            serialized: Dict[str, Any],
            input_str: str,
            *,
            run_id: UUID,
            parent_run_id: Union[UUID, None] = None,
            tags: Union[List[str], None] = None,
            metadata: Union[Dict[str, Any], None] = None,
            **kwargs: Any,
        ) -> None:
            try:
                # if parent_run_id is None:
                #     parent_run_id = run_manager.current_run_id
                run = run_manager.start_run(run_id, parent_run_id)
                
                user_id = _get_user_id(metadata)
                user_props = _get_user_props(metadata)
                name = serialized.get("name")
                
                if self._should_ignore_run(run.id, run_type="tool", name=name):
                    self.__track_event(
                        "tool",
                        "start",
                        run_id=run.id,
                        parent_run_id=run.parent_run_id,
                        name=name,
                        input="__NOT_INGESTED__",
                        output="__NOT_INGESTED__",
                        app_id=self.__app_id,
                        api_url=self.__api_url,
                        callback_queue=self.queue,
                        runtime="langchain-py",
                    )
                    return

                self.__track_event(
                    "tool",
                    "start",
                    user_id=user_id,
                    run_id=run.id,
                    parent_run_id=run.parent_run_id,
                    name=name,
                    input=input_str,
                    tags=tags,
                    metadata=metadata,
                    user_props=user_props,
                    app_id=self.__app_id,
                    api_url=self.__api_url,
                    callback_queue=self.queue,
                    runtime="langchain-py",
                )
            except Exception as e:
                logger.exception(f"An error occurred in `on_tool_start`: {e}")

        def on_tool_end(
            self,
            output: str,
            *,
            run_id: UUID,
            parent_run_id: Union[UUID, None] = None,
            tags: Union[List[str], None] = None,
            **kwargs: Any,
        ) -> None:
            try:
                if self._should_ignore_run(str(run_id), run_type="tool"):
                    self.__track_event(
                        "tool",
                        "end",
                        run_id=str(run_id),
                        input="__NOT_INGESTED__",
                        output="__NOT_INGESTED__",
                        app_id=self.__app_id,
                        api_url=self.__api_url,
                        callback_queue=self.queue,
                        runtime="langchain-py",
                    )
                    run_manager.end_run(run_id)
                    return
                    
                run_id = run_manager.end_run(run_id)
                self.__track_event(
                    "tool",
                    "end",
                    run_id=run_id,
                    output=output,
                    app_id=self.__app_id,
                    api_url=self.__api_url,
                    callback_queue=self.queue,
                    runtime="langchain-py",
                )
            except Exception as e:
                logger.exception(f"An error occurred in `on_tool_end`: {e}")

        def on_chain_start(
            self,
            serialized: Dict[str, Any],
            inputs: Dict[str, Any],
            *args,
            run_id: UUID,
            parent_run_id: Union[UUID, None] = None,
            tags: Union[List[str], None] = None,
            metadata: Union[Dict[str, Any], None] = None,
            name: Union[str, None] = None,
            **kwargs: Any,
        ) -> Any:
            try:
                # if parent_run_id is None:
                #     parent_run_id = run_manager.current_run_id
                run = run_manager.start_run(run_id, parent_run_id)

                if name is None and serialized:
                    name = (
                        serialized.get("id", [None, None, None, None])[3]
                        if len(serialized.get("id", [])) > 3
                        else None
                    )

                type = "chain"
                metadata = metadata or {}

                agent_name = metadata.get("agent_name", metadata.get("agentName"))

                if name == "AgentExecutor" or name == "PlanAndExecute" or name == "LangGraph":
                    type = "agent"
                if agent_name is not None:
                    type = "agent"
                    name = agent_name
                if parent_run_id is not None and type != "agent":
                    type = "chain"
                    name = kwargs.get("name", name)

                if self._should_ignore_run(run.id, run_type=type, name=name):
                    run._ignored = True
                    matching_rule = self._get_matching_ignore_rule(run_type=type, name=name)
                    if matching_rule:
                        run._ignore_children = matching_rule.get("ignore_children", True)
                    else:
                        run._ignore_children = True  # Default behavior
                    self.__track_event(
                        type,
                        "start",
                        run_id=run.id,
                        parent_run_id=run.parent_run_id,
                        name=name,
                        input="__NOT_INGESTED__",
                        output="__NOT_INGESTED__",
                        app_id=self.__app_id,
                        api_url=self.__api_url,
                        callback_queue=self.queue,
                        runtime="langchain-py",
                    )
                    return

                user_id = _get_user_id(metadata)
                user_props = _get_user_props(metadata)
                input = _parse_input(inputs)

                self.__track_event(
                    type,
                    "start",
                    user_id=user_id,
                    run_id=run.id,
                    parent_run_id=run.parent_run_id,
                    name=name,
                    input=input,
                    tags=tags,
                    metadata=metadata,
                    user_props=user_props,
                    app_id=self.__app_id,
                    api_url=self.__api_url,
                    callback_queue=self.queue,
                    runtime="langchain-py",
                )
            except Exception as e:
                logger.exception(f"An error occurred in `on_chain_start`: {e}")

        def on_chain_end(
            self,
            outputs: Dict[str, Any],
            *args,
            run_id: UUID,
            parent_run_id: Union[UUID, None] = None,
            **kwargs: Any,
        ) -> Any:
            try:
                if self._should_ignore_run(str(run_id), run_type="chain"):
                    self.__track_event(
                        "chain",
                        "end",
                        run_id=str(run_id),
                        input="__NOT_INGESTED__",
                        output="__NOT_INGESTED__",
                        app_id=self.__app_id,
                        api_url=self.__api_url,
                        callback_queue=self.queue,
                        runtime="langchain-py",
                    )
                    run_manager.end_run(run_id)
                    return
                    
                run_id = run_manager.end_run(run_id)

                output = _parse_output(outputs)
                # For `astream_events(version="v2")`, LangChain can call
                # `on_chain_start` with a placeholder input and later pass the
                # real input as `kwargs["inputs"]` on `on_chain_end`.
                input = _parse_end_inputs(kwargs)

                event_payload = {
                    "run_id": run_id,
                    "output": output,
                    "app_id": self.__app_id,
                    "api_url": self.__api_url,
                    "callback_queue": self.queue,
                    "runtime": "langchain-py",
                }

                if input is not _MISSING:
                    event_payload["input"] = input

                self.__track_event(
                    "chain",
                    "end",
                    **event_payload,
                )
            except Exception as e:
                logger.exception(f"An error occurred in `on_chain_end`: {e}")

        def on_agent_finish(
            self,
            finish: AgentFinish,
            *,
            run_id: UUID,
            parent_run_id: Union[UUID, None] = None,
            **kwargs: Any,
        ) -> Any:
            try:
                if self._should_ignore_run(str(run_id), run_type="agent"):
                    self.__track_event(
                        "agent",
                        "end",
                        run_id=str(run_id),
                        input="__NOT_INGESTED__",
                        output="__NOT_INGESTED__",
                        app_id=self.__app_id,
                        api_url=self.__api_url,
                        callback_queue=self.queue,
                        runtime="langchain-py",
                    )
                    run_manager.end_run(run_id)
                    return
                    
                run_id = run_manager.end_run(run_id)

                output = _parse_output(finish.return_values)

                self.__track_event(
                    "agent",
                    "end",
                    run_id=run_id,
                    output=output,
                    app_id=self.__app_id,
                    api_url=self.__api_url,
                    callback_queue=self.queue,
                    runtime="langchain-py",
                )
            except Exception as e:
                logger.exception(f"An error occurred in `on_agent_finish`: {e}")

        def on_chain_error(
            self,
            error: BaseException,
            *,
            run_id: UUID,
            parent_run_id: Union[UUID, None] = None,
            **kwargs: Any,
        ) -> Any:
            try:
                if self._should_ignore_run(str(run_id), run_type="chain"):
                    self.__track_event(
                        "chain",
                        "error",
                        run_id=str(run_id),
                        input="__NOT_INGESTED__",
                        output="__NOT_INGESTED__",
                        app_id=self.__app_id,
                        api_url=self.__api_url,
                        callback_queue=self.queue,
                        runtime="langchain-py",
                    )
                    run_manager.end_run(run_id)
                    return
                    
                run_id = run_manager.end_run(run_id)

                self.__track_event(
                    "chain",
                    "error",
                    run_id=run_id,
                    error={"message": str(error) or "Unknown error", "stack": traceback.format_exc() or "No stack trace available"},
                    app_id=self.__app_id,
                    api_url=self.__api_url,
                    callback_queue=self.queue,
                    runtime="langchain-py",
                )
            except Exception as e:
                logger.exception(f"An error occurred in `on_chain_error`: {e}")

        def on_tool_error(
            self,
            error: BaseException,
            *,
            run_id: UUID,
            parent_run_id: Union[UUID, None] = None,
            **kwargs: Any,
        ) -> Any:
            try:
                if self._should_ignore_run(str(run_id), run_type="tool"):
                    self.__track_event(
                        "tool",
                        "error",
                        run_id=str(run_id),
                        input="__NOT_INGESTED__",
                        output="__NOT_INGESTED__",
                        app_id=self.__app_id,
                        api_url=self.__api_url,
                        callback_queue=self.queue,
                        runtime="langchain-py",
                    )
                    run_manager.end_run(run_id)
                    return
                    
                run_id = run_manager.end_run(run_id)

                self.__track_event(
                    "tool",
                    "error",
                    run_id=run_id,
                    error={"message": str(error) or "Unknown error", "stack": traceback.format_exc() or "No stack trace available"},
                    app_id=self.__app_id,
                    api_url=self.__api_url,
                    callback_queue=self.queue,
                    runtime="langchain-py",
                )
            except Exception as e:
                logger.exception(f"An error occurred in `on_tool_error`: {e}")

        def on_llm_error(
            self,
            error: BaseException,
            *,
            run_id: UUID,
            parent_run_id: Union[UUID, None] = None,
            **kwargs: Any,
        ) -> Any:
            try:
                if self._should_ignore_run(str(run_id), run_type="llm"):
                    self.__track_event(
                        "llm",
                        "error",
                        run_id=str(run_id),
                        input="__NOT_INGESTED__",
                        output="__NOT_INGESTED__",
                        app_id=self.__app_id,
                        api_url=self.__api_url,
                        callback_queue=self.queue,
                        runtime="langchain-py",
                    )
                    run_manager.end_run(run_id)
                    return
                    
                run_id = run_manager.end_run(run_id)

                self.__track_event(
                    "llm",
                    "error",
                    run_id=run_id,
                    error={"message": str(error) or "Unknown error", "stack": traceback.format_exc() or "No stack trace available"},
                    app_id=self.__app_id,
                    api_url=self.__api_url,
                    callback_queue=self.queue,
                    runtime="langchain-py",
                )
            except Exception as e:
                logger.exception(f"An error occurred in `on_llm_error`: {e}")

        def on_retriever_start(
            self,
            serialized: Dict[str, Any],
            query: str,
            run_id: Optional[UUID] = None,
            parent_run_id: Optional[UUID] = None,
            name: Union[str, None] = None,
            tags: Optional[list[str]] = None,
            metadata: Optional[dict[str, Any]] = None,
            **kwargs: Any,
        ) -> None:
            try:
                # if parent_run_id is None:
                #     parent_run_id = run_manager.current_run_id
                run = run_manager.start_run(run_id, parent_run_id)
                
                user_id = _get_user_id(kwargs.get("metadata"))
                user_props = _get_user_props(kwargs.get("metadata"))

                if name is None and serialized:
                    name = serialized.get("name")
                
                if self._should_ignore_run(run.id, run_type="retriever", name=name):
                    self.__track_event(
                        "retriever",
                        "start",
                        run_id=run.id,
                        parent_run_id=run.parent_run_id,
                        name=name,
                        input="__NOT_INGESTED__",
                        output="__NOT_INGESTED__",
                        app_id=self.__app_id,
                        api_url=self.__api_url,
                        callback_queue=self.queue,
                        runtime="langchain-py",
                    )
                    return

                self.__track_event(
                    "retriever",
                    "start",
                    user_id=user_id,
                    user_props=user_props,
                    run_id=run.id,
                    parent_run_id=run.parent_run_id,
                    name=name,
                    input=query,
                    app_id=self.__app_id,
                    api_url=self.__api_url,
                    callback_queue=self.queue,
                    runtime="langchain-py",
                    metadata=metadata,
                    tags=tags
                )
            except Exception as e:
                logger.exception(f"An error occurred in `on_retriever_start`: {e}")

        def on_retriever_end(
            self,
            documents: Sequence[Document],
            run_id: UUID,
            parent_run_id: Union[UUID, None] = None,
            **kwargs: Any,
        ) -> None:
            try:
                if self._should_ignore_run(str(run_id), run_type="retriever"):
                    self.__track_event(
                        "retriever",
                        "end",
                        run_id=str(run_id),
                        input="__NOT_INGESTED__",
                        output="__NOT_INGESTED__",
                        app_id=self.__app_id,
                        api_url=self.__api_url,
                        callback_queue=self.queue,
                        runtime="langchain-py",
                    )
                    return
                    
                run = run_manager.start_run(run_id, parent_run_id)

                # only report the metadata
                doc_metadata = [
                    (
                        doc.metadata
                        if doc.metadata
                        else {"summary": doc.page_content[:100]}
                    )
                    for doc in documents
                ]

                self.__track_event(
                    "retriever",
                    "end",
                    run_id=run.id,
                    parent_run_id=run.parent_run_id,
                    output=doc_metadata,
                    app_id=self.__app_id,
                    api_url=self.__api_url,
                    callback_queue=self.queue,
                    runtime="langchain-py",
                )
            except Exception as e:
                logger.exception(f"An error occurred in `on_retriever_end`: {e}")

        def on_retriever_error(
            self,
            error: BaseException,
            run_id: UUID,
            parent_run_id: Union[UUID, None] = None,
            **kwargs: Any,
        ) -> None:
            try:
                if self._should_ignore_run(str(run_id), run_type="retriever"):
                    self.__track_event(
                        "retriever",
                        "error",
                        run_id=str(run_id),
                        input="__NOT_INGESTED__",
                        output="__NOT_INGESTED__",
                        app_id=self.__app_id,
                        api_url=self.__api_url,
                        callback_queue=self.queue,
                        runtime="langchain-py",
                    )
                    run_manager.end_run(run_id)
                    return
                    
                run_id = run_manager.end_run(run_id)

                self.__track_event(
                    "retriever",
                    "error",
                    run_id=run_id,
                    error={"message": str(error) or "Unknown error", "stack": traceback.format_exc() or "No stack trace available"},
                    app_id=self.__app_id,
                    api_url=self.__api_url,
                    callback_queue=self.queue,
                    runtime="langchain-py",
                )
            except Exception as e:
                logger.exception(f"An error occurred in `on_retriever_error`: {e}")

except Exception as e:
    # Do not raise or print error for users that do not have Langchain installed
    pass

# TODO: depracte a use a new function nammed `open_conversation`?
def open_thread(id: Optional[str] = None, tags: Optional[List[str]] = None, app_id: str | None = None, user_id: str | None = None, user_props: Any | None = None, metadata: Dict[str, Any] | None = None):
    """
    Opens a new thread or connects to an existing one.

    Args:
        id: Optional thread identifier
        tags: Optional list of tags for the thread
        app_id: Optional app ID override
        user_id: Optional user ID for the thread
        user_props: Optional user properties
        metadata: Optional metadata for the thread

    Returns:
        Thread object

    Raises:
        ThreadError: If there's any error creating or connecting to the thread
    """
    try:
        config = get_config()
        token = app_id or config.app_id

        if not token:
            raise ThreadError("API token is required")

        return Thread(track_event=track_event, id=id, tags=tags, user_id=user_id, user_props=user_props, app_id=token, metadata=metadata)
    except Exception as e:
        raise ThreadError(f"Error opening thread: {str(e)}")

def track_feedback(run_id: str, feedback: Dict[str, Any] | Any):
    """
    Tracks feedback for a specific run.

    Args:
        run_id: The ID of the run to track feedback for
        feedback: Feedback data, must be a dictionary

    Raises:
        FeedbackError: If there's any error with the feedback data or tracking
    """
    try:
        if not run_id:
            raise FeedbackError("No message ID provided to track feedback")

        if not isinstance(feedback, dict):
            raise FeedbackError("Invalid feedback provided. Pass a valid dictionary")

        track_event(None, "feedback", run_id=run_id, feedback=feedback)
    except Exception as e:
        raise FeedbackError(f"Error tracking feedback: {str(e)}")


templateCache = {}
def get_raw_template(slug: str, app_id: str | None = None, api_url: str | None = None):
    """
    Fetches the latest version of a template based on a given slug.
    If a cached version is available and recent (less than 60 seconds old), 
    it will return the cached data. Otherwise, it makes an HTTP GET request
    to fetch the template from the specified or default API.

    Parameters:
        slug (str): Unique identifier for the template.
        app_id (str, optional): Application ID for authentication. Defaults to config's app ID.
        api_url (str, optional): API base URL. Defaults to config's API URL.

    Returns:
        dict: JSON response containing template data.
    
    Raises:
        TemplateError: If fetching the template fails.
    """
    try:
        config = get_config()
        token = app_id or config.app_id
        base_url = api_url or config.api_url

        if not token:
            raise TemplateError("No authentication token provided")

        global templateCache
        now = time.time() * 1000
        cache_entry = templateCache.get(slug)

        if cache_entry and now - cache_entry["timestamp"] < 60000:
            return cache_entry["data"]

        headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
        response = requests.get(
            f"{base_url}/v1/template_versions/latest?slug={slug}",
            headers=headers,
            verify=config.ssl_verify,
        )
        
        if response.status_code == 401:
            raise TemplateError("Invalid or unauthorized API credentials")
        
        if not response.ok:
            raise TemplateError(f"Error fetching template: {response.status_code} - {response.text}")

        data = response.json()
        templateCache[slug] = {"timestamp": now, "data": data}
        return data
        
    except requests.exceptions.RequestException as e:
        raise TemplateError(f"Network error while fetching template: {str(e)}")
    except Exception as e:
        raise TemplateError(f"Error fetching template: {str(e)}")

async def get_raw_template_async(slug: str, app_id: str | None = None, api_url: str | None = None):
    """
    Asynchronously fetches the latest version of a template based on a given slug.
    Similar to `get_raw_template`, but uses asynchronous requests.

    Parameters:
        slug (str): Unique identifier for the template.
        app_id (str, optional): Application ID for authentication. Defaults to config's app ID.
        api_url (str, optional): API base URL. Defaults to config's API URL.

    Returns:
        dict: JSON response containing template data.
    
    Raises:
        TemplateError: If fetching the template fails.
    """
    try:
        config = get_config()
        token = app_id or config.app_id
        api_url = api_url or config.api_url



        global templateCache
        now = time.time() * 1000
        cache_entry = templateCache.get(slug)

        if cache_entry and now - cache_entry["timestamp"] < 60000:
            return cache_entry["data"]

        headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"{api_url}/v1/template_versions/latest?slug={slug}",
                headers=headers
            ) as response:
                if not response.ok:
                    raise TemplateError(
                        f"Error fetching template: {response.status} - {await response.text()}"
                    )

                data = await response.json()
                templateCache[slug] = {"timestamp": now, "data": data}
                return data

    except TemplateError:
        raise
    except Exception as e:
        raise TemplateError(f"Error fetching template: {str(e)}")

def render_template(slug: str, data={}, app_id: str | None = None, api_url: str | None = None):
    """
    Renders a template by populating it with the provided data.
    Retrieves the raw template, then uses `chevron.render` to substitute variables.

    Parameters:
        slug (str): Template identifier.
        data (dict): Data for template rendering.
        app_id (str, optional): Application ID for authentication.
        api_url (str, optional): API base URL.

    Returns:
        dict: Rendered template with headers and extra metadata.

    Raises:
        TemplateError: If rendering fails.
    """
    try: 
        raw_template = get_raw_template(slug, app_id, api_url)

        if raw_template.get("message") == "Template not found, is the project ID correct?":
            raise TemplateError("Template not found, are the project ID and slug correct?")

        template_id = copy.deepcopy(raw_template["id"])
        content = copy.deepcopy(raw_template["content"])
        extra = copy.deepcopy(raw_template["extra"])
        text_mode = isinstance(content, str)
        extra_headers = {"Template-Id": str(template_id)}

        if text_mode:
            rendered = chevron.render(content, data)
            return {"text": rendered, "extra_headers": extra_headers, **extra}
        else:
            messages = []
            for message in content:
                message["content"] = chevron.render(message["content"], data)
                messages.append(message)
            return {"messages": messages, "extra_headers": extra_headers, **extra}

    except Exception as e:
        raise TemplateError(f"Error rendering template: {str(e)}")

async def render_template_async(slug: str, data={}, app_id: str | None = None, api_url: str | None = None):
    """
    Asynchronous version of `render_template`, which fetches and renders a template
    using asynchronous requests.

    Parameters:
        slug (str): Template identifier.
        data (dict): Data for template rendering.
        app_id (str, optional): Application ID for authentication.
        api_url (str, optional): API base URL.

    Returns:
        dict: Rendered template with headers and extra metadata.

    Raises:
        TemplateError: If rendering fails.
    """
    try:
        raw_template = await get_raw_template_async(slug, app_id, api_url)

        if raw_template.get("message") == "Template not found, is the project ID correct?":
            raise TemplateError("Template not found, are the project ID and slug correct?")

        template_id = copy.deepcopy(raw_template["id"])
        content = copy.deepcopy(raw_template["content"])
        extra = copy.deepcopy(raw_template["extra"])
        text_mode = isinstance(content, str)
        extra_headers = {"Template-Id": str(template_id)}

        if text_mode:
            rendered = chevron.render(content, data)
            return {"text": rendered, "extra_headers": extra_headers, **extra}
        else:
            messages = []
            for message in content:
                message["content"] = chevron.render(message["content"], data)
                messages.append(message)
            return {"messages": messages, "extra_headers": extra_headers, **extra}

    except Exception as e:
        raise TemplateError(f"Error rendering template: {str(e)}")

def get_langchain_template(slug: str, app_id: str | None = None, api_url: str | None = None):
    """
    Creates a LangChain prompt template from a raw template, converting any double braces.

    Parameters:
        slug (str): Template identifier.
        app_id (str, optional): Application ID for authentication.
        api_url (str, optional): API base URL.

    Returns:
        PromptTemplate or ChatPromptTemplate: Processed LangChain template.

    Raises:
        TemplateError: If creating the LangChain template fails.
    """
    try:
        from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
        
        raw_template = get_raw_template(slug, app_id, api_url)

        if raw_template.get("message") == "Template not found, is the project ID correct?":
            raise TemplateError("Template not found, are the project ID and slug correct?")

        content = copy.deepcopy(raw_template["content"])
        text_mode = isinstance(content, str)

        def replace_double_braces(text):
            return text.replace("{{", "{").replace("}}", "}")

        if text_mode:
            rendered = replace_double_braces(content)
            return PromptTemplate.from_template(rendered)
        else:
            messages = []
            for message in content:
                messages.append(
                    (
                        message["role"].replace("assistant", "ai").replace("user", "human"),
                        replace_double_braces(message["content"]),
                    )
                )
            return ChatPromptTemplate.from_messages(messages)

    except ImportError:
        raise TemplateError("LangChain is required. Install it with: pip install langchain-core")
    except Exception as e:
        raise TemplateError(f"Error creating LangChain template: {str(e)}")

async def get_langchain_template_async(slug: str, app_id: str | None = None, api_url: str | None = None):
    """
    Asynchronous version of `get_langchain_template`, which creates a LangChain prompt
    template using asynchronous requests.

    Parameters:
        slug (str): Template identifier.
        app_id (str, optional): Application ID for authentication.
        api_url (str, optional): API base URL.

    Returns:
        PromptTemplate or ChatPromptTemplate: Processed LangChain template.

    Raises:
        TemplateError: If creating the LangChain template fails.
    """
    try:
        from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
        
        raw_template = await get_raw_template_async(slug, app_id, api_url)

        if raw_template.get("message") == "Template not found, is the project ID correct?":
            raise TemplateError("Template not found, are the project ID and slug correct?")

        content = copy.deepcopy(raw_template["content"])
        text_mode = isinstance(content, str)

        def replace_double_braces(text):
            return text.replace("{{", "{").replace("}}", "}")

        if text_mode:
            rendered = replace_double_braces(content)
            return PromptTemplate.from_template(rendered)
        else:
            messages = []
            for message in content:
                messages.append(
                    (
                        message["role"].replace("assistant", "ai").replace("user", "human"),
                        replace_double_braces(message["content"]),
                    )
                )
            return ChatPromptTemplate.from_messages(messages)

    except ImportError:
        raise TemplateError("LangChain is required. Install it with: pip install langchain-core")
    except Exception as e:
        raise TemplateError(f"Error creating LangChain template: {str(e)}")

def get_live_templates(app_id: str | None = None, api_url: str | None = None):
    """
    Fetches a list of the latest live templates available.

    Parameters:
        app_id (str, optional): Application ID for authentication.
        api_url (str, optional): API base URL.

    Returns:
        list: JSON list of live templates.

    Raises:
        TemplateError: If fetching templates fails.
    """
    try:
        config = get_config()
        token = app_id or config.app_id
        api_url = api_url or config.api_url

        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }

        response = requests.get(
            url=f"{api_url}/v1/templates/latest",
            headers=headers,
            verify=config.ssl_verify,
        )
        
        if not response.ok:
            raise TemplateError(f"Error fetching templates: {response.status_code} - {response.text}")

        return response.json()
    except Exception as e:
        raise TemplateError(f"Error fetching templates: {str(e)}")
    
class DatasetItem:
    def __init__(self, d=None):
        if d is not None:
            for key, value in d.items():
                setattr(self, key, value)

def get_dataset(slug: str, app_id: str | None = None, api_url: str | None = None):
    """
    Fetches a dataset based on the given slug, parsing and returning it as a list of
    DatasetItem objects.

    Parameters:
        slug (str): Dataset identifier.
        app_id (str, optional): Application ID for authentication.
        api_url (str, optional): API base URL.

    Returns:
        list[DatasetItem]: List of dataset items.

    Raises:
        DatasetError: If fetching the dataset fails.
    """
    try:
        config = get_config()
        token = app_id or config.app_id
        api_url = api_url or config.api_url

        url = f"{api_url}/v1/datasets/{slug}"
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }
        
        response = requests.get(url, headers=headers, verify=config.ssl_verify)
        if not response.ok:
            raise DatasetError(f"Error fetching dataset: {response.status_code}")

        dataset = response.json()
        dataset = humps.decamelize(dataset)
        items_data = dataset.get("items", [])
        return [DatasetItem(d=item) for item in items_data]

    except Exception as e:
        raise DatasetError(f"Error fetching dataset: {str(e)}")
    
def score(run_id: str, label: str, value: int | float | str | bool, comment: str | None = None, app_id: str | None = None, api_url: str | None = None):
    """
    Scores a run based on the provided label, value, and optional comment.

    Parameters:
        run_id (str): Unique run identifier.
        label (str): Evaluation label.
        value (int | float | str | bool): Evaluation value.
        comment (str, optional): Evaluation comment.

    Raises:
        ScoringError: If scoring fails.
    """
    try:
        config = get_config()
        token = app_id or config.app_id
        api_url = api_url or config.api_url

        url = f"{api_url}/v1/runs/{run_id}/score"
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }

        data = {
            "label": label,
            "value": value,
            **({"comment": comment} if comment else {}),
        }

        response = requests.patch(url, headers=headers, json=data, verify=config.ssl_verify)
        
        if response.status_code == 500:
            error_message = response.json().get("message", "Unknown error")
            raise ScoringError(f"Scoring failed: {error_message}")
        elif not response.ok:
            raise ScoringError(f"Error scoring run: {response.status_code} - {response.text}")

    except Exception as e:
        raise EvaluationError(f"Error scoring run: {str(e)}")


def evaluate(
    checklist,
    input,
    output,
    ideal_output=None,
    context=None,
    model=None,
    duration=None,
    tags=None,
    app_id: str | None = None,
    api_url: str | None = None,
):
    """
    Submits an evaluation run based on provided input, output, and other optional parameters.

    Parameters:
        checklist (list): Evaluation criteria checklist.
        input (Any): Input data for the evaluation.
        output (Any): Output to evaluate.
        ideal_output (Any, optional): Expected ideal output.
        context (Any, optional): Additional evaluation context.
        model (Any, optional): Model used for the evaluation.
        duration (float, optional): Evaluation duration.
        tags (list, optional): Evaluation tags.
        app_id (str, optional): Application ID for authentication.
        api_url (str, optional): API base URL.

    Returns:
        tuple: (passed, results) evaluation status and details.

    Raises:
        EvaluationError: If evaluation fails.
    """
    try:
        config = get_config()
        token = app_id or config.app_id
        api_url = api_url or config.api_url

        url = f"{api_url}/v1/evaluations/run"
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }
        
        data = {
            "checklist": checklist,
            "input": input,
            "output": output,
            **({"idealOutput": ideal_output} if ideal_output else {}),
            **({"context": context} if context else {}),
            **({"model": model} if model else {}),
            **({"duration": duration} if duration else {}),
            **({"tags": tags} if tags else {})
        }

        response = requests.post(url, headers=headers, json=data, verify=config.ssl_verify)
        
        if response.status_code == 500:
            error_message = response.json().get("message", "Unknown error")
            raise EvaluationError(f"Evaluation failed: {error_message}")
        elif not response.ok:
            raise EvaluationError(f"Error running evaluation: {response.status_code} - {response.text}")

        data = humps.decamelize(response.json())
        return data["passed"], data["results"]

    except Exception as e:
        raise EvaluationError(f"Error evaluating result: {str(e)}")


# TODO: use the endpoint, not track_event
def track_feedback(run_id: str, feedback: Dict[str, Any] | Any):
    """
    Tracks feedback for a given run ID, validating the provided feedback.

    Parameters:
        run_id (str): Unique run identifier.
        feedback (dict): Feedback data.

    Raises:
        LunaryError: If tracking feedback fails.
    """
    try:
        if not run_id:
            raise LunaryError("No message ID provided to track feedback")

        if not isinstance(feedback, dict):
            raise LunaryError("Invalid feedback provided. Pass a valid object")

        track_event(None, "feedback", run_id=run_id, feedback=feedback)
    except Exception as e:
        raise LunaryError(f"Error tracking feedback: {str(e)}")
