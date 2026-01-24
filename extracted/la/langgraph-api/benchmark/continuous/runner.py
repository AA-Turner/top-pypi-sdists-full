#!/usr/bin/env python3
"""
Continuous stress test for long-running runs.

Maintains a target pool of running threads, replacing failed ones automatically.
"""

import asyncio
import json
import logging
import os
import signal
import sys
import time
from dataclasses import dataclass, field
from datetime import UTC, datetime
from http.server import BaseHTTPRequestHandler, HTTPServer
from threading import Thread

import click
import httpx
import structlog
from datadog_api_client import ApiClient, Configuration
from datadog_api_client.v1.api.metrics_api import MetricsApi as MetricsApiV1
from datadog_api_client.v1.model.distribution_point import DistributionPoint
from datadog_api_client.v1.model.distribution_points_payload import (
    DistributionPointsPayload,
)
from datadog_api_client.v1.model.distribution_points_series import (
    DistributionPointsSeries,
)
from datadog_api_client.v2.api.metrics_api import MetricsApi as MetricsApiV2
from datadog_api_client.v2.model.metric_intake_type import MetricIntakeType
from datadog_api_client.v2.model.metric_payload import MetricPayload
from datadog_api_client.v2.model.metric_point import MetricPoint
from datadog_api_client.v2.model.metric_series import MetricSeries
from dateutil import parser as dateutil_parser
from langgraph_sdk import get_client

logger = structlog.get_logger("runner")
health_logger = structlog.get_logger("health")
metrics_logger = structlog.get_logger("metrics")


# Run configuration
MAINTENANCE_INTERVAL_SECONDS = (
    5.0  # How often to check for dead runs and start replacements
)

# Metrics shipping configuration (Datadog)
METRICS_INTERVAL_SECONDS = 60.0
DATADOG_SITE = os.getenv("DD_SITE", "us5.datadoghq.com")
METRIC_THREADS_ACTIVE = "langsmith_deployment.continuous.threads.active"
METRIC_THREADS_FAILED = "langsmith_deployment.continuous.threads.failed"
METRIC_EVENTS = "langsmith_deployment.continuous.events"
METRIC_FAILURES = "langsmith_deployment.continuous.failures"
METRIC_DROPPED_CHUNKS = "langsmith_deployment.continuous.threads.faults.dropped_chunks"
METRIC_OUT_OF_ORDER_RUNS = (
    "langsmith_deployment.continuous.threads.faults.out_of_order_runs"
)
METRIC_MALFORMED_CHUNKS = (
    "langsmith_deployment.continuous.threads.faults.malformed_chunks"
)
METRIC_LATENCY = "langsmith_deployment.continuous.threads.latency"


class HealthCheckHandler(BaseHTTPRequestHandler):
    """Minimal HTTP handler for Cloud Run health checks."""

    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(b"OK")

    def log_message(self, format, *args):
        health_logger.info("health_check", message=format % args)


def start_health_check_server(port: int = 8080):
    """Start HTTP server for Cloud Run health checks in background thread."""
    server = HTTPServer(("", port), HealthCheckHandler)
    thread = Thread(target=server.serve_forever, daemon=True)
    thread.start()
    health_logger.info("health_check_started", port=port)


@dataclass
class RunMetrics:
    """Metrics tracked per run."""

    run_id: str | None = None
    events_received: int = 0
    connection_failures: int = 0
    last_error: str | None = None

    # Correctness tracking
    message_numbers: list[int] = field(default_factory=list)
    total_messages: int | None = None
    latencies: list[float] = field(default_factory=list)
    malformed_chunks: int = 0

    dropped_chunks: int = 0
    out_of_order: bool = False


