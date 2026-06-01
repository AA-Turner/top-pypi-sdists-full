from typing import Any, Protocol


class PayloadExtractor(Protocol):
    def extract(self, source: Any) -> Any: ...
