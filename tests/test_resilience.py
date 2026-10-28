import pytest
import asyncio
from py_resilience import circuit_breaker, CircuitBreakerOpenException, retry, fallback, bulkhead

def test_circuit_breaker_sync():
    call_count = 0

    @circuit_breaker(failure_threshold=2, recovery_timeout=0.1)
    def flaky_service():
        nonlocal call_count
        call_count += 1
        raise ValueError("Service unavailable")

    # Fail 1
    with pytest.raises(ValueError):
        flaky_service()
    # Fail 2 (trips circuit)
    with pytest.raises(ValueError):
        flaky_service()

    # Fail 3: Should raise CircuitBreakerOpenException without running func
    with pytest.raises(CircuitBreakerOpenException):
        flaky_service()

    assert call_count == 2

def test_retry_sync():
    attempts = 0

    @retry(max_attempts=3, base_delay=0.01, jitter=False)
    def flaky_call():
        nonlocal attempts
        attempts += 1
        if attempts < 3:
            raise RuntimeError("Transient error")
        return "Success"

    assert flaky_call() == "Success"
    assert attempts == 3

@pytest.mark.asyncio
async def test_fallback_async():
    async def fallback_fn(x):
        return x * 10

    @fallback(fallback_fn)
    async def failing_async(x):
        raise ConnectionError("Remote timeout")

    res = await failing_async(5)
    assert res == 50

def test_bulkhead_sync():
    @bulkhead(max_concurrent=2)
    def limited_job():
        return "Executed"

    assert limited_job() == "Executed"
