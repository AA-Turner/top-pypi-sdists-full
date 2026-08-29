import glob
import os

from metaflow import current, user_step_decorator
from metaflow.exception import MetaflowException
from metaflow.user_decorators.user_step_decorator import StepMutator

from .llamacpp_manager import LlamaCppPyManager

__mf_promote_submodules__ = ["plugins.llamacpp"]


class LlamaCpp:
    def __init__(self, llm):
        self.llm = llm


def _gguf_or_quant(attr):
    return attr.get("gguf_filename") or attr["quant"]


def _anaconda_model_filters(attr):
    if attr.get("quant"):
        return {"quant_method": attr["quant"]}
    return {"filename": attr["gguf_filename"]}


def _huggingface_allow_pattern(attr):
    if attr.get("quant"):
        return "*{}*.gguf".format(attr["quant"])
    return attr["gguf_filename"]


def _resolve_huggingface_model_path(model_dir, allow_pattern):
    matches = sorted(
        glob.glob(os.path.join(model_dir, "**", allow_pattern), recursive=True)
    )
    if len(matches) == 1:
        return matches[0]
    if not matches:
        raise MetaflowException(
            "[@llamacpp] No downloaded GGUF file matches pattern {!r} in {!r}.".format(
                allow_pattern, model_dir
            )
        )
    raise MetaflowException(
        "[@llamacpp] Multiple downloaded GGUF files match pattern {!r} in {!r}: {}. "
        "Specify 'gguf_filename' to select one file.".format(
            allow_pattern, model_dir, matches
        )
    )


@user_step_decorator
def _llamacpp_huggingface_wrapper(step_name, flow, inputs=None, attr=None):
    attr = attr or {}
    debug = attr.get("debug", False)
    gguf_or_quant = _gguf_or_quant(attr)
    allow_pattern = _huggingface_allow_pattern(attr)

    manager = None
    try:
        with current.huggingface_hub.load(
            repo_id=attr["model"],
            allow_patterns=[allow_pattern],
        ) as model_dir:
            model_path = _resolve_huggingface_model_path(model_dir, allow_pattern)
            manager = LlamaCppPyManager(
                model=attr["model"],
                gguf_or_quant=gguf_or_quant,
                model_path=model_path,
                debug=debug,
                **attr.get("llama_args", {}),
            )
            current._update_env(dict(llamacpp=LlamaCpp(llm=manager.engine)))
            if debug:
                print("[@llamacpp] HuggingFace native engine initialized.")

            yield

    except Exception as e:
        print(f"[@llamacpp] Error initializing engine: {e}")
        raise
    finally:
        if manager:
            manager.terminate_engine()


@user_step_decorator
def _llamacpp_anaconda_wrapper(step_name, flow, inputs=None, attr=None):
    attr = attr or {}
    debug = attr.get("debug", False)
    gguf_or_quant = _gguf_or_quant(attr)
    filters = _anaconda_model_filters(attr)

    anaconda_model = flow.anaconda_models.model(attr["model"], pull=True, **filters)

    if hasattr(anaconda_model, "access_denied_reason"):
        raise MetaflowException(
            f"[@llamacpp] Anaconda model access denied for '{attr['model']}': "
            f"{anaconda_model.access_denied_reason}"
        )

    if not anaconda_model.path:
        raise MetaflowException(
            f"[@llamacpp] Failed to download model '{attr['model']}' "
            f"(model selector='{gguf_or_quant}') from Anaconda catalog."
        )

    manager = None
    try:
        manager = LlamaCppPyManager(
            model=attr["model"],
            gguf_or_quant=gguf_or_quant,
            model_path=anaconda_model.path,
            debug=debug,
            **attr.get("llama_args", {}),
        )
        current._update_env(dict(llamacpp=LlamaCpp(llm=manager.engine)))
        if debug:
            print("[@llamacpp] Anaconda native engine initialized.")

        yield

    except Exception as e:
        print(f"[@llamacpp] Error initializing engine: {e}")
        raise
    finally:
        if manager:
            manager.terminate_engine()
        try:
            anaconda_model.delete()
            if debug:
                print(
                    f"[@llamacpp] Removed downloaded model files at {anaconda_model.path}"
                )
        except Exception as e:
            print(f"[@llamacpp] Warning: failed to remove downloaded model files: {e}")


