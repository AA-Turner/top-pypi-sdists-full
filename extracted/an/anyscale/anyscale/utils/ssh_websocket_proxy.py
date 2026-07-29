#!/usr/bin/env python3
import asyncio
import logging
import os
import sys

from packaging import version
import websockets
import websockets.exceptions


# Define global constants
DEFAULT_CHUNK_SIZE = 4096
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(funcName)s - %(message)s"

# Configure logging
DEBUG_ENABLED = os.environ.get("ANYSCALE_SSH_DEBUG") == "1"
LOG_LEVEL = logging.DEBUG if DEBUG_ENABLED else logging.INFO
logging.basicConfig(level=LOG_LEVEL, format=LOG_FORMAT, stream=sys.stderr)
logger = logging.getLogger(__name__)

# websockets v14 renamed the rejected-handshake exception from InvalidStatusCode
# (legacy) to InvalidStatus (asyncio impl); recognize whichever exists (CI-1744).
# `websockets.exceptions` is imported explicitly above because websockets<14 lazily
# exposes submodules -- without that import this lookup raises AttributeError at
# module load on the very old versions this fix is meant to support.
_INVALID_STATUS_EXC_CANDIDATES = (
    getattr(websockets.exceptions, "InvalidStatus", None),
    getattr(websockets.exceptions, "InvalidStatusCode", None),
)
_INVALID_STATUS_EXCEPTIONS = tuple(
    exc for exc in _INVALID_STATUS_EXC_CANDIDATES if exc is not None
)


def _additional_headers_kwarg() -> str:
    # websockets>=14 binds connect() to the asyncio impl (additional_headers);
    # older binds legacy (extra_headers) and raises TypeError otherwise (CI-1744).
    # 13.x ships the asyncio module but still binds legacy, so gate on version.
    try:
        use_new = version.parse(websockets.__version__) >= version.parse("14.0")
    except Exception:  # noqa: BLE001
        # An unparseable version string shouldn't crash the proxy; assume modern.
        use_new = True
    return "additional_headers" if use_new else "extra_headers"


async def pump(stream_reader: asyncio.StreamReader, send_func):
    logger.debug("pump: started")
    try:
        while True:
            logger.debug("pump: trying to read from stream_reader")
            chunk = await stream_reader.read(DEFAULT_CHUNK_SIZE)
            logger.debug(
                f"pump: read {len(chunk) if chunk else 0} bytes from stream_reader"
            )
            if not chunk:  # EOF
                logger.debug("pump: EOF from stream_reader, closing send_func")
                await send_func.close()
                logger.debug("pump: send_func closed")
                return
            logger.debug(f"pump: sending {len(chunk)} bytes to websocket")
            await send_func(chunk)
            logger.debug("pump: sent to websocket")
    except websockets.ConnectionClosedOK:
        logger.debug("pump: ConnectionClosedOK")
    except asyncio.CancelledError:
        logger.debug("pump: CancelledError")
        raise
    except Exception:
        logger.exception("pump: Exception encountered")
        if not getattr(send_func, "closed", False):
            logger.debug("pump: Exception, closing send_func")
            await send_func.close()
            logger.debug("pump: send_func closed due to exception")
        raise
    finally:
        logger.debug("pump: finished")


async def drain(ws_receive_func):
    logger.debug("drain: started")
    try:
        async for msg in ws_receive_func:
            logger.debug(
                f"drain: received {len(msg) if isinstance(msg, bytes) else type(msg)} from websocket"
            )
            if isinstance(msg, bytes):
                sys.stdout.buffer.write(msg)
                sys.stdout.buffer.flush()
                logger.debug("drain: wrote to stdout and flushed")
            else:
                logger.warning(f"Received unexpected non-bytes message: {type(msg)}")
    except websockets.ConnectionClosedOK:
        logger.debug("drain: ConnectionClosedOK")
    except asyncio.CancelledError:
        logger.debug("drain: CancelledError")
        raise
    except Exception:
        logger.exception("drain: Exception encountered")
        raise
    finally:
        logger.debug("drain: finished")


