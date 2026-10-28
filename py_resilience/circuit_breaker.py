import time
import asyncio
from functools import wraps
from enum import Enum
from typing import Callable, Any, Optional

class CircuitState(Enum):
    CLOSED = "CLOSED"
    OPEN = "OPEN"
    HALF_OPEN = "HALF_OPEN"

class CircuitBreakerOpenException(Exception):
    """Raised when an operation is attempted while circuit is open."""
    pass

class CircuitBreaker:
    def __init__(self, failure_threshold: int = 5, recovery_timeout: float = 30.0, expected_exceptions=(Exception,)):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.expected_exceptions = expected_exceptions
        self.state = CircuitState.CLOSED
        self.failure_count = 0
        self.last_failure_time = 0.0

    def _before_call(self):
        now = time.time()
        if self.state == CircuitState.OPEN:
            if now - self.last_failure_time > self.recovery_timeout:
                self.state = CircuitState.HALF_OPEN
            else:
                raise CircuitBreakerOpenException("Circuit breaker is OPEN. Calls rejected.")

    def _on_success(self):
        self.failure_count = 0
        self.state = CircuitState.CLOSED

    def _on_failure(self):
        self.failure_count += 1
        self.last_failure_time = time.time()
        if self.failure_count >= self.failure_threshold:
            self.state = CircuitState.OPEN

    def __call__(self, func: Callable) -> Callable:
        if asyncio.iscoroutinefunction(func):
            @wraps(func)
            async def async_wrapper(*args, **kwargs):
                self._before_call()
                try:
                    res = await func(*args, **kwargs)
                    self._on_success()
                    return res
                except self.expected_exceptions as e:
                    self._on_failure()
                    raise e
            return async_wrapper
        else:
            @wraps(func)
            def sync_wrapper(*args, **kwargs):
                self._before_call()
                try:
                    res = func(*args, **kwargs)
                    self._on_success()
                    return res
                except self.expected_exceptions as e:
                    self._on_failure()
                    raise e
            return sync_wrapper

def circuit_breaker(failure_threshold: int = 5, recovery_timeout: float = 30.0, expected_exceptions=(Exception,)):
    cb = CircuitBreaker(failure_threshold, recovery_timeout, expected_exceptions)
    return cb
