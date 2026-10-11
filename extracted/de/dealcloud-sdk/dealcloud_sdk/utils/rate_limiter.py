"""
Rate limiter for API calls to respect DealCloud API rate limits.

DealCloud API enforces rate limits:
- Data endpoints: 5 requests/second
- Schema endpoints: 5 requests/second
- User Management: 5 requests/second

This module provides a thread-safe rate limiter to ensure compliance.
"""

import time
import threading
from typing import Optional


class RateLimiter:
    """
    Thread-safe rate limiter for API calls.
    
    Ensures API calls don't exceed the specified rate limit by enforcing
    a minimum interval between calls.
    
    Example:
        >>> limiter = RateLimiter(max_calls_per_second=4.0)
        >>> for i in range(10):
        ...     limiter.wait_if_needed()
        ...     make_api_call()
    """
    
    def __init__(self, max_calls_per_second: float = 4.0):
        """
        Initialize rate limiter.
        
        Args:
            max_calls_per_second: Maximum calls per second (default: 4.0 for safety margin)
                                  Should be < 5 to respect DealCloud API limits
        """
        if max_calls_per_second <= 0:
            raise ValueError("max_calls_per_second must be positive")
        if max_calls_per_second > 5:
            import warnings
            warnings.warn(
                f"Rate limiter set to {max_calls_per_second}/second, but DealCloud API "
                f"limits Data endpoints to 5/second. This may cause 429 errors.",
                UserWarning
            )
        
        self.max_calls_per_second = max_calls_per_second
        self.min_interval = 1.0 / max_calls_per_second
        self.last_call_time = 0.0
        self._lock = threading.Lock()
    
    def wait_if_needed(self):
        """
        Wait if needed to respect rate limit.
        
        Thread-safe method that ensures minimum interval between calls.
        If called too soon after the last call, it will sleep to maintain
        the rate limit.
        
        Example:
            >>> limiter = RateLimiter(max_calls_per_second=4.0)
            >>> limiter.wait_if_needed()  # First call, no wait
            >>> limiter.wait_if_needed()  # Waits ~0.25 seconds
        """
        with self._lock:
            now = time.time()
            elapsed = now - self.last_call_time
            
            if elapsed < self.min_interval:
                sleep_time = self.min_interval - elapsed
                time.sleep(sleep_time)
                self.last_call_time = time.time()
            else:
                self.last_call_time = now
    
    def reset(self):
        """
        Reset the rate limiter.
        
        Useful for testing or when you want to allow immediate calls
        after a period of inactivity.
        """
        with self._lock:
            self.last_call_time = 0.0
    
    def __repr__(self) -> str:
        return f"RateLimiter(max_calls_per_second={self.max_calls_per_second})"


class AsyncRateLimiter:
    """
    Async rate limiter for API calls in async contexts.
    
    Ensures API calls don't exceed the specified rate limit by enforcing
    a minimum interval between calls using async/await.
    
    Example:
        >>> limiter = AsyncRateLimiter(max_calls_per_second=4.0)
        >>> async for item in items:
        ...     await limiter.wait_if_needed()
        ...     await make_api_call()
    """
    
    def __init__(self, max_calls_per_second: float = 4.0):
        """
        Initialize async rate limiter.
        
        Args:
            max_calls_per_second: Maximum calls per second (default: 4.0 for safety margin)
                                  Should be < 5 to respect DealCloud API limits
        """
        if max_calls_per_second <= 0:
            raise ValueError("max_calls_per_second must be positive")
        if max_calls_per_second > 5:
            import warnings
            warnings.warn(
                f"Rate limiter set to {max_calls_per_second}/second, but DealCloud API "
                f"limits Data endpoints to 5/second. This may cause 429 errors.",
                UserWarning
            )
        
        self.max_calls_per_second = max_calls_per_second
        self.min_interval = 1.0 / max_calls_per_second
        self.last_call_time = 0.0
        self._lock = None  # Will be asyncio.Lock, created lazily
    
    async def wait_if_needed(self):
        """
        Wait if needed to respect rate limit (async).
        
        Async method that ensures minimum interval between calls.
        If called too soon after the last call, it will sleep asynchronously
        to maintain the rate limit without blocking the event loop.
        
        Example:
            >>> limiter = AsyncRateLimiter(max_calls_per_second=4.0)
            >>> await limiter.wait_if_needed()  # First call, no wait
            >>> await limiter.wait_if_needed()  # Waits ~0.25 seconds (non-blocking)
        """
        import asyncio
        
        # Create lock lazily (can't do in __init__ because we might not be in async context)
        if self._lock is None:
            self._lock = asyncio.Lock()
        
        async with self._lock:
            now = time.time()
            elapsed = now - self.last_call_time
            
            if elapsed < self.min_interval:
                sleep_time = self.min_interval - elapsed
                await asyncio.sleep(sleep_time)
                self.last_call_time = time.time()
            else:
                self.last_call_time = now
    
    def reset(self):
        """
        Reset the rate limiter.
        
        Useful for testing or when you want to allow immediate calls
        after a period of inactivity.
        """
        self.last_call_time = 0.0
    
    def __repr__(self) -> str:
        return f"AsyncRateLimiter(max_calls_per_second={self.max_calls_per_second})"
