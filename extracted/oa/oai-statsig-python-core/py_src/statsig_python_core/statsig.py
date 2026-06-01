import inspect
import json
import os
from pathlib import Path
from weakref import ref
from statsig_python_core import (
    DynamicConfigEvaluationOptions,
    ExperimentEvaluationOptions,
    FeatureGateEvaluationOptions,
    LayerEvaluationOptions,
    StatsigBasePy,
    StatsigOptions,
    StatsigUser,
    notify_python_fork,
    notify_python_shutdown,
)
from typing import Any, Callable, Optional
from .error_boundary import ErrorBoundary
from .statsig_types import DynamicConfig, FeatureGate, Experiment, Layer
import atexit


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


def handle_fork():
    notify_python_fork()


if hasattr(os, "register_at_fork"):
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


class Statsig(StatsigBasePy):
    _statsig_shared_instance = None

    def __new__(cls, sdk_key: str, options: Optional[StatsigOptions] = None):
        instance = super().__new__(cls, sdk_key, options)
        _setup_internal_sdk_configs_cache(instance)
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

        cls._statsig_shared_instance = super().__new__(cls, sdk_key, options)
        _setup_internal_sdk_configs_cache(cls._statsig_shared_instance)
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

    def get_feature_gate(
        self,
        user: StatsigUser,
        name: str,
        options: Optional[FeatureGateEvaluationOptions] = None,
    ) -> FeatureGate:
        raw = super()._INTERNAL_get_feature_gate(user, name, options)
        return FeatureGate(name, raw)

    def get_dynamic_config(
        self,
        user: StatsigUser,
        name: str,
        options: Optional[DynamicConfigEvaluationOptions] = None,
    ) -> DynamicConfig:
        raw = super()._INTERNAL_get_dynamic_config(user, name, options)
        return DynamicConfig(name, raw)

    def get_experiment(
        self,
        user: StatsigUser,
        name: str,
        options: Optional[ExperimentEvaluationOptions] = None,
    ) -> Experiment:
        raw = super()._INTERNAL_get_experiment(
            user,
            name,
            options,
            self._get_experiment_exposure_metadata(name),
        )
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
        raw = super()._INTERNAL_get_layer(user, name, options)
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
                        frame.f_code.co_qualname,
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

    def _get_layer_exposure_metadata(
        self, layer_name: str
    ) -> Optional[dict[str, Any]]:
        if not self._sdk_config_enabled(
            f"{_LAYER_EXPOSURE_CALLSITE_SDK_CONFIG_PREFIX}{layer_name}"
        ):
            return None
        return self._get_exposure_callsite_metadata()


def create_statsig_error_instance(message: str) -> StatsigBasePy:
    print("Error: ", message)
    return StatsigBasePy.__new__(StatsigBasePy, "__STATSIG_ERROR_SDK_KEY__", None)
