from datetime import datetime
import json
import logging


class GCPJsonFormatter(logging.Formatter):
    """
    Custom JSON formatter for Google Cloud Platform logging.

    Outputs logs in JSON format with a 'severity' field that GCP Cloud Logging
    can properly parse. This ensures INFO logs show up as INFO in GCP instead of ERROR.

    See: https://cloud.google.com/logging/docs/structured-logging
    """

    SEVERITY_MAP = {
        "DEBUG": "DEBUG",
        "INFO": "INFO",
        "WARNING": "WARNING",
        "ERROR": "ERROR",
        "CRITICAL": "CRITICAL",
    }

    def format(self, record: logging.LogRecord) -> str:
        log_obj = {
            "severity": self.SEVERITY_MAP.get(record.levelname, "DEFAULT"),
            "message": record.getMessage(),
            "timestamp": datetime.utcfromtimestamp(record.created).isoformat() + "Z",
            "logging.googleapis.com/sourceLocation": {
                "file": record.pathname,
                "line": record.lineno,
                "function": record.funcName,
            },
        }

        if record.exc_info:
            log_obj["exception"] = self.formatException(record.exc_info)

        return json.dumps(log_obj)
