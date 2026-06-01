from typing import Any

from .payload_extractor_protocol import PayloadExtractor


class DefaultExtractor(PayloadExtractor):
    def extract(self, source: Any):
        if hasattr(source, "json") and callable(source.json):
            result = source.json()
            # Guard against .json() returning a string (e.g. httpx Response)
            # — callers expect a dict or list, not a raw JSON string.
            if isinstance(result, str):
                import json

                return json.loads(result)
            return result
        return source
