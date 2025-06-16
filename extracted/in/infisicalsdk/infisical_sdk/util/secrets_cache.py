from typing import Dict, Tuple, Any

from infisical_sdk.api_types import BaseSecret
import json
import time
import threading
from hashlib import sha256
import pickle

MAX_CACHE_SIZE = 1000

class SecretsCache:
    def __init__(self, ttl_seconds: int = 60) -> None:
      if ttl_seconds is None or ttl_seconds <= 0:
          self.enabled = False
          return
    
      self.enabled = True
      self.ttl = ttl_seconds
      self.cleanup_interval = 60

      self.cache: Dict[str, Tuple[bytes, float]] = {}

      self.lock = threading.RLock()

      self.stop_cleanup_thread = False
      self.cleanup_thread = threading.Thread(target=self._cleanup_worker, daemon=True)
      self.cleanup_thread.start()

    def compute_cache_key(self, operation_name: str, **kwargs) -> str:
      sorted_kwargs = sorted(kwargs.items())
      json_str = json.dumps(sorted_kwargs)

      return f"{operation_name}-{sha256(json_str.encode()).hexdigest()}"
  
    def get(self, cache_key: str) -> Any:
      if not self.enabled:
        return None

      with self.lock:
          if cache_key in self.cache:
              serialized_value, timestamp = self.cache[cache_key]
              if time.time() - timestamp <= self.ttl:
                  return pickle.loads(serialized_value)
              else:
                  self.cache.pop(cache_key, None)
                  return None
          else:
              return None
            
            
    def set(self, cache_key: str, value: Any) -> None:
      if not self.enabled:
        return

      with self.lock:
        serialized_value = pickle.dumps(value)
        self.cache[cache_key] = (serialized_value, time.time())

        if len(self.cache) > MAX_CACHE_SIZE:
          oldest_key = min(self.cache.keys(), key=lambda k: self.cache[k][1]) # oldest key based on timestamp
          self.cache.pop(oldest_key)



    def unset(self, cache_key: str) -> None:
      if not self.enabled:
        return

      with self.lock:
        self.cache.pop(cache_key, None)

    def invalidate_operation(self, operation_name: str) -> None:
      if not self.enabled:
        return

      with self.lock:
        for key in list(self.cache.keys()):
          if key.startswith(operation_name):
            self.cache.pop(key, None)


    def _cleanup_expired_items(self) -> None:
      """Remove all expired items from the cache."""
      current_time = time.time()
      with self.lock:
          expired_keys = [
              key for key, (_, timestamp) in self.cache.items() 
              if current_time - timestamp > self.ttl
          ]
          for key in expired_keys:
              self.cache.pop(key, None)
  
    def _cleanup_worker(self) -> None:
      """Background worker that periodically cleans up expired items."""
      while not self.stop_cleanup_thread:
        time.sleep(self.cleanup_interval)
        self._cleanup_expired_items()

    def __del__(self) -> None:
      """Ensure thread is properly stopped when the object is garbage collected."""
      self.stop_cleanup_thread = True
      if self.enabled and self.cleanup_thread.is_alive():
        self.cleanup_thread.join(timeout=1.0)
        
        