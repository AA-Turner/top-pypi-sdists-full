import time
import asyncio
from typing import Union, TypeVar, Callable, Optional, Awaitable

from .polling import PollingConfig, PollingTimeout

T = TypeVar('T')

async def async_poll_until(
    retriever: Callable[[], Awaitable[T]],
    is_terminal: Callable[[T], bool],
    config: Optional[PollingConfig] = None,
) -> T:
    """
    Poll until a condition is met or timeout/max attempts are reached.
    
    Args:
        retriever: Async or sync callable that returns the object to check
        is_terminal: Callable that returns True when polling should stop
        config: Optional polling configuration
        
    Returns:
        The final state of the polled object
        
    Raises:
        PollingTimeout: When max attempts or timeout is reached
    """
    if config is None:
        config = PollingConfig()
    
    attempts = 0
    start_time = time.time()
    last_result: Union[T, None] = None
    
    while True:
        last_result = await retriever()
        
        if is_terminal(last_result):
            return last_result
            
        attempts += 1
        if attempts >= config.max_attempts:
            raise PollingTimeout(
                f"Exceeded maximum attempts ({config.max_attempts})",
                last_result
            )
            
        if config.timeout_seconds is not None:
            elapsed = time.time() - start_time
            if elapsed >= config.timeout_seconds:
                raise PollingTimeout(
                    f"Exceeded timeout of {config.timeout_seconds} seconds",
                    last_result
                )
                
        await asyncio.sleep(config.interval_seconds)
