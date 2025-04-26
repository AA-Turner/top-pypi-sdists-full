from __future__ import annotations

import asyncio
import base64
import inspect
import logging
import os
import subprocess
import threading
import time

from dataclasses import dataclass
from io import BytesIO, StringIO
from typing import Any, Callable, Dict, List, Optional, Set, Tuple, Type, Union

import aiohttp
import requests

# TODO: Long term, probably cannibalize thriftpy2 for the parser and the
# encoder, don't need anything else
import thriftpy2  # type: ignore[import-untyped]
import thriftpy2.parser.parser  # type: ignore[import-untyped]
from thriftpy2.protocol.binary import TBinaryProtocol  # type: ignore[import-untyped]
from thriftpy2.protocol.compact import TCompactProtocol  # type: ignore[import-untyped]
from typing_extensions import TypeAlias

log = logging.getLogger(__name__)


TAtom: TypeAlias = Union[int, float, bool, str]
TField: TypeAlias = Union[TAtom, List[TAtom]]
TLazyField: TypeAlias = Union[TField, Callable[[], TField]]
TDict: TypeAlias = Dict[str, TField]


# E.g.,
# THRIFT_DEFS["EzyangTest"] = thriftpy2.load("ex.thrift").EzyangTestLogEntry
THRIFT_DEFS: Dict[str, Type[Any]] = {}


@dataclass
class LoggerConfig:
    name: str  # includes LoggerConfig suffix
    log_entry_cls: Callable[[TDict], Any]
    supported_fields: Set[str]


Message: TypeAlias = Tuple[LoggerConfig, TDict]


