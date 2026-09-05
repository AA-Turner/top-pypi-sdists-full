######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.19.37.3+obcheckpoint(0.2.10);<unk>(<unk>);ob(v1)                                     #
# Generated on 2026-09-04T19:03:46.104805                                                            #
######################################################################################################

from __future__ import annotations



class LlamaCppPyManager(object, metaclass=type):
    """
    A native llama.cpp engine manager that provides direct access to the
    llama-cpp-python `Llama` class.
    
    Example usage:
        llm = current.llamacpp.llm
        output = llm.create_chat_completion(
            messages=[{"role": "user", "content": "Hello"}]
        )
    """
    def __init__(self, model, gguf_or_quant, model_path, debug = False, **llama_kwargs):
        ...
    def terminate_engine(self):
        """
        Clean up the native engine.
        """
        ...
    ...