def _process_values_event(
    data: dict,
    receive_time: datetime,
    metrics: RunMetrics,
    log: structlog.BoundLogger,
) -> None:
    """Process a 'values' SSE event and update metrics for correctness tracking."""
    current_message = data.get("current_message")
    total_messages = data.get("total_messages")
    last_message_time_str = data.get("last_message_time")

    if current_message is None or total_messages is None:
        metrics.malformed_chunks += 1
        return

    metrics.message_numbers.append(current_message)

    if metrics.total_messages is None:
        metrics.total_messages = total_messages

    if last_message_time_str:
        try:
            send_time = dateutil_parser.isoparse(last_message_time_str)
            latency = (receive_time - send_time).total_seconds()
            metrics.latencies.append(latency)
        except Exception as e:
            metrics.malformed_chunks += 1
            log.warning(
                "malformed_timestamp",
                error=str(e),
                timestamp=last_message_time_str,
            )


def _analyze_correctness(metrics: RunMetrics) -> None:
    """Analyze message sequence for dropped or out-of-order chunks."""
    if metrics.total_messages is None or not metrics.message_numbers:
        return

    expected_sequence = list(range(metrics.total_messages))

    # Check if received messages match expected prefix
    if metrics.message_numbers != expected_sequence[: len(metrics.message_numbers)]:
        metrics.out_of_order = True

    # Count missing messages
    metrics.dropped_chunks = len(set(expected_sequence) - set(metrics.message_numbers))


async def stream_run(
    thread_id: str,
    assistant_id: str,
    base_url: str,
    api_key: str | None,
    metrics: RunMetrics,
) -> None:
    """
    Stream a run in a thread.

    Starts a new streaming run on the given thread and consumes all events
    until completion or cancellation. The SDK handles SSE reconnection internally.
    Updates the provided metrics object in-place.
    """
    log = structlog.get_logger("run").bind(
        thread_id=thread_id, assistant_id=assistant_id
    )
    client = get_client(url=base_url, api_key=api_key)
    run_id = None

    try:
        log.info("run_starting")

        run_stream = client.runs.stream(
            thread_id,
            assistant_id,
            input={},
            stream_mode=["values", "messages"],
        )

        # Consume run (SDK handles reconnection internally)
        async for chunk in run_stream:
            receive_time = datetime.now(UTC)
            log.info("received_chunk")

            # Capture run_id from first chunk if available
            if (
                run_id is None
                and hasattr(chunk, "data")
                and isinstance(chunk.data, dict)
            ):
                run_id = chunk.data.get("run_id")
                if run_id:
                    metrics.run_id = run_id
                    log = log.bind(run_id=run_id)
                    log.info("run_started", run_id=run_id)

            # Extract chunk data for correctness tracking
            if (
                hasattr(chunk, "event")
                and chunk.event == "values"
                and hasattr(chunk, "data")
                and isinstance(chunk.data, dict)
            ):
                _process_values_event(chunk.data, receive_time, metrics, log)

            metrics.events_received += 1

        _analyze_correctness(metrics)

        log.info(
            "run_completed",
            dropped_chunks=metrics.dropped_chunks,
            out_of_order=metrics.out_of_order,
            malformed_chunks=metrics.malformed_chunks,
        )

    except asyncio.CancelledError:
        log.debug("run_cancelled")
        raise

    except Exception as e:
        metrics.connection_failures += 1
        metrics.last_error = str(e)
        log.exception("run_failed", error=str(e))


