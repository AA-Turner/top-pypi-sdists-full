"""
Configuration for DSPy integration.
"""

from dataclasses import dataclass, field


@dataclass
class DSPyConfig:
    """Configuration for DSPy tracing.

    Attributes:
        trace_modules: Enable module execution tracing
        trace_predictions: Enable prediction call tracing
        trace_optimizations: Enable optimizer/compilation tracing
        trace_retrievers: Enable retriever call tracing
        trace_reasoning: Enable detailed reasoning step tracing (CoT, ReAct)
        capture_inputs: Capture input arguments
        capture_outputs: Capture output predictions
        capture_signatures: Capture signature details
        capture_demonstrations: Capture few-shot examples
        max_input_length: Maximum input length to capture
        max_output_length: Maximum output length to capture
        max_demonstrations: Maximum number of demonstrations to capture
        module_timeout: Timeout for module execution in seconds
        prediction_timeout: Timeout for LLM prediction in seconds
        max_retries: Maximum retry attempts for failed operations
        retry_delay: Initial delay between retries in seconds
        sensitive_patterns: Patterns to mask in captured content
    """

    # Tracing toggles
    trace_modules: bool = True
    trace_predictions: bool = True
    trace_optimizations: bool = True
    trace_retrievers: bool = True
    trace_reasoning: bool = True

    # Capture settings
    capture_inputs: bool = True
    capture_outputs: bool = True
    capture_signatures: bool = True
    capture_demonstrations: bool = True
    max_input_length: int = 2000
    max_output_length: int = 2000
    max_demonstrations: int = 5

    # Timeouts
    module_timeout: float = 120.0  # 2 minutes per module
    prediction_timeout: float = 60.0  # 1 minute per prediction
    optimization_timeout: float = 3600.0  # 1 hour for optimization

    # Retry settings
    max_retries: int = 3
    retry_delay: float = 1.0

    # Privacy
    sensitive_patterns: list[str] = field(default_factory=list)

    def __post_init__(self):
        """Validate configuration."""
        if self.max_input_length < 0:
            raise ValueError("max_input_length must be non-negative")
        if self.max_output_length < 0:
            raise ValueError("max_output_length must be non-negative")
        if self.max_demonstrations < 0:
            raise ValueError("max_demonstrations must be non-negative")
        if self.module_timeout <= 0:
            raise ValueError("module_timeout must be positive")
        if self.prediction_timeout <= 0:
            raise ValueError("prediction_timeout must be positive")
        if self.optimization_timeout <= 0:
            raise ValueError("optimization_timeout must be positive")
        if self.max_retries < 0:
            raise ValueError("max_retries must be non-negative")
        if self.retry_delay < 0:
            raise ValueError("retry_delay must be non-negative")


# Default configuration
DEFAULT_CONFIG = DSPyConfig()
