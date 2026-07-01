from enum import Enum

class ConnectorCreate_type(str, Enum):
    Http = "http",
    Sse = "sse",

