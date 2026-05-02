"""
Events Manager - Handles queuing and publishing events to EventBridge

This is a generic implementation that can be configured for different environments.
"""
from ...models.base_models.singleton import SingletonMeta
from ...models.analytics.events.base import Event, EventType
from typing import List, Optional, Callable
import logging
import boto3
import queue
import threading
import time
from datetime import datetime
from zoneinfo import ZoneInfo
import os
import json

logger = logging.getLogger("EventsManager")


class EventsManager(metaclass=SingletonMeta):
    """
    Manages event queuing and publishing to AWS EventBridge.

    Can be configured via environment variables or init parameters.
    """

    def __init__(self,
                 event_bus_name: Optional[str] = None,
                 source: Optional[str] = None,
                 publish_events: Optional[bool] = None,
                 failed_events_callback: Optional[Callable] = None):
        """
        Initialize EventsManager.

        Args:
            event_bus_name: AWS EventBridge event bus name (or uses env var)
            source: Source identifier for events (or uses env var)
            publish_events: Whether to publish events (or uses env var)
            failed_events_callback: Optional callback for handling failed events
        """
        self.events_queue: queue.Queue[Event] = queue.Queue()
        self.eventbridge_client = boto3.client('events', region_name='us-east-1')

        # Configuration - prefer parameters, fall back to env vars
        self.event_bus_name = event_bus_name or os.getenv('CHATTY_EVENT_BUS_NAME', 'chatty-events')
        self.source = source or os.getenv('CHATTY_EVENT_SOURCE')
        if not self.source:
            raise ValueError("Source must be provided either as a parameter or through the CHATTY_EVENT_SOURCE environment variable.")
        self.publish_events = publish_events if publish_events is not None else os.getenv('PUBLISH_EVENTS_TO_EVENTBRIDGE', 'true').lower() == 'true'

        self.max_retries = 3
        self.thread_lock = threading.Lock()
        self.thread_running = False
        self.max_thread_runtime = 300
        self.failed_events_callback = failed_events_callback

        logger.debug(f"EventsManager initialized: bus={self.event_bus_name}, source={self.source}, publish={self.publish_events}")

    def queue_events(self, events: List[Event]):
        """Queue events and spawn a thread to publish them if one isn't already running"""
        if not self.publish_events:
            logger.debug("Event publishing disabled, skipping")
            return

        for event in events:
            logger.debug(f"Queueing event: {event.type.value} {event.company_id}")
            logger.debug(f"Event: {event.model_dump_json()}")
            self.events_queue.put(event)

        logger.debug(f"Queued {len(events)} events")
        if events:
            logger.debug(f"1° event: {events[0].model_dump_json()}")

        # Only start a new thread if one isn't already running
        with self.thread_lock:
            if not self.thread_running:
                logger.debug("Starting publisher thread")
                self.thread_running = True
                thread = threading.Thread(
                    target=self._process_queue,
                    daemon=True,
                    name="EventBridge-Publisher"
                )
                thread.start()
                logger.debug("Started publisher thread")
            else:
                logger.debug("Publisher thread already running, using existing thread")

    def _process_queue(self):
        """Process all events in the queue and then terminate"""
        try:
            start_time = time.time()
            while not self.events_queue.empty():
                logger.debug("Processing queue")
                events_batch = []
                if time.time() - start_time > self.max_thread_runtime:
                    logger.warning(f"Thread ran for more than {self.max_thread_runtime}s - terminating")
                    break

                # Collect up to 10 events (EventBridge limit)
                for _ in range(10):
                    try:
                        event = self.events_queue.get(timeout=0.5)
                        events_batch.append(event)
                        self.events_queue.task_done()
                    except queue.Empty:
                        logger.debug("Queue is empty")
                        break

                # Publish this batch
                if events_batch:
                    self._publish_batch(events_batch)

        except Exception as e:
            logger.exception(f"Error in publisher thread: {str(e)}")

        finally:
            # Mark thread as completed
            with self.thread_lock:
                self.thread_running = False

    def _publish_batch(self, events: List[Event]):
        """Send a batch of events to EventBridge with retries"""
        if not events:
            return

        entries = []
        for event in events:
            entry = {
                'Source': self.source,
                'DetailType': event.type.value,
                'Detail': json.dumps(event.model_dump_json()),
                'EventBusName': self.event_bus_name
            }
            logger.debug(f"Appending event: {event.type.value}")
            entries.append(entry)

        for retry in range(self.max_retries):
            try:
                logger.debug(f"Sending {len(entries)} events to EventBridge")
                logger.debug(f"Entries: {entries}")
                response = self.eventbridge_client.put_events(Entries=entries)
                logger.debug(f"Response: {response}")

                if response.get('FailedEntryCount', 0) == 0:
                    logger.info(f"Successfully published {len(events)} events")
                    return

                # Handle partial failures
                failed_entries: List[dict] = []
                failed_events: List[Event] = []

                for i, result in enumerate(response.get('Entries', [])):
                    if 'ErrorCode' in result:
                        failed_entries.append(entries[i])
                        failed_events.append(events[i])
                        logger.error(f"Failed to publish event: {events[i].type.value}")

                if retry < self.max_retries - 1 and failed_entries:
                    logger.info(f"Retrying {len(failed_entries)} events")
                    entries = failed_entries
                    events = failed_events
                else:
                    # Store failed events via callback if provided
                    if self.failed_events_callback and failed_events:
                        failed_events_with_errors = []
                        for i, event in enumerate(failed_events):
                            result = response.get('Entries', [])[i]
                            failed_event_data = {
                                "event": event.model_dump_json(),
                                "error_code": result.get('ErrorCode'),
                                "error_message": result.get('ErrorMessage'),
                                "retry_count": self.max_retries,
                                "timestamp": datetime.now(ZoneInfo("UTC"))
                            }
                            failed_events_with_errors.append(failed_event_data)

                        try:
                            self.failed_events_callback(failed_events_with_errors)
                        except Exception as e:
                            logger.error(f"Error calling failed_events_callback: {e}")

                    logger.error(f"Gave up on {len(failed_entries)} events after {self.max_retries} attempts")
                    return

            except Exception as e:
                if retry < self.max_retries - 1:
                    logger.warning(f"Error publishing events (attempt {retry+1}/{self.max_retries}): {str(e)}")
                    time.sleep(0.5 * (2 ** retry))  # Exponential backoff
                else:
                    logger.exception(f"Failed to publish events after {self.max_retries} attempts")
                    return

    def flush(self):
        """Wait for all queued events to be processed"""
        # If no thread is running but we have events, start one
        with self.thread_lock:
            if not self.thread_running and not self.events_queue.empty():
                self.thread_running = True
                thread = threading.Thread(
                    target=self._process_queue,
                    daemon=True,
                    name="EventBridge-Publisher"
                )
                thread.start()

        # Wait for queue to be empty
        try:
            self.events_queue.join()
            return True
        except Exception:
            logger.warning("Error waiting for events queue to complete")
            return False


# Singleton instance (best-effort to avoid import-time crashes when env is incomplete)
class _NoOpEventsManager:
    """Fallback manager used when real EventsManager cannot be initialized."""

    def queue_events(self, events):
        logger.warning("NoOpEventsManager: queue_events skipped because EventsManager is not initialized")

    def flush(self):
        logger.warning("NoOpEventsManager: flush skipped because EventsManager is not initialized")
        return False


try:
    events_manager = EventsManager()
except Exception as e:
    logger.warning("EventsManager singleton not initialized at import time: %s", e)
    events_manager = _NoOpEventsManager()
