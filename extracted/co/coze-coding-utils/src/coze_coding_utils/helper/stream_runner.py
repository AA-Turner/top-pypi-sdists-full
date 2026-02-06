import time
import asyncio
import threading
import contextvars
import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Dict, Iterator, AsyncIterable, Optional, Literal
from langchain_core.runnables import RunnableConfig
from langgraph.graph.state import CompiledStateGraph
from coze_coding_utils.helper.agent_helper import (
    to_stream_input,
    agent_iter_server_messages,
)

from coze_coding_utils.error import classify_error
import asyncio
import time
import traceback
from typing import Any, Dict, AsyncGenerator, Callable
from coze_coding_utils.runtime_ctx.context import Context
from coze_coding_utils.messages.server import (
    create_message_end_dict,
    create_message_error_dict,
    MESSAGE_END_CODE_CANCELED,
)
from coze_coding_utils.helper.agent_helper import to_client_message
from coze_coding_utils.error.classifier import ErrorClassifier

logger = logging.getLogger(__name__)

TIMEOUT_SECONDS = 900
PING_INTERVAL_SECONDS = 30


@dataclass
class RunOpt:
    workflow_debug: bool = False

    @property
    def stream_mode(self) -> Literal["debug", "updates"]:
        return "debug" if self.workflow_debug else "updates"

class WorkflowEventType:
    WORKFLOW_START = "workflow_start"
    WORKFLOW_END = "workflow_end"
    NODE_START = "node_start" # 节点开始事件，只有debug模式发送
    NODE_END = "node_end" # 节点结束事件，只有debug模式发送
    ERROR = "error" # 错误事件
    PING = "ping" # 心跳事件


class WorkflowErrorCode:
    CANCELED = "CANCELED" # 取消事件
    TIMEOUT = "TIMEOUT" # 超时事件


class BaseStreamRunner(ABC):
    @abstractmethod
    def stream(self, payload: Dict[str, Any], graph: CompiledStateGraph, run_config: RunnableConfig, ctx: Context, run_opt: Optional[RunOpt] = None) -> Iterator[Any]:
        pass

    @abstractmethod
    async def astream(self, payload: Dict[str, Any], graph: CompiledStateGraph, run_config: RunnableConfig, ctx: Context, run_opt: Optional[RunOpt] = None) -> AsyncIterable[Any]:
        pass


