"""
Utility functions for DSPy integration.
"""

import logging
from typing import Any

logger = logging.getLogger(__name__)


def is_dspy_available() -> bool:
    """Check if DSPy is installed and importable.

    Returns:
        True if DSPy is available
    """
    try:
        import dspy

        return True
    except ImportError:
        return False


def get_dspy_version() -> str | None:
    """Get the installed DSPy version.

    Returns:
        Version string or None if not installed
    """
    try:
        import dspy

        return getattr(dspy, "__version__", "unknown")
    except ImportError:
        return None


def safe_str(value: Any, max_length: int = 1000) -> str:
    """Safely convert a value to string with length limit.

    Args:
        value: Value to convert
        max_length: Maximum length of output string

    Returns:
        String representation, truncated if necessary
    """
    try:
        if value is None:
            return ""
        s = str(value)
        if len(s) > max_length:
            return s[:max_length] + "..."
        return s
    except Exception as e:
        return f"<error: {e}>"


def extract_module_info(module: Any) -> dict[str, Any]:
    """Extract information from a DSPy module.

    Args:
        module: The module object

    Returns:
        Dictionary with module information
    """
    info = {
        "name": module.__class__.__name__,
        "type": "module",
        "signature": None,
        "has_demos": False,
    }

    try:
        # Determine module type
        class_name = module.__class__.__name__

        if "ChainOfThought" in class_name:
            info["type"] = "chain_of_thought"
        elif "ReAct" in class_name:
            info["type"] = "react"
        elif "Retrieve" in class_name:
            info["type"] = "retriever"
        elif "Predict" in class_name or hasattr(module, "signature"):
            info["type"] = "predict"

        # Get signature info
        if hasattr(module, "signature"):
            sig = module.signature
            if hasattr(sig, "__name__"):
                info["signature"] = sig.__name__
            elif hasattr(sig, "signature"):
                info["signature"] = str(sig.signature)
            else:
                info["signature"] = str(sig)

            # Get input/output fields
            if hasattr(sig, "input_fields"):
                info["input_fields"] = list(sig.input_fields.keys()) if sig.input_fields else []
            if hasattr(sig, "output_fields"):
                info["output_fields"] = list(sig.output_fields.keys()) if sig.output_fields else []

        # Check for demonstrations
        if hasattr(module, "demos") and module.demos:
            info["has_demos"] = True
            info["demo_count"] = len(module.demos)

        # Get submodules
        if hasattr(module, "named_predictors"):
            try:
                predictors = list(module.named_predictors())
                info["submodules"] = [name for name, _ in predictors]
            except Exception:
                pass

    except Exception as e:
        logger.debug(f"Error extracting module info: {e}")

    return info


def extract_prediction_info(prediction: Any) -> dict[str, Any]:
    """Extract information from a DSPy Prediction object.

    Args:
        prediction: The Prediction object

    Returns:
        Dictionary with prediction information
    """
    info = {
        "fields": {},
        "reasoning": None,
    }

    try:
        if hasattr(prediction, "__dict__"):
            for key, value in prediction.__dict__.items():
                if not key.startswith("_"):
                    if key in ("rationale", "reasoning"):
                        info["reasoning"] = safe_str(value, 500)
                    else:
                        info["fields"][key] = safe_str(value, 200)

        # Check for completions (raw LLM outputs)
        if hasattr(prediction, "completions"):
            info["has_completions"] = True
            info["completion_count"] = len(prediction.completions) if prediction.completions else 0

    except Exception as e:
        logger.debug(f"Error extracting prediction info: {e}")

    return info


def extract_signature_info(signature: Any) -> dict[str, Any]:
    """Extract information from a DSPy Signature.

    Args:
        signature: The Signature class or instance

    Returns:
        Dictionary with signature information
    """
    info = {
        "name": None,
        "input_fields": [],
        "output_fields": [],
        "instructions": None,
    }

    try:
        # Get name
        if hasattr(signature, "__name__"):
            info["name"] = signature.__name__
        elif hasattr(signature, "signature"):
            info["name"] = str(signature.signature)

        # Get fields
        if hasattr(signature, "input_fields"):
            info["input_fields"] = (
                list(signature.input_fields.keys()) if signature.input_fields else []
            )
        if hasattr(signature, "output_fields"):
            info["output_fields"] = (
                list(signature.output_fields.keys()) if signature.output_fields else []
            )

        # Get instructions/docstring
        if hasattr(signature, "__doc__") and signature.__doc__:
            info["instructions"] = signature.__doc__

    except Exception as e:
        logger.debug(f"Error extracting signature info: {e}")

    return info


