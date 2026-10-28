import time
import random
import asyncio
from functools import wraps
from typing import Callable, Tuple, Type

def retry(
    max_attempts: int = 3,
    base_delay: float = 0.5,
    max_delay: float = 10.0,
    backoff_factor: float = 2.0,
    jitter: bool = True,
    retry_on: Tuple[Type[Exception], ...] = (Exception,)
) -> Callable:
    """Retry decorator with exponential backoff and full jitter."""
    def decorator(func: Callable) -> Callable:
        if asyncio.iscoroutinefunction(func):
            @wraps(func)
            async def async_wrapper(*args, **kwargs):
                attempts = 0
                while True:
                    attempts += 1
                    try:
                        return await func(*args, **kwargs)
                    except retry_on as e:
                        if attempts >= max_attempts:
                            raise e
                        delay = min(max_delay, base_delay * (backoff_factor ** (attempts - 1)))
                        if jitter:
                            delay = random.uniform(0, delay)
                        await asyncio.sleep(delay)
            return async_wrapper
        else:
            @wraps(func)
            def sync_wrapper(*args, **kwargs):
                attempts = 0
                while True:
                    attempts += 1
                    try:
                        return func(*args, **kwargs)
                    except retry_on as e:
                        if attempts >= max_attempts:
                            raise e
                        delay = min(max_delay, base_delay * (backoff_factor ** (attempts - 1)))
                        if jitter:
                            delay = random.uniform(0, delay)
                        time.sleep(delay)
            return sync_wrapper
    return decorator
