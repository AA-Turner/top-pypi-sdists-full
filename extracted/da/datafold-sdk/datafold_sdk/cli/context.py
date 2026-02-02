from dataclasses import dataclass


DATAFOLD_API_KEY = "DATAFOLD_API_KEY"
DATAFOLD_APIKEY = "DATAFOLD_APIKEY"  # obsolete spelling
DATAFOLD_HOST = "DATAFOLD_HOST"


@dataclass
class CliContext:
    host: str
    api_key: str
