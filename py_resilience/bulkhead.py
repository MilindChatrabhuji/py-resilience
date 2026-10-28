import asyncio
import threading
from functools import wraps
from typing import Callable

class Bulkhead:
    """Limits concurrent executions across threads or coroutines."""
    def __init__(self, max_concurrent: int = 10):
        self.semaphore_sync = threading.Semaphore(max_concurrent)
        self.semaphore_async = None
        self.max_concurrent = max_concurrent

    def __call__(self, func: Callable) -> Callable:
        if asyncio.iscoroutinefunction(func):
            @wraps(func)
            async def async_wrapper(*args, **kwargs):
                if self.semaphore_async is None:
                    self.semaphore_async = asyncio.Semaphore(self.max_concurrent)
                async with self.semaphore_async:
                    return await func(*args, **kwargs)
            return async_wrapper
        else:
            @wraps(func)
            def sync_wrapper(*args, **kwargs):
                with self.semaphore_sync:
                    return func(*args, **kwargs)
            return sync_wrapper

def bulkhead(max_concurrent: int = 10) -> Callable:
    return Bulkhead(max_concurrent)
