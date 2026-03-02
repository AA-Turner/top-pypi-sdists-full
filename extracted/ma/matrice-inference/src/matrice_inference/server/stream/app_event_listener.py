"""Kafka event listener for app deployment topic events."""
import logging
from typing import Any, Dict, Callable
from matrice_common.session import Session
from matrice_common.stream import EventListener as GenericEventListener


class AppEventListener:
    """Listener for app deployment add/delete events from Kafka.

    This class wraps the generic EventListener from matrice_common
    and provides app-specific event handling logic for input/output topics.

    Events handled:
    - add: New input/output topic created for a camera
    - delete: Input/output topic removed for a camera
    """

    def __init__(
        self,
        session: Session,
        app_deployment_id: str,
        on_topic_added: Callable[[Dict[str, Any]], None],
        on_topic_deleted: Callable[[Dict[str, Any]], None],
    ) -> None:
        """Initialize app event listener.

        Args:
            session: Session object for authentication
            app_deployment_id: ID of app deployment to filter events
            on_topic_added: Callback when a topic is added
            on_topic_deleted: Callback when a topic is deleted
        """
        self.app_deployment_id = app_deployment_id
        self.session = session
        self.on_topic_added = on_topic_added
        self.on_topic_deleted = on_topic_deleted
        self.logger = logging.getLogger(__name__)

        # Create generic event listener for App_Events_Topic
        self._listener = GenericEventListener(
            session=session,
            topics=['App_Events_Topic'],
            event_handler=self.handle_event,
            filter_field='appDeploymentId',
            filter_value=app_deployment_id,
            consumer_group_id=f"app_deployment_events_{app_deployment_id}"
        )

        self.logger.info(f"App EventListener initialized for deployment {app_deployment_id}")

    @property
    def is_listening(self) -> bool:
        """Check if listener is active."""
        return self._listener.is_listening

    def start(self) -> bool:
        """Start listening to app events.

        Returns:
            bool: True if started successfully
        """
        return self._listener.start()

    def stop(self):
        """Stop listening."""
        self._listener.stop()

    def handle_event(self, event: Dict[str, Any]):
        """Handle app deployment event.

        Args:
            event: App event dict with structure:
                {
                    "eventType": "add" | "delete",
                    "appDeploymentId": "...",
                    "topicType": "input" | "output",
                    "timestamp": "...",
                    "data": {
                        "id": "...",
                        "cameraId": "...",
                        "topicName": "...",
                        "topicType": "input" | "output",
                        "serverId": "...",
                        "serverType": "redis" | "kafka",
                        ...
                    }
                }
        """
        event_type = event.get('eventType')
        topic_type = event.get('topicType')
        topic_data = event.get('data', {})

        camera_id = topic_data.get('cameraId')
        topic_name = topic_data.get('topicName')
        server_type = topic_data.get('serverType')

        self.logger.info(
            f"Handling {event_type} event for {topic_type} topic: "
            f"camera={camera_id}, topic={topic_name}, server={server_type}"
        )

        try:
            if event_type == 'add':
                self._handle_add_event(event, topic_data)
            elif event_type == 'delete':
                self._handle_delete_event(event, topic_data)
            else:
                self.logger.warning(f"Unknown event type: {event_type}")

        except Exception as e:
            self.logger.error(f"Error handling {event_type} for camera {camera_id}: {e}")

    def _handle_add_event(self, event: Dict[str, Any], topic_data: Dict[str, Any]):
        """Handle topic add event.

        Args:
            event: Full event dict
            topic_data: Topic data from event
        """
        camera_id = topic_data.get('cameraId')
        topic_type = event.get('topicType')

        self.logger.info(f"Adding {topic_type} topic for camera {camera_id}")

        # Call the callback to handle topic addition
        if self.on_topic_added:
            self.on_topic_added(event)

    def _handle_delete_event(self, event: Dict[str, Any], topic_data: Dict[str, Any]):
        """Handle topic delete event.

        Args:
            event: Full event dict
            topic_data: Topic data from event
        """
        camera_id = topic_data.get('cameraId')
        topic_type = event.get('topicType')

        self.logger.info(f"Deleting {topic_type} topic for camera {camera_id}")

        # Call the callback to handle topic deletion
        if self.on_topic_deleted:
            self.on_topic_deleted(event)

    def get_statistics(self) -> dict:
        """Get statistics."""
        return self._listener.get_statistics()
