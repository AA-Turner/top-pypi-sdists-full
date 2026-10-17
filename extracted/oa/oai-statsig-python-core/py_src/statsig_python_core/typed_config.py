"""Per-call typed conversion and explicit publication observers."""

import json
import logging
from copy import deepcopy
from dataclasses import dataclass
from functools import lru_cache
from importlib import import_module, resources
from threading import Condition, Lock, Thread, current_thread
from types import ModuleType
from typing import TYPE_CHECKING, Any, Callable, Optional, TypeVar
from weakref import ref

from .evaluation_cache import _VALUE_CACHE_HIT_FIELD
from .statsig_types import TypedDynamicConfig

if TYPE_CHECKING:
    from google.protobuf.message import Message


T = TypeVar("T", bound="Message")
_LOGGER = logging.getLogger(__name__)


class TypedConfigUnavailableError(RuntimeError):
    """No usable config/resource is available, or the SDK is closed."""


class TypedConfigConversionError(RuntimeError):
    """The selected value or packaged document is invalid for the requested type."""


def _validate_message_type(message_type: type[T]) -> None:
    from google.protobuf.message import Message

    if not isinstance(message_type, type) or not issubclass(message_type, Message):
        raise TypeError("message_type must be a protobuf Message class")


@lru_cache(maxsize=64)
def _load_packaged_document(package: ModuleType) -> Any:
    # Packages are immutable build artifacts shared across SDK instances.
    content = resources.files(package).joinpath("fallback.json").read_bytes()
    try:
        return json.loads(content)
    except Exception as error:
        raise TypedConfigConversionError("Invalid packaged fallback JSON") from error


def _infer_packaged_fallback_package(name: str, message_type: type[T]) -> ModuleType:
    parts = message_type.__module__.split(".")
    if (
        len(parts) != 4
        or parts[:2] != ["oaiproto", "statsig_configs"]
        or parts[3] != "config_pb2"
    ):
        raise TypedConfigUnavailableError(
            f"Cannot infer packaged fallback for typed config {name!r}; "
            "pass packaged_fallback_package for a nonstandard protobuf package"
        )
    try:
        return import_module(parts[2])
    except Exception as error:
        raise TypedConfigUnavailableError(
            f"Cannot import packaged fallback for typed config {name!r}: {parts[2]}"
        ) from error


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
        packaged_fallback_package: Optional[ModuleType] = None,
        *,
        allow_packaged_fallback: bool = True,
    ) -> TypedDynamicConfig[T]:
        _validate_message_type(message_type)
        if packaged_fallback_package is not None and not isinstance(
            packaged_fallback_package, ModuleType
        ):
            raise TypeError("packaged_fallback_package must be a package module")
        sdk = self._get_sdk()
        if not allow_packaged_fallback:
            raw = sdk._INTERNAL_get_typed_config(user, name, options)
        else:
            raw = sdk._INTERNAL_get_typed_config(
                user, name, options, allow_packaged_fallback=True
            )
        if (
            allow_packaged_fallback
            and raw.get("__typed_packaged_fallback_eligible") is True
        ):
            if packaged_fallback_package is None:
                packaged_fallback_package = _infer_packaged_fallback_package(
                    name, message_type
                )
            result = self._get_packaged(
                name,
                packaged_fallback_package,
                raw.get("__typed_packaged_fallback_tier"),
                message_type,
            )
        else:
            result = self._convert(name, raw, message_type)
        return result

    def _get_packaged(
        self, name: str, package: ModuleType, tier: Optional[str], message_type: type[T]
    ) -> TypedDynamicConfig[T]:
        if tier is not None and not isinstance(tier, str):
            raise TypedConfigUnavailableError(
                "Native packaged fallback tier is invalid"
            )
        resource_name = f"{package.__name__}/fallback.json"
        try:
            document = _load_packaged_document(package)
        except TypedConfigConversionError as error:
            raise TypedConfigConversionError(
                f"Invalid packaged fallback for typed config {name!r}: {resource_name}"
            ) from error.__cause__
        except Exception as error:
            raise TypedConfigUnavailableError(
                f"Cannot read packaged fallback for typed config {name!r}: {resource_name}"
            ) from error
        try:
            environments = document.get("environments", {})
            selected = (
                environments[tier] if tier in environments else document["default"]
            )
        except Exception as error:
            raise TypedConfigConversionError(
                f"Cannot select packaged fallback for typed config {name!r}: {resource_name}"
            ) from error
        # Protobuf's Any parser temporarily mutates its input, so never give it
        # the shared cached document even though each output message is fresh.
        value = self._parse_value(name, deepcopy(selected), message_type, resource_name)
        return TypedDynamicConfig(
            name,
            {"details": {"reason": "PackagedFallback"}, "__typed_revision": None},
            value,
            value_source="packaged",
        )

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
        value = self._parse_value(name, raw["value"], message_type)
        return TypedDynamicConfig(name, raw, value)

    @staticmethod
    def _parse_value(
        name: str,
        selected: dict,
        message_type: type[T],
        resource_name: Optional[str] = None,
    ) -> T:
        from google.protobuf.json_format import ParseDict

        try:
            return ParseDict(selected, message_type(), ignore_unknown_fields=True)
        except Exception as error:
            raise TypedConfigConversionError(
                f"Failed to convert typed config {name!r}"
                + (f" from {resource_name}" if resource_name is not None else "")
            ) from error

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

    def _get_sdk(self) -> Any:
        sdk = self._sdk()
        if sdk is None:
            raise TypedConfigUnavailableError("Statsig instance is no longer available")
        return sdk

    def _ensure_open(self) -> Any:
        if self._closed:
            raise TypedConfigUnavailableError("Statsig has been shut down")
        return self._get_sdk()

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