class FbScribeLogger:
    """
    Batched, streaming remote logging implementation
    """

    def __init__(
        self,
        access_token: str,
        *,
        endpoint: Optional[str] = None,
        batch_window: int = 100,
        flush_interval: float = 1.0,
    ) -> None:
        """
        endpoint: Useful if you're testing on an OnDemand server
        batch_window: Max number of message to accumulate before sending HTTP request
        flush_interval: Max amount of time in seconds before sending HTTP request
        """
        self.endpoint: str = endpoint or "https://graph.facebook.com/scribe_logs"
        self.access_token: str = access_token
        self.batch_window: int = batch_window
        self.flush_interval: float = flush_interval

        self.structured_thrift = thriftpy2.load_fp(
            StringIO(
                """
struct CompactMessage {
  1: binary data;
}

struct WriteStructuredMessage {
  1: string targetName;
  2: CompactMessage message;
}
"""
            ),
            "fbscribelogger._structured_thrift",
        )

    def start(self) -> None:
        log.info("start")

        def getenv_int(name: str) -> Optional[int]:
            s = os.getenv(name)
            if s is None:
                return None
            try:
                return int(s)
            except ValueError:
                log.warning("invalid int value %s=%s", name, s)
                return None

        def getenv_bool(name: str) -> Optional[bool]:
            s = os.getenv(name)
            if s is None:
                return None
            # NB: when it's not protected, value is false, which is not
            # string falsey, so we have to match for true specifically
            return s == "true"

        commit_sha = os.getenv("SHA1")
        if commit_sha is None:
            try:
                commit_sha = subprocess.check_output(
                    ["git", "rev-parse", "HEAD"], text=True
                ).strip()
            except subprocess.CalledProcessError:
                log.warning("could not determine commit sha")

        commit_date: Optional[int] = None
        if commit_sha is not None:
            try:
                commit_date_str = subprocess.check_output(
                    ["git", "show", "-s", "--format=%cd", "--date=unix", commit_sha],
                    text=True,
                )
            except subprocess.CalledProcessError:
                log.warning("cannot compute commit date of %s", commit_sha)
            else:
                try:
                    commit_date = int(commit_date_str.strip())
                except ValueError:
                    log.warning("cannot parse git output as int: %s", commit_date_str)

        self.github_action_fields: Dict[str, Optional[TField]] = {
            "commit_sha": commit_sha,
            "commit_date": commit_date,
            "github_ref": os.getenv("GITHUB_REF"),
            "github_ref_protected": getenv_bool("GITHUB_REF_PROTECTED"),
            "github_run_attempt": os.getenv("GITHUB_RUN_ATTEMPT"),
            "github_run_id": os.getenv("GITHUB_RUN_ID"),
            "github_run_number_str": os.getenv("GITHUB_RUN_NUMBER"),
            "job_name": os.getenv("JOB_NAME"),
            "github_triggering_actor": os.getenv("GITHUB_TRIGGERING_ACTOR"),
        }

        self.pending_sends: Set[asyncio.Task[None]] = set()
        self.worker_thread_ready = threading.Event()
        self.worker_thread = threading.Thread(target=self._run_event_loop, daemon=False)
        self.worker_thread.start()
        self.worker_thread_ready.wait()
        self.watcher_thread = threading.Thread(target=self._watch_main, daemon=False)
        self.watcher_thread.start()

    def _watch_main(self) -> None:
        threading.main_thread().join()
        self.stop()

    def stop(self) -> None:
        log.info("stop")
        if self.loop.is_running():
            self.loop.call_soon_threadsafe(self.queue.put_nowait, None)
            self.worker_thread.join()

    # Data is expected to be a dataclass/dict representing the message to be
    # sent.  We do Thrift encoding in a side thread to avoid blocking main
    # process (if the Thrift encoding is in Python, this doesn't help much,
    # but if it is GIL free it can help a lot!)
    def log(self, config: LoggerConfig, payload: TDict) -> None:
        self.loop.call_soon_threadsafe(self.queue.put_nowait, (config, payload))

    # Worker thread only
    def _run_event_loop(self) -> None:
        # Make sure event loop is created on the thread that will run it
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        self.task = self.loop.create_task(self._worker())
        self.queue: asyncio.Queue[Optional[Message]] = asyncio.Queue()
        self.worker_thread_ready.set()
        self.loop.run_until_complete(self.task)

    # Worker thread only
    async def _worker(self) -> None:
        async with aiohttp.ClientSession() as session:
            # This gets set when we first buffer a message, and indicates how
            # long we will wait before we will transmit the message even if
            # our buffer size hasn't been filled
            time_to_flush = None

            # Number of messages which we will send on the next request.  This
            # isn't the full message queue; the rest of the messages are in
            # self.queue
            messages: List[Message] = []

            # Did we receive a None message, indicating to terminate the
            # worker
            terminate = False

            # NB: Even during shutdown, we will still keep doing this event
            # loop until the queue is drained.  Specifically, the None demarcates
            # when we should stop processing message.  The invariant is you
            # do an iteration of the loop every time you send a batch of messages.
            # Because of HTTP request size limits, it's important not to
            # infinitely batch messages.
            while True:
                log.debug(
                    "worker: iter time_to_flush=%s messages_len=%s",
                    time_to_flush,
                    len(messages),
                )
                start = time.time()
                try:
                    # Wait for a new message.  If there are pending messages
                    # to send, we set a timeout, after which we will
                    # unconditionally send the messages even if we haven't hit
                    # the batch window.  But if there are no pending messages,
                    # we should happily wait indefinitely and not waste CPU.
                    message = await asyncio.wait_for(
                        self.queue.get(), timeout=time_to_flush if messages else None
                    )
                except asyncio.TimeoutError:
                    log.debug("worker: timeout")
                    # Timeout occurred, get ready to send everything in messages
                    pass
                else:
                    # Check if we're told to shutdown!
                    if message is None:
                        log.debug("worker: terminate1")
                        terminate = True
                    else:
                        messages.append(message)
                        # Get the rest of the messages, in case a lot of stuff is
                        # pending.  But don't bother if we had timed out!
                        while (
                            len(messages) < self.batch_window and not self.queue.empty()
                        ):
                            message = self.queue.get_nowait()
                            if message is None:
                                log.debug("worker: terminate2")
                                terminate = True
                                break
                            else:
                                messages.append(message)

                        # Decide if we're going to wait for more messages or not
                        if len(messages) < self.batch_window:
                            end = time.time()
                            if time_to_flush is None:
                                time_to_flush = self.flush_interval
                            else:
                                time_to_flush -= end - start
                            # Not enough messages, haven't waited long enough,
                            # wait for more
                            if time_to_flush > 0:
                                log.debug("worker: batching")
                                continue

                if messages:
                    self.pending_sends.add(
                        asyncio.create_task(self._send_messages(session, messages))
                    )
                    messages = []  # NB: not clear!

                if terminate:
                    return await self._shutdown()

                # Policy decision here.  We choose to always reset time to
                # flush.  If the overflow is enough to fill the entire batch
                # window, you won't actually end up waiting, you'll work as
                # hard as you can.  So mostly this smooths out the
                # "leftovers", e.g., if your batch window size is 5, but you
                # keep getting bursts of 6 within your window.  Continuously
                # sending 5-1 requests is worse than 5-5-...
                time_to_flush = None

    async def _shutdown(self) -> None:
        log.debug("_shutdown %s", len(self.pending_sends))
        try:
            while self.pending_sends:
                # TODO: this is probably kind of crappy
                s = next(iter(self.pending_sends))
                await s
        except Exception:
            log.exception("shutting down anyway")

    def _process_message(self, message: Message) -> str:
        config, payload = message

        b = BytesIO()
        proto = TCompactProtocol(b)
        log_entry_cls = config.log_entry_cls
        if "time" not in payload:
            payload["time"] = int(time.time())
        if "weight" not in payload:
            payload["weight"] = 1
        for k, v in self.github_action_fields.items():
            if k not in payload and k in config.supported_fields and v is not None:
                payload[k] = v
        log_entry = log_entry_cls(**payload)  # type: ignore[call-arg]
        proto.write_struct(log_entry)
        # TODO: get rid of memory copy here
        cm = self.structured_thrift.CompactMessage(data=b.getvalue())
        wsm = self.structured_thrift.WriteStructuredMessage(
            targetName=config.name, message=cm
        )

        b2 = BytesIO()
        proto2 = TBinaryProtocol(b2)
        proto2.write_struct(wsm)
        return base64.b64encode(b2.getvalue()).decode("ascii")

    async def _send_messages(
        self, session: aiohttp.ClientSession, messages: List[Message]
    ) -> None:
        try:
            logs = [
                {
                    "category": "UNUSED",
                    "message": self._process_message(m),
                }
                for m in messages
            ]

            # This is a hack.  aiohttp doesn't work when the main thread has
            # shut down because it uses concurrent.futures which doesn't work
            # when the main thread is dead.  We still want to send the
            # requests though.  Do it more slowly serially.
            # TODO: In principle we could do all the final dumping in parallel
            # using whatever it is requests does
            if not threading.main_thread().is_alive():
                log.info("send_messages: atexit")
                sync_response = requests.post(
                    self.endpoint,
                    params={
                        "structured": "true",
                        "access_token": self.access_token,
                    },
                    json={"logs": logs},
                )
                if sync_response.status_code != 200:
                    log.error("send_messages: atexit err %s", sync_response)
                else:
                    log.debug("send_messages: atexit ok")
                return

            async with session.post(
                self.endpoint,
                params={
                    "structured": "true",
                    "access_token": self.access_token,
                },
                json={"logs": logs},
            ) as response:
                if response.status != 200:
                    log.error("send_messages: err %s", response)
                else:
                    log.debug("send_messages: ok")
        except Exception:
            log.exception("send_messages: exception")
            log.error("send_messages: the exception above IS SUPPRESSED")
        finally:
            t = asyncio.current_task()
            assert t is not None
            self.pending_sends.remove(t)


