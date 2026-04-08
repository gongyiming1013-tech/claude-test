"""Tests for ThreadSafeCache wrapper."""

import sys
import os
import threading
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from lru_cache import LRUCache
from thread_safe_cache import ThreadSafeCache
from exceptions import CacheKeyError


class TestThreadSafeCacheBasic:
    """Verify ThreadSafeCache delegates correctly to the inner cache."""

    def test_put_and_get(self) -> None:
        cache = ThreadSafeCache(LRUCache(capacity=5))
        cache.put("a", 1)
        assert cache.get("a") == 1

    def test_get_missing_returns_none(self) -> None:
        cache = ThreadSafeCache(LRUCache(capacity=5))
        assert cache.get("x") is None

    def test_delete(self) -> None:
        cache = ThreadSafeCache(LRUCache(capacity=5))
        cache.put("a", 1)
        cache.delete("a")
        assert cache.get("a") is None

    def test_delete_missing_raises(self) -> None:
        cache = ThreadSafeCache(LRUCache(capacity=5))
        with pytest.raises(CacheKeyError):
            cache.delete("x")

    def test_clear(self) -> None:
        cache = ThreadSafeCache(LRUCache(capacity=5))
        cache.put("a", 1)
        cache.put("b", 2)
        cache.clear()
        assert cache.size == 0

    def test_size_and_len(self) -> None:
        cache = ThreadSafeCache(LRUCache(capacity=5))
        cache.put("a", 1)
        assert cache.size == 1
        assert len(cache) == 1

    def test_eviction_through_wrapper(self) -> None:
        cache = ThreadSafeCache(LRUCache(capacity=2))
        cache.put("a", 1)
        cache.put("b", 2)
        cache.put("c", 3)
        assert cache.get("a") is None
        assert cache.get("c") == 3


class TestThreadSafeCacheConcurrency:
    """Verify thread safety under concurrent access."""

    def test_concurrent_puts_no_crash(self) -> None:
        """Multiple threads writing should not corrupt the cache."""
        cache = ThreadSafeCache(LRUCache(capacity=100))
        errors: list[Exception] = []

        def writer(start: int) -> None:
            try:
                for i in range(100):
                    cache.put(f"key-{start}-{i}", i)
            except Exception as e:
                errors.append(e)

        threads = [threading.Thread(target=writer, args=(t,)) for t in range(10)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert len(errors) == 0
        assert cache.size <= 100

    def test_concurrent_reads_and_writes(self) -> None:
        """Mixed read/write workload should not crash or corrupt data."""
        cache = ThreadSafeCache(LRUCache(capacity=50))
        errors: list[Exception] = []

        # Pre-populate
        for i in range(50):
            cache.put(f"key-{i}", i)

        def reader() -> None:
            try:
                for i in range(50):
                    cache.get(f"key-{i}")
            except Exception as e:
                errors.append(e)

        def writer() -> None:
            try:
                for i in range(50):
                    cache.put(f"new-{i}", i * 10)
            except Exception as e:
                errors.append(e)

        threads = []
        for _ in range(5):
            threads.append(threading.Thread(target=reader))
            threads.append(threading.Thread(target=writer))

        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert len(errors) == 0
        assert cache.size <= 50

    def test_concurrent_delete_and_put(self) -> None:
        """Concurrent deletes and puts should not raise unexpected errors."""
        cache = ThreadSafeCache(LRUCache(capacity=20))
        errors: list[Exception] = []

        for i in range(20):
            cache.put(f"key-{i}", i)

        def deleter() -> None:
            for i in range(20):
                try:
                    cache.delete(f"key-{i}")
                except CacheKeyError:
                    pass  # Another thread may have already deleted it
                except Exception as e:
                    errors.append(e)

        def putter() -> None:
            try:
                for i in range(20):
                    cache.put(f"put-{i}", i)
            except Exception as e:
                errors.append(e)

        t1 = threading.Thread(target=deleter)
        t2 = threading.Thread(target=putter)
        t1.start()
        t2.start()
        t1.join()
        t2.join()

        assert len(errors) == 0