class AgentStreamRunner(BaseStreamRunner):
    def stream(self, payload: Dict[str, Any], graph: CompiledStateGraph, run_config: RunnableConfig, ctx: Context, run_opt: Optional[RunOpt] = None) -> Iterator[Any]:
        client_msg, session_id = to_client_message(payload)
        run_config["recursion_limit"] = 100
        run_config["configurable"] = {"thread_id": session_id}
        stream_input = to_stream_input(client_msg)
        t0 = time.time()
        try:
            items = graph.stream(stream_input, stream_mode="messages", config=run_config, context=ctx)
            server_msgs_iter = agent_iter_server_messages(
                items,
                session_id=client_msg.session_id,
                query_msg_id=client_msg.local_msg_id,
                local_msg_id=client_msg.local_msg_id,
                run_id=ctx.run_id,
                log_id=ctx.logid,
            )
            for sm in server_msgs_iter:
                yield sm.dict()
        except asyncio.CancelledError:
            logger.info(f"Stream cancelled for run_id: {ctx.run_id}")
            end_msg = create_message_end_dict(
                code=MESSAGE_END_CODE_CANCELED,
                message="Stream execution cancelled",
                session_id=client_msg.session_id,
                query_msg_id=client_msg.local_msg_id,
                log_id=ctx.logid,
                time_cost_ms=int((time.time() - t0) * 1000),
                reply_id="",
                sequence_id=1,
            )
            yield end_msg
            raise
        except Exception as ex:
            err = classify_error(ex, {"node_name": "stream"})
            end_msg = create_message_error_dict(
                code=str(err.code),
                message=err.message,
                session_id=client_msg.session_id,
                query_msg_id=client_msg.local_msg_id,
                log_id=ctx.logid,
                reply_id="",
                sequence_id=1,
            )
            yield end_msg

    async def astream(self, payload: Dict[str, Any], graph: CompiledStateGraph, run_config: RunnableConfig, ctx: Context, run_opt: Optional[RunOpt] = None) -> AsyncIterable[Any]:
        client_msg, session_id = to_client_message(payload)
        run_config["recursion_limit"] = 100
        run_config["configurable"] = {"thread_id": session_id}
        stream_input = to_stream_input(client_msg)

        loop = asyncio.get_running_loop()
        q: asyncio.Queue = asyncio.Queue()
        context = contextvars.copy_context()
        start_time = time.time()
        cancelled = threading.Event()

        def producer():
            last_seq = 0
            try:
                if cancelled.is_set():
                    logger.info(f"Producer cancelled before start for run_id: {ctx.run_id}")
                    return

                items = graph.stream(stream_input, stream_mode="messages", config=run_config, context=ctx)
                server_msgs_iter = agent_iter_server_messages(
                    items,
                    session_id=client_msg.session_id,
                    query_msg_id=client_msg.local_msg_id,
                    local_msg_id=client_msg.local_msg_id,
                    run_id=ctx.run_id,
                    log_id=ctx.logid,
                )
                for sm in server_msgs_iter:
                    if cancelled.is_set():
                        logger.info(f"Producer cancelled during iteration for run_id: {ctx.run_id}")
                        cancel_msg = create_message_end_dict(
                            code=MESSAGE_END_CODE_CANCELED,
                            message="Stream cancelled by upstream",
                            session_id=client_msg.session_id,
                            query_msg_id=client_msg.local_msg_id,
                            log_id=ctx.logid,
                            time_cost_ms=int((time.time() - start_time) * 1000),
                            reply_id=getattr(sm, 'reply_id', ''),
                            sequence_id=last_seq + 1,
                        )
                        loop.call_soon_threadsafe(q.put_nowait, cancel_msg)
                        return

                    if time.time() - start_time > TIMEOUT_SECONDS:
                        logger.error(f"Agent execution timeout after {TIMEOUT_SECONDS}s for run_id: {ctx.run_id}")
                        timeout_msg = create_message_end_dict(
                            code="TIMEOUT",
                            message=f"Execution timeout: exceeded {TIMEOUT_SECONDS} seconds",
                            session_id=client_msg.session_id,
                            query_msg_id=client_msg.local_msg_id,
                            log_id=ctx.logid,
                            time_cost_ms=int((time.time() - start_time) * 1000),
                            reply_id=getattr(sm, 'reply_id', ''),
                            sequence_id=last_seq + 1,
                        )
                        loop.call_soon_threadsafe(q.put_nowait, timeout_msg)
                        return
                    loop.call_soon_threadsafe(q.put_nowait, sm.dict())
                    last_seq = sm.sequence_id
            except Exception as ex:
                if cancelled.is_set():
                    logger.info(f"Producer exception after cancel for run_id: {ctx.run_id}, ignoring: {ex}")
                    return
                err = classify_error(ex, {"node_name": "astream"})
                end_msg = create_message_error_dict(
                    code=str(err.code),
                    message=err.message,
                    session_id=client_msg.session_id,
                    query_msg_id=client_msg.local_msg_id,
                    log_id=ctx.logid,
                    reply_id="",
                    sequence_id=last_seq + 1,
                )
                loop.call_soon_threadsafe(q.put_nowait, end_msg)
            finally:
                loop.call_soon_threadsafe(q.put_nowait, None)

        threading.Thread(target=lambda: context.run(producer), daemon=True).start()

        try:
            while True:
                item = await q.get()
                if item is None:
                    break
                yield item
        except asyncio.CancelledError:
            logger.info(f"Stream cancelled for run_id: {ctx.run_id}, signaling producer to stop")
            cancelled.set()
            raise