async def stream_run_raw(
    thread_id: str,
    assistant_id: str,
    base_url: str,
    api_key: str | None,
    metrics: RunMetrics,
) -> None:
    """
    Stream a run using raw HTTP/SSE without SDK retry logic.

    This measures the true performance of the system without SDK retries masking issues.
    """
    log = structlog.get_logger("run").bind(
        thread_id=thread_id, assistant_id=assistant_id
    )
    run_id = None

    headers = {
        "Accept": "text/event-stream",
        "Content-Type": "application/json",
    }
    if api_key:
        headers["X-Api-Key"] = api_key

    url = f"{base_url.rstrip('/')}/threads/{thread_id}/runs/stream"
    body = {
        "assistant_id": assistant_id,
        "input": {},
        "stream_mode": ["values", "messages"],
    }

    try:
        log.info("run_starting")

        async with (
            httpx.AsyncClient(timeout=httpx.Timeout(None)) as client,
            client.stream("POST", url, json=body, headers=headers) as response,
        ):
            response.raise_for_status()

            event_type = None
            data_buffer = []

            async for line in response.aiter_lines():
                if line.startswith("event:"):
                    event_type = line[6:].strip()
                elif line.startswith("data:"):
                    data_buffer.append(line[5:].strip())
                elif line == "" and data_buffer:
                    # End of event, process it
                    receive_time = datetime.now(UTC)
                    log.info("received_chunk")

                    try:
                        data_str = "\n".join(data_buffer)
                        data = json.loads(data_str) if data_str else {}
                    except json.JSONDecodeError:
                        data = {}

                    data_buffer = []

                    # Capture run_id from first chunk
                    if run_id is None and isinstance(data, dict):
                        run_id = data.get("run_id")
                        if run_id:
                            metrics.run_id = run_id
                            log = log.bind(run_id=run_id)
                            log.info("run_started", run_id=run_id)

                    # Extract chunk data for correctness tracking
                    if event_type == "values" and isinstance(data, dict):
                        _process_values_event(data, receive_time, metrics, log)

                    metrics.events_received += 1
                    event_type = None

        _analyze_correctness(metrics)

        log.info(
            "run_completed",
            dropped_chunks=metrics.dropped_chunks,
            out_of_order=metrics.out_of_order,
            malformed_chunks=metrics.malformed_chunks,
        )

    except asyncio.CancelledError:
        log.debug("run_cancelled")
        raise

    except Exception as e:
        metrics.connection_failures += 1
        metrics.last_error = str(e)
        log.exception("run_failed", error=str(e))


