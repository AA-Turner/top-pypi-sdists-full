import atexit
import inspect
import json
import os
from pathlib import Path
from typing import TYPE_CHECKING, Any, Callable, Optional, TypeVar
from weakref import ref

from statsig_python_core import (
    BulkEvaluationOptions,
    DynamicConfigEvaluationOptions,
    ExperimentEvaluationOptions,
    FeatureGateEvaluationOptions,
    LayerEvaluationOptions,
    StatsigBasePy,
    StatsigOptions,
    StatsigRandomUserID,
    StatsigUser,
    StatsigUserContext,
    notify_python_fork,
    notify_python_shutdown,
)

from .error_boundary import ErrorBoundary
from .evaluation_cache import (
    EvaluationCache,
    _EvaluationCacheKeys,
    _get_evaluation_cache,
)
from .statsig_types import (
    DynamicConfig,
    Experiment,
    FeatureGate,
    Layer,
    TypedDynamicConfig,
)
from .typed_config import _TypedConfigs

if TYPE_CHECKING:
    from google.protobuf.message import Message

    from .statsig_python_core import AttributesDict, CustomIdsDict


def handle_atexit():
    notify_python_shutdown()


atexit.register(handle_atexit)

_INTERNAL_SDK_CONFIGS_UPDATED_EVENT = "__internal_sdk_configs_updated__"
_EXPOSURE_SOURCE_FILE_MAX_LENGTH = 128
_EXPOSURE_SOURCE_FUNCTION_MAX_LENGTH = 256
_DEFAULT_EXPOSURE_CALLSITE_IGNORED_MODULE_PREFIXES: tuple[str, ...] = (
    "statsig_python_core",
)
_EXPERIMENT_EXPOSURE_CALLSITE_SDK_CONFIG_PREFIX = "expo_callsite_logging_experiment::"
_LAYER_EXPOSURE_CALLSITE_SDK_CONFIG_PREFIX = "expo_callsite_logging_layer::"
_TypedConfigValue = TypeVar("_TypedConfigValue", bound="Message")


def handle_fork():
    notify_python_fork()


if hasattr(os, "register_at_fork"):
    # Reset before forking so no Rust runtime workers are inherited by the
    # child. notify_python_fork releases the GIL while teardown completes.
    os.register_at_fork(
        before=handle_fork,
    )


def _setup_internal_sdk_configs_cache(instance: StatsigBasePy) -> None:
    setattr(instance, "_internal_sdk_configs", {})
    instance_ref = ref(instance)

    def update_sdk_configs(raw: str) -> bool:
        statsig = instance_ref()
        if statsig is None:
            return False

        try:
            event = json.loads(raw)
            sdk_configs = event.get("data", {}).get("sdk_configs")
            if isinstance(sdk_configs, dict):
                setattr(statsig, "_internal_sdk_configs", dict(sdk_configs))
        except Exception as error:
            print(f"[Statsig] Error parsing internal SDK configs update: {error}")

        return True

    instance._INTERNAL_subscribe_internal(
        _INTERNAL_SDK_CONFIGS_UPDATED_EVENT,
        update_sdk_configs,
    )


def _setup_evaluation_cache(
    instance: StatsigBasePy, cache: Optional[EvaluationCache]
) -> None:
    setattr(instance, "_evaluation_cache", cache)


def _setup_typed_configs(instance: StatsigBasePy) -> None:
    setattr(instance, "_typed_configs", _TypedConfigs(instance))


def _get_cache_for_call(
    instance: StatsigBasePy,
) -> tuple[Optional[EvaluationCache], Optional[_EvaluationCacheKeys]]:
    cache = getattr(instance, "_evaluation_cache", None)
    if cache is None:
        return None, None
    return cache, cache._keys_for_call()


