from datadog_serverless_compat.logger import initialize_logging

initialize_logging(__name__)

from datadog_serverless_compat.main import start  # noqa: E402 F401