class WorkflowStreamRunner(BaseStreamRunner):
    def _serialize_data(self, data: Any) -> Any:
        if isinstance(data, dict):
            return {k: self._serialize_data(v) for k, v in data.items()}
        elif isinstance(data, (list, tuple)):
            return [self._serialize_data(item) for item in data]
        elif hasattr(data, 'model_dump'):
            return data.model_dump()
        elif hasattr(data, 'dict'):
            return data.dict()
        elif hasattr(data, '__dict__'):
            return {k: self._serialize_data(v) for k, v in data.__dict__.items() if not k.startswith('_')}
        else:
            return data

    def _build_event(self, event_type: str, ctx: Context, **kwargs) -> Dict[str, Any]:
        result = {
            "type": event_type,
            "timestamp": int(time.time() * 1000),
            "log_id": ctx.logid,
            "run_id": ctx.run_id,
        }
        result.update(kwargs)
        return result

    def stream(self, payload: Dict[str, Any], graph: CompiledStateGraph, run_config: RunnableConfig, ctx: Context, run_opt: Optional[RunOpt] = None) -> Iterator[Any]:
        if run_opt is None:
            run_opt = RunOpt()
        run_config["recursion_limit"] = 100
        if "configurable" not in run_config:
            run_config["configurable"] = {}
        run_config["configurable"]["thread_id"] = ctx.run_id
        
        t0 = time.time()
        last_ping_time = t0
        node_start_times: Dict[str, float] = {}
        final_output = {}
        seq = 0

        try:
            seq += 1
            yield (seq, self._build_event(WorkflowEventType.WORKFLOW_START, ctx))

            for event in graph.stream(payload, stream_mode=run_opt.stream_mode, config=run_config, context=ctx):
                current_time = time.time()
                if current_time - last_ping_time >= PING_INTERVAL_SECONDS:
                    seq += 1
                    yield (seq, self._build_event(WorkflowEventType.PING, ctx))
                    last_ping_time = current_time
                
                if not run_opt.workflow_debug:
                    if isinstance(event, dict):
                        logger.info(f"Debug event: {event}")
                        for node_name, node_output in event.items():
                            final_output = self._serialize_data(node_output) if node_output else {}
                    continue

                event_type = event.get("type", "")
                
                if event_type == "task":
                    node_name = event.get("payload", {}).get("name", "")
                    node_start_times[node_name] = current_time
                    
                    input_data = event.get("payload", {}).get("input", {})
                    seq += 1
                    yield (seq, self._build_event(
                        WorkflowEventType.NODE_START,
                        ctx,
                        node_name=node_name,
                        input=self._serialize_data(input_data),
                    ))
                    
                elif event_type == "task_result":
                    node_name = event.get("payload", {}).get("name", "")
                    result = event.get("payload", {}).get("result")
                    
                    output_data = {}
                    if result is not None:
                        if isinstance(result, (list, tuple)) and len(result) > 0:
                            output_data = self._serialize_data(result[0]) if len(result) == 1 else {"results": [self._serialize_data(r) for r in result]}
                        else:
                            output_data = self._serialize_data(result)
                    
                    final_output = output_data
                    
                    node_start_time = node_start_times.pop(node_name, current_time)
                    time_cost_ms = int((current_time - node_start_time) * 1000)
                    
                    seq += 1
                    yield (seq, self._build_event(
                        WorkflowEventType.NODE_END,
                        ctx,
                        node_name=node_name,
                        output=output_data,
                        time_cost_ms=time_cost_ms,
                    ))

            seq += 1
            yield (seq, self._build_event(
                WorkflowEventType.WORKFLOW_END,
                ctx,
                output=final_output,
                time_cost_ms=int((time.time() - t0) * 1000),
            ))

        except asyncio.CancelledError:
            logger.info(f"Workflow stream cancelled for run_id: {ctx.run_id}")
            seq += 1
            yield (seq, self._build_event(WorkflowEventType.ERROR, ctx, code=WorkflowErrorCode.CANCELED, message="Stream execution cancelled"))
            raise
        except Exception as ex:
            err = classify_error(ex, {"node_name": "workflow_stream"})
            seq += 1
            yield (seq, self._build_event(WorkflowEventType.ERROR, ctx, code=str(err.code), error_msg=err.message))

    async def astream(self, payload: Dict[str, Any], graph: CompiledStateGraph, run_config: RunnableConfig, ctx: Context, run_opt: Optional[RunOpt] = None) -> AsyncIterable[Any]:
        if run_opt is None:
            run_opt = RunOpt()
        run_config["recursion_limit"] = 100
        if "configurable" not in run_config:
            run_config["configurable"] = {}
        run_config["configurable"]["thread_id"] = ctx.run_id

        loop = asyncio.get_running_loop()
        q: asyncio.Queue = asyncio.Queue()
        context = contextvars.copy_context()
        start_time = time.time()
        cancelled = threading.Event()
        last_ping_time = [start_time]
        logger.info(f"Stream mode: {run_opt.stream_mode}")
        seq = [0]

        def producer():
            node_start_times: Dict[str, float] = {}
            final_output = {}
            try:
                if cancelled.is_set():
                    logger.info(f"Workflow producer cancelled before start for run_id: {ctx.run_id}")
                    return

                seq[0] += 1
                loop.call_soon_threadsafe(q.put_nowait, (seq[0], self._build_event(WorkflowEventType.WORKFLOW_START, ctx)))

                for event in graph.stream(payload, stream_mode=run_opt.stream_mode, config=run_config, context=ctx):
                    if cancelled.is_set():
                        logger.info(f"Workflow producer cancelled during iteration for run_id: {ctx.run_id}")
                        seq[0] += 1
                        loop.call_soon_threadsafe(q.put_nowait, (seq[0], self._build_event(WorkflowEventType.ERROR, ctx, code=WorkflowErrorCode.CANCELED, message="Stream cancelled by upstream")))
                        return

                    if time.time() - start_time > TIMEOUT_SECONDS:
                        logger.error(f"Workflow execution timeout after {TIMEOUT_SECONDS}s for run_id: {ctx.run_id}")
                        seq[0] += 1
                        loop.call_soon_threadsafe(q.put_nowait, (seq[0], self._build_event(WorkflowEventType.ERROR, ctx, code=WorkflowErrorCode.TIMEOUT, message=f"Execution timeout: exceeded {TIMEOUT_SECONDS} seconds")))
                        return

                    current_time = time.time()
                    if current_time - last_ping_time[0] >= PING_INTERVAL_SECONDS:
                        seq[0] += 1
                        loop.call_soon_threadsafe(q.put_nowait, (seq[0], self._build_event(WorkflowEventType.PING, ctx)))
                        last_ping_time[0] = current_time

                    if not run_opt.workflow_debug:
                        if isinstance(event, dict):
                            for node_name, node_output in event.items():
                                logger.info(f"Node output: {node_name}")
                                final_output = self._serialize_data(node_output) if node_output else {}
                        continue

                    event_type = event.get("type", "")
                    
                    if event_type == "task":
                        node_name = event.get("payload", {}).get("name", "")
                        node_start_times[node_name] = current_time
                        
                        input_data = event.get("payload", {}).get("input", {})
                        seq[0] += 1
                        loop.call_soon_threadsafe(q.put_nowait, (seq[0], self._build_event(
                            WorkflowEventType.NODE_START,
                            ctx,
                            node_name=node_name,
                            input=self._serialize_data(input_data),
                        )))
                        
                    elif event_type == "task_result":
                        node_name = event.get("payload", {}).get("name", "")
                        result = event.get("payload", {}).get("result")
                        
                        output_data = {}
                        if result is not None:
                            if isinstance(result, (list, tuple)) and len(result) > 0:
                                output_data = self._serialize_data(result[0]) if len(result) == 1 else {"results": [self._serialize_data(r) for r in result]}
                            else:
                                output_data = self._serialize_data(result)
                        
                        final_output = output_data
                        
                        node_start_time = node_start_times.pop(node_name, current_time)
                        time_cost_ms = int((current_time - node_start_time) * 1000)
                        
                        seq[0] += 1
                        loop.call_soon_threadsafe(q.put_nowait, (seq[0], self._build_event(
                            WorkflowEventType.NODE_END,
                            ctx,
                            node_name=node_name,
                            output=output_data,
                            time_cost_ms=time_cost_ms,
                        )))

                seq[0] += 1
                loop.call_soon_threadsafe(q.put_nowait, (seq[0], self._build_event(
                    WorkflowEventType.WORKFLOW_END,
                    ctx,
                    output=final_output,
                    time_cost_ms=int((time.time() - start_time) * 1000),
                )))

            except Exception as ex:
                if cancelled.is_set():
                    logger.info(f"Workflow producer exception after cancel for run_id: {ctx.run_id}, ignoring: {ex}")
                    return
                err = classify_error(ex, {"node_name": "workflow_astream"})
                seq[0] += 1
                loop.call_soon_threadsafe(q.put_nowait, (seq[0], self._build_event(WorkflowEventType.ERROR, ctx, code=str(err.code), error_msg=err.message)))
            finally:
                loop.call_soon_threadsafe(q.put_nowait, None)

        async def ping_sender():
            while not cancelled.is_set():
                await asyncio.sleep(PING_INTERVAL_SECONDS)
                if cancelled.is_set():
                    break
                current_time = time.time()
                if current_time - last_ping_time[0] >= PING_INTERVAL_SECONDS:
                    seq[0] += 1
                    await q.put((seq[0], self._build_event(WorkflowEventType.PING, ctx)))
                    last_ping_time[0] = current_time

        threading.Thread(target=lambda: context.run(producer), daemon=True).start()
        ping_task = asyncio.create_task(ping_sender())

        try:
            while True:
                item = await q.get()
                if item is None:
                    break
                yield item
        except asyncio.CancelledError:
            logger.info(f"Workflow stream cancelled for run_id: {ctx.run_id}, signaling producer to stop")
            cancelled.set()
            raise
        finally:
            cancelled.set()
            ping_task.cancel()
            try:
                await ping_task
            except asyncio.CancelledError:
                pass


