from .imports import *
@dataclass
class ChunkParams:
    text: str
    max_tokens: int = 1000
    model_name: str = "gpt-4"
    encoding_name: str = None
    overlap: int = 0
    verbose: bool = False
    reverse: bool = False