async def main():
    if len(sys.argv) < 2:
        logger.debug("WebSocket URL must be provided as the first argument.")
        sys.exit(1)

    ws_url = sys.argv[1]
    logger.debug(f"WebSocket URL: {ws_url}")

    # Check for optional token argument
    auth_token = None
    if len(sys.argv) >= 3:
        auth_token = sys.argv[2]
        logger.debug("Authentication token provided as second argument")

    loop = asyncio.get_running_loop()
    reader = asyncio.StreamReader(loop=loop)
    protocol = asyncio.StreamReaderProtocol(reader, loop=loop)
    await loop.connect_read_pipe(lambda: protocol, sys.stdin)
    logger.debug("stdin connected to StreamReader")

    # Prepare additional headers if token is provided
    additional_headers = {}
    if auth_token:
        additional_headers["Authorization"] = f"Bearer {auth_token}"
        logger.debug("Added Authorization header with Bearer token")

    connect_kwargs = {
        # The header-kwarg name differs across websockets versions (CI-1744).
        _additional_headers_kwarg(): additional_headers,
        # An SSH-tunnel upgrade legitimately exceeds the 10s default under load.
        "open_timeout": None,
        # The server sends keepalive pings; rely on those for liveness. Safe
        # only because the server keepalive detects a dead peer.
        "ping_interval": None,
    }

    try:
        logger.debug("Attempting to connect to websocket...")
        async with websockets.connect(ws_url, **connect_kwargs) as ws:
            logger.debug("Connected to websocket successfully")
            pump_task = asyncio.create_task(pump(reader, ws.send))
            drain_task = asyncio.create_task(drain(ws))

            _done, pending = await asyncio.wait(
                [pump_task, drain_task], return_when=asyncio.FIRST_COMPLETED,
            )

            # Convert pending set to a list to maintain order for results processing
            pending_list = list(pending)

            for task in pending_list:  # Iterate over the list
                logger.debug(f"Cancelling pending task {task.get_name()}")
                task.cancel()

            # Wait for pending tasks to finish cancellation
            # Pass the list of pending tasks to gather
            results = await asyncio.gather(*pending_list, return_exceptions=True)

            for i, result in enumerate(results):
                if isinstance(result, Exception) and not isinstance(
                    result, asyncio.CancelledError
                ):
                    # Use pending_list[i] to get the corresponding task
                    task_name = (
                        pending_list[i].get_name()
                        if pending_list[i].get_name()
                        else "unnamed task"
                    )
                    logger.debug(
                        f"Pending task '{task_name}' raised an exception: {result!r}"
                    )
            logger.debug("Pump and drain tasks finished or cancelled.")

    except asyncio.TimeoutError:
        logger.error("Connection to websocket timed out.")
        sys.exit(1)
    except Exception:
        logger.exception("Exception in main connection/task management logic")
        raise  # Re-raise after logging
    finally:
        logger.debug("main: finished")


if __name__ == "__main__":
    try:
        logger.debug("Starting proxy script")
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.debug("KeyboardInterrupt received. Exiting.")
        # Python's default handler for KeyboardInterrupt will exit (usually with code 130)
    except SystemExit as e:
        logger.debug(f"SystemExit called with code {e.code}")
        sys.exit(e.code)  # Propagate the intended exit code
    except _INVALID_STATUS_EXCEPTIONS as e_is:
        # Status attr differs: legacy .status_code vs new-asyncio .response.status_code.
        response = getattr(e_is, "response", None)
        status = getattr(e_is, "status_code", None) or getattr(
            response, "status_code", None
        )
        logger.debug(
            f"Unhandled WebSocket invalid-status error: {e_is!r}, Status code: {status}"
        )
        sys.exit(1)
    except (websockets.exceptions.WebSocketException, OSError) as e_wso:
        # Handle other WebSocket and OS errors
        logger.debug(f"Unhandled WebSocket/OS error: {e_wso!r}")
        sys.exit(1)
    except Exception as e_unhandled:  # noqa: BLE001 # Catch any other unexpected exceptions
        logger.debug(f"Unhandled exception: {e_unhandled!r}", exc_info=True)
        sys.exit(1)
    finally:
        logger.debug("Proxy script exiting")
