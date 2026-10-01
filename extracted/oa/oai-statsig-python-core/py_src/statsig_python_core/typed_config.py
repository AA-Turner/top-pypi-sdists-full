"""Per-call typed conversion and explicit publication observers."""

import logging
from dataclasses import dataclass
from threading import Condition, Lock, Thread, current_thread
from typing import TYPE_CHECKING, Any, Callable, Optional, TypeVar
from weakref import ref

from .evaluation_cache import _VALUE_CACHE_HIT_FIELD
from .statsig_types import TypedDynamicConfig

if TYPE_CHECKING:
    from google.protobuf.message import Message


T = TypeVar("T", bound="Message")
_LOGGER = logging.getLogger(__name__)


class TypedConfigUnavailableError(RuntimeError):
    """Native evaluation has no usable config, or the SDK is closed."""


class TypedConfigConversionError(RuntimeError):
    """The selected native value could not be converted to the requested type."""


def _validate_message_type(message_type: type[T]) -> None:
    from google.protobuf.message import Message

    if not isinstance(message_type, type) or not issubclass(message_type, Message):
        raise TypeError("message_type must be a protobuf Message class")


@dataclass
class _Observer:
    name: str
    native: Any
    message_type: type["Message"]
    callback: Callable
    revision: Any = None
    error: Optional[str] = None


class _TypedConfigs:
    def __init__(self, sdk: Any) -> None:
        self._sdk = ref(sdk)
        self.lock = Condition(Lock())
        self.observers: list[_Observer] = []
        self._baselines = 0
        self._updates: Any = None
        self._worker: Optional[Thread] = None
        self._closed = False

    def get(
        self,
        name: str,
        user: Any,
        message_type: type[T],
        options: Any,
    ) -> TypedDynamicConfig[T]:
        _validate_message_type(message_type)
        with self.lock:
            sdk = self._ensure_open()
        raw = sdk._INTERNAL_get_typed_config(user, name, options)
        result = self._convert(name, raw, message_type)
        with self.lock:
            self._ensure_open()
        return result

    def register(
        self,
        name: str,
        user: Any,
        callback: Callable[[TypedDynamicConfig[T]], None],
        message_type: type[T],
    ) -> None:
        if not callable(callback):
            raise TypeError("callback must be callable")
        _validate_message_type(message_type)
        with self.lock:
            sdk = self._ensure_open()
            if not sdk.is_initialized():
                raise TypedConfigUnavailableError(
                    "Initialize Statsig before registering callbacks"
                )
            if self._updates is None:
                self._updates = sdk._INTERNAL_typed_config_updates()
            self._baselines += 1
        try:
            observer = _Observer(
                name,
                sdk._INTERNAL_typed_config_context(user, name),
                message_type,
                callback,
            )
            self._observe(observer, baseline=True)
            with self.lock:
                self._ensure_open()
                self.observers.append(observer)
                if self._worker is None or not self._worker.is_alive():
                    self._worker = Thread(
                        target=self._run, name="StatsigTypedConfigs", daemon=True
                    )
                    self._worker.start()
        finally:
            with self.lock:
                self._baselines -= 1
                self.lock.notify_all()

    def _convert(
        self, name: str, raw: dict, message_type: type[T]
    ) -> TypedDynamicConfig[T]:
        if (
            not raw.get("__typed_usable", False)
            or raw.get(_VALUE_CACHE_HIT_FIELD)
            or not isinstance(raw.get("value"), dict)
        ):
            raise TypedConfigUnavailableError(
                f"Typed config {name!r} has no usable value"
            )
        from google.protobuf.json_format import ParseDict

        try:
            value = ParseDict(raw["value"], message_type())
        except Exception as error:
            raise TypedConfigConversionError(
                f"Failed to convert typed config {name!r}"
            ) from error
        return TypedDynamicConfig(name, raw, value)

    def _observe(self, observer: _Observer, *, baseline: bool = False) -> None:
        with self.lock:
            if self._closed:
                return
        try:
            result = self._convert(
                observer.name,
                observer.native.get_evaluation(),
                observer.message_type,
            )
        except Exception as error:
            error_name = type(error).__name__
            with self.lock:
                if self._closed:
                    return
                changed_error = observer.error != error_name
                observer.error = error_name
            if changed_error:
                _LOGGER.warning("Typed config observation failed (%s)", error_name)
            return
        with self.lock:
            if self._closed:
                return
            observer.error = None
            previous = observer.revision
            revision = result._revision
            if baseline:
                observer.revision = revision
                return
            if previous is not None and previous == revision:
                return
        try:
            observer.callback(result)
        except Exception as error:
            _LOGGER.warning("Typed config callback failed (%s)", type(error).__name__)
        else:
            with self.lock:
                if not self._closed:
                    observer.revision = revision

    def _run(self) -> None:
        updates = self._updates
        while True:
            changed = updates.wait()
            if changed is None:
                return
            with self.lock:
                self.lock.wait_for(lambda: not self._baselines or self._closed)
                if self._closed:
                    return
                owner_missing = self._sdk() is None
                observers = tuple(self.observers) if changed else ()
            if owner_missing:
                self.close()
                return
            for observer in observers:
                self._observe(observer)

    def _ensure_open(self) -> Any:
        sdk = self._sdk()
        if self._closed or sdk is None:
            raise TypedConfigUnavailableError("Statsig has been shut down")
        return sdk

    def close(self) -> None:
        with self.lock:
            self._closed = True
            updates = self._updates
            worker = self._worker
            self.observers.clear()
            self.lock.notify_all()
        if updates is not None:
            updates.close()
        if worker is not None and worker is not current_thread():
            worker.join()
