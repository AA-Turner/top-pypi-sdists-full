import asyncio
import inspect
from google.cloud import pubsub_v1
from google.cloud.pubsub_v1.subscriber.futures import StreamingPullFuture
from google.cloud.pubsub_v1.subscriber.message import Message
from google.oauth2.service_account import Credentials
from pathlib import Path
from pydantic import BaseModel
from typing import Awaitable, Callable, Dict, List, Optional, Union
from maleo_foundation.managers.client.google.base import GoogleClientManager

SyncController = Callable[[str, Message], bool]
AsyncController = Callable[[str, Message], Awaitable[bool]]
Controller = Union[SyncController, AsyncController]
OptionalController = Optional[Controller]

class SubscriptionConfigurations(BaseModel):
    subscription_name: str
    max_messages: int = 10
    ack_deadline: int = 10
    controller: OptionalController = None

class SubscriptionManager(GoogleClientManager):
    def __init__(
        self,
        subscriptions: List[SubscriptionConfigurations],
        log_config,
        service_key: Optional[str] = None,
        credentials: Optional[Credentials] = None,
        credentials_path: Optional[Union[Path, str]] = None,
    ):
        key = "google-subscription-manager"
        name = "GoogleSubscriptionManager"
        super().__init__(key, name, log_config, service_key, credentials, credentials_path)
        self.subscriber = pubsub_v1.SubscriberClient(credentials=self._credentials)
        self.subscriptions = subscriptions
        self.active_listeners: Dict[str, StreamingPullFuture] = {}
        self.loop: Optional[asyncio.AbstractEventLoop] = None

    async def _handle_async_controller(
        self,
        controller: AsyncController,
        subscription_name: str,
        message: Message
    ) -> None:
        success = await controller(subscription_name, message)
        message.ack() if success else message.nack()

    def _handle_sync_controller(
        self,
        controller: SyncController,
        subscription_name: str,
        message: Message
    ) -> None:
        success = controller(subscription_name, message)
        message.ack() if success else message.nack()

    def _message_callback(
        self,
        controller: OptionalController,
        subscription_name: str,
        message: Message
    ):
        # If controller is not given, conduct default message processing
        if controller is None:
            self._default_message_processing(subscription_name, message)
            return

        # Check controller function type and handle accordingly
        is_async_controller = inspect.iscoroutinefunction(controller)
        if is_async_controller:
            if not self.loop:
                raise RuntimeError("Event loop not set in SubscriptionManager")
            asyncio.run_coroutine_threadsafe(
                self._handle_async_controller(
                    controller,
                    subscription_name,
                    message
                ),
                self.loop
            )
        else:
            self._handle_sync_controller(
                controller,
                subscription_name,
                message
            )

    def _default_message_processing(
        self,
        subscription_name: str,
        message: Message
    ) -> None:
        try:
            self._logger.info("Default message processing for subscription '%s': %s", subscription_name, message.data.decode("utf-8"))
            message.ack()
        except Exception as e:
            self._logger.error("Error handling message through default processor: %s", e, exc_info=True)
            message.nack()

    async def _start_subscription_listener(
        self,
        config: SubscriptionConfigurations
    ) -> None:
        subscription_path = self.subscriber.subscription_path(self.credentials.project_id, config.subscription_name)
        flow_control = pubsub_v1.types.FlowControl(max_messages=config.max_messages)
        future = self.subscriber.subscribe(
            subscription_path,
            callback=lambda message: self._message_callback(
                config.controller,
                config.subscription_name,
                message
            ),
            flow_control=flow_control,
            await_callbacks_on_shutdown=True
        )
        self.active_listeners[subscription_path] = future
        try:
            await asyncio.get_event_loop().run_in_executor(None, future.result)
        except Exception as e:
            if not isinstance(e, asyncio.CancelledError):
                self._logger.error("Listener error for subscription '%s': %s", config.subscription_name, e, exc_info=True)

    async def start_listeners(
        self,
        loop: asyncio.AbstractEventLoop
    ) -> None:
        self.loop = loop
        for config in self.subscriptions:
            asyncio.create_task(self._start_subscription_listener(config))
        await asyncio.sleep(0.1)

    async def stop_listeners(self):
        for future in self.active_listeners.values():
            future.cancel()
            try:
                future.result()
            except Exception:
                pass
        self.active_listeners.clear()