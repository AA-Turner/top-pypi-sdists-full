from enum import Enum

class Connector_type(str, Enum):
    Http = "http",
    Sse = "sse",
    Internal = "internal",