class llamacpp(StepMutator):
    """
    Load a llama.cpp model as a native in-process engine for a Metaflow step,
    via llama-cpp-python.

    Parameters
    ----------
    model : str
        HuggingFace-style model name (e.g. 'bartowski/Meta-Llama-3.1-8B-Instruct-GGUF').
    gguf_filename : str, optional
        GGUF filename to load (e.g. 'Meta-Llama-3.1-8B-Instruct-Q4_K_M.gguf').
        Either ``gguf_filename`` or ``quant`` must be provided.
    quant : str, optional
        Quantization selector (e.g. 'q4_k_m', 'q8_0', etc).
         Either ``quant`` or ``gguf_filename`` must be provided.
    source : str
        Model source: 'huggingface' (default) or 'anaconda'.
    debug : bool
        Enable verbose debug logging.
    llama_args : dict
        Extra keyword arguments passed directly to `llama_cpp.Llama(...)`,
        e.g. {'n_gpu_layers': 99, 'n_ctx': 4096}.

    Usage
    -----
    ```python
    from metaflow import FlowSpec, step, current, kubernetes, conda, llamacpp

    class MyFlow(FlowSpec):
        @llamacpp(
            model="Qwen/Qwen2.5-0.5B-Instruct",
            quant="q8_0",
            source="anaconda",
        )
        @conda(
            python="3.13",
            packages={
                "llama-cpp-python": ">=0.3.35",
                "llama.cpp": "=*=cpu_*",
            },
        )
        @kubernetes(
            cpu=1.8,
            memory=8192,
            disk=10240,
        )
        @step
        def start(self):
            llm = current.llamacpp.llm
            self.messages = [
                {
                    "role": "system",
                    "content": "You are a helpful assistant.",
                },
                {
                    "role": "user",
                    "content": "Explain the basics of metaflow to me.",
                },
            ]
            outputs = llm.create_chat_completion(self.messages)
            self.response = outputs["choices"][0]["message"]["content"]

            print(self.messages[-1]["content"])
            print(self.response)

            self.next(self.end)

        @step
        def end(self):
            pass
    ```
    """

    def init(
        self,
        model,
        *,
        gguf_filename=None,
        quant=None,
        source="huggingface",
        debug=False,
        llama_args=None,
    ):
        if source not in ("huggingface", "anaconda"):
            raise MetaflowException(
                f"@llamacpp 'source' must be 'huggingface' or 'anaconda', got '{source}'."
            )
        if (gguf_filename is None) == (quant is None):
            raise MetaflowException(
                "@llamacpp requires exactly one of 'gguf_filename' or 'quant'."
            )
        self._attrs = dict(
            model=model,
            gguf_filename=gguf_filename,
            quant=quant,
            source=source,
            debug=debug,
            llama_args=llama_args or {},
        )

    def pre_mutate(self, mutable_step):
        names = [s[0] for s in mutable_step.decorator_specs]

        if "anaconda_models" in names:
            raise MetaflowException(
                "@anaconda_models cannot be used together with @llamacpp — "
                "@llamacpp manages the model download automatically. "
                "Remove @anaconda_models from this step."
            )

        if "huggingface_hub" in names:
            raise MetaflowException(
                "@huggingface_hub cannot be used together with @llamacpp — "
                "@llamacpp manages the model download automatically. "
                "Remove @huggingface_hub from this step."
            )

        if (
            "_llamacpp_huggingface_wrapper" in names
            or "_llamacpp_anaconda_wrapper" in names
        ):
            return

        if self._attrs["source"] == "anaconda":
            from metaflow_extensions.outerbounds.plugins.anaconda_models.decorator import (
                anaconda_models,
            )

            mutable_step.add_decorator(
                anaconda_models,
                deco_kwargs={},
                duplicates=mutable_step.IGNORE,
            )
            mutable_step.add_decorator(
                _llamacpp_anaconda_wrapper,
                deco_kwargs=self._attrs,
                duplicates=mutable_step.ERROR,
            )
        else:
            from metaflow import huggingface_hub

            mutable_step.add_decorator(
                huggingface_hub,
                deco_kwargs={"cache_scope": "global"},
                duplicates=mutable_step.IGNORE,
            )
            mutable_step.add_decorator(
                _llamacpp_huggingface_wrapper,
                deco_kwargs=self._attrs,
                duplicates=mutable_step.ERROR,
            )
