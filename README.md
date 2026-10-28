# py-resilience ⚡

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://www.python.org/)
[![Zero Dependencies](https://img.shields.io/badge/Dependencies-0-brightgreen.svg)](https://github.com/MilindChatrabhuji/py-resilience)

An ultra-lightweight, **zero-dependency** Python fault-tolerance and resilience library. Inspired by Resilience4j and Polly, built for both synchronous code and modern asynchronous (`asyncio`) architectures.

---

## 🛡️ Resilience Primitives

| Pattern | Description |
| :--- | :--- |
| **Circuit Breaker** | Prevent cascading failures by failing fast when downstream services are down. |
| **Retry & Jitter** | Exponential backoff with full randomized jitter to prevent thundering herds. |
| **Fallback** | Gracefully degrade by returning cached data or backup responses when calls fail. |
| **Bulkhead** | Isolate concurrent resource consumption across threads and async tasks. |

---

## 🚀 Quickstart

### 1. Circuit Breaker

```python
from py_resilience import circuit_breaker, CircuitBreakerOpenException

# Open circuit after 3 consecutive failures; re-evaluate after 30 seconds
@circuit_breaker(failure_threshold=3, recovery_timeout=30.0)
async def query_payment_gateway(charge_id: str):
    # network request...
    pass
```

### 2. Retry with Exponential Jitter

```python
from py_resilience import retry

# Retry up to 4 times with exponential delay and randomized jitter
@retry(max_attempts=4, base_delay=0.5, max_delay=10.0, retry_on=(ConnectionError, TimeoutError))
def fetch_remote_metrics():
    # network call...
    pass
```

### 3. Graceful Fallback

```python
from py_resilience import fallback

async def get_cached_feed(user_id: str):
    return {"status": "degraded", "items": ["cached_post_1", "cached_post_2"]}

@fallback(fallback_handler=get_cached_feed)
async def get_live_feed(user_id: str):
    # calls upstream service that might fail...
    pass
```

---

## 🧪 Testing

```bash
python -m pytest tests
```

---

## 📄 License
Released under the [MIT License](LICENSE). Architected by [Milind Chatrabhuji](https://github.com/MilindChatrabhuji).
