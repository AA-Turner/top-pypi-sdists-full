"""
Spotlight Client

Main client for sending metrics and exceptions to Spotlight API.
"""

import atexit
import logging
import os
import threading
import time
from datetime import datetime
from typing import Optional, List, Dict, Any
from queue import Queue, Empty
import httpx

from .models import RequestMetric, MetricsBatch
from .validators import ValidatorRegistry
from .exceptions import ExceptionInfo, Breadcrumb, capture_exception

logger = logging.getLogger("spotlight")


class Spotlight:
    """
    Main Spotlight client.

    Usage:
        spotlight = Spotlight(api_key="sp_xxx")
        spotlight.instrument(app)  # Auto-instrument FastAPI

        # Manual exception capture
        try:
            risky_operation()
        except Exception as e:
            spotlight.capture_exception(e)
            raise
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        api_url: Optional[str] = None,
        service_slug: Optional[str] = None,
        environment: Optional[str] = None,
        release: Optional[str] = None,
        batch_size: int = 100,
        flush_interval: float = 5.0,
        enabled: bool = True,
        tags: Optional[Dict[str, str]] = None,
    ):
        """
        Initialize Spotlight client.

        Args:
            api_key: API key (or set SPOTLIGHT_API_KEY env var)
            api_url: Spotlight API URL (or set SPOTLIGHT_API_URL env var)
            service_slug: Service identifier (or set SPOTLIGHT_SERVICE env var)
            environment: Environment name (production, staging, development)
            release: Release/version string
            batch_size: Max metrics to batch before sending
            flush_interval: Seconds between batch flushes
            enabled: Set to False to disable (useful for local dev)
            tags: Default tags to add to all events
        """
        self.api_key = api_key or os.getenv("SPOTLIGHT_API_KEY")
        self.api_url = (api_url or os.getenv("SPOTLIGHT_API_URL", "http://localhost:8100")).rstrip("/")
        self.service_slug = service_slug or os.getenv("SPOTLIGHT_SERVICE", "unknown")
        self.environment = environment or os.getenv("SPOTLIGHT_ENVIRONMENT", "production")
        self.release = release or os.getenv("SPOTLIGHT_RELEASE")
        self.batch_size = batch_size
        self.flush_interval = flush_interval
        self.enabled = enabled
        self.tags = tags or {}

        # Validator registry
        self.validators = ValidatorRegistry()

        # Metrics queue for async batching
        self._metrics_queue: Queue = Queue()
        self._exceptions_queue: Queue = Queue()
        self._events_queue: Queue = Queue()
        self._flush_thread: Optional[threading.Thread] = None
        self._stop_event = threading.Event()

        if self.enabled and self.api_key:
            self._start_flush_thread()
            atexit.register(self.shutdown)
        elif self.enabled and not self.api_key:
            logger.warning("Spotlight API key not set. Metrics will not be sent.")

    def _start_flush_thread(self):
        """Start background thread for flushing metrics."""
        self._flush_thread = threading.Thread(target=self._flush_loop, daemon=True)
        self._flush_thread.start()

    def _flush_loop(self):
        """Background loop that flushes metrics periodically."""
        while not self._stop_event.is_set():
            time.sleep(self.flush_interval)
            self._flush()

    def _flush(self):
        """Flush queued metrics and exceptions to API."""
        if not self.enabled or not self.api_key:
            return

        self._flush_metrics()
        self._flush_exceptions()
        self._flush_events()

    def _flush_metrics(self):
        """Flush metrics queue."""
        requests = []
        while len(requests) < self.batch_size:
            try:
                metric = self._metrics_queue.get_nowait()
                requests.append(metric)
            except Empty:
                break

        if not requests:
            return

        batch = MetricsBatch(
            service_slug=self.service_slug,
            requests=requests,
            environment=self.environment,  # Add this
        )

        try:
            with httpx.Client(timeout=10.0) as client:
                response = client.post(
                    f"{self.api_url}/api/v1/ingest",
                    json=batch.to_dict(),
                    headers={"Authorization": f"Bearer {self.api_key}"},
                )
                if response.status_code != 200:
                    logger.error(f"Spotlight ingest failed: {response.status_code} {response.text}")
        except Exception as e:
            logger.error(f"Spotlight ingest error: {e}")

    def _flush_exceptions(self):
        """Flush exceptions queue."""
        exceptions = []
        while len(exceptions) < 50:  # Smaller batch for exceptions
            try:
                exc_info = self._exceptions_queue.get_nowait()
                exceptions.append(exc_info)
            except Empty:
                break

        if not exceptions:
            return

        payload = {
            "service_slug": self.service_slug,
            "exceptions": [e.to_dict() for e in exceptions],
        }

        try:
            with httpx.Client(timeout=10.0) as client:
                response = client.post(
                    f"{self.api_url}/api/v1/ingest/exceptions",
                    json=payload,
                    headers={"Authorization": f"Bearer {self.api_key}"},
                )
                if response.status_code != 200:
                    logger.error(f"Spotlight exception ingest failed: {response.status_code} {response.text}")
        except Exception as e:
            logger.error(f"Spotlight exception ingest error: {e}")

    def _flush_events(self):
        """Flush events queue."""
        events = []
        while len(events) < self.batch_size:
            try:
                event = self._events_queue.get_nowait()
                events.append(event)
            except Empty:
                break

        if not events:
            return

        payload = {
            "service_slug": self.service_slug,
            "environment": self.environment,
            "events": events,
        }

        try:
            with httpx.Client(timeout=10.0) as client:
                response = client.post(
                    f"{self.api_url}/api/v1/ingest/events",
                    json=payload,
                    headers={"Authorization": f"Bearer {self.api_key}"},
                )
                if response.status_code != 200:
                    logger.error(f"Spotlight events ingest failed: {response.status_code} {response.text}")
        except Exception as e:
            logger.error(f"Spotlight events ingest error: {e}")

    def track(
        self,
        event: str,
        data: Dict[str, Any],
        request_id: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ):
        """
        Track a custom event for validation.

        Events are sent async and validated server-side based on
        configured validators.

        Args:
            event: Event type (e.g., "conversation", "recommendation", "api_call")
            data: Event data to validate
            request_id: Optional ID to link with other events
            metadata: Optional metadata

        Usage:
            # Track a conversation
            spotlight.track(
                event="conversation",
                data={
                    "user_message": "What pills should I take?",
                    "agent_response": "Based on your symptoms...",
                    "confidence": 0.85,
                    "recommendations": ["pill_a", "pill_b"]
                }
            )

            # Track an API call
            spotlight.track(
                event="api_call",
                data={
                    "endpoint": "/generate",
                    "latency_ms": 234,
                    "status_code": 200
                }
            )
        """
        if not self.enabled:
            return

        event_payload = {
            "event_type": event,
            "data": data,
            "request_id": request_id,
            "metadata": metadata or {},
            "timestamp": datetime.utcnow().isoformat(),
        }

        self._events_queue.put(event_payload)

        # Flush if queue is getting full
        if self._events_queue.qsize() >= self.batch_size:
            self._flush_events()


    def track_request(
        self,
        endpoint: str,
        method: str,
        status_code: int,
        latency_ms: int,
        error_type: Optional[str] = None,
        error_message: Optional[str] = None,
        request_data: Optional[dict] = None,
        response_data: Optional[dict] = None,
        metadata: Optional[dict] = None,
    ):
        """Track a single request."""
        if not self.enabled:
            return

        # Run validators
        validations = []
        if request_data is not None and response_data is not None:
            validations = self.validators.run_validators(
                endpoint=endpoint,
                method=method,
                request_data=request_data,
                response_data=response_data,
            )

        metric = RequestMetric(
            endpoint=endpoint,
            method=method,
            status_code=status_code,
            latency_ms=latency_ms,
            timestamp=datetime.utcnow(),
            error_type=error_type,
            error_message=error_message,
            validations=validations,
            metadata=metadata or {},
        )

        self._metrics_queue.put(metric)

        # Flush if batch is full
        if self._metrics_queue.qsize() >= self.batch_size:
            self._flush_metrics()

    def track_exception(self, exception_info: ExceptionInfo):
        """Track an exception (usually called by middleware)."""
        if not self.enabled:
            return

        self._exceptions_queue.put(exception_info)

        # Flush immediately for exceptions
        if self._exceptions_queue.qsize() >= 10:
            self._flush_exceptions()

    def capture_exception(
        self,
        exc: Optional[BaseException] = None,
        tags: Optional[Dict[str, str]] = None,
        extra: Optional[Dict[str, Any]] = None,
    ):
        """
        Manually capture an exception.

        Usage:
            try:
                risky_operation()
            except Exception as e:
                spotlight.capture_exception(e)
                raise
        """
        merged_tags = {**self.tags, **(tags or {})}

        exc_info = capture_exception(
            exc,
            environment=self.environment,
            release=self.release,
            tags=merged_tags,
            extra=extra,
        )

        if exc_info:
            self.track_exception(exc_info)

        return exc_info

    def add_breadcrumb(
        self,
        message: str,
        category: str = "default",
        level: str = "info",
        data: Optional[Dict] = None,
    ):
        """Add a breadcrumb for context."""
        Breadcrumb.add(message, category, level, data)

    def validator(
        self,
        name: Optional[str] = None,
        endpoint: Optional[str] = None,
        methods: Optional[List[str]] = None,
    ):
        """Decorator to register a validator."""
        def decorator(func):
            validator_name = name or func.__name__
            self.validators.add(
                name=validator_name,
                func=func,
                endpoint_pattern=endpoint,
                methods=methods,
            )
            return func
        return decorator

    def instrument(self, app):
        """Auto-instrument a FastAPI application."""
        from .middleware import SpotlightMiddleware
        app.add_middleware(SpotlightMiddleware, spotlight=self)

    def shutdown(self):
        """Shutdown client and flush remaining metrics."""
        self._stop_event.set()
        self._flush()
        if self._flush_thread:
            self._flush_thread.join(timeout=5.0)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.shutdown()