class ContinuousRunner:
    """
    Manages a pool of long-running threads.

    Maintains target number of active runs, replacing failed ones automatically.
    """

    def __init__(
        self,
        base_url: str,
        assistant_id: str,
        target_threads: int,
        api_key: str | None = None,
        dd_api_key: str | None = None,
        deployment_name: str | None = None,
        raw_sse: bool = False,
    ):
        self.base_url = base_url
        self.assistant_id = assistant_id
        self.target_threads = target_threads
        self.api_key = api_key
        self.dd_api_key = dd_api_key
        self.raw_sse = raw_sse

        # Extract deployment name from URL if not provided
        if deployment_name:
            self.deployment_name = deployment_name
        else:
            # Try to extract from URL like "https://foo-bar.staging.langgraph.app"
            from urllib.parse import urlparse

            parsed = urlparse(base_url)
            self.deployment_name = parsed.hostname or "unknown"

        self.client = get_client(url=base_url, api_key=api_key)

        # Track active threads: {thread_id: (task, metrics)}
        self.threads: dict[str, tuple[asyncio.Task, RunMetrics]] = {}

        self._stop = False
        self._start_time = time.time()

    async def start(self):
        """Start the continuous stress test."""
        mode = "raw_sse" if self.raw_sse else "sdk"
        logger.info("runner_starting", target_threads=self.target_threads, mode=mode)

        loop = asyncio.get_running_loop()
        for sig in (signal.SIGTERM, signal.SIGINT):
            loop.add_signal_handler(sig, lambda: setattr(self, "_stop", True))

        try:
            maintenance_task = asyncio.create_task(self._maintenance_loop())
            metrics_task = asyncio.create_task(self._metrics_loop())

            while not self._stop:
                await asyncio.sleep(1)

            logger.info("runner_stopping")

            # Send cancel signals to all active runs (fire and forget)
            cancel_tasks = []
            for thread_id, (_, metrics) in self.threads.items():
                if metrics.run_id:
                    logger.info(
                        "canceling_run", thread_id=thread_id, run_id=metrics.run_id
                    )
                    cancel_tasks.append(
                        asyncio.create_task(
                            self.client.runs.cancel(
                                thread_id, metrics.run_id, wait=False
                            )
                        )
                    )

            if cancel_tasks:
                logger.info("canceling_runs", count=len(cancel_tasks))
                await asyncio.gather(*cancel_tasks, return_exceptions=True)

            # Cancel local tasks
            maintenance_task.cancel()
            metrics_task.cancel()
            for task, _ in self.threads.values():
                task.cancel()

            # Wait for all to finish
            await asyncio.gather(
                maintenance_task,
                metrics_task,
                *[task for task, _ in self.threads.values()],
                return_exceptions=True,
            )

        except Exception:
            logger.exception("runner_fatal_error")
            raise
        finally:
            logger.info("runner_stopped")

    async def _upload_to_datadog(self):
        """Upload metrics to Datadog and clean up completed runs."""
        if not self.dd_api_key:
            return

        try:
            timestamp = int(time.time())

            # Count current active/failed threads
            active = sum(1 for task, _ in self.threads.values() if not task.done())
            failed = sum(
                1
                for task, _ in self.threads.values()
                if task.done() and task.exception()
            )

            # Common tags for all metrics
            common_tags = [f"deployment:{self.deployment_name}"]

            # Build metric series
            series = [
                MetricSeries(
                    metric=METRIC_THREADS_ACTIVE,
                    type=MetricIntakeType.GAUGE,
                    points=[MetricPoint(timestamp=timestamp, value=float(active))],
                    tags=common_tags,
                ),
                MetricSeries(
                    metric=METRIC_THREADS_FAILED,
                    type=MetricIntakeType.GAUGE,
                    points=[MetricPoint(timestamp=timestamp, value=float(failed))],
                    tags=common_tags,
                ),
            ]

            # Collect metrics only from completed runs
            completed_thread_ids = []
            latency_distribution_series = []

            for thread_id, (task, metrics) in self.threads.items():
                if not task.done():
                    continue

                completed_thread_ids.append(thread_id)

                # Build tags for this run
                tags = [f"deployment:{self.deployment_name}"]

                # Send all count metrics for this completed run
                count_metrics = [
                    (METRIC_EVENTS, metrics.events_received),
                    (METRIC_FAILURES, metrics.connection_failures),
                    (METRIC_DROPPED_CHUNKS, metrics.dropped_chunks),
                    (METRIC_OUT_OF_ORDER_RUNS, 1.0 if metrics.out_of_order else 0),
                    (METRIC_MALFORMED_CHUNKS, metrics.malformed_chunks),
                ]

                for metric_name, value in count_metrics:
                    if value > 0:
                        series.append(
                            MetricSeries(
                                metric=metric_name,
                                type=MetricIntakeType.COUNT,
                                points=[
                                    MetricPoint(timestamp=timestamp, value=float(value))
                                ],
                                tags=tags,
                            )
                        )

                # Collect latency distribution for this run
                # DistributionPoint format: [timestamp, [values]]
                if metrics.latencies:
                    latency_distribution_series.append(
                        DistributionPointsSeries(
                            metric=METRIC_LATENCY,
                            points=[DistributionPoint([timestamp, metrics.latencies])],
                            tags=tags,
                        )
                    )

            # Remove completed threads (metrics already sent)
            for thread_id in completed_thread_ids:
                del self.threads[thread_id]

            if completed_thread_ids:
                metrics_logger.info(
                    "sent_final_metrics", completed_runs=len(completed_thread_ids)
                )

            configuration = Configuration()
            configuration.server_variables["site"] = DATADOG_SITE
            configuration.api_key["apiKeyAuth"] = self.dd_api_key

            with ApiClient(configuration) as api_client:
                # Submit count metrics
                if series:
                    count_api_instance = MetricsApiV2(api_client)
                    body = MetricPayload(series=series)
                    response = count_api_instance.submit_metrics(body=body)

                    if hasattr(response, "errors") and response.errors:
                        logger.warning("datadog_errors", errors=response.errors)

                # Submit distribution metrics
                if latency_distribution_series:
                    distribution_api_instance = MetricsApiV1(api_client)
                    dist_body = DistributionPointsPayload(
                        series=latency_distribution_series
                    )
                    dist_response = (
                        distribution_api_instance.submit_distribution_points(
                            body=dist_body
                        )
                    )

                    if hasattr(dist_response, "errors") and dist_response.errors:
                        logger.warning("datadog_errors", errors=dist_response.errors)

        except Exception as e:
            logger.exception("datadog_upload_failed", error=str(e))

    async def _maintenance_loop(self):
        """Periodically check for completed threads and start replacements."""
        try:
            while not self._stop:
                # Clean up completed threads (if no DD key, we just log; otherwise _upload_to_datadog handles cleanup)
                if not self.dd_api_key:
                    completed_thread_ids = [
                        thread_id
                        for thread_id, (task, _) in self.threads.items()
                        if task.done()
                    ]
                    for thread_id in completed_thread_ids:
                        del self.threads[thread_id]

                    if completed_thread_ids:
                        logger.info(
                            "cleaned_up_threads", count=len(completed_thread_ids)
                        )

                # Count only active (not done) threads
                active = sum(1 for task, _ in self.threads.values() if not task.done())
                deficit = self.target_threads - active

                if deficit > 0:
                    logger.info(
                        "starting_threads",
                        deficit=deficit,
                        active=active,
                        target=self.target_threads,
                    )
                    for _ in range(deficit):
                        await self._start_run()

                await asyncio.sleep(MAINTENANCE_INTERVAL_SECONDS)

        except asyncio.CancelledError:
            pass

    async def _start_run(self):
        """Start a new run on a new thread."""
        # Create thread
        thread = await self.client.threads.create()
        thread_id = thread["thread_id"]

        # Start run task - use raw SSE or SDK based on flag
        metrics = RunMetrics()
        stream_fn = stream_run_raw if self.raw_sse else stream_run
        task = asyncio.create_task(
            stream_fn(
                thread_id=thread_id,
                assistant_id=self.assistant_id,
                base_url=self.base_url,
                api_key=self.api_key,
                metrics=metrics,
            )
        )

        # Store
        self.threads[thread_id] = (task, metrics)
        logger.debug("run_started", thread_id=thread_id)

    async def _metrics_loop(self):
        """Periodically collect and export metrics."""
        try:
            while not self._stop:
                await self._upload_to_datadog()
                await asyncio.sleep(METRICS_INTERVAL_SECONDS)

        except asyncio.CancelledError:
            pass


