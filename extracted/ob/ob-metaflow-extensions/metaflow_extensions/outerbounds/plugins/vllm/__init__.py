from metaflow.decorators import StepDecorator
from metaflow import current
from metaflow.exception import MetaflowException
import functools
from enum import Enum
import threading
from metaflow.unbounded_foreach import UBF_CONTROL, UBF_TASK
from metaflow.metaflow_config import from_conf

from .vllm_manager import VLLMOpenAIManager, VLLMPyManager
from .status_card import VLLMStatusCard, CardDecoratorInjector

__mf_promote_submodules__ = ["plugins.vllm"]


### The following classes are used to store the vLLM information in the current environment.
# Then, Metaflow users can access the vLLM information through the current environment.
class OpenAIAPIInfo:
    def __init__(self, local_endpoint, local_api_key, model_name):
        self.local_endpoint = local_endpoint
        self.local_api_key = local_api_key
        # The model name to pass as `model=` when calling the OpenAI-compatible
        # API (e.g. client.chat.completions.create(model=..., ...)). This is
        # the logical model name (self.attributes["model"]), which vLLM is
        # configured to serve under regardless of source ('huggingface' or
        # 'anaconda') or whether a local model_path was resolved.
        self.model_name = model_name


class VLLM:
    def __init__(self, llm):
        self.llm = llm


