import orjson
import timeit
from functools import lru_cache
from copy import deepcopy

# Example JSON string
json_str = '{"name": "John Doe", "age": 30, "active": true, "roles": ["admin", "user"], "meta": {"last_login": "2024-03-06T12:34:56", "preferences": {"theme": "dark", "notifications": false}}}'

@lru_cache(maxsize=None)
def cached_orjson_loads(s):
    return orjson.loads(s)

def deserialize_direct():
    return orjson.loads(json_str)

def deserialize_cached_with_deepcopy():
    cached_result = cached_orjson_loads(json_str)
    return deepcopy(cached_result)

def benchmark():
    iterations = 100000

    direct_time = timeit.timeit(deserialize_direct, number=iterations)
    cached_deepcopy_time = timeit.timeit(deserialize_cached_with_deepcopy, number=iterations)

    print(f"Direct orjson.loads: {direct_time:.6f}s total ({direct_time/iterations:.8f}s per call)")
    print(f"lru_cache + deepcopy: {cached_deepcopy_time:.6f}s total ({cached_deepcopy_time/iterations:.8f}s per call)")

    faster_method = "Direct deserialization" if direct_time < cached_deepcopy_time else "lru_cache + deepcopy"
    print(f"\nFaster method: {faster_method}")

if __name__ == "__main__":
    benchmark()
