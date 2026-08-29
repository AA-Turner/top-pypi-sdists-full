class LlamaCppPyManager:
    """
    A native llama.cpp engine manager that provides direct access to the
    llama-cpp-python `Llama` class.

    Example usage:
        llm = current.llamacpp.llm
        output = llm.create_chat_completion(
            messages=[{"role": "user", "content": "Hello"}]
        )
    """

    def __init__(
        self,
        model,
        gguf_or_quant,
        model_path,
        debug=False,
        **llama_kwargs,
    ):
        self.repo_id = model
        self.gguf_or_quant = gguf_or_quant
        self.model_path = model_path
        self.debug = debug
        self.llama_kwargs = llama_kwargs
        self.engine = None

        self._validate_llamacpp_installation()
        self._initialize_engine()

    def _validate_llamacpp_installation(self):
        """Validate that llama-cpp-python is properly installed"""
        try:
            import llama_cpp

            if self.debug:
                print(
                    f"[@llamacpp] llama-cpp-python is available (model_path={self.model_path})"
                )
        except ImportError as e:
            raise ImportError(
                "llama-cpp-python not installed. Please add it to your environment."
            ) from e

    def _initialize_engine(self):
        """Initialize the native llama.cpp Llama engine"""
        try:
            from llama_cpp import Llama

            if self.debug:
                print(
                    f"[@llamacpp] Initializing Llama with kwargs: {self.llama_kwargs}"
                )

            self.engine = Llama(model_path=self.model_path, **self.llama_kwargs)

            if self.debug:
                print("[@llamacpp] Engine is ready.")

        except Exception as e:
            raise RuntimeError(f"Error initializing llama.cpp engine: {e}") from e

    def terminate_engine(self):
        """Clean up the native engine."""
        if self.debug:
            print("[@llamacpp] Cleaning up llama.cpp engine")

        if self.engine is not None:
            # `close` introduced in newer versions; use if available
            close = getattr(self.engine, "close", None)
            if callable(close):
                close()
            self.engine = None

        if self.debug:
            print("[@llamacpp] Engine cleanup completed")
