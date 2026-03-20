import asyncio
import json
import logging
import threading
import traceback
from typing import Any, Awaitable, Callable, Dict, Optional, Type
from uuid import uuid4

from prophecy.executionmetrics.execution_metrics_handler import ExecutionMetricsHandler
from prophecy.jsonrpc.models import (
    DatasetRunsDetailedRequest,
    DatasetRunsRequest,
    DeleteDatasetRunRequest,
    DeletePipelineRunRequest,
    EMRequest,
    ErrorResponse,
    HistoricalGemProgressRequest,
    HistoricalViewRequest,
    InterimsRequest,
    JsonRpcError,
    JsonRpcResult,
    LoadLastPipelineRunInterimsRequest,
    PipelineRunsRequest,
    RequestMessage,
    RequestMethod,
    ResponseMessage,
    SuccessResponse,
)
from prophecy.utils.secrets import SecretCrudRequest, handle_secrets_crud


_execution_metrics_handler: Optional[ExecutionMetricsHandler] = None
_handler_init_lock = threading.Lock()


def _get_spark_session():
    # Try serverless mode first
    try:
        from server_rest import SparkSessionProxy
        return SparkSessionProxy.get_instance()
    except ImportError:
        pass
    except Exception as e:
        logging.debug(f"SparkSessionProxy not available: {e}")

    # Try getting active SparkSession (interactive mode)
    try:
        from pyspark.sql import SparkSession
        spark = SparkSession.getActiveSession()
        if spark is not None:
            return spark
    except ImportError:
        pass
    except Exception as e:
        logging.debug(f"Failed to get active SparkSession: {e}")

    return None


def _get_execution_metrics_handler() -> Optional[ExecutionMetricsHandler]:
    """Lazy-initialize and return the ExecutionMetricsHandler."""
    global _execution_metrics_handler

    if _execution_metrics_handler is not None:
        return _execution_metrics_handler

    with _handler_init_lock:
        if _execution_metrics_handler is not None:
            return _execution_metrics_handler

        spark = _get_spark_session()
        if spark is not None:
            try:
                _execution_metrics_handler = ExecutionMetricsHandler(spark)
            except Exception as e:
                logging.error(f"Failed to create ExecutionMetricsHandler: {e}")
    return _execution_metrics_handler


def _get_handler_for_request(request_type: Type[RequestMethod]) -> Optional[Callable]:
    """Get the appropriate handler for a request type."""
    handler = _get_execution_metrics_handler()
    if handler is None:
        return None

    handler_map: Dict[Type[RequestMethod], Callable] = {
        DatasetRunsRequest: handler._handle_dataset_runs,
        DatasetRunsDetailedRequest: handler._handle_dataset_runs_detailed,
        InterimsRequest: handler.find_interim_response_for_pipeline,
        HistoricalGemProgressRequest: handler.get_gem_progress_for_pipeline,
        HistoricalViewRequest: handler._handle_historical_view,
        PipelineRunsRequest: handler._handle_pipeline_runs,
        DeleteDatasetRunRequest: handler._handle_delete_dataset_run,
        DeletePipelineRunRequest: handler._handle_delete_pipeline_run,
        LoadLastPipelineRunInterimsRequest: handler._handle_load_last_pipeline_run_interims,
        SecretCrudRequest: handle_secrets_crud,
    }
    return handler_map.get(request_type)


# ----- 2.2  async dispatcher (runs inside a background event‑loop) ---------
async def dispatch_em_request_async(
    req_msg: RequestMessage,
) -> ResponseMessage:  # noqa: D401
    req = req_msg.method

    em_handler = _get_execution_metrics_handler()

    if isinstance(req, EMRequest) and em_handler is not None:
        try:
            em_handler.refresh_tables_with_filters(req.filters)
        except Exception as e:
            logging.warning(f"Failed to refresh tables: {e}")

    handler = _get_handler_for_request(type(req))
    if handler is None:
        raise RuntimeError(f"No handler registered for {type(req).__name__} (SparkSession may not be available)")
    try:
        result = await handler(req)  # type: ignore[arg-type]
        return SuccessResponse(id=req_msg.id, result=result)  # type: ignore[return-value]
    except Exception as exc:  # noqa: BLE001
        logging.info(f"Failed procesing request: {req}, error: {exc}, trace: {traceback.format_exc()}")
        err = JsonRpcError(message=str(exc), trace=traceback.format_exc().splitlines())
        return ErrorResponse(id=req_msg.id, error=err)  # type: ignore[return-value]


# ----- 2.3  background asyncio loop in daemon thread -----------------------
_EVENT_LOOP = asyncio.new_event_loop()
_thread = threading.Thread(target=_EVENT_LOOP.run_forever, daemon=True)
_thread.start()


def _schedule(coro: Awaitable[Any]):  # noqa: D401
    """Run *coro* in the background loop and return its result (blocking)."""
    return asyncio.run_coroutine_threadsafe(coro, _EVENT_LOOP).result()


###############################################################################
# 3.  WEBSOCKET‑CLIENT GLUE                                                 #
###############################################################################


def _send_ws_response(ws, response_json: str) -> None:
    """Send response via WebSocket - supports both interactive and serverless modes."""
    if ws is not None:
        try:
            ws.send(response_json)
            return
        except Exception as e:
            logging.warning(f"Failed to send via interactive WS: {e}")

    # Fall back to serverless mode
    try:
        from websocket_runner import send_message_via_ws
        send_message_via_ws(response_json)
    except ImportError:
        logging.error("No WebSocket available to send response")
    except Exception as e:
        logging.error(f"Failed to send response: {e}")


def _process_request(payload_raw: str, ws) -> None:  # noqa: D401
    """Handle one frame coming from server, send back a response frame."""

    try:
        payload_str = (
            json.dumps(payload_raw) if isinstance(payload_raw, dict) else payload_raw
        )
        req_msg = RequestMessage.from_json(payload_str)

        resp_msg = _schedule(dispatch_em_request_async(req_msg))
        logging.info(f"Sending back success response")
        _send_ws_response(ws, resp_msg.to_json())

    except Exception as exc:  # catch‑all: malformed frame
        logging.info(f"Error processing request {exc} -- {traceback.format_exc()}")
        err_resp = ErrorResponse(
            id=str(uuid4()),
            error=JsonRpcError.from_exception(exc),
        )
        _send_ws_response(ws, err_resp.to_json())