class Statsig(StatsigBasePy):
    _statsig_shared_instance = None
    _typed_configs: _TypedConfigs

    def __new__(cls, sdk_key: str, options: Optional[StatsigOptions] = None):
        cache = _get_evaluation_cache(options)
        instance = super().__new__(cls, sdk_key, options)
        _setup_internal_sdk_configs_cache(instance)
        _setup_evaluation_cache(instance, cache)
        _setup_typed_configs(instance)
        ErrorBoundary.wrap(instance)
        return instance

    # ----------------------------
    #       Shared Instance
    # ----------------------------

    @classmethod
    def shared(cls) -> StatsigBasePy:
        if not Statsig.has_shared_instance() or cls._statsig_shared_instance is None:
            return create_statsig_error_instance(
                "Statsig.shared() called, but no instance has been set with Statsig.new_shared(...)"
            )

        return cls._statsig_shared_instance

    @classmethod
    def new_shared(
        cls, sdk_key: str, options: Optional[StatsigOptions] = None
    ) -> StatsigBasePy:
        if Statsig.has_shared_instance():
            return create_statsig_error_instance(
                "Statsig shared instance already exists. Call Statsig.remove_shared() before creating a new instance."
            )

        cache = _get_evaluation_cache(options)
        cls._statsig_shared_instance = super().__new__(cls, sdk_key, options)
        _setup_internal_sdk_configs_cache(cls._statsig_shared_instance)
        _setup_evaluation_cache(cls._statsig_shared_instance, cache)
        _setup_typed_configs(cls._statsig_shared_instance)
        return cls._statsig_shared_instance

    @classmethod
    def remove_shared(cls) -> None:
        cls._statsig_shared_instance = None

    @classmethod
    def has_shared_instance(cls) -> bool:
        return (
            hasattr(cls, "_statsig_shared_instance")
            and cls._statsig_shared_instance is not None
        )

    # ------------------------------------------------------------ [ Core APIs ]

    def get_typed_config(
        self,
        name: str,
        user: StatsigUser,
        *,
        message_type: type[_TypedConfigValue],
        options: Optional[DynamicConfigEvaluationOptions] = None,
    ) -> TypedDynamicConfig[_TypedConfigValue]:
        """Evaluate the supplied current context and freshly convert its value.

        Supply a generated protobuf ``message_type``. The result
        pairs its value with metadata from that same evaluation. Ordinary
        exposure semantics apply; conversion failures raise and never substitute
        an earlier value. Reads retain no context binding and notify no callbacks.
        """
        if options is not None and not isinstance(
            options, DynamicConfigEvaluationOptions
        ):
            raise TypeError("options must be DynamicConfigEvaluationOptions")
        return self._typed_configs.get(name, user, message_type, options)

    def register_typed_config_callback(
        self,
        name: str,
        user: StatsigUser,
        callback: Callable[[TypedDynamicConfig[_TypedConfigValue]], None],
        *,
        message_type: type[_TypedConfigValue],
    ) -> None:
        """Observe publications using an explicit captured context until shutdown.

        Initialization is required, but no preceding getter is needed. No initial
        replay, product exposures or getter-driven delivery. Changed selected
        revisions notify with whole typed results; unrelated LCUT does not.
        Updates may coalesce. Callbacks run outside shared-state locks on one
        worker, should be short and nonblocking, and may read a newer snapshot
        through the ordinary getter. Shutdown waits for admitted delivery unless
        called by that worker, and prevents later delivery.
        Conversion and callback errors are reported and isolated.
        """
        self._typed_configs.register(name, user, callback, message_type)

    def shutdown(self) -> Any:
        self._typed_configs.close()
        return super().shutdown()

    def subscribe(
        self,
        event_name: str,
        callback: Callable[[dict[str, Any]], None],
    ) -> str:
        def emit(raw: str) -> None:
            try:
                callback(json.loads(raw))
            except Exception as error:
                print(f"[Statsig] Error parsing SDK Event: {error}")

        return super()._INTERNAL_subscribe(event_name, emit)

    def get_feature_gate_anonymous(
        self,
        name: str,
        id_options: StatsigRandomUserID,
        *,
        context: Optional[StatsigUserContext] = None,
        custom: Optional["AttributesDict"] = None,
        custom_ids: Optional["CustomIdsDict"] = None,
        ip: Optional[str] = None,
        country: Optional[str] = None,
        locale: Optional[str] = None,
        user_agent: Optional[str] = None,
        options: Optional[FeatureGateEvaluationOptions] = None,
    ) -> FeatureGate:
        """Randomize userID; custom IDs and request fields override context."""
        # The public API names these arguments; positional forwarding avoids
        # repeating keyword-name searches at the private native boundary.
        parts = super()._INTERNAL_get_feature_gate_anonymous_parts(
            name,
            id_options,
            context,
            custom,
            custom_ids,
            ip,
            country,
            locale,
            user_agent,
            options,
        )
        return FeatureGate._from_parts(name, parts)

    def get_feature_gate_fields_anonymous(
        self,
        name: str,
        id_options: StatsigRandomUserID,
        *,
        context: Optional[StatsigUserContext] = None,
        custom: Optional["AttributesDict"] = None,
        custom_ids: Optional["CustomIdsDict"] = None,
        ip: Optional[str] = None,
        country: Optional[str] = None,
        locale: Optional[str] = None,
        user_agent: Optional[str] = None,
        options: Optional[FeatureGateEvaluationOptions] = None,
    ) -> Optional[tuple[bool, str]]:
        """Return (value, reason), with a fresh anonymous identity per call.

        Options, callbacks and exposures match get_feature_gate_anonymous.
        The SDK error boundary returns None if the call fails.
        """
        parts = super()._INTERNAL_get_feature_gate_anonymous_parts(
            name,
            id_options,
            context,
            custom,
            custom_ids,
            ip,
            country,
            locale,
            user_agent,
            options,
        )
        return parts[0], parts[3]

    def get_layer_anonymous(
        self,
        name: str,
        id_options: StatsigRandomUserID,
        *,
        context: Optional[StatsigUserContext] = None,
        custom: Optional["AttributesDict"] = None,
        custom_ids: Optional["CustomIdsDict"] = None,
        ip: Optional[str] = None,
        country: Optional[str] = None,
        locale: Optional[str] = None,
        user_agent: Optional[str] = None,
        options: Optional[LayerEvaluationOptions] = None,
    ) -> Layer:
        """Evaluate once; delayed parameter exposures retain that call's identity."""
        cache, cache_keys = _get_cache_for_call(self)
        raw = super()._INTERNAL_get_layer_anonymous(
            name,
            id_options,
            context,
            custom,
            custom_ids,
            ip,
            country,
            locale,
            user_agent,
            options,
            cache_keys,
        )
        if cache is not None:
            cache._consume_result(raw, cache_keys)
        exposure = raw.get("__exposure") if isinstance(raw, dict) else None

        def exposure_func(param: str):
            if exposure is None:
                return
            return self._INTERNAL_log_layer_param_exposure(
                exposure, param, self._get_layer_exposure_metadata(name)
            )

        return Layer(exposure_func, name, raw)

    def get_feature_gate_with_context(
        self,
        context: Optional[StatsigUserContext],
        name: str,
        user_id: Optional[str] = None,
        custom: Optional["AttributesDict"] = None,
        options: Optional[FeatureGateEvaluationOptions] = None,
    ) -> FeatureGate:
        parts = super()._INTERNAL_get_feature_gate_with_context_parts(
            context, name, user_id, custom, options
        )
        return FeatureGate._from_parts(name, parts)

    def get_feature_gate_fields_with_context(
        self,
        context: Optional[StatsigUserContext],
        name: str,
        user_id: Optional[str] = None,
        custom: Optional["AttributesDict"] = None,
        options: Optional[FeatureGateEvaluationOptions] = None,
    ) -> Optional[tuple[bool, str]]:
        """Return (value, reason) without constructing a FeatureGate.

        Options, callbacks and exposures match get_feature_gate_with_context.
        The SDK error boundary returns None if the call fails.
        """
        parts = super()._INTERNAL_get_feature_gate_with_context_parts(
            context, name, user_id, custom, options
        )
        return parts[0], parts[3]

    def get_dynamic_config_with_context(
        self,
        context: Optional[StatsigUserContext],
        name: str,
        user_id: Optional[str] = None,
        custom: Optional["AttributesDict"] = None,
        options: Optional[DynamicConfigEvaluationOptions] = None,
    ) -> DynamicConfig:
        cache, cache_keys = _get_cache_for_call(self)
        raw = super()._INTERNAL_get_dynamic_config_with_context(
            context, name, user_id, custom, options, cache_keys
        )
        if cache is not None:
            cache._consume_result(raw, cache_keys)
        return DynamicConfig(name, raw)

    def get_layer_with_context(
        self,
        context: Optional[StatsigUserContext],
        name: str,
        user_id: Optional[str] = None,
        custom: Optional["AttributesDict"] = None,
        options: Optional[LayerEvaluationOptions] = None,
    ) -> Layer:
        cache, cache_keys = _get_cache_for_call(self)
        raw = super()._INTERNAL_get_layer_with_context(
            context, name, user_id, custom, options, cache_keys
        )
        if cache is not None:
            cache._consume_result(raw, cache_keys)
        exposure = raw.get("__exposure") if isinstance(raw, dict) else None

        def exposure_func(param: str):
            if exposure is None:
                return
            return self._INTERNAL_log_layer_param_exposure(
                exposure, param, self._get_layer_exposure_metadata(name)
            )

        return Layer(exposure_func, name, raw)

    def get_feature_gate(
        self,
        user: StatsigUser,
        name: str,
        options: Optional[FeatureGateEvaluationOptions] = None,
    ) -> FeatureGate:
        parts = super()._INTERNAL_get_feature_gate_parts(user, name, options)
        return FeatureGate._from_parts(name, parts)

    def get_feature_gate_fields(
        self,
        user: StatsigUser,
        name: str,
        options: Optional[FeatureGateEvaluationOptions] = None,
    ) -> Optional[tuple[bool, str]]:
        """Return (value, reason) without constructing a FeatureGate.

        The reason is identical to get_feature_gate(...).details.reason,
        including uninitialized, unrecognized and local override results.
        Options, callbacks and exposures are unchanged. The SDK error boundary
        returns None if the call fails.
        """
        parts = super()._INTERNAL_get_feature_gate_parts(user, name, options)
        return parts[0], parts[3]

    def get_dynamic_config(
        self,
        user: StatsigUser,
        name: str,
        options: Optional[DynamicConfigEvaluationOptions] = None,
    ) -> DynamicConfig:
        cache, cache_keys = _get_cache_for_call(self)
        raw = super()._INTERNAL_get_dynamic_config(
            user,
            name,
            options,
            cache_keys,
        )
        if cache is not None:
            cache._consume_result(raw, cache_keys)
        return DynamicConfig(name, raw)

    def get_experiment(
        self,
        user: StatsigUser,
        name: str,
        options: Optional[ExperimentEvaluationOptions] = None,
    ) -> Experiment:
        cache, cache_keys = _get_cache_for_call(self)
        raw = super()._INTERNAL_get_experiment(
            user,
            name,
            options,
            self._get_experiment_exposure_metadata(name),
            cache_keys,
        )
        if cache is not None:
            cache._consume_result(raw, cache_keys)
        return Experiment(name, raw)

    def manually_log_experiment_exposure(
        self,
        user: StatsigUser,
        name: str,
    ) -> None:
        return super()._INTERNAL_manually_log_experiment_exposure(
            user,
            name,
            self._get_experiment_exposure_metadata(name),
        )

    def manually_log_layer_parameter_exposure(
        self,
        user: StatsigUser,
        name: str,
        param_name: str,
    ) -> None:
        return super()._INTERNAL_manually_log_layer_parameter_exposure(
            user,
            name,
            param_name,
            self._get_layer_exposure_metadata(name),
        )

    def get_layer(
        self,
        user: StatsigUser,
        name: str,
        options: Optional[LayerEvaluationOptions] = None,
    ) -> Layer:
        cache, cache_keys = _get_cache_for_call(self)
        raw = super()._INTERNAL_get_layer(user, name, options, cache_keys)
        if cache is not None:
            cache._consume_result(raw, cache_keys)
        exposure = raw.get("__exposure") if isinstance(raw, dict) else None

        def exposure_func(param: str):
            if exposure is None:
                return
            return self._INTERNAL_log_layer_param_exposure(
                exposure,
                param,
                self._get_layer_exposure_metadata(name),
            )

        return Layer(
            exposure_func,
            name,
            raw,
        )

    def bulk_evaluate(
        self,
        user: StatsigUser,
        options: Optional[BulkEvaluationOptions] = None,
    ) -> dict:
        cache, cache_keys = _get_cache_for_call(self)
        raw = super()._INTERNAL_bulk_evaluate(user, options, cache_keys)
        if cache is not None:
            for category in (
                "dynamic_configs",
                "experiments",
                "layer_configs",
            ):
                evaluations = raw.get(category, {})
                if not isinstance(evaluations, dict):
                    continue
                for evaluation in evaluations.values():
                    if isinstance(evaluation, dict):
                        cache._consume_result(evaluation, cache_keys)
        return raw

    def _is_exposure_callsite_module_ignored(self, module_name: str) -> bool:
        return module_name.startswith(
            _DEFAULT_EXPOSURE_CALLSITE_IGNORED_MODULE_PREFIXES
        )

    def _find_exposure_callsite(self) -> tuple[str, str, int | None] | None:
        frame = inspect.currentframe()
        try:
            frame = frame.f_back if frame is not None else None
            while frame is not None:
                module_name = frame.f_globals.get("__name__", "")
                if not self._is_exposure_callsite_module_ignored(module_name):
                    return (
                        Path(frame.f_code.co_filename).name,
                        getattr(frame.f_code, "co_qualname", frame.f_code.co_name),
                        frame.f_lineno,
                    )
                frame = frame.f_back
        finally:
            del frame
        return None

    def _get_exposure_callsite_metadata(self) -> dict[str, Any]:
        callsite = self._find_exposure_callsite()
        if callsite is None:
            return {
                "exposure_source_file": "unknown",
                "exposure_source_function": "unknown",
                "exposure_source_line": None,
            }

        file_name, function_name, line_number = callsite
        return {
            "exposure_source_file": file_name[:_EXPOSURE_SOURCE_FILE_MAX_LENGTH],
            "exposure_source_function": function_name[
                :_EXPOSURE_SOURCE_FUNCTION_MAX_LENGTH
            ],
            "exposure_source_line": line_number,
        }

    def _sdk_config_enabled(self, key: str) -> bool:
        sdk_configs = getattr(self, "_internal_sdk_configs", {})
        if not isinstance(sdk_configs, dict):
            return False
        return sdk_configs.get(key) == 1

    def _get_experiment_exposure_metadata(
        self, experiment_name: str
    ) -> Optional[dict[str, Any]]:
        if not self._sdk_config_enabled(
            f"{_EXPERIMENT_EXPOSURE_CALLSITE_SDK_CONFIG_PREFIX}{experiment_name}"
        ):
            return None
        return self._get_exposure_callsite_metadata()

    def _get_layer_exposure_metadata(self, layer_name: str) -> Optional[dict[str, Any]]:
        if not self._sdk_config_enabled(
            f"{_LAYER_EXPOSURE_CALLSITE_SDK_CONFIG_PREFIX}{layer_name}"
        ):
            return None
        return self._get_exposure_callsite_metadata()


def create_statsig_error_instance(message: str) -> StatsigBasePy:
    print("Error: ", message)
    return StatsigBasePy.__new__(StatsigBasePy, "__STATSIG_ERROR_SDK_KEY__", None)