def format_demonstrations(demos: list[Any], max_demos: int = 5) -> list[dict[str, Any]]:
    """Format demonstrations for tracing.

    Args:
        demos: List of demonstration examples
        max_demos: Maximum number of demos to include

    Returns:
        List of formatted demonstration dictionaries
    """
    formatted = []

    for demo in demos[:max_demos]:
        demo_dict = {}

        try:
            if hasattr(demo, "__dict__"):
                for key, value in demo.__dict__.items():
                    if not key.startswith("_"):
                        demo_dict[key] = safe_str(value, 200)
            else:
                demo_dict["value"] = safe_str(demo, 500)

            formatted.append(demo_dict)

        except Exception as e:
            formatted.append({"error": str(e)})

    if len(demos) > max_demos:
        formatted.append({"note": f"... and {len(demos) - max_demos} more demos"})

    return formatted


def get_lm_info() -> dict[str, Any]:
    """Get information about the current DSPy language model.

    Returns:
        Dictionary with LM information
    """
    info = {
        "model": None,
        "provider": None,
        "temperature": None,
    }

    try:
        import dspy

        if hasattr(dspy, "settings") and hasattr(dspy.settings, "lm"):
            lm = dspy.settings.lm
            if lm:
                if hasattr(lm, "model"):
                    info["model"] = lm.model
                if hasattr(lm, "provider"):
                    info["provider"] = lm.provider
                if hasattr(lm, "temperature"):
                    info["temperature"] = lm.temperature

                # Try to get model name from string representation
                if not info["model"]:
                    info["model"] = str(lm)[:100]

    except Exception as e:
        logger.debug(f"Error getting LM info: {e}")

    return info


def extract_optimizer_info(optimizer: Any) -> dict[str, Any]:
    """Extract information from a DSPy optimizer.

    Args:
        optimizer: The optimizer object

    Returns:
        Dictionary with optimizer information
    """
    info = {
        "name": optimizer.__class__.__name__,
        "type": "optimizer",
        "metric": None,
    }

    try:
        # Get metric info
        if hasattr(optimizer, "metric"):
            metric = optimizer.metric
            if hasattr(metric, "__name__"):
                info["metric"] = metric.__name__
            else:
                info["metric"] = str(metric)[:100]

        # Get configuration
        if hasattr(optimizer, "config"):
            config = optimizer.config
            if isinstance(config, dict):
                info["config"] = {k: str(v)[:100] for k, v in list(config.items())[:10]}

        # Get specific optimizer params
        if hasattr(optimizer, "num_candidates"):
            info["num_candidates"] = optimizer.num_candidates
        if hasattr(optimizer, "max_bootstrapped_demos"):
            info["max_bootstrapped_demos"] = optimizer.max_bootstrapped_demos
        if hasattr(optimizer, "num_threads"):
            info["num_threads"] = optimizer.num_threads

    except Exception as e:
        logger.debug(f"Error extracting optimizer info: {e}")

    return info


def mask_sensitive_content(content: str, patterns: list[str] | None = None) -> str:
    """Mask potentially sensitive content in strings.

    Args:
        content: Content to mask
        patterns: Optional list of regex patterns to mask

    Returns:
        Content with sensitive data masked
    """
    import re

    if not content:
        return content

    # Default patterns for common sensitive data
    default_patterns = [
        (r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b", "[EMAIL]"),
        (r"\b\d{3}[-.]?\d{3}[-.]?\d{4}\b", "[PHONE]"),
        (r"\b\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b", "[CARD]"),
        (r"\b\d{3}[-]?\d{2}[-]?\d{4}\b", "[SSN]"),
        (r"(?i)(password|secret|token|api_key|apikey|bearer)[\s]*[=:][\s]*[^\s,]+", "[REDACTED]"),
    ]

    patterns_to_use = patterns if patterns is not None else default_patterns

    result = content
    for pattern, replacement in patterns_to_use:
        result = re.sub(pattern, replacement, result)

    return result