async def agent_stream_handler(
    payload: Dict[str, Any],
    ctx: Context,
    run_id: str,
    stream_sse_func: Callable,
    sse_event_func: Callable,
    error_classifier: ErrorClassifier,
    register_task_func: Callable[[str, asyncio.Task], None],
) -> AsyncGenerator[str, None]:
    task = asyncio.current_task()
    if task:
        register_task_func(run_id, task)
        logger.info(f"Registered agent streaming task for run_id: {run_id}")

    client_msg, _ = to_client_message(payload)
    t0 = time.time()

    try:
        async for chunk in stream_sse_func(payload, ctx):
            yield chunk
    except asyncio.CancelledError:
        logger.info(f"Agent stream cancelled for run_id: {run_id}")
        end_msg = create_message_end_dict(
            code=MESSAGE_END_CODE_CANCELED,
            message="Stream cancelled by user",
            session_id=client_msg.session_id,
            query_msg_id=client_msg.local_msg_id,
            log_id=ctx.logid,
            time_cost_ms=int((time.time() - t0) * 1000),
            reply_id="",
            sequence_id=1,
        )
        yield sse_event_func(end_msg)
        raise
    except Exception as ex:
        err = error_classifier.classify(ex, {"node_name": "agent_stream", "run_id": run_id})
        logger.error(
            f"Unexpected error in agent_stream: [{err.code}] {err.message}, "
            f"traceback: {traceback.format_exc()}"
        )
        error_msg = create_message_error_dict(
            code=str(err.code),
            message=str(ex),
            session_id=client_msg.session_id,
            query_msg_id=client_msg.local_msg_id,
            log_id=ctx.logid,
            reply_id="",
            sequence_id=1,
            local_msg_id=client_msg.local_msg_id,
        )
        yield sse_event_func(error_msg)


