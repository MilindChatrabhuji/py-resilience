"""
py-resilience: Zero-dependency fault tolerance and resilience primitives for Python.
"""
__version__ = "0.1.0"

from .circuit_breaker import CircuitBreaker, CircuitBreakerOpenException, circuit_breaker
from .retry import retry
from .fallback import fallback
from .bulkhead import Bulkhead, bulkhead

__all__ = [
    "CircuitBreaker",
    "CircuitBreakerOpenException",
    "circuit_breaker",
    "retry",
    "fallback",
    "Bulkhead",
    "bulkhead",
]
