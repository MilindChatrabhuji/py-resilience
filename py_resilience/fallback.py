import asyncio
from functools import wraps
from typing import Callable, Any, Tuple, Type

def fallback(fallback_handler: Callable, on_exceptions: Tuple[Type[Exception], ...] = (Exception,)) -> Callable:
    """Executes a fallback function if primary function raises specified exceptions."""
    def decorator(func: Callable) -> Callable:
        if asyncio.iscoroutinefunction(func):
            @wraps(func)
            async def async_wrapper(*args, **kwargs):
                try:
                    return await func(*args, **kwargs)
                except on_exceptions:
                    if asyncio.iscoroutinefunction(fallback_handler):
                        return await fallback_handler(*args, **kwargs)
                    return fallback_handler(*args, **kwargs)
            return async_wrapper
        else:
            @wraps(func)
            def sync_wrapper(*args, **kwargs):
                try:
                    return func(*args, **kwargs)
                except on_exceptions:
                    return fallback_handler(*args, **kwargs)
            return sync_wrapper
    return decorator
