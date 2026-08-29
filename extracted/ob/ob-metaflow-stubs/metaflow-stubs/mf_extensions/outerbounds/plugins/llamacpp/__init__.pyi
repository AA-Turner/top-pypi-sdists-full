######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.19.37.2+obcheckpoint(0.2.10);<unk>(<unk>);ob(v1)                                     #
# Generated on 2026-08-28T18:11:58.363771                                                            #
######################################################################################################

from __future__ import annotations

import metaflow
import typing
if typing.TYPE_CHECKING:
    import metaflow.user_decorators.user_step_decorator

from .....metaflow_current import current as current
from .....user_decorators.user_step_decorator import user_step_decorator as user_step_decorator
from .....exception import MetaflowException as MetaflowException
from .....user_decorators.user_step_decorator import StepMutator as StepMutator
from . import llamacpp_manager as llamacpp_manager
from .llamacpp_manager import LlamaCppPyManager as LlamaCppPyManager

class LlamaCpp(object, metaclass=type):
    def __init__(self, llm):
        ...
    ...

class llamacpp(metaflow.user_decorators.user_step_decorator.StepMutator, metaclass=metaflow.user_decorators.user_step_decorator.UserStepDecoratorMeta):
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
    def init(self, model, *, gguf_filename = None, quant = None, source = 'huggingface', debug = False, llama_args = None):
        ...
    def pre_mutate(self, mutable_step):
        ...
    @classmethod
    def __init_subclass__(cls_, **_kwargs):
        ...
    ...

