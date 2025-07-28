from typing import Dict, Any
from collections import OrderedDict


class CacheManager:
    def __init__(self, max_cache_size: int = 5):
        self.cache: Dict[str, OrderedDict[str, Any]] = {}
        self.max_cache_size = max_cache_size

    def get_cached_result(self, input_hash: str, stream_key: str = None):
        if not stream_key:
            stream_key = "default_stream_key"
        stream_cache = self.cache.get(stream_key, OrderedDict())
        if input_hash in stream_cache:
            # Move to end (most recently used)
            stream_cache.move_to_end(input_hash)
            return stream_cache[input_hash]
        return None

    def set_cached_result(self, input_hash: str, value: dict, stream_key: str = None):
        if not stream_key:
            stream_key = "default_stream_key"
        if stream_key not in self.cache:
            self.cache[stream_key] = OrderedDict()
        
        stream_cache = self.cache[stream_key]
        
        # If key already exists, update and move to end
        if input_hash in stream_cache:
            stream_cache[input_hash] = value
            stream_cache.move_to_end(input_hash)
        else:
            # Add new entry
            stream_cache[input_hash] = value
            # Remove oldest entries if cache exceeds max size
            while len(stream_cache) > self.max_cache_size:
                stream_cache.popitem(last=False)  # Remove oldest (first) item

    def clear_cache(self, stream_key: str = None):
        if not stream_key:
            stream_key = "default_stream_key"
        self.cache.pop(stream_key, None)
