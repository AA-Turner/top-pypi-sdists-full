import logging

from fluidattacks_core.logging.sources.utils import get_env_var, get_environment


class NoProductionFilter(logging.Filter):
    def filter(self, _record: logging.LogRecord) -> bool:
        return get_environment() != "production"


class ProductionOnlyFilter(logging.Filter):
    def filter(self, _record: logging.LogRecord) -> bool:
        return get_environment() == "production"


class ErrorOnlyFilter(logging.Filter):
    def filter(self, _record: logging.LogRecord) -> bool:
        return _record.levelno >= logging.ERROR


class EnabledTelemetryFilter(logging.Filter):
    def filter(self, _record: logging.LogRecord) -> bool:
        return str(get_env_var("TELEMETRY_OPT_OUT")).lower() != "true"
