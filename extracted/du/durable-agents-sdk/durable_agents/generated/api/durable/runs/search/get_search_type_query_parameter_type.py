from enum import Enum

class GetSearch_typeQueryParameterType(str, Enum):
    Keyword = "keyword",
    Vector = "vector",
    Hybrid = "hybrid",

