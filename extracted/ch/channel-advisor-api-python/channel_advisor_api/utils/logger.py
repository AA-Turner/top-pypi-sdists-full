from aws_lambda_powertools import Logger

# Define common logging configuration
DEFAULT_LOG_RECORD_ORDER = ["message", "service", "location", "level"]


def get_logger(service_name: str) -> Logger:
    """Create a logger with consistent configuration."""
    return Logger(service=service_name, log_record_order=DEFAULT_LOG_RECORD_ORDER)
