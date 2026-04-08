"""Tests for MonitoredCache wrapper."""

import sys
import os
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from lru_cache import LRUCache
from monitored_cache import MonitoredCache


class TestMonitoredCacheBasic:
    """Verify MonitoredCache delegates correctly and does not alter behavior."""

    def test_put_and_get(self) -> None:
        cache = MonitoredCache(LRUCache(capacity=5))
        cache.put("a", 1)
        assert cache.get("a") == 1

    def test_get_missing_returns_none(self) -> None:
        cache = MonitoredCache(LRUCache(capacity=5))
        assert cache.get("x") is None

    def test_delete(self) -> None:
        cache = MonitoredCache(LRUCache(capacity=5))
        cache.put("a", 1)
        cache.delete("a")
        assert cache.get("a") is None

    def test_clear(self) -> None:
        cache = MonitoredCache(LRUCache(capacity=5))
        cache.put("a", 1)
        cache.put("b", 2)
        cache.clear()
        assert cache.size == 0

    def test_size_and_len(self) -> None:
        cache = MonitoredCache(LRUCache(capacity=5))
        cache.put("a", 1)
        assert cache.size == 1
        assert len(cache) == 1

    def test_eviction_through_wrapper(self) -> None:
        cache = MonitoredCache(LRUCache(capacity=2))
        cache.put("a", 1)
        cache.put("b", 2)
        cache.put("c", 3)
        assert cache.get("a") is None
        assert cache.get("c") == 3


class TestMonitoredCacheHitMiss:
    """Verify hit/miss counting logic."""

    def test_initial_stats_are_zero(self) -> None:
        cache = MonitoredCache(LRUCache(capacity=5))
        assert cache.hits == 0
        assert cache.misses == 0

    def test_hit_increments_on_existing_key(self) -> None:
        cache = MonitoredCache(LRUCache(capacity=5))
        cache.put("a", 1)
        cache.get("a")
        assert cache.hits == 1
        assert cache.misses == 0

    def test_miss_increments_on_missing_key(self) -> None:
        cache = MonitoredCache(LRUCache(capacity=5))
        cache.get("nonexistent")
        assert cache.hits == 0
        assert cache.misses == 1

    def test_multiple_hits_and_misses(self) -> None:
        cache = MonitoredCache(LRUCache(capacity=5))
        cache.put("a", 1)
        cache.put("b", 2)
        cache.get("a")  # hit
        cache.get("b")  # hit
        cache.get("c")  # miss
        cache.get("a")  # hit
        cache.get("d")  # miss
        assert cache.hits == 3
        assert cache.misses == 2

    def test_evicted_key_counts_as_miss(self) -> None:
        cache = MonitoredCache(LRUCache(capacity=2))
        cache.put("a", 1)
        cache.put("b", 2)
        cache.put("c", 3)  # evicts "a"
        cache.get("a")     # miss
        assert cache.misses == 1


class TestMonitoredCacheHitRate:
    """Verify hit_rate calculation."""

    def test_hit_rate_no_requests(self) -> None:
        """Hit rate should be 0.0 when no get requests have been made."""
        cache = MonitoredCache(LRUCache(capacity=5))
        assert cache.hit_rate == 0.0

    def test_hit_rate_all_hits(self) -> None:
        cache = MonitoredCache(LRUCache(capacity=5))
        cache.put("a", 1)
        cache.get("a")
        cache.get("a")
        cache.get("a")
        assert cache.hit_rate == 1.0

    def test_hit_rate_all_misses(self) -> None:
        cache = MonitoredCache(LRUCache(capacity=5))
        cache.get("x")
        cache.get("y")
        assert cache.hit_rate == 0.0

    def test_hit_rate_mixed(self) -> None:
        cache = MonitoredCache(LRUCache(capacity=5))
        cache.put("a", 1)
        cache.get("a")  # hit
        cache.get("b")  # miss
        cache.get("a")  # hit
        cache.get("c")  # miss
        # 2 hits / 4 total = 0.5
        assert cache.hit_rate == 0.5


class TestMonitoredCacheStats:
    """Verify stats dict and reset functionality."""

    def test_stats_returns_correct_dict(self) -> None:
        cache = MonitoredCache(LRUCache(capacity=5))
        cache.put("a", 1)
        cache.get("a")  # hit
        cache.get("b")  # miss
        stats = cache.stats
        assert stats["hits"] == 1
        assert stats["misses"] == 1
        assert stats["hit_rate"] == 0.5
        assert stats["total_requests"] == 2

    def test_reset_stats(self) -> None:
        cache = MonitoredCache(LRUCache(capacity=5))
        cache.put("a", 1)
        cache.get("a")
        cache.get("b")
        cache.reset_stats()
        assert cache.hits == 0
        assert cache.misses == 0
        assert cache.hit_rate == 0.0

    def test_reset_does_not_affect_cache_data(self) -> None:
        """Resetting stats should not clear the cache itself."""
        cache = MonitoredCache(LRUCache(capacity=5))
        cache.put("a", 1)
        cache.get("a")
        cache.reset_stats()
        # Data still in cache
        assert cache.get("a") == 1
        # New stats after reset
        assert cache.hits == 1
        assert cache.misses == 0
