from cuga.config import settings


def is_benchmark_mode() -> bool:
    """Check if benchmark mode is enabled (non-default benchmark setting).

    Returns:
        True if benchmark mode is enabled, False otherwise
    """
    return settings.advanced_features.benchmark != "default"