_uninit = object()
SCRIBE_LOG: Union[object, FbScribeLogger, None] = _uninit


def make_scribe_logger(name: str, thrift_src: str) -> Callable[..., None]:
    assert not name.endswith("LoggerConfig")

    log_entry_cls = getattr(
        thriftpy2.load_fp(StringIO(thrift_src), "fbscribelogger." + name + "_thrift"),
        name + "LogEntry",
    )

    config = LoggerConfig(
        name=name + "LoggerConfig",
        log_entry_cls=log_entry_cls,
        supported_fields=set(inspect.signature(log_entry_cls).parameters.keys()),
    )

    def scribe_logger(**kwargs: TLazyField) -> None:
        global SCRIBE_LOG
        if SCRIBE_LOG is _uninit:
            access_token = os.getenv("SCRIBE_GRAPHQL_ACCESS_TOKEN")
            endpoint = os.getenv("SCRIBE_GRAPHQL_ENDPOINT")

            if access_token is not None:
                logger = FbScribeLogger(
                    access_token,
                    endpoint=endpoint,
                )
                logger.start()
                SCRIBE_LOG = logger
            else:
                # Don't keep uselessly banging on the envvar
                log.debug("no access token, disabling fbscribelogger")
                SCRIBE_LOG = None
                return

        if isinstance(SCRIBE_LOG, FbScribeLogger):
            kwargs = {k: v() if callable(v) else v for k, v in kwargs.items()}
            SCRIBE_LOG.log(config, kwargs)  # type: ignore[arg-type]

    return scribe_logger