@click.command()
@click.option(
    "--base-url",
    envvar="BASE_URL",
    default="http://localhost:2024",
    help="Base URL of LangGraph API",
)
@click.option(
    "--assistant-id",
    envvar="ASSISTANT_ID",
    default="long_running",
    help="Assistant ID to test against",
)
@click.option(
    "--num-threads",
    envvar="TARGET_THREADS",
    type=int,
    default=1000,
    help="Target number of concurrent threads",
)
@click.option(
    "--deployment-name",
    envvar="DEPLOYMENT_NAME",
    default=None,
    help="Name for this deployment (used in Datadog tags). Defaults to hostname from base URL.",
)
@click.option(
    "--raw-sse",
    is_flag=True,
    default=False,
    help="Use raw HTTP/SSE instead of SDK (no automatic retries). Measures true system performance.",
)
def main(
    base_url: str,
    assistant_id: str,
    num_threads: int,
    deployment_name: str | None,
    raw_sse: bool,
):
    """Continuous long-running SSE stress test for LangGraph API."""

    # Configure structlog for JSONL logging
    structlog.configure(
        processors=[
            structlog.stdlib.add_log_level,
            structlog.processors.TimeStamper(fmt="iso", utc=True),
            structlog.processors.JSONRenderer(),
        ],
        wrapper_class=structlog.make_filtering_bound_logger(logging.INFO),
        context_class=dict,
        logger_factory=structlog.PrintLoggerFactory(file=sys.stdout),
        cache_logger_on_first_use=True,
    )

    # Load API keys from environment
    api_key = os.getenv("LANGSMITH_API_KEY")
    dd_api_key = os.getenv("DD_API_KEY")

    # Start health check server for Cloud Run
    port = int(os.getenv("PORT", "8080"))
    start_health_check_server(port)

    runner = ContinuousRunner(
        base_url=base_url,
        assistant_id=assistant_id,
        target_threads=num_threads,
        api_key=api_key,
        dd_api_key=dd_api_key,
        deployment_name=deployment_name,
        raw_sse=raw_sse,
    )

    asyncio.run(runner.start())


if __name__ == "__main__":
    main()