async def workflow_stream_handler(
    payload: Dict[str, Any],
    ctx: Context,
    run_id: str,
    stream_sse_func: Callable,
    sse_event_func: Callable,
    error_classifier: ErrorClassifier,
    register_task_func: Callable[[str, asyncio.Task], None],
    run_opt: Optional[RunOpt] = None,
) -> AsyncGenerator[str, None]:
    if run_opt is None:
        run_opt = RunOpt()
    task = asyncio.current_task()
    if task:
        register_task_func(run_id, task)
        logger.info(f"Registered workflow streaming task for run_id: {run_id}")

    try:
        async for chunk in stream_sse_func(payload, ctx, run_opt):
            yield chunk
    except asyncio.CancelledError:
        logger.info(f"Workflow stream cancelled for run_id: {run_id}")
        cancel_event = {
            "type": "error",
            "timestamp": int(time.time() * 1000),
            "log_id": ctx.logid,
            "run_id": run_id,
            "code": "CANCELED",
            "error_msg": "Stream cancelled by user",
        }
        yield sse_event_func(cancel_event)
        raise
    except Exception as ex:
        err = error_classifier.classify(ex, {"node_name": "workflow_stream", "run_id": run_id})
        logger.error(
            f"Unexpected error in workflow_stream: [{err.code}] {err.message}, "
            f"traceback: {traceback.format_exc()}"
        )
        error_event = {
            "type": "error",
            "timestamp": int(time.time() * 1000),
            "log_id": ctx.logid,
            "run_id": run_id,
            "code": str(err.code),
            "error_msg": str(ex),
        }
        yield sse_event_func(error_event)


def get_stream_runner(is_agent: bool) -> BaseStreamRunner:
    if is_agent:
        return AgentStreamRunner()
    else:
        return WorkflowStreamRunner()