class VLLMDecorator(StepDecorator, CardDecoratorInjector):
    """
    This decorator is used to run vllm APIs as Metaflow task sidecars.

    User code call
    --------------
    @vllm(
        model="...",
        ...
    )

    Valid backend options
    ---------------------
    - 'local': Run as a separate process on the local task machine.

    Valid model options
    -------------------
    Any HuggingFace model identifier, e.g. 'meta-llama/Llama-3.2-1B'

    NOTE: vLLM's OpenAI-compatible server serves ONE model per server instance.
    If you need multiple models, you must create multiple @vllm decorators.

    Parameters
    ----------
    model: str
        HuggingFace or Anaconda model identifier to be served by vLLM.
    backend: str
        Determines where and how to run the vLLM process.
    source: str
        Where to obtain the model from: 'huggingface' (default) or 'anaconda'.
    openai_api_server: bool
        Whether to use OpenAI-compatible API server mode (subprocess) instead of native engine.
        Default is False (uses native engine).
        Set to True for backward compatibility with existing code.
    debug: bool
        Whether to turn on verbose debugging logs.
    card_refresh_interval: int
        Interval in seconds for refreshing the vLLM status card.
        Only used when openai_api_server=True.
    max_retries: int
        Maximum number of retries checking for vLLM server startup.
        Only used when openai_api_server=True.
    retry_alert_frequency: int
        Frequency of alert logs for vLLM server startup retries.
        Only used when openai_api_server=True.
    engine_args : dict
        Additional keyword arguments to pass to the vLLM engine.
        For example, `tensor_parallel_size=2`.
    """

    name = "vllm"
    defaults = {
        "model": None,
        "backend": "local",
        "source": "huggingface",
        "openai_api_server": False,  # Default to native engine
        "debug": False,
        "stream_logs_to_card": False,
        "card_refresh_interval": 10,
        "max_retries": 60,
        "retry_alert_frequency": 5,
        "engine_args": {},
    }

    def step_init(
        self, flow, graph, step_name, decorators, environment, flow_datastore, logger
    ):
        super().step_init(
            flow, graph, step_name, decorators, environment, flow_datastore, logger
        )

        # Validate that a model is specified
        if not self.attributes["model"]:
            raise ValueError(
                f"@vllm decorator on step '{step_name}' requires a 'model' parameter. "
                f"Example: @vllm(model='meta-llama/Llama-3.2-1B')"
            )

        if self.attributes["source"] not in ("huggingface", "anaconda"):
            raise MetaflowException(
                f"@vllm 'source' must be 'huggingface' or 'anaconda', got "
                f"'{self.attributes['source']}'."
            )

        if self.attributes["source"] == "anaconda":
            if any(deco.name == "anaconda_models" for deco in decorators):
                raise MetaflowException(
                    "@anaconda_models cannot be used together with @vllm(source='anaconda') — "
                    "@vllm manages the model download automatically. "
                    "Remove @anaconda_models from this step."
                )

            # Attach a card to visualize the downloaded Anaconda model,
            # mirroring what @anaconda_models does.
            self.attach_card_decorator(flow, step_name, "anaconda_models", "blank")

        # Attach the vllm status card only for API server mode
        if self.attributes["openai_api_server"]:
            self.attach_card_decorator(
                flow,
                step_name,
                "vllm_status",
                "blank",
                refresh_interval=self.attributes["card_refresh_interval"],
            )

    def task_decorate(
        self, step_func, flow, graph, retry_count, max_user_code_retries, ubf_context
    ):
        @functools.wraps(step_func)
        def vllm_wrapper():
            # FIXME: Kind of ugly branch. Causing branching elsewhere.
            # Other possibile code paths:
            # - OpenAI batch API
            # - Embedding
            # - Special types of models
            if self.attributes["openai_api_server"]:
                # API Server mode (existing functionality)
                self._run_api_server_mode(step_func)
            else:
                # Native engine mode (new functionality)
                self._run_native_engine_mode(step_func)

        return vllm_wrapper

    def _resolve_anaconda_model(self):
        """
        Download the model from the Anaconda model catalog and return the
        AnacondaModel handle (whose `.path` is the local safetensors
        directory to hand to vLLM). Raises MetaflowException on failure.
        """
        from metaflow_extensions.outerbounds.plugins.anaconda_models.client import (
            AnacondaModelClient,
        )
        from metaflow_extensions.outerbounds.plugins.anaconda_models.exceptions import (
            ModelAccessDenied,
        )
        from metaflow_extensions.outerbounds.plugins.anaconda_models.decorator import (
            _paint_card,
            _DeniedModel,
        )

        model_name = self.attributes["model"]
        client = AnacondaModelClient()

        try:
            card = current.card["anaconda_models"]
        except Exception:
            card = None

        try:
            anaconda_model = client.model(model_name, format="safetensors")
            anaconda_model.pull()
        except ModelAccessDenied as e:
            if card is not None:
                try:
                    _paint_card(card, [_DeniedModel(name=model_name, reason=e.reason)])
                except Exception:
                    pass
            raise MetaflowException(
                f"[@vllm] Anaconda model access denied for '{model_name}': {e.reason}"
            )
        except Exception as e:
            raise MetaflowException(
                f"[@vllm] Failed to download model '{model_name}' from Anaconda catalog: {e}"
            )

        if not anaconda_model.path:
            raise MetaflowException(
                f"[@vllm] Failed to download model '{model_name}' from Anaconda catalog."
            )

        if card is not None:
            try:
                _paint_card(card, [anaconda_model])
            except Exception:
                pass

        return anaconda_model

    def _cleanup_anaconda_model(self):
        anaconda_model = getattr(self, "_anaconda_model", None)
        if anaconda_model is None:
            return
        try:
            anaconda_model.delete()
            if self.attributes["debug"]:
                print(
                    f"[@vllm] Removed downloaded model files at {anaconda_model.path}"
                )
        except Exception as e:
            print(f"[@vllm] Warning: failed to remove downloaded model files: {e}")
        finally:
            self._anaconda_model = None

    def _run_api_server_mode(self, step_func):
        """Run vLLM in API server mode (subprocess, existing functionality)"""
        self.vllm_manager = None
        self.status_card = None
        self.card_monitor_thread = None
        self._anaconda_model = None

        try:
            self.status_card = VLLMStatusCard(
                refresh_interval=self.attributes["card_refresh_interval"]
            )

            def monitor_card():
                try:
                    self.status_card.on_startup(current.card["vllm_status"])

                    while not getattr(self.card_monitor_thread, "_stop_event", False):
                        try:
                            self.status_card.on_update(
                                current.card["vllm_status"], None
                            )
                            import time

                            time.sleep(self.attributes["card_refresh_interval"])
                        except Exception as e:
                            if self.attributes["debug"]:
                                print(f"[@vllm] Card monitoring error: {e}")
                            break
                except Exception as e:
                    if self.attributes["debug"]:
                        print(f"[@vllm] Card monitor thread error: {e}")
                    self.status_card.on_error(current.card["vllm_status"], str(e))

            self.card_monitor_thread = threading.Thread(
                target=monitor_card, daemon=True
            )
            self.card_monitor_thread._stop_event = False
            self.card_monitor_thread.start()

            model_path = None
            if self.attributes["source"] == "anaconda":
                if self.status_card:
                    self.status_card.add_event(
                        "info", "Downloading model from Anaconda catalog"
                    )
                self._anaconda_model = self._resolve_anaconda_model()
                model_path = self._anaconda_model.path

            self.vllm_manager = VLLMOpenAIManager(
                model=self.attributes["model"],
                model_path=model_path,
                backend=self.attributes["backend"],
                debug=self.attributes["debug"],
                status_card=self.status_card,
                max_retries=self.attributes["max_retries"],
                retry_alert_frequency=self.attributes["retry_alert_frequency"],
                stream_logs_to_card=self.attributes["stream_logs_to_card"],
                **self.attributes["engine_args"],
            )
            current._update_env(
                dict(
                    vllm=OpenAIAPIInfo(
                        local_endpoint=f"http://127.0.0.1:{self.vllm_manager.port}/v1",
                        local_api_key="token123",
                        model_name=self.attributes["model"],
                    )
                )
            )

            if self.attributes["debug"]:
                print("[@vllm] API server mode initialized.")

        except Exception as e:
            if self.status_card:
                self.status_card.add_event("error", f"Initialization failed: {str(e)}")
                try:
                    self.status_card.on_error(current.card["vllm_status"], str(e))
                except:
                    pass
            print(f"[@vllm] Error initializing API server mode: {e}")
            raise

        try:
            if self.status_card:
                self.status_card.add_event("info", "Starting user step function")
            step_func()
            if self.status_card:
                self.status_card.add_event(
                    "success", "User step function completed successfully"
                )
        finally:
            if self.vllm_manager:
                self.vllm_manager.terminate_models()

            if self.card_monitor_thread and self.status_card:
                import time

                try:
                    self.status_card.on_update(current.card["vllm_status"], None)
                except Exception as e:
                    if self.attributes["debug"]:
                        print(f"[@vllm] Final card update error: {e}")
                time.sleep(2)

            if self.card_monitor_thread:
                self.card_monitor_thread._stop_event = True
                self.card_monitor_thread.join(timeout=5)
                if self.attributes["debug"]:
                    print("[@vllm] Card monitoring thread stopped.")

            self._cleanup_anaconda_model()

    def _run_native_engine_mode(self, step_func):
        """Run vLLM in native engine mode (direct LLM API access)"""
        self.vllm = None
        self._anaconda_model = None

        try:
            if self.attributes["debug"]:
                print("[@vllm] Initializing native engine mode")

            model_path = None
            if self.attributes["source"] == "anaconda":
                self._anaconda_model = self._resolve_anaconda_model()
                model_path = self._anaconda_model.path

            self.vllm = VLLMPyManager(
                model=self.attributes["model"],
                model_path=model_path,
                debug=self.attributes["debug"],
                **self.attributes["engine_args"],
            )
            current._update_env(dict(vllm=VLLM(llm=self.vllm.engine)))

            if self.attributes["debug"]:
                print("[@vllm] Native engine mode initialized.")

        except Exception as e:
            print(f"[@vllm] Error initializing native engine mode: {e}")
            raise

        try:
            step_func()
        finally:
            if self.vllm:
                self.vllm.terminate_engine()
            self._cleanup_anaconda_model()